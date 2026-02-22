"""
BTX <-> Image converter — pure Python, no subprocess, no external binaries.

Uses `imagecodecs` for ASTC encode/decode (compiled Python extension,
installed via pip, no system packages or binaries needed).

BTX format: 4 bytes magic \x02\x00\x00\x00 + KTX1 binary data
KTX1 contains ASTC compressed texture (4x4, 6x6, or 8x8 blocks)

Encoding pipeline (image → BTX):
  1. Load image → RGBA numpy array
  2. Premultiply alpha
  3. Bleed colors into transparent areas (prevents dark halos)
  4. Pad to power-of-2 dimensions
  5. Generate mipmap chain
  6. Encode each mip with imagecodecs.astc_encode
  7. Assemble KTX1 container
  8. Prepend BTX header  (\x02\x00\x00\x00)

Decoding pipeline (BTX → image):
  1. Strip 4-byte BTX header → KTX1 bytes
  2. Parse KTX1 header (ASTC block size, dimensions, mip data)
  3. Decode mip0 with imagecodecs.astc_decode
  4. Save via Pillow
"""

import os
import struct
import math
import logging
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image

try:
    import imagecodecs
    _HAS_IMAGECODECS = True
except ImportError:
    _HAS_IMAGECODECS = False

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

def check_dependencies() -> None:
    """Raise a clear error if imagecodecs (with ASTC) is not available."""
    if not _HAS_IMAGECODECS:
        raise ImportError(
            "imagecodecs is not installed.\n"
            "Run:  pip install imagecodecs\n"
            "Wheels are available for Linux / macOS / Windows (x64 and arm64)."
        )
    if not imagecodecs.astc_check(enums=False):
        raise RuntimeError(
            "Your imagecodecs build does not include the ASTC codec.\n"
            "Try:  pip install --force-reinstall imagecodecs"
        )


# ---------------------------------------------------------------------------
# BTX / KTX1 constants
# ---------------------------------------------------------------------------

BTX_MAGIC  = b'\x02\x00\x00\x00'
KTX1_MAGIC = b'\xabKTX 11\xbb\r\n\x1a\n'

# OpenGL ASTC sRGB internal format codes (GL_KHR_texture_compression_astc_hdr)
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

# imagecodecs quality levels (0 = fastest … 100 = exhaustive)
QUALITY_LEVELS = {
    "fast":       10,
    "medium":     60,
    "thorough":   80,
    "exhaustive": 100,
}


# ---------------------------------------------------------------------------
# KTX1 parsing / assembly
# ---------------------------------------------------------------------------

def parse_ktx1(data: bytes) -> dict:
    """
    Parse KTX1 binary → dict:
      width, height, block_w, block_h, mip_data_list
    """
    if data[:12] != KTX1_MAGIC:
        raise ValueError(f"Not a KTX1 file (magic bytes: {data[:12].hex()})")

    off = 12
    (endianness, gl_type, gl_type_size, gl_format,
     gl_internal_format, gl_base_internal_format,
     pixel_width, pixel_height, pixel_depth,
     num_array_elements, num_faces, num_mip_levels,
     bytes_kv_data) = struct.unpack_from("<13I", data, off)
    off += 13 * 4 + bytes_kv_data

    block = GL_FORMAT_TO_ASTC.get(gl_internal_format)
    if block is None:
        raise ValueError(
            f"Unsupported KTX internal format: {gl_internal_format:#010x}\n"
            "Only ASTC sRGB formats (4x4 / 6x6 / 8x8 etc.) are supported."
        )

    bw, bh = block
    mip_data_list: List[bytes] = []
    for _ in range(max(num_mip_levels, 1)):
        if off + 4 > len(data):
            break
        image_size = struct.unpack_from("<I", data, off)[0]
        off += 4
        mip_data_list.append(data[off: off + image_size])
        off += (image_size + 3) & ~3  # 4-byte padding

    return {
        "width":         pixel_width,
        "height":        pixel_height,
        "block_w":       bw,
        "block_h":       bh,
        "mip_data_list": mip_data_list,
    }


def make_ktx1(mip_levels: List[bytes], width: int, height: int, bw: int, bh: int) -> bytes:
    """Assemble KTX1 binary from a list of compressed mip data blobs."""
    gl_format = ASTC_GL_FORMAT.get((bw, bh))
    if gl_format is None:
        raise ValueError(f"Unknown ASTC block size: {bw}x{bh}")

    out = KTX1_MAGIC
    out += struct.pack(
        "<13I",
        0x04030201,  # endianness marker
        0,           # glType = 0 (compressed)
        1,           # glTypeSize
        0,           # glFormat = 0 (compressed)
        gl_format,   # glInternalFormat
        0x1908,      # glBaseInternalFormat = GL_RGBA
        width, height, 0,
        0,           # numberOfArrayElements
        1,           # numberOfFaces
        len(mip_levels),
        0,           # bytesOfKeyValueData
    )
    for mip in mip_levels:
        padded = (len(mip) + 3) & ~3
        out += struct.pack("<I", len(mip))
        out += mip
        out += b"\x00" * (padded - len(mip))

    return out


# ---------------------------------------------------------------------------
# Image processing helpers
# ---------------------------------------------------------------------------

def to_rgba_array(img: Image.Image) -> np.ndarray:
    return np.array(img.convert("RGBA"), dtype=np.uint8)


def premultiply_alpha(arr: np.ndarray) -> np.ndarray:
    """Premultiply RGB by alpha (matches PVRTexLib PreMultiplyAlpha)."""
    a = arr[:, :, 3:4].astype(np.float32) / 255.0
    out = arr.astype(np.float32)
    out[:, :, :3] *= a
    return np.clip(out, 0, 255).astype(np.uint8)


def bleed(arr: np.ndarray, iterations: int = 16) -> np.ndarray:
    """
    Fill transparent pixels with neighbour opaque colors (matches PVRTexLib Bleed).
    Prevents dark-halo artifacts around semi-transparent edges after mipmapping.
    """
    arr = arr.copy()
    h, w = arr.shape[:2]
    for _ in range(iterations):
        transparent = arr[:, :, 3] == 0
        if not np.any(transparent):
            break
        padded = np.pad(arr, ((1, 1), (1, 1), (0, 0)), mode="edge")
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nb = padded[1 + dy: 1 + dy + h, 1 + dx: 1 + dx + w]
            mask = transparent & (nb[:, :, 3] > 0)
            arr[mask, :3] = nb[mask, :3]
    return arr


def next_pow2(n: int) -> int:
    return 1 << math.ceil(math.log2(max(n, 1)))


def pad_to_pow2(arr: np.ndarray) -> np.ndarray:
    """Pad image canvas to power-of-2 dimensions (required for full mip chain)."""
    h, w = arr.shape[:2]
    nh, nw = next_pow2(h), next_pow2(w)
    if nh == h and nw == w:
        return arr
    out = np.zeros((nh, nw, 4), dtype=np.uint8)
    out[:h, :w] = arr
    return out


def generate_mipmaps(arr: np.ndarray) -> List[np.ndarray]:
    """Generate full mip chain (matches PVRTexLib GenerateMIPMaps Linear)."""
    mips = [arr]
    h, w = arr.shape[:2]
    img = Image.fromarray(arr, "RGBA")
    while w > 1 or h > 1:
        w = max(1, w // 2)
        h = max(1, h // 2)
        mip_img = img.resize((w, h), Image.LANCZOS)
        mips.append(np.array(mip_img, dtype=np.uint8))
    return mips


# ---------------------------------------------------------------------------
# ASTC encode / decode via imagecodecs (no subprocess, no external binary)
# ---------------------------------------------------------------------------

def encode_astc(arr: np.ndarray, bw: int, bh: int, quality: str) -> bytes:
    """
    Encode uint8 RGBA numpy array (H, W, 4) → raw ASTC block bytes.
    No subprocess, no external binary — uses imagecodecs compiled extension.
    """
    level = QUALITY_LEVELS.get(quality, 60)
    compressed = imagecodecs.astc_encode(arr, level=level, blocksize=(bw, bh, 1))
    return bytes(compressed)


def decode_astc(blocks: bytes, width: int, height: int, bw: int, bh: int) -> np.ndarray:
    """
    Decode raw ASTC block bytes → uint8 RGBA numpy array (H, W, 4).
    No subprocess, no external binary — uses imagecodecs compiled extension.
    """
    arr = imagecodecs.astc_decode(
        blocks,
        shape=(height, width, 4),
        blocksize=(bw, bh, 1),
    )
    return np.asarray(arr, dtype=np.uint8)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def image_to_btx(
    image_path: str,
    btx_path: str,
    compress_mode: str = "4x4",
    quality_mode: str = "medium",
) -> None:
    """
    Convert any image (PNG / JPG / BMP / WEBP / TIFF / TGA …) to BTX.

    Parameters
    ----------
    image_path    : source image file
    btx_path      : output .btx file
    compress_mode : ASTC block size — "4x4" | "6x6" | "8x8"
    quality_mode  : "fast" | "medium" | "thorough" | "exhaustive"
    """
    check_dependencies()

    bw, bh = (int(x) for x in compress_mode.split("x"))

    # 1. Load → RGBA uint8 array
    arr = to_rgba_array(Image.open(image_path))
    logger.info(f"Loaded: {image_path}  {arr.shape[1]}x{arr.shape[0]}")

    # 2. Pad to power-of-2
    arr = pad_to_pow2(arr)
    orig_h, orig_w = arr.shape[:2]

    # 3. Premultiply alpha
    arr = premultiply_alpha(arr)

    # 4. Bleed transparent areas
    arr = bleed(arr)

    # 5. Generate mip chain
    mips = generate_mipmaps(arr)
    logger.info(f"Mip levels: {len(mips)}  (base {orig_w}x{orig_h})")

    # 6. Encode each mip
    compressed_mips: List[bytes] = []
    for idx, mip in enumerate(mips):
        h, w = mip.shape[:2]
        blocks = encode_astc(mip, bw, bh, quality_mode)
        compressed_mips.append(blocks)
        logger.info(f"  mip {idx}: {w}x{h} → {len(blocks)} bytes")

    # 7. Assemble KTX1
    ktx_data = make_ktx1(compressed_mips, orig_w, orig_h, bw, bh)

    # 8. Write BTX = 4-byte magic + KTX1
    os.makedirs(os.path.dirname(btx_path) or ".", exist_ok=True)
    with open(btx_path, "wb") as f:
        f.write(BTX_MAGIC + ktx_data)

    size_kb = Path(btx_path).stat().st_size / 1024
    logger.info(f"BTX written: {btx_path}  ({size_kb:.1f} KB)")


def btx_to_image(btx_path: str, output_path: str) -> str:
    """
    Convert BTX → image.
    Output format is determined by the extension of output_path.
    Returns output_path.
    """
    check_dependencies()

    with open(btx_path, "rb") as f:
        raw = f.read()

    if raw[:4] != BTX_MAGIC:
        raise ValueError(f"Not a valid BTX file (bad magic: {raw[:4].hex()})")

    ktx = parse_ktx1(raw[4:])
    bw, bh = ktx["block_w"], ktx["block_h"]
    width, height = ktx["width"], ktx["height"]
    mip0 = ktx["mip_data_list"][0]

    logger.info(f"BTX: {width}x{height}  ASTC {bw}x{bh}  {len(ktx['mip_data_list'])} mips")

    rgba = decode_astc(mip0, width, height, bw, bh)
    img  = Image.fromarray(rgba, "RGBA")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path)

    logger.info(f"Saved: {output_path}")
    return output_path
