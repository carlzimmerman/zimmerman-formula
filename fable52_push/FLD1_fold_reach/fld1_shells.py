#!/usr/bin/env python3
"""FLD1: reach of the folded region of the clock, from COL1's exact X14 shells (law-dominated limit).

    python3 fld1_shells.py --footing canonical --logMb 10.45 [--zi 10] [--mode hubble|rest] [--law on|off] [--mu 0]
                           [--N 2400] [--grid scaled|a4] [--tag NAME]   -> runs/<name>.json

Equation, reflection and integrator are COL1's col1_outer.py (A4); this file adds R_fold(t), R_ta(t), the start redshift,
the at-rest mode, the law-off arm and the mu_K dust correction (FROZEN_CRITERIA.md sections 1, 2, 5, 7).
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'COL1_clock_collapse'))
import col1_lib as L
KD1 = json.load(open(os.path.join(HERE, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
RX = [3.0, 10.0, 30.0, 100.0]
RS = 0.3
EPS = 1.0
# A1: reflection at max(FW r_w, RS), FW = 1.2, with the outgoing speed set by energy conservation (ECORR); COL1's A4 used
# FW = 1.001 and no correction (pass FW=1.001, ECORR=False to reproduce it).


def run(footing, lM, zi=10.0, mode='hubble', law='on', mu_Mpc=0.0, N=2400, grid='scaled', out_dt_gyr=0.02, ramp_gyr=1.0,
        FW=1.2, ECORR=True, r_perturb=0.0):
    s = KD1['footings'][footing]['setting']; cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = L.a0_of(footing); Mb = 10 ** lM
    nb0 = cos.nbar0
    if grid == 'a4':
        X = np.logspace(math.log10(20.0), math.log10(8000.0), N)
    else:
        XM = (Mb / ((4 * math.pi / 3) * nb0)) ** (1 / 3)
        X = np.logspace(math.log10(0.03 * XM), math.log10(15 * XM), N)
    MX = (4 * math.pi / 3) * nb0 * X ** 3
    dM = np.diff(np.concatenate([[0.0], MX]))
    mu = mu_Mpc / 1000.0; mu2K = mu * mu / L.K
    if mode == 'hubble':
        ai = 1 / (1 + zi); ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0)
        r = X / (1 + zi) * (1 + r_perturb); v = cos.H_of_a(1 / (1 + zi)) * r
    else:                                          # at rest at today's mean density, mean gravity subtracted
        ti = 0.0; tend = (cos.t_of_a(1.0) - cos.t_of_a(1 / 11.))
        r = X.copy(); v = np.zeros_like(X)
    U = lambda y: a0 * y / (a0 - np.abs(y))

    def nbar(t):
        return nb0 * cos.a_of_t(t) ** -3 if mode == 'hubble' else nb0

    DMDbox = [None]

    def mpi(t, r):
        m0 = MX - (4 * math.pi / 3) * nbar(t) * r ** 3
        if mu2K == 0.0 or law == 'off':
            return m0
        # dust correction (section 5): dh = Int_r^inf A dr ; dM_d(<r) = mu^2/K Int_0^r 4 pi r'^2 dh dr'
        o = np.argsort(r); rs = r[o]
        A = U(np.clip(L.G * m0[o] / rs ** 2, -0.999999 * a0, 0.999999 * a0))
        seg = 0.5 * (A[1:] + A[:-1]) * np.diff(rs)
        dh = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        integ = 4 * math.pi * rs ** 2 * dh
        dMd = mu2K * np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(rs))])
        dMd += mu2K * (4 * math.pi / 3) * rs[0] ** 3 * dh[0]
        out = np.empty_like(m0); out[o] = m0[o] - dMd
        dmd = np.empty_like(m0); dmd[o] = dMd; DMDbox[0] = dmd
        return out

    def acc(t, r, idx=None):
        MXs = MX if idx is None else MX[idx]
        M = Mb * float(L.smoothstep((t - ti) / (ramp_gyr / L.TU)))
        if mode == 'hubble':
            a = cos.a_of_t(t)
            g = (-L.G * M * r / (r * r + EPS * EPS) ** 1.5 - L.G * MXs / r ** 2
                 + (-(4 * math.pi / 3) * L.G * cos.rhob0 * a ** -3 + cos.OL * cos.H0 ** 2) * r)
        else:
            g = -L.G * M * r / (r * r + EPS * EPS) ** 1.5 - L.G * MXs / r ** 2 + (4 * math.pi / 3) * L.G * nb0 * r
        if law == 'on':
            if idx is None:
                mp = mpi(t, r)
            else:
                mp = MXs - (4 * math.pi / 3) * nbar(t) * r ** 3 - (DMD[idx] if DMD is not None else 0.0)
            y = np.clip(L.G * mp / r ** 2, -0.999999 * a0, 0.999999 * a0)
            g = g + U(y)
        return g

    def wall(t, r):
        if law == 'off':
            return np.full_like(r, RS)
        m = np.maximum(MX - (4 * math.pi / 3) * nbar(t) * r ** 3, 0.0)
        return np.maximum(np.sqrt(L.G * m / a0) * FW, RS)

    DMD = None
    t = ti; A = acc(t, r)
    first = {rx: None for rx in RX}
    crossed = np.zeros(N, bool)
    rmax = r.copy()
    TS = []; next_out = ti
    nsteps = 0; T0 = time.time()
    while t < tend:
        dt = min(0.02 * np.min(r / np.maximum(np.abs(v), 1e-3)), 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(A), 1e-12))),
                 1e-3, tend - t)
        r_old = r; v_old = v
        vh = v + 0.5 * dt * A
        rn = r + dt * vh
        rw = wall(t + dt, rn)
        hit = rn < rw
        if hit.any():
            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit])
        t += dt; r = rn
        A = acc(t, r)
        v = vh + 0.5 * dt * A
        if hit.any() and ECORR:                    # A1: outgoing speed from energy conservation across the step
            idx = np.where(hit)[0]
            DMD = DMDbox[0]
            ro, rn_ = r_old[idx], r[idx]; mid = 0.5 * (ro + rn_)
            dV = -(rn_ - ro) * (acc(t, ro, idx) + 4 * acc(t, mid, idx) + acc(t, rn_, idx)) / 6
            v[idx] = np.sqrt(np.maximum(v_old[idx] ** 2 - 2 * dV, 0.0))
        nsteps += 1
        rmax = np.maximum(rmax, r)
        inv = np.where(np.diff(r) <= 0)[0]
        if len(inv):
            crossed[inv] = True; crossed[inv + 1] = True
            for rx in RX:
                if first[rx] is None:
                    ok = inv[(r[inv] > rx) & (r[inv + 1] > rx)]
                    if len(ok):
                        first[rx] = {'t_since_start_gyr': (t - ti) * L.TU,
                                     'z': (1 / cos.a_of_t(t) - 1) if mode == 'hubble' else None, 'r_kpc': float(r[ok[0]])}
        if t >= next_out or t >= tend:
            rf = float(r[crossed].max()) if crossed.any() else 0.0
            fall = v <= 0
            rta = float(r[fall].max()) if fall.any() else 0.0
            TS.append([(t - ti) * L.TU, (1 / cos.a_of_t(t) - 1) if mode == 'hubble' else float('nan'), rf, rta,
                       float(crossed.mean())])
            next_out += out_dt_gyr / L.TU
    turned = rmax > 1.01 * r
    Mph = lambda R: R * R * (L.law_g(L.G * Mb * R / (R * R + EPS * EPS) ** 1.5, a0) - L.G * Mb * R / (R * R + EPS * EPS) ** 1.5) / L.G
    reads_end = {f'{R:g}': {'M_N_all_shells_over_M_ph': float(np.sum(dM[r < R])) / Mph(R),
                            'M_N_uncrossed_over_M_ph': float(np.sum(dM[(r < R) & ~crossed])) / Mph(R)} for R in (10.0, 30.0, 100.0, 300.0)}
    return {'reads_end': reads_end,'footing': footing, 'logMb': lM, 'zi': zi, 'mode': mode, 'law': law, 'mu_Mpc': mu_Mpc, 'N': N, 'grid': grid,
            'X_range_kpc': [float(X[0]), float(X[-1])], 'first_crossing_outside': {f'{k:g}': v for k, v in first.items()},
            'series_cols': ['t_since_start_gyr', 'z', 'R_fold_kpc', 'R_ta_kpc', 'fraction_crossed'], 'series': TS,
            'R_fold_end_kpc': TS[-1][2], 'R_ta_end_kpc': TS[-1][3],
            'charge_turned_around_over_Mb': float(MX[turned].max()) / Mb if turned.any() else 0.0,
            'steps': nsteps, 'wall_s': time.time() - T0,
            'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--footing', default='canonical'); ap.add_argument('--logMb', type=float, default=10.45)
    ap.add_argument('--zi', type=float, default=10.0); ap.add_argument('--mode', default='hubble')
    ap.add_argument('--law', default='on'); ap.add_argument('--mu', type=float, default=0.0)
    ap.add_argument('--N', type=int, default=2400); ap.add_argument('--grid', default='scaled'); ap.add_argument('--tag', default='')
    ap.add_argument('--perturb', type=float, default=0.0)
    a = ap.parse_args()
    name = a.tag or (f'{a.mode}_{a.footing}_M{a.logMb:g}_zi{a.zi:g}_N{a.N}' + ('' if a.law == 'on' else '_lawoff')
                     + ('' if a.mu == 0 else f'_mu{a.mu:g}') + ('' if a.grid == 'scaled' else f'_{a.grid}') + ('' if a.perturb == 0 else '_perturb'))
    os.makedirs(os.path.join(HERE, 'runs'), exist_ok=True)
    o = run(a.footing, a.logMb, a.zi, a.mode, a.law, a.mu, a.N, a.grid, r_perturb=a.perturb)
    json.dump(o, open(os.path.join(HERE, 'runs', name + '.json'), 'w'), indent=1, default=str)
    fc = o['first_crossing_outside']
    print(f'{name}: R_fold(end) {o["R_fold_end_kpc"]:.1f} kpc, R_ta(end) {o["R_ta_end_kpc"]:.1f} kpc; first crossing outside 3/10/30/100: '
          + ' / '.join('none' if fc[k] is None else f'{fc[k]["t_since_start_gyr"]:.3f}' for k in ('3', '10', '30', '100'))
          + f' Gyr; steps {o["steps"]}, {o["wall_s"]:.0f}s')
