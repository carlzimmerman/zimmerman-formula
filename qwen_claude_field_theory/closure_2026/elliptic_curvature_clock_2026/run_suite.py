#!/usr/bin/env python3
"""Action, falsifiable health/causality checks, Lean, and existing regressions."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LEAN=ROOT.parent/'clock_constitutive_construction_2026/lean_formalization_2026'
PREVIOUS=ROOT.parent/'trace_variance_mond_2026'


def main():
    py=[sys.executable,'-B']
    cases=[
        ('compensator action audit',py+['compensator.py'],ROOT,0),
        ('full closure refusal',py+['compensator.py','--require-closure'],ROOT,2),
        ('new regressions',py+['-m','unittest','-v','test_compensator.py'],ROOT,0),
        ('Lean health and remainder proofs',['lake','env','lean',str(ROOT/'CompensatorFormal.lean')],LEAN,0),
        ('previous trace and CAM full regressions',py+['run_suite.py'],PREVIOUS,0),
    ]
    records=[]
    for label,command,cwd,expected in cases:
        p=subprocess.run(command,cwd=cwd,text=True,capture_output=True,timeout=240)
        r=dict(label=label,argv=command,cwd=str(cwd),exit_status=p.returncode,expected_exit=expected)
        print('CASE='+json.dumps(r),flush=True)
        print(p.stdout,end='');print(p.stderr,end='');records.append(r)
    print('SUITE_RESULTS='+json.dumps(records))
    print('PHYSICS_STATUS=NOT_CLOSED; positive local health is not causal certification.')
    return 0 if all(r['exit_status']==r['expected_exit'] for r in records) else 1


if __name__=='__main__':
    raise SystemExit(main())
