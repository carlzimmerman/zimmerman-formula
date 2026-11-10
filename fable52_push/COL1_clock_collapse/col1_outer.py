#!/usr/bin/env python3
"""COL1 reported diagnostic (amendment A4): independent shells, law-dominated limit mu_K L << 1, X14's exact equation.

    python3 col1_outer.py -> col1_outer.json / col1_outer.out

Each shell: r'' = -G M_b s(t) r/(r^2+eps^2)^1.5 - G M_X/r^2 - (4 pi/3) G rho_b(t) r + Omega_L H0^2 r + U(G [M_X - (4 pi/3) nbar(t) r^3]/r^2).
A shell that reaches its flux-cap wall (or r_s = 0.3 kpc, where it would pass through the centre) is reflected elastically.
Vectorised leapfrog; the first order inversion among shells that are both outside r_x is the first crossing outside r_x.
Sets no label. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import col1_lib as L
KD1 = json.load(open(os.path.join(HERE, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
OUT = []; RES = {'note': 'A4 diagnostic; sets no label. kappa = 1/2 FITTED; not theory closed.', 'rows': {}}
RX = [3.0, 10.0, 30.0, 100.0]
RS = 0.3


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def run(f, lM, N=2400):
    s = KD1['footings'][f]['setting']; cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = L.a0_of(f); Mb = 10 ** lM; eps = 1.0
    X = np.logspace(math.log10(20.0), math.log10(8000.0), N)
    MX = (4 * math.pi / 3) * cos.nbar0 * X ** 3
    ti = cos.t_of_a(1 / 11.); t0 = cos.t_of_a(1.0)
    r = X / 11.; v = cos.H_of_a(1 / 11.) * r
    U = lambda y: a0 * y / (a0 - np.abs(y))

    def acc(t, r):
        a = cos.a_of_t(t)
        M = Mb * float(L.smoothstep((t - ti) / (1 / L.TU)))
        y = L.G * (MX - (4 * math.pi / 3) * cos.nbar0 * a ** -3 * r ** 3) / r ** 2
        y = np.clip(y, -0.999999 * a0, 0.999999 * a0)
        return (-L.G * M * r / (r * r + eps * eps) ** 1.5 - L.G * MX / r ** 2
                + (-(4 * math.pi / 3) * L.G * cos.rhob0 * a ** -3 + cos.OL * cos.H0 ** 2) * r + U(y))

    def wall(t, r):
        a = cos.a_of_t(t)
        mpi = MX - (4 * math.pi / 3) * cos.nbar0 * a ** -3 * r ** 3
        rw = np.sqrt(np.maximum(L.G * mpi, 0.0) / a0) * 1.001
        return np.maximum(rw, RS)

    t = ti; A = acc(t, r)
    first = {rx: None for rx in RX}
    crossed = np.zeros(N, bool); tcross = np.full(N, np.nan)
    rmax = r.copy()
    hist_t, hist_r, hist_v = [], [], []
    nsteps = 0; next_snap = ti
    while t < t0:
        dt = min(0.02 * np.min(r / np.maximum(np.abs(v), 1e-3)), 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(A), 1e-12))),
                 1e-3, t0 - t)
        vh = v + 0.5 * dt * A
        rn = r + dt * vh
        rw = wall(t + dt, rn)
        hit = rn < rw
        if hit.any():                                # elastic reflection at the wall / passage through the centre
            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit])
        t += dt; r = rn
        A = acc(t, r)
        v = vh + 0.5 * dt * A
        nsteps += 1
        rmax = np.maximum(rmax, r)
        inv = np.where(np.diff(r) <= 0)[0]           # order inversions between Lagrangian neighbours
        if len(inv):
            crossed[inv] = True; crossed[inv + 1] = True
            tcross[inv] = np.where(np.isnan(tcross[inv]), t, tcross[inv]); tcross[inv + 1] = np.where(np.isnan(tcross[inv + 1]), t, tcross[inv + 1])
            for rx in RX:
                if first[rx] is None:
                    ok = inv[(r[inv] > rx) & (r[inv + 1] > rx)]
                    if len(ok):
                        first[rx] = {'t_since_start_gyr': (t - ti) * L.TU, 'z': 1 / cos.a_of_t(t) - 1, 'r_kpc': float(r[ok[0]]),
                                     'X_kpc': float(X[ok[0]])}
        if t >= next_snap:
            hist_t.append(t); hist_r.append(r.copy()); hist_v.append(v.copy()); next_snap += 0.25 / L.TU
    # z = 0 reads, uncrossed shells only
    a = 1.0
    Mph = lambda R: R * R * (L.law_g(L.G * Mb * R / (R * R + eps * eps) ** 1.5, a0) - L.G * Mb * R / (R * R + eps * eps) ** 1.5) / L.G
    reads = {}
    for R in (10.0, 30.0, 100.0, 300.0):
        inside = r < R
        reads[f'{R:g}'] = {'M_N_uncrossed_over_M_ph': float(np.sum(np.diff(np.concatenate([[0], MX]))[inside & ~crossed])) / Mph(R),
                           'M_N_all_shells_over_M_ph': float(np.sum(np.diff(np.concatenate([[0], MX]))[inside])) / Mph(R),
                           'M_ph_over_Mb': Mph(R) / Mb}
    # turned-around charge: shells now inside their own maximum radius by > 1 %
    turned = rmax > 1.01 * r
    Mturn = float(MX[turned].max()) if turned.any() else 0.0
    out = {'first_crossing_outside': first, 'fraction_shells_crossed_by_z0': float(crossed.mean()),
           'charge_turned_around_over_Mb': Mturn / Mb, 'reads_z0': reads, 'steps': nsteps,
           'innermost_uncrossed_X_kpc': float(X[~crossed][0]) if (~crossed).any() else None}
    return out


def report(f, lM, o):
    if True:
        if True:
            RES['rows'][f'{f}|{lM}'] = o
            fc = o['first_crossing_outside']
            P(f'{f:9s} log M_b {lM:5g}: first crossing outside ' + '; '.join(
                f'{rx:g} kpc: ' + ('none' if fc[rx] is None else f'{fc[rx]["t_since_start_gyr"]:.3f} Gyr (z {fc[rx]["z"]:.2f}) at {fc[rx]["r_kpc"]:.1f} kpc')
                for rx in RX))
            rd = o['reads_z0']
            P(f'      z 0: shells crossed {o["fraction_shells_crossed_by_z0"]:.3f}; charge turned around {o["charge_turned_around_over_Mb"]:.2f} M_b;'
              f' M_N(all shells)/M_ph at 10/30/100/300 = ' + ' / '.join(f'{rd[k]["M_N_all_shells_over_M_ph"]:.3g}' for k in ('10', '30', '100', '300'))
              + '; uncrossed only = ' + ' / '.join(f'{rd[k]["M_N_uncrossed_over_M_ph"]:.3g}' for k in ('10', '30', '100', '300')))


if __name__ == '__main__':
    # one row per process: python3 col1_outer.py <footing> <logMb>  -> runs/outer_<f>_<M>.json ; merge: python3 col1_outer.py merge
    if len(sys.argv) == 3:
        f, lM = sys.argv[1], float(sys.argv[2])
        o = run(f, lM)
        json.dump(o, open(os.path.join(HERE, 'runs', f'outer_{f}_M{lM:g}.json'), 'w'), indent=1, default=str)
    else:
        P('COL1 A4 outer-shell diagnostic (law-dominated limit, X14 shells, Hubble start z 10). Sets no label. kappa = 1/2 FITTED; not theory closed.')
        for f in ('canonical', 'alt'):
            for lM in (9.4, 10.45, 10.7, 10.9):
                o = json.load(open(os.path.join(HERE, 'runs', f'outer_{f}_M{lM:g}.json')))
                o['first_crossing_outside'] = {float(k): v for k, v in o['first_crossing_outside'].items()}
                report(f, lM, o)
        RES['rows'] = {k: v for k, v in RES['rows'].items()}
        json.dump(RES, open(os.path.join(HERE, 'col1_outer.json'), 'w'), indent=1, default=str)
        open(os.path.join(HERE, 'col1_outer.out'), 'w').write('\n'.join(OUT) + '\n\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n')
