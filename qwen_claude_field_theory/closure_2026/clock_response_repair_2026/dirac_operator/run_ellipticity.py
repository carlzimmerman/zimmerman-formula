#!/usr/bin/env python3
"""Run the exact eigenvalue reduction and conditional Lean proof together."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path,required=True);a=p.parse_args()
    cases=[([sys.executable,'-B',str(HERE/'ellipticity.py'),'--result-file',str(a.result_file.parent/'eigenvalues.json')],ROOT),
           (['lake','env','lean',str(HERE/'Ellipticity.lean')],LEAN)]
    results=[]
    for argv,cwd in cases:
        r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=90)
        results.append(dict(argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=r.returncode,stdout=r.stdout,stderr=r.stderr))
    a.result_file.write_text(json.dumps(dict(cases=results,full_theory_status='OPEN'),indent=2)+'\n')
    print(json.dumps([dict(argv=r['argv'],exit_status=r['exit_status']) for r in results]))
    return int(any(r['exit_status']!=0 for r in results))


if __name__=='__main__':raise SystemExit(main())
