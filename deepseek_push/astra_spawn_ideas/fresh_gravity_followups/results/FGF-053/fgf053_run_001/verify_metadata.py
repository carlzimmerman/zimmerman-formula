#!/usr/bin/env python3
"""Read-only byte/schema verifier. No mathematical theorem validation."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]

def read_json(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_map(mapping):
    for relative, expected in mapping.items():
        path = ROOT / relative
        assert path.is_file(), relative
        assert digest(path) == expected, 'SHA256 mismatch: ' + relative

result = read_json(HERE / 'result.json')
inputs = read_json(HERE / 'input_pins.json')
check_map(inputs)
assert result['input_sha256'] == inputs
base = ROOT / 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups'
task = base / 'tasks/FGF-053.md'
assert digest(task) == result['task_sha256'] == 'e4aade5337048d6abf27e5aa18911eed10f0a9716f13e69a0c38eee4f610bc95'
pins = re.findall(r'`([^`]+)` SHA256 `([a-f0-9]{64})`', task.read_text())
assert len(pins) == 12
for relative, expected in pins:
    assert inputs[relative] == expected
contract = read_json(base / 'RESULT_CONTRACT.json')
assert set(contract['required_fields']).issubset(result)
assert result['outcome'] in {'supports_scoped_claim','counterexample','inconclusive','blocked_on_data','implementation_failure'}
assert result['mathematical_computation_count'] == 0
assert result['acceptance_state'] == 'unreviewed'
check_map(result['artifacts_sha256'])
freeze = read_json(HERE / 'FREEZE.json')
check_map(freeze['artifacts_sha256'])
assert freeze['artifacts_sha256'][str((HERE/'result.json').relative_to(ROOT))] == digest(HERE/'result.json')
print('PASS: task + 12 ancestry pins, contract fields, supporting outputs and final freeze; mathematical computations = 0. Metadata only, not a proof checker.')
