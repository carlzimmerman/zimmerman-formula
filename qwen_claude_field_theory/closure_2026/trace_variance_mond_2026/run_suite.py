#!/usr/bin/env python3
"""Reproduce action calculations, expected refusal, Lean, and prior regressions."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LEAN=ROOT.parent/'clock_constitutive_construction_2026/lean_formalization_2026'
CAM=ROOT.parent/'cuscuton_acceleration_mond_2026'


def main():
    py=[sys.executable,'-B']
    cases=[
        ('trace action audit',py+['trace_variance.py'],ROOT,0),
        ('closure refusal',py+['trace_variance.py','--require-closure'],ROOT,2),
        ('regressions',py+['-m','unittest','-v','test_trace_variance.py'],ROOT,0),
        ('Lean sign theorem',['lake','env','lean',str(ROOT/'TraceVarianceFormal.lean')],LEAN,0),
        ('historical frozen coupling gauntlet',py+[str(ROOT.parent/'theory_discovery/khronometric_mond_gauntlet_2026.py')],ROOT,0),
        ('CAM physical and closure regressions',py+['run_physical_audit_suite.py'],CAM,0),
    ]
    records=[]
    for label,command,cwd,expected in cases:
        p=subprocess.run(command,cwd=cwd,text=True,capture_output=True,timeout=240)
        r=dict(label=label,argv=command,cwd=str(cwd),exit_status=p.returncode,expected_exit=expected)
        print('CASE='+json.dumps(r),flush=True)
        print(p.stdout,end=''); print(p.stderr,end='')
        records.append(r)
    print('SUITE_RESULTS='+json.dumps(records))
    print('PHYSICS_STATUS=NOT_CLOSED; the old gauntlet passing does not validate its running-coupling substitution.')
    return 0 if all(r['exit_status']==r['expected_exit'] for r in records) else 1


if __name__=='__main__':
    raise SystemExit(main())
