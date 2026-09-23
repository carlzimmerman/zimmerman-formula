"""Independent statistics harness; unchanged pinned transport, fixed v8 sample plan.

This is a finite simulation, not a proof of a small-delay asymptotic.
"""
import json
import math
from pathlib import Path
import runpy
import sys

import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[3]
simulate = runpy.run_path(str(ROOT / 'real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py'))['simulate']
reference = json.loads((ROOT / 'real_research/reviews/jwst_small_delay_leaf_2026_09_22/certified/result.json').read_text())
F1 = {(row['tau'], row['epsilon']): row['density_refined'] for row in reference['rows']}


def interval(k, n):
    return [float(beta.ppf(.025, k, n-k+1)) if k else 0.,
            float(beta.ppf(.975, k+1, n-k)) if k < n else 1.]


def evaluate(out, tau, total, seed, mode):
    d, t, n = out['delay'], out['time'], out['n']
    observed = t if mode == 'negative' else d
    integrity = all(len(out[key]) == total and np.all(np.isfinite(out[key]))
                    for key in ('v', 'time', 'exposure', 'angular', 'n', 'delay'))
    integrity = bool(integrity and np.all(n >= 0) and np.all(n == np.floor(n))
                     and np.all(d >= -1e-12) and np.all(t >= 1-1e-12))
    atom = int(np.count_nonzero(n == 0))
    q = math.exp(-tau)
    atom_z = (atom/total-q)/math.sqrt(q*(1-q)/total)
    mean = float(d.mean())
    mean_se = float(d.std(ddof=1)/math.sqrt(total))
    mean_z = (mean-tau/2)/mean_se
    checks = [integrity, abs(atom_z) <= 5, abs(mean_z) <= 5]
    rows = []
    for epsilon in (.01, .003, .001):
        k1 = int(np.count_nonzero((n == 1) & (observed > 0) & (observed <= epsilon)))
        k2 = int(np.count_nonzero((n == 2) & (d > 0) & (d <= epsilon)))
        k3 = int(np.count_nonzero((n >= 3) & (d > 0) & (d <= epsilon)))
        km = k2+k3
        f = F1[tau, epsilon]
        se = math.sqrt(f*(1-f)/total)
        ok = abs(k1/total-f) <= 5*se+1e-8
        checks.append(ok)
        rows.append(dict(epsilon=epsilon, count1=k1, count2=k2, count3plus=k3,
                         countmulti=km, full_positive=k1+km, reference1=f,
                         z1=(k1/total-f)/se, calibration1=ok,
                         probability1=k1/total, probability_multi=km/total,
                         ci1=interval(k1,total), ci_multi=interval(km,total),
                         multi_over_one=km/k1 if k1 else None))
    return dict(mode=mode,tau=tau,N=total,seed=seed,steps=out['steps'],
                integrity=integrity,atom=atom,atom_z=atom_z,meanD=mean,
                meanD_se=mean_se,mean_z=mean_z,rows=rows,
                tail_certificate=bool(all(checks)))


def main():
    cases = []
    for mode,total,seeds in [('main',1000000,(1800101,1800102)),
                             ('positive',2000000,(1800201,1800202))]:
        for tau,seed in zip((1.,4.),seeds):
            out = simulate(total,tau0=tau,q=0,h=0,source='central',seed=seed)
            cases.append(evaluate(out,tau,total,seed,mode))
            if mode == 'main':
                cases.append(evaluate(out,tau,total,seed,'negative'))
            print(json.dumps(dict(mode=mode,tau=tau,complete=total)),flush=True)
            del out
    checks = {f"{c['mode']}_tau{c['tau']}": c['tail_certificate'] == (c['mode'] != 'negative') for c in cases}
    result = dict(cases=cases,checks=checks,passed=all(checks.values()),
                  scope='Finite Monte Carlo over unchanged shared solver; no all-order asymptotic, physical confirmation, or novelty claim.')
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(checks=checks,passed=result['passed'])))


if __name__ == '__main__':
    main()
