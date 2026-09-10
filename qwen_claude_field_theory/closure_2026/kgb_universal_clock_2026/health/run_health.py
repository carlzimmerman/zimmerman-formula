#!/usr/bin/env python3
"""Reproduce the bounded interval audit and record actual command outcomes."""
import argparse
import json
from pathlib import Path
import subprocess
import unittest
import actual_pencils
import test_common_interval

HERE=Path(__file__).resolve().parent
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_common_interval))
    argv=['lake','env','lean',str(HERE/'CommonInterval.lean')]
    process=subprocess.run(argv,cwd=LEAN,capture_output=True,text=True,timeout=60)
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),
        lean=dict(argv=argv,cwd=str(LEAN),exit_status=process.returncode,stdout=process.stdout,stderr=process.stderr),
        actual_pair=actual_pencils.run_control_pair(),
        scope='Exact conditional interval reduction; numerical two-pencil controls are not a common-action or full-theory certificate')
    payload=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() and process.returncode==0 else 1


if __name__=='__main__':raise SystemExit(main())
