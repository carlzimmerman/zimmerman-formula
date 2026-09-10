#!/usr/bin/env python3
"""Execute exact background derivation, bounded scan, Lean, independent audits and regressions."""
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
    cases=[('background_variation',[sys.executable,'-B',str(HERE/'derive.py'),'--result-file',str(out/'derivation.json')],ROOT),
           ('homogeneous_scan',[sys.executable,'-B',str(HERE/'numerical.py'),'--result-file',str(out/'numerical.json')],ROOT),
           ('HomogeneousGap.lean',['lake','env','lean',str(HERE/'HomogeneousGap.lean')],LEAN),
           ('independent_current_stress',[sys.executable,'-B',str(HERE.parent/'cubic_current_audit/derive.py')],ROOT),
           ('independent_scalar_principal',[sys.executable,'-B',str(HERE.parent/'cubic_principal_audit/derive.py')],ROOT),
           ('prior_ellipticity',[sys.executable,'-B',str(HERE.parent/'dirac_operator/ellipticity.py'),'--result-file',str(out/'prior_ellipticity.json')],ROOT),
           ('prior_lapse',[sys.executable,'-B',str(HERE.parent/'dirac_operator/lapse_source.py'),'--result-file',str(out/'prior_lapse.json')],ROOT)]
    rows=[]
    for name,argv,cwd in cases:
        r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=90)
        rows.append(dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=r.returncode,
            stdout=r.stdout,stderr=r.stderr))
        print(json.dumps(dict(name=name,exit_status=r.returncode)),flush=True)
    args.result_file.write_text(json.dumps(dict(cases=rows,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(row['exit_status']!=0 for row in rows))

if __name__=='__main__':raise SystemExit(main())
