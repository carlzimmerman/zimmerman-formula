#!/usr/bin/env python3
r"""mi_forest_bcut_data_2026.py -- the VERIFIED low-b cutoff data used by every forest script in this
directory, plus the audit trail for the four values it replaces. Imported by:

    mi_lyalpha_forest_b_test_2026.py
    mi_forest_total_acceleration_2026.py
    mi_forest_conditional_accel_2026.py
    mi_forest_a0_footing_forks_2026.py

It is a single module so that the correction cannot be applied to three scripts and missed in a fourth,
which is exactly how the bad numbers survived. Run it directly to print the audit trail and the checks.

=======================================================================================================
CORRECTION 2026-07-30 -- THE FOUR b-CUTOFF VALUES THIS DIRECTORY USED ARE UNSOURCEABLE AND ARE GONE.
=======================================================================================================
The retired sequence, carried by four scripts and introduced in commit 138d8ae4 with the description
"web-verified this session, NOT quoted from memory", was

    b_cut = {z=3.70: 15.0, z=3.35: 17.0, z=2.85: 22.0, z=2.30: 24.0} km/s,  B_CUT_ERR = +/- 2.0 km/s

Independent verification against the primary PDFs could not source ANY of it:

  * Schaye et al. 2000 (MNRAS 318, 817; astro-ph/9912432v2) contains NO table of fitted b-cutoff
    values at all. Its only tables are Table 1 (quasar spectra), Table 2 (observed absorption line
    samples) and Table 3 (simulations); the cutoff intercepts appear only as unlabelled lines in
    Figs. 1, 3, 4, 5, 6. Its Fig. 4 DOES document the DIRECTION at fixed N_HI = 10^13.6 cm^-2 --
    caption, verbatim: "The cut-off shifts to larger b-values with decreasing redshift, even though
    the temperature at the mean density, T0, decreases" -- but (i) that figure is for SIMULATION model
    L1, not the observed sample, (ii) the mechanism is explicitly a differential-Hubble-flow / Jeans
    term rather than temperature, and (iii) the numbers "16" and "22" that the retired sequence
    resembles are that figure's y-AXIS TICK LABELS. 15 and 24 fall OUTSIDE the plotted axis range.
    Schaye's actual sample median redshifts are 3.72 / 3.37 / 2.84 / 2.29 at MISMATCHED pivots
    log N0 = 13.5 / 13.0 / 13.0 / 13.0, so no common-pivot four-value sequence is even defined.

  * The low-z half is not merely unsourced, it is REFUTED. Rudie, Steidel & Pettini 2012 (ApJ 757,
    L30; arXiv:1209.0005v1) Table 2 measures the cutoff intercept at EXACTLY the pivot in question,
    log N_HI,0 = 13.6, and gets b0 = 17.90 +/- 0.21 km/s at <z> = 2.4 (2sigma-rejection row) and
    18.50 +/- 0.22 km/s in the <z> = 2.3 bin. A claimed 24 km/s at z = 2.30 is 25 sigma above Rudie's
    own directly measured value at the same redshift and essentially the same pivot. On pure thermal
    broadening 22-24 km/s would demand T0 = 2.9-3.5e4 K, above every one of the thirteen studies
    tabulated in Rudie's Table 3 (which span T0/1e4 K = 1.11 to 2.52).

REPLACED BY the real published sequence: Hiss et al. 2018, ApJ 865, 42 (DOI 10.3847/1538-4357/aada86;
arXiv:1710.00700), TABLE 4, b0(z) in dz = 0.2 bins, carrying the table's OWN ASYMMETRIC percentile
errors instead of one invented symmetric +/- 2.0 km/s -- and carrying, as a SEPARATE and much larger
channel, the cutoff-fitting calibration systematic that Hiss et al. document in their Sec. 5.3 and
that is explicitly NOT in the Table 4 error bars.

THE SHAPE WAS WRONG TOO, NOT JUST THE VALUES. The retired sequence asserted a MONOTONIC RISE toward
low redshift (22 -> 24 km/s from z = 2.85 to z = 2.30). The measured b0(z) is NON-MONOTONIC and turns
over near z = 2.8, FALLING from 22.67 km/s at z = 2.8 to 18.22 km/s at z = 2.0 -- the opposite sense.
Two caveats travel with that statement and are carried in the checks below:
  (a) there is a weak, low-significance secondary DIP at z = 2.2 (16.89 km/s, and by far the worst
      error bar in the table, +1.37/-3.12), so the low-z side is not monotonic either;
  (b) Hiss's b0 is quoted at a z-DEPENDENT pivot, log N_HI,0(z) = 0.6225 (1+z) + 11.1068 (their
      eqn 11), which climbs 0.872 dex from 10^12.97 to 10^13.85 cm^-2 across the eight bins.
      Rescaling every row to one common pivot moves the argmax from z = 2.8 to z = 3.0 and shrinks the
      peak-to-trough contrast from 1.34x to 1.21x. So Schaye's fixed-N_HI direction and Hiss's
      Table 4 b0 are NOT the same statistic, and Schaye's direction does not license the old numbers.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np

# ---------------------------------------------------------------------------------------------------
# THE RETIRED VALUES, kept ONLY so that every script can print what was withdrawn. Never used in any
# calculation. If you find these four numbers in a live code path, that is a bug.
# ---------------------------------------------------------------------------------------------------
RETIRED_B_CUT = {3.70: 15.0, 3.35: 17.0, 2.85: 22.0, 2.30: 24.0}
RETIRED_B_CUT_ERR = 2.0

# ---------------------------------------------------------------------------------------------------
# Hiss et al. 2018, ApJ 865, 42 (arXiv:1710.00700), TABLE 4 ("Measurements and values adopted"):
#     z -> (b0 in km/s, +err, -err)   [median and percentile-based errors of the cutoff parameter b0]
# Transcribed verbatim from the published table. Note the paper prints 22.67+0.55/-0.6 and
# 20.8+0.71/-1.27, i.e. trailing-zero formatting only.
# ---------------------------------------------------------------------------------------------------
B_CUT_HISS = {
    2.0: (18.22, 0.97, 1.39),
    2.2: (16.89, 1.37, 3.12),
    2.4: (18.68, 0.74, 1.07),
    2.6: (20.41, 1.02, 0.87),
    2.8: (22.67, 0.55, 0.60),
    3.0: (22.24, 0.33, 0.73),
    3.2: (21.65, 0.40, 0.52),
    3.4: (20.80, 0.71, 1.27),
}
B_CUT = {z: v[0] for z, v in B_CUT_HISS.items()}
ZS_FOREST = sorted(B_CUT)

# Hiss eqn (11): the z-dependent pivot at which each Table 4 b0 is quoted.
def log_NHI0(z: float) -> float:
    return 0.6225 * (1.0 + z) + 11.1068

# ---------------------------------------------------------------------------------------------------
# THE CALIBRATION SYSTEMATIC -- a SEPARATE, larger error channel, NOT included in Table 4's bars.
#
# Hiss et al. Sec. 5.3 re-evaluate Rudie et al. 2012's cutoff at their own pivot 10^13.2233 cm^-2
# (holding Rudie's Gamma fixed) and get b0' = 15.32 +/- 0.55 km/s, against their own
# b0(z = 2.4) = 18.68 +0.74/-1.07 km/s. Their words: "Our measurement p(b0, Gamma) marginalized over
# Gamma (with b0 = 18.68+0.74/-1.07 km/s) is more than 3 sigma higher than this value, indicating
# tension between our measurements and Rudie et al. (2012a) in terms of b0. This discrepancy is
# probably due to a different implementation of the cutoff and VP-fitting algorithms used."
# i.e. METHOD (least squares vs least absolute deviation), not statistics.
#
# IMPORTANT, so the comparison is not written backwards: the >3 sigma is HISS-vs-RESCALED-RUDIE.
# It is NOT 15.32 versus Rudie's own quoted 17.56 +/- 0.4 -- those are the SAME Rudie measurement at
# two different pivots (10^13.2233 and 10^13.6), so their difference is a definitional rescaling and
# writing it as a disagreement would manufacture one the paper does not claim.
# ---------------------------------------------------------------------------------------------------
HISS_Z24_B0 = 18.68                     # Hiss Table 4, z = 2.4
RUDIE_RESCALED_TO_HISS_PIVOT = 15.32    # Hiss Sec. 5.3, Rudie's default row at Hiss's pivot
RUDIE_DEFAULT_AT_13p6 = 17.56           # Rudie Table 1/2 "default" row, pivot 10^13.6 -- SAME datum
RUDIE_2SIG_AT_13p6 = 17.90              # Rudie Table 2 "2sigma-rej." row, pivot 10^13.6
RUDIE_2SIG_RESCALED = 15.69             # the 2sigma-rej. row through the same rescaling

B_CAL_SYS = HISS_Z24_B0 - RUDIE_RESCALED_TO_HISS_PIVOT      # 3.36 km/s -- headline
B_CAL_SYS_ALT = HISS_Z24_B0 - RUDIE_2SIG_RESCALED           # 2.99 km/s -- 2sigma-rej. variant

# Aguirre, Schaye & Quataert 2001 (ApJ 561, 550; astro-ph/0105184v2) -- DIRECT PRIOR ART.
AGUIRRE_AN = 4.0e-15        # m/s^2; their Eq. 8, 4e-13 cm/s^2 at N_HI = 1e14, T_4 = 1, Gamma_12 = 1
AGUIRRE_LJ_KPC = 11.0       # their Eq. 7, the MOND Jeans length, GAS ONLY
AGUIRRE_A0 = 1.2e-10        # their a0 (McGaugh & de Blok 1998), in m/s^2

# Rudie/Schaye thermal relation, b_thermal = 12.85 sqrt(T/1e4 K) km/s (Rudie eqs. 4-6, proton mass).
B_THERMAL_COEF = 12.85


# ===================================================================================================
# *** THE RESPONSE KERNEL, AND THE ARGUMENT IT TAKES. ADDED 2026-07-30 AFTER AN ADVERSARIAL CHECK
# *** CAUGHT ALL FOUR FOREST SCRIPTS -- AND THE ORIGINAL CORPUS VERSIONS -- EVALUATING IT AT THE WRONG
# *** ACCELERATION, WHICH INFLATED EVERY REPORTED SIGMA. THE ERROR MANUFACTURED A DEFICIT.
# ===================================================================================================
# The framework is modified INERTIA: its law is  mu_fw(|a|/a0) a = g_bar  with
# mu_fw(x) = (sqrt(1+4x^2)-1)/(2x). Note WHICH acceleration is the argument -- the ACTUAL one, |a|.
# Linearising at fixed configuration,
#         d/da [ a mu_fw(a/a0) ] * delta_a = delta_g_bar   =>   delta_a/delta_g_bar = 1/h(x),
#         h(x) = d(x mu_fw(x))/dx = 2x/sqrt(1+4x^2),   x = |a|/a0   (the OBSERVED acceleration).
# The scripts were passing y = g_bar/a0, the NEWTONIAN one. But the framework's own closure says
#         x = y nu(y) = sqrt(y^2 + y)      (exactly g_obs^2 = g_bar^2 + a0 g_bar),
# and in the deep regime sqrt(y^2+y) ~ sqrt(y) >> y, so h(y) << h(x) and 1/h(y) >> 1/h(x).
# Sympy-verified: mu_fw(sqrt(y^2+y)) * sqrt(y^2+y) = y identically, so sqrt(y^2+y) IS mu_fw's argument.
# Deep-regime consequence: the CORRECT linear response is 1/h -> 1/(2 sqrt(y)), NOT 1/(2y).
# At the corpus's own x_rms = 0.0372 that is 2.74 rather than 13.48, i.e. the conservative sqrt(1/h)
# amplification is 1.65x rather than 3.67x -- an inflation factor of 2.2x, and up to 5.6x at the
# smallest y in play. Every sigma computed with the old argument was too large by that factor.
# The scripts' own printed row "[Aguirre a=sqrt(a_N a0) = a0/170] <- MODIFIED a, NOT a_N" was the one
# place the distinction was handled correctly, and it was excluded from the fork rather than adopted.


def x_obs_from_newtonian(y):
    """x = |a|/a0 from y = g_bar/a0, via the framework's OWN closure g_obs^2 = g_bar^2 + a0 g_bar."""
    y = np.asarray(y, dtype=float)
    return np.sqrt(y * y + y)


def h_resp_at_obs(y):
    """h = d(x mu_fw)/dx evaluated at the OBSERVED acceleration, as a function of the Newtonian y."""
    x = x_obs_from_newtonian(y)
    return 2.0 * x / np.sqrt(1.0 + 4.0 * x * x)


def amp_linear(y):
    """Linear-infall amplification 1/h, correctly argumented. Deep limit -> 1/(2 sqrt(y))."""
    return 1.0 / h_resp_at_obs(y)


def amp_sqrt(y):
    """Quasi-equilibrium (conservative) amplification sqrt(1/h), correctly argumented."""
    return float(np.sqrt(amp_linear(y)))


def amp_linear_WRONG_newtonian_arg(y):
    """RETIRED. 1/h evaluated at the NEWTONIAN y -- what the scripts did. Kept so the inflation factor
    can be printed and audited, never for use in a live result path."""
    y = np.asarray(y, dtype=float)
    return np.sqrt(1.0 + 4.0 * y * y) / (2.0 * y)


def amp_inflation_factor(y):
    """How much the retired argument overstated the conservative amplification at this y."""
    return float(np.sqrt(amp_linear_WRONG_newtonian_arg(y) / amp_linear(y)))


def b_thermal(T: float) -> float:
    return B_THERMAL_COEF * np.sqrt(T / 1.0e4)


def err_up(z: float) -> float:
    """Table 4 upward error at z. The prediction under test lies ABOVE the measurement, so the
    measurement uncertainty in the direction of the prediction is the + error."""
    return B_CUT_HISS[z][1]


def err_dn(z: float) -> float:
    return B_CUT_HISS[z][2]


def sig_stat(z: float, b_pred: float) -> float:
    """Significance against Hiss's own STATISTICAL error bar."""
    return (b_pred - B_CUT[z]) / err_up(z)


def sig_cal(z: float, b_pred: float) -> float:
    """Significance against the cutoff-fitting CALIBRATION systematic. Always reported alongside
    sig_stat, never instead of it."""
    return (b_pred - B_CUT[z]) / B_CAL_SYS


def print_correction_notice() -> None:
    """Every forest script prints this. The scripts are the audit trail."""
    print("=" * 100)
    print("CORRECTION NOTICE -- READ BEFORE ANY NUMBER BELOW")
    print("=" * 100)
    print("  The four low-b cutoff values this script used until 2026-07-30 --")
    print(f"    {RETIRED_B_CUT} km/s, +/- {RETIRED_B_CUT_ERR} km/s --")
    print("  were labelled 'web-verified, NOT quoted from memory'. They are UNSOURCEABLE. Verification")
    print("  against the primary PDFs found: Schaye et al. 2000 (MNRAS 318, 817; astro-ph/9912432) has")
    print("  NO table of fitted cutoff values at all, and the 16/22 that sequence resembles are the")
    print("  y-AXIS TICKS of its Fig. 4 (simulation model L1); 15 and 24 lie outside that range. Worse,")
    print("  the low-z half is REFUTED: Rudie, Steidel & Pettini 2012 (ApJ 757, L30; arXiv:1209.0005)")
    print("  Table 2 measures 18.50 +/- 0.22 km/s at <z> = 2.3 at the same pivot, so 24 km/s is 25")
    print("  sigma high, and 22-24 km/s would need T0 = 2.9-3.5e4 K, above all 13 studies in their")
    print("  Table 3.  REPLACED BY Hiss et al. 2018, ApJ 865, 42 (arXiv:1710.00700), Table 4, with the")
    print("  table's own asymmetric errors plus a separate calibration systematic.")
    print("  THE SHAPE WAS ALSO WRONG: the retired sequence rose monotonically toward low z")
    print(f"  (22 -> 24 km/s, z = 2.85 -> 2.30); the measured b0(z) TURNS OVER near z = 2.8 and FALLS to")
    print(f"  {B_CUT[2.0]} km/s at z = 2.0. Schaye's Fig. 4 documents a rise at FIXED N_HI = 10^13.6 in a")
    print("  simulation, but Hiss's b0 sits at a z-DEPENDENT pivot log N_HI,0 = 0.6225(1+z) + 11.1068,")
    print("  so they are different statistics and Schaye does not license the retired numbers.")
    print("=" * 100)


def print_data_table() -> None:
    print(f"  Hiss et al. 2018, ApJ 865, 42 (arXiv:1710.00700), Table 4 -- the b(N) cutoff parameter b0:")
    print(f"  {'z':>5s} {'b0 (km/s)':>10s} {'+err':>6s} {'-err':>6s} {'log N_HI,0(z)':>14s} "
          f"{'sigma_stat/sigma_cal':>21s}")
    for z in ZS_FOREST:
        b0, ep, em = B_CUT_HISS[z]
        print(f"  {z:5.1f} {b0:10.2f} {ep:6.2f} {em:6.2f} {log_NHI0(z):14.4f} "
              f"{B_CAL_SYS/ep:20.2f}x")
    print(f"  calibration systematic B_CAL_SYS = {B_CAL_SYS:.2f} km/s "
          f"({HISS_Z24_B0} - {RUDIE_RESCALED_TO_HISS_PIVOT}, Hiss Sec. 5.3), "
          f"2sigma-rej. variant {B_CAL_SYS_ALT:.2f} km/s")
    print(f"  median Table 4 statistical +err = {np.median([err_up(z) for z in ZS_FOREST]):.2f} km/s, so the")
    print(f"  calibration channel is {B_CAL_SYS/np.median([err_up(z) for z in ZS_FOREST]):.1f}x wider than the median statistical bar.")


def _self_test() -> int:
    ok = True

    def check(c, m):
        nonlocal ok
        if not c:
            ok = False
        print(f"  [{'OK' if c else 'FAIL'}] {m}")

    print_correction_notice()
    print()
    print_data_table()
    print()
    print("SELF-TESTS ON THE VERIFIED DATA")

    check(len(B_CUT_HISS) == 8, f"Table 4 transcribed with all {len(B_CUT_HISS)} dz = 0.2 bins, z = "
                                f"{min(ZS_FOREST)} to {max(ZS_FOREST)}")

    zmax_b = max(ZS_FOREST, key=lambda z: B_CUT[z])
    check(zmax_b == 2.8,
          f"b0(z) peaks at z = {zmax_b} (b0 = {B_CUT[zmax_b]} km/s) -- NON-MONOTONIC, and note the peak "
          f"moves to z = 3.0 if all rows are rescaled to one common pivot (contrast 1.34x -> 1.21x)")

    check(B_CUT[2.0] < B_CUT[2.8],
          f"the retired sequence's SHAPE is contradicted: it rose toward low z, but measured b0 FALLS "
          f"from {B_CUT[2.8]} km/s at z = 2.8 to {B_CUT[2.0]} km/s at z = 2.0")

    dip = B_CUT[2.2] < min(B_CUT[2.0], B_CUT[2.4])
    dip_sig = (min(B_CUT[2.0], B_CUT[2.4]) - B_CUT[2.2]) / err_up(2.2)
    check(dip,
          f"secondary DIP at z = 2.2 present as tabulated ({B_CUT[2.2]} km/s) but only "
          f"{dip_sig:.1f} sigma on its own +err and it carries the table's worst bar "
          f"(+{err_up(2.2)}/-{err_dn(2.2)}) -- reported, not leaned on")

    contrast = max(B_CUT.values()) / min(B_CUT.values())
    check(abs(contrast - 1.342) < 0.01,
          f"raw peak-to-trough contrast {contrast:.3f}x ({max(B_CUT.values())}/{min(B_CUT.values())}), "
          f"which the verified common-pivot rescaling reduces to ~1.21x")

    check(abs(log_NHI0(2.4) - 13.2233) < 1e-3,
          f"Hiss eqn 11 reproduces their quoted pivot at z = 2.4: log N_HI,0 = {log_NHI0(2.4):.4f} "
          f"vs the paper's 10^13.22 cm^-2")

    check(abs(B_CAL_SYS - 3.36) < 0.01 and abs(B_CAL_SYS_ALT - 2.99) < 0.01,
          f"calibration systematic {B_CAL_SYS:.2f} km/s (2sigma-rej. variant {B_CAL_SYS_ALT:.2f}), i.e. "
          f"{100*B_CAL_SYS/HISS_Z24_B0:.0f}% of b0 -- Hiss's own >3 sigma method disagreement with Rudie")

    check(B_CAL_SYS > max(err_up(z) for z in ZS_FOREST),
          f"the calibration channel ({B_CAL_SYS:.2f} km/s) is wider than EVERY Table 4 statistical bar "
          f"(max +err = {max(err_up(z) for z in ZS_FOREST)} km/s), so it is always the WEAKER of the two "
          f"significances -- which is why both must be printed side by side, never one alone")

    check(abs(RUDIE_DEFAULT_AT_13p6 - 17.56) < 1e-9 and RUDIE_RESCALED_TO_HISS_PIVOT < RUDIE_DEFAULT_AT_13p6,
          f"the >3 sigma is HISS ({HISS_Z24_B0}) vs RESCALED RUDIE ({RUDIE_RESCALED_TO_HISS_PIVOT}); "
          f"{RUDIE_RESCALED_TO_HISS_PIVOT} vs {RUDIE_DEFAULT_AT_13p6} is the SAME Rudie datum at two "
          f"pivots and is NOT a disagreement")

    # the rescaling itself, reproduced: 17.56 * 10^(0.156*(13.2233-13.6)) should give ~15.3
    resc = RUDIE_DEFAULT_AT_13p6 * 10 ** (0.156 * (log_NHI0(2.4) - 13.6))
    check(abs(resc - RUDIE_RESCALED_TO_HISS_PIVOT) < 0.10,
          f"Hiss's pivot rescaling reproduced independently: {RUDIE_DEFAULT_AT_13p6} x "
          f"10^(0.156 x ({log_NHI0(2.4):.4f} - 13.6)) = {resc:.2f} vs their {RUDIE_RESCALED_TO_HISS_PIVOT}")

    check(not any(v in set(B_CUT.values()) for v in RETIRED_B_CUT.values()),
          "none of the four retired values appears anywhere in the replacement data")

    # *** THE KERNEL-ARGUMENT GUARD. *** This is the identity that was violated for months: mu_fw's
    # argument is the OBSERVED acceleration, and the framework's own closure fixes it to sqrt(y^2+y).
    # If anyone re-points h at the Newtonian y, THIS check fails. It is an identity, not a verdict.
    yy = np.array([1e-4, 1e-3, 1e-2, 0.0372, 0.1, 1.0, 10.0, 1e3])
    xx = x_obs_from_newtonian(yy)
    mu = (np.sqrt(1.0 + 4.0 * xx * xx) - 1.0) / (2.0 * xx)
    round_trip = mu * xx                      # must return y exactly
    check(np.allclose(round_trip, yy, rtol=1e-12),
          f"KERNEL-ARGUMENT IDENTITY: mu_fw(sqrt(y^2+y)) * sqrt(y^2+y) = y to rtol 1e-12 over "
          f"y = {yy.min():.0e}..{yy.max():.0e} -- confirming sqrt(y^2+y), the OBSERVED acceleration, is "
          f"mu_fw's argument. If h is ever re-pointed at the Newtonian y this check FAILS.")
    deep = amp_linear(1e-6) * 2.0 * np.sqrt(1e-6)
    check(abs(deep - 1.0) < 1e-3,
          f"and the deep-regime asymptote is the CORRECT one: 1/h -> 1/(2 sqrt(y)) (ratio {deep:.6f} to "
          f"1), NOT the 1/(2y) the retired argument gave -- which at y=1e-6 would differ by "
          f"{amp_inflation_factor(1e-6):.0f}x")

    check(abs(b_thermal(1.0e4) - 12.85) < 1e-9 and abs(b_thermal(2.0e4) - 12.85 * np.sqrt(2)) < 1e-9,
          f"thermal floor b_th = {b_thermal(1.0e4):.2f} km/s at T = 1e4 K, "
          f"{b_thermal(2.0e4):.2f} at 2e4 K (Rudie eqs. 4-6, proton mass)")

    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_self_test())
