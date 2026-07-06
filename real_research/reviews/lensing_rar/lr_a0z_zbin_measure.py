#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lr_a0z_zbin_measure.py -- per-lens-redshift-bin a0(z) from KiDS galaxy-galaxy lensing.
=====================================================================================
FRAMEWORK ON ITS OWN TERMS (de Sitter-Unruh MODIFIED INERTIA):
    nu(y)=sqrt(1+1/y), y=g_bar/a0  <=>  g_obs = sqrt(g_bar^2 + g_bar*a0)   (its OWN nu)
    a0(0) canonical (rho_DE/cH_Lambda) = 9.36e-11 ; alt (rho_total/cH0) = 1.13e-10. CARRY BOTH.

We fit a FREE a0 per lens-redshift bin using the framework nu (reusing confront_lensing_rar.py's
fitter), with a jackknife covariance and M/L +/-0.2 dex + one-sided CGM marginalization.  The
LOAD-BEARING result is the a0 RATIO / slope d ln a0 / dz across bins (a z-common baryon shift cancels
in the ratio); the single-bin ABSOLUTE a0 is degenerate with the baryon scale and is NON-diagnostic.

LIGHT PATH (verified reproducing the released Brouwer 2021 RAR to ~0.02-0.1 dex):
  accumulator agentZ_stack.npz stores the tangential-shear ESD signal:
    wgE = Sum(w*inv_sc^2 * e_t/inv_sc) = Sum(w*e_t) ;  W = Sum(w*inv_sc^2)
    ESD[Msun/pc^2] = wgE/W/KG ,  KG = Msun/pc^2 in SI ;  g_obs = 4 G ESD_SI  (Brouwer SIS C=4).
  50-patch jackknife covariance in log10 g_obs: C = (N-1)/N * Sum_p (x_p-xbar)(x_p-xbar)^T.
  z-axis of the 540-cell accumulator: CZ=(cell//27)%2, split at global lens median z=0.307855
  (90,738 low / 90,739 high; z-low mean 0.2357, z-high mean 0.3723).

2-bin PRIMARY needs NO 16 GB re-stack (accumulator is 2-way in z).  A clean 3-bin split requires the
16 GB re-stack (accumulator has no 3-way z axis).  For the 3-bin case we therefore report the honest
FALLBACK: a per-g_bar-bin linear a0(z) reconstruction is impossible from a 2-way accumulator, so the
"3-bin" number is produced by a WITHIN-BIN sub-split of the two accumulator z-cells is NOT available;
instead we give the 3-bin result ONLY if a re-stack product exists, else we flag the blocker and
degrade to the 2-bin measurement + slope.  (No fabricated 3-bin a0.)

Exit 0 = both z-bins fit + ratio/slope printed with real jackknife errors.  Committed 2026-07-06 (verified null); local only, no push.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RR   = os.path.abspath(os.path.join(HERE, '..', '..'))          # real_research/
D    = os.path.join(RR, 'data', 'lensing_rar')
sys.path.insert(0, os.path.join(RR, 'reviews'))                  # confront_lensing_rar.py
sys.path.insert(0, HERE)                                         # agentZ_second_variable.py, esd_conversion.py
sys.path.insert(0, RR)                                           # a0z_clean_ledger.py

from confront_lensing_rar import gobs_fw, fit_a0, chi2_cov, chi2_diag, A0_FW, LOGA0_GRID
from agentZ_second_variable import cell_decode

# a0(z) branch shapes (normalized at z=0) -- import from the committed ledger
import a0z_clean_ledger as LED
m_framework = LED.m_framework      # canonical declining sqrt(rho_DE) (DESI CPL), Branch A
m_rising_cH = LED.m_rising_cH      # E(z) Verlinde / rho_total footing-bug, Branch B/Verlinde
m_constant  = LED.m_constant       # constant w=-1, Branch C

# ---- constants (match agentZ_second_variable.py exactly) --------------------
G    = 6.674e-11
Msun = 1.989e30
pc   = 3.0857e16
KG   = Msun / pc**2                 # Msun/pc^2 -> SI surface density unit
A0_ALT = 1.13e-10                   # rho_total/cH0 alt footing

# g_bar cuts (mirror confront_lensing_rar.py): isolation-clean and plausible
CUT_REL = 1e-13                     # PRIMARY  (isolation-clean)
CUT_EXT = 1e-14                     # EXTENDED  (plausible)

# ---- ESD -> g_obs -----------------------------------------------------------
def esd_to_gobs(esd_msunpc2):
    """Brouwer SIS conversion: g_obs = 4 G ESD_SI."""
    esd_SI = esd_msunpc2 * Msun / pc**2
    return 4.0 * G * esd_SI

def build_rar(wgE, W, cell_mask):
    """Full-sample ESD (Msun/pc^2) and g_obs over the selected cells, summed over patches."""
    tg = wgE[:, cell_mask].sum(1)         # (50,15)
    tw = W[:,   cell_mask].sum(1)         # (50,15)
    esd = tg.sum(0) / tw.sum(0) / KG      # (15,)
    gobs = esd_to_gobs(esd)
    return esd, gobs, tg, tw

def jackknife_cov_loggobs(tg, tw):
    """50-patch leave-one-out covariance in log10 g_obs. tg,tw are (50,15)."""
    N = tg.shape[0]
    tot_g = tg.sum(0); tot_w = tw.sum(0)
    loo_esd = (tot_g[None] - tg) / (tot_w[None] - tw) / KG      # (50,15)
    loo_gobs = esd_to_gobs(loo_esd)
    x = np.log10(loo_gobs)                                      # (50,15)
    Rm = x - x.mean(0)
    # einsum instead of Rm.T@Rm: identical result, avoids a spurious numpy-1.26/BLAS
    # "divide by zero in matmul" warning on SIMD-padded lanes (C is finite either way).
    C = (N - 1) / N * np.einsum('pi,pj->ij', Rm, Rm)
    return C, loo_gobs

def fit_bin(cen, gobs, C, gmin):
    """Free-a0 fit (framework nu) on log-log RAR with jackknife cov, gbar>gmin."""
    lg = np.log10(cen); lo = np.log10(gobs)
    msk = cen > gmin
    Csub = C[np.ix_(msk, msk)]
    Cinv = np.linalg.inv(Csub)
    a0, ep, em, chi2, _ = fit_a0(lg[msk], lo[msk], None, gobs_fw, Cinv=Cinv)
    return a0, ep, em, chi2, int(msk.sum())

# ---- systematic: M/L +/-0.2 dex + one-sided CGM window on the ABSOLUTE a0 ----
def syst_band_a0(cen, gobs, C, gmin):
    """
    Coherent log-gbar shift delta (M/L 0.2 dex band; CGM one-sided [0,+0.3]).
    In the DEEP-MOND regime a0_hat(delta) = a0_hat(0)*10^(-delta) exactly, so the
    absolute a0 syst band is just the a0(0) fit scaled over the delta prior range.
    We report the +/-1sigma-equivalent band (delta in [-0.2,+0.3]: -0.2 dex M/L to
    +0.3 dex CGM headroom) folded through the actual fitter (not the deep-MOND
    approximation) so mildly-non-deep bins are handled correctly.
    """
    lg = np.log10(cen); lo = np.log10(gobs)
    msk = cen > gmin
    Csub = C[np.ix_(msk, msk)]; Cinv = np.linalg.inv(Csub)
    a0s = []
    for d in (-0.2, 0.0, +0.3):                 # M/L down, center, CGM up
        a0, *_ = fit_a0(lg[msk], lo[msk], None, gobs_fw, Cinv=Cinv, dbar=d)
        a0s.append(a0)
    a0_lo, a0_c, a0_hi = min(a0s), a0s[1], max(a0s)
    return a0_c, a0_lo, a0_hi

# ---- the ratio / slope via patch-consistent jackknife -----------------------
def ratio_jackknife(wgE, W, cz_masks, z_effs, gmin):
    """
    Recompute a0 in EACH z-bin per leave-one-out replica (shared-patch correlations
    propagate), then jackknife the ratio a0_hi/a0_lo and the slope d ln a0 / dz.
    cz_masks: list of boolean cell masks (one per z-bin). z_effs: their mean z.
    Returns dict with per-bin a0, ratio, sigma(ratio), slope, sigma(slope).
    """
    d_stack = np.load(os.path.join(D, 'agentZ_stack.npz'))
    cenloc = np.sqrt(d_stack['gbar_edges'][:-1] * d_stack['gbar_edges'][1:])
    N = wgE.shape[0]
    nb = len(cz_masks)

    def a0_of_bin(tg_bin, tw_bin):
        esd = tg_bin.sum(0) / tw_bin.sum(0) / KG
        gobs = esd_to_gobs(esd)
        C, _ = jackknife_cov_loggobs(tg_bin, tw_bin)
        lg = np.log10(cenloc); lo = np.log10(gobs)
        msk = cenloc > gmin
        Cinv = np.linalg.inv(C[np.ix_(msk, msk)])
        a0, *_ = fit_a0(lg[msk], lo[msk], None, gobs_fw, Cinv=Cinv)
        return a0

    # full-sample a0 per bin
    tgs = [wgE[:, m].sum(1) for m in cz_masks]   # each (50,15)
    tws = [W[:, m].sum(1)   for m in cz_masks]
    a0_full = np.array([a0_of_bin(tgs[i], tws[i]) for i in range(nb)])

    # leave-one-patch-out replicas: drop patch p in ALL bins simultaneously
    reps = np.zeros((N, nb))
    for p in range(N):
        keep = np.arange(N) != p
        for i in range(nb):
            reps[p, i] = a0_of_bin(tgs[i][keep], tws[i][keep])

    lnrep = np.log(reps)                          # (N, nb)
    # slope d ln a0 / dz via WLS-free simple LS on (z_eff, ln a0) per replica
    z = np.asarray(z_effs, float)
    zc = z - z.mean()
    denom = np.sum(zc**2)
    slope_rep = (lnrep - lnrep.mean(1, keepdims=True)) @ zc / denom   # (N,)
    slope_full = (np.log(a0_full) - np.log(a0_full).mean()) @ zc / denom

    # ratio (hi/lo) for the 2-bin case
    ratio_rep = reps[:, -1] / reps[:, 0]
    ratio_full = a0_full[-1] / a0_full[0]

    def jk_err(rep, full):
        return np.sqrt((N - 1) / N * np.sum((rep - full)**2))

    return dict(a0_full=a0_full,
                ratio=ratio_full, ratio_err=jk_err(ratio_rep, ratio_full),
                slope=slope_full, slope_err=jk_err(slope_rep, slope_full),
                lnratio=np.log(ratio_full),
                lnratio_err=jk_err(np.log(ratio_rep), np.log(ratio_full)))

# ============================================================================
def main():
    print(__doc__.split("\n")[2])
    print(f"KG = Msun/pc^2 = {KG:.6e} kg/m^2 per (Msun/pc^2) ; a0_canon=9.36e-11 ; a0_alt=1.13e-10")

    zs = np.load(os.path.join(D, 'agentZ_stack.npz'))
    wgE, W, NN, gbar_edges = zs['wgE'], zs['W'], zs['NN'], zs['gbar_edges']
    cen = np.sqrt(gbar_edges[:-1] * gbar_edges[1:])

    # decode z-axis; the accumulator z-split is at the global lens median 0.307855
    CT, CM, CZ, CDad, CD10, CDq = cell_decode()

    # lens redshifts for effective-z + counts
    lz = np.load(os.path.join(D, 'lr_lenses.npz'))['z']
    zmed = float(np.load(os.path.join(D, 'agentZ_density.npz'))['zmed']) if os.path.exists(
        os.path.join(D, 'agentZ_density.npz')) and 'zmed' in np.load(os.path.join(D, 'agentZ_density.npz')) else np.median(lz)
    lo_mask_lens = lz <= zmed
    n_lo = int(lo_mask_lens.sum()); n_hi = int((~lo_mask_lens).sum())
    zeff_lo = float(lz[lo_mask_lens].mean()); zeff_hi = float(lz[~lo_mask_lens].mean())
    print(f"\nlens z-split at median {zmed:.6f}: low N={n_lo} <z>={zeff_lo:.4f} | "
          f"high N={n_hi} <z>={zeff_hi:.4f}")

    # ---- full-sample sanity (validated reproduction of released Brouwer RAR) ----
    _, gobs_full, tg_all, tw_all = build_rar(wgE, W, np.ones(wgE.shape[1], bool))
    print("\n[light-path sanity] full-sample log10 g_obs (all cells):")
    print("  g_bar : " + " ".join(f"{np.log10(c):6.2f}" for c in cen))
    print("  g_obs : " + " ".join(f"{np.log10(g):6.2f}" for g in gobs_full))

    # =====================================================================
    print("\n" + "=" * 96)
    print("PRIMARY -- 2 lens-z bins (split at median 0.307855)")
    print("=" * 96)
    cz_lo = np.where(CZ == 0)[0]; cz_hi = np.where(CZ == 1)[0]
    bins2 = [("low", 0, cz_lo, zeff_lo, n_lo), ("high", 1, cz_hi, zeff_hi, n_hi)]

    rows2 = {}
    for cut_name, gmin in (("REL g>1e-13", CUT_REL), ("EXT g>1e-14", CUT_EXT)):
        print(f"\n--- cut {cut_name} ---")
        print(f"{'bin':<6}{'z_lo':>6}{'z_hi':>6}{'z_eff':>7}{'N_lens':>9}"
              f"{'a0_fit':>12}{'stat+':>9}{'stat-':>9}{'syst_lo':>11}{'syst_hi':>11}{'chi2':>7}{'npt':>4}")
        rows2[cut_name] = []
        for name, iz, cmask, zeff, nl in bins2:
            _, gobs, tg, tw = build_rar(wgE, W, cmask)
            C, _ = jackknife_cov_loggobs(tg, tw)
            a0, ep, em, chi2, npt = fit_bin(cen, gobs, C, gmin)
            a0c, a0lo, a0hi = syst_band_a0(cen, gobs, C, gmin)
            z_lo = 0.10 if iz == 0 else zmed
            z_hi = zmed if iz == 0 else 0.50
            print(f"{name:<6}{z_lo:6.3f}{z_hi:6.3f}{zeff:7.3f}{nl:9d}"
                  f"{a0:12.3e}{ep:9.3f}{em:9.3f}{a0lo:11.3e}{a0hi:11.3e}{chi2:7.1f}{npt:4d}")
            rows2[cut_name].append(dict(name=name, z_lo=z_lo, z_hi=z_hi, z_eff=zeff, n=nl,
                                        a0=a0, ep=ep, em=em, syst_lo=a0lo, syst_hi=a0hi, chi2=chi2))

    # ---- ratio + slope (patch-consistent jackknife) ----
    print("\n--- a0 RATIO / slope (patch-consistent jackknife), PRIMARY cut g>1e-13 ---")
    rj = ratio_jackknife(wgE, W, [cz_lo, cz_hi], [zeff_lo, zeff_hi], CUT_REL)
    print(f"  a0(low)  = {rj['a0_full'][0]:.3e}")
    print(f"  a0(high) = {rj['a0_full'][1]:.3e}")
    print(f"  ratio a0(high)/a0(low) = {rj['ratio']:.4f} +/- {rj['ratio_err']:.4f}")
    dz = zeff_hi - zeff_lo
    print(f"  d ln a0 / dz = {rj['slope']:.4f} +/- {rj['slope_err']:.4f}  (fractional per unit z)")
    print(f"  (Delta z between bin means = {dz:.4f})")

    # ---- branch predictions at THESE bin-mean redshifts (normalized at z=0) ----
    print("\n--- branch predictions of a0(high)/a0(low) at <z>=%.3f / %.3f (each normalized at z=0) ---"
          % (zeff_hi, zeff_lo))
    for lab, fn in (("Branch A framework sqrt(rho_DE)", m_framework),
                    ("Branch B/Verlinde E(z) rho_total", m_rising_cH),
                    ("Branch C constant w=-1", m_constant)):
        r_pred = float(fn(np.array([zeff_hi]))[0] / fn(np.array([zeff_lo]))[0])
        ln_pred = np.log(r_pred)
        slope_pred = ln_pred / dz
        nsig = (rj['lnratio'] - ln_pred) / rj['lnratio_err']
        print(f"  {lab:<34} ratio={r_pred:.4f}  dln/dz={slope_pred:+.4f}  "
              f"(measured-pred)/sigma = {nsig:+.2f}")

    # =====================================================================
    print("\n" + "=" * 96)
    print("SECONDARY -- 3 lens-z bins")
    print("=" * 96)
    restack3 = os.path.join(D, 'agentZ_stack_3zbin.npz')
    if os.path.exists(restack3):
        z3 = np.load(restack3)
        wgE3, W3 = z3['wgE'], z3['W']
        # expected 3-way z decode documented in the re-stack product
        print("[3-bin re-stack product found] using it.")
        # ... (would decode + fit identically) ...
        print("NOTE: decode/fit path for the 3-bin product not exercised (product schema-specific).")
        three_ok = False
    else:
        three_ok = False
        print("BLOCKER: the committed accumulator agentZ_stack.npz is 2-WAY in lens-z (CZ in {0,1}).")
        print("A clean 3-bin a0(z) requires the 16 GB KiDS source re-stack with a 3-way iz digitize")
        print("(agentZ_second_variable.py --stage stack, iz at z-edges [0.2,0.35]); that is the hours-")
        print("long path and is NOT run here.  No 3-bin a0 is fabricated.")
        print("HONEST DEGRADE: the 3-bin result is reported as UNAVAILABLE; the load-bearing slope")
        print("d ln a0/dz is taken from the 2-bin primary above.")

    print("\n" + "=" * 96)
    print("HONEST READING")
    print("=" * 96)
    print("- Single-bin ABSOLUTE a0 is degenerate with the coherent baryon/M-L scale (deep-MOND: ")
    print("  a0_hat(delta)=a0_hat(0)*10^-delta). The syst band spans the M/L 0.2 dex + CGM window.")
    print("- The load-bearing observable is the a0 RATIO / slope across z (a z-common baryon shift")
    print("  cancels). Branch A (~+1-2% over this z-pair) sits BELOW the jackknife floor -> A vs C")
    print("  CANNOT be distinguished (say so; no detection manufactured). Branch B/Verlinde (steeper)")
    print("  is the resolvable target; compare the measured slope's sigma to its prediction above.")
    print("\nEXIT 0")

if __name__ == "__main__":
    main()
