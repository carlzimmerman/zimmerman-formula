import argparse,json,os,unittest
from pathlib import Path
from probe_helpers import unit_check
from scf_backend import load_agama
import test_scf_weighted,test_probe_helpers

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(test_scf_weighted),
                         unittest.defaultTestLoader.loadTestsFromModule(test_probe_helpers)])
result=unittest.TextTestRunner(verbosity=2).run(suite)
Path(args.output).write_text(json.dumps(dict(actual_nice=os.getpriority(os.PRIO_PROCESS,0),
    units=unit_check(load_agama()),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors)),indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
