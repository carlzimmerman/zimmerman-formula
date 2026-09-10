#!/usr/bin/env python3
"""Finite evidence, not certification of a complete gravity theory."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LEAN=ROOT.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[(name,[sys.executable,'-B',name],ROOT,0) for name in
           ('jet_window.py','precision_check.py','jet_steering.py','steered_profile.py','regular_clock.py')]
    cases += [
        ('pressure inverse scan',[sys.executable,'-B','shared_pressure.py','--scan'],ROOT,0),
        ('new regressions',[sys.executable,'-B','-m','unittest','-v','test_pressure.py'],ROOT,0),
        ('Lean local window',['lake','env','lean',str(ROOT/'PressureWindowFormal.lean')],LEAN,0),
        ('previous 49 regressions',[sys.executable,'-B','run_suite.py'],ROOT.parent/'ticking_kgb_inverse_2026',0),
    ]
    results=[]
    for label,argv,cwd,expected in cases:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=300)
        record=dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode,expected_exit=expected)
        print('CASE='+json.dumps(record),flush=True)
        print(p.stdout,end='');print(p.stderr,end='');results.append(record)
    print('SUITE_RESULTS='+json.dumps(results))
    print('PHYSICS_STATUS=OPEN; local action-derived repair is not global MOND closure')
    return 0 if all(r['exit_status']==r['expected_exit'] for r in results) else 1


if __name__=='__main__':raise SystemExit(main())
