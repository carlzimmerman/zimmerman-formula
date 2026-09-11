#!/usr/bin/env python3
"""Bounded regression bundle, with an actual action-output/Lean definition bridge."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();out=args.result_file.parent
    cases=[
        ('density_action',[sys.executable,str(HERE/'density_gap.py'),'--result-file',str(out/'density.json')],ROOT),
        ('budget_tests',[sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_budget.py'],ROOT),
        ('DensityCompactness.lean',['/opt/homebrew/bin/lake','env','lean',str(HERE/'DensityCompactness.lean')],LEAN),
        ('existing_all_gradient_ellipticity',[sys.executable,str(HERE.parent/'dirac_operator/ellipticity.py')],ROOT),
        ('existing_Ellipticity.lean',['/opt/homebrew/bin/lake','env','lean',str(HERE.parent/'dirac_operator/Ellipticity.lean')],LEAN)]
    rows=[]
    for name,argv,cwd in cases:
        result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=180)
        rows.append(dict(name=name,argv=argv,exit_status=result.returncode,stdout=result.stdout,stderr=result.stderr))
        print(json.dumps(dict(name=name,exit_status=result.returncode)),flush=True)
    if rows[0]['exit_status']!=0:
        args.result_file.write_text(json.dumps(dict(cases=rows,bridge=False),indent=2)+'\n')
        return 1
    data=json.loads((out/'density.json').read_text())
    match=re.search(r'def densitySlope \(M m : ℝ\) : ℝ := ([^\n]+)',(HERE/'DensityCompactness.lean').read_text())
    assert match,'missing actual Lean definition'
    M,m=s.symbols('M m')
    action=s.sympify(data['stationary_density_coefficient'],locals={'M2':M,'m':m})
    formal=s.sympify(match.group(1),locals={'M':M,'m':m})
    assert s.factor(action-formal)==0,'action/Lean coefficient mismatch'
    assert s.factor(action+formal)!=0,'sign mutation not rejected'
    H,v,rho=s.symbols('H v rho')
    match_gap=re.search(r'def lapseGap \(H M m v rho : ℝ\) : ℝ := ([^\n]+)',(HERE/'DensityCompactness.lean').read_text())
    assert match_gap,'missing actual Lean gap'
    variables={'H':H,'M':M,'M2':M,'m':m,'v':v,'rho':rho}
    actual_gap=s.sympify(data['stationary_full_gap'],locals=variables)
    formal_gap=s.sympify(match_gap.group(1).replace('^','**'),locals=variables)
    assert s.factor(actual_gap-formal_gap)==0,'full gap action/Lean mismatch'
    output=dict(cases=rows,action_Lean_definition_bridge=True,full_gap_Lean_bridge=True,
                sign_mutation_rejected=True,full_theory_status='OPEN')
    args.result_file.write_text(json.dumps(output,indent=2)+'\n')
    return int(any(row['exit_status']!=0 for row in rows))


if __name__=='__main__':raise SystemExit(main())
