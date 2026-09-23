"""Reproduce the constructive checkpoint and snapshot its generated evidence.

Usage: python3 verify_constructive.py OUTPUT_DIRECTORY
Use the computation-audit runner for pinned inputs and bounded execution.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[3]
out = Path(sys.argv[1]).resolve()
assert out.is_relative_to(here)
out.mkdir(parents=True, exist_ok=True)
for name in ('run_adm', 'run_general', 'run_response_extended'):
    (here / name).mkdir(exist_ok=True)
for name in ('background_check.py', 'adm_unitary.py', 'minkowski_control.py',
             'general_kinetic.py', 'kinetic_independent.py', 'reduce_adm.py',
             'response_extended.py', 'evolve_local.py'):
    print('CHECK', name, flush=True)
    subprocess.run([sys.executable, str(here / name)], check=True, cwd=root)
host = root / 'fable_independent_2026/lean_2026'
subprocess.run(['lake', 'env', 'lean', '--version'], check=True, cwd=host)
subprocess.run(['lake', 'env', 'lean', str(here / 'PositiveKinetic.lean')],
               check=True, cwd=host)
artifacts = {
    'equations.json': 'run_adm/equations.json',
    'general_reduced.json': 'run_general/reduced.json',
    'constant_reduced.json': 'run_adm/reduced.json',
    'constant_spectrum.json': 'run_adm/spectrum.json',
    'response_reduced.json': 'run_response_extended/reduced.json',
    'response_spectrum.json': 'run_response_extended/spectrum.json',
    'local_evolution.json': 'local_evolution.json',
}
for target, source in artifacts.items():
    shutil.copyfile(here / source, out / target)
constant = json.loads((out / 'constant_spectrum.json').read_text())
response = json.loads((out / 'response_spectrum.json').read_text())
evolution = json.loads((out / 'local_evolution.json').read_text())
summary = {
    'all_executed_checks_passed': True,
    'mathematical_result': 'Positive scalar kinetic matrix on the stated generic branch; five Lean theorems compiled.',
    'physical_status': 'Incomplete. Both selected parameter families retain rapid amplification for tested initial data.',
    'constant_points': len(constant), 'response_points': len(response),
    'sampled_kinetic_positive': all(z['kinetic_positive'] for z in constant + response),
    'largest_constant_frozen_rate_over_H': max(z['max_growth_over_H'] for z in constant),
    'largest_response_frozen_rate_over_H': max(z['max_growth_over_H'] for z in response),
    'bounded_time_evolution': evolution,
    'scope': 'See constructive_contract.json and CONSTRUCTION.md; no claim of theory closure.',
}
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print('Constructive checkpoint reproduced and evidence snapshotted.', flush=True)
