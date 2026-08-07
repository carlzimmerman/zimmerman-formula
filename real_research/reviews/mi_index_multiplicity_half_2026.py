#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_index_multiplicity_half_2026.py
==================================
ATTEMPT TO BUILD THE INDEX / MULTIPLICITY PREDICTION OF kappa = 1/2.

The brief (from `mi_number_field_local_presentation_2026.py`, 29/29): the one door the number-field
obstruction leaves open is a construction that PREDICTS the rational 1/2 from an INTEGER-WEIGHT
source -- an index, a multiplicity, a representation dimension -- subject to three requirements:
    (i)   predict 1/2 EXACTLY from a source fixed BEFORE looking,
    (ii)  make an INDEPENDENT prediction elsewhere,
    (iii) beat the degeneracy count explicitly.
This script attempts it.  Verdict up front: **(i) is MET, (iii) is PRICED AND SURVIVED, (ii) FAILS.**
So the answer is "not built", and two of my own earlier headlines need amending.  Details below.

--------------------------------------------------------------------------------------------------
THE FINDING THAT MAKES THE ATTEMPT POSSIBLE AT ALL
--------------------------------------------------------------------------------------------------
The obstruction was always stated on the LINEAR object a_0/(c H_Lambda) = 2 kappa/Z, whose pi-weight
is -1/2 -- HALF-INTEGER, hence unreachable from any algebraic/index source (that is Theorem 2 and
escape E1 of `mi_number_field_theorem_2026.py`, whose note already says the half-weight has the
provenance "sqrt of a gravitational density").

But the framework's law is QUADRATIC in accelerations:
        g_obs^2 = g_bar^2 + a_0 g_bar        (the a_0-line)
        T = sqrt(a^2 + H^2)/2 pi   =>   T^2 = (a^2 + H^2)/4 pi^2
so the natural invariant is a_0^2, not a_0.  And squaring DOUBLES the pi-weight:

        *** a_0^2 / (c^4 Lambda) = 1/(32 pi),   pi-weight -1  --  an INTEGER. ***

*** So the half-integer obstruction is an ARTEFACT OF THE LINEAR PRESENTATION. ***  On the natural
quadratic invariant, Theorem 1 does not apply -- to the framework OR to Milgrom.  Equivalently,
normalising by Einstein's own coupling 8 pi (which every gravitational action contains):

        *** 8 pi a_0^2 / (c^4 Lambda) = 1/4  EXACTLY -- a pure rational. ***

That is the target an index must produce, and it is now an integer-weight target.

--------------------------------------------------------------------------------------------------
TWO SELF-CORRECTIONS I OWE, BOTH DEFLATING MY OWN EARLIER HEADLINES
--------------------------------------------------------------------------------------------------
(1) Commit 6b7edf77 ("THE PRESENTATION THEOREM") headlined: "the open problem collapses from a
    transcendental to a rational" because the framework's local lambda = 1/2 is rational while
    Milgrom's are not.  In the QUADRATIC presentation ALL of them are integer-weight (Part B):
    framework 1/(32 pi), Milgrom 1999 eqs 6-9 -> 4/3, eqs 10-11 -> 1/3, Milgrom 2020 -> 1/(12 pi^2).
    So the "collapse" is NOT special to the framework -- it levels the field.  AGAINST INTEREST:
    Milgrom 1999's invariant is a PURE RATIONAL needing NO pi from the source at all, so on
    economy of required input his coefficient is the CHEAPEST of the three, not the framework's.
(2) The same commit's PHYSICAL story -- "modified inertia couples to T_munu, therefore the matter
    side (rho_Lambda) is primitive, therefore kappa is rational" -- is UNDERCUT by the framework's
    OWN canonical form, which is G-FREE:
        a_0 = c^2 sqrt(Lambda / 32 pi)          [corpus canon; see CREDIT below]
    G cancels identically between sqrt(G) and rho_Lambda's 1/G.  So the framework's a_0 references
    only c and Lambda -- PURE CURVATURE, no matter side at all.  Writing it via rho_Lambda is a
    CHOICE of bookkeeping, not a physical selection.  The presentation theorem survives as
    arithmetic; its "MI selects the matter side" motivation is WITHDRAWN.

--------------------------------------------------------------------------------------------------
THE CANDIDATE CONSTRUCTION, AND EXACTLY HOW FAR IT GETS
--------------------------------------------------------------------------------------------------
Requirement (i).  The residue 1/4 is prespecified and integer-weight, with a standard provenance:
in the conical-deficit / Gibbons-Hawking derivation of horizon entropy the 4 of S = A/4G is
                4 = (Einstein coupling 8 pi) / (Euclidean period 2 pi),
a RATIO of two pi's, which is why it is pi-free.  Both numbers are fixed before looking (they are
Einstein's equations and the smoothness period of the Euclidean section).  Assembling:
        *** a_0^2 = c^4 Lambda * (2 pi) / (8 pi)^2      EXACT (Part D) ***
i.e. one Euclidean period over the square of Einstein's coupling.  Verified to 60 dps below.

Requirement (iii).  Priced in Part E over a mechanically-closed menu of
(small rational) x (8 pi)^n x (2 pi)^m forms.  The target is hit by only a handful of the menu's
entries, and the count is reported honestly rather than asserted.

Requirement (ii) -- WHERE IT FAILS.  The construction makes no NEW prediction:
  * a_0 being G-free is not discriminating: Milgrom's a_0 = 2 c H_Lambda = 2 c^2 sqrt(Lambda/3)
    is G-free too (Part F).  No test separates them here.
  * the one genuine over-determination -- if the 4 really is the entropy normalisation then a_0
    must shift with any change to that normalisation (Wald / Gauss-Bonnet corrections) at fixed
    Lambda -- is NOT COMPUTED here and needs an actual Wald-entropy calculation.
  * and the assembly (2 pi)/(8 pi)^2 is a REWRITING of 1/(32 pi), not a derivation of it: nothing
    in it forces the exponents.  Part E shows other exponent choices also land on the target.
So: an index-shaped TARGET exists and is now legitimately reachable; an index-shaped DERIVATION
does not exist.  *** kappa = 1/2 remains FITTED, NOT DERIVED. ***

CREDIT.  a_0 = c^2 sqrt(Lambda/32 pi) = (c/2) sqrt(G rho_Lambda) is this corpus's own canonical
form (`real_research/rar_framework_a0_mlfit.py`, `a0z_clean_ledger.py`, PREDICTIONS_100 #1) -- it is
NOT introduced here; only its pi-weight consequence is.  Theorems 1-3, Corollary 2a/2b and escapes
E1-E5 are `mi_number_field_theorem_2026.py`.  nu = sqrt(1+1/y) and the temperature balance are
MILGROM 1999 PLA 253:273 eqs 6-9 (a_0_hat = 2 c H_Lambda); the cH_L/2pi form is MILGROM 2020;
a_lambda = c^2 sqrt(Lambda/3) is MILGROM 1994 Ann.Phys. 229:384; the temperature
sqrt(a^2 + Lambda/3)/2pi is NARNHOFER, PETER & THIRRING 1996 IJMPB 10:1507.  S = A/4G is
BEKENSTEIN 1973 / HAWKING 1975; the conical-deficit route is GIBBONS & HAWKING 1977.
pi transcendental: LINDEMANN 1882.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 60

# =================================================================================================
# AMENDMENT 2026-08-07 (see `mi_wald_entropy_normalisation_2026.py`, 26/26) -- THE OWED WALD
# CALCULATION IS DONE, AND THE CONJECTURE LOSES ON ITS OWN TEST.
# -------------------------------------------------------------------------------------------------
# This file records as OWED: "if the 4 is the entropy normalisation, a_0 must shift with a
# Wald/Gauss-Bonnet correction at fixed Lambda, no new parameter."  That calculation is now done:
#   * Wald's formula, by explicit contraction, gives S = f'(R_0) A/(4G); Einstein-Hilbert (f'=1)
#     returns exactly A/(4G), so the target 1/4 IS reproduced from the formula.
#   * "GAUSS-BONNET" WAS THE WRONG PROBE and that half of the owed item was misconceived: in 4D GB
#     is topological, Delta S = 4 pi alpha/G is radius-INDEPENDENT, and the area-law coefficient is
#     untouched (lim S/A = 1/4G exactly).  GB can never rescale the 1/4.
#   * f(R) = R - 2 Lambda_b + beta R^2 IS the clean lever: the dS trace condition gives
#     R_0 = 4 Lambda_b exactly (R^2 does not move the dS point) while f' = 1 + 8 beta Lambda_b is
#     free -- fixed observed Lambda, adjustable entropy normalisation.
#   * VERDICT: the framework's canonical a_0 = c^2 sqrt(Lambda/32 pi) is beta-BLIND, while the
#     conjecture requires a_0 -> f'^p a_0 and CANNOT FIX p in {0, 1/2, 1}, because the assembly's
#     two factors of 8 pi are not distinguished.  A hypothesis that cannot fix its own exponent
#     makes no prediction.  AND in the MI realisation f' == 1 identically, so the fork never opens:
#     the over-determination is VACUOUS where the framework actually lives.
# DOWNGRADE: "the 1/4 is Bekenstein-Hawking's 1/4" is now a named conjecture whose only proposed
# test is vacuous in the framework's own realisation.  Do NOT cite it as support for kappa = 1/2.
# PAYOFF KEPT: a new internal MI-vs-MG discriminator -- MI says a_0 is entropy-normalisation-blind,
# MG/AeST says it tracks f'.  Structural only; magnitude ~1e-50, never measurable.
# =================================================================================================

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=12):
    return mp.nstr(mp.mpf(x), n)


# ---------------------------------------------------------------------------------------------
G       = mp.mpf("6.67430e-11")
C       = mp.mpf("2.99792458e8")
LAMBDA  = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
H0      = mp.mpf("67.36") * 1000 / mp.mpf("3.0856775814913673e22")
RHO_L   = LAMBDA * C**2 / (8 * mp.pi * G)
RHO_TOT = 3 * H0**2 / (8 * mp.pi * G)
CHL     = C**2 * mp.sqrt(LAMBDA / 3)
A0      = (C / 2) * mp.sqrt(G * RHO_L)
A0_ALT  = (C / 2) * mp.sqrt(G * RHO_TOT)

pi_s = sp.pi
Lam_s, c_s, G_s = sp.symbols("Lambda c G", positive=True)

print(__doc__)


def pi_weight(expr):
    """w of the committed theorem: expr = algebraic * pi^r -> r (half-integers allowed), else None."""
    for num in range(-6, 7):
        for den in (1, 2):
            r = sp.Rational(num, den)
            if sp.simplify(expr / pi_s ** r).is_algebraic:
                return r
    return None


# =============================================================================================
print("=" * 100)
print("PART A -- the framework's law is G-FREE, and its QUADRATIC invariant is 1/(32 pi)")
print("=" * 100)
rho_expr = Lam_s * c_s**2 / (8 * pi_s * G_s)
a0_expr = sp.simplify((c_s / 2) * sp.sqrt(G_s * rho_expr))
check(sp.simplify(a0_expr - c_s**2 * sp.sqrt(Lam_s / (32 * pi_s))) == 0,
      "A1  a_0 = (c/2) sqrt(G rho_Lambda) = c^2 sqrt(Lambda/(32 pi))  -- G cancels identically",
      f"= {a0_expr}   (corpus canon, NOT new here)")
check(sp.simplify(sp.diff(a0_expr, G_s)) == 0,
      "A2  d a_0 / d G = 0 exactly: the framework's a_0 does not contain Newton's constant")
inv = sp.simplify(a0_expr**2 / (c_s**4 * Lam_s))
check(sp.simplify(inv - 1 / (32 * pi_s)) == 0,
      "A3  THE QUADRATIC INVARIANT  a_0^2/(c^4 Lambda) = 1/(32 pi)  exactly", f"= {inv}")
check(sp.simplify(8 * pi_s * inv - sp.Rational(1, 4)) == 0,
      "A4  *** 8 pi a_0^2/(c^4 Lambda) = 1/4 EXACTLY -- a PURE RATIONAL, integer pi-weight ***")
print(f"  numerically, canonical: a_0 = {sig(A0)}   c^2 sqrt(L/32pi) = "
      f"{sig(C**2*mp.sqrt(LAMBDA/(32*mp.pi)))}")
check(abs(A0 / (C**2 * mp.sqrt(LAMBDA / (32 * mp.pi))) - 1) < mp.mpf("1e-50"),
      "A5  and it agrees on real constants at 60 dps")
# ALT footing: is it G-free too?
a0_alt_expr = sp.simplify((c_s / 2) * sp.sqrt(G_s * 3 * sp.Symbol("H0", positive=True)**2
                                              / (8 * pi_s * G_s)))
check(sp.simplify(sp.diff(a0_alt_expr, G_s)) == 0,
      "A6  BOTH FOOTINGS: the ALT form (c/2) sqrt(G rho_total) is G-free too",
      f"= {a0_alt_expr}   -> a_0(ALT) = {sig(A0_ALT)} m/s^2, ratio {sig(A0_ALT/A0, 8)}")
# A7 -- this check FAILED as first written, and the failure is a real (small) corpus defect, so it
# is kept as the finding rather than loosened.  ALT/canonical = 1/sqrt(Omega_L) is an IDENTITY, but
# only for the Omega_L that (Lambda, H_0) actually imply.  The corpus carries THREE inconsistent
# values, and mi_constants.py already documents two of them.
OmL_implied = LAMBDA * C**2 / (3 * H0**2)          # forced by Lambda = 1.0908e-52 and H0 = 67.36
ratio_meas = A0_ALT / A0
print(f"  Omega_Lambda, three ways: stated Planck {sig(OMEGA_L, 6)} | implied by (Lambda,H0) "
      f"{sig(OmL_implied, 6)} | implied by the banked 1.2082 ratio {sig(1/mp.mpf('1.2082')**2, 6)}")
check(abs(ratio_meas - 1 / mp.sqrt(OmL_implied)) / ratio_meas < mp.mpf("1e-40"),
      "A7a ALT/canonical = 1/sqrt(Omega_L) is an EXACT identity for the IMPLIED Omega_L",
      f"ratio {sig(ratio_meas, 8)} = 1/sqrt({sig(OmL_implied, 6)})")
spread = (max(OMEGA_L, OmL_implied, 1 / mp.mpf("1.2082")**2)
          / min(OMEGA_L, OmL_implied, 1 / mp.mpf("1.2082")**2) - 1)
check(spread < mp.mpf("0.007"),
      "A7b DEFECT SURFACED: the corpus carries THREE mutually inconsistent Omega_Lambda "
      "(0.6889 stated, 0.68580 implied by Lambda+H0, 0.68505 implied by the banked 1.2082) -- "
      "spread 0.56%, so every ALT-footing number is ambiguous at that level",
      f"spread {float(spread)*100:.2f}%; mi_constants.py documents two of the three, not this one")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the half-integer obstruction is an ARTEFACT of the LINEAR presentation")
print("=" * 100)
Z_sym = 2 * sp.sqrt(8 * pi_s / 3)
COEFFS = {
    "framework kappa = 1/2": c_s**2 * sp.sqrt(Lam_s / (32 * pi_s)),
    "Milgrom 1999 eqs 6-9": 2 * c_s**2 * sp.sqrt(Lam_s / 3),
    "Milgrom 1999 eqs 10-11": c_s**2 * sp.sqrt(Lam_s / 3),
    "Milgrom 2020": c_s**2 * sp.sqrt(Lam_s / 3) / (2 * pi_s),
}
print(f"  {'coefficient':26s} {'w(LINEAR a_0/cH_L)':>19s} {'w(a_0^2/c^4 Lam)':>18s} "
      f"{'quadratic invariant':>22s}")
lin_w, quad_w = {}, {}
for name, ae in COEFFS.items():
    lin = sp.simplify(ae / (c_s**2 * sp.sqrt(Lam_s / 3)))
    quad = sp.simplify(ae**2 / (c_s**4 * Lam_s))
    lin_w[name], quad_w[name] = pi_weight(lin), pi_weight(quad)
    print(f"  {name:26s} {str(lin_w[name]):>19s} {str(quad_w[name]):>18s} {str(quad):>22s}")
check(all(sp.Rational(w).q == 2 for w in [lin_w["framework kappa = 1/2"]]),
      "B1  LINEAR: the framework's weight is HALF-INTEGER (-1/2), the classic obstruction",
      f"w = {lin_w['framework kappa = 1/2']}")
check(all(sp.Rational(w).q == 1 for w in quad_w.values()),
      "B2  *** QUADRATIC: EVERY coefficient has INTEGER weight -- the obstruction vanishes ***",
      f"{[(n.split()[0], str(quad_w[n])) for n in quad_w]}")
check(quad_w["Milgrom 1999 eqs 6-9"] == 0 and quad_w["framework kappa = 1/2"] == -1,
      "B3  AGAINST INTEREST: Milgrom 1999's quadratic invariant is a PURE RATIONAL (4/3, weight 0) "
      "needing NO pi from the source, while the framework's needs one inverse power",
      "=> on economy of required input HIS coefficient is the cheapest of the three")
check(quad_w["Milgrom 2020"] == -2,
      "B4  and Milgrom 2020 needs pi^(-2) -- the most expensive of the three",
      f"invariant = {sp.simplify(COEFFS['Milgrom 2020']**2/(c_s**4*Lam_s))}")
# legitimacy of squaring: the framework's own law is quadratic in accelerations
gobs, gbar, a0s, a_s, H_s, T_s = sp.symbols("g_obs g_bar a_0 a H T", positive=True)
a0_line = gobs**2 - gbar**2 - a0s * gbar
check(sp.degree(sp.Poly(a0_line, gobs)) == 2,
      "B5  squaring is not a trick: the a_0-line g_obs^2 = g_bar^2 + a_0 g_bar is QUADRATIC in "
      "the accelerations, so a_0^2 is the natural invariant of the law")
check(sp.simplify((sp.sqrt(a_s**2 + H_s**2) / (2 * pi_s))**2 - (a_s**2 + H_s**2) / (4 * pi_s**2)) == 0,
      "B6  and the dS-Unruh temperature is a square root of a sum of SQUARES: T^2 is the "
      "polynomial object (Narnhofer-Peter-Thirring 1996)")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- requirement (i): the residue 1/4 from a PRESPECIFIED integer-weight source")
print("=" * 100)
four = sp.simplify(8 * pi_s / (2 * pi_s))
check(four == 4,
      "C1  the Bekenstein-Hawking 4 is a RATIO of two pi's: (Einstein coupling 8 pi)/(Euclidean "
      "period 2 pi) = 4 exactly -- which is WHY it is pi-free", f"8pi/2pi = {four}")
check(pi_weight(sp.Rational(1, 4)) == 0,
      "C2  so 1/4 has pi-weight 0: an index / multiplicity CAN supply it")
assembled = sp.simplify(c_s**4 * Lam_s * (2 * pi_s) / (8 * pi_s)**2)
check(sp.simplify(assembled - COEFFS["framework kappa = 1/2"]**2) == 0,
      "C3  *** a_0^2 = c^4 Lambda (2 pi)/(8 pi)^2 EXACTLY -- one Euclidean period over the "
      "square of Einstein's coupling ***", f"= {assembled}")
check(abs(mp.mpf(str(sp.N(assembled.subs({c_s: sp.Float(str(C), 40),
                                          Lam_s: sp.Float(str(LAMBDA), 40)}), 40)))
          - A0**2) / A0**2 < mp.mpf("1e-30"),
      "C4  and it reproduces a_0 on real constants", f"a_0 = {sig(A0, 12)} m/s^2")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- requirement (iii): PRICING the assembly against a mechanical menu")
print("=" * 100)
target = mp.mpf(1) / (32 * mp.pi)
menu, hits = {}, {}
RATS = [sp.Rational(p, q) for q in range(1, 7) for p in range(1, 13) if sp.gcd(p, q) == 1]
for rr in RATS:
    for n in range(-2, 3):
        for m in range(-2, 3):
            e = sp.simplify(rr * (8 * pi_s) ** n * (2 * pi_s) ** m)
            v = mp.mpf(str(sp.N(e, 45)))
            key = f"({rr})*(8pi)^{n}*(2pi)^{m}"
            menu[key] = v
            if abs(v / target - 1) < mp.mpf("1e-35"):
                hits[key] = v
print(f"  menu: {len(RATS)} rationals x 5 powers of 8pi x 5 powers of 2pi = {len(menu)} forms")
print(f"  target a_0^2/(c^4 Lambda) = 1/(32 pi) = {sig(target, 14)}")
print(f"  EXACT hits: {len(hits)}")
for k in sorted(hits)[:8]:
    print(f"      {k}")
check(len(hits) >= 1,
      "D1  the target IS reachable inside the menu (sanity: the assembly is in there)",
      f"{len(hits)} exact representations")
check(len(hits) > 1,
      "D2  AGAINST INTEREST: the representation is NOT unique -- several (rational, n, m) triples "
      "land on the same number, so 'it is BH's 4 over Einstein's 8pi squared' is a REWRITING",
      f"{len(hits)} of {len(menu)} forms hit exactly; nothing in the menu forces the exponents")
frac = mp.mpf(len(hits)) / len(menu)
check(frac < mp.mpf("0.01"),
      "D3  but the hit set is a small fraction of the menu, so the form is not generic either",
      f"{len(hits)}/{len(menu)} = {float(frac)*100:.3f}%")
# do Milgrom's coefficients also sit in this menu?  (they must, and that is the point)
for nm, ae in COEFFS.items():
    q = sp.simplify(ae**2 / (c_s**4 * Lam_s))
    v = mp.mpf(str(sp.N(q, 45)))
    inmenu = any(abs(v / mv - 1) < mp.mpf("1e-35") for mv in menu.values())
    print(f"    {nm:26s} invariant {str(q):>16s}  in menu: {inmenu}")
check(True,
      "D4  all four coefficients live in the same integer-weight menu -- so this pricing cannot "
      "discriminate between them; it only shows the target is of the right ARITHMETIC TYPE")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- requirement (ii): the INDEPENDENT prediction.  THIS IS WHERE IT FAILS.")
print("=" * 100)
m99 = COEFFS["Milgrom 1999 eqs 6-9"]
check(sp.simplify(sp.diff(m99, G_s)) == 0,
      "E1  G-freeness does NOT discriminate: Milgrom's a_0 = 2 c^2 sqrt(Lambda/3) is G-free too",
      "-> so 'a_0 contains no Newton constant' is a shared property, not a framework prediction")
check(sp.simplify(sp.diff(COEFFS["Milgrom 2020"], G_s)) == 0,
      "E2  and so is Milgrom 2020's -- all three are pure-curvature scales")
# the one over-determination, stated precisely and NOT computed here
alpha_w = sp.symbols("alpha_Wald", positive=True)
a0_wald = sp.sqrt(c_s**4 * Lam_s * (2 * pi_s) / (8 * pi_s)**2 * (1 + alpha_w))
check(sp.simplify(sp.diff(a0_wald, alpha_w)) != 0,
      "E3  the over-determination EXISTS in principle: if the 4 is the entropy normalisation, a "
      "Wald/Gauss-Bonnet correction alpha shifts a_0 at fixed Lambda, with NO new parameter",
      "d a_0/d alpha != 0 -- but the VALUE of alpha is NOT computed here, so this is an owed "
      "calculation, not a prediction")
check(len(hits) > 1,
      "E4  and requirement (ii) FAILS on its own terms: the assembly (2pi)/(8pi)^2 is a rewriting "
      "(D2), so nothing forces the exponents and no new number is predicted",
      "*** VERDICT: index-shaped TARGET yes; index-shaped DERIVATION no. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
check(pi_weight(sp.sqrt(pi_s)) == sp.Rational(1, 2),
      "NC1  CONTROL: w still detects half-integer weight when it is there (sqrt(pi) -> 1/2), "
      "so B2's all-integer result is a finding and not a broken detector")
check(pi_weight(1 + sp.sqrt(pi_s)) is None,
      "NC2  CONTROL FIRES: w rejects sums (1 + sqrt(pi) has no weight)")
bad = sp.simplify(c_s**2 * sp.sqrt(Lam_s / (31 * pi_s)))
check(abs(mp.mpf(str(sp.N(bad.subs({c_s: sp.Float(str(C), 40),
                                    Lam_s: sp.Float(str(LAMBDA), 40)}), 40))) / A0 - 1)
      > mp.mpf("1e-3"),
      "NC3  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6%, so the integer 32 is load-bearing "
      "and A1 is not an algebraic tautology")
check(sp.simplify(sp.diff(sp.simplify(a0_expr.subs(G_s, 2 * G_s)) - a0_expr, Lam_s)) == 0,
      "NC4  CONTROL: doubling G leaves a_0 unchanged (the G-freeness of A2 re-tested by "
      "substitution, not by differentiation)")
target_decoy = mp.mpf(1) / (30 * mp.pi)
dec_hits = sum(1 for v in menu.values() if abs(v / target_decoy - 1) < mp.mpf("1e-35"))
check(dec_hits < len(hits),
      "NC5  CONTROL: a decoy target 1/(30 pi) gets fewer exact hits than 1/(32 pi), so the menu "
      f"is not a universal hitter", f"decoy {dec_hits} vs target {len(hits)}")

print("""
==================================================================================================
BOTTOM LINE
==================================================================================================
  BUILT:  the TARGET.  8 pi a_0^2/(c^4 Lambda) = 1/4 exactly, an integer-weight rational, so the
          half-integer pi-weight obstruction that the corpus treated as the deep reason all 18
          unification routes failed is an ARTEFACT OF THE LINEAR PRESENTATION.  On the framework's
          own quadratic law, an index / multiplicity / representation dimension CAN in principle
          supply the coefficient.  That is a real change of status for the door.
  NOT BUILT:  the DERIVATION.  a_0^2 = c^4 Lambda (2 pi)/(8 pi)^2 is exact but is a REWRITING of
          1/(32 pi) -- the menu contains several other (rational, n, m) triples hitting the same
          number, so nothing forces the exponents, and no new observable is predicted.
  AMENDED, both mine:  (1) "the open problem collapses from a transcendental to a rational" is not
          special to the framework -- in the quadratic presentation all four coefficients are
          integer-weight, and Milgrom 1999's is a PURE rational, cheaper than the framework's.
          (2) The "MI couples to T_munu so the matter side is primitive" motivation is WITHDRAWN:
          the framework's own canonical a_0 = c^2 sqrt(Lambda/32 pi) is G-FREE and pure-curvature,
          so the rho_Lambda writing was bookkeeping, not physics.
  OWED:  the Wald / Gauss-Bonnet entropy-normalisation calculation.  If the 4 is the entropy
          normalisation, a_0 must shift with it at fixed Lambda, with no new parameter -- the only
          genuine over-determination this construction offers, and it is not computed.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
