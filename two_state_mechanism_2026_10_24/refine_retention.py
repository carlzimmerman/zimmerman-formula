"""Targeted follow-up: separate timestep and particle-count dwarf sensitivity."""
import json
import sys
from pathlib import Path
from model import PROFILES
from profile_experiment import run

rows=[run(PROFILES[0],256,.000025),run(PROFILES[0],512,.000025)]
prior=json.loads(Path(__file__).with_name('run_profiles').joinpath('results.json').read_text())['runs'][1]
result=dict(runs=rows,
    energy_criterion_pass=all(x['max_energy_relative_error']<.005 for x in rows),
    timestep_bound_difference=abs(rows[0]['final_bound_fraction']-prior['final_bound_fraction']),
    particle_count_bound_difference=abs(rows[1]['final_bound_fraction']-rows[0]['final_bound_fraction']),
    interpretation='Finite-time softened cold-collapse sensitivity; not asymptotic retention')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result,indent=2,allow_nan=False))
