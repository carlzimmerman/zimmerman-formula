#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage21_muse_msa_reexam_derived_law_2026.py
===========================================
THE MUSE / MSA-3D RE-EXAMINATION AGAINST THE DERIVED a_0(z) LAW -- non-claim 2e's second owed item.

Every published grade of the a_0(z) front was earned against the WITHDRAWN CPL-dressed law
(bump +6% at z ~ 0.4, decline to 0.74 at z = 3).  The v7 derived law is a different object:
CONSTANT to <1% through z <= 5, transition at z_t in [17, 35].  This stage re-grades the three
confrontations that carried verdicts -- Ciocan MUSE-DARK III, MSA-3D, and the 2026-07-25 joint fork
likelihood -- and prices, AGAINST INTEREST, the three defenses the framework forfeits by the change.

HEADLINES:
  * the MUSE tension PERSISTS but re-grades from FRAMEWORK-DISTINCTIVE-WORST (the old declining
    branch: wrong sign, ~16σ raw, "needs the MOST ΛCDM artifact of the three") to SHARED-WITH-ALL-
    CONSTANT-a_0-MOND (~15σ raw, ~2-3σ after the genuinely shared ΛCDM assembly drift);
  * in the committed joint likelihood the framework's branch RELABELS M-DEC -> M-FLAT, i.e. from
    the branch that needed drift p = 1.22-1.43 to the branch that needs exactly the drift MSA-3D
    itself measures (p = 1.22) -- and whose near-unfalsifiability critique INVERTS into the
    framework's sharpest new prediction;
  * MSA-3D re-grades from WEAK-TENSION/WATCH to CONSISTENT (the genuine trend is 1.1σ from the
    flat line the derived law predicts);
  * and the framework now has SKIN IN THE GAME: zero evolution below z ~ 5 at the <1% level is a
    sharp null -- a robust nonzero a_0 evolution at z < 5, EITHER SIGN, falsifies the v7 law
    outright.  The old law could bend; this one cannot.

FORFEITED (priced in Part E, not buried): the z ~ 0.4 bump defense, the 3.1-4.2σ DESI cosmology
tailwind, and the z ~ 2-3 distinctive-decline discriminator.  Plus one NEW exposure: full-strength
MOND through cosmic dawn.
"""

import sys
import mpmath as mp

mp.mp.dps = 25
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


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ---- the laws -----------------------------------------------------------------------------------
W0, WA = mp.mpf("-0.75"), mp.mpf("-0.86")         # the WITHDRAWN CPL dressing (comparison only)
NU0_FLOOR, NU0_CEIL = mp.mpf("2.14e-5"), mp.mpf("1.77e-4")


def a0r_cpl(z):
    z = mp.mpf(z)
    return (1 + z) ** (mp.mpf("1.5") * (1 + W0 + WA)) * mp.e ** (-mp.mpf("1.5") * WA * z / (1 + z))


def a0r_derived(z, nu0):
    z = mp.mpf(z)
    nu = nu0 * (1 + z) ** 3
    return (mp.sqrt(1 + nu0 ** 2) / mp.sqrt(1 + nu ** 2)) ** mp.mpf("0.5")


# ---- the data (committed values, real papers) ---------------------------------------------------
# Ciocan MUSE-DARK III (A&A 709, L16; arXiv:2604.22613): a0(z) = a0(0) + a1 z over 0.5 < z < 1.44
A1_MUSE, A1_ERR = mp.mpf("1.59"), mp.mpf("0.105")      # x 1e-10 m/s^2 per unit z; a0(0) = 1.00+-0.04
Z_LO, Z_HI = mp.mpf("0.5"), mp.mpf("1.44")
# Magneticum LCDM assembly drift (Mayer+2023): apparent a0 rise with NO fundamental a0
A1_DRIFT = mp.mpf("0.80")                               # x 1e-10 per z (~x3 to z=2.3), committed
# MSA-3D after the committed selection decomposition: genuine trend +0.91 [+0.05, +1.63]
MSA_TREND, MSA_SIG = mp.mpf("0.91"), mp.mpf("0.79")

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the Ciocan slope test, re-run branch by branch")
print("=" * 100)


def model_slope(law):
    """predicted a1 over the MUSE window, in Ciocan's units (anchor a0(0) = 1.0e-10)."""
    return (law(Z_HI) - law(Z_LO)) / (Z_HI - Z_LO)


s_cpl = model_slope(a0r_cpl)
s_der_f = model_slope(lambda z: a0r_derived(z, NU0_FLOOR))
s_der_c = model_slope(lambda z: a0r_derived(z, NU0_CEIL))

t_cpl = (A1_MUSE - s_cpl) / A1_ERR
t_flat = A1_MUSE / A1_ERR
t_der = (A1_MUSE - s_der_c) / A1_ERR

print(f"\n   branch                  predicted a1 [1e-10/z]    raw tension vs Ciocan")
print(f"   withdrawn CPL (old)          {sig(s_cpl, 3):>8s}                {sig(t_cpl, 3)} sigma  (WRONG SIGN)")
print(f"   derived law (v7)             {sig(s_der_c, 2):>8s}                {sig(t_der, 3)} sigma")
print(f"   exactly flat                 0.0                     {sig(t_flat, 3)} sigma")

check(abs(s_der_c) < mp.mpf("1e-3") and abs(t_der - t_flat) < mp.mpf("0.02"),
      f"A1  the derived law IS the flat branch on the MUSE window: predicted slope |a1| < 1e-3 at "
      f"the window ceiling (vs the withdrawn CPL's {sig(s_cpl, 3)}), so its raw tension equals the "
      f"flat branch's {sig(t_flat, 3)} sigma",
      "the re-grade is exact, not approximate: constant to <0.01% over 0.5 < z < 1.44")

check(t_cpl > t_flat,
      f"A2  and the WRONG-SIGN liability is GONE: the withdrawn declining branch was {sig(t_cpl, 3)} "
      f"sigma -- the WORST of the branches -- because it predicted a_0 FALLING across a window where "
      f"the fit rises.  The derived law improves the raw number by {sig(t_cpl - t_flat, 2)} sigma and, "
      f"more importantly, the residual tension is now IDENTICAL to standard constant-a_0 MOND's: "
      f"REAL but NOT framework-distinctive",
      "the framework no longer carries a private liability on this front; it carries MOND's")

# the genuinely-shared LCDM drift, folded transparently
for frac in ("0.5", "0.3"):
    f = mp.mpf(frac)
    resid = (A1_MUSE - A1_DRIFT) / mp.sqrt(A1_ERR ** 2 + (f * A1_DRIFT) ** 2)
    info(f"A3  drift-folded residual at {sig(100 * f, 2)}% drift uncertainty: "
         f"({sig(A1_MUSE, 3)} - {sig(A1_DRIFT, 2)})/sqrt({sig(A1_ERR, 3)}^2 + {sig(f * A1_DRIFT, 2)}^2) "
         f"= {sig(resid, 3)} sigma", "")
check((A1_MUSE - A1_DRIFT) / mp.sqrt(A1_ERR ** 2 + (mp.mpf("0.3") * A1_DRIFT) ** 2) < 3.1,
      "A4  after subtracting the Magneticum LCDM-assembly drift (Mayer+2023: apparent a_0 rises x3 "
      "to z = 2.3 with NO fundamental a_0 -- a systematic SHARED by every branch, not special "
      "pleading) the residual is ~1.9-3.0 sigma by this transparent folding; the banked record "
      "carries ~3-5 sigma from a stricter folding.  EITHER WAY: real, unresolved, and now owned "
      "jointly with all of constant-a_0 MOND",
      "do NOT quote the raw 15 sigma without the drift, and do NOT quote ~0 sigma either -- the "
      "committed standing (2026-06-20) stands, re-attributed")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the joint fork likelihood: the framework CHANGES BRANCH")
print("=" * 100)

info("B1  the committed 2026-07-25 joint likelihood (a0z_fork_likelihood_2026.py, 11 constraints, "
     "three zero-parameter laws) graded M-DEC (the withdrawn declining law), M-FLAT (constant), "
     "M-RISE (cH E(z)).  Its committed findings, RE-ATTRIBUTED under v7:")
info("B2  *** the framework's branch is now M-FLAT ***, and the committed numbers say: M-FLAT needs "
     "drift p = 1.22 -- EXACTLY the apparent-rise component MSA-3D itself measures -- where M-DEC "
     "needed p = 1.22-1.43, THE MOST ARTIFACT OF THE THREE (a recorded mark against the old law "
     "that the derived law simply deletes); at that measured prior M-FLAT beat M-DEC 59.5:1")
info("B3  M-RISE (the alt-footing rising law) fits the single Ciocan point best (needs only "
     "p = 0.197) but is excluded by everything else on the front -- Milgrom 2017's (1+z)^1.5 "
     "exclusion, the 17x cluster offset with no z-trend (Tian+2024, eRASS1), the disk BTFR null -- "
     "AND, since stage 17, corresponds to NO scalar of the v7 action.  It is no longer a live rival "
     "inside the framework; it survives only as an external hypothesis")
info("B4  and the committed likelihood's sharpest CRITICISM inverts: it found that if M-FLAT is "
     "true, no single z >= 1.5 measurement could ever clear 20:1 against M-DEC (a null is always "
     "absorbable by M-DEC + slightly more drift) -- a near-unfalsifiability problem FOR THE OLD "
     "LAW.  With M-DEC withdrawn, the absorbing branch is gone: the derived law predicts ZERO "
     "evolution below z ~ 5 at <1%, and any robust nonzero evolution, EITHER SIGN, kills it.")

check(a0r_derived(3, NU0_CEIL) > mp.mpf("0.9999") and a0r_derived(5, NU0_CEIL) > mp.mpf("0.999"),
      f"B5  the sharp null, quantified: a_0(3)/a_0(0) = {sig(a0r_derived(3, NU0_CEIL), 5)} and "
      f"a_0(5)/a_0(0) = {sig(a0r_derived(5, NU0_CEIL), 5)} at the window CEILING (floor is flatter "
      f"still) -- against the withdrawn law's 0.74 at z = 3",
      "the framework now has skin in the game on the direct-datum front: MUSE's rise, if it ever "
      "survives a homogeneous drift-modeled pipeline, FALSIFIES the v7 law outright")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- MSA-3D, re-graded")
print("=" * 100)

t_msa = MSA_TREND / MSA_SIG
check(t_msa < mp.mpf("1.5"),
      f"C1  MSA-3D's genuine trend (+0.91 [+0.05, +1.63] after the committed selection "
      f"decomposition -- the raw +2.13 was acceleration-selection-confounded) sits {sig(t_msa, 3)} "
      f"sigma from the flat line the derived law predicts: *** WEAK-TENSION/WATCH re-grades to "
      f"CONSISTENT ***",
      "the paper's own statement -- f_DM has 'no clear redshift trend' -- is now the framework's "
      "prediction verbatim")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the Jeanneau deep refit and the high-z BTFR fork, re-attributed")
print("=" * 100)

info("D1  the committed Jeanneau+26 deep refit (N = 61 lensed dwarfs at g_bar < 0.5 a_0) measured "
     "Delta b = +0.140 +- 0.276 against canonical 0.000 / ALT-rising -0.243.  The derived law "
     "predicts 0.000 EXACTLY (constant a_0), i.e. the 0.51-sigma-consistent branch -- unchanged in "
     "number, sharpened in status: it is no longer 'canonical branch of a fork', it is the action's "
     "output.  The ALT-side 1.0-1.4 sigma lean targets a law that stage 17 removed from the theory.")

info("D2  the cosmic-noon BTFR systematics floor (~0.06 dex, AD-degenerate) made declining-vs-"
     "constant undecidable there; under the derived law there is nothing to decide below z ~ 5 -- "
     "the mid-2030s ELT/HARMONI declining-a_0 target (a_0(3) = 0.74) NO LONGER EXISTS.  Priced in "
     "Part E as a forfeited discriminator, credited here as a dissolved liability.")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- what the derived law FORFEITS, priced against interest")
print("=" * 100)

check(a0r_cpl(mp.mpf("0.405")) > mp.mpf("1.05") and abs(a0r_derived(mp.mpf("0.405"), NU0_CEIL) - 1) < mp.mpf("1e-5"),
      f"E1  FORFEIT 1 -- the bump defense: the old law rose {sig(100 * (a0r_cpl(mp.mpf('0.405')) - 1), 3)}% "
      f"at z = 0.405, which let a modest low-z rise be read as CONSISTENT.  The derived law is flat "
      f"there to 1e-5: any robust low-z rise now counts fully against the framework, same as against "
      f"all constant-a_0 MOND",
      "a defense the framework USED in the 2026-06-06 reframing, now gone -- stated, not hidden")

info("E2  FORFEIT 2 -- the DESI tailwind: the old law inherited DESI's evolving w and wore the "
     "3.1-4.2 sigma evolving-DE preference as a 'cosmology-leg tailwind'.  The derived law does not "
     "inherit w(z) AT ALL -- a_0(z) is set by the sector's own charge, whatever DE does.  The "
     "tailwind is FORFEITED as support... and the hostage dies with it: 'w -> -1 dissolves the "
     "framework to constant MOND' is no longer a risk, it is the PREDICTION.  DESI DR3 stops being "
     "the gate for a_0(z); it remains relevant only to the standing w = -1-exact vs evolving-DE "
     "tension (non-claim 2e-ii), which is unchanged.")

r10_c, r10_f = a0r_derived(10, NU0_CEIL), a0r_derived(10, NU0_FLOOR)
check(a0r_cpl(10) < mp.mpf("0.40") and r10_c > mp.mpf("0.98"),
      f"E3  NEW EXPOSURE -- cosmic dawn at full strength: the old law had a_0(10) = "
      f"{sig(a0r_cpl(10), 3)}; the derived law has a_0(10) = {sig(r10_c, 4)}-{sig(r10_f, 4)}.  "
      f"MOND now runs at FULL strength through z = 5-15, where Nusser 2002's over-production "
      f"concern lives -- the committed 'declining a_0 is favorable/neutral for JWST' read is "
      f"WITHDRAWN for the derived law and the early-structure front needs its own quantitative "
      f"confrontation",
      "against interest and unpriced tonight: flagged as the derived law's newest open front, "
      "with the transition z_t in [17, 35] sitting exactly in the 21-cm / first-structure window")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE MUSE / MSA-3D RE-EXAM IS DONE.  Under the derived law:

  1. MUSE: the tension PERSISTS ({sig(t_flat, 3)} sigma raw, ~2-3 sigma after the shared LCDM
     assembly drift by transparent folding; banked stricter folding ~3-5 sigma) but re-grades from
     FRAMEWORK-DISTINCTIVE-WORST (wrong-sign decline, {sig(t_cpl, 3)} sigma) to SHARED-WITH-ALL-
     CONSTANT-a_0-MOND.  The framework's private liability on this front is deleted.

  2. THE JOINT LIKELIHOOD RELABELS: the framework's branch is now M-FLAT -- the branch needing
     exactly the drift MSA-3D measures (p = 1.22), not the most-artifact branch (M-DEC, 1.22-1.43).
     The old near-unfalsifiability critique inverts into the sharpest new prediction: ZERO
     evolution below z ~ 5, falsified by any robust detection of a_0 evolution there, either sign.

  3. MSA-3D: WEAK-TENSION/WATCH -> CONSISTENT ({sig(t_msa, 3)} sigma from flat).
     Jeanneau deep refit: the consistent branch (0.51 sigma) is now the action's own output.

  4. FORFEITED, priced: the z ~ 0.4 bump defense; the 3.1-4.2 sigma DESI tailwind (and with it
     the w -> -1 hostage -- dissolution is now the prediction); the z ~ 2-3 declining
     discriminator.  NEW EXPOSURE: full-strength MOND through cosmic dawn (a_0(10) = {sig(r10_c, 3)}
     vs the old 0.36), Nusser over-production unpriced, z_t in the 21-cm window.

  Non-claim 2e's MUSE/MSA-3D re-examination is CLOSED.  Remaining owed: the covariant SVT
  decomposition -- and the new cosmic-dawn confrontation opened by E3.
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
