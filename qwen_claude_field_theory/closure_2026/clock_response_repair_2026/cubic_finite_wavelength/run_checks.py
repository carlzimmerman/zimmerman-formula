#!/usr/bin/env python3
"""Run same-action finite-wave, formal algebra, radiation and regression gates."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'

def main():
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path,required=True);args=p.parse_args()
    out=args.result_file.parent
    cases=[('finite_wavelength_action',[sys.executable,'-B',str(HERE/'derive.py'),'--result-file',str(out/'derivation.json')],ROOT),
        ('finite_wavelength_evolution',[sys.executable,'-B',str(HERE/'numerical.py'),'--result-file',str(out/'numerical.json')],ROOT),
        ('ConstraintSchur.lean',['lake','env','lean',str(HERE/'ConstraintSchur.lean')],LEAN),
        ('PointSigns.lean',['lake','env','lean',str(HERE/'PointSigns.lean')],LEAN),
        ('selected_epoch_exact_bridge',[sys.executable,'-B',str(HERE/'point_certificate.py')],ROOT),
        ('tensor_variation',[sys.executable,'-B',str(HERE/'tensor_gate.py')],ROOT),
        ('fixed_action_radiation',[sys.executable,'-B',str(HERE.parent/'cubic_radiation_background/derive.py')],ROOT),
        ('prior_background_regression',[sys.executable,'-B',str(HERE.parent/'cubic_background_completion/derive.py')],ROOT),
        ('prior_principal_regression',[sys.executable,'-B',str(HERE.parent/'cubic_principal_audit/derive.py')],ROOT)]
    rows=[]
    for name,argv,cwd in cases:
        r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=180)
        rows.append(dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=r.returncode,
            stdout=r.stdout,stderr=r.stderr))
        print(json.dumps(dict(name=name,exit_status=r.returncode)),flush=True)
    args.result_file.write_text(json.dumps(dict(cases=rows,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(row['exit_status']!=0 for row in rows))

if __name__=='__main__':raise SystemExit(main())
