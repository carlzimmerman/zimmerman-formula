import sys,json,subprocess
from pathlib import Path
b=Path('sol61_push/kinetic_support_2026_10_23');name=sys.argv[1];args=sys.argv[2:];c=json.loads((b/'family_contract.json').read_text());c['claim_id']='KS_'+name;c['execution_artifacts']=[str(b/x) for x in ['CONTRACT.md','equilibrium.py','particle_base.py','dynamics_v2.py']];c['mathematics']['assertion_tested']='Finite 3D waterbag supported-state deformation and canonical dilation, live fields, no gas or expansion';c['mathematics']['inputs']=args;c['randomness']={'used':True,'generator':'scipy.stats.qmc.Sobol scrambled','seed':61423};p=b/(name+'_contract.json');assert not p.exists();p.write_text(json.dumps(c,indent=2));o=b/name
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p),'--output',str(o),'--result',str(o/'result.json'),'--timeout','300','--max-threads','1']
for f in c['execution_artifacts']:cmd+=['--input',f]
subprocess.run(cmd+['--','python3',str(b/'dynamics_v2.py'),'--output',str(o/'result.json')]+args,check=True)
