import sys,json,subprocess
from pathlib import Path
b=Path('sol61_push/kinetic_support_2026_10_23');name=sys.argv[1];files=[str(b/'CONTRACT.md'),str(b/(name+'.py'))]+[str(b/'family/result.json')]
c=json.loads((b/'family_contract.json').read_text());c['claim_id']='KS_'+name;c['execution_artifacts']=files;c['mathematics']['assertion_tested']='Virial, Jeans and fixed-occupancy energy-per-mass identities over supported family';p=b/(name+'_contract.json');assert not p.exists();p.write_text(json.dumps(c,indent=2));o=b/name
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p),'--output',str(o),'--result',str(o/'result.json'),'--timeout','60','--max-threads','1']
for f in files:cmd+=['--input',f]
subprocess.run(cmd+['--','python3',str(b/(name+'.py')),str(o/'result.json')],check=True)
