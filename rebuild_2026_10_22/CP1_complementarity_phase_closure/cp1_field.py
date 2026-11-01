#!/usr/bin/env python3
"""CP1 note (a): the earlier proposed field equation at chi_pol = 1, spherical symmetry. div[(1 + chi/sqrt(1 + |grad Phi|^2/a0^2)) grad Phi] = 4 pi G rho_b. Gauss gives (1 + chi/sqrt(1 + g^2/a0^2)) g = g_b. Solved by root; then the divergence is checked by finite volume on a Plummer sphere. kappa = 1/2 FITTED; not theory closed."""
import json, math, os
import numpy as np
from scipy.optimize import brentq
a0 = 9.3603e-11; G = 6.6743e-11; O = {}
def solve(gb, chi=1.0): return brentq(lambda g: (1 + chi / math.sqrt(1 + (g / a0) ** 2)) * g - gb, 0, gb * 1.0000001, xtol=1e-30, rtol=1e-14)
print("g_b/a0, g/a0, g/(g_b/2), g/(g_b - a0), g/sqrt(g_b a0), law g/a0")
rows = []
for x in (1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4):
    gb = x * a0; g = solve(gb); law = gb * (0.5 + math.sqrt(0.25 + a0 / gb)); rows.append(dict(x=x, g=g / a0, half=g / (gb / 2), minus=g / (gb - a0) if x > 1 else None, deep=g / math.sqrt(gb * a0), law=law / a0)); print(f"{x:g}, {g / a0:.6g}, {g / (gb / 2):.6f}, {(g / (gb - a0)) if x > 1 else float('nan'):.6f}, {g / math.sqrt(gb * a0):.4f}, {law / a0:.6g}")
M = 1e41; b = 3e19; r = np.geomspace(1e18, 1e23, 8001); rho = 3 * M * b ** 2 / (4 * math.pi) / (r ** 2 + b ** 2) ** 2.5; gb = G * M * r ** 3 / (r ** 2 + b ** 2) ** 1.5 / r ** 2; g = np.array([solve(x) for x in gb]); fl = (1 + 1 / np.sqrt(1 + (g / a0) ** 2)) * g; dv = np.gradient(r ** 2 * fl, r) / r ** 2; res = np.abs(dv / (4 * math.pi * G * rho) - 1)[5:-5]; sel = rho[5:-5] > 1e-6 * rho[0]
O = dict(rows=rows, plummer_residual_max=float(res[sel].max()), low_half_limit=rows[0]["half"], high_minus_limit=rows[-1]["minus"], deep_ratio_at_1e_4=rows[0]["deep"])
print(f"Plummer finite-volume residual, |div F/(4 pi G rho) - 1| max {O['plummer_residual_max']:.1e}")
p = solve(1e-4 * a0, 0.0) / (1e-4 * a0); print(f"K chi 0 gives g = g_b: {p:.8f}"); O["chi0"] = p
json.dump(O, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cp1_field.json"), "w"), indent=1)
