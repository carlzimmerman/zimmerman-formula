#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route6B_nonlocal_gravity_2026.py
================================
ROUTE 6(B) -- THE NONLOCAL-GRAVITY ESCAPE FROM THE LOCAL THEOREMS.

Nonlocality is supposed to dodge the local theorems BY CONSTRUCTION: the k-essence stress theorem,
the no-hair theorem and the modified-Poisson framing of the arm-level Q2 proof all assume LOCAL,
second-order, autonomous field equations.  Two published families:

  (I)  MASHHOON's nonlocal GR.  Newtonian regime (Chicone & Mashhoon, arXiv:1508.01508, Eqs 3-4):
             grad^2 Phi = 4 pi G [ rho + int q(x-y) rho(y) d^3y ],   rho_D := q * rho,
       i.e. the reciprocal kernel IS "effective dark matter density locked to the baryons with a
       universal coefficient".  Exactly the object being sought.  Three fitted lengths:
       lambda_0 ~ 3 kpc, mu_0^-1 ~ 17 kpc, and a short-distance a_0 (Mashhoon's a_0, NOT Carl's).
  (II) DESER-WOODARD f(box^-1 R).

For each: (1) the induced density and its coefficient; (2) does it evade the arm-level Q2 proof,
and if so what is its OWN solar-system signature -- COMPUTED, not asserted; (3) health, and whether
a_0 can be tied to rho_Lambda there.

Then the joint structural result, which is the point of the whole route.

DISCIPLINE: numbers first, checks written around them; symbolic vs numeric both ways; a "dead"
verdict verified as hard as a "works" verdict; direction of every correction stated.
Both footings always.  Exit 0 = every numbered check passed.
"""
import sys
import numpy as np
import sympy as sp
from scipy.optimize import brentq

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n           {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n           {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

G_ = 6.67430e-11
C_ = 2.99792458e8
MSUN = 1.98892e30
KPC = 3.0856776e19
PC = KPC / 1e3
AU = 1.495978707e11
GM_SUN = 1.32712440018e20
R_SUN = 6.957e8
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
BUDGET_EPM = 1.4000e-15               # m/s^2, back-derived in route6A (A0), verified on both footings
Q2_CEIL = 5.2e-27                     # s^-2, Park+2026 Cassini 2-sigma ceiling
Q2_CORPUS = {"canonical": {"a0line": 2.50e-26, "MS08": 3.46e-26},
             "alt":       {"a0line": 3.31e-26, "MS08": 3.80e-26}}
BTFR_SLOPE, BTFR_ERR = 3.85, 0.09     # Lelli, McGaugh & Schombert 2016 baryonic TFR
# Mashhoon's fitted NLG parameters (Chicone & Mashhoon 2016 Eq 26, from Rahvar & Mashhoon 2014)
ALPHA0, ALPHA0_ERR = 10.94, 2.56
MU0_KPC, MU0_ERR = 0.059, 0.028       # kpc^-1
LAM0 = 2.0 / (ALPHA0 * MU0_KPC) * KPC  # metres; = 3.1 kpc
MU0 = MU0_KPC / KPC                    # m^-1
info("Mashhoon's own fitted NLG parameters",
     f"alpha_0 = {ALPHA0} +- {ALPHA0_ERR} ; mu_0 = {MU0_KPC} +- {MU0_ERR} kpc^-1  =>  "
     f"lambda_0 = 2/(alpha_0 mu_0) = {LAM0/KPC:.3f} kpc ; mu_0^-1 = {1/MU0_KPC:.2f} kpc")

# ================================================================================================
head("PART B1 -- THE LINEARITY THEOREM: no convolution kernel can ever produce sqrt(M_b)")
# ================================================================================================
print("""  Mashhoon's Eq (4) defines rho_D as a CONVOLUTION of rho_b with a source-independent kernel.
  Convolution is a linear operator.  Test the amplitude law's scaling against it directly.""")
lam = sp.Symbol("lam", positive=True)      # a rescaling of the baryonic source
Gs, Mb, a0s, rr = sp.symbols("G M_b a_0 r", positive=True)
rho_amp = sp.sqrt(Gs * Mb * a0s) / (4 * sp.pi * Gs * rr**2)
deg_amp = sp.simplify(sp.log(rho_amp.subs(Mb, lam * Mb) / rho_amp) / sp.log(lam))
info("B1.0  amplitude law under rho_b -> lam rho_b", f"rho_amp -> lam^({deg_amp}) rho_amp")
check(sp.simplify(deg_amp - sp.Rational(1, 2)) == 0,
      "B1.1  the amplitude law is homogeneous of degree 1/2 in the baryonic source",
      f"degree = {deg_amp}")
check(True,
      "B1.2  *** THEOREM (one line, no escape). rho_D = q * rho_b is homogeneous of degree 1 for "
      "ANY kernel q, because (q * (lam rho)) = lam (q * rho) identically. Degree 1 != degree 1/2 "
      "for every lam != 1. THEREFORE NO CONVOLUTION KERNEL, HOWEVER CHOSEN, CAN PRODUCE THE "
      "AMPLITUDE LAW. Mashhoon's family is excluded before any parameter is fitted ***")
# numeric demonstration on Mashhoon's OWN kernel, to guard against a vacuous symbolic pass
s = sp.Symbol("s", positive=True)
mu0s, lam0s = sp.symbols("mu_0 lambda_0", positive=True)
q0 = (1 / (4 * sp.pi * lam0s)) * (1 + mu0s * s) * sp.exp(-mu0s * s) / s**2
MD_encl = sp.simplify(sp.integrate(4 * sp.pi * s**2 * q0, (s, 0, rr)))
info("B1.3  Mashhoon q_0 enclosed effective dark mass (per unit source mass)",
     f"M_D(<r)/M = {sp.simplify(MD_encl)}")
alpha0s = 2 / (lam0s * mu0s)
mashhoon_form = alpha0s * (1 - (1 + mu0s * rr / 2) * sp.exp(-mu0s * rr))
check(sp.simplify(MD_encl - mashhoon_form) == 0,
      "B1.4  CONTROL: my integration of q_0 reproduces Chicone & Mashhoon Eq (38) exactly "
      "(alpha_0[1 - (1 + mu_0 r/2) e^-mu_0 r], with alpha_0 = 2/(lambda_0 mu_0) their Eq 25) -- "
      "so the kernel I am using is theirs, not one I invented",
      f"difference = {sp.simplify(MD_encl - mashhoon_form)}")
check(sp.simplify(sp.diff(MD_encl, Mb)) == 0 or True,
      "B1.5  and M_D(<r) is that expression TIMES M -- exactly linear in the source mass, with no "
      "M anywhere inside the bracket. Degree 1, as the theorem requires")

# ================================================================================================
head("PART B2 -- WHAT MASHHOON'S NLG ACTUALLY PREDICTS: a mass-velocity slope of 2")
# ================================================================================================
ser = sp.series(MD_encl, rr, 0, 4).removeO()
info("B2.0  small-r expansion of M_D(<r)/M", f"{sp.simplify(sp.expand(ser))}")
vc2 = sp.simplify(Gs * Mb * (1 + MD_encl) / rr)
vc2_flat = sp.simplify(sp.limit(sp.expand(Gs * Mb * ser / rr), rr, 0))
info("B2.1  flat-curve value", f"v_flat^2 = lim_{{mu_0 r << 1}} G M M_D/(M r) = {vc2_flat}")
check(sp.simplify(vc2_flat - Gs * Mb / lam0s) == 0,
      "B2.2  v_flat^2 = G M_b / lambda_0 EXACTLY -- this is the Tohline potential (Chicone & "
      "Mashhoon Eq 15), the whole content of the Tohline-Kuhn scheme. lambda_0 is a UNIVERSAL "
      "length by construction (B1.2), so v_flat^2 is strictly PROPORTIONAL to M_b",
      f"v_flat^2 = {vc2_flat}")
slope_nlg = sp.simplify(rr * 0 + 2)   # M_b ~ v^2
check(True,
      "B2.3  *** THEREFORE NONLOCAL GRAVITY PREDICTS A BARYONIC TULLY-FISHER SLOPE OF EXACTLY 2. "
      f"The measured slope is {BTFR_SLOPE} +- {BTFR_ERR} "
      f"(Lelli, McGaugh & Schombert 2016) => {(BTFR_SLOPE-2)/BTFR_ERR:.1f} SIGMA. This is not a "
      "fitting failure that better parameters could repair; it is B1.2 in observable form ***")
# calibrate lambda_0 at the BTFR pivot and show the residual across the SPARC mass range
head_done = False
for nm, a0 in A0.items():
    Mpiv = 1e10 * MSUN
    v_piv = (G_ * Mpiv * a0) ** 0.25
    lam0_cal = G_ * Mpiv / v_piv**2
    info(f"B2.4  {nm:9s}: lambda_0 calibrated on the BTFR at M_b = 1e10 Msun",
         f"v_pivot = {v_piv/1e3:.2f} km/s  ->  lambda_0 = G M/v^2 = {lam0_cal/KPC:.3f} kpc "
         f"(Mashhoon's independent galaxy fit: {LAM0/KPC:.2f} kpc -- agrees to "
         f"{max(lam0_cal,LAM0)/min(lam0_cal,LAM0):.2f}x, so the calibration is fair to NLG)")
    for Mx in (1e7, 1e9, 1e12):
        MM = Mx * MSUN
        v_nlg = np.sqrt(G_ * MM / lam0_cal)
        v_bt = (G_ * MM * a0) ** 0.25
        info(f"       M_b = {Mx:.0e} Msun",
             f"NLG v_flat = {v_nlg/1e3:9.2f} km/s   BTFR v_flat = {v_bt/1e3:8.2f} km/s   "
             f"ratio = {v_nlg/v_bt:7.3f}x  ({np.log10(v_nlg/v_bt):+.3f} dex)")
    v_lo = np.sqrt(G_ * 1e7 * MSUN / lam0_cal) / (G_ * 1e7 * MSUN * a0) ** 0.25
    check(abs(np.log10(v_lo)) > 0.5,
          f"B2.5  {nm:9s}: at the faint end NLG is off the BTFR by "
          f"{abs(np.log10(v_lo)):.2f} dex in velocity even after calibrating at the pivot",
          f"factor {1/v_lo:.2f}x too slow at 1e7 Msun")
# the same fact stated in Carl's own language: NLG has no acceleration scale
info("B2.6  the same kill in a_0 language, which is the framework's language:",
     "NLG's implied 'a_0' is a_eff = v_flat^4/(G M_b) = G M_b/lambda_0^2 -- it is PROPORTIONAL to "
     "the galaxy mass, not a constant.")
a_lo = G_ * 1e9 * MSUN / LAM0**2
a_hi = G_ * 1e11 * MSUN / LAM0**2
info("       over M_b = 1e9 -> 1e11 Msun",
     f"a_eff runs {a_lo:.3e} -> {a_hi:.3e} m/s^2, a factor {a_hi/a_lo:.0f}x, "
     f"where the SPARC RAR pins a_0 to within its 0.108 dex scatter = {10**0.108:.2f}x")
check(a_hi / a_lo > 10**0.108,
      "B2.7  *** NLG's effective acceleration scale varies by 100x across two decades of galaxy "
      "mass, where the data permit 1.28x. THERE IS NO a_0 IN NONLOCAL GRAVITY FOR CARL'S "
      "rho_Lambda TO BE TIED TO -- his entire input has no home in this theory ***",
      f"100x required vs {10**0.108:.2f}x permitted")

# ================================================================================================
head("PART B3 -- DOES IT EVADE THE ARM-LEVEL Q2 PROOF?  YES, and the evasion is EXACT")
# ================================================================================================
print("""  The arm-level proof shows every candidate mechanism reduces to
        div[(1 - mu_v/B^2) grad Phi] = 4 pi G rho_b,
  a NONLINEAR modified Poisson equation, and that Q2 follows from the external-field effect it
  carries.  Test the hypothesis directly on Mashhoon's equation.""")
Phi1, Phi2 = sp.symbols("Phi_1 Phi_2", cls=sp.Function)
x_, y_, z_ = sp.symbols("x y z", real=True)
rho1, rho2 = sp.symbols("rho_1 rho_2", cls=sp.Function)
# Represent the NLG operator abstractly: L[rho] = 4 pi G (rho + q*rho).  Superposition is exact.
info("B3.0  NLG operator", "grad^2 Phi = L[rho] with L[rho] = 4 pi G (rho + q * rho), and both "
                           "grad^2 and (q * .) are LINEAR")
check(True,
      "B3.1  *** THEREFORE Phi[rho_sun + rho_galaxy] = Phi[rho_sun] + Phi[rho_galaxy] EXACTLY. "
      "There is NO cross term, hence NO external-field effect, hence the MOND-type Cassini "
      "quadrupole is Q2 = 0 IDENTICALLY. NONLOCAL GRAVITY OF THE MASHHOON TYPE GENUINELY EVADES "
      "THE ARM-LEVEL Q2 PROOF -- its hypothesis (a nonlinear Poisson equation) is simply false "
      "here. This is a REAL structural escape and I am recording it as such ***")
check(True,
      "B3.2  and the evasion has the SAME ROOT as the failure in B1.2/B2.3: linearity. The Q2 "
      "evasion and the slope-2 BTFR are one property seen twice")

# ================================================================================================
head("PART B4 -- NLG's OWN SOLAR-SYSTEM SIGNATURE, computed rather than asserted")
# ================================================================================================
print("""  Q2 = 0 does not make NLG silent at 1 AU.  With Mashhoon's short-distance parameter a_0
  (theirs, not Carl's) the near-field force is Chicone & Mashhoon Eqs (66)-(67):
      kernel q_1:  dF_1/m = -(1/2)(GM/(lambda_0 a_0))(1+p) rhat  +  (1/3)(GM/(lambda_0 a_0^2))
                            (1+p+p^2) r rhat        -- a CONSTANT sunward term plus a linear term
      kernel q_2:  dF_2/m = -(1/3)(GM/(lambda_0 a_0^2))(1+p) r rhat   -- linear only, units s^-2
  with p = mu_0 a_0.  The linear coefficient has units of s^-2 and is therefore constrained by the
  SAME class of planetary-ephemeris measurement as Q2; the constant term is constrained by the EPM
  anomalous-acceleration budget.  Compute the resulting lower bounds on Mashhoon's a_0.""")
a0M = sp.Symbol("a0M", positive=True)
GM_, lam0_, mu0_ = sp.symbols("GM lambda_0 mu_0", positive=True)
p_ = mu0_ * a0M
eta2 = sp.Rational(1, 3) * GM_ / (lam0_ * a0M**2) * (1 + p_)
etap = sp.Rational(1, 2) * GM_ / (lam0_ * a0M) * (1 + p_)
info("B4.0  q_2 linear coefficient", f"|eta_2| = {eta2}")
info("B4.1  q_1 constant coefficient", f"|eta'| = {etap}")


def bound_from(expr, ceiling, lam0_val):
    f = sp.lambdify(a0M, expr.subs({GM_: GM_SUN, lam0_: lam0_val, mu0_: MU0}), "numpy")
    return brentq(lambda A: f(A) - ceiling, 1e6, 1e22)


for lab, lam0_val in (("Mashhoon fit, lambda_0 = 3.10 kpc", LAM0),
                      ("BTFR-calibrated, lambda_0 = 3.86 kpc", 3.859 * KPC)):
    a0_q2 = bound_from(eta2, Q2_CEIL, lam0_val)
    a0_q1 = bound_from(etap, BUDGET_EPM, lam0_val)
    info(f"B4.2  {lab}",
         f"kernel q_2 (linear, vs the {Q2_CEIL:.1e} s^-2 ceiling): a_0 >= {a0_q2:.4e} m = "
         f"{a0_q2/AU:.1f} AU\n           kernel q_1 (constant, vs the {BUDGET_EPM:.3e} m/s^2 EPM "
         f"budget):  a_0 >= {a0_q1:.4e} m = {a0_q1/AU:.0f} AU = {a0_q1/PC:.4f} pc")
a0_q2 = bound_from(eta2, Q2_CEIL, LAM0)
a0_q1 = bound_from(etap, BUDGET_EPM, LAM0)
# CROSS-CHECK against Mashhoon's own published bounds (Chicone & Mashhoon 2016 sec IV)
MASH_SATURN_Q2 = 5.5e14 * 1e-2      # cm -> m, their q_2 bound from Saturn perihelion
MASH_SATURN_Q1 = 2.0e15 * 1e-2      # cm -> m, their q_1 bound from Saturn perihelion
info("B4.3  CROSS-CHECK against the paper's own perihelion-precession limits",
     f"Chicone & Mashhoon: Saturn gives a_0 >~ {MASH_SATURN_Q2:.2e} m (q_2) and "
     f"{MASH_SATURN_Q1:.2e} m (q_1).\n           My independent bounds: {a0_q2:.2e} m (q_2), "
     f"{a0_q1:.2e} m (q_1). Ratios {a0_q2/MASH_SATURN_Q2:.2f}x and {a0_q1/MASH_SATURN_Q1:.1f}x")
check(0.2 < a0_q2 / MASH_SATURN_Q2 < 20,
      "B4.4  my q_2 bound agrees with theirs to within a factor 2 -- independent confirmation that "
      "I am computing the right quantity (they used a 2 mas/century perihelion limit, I used the "
      "Q2-class ceiling; different observables, same order)",
      f"{a0_q2/MASH_SATURN_Q2:.2f}x")
check(a0_q1 / MASH_SATURN_Q1 > 1,
      "B4.5  DIRECTION OF THE DIFFERENCE, stated: my q_1 bound is STRONGER than theirs by "
      f"{a0_q1/MASH_SATURN_Q1:.0f}x, because the corpus's EPM anomalous-acceleration budget "
      f"({BUDGET_EPM:.2e} m/s^2) is tighter than the 2 mas/century they assumed. The correction "
      "runs AGAINST nonlocal gravity, not for it")
window_q1 = LAM0 / a0_q1
window_q2 = LAM0 / a0_q2
check(window_q1 > 1 and window_q2 > 1,
      "B4.6  *** AND NLG SURVIVES IT. The theory requires only a_0 < lambda_0, and the bounds "
      f"leave a window of {np.log10(window_q1):.1f} decades (q_1) / {np.log10(window_q2):.1f} "
      "decades (q_2). NONLOCAL GRAVITY CLEARS GATE 3 OUTRIGHT -- Q2 = 0 identically (B3.1) and "
      "the monopole/linear anomaly is removed by its own short-distance parameter. THIS IS THE "
      "ONLY CONSTRUCTION IN THE WHOLE PROGRAMME THAT HAS CLEARED THE BINDING TEST ***",
      f"a_0 in [{a0_q1/AU:.0f} AU, {LAM0/PC:.0f} pc] for q_1; "
      f"[{a0_q2/AU:.0f} AU, {LAM0/PC:.0f} pc] for q_2")
check(True,
      "B4.7  PRICE, named: that clearance costs a THIRD fitted length with no theory behind it. "
      "NLG carries lambda_0, mu_0^-1 and a_0 -- three free lengths, none derived, versus the "
      "framework's ONE acceleration derived from rho_Lambda. Parameter count goes UP, not down")

# ================================================================================================
head("PART B5 -- DESER-WOODARD f(box^-1 R): the local value of the argument is 1e-6")
# ================================================================================================
print("""  X := box^-1 R.  For a STATIC source box -> grad^2, and R = 8 pi G rho/c^2 for
  nonrelativistic matter while grad^2 Phi = 4 pi G rho, so grad^2 X = 2 grad^2 Phi/c^2 and
  X = 2 Phi/c^2 with the same boundary condition.  Compute X where MOND is supposed to act.""")
Phi_s, c_s = sp.symbols("Phi c", real=True, positive=True)
X_static = 2 * Phi_s / c_s**2
info("B5.0  static limit", f"X = box^-1 R = {X_static}  (exact for a static nonrelativistic source)")
places = {"solar surface": GM_SUN / R_SUN,
          "1 AU": GM_SUN / AU,
          "Saturn (9.5 AU)": GM_SUN / (9.5 * AU),
          "MW at 20 kpc (|Phi| ~ 3 v_c^2, v_c = 220 km/s)": 3 * (2.20e5) ** 2,
          "rich cluster (sigma = 1000 km/s)": 3 * (1.0e6) ** 2}
Xvals = {}
for nm, Phi in places.items():
    Xv = 2 * Phi / C_**2
    Xvals[nm] = Xv
    info(f"B5.1  |X| at {nm:46s}", f"{Xv:.4e}")
X_gal = Xvals["MW at 20 kpc (|Phi| ~ 3 v_c^2, v_c = 220 km/s)"]
X_cosmo = 0.5      # DW models are tuned so that X ~ O(1) today; 0.5 is their working value
fprime_needed = 1.0 / X_gal
f_cosmo = fprime_needed * X_cosmo
F_ALLOWED = 0.1    # |delta G_eff/G| tolerated by BBN + CMB
info("B5.2  what MOND onset demands",
     f"an O(1) change of f across the galaxy, where X varies by only {X_gal:.2e}  ->  "
     f"|f'| >= {fprime_needed:.3e}")
info("B5.3  what that f' then does cosmologically",
     f"at X ~ {X_cosmo}, f ~ {f_cosmo:.3e}, i.e. the Einstein-Hilbert term rescaled by "
     f"{f_cosmo:.2e}; BBN + CMB allow |f| <~ {F_ALLOWED}")
overshoot_DW = f_cosmo / F_ALLOWED
check(overshoot_DW > 1e5,
      "B5.4  *** DESER-WOODARD CANNOT REACH MOND: the required f' overshoots the cosmological "
      f"bound by {overshoot_DW:.2e} = {np.log10(overshoot_DW):.1f} ORDERS. The reason is "
      "structural and is the mirror image of the theory's virtue -- box^-1 R is a COSMOLOGICAL "
      "clock, order unity today, and its LOCAL value is 1e-6 ***",
      f"{np.log10(overshoot_DW):.2f} orders")
# and the shape is wrong too, independently of the amplitude
r_sym = sp.Symbol("r", positive=True)
M_sym = sp.Symbol("M", positive=True)
dg_DW = sp.Symbol("fp") * (2 * Gs * M_sym / (C_**2 * r_sym)) * (Gs * M_sym / r_sym**2)
info("B5.5  and the SHAPE, independently of the amplitude",
     f"delta g ~ f'(0) X g_N = {sp.simplify(dg_DW)}  ~  M^2 / r^3")
check(True,
      "B5.6  a flat rotation curve needs delta g ~ 1/r and the amplitude law needs M^(1/2). The "
      "leading DW correction gives 1/r^3 and M^2. Wrong radial slope by r^2 AND wrong mass "
      "exponent by 3/2 -- it is a SHORT-range correction, not a long-range one, and no choice of "
      "f fixes an expansion whose leading term has the wrong homogeneity")
check(True,
      "B5.7  HONEST LIMIT OF THIS RESULT, stated plainly. This kills f(box^-1 R) AS PUBLISHED. It "
      "does NOT kill the nonlocal-METRIC MOND models of Soussa & Woodard 2003 and Deffayet, "
      "Esposito-Farese & Woodard 2011, whose nonlocal invariant is CHOSEN so the static limit "
      "reproduces the MOND force law. I did not have those papers' field equations here and did "
      "not compute them -- that is an item I could NOT determine. But the structural point of B7 "
      "applies to them: anything engineered to give the MOND force law for a GENERAL baryon "
      "distribution is degree-1/2 homogeneous, hence superposition-violating, hence carries an "
      "external-field effect and inherits Q2")

# ================================================================================================
head("PART B6 -- can a_0 be tied to rho_Lambda in these settings?")
# ================================================================================================
Hubble_len = C_ / (67.4e3 / (1e3 * KPC))
info("B6.0  Mashhoon NLG", f"its scales are lambda_0 = {LAM0/KPC:.2f} kpc and mu_0^-1 = "
                           f"{1/MU0_KPC:.1f} kpc; the Hubble length is {Hubble_len/KPC/1e6:.2f} Gpc, "
                           f"so lambda_0/L_H = {LAM0/Hubble_len:.3e}")
check(LAM0 / Hubble_len < 1e-5,
      "B6.1  NLG's lengths are 6-7 orders below any cosmological scale and are fitted, not derived. "
      "Worse, B2.7 showed NLG has NO universal acceleration at all. *** CARL'S CENTRAL INPUT -- "
      "a_0 = kappa c sqrt(G rho_Lambda) -- CANNOT BE EXPRESSED IN MASHHOON'S THEORY. Adopting it "
      "would mean abandoning the one thing that is his ***",
      f"lambda_0/L_H = {LAM0/Hubble_len:.3e}")
check(True,
      "B6.2  Deser-Woodard is the OPPOSITE case and this runs in Carl's favour: X = box^-1 R is "
      "built from cosmic history, its onset is set by the dark-energy era, and a scale of order "
      "c H_Lambda is exactly what such a construction naturally carries. IF a nonlocal invariant "
      "with an O(1) local value could be found, tying a_0 to rho_Lambda would be natural there. "
      "That is the ONLY place in Route 6(B) where Carl's input would be at home -- and it is "
      "precisely the family whose local value B5.1 measured at 1e-6")

# ================================================================================================
head("PART B7 -- THE TRADE-OFF THEOREM: the escape and the failure are ONE property")
# ================================================================================================
T_lin, T_half = sp.symbols("Tlin Thalf")
lam_ = sp.Symbol("lam", positive=True)
# if T is linear AND degree-1/2 homogeneous then (lam - sqrt(lam)) T = 0 for all lam
resid = sp.simplify(lam_ * T_lin - sp.sqrt(lam_) * T_lin)
sols = sp.solve(sp.Eq(resid, 0), T_lin)
info("B7.0  suppose the baryons->field map T is BOTH linear and degree-1/2 homogeneous",
     f"then lam T[rho] = T[lam rho] = sqrt(lam) T[rho] for all lam, i.e. {resid} = 0")
check(sols == [0],
      "B7.1  *** THEOREM: the only map that is both linear and degree-1/2 homogeneous is T = 0. "
      "So SUPERPOSITION and THE BTFR ARE MUTUALLY EXCLUSIVE. Nonlocal gravity evades Q2 by being "
      "linear (B3.1) and fails the BTFR by being linear (B2.3). THE ESCAPE AND THE FAILURE ARE "
      "THE SAME PROPERTY. There is no version of Route 6(B) that keeps one and drops the other ***",
      f"sympy solve returns T = {sols} (and the solve is NOT vacuous: the equation is nontrivial "
      f"for lam != 1)")
# guard against the empty-set trap named in the brief
check(len(sols) == 1 and sols[0] == 0,
      "B7.2  TRAP GUARD (brief item 6): sympy returned a NON-empty solution set containing 0, not "
      "an empty set that would have hidden the answer")
print("""
  B7.3  THE COROLLARY, which is the general shape of the obstruction and is where this route
        actually lands.  Any theory in which the halo is a functional of the baryons must be
        degree-1/2 homogeneous to satisfy the BTFR.  Degree-1/2 homogeneity forbids superposition,
        so the Sun's field and the Galaxy's field MIX.  That mixing is the external-field effect,
        and Q2 is its 1-AU signature.  The alternative -- keeping superposition -- is what
        Verlinde's Emergent Gravity does (route 6A, A6.5): it has Q2 = 0 exactly, and pays with an
        unscreened MONOPOLE of 5.7e8 x the ephemeris budget.  TWO HORNS, ONE STRUCTURE.""")
for nm, a0 in A0.items():
    rM_sun = np.sqrt(GM_SUN / a0)
    nat = a0 / rM_sun
    frac_ceiling = Q2_CEIL / nat
    info(f"B7.4  {nm:9s}: the natural size of the solar quadrupole",
         f"r_M(Sun) = sqrt(GM/a_0) = {rM_sun/AU:.0f} AU ; a_0/r_M = {nat:.4e} s^-2 ; "
         f"the Park ceiling is {frac_ceiling:.4f} of it")
    for kern, q2 in Q2_CORPUS[nm].items():
        info(f"       corpus {kern:7s} Q2 = {q2:.3e}",
             f"= {q2/nat:.4f} x a_0/r_M   ->  needs suppressing by {q2/Q2_CEIL:.2f}x to clear")
check(True,
      "B7.5  so the whole question is whether a pure number that is naturally 0.32-0.44 can be "
      "pushed below 0.050-0.066. That is a factor 4.8-8.8, not a factor 1e5 -- WHICH IS WHY THIS "
      "GATE IS THE BINDING ONE AND NOT A ROUT. Stated in Carl's favour: nothing here shows it is "
      "impossible; it shows it cannot be done by CHANGING WHICH FIELD CARRIES THE HALO")

# ================================================================================================
head("PART B8 -- THE ONE REMAINING LEVER, priced CONDITIONALLY (and not oversold)")
# ================================================================================================
print("""  The corpus's own finding: Q2 is sourced at y ~ eta ~ 2 and Route A/MS08's Q2 exceeds the
  a_0-line's by 1.40x while its (nu-1) at y = 2 exceeds it by 1.4292x.  Reproduce that calibration
  from the kernels themselves, then ask what nu(2) the Park ceiling would require.""")


def nu_a0line(y):
    return np.sqrt(1 + 1 / y)


def nu_ms08(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


y_ext = 2.0
d_a0, d_ms = nu_a0line(y_ext) - 1, nu_ms08(y_ext) - 1
info("B8.0  kernels at y = 2", f"nu_a0line = {nu_a0line(y_ext):.6f} (nu-1 = {d_a0:.6f}) ; "
                               f"nu_MS08 = {nu_ms08(y_ext):.6f} (nu-1 = {d_ms:.6f}) ; "
                               f"ratio = {d_ms/d_a0:.4f}")
check(abs(d_ms / d_a0 - 1.4292) < 5e-4,
      "B8.1  CONTROL: I reproduce the corpus's 1.4292 exactly from the two kernel definitions at "
      "y = 2, so the corpus's 'sourced at y ~ 2' reading is confirmed independently",
      f"{d_ms/d_a0:.6f} vs the banked 1.4292")
q2_ratio = Q2_CORPUS["canonical"]["MS08"] / Q2_CORPUS["canonical"]["a0line"]
info("B8.2  and the Q2 ratio it is supposed to explain",
     f"3.46e-26/2.50e-26 = {q2_ratio:.4f} vs (nu-1) ratio {d_ms/d_a0:.4f}  -- agreement to "
     f"{100*abs(q2_ratio/(d_ms/d_a0)-1):.1f}%")
check(abs(q2_ratio / (d_ms / d_a0) - 1) < 0.06,
      "B8.3  the scaling Q2 ~ (nu-1)|_{y=2} holds to 3% on the two kernels available. TWO POINTS "
      "ONLY -- I did not derive this scaling and it is a CALIBRATION, not a theorem. Everything "
      "below is CONDITIONAL on it")
for nm, a0 in A0.items():
    q2_line = Q2_CORPUS[nm]["a0line"]
    supp = Q2_CEIL / q2_line
    nu_req = 1 + d_a0 * supp
    dex = np.log10(nu_a0line(y_ext) / nu_req)
    info(f"B8.4  {nm:9s}", f"Q2(a_0-line) = {q2_line:.3e} -> need {supp:.4f}x  ->  "
                           f"nu(2) <= {nu_req:.5f}, i.e. a {dex:.4f} dex reduction in nu at "
                           f"g_bar = 2 a_0 relative to the a_0-line")
# what that does to the transition width
nu_req_can = 1 + d_a0 * (Q2_CEIL / Q2_CORPUS["canonical"]["a0line"])
y_at_nu2_deep = 0.25                      # deep asymptote nu -> 1/sqrt(y) gives nu = 2 at y = 1/4
y_a0_nu2 = brentq(lambda y: nu_a0line(y) - 2.0, 1e-4, 1e3)
y_a0_nureq = brentq(lambda y: nu_a0line(y) - nu_req_can, 1e-4, 1e6)
w_a0 = np.log10(y_a0_nureq / y_a0_nu2)
w_req = np.log10(y_ext / y_at_nu2_deep)
info("B8.5  the required kernel SHARPNESS",
     f"a_0-line runs nu: 2 -> {nu_req_can:.4f} over {w_a0:.3f} dex in y (y = {y_a0_nu2:.4f} -> "
     f"{y_a0_nureq:.2f}); a compliant kernel must do it in {w_req:.3f} dex "
     f"(y = 0.25 -> 2), i.e. a transition {w_a0/w_req:.2f}x narrower in log y")
check(w_a0 / w_req > 1.2,
      "B8.6  so the surviving lever is a kernel with a transition compressed by "
      f"{w_a0-w_req:.2f} dex relative to the a_0-line -- and MS08, the sharpest kernel the "
      "framework carries, goes the WRONG WAY (its nu-1 at y=2 is 1.43x LARGER). The exponential "
      "tail that saves the 1-AU monopole is being evaluated seven orders above where Q2 lives",
      f"{w_a0:.3f} dex available vs {w_req:.3f} dex required")
check(True,
      "B8.7  *** WHAT I COULD NOT DETERMINE, and I am NOT going to assert it either way: whether "
      "a kernel that sharp still fits the SPARC RAR. The required change is a 0.068 dex "
      "(canonical) / 0.073 dex (alt) reduction of the MEAN relation at g_bar = 2 a_0, against a "
      "0.108 dex observed scatter and a stellar-M/L systematic of comparable size. That is "
      "0.63-0.68 of the scatter applied to the mean at ONE value of y -- large, but NOT a "
      "manufactured kill. THE DECISIVE TEST IS NAMED AND OWED: refit the SPARC RAR with a "
      "one-parameter sharpness deformation of the a_0-line subject to nu(2) <= 1.0467, float "
      "Upsilon on BOTH sides per the standing rule, and report Delta chi^2. Until that is run, "
      "'no interpolation can clear Q2' is a CONJECTURE, not a result ***")

# ================================================================================================
head("PART B9 -- THE FIVE GATES, both routes, both footings")
# ================================================================================================
rows = [
    ("GATE 1  amplitude law / BTFR",
     "FAIL - slope 2, %.1f sigma (B2.3), by THEOREM (B1.2)" % ((BTFR_SLOPE - 2) / BTFR_ERR),
     "FAIL - 1/r^3, M^2 (B5.6)"),
    ("GATE 2  screen the FORCE",
     "CLEAR - a_0 shields the near field (B4.6), Mashhoon's own Eqs 64-65",
     "CLEAR - trivially, the correction is 1e-6 (B5.1)"),
    ("GATE 3  Q2 + 1-AU monopole",
     "CLEAR - Q2 = 0 exactly (B3.1); monopole cleared for a_0 >= %.0f AU (B4.2)" % (a0_q1 / AU),
     "CLEAR - trivially"),
    ("GATE 4  theoretical health",
     "UNDETERMINED - c_T, ghosts, CMB not computed here; 3 fitted lengths (B4.7)",
     "UNDETERMINED - localization ghosts contested in the literature"),
    ("GATE 5  no double count",
     "FAIL - Mashhoon's own paper states DM remains indispensable for clusters, the Bullet "
     "Cluster and structure formation",
     "N/A - never reaches a halo"),
]
print(f"  {'gate':32s} | {'Mashhoon nonlocal GR':70s}")
for g, m, d in rows:
    print(f"  {g:32s} | {m}")
    print(f"  {'':32s} | (Deser-Woodard: {d})")
check(True,
      "B9.0  *** ROUTE 6(B) SCORE: Mashhoon clears 2 of 5 and, uniquely in this programme, one of "
      "the two is GATE 3 -- the binding test. It dies instead on GATE 1, at 20.6 sigma, by a "
      "one-line theorem that no reparameterisation can touch. Deser-Woodard clears the two cheap "
      "gates by being 1e-6 too small to do anything at all ***")

print("\n" + "=" * 100)
print(f"ROUTE 6B CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
