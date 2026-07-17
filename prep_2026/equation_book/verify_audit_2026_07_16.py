#!/usr/bin/env python3
"""
EQUATION BOOK -- ADVERSARIAL VERIFY PASS (2026-07-16, independent re-derivations)
==================================================================================
Companion to VERIFY.md. Every check here re-derives the mined equations by a
DIFFERENT route than the original eqbook_*/s*_ scripts (fresh eliminations,
different substitutions/parametrizations, independent numerics), so agreement is
evidence, not repetition. No hard-coded booleans; exit 0 iff all checks pass.

The single biggest audit finding is encoded as check A below:
  Milgrom 1999 (astro-ph/9805346, Phys.Lett.A 253:273) Eq (8)-(9) define
     2 pi DeltaT = a * mu_hat(a/a0h),  mu_hat(x) = [1+(2x)^-2]^(1/2) - (2x)^-1,
  and Eq (5) a mu(a/a0) = g_N.  Together these CONTAIN the framework law
     g_obs^2 = g_bar^2 + a0 g_bar  and its inversion -- machine-verified here.
  Milgrom's Eq (6)-(7): T(a) = (1/2pi)(a^2 + Lambda/3)^(1/2) is the Pythagorean
  dS-Unruh pole (via Narnhofer-Peter-Thirring 1996; Deser-Levin 1997).
  => the LAW and the thermal Pythagoras are CREDIT-NOT-CLAIM; what remains the
  framework's own is the coefficient (1/Z vs Milgrom's a0h = 2 c^2 sqrt(Lambda/3),
  a factor 2Z ~ 11.6) and everything downstream mined in M1/M2.
"""
import sys
import sympy as sp
import mpmath as mp
import numpy as np

mp.mp.dps = 30
FAIL = []
def check(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

x, y, yN, a0, g, gob, e, b, r, G, M, c = sp.symbols(
    'x y y_N a0 g g_obs e b r G M c', positive=True)
ell = sp.symbols('ell', real=True)   # ln y ranges over ALL reals (0 must be a root candidate)

print("=" * 78)
print("A. MILGROM-1999 CONTAINMENT (the credit-correcting check)")
print("=" * 78)
# Milgrom's mu_hat exactly as printed in his Eq (9):
mu_hat_paper = sp.sqrt(1 + (2*x)**(-2)) - 1/(2*x)
mu_fw = (sp.sqrt(1 + 4*x**2) - 1)/(2*x)          # the framework kernel K(x^2)
check("Milgrom Eq(9) mu_hat == framework mu (identical function)",
      sp.simplify(mu_hat_paper - mu_fw) == 0)
# Eq (5) balance a*mu(a/a0)=g_N with Milgrom's mu_hat -> the squared law:
bal = x*mu_hat_paper - yN                         # x = a/a0, yN = g_N/a0
sq = sp.simplify((x**2 - yN**2 - yN).subs(yN, sp.simplify(x*mu_hat_paper)))
check("Eq(5)+Eq(9) => a^2 = g_N^2 + a0 g_N identically (the 'a0-line' law)",
      sq == 0)
# the 'exact inversion' E-S1.1 is x*mu_hat written out:
check("inversion g_bar=(sqrt(a0^2+4g_obs^2)-a0)/2 == a*mu_hat(a/a0) (Milgrom's 2pi DeltaT)",
      sp.simplify(x*mu_hat_paper - (sp.sqrt(1 + 4*x**2) - 1)/2) == 0)
# Milgrom Eq (6): T = (1/2pi) sqrt(a^2 + Lambda/3) == the kappa_eff Pythagoras
Lam, H = sp.symbols('Lambda H', positive=True)
T_milgrom = sp.sqrt(x**2*a0**2 + Lam/3)/(2*sp.pi)         # units c=1
kap = sp.sqrt(H**2 + x**2*a0**2)                           # framework pole (c=1)
check("Milgrom Eq(6) == framework kappa_eff Pythagoras under H^2 = Lambda/3",
      sp.simplify(T_milgrom.subs(Lam, 3*H**2)*2*sp.pi - kap) == 0)
# coefficient split: Milgrom a0h = 2 sqrt(Lambda/3) vs framework a0 = sqrt(Lambda/3)/Z
Zs = sp.sqrt(32*sp.pi/3)
check("coefficient fork: a0h_Milgrom / a0_framework == 2Z ~ 11.58 (NOT the same a0)",
      sp.simplify(2*sp.sqrt(Lam/3)/(sp.sqrt(Lam/3)/Zs) - 2*Zs) == 0
      and abs(float(2*Zs) - 11.58) < 0.01)

print()
print("=" * 78)
print("B. LANDMARK TRIPLET, independent route (chain rule in ell = ln y directly)")
print("=" * 78)
L = sp.log(sp.sqrt(sp.exp(2*ell) + sp.exp(ell)))   # ln(g_obs/a0) as fn of ell=ln y
sig = sp.simplify(sp.diff(L, ell))
C = sp.simplify(sp.diff(L, ell, 2))
yE = sp.exp(ell)
check("slope sigma == (2y+1)/(2(y+1)) [fresh chain-rule route]",
      sp.simplify(sig - (2*yE + 1)/(2*(yE + 1))) == 0)
check("curvature C(ell) is EVEN: C(ell) - C(-ell) == 0 identically",
      sp.simplify(C - C.subs(ell, -ell)) == 0)
check("sum rule sigma(ell)+sigma(-ell) == 3/2 identically",
      sp.simplify(sig + sig.subs(ell, -ell) - sp.Rational(3, 2)) == 0)
crit = sp.solve(sp.diff(C, ell), ell)
check("curvature max at ell=0 (y=1) exactly; sigma(0)=3/4, C(0)=1/8",
      (0 in [sp.simplify(s) for s in crit]) and
      sp.simplify(sig.subs(ell, 0) - sp.Rational(3, 4)) == 0 and
      sp.simplify(C.subs(ell, 0) - sp.Rational(1, 8)) == 0)
# second-derivative test that ell=0 is a maximum
check("d2C/dell2 < 0 at ell=0 (it is a MAXIMUM)",
      sp.diff(C, ell, 2).subs(ell, 0) < 0)

print()
print("=" * 78)
print("C. PAIR ESTIMATOR, independent elimination (sp.solve, not construction)")
print("=" * 78)
s1, s2, th1, th2, D, si, U = sp.symbols('s1 s2 theta1 theta2 D sin_i Upsilon',
                                        positive=True)
# observables built from the law with nuisances; then ELIMINATE a0 blindly
v1sq = sp.sqrt((U*s1)**2 + a0*U*s1)*D*th1*si**2
v2sq = sp.sqrt((U*s2)**2 + a0*U*s2)*D*th2*si**2
R12 = sp.simplify((v1sq/v2sq)**2*(th2/th1)**2)
sol = sp.solve(sp.Eq(R12, sp.symbols('R', positive=True)), a0)
check("blind sp.solve of R12 = R for a0 returns exactly ONE solution",
      len(sol) == 1)
est_claimed = (s1**2 - sp.symbols('R', positive=True)*s2**2) / \
              (sp.symbols('R', positive=True)*s2 - s1) * U
check("the unique solution == U*(s1^2 - R s2^2)/(R s2 - s1)  (claimed estimator)",
      sp.simplify(sol[0] - est_claimed) == 0)
check("nuisances D, sin_i absent from R12 (structurally, not just derivative-zero)",
      not R12.has(D) and not R12.has(si))

print()
print("=" * 78)
print("D. EFE CUBIC, independent route (resultant elimination)")
print("=" * 78)
X, B, E = sp.symbols('X B E', positive=True)
w = sp.symbols('w', positive=True)     # w = sqrt(1+4(X+E)^2), auxiliary
# balance mu_hat(X+E)*X = B  <=>  X*(w-1) = 2B(X+E)  with  w^2 = 1+4(X+E)^2
res = sp.resultant(X*(w - 1) - 2*B*(X + E), w**2 - 1 - 4*(X + E)**2, w)
cubic = X**3 + E*X**2 - B*(B + 1)*X - B**2*E
q = sp.simplify(sp.factor(res)/sp.factor(4*(X + E)*cubic))
check("resultant elimination reproduces 4(X+E)*(EFE cubic) up to constant",
      q.is_number and sp.simplify(sp.factor(res) - q*4*(X + E)*cubic) == 0)
# susceptibility by implicit differentiation of the UNSQUARED balance (fresh route)
mu_arg = (sp.sqrt(1 + 4*(X + E)**2) - 1)/(2*(X + E))
F = mu_arg*X - B
dXdE = sp.simplify(-sp.diff(F, E)/sp.diff(F, X))
chi0 = sp.simplify(dXdE.subs(E, 0).subs(X, sp.sqrt(B**2 + B)))
# sympy leaves sqrt(4B^2+4B+1) undenested; collapse it via the verified identity
check("radical collapse: 4B^2+4B+1 == (2B+1)^2 (the denesting step, exact)",
      sp.expand((2*B + 1)**2 - (4*B**2 + 4*B + 1)) == 0)
chi0c = chi0.subs(sp.sqrt(4*B**2 + 4*B + 1), 2*B + 1)
check("EFE susceptibility from UNSQUARED balance == -1/(2(1+b))",
      sp.simplify(chi0c + 1/(2*(B + 1))) == 0)
# half-quench: solve (X^2-B^2)=B/2 branch on the attenuated line, fresh numeric probe
for Bv in (0.05, 0.7, 4.0):
    Xh = float(sp.sqrt(Bv**2 + Bv/2))
    Ev = sp.symbols('Ev')
    ev = sp.solve(sp.Eq((Xh**2 - Bv**2)*(Xh + Ev), Bv*Xh), Ev)[0]
    check(f"half-quench e == g_obs at b={Bv} (numeric {float(ev):.4f} vs {Xh:.4f})",
          abs(float(ev) - Xh) < 1e-12)

print()
print("=" * 78)
print("E. BTFR + M_bar predictor round trips (fresh)")
print("=" * 78)
v = sp.symbols('v', positive=True)
Mpred = (r**2/(2*G))*(sp.sqrt(a0**2 + 4*v**4/r**2) - a0)
# feed M_pred back through the law and demand v comes back (full round trip):
gbarP = G*Mpred/r**2
vback = sp.sqrt(sp.sqrt(gbarP**2 + a0*gbarP)*r)
check("M_bar predictor round trip: v -> M_pred -> law -> v identically",
      sp.simplify(vback - v) == 0)
v4 = sp.expand((sp.sqrt((G*M/r**2)**2 + a0*G*M/r**2)*r)**2)
check("exact finite-radius BTFR v^4 = GMa0 + (GM/r)^2 (fresh expansion)",
      sp.simplify(v4 - G*M*a0 - (G*M/r)**2) == 0)

print()
print("=" * 78)
print("F. DEFLECTION + PHANTOM SURFACE DENSITY, independent numerics")
print("=" * 78)
# independent parametrization: alpha(b) = (2/c^2) INT_b^inf g_obs(r)*(b/r)*(2r dr / sqrt(r^2-b^2))/r
# i.e. substitute l = sqrt(r^2-b^2) analytically -> integrate in r (DIFFERENT from s6's l/psi routes)
def alpha_closed(bb, GM=1.0, a0n=1.0):
    rM = mp.sqrt(GM/a0n)
    uu = bb/rM
    return (4*GM/bb)*mp.sqrt(1 + uu**2)*mp.ellipe(1/(1 + uu**2))
def alpha_r_route(bb, GM=1.0, a0n=1.0):
    # alpha = 4b INT_b^inf g(r) dr/sqrt(r^2-b^2); r = b cosh t makes the
    # sqrt CANCEL analytically: alpha = 4b INT_0^inf g(b cosh t) dt  (c=1)
    gobs = lambda rr: mp.sqrt((GM/rr**2)**2 + a0n*GM/rr**2)
    return 4*bb*mp.quad(lambda t: gobs(bb*mp.cosh(t)), [0, 1, 5, 80])
ok = True
for uu in (0.1, 1.0, 10.0):
    a1, a2 = alpha_closed(mp.mpf(uu)), alpha_r_route(mp.mpf(uu))
    rel = abs(a1 - a2)/a1
    ok = ok and rel < mp.mpf('1e-18')
    print(f"   u={uu}: closed={mp.nstr(a1,12)} r-route={mp.nstr(a2,12)} rel={mp.nstr(rel,3)}")
check("alpha(b) closed form vs INDEPENDENT r-parametrized LOS integral (<1e-18)", ok)
# approach law by pure numerics (no series): [alpha/alpha_inf - 1]*4b^2/r_M^2 -> 1
big = mp.mpf(40)
ainf = 2*mp.pi*mp.sqrt(1.0)     # GM=a0=1 -> alpha_inf = 2 pi
val = (alpha_closed(big)/ainf - 1)*4*big**2
check(f"approach law numeric: (alpha/alpha_inf-1)*4b^2/r_M^2 = {mp.nstr(val,8)} -> 1",
      abs(val - 1) < 2e-3)
# Sigma_ph: independent check by Abel projection of rho_ph (r-route, not l-route)
def Sig_closed(bb):
    return mp.ellipk(1/(bb**2 + 1))/(2*mp.pi*mp.sqrt(bb**2 + 1))
def Sig_abel(bb):
    # Sigma = 2 INT_b^inf rho r dr/sqrt(r^2-b^2); r = b cosh t cancels the sqrt:
    # Sigma = 2b INT_0^inf rho(b cosh t) cosh t dt
    rho = lambda rr: 1/(4*mp.pi*rr*mp.sqrt(rr**2 + 1))
    return 2*bb*mp.quad(lambda t: rho(bb*mp.cosh(t))*mp.cosh(t), [0, 1, 5, 80])
ok = True
for bb in (0.2, 1.0, 5.0):
    s1_, s2_ = Sig_closed(mp.mpf(bb)), Sig_abel(mp.mpf(bb))
    ok = ok and abs(s1_ - s2_)/s1_ < mp.mpf('1e-18')
check("Sigma_ph(b) K-form vs independent Abel projection of rho_ph (<1e-18)", ok)
# closure by pure finite difference of the E-form 2D mass (no sympy elliptic derivs)
def M2D(bb):
    return mp.sqrt(1 + bb**2)*mp.ellipe(1/(1 + bb**2))
h = mp.mpf('1e-9')
ok = True
for bb in (0.5, 2.0):
    lhs = (M2D(mp.mpf(bb) + h) - M2D(mp.mpf(bb) - h))/(2*h)
    rhs = 2*mp.pi*bb*Sig_closed(mp.mpf(bb))
    ok = ok and abs(lhs - rhs) < 1e-12
check("closure dM2D/db == 2 pi b Sigma_ph by finite difference", ok)

print()
print("=" * 78)
print("G. MEMORY FUNCTION: single end-to-end Laplace closure (independent)")
print("=" * 78)
# If Gamma_closed is right, INT_0^inf Gamma(s) e^{-lam s} ds == 1 - K(lam^2), tau=2 units
def intJ0(bb):
    return bb*mp.besselj(0, bb) + mp.pi*bb/2*(
        mp.besselj(1, bb)*mp.struveh(0, bb) - mp.besselj(0, bb)*mp.struveh(1, bb))
def Gam_closed(ss):
    bb = ss/2
    if bb == 0:
        return mp.mpf(1)/2
    return (1 + mp.besselj(1, bb) - intJ0(bb))/2
ok = True
for lamv in (mp.mpf('0.2'), mp.mpf('1'), mp.mpf('3')):
    L1 = mp.quad(lambda ss: Gam_closed(ss)*mp.exp(-lamv*ss), [0, 5, 30, 200])
    K = (mp.sqrt(1 + 4*lamv**2) - 1)/(2*lamv)
    rel = abs(L1 - (1 - K))
    ok = ok and rel < mp.mpf('1e-10')
    print(f"   lam={float(lamv)}: L[Gamma]={mp.nstr(L1,10)}  1-K={mp.nstr(1-K,10)}")
check("L[Gamma_closed](lam) == 1 - K(lam^2) end-to-end (independent of derivation chain)", ok)

print()
print("=" * 78)
print("H. THROTTLE CUBIC INVARIANT + SATURATION (fresh random-y + symbolic)")
print("=" * 78)
Zsym = sp.symbols('Z', positive=True)
nu_y = sp.sqrt(1 + 1/y)
gobs_ab = y*a0*(1 + (nu_y - 1)*(Zsym/2)/y)
Ddef = sp.simplify(gobs_ab - y*a0)
inv_expr = sp.simplify((y*a0)*Ddef*(Ddef + Zsym*a0) - Zsym**2*a0**3/4)
check("throttle cubic invariant == 0 identically (fresh symbols)", inv_expr == 0)
rng = np.random.default_rng(7)
Zn = float(sp.sqrt(32*sp.pi/3))
ok = True
for yv in rng.uniform(Zn/2, 500, 6):
    a0v = 9.362e-11
    nuv = np.sqrt(1 + 1/yv)
    go = yv*a0v*(1 + (nuv - 1)*(Zn/2)/yv)
    gb = yv*a0v
    val = gb*(go - gb)*(go - gb + Zn*a0v)/(Zn**2*a0v**3/4)
    ok = ok and abs(val - 1) < 1e-10
check("cubic invariant numeric at 6 random y in (y_c, 500)", ok)
Ysat = sp.limit(sp.simplify(gobs_ab**2 - (y*a0)**2), y, sp.oo)
check("a0-line saturation Y_inf == (Z/2) a0^2 (fresh limit)",
      sp.simplify(Ysat - Zsym*a0**2/2) == 0)

print()
print("=" * 78)
print("I. INVERSE-MOMENT CLOSED FORM at untested p values")
print("=" * 78)
def Mp_direct(pr):
    def fA(vv):
        uu = vv**5/2
        wA = 4*uu**2/(1 + mp.sqrt(1 - 4*uu**2))
        return wA/mp.pi*uu**(-2*pr)*mp.mpf(5)/2*vv**4
    A = mp.quad(fA, [0, 0.5, 1])
    B_ = 2**(2*pr - 1)/(mp.pi*(2*pr - 1))
    return A + B_
ok = True
for pr in (mp.mpf('0.55'), mp.mpf('0.9'), mp.mpf('1.45')):
    cf = (2**(2*pr - 2)*mp.gamma(mp.mpf(3)/2 - pr) /
          (mp.sqrt(mp.pi)*(2*pr - 1)*mp.gamma(2 - pr)))
    ok = ok and abs(cf - Mp_direct(pr)) < mp.mpf('1e-10')
check("M_p closed form at fresh p = 0.55, 0.9, 1.45 (edges + middle)", ok)

print()
print("=" * 78)
print("J. HUBBLE CHAIN: circularity documentation (consistency, NOT prediction)")
print("=" * 78)
# canonical a0 is DEFINED from Planck's H_Lambda; the weld must therefore return
# Planck H0 identically -- document that the '67.4' is input-recovery, not a prediction.
cv = 2.99792458e8
KMSMPC = 1.0e3/3.0856775814913673e22
H0p, OmLp = 67.36, 0.6847                       # Planck 2018 TT,TE,EE+lowE+lensing
a0_can = cv*H0p*KMSMPC*np.sqrt(OmLp)/Zn
HL = Zn*a0_can/cv
H0back = np.sqrt(HL**2 + (OmLp and (1 - OmLp))*(H0p*KMSMPC)**2)/KMSMPC
check(f"defining a0 from Planck and welding back returns Planck H0 ({H0back:.2f})",
      abs(H0back - H0p) < 0.02)
print("   => the chain is PREDICTIVE only if a0 enters from galaxies (E-S8.1),")
print("      distance-free; with the canonical footing it is input-recovery.")

print()
print(f"{len(FAIL)} failures" if FAIL else "ALL CHECKS PASS")
sys.exit(1 if FAIL else 0)
