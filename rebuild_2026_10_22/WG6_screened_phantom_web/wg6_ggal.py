#!/usr/bin/env python3
"""WG6 G-gal (FROZEN_CRITERIA.md 1a7c1cdde9): screened over unscreened radial force of an isolated deep-MOND phantom halo,
rho_ph = A / r^2 out to R_out = 10 Mpc, with the Yukawa screening applied by shells (scale-free: depends on mu r only).
Pass: ratio >= 0.89 (0.05 dex) at r = 0.1, 0.3, 1 Mpc; 3 Mpc reported. K11: mu -> 0 gives 1 to 1e-6 at r = 1 Mpc.
Run: python3 wg6_ggal.py. kappa = 1/2 FITTED; not theory closed."""
import os, json, math
import numpy as np
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); R_OUT = 10.0
def ratio(mu, r):
    if mu * r < 1e-6 and mu * R_OUT < 1e-6:
        mu = max(mu, 1e-9)
    inner = quad(lambda s: math.sinh(mu * s) / (mu * s) if mu * s > 1e-12 else 1.0, 0.0, r, limit=200)[0]
    outer = quad(lambda s: math.exp(-mu * s) / s, r, R_OUT, limit=200)[0]
    x = mu * r
    t_out = (x * math.cosh(x) - math.sinh(x)) / (mu * r * r) if x > 1e-4 else mu * r / 3.0
    return r * (math.exp(-x) * (1 + x) / r ** 2 * inner - t_out * outer)
OUT = []; RES = {}
k11 = abs(ratio(1e-9, 1.0) - 1.0); OUT.append(f"K11 Yukawa shells, mu -> 0 at r = 1 Mpc: |ratio - 1| = {k11:.2e} -> {'PASS' if k11 < 1e-6 else 'FAIL'}")
for mu in (0.01, 0.03, 0.1):
    rs = {r: ratio(mu, r) for r in (0.1, 0.3, 1.0, 3.0)}
    ok = all(rs[r] >= 0.89 for r in (0.1, 0.3, 1.0))
    RES[str(mu)] = dict(ratios={str(k): v for k, v in rs.items()}, pass_=ok)
    OUT.append(f"G-gal mu {mu}/Mpc: force ratio " + ", ".join(f"r {r:g} Mpc {v:.4f}" for r, v in rs.items()) + f" -> {'PASS' if ok else 'FAIL'}")
print("\n".join(OUT))
json.dump(dict(K11=dict(err=k11, pass_=k11 < 1e-6), G_gal=RES), open(os.path.join(HERE, "wg6_ggal.json"), "w"), indent=1)
open(os.path.join(HERE, "wg6_ggal.out"), "w").write("\n".join(OUT) + "\n")
