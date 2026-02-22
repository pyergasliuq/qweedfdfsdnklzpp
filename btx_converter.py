"""
BTX <-> Image converter

BTX format: 4-byte magic \x02\x00\x00\x00 + KTX1 data (ASTC compressed texture)

Encoding (image → BTX):
  1. Load → RGBA
  2. Premultiply alpha + bleed transparent areas
  3. Pad to power-of-2
  4. Generate mipmap chain
  5. Encode each mip with astcenc → raw ASTC blocks
  6. Assemble KTX1 container
  7. Prepend BTX magic header

Decoding (BTX → image):
  1. Strip 4-byte BTX header → KTX1
  2. Parse KTX1 (format, size, mip0 data)
  3. Decode mip0 with astcenc → PNG
"""

import os
import io
import math
import struct
import shutil
import logging
import platform
import tempfile
import subprocess
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────

BTX_MAGIC = b'\x02\x00\x00\x00'
KTX1_MAGIC = b'\xabKTX 11\xbb\r\n\x1a\n'
ASTC_RAW_MAGIC = 0x5CA1AB13

# OpenGL ASTC sRGB internal formats (KHR_texture_compression_astc_hdr)
ASTC_GL_FORMAT: dict = {
    (4,  4):  0x93D0,
    (5,  4):  0x93D1,
    (5,  5):  0x93D2,
    (6,  5):  0x93D3,
    (6,  6):  0x93D4,
    (8,  5):  0x93D5,
    (8,  6):  0x93D6,
    (8,  8):  0x93D7,
    (10, 5):  0x93D8,
    (10, 6):  0x93D9,
    (10, 8):  0x93DA,
    (10, 10): 0x93DB,
    (12, 10): 0x93DC,
    (12, 12): 0x93DD,
}
GL_FORMAT_TO_ASTC: dict = {v: k for k, v in ASTC_GL_FORMAT.items()}

QUALITY_FLAGS = {
    "fast":       "-fastest",
    "medium":     "-medium",
    "thorough":   "-thorough",
    "exhaustive": "-exhaustive",
}

# ─────────────────────────────────────────────────────────
# astcenc binary management  (no root, no shell needed)
# ─────────────────────────────────────────────────────────

ASTCENC_VERSION = "4.7.0"
ASTCENC_RELEASES = "https://github.com/ARM-software/astc-encoder/releases/download"


def _astcenc_dir() -> Path:
    """Find a writable directory for the binary."""
    candidates = [
        Path.home() / ".local" / "bin",
        Path("/tmp/astcenc_bin"),
        Path(tempfile.gettempdir()) / "astcenc_bin",
    ]
    for p in candidates:
        try:
            p.mkdir(parents=True, exist_ok=True)
            test = p / ".write_test"
            test.touch()
            test.unlink()
            return p
        except OSError:
            continue
    raise RuntimeError("No writable directory found for astcenc")


def _astcenc_candidates() -> List[str]:
    d = _astcenc_dir()
    return [
        str(d / "astcenc-avx2"),
        str(d / "astcenc-sse4.1"),
        str(d / "astcenc-sse2"),
        str(d / "astcenc"),
        "astcenc-avx2",
        "astcenc",
    ]


def find_astcenc() -> Optional[str]:
    for c in _astcenc_candidates():
        if shutil.which(c):
            return c
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def download_astcenc() -> str:
    d = _astcenc_dir()
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        pkg = (
            f"astcenc-{ASTCENC_VERSION}-linux-aarch64.zip"
            if ("aarch64" in machine or "arm64" in machine)
            else f"astcenc-{ASTCENC_VERSION}-linux-x64.zip"
        )
    elif system == "darwin":
        pkg = f"astcenc-{ASTCENC_VERSION}-macos-universal.zip"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    url = f"{ASTCENC_RELEASES}/{ASTCENC_VERSION}/{pkg}"
    zip_path = d / pkg

    logger.info(f"Downloading astcenc {ASTCENC_VERSION} …  {url}")
    with urllib.request.urlopen(url) as r:
        total = int(r.headers.get("Content-Length", 0))
        downloaded = 0
        with open(zip_path, "wb") as f:
            while chunk := r.read(65536):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    logger.info(f"  {downloaded * 100 // total}%")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(d)
    zip_path.unlink(missing_ok=True)

    for f in d.iterdir():
        if f.name.startswith("astcenc") and f.is_file():
            os.chmod(f, 0o755)

    binary = find_astcenc()
    if not binary:
        raise RuntimeError("astcenc not found after download")
    logger.info(f"astcenc ready: {binary}")
    return binary


def ensure_astcenc() -> str:
    b = find_astcenc()
    return b if b else download_astcenc()


# ─────────────────────────────────────────────────────────
# Image processing helpers
# ─────────────────────────────────────────────────────────

def _premultiply_alpha(img: Image.Image) -> Image.Image:
    arr = np.array(img, dtype=np.float32)
    a = arr[:, :, 3:4] / 255.0
    arr[:, :, :3] = np.clip(arr[:, :, :3] * a, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def _bleed(img: Image.Image, iterations: int = 16) -> Image.Image:
    arr = np.array(img, dtype=np.uint8).copy()
    h, w = arr.shape[:2]
    for _ in range(iterations):
        alpha = arr[:, :, 3]
        transparent = alpha == 0
        if not np.any(transparent):
            break
        padded = np.pad(arr, ((1, 1), (1, 1), (0, 0)), mode="edge")
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nb = padded[1 + dy:1 + dy + h, 1 + dx:1 + dx + w]
            fill = transparent & (nb[:, :, 3] > 0)
            arr[fill, :3] = nb[fill, :3]
    return Image.fromarray(arr, "RGBA")


def _pad_pow2(img: Image.Image) -> Image.Image:
    def np2(n):
        return 1 << math.ceil(math.log2(max(n, 1)))
    w, h = img.size
    nw, nh = np2(w), np2(h)
    if nw == w and nh == h:
        return img
    out = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
    out.paste(img, (0, 0))
    return out


def _gen_mipmaps(img: Image.Image) -> List[Image.Image]:
    mips = [img]
    w, h = img.size
    while w > 1 or h > 1:
        w, h = max(1, w // 2), max(1, h // 2)
        mips.append(img.resize((w, h), Image.LANCZOS))
    return mips


# ─────────────────────────────────────────────────────────
# Raw .astc container
# ─────────────────────────────────────────────────────────

def _make_astc_file(data: bytes, w: int, h: int, bw: int, bh: int) -> bytes:
    hdr = struct.pack("<I", ASTC_RAW_MAGIC)
    hdr += bytes([bw, bh, 1])
    hdr += struct.pack("<I", w)[:3]
    hdr += struct.pack("<I", h)[:3]
    hdr += b"\x01\x00\x00"
    return hdr + data


# ─────────────────────────────────────────────────────────
# KTX1 container
# ─────────────────────────────────────────────────────────

def _parse_ktx1(data: bytes) -> dict:
    if not data.startswith(KTX1_MAGIC):
        raise ValueError("Not a KTX1 file")
    off = 12
    fields = struct.unpack_from("<13I", data, off)
    off += 52
    (*_, gl_internal_format, _, pixel_width, pixel_height, _,
     _, _, num_mip_levels, bytes_kv) = fields
    off += bytes_kv
    block = GL_FORMAT_TO_ASTC.get(gl_internal_format)
    if block is None:
        raise ValueError(f"Unsupported KTX format: {gl_internal_format:#010x}")
    bw, bh = block
    mips = []
    for _ in range(max(num_mip_levels, 1)):
        if off + 4 > len(data):
            break
        size = struct.unpack_from("<I", data, off)[0]
        off += 4
        mips.append(data[off: off + size])
        off += (size + 3) & ~3
    return {"width": pixel_width, "height": pixel_height,
            "block_w": bw, "block_h": bh, "mip_data_list": mips}


def _make_ktx1(mips: List[bytes], w: int, h: int, bw: int, bh: int) -> bytes:
    gl_fmt = ASTC_GL_FORMAT.get((bw, bh))
    if not gl_fmt:
        raise ValueError(f"Unknown ASTC block: {bw}x{bh}")
    out = KTX1_MAGIC
    out += struct.pack("<13I",
                       0x04030201, 0, 1, 0, gl_fmt, 0x1908,
                       w, h, 0, 0, 1, len(mips), 0)
    for mip in mips:
        pad = (len(mip) + 3) & ~3
        out += struct.pack("<I", len(mip)) + mip + b"\x00" * (pad - len(mip))
    return out


# ─────────────────────────────────────────────────────────
# astcenc wrappers
# ─────────────────────────────────────────────────────────

def _astcenc_encode(png: str, astc: str, block: str, quality: str, bin: str):
    flag = QUALITY_FLAGS.get(quality, "-medium")
    r = subprocess.run([bin, "-cl", png, astc, block, flag],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"astcenc encode failed:\n{r.stdout}\n{r.stderr}")


def _astcenc_decode(astc: str, png: str, block: str, bin: str):
    r = subprocess.run([bin, "-dl", astc, png, block],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"astcenc decode failed:\n{r.stdout}\n{r.stderr}")


# ─────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────

def image_to_btx(
    image_path: str,
    btx_path: str,
    compress_mode: str = "4x4",
    quality_mode: str = "medium",
    astcenc_bin: Optional[str] = None,
) -> None:
    """Convert any image (PNG/JPG/BMP/WEBP/TIFF…) → BTX."""
    if astcenc_bin is None:
        astcenc_bin = ensure_astcenc()

    bw, bh = (int(x) for x in compress_mode.split("x"))

    with tempfile.TemporaryDirectory(prefix="btx_enc_") as tmp:
        tmp = Path(tmp)
        img = Image.open(image_path).convert("RGBA")
        img = _pad_pow2(img)
        orig_w, orig_h = img.size
        img = _premultiply_alpha(img)
        img = _bleed(img)
        mips = _gen_mipmaps(img)
        logger.info(f"BTX encode: {orig_w}x{orig_h}, {len(mips)} mips, ASTC {compress_mode}")

        compressed = []
        for i, mip in enumerate(mips):
            mip_png = str(tmp / f"m{i}.png")
            mip_astc = str(tmp / f"m{i}.astc")
            mip.save(mip_png, "PNG")
            _astcenc_encode(mip_png, mip_astc, compress_mode, quality_mode, astcenc_bin)
            with open(mip_astc, "rb") as f:
                compressed.append(f.read()[16:])  # strip 16-byte .astc header

        ktx = _make_ktx1(compressed, orig_w, orig_h, bw, bh)
        os.makedirs(os.path.dirname(btx_path) or ".", exist_ok=True)
        with open(btx_path, "wb") as f:
            f.write(BTX_MAGIC + ktx)

    logger.info(f"BTX written: {btx_path}")


def btx_to_image(
    btx_path: str,
    output_path: str,
    astcenc_bin: Optional[str] = None,
) -> str:
    """Convert BTX → image (format from extension). Returns output_path."""
    if astcenc_bin is None:
        astcenc_bin = ensure_astcenc()

    with open(btx_path, "rb") as f:
        raw = f.read()
    if raw[:4] != BTX_MAGIC:
        raise ValueError(f"Invalid BTX magic: {raw[:4].hex()}")

    ktx = _parse_ktx1(raw[4:])
    bw, bh = ktx["block_w"], ktx["block_h"]
    w, h = ktx["width"], ktx["height"]
    mip0 = ktx["mip_data_list"][0]
    block_str = f"{bw}x{bh}"
    logger.info(f"BTX decode: {w}x{h} ASTC {block_str}")

    with tempfile.TemporaryDirectory(prefix="btx_dec_") as tmp:
        tmp = Path(tmp)
        astc_file = _make_astc_file(mip0, w, h, bw, bh)
        astc_path = str(tmp / "mip0.astc")
        with open(astc_path, "wb") as f:
            f.write(astc_file)

        decoded_png = str(tmp / "decoded.png")
        _astcenc_decode(astc_path, decoded_png, block_str, astcenc_bin)

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        Image.open(decoded_png).save(output_path)

    logger.info(f"Image written: {output_path}")
    return output_path
