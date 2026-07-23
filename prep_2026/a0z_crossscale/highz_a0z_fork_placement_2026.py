#!/usr/bin/env python3
"""
highz_a0z_fork_placement_2026.py -- PLACE the real high-z a0(z) constraints on the HORIZON FORK.
=================================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA. Builds on (does NOT modify) the committed
  prep_2026/a0z_crossscale/desitter_unruh_horizon_fork_2026.py
which sets the fork: a0(z)/a0(0) reads
  (A) de Sitter / future-event horizon  [Carl's canonical]:  sqrt(rho_DE(z))  -> DECLINES (~0.78x@z3)
  (B) Hubble horizon  [McCulloch MiHsC; credited]:           E(z)=H(z)/H0     -> RISES  (~4.5x@z3)
and a pure-Lambda limit (C) FLAT (constant a0), which is Carl's side when w->-1.
Because the two horizons diverge by a FACTOR (5.9x@z3), a CRUDE high-z a0(z) point at tens-of-%
precision separates them at 3 sigma (19%/37%/47% at z=1/2/3). This script takes the REAL existing
high-z a0(z) constraints and, FOR EACH, computes: which branch it favors and at how many sigma
from declining vs from rising; then the COMBINED constraint; then the single decisive measurement.

HARD CALIBRATION (manufactured win == manufactured deficit; penalized equally):
  * MUSE-DARK III (Ciocan) leans RISING (favors McCulloch) -> reported as a TENSION for Carl, not spun.
  * MSA-3D: SELECTION-CORRECTED slope +0.91+/-0.79 (NOT the raw +2.13, which is >half g_obs-selection).
  * All points are REAL cited literature / committed digitized data; estimates are labeled.
  * a0's value + the horizon choice are POSITS; nu is Milgrom 1999 (PLA 253:273); McCulloch credited
    for the Hubble reading. No TOE. No 'theory closed'.

TWO MUSE-DARK PAPERS (do NOT conflate -- they are different samples and OPPOSITE results):
  * MUSE-DARK III = CIOCAN et al. 2026, A&A 709 L16 (arXiv:2604.22613): 79 non-lensed SFGs
    (M*>10^8.8), 0.33<z<1.44, MUSE HUDF. DIRECT a0(z) fit a0(z)=1.0+1.59 z [x1e-10] -> STRONG RISE.
  * MUSE-DARK II  = JEANNEAU et al. 2026, A&A (arXiv:2603.28856): 95 LENSED SFGs (M*=10^8.1-10.3),
    0.56<z<1.37 -> reaches g_bar~a0. bTFR zero-point Delta_b = 0.00+/-0.06(stat) -> FLAT.
  The task brief's "MUSE-DARK III, 95 lensed, 0.56-1.37, 0.00+/-0.27" MERGES the two; the 95-lensed
  0.00+/-0.27 is JEANNEAU (MUSE-DARK II, FLAT); the RISING a0 is CIOCAN (MUSE-DARK III). Both below.
"""
import numpy as np

np.seterr(all="ignore")

# ======================================================================================
# 1. THE FORK BRANCHES  (identical machinery to desitter_unruh_horizon_fork_2026.py)
# ======================================================================================
OM, OL = 0.315, 0.685
W0, WA = -0.838, -0.62          # DESI DR2 w0waCDM Pantheon+ central (the fork script's head)

def rho_de_ratio(z, w0=W0, wa=WA):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def a0_deSitter(z):   return np.sqrt(rho_de_ratio(z))              # (A) declining  [Carl]
def a0_Hubble(z):     return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + OL)  # (B) rising [McCulloch]
def a0_flat(z):       return np.ones_like(np.asarray(z, float))   # (C) pure-Lambda flat [Carl, w->-1]

def loglog_slope(fn, zlo, zhi, n=400):
    z = np.linspace(zlo, zhi, n)
    return float(np.polyfit(np.log10(1 + z), np.log10(fn(z)), 1)[0])

def lin_slope_ratio(fn, zlo, zhi, n=400):
    """slope d(a0(z)/a0(0))/dz of a branch, matching Ciocan's linear a1 units (a0(0)=1)."""
    z = np.linspace(zlo, zhi, n)
    y = fn(z) / fn(0.0)
    return float(np.polyfit(z, y, 1)[0])

bar = "=" * 100
print(bar); print("HIGH-z a0(z) CONSTRAINTS PLACED ON THE de Sitter-Unruh HORIZON FORK"); print(bar)
print("Fork branches (a0(z)/a0(0), DESI DR2 Pantheon+ w0wa):  (A) de Sitter=sqrt(rhoDE) DECLINES,")
print("(B) Hubble=E(z) RISES [McCulloch],  (C) pure-Lambda FLAT [Carl's w->-1 limit].")
print(f"  ratios:  z=1  A={a0_deSitter(1.0):.3f}  B={a0_Hubble(1.0):.3f}   |  "
      f"z=2  A={a0_deSitter(2.0):.3f}  B={a0_Hubble(2.0):.3f}   |  "
      f"z=3  A={a0_deSitter(3.0):.3f}  B={a0_Hubble(3.0):.3f}")
print(f"  divergence B/A: z=1 {a0_Hubble(1.)/a0_deSitter(1.):.1f}x  z=2 {a0_Hubble(2.)/a0_deSitter(2.):.1f}x  "
      f"z=3 {a0_Hubble(3.)/a0_deSitter(3.):.1f}x  -> a FACTOR, so tens-of-% precision forks it.")

# ======================================================================================
# 2. THE REAL DATA POINTS
#    Two currencies:
#      SLOPE points  : measured d log10(a0)/d log10(1+z) [or linear a1], vs branch slopes.
#      RATIO points  : measured a0(z_med)/a0(0) (from bTFR Delta_b via deep-MOND), vs branch ratios.
#    Each point carries: naive (stat-only) error AND honest (stat + documented systematics) error,
#    and a 'clean' flag = does it probe a0 in the low-acceleration (g_bar<~a0), non-degenerate regime.
# ======================================================================================

print("\n" + bar); print("2A. SLOPE-CURRENCY POINTS  (the M-L-offset-canceling observable)"); print(bar)

# --- branch slopes over each dataset's z-support ---
# MSA-3D golden support 0.58-1.68 (median z~1.1); MUSE-III 0.33-1.44.
sd_msa = loglog_slope(a0_deSitter, 0.58, 1.68); sr_msa = loglog_slope(a0_Hubble, 0.58, 1.68)
sd_mu  = lin_slope_ratio(a0_deSitter, 0.33, 1.44); sr_mu = lin_slope_ratio(a0_Hubble, 0.33, 1.44)
# MUSE-III also in log-log currency for the combined direct-probe statement:
sd_mu_ll = loglog_slope(a0_deSitter, 0.33, 1.44); sr_mu_ll = loglog_slope(a0_Hubble, 0.33, 1.44)

def sigmas(meas, err, s_decl, s_rise, s_flat=0.0):
    return (abs(meas - s_decl) / err, abs(meas - s_rise) / err, abs(meas - s_flat) / err)

# -------------------- MSA-3D (selection-corrected) --------------------
# Espejo Salcedo+2026 (arXiv:2606.27853), JWST/NIRSpec, 23 golden SFGs 0.58<z<1.68.
# Committed msa3d_a0z_selection_decomposition.py: raw +2.13 = g_obs-selection +1.13 + h(f_DM) +1.00;
# controlling for g_obs the GENUINE residual slope = +0.91 [16-84: +0.05,+1.63] -> sigma ~0.79.
msa_slope, msa_err = 0.91, 0.79
sD, sR, sF = sigmas(msa_slope, msa_err, sd_msa, sr_msa)
print(f"\n[MSA-3D sel-corrected]  d log10(a0)/d log10(1+z) = {msa_slope:+.2f} +/- {msa_err:.2f}  (z~0.58-1.68, N=23)")
print(f"   branch slopes over its range:  declining {sd_msa:+.2f}   rising {sr_msa:+.2f}   flat 0.00")
print(f"   -> {sD:.2f} sigma from DECLINING | {sR:.2f} sigma from RISING | {sF:.2f} sigma from FLAT")
print("   FAVORS: NOTHING SIGNIFICANTLY. UNDERPOWERED -- consistent with declining, flat (Carl's side)")
print("   AND rising AND Ciocan's slope, all within ~1.5s. Central value nominally nearest rising, but")
print("   the preference over flat is only ~0.8s (sub-significant). It EXCLUDES no branch and CONFIRMS none.")
print("   NOTE: g_bar/a0 ~ 0.2-6 (mixed, mostly g>~a0); absolute a0 M-L-degenerate; slope is the clean part.")

# -------------------- MUSE-DARK III (Ciocan) --------------------
# a0(z)=1.0+1.59 z [x1e-10]; a1=+1.59 (+0.11/-0.10) -> stat sigma ~0.105 /z. a0(z~1)=2.38.
mu_a1, mu_a1_stat = 1.59, 0.105
# honest error: fold the shared LCDM-assembly apparent-a0 drift (Magneticum/Mayer+2023, ~x3 to z=2.3,
# slope ~+0.80/z over this range) + un-budgeted pressure-support/M-L as a systematic on a1.
# Committed ciocan_a0z_FINAL_RECONCILE.py: real tension ~15s -> ~3-5s after this systematic.
slope_mag = 0.80                       # Magneticum LCDM-apparent slope over data range (ratio units /z)
mu_a1_sys = np.hypot(mu_a1_stat, 0.5 * slope_mag)   # add half the shared-drift slope as sys
sD, sR, sF = sigmas(mu_a1, mu_a1_stat, sd_mu, sr_mu)
hD, hR, hF = sigmas(mu_a1, mu_a1_sys, sd_mu, sr_mu)
print(f"\n[MUSE-DARK III / Ciocan]  d(a0/a0(0))/dz = a1 = {mu_a1:+.2f} +/- {mu_a1_stat:.3f} (stat)  (z~0.33-1.44, N=79)")
print(f"   branch linear slopes over its range:  declining {sd_mu:+.2f}   rising {sr_mu:+.2f}   flat 0.00")
print(f"   NAIVE stat:   {sD:.1f}s from DECLINING | {sR:.1f}s from RISING | {sF:.1f}s from FLAT")
print(f"   HONEST (a1 err inflated to {mu_a1_sys:.2f} by shared LCDM-assembly + pressure-support sys):")
print(f"                 {hD:.1f}s from DECLINING | {hR:.1f}s from RISING | {hF:.1f}s from FLAT")
print("   FAVORS: RISING over declining, HARD -> this is the live TENSION for Carl's declining branch.")
print("   BUT it OVERSHOOTS McCulloch too (rises FASTER than E(z)) and is LCDM-degenerate (Magneticum")
print("   reproduces ~half the slope with NO fundamental a0) -> NOT a clean confirmation of McCulloch either.")

# ======================================================================================
# 2B. RATIO-CURRENCY POINTS  (bTFR zero-points -> a0(z_med)/a0(0), deep-MOND mapping)
#     bTFR mass-axis offset Delta_b = -log10(a0(z)/a0(0))  (deep-MOND) => R = 10^(-Delta_b).
#     Velocity-axis desensitization: d a0/a0 = 4 d V/V, so a 4x-forgiving V precision.
#     Dilution: samples at g_bar>>a0 see only x/(2+x) of the a0-lever -> flagged as degenerate.
# ======================================================================================
print("\n" + bar); print("2B. RATIO-CURRENCY POINTS  (high-z TFR zero-points -> a0(z_med)/a0(0))"); print(bar)

def ratio_from_db(db, db_err):
    R = 10.0 ** (-db)
    sR = np.log(10.0) * R * db_err
    return R, sR

def place_ratio(label, z, db, db_err, clean, note):
    R, sR = ratio_from_db(db, db_err)
    Rd, Rr, Rf = float(a0_deSitter(z)), float(a0_Hubble(z)), 1.0
    sD, sRi, sF = abs(R - Rd) / sR, abs(R - Rr) / sR, abs(R - Rf) / sR
    fav = "RISING" if sRi < sD and sRi < sF else ("FLAT/Carl" if sF <= sD else "DECLINING/Carl")
    print(f"\n[{label}]  z~{z:.1f}  Delta_b={db:+.2f}+/-{db_err:.2f} dex -> a0(z)/a0(0) = {R:.2f} +/- {sR:.2f}  "
          f"[{'CLEAN low-acc' if clean else 'DEGENERATE g>>a0'}]")
    print(f"   branch ratios at z~{z:.1f}:  declining {Rd:.2f}   rising {Rr:.2f}   flat 1.00")
    print(f"   -> {sD:.2f}s from DECLINING | {sRi:.2f}s from RISING | {sF:.2f}s from FLAT   FAVORS: {fav}")
    print(f"   {note}")
    return dict(label=label, z=z, R=R, sR=sR, clean=clean, sD=sD, sR_=sRi, sF=sF)

ratio_pts = []
# JEANNEAU (MUSE-DARK II) -- the cleanest low-acceleration bTFR in hand.
ratio_pts.append(place_ratio(
    "MUSE-DARK II / Jeanneau bTFR", 0.9, 0.00, 0.27, True,
    "Cleanest LOW-ACC point (lensed, g_bar~0.3-1 a0). 0.00+/-0.06 stat; honest +/-0.27 incl gas-model"
    " (Tacconi+20+NUM HI 0.8dex) + local-ref +/-0.16. LEANS Carl's flat/declining side, weakly."))
# UBLER+17 bTFR z~0.9 and z~2.3
ratio_pts.append(place_ratio(
    "Ubler+17 KMOS3D bTFR", 0.9, -0.44, 0.35, False,
    "RISING pull, but g_bar>>a0 (dilutes a0-lever to ~20-60%), LCDM-halo + size-degenerate; and 6-sigma"
    " INTERNALLY INCONSISTENT with Jeanneau at the SAME z -> the z~1 bTFR is unresolved, not a clean a0 read."))
ratio_pts.append(place_ratio(
    "Ubler+17 KMOS3D bTFR", 2.3, -0.27, 0.35, False,
    "Between branches; g_bar~(2-6)a0 -> a0-lever ~7-18% only. -0.27 is simultaneously rising-shaped,"
    " LCDM-halo-shaped, and canonical+size-shaped (van der Wel compactness) -> WASH for the fork."))
ratio_pts.append(place_ratio(
    "Amvrosiadis+25 DSFG bTFR", 2.4, -0.26, 0.30, False,
    "Agrees with Ubler (the one reproduced high-z bTFR number), but N=12, alpha_CO-mediated, g>>a0 -> WASH."))

# ======================================================================================
# 3. COMBINED CONSTRAINT
# ======================================================================================
print("\n" + bar); print("3. COMBINED CONSTRAINT"); print(bar)

# (i) the two DIRECT a0(z) probes, in common log-log slope currency, honest errors.
# MUSE-III log-log slope of (1+1.59z) over 0.33-1.44, with honest error scaled from a1 (stat vs sys).
zz = np.linspace(0.33, 1.44, 400)
mu_ll = float(np.polyfit(np.log10(1 + zz), np.log10(1 + mu_a1 * zz), 1)[0])
# scale a1 stat/sys errors into the log-log slope by the local Jacobian (a1 -> mu_ll is ~linear here)
jac = mu_ll / mu_a1
mu_ll_stat, mu_ll_sys = mu_a1_stat * jac, mu_a1_sys * jac
print(f"  Direct a0(z) probes in log-log slope d log10(a0)/d log10(1+z):")
print(f"    MSA-3D  = {msa_slope:+.2f} +/- {msa_err:.2f}")
print(f"    Ciocan  = {mu_ll:+.2f} +/- {mu_ll_stat:.2f} (stat) / {mu_ll_sys:.2f} (honest w/ LCDM-assembly sys)")
print(f"    branch log-log slopes (0.3-1.7): declining ~{sd_msa:+.2f}  rising ~{sr_msa:+.2f}  flat 0.00")

for tag, mu_err in [("NAIVE stat", mu_ll_stat), ("HONEST (Ciocan sys-inflated)", mu_ll_sys)]:
    w1, w2 = 1 / msa_err ** 2, 1 / mu_err ** 2
    comb = (msa_slope * w1 + mu_ll * w2) / (w1 + w2)
    comb_err = (w1 + w2) ** -0.5
    cD, cR, cF = abs(comb - sd_msa) / comb_err, abs(comb - sr_msa) / comb_err, abs(comb - 0) / comb_err
    print(f"    [{tag}] inverse-variance combined slope = {comb:+.2f} +/- {comb_err:.2f}"
          f"  -> {cD:.1f}s from declining | {cR:.1f}s from rising | {cF:.1f}s from flat")

print("\n  (ii) the bTFR / RATIO arm is SPLIT and mostly degenerate:")
clean_leans = [p for p in ratio_pts if p["clean"]]
print(f"    - CLEAN low-acc (Jeanneau bTFR): leans Carl's flat/declining side "
      f"({clean_leans[0]['sF']:.1f}s from flat vs {clean_leans[0]['sR_']:.1f}s from rising).")
print("    - DEGENERATE (Ubler z0.9, Ubler/Amvrosiadis z2.3-2.4): negative Delta_b = rising PULL, but")
print("      g_bar>>a0 + LCDM-halo + size degeneracy => cannot attribute to a0 -> WASH, not a fork read.")

print("\n  (iii) external bounds (context, real & cited):")
print("    - McGaugh+24 (arXiv:2406.17930) BTFR/f_DM to z~2.5: 'no clear evolution' -> favors Carl's flat side.")
print("    - Milgrom 2017 (arXiv:1703.06110) direct high-z RC: 'all but excludes' a x4 a0 rise AND the")
print("      (1+z)^1.5 law -> BOUNDS steep rises; would EXCLUDE the full McCulloch branch (x4.5@z3) at high z.")

# ======================================================================================
# 4. VERDICT + DECISIVE MEASUREMENT
# ======================================================================================
print("\n" + bar); print("4. HONEST VERDICT -- does current crude high-z data pick a branch?"); print(bar)
print("""  DO THEY AGREE OR CONFLICT?  They CONFLICT, and the net is MIXED + WEAK:
   * The single STRONGEST direct measurement (Ciocan/MUSE-DARK III, ~15s stat) leans RISING and is a
     genuine TENSION for Carl's declining branch -- stated plainly, not spun. Its raw precision (a0@z~1
     to ~6%) FAR exceeds the fork's ~19% requirement, so on PRECISION it reaches the fork and picks rising.
   * BUT it FAILS the fork's CLEANLINESS requirement: it OVERSHOOTS even McCulloch (rises faster than
     E(z)) and is LCDM-assembly-degenerate (an LCDM sim with NO fundamental a0 reproduces ~half its
     slope). So it does not cleanly confirm McCulloch, and its honest fundamental-a0 tension is ~3-5s.
   * The OTHER direct probe (MSA-3D, selection-corrected +0.91+/-0.79) is UNDERPOWERED: its central value
     sits nearest the rising branch (~0.4s) yet is only ~1.1-1.5s from Carl's flat/declining side -> it
     EXCLUDES nothing and does NOT corroborate Ciocan's strong rise.
   * The cleanest LOW-ACCELERATION probe (Jeanneau/MUSE-DARK II bTFR, 0.00+/-0.27) is FLAT -> leans
     Carl's side, and is ~6s inconsistent with Ubler at the same z (the z~1 bTFR is itself unresolved).
   * McGaugh+24 + Milgrom17 favor constancy and BOUND steep rises (Milgrom would exclude the full
     McCulloch branch at high z).

  NET: current crude high-z a0(z) data do NOT decisively pick a branch. The pull of the highest-
  significance single point (Ciocan) is toward RISING/McCulloch = a real tension for the declining
  branch; but that point is degeneracy-contaminated and overshoots McCulloch, while the clean low-
  acceleration constraint (Jeanneau) and the constancy bounds (McGaugh, Milgrom) lean Carl's side.
  The fork's PRECISION target is met; its CLEANLINESS target (a FUNDAMENTAL a0 in the g<<a0 regime,
  free of assembly/dilution degeneracy) is met by NO current measurement. Honest label: MIXED /
  UNDERPOWERED-FOR-A-CLEAN-FORK, with a degeneracy-contaminated net lean toward rising.

  THE SINGLE DECISIVE NEW MEASUREMENT:
   A CLEAN deep-MOND rotation curve / RAR at z~2-3, LOW-ACCELERATION selected (g_bar < ~0.3 a0, where
   fitted a0 = fundamental a0 and the assembly/size/dilution degeneracies all vanish), measured to
   ~30-40% a0 precision. At z=2 the branches are 3.5x apart (declining 0.87 vs rising 3.03), so ~37%
   a0 suffices for 3s; at z=3 they are 5.9x apart (~47% suffices). Instrument: JWST NIRSpec-IFU on
   LENSED low-mass rotators / dwarfs at z~2-3 (+ ALMA CO/[CII] for the cold-gas velocity field). One
   clean lensed dwarf RC at z~3, g<0.3a0, sigma(a0)~35%, forks it in a single pointing; a small sample
   (N~15-40, the banked forecast) does it robustly. This is the crude-but-CLEAN point the fork needs --
   NOT more RAR-fits on massive intermediate-z SFGs, where the LCDM apparent-a0 contaminates the signal.""")

# ======================================================================================
# SELF-CHECK
# ======================================================================================
assert sr_msa > 1.0 > sd_msa > -1.0, "rising slope must be strongly +, declining mildly -"
assert a0_Hubble(3.0) / a0_deSitter(3.0) > 5.0, "z=3 divergence must exceed 5x"
r0 = ratio_from_db(0.0, 0.27)[0]
assert abs(r0 - 1.0) < 1e-9, "Delta_b=0 -> ratio 1"
print("\nSELF-CHECK OK: declining slope %.2f (mild -), rising slope %.2f (strong +), z=3 divergence %.1fx."
      % (sd_msa, sr_msa, a0_Hubble(3.0) / a0_deSitter(3.0)))
print("EXIT 0 (ran; not a verdict).")
