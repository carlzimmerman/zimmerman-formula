"""Reproduce exact charge coordinates and bounded physical transfers.

Use the computation-audit runner with contract.json and a fresh output path.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[4]
out = Path(sys.argv[1]).resolve()
assert out.is_relative_to(here)
out.mkdir(parents=True, exist_ok=True)
for name in ('canonical_density.py', 'lorentz_well.py', 'canonical_evolve.py',
             'lorentz_evolve.py', 'phase_precision.py'):
    print('CHECK', name, flush=True)
    subprocess.run([sys.executable, str(here / name)], check=True, cwd=root)
for name in ('canonical.json', 'lorentz_canonical.json', 'canonical_evolution.json',
             'lorentz_evolution.json', 'phase_precision_results.json'):
    shutil.copyfile(here / name, out / name)
rows = json.loads((out / 'phase_precision_results.json').read_text())
summary = {
    'all_executed_checks_passed': True,
    'exact_checks': ['invertible charge transformation and differential identity',
                     'Bardeen potential equality',
                     'Lorentz-well correction leaves reconstructed potential equality intact'],
    'original_transfer_cases': 6,
    'lorentz_transfer_cases': 5,
    'high_precision_witnesses': rows,
    'physical_status': 'Incomplete. These finite linear evolutions do not certify a theory.',
    'scope': 'See contract.json and ../STATUS.md. Operator norms use the explicitly declared initial state norm.',
}
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print('Exact phase transformation and bounded evolution checks reproduced.', flush=True)
