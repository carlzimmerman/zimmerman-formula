#!/usr/bin/env python3
"""FINAL-18 (KAPPA_B): patched copy of FLD1's fold solver (origin bce6d61451).

    python3 final18_shells.py --footing canonical --logMb 10.45 [--s 1] [--wallscale 1] [--N 1200] [--tag NAME]

The equation, the reflection and the integrator are FLD1's `fld1_shells.py` verbatim in substance; three
things are ADDED and nothing is changed:

  * the fold-front charge series `q_fold(t) = M(< x_L(t))/M_b` on both criteria
    (`crossed`: radial-order inversion, the front itself; `turned`: FLD1's stored rmax > 1.01 r, a lagged
    lower bound);
  * an `a_0` scale knob `s` (a_0 -> s a_0) in the law force U, with an independent flag for whether the
    flux-cap wall radius r_w = sqrt(G m/a_0) FW follows it (`--wallscale`);
  * a diagnostic `eps_u(t) = max_shells |u|/a_0`, with u = G (M_X - M_bg)/r^2 the excess (polarization) field,
    i.e. the exact small parameter of the G1 cancellation lemma.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'fable52_push', 'COL1_clock_collapse'))
import col1_lib as L
KD1 = json.load(open(os.path.join(HERE, '..', '..', 'closure_2026_11_06', 'KD1_unpinned_kq_dust', 'kd1.json')))
RS = 0.3
EPS = 1.0


def run(footing, lM, zi=10.0, mode='hubble', law='on', mu_Mpc=0.0, N=1200, grid='scaled', out_dt_gyr=0.02,
        ramp_gyr=1.0, FW=1.2, ECORR=True, s=1.0, wallscale=True):
    """s: a_0 -> s * a_0 in the law force U only (the wall follows only if wallscale)."""
    st = KD1['footings'][footing]['setting']; cos = L.Cosmo(st['h'], st['omega_d'], st['omega_b'])
    a0 = L.a0_of(footing)                       # internal units: (km/s)^2 / kpc
    a0l = s * a0                                # the a_0 that appears in the law force
    nb0 = cos.nbar0
    if grid == 'a4':
        X = np.logspace(math.log10(20.0), math.log10(8000.0), N)
    else:
        XM = (10 ** lM / ((4 * math.pi / 3) * nb0)) ** (1 / 3)
        X = np.logspace(math.log10(0.03 * XM), math.log10(15 * XM), N)
    MX = (4 * math.pi / 3) * nb0 * X ** 3
    dM = np.diff(np.concatenate([[0.0], MX]))
    mu = mu_Mpc / 1000.0; mu2K = mu * mu / L.K

    def nbar(t):
        return nb0 * cos.a_of_t(t) ** -3 if mode == 'hubble' else nb0

    DMDbox = [None]

    def mpi(t, r):
        m0 = MX - (4 * math.pi / 3) * nbar(t) * r ** 3
        if mu2K == 0.0 or law == 'off':
            return m0
        U = lambda y: a0l * y / (a0l - np.abs(y))
        o = np.argsort(r); rs = r[o]
        A = U(np.clip(L.G * m0[o] / rs ** 2, -0.999999 * a0l, 0.999999 * a0l))
        seg = 0.5 * (A[1:] + A[:-1]) * np.diff(rs)
        dh = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        integ = 4 * math.pi * rs ** 2 * dh
        dMd = mu2K * np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(rs))])
        dMd += mu2K * (4 * math.pi / 3) * rs[0] ** 3 * dh[0]
        out = np.empty_like(m0); out[o] = m0[o] - dMd
        dmd = np.empty_like(m0); dmd[o] = dMd; DMDbox[0] = dmd
        return out

    U = lambda y: a0l * y / (a0l - np.abs(y))

    def acc(t, r, idx=None):
        MXs = MX if idx is None else MX[idx]
        M = (10 ** lM) * float(L.smoothstep((t - ti) / (ramp_gyr / L.TU)))
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
            y = np.clip(L.G * mp / r ** 2, -0.999999 * a0l, 0.999999 * a0l)
            g = g + U(y)
        return g

    def wall(t, r):
        if law == 'off':
            return np.full_like(r, RS)
        a0w = a0l if wallscale else a0
        m = np.maximum(MX - (4 * math.pi / 3) * nbar(t) * r ** 3, 0.0)
        return np.maximum(np.sqrt(L.G * m / a0w) * FW, RS)

    if mode == 'hubble':
        ai = 1 / (1 + zi); ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0)
        r = X / (1 + zi); v = cos.H_of_a(1 / (1 + zi)) * r
    else:
        ti = 0.0; tend = (cos.t_of_a(1.0) - cos.t_of_a(1 / 11.))
        r = X.copy(); v = np.zeros_like(X)
    DMD = None
    t = ti; A = acc(t, r)
    crossed = np.zeros(N, bool); rmax = r.copy()
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
        if hit.any() and ECORR:
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
        if t >= next_out or t >= tend:
            rf = float(r[crossed].max()) if crossed.any() else 0.0
            fall = v <= 0
            rta = float(r[fall].max()) if fall.any() else 0.0
            turned = rmax > 1.01 * r
            qc = float(MX[crossed].max()) / (10 ** lM) if crossed.any() else 0.0
            qt = float(MX[turned].max()) / (10 ** lM) if turned.any() else 0.0
            # G1 small parameter: u = G (M_X - M_bg)/r^2 over a_0, on every shell
            m0 = MX - (4 * math.pi / 3) * nbar(t) * r ** 3
            uu = np.abs(L.G * m0 / r ** 2) / a0l
            uf = float(uu[crossed].max()) if crossed.any() else 0.0
            ifront = int(np.argmax(np.where(crossed, r, -np.inf))) if crossed.any() else 0
            ufront = float(uu[ifront]) if crossed.any() else 0.0
            qf = float(MX[ifront]) / (10 ** lM) if crossed.any() else 0.0
            TS.append([(t - ti) * L.TU, (1 / cos.a_of_t(t) - 1) if mode == 'hubble' else float('nan'), rf, rta,
                       float(crossed.mean()), qc, qt, float(uu.max()), uf, ufront, qf])
            next_out += out_dt_gyr / L.TU
    Mb = 10 ** lM
    rM = math.sqrt(L.G * Mb / a0)
    Xf = lambda R: (math.sqrt(1 + 4 * (R / rM) ** 2) - 1) / 2
    last = TS[-1]
    out = {'footing': footing, 'logMb': lM, 'zi': zi, 'mode': mode, 'law': law, 'mu_Mpc': mu_Mpc, 'N': N, 'grid': grid,
           's': s, 'wallscale': wallscale, 'r_M_kpc': rM,
           'series_cols': ['t_since_start_gyr', 'z', 'R_fold_kpc', 'R_ta_kpc', 'fraction_crossed',
                           'q_cross', 'q_turn', 'eps_u_max', 'eps_u_crossed', 'eps_u_front', 'q_front'],
           'series': TS,
           'R_fold_z0_kpc': last[2], 'R_ta_z0_kpc': last[3], 'q_cross_z0': last[5], 'q_turn_z0': last[6],
           'eps_u_max_run': float(max(row[7] for row in TS)),
           'eps_u_crossed_run': float(max(row[8] for row in TS)),
           'eps_u_front_run': float(max(row[9] for row in TS)),
           'q_front_z0': last[10],
           'X_fold_z0': Xf(last[2]), 'steps': nsteps, 'wall_s': time.time() - T0,
           'note': 'Patched copy of FLD1 fld1_shells.py (origin bce6d61451). Adopts nothing. kappa = 1/2 FITTED.'}
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--footing', default='canonical'); ap.add_argument('--logMb', type=float, default=10.45)
    ap.add_argument('--zi', type=float, default=10.0); ap.add_argument('--mode', default='hubble')
    ap.add_argument('--law', default='on'); ap.add_argument('--mu', type=float, default=0.0)
    ap.add_argument('--N', type=int, default=1200); ap.add_argument('--grid', default='scaled')
    ap.add_argument('--s', type=float, default=1.0); ap.add_argument('--wallscale', type=int, default=1)
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    name = a.tag or f'{a.mode}_{a.footing}_M{a.logMb:g}_zi{a.zi:g}_N{a.N}_s{a.s:g}_w{int(a.wallscale)}'
    os.makedirs(os.path.join(HERE, 'runs'), exist_ok=True)
    o = run(a.footing, a.logMb, a.zi, a.mode, a.law, a.mu, a.N, a.grid, s=a.s, wallscale=bool(a.wallscale))
    json.dump(o, open(os.path.join(HERE, 'runs', name + '.json'), 'w'), indent=1, default=str)
    print(f"{name}: R_fold(z=0) {o['R_fold_z0_kpc']:.4f} kpc, R_ta {o['R_ta_z0_kpc']:.4f}, "
          f"q_cross {o['q_cross_z0']:.6f}, q_turn {o['q_turn_z0']:.6f}, X_fold {o['X_fold_z0']:.4f}, "
          f"eps_u_max {o['eps_u_max_run']:.3e}, steps {o['steps']}, {o['wall_s']:.0f}s")
