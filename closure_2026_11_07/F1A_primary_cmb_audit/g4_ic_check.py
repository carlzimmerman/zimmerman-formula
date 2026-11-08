#!/usr/bin/env python3
"""F1A amendment A2 check (after the result; prompted by CMB2 cd1c7c35a3): does G4 depend on the starting a_i, and does
its starting state satisfy the comoving Poisson constraint k^2 phi = -(3/2) Hc^2 sum (rho_i/rho) Delta_i,
Delta_i = delta_i + 3 Hc (1+w_i) theta_i / k^2 ?  Same equations as f1a.g4; the IC is either F1A's
(delta_i = -1.5 (1+w_i) phi) or the consistent one (delta_i = (1+w_i)(-1.5 - 0.5 (k tau)^2) phi, from the 00 equation).
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
f = json.load(open(os.path.join(HERE, "parts/fit_B2_canonical_cold.json")))["pars"]
OMR = 2.4728e-5 * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
h = f["h"]; H0 = h / 2997.92458; Ob, Od, Or = f["ob"] / h ** 2, f["oc"] / h ** 2, OMR / h ** 2
def run(k, fl, ai, ic, zend=1100.0):
    names = list(fl); ODE = 1 - sum(v[0] for v in fl.values())
    rho = lambda a: np.array([fl[n][0] * a ** (-3 * (1 + fl[n][1])) for n in names])
    def Hc(a): return a * H0 * math.sqrt(rho(a).sum() + ODE)
    def rhs(x, y):
        a = math.exp(x); rr = rho(a); tot = rr.sum() + ODE; H = Hc(a); phi = y[0]; d = y[1::2]; th = y[2::2]
        dphi = -H * phi + 1.5 * H ** 2 / k ** 2 * sum(rr[i] / tot * (1 + fl[n][1]) * th[i] for i, n in enumerate(names))
        out = [dphi]
        for i, n in enumerate(names):
            w, cs2 = fl[n][1], fl[n][2]
            out += [-(1 + w) * (th[i] - 3 * dphi) - 3 * H * (cs2 - w) * d[i] - 9 * H ** 2 * (1 + w) * (cs2 - w) * th[i] / k ** 2,
                    -H * (1 - 3 * cs2) * th[i] + cs2 * k ** 2 * d[i] / (1 + w) + k ** 2 * phi]
        return np.array(out) / H
    tau = ai / (H0 * math.sqrt(Or)); x2 = (k * tau) ** 2; y0 = [1.0]
    for n in names:
        w = fl[n][1]; d0 = -1.5 * (1 + w) if ic == "F1A" else (1 + w) * (-1.5 - 0.5 * x2)
        y0 += [d0, 0.5 * k ** 2 * tau]
    a = ai; rr = rho(a); tot = rr.sum() + ODE; H = Hc(a)
    Dtot = sum(rr[i] / tot * (y0[1 + 2 * i] + 3 * H * (1 + fl[n][1]) * y0[2 + 2 * i] / k ** 2) for i, n in enumerate(names))
    poisson = (k ** 2 * 1.0 + 1.5 * H ** 2 * Dtot) / k ** 2          # 0 if satisfied (relative to k^2 phi)
    s = solve_ivp(rhs, (math.log(ai), math.log(1 / (1 + zend))), y0, method="LSODA", rtol=1e-8, atol=1e-13)
    y = s.y[:, -1]; return {n: float(y[1 + 2 * i]) for i, n in enumerate(names)}, float(y[0]), poisson
rows = []
for k in (0.02, 0.05, 0.1, 0.2, 0.3):
    for ic in ("F1A", "consistent"):
        for ai in (1e-7, 1e-6, 1e-5):
            ref, phi, pr = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "d": (Od, 0, 0)}, ai, ic)
            x2r, _, _ = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "X": (Od, 0.0, 1.0)}, ai, ic)
            x1r, _, _ = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "d": (Od, 0, 0), "X": (1 - Ob - Od - Or, -0.95, 1.0)}, ai, ic)
            Q2 = abs(Od * 1101 ** 3 * x2r["X"]) / abs(Od * 1101 ** 3 * ref["d"])
            Q1 = abs((1 - Ob - Od - Or) * 1101 ** (3 * 0.05) * x1r["X"]) / abs(Od * 1101 ** 3 * ref["d"])
            rows.append(dict(k=k, ic=ic, ai=ai, poisson_resid=pr, delta_dust=ref["d"], delta_b=ref["b"], phi=phi, Q_X1=Q1, Q_X2=Q2))
            print(json.dumps(rows[-1]), flush=True)
json.dump(dict(rows=rows, note="kappa = 1/2 FITTED; not theory closed"), open(os.path.join(HERE, "g4_ic_check.json"), "w"), indent=1)
