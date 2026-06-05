#!/usr/bin/env python3
"""
ULTRA-PRECISION: the acceleration scale a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda)
============================================================================================
Full error propagation. Reports a CENTRAL a0 +/- STATISTICAL (cosmological) error, then the
~20% interpolating-function SYSTEMATIC separately. Also: the dimensionless Z = c H_Lambda / a0
and the prefactor kappa in a0 = kappa c sqrt(G rho_Lambda), with error bands, and a check of the
data-allowed bands Z in [4.2,6.0] / kappa in [0.48,0.69]. Compares to observed 1.2e-10 (McGaugh)
and 9.1e-11 (simple-mu).

Every number is COMPUTED here (numpy/scipy). Reproducible: `python ultra_precision_a0.py`.
"""
import numpy as np

# ----------------------------------------------------------------------------------------------
# MANDATED CONSTANTS (exact / CODATA 2018 / standard)
# ----------------------------------------------------------------------------------------------
C    = 299792458.0          # m/s, exact
G    = 6.67430e-11          # m^3 kg^-1 s^-2, CODATA 2018
Msun = 1.98892e30           # kg
MPC  = 3.0857e22            # m

# Planck 2018 (TT,TE,EE+lowE+lensing base-LCDM, the values handed to me)
H0_KMS   = 67.36;  H0_KMS_ERR   = 0.54     # km/s/Mpc
OmL      = 0.6847; OmL_ERR      = 0.0073
Om_m     = 0.3153; Om_m_ERR     = 0.0073   # (not needed for Lambda-only a0; kept for completeness)

# DESI DR2 dark-energy equation of state (CPL), for a0(z) -- not the z=0 scale, but reported for context
W0 = -0.752; W0_ERR = 0.057
WA = -0.86;  WA_ERR = 0.22

# Observed a0 endpoints of the interpolating-function systematic
A0_RAR    = 1.20e-10        # McGaugh radial-acceleration-relation normalization
A0_SIMPLE = 9.1e-11         # simple-mu best fit to SPARC (min RAR scatter)

# Data-allowed bands to confirm (from the repo's coefficient_landscape / factor_of_four logic)
Z_BAND_LO, Z_BAND_HI = 4.2, 6.0
K_BAND_LO, K_BAND_HI = 0.48, 0.69

# ----------------------------------------------------------------------------------------------
# Core relations
# ----------------------------------------------------------------------------------------------
def H0_si(h0_kms):
    return h0_kms * 1.0e3 / MPC                       # s^-1

def Lambda_of(omL, h0_kms):
    """Cosmological constant Lambda = 3 Omega_Lambda H0^2 / c^2  (units 1/m^2)."""
    H0 = H0_si(h0_kms)
    return 3.0 * omL * H0**2 / C**2

def a0_of(omL, h0_kms):
    """Framework acceleration scale a0 = c^2 sqrt(Lambda/32pi)  (m/s^2)."""
    return C**2 * np.sqrt(Lambda_of(omL, h0_kms) / (32.0 * np.pi))

def rho_Lambda_of(omL, h0_kms):
    """Vacuum (dark-energy) mass density rho_Lambda = Lambda c^2 / (8 pi G)  (kg/m^3)."""
    return Lambda_of(omL, h0_kms) * C**2 / (8.0 * np.pi * G)

def H_Lambda_of(omL, h0_kms):
    """de Sitter (asymptotic) Hubble rate H_Lambda = c sqrt(Lambda/3)  (s^-1)."""
    return C * np.sqrt(Lambda_of(omL, h0_kms) / 3.0)

def cH_Lambda_of(omL, h0_kms):
    """The 'Z=1' acceleration c H_Lambda = c^2 sqrt(Lambda/3)  (m/s^2)."""
    return C * H_Lambda_of(omL, h0_kms)

def Z_of(omL, h0_kms, a0):
    return cH_Lambda_of(omL, h0_kms) / a0

def kappa_of(omL, h0_kms, a0):
    """a0 = kappa c sqrt(G rho_Lambda)  ->  kappa = a0 / (c sqrt(G rho_Lambda))."""
    return a0 / (C * np.sqrt(G * rho_Lambda_of(omL, h0_kms)))


def rhoDE_ratio(z, w0=W0, wa=WA):
    """rho_DE(z)/rho_DE0 for CPL w(a)=w0+wa(1-a):  a^{-3(1+w0+wa)} exp(-3 wa (1-a))."""
    a = 1.0 / (1.0 + z)
    return a**(-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))


def fmt(x, n=4):
    return f"{x:.{n}e}"


def main():
    rng = np.random.default_rng(20260605)
    NMC = 4_000_000

    print("#" * 104)
    print("# ULTRA-PRECISION  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda)   [Lambda = 3 OmL H0^2 / c^2]")
    print("#" * 104)
    print(f"  Constants: c={C:.0f} (exact)  G={G:.5e}  Msun={Msun:.5e}  1Mpc={MPC:.4e} m")
    print(f"  Planck18 : H0={H0_KMS}+/-{H0_KMS_ERR} km/s/Mpc   OmegaLambda={OmL}+/-{OmL_ERR}")
    print(f"  DESI DR2 : w0={W0}+/-{W0_ERR}   wa={WA}+/-{WA_ERR}  (used only for a0(z); not the z=0 scale)\n")

    # ----------------------------------------------------------------------------------------
    # (0) central values
    # ----------------------------------------------------------------------------------------
    Lam0   = Lambda_of(OmL, H0_KMS)
    a0_0   = a0_of(OmL, H0_KMS)
    rhoL0  = rho_Lambda_of(OmL, H0_KMS)
    HLam0  = H_Lambda_of(OmL, H0_KMS)
    cHLam0 = cH_Lambda_of(OmL, H0_KMS)
    Zframe = np.sqrt(32.0 * np.pi / 3.0)     # = c H_Lambda / a0 analytically (independent of cosmology)
    kframe = 0.5                              # = 1/2 analytically

    print("=" * 104)
    print("(0) CENTRAL VALUES (Planck-2018 central cosmology)")
    print("=" * 104)
    print(f"   Lambda          = {fmt(Lam0)} m^-2")
    print(f"   rho_Lambda      = {fmt(rhoL0)} kg/m^3   (= {rhoL0/1.67262e-27:.2f} H-atoms/m^3)")
    print(f"   H_Lambda        = {fmt(HLam0)} s^-1     (de Sitter rate; = sqrt(OmL) H0 = {np.sqrt(OmL)*H0_si(H0_KMS):.4e})")
    print(f"   c H_Lambda      = {fmt(cHLam0)} m/s^2   (the 'Z=1' acceleration)")
    print(f"   a0  (framework) = {fmt(a0_0)} m/s^2")
    print(f"   cross-check (c/2)sqrt(G rho_L) = {fmt(0.5*C*np.sqrt(G*rhoL0))}  (identical: {np.isclose(a0_0, 0.5*C*np.sqrt(G*rhoL0))})")
    print(f"   Z = cH_Lambda/a0 = {Zframe:.6f}  (analytic sqrt(32pi/3); numeric {cHLam0/a0_0:.6f})")
    print(f"   kappa            = {kframe:.6f}  (analytic 1/2; numeric {kappa_of(OmL,H0_KMS,a0_0):.6f})")
    print(f"   a0 in 1e-10 units: {a0_0*1e10:.4f} e-10 m/s^2\n")

    # ----------------------------------------------------------------------------------------
    # (1) ANALYTIC linear error propagation of the STATISTICAL (cosmological) error on a0
    #     a0 propto sqrt(OmL) * H0  =>  (da0/a0)^2 = (1/2 dOmL/OmL)^2 + (dH0/H0)^2
    # ----------------------------------------------------------------------------------------
    rel_OmL = 0.5 * OmL_ERR / OmL            # a0 ~ OmL^{1/2}
    rel_H0  = H0_KMS_ERR / H0_KMS            # a0 ~ H0^{1}
    rel_a0_stat = np.hypot(rel_OmL, rel_H0)
    a0_stat_abs = rel_a0_stat * a0_0

    print("=" * 104)
    print("(1) STATISTICAL (cosmological-parameter) error on a0  -- analytic linear propagation")
    print("=" * 104)
    print(f"   a0 propto OmL^(1/2) H0^(1):")
    print(f"     from OmegaLambda: (1/2)(dOmL/OmL) = (1/2)({OmL_ERR}/{OmL}) = {rel_OmL*100:.3f}%")
    print(f"     from H0         :       dH0/H0     =       {H0_KMS_ERR}/{H0_KMS}  = {rel_H0*100:.3f}%")
    print(f"     combined (quadrature)              = {rel_a0_stat*100:.3f}%")
    print(f"   => a0 = {fmt(a0_0)} +/- {fmt(a0_stat_abs)} m/s^2  (statistical)")
    print(f"        = ({a0_0*1e10:.4f} +/- {a0_stat_abs*1e10:.4f}) e-10 m/s^2")
    print(f"   DOMINANT statistical term: {'H0' if rel_H0>rel_OmL else 'Omega_Lambda'} "
          f"({max(rel_H0,rel_OmL)*100:.3f}% vs {min(rel_H0,rel_OmL)*100:.3f}%)\n")

    # ----------------------------------------------------------------------------------------
    # (2) MONTE CARLO cross-check of the statistical error (OmL, H0 Gaussian, independent)
    #     Note: Planck OmL and H0 are correlated, but with only the marginal sigmas given we
    #     treat them independent (conservative, slightly over-estimates the error).
    # ----------------------------------------------------------------------------------------
    omL_s = rng.normal(OmL, OmL_ERR, NMC)
    h0_s  = rng.normal(H0_KMS, H0_KMS_ERR, NMC)
    omL_s = np.clip(omL_s, 1e-6, None)       # keep sqrt real
    a0_s  = a0_of(omL_s, h0_s)
    mc_mean = a0_s.mean(); mc_std = a0_s.std(ddof=1)
    mc_lo, mc_hi = np.percentile(a0_s, [15.865, 84.135])
    print("=" * 104)
    print(f"(2) MONTE CARLO cross-check  (N={NMC:,}; OmL, H0 Gaussian & independent)")
    print("=" * 104)
    print(f"   a0 mean = {fmt(mc_mean)}   std = {fmt(mc_std)}   ({mc_std/mc_mean*100:.3f}%)")
    print(f"   68% interval [{fmt(mc_lo)}, {fmt(mc_hi)}]  (half-width {fmt(0.5*(mc_hi-mc_lo))})")
    print(f"   -> MC std {mc_std/mc_mean*100:.3f}% vs analytic {rel_a0_stat*100:.3f}%  (agree: "
          f"{np.isclose(mc_std/mc_mean, rel_a0_stat, rtol=0.03)})\n")

    # ----------------------------------------------------------------------------------------
    # (3) the ~20% interpolating-function SYSTEMATIC (separate from statistical)
    # ----------------------------------------------------------------------------------------
    # quantify it directly from the two endpoints
    sys_full = (A0_RAR - A0_SIMPLE) / (0.5 * (A0_RAR + A0_SIMPLE))    # full spread / mean
    sys_half = 0.5 * sys_full
    print("=" * 104)
    print("(3) SYSTEMATIC: the interpolating-function (mu/nu-shape) uncertainty on the ABSOLUTE a0")
    print("=" * 104)
    print(f"   McGaugh RAR normalization a0 = {A0_RAR:.3e}")
    print(f"   simple-mu best fit a0        = {A0_SIMPLE:.3e}")
    print(f"   full spread / mean           = {sys_full*100:.1f}%   (half-spread +/-{sys_half*100:.1f}%)")
    print(f"   -> this ~20% SYSTEMATIC is the DOMINANT uncertainty on the absolute scale")
    print(f"      (statistical {rel_a0_stat*100:.2f}% << systematic ~{sys_full*100:.0f}%).\n")

    # ----------------------------------------------------------------------------------------
    # (4) FRAMEWORK a0 vs the two observed values (where does the framework prediction sit?)
    # ----------------------------------------------------------------------------------------
    print("=" * 104)
    print("(4) framework a0 vs observed a0  (is the prediction high/low, and by how much?)")
    print("=" * 104)
    for lab, obs in [("McGaugh RAR (1.2e-10)", A0_RAR), ("simple-mu (9.1e-11)", A0_SIMPLE)]:
        ratio = a0_0 / obs
        # offset in units of the STATISTICAL error only:
        nsig_stat = (a0_0 - obs) / a0_stat_abs
        print(f"   vs {lab:<26}: a0_frame/a0_obs = {ratio:.3f}  "
              f"(framework {'+' if ratio>1 else ''}{(ratio-1)*100:.1f}%);  "
              f"offset = {nsig_stat:+.1f} sigma_stat")
    print(f"   READING: framework a0={a0_0*1e10:.2f}e-10 sits BETWEEN the two endpoints, "
          f"~{(a0_0/A0_SIMPLE-1)*100:.0f}% above simple-mu and ~{(1-a0_0/A0_RAR)*100:.0f}% below McGaugh RAR.")
    print(f"   The whole ~20% gap to the McGaugh value IS the interpolating-function systematic, not a "
          f"statistical discrepancy.\n")

    # ----------------------------------------------------------------------------------------
    # (5) Z = cH_Lambda/a0 and kappa with error bands -- and confirm the data-allowed bands
    # ----------------------------------------------------------------------------------------
    print("=" * 104)
    print("(5) dimensionless Z = cH_Lambda/a0  and prefactor kappa (a0 = kappa c sqrt(G rho_L)) -- with bands")
    print("=" * 104)
    print("   (a) FRAMEWORK Z, kappa are PURE NUMBERS (cosmology-independent): the cosmological errors CANCEL")
    print("       because cH_Lambda and a0 share the same sqrt(Lambda). Verify by MC of Z_frame, kappa_frame:")
    Zfr_s = cH_Lambda_of(omL_s, h0_s) / a0_s
    kfr_s = kappa_of(omL_s, h0_s, a0_s)
    print(f"       Z_frame    = {Zfr_s.mean():.5f} +/- {Zfr_s.std(ddof=1):.2e}  (analytic sqrt(32pi/3)={Zframe:.5f})")
    print(f"       kappa_frame= {kfr_s.mean():.5f} +/- {kfr_s.std(ddof=1):.2e}  (analytic 1/2 = 0.50000)\n")

    print("   (b) EMPIRICAL Z, kappa from the MEASURED a0 (this is where the error lives -- in a0_obs).")
    print("       For each observed a0 we propagate the cosmological error on cH_Lambda / sqrt(G rho_L)")
    print("       (small) AND carry the a0 systematic by using both endpoints:")
    print(f"       {'a0 source':<26}{'a0 [m/s^2]':>13}{'Z = cHL/a0':>13}{'kappa':>11}")
    rows = []
    for lab, obs in [("McGaugh RAR", A0_RAR), ("simple-mu fit", A0_SIMPLE)]:
        Zc = cHLam0 / obs
        kc = obs / (C * np.sqrt(G * rhoL0))
        # cosmological error on the cH_Lambda (resp sqrt(G rho_L)) factor, a0_obs fixed:
        cHL_s = cH_Lambda_of(omL_s, h0_s)
        sgr_s = C * np.sqrt(G * rho_Lambda_of(omL_s, h0_s))
        Zc_err = (cHL_s/obs).std(ddof=1)
        kc_err = (obs/sgr_s).std(ddof=1)
        rows.append((lab, obs, Zc, Zc_err, kc, kc_err))
        print(f"       {lab:<26}{obs:>13.3e}{Zc:>13.3f}{kc:>11.4f}")
    # empirical band spanning the two observed values (the systematic)
    Z_emp_hi = cHLam0 / A0_SIMPLE     # smaller a0 -> larger Z
    Z_emp_lo = cHLam0 / A0_RAR        # larger  a0 -> smaller Z
    k_emp_lo = A0_SIMPLE / (C*np.sqrt(G*rhoL0))
    k_emp_hi = A0_RAR    / (C*np.sqrt(G*rhoL0))
    # cosmological-error widening of those edges (1 sigma):
    cHL_relerr = (cH_Lambda_of(omL_s,h0_s)).std(ddof=1)/cHLam0
    sgr_relerr = (C*np.sqrt(G*rho_Lambda_of(omL_s,h0_s))).std(ddof=1)/(C*np.sqrt(G*rhoL0))
    print(f"\n       EMPIRICAL Z spans [{Z_emp_lo:.3f}, {Z_emp_hi:.3f}] (McGaugh..simple-mu), each +/-{cHL_relerr*100:.2f}% cosmo")
    print(f"       EMPIRICAL kappa spans [{k_emp_lo:.4f}, {k_emp_hi:.4f}], each +/-{sgr_relerr*100:.2f}% cosmo\n")

    # confirm the mandated data-allowed bands
    print("   (c) CONFIRM the data-allowed bands:")
    Z_in = (Z_BAND_LO <= Zframe <= Z_BAND_HI)
    k_in = (K_BAND_LO <= kframe <= K_BAND_HI)
    # widen empirical band by 1-sigma cosmo to test consistency with the quoted band:
    Z_emp_band = (Z_emp_lo*(1-cHL_relerr), Z_emp_hi*(1+cHL_relerr))
    k_emp_band = (k_emp_lo*(1-sgr_relerr), k_emp_hi*(1+sgr_relerr))
    print(f"       quoted Z-band     [{Z_BAND_LO}, {Z_BAND_HI}] ; framework Z={Zframe:.3f} -> IN band: {Z_in}")
    print(f"       quoted kappa-band [{K_BAND_LO}, {K_BAND_HI}] ; framework kappa={kframe:.3f} -> IN band: {k_in}")
    print(f"       empirical Z-band  (data, +/-1sig cosmo) [{Z_emp_band[0]:.2f}, {Z_emp_band[1]:.2f}]  "
          f"vs quoted [{Z_BAND_LO}, {Z_BAND_HI}]")
    print(f"       empirical k-band  (data, +/-1sig cosmo) [{k_emp_band[0]:.3f}, {k_emp_band[1]:.3f}]  "
          f"vs quoted [{K_BAND_LO}, {K_BAND_HI}]")
    # Is the framework value inside the empirical band?
    print(f"       framework Z={Zframe:.3f} inside empirical data band: "
          f"{Z_emp_band[0] <= Zframe <= Z_emp_band[1]}")
    print(f"       framework kappa={kframe:.3f} inside empirical data band: "
          f"{k_emp_band[0] <= kframe <= k_emp_band[1]}\n")

    # ----------------------------------------------------------------------------------------
    # (6) a0(z) evolution-coefficient error from DESI w0, wa (context; cancels in the bridge ratio)
    # ----------------------------------------------------------------------------------------
    print("=" * 104)
    print("(6) a0(z) EVOLUTION (DESI w0,wa) -- the distinctive, framework-specific prediction; MC error band")
    print("=" * 104)
    w0_s = rng.normal(W0, W0_ERR, NMC); wa_s = rng.normal(WA, WA_ERR, NMC)
    print(f"   a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0):")
    print(f"   {'z':>5}{'central':>12}{'+/- (w0,wa)':>16}{'68% interval':>26}")
    for z in [0.5, 1.0, 2.0, 3.0]:
        r_c   = np.sqrt(rhoDE_ratio(z))                       # central
        r_mc  = np.sqrt(rhoDE_ratio(z, w0_s, wa_s))
        r_lo, r_hi = np.percentile(r_mc, [15.865, 84.135])
        print(f"   {z:>5.1f}{r_c:>12.4f}{r_mc.std(ddof=1):>16.4f}     [{r_lo:.4f}, {r_hi:.4f}]")
    # absolute a0(z=3) folding BOTH cosmo(z=0) and DESI(evolution): central +/- combined
    z = 3.0
    a0z_c = a0_0 * np.sqrt(rhoDE_ratio(z))
    # combine: a0(0) MC * sqrt(rhoDE) MC (independent samples)
    a0z_s = a0_s * np.sqrt(rhoDE_ratio(z, w0_s, wa_s))
    print(f"\n   ABSOLUTE a0(z=3) = a0(0) sqrt(rho_DE(3)/rho_DE0):")
    print(f"     central = {fmt(a0z_c)} m/s^2  (= {a0z_c*1e10:.3f} e-10)")
    print(f"     combined stat error (cosmo z=0 (+) DESI evolution): "
          f"+/- {fmt(a0z_s.std(ddof=1))} ({a0z_s.std(ddof=1)/a0z_c*100:.2f}%)")
    # split contributions
    err_evo = (np.sqrt(rhoDE_ratio(z,w0_s,wa_s))).std(ddof=1)/np.sqrt(rhoDE_ratio(z))
    err_cos = rel_a0_stat
    print(f"     of which: evolution (w0,wa) {err_evo*100:.2f}% ; cosmology (OmL,H0) {err_cos*100:.2f}% "
          f"-> {'evolution' if err_evo>err_cos else 'cosmology'} dominates the z=3 statistical error.")
    print(f"   NOTE: the RATIO a0(z)/a0(0) is COEFFICIENT-FREE -- 32pi and c^2 sqrt(G) cancel; only rho_DE(z) enters.")
    print(f"   This evolution is DISTINCTIVE to the framework; constant-a0 MOND predicts a0(z)/a0(0)=1 exactly.\n")

    # ----------------------------------------------------------------------------------------
    # (7) FINAL LEDGER LINE
    # ----------------------------------------------------------------------------------------
    print("#" * 104)
    print("# FINAL (ledger):")
    print(f"#   a0 = c^2 sqrt(Lambda/32pi) = ({a0_0*1e10:.3f} +/- {a0_stat_abs*1e10:.3f}_stat) e-10 m/s^2  "
          f"+/- ~{sys_full*100:.0f}% systematic (mu-shape)")
    print(f"#   = ({a0_0*1e10:.3f} +/- {a0_stat_abs*1e10:.3f}_stat +/- {sys_half*a0_0*1e10:.3f}_sys) e-10 m/s^2")
    print(f"#   Z = cH_Lambda/a0 = {Zframe:.3f} (exact, no cosmo error);  kappa = 1/2 (exact)")
    print(f"#   DOMINANT error: the ~{sys_full*100:.0f}% interpolating-function SYSTEMATIC "
          f"(statistical is only {rel_a0_stat*100:.2f}%, set mostly by H0)")
    print(f"#   vs data: framework {a0_0/A0_SIMPLE:.2f}x simple-mu, {a0_0/A0_RAR:.2f}x McGaugh RAR; "
          f"Z={Zframe:.2f} in [{Z_BAND_LO},{Z_BAND_HI}], kappa=0.50 in [{K_BAND_LO},{K_BAND_HI}].")
    print("#   DISTINCTIVENESS: absolute a0 value & Z/kappa are SHARED with constant-a0 MOND; only a0(z) evolution is DISTINCT.")
    print("#" * 104)

    # return for any programmatic use
    return dict(a0=a0_0, a0_stat=a0_stat_abs, sys_full=sys_full, Z=Zframe, kappa=kframe,
                rel_stat=rel_a0_stat, rel_OmL=rel_OmL, rel_H0=rel_H0)


if __name__ == "__main__":
    main()
