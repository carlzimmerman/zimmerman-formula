#!/usr/bin/env python3
"""FINAL-18 (KAPPA_B) production runs + code-fidelity known answer KA-1.

    python3 final18_run.py [--workers 8] [--grid production|ka1|g2|all]

Rows are FLD1's shell equation exactly (patched copy, see final18_shells.py):
  production : s = 1, N = 1200, zi = 10, law on, both footings, 12 masses   (G3, G4, G5)
  ka1        : s = 1, N = 1200 and N = 2400, canonical; N = 2400 alt          (KA-1 fidelity)
  g2         : a_0 -> s a_0, s in {0.1, 10, 100}; wall scaled and held fixed  (G2)
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, os, sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import final18_shells as F

MASSES = [6.5, 7.0, 8.0, 9.0, 9.4, 10.0, 10.45, 10.7, 10.9, 11.2, 11.5, 12.0]
FLD1 = os.path.join(HERE, '..', '..', 'fable52_push', 'FLD1_fold_reach', 'runs')


def job(cfg):
    footing, lM, N, s, wallscale, tag = cfg
    o = F.run(footing, lM, zi=10.0, N=N, s=s, wallscale=wallscale)
    os.makedirs(os.path.join(HERE, 'runs'), exist_ok=True)
    json.dump(o, open(os.path.join(HERE, 'runs', tag + '.json'), 'w'), indent=1, default=str)
    return (tag, o['R_fold_z0_kpc'], o['q_cross_z0'], o['q_turn_z0'], o['q_front_z0'],
            o['eps_u_max_run'], o['eps_u_front_run'], o['X_fold_z0'], o['r_M_kpc'], o['wall_s'])


def configs(which):
    out = []
    if which in ('production', 'all'):
        for f in ('canonical', 'alt'):
            for m in MASSES:
                out.append((f, m, 1200, 1.0, True, f'prod_{f}_M{m:g}_N1200_s1'))
    if which in ('ka1', 'all'):
        out.append(('canonical', 10.45, 1200, 1.0, True, 'ka1_canonical_M10.45_N1200_s1'))
        out.append(('canonical', 10.45, 2400, 1.0, True, 'ka1_canonical_M10.45_N2400_s1'))
        out.append(('alt', 10.45, 2400, 1.0, True, 'ka1_alt_M10.45_N2400_s1'))
    if which in ('g2', 'all'):
        for f in ('canonical', 'alt'):
            for m in (8.0, 10.45):
                for s in (0.1, 10.0):
                    out.append((f, m, 1200, s, True, f'g2_{f}_M{m:g}_N1200_s{s:g}_w1'))
            out.append((f, 10.45, 1200, 100.0, True, f'g2_{f}_M10.45_N1200_s100_w1'))
        for s in (0.1, 10.0):
            out.append(('canonical', 10.45, 1200, s, False, f'g2_canonical_M10.45_N1200_s{s:g}_w0'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--grid', default='all')
    a = ap.parse_args()
    cfgs = configs(a.grid)
    print(f'FINAL-18 production: {len(cfgs)} rows, {a.workers} workers', flush=True)
    with Pool(a.workers) as p:
        for res in p.imap_unordered(job, cfgs):
            print(f'  {res[0]}: R_fold(z=0) {res[1]:.4f} kpc, q_cross {res[2]:.6f}, q_turn {res[3]:.6f}, '
                  f'q_front {res[4]:.6f}, eps_u(max) {res[5]:.3e}, eps_u(front) {res[6]:.3e}, '
                  f'X_fold {res[7]:.4f}, r_M {res[8]:.4f} kpc, {res[9]:.0f}s', flush=True)
    print('FINAL-18 rows done.', flush=True)


if __name__ == '__main__':
    main()
