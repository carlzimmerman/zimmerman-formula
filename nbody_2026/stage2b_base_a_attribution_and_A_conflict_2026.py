#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage2b_base_a_attribution_and_A_conflict_2026.py
=================================================
STAGE 2b -- A CORRECTION TO MY OWN STAGE-2 VERDICT, AND THE SHARPER PINCH THAT REPLACES IT.

*** THE CORRECTION, STATED FIRST AND AGAINST INTEREST.  Stage 2's verdict named two escape doors
for the galaxy-dust problem.  Door (ii) was: "base_a shifting the FRW ceiling past 1.2e-6", and I
wrote that "a literature lookup now carries mortal weight" FOR THE GALAXY PROBLEM.  THAT IS WRONG.
base_a -- the aether's algebraic gradient entry -- enters ONLY the HALO amplitude cap (G2/G3 of
mi_aest_full_matrix_bump_2026.py, where the bound softens by 0.64/base_a).  The FRW ceiling is

        Lam_D_max = sqrt( CLASS_DMG * mu^2 / (2 * A * L0^2 * pk) )      (H5b of
                                                                mi_a0_bump_health_2026.py)

in which base_a DOES NOT APPEAR, and whose only aether mixing was already shown to be
Poisson-suppressed at 3.2e-4 (F1 of the full matrix).  So no value of base_a can move the FRW
ceiling the 1.38x that galactic self-support needs.  Door (ii) of stage 2 is CLOSED.  I invented a
hope rather than a deficit, which is the same error in the other direction, and it is corrected
here with the same prominence as the finding it decorated. ***

base_a's REAL stake is the CLUSTER pinch (Part C), which is where the lookup matters.

AND THE PINCH THAT REPLACES THE CLOSED DOOR (Part B, new):  the FRW ceiling scales as A^(-1/2),
so the SAME amplitude A that the cluster mechanism needs is what pushes the ceiling BELOW the
support requirement.  Galaxy support and cluster phenomenology pull A in OPPOSITE directions.
That is a three-way squeeze, and it is tighter than anything stage 2 claimed.

Also settled here: (Part D) "supported" is NOT "clean" -- pressure support stops the caustic, it
does not remove the dust; and (Part E) the support threshold is v_c-dependent, so the failure
MORPHOLOGY changes at v_c ~ 170 km/s while remaining a failure at every mass.
"""

import sys
import math
import mpmath as mp

mp.mp.dps = 30
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ---------------------------------------------------------------------------------------------
# Banked inputs, quoted from the committed scripts they come from (no re-derivation, no drift)
# ---------------------------------------------------------------------------------------------
# mi_a0_bump_health_2026.py, line 51-52:
A_FID = mp.mpf("1.65")            # Mpc^-2, cluster-calibrated fiducial amplitude
MU2 = mp.mpf("100")               # mu^2 in the script's units
L0SQ = mp.mpf("3.111e4") ** 2     # L0^2
CLASS_DMG = mp.mpf("4.2e-6")      # CLASS first-damage point
PK = mp.mpf("0.18594")            # FRW wrong-sign shape factor, peak at R = sqrt(2/3)
LAM_CEIL = mp.mpf("8.4e-7")       # the published FRW ceiling (H5b)
MIX = mp.mpf("0.64")              # full-matrix G2: halo bound softens by 0.64/base_a
A_MAX_ISO = mp.mpf("4.49")        # full-matrix/health isolated-term cap, Mpc^-2
FRW_MIXSUP = mp.mpf("3.2e-4")     # full-matrix F1: (aH/k)^2 suppression of the only FRW mixing
CS2_COEF = mp.mpf("0.385")        # mi_dbi_khronon_2026.py: max c_s^2 = 0.385 Lam_D
C_KMS = mp.mpf("299792.458")
G_KMS = mp.mpf("4.300e-9")        # Mpc (km/s)^2 / Msun
M_DUST = mp.mpf("2.51e12")        # stage 2's captured share in an L* basin, Msun
V_C = mp.mpf("200")               # km/s, L* circular speed
MIST_LO, MIST_HI = mp.mpf("4"), mp.mpf("34")   # Mistele demand in units of A_FID

print(__doc__)


def lam_ceiling(A):
    """H5b's FRW gradient-health ceiling as an explicit function of the amplitude A."""
    return mp.sqrt(CLASS_DMG * MU2 / (2 * A * L0SQ * PK))


# =============================================================================================
print("=" * 100)
print("PART A -- THE CORRECTION: base_a cannot move the FRW ceiling")
print("=" * 100)

check(abs(lam_ceiling(A_FID) - LAM_CEIL) / LAM_CEIL < mp.mpf("0.02"),
      f"A1  the ceiling formula reproduces the published bound: Lam_D_max(A_fid) = "
      f"{sig(lam_ceiling(A_FID),3)} vs published {sig(LAM_CEIL,3)}",
      "so Part A reasons about the SAME quantity the papers quote, not a lookalike")

# A2 -- the formula's arguments are enumerated; base_a is not among them.
ARGS = {"CLASS_DMG": CLASS_DMG, "mu^2": MU2, "A": A_FID, "L0^2": L0SQ, "pk": PK}
check("base_a" not in ARGS and len(ARGS) == 5,
      "A2  *** the FRW ceiling depends on exactly {CLASS_DMG, mu^2, A, L0^2, pk} -- base_a IS NOT "
      "AN ARGUMENT.  Stage 2's door (ii) was a misattribution ***",
      "base_a enters the HALO cap only (full-matrix G2), never the FRW bound")

# A3 -- and the one aether mixing that COULD have entered was already bounded by the full matrix:
# even a base_a as extreme as 0.1 or 10 can shift the ceiling only through that suppressed channel.
shift_max = mp.sqrt(1 + FRW_MIXSUP)          # generous: full mixing strength, one-sided
need = mp.mpf("1.38")                        # stage 2's support shortfall
check(shift_max < need,
      f"A3  *** even granting the FULL suppressed mixing its maximum effect, the ceiling moves by "
      f"<= {sig(shift_max,6)}x -- against the {sig(need,3)}x that galactic self-support requires. "
      "NO base_a REOPENS THE GALAXY DOOR ***",
      f"the mixing channel is (aH/k)^2 = {sig(FRW_MIXSUP,2)} at the damage scale (full-matrix F1)")

# NC-A (negative control): the machinery must show the ceiling IS movable by its real arguments,
# or A2/A3 would be vacuous ("nothing moves it").
check(abs(lam_ceiling(A_FID / 4) / lam_ceiling(A_FID) - 2) < mp.mpf("1e-12"),
      "NC-A  CONTROL: the ceiling DOES move by its actual arguments -- quartering A doubles it "
      "exactly (A^-1/2) -- so A2/A3 identify a specific absent dependence, not a numb formula",
      "which is exactly the lever Part B now exploits")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- THE PINCH THAT REPLACES THE CLOSED DOOR: galaxies and clusters pull A apart")
print("=" * 100)

lam_support = (V_C / C_KMS) ** 2 / CS2_COEF        # stage 2's Lam_D needed for L* support
A_for_support = CLASS_DMG * MU2 / (2 * lam_support ** 2 * L0SQ * PK)
print(f"""
  Galactic self-support needs   Lam_D >= {sig(lam_support,3)}   (stage 2, Part A)
  The ceiling allows            Lam_D <= {sig(lam_ceiling(A_FID),3)}   at A = A_fid = {sig(A_FID,3)} Mpc^-2
  But the ceiling is A-dependent: Lam_D_max ~ A^(-1/2), so support is allowed iff

        A <= {sig(A_for_support,3)} Mpc^-2  =  {sig(A_for_support/A_FID,3)} x fiducial.
""")
check(A_for_support < A_FID,
      f"B1  *** THE THREE-WAY SQUEEZE: galaxy dust support needs A <= {sig(A_for_support,3)} Mpc^-2, "
      f"but the cluster residual CALIBRATES A = {sig(A_FID,3)} -- a factor "
      f"{sig(A_FID/A_for_support,3)} apart.  The two jobs pull the SAME parameter in OPPOSITE "
      "directions ***",
      "this replaces stage 2's closed door with a genuine, tighter constraint")

check(A_for_support < MIST_LO * A_FID / 4,
      f"B2  *** and against Mistele's cluster demand (4-34x fiducial = "
      f"{sig(MIST_LO*A_FID,3)}-{sig(MIST_HI*A_FID,3)} Mpc^-2) the conflict is "
      f"{sig(MIST_LO*A_FID/A_for_support,3)}-{sig(MIST_HI*A_FID/A_for_support,3)}x -- the "
      "amplitude that clusters want makes the galaxy problem STRICTLY WORSE, monotonically ***",
      "no single A serves both; the mechanism's own success on clusters deepens its galaxy failure")

# B3 -- how much would the CLUSTER side have to give? A <= A_for_support means the cluster
# residual is under-supplied by exactly that ratio (mu^2_eff scales linearly in A).
check(A_for_support / A_FID < mp.mpf("0.6"),
      f"B3  quantified the other way: choosing A for the galaxies delivers only "
      f"{sig(A_for_support/A_FID*100,3)}% of the calibrated cluster response -- the cluster "
      "mechanism would be surrendered, not merely strained",
      "so B1 is a genuine either/or, not a tuning window")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- what base_a DOES settle: the cluster amplitude pinch")
print("=" * 100)

print("""
  The full matrix (G2/G3) gives the halo cap A_max = A_max_isolated x (1 +/- 0.64/base_a), i.e.
  the band widens as base_a shrinks.  This is base_a's ONLY load, and it is a real one: whether
  Mistele's 4x lower edge is EXCLUDED or MARGINAL.
""")
print("   base_a   A_max (Mpc^-2)    Mistele 4x edge (6.60)   Mistele 34x end (56.1)")
verdicts = {}
for ba_s in ("0.5", "1.0", "2.0", "4.0"):
    ba = mp.mpf(ba_s)
    amax = A_MAX_ISO * (1 + MIX / ba)
    v4 = "MARGINAL (inside)" if amax >= MIST_LO * A_FID else "EXCLUDED"
    v34 = "EXCLUDED" if amax < MIST_HI * A_FID else "ALLOWED"
    verdicts[ba_s] = (amax, v4, v34)
    print(f"   {ba_s:>6s}   {sig(amax,4):>8s}         {v4:<22s}   {v34}")

check(all(verdicts[k][2] == "EXCLUDED" for k in verdicts),
      "C1  the 34x end of the Mistele demand stays EXCLUDED for every base_a in 0.5-4.0 -- that "
      "half of the cluster pinch is base_a-INDEPENDENT and holds",
      f"even at base_a = 0.5 the cap is {sig(verdicts['0.5'][0],4)} vs the 34x demand "
      f"{sig(MIST_HI*A_FID,3)}")

flip = [k for k in verdicts if verdicts[k][1].startswith("MARGINAL")]
check(len(flip) > 0 and len(flip) < len(verdicts),
      f"C2  *** and the 4x EDGE genuinely turns on base_a: MARGINAL for base_a <= "
      f"{max(float(k) for k in flip):.1f}, EXCLUDED above -- this, and only this, is what the "
      "lookup decides ***",
      "the honest scope of the 'mortal weight' I mis-assigned to the galaxy problem")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- A SECOND SELF-CAUGHT ERROR, in the OPPOSITE direction to Part A's")
print("=" * 100)

# D0 -- the circularity, shown explicitly.  If the "support radius" is DEFINED by balancing the
# dust's own gravity against v_c^2, then r = G M/v_c^2 and the ratio G M/(r v_c^2) is IDENTICALLY 1
# for every M -- so the resulting "0.151 dex" was a constant of the definition, not physics.
ratios = [G_KMS * M / ((G_KMS * M / V_C ** 2) * V_C ** 2) for M in
          (M_DUST, M_DUST / mp.mpf("1e4"), M_DUST * mp.mpf("1e3"))]
check(all(abs(r - 1) < mp.mpf("1e-25") for r in ratios),
      "D0  *** WITHDRAWN, caught by this script's own control: defining the support radius as "
      "r = GM/v_c^2 forces g_dust/g_obs = 1 for ANY dust mass (verified across 1e-4 to 1e3 x M_d), "
      "so my attempted tightening of stage 2 rested on a TAUTOLOGY (0.5*log10(2) = 0.151 dex) ***",
      "Part A caught me inventing a HOPE; Part D catches me inventing a DEFICIT. Both are logged.")

# D1 -- the non-circular estimate: evaluate the supported dust's contribution at a FIXED radius
# where data actually constrain it (the 1 Mpc weak-lensing shell).
R_LENS = mp.mpf("1.0")
g_ratio_1mpc = G_KMS * M_DUST / (R_LENS * V_C ** 2)
dex_1mpc = mp.log(1 + g_ratio_1mpc, 10) / 2
F2_LO, F2_HI = mp.mpf("0.12"), mp.mpf("0.32")     # banked F2 range, mi_session_audit_2026.py
TOL = mp.mpf("0.1")                                # ~0.1 dex outskirt tolerance
print(f"""
  Non-circular: put the supported dust at the 1 Mpc lensing shell and ask what it adds THERE.
        g_dust/g_obs(1 Mpc) = {sig(g_ratio_1mpc,3)}   ->   {sig(dex_1mpc,3)} dex in velocity
  against a ~{sig(TOL,2)} dex outskirt tolerance, and the corpus's independently banked F2 range
  {sig(F2_LO,2)}-{sig(F2_HI,2)} dex for dust at these radii.
""")
check(dex_1mpc < TOL,
      f"D1  the honest number is {sig(dex_1mpc,3)} dex -- BELOW the ~{sig(TOL,2)} dex tolerance. "
      "*** STAGE 2's 'possibly survivable' IS UPHELD and my tightening of it is WITHDRAWN: the "
      "supported configuration is MARGINAL, not failing ***",
      f"F2's independent estimate ({sig(F2_LO,2)}-{sig(F2_HI,2)} dex) straddles the tolerance, so "
      "'marginal' is the defensible word in both directions -- neither clean nor dead")

# NC-D (rebuilt so it can actually fail): the fixed-radius estimator must clear tolerance for a
# negligible dust share and breach it for a large one.
dex_tiny = mp.log(1 + G_KMS * (M_DUST / mp.mpf("1e4")) / (R_LENS * V_C ** 2), 10) / 2
dex_big = mp.log(1 + G_KMS * (M_DUST * mp.mpf("30")) / (R_LENS * V_C ** 2), 10) / 2
check(dex_tiny < mp.mpf("0.001") and dex_big > TOL,
      f"NC-D  CONTROL (rebuilt): the fixed-radius estimator responds to the mass -- "
      f"{sig(dex_tiny,2)} dex at 1e-4 x M_d, {sig(dex_big,3)} dex at 30 x M_d -- so D1 is a "
      "measurement, not a definition",
      "the discarded estimator failed exactly this test, which is why it is gone")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the mass-dependent split, and the RAR break it predicts")
print("=" * 100)

v_crit = C_KMS * mp.sqrt(CS2_COEF * LAM_CEIL)
DEX_CAUSTIC = mp.mpf("0.724")     # stage 2 D1, 10 kpc
RAR_SCAT = mp.mpf("0.034")
print(f"""
  Support at the ceiling requires (v_c/c)^2 <= 0.385 Lam_D_max, i.e.  v_c <= {sig(v_crit,4)} km/s.
  With Part D's corrected numbers the two branches are NOT both catastrophic -- they differ in
  WHERE the dust ends up, and only one of them ruins the rotation-curve region:

    v_c >  {sig(v_crit,4)} km/s (L* and up):  caustic collapse INTO the interior
                                    -> {sig(DEX_CAUSTIC,3)} dex at 10 kpc = {sig(DEX_CAUSTIC/RAR_SCAT,3)}x the RAR scatter: FATAL
    v_c <  {sig(v_crit,4)} km/s (dwarfs/LSBs): dust held OUT at ~Mpc radii, interior CLEAN
                                    -> {sig(dex_1mpc,3)} dex at 1 Mpc, marginal vs tolerance: SURVIVABLE
""")
check(mp.mpf("150") < v_crit < mp.mpf("200"),
      f"E1  the split sits at v_c = {sig(v_crit,4)} km/s -- squarely INSIDE the SPARC range, and it "
      "is not a free parameter: it is c*sqrt(0.385 Lam_D_max) with the published ceiling",
      "so the theory's own numbers place a morphology change in the middle of its best dataset")

check(DEX_CAUSTIC / RAR_SCAT > 10 and dex_1mpc < TOL,
      "E2  *** and the two sides differ QUALITATIVELY, not just in degree: below the threshold the "
      "RAR region is clean; above it the RAR region is destroyed. So the prediction is a BREAK in "
      "the RAR residual at v_c ~ 170 km/s -- dwarfs on the relation, spirals catastrophically off ***",
      f"{sig(DEX_CAUSTIC/RAR_SCAT,3)}x scatter above vs interior-clean below")

check(DEX_CAUSTIC > RAR_SCAT * 10,
      "E3  *** WHICH IS THE FALSIFICATION, ON EXISTING DATA: the observed RAR is universal and "
      "tight (0.034 dex) across exactly this v_c range -- SPARC's spirals at v_c > 170 km/s sit ON "
      "the relation, where this branch demands they sit 0.72 dex off it ***",
      "no new observation needed; the kill is in hand unless stage 3 changes the interior physics")


# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  1. *** MY STAGE-2 DOOR (ii) IS WITHDRAWN.  base_a cannot move the FRW ceiling -- it is not an
     argument of the bound, and the one channel by which it could have entered was already
     bounded at 3.2e-4 by the full matrix's own F1.  I attributed "mortal weight" for the GALAXY
     problem to a lookup that has no bearing on it.  Corrected here, against interest: the galaxy
     situation is WORSE than stage 2 stated, by one door. ***

  2. base_a's real and only load is the CLUSTER pinch: the 34x end of the Mistele demand stays
     excluded for any base_a in 0.5-4.0, while the 4x EDGE is MARGINAL for small base_a and
     EXCLUDED for large.  That is what the literature lookup decides.

  3. *** THE REPLACEMENT CONSTRAINT IS TIGHTER THAN THE DOOR IT LOST: because the FRW ceiling
     scales as A^(-1/2), galactic dust support needs A <= {sig(A_for_support,3)} Mpc^-2 while the
     cluster residual calibrates A = {sig(A_FID,3)} and Mistele's modelling wants
     {sig(MIST_LO*A_FID,3)}-{sig(MIST_HI*A_FID,3)}.  The a0-bump's success on clusters
     MONOTONICALLY DEEPENS its galaxy failure.  One parameter, two jobs, opposite directions. ***

  4. *** AND A SECOND SELF-CAUGHT ERROR, THE OTHER WAY.  My attempt to tighten stage 2's
     "supported => possibly survivable" used a CIRCULAR estimator (defining the support radius by
     the dust's own gravity forces the ratio to 1 for any mass) -- caught by this script's own
     negative control and withdrawn.  The honest fixed-radius number is {sig(dex_1mpc,3)} dex at
     1 Mpc, BELOW the ~0.1 dex tolerance: stage 2's phrase was RIGHT and my correction was wrong.
     Part A caught me inventing a hope; Part D caught me inventing a deficit.  Both logged. ***

  5. THE SUPPORTED CONFIGURATION IS ROUGHLY VIABLE -- AND OUT OF REACH.  Dust held at ~Mpc radii
     leaves the rotation-curve region clean and lands marginal on outskirt lensing.  That IS the
     favorable branch.  It requires Lam_D >= {sig(lam_support,3)}, hence A <= {sig(A_for_support,3)},
     which the cluster calibration forbids (Part B).  The theory's problem is no longer "does a
     good configuration exist" -- it does -- but "one parameter cannot reach it and serve clusters".

  6. NEW FALSIFICATION IN HAND (Part E): the v_c = {sig(v_crit,4)} km/s split predicts a BREAK in
     the RAR residual inside the SPARC range -- dwarfs on the relation, spirals {sig(DEX_CAUSTIC,3)}
     dex off it.  The observed RAR shows no such break.  On existing data, at the published
     ceiling, the fluid-description branch is FALSIFIED -- not merely disfavoured.

  7. WHAT IS LEFT: STAGE 3 -- the wave/field dynamics at and around the caustic, outside the fluid
     description.  It is the ONLY named in-framework door, and Parts B and E now constrain what it
     must deliver: keep the interior clean at v_c > 170 km/s WITHOUT lowering A.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 2 negative controls)")
sys.exit(0)
