#!/usr/bin/env python3
"""v3s soft side: do khronon elements shell-cross in finite time in the moving MW-M31 saddle? (FROZEN_CRITERIA.md, 60b8506f4e)

Units: kpc, Gyr, Msun.  Soft elements (QUMOND phantom < 0 at t_i) move as test particles in the difference field
Delta g_b(x,t) = g_b(x,t) - g_b(x,t_i), plus an optional isotropic soft-side growth term s * Gamma^2.  The deformation
D = dxi/dq obeys D'' = -Delta T_b(x,t)(I + D) + s Gamma^2 D; shell crossing <=> det(I + D) <= 0.
--mutate: masses frozen at r(t_i).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MUTATE = "--mutate" in sys.argv
HERE = Path(__file__).resolve().parent
G = 4.498502151469554e-06            # kpc^3 / (Msun Gyr^2)
MS_TO_KPCGYR2 = (3.15576e16) ** 2 / 3.0856775814913673e19
A0 = {"canonical": 9.36e-11 * MS_TO_KPCGYR2, "alt": 1.13e-10 * MS_TO_KPCGYR2}
KMS = 1.0227121650537077               # kpc/Gyr per km/s
M1, M2 = 6e10, 1e11                    # MW, M31 baryons (H4 S1)
EPS = 20.0                             # Plummer softening, kpc
R0, V0, T0 = 780.0, -110.0 * KMS, 13.8
checks, out = [], {"mutate": MUTATE}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


# ================================================================ orbits
def f_eta(eta):
    return math.sin(eta) * (eta - math.sin(eta)) / (1 - math.cos(eta)) ** 2


eta0 = brentq(lambda e: f_eta(e) - V0 * T0 / R0, math.pi + 1e-9, 2 * math.pi - 1e-6)
a_k = R0 / (1 - math.cos(eta0))
GMk = a_k ** 3 * ((eta0 - math.sin(eta0)) / T0) ** 2
tk = math.sqrt(a_k ** 3 / GMk)


def r_O1(t):
    eta = brentq(lambda e: tk * (e - math.sin(e)) - t, 0.0, 2 * math.pi)
    return a_k * (1 - math.cos(eta))


def rdot_O1(t):
    eta = brentq(lambda e: tk * (e - math.sin(e)) - t, 0.0, 2 * math.pi)
    return math.sqrt(GMk / a_k) * math.sin(eta) / (1 - math.cos(eta))


def r_O2(t):
    return R0 + (-V0) * (T0 - t)          # V0 < 0: larger in the past, shrinking after t0


ORBITS = {"O1 timing Kepler": r_O1, "O2 constant velocity": r_O2}
r1t, v1t = r_O1(T0), rdot_O1(T0)
t_end = {"O1 timing Kepler": brentq(lambda t: r_O1(t) - 300.0, T0, tk * 2 * math.pi - 1e-6),
         "O2 constant velocity": T0 + (R0 - 300.0) / (-V0)}
t_ext = {"O1 timing Kepler": brentq(lambda t: r_O1(t) - 150.0, T0, tk * 2 * math.pi - 1e-6),
         "O2 constant velocity": T0 + (R0 - 150.0) / (-V0)}
record("C1", abs(r1t / R0 - 1) < 1e-9 and abs(v1t / V0 - 1) < 1e-9,
       f"O1: r(t0) = {r1t:.9f} kpc, rdot(t0) = {v1t / KMS:.9f} km/s; effective mass {GMk / G:.3e} Msun (orbit parameter, "
       f"not baryons); apocentre t = {math.pi * tk:.3f} Gyr at r = {2 * a_k:.1f} kpc; t_end (r = 300 kpc) O1 "
       f"{t_end['O1 timing Kepler']:.3f} / O2 {t_end['O2 constant velocity']:.3f} Gyr; r = 150 kpc at "
       f"{t_ext['O1 timing Kepler']:.3f} / {t_ext['O2 constant velocity']:.3f} Gyr")
out["orbit"] = {"eta0": eta0, "a_kpc": a_k, "M_eff": GMk / G, "t_apo": math.pi * tk, "t_end": t_end, "t_ext": t_ext}


# ================================================================ fields
def mass_pos(r):
    return np.array([-M2 / (M1 + M2) * r, 0, 0]), np.array([M1 / (M1 + M2) * r, 0, 0])


def g_and_T(X, r):
    """X: (N, 3) -> g (N, 3), T = grad grad phi (N, 3, 3) of the two Plummer masses at separation r."""
    g = np.zeros_like(X)
    T = np.zeros((X.shape[0], 3, 3))
    for M, p in zip((M1, M2), mass_pos(r)):
        d = X - p
        s2 = np.einsum("ni,ni->n", d, d) + EPS ** 2
        g -= G * M * d / s2[:, None] ** 1.5
        T += G * M * (np.eye(3)[None] / s2[:, None, None] ** 1.5 - 3 * np.einsum("ni,nj->nij", d, d) / s2[:, None, None] ** 2.5)
    return g, T


def nu(y):
    return 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-300)))


def phantom(X, r, a0, h=0.5):
    """QUMOND phantom density rho_ph = -div[(nu - 1) g_N]/(4 pi G) by central differences (Msun/kpc^3)."""
    div = np.zeros(X.shape[0])
    for k_ in range(3):
        e = np.zeros(3)
        e[k_] = h
        vals = []
        for sgn in (1, -1):
            gN, _ = g_and_T(X + sgn * e, r)
            y = np.linalg.norm(gN, axis=1) / a0
            vals.append(((nu(y) - 1)[:, None] * gN)[:, k_])
        div += (vals[0] - vals[1]) / (2 * h)
    return -div / (4 * math.pi * G)


def null_x(r):
    p1, p2 = mass_pos(r)
    # bracket away from the Plummer cores (run 1 bracketed from p + 1e-3 and found the trivial zero inside MW's core)
    return brentq(lambda xx: g_and_T(np.array([[xx, 0, 0]]), r)[0][0, 0], p1[0] + 3 * EPS, p2[0] - 3 * EPS)


# ================================================================ integrator
def integrate(Q, Gam2, r_of_t, ti, tf, s, field=None, n_eval=1201):
    """Return det(I+D) on a time grid (n_eval, N), positions at the grid, and times."""
    N = Q.shape[0]
    ri = r_of_t(ti)
    gi_fun = lambda X: g_and_T(X, ri)

    def rhs(t, y):
        Y = y.reshape(N, 24)
        X, V, D, Dd = Y[:, 0:3], Y[:, 3:6], Y[:, 6:15].reshape(N, 3, 3), Y[:, 15:24].reshape(N, 3, 3)
        if field is not None:
            dg, dT = field(X)
        else:
            rt = ri if MUTATE else r_of_t(t)
            g1, T1 = g_and_T(X, rt)
            g0, T0_ = gi_fun(X)
            dg, dT = g1 - g0, T1 - T0_
        acc = dg + s * Gam2[:, None] * (X - Q)
        Ddd = -np.einsum("nij,njk->nik", dT, np.eye(3)[None] + D) + s * Gam2[:, None, None] * D
        return np.concatenate([V, acc, Dd.reshape(N, 9), Ddd.reshape(N, 9)], axis=1).ravel()

    y0 = np.zeros((N, 24))
    y0[:, 0:3] = Q
    tt = np.linspace(ti, tf, n_eval)
    sol = solve_ivp(rhs, (ti, tf), y0.ravel(), t_eval=tt, rtol=1e-9, atol=1e-10, method="DOP853")
    Y = sol.y.T.reshape(len(sol.t), N, 24)
    dets = np.linalg.det(np.eye(3)[None, None] + Y[:, :, 6:15].reshape(len(sol.t), N, 3, 3))
    return sol.t, dets, Y[:, :, 0:3], sol


# ================================================================ C0 solver check
tau = 0.04
const_field = lambda X: (np.zeros_like(X), np.tile(tau * np.diag([1.0, 1.0, -2.0]), (X.shape[0], 1, 1)))
tt, dets, _, sol0 = integrate(np.zeros((1, 3)), np.zeros(1), lambda t: 0.0, 0.0, 9.0, 0, field=const_field, n_eval=9001)
# single-axis factor 1 + D_11 = cos(sqrt(tau) t); its zero is the crossing
Y = sol0.y.T.reshape(len(sol0.t), 1, 24)
f11 = 1 + Y[:, 0, 6]
iz = np.where(f11 <= 0)[0][0]
tz = tt[iz - 1] + (tt[iz] - tt[iz - 1]) * f11[iz - 1] / (f11[iz - 1] - f11[iz])
texact = math.pi / (2 * math.sqrt(tau))
y_end = sol0.y[:, -1]


def rhs_c(t, y):
    D = y[6:15].reshape(3, 3)
    Dd = y[15:24].reshape(3, 3)
    Ddd = -(tau * np.diag([1.0, 1.0, -2.0])) @ (np.eye(3) + D)
    return np.concatenate([y[3:6], np.zeros(3), Dd.ravel(), Ddd.ravel()])


back = solve_ivp(rhs_c, (9.0, 0.0), y_end, rtol=1e-12, atol=1e-13, method="DOP853")
rev = float(np.max(np.abs(back.y[:, -1])))
record("C0", abs(tz / texact - 1) < 1e-6 and rev < 1e-9,
       f"constant tidal field: 1 + D_11 = 0 at t = {tz:.9f} vs pi/(2 sqrt(tau)) = {texact:.9f}; time reversal {rev:.1e}")

# ================================================================ C2 + C3
results, c2_ok, min_by_case = {}, True, {}
xs_rel = np.arange(-400.0, 400.0 + 1e-9, 10.0)
zs = np.arange(0.0, 400.0 + 1e-9, 10.0)
for foot, a0 in A0.items():
    for oname, rfun in ORBITS.items():
        for ti in (3.0, 6.0, 9.0):
            ri = rfun(ti)
            xn = null_x(ri)
            Xg = np.array([[xn + dx, 0.0, z] for dx in xs_rel for z in zs])
            p1, p2 = mass_pos(ri)
            far = np.minimum(np.linalg.norm(Xg - p1, axis=1), np.linalg.norm(Xg - p2, axis=1)) > 2 * EPS
            Xg = Xg[far]
            rho = phantom(Xg, ri, a0)
            soft = rho < 0
            Q = Xg[soft]
            gN, _ = g_and_T(Q, ri)
            xq = nu(np.linalg.norm(gN, axis=1) / a0) * np.linalg.norm(gN, axis=1) / a0
            Gam2 = 4 * math.pi * G * np.abs(rho[soft]) * ((1 + xq) ** 2 - 1)
            inull = np.argmin(np.linalg.norm(Xg - np.array([xn, 0, 0]), axis=1))
            c2 = soft.sum() > 0 and rho[inull] < 0
            c2_ok &= bool(c2)
            for s in (0, 1):
                tf = t_ext[oname]
                tt, dets, XX, _ = integrate(Q, Gam2, rfun, ti, tf, s)
                mask_end = tt <= t_end[oname] + 1e-12
                det_min = float(dets[mask_end].min())
                crossed = dets <= 0
                key = f"{foot}|{oname}|t_i {ti}|s {s}"
                rec = {"n_soft": int(soft.sum()), "soft_extent_kpc": [float(Q[:, 0].min() - xn), float(Q[:, 0].max() - xn),
                                                                     float(Q[:, 2].max())],
                       "r_ti": ri, "Gamma_max_per_Gyr": float(np.sqrt(Gam2.max())), "det_min_to_t_end": det_min,
                       "det_min_to_r150": float(dets.min())}
                if crossed[mask_end].any():
                    it = np.where(crossed[mask_end].any(axis=1))[0][0]
                    tsc = float(tt[it])
                    j = int(np.where(crossed[it])[0][0])
                    pp1, pp2 = mass_pos(rfun(tsc) if not MUTATE else ri)
                    dist = float(min(np.linalg.norm(XX[it, j] - pp1), np.linalg.norm(XX[it, j] - pp2)))
                    rec.update({"t_sc": tsc, "t_sc_minus_t0": tsc - T0, "q_first": Q[j].tolist(),
                                "q_first_rel_null": [float(Q[j, 0] - xn), float(Q[j, 2])],
                                "dist_to_galaxy_kpc": dist,
                                "frac_crossed_by_t0": float(crossed[tt <= T0].any(axis=0).mean()) if (tt <= T0).any() else 0.0,
                                "frac_crossed_by_t_end": float(crossed[mask_end].any(axis=0).mean())})
                else:
                    rec.update({"t_sc": None})
                if crossed.any() and not crossed[mask_end].any():
                    it2 = np.where(crossed.any(axis=1))[0][0]
                    rec["t_sc_extended_r150"] = float(tt[it2])
                results[key] = rec
                print(f"   {key:52s} n_soft {rec['n_soft']:4d}  det_min(t_end) {det_min:+.4f}  t_sc "
                      f"{('%.3f' % rec['t_sc']) if rec['t_sc'] is not None else '  none'}"
                      + (f"  (t0{rec['t_sc_minus_t0']:+.2f} Gyr, {rec['dist_to_galaxy_kpc']:.0f} kpc from a galaxy, "
                         f"crossed by t0 {rec['frac_crossed_by_t0']:.3f}, by t_end {rec['frac_crossed_by_t_end']:.3f})"
                         if rec['t_sc'] is not None else "")
                      + f"  [to r=150: det_min {rec['det_min_to_r150']:+.3f}]")
record("C2", c2_ok, "soft region non-empty and containing the axis null at every t_i, orbit and footing")
out["C3"] = results

# reading
cases = {}
for k_, v in results.items():
    base = k_.rsplit("|s ", 1)[0]
    cases.setdefault(base, {})[k_.rsplit("|s ", 1)[1]] = v
both_cross = [b for b, d in cases.items() if all(d[s_]["t_sc"] is not None for s_ in ("0", "1"))]
all_safe = all(v["det_min_to_t_end"] > 0.5 for v in results.values())
if MUTATE:
    mut_ok = all(v["det_min_to_t_end"] >= 0.999 for k_, v in results.items() if k_.endswith("|s 0"))
    record("MUT", mut_ok, f"static masses: min det over s = 0 cases {min(v['det_min_to_t_end'] for k_, v in results.items() if k_.endswith('|s 0')):.6f}"
                          f"; s = 1 {min(v['det_min_to_t_end'] for k_, v in results.items() if k_.endswith('|s 1')):.6f}")
    reading = "MUTATE"
elif both_cross:
    earliest = min(both_cross, key=lambda b: max(cases[b][s_]["t_sc"] for s_ in ("0", "1")))
    reading = "SHELL-CROSSES"
    e0, e1 = cases[earliest]["0"], cases[earliest]["1"]
    record("C3", True, f"SHELL-CROSSES in {len(both_cross)}/{len(cases)} cases (both self-term brackets); earliest {earliest}: "
                       f"t_sc {e0['t_sc']:.3f} (s 0) / {e1['t_sc']:.3f} (s 1) Gyr = t0 {e0['t_sc_minus_t0']:+.2f} / "
                       f"{e1['t_sc_minus_t0']:+.2f} Gyr; first element at (dx, z) = {e0['q_first_rel_null']} kpc from the "
                       f"null, {e0['dist_to_galaxy_kpc']:.0f} kpc from a galaxy at t_sc")
elif all_safe:
    reading = "NO SHELL CROSSING"
    record("C3", True, f"NO SHELL CROSSING: min det over all {len(results)} runs = {min(v['det_min_to_t_end'] for v in results.values()):.4f} > 0.5")
else:
    reading = "UNDECIDED"
    und = [k_ for k_, v in results.items() if v["det_min_to_t_end"] <= 0.5]
    record("C3", True, f"UNDECIDED: {len(und)} runs with min det <= 0.5 but no case crosses in both brackets: {und[:6]}")
out["reading"] = reading
out["both_bracket_crossing_cases"] = both_cross
npass = sum(c["pass"] for c in checks)
out["checks"] = checks
out["summary"] = f"{npass}/{len(checks)} PASS; reading {reading}"
print(out["summary"])
(HERE / ("caustics_results_MUTATE.json" if MUTATE else "caustics_results.json")).write_text(json.dumps(out, indent=1, default=str))
sys.exit(0 if npass == len(checks) else 1)
