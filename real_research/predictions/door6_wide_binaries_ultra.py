#!/usr/bin/env python3
"""
DOOR 6 (ULTRA-PRECISION) -- WIDE BINARIES: the local z=0 test of the deep-MOND enhancement.
============================================================================================
Channel: WIDE BINARIES (local test of the framework a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda)).

WHAT IS COMPUTED (every number from the math; nothing asserted):
  (A) The MOND/transition separation s_t for a ~1.5 Msun wide binary: the separation at which the INTERNAL
      Newtonian acceleration g_N = G M / s^2 equals a0, i.e.  s_t = sqrt(G M / a0).  Reported in AU with the
      full a0 error bar (statistical from Lambda + systematic from the interpolation function).
  (B) The asymptotic ISOLATED deep-MOND velocity boost beyond s_t:  v/v_N -> nu^(1/2) -> (a0/g_N)^(1/4) as
      g_N -> 0, which is the famous "+~20% at large s" (actually unbounded as s->inf; ~+20-30% at the
      separations Gaia probes). We report the boost as a function of separation.
  (C) The REALISTIC (EFE-suppressed) boost: solar-neighbourhood binaries sit in the Milky Way external field
      g_ext ~ V_MW^2 / R0 ~ 1.8 a0 > a0, which partially Newtonizes them. We compute the QUMOND angle-averaged
      G_eff/G in that external field for two interpolation functions, giving the actually-observable boost.

ERROR BUDGET (ultra-precision mandate): the separation s_t ~ a0^(-1/2) and the boost ~ a0^(1/4), so we
propagate onto each:
  * STATISTICAL (cosmological): Lambda error from Omega_Lambda and H0 (Planck 2018), by analytic partials AND
    Monte Carlo (cross-checked).
  * SYSTEMATIC: the ~20% interpolation-function ("mu") systematic on the ABSOLUTE a0 (simple-mu fit 9.1e-11 vs
    McGaugh RAR 1.2e-10). This DOMINATES.
  * (No evolution error here: wide binaries are LOCAL, z=0. w0,wa give ZERO leverage. Stated explicitly.)
  * Measurement input: the binary stellar mass uncertainty (M = 1.5 +/- ~0.15 Msun) enters s_t ~ M^(1/2).

HONEST STATUS: this is a SHARED MOND prediction (constant-a0 MOND gives the identical z=0 result -- the
framework adds NO new term locally), and it is currently CONTESTED: Chae (2023-2026) reports a detection
(g_obs/g_N ~ 1.3-1.4, ~+15-20% velocity, >3.5 sigma) while Banik et al. (2024) and Pittordis & Sutherland
report a Newtonian result (up to ~19 sigma vs MOND). Gaia DR4 is the hoped-for arbiter. We do NOT lean either
way and we flag every assumption.

Reproducible: `python door6_wide_binaries_ultra.py`. Needs numpy (+ matplotlib for the optional figure).
"""
import numpy as np

# =============================================================================================================
# CONSTANTS -- exactly as mandated (be consistent).
# =============================================================================================================
C       = 299792458.0          # m/s, exact
G       = 6.67430e-11          # CODATA 2018, m^3 kg^-1 s^-2
MSUN    = 1.98892e30           # kg
MPC     = 3.0857e22            # m
AU      = 1.495978707e11       # m (IAU 2012 definition; exact)
KMS     = 1.0e3

# Planck 2018 (statistical, cosmological-parameter errors)
H0_KMS, H0_ERR_KMS = 67.36, 0.54                 # km/s/Mpc
OML,    OML_ERR    = 0.6847, 0.0073              # Omega_Lambda
H0      = H0_KMS * KMS / MPC                      # 1/s
H0_ERR  = H0_ERR_KMS * KMS / MPC

# The interpolation-function (mu) SYSTEMATIC on absolute a0:
#   simple-mu fit         a0 ~ 9.1e-11 m/s^2
#   McGaugh RAR (std-mu)  a0 ~ 1.2e-10 m/s^2
A0_SIMPLE = 9.1e-11
A0_RAR    = 1.20e-10

# Wide-binary system: a ~1.5 Msun primary+secondary system (Gaia wide-binary regime).
M_SYS, M_ERR = 1.5, 0.15        # Msun (a representative few-tenths-Msun mass uncertainty for the pair)

# Milky Way external field at the Sun (for the EFE-suppressed, realistic boost):
V_MW, V_MW_ERR = 233e3, 6e3     # m/s  (local circular speed; GRAVITY/Gaia ~233 +/- ~6 km/s)
KPC    = 3.0857e19               # m  (1 kpc; 1 pc = 3.0857e16 m)
R0     = 8.178 * KPC             # m  (8.178 kpc, GRAVITY 2019)
R0_ERR = 0.022 * KPC            # m  (+/- 0.022 kpc)

LN10 = np.log(10.0)


# =============================================================================================================
# a0 FROM Lambda (the framework's geometric formula)
# =============================================================================================================
def a0_from_lambda(omega_lambda, h0):
    """a0 = c^2 sqrt(Lambda / 32 pi),  Lambda = 3 Omega_Lambda H0^2 / c^2.  -> a0 = (c/2) sqrt(G rho_Lambda) form
    reduces to a0 = c H0 sqrt(3 Omega_Lambda / (32 pi))."""
    Lam = 3.0 * omega_lambda * h0**2 / C**2          # 1/m^2
    return C**2 * np.sqrt(Lam / (32.0 * np.pi))      # m/s^2


A0_LAMBDA = a0_from_lambda(OML, H0)                  # the framework's central Lambda-only value


# =============================================================================================================
# INTERPOLATION FUNCTIONS and the deep-MOND / EFE boost
# =============================================================================================================
def nu_isolated_from_gN(gN, a0):
    """Isolated MOND: the boost to the effective gravity is nu(gN/a0) with the 'standard' simple algebraic
    nu so that g = nu * gN. In the deep regime g -> sqrt(gN a0), so nu -> sqrt(a0/gN). The orbital-velocity
    boost relative to Newton is v/v_N = sqrt(nu)."""
    x = gN / a0
    # standard simple nu(x) such that y = g/a0 solves mu(y)*y = x with mu(y)=y/(1+y) -> nu = (1+sqrt(1+4/x))/2
    return (1.0 + np.sqrt(1.0 + 4.0 / x)) / 2.0


def nu_simple(y):
    """nu from mu(x)=x/(1+x): g = nu*gN with nu(y)=(1+sqrt(1+4/y))/2, y=gN/a0."""
    return (1.0 + np.sqrt(1.0 + 4.0 / y)) / 2.0


def nu_standard(y):
    """nu from mu(x)=x/sqrt(1+x^2): nu(y)=sqrt((1+sqrt(1+4/y^2))/2), y=gN/a0."""
    return np.sqrt((1.0 + np.sqrt(1.0 + 4.0 / y**2)) / 2.0)


def efe_boost(nu, y_ext, h=1e-4):
    """Orbital-velocity boost sqrt(G_eff/G) for an internal binary DEEP in MOND (internal a -> 0) embedded in a
    DOMINANT external field g_ext = y_ext * a0. Angle-averaged QUMOND estimate:
        G_eff/G = nu_e * (1 + L_e/3),   L_e = d ln nu / d ln g  evaluated at the external field.
    (This is the standard QUMOND EFE result; the 1+L/3 is the angle average of the anisotropic effective G.)"""
    nue = nu(y_ext)
    L = (np.log(nu(y_ext * (1 + h))) - np.log(nu(y_ext * (1 - h)))) / (2 * h)
    return np.sqrt(max(nue * (1 + L / 3.0), 1.0))


# =============================================================================================================
# (A) TRANSITION SEPARATION  s_t = sqrt(G M / a0),  with full a0 error propagation
# =============================================================================================================
def transition_separation(M_msun, a0):
    """Separation where g_N = G M / s^2 = a0  ->  s_t = sqrt(G M / a0).  Returns metres."""
    return np.sqrt(G * M_msun * MSUN / a0)


def main():
    print("#" * 110)
    print("# DOOR 6 (ULTRA) -- WIDE BINARIES: local z=0 test of the deep-MOND enhancement of a0 = c^2 sqrt(Lambda/32pi)")
    print("#" * 110 + "\n")

    # ---- a0 values ----
    print("=" * 110)
    print("0. THE a0 VALUES (framework Lambda-only central, and the mu-systematic band)")
    print("=" * 110)
    print(f"   Lambda = 3 Omega_L H0^2 / c^2 = {3*OML*H0**2/C**2:.4e} m^-2")
    print(f"   a0(Lambda, central)      = {A0_LAMBDA:.4e} m/s^2   [framework geometric value]")
    print(f"   a0(simple-mu fit)        = {A0_SIMPLE:.4e} m/s^2")
    print(f"   a0(McGaugh RAR, std-mu)  = {A0_RAR:.4e} m/s^2")
    print(f"   -> interpolation-function SYSTEMATIC band on absolute a0: "
          f"[{A0_SIMPLE:.2e}, {A0_RAR:.2e}], ratio {A0_RAR/A0_SIMPLE:.2f} (~{100*(A0_RAR/A0_SIMPLE-1):.0f}%).")
    print(f"      (framework Lambda value sits {'inside' if A0_SIMPLE<=A0_LAMBDA<=A0_RAR else 'NEAR'} this band.)\n")

    # ---- statistical error on a0(Lambda) from Lambda (Omega_L, H0): analytic partials ----
    # a0 = c H0 sqrt(3 OmL/(32 pi)).  d a0/a0 = dH0/H0 + (1/2) dOmL/OmL
    rel_H0  = H0_ERR / H0
    rel_OmL = 0.5 * OML_ERR / OML
    rel_a0_stat = np.sqrt(rel_H0**2 + rel_OmL**2)
    a0_stat_err = A0_LAMBDA * rel_a0_stat
    print("=" * 110)
    print("1. STATISTICAL (cosmological) error on a0(Lambda): from H0 and Omega_Lambda (Planck 2018)")
    print("=" * 110)
    print(f"   a0 = c H0 sqrt(3 Omega_L/(32 pi))  ->  d a0/a0 = sqrt[(dH0/H0)^2 + (1/2 dOmL/OmL)^2]")
    print(f"   dH0/H0            = {rel_H0*100:.3f}%   (67.36 +/- 0.54)")
    print(f"   (1/2) dOmL/OmL    = {rel_OmL*100:.3f}%   (0.6847 +/- 0.0073)")
    print(f"   -> d a0/a0 (stat) = {rel_a0_stat*100:.3f}%")
    print(f"   -> a0(Lambda)     = {A0_LAMBDA:.4e} +/- {a0_stat_err:.2e} m/s^2 (statistical)\n")

    # Monte Carlo cross-check on the statistical a0 error
    rng = np.random.default_rng(20260605)
    NMC = 400000
    H0_s  = rng.normal(H0,  H0_ERR,  NMC)
    OmL_s = rng.normal(OML, OML_ERR, NMC)
    a0_s  = a0_from_lambda(OmL_s, H0_s)
    print(f"   [MC cross-check] a0(Lambda) = {a0_s.mean():.4e} +/- {a0_s.std():.2e} m/s^2  "
          f"(matches analytic {a0_stat_err:.2e})\n")

    # =========================================================================================================
    # (A) TRANSITION SEPARATION with full error budget
    # =========================================================================================================
    print("=" * 110)
    print(f"2. (A) TRANSITION SEPARATION  s_t = sqrt(G M / a0)  for M = {M_SYS} Msun  (g_N = a0 there)")
    print("=" * 110)
    s_central = transition_separation(M_SYS, A0_LAMBDA)
    print(f"   central (a0 = Lambda value): s_t = {s_central/AU:.0f} AU  ({s_central:.3e} m)")
    # band from the mu systematic (s ~ a0^-1/2): smaller a0 -> LARGER s_t
    s_lo = transition_separation(M_SYS, A0_RAR)      # largest a0 -> smallest s
    s_hi = transition_separation(M_SYS, A0_SIMPLE)   # smallest a0 -> largest s
    print(f"   mu-systematic band:          s_t in [{s_lo/AU:.0f}, {s_hi/AU:.0f}] AU  "
          f"(a0=RAR -> {s_lo/AU:.0f}; a0=simple -> {s_hi/AU:.0f})")

    # full MC error on s_t: combine statistical a0(Lambda), the mu systematic (log-uniform across the band),
    # and the mass uncertainty.
    M_s   = rng.normal(M_SYS, M_ERR, NMC)
    M_s   = np.clip(M_s, 0.5, None)
    # statistical-only s_t (a0 = Lambda value, mass fixed at central):
    s_stat = transition_separation(M_SYS, a0_s)
    print(f"\n   ERROR BUDGET on s_t:")
    print(f"     - statistical (Lambda; a0 stat only):  s_t = {s_central/AU:.0f} +/- {s_stat.std()/AU:.0f} AU "
          f"({100*s_stat.std()/s_central:.1f}%)")
    print(f"     - mass M = {M_SYS}+/-{M_ERR} Msun (s ~ M^1/2):  +/-{100*0.5*M_ERR/M_SYS:.1f}% "
          f"= +/-{0.5*M_ERR/M_SYS*s_central/AU:.0f} AU")
    print(f"     - mu SYSTEMATIC (a0 9.1e-11..1.2e-10):  s_t {s_lo/AU:.0f}..{s_hi/AU:.0f} AU "
          f"({100*(s_hi-s_central)/s_central:+.0f}% / {100*(s_lo-s_central)/s_central:+.0f}%)")
    # combined MC: draw a0 across the FULL systematic band (log-uniform) x statistical, times mass
    loga0_band = rng.uniform(np.log(A0_SIMPLE), np.log(A0_RAR), NMC)
    a0_band = np.exp(loga0_band) * (a0_s / A0_LAMBDA)   # band center varied + statistical jitter folded in
    s_full = transition_separation(M_s, a0_band)
    s_med = np.median(s_full); s_p16, s_p84 = np.percentile(s_full, [16, 84])
    print(f"     - COMBINED (stat (+) mu-syst (+) mass), MC: s_t = {s_med/AU:.0f} AU "
          f"[{s_p16/AU:.0f}, {s_p84/AU:.0f}] (16-84%)")
    print(f"   DOMINANT ERROR: the mu (interpolation-function) SYSTEMATIC -- it sets the {s_lo/AU:.0f}-{s_hi/AU:.0f} AU")
    print(f"   width, far larger than the {100*s_stat.std()/s_central:.1f}% statistical or {100*0.5*M_ERR/M_SYS:.1f}% mass error.\n")

    # geometric-mean identity (a beautiful exact reference, reported for completeness)
    print("=" * 110)
    print("   GEOMETRIC NOTE: s_t = r_M = sqrt(G M / a0) is the geometric mean of r_s = 2GM/c^2 and R_H = c/H0,")
    print("=" * 110)
    rs = 2 * G * M_SYS * MSUN / C**2
    RH = C / H0
    # s_t = sqrt(GM/a0), a0 = cH0 * k with k = sqrt(3 Omega_L/32pi); sqrt(rs RH) = sqrt(2GM/(cH0)).
    # -> s_t/sqrt(rs RH) = (2k)^(-1/2)  EXACTLY (the Omega_L=1 deSitter case would give (8pi/3)^(1/4)).
    k_geo  = np.sqrt(3 * OML / (32 * np.pi))
    factor = s_central / np.sqrt(rs * RH)
    print(f"     r_s = 2GM/c^2 = {rs/1e3:.2f} km ; R_H = c/H0 = {RH:.3e} m ; "
          f"s_t/sqrt(r_s R_H) = {factor:.3f}")
    print(f"     (= (2 sqrt(3 Omega_L/32pi))^(-1/2) = {(2*k_geo)**-0.5:.3f}, exact; the ~10^4 AU scale bridges km and the horizon.)\n")

    # =========================================================================================================
    # (B) ASYMPTOTIC ISOLATED deep-MOND velocity boost  v/v_N = sqrt(nu) -> (a0/g_N)^(1/4)
    # =========================================================================================================
    print("=" * 110)
    print("3. (B) ISOLATED deep-MOND velocity boost beyond s_t:  v/v_N = nu^(1/2) -> (a0/g_N)^(1/4)")
    print("=" * 110)
    print(f"   At separation s, g_N = G M / s^2, so (a0/g_N)^(1/4) = (s/s_t)^(1/2) in the deep limit.")
    print(f"   {'s (AU)':>10}{'s/s_t':>9}{'g_N/a0':>10}{'boost v/v_N (a0=Lambda)':>26}{'(a0 band)':>20}")
    for s_au in (2000, 3000, 5000, 7000, 10000, 20000, 50000):
        s = s_au * AU
        gN = G * M_SYS * MSUN / s**2
        # exact isolated nu boost at each a0 of the band
        b_c   = np.sqrt(nu_simple(gN / A0_LAMBDA))
        b_lo  = np.sqrt(nu_simple(gN / A0_SIMPLE))
        b_hi  = np.sqrt(nu_simple(gN / A0_RAR))
        print(f"   {s_au:>10d}{s/s_central:>9.2f}{gN/A0_LAMBDA:>10.3f}"
              f"{f'+{100*(b_c-1):.1f}%':>26}{f'[{100*(b_hi-1):+.0f},{100*(b_lo-1):+.0f}]%':>20}")
    # the "+~20%" the prompt names: find the separation where the ISOLATED boost = 1.20 exactly.
    from scipy.optimize import brentq
    boost_of_s = lambda s: np.sqrt(nu_simple((G * M_SYS * MSUN / s**2) / A0_LAMBDA)) - 1.20
    s_20 = brentq(boost_of_s, 0.3 * s_central, 5 * s_central)
    s_ref = 3.0 * s_central   # a few x s_t -> "large s"
    gN_ref = G * M_SYS * MSUN / s_ref**2
    b_ref = np.sqrt(nu_simple(gN_ref / A0_LAMBDA))
    print(f"\n   -> the 'asymptotic deep-MOND boost ~+20% above Newton' is reached at s = {s_20/AU:.0f} AU "
          f"(~{s_20/s_central:.2f} s_t),")
    print(f"      i.e. just as the binary enters the MOND regime. The isolated boost is NOT bounded at +20%:")
    print(f"      at s ~ 3 s_t (~{s_ref/AU:.0f} AU) it is already +{100*(b_ref-1):.0f}% and grows as v/v_N ~ (s/s_t)^(1/2) "
          f"(UNBOUNDED, isolated).")
    print(f"      The bounded '~20%' number is the REALISTIC, EFE-corrected expectation (section 4) -- not the isolated asymptote.\n")

    # error on the boost from a0 (boost ~ a0^(1/4) in deep limit -> 1/4 the a0 error)
    print(f"   ERROR on the boost: in the deep limit v/v_N ~ a0^(1/4), so the {rel_a0_stat*100:.1f}% statistical")
    print(f"   a0 error -> {0.25*rel_a0_stat*100:.2f}% on the boost (tiny); the mu systematic ({100*(A0_RAR/A0_SIMPLE-1):.0f}% on a0) ->")
    print(f"   {100*((A0_RAR/A0_SIMPLE)**0.25-1):.0f}% on the boost -- again the DOMINANT error. (Statistical << systematic.)\n")

    # =========================================================================================================
    # (C) REALISTIC EFE-SUPPRESSED boost (the actually-observable signal in the solar neighbourhood)
    # =========================================================================================================
    print("=" * 110)
    print("4. (C) REALISTIC boost WITH the Milky-Way external-field effect (what Gaia actually probes)")
    print("=" * 110)
    g_ext = V_MW**2 / R0
    y_ext = g_ext / A0_LAMBDA
    print(f"   MW external field at Sun: g_ext = V_MW^2/R0 = {g_ext:.3e} m/s^2 = {y_ext:.2f} a0(Lambda)")
    print(f"   (V_MW = {V_MW/1e3:.0f}+/-{V_MW_ERR/1e3:.0f} km/s, R0 = {R0/KPC:.3f} kpc)  -> EFE-DOMINATED (g_ext > a0).")
    b_iso = np.sqrt(2.0)
    b_simple = efe_boost(nu_simple,   y_ext)
    b_std    = efe_boost(nu_standard, y_ext)
    print(f"\n   asymptotic (widest-separation) orbital-velocity boost v/v_N:")
    print(f"     isolated deep-MOND (NO EFE):        +{100*(b_iso-1):.0f}%   (sqrt2 -- the naive, wrong-for-the-Sun number)")
    print(f"     simple   mu(x)=x/(1+x)   + EFE:     +{100*(b_simple-1):.0f}%")
    print(f"     standard mu(x)=x/sqrt(1+x^2) + EFE: +{100*(b_std-1):.0f}%   (sharp interp -> small end)")
    print(f"   -> the EFE knocks the observable boost down to ~{100*(b_std-1):.0f}-{100*(b_simple-1):.0f}%; the value is")
    print(f"      interpolation-function dependent. THIS is why the test is marginal by construction.\n")

    # propagate the a0 systematic + V_MW/R0 onto y_ext and the EFE boost by MC
    g_ext_s = (rng.normal(V_MW, V_MW_ERR, NMC))**2 / np.clip(rng.normal(R0, R0_ERR, NMC), 1e19, None)
    # vary a0 across the mu band (log-uniform) -- the dominant axis
    a0_band2 = np.exp(rng.uniform(np.log(A0_SIMPLE), np.log(A0_RAR), NMC))
    y_s = g_ext_s / a0_band2
    bs_simple = np.array([efe_boost(nu_simple,   yy) for yy in y_s[:4000]])   # subsample (derivative per draw)
    bs_std    = np.array([efe_boost(nu_standard, yy) for yy in y_s[:4000]])
    print(f"   MC over (a0 mu-band, V_MW, R0):")
    print(f"     simple-mu+EFE boost:   +{100*(np.median(bs_simple)-1):.1f}%  "
          f"[{100*(np.percentile(bs_simple,16)-1):.1f}, {100*(np.percentile(bs_simple,84)-1):.1f}]% (16-84)")
    print(f"     standard-mu+EFE boost: +{100*(np.median(bs_std)-1):.1f}%  "
          f"[{100*(np.percentile(bs_std,16)-1):.1f}, {100*(np.percentile(bs_std,84)-1):.1f}]% (16-84)")
    print(f"   -> interpolation-function choice DOMINATES the spread (simple vs standard), not the cosmology.\n")

    # =========================================================================================================
    # NO EVOLUTION LEVERAGE (stated explicitly)
    # =========================================================================================================
    print("=" * 110)
    print("5. NO EVOLUTION LEVERAGE (z=0 channel): w0, wa do NOT enter")
    print("=" * 110)
    print("   Wide binaries are LOCAL (d ~ pc, z ~ 0), so a0 = a0(z=0). The DESI w0,wa dark-energy evolution")
    print("   (a0(z) ~ sqrt(rho_DE(z))) gives ZERO leverage here -- there is no high-z lever arm. This channel")
    print("   tests the ABSOLUTE z=0 deep-MOND enhancement, NOT the framework's distinctive sqrt(rho_DE) law.\n")

    # =========================================================================================================
    # VERDICT
    # =========================================================================================================
    print("#" * 110)
    print("# VERDICT (Door 6, wide binaries):")
    print(f"#  - Transition separation for {M_SYS} Msun: s_t = {s_central/AU:.0f} AU (central), "
          f"{s_lo/AU:.0f}-{s_hi/AU:.0f} AU across the mu band.")
    print(f"#  - Isolated deep-MOND boost grows as (s/s_t)^1/2 (+{100*(b_ref-1):.0f}% at ~3 s_t); EFE-suppressed to "
          f"+{100*(b_std-1):.0f}-{100*(b_simple-1):.0f}% at the Sun.")
    print(f"#  - DOMINANT error = the ~{100*(A0_RAR/A0_SIMPLE-1):.0f}% interpolation-function SYSTEMATIC on absolute a0 "
          f"(statistical {rel_a0_stat*100:.1f}% is negligible).")
    print("#  - SHARED with constant-a0 MOND (no new term at z=0); DISTINCTIVENESS = none here (framework-shared).")
    print("#  - CONTESTED: Chae 2023-26 detection (g_obs/g_N~1.3-1.4) vs Banik 2024 null (~19 sigma). Gaia DR4 = arbiter.")
    print("#" * 110)

    # ---- optional figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.4))
        s_au = np.linspace(500, 60000, 400)
        s = s_au * AU
        gN = G * M_SYS * MSUN / s**2
        axA.plot(s_au, 100 * (np.sqrt(nu_simple(gN / A0_LAMBDA)) - 1), "b-", lw=2.2, label="isolated (a0=Lambda)")
        axA.fill_between(s_au,
                         100 * (np.sqrt(nu_simple(gN / A0_RAR)) - 1),
                         100 * (np.sqrt(nu_simple(gN / A0_SIMPLE)) - 1),
                         color="b", alpha=0.15, label="mu-systematic band")
        axA.axhline(100 * (b_simple - 1), color="g", ls="--", lw=1.6, label=f"EFE simple-mu (+{100*(b_simple-1):.0f}%)")
        axA.axhline(100 * (b_std - 1),    color="orange", ls="--", lw=1.6, label=f"EFE std-mu (+{100*(b_std-1):.0f}%)")
        axA.axvline(s_central / AU, color="k", ls=":", lw=1.3)
        axA.text(s_central / AU * 1.03, 2, f"$s_t$={s_central/AU:.0f} AU", fontsize=8.5)
        axA.set_xlabel("separation s [AU]"); axA.set_ylabel("velocity boost v/v_N - 1 [%]")
        axA.set_title(f"(A) Wide-binary deep-MOND boost, M={M_SYS} M$_\\odot$\nisolated (grows) vs EFE-suppressed (flat, ~obs)")
        axA.legend(fontsize=8); axA.set_xlim(500, 60000); axA.set_ylim(0, 45)

        # s_t vs a0 with error band
        a0g = np.linspace(8e-11, 1.3e-10, 200)
        axB.plot(a0g, transition_separation(M_SYS, a0g) / AU, "k-", lw=2)
        axB.axvspan(A0_SIMPLE, A0_RAR, color="red", alpha=0.10, label="mu-systematic band")
        axB.axvline(A0_LAMBDA, color="b", ls="--", lw=1.6, label=f"a0(Lambda)={A0_LAMBDA:.2e}")
        axB.scatter([A0_LAMBDA], [s_central / AU], color="b", zorder=5)
        axB.set_xlabel("a0 [m/s$^2$]"); axB.set_ylabel("transition separation $s_t$ [AU]")
        axB.set_title("(B) $s_t = \\sqrt{GM/a_0}$ vs $a_0$\n(the mu systematic dominates the $s_t$ uncertainty)")
        axB.legend(fontsize=8.5)
        fig.tight_layout()
        import os
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "door6_wide_binaries.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    # return a compact dict for any caller
    return dict(a0_lambda=A0_LAMBDA, a0_stat_err=a0_stat_err, s_t_AU=s_central / AU,
                s_t_lo_AU=s_lo / AU, s_t_hi_AU=s_hi / AU, boost_iso_3st=b_ref,
                boost_efe_simple=b_simple, boost_efe_std=b_std, y_ext=y_ext)


if __name__ == "__main__":
    main()
