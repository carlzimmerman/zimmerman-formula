#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agentN1_nonhuygens_commutator.py  (agentN1, 2026-06-10)

GATE QUESTION (the unique field-side escape named by agentF's all-orders census):
agentF's kill of the bath-inertia mechanism rests on the lemma that for the CONFORMAL
massless scalar in dS the field commutator pulled back on any stationary Deser-Levin
worldline (proper acceleration a, Hubble H, kappa = sqrt(a^2+H^2)) is the universal
contact term (i/2pi) delta'(s) -- trajectory-blind -- so dissipation carries no (a,H)
information beyond kappa and the exact response is forced to A(kappa)+a^2 B(kappa).
This script computes the pulled-back commutator C(s) = <[phi(z(tau)), phi(z(tau-s))]>
on the SAME worldline family for
  (a) the massive scalar in dS (Bunch-Davies), principal (m > 3H/2) and complementary
      (m < 3H/2) series, via the exact Gauss-hypergeometric Wightman function, and
  (b) the minimally coupled massless limit (xi = 0, m -> 0), with the Allen IR issue
      handled explicitly (the commutator is state-independent; see [D3] notes).

CENTRAL EXACT RESULT (derived in agentN1_nonhuygens_commutator.md, verified here):
  with M^2 = m^2 + 12 xi H^2,  nu = sqrt(9/4 - M^2/H^2),  h+- = 3/2 +- nu,
  beta = H^2/kappa^2,  y(s) = -beta sinh^2(kappa s/2)  [= (1-Z)/2 on the worldline]:

    C(s) = (i/2pi) delta'(s)  +  i T(s),
    T(s) = (1/8pi) (M^2 - 2H^2) sgn(s) 2F1(h+, h-; 2; y(|s|)).         (TAIL)

  Conformal anchor: M^2 = 2H^2 (nu = 1/2)  =>  T == 0  =>  C = (i/2pi) delta'(s).
  The tail is a function of TWO variables (kappa, beta) <-> (a, H): trajectory-blind
  ONLY at the two measure-zero points M^2 = 2H^2 (conformal) and M^2 -> 0 (where
  2F1(3,0;2;y) == 1 and T -> -(H^2/4pi) sgn(s): a-blind constant, H-aware).

Sections:
 [A1] sympy: worldline embedding identities; Z(s) pullback; KMS periodicity of Z
 [A2] sympy: conformal reduction (Deser-Levin kernel); tail coefficient (M^2-2H^2)/8pi
 [B1] mpmath: the hypergeometric discontinuity identity across the timelike cut
 [B2] mpmath: closed-form tail vs direct boundary value of the BD pullback (2 routes)
 [B3] mpmath: distributional check: full C(s) = (i/2pi)delta'(s) + i T(s) on test fns
 [C1] small-mass expansion: T = -(H^2/4pi) + (m^2/8pi)[1 - (2/3) g(y)] + O(m^4)
 [C2] sympy small-s series: step (M^2-2H^2)/8pi; shape 1 - M^2 s^2/8 +
      (M^2/192)(M^2+2H^2-2a^2) s^4: the trajectory (a^2) enters the SHAPE at s^4
 [C3] large-s asymptotics: branches (-y)^{-h-} and (-y)^{-h+}; decay rates (3/2-+nu)kappa
 [D1] THE GATE TABLE: fixed kappa = 1, fixed field m = 0.5 (xi=0); (a,H) family scan
 [D2] flat-space validation: dS formula -> Bessel J1 tail; independent K1-pullback
      route; independent mode-integral route (three independent routes agree)
 [D3] minimally coupled massless limit: T -> -(H^2/4pi) sgn(s) (a-blind, H-aware)
 [D4] KMS check: the pullback is KMS at T = kappa/2pi for EVERY mass (temperature
      stays kappa-only; what breaks kappa-blindness is the spectral content)

Units hbar = c = k_B = 1.  No git.
"""
import sympy as sp
from mpmath import mp, mpf, mpc, sqrt as msqrt, sinh, cosh, gamma, hyp2f1, \
    quad, besselj, besselk, exp, log, pi as mppi, sin, cos, conj, im, re, mpmathify

mp.dps = 25
PI = mppi


def banner(tag, txt):
    print()
    print("=" * 96)
    print(f"[{tag}] {txt}")
    print("=" * 96)


# ----------------------------------------------------------------------------------
banner("A1", "sympy: Deser-Levin worldline in the dS4 embedding; Z(s) pullback; KMS periodicity")
# ----------------------------------------------------------------------------------
tau, s_, a_, H_ = sp.symbols('tau s a H', positive=True)
kap_ = sp.sqrt(a_**2 + H_**2)
eta5 = sp.diag(-1, 1, 1, 1, 1)
X = sp.Matrix([sp.sinh(kap_*tau)/kap_, sp.cosh(kap_*tau)/kap_, a_/(H_*kap_), 0, 0])


def dot5(U, V):
    return sum(eta5[i, i]*U[i]*V[i] for i in range(5))


XX = sp.simplify(dot5(X, X))
U5 = X.diff(tau)
UU = sp.simplify(dot5(U5, U5))
Acc = U5.diff(tau)
Aproj = sp.Matrix([Acc[i] - H_**2*dot5(Acc, X)*X[i] for i in range(5)])
AA = sp.simplify(dot5(Aproj, Aproj))
print(f"  X.X = {XX}   (must be 1/H^2)      -> {'OK' if sp.simplify(XX - 1/H_**2) == 0 else 'FAIL'}")
print(f"  u.u = {UU}   (must be -1)         -> {'OK' if sp.simplify(UU + 1) == 0 else 'FAIL'}")
print(f"  A.A = {AA}   (must be a^2: proper acceleration) -> {'OK' if sp.simplify(AA - a_**2) == 0 else 'FAIL'}")

Xs = X.subs(tau, tau - s_)
Zp = sp.simplify(H_**2*dot5(X, Xs))
Ztarget = (H_**2*sp.cosh(kap_*s_) + a_**2)/kap_**2
print(f"  Z(s) = H^2 X(tau).X(tau-s) = {sp.simplify(Zp)}")
print(f"  Z(s) == (H^2 cosh(kappa s) + a^2)/kappa^2      -> "
      f"{'OK' if sp.simplify(Zp - Ztarget) == 0 else 'FAIL'}")
omz = sp.simplify(1 - Ztarget - (-2*H_**2/kap_**2*sp.sinh(kap_*s_/2)**2))
print(f"  1 - Z(s) == -2(H^2/kappa^2) sinh^2(kappa s/2)  -> {'OK' if omz == 0 else 'FAIL'}")
print(f"  => hypergeometric argument w = (1+Z)/2 = 1 + beta sinh^2(kappa s/2), beta = H^2/kappa^2:")
print(f"     the pullback depends on TWO invariants (kappa, beta), not kappa alone.")
per = sp.simplify((Ztarget.subs(s_, s_ + 2*sp.pi*sp.I/kap_) - Ztarget).rewrite(sp.exp))
print(f"  KMS geometric periodicity Z(s + 2 pi i/kappa) - Z(s) = {per}  "
      f"-> {'OK (period 2pi/kappa for EVERY mass)' if per == 0 else 'FAIL'}")

# ----------------------------------------------------------------------------------
banner("A2", "sympy: conformal point reduces to the Deser-Levin kernel; tail coefficient (M^2-2H^2)/8pi")
# ----------------------------------------------------------------------------------
w_, nu_, M_ = sp.symbols('w nu M', positive=True)
# nu = 1/2 (i.e. M^2 = 2H^2): Gamma(2)Gamma(1) 2F1(2,1;2;w) = 1/(1-w)
F_conf = sp.hyperexpand(sp.hyper([2, 1], [2], w_))
print(f"  Gamma(2)Gamma(1) 2F1(2,1;2;w) = {F_conf}   -> {'OK' if sp.simplify(F_conf - 1/(1-w_)) == 0 else 'FAIL'}")
W_conf = (H_**2/(16*sp.pi**2))/(1 - w_)
# w = (1+Z)/2 = 1 + beta sinh^2(kappa s/2)  (timelike: w >= 1, so 1-w = -beta sinh^2 <= 0)
W_conf_pulled = sp.simplify(W_conf.subs(w_, 1 + H_**2/kap_**2*sp.sinh(kap_*s_/2)**2))
print(f"  conformal pullback W(s) = {W_conf_pulled}")
chk = sp.simplify(W_conf_pulled - (-kap_**2/(16*sp.pi**2*sp.sinh(kap_*s_/2)**2)))
print(f"  == -kappa^2/(16 pi^2 sinh^2(kappa s/2)) (Deser-Levin thermal kernel, kappa-ONLY) "
      f"-> {'OK' if chk == 0 else 'FAIL'}")
# tail coefficient: (H^2/8pi)(1/4 - nu^2) with nu^2 = 9/4 - M^2/H^2
coef = sp.simplify((H_**2/(8*sp.pi))*(sp.Rational(1, 4) - (sp.Rational(9, 4) - M_**2/H_**2)))
print(f"  tail coefficient (H^2/8pi)(1/4 - nu^2) = {coef}  "
      f"-> {'OK: (M^2-2H^2)/(8pi), zero IFF M^2 = 2H^2 (conformal)' if sp.simplify(coef - (M_**2 - 2*H_**2)/(8*sp.pi)) == 0 else 'FAIL'}")

# ==================================================================================
# numerical machinery
# ==================================================================================


def nu_of(MH):           # MH = M/H ; returns nu (real or pure imaginary mpc)
    x = mpf(9)/4 - mpf(MH)**2
    return msqrt(x) if x >= 0 else mpc(0, 1)*msqrt(-x)


def W_BD(s_complex, a, H, M):
    """BD Wightman 2F1 at complex proper-time separation (caller supplies the i*eps)."""
    a, H, M = mpf(a), mpf(H), mpf(M)
    kap = msqrt(a**2 + H**2)
    Z = (H**2*cosh(kap*s_complex) + a**2)/kap**2
    w = (1 + Z)/2
    nu = nu_of(M/H)
    hp, hm = mpf(3)/2 + nu, mpf(3)/2 - nu
    return (H**2/(16*PI**2))*gamma(hp)*gamma(hm)*hyp2f1(hp, hm, 2, w)


def T_closed(s, a, H, M):
    """closed-form tail for s>0: (1/8pi)(M^2-2H^2) 2F1(h+,h-;2; -beta sinh^2(kappa s/2))"""
    a, H, M = mpf(a), mpf(H), mpf(M)
    kap = msqrt(a**2 + H**2)
    y = -(H**2/kap**2)*sinh(kap*s/2)**2
    nu = nu_of(M/H)
    hp, hm = mpf(3)/2 + nu, mpf(3)/2 - nu
    val = (M**2 - 2*H**2)/(8*PI)*hyp2f1(hp, hm, 2, y)
    return re(val)   # analytically real (conjugate parameter pair); strip numeric dust


def T_flat(s, a, m):
    """flat-space (H=0) Rindler tail: (m/4pi rho) J1(m rho), rho = (2/a) sinh(a s/2)."""
    a, m = mpf(a), mpf(m)
    rho = 2*sinh(a*s/2)/a if a > 0 else mpf(s)
    return m*besselj(1, m*rho)/(4*PI*rho)


# ----------------------------------------------------------------------------------
banner("B1", "discontinuity identity: Im 2F1(h+,h-;2;x-i0) = pi(1/4-nu^2)/(Gam(h+)Gam(h-)) * 2F1(h+,h-;2;1-x)")
# ----------------------------------------------------------------------------------
print("  (the timelike cut x>1; boundary value from BELOW = Wightman ordering s-i*eps, s>0)")
print(f"  {'nu':>10}  {'x':>7}  {'Im F(x-i d), d=1e-12':>24}  {'prediction':>24}  {'rel.err':>10}")
for nu in [mpf('0.3'), mpf('0.9'), mpf('1.45'), mpc(0, '0.7'), mpc(0, '2.5')]:
    hp, hm = mpf(3)/2 + nu, mpf(3)/2 - nu
    gg = gamma(hp)*gamma(hm)
    for x in [mpf('1.3'), mpf('3'), mpf('10'), mpf('100')]:
        lhs = im(hyp2f1(hp, hm, 2, x - mpc(0, 1)*mpf('1e-12')))
        rhs = re(PI*(mpf(1)/4 - nu**2)/gg*hyp2f1(hp, hm, 2, 1 - x))
        rel = abs(lhs - rhs)/abs(rhs)
        nus = (f"{float(im(nu)):.2f}i" if im(nu) != 0 else f"{float(re(nu)):.2f}")
        print(f"  {nus:>10}  {float(x):>7.1f}  {float(lhs):>24.12e}  {float(rhs):>24.12e}  {float(rel):>10.1e}")
print("  delta -> 0 convergence at nu=0.9, x=3:")
hp, hm = mpf(3)/2 + mpf('0.9'), mpf(3)/2 - mpf('0.9')
rhs = re(PI*(mpf(1)/4 - mpf('0.9')**2)/(gamma(hp)*gamma(hm))*hyp2f1(hp, hm, 2, -2))
for d in [mpf('1e-6'), mpf('1e-9'), mpf('1e-12')]:
    lhs = im(hyp2f1(hp, hm, 2, 3 - mpc(0, 1)*d))
    print(f"    delta={float(d):.0e}:  rel.err = {float(abs(lhs-rhs)/abs(rhs)):.2e}")
# regularized-2F1 identity used in the degenerate (c-a-b=-1) connection formula:
al, be, yy = mpf('0.7'), mpf('2.3'), mpf('-1.4')
lhs = hyp2f1(al, be, mpf('1e-7'), yy)/gamma(mpf('1e-7'))
rhs = al*be*yy*hyp2f1(al + 1, be + 1, 2, yy)
print(f"  degenerate-case identity 2F1~(a,b;0;y) = a b y 2F1(a+1,b+1;2;y): rel.err = "
      f"{float(abs(lhs-rhs)/abs(rhs)):.1e}  (c->0 limit, c=1e-7)")

# ----------------------------------------------------------------------------------
banner("B2", "closed-form tail vs direct boundary value 2 Im W_BD(s - i eps): two independent routes")
# ----------------------------------------------------------------------------------
cases = [("complementary m=0.8, (a,H)=(0.6,0.8)", 0.6, 0.8, 0.8),
         ("principal     m=2.0, (a,H)=(0.6,0.8)  [m/H=2.5, nu=2i]", 0.6, 0.8, 2.0),
         ("complementary m=0.5, (a,H)=(0.0,1.0)  [geodesic]", 1e-12, 1.0, 0.5),
         ("principal     m=2.0, (a,H)=(1.5,0.9)", 1.5, 0.9, 2.0)]
for label, a, H, m in cases:
    print(f"  {label}")
    for s in [mpf('0.4'), mpf('1.0'), mpf('2.5')]:
        direct = 2*im(W_BD(s - mpc(0, 1)*mpf('1e-10'), a, H, m))
        closed = T_closed(s, a, H, m)
        print(f"    s={float(s):4.1f}:  2 Im W(s-ieps) = {float(direct):+.12e}   "
              f"T_closed = {float(closed):+.12e}   rel.diff = {float(abs(direct-closed)/abs(closed)):.1e}")

# ----------------------------------------------------------------------------------
banner("B3", "distributional check: INT C_eps(s) f(s) ds  ->  -(1/2pi) f'(0) + INT T(s) f(s) ds (coefficient of i)")
# ----------------------------------------------------------------------------------
# f(s) = (s+0.7) exp(-s^2):  f(0)=0.7 (catches any spurious delta(s)),  f'(0)=1.
mp.dps = 20


def f_test(s):
    return (s + mpf('0.7'))*exp(-s**2)


fp0 = mpf(1)


def commutator_action(a, H, m, eps):
    """INT 2 Im W(s-i eps) f(s) ds  over [-8,8] with eps-aware subdivision."""
    def g(sv):
        return 2*im(W_BD(sv - mpc(0, 1)*eps, a, H, m))*f_test(sv)
    pts = [-8, -1, -30*eps, 0, 30*eps, 1, 8]
    return quad(g, pts)


def tail_integral(a, H, m):
    """INT T(s) f(s) ds = INT_0^inf T(s) [f(s)-f(-s)] ds (T odd)."""
    def g(sv):
        return T_closed(sv, a, H, m)*(f_test(sv) - f_test(-sv))
    return quad(g, [mpf('1e-8'), 1, 4, 8])


def richardson3(es, vs):
    """quadratic Lagrange extrapolation of (eps, val) to eps=0."""
    e0, e1, e2 = es
    v0, v1, v2 = vs
    L0 = (0 - e1)*(0 - e2)/((e0 - e1)*(e0 - e2))
    L1 = (0 - e0)*(0 - e2)/((e1 - e0)*(e1 - e2))
    L2 = (0 - e0)*(0 - e1)/((e2 - e0)*(e2 - e1))
    return v0*L0 + v1*L1 + v2*L2


for label, a, H, m, conformal in [
        ("CONFORMAL ANCHOR (M^2=2H^2 via nu=1/2 field) at (a,H)=(0.6,0.8)", 0.6, 0.8, None, True),
        ("massive complementary m=1.0, (a,H)=(0.6,0.8)", 0.6, 0.8, 1.0, False),
        ("massive principal     m=2.0, (a,H)=(0.6,0.8)", 0.6, 0.8, 2.0, False)]:
    if conformal:
        H_ = mpf(H)
        m_eff = msqrt(2)*H_   # M^2 = 2H^2 realized as effective mass (nu = 1/2 exactly)
        a_, m_ = mpf(a), m_eff
        tailI = mpf(0)
    else:
        a_, H_, m_ = mpf(a), mpf(H), mpf(m)
        tailI = tail_integral(a_, H_, m_)
    target = -fp0/(2*PI) + tailI
    es, vs = [], []
    for eps in [mpf('4e-3'), mpf('2e-3'), mpf('1e-3')]:
        val = commutator_action(a_, H_, m_, eps)
        es.append(eps)
        vs.append(val)
    extr = richardson3(es, vs)
    print(f"  {label}")
    print(f"    -(1/2pi) f'(0) = {float(-fp0/(2*PI)):+.9f}    tail integral = {float(tailI):+.9f}    "
          f"TARGET = {float(target):+.9f}")
    for eps, val in zip(es, vs):
        print(f"    eps={float(eps):.0e}:  action = {float(val):+.9f}")
    print(f"    Richardson(eps->0) = {float(extr):+.9f}   |extr - target| = {float(abs(extr-target)):.2e}  "
          f"rel = {float(abs(extr-target)/abs(target)):.1e}")
mp.dps = 25

# ----------------------------------------------------------------------------------
banner("C1", "small-mass expansion: T(s) = -(H^2/4pi) + (m^2/8pi)[1 - (2/3) g(y)] + O(m^4)")
# ----------------------------------------------------------------------------------
print("  g(y) = y/(2(1-y)) - ln(1-y),  y = -(H^2/kappa^2) sinh^2(kappa s/2)  [xi=0: M=m]")
a, H, s = mpf('0.6'), mpf('0.8'), mpf('1.3')
kap = msqrt(a**2 + H**2)
y = -(H**2/kap**2)*sinh(kap*s/2)**2
gy = y/(2*(1 - y)) - log(1 - y)
print(f"  probe (a,H)=(0.6,0.8), s=1.3:  y = {float(y):+.6f},  g(y) = {float(gy):+.6f}")
print(f"  {'m':>6}  {'(F-1)/h_-':>14}  {'-> g(y)?':>10}  {'T_exact':>16}  {'T_smallmass':>16}  {'abs.err':>10}")
errs = []
for m in [mpf('0.2'), mpf('0.1'), mpf('0.05')]:
    nu = nu_of(m/H)
    hm = mpf(3)/2 - nu
    F = hyp2f1(mpf(3)/2 + nu, hm, 2, y)
    ratio = (F - 1)/hm
    Tex = T_closed(s, a, H, m)
    Tsm = -(H**2/(4*PI)) + (m**2/(8*PI))*(1 - mpf(2)/3*gy)
    err = abs(Tex - Tsm)
    errs.append(err)
    print(f"  {float(m):>6.2f}  {float(re(ratio)):>14.8f}  {float(gy):>10.6f}  {float(Tex):>16.10e}  "
          f"{float(Tsm):>16.10e}  {float(err):>10.2e}")
print(f"  error scaling err(m)/err(m/2) = {float(errs[0]/errs[1]):.2f}, {float(errs[1]/errs[2]):.2f}  "
      f"(O(m^4) predicts ~16)")
print("  secular regime s >> 1/kappa (still m<<H): g -> -1/2 - kappa s - ln(beta/4):")
print("    T ~ -(H^2/4pi) + (m^2/8pi)[4/3 + (2/3)(kappa s + ln(beta/4))]")
print("    -> the slope offset carries ln(beta) = ln(H^2/kappa^2): EXPLICIT non-kappa structure;")
print("       valid until kappa s ~ 3H^2/m^2, beyond which the exact tail decays as exp(-h_- kappa s).")

# ----------------------------------------------------------------------------------
banner("C2", "sympy small-s series of the tail SHAPE: trajectory (a^2) enters at s^4")
# ----------------------------------------------------------------------------------
a2, H2, M2, ss = sp.symbols('a2 H2 M2 s', positive=True)
k2 = a2 + H2
e2 = M2/H2                                     # h+ h- = M^2/H^2
y_ser = sp.series(-(H2/k2)*sp.sinh(sp.sqrt(k2)*ss/2)**2, ss, 0, 7).removeO()
F_ser = 1 + e2/2*y_ser + e2*(e2 + 4)/12*y_ser**2 + e2*(e2 + 4)*(e2 + 10)/144*y_ser**3
F_ser = sp.expand(sp.series(sp.expand(F_ser), ss, 0, 5).removeO())
c2 = sp.simplify(F_ser.coeff(ss, 2))
c4 = sp.simplify(F_ser.coeff(ss, 4))
c4_target = sp.simplify(M2*(M2 + 2*H2 - 2*a2)/192)
print(f"  2F1(h+,h-;2;y(s)) = 1 + ({sp.simplify(c2)}) s^2 + ({sp.factor(c4)}) s^4 + O(s^6)")
print(f"  s^2 coefficient = -M^2/8        -> {'OK (mass-only: NO trajectory info at s^2)' if sp.simplify(c2 + M2/8) == 0 else 'FAIL'}")
print(f"  s^4 coefficient = (M^2/192)(M^2+2H^2-2a^2) -> {'OK' if sp.simplify(c4 - c4_target) == 0 else 'FAIL'}")
print("  => T(s) = (M^2-2H^2)/(8pi) sgn(s) [1 - M^2 s^2/8 + (M^2/192)(M^2+2H^2-2a^2) s^4 + ...]")
print("     STEP   T(0+) = (M^2-2H^2)/8pi = (M^2-2kappa^2+2a^2)/8pi:  d T(0+)/d(a^2) |_kappa = 1/(4pi)")
print("            (exact, mass-independent) -- the LEADING non-kappa structure, at order s^0;")
print("     SHAPE  the a^2 dependence enters at s^4 with coefficient -(M^2/96) a^2 * pref.")
print("     In (kappa, H): s^4 coeff = (M^2/192)(M^2+4H^2-2kappa^2): explicit H^2 at fixed kappa.")

# ----------------------------------------------------------------------------------
banner("C3", "large-s asymptotics: T -> pref*[A_- (-y)^{-h_-} + A_+ (-y)^{-h_+}], rates (3/2 -+ nu) kappa")
# ----------------------------------------------------------------------------------


def T_asym(s, a, H, M):
    a, H, M = mpf(a), mpf(H), mpf(M)
    kap = msqrt(a**2 + H**2)
    y = -(H**2/kap**2)*sinh(kap*s/2)**2
    nu = nu_of(M/H)
    hp, hm = mpf(3)/2 + nu, mpf(3)/2 - nu
    Am = gamma(2*nu)/(gamma(mpf(3)/2 + nu)*gamma(mpf(1)/2 + nu))
    Ap = gamma(-2*nu)/(gamma(mpf(3)/2 - nu)*gamma(mpf(1)/2 - nu))
    return re((M**2 - 2*H**2)/(8*PI)*(Am*(-y)**(-hm) + Ap*(-y)**(-hp)))


# NB: integer 2nu (e.g. nu=1) is the degenerate case of the large-argument expansion
# (Gamma(-2nu) pole; log corrections): probe at non-integer 2nu.
for label, a, H, m in [("complementary nu=0.8: m=H sqrt(1.61), (a,H)=(0.6,0.8)", 0.6, 0.8, 0.8*msqrt('1.61')),
                       ("principal nu=2i:      m=2.5H,         (a,H)=(0.6,0.8)", 0.6, 0.8, 2.0)]:
    print(f"  {label}")
    for s in [mpf('12'), mpf('20'), mpf('30')]:
        ex = T_closed(s, a, H, m)
        asy = T_asym(s, a, H, m)
        print(f"    kappa*s={float(s):5.1f}:  T_exact = {float(ex):+.10e}   T_asym = {float(asy):+.10e}   "
              f"rel.err = {float(abs(ex-asy)/abs(ex)):.1e}")
print("  decay rates: complementary (3/2-nu)kappa [slow for light fields: h_- ~ m^2/(3H^2)];")
print("  principal: e^{-3 kappa s/2} times ringing at mu*kappa, mu=sqrt(m^2/H^2-9/4); at a=0 these are")
print("  the dS quasinormal rates H(Delta_-+n) [Lopez-Ortega gr-qc/0605027]. AMPLITUDE carries")
print("  (beta/4)^{-h_-} and (principal) phase mu*ln(beta): non-kappa structure also at late times.")

# ----------------------------------------------------------------------------------
banner("D1", "THE GATE TABLE: fixed kappa = 1, fixed field m = 0.5 (xi = 0); vary (a,H) with a^2+H^2 = 1")
# ----------------------------------------------------------------------------------
print("  agentF's lemma (conformal field): C(s) IDENTICAL for every (a,H) -- the same (i/2pi)delta'(s).")
print("  Massive field: tail T(s) tabulated below in units 1/(8pi), i.e. entries are 8pi*T(s).")
print()
fam = [(mpf(0), None), (mpf('0.6'), None), (mpf('0.8'), None), (mpf('0.95'), None), (mpf('0.999'), None)]
m = mpf('0.5')
svals = [mpf('0.5'), mpf('1'), mpf('2'), mpf('4'), mpf('8')]
hdr = f"  {'a':>6} {'H':>7} {'series':>14} {'nu/mu':>8} {'8piT(0+)':>10}" + "".join(f" {'s='+str(float(sv)):>12}" for sv in svals)
print(hdr)
rows = []
for a, _ in fam:
    H = msqrt(1 - a**2)
    nu = nu_of(m/H)
    if im(nu) == 0:
        ser, nuval = "complementary", float(re(nu))
    else:
        ser, nuval = "principal", float(im(nu))
    step = float(8*PI*(m**2 - 2*H**2)/(8*PI))
    vals = [float(8*PI*T_closed(sv, a, H, m)) for sv in svals]
    rows.append(vals)
    print(f"  {float(a):>6.3f} {float(H):>7.4f} {ser:>14} {nuval:>8.3f} {step:>10.4f}" +
          "".join(f" {v:>12.4e}" for v in vals))
# flat endpoint
vals_flat = [float(8*PI*T_flat(sv, 1, m)) for sv in svals]
rows.append(vals_flat)
print(f"  {'1.000':>6} {'0.0000':>7} {'flat (Bessel)':>14} {'-':>8} {float(m**2):>10.4f}" +
      "".join(f" {v:>12.4e}" for v in vals_flat))
print()
print("  SPREAD ACROSS THE FAMILY AT FIXED kappa = 1 (the gate quantity):")
for j, sv in enumerate(svals):
    col = [r[j] for r in rows]
    mx, mn = max(col), min(col)
    dyn = max(abs(v) for v in col)/min(abs(v) for v in col)
    flip = "SIGN FLIP" if mx > 0 > mn else ""
    print(f"    s={float(sv):4.1f}:  min = {mn:+.3e}  max = {mx:+.3e}  spread = {mx-mn:.3e}  "
          f"dyn.range max|T|/min|T| = {dyn:.1e}  {flip}")
print("  step column: 8piT(0+) = m^2-2H^2 runs from -1.75 (geodesic) to +0.25 (flat): sign flip ON the family.")
print()
print("  CONFORMAL CONTROL on the same family (must vanish: Huygens):")
for a, _ in fam[:3]:
    H = msqrt(1 - a**2)
    Meff = msqrt(2)*H
    d = 2*im(W_BD(mpf(1) - mpc(0, 1)*mpf('1e-10'), a, H, Meff))
    print(f"    (a,H)=({float(a):.2f},{float(H):.3f}):  2 Im W_conf(s=1 - i*1e-10) = {float(d):+.2e}  (O(eps): pure contact, NO tail)")

# within-one-universe supplement: fixed H, the dissipation kernel now varies with a
print()
print("  WITHIN ONE UNIVERSE (fixed H = 0.6, m = 0.5): tail at s = 1 vs a  [conformal field: identically 0]:")
for a in [mpf(0), mpf('0.8'), mpf('2'), mpf('5')]:
    print(f"    a = {float(a):4.1f}:  8pi T(1) = {float(8*PI*T_closed(1, a, mpf('0.6'), m)):+.6e}")

# ----------------------------------------------------------------------------------
banner("D2", "flat-space validation: three independent routes")
# ----------------------------------------------------------------------------------
print("  route 1 (dS closed form, H->0): vs route 0 (Bessel J1 closed form), (a,H)=(0.99995,0.01), m=1:")
a, H, m = msqrt(1 - mpf('0.01')**2), mpf('0.01'), mpf(1)
for s in [mpf('0.7'), mpf('1.5'), mpf('3')]:
    t_dS = T_closed(s, a, H, m)
    t_fl = T_flat(s, 1, m)
    print(f"    s={float(s):4.1f}:  T_dS = {float(t_dS):+.8e}   T_flatJ1 = {float(t_fl):+.8e}   "
          f"rel.diff = {float(abs(t_dS-t_fl)/abs(t_fl)):.1e}  (O(H^2)={float(H**2):.0e})")
print("  route 2 (independent special function): Wightman K1-pullback boundary value, Rindler a=1, m=1:")
for s in [mpf('0.7'), mpf('1.5'), mpf('3')]:
    epsv = mpf('1e-12')
    lam = 4*sinh((s - mpc(0, 1)*epsv)/2)**2     # a = 1
    sig = -lam
    r = msqrt(sig)
    W = (m/(4*PI**2))*besselk(1, m*r)/r
    t_K1 = 2*im(W)
    t_fl = T_flat(s, 1, m)
    print(f"    s={float(s):4.1f}:  2 Im W_K1 = {float(t_K1):+.8e}   T_flatJ1 = {float(t_fl):+.8e}   "
          f"rel.diff = {float(abs(t_K1-t_fl)/abs(t_fl)):.1e}")
print("  route 3 (mode integral, inertial): -(1/4pi^2) INT k^2 e^{-eta k} sin(w t)/w dk -> m J1(mt)/(8 pi t):")
t, m = mpf(2), mpf(1)
target = m*besselj(1, m*t)/(8*PI*t)


def mode_int(eta):
    def f(k):
        w = msqrt(k**2 + m**2)
        return -(1/(4*PI**2))*k**2*exp(-eta*k)*sin(w*t)/w
    seg = [j*PI/t for j in range(0, 360)] + [mpf(360)*PI/t, mpf('1e4')]
    return quad(f, seg)


es, vs = [], []
for eta in [mpf('0.10'), mpf('0.05'), mpf('0.025')]:
    v = mode_int(eta)
    es.append(eta)
    vs.append(v)
    print(f"    eta={float(eta):5.3f}:  I(eta) = {float(v):+.8e}")
extr = richardson3(es, vs)
print(f"    Richardson(eta->0) = {float(extr):+.8e}   target Im W = {float(target):+.8e}   "
      f"rel.err = {float(abs(extr-target)/abs(target)):.1e}")

# ----------------------------------------------------------------------------------
banner("D3", "minimally coupled massless limit (xi=0, m->0): T -> -(H^2/4pi) sgn(s): a-BLIND, H-AWARE")
# ----------------------------------------------------------------------------------
print("  The commutator is STATE-INDEPENDENT (Pauli-Jordan; canonical), so the m->0 limit is clean even")
print("  though no dS-invariant Fock vacuum exists at m=0 (Allen 1985): the IR pathology (the divergent")
print("  constant zero-mode ~ 3H^4/(8pi^2 m^2) in W) is symmetric-part-only and cancels in C(s).")
print("  Limit check at (a,H)=(0.6,0.8), target -H^2/4pi = " + f"{float(-mpf('0.64')/(4*PI)):+.8e}:")
a, H = mpf('0.6'), mpf('0.8')
for m in [mpf('0.1'), mpf('0.03'), mpf('0.01')]:
    devs = [abs(T_closed(sv, a, H, m) - (-(H**2)/(4*PI))) for sv in [mpf('0.5'), mpf('1'), mpf('2'), mpf('5')]]
    print(f"    m={float(m):5.2f}:  max_s |T - (-H^2/4pi)| over s in {{0.5,1,2,5}} = {float(max(devs)):.2e}   (-> 0 like m^2)")
print("  a-BLINDNESS at fixed H (the residual within-universe trajectory-blindness of the m->0 endpoint):")
H = mpf('0.8')
m = mpf('0.001')
ref = T_closed(1, 0, H, m)
for a in [mpf(0), mpf('0.6'), mpf('3')]:
    v = T_closed(1, a, H, m)
    print(f"    a={float(a):4.1f}:  T(1) = {float(v):+.10e}   diff from a=0: {float(abs(v-ref)):.1e}")
print("  H-AWARENESS at fixed kappa: kappa=1 pairs (a,H)=(0,1) vs (0.8,0.6) vs flat:")
for a in [mpf(0), mpf('0.8')]:
    H = msqrt(1 - a**2)
    print(f"    (a,H)=({float(a):.1f},{float(H):.1f}):  T(1) = {float(T_closed(1, a, H, m)):+.8e}  (-> -H^2/4pi = {float(-(H**2)/(4*PI)):+.8e})")
print(f"    flat (1,0):       T(1) = {float(T_flat(1, 1, m)):+.8e}  (-> 0: massless flat = Huygens)")
print("  => 2F1(3,0;2;y) == 1: the m->0 tail is the s-CONSTANT -(H^2/4pi)sgn(s); spectral density")
print("     rho(w) = w/2pi + H^2/(2pi w): the famous dS 1/w IR enhancement, a-independent at fixed H.")
print("     Retarded tail = +H^2/4pi inside the cone: matches the known MMC dS Green function")
print("     [Burko-Harte-Poisson gr-qc/0201020]. Order of limits: (m->0, H->0) do not commute.")

# ----------------------------------------------------------------------------------
banner("D4", "KMS at T = kappa/2pi for EVERY mass: W(s - 2pi i/kappa + i eta) -> W(-s - i eta)")
# ----------------------------------------------------------------------------------
for label, a, H, m in [("complementary m=0.8", 0.6, 0.8, 0.8), ("principal m=2.0", 0.6, 0.8, 2.0)]:
    a, H, m = mpf(a), mpf(H), mpf(m)
    kap = msqrt(a**2 + H**2)
    beta_kms = 2*PI/kap
    s0 = mpf('0.7')
    for eta in [mpf('1e-3'), mpf('1e-6')]:
        lhs = W_BD(s0 - mpc(0, 1)*(beta_kms - eta), a, H, m)
        rhs = W_BD(-s0 - mpc(0, 1)*eta, a, H, m)
        print(f"  {label}: eta={float(eta):.0e}:  |W(s-i(beta-eta)) - W(-s-i eta)|/|W| = "
              f"{float(abs(lhs-rhs)/abs(rhs)):.1e}")
print("  => Deser-Levin temperature kappa/2pi is mass-INDEPENDENT (geometric: Z has imaginary period")
print("     2pi/kappa). What the tail changes is NOT the temperature but the SPECTRAL FUNCTION, which")
print("     now depends on (kappa, beta) = (kappa, H^2/kappa^2) instead of being universal.")

# ----------------------------------------------------------------------------------
banner("GATE", "DECISION SUMMARY")
# ----------------------------------------------------------------------------------
print("""  C(s) = (i/2pi) delta'(s) + (i/8pi)(M^2-2H^2) sgn(s) 2F1(3/2+nu, 3/2-nu; 2; -(H^2/kappa^2) sinh^2(kappa|s|/2))
  - conformal anchor (M^2 = 2H^2): tail coefficient EXACTLY zero -> (i/2pi)delta'(s) reproduced  [A2,B3]
  - massive scalar, BOTH series: the tail depends on (kappa, beta=H^2/kappa^2), i.e. on a and H
    SEPARATELY. At fixed kappa = 1 (m = 0.5) the tail spans order-1 ranges WITH a sign flip at every
    s probed, and a dynamic range ~4e4 at s = 8, across the (a,H) family  [D1]. Trajectory-blindness
    is BROKEN.
  - leading non-kappa structure: step T(0+) = (M^2-2H^2)/8pi with d/d(a^2)|_kappa = 1/4pi exactly;
    shape: a^2 enters at s^4; late time: rates (3/2 -+ nu)kappa with beta-dependent amplitude/phase.
  - the m->0 minimal endpoint is the degenerate boundary: constant tail -(H^2/4pi)sgn(s): H-aware but
    a-blind within a fixed universe (and its noise sector is the Allen-pathological one).
  => GATE-OPENS: dissipation on the Deser-Levin family DOES carry (a,H) information beyond kappa for
     every M^2 not in {0, 2H^2}. agentF's all-orders census does NOT extend to non-Huygens fields:
     its premise (universal contact dissipation kernel) is false for every m > 0.""")
print("done.")
