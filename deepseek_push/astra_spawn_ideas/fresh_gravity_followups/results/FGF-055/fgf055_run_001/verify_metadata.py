#!/usr/bin/env python3
"""READ ONLY. Checks byte pins/schema only; never checks mathematical truth."""
import hashlib
import json
from pathlib import Path
import re

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[5]
TASK = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-055.md'
CONTRACT = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_map(mapping):
    for rel, expected in mapping.items():
        assert digest(ROOT / rel) == expected, 'SHA256 mismatch: ' + rel


result = json.loads((RUN / 'result.json').read_text())
pins = json.loads((RUN / 'input_pins.json').read_text())
manifest = json.loads((RUN / 'manifest.json').read_text())
freeze = json.loads((RUN / 'FREEZE.json').read_text())
contract = json.loads((ROOT / CONTRACT).read_text())
assert not set(contract['required_fields']).difference(result)
assert result['task_id'] == 'FGF055'
assert result['run_id'] == 'fgf055_run_001'
assert result['acceptance_state'] == 'unreviewed'
assert result['orchestrator_review_required'] is True
assert result['mathematical_computation_count'] == 0
assert result['input_sha256'] == pins['input_sha256'] == manifest['input_sha256']
check_map(result['input_sha256'])
assert result['task_sha256'] == digest(ROOT / TASK)
ancestry = dict(re.findall(r'`([^`]+)` SHA256 `([a-f0-9]{64})`',
                          (ROOT / TASK).read_text()))
assert len(ancestry) == 10
assert all(result['input_sha256'].get(p) == h for p, h in ancestry.items())
check_map(result['artifacts_sha256'])
check_map(manifest['artifacts_sha256'])
assert all(result['artifacts_sha256'].get(p) == h
           for p, h in manifest['artifacts_sha256'].items())
check_map(freeze['sha256'])
expected = dict(result['artifacts_sha256'])
expected[str((RUN / 'result.json').relative_to(ROOT))] = digest(RUN / 'result.json')
assert freeze['sha256'] == expected
actual = {str(p.relative_to(ROOT)) for p in RUN.iterdir() if p.is_file()}
assert actual == set(expected) | {str((RUN / 'FREEZE.json').relative_to(ROOT))}
assert not any(p.is_dir() for p in RUN.iterdir()), 'Unexpected subdirectory'
assert all('stage_42' not in path for path in result['input_sha256'])
print('PASS: ten ancestry pins and all source/output/manifest/freeze hashes.')
print('PASS: required contract fields and exact frozen file inventory.')
print('READ-ONLY METADATA ONLY: zero mathematical computations; author unreviewed.')
print('DERIVATION_SHA256=' + digest(RUN / 'DERIVATION.md'))
print('RESULT_SHA256=' + digest(RUN / 'result.json'))
