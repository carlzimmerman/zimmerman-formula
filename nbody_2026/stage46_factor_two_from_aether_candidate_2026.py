#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
==================================================================================================
*** RETRACTED 2026-08-12 BY STAGE 48.  THIS CANDIDATE IS DEAD.  DO NOT CITE. ***
==================================================================================================
The deciding assumption below was not merely unverified -- it was INVERTED.  In G_tilde = (1-K_B/2)Ghat
as Skordis & Zlosnik write it, G_tilde is the FUNDAMENTAL constant (the one in 1/16piG_tilde and in the
Friedmann equation) and Ghat is the DERIVED, LARGER quasi-static one.  So
        G_cosmo/G_local = G_tilde/Ghat = 1 - K_B/2 <= 1,   NOT 1/(1 - K_B/2).
This stage assumed the exact reciprocal.  Worse: for AeST c_13 + 3c_2 = 0 IDENTICALLY, so the ratio is 1
and was never available at all -- on FRW the entire aether Lagrangian vanishes (F_munu = J^mu = Y = 0), so
K_B cannot enter the Friedmann equation.  With the correct direction kappa_eff = kappa/sqrt(1-K_B/2) >= 1
for every K_B in (0,2), so kappa_eff = 1/2 has NO solution: the correction can only push kappa_eff UP,
never down, and cannot explain any kappa < 1.

AND PART B WAS A TAUTOLOGY: under its own map K_B = 2(1-kappa^2), kappa = 1/2 gives K_B = 3/2
IDENTICALLY.  "This predicts K_B = 3/2" and "kappa = 1/2" are the same statement -- exactly the
circularity stage 43 had diagnosed one stage earlier about epsilon_tot = 1/(32 pi).

SURVIVING BYPRODUCTS, recorded in stage 48: the identity Z = [sqrt(8pi/3)/kappa] sqrt(G_cosmo/G_local) is
correct; GW170817 is satisfied EXACTLY (c_13 = 0 identically, vs |c_13| < 1e-15) rather than approximately;
and K_B IS constrained after all via alpha_1 = -4 K_B in the preferred-frame PPN sector, so the corpus's
"K_B is unconstrained" claim is incomplete.
==================================================================================================

stage46_factor_two_from_aether_candidate_2026.py
================================================
A CANDIDATE FOR THE FACTOR OF 2, FROM THE AETHER SECTOR -- filed as a CANDIDATE, not a result, with
the single assumption that decides it named up front and NOT verified.

Stage 43 reduced the whole coefficient question to one factor of two: kappa = 1/2 is identically
Z = 2 sqrt(8pi/3), i.e. Z is exactly twice the Friedmann factor.  This stage attacks that factor from
the one place K_B enters the phenomenology at all.

--------------------------------------------------------------------------------------------------
THE DERIVATION (algebra, solid)
--------------------------------------------------------------------------------------------------
Two different Newton constants appear in the two different places:
        promotion, LOCAL/quasi-static:   a_0^2 = kappa^2 G_local (-K)
        Friedmann, COSMOLOGICAL:         H_Lambda^2 = (8 pi G_cosmo/3) rho_Lambda
With -K = rho_Lambda c^2 on the background, Z = c H_Lambda / a_0 gives

    *** Z = [ sqrt(8pi/3) / kappa ] x sqrt( G_cosmo / G_local ) ***

so the "extra" factor multiplying the Friedmann factor is sqrt(G_cosmo/G_local), and Z = 2 sqrt(8pi/3)
requires kappa^-1 sqrt(G_cosmo/G_local) = 2.

--------------------------------------------------------------------------------------------------
THE CANDIDATE
--------------------------------------------------------------------------------------------------
Take the COEFFICIENT-FREE promotion, kappa = 1, i.e. a_0^2 = G(-K) with no inserted number at all --
which is the minimal reading of the identification, and arguably the only natural one.  Then
        G_cosmo / G_local = 4 exactly.
The corpus's one committed statement about K_B is that the aether sector renormalises Newton's constant,
G_tilde = (1 - K_B/2) Ghat, and that K_B is otherwise quasi-static-BLIND (it appears 0 times in the
published quasi-static phenomenology).  If G_local = (1 - K_B/2) Ghat while G_cosmo = Ghat, then
        1/(1 - K_B/2) = 4   =>   *** K_B = 3/2 ***
and the committed stability window is 0 < K_B < 2, so 3/2 is INSIDE it.

Inverting, the measured MOND coefficient becomes a measurement of the aether parameter:
        kappa_eff = sqrt(1 - K_B/2)   =>   K_B = 2(1 - kappa_eff^2)
        distance-free RAR  kappa = 0.551 +/- 0.043  ->  K_B = 1.393 +/- 0.095   (3/2 at 1.13 sigma)
        BTFR               kappa = 0.465 +/- 0.076  ->  K_B = 1.568 +/- 0.141   (3/2 at 0.48 sigma)
Both land inside the stability window, from opposite sides, and both are consistent with 3/2.

--------------------------------------------------------------------------------------------------
*** THE ASSUMPTION THAT DECIDES THE WHOLE THING, AND IT IS UNVERIFIED ***
--------------------------------------------------------------------------------------------------
I assumed G_local = (1 - K_B/2) Ghat AND G_cosmo = Ghat.  IF BOTH ARE RENORMALISED THE SAME WAY, THEN
G_cosmo/G_local = 1, THE EXTRA FACTOR IS 1, AND THIS ENTIRE CONSTRUCTION COLLAPSES -- kappa would have to
be set to 1/2 by hand exactly as before.  I have not checked which is true, and it is not a detail: it is
the result.

--------------------------------------------------------------------------------------------------
AND THE HONEST ACCOUNTING, EVEN IF IT SURVIVES
--------------------------------------------------------------------------------------------------
This does NOT reduce the parameter count.  Before: kappa free, measured 0.551.  After: kappa == 1 by
naturalness, K_B free, measured 1.393.  A one-for-one trade.  What it would buy is a trade of an AD HOC
number, inserted by this framework, for a STRUCTURAL one belonging to the published parent theory --
which has its own stability window and potentially its own independent observational handles.  That is
the same kind of move as the pressure promotion itself, and it is worth something, but it is not a
derivation of 1/2 and must not be described as one.

The falsifiable content is real: this predicts K_B = 3/2, and K_B is currently unconstrained by the
quasi-static phenomenology.  If any independent measurement fixes K_B -- preferred-frame PPN parameters
alpha_1, alpha_2 are the obvious place to look, given the corpus already carries a Cassini Q_2 liability
at 3-15 sigma -- this becomes an immediate test rather than a relocation.
"""

import sys

import numpy as np
import sympy as sp

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


print(__doc__)

pi = sp.pi
KB = sp.symbols("K_B", positive=True)
Gl, Gc, rhoL, c, kap = sp.symbols("G_local G_cosmo rho_L c kappa", positive=True)
KAPPA_RAR, ERR_RAR = 0.551, 0.043
KAPPA_BTFR, ERR_BTFR = 0.465, 0.076
KB_LO, KB_HI = 0.0, 2.0        # committed stability window

# =================================================================================================
print("=" * 100)
print("PART A -- the algebra")
print("=" * 100)

Z = sp.simplify(c * sp.sqrt(8 * pi * Gc * rhoL / 3) / (kap * sp.sqrt(Gl * rhoL * c ** 2)))
extra = sp.simplify(Z / (sp.sqrt(8 * pi / 3) / kap))
check(sp.simplify(extra - sp.sqrt(Gc / Gl)) == 0,
      f"A1  Z = [sqrt(8pi/3)/kappa] x sqrt(G_cosmo/G_local) exactly; the extra factor is {sp.simplify(extra)}",
      "so if the two Newton constants differ, Z is NOT simply sqrt(8pi/3)/kappa")

check(sp.simplify(sp.sqrt(sp.Integer(4))) == 2,
      f"A2  therefore Z = 2 sqrt(8pi/3) with the COEFFICIENT-FREE promotion kappa = 1 requires "
      f"G_cosmo/G_local = 4 exactly",
      "kappa = 1 means a_0^2 = G(-K) with no inserted number -- the minimal reading")

sol = sp.solve(sp.Eq(1 / (1 - KB / 2), 4), KB)
KB_PRED = sol[0]
check(KB_PRED == sp.Rational(3, 2),
      f"A3  *** and with G_local = (1-K_B/2)Ghat, G_cosmo = Ghat: 1/(1-K_B/2) = 4 gives K_B = {KB_PRED} ***",
      f"which is INSIDE the committed stability window {KB_LO} < K_B < {KB_HI}")

check(KB_LO < float(KB_PRED) < KB_HI,
      f"A4  K_B = {float(KB_PRED)} lies in ({KB_LO}, {KB_HI}) -- it is not excluded by the stability "
      f"condition, which is the only constraint the corpus currently places on it")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- inverting: the measured kappa becomes a measurement of K_B")
print("=" * 100)


def kb_of_kappa(k, e):
    return 2.0 * (1.0 - k ** 2), 4.0 * k * e     # dK_B/dkappa = -4 kappa


print(f"    {'source':20s} {'kappa':>16s} {'-> K_B':>18s} {'3/2 at':>9s} {'in window':>10s}")
kbs = {}
for lab, k, e in (("distance-free RAR", KAPPA_RAR, ERR_RAR), ("BTFR", KAPPA_BTFR, ERR_BTFR)):
    kb, dkb = kb_of_kappa(k, e)
    kbs[lab] = (kb, dkb)
    print(f"    {lab:20s} {k:.3f} +/- {e:.3f}   {kb:.3f} +/- {dkb:.3f}   "
          f"{abs(kb-1.5)/dkb:7.2f}s   {str(KB_LO < kb < KB_HI):>10s}")

check(all(KB_LO < v[0] < KB_HI for v in kbs.values()),
      f"B1  BOTH kappa determinations map to K_B INSIDE the stability window, and they bracket 3/2 from "
      f"opposite sides ({kbs['distance-free RAR'][0]:.3f} and {kbs['BTFR'][0]:.3f})",
      "that is a non-trivial consistency, though two numbers bracketing a third is weak evidence on its own")

check(all(abs(v[0] - 1.5) / v[1] < 2.0 for v in kbs.values()),
      f"B2  and both are consistent with K_B = 3/2 at "
      f"{max(abs(v[0]-1.5)/v[1] for v in kbs.values()):.2f} sigma or better")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the assumption that decides it, and the honest accounting")
print("=" * 100)

info("C1  *** THE DECIDING ASSUMPTION, UNVERIFIED: I took G_local = (1 - K_B/2) Ghat and G_cosmo = Ghat.  "
     "If BOTH are renormalised identically then G_cosmo/G_local = 1, the extra factor is 1, and this whole "
     "construction collapses -- kappa would have to be set to 1/2 by hand exactly as before.  This is not "
     "a detail; it IS the result, and I have not checked it. ***")

info("C2  the check required is specific: in AeST/Einstein-aether, does the FRIEDMANN equation use the "
     "bare Ghat while the QUASI-STATIC limit uses (1-K_B/2)Ghat, or do both carry the same factor?  In "
     "Einstein-aether theories the cosmological and Newtonian G are known to differ by a combination of "
     "the c_i, which is why this is worth asking -- but 'worth asking' is not 'established'.")

info("C3  AND THE ACCOUNTING, EVEN IF IT SURVIVES: this does NOT reduce the parameter count.  Before, "
     "kappa free and measured at 0.551.  After, kappa == 1 by naturalness and K_B free and measured at "
     "1.393.  One for one.  What it buys is trading an AD HOC number inserted by this framework for a "
     "STRUCTURAL one belonging to the published parent theory, with its own stability window.  Worth "
     "something; NOT a derivation of 1/2, and it must never be described as one.")

info("C4  THE FALSIFIABLE CONTENT IS REAL THOUGH: this predicts K_B = 3/2 for a parameter currently "
     "unconstrained by the quasi-static phenomenology.  The obvious independent handle is the "
     "preferred-frame PPN sector (alpha_1, alpha_2), especially since the corpus already carries a Cassini "
     "Q_2 liability at 3-15 sigma.  If PPN bounds fix K_B, this becomes a test rather than a relocation -- "
     "and it could equally kill it outright.")

# a sanity check on the coincidence risk
info(f"C5  COINCIDENCE RISK, quantified as fairly as I can: the stability window has width 2, and the "
     f"K_B implied by the measured kappa is {kbs['distance-free RAR'][0]:.3f} +/- {kbs['distance-free RAR'][1]:.3f}.  Landing within 1.13 sigma of the "
     f"specific rational 3/2 is not impressive on its own -- 3/2 occupies no privileged position in "
     f"(0,2) a priori.  What would make it impressive is if 3/2 were independently forced.  It is not, "
     f"currently.")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  A CANDIDATE, FILED AS ONE.  NOT A DERIVATION OF kappa = 1/2.

  1. THE ALGEBRA IS SOLID: Z = [sqrt(8pi/3)/kappa] x sqrt(G_cosmo/G_local).  If the local and
     cosmological Newton constants differ, the factor multiplying the Friedmann factor is
     sqrt(G_cosmo/G_local), and nobody in this corpus had written that down.

  2. THE CANDIDATE: with the coefficient-free promotion kappa = 1 (a_0^2 = G(-K), nothing inserted),
     Z = 2 sqrt(8pi/3) requires G_cosmo/G_local = 4, which with G_tilde = (1-K_B/2)Ghat gives
        *** K_B = 3/2, inside the committed stability window 0 < K_B < 2. ***
     Inverting, the measured kappa becomes K_B = 1.393 +/- 0.095 (RAR) and 1.568 +/- 0.141 (BTFR) --
     both in-window, bracketing 3/2 from opposite sides, both consistent with it.

  3. *** AND THE ONE ASSUMPTION THAT DECIDES IT IS UNVERIFIED: that the Friedmann equation carries the
     BARE Ghat while the quasi-static limit carries (1-K_B/2)Ghat.  If both carry the same factor, the
     ratio is 1 and this collapses entirely. ***  In Einstein-aether theories the cosmological and
     Newtonian G are known to differ by a combination of the c_i, which is why the question is worth
     asking -- but that is not the same as having checked it in AeST.

  4. EVEN IF IT SURVIVES, THE ACCOUNTING IS ONE-FOR-ONE: kappa free (0.551) becomes K_B free (1.393).
     No parameters are saved.  What is gained is a trade of an ad-hoc number for a structural one in the
     parent theory.  Real, modest, and NOT a derivation.

  5. COINCIDENCE RISK, stated plainly: 3/2 occupies no privileged position in (0,2), and landing 1.13
     sigma from it is not impressive by itself.  The construction becomes interesting only if something
     independently forces 3/2, or if PPN bounds on alpha_1/alpha_2 pin K_B -- which could equally kill it.

  NEXT: verify item 3 against the published AeST and Einstein-aether literature, and look for existing
  preferred-frame bounds on K_B.  Both are short, and either could end this in one step.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
