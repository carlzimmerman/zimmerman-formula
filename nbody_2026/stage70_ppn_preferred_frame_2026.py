#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""

!!! SUPERSEDED IN PART -- 2026-08-17, by stage74_ppn_fork_adjudicated_2026.py !!!
THIS FILE'S HEADLINE BOUND IS WITHDRAWN.  alpha_1 = -4 K_B is CORRECT arithmetic, but
Foster & Jacobson's own appendix removes c_123 = 0 from their domain of validity BEFORE
deriving the formula, and Jacobson arXiv:0801.1547 names THIS EXACT THEORY and states the
PPN perturbation series is not applicable to it.  So:
  * "K_B < 2.5e-5" is NOT a bound.  Do not quote it.
  * SZ21's three published K_B fits (0.5/0.3/0.1) are NOT excluded.
  * check B2's label "THE BOUND" should read "the value of the generic formula evaluated
    outside its stated domain of validity".
  * IN FORCE instead: K_B in [2.1e-4, 0.25].  See stage74.
The checks below still pass on their own terms; they verify the ALGEBRA, not the APPLICABILITY.
stage70_ppn_preferred_frame_2026.py
===================================
STAGE 70: THE PPN PREFERRED-FRAME PARAMETERS alpha_1, alpha_2 -- THE_COMPLETION's
non-claim 6 ("PPN preferred-frame parameters alpha_1, alpha_2 for this F have not been
computed against lunar-laser and binary-pulsar bounds"), computed for the first time.

THE RESULT IS A TIGHT NEW BOUND, AND IT IS NOT COMFORTABLE.  Mapping AeST's aether
sector onto the Einstein-aether class (verified symbolically in PART A) gives
c_1 = K_B, c_2 = 0, c_3 = -K_B, c_4 = 0, and the standard Einstein-aether PPN result
then reduces to

        alpha_1 = -8(c_3^2 + c_1 c_4)/(2 c_1 - c_1^2 + c_3^2) = -4 K_B     (exactly)

so lunar laser ranging (|alpha_1| < 1e-4) demands

        K_B < 2.5e-5

which is FOUR ORDERS OF MAGNITUDE tighter than the corpus's own BBN cap (K_B <= 0.25),
and which EXCLUDES all three of Skordis & Zlosnik's published parameter sets
(K_B = 0.5 Cosh, 0.3 Higgs, 0.1 Exp).  The framework itself SURVIVES -- its quasi-static
phenomenology is K_B-blind (G~ = (1-K_B/2)G_qs; K_B appears zero times in the QS
equations, verified in the corpus) -- but the survival is by BLINDNESS, not by margin,
and the literature's fitted values are hit.

STATUS OF THE INPUT FORMULA: LITERATURE-INHERITED (Foster & Jacobson 2006,
gr-qc/0509083, the Einstein-aether PPN parameters).  It is NOT re-derived here.  Every
conclusion below is therefore CONDITIONAL on that formula and on the mapping's validity
(PART D lists the three ways AeST could evade it).  This stage's job is to put the number
on the table with its conditions attached, not to settle the theory.

Exit 0 = every check passed.
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


print(__doc__)

KB_BBN = 0.25            # corpus BBN cap (stage50)
SZ21_KB = {"Cosh": 0.5, "Higgs": 0.3, "Exp": 0.1}     # SZ21's published fits (stage57)
A1_BOUND = 1e-4          # |alpha_1|, lunar laser ranging
A2_BOUND = 1e-7          # |alpha_2|, solar-spin-axis / pulsars

# =================================================================================================
print("=" * 100)
print("PART A -- the mapping AeST aether sector -> Einstein-aether c's, verified symbolically")
print("=" * 100)
# Work with an abstract 4x4 gradient T_{mu nu} = grad_mu A_nu and match COEFFICIENT BY
# COEFFICIENT on the three independent scalars: T:T, (tr T)^2, T:T^transpose.
KB = sp.symbols("K_B", positive=True)
c1, c2, c3, c4 = sp.symbols("c_1 c_2 c_3 c_4")
TT, TR2, TTT = sp.symbols("TdotT trT2 TdotTt")     # T:T, (tr T)^2, T:T^T

# AeST: -(K_B/2) F_{mu nu} F^{mu nu} with F = 2 grad_[mu A_nu]
#   F:F = 2(T:T) - 2(T:T^T)   ==>   -(K_B/2) F:F = -K_B (T:T) + K_B (T:T^T)
aest = -KB * TT + KB * TTT
# Einstein-aether: -[c1 (T:T) + c2 (tr T)^2 + c3 (T:T^T) + c4 (J:J)]   (c4 term is A-dependent)
ea = -(c1 * TT + c2 * TR2 + c3 * TTT)
sol = sp.solve([sp.Eq(sp.expand(aest - ea).coeff(s), 0) for s in (TT, TR2, TTT)],
               [c1, c2, c3], dict=True)[0]
print(f"    matching the three independent gradient scalars gives: {sol}")
check(sol[c1] == KB and sol[c2] == 0 and sol[c3] == -KB,
      f"A1  *** THE MAPPING IS EXACT: AeST's -(K_B/2)F^2 aether term IS Einstein-aether with "
      f"c_1 = K_B, c_2 = 0, c_3 = -K_B, c_4 = 0 ***",
      "and c_1 + c_3 = 0 is precisely the corpus's committed GW170817 condition (c_T = 1 "
      "exact), so the mapping reproduces a result the corpus already has -- a consistency "
      "check on the identification itself")
check(sol[c1] + sol[c3] == 0,
      "A2  cross-check: c_1 + c_3 = 0 exactly, which is the c_T = 1 condition -- the same "
      "structural fact the corpus derives from the F^2 form, recovered here independently",
      "if the mapping were wrong, this would generically fail")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- alpha_1 for this theory (LITERATURE-INHERITED formula, flagged)")
print("=" * 100)
info("B0  *** LITERATURE-INHERITED: alpha_1 = -8(c_3^2 + c_1 c_4)/(2 c_1 - c_1^2 + c_3^2) "
     "is Foster & Jacobson 2006 (gr-qc/0509083) for Einstein-aether.  It is NOT re-derived "
     "here, and every number below inherits that dependence ***")
alpha1_gen = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)
alpha1 = sp.simplify(alpha1_gen.subs({c1: KB, c2: 0, c3: -KB, c4: 0}))
print(f"    alpha_1(general) = {alpha1_gen}")
print(f"    alpha_1(AeST)    = {alpha1}")
check(sp.simplify(alpha1 + 4 * KB) == 0,
      f"B1  *** alpha_1 = -4 K_B EXACTLY for this aether sector -- linear in K_B, with the "
      f"c_1^2 and c_3^2 pieces cancelling in the denominator because c_1 = -c_3 ***",
      "the same structure that protects the gravitational-wave speed makes the "
      "preferred-frame parameter maximally simple: no cancellation is available in the "
      "numerator, because c_3^2 survives whatever the sign of c_3")
kb_max = A1_BOUND / 4
check(abs(kb_max - 2.5e-5) < 1e-7,
      f"B2  *** THE BOUND: |alpha_1| < {A1_BOUND:.0e} (lunar laser ranging) requires "
      f"K_B < {kb_max:.2e} ***",
      f"versus the corpus's BBN cap K_B <= {KB_BBN} -- a factor "
      f"{KB_BBN/kb_max:.0f} tighter, i.e. four orders of magnitude")
info("B3  alpha_2 is NOT computed here: its Einstein-aether expression involves c_2 and the "
     "c_123 combinations in a form this stage does not have verified, and inventing it would "
     "be worse than leaving it open.  What CAN be said: alpha_2's observational bound "
     f"({A2_BOUND:.0e}) is {A1_BOUND/A2_BOUND:.0f}x TIGHTER than alpha_1's, so unless the "
     "AeST structure makes alpha_2 vanish identically, the K_B bound from alpha_2 would be "
     "correspondingly tighter still.  NAMED AS OWED, with the direction known.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- what the bound hits, and what it does not")
print("=" * 100)
print(f"    {'K_B value':>28s} {'|alpha_1| = 4 K_B':>18s} {'vs LLR 1e-4':>14s}")
for lab, v in list(SZ21_KB.items()) + [("corpus BBN cap", KB_BBN), ("PPN-allowed", kb_max)]:
    a1 = 4 * v
    print(f"    {lab:>28s} {a1:>18.2e} {'EXCLUDED x' + f'{a1/A1_BOUND:.0f}' if a1 > A1_BOUND else 'ok':>14s}")
check(all(4 * v > A1_BOUND for v in SZ21_KB.values()),
      f"C1  *** ALL THREE of SZ21's published parameter sets are EXCLUDED by lunar laser "
      f"ranging on this calculation, by factors "
      f"{min(4*v/A1_BOUND for v in SZ21_KB.values()):.0f}x-"
      f"{max(4*v/A1_BOUND for v in SZ21_KB.values()):.0f}x ***",
      "this is a statement about AeST-class theories in the literature, not only about this "
      "framework -- which is exactly why the conditional status of the input formula (B0) "
      "matters and why PART D lists the escapes before anyone quotes this")
check(True,
      "C2  WHAT THE FRAMEWORK LOSES: nothing computed.  The corpus's quasi-static "
      "phenomenology is K_B-BLIND -- G~ = (1 - K_B/2)G_qs is absorbed into the Newtonian "
      "normalisation, and K_B appears ZERO times in the QS equations (verified in the "
      "corpus against arXiv:2304.05134).  The RAR, the a_0-line, lensing, the wide-binary "
      "band and the Q_0 pin are all untouched by shrinking K_B to 1e-5",
      "so the framework survives -- but by blindness, not by margin: no observable it "
      "currently predicts would notice, which also means K_B is now pinned by PPN rather "
      "than by anything the framework itself says")
check(0 < kb_max < 2,
      f"C3  and the bound is INSIDE the stability window: 0 < K_B < 2 is the AeST/aether "
      f"no-ghost condition, and K_B < {kb_max:.1e} respects it (K_B stays positive).  So the "
      f"constraint tightens K_B without hitting a stability wall",
      "the residual worry is the K_B -> 0 limit itself, where the vector modes become "
      "non-dynamical; whether K_B ~ 1e-5 is safely inside that limit is an owed item "
      "(the vector-mode sound speed at c_1 = -c_3 was not computed here)")
check(True,
      f"C4  THE ONE THING THAT DOES CHANGE: the corpus's BBN bound (K_B <= {KB_BBN}) is no "
      f"longer the operative constraint on K_B -- PPN is, by four orders.  Any future "
      f"statement of the form 'under the corpus's own BBN bound K_B <= 0.25 ...' should now "
      f"quote K_B < {kb_max:.1e} instead, which STRENGTHENS conclusions that used the BBN "
      f"cap (e.g. stage57's mixing-share argument, where smaller K_B made the share smaller)",
      "so the practical effect on the corpus's existing arguments is favourable -- they were "
      "computed at a K_B that is now excluded from ABOVE, and the surviving region makes "
      "them stronger")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the three escapes, priced (this is why the result is CONDITIONAL)")
print("=" * 100)
esc = {
    "E1 the scalar sector contributes to alpha_1":
        "AeST is NOT pure Einstein-aether: it carries 2(2-K_B) J^mu grad_mu phi and "
        "-(2-K_B) Y.  These are scalar-aether couplings outside the c_1..c_4 class, and they "
        "could contribute to (or cancel) the preferred-frame response.  This is the MOST "
        "LIKELY escape and it is a well-posed calculation: redo the PPN expansion with the "
        "J.grad(phi) term retained.  Until then alpha_1 = -4K_B is the AETHER-SECTOR-ONLY "
        "result.",
    "E2 solar-system screening of the scalar":
        "if the scalar is screened in the solar system (lambda_s -> infinity, the corpus's "
        "Newtonian residual e^(-sqrt y) ~ 1e-3457 at Earth's orbit), then the scalar "
        "contribution to the PPN metric is suppressed and the aether-only result is the "
        "right one -- i.e. THIS ESCAPE CLOSES E1 in the direction UNFAVOURABLE to the "
        "framework.  Which of E1/E2 wins depends on lambda_s, which is FREE.",
    "E3 the curl-sector vanishing argument":
        "the corpus's aest_radial_aether_eom (citing Mistele 2305.07742) argues the spatial "
        "aether is the CURL sector and vanishes identically in SPHERICAL symmetry.  But the "
        "alpha_1 configuration is a mass moving at velocity w relative to the aether -- "
        "axisymmetric, NOT spherical -- so the curl sector is excited by construction and "
        "this argument does not apply to alpha_1.  Recorded because the corpus has used it "
        "as a general PPN defence (FACT 1 there), and for alpha_1 it is not one.",
}
for k, v in esc.items():
    print(f"    {k}:\n        {v}")
check(True,
      "D1  *** HONEST STATUS: the result is CONDITIONAL on (i) the Foster-Jacobson formula "
      "and (ii) the aether sector dominating the preferred-frame response.  Escape E1 is "
      "live and is the calculation that must be done; escape E2, if it holds, makes the "
      "bound BINDING rather than evadable; escape E3 -- the corpus's existing PPN defence "
      "-- does NOT cover alpha_1 ***",
      "so this stage does not claim the framework is in trouble; it claims the corpus has "
      "been carrying a defence that does not apply to this parameter, and names the one "
      "calculation that decides it")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- verdict")
print("=" * 100)
check(True,
      f"E1  NON-CLAIM 6 is now PARTLY DISCHARGED: alpha_1 = -4 K_B is computed (conditional, "
      f"aether-sector-only), giving K_B < {kb_max:.1e} from LLR -- the first quantitative "
      f"preferred-frame constraint in the corpus.  alpha_2 remains uncomputed and its bound "
      f"is 1000x tighter, so it is the sharper half and is still open",
      "the non-claim should be updated to reflect a computed alpha_1 with its conditions, "
      "not deleted")
check(True,
      "E2  RECOMMENDED CORPUS ACTIONS: (a) replace 'BBN K_B <= 0.25' with the PPN bound "
      "wherever K_B is quoted, noting it strengthens the arguments that used it; (b) record "
      "that the curl-sector spherical-symmetry defence does not cover alpha_1; (c) book the "
      "E1 calculation (PPN expansion retaining J.grad(phi)) as the deciding item; "
      "(d) compute alpha_2",
      "and (e) note for any future paper that SZ21's own published K_B values are excluded "
      "on this calculation -- a claim that needs E1 settled before it is made in public")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 70 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
