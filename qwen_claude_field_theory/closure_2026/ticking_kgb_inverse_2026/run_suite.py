#!/usr/bin/env python3
"""Record execution separately from physics certification; never turn OPEN into PASS."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LEAN=ROOT.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[
        ('varied action, inverse identity, halo and FLRW',[sys.executable,'-B','kgb_inverse.py'],ROOT,0),
        ('full closure refusal',[sys.executable,'-B','kgb_inverse.py','--require-closure'],ROOT,2),
        ('exponential profile and two-mass compatibility',[sys.executable,'-B','mond_profile.py'],ROOT,0),
        ('nine independent checks',[sys.executable,'-B','-m','unittest','-v','test_kgb.py'],ROOT,0),
        ('Lean conditional inequalities and fixed-power obstruction',
         ['lake','env','lean',str(ROOT/'KGBFormal.lean')],LEAN,0),
        ('previous closure regressions',[sys.executable,'-B','run_suite.py'],ROOT.parent/'linear_curvature_clock_2026',0),
    ]
    results=[]
    for label,argv,cwd,expected in cases:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=300)
        record=dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode,expected_exit=expected)
        print('CASE='+json.dumps(record),flush=True)
        print(p.stdout,end='');print(p.stderr,end='');results.append(record)
    print('SUITE_RESULTS='+json.dumps(results))
    print('PHYSICS_STATUS=OPEN; exact halo is not universal MOND; exponential inverse fails tested health and compatibility')
    return 0 if all(r['exit_status']==r['expected_exit'] for r in results) else 1


if __name__=='__main__':raise SystemExit(main())
