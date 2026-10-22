#!/usr/bin/env python3
"""Read-only provenance check; does not validate the mathematical proof."""
from pathlib import Path
import hashlib
import json

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p / 'campaign_fresh_gravity_astra').is_dir())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
result = json.loads((run / 'result.json').read_text())
freeze = json.loads((run / 'FREEZE.json').read_text())
for section in ('input_sha256', 'artifacts_sha256'):
    for path, expected in result[section].items():
        assert sha(root / path) == expected, (section, path)
for path, expected in freeze['files_sha256'].items():
    assert sha(root / path) == expected, ('freeze', path)
expected_files = set(freeze['files_sha256']) | {str((run / 'FREEZE.json').relative_to(root))}
actual_files = {str(p.relative_to(root)) for p in run.iterdir() if p.is_file()}
assert actual_files == expected_files, ('inventory', actual_files ^ expected_files)
assert result['acceptance_state'] == 'unreviewed'
assert result['execution_bounds']['mathematical_processes'] == 0
print(json.dumps({'status': 'pass', 'input_pins': len(result['input_sha256']),
                  'artifact_pins': len(result['artifacts_sha256']),
                  'frozen_files': len(freeze['files_sha256']),
                  'mathematical_validation': False}, sort_keys=True))
