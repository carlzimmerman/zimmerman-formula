#!/usr/bin/env python3
"""Bounded regression evidence; execution success never certifies a theory."""
import argparse,json,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True);args=parser.parse_args()
    cases=['test_fast.py','fast.py','joint.py','verify_joint.py',
           'reference/run_reference.py','constant_f/run_constant_f.py',
           '../kgb_pressure_freedom_2026/general_inverse/test_pressure_inverse.py']
    records=[]
    for path in cases:
        argv=[sys.executable,'-B',str(HERE/path)]
        out=subprocess.run(argv,cwd=HERE,capture_output=True,text=True,timeout=60)
        records.append(dict(argv=argv,cwd=str(HERE),exit_status=out.returncode,stdout=out.stdout,stderr=out.stderr))
        print(json.dumps(dict(path=path,exit_status=out.returncode)),flush=True)
    args.result_file.write_text(json.dumps(dict(cases=records,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(row['exit_status'] for row in records))

if __name__=='__main__':raise SystemExit(main())
