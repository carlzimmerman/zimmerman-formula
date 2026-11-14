#!/usr/bin/env python3
"""Regenerate either bounded audit into a fresh, named directory."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
PYTHON='/private/tmp/forj0332-fit-venv/bin/python'
parser=argparse.ArgumentParser()
parser.add_argument('--stage',type=int,choices=(1,2,3,4,5),required=True)
parser.add_argument('--run-name',required=True)
args=parser.parse_args()
assert '/' not in args.run_name and args.run_name not in ('.','..')
spec={1:('contract.json','calculate.py',['results.json','halo_masses.csv','representative_profiles.npz']),
      2:('source_contract.json','analyze_sources.py',['results.json','source_comparisons.csv']),
      3:('crossing_contract.json','check_crossing_scope.py',['results.json','scope_rows.csv']),
      4:('figure_contract.json','plot_example.py',['mass_budget_example.png','mass_budget_example.svg','figure_context.json']),
      5:('budget_contract_v2.json','budget_bound_v2.py',['results.json','budget_bounds.csv'])}
contract_name,script_name,results=spec[args.stage]
contract=HERE/contract_name
out=HERE/args.run_name
assert not out.exists(), 'A fresh output directory is required'
c=json.loads(contract.read_text())
rel=lambda p:str(p.relative_to(ROOT))
argv=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
      '--contract',str(contract),'--output',rel(out),'--timeout','300' if args.stage==1 else '120' if args.stage==5 else '30',
      '--max-output-bytes','1048576','--max-threads','1']
for path in c['execution_artifacts']:argv+=['--input',path]
for name in results:argv+=['--result',rel(out/name)]
argv+=['--',PYTHON,rel(HERE/script_name),'--output',rel(out)]
code=subprocess.call(argv,cwd=ROOT)
if code==0:
    code=subprocess.call([sys.executable,str(SKILL/'scripts/validate_manifest.py'),str(out/'manifest.json'),'--root',str(ROOT)],cwd=ROOT)
raise SystemExit(code)
