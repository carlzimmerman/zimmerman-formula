import json,subprocess,sys
from pathlib import Path
base=Path('sol61_push/compatible_gas_2026_10_23');name=sys.argv[1];args=sys.argv[2:];check=name.startswith('check') or name=='cooling_scale'; script='cooling_scale.py' if name=='cooling_scale' else ('check_final.py' if name=='check_final' else 'check_v3.py')

if (base/name).exists() or (base/(name+'_contract.json')).exists():raise SystemExit('Use a fresh run name; existing evidence is immutable')
files=[str(base/x) for x in ['radial_base.py','gas_v4.py','CONTRACT.md']]+([str(base/script)] if check else [])

if '--resume' in args:files.append(args[args.index('--resume')+1])
timeout=600 if name=='ultra' else 300
c={'claim_id':'CG_'+name,'mathematics':{'assertion_tested':'Semidiscrete gas energy consistency and bounded spherical collapse with density-dependent cooling','coefficient_domain':'float64','conventions':str(base/'CONTRACT.md'),'inputs':args,'bounds':{'timeout_seconds':timeout},'non_claims':['No mass selection or observational preservation inferred from endpoint alone']},'execution_artifacts':files,'software':[{'name':'Python','version':'3.9.6'},{'name':'NumPy','version':'1.26.2'},{'name':'SciPy','version':'1.11.4'}],'randomness':{'used':False,'generator':'','seed':None}}
contract=base/(name+'_contract.json');contract.write_text(json.dumps(c,indent=2));out=base/name;result=out/'result.json'
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(contract),'--output',str(out),'--result',str(result),'--timeout',str(timeout),'--max-threads','1']
for f in files:cmd+=['--input',f]
cmd+=['--','python3',str(base/(script if check else 'gas_v4.py'))]+([str(result)] if check else ['--output',str(result)]+args)
subprocess.run(cmd,check=True)
