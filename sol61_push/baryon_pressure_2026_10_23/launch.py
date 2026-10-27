import json,subprocess,sys
from pathlib import Path
p=Path('sol61_push/baryon_pressure_2026_10_23');name=sys.argv[1];c=json.loads((p/(name+'_contract.json')).read_text());cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p/(name+'_contract.json'))]
for f in c['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(p/name),'--result',str(p/name/'result.json'),'--timeout','300','--max-threads','1','--','python3',str(p/'run.py'),'--output',str(p/name/'result.json')]
b=c['mathematics']['bounds']
for key in ['n','amp','gamma','xe','baryon_ratio','cfl','zend']:cmd+=['--'+key.replace('_','-'),str(b[key])]
if not b['pressure']:cmd+=['--no-pressure']
subprocess.run(cmd,check=False)
