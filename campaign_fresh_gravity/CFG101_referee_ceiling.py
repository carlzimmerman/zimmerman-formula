#!/usr/bin/env python3
"""CFG101 referee: an analytic re-derivation, with the referee's own code, of CFG101's two corrections to CFG50 (the tidal-tensor closure):
the ghost-free force ceiling (0.5008 g_tot, not 0.505) and the radius inside which the reaction on the baryons opposes the fluid force
(1.78 h, not 1.7 h).  Nothing from CFG44 / CFG50 / CFG101 is imported; the formulas are CFG50's README / D2 definitions:
  baryons   exponential sphere rho_b = M e^{-x} / (8 pi h^3), x = r/h
  target    rho_c = a0 u_N / (4 pi G r u) (CFG44's closure), g_tot = u / r^2; Jeans stress P_rr = rho_c r g_tot / 2, P_perp = (1 - beta) P_rr,
            beta = -(3/2) rho_b / rhobar_b(<r)
  tidal     T_rr = 2 g_N / r, T_perp = 4 pi G rho_b - g_N / r;  ghost boundary chi_c = 1 / lambda_max(T)
  forces    a_f = (1/2 rho_c) (T_rr' P_rr + 2 T_perp' P_perp) per unit chi;  a_react = 8 pi G [F_perp' + (F_perp - F_rr)/r], F = chi Pi / 2
Two exact reductions make both results functions of x alone (so mass- and a0-independent): P_rr = a0 g_N / (8 pi G) (u cancels), and
  |chi_c a_f| / g_tot = (r / 4) |T_rr' + 2 (1 - beta) T_perp'| / lambda_max.   Units below: G = M = h = 1.
Run: python3 campaign_fresh_gravity/CFG101_referee_ceiling.py
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

print(__doc__.split("Run:")[0].strip() + "\n")


def menc(x):
    x = np.asarray(x, float)
    return np.where(x < 1e-3, x ** 3 / 6 - x ** 4 / 8 + x ** 5 / 20 - x ** 6 / 72, -np.expm1(-x) - np.exp(-x) * (x + x * x / 2))


gN = lambda x: menc(x) / x ** 2
Trr = lambda x: 2 * menc(x) / x ** 3
Tp = lambda x: np.exp(-x) / 2 - menc(x) / x ** 3
beta = lambda x: -(x ** 3 * np.exp(-x)) / (4 * menc(x))
dTrr = lambda x: np.exp(-x) / x - 6 * menc(x) / x ** 4                              # M' = x^2 e^{-x} / 2
dTp = lambda x: -np.exp(-x) / 2 - np.exp(-x) / (2 * x) + 3 * menc(x) / x ** 4
LMAX = 1.0 / 3.0                                                                    # (8 pi / 3) G rho_b(0) = G M / (3 h^3)

xs = np.geomspace(1e-4, 50, 200001)
print(f"lambda_max: analytic 1/3; numeric max of (T_rr, T_perp) on [1e-4, 50] h: {max(Trr(xs).max(), Tp(xs).max()):.7f} (reached as x -> 0)")
frac = lambda x: (x / 4) * np.abs(dTrr(x) + 2 * (1 - beta(x)) * dTp(x)) / LMAX
res = minimize_scalar(lambda x: -frac(x), bounds=(0.3, 5.0), method="bounded", options=dict(xatol=1e-10))
print(f"ghost-free ceiling max |a_f| / g_tot on [0.3, 5] h: {-res.fun:.5f} at r = {res.x:.4f} h;  at 0.3 h {frac(0.3):.4f}, 1 h {frac(1.0):.4f}, 3 h {frac(3.0):.4f}"
      "   [CFG101: 0.5008 at 0.85 h; 0.337, 0.494, 0.143.  CFG50: 0.505; 0.34, -, 0.14]")
lg = max(Trr(0.01), Tp(0.01))
print(f"lambda_max read from a grid starting at 0.01 h: {lg:.6f} ({3 * lg - 1:+.3%}); the ceiling it implies: {-res.fun * LMAX / lg:.5f}   [CFG50's D2 grid starts at 0.01 h]")


def react(x, e=1e-6):                                                               # a_react per unit chi, up to the positive factor a0 / 2
    pp = lambda y: (1 - beta(y)) * gN(y)
    return (pp(x + e) - pp(x - e)) / (2 * e) + (pp(x) - gN(x)) / x


force = lambda x: dTrr(x) + 2 * (1 - beta(x)) * dTp(x)                             # sign of a_f per unit chi (times r g_tot / 4 > 0)
xx = np.linspace(0.05, 6.0, 5901)
s = np.sign(react(xx) * force(xx))
ch = np.where(np.diff(s) != 0)[0]
roots = []
for i in ch:
    lo, hi = xx[i], xx[i + 1]
    fz = react if np.sign(react(lo)) != np.sign(react(hi)) else force
    roots.append((brentq(fz, lo, hi, xtol=1e-12), "a_react = 0" if fz is react else "a_f = 0"))
print(f"a_react x a_f on [0.05, 6] h: negative (opposed) for r < {roots[0][0]:.4f} h ({roots[0][1]}), positive beyond; sign changes found: {len(roots)}"
      "   [CFG101: flips at 1.78 h, mass-independent.  CFG50: 'inside r < 1.7 h']")
