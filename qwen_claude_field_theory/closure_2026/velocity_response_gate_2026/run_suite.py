#!/usr/bin/env python3
"""Bounded response checks and the existing action/Dirac/Lean regression suite."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LEAN=ROOT.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[
        ('action-derived response',[sys.executable,'-B','response_gate.py'],ROOT,0),
        ('closure refusal',[sys.executable,'-B','response_gate.py','--require-closure'],ROOT,2),
        ('six response regressions',[sys.executable,'-B','-m','unittest','-v','test_response.py'],ROOT,0),
        ('five conditional Lean lemmas',['lake','env','lean',str(ROOT/'ResponseFormal.lean')],LEAN,0),
        ('previous elliptic curvature action suite',[sys.executable,'-B','run_suite.py'],ROOT.parent/'elliptic_curvature_clock_2026',0),
    ]
    records=[]
    for label,argv,cwd,expected in cases:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=240)
        record=dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode,expected_exit=expected)
        print('CASE='+json.dumps(record),flush=True)
        print(p.stdout,end='');print(p.stderr,end='');records.append(record)
    print('SUITE_RESULTS='+json.dumps(records))
    print('PHYSICS_STATUS=OPEN; partial principal-action audit only')
    return 0 if all(r['exit_status']==r['expected_exit'] for r in records) else 1


if __name__=='__main__':
    raise SystemExit(main())
