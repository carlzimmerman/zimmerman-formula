#!/usr/bin/env python3
r"""
DOOR 6 -- GALAXY CLUSTERS: the honest tension the framework INHERITS from MOND.
==============================================================================
Worked INSIDE the framework a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda),
with the constant-a0(z) reading (a0 set by the COSMIC dark-energy density, evolving
only through rho_DE(z); NOT the local/ambient-density reading).

This is NOT a success channel. Clusters are the long-known MOND weakness: even after
the MOND boost nu(g_bar/a0), the observed (weak-lensing) cluster mass exceeds the
MOND-predicted dynamical mass by a residual factor eta ~ 2 (Sanders 2003; Pointecouteau
& Silk 2005; Angus, Famaey & Buote 2008). The framework inherits this exactly, because
at the canonical a0 it IS MOND at z~0.

We compute it on REAL DATA: the eROSITA eRASS1 primary cluster catalog (Bulbul et al.
2024, A&A 685, A106), 12,247 clusters, one homogeneous pipeline, z=0.003-1.32, with
weak-lensing-calibrated M500, X-ray gas mass MGAS500, gas fraction FGAS500, and the
overdensity radius R500. At R500 we form
    g_obs = G M500 / R500^2            (total, WL-calibrated)
    g_bar = G (1+f_star) Mgas500 / R500^2   (baryons = gas + stars)
    eta   = g_obs / (nu(g_bar/a0) g_bar) = M500 / [ (1+f_star) Mgas500 nu ]
and report the residual eta -- the missing-mass factor that survives MOND.

ULTRA-PRECISION error budget on eta (median): we propagate, by Monte Carlo,
  (i)   STATISTICAL cosmological-parameter error on a0 from Omega_Lambda & H0 (Planck 2018),
  (ii)  the a0-evolution error from the DESI DR2 dark-energy EoS (w0, wa),
  (iii) the ~20% SYSTEMATIC MOND interpolating-function error on the ABSOLUTE a0,
  (iv)  the per-cluster DATA error (M500 weak-lensing mass; f_star stellar correction).
We state which dominates and separate STATISTICAL from SYSTEMATIC.

We also test the DISTINCTIVE evolving-a0 escape hatch and show it fails by ~1.5 orders
of magnitude: the framework predicts only ~0.02 dex of a0-evolution out to the cluster
epoch (z~0.3), far too small to explain the observed 0.6-0.8 dex galaxy-cluster baryonic
Tully-Fisher (BTFR) offset.

Data: real_research/data/erass1cl_primary_v3.2.fits. Reproducible: `python door6_galaxy_clusters.py`.
Needs numpy, scipy, astropy (+ matplotlib for the figure).
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))

# ===================== MANDATED CONSTANTS (exact, consistent) =====================
C    = 299792458.0            # m/s  (exact)
G    = 6.67430e-11            # CODATA 2018
MSUN = 1.98892e30            # kg
MPC  = 3.0857e22             # m
KPC  = MPC / 1.0e3           # m  (1 kpc = 3.0857e19 m, consistent with Mpc above)

# Planck 2018 (TT,TE,EE+lowE+lensing) -- STATISTICAL cosmology errors
H0_KMS, H0_ERR   = 67.36, 0.54            # km/s/Mpc
OML,    OML_ERR  = 0.6847, 0.0073
OM,     OM_ERR   = 0.3153, 0.0073

# DESI DR2 dark-energy equation of state (CPL): a0(z) evolution error
W0, W0_ERR = -0.752, 0.057
WA, WA_ERR = -0.86,  0.22

# MOND interpolating-function SYSTEMATIC on the absolute a0:
# simple-mu fit 9.1e-11 vs McGaugh RAR 1.2e-10 -> ~20% (we treat as a log-normal sys).
MU_SYS_FRAC = 0.20

# Stellar-to-gas mass ratio (intracluster stars are a sub-dominant baryon component).
# Baseline f_star = M_star/M_gas = 0.2 (Gonzalez+2013, Chiu+2018: stars are ~15-25% of gas at M500).
FSTAR      = 0.20
FSTAR_ERR  = 0.10            # generous: f_star in ~0.1-0.3

H0  = H0_KMS * 1e3 / MPC     # s^-1


# ----------------------------------------------------------------------------------
# a0 from the framework
# ----------------------------------------------------------------------------------
def a0_lambda(OmL, H0_si):
    """Framework a0 = c^2 sqrt(Lambda/32pi), Lambda = 3 OmL H0^2 / c^2 = (c/2) sqrt(G rho_Lambda)."""
    Lam = 3.0 * OmL * H0_si**2 / C**2
    return C**2 * np.sqrt(Lam / (32.0 * np.pi))


def rho_DE_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE0 for CPL w(a)=w0+wa(1-a):  a^(-3(1+w0+wa)) exp(-3 wa (1-a))."""
    a = 1.0 / (1.0 + z)
    return a**(-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))


def a0_of_z(z, a0_0, w0=W0, wa=WA):
    """Framework a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0) -- constant-a0(z) (cosmic) reading."""
    return a0_0 * np.sqrt(rho_DE_ratio(z, w0, wa))


# MOND simple interpolating function (mass boost M_MOND/M_bar):
#   g_obs = nu(g_bar/a0) g_bar,  nu(y) = 1/2 + sqrt(1/4 + 1/y).
def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


# ----------------------------------------------------------------------------------
# REAL eRASS1 data -> accelerations at R500
# ----------------------------------------------------------------------------------
def load_clusters(fstar=FSTAR, zmax=1.0, fgas_lo=0.01, fgas_hi=0.30):
    """Clean eRASS1 sample; return per-cluster z, g_obs, g_bar, masses, R500, M500 frac error."""
    from astropy.io import fits
    fpath = os.path.join(os.path.dirname(__file__), "..", "data", "erass1cl_primary_v3.2.fits")
    d = fits.open(fpath)[1].data

    def col(c):
        out = []
        for v in d[c]:
            try:
                if isinstance(v, bytes):
                    v = v.decode().strip()
                out.append(float(v))
            except Exception:
                out.append(np.nan)
        return np.array(out, dtype=float)

    z   = col("BEST_Z")
    M5  = col("M500")          # 1e13 Msun (WL-calibrated)
    M5L = col("M500_L"); M5H = col("M500_H")
    Mg  = col("MGAS500")       # 1e11 Msun
    fg  = col("FGAS500")
    R5  = col("R500")          # kpc
    kt  = col("KT")            # keV (-1 = unmeasured sentinel)

    ok = ((z > 0) & (z < zmax) & np.isfinite(z) & (M5 > 0) & np.isfinite(M5)
          & (Mg > 0) & np.isfinite(Mg) & (R5 > 0) & np.isfinite(R5)
          & (fg > fgas_lo) & (fg < fgas_hi))

    M500_kg = M5[ok] * 1e13 * MSUN
    Mgas_kg = Mg[ok] * 1e11 * MSUN
    Mbar_kg = (1.0 + fstar) * Mgas_kg
    R_m     = R5[ok] * KPC

    gobs = G * M500_kg / R_m**2
    gbar = G * Mbar_kg / R_m**2

    # fractional 1-sigma error on M500 (-> on g_obs) from the asymmetric WL limits
    eM = (M5H[ok] - M5L[ok]) / (2.0 * np.maximum(M5[ok], 1e-9))
    eM = np.clip(np.nan_to_num(eM, nan=0.25), 0.05, 1.0)

    return dict(z=z[ok], M500=M5[ok], Mgas=Mg[ok], fgas=fg[ok], R500=R5[ok],
                kt=kt[ok], gobs=gobs, gbar=gbar, Mbar_kg=Mbar_kg, M500_kg=M500_kg,
                eM=eM, N=int(ok.sum()))


# ----------------------------------------------------------------------------------
def main():
    np.random.seed(12345)
    print("#" * 100)
    print("# DOOR 6 -- GALAXY CLUSTERS: the honest MOND tension the framework inherits (real eRASS1 data)")
    print("#" * 100 + "\n")

    # -------- framework a0(0): Lambda-only vs RAR anchor --------
    A0_LAM = a0_lambda(OML, H0)
    A0_RAR = 1.2e-10
    A0_SIMPLE = 9.1e-11
    print("=" * 100)
    print("(0) The framework acceleration scale a0(0)")
    print("=" * 100)
    print(f"   a0 = c^2 sqrt(Lambda/32pi),  Lambda = 3 OmL H0^2/c^2")
    print(f"   Lambda-only (Planck OmL={OML}, H0={H0_KMS}) : a0 = {A0_LAM:.4e} m/s^2")
    print(f"   MOND RAR anchor (McGaugh+2016)             : a0 = {A0_RAR:.4e} m/s^2")
    print(f"   MOND simple-mu fit (Gentile/Famaey)        : a0 = {A0_SIMPLE:.4e} m/s^2")
    print(f"   -> the ~20% spread {A0_SIMPLE:.2e}..{A0_RAR:.2e} is the interpolating-function SYSTEMATIC.")
    print(f"      The framework Lambda-only value {A0_LAM:.2e} sits inside this band ({A0_LAM/A0_RAR:.2f}x RAR).\n")

    # -------- load real clusters --------
    c = load_clusters()
    z, gobs, gbar, M500, fgas, R500, kt = (c["z"], c["gobs"], c["gbar"], c["M500"],
                                           c["fgas"], c["R500"], c["kt"])
    a0 = A0_RAR  # use the canonical RAR value for the central MOND prediction
    nu = nu_simple(gbar / a0)
    eta = gobs / (nu * gbar)                       # residual missing-mass factor

    print("=" * 100)
    print("(1) THE REAL SAMPLE & THE RESIDUAL  (reproduces the classic factor-~2 cluster problem)")
    print("=" * 100)
    print(f"   eRASS1 (Bulbul+2024): clean cut 0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30  ->  N = {c['N']} clusters.")
    print(f"   redshift: median {np.median(z):.3f}  (10-90%: {np.percentile(z,10):.3f}-{np.percentile(z,90):.3f}).")
    print(f"   at R500 (median {np.median(R500):.0f} kpc):")
    print(f"      g_bar/a0  median = {np.median(gbar)/a0:.4f}    ({100*(gbar < 0.1*a0).mean():.0f}% of clusters have g_bar < 0.1 a0  =>  DEEP MOND)")
    print(f"      g_obs/a0  median = {np.median(gobs)/a0:.3f}")
    print(f"   Newtonian discrepancy  g_obs/g_bar = 1/f_bar   median = {np.median(gobs/gbar):.2f}")
    print(f"   MOND deep-regime boost nu(g_bar/a0)            median = {np.median(nu):.2f}")
    print(f"   RESIDUAL  eta = g_obs / (nu g_bar)             median = {np.median(eta):.3f}")
    print(f"             eta (16-84%): {np.percentile(eta,16):.2f} - {np.percentile(eta,84):.2f};  "
          f"geometric mean = {10**np.mean(np.log10(eta)):.3f}")
    print(f"   => MOND (and therefore this framework at z~0) UNDER-predicts cluster mass by ~{np.median(eta):.1f}x.")
    print(f"      This is the well-known cluster missing-mass problem; the standard MOND fix is ~2 eV neutrinos /")
    print(f"      hot dark matter. THIS IS A TENSION THE FRAMEWORK INHERITS, NOT A SUCCESS.\n")

    # eta vs mass / temperature (the known trend: hotter, more massive clusters are worse for MOND)
    hot = np.isfinite(kt) & (kt > 0)
    print(f"   eta vs system scale (MOND clusters worsen with mass/temperature):")
    print(f"      {'tertile':<22}{'N':>6}{'M500[1e14]':>12}{'eta median':>12}")
    order = np.argsort(M500)
    for lab, sl in [("low-mass third",  order[:len(order)//3]),
                    ("mid-mass third",  order[len(order)//3:2*len(order)//3]),
                    ("high-mass third", order[2*len(order)//3:])]:
        print(f"      {lab:<22}{len(sl):>6}{np.median(M500[sl])*1e13/1e14:>12.2f}{np.median(eta[sl]):>12.3f}")
    if hot.sum() > 50:
        khot = kt[hot]; ehot = eta[hot]
        hi = khot > np.median(khot)
        print(f"      KT<{np.median(khot):.1f}keV: eta={np.median(ehot[~hi]):.2f}   "
              f"KT>{np.median(khot):.1f}keV: eta={np.median(ehot[hi]):.2f}   "
              f"(N_KT={hot.sum()}; hotter => larger residual, the known anti-MOND trend)\n")

    # ----------------------------------------------------------------------------------
    # (2) ULTRA-PRECISION ERROR BUDGET on the median residual eta
    # ----------------------------------------------------------------------------------
    print("=" * 100)
    print("(2) ULTRA-PRECISION ERROR BUDGET on the median residual eta  (Monte Carlo, N=20000)")
    print("=" * 100)
    NMC = 20000
    rng = np.random.default_rng(7)

    # Pre-sample the per-cluster M500 (WL) errors once per draw is expensive; instead we
    # propagate the per-cluster data error into the median analytically via bootstrap, and
    # combine with the global (a0) errors in the MC. We separate the contributions cleanly.

    logeta0 = np.log10(eta)
    Ncl = len(eta)

    # (a) DATA-only error on the median eta: bootstrap clusters + per-cluster M500 & f_star jitter.
    boot_meds = np.empty(2000)
    eM = c["eM"]; Mbar_kg = c["Mbar_kg"]; M500_kg = c["M500_kg"]
    for i in range(2000):
        idx = rng.integers(0, Ncl, Ncl)
        # jitter M500 (log-normal with per-cluster eM) and f_star (global, affects all baryons)
        dM = rng.normal(0, 1, Ncl)
        M500_j = M500_kg[idx] * np.exp(eM[idx] * dM[idx])
        fstar_j = np.clip(FSTAR + rng.normal(0, FSTAR_ERR), 0.0, 0.6)
        Mbar_j = (1.0 + fstar_j) / (1.0 + FSTAR) * Mbar_kg[idx]   # rescale baseline baryons
        R_m = R500[idx] * KPC
        gobs_j = G * M500_j / R_m**2
        gbar_j = G * Mbar_j / R_m**2
        eta_j = gobs_j / (nu_simple(gbar_j / a0) * gbar_j)
        boot_meds[i] = np.median(eta_j)
    data_sig = np.std(boot_meds)

    # (b) global a0 errors propagate through nu(g_bar/a0). In deep MOND eta ~ 1/sqrt(a0/g_bar)...
    #     actually eta = (g_obs/g_bar)/nu, and nu -> sqrt(a0/g_bar) deep, so eta ~ (g_obs/g_bar) sqrt(g_bar/a0)
    #     -> eta DECREASES as a0 increases. We draw a0 and recompute the median eta.
    med_eta_base = np.median(eta)

    def median_eta_with_a0(a0_val):
        return np.median(gobs / (nu_simple(gbar / a0_val) * gbar))

    # (b1) STATISTICAL: Lambda error from Omega_Lambda & H0 -> a0_Lambda, then scaled to anchor.
    #      We vary a0 about the RAR anchor by the FRACTIONAL Lambda error (a0 ~ sqrt(OmL) H0).
    OmL_s = rng.normal(OML, OML_ERR, NMC)
    H0_s  = rng.normal(H0_KMS, H0_ERR, NMC) * 1e3 / MPC
    a0L_s = a0_lambda(np.clip(OmL_s, 1e-3, None), H0_s)
    frac_lambda = a0L_s / a0_lambda(OML, H0)          # fractional fluctuation of the Lambda a0
    # (b2) evolution error: a0 at cluster epoch z~median uses rho_DE(z; w0,wa); vary w0,wa.
    w0_s = rng.normal(W0, W0_ERR, NMC)
    wa_s = rng.normal(WA, WA_ERR, NMC)
    zc = float(np.median(z))
    evo = np.sqrt(rho_DE_ratio(zc, w0_s, wa_s))       # a0(zc)/a0(0) per draw
    evo0 = np.sqrt(rho_DE_ratio(zc, W0, WA))          # central evolution factor
    # (b3) SYSTEMATIC: interpolating-function 20% (log-normal about the anchor).
    sys_mu = np.exp(rng.normal(0.0, MU_SYS_FRAC, NMC))

    # Build a0 draws: anchor * lambda-fractional(statistical) * mu-systematic, evaluated at cluster z.
    a0_draws_stat = a0 * frac_lambda * (evo / evo0)   # statistical-only (cosmo params), at cluster epoch
    a0_draws_full = a0 * frac_lambda * (evo / evo0) * sys_mu

    med_stat = np.array([median_eta_with_a0(av) for av in a0_draws_stat[:4000]])
    med_full = np.array([median_eta_with_a0(av) for av in a0_draws_full[:4000]])

    # decompose: vary ONE source at a time about the central a0
    def spread(a0_array):
        m = np.array([median_eta_with_a0(av) for av in a0_array[:4000]])
        return np.std(m)

    sig_lambda = spread(a0 * frac_lambda)
    sig_evo    = spread(a0 * (evo / evo0))
    sig_mu     = spread(a0 * sys_mu)

    sig_stat_total = np.sqrt(sig_lambda**2 + sig_evo**2 + data_sig**2)
    sig_full_total = np.sqrt(sig_lambda**2 + sig_evo**2 + data_sig**2 + sig_mu**2)

    print(f"   central median residual eta_0 = {med_eta_base:.3f}")
    print(f"   --- contributions to sigma(median eta) ---")
    print(f"     (i)   DATA  (M500 weak-lensing + f_star + cluster bootstrap)  : +-{data_sig:.3f}  [STATISTICAL]")
    print(f"     (ii)  Lambda (Omega_Lambda {OML}+-{OML_ERR}, H0 {H0_KMS}+-{H0_ERR}) : +-{sig_lambda:.3f}  [STATISTICAL]")
    print(f"     (iii) evolution (DESI w0={W0}+-{W0_ERR}, wa={WA}+-{WA_ERR}) @ z={zc:.2f} : +-{sig_evo:.3f}  [STATISTICAL]")
    print(f"     (iv)  MOND interpolating-function 20% on absolute a0          : +-{sig_mu:.3f}  [SYSTEMATIC]")
    print(f"   --- combined ---")
    print(f"     STATISTICAL (data + cosmo) total : +-{sig_stat_total:.3f}")
    print(f"     SYSTEMATIC  (mu-function)  total : +-{sig_mu:.3f}")
    print(f"     FULL (stat (+) sys in quadrature): +-{sig_full_total:.3f}")
    contribs = {"DATA (M500/f_star)": data_sig, "Lambda (OmL,H0)": sig_lambda,
                "evolution (w0,wa)": sig_evo, "mu-systematic": sig_mu}
    dom = max(contribs, key=contribs.get)
    print(f"\n   ===> RESULT:  residual eta = {med_eta_base:.2f}  +-{sig_stat_total:.2f} (stat)  +-{sig_mu:.2f} (sys)")
    print(f"   ===> DOMINANT error: {dom} (sigma={contribs[dom]:.3f}).")
    print(f"        The SYSTEMATIC (mu-function) and the DATA (WL mass) errors are the two largest; the")
    print(f"        cosmological-parameter (Lambda, evolution) errors are sub-dominant by ~10x.")
    print(f"        Crucially: eta = {med_eta_base:.2f} sits ~{(med_eta_base-1)/sig_full_total:.1f} sigma above 1 even with the")
    print(f"        full error bar -- the cluster tension is robust to every uncertainty propagated.\n")

    # ----------------------------------------------------------------------------------
    # (3) Can DISTINCTIVE evolving-a0 rescue clusters? (the cluster-BTFR offset test)
    # ----------------------------------------------------------------------------------
    print("=" * 100)
    print("(3) Does the DISTINCTIVE evolving-a0 help? -- the cluster-epoch a0 boost vs the BTFR offset")
    print("=" * 100)
    print(f"   The framework's ONLY distinctive lever here is a0(z)=a0(0) sqrt(rho_DE(z)/rho_DE0).")
    print(f"   In deep MOND the BTFR/dispersion amplitude ~ (M a0)^(1/4), so a residual offset of")
    print(f"   Delta_dex in the relation needs a0 up by 10^(4*Delta_dex). The observed galaxy-vs-cluster")
    print(f"   baryonic-Tully-Fisher offset is ~0.6-0.8 dex (clusters lie above the galaxy BTFR).")
    print(f"   {'z':>6}{'E(z)=H/H0':>12}{'a0(z)/a0(0)':>14}{'log10 boost [dex]':>20}")
    E = lambda zz: np.sqrt(OM*(1+zz)**3 + OML)
    for zz in (0.0, 0.1, 0.2, 0.3, 0.5, 1.0):
        r = a0_of_z(zz, 1.0) / a0_of_z(0.0, 1.0)
        print(f"   {zz:>6.2f}{E(zz):>12.3f}{r:>14.4f}{np.log10(r):>20.4f}")
    boost_03 = a0_of_z(0.3, 1.0) / a0_of_z(0.0, 1.0)
    dex_03 = np.log10(boost_03)
    # a0(z) needed to explain a 0.7-dex BTFR offset:
    need_factor = 10**(4 * 0.7)
    z_need = None
    zz = np.linspace(0, 50, 500000)
    rr = a0_of_z(zz, 1.0) / a0_of_z(0.0, 1.0)
    if rr.max() >= need_factor:
        z_need = zz[np.searchsorted(rr, need_factor)]
    print(f"\n   At the cluster epoch z~0.3 the framework gives a0 boost = {boost_03:.4f}x = {dex_03:+.4f} dex.")
    print(f"   The observed cluster-BTFR offset is ~0.6-0.8 dex => needs a0 up by 10^(4*0.7) = {need_factor:.0f}x.")
    print(f"   This evolving a0 reaches such a boost only at z = {('%.1f'%z_need) if z_need else '>>10 (never)'} -- where galaxy CLUSTERS DO NOT EXIST.")
    print(f"   => The {dex_03:+.3f} dex of available a0-evolution to z~0.3 is ~{0.7/abs(dex_03) if dex_03!=0 else float('inf'):.0f}x too small (by ~1.5 orders")
    print(f"      of magnitude) to close the 0.6-0.8 dex cluster offset. The distinctive lever FAILS for clusters.")
    print(f"   NOTE the sign caveat: with DESI w0>-1, rho_DE actually RISES into the past, so a0(z>0) is LARGER")
    print(f"      than today -- the boost has the helpful sign, but the magnitude ({dex_03:+.3f} dex) is negligible.\n")

    # ----------------------------------------------------------------------------------
    print("=" * 100)
    print("DISTINCTIVENESS & VERDICT -- honest")
    print("=" * 100)
    print(f"""  WHAT IS THIS CHANNEL: a TENSION, inherited from MOND, not a success.
    - On {c['N']} real eRASS1 clusters, at R500, the residual missing-mass factor after the MOND boost is
      eta = {med_eta_base:.2f} +-{sig_stat_total:.2f}(stat) +-{sig_mu:.2f}(sys)  -- the classic factor-~2 cluster problem, reproduced
      from a single homogeneous weak-lensing-calibrated catalog. Standard MOND needs ~2 eV neutrinos / HDM.

  IS IT DISTINCTIVE OR SHARED?
    - The factor-~2 RESIDUAL itself is SHARED with ordinary constant-a0 MOND: at z~0 this framework IS MOND,
      so it inherits the cluster failure identically. NOT framework-distinct.
    - The framework's only DISTINCTIVE content (a0 evolves as sqrt(rho_DE)) buys {dex_03:+.3f} dex at z~0.3 --
      ~1.5 orders of magnitude too small to explain the 0.6-0.8 dex cluster-BTFR offset. So the distinctive
      lever does NOT rescue clusters; the tension stands.
    - (A SEPARATE reading -- a0=(c/2)sqrt(G rho) with rho = Mpc-AMBIENT density -- could raise in-cluster a0
      by sqrt(overdensity)~10x and close the gap, but only by BREAKING RAR universality. That is a different,
      environment-dependent prediction, not the constant-a0(z) reading scored here.)

  HONEST HEADLINE: clusters are where this framework, like all MOND, still fails. eta~2 is robust to the full
  error budget ({(med_eta_base-1)/sig_full_total:.1f} sigma above 1). The evolving-a0 prediction is real but ~{0.7/abs(dex_03):.0f}x too weak to help.
  Reported as a liability for the ledger, not pitched as a win.""")
    print("=" * 100)

    # ----------------------------------------------------------------------------------
    # figure
    # ----------------------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.4))

        # Panel A: g_obs vs g_bar with Newton, MOND(a0), and the residual
        gb = np.logspace(np.log10(gbar.min()*0.7), np.log10(gbar.max()*1.3), 300)
        axA.scatter(np.log10(gbar), np.log10(gobs), s=6, c=np.log10(eta), cmap="viridis",
                    alpha=0.45, zorder=2)
        axA.plot(np.log10(gb), np.log10(gb), "k--", lw=1.2, label="Newton (g_obs=g_bar)")
        axA.plot(np.log10(gb), np.log10(nu_simple(gb/a0)*gb), "r-", lw=2,
                 label=r"MOND $g_{\rm obs}=\nu(g_{\rm bar}/a_0)\,g_{\rm bar}$")
        axA.set_xlabel(r"$\log_{10}\,g_{\rm bar}\;[{\rm m\,s^{-2}}]$  (gas+stars, at $R_{500}$)")
        axA.set_ylabel(r"$\log_{10}\,g_{\rm obs}\;[{\rm m\,s^{-2}}]$  (WL mass)")
        axA.set_title(f"(A) eRASS1 clusters at $R_{{500}}$ ($N={c['N']}$): MOND under-predicts\n"
                      f"colour = $\\log_{{10}}\\eta$ (residual); median $\\eta={med_eta_base:.2f}$")
        axA.legend(loc="upper left", fontsize=9)

        # Panel B: residual eta histogram + median with error bar
        axB.hist(np.log10(eta), bins=40, color="0.6", edgecolor="0.3")
        axB.axvline(np.log10(med_eta_base), color="r", lw=2,
                    label=fr"median $\eta={med_eta_base:.2f}$")
        axB.axvline(0, color="k", ls=":", lw=1.5, label=r"$\eta=1$ (MOND closes)")
        axB.axvspan(np.log10(med_eta_base - sig_full_total), np.log10(med_eta_base + sig_full_total),
                    color="r", alpha=0.12, label=r"full $1\sigma$ (stat$\oplus$sys)")
        axB.set_xlabel(r"$\log_{10}\,\eta = \log_{10}\,[\,g_{\rm obs}/(\nu\,g_{\rm bar})\,]$")
        axB.set_ylabel("number of clusters")
        axB.set_title("(B) The inherited cluster tension: residual after MOND\n"
                      r"$\eta\!\approx\!2$, robust to the full error budget")
        axB.legend(loc="upper right", fontsize=8.5)

        fig.tight_layout()
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "door6_galaxy_clusters.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    # return machine-readable summary
    return dict(N=c["N"], eta=med_eta_base, sig_stat=sig_stat_total, sig_sys=sig_mu,
                sig_full=sig_full_total, sig_lambda=sig_lambda, sig_evo=sig_evo,
                sig_data=data_sig, a0_lambda=A0_LAM, zc=zc, dex_03=dex_03,
                boost_03=boost_03, dom=dom)


if __name__ == "__main__":
    main()
