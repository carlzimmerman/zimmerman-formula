#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE P2 -- THE UNIMODALITY / SINGLE-SCALE AXIOM: does tree-level dynamics supply one?
real_research/reviews/mi_unimodality_axiom_2026.py

QUESTION (double-edged, both halves reported with equal weight).  The LP lane
(mi_extremal_kernel_lp_2026.py) found sup r = +infinity for the admissibility class, but only
because psi may carry a SECOND scale; the committed 7-shape SINGLE-SCALE menu ceiling is exactly
r = 9 (mi_psi_search_r2Z_2026.py section H, closed form 4(2-d)^2/(2+7d-4d^2) -> 8).  Since
2 c H_Lambda/9 = 1.2044e-10 sits 0.36% from McGaugh's empirical 1.20e-10, that lane flagged: IF a
physically motivated single-scale/unimodality axiom on psi were independently justified, the
coincidence would upgrade to a LEAD -- and would simultaneously EXCLUDE kappa = 1/2 (r = 2Z =
11.5776, 28.6% above 9), the ALT footing (9.5919, 6.6% above) and Milgrom 2020's 4 pi (39.6%
above).  This script tests whether tree-level dynamics supplies the axiom.

FRAMEWORK OBJECT UNDER TEST (the CRP master formula, mi_crossover_master_formula_2026.py):
  I = f(T) - f(T_GH),  T = sqrt(a^2 + H^2)/2pi,  q = a_0/(c H_Lambda) = 2 c1p/f'(T_GH) = 2/r.
  In T_GH units with s = T - T_GH:  F'(s) = c1p [1 + (r-1) psi(s)],  psi(0) = 1, psi decreasing
  to 0, Int psi finite.  Write lam = r-1, Psi(s) = Int_0^s psi.  Then
    Phi(s) := F(s)/c1p = s + lam Psi(s) = g_bar/(c H_Lambda),   w(s) := sqrt(s(s+2T)) = g_obs/(c H_Lambda)
    (A1) mu <= 1      <=>  lam Psi(inf) <= T_GH
    (A2) mu monotone  <=>  F'(s) s(s+2T_GH) >= F(s)(s+T_GH)
       <=>  lam J(s) <= 1  with  J(s) = [Psi(s)(s+T) - psi(s) s(s+2T)]/(s T),   so lam_max = 1/sup J.
    (Lemma 2 of the psi-search lane: J(inf) = Psi(inf)/T, so (A1) is the s -> inf limit of (A2).)

WHAT THIS SCRIPT ESTABLISHES (five results, three of them new):
  R1  ARITHMETIC.  a_0(r=9) = 1.204311111e-10 canonical, +0.3593% from McGaugh's 1.20e-10 and
      +28.647% from the framework's 9.3614e-11.  Both footings reported.
  R2  *** THE PREMISE "single-scale => r <= 9" IS FALSE. ***  The ONE-PARAMETER, unimodal,
      completely monotone, C^infinity single-scale family psi = (1+s/d)^-p has a d -> 0 ceiling
      r_max(p) that is continuous and strictly decreasing on p in (1, inf) with range
      (5.58208, 17.62251).  ALL FOUR target coefficients lie inside it:
          r = 9        at p = 2.00000000 (exactly, sup J_0 = 1/8 at u = 3)
          r = 9.03233  at p = 1.98710391   (McGaugh 1.20e-10)
          r = 11.57761 at p = 1.40509449   (2Z, kappa = 1/2)
          r = 12.56637 at p = 1.29214700   (4 pi)
      The committed "9" was a MENU artefact: the 7 shapes contained only the integer exponents
      p = 2, 3 and faster-decaying shapes, missing the whole band 1 < p < 2.  So the axiom, even
      if granted, derives NOTHING and excludes NOTHING.
  R3  *** SCALE-BLINDNESS THEOREM. ***  The ceiling functional is sup_u [X(u)/u - 2 chi(u)] with
      psi = chi(s/d), X = Int chi, and it is INVARIANT under u -> u/c.  r is therefore a pure
      SHAPE functional: any axiom that fixes only a SCALE -- one relaxation time, one quasinormal
      frequency, one resonance, one attractor -- constrains r NOT AT ALL.  Every tree-level
      mechanism on the list supplies a scale, not a shape.
  R4  *** THE FRAMEWORK'S OWN EXACT LAW IS ADMISSIBLE AT EVERY r, and its psi is TWO-SCALE. ***
      g_obs^2 = g_bar^2 + a_0 g_bar is realised in this class by the closed-form
          Phi_law = 2 s(s+2T)/(D+q),  D = sqrt(q^2+4s(s+2T)),
          psi_law = (4T^2-q^2)/(lam D (2(s+T)+D)),     Psi_law(inf) = (1-q/2T)/lam,
      which is admissible EXACTLY when r > 1 (sympy: dpsi/ds sign = q^2-4T^2), satisfies (A1) as
      lam Psi(inf) = 1 - 1/r < 1 identically, and passes (A2) at r = 2, 9, 2Z, 4pi, 17.6, 100.
      Its log-log slope is monotone and runs 0 -> 1/2 -> 2, with the inner break at
      a = (a_0/2) sqrt(1+(a_0/4cH_L)^2) = a_0/2 to O(1/r^2) (0.09% at kappa = 1/2) -- the
      framework's own floor k -- and scale ratio 2 r^2.  The 1/2-shelf is 0.68 decades wide at 2Z
      against 0.234 for ANY single-scale power kernel.  So the axiom is not merely unmotivated: for
      r >> 1 it is INCONSISTENT with the phenomenology it was meant to explain, and the "second
      scale sitting at a ~ a_0" that the LP lane priced is precisely k = a_0/2.
  R5  *** FORMAL r IS NOT THE OBSERVED a_0 for the ceiling kernels. ***  Fit the a_0-line
      g_obs^2 = g_bar^2 + a_0 g_bar on the SPARC window y in [0.1,10] (window made self-consistent
      in the fitted a_0) to the r_formal = 9 extremal kernel: a_0_obs = 2 c H_Lambda EXACTLY, i.e.
      r_obs = 1.0000 (Milgrom 1999's own value), a factor 9 away from the 1.2044e-10 that the
      coincidence is about.  The extremal kernels miss nu = sqrt(1+1/y) by 0.37-0.55 dex, versus
      SPARC's 0.108 dex.

VERDICT: NO tree-level mechanism examined forces a single-scale psi; and the axiom would not
deliver r = 9 even if it did.  The 0.36% proximity of 2 c H_Lambda/9 to 1.20e-10 is a
COINCIDENCE -- it is a 0.65% tuning of a free shape exponent (p = 2 vs p = 1.9871).  sup r stays
+infinity.  kappa = 1/2 is NOT excluded and NOT derived; it remains FITTED.

AGAINST INTEREST (recorded in full, section I): p = 2 is an INTEGER exponent (a second-order pole)
while 2Z needs the fractional p = 1.405 and 4pi needs p = 1.292, so on any naturalness-of-exponent
ordering r = 9 beats the framework's own coefficient; the exact-law kernel sits within 1-12.5% of
the (A2) boundary for every r >= 9, i.e. the framework's kernel is nearly extremal; and under the
strict shape budgets (max|dex| <= 0.108, or rms <= 0.050) the single-scale class reaches only
r_obs ~ 9.34-9.38, which would bear against 2Z = 11.578 and 4 pi while ADMITTING r = 9, McGaugh's
9.0323 and the ALT 9.5919.  That last item is knife-edge and budget-dependent (the like-for-like
rms <= 0.108 reading gives 15.0 and admits everything, and a scan maximum is only a LOWER bound) --
reported with the fork, not as a result.

MANDATORY CREDIT.  nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9
(he fixes a_0_hat = 2 c H_Lambda, r = 1); his eqs 10-11 give a second coefficient (r = 2); Milgrom
2008 arXiv:0801.3133 sec 7.3.1 notes the coefficient mismatch "isn't necessarily meaningful".
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384.  T = sqrt(a^2+Lambda/3)/2pi:
Narnhofer, Peter and Thirring 1996 IJMPB 10:1507.  Five-acceleration: Deser and Levin 1997 CQG
14:L163.  Exponential kernel: McGaugh 2008 ApJ 683:137 eq 11a.  AQUAL: Bekenstein and Milgrom
1984.  Ghost condensate: Arkani-Hamed, Cheng, Luty, Mukohyama 2004.  Boost-breaking EFT: Nicolis,
Penco, Piazza, Rattazzi 2015.  GHY boundary term: Gibbons and Hawking 1977, York 1972.  Bernstein's
theorem on completely monotone functions: Bernstein 1929.  Empirical a_0 = 1.2e-10 and the 0.108
dex RAR scatter: McGaugh / Lelli-McGaugh-Schombert SPARC.

kappa = 1/2 IS FITTED, NOT DERIVED.  Nothing below changes that.
"""
import sys
import math
import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar, brentq, linprog
from mpmath import mp, mpf, sqrt as msqrt, log as mlog

mp.dps = 50
np.seterr(all="ignore")     # finiteness asserted explicitly where it matters

# ----------------------------------------------------------------- constants (locked footing)
CHL      = 5.4194e-10          # c H_Lambda [m/s^2]      canonical floor scale
A0_CANON = 9.3614e-11          # kappa = 1/2 canonical (rho_DE + c H_Lambda)
A0_ALT   = 1.13e-10            # ALT footing (x 1.2082)
A0_EMP   = 1.20e-10            # McGaugh empirical
OM_L     = 0.6847              # for the ALT reading cH_0 = cH_Lambda/sqrt(Omega_Lambda)
CH0      = CHL/math.sqrt(OM_L)
G_NEWT   = 6.67430e-11
RHO_L    = 5.844e-27           # kg/m^3 canonical
C_LIGHT  = 2.99792458e8
Z_CONST  = 2.0*math.sqrt(8.0*math.pi/3.0)
TWOZ     = 2.0*Z_CONST
FOURPI   = 4.0*math.pi
R_EMP    = 2.0*CHL/A0_EMP      # 9.0323...
R_ALT    = 2.0*CHL/A0_ALT      # 9.5919...
SPARC_DEX = 0.108              # framework-kernel RAR scatter (rar_framework_a0_mlfit.py)

TARGETS = [("9  (menu ceiling)", 9.0),
           ("9.0323 McGaugh 1.20e-10", R_EMP),
           ("9.5919 ALT 1.13e-10", R_ALT),
           ("11.5776 2Z kappa=1/2", TWOZ),
           ("12.5664 4pi Milgrom 2020", FOURPI)]

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok))
    print(("[OK]   " if ok else "[FAIL] ") + name + (("\n       " + detail) if detail else ""))

def banner(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

# =========================================================================================
# core numerics
# =========================================================================================
def pow_psi(s, d, p):
    """psi = (1+s/d)^-p and Psi = Int_0^s psi, both cancellation-free (log1p/expm1)."""
    u = np.asarray(s, float)/d
    l1 = np.log1p(u)
    psi = np.exp(-p*l1)
    q = p - 1.0
    if abs(q) < 1e-13:
        Psi = d*l1
    else:
        Psi = d*(-np.expm1(-q*l1))/q
    return psi, Psi

def exp_psi(s, d):
    u = np.asarray(s, float)/d
    return np.exp(-u), d*(-np.expm1(-u))

def J_of(s, psi, Psi, T=1.0, newton_bug=False):
    """(A2) ratio.  lam <= 1/sup J.  newton_bug=True reinstates the historical 's' for 's*T'."""
    den = (s*1.0) if newton_bug else (s*T)
    return (Psi*(s + T) - psi*s*(s + 2.0*T))/den

def lam_max_num(psi_fn, T=1.0, lo=-15.0, hi=11.0, n=1200001, newton_bug=False):
    s = np.logspace(lo, hi, n)*T
    psi, Psi = psi_fn(s)
    J = J_of(s, psi, Psi, T, newton_bug)
    assert np.all(np.isfinite(J)), "non-finite J"
    i = int(np.argmax(J))
    return 1.0/J[i], s[i], J[i]

# --- the d -> 0 ceiling functional:  sup_u [ X(u)/u - 2 chi(u) ]  (scale-free) --------------
def J0_pow(u, p):
    u = np.asarray(u, float)
    l1 = np.log1p(u)
    chi = np.exp(-p*l1)
    q = p - 1.0
    X = (l1 if abs(q) < 1e-13 else (-np.expm1(-q*l1))/q)
    return X/u - 2.0*chi

def supJ0_pow(p):
    u = np.logspace(-8, 8, 400001)
    J = J0_pow(u, p)
    i = int(np.argmax(J))
    lu = math.log10(u[i])
    res = minimize_scalar(lambda t: -float(J0_pow(10.0**t, p)),
                          bracket=(lu - 0.05, lu, lu + 0.05))
    return -res.fun, 10.0**res.x

def r_ceiling_pow(p):
    return 1.0 + 1.0/supJ0_pow(p)[0]

# =========================================================================================
banner("A  ARITHMETIC FIRST: a_0 = 2 c H_Lambda/9 to ten digits, BOTH footings")

a0_r9_canon = 2.0*CHL/9.0
a0_r9_alt   = 2.0*CH0/9.0
print("  canonical floor  c H_Lambda = %.6e m/s^2   ->  a_0(r=9) = %.10e m/s^2" % (CHL, a0_r9_canon))
print("  ALT-floor reading c H_0     = %.6e m/s^2   ->  a_0(r=9) = %.10e m/s^2" % (CH0, a0_r9_alt))
print("  distance of a_0(r=9)|canonical to  McGaugh 1.20e-10   : %+8.4f %%" % (100*(a0_r9_canon/A0_EMP - 1)))
print("  distance of a_0(r=9)|canonical to  framework 9.3614e-11: %+8.4f %%" % (100*(a0_r9_canon/A0_CANON - 1)))
print("  distance of a_0(r=9)|canonical to  ALT 1.13e-10        : %+8.4f %%" % (100*(a0_r9_canon/A0_ALT - 1)))
print("  distance of a_0(r=9)|ALT-floor to  framework 9.3614e-11: %+8.4f %%" % (100*(a0_r9_alt/A0_CANON - 1)))
check("A1 a_0(r=9) = 1.204311111e-10 m/s^2 on the canonical floor, +0.3593% from McGaugh's "
      "1.20e-10 and +28.647% from the framework's 9.3614e-11",
      abs(a0_r9_canon - 1.204311111e-10) < 1e-19
      and abs(100*(a0_r9_canon/A0_EMP - 1) - 0.3593) < 2e-3
      and abs(100*(a0_r9_canon/A0_CANON - 1) - 28.647) < 2e-2,
      "the 0.36% is real arithmetic; sections C-E price what it is worth")

print("\n  the SAME statement as an r-table (r = 2 c H_Lambda/a_0, one floor, several a_0):")
print("  %-28s %12s %14s %12s" % ("coefficient", "r", "a_0 [m/s^2]", "% above 9"))
for nm, R in TARGETS:
    print("  %-28s %12.6f %14.4e %+11.3f" % (nm, R, 2.0*CHL/R, 100*(R/9.0 - 1)))
check("A2 the four coefficients on one floor: 9 -> 1.2043e-10, 9.0323 -> 1.2000e-10, 9.5919 -> "
      "1.1300e-10, 2Z = 11.5776 -> 9.3614e-11, 4pi = 12.5664 -> 8.6247e-11; 2Z is 28.640% above "
      "9 and 4pi is 39.626% above",
      abs(2.0*CHL/TWOZ - A0_CANON)/A0_CANON < 3e-4 and abs(100*(TWOZ/9 - 1) - 28.640) < 2e-2
      and abs(100*(FOURPI/9 - 1) - 39.626) < 2e-2,
      "the two ALT readings differ: 'same floor, a_0 = 1.13e-10' needs r = %.4f (6.6%% above 9), "
      "'ALT floor cH_0 at r = 9' gives a_0 = %.4e (%.2f%% above canonical). BOTH reported "
      "everywhere below." % (R_ALT, a0_r9_alt, 100*(a0_r9_alt/A0_CANON - 1)))

# footing cross-check demanded by the brief: the pi-free corner's sqrt(6)/8
A_hor_sym, rho, Gs, cs = sp.symbols("A_hor rho G c", positive=True)
A_hor_expr = 3*cs**2/(2*Gs*rho)
lhs = sp.simplify(cs**2/sp.sqrt(A_hor_expr)*sp.sqrt(6)/8)
rhs = sp.Rational(1, 4)*cs*sp.sqrt(Gs*rho)
print("\n  pi-free corner: c^2/sqrt(A_hor) * sqrt(6)/8 = %s ;  a_0/2 = (1/4) c sqrt(G rho_L) = %s"
      % (sp.simplify(lhs), rhs))
a0_from_rho = 0.5*C_LIGHT*math.sqrt(G_NEWT*RHO_L)
check("A3 sqrt(6)/8 = 2^(-5/2) 3^(1/2) = 0.306186217848 is the EXACT factor on c^2/sqrt(A_hor) "
      "that gives the framework's floor k = a_0/2 (sympy, symbol-for-symbol), and the numbers "
      "close: a_0 = (1/2) c sqrt(G rho_L) = %.6e vs the brief's 9.3614e-11" % a0_from_rho,
      sp.simplify(lhs - rhs) == 0
      and abs(math.sqrt(6)/8 - 0.306186217848) < 1e-12
      and abs(a0_from_rho/A0_CANON - 1) < 3e-3,
      "verified independently as the brief requires before use; A_hor = 4pi/H^2 with "
      "H^2 = 8 pi G rho/3 is pi-free")

# =========================================================================================
banner("B  THE FUNCTIONAL, RE-DERIVED, AND THE DIMENSIONAL-RESCALING REPRODUCTION CHECK")

sS, TS, lS, c1S = sp.symbols("s T lam c1p", positive=True)
psiS = sp.Function("psi")
PsiS = sp.Function("Psi")
Fsym = c1S*(sS + lS*PsiS(sS))
Fp = c1S*(1 + lS*sp.Derivative(PsiS(sS), sS))
A2 = sp.expand(sp.simplify((Fp*sS*(sS + 2*TS) - Fsym*(sS + TS)).subs(
    sp.Derivative(PsiS(sS), sS), psiS(sS))/c1S))
target = sp.expand(sS*TS + lS*(psiS(sS)*sS*(sS + 2*TS) - PsiS(sS)*(sS + TS)))
print("  (A2) bracket F' s(s+2T) - F (s+T), divided by c1p, expanded:")
print("      %s" % A2)
print("  claimed identity  s*T + lam[psi s(s+2T) - Psi (s+T)]:")
print("      %s" % target)
check("B1 the (A2) Newtonian term is s*T, NOT s (sympy identity, difference = 0). This is the "
      "exact bug that bit the corpus once; it is re-derived here from F and F' rather than copied",
      sp.simplify(A2 - target) == 0)

# rescaling reproduction: T_GH = 1 with scale d must equal T_GH = 3.7 with scale 3.7 d
T2 = 3.7
for p in (1.3, 2.0):
    lm1, s1, _ = lam_max_num(lambda s: pow_psi(s, 1e-3, p), T=1.0, n=600001)
    lm2, s2, _ = lam_max_num(lambda s: pow_psi(s, 1e-3*T2, p), T=T2, n=600001)
    print("  p = %.2f:  lam_max(T=1, d=1e-3) = %.10f   lam_max(T=3.7, d=3.7e-3) = %.10f   "
          "s*/T ratio = %.6f" % (p, lm1, lm2, (s2/T2)/s1))
    if p == 2.0:
        keep = (lm1, lm2, s1, s2)
lmB1, lmB2, sB1, sB2 = keep
lmbug1, _, _ = lam_max_num(lambda s: pow_psi(s, 1e-3, 2.0), T=1.0, n=600001, newton_bug=True)
lmbug2, _, _ = lam_max_num(lambda s: pow_psi(s, 1e-3*T2, 2.0), T=T2, n=600001, newton_bug=True)
print("  NEGATIVE CONTROL (Newtonian term s instead of s*T): %.8f vs %.8f -- ratio %.4f, "
      "invariance DESTROYED" % (lmbug1, lmbug2, lmbug2/lmbug1))
check("B2 lam_max is invariant under the dimensional rescaling (T_GH, d) -> (3.7 T_GH, 3.7 d) to "
      "%.1e relative, and the binding point s* scales with T_GH; the NEGATIVE CONTROL that uses "
      "s for s*T breaks the invariance by a factor %.3f, so this check can fail"
      % (abs(lmB2/lmB1 - 1), lmbug2/lmbug1),
      abs(lmB2/lmB1 - 1) < 1e-6 and abs((sB2/T2)/sB1 - 1) < 1e-6
      and abs(lmbug2/lmbug1 - 1) > 0.5)

# mpmath cancellation guard at the binding point
def J_mp(sv, d, p, T=1.0):
    sv, d, T = mpf(sv), mpf(d), mpf(T)
    u = sv/d
    chi = (1 + u)**(-mpf(p))
    X = (1 - (1 + u)**(1 - mpf(p)))/(mpf(p) - 1)
    return ((d*X)*(sv + T) - chi*sv*(sv + 2*T))/(sv*T)
worst = 0.0
for sv in (1e-6, 1e-3, 3e-3, 1e-1, 1.0, 1e3):
    f64 = float(J_of(np.array([sv]), *pow_psi(np.array([sv]), 1e-3, 2.0))[0])
    ref = float(J_mp(sv, 1e-3, 2.0))
    worst = max(worst, abs(f64 - ref)/max(abs(ref), 1e-300))
check("B3 float64 J agrees with 50-digit mpmath to %.1e relative at six decades incl. the binding "
      "point s* ~ 3d, so sup J is not a cancellation artefact" % worst, worst < 1e-9)

# =========================================================================================
banner("C  ACHIEVABLE r BY KERNEL CLASS -- the premise 'single-scale => r <= 9' TESTED")

# C1: p = 2 gives EXACTLY 9, symbolically
u = sp.symbols("u", positive=True)
J0_p2 = sp.simplify(sp.Rational(1, 1)/(1 + u) - 2/(1 + u)**2)     # X/u - 2 chi at p = 2
crit = sp.solve(sp.diff(J0_p2, u), u)
print("  p = 2, d -> 0:  J_0(u) = X(u)/u - 2 chi(u) = %s,  critical u = %s,  J_0 = %s"
      % (J0_p2, crit, sp.simplify(J0_p2.subs(u, crit[0]))))
dsym = sp.symbols("d", positive=True)
lam_pl = 4*(2 - dsym)**2/(2 + 7*dsym - 4*dsym**2)
print("  committed closed form 4(2-d)^2/(2+7d-4d^2) at d -> 0 : %s" % sp.limit(lam_pl, dsym, 0))
lm_p2_d, _, _ = lam_max_num(lambda s: pow_psi(s, 1e-7, 2.0), n=2000001)
print("  direct numeric lam_max(p=2, d=1e-7) = %.9f   (closed form %.9f)"
      % (lm_p2_d, float(lam_pl.subs(dsym, 1e-7))))
BUG_lam_pl = 4*(2 - dsym)/(2 + 7*dsym - 4*dsym**2)                # negative control
check("C1 the menu ceiling is r = 9 EXACTLY: sup_u J_0 = 1/8 at u = 3 for p = 2 (sympy), the "
      "committed closed form -> 8, and the direct numeric agrees to %.1e. NEGATIVE CONTROL: the "
      "corrupted closed form 4(2-d)/(...) gives %.4f, not 8, so this check can fail"
      % (abs(lm_p2_d - 8.0), float(sp.limit(BUG_lam_pl, dsym, 0))),
      crit == [3] and sp.simplify(J0_p2.subs(u, 3) - sp.Rational(1, 8)) == 0
      and sp.limit(lam_pl, dsym, 0) == 8 and abs(lm_p2_d - 8.0) < 1e-4
      and abs(float(sp.limit(BUG_lam_pl, dsym, 0)) - 8.0) > 1.0)

# C2: single exponential = ONE relaxation rate, ONE pole in the conjugate variable
g_exp = lambda t: -float((-np.expm1(-10.0**t))/10.0**t - 2*np.exp(-10.0**t))
resE = minimize_scalar(g_exp, bracket=(0.3, 0.51, 0.8))
sup_exp, u_exp = -resE.fun, 10.0**resE.x
r_exp = 1.0 + 1.0/sup_exp
lm_exp_fin, _, _ = lam_max_num(lambda s: exp_psi(s, 1e-6), n=2000001)
print("  SINGLE EXPONENTIAL psi = e^(-s/d)  (one relaxation rate; one pole in the conjugate var):")
print("      sup J_0 = %.10f at u* = %.6f  ->  r = %.8f   (finite d = 1e-6: r = %.8f)"
      % (sup_exp, u_exp, r_exp, 1.0 + lm_exp_fin))
print("      => a_0 = %.4e (canonical floor) / %.4e (ALT floor)" % (2*CHL/r_exp, 2*CH0/r_exp))
check("C3 the ONE kernel a single relaxation process actually supplies -- psi = e^(-s/d) -- gives "
      "r = 5.5820826, i.e. a_0 = 1.9418e-10 canonical. It MISSES ALL FOUR targets LOW (38% below "
      "9, 52% below 2Z), so the mechanism-forced single-scale kernel does not deliver the "
      "coincidence; it delivers a number no footing wants",
      abs(r_exp - 5.58208263) < 1e-6 and abs(1.0 + lm_exp_fin - r_exp) < 1e-4
      and r_exp < 9.0 and 2*CHL/r_exp > 1.9e-10)

# C3: single POLE in s -- the Lorentzian/Debye saturation
lm_pole, s_pole, _ = lam_max_num(lambda s: pow_psi(s, 1e-3, 1.0), lo=-14, hi=60, n=2000001)
_, Psi_pole = pow_psi(np.array([1e30]), 1e-3, 1.0)
print("  SINGLE POLE psi = (1+s/d)^-1 (Lorentzian saturation): Psi(inf) DIVERGES "
      "(Psi(1e30) = %.4f and growing like d ln s) => (A1) lam Psi(inf) <= T forces lam = 0, "
      "r = 1 EXACTLY" % Psi_pole[0])
print("      r = 1 is Milgrom 1999's OWN coefficient a_0_hat = 2 c H_Lambda = %.4e." % (2*CHL))
print("      HONEST CAVEAT: the exclusion is a formal tail constraint -- mu exceeds 1 only beyond "
      "s ~ d exp(1/(lam d)); over any finite range the pole behaves like the p -> 1+ limit below.")
check("C4 the single-pole (Debye/Lorentzian) response is EXCLUDED by (A1) and collapses to r = 1 = "
      "2 c H_Lambda, Milgrom 1999's own value, because Int (1+s/d)^-1 ds diverges logarithmically",
      Psi_pole[0] > 5*1e-3*math.log(1e30/1e-3)*0.9 or Psi_pole[0] > 0.05)

# C4: *** THE KILL -- the fractional-power band 1 < p < 2 ***
print("\n  *** the ONE-PARAMETER single-scale family psi = (1+s/d)^-p, d -> 0 ceiling: ***")
print("  %8s %14s %12s %14s" % ("p", "sup J_0", "r_max", "a_0 canon"))
rows = []
for p in (100.0, 6.0, 3.0, 2.0, 1.7, 1.5, 1.405, 1.3, 1.292, 1.2, 1.1, 1.05, 1.01, 1.001):
    sj, us = supJ0_pow(p)
    rc = 1.0 + 1.0/sj
    rows.append((p, sj, rc))
    print("  %8.3f %14.9f %12.6f %14.4e" % (p, sj, rc, 2*CHL/rc))
r_lim_p1 = 1.0 + 1.0/(-minimize_scalar(
    lambda t: -float(np.log1p(10.0**t)/10.0**t - 2.0/(1 + 10.0**t)),
    bracket=(0.9, 1.12, 1.4)).fun)
print("  p -> 1+ ceiling of the family (closed functional ln(1+u)/u - 2/(1+u)): r -> %.8f" % r_lim_p1)
print("  p -> inf ceiling: r -> %.8f (the single exponential)" % r_exp)
p_at = {}
for nm, R in TARGETS:
    p_at[nm] = brentq(lambda pp: r_ceiling_pow(pp) - R, 1.0001, 60.0, xtol=1e-11)
    print("  r = %11.6f (%-24s) is reached by the SINGLE-SCALE shape p = %.8f" % (R, nm, p_at[nm]))
# rows run from large p to small p, so r_max must INCREASE monotonically down the list
mono = all(rows[i][2] > rows[i - 1][2] for i in range(1, len(rows)))
check("C5 *** THE PREMISE IS FALSE: single-scale does NOT imply r <= 9. *** The one-parameter, "
      "unimodal, completely monotone, C^infinity family (1+s/d)^-p has a strictly decreasing "
      "ceiling r_max(p) spanning (%.5f, %.5f), and ALL FOUR targets sit inside it: 9 at p = 2 "
      "exactly, 9.0323 at p = 1.98710, 2Z at p = 1.40509, 4pi at p = 1.29215. This check FAILS if "
      "r_max(1.3) <= 9 or if the family is not monotone in p" % (r_exp, r_lim_p1),
      mono and r_ceiling_pow(1.3) > 9.0 and r_ceiling_pow(1.405) > TWOZ*0.999
      and r_ceiling_pow(1.292) > FOURPI*0.999
      and abs(p_at["9  (menu ceiling)"] - 2.0) < 1e-7
      and abs(r_lim_p1 - 17.62251305) < 1e-5,
      "the committed 7-shape menu contained only the INTEGER exponents p = 2, 3 plus "
      "faster-decaying shapes; the entire band 1 < p < 2 was unsampled. 9 was a MENU artefact, "
      "not a class ceiling -- float64 hazard 'coarse grids reporting unsampled extrema', on a "
      "grid over SHAPES rather than over s")
check("C6 and the coincidence is quantitatively worthless: p = 2 gives 1.20431e-10 while McGaugh's "
      "1.20e-10 needs p = 1.98710 -- a 0.65%% shift of a FREE shape exponent. The family covers "
      "a_0 in [%.4e, %.4e], a factor %.2f, which CONTAINS 9.3614e-11, 1.13e-10, 1.20e-10 and "
      "c H_Lambda/2pi = %.4e alike"
      % (2*CHL/r_lim_p1, 2*CHL/r_exp, r_lim_p1/r_exp, CHL/(2*math.pi)),
      abs(100*(p_at["9  (menu ceiling)"]/p_at["9.0323 McGaugh 1.20e-10"] - 1) - 0.649) < 0.05
      and 2*CHL/r_lim_p1 < A0_CANON < 2*CHL/r_exp
      and 2*CHL/r_lim_p1 < CHL/(2*math.pi) < 2*CHL/r_exp)

# C5: completely monotone LP (reproduce the psi-search F4 result: unbounded)
def cm_lp(tlo, thi, NT=140, xlo=1e-10, xhi=1e6, NX=800):
    t = np.logspace(math.log10(tlo), math.log10(thi), NT)
    xv = np.logspace(math.log10(xlo), math.log10(xhi), NX)
    TX = np.outer(xv, t)
    Jm = (1 + 1/xv)[:, None]*(-np.expm1(-TX))/t[None, :] - (xv + 2)[:, None]*np.exp(-TX)
    A = np.hstack([Jm, -np.ones((NX, 1))])
    Aeq = np.zeros((1, NT + 1)); Aeq[0, :NT] = 1.0
    obj = np.zeros(NT + 1); obj[-1] = 1.0
    res = linprog(obj, A_ub=A, b_ub=np.zeros(NX), A_eq=Aeq, b_eq=[1.0],
                  bounds=[(0, None)]*NT + [(-2, 5)], method="highs")
    return 1.0 + 1.0/res.x[-1]
print("\n  COMPLETELY MONOTONE class (Bernstein: psi = Int e^(-s t) drho(t), rho >= 0), LP over rho:")
cmv = {}
for thi in (1e2, 1e4, 1e6, 1e8):
    cmv[thi] = cm_lp(1e-2, thi)
    print("      rate range [1e-2, %.0e]:  r_max = %12.4f" % (thi, cmv[thi]))
check("C7 complete monotonicity is STRICTLY WEAKER than 'one relaxation process', and by an "
      "unbounded amount: a single exponential caps r at %.4f, while the LP over the whole CM cone "
      "gives r_max = %.2f -> %.0f as the spectral range widens (~sqrt(t_max)), reproducing the "
      "psi-search F4 result. A superposition of exponentials is NOT single-scale, so Bernstein "
      "positivity supplies no ceiling at all" % (r_exp, cmv[1e2], cmv[1e8]),
      cmv[1e2] > r_exp and cmv[1e8]/cmv[1e4] > 5 and cmv[1e2] > TWOZ)

# C6: two-scale product (reproduce the psi-search F3 exhibit's ceiling)
dlt, Dlt = 1e-3, 1e-1
def prod_psi(s):
    s = np.asarray(s, float)
    psi = (1.0 + s/dlt)**-0.5/(1.0 + s/Dlt)
    KAP = math.sqrt(dlt/(Dlt - dlt))
    qq = np.sqrt(1.0 + s/dlt)
    Psi = 2*Dlt*KAP*np.arctan(KAP*(s/dlt)/((qq + 1.0)*(1.0 + KAP*KAP*qq)))
    return psi, Psi
lm_two, _, _ = lam_max_num(prod_psi, n=2000001)
print("\n  TWO-SCALE product psi = (1+s/1e-3)^-1/2 (1+s/1e-1)^-1 (CM, real-analytic): r_max = %.4f"
      % (1 + lm_two))
check("C8 the two-scale CM product reaches r_max = %.2f, above every target -- reproducing the "
      "psi-search F3 exhibit. Ordering of ceilings: single exponential %.3f < p=2 power 9 < "
      "fractional power %.3f < two-scale %.1f < CM cone infinity"
      % (1 + lm_two, r_exp, r_lim_p1, 1 + lm_two),
      1 + lm_two > FOURPI and 1 + lm_two > r_lim_p1)

print("\n  === TABLE 4 (the brief's item 4): achievable r by kernel class vs the four targets ===")
print("  %-42s %12s %6s %8s %8s %8s" % ("kernel class", "r ceiling", "9", "9.0323", "11.5776", "12.5664"))
def mk_row(nm, rr):
    f = lambda t: (" yes" if rr >= t*(1 - 1e-9) else "  no")
    print("  %-42s %12.4f %6s %8s %8s %8s" % (nm, rr, f(9.0), f(R_EMP), f(TWOZ), f(FOURPI)))
mk_row("single exponential (one rate/one pole)", r_exp)
mk_row("single pole (1+s/d)^-1  [(A1)-excluded]", 1.0)
mk_row("single-scale power p = 3", r_ceiling_pow(3.0))
mk_row("single-scale power p = 2 (double pole)", 9.0)
mk_row("single-scale power p -> 1+", r_lim_p1)
mk_row("completely monotone cone (Bernstein)", cmv[1e8])
mk_row("two-scale CM product", 1 + lm_two)
mk_row("exact-law kernel (section D)", float("inf"))

# =========================================================================================
banner("D  THE FRAMEWORK'S OWN EXACT LAW IS IN THE CLASS -- ADMISSIBLE AT EVERY r, TWO-SCALE")

sq, qq_, lq, Tq = sp.symbols("s q lam T", positive=True)
D_sym = sp.sqrt(qq_**2 + 4*sq*(sq + 2*Tq))
Phi_law = (-qq_ + D_sym)/2
law_res = sp.simplify(Phi_law**2 + qq_*Phi_law - sq*(sq + 2*Tq))
Phip = sp.simplify(sp.diff(Phi_law, sq))
psi_law_sym = sp.simplify((Phip - 1)/lq)
dpsi_num = sp.simplify(sp.diff(Phip, sq))
Psi_inf = sp.simplify(sp.limit(Phi_law - sq, sq, sp.oo))
print("  Phi_law = (-q + sqrt(q^2+4s(s+2T)))/2   solves  Phi^2 + q Phi = s(s+2T)  exactly: "
      "residual = %s" % law_res)
print("  Phi_law'(s) = %s      Phi_law'(0) = %s  =>  r = 2T/q, i.e. q = 2/r  (the CRP formula)"
      % (Phip, sp.limit(Phip, sq, 0, "+")))
print("  psi_law = %s" % psi_law_sym)
print("  d(Phi')/ds = %s   -> psi_law strictly DECREASING iff q < 2T iff r > 1" % dpsi_num)
print("  Psi_law(inf) = lim (Phi - s) = %s   =>  lam Psi(inf) = 1 - 1/r < 1  identically" % Psi_inf)
BUG_law = sp.simplify(((-2*qq_ + sp.sqrt(4*qq_**2 + 4*sq*(sq + 2*Tq)))/2)**2
                      + qq_*((-2*qq_ + sp.sqrt(4*qq_**2 + 4*sq*(sq + 2*Tq)))/2) - sq*(sq + 2*Tq))
check("D1 the exact law g_obs^2 = g_bar^2 + a_0 g_bar IS a member of the master-formula class, with "
      "the closed-form Phi above (sympy residual 0), and it reproduces q = 2/r from Phi'(0) = 2T/q "
      "-- so the framework's own law fixes psi UNIQUELY given r. NEGATIVE CONTROL: q -> 2q inside "
      "the radical leaves residual %s != 0, so this check can fail" % sp.simplify(BUG_law),
      law_res == 0 and sp.limit(Phip, sq, 0, "+") == 2*Tq/qq_ and sp.simplify(BUG_law) != 0)
check("D2 psi_law is admissible EXACTLY when r > 1: sign(dpsi/ds) = sign(q^2 - 4T^2) (sympy), so "
      "monotone decrease holds iff q < 2T iff a_0 < 2 c H_Lambda. That is the ONLY bound the class "
      "puts on a_0 -- a_0 < %.4e -- and every candidate satisfies it" % (2*CHL),
      sp.simplify(dpsi_num - 2*(qq_**2 - 4*Tq**2)/(qq_**2 + 4*sq*(sq + 2*Tq))**sp.Rational(3, 2)) == 0
      and sp.simplify(Psi_inf - (Tq - qq_/2)) == 0)

# numeric exact-law kernel, cancellation-free
def exact_law_arrays(r, T=1.0, lo=-16, hi=12, n=1500001):
    q = 2.0*T/r
    lam = r - 1.0
    s = np.logspace(lo, hi, n)*T
    D = np.sqrt(q*q + 4.0*s*(s + 2.0*T))
    Phi = 2.0*s*(s + 2.0*T)/(D + q)                    # cancellation-free (-q+D)/2
    psi = (4.0*T*T - q*q)/(lam*D*(2.0*(s + T) + D))    # cancellation-free 2(s+T)/D - 1
    Psi = 2.0*s*(2.0*T - q)/(lam*(D + q + 2.0*s))      # cancellation-free (Phi - s)/lam
    w = np.sqrt(s*(s + 2.0*T))
    return dict(s=s, psi=psi, Psi=Psi, Phi=Phi, w=w, q=q, lam=lam, T=T)

# float hazard: the naive forms lose all digits.  mpmath cross-check.
K9 = exact_law_arrays(9.0)
naive_psi = 2.0*(K9["s"] + 1.0)/np.sqrt(K9["q"]**2 + 4*K9["s"]*(K9["s"] + 2)) - 1.0
def psi_mp(sv, r):
    q = mpf(2)/mpf(r); lam = mpf(r) - 1
    D = msqrt(q*q + 4*mpf(sv)*(mpf(sv) + 2))
    return (2*(mpf(sv) + 1)/D - 1)/lam
worst2 = 0.0; worstn = 0.0
for sv in (1e-8, 1e-3, 1.0, 1e4, 1e8):
    i = int(np.argmin(abs(K9["s"] - sv)))
    ref = float(psi_mp(K9["s"][i], 9.0))
    worst2 = max(worst2, abs(K9["psi"][i] - ref)/max(abs(ref), 1e-300))
    worstn = max(worstn, abs(naive_psi[i]/(9.0 - 1.0) - ref)/max(abs(ref), 1e-300))
print("\n  psi_law: cancellation-free form vs 50-digit mpmath: %.2e relative worst over 5 decades" % worst2)
print("  the NAIVE form 2(s+T)/D - 1 (a difference of two -> 1 quantities): %.2e relative -- "
      "float64 hazard 'catastrophic cancellation in sqrt(1+a^2)-1' realised" % worstn)
check("D3 the algebraic rewrite psi_law = (4T^2-q^2)/(lam D (2(s+T)+D)) is exact and stable "
      "(%.1e vs mpmath) where the naive difference form loses %.0f orders of magnitude at large s "
      "-- the rewrite is load-bearing, not cosmetic" % (worst2, math.log10(max(worstn, 1e-300)) + 16),
      worst2 < 1e-12 and worstn > 1e4*worst2)

print("\n  %-12s %10s %12s %12s %14s %12s %10s" % ("r", "lam", "lam_max", "margin", "lam Psi(inf)",
                                                   "max|dex| nu", "mu<=1"))
adm = []
for r in (2.0, 9.0, R_EMP, R_ALT, TWOZ, FOURPI, r_lim_p1, 100.0):
    K = exact_law_arrays(r)
    J = J_of(K["s"], K["psi"], K["Psi"], K["T"])
    lmx = 1.0/J.max()
    mu = K["Phi"]/K["w"]
    y = K["Phi"]/K["q"]
    sel = (y >= 1e-2) & (y <= 1e2)
    dex = np.max(np.abs(np.log10((1.0/mu[sel])/np.sqrt(1.0 + 1.0/y[sel]))))
    lamPsi = (1 - K["q"]/(2*K["T"]))
    adm.append((r, K["lam"], lmx, dex, lamPsi, mu.max()))
    print("  %-12.5f %10.4f %12.4f %11.2f%% %14.8f %12.2e %10s"
          % (r, K["lam"], lmx, 100*(lmx/K["lam"] - 1), lamPsi, dex, mu.max() <= 1 + 1e-12))
check("D4 *** the exact-law kernel is ADMISSIBLE AT EVERY r TESTED (2, 9, 9.03, 9.59, 2Z, 4pi, "
      "17.6, 100): lam <= lam_max on (A2), lam Psi(inf) = 1 - 1/r < 1 on (A1), mu <= 1. So the "
      "class puts NO ceiling on the framework's own kernel and the would-be exclusion of "
      "kappa = 1/2 is VOID *** (this check FAILS if any r has lam > lam_max or mu > 1)",
      all(a[1] <= a[2]*(1 + 1e-9) and a[5] <= 1 + 1e-12 and a[4] < 1.0 for a in adm))
check("D5 and it reproduces nu = sqrt(1+1/y) to %.1e dex over y in [1e-2, 1e2] at every r, by "
      "construction -- validating the mu/y/nu pipeline used for the dex comparisons in section E"
      % max(a[3] for a in adm),
      max(a[3] for a in adm) < 1e-12)

# two-scale structure of psi_law.  The exact asymptotics are
#   s << q^2/8T : psi -> 1                      (log-log slope 0)
#   q^2/8T << s << T : psi ~ (2T/lam)/sqrt(8Ts) (slope 1/2)  -- the INTERMEDIATE regime
#   s >> T      : psi ~ (4T^2-q^2)/(4 lam s^2)  (slope 2)
# so the slope must traverse 0 -> 2 through an intermediate 1/2 shelf whose width grows with the
# scale separation 8T^2/q^2 = 2r^2.  A one-parameter single-scale kernel (1+s/d)^-p has a slope
# that runs 0 -> p with ONE crossover and cannot do this.
def slope_window(s, psi, lo=0.4, hi=0.6):
    sl = -np.gradient(np.log(psi), np.log(s))
    m = (sl >= lo) & (sl <= hi)
    return (0.0 if not m.any() else float(np.log10(s[m].max()/s[m].min()))), sl

print("\n  log-log slope -d ln psi_law/d ln s: it must run 0 -> 2 through an intermediate 1/2 shelf")
print("  %-12s %10s %14s %14s %16s" % ("r", "2 r^2", "slope@geo-mean", "[0.4,0.6] width",
                                       "inner break a/a_0"))
two_scale_ok = True
law_widths = {}
for r in (2.0, 9.0, TWOZ, FOURPI, 100.0, 1.0e4):
    K = exact_law_arrays(r, n=2000001, lo=-20, hi=12)
    wdt, sl = slope_window(K["s"], K["psi"])
    gm = K["q"]/(2.0*math.sqrt(2.0))                 # geometric mean of q^2/8 and T=1
    i = int(np.argmin(abs(K["s"] - gm)))
    s_in = K["q"]**2/8.0
    a_in = math.sqrt(s_in*(s_in + 2.0))
    law_widths[r] = wdt
    mono_slope = bool(np.all(np.diff(sl[200:-200]) > -1e-8))
    # EXACT: s_in = q^2/8T  =>  a_in = (q/2) sqrt(1 + q^2/16T^2), i.e. a_0/2 up to O(1/r^2)
    a_exact = 0.5*K["q"]*math.sqrt(1.0 + K["q"]**2/16.0)
    print("  %-12.4f %10.2f %14.4f %14.4f %16.6f   (exact (1/2)sqrt(1+q^2/16) = %.6f)  mono: %s"
          % (r, 2*r*r, sl[i], wdt, a_in/K["q"], a_exact/K["q"], mono_slope))
    two_scale_ok &= mono_slope and abs(a_in/a_exact - 1) < 1e-9
print("  the SAME statistic for single-scale power kernels (which have only ONE crossover):")
for p in (1.3, 2.0, 3.0):
    s_g = np.logspace(-20, 12, 2000001)
    wdt, _ = slope_window(s_g, pow_psi(s_g, 1e-3, p)[0])
    print("      p = %.1f: [0.4,0.6] width = %.4f decades (r-independent)" % (p, wdt))
    if p == 2.0:
        w_pow = wdt
two_scale_ok &= (law_widths[9.0] > 2*w_pow) and (law_widths[TWOZ] > law_widths[9.0])
q2Z = exact_law_arrays(TWOZ)["q"]
dev_half = abs(0.5*math.sqrt(1.0 + q2Z**2/16.0)/0.5 - 1)
check("D6 *** psi_law is irreducibly TWO-SCALE for every r > 1. *** Its log-log slope is monotone "
      "and traverses 0 -> 2 (exact asymptotics psi -> 1, then s^-1/2, then s^-2), the intermediate "
      "slope tends to 1/2 as the separation 2 r^2 grows (%.4f at r = 9, %.4f at 2Z, %.4f at "
      "r = 1e4), and the INNER break sits at a = (a_0/2) sqrt(1 + (a_0/4cH_L)^2) -- the framework's "
      "OWN floor k = a_0/2, exact up to O(1/r^2), which is %.3f%% at kappa = 1/2. The 1/2-shelf "
      "width is %.3f decades at r = 9 and %.3f at 2Z versus %.3f for ANY single-scale power kernel "
      "(r-independent), so a single-scale axiom would FORBID the framework's exact law: it is not "
      "merely unmotivated, it is inconsistent with the phenomenology it was invoked to explain"
      % (0.6699, 0.6533, 0.5059, 100*dev_half, law_widths[9.0], law_widths[TWOZ], w_pow),
      two_scale_ok and abs(8/exact_law_arrays(9.0)["q"]**2 - 2*81) < 1e-6 and dev_half < 1e-3)

# =========================================================================================
banner("E  FORMAL r vs OBSERVED a_0 -- what the ceiling kernels actually predict for the RAR")

def kernel_from_psi(psi_fn, lam, T=1.0, lo=-15, hi=11, n=1200001):
    s = np.logspace(lo, hi, n)*T
    psi, Psi = psi_fn(s)
    Phi = s + lam*Psi
    w = np.sqrt(s*(s + 2.0*T))
    return s, psi, Psi, Phi, w

def fit_a0line(Phi, w, a0seed, ylo=0.1, yhi=10.0, iters=16):
    """Least-squares a_0 in g_obs^2 - g_bar^2 = a_0 g_bar on the window y = g_bar/a_0 in [ylo,yhi],
    with the window made SELF-CONSISTENT in the fitted a_0.  Without the self-consistency the
    estimator is gameable: a window placed by the FORMAL a_0 can land in the Newtonian regime,
    where the a_0-line fits any small a_0 with vanishing residual and r_obs runs away."""
    a0 = a0seed
    for _ in range(iters):
        sel = (Phi/a0 >= ylo) & (Phi/a0 <= yhi)
        if sel.sum() < 64:
            return None
        X = Phi[sel]; Y = w[sel]**2 - X**2
        a0n = float(np.sum(X*Y)/np.sum(X*X))
        if a0n <= 0:
            return None
        conv = abs(a0n/a0 - 1) < 1e-12
        a0 = a0n
        if conv:
            break
    sel = (Phi/a0 >= ylo) & (Phi/a0 <= yhi)
    X = Phi[sel]; Y = w[sel]**2 - X**2
    dd = np.log10(w[sel]/np.sqrt(X**2 + a0*X))
    return a0, sel, dd

def rar_stats(psi_fn, lam, T=1.0, ylo=0.1, yhi=10.0, n=1200001):
    """Fit g_obs^2 = g_bar^2 + a_0_obs g_bar on the SPARC window; return r_obs and dex residuals."""
    s, psi, Psi, Phi, w = kernel_from_psi(psi_fn, lam, T, n=n)
    r = 1.0 + lam
    a0f = 2.0*T/r
    got = fit_a0line(Phi, w, a0f, ylo, yhi)
    if got is None:
        return dict(r_obs=0.0, dexmax=9e9, dexrms=9e9, a0o=0.0, d99=9e9, dmg=9e9, ok=False)
    a0o, sel, dd = got
    # shape distance to the two published kernels, at each kernel's OWN a_0
    y = Phi/a0f
    s2 = (y >= 1e-2) & (y <= 1e2)
    nu = w[s2]/Phi[s2]
    d99 = np.max(np.abs(np.log10(nu/np.sqrt(1.0 + 1.0/y[s2]))))
    dmg = np.max(np.abs(np.log10(nu*(-np.expm1(-np.sqrt(y[s2]))))))
    return dict(r_obs=2.0*T/a0o, dexmax=float(np.max(np.abs(dd))), dexrms=float(np.sqrt(np.mean(dd**2))),
                a0o=a0o, d99=d99, dmg=dmg, ok=True)

print("  the a_0-line fit on y in [0.1, 10] (SPARC's window) for the CEILING kernels:")
print("  %-34s %10s %10s %10s %10s %10s" % ("kernel", "r_formal", "r_obs", "a_0_obs", "dexmax", "dex(nu99)"))
E_rows = []
for nm, pf, dd_, pp in (("p=2 extremal, d=1e-8 (r->9)", pow_psi, 1e-8, 2.0),
                        ("p=2 extremal, d=1e-3", pow_psi, 1e-3, 2.0),
                        ("p=1.405 extremal, d=1e-8 (r->2Z)", pow_psi, 1e-8, 1.405),
                        ("p=1.292 extremal, d=1e-8 (r->4pi)", pow_psi, 1e-8, 1.292),
                        ("single exponential, d=1e-6", exp_psi, 1e-6, None)):
    fn = (lambda s, dd_=dd_, pp=pp: pow_psi(s, dd_, pp)) if pp else (lambda s, dd_=dd_: exp_psi(s, dd_))
    lmx, _, _ = lam_max_num(fn, n=1200001)
    st = rar_stats(fn, lmx)
    E_rows.append((nm, 1 + lmx, st))
    print("  %-34s %10.4f %10.4f %10.4e %10.4f %10.4f"
          % (nm, 1 + lmx, st["r_obs"], st["a0o"]*CHL, st["dexmax"], st["d99"]))
r_obs_9 = [e for e in E_rows if e[0].startswith("p=2 extremal, d=1e-8")][0][2]["r_obs"]
check("E1 *** the formal r is NOT the observed a_0 for the ceiling kernels. *** The p = 2, d -> 0 "
      "extremal kernel that attains r_formal = 9 has an a_0-LINE fit of r_obs = %.5f -- Milgrom "
      "1999's r = 1 -- so its OBSERVED MOND scale is 2 c H_Lambda = %.4e, a factor 9 from the "
      "1.2044e-10 the coincidence is about. The 0.36%% match is to a coefficient the construction "
      "does not deliver" % (r_obs_9, 2*CHL),
      abs(r_obs_9 - 1.0) < 1e-3)
check("E2 and the extremal kernels are observationally dead on SHAPE alone: max|dex| from "
      "nu = sqrt(1+1/y) is %.3f-%.3f over y in [1e-2,1e2], versus SPARC's 0.108 dex scatter on the "
      "framework's own kernel -- a factor %.1f-%.1f. Saturating (A2) is what buys large r, and "
      "saturating (A2) is what the RAR excludes"
      % (min(e[2]["d99"] for e in E_rows), max(e[2]["d99"] for e in E_rows),
         min(e[2]["d99"] for e in E_rows)/SPARC_DEX, max(e[2]["d99"] for e in E_rows)/SPARC_DEX),
      min(e[2]["d99"] for e in E_rows) > 2.0*SPARC_DEX)

# how much r_obs can a single-scale kernel deliver at a given RAR shape budget?
print("\n  max r_obs over the single-scale power class at a shape budget (scan over p, d, lam):")
S_SCAN = np.logspace(-14, 10, 60001)
W_SCAN = np.sqrt(S_SCAN*(S_SCAN + 2.0))
def scan_stats(p, d, lam):
    psi, Psi = pow_psi(S_SCAN, d, p)
    Phi = S_SCAN + lam*Psi
    lmx = 1.0/J_of(S_SCAN, psi, Psi, 1.0).max()
    got = fit_a0line(Phi, W_SCAN, 2.0/(1 + lam))
    if got is None:
        return lmx, 0.0, 9e9, 9e9
    a0o, sel, dd = got
    return lmx, 2.0/a0o, float(np.max(np.abs(dd))), float(np.sqrt(np.mean(dd**2)))
PGRID = np.concatenate([np.linspace(1.03, 3.0, 18), np.linspace(3.4, 10.0, 7)])
DGRID = np.logspace(-3, 1.1, 22)
best = {}
for p in PGRID:
    for d in DGRID:
        lmx, _, _, _ = scan_stats(p, d, 1.0)
        for f in np.linspace(0.06, 1.0, 16):
            lam = f*lmx
            lmx2, ro, dmx, drms = scan_stats(p, d, lam)
            if lam > lmx2*(1 + 1e-9):
                continue
            for key, val in (("max<=0.108", dmx <= 0.108), ("max<=0.050", dmx <= 0.050),
                             ("rms<=0.108", drms <= 0.108), ("rms<=0.050", drms <= 0.050)):
                if val and ro > best.get(key, (0,))[0]:
                    best[key] = (ro, p, d, lam, dmx, drms)
for key in ("rms<=0.108", "max<=0.108", "rms<=0.050", "max<=0.050"):
    ro, p, d, lam, dmx, drms = best[key]
    print("      budget %-10s ->  max r_obs = %8.4f  (a_0_obs = %.4e canon / %.4e ALT)   at "
          "p = %.3f, d = %.4f, lam = %.4f  [max %.4f, rms %.4f]"
          % (key, ro, 2*CHL/ro, 2*CH0/ro, p, d, lam, dmx, drms))
r_rms108 = best["rms<=0.108"][0]; r_max108 = best["max<=0.108"][0]
r_rms050 = best["rms<=0.050"][0]
check("E3 with the RAR SHAPE as the only extra input, the single-scale class reaches r_obs = %.2f at "
      "an rms budget of 0.108 dex, %.2f at a max|dex| budget of 0.108, and %.2f at rms <= 0.050. "
      "BOTH READINGS REPORTED because the choice is not innocent: rms is the like-for-like "
      "comparison with SPARC's 0.108 dex SCATTER and it ADMITS 2Z = 11.578 and 4 pi = 12.566, while "
      "the stricter max|dex| readings cap r_obs near 9.3-9.4 -- which would favour the 1.20e-10 "
      "corner over kappa = 1/2. NO exclusion is drawn from the strict reading: (i) the budget is "
      "arbitrary, (ii) a scan MAXIMUM is a LOWER bound on the true achievable r_obs so any "
      "exclusion built on it is unsafe, and (iii) grading a systematic shape against a random "
      "scatter is the exact error this corpus has logged twice"
      % (r_rms108, r_max108, r_rms050),
      r_rms108 > TWOZ and r_max108 > 9.0 and r_rms050 < r_rms108)

# the exact-law kernel: r_obs = r_formal at every r -- the estimator's POSITIVE CONTROL
print("\n  the exact-law (two-scale) kernel, same estimator: r_obs must equal r_formal exactly")
lawok = True
worst_law = 0.0
for r in (9.0, TWOZ, FOURPI, 100.0):
    K = exact_law_arrays(r, n=1200001)
    got = fit_a0line(K["Phi"], K["w"], K["q"])
    a0o, sel, dd = got
    worst_law = max(worst_law, abs(2.0/a0o/r - 1))
    print("      r_formal = %10.5f  ->  r_obs = %10.5f   (relative %.2e, max|dex| %.2e)"
          % (r, 2.0/a0o, abs(2.0/a0o/r - 1), np.max(np.abs(dd))))
    lawok &= abs(2.0/a0o/r - 1) < 1e-6 and np.max(np.abs(dd)) < 1e-12
check("E4 the exact-law kernel returns r_obs = r_formal to %.1e at every r with zero dex residual "
      "-- which is simultaneously the POSITIVE CONTROL on the a_0-line estimator used in E1/E3 and "
      "the statement that the escape from the single-scale trap is EXACTLY the second scale. Once "
      "you take it the RAR becomes NON-DIAGNOSTIC of r, consistent with the corpus finding that "
      "SPARC is convention-compatible and non-diagnostic of 9.36e-11" % worst_law, lawok)

# =========================================================================================
banner("F  THE MECHANISM AUDIT: does any tree-level process force a single-scale psi?")

# F1 scale-blindness theorem
print("  (0) SCALE-BLINDNESS.  ceiling functional sup_u [X(u)/u - 2 chi(u)] under u -> u/c:")
for p in (1.4, 2.0):
    base = supJ0_pow(p)[0]
    vals = []
    for c in (1e-3, 1.0, 1e3):
        # chi_c(u) = chi(u/c): X_c(u) = c X(u/c) -> X_c/u - 2 chi_c = X(v)/v - 2 chi(v), v = u/c
        uu = np.logspace(-8, 8, 400001)
        l1 = np.log1p(uu/c); chi = np.exp(-p*l1); X = c*(-np.expm1(-(p - 1)*l1))/(p - 1)
        vals.append(float(np.max(X/uu - 2*chi)))
    print("      p = %.2f:  sup J_0 = %.10f, %.10f, %.10f  for c = 1e-3, 1, 1e3  (spread %.1e)"
          % (p, *vals, max(vals) - min(vals)))
    if p == 2.0:
        spread = max(vals) - min(vals)
check("F1 *** SCALE-BLINDNESS THEOREM (numerically exact, spread %.1e): the ceiling functional is "
      "invariant under u -> u/c, so r is a pure SHAPE functional of psi and is completely blind to "
      "the kernel's SCALE. Every axiom of the form 'one relaxation time / one quasinormal "
      "frequency / one resonance / one attractor scale' fixes the SCALE and therefore constrains r "
      "NOT AT ALL. *** This is the structural reason the search below comes up empty" % spread,
      spread < 1e-9)

# F2 (a) single dS mode / one quasinormal frequency
Tsym, om = sp.symbols("T omega", positive=True)
nB = 1/(sp.exp(om/Tsym) - 1)
dnB = sp.simplify(sp.diff(nB, Tsym))
print("\n  (a) SINGLE dS MODE / ONE QUASINORMAL FREQUENCY.")
print("      dS static-patch quasinormal frequencies are purely imaginary (no oscillation), so a "
      "single mode gives a monotone relaxation -- consistent with psi decreasing. But:")
print("      (i)  the mode's thermal weight is n(T) = 1/(e^(w/T)-1) with dn/dT = %s > 0: INCREASING "
      "in T, the WRONG SIGN for psi (which must DECREASE so that f'(T_GH) > c1p, r > 1)." % dnB)
print("      (ii) 'one pole' has two inequivalent readings in this variable, and they differ by a "
      "factor %.2f in r: exponential in the conjugate variable -> r = %.4f; Lorentzian in the "
      "response variable -> r = 1 formally, and r = %.4f over any finite range."
      % (r_lim_p1/r_exp, r_exp, r_lim_p1))
pos = all(float(dnB.subs({om: 1.0, Tsym: tv})) > 0 for tv in (0.1, 0.5, 1.0, 3.0))
check("F2 (a) a single dS mode does NOT force an admissible single-scale psi: its thermal weight "
      "is strictly INCREASING in T (sympy dn/dT > 0 at four T, the wrong sign for r > 1), and the "
      "two natural 'one-pole' readings give r = %.4f and r = %.4f -- a factor %.2f spread. One pole "
      "does not determine r" % (r_exp, r_lim_p1, r_lim_p1/r_exp),
      pos and r_lim_p1/r_exp > 3.0)

# F3 (b) P(X) / the free function f: the map f -> psi is onto
print("\n  (b) P(X) SOUND-MODE RESPONSE WITH ONE ATTRACTOR SCALE.")
print("      the class is parametrised by the free function f; psi is a RELABELLING of f':")
print("          psi = (f'(T)/c1p - 1)/(r-1),    f'(T)/c1p = 1 + (r-1) psi(T - T_GH).")
print("      so the map f -> psi is a bijection onto the admissible class. Round-trip test: take "
      "the exact-law psi at r = 2Z, integrate to f, differentiate back, recover r and psi:")
Kz = exact_law_arrays(TWOZ, n=800001, lo=-12, hi=6)
fprime = 1.0 + Kz["lam"]*Kz["psi"]                       # f'/c1p
f_of_s = np.concatenate(([0.0], np.cumsum(0.5*(fprime[1:] + fprime[:-1])*np.diff(Kz["s"]))))
fp_back = np.gradient(f_of_s, Kz["s"])
r_back = float(np.interp(0.0, Kz["s"], fp_back))
i0 = int(np.argmin(abs(Kz["s"] - 1e-3)))
psi_back = (fp_back - 1.0)/Kz["lam"]
rel = abs(psi_back[i0]/Kz["psi"][i0] - 1)
print("      recovered f'(s -> 0)/c1p = %.6f  (input r = %.6f, relative %.2e);  psi round-trip at "
      "s = 1e-3: %.2e relative" % (r_back, TWOZ, abs(r_back/TWOZ - 1), rel))
check("F3 (b) P(X) forces nothing: f is a FREE function of one variable and psi is a bijective "
      "relabelling of f' (round-trip recovers r to %.1e and psi to %.1e). 'One attractor scale' "
      "fixes d; by F1 the ceiling depends only on the SHAPE, which P(X) leaves free -- and the "
      "shape exponent alone moves r over (%.3f, %.3f)" % (abs(r_back/TWOZ - 1), rel, r_exp, r_lim_p1),
      abs(r_back/TWOZ - 1) < 2e-3 and rel < 1e-3)

# F4 (c) GHY / boundary response: scale-free => step => r_eff = 1
print("\n  (c) GHY / BOUNDARY RESPONSE (lane P1).  A boundary/curvature response is SCALE-FREE: "
      "every polynomial curvature invariant of dS4 is algebraic x H^(2w), so f is a power law and "
      "psi carries no scale. A scale-invariant decreasing psi with psi(0)=1, psi(inf)=0 is a STEP, "
      "hence Psi == 0 a.e.:")
print("      %-14s %12s %12s %12s" % ("step width eps", "r_formal", "r_obs", "a_0_obs/2cH_L"))
step_rows = []
for eps in (1e-4, 1e-6, 1e-8, 1e-10):
    fn = lambda s, eps=eps: (np.where(s <= eps, 1.0, 0.0), np.minimum(s, eps))
    lam = 8.0                                  # any lam; the point is what the RAR sees
    st = rar_stats(fn, lam, n=1200001)
    step_rows.append(st["r_obs"])
    print("      %-14.0e %12.4f %12.6f %12.6f" % (eps, 1 + lam, st["r_obs"], st["a0o"]/2.0))
check("F4 (c) a scale-free (GHY/curvature-invariant) response gives a STEP psi, whose observed "
      "a_0 is 2 c H_Lambda EXACTLY -- r_obs -> 1.000000 as the step narrows (%.6f at eps = 1e-10) "
      "no matter what formal r = 1 + lam is imposed. Scale-free mechanisms land on Milgrom 1999's "
      "own coefficient and cannot produce r != 1" % step_rows[-1],
      abs(step_rows[-1] - 1.0) < 1e-4 and step_rows[-1] < step_rows[0] + 1e-9)

# F5 (d) complete monotonicity vs unimodality
print("\n  (d) COMPLETE MONOTONICITY (Bernstein) vs UNIMODALITY.")
print("      unimodality of psi is VACUOUS in this class: admissibility already requires psi "
      "monotone DECREASING, and a monotone function is unimodal with its mode at s = 0. So the "
      "'unimodality axiom' adds literally nothing -- it is implied by (A1)/(A2)'s own hypotheses.")
print("      complete monotonicity is WEAKER than one-relaxation: psi = Int e^(-st) drho(t) is a "
      "SUPERPOSITION, i.e. a continuum of scales. Ceilings: one exponential %.4f, CM cone %.1f "
      "(unbounded)." % (r_exp, cmv[1e8]))
mono_psi = np.all(np.diff(exact_law_arrays(9.0, n=400001)["psi"]) <= 1e-18)
check("F5 (d) 'unimodality' is VACUOUS (every admissible psi is monotone decreasing, hence "
      "unimodal -- verified on the exact-law psi at r = 9), and complete monotonicity is strictly "
      "WEAKER than a single relaxation process, admitting r from %.4f to unbounded. Neither "
      "supplies a ceiling; 'single-scale' is not even a property of a FUNCTION, only of a chosen "
      "one-parameter family, and by F1 the family's scale is exactly what r ignores" % r_exp,
      mono_psi and cmv[1e8] > 10*r_exp)

# =========================================================================================
banner("G  INDEPENDENT PREDICTION: the interpolation shapes, and whether SPARC can tell them apart")

yv = np.logspace(-2, 2, 200001)
nu99 = np.sqrt(1.0 + 1.0/yv)
nuMG = 1.0/(-np.expm1(-np.sqrt(yv)))                     # McGaugh 2008 ApJ 683:137 eq 11a
nusim = 0.5 + np.sqrt(0.25 + 1.0/yv)
print("  reference kernels on y in [1e-2, 1e2]:  max|dex| between nu = sqrt(1+1/y) (Milgrom 1999) "
      "and McGaugh 2008 eq 11a = %.4f dex" % np.max(np.abs(np.log10(nu99/nuMG))))
print("  %-38s %12s %12s %12s" % ("kernel", "dex vs M99", "dex vs McG", "vs 0.108"))
pred_rows = []
for nm, pf, dd_, pp, use_max in (("single-scale extremal p=2 (r->9)", pow_psi, 1e-8, 2.0, True),
                                 ("single-scale extremal p=1.405 (r->2Z)", pow_psi, 1e-8, 1.405, True),
                                 ("single exponential extremal (r=5.58)", exp_psi, 1e-6, None, True),
                                 ("single-scale best-RAR fit (E3, rms)", pow_psi,
                                  best["rms<=0.108"][2], best["rms<=0.108"][1], False)):
    fn = (lambda s, dd_=dd_, pp=pp: pow_psi(s, dd_, pp)) if pp else (lambda s, dd_=dd_: exp_psi(s, dd_))
    lam = lam_max_num(fn, n=1200001)[0] if use_max else best["rms<=0.108"][3]
    st = rar_stats(fn, lam, n=1200001)
    pred_rows.append((nm, st["d99"], st["dmg"]))
    print("  %-38s %12.4f %12.4f %12s" % (nm, st["d99"], st["dmg"],
                                          "EXCLUDED" if st["d99"] > SPARC_DEX else "allowed"))
print("  %-38s %12.4f %12.4f %12s" % ("exact-law kernel (any r)", 0.0,
                                      np.max(np.abs(np.log10(nu99/nuMG))), "allowed"))
check("G1 THE FALSIFIABLE CONTENT, stated as a prediction and already tested: any kernel that "
      "SATURATES (A2) -- which is the only way a single-scale psi reaches r >= 9 -- differs from "
      "nu = sqrt(1+1/y) by %.2f-%.2f dex and from McGaugh 2008 eq 11a by %.2f-%.2f dex across "
      "y in [1e-2,1e2]. SPARC's 0.108 dex scatter on the framework's own kernel is %.1fx-%.1fx "
      "smaller, so these shapes ARE distinguishable and ARE excluded. The exact-law kernel is at "
      "0 dex by construction at EVERY r, so the RAR distinguishes SHAPES but not COEFFICIENTS"
      % (min(p[1] for p in pred_rows[:3]), max(p[1] for p in pred_rows[:3]),
         min(p[2] for p in pred_rows[:3]), max(p[2] for p in pred_rows[:3]),
         min(p[1] for p in pred_rows[:3])/SPARC_DEX, max(p[1] for p in pred_rows[:3])/SPARC_DEX),
      min(p[1] for p in pred_rows[:3]) > 2*SPARC_DEX
      and np.max(np.abs(np.log10(nu99/nuMG))) < 0.3)
check("G2 and a SECOND, sharper prediction that does not depend on any dex budget: by D6 the exact "
      "law forces the inertia kernel to carry a break at a = a_0/2 (to %.3f%%) and a second at "
      "a ~ c H_Lambda, separated by 2 r^2 = %.0f at kappa = 1/2, with a 1/2-shelf %.2f decades wide "
      "-- %.1fx wider than ANY single-scale kernel can produce. So the SHAPE of the inertia response "
      "around g_obs ~ a_0/2 = %.4e (canonical) / %.4e (ALT) is where the master formula is "
      "falsifiable, and it is falsifiable there independently of which r is right"
      % (100*dev_half, 2*TWOZ**2, law_widths[TWOZ], law_widths[TWOZ]/w_pow, A0_CANON/2, A0_ALT/2),
      two_scale_ok and law_widths[TWOZ] > 2*w_pow)

# =========================================================================================
banner("H  REFINEMENT (4x) AND THE REMAINING NEGATIVE CONTROLS")

print("  4x grid / wider domain on the load-bearing ceilings:")
ref_rows = []
for nm, fn in (("p=2, d=1e-7", lambda s: pow_psi(s, 1e-7, 2.0)),
               ("p=1.405, d=1e-7", lambda s: pow_psi(s, 1e-7, 1.405)),
               ("single exponential d=1e-6", lambda s: exp_psi(s, 1e-6)),
               ("two-scale CM product", prod_psi)):
    a = lam_max_num(fn, lo=-15, hi=11, n=1200001)[0]
    b = lam_max_num(fn, lo=-17, hi=13, n=4800001)[0]
    ref_rows.append(abs(b/a - 1))
    print("      %-28s r_max: %12.6f -> %12.6f   shift %.2e" % (nm, 1 + a, 1 + b, abs(b - a)))
print("  4x on the exact-law (A2) margin at r = 2Z:")
K = exact_law_arrays(TWOZ, n=1200001); m1 = 1.0/J_of(K["s"], K["psi"], K["Psi"], 1.0).max()/K["lam"]
K = exact_law_arrays(TWOZ, n=4800001, lo=-18, hi=14); m2 = 1.0/J_of(K["s"], K["psi"], K["Psi"], 1.0).max()/K["lam"]
print("      lam_max/lam = %.8f -> %.8f   shift %.2e" % (m1, m2, abs(m2 - m1)))
check("H1 4x grid density and +-2 decades of domain move every load-bearing ceiling by <= %.1e "
      "relative and the exact-law (A2) margin by %.1e: the numbers above are resolved, not "
      "discretisation artefacts (the hazard that produced the committed 9.016763 for the exact 9)"
      % (max(ref_rows), abs(m2 - m1)),
      max(ref_rows) < 1e-4 and abs(m2 - m1) < 1e-4 and m2 > 1.0)

# negative control 3: corrupt the exact-law psi normalisation
K = exact_law_arrays(9.0, n=400001)
psi0_true = float(np.interp(0.0, K["s"], K["psi"]))
psi0_bug = float(np.interp(0.0, K["s"], K["psi"]*1.05))
print("\n  NEGATIVE CONTROL 3: psi_law(0) must be 1 by construction. true %.10f, "
      "5%%-corrupted %.10f" % (psi0_true, psi0_bug))
check("H2 psi_law(0) = 1 to %.1e (the normalisation that makes r = 1 + lam meaningful), and the "
      "5%%-corrupted kernel gives %.4f, so this check can fail" % (abs(psi0_true - 1), psi0_bug),
      abs(psi0_true - 1.0) < 1e-6 and abs(psi0_bug - 1.0) > 1e-2)

# negative control 4: the menu claim itself.  If the single-scale class really capped r at 9,
# then r_ceiling_pow(p) <= 9 for ALL p > 1.  Assert the falsifying witness explicitly.
witness = r_ceiling_pow(1.405)
check("H3 EXPLICIT FALSIFYING WITNESS for the menu ceiling: p = 1.405 is a single-scale, unimodal, "
      "completely monotone, C^infinity kernel with r_max = %.6f > 9. If the axiom capped r at 9 "
      "this check would fail; it does not" % witness, witness > 9.0)

# =========================================================================================
banner("I  THE FORK, BOTH HALVES, AND WHAT IS RECORDED AGAINST INTEREST")

print(f"""  THE FORK AS THE BRIEF POSED IT.
  HALF 1 -- 'a tree-level mechanism DOES force single-scale psi, so r <= 9 exactly, DERIVING
  a_0 = 2 c H_Lambda/9 = 1.2044e-10 with zero free parameters and EXCLUDING kappa = 1/2 (2Z is
  28.6% above 9), the ALT footing (6.6% above) and 4 pi (39.6% above)':  THIS HALF IS NOT REACHED,
  and it fails twice over.
    (1) No mechanism examined forces it. By the SCALE-BLINDNESS THEOREM (F1) r is a pure SHAPE
        functional, invariant under the kernel's scale, while every candidate -- one quasinormal
        frequency (F2), one P(X) attractor (F3), a GHY/curvature response (F4), Bernstein
        positivity (F5) -- supplies a SCALE and leaves the shape free. 'Unimodality' is vacuous
        (admissible psi is already monotone). The GHY branch is worse than free: being scale-free
        it forces r = 1 exactly.
    (2) Even if some mechanism DID force single-scale, r <= 9 IS FALSE. The single-scale family
        (1+s/d)^-p reaches r_max = 17.6225 as p -> 1+, and hits 9, 9.0323, 11.5776 and 12.5664 at
        p = 2, 1.98710, 1.40509, 1.29215. The committed '9' was a 7-shape MENU artefact that
        skipped the band 1 < p < 2.
  HALF 2 -- 'no mechanism forces it, the axiom is unmotivated, sup r stays +infinity and the 0.4%
  proximity is a coincidence':  THIS IS THE ANSWER. And the coincidence is now priced: it is a
  0.65% shift of a free shape exponent, inside a family that covers a_0 from 6.15e-11 to 1.94e-10
  -- a factor 3.2 containing every candidate on the table, 9.3614e-11 and c H_Lambda/2pi included.
  Worse for the lead, the r = 9 kernel's OBSERVED a_0 is 2 c H_Lambda (r_obs = 1.0000, E1), so the
  number the coincidence is about is not even what that kernel predicts.

  AGAINST INTEREST -- recorded in full because it is where the argument does not favour Carl.
   * p = 2 is an INTEGER exponent (a second-order pole), while kappa = 1/2 needs the fractional
     p = 1.40509 and 4 pi needs p = 1.29215. On any naturalness-of-exponent ordering, r = 9 is the
     more natural member of the family than the framework's own coefficient. This mirrors the
     standing against-interest item that the two natural constants in the a_0 box are both
     Z = 2 pi (Milgrom), so THEORY keeps leaning away from kappa = 1/2 while DATA leans toward it.
   * the exact-law kernel sits within 1-12% of the (A2) monotonicity boundary at every r tested
     (D4): the framework's own law is NEARLY EXTREMAL in this class. That is a fine-tuning-flavoured
     fact, not a win, and it is why the extremal-kernel pathologies of section E sit so close by.
   * under the STRICT shape budgets -- max|dex| <= 0.108 or rms <= 0.050 -- the single-scale class
     reaches only r_obs ~ {r_max108:.2f} / {r_rms050:.2f}, i.e. a_0_obs >~ {2*CHL/max(r_max108, r_rms050):.3e}. If those were
     the right statistics they would bear against 2Z = 11.578 and 4 pi = 12.566 while comfortably
     ADMITTING r = 9, McGaugh's 9.0323 and the ALT 9.5919 -- the one place in this lane where a
     defensible statistic leans away from kappa = 1/2. NO exclusion is drawn from it, for three
     reasons: the budget is arbitrary; the like-for-like rms comparison with SPARC's rms SCATTER
     gives {r_rms108:.2f} and admits everything; and a scan MAXIMUM is a LOWER bound on what the class can
     achieve, so the apparent cap is not a ceiling. Grading a systematic shape by a random scatter
     is the exact error this corpus has logged twice.
   * the only firm bound this class puts on the coefficient is a_0 < 2 c H_Lambda = 1.0839e-9 (D2),
     which every candidate satisfies. The class discriminates nothing, in either direction.

  WHAT IS NOT CLOSED.  This lane closes the SINGLE-SCALE AXIOM, not the master formula. Open:
  (i) an axiom that constrains the SHAPE (not the scale) of psi -- e.g. a forced spectral exponent
      p from a genuine tree-level two-point function -- would be a real derivation route, and
      nothing here excludes one; by C5 it would have to force p to ~0.65% to select between 9 and
      McGaugh's 9.0323, and to p = 1.40509 to select kappa = 1/2;
  (ii) the D6 structure -- inner break at a = a_0/2 = k, outer at c H_Lambda, ratio 2 r^2 -- is
      real STRUCTURE the framework predicts and is worth confronting with the observed RAR;
  (iii) lane P1's GHY response is treated here only through its scale-free character; if P1 finds a
      boundary term that carries an intrinsic scale, F4's r = 1 collapse does not apply to it.
  kappa = 1/2 remains FITTED, NOT DERIVED -- and is NOT excluded.""")

# =========================================================================================
n_ok = sum(checks)
print("\n" + "=" * 100)
print("%d/%d checks held." % (n_ok, len(checks)))
print("VERDICT: NO_GO. No tree-level mechanism forces a single-scale psi (r is scale-blind, F1), "
      "and 'single-scale => r <= 9' is FALSE anyway (C5). a_0 = 2 c H_Lambda/9 is NOT derived; "
      "kappa = 1/2 is NOT excluded; sup r stays +infinity. kappa = 1/2 stays FITTED.")
print("=" * 100)
if n_ok != len(checks):
    sys.exit(1)
sys.exit(0)
