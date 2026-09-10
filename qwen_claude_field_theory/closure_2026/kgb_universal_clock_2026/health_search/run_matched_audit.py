#!/usr/bin/env python3
"""Focused actual-seed evidence; deliberately does not run the broad search."""
import argparse
import json
from pathlib import Path
import unittest
import matched_seed_audit as audit
import test_signed_search


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_signed_search))
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),
        precision=80,seeds={u:audit.run(80,u) for u in ('.03','.128','.5')},
        broad_signed_search_attempts=0,
        scope='Three actual five-jet matches with shared local health witnesses; next preservation fails at each seed, not a universal no-go')
    payload=json.dumps(audit.ef.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
