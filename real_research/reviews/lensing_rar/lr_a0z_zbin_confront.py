#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lr_a0z_zbin_confront.py -- confront the MEASURED a0(z_bin) against every committed branch.
==========================================================================================
Downstream of lr_a0z_zbin_measure.py.  That script produced the MEASUREMENT (per-lens-z-bin
free-a0 fit to the framework's OWN nu g_obs=sqrt(g_bar^2+g_bar*a0), 50-patch jackknife cov,
M/L 0.2 dex + one-sided CGM systematic).  Here we do ONLY the confrontation / scoring:

  For each committed a0(z) branch, normalized to a0(0) at BOTH footings (9.36e-11, 1.13e-10):
    Branch A -- canonical framework sqrt(rho_DE), DESI CPL w0=-0.752 wa=-0.86 (+6% bump, declining).
    Branch B -- sqrt(rho_total)=E(z), the framework's OWN self-labeled DISFAVORED rival / footing-bug.
    Branch C -- constant (w=-1), the safe geometric core.
    Verlinde  -- a0(z) proportional to cH(z) proportional to E(z) (same SHAPE as Branch B).

  Two observables:
   (I) ABSOLUTE per-bin chi^2 : predicted a0(z_i)=a0(0)*branch(z_i)/branch(0) at each footing vs the
       measured a0_i with FULL per-bin error (stat (+) syst in quadrature, in log10).  dof, sigma.
       -> This is footing-SENSITIVE and dominated by the ~0.25 dex CGM/M-L systematic (NON-diagnostic;
          we say so).  It answers 'is the canonical LEVEL 9.36e-11 (or 1.13e-10) at z consistent?'.
  (II) MODEL-INDEPENDENT slope / ratio : measured d ln a0 / dz (and ratio a0_hi/a0_lo) vs each branch's
       predicted slope.  Footing-INVARIANT (the a0(0) normalization cancels in a ratio) and baryon-shift
       -invariant (a z-common M/L shift cancels).  THIS is the load-bearing discriminator.

The MEASUREMENT is passed in as literals below (copied verbatim from the measure script's exit-0 run:
2-bin primary, REL cut g>1e-13, the load-bearing cut).  We do NOT re-stack; we confront.

Exit 0 = every branch scored at both footings for the 2-bin case + slope confrontation + 3-bin
handled (blocker-honest: the measurement has no clean 3-bin, so no 3-bin chi^2 is fabricated).
Committed 2026-07-06 as a verified NULL (adversarially checked, no branch excluded); local only, no push.
"""
import numpy as np
from scipy import stats
import os, sys

RR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # real_research/ (this file lives in real_research/reviews/lensing_rar/)
sys.path.insert(0, RR)
import a0z_clean_ledger as LED   # committed branch shapes (verified to match the prompt's tabulated ratios)

# ---- the committed branch SHAPES a0(z)/a0(0), normalized at z=0 -------------------------------
def branch_A(z):  return LED.m_framework(z) / LED.m_framework(0.0)     # canonical sqrt(rho_DE), DESI CPL
def branch_B(z):  return LED.m_rising_cH(z) / LED.m_rising_cH(0.0)     # sqrt(rho_total)=E(z), disfavored rival
def branch_C(z):  return LED.m_constant(z)                            # constant w=-1
def branch_V(z):  return LED.m_rising_cH(z) / LED.m_rising_cH(0.0)     # Verlinde a0 ~ cH ~ E(z) : SAME shape as B

BRANCHES = [
    ("BranchA-canon sqrt(rho_DE)", branch_A, "declining, +6% bump @z~0.4"),
    ("BranchB-rising sqrt(rho_tot)=E(z)", branch_B, "framework's self-labeled DISFAVORED rival"),
    ("BranchC-const w=-1", branch_C, "flat geometric core"),
    ("Verlinde ~ cH ~ E(z)", branch_V, "external rival, same shape as B"),
]

FOOTINGS = [("canonical a0(0)=9.36e-11", 9.36e-11), ("alt a0(0)=1.13e-10", 1.13e-10)]

# =================================================================================================
# THE MEASUREMENT (verbatim from lr_a0z_zbin_measure.py exit-0 run; REL cut g>1e-13, load-bearing).
# a0 in m/s^2; stat error is symmetric in log10 (dex); syst ~0.25 dex (half-width of the M/L->CGM band).
# =================================================================================================
BIN2 = [
    dict(name="low",  z_eff=0.2357, n=90739, a0=2.187e-10, stat_dex=0.041, syst_dex=0.25),
    dict(name="high", z_eff=0.3723, n=90738, a0=2.864e-10, stat_dex=0.044, syst_dex=0.25),
]
# measured ratio / slope (patch-consistent jackknife, from the measure script):
MEAS_RATIO           = 1.3093     # a0(high)/a0(low)
MEAS_SLOPE           = 1.9721     # d ln a0 / dz
MEAS_SLOPE_ERR_STAT  = 1.1586     # stat-only jackknife
# CORRECTION (all 3 adversarial verifiers, 2026-07-06): the two lens-z bins are NOT mass-matched --
# the r<20 magnitude limit makes the high-z bin 0.465 dex more massive in logM, so the CGM/M-L
# baryon systematic is NOT z-common and does NOT fully cancel in the ratio.  The earlier
# "syst cancels in the ratio" claim was an overclaim on precision.  A differential-CGM term
# ~0.90/z (50% CGM-model amplitude uncertainty over dlogM=0.465) adds in quadrature to the
# LOAD-BEARING slope error:
MEAS_SLOPE_ERR_SYST  = 0.90
MEAS_SLOPE_ERR       = float(np.sqrt(MEAS_SLOPE_ERR_STAT**2 + MEAS_SLOPE_ERR_SYST**2))  # ~1.47/z (honest)
MEAS_RATIO_ERR       = float(MEAS_SLOPE_ERR * MEAS_RATIO * (0.3723 - 0.2357))           # ~0.26 combined
# For the ABSOLUTE chi^2 (test I) the per-bin syst is included directly (ERR_ABS below).

Z = np.array([b["z_eff"] for b in BIN2])
LOGA0 = np.log10(np.array([b["a0"] for b in BIN2]))
# full per-bin error in log10 = stat (+) syst in quadrature (absolute-level test only)
ERR_ABS = np.sqrt(np.array([b["stat_dex"] for b in BIN2])**2 + np.array([b["syst_dex"] for b in BIN2])**2)
# stat-only per-bin error (for a footing-agnostic 'shape after free amplitude' cross-check)
ERR_STAT = np.array([b["stat_dex"] for b in BIN2])


def chi2_absolute(branch, a0_0):
    """chi^2 of the ABSOLUTE prediction a0(0)*branch(z)/branch(0) vs measured a0_i, full error, log10."""
    pred = a0_0 * branch(Z) / branch(0.0)
    resid = LOGA0 - np.log10(pred)
    chi2 = float(np.sum((resid / ERR_ABS)**2))
    dof = len(Z)                       # no free params -- the footing FIXES a0(0)
    return chi2, dof, resid


def chi2_shape_freeA(branch):
    """Footing-agnostic: fit a free log-amplitude A (absorbs a0(0) and any z-common baryon shift),
    then chi^2 of the SHAPE on stat-only error.  dof = Nbin-1.  This isolates the z-DEPENDENCE."""
    lp = np.log10(branch(Z) / branch(0.0))
    w = 1.0 / ERR_STAT**2
    A = np.sum((LOGA0 - lp) * w) / np.sum(w)      # best-fit log-amplitude
    resid = LOGA0 - lp - A
    chi2 = float(np.sum((resid / ERR_STAT)**2))
    dof = max(len(Z) - 1, 1)
    return chi2, dof, A


def sigma_from_chi2(chi2, dof):
    """Two-sided Gaussian-equivalent sigma of a chi^2 with dof (survival -> normal quantile)."""
    if dof <= 0:
        return float('nan')
    p = stats.chi2.sf(chi2, dof)                  # p-value (prob of a worse fit by chance)
    p = min(max(p, 1e-300), 1.0 - 1e-16)
    return float(stats.norm.isf(p / 2.0))         # two-sided


def verdict(sig):
    if not np.isfinite(sig):
        return "undetermined"
    if sig < 2.0:
        return "consistent"
    if sig < 3.0:
        return "disfavored"
    return "excluded"


def branch_slope(branch):
    """Predicted d ln a0 / dz over the measured z-pair (secant slope between the two bin means)."""
    r = branch(Z[1]) / branch(Z[0])
    return np.log(r) / (Z[1] - Z[0]), r


# =================================================================================================
def main():
    print("#" * 100)
    print("# lr_a0z_zbin_confront -- MEASURED a0(z_bin) vs committed branches, BOTH footings")
    print("#" * 100)
    print(f"\nMEASURED (2-bin primary, REL cut g>1e-13, framework's own nu):")
    for b in BIN2:
        print(f"  {b['name']:>4}: z_eff={b['z_eff']:.4f}  a0={b['a0']:.3e}  "
              f"stat={b['stat_dex']:.3f}dex syst~{b['syst_dex']:.2f}dex  N={b['n']}")
    print(f"  ratio a0(hi)/a0(lo) = {MEAS_RATIO:.4f} +/- {MEAS_RATIO_ERR:.4f}")
    print(f"  d ln a0/dz          = {MEAS_SLOPE:.4f} +/- {MEAS_SLOPE_ERR:.4f}  (per unit z; dz_bins={Z[1]-Z[0]:.4f})")

    # -------- (I) ABSOLUTE per-bin chi^2, BOTH footings --------
    print("\n" + "=" * 100)
    print("(I) ABSOLUTE per-bin chi^2  [predicted a0(0)*branch(z)/branch(0) vs measured, FULL err incl. syst]")
    print("    dof=2 (footing fixes a0(0), no free params).  FOOTING-SENSITIVE + syst-dominated => NON-diagnostic.")
    print("=" * 100)
    abs_records = []
    for fname, a0_0 in FOOTINGS:
        print(f"\n  --- footing: {fname} ---")
        print(f"    {'branch':<38}{'chi2':>9}{'dof':>5}{'sigma':>8}   verdict")
        for bname, bf, _ in BRANCHES:
            chi2, dof, _ = chi2_absolute(bf, a0_0)
            sig = sigma_from_chi2(chi2, dof)
            v = verdict(sig)
            print(f"    {bname:<38}{chi2:>9.2f}{dof:>5}{sig:>8.2f}   {v}")
            abs_records.append(dict(footing=fname, name=bname, chi2=chi2, dof=dof, sigma=sig, verdict=v))

    # -------- (II) SHAPE after free amplitude (footing-agnostic) --------
    print("\n" + "=" * 100)
    print("(II) SHAPE chi^2 after a FREE log-amplitude (absorbs a0(0) AND any z-common baryon shift)")
    print("     stat-only err; dof=1.  FOOTING-INVARIANT cross-check (shares the mass-mismatch caveat);")
    print("     the SLOPE (III, with the differential-CGM syst folded in) is the honest load-bearing test.")
    print("=" * 100)
    print(f"    {'branch':<38}{'chi2':>9}{'dof':>5}{'sigma':>8}   verdict")
    shape_records = []
    for bname, bf, _ in BRANCHES:
        chi2, dof, A = chi2_shape_freeA(bf)
        sig = sigma_from_chi2(chi2, dof)
        v = verdict(sig)
        print(f"    {bname:<38}{chi2:>9.2f}{dof:>5}{sig:>8.2f}   {v}   (bestA=10^{A:.3f}={10**A:.3e})")
        shape_records.append(dict(name=bname, chi2=chi2, dof=dof, sigma=sig, verdict=v))

    # -------- (III) MODEL-INDEPENDENT slope confrontation --------
    print("\n" + "=" * 100)
    print("(III) MODEL-INDEPENDENT slope: measured d ln a0/dz vs each branch's predicted slope")
    print("      (footing cancels in the ratio; z-common baryon shift cancels)")
    print("=" * 100)
    print(f"    measured d ln a0/dz = {MEAS_SLOPE:+.4f} +/- {MEAS_SLOPE_ERR:.4f}")
    print(f"    measured ratio hi/lo = {MEAS_RATIO:.4f} +/- {MEAS_RATIO_ERR:.4f}\n")
    print(f"    {'branch':<38}{'pred_slope':>11}{'pred_ratio':>11}{'(meas-pred)/sig_slope':>23}  verdict")
    slope_records = []
    for bname, bf, _ in BRANCHES:
        ps, pr = branch_slope(bf)
        nsig = (MEAS_SLOPE - ps) / MEAS_SLOPE_ERR
        v = verdict(abs(nsig))
        print(f"    {bname:<38}{ps:>+11.4f}{pr:>11.4f}{nsig:>+23.2f}  {v}")
        slope_records.append(dict(name=bname, pred_slope=ps, pred_ratio=pr, nsig=float(nsig), verdict=v))
    # also express via the ratio directly
    print("\n    (same test in ratio space, for cross-check):")
    for bname, bf, _ in BRANCHES:
        _, pr = branch_slope(bf)
        nsig_r = (MEAS_RATIO - pr) / MEAS_RATIO_ERR
        print(f"    {bname:<38} pred_ratio={pr:.4f}  (meas-pred)/sig_ratio = {nsig_r:+.2f}")

    # -------- 3-bin secondary --------
    print("\n" + "=" * 100)
    print("3-BIN SECONDARY")
    print("=" * 100)
    print("  BLOCKER (inherited from the measurement): the committed accumulator is 2-WAY in lens-z;")
    print("  a clean 3-bin a0(z) needs the 16 GB KiDS source re-stack (not run).  zbins_3 is EMPTY in the")
    print("  measurement, so NO 3-bin chi^2 is fabricated here.  The load-bearing confrontation is the")
    print("  2-bin slope (III) above, which is footing- and baryon-shift-invariant.")

    # -------- HEADLINE --------
    print("\n" + "=" * 100)
    print("HEADLINE (both-ways, no manufactured verdict)")
    print("=" * 100)
    sV = next(r for r in slope_records if r["name"].startswith("Verlinde"))
    sB = next(r for r in slope_records if r["name"].startswith("BranchB"))
    sA = next(r for r in slope_records if r["name"].startswith("BranchA"))
    sC = next(r for r in slope_records if r["name"].startswith("BranchC"))
    print(f"  * SLOPE (load-bearing, footing-invariant): measured +{MEAS_SLOPE:.2f}+/-{MEAS_SLOPE_ERR:.2f} per z.")
    print(f"      BranchA (canon decline) pred slope {sA['pred_slope']:+.3f} -> {abs(sA['nsig']):.2f}sig -> {sA['verdict']}")
    print(f"      BranchC (constant)      pred slope {sC['pred_slope']:+.3f} -> {abs(sC['nsig']):.2f}sig -> {sC['verdict']}")
    print(f"      BranchB (rising E(z))   pred slope {sB['pred_slope']:+.3f} -> {abs(sB['nsig']):.2f}sig -> {sB['verdict']}")
    print(f"      Verlinde (~cH~E(z))     pred slope {sV['pred_slope']:+.3f} -> {abs(sV['nsig']):.2f}sig -> {sV['verdict']}")
    print("  * A vs C: their predicted slopes differ by only ~0.06/z, far below the {:.2f}/z measured error".format(MEAS_SLOPE_ERR))
    print("    => UNDETERMINED. The signal is below precision; NO detection of the +6% bump is claimed.")
    print(f"  * B/Verlinde: the steep rise is NOT excluded either (within ~{abs(sV['nsig']):.2f}sig) -- but note the DATA")
    print(f"    slope is steeper than every branch, a mild (~{abs(sC['nsig']):.2f}sig vs flat) hint of RISING a0(z), not a kill.")
    print("  * ABSOLUTE level (I): syst-dominated (~0.25 dex CGM/M-L); neither 9.36e-11 nor 1.13e-10 is")
    print("    confirmed or refuted -- canonical sits at the EDGE of the fitter's one-sided syst band")
    print("    (reached only ~0.07 dex beyond the +0.30 dex CGM prior), NOT comfortably inside.")
    print("  * MUSE-DARK III cross-check: MUSE measures a0 RISING (~2.4e-10 at z~1, +1.59/z). The lensing")
    print(f"    slope's SIGN agrees with MUSE (both positive), but is statistically inconclusive (~{abs(sC['nsig']):.1f}sig) and")
    print("    LCDM-degenerate; it neither confirms MUSE's rise nor the framework's flat/mild-decline claim.")
    print("\nEXIT 0")

    # stash for structured return
    return dict(abs_records=abs_records, shape_records=shape_records, slope_records=slope_records)


if __name__ == "__main__":
    main()
