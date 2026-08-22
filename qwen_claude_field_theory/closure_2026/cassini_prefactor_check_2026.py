#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cassini_prefactor_check_2026.py
===============================
IS THE CORPUS'S 4.8x-8.9x EVEN DIMENSIONALLY CONSISTENT WITH THE PUBLISHED ANCHORS?

Carl's question: before importing a pile of literature, check whether the original number was
calculated correctly at all. This is the fast, decisive version of that check -- it does not
require solving the nonlinear PDE, only that the answer have the right FORM and the right SCALE.

THE STRUCTURE, derived rather than quoted. In QUMOND the anomalous field is
(nu - 1) grad Phi_N. Near the Sun y = g_N/a_0 ~ 1e7-1e8, so any kernel with a power-law
approach nu -> 1 + 1/(2y) gives an anomalous field of CONSTANT magnitude a_0/2 -- the known
monopole liability -- while the QUADRUPOLE is generated where the solar field falls to the
external field, at the transition radius

        r_t = sqrt(G M_sun / g_ext).

An interior l = 2 harmonic is r^2 P_2, so it produces a CONSTANT tidal tensor. Matching at r_t
therefore forces, on dimensional grounds alone,

        Q_2 = q(eta) * sqrt(a_0^3 / (G M_sun)),   eta = g_ext/a_0

with q dimensionless. That prefactor is computable exactly and is kernel-INDEPENDENT; all the
kernel dependence sits in q. So the corpus's claim can be tested WITHOUT redoing the PDE:
does q implied by the corpus number match the published q anchors?
"""
import sys
import numpy as np

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
G_, MSUN, AU = 6.6743e-11, 1.98892e30, 1.495978707e11
GM = G_ * MSUN
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
CEIL = 5.2e-27
ANCH = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}      # Desmond, Hees & Famaey 2024

head("PART A -- the prefactor, computed exactly")
for nm, a0 in A0.items():
    pre = np.sqrt(a0**3 / GM)
    rt = np.sqrt(GM / (2.0 * a0))
    info(f"A1  {nm:9s}", f"sqrt(a_0^3/GM_sun) = {pre:.4e} s^-2;  "
                          f"r_t at eta=2 = {rt/AU:.0f} AU = {rt:.3e} m")
pre_can, pre_alt = np.sqrt(A0["canonical"]**3 / GM), np.sqrt(A0["alt"]**3 / GM)
check(abs(pre_can - 7.86e-26) / 7.86e-26 < 0.02,
      f"A2  the prefactor is {pre_can:.3e} s^-2 canonical / {pre_alt:.3e} alt -- and note it is "
      f"already ~15x the Cassini ceiling {CEIL:.1e}, so q must be BELOW ~0.066 to pass",
      "this single number frames the whole problem")

head("PART B -- what the PUBLISHED anchors imply, before any kernel choice")
for eta, q in ANCH.items():
    for nm, a0 in A0.items():
        Q = q * np.sqrt(a0**3 / GM)
        info(f"B1  eta={eta}, q={q:.3f}, {nm:9s}",
             f"Q_2 = {Q:.3e} s^-2 = {Q/CEIL:.2f}x the ceiling")
Q_at2_can = ANCH[2.0] * pre_can
Q_at2_alt = ANCH[2.0] * pre_alt
check(2.0 < Q_at2_can / CEIL < 4.5,
      f"B2  *** AT eta = 2 THE PUBLISHED ANCHOR GIVES {Q_at2_can/CEIL:.2f}x THE CEILING "
      f"CANONICAL / {Q_at2_alt/CEIL:.2f}x ALT -- NOT the 4.8x-8.9x the corpus reports ***",
      "and the anchors are the calibration the corpus's own pipeline was supposed to reproduce")
# extrapolate to the actual solar-circle eta
sl = np.polyfit(np.log(list(ANCH)), np.log(list(ANCH.values())), 1)
info("B3  q(eta) scaling from the three anchors", f"q ~ eta^{sl[0]:.3f}")
for eta in (1.9, 2.29, 2.6):
    q = np.exp(sl[1]) * eta ** sl[0]
    info(f"B4  extrapolated eta={eta:.2f}", f"q={q:.3f} -> {q*pre_can/CEIL:.2f}x canonical, "
                                             f"{q*pre_alt/CEIL:.2f}x alt")

head("PART C -- the discrepancy, stated plainly")
corp_lo, corp_hi = 4.8, 8.9
q_needed_lo = corp_lo * CEIL / pre_can
q_needed_hi = corp_hi * CEIL / pre_can
info("C0  inverting the corpus claim", f"4.8x-8.9x the ceiling requires "
     f"q = {q_needed_lo:.3f} to {q_needed_hi:.3f}")
# MATCHED-eta COMPARISON. The corpus number was computed over eta = 1.9-2.6, so comparing it
# with the anchor at eta = 2.0 is NOT like-for-like and overstates the gap. Extrapolate the
# anchors across the SAME eta range before judging.
band = []
for eta in (1.9, 2.29, 2.6):
    q = np.exp(sl[1]) * eta ** sl[0]
    band += [q * pre_can / CEIL, q * pre_alt / CEIL]
lo_a, hi_a = min(band), max(band)
info("C1a  anchors extrapolated over the SAME eta = 1.9-2.6, both footings",
     f"{lo_a:.2f}x to {hi_a:.2f}x the ceiling")
info("C1b  the corpus reports", f"{corp_lo:.1f}x to {corp_hi:.1f}x, and for the a_0-line "
     "specifically 5.59x canonical / 6.39x alt")
check(hi_a > corp_lo,
      f"C1  *** MATCHED LIKE-FOR-LIKE THE DISCREPANCY LARGELY DISSOLVES: the published anchors "
      f"extrapolated across eta = 1.9-2.6 give {lo_a:.2f}x-{hi_a:.2f}x, overlapping the corpus's "
      f"{corp_lo:.1f}x-{corp_hi:.1f}x. The corpus's a_0-line values (5.59x/6.39x) sit at most "
      f"{5.59/ (np.exp(sl[1])*2.29**sl[0]*pre_can/CEIL):.2f}x above the matched extrapolation. "
      "AN EARLIER DRAFT OF THIS FILE COMPARED AT MISMATCHED eta AND CLAIMED A 1.4x-2.7x "
      "DISCREPANCY -- THAT WAS A MANUFACTURED DEFICIT AGAINST THE CORPUS AND IS WITHDRAWN ***",
      "the corpus number is broadly CONSISTENT with the published calibration, not far from it")

info("C2  the benign explanation, which must be tested not assumed",
     "the anchors are for ONE kernel (the 'simple' nu). Carl's a_0-line approaches nu -> 1 as "
     "1/(2y), a POWER LAW, which is the slowest possible approach and gives the largest "
     "residual at eta ~ 2. A genuinely larger q is therefore POSSIBLE -- but it must be "
     "DERIVED, and the corpus never derived it")
info("C3  the adverse explanation, equally untested",
     "a factor-of-2 or 3/2 convention error in Q_2's definition would produce exactly this kind "
     "of offset, and those factors differ between papers")

head("PART D -- verdict on the audit question")
for s_ in [
    "*** THE 4.8x-8.9x SURVIVES A MATCHED-eta CONSISTENCY CHECK. Extrapolating the published "
    f"anchors across the same eta = 1.9-2.6 range gives {lo_a:.2f}x-{hi_a:.2f}x the ceiling, "
    "which OVERLAPS the corpus's range. The corpus number is therefore broadly consistent with "
    "its own calibration and is NOT obviously miscalculated. An earlier draft of this file said "
    "otherwise by comparing at mismatched eta; that claim is withdrawn as a manufactured "
    "deficit. ***",
    "WHAT IS SOLID REGARDLESS: the prefactor sqrt(a_0^3/G M_sun) = "
    f"{pre_can:.3e} s^-2 is exact, kernel-independent, and ALREADY {pre_can/CEIL:.0f}x the "
    "Cassini ceiling. So q must be below ~0.066 for ANY kernel to pass. The published anchors "
    f"({ANCH[1.0]}, {ANCH[1.5]}, {ANCH[2.0]}) are ALL above that. *** ON THE ANCHORS' OWN "
    "NUMBERS, THE ANCHOR KERNEL ALSO FAILS CASSINI, by 1.4x-3.3x. *** That is a much weaker "
    "statement than the corpus's, but it is one that follows from published values alone.",
    "SO THE AUDIT'S BRANCH IS NOT YET DETERMINED, and this file does not determine it. It "
    "establishes only that the SPECIFIC FACTOR 4.8x-8.9x is unsupported by the calibration it "
    "claims, while a violation of ORDER a few x remains plausible on the anchors alone. The "
    "three blind derivations must settle which.",
    "AND THE DECISIVE QUANTITY IS q(eta) FOR EACH KERNEL, computed from the field equations. "
    "That is exactly what the three independent derivations were commissioned to produce, and "
    "it is the only thing that separates 'the a_0-line is uniquely bad' from 'the pipeline was "
    "wrong'.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"PREFACTOR CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
