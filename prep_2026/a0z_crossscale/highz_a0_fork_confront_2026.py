#!/usr/bin/env python3
"""
highz_a0_fork_confront_2026.py -- FROZEN CONFRONTATION: real high-z a0(z) data on the HORIZON FORK.
====================================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA.  a0 = c H_Lambda / Z,  Z = sqrt(32pi/3).

The de Sitter-Unruh mechanism ties a0 to the Unruh temperature of a horizon; WHICH horizon is a
POSIT, and different horizons give OPPOSITE a0(z) evolution.  BAO's precise E(z) and rho_DE(z) drive
the two readings a FACTOR apart at z~2-3, so a CRUDE high-z a0(z) point (tens-of-% precision) forks
them -- it does NOT need the ~7% precision the 9.36-vs-1.13 FOOTING question demands.

  BRANCH A  de Sitter / future-event horizon  [Carl's canonical] : a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
            -> DECLINES to ~0.78x at z=3 (bump-then-decline; pure-Lambda limit is FLAT=1).
  BRANCH B  Hubble horizon  [McCulloch MiHsC; credited]          : a0(z)/a0(0) = E(z) = H(z)/H0
            -> RISES steeply to ~4.5x at z=3 (matter-dominated).
  BRANCH C  pure-Lambda FLAT (Carl's w->-1 limit)                : a0(z)/a0(0) = 1 for all z.

This is the FROZEN confrontation that:
  (i)   reproduces the fork predictions from the committed desitter_unruh_horizon_fork_2026.py;
  (ii)  hard-codes the REAL compiled high-z a0(z) data (cited in-line);
  (iii) places EACH point on the fork -> branch + significance;
  (iv)  prints the COMBINED constraint + the honest verdict (does the data pick a branch? net lean?);
  (v)   prints the single decisive new measurement (z, a0 precision, instrument);
  and ends with a PRE-REGISTRATION block (decision thresholds + every load-bearing caveat).

HARD CALIBRATION (manufactured win == manufactured deficit; penalized EQUALLY):
  * MUSE-DARK III (Ciocan) DIRECTLY measures a0 RISING -> reported as a TENSION for Carl's declining
    branch, NOT buried, NOT spun into support. It even overshoots McCulloch. Its pull is toward RISING.
  * MSA-3D uses the SELECTION-CORRECTED slope +0.91+/-0.79 (NOT the raw +2.13, which is >half
    g_obs-selection). Its central value is mildly RISING but consistent with flat at ~1.1 sigma.
  * BTFR zero-points are 4x-DESENSITIZED (bTFR ZP ~ a0^(1/4) => d a0/a0 = 4 d V/V), so their a0(z)
    errors are honestly LARGE (systematics-inclusive +/-0.30-0.35 dex ~ a factor of 2 in a0).
  * All points are REAL cited literature / committed digitized data; estimates are LABELED.
  * a0's value + the horizon choice are POSITS; nu = Milgrom 1999 (PLA 253:273 Eq.9); McCulloch
    credited for the Hubble reading. No TOE. No 'theory closed'.

An honest 'current crude data is MIXED/WEAK and MUSE-DARK III leans RISING against the declining
branch; decisive point = a clean deep-MOND a0(z) at z~2-3' is the accepted verdict of this file.
Exit 0 = ran (not a verdict).
"""
import numpy as np

np.seterr(all="ignore")   # silence a spurious platform BLAS matmul warning (results unaffected)

# ======================================================================================
# 1. THE FORK BRANCHES  (identical machinery + posteriors to desitter_unruh_horizon_fork_2026.py)
# ======================================================================================
OM, OL = 0.315, 0.685
Z_CONST = np.sqrt(32 * np.pi / 3)
A0_CAN, A0_ALT = 9.355e-11, 1.131e-10          # canonical cH_Lambda/Z ; alt cH0/Z
W0, WA = -0.838, -0.62                          # DESI DR2 w0waCDM Pantheon+ central (the fork head)

def rho_de_ratio(z, w0=W0, wa=WA):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def a0_deSitter(z):  return np.sqrt(rho_de_ratio(z))                                   # (A) declining [Carl]
def a0_Hubble(z):    return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + OL * rho_de_ratio(z))  # (B) rising [McCulloch]
def a0_flat(z):      return np.ones_like(np.asarray(z, float))                          # (C) pure-Lambda flat [Carl w->-1]

def loglog_slope(fn, zlo, zhi, n=400):
    z = np.linspace(zlo, zhi, n)
    return float(np.polyfit(np.log10(1 + z), np.log10(fn(z)), 1)[0])

def lin_slope_ratio(fn, zlo, zhi, n=400):
    """slope d(a0(z)/a0(0))/dz of a branch, matching Ciocan's linear a1 units (a0(0)=1)."""
    z = np.linspace(zlo, zhi, n)
    y = fn(z) / fn(0.0)
    return float(np.polyfit(z, y, 1)[0])

bar = "=" * 100
print(bar)
print("FROZEN HIGH-z a0(z) CONFRONTATION ON THE de Sitter-Unruh HORIZON FORK  (2026-07-23)")
print(bar)
print(f"  a0 = cH_Lambda/Z, Z = {Z_CONST:.5f}.  canonical a0(0)={A0_CAN:.3e}, alt={A0_ALT:.3e} m/s^2.")
print("  Fork: (A) de Sitter sqrt(rho_DE) DECLINES | (B) Hubble E(z) [McCulloch] RISES | (C) pure-Lambda FLAT.")
print(f"\n  {'z':>4} | {'A declining':>12} | {'B rising':>10} | {'C flat':>7} | {'B/A divergence':>15}")
print("  " + "-" * 62)
for z in [0.5, 0.9, 1.0, 1.1, 1.5, 2.0, 2.3, 2.4, 3.0, 3.25]:
    A, B = float(a0_deSitter(z)), float(a0_Hubble(z))
    print(f"  {z:>4.2f} | {A:>12.3f} | {B:>10.3f} | {1.0:>7.3f} | {B/A:>14.2f}x")
print("  => the branches diverge by a FACTOR (5.9x @ z=3): tens-of-% a0(z) precision forks them.")
print(f"     required a0(z) precision for 3-sigma separation: z=1 ~19% | z=2 ~37% | z=3 ~47%.")

# ======================================================================================
# 2A. DIRECT a0(z) / RAR-SLOPE POINTS  (the M-L-offset-canceling observable; the SHARPEST class)
# ======================================================================================
print("\n" + bar); print("2A. DIRECT a0(z) PROBES  (RAR / a0-slope fits -- the clean M-L-canceling observable)"); print(bar)

def sig(meas, err, target):
    return abs(meas - target) / err

# -------------------- MSA-3D (SELECTION-CORRECTED) --------------------
# Espejo Salcedo et al. 2026, "MSA-3D: Rotation Curves and Dark Matter Fractions at z~0.5-1.7 with
# JWST/NIRSpec", arXiv:2606.27853.  30 SFGs (golden N=23) 0.58<z<1.68, JWST/NIRSpec + NIRCam masses.
# Committed msa3d_a0z_selection_decomposition.py:  RAW slope d log10(a0)/d log10(1+z) = +2.13
#   = g_obs(selection) +1.13  +  h(f_DM) +1.00 ;  GENUINE residual controlling for g_obs = +0.91
#   [16-84%: +0.05, +1.63] -> sigma ~ 0.79.  USE +0.91 (NOT +2.13, which is >half selection).
MSA_SLOPE, MSA_ERR, MSA_ZLO, MSA_ZHI = 0.91, 0.79, 0.58, 1.68
sd_msa = loglog_slope(a0_deSitter, MSA_ZLO, MSA_ZHI)   # declining branch log-log slope over its range
sr_msa = loglog_slope(a0_Hubble,   MSA_ZLO, MSA_ZHI)   # rising branch log-log slope over its range
mD, mR, mF = sig(MSA_SLOPE, MSA_ERR, sd_msa), sig(MSA_SLOPE, MSA_ERR, sr_msa), sig(MSA_SLOPE, MSA_ERR, 0.0)
print(f"\n[1] MSA-3D (sel-corrected)  arXiv:2606.27853  z~0.58-1.68 (median ~1.1), N=23 golden")
print(f"    measured d log10(a0)/d log10(1+z) = {MSA_SLOPE:+.2f} +/- {MSA_ERR:.2f}   (RAW +2.13 was >half g_obs-selection)")
print(f"    branch slopes over its z-range:  declining {sd_msa:+.2f} | rising {sr_msa:+.2f} | flat 0.00")
print(f"    -> {mD:.2f}s from DECLINING | {mR:.2f}s from RISING | {mF:.2f}s from FLAT")
print(f"    PLACEMENT: BETWEEN branches; central mildly RISING but consistent with FLAT at {mF:.1f}s and")
print(f"    with declining at {mD:.1f}s. Nominally nearest rising, preference over flat only ~{mF:.1f}s (sub-sig).")
print(f"    => UNDERPOWERED / WATCH: excludes NO branch, confirms NONE.")

# -------------------- MUSE-DARK III (Ciocan) -- THE RISING PULL --------------------
# Ciocan et al. 2026, "MUSE-DARK III: The evolution of the radial acceleration relation at
# intermediate redshifts", A&A 709 L16, arXiv:2604.22613.  79 SFGs 0.33<z<1.44, MUSE HUDF.
# DIRECT RAR fit a0(z)=a0(0)+a1*z [x1e-10]:  LCDM-mass route a1=+1.59+/-0.10, MOND-3D route a1=+1.20+/-0.10;
# a0(z~1)=2.38(+0.12/-0.10)e-10; evolution detected ~30 sigma; a0 rises FASTER than H(z).
MU_A1, MU_A1_STAT, MU_ZLO, MU_ZHI = 1.59, 0.105, 0.33, 1.44     # LCDM-route slope (the headline)
sd_mu = lin_slope_ratio(a0_deSitter, MU_ZLO, MU_ZHI)            # declining branch linear a1 over its range
sr_mu = lin_slope_ratio(a0_Hubble,   MU_ZLO, MU_ZHI)            # rising branch linear a1 over its range
# HONEST systematic: MUSE-DARK III is a RAR fit on SFGs and thus shares the LCDM-assembly "apparent-a0"
# drift that a pure-LCDM sim with NO fundamental a0 already produces -- Magneticum / Mayer et al. 2023
# (arXiv:2206.04333, MNRAS) reproduces an apparent-a0 rise ~x3 by z=2.3 (slope ~+0.80/z over this range).
# Fold HALF that shared-drift slope in quadrature as an a1 systematic (de-systematization).
SLOPE_MAG = 0.80
MU_A1_SYS = float(np.hypot(MU_A1_STAT, 0.5 * SLOPE_MAG))
nD, nR, nF = sig(MU_A1, MU_A1_STAT, sd_mu), sig(MU_A1, MU_A1_STAT, sr_mu), sig(MU_A1, MU_A1_STAT, 0.0)
hD, hR, hF = sig(MU_A1, MU_A1_SYS,  sd_mu), sig(MU_A1, MU_A1_SYS,  sr_mu), sig(MU_A1, MU_A1_SYS,  0.0)
print(f"\n[2] MUSE-DARK III / Ciocan  arXiv:2604.22613 (A&A 709 L16)  z~0.33-1.44, N=79  ** THE RISING PULL **")
print(f"    measured a0(z)=a0(0)+a1*z, a1(LCDM-route)=+{MU_A1:.2f}+/-{MU_A1_STAT:.3f} (stat); a1(MOND-3D)=+1.20+/-0.10;")
print(f"    a0(z~1)=2.38(+0.12/-0.10)e-10; evolution ~30 sigma; a0 rises FASTER than H(z).")
print(f"    branch linear slopes over its z-range:  declining {sd_mu:+.2f} | rising {sr_mu:+.2f} | flat 0.00")
print(f"    NAIVE stat:  {nD:.1f}s from DECLINING | {nR:.1f}s from RISING | {nF:.1f}s from FLAT")
print(f"    HONEST (a1 err inflated to {MU_A1_SYS:.2f} by shared LCDM-assembly drift, Magneticum/Mayer+2023):")
print(f"                 {hD:.1f}s from DECLINING | {hR:.1f}s from RISING | {hF:.1f}s from FLAT")
print(f"    PLACEMENT: RISING -- and OVERSHOOTS even McCulloch (a1={sr_mu:+.2f}); it is the live TENSION for")
print(f"    Carl's DECLINING branch. Face-value ~{nD:.0f}s against declining; de-systematized ~{hD:.1f}s against.")
print(f"    LCDM-DEGENERATE (Magneticum reproduces ~half the slope with NO fundamental a0) -> NOT a clean")
print(f"    confirmation of McCulloch EITHER. Net: its PULL is toward RISING, away from Carl.")

# ======================================================================================
# 2B. bTFR ZERO-POINT POINTS  (4x-desensitized; Delta_b along mass axis -> a0(z)/a0(0)=10^(-Delta_b))
#     bTFR ZP ~ a0^(1/4) => d a0/a0 = 4 d V/V (velocity axis), so the MASS-axis Delta_b maps 1:1 to
#     log10(a0 ratio) and the a0 error is honestly LARGE. Dilution: g_bar>>a0 samples see only a
#     fraction x/(2+x) of the a0-lever -> flagged DEGENERATE / non-diagnostic.
# ======================================================================================
print("\n" + bar); print("2B. bTFR ZERO-POINT POINTS  (4x-desensitized; systematics-inclusive errors)"); print(bar)

def place_ratio(tag, cite, z, R, sR_, clean, note):
    Rd, Rr, Rf = float(a0_deSitter(z)), float(a0_Hubble(z)), 1.0
    sD, sRi, sF = abs(R - Rd) / sR_, abs(R - Rr) / sR_, abs(R - Rf) / sR_
    fav = "RISING" if (sRi < sD and sRi < sF) else ("FLAT/declining (Carl)" if sF <= sD else "DECLINING (Carl)")
    print(f"\n[{tag}]  {cite}  z~{z:.2f}   a0(z)/a0(0) = {R:.2f} +/- {sR_:.2f}   [{'CLEAN low-acc' if clean else 'DEGENERATE g>>a0'}]")
    print(f"    branch ratios at z~{z:.2f}:  declining {Rd:.2f} | rising {Rr:.2f} | flat 1.00")
    print(f"    -> {sD:.2f}s from DECLINING | {sRi:.2f}s from RISING | {sF:.2f}s from FLAT   FAVORS: {fav}")
    print(f"    {note}")
    return dict(tag=tag, z=z, R=R, sR=sR_, clean=clean, sD=sD, sR_=sRi, sF=sF, fav=fav)

def ratio_from_db(db, db_err_dex):
    """Delta_b (mass axis, dex) -> a0(z)/a0(0)=10^(-Delta_b); error via log Jacobian."""
    R = 10.0 ** (-db)
    return R, float(np.log(10.0) * R * db_err_dex)

ratio_pts = []
# [3] Jeanneau et al. 2026 (MUSE-DARK II), A&A, arXiv:2603.28856 -- 95 LENSED low-mass SFGs 0.56<z<1.37.
#     bTFR Delta_b = 0.00 +/- 0.06 (stat); systematics-inclusive honest band 0.00 +/- 0.27 dex.
#     The ONLY near-a0 (g_bar~0.3-1 a0) bTFR in hand. NOTE: MUSE-DARK II (Jeanneau) is FLAT and a
#     DIFFERENT paper/sample from MUSE-DARK III (Ciocan, above, which is RISING) -- do NOT conflate.
R, sR_ = ratio_from_db(0.00, 0.27)
ratio_pts.append(place_ratio("3", "Jeanneau+26 MUSE-DARK II bTFR  arXiv:2603.28856", 0.9, R, sR_, True,
    "CLEANEST low-acc point (lensed, g_bar~0.3-1 a0). 0.00+/-0.06 stat; honest +/-0.27 folds gas-model\n"
    "    (Tacconi+20 + NeutralUniverseMachine 0.8dex) + local-ref +/-0.16. FLAT -> leans Carl's flat/declining side."))
# [4] Ubler et al. 2017, ApJ 842,121, arXiv:1703.04321 -- KMOS3D bTFR.  z~0.9 Delta_b=-0.44+/-0.04 stat.
#     Honest sys +/-0.35 (M* 0.15 + gas 0.20 scaling-relation + convention). g_bar>>a0 => diluted.
R, sR_ = ratio_from_db(-0.44, 0.35)
ratio_pts.append(place_ratio("4", "Ubler+17 KMOS3D bTFR  arXiv:1703.04321", 0.9, R, sR_, False,
    "naive RISING x2.75, BUT g_bar~0.3-1.7 a0 (a0-lever diluted to 0.23-0.63) + LCDM-halo/size-degenerate;\n"
    "    and 6-sigma INTERNALLY INCONSISTENT with Jeanneau at the SAME z -> the z~1 bTFR is unresolved. NON-diagnostic."))
# [5] Ubler et al. 2017 -- KMOS3D bTFR.  z~2.3 Delta_b=-0.27+/-0.05 stat; honest sys +/-0.35.
R, sR_ = ratio_from_db(-0.27, 0.35)
ratio_pts.append(place_ratio("5", "Ubler+17 KMOS3D bTFR  arXiv:1703.04321", 2.3, R, sR_, False,
    "naive RISING x1.86 (NON-monotonic: BELOW its own z=0.9 value); g_bar~(2-6)a0 (lever 0.07-0.18) +\n"
    "    canonical size-evolution term (-0.2..-0.3) lives in the SAME direction -> WASH, NON-diagnostic."))
# [6] Amvrosiadis et al. 2025, MNRAS, arXiv:2312.08959 -- 12 ALMA CO disc DSFGs.  z~2.4 Delta_b=-0.26+/-0.19 stat.
R, sR_ = ratio_from_db(-0.26, 0.30)
ratio_pts.append(place_ratio("6", "Amvrosiadis+25 DSFG bTFR  arXiv:2312.08959", 2.4, R, sR_, False,
    "CONCORDANT with Ubler z~2.3 (the one reproduced high-z bTFR number), but N=12, alpha_CO=0.92+/-0.36-mediated,\n"
    "    g_bar~6a0 (lever ~0.07) -> WASH, NON-diagnostic."))
# [7] Tiley et al. 2019, MNRAS 482,2166, arXiv:1810.07202 -- KROSS quality-matched sTFR.  z~1.0
#     matched Delta_b=-0.09 (disky)/+0.02 (v/sigma>1); K-band null. Map to a0 ratio ~1.0-1.1, +/-0.10 dex.
R, sR_ = ratio_from_db(-0.05, 0.10)   # midpoint of matched stellar-axis result, stellar (not a clean bTFR)
ratio_pts.append(place_ratio("7", "Tiley+19 KROSS matched sTFR  arXiv:1810.07202", 1.0, R, sR_, False,
    "quality-matched (degrading local SAMI to KROSS quality removes the apparent evolution). FLAT/constant.\n"
    "    Stellar (not the clean bTFR fork observable) -> leans FLAT; degrading-quality artifact ~ size of any evolution."))

# ======================================================================================
# 2C. DIRECT DEEP-MOND OBJECT + EXTERNAL BOUNDS  (context, real & cited)
# ======================================================================================
print("\n" + bar); print("2C. DIRECT DEEP-MOND OBJECT + CONSTANCY BOUNDS (context)"); print(bar)
# [8] "Big Wheel" z=3.245 giant disc, arXiv:2409.17956 (Nature Astronomy) -- a single deep-MOND-regime
#     rotator that FOLLOWS the local TFR => a0_eff = V^4/(G M_bar) ~ 1.0-1.3 x a0(0) [MC, +/-0.22 dex, N=1].
BW_R, BW_sR, BW_z = 1.15, 0.22 * np.log(10) * 1.15, 3.25   # crude: +/-0.22 dex -> linear error
bD, bR, bF = abs(BW_R - float(a0_deSitter(BW_z))) / BW_sR, abs(BW_R - float(a0_Hubble(BW_z))) / BW_sR, abs(BW_R - 1.0) / BW_sR
print(f"\n[8] Big Wheel z=3.25  arXiv:2409.17956  (single deep-MOND disc; N=1, a0 err ~+/-0.22 dex optimistic)")
print(f"    a0_eff/a0(0) ~ {BW_R:.2f} +/- {BW_sR:.2f}   branch: declining {float(a0_deSitter(BW_z)):.2f} | rising {float(a0_Hubble(BW_z)):.2f} | flat 1.00")
print(f"    -> {bD:.2f}s from DECLINING | {bR:.2f}s from RISING | {bF:.2f}s from FLAT")
print(f"    CLEAN deep-MOND regime: disfavors the ~5x rise at ~{bR:.1f}s; cannot resolve the 0.75 decline -> leans FLAT.")
print("\n[9] McGaugh+24 (arXiv:2406.17930): BTFR/f_DM to z~2.5 shows 'no clear evolution' -> favors Carl's flat side.")
print("[10] Milgrom 2017 (arXiv:1703.06110): direct high-z RCs 'all but exclude' a x4 a0 rise AND the (1+z)^1.5")
print("     law -> BOUNDS steep rises; would EXCLUDE the full McCulloch branch (x4.5@z3) at high z.")
print("[11] Sharma+24 (arXiv:2406.08934, free-slope bTFR): intermediate-z ZP is slope-dependent and can FLIP")
print("     sign vs Ubler -> demonstrates fixed-slope bTFR ZPs are NOT clean a0 reads. Context only.")

# ======================================================================================
# 3. COMBINED CONSTRAINT
# ======================================================================================
print("\n" + bar); print("3. COMBINED CONSTRAINT"); print(bar)

# (i) the two DIRECT probes in a common log-log slope currency.
zz = np.linspace(MU_ZLO, MU_ZHI, 400)
mu_ll = float(np.polyfit(np.log10(1 + zz), np.log10(1 + MU_A1 * zz), 1)[0])   # Ciocan in log-log slope
jac = mu_ll / MU_A1
mu_ll_stat, mu_ll_sys = MU_A1_STAT * jac, MU_A1_SYS * jac
print(f"  DIRECT probes in log-log slope d log10(a0)/d log10(1+z):")
print(f"    MSA-3D  = {MSA_SLOPE:+.2f} +/- {MSA_ERR:.2f}")
print(f"    Ciocan  = {mu_ll:+.2f} +/- {mu_ll_stat:.2f} (stat) / {mu_ll_sys:.2f} (honest, LCDM-assembly sys)")
print(f"    branch log-log slopes (~0.3-1.7): declining {sd_msa:+.2f} | rising {sr_msa:+.2f} | flat 0.00")
for tag, mu_err in [("NAIVE stat", mu_ll_stat), ("HONEST (Ciocan sys-inflated)", mu_ll_sys)]:
    w1, w2 = 1 / MSA_ERR ** 2, 1 / mu_err ** 2
    comb = (MSA_SLOPE * w1 + mu_ll * w2) / (w1 + w2)
    comb_err = (w1 + w2) ** -0.5
    cD, cR, cF = abs(comb - sd_msa) / comb_err, abs(comb - sr_msa) / comb_err, abs(comb - 0) / comb_err
    print(f"    [{tag:28}] IV-combined slope = {comb:+.2f} +/- {comb_err:.2f}"
          f"  -> {cD:.1f}s declining | {cR:.1f}s rising | {cF:.1f}s flat")
print("    CAVEAT (load-bearing): BOTH direct probes are RAR-fits on SFGs => they SHARE the LCDM-assembly")
print("    apparent-a0 drift; combining does NOT beat it down. The declining-branch tension therefore spans")
print("    ~0s (if the apparent rise is FULLY assembly) to ~5s (if only HALF). No clean fork read lives there.")

print("\n  bTFR / RATIO arm (SPLIT and mostly degenerate):")
clean = [p for p in ratio_pts if p["clean"]]
print(f"    - CLEAN low-acc (Jeanneau): FLAT, leans Carl -> {clean[0]['sF']:.1f}s from flat vs {clean[0]['sR_']:.1f}s from rising.")
print("    - DEGENERATE (Ubler z0.9/z2.3, Amvrosiadis z2.4): negative Delta_b = rising PULL, but g_bar>>a0 +")
print("      LCDM-halo + size degeneracy => cannot attribute to a0 -> WASH, NON-diagnostic.")
print("    - Big Wheel z=3.25 (clean deep-MOND, N=1) + Tiley matched + McGaugh/Milgrom bounds -> lean FLAT.")

# ======================================================================================
# 4. HONEST VERDICT  +  DECISIVE MEASUREMENT
# ======================================================================================
print("\n" + bar); print("4. HONEST VERDICT -- does current crude high-z a0(z) data pick a branch?"); print(bar)
print("""  MIXED and WEAK -- the data does NOT yet decisively pick a branch, and its lean depends on which
  probe class you weight:
   (i)  DIRECT RAR / a0 fits pull RISING: MUSE-DARK III strongly (it OVERSHOOTS even McCulloch), MSA-3D's
        selection-corrected central value mildly (but consistent with flat at ~1.1s).
   (ii) CLEAN-REGIME baryonic / deep-MOND zero-points pull FLAT: Jeanneau near-a0 bTFR 0.00+/-0.27, Big
        Wheel z=3.25 ~1.0-1.3, Tiley matched ~0, McGaugh/Milgrom constancy bounds -- all consistent with
        Carl's DECLINING branch (only 0.75-1.0 at z<=3.25, INDISTINGUISHABLE from flat at this precision)
        and mildly against a steep rise.
   (iii)The fixed-slope 'rising' bTFR points (Ubler / Amvrosiadis) are gutted by acceleration DILUTION
        (g_bar>>a0) and are LCDM/size-degenerate -> NON-diagnostic.

  NET (stated plainly): the single most-cited DIRECT measurement (MUSE-DARK III) LEANS AGAINST Carl's
  declining branch -- a real TENSION. Face value it is ~16s against declining (~18s combined with MSA-3D).
  It is LCDM-degenerate (Magneticum/Mayer+2023 reproduces an apparent-a0 rise ~x3 by z=2.3 in PURE LCDM
  with NO fundamental a0), so the HONEST residual tension against declining SPANS A RANGE: ~0s if the
  apparent rise is FULLY LCDM-assembly, up to ~4-5s (this script: 4.1s single / 4.8s combined) if the
  error is merely inflated by half the shared-assembly drift and none of the central rise is subtracted.
  Either way MUSE-DARK III does NOT cleanly confirm McCulloch either -- it OVERSHOOTS E(z) (its residual
  is only ~1.5s from the rising branch). The clean deep-MOND / low-acceleration constraints (Jeanneau,
  Big Wheel, Tiley, McGaugh/Milgrom) lean FLAT (Carl-compatible). NO branch is excluded. Honest label:
  MIXED / UNDERPOWERED-FOR-A-CLEAN-FORK, with a degeneracy-contaminated net lean toward RISING from the
  direct probes and toward FLAT from the clean deep-MOND probes.

  THE SINGLE DECISIVE NEW MEASUREMENT:
   A CLEAN deep-MOND-selected a0(z) at z~2-3: LOW-ACCELERATION selected (g_bar < ~0.3 a0, where fitted a0
   = fundamental a0 and the assembly/size/dilution degeneracies all vanish -- the requirement NO current
   sample meets), measured to ~35-47% a0 precision. At z=2 the branches are ~3.4x apart (declining 0.87 vs
   rising 3.01) so ~37% a0 => 3s; at z=3 they are ~5.9x apart (~47% => 3s). Instrument: JWST NIRSpec-IFU on
   LENSED low-mass rotators / dwarfs at z~2-3 (+ ALMA CO/[CII] cold-gas velocity fields). One clean lensed
   dwarf RC at z~3, g<0.3a0, sigma(a0)~35% forks it in a single pointing; a small sample (N~15-40) does it
   robustly. NOTE the systematics floor (committed highz_systematics_floor.py): today's samples are NO-GO
   (~0.3 dex coherent bias, ~9-55x the requirement); a clean fork read likely needs ELT/ALMA cold tracers +
   DIRECT HI 21cm gas masses (SKA2/ngVLA, <0.05 dex, no alpha_CO) -> ~2035+, NOT more massive-SFG RAR-fits.""")

# ======================================================================================
# 5. PRE-REGISTRATION BLOCK  (frozen decision thresholds + every load-bearing caveat)
# ======================================================================================
print("\n" + "#" * 100)
print("# PRE-REGISTRATION  --  FROZEN 2026-07-23  --  high-z a0(z) horizon-fork confrontation")
print("#" * 100)
print("# FORK (a0(z)/a0(0), DESI DR2 Pantheon+ w0wa):  (A) de Sitter sqrt(rho_DE) DECLINES ~0.78x@z3 [Carl];")
print("#   (B) Hubble E(z) RISES ~4.54x@z3 [McCulloch]; (C) pure-Lambda FLAT=1 [Carl w->-1]. Separated by a")
print("#   FACTOR at z>~2, so ~35-47% a0 precision gives 3-sigma. Below z~1 both branches sit near ~1-2.")
print("# DECISION THRESHOLDS (a clean deep-MOND a0(z) at z~2-3, g_bar<0.3 a0, on the ratio a0(z)/a0(0)):")
print("#   * a0(z=3)/a0(0) measured in [0.6,1.0] at <=35% => CONFIRMS declining/flat (Carl), EXCLUDES rising >3s.")
print("#   * a0(z=3)/a0(0) measured >~2 at <=35%          => CONFIRMS rising (McCulloch), EXCLUDES declining >3s.")
print("#   * a0(z=3)/a0(0) ~1 flat at <=15%               => Carl-compatible (declining ~ flat here) but MOND-degenerate.")
print("#   * DESI DR3 relaxes to w=-1 => declining branch COLLAPSES to flat -> fork UNTESTABLE (not falsified).")
print("# LOAD-BEARING CAVEATS (none overrideable):")
CAVEATS = [
 "MUSE-DARK III (Ciocan, arXiv:2604.22613) DIRECTLY measures a0 RISING and OVERSHOOTS McCulloch. It is the "
 "live TENSION for Carl's declining branch, reported as such -- NOT buried, NOT spun into support. Its pull "
 "is toward RISING. Face-value ~16s against declining; but LCDM-assembly-degenerate (Magneticum/Mayer+2023 "
 "reproduces ~x3 apparent-a0 rise with NO fundamental a0), so the honest residual vs declining SPANS ~0s "
 "(fully assembly) to ~4-5s (error-inflated); it is NOT a clean confirmation of EITHER branch (only ~1.5s from rising).",
 "MSA-3D (Espejo Salcedo, arXiv:2606.27853) uses the SELECTION-CORRECTED slope +0.91+/-0.79, NOT the raw "
 "+2.13 (which is >half g_obs-selection: total +2.13 = selection +1.13 + h(f_DM) +1.00). Central value mildly "
 "RISING but consistent with FLAT at ~1.1s -> UNDERPOWERED/WATCH, excludes no branch.",
 "bTFR zero-points are 4x-DESENSITIZED: bTFR ZP ~ a0^(1/4) => d a0/a0 = 4 d V/V. Errors carried are "
 "SYSTEMATICS-INCLUSIVE (+/-0.27-0.35 dex ~ a factor of 2 in a0), NOT the small +/-0.04-0.06 stat. Under those "
 "honest errors BOTH branches sit within ~1s of every bTFR point -> the bTFR arm is largely NON-diagnostic.",
 "Acceleration DILUTION: the deep-MOND mapping Delta_b=-log10(a0 ratio) assumes g_bar<<a0. Every published "
 "high-z bTFR sits at g_bar~(0.3-6)a0; the framework's own nu gives usable lever x/(2+x) = 7-63% of deep-MOND. "
 "Only Jeanneau (lensed, g_bar~0.3-1 a0) is near the a0 regime; it reads FLAT (Carl-compatible).",
 "LCDM-DEGENERACY of the RATIO test: a falling bTFR ZP is reproduced by standard LCDM disk/size evolution to "
 "within ~0.1 dex at every z probed. The fork (declining vs rising) is INTERNAL to the framework's two horizon "
 "readings; it is sharp between A and B but is NOT by itself an MI-vs-LCDM discriminator.",
 "SYSTEMATICS FLOOR (committed highz_systematics_floor.py): today's samples are NO-GO for a clean fork read "
 "(per-bin ~0.3 dex COHERENT bias -- pressure support tracks sigma_0(z), does NOT average down). Decisive likely "
 "~2035+ with ELT/ALMA cold tracers + DIRECT HI 21cm gas masses (SKA2/ngVLA, <0.05 dex, no alpha_CO).",
 "BOTH FOOTINGS carried: canonical a0(0)=cH_Lambda/Z=9.355e-11 and alt a0(0)=cH0/Z=1.131e-10. The RATIO "
 "a0(z)/a0(0) is FOOTING-INDEPENDENT (Z, a0(0) cancel) -> the fork placement is identical on both; only the "
 "absolute a0(z) scale moves.",
 "a0's VALUE and the HORIZON CHOICE are POSITS (not derived). nu=sqrt(1+1/y) is Milgrom 1999 (PLA 253:273 "
 "Eq.9). McCulloch (MiHsC / quantised inertia) is credited for the Hubble-horizon rising reading. No TOE; no "
 "'theory closed'. A NULL / mixed-and-weak outcome is stated as plainly as a win would be.",
]
for i, c in enumerate(CAVEATS, 1):
    print(f"#   {i}. {c}")
print("#" * 100)

# ======================================================================================
# SELF-CHECK  (frozen invariants)
# ======================================================================================
assert abs(MSA_SLOPE - 0.91) < 1e-9, "MSA-3D MUST use the selection-corrected +0.91, not the raw +2.13"
assert MSA_SLOPE < 2.0, "MSA-3D raw +2.13 (>half selection) must NOT be used"
assert 0.77 <= float(a0_deSitter(3.0)) <= 0.78, "declining branch @z3 must match committed fork (~0.775)"
assert 4.5 <= float(a0_Hubble(3.0)) <= 4.6, "rising branch @z3 must match committed fork (~4.54)"
assert a0_Hubble(3.0) / a0_deSitter(3.0) > 5.0, "z=3 divergence must exceed 5x (a FACTOR)"
assert sr_msa > 1.0 > sd_msa > -1.0, "rising slope strongly +, declining slope mildly -"
assert hD < nD, "de-systematization must REDUCE (not inflate) the MUSE-vs-declining tension"
print(f"\nSELF-CHECK OK: MSA-3D uses +{MSA_SLOPE:.2f} (NOT raw +2.13); declining@z3={float(a0_deSitter(3.0)):.3f}, "
      f"rising@z3={float(a0_Hubble(3.0)):.3f}, divergence {float(a0_Hubble(3.0)/a0_deSitter(3.0)):.1f}x.")
print("EXIT 0 (ran; not a verdict).")
