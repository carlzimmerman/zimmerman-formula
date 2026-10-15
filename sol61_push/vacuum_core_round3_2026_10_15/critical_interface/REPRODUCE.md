# Reproduce the joined critical-body exact check

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Keep the existing
`run_v1` immutable and use a new output directory for a repeated run.

```python
import json, subprocess
from pathlib import Path
p = Path('sol61_push/vacuum_core_round3_2026_10_15/critical_interface')
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
    'python3', str(p / 'check_critical_interface.py'), str(out / 'results.json'),
]
subprocess.run(cmd, check=True)
```

Validate the recorded run with:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/vacuum_core_round3_2026_10_15/critical_interface/run_v1/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Expected: 37 exact checks, with strict rational coercivity and contraction
certificates. A pass audits this reduction and assigned parameter example;
the analytic proof establishes the uniform radial and existence implications.
