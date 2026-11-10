#!/usr/bin/env python3
"""CLS1 reported (not label-setting) check of the construction scan: a 10x finer mu grid across each two-error HSE
window, and the same scan without the positivity requirement (x > 0), per cluster and footing.

Usage: python3 -I cls1_fine.py cls1.json OUT.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cls1_lib as L  # noqa: E402


def scan(prof, rows, a0, mus, nx=2800):
    re = [p['r'] for p in rows]
    lo = np.array([p['M']-2*p['E'] for p in rows]); hi = np.array([p['M']+2*p['E'] for p in rows])
    x0 = np.geomspace(1e-14, 1.0, nx)
    best = {'pos': None, 'any': None}
    for m in mus:
        M, xmin, D = L.integrate(prof, a0, m/L.KPC_PER_MPC, x0, re)
        dev = np.max(np.abs(M-0.5*(lo+hi))/(0.5*(hi-lo)), axis=1)
        dev = np.where(np.isfinite(dev), dev, np.inf)
        for key, d in (('any', dev), ('pos', np.where(xmin > 0, dev, np.inf))):
            k = int(np.argmin(d))
            if best[key] is None or d[k] < best[key]['max_dev']:
                best[key] = dict(mu_mpc=float(m), x0=float(x0[k]), max_dev=float(d[k]), xmin=float(xmin[k]),
                                 M_over_central=(M[k]/np.array([p['M'] for p in rows])).tolist())
    return best


def main():
    r = json.load(open(sys.argv[1]))
    data = L.load(with_hecs=False)
    out = {}
    for f in L.FOOTINGS:
        out[f] = {}
        for name in L.NAMES:
            ivs = r['rows'][f]['HSE/2sigma'][name]['window_per_Mpc']
            mus = sorted(set(float(m) for a, b in ivs for m in np.geomspace(a, b, 240)))
            out[f][name] = scan(data[name]['prof'], data[name]['rows'], L.A0[f], mus)
            b = out[f][name]
            print(f, name, 'positive: dev %.3f at mu %.3f' % (b['pos']['max_dev'], b['pos']['mu_mpc']),
                  '| no positivity: dev %.3f at mu %.3f xmin %.2e' % (b['any']['max_dev'], b['any']['mu_mpc'],
                                                                      b['any']['xmin']), flush=True)
    out['note'] = L.Adopts_nothing
    json.dump(out, open(sys.argv[2], 'w'), indent=1)


if __name__ == '__main__':
    main()

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
