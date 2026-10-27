import json,subprocess,sys
from pathlib import Path
p=Path('sol61_push/baryon_pressure_2026_10_23');name=sys.argv[1];script='hydro_check.py' if name=='hydro_check' else 'hydro_run.py';bounds={'n':256,'amp':.05,'zend':10,'ratio':1,'cfl':.6}
if name=='hydro_fine':bounds['n']=512
if name=='hydro_time':bounds['cfl']=.3
if name=='hydro_late':bounds.update(n=512,zend=8)
if name=='hydro_smooth':bounds['ratio']=0
if name=='hydro_weak':bounds['amp']=.03
if name=='hydro_null':bounds.update(n=128,amp=0)
c=json.loads((p/'check_contract.json').read_text());c['claim_id']='BP_'+name.upper();c['mathematics'].update(assertion_tested='Spherical finite-volume Euler gas with Compton heating and reciprocal fields',conventions='HYDRO_CONTRACT.md',bounds=bounds);c['execution_artifacts']=[str(p/f) for f in ['HYDRO_CONTRACT.md','radial_base.py','hydro.py',script]];(p/(name+'_contract.json')).write_text(json.dumps(c,indent=2)+'\n')
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p/(name+'_contract.json'))]
for f in c['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(p/name),'--result',str(p/name/'result.json'),'--timeout','300','--max-threads','1','--','python3',str(p/script),'--output',str(p/name/'result.json')]
if name!='hydro_check':
 for k,v in bounds.items():cmd+=['--'+k,str(v)]
subprocess.run(cmd,check=False)
