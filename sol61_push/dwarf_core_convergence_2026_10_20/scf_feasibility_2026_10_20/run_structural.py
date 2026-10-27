"""Recorded focused structural tests with an output result for the audit runner."""
import argparse,json,os,unittest
from pathlib import Path
import test_scf_backend

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
suite=unittest.defaultTestLoader.loadTestsFromModule(test_scf_backend)
result=unittest.TextTestRunner(verbosity=2).run(suite)
Path(args.output).write_text(json.dumps(dict(tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful(),actual_nice=os.getpriority(os.PRIO_PROCESS,0)),indent=2)+'\n')
raise SystemExit(0 if result.wasSuccessful() else 1)
