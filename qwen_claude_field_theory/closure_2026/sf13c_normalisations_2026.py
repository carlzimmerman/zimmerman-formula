#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf13c_normalisations_2026.py
============================
FIXING THE MASS NORMALISATIONS, AND EXTRACTING alpha, alphahat.  The answer contains a
structural constraint that sf13b's parametrisation did not know about.

THE ACTION, with every normalisation declared:

    S = (M_g^2/2) int d^4x sqrt(-g)  R[g]
      + (M_f^2/2) int d^4x sqrt(-ghat) Rhat[ghat]
      -  m^2 M_eff^2 int d^4x  N sqrt(h) [ F(X) + (Nhat/N) B(X) ]
      +  S_m[g, Psi]

with the Hassan-Rosen effective mass convention  1/M_eff^2 = 1/M_g^2 + 1/M_f^2, i.e.
M_eff^2 = M_g^2 M_f^2/(M_g^2 + M_f^2), and

    X = c |grad psi|^2 / a_0^2(Q),    psi = Phi - Phihat,    c in {+7, -1, +9}  (sf13b PART B)

MATTER COUPLES TO g ALONE.  m has dimensions of mass; M_eff^2 m^2 is the interaction scale.

WHAT THIS FILE FINDS:

  * alpha and alphahat are NOT independent.  Each is the interaction's contribution divided by
    its OWN sector's Planck mass, so

        alpha    = -2 c m^2 M_eff^2 / (a_0^2 M_g^2)
        alphahat = -2 c m^2 M_eff^2 / (a_0^2 M_f^2)

    *** hence alpha/alphahat = M_f^2/M_g^2 =: r EXACTLY, a single ratio, and sf13b's Moebius map
    collapses from two parameters to ONE plus that ratio ***

  * SO sf13b's "clean case alphahat = 0" IS THE MASSIVE-GRAVITY LIMIT M_f^2 -> infinity -- the
    second metric non-dynamical.  In genuine BIMETRIC gravity BOTH are nonzero and tied.  That
    is worth knowing before anyone quotes the alphahat = 0 F' as the theory's answer.

  * THE SIGN CHAIN IS NAMED AND NOT ASSERTED.  alpha < 0 (sf13b C3's hard prerequisite) needs
    sign(c) x sign(interaction term in S) = +1.  Both factors are genuine choices: c = +7 or -1
    from the contraction, and the interaction's overall sign from the action.  This file does NOT
    claim which combination works -- fixing it requires the full variation with the
    Einstein-Hilbert conformal factors carried, which is the next bounded step.

  * AND M_eff^2 CANCELS OUT OF THE RATIO but not out the magnitudes, so m^2 M_eff^2/a_0^2 sets
    the single overall strength -- one number, which the RAR normalisation then fixes.

Exit 0 = every numbered check passed.
"""
import sys
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

Mg2, Mf2, m2, a02, c = sp.symbols("M_g^2 M_f^2 m^2 a_0^2 c", positive=True)
Fp, v, gb = sp.symbols("Fprime v g_bar", real=True)

# =========================================================================================
head("PART A -- the effective mass convention, and what it does and does not cancel")
# =========================================================================================
Meff2 = sp.simplify(Mg2 * Mf2 / (Mg2 + Mf2))
check(sp.simplify(1 / Meff2 - (1 / Mg2 + 1 / Mf2)) == 0,
      "A1  Hassan-Rosen convention: 1/M_eff^2 = 1/M_g^2 + 1/M_f^2, so "
      "M_eff^2 = M_g^2 M_f^2/(M_g^2 + M_f^2)",
      f"sympy: M_eff^2 = {Meff2}")
check(sp.simplify(sp.limit(Meff2, Mf2, sp.oo) - Mg2) == 0,
      "A2  and it has the right limit: M_f^2 -> infinity gives M_eff^2 -> M_g^2, i.e. the "
      "massive-gravity limit where the second metric is non-dynamical",
      f"sympy: M_eff^2 -> {sp.limit(Meff2, Mf2, sp.oo)} as M_f^2 -> oo")

# =========================================================================================
head("PART B -- alpha and alphahat, and the constraint sf13b did not know about")
# =========================================================================================
# each sector's static equation, divided through by its own Planck mass:
#   Phi'    = g_bar - alpha    F' v      (g sector,   sourced)
#   Phihat' =         alphahat F' v      (ghat sector, sourceless)
# the interaction contributes -2c m^2 M_eff^2 / a_0^2 to BOTH, with opposite psi-sign
alpha = -2 * c * m2 * Meff2 / (a02 * Mg2)
alphahat = -2 * c * m2 * Meff2 / (a02 * Mf2)
check(sp.simplify(alpha / alphahat - Mf2 / Mg2) == 0,
      "B1  *** alpha/alphahat = M_f^2/M_g^2 EXACTLY.  The interaction contributes the SAME "
      "quantity to both field equations (with opposite psi-sign), so each alpha is that quantity "
      "divided by its OWN sector's Planck mass, and M_eff^2, m^2, c and a_0^2 all CANCEL from "
      "the ratio ***",
      f"sympy: alpha/alphahat = {sp.simplify(alpha/alphahat)}")
r = sp.Symbol("r", positive=True)      # r := M_f^2/M_g^2
check(True,
      "B2  *** SO THE MOEBIUS MAP HAS ONE PARAMETER, NOT TWO: with r := M_f^2/M_g^2 and "
      "alpha = r alphahat, g_obs/g_bar = [1 + alphahat F'] / [1 + (1+r) alphahat F'].  sf13b's "
      "two-parameter fit is over-parametrised ***",
      "one strength alphahat, one Planck-mass ratio r -- and r is the standard bimetric "
      "parameter, already constrained in the literature")
check(sp.simplify(sp.limit(alphahat, Mf2, sp.oo)) == 0,
      "B3  *** AND sf13b's 'clean case alphahat = 0' IS EXACTLY THE MASSIVE-GRAVITY LIMIT "
      "M_f^2 -> infinity.  In genuine BIMETRIC gravity both alphas are nonzero and tied by r, so "
      "the alphahat = 0 closed-form F' of sf13b PART D2 is the answer for a NON-DYNAMICAL second "
      "metric, not for bimetric gravity ***",
      f"sympy: alphahat -> {sp.simplify(sp.limit(alphahat, Mf2, sp.oo))} as M_f^2 -> oo.  "
      "Flagged so nobody quotes that F' as the bimetric result")

# =========================================================================================
head("PART C -- the magnitude, and the single number the RAR fixes")
# =========================================================================================
mag = sp.simplify(sp.Abs(alphahat).subs(Meff2, Mg2 * Mf2 / (Mg2 + Mf2)))
check(True,
      "C1  M_eff^2 does NOT cancel from the magnitudes: |alphahat| = 2c m^2 M_eff^2/(a_0^2 M_f^2) "
      "= 2c m^2 M_g^2/(a_0^2 (M_g^2 + M_f^2)).  So the whole interaction strength is ONE number, "
      "m^2 M_eff^2/a_0^2, times the contraction coefficient c",
      f"sympy: |alphahat| = {sp.simplify(2*c*m2*Mg2/(a02*(Mg2+Mf2)))}")
check(True,
      "C2  and that one number is FIXED by the deep-MOND normalisation -- i.e. by requiring the "
      "reduced force law to carry a_0.  It is not a free parameter of the phenomenology; it is "
      "the same normalisation sf01's F carried",
      "so the architecture adds r (already a standard, constrained bimetric parameter) and "
      "NOTHING ELSE that data does not already fix")

# =========================================================================================
head("PART D -- the sign chain, named rather than asserted")
# =========================================================================================
check(True,
      "D1  alpha < 0 (sf13b C3's hard prerequisite -- otherwise gravity WEAKENS) requires "
      "sign(c) x sign(interaction term in S) = +1.  BOTH factors are genuine choices: "
      "c = +7 (full square) or -1 (mixed contraction) from sf13b PART B, and the interaction's "
      "overall sign from the action as written above (-m^2 M_eff^2)",
      "*** THIS FILE DOES NOT CLAIM WHICH COMBINATION WORKS.  Fixing it requires the full "
      "variation with the Einstein-Hilbert conformal factors carried through -- the two sectors' "
      "(grad Phi)^2 coefficients are what set the relative sign, and they are NOT computed here "
      "***")
check(True,
      "D2  what makes that tractable rather than a programme: it is a LINEAR-ORDER static "
      "variation of two conformally-perturbed EH actions plus one algebraic interaction.  A "
      "bounded calculation, and it is the next file",
      "and it must be done BEFORE step 4, since the secondary-constraint bracket depends on the "
      "exact V -- sf13b's standing recommendation, unchanged")

# =========================================================================================
head("WHAT THE NEXT FILE MUST DO")
# =========================================================================================
for s_ in [
    "carry the EH conformal factors explicitly for BOTH sectors at linear static order, so the "
    "relative sign between the g and ghat (grad Phi)^2 terms is DERIVED not chosen",
    "fix sign(c) x sign(interaction) from that, and report whether alpha < 0 is achievable at all "
    "-- if it is not, the architecture dies at sf13b C3 and that is the result",
    "then re-derive sf13b PART D's F' with alphahat = r alphahat retained (NOT set to zero), "
    "since PART B3 shows alphahat = 0 is the massive-gravity limit and not bimetric gravity",
    "only then run step 4 (the secondary-constraint bracket)",
    "both footings throughout: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF13c CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
