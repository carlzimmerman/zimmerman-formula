#!/usr/bin/env python3
"""CFG152 S: the secondary row, "0 of 2624 shell cases survive 10 Gyr" (CFG124 G1.2), point-mass half only.

Frozen criteria: ../CFG152_FROZEN_CRITERIA.md (sha256 printed first).  Modes: MUTATE unset (main), s, 1
(for this script, 1 = s: the other parts of MUTATE=1 do not apply here).
S0: the mimetic constraint alone makes the flow geodesic (sympy, general 2-D metric).
S : shells start at rest on the CFG44 point-mass target; class A = geodesic = Newtonian radial free fall;
    before any crossing each shell encloses M_b sqrt(1 + x0^2); t_fall = (pi/2) sqrt(r0^3 / (2 G M_enc)).
"""
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

import cfg152_common as C

NAME = "cfg152_S_shells"
mode = C.get_mode(["main", "s", "1"])
support = mode in ("s", "1")
rep = C.Report(NAME, mode)
C.header(rep)
R = rep.results

GM_SUN = 1.32712440018e20     # m^3 s^-2
GYR = 3.15576e16              # s
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # m s^-2 (both footings)
MASSES = [1e9, 1e10, 1e11, 1e12]                    # Msun
XG = np.logspace(np.log10(0.3), np.log10(30.0), 200)
T_H = 10.0 * GYR
rep.p(f"hydrostatic support (MUTATE=s): {support}")

# ------------------------------------------------------------------ S0: geodesic identity
rep.p("\n== S0: u^nu nabla_nu u_mu = (1/2) d_mu X for u_mu = d_mu phi, general (t, x)-dependent 2-D metric")
tt, xx = sp.symbols("t x", real=True)
g00, g01, g11, ph = (sp.Function(n)(tt, xx) for n in ("g00", "g01", "g11", "phi"))
g = sp.Matrix([[g00, g01], [g01, g11]])
gi = g.inv()
co = (tt, xx)
Gam = [[[sum(gi[r, s] * (sp.diff(g[s, n], co[m]) + sp.diff(g[s, m], co[n]) - sp.diff(g[m, n], co[s]))
             for s in range(2)) / 2 for n in range(2)] for m in range(2)] for r in range(2)]
u = [sp.diff(ph, c_) for c_ in co]
uu = [sum(gi[m, n] * u[n] for n in range(2)) for m in range(2)]
X = sum(uu[m] * u[m] for m in range(2))
acc = [sum(uu[n] * (sp.diff(u[m], co[n]) - sum(Gam[r][n][m] * u[r] for r in range(2))) for n in range(2))
       for m in range(2)]
s0 = [sp.simplify(acc[m] - sp.diff(X, co[m]) / 2) for m in range(2)]
rep.check("S0: u^nu nabla_nu u_mu - (1/2) d_mu X = 0 identically (so the flow is geodesic on X = -1, any V, gamma)",
          all(v == 0 for v in s0), s0, kind="identity")

# ------------------------------------------------------------------ S: fall times
rep.p("\n== S: shells released from rest on the point-mass target, x0 in [0.3, 30] (200 log points)")


def setup(x0, Mb, a0):
    GM = GM_SUN * Mb
    rM = np.sqrt(GM / a0)
    r0 = x0 * rM
    GMenc = GM * np.sqrt(1.0 + x0**2)          # M_b + M_c(<r0) = M_b sqrt(1 + x0^2)
    return r0, GMenc


def t_fall_analytic(x0, Mb, a0):
    r0, GMenc = setup(x0, Mb, a0)
    return 0.5 * np.pi * np.sqrt(r0**3 / (2.0 * GMenc))


def t_fall_ode(x0, Mb, a0, with_support):
    r0, GMenc = setup(x0, Mb, a0)
    tff = 0.5 * np.pi * np.sqrt(r0**3 / (2.0 * GMenc))

    # dimensionless: r = r0 q, t = tff s
    kappa_ = GMenc * tff**2 / r0**3

    def rhs(s, yv):
        q, v = yv
        acc_ = -kappa_ / q**2
        if with_support:
            acc_ += kappa_ / q**2               # the target's own hydrostatic support: net force zero
        return [v, acc_]

    def ev(s, yv):
        return yv[0] - 1e-6
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs, (0.0, T_H / tff), [1.0, 0.0], method="DOP853", rtol=1e-10, atol=1e-14, events=ev)
    return sol.t_events[0][0] * tff if sol.t_events[0].size else np.inf


rows, n_surv, mono_ok, ode_ok, ode_maxerr, n_cases = [], 0, True, True, 0.0, 0
tf_all = {}
for fname, a0 in A0.items():
    for Mb in MASSES:
        if support:
            tf = np.array([t_fall_ode(x0, Mb, a0, True) for x0 in XG])
        else:
            tf = np.array([t_fall_analytic(x0, Mb, a0) for x0 in XG])
            mono_ok &= bool(np.all(np.diff(tf) > 0))
            for x0 in XG[::20]:
                ta, to = t_fall_analytic(x0, Mb, a0), t_fall_ode(x0, Mb, a0, False)
                err = abs(to / ta - 1)
                ode_maxerr = max(ode_maxerr, err)
                ode_ok &= err < 1e-6
        tf_all[(fname, Mb)] = tf
        surv = int(np.sum(tf >= T_H))
        n_surv += surv
        n_cases += len(XG)
        rows.append({"footing": fname, "M_b": Mb, "tfall_min_Gyr": float(np.min(tf) / GYR),
                     "tfall_max_Gyr": float(np.max(tf) / GYR), "survivors": surv})
        rep.p(f"   {fname:9s} M_b = {Mb:.0e}: t_fall in [{np.min(tf) / GYR:.4g}, {np.max(tf) / GYR:.4g}] Gyr, "
              f"cases with t_fall >= 10 Gyr: {surv} of {len(XG)}")
R["rows"] = rows
if not support:
    rep.check("S: t_fall rises with x0 on the grid (inner shells reach the centre first)", mono_ok, kind="method check")
    rep.check("S: analytic t_fall agrees with the integrated radial ODE to 1e-6 (every 20th x0)", ode_ok,
              f"max rel err {ode_maxerr:.2e}", kind="method check")
rep.check(f"S pass line: number of cases with t_fall >= 10 Gyr is 0 (of {n_cases})", n_surv == 0,
          f"{n_surv} of {n_cases} survive", kind="pass line")
R["n_cases"], R["n_survive"] = n_cases, n_surv

# reported rows: range per footing against the printed 0.003-3.7 Gyr
for fname in A0:
    lo = min(np.min(tf_all[(fname, Mb)]) for Mb in MASSES) / GYR
    hi = max(np.max(tf_all[(fname, Mb)]) for Mb in MASSES) / GYR
    rep.p(f"   reported: {fname}: t_fall range {lo:.4g} - {hi:.4g} Gyr")
lo = min(np.min(v) for v in tf_all.values()) / GYR
hi = max(np.max(v) for v in tf_all.values()) / GYR
agree = (0.0025 <= lo < 0.0035) and (3.65 <= hi < 3.75)
rep.p(f"   reported: overall t_fall range {lo:.4g} - {hi:.4g} Gyr; printed CFG124 range 0.003-3.7 Gyr; "
      f"agrees at the printed precision (min in [0.0025, 0.0035), max in [3.65, 3.75)): {agree}")
R["range_overall_Gyr"] = [lo, hi]
R["range_agrees_printed"] = bool(agree)

rc = rep.finish()
sys.exit(rc)
