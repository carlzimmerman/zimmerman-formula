"""Execute with pinned inputs; argument chooses a fresh run directory."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent.relative_to(ROOT)
RUN=BASE/(sys.argv[1] if len(sys.argv)>1 else 'run_001')
c=json.loads((ROOT/BASE/'contract.json').read_text())
argv=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py',
      '--root',str(ROOT),'--contract',str(BASE/'contract.json'),'--output',str(RUN),
      '--timeout','180','--max-output-bytes','1048576','--max-cpu-seconds','150','--max-threads','1']
for p in c['execution_artifacts']:
    argv+=['--input',p]
for name in ['catalogue_matches.csv','gas_comparison.csv','closure_requirements.csv','dependent_quantity_checks.csv','data_inventory.json','checks.json']:
    argv+=['--result',str(RUN/name)]
argv+=['--',sys.executable,str(BASE/'observe.py'),'--out',str(RUN)]
raise SystemExit(subprocess.run(argv,cwd=ROOT).returncode)
