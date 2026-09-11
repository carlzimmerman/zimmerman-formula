#!/usr/bin/env python3
"""Check action-output/Lean bridge and run scoped regression certificates."""
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
    args=parser.parse_args()
    data=json.loads((HERE/'run_003/result.json').read_text())
    assert all(data['checks'].values())
    m,v=s.symbols('m v',positive=True)
    match=re.search(r'def ellH2 \(m v : ℝ\) : ℝ := ([^\n]+)',(HERE/'ConstraintLength.lean').read_text())
    assert match,'missing Lean expression'
    actual=s.sympify(data['gamma_zero_profile_ellH_squared'],locals={'m':m,'v':v})
    formal=s.sympify(match.group(1),locals={'m':m,'v':v})
    assert s.factor(actual-formal)==0,'action output and actual Lean definition differ'
    assert s.factor(actual+formal)!=0,'sign-reversal control failed'
    cases=[
        ('filter_unit_tests',[sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_filter.py'],ROOT),
        ('ConstraintLength.lean',['/opt/homebrew/bin/lake','env','lean',str(HERE/'ConstraintLength.lean')],LEAN),
        ('existing_exact_point_bridge',[sys.executable,str(HERE.parent/'cubic_finite_wavelength/point_certificate.py')],ROOT),
        ('existing_tensor_variation',[sys.executable,str(HERE.parent/'cubic_finite_wavelength/tensor_gate.py')],ROOT),
        ('existing_PointSigns.lean',['/opt/homebrew/bin/lake','env','lean',str(HERE.parent/'cubic_finite_wavelength/PointSigns.lean')],LEAN)]
    results=[]
    for name,argv,cwd in cases:
        result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=180)
        results.append(dict(name=name,argv=argv,exit_status=result.returncode,
                            stdout=result.stdout,stderr=result.stderr))
        print(json.dumps(dict(name=name,exit_status=result.returncode)),flush=True)
    output=dict(action_output_Lean_definition_bridge=True,sign_reversal_rejected=True,cases=results,
                full_theory_status='OPEN')
    args.result_file.write_text(json.dumps(output,indent=2)+'\n')
    return int(any(case['exit_status']!=0 for case in results))


if __name__=='__main__':raise SystemExit(main())
