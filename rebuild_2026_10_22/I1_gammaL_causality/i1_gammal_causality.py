#!/usr/bin/env python3
"""I1_gammaL_causality: causal structure of v4 = AeST (SZ21) + capped F + stiffness -(gamma_L/2K^2)(q^{mn} D_m D_n phi + theta Q)^2.

Frozen criteria: FROZEN_CRITERIA.md (+ AMENDMENT A1, pre-result). One line per check; ends 'I1_GAMMAL_CAUSALITY COMPLETE: N/M'.
External input on disk (outside the repo): ../_external_data/aest_papers_2026_10_22/src_2007.00082/newRMONDLett.tex,
eq. Minkowski_action and the dispersion relations stated after it.
kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled.

Run: OMP_NUM_THREADS=1 nice -n 15 python3 i1_gammal_causality.py        (I1_MUTATE=1 for the mutation run)
"""
import json
import math
import os
import resource
import sys
import time

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.special import ellipe, ellipk

T0 = time.time()
MUTATE = os.environ.get("I1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
SG = -1 if MUTATE else 1            # mutation 1: gamma_L -> -gamma_L
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, f"i1_gammal_causality{TAG}.out")
JSON = os.path.join(HERE, f"i1_gammal_causality_results{TAG}.json")
mp.mp.dps = 50

c_SI = 2.99792458e8
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
AU = 1.495978707e11
G_SI = 6.67430e-11
MSUN = 1.98847e30
GMSUN = 1.32712440018e20
GMJUP = 1.26686534e17
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTARS = [24.0, 50.0, 90.0]
KBS = [0.05, 1.0]
CSS = [1.0, 0.1]
MUINV = [1.0, 10.0]

lines, checks, res = [], [], {"mutate": MUTATE}


def log(s):
    print(s, flush=True)
    lines.append(s)


def check(kid, ok, value, thr):
    checks.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr})
    log(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


# ============================================================================ K1: covariant linearisation
t, x, y, z = sp.symbols("t x y z", real=True)
X4 = (t, x, y, z)
eps, Q0 = sp.symbols("epsilon Q_0", positive=True)
ETA = sp.diag(-1, 1, 1, 1)


def stiff_scalar(g, ginv, A_lo, phi, proj="q"):
    """(q^{mn} nabla_m nabla_n phi + theta Q); proj='g' replaces q^{mn} by g^{mn} (K8a partner)."""
    dg = [[[sp.diff(g[a, b], X4[c]) for c in range(4)] for b in range(4)] for a in range(4)]
    Gam = [[[sum(ginv[l, s_] * (dg[s_][m][n] + dg[s_][n][m] - dg[m][n][s_]) for s_ in range(4)) / 2
             for n in range(4)] for m in range(4)] for l in range(4)]
    dphi = [sp.diff(phi, X4[m]) for m in range(4)]
    hess = [[sp.diff(phi, X4[m], X4[n]) - sum(Gam[l][m][n] * dphi[l] for l in range(4)) for n in range(4)] for m in range(4)]
    A_up = [sum(ginv[m, n] * A_lo[n] for n in range(4)) for m in range(4)]
    q = sp.Matrix(4, 4, lambda m, n: ginv[m, n] + (A_up[m] * A_up[n] if proj == "q" else 0))
    trace = sum(q[m, n] * hess[m][n] for m in range(4) for n in range(4))
    theta = sum(sp.diff(A_up[m], X4[m]) for m in range(4)) + sum(Gam[m][m][l] * A_up[l] for m in range(4) for l in range(4))
    Q = sum(A_up[m] * dphi[m] for m in range(4))
    return trace + theta * Q


def first_order(expr):
    return sp.expand(sp.diff(expr, eps).subs(eps, 0))


# Minkowski, general H_{mn}, general aether a_i, scalar varphi
Hf = [[None] * 4 for _ in range(4)]
for a_ in range(4):
    for b_ in range(a_, 4):
        Hf[a_][b_] = Hf[b_][a_] = sp.Function(f"H{a_}{b_}")(*X4)
H = sp.Matrix(4, 4, lambda a_, b_: Hf[a_][b_])
g_M = ETA + eps * H
ginv_M = ETA - eps * ETA * H * ETA
af = [sp.Function(f"a{i}")(*X4) for i in (1, 2, 3)]
vp = sp.Function("varphi")(*X4)
A_lo_M = [-1 + eps * Hf[0][0] / 2] + [eps * af[i] for i in range(3)]
phi_M = Q0 * t + eps * vp
unit = first_order(sum(ginv_M[m, n] * A_lo_M[m] * A_lo_M[n] for m in range(4) for n in range(4)))
X1 = first_order(stiff_scalar(g_M, ginv_M, A_lo_M, phi_M))
# A_lo_i = eps*a_i is the lower spatial aether component, so V_i = d_i varphi + Q0 A_lo_i (SZ21 split)
divV_lo = sum(sp.diff(sp.diff(vp, X4[i + 1]) + Q0 * af[i], X4[i + 1]) for i in range(3))
r1_lo = sp.simplify(X1 - divV_lo)
has_dt = any(isinstance(d_, sp.Derivative) and t in d_.variables for d_ in X1.atoms(sp.Derivative))
X0_M = sp.simplify(stiff_scalar(g_M, ginv_M, A_lo_M, phi_M).subs(eps, 0))

# FRW (flat), Newtonian gauge + general aether perturbation B_i, background phi(t)
aa = sp.Function("a")(t)
phib = sp.Function("phibar")(t)
Psi, Phi = sp.Function("Psi")(*X4), sp.Function("Phi")(*X4)
Bf = [sp.Function(f"B{i}")(*X4) for i in (1, 2, 3)]
g_F = sp.diag(-(1 + 2 * eps * Psi), *([aa ** 2 * (1 - 2 * eps * Phi)] * 3))
ginv_F = sp.diag(-(1 - 2 * eps * Psi), *([(1 + 2 * eps * Phi) / aa ** 2] * 3))
A_lo_F = [-(1 + eps * Psi)] + [eps * Bf[i] for i in range(3)]
phi_F = phib + eps * vp
XF = stiff_scalar(g_F, ginv_F, A_lo_F, phi_F)
XF0 = sp.simplify(XF.subs(eps, 0))
XF1 = sp.simplify(first_order(XF))
dt_vp_F = any(isinstance(d_, sp.Derivative) and d_.expr == vp and t in d_.variables for d_ in XF1.atoms(sp.Derivative))
dt_any_F = sorted({str(d_) for d_ in XF1.atoms(sp.Derivative) if t in d_.variables})
res["K1"] = {"unit_norm_first_order": str(sp.simplify(unit)), "minkowski_X0": str(X0_M), "minkowski_X1": str(X1),
             "residual_vs_div(d varphi + Q0 A_lo)": str(r1_lo), "minkowski_has_time_derivative": has_dt,
             "frw_X0": str(XF0), "frw_X1": str(XF1), "frw_X1_has_dt_varphi": dt_vp_F, "frw_X1_time_derivatives": dt_any_F}
log(f"  K1 Minkowski first order: {X1}")
log(f"  K1 FRW background: {XF0}; FRW first order: {XF1}")
check("K1", sp.simplify(unit) == 0 and X0_M == 0 and r1_lo == 0 and not has_dt and XF0 == 0 and not dt_vp_F,
      f"unit-norm residual {sp.simplify(unit)}; Minkowski X0 {X0_M}; X1 - div(grad varphi + Q0 A_i) = {r1_lo}; "
      f"d_t in X1: {has_dt}; FRW X0 {XF0}; d_t varphi in FRW X1: {dt_vp_F} (other d_t: {dt_any_F})",
      "all residuals 0 and no d_t (Minkowski); FRW background 0, no d_t varphi")

# ============================================================================ K2: own scalar operator (SZ21 + stiffness)
KB, K2c, lam, Ls = sp.symbols("K_B K_2 lambda L_s", real=True)
w, k = sp.symbols("omega k", positive=True)
cA, cB = sp.symbols("cA0:4"), sp.symbols("cB0:4")


def quad_matrix(Lfun, nf):
    """Plane-wave matrix: fields f_a = cA_a E + cB_a conj(E), E = exp(i(k z - w t)); M_ab = coeff of cA_a cB_b
    in the E-independent (time-averaged) part of L."""
    E = sp.exp(sp.I * (k * z - w * t))
    flds = [cA[i] * E + cB[i] / E for i in range(nf)]
    L = sp.expand(sp.powsimp(sp.expand(Lfun(flds))))
    L0 = sp.Add(*[term for term in L.as_ordered_terms() if not term.has(sp.exp)])
    M = sp.zeros(nf, nf)
    for i in range(nf):
        for j in range(nf):
            M[i, j] = sp.simplify(L0.coeff(cA[i]).coeff(cB[j]))
    return M


def sz_L(flds, stiff=True):
    Psi_, Phi_, al_, vp_ = flds
    hup = sp.diag(-2 * Psi_, -2 * Phi_, -2 * Phi_, -2 * Phi_)
    A = [sp.diff(al_, v) for v in (x, y, z)]
    hlo = ETA * hup * ETA
    htr = sum(ETA[m, m] * hup[m, m] for m in range(4))
    d = lambda f, m: sp.diff(f, X4[m])
    up = lambda m: ETA[m, m]
    L = -sp.Rational(1, 2) * sum(d(htr, m) * d(hup[m, n], n) for m in range(4) for n in range(4))
    L += sp.Rational(1, 4) * sum(up(r) * d(htr, r) ** 2 for r in range(4))
    L += sp.Rational(1, 2) * sum(d(hup[m, r], m) * d(hup[n, s_], n) * ETA[s_, r] for m in range(4) for n in range(4)
                                 for r in range(4) for s_ in range(4))
    L += -sp.Rational(1, 4) * sum(up(r) * d(hup[m, n], r) * d(hlo[m, n], r) for r in range(4) for m in range(4) for n in range(4))
    Ev = [d(A[i], 0) - d(hup[0, 0], i + 1) / 2 for i in range(3)]
    V = [d(vp_, i + 1) + Q0 * A[i] for i in range(3)]
    L += KB * sum(e ** 2 for e in Ev)
    L += (2 - KB) * (2 * sum(Ev[i] * V[i] for i in range(3)) - (1 + lam) * sum(v ** 2 for v in V))
    L += 2 * K2c * (d(vp_, 0) + Q0 * hup[0, 0] / 2) ** 2
    if stiff:
        L += -SG * (2 - KB) * Ls ** 2 / 2 * sum(d(V[i], i + 1) for i in range(3)) ** 2
    return L


Ms = quad_matrix(sz_L, 4)
det = sp.factor(Ms.det())
deg = sp.Poly(sp.numer(sp.together(det)), w).degree()
wsq = sp.Symbol("W2")
detW = sp.factor(sp.numer(sp.together(det)).subs(w, sp.sqrt(wsq)))
sols = [s_ for s_ in sp.solve(detW, wsq) if sp.simplify(s_) != 0]
w2_closed = ((2 - KB) * (1 + KB * lam / 2) * k ** 2 / (K2c * KB) + (2 - KB) * (1 + lam) * Q0 ** 2 / KB
             + (2 - KB) * Ls ** 2 * Q0 ** 2 * k ** 2 / (2 * KB) + (2 - KB) * Ls ** 2 * k ** 4 / (4 * K2c))
if MUTATE:
    w2_closed_ref = w2_closed.subs(Ls ** 2, -Ls ** 2)
else:
    w2_closed_ref = w2_closed
r2 = [sp.simplify(s_ - w2_closed_ref) for s_ in sols]
res["K2"] = {"det": str(det), "deg_omega": deg, "nonzero_w2_roots": [str(s_) for s_ in sols],
             "C5_H10_closed_form": str(w2_closed), "residuals": [str(r) for r in r2]}
log(f"  K2 nonzero w^2 root(s): {sols}")
check("K2", deg == 4 and len(sols) == 1 and r2[0] == 0, f"det degree in omega {deg}; residual vs C5 H10 closed form {r2}",
      "degree 4 AND residual 0")
W2 = sols[0]

# ============================================================================ K3: aether slicing (Petrovskii)
s_, l_ = sp.symbols("s l", positive=True)      # K_B = 2s/(1+s) in (0,2); lambda = l >= 0 (l > 0 and l = 0 both checked)
Wp = sp.expand(W2.subs(KB, 2 * s_ / (1 + s_)))
K2p, Lp, Qp = sp.symbols("K2p Lp Qp", positive=True)
Wp = Wp.subs({K2c: K2p, Ls: Lp, Q0: Qp})
terms_pos = []
for lv in (l_, 0):
    Wl = sp.expand(Wp.subs(lam, lv))
    poly = sp.Poly(Wl, k)
    coeffs = [sp.simplify(cf) for cf in poly.coeffs()]
    terms_pos.append(all(sp.simplify(cf).is_nonnegative for cf in coeffs))
A_lim = sp.simplify(sp.limit(W2 / k ** 4, k, sp.oo))
A_expect = SG * (2 - KB) * Ls ** 2 / (4 * K2c)
A_pos = sp.simplify(A_lim.subs({KB: 2 * s_ / (1 + s_), K2c: K2p, Ls: Lp})).is_positive
res["K3"] = {"coefficients_nonnegative(lambda=l>0, lambda=0)": terms_pos, "A=lim w^2/k^4": str(A_lim),
             "A_expected": str(A_expect), "A_positive": bool(A_pos),
             "reading": "aether slicing: w^2 = A k^4 + B k^2 + M^2 real and >= 0 at every k -> Im w = 0 (Petrovskii-correct, "
                        "time-reversible, dispersive: beam/Schroedinger type); group speed 2 sqrt(A) k unbounded"}
log(f"  K3 A = lim w^2/k^4 = {A_lim}")
check("K3", all(terms_pos) and bool(A_pos) and sp.simplify(A_lim - A_expect) == 0,
      f"all k-coefficients of w^2 nonnegative (lambda>0, lambda=0): {terms_pos}; A = {A_lim} > 0: {A_pos}",
      "every w^2 root real >= 0 AND A > 0")

# ============================================================================ K4: tilted slicing
Om, kap, wv, Ac, Bc, Mc, cth = sp.symbols("Omega kappa w A B M c_theta", real=True)
gam = 1 / sp.sqrt(1 - wv ** 2)
kx = kap * cth
s_t = gam * (Om - wv * kx)
p2_t = -Om ** 2 + kap ** 2 + s_t ** 2                    # q^{mn}k_m k_n = eta k k + (u.k)^2
f_t = sp.expand(s_t ** 2 - Ac * p2_t ** 2 - Bc * p2_t - Mc ** 2)
# (b) kappa perp w: p^2 = kappa^2 + w^2 s^2
Xs = sp.Symbol("X")
p2_perp = sp.simplify(p2_t.subs(cth, 0).subs(Om, Xs / gam))
r4b = sp.simplify(p2_perp - (kap ** 2 + wv ** 2 * Xs ** 2))
Yq = sp.Symbol("Y")
quadY = sp.expand(Ac * wv ** 2 * Yq ** 2 + (Bc * wv ** 2 - 1) * Yq + (kap ** 2 + Mc ** 2 * wv ** 2))
r4b2 = sp.simplify(sp.expand((Xs ** 2 - Ac * p2_perp ** 2 - Bc * p2_perp - Mc ** 2) * (-wv ** 2)).subs(Xs ** 2, (Yq - kap ** 2) / wv ** 2) - quadY)
kc2 = (1 - Bc * wv ** 2) ** 2 / (4 * Ac * wv ** 2) - Mc ** 2 * wv ** 2
# (a) w = 0 real roots and (c) numeric scan
num = dict(A=mp.mpf(1), B=mp.mpf("0.3"), M=mp.mpf("0.1"), w=mp.mpf("1e-3"))


def roots_tilt(kv, th, wnum):
    fe = f_t.subs({Ac: num["A"], Bc: num["B"], Mc: num["M"], wv: wnum, kap: kv, cth: sp.cos(th)})
    P = sp.Poly(sp.expand(fe), Om)
    cs = [mp.mpf(sp.N(cf, 60)) if sp.im(sp.N(cf, 60)) == 0 else mp.mpc(sp.N(cf, 60)) for cf in P.all_coeffs()]
    return mp.polyroots(cs, maxsteps=400, extraprec=400)


real0 = []
for kv in (sp.Rational(1, 10), 10, 1000):
    rr = roots_tilt(kv, 0, 0)
    real0.append(max(abs(mp.im(r)) for r in rr))
kcn = mp.sqrt(kc2.subs({Ac: 1, Bc: sp.Rational(3, 10), Mc: sp.Rational(1, 10), wv: sp.Rational(1, 1000)}).evalf(50))
kbig = 1000 * kcn
ratios = {}
for th in [i * sp.pi / 12 for i in range(7)]:
    rr = roots_tilt(sp.Float(kbig, 50), th, sp.Rational(1, 1000))
    gm = 1 / mp.sqrt(1 - mp.mpf("1e-6"))
    ratios[f"{float(th):.3f}"] = float(max(abs(mp.im(r)) for r in rr) / (kbig / (gm * mp.mpf("1e-3"))))
# just below / above kappa_c (perp)
below = max(abs(mp.im(r)) for r in roots_tilt(sp.Float(kcn * mp.mpf("0.99"), 50), sp.pi / 2, sp.Rational(1, 1000)))
above = max(abs(mp.im(r)) for r in roots_tilt(sp.Float(kcn * mp.mpf("1.01"), 50), sp.pi / 2, sp.Rational(1, 1000)))
mx = max(ratios.values())
res["K4"] = {"p2_perp_residual": str(r4b), "Y_quadratic_residual": str(r4b2), "kappa_c^2": str(kc2),
             "w0_max_Im": [float(v) for v in real0], "kappa_c_numeric(A=1,B=.3,M=.1,w=1e-3)": float(kcn),
             "Im_ratio_at_1e3_kc_by_angle(rad)": ratios, "max_Im_just_below_kc": float(below), "max_Im_just_above_kc": float(above),
             "reading": "Im Omega -> kappa/(gamma w) above kappa_c ~ 1/(2 sqrt(A) w): unbounded, linear in kappa (Hadamard ill-posed, "
                        "Laplace-like) on any slice tilted by w != 0 relative to the aether"}
log(f"  K4 kappa_c^2 = {kc2}; Im/(kappa/(gamma w)) by angle: {ratios}; below/above kc: {float(below):.3g}/{float(above):.3g}")
check("K4", r4b == 0 and r4b2 == 0 and max(real0) < 1e-30 and below < 1e-30 and above > 0 and abs(mx - 1) < 1e-2,
      f"p2 residual {r4b}, Y-quadratic residual {r4b2}; w=0 max|Im| {float(max(real0)):.2g}; |Im| just below/above kc "
      f"{float(below):.2g}/{float(above):.3g}; max Im ratio over 7 directions {mx:.6f}",
      "(a) real at w=0, (b) complex iff kappa > kappa_c, (c) max ratio within 1e-2 of 1")

# ============================================================================ K5: twist forced
yy, thh, hh, lF, rr_ = sp.symbols("y theta h ell_F r", positive=True)
Mresp = sp.diag(1 + yy, 1 + yy, (1 + yy) ** (1 if MUTATE else 2))
khat = sp.Matrix([sp.sin(thh), 0, sp.cos(thh)])
Pi = sp.eye(3) - khat * khat.T
vecT = Pi * Mresp * khat
r5a = sp.simplify(sp.simplify(vecT.dot(vecT)) - ((1 + yy) * yy * sp.sin(thh) * sp.cos(thh)) ** 2)
# (b) Cartesian check of the toroidal particular solution
Xc, Yc, Zc = sp.symbols("X Y Z", real=True)
Rc = sp.sqrt(Xc ** 2 + Yc ** 2 + Zc ** 2)
Cc = -(1 + yy) * yy * hh / (2 * lF ** 2)
Om_c = [Cc * Zc / Rc * (-Yc), Cc * Zc / Rc * Xc, 0]                      # C r sin cos phi_hat = C (z/r)(-y, x, 0)
S_c = [(1 + yy) * yy * hh * Zc / Rc ** 3 * (-Yc), (1 + yy) * yy * hh * Zc / Rc ** 3 * Xc, 0]
lap = lambda f: sum(sp.diff(f, v, 2) for v in (Xc, Yc, Zc))
r5b = [sp.simplify(lap(Om_c[i]) - 2 / lF ** 2 * S_c[i]) for i in range(3)]
# source: curl(M dV_L) for dV_L = h rhat with M = (1+y)(I + y zz)
dVL = [hh * v / Rc for v in (Xc, Yc, Zc)]
MdV = [(1 + yy) * dVL[0], (1 + yy) * dVL[1], (1 + yy) * (1 + (yy if not MUTATE else 0)) * dVL[2]]
curl = [sp.diff(MdV[2], Yc) - sp.diff(MdV[1], Zc), sp.diff(MdV[0], Zc) - sp.diff(MdV[2], Xc), sp.diff(MdV[1], Xc) - sp.diff(MdV[0], Yc)]
r5c = [sp.simplify(curl[i] - S_c[i]) for i in range(3)]
res["K5"] = {"|Pi M khat|^2 - ((1+y)y sin cos)^2": str(r5a), "toroidal_ODE_residual": [str(v) for v in r5b],
             "curl(M dV_L) - source residual": [str(v) for v in r5c],
             "transverse_equation": "(ell_F^2/2) curl curl V_T + M_T V_T = -Pi(M dV); a_T = V_T/Q0; ell_F^2 = 2K_B/((2-K_B)Q0^2)",
             "solar_solution": "curl V_T = -(1+y) y h r sin(theta) cos(theta)/(2 ell_F^2) phi_hat (r << L*, ell_F; h = GM/L*^2)"}
check("K5", r5a == 0 and all(v == 0 for v in r5b) and all(v == 0 for v in r5c),
      f"|Pi M khat|^2 residual {r5a}; toroidal solution residual {r5b}; source residual {r5c}",
      "all residuals 0 (twist forced by the anisotropic capped-F response)")

# ============================================================================ K6: ray loop identity
a1, a2, a3, e1, e2, e3, vv, dtau = sp.symbols("a1 a2 a3 e1 e2 e3 v dtau", real=True)
e0 = sp.Symbol("e0")
u_lo = [-1, a1, a2, a3]
e0sol = sp.solve(sp.Eq(-e0 * 1 * (-1) * (-1) + a1 * e1 + a2 * e2 + a3 * e3, 0), e0)[0]  # u_mu e^mu = -e0 + a.e = 0
dt_ray = dtau * (1 + vv * e0sol)
dx_ray = [dtau * (av + vv * ev) for av, ev in ((a1, e1), (a2, e2), (a3, e3))]
r6 = sp.expand(dt_ray - (dtau + a1 * dx_ray[0] + a2 * dx_ray[1] + a3 * dx_ray[2]) + dtau * (a1 ** 2 + a2 ** 2 + a3 ** 2))
check("K6", sp.simplify(e0sol - (a1 * e1 + a2 * e2 + a3 * e3)) == 0 and r6 == 0,
      f"e0 = {e0sol}; dt - (dtau + a.dx) = O(a^2) residual {r6}",
      "residual 0 -> Delta t = l/v + loop integral of a.dx")

# ============================================================================ K7: magnitudes (illustrative Galaxy)
Rs, Zs, GMs, aMN, bMN = sp.symbols("R Z GM aMN bMN", positive=True)
PhiMN = -GMs / sp.sqrt(Rs ** 2 + (aMN + sp.sqrt(Zs ** 2 + bMN ** 2)) ** 2)
gR, gZ = -sp.diff(PhiMN, Rs), -sp.diff(PhiMN, Zs)
gN = sp.sqrt(gR ** 2 + gZ ** 2)
gL = (gN + sp.sqrt(gN ** 2 + 4 * gN)) / 2          # law g_N = g^2/(g + a0), a0 = 1
nu = gL / gN
S_phi = sp.diff(nu, Zs) * gR - sp.diff(nu, Rs) * gZ  # (grad nu x g_N)_phi
S_num = sp.lambdify((Rs, Zs, GMs, aMN, bMN), S_phi, "numpy")


def ring_kernel(R, Z, Rp, Zp):
    """int_0^{2pi} cos(phi')/|x - x'| dphi' for target (R, 0, Z) and ring (Rp, Zp)."""
    den = (R + Rp) ** 2 + (Z - Zp) ** 2
    m = np.clip(4 * R * Rp / den, 1e-300, 1 - 1e-16)
    return 4 / np.sqrt(den) * ((2 - m) * ellipk(m) - 2 * ellipe(m)) / m


# sanity of ring kernel by quadrature
phq = np.linspace(0, 2 * np.pi, 200001)
Rt, Zt, Rpt, Zpt = 8.2, 0.3, 5.0, -0.4
quad = np.trapz(np.cos(phq) / np.sqrt(Rt ** 2 + Rpt ** 2 - 2 * Rt * Rpt * np.cos(phq) + (Zt - Zpt) ** 2), phq)
ring_err = abs(ring_kernel(Rt, Zt, Rpt, Zpt) - quad) / abs(quad)


def omega_field(targets, GMd, a_, b_, N):
    """J_d(target) = -(1/4pi) int S_phi I ring dR dZ R ; Omega_V = (2/ell_F^2)(a0/c^2) kpc J_d (units: kpc, a0)."""
    Re = np.concatenate([[0.0], np.geomspace(1e-3, 300.0, N)])
    Rm, dR = 0.5 * (Re[1:] + Re[:-1]), np.diff(Re)
    ze = 0.05 * np.sinh(np.linspace(0, np.arcsinh(300 / 0.05), N // 2 + 1))
    ze = np.concatenate([-ze[::-1], ze[1:]])
    Zm, dZ = 0.5 * (ze[1:] + ze[:-1]), np.diff(ze)
    RR, ZZ = np.meshgrid(Rm, Zm, indexing="ij")
    W = np.outer(dR * Rm, dZ)
    S = S_num(RR, ZZ, GMd, a_, b_)
    S = np.where(np.isfinite(S), S, 0.0)
    out = []
    for (Rt_, Zt_) in targets:
        out.append(-np.sum(S * ring_kernel(Rt_, Zt_, RR, ZZ) * W) / (4 * np.pi))
    return np.array(out)


SUN = (8.2, 0.02)
loopR = np.linspace(4.25, 11.75, 16)      # midpoints of [4,12] kpc
loopZ = np.linspace(0.125, 1.875, 8)      # midpoints of [0,2] kpc
loop_targets = [(r_, z_) for r_ in loopR for z_ in loopZ]
near_targets = [(r_, z_) for r_ in (7.7, 8.2, 8.7) for z_ in (0.02, 0.25, 0.5)]
gal = {}
for foot, a0v in A0.items():
    GMd = G_SI * 6e10 * MSUN / a0v / KPC ** 2
    Jsun = omega_field([SUN], GMd, 3.0, 0.28, 400)[0]
    Jsun2 = omega_field([SUN], GMd, 3.0, 0.28, 800)[0]
    Jloop = omega_field(loop_targets, GMd, 3.0, 0.28, 400)
    Jnear = omega_field(near_targets, GMd, 3.0, 0.28, 400)
    Jkuz = omega_field([SUN, (8.2, 0.5)], GMd, 3.0, 1e-9, 400)
    flux_d = np.sum(Jloop) * (0.5 * 0.25)     # kpc^2 * J
    gal[foot] = {"GM/a0_kpc2": GMd, "J_sun": Jsun, "J_sun_2x": Jsun2, "rel_change_2x": abs(Jsun2 / Jsun - 1),
                 "J_near_max": float(np.max(np.abs(Jnear))), "flux_d_kpc2": float(flux_d),
                 "J_kuzmin_(sun,z=0.5)": [float(v) for v in Jkuz], "J_MN_(8.2,0.5)": float(Jnear[5])}
    log(f"  K7 {foot}: J_d(Sun) = {Jsun:.4e} (2x grid {Jsun2:.4e}, rel {abs(Jsun2 / Jsun - 1):.3g}); near-Sun max {np.max(np.abs(Jnear)):.3e}; "
        f"loop flux {flux_d:.3e}; Kuzmin sanity {Jkuz}")

# physical grid
c2 = c_SI ** 2
grid = []
for foot, a0v in A0.items():
    xe = max(json.load(open(os.path.join(ROOT, "covariant_push_2026_10_22/C5_health/c5_health_results.json")))["x_e_D7d"][foot])
    G = gal[foot]
    for KBv in KBS:
        for csv in CSS:
            for mui in MUINV:
                mu = 1 / (mui * MPC)
                Q0v = mu * csv * math.sqrt(KBv / 2)
                lF2 = 2 * KBv / ((2 - KBv) * Q0v ** 2)
                K2v = (2 - KBv) / (KBv * csv ** 2)
                for Lpc in LSTARS:
                    Lm = Lpc * PC
                    sqA = csv * math.sqrt(KBv) / 2 * Lm                   # sqrt(A) in m
                    B = csv ** 2 * (1 + KBv * ((1 + xe) ** 2 - 1) / 2)
                    conv = 2 * a0v / c2 * KPC / lF2                         # Omega_V [1/m^2] per unit J_d
                    Om_sun_gal = abs(G["J_sun"]) * conv / Q0v               # aether twist [1/m]
                    Om_near = G["J_near_max"] * conv / Q0v
                    h = GMSUN / c2 / Lm ** 2
                    R100 = 100 * AU
                    Om_sun_own = (1 + xe) * xe * h * R100 / (4 * lF2) / Q0v
                    w100 = (Om_sun_gal + Om_sun_own) * R100 / 2
                    w1k = Om_near * KPC / 2
                    out = {"foot": foot, "K_B": KBv, "c_s": csv, "mu_inv_Mpc": mui, "Lstar_pc": Lpc, "Q0_per_m": Q0v,
                           "ell_F_Mpc": math.sqrt(lF2) / MPC, "K2": K2v, "sqrtA_m": sqA, "x_e": xe}
                    for lab, wt in (("100AU", w100), ("1kpc", w1k)):
                        kc = (1 - B * wt ** 2) / (2 * sqA * wt)
                        kk_ = 2 * kc
                        D = (1 - B * wt ** 2) ** 2 - 4 * sqA ** 2 * wt ** 2 * kk_ ** 2
                        Y = ((1 - B * wt ** 2) + 1j * math.sqrt(-D)) / (2 * sqA ** 2 * wt ** 2)
                        Xr = np.sqrt((Y - kk_ ** 2) / wt ** 2)
                        out[f"w_{lab}"] = wt
                        out[f"kappa_c_{lab}_per_m"] = kc
                        out[f"lambda_c_{lab}_m"] = 2 * math.pi / kc
                        out[f"rate_2kc_{lab}_per_s"] = abs(Xr.imag) * c_SI
                    flux_a = G["flux_d_kpc2"] * conv * KPC ** 2 / Q0v      # Delta t in metres
                    ell_loop = 20 * KPC
                    vneed = ell_loop / abs(flux_a)
                    out.update(dt_gal_loop_s=abs(flux_a) / c_SI, v_needed_gal_c=vneed,
                               lambda_needed_gal_m=2 * math.pi / (vneed / (2 * sqA)))
                    dt_ss = Om_sun_gal * R100 ** 2 + (1 + xe) * xe * h * R100 ** 3 / (12 * lF2 * Q0v)
                    out.update(dt_ss_loop_s=dt_ss / c_SI, v_needed_ss_c=4 * R100 / dt_ss,
                               lambda_needed_ss_m=2 * math.pi / ((4 * R100 / dt_ss) / (2 * sqA)))
                    out["vg_lab_1km_c"] = 2 * sqA / 1e3
                    grid.append(out)
res["K7"] = {"galaxy_model": "Miyamoto-Nagai M=6e10 Msun, a=3 kpc, b=0.28 kpc (ILLUSTRATIVE); law pointwise along g_N",
             "ring_kernel_rel_err": float(ring_err), "galaxy": gal, "grid": grid}
rng = lambda key: (min(g_[key] for g_ in grid), max(g_[key] for g_ in grid))
summ = {kk: rng(kk) for kk in ("w_100AU", "w_1kpc", "lambda_c_100AU_m", "lambda_c_1kpc_m", "rate_2kc_100AU_per_s",
                               "rate_2kc_1kpc_per_s", "dt_gal_loop_s", "v_needed_gal_c", "lambda_needed_gal_m",
                               "dt_ss_loop_s", "lambda_needed_ss_m", "vg_lab_1km_c")}
ref = [g_ for g_ in grid if g_["foot"] == "canonical" and g_["K_B"] == 0.05 and g_["c_s"] == 1.0 and g_["mu_inv_Mpc"] == 1.0 and g_["Lstar_pc"] == 24.0][0]
res["K7"]["summary_ranges"] = summ
res["K7"]["reference_point(canonical,K_B=.05,c_s=1,mu^-1=1Mpc,L*=24pc)"] = ref
for kk, v in summ.items():
    log(f"  K7 range {kk}: {v[0]:.3g} .. {v[1]:.3g}")
log(f"  K7 reference point: {json.dumps({k_: (f'{v:.3g}' if isinstance(v, float) else v) for k_, v in ref.items()})}")
k7ok = all(gal[f]["rel_change_2x"] < 0.10 for f in gal)
check("K7", k7ok and ring_err < 1e-6,
      f"Omega at Sun, grid x2 rel change: canonical {gal['canonical']['rel_change_2x']:.3g}, alt {gal['alt']['rel_change_2x']:.3g}; "
      f"ring kernel vs quadrature {ring_err:.2g}", "< 0.10 (and ring kernel < 1e-6)")

# ============================================================================ K8: completions
# (a) q -> g in the stiffness: static part identical
X1g = first_order(stiff_scalar(g_M, ginv_M, A_lo_M, phi_M, proj="g"))
static = {f: f.func(x, y, z) for f in [vp] + af + [Hf[a_][b_] for a_ in range(4) for b_ in range(a_, 4)]}
X1g_st = sp.simplify(X1g.subs(static).doit())
X1_st = sp.simplify(X1.subs(static).doit())
r8a = sp.simplify(X1g_st - X1_st)
X1g_dt = sorted({str(d_) for d_ in X1g.atoms(sp.Derivative) if t in d_.variables})
# reduced scalar symbols: L(w) = 2K2 w^2 - B k^2 - m^2 - beta (k^2 - w^2)^2 ; beta = 2 K2 A
wn = sp.Symbol("wn")
K2n, Bn, mn, An, kn = 1, sp.Rational(1, 2), sp.Rational(1, 10), 1, 10
beta_n = 2 * K2n * An
Lg = 2 * K2n * wn ** 2 - Bn * kn ** 2 - mn ** 2 - beta_n * (kn ** 2 - wn ** 2) ** 2
krein_a = []
for r_ in sp.Poly(sp.expand(Lg), wn).nroots(n=40):
    if abs(sp.im(r_)) < 1e-20 and sp.re(r_) > 0:
        krein_a.append((float(sp.re(r_)), float(sp.re(r_) * sp.diff(Lg, wn).subs(wn, sp.re(r_)))))
# (b) auxiliary sigma with eps (d sigma)^2/2
aux = {}
for epsv in (sp.Rational(1, 100), -sp.Rational(1, 100)):
    for kv in (10, 100, 1000):
        Mm = sp.Matrix([[2 * K2n * wn ** 2 - Bn * kv ** 2 - mn ** 2, -kv ** 2], [-kv ** 2, 1 / sp.Integer(beta_n) + epsv * (wn ** 2 - kv ** 2)]])
        dd = sp.Poly(sp.expand(Mm.det()), wn)
        rts = dd.nroots(n=40)
        maxim = max(abs(float(sp.im(r_))) for r_ in rts)
        kr = []
        for r_ in rts:
            if abs(sp.im(r_)) < 1e-20 and sp.re(r_) > 0:
                Mr = Mm.subs(wn, sp.re(r_))
                vnull = sp.Matrix([-Mr[0, 1], Mr[0, 0]]) if abs(Mr[0, 0]) + abs(Mr[0, 1]) > 1e-30 else sp.Matrix([1, 0])
                kr.append(float(sp.re(r_) * (vnull.T * sp.diff(Mm, wn).subs(wn, sp.re(r_)) * vnull)[0]))
        aux[f"eps={epsv}|k={kv}"] = {"max_Im_w": maxim, "max_Im_w_over_k": maxim / kv, "krein_of_real_positive_roots": kr}
# static symbol change of (b): chi kernel -B k^2 - m^2 - k^4/(1/beta - eps k^2) vs -B k^2 - m^2 - beta k^4
res["K8"] = {"a_static_residual(q->g)": str(r8a), "a_time_derivatives_introduced": X1g_dt,
             "a_reduced_roots_and_krein(w, w dL/dw)": krein_a,
             "b_aux_sigma": aux,
             "b_static_kernel": "k^4/(1/beta - eps k^2): differs from beta k^4 at k^2 ~ 1/(eps beta) (changes the static law unless eps -> 0)"}
log(f"  K8a time derivatives introduced by q->g: {X1g_dt}")
log(f"  K8a reduced roots (w, Krein): {krein_a}")
log(f"  K8b aux sigma: {json.dumps(aux)}")
check("K8", r8a == 0, f"static part of (box phi + theta Q) - (q DD phi + theta Q) = {r8a}", "residual 0 (health reported)")

# ============================================================================ K9: criterion-A size
lab_sig = G_SI * 1000 / (24 * PC) ** 2 * (1.0 / 1000.0)
c8 = json.load(open(os.path.join(ROOT, "covariant_push_2026_10_22/C8_instantaneous/c8_instantaneous_results.json")))["signal_illustration"]["L24"]
r9 = abs(lab_sig / c8 - 1)
jup = {}
for Lpc in LSTARS:
    aP = GMJUP / (Lpc * PC) ** 2
    jup[f"{Lpc:.0f}pc"] = {"a_P_Jupiter": aP, "inst_minus_retarded": aP * (5.2 * AU / c_SI) * 2 * math.pi / (11.862 * 3.15576e7)}
galA = {f: a0v * 200e3 / c_SI for f, a0v in A0.items()}
res["K9"] = {"lab_signal_m_s2(L*=24pc)": lab_sig, "C8_value": c8, "rel": r9,
             "lab_signal_by_Lstar": {f"{L:.0f}pc": G_SI * 1000 / (L * PC) ** 2 * 1e-3 for L in LSTARS},
             "jupiter_hedgehog": jup, "galaxy_inst_minus_retarded_a0_v_over_c(v=200km/s)": galA}
check("K9", r9 < 1e-2, f"lab signal {lab_sig:.4g} m/s^2 vs C8 {c8:.2g} (rel {r9:.2g})", "< 1e-2")

# ============================================================================ verdict
cd = {c_["id"]: c_["pass"] for c_ in checks}
if not (cd["K1"] and cd["K2"]):
    verdict = "UNDECIDED"
elif not cd["K3"]:
    verdict = "ILL-POSED (everywhere)"
elif cd["K4"] and cd["K5"]:
    verdict = "ILL-POSED (where the aether twists)"
else:
    verdict = "WELL-POSED, CRITERION A VIOLATED / B MET"
res["verdict"] = verdict
log(f"  VERDICT (frozen rule): {verdict}")
npass = sum(c_["pass"] for c_ in checks)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
res.update(checks=checks, n_pass=npass, n_checks=len(checks), runtime_s=round(time.time() - T0, 1), max_rss_GB=round(rss, 3))
log(f"  runtime {time.time() - T0:.1f} s, max RSS {rss:.3f} GB")
log(f"I1_GAMMAL_CAUSALITY COMPLETE: {npass}/{len(checks)} checks PASS.")
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(0 if npass == len(checks) else 1)
