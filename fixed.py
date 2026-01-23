import struct
import zipfile
from pathlib import Path
import sys

def compute_data_offset(zip_path: Path, header_offset: int) -> int:
    with zip_path.open('rb') as f:
        f.seek(header_offset)
        header = f.read(30)
        if len(header) < 30:
            raise IOError(f"Unexpected short local header at offset {header_offset}")
        file_name_len = int.from_bytes(header[26:28], 'little')
        extra_field_len = int.from_bytes(header[28:30], 'little')
        data_offset = header_offset + 30 + file_name_len + extra_field_len
        return data_offset

def generate_bpcmeta(zip_path_str: str, output_path_str: str = None):
    zip_path = Path(zip_path_str)
    if output_path_str:
        out_path = Path(output_path_str)
    else:
        out_path = zip_path.with_suffix('.bpcmeta')

    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")

    entries = []
    with zipfile.ZipFile(zip_path, 'r') as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            lower = info.filename.lower()
            if not lower.endswith(('.mp3', '.wav', '.ogg')):
                continue
            header_offset = getattr(info, 'header_offset', None)
            if header_offset is None:
                raise RuntimeError(f"No header_offset for {info.filename}; Python's zipfile lacks it.")
            data_offset = compute_data_offset(zip_path, header_offset)
            comp_size = int(info.compress_size)

            is_mp3_flag = 1 if lower.endswith('.mp3') else 0

            entries.append({
                'name': info.filename,
                'data_offset': int(data_offset),
                'comp_size': comp_size,
                'is_mp3': is_mp3_flag
            })

    entries.sort(key=lambda e: e['name'].lower())

    # Format:
    # <I> count
    # For each entry:
    #   <I> data_offset
    #   <I> compressed_size
    #   <B> is_mp3 (1 or 0)
    #   <H> name_len
    #   <name_bytes> (UTF-8)
    out = bytearray()
    out += struct.pack('<I', len(entries))
    for e in entries:
        name_bytes = e['name'].encode('utf-8')
        if len(name_bytes) > 0xFFFF:
            raise ValueError(f"Filename too long after utf-8 encoding: {e['name']}")
        out += struct.pack('<I', e['data_offset'])
        out += struct.pack('<I', e['comp_size'])
        out += struct.pack('B', e['is_mp3'])
        out += struct.pack('<H', len(name_bytes))
        out += name_bytes

    out_path.write_bytes(out)
    print(f"bpcmeta: {out_path}  ({len(out)} bytes) -- entries: {len(entries)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fixed.py /path/to/GENERIC.bpc [/path/to/output.bpcmeta]")
        sys.exit(2)
    zip_in = sys.argv[1]
    zip_out = sys.argv[2] if len(sys.argv) > 2 else None
    generate_bpcmeta(zip_in, zip_out)
