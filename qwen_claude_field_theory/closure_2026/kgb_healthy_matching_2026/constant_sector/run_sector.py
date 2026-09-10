#!/usr/bin/env python3
"""Record bounded constant-F regimes and independent checks."""
import argparse
import json
from pathlib import Path
import time
import unittest
import sector
import test_sector


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    started=time.process_time()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_sector))
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),computation=sector.run())
    result['total_cpu_seconds']=time.process_time()-started
    if result['total_cpu_seconds']>180:raise TimeoutError('total CPU cap exceeded')
    payload=json.dumps(sector.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
