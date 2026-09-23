#!/usr/bin/env python3
"""Compile the local certificate in the existing Lean host; preserve exact argv."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
args=ap.parse_args()
root=Path.cwd()
host=root/'fable_independent_2026/lean_2026'
source=Path(__file__).resolve().with_name('NormalizationConsequences.lean')
argv=['lake','env','lean',str(source)]
version=subprocess.run(['lake','env','lean','--version'],cwd=host,text=True,capture_output=True,check=True).stdout.strip()
run=subprocess.run(argv,cwd=host,text=True,capture_output=True)
print(run.stdout,end='')
print(run.stderr,file=sys.stderr,end='')
result={'argv':argv,'cwd':str(host),'lean_version':version,'returncode':run.returncode,
        'stdout':run.stdout,'stderr':run.stderr,
        'scope':'Integral area bound and profile-to-health-bound are hypotheses/external analytic steps, not formalized here.'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
sys.exit(run.returncode)
