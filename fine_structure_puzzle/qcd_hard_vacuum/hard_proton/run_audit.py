#!/usr/bin/env python3
"""Reproduction launcher: installed bounded v2 runner, no RLIMIT_AS."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True,help='Fresh project-relative run directory')
args=parser.parse_args()
root=Path(__file__).resolve().parents[3]
base='fine_structure_puzzle/qcd_hard_vacuum/hard_proton/'
contract=root/(base+'COMPUTATION_CONTRACT.json')
runner=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
assert runner.is_file(),'Installed runner unavailable; no execution attempted'
argv=[sys.executable,str(runner),'--root',str(root),'--contract',str(contract)]
for path in json.loads(contract.read_text())['execution_artifacts']:
    argv+=['--input',path]
argv+=['--output',args.output,'--result',args.output+'/result.json','--timeout','30',
       '--max-output-bytes','1048576','--max-cpu-seconds','15','--max-threads','1','--',
       sys.executable,base+'calculate_hard.py','--inputs',base+'INPUTS.json','--output',args.output+'/result.json']
raise SystemExit(subprocess.call(argv,cwd=str(root)))
