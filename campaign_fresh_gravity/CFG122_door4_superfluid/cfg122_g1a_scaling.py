#!/usr/bin/env python3
"""CFG122 G1.1a (symbolic): the gradient-dominated condensate density against the CFG44 target, point mass.
   rho_grad(r) = 2 m^2 Lam |grad phi|,  |grad phi|^2 = alpha M_b/(8 pi M_Pl r^2)   (sympy from the flux law, S0.1)
   rho_t(x)    = a0/(4 pi G r sqrt(1+x^2)),  x = r/r_M,  r_M = sqrt(G M/a0)
   ratio = rho_grad/rho_t = R0(M) sqrt(1+x^2),  R0 ∝ sqrt(M);  deep regime (x >> 1): ratio = r/r_*, r_* independent of M.
PASS (G1.1a) iff the spread of the ratio at fixed x across 1e9..1e12 is <= 10%.  Analytic value (1e3)^(1/2) = 31.6.
(No MUTATE here: the frozen MUTATE=a is exercised numerically in cfg122_g1_plane.py, where the target is replaced by rho_grad inside the full solver.)
Run: python3 cfg122_g1a_scaling.py"""
import os, sys, math
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *

MUT = os.environ.get("MUTATE", "")
R = Report("cfg122_g1a_scaling")
P, check = R.P, R.check
m, Lam, al, M, Mpl, G, a0, r, x = sp.symbols("m Lambda alpha M M_Pl G a0 r x", positive=True)
Gs = 1 / (8 * sp.pi * Mpl ** 2)
p_grad = sp.sqrt(al * M / (8 * sp.pi * Mpl)) / r
rho_grad = 2 * m ** 2 * Lam * p_grad
rM_ = sp.sqrt(G * M / a0)
rho_t = a0 / (4 * sp.pi * G * r * sp.sqrt(1 + (r / rM_) ** 2))
ratio = sp.simplify((rho_grad / rho_t))
P(f"  ratio rho_grad/rho_t = {ratio}")
R0 = sp.simplify(sp.limit(ratio.subs(r, x * rM_), x, 0))            # x -> 0 limit
ratio_x = sp.simplify(ratio.subs(r, x * rM_) / R0)
P(f"  R0(M) = ratio at x -> 0 = {sp.simplify(R0.subs(G, Gs))};   ratio/R0 = {ratio_x}")
scal = sp.simplify(sp.diff(sp.log(R0), M) * M)
P(f"  d ln R0/d ln M = {scal}   (so the ratio at fixed x scales as M^{scal})")
check("G1.1a-i  ratio(x, M) = R0(M) sqrt(1 + x^2) with R0 ∝ M^(1/2)  (sympy)", f"ratio/R0 = {ratio_x}; dlnR0/dlnM = {scal}", sp.simplify(ratio_x - sp.sqrt(1 + x ** 2)) == 0 and scal == sp.Rational(1, 2))
# deep regime: ratio = r/r_*, r_* independent of M
rstar = sp.simplify(1 / sp.limit((ratio / r), r, sp.oo))
P(f"  deep regime x >> 1: ratio -> r/r_*,  r_* = {sp.simplify(rstar.subs(G, Gs))}")
dep = sp.simplify(sp.diff(rstar, M))
check("G1.1a-ii  r_*(m, alpha) is independent of M_b (deep regime)", f"d r_*/dM = {dep}", dep == 0)
spread_M = (1e12 / 1e9) ** 0.5
spread_x = math.sqrt(1 + 30.0 ** 2) / math.sqrt(1 + 0.1 ** 2)
P(f"  spread of the ratio at fixed x across 1e9..1e12: {spread_M:.4g};  spread across x in [0.1, 30] at fixed M: {spread_x:.4g}   (the 10% line: 1.10)")
# numeric cross-check through the solver's algebra (Y = 0):
worst = 0.0
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    for (mm, aa) in ((1.0, 1.0), (0.01, 30.0)):
        Lm = float(lam_tie(mm, aa, a0n))
        for Mmsun in MASSES:
            Mv = Mmsun * MSUN_EV
            for xx in (0.1, 1.0, 10.0, 30.0):
                rr = xx * float(rM(Mv, a0n))
                Cc = mm * aa * Mv / (4 * math.pi * rr ** 2 * MPL); D = Cc * Cc / (16 * mm ** 4)
                X = float(solveX(np.array(0.0), np.array(D), "B-"))
                rho_num = mm * Lm * (2 * mm) ** 1.5 * math.sqrt(abs(X))
                rho_th = float(a0n / (4 * math.pi * G_N * rr * math.sqrt(1 + xx ** 2)))
                ratio_num = rho_num / rho_th
                Rfun = float((R0 * sp.sqrt(1 + x ** 2)).subs({m: mm, Lam: Lm, al: aa, M: Mv, Mpl: MPL, G: G_N, a0: a0n, x: xx}))
                worst = max(worst, abs(ratio_num / Rfun - 1))
check("G1.1a-iii  the closed form matches the solver's algebra (Y = 0) at 2 (m, alpha) x 4 masses x 4 x, both footings", f"worst relative deviation {worst:.2e}", worst < 1e-8)
ok = spread_M <= 1.10
check("G1.1a  the mass spread of rho_DM/rho_target at fixed x is <= 10%  [HEADLINE sub-check: the analytic spread is 31.6]", f"spread {spread_M:.4g} (x-spread at fixed M {spread_x:.4g})", ok, load_bearing=False)
R.num("G1.1a", dict(spread_mass=spread_M, spread_x=spread_x, R0_scaling=str(scal)))
R.verdict("G1.1a", "PASS" if ok else "FAIL", f"ratio spread across masses at fixed x = {spread_M:.4g} (1.10 line); across x in [0.1, 30] at fixed M = {spread_x:.4g}; the inner slope agrees with the target (both ∝ 1/r for x < 1), the outer does not (target ∝ 1/r^2)")
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
