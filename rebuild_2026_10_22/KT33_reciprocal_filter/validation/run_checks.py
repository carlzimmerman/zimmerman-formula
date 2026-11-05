"""Record independent operator limits and convergence in structured form."""
import argparse
import json
from pathlib import Path
import unittest
import numpy as np
from periodic_filter import PeriodicFilter
from test_periodic_filter import PeriodicChecks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    tests = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(PeriodicChecks))
    rows = []
    for n in [16,24,32,48]:
        m = PeriodicFilter(n, sigma=0.7, external=(3,0,0))
        x,y,z = m.coordinates
        rho = 2 + np.cos(x) + 0.4*np.cos(2*x) + 0.1*np.cos(y+z)
        row = {'n':n}
        for label,outer in [('source_only',False),('reciprocal',True)]:
            phi = m.potential(rho,outer=outer)
            row[label+'_force'] = [float(np.mean(rho*g)) for g in m.gradient(phi)]
        rows.append(row)
    success = tests.wasSuccessful() and all(
        np.linalg.norm(r['reciprocal_force']) < 1e-12
        and np.linalg.norm(r['source_only_force']) > 1e-4 for r in rows)
    result = {'tests_run': tests.testsRun, 'test_failures': len(tests.failures),
              'test_errors': len(tests.errors), 'force_convergence': rows,
              'all_pass': bool(success),
              'scope':'Finite periodic operator benchmark, separate from isolated observational solvers'}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
