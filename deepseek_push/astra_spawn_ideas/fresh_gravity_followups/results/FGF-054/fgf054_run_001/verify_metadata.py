#!/usr/bin/env python3
"""Read-only byte-pin/schema replay. This is not mathematical verification."""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[6]
RUN = pathlib.Path(__file__).resolve().parent
TASK = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-054.md'
CONTRACT = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_map(mapping):
    for path, expected in mapping.items():
        assert digest(ROOT / path) == expected, 'SHA256 mismatch: ' + path


result = json.loads((RUN / 'result.json').read_text())
pins = json.loads((RUN / 'input_pins.json').read_text())
manifest = json.loads((RUN / 'manifest.json').read_text())
freeze = json.loads((RUN / 'FREEZE.json').read_text())
contract = json.loads((ROOT / CONTRACT).read_text())
assert not set(contract['required_fields']).difference(result), 'Missing required field'
assert result['task_id'] == 'FGF054'
assert result['run_id'] == 'fgf054_run_001'
assert result['mathematical_computation_count'] == 0
assert result['acceptance_state'] == 'unreviewed'
assert result['orchestrator_review_required'] is True
assert result['input_sha256'] == pins['input_sha256'] == manifest['input_sha256']
check_map(result['input_sha256'])
assert result['task_sha256'] == digest(ROOT / TASK)
ancestry = dict(re.findall(r'- `([^`]+)` SHA256 `([a-f0-9]{64})`',
                          (ROOT / TASK).read_text()))
assert len(ancestry) == 10
assert all(result['input_sha256'].get(p) == h for p, h in ancestry.items())
check_map(result['artifacts_sha256'])
check_map(manifest['artifacts_sha256'])
assert all(result['artifacts_sha256'].get(p) == h
           for p, h in manifest['artifacts_sha256'].items())
check_map(freeze['sha256'])
expected_frozen = dict(result['artifacts_sha256'])
expected_frozen[str((RUN / 'result.json').relative_to(ROOT))] = digest(RUN / 'result.json')
assert freeze['sha256'] == expected_frozen
actual_files = {str(p.relative_to(ROOT)) for p in RUN.iterdir() if p.is_file()}
assert actual_files == set(expected_frozen) | {str((RUN / 'FREEZE.json').relative_to(ROOT))}
print('PASS: 10 ancestry pins, 13 inputs, all result/manifest/freeze pins, contract fields.')
print('PASS: read-only metadata replay; zero mathematical executable computations.')
print('Unreviewed author candidate. No mathematical theorem is certified by this verifier.')
