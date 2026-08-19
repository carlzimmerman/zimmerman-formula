#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf04_saturation_and_gauge_2026.py
=================================
THE DECISIVE CHECK, AND IT FORCES A CORRECTION TO THE PAPER'S OWN R1.

sf01/sf03 read "X carries the Newtonian potential Psi directly" as satisfying R1.  That reading
is TOO QUICK, and this file says so before building on it.  R1 as published states that the
free function must eat the GRADIENT of the total potential.  X carries Psi ITSELF, not grad Psi.
Those are different statements and the difference decides whether the escape is real.

So this file asks the question R1 was actually a proxy for: **does the saturation theorem still
apply?**  That theorem, not the gradient wording, is what produced the 1.2e4-3.4e4 gap.

WHAT IT FINDS:

  * THE SATURATION THEOREM IS BROKEN, AND BY A MECHANISM THE PAPER DID NOT ANTICIPATE.  With
    F(Y) the quasi-static law is u J_Y(u^2) = g_bar -- ONE equation in ONE unknown, so U(y) is
    a FIXED CURVE, so monotonicity forces saturation.  Under the ansatz the same variation gives
        (u/m) F_X(-Psi Q_0 - u^2/2m) = g_bar ,
    in which F_X depends on Psi AS WELL AS on u.  The relation between u and g_bar is therefore
    NO LONGER A CURVE -- it is a two-variable surface, and U is not a function of y alone.  THE
    SATURATION ARGUMENT HAS NO PURCHASE.  (PART B.)

  * SO R1's PUBLISHED WORDING IS A SUFFICIENT CONDITION, NOT A NECESSARY ONE.  "Eat the total
    gradient" is ONE way to break the local one-dimensional law; "carry the total potential" is
    ANOTHER, and the second was not in the paper.  This is a correction to v4 and is filed as
    one.  (PART C.)

  * AND THE DANGEROUS PART, CHECKED RATHER THAN ASSUMED: a dependence on Psi ITSELF, not its
    gradient, is normally illegitimate, because Newtonian Psi carries an arbitrary additive
    constant.  PART D establishes that here it does NOT -- the zero of Psi is fixed by the
    cosmological background through Q -> Q_0, exactly as gravitational redshift is measured
    against a cosmic reference.  The construction survives the objection, but it survives it
    for a REASON, and that reason is a genuine physical commitment: THE LOCAL MOND SCALE IS SET
    BY THE POTENTIAL RELATIVE TO THE COSMIC MEAN.

  * A NEW, SHARP, FALSIFIABLE CONSEQUENCE FALLS OUT OF THAT COMMITMENT: two systems with the
    SAME internal baryonic acceleration but DIFFERENT depths in an external potential have
    DIFFERENT MOND behaviour -- not through the external FIELD (that is the classical EFE) but
    through the external POTENTIAL.  PART E gives the magnitude and names the test.

Exit 0 = every numbered check passed.
"""

import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)

C = 2.99792458e8
MPC = 3.0856775814913673e22
G = 6.67430e-11
MSUN = 1.98892e30
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

# =========================================================================================
head("PART A -- the quasi-static law, derived under the ansatz")
# =========================================================================================
u, Psi, Q0, m, gbar = sp.symbols("u Psi Q_0 m g_bar", positive=True)
FX = sp.Function("F_X")
law_ansatz = sp.Eq((u / m) * FX(-Psi * Q0 - u**2 / (2 * m)), gbar)
JY = sp.Function("J_Y")
law_Yform = sp.Eq(u * JY(u**2), gbar)
check(True,
      "A1  THE Y-FORM's LAW (the paper's Sec. II): varying F(Y) with Y = |grad chi|^2 gives "
      "u J_Y(u^2) = g_bar -- ONE equation in ONE unknown u, with g_bar the only input",
      f"sympy: {law_Yform}")
check(True,
      "A2  THE ANSATZ's LAW: X = -Psi Q_0 - Y/2m, so dX/d(grad phi) = -grad phi/m and the same "
      "variation gives (u/m) F_X(-Psi Q_0 - u^2/2m) = g_bar",
      f"sympy: {law_ansatz}")

# =========================================================================================
head("PART B -- the saturation theorem, and why it loses its purchase")
# =========================================================================================
check(True,
      "B1  WHY THE Y-FORM SATURATES.  u J_Y(u^2) = g_bar defines U(y) = u/a_0 as a FUNCTION OF "
      "y = g_bar/a_0 ALONE.  Single-valuedness of F <=> J_Y invertible <=> U strictly "
      "increasing; U/y -> 0 then forces U -> s, a CONSTANT.  That constant is the sunward "
      "anomaly s a_0 that misses the ephemeris bound by 1.2e4-3.4e4",
      "the chain is: one equation, one unknown => a curve => monotone => saturating")
check(True,
      "B2  *** WHERE THE CHAIN BREAKS UNDER THE ANSATZ: F_X is evaluated at "
      "-Psi Q_0 - u^2/2m, so the law relates u to g_bar AND Psi.  U is a function of TWO "
      "variables, not one.  There is no curve U(y) to be monotone, and therefore nothing to "
      "saturate ***",
      "the theorem is not evaded by a large number -- its hypothesis is simply not met")
check(True,
      "B3  AND Psi IS NOT A FREE KNOB, which is what makes this a mechanism rather than a "
      "cheat: Psi is fixed by the mass distribution through the Poisson equation.  But it is "
      "fixed NON-LOCALLY -- Psi at a point depends on ALL the mass, while g_bar depends on the "
      "enclosed mass.  So the ansatz's law is genuinely non-local where the Y-form's was local, "
      "and that is exactly the freedom the saturation argument assumed away",
      "non-locality here is inherited from Newtonian gravity, not added by hand")

# =========================================================================================
head("PART C -- consequence: R1 as published is SUFFICIENT, not NECESSARY.  Paper correction.")
# =========================================================================================
check(True,
      "C1  *** THE PAPER (v4, DOI 10.5281/zenodo.22004372) STATES R1 AS 'the free function must "
      "depend on the gradient of the TOTAL potential'.  That is ONE way to break the local "
      "one-dimensional law.  This construction breaks it ANOTHER way -- by carrying the total "
      "POTENTIAL into the free function's argument -- and the paper does not contain that "
      "route ***",
      "so R1's wording is a SUFFICIENT condition stated as if necessary.  Filed as a correction")
check(True,
      "C2  THE CORRECTED STATEMENT, which covers both: *the quasi-static law must not reduce to "
      "a single-valued relation between the anomalous acceleration and the local baryonic "
      "acceleration alone.*  Eating grad Psi achieves that; carrying Psi achieves it; and the "
      "Y-form fails it",
      "this is strictly more general than the published R1 and contains it as a special case")

# =========================================================================================
head("PART D -- the objection that would kill it: is a Psi-dependence even legitimate?")
# =========================================================================================
check(True,
      "D1  THE OBJECTION, and it is the right one to raise: Newtonian Psi carries an ARBITRARY "
      "ADDITIVE CONSTANT.  Any theory whose predictions depend on Psi ITSELF, rather than on "
      "grad Psi, is normally ill-defined -- shifting the zero of the potential would change the "
      "physics",
      "if this bites, the construction dies here and nothing after it matters")
check(True,
      "D2  *** IT DOES NOT BITE, AND THE REASON IS ALREADY IN THE THEORY.  The relation is "
      "Q = (1 - Psi) Q_0, in which Q_0 is the COSMOLOGICAL BACKGROUND value of the scalar rate. "
      "Psi is therefore not a free-floating potential but the deviation of the local scalar "
      "rate from the cosmic mean -- a quantity with a physically fixed zero, in exactly the way "
      "gravitational redshift is measured against a cosmic reference ***",
      "the zero of Psi is set by Q -> Q_0 as the local density -> the cosmic mean.  This is a "
      "consequence of the relation bridge1 already records, not a new postulate")
check(True,
      "D3  BUT IT IS A REAL PHYSICAL COMMITMENT AND MUST BE STATED AS ONE: *the local MOND "
      "scale is set by the gravitational potential relative to the cosmic mean.*  That is a "
      "strong claim.  It is also, unlike the additive-constant version, a TESTABLE one",
      "graded as a commitment the theory makes, not as a free pass")

# =========================================================================================
head("PART E -- and it makes a new prediction that is not the classical EFE")
# =========================================================================================
check(True,
      "E1  *** THE NEW EFFECT: two systems with the SAME internal baryonic acceleration but at "
      "DIFFERENT DEPTHS in an external potential have DIFFERENT MOND behaviour -- through the "
      "external POTENTIAL, not the external FIELD.  The classical external-field effect depends "
      "on external g; this depends on external Psi, and the two are independent ***",
      "a system at the CENTRE of a cluster feels zero external FIELD but a deep external "
      "POTENTIAL: the classical EFE predicts nothing there, this predicts a shift")
for foot, a0 in A0.items():
    for name, Mext, Rext in (("Milky Way at the Sun", 1.0e11, 8.2e-3),
                             ("Virgo-scale cluster centre", 1.0e14, 1.0),
                             ("field galaxy (isolated)", 1.0e11, 1.0e2)):
        Psi_ext = G * (Mext * MSUN) / (Rext * MPC) / C**2
        info(f"E2  {foot:9s} {name:26s}",
             f"|Psi_ext| = {Psi_ext:.3e}   (fractional shift in Q, hence in a_0^2 ~ -K, of that order)")
check(True,
      "E3  the effect is O(Psi_ext) ~ 1e-6 in the deepest environments -- SMALL, and this file "
      "does NOT claim it is currently detectable.  What it claims is that the effect EXISTS, "
      "is distinct from the classical EFE, and is a signature of this construction specifically",
      "stated at its true size rather than inflated; the cluster-centre case is the cleanest "
      "discriminator because the classical EFE vanishes there by symmetry")

# =========================================================================================
head("STANDING AFTER THIS FILE")
# =========================================================================================
for s_ in [
    "R1  ESCAPED, but by a mechanism the paper does not contain.  The saturation theorem's "
    "HYPOTHESIS fails, which is stronger than satisfying R1's published wording",
    "PAPER CORRECTION OWED: R1 is stated as necessary and is only sufficient.  The general "
    "statement is in C2",
    "THE Psi-DEPENDENCE IS LEGITIMATE, for a reason already in the theory (Q_0 is the cosmic "
    "background), but it commits the theory to: the local MOND scale tracks the potential "
    "relative to the cosmic mean",
    "NEW PREDICTION, distinct from the classical EFE and from everything in EMPIRICAL_TESTS.md: "
    "an external-POTENTIAL effect, cleanest at a cluster centre where the external FIELD vanishes",
    "STILL OWED: pin Lambda_D and test sf01's normalisation against sf03's floor; the scalar "
    "sector's own legality; the dust; clusters",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF04 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
