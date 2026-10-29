"""Restore exact missing input files without overwriting user changes."""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--root',required=True,type=Path)
args=parser.parse_args()
base=Path(__file__).resolve().parent
root=args.root.resolve()
index=json.loads((base/'INDEX.json').read_text())
pending=[]
for entry in index['entries']:
    source=(base/entry['snapshot_path']).resolve()
    target=(root/entry['original_path']).resolve()
    assert base in source.parents and root in target.parents
    payload=source.read_bytes()
    assert hashlib.sha256(payload).hexdigest()==entry['sha256']
    if target.exists():
        assert target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest()==entry['sha256'],f'Different existing input: {target}'
    else:
        pending.append((target,payload))
for target,payload in pending:
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as handle:
        handle.write(payload)
print(f'Created {len(pending)} missing inputs; {len(index["entries"])} snapshots verified.')
