#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage47_ds_entropy_mechanism_2026.py
====================================
SEPARATING TWO CLAIMS STAGE 43 WRONGLY COLLAPSED.  Killing "kappa^2 = 8 pi epsilon_tot" as circular was
correct; discarding the de Sitter-entropy mechanism packaged with it was not.  The mechanism survives,
and it answers a question about this framework that nobody asks.

Carl pointed out that a route had been thrown away along the way.  He was right.

--------------------------------------------------------------------------------------------------
THE IDENTITY: TRIVIAL
--------------------------------------------------------------------------------------------------
        r_H = c/H,   A = 4 pi c^2/H^2,   S_dS = k_B A c^3 / (4 G hbar) = pi k_B c^5 / (G hbar H^2)
        =>  S_dS x G H^2 = pi k_B c^5 / hbar  =  pi   in natural units.
So "S_dS G H^2 = pi" is an EXACT IDENTITY and a trivial one -- it is S = A/4G rewritten with
A = 4 pi/H^2.  It is not a coincidence, not new physics, and carries no information by itself.

--------------------------------------------------------------------------------------------------
THE CONSEQUENCE: NOT TRIVIAL, AND THIS IS WHAT WAS DISCARDED
--------------------------------------------------------------------------------------------------
        *** G x S_dS = pi k_B c^5 / (hbar H^2)  =  pi/H^2  in natural units.  THE G CANCELS. ***
Any effect suppressed by ONE power of G and weighted by the de Sitter entropy is PLANCK-FREE and lands
purely at the Hubble scale.  That is a real answer to a question this corpus has never asked:

        why is a_0 ~ 1e-10 m/s^2 AT ALL, rather than Planckian?

The gap to bridge is enormous -- the Planck acceleration c^2/l_P is ~6e61 times a_0 -- and G x S_dS
bridges it exactly, by cancelling G rather than by tuning anything.

--------------------------------------------------------------------------------------------------
WHAT THIS DOES AND DOES NOT BUY, stated separately because stage 43 conflated them
--------------------------------------------------------------------------------------------------
  (1) AS A DERIVATION OF kappa: still circular.  Stage 43 stands unchanged -- kappa^2 = 8 pi epsilon
      solved for epsilon returns 1/32pi, with the 8 pi carried over from the formula's own left side and
      the 4 in 32 pi equal to 1/kappa^2.  The mechanism cannot supply Z = 5.78881.
  (2) AS A MECHANISM FOR THE SCALE: SURVIVES, and is the stronger of the two claims.
  (3) NOVELTY: LOW, and this must be said plainly.  This is the standard de Sitter-entropy argument
      already used by entropic-gravity and holographic dark-energy work (Verlinde, Padmanabhan, Li).
      The identity is textbook.  What is specific here is only that this framework's a_0 is tied to
      rho_Lambda by an action-level identification rather than by an entropic argument.
  (4) SO THE HONEST STATUS is: the framework has a candidate answer for WHY the scale is cosmological
      rather than Planckian, borrowed from known reasoning, and no answer for the coefficient.

--------------------------------------------------------------------------------------------------
AND A SECOND OBSERVATION, RECORDED BECAUSE IT WAS ALSO GLOSSED
--------------------------------------------------------------------------------------------------
Stage 45 found the only kernel surviving the solar system is the exponential
nu(y) = [1 - e^(-sqrt y)]^(-1).  Its approach to Newtonian is e^(-sqrt(g/a_0)) -- i.e. e^(-S) with
S ~ sqrt(y).  An action exponential in a square root is the signature of a NON-PERTURBATIVE effect
(instanton / tunnelling), not of a perturbative expansion.  Power-law kernels FAIL the solar system and
the non-perturbative one PASSES.  That was reported as a bookkeeping fix; it may be structural.  Flagged
as an observation only -- no derivation is attempted here and none is claimed.
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
    return True


print(__doc__)

# --- constants.  NOTE: H_Lambda = H_0 sqrt(Omega_Lambda), NOT H_0.  A first draft of this stage used
# --- H_0 here and printed Z = 7.02 instead of the committed 5.78881; corrected before commit.
C = 2.99792458e8
HBAR = 1.054571817e-34
KB = 1.380649e-23
G = 6.67430e-11
L_PLANCK = 1.616255e-35
H0 = 67.4 * 1e3 / 3.0856775814913673e22       # s^-1
OM_L = 0.685
H_LAM = H0 * np.sqrt(OM_L)                     # s^-1
A0 = 9.3619e-11
A0_ALT = 1.1279e-10
Z_COMMITTED = float(sp.sqrt(32 * sp.pi / 3))

print("=" * 100)
print("PART A -- the identity")
print("=" * 100)

Gs, Hs, cs, hs, ks = sp.symbols("G H c hbar k_B", positive=True)
S_dS = sp.simplify(ks * (4 * sp.pi * (cs / Hs) ** 2) * cs ** 3 / (4 * Gs * hs))
check(sp.simplify(S_dS - sp.pi * ks * cs ** 5 / (Gs * hs * Hs ** 2)) == 0,
      f"A1  S_dS = k_B A c^3/(4 G hbar) with A = 4 pi c^2/H^2 gives S_dS = {S_dS}")

prod = sp.simplify(S_dS * Gs * Hs ** 2)
check(sp.simplify(prod.subs({ks: 1, cs: 1, hs: 1}) - sp.pi) == 0,
      f"A2  S_dS x G H^2 = {prod} = pi in natural units -- an EXACT but TRIVIAL identity, being S = A/4G "
      f"rewritten with A = 4 pi/H^2.  Not a coincidence, and carries no information alone")

print()
print("=" * 100)
print("PART B -- the consequence, which is what was discarded")
print("=" * 100)

GS = sp.simplify(Gs * S_dS)
check(sp.simplify(GS.subs({ks: 1, cs: 1, hs: 1}) - sp.pi / Hs ** 2) == 0,
      f"B1  *** G x S_dS = {GS} = pi/H^2 in natural units.  THE G CANCELS IDENTICALLY. ***  So any effect "
      f"suppressed by one power of G and weighted by the de Sitter entropy is PLANCK-FREE and sits at the "
      f"Hubble scale",
      "this is the mechanism, and it is separable from the failed coefficient derivation")

a_planck = C ** 2 / L_PLANCK
gap = a_planck / A0
check(gap > 1e60,
      f"B2  and the gap it has to bridge is real: the Planck acceleration c^2/l_P = {a_planck:.3e} m/s^2 is "
      f"{gap:.1e}x a_0.  The G-cancellation bridges it by structure, not by tuning",
      f"alt footing: {a_planck/A0_ALT:.1e}x")

cH = C * H_LAM
Z_obs = cH / A0
check(abs(Z_obs - Z_COMMITTED) / Z_COMMITTED < 0.05,
      f"B3  SANITY CHECK on the scale the mechanism delivers: c H_Lambda = {cH:.4e} m/s^2 with "
      f"H_Lambda = H_0 sqrt(Omega_L) = {H_LAM:.4e} s^-1, so c H_Lambda / a_0 = {Z_obs:.4f} against the committed "
      f"Z = {Z_COMMITTED:.4f} -- agreeing to {100*abs(Z_obs-Z_COMMITTED)/Z_COMMITTED:.1f}%",
      "a first draft of this stage used H_0 in place of H_Lambda and printed 7.02; corrected before commit")

print()
print("=" * 100)
print("PART C -- what it buys, and what it does not")
print("=" * 100)

info("C1  AS A DERIVATION OF kappa: STILL CIRCULAR.  Stage 43 stands.  kappa^2 = 8 pi epsilon solved for "
     "epsilon returns 1/32 pi; the 8 pi is carried over from the formula's own left-hand side and the 4 in "
     "32 pi is 1/kappa^2.  The mechanism cannot supply Z = 5.78881, and nothing here changes that.")

info("C2  AS A MECHANISM FOR THE SCALE: SURVIVES, and it is the stronger claim of the two.  It answers "
     "why a_0 is cosmological rather than Planckian -- a question this corpus had never posed.")

info("C3  *** NOVELTY: LOW, and this must be stated plainly.  G x S_dS = pi/H^2 is the standard de Sitter-"
     "entropy argument already used by entropic-gravity and holographic dark-energy work (Verlinde, "
     "Padmanabhan, Li).  The identity is textbook.  What is specific to this framework is only that its "
     "a_0 is tied to rho_Lambda by an ACTION-LEVEL identification rather than by an entropic argument. ***")

info("C4  SECOND OBSERVATION, also previously glossed: the only kernel surviving the solar system is "
     "nu(y) = [1 - e^(-sqrt y)]^(-1), whose approach to Newtonian is e^(-sqrt(g/a_0)) = e^(-S) with "
     "S ~ sqrt(y).  An action exponential in a square root is the signature of a NON-PERTURBATIVE effect, "
     "not a perturbative expansion -- and the power-law kernels are exactly the ones that FAIL the solar "
     "system.  Recorded as an observation.  No derivation attempted, none claimed.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  STAGE 43 KILLED TWO CLAIMS WHEN IT SHOULD HAVE KILLED ONE.

  KILLED, correctly, and still dead: kappa^2 = 8 pi epsilon_tot as a derivation of the coefficient.  It is
  a solve, not a derivation, and Z = {Z_COMMITTED:.5f} is precisely what it cannot supply.

  WRONGLY DISCARDED, and reinstated here: the de Sitter-entropy mechanism.  G x S_dS = pi/H^2 exactly, so
  the G cancels and any single-power-of-G effect weighted by the horizon entropy is PLANCK-FREE.  That
  bridges the {gap:.0e} between the Planck acceleration and a_0 structurally rather than by tuning, and it
  answers a question the corpus had never asked: why is the MOND scale cosmological at all?

  BUT ITS NOVELTY IS LOW.  This is the standard horizon-entropy argument from entropic gravity and
  holographic dark energy.  The identity is textbook.  It should be cited as context for why a_0 is
  cosmological, NOT advertised as a result.

  AND A SECOND THING WAS GLOSSED: the surviving kernel's e^(-sqrt(y)) tail is the form of a
  NON-PERTURBATIVE amplitude, and the power-law kernels are the ones that fail the solar system.  That may
  be structural.  Flagged, not claimed.

  NET: the framework now has a borrowed-but-real answer for the SCALE, no answer for the COEFFICIENT, and
  one unexamined structural hint in the kernel's functional form.
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
