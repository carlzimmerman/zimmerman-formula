#!/usr/bin/env python3
"""Re-run the eight-case suite, then the all-wavelength action/Lean bridge."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from run_checks import HERE, ROOT, LEAN

p=argparse.ArgumentParser()
p.add_argument('--result-file',type=Path,required=True)
a=p.parse_args()
base=subprocess.run([sys.executable,'-B',str(HERE/'run_checks.py'),'--result-file',str(a.result_file)],cwd=ROOT,timeout=270)
if base.returncode:raise SystemExit(base.returncode)
result=json.loads(a.result_file.read_text())
for name,argv,cwd in [
    ('check_all_scales.py',[sys.executable,'-B',str(HERE/'check_all_scales.py')],ROOT),
    ('AllScales.lean',['lake','env','lean',str(HERE/'AllScales.lean')],LEAN)]:
    try:
        r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=90)
        row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=r.returncode,stdout=r.stdout,stderr=r.stderr)
    except subprocess.TimeoutExpired:
        row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=None,status='timeout')
    result['cases'].append(row)
    print(json.dumps(dict(name=name,exit_status=row['exit_status'])),flush=True)
a.result_file.write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(int(any(r['exit_status']!=0 for r in result['cases'])))
