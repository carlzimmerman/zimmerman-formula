#!/usr/bin/env python3
"""Read-only verification. Never rewrites pins, artifacts, or freezes."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
AUDIT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

errors = []
freeze = json.loads((AUDIT / 'independent_freeze.json').read_text())
for name, expected in freeze['artifacts_sha256'].items():
    actual = digest(AUDIT / name)
    if actual != expected:
        errors.append(f'frozen artifact mismatch: {name}')
inputs = json.loads((AUDIT / 'input_sha256.json').read_text())
for rel, expected in inputs.items():
    if digest(ROOT / rel) != expected:
        errors.append(f'input mismatch: {rel}')
ancestry = json.loads((AUDIT / 'ANCESTRY_VERIFICATION.json').read_text())
if len(ancestry['pins']) != 10:
    errors.append('ancestry pin count differs from ten')
for item in ancestry['pins']:
    if digest(ROOT / item['path']) != item['expected']:
        errors.append(f'ancestry mismatch: {item["path"]}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(inputs)} input pins, ten ancestry pins, and three frozen artifacts; read-only verification.')
