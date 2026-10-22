#!/usr/bin/env python3
"""Read-only byte/contract verification; not a mathematical proof checker."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[6]
RUN = Path(__file__).resolve().parent
TASK = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-052.md'
TASK_HASH = 'd368f8c60bf9d3bf112c50c3eafc77b3e083c76d0b7fc7c64bf8b178545b2fa1'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert (ROOT / TASK).is_file(), 'repository root resolution'
    assert digest(ROOT / TASK) == TASK_HASH, 'task bytes changed'
    pins = json.loads((RUN / 'input_pins.json').read_text())
    result = json.loads((RUN / 'result.json').read_text())
    freeze = json.loads((RUN / 'FREEZE.json').read_text())
    pairs = re.findall(r'`([^`]+)` SHA256 `([0-9a-f]{64})`', (ROOT / TASK).read_text())
    assert len(pairs) == 10, 'expected ten ancestry pins'
    for path, expected in pairs:
        assert pins['input_sha256'][path] == expected, path
    assert pins['verified_before_source_use'] is True
    assert result['task_sha256'] == TASK_HASH
    assert result['task_id'] == 'FGF052'
    assert result['run_id'] == 'fgf052_run_001'
    assert result['input_sha256'] == pins['input_sha256']
    for path, expected in result['input_sha256'].items():
        assert digest(ROOT / path) == expected, 'input mismatch: ' + path
    for path, expected in result['artifacts_sha256'].items():
        assert (ROOT / path).parent == RUN, 'artifact outside assigned run'
        assert digest(ROOT / path) == expected, 'artifact mismatch: ' + path
    for path, expected in freeze['sha256'].items():
        assert (ROOT / path).parent == RUN, 'freeze outside assigned run'
        assert digest(ROOT / path) == expected, 'freeze mismatch: ' + path
    result_path = str((RUN / 'result.json').relative_to(ROOT))
    assert result_path in freeze['sha256'], 'result is not frozen'
    assert set(result['artifacts_sha256']).issubset(freeze['sha256'])
    contract = json.loads((ROOT / 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json').read_text())
    assert set(contract['required_fields']).issubset(result), 'missing contract fields'
    assert result['mathematical_computation_count'] == 0
    print('PASS: task, ten ancestry pins, all input/artifact/freeze hashes, and required contract fields. Read-only metadata verification; mathematics not machine-verified.')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL:', str(exc), file=sys.stderr)
        sys.exit(1)
