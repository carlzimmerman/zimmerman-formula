#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPAIR = HERE.parents[1]
ROOT = next(path for path in HERE.parents if (path/'.git').exists())
SKILL = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit')
inputs = [HERE/name for name in ('exterior.py', 'test_exterior.py', 'contract.json', 'run_bounded.py')]
inputs += [REPAIR/'cosmological_bridge_2026'/name for name in
           ('radiation_002/result.json', 'radiation_probe.py', 'background_evolve.py',
            'transfer_evolve.py', 'transfer_jets.py', 'derive.py')]
inputs += [REPAIR/path for path in ('nonlinear_evolution_2026/constitutive.py',
           'l192_principal_audit_2026/principal_audit.py',
           'finite_gradient_metric_2026/cubic/cubic_debraiding.py')]
relative = lambda path: str(path.relative_to(ROOT))
output = HERE/'run_001'
command = [sys.executable, str(SKILL/'scripts/run_experiment.py'), '--root', str(ROOT),
           '--contract', relative(HERE/'contract.json'), '--output', relative(output),
           '--timeout', '90', '--max-output-bytes', '1048576', '--max-threads', '1']
for path in inputs:
    command += ['--input', relative(path)]
command += ['--result', relative(output/'result.json'), '--', sys.executable, '-B',
            relative(HERE/'exterior.py'), '--result-file', relative(output/'result.json')]
result = subprocess.run(command, cwd=ROOT)
if result.returncode:
    raise SystemExit(result.returncode)
raise SystemExit(subprocess.run([sys.executable, str(SKILL/'scripts/validate_manifest.py'),
    str(output/'manifest.json'), '--root', str(ROOT)], cwd=ROOT).returncode)
