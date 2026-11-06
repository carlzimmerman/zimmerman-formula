"""AC13 STRESS rows rerun with the corrected full-measure factor at z = 0.1:
pol_on = (1 - z)^2 = 0.81 instead of the legacy (1 - 2z)^2 = 0.64.
AC13's run() is imported unchanged (read-only); outputs go only to argv[1].
Post-hoc corrected-coefficient evidence, NOT a frozen regrade. Run from the repo root.
Kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, sys
from multiprocessing import Pool
from pathlib import Path
OUT = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('ac13', 'action_search_2026_11_05/AC13_slow_root_closure/ac13.py')
ac13 = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac13)
ac13.OUT = OUT
ac13.POL['stress'] = (1 - 0.1) ** 2


def runj(j):
    ac13.OUT = OUT; ac13.POL['stress'] = (1 - 0.1) ** 2
    return ac13.run(j)


if __name__ == '__main__':
    jobs = [j for j in ac13.jobs() if j[4] == 'stress']
    jobs.sort(key=lambda j: float(j[3]) * (10.0 if j[0] == '2' else 1.0))   # fastest first
    with Pool(3) as p:
        for _ in p.imap_unordered(runj, jobs):
            pass
    print('all done', len(jobs), flush=True)
