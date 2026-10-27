import json,sys,subprocess
from pathlib import Path
contract=Path(sys.argv[1]);output=Path(sys.argv[2]);script=sys.argv[3];timeout=sys.argv[4];c=json.loads(contract.read_text());cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root','.','--contract',str(contract)]
for f in c['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(output),'--result',str(output/'results.json'),'--timeout',timeout,'--max-threads','1','--','python3',script,'--output',str(output/'results.json')];raise SystemExit(subprocess.call(cmd))
