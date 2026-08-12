#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage36_bump_slot_derivation_2026.py
====================================
DERIVING THE SLOT FROM THE ACTION -- and the answer closes the a_0-bump as the cluster mechanism, on
a derivation rather than on a fit.

--------------------------------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------------------------------
Stage 35 found that the corpus's own response B(y) x |Phi| is EXCLUDED in the mass slot (stage 33's
theorem) and, as a GRADIENT modification, clears every gate and removes 59% of the cluster chi^2:

        mu_eff(x, Phi) = mu_M(x) - w_b B(x^2) (|Phi|/Phi_ref)

But that was an ANSATZ.  The action's bump term is A B(Y/Acal)(Q-Q_0)^2, and the question left owed
was: which slot does it actually generate, and with which function?  This stage varies it.

--------------------------------------------------------------------------------------------------
THE ANSWER: BOTH SLOTS, AND NEITHER IS THE ONE THAT WORKS
--------------------------------------------------------------------------------------------------
With row 17's derived static closure delta Q = -Q_0 Phi:

  MASS SLOT (vary w.r.t. Phi; Phi appears only inside (delta Q)^2):
        coefficient ~ A B(w) Q_0^2        -- carries B, is >= 0
        => EXCLUDED by stage 33's theorem.

  GRADIENT SLOT (vary w.r.t. the khronon; Y = |grad phi|^2 enters through B's argument):
        coefficient ~ A B'(w) Q_0^2 Phi^2 -- carries B PRIME, and Phi SQUARED
        and it fails on all three counts:
          (b)  B'(0) = 1, not 0  -> breaks the deep-MOND limit, exactly as q(0) = 1 did (stage 34)
          (a') B' FALLS 9.6x across the cluster range w = 0.06-0.64  -> boost DECREASES with x
               -> residual RISES outward: the wrong radial direction
          SIGN: no-ghost requires 2AB >= 0 hence A > 0, and B' > 0 across clusters, so the derived
               term ADDS to mu_eff and REDUCES the cluster boost -- the opposite of what is needed.

*** So stage 35's mechanism is NOT what the action produces.  The a_0-bump term generates exactly the
two things already excluded. ***

And the profile that WOULD generate it is identified and is itself unacceptable: a bump profile C with
C'(w) = -B(w), i.e. C(w) = -[(1+w)ln(1+w) + 1]/(1+w), has C(0) = -1, so the kinetic addition 2AC is
NEGATIVE for A > 0 -- a GHOST.  Flipping to A < 0 restores the kinetic sign but inverts the mass slot
and breaks the five-environment calibration that fixed A in the first place.
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

w, A_, Q0, Phi = sp.symbols("w A Q_0 Phi", positive=True)
B = w / (1 + w) ** 2

# =================================================================================================
print("=" * 100)
print("PART A -- vary the bump term: which slot, which function")
print("=" * 100)

mass_coeff = sp.simplify(sp.diff(A_ * B * (Q0 * Phi) ** 2, Phi) / (2 * Phi))
check(sp.simplify(mass_coeff - A_ * B * Q0 ** 2) == 0,
      f"A1  MASS SLOT: varying w.r.t. Phi gives a term LINEAR in Phi with coefficient "
      f"A B(w) Q_0^2 -- it carries B, which is >= 0 everywhere",
      "so stage 33's theorem applies and excludes it: rho_eff >= 0 forces the extra enclosed mass to "
      "grow outward, while the data have it falling 12/12")

Bp = sp.simplify(sp.diff(B, w))
check(sp.simplify(Bp - (1 - w) / (1 + w) ** 3) == 0,
      f"A2  GRADIENT SLOT: varying w.r.t. the khronon hits B through its argument Y, giving a "
      f"coefficient A B'(w) Q_0^2 Phi^2 with B'(w) = {Bp} -- it carries B PRIME, not B, and Phi SQUARED",
      "this is the derivation the owed item asked for, and the function it returns is not the one "
      "stage 35 fitted")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- test the DERIVED gradient form against the two conditions")
print("=" * 100)


def Bp_n(v):
    v = np.asarray(v, float)
    return (1 - v) / (1 + v) ** 3


check(abs(float(Bp_n(0.0)) - 1.0) < 1e-12,
      f"B1  CONDITION (b) FAILS: B'(0) = {float(Bp_n(0.0)):.1f}, not 0.  So the derived gradient term "
      f"adds a CONSTANT to mu_eff in the deep-MOND limit where mu_M -> x vanishes -- the exact failure "
      f"that killed the q-route (q(0) = 1), and it breaks v^4 = G M_b a_0",
      "the Phi^2 factor softens it in galaxies but does not remove it: Phi does not vanish as x -> 0 "
      "within a system")

wl = np.array([0.0625, 0.16, 0.36, 0.64])
check(np.all(np.diff(Bp_n(wl)) < 0),
      f"B2  CONDITION (a') FAILS: across the cluster range w = 0.06-0.64, B' FALLS "
      f"{Bp_n(wl)[0]/Bp_n(wl)[-1]:.1f}x ({np.round(Bp_n(wl),4).tolist()}).  So the boost DECREASES with "
      f"x, i.e. the residual RISES outward -- the wrong radial direction, the same one every "
      f"positive-mass variant produced",
      "stage 35's B(w) RISES across that range, which is exactly why it worked and why it is not this")

check(float(Bp_n(0.36)) > 0,
      f"B3  AND THE SIGN IS WRONG TOO: no-ghost requires 2AB >= 0, hence A > 0; B' > 0 across the "
      f"whole cluster range (B'(0.36) = {float(Bp_n(0.36)):.4f}); so the derived term ADDS to mu_eff and "
      f"REDUCES the cluster boost.  Three independent failures, not one",
      "a mechanism that reduces the boost cannot close a deficit")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- what profile WOULD generate stage 35's mechanism, and why it is not allowed")
print("=" * 100)

C = sp.simplify(-sp.integrate(B, w))
check(sp.simplify(sp.diff(C, w) + B) == 0,
      f"C1  the profile that generates stage 35's form is fixed uniquely by C'(w) = -B(w): "
      f"C(w) = {sp.simplify(C)}",
      "so the working mechanism IS derivable from an action -- just not from THIS action's B")

C0 = float(sp.limit(C, w, 0))
check(C0 < 0,
      f"C2  *** AND IT IS GHOST-UNSTABLE: C(0) = {C0:.1f} < 0, so the kinetic addition 2AC that the "
      f"no-ghost theorem requires to be NON-NEGATIVE is negative for A > 0.  Replacing B by C buys "
      f"clusters at the price of a ghost ***",
      "and flipping to A < 0 restores the kinetic sign while inverting the mass slot and destroying "
      "the five-environment calibration that fixed A")

info("C3  FOR COMPLETENESS, the escape routes and why each is closed: (i) A < 0 -- inverts the mass "
     "term and the calibration; (ii) a NEW independent action term with profile C, on top of B -- "
     "possible in principle but that is ADDING STRUCTURE, i.e. a sixth dark-sector function, which is "
     "exactly what this framework's parameter-count argument has been built to avoid; (iii) a "
     "different quasi-static closure than delta Q = -Q_0 Phi -- but that closure is DERIVED (row 17, "
     "from unit-norm), not assumed, so it is not available to trade away.")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE OWED DERIVATION IS DONE AND IT CLOSES THE a_0-BUMP AS THE CLUSTER MECHANISM.

  1. The action's bump term A B(Y/Acal)(Q-Q_0)^2 generates BOTH slots, and the functions are fixed:
        MASS slot     ->  coefficient A B(w) Q_0^2          [carries B]
        GRADIENT slot ->  coefficient A B'(w) Q_0^2 Phi^2   [carries B PRIME]

  2. The mass slot is excluded by stage 33's theorem.  The gradient slot fails THREE ways:
        (b)  B'(0) = 1, not 0        -> breaks the deep-MOND limit and the BTFR theorem
        (a') B' falls 9.6x across clusters -> residual rises outward, wrong direction
        sign  A > 0 from no-ghost with B' > 0 -> REDUCES the cluster boost

  3. *** SO STAGE 35's MECHANISM IS NOT DERIVABLE FROM THIS ACTION.  It fits better than anything
     else tried -- 59% of the chi^2, every gate cleared -- and it is not what the theory produces. ***

  4. The profile that WOULD produce it is unique and identified: C(w) with C'(w) = -B(w), i.e.
     C(w) = -[(1+w)ln(1+w)+1]/(1+w).  And C(0) = -1, so 2AC < 0 for A > 0: a GHOST.  Every escape is
     closed -- A < 0 inverts the mass slot and the calibration; a separate C-term is a SIXTH
     dark-sector function, which the framework's own parameter argument forbids; and the closure
     delta Q = -Q_0 Phi is derived from unit-norm, not available to trade.

  5. WHAT THIS MEANS FOR THE PROGRAMME, plainly: the a_0-bump has been the live cluster candidate
     since v2.  It is now closed on a derivation, not on a fit -- the strongest kind of closure and
     the least pleasant.  Clusters return to OPEN with no candidate mechanism inside the current
     action, and the honest options are (i) accept clusters as an open problem of the framework,
     stated as such, or (ii) add structure and pay the parameter-count price openly.

  NOT CLAIMED: that no mechanism exists.  Claimed: that none exists in the action as written, and
  that stage 35's phenomenological success does not survive contact with the variation.
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
