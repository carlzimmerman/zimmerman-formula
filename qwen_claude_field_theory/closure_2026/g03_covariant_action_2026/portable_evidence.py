#!/usr/bin/env python3
"""Remove machine prefixes from serialized G03 evidence, preserving old hashes.

This is a mechanical presentation rewrite, not a change to numerical evidence.
The provenance record retains each pre-rewrite and post-rewrite hash. Scientific
source hashes in historical manifests continue to describe their original run.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def portable(text):
    text=text.replace(str(ROOT)+'/', '')
    text=text.replace(str(ROOT), '.')
    text=re.sub(r'/Applications/[^\s"\']*/(?:bin/python3|usr/bin/python3)', 'python3', text)
    text=re.sub(r'/Applications/[^\s"\']*/lib/python([0-9.]+)/', r'<python-stdlib-\1>/', text)
    return text


def main():
    records=[]
    for path in sorted(HERE.rglob('*')):
        if not path.is_file() or path.suffix not in ('.json','.out','.md'):
            continue
        if path.name in ('portability_record.json','file_inventory.json'):
            continue
        old=path.read_bytes()
        new=portable(old.decode()).encode()
        if new != old:
            path.write_bytes(new)
            records.append(dict(path=str(path.relative_to(ROOT)),before_sha256=sha(old),
                                after_sha256=sha(new),change='machine prefixes only'))
    record=HERE/'portability_record.json'
    previous=json.loads(record.read_text()) if record.exists() else []
    record.write_text(json.dumps(previous+records,indent=2)+'\n')
    print(f'[ok] {len(records)} evidence files made portable; original hashes retained')
    return 0


if __name__=='__main__':
    sys.exit(main())
