#!/usr/bin/env python3
"""FINAL-18 (KAPPA_B) added item G2c: the SELF-CONSISTENT root of the fold matching condition.

(M) was evaluated in the main lane with the fold inputs (R_fold, Q_fold) taken at the frozen a_0. But G2
showed those inputs are themselves weakly a_0-dependent (~1e-2 dex per dex), so the honest object is the
fixed point of

    a_0 -> a_0^M(a_0) = G M_b q(1+q)/R_fold(a_0)^2 ,

i.e.  s -> s' with s = a_0/a_0(frozen).  This script iterates that map with the SAME fold solver, and
prints the sequence. It is an ADDED item (G2 failed its frozen 1e-6 rule; see RESULT.md), reported and
disclosed as such.

    python3 final18_fixedpoint.py [--steps 4] [--mass 10.45]
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, math, os, sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'fable52_push', 'COL1_clock_collapse'))
import col1_lib as L
import final18_shells as F

KD1 = json.load(open(os.path.join(HERE, '..', '..', 'closure_2026_11_06', 'KD1_unpinned_kq_dust', 'kd1.json')))
C_KMS = 2.99792458e5
G = L.G


def rho_L(footing):
    s = KD1['footings'][footing]['setting']
    c = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    return c.OL * c.rhoc0


def one(args):
    footing, m, s, N = args
    o = F.run(footing, m, zi=10.0, N=N, s=s, wallscale=True)
    a0 = L.a0_of(footing)
    Mb = 10 ** m
    R = o['R_fold_z0_kpc']
    q = o['q_front_z0']
    a0M = G * Mb * q * (1 + q) / R ** 2
    return dict(footing=footing, m=m, s=s, R=R, q=q, q_cross=o['q_cross_z0'], q_turn=o['q_turn_z0'],
                a0M=a0M, sprime=a0M / a0, kappa=a0M / (C_KMS * math.sqrt(G * rho_L(footing))),
                eps_u=o['eps_u_max_run'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--steps', type=int, default=4)
    ap.add_argument('--mass', type=float, default=10.45)
    ap.add_argument('--N', type=int, default=1200)
    ap.add_argument('--workers', type=int, default=2)
    a = ap.parse_args()
    cfgs = [(f, a.mass, 1.0, a.N) for f in ('canonical', 'alt')]
    hist = {f: [] for f in ('canonical', 'alt')}
    print('FINAL-18 G2c: self-consistent fixed point of the fold matching condition')
    print('  s = a_0/a_0(frozen); the map is s -> s\' = G M_b q(1+q)/(R_fold(s)^2 a_0(frozen))')
    for step in range(a.steps):
        with Pool(a.workers) as p:
            res = p.map(one, cfgs)
        for r in res:
            hist[r['footing']].append(r)
            print(f"  {r['footing']:9s} step {step}: s_in {r['s']:.6e} -> R_fold {r['R']:11.4f} kpc, "
                  f"q_front {r['q']:.5f}, a_0^M {r['a0M'] * 1e6 / 3.0857e19:.4e} m/s^2, "
                  f"kappa_M {r['kappa']:.4e}, s_out {r['sprime']:.6e}")
        cfgs = [(r['footing'], a.mass, min(max(r['sprime'], 1e-8), 1e8), a.N) for r in res]
        if all(r['sprime'] < 1e-6 or r['sprime'] > 1e6 for r in res):
            print('  map has left the probed range; stopping.')
            break
    json.dump(hist, open(os.path.join(HERE, 'final18_fixedpoint.json'), 'w'), indent=1, default=str)
    print('  wrote final18_fixedpoint.json')
    print('  kappa = 1/2 FITTED; not theory closed.')


if __name__ == '__main__':
    main()
