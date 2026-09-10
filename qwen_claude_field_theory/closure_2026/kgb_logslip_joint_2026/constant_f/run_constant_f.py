#!/usr/bin/env python3
"""Run the single-point constant-F construction and its independent tests."""
import argparse
import json
from pathlib import Path
import unittest
import constant_f as c
import test_constant_f


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_constant_f))
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),computation=c.run(65))
    payload=json.dumps(c.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
