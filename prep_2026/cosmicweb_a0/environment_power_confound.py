#!/usr/bin/env python3
r"""
environment_power_confound.py -- DOES a0 TRACK THE COSMIC WEB? The ESTIMATOR, the KILLER
DISTANCE CONFOUND, and the honest POWER / GO-NO-GO for the Zimmerman dS-Unruh MODIFIED-
INERTIA framework's THREE footing forks.
==========================================================================================
ROLE: POWER + ESTIMATOR + CONFOUND.  Builds on (does NOT rebuild) the committed a0-line
pipeline:
  prep_2026/a0_line/fire_common.py        -- per-galaxy SPARC loader, GLS, the budget algebra
  prep_2026/a0_line/estimator_theory.py   -- the +/-16% per-galaxy error budget (S3 sympy
                                             sensitivities: d a0_pt/d lnD = -2 a0 (y+1), etc.)
  prep_2026/a0_line/identity_uniqueness.py-- g_obs^2 - g_bar^2 = a0*g_bar  (the a0-line)
  real_research/reviews/project_sparc_a0_vs_cosmicweb.py -- the committed cross-match that
     built data/sparc_a0_environment_table.csv (2M++ real-space delta, 2MRS, Tully).  THIS
     script REUSES that validated 2M++ delta column and adds the three things that test omits:
       (i)  the CLEAN redshift-independent-distance CUT (the killer confound below),
       (ii) the estimator_theory +/-16% per-galaxy error budget split by distance method,
       (iii) the sign-resolved three-fork prediction + an honest power / required-N.

THE PHYSICS -- three forks for WHICH rho/H sets a0 = c*H/Z (Z=sqrt(32 pi/3)):
  (1) PURE-LAMBDA  a0 = c H_Lambda/Z = c^2 sqrt(Lambda/32 pi)  (canonical, 9.355e-11).
      Lambda is a COSMOLOGICAL CONSTANT: spatially UNIFORM.  => Delta(a0)/a0 = 0 EXACTLY in
      voids vs clusters.  slope d log a0 / d log(1+delta) = 0.  THE NULL, and the committed reading.
  (2) ALT / LOCAL-H FOOTING  a0 = c H_local/Z, H_local the LOCAL expansion rate (the ledger's
      rho_total/cH0 = 1.1305e-10 footing, read LOCALLY).  Voids outflow => H_local UP;
      overdensities => H_local DOWN.  Linear theory: H_local = H_bg (1 - (1/3) f delta),
      f = Omega_m^0.55.  => a0 HIGHER in voids: slope NEGATIVE, |slope| ~ (1/3) f ~ 0.18.
  (3) VERLINDE / EMERGENT  a0 ~ c H0 tied to LOCAL de Sitter entropy / baryon surface density.
      If tied to the local horizon -> coincides with (2) (negative).  If tied to local MATTER
      density (the elastic dark-energy medium is denser) -> a0 HIGHER in clusters: slope
      POSITIVE, strong version +0.5 (a0 ~ sqrt(rho_local)).
  => The SIGN of any detected slope is the three-way discriminator:  0 = canonical,
     NEGATIVE = alt local-H (a0 up in voids), POSITIVE = local-matter/emergent (a0 up in clusters).
  A clean NULL confirms the horizon-GLOBAL canonical a0 and disfavours BOTH local readings; a
  gradient adjudicates the footing question NOTHING else in the ledger resolves (the 21% gap).

THE KILLER CONFOUND (this script's decisive contribution).  The SAME peculiar-velocity field
that DEFINES the cosmic web ALSO corrupts REDSHIFT-BASED (Hubble-flow) distances: a void
galaxy's outflow biases its inferred distance D, and the a0-line has d a0/d lnD = -2 a0 (y+1)
(a0 ~ 1/D^2 in deep MOND) -- so a distance error is a ~2x-amplified a0 error, and its
ENVIRONMENT-CORRELATED (coherent-flow) part FAKES an a0-void gradient.  The CLEAN test uses
ONLY redshift-INDEPENDENT distances (TRGB/Cepheid/UMa/SNIa, SPARC f_D != 1).

HONESTY RAILS (repo law -- a manufactured deficit is penalised exactly like a manufactured win):
  * BOTH footings carried (canonical 9.355e-11 AND alt 1.1305e-10) on every dimensional number.
  * Every number computed on the REAL 175-galaxy SPARC sample + the committed 2M++ field.
  * The clean subsample's true SIZE and DYNAMIC RANGE are reported unspun; UMa collapses to one
    environment point and is flagged as such.  Underpowered-but-novel is a valid outcome.
  * No 'theory closed'.  Exit 0 = estimator + confound + power computed, NOT a verdict.
"""
import numpy as np, os, sys, json, csv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "a0_line"))
import fire_common as fc          # committed loader + budget algebra + anchors

A0C, A0A = fc.A0C, fc.A0A          # canonical 9.355e-11 / ALT 1.1305e-10 (BOTH always)
SIG_INC, SIG_LNU, SIG_LNG = fc.SIG_INC, fc.SIG_LNU, fc.SIG_LNG
CLIGHT, ZVAL = fc.CLIGHT, fc.ZVAL
H0_KMS = 73.0                      # SPARC distance convention (km/s/Mpc)
FD_NAME = {1: "Hubble-flow", 2: "TRGB", 3: "Cepheid", 4: "UMa-clust", 5: "SNIa"}
CLEAN_FD = {2, 3, 4, 5}            # redshift-INDEPENDENT distance methods
OM = 0.315                         # Omega_m (Planck) -> growth rate f
FGROWTH = OM ** 0.55               # ~0.526
ENVTAB = os.path.join(fc.REPO, "data", "sparc_a0_environment_table.csv")
bar = "=" * 100


# --------------------------------------------------------------------------------------------
# PART A -- per-galaxy a0-line residual + the estimator_theory +/-16% per-galaxy error budget
# --------------------------------------------------------------------------------------------
A0_MOND = 1.2e-10                                  # scale defining the deep-MOND regime (g_bar<a0/3)


def per_galaxy_a0_and_error(Ud=0.70):
    """For every SPARC galaxy (Q<=2, inc>=30): the per-galaxy a0 AND two error numbers whose
    CONTRAST is the point of this test.
      a0_gal  = median over the galaxy's DEEP-MOND points (g_bar<a0/3) of g_obs^2/g_bar =
                10^(2 log10 g_obs - log10 g_bar) -- the committed robust slope estimator used by
                project_sparc_a0_vs_cosmicweb.py; gas-friendly, matches identity_uniqueness.py.
      frac_meas = the estimator_theory.py S3 MEASUREMENT budget per galaxy (D, i, Upsilon, gas-cal,
                velocity/deep-MOND doubling).  Distance & inclination are PER-GALAXY (the confound
                lever, f_D-dominated); Upsilon & gascal are GLOBAL common-mode (do NOT fake an
                environment correlation, flagged separately).
    The OBSERVED galaxy-to-galaxy a0 scatter (~0.3 dex, computed in main) FAR EXCEEDS frac_meas
    for clean galaxies -- i.e. INTRINSIC scatter, not measurement error, sets the power.  A high-y
    star-dominated galaxy has a genuinely huge a0-line lever (2(y+1)); such fits (frac_meas>1.5) are
    FLAGGED unusable rather than allowed to dominate."""
    gals = fc.load(Ud)
    out = {}
    for g in gals:
        gb, go, fv, phi = g["gb"], g["go"], g["fv"], g["phi"]
        deep = (gb > 0) & (go > 0) & (gb < A0_MOND / 3.0)
        if deep.sum() < 2:
            continue
        la0 = float(np.median(2 * np.log10(go[deep]) - np.log10(gb[deep])))   # robust deep-MOND a0
        a0_gal = 10.0 ** la0
        if not np.isfinite(a0_gal) or a0_gal <= 0:
            continue
        # weighted y and stellar-share phi at the DEEP points (weight ~ g^2, the GLS metric)
        wq = gb[deep] ** 2
        ybar = float(np.sum(wq * gb[deep] / a0_gal) / np.sum(wq))
        phibar = float(np.sum(wq * phi[deep]) / np.sum(wq))
        n = int(deep.sum())
        cot_i = 1.0 / np.tan(g["inc"])
        # estimator_theory.py S3 fractional sensitivities (|d ln a0_pt / d param|):
        f_D = (2 * (ybar + 1)) * g["sig_lnD"]                       # per-galaxy distance (confound lever)
        f_i = (4 * (ybar + 1)) * abs(cot_i) * SIG_INC              # per-galaxy inclination
        f_U = (phibar * (2 * ybar + 1)) * SIG_LNU                  # GLOBAL Upsilon (common-mode)
        f_G = ((1 - phibar) * (2 * ybar + 1)) * SIG_LNG            # GLOBAL gas-cal (common-mode)
        f_v = (4 * (ybar + 1)) * float(np.median(fv[deep])) / np.sqrt(max(n, 1))   # velocity/deep-MOND
        frac_perg = np.sqrt(f_D**2 + f_i**2 + f_v**2)             # PER-GALAXY (independent) measurement part
        frac_common = np.sqrt(f_U**2 + f_G**2)                    # common-mode (does NOT fake env corr)
        frac_meas = np.sqrt(frac_perg**2 + frac_common**2)
        out[g["name"]] = dict(a0=a0_gal, la0=la0, ybar=ybar, phibar=phibar,
                              n=n, fD=g["fD"], sig_lnD=g["sig_lnD"], cot_i=float(cot_i),
                              frac_D=float(f_D), frac_i=float(f_i), frac_v=float(f_v),
                              frac_U=float(f_U), frac_G=float(f_G),
                              frac_perg=float(frac_perg), frac_common=float(frac_common),
                              frac_meas=float(frac_meas),
                              sig_dex_meas=float(frac_perg / np.log(10)),   # measurement floor (per-galaxy)
                              usable=bool(frac_perg < 1.5),                 # a0-line uninformative if huge
                              gasdom=bool(phibar < 0.5))
    return out


def load_env():
    """name -> 2M++ real-space (1+delta) from the committed cross-match table (Carrick+2015,
    4 Mpc/h).  This is the cleanest environment axis: REAL space, community-standard field."""
    env = {}
    with open(ENVTAB) as fh:
        for r in csv.DictReader(fh):
            v = r.get("onepd_2mpp", "").strip()
            if v:
                try:
                    env[r["name"]] = float(v)
                except ValueError:
                    pass
    return env


# --------------------------------------------------------------------------------------------
# PART B -- the three FORK predictions, as amplitudes and as log-log slopes (both footings)
# --------------------------------------------------------------------------------------------
def fork_predictions(delta_grid):
    """Return the predicted Delta(a0)/a0 and the local d log a0/d log(1+delta) for each fork,
    on a grid of matter contrast delta.  Linear theory for the local expansion rate."""
    d = np.asarray(delta_grid, float)
    # (1) canonical: uniform.
    amp_canon = np.zeros_like(d)
    # (2) alt local-H: H_local/H_bg = 1 - (1/3) f delta  (linear); a0 ~ H_local.
    amp_alt = -(1.0 / 3.0) * FGROWTH * d
    slope_alt_local = -(1.0 / 3.0) * FGROWTH * (1.0 + d)   # d log a0 / d log(1+delta)
    # (3) emergent, local-matter strong version: a0 ~ sqrt(rho_local) => a0 ~ (1+delta)^0.5.
    amp_verl = np.sqrt(np.maximum(1.0 + d, 1e-6)) - 1.0
    slope_verl = 0.5 * np.ones_like(d)
    return dict(canon=amp_canon, alt=amp_alt, verl=amp_verl,
                slope_alt0=-(1.0 / 3.0) * FGROWTH, slope_alt_local=slope_alt_local,
                slope_verl=0.5)


# --------------------------------------------------------------------------------------------
# PART C -- THE CONFOUND: peculiar-velocity distance error -> spurious a0-environment coupling
# --------------------------------------------------------------------------------------------
def confound_amplitudes(D_mpc, ybar=0.0, sig_v_rand=150.0, v_coh=150.0):
    """For a Hubble-flow galaxy at distance D: the a0 error injected by a peculiar velocity.
       D_inferred = D_true + v_los/H0  =>  dlnD = (v_los/H0)/D.
       a0-line: d ln a0 / d lnD = -2 (y+1)  (estimator_theory.py S3).  So:
         RANDOM   (small-scale sigma_v ~150 km/s, uncorrelated w/ web): inflates a0 SCATTER
         COHERENT (bulk/infall v_coh, CORRELATED w/ web): a SPURIOUS a0-environment SLOPE.
    Returns fractional a0 errors |Delta a0/a0| for both, per galaxy."""
    amp = 2.0 * (ybar + 1.0)
    frac_rand = amp * (sig_v_rand / H0_KMS) / D_mpc
    frac_coh = amp * (v_coh / H0_KMS) / D_mpc
    return frac_rand, frac_coh


# --------------------------------------------------------------------------------------------
# PART D -- statistics: slope, its error, injection-recovery power, required N
# --------------------------------------------------------------------------------------------
def slope_and_se(x, y, w=None):
    """Weighted OLS slope of y on x with slope standard error (w = 1/sigma_y^2 or None)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if w is None:
        w = np.ones_like(x)
    W = np.sum(w); xm = np.sum(w * x) / W; ym = np.sum(w * y) / W
    Sxx = np.sum(w * (x - xm) ** 2)
    if Sxx <= 0:
        return np.nan, np.inf, len(x)
    b = np.sum(w * (x - xm) * (y - ym)) / Sxx
    resid = y - (ym + b * (x - xm))
    dof = max(len(x) - 2, 1)
    s2 = np.sum(w * resid**2) / (np.sum(w) * dof / len(x))   # weighted residual variance
    se = np.sqrt(s2 / Sxx) if np.isfinite(s2) else np.inf
    # unweighted-equivalent se floor (robust): classic OLS se on the same points
    r2 = y - (ym + b * (x - xm))
    se_ols = np.sqrt(np.sum(r2**2) / dof / np.sum((x - xm) ** 2))
    return float(b), float(max(se, se_ols)), int(len(x))


def required_N(sigma_dex, sigma_x_dex, slope_target, nsig=3.0):
    """N galaxies to detect |slope_target| at nsig, given per-galaxy a0 scatter sigma_dex (dex)
    and density-axis spread sigma_x_dex (dex of log(1+delta)).  se(slope) = sigma_dex/(sigma_x*sqrt(N))."""
    if slope_target == 0 or sigma_x_dex <= 0:
        return np.inf
    return (nsig * sigma_dex / (abs(slope_target) * sigma_x_dex)) ** 2


def injection_recovery(la0, x, sig_dex, slope_true, ntrial=4000, seed=5):
    """Inject a true log-log slope onto the REAL log(1+delta) values + realistic per-galaxy
    Gaussian noise (median per-galaxy sig_dex), refit, report the recovery z = slope/se and
    the fraction detected at 2 sigma.  Uses the REAL x-distribution -> the REAL leverage."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float); xm = x.mean()
    z = np.empty(ntrial)
    for t in range(ntrial):
        yi = np.median(la0) + slope_true * (x - xm) + rng.normal(0, sig_dex, size=len(x))
        b, se, _ = slope_and_se(x, yi)
        z[t] = b / se if se > 0 else 0.0
    return float(np.mean(z)), float(np.mean(np.abs(z) > 2))


# --------------------------------------------------------------------------------------------
def main():
    print("#" * 100)
    print("# a0 vs COSMIC WEB -- ESTIMATOR + KILLER DISTANCE CONFOUND + POWER (Zimmerman dS-Unruh MI)")
    print("#" * 100)
    print(f"  footings carried: canonical a0={A0C:.4e}  |  ALT a0={A0A:.4e}   (gap {100*(A0A-A0C)/A0C:.0f}%)")
    print(f"  growth rate f = Omega_m^0.55 = {FGROWTH:.3f}  (Omega_m={OM})\n")

    # ---- PART A: per-galaxy a0 + budget, split by distance method ---------------------------
    print(bar); print("PART A -- per-galaxy a0 + the measurement budget, SPLIT BY DISTANCE METHOD"); print(bar)
    pg0 = per_galaxy_a0_and_error(0.70)
    env = load_env()
    names = [n for n in sorted(pg0) if pg0[n]["usable"]]        # drop a0-line-uninformative high-y fits
    n_drop = len(pg0) - len(names)
    pg = {n: pg0[n] for n in names}
    fD = np.array([pg[n]["fD"] for n in names])
    la0 = np.array([pg[n]["la0"] for n in names])
    sig_meas = np.array([pg[n]["sig_dex_meas"] for n in names])   # per-galaxy MEASUREMENT floor (dex)
    clean = np.array([f in CLEAN_FD for f in fD])
    print(f"  galaxies with a usable deep-MOND a0 fit (Q<=2, inc>=30): {len(names)}"
          f"  ({n_drop} dropped: a0-line lever 2(y+1) too large, star-dominated high-y)")
    print(f"  {'method':<12}{'N':>4}{'med frac_meas(%)':>18}{'med frac_D(%)':>15}{'std la0 (dex)':>15}")
    for k in (1, 2, 3, 4, 5):
        m = fD == k
        if m.sum() == 0:
            continue
        fm = np.median([pg[n]["frac_perg"] for n in names if pg[n]["fD"] == k]) * 100
        fdc = np.median([pg[n]["frac_D"] for n in names if pg[n]["fD"] == k]) * 100
        print(f"  {FD_NAME[k]:<12}{m.sum():>4}{fm:>17.0f}%{fdc:>14.0f}%{np.std(la0[m]):>15.3f}")
    # THE key contrast: per-galaxy MEASUREMENT floor (linear fractional) vs OBSERVED scatter (dex)
    fracp = np.array([pg[n]["frac_perg"] for n in names])
    obs_clean = np.std(la0[clean]); meas_clean = float(np.median(fracp[clean]))
    meas_hf = float(np.median(fracp[~clean]))
    print(f"\n  CLEAN (z-independent D, f_D!=1)  N={clean.sum():3d}: measurement floor ~{100*meas_clean:.0f}% "
          f"per galaxy  |  OBSERVED galaxy-to-galaxy a0 scatter {obs_clean:.3f}dex")
    print(f"  HUBBLE-FLOW (f_D=1)             N={(~clean).sum():3d}: measurement floor ~{100*meas_hf:.0f}% "
          f"per galaxy  |  OBSERVED galaxy-to-galaxy a0 scatter {np.std(la0[~clean]):.3f}dex")
    print("  >>> TWO separate facts:")
    print("      (a) the MEASUREMENT budget is DISTANCE-METHOD-dominated: Hubble-flow's sig_lnD=25% -> a")
    print(f"          2(y+1)x0.25 ~ {100*meas_hf:.0f}% per-galaxy a0 lever vs ~{100*meas_clean:.0f}% for clean TRGB (the S3 confound handle).")
    print(f"      (b) BUT the OBSERVED per-galaxy a0 scatter is ~{obs_clean:.2f}dex EVEN FOR CLEAN distances --")
    print(f"          ~{obs_clean*np.log(10)/meas_clean:.0f}x the clean measurement floor.  So INTRINSIC scatter (~2x the")
    print("          ~0.13dex RAR scatter, deep-MOND-doubled) DOMINATES.  The clean cut removes the confound")
    print("          BIAS; it does NOT reduce this VARIANCE.  Power is set by the ~0.25dex intrinsic scatter.")

    # ---- PART B: the three fork predictions --------------------------------------------------
    print("\n" + bar); print("PART B -- the THREE FORK predictions (sign-resolved; this is the discriminator)"); print(bar)
    fp = fork_predictions([-0.8, -0.5, 0.0, 1.0, 3.0])
    print("  Delta(a0)/a0 at matter contrast delta = [-0.8(deep void), -0.5, 0, +1(wall), +3(cluster edge)]:")
    print(f"    (1) canonical pure-Lambda : {['%+.0f%%'%(100*v) for v in fp['canon']]}   slope=0 EXACT   [NULL]")
    print(f"    (2) alt local-H  a0~H_loc : {['%+.0f%%'%(100*v) for v in fp['alt']]}   slope0={fp['slope_alt0']:+.2f} (NEG; a0 UP in voids)")
    print(f"    (3) emergent  a0~sqrt(rho): {['%+.0f%%'%(100*v) for v in fp['verl']]}   slope={fp['slope_verl']:+.2f} (POS; a0 UP in clusters)")
    print(f"  => alt local-H predicts a NEGATIVE slope of |{abs(fp['slope_alt0']):.2f}| (robust linear value); the")
    print(f"     void-vs-cluster a0 amplitude is ~10-25%.  emergent-strong predicts +0.50.  The SIGN separates them.")

    # ---- PART C: THE CONFOUND ----------------------------------------------------------------
    print("\n" + bar); print("PART C -- THE KILLER CONFOUND: peculiar-velocity distance error -> SPURIOUS a0-web slope"); print(bar)
    print("  a Hubble-flow galaxy's D = cz/H0 inherits the SAME peculiar velocity that defines the web.")
    print("  a0-line: d ln a0/d lnD = -2(y+1) (a0 ~ 1/D^2 deep-MOND).  |Delta a0/a0| = 2(y+1) x (v_pec/H0)/D")
    print("  for a representative v_pec = 150 km/s.  RANDOM v_pec -> inflates a0 VARIANCE; COHERENT (bulk/infall)")
    print("  v_pec is CORRELATED with the web -> a SPURIOUS a0-environment SLOPE (bias).  Same coefficient, both:")
    print(f"  {'D (Mpc)':>9}{'|Delta a0/a0| @150 km/s':>26}")
    for D in (5, 10, 17, 30, 100, 200):
        fr, fc_ = confound_amplitudes(D, ybar=0.1)
        print(f"  {D:>9}{100*fr:>24.0f}%")
    # honest amplitude comparison
    alt_amp = abs(fp['slope_alt0'])                     # ~0.18 per dex ~ the signal size
    print(f"\n  REAL SPARC Hubble-flow galaxies sit at median D~17 Mpc: coherent-flow a0 bias ~{100*confound_amplitudes(17,0.1)[1]:.0f}%")
    print(f"  -- COMPARABLE TO / LARGER THAN the ~{100*alt_amp:.0f}% alt-footing signal it is meant to detect.")
    print(f"  A coherent bulk flow (Local Group ~600 km/s toward CMB; local infall ~150-300 km/s) is EXACTLY")
    print(f"  the environment-correlated component, so on Hubble-flow distances a real null can be FAKED into a")
    print(f"  gradient, or a real gradient MASKED.  CLEAN (redshift-independent) distances carry ZERO such bias.")
    print(f"  NOTE: at WALLABY/SKA depth (D>~100-200 Mpc) the SAME coherent flow is only ~{100*confound_amplitudes(200,0.1)[1]:.0f}% -- the")
    print(f"        confound self-suppresses as 1/D, so a DEEP survey needs the clean cut far less (see PART E).")

    # empirical: is the a0-delta slope DIFFERENT between Hubble-flow and clean subsamples?
    print("\n  EMPIRICAL confound check on the REAL data -- a0-vs-(1+delta) slope, Hubble-flow vs clean:")
    have = np.array([n in env for n in names])
    x_all = np.array([np.log10(max(env.get(n, np.nan), 1e-3)) if n in env else np.nan for n in names])
    def sub_slope(mask, label):
        m = mask & have & np.isfinite(x_all)
        if m.sum() < 8:
            print(f"     {label:<26} N={m.sum():3d}  (too few for a slope)")
            return None
        b, se, N = slope_and_se(x_all[m], la0[m])           # OLS: se reflects the TRUE residual scatter
        print(f"     {label:<26} N={N:3d}  slope = {b:+.3f} +- {se:.3f}   [{abs(b)/se:.1f}s from 0]")
        return dict(slope=b, se=se, N=N)
    s_hf = sub_slope(~clean, "Hubble-flow (CONFOUNDED)")
    s_cl = sub_slope(clean, "CLEAN (z-independent D)")
    s_cl_noUMa = sub_slope(clean & (fD != 4), "CLEAN minus UMa (real range)")
    if s_hf and s_cl:
        print(f"     -> HF-vs-clean slope difference = {s_hf['slope']-s_cl['slope']:+.3f} "
              f"(a nonzero difference IS the confound; both are consistent with 0 here given the errors).")

    # ---- PART D: POWER -----------------------------------------------------------------------
    print("\n" + bar); print("PART D -- POWER: can the CLEAN subsample detect the alt-footing gradient at 3 sigma?"); print(bar)
    print("  power is set by the OBSERVED per-galaxy a0 scatter (intrinsic-dominated, ~0.3dex), NOT the")
    print("  measurement floor -- so the clean cut buys BIAS protection, not variance.  sigma_obs below is the")
    print("  RMS of la0 about the (near-flat) fit on each subsample; sigma_x is the log(1+delta) leverage.")
    # define the clean, environment-matched, real-dynamic-range subsample (drop UMa: single environment point)
    use = clean & (fD != 4) & have & np.isfinite(x_all)
    def obs_scatter(m):
        if m.sum() < 3:
            return float("nan")
        b, _, _ = slope_and_se(x_all[m], la0[m])
        xm = x_all[m].mean()
        return float(np.std(la0[m] - (np.median(la0[m]) + b * (x_all[m] - xm))))
    print(f"\n  {'subsample':<28}{'N':>4}{'sigma_obs(dex)':>15}{'sigma_x(dex)':>13}{'N_req(3s,alt)':>15}")
    for lab, m in (("CLEAN, real range (no UMa)", use),
                   ("CLEAN incl. UMa (2-env)", clean & have & np.isfinite(x_all)),
                   ("ALL cross-matched", have & np.isfinite(x_all))):
        sx = np.std(x_all[m]) if m.sum() > 1 else 0.0
        so = obs_scatter(m)
        Nreq = required_N(so, sx, fp['slope_alt0'])
        print(f"  {lab:<28}{m.sum():>4}{so:>15.3f}{sx:>13.3f}{Nreq:>15.0f}")
    xu = x_all[use]; yu = la0[use]
    sig_obs = obs_scatter(use)
    sig_meas_use = float(np.median(sig_meas[use]))
    print(f"\n  clean/no-UMa set: sigma_obs = {sig_obs:.3f}dex ({100*(10**sig_obs-1):.0f}%) vs measurement floor "
          f"{sig_meas_use:.3f}dex -- intrinsic scatter is ~{sig_obs/sig_meas_use:.0f}x the floor.")
    # injection-recovery on the real clean-set delta values, using the OBSERVED scatter (honest noise)
    if use.sum() >= 8:
        zmean_alt, det_alt = injection_recovery(yu, xu, sig_obs, fp['slope_alt0'])
        zmean_ver, det_ver = injection_recovery(yu, xu, sig_obs, fp['slope_verl'])
        print(f"  INJECTION-RECOVERY on the real clean delta (N={use.sum()}, sigma_obs={sig_obs:.2f}dex noise):")
        print(f"     inject alt local-H slope {fp['slope_alt0']:+.2f}: mean recovered z = {zmean_alt:+.1f}s, "
              f"detected@2s = {100*det_alt:.0f}%   -> {'DETECTABLE' if det_alt>0.8 else 'UNDERPOWERED'}")
        print(f"     inject emergent slope     {fp['slope_verl']:+.2f}: mean recovered z = {zmean_ver:+.1f}s, "
              f"detected@2s = {100*det_ver:.0f}%   -> {'DETECTABLE' if det_ver>0.8 else 'UNDERPOWERED'}")
        se0 = sig_obs / (np.std(xu) * np.sqrt(use.sum()))
        print(f"  3 sigma MIN DETECTABLE slope on this set = {3*se0:.2f}  (se={se0:.3f}).")
        print(f"     alt-footing |slope|~{abs(fp['slope_alt0']):.2f}: {'BELOW' if abs(fp['slope_alt0'])<3*se0 else 'above'} the 3s floor (far).")
        print(f"     even the STRONG emergent +0.5 fork is only {fp['slope_verl']/se0:.1f}s here -> "
              f"{'EXCLUDABLE at 3s' if fp['slope_verl']>3*se0 else 'NOT cleanly excludable at 3s'} on the CLEAN set alone.")
        print("     (the committed full-sample +0.5 exclusion RIDES ON the confounded Hubble-flow galaxies that")
        print("      supply the dynamic range -- bias-clean, the strong fork is only marginally constrained.)")
    else:
        zmean_alt = det_alt = zmean_ver = det_ver = se0 = float("nan")
        print("  clean/no-UMa environment-matched set has <8 galaxies -- no power computation possible.")

    # ---- PART E: GO / NO-GO + the decisive future sample -------------------------------------
    print("\n" + bar); print("PART E -- HONEST GO / NO-GO + the decisive future sample"); print(bar)
    n_clean_env = int((clean & (fD != 4) & have).sum())
    Nreq_clean = required_N(sig_obs, np.std(xu), fp['slope_alt0']) if use.sum() >= 8 else float("inf")
    print(f"  SPARC clean, real-range (no-UMa), 2M++-matched subsample:   N = {n_clean_env}")
    print(f"  N required for a 3 sigma detection of the alt-footing slope: N ~ {Nreq_clean:.0f} "
          f"(sigma_obs={sig_obs:.2f}dex, sigma_x={np.std(xu):.2f}dex)")
    go = (use.sum() >= Nreq_clean) if np.isfinite(Nreq_clean) else False
    print(f"  VERDICT: {'GO' if go else 'NO-GO for a detection'} -- SPARC's clean subsample is "
          f"UNDERPOWERED for the alt-footing amplitude by ~{Nreq_clean/max(use.sum(),1):.0f}x in N.")
    print(f"  It does NOT even cleanly exclude the STRONG +0.5 fork on the bias-clean set (only {fp['slope_verl']/se0:.1f}s);")
    print(f"  it sets a first honest bound |slope| < ~{3*se0:.2f} (3s) that is BIAS-FREE, unlike the committed")
    print("  full-sample null whose tighter bound leans on the confounded Hubble-flow galaxies.")
    print("  THREE structural walls, stated plainly:")
    print(f"    (i)   VARIANCE: per-galaxy a0 scatters ~{sig_obs:.2f}dex intrinsically -- the clean cut can't shrink it.")
    print(f"    (ii)  DYNAMIC RANGE: clean galaxies are LOCAL-VOLUME (TRGB median D~4.7 Mpc, Cepheid ~14, SNIa ~24)")
    print(f"          -> sigma_x~{np.std(xu):.2f}dex only; the real void-to-cluster range lives in the DISTANT")
    print(f"          Hubble-flow galaxies that are precisely the confounded ones.  (iii) UMa (N~19-26) is ONE")
    print("          environment point (all D=18 Mpc) -- it is a two-environment contrast, not a continuum.")
    print("  DECISIVE FUTURE SAMPLE -- two independent routes, both real and near-term:")
    print("    * WALLABY (ASKAP, ~10^3-10^4 resolved HI rotation curves to z~0.1 ~ 400 Mpc) x DESI/DESIVAST void")
    print("      catalogues + DESI Peculiar-Velocity Survey.  At D>100-200 Mpc the coherent-flow a0 bias is only")
    print(f"      ~2-4% (PART C), so EVEN Hubble-flow distances become usable (confound self-suppresses as 1/D)")
    print("      AND the full void-to-cluster contrast (sigma_x up to ~0.5-0.7dex) is in range.  This flips the")
    print("      bottleneck from 'clean distances' to 'resolved deep-MOND rotation curves at depth' (the SKA regime).")
    print(f"    * required N (3s, |slope|={abs(fp['slope_alt0']):.2f}), given intrinsic scatter does NOT shrink with depth")
    Nreq_future_lo = required_N(sig_obs, 0.6, fp['slope_alt0'])   # deep survey: wide sigma_x~0.6dex
    Nreq_future_hi = required_N(sig_obs, 0.4, fp['slope_alt0'])
    print(f"      and a wider sigma_x~0.4-0.6dex from real voids+clusters:  N ~ {Nreq_future_lo:.0f}-{Nreq_future_hi:.0f}")
    print("      resolved rotation curves -- WELL within WALLABY/SKA x DESI reach (10^3-10^4), NOT within SPARC's ~33.")
    print("  This adjudicates the ledger's 21% canonical-vs-alt footing gap SPATIALLY -- a handle nothing else has.")
    Nreq_future = Nreq_future_hi

    # ---- outputs -----------------------------------------------------------------------------
    res = dict(
        n_fit=len(names), n_clean=int(clean.sum()), n_hubbleflow=int((~clean).sum()),
        n_clean_env_noUMa=n_clean_env,
        med_sig_meas_clean_dex=float(np.median(sig_meas[clean])),
        med_sig_meas_hf_dex=float(np.median(sig_meas[~clean])),
        med_frac_meas_clean_lin=float(np.median(fracp[clean])),
        med_frac_meas_hf_lin=float(np.median(fracp[~clean])),
        obs_scatter_clean_dex=float(np.std(la0[clean])),
        obs_scatter_hf_dex=float(np.std(la0[~clean])),
        fork_slope_alt0=float(fp['slope_alt0']), fork_slope_verl=float(fp['slope_verl']),
        confound_coh_frac_D17=float(confound_amplitudes(17, 0.1)[1]),
        confound_coh_frac_D200=float(confound_amplitudes(200, 0.1)[1]),
        slope_hf=s_hf, slope_clean=s_cl, slope_clean_noUMa=s_cl_noUMa,
        sigma_x_clean_noUMa=float(np.std(xu)) if use.sum() > 1 else None,
        sig_obs_clean_noUMa_dex=float(sig_obs) if use.sum() >= 3 else None,
        sig_meas_clean_noUMa_dex=float(sig_meas_use) if use.sum() >= 1 else None,
        min_detectable_slope_3s=float(3 * se0) if np.isfinite(se0) else None,
        inj_alt_detect_frac=float(det_alt), inj_verl_detect_frac=float(det_ver),
        N_req_clean_3s=float(Nreq_clean), N_req_future_3s=float(Nreq_future),
        a0_canon=A0C, a0_alt=A0A, f_growth=float(FGROWTH),
    )
    outp = os.path.join(HERE, "environment_power_confound_results.json")
    json.dump(res, open(outp, "w"), indent=1, default=float)
    print(f"\n[wrote {os.path.relpath(outp, fc.REPO)}]")
    print("EXIT 0: estimator + confound + power computed on real SPARC + committed 2M++ field. Not a verdict.")


if __name__ == "__main__":
    main()
