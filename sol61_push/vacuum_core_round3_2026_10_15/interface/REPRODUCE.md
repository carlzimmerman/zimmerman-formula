# Reproduce the authoritative interface check

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Preserve the
existing `run_v1` and `run_v2` evidence and use a fresh output destination.

```python
import json, subprocess
from pathlib import Path
p = Path('sol61_push/vacuum_core_round3_2026_10_15/interface')
c = json.loads((p / 'computation_contract_v2.json').read_text())
out = p / 'run_reproduction'
cmd = [
    'python3',
    '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py',
    '--root', str(Path.cwd()),
    '--contract', str(p / 'computation_contract_v2.json'),
]
for source in c['execution_artifacts']:
    cmd += ['--input', source]
cmd += [
    '--output', str(out), '--result', str(out / 'results.json'),
    '--timeout', '45', '--max-output-bytes', '65536',
    '--max-cpu-seconds', '35', '--max-threads', '1', '--',
    'python3', str(p / 'check_interface_v2.py'), str(out / 'results.json'),
]
subprocess.run(cmd, check=True)
```

Validate the recorded authoritative run:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/vacuum_core_round3_2026_10_15/interface/run_v2/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The expected count is 32 exact checks. The corrected full-current Rayleigh
lower bound is above 43/1000, with all declared kinetic and gravitational
truncation conditions in the proof and amendment.
