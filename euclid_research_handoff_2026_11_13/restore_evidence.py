"""Restore losslessly packed tables; verify hashes and never overwrite conflicts.

This performs no network access and starts no scientific experiment. Omitted
third-party caches are listed separately in snapshot_manifest.json.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((HERE/'snapshot_manifest.json').read_text())
    for item in manifest['compressed_tables']:
        payload = ROOT/item['packed_path']
        raw = gzip.decompress(payload.read_bytes())
        if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('Packed data integrity failure: '+str(payload))
        dest = ROOT/item['path']
        if dest.exists():
            if hashlib.sha256(dest.read_bytes()).hexdigest() != item['sha256']:
                raise FileExistsError('Refusing to overwrite conflicting local evidence: '+str(dest))
        elif not args.verify_only:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
        print(('verified ' if args.verify_only else 'available ')+item['path'])
    print('No research or downloads started. See omitted_caches for external files.')

if __name__ == '__main__':
    main()
