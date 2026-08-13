#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage54_y_gate_and_cell3_verdicts_2026.py
=========================================
STAGE 54: THE Y=0 GATE-COUNTING QUESTION AND CELL 3, BOTH ADVERSARIALLY REFEREED --
CELL 3 SURVIVES AS A TRANSPORT CHANNEL (the first mechanism to pass the binding-epoch
wall STRUCTURALLY), AND THE Y-LANE'S TWO HEADLINES DIE WHILE ITS REFEREE FINDS THE
SHARPER RESULT: A CANDIDATE PIN ON X, AND THE X DILEMMA.

Provenance: two builder lanes (2026-08-13; their verifiers were killed by a session limit,
so verification ran as two dedicated referees after the reset -- one per lane, per the
standing rule).  Evidence committed alongside, with supersession banners where refuted:
  stage54_ev_laneY_gate_counting_2026.py   (18/18; two headlines REFUTED by its referee)
  stage54_ev_laneY_referee_2026.py         (the Y referee's counter-script, green)
  stage54_ev_lane_c3_pricing_2026.py       (12/12; survived, corrections carried here)
  stage54_ev_c3_referee_symbolic.py        (8/8)   stage54_ev_c3_referee_numbers.py (9/9)

WHAT DIED:
  * Lane Y's D1 "X-free ratio theorem / the wall stands in every fork": the support-side y
    DROPPED the static MOND gradient (y_static ~ 0.06-0.28 at the halt radii, X-free --
    stage 51 line 62 had committed "inside a collapsed halo y is order 0.1-1" all along).
  * Lane Y's fork (c) "the corpus does not pin X": the corpus's own RAR + drain free-fall
    arithmetic MIRRORS the lane's C3 bound into an equality (B2 below).
  * Cell 3 as PRESSURE support: dead three ways over (surface ceiling O(1) at best, deep
    shortfall 134x-1.7e4x, monotone inward decline).

WHAT SURVIVES (labels per the referees):
  * ESTABLISHED -- the flow-form identity Y = Qbar^2|v_phi - v_aether|^2 on linear modes
    (EXACT in the aether rest frame); delta-Y^(1) = 0 intact; the provenance algebra
    X = sqrt(8pi) R_dm/(kappa nu0 mu17) with mu17 = sqrt(K''(Q0)) free WITHIN the cited
    relations; the velocity table + gate thresholds as CONDITIONAL arithmetic; the rec-side
    correction of stage 51/52's linear-mode pricing (their kill priced Y-held, not the
    realized flow object -- same verdict at large X, wrong variable).
  * ESTABLISHED -- Cell 3 sign/taxonomy (J.A = 0 identically; J = 0 on FLRW; the O(eps^2)
    piece feeds the (2-K_B) chi-E mixing; static limit = SZ21 Eq 6's -2 grad(Phi).grad(phi)
    cross term EXACTLY and ALONE), and the pressure-reading kill.
  * CANDIDATE -- THE X-PIN (B2): X ~ 316-1000, mu17 ~ 181-574.  Wants its own lane.
  * CANDIDATE -- Cell 3's transport/drain channel: two-ended separation ~1e7 (halo drain up
    to 671x binding at the mu-pinned ceiling vs 6.8e-5 of H(rec) at recombination) -- the
    binding-epoch wall does NOT kill it, structurally (fixed coefficient, no y-gate, no
    1/a0^2(z) amplification: stage 51's failure mode is absent by construction).
  * THE X DILEMMA (the new standing question, adverse-leaning both ways): EITHER X is
    pinned ~10^3 and the banked CLASS pass carries an UNPRICED ACTIVE Y-SECTOR at
    recombination, OR X is free and the gate wall has an unpriced small-X escape.  The
    corpus cannot currently hold BOTH the wall and the clean CMB.  Settling X settles it.

NEW OWED ITEMS (booked here; none may be silently dropped):
  (1) the X-pin adversarial lane (escape route to price: an aether spatial profile changing
      the static/flow split);
  (2) an in-repo linear-perturbation check of SZ21 Eqs 11-12 at the (Q0, K2, K_B) the
      collapse solve will use -- the two-ended test's recombination leg is the corpus's
      FIRST load-bearing use of SZ21's unreproduced Boltzmann fit; until then every use
      carries the tag LITERATURE-INHERITED;
  (3) the F1 normalization convention (a factor-2 ambiguity) pinned BEFORE the transport
      solve's 0.3x kill threshold freezes;
  (4) the 1+1D w(r,t) transport solve with alignment-sign reporting and the anti-aligned
      (reversed-scalar, net-repulsive) branch as a PRE-STATED report condition;
  (5) the perturbation health matrix (still owed from stage 51 -- unchanged).
CORRECTION to stage 53 PART B (CANDIDATE map): Cell 1 at (2,0) is NOT robustly dead -- at
pinned X under FLOW pricing the violation is ~1.3 (marginal-LIVE); the committed
674x-3.79e4x figure is the quasi-static pricing.  Both recorded; neither is a theorem.

Exit 0 = every check passed.
"""

import os
import sys

import numpy as np

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


print(__doc__)
C_KMS = 2.99792458e5

# =================================================================================================
print("=" * 100)
print("PART A -- the Y-lane's surviving arithmetic, re-checked inline")
print("=" * 100)

# A1 the provenance algebra: X = sqrt(8pi) R_dm / (kappa nu0 mu17), mu17 = 1 endpoints
KAPPA, R_DM = 0.5, 0.387
NU0_LO, NU0_HI = 2.14e-5, 1.77e-4
X_nat_lo = np.sqrt(8 * np.pi) * R_DM / (KAPPA * NU0_HI * 1.0)
X_nat_hi = np.sqrt(8 * np.pi) * R_DM / (KAPPA * NU0_LO * 1.0)
check(abs(X_nat_hi / 1.813e5 - 1) < 0.01 and abs(X_nat_lo / 2.192e4 - 1) < 0.01,
      f"A1  provenance algebra reproduces: natural (mu17=1) X = {X_nat_lo:.3e} (nu0 ceiling) "
      f"to {X_nat_hi:.3e} (floor)",
      "mu17 = sqrt(K''(Q0)) is free WITHIN the cited relations (beta=1, the a0(z) law and "
      "c_s^2 do not pin it) -- but see B2: the corpus pins X elsewhere")

# A2 the static support-side y that the lane's theorem dropped (the refutation's core)
CH2 = 1.08e4                      # (km/s)^2, committed c_h^2 = G M / R_halt
A0_CAN = 9.3619e-11
R_HALT_KPC = np.array([13.5, 60.0])
KPC = 3.0857e16                   # km
y_static = (CH2 / (R_HALT_KPC * KPC)) / (A0_CAN * 1e-3)   # g_N/a0, a0 in km/s^2
check(0.04 < y_static.min() < 0.07 and 0.2 < y_static.max() < 0.35,
      f"A2  the STATIC MOND gradient at the committed halt radii gives y_static = "
      f"{y_static.max():.2f}-{y_static.min():.2f} (13.5-60 kpc) -- X-FREE, and stage 51:62 "
      f"committed 'y is order 0.1-1' inside halos",
      "dropping this from the support side is what made the lane's 'X-free wall theorem' "
      "false: Y at the support point is |grad phi_static + Qbar v_flow|^2, not flow alone")

# A3 the flow-side thresholds (conditional arithmetic, confirmed by both scripts)
V_REC_MODE, V_REC_RMS = 12.6, 23.1          # km/s
AMP_FLOOR, AMP_CEIL = 2.78e4, 2.30e5        # A0/A(rec)
for v, xm, xc, lab in ((V_REC_MODE, 134, 47, "worst mode"), (V_REC_RMS, 78, 27, "rms")):
    x_lo = 1.0 / np.sqrt((v / C_KMS) ** 2 * AMP_FLOOR)
    x_hi = 1.0 / np.sqrt((v / C_KMS) ** 2 * AMP_CEIL)
    check(abs(x_lo / xm - 1) < 0.15 and abs(x_hi / xc - 1) < 0.15,
          f"A3  y_rec < 1 ({lab}) requires X < {x_lo:.0f} (floor) / {x_hi:.0f} (ceiling) "
          f"-- lane quoted {xm}/{xc}",
          "CONDITIONAL arithmetic: which side of these X sits on is the X-question itself")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the referee's own findings: the X-pin (CANDIDATE) and the X dilemma")
print("=" * 100)

# B2 the X-pin mirror: the same field carries the RAR static gradient, so the condensate
# flow speed is slaved: v_s = sqrt(y_static) c / X; the committed drain free-fall ~300 km/s
V_FF = 300.0
X_pin = np.sqrt(np.array([0.1, 1.0])) * C_KMS / V_FF
check(abs(X_pin[0] / 316 - 1) < 0.01 and abs(X_pin[1] / 1000 - 1) < 0.01,
      f"B2  THE X-PIN (CANDIDATE): v_s = sqrt(y_static) c/X with the committed free-fall "
      f"~{V_FF:.0f} km/s and y_static = 0.1-1 forces X = {X_pin[0]:.0f}-{X_pin[1]:.0f}",
      "one field, one gradient, both jobs: an equality, not a free parameter.  Implied "
      "mu17 = 181-574.  Escape to price in its own lane: an aether spatial profile "
      "changing the static/flow split")
y_rec_pin = X_pin**2 * (V_REC_RMS / C_KMS) ** 2 * AMP_FLOOR
check(y_rec_pin[0] > 10,
      f"B3  at the pinned X the recombination flow-y is {y_rec_pin[0]:.0f}-{y_rec_pin[1]:.0f} "
      f"(floor amp; x8.3 at the ceiling) -- fork (a) REALIZED: gates saturate, V_sat governs",
      "THE DILEMMA: pinned X => the banked CLASS pass carries an unpriced ACTIVE Y-sector "
      "at recombination; free X => the wall has a small-X escape.  Not both wall and clean "
      "CMB, until X is settled")
info("B4  correction to stage 53 B2 (CANDIDATE map): Cell 1 (2,0) violation ~1.3 at pinned X "
     "under FLOW pricing = marginal-LIVE; the committed 674x-3.79e4x is the QUASI-STATIC "
     "pricing.  Both recorded; the map stays CANDIDATE")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- Cell 3: pressure DEAD, transport VIABLE-CANDIDATE (referee-corrected numbers)")
print("=" * 100)

info("C1  ESTABLISHED (doubly verified, sympy x2): J.A = 0 identically; J = 0 on FLRW exactly; "
     "delta-J^0 = 0 at first order; the O(eps^2) piece feeds the (2-K_B) chi-E mixing; the "
     "static limit is SZ21 Eq 6's -2 grad(Phi).grad(phi) cross term EXACTLY -- and ALONE "
     "(the -(2-K_B)Y term contributes NO static cross term; referee's V5).  Citation "
     "corrected: the committed Eq-6 source is AEST_SPHERICAL_COLLAPSE_SETUP.md:136, not bridge1")
info("C2  PRESSURE READING DEAD (ESTABLISHED): surface ceiling 0.80-1.11 (O(1) at best), "
     "interior 1e4 rho_dm0: 0.27-0.43, deep 1e6: shortfall 134x-1.7e4x (the lane UNDERSTATED "
     "it), monotone inward decline 0.86 -> 0.0022.  R_halt = 176-210 kpc (erratum: not 226) "
     "-- the ~200-kpc fringe-core class KiDS already charges")
sep = 671.0 / 6.8e-5
check(sep > 1e6,
      f"C3  the TWO-ENDED TEST (ESTABLISHED as structure): halo-end drain up to 671x binding "
      f"(mu-pinned ceiling) vs recombination-end 6.8e-5 of H(rec) -- separation {sep:.1e}",
      "the FIRST mechanism in the graveyard to pass the binding-epoch wall STRUCTURALLY: "
      "fixed coefficient, no y-gate, no 1/a0^2(z) amplification.  Transport channel = "
      "VIABLE-CANDIDATE; owed items (2)-(4) of the header gate the next step")
info("C4  the recombination leg is the corpus's FIRST load-bearing use of SZ21's unreproduced "
     "Boltzmann fit: every use is tagged LITERATURE-INHERITED until owed item (2) closes.  "
     "DEAD-2 (modulation kill) holds in the ALIGNED sector only; the anti-aligned "
     "(net-repulsive) branch is a pre-stated report condition of the 1+1D solve")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 54 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
