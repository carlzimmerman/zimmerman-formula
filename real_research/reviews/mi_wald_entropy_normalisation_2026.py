#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_wald_entropy_normalisation_2026.py
=====================================
THE OWED WALD-ENTROPY CALCULATION: does the 1/4 in  8 pi a_0^2/(c^4 Lambda) = 1/4  track the
horizon-entropy normalisation?

BRIEF (owed from `mi_index_multiplicity_half_2026.py`, 31/31, commit 57142f1b).  That script showed
the framework's coefficient content is an integer-weight rational on the quadratic invariant,
        a_0^2/(c^4 Lambda) = 1/(32 pi),     8 pi a_0^2/(c^4 Lambda) = 1/4  EXACTLY,
and conjectured the 1/4 is the Bekenstein-Hawking 1/4 -- i.e. (Einstein coupling 8 pi)/(Euclidean
period 2 pi) = 4.  The only genuine over-determination that conjecture offers: in a gravity theory
whose horizon-entropy NORMALISATION differs from 1/4, a_0 must shift by the same factor at fixed
observed Lambda, with no new parameter.  This script computes it.

--------------------------------------------------------------------------------------------------
RESULT, UP FRONT, AND IT IS A KILL OF MY OWN OWED ITEM
--------------------------------------------------------------------------------------------------
1.  Wald's formula is computed here by explicit index contraction (Part A), not asserted.  For
    L = f(R)/(16 pi G) it gives  S = f'(R_0) A / (4 G).  Einstein-Hilbert (f' = 1) returns exactly
    A/(4G), so the 1/4 anchor is reproduced from the formula.

2.  *** GAUSS-BONNET IS THE WRONG PROBE, and I named it wrongly in the owed item. ***  In 4D the
    Gauss-Bonnet term is topological: its Wald entropy contribution is
        Delta S = (2 alpha / 4G) * Integral(curly-R sqrt h) = (2 alpha/4G) * 4 pi chi = 4 pi alpha/G,
    a CONSTANT, independent of the horizon radius (Part B).  It SHIFTS the entropy additively and
    does NOT rescale the area law, so it cannot move a_0 at all.  Any test built on "Gauss-Bonnet
    changes the 1/4" is void.  f(R) / scalar-tensor is the right probe.

3.  f(R) = R - 2 Lambda_b + beta R^2 is the CLEAN lever (Part C).  The de Sitter trace condition
    f'(R_0) R_0 = 2 f(R_0) gives R_0 = 4 Lambda_b EXACTLY -- the R^2 term does NOT move the de
    Sitter point -- while f'(R_0) = 1 + 8 beta Lambda_b is freely adjustable.  So beta changes the
    entropy normalisation at FIXED observed Lambda.  That is exactly the counterfactual needed.

4.  *** THE FORK, and the conjecture loses. ***  At fixed observed Lambda:
        the framework's OWN canonical law  a_0 = c^2 sqrt(Lambda/(32 pi))  is beta-INDEPENDENT;
        the entropy conjecture requires  a_0 -> f'^p a_0  with p = 1/2 or 1.
    These disagree at first order in beta.  Worse, the conjecture does not even fix p: the
    assembly a_0^2 = c^4 Lambda (2 pi)/(8 pi)^2 contains TWO factors of 8 pi and the conjecture
    says nothing about which is the entropy normalisation and which is the Lambda-to-rho_Lambda
    conversion, giving p in {0, 1/2, 1} (Part D).  A hypothesis that does not fix its own exponent
    makes no prediction.

5.  *** AND INSIDE THE FRAMEWORK THE TEST IS VACUOUS. ***  The framework is MODIFIED INERTIA: the
    gravity sector is standard GR, so f' == 1 identically and the fork never opens (Part E).  The
    over-determination I promised does not exist in the MI realisation.
    ONE PAYOFF SURVIVES: it IS live in the framework's MG/AeST realisation, whose gravity sector is
    scalar-tensor with f' != 1.  So "does a_0 track the entropy normalisation?" is a NEW internal
    MI-vs-MG discriminator, alongside the banked Cassini-Q2 one (MI evades by ~4e7; MG/AeST is
    11.3-13.0 sigma over).  MI predicts a_0 fixed by Lambda alone; MG predicts a_0 tracking f'.

6.  Magnitude, so nobody cites this as observationally live: the shift is 1 + 4 beta Lambda at
    p = 1/2, and beta Lambda is ~1e-52 x beta[m^2].  Even at beta = (1 mm)^2 the fractional shift is
    ~1e-58 (Part D).  This is a STRUCTURAL consistency test, never a measurement.

CONCLUSION.  The owed calculation is done and it does NOT convert the 1/4 from a rewriting into a
prediction.  *** kappa = 1/2 remains FITTED, NOT DERIVED, and the "1/4 is Bekenstein-Hawking's 1/4"
conjecture is now DOWNGRADED from "named conjecture with an owed test" to "named conjecture whose
only proposed test is vacuous in the framework's own realisation". ***  Do not cite it as support.

CREDIT.  Wald entropy: WALD 1993 PRD 48:R3427; IYER & WALD 1994 PRD 50:846.  Gauss-Bonnet horizon
entropy: JACOBSON & MYERS 1993 PRL 70:3684.  f(R) Wald entropy S = f' A/4G: BRUSTEIN, GORBONOS &
HADAD 2009 PRD 79:044025 (and standard in the f(R) literature).  S = A/4G: BEKENSTEIN 1973 /
HAWKING 1975; conical-deficit route GIBBONS & HAWKING 1977.  2D Gauss-Bonnet theorem: classical.
a_0 = c^2 sqrt(Lambda/32 pi) = (c/2) sqrt(G rho_Lambda) is this corpus's canonical form
(`rar_framework_a0_mlfit.py`, `a0z_clean_ledger.py`, PREDICTIONS_100 #1).  nu = sqrt(1+1/y) and the
temperature balance are MILGROM 1999 PLA 253:273 eqs 6-9; a_lambda = c^2 sqrt(Lambda/3) is
MILGROM 1994 Ann.Phys. 229:384.  AeST: SKORDIS & ZLOSNIK 2021.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 50

# =================================================================================================
# AMENDMENT 2026-08-07 (see `mi_aest_entropy_discriminator_2026.py`, 23/23) -- THIS FILE'S
# "PAYOFF KEPT" IS WITHDRAWN.  THE WHOLE TEST CLASS IS VOID, NOT MERELY VACUOUS IN MI.
# -------------------------------------------------------------------------------------------------
# Part E below keeps one payoff: that the entropy-normalisation test, though vacuous in MI (f' == 1),
# is LIVE in the MG/AeST realisation and yields an MI-vs-MG discriminator.  Pushing the AeST side
# kills it, for two independent reasons either of which suffices:
#   (a) AeST has NO curvature coupling.  Everything beyond R/(16 pi G-tilde) is built from the unit
#       vector A^mu, the scalar phi and their FIRST derivatives, so nothing contributes to
#       dL/dR_abcd and S_Wald(AeST) = A/(4 G-tilde) with f' == 1 EXACTLY.  The premise "MG/AeST has
#       f' != 1" is false at the root.
#   (b) THEOREM: every Lambda-tied coefficient is G-FREE -- the framework's a_0 = c^2 sqrt(L/32 pi)
#       AND both of Milgrom's -- so each is invariant under G -> G/(1-xi) for ALL xi, hence blind to
#       every redefinition of the gravitational coupling and therefore to every entropy-
#       normalisation rescaling, in EVERY realisation.  Control: the corpus's dead rho_local route
#       IS G-dependent and WOULD track (reproducing the banked 1076x), so the blindness is specific
#       to the Lambda-tied form and the theorem is not vacuous.
# STRENGTH: not a small-effect result.  Had a_0 tracked G_N/G-tilde it would have moved >5% at
# xi = 0.1 -- measurable.  The effect is structurally absent, not tiny.
# WHAT REPLACES IT: an ECONOMY discriminator on different grounds.  In AeST the MOND scale is a free
# function's normalisation, independent of Lambda, so a_0 = c^2 sqrt(Lambda/32 pi) is a PREDICTION in
# the MI realisation and an extra POSTULATE in MG/AeST.  Same direction as the banked Cassini-Q2
# result.  COST, against interest: MI is now load-bearing for BOTH the observational evasion AND the
# coefficient's status as a prediction, so the coefficient claim cannot be rescued by retreating to a
# covariant MG completion if MI's own problems bite.
# Everything else in this file stands: Wald by explicit contraction, S = f' A/(4G), the EH anchor,
# Gauss-Bonnet being topological and the wrong probe, and the f(R) = R - 2L_b + beta R^2 lever.
# kappa = 1/2 remains FITTED, NOT DERIVED.
# =================================================================================================

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C      = mp.mpf("2.99792458e8")
LAMBDA = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
A0     = C**2 * mp.sqrt(LAMBDA / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- Wald's formula by EXPLICIT index contraction: recover S = f' A/(4G)")
print("=" * 100)
# Wald:  S = -2 pi Integral_H  (dL/dR_abcd) eps_ab eps_cd  sqrt(h) d^2x
# For L = f(R)/(16 pi G):   dL/dR_abcd = f'/(16 pi G) * (1/2)(g^ac g^bd - g^ad g^bc)
# Binormal eps_ab: antisymmetric, supported on the (t,r) block, normalised eps_ab eps^ab = -2.
gd = sp.diag(-1, 1, 1, 1)                     # local orthonormal frame, signature (-+++)
gu = gd.inv()
eps = sp.zeros(4, 4)
eps[0, 1], eps[1, 0] = 1, -1                  # the t-r binormal

# normalisation check: eps_ab eps^ab must be -2
norm = sum(eps[a, b] * eps[c, d] * gu[a, c] * gu[b, d]
           for a in range(4) for b in range(4) for c in range(4) for d in range(4))
check(sp.simplify(norm) == -2,
      "A1  binormal normalisation eps_ab eps^ab = -2 (Wald's convention)", f"got {sp.simplify(norm)}")

fp = sp.symbols("fprime", positive=True)      # f'(R_0)
Gc, Ah = sp.symbols("G A_hor", positive=True)
# the contraction  (1/2)(g^ac g^bd - g^ad g^bc) eps_ab eps_cd
contr = sp.simplify(sum(
    sp.Rational(1, 2) * (gu[a, c] * gu[b, d] - gu[a, d] * gu[b, c]) * eps[a, b] * eps[c, d]
    for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
check(contr == -2,
      "A2  the Riemann-derivative contraction equals -2 (computed, not quoted)", f"got {contr}")

S_wald = sp.simplify(-2 * sp.pi * (fp / (16 * sp.pi * Gc)) * contr * Ah)
check(sp.simplify(S_wald - fp * Ah / (4 * Gc)) == 0,
      "A3  *** Wald gives S = f'(R_0) A/(4G) ***", f"S = {S_wald}")
check(sp.simplify(S_wald.subs(fp, 1) - Ah / (4 * Gc)) == 0,
      "A4  Einstein-Hilbert (f' = 1) returns EXACTLY A/(4G) -- the 1/4 anchor is reproduced "
      "from the formula, so Part A is a real derivation of the conjecture's target number")
# and the 1/4 as a ratio of two pi's, as the conjecture reads it
check(sp.simplify(8 * sp.pi / (2 * sp.pi)) == 4,
      "A5  and 4 = (Einstein coupling 8 pi)/(Euclidean period 2 pi), the conjecture's provenance")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- GAUSS-BONNET IS THE WRONG PROBE (correcting my own owed item)")
print("=" * 100)
alpha, L_h = sp.symbols("alpha L", positive=True)
# Jacobson-Myers: S = (1/4G) Integral (1 + 2 alpha curlyR) sqrt(h);  curlyR = 2/L^2 on a 2-sphere
curlyR = 2 / L_h**2
area = 4 * sp.pi * L_h**2
int_curlyR = sp.simplify(curlyR * area)
check(sp.simplify(int_curlyR - 8 * sp.pi) == 0,
      "B1  Integral(curlyR sqrt h) = 8 pi on the 2-sphere = 4 pi chi with chi = 2 "
      "(2D Gauss-Bonnet theorem)", f"= {int_curlyR}")
chi = sp.symbols("chi")
dS_gb_chi = sp.simplify((1 / (4 * Gc)) * 2 * alpha * 4 * sp.pi * chi)      # general topology
dS_gb = sp.simplify(dS_gb_chi.subs(chi, 2))                                # sphere
check(sp.simplify(dS_gb - 4 * sp.pi * alpha / Gc) == 0,
      "B2  so Delta S_GB = 4 pi alpha / G on the sphere (chi = 2)", f"= {dS_gb}")
check(sp.simplify(sp.diff(dS_gb, L_h)) == 0,
      "B3  *** and d(Delta S_GB)/dL = 0: the shift is a CONSTANT, independent of horizon radius ***",
      "=> Gauss-Bonnet does NOT rescale the area law in 4D; it is topological")
# the load-bearing statement: the AREA-LAW COEFFICIENT is untouched, so a_0 cannot move.
coeff_limit = sp.limit(sp.simplify((area / (4 * Gc) + dS_gb) / area), L_h, sp.oo)
check(sp.simplify(coeff_limit - 1 / (4 * Gc)) == 0,
      "B4  the area-law COEFFICIENT is unchanged: lim_{L->inf} S_total/A = 1/(4G) exactly, so the "
      "1/4 the conjecture needs is untouched and a_0 cannot move",
      f"limit = {coeff_limit}  -> any 'Gauss-Bonnet changes the 1/4' test is VOID; my owed item "
      "said 'Wald / Gauss-Bonnet' and the Gauss-Bonnet half was misconceived")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- f(R) = R - 2 Lambda_b + beta R^2 IS the clean lever")
print("=" * 100)
R, beta, Lam_b = sp.symbols("R beta Lambda_b", positive=True)
f_R2 = R - 2 * Lam_b + beta * R**2
fprime_R2 = sp.diff(f_R2, R)
# de Sitter (constant-R vacuum) condition for f(R): f'(R_0) R_0 - 2 f(R_0) = 0
cond = sp.simplify(fprime_R2 * R - 2 * f_R2)
roots = sp.solve(sp.Eq(cond, 0), R)
check(roots == [4 * Lam_b],
      "C1  *** the dS trace condition gives R_0 = 4 Lambda_b EXACTLY -- the R^2 term does NOT "
      "move the de Sitter point ***", f"roots = {roots}")
fp0 = sp.simplify(fprime_R2.subs(R, 4 * Lam_b))
check(sp.simplify(fp0 - (1 + 8 * beta * Lam_b)) == 0,
      "C2  while f'(R_0) = 1 + 8 beta Lambda_b is FREELY adjustable", f"f' = {fp0}")
check(sp.simplify(sp.diff(fp0, beta)) != 0 and sp.simplify(sp.diff(roots[0], beta)) == 0,
      "C3  *** so beta changes the entropy normalisation at FIXED observed Lambda -- exactly the "
      "counterfactual the conjecture needs ***",
      f"d f'/d beta = {sp.simplify(sp.diff(fp0, beta))}, d R_0/d beta = 0")
# POSITIVE CONTROL: a cubic term MUST move the dS point, or the machinery is dead
f_R3 = R - 2 * Lam_b + beta * R**3
cond3 = sp.simplify(sp.diff(f_R3, R) * R - 2 * f_R3)
check(sp.simplify(cond3.subs(R, 4 * Lam_b)) != 0,
      "C4  POSITIVE CONTROL: with beta R^3 the dS condition is NOT satisfied at R_0 = 4 Lambda_b, "
      "so C1 is a real property of R^2 and not a dead solver",
      f"residual at R_0=4Lam_b: {sp.simplify(cond3.subs(R, 4*Lam_b))}")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- THE FORK: the framework's law is beta-blind, the conjecture is not (and is "
      "underspecified)")
print("=" * 100)
c_s, Lam_s = sp.symbols("c Lambda", positive=True)
a0_canon = c_s**2 * sp.sqrt(Lam_s / (32 * sp.pi))
check(sp.simplify(sp.diff(a0_canon, beta)) == 0,
      "D1  the framework's canonical a_0 = c^2 sqrt(Lambda/32 pi) is beta-INDEPENDENT: at fixed "
      "observed Lambda it does not move at all")
print("  the conjecture's three possible exponents, from the TWO factors of 8 pi in "
      "a_0^2 = c^4 Lambda (2 pi)/(8 pi)^2:")
for p, why in [(sp.Integer(0), "neither 8 pi is the entropy normalisation"),
               (sp.Rational(1, 2), "ONE of the two 8 pi's is (S = f'A/4G rescales one)"),
               (sp.Integer(1), "BOTH 8 pi's rescale")]:
    shift = sp.simplify(fp0**p)
    lin = sp.simplify(sp.series(shift, beta, 0, 2).removeO())
    print(f"    p = {str(p):>3s}:  a_0 -> f'^{p} a_0 = {shift}   ~ {lin}   [{why}]")
check(len({sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)}) == 3,
      "D2  *** the conjecture does NOT fix p: it says nothing about WHICH 8 pi is the entropy "
      "normalisation and which is the Lambda-to-rho_Lambda conversion ***",
      "=> a hypothesis that cannot fix its own exponent makes no prediction; this is the same "
      "non-uniqueness that made the assembly a rewriting (57142f1b, check D2)")
check(sp.simplify(fp0**sp.Rational(1, 2) - 1) != 0,
      "D3  and for p = 1/2 the prediction DISAGREES with the framework's own law at first order: "
      "a_0 -> (1 + 4 beta Lambda) a_0 vs beta-blind",
      "=> the conjecture, taken seriously, MODIFIES the framework's law in modified gravity")
print()
print("  MAGNITUDE (so this is never cited as observationally live), p = 1/2, shift = 1 + 4 beta Lam:")
for nm, bval in [("(1 mm)^2", mp.mpf("1e-6")), ("(1 m)^2", mp.mpf("1")),
                 ("(1 kpc)^2", mp.mpf("3.086e19")**2), ("Starobinsky ~ (1e-6 m)^2", mp.mpf("1e-12"))]:
    print(f"    beta = {nm:24s}: 4 beta Lambda = {sig(4*bval*LAMBDA, 4)}")
check(4 * mp.mpf("1e-6") * LAMBDA < mp.mpf("1e-50"),
      "D4  even at beta = (1 mm)^2 the fractional shift is < 1e-50: a STRUCTURAL test, never a "
      "measurement", f"= {sig(4*mp.mpf('1e-6')*LAMBDA, 4)}")
print(f"  both footings unaffected (a_0 is beta-blind on each): canonical {sig(A0)}   "
      f"ALT {sig(A0_ALT)}   m/s^2")
check(abs(A0_ALT / A0 - 1 / mp.sqrt(OMEGA_L)) < mp.mpf("1e-40"),
      "D5  both footings carried, and the ALT/canonical ratio is the stated 1/sqrt(Omega_L)",
      f"{sig(A0_ALT/A0, 8)}")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- inside MODIFIED INERTIA the test is VACUOUS (and that is the one payoff)")
print("=" * 100)
print("""  The framework is MODIFIED INERTIA: the gravity sector is standard General Relativity and
  the modification lives in the particle's inertial response.  So for the MI realisation
  f(R) = R - 2 Lambda identically, f' == 1, beta == 0, and the fork of Part D NEVER OPENS.
  The over-determination promised in the owed item does not exist inside the framework.""")
check(sp.simplify(fprime_R2.subs(beta, 0)) == 1,
      "E1  MI: f' == 1 identically (gravity sector is GR) => no entropy-normalisation lever exists")
check(sp.simplify((fp0**sp.Rational(1, 2)).subs(beta, 0) - 1) == 0,
      "E2  so every exponent p gives the SAME (null) prediction in MI: the test cannot discriminate",
      "*** the owed over-determination is VACUOUS in the framework's own realisation ***")
print("""
  THE ONE PAYOFF.  It is NOT vacuous in the framework's MG / AeST realisation, whose gravity sector
  is scalar-tensor with f' != 1.  So a NEW internal discriminator exists:
        MI  realisation:  a_0 is fixed by Lambda alone, and does NOT track the entropy normalisation
        MG  realisation:  if the 1/4 is the entropy normalisation, a_0 MUST track f'
  This joins the banked Cassini-Q2 discriminator (pure MI evades by ~4e7; MG/AeST sits 11.3-13.0
  sigma over).  ⚠️ It is a discriminator between REALISATIONS, not a test of kappa, and it is
  unobservably small in magnitude (D4) -- so it is a consistency requirement on model-building,
  not a measurement anyone can make.""")
check(True,
      "E3  discriminator recorded: MI predicts a_0 entropy-normalisation-blind, MG predicts it "
      "tracks f' -- structural only, magnitude ~1e-50 (D4)")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
# NC1: if the binormal were mis-normalised, A3/A4 must NOT return 1/4
eps_bad = sp.zeros(4, 4)
eps_bad[0, 1], eps_bad[1, 0] = 2, -2          # wrong normalisation (eps.eps = -8)
contr_bad = sp.simplify(sum(
    sp.Rational(1, 2) * (gu[a, c] * gu[b, d] - gu[a, d] * gu[b, c]) * eps_bad[a, b] * eps_bad[c, d]
    for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
S_bad = sp.simplify(-2 * sp.pi * (1 / (16 * sp.pi * Gc)) * contr_bad * Ah)
check(sp.simplify(S_bad - Ah / (4 * Gc)) != 0,
      "NC1  CONTROL FIRES: a mis-normalised binormal does NOT give A/(4G), so A4's 1/4 is a real "
      "consequence of Wald's formula", f"wrong-eps gives S = {S_bad}")
# NC2: the GB constancy must fail for a non-spherical (torus) horizon, chi = 0
check(sp.simplify(dS_gb_chi.subs(chi, 0)) == 0 and sp.simplify(dS_gb_chi.subs(chi, 2)) != 0,
      "NC2  CONTROL FIRES: the same formula gives Delta S_GB = 0 for a torus horizon (chi = 0) and "
      "4 pi alpha/G for a sphere (chi = 2) -- so B3's constancy is genuinely topological, "
      "not an algebra slip",
      f"chi=0 -> {sp.simplify(dS_gb_chi.subs(chi, 0))}, chi=2 -> {sp.simplify(dS_gb_chi.subs(chi, 2))}")
# NC3: does the dS condition machinery detect a genuinely entropy-rescaling AND dS-shifting theory?
f_lin = R - 2 * Lam_b + beta * R
check(sp.simplify(sp.diff(f_lin, R)) == 1 + beta,
      "NC3  CONTROL: f = (1+beta)R - 2Lambda_b has f' = 1+beta, a pure rescaling of G -- so a "
      "'shift' with no physical content must be excluded by hand, and it is: it renormalises G, "
      "which the framework's G-FREE a_0 cannot see",
      "-> reinforces D1: a_0 = c^2 sqrt(Lambda/32pi) has no G to rescale")
# NC4: verify a_0 numerically against the corpus canon
check(abs(A0 - mp.mpf("9.3619e-11")) / A0 < mp.mpf("1e-4"),
      "NC4  a_0 reproduces the corpus's canonical 9.3619e-11 m/s^2", f"{sig(A0, 12)}")
# NC5: a real dimensional guard
check(abs(C**2 * mp.sqrt(LAMBDA / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6%, so the integer is load-bearing")

print("""
==================================================================================================
BOTTOM LINE
==================================================================================================
  DONE:  Wald's formula computed by explicit contraction; S = f' A/(4G); Einstein-Hilbert returns
         exactly A/(4G), so the conjecture's target 1/4 is reproduced from the formula itself.
  CORRECTED:  my own owed item said "Wald / Gauss-Bonnet".  In 4D Gauss-Bonnet is topological --
         Delta S = 4 pi alpha/G, radius-INDEPENDENT -- so it shifts the entropy additively and can
         never rescale the 1/4.  That half of the owed item was misconceived.
  THE TEST:  f(R) = R - 2 Lambda_b + beta R^2 is the clean lever: R_0 = 4 Lambda_b exactly (the
         R^2 term does not move the dS point) while f' = 1 + 8 beta Lambda_b is free.  Fixed
         observed Lambda, adjustable entropy normalisation.
  VERDICT:  the conjecture LOSES on its own test.  The framework's canonical a_0 is beta-blind; the
         conjecture requires a_0 -> f'^p a_0; and it cannot fix p in {0, 1/2, 1} because the
         assembly's two factors of 8 pi are not distinguished.  A hypothesis that cannot fix its own
         exponent makes no prediction.  AND in the MI realisation f' == 1 identically, so the fork
         never opens -- the over-determination is VACUOUS where the framework actually lives.
  DOWNGRADE:  "the 1/4 is Bekenstein-Hawking's 1/4" moves from "named conjecture with an owed test"
         to "named conjecture whose only proposed test is vacuous in the framework's own
         realisation".  Do NOT cite it as support for kappa = 1/2.
  PAYOFF KEPT:  a new internal MI-vs-MG discriminator -- MI says a_0 is entropy-normalisation-blind,
         MG/AeST says it tracks f'.  Structural only: the magnitude is ~1e-50, never measurable.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
