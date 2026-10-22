#!/usr/bin/env python3
"""Administrative hashes/schema checks only; no mathematical computation."""
import hashlib, json, pathlib, re
root = pathlib.Path(__file__).resolve().parents[6]
run = pathlib.Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
task = root / 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-048.md'
assert sha(task) == '028ae73e50048d0412fde4d5ddd88e1b94e8bd127d75b80fc952382fdeb4b377'
pins = re.findall(r'`([^`]+)` SHA256 `([0-9a-f]+)`', task.read_text())
assert len(pins) == 8
for path, expected in pins:
    assert sha(root/path) == expected, path
result = json.loads((run/'result.json').read_text())
contract = json.loads((root/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json').read_text())
assert set(contract['required_fields']) <= set(result)
for section in ['input_sha256', 'artifacts_sha256']:
    for path, expected in result[section].items():
        assert sha(root/path) == expected, path
assert json.loads((run/'input_sha256.json').read_text()) == result['input_sha256']
freeze = json.loads((run/'FREEZE.json').read_text())
for path, expected in freeze['artifacts_sha256'].items():
    assert sha(root/path) == expected, path
assert result['execution_bounds']['mathematical_processes'] == 0
assert result['commands'] == []
print('PASS: task hash; all 8 pinned ancestry hashes; all current inputs; required result fields; artifact hashes; author freeze; proof-only metadata.')
print('DERIVATION_SHA256', sha(run/'DERIVATION.md'))
print('RESULT_SHA256', sha(run/'result.json'))
print('No mathematical executable computations or numerical tests performed.')
