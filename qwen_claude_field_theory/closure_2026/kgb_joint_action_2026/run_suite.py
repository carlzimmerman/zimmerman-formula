#!/usr/bin/env python3
"""Run local construction, next-gate falsification, independent audits and Lean.

Exit zero means these computations executed and their explicit assertions held.
It NEVER means the complete gravity requirements passed.
"""
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
CLOSURE=HERE.parent
REPO=CLOSURE.parent.parent
LEAN=CLOSURE/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[(name,[sys.executable,'-B',name],HERE) for name in ('joint_static.py','third_mass.py')]
    cases += [
        ('8 joint-action regressions',[sys.executable,'-B','-m','unittest','-v','test_joint.py'],HERE),
        ('independent audit',[sys.executable,'-B','test_independent_audit.py'],HERE/'audit'),
        ('lensing derivation',[sys.executable,'-B','lensing.py'],HERE/'lensing'),
        ('lensing tests',[sys.executable,'-B','test_lensing.py'],HERE/'lensing'),
        ('independent high precision',[sys.executable,'-B','precision_check.py'],HERE/'precision'),
        ('precision regressions',[sys.executable,'-B','test_precision.py'],HERE/'precision'),
        ('Lean preservation',['lake','env','lean',str(HERE/'audit/SharedPreservationFormal.lean')],LEAN),
        ('previous 58 regressions',[sys.executable,'-B','run_suite.py'],CLOSURE/'kgb_shared_pressure_2026'),
        ('Fable L118 scope check',[sys.executable,'-B','fable_independent_2026/L118_gate_spec_and_transition_pathology.py'],REPO),
    ]
    results=[]
    for label,argv,cwd in cases:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=300)
        record=dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode)
        print('CASE='+json.dumps(record),flush=True)
        print(p.stdout,end='');print(p.stderr,end='');results.append(record)
    print('SUITE_RESULTS='+json.dumps(results))
    print('PHYSICS_STATUS=OPEN; local shared action constructed, full universal theory not certified')
    return 0 if all(r['exit_status']==0 for r in results) else 1


if __name__=='__main__':raise SystemExit(main())
