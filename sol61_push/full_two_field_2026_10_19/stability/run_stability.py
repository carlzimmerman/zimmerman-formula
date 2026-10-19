"""Orchestrate one declared long radial evolution; runner owns provenance."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--dx',type=float,required=True)
p.add_argument('--eps-x',type=float,default=.01);p.add_argument('--eps-phi',type=float,default=.01)
p.add_argument('--T',type=float,default=1000);p.add_argument('--R',type=float,default=600)
a=p.parse_args();root=Path.cwd();base=Path('sol61_push/full_two_field_2026_10_19/stability')
import numpy,scipy
contract=json.loads((base/'contract_smoke.json').read_text())
contract['mathematics']['assertion_tested']='Full nonlinear spherical two-field EKG radial baseline/perturbation evolution with radial and independent momentum constraints, energy/charge drift and daughter positive-stiffness control.'
contract['mathematics']['bounds']={'dx':a.dx,'R':a.R,'T':a.T,'dt_factor':.2,'eps_X':a.eps_x,'eps_Phi':a.eps_phi}
contract['execution_artifacts']=[str(base/'evolve_ekg_v2.py'),'sol61_push/full_two_field_2026_10_19/reference/run_003/pureX_h0.050.npz']
cp=base/(a.run+'_contract.json');cp.write_text(json.dumps(contract,indent=2)+'\n')
cmd=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(root),'--contract',str(cp)]
for item in contract['execution_artifacts']:cmd+=['--input',item]
cmd+=['--output',str(base/a.run),'--result',str(base/a.run/'evolution.json'),'--result',str(base/a.run/'evolution.npz'),'--timeout','180','--max-output-bytes','1048576','--max-threads','1','--',sys.executable,str(base/'evolve_ekg_v2.py'),'--profile',contract['execution_artifacts'][1],'--dx',str(a.dx),'--R',str(a.R),'--T',str(a.T),'--eps-x',str(a.eps_x),'--eps-phi',str(a.eps_phi),'--result',str(base/a.run/'evolution.json')]
raise SystemExit(subprocess.call(cmd))
