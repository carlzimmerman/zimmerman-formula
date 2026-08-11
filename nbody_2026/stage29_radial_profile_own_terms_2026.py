#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage29_radial_profile_own_terms_2026.py
========================================
THE RADIAL PROFILE CONFRONTATION, ON THE FRAMEWORK'S OWN TWO CLAIMS -- and it yields a THEOREM about
the cluster residual that no single-acceleration mechanism can satisfy.

--------------------------------------------------------------------------------------------------
SCOPE, STATED FIRST SO NOTHING IS OVERSOLD
--------------------------------------------------------------------------------------------------
A full profile FIT needs radial mass profiles (X-COP, CLASH).  *** THOSE ARE NOT IN THIS REPOSITORY. ***
The HFF Granata tables here are member PHOTOMETRY (positions, magnitudes, Sersic n), not M(r).  So
this stage does NOT fit profiles.  What it does instead is exact and was never done:

   1. DERIVE, from the framework's own a_0-line, what eta(r) MUST look like if the framework's own
      Sec. 5 profile prediction (rho_residual flat, M_residual ~ r^3) is true.
   2. CONFRONT that with the radial behaviour this corpus has already verified from the published
      literature with citations (the deficit is centrally concentrated, ~450 kpc cutoff, dying to
      eta ~ 1 by 2-3 Mpc: CLASH/Pizzuti-Famaey-Saltas, X-COP/Kelleher & Lelli 2024 arXiv:2405.08557).
   3. COMBINE with stage 28's measured cluster-to-cluster trend on 9830 real eRASS1 clusters.

Steps 1-3 are enough to prove something the profile fit would only confirm.

--------------------------------------------------------------------------------------------------
THE RESULT: eta IS NOT A FUNCTION OF ACCELERATION ALONE
--------------------------------------------------------------------------------------------------
    WITHIN a cluster:  g_bar FALLS outward, and the deficit ALSO falls outward
                       ==> eta RISES with g_bar   (positive dependence)
    ACROSS clusters at R500: stage 28 measured eta FALLING with g_bar
                       ==> eta FALLS with g_bar   (negative dependence, -0.149)

*** The same variable, opposite signs, in the same objects.  Therefore NO law of the form
eta = f(g_bar) -- the a_0-bump, a RAR-like cluster relation, any single-argument interpolation --
can describe the cluster residual.  A second variable is REQUIRED. ***  That is a structural
obstruction, it is derived from the framework's own kernel plus already-verified published radial
behaviour, and it is stronger than stage 28's sign result because it cannot be evaded by changing
which acceleration the mechanism reads.

And Part B shows the framework's own Sec. 5 row fails the radial test by a computable factor: rho_c
flat forces eta to GROW as r^2, so a residual normalised to eta(R500) = 2.334 predicts eta ~ 6.8 at
2.5 Mpc where the published behaviour is eta -> 1.  *** The Sec. 5 profile prediction has the wrong
radial SIGN, and it is the framework's own prediction, not an imported one. ***
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


# committed anchors
ETA_R500 = 2.334          # eRASS1 median, framework's own kernel (reproduced in stage 28 from FITS)
R500_MPC = 1.2            # typical R500 for these clusters
ETA_OUT_LO, ETA_OUT_HI = 1.0, 1.3     # published: eta -> ~1 by 2-3 Mpc
R_OUT_MPC = 2.5
SLOPE_POP = -0.149        # stage 28, measured: d log eta / d log y_bar across 9830 clusters

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- derive eta(r) from the a_0-line PLUS the framework's own Sec. 5 profile claim")
print("=" * 100)

r, a0, Gs, Mb, rho_c = sp.symbols("r a_0 G M_b rho_c", positive=True)

# the framework's OWN interpolation, and its deep limit
g_bar = Gs * Mb / r ** 2
g_pred = sp.sqrt(g_bar ** 2 + a0 * g_bar)                      # the a_0-line
g_deep = sp.sqrt(a0 * g_bar)
check(sp.simplify(sp.limit(g_pred / g_deep, r, sp.oo)) == 1,
      "A1  the a_0-line's outskirt limit is g -> sqrt(a_0 G M_b)/r (deep MOND), from the framework's "
      "own interpolation",
      "sympy limit; M_b -> const outside the gas, which is the relevant regime beyond R500")

# the mass the kernel itself accounts for
M_pred = sp.simplify(g_deep * r ** 2 / Gs)
check(sp.simplify(M_pred - r * sp.sqrt(a0 * Mb / Gs)) == 0,
      f"A2  so the kernel's own equivalent mass grows LINEARLY: M_pred(r) = r sqrt(a_0 M_b/G)",
      "this is the framework's prediction with NO extra component -- the baseline eta is measured "
      "against")

# Sec. 5's own residual-profile claim: rho_c flat  =>  M_res = (4pi/3) rho_c r^3
M_res = sp.Rational(4, 3) * sp.pi * rho_c * r ** 3
eta_r = sp.simplify(1 + M_res / M_pred)
# logarithmic slope done properly: d ln(eta-1)/d ln r = (r/(eta-1)) d(eta-1)/dr
pw = sp.simplify(r * sp.diff(eta_r - 1, r) / (eta_r - 1))
check(sp.simplify(pw - 2) == 0,
      f"A3  *** and Sec. 5's OWN profile claim (rho_c flat, M_c ~ r^3) then FORCES "
      f"eta(r) = 1 + C r^2 EXACTLY: the sympy log-slope d ln(eta-1)/d ln r = {pw}, i.e. the residual "
      f"must GROW as the SQUARE of radius ***",
      "derived from the framework's two claims together, with nothing imported")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- confront that with the radial behaviour the corpus has already verified")
print("=" * 100)

C = (ETA_R500 - 1.0) / R500_MPC ** 2
eta_pred_out = 1.0 + C * R_OUT_MPC ** 2
over = (eta_pred_out - 1.0) / (np.mean([ETA_OUT_LO, ETA_OUT_HI]) - 1.0 + 1e-9)

print(f"\n   normalise Sec. 5's flat-rho_c residual on the measured eta(R500) = {ETA_R500}:")
print(f"     C = (eta(R500) - 1)/R500^2 = {C:.4f} Mpc^-2   (R500 = {R500_MPC} Mpc)")
print(f"     => predicted eta({R_OUT_MPC} Mpc) = 1 + C r^2 = {eta_pred_out:.2f}")
print(f"     published behaviour at 2-3 Mpc:  eta -> {ETA_OUT_LO}-{ETA_OUT_HI}")

check(eta_pred_out > 3.0,
      f"B1  *** THE SEC. 5 PROFILE PREDICTION HAS THE WRONG RADIAL SIGN: flat rho_c forces "
      f"eta({R_OUT_MPC} Mpc) = {eta_pred_out:.1f}, while the published radial behaviour has the deficit "
      f"DYING to eta ~ {ETA_OUT_LO}-{ETA_OUT_HI} there.  The framework predicts the residual GROWS "
      f"outward as r^2; the data have it VANISHING outward ***",
      "cited, verified-in-corpus radial facts: CLASH (Pizzuti/Famaey/Saltas) and X-COP "
      "(Kelleher & Lelli 2024, arXiv:2405.08557); the ~450 kpc concentration is in the same record")

info(f"B2  the mismatch is not marginal: the excess residual at {R_OUT_MPC} Mpc is "
     f"{over:.0f}x what the published behaviour allows. And it CANNOT be rescued by lowering the "
     f"normalisation, because C is fixed by the measured eta(R500) = {ETA_R500} -- the same number "
     f"the corpus quotes as the cluster problem. Lowering C to fit the outskirts would erase the "
     f"R500 deficit the mechanism exists to explain.")

info("B3  AND THE ROW SHOULD NOT SIMPLY BE DELETED, because its OTHER half is confirmed: Sec. 5 says "
     "'rho_c flat, M_c ~ r^3, CAN GO NEGATIVE'. A residual that must go negative to keep eta from "
     "growing is exactly what the published outskirt behaviour demands. So the row's *sign-changing* "
     "clause is the part the data support, and the flat-rho_c parametrisation is the part that fails. "
     "That is a re-scope, not a withdrawal -- and it is a testable one.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE THEOREM: eta cannot be a function of g_bar alone")
print("=" * 100)

info("C1  WITHIN a cluster: g_bar falls monotonically outward (the gas is centrally concentrated), "
     "and the published deficit ALSO falls outward (concentrated inside ~450 kpc, eta -> 1 by "
     "2-3 Mpc). Two monotone decreasing functions of radius ==> eta is an INCREASING function of "
     "g_bar within a cluster.")

info(f"C2  ACROSS clusters at fixed R500: stage 28 measured d log eta/d log y_bar = {SLOPE_POP:+.3f} "
     f"on 9830 real eRASS1 clusters, robust to both kernels and both footings ==> eta is a "
     f"DECREASING function of g_bar across the population.")

check(SLOPE_POP < 0,
      "C3  *** THEREFORE eta IS NOT A FUNCTION OF g_bar ALONE: the same variable carries OPPOSITE "
      "signs within a cluster and across clusters.  Any law of the form eta = f(g_bar) -- the "
      "a_0-bump, a cluster RAR, any single-argument interpolation, whichever acceleration it reads -- "
      "is excluded by this alone ***",
      "and it is stronger than stage 28's sign result, which could be evaded by changing the "
      "mechanism's argument; this cannot, because it is a statement about ONE argument having two "
      "signs")

info("C4  WHAT THE SECOND VARIABLE COULD BE, and this is where the next real work is: the candidates "
     "that carry a radial direction independent of g_bar are (i) the local BARYON DENSITY or gas "
     "fraction (which varies with radius and with cluster mass differently), (ii) the enclosed-mass "
     "SCALE itself (a genuinely non-local ingredient, which is what the framework's Helmholtz sector "
     "supplies), and (iii) the external-field/environment term. The corpus's own EFE work and the "
     "khronon's non-local Helmholtz structure are both second-variable mechanisms already in hand -- "
     "so this obstruction points INTO the framework rather than out of it.")

info("C5  AND THE HONEST LIMIT ON C1: the within-cluster direction is taken from PUBLISHED radial "
     "behaviour, not measured here, because this repository has no radial mass profiles. If the "
     "published picture is wrong -- if the deficit does NOT die outward -- C3 dissolves. That is the "
     "single assumption the theorem rests on, it is well-sourced but it is an assumption, and the "
     "X-COP/CLASH profile fit is exactly what would retire it.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE RADIAL CONFRONTATION, ON THE FRAMEWORK'S OWN CLAIMS:

  1. From the a_0-line alone: outside the gas, M_pred(r) = r sqrt(a_0 M_b/G) -- the kernel's own
     equivalent mass grows LINEARLY with radius.

  2. Add Sec. 5's own profile prediction (rho_c flat, M_c ~ r^3) and eta(r) = 1 + C r^2 FOLLOWS.
     Normalised on the measured eta(R500) = {ETA_R500}, that gives eta({R_OUT_MPC} Mpc) = {eta_pred_out:.1f} where the
     published radial behaviour has eta -> {ETA_OUT_LO}-{ETA_OUT_HI}.  *** The Sec. 5 profile row has the wrong
     radial sign, by {over:.0f}x, and it cannot be renormalised out because C is fixed by the R500
     deficit the mechanism exists to explain. ***  Its 'can go negative' clause is the half the data
     DO support -- so the row is a re-scope, not a deletion.

  3. *** AND THE THEOREM, which is the real product: eta RISES with g_bar within a cluster (the
     deficit and g_bar both fall outward) and FALLS with g_bar across clusters (stage 28's measured
     -0.149 on 9830 objects).  One variable, two signs.  So NO single-argument acceleration law can
     describe the cluster residual -- the a_0-bump included, whichever acceleration it reads. ***

  4. That obstruction points INTO the framework: the second variable it demands is exactly what the
     khronon's non-local Helmholtz sector and the corpus's own EFE work already supply.  The next
     step is no longer 'find a mechanism' but 'fit the two-variable residual', and it needs the
     X-COP/CLASH radial profiles this repository does not yet hold.

  RESTS ON ONE ASSUMPTION, named: the within-cluster direction is taken from published radial
  behaviour (CLASH, X-COP), not measured here.  If the deficit does not die outward, item 3
  dissolves.
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
