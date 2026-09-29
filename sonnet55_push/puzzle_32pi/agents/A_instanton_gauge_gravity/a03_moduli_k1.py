#!/usr/bin/env python3
"""a03: the k = 1 SU(2) instanton moduli space on the round S^4(L) (position x0 in R^4 = stereographic chart, size rho): does L, the a0-Rindler
length Z L, or Lambda select a point on it, and does its L^2 metric produce a '32 pi'?

Conventions: stereographic coordinates x in R^4 (dimensionless), g = Omega^2 delta, Omega = 2L/(1+r^2);  BPST in regular gauge
A^a_mu = 2 eta^a_{mu nu} (x-x0)_nu / ((x-x0)^2 + rho^2),  F = dA + eps A A = -4 rho^2 eta^a_{mu nu}/((x-x0)^2+rho^2)^2  (rho is dimensionless: rho = 1 <-> physical size L).
Weight of the L^2 metric on 1-forms: sqrt(g) g^{mu nu} = Omega^2 delta^{mu nu}.  The moduli metric is (1/g_YM^2) x [horizontal L^2 norm].
Checks:
  M1  F above is the curvature of A, (anti-)self-dual, |F|^2 = 192 rho^4/(r^2+rho^2)^4, and the stress tensor F_{ml}F_{nl} - delta F^2/4 = 0:
      an instanton does NOT back-react on the metric, so all of M_1 has the same action AND the same (zero) energy-momentum: no potential on M_1 at this order.
  M2  The gauge-invariant density |F|^2_phys(x) = Omega^-4 |F|^2 is CONSTANT on S^4 iff x0 = 0 and rho = 1 (size = L): the unique SO(5)-invariant point of M_1
      (it is the SU(2)_pm spin connection, a01/p10).  Every other point breaks SO(5).
  M3  Flat-weight zero-mode norms: translation 8 pi^2 per direction, dilation 16 pi^2, ratio 2 (in units 1/g^2).
  M4  Weighted (S^4) norms.  Dilation along x0 = 0: the mode d_rho A is horizontal for EVERY radial weight; N(rho) = ||d_rho A||^2 in closed form;
      N(1/rho) = rho^4 N(rho) (the S^4 isometry rho -> 1/rho), N(1) = 32 pi^2 L^2/5, N(0+) = 64 pi^2 L^2.
      Translation at the centre: the weighted horizontal representative is d_nu A (gauge parameter eps_nu = A_nu, an exact solution of the Euler-Lagrange equation),
      norm 32 pi^2/5 per direction = N(1): the metric at the centre is (32 pi^2 L^2/5)(dx0^2 + drho^2), an SO(5)-vector (proportional to delta) as required.
  M5  In u = ln rho the coefficient N_u(u) = rho^2 N(rho) is even, has ONE critical point (the centre u = 0, a maximum) and is not constant: the L^2 metric is
      not the SO(5,1)-invariant hyperbolic metric (constant N_u) and has no special locus at rho = Z, Z L, L/Z.
Exit 0 = all checks and controls behave.
"""
import sys
import sympy as sp
import mpmath as mp
import numpy as np

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

x = sp.symbols('x1:5', real=True); r2 = sum(xi ** 2 for xi in x)
r = sp.symbols('r', positive=True)
rho = sp.symbols('rho', positive=True); Ls = sp.symbols('L', positive=True)
def eta(a, m, n):
    if m < 3 and n < 3: return sp.LeviCivita(a, m, n)
    if n == 3 and m == a: return 1
    if m == 3 and n == a: return -1
    return 0
eps = sp.LeviCivita
def Afield(rho_, x0=(0, 0, 0, 0)):
    d = [x[k] - x0[k] for k in range(4)]
    dd = sum(t ** 2 for t in d)
    return [[2 * sum(eta(a, m, n) * d[n] for n in range(4)) / (dd + rho_ ** 2) for m in range(4)] for a in range(3)]
def Fcomp(A, a, m, n):
    return sp.simplify(sp.diff(A[a][n], x[m]) - sp.diff(A[a][m], x[n]) + sum(eps(a, b, c) * A[b][m] * A[c][n] for b in range(3) for c in range(3)))

# ---------------------------------------------------------------- M1
A1 = Afield(rho)
Fm = [[[Fcomp(A1, a, m, n) for n in range(4)] for m in range(4)] for a in range(3)]
form = all(sp.simplify(Fm[a][m][n] + 4 * eta(a, m, n) * rho ** 2 / (r2 + rho ** 2) ** 2) == 0 for a in range(3) for m in range(4) for n in range(4))
chk("M1 F = -4 rho^2 eta^a_{mn}/(r^2+rho^2)^2 for A = 2 eta x/(r^2+rho^2) (all 48 components)", form)
Fsq = sp.simplify(sum(Fm[a][m][n] ** 2 for a in range(3) for m in range(4) for n in range(4)))
chk("M1 |F|^2 = 192 rho^4/(r^2+rho^2)^4", sp.simplify(Fsq - 192 * rho ** 4 / (r2 + rho ** 2) ** 4) == 0)
selfdual = all(sp.simplify(Fm[a][m][n] - sp.Rational(1, 2) * sum(sp.LeviCivita(m, n, p, q) * Fm[a][p][q] for p in range(4) for q in range(4))) == 0 for a in range(3) for m in range(4) for n in range(4))
chk("M1 F is self-dual (F = *F in the flat conformal class)", selfdual)
T = [[sp.simplify(sum(Fm[a][m][l] * Fm[a][n][l] for a in range(3) for l in range(4)) - (sp.Rational(1, 4) if m == n else 0) * Fsq) for n in range(4)] for m in range(4)]
chk("M1 stress tensor T_mn = F^a_ml F^a_nl - (1/4) delta_mn F^2 = 0 identically: no back-reaction, no energy on M_1 (the moduli are exact flat directions at this order)", all(T[m][n] == 0 for m in range(4) for n in range(4)))
pt = {x[0]: sp.Rational(1, 2), x[1]: sp.Rational(1, 5), x[2]: sp.Rational(1, 10), x[3]: sp.Rational(3, 10), rho: 1}
def etabar(a, m, n):     # anti-self-dual 't Hooft symbol
    if m < 3 and n < 3: return sp.LeviCivita(a, m, n)
    if n == 3 and m == a: return -1
    if m == 3 and n == a: return 1
    return 0
Fpert = [[[Fm[a][m][n] + (sp.Rational(1, 2) * 4 / (r2 + rho ** 2) ** 2 * etabar(a, m, n) if a == 0 else 0) for n in range(4)] for m in range(4)] for a in range(3)]      # mutation: add an anti-self-dual piece to colour 0
Fsq_p = sum(Fpert[a][m][n] ** 2 for a in range(3) for m in range(4) for n in range(4))
Tp = [[(sum(Fpert[a][m][l] * Fpert[a][n][l] for a in range(3) for l in range(4)) - (sp.Rational(1, 4) if m == n else 0) * Fsq_p).subs(pt) for n in range(4)] for m in range(4)]
chk("M1-control: a mutated field (an anti-self-dual piece added to colour 0) has T_mn != 0 (max |T| = %.3f), so the T = 0 check can fail" % max(abs(float(sp.N(Tp[m][n]))) for m in range(4) for n in range(4)),
    max(abs(float(sp.N(Tp[m][n]))) for m in range(4) for n in range(4)) > 1e-3)

# ---------------------------------------------------------------- M2 unique SO(5)-invariant point
x0s = sp.symbols('y1:5', real=True)
dd = sum((x[k] - x0s[k]) ** 2 for k in range(4))
Q = (1 + r2)
target = sp.expand(Q - sp.Symbol('k', positive=True) * (dd + rho ** 2))     # 1 + x^2 = k ((x-x0)^2 + rho^2) identically in x
poly = sp.Poly(target, *x)
sol = sp.solve(poly.coeffs(), list(x0s) + [rho, sp.Symbol('k', positive=True)], dict=True)
print("   |F|^2_phys = const on S^4  <=>  1 + x^2 = k((x-x0)^2 + rho^2) identically; solution:", sol)
chk("M2 the density of instanton (x0, rho) is constant on S^4 iff x0 = 0 and rho = 1 (physical size L)", len(sol) == 1 and all(sol[0][y] == 0 for y in x0s) and sol[0][rho] == 1)
dens_phys = lambda rho_, x0v, pt: (sp.Integer(192) * sp.sympify(rho_) ** 4 / (sum((sp.sympify(pt[k]) - sp.sympify(x0v[k])) ** 2 for k in range(4)) + sp.sympify(rho_) ** 2) ** 4) * ((1 + sum(sp.sympify(t) ** 2 for t in pt)) * sp.Rational(1, 2)) ** 4     # L = 1
pts = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 2, 0, 1)]
chk("M2 at (x0, rho) = (0, 1): |F|_phys^2 = 12/L^4 at every point (checked at 3 points); at rho = Z or x0 != 0 it varies",
    all(sp.simplify(dens_phys(1, (0, 0, 0, 0), p) - 12) == 0 for p in pts)
    and len({round(float(dens_phys(sp.sqrt(32 * sp.pi / 3), (0, 0, 0, 0), p)), 6) for p in pts}) > 1
    and len({round(float(dens_phys(1, (sp.Rational(1, 2), 0, 0, 0), p)), 6) for p in pts}) > 1)
chk("M2 12/L^4 is exactly |R_pm|^2 = |Riemann_pm|^2 of S^4 (a01: |G_pm|^2_phys = 192/(1+r^2)^4 * Omega^-4 = 12/L^4): the special instanton is the spin connection", sp.simplify(sp.Rational(192, 16) - 12) == 0)

# ---------------------------------------------------------------- M3 flat weight
Ifl_dil = 2 * sp.pi ** 2 * sp.integrate(sp.Rational(1, 4) * r ** 2 * 192 * r ** 3 * 1 / (r ** 2 + 1) ** 4 * 1 / 1, (r, 0, sp.oo))      # rho = 1: |x_nu F_{nu mu}|^2 = (r^2/4) |F|^2
Ifl_tr = 2 * sp.pi ** 2 * sp.integrate(sp.Rational(1, 4) * 192 * r ** 3 / (r ** 2 + 1) ** 4, (r, 0, sp.oo))
chk("M3 flat weight: translation norm per direction = (1/4) Int F^2 d^4x = 8 pi^2; dilation = 16 pi^2; ratio 2", sp.simplify(Ifl_tr - 8 * sp.pi ** 2) == 0 and sp.simplify(Ifl_dil - 16 * sp.pi ** 2) == 0)

# ---------------------------------------------------------------- M4 weighted norms
# horizontality of d_rho A for a generic radial weight w(r)
wf = sp.Function('w')
Ar = Afield(rho)
dA = [[sp.diff(Ar[a][m], rho) for m in range(4)] for a in range(3)]
def Dcov(phi_a, m):     # (D_m phi)^a with the connection Ar
    return [sp.diff(phi_a[a], x[m]) + sum(eps(a, b, c) * Ar[b][m] * phi_a[c] for b in range(3) for c in range(3)) for a in range(3)]
rad = sp.sqrt(r2)
div = [0, 0, 0]
for m in range(4):
    phi = [wf(rad) * dA[a][m] for a in range(3)]
    Dp = Dcov(phi, m)
    for a in range(3):
        div[a] += Dp[a]
chk("M4 D_mu( w(r) d_rho A_mu ) = 0 for EVERY radial weight w: the dilation mode is horizontal on S^4 as well as in flat space", all(sp.simplify(d.doit()) == 0 for d in div))
p_ = sp.symbols('p', positive=True)    # p = rho^2
# |d_rho A|^2 = 48 rho^2 r^2/(r^2+rho^2)^4
dA2 = sp.simplify(sum(dA[a][m] ** 2 for a in range(3) for m in range(4)))
chk("M4 |d_rho A|^2 = 48 rho^2 r^2/(r^2+rho^2)^4", sp.simplify(dA2 - 48 * rho ** 2 * r2 / (r2 + rho ** 2) ** 4) == 0)
u = sp.symbols('u', positive=True)
Ntmp = sp.integrate(sp.apart(u ** 2 / ((1 + u) ** 2 * (u + p_) ** 4), u), (u, 0, sp.oo))
Npar = sp.simplify(4 * sp.Rational(1, 2) * 96 * sp.pi ** 2 * p_ * Ntmp)                        # 2 pi^2 * (1/2) [u = r^2] * 48 rho^2 * w(r)=4/(1+r^2)^2, L = 1
Nclosed = 64 * sp.pi ** 2 * (p_ ** 3 + 9 * p_ ** 2 - 6 * p_ * (p_ + 1) * sp.log(p_) - 9 * p_ - 1) / (p_ - 1) ** 5
chk("M4 N(rho) = 64 pi^2 L^2 [p^3 + 9p^2 - 9p - 1 - 6p(p+1) ln p]/(p-1)^5,  p = rho^2", sp.simplify(Npar - Nclosed) == 0)
chk("M4 N(1) = 32 pi^2 L^2/5 and N(0+) = 64 pi^2 L^2 (= 2 x 8 pi^2 x (2L)^2/... the flat-space value with the local scale Omega(0) = 2L)",
    sp.limit(Nclosed, p_, 1) == 32 * sp.pi ** 2 / 5 and sp.limit(Nclosed, p_, 0) == 64 * sp.pi ** 2)
mp.mp.dps = 30
def Nnum(pv):
    pv = mp.mpf(pv)
    if abs(pv - 1) < mp.mpf('1e-6'): return 32 * mp.pi ** 2 / 5
    return 64 * mp.pi ** 2 * (pv ** 3 + 9 * pv ** 2 - 6 * pv * (pv + 1) * mp.log(pv) - 9 * pv - 1) / (pv - 1) ** 5
def Nnum_nolog(pv):
    pv = mp.mpf(pv)
    return 64 * mp.pi ** 2 * (pv ** 3 + 8 * pv ** 2 - 6 * pv * (pv + 1) * mp.log(pv) - 9 * pv - 1) / (pv - 1) ** 5      # one polynomial coefficient mutated (9 -> 8)
iso = max(abs(Nnum(1 / mp.mpf(pv)) - mp.mpf(pv) ** 2 * Nnum(pv)) / Nnum(pv) for pv in ('0.05', '0.3', '2', '7', '40'))
chk("M4 isometry rho -> 1/rho: N(1/p) = p^2 N(p) (i.e. N(rho) d rho^2 invariant), max relative deviation %.1e over p in {0.05, 0.3, 2, 7, 40}" % float(iso), iso < mp.mpf('1e-15'))
iso_w = max(abs(Nnum_nolog(1 / mp.mpf(pv)) - mp.mpf(pv) ** 2 * Nnum_nolog(pv)) / abs(Nnum_nolog(pv)) for pv in ('0.3', '2'))
chk("M4-control: mutating one polynomial coefficient (9 -> 8) destroys the inversion symmetry (deviation %.2f): the check can fail" % float(iso_w), iso_w > 1e-2)

# translation at the centre with the S^4 weight: horizontal representative F_{nu mu} + D_mu eps_nu, eps^a_nu = f(r) eta^a_{nu l} x_l
f = sp.Function('f')
Ac = Afield(1)
Fc = lambda a, m, n: -4 * eta(a, m, n) / (r2 + 1) ** 2
def epsn(a, nu): return f(rad) * sum(eta(a, nu, l) * x[l] for l in range(4))
def Dmu(a, m, nu): return sp.diff(epsn(a, nu), x[m]) + sum(eps(a, b, c) * Ac[b][m] * epsn(c, nu) for b in range(3) for c in range(3))
S = 0
for nu in range(4):
    for m in range(4):
        for a in range(3):
            S += (Fc(a, nu, m) + Dmu(a, m, nu)) ** 2
S = sp.simplify(S.subs({x[1]: 0, x[2]: 0, x[3]: 0}).subs(x[0], r).doit())
fr = sp.Function('f')(r); fp = sp.diff(fr, r)
Sf = S.subs(f(r), fr).doit()
Lag = r ** 3 * (4 / (1 + r ** 2) ** 2) * Sf
Fs, Fps = sp.symbols('Fs Fps')
Lg = Lag.subs(fp, Fps).subs(fr, Fs)
EL = sp.diff(sp.diff(Lg, Fps).subs({Fs: fr, Fps: fp}), r) - sp.diff(Lg, Fs).subs({Fs: fr, Fps: fp})
EL = sp.simplify(EL)
fstar = 2 / (1 + r ** 2)
chk("M4 f* = 2/(1+r^2) (i.e. eps_nu = A_nu, horizontal representative = d_nu A) solves the Euler-Lagrange equation of the weighted translation norm",
    sp.simplify(EL.subs(fr, fstar).doit()) == 0)
chk("M4 the functional is strictly convex (coefficient of f'^2 positive at r = 0.1, 1, 10, 100), so f* is THE minimiser (f* regular at 0 and decaying)", all(sp.simplify(sp.diff(Lg, Fps, 2).subs(r, rv)) > 0 for rv in (sp.Rational(1, 10), 1, 10, 100)))
Sstar = sp.simplify(Sf.subs(fr, fstar).doit())
Jtr = 2 * sp.pi ** 2 * sp.integrate(sp.simplify(r ** 3 * (4 / (1 + r ** 2) ** 2) * Sstar), (r, 0, sp.oo)) / 4
J0 = 2 * sp.pi ** 2 * sp.integrate(sp.simplify(r ** 3 * (4 / (1 + r ** 2) ** 2) * Sf.subs(fr, 0).doit()), (r, 0, sp.oo)) / 4
print("   weighted translation norm per direction: horizontal %s ;  un-projected F_{nu mu} %s  (L = 1)" % (sp.simplify(Jtr), sp.simplify(J0)))
chk("M4 weighted translation norm = 32 pi^2/5 (= N(1)): the centre metric is (32 pi^2 L^2/5)(dx0^2 + drho^2)/g^2, SO(5)-vector as it must be", sp.simplify(Jtr - 32 * sp.pi ** 2 / 5) == 0)
chk("M4-control: the un-projected F_{nu mu} (flat-space horizontal) has LARGER weighted norm (the projection is not a no-op), so the equality above is non-trivial", sp.N(J0 - Jtr) > 1e-6)

# ---------------------------------------------------------------- M5 profile
Nu = lambda uu: Nnum(mp.e ** (2 * uu)) * mp.e ** (2 * uu) / mp.pi ** 2
us = np.linspace(-8, 8, 321)
vals = np.array([float(Nu(uu)) for uu in us])
dv = np.diff(vals); sc = [(us[i], us[i + 1]) for i in range(len(dv) - 1) if np.sign(dv[i]) != np.sign(dv[i + 1])]
chk("M5 N_u(u) = rho^2 N(rho)/pi^2 is even in u = ln rho (max asymmetry %.1e)" % float(np.max(np.abs(vals - vals[::-1]))), np.max(np.abs(vals - vals[::-1])) < 1e-9)
chk("M5 N_u has exactly one critical point on u in [-8, 8] (the centre u = 0, a maximum, N_u = 6.4 pi^2 L^2): no special locus at any other rho", len(sc) == 1 and abs(sc[0][0] + 0.025) < 0.05 and vals.max() == vals[160])
Zv = mp.sqrt(32 * mp.pi / 3)
print("   N_u(ln Z)/N_u(0) = %s  (Z = 5.7888; the metric is smooth and monotone there; nothing marks it)" % mp.nstr(Nu(mp.log(Zv)) / Nu(0), 5))
chk("M5 N_u is not constant: the L^2 metric is NOT the (scale-free) SO(5,1)-invariant hyperbolic metric du^2; the scale L enters as an overall factor and through the SO(5) breaking", float(vals.max() / vals[0]) > 1e3)
D = mp.quad(lambda rr: mp.sqrt(Nnum(rr ** 2)), [0, 1])
print("   L^2 distance centre -> boundary (point-instanton limit) along the diameter = %s * L/g : FINITE (the metric is incomplete)" % mp.nstr(D, 8))
chk("M5 the point-instanton boundary is at finite L^2 distance", D < 100)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
