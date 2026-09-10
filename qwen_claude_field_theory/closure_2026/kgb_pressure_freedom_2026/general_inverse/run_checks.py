#!/usr/bin/env python3
"""Bounded tests plus six actual general-pressure controls."""
import argparse
import json
from pathlib import Path
import unittest
import pressure_inverse as p
import test_pressure_inverse


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_pressure_inverse))
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),computation=p.run(65))
    payload=json.dumps(p.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
