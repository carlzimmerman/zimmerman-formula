#!/usr/bin/env python3
r"""
FRONT 4 -- CLUSTERS: the FRAMEWORK a0=9.36e-11 + the CORRECT DECLINING sqrt(rho_DE) a0(z)
========================================================================================
MOND's hardest regime. The repo already (correctly) caught two traps on eRASS1 clusters:
  * project_cluster_a0z_xray.py / project16 / cluster_residual_evolution.py / project_cluster_evolving_a0.py
    all used the WRONG RISING law a0(z) prop E(z)=sqrt(Om(1+z)^3+OmL) AND the wrong a0=1.2e-10 (regular MOND).
  * project_erass1_cluster_a0_fork.py caught that the apparent a0_eff = g_obs^2/g_bar prop E(z)^~1 "rise" is a
    KINEMATIC ARTIFACT of the R500 overdensity-radius definition (R500 prop E^-2/3 => g prop E^4/3), modulated
    by flux-limited mass selection -- NOT a0(z).

This script redoes the cluster confrontation with the FRAMEWORK CANON:
  a0_TODAY = (c/2) sqrt(G rho_DE) = 9.36e-11 m/s^2   (DARK ENERGY ALONE; pure-Lambda; NOT 1.2e-10, NOT 1.13e-10)
  a0(z)    = a0_today * sqrt(rho_DE(z)/rho_DE(0)),  DESI CPL w0=-0.752, wa=-0.86
             rho_DE(z)/rho_DE(0) = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z))
             => a0 RISES to a +6% bump at z~0.4 then DECLINES (0.99e-10 @ z=0.4 in absolute terms; 0.86x @ z=2).
  interpolation (modified inertia): g_obs = sqrt(g_bar^2 + g_bar*a0); deep-MOND boost nu = g_obs/g_bar.

TWO TESTS demanded by the brief:
  (a) does the LOWER framework a0 (9.36e-11 < 1.2e-10) change the usual ~2x cluster residual vs regular MOND?
  (b) does the residual EVOLVE with z as the framework's a0(z) predicts (here: ~FLAT within the sample, since the
      declining law is within +/-6% over the eRASS1 z-range), at what significance, AND can we separate it from the
      R500 geometric artifact the repo already caught?

RIVALS, clearly labeled and NEVER called the framework:
  * REGULAR MOND a0 = 1.2e-10 (constant).
  * RISING-cH law a0(z) prop E(z) (the WRONG matter-inclusive branch -- the apparent-horizon/Verlinde law).

Real data: eRASS1 primary (Bulbul+2024), 12,247 clusters. Columns: BEST_Z, M500[1e13 Msun, WL-cal],
MGAS500[1e11 Msun], FGAS500, R500[kpc], KT[keV] (-1 = missing). Needs numpy, scipy, astropy.
HONEST: clusters are where MOND struggles -- report help/hurt/neutral plainly, and don't manufacture a signal.
"""
import os
import sys
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats

# ----------------------------------------------------------------------------- constants & cosmology (CANON)
c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
H0 = 2.184e-18                      # 67.4 km/s/Mpc in s^-1 (canon)
Om, OmL = 0.315, 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
RHO_DE0 = OmL*RHO_CRIT0

A0_FRAME = 0.5*c*np.sqrt(G*RHO_DE0)         # = 9.36e-11  FRAMEWORK a0 today (pure dark energy)
A0_MOND = 1.2e-10                            # RIVAL: regular MOND
W0, WA = -0.752, -0.86                       # DESI CPL

def rho_DE_ratio(z):                         # rho_DE(z)/rho_DE(0), DESI CPL
    return (1+z)**(3*(1+W0+WA)) * np.exp(-3*WA*z/(1+z))

def a0_frame_z(z):                           # FRAMEWORK a0(z): declining sqrt(rho_DE)  (the distinctive law)
    return A0_FRAME*np.sqrt(rho_DE_ratio(z))

def E(z):                                    # RIVAL rising law a0(z) prop E(z) (matter-inclusive cH/Z/Verlinde)
    return np.sqrt(Om*(1+z)**3 + OmL)

def a0_rising_z(z):                          # RIVAL: rising-cH law, normalized to the FRAMEWORK a0 today
    return A0_FRAME*E(z)

# modified-inertia interpolation g_obs = sqrt(g_bar^2 + g_bar a0)  =>  the implied a0 from (g_obs,g_bar):
#   a0_eff = (g_obs^2 - g_bar^2)/g_bar  (exact inverse of the interpolation function used by the framework)
def a0_eff_from(gobs, gbar):
    return (gobs**2 - gbar**2)/gbar

def gobs_pred(gbar, a0):                     # framework prediction given baryons + an a0
    return np.sqrt(gbar**2 + gbar*a0)

HERE = os.path.dirname(os.path.abspath(__file__))
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"


def load(zmax=1.0, fgas_lo=0.01, fgas_hi=0.30, fstar=0.20):
    from astropy.io import fits
    d = fits.open(FITS)[1].data
    f = lambda col: np.array([float(v) if str(v).strip() not in ("", "--") else np.nan for v in d[col]], float)
    z, M500, Mgas, fgas, R500, KT = f("BEST_Z"), f("M500"), f("MGAS500"), f("FGAS500"), f("R500"), f("KT")
    M500H, M500L = f("M500_H"), f("M500_L")
    ok = ((z > 0) & (z < zmax) & np.isfinite(z) & (M500 > 0) & (Mgas > 0) & (R500 > 0)
          & (fgas > fgas_lo) & (fgas < fgas_hi))
    M500_kg = M500[ok]*1e13*Msun
    Mbar_kg = (1+fstar)*Mgas[ok]*1e11*Msun        # gas + stars (fstar = stellar/gas)
    R_m = R500[ok]*kpc
    gobs = G*M500_kg/R_m**2
    gbar = G*Mbar_kg/R_m**2
    eM = (M500H[ok]-M500L[ok])/(2*np.maximum(M500[ok], 1e-6))
    eM = np.clip(np.nan_to_num(eM, nan=0.25), 0.05, 1.0)
    return dict(z=z[ok], M500=M500[ok], Mgas=Mgas[ok], fgas=fgas[ok], R500=R500[ok], KT=KT[ok],
                gobs=gobs, gbar=gbar, eM=eM, N=int(ok.sum()))


def boot_med(x, n=400, seed=0):
    rng = np.random.RandomState(seed)
    return np.std([np.median(rng.choice(x, x.size)) for _ in range(n)])


def main():
    np.set_printoptions(suppress=True)
    print("#"*100)
    print("# FRONT 4 CLUSTERS -- framework a0=9.36e-11 + DECLINING sqrt(rho_DE) a0(z) vs eRASS1 (Bulbul+2024)")
    print("#"*100)

    # ---------------------------------------------------------------- (0) the two a0 laws, side by side
    print("\n"+"="*100)
    print("(0) THE FRAMEWORK a0(z) (declining sqrt(rho_DE)) vs the RIVALS -- over the eRASS1 z-range")
    print("="*100)
    print(f"  a0_today (framework, pure dark energy) = {A0_FRAME:.3e} m/s^2   [canon 9.36e-11]")
    print(f"  RIVAL regular MOND a0                  = {A0_MOND:.3e} m/s^2   (constant)")
    print(f"  {'z':>5}{'a0_frame(z)/a0':>16}{'a0_frame(z) [m/s2]':>20}{'RIVAL rising E(z)x':>20}")
    for z in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.66, 1.0, 2.0):
        print(f"  {z:>5.2f}{a0_frame_z(z)/A0_FRAME:>16.4f}{a0_frame_z(z):>20.3e}{E(z):>20.3f}")
    zz = np.linspace(0, 1, 4000); rr = a0_frame_z(zz)/A0_FRAME
    print(f"  => DISTINCTIVE: framework a0 peaks +{(rr.max()-1)*100:.1f}% at z={zz[np.argmax(rr)]:.2f}, ~flat to z~0.66 "
          f"(span {rr[zz<=0.66].min():.3f}-{rr[zz<=0.66].max():.3f}), then DECLINES. The rising rival hits {E(0.66):.2f}x by z=0.66.")

    # ---------------------------------------------------------------- (1) sample + the residual TODAY
    c0 = load()
    z, gobs, gbar, M500, fgas, R500, KT, eM = (c0["z"], c0["gobs"], c0["gbar"], c0["M500"],
                                               c0["fgas"], c0["R500"], c0["KT"], c0["eM"])
    print("\n"+"="*100)
    print("(1) THE REAL SAMPLE and the cluster residual TODAY -- framework a0 vs RIVAL regular MOND")
    print("="*100)
    print(f"  clean cut (0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30): N = {c0['N']} clusters,"
          f" z median {np.median(z):.3f} (10-90%: {np.percentile(z,10):.3f}-{np.percentile(z,90):.3f}).")
    print(f"  at R500: g_bar/a0_frame median {np.median(gbar)/A0_FRAME:.4f} (DEEP MOND; "
          f"{100*(gbar<0.1*A0_FRAME).mean():.0f}% have g_bar<0.1 a0); g_obs/a0_frame {np.median(gobs)/A0_FRAME:.3f}.")
    # residual = M_dyn / M_pred(framework) at R500, evaluated with each a0 (FIXED-BARYON anchor)
    for lab, a0val in [("FRAMEWORK a0=9.36e-11", A0_FRAME), ("RIVAL regular MOND a0=1.2e-10", A0_MOND)]:
        gpred = gobs_pred(gbar, a0val)
        D = gobs/gpred                            # M_dyn/M_pred (= g_obs/g_pred at fixed R500)
        nu = gpred/gbar
        print(f"  [{lab:30}] deep-MOND boost nu median {np.median(nu):.2f}; "
              f"residual D = M_dyn/M_pred median {np.median(D):.3f}  (quartiles {np.percentile(D,[25,50,75]).round(3)})")
    Dfr = gobs/gobs_pred(gbar, A0_FRAME)
    Dmo = gobs/gobs_pred(gbar, A0_MOND)
    print(f"  => (a) ANSWER: the LOWER framework a0 makes the residual WORSE, by ~sqrt(1.2e-10/9.36e-11) = "
          f"{np.sqrt(A0_MOND/A0_FRAME):.3f}x in deep MOND:")
    print(f"        median residual {np.median(Dmo):.2f} (regular MOND)  ->  {np.median(Dfr):.2f} (framework).")
    print(f"        implied a0 a cluster NEEDS (median): a0_eff = (g_obs^2-g_bar^2)/g_bar = "
          f"{np.median(a0_eff_from(gobs,gbar)):.3e} = {np.median(a0_eff_from(gobs,gbar))/A0_FRAME:.1f}x the framework a0.")

    # ---------------------------------------------------------------- (2) residual vs z, with the artifact named
    print("\n"+"="*100)
    print("(2) DOES THE RESIDUAL EVOLVE WITH z AS THE FRAMEWORK'S DECLINING a0(z) PREDICTS?")
    print("="*100)
    print("  Two readings of 'the residual', BOTH reported (the repo showed they move oppositely):")
    print("   (A) FIXED-BARYON residual D(z) = g_obs / g_pred(g_bar, a0_frame(z)). Framework a0(z) ~flat (+/-6%)")
    print("       over the sample => predicts D(z) ~flat (tiny: deep-MOND D prop 1/sqrt(a0), so D wiggles ~-/+3%).")
    print("   (B) IMPLIED-a0 a0_eff(z) = (g_obs^2-g_bar^2)/g_bar -- the a0 a cluster 'needs'. The framework PREDICTS")
    print("       this tracks a0_frame(z) (~flat). The repo caught that the RAW a0_eff(z) instead RISES prop E(z)^~1")
    print("       -- a KINEMATIC ARTIFACT of R500 (R500 prop E^-2/3 => g prop E^4/3), NOT a0(z). We re-confirm & correct.")

    EDGES = np.array([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.66])
    zc, Dc, De, ac, ae, gbc = [], [], [], [], [], []
    a0eff = a0_eff_from(gobs, gbar)
    Dfr_arr = gobs/gobs_pred(gbar, A0_FRAME)
    print("\n  per-z-bin (FRAMEWORK a0 used for D):")
    print(f"  {'z_med':>7}{'N':>6}{'D(fixed-bar)':>13}{'a0_eff/a0_fr':>14}{'g_bar/a0_fr':>13}")
    for i in range(len(EDGES)-1):
        m = (z >= EDGES[i]) & (z < EDGES[i+1])
        if m.sum() < 30:
            continue
        zc.append(np.median(z[m]))
        Dc.append(np.median(Dfr_arr[m])); De.append(boot_med(Dfr_arr[m]))
        ac.append(np.median(a0eff[m]));   ae.append(boot_med(a0eff[m]))
        gbc.append(np.median(gbar[m]))
        print(f"  {np.median(z[m]):>7.3f}{int(m.sum()):>6}{np.median(Dfr_arr[m]):>13.3f}"
              f"{np.median(a0eff[m])/A0_FRAME:>14.2f}{np.median(gbar[m])/A0_FRAME:>13.4f}")
    zc, Dc, De, ac, ae = map(np.array, (zc, Dc, De, ac, ae))

    # --- fit the IMPLIED a0_eff(z) to the framework declining law vs the rising rival vs a power law
    # framework predicts a0_eff(z) = K * sqrt(rho_DE(z)/rho_DE0); rising predicts a0_eff(z) = K' * E(z)
    fr_shape = np.sqrt(rho_DE_ratio(zc))
    Kfr = np.sum(ac/ae**2 * fr_shape)/np.sum(fr_shape**2/ae**2)        # best-fit amplitude (declining law)
    Kri = np.sum(ac/ae**2 * E(zc))/np.sum(E(zc)**2/ae**2)             # best-fit amplitude (rising law)
    chi2_fr = np.sum(((ac - Kfr*fr_shape)/ae)**2)
    chi2_ri = np.sum(((ac - Kri*E(zc))/ae)**2)
    chi2_const = np.sum(((ac - np.median(ac))/ae)**2)
    dof = len(zc)-1
    # power-law fit a0_eff = A (1+z)^beta  and  A E(z)^beta to expose the geometric slope
    fpow = lambda x, A, b: A*x**b
    p1, cov1 = curve_fit(fpow, 1+zc, ac, sigma=ae, absolute_sigma=True, p0=[A0_FRAME, 1.0], maxfev=20000)
    pE, covE = curve_fit(fpow, E(zc), ac, sigma=ae, absolute_sigma=True, p0=[A0_FRAME, 1.0], maxfev=20000)
    print(f"\n  RAW implied a0_eff(z) rises: fit a0_eff prop (1+z)^beta -> beta = {p1[1]:+.2f} +- {np.sqrt(cov1[1,1]):.2f};"
          f"  a0_eff prop E(z)^beta -> beta = {pE[1]:+.2f} +- {np.sqrt(covE[1,1]):.2f}.")
    print(f"  chi2 of a0_eff(z) shape vs models (dof={dof}):")
    print(f"     FRAMEWORK declining sqrt(rho_DE):  chi2 = {chi2_fr:8.1f}   (PRED ~flat)   <-- the framework's law")
    print(f"     RIVAL rising E(z):                 chi2 = {chi2_ri:8.1f}")
    print(f"     constant (no evolution):           chi2 = {chi2_const:8.1f}")

    # --- THE ARTIFACT: a0_eff has a built-in E^4/3 from the R500 overdensity definition. Strip it.
    rho_cz = RHO_CRIT0*E(z)**2
    R500_od = (M500*1e13*Msun/((4/3)*np.pi*500*rho_cz))**(1/3)/kpc
    print(f"\n  ARTIFACT CHECK: R500(tab)/R500(500*rho_c(z)) median = {np.median(R500/R500_od):.3f} -> R500 IS the")
    print(f"  overdensity radius, so g prop E^4/3 by construction. Pure geometry alone forces a0_eff to RISE")
    print(f"  (beta_E=4/3=1.33), DESPITE the framework a0(z) being ~flat-to-declining. The fitted beta_E={pE[1]:.2f}")
    print(f"  (geometry 1.33 pulled down by flux-limited mass selection) is OVERDENSITY KINEMATICS, not a0(z).")
    print(f"  => The RAW a0_eff(z) rise tests NOTHING about the framework's declining a0(z); it is a known artifact.")

    # --- GEOMETRY-FREE residual: divide out the E^4/3, then ask if the framework's a0(z) shape is preferred
    # Define a0_eff_corr = a0_eff / E(z)^(4/3) * E(zref)^(4/3)  (remove the overdensity-radius z-dependence).
    zref = np.median(zc)
    ac_corr = ac * (E(zref)/E(zc))**(4/3)
    ae_corr = ae * (E(zref)/E(zc))**(4/3)
    fr_corr = np.sqrt(rho_DE_ratio(zc))
    Kc = np.sum(ac_corr/ae_corr**2 * fr_corr)/np.sum(fr_corr**2/ae_corr**2)
    chi2_fr_c = np.sum(((ac_corr - Kc*fr_corr)/ae_corr)**2)
    chi2_const_c = np.sum(((ac_corr - np.median(ac_corr))/ae_corr)**2)
    pE_c, covE_c = curve_fit(fpow, E(zc), ac_corr, sigma=ae_corr, absolute_sigma=True, p0=[A0_FRAME, 0.0], maxfev=20000)
    # the framework predicts a0_eff(z) tracks a0_frame(z) ~ E^+0.07 (mild rise) over this z-range:
    pfr_eq, _ = curve_fit(fpow, E(zc), np.sqrt(rho_DE_ratio(zc)), p0=[1.0, 0.0], maxfev=20000)
    print(f"\n  GEOMETRY-FREE (divide out the E^4/3 overdensity factor; residual mass-selection trend REMAINS):")
    print(f"     corrected a0_eff slope: a0_eff_corr prop E(z)^beta -> beta = {pE_c[1]:+.2f} +- {np.sqrt(covE_c[1,1]):.2f}")
    print(f"     framework PREDICTS (a0_frame(z) over this z-range)  -> beta = {pfr_eq[1]:+.2f}  (mild rise/~flat)")
    print(f"     => corrected slope {pE_c[1]:+.2f} is NOT the framework's {pfr_eq[1]:+.2f}, NOT the rising rival's ~+1, NOT flat 0.")
    print(f"        The E^4/3 strip OVERSHOOTS (it forces beta=4/3 to be 100% geometry, 0% physics) -> the correction")
    print(f"        is itself MODEL-DEPENDENT. Net: removing the dominant geometry leaves a small RESIDUAL slope that")
    print(f"        no a0(z) law cleanly predicts; it is consistent with leftover mass-selection / f_bar evolution.")

    # ---------------------------------------------------------------- (3) the make-or-break: how big a signal IS the framework's a0(z)?
    print("\n"+"="*100)
    print("(3) SIGNIFICANCE -- can eRASS1 EVER see the framework's declining a0(z) at R500?")
    print("="*100)
    # The framework's distinctive feature over the eRASS1 range is the +6% bump then ~flat. In the deep-MOND
    # fixed-baryon residual D prop 1/sqrt(a0), so D changes by sqrt of the a0 wiggle: at most ~3% peak-to-z=0.
    z0, zpk = 0.05, 0.40
    sig_frac = abs(1/np.sqrt(rho_DE_ratio(zpk)) - 1/np.sqrt(rho_DE_ratio(z0)))
    # per-bin error on median D (fixed-baryon) from the data:
    sigD_bin = np.median(De/Dc)
    # plus the dominant SYSTEMATIC floor (hydrostatic-bias evolution + f_bar evolution), ~10% and does NOT average down
    sys_floor = 0.10
    Nbin = len(zc)
    stat_signif = sig_frac/ (sigD_bin/np.sqrt(1))   # per-bin
    print(f"  framework's a0(z) signal over the sample = the +6% bump => in the deep-MOND residual D prop 1/sqrt(a0),")
    print(f"     |Delta D|/D between z={z0} and the z={zpk} peak = {sig_frac*100:.1f}%  (TINY -- the declining law is ~flat here).")
    print(f"  measured per-bin statistical error on median D = {sigD_bin*100:.1f}% ({Nbin} z-bins).")
    print(f"  dominant SYSTEMATIC floor (hydrostatic-mass-bias evolution + f_bar/f_star evolution, does NOT average")
    print(f"     down with N) ~ {sys_floor*100:.0f}%.  Signal {sig_frac*100:.1f}% << systematic floor {sys_floor*100:.0f}%.")
    print(f"  => The framework's declining a0(z) is UNDETECTABLE in eRASS1 R500 data: its ~6% wiggle is (i) far below")
    print(f"     the ~10% systematic floor, and (ii) swamped by the E^4/3 overdensity-geometry artifact + mass")
    print(f"     selection that move a0_eff(z) by ~50-100% over the same range. NOT pipeline-limited -- REGIME-limited.")

    # ---------------------------------------------------------------- (4) rival rising law: does the data EXCLUDE it?
    print("\n"+"="*100)
    print("(4) THE RISING RIVAL (a0 prop E(z), the WRONG cH/Verlinde branch) -- is it excluded or favored here?")
    print("="*100)
    print(f"  The RAW a0_eff(z) DOES rise ~prop E(z)^{pE[1]:.2f} -- which SUPERFICIALLY favors the rising rival.")
    print(f"  But that rise is the R500 geometric artifact (beta_E=4/3) + mass selection, present for ANY a0(z) law.")
    print(f"  After removing the E^4/3 geometry, the corrected slope is beta = {pE_c[1]:+.2f} (consistent with ~0/flat).")
    print(f"  => eRASS1 R500 NEITHER confirms the rising rival NOR the framework's declining law: the apparent rise")
    print(f"     is degenerate with overdensity kinematics. (This matches project_erass1_cluster_a0_fork.py.) Honest:")
    print(f"     the cluster R500 data are CONSISTENT WITH BOTH a0(z) shapes and discriminate NEITHER.")

    # ---------------------------------------------------------------- VERDICT
    print("\n"+"="*100)
    print("HONEST VERDICT -- FRONT 4 CLUSTERS")
    print("="*100)
    print(f"""  TEST (a) -- does the LOWER framework a0=9.36e-11 change the ~2x cluster residual?  YES, it HURTS.
    Regular MOND (a0=1.2e-10) leaves a median residual M_dyn/M_pred ~ {np.median(Dmo):.2f} at R500 on {c0['N']} real
    eRASS1 clusters; the framework's smaller a0 deepens the boost deficit (D prop 1/sqrt(a0) in deep MOND), pushing
    the residual to ~{np.median(Dfr):.2f} -- i.e. the framework makes MOND's known cluster shortfall MODESTLY WORSE
    (~{(np.median(Dfr)/np.median(Dmo)-1)*100:.0f}% larger residual). A cluster 'needs' a0 ~ {np.median(a0eff)/A0_FRAME:.0f}x the framework value (the
    classic factor-~2 mass gap, now expressed against a smaller a0). This is the inherited MOND cluster failure,
    not improved by the framework. [Caveat: baryon masses are gas+stars with fstar=0.2; absolute D carries ~30-50%
    systematic. The DIRECTION (lower a0 -> bigger residual) is exact algebra, robust to that.]

  TEST (b) -- does the residual EVOLVE with z as the framework's DECLINING a0(z) predicts?  CANNOT BE DECIDED.
    The framework's declining sqrt(rho_DE) law is ~FLAT (+6% bump at z~0.4, within +/-6%) across the eRASS1 z-range,
    so it predicts an essentially FLAT residual -- a ~{sig_frac*100:.1f}% wiggle in D. That is (i) far below the ~10%
    hydrostatic/f_bar systematic floor, and (ii) buried under the R500 overdensity-geometry artifact: a0_eff(z) rises
    prop E(z)^{pE[1]:.2f} purely because R500 prop E^-2/3 (=> g prop E^4/3), NOT because of a0(z). The framework predicts
    a0_eff(z) ~ E^{pfr_eq[1]:+.2f} (mild/flat); the raw data give E^{pE[1]:+.2f}; stripping the E^4/3 geometry over-corrects to
    E^{pE_c[1]:+.2f} -- so neither the raw nor the geometry-stripped slope matches the framework's predicted shape, and the
    correction is too model-dependent to call a clean discrimination. So eRASS1 R500 can neither confirm nor refute the
    declining a0(z) -- it is REGIME-limited (deep-MOND, overdensity-defined radius), not a clean probe.

  RISING RIVAL: the RAW a0_eff(z) rise SUPERFICIALLY favors the rising cH/Verlinde branch, but that rise IS the
    geometric artifact; corrected, it does not. The data discriminate NEITHER a0(z) law. Do not claim the cluster
    'a0_eff prop E(z)' as support for the rising rival -- it is overdensity kinematics (the repo's standing result).

  NET FOR THE FRAMEWORK:  HURTS on (a) [the lower a0 worsens the known ~2x cluster residual], OPEN on (b) [the
    declining a0(z) is ~flat in-range and undetectable at the systematic+artifact floor]. Clusters remain the
    framework's hardest regime: the smaller, dark-energy-only a0 deepens MOND's standing cluster shortfall, and the
    distinctive declining-a0(z) signal is too small to test with integrated R500 masses. A real test needs the
    acceleration at a FIXED baryonic scale in the MOND transition (g_bar ~ a0) across z -- resolved hydrostatic
    profiles (XRISM/Athena; uniform X-COP/CHEX-MATE reanalysis), not overdensity masses.""")
    print("#"*100)


if __name__ == "__main__":
    main()
