#!/usr/bin/env python3
"""Bounded execution record. Exit zero means checks executed, not gravity closure."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LEAN_CWD=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args()
    cases=[('coupled_action',[sys.executable,'-B',str(HERE/'derive.py')],ROOT),
           ('Lean',['lake','env','lean',str(HERE/'ResponseRepair.lean')],LEAN_CWD),
           ('review_regression',[sys.executable,'-B',str(ROOT/'fable_independent_2026/reviews/2026-09-10_twenty_recommendations/check_review_algebra.py')],ROOT)]
    records=[]
    for name,argv,cwd in cases:
        try:
            result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=90)
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=result.returncode,
                     stdout=result.stdout,stderr=result.stderr)
        except subprocess.TimeoutExpired:
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=None,status='timeout_90_seconds')
        records.append(row)
        print(json.dumps({k:v for k,v in row.items() if k not in ('stdout','stderr','argv')}),flush=True)
    args.result_file.write_text(json.dumps(dict(cases=records,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(row['exit_status']!=0 for row in records))


if __name__=='__main__':
    raise SystemExit(main())
