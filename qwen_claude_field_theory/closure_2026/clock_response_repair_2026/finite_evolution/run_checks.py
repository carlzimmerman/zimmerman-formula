#!/usr/bin/env python3
"""Run the bounded finite-scale study and new entropy-clock construction."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path,required=True);a=p.parse_args()
    cases=[(name,[sys.executable,'-B',str(HERE/name)],ROOT) for name in
           ('evolve.py','inverse_clock.py','inverse_entropy_clock.py','entropy_health.py','entropy_quadratic.py')]
    cases.extend([('EntropyProfile.lean',['lake','env','lean',str(HERE/'EntropyProfile.lean')],LEAN),
                  ('prior_67_check_regression',[sys.executable,'-B',str(HERE.parent/'derive.py')],ROOT),
                  ('prior_Lean_regression',['lake','env','lean',str(HERE.parent/'ResponseRepair.lean')],LEAN)])
    records=[]
    for name,argv,cwd in cases:
        try:
            r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=90)
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=r.returncode,stdout=r.stdout,stderr=r.stderr)
        except subprocess.TimeoutExpired:
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=None,status='timeout')
        records.append(row)
        print(json.dumps(dict(name=name,exit_status=row['exit_status'])),flush=True)
    a.result_file.write_text(json.dumps(dict(cases=records,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(r['exit_status']!=0 for r in records))


if __name__=='__main__':raise SystemExit(main())
