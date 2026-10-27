"""Repeat the linear-front test including its complete kinetic stiffness."""
import argparse,json,copy
from pathlib import Path
import numpy as np
from forced_front import calculate
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args()
branch=json.loads(Path('front_dynamics_2026_10_25/run_branch_checked/results.json').read_text())['runs'][-1];audit=json.loads(Path('front_dynamics_2026_10_25/run_geometry/results.json').read_text());out={'runs':[],'non_claims':['FD03 theorem hypotheses and exclusions remain in force','Computed metric second derivatives are a finite-difference audit, not a certified continuum correction','Source-grid variation of the passive bound remains unresolved; no uniform continuum bound is claimed']}
for correction in audit['kinetic_stiffness_runs']:
 r=copy.deepcopy(branch);rows=np.array(r['rows']);rows[:,5]=correction['effective_curvature'];r['rows']=rows.tolist()
 for dt in [.1,.05]:
  ans=calculate(r,dt);ans['metric_R_difference_step']=correction['R_step_dimensionless'];assert ans['absolute_energy_ledger_error']<1e-14;out['runs'].append(ans);Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(ans,flush=True)
