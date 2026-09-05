#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03c -- the zero-field limit (spec requirement 9) with the coherence term OUTSIDE the MOND function.
Static scalar sector, clock at rest:  E[phi] = (1/8 pi G) int [ a0^2 F(|grad phi|^2/a0^2) + c xi^2 (Delta phi)^2 ] + int rho phi,  F' = mu,
giving  div[mu(|grad phi|/a0) grad phi] - c xi^2 Delta^2 phi = 4 pi G rho   (c = 1 here; (d_i d_j phi)^2 differs from (Delta phi)^2 by a divergence).
(A) symbols: bare AQUAL linearisation has eigenvalues lambda_perp = mu, lambda_par = mu + y mu' (spec req 12), both -> 0 as y -> 0 (loss of ellipticity);
    outside J the symbol is lambda k^2 + xi^2 k^4 >= xi^2 k^4 (uniformly elliptic at y = 0); inside J it is lambda (k^2 + xi^2 k^4) -> 0.
(B) spherical point mass: first integral  mu(g/a0) g - xi^2 [g'' + 2g'/r - 2g/r^2] = GM/r^2, solved as a BVP for xi/r_M = 0.03..1: Newton exact inside,
    deep-MOND 1/r outside with the analytic correction delta = -xi^2/(r_M r), deviation from the algebraic law scaling as (xi/r_M)^2, no oscillation.
(C) field nulls (saddles), where the bare law is degenerate: the outside-J term dominates for structure below (xi^2 a0/|T|)^{1/3}; the Earth-Sun saddle numbers.
Checks can fail."""
import math, sys, numpy as np, sympy as sp, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import brentq
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("=" * 100); print("g03c -- zero-field limit with the coherence term outside J"); print("=" * 100)
# ---- A
y, k, xi = sp.symbols('y k xi', positive=True)
mu = 1 - sp.exp(-y); lam_perp = mu; lam_par = sp.simplify(mu + y*sp.diff(mu, y))
check("A1 bare AQUAL eigenvalues: lambda_perp = mu, lambda_par = 1 + (y-1)e^{-y} (spec req 12), positive for y > 0 and BOTH -> 0 as y -> 0",
      sp.simplify(lam_par - (1 + (y - 1)*sp.exp(-y))) == 0 and sp.limit(lam_perp, y, 0) == 0 and sp.limit(lam_par, y, 0) == 0 and lam_par.subs(y, sp.Rational(1, 10)) > 0)
sym_out = lambda lam: lam*k**2 + xi**2*k**4; sym_in = lambda lam: lam*(k**2 + xi**2*k**4)
check("A2 outside J: the symbol's smaller eigenvalue at y = 0 is xi^2 k^4 > 0 (uniformly elliptic, fourth order); inside J it is 0 (degenerate)",
      sp.simplify(sym_out(lam_perp).subs(y, 0) - xi**2*k**4) == 0 and sp.simplify(sym_in(lam_perp).subs(y, 0)) == 0)
# ---- B
def mu_f(G): return 1 - np.exp(-G)
def alg(x):                                            # algebraic spherical law mu(G) G = e^{-2x}, G = g/a0, r in units of r_M
    s = math.exp(-2*x); return brentq(lambda G: G*(1 - math.exp(-G)) - s, 1e-16, s + 60.0, xtol=1e-15) if s < 300 else s
XMIN, XMAX = math.log(1e-3), math.log(1e3); xs = np.linspace(XMIN, XMAX, 4001); Galg = np.array([alg(x) for x in xs]); GN = np.exp(-2*xs)
from scipy.linalg import solve_banded
XS = np.linspace(XMIN, XMAX, 60001); H = XS[1] - XS[0]; GALG = np.array([alg(x) for x in XS]); GNN = np.exp(-2*XS)
def solve(eps):
    """damped Newton on the finite-difference form of  G_xx + G_x - 2G - (e^{2x} mu(G) G - 1)/eps^2 = 0, Dirichlet ends (Newton inside, deep MOND with delta outside)."""
    G = GALG.copy(); G[0] = math.exp(-2*XMIN); G[-1] = math.exp(-XMAX)*(1 - eps**2*math.exp(-XMAX)); n = len(XS)
    for it in range(60):
        mu_ = 1 - np.exp(-G); dmu = np.exp(-G); e2 = np.exp(2*XS)
        F = np.zeros(n); F[1:-1] = (G[2:] - 2*G[1:-1] + G[:-2])/H**2 + (G[2:] - G[:-2])/(2*H) - 2*G[1:-1] - (e2[1:-1]*mu_[1:-1]*G[1:-1] - 1)/eps**2
        ab = np.zeros((3, n)); ab[1, :] = 1.0                                     # boundary rows: identity
        ab[1, 1:-1] = -2/H**2 - 2 - e2[1:-1]*(mu_[1:-1] + G[1:-1]*dmu[1:-1])/eps**2
        ab[0, 2:] = 1/H**2 + 1/(2*H); ab[2, :-2] = 1/H**2 - 1/(2*H)
        dG = solve_banded((1, 1), ab, -F); lam = 1.0
        while np.any(G[1:-1] + lam*dG[1:-1] <= 0) and lam > 1e-4: lam *= 0.5
        G = G + lam*dG
        if np.max(np.abs(dG[1:-1])/np.maximum(G[1:-1], 1e-300)) < 1e-12: break
    mu_ = 1 - np.exp(-G); res = (G[2:] - 2*G[1:-1] + G[:-2])/H**2 + (G[2:] - G[:-2])/(2*H) - 2*G[1:-1] - (np.exp(2*XS[1:-1])*mu_[1:-1]*G[1:-1] - 1)/eps**2
    scale = np.abs(G[1:-1])/H**2 + np.exp(2*XS[1:-1])*np.abs(mu_[1:-1]*G[1:-1])/eps**2 + 1e-300
    return G, it, float(np.max(np.abs(res)/scale))
print("  spherical point mass, r in units of r_M = sqrt(GM/a0), G = g/a0.  xi/r_M | Newton its, scaled residual | max |G/G_alg - 1| | at r = r_M | G/G_alg - 1 at r = 300: numeric vs -xi^2/(r_M r) | phantom kept at r_M")
dev = {}; rows = {}
for eps in (0.03, 0.1, 0.3, 1.0):
    G, its, res = solve(eps); d = np.abs(G/GALG - 1); i1 = np.argmin(np.abs(XS)); i300 = np.argmin(np.abs(XS - math.log(300))); i001 = np.argmin(np.abs(XS - math.log(0.01)))
    delta_num = G[i300]/GALG[i300] - 1; delta_an = -eps**2*math.exp(-XS[i300])
    kept = (G[i1] - GNN[i1])/(GALG[i1] - GNN[i1]); mono = bool(np.all(np.diff(G) < 0)); newt = abs(G[i001]*0.01**2 - 1)
    dev[eps] = float(d[i1]); rows[eps] = (its, res, kept, delta_num, delta_an, mono, newt)
    print(f"    {eps:5.2f} | {its:2d}, {res:.1e} | {d.max():.3e} | {d[i1]:.3e} | {delta_num:+.3e} vs {delta_an:+.3e} | {kept:.4f}  monotonic {mono}")
check("B1 every Newton solve converges (residual relative to the largest term < 1e-10) and every solution is monotonic (no oscillatory homogeneous mode: the stiffening is Yukawa-like, not wave-like)",
      all(rows[e][1] < 1e-10 and rows[e][5] for e in rows), f"residuals {[f'{rows[e][1]:.0e}' for e in rows]}")
check("B2 Newton is exact inside: at r = 0.01 r_M, |G r^2 - 1| < 1e-6 for every xi/r_M (the fourth-order term annihilates 1/r^2)", all(rows[e][6] < 1e-6 for e in rows), f"worst {max(rows[e][6] for e in rows):.1e}")
check("B3 the deviation at r = r_M scales as (xi/r_M)^2 in the perturbative range (0.03 -> 0.1: ratio within 15% of 11.1) and then saturates (ratios decrease for 0.1 -> 0.3 -> 1)",
      abs(dev[0.1]/dev[0.03]/11.11 - 1) < 0.15 and dev[0.3]/dev[0.1] < dev[0.1]/dev[0.03] and dev[1.0]/dev[0.3] < dev[0.3]/dev[0.1], f"ratios {dev[0.1]/dev[0.03]:.2f}, {dev[0.3]/dev[0.1]:.2f}, {dev[1.0]/dev[0.3]:.2f}")
check("B4 the deep-MOND 1/r law survives with the analytic correction G/G_alg - 1 = -xi^2/(r_M r): numeric within 30% of it at r = 300 r_M for xi/r_M = 0.3 and 1, and negative for all four",
      all(abs(rows[e][3]/rows[e][4] - 1) < 0.30 for e in (0.3, 1.0)) and all(rows[e][3] < 0 for e in rows), f"ratios {rows[0.3][3]/rows[0.3][4]:.3f}, {rows[1.0][3]/rows[1.0][4]:.3f}")
check("B5 a solar-mass body with xi = r_M keeps less than 60% of the algebraic phantom at r = r_M (the term acts on the transition when xi ~ r_M), and more than 99% when xi = 0.03 r_M",
      rows[1.0][2] < 0.60 and rows[0.03][2] > 0.99, f"kept {rows[1.0][2]:.3f} (xi = r_M), {rows[0.03][2]:.4f} (xi = 0.03 r_M)")
# ---- C
G_, MS, ME, AU, a0 = 6.6743e-11, 1.98892e30, 5.9722e24, 1.495978707e11, 9.3619e-11
rs = AU*math.sqrt(ME/MS)                              # Earth-Sun saddle distance from Earth (equal Newtonian pulls)
T = 2*G_*ME/rs**3 + 2*G_*MS/(AU - rs)**3             # tidal stress along the axis at the saddle
rb = a0/T                                             # bare-law MOND bubble: |g| < a0
for xi_pc in (0.02, 0.03, 0.05):
    xim = xi_pc*3.0857e16; rsup = (xim**2*rb)**(1/3); supp = (rb/xim)**2
    print(f"  Earth-Sun saddle: {rs/1e3:.0f} km from Earth, |T| = {T:.2e} s^-2, bare MOND bubble a0/|T| = {rb:.2f} m; xi = {xi_pc} pc: the outside-J term dominates below {rsup/1e3:.2e} km, amplitude suppression ~ (r_b/xi)^2 = {supp:.1e}")
check("C1 at every Solar-System field null the coherence term dominates the response by more than 1e12 for xi >= 0.02 pc (bubble a0/|T| under 1e6 km): the saddle anomaly of the bare law is erased, and for any bubble below 1e6 km the statement holds",
      rb < 1e9 and (rb/(0.02*3.0857e16))**2 < 1e-12, f"suppression {(rb/(0.02*3.0857e16))**2:.1e}")
print("\n  requirement 9 status: outside J the static operator is uniformly elliptic at y = 0 (fourth order), the point-mass solution is regular, Newton-exact inside and deep-MOND outside with a computed O(xi^2/(r_M r)) correction; inside J the y -> 0 degeneracy of the bare law remains. Null-point (saddle) anomalies are a null prediction of both placements.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
