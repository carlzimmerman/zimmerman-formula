#!/usr/bin/env python3
"""New action, physical-beam test, Lean, and directly relevant regressions."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LEAN=ROOT.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[
        ('linear curvature-clock action',[sys.executable,'-B','linear_clock.py'],ROOT,0),
        ('full closure refusal',[sys.executable,'-B','linear_clock.py','--require-closure'],ROOT,2),
        ('seven new regressions',[sys.executable,'-B','-m','unittest','-v','test_linear_clock.py'],ROOT,0),
        ('Lean cone and radiation-tail proofs',['lake','env','lean',str(ROOT/'LinearClockFormal.lean')],LEAN,0),
        ('original curvature action and closure tests',[sys.executable,'-B','run_suite.py'],ROOT.parent/'elliptic_curvature_clock_2026',0),
    ]
    results=[]
    for label,argv,cwd,expected in cases:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=240)
        record=dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode,expected_exit=expected)
        print('CASE='+json.dumps(record),flush=True)
        print(p.stdout,end='');print(p.stderr,end='');results.append(record)
    print('SUITE_RESULTS='+json.dumps(results))
    print('PHYSICS_STATUS=OPEN; vacuum repair does not certify matter causality')
    return 0 if all(r['exit_status']==r['expected_exit'] for r in results) else 1


if __name__=='__main__':
    raise SystemExit(main())
