#!/usr/bin/env python3
"""Bounded nonlinear gate, constructive repair, stationary completion and regressions."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path,required=True);a=p.parse_args()
    out=a.result_file.parent
    cases=[(name,[sys.executable,'-B',str(HERE/name),'--result-file',str(out/(name[:-3]+'.json'))],ROOT,90)
           for name in ('derive.py','repair.py','stationary.py')]
    cases.extend((name,['lake','env','lean',str(HERE/name)],LEAN,90)
                 for name in ('Characteristic.lean','Repair.lean','Stationarity.lean'))
    cases.append(('prior_ten_case_regression',[sys.executable,'-B',str(HERE.parent/'finite_evolution/run_certificates.py'),
                  '--result-file',str(out/'prior_cases.json')],ROOT,270))
    records=[]
    for name,argv,cwd,limit in cases:
        try:
            r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=limit)
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=r.returncode,stdout=r.stdout,stderr=r.stderr)
        except subprocess.TimeoutExpired:
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=None,status='timeout')
        records.append(row);print(json.dumps(dict(name=name,exit_status=row['exit_status'])),flush=True)
    # Authenticate the actual Lean polynomial definition against the action output.
    data=json.loads((out/'derive.json').read_text())
    source=(HERE/'Characteristic.lean').read_text()
    matched=re.search(r'noncomputable def p \(v : ℝ\) : ℝ :=\s*(\d+)\*v\^3 \+ (\d+)\*v\^2 \+ (\d+)\*v - (\d+)',source)
    if not matched:raise AssertionError('Lean polynomial source format changed; review bridge')
    coefficients=list(matched.groups());coefficients[-1]='-'+coefficients[-1]
    if coefficients!=data['rational_witness_coefficients']:raise AssertionError('Lean polynomial differs from action')
    result=dict(cases=records,actual_Lean_polynomial_matches_action=True,full_theory_status='OPEN')
    a.result_file.write_text(json.dumps(result,indent=2)+'\n')
    return int(any(r['exit_status']!=0 for r in records))


if __name__=='__main__':raise SystemExit(main())
