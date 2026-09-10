#!/usr/bin/env python3
"""Finite checkpoint run; successful execution is not theory closure."""
import argparse,json,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True);args=parser.parse_args()
    files=['test_family_continuation.py','family_continuation.py','log_slip_geometry.py',
           'general_inverse/test_pressure_inverse.py','general_inverse/pressure_inverse.py','general_inverse/run_checks.py']
    records=[]
    for path in files:
        argv=[sys.executable,'-B',str(HERE/path)]
        result=subprocess.run(argv,cwd=HERE,capture_output=True,text=True,timeout=65)
        row=dict(argv=argv,cwd=str(HERE),exit_status=result.returncode,stdout=result.stdout,stderr=result.stderr)
        records.append(row);print(json.dumps(dict(path=path,exit_status=result.returncode)),flush=True)
    args.result_file.write_text(json.dumps(dict(cases=records,status='OPEN'),indent=2)+'\n')
    return int(any(r['exit_status'] for r in records))

if __name__=='__main__':raise SystemExit(main())
