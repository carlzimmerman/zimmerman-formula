import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--dx',type=float,required=True)
p.add_argument('--basis',type=int,required=True);p.add_argument('--v2',action='store_true');p.add_argument('--profile');p.add_argument('--R',type=float,default=300);a=p.parse_args()
base=Path('sol61_push/full_two_field_2026_10_19/stability')
c=json.loads((base/'hessian_contract.json').read_text())
c['mathematics']['bounds']={'R':a.R,'dx':a.dx,'basis_per_real_component':a.basis,'dimension_per_parity':4*a.basis}
if a.v2:c['execution_artifacts'][0]=str(base/'hessian_ekg_v2.py')
c['execution_artifacts'][1]=a.profile or 'sol61_push/full_two_field_2026_10_19/equilibria/run_001/mixed_center.npz'
cp=base/(a.run+'_contract.json');cp.write_text(json.dumps(c,indent=2)+'\n')
cmd=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(cp)]
for x in c['execution_artifacts']:cmd+=['--input',x]
if a.v2:cmd+=['--result',str(base/a.run/'hessian.npz')]
cmd+=['--output',str(base/a.run),'--result',str(base/a.run/'hessian.json'),'--timeout','120','--max-output-bytes','1048576','--max-threads','1','--',sys.executable,c['execution_artifacts'][0],'--profile',c['execution_artifacts'][1],'--R',str(a.R),'--dx',str(a.dx),'--basis',str(a.basis),'--result',str(base/a.run/'hessian.json')]
raise SystemExit(subprocess.call(cmd))
