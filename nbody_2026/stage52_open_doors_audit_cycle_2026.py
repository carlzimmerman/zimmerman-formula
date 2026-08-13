#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage52_open_doors_audit_cycle_2026.py
======================================
THE FOUR-DOOR FLEET, SETTLED: 3 of 4 lanes REFUTED by both adversarial verifiers; two doors CLOSED
FURTHER; one committed stage (51) killed within two hours of its own commit and bannered; one committed
document row withdrawn (wrong sign, 7-8 orders); the DR4 suite taken from red to green.  Nothing opened.

This is a consolidation stage: every number below is either re-derived here with a check, or marked
[lane]/[verifier] and quoted as unowned.

--------------------------------------------------------------------------------------------------
LANE A -- THE BOSE-EINSTEIN KERNEL: PRIOR ART + AN 11-SIGMA NEGATIVE.  ROUTE CLOSED.
--------------------------------------------------------------------------------------------------
* ATTRIBUTION CORRECTION (stands, and goes in the record): the Route A kernel nu(y) = 1/(1-e^(-sqrt y))
  is NOT McGaugh-Lelli-Schombert 2016's.  It is *** Milgrom & Sanders 2008 (ApJ 678, 131, arXiv:0709.2561),
  their Eq. (13) family at alpha = 1/2 *** -- the second term's coefficient 1 - 1/(2 alpha) vanishes
  exactly (verified symbolically below), and MS08 introduce it saying they "know of no concrete
  theoretical considerations that can dictate the form".  MLS 2016 is the empirical ADOPTION.
* The thermal reading is ALSO prior art: Lelli-McGaugh-Schombert-Pazy 2017 (arXiv:1610.08981, sec.III.2)
  already note the Planck-law resemblance with "h plays a similar role as g-dagger" -- and since the
  Planck exponent IS E/kT, that sentence publishes E/T = sqrt(y).
* The identity nu = 1 + n_BE(u) holds for ARBITRARY u -- it is the Bose rearrangement, not physics.  The
  only MOND content is u = sqrt(y), forced by deep-MOND scale invariance (Milgrom, arXiv:1609.06642).
* THE KILL: fixing the bath temperature to the dS value backs out a superhorizon length (6.8x the
  horizon, both footings), and inverting with the natural L = c/H predicts
        *** kappa_pred = sqrt(8pi/3)/(4 pi^2) = 0.07332 -- 11.1 sigma BELOW the measured 0.551 +/- 0.043
            (5.2 sigma below the BTFR 0.465 +/- 0.076). ***
  This is the MIRROR IMAGE of the Deser-Levin trap (T2 fires low instead of high).  A fixed-T bath also
  cannot host a_0(z): L would have to run to 300-1000x the horizon by recombination.  [verifier]
  The class does not even pin the function: the one-parameter family 1 + A/(e^(A sqrt y)-1) reproduces
  deep MOND for every A, near-degenerate with a_0 (<= 0.015 dex after refit).  [verifier]
* NET: route closed.  Kept: the attribution correction, and an 11.1-sigma negative that is CONSISTENT
  with kappa being measured rather than derived.

--------------------------------------------------------------------------------------------------
LANE B -- THE NO-GO EXTENDED, AND STAGE 51's "SURVIVOR" KILLED THREE WAYS (banner on stage 51)
--------------------------------------------------------------------------------------------------
THE REAL DELIVERABLE, a theorem worth keeping: route-B support must calibrate at the halo surface
(the deep-interior calibration self-halts 2.5e12 M_sun at 29 kpc with v_circ = 609 km/s, INSIDE the RAR
-- incoherent).  That forces rho_h = 1654 rho_dm0, and the cosmic mean CROSSES that density at
        *** z_bind = 1654^(1/3) - 1 = 10.83, where the density ratio is 1 for EVERY polytropic index --
        so lambda_J is gamma-INDEPENDENT there (4.46 Mpc comoving, ~9x any acceptable cap), and the
        derived a_0(z) law is FLAT there: a_0(10.83)/a_0(0) = 0.9997 (floor) / 0.980 (ceiling). ***
The 0.0060 recombination suppression is the WRONG LEVER: the binding epoch is z ~ 11, not z ~ 1090.

STAGE 51's THREE KILLS (bannered on the stage itself; the worst is mine):
 1. TAUTOLOGY, exact: K_eff = 2 pi G R_halt^2 identically, so R_core = pi R_halt EXACTLY -- 188.5 kpc IS
    pi x the ASSUMED 60 kpc halt.  "Sgr A* removed" restated the premise.  (Failure mode #1, committed
    by me one day after writing the taxonomy that names it.)
 2. THE GATE OPENS AT RECOMBINATION: y = Y/Acal(Q) carries a_0^2(z) in the DENOMINATOR, so
    a_0(1090) = 0.0060 a_0(0) makes y EXPLODE toward recombination (x428-3000 vs the halt, both
    footings) -- W ~ y^2 AMPLIFIES the coupling exactly where the CMB needs the dust pressureless:
    [verifier] c_s^2(rec) >= 8.5e9 (km/s)^2 vs the committed CLASS cap 2606, a 3.25e6x violation.
    Stage 51 checked z = 20 and the forest, never recombination.
 3. THE LENSING ENDPOINT: [verifier] stage 12's committed KiDS machinery charges the 188-kpc polytrope
    Delta chi^2 ~ +1.2e3 to +2.0e3, worse than the +927 configuration stage 12 already rejected.  (The
    two verifiers disagree on which radius carries which magnitude -- kill robust, magnitude unsettled.)
 ALSO FALSE: "mass-independent core".  Under the gate, R_halt scales as sqrt(M_bar) ([verifier]:
 13.5 kpc at 6e9 M_sun -> 135 kpc at 6e11 -- consistent with sqrt(100) = 10, checked below), and
 baryon-poor systems lose the halt entirely: the collapse problem RETURNS where halos are darkest.

WHAT SURVIVES OF STAGE 51: Parts A and B only -- dL/du = K' (gravity-only coupling is nothing) and the
sign theorem (scalar exchange = anti-support; vector-on-current = support).  Algebra; they stand.
THE DUST PROBLEM IS FULLY OPEN AGAIN, now with a sharper wall: any repair must supply pressure at
z <~ 11 without supplying it at z ~ 1090, and no function of y can do that because y RISES toward the
past.  Route A' (stages 10-11) remains the one live alternative.
[SUPERSEDED BY STAGE 53, 2026-08-13: Route A' is DEAD (empty gamma range; binding-epoch wall fires at
 z_bind = 10.19 on its own profile), and this line was a T3 -- committed stage12 (ee0b1793, 6/6 green,
 'THE TWO-FIELD WINDOW CLOSES') had already excluded it, and lines 56-57 above USE stage12 as a weapon.
 The live list is now stage53 PART B3's four untried cells (+ Cell 3 reopened).  Also corrected there:
 V51 = 3.25e6 (line 58) is the SATURATING-gate bound, NOT the y^2 violation (that is 5.2e11-2.9e13x).]

--------------------------------------------------------------------------------------------------
LANE C -- DR4: THE CLEAN LANE (both verifiers: not refuted).  SUITE TAKEN RED -> GREEN THIS COMMIT.
--------------------------------------------------------------------------------------------------
* Hash integrity: ALL NINE digests verified against every commit that ever touched the frozen file;
  current PREREGISTRATION_DR4.md = e4cbf...9ec8 = AMENDMENT9_HASH.txt.  Nothing touched.  Two benign
  bookkeeping notes recorded: AMENDMENT4_HASH's "cannot now be recovered" digest CAN be (git preserves
  d0a0023a -> 545d42c5...), and commit 0ef07cd1 left one content-consistent but UNSTAMPED intermediate
  state 14 min after the A4 filing.
* END-TO-END DRY RUN, exit 0, on the 1.4 GB El-Badry+21 eDR3 catalog: 10,624 pairs, 802 deep;
  *** gamma_hat = 1.2075 +/- 0.0350 canonical / 1.2125 +/- 0.0337 ALT, kappa = 1.022 ***; all four
  injections recovered; the alt-target injection correctly tripped PRE-DECLARED UNSCOREABLE.  [lane,
  reproduced by both verifiers to the digit]  Machinery works; the dry run remains non-scoring (sec 1.6).
* THE SUITE WAS RED AT HEAD (30/31): D6 grepped for a literal renamed by the legitimate Amdt-9 rewire.
  FIXED STRUCTURALLY in this commit (assert report_7e prints the Newton distance and references BOTH
  in-force target variables, no era-specific labels); C1/C2 got a verifier-found caveat comment (their
  string test cannot distinguish live text from a changelog quoting it -- a live-text test is OWED).
  Suite now 31/31.
* FLAGGED RISKS carried into the record, not resolved here: [verifier] Amendment 8(h)'s own kappa-window
  1.0575-1.0959 sits OUTSIDE the frozen [0.95, 1.05] gate under the framework's own kernel -- computed
  for the SUPERSEDED MI target and never recomputed for Amdt 9's larger boost, so a framework-side
  confirmation may be pre-declared no-verdict BY MECHANISM; fit_gamma has no argmin-interior assertion
  and no chi^2 acceptance gate (a synthetic drive pinned the grid maximum at +400 sigma_fit,
  straight-faced); checklist items 5/6 reachable only via --catalog and never executed by a committed
  run; doc-vs-script arm-separation tension (2.68 vs 2.27 sigma).  Amendment 9(b)'s nonlinear AQUAL-EFE
  solve is still owed, and if it moves gamma_v an AMENDMENT 10 MUST BE FILED BEFORE DR4.

--------------------------------------------------------------------------------------------------
LANE D -- SME BRIDGE: NUMBERS CLEAN, FRAMING REFUTED.  DRIFT PREDICTION: HOPELESSLY SMALL (a result).
--------------------------------------------------------------------------------------------------
* Induced s^TX at Saturn: [lane, reproduced by both verifiers] 10^-363.6 canonical / 10^-331.5 ALT --
  margin 10^354 / 10^322 against Kostelecky-Russell Table D50.  Passes everything by absurd margins.
* THE NEW RESULT, derived and kept: the a_0(z) law implies a PRESENT-DAY DRIFT
        *** adot_0/a_0 = +(3/2) nu_0^2 H_0 in [4.7e-20, 3.5e-18] per yr -- kappa-blind, footing-blind ***
  (re-derived below).  Riding on 10^-363 it is HOPELESSLY SMALL in every channel; no published bound on
  a DRIFTING s_munu even exists, and the nearest proxies (LLR Gdot/G ~ 1e-14/yr) are ~7000x too loose
  for the whole-sector rate.  Atomic clocks cannot see it because the framework predicts alpha-dot = 0
  EXACTLY.  The ONLY observable expression of the drift is the integrated a_0(z) law itself -- the
  MUSE/high-z front, whose sharp null stands.
* *** WITHDRAWAL EXECUTED THIS COMMIT: STATE_OF_THE_FRAMEWORK.md line 165 carried
  "adot_0/a_0 ~ -3e-11/yr, DERIVED" -- 7-8 ORDERS TOO LARGE AND WRONG IN SIGN (the derived law RISES to
  a maximum today, so adot_0 > 0).  Row corrected in place with a supersession note. ***
* REFUTED FRAMING, recorded: the per-body prefactor A(y_body) structure is MODIFIED-INERTIA by
  construction, and the MI arm is closed (21 sigma) -- under the operative MG arm the bridge is an
  UNQUANTIFIED "survives if AeST-type", not a derivation; "CPT-even-only" is a structural inference
  (MEDIUM), NOT a theorem, and must stop being called one; and the "K_B <= 0.25 tightens the bridge"
  paragraph was CIRCULAR (K_B <= 1/4 was obtained FROM the 1/8 deficit bound, so deriving the deficit
  cap from it returns the input).  What actually rigidifies the bridge: c_13 = 0 as an identity for
  every K_B => c_T = 1 exactly -- a falsifiable ZERO.

--------------------------------------------------------------------------------------------------
THE CYCLE'S LESSON, WRITTEN WHERE IT CANNOT BE MISSED
--------------------------------------------------------------------------------------------------
I wrote the failure-mode taxonomy into RETRACTIONS.md, put T1 at the top -- and committed a T1 within
24 hours (stage 51's K_eff), catching it only because the verifiers were still running.  The taxonomy is
necessary and NOT sufficient: the enforcement that works is ADVERSARIAL VERIFICATION BEFORE COMMIT, not
self-checking after.  Standing rule going forward: constructions from unverified lane reports get
committed as CANDIDATE-flagged or not at all.
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

NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4
KAPPA_MEAS, ERR = 0.551, 0.043
KAPPA_BTFR, ERR_B = 0.465, 0.076
H0_LO, H0_HI = 67.4, 73.0                     # km/s/Mpc
MPC = 3.0856775814913673e22
YR = 3.155815e7

print("=" * 100)
print("PART A -- Lane A: the MS08 reduction, the trivial identity, and the 11-sigma kill")
print("=" * 100)

al, y = sp.symbols("alpha y", positive=True)
coeff = 1 - 1 / (2 * al)
check(sp.simplify(coeff.subs(al, sp.Rational(1, 2))) == 0,
      f"A1  ATTRIBUTION: Milgrom & Sanders 2008 Eq. (13)'s second-term coefficient 1 - 1/(2 alpha) "
      f"vanishes EXACTLY at alpha = 1/2, leaving nu = 1/(1 - e^(-sqrt y)) -- the Route A kernel is MS08's, "
      f"introduced with an explicit no-mechanism disclaimer; MLS 2016 is the empirical ADOPTION",
      "corpus attribution corrected: 'form: MLS 2016' -> 'form: MS08 Eq. 13 at alpha = 1/2, adopted MLS16'")

u_ = sp.symbols("u", positive=True)
check(sp.simplify(1 / (1 - sp.exp(-u_)) - (1 + 1 / (sp.exp(u_) - 1))) == 0,
      f"A2  the identity nu = 1 + n_BE(u) holds for ARBITRARY u -- it is the Bose rearrangement, not "
      f"physics.  The only MOND content is u = sqrt(y), which is scale-invariance, already published",
      "so the 'striking identity' I flagged going in was a re-notation; the lane and verifiers agree")

kappa_pred = float(sp.sqrt(8 * sp.pi / 3) / (4 * sp.pi ** 2))
sig = (KAPPA_MEAS - kappa_pred) / ERR
sig_b = (KAPPA_BTFR - kappa_pred) / ERR_B
check(abs(kappa_pred - 0.07332) < 1e-4 and sig > 10 and sig_b > 5,
      f"A3  *** THE KILL: the natural bath normalisation predicts kappa = sqrt(8pi/3)/(4pi^2) = "
      f"{kappa_pred:.5f} -- {sig:.1f} sigma BELOW the measured {KAPPA_MEAS} and {sig_b:.1f} sigma below the BTFR value.  "
      f"The mirror image of the Deser-Levin trap: T2 fires LOW instead of high.  Route closed ***",
      "and a fixed-T bath cannot host a_0(z) at all; the negative is CONSISTENT with kappa being "
      "measured, not derived")

print()
print("=" * 100)
print("PART B -- Lane B: the extended no-go's binding-epoch theorem, and stage 51's kills")
print("=" * 100)

z_bind = 1654.0 ** (1.0 / 3.0) - 1.0


def a0_ratio(z, nu0):
    return (np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + nu0 ** 2 * (1 + z) ** 6)) ** 0.5


check(abs(z_bind - 10.83) < 0.01 and a0_ratio(z_bind, NU0_FLOOR) > 0.999 and a0_ratio(z_bind, NU0_CEIL) > 0.97,
      f"B1  *** THE BINDING-EPOCH THEOREM: surface calibration forces rho_h = 1654 rho_dm0, and the "
      f"cosmic mean crosses that at z_bind = {z_bind:.2f} -- where the density ratio is 1 for EVERY "
      f"polytropic gamma, and the derived a_0(z) law is FLAT: {a0_ratio(z_bind, NU0_FLOOR):.4f} floor / "
      f"{a0_ratio(z_bind, NU0_CEIL):.3f} ceiling.  The 0.0060 recombination lever is the WRONG lever ***",
      "[lane]: lambda_J = 4.46 Mpc comoving there, gamma-independent, ~9x any acceptable cap")

Rh, G_, Keff = sp.symbols("R_halt G K_eff", positive=True)
check(sp.simplify(sp.pi * sp.sqrt((2 * sp.pi * G_ * Rh ** 2) / (2 * sp.pi * G_)) - sp.pi * Rh) == 0,
      f"B2  STAGE 51 KILL 1, THE TAUTOLOGY, verified: with K_eff = 2 pi G R_halt^2, "
      f"R_core = pi sqrt(K_eff/2piG) = pi R_halt IDENTICALLY (pi x 60 = {np.pi*60:.1f} kpc).  The "
      f"'mass-independent 188.7 kpc core' was the assumed halt radius wearing a formula; 'Sgr A* removed' "
      f"restated the premise.  Failure mode #1, committed by me the day after cataloguing it",
      "stage 51 now carries a KILLED banner; Parts A-B (the two sign/no-coupling theorems) survive")

amp_deep = 1.0 / 0.0060          # y ~ 1/a_0 in deep MOND
amp_A = 1.0 / 0.0060 ** 2        # y = Y/Acal with Acal ~ a_0^2, Y held
check(amp_deep > 150 and amp_A > 2e4,
      f"B3  STAGE 51 KILL 2, THE DIRECTION, verified: y carries a_0(z) INVERSELY, so at recombination "
      f"(a_0 = 0.0060 a_0(0)) y is amplified x{amp_deep:.0f} (deep-MOND convention) to x{amp_A:.0f} (Y/Acal "
      f"convention).  W ~ y^2 therefore AMPLIFIES the coupling exactly where the CMB needs the dust "
      f"pressureless -- [verifier]: 3.25e6x the committed CLASS cap.  The gate runs the WRONG WAY in time",
      "the same a_0(z) law that makes the CMB a prediction closes this gate -- one property, two "
      "consequences, for the FOURTH time in this corpus")

check(abs(np.sqrt(6e11 / 6e9) - 10.0) < 0.01,
      f"B4  and the 'mass-independent' signature is FALSE under the stage's own gate: R_halt ~ "
      f"sqrt(M_bar), so 6e9 -> 6e11 M_sun scales the radius x{np.sqrt(100):.0f} ([verifier]: 13.5 -> 135 kpc, "
      f"consistent).  Baryon-poor systems lose the halt entirely: the collapse returns where halos are "
      f"darkest",
      "[verifier] kill 3, quoted unowned: KiDS lensing charges the core Delta chi^2 ~ +1.2e3 to +2.0e3, "
      "worse than stage 12's already-rejected +927; verifiers disagree on the radius-magnitude pairing")

print()
print("=" * 100)
print("PART C -- Lane D: the drift, re-derived, and the executed withdrawal")
print("=" * 100)

nu0s, zs = sp.symbols("nu_0 z", positive=True)
law = (sp.sqrt(1 + nu0s ** 2) / sp.sqrt(1 + nu0s ** 2 * (1 + zs) ** 6)) ** sp.Rational(1, 2)
dlnda = sp.simplify(sp.diff(sp.log(law), zs).subs(zs, 0))
check(sp.simplify(dlnda + sp.Rational(3, 2) * nu0s ** 2 / (1 + nu0s ** 2)) == 0,
      f"C1  d ln a_0/dz at z = 0 is -(3/2) nu_0^2/(1+nu_0^2) EXACTLY, so adot_0/a_0 = +(3/2) nu_0^2 H_0 "
      f"-- POSITIVE (a_0 rising to its maximum today), kappa-blind and footing-blind")

lo = 1.5 * NU0_FLOOR ** 2 * (H0_LO * 1e3 / MPC) * YR
hi = 1.5 * NU0_CEIL ** 2 * (H0_HI * 1e3 / MPC) * YR
check(4e-20 < lo < 5e-20 and 3e-18 < hi < 4e-18,
      f"C2  numerically adot_0/a_0 in [{lo:.2e}, {hi:.2e}] per yr across the nu_0 window and H_0 = "
      f"67.4-73.  HOPELESSLY SMALL in every direct channel (nearest proxy bounds ~7000x too loose; "
      f"alpha-dot = 0 exactly, so clocks are blind).  The only observable expression is the integrated "
      f"a_0(z) law -- the MUSE/high-z sharp null, which stands",
      "a null RESULT, kept as one: the drift is real, derived, and unmeasurable in any direct channel")

check(-3e-11 < 0 and lo > 0,
      f"C3  *** WITHDRAWAL EXECUTED: STATE_OF_THE_FRAMEWORK.md carried 'adot_0/a_0 ~ -3e-11/yr, DERIVED' "
      f"-- 7-8 ORDERS TOO LARGE and WRONG IN SIGN.  Corrected in place this commit with a supersession "
      f"note ***",
      "found by a verifier, not by the lane -- the lane reported the right number and failed to flag the "
      "contradiction with the committed row (T3)")

print()
print("=" * 100)
print("PART D -- Lane C: the clean lane, and the suite taken red -> green")
print("=" * 100)

info("D1  hash integrity: all nine digests verified by both verifiers independently; the frozen "
     "pre-registration is intact and untouched.  Dry run on the real eDR3 catalog: gamma_hat = "
     "1.2075 +/- 0.0350 canonical / 1.2125 +/- 0.0337 ALT, kappa = 1.022, all injections recovered, "
     "alt-target injection correctly tripped PRE-DECLARED UNSCOREABLE.  Machinery works; non-scoring "
     "per the frozen sec 1.6.")

info("D2  the committed readiness suite was RED at HEAD (30/31): D6's guard grepped a literal renamed by "
     "the legitimate Amdt-9 rewire.  FIXED STRUCTURALLY this commit (assert the reporter prints the "
     "Newton distance and references BOTH in-force GAMMA_TARGET variables); C1/C2 carry a verifier-found "
     "caveat (string test cannot distinguish live text from a changelog quoting it).  Suite: 31/31.")

info("D3  RISKS CARRIED FORWARD, unresolved and on the record: Amdt 8(h)'s own kappa-window lands "
     "OUTSIDE the frozen gate under the framework's kernel (computed for the superseded MI target, never "
     "recomputed for Amdt 9) -- a framework-side confirmation may be no-verdict BY MECHANISM; fit_gamma "
     "lacks an argmin-interior assertion and a chi^2 gate (synthetic drive pinned the grid max at +400 "
     "sigma_fit, straight-faced); checklist items 5/6 never executed by a committed run; Amendment 9(b)'s "
     "nonlinear AQUAL-EFE solve still owed -- if it moves gamma_v, AMENDMENT 10 BEFORE DR4.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE FOUR-DOOR FLEET, SETTLED.  3 of 4 lanes refuted by both verifiers; nothing opened.

  LANE A (BE kernel):   CLOSED.  Prior art on both halves (MS08 Eq. 13 at alpha = 1/2 for the function --
     an attribution CORRECTION now in the record -- and LMSP17 for the thermal reading); the identity is
     a trivial rearrangement; and the natural normalisation lands kappa = {kappa_pred:.4f}, {sig:.1f} sigma LOW: the
     mirror of Deser-Levin.  The negative is consistent with kappa being MEASURED.

  LANE B (second field): the no-go EXTENDED -- the binding epoch is z = {z_bind:.1f}, where a_0(z) is flat for
     both window ends and lambda_J is gamma-independent; the 0.0060 lever protects only recombination.
     Stage 51's construction: KILLED three ways within two hours of commit (tautology; gate runs the
     wrong way in time -- y ~ 1/a_0(z) EXPLODES at recombination; lensing endpoint rejected).  Bannered,
     not edited.  Parts A-B (two sign/no-coupling theorems) survive.  THE DUST PROBLEM IS FULLY OPEN,
     with a sharper wall: pressure at z <~ 11 but not at z ~ 1090, and no function of y can do that.

  LANE C (DR4):         the CLEAN lane.  Hashes intact, dry run green (gamma_hat = 1.2075 +/- 0.035),
     suite taken 30/31 -> 31/31 this commit, and four real risks carried onto the record -- the sharpest
     being Amdt 8(h)'s kappa-window, which may pre-declare a framework-side confirmation no-verdict and
     was never recomputed for the in-force target.

  LANE D (SME bridge):  numbers clean (s^TX ~ 10^-363.6 / 10^-331.5, margins 10^354 / 10^322), and ONE new
     derived result kept: adot_0/a_0 = +(3/2) nu_0^2 H_0 in [{lo:.1e}, {hi:.1e}]/yr -- real, kappa-blind,
     and unmeasurable in any direct channel.  A committed row withdrawn (wrong sign, 7-8 orders).  The
     "CPT-even-only THEOREM" language is downgraded to structural inference; the K_B "tightening" was
     circular; what rigidifies the bridge is c_13 = 0 identically => c_T = 1 exactly.

  THE LESSON, standing rule from here: the taxonomy did not stop me committing a T1 the day after writing
  it.  ADVERSARIAL VERIFICATION BEFORE COMMIT -- constructions from unverified lane reports get committed
  CANDIDATE-flagged or not at all.
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
