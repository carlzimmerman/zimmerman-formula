#!/usr/bin/env python3
"""Run bounded zero-braiding computation, tests and conditional Lean proof."""
import argparse
import json
from pathlib import Path
import subprocess
import unittest
import zero_gamma as z
import test_zero_gamma

HERE=Path(__file__).resolve().parent
LEAN=z.CLOSURE/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_zero_gamma))
    command=['lake','env','lean',str(HERE/'ZeroBraiding.lean')]
    lean=subprocess.run(command,cwd=LEAN,capture_output=True,text=True,timeout=60)
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),
        Lean=dict(argv=command,cwd=str(LEAN),exit_status=lean.returncode,stdout=lean.stdout,stderr=lean.stderr),
        computation=z.run(80))
    payload=json.dumps(z.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() and lean.returncode==0 else 1


if __name__=='__main__':raise SystemExit(main())
