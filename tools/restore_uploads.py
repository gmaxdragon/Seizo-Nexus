"""Restore the exact owner-supplied files during initial repository packaging.

After packaging, original STLs and the screenshot are committed directly. This
helper then only verifies them; it does not replace an existing mismatched file.
"""
from pathlib import Path
import hashlib
import json
import lzma
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
IMAGE_URL = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3Exj9bDHoXP3JuENaws4UF74BKT/d28a142a-d723-4492-9f31-be51509049fd.png'


def verify(data: bytes, item: dict) -> None:
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        raise ValueError('Owner-supplied file identity mismatch')


def main() -> None:
    manifest = json.loads((ROOT / 'tools/source-manifest.json').read_text())
    for item in manifest['files']:
        path = ROOT / 'models/stl' / item['name']
        if path.exists():
            verify(path.read_bytes(), item)
            continue
        raw = lzma.decompress((ROOT / 'tools/import_payload' / item['payload']).read_bytes())
        verify(raw, item)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    item = manifest['screenshot']
    path = ROOT / item['path']
    if path.exists():
        verify(path.read_bytes(), item)
    else:
        with urllib.request.urlopen(IMAGE_URL, timeout=45) as response:
            raw = response.read(1_000_001)
        verify(raw, item)
        if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Expected the original PNG screenshot')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    print('Verified four original STL byte identities and original screenshot.')


if __name__ == '__main__':
    main()
