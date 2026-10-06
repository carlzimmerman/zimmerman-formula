#!/usr/bin/env python3
"""Use a fresh tag; restore and hash-verify cached source inputs before rerun."""
import argparse,json,pathlib,subprocess,re
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);p.add_argument('--control',choices=['none','mixing','canonical','mond'],default='none');a=p.parse_args()
if not re.fullmatch('[A-Za-z0-9_-]+',a.tag):raise SystemExit('tag must be a simple directory name')
own=pathlib.Path(__file__).resolve().parent;root=own.parents[3];rel=own.relative_to(root);contract=json.loads((own/'contract.json').read_text());out=rel/'runs'/a.tag;result=out/'results.json'
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py'
argv=['/opt/homebrew/Caskroom/miniconda/base/bin/python3.13',runner,'--root',str(root),'--contract',str(rel/'contract.json'),'--output',str(out),'--result',str(result),'--timeout','60','--max-cpu-seconds','45','--max-output-bytes','200000','--max-threads','1']
for x in contract['execution_artifacts']:argv+=['--input',x]
argv+=['--','/usr/bin/python3',str(rel/'checks.py'),'--output',str(result),'--control',a.control]
raise SystemExit(subprocess.call(argv,cwd=root))
