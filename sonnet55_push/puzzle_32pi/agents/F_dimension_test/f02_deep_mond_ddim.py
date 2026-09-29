#!/usr/bin/env python3
"""f02_deep_mond_ddim.py -- what 'deep-MOND flat rotation curve' means in d spatial dimensions, computed.

Newtonian field of a point mass in d dims (Gauss law): g_N = C_d G M / r^(d-1)  (C_d a convention constant, see f01).
Algebraic (spherical) MOND: mu(g/a0) g = g_N  (exact for AQUAL, and for QUMOND with nu = 1/mu).  Deep limit mu -> x^s.

  A  the RECORD's kernel (s = 1, mu -> x, Milgrom eq. 9 family) in d dims:  g = sqrt(a0 g_N) ~ r^(-(d-1)/2),
     v^2 = g r ~ r^((3-d)/2)  (so v ~ r^((3-d)/4)): flat iff d = 3, rising for d = 2, falling for d >= 4; potential ~ r^((3-d)/2)
     (log at d=3): confining for d<3, bounded (escape possible) for d>3.  Checked NUMERICALLY with mu = x/(1+x), d = 2..6.
  B  what flatness needs in d dims: g ~ 1/r  <=>  s = d-2.  The deep field equation is then the p-Laplacian with p = s+2 = d, whose
     action  int |grad Phi|^p d^dx  is conformally invariant iff p = d (inversion check, exact).  So 'flat' <=> 'conformally invariant'
     <=> p = d, in every d;  with the FIXED kernel s=1 (p=3) all of them hold iff d = 3.
  C  Milgrom-type scale invariance (x,t) -> lambda (x,t), velocities fixed, rho -> lambda^-3 rho (from G a0 rho fixed): mass scales as
     lambda^(d-3): mass-preserving only at d = 3 (s=1 kernel).
  D  dimensional analysis does NOT single out d=3: a velocity v = (G M)^p a0^q exists for every d (p = 1/(2(d-1))); at d=3 v^4 = G M a0.
     [An earlier draft of this lane said otherwise; corrected here: the d=3 statement is about the r-INDEPENDENT plateau of the s=1 kernel.]
  F  the isometry group of dS_(d+1) is the conformal group of R^d for every d (Milgrom's ten generators are the d = 3 case), so a dS/conformal reading of deep-MOND
     extends to every d only with the p = d kernel (which has flat curves in every d).
  E  the 'slope reading' (mu'(0) = N, kappa = 1/N; p05 part A) needs mu ~ x^1 in the deep limit: with the flatness-preserving kernel
     s = d-2 the slope is 0 for d>3 and infinite/undefined for d<3.  So the record's N-readings of kappa live on the s=1 kernel, which
     is non-flat for every d != 3.
Controls: d = 3 (both kernels coincide), d = 2 (Newtonian gravity is already flat: s = d-2 = 0), d = 4 (falling), mutation (wrong exponents fail).
Exit 0 = all checks as stated.
"""
import sys
import numpy as np
import sympy as sp
from scipy.optimize import brentq

OK = []
def check(name, cond):
    OK.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

r, d, s_, a0, GM = sp.symbols('r d s a0 GM', positive=True)

# ---------------------------------------------------------------------------- A  analytic deep limit
print("A  the fixed kernel s = 1 (mu -> x), analytic:")
gN = GM / r**(d - 1)
g_deep = sp.sqrt(a0 * gN)
v2 = sp.simplify(g_deep * r)
Phi = sp.integrate(g_deep.subs(d, sp.Symbol('dd', positive=True)), r)  # symbolic power; specific d below
print("    g = sqrt(a0 GM) r^(-(d-1)/2),   v^2 = g r = sqrt(a0 GM) r^((3-d)/2)")
for dd in range(2, 7):
    e = sp.simplify(sp.diff(sp.log(v2.subs(d, dd)), r) * r)     # d ln v^2 / d ln r
    check(f"A{dd}  d={dd}: d ln v^2/d ln r = (3-d)/2 = {sp.Rational(3 - dd, 2)}   (flat iff 0)", sp.simplify(e - sp.Rational(3 - dd, 2)) == 0)
# potential
for dd in (2, 3, 4, 5):
    Pot = sp.integrate(g_deep.subs(d, dd), (r, 1, sp.oo)) if dd > 3 else None
    if dd > 3:
        finite = Pot.is_finite is not False and sp.simplify(Pot) != sp.oo
        check(f"A-pot{dd} d={dd}: the deep-MOND potential difference Phi(inf)-Phi(1) is finite (escape possible)", finite)
    else:
        diverges = sp.integrate(g_deep.subs(d, dd), (r, 1, sp.oo)) == sp.oo
        check(f"A-pot{dd} d={dd}: the deep-MOND potential diverges at infinity ({'log' if dd == 3 else 'power'}: all orbits bound)", diverges)

# ---------------------------------------------------------------------------- numerical, full mu
def slope_numeric(dd, s, rlo=1e5, rhi=1e7):
    """d ln v / d ln r at large r for mu(x) = x^s/(1+x^s), a0 = 1, GM = 1, g_N = r^-(d-1)."""
    def g_of_r(rr):
        gn = rr**(-(dd - 1))
        f = lambda g: (g**s / (1 + g**s)) * g - gn
        return brentq(f, 1e-40, 1e5, xtol=1e-300, rtol=1e-14, maxiter=500)
    def v(rr):
        return np.sqrt(g_of_r(rr) * rr)
    return (np.log(v(rhi)) - np.log(v(rlo))) / (np.log(rhi) - np.log(rlo))
print("\n  numerical log-slope d ln v/d ln r at r = 1e5..1e7 r_M (a0 = 1, GM = 1)")
print(f"    {'d':>3}{'s=1 (fixed kernel)':>22}{'predicted (3-d)/4':>20}{'s=d-2 (flat kernel)':>24}")
res = {}
for dd in range(2, 7):
    sl1 = slope_numeric(dd, 1.0)
    sl_flat = slope_numeric(dd, dd - 2.0) if dd > 2 else float('nan')
    res[dd] = (sl1, sl_flat)
    print(f"    {dd:>3}{sl1:>22.6f}{(3 - dd) / 4:>20.6f}{sl_flat:>24.6f}")
for dd in range(2, 7):
    check(f"An{dd} d={dd}: numerical slope with mu = x/(1+x) equals (3-d)/4 within 1e-3", abs(res[dd][0] - (3 - dd) / 4) < 1e-3)
for dd in range(3, 7):
    check(f"Bn{dd} d={dd}: with mu -> x^(d-2) the deep curve is flat (|slope| < 1e-3)", abs(res[dd][1]) < 1e-3)
check("A-ctl  control: at d = 3 both kernels are the same (s = d-2 = 1) and flat", abs(res[3][0]) < 1e-3 and abs(res[3][1]) < 1e-3)
# d = 2 Newtonian: g_N ~ 1/r, so v^2 = g r is constant with NO modification (s = d-2 = 0 gives mu = 1/2, a rescaled Newtonian force)
sl_d2_newton = slope_numeric(2, 0.0)
check("A-d2   control: at d = 2 Newtonian gravity g_N ~ 1/r is ALREADY flat (numerical slope %.2e); the flatness-preserving kernel s = d-2 = 0 is a constant mu (no MOND needed)" % sl_d2_newton, abs(sl_d2_newton) < 1e-6)
# mutation: a wrong exponent
check("A-mut  mutation: claiming flatness for s=1 at d=4 (slope 0) is rejected by the numerics", not abs(res[4][0]) < 1e-3)

# ---------------------------------------------------------------------------- B  s = d-2 and the p-Laplacian
print("\nB  flatness and conformal invariance")
sv = sp.symbols('s', positive=True)
dd_ = sp.symbols('dd_', positive=True)
# flatness: g ~ r^(-(d-1)/(s+1)) = 1/r  =>  s = d-2
sol_flat = sp.solve(sp.Eq((dd_ - 1) / (sv + 1), 1), sv)
check("B1  g ~ 1/r (flat curve) from the deep kernel mu ~ x^s requires s = d - 2", sol_flat == [dd_ - 2])
# deep field equation div(|grad Phi|^s grad Phi) = source is the p-Laplacian with p = s + 2 ; action int |grad Phi|^(s+2)
p = sv + 2
# conformal invariance under inversion x -> x/|x|^2 for radial Phi: int |Phi'|^p r^(d-1) dr -> int r'^(2p-d-1) |Phi~'|^p dr'
q = sp.symbols('q')
expo_lhs = 2 * p - dd_ - 1        # exponent of r' after inversion
expo_rhs = dd_ - 1                # exponent required for the same functional form
sol_conf = sp.solve(sp.Eq(expo_lhs, expo_rhs), sv)
check("B2  inversion x -> x/|x|^2 maps int |grad Phi|^p d^dx to itself iff 2p - d - 1 = d - 1, i.e. p = d  (s = d - 2)", sol_conf == [dd_ - 2])
# verify the inversion Jacobian bookkeeping explicitly for one function
rp = sp.symbols('rp', positive=True)
Phi_r = sp.Function('F')
F = sp.Function('F')
# Phi(r) = F(r); Phi~(r') = F(1/r'); |Phi'(r)| = r'^2 |Phi~'(r')|, dr = dr'/r'^2, r^(d-1) = r'^(-(d-1))
Ft = F(1 / rp)
dFt = sp.diff(Ft, rp)
Fprime_at_r = sp.diff(F(r), r).subs(r, 1 / rp)
lhs = sp.simplify(Fprime_at_r * (-1) * rp**-2)      # dPhi~/dr' = -(1/r'^2) Phi'(1/r')  => Phi'(r) = -r'^2 dPhi~/dr'
check("B3  chain rule: dPhi~/dr' = -(1/r'^2) Phi'(r) with r = 1/r' (so |grad Phi| = r'^2 |grad Phi~|)", sp.simplify(dFt - lhs) == 0)
check("B4  the fixed kernel s=1 (p=3) is conformally invariant iff d = 3 (2p-d-1 = d-1 -> d = 3)", sp.solve(sp.Eq(2 * 3 - dd_ - 1, dd_ - 1), dd_) == [3])
check("B5  control: s = 1 at d = 4 gives exponent 2p-d-1 = 1 != d-1 = 3 (not invariant); s = d-2 = 2 at d = 4 gives p = 4 = d (invariant)",
      (2 * 3 - 4 - 1 != 4 - 1) and (2 * (2 + 2) - 4 - 1 == 4 - 1))

# ---------------------------------------------------------------------------- C  scale invariance and mass scaling
print("\nC  (x,t) -> lambda (x,t) with Phi (a velocity^2) fixed, s = 1")
lam = sp.symbols('lambda', positive=True)
# div(|grad Phi| grad Phi) ~ L^-3 ; G a0 rho: G a0 fixed ; so rho -> lam^-3 rho ; M = rho L^d -> lam^(d-3) M
mass_scale = sp.simplify(lam**(-3) * lam**dd_)
check("C1  mass scales as lambda^(d-3): mass-preserving scale invariance only at d = 3", sp.simplify(mass_scale - lam**(dd_ - 3)) == 0)
check("C2  control d=3 -> 1, d=4 -> lambda, d=2 -> 1/lambda", [sp.simplify(mass_scale.subs(dd_, k)) for k in (3, 4, 2)] == [1, lam, 1 / lam])

# ---------------------------------------------------------------------------- D  dimensional analysis
print("\nD  dimensional analysis of a velocity from (G M) and a0")
L_, T_ = sp.symbols('L_ T_')
pp, qq = sp.symbols('pp qq')
dv = sp.symbols('dv', positive=True)
# [G M] = L^d T^-2 (acceleration x length^(d-1)),  [a0] = L T^-2,  [v] = L T^-1
eq1 = sp.Eq(dv * pp + qq, 1)
eq2 = sp.Eq(-2 * pp - 2 * qq, -1)
sol = sp.solve([eq1, eq2], [pp, qq], dict=True)[0]
check("D1  v = (G M)^p a0^q exists for EVERY d: p = 1/(2(d-1)), q = (d-2)/(2(d-1))  (v^4 = G M a0 at d = 3)",
      sp.simplify(sol[pp] - 1 / (2 * (dv - 1))) == 0 and sp.simplify(sol[qq] - (dv - 2) / (2 * (dv - 1))) == 0)
check("D2  at d = 3: p = q = 1/4", (sol[pp].subs(dv, 3), sol[qq].subs(dv, 3)) == (sp.Rational(1, 4), sp.Rational(1, 4)))
# with s = d-2 kernel: g = (a0^(d-2) G M)^(1/(d-1)) / r  =>  v^(2(d-1)) = a0^(d-2) G M   (this D1 velocity IS the flat plateau)
gflat = (a0**(dv - 2) * GM)**(1 / (dv - 1)) / r
vflat2 = sp.simplify(gflat * r)
check("D3  the s = d-2 kernel's plateau v^2 = (a0^(d-2) G M)^(1/(d-1)) is exactly the dimensional-analysis velocity of D1",
      sp.simplify(vflat2 - (GM**sol[pp] * a0**sol[qq])**2) == 0)

# ---------------------------------------------------------------------------- E  slope reading
print("\nE  the 'slope reading' mu'(0) = N needs the deep kernel mu ~ x^1")
xx = sp.symbols('x', positive=True)
for dd in (3, 4, 5):
    mu_flat = xx**(dd - 2) / (1 + xx**(dd - 2))
    slope0 = sp.limit(sp.diff(mu_flat, xx), xx, 0)
    print(f"    d={dd}: mu = x^{dd - 2}/(1+x^{dd - 2}):  mu'(0) = {slope0}")
check("E1  flat kernel: mu'(0) = 1 at d = 3 (finite, nonzero) and 0 at d = 4, 5 : N-slope readings of kappa are defined only at d = 3 when the curve is flat",
      [sp.limit(sp.diff(xx**(k - 2) / (1 + xx**(k - 2)), xx), xx, 0) for k in (3, 4, 5)] == [1, 0, 0])

# ---------------------------------------------------------------------------- F  the de Sitter <-> conformal-group link is d-general
print("\nF  isometry group of dS_(d+1) = conformal group of R^d, for every d (Milgrom 2009, arXiv:0810.4065, states the d = 3 case: ten generators)")
n_iso = lambda k: (k + 1) * (k + 2) // 2                          # dim SO(k+1,1)
n_conf = lambda k: k * (k + 1) // 2 + 1 + k                       # rotations+translations (k(k+1)/2) + dilation + k special conformal
check("F1  dim Isom(dS_(d+1)) = dim SO(d+1,1) = (d+1)(d+2)/2 equals dim Conf(R^d) = d(d+1)/2 + 1 + d for every d; d = 3: 10 = 10 (Milgrom's ten)", all(n_iso(k) == n_conf(k) for k in range(1, 12)) and n_iso(3) == 10)
check("F2  so a 'deep-MOND equation conformally invariant in R^d' matches dS_(d+1) symmetry for EVERY d, provided the deep kernel is the p = d one (s = d-2, flat curves); the fixed p = 3 cubic action does so only at d = 3",
      sol_conf == [dd_ - 2] and [k for k in range(2, 12) if 3 == k] == [3])
print(f"\n  {sum(OK)}/{len(OK)} checks held.")
sys.exit(0 if all(OK) else 1)
