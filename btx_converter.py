"""
BTX ↔ Image converter — полная реализация пайплайна PVRTexLib на чистом Python.

Пайплайн ПОЛНОСТЬЮ соответствует btx_editor (C++ / PVRTexLib):
  PNG → BTX:
    1. Загрузка → RGBA uint8
    2. PreMultiplyAlpha  (RGB *= A/255)
    3. Bleed             (заливка прозрачных пикселей цветами соседей)
    4. GenerateMIPMaps   (Linear / LANCZOS, полная цепочка до 1×1)
    5. Pad to pow-of-2   (если нужно)
    6. ASTC encode каждого mip (4×4 / 6×6 / 8×8, fast/medium/thorough/exhaustive)
    7. Сборка KTX1 контейнера
    8. Prepend BTX magic  \x02\x00\x00\x00

  BTX → PNG:
    1. Strip 4-byte BTX header → KTX1
    2. Parse KTX1 (блок, размеры, mip-данные)
    3. Декодировать mip0 ASTC → RGBA
    4. Сохранить через Pillow

Зависимости (pip install):
    imagecodecs   — ASTC кодек (основной, нет subprocess/бинарников)
    numpy
    Pillow

Опционально (лучше качество):
    pvrtex        — Python-обёртка над PVRTexLib (pip install pvrtex)
                    если установлен — используется автоматически.
"""

from __future__ import annotations

import os
import struct
import math
import logging
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Бэкенды кодирования — пробуем в порядке приоритета
# ─────────────────────────────────────────────────────────────────────────────

_BACKEND: str = "none"

try:
    import pvrtex  # type: ignore
    _BACKEND = "pvrtex"
    logger.info("BTX backend: pvrtex (PVRTexLib Python bindings)")
except ImportError:
    pass

if _BACKEND == "none":
    try:
        import imagecodecs  # type: ignore
        if imagecodecs.astc_check(enums=False):
            _BACKEND = "imagecodecs"
            logger.info("BTX backend: imagecodecs (ASTC)")
        else:
            logger.warning("imagecodecs установлен, но без ASTC поддержки")
    except ImportError:
        pass

if _BACKEND == "none":
    logger.error(
        "Нет доступного ASTC бэкенда!\n"
        "  pip install imagecodecs   (основной)\n"
        "  pip install pvrtex        (опциональный, лучшее качество)"
    )


def check_dependencies() -> None:
    """Проверить зависимости и поднять исключение если ни один бэкенд не доступен."""
    if _BACKEND == "none":
        raise ImportError(
            "Не установлен ни один ASTC кодек.\n"
            "Установи: pip install imagecodecs\n"
            "Или:      pip install pvrtex"
        )


# ─────────────────────────────────────────────────────────────────────────────
# BTX / KTX1 константы
# ─────────────────────────────────────────────────────────────────────────────

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

# Уровни качества → imagecodecs level (0=fast … 100=exhaustive)
QUALITY_LEVELS_IC = {
    "fast":       10,
    "medium":     60,
    "thorough":   80,
    "exhaustive": 100,
}

# Уровни качества → pvrtex enum names
QUALITY_LEVELS_PVR = {
    "fast":       "ASTCFast",
    "medium":     "ASTCMedium",
    "thorough":   "ASTCThorough",
    "exhaustive": "ASTCExhaustive",
}


# ─────────────────────────────────────────────────────────────────────────────
# KTX1 парсинг / сборка
# ─────────────────────────────────────────────────────────────────────────────

def parse_ktx1(data: bytes) -> dict:
    """Разобрать KTX1 binary → dict: width, height, block_w, block_h, mip_data_list."""
    if data[:12] != KTX1_MAGIC:
        raise ValueError(f"Не KTX1 (magic: {data[:12].hex()})")

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
            f"Неподдерживаемый KTX internal format: {gl_internal_format:#010x}\n"
            "Поддерживаются только ASTC sRGB форматы (4×4, 6×6, 8×8 и т.д.)"
        )

    bw, bh = block
    mip_data_list: List[bytes] = []
    for _ in range(max(num_mip_levels, 1)):
        if off + 4 > len(data):
            break
        image_size = struct.unpack_from("<I", data, off)[0]
        off += 4
        mip_data_list.append(data[off: off + image_size])
        off += (image_size + 3) & ~3   # выравнивание 4 байта

    return {
        "width":         pixel_width,
        "height":        pixel_height,
        "block_w":       bw,
        "block_h":       bh,
        "mip_data_list": mip_data_list,
    }


def make_ktx1(mip_levels: List[bytes], width: int, height: int, bw: int, bh: int) -> bytes:
    """Собрать KTX1 binary из списка сжатых mip-блоков."""
    gl_format = ASTC_GL_FORMAT.get((bw, bh))
    if gl_format is None:
        raise ValueError(f"Неизвестный ASTC блок: {bw}×{bh}")

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


# ─────────────────────────────────────────────────────────────────────────────
# Обработка изображений (полностью совпадает с PVRTexLib)
# ─────────────────────────────────────────────────────────────────────────────

def to_rgba_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img.convert("RGBA"), dtype=np.uint8).copy()


def premultiply_alpha(arr: np.ndarray) -> np.ndarray:
    """
    RGB *= A/255  —  точно как PVRTexLib::PreMultiplyAlpha().
    Предотвращает тёмные ореолы вокруг прозрачных краёв.
    """
    alpha = arr[:, :, 3:4].astype(np.float32) / 255.0
    result = arr.astype(np.float32)
    result[:, :, :3] *= alpha
    return np.clip(result, 0, 255).astype(np.uint8)


def bleed(arr: np.ndarray, iterations: int = 8) -> np.ndarray:
    """
    Заливка прозрачных пикселей цветами соседних непрозрачных —
    точно как PVRTexLib::Bleed().
    Убирает чёрные/тёмные пиксели на краях после mipmapping.
    """
    arr = arr.copy()
    h, w = arr.shape[:2]

    for _ in range(iterations):
        alpha = arr[:, :, 3]
        transparent_mask = (alpha == 0)
        if not np.any(transparent_mask):
            break

        # Расширяем непрозрачные пиксели в 4 соседних направлениях
        filled = False
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            # Сдвигаем массив
            sy = slice(max(-dy, 0), h + min(-dy, 0))
            sx = slice(max(-dx, 0), w + min(-dx, 0))
            ty = slice(max(dy,  0), h + min(dy,  0))
            tx = slice(max(dx,  0), w + min(dx,  0))

            neighbor_alpha = arr[sy, sx, 3]
            can_fill = transparent_mask[ty, tx] & (neighbor_alpha > 0)
            if np.any(can_fill):
                arr[ty, tx][can_fill, :3] = arr[sy, sx][can_fill, :3]
                filled = True

        if not filled:
            break

    return arr


def next_pow2(n: int) -> int:
    return 1 << math.ceil(math.log2(max(n, 1)))


def pad_to_pow2(arr: np.ndarray) -> Tuple[np.ndarray, int, int]:
    """
    Дополнить холст до степени двойки (требование ASTC mipmaps).
    Возвращает (padded_array, orig_width, orig_height).
    """
    h, w = arr.shape[:2]
    nh, nw = next_pow2(h), next_pow2(w)
    if nh == h and nw == w:
        return arr, w, h
    out = np.zeros((nh, nw, 4), dtype=np.uint8)
    out[:h, :w] = arr
    return out, w, h


def generate_mipmaps(arr: np.ndarray) -> List[np.ndarray]:
    """
    Полная mip-цепочка до 1×1 — как PVRTexLib::GenerateMIPMaps(PVRTLRM_Linear).
    Использует LANCZOS (Pillow) — наиболее близкий к Linear resample.
    """
    mips: List[np.ndarray] = [arr]
    h, w = arr.shape[:2]
    img = Image.fromarray(arr, "RGBA")

    while w > 1 or h > 1:
        w = max(1, w // 2)
        h = max(1, h // 2)
        mip_img = img.resize((w, h), Image.LANCZOS)
        mips.append(np.asarray(mip_img, dtype=np.uint8).copy())

    return mips


# ─────────────────────────────────────────────────────────────────────────────
# ASTC кодирование / декодирование — мультибэкендно
# ─────────────────────────────────────────────────────────────────────────────

def _encode_astc_imagecodecs(arr: np.ndarray, bw: int, bh: int, quality: str) -> bytes:
    """ASTC encode через imagecodecs."""
    import imagecodecs  # type: ignore
    level = QUALITY_LEVELS_IC.get(quality, 60)
    # imagecodecs.astc_encode принимает blocksize как кортеж (x, y) или (x, y, z)
    try:
        compressed = imagecodecs.astc_encode(arr, level=level, blocksize=(bw, bh))
    except TypeError:
        # Некоторые версии требуют трёхмерный blocksize
        compressed = imagecodecs.astc_encode(arr, level=level, blocksize=(bw, bh, 1))
    return bytes(compressed)


def _decode_astc_imagecodecs(blocks: bytes, width: int, height: int, bw: int, bh: int) -> np.ndarray:
    """ASTC decode через imagecodecs."""
    import imagecodecs  # type: ignore
    try:
        arr = imagecodecs.astc_decode(blocks, shape=(height, width, 4), blocksize=(bw, bh))
    except TypeError:
        arr = imagecodecs.astc_decode(blocks, shape=(height, width, 4), blocksize=(bw, bh, 1))
    return np.asarray(arr, dtype=np.uint8)


def _encode_astc_pvrtex(arr: np.ndarray, bw: int, bh: int, quality: str) -> bytes:
    """ASTC encode через pvrtex (PVRTexLib Python bindings)."""
    import pvrtex  # type: ignore
    quality_flag = getattr(pvrtex, f"PVRTLCQ_{QUALITY_LEVELS_PVR.get(quality, 'ASTCMedium')}")
    format_name  = f"PVRTLPF_ASTC_{bw}x{bh}"
    astc_format  = getattr(pvrtex, format_name)

    tex = pvrtex.Texture(arr)
    tex.transcode(astc_format, pvrtex.PVRTLVT_UnsignedByteNorm,
                  pvrtex.PVRTLCS_sRGB, quality_flag)
    # pvrtex возвращает KTX данные — нам нужны только raw ASTC блоки
    # (без KTX заголовка)
    ktx_data = tex.save_to_memory(".ktx")
    ktx_parsed = parse_ktx1(ktx_data)
    return ktx_parsed["mip_data_list"][0]


def _decode_astc_pvrtex(blocks: bytes, width: int, height: int, bw: int, bh: int) -> np.ndarray:
    """ASTC decode через pvrtex (PVRTexLib Python bindings)."""
    import pvrtex  # type: ignore
    # Собираем минимальный KTX1 чтобы pvrtex мог его загрузить
    ktx_data = make_ktx1([blocks], width, height, bw, bh)
    tex = pvrtex.Texture(ktx_data, ".ktx")
    tex.decompress(10)  # 10 = num_threads
    return np.asarray(tex.to_numpy(), dtype=np.uint8)


def encode_astc(arr: np.ndarray, bw: int, bh: int, quality: str) -> bytes:
    """
    Кодировать uint8 RGBA numpy array (H, W, 4) → raw ASTC блоки.
    Автоматически выбирает лучший доступный бэкенд.
    """
    if _BACKEND == "pvrtex":
        try:
            return _encode_astc_pvrtex(arr, bw, bh, quality)
        except Exception as e:
            logger.warning(f"pvrtex encode failed ({e}), fallback → imagecodecs")
    if _BACKEND in ("imagecodecs", "pvrtex"):
        return _encode_astc_imagecodecs(arr, bw, bh, quality)
    raise RuntimeError("Нет доступного ASTC кодека.")


def decode_astc(blocks: bytes, width: int, height: int, bw: int, bh: int) -> np.ndarray:
    """
    Декодировать raw ASTC блоки → uint8 RGBA numpy array (H, W, 4).
    Автоматически выбирает лучший доступный бэкенд.
    """
    if _BACKEND == "pvrtex":
        try:
            return _decode_astc_pvrtex(blocks, width, height, bw, bh)
        except Exception as e:
            logger.warning(f"pvrtex decode failed ({e}), fallback → imagecodecs")
    if _BACKEND in ("imagecodecs", "pvrtex"):
        return _decode_astc_imagecodecs(blocks, width, height, bw, bh)
    raise RuntimeError("Нет доступного ASTC кодека.")


# ─────────────────────────────────────────────────────────────────────────────
# Публичное API
# ─────────────────────────────────────────────────────────────────────────────

def image_to_btx(
    image_path: str,
    btx_path: str,
    compress_mode: str = "4x4",
    quality_mode:  str = "medium",
) -> None:
    """
    Конвертировать изображение (PNG / JPG / BMP / WEBP / TIFF / TGA …) → BTX.

    Параметры
    ---------
    image_path    : исходное изображение
    btx_path      : выходной .btx файл
    compress_mode : размер ASTC блока — "4x4" | "6x6" | "8x8"
    quality_mode  : "fast" | "medium" | "thorough" | "exhaustive"
    """
    check_dependencies()

    bw, bh = (int(x) for x in compress_mode.split("x"))

    # 1. Загрузка → RGBA uint8
    arr = to_rgba_array(Image.open(image_path))
    src_h, src_w = arr.shape[:2]
    logger.info(f"Загружено: {image_path}  {src_w}×{src_h}")

    # 2. Pad до степени двойки (PVRTexLib делает это автоматически)
    arr, orig_w, orig_h = pad_to_pow2(arr)
    if (orig_w, orig_h) != (src_w, src_h):
        logger.info(f"Дополнено до: {arr.shape[1]}×{arr.shape[0]}")

    # 3. Premultiply alpha  (PVRTexLib::PreMultiplyAlpha)
    arr = premultiply_alpha(arr)

    # 4. Bleed прозрачных областей  (PVRTexLib::Bleed)
    arr = bleed(arr)

    # 5. Генерация mip-цепочки  (PVRTexLib::GenerateMIPMaps Linear)
    mips = generate_mipmaps(arr)
    logger.info(f"Mip уровней: {len(mips)}  (base {arr.shape[1]}×{arr.shape[0]})")

    # 6. ASTC encode каждого mip  (PVRTexLib::Transcode ASTC sRGB)
    compressed_mips: List[bytes] = []
    for idx, mip in enumerate(mips):
        h, w = mip.shape[:2]
        blocks = encode_astc(mip, bw, bh, quality_mode)
        compressed_mips.append(blocks)
        logger.info(f"  mip {idx}: {w}×{h} → {len(blocks)} байт")

    # 7. Сборка KTX1 контейнера
    ktx_data = make_ktx1(compressed_mips, arr.shape[1], arr.shape[0], bw, bh)

    # 8. BTX = 4-байтовый magic + KTX1
    os.makedirs(os.path.dirname(btx_path) or ".", exist_ok=True)
    with open(btx_path, "wb") as f:
        f.write(BTX_MAGIC + ktx_data)

    size_kb = Path(btx_path).stat().st_size / 1024
    logger.info(f"BTX записан: {btx_path}  ({size_kb:.1f} KB)")


def btx_to_image(btx_path: str, output_path: str) -> str:
    """
    Конвертировать BTX → изображение.
    Формат определяется расширением output_path.
    Возвращает output_path.
    """
    check_dependencies()

    with open(btx_path, "rb") as f:
        raw = f.read()

    if raw[:4] != BTX_MAGIC:
        raise ValueError(f"Не валидный BTX файл (magic: {raw[:4].hex()})")

    ktx = parse_ktx1(raw[4:])
    bw, bh   = ktx["block_w"],  ktx["block_h"]
    width, height = ktx["width"], ktx["height"]
    mip0 = ktx["mip_data_list"][0]

    logger.info(f"BTX: {width}×{height}  ASTC {bw}×{bh}  {len(ktx['mip_data_list'])} mip(s)")

    rgba = decode_astc(mip0, width, height, bw, bh)
    img  = Image.fromarray(rgba, "RGBA")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path)

    logger.info(f"Сохранено: {output_path}")
    return output_path


def btx_info(btx_path: str) -> dict:
    """
    Вернуть метаданные BTX файла без декодирования пикселей.
    Полезно для быстрой проверки файла.
    """
    with open(btx_path, "rb") as f:
        raw = f.read()

    if raw[:4] != BTX_MAGIC:
        raise ValueError(f"Не валидный BTX файл")

    ktx = parse_ktx1(raw[4:])
    return {
        "width":      ktx["width"],
        "height":     ktx["height"],
        "block_w":    ktx["block_w"],
        "block_h":    ktx["block_h"],
        "mip_levels": len(ktx["mip_data_list"]),
        "file_size":  len(raw),
        "backend":    _BACKEND,
    }
