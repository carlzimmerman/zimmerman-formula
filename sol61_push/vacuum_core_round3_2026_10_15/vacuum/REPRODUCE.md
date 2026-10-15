# Reproduce the vacuum-route bounded check

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. The existing
`run_v1` is immutable evidence; choose a fresh destination when repeating.

```python
import json, subprocess
from pathlib import Path
p = Path('sol61_push/vacuum_core_round3_2026_10_15/vacuum')
c = json.loads((p / 'computation_contract.json').read_text())
out = p / 'run_reproduction'
cmd = [
    'python3',
    '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py',
    '--root', str(Path.cwd()),
    '--contract', str(p / 'computation_contract.json'),
]
for source in c['execution_artifacts']:
    cmd += ['--input', source]
cmd += [
    '--output', str(out), '--result', str(out / 'results.json'),
    '--timeout', '45', '--max-output-bytes', '65536',
    '--max-cpu-seconds', '35', '--max-threads', '1', '--',
    'python3', str(p / 'check_vacuum.py'), str(out / 'results.json'),
]
subprocess.run(cmd, check=True)
```

Validate the recorded run with:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/vacuum_core_round3_2026_10_15/vacuum/run_v1/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

A pass confirms these finite exact controls and provenance, not the unproved
global interface or whole physical theory.
