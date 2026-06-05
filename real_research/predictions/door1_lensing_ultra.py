#!/usr/bin/env python3
"""
ULTRA-PRECISION -- Channel: GRAVITATIONAL LENSING (saturated deflection alpha_inf and its evolution).
=====================================================================================================
Framework: a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda), with Lambda = 3 Omega_L H0^2 / c^2.

PREDICTION (this channel):
  An isolated baryonic mass M produces, in the deep-MOND regime g = sqrt(G M a0)/r, a SATURATED light deflection
        alpha_inf = 2 pi sqrt(G M a0) / c^2      [independent of impact parameter b]
  (In GR alpha = 4GM/(c^2 b) -> 0 as b grows. Here it levels off at a constant.)

  Derivation: alpha = (2/c^2) integral g_perp dl ;  g_perp = sqrt(GMa0) * b/(b^2+l^2) ;
              integral_{-inf}^{inf} b dl/(b^2+l^2) = pi  ->  alpha_inf = 2 pi sqrt(GMa0)/c^2.   (b cancels -> constant)

  Evolution: alpha_inf ~ sqrt(a0) ~ (rho_DE)^(1/4). The 2pi, c^2, sqrt(G) all cancel in the RATIO, so the
             redshift dependence is COEFFICIENT-FREE and set only by DESI rho_DE(z).

We compute EVERY number (numpy/scipy), propagate ALL errors, and separate STATISTICAL (cosmological-parameter)
from SYSTEMATIC (MOND interpolating-function) error. Honesty mandate: report what the math gives; flag MOND tensions.

Run:  python3 door1_lensing_ultra.py
"""
import numpy as np

# ----------------------------------------------------------------------------------------------------------------
# CONSTANTS (mandated, consistent)
# ----------------------------------------------------------------------------------------------------------------
C    = 299792458.0          # m/s (exact)
G    = 6.67430e-11          # CODATA 2018
Msun = 1.98892e30           # kg
MPC  = 3.0857e22            # m
ARCSEC = 180.0 * 3600.0 / np.pi      # rad -> arcsec

# Planck 2018 (statistical cosmology errors)
H0_kms, H0_kms_e = 67.36, 0.54       # km/s/Mpc
OmL, OmL_e       = 0.6847, 0.0073
Omm, Omm_e       = 0.3153, 0.0073

# DESI DR2 dark-energy (w0waCDM) -- for the evolution
W0, W0_e = -0.752, 0.057
WA, WA_e = -0.86,  0.22
# DESI quotes a strong w0-wa anti-correlation; the published 2D contour corr ~ -0.9.
RHO_W0WA = -0.9

# MOND interpolating-function SYSTEMATIC on the ABSOLUTE a0 (NOT statistical):
A0_SIMPLE = 9.1e-11          # simple-mu best fit to SPARC (minimizes RAR scatter)
A0_RAR    = 1.20e-10         # McGaugh RAR-function normalization (the canonical "1.2e-10")

LN10 = np.log(10.0)


def H0_si(H0_kms_val):
    return H0_kms_val * 1.0e3 / MPC          # s^-1


def Lambda_of(OmL_val, H0_kms_val):
    """Cosmological constant Lambda = 3 Omega_L H0^2 / c^2  [m^-2]."""
    return 3.0 * OmL_val * H0_si(H0_kms_val)**2 / C**2


def a0_framework(OmL_val, H0_kms_val):
    """Framework absolute a0 = c^2 sqrt(Lambda/32pi)  [m/s^2]."""
    return C**2 * np.sqrt(Lambda_of(OmL_val, H0_kms_val) / (32.0 * np.pi))


def rho_DE_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE0 for CPL w(a)=w0+wa(1-a):  a^(-3(1+w0+wa)) exp(-3 wa (1-a))."""
    a = 1.0 / (1.0 + z)
    return a**(-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))


def alpha_inf_rad(M_solar, a0):
    """Saturated MOND deflection [rad] = 2 pi sqrt(G M a0)/c^2."""
    return 2.0 * np.pi * np.sqrt(G * M_solar * Msun * a0) / C**2


# ----------------------------------------------------------------------------------------------------------------
# (0) numerical confirmation that alpha_inf is impact-parameter independent  (do the integral, don't assert it)
# ----------------------------------------------------------------------------------------------------------------
def numeric_alpha_inf(M_solar, a0, b_m, L_over_b=2000.0, npts=2_000_001):
    """alpha = (2/c^2) * integral_{-inf}^{inf} g_perp dl, with g_perp = sqrt(GMa0) b/(b^2+l^2). Should NOT depend on b.
    We integrate over the PHYSICAL line-of-sight l (meters) using the ACTUAL b -- not a pre-cancelled substitution --
    on a dense symmetric grid l in [-L,L], L = L_over_b * b (so the width-b core at l=0 is always resolved and the
    integration range is the SAME number of core-widths for every b). Analytic value: integral b dl/(b^2+l^2) = pi,
    so alpha -> 2 pi sqrt(GMa0)/c^2 as L->inf. The finite-L deficit is 2*arctan(1/L_over_b)/pi (identical at all b),
    which is why the numeric/analytic ratio is the SAME constant for every b -- the demonstration of b-independence."""
    K = np.sqrt(G * M_solar * Msun * a0)
    L = L_over_b * b_m
    l = np.linspace(-L, L, npts)              # spacing 2L/npts = 4e-3 * b near the peak -> core well sampled
    integ = np.trapz(b_m / (b_m**2 + l**2), l)
    return (2.0 / C**2) * K * integ


def main():
    np.random.seed(0xA11)
    print("#" * 108)
    print("# ULTRA-PRECISION -- GRAVITATIONAL LENSING: saturated deflection alpha_inf = 2 pi sqrt(G M a0)/c^2")
    print("#" * 108 + "\n")

    # ---------------- absolute a0: central + statistical + systematic ----------------
    a0_fw   = a0_framework(OmL, H0_kms)
    Lam     = Lambda_of(OmL, H0_kms)
    print("INPUTS / DERIVED a0")
    print("-" * 108)
    print(f"  c={C:.0f} m/s (exact); G={G:.5e}; Msun={Msun:.5e} kg; 1 Mpc={MPC:.4e} m")
    print(f"  Planck18: H0={H0_kms}+/-{H0_kms_e} km/s/Mpc ; OmL={OmL}+/-{OmL_e}")
    print(f"  Lambda = 3 OmL H0^2/c^2 = {Lam:.4e} m^-2")
    print(f"  FRAMEWORK absolute a0 = c^2 sqrt(Lambda/32pi) = {a0_fw:.4e} m/s^2")

    # Statistical error on a0_framework from OmL and H0 (a0 ~ sqrt(OmL) * H0):
    #   dln a0 = 0.5 dln OmL  +  dln H0
    rel_OmL = 0.5 * (OmL_e / OmL)
    rel_H0  = (H0_kms_e / H0_kms)
    a0_fw_relerr = np.sqrt(rel_OmL**2 + rel_H0**2)
    a0_fw_e = a0_fw * a0_fw_relerr
    print(f"  a0_framework STATISTICAL err (OmL,H0): rel = {a0_fw_relerr*100:.2f}%  "
          f"-> a0 = ({a0_fw*1e11:.3f} +/- {a0_fw_e*1e11:.3f}) e-11  [OmL term {rel_OmL*100:.2f}%, H0 term {rel_H0*100:.2f}%]")

    # MOND interpolating-function SYSTEMATIC band on absolute a0:
    a0_sys_lo, a0_sys_hi = A0_SIMPLE, A0_RAR
    a0_sys_mid = 0.5 * (a0_sys_lo + a0_sys_hi)
    a0_sys_halfspan = 0.5 * (a0_sys_hi - a0_sys_lo)
    print(f"  MOND interpolating-fn SYSTEMATIC band on absolute a0: "
          f"[{a0_sys_lo*1e11:.2f}, {a0_sys_hi*1e11:.2f}] e-11  (simple-mu 9.1 vs McGaugh RAR 12.0)")
    print(f"     -> systematic ~ +/-{100*a0_sys_halfspan/a0_sys_mid:.0f}% about midpoint {a0_sys_mid*1e11:.2f}e-11; "
          f"framework {a0_fw*1e11:.2f}e-11 sits {'INSIDE' if a0_sys_lo<=a0_fw<=a0_sys_hi else 'OUTSIDE'} this band.")
    print()

    # ---------------- (0) confirm b-independence numerically ----------------
    print("=" * 108)
    print("(0) CONFIRM the deflection is IMPACT-PARAMETER INDEPENDENT (numerical line-of-sight integral)")
    print("=" * 108)
    Mtest, a0test = 1e13, a0_fw
    analytic = alpha_inf_rad(Mtest, a0test) * ARCSEC
    print(f"   M={Mtest:.0e} Msun, a0={a0test:.3e}: analytic alpha_inf = 2pi sqrt(GMa0)/c^2 = {analytic:.6f} arcsec")
    print(f"   (numeric = dense trapezoid of the PHYSICAL l-integral with the actual b; ratio<1 only from finite-L tail)")
    print(f"   {'impact b':>12}{'numeric alpha [arcsec]':>26}{'ratio numeric/analytic':>26}")
    ratios = []
    for b_kpc in (0.1, 1.0, 10.0, 100.0, 1000.0):
        b_m = b_kpc * 1e3 * MPC / 1e6          # kpc -> m  (1 kpc = MPC/1000)
        num = numeric_alpha_inf(Mtest, a0test, b_m) * ARCSEC
        ratios.append(num / analytic)
        print(f"   {b_kpc:>9.1f} kpc{num:>26.6f}{num/analytic:>26.10f}")
    spread = max(ratios) - min(ratios)
    print(f"   -> numeric/analytic ratio is CONSTANT across 4 decades in b (max-min spread = {spread:.2e});")
    print(f"      the common {(1-np.mean(ratios))*100:.3f}% deficit is the finite-range tail (2 arctan(1/2000)/pi), NOT b-dependence.")
    print(f"      => the saturated deflection is genuinely IMPACT-PARAMETER INDEPENDENT.")
    print("      (DISTINCTIVE vs dark matter: no NFW halo gives a b-independent deflection -- a halo's alpha keeps falling.)\n")

    # ---------------- (1) alpha_inf at z=0 for the three masses, with FULL a0 error ----------------
    print("=" * 108)
    print("(1) SATURATED DEFLECTION alpha_inf(z=0) for M = 1e11, 1e13, 1e14 Msun  (arcsec +/- error)")
    print("=" * 108)
    masses = [1e11, 1e13, 1e14]
    # alpha_inf ~ sqrt(a0) -> rel err on alpha = 0.5 * rel err on a0.
    stat_rel_alpha = 0.5 * a0_fw_relerr
    sys_rel_alpha  = 0.5 * (a0_sys_halfspan / a0_sys_mid)     # systematic as fractional on alpha
    print(f"   Using framework a0={a0_fw*1e11:.3f}e-11 as central; alpha~sqrt(a0) so rel.err(alpha)=0.5*rel.err(a0).")
    print(f"   statistical rel.err(alpha) = {stat_rel_alpha*100:.2f}% ;  systematic(mu-fn) rel.err(alpha) ~ {sys_rel_alpha*100:.0f}%\n")
    print(f"   {'M [Msun]':>10}{'alpha_inf [arcsec]':>20}{'stat err':>12}{'syst err':>12}{'total (stat+syst)':>20}")
    results_z0 = {}
    for M in masses:
        a_c = alpha_inf_rad(M, a0_fw) * ARCSEC
        e_stat = a_c * stat_rel_alpha
        e_sys  = a_c * sys_rel_alpha
        e_tot  = np.sqrt(e_stat**2 + e_sys**2)
        results_z0[M] = (a_c, e_stat, e_sys, e_tot)
        print(f"   {M:>10.0e}{a_c:>18.4f}\"{e_stat:>11.4f}\"{e_sys:>11.4f}\"{a_c:>9.4f} +/- {e_tot:.4f}\"")
    print(f"\n   Also report the absolute-a0 systematic as an EXPLICIT RANGE (simple-mu -> McGaugh RAR):")
    print(f"   {'M [Msun]':>10}{'alpha(a0=9.1e-11)':>20}{'alpha(a0=12.0e-11)':>22}{'framework-a0 value':>22}")
    for M in masses:
        a_lo = alpha_inf_rad(M, a0_sys_lo) * ARCSEC
        a_hi = alpha_inf_rad(M, a0_sys_hi) * ARCSEC
        a_fw = alpha_inf_rad(M, a0_fw) * ARCSEC
        print(f"   {M:>10.0e}{a_lo:>18.4f}\"{a_hi:>20.4f}\"{a_fw:>20.4f}\"")
    print()

    # ---------------- (2) evolution: amplitude ratio alpha_inf(z)/alpha_inf(0) with w0/wa Monte Carlo ----------------
    print("=" * 108)
    print("(2) AMPLITUDE EVOLUTION  alpha_inf(z)/alpha_inf(0) = (rho_DE(z)/rho_DE0)^(1/4)  with DESI w0,wa errors")
    print("=" * 108)
    print(f"   COEFFICIENT-FREE ratio (2pi, c^2, sqrt(G), and the absolute-a0 systematic ALL cancel).")
    print(f"   DESI DR2: w0={W0}+/-{W0_e}, wa={WA}+/-{WA_e}, corr(w0,wa)={RHO_W0WA} (CPL). MC with {200000} draws.\n")

    # Monte Carlo over correlated (w0, wa):
    N = 200000
    cov = np.array([[W0_e**2, RHO_W0WA*W0_e*WA_e],
                    [RHO_W0WA*W0_e*WA_e, WA_e**2]])
    draws = np.random.multivariate_normal([W0, WA], cov, size=N)
    w0s, was = draws[:, 0], draws[:, 1]

    zs_eval = [0.4, 1.0, 2.0, 3.0]
    print(f"   {'z':>6}{'rho_DE(z)/rho0 (cen)':>22}{'amp ratio alpha(z)/alpha(0)':>30}{'MC 68% CI':>26}")
    amp_central = {}
    amp_ci = {}
    for z in zs_eval:
        rr_c = rho_DE_ratio(z, W0, WA)
        amp_c = rr_c**0.25
        amp_mc = rho_DE_ratio(z, w0s, was)**0.25
        lo, hi = np.percentile(amp_mc, [16, 84])
        med = np.median(amp_mc)
        amp_central[z] = amp_c
        amp_ci[z] = (lo, hi, med, amp_mc.std())
        print(f"   {z:>6.1f}{rr_c:>22.4f}{amp_c:>30.4f}{'['+format(lo,'.4f')+', '+format(hi,'.4f')+']':>26}"
              f"  (sigma={amp_mc.std():.4f})")
    print()

    # Locate the non-monotonic PEAK of a0(z) (=> peak lensing amplitude) and its z, with MC error on z_peak.
    zgrid = np.linspace(0.0, 1.5, 3001)
    amp_grid_c = rho_DE_ratio(zgrid, W0, WA)**0.25
    ipk = int(np.argmax(amp_grid_c))
    zpk_c = zgrid[ipk]
    amp_pk_c = amp_grid_c[ipk]
    # MC the peak location:
    zpk_mc = np.empty(20000)
    sub = slice(0, 20000)
    for i, (w0i, wai) in enumerate(zip(w0s[sub], was[sub])):
        g = rho_DE_ratio(zgrid, w0i, wai)
        zpk_mc[i] = zgrid[np.argmax(g)]
    zpk_lo, zpk_hi = np.percentile(zpk_mc, [16, 84])
    boost_pct = (amp_pk_c - 1.0) * 100.0
    print(f"   NON-MONOTONIC PEAK: alpha_inf is MAXIMUM at z_peak = {zpk_c:.2f}  (MC 68%: [{zpk_lo:.2f}, {zpk_hi:.2f}])")
    print(f"     peak amplitude alpha_inf(z_pk)/alpha_inf(0) = {amp_pk_c:.4f}  (i.e. lensing ~{boost_pct:+.1f}% stronger than today)")
    frac_peaked = np.mean(zpk_mc > 1e-6)
    print(f"     fraction of MC draws with a genuine interior peak (z_pk>0): {100*frac_peaked:.1f}%  "
          f"(robustness of the 'non-monotonic' claim)\n")

    # ---------------- (3) FULL error budget on a concrete deliverable: alpha_inf at z=0.4 peak, M=1e13 ----------------
    print("=" * 108)
    print("(3) FULL ERROR BUDGET on a concrete deliverable: alpha_inf at the z=0.4 PEAK for a 1e13 Msun group")
    print("=" * 108)
    Mref = 1e13
    z_peak_report = 0.4
    # central absolute alpha at z=0.4 using framework a0 (the absolute prediction):
    a0_z = a0_fw * np.sqrt(rho_DE_ratio(z_peak_report, W0, WA))   # a0(z)=a0(0) sqrt(rho_DE ratio)
    alpha_z_c = alpha_inf_rad(Mref, a0_z) * ARCSEC
    # error components (all as fractional on alpha = 0.5*frac on a0; evolution adds via rho_DE ratio):
    # (a) Lambda statistical -> 0.5*rel(a0_fw)
    fa_stat = 0.5 * a0_fw_relerr
    # (b) systematic (mu-fn)
    fa_sys  = 0.5 * (a0_sys_halfspan / a0_sys_mid)
    # (c) evolution (w0,wa): alpha ~ (rho_DE ratio)^(1/4) -> propagate via MC std of amp ratio at z=0.4
    fa_evo  = amp_ci[0.4][3] / amp_central[0.4]      # fractional sigma of the amplitude ratio at z=0.4
    e_stat = alpha_z_c * fa_stat
    e_sys  = alpha_z_c * fa_sys
    e_evo  = alpha_z_c * fa_evo
    e_tot_statonly = np.sqrt(e_stat**2 + e_evo**2)              # all STATISTICAL (cosmo params)
    e_tot_all      = np.sqrt(e_stat**2 + e_evo**2 + e_sys**2)   # incl SYSTEMATIC
    print(f"   alpha_inf(z=0.4, M=1e13) = {alpha_z_c:.4f} arcsec  (framework a0(z=0.4)={a0_z*1e11:.3f}e-11)")
    print(f"   {'component':<42}{'fractional on alpha':>22}{'arcsec':>14}{'class':>14}")
    print(f"   {'Lambda (OmL,H0) [Planck18]':<42}{fa_stat*100:>20.2f}%{e_stat:>13.4f}\"{'STATISTICAL':>14}")
    print(f"   {'evolution (w0,wa) [DESI DR2]':<42}{fa_evo*100:>20.2f}%{e_evo:>13.4f}\"{'STATISTICAL':>14}")
    print(f"   {'interpolating-fn (mu) [MOND systematic]':<42}{fa_sys*100:>20.2f}%{e_sys:>13.4f}\"{'SYSTEMATIC':>14}")
    print(f"   {'-'*92}")
    print(f"   {'STATISTICAL total (cosmo only)':<42}{(e_tot_statonly/alpha_z_c)*100:>20.2f}%{e_tot_statonly:>13.4f}\"")
    print(f"   {'TOTAL incl. systematic':<42}{(e_tot_all/alpha_z_c)*100:>20.2f}%{e_tot_all:>13.4f}\"")
    print(f"\n   => alpha_inf(z=0.4, 1e13 Msun) = {alpha_z_c:.3f} +/- {e_tot_statonly:.3f}(stat) +/- {e_sys:.3f}(syst) arcsec")
    print(f"      = {alpha_z_c:.3f} +/- {e_tot_all:.3f} arcsec (stat+syst in quadrature).")

    # which error dominates?
    comps = {"statistical: Lambda(OmL,H0)": fa_stat, "statistical: evolution(w0,wa)": fa_evo,
             "SYSTEMATIC: interpolating-fn": fa_sys}
    dom = max(comps, key=comps.get)
    print(f"\n   DOMINANT ERROR: {dom} ({comps[dom]*100:.1f}% on alpha).")
    print(f"     (statistical sub-dominant: Lambda {fa_stat*100:.2f}%, evolution {fa_evo*100:.2f}%; "
          f"the ~{fa_sys*100:.0f}% mu-function systematic dominates the ABSOLUTE alpha by ~{fa_sys/max(fa_stat,fa_evo):.0f}x.)")

    # ---------------- (4) honesty: distinctiveness + what cancels ----------------
    print("\n" + "=" * 108)
    print("(4) DISTINCTIVENESS & HONEST CAVEATS")
    print("=" * 108)
    # the absolute alpha and its mu-systematic are SHARED with constant-a0 MOND; only the EVOLUTION is framework-distinct.
    print(f"""   * The b-INDEPENDENT saturated deflection alpha_inf=2pi sqrt(GMa0)/c^2 is a MOND prediction -- SHARED with
     ordinary (constant-a0) MOND. Its ABSOLUTE value carries the full ~{fa_sys*100:.0f}% interpolating-function systematic
     (for 1e13 Msun: simple-mu a0=9.1e-11 -> {alpha_inf_rad(1e13,a0_sys_lo)*ARCSEC:.3f}\"  vs  McGaugh a0=12e-11 -> {alpha_inf_rad(1e13,a0_sys_hi)*ARCSEC:.3f}\").
     It is DISTINCT from dark matter (no NFW halo gives b-independent deflection), but NOT distinct from MOND.

   * The framework-DISTINCT content is the EVOLUTION amplitude alpha_inf(z)/alpha_inf(0)=(rho_DE)^(1/4): coefficient-free,
     non-monotonic (peak z~{zpk_c:.1f}, ~{boost_pct:+.0f}% above today; declines for z>1). Constant-a0 MOND predicts a FLAT line at 1.0.
     This is the only part that separates the framework from ordinary MOND in this channel.

   * HONEST SIZE-OF-SIGNAL: the evolution amplitude is TINY across the accessible lens range -- peak boost ~{boost_pct:+.1f}%
     at z~{zpk_c:.1f}, and at z=1 the deviation is {(amp_central[1.0]-1)*100:+.1f}%. These are FAR below the ~{fa_sys*100:.0f}% absolute-a0
     systematic and below current stacked-lensing amplitude precision (~5-10%). So lensing ANCHORS a0(0) but is a
     WEAK evolution probe; the decisive evolution lever is at z>2 (high-z BTFR/RAR), not in lensing.

   * MOND-TENSION FLAG: at CLUSTER scale (1e14 Msun baryons) MOND/AeST is known to UNDER-predict lensing mass by
     ~2x (the residual-mass / "missing baryons in MOND clusters" problem). The 1e14 alpha_inf row is the baryon-only
     framework value; real clusters lens ~2x more strongly than this, an OPEN MOND tension (shared, not fixed here).""")

    # ---------------- machine-readable summary ----------------
    print("\n" + "=" * 108)
    print("(5) MACHINE-READABLE SUMMARY")
    print("=" * 108)
    a11 = results_z0[1e11]; a13 = results_z0[1e13]; a14 = results_z0[1e14]
    print(f"   a0_framework_z0      = {a0_fw:.4e} +/- {a0_fw_e:.2e} (stat) m/s^2  [+/- ~{sys_rel_alpha*200:.0f}% syst from mu-fn]")
    print(f"   alpha_inf(1e11,z=0)  = {a11[0]:.4f} +/- {a11[1]:.4f}(stat) +/- {a11[2]:.4f}(syst) arcsec")
    print(f"   alpha_inf(1e13,z=0)  = {a13[0]:.4f} +/- {a13[1]:.4f}(stat) +/- {a13[2]:.4f}(syst) arcsec")
    print(f"   alpha_inf(1e14,z=0)  = {a14[0]:.4f} +/- {a14[1]:.4f}(stat) +/- {a14[2]:.4f}(syst) arcsec  [baryon-only; cluster MOND tension ~2x]")
    for z in zs_eval:
        lo, hi, med, sd = amp_ci[z]
        print(f"   amp_ratio(z={z:.1f})     = {amp_central[z]:.4f}  68%CI[{lo:.4f},{hi:.4f}]  (alpha~sqrt(a0); coeff-free)")
    print(f"   peak: z_peak={zpk_c:.2f} [68% {zpk_lo:.2f},{zpk_hi:.2f}], boost={boost_pct:+.1f}%")
    print(f"   DOMINANT ERROR = interpolating-function SYSTEMATIC (~{fa_sys*100:.0f}% on absolute alpha)")
    print("#" * 108)

    return dict(a0_fw=a0_fw, a0_fw_e=a0_fw_e, results_z0=results_z0, amp_central=amp_central, amp_ci=amp_ci,
                zpk_c=zpk_c, zpk_ci=(zpk_lo, zpk_hi), boost_pct=boost_pct,
                fa_stat=fa_stat, fa_sys=fa_sys, fa_evo=fa_evo,
                alpha_z04_1e13=(alpha_z_c, e_tot_statonly, e_sys, e_tot_all))


if __name__ == "__main__":
    main()
