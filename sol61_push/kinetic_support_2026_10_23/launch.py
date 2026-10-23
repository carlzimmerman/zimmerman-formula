import json,sys,subprocess
from pathlib import Path
b=Path('sol61_push/kinetic_support_2026_10_23');name=sys.argv[1];files=[str(b/x) for x in (['CONTRACT.md','growth.py'] if name.startswith('growth') else ['CONTRACT.md','equilibrium.py','spectrum_v2.py','run_v2.py'])];c={'claim_id':'KS_'+name,'mathematics':{'assertion_tested':'Finite spherical kinetic equilibria and nonradial density-energy Hessian','coefficient_domain':'float64','conventions':str(b/'CONTRACT.md'),'inputs':[name],'bounds':{'seconds':300},'non_claims':['Not formation, universal mass selection, full kinetic nonlinear stability or observational preservation']},'execution_artifacts':files,'software':[{'name':'Python','version':'3.9.6'},{'name':'NumPy','version':'1.26.2'},{'name':'SciPy','version':'1.11.4'}],'randomness':{'used':False,'generator':'','seed':None}}

if name.startswith('growth'):
 c['mathematics']['assertion_tested']='Conditional primordial waterbag free-stream displacement and ballistic Fourier kernel, not gravitational growth';c['mathematics']['non_claims']=['No full coupled linear growth prediction']
p=b/(name+'_contract.json');assert not p.exists();p.write_text(json.dumps(c,indent=2));o=b/name
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p),'--output',str(o),'--result',str(o/'result.json'),'--timeout','300','--max-threads','1']
for f in files:cmd+=['--input',f]
subprocess.run(cmd+(['--','python3',str(b/'growth.py'),str(o/'result.json')] if name.startswith('growth') else ['--','python3',str(b/'run_v2.py'),name,str(o/'result.json')]),check=True)
