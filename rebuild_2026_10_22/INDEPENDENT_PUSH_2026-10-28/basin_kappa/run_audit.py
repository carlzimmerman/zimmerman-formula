#!/usr/bin/env python3
"""Reproduce one fresh bounded run. This wrapper needs Python 3.10+."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--runner', required=True, help='Installed mathbox run_experiment.py')
ap.add_argument('--name', required=True, help='New, nonexisting output directory basename')
ap.add_argument('--python', default='/usr/bin/python3')
ap.add_argument('--mutate', action='store_true')
args = ap.parse_args()
here = Path(__file__).resolve().parent
repo = here.parents[2]
contract = json.loads((here/'contract.json').read_text())
out = here/args.name
if out.exists() or out.parent != here:
    raise SystemExit('Output name must be a new directory in this lane')
cmd = [sys.executable,args.runner,'--root',str(repo),'--contract',str(here/'contract.json')]
for p in contract['execution_artifacts']:
    cmd += ['--input',p]
cmd += ['--output',str(out.relative_to(repo)),'--result',str((out/'results.json').relative_to(repo)),
        '--timeout','90','--max-output-bytes','100000','--max-cpu-seconds','60',
        '--max-threads','1','--',args.python,str(here/'basin_kappa.py'),'--output',str(out)]
if args.mutate:
    cmd += ['--mutate']
raise SystemExit(subprocess.call(cmd,cwd=repo))
