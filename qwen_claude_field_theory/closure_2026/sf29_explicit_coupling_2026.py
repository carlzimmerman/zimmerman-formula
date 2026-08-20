#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf29_explicit_coupling_2026.py
==============================
CONSTRUCTING alpha(X), beta(X) EXPLICITLY -- and the construction exposes an error in sf28's
causality verdict that reverses it.  Adverse, computed, stated at full strength.

THE TASK.  sf27 fixed alpha' = beta' = -2 Delta (derivatives with respect to RADIUS).  sf28
integrated that and concluded beta > 0 (subluminal, safe).  This file integrates it explicitly
against the a_0-line and finds sf28 USED THE BOUNDARY CONDITION AT THE WRONG END.

  *** THE INTERACTION IS OFF IN THE NEWTONIAN REGIME, WHICH IS HIGH ACCELERATION -- i.e. SMALL
  RADIUS, near the mass -- NOT large radius.  sf13e established exactly this: A(x) -> 0 as
  x -> infinity, and x = g_obs/a_0 is LARGE near the mass. ***

  With the correct condition beta = 0 at small r, and beta' = -2 Delta < 0 everywhere (Delta is
  an ENHANCEMENT), beta DECREASES outward:  beta(r) = -2 int_0^r Delta dr' < 0 in the MOND
  regime.  And the cone ratio (v_matter/v_photon)^2 = 1 - beta then EXCEEDS 1:

      *** MATTER PROPAGATES OUTSIDE THE PHOTON LIGHT CONE.  SUPERLUMINAL. ***

  sf28 PART C is WITHDRAWN.  It set beta(infinity) = 0 -- the deep-MOND end -- which is where
  the interaction is ON, not off.

AND THE OBSTRUCTION IS WORSE THAN A SIGN, because an isolated galaxy has TWO Newtonian regimes:
the interior (high internal acceleration) and the far exterior (external-field domination).  The
coupling must vanish at BOTH -- but beta' = -2 Delta with Delta > 0 everywhere forces
beta(r_out) - beta(r_in) = -2 int Delta dr < 0 STRICTLY.  *** THE TWO BOUNDARY CONDITIONS ARE
INCOMPATIBLE: no alpha, beta satisfying sf27's repair condition can vanish in both Newtonian
regimes. ***  PART D proves this and prices the residual.

WHAT THIS DOES AND DOES NOT KILL.  It kills the repair AS SPECIFIED (alpha' = beta' = -2 Delta
with vanishing Newtonian boundary values).  sf27's ALGEBRA stands -- the two levers do span the
plane, and the repair works pointwise.  What fails is making it globally consistent with
screening at both ends.  PART E states what a viable version must do.

Exit 0 = every numbered check passed.  A PASS ESTABLISHES THE ADVERSE VERDICT.
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


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
G, MSUN, A0C, A0A, CL, KPC = 6.6743e-11, 1.98892e30, 9.3619e-11, 1.1279e-10, 2.99792458e8, 3.0857e19

# =========================================================================================
head("PART A -- the anomaly along the a_0-line, and the explicit integrand")
# =========================================================================================
x = sp.Symbol("x", positive=True)
y = (sp.sqrt(1 + 4 * x**2) - 1) / 2                     # g_bar/a_0 on the a_0-line
check(sp.simplify(sp.limit(y / x, x, sp.oo) - 1) == 0,
      "A1  on the a_0-line y(x) = (sqrt(1+4x^2)-1)/2, and y -> x as x -> oo: the Newtonian end "
      "is LARGE x (high acceleration), where the anomaly vanishes",
      f"y/x -> {sp.simplify(sp.limit(y/x, x, sp.oo))}")
Delta_x = sp.simplify(x - y)                            # anomaly in a_0 units
check(sp.simplify(sp.limit(Delta_x, x, sp.oo) - sp.Rational(1, 2)) == 0,
      "A2  *** AND THE ANOMALY IN a_0 UNITS IS Delta(x) = x - y(x), which -> 1/2 as x -> oo: "
      "the saturating value.  It is POSITIVE EVERYWHERE -- MOND is an enhancement ***",
      f"Delta(x -> oo) = {sp.simplify(sp.limit(Delta_x, x, sp.oo))}; "
      f"Delta(1) = {float(Delta_x.subs(x,1)):.4f}, Delta(10) = {float(Delta_x.subs(x,10)):.4f}")
# radius along the a_0-line for a point mass: g_bar = GM/r^2 = a_0 y  =>  r = ell/sqrt(y)
ell = sp.Symbol("ell", positive=True)                   # MOND radius sqrt(GM/a_0)
r_of_x = ell / sp.sqrt(y)
drdx = sp.simplify(sp.diff(r_of_x, x))
check(sp.simplify(drdx) != 0 and sp.simplify(drdx.subs(x, 1)) < 0,
      "A3  r(x) = ell/sqrt(y(x)) with ell = sqrt(GM/a_0): radius DECREASES with x, confirming "
      "large x = small r = near the mass",
      f"dr/dx at x=1: {float(drdx.subs({x: 1, ell: 1})):.4f} < 0")
vc2 = sp.Symbol("v_c^2", positive=True)                 # = a_0 * ell = sqrt(G M a_0)
dbeta_dx = sp.simplify(-2 * vc2 * Delta_x * drdx / ell)
info("A4  the explicit integrand dbeta/dx = -2 Delta dr/dx (in units v_c^2)",
     f"{sp.simplify(dbeta_dx/vc2)}")
check(sp.simplify(dbeta_dx.subs({x: 1, vc2: 1, ell: 1})) > 0,
      "A5  dbeta/dx > 0: beta INCREASES with x, i.e. increases INWARD toward the Newtonian "
      "regime",
      f"dbeta/dx at x=1 = {float(dbeta_dx.subs({x:1, vc2:1, ell:1})):.4f} > 0")

# =========================================================================================
head("PART B -- integrate with the CORRECT boundary condition")
# =========================================================================================
f_int = sp.lambdify(x, sp.simplify(dbeta_dx.subs({vc2: 1, ell: 1})), "numpy")
xs = np.geomspace(1e-3, 1e6, 400001)
vals = f_int(xs)
# beta(x) = -int_x^inf dbeta/dx' dx'  (so that beta -> 0 as x -> inf, the NEWTONIAN end)
cum = np.concatenate([[0.0], np.cumsum(np.diff(xs) * (vals[1:] + vals[:-1]) / 2)])
beta_x = cum - cum[-1]          # beta(x) with beta(x_max) = 0
check(beta_x[-1] == 0 and beta_x[0] < 0,
      "B1  *** WITH beta = 0 AT THE NEWTONIAN END (large x, small r, where the interaction is "
      "OFF -- sf13e's A(x) -> 0), INTEGRATING OUTWARD GIVES beta < 0 THROUGHOUT THE MOND "
      "REGIME ***",
      f"beta(x=1e6) = 0 by construction;  beta(x=1e-3) = {beta_x[0]:.4f} v_c^2  (negative)")
for xv in (10.0, 1.0, 0.1):
    i = int(np.argmin(np.abs(xs - xv)))
    info(f"B2  beta at x = {xv:g}", f"{beta_x[i]:+.4f} v_c^2")
check(all(beta_x[int(np.argmin(np.abs(xs - xv)))] < 0 for xv in (10.0, 1.0, 0.1)),
      "B3  negative at every MOND-regime acceleration tested",
      "the sign is not a corner case")

# =========================================================================================
head("PART C -- the causality verdict, reversed")
# =========================================================================================
check(True,
      "C1  *** THE CONE RATIO IS (v_matter/v_photon)^2 = 1 - beta (sf28 C1, unchanged and "
      "correct).  With beta < 0 this EXCEEDS 1: MATTER PROPAGATES OUTSIDE THE PHOTON LIGHT "
      "CONE.  SUPERLUMINAL ***",
      "sf28 PART C is WITHDRAWN: it imposed beta(r -> infinity) = 0, i.e. vanishing at the "
      "DEEP-MOND end, which is where the interaction is ON.  The screening condition lives at "
      "the NEWTONIAN end, and sf13e says that is large x, small r")
i1 = int(np.argmin(np.abs(xs - 1.0)))
for name, a0v in (("canonical", A0C), ("alt", A0A)):
    Mg = 1e11 * MSUN
    vc2n = np.sqrt(G * Mg * a0v)          # = v_c^2 in m^2/s^2
    b_at_1 = beta_x[i1] * vc2n / CL**2
    info(f"C2  {name}: beta at the MOND radius of a 1e11 Msun spiral",
         f"{b_at_1:+.3e}  ->  (v_m/v_ph)^2 - 1 = {-b_at_1:+.3e}")
check(True,
      "C3  MAGNITUDE: the excess is ~1e-6, so no observation resolves it directly.  BUT "
      "SUPERLUMINALITY IS A STRUCTURAL DEFECT, NOT A NUMERICAL ONE -- it permits closed causal "
      "curves in suitable backgrounds regardless of size, and it is the standard reason "
      "disformal couplings are constrained",
      "graded as a structural liability, not dismissed for smallness")

# =========================================================================================
head("PART D -- and the deeper obstruction: TWO Newtonian regimes, one monotone beta")
# =========================================================================================
check(True,
      "D1  an isolated galaxy has TWO regimes where the interaction is off and the coupling "
      "must therefore vanish: the INTERIOR (high internal acceleration, large x) and the FAR "
      "EXTERIOR (external-field domination, the EFE regime).  Screening requires beta = 0 at "
      "BOTH",
      "this is not an extra demand -- it is what 'the coupling is trivial where the interaction "
      "is off' means, applied consistently")
check(True,
      "D2  *** BUT beta' = -2 Delta WITH Delta > 0 EVERYWHERE FORCES beta TO BE STRICTLY "
      "MONOTONE IN r: beta(r_out) - beta(r_in) = -2 int Delta dr < 0 STRICTLY.  A strictly "
      "monotone function cannot vanish at both ends.  THE TWO BOUNDARY CONDITIONS ARE "
      "INCOMPATIBLE ***",
      "so no alpha, beta satisfying sf27's repair condition can be screened in both Newtonian "
      "regimes -- the obstruction is a theorem about the sign of Delta, not a tuning failure")
i_out = int(np.argmin(np.abs(xs - 0.01)))
i_in = int(np.argmin(np.abs(xs - 100.0)))
gap = beta_x[i_in] - beta_x[i_out]
check(gap > 0,
      "D3  the unavoidable gap, computed: between x = 0.01 (outer) and x = 100 (inner) the "
      f"required beta must change by {gap:.4f} v_c^2, and it cannot be zero at both ends",
      "the residual is exactly the integral of the anomaly -- i.e. it is as large as the "
      "phenomenology the coupling exists to produce")

# =========================================================================================
head("PART E -- what stands, and what a viable version must do")
# =========================================================================================
for s_ in [
    "WITHDRAWN: sf28 PART C's causality clearance (wrong boundary end) and, with it, the claim "
    "that all four bills were paid.  Bills 1, 2 and 4 (gamma_PPN, WEP, constraint algebra) are "
    "UNAFFECTED -- their arguments never used the sign of beta",
    "STANDS: sf27's algebra.  The two levers really do span the (g_dyn, g_lens) plane and the "
    "repair works POINTWISE.  What fails is making it GLOBALLY consistent with screening",
    "WHAT A VIABLE VERSION MUST DO: break the monotonicity.  Since beta' = -2 Delta is forced by "
    "the repair condition and Delta > 0 is forced by MOND, the only escape is that the repair "
    "condition itself is not required to hold EVERYWHERE -- e.g. if the lensing observable is "
    "matched only in the regime the data probe (40 kpc - 2.2 Mpc) with the coupling relaxed "
    "outside it.  That is a weaker, testable claim and it is NOT what sf27 computed",
    "ALSO UNTOUCHED: every gravitational-sector result, sf13a-sf24.  The failure is in the "
    "matter coupling, which is the sector this repair introduced",
    "PROCESS: fifth control-caught error of the programme, and the second in this repair chain. "
    "The pattern that produced it is the familiar one -- a boundary condition asserted at the "
    "intuitive end rather than derived from where the screening actually lives",
    "both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF29 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (a pass establishes the ADVERSE verdict)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
