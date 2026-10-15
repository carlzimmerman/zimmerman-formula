# Reproduce the binding energy calculation

The authoritative run is `run_v2`. It passed nine exact symbolic reductions,
three independent 70-digit energy integrals, and nine finite uniform-start
budgets. The maximum closed-form/direct-integral discrepancy was below
2e-70. The positive-series truncation has the separate analytic bound in
PROOF.md. Software: Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0.

`run_v1` failed because SymPy did not simplify the positive square root
sqrt(1+4s(s+1)) to 2s+1. The unchanged first code and failed manifest are
retained. Version 2 checks its squared identity and positivity explicitly;
no proof input changed between these runs.

Run this from the repository root with a new output directory:

```python
import json, subprocess
from pathlib import Path
b = Path('sol61_push/ambitious_round4_2026_10_15/inventory_energy')
c = json.loads((b / 'computation_contract_v2.json').read_text())
out = b / 'run_reproduction'
skill = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts')
cmd = ['python3', str(skill / 'run_experiment.py'), '--root', str(Path.cwd()),
       '--contract', str(b / 'computation_contract_v2.json')]
for p in c['execution_artifacts']:
    cmd += ['--input', p]
cmd += ['--output', str(out), '--result', str(out / 'results.json'),
        '--timeout', '45', '--max-output-bytes', '65536',
        '--max-cpu-seconds', '30', '--max-threads', '1', '--',
        'python3', str(b / 'check_energy_v2.py'), str(out / 'results.json')]
subprocess.run(cmd, check=True)
subprocess.run(['python3', str(skill / 'validate_manifest.py'),
                str(out / 'manifest.json'), '--root', str(Path.cwd())], check=True)
```

The physical-unit example assigns Mb=10^10.5 solar masses and the stated
constants. For a uniform start at twice the eventual edge, N=3,6,10 gives
excess energies about 3.15e51, 3.70e51 and 4.12e51 joules, or 3.46e-8,
2.04e-8 and 1.36e-8 of the respective cold rest energies. These are conditional
state-energy differences, not predicted luminosities, rates or cosmic supplies.

Validation checks artifact integrity. The analytic derivative/envelope
argument and positive-series bound supply the continuum identities and scope.
