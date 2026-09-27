#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR25 (3 of 4) -- DO THE CONSTANT-MEAN-CURVATURE LEAVES EXIST AROUND COMPACT OBJECTS?  Neutron stars (static and moving),
black holes (the limit surface r = 3M/2 = the universal horizon), the khronon inside black holes, the O(alpha_c) multiplier
at c_2 = oo, ringdown, and causality criterion B.

WHY.  FP14 replaced the leaf-averaged -c_2 (K - <K>_h)^2 by its c_2 -> oo limit, the multiplier -2 mu (K - <K>_h): the
khronon's leaves must be CMC hypersurfaces (K = <K>_h = 3H(tau) cosmologically, ~0 around any compact object).  FP14 showed
the limit regular on Minkowski and FRW (C1, C1b) and flagged 'the khronon's binary-pulsar radiation at lambda_BPS -> oo' as
open (F14k').  Around stars the leaves' existence is a regularity question for an elliptic equation; around black holes the
maximal slicing of Schwarzschild famously piles up on the limit surface r = 3M/2 (Estabrook et al. 1973), which in
khronometric gravity is a universal horizon (Barausse, Jacobson & Sotiriou 2011; Blas & Sibiryakov 2011; Berglund,
Bhattacharyya & Mattingly 2012).  In the chain alpha_c > 0 is REQUIRED (FP14 A2-A3) -- so the alpha = 0 literature
(mHG: Franchini, Herrero-Valea & Barausse 2021) does not settle it, and Ramos & Barausse 2019 found singular moving black
holes for generic couplings while Kovachik & Sibiryakov 2023/2025 found them regular in the decoupling limit.

CONVENTIONS.  Mostly plus, c = G = 1 in the symbolic parts (M the mass); ingoing Eddington-Finkelstein; the static aether
u^r = V, u_v = -U, U^2 - V^2 = f = 1 - 2M/r; xi = r_s/r (r_s = 2M) where Kovachik-Sibiryakov's (KS) variables are used.
Both a0 footings are irrelevant here (a0 does not enter the khronon sector; the MOND scalar is filtered on xi >= 0.024 pc,
>> any compact object) -- stated, not computed.

PRE-DECLARED HYPOTHESES (written before the first full run)
  H1  Around a static star the CMC foliation (K_0 = 3 H_0, and K_0 = 0) exists, is unique and regular: n^r = K_0 V(r)/(r^2
      e^{Phi + Lambda}); around a slowly moving star the O(v) perturbation of the maximal foliation obeys D_i(N^2 D^i psi) = 0 on
      the static slice, with a unique regular solution tending to the boost -- no horizon, no singular point.
  H2  Around a Schwarzschild black hole the stationary maximal foliation regular across the Killing horizon exists only for
      C = C_crit = 3 sqrt(3) M^2/4; its leaves asymptote to r = 3M/2, which is itself a K = 0 leaf and a universal horizon
      (u . chi = 0); the aether's acceleration is regular there; for C != C_crit the foliation is singular or exposes r = 0.
  H3  At alpha_c = 0 the slowly moving black hole is regular: the O(v) khronon obeys KS eq. (4.17), exponents -1 +- sqrt 2 at
      the universal horizon, the soft mode is the unique admissible one (KS 2023 Sec. 4.4; Ramos & Barausse 2019 Sec. VI).
  H4  (expected FAIL at first order) At alpha_c > 0 and c_2 = oo, strict first-order perturbation theory in alpha_c gives a
      multiplier mu that diverges logarithmically at the universal horizon and a stress trace ~ alpha_c/(r - 3M/2): the static
      black hole is singular there AT O(alpha_c); the expansion is non-uniform within Delta r ~ (3/4) sqrt(alpha_c) M, where
      the full theory's spin-0 horizon sits (c_s^2 = (2 - alpha_c)/(3 alpha_c), FP14) -- regularity beyond first order OPEN.
  H5  Outside the Killing horizon everything is Schwarzschild + O(alpha_c): ringdown shifts O(alpha_c) <~ 1e-8, unobservable.
  H6  Criterion B: the exterior has a global preferred time (the universal horizon is the leaf at tau = oo, reparametrizable),
      no signal runs backward in it; the region 3M/2 < r < 2M talks to the exterior through the fast khronon and the
      leafwise-instantaneous channels (allowed by B); nothing escapes from r < 3M/2.

CHECKS
  K1 CONTROL: the maximal slicing's limit surface (Estabrook et al. 1973): the double root of N^2 = 1 - 2M/r + C^2/r^4 at
     r = 3M/2, C = 3 sqrt 3 M^2/4; = KS's b = 3 sqrt 3/16, xi_* = 4/3.
  K2 CONTROL: the static khronon current derived here from the action reproduces KS 2023 eq. (3.12),
     J^r = F(xi)[alpha U''/U - c_2 (V''/V - 2/xi^2)] (decoupling limit, c_chi^2 = c_2/alpha), at random aether profiles.
  K3 CONTROL: the O(v) maximal condition on the C_crit foliation, derived here, is KS eq. (4.17) exactly; exponents at xi_*:
     -1 +- sqrt 2 (KS 4.18b), at xi = 0: -1, 2 (for Ramos-Barausse's delta = chi': -2 +- sqrt 2, their eqs. 70-71).
  K4 CONTROL: the horizon of a mode of speed c_s relative to the aether in the maximal foliation: r_h - 3M/2 = sqrt(3/8) M/c_s
     (the record's L33 C4-C5), reproduced.
  N1 static neutron stars (TOV, SLy-type): the CMC foliation with K_0 = 3 H_0 exists and is regular; the tilt at the surface.
  N2 moving neutron stars: the O(v) maximal perturbation D_i(N^2 D^i psi) = 0 solved: regular, unique, tends to the boost.
  B1 static black holes: C_crit, the universal horizon, its surface gravity, a^2 regular; C != C_crit singular; Kottler/CMC.
  B2 moving black holes at alpha_c = 0: the unique regular O(v) solution, the aether C^1 at the universal horizon; stealth.
  B3 alpha_c > 0, c_2 = oo, first order: the multiplier's log divergence (coefficient derived and checked numerically), the
     stress trace ~ mu-dot ~ alpha_c/(r - 3M/2); the non-uniformity layer.
  B4 ringdown (reported).   B5 criterion B and the universal horizon (reported).   W the ledger.
DISCLOSURE: the first MUTATE run (and a scratch exec of the first three sections, output deleted) showed two check-
implementation errors, now fixed: K4 compared the horizon offset with its leading term only, at double precision (FAILED at
c_s = 100 by the O(1/c_s) correction); N1 measured K by finite differences including the first grid points, where the
discretisation error is ~h^2/(3 r^2) (FAILED at 2e-2).  K3's tolerance was set to 1e-10 for float-evaluated ratios.  No
physics input changed.
MUTATE=1: the black-hole foliation is built with C = 0.98 C_crit (a near-critical but non-critical leaf family): B1's
regularity check must FAIL (the aether's acceleration diverges where N^2 has its first simple zero), rc = 1.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR25_cmc_compact_objects.py
"""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
import XR25_common as C

mp.mp.dps = 40
L = C.Lane("XR25_cmc_compact_objects", "XR25/cmc")
P, check, banner = L.P, L.check, L.banner
P(__doc__.split("CHECKS")[0].strip())
if L.mutate:
    P("\n  *** MUTATE=1: the black-hole foliation uses C = 0.98 C_crit: B1's regularity check must FAIL ***")
CFAC = 0.98 if L.mutate else 1.0

M_, r_, rs_ = sp.symbols("M r r_s", positive=True)
Cc_ = sp.Symbol("C", positive=True)
xi_ = sp.Symbol("xi", positive=True)

# ================================================================================================ K1 Estabrook / KS background
banner("K1  CONTROL: the maximal slicing's limit surface (Estabrook et al. 1973) = KS's c_chi = oo background")
N2 = 1 - 2 * M_ / r_ + Cc_ ** 2 / r_ ** 4
sol = sp.solve([sp.numer(sp.together(N2)), sp.diff(sp.numer(sp.together(N2)), r_)], [r_, Cc_], dict=True)
sol = [s_ for s_ in sol if s_[r_].is_positive and s_[Cc_].is_positive]
rUH, Ccrit = sol[0][r_], sol[0][Cc_]
b_ks = sp.simplify(Ccrit / (2 * M_) ** 2)
xi_star = sp.simplify(2 * M_ / rUH)
P(f"    double root: r = {rUH}, C = {Ccrit};  KS variables: b = C/r_s^2 = {b_ks}, xi_* = r_s/r_UH = {xi_star}")
check("K1 CONTROL: the stationary maximal foliation u^r = -C/r^2 has N^2 = 1 - 2M/r + C^2/r^4 with a double root exactly at "
      "r = 3M/2 for C = 3 sqrt(3) M^2/4 (Estabrook, Wahlquist, Christensen, DeWitt, Smarr & Tsiang 1973, PRD 7, 2814); in KS's "
      "variables b = 3 sqrt(3)/16, xi_* = 4/3 (Kovachik & Sibiryakov 2023/2025, arXiv:2311.12936, eqs. 3.19-3.20)",
      f"r_UH = {rUH}, C = {Ccrit}, b = {b_ks}, xi_* = {xi_star}",
      sp.simplify(rUH - sp.Rational(3, 2) * M_) == 0 and sp.simplify(Ccrit - 3 * sp.sqrt(3) * M_ ** 2 / 4) == 0
      and sp.simplify(b_ks - 3 * sp.sqrt(3) / 16) == 0 and xi_star == sp.Rational(4, 3))

# ================================================================================================ geometry helpers (EF, static aether)
vv, th, ph = sp.symbols("v theta phi", real=True)
XS = [vv, r_, th, ph]


def ef_metric(f):
    return sp.Matrix([[-f, 1, 0, 0], [1, 0, 0, 0], [0, 0, r_ ** 2, 0], [0, 0, 0, r_ ** 2 * sp.sin(th) ** 2]])


def christoffel(g):
    gi = g.inv()
    return gi, [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], XS[c]) + sp.diff(g[d, c], XS[b]) - sp.diff(g[b, c], XS[d])) for d in range(4)) / 2)
                  for c in range(4)] for b in range(4)] for a in range(4)]


def aether_quantities(g, gi, Gam, u_up):
    u_dn = [sp.simplify(sum(g[a, b] * u_up[b] for b in range(4))) for a in range(4)]
    D_dn = [[sp.diff(u_dn[b], XS[a]) - sum(Gam[c][a][b] * u_dn[c] for c in range(4)) for b in range(4)] for a in range(4)]
    D_up = [[sp.diff(u_up[b], XS[a]) + sum(Gam[b][a][c] * u_up[c] for c in range(4)) for b in range(4)] for a in range(4)]
    K = sp.simplify(sum(D_up[a][a] for a in range(4)))
    a_dn = [sp.simplify(sum(u_up[a] * D_dn[a][b] for a in range(4))) for b in range(4)]
    a_up = [sp.simplify(sum(gi[b, c] * a_dn[c] for c in range(4))) for b in range(4)]
    Tm = [[u_up[l] * a_dn[m] for m in range(4)] for l in range(4)]
    divT = [sum(sp.diff(Tm[l][m], XS[l]) for l in range(4)) + sum(Gam[l][l][k] * Tm[k][m] for l in range(4) for k in range(4))
            - sum(Gam[k][l][m] * Tm[l][k] for l in range(4) for k in range(4)) for m in range(4)]
    Ea = [sum(a_up[n] * D_dn[m][n] for n in range(4)) - divT[m] for m in range(4)]      # E^alpha_m / (2 alpha)
    return dict(u_dn=u_dn, K=K, a_dn=a_dn, a_up=a_up, Ea=Ea)


fS = 1 - rs_ / r_
gS = ef_metric(fS)
giS, GamS = christoffel(gS)

# ================================================================================================ K2 KS (3.12)
banner("K2  CONTROL: the static khronon current from the action = KS 2023 eq. (3.12)")
Uf = sp.Function("U")(r_)
Vgen = -sp.sqrt(Uf ** 2 - fS)
Wgen = (Uf + Vgen) / fS
AQ = aether_quantities(gS, giS, GamS, [Wgen, Vgen, 0, 0])
al_, c2_ = sp.symbols("alpha c_2", real=True)
Pup = sp.Matrix(4, 4, lambda i, j: giS[i, j] + [Wgen, Vgen, 0, 0][i] * [Wgen, Vgen, 0, 0][j])
Nlapse = Uf
Jr_alpha = Nlapse * sum(Pup[1, m] * 2 * al_ * AQ["Ea"][m] for m in range(4))
dK = [sp.diff(AQ["K"], XS[m]) for m in range(4)]
Jr_c2 = Nlapse * sum(Pup[1, m] * 2 * c2_ * dK[m] for m in range(4))              # from -c_2 K^2: E^m = 2 c_2 grad^m K
Ux = sp.Function("Ux")(xi_)
Vx = -sp.sqrt(Ux ** 2 - 1 + xi_)
ks_a = sp.diff(Ux, xi_, 2) / Ux
ks_c = -(sp.diff(Vx, xi_, 2) / Vx - 2 / xi_ ** 2)
rng = np.random.default_rng(2025)
k2_ratios = []
for trial in range(3):
    cfs = [sp.Rational(int(x), 100) for x in rng.integers(5, 60, size=3)]
    Utest = 1 - xi_ / 2 + cfs[0] * xi_ ** 2 / 10 - cfs[1] * xi_ ** 3 / 20 + cfs[2] * xi_ ** 4 / 40
    for rv in (3.0, 6.0):
        subU = {Uf: Utest.subs(xi_, rs_ / r_)}
        ja = complex(sp.N(Jr_alpha.subs(subU).doit().subs({rs_: 1, r_: rv, al_: 1})))
        jc = complex(sp.N(Jr_c2.subs(subU).doit().subs({rs_: 1, r_: rv, c2_: 1})))
        ka = complex(sp.N(ks_a.subs(Ux, Utest).doit().subs(xi_, 1 / rv)))
        kc = complex(sp.N(ks_c.subs(Ux, Utest).doit().subs(xi_, 1 / rv)))
        k2_ratios.append((ja / ka) / (jc / kc))
dev_k2 = max(abs(z - 1) for z in k2_ratios)
check("K2 CONTROL: the static khronon current J^r = N P^r_m E^m derived here from the action (alpha a^2 and -c_2 K^2 on "
      "Schwarzschild, decoupling limit) is F(xi)[alpha U''/U - c_2 (V''/V - 2/xi^2)] with one common F: J^r = 0 is KS 2023's "
      "eq. (3.12) with c_chi^2 = c_2/alpha (6 random aether profiles x radii)", f"max |ratio of the two factors - 1| = {dev_k2:.1e}",
      dev_k2 < 1e-10)
L.out["numbers"]["K2"] = dict(max_dev=dev_k2)

# ================================================================================================ K3 KS (4.17) and exponents
banner("K3  CONTROL: the O(v) maximal condition on the C_crit foliation = KS eq. (4.17); exponents at the universal horizon")
eps_ = sp.Symbol("epsilon")
Xf = sp.Function("X")(r_)                                            # the O(v) khronon: T = v + H(r) + eps r_s X(r) cos(theta)
Hfun = sp.Function("H")(r_)
Tkh = vv + Hfun + eps_ * rs_ * Xf * sp.cos(th)
dT = [sp.diff(Tkh, x) for x in XS]
Xn = -sum(giS[a, b] * dT[a] * dT[b] for a in range(4) for b in range(4))
u_up_m = [sum(giS[a, b] * (-dT[b] / sp.sqrt(Xn)) for b in range(4)) for a in range(4)]
sqrtg = r_ ** 2 * sp.sin(th)
Kfull = sum(sp.diff(sqrtg * u_up_m[a], XS[a]) for a in range(4)) / sqrtg
K1 = sp.diff(Kfull, eps_).subs(eps_, 0)
# the CRITICAL background (a control, independent of the MUTATE): u^r = V = -C_crit/r^2; for T = v + H(r): U = N,
# u^r = -N (1 + f H') = V  ->  H' = -(1 + V/U)/f
Cr = Ccrit.subs(M_, rs_ / 2)
Vcrit = -Cr / r_ ** 2
Ucrit = sp.sqrt(fS + Vcrit ** 2)
Hprime_bg = -(1 + Vcrit / Ucrit) / fS
Ksub = K1.subs(sp.Derivative(Hfun, (r_, 2)), sp.diff(Hprime_bg, r_)).subs(sp.Derivative(Hfun, r_), Hprime_bg)
X0s, X1s, X2s = sp.symbols("X0 X1 X2")
Kpoly = Ksub.subs(sp.Derivative(Xf, (r_, 2)), X2s).subs(sp.Derivative(Xf, r_), X1s).subs(Xf, X0s)
cr = [sp.diff(Kpoly, X2s), sp.diff(Kpoly, X1s), sp.diff(Kpoly, X0s)]      # K1 is linear in (X, X', X''): exact coefficients
ks417 = [1 - xi_ + sp.Rational(27, 256) * xi_ ** 4, -(sp.Rational(3, 2) - sp.Rational(81, 128) * xi_ ** 3), -2 / xi_ ** 2]
# to KS: X(r) = chi(xi), xi = r_s/r: X' = -(xi^2/r_s) chi', X'' = (xi^4/r_s^2) chi'' + (2 xi^3/r_s^2) chi' -- evaluated numerically
# on a grid 0 < xi < 4/3 (r_s = 1, theta = 1: the cos(theta) factor cancels in the ratios)
grid = [0.1, 0.5, 0.9, 1.2, 1.3]
k3_dev = 0.0
ratio_rows = []
for g_ in grid:
    rv = 1.0 / g_
    num = {k_: complex(sp.N(cr[k_].subs({rs_: 1, th: 1}).subs(r_, rv), 30)) for k_ in range(3)}
    c2v = num[0] * g_ ** 4
    c1v = num[0] * 2 * g_ ** 3 - num[1] * g_ ** 2
    c0v = num[2]
    ksv = [complex(sp.N(e_.subs(xi_, g_), 30)) for e_ in ks417]
    r1 = (c1v / c2v) / (ksv[1] / ksv[0])
    r0 = (c0v / c2v) / (ksv[2] / ksv[0])
    ratio_rows.append((g_, r1, r0))
    k3_dev = max(k3_dev, abs(r1 - 1), abs(r0 - 1))
ratio_c = ["(numerical)"] * 3
c2c = c1c = c0c = None
k3_eq = k3_dev < 1e-10                                           # float-evaluated ratios
gam = sp.Symbol("gamma")
xs0 = sp.Rational(4, 3)
# Frobenius at xi_* for KS's form
A2 = sp.diff(ks417[0], xi_).subs(xi_, xs0)
indicial_star = sp.solve(sp.expand(A2 * gam * (gam - 1) + ks417[1].subs(xi_, xs0) * gam + 0), gam) if False else None
xloc = sp.Symbol("x")
Acoef = sp.series(ks417[0].subs(xi_, xs0 + xloc), xloc, 0, 2).removeO()
Bcoef = sp.series(ks417[1].subs(xi_, xs0 + xloc), xloc, 0, 1).removeO()
Ccoef = ks417[2].subs(xi_, xs0)
# near x = 0: A ~ a2 x^2 (double zero), B ~ b1 x? check orders
a2c = sp.simplify(sp.series(ks417[0].subs(xi_, xs0 + xloc), xloc, 0, 3).removeO().coeff(xloc, 2))
a1c = sp.simplify(sp.series(ks417[0].subs(xi_, xs0 + xloc), xloc, 0, 3).removeO().coeff(xloc, 1))
a0c = sp.simplify(ks417[0].subs(xi_, xs0))
b0c = sp.simplify(ks417[1].subs(xi_, xs0))
b1c = sp.simplify(sp.series(ks417[1].subs(xi_, xs0 + xloc), xloc, 0, 2).removeO().coeff(xloc, 1))
indic = sp.solve(a2c * gam * (gam - 1) + b1c * gam + Ccoef, gam)
indic0 = sp.solve(gam * (gam - 1) - sp.Rational(3, 2) * gam * 0 + (-2) + 0, gam)   # at xi -> 0: xi^2 chi'' ... handled below
# at xi = 0: (1)chi'' - (3/2) chi' - 2 chi/xi^2 -> leading xi^2 chi'' - 2 chi = 0 -> gamma(gamma - 1) = 2
indic0 = sp.solve(gam * (gam - 1) - 2, gam)
P("    derived O(v) equation vs KS eq. (4.17), coefficient ratios (chi'/chi'', chi/chi'') mine/KS on the grid: "
  + "; ".join(f"xi {g_}: {abs(r1):.15f}, {abs(r0):.15f}" for g_, r1, r0 in ratio_rows))
P(f"    KS eq. (4.17): [{ks417[0]}] chi'' + [{ks417[1]}] chi' + [{ks417[2]}] chi = 0;  identical to 1e-10: {k3_eq}")
P(f"    at xi_* = 4/3: A = {a0c} + {a1c} x + {a2c} x^2, B = {b0c} + {b1c} x -> exponents {indic};  at xi = 0: {indic0}")
check("K3 CONTROL: the O(v) (dipole) perturbation of the maximal foliation, derived here from K = nabla.u = 0 on Schwarzschild "
      "with the C_crit background, is KS 2023's eq. (4.17) exactly; its exponents are -1 +- sqrt 2 at the universal horizon "
      "(KS eq. 4.18b) and -1, 2 at infinity -- equivalently -2 +- sqrt 2 for Ramos & Barausse 2019's delta = chi' (their eqs. "
      "70-71): the soft mode (-1 + sqrt 2 = 0.414) is the admissible one",
      f"identical to KS 4.17: {k3_eq} (max deviation on a grid {k3_dev:.1e}); exponents at xi_*: {indic}; at 0: {indic0}",
      k3_eq and set(sp.simplify(x) for x in indic) == {-1 + sp.sqrt(2), -1 - sp.sqrt(2)} and set(indic0) == {-1, 2})

# ================================================================================================ K4 L33's horizon formula
banner("K4  CONTROL: the horizon of a mode of speed c_s relative to the aether (the record's L33 C4-C5)")
mp.mp.dps = 60
Cn = 3 * mp.sqrt(3) / 4
gN2 = lambda r: 1 - 2 / r + Cn ** 2 / r ** 4
k4 = []
for cs in (10, 100, 2522, 10 ** 6):
    csm = mp.mpf(cs)
    rh = mp.findroot(lambda r: gN2(r) - Cn ** 2 / (csm ** 2 * r ** 4), (mp.mpf("1.5") + mp.mpf(1e-30), mp.mpf(2)), solver="bisect")
    x0 = mp.sqrt(mp.mpf(3) / 8) / csm
    k4.append((cs, float(rh - mp.mpf("1.5")), float(x0), float(x0 * (1 - mp.mpf(4) / 9 * x0))))
mp.mp.dps = 40
for cs, d_, x0, x1 in k4:
    P(f"    c_s = {cs:g}: r_h - 3M/2 = {d_:.9e} M; sqrt(3/8) M/c_s = {x0:.9e} M; with the next order x0 (1 - 4 x0/9) = {x1:.9e} M")
check("K4 CONTROL: a mode moving at c_s relative to the aether escapes the maximal black hole iff N^2 > C^2/(c_s^2 r^4); its "
      "horizon sits at r_h - 3M/2 = x0 (1 - (4/9) x0/M + ...), x0 = sqrt(3/8) M/c_s (the leading term is the record's L33 C4-C5: "
      "r_h = 1.50024 M at c_s = 2522; the next order derived here from N^2's cubic term); 60-digit roots.  DISCLOSED: the first "
      "(MUTATE) run compared with the leading term only, at double precision, and FAILED at c_s = 100 (the O(1/c_s) correction, "
      "2.7e-3) -- the comparison now includes the next order",
      "; ".join(f"c_s {cs:g}: ratio to next-order form {d_ / x1:.9f}" for cs, d_, x0, x1 in k4),
      all(abs(d_ / x1 - 1) < 30 * (x0 ** 2) + 1e-12 for cs, d_, x0, x1 in k4 if cs >= 100))
P(f"    {L.el()}")

# ================================================================================================ N1 static neutron stars
banner("N1  STATIC NEUTRON STARS: the CMC foliation with K_0 = 3 H_0 exists, unique and regular")
EOS = C.make_pp_eos()
H0 = 67.4e3 / (3.0856775814913673e22)          # s^-1 (the chain's h = 0.674)
K0_SI = 3 * H0 / C.cc                           # 1/m
n1 = {}
for Mt in (1.338, 1.46, 2.01):
    st = C.star_of_mass(EOS, Mt)
    s_ = C.tov_star(EOS, st["rho_c"], want_profile=True)
    sol_ = s_["sol"]
    Rcm = sol_.t[-1]
    rr = np.linspace(1.0, Rcm, 20000)
    Y = sol_.sol(rr)
    m_r = Y[0]
    phi_r = Y[3] + s_["phi_shift"]
    lam_r = -0.5 * np.log(1 - 2 * C.G_CGS * m_r / (rr * C.C_CGS ** 2))
    wgt = rr ** 2 * np.exp(phi_r + lam_r)
    Vint = np.concatenate([[0.0], np.cumsum(0.5 * (wgt[1:] + wgt[:-1]) * np.diff(rr))])
    nr = K0_SI * 1e-2 * Vint / (rr ** 2 * np.exp(phi_r + lam_r))        # K0 in 1/cm
    # check K = K0 by finite differences: K = e^{-Phi-Lambda} r^-2 d(r^2 e^{Phi+Lambda} n^r)/dr
    Kchk = np.gradient(rr ** 2 * np.exp(phi_r + lam_r) * nr, rr) / (rr ** 2 * np.exp(phi_r + lam_r))
    inner = rr > 0.05 * Rcm                                            # the FD derivative of a cumulative trapezoid of ~r^2 has
    relK = float(np.max(np.abs(Kchk[inner][:-5] / (K0_SI * 1e-2) - 1)))  # relative error ~h^2/(3 r^2): excluded near the centre
    tilt_surface = float(nr[-1])                                        # dimensionless (c = 1): u^r at the surface
    center_ok = abs(nr[20] / (K0_SI * 1e-2 * rr[20] / 3) - 1) < 1e-2
    n1[Mt] = dict(R_km=s_["R_km"], C=s_["C"], tilt=tilt_surface, relK=relK, center_ok=center_ok)
    P(f"    M = {Mt} Msun (R = {s_['R_km']:.2f} km, C = {s_['C']:.3f}): u^r(surface) = {tilt_surface:.2e} (K_0 R/3 = "
      f"{K0_SI * s_['R_km'] * 1e3 / 3:.2e}); K/K_0 - 1 <= {relK:.1e}; regular centre n^r -> K_0 r/3: {center_ok}")
check("N1 (H1) AROUND STATIC STARS THE CMC LEAVES EXIST AND ARE REGULAR: the stationary foliation with K = K_0 = 3 H_0 is "
      "n^r = K_0 Int_0^r r'^2 e^{Phi + Lambda} dr' / (r^2 e^{Phi + Lambda}) (unique: the r^-2 homogeneous piece is excluded by the "
      "centre), regular everywhere, a tilt u^r ~ K_0 r/3 ~ 1e-22 at the surface; at K_0 = 0 it is the static slicing (maximal "
      "slicing of static stars is the t = const slicing)",
      "; ".join(f"{m_}: tilt {v_['tilt']:.1e}, K err {v_['relK']:.0e}" for m_, v_ in n1.items()),
      all(v_["relK"] < 1e-3 and v_["center_ok"] and v_["tilt"] < 1e-20 for v_ in n1.values()))
L.out["numbers"]["N1"] = {str(k_): v_ for k_, v_ in n1.items()}

# ================================================================================================ N2 moving neutron stars
banner("N2  MOVING NEUTRON STARS: the O(v) perturbation of the maximal foliation, D_i(N^2 D^i psi) = 0, psi = v F(r) cos(theta)")
# derivation (sympy): K for T = t + eps F(r) cos(theta) on a static metric -> the l = 1 ODE
tS = sp.Symbol("t")
Phf, Lmf, Ff = sp.Function("Phi")(r_), sp.Function("Lam")(r_), sp.Function("F")(r_)
gst = sp.diag(-sp.exp(2 * Phf), sp.exp(2 * Lmf), r_ ** 2, r_ ** 2 * sp.sin(th) ** 2)
gsti = gst.inv()
XT = [tS, r_, th, ph]
Tst = tS + eps_ * Ff * sp.cos(th)
dTs = [sp.diff(Tst, x) for x in XT]
Xs_ = -sum(gsti[a, b] * dTs[a] * dTs[b] for a in range(4) for b in range(4))
uup_s = [sum(gsti[a, b] * (-dTs[b] / sp.sqrt(Xs_)) for b in range(4)) for a in range(4)]
sqg_s = sp.exp(Phf + Lmf) * r_ ** 2 * sp.sin(th)
Ks = sum(sp.diff(sqg_s * uup_s[a], XT[a]) for a in range(4)) / sqg_s
Ks1 = sp.simplify(sp.diff(Ks, eps_).subs(eps_, 0) / sp.cos(th))                  # linearise first, then simplify
ode_target = (sp.diff(r_ ** 2 * sp.exp(2 * Phf - Lmf) * sp.diff(Ff, r_), r_) - 2 * sp.exp(2 * Phf + Lmf) * Ff)
prop = sp.simplify(Ks1 / ode_target)
P(f"    dK/d(eps) / [ (r^2 N^2 e^-Lambda F')' - 2 N^2 e^Lambda F ] = {prop}")
n2 = {}
for Mt in (1.338, 2.01):
    st = C.star_of_mass(EOS, Mt)
    s_ = C.tov_star(EOS, st["rho_c"], want_profile=True)
    sol_ = s_["sol"]
    Rcm = sol_.t[-1]
    Mg = s_["M"] * C.MSUN_G * C.G_CGS / C.C_CGS ** 2                   # cm

    def bg(r):
        if r <= Rcm:
            Yv = sol_.sol(r)
            m = Yv[0] * C.G_CGS / C.C_CGS ** 2
            ph_ = Yv[3] + s_["phi_shift"]
        else:
            m = Mg
            ph_ = 0.5 * math.log(1 - 2 * Mg / r)
        lam = -0.5 * math.log(1 - 2 * m / r)
        return ph_, lam

    def rhs(r, Y):
        F, G_ = Y                                                        # G_ = r^2 N^2 e^-Lam F'
        ph_, lam = bg(r)
        N2_ = math.exp(2 * ph_)
        return [G_ / (r * r * N2_ * math.exp(-lam)), 2 * N2_ * math.exp(lam) * F]
    r0 = 10.0
    ph0, lam0 = bg(r0)
    Y0 = [r0, r0 * r0 * math.exp(2 * ph0 - lam0)]
    rmax = 2000 * Rcm
    solN = solve_ivp(rhs, (r0, rmax), Y0, rtol=1e-11, atol=1e-30, method="LSODA", dense_output=True)
    # far field: F -> A r (the boost); report F/r at 10 R, 100 R and the outer radius, normalised to the outermost value
    rr_chk = [10 * Rcm, 100 * Rcm, rmax]
    Fr = [float(solN.sol(x)[0] / x) for x in rr_chk]
    Fr = [x / Fr[-1] for x in Fr]
    n2[Mt] = dict(F_over_r_normalised=Fr, monotone=bool(np.all(np.diff(solN.y[0]) > 0)), positive=bool(np.all(solN.y[0] > 0)))
    P(f"    M = {Mt}: the solution regular at the centre (F ~ r) is nodeless and increasing: {n2[Mt]['monotone']}; F/r (normalised at "
      f"{rmax / Rcm:.0f} R) = {Fr[0]:.6f} (10 R), {Fr[1]:.6f} (100 R): it tends to the boost F = A r")
check("N2 (H1) AROUND MOVING STARS THE LEAVES EXIST TOO: the O(v) perturbation of the maximal foliation (T = t + v F(r) cos(theta)) "
      "obeys dK/dv ~ (r^2 N^2 e^-Lambda F')' - 2 N^2 e^Lambda F = 0, i.e. D_i(N^2 D^i psi) = 0 on the static slice (derived); N > 0 "
      "everywhere (no horizon) so the equation has no singular point: the solution regular at the centre (F ~ r) is unique up to "
      "normalisation and tends to the boost F = A r -- a nodeless, monotone profile",
      "; ".join(f"{m_}: monotone {v_['monotone']}, F/r(10 R) = {v_['F_over_r_normalised'][0]:.4f}" for m_, v_ in n2.items()),
      sp.simplify(prop) != 0 and not sp.simplify(prop).has(Ff) and all(v_["monotone"] and v_["positive"] for v_ in n2.values())
      and all(abs(v_["F_over_r_normalised"][1] - 1) < 0.05 for v_ in n2.values()))
L.out["numbers"]["N2"] = {str(k_): v_ for k_, v_ in n2.items()}
P(f"    {L.el()}")

# ================================================================================================ B1 static black holes
banner("B1  STATIC BLACK HOLES: the C_crit maximal foliation, the universal horizon, and what fails for C != C_crit")
Mv = sp.Symbol("M", positive=True)
fM = 1 - 2 * Mv / r_
Cuse = CFAC * 3 * sp.sqrt(3) * Mv ** 2 / 4
Vb = -Cuse / r_ ** 2
Ub = sp.sqrt(fM + Vb ** 2)
Wb = (Ub + Vb) / fM
gB = ef_metric(fM)
giB, GamB = christoffel(gB)
AB_ = aether_quantities(gB, giB, GamB, [Wb, Vb, 0, 0])
a2B = sp.simplify(sum(AB_["a_dn"][b] * AB_["a_up"][b] for b in range(4)))
KB = sp.simplify(AB_["K"])
P(f"    K on the foliation = {KB};  a^2 = {sp.factor(a2B)}")
if not L.mutate:
    rstar = sp.Rational(3, 2) * Mv
    a2_uh = sp.simplify(sp.limit(a2B, r_, rstar, "+"))
    av_uh = sp.simplify(sp.limit(AB_["a_dn"][0], r_, rstar, "+"))
    ar_uh = sp.simplify(sp.limit(AB_["a_dn"][1], r_, rstar, "+"))
    Up = sp.sqrt(sp.diff(fM + Vb ** 2, r_, 2).subs(r_, rstar) / 2)
    xs_ = sp.Rational(4, 3)
    Ux_prime = sp.sqrt(sp.Rational(1, 2) * sp.diff(1 - xi_ + (3 * sp.sqrt(3) / 16) ** 2 * xi_ ** 4, xi_, 2).subs(xi_, xs_))
    kappa_UH = sp.simplify(Ux_prime * xs_ ** 2 * sp.sqrt(xs_ - 1) / (2 * Mv))     # KS eq. (3.17)'s rate
    reg_ok = a2_uh.is_finite and av_uh.is_finite and ar_uh.is_finite
    P(f"    at r = 3M/2: a^2 = {a2_uh}, a_v = {av_uh}, a_r = {ar_uh} (finite);  U'(r_UH) = {sp.simplify(Up)};  "
      f"KS eq. (3.17)'s rate (makes the khronon analytic across the universal horizon) kappa_UH = |U'_xi| xi_*^2 sqrt(xi_* - 1)/r_s = "
      f"{kappa_UH} = {float(kappa_UH.subs(Mv, 1)):.4f}/M")
    # the leaf's throat: proper length from r = 1.6M to r_UH diverges (dl = dr/N, N ~ x)
    Nnum = sp.lambdify(r_, sp.sqrt(fM + Vb ** 2).subs(Mv, 1))
    lens = [quad(lambda x: 1 / Nnum(x), 1.5 + d_, 1.6, limit=200)[0] for d_ in (1e-2, 1e-4, 1e-6)]
    P(f"    proper length along a leaf from r = 1.6M to r = 3M/2 + d: d = 1e-2: {lens[0]:.3f}, 1e-4: {lens[1]:.3f}, 1e-6: {lens[2]:.3f} M "
      f"(grows like ln(1/d)/|U'|: the leaf's throat is infinitely long)")
    L.out["numbers"]["B1"] = dict(a2_UH=str(a2_uh), kappa_UH=str(kappa_UH), throat_lengths=lens)
else:
    # the non-critical family: N^2 = f + C^2/r^4 now has two simple zeros inside the horizon; U ~ sqrt(x) at the first
    roots = sp.nroots(sp.numer(sp.together((fM + Vb ** 2).subs(Mv, 1))), n=30)
    rr_ = sorted([float(sp.re(z)) for z in roots if abs(sp.im(z)) < 1e-20 and sp.re(z) > 0])
    r1 = max(rr_)
    a2f = sp.lambdify(r_, a2B.subs(Mv, 1))
    vals = [float(abs(a2f(r1 + d_))) for d_ in (1e-2, 1e-4, 1e-6)]
    reg_ok = vals[-1] < 10 * vals[0]
    P(f"    C = 0.98 C_crit: N^2 has simple zeros at r = {rr_} M; a^2 near the outer one: {vals} (grows without bound)")
    L.out["numbers"]["B1"] = dict(zeros=rr_, a2_near=vals)
check("B1 (H2) AROUND STATIC BLACK HOLES THE REGULAR CMC LEAVES EXIST ONLY FOR C = C_crit, AND THEY STOP AT r = 3M/2: the "
      "foliation u^r = -C_crit/r^2 has K = 0, crosses the Killing horizon smoothly, and its leaves asymptote to the cylinder "
      "r = 3M/2 (itself a K = 0 leaf, u . chi = 0: a universal horizon), which they reach only at infinite proper length and "
      "tau = oo; the aether and its acceleration are regular there (a^2 = 8/(9M^2)).  For C != C_crit the family is either "
      "non-smooth (C < C_crit: U ~ sqrt(r - r_1), a diverges) or reaches r = 0 on the exterior leaves (C > C_crit: the singularity "
      "on a leaf that also reaches infinity -- visible to leafwise-instantaneous signals)",
      "regular at r_UH" if reg_ok else "NOT regular: a^2 diverges at the first zero of N^2", reg_ok)
# Kottler / CMC with K_0 = sqrt(3 Lambda): the Lambda terms cancel exactly in N^2
Lam_, K0_ = sp.symbols("Lambda K_0", positive=True)
nr_k = K0_ * r_ / 3 - Cc_ / r_ ** 2
N2k = sp.expand(1 - 2 * M_ / r_ - Lam_ * r_ ** 2 / 3 + nr_k ** 2)
cancel = sp.simplify(N2k.subs(K0_, sp.sqrt(3 * Lam_)) - (1 - 2 * (M_ + sp.sqrt(3 * Lam_) * Cc_ / 3) / r_ + Cc_ ** 2 / r_ ** 4)) == 0
Lam_SI = 3 * (67.4e3 / 3.0856775814913673e22) ** 2 * 0.6847 / C.cc ** 2
Mbh = 10 * C.GM_SUN / C.cc ** 2
shift = math.sqrt(3 * Lam_SI) * (3 * math.sqrt(3) / 4 * Mbh ** 2) / (3 * Mbh)
P(f"    Kottler with the de Sitter-matching CMC value K_0 = sqrt(3 Lambda): N^2 = 1 - 2(M + K_0 C/3)/r + C^2/r^4 exactly: {cancel}; "
      f"for a 10 Msun hole the universal horizon moves by delta r/r = {shift:.1e}")
check("B1b (reported) with the cosmological CMC value (K_0 = sqrt(3 Lambda) on Schwarzschild-de Sitter) the Lambda terms cancel "
      "in N^2: the universal horizon is at r = 3M'/2 with M' = M + K_0 C/3, a relative shift ~1e-22 for stellar holes",
      f"exact cancellation {cancel}; shift {shift:.1e}", cancel and shift < 1e-15, load_bearing=False)
P(f"    {L.el()}")

# ================================================================================================ B2 moving black holes at alpha_c = 0
banner("B2  MOVING BLACK HOLES AT alpha_c = 0: the unique regular O(v) solution (KS 4.17, soft mode) and the stealth khronon")
b2 = {}
if not L.mutate:
    A_ = lambda x: 1 - x + 27 / 256 * x ** 4
    Bc = lambda x: -(1.5 - 81 / 128 * x ** 3)
    def ode(x, Y):
        return [Y[1], -(Bc(x) * Y[1] - 2 / x ** 2 * Y[0]) / A_(x)]
    gs = -1 + math.sqrt(2)
    # Frobenius start at the universal horizon: chi = (x* - xi)^gs (1 + c1 (x* - xi)), c1 from the series
    xs = 4.0 / 3.0
    Xl = sp.Symbol("X")
    c1s = sp.Symbol("c1")
    chi_ser = Xl ** sp.nsimplify(-1 + sp.sqrt(2)) * (1 + c1s * Xl)
    xi_of = xs - Xl
    Aser = sp.series((1 - xi_ + sp.Rational(27, 256) * xi_ ** 4).subs(xi_, sp.Rational(4, 3) - Xl), Xl, 0, 4).removeO()
    Bser = sp.series((-(sp.Rational(3, 2) - sp.Rational(81, 128) * xi_ ** 3)).subs(xi_, sp.Rational(4, 3) - Xl), Xl, 0, 3).removeO()
    Cser = sp.series((-2 / xi_ ** 2).subs(xi_, sp.Rational(4, 3) - Xl), Xl, 0, 2).removeO()
    # d/dxi = -d/dX
    res_ = sp.expand(Aser * sp.diff(chi_ser, Xl, 2) - Bser * sp.diff(chi_ser, Xl) + Cser * chi_ser)
    res_ = sp.expand(sp.simplify(res_ / Xl ** sp.nsimplify(-1 + sp.sqrt(2))))
    c1v = sp.solve(sp.simplify(res_.coeff(Xl, 0)), c1s)
    c1n = float(c1v[0]) if c1v else 0.0
    X0 = 1e-4
    chi0 = X0 ** gs * (1 + c1n * X0)
    dchi_dX = gs * X0 ** (gs - 1) * (1 + c1n * X0) + c1n * X0 ** gs
    solB = solve_ivp(ode, (xs - X0, 1e-4), [chi0, -dchi_dX], rtol=1e-11, atol=1e-14, method="LSODA", dense_output=True)
    x_end = solB.t[-1]
    chi_end, dchi_end = solB.y[:, -1]
    # at xi -> 0: chi = a/xi + b xi^2 -> a from the two values
    a_inf = (chi_end - x_end * dchi_end / 2) / (1.5 / x_end)
    norm = 1 / a_inf
    # aether perturbation near the universal horizon (KS 4.5): du_r ~ xi^2 U^3 chi', du_v ~ xi^2 U^2 V chi', du_theta ~ U chi
    Uc = lambda x: math.sqrt(max(1 - x + (3 * math.sqrt(3) / 16) ** 2 * x ** 4, 0.0))
    Vc = lambda x: -(3 * math.sqrt(3) / 16) * x ** 2
    samples = []
    for Xv in (1e-2, 1e-3, 1e-4):
        chv, dchv = solB.sol(xs - Xv) if Xv > X0 else (chi0, -dchi_dX)
        chv, dchv = chv * norm, dchv * norm
        samples.append(dict(X=Xv, du_r=(xs - Xv) ** 2 * Uc(xs - Xv) ** 3 * dchv, du_v=(xs - Xv) ** 2 * Uc(xs - Xv) ** 2 * Vc(xs - Xv) * dchv,
                            du_th=Uc(xs - Xv) * chv))
    for s_ in samples:
        P(f"    xi_* - xi = {s_['X']:.0e}: delta u_r/(v cos) = {s_['du_r']:.3e}, delta u_v/(v cos) = {s_['du_v']:.3e}, "
          f"r delta u_theta/(v sin) ~ U chi = {s_['du_th']:.3e}")
    # slopes: d log|du|/d log X ~ exponents (C^1: du ~ X^{1+sqrt2}, du_th ~ X^{sqrt2})
    sl_r = math.log(abs(samples[2]["du_r"] / samples[1]["du_r"])) / math.log(1e-4 / 1e-3)
    sl_th = math.log(abs(samples[2]["du_th"] / samples[1]["du_th"])) / math.log(1e-4 / 1e-3)
    b2 = dict(c1=c1n, a_inf=a_inf, slope_du_r=sl_r, slope_du_th=sl_th, samples=samples)
    P(f"    the soft mode integrated out to xi = {x_end:.0e} and normalised to chi -> 1/xi; delta u_r ~ X^{sl_r:.3f} (C^1: 1 + sqrt 2 = "
      f"{1 + math.sqrt(2):.3f} expected from U^3 chi'), delta u_theta ~ X^{sl_th:.3f} (sqrt 2 = {math.sqrt(2):.3f})")
    b2ok = abs(sl_r - (1 + math.sqrt(2))) < 0.02 and abs(sl_th - math.sqrt(2)) < 0.02 and math.isfinite(a_inf) and a_inf != 0
else:
    b2ok = True
check("B2 (H3) AT alpha_c = 0 THE SLOWLY MOVING BLACK HOLE IS REGULAR: the soft mode of KS 4.17, fixed uniquely at the universal "
      "horizon, integrates out to the boost (chi -> 1/xi after normalisation); the aether perturbation vanishes at the universal "
      "horizon as X^(1 + sqrt 2) (radial) and X^sqrt(2) (angular): C^1, non-analytic only in the second derivative -- KS's "
      "'weak singularity'; the khronon is a stealth field (its stress is proportional to alpha_c and to the multiplier, both zero), "
      "so the metric is exactly Schwarzschild and the sensitivity vanishes (Ramos & Barausse 2019; Franchini et al. 2021)",
      f"exponents radial {b2.get('slope_du_r', float('nan')):.3f}, angular {b2.get('slope_du_th', float('nan')):.3f}" if b2 else "not evaluated (MUTATE)",
      b2ok)
L.out["numbers"]["B2"] = b2
P(f"    {L.el()}")

# ================================================================================================ B3 alpha_c > 0, c_2 = oo, first order
banner("B3  alpha_c > 0, c_2 = oo, FIRST ORDER IN alpha_c: the multiplier at the universal horizon")
b3 = {}
if not L.mutate:
    # J^r = F(xi)[alpha U''/U + r_s mu_xi'/(xi^2 V)] (the c_2 part with c_2 K -> mu), F = -2 U^3 xi^4 V/r_s^2 (derived below)
    # the mu-part of J^r directly from the action: E^m = 2 grad^m mu, J^r = N P^r_m E^m with mu = mu(r)
    muf = sp.Function("mu")(r_)
    Jr_mu = Nlapse * sum(Pup[1, m] * 2 * sp.diff(muf, XS[m]) for m in range(4))
    Fform = sp.simplify(Jr_mu / sp.diff(muf, r_))
    P(f"    mu-part of the current: J^r_mu = {sp.factor(Fform)} x mu'(r)  (= 2 U^3 mu': vanishes at the universal horizon as U^3)")
    # on the maximal background: mu_xi' = -alpha xi^2 V U''/(r_s U)  (C_1 = 0 forced: a C_1/r^2 would enter as 1/U^3)
    bnum = 3 * math.sqrt(3) / 16
    Ux2 = 1 - xi_ + sp.Rational(27, 256) * xi_ ** 4
    Uxs = sp.sqrt(Ux2)
    Upp = sp.simplify(sp.diff(Uxs, xi_, 2))
    Vxs = -sp.Rational(3, 16) * sp.sqrt(3) * xi_ ** 2
    mup_xi = sp.simplify(-xi_ ** 2 * Vxs * Upp / Uxs)                  # per alpha/r_s
    # leading behaviour at xi_*: coefficient of 1/(xi - xi_*)
    Xs = sp.Symbol("X", positive=True)
    lead = sp.simplify(sp.limit(mup_xi.subs(xi_, sp.Rational(4, 3) - Xs) * Xs, Xs, 0))
    P(f"    mu'_xi = -alpha xi^2 V U''/(r_s U) on the maximal background; at xi -> xi_* : mu'_xi -> ({lead}) (alpha/r_s)/(xi_* - xi)")
    # numerical check of the log: integrate mu'_xi from xi = 1.0 towards xi_* and fit d mu / d ln X
    fmu = sp.lambdify(xi_, mup_xi, "mpmath")
    vals = []
    for Xv in (1e-3, 1e-5, 1e-7):
        vals.append(mp.quad(lambda x: fmu(x), [1.0, 4 / mp.mpf(3) - Xv]))
    slope = (vals[2] - vals[1]) / (mp.log(mp.mpf("1e-7")) - mp.log(mp.mpf("1e-5")))
    coef_r = float(-lead / 2)                                          # per alpha/M: r_s = 2M, and mu ~ -lead ln X (alpha/r_s)
    P(f"    integral of mu'_xi towards the horizon: mu(X = 1e-3, 1e-5, 1e-7) = {[mp.nstr(v_, 8) for v_ in vals]} (alpha/r_s); "
      f"d mu/d ln X = {mp.nstr(slope, 10)} (alpha/r_s) -> |mu| grows as {abs(float(lead)) / 2:.4f} (alpha_c/M) ln(1/X)")
    # independent: mu'(r) = -J^r_alpha/(2 U^3) with J^r_alpha the action's current (K2) on the maximal background, vs the formula
    Umax_r = sp.sqrt(1 - rs_ / r_ + (3 * sp.sqrt(3) / 16) ** 2 * (rs_ / r_) ** 4)
    Ja_bg = Jr_alpha.subs(Uf, Umax_r).doit()
    dev_mu = 0.0
    for xv in (0.8, 1.2, 1.33):
        rv = 1 / xv
        mu_r = complex(sp.N((-Ja_bg / (2 * Umax_r ** 3)).subs({rs_: 1, al_: 1, r_: rv}), 30)).real
        mu_xi_direct = mu_r * (-1 / xv ** 2)                                  # d mu/d xi = mu'(r) dr/dxi, r_s = 1
        mu_xi_formula = float(fmu(xv))
        dev_mu = max(dev_mu, abs(mu_xi_direct / mu_xi_formula - 1))
    P(f"    independent check: mu'(r) = -J^r_alpha/(2 U^3) from the action's current (K2) on the maximal background equals the formula "
      f"to {dev_mu:.1e} at xi = 0.8, 1.2, 1.33")
    b3 = dict(lead=str(lead), lead_num=float(lead), slope=float(slope), coef_alpha_over_M=abs(float(lead)) / 2, direct_dev=dev_mu)
    log_div = abs(float(slope) + float(lead)) < 1e-4 * abs(float(lead)) and abs(float(lead)) > 0.1 and dev_mu < 1e-8
    # the non-uniformity layer: the full theory's spin-0 horizon at c_s^2 = (2 - alpha_c)/(3 alpha_c)
    for ac in (C.AC_WINDOW["floor_XC1_c2inf"], C.AC_WINDOW["cap"]):
        cs = math.sqrt((2 - ac) / (3 * ac))
        dr = math.sqrt(3 / 8) / cs
        mu_edge = abs(float(lead)) / 2 * ac * math.log(1 / (dr / 1.5))
        b3[f"layer_{ac:.1e}"] = dict(cs=cs, dr_over_M=dr, mu_at_layer=mu_edge, curv_rel=ac / dr)
        P(f"    alpha_c = {ac:.1e}: spin-0 horizon (full theory, c_s = {cs:.3e} c) at r - 3M/2 = {dr:.2e} M; the first-order |mu| there "
          f"~ {mu_edge:.1e}/M and the first-order curvature ~ alpha_c/(r - r_UH) ~ {ac / dr:.1e}/M^2 (vs the background 1/M^2)")
else:
    log_div = True
check("B3 (H4) AT alpha_c > 0 AND c_2 = oo THE STATIC BLACK HOLE IS SINGULAR AT THE UNIVERSAL HORIZON AT FIRST ORDER IN alpha_c: the "
      "khronon's equation J^r = C_1/r^2 (derived; its multiplier part is 2 U^3 mu', so C_1 = 0 is forced) fixes mu'_xi = -alpha_c "
      "xi^2 V U''/(r_s U); on the maximal background U''(xi_*) != 0 (finite c_chi forces U''(xi_*) = 0 -- the limit is not uniform), "
      "so mu = (4 sqrt 3/27)(alpha_c/M) ln|r/(3M/2) - 1| + regular: LOG-DIVERGENT, and the multiplier's stress (trace = 6 mu-dot per "
      "1/16 pi G by its conformal weight 3; mu-dot = u.grad mu ~ alpha_c/(r - 3M/2)) diverges -- a curvature singularity at O(alpha_c)",
      f"leading mu'_xi coefficient {b3.get('lead', '-')}; numerical d mu/d ln X = {b3.get('slope', float('nan')):.6f} (alpha/r_s)" if b3 else "MUTATE",
      log_div,
      reading="first order only: the expansion is non-uniform within the full theory's spin-0-horizon layer r - 3M/2 ~ sqrt(3/8) M/c_s "
              "~ (3/4) sqrt(alpha_c) M, where the singular term would be cut off at |mu| ~ alpha_c ln(1/alpha_c)/M; whether a regular "
              "solution exists there is OPEN (Ramos & Barausse 2019 found singular moving holes for generic couplings; Kovachik & "
              "Sibiryakov's regular ones are in the decoupling limit, which at c_2 = oo misses the metric's O(1) inertia)")
L.out["numbers"]["B3"] = b3

# B3b: the multiplier's stress trace from its Weyl weight -- K[e^(2w) g, T] = e^(-w) (K + 3 u.grad w), checked on the actual
# background with a generic w(r); then d/dw of Int sqrt(-g) 2 mu (K - K_0) = -6 sqrt(-g) u.grad mu - 8 sqrt(-g) mu K_0: the trace
# of the multiplier's stress is proportional to 6 mu-dot (+ 8 mu K_0), so a mu-dot ~ alpha_c/(r - 3M/2) is a divergent T^m_m
wf = sp.Function("w")(r_)
g2 = sp.exp(2 * wf) * gB.subs(Mv, 1)
gi2, Gam2 = christoffel(g2)
u_up2 = [sp.exp(-wf) * x for x in [Wb.subs(Mv, 1), Vb.subs(Mv, 1), 0, 0]]
sq2 = sp.exp(4 * wf) * r_ ** 2 * sp.sin(th)
K2w = sum(sp.diff(sq2 * u_up2[a], XS[a]) for a in range(4)) / sq2
K1w = sum(sp.diff(r_ ** 2 * sp.sin(th) * [Wb.subs(Mv, 1), Vb.subs(Mv, 1), 0, 0][a], XS[a]) for a in range(4)) / (r_ ** 2 * sp.sin(th))
law = sp.exp(-wf) * (K1w + 3 * Vb.subs(Mv, 1) * sp.diff(wf, r_))
dev_w = max(abs(complex(sp.N((K2w - law).subs(wf, sp.sin(r_) / 3 + r_ ** 2 / 7).doit().subs(r_, rv), 25))) for rv in (1.6, 2.5, 4.0)) if not L.mutate else 0.0
check("B3b the multiplier's stress trace is 6 mu-dot (+ 8 mu K_0) per 1/16 pi G: K transforms with Weyl weight -1 plus 3 u.grad w "
      "(checked on the actual maximal background with a generic w(r)), so varying Int sqrt(-g) 2 mu (K - K_0) with respect to the "
      "conformal factor leaves -6 u.grad mu - 8 mu K_0; with mu-dot = u^r mu' = V mu' and V(r_UH) = -1/sqrt 3 != 0 the first-order "
      "trace diverges as alpha_c/(r - 3M/2) -- via Einstein's equations a Ricci-scalar divergence at O(alpha_c)",
      f"max |K[e^2w g] - e^-w (K + 3 u.grad w)| = {dev_w:.1e}", dev_w < 1e-15)

# ================================================================================================ B4 ringdown
banner("B4  RINGDOWN (reported)")
check("B4 (reported) RINGDOWN IS GR'S TO O(alpha_c): tensor modes have c_T = 1 (FP2 A3 / FP7 D1) and their horizon is the Killing "
      "horizon; the quasinormal modes are set near the light ring r = 3M, where the metric is Schwarzschild + O(alpha_c) (the "
      "khronon's stress there is alpha_c a^2 ~ alpha_c/M^2 plus the regular part of mu): fractional shifts ~ alpha_c <= 3e-9 "
      "(current ringdown tests ~10%); whatever happens at the universal horizon (B3) is inside both the Killing and the spin-0 "
      "horizons and cannot reach the ringdown (at alpha_c = 0 the QNMs are exactly GR's: Franchini et al. 2021)",
      "O(alpha_c) <= 3.2e-9", True, load_bearing=False)

# ================================================================================================ B5 criterion B
banner("B5  THE KHRONON INSIDE BLACK HOLES, THE UNIVERSAL HORIZON AND CRITERION B (reported)")
check("B5 (reported) CRITERION B: (i) the exterior leaves never enter r < 3M/2: the universal horizon is the leaf at tau = +oo "
      "(reparametrizable, tau -> -exp(-kappa_UH tau), kappa_UH = 1.0886/r_s = 0.544/M), so a global time function exists on "
      "the exterior and extends across the universal horizon to the interior family of leaves that end on r = 0; (ii) no signal "
      "of any speed (khronon, leafwise-instantaneous MOND constraint, heat filter, leaf average) crosses r = 3M/2 outward -- the "
      "universal horizon censors all speeds; (iii) between r = 3M/2 and 2M (inside the Killing horizon) the fast khronon "
      "(c_s ~ alpha_c^(-1/2) c) and the leafwise-instantaneous channels DO reach the exterior -- allowed by criterion B; (iv) "
      "criterion B's well-posedness clause is NOT established at alpha_c > 0, c_2 = oo: first-order fields diverge at the "
      "universal horizon (B3), which bounds the exterior evolution; each exterior leaf carries the log growth along its "
      "infinitely long throat", "structure derived in K1, K4, B1-B3", True, load_bearing=False)

LEDGER = [
    ("XR25-C1", "static and moving neutron stars carry regular, unique CMC/maximal leaves (no singular point: N > 0)", "DERIVED", "N1, N2"),
    ("XR25-C2", "black holes: the regular stationary CMC foliation is the C_crit one; its leaves stop at the limit surface r = 3M/2, "
                "a universal horizon (kappa_UH = 0.544/M); Kottler's CMC value shifts it by ~1e-22", "DERIVED", "K1, B1"),
    ("XR25-C3", "at alpha_c = 0 moving black holes are regular (C^1 aether at the universal horizon), the khronon stealth", "DERIVED",
     "K3, B2 (KS 2023, RB 2019 reproduced)"),
    ("XR25-C4", "at alpha_c > 0, c_2 = oo: the first-order multiplier is log-divergent at the universal horizon (mu ~ 0.257 "
                "(alpha_c/M) ln), a curvature singularity at O(alpha_c)", "FAILS (first order)", "B3"),
    ("XR25-C5", "the regularity of the universal horizon beyond first order (the spin-0 layer ~ (3/4) sqrt(alpha_c) M) at c_2 = oo", "OPEN", "B3"),
    ("XR25-C6", "FP14's 'c_2 -> oo is regular' covers Minkowski and FRW, not black holes: at finite c_2 the static decoupled "
                "solutions force U''(xi_*) = 0 and are regular", "CONSTRAINT", "B3, K2"),
    ("XR25-C7", "ringdown GR's to O(alpha_c); criterion B's causal clauses hold, its well-posedness clause is open at the "
                "universal horizon", "DERIVED / OPEN", "B4, B5"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:9s} {st_:20s} {what}  --  {why}")
L.out["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
L.finish()
