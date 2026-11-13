#!/usr/bin/env python3
"""EXR1R K6 (run only after the blind outputs were committed): my G2 solver, imported unchanged from exr1r_lib, on
ESZ1's 237 W lenses (esz1_per_lens.csv, is_W = 1), far source, b* = +0.10, both footings, against the medians stored in
esz1_results.json (Mg_med over all; mass-weighted kT and n_e at R_E over lenses that need gas, as ESZ1 stores them).
Frozen tolerance 0.1 %. Output exr1r_k6_posthoc.{out,json}. kappa = 1/2 FITTED; not theory closed.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exr1r_lib import *  # noqa: E402,F401,F403

ESZ = os.path.join(HERE, '..', 'ESZ1_wide_lens_gas_pressure')
ids = [r['unique_identifier'] for r in csv.DictReader(open(os.path.join(ESZ, 'esz1_per_lens.csv'))) if r['is_W'] == '1']
ref = json.load(open(os.path.join(ESZ, 'esz1_results.json')))['model']
S, _ = load_sample()
D = {d['id']: d for d in S}
log, out, worst = [], {}, 0.0
for foot, a0 in A0.items():
    mg, ktm, ne, ktq = [], [], [], []
    for i in ids:
        L = Lens(D[i], bstar=0.10, zs=1100.0)
        A = L.solve_A(a0)
        mg.append(L.mgas_total(A) / MSUN)
        if A > 0:
            r, kT = L.kT_profile(A, a0, rmin_kpc=1e-4, npts=20000)
            # mass-weighted: dM = 4 pi A dr for rho = A r^-2, so <kT> = (1/r_t) int kT dr
            ktm.append(np.trapz(kT * r, np.log(r)) / L.rt)
            ne.append(A / L.RE ** 2 / (MU_E * MP) * 1e-6)
            # the same quantity with ESZ1's stated quadrature (1000 log points from 0.02 kpc, trapezoid in ln r for
            # P and for P r^3), to trace any difference to discretisation (post hoc)
            rg = np.geomspace(0.02 * KPC, L.rt, 1000)
            f = (A / rg ** 2) * L.g(rg, A, a0) * rg
            h = np.log(rg[1] / rg[0])
            Pr = np.zeros_like(f)
            Pr[:-1] = np.cumsum((0.5 * (f[:-1] + f[1:]) * h)[::-1])[::-1]
            w = np.full(len(rg), h)
            w[0] = w[-1] = 0.5 * h
            ktq.append(MU * MP * 4 * np.pi * np.sum(Pr * rg ** 3 * w) / L.mgas_total(A) / KEV)
    got = {'Mg_med': float(np.median(mg)), 'kT_med': float(np.median(ktm)), 'ne_med': float(np.median(ne))}
    want = ref[f'{foot}|G2|far|+0.10']
    dev = {k: got[k] / want[k] - 1 for k in got}
    worst = max(worst, max(abs(v) for v in dev.values()))
    kq = float(np.median(ktq))
    out[foot] = {'N': len(ids), 'mine': got, 'esz1': {k: want[k] for k in got}, 'rel_dev': dev,
                 'kT_med_on_esz1_quadrature': kq, 'rel_dev_kT_on_esz1_quadrature': kq / want['kT_med'] - 1}
    log.append(f'{foot}: N {len(ids)}; ' + '; '.join(f'{k} mine {got[k]:.6g} ESZ1 {want[k]:.6g} ({dev[k]:+.2e})'
                                                     for k in got)
               + f'; kT_med on ESZ1 quadrature {kq:.6g} ({kq / want["kT_med"] - 1:+.2e})')
ok = worst < 1e-3
worst_q = max(max(abs(out[f]['rel_dev'][k]) for k in ('Mg_med', 'ne_med')) for f in A0)
worst_q = max(worst_q, max(abs(out[f]['rel_dev_kT_on_esz1_quadrature']) for f in A0))
log.append(f'K6 (post hoc, after the blind commit): converged integrals, worst relative deviation {worst:.2e} (0.1 %) '
           f'-> {"PASS" if ok else "FAIL"}; with ESZ1 own quadrature for the mass-weighted kT, worst {worst_q:.2e} -> '
           f'{"PASS" if worst_q < 1e-3 else "FAIL"}')
out['worst_on_esz1_quadrature'] = worst_q
out['K6_pass'] = bool(ok)
out['worst'] = worst
print('\n'.join(log))
open(os.path.join(HERE, 'exr1r_k6_posthoc.out'), 'w').write('\n'.join(log) + '\n')
json.dump(out, open(os.path.join(HERE, 'exr1r_k6_posthoc.json'), 'w'), indent=1)
