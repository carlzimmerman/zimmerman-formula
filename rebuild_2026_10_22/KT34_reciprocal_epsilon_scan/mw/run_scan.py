#!/usr/bin/env python3
"""Bounded manifest runner; explicit argv, never executes recorded manifest commands."""
import argparse,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
def main():
    p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--run',required=True);p.add_argument('--script',default='scan.py');a,rest=p.parse_known_args()
    contract=HERE/a.contract;c=json.loads(contract.read_text());run=HERE/a.run
    argv=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),'--contract',str(contract),'--output',str(run.relative_to(ROOT)),'--result',str((run/'results.json').relative_to(ROOT)),'--timeout','1800','--max-output-bytes','1048576','--max-cpu-seconds','1750','--max-threads','1']
    for f in c['execution_artifacts']:argv += ['--input',f]
    argv += ['--',sys.executable,str(HERE/a.script),'--output',str(run/'results.json')]+rest
    raise SystemExit(subprocess.call(argv))
if __name__=='__main__':main()
