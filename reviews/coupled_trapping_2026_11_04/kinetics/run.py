"""Run an explicitly named local CT09 script under the v2 bounded runner."""
from pathlib import Path
import json,sys,subprocess
p=Path('reviews/coupled_trapping_2026_11_04/kinetics');stem,script,*args=sys.argv[1:];c=json.loads((p/(stem+'_contract.json')).read_text());out=p/('run_'+stem+'_001');cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p/(stem+'_contract.json'))]
for f in c['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(out),'--result',str(out/'result.json'),'--timeout','240','--max-output-bytes','1000000','--max-cpu-seconds','235','--max-threads','1','--','python3',str(p/script),str(out/'result.json'),*args]
raise SystemExit(subprocess.call(cmd))
