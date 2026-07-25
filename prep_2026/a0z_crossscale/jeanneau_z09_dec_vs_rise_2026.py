#!/usr/bin/env python3
"""
jeanneau_z09_dec_vs_rise_2026.py -- CAN THE DEC-vs-RISE HORIZON FORK BE CALLED AT z~0.9
FROM ALREADY-PUBLISHED DATA?  Estimator + nuisance design, and the honest bottom line.
=======================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework: a0 = c H_Lambda / Z,
Z = sqrt(32 pi/3) = 5.78633, canonical a0(0) = 9.355e-11 m/s^2, and its OWN interpolation
    g_obs = sqrt(g_bar^2 + g_bar a0)   <=>   the a0-line   g_obs^2 - g_bar^2 = a0 g_bar.
Judged on ITS OWN terms.  nu = sqrt(1+1/y) is Milgrom 1999 (PLA 253:273 Eq.9) -- wellhead
credit; the framework's distinctive content is the cH_Lambda/Z COEFFICIENT + the modified-
inertia completion.  McCulloch (MiHsC / quantised inertia) is CREDITED for the Hubble-horizon
reading.  a0's VALUE and the HORIZON CHOICE remain POSITS.  No TOE.  No "theory closed".

THE QUESTION (ROLE = estimator + nuisance design + honest bottom line)
  At z~0.9-1.1 the two horizon readings of the SAME dS-Unruh mechanism are
      DEC  (framework, future de Sitter event horizon):  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
      RISE (McCulloch, Hubble horizon):                 a0(z)/a0(0) = E(z) = H(z)/H0
  and they differ by ~1.7x -- a FACTOR.  MUSE-DARK II (Jeanneau+2026, A&A 709 A120,
  arXiv:2603.28856) is 95 REAL lensed low-mass star-forming rotators at z = 0.50-1.45 with
  lensing-aware 3D forward modelling (GalPaK3D), the best acceleration-dilution lever of any
  high-z sample.  Can the fork be CALLED from it, and if not, what exactly is missing?

WHAT THIS FILE ADDS TO THE COMMITTED CORPUS (it contradicts none of it)
  parents:  desitter_unruh_horizon_fork_2026.py   (the DEC/RISE branches per z)
            a0z_fork_likelihood_2026.py           (joint likelihood, drift nuisance, levers)
            highz_a0_fork_confront_2026.py        (the 11-constraint compilation)
            ../a0_line/estimator_bias_mocks.py    (GLS FORBIDDEN: +10.34 pp bias, FAIL tier)
            ../jeanneau_refit/deep_refit.py       (the FROZEN per-object refit, N=61 deep cut)
  *** THE OPEN DOOR IS NOT WHERE THE PROMPT PLACED IT. ***  The prompt asks "what is needed --
  a per-object table?".  THE PER-OBJECT TABLE IS ALREADY PUBLIC AND ALREADY COMMITTED:
  CDS/VizieR J/A+A/709/A120 (their Table E1, CC-BY-4.0, 95 rows = exactly their fiducial bTFR
  sample), sitting in ../jeanneau_refit/jeanneau26_catalog_cds.csv, already run through a
  hash-frozen deep-acceleration refit.  So this file does NOT forecast a per-object analysis:
  it PERFORMS the DEC-vs-RISE call on the real per-object data and reports the odds.

THREE ESTIMATOR CANDIDATES, AND WHICH ONE ACTUALLY APPLIES (section 2 computes all three)
  (a) the RESOLVED a0-line per point, a0 = (g_obs^2 - g_bar^2)/g_bar, and its exact
      nuisance-free relatives E4/E5/E6 of the committed equation book -- UNAVAILABLE here:
      they need a per-RADIUS baryonic shape, and 70-85% of M_bar in this sample is
      scaling-relation gas with NO radial information at all.
  (b) the DEEP-MOND BTFR a0 = V^4/(G M_bar) -- FORBIDDEN: exactly a0(1+y), i.e. biased HIGH
      by (1+y), SIGN-LOCKED TOWARD RISE.  Using it would MANUFACTURE A DEFICIT.
  (c) the EXACT nu-inverted zero-point readout at fixed g_obs (what the data delivers):
          Delta_b_pred,i = log10[ g_bar(a0 * R(z_i)) / g_bar(a0) ] ,
          g_bar(a0) = ( -a0 + sqrt(a0^2 + 4 g_obs^2) ) / 2
      -- no deep-MOND assumption, per-object dilution EXACT, no lever linearization.
      THIS is the readout for this sample.  Combined across objects with a MEDIAN.

HARD CALIBRATION (a manufactured detection and a manufactured deficit are penalized EQUALLY)
  * MEDIAN-LIKE combination is PRE-REGISTERED (../a0_line/estimator_bias_verdict.json):
    gls_origin +10.34 pp FAIL, theilsen_pairwise -7.93 pp FAIL; median-like PASS (+0.28 to
    +1.34 pp).  GLS IS FORBIDDEN.  Section 2 shows the freeze does NOT pick the framework's
    best case (the plain and trimmed means are both MORE anti-RISE than the median) and that
    estimator choice alone spans ~0.12 dex = ~half the whole DEC-vs-RISE separation.
  * The LCDM-degenerate apparent drift is carried with the LOW exposure w=0.15-0.20 the
    committed likelihood assigns a clean lensed near-a0 bTFR, and section 3 PROVES the drift
    monotonically HELPS DEC-over-RISE here -- so the low w is the ANTI-framework choice.
  * The HI nuisance is carried with the instructed prior M_HI in [0, M_mol] (never zero).
    Less HI => a0 reads HIGH => toward RISE => AGAINST the framework.  Stated, applied, swept.
  * Coherent per-cluster magnification carried: only 5 clusters, so it barely averages down.
  * BOTH footings (canonical cH_Lambda/Z, alt cH0/Z) and all three DESI SNe (w0,wa) pairs.
  * Section 3(iv) reports an INTERNAL FAILURE MEASURED IN THE DATA that no amount of
    framework-friendly reading survives, and it is the reason the answer is NO.
Exit 0 = ran.  NOT a verdict.
"""
import csv
import json
import os

import numpy as np

np.seterr(all="ignore")
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
BAR = "=" * 100
HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, "..", "jeanneau_refit", "jeanneau26_catalog_cds.csv")

# ================================================================= 0. THE FRAMEWORK + LAWS
Z_CONST = np.sqrt(32 * np.pi / 3)
A0_CAN, A0_ALT = 9.355e-11, 1.1305e-10          # canonical cH_Lambda/Z ; alt cH0/Z
OM, OL = 0.3150, 0.6850
DESI = {"Pantheon+": (-0.838, -0.62), "DESY5": (-0.752, -0.86), "Union3": (-0.667, -1.09)}
HEAD = "Pantheon+"                               # the committed fork head
KPC_M = 3.0857e19
SLOPE, BREF = 3.14, 3.54                         # Jeanneau+26 Tab.4 fiducial bTFR (Lelli+19)
SYS_GAS, SYS_REF, SYS_CONV = 0.20, 0.16, 0.06    # the FROZEN honest-band terms (../jeanneau_refit)
CUT_FROZEN = 0.5                                 # frozen cut: g_bar < 0.5 a0_canon
PMAX_LADDER = [0.46, 0.92, 1.22, 1.50]           # committed A_drift prior ladder
W_EXPOSURE = 0.20                                # committed exposure for this point (0.15-0.20)


def rho_de_ratio(z, w0, wa):
    z = np.asarray(z, float)
    return (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1.0 + z))


def R_dec(z, w0, wa):
    return np.sqrt(rho_de_ratio(z, w0, wa))


def R_rise(z, w0, wa):
    z = np.asarray(z, float)
    return np.sqrt(OM * (1.0 + z) ** 3 + OL * rho_de_ratio(z, w0, wa))


def R_flat(z, w0, wa):
    return np.ones_like(np.asarray(z, float))


LAWS = {"DEC": R_dec, "RISE": R_rise, "FLAT": R_flat}
LAW_ORDER = ["DEC", "RISE", "FLAT"]


def g_bar_of(g_obs, a0):
    """Invert the framework's OWN kernel g_obs = sqrt(g_bar^2 + g_bar a0).  EXACT."""
    return 0.5 * (-a0 + np.sqrt(a0 ** 2 + 4.0 * np.asarray(g_obs, float) ** 2))


def DA_kpc_per_arcsec(z, Om=0.30, OLp=0.70, H0=70.0):
    """The PAPER's cosmology, used only for their arcsec->kpc (their convention, logged)."""
    c = 299792.458
    zz = np.linspace(0.0, z, 4096)
    Dc = c / H0 * TRAPZ(1.0 / np.sqrt(Om * (1 + zz) ** 3 + OLp), zz)
    return Dc / (1 + z) * 1e3 * np.pi / (180 * 3600)


print(BAR)
print("DEC vs RISE AT z~0.9 FROM PUBLISHED DATA -- MUSE-DARK II per-object confrontation")
print(BAR)
print(f"  a0 = c H_Lambda / Z,  Z = {Z_CONST:.5f};  canonical a0(0) = {A0_CAN:.4e} m/s^2,"
      f"  alt = {A0_ALT:.4e}.")
w0, wa = DESI[HEAD]
print(f"  DESI DR2 w0waCDM + {HEAD}: (w0,wa) = ({w0}, {wa}).  Om = {OM}, Omega_DE = {OL}.")
print(f"\n  {'z':>5} | {'DEC':>7} | {'RISE':>7} | {'FLAT':>7} | {'RISE/DEC':>9} | {'DEC vs FLAT':>12}")
print("  " + "-" * 66)
for z in [0.50, 0.90, 1.03, 1.06, 1.45, 2.00]:
    d, r = float(R_dec(z, w0, wa)), float(R_rise(z, w0, wa))
    print(f"  {z:>5.2f} | {d:>7.4f} | {r:>7.4f} | {1.0:>7.4f} | {r/d:>8.3f}x | "
          f"{100*(d-1):>+11.2f}%")
_r1 = (A0_CAN * R_rise(1.0, w0, wa)) / (A0_CAN * R_dec(1.0, w0, wa))
_r2 = (A0_ALT * R_rise(1.0, w0, wa)) / (A0_ALT * R_dec(1.0, w0, wa))
assert abs(float(_r1) - float(_r2)) < 1e-15
print(f"  footing check: RISE/DEC at z=1 is {float(_r1):.9f} on canonical and {float(_r2):.9f}")
print("  on alt -> the LAW RATIO is FOOTING-INDEPENDENT.  (The predicted Delta_b is NOT quite:")
print("  the dilution depends on y = g_bar/a0, so both footings are carried explicitly below.)")
print(f"\n  *** DEC vs FLAT at z~1 is a {100*abs(float(R_dec(1.06,w0,wa))-1):.2f}% effect: at this")
print("  redshift the framework's DISTINCTIVE DECLINE IS NOT ACCESSIBLE AT ALL, by any data.")
print("  z~0.9-1.1 can only ever test the MECHANISM fork DEC-vs-RISE (Carl vs McCulloch).")
print("  A 'not-RISE' win at z~1 is a win for DEC-or-FLAT, and FLAT is standard MOND.")

# ============================================ 1. THE REAL PER-OBJECT DATA (already committed)
print("\n" + BAR)
print("1. THE PER-OBJECT TABLE -- ALREADY PUBLIC, ALREADY COMMITTED (not a forecast)")
print(BAR)
rows = list(csv.DictReader(open(CAT)))
assert len(rows) == 95, "must be Jeanneau+26's fiducial N=95 (VizieR J/A+A/709/A120)"
zg = np.array([float(r["zR21"]) for r in rows])
mug = np.array([float(r["muR21"]) for r in rows])
Re_as = np.array([float(r["Reff"]) for r in rows])
logV = np.array([float(r["logV2_0"]) for r in rows])
s_logV = np.array([float(r["s_logV2_0"]) for r in rows])
logV18 = np.array([float(r["logV1_8"]) for r in rows])
logMs = np.array([float(r["logM*"]) for r in rows])
logMHI = np.array([float(r["logMHI"]) for r in rows])
logMMol = np.array([float(r["logMMol"]) for r in rows])
logMbar = np.array([float(r["logMBar"]) for r in rows])
sig0 = np.array([float(r["sigma0"]) for r in rows])
cluster = np.array([r["Cluster"] for r in rows])
assert np.max(np.abs(np.log10(10 ** logMs + 10 ** logMHI + 10 ** logMMol) - logMbar)) < 0.02, \
    "their own M_bar = M* + M_HI + M_mol bookkeeping must reproduce"
kpc_as = np.array([DA_kpc_per_arcsec(zi) for zi in zg])
R_m = 2.0 * Re_as * kpc_as * KPC_M                      # 2 R_e, source-plane (delensed)
g_obs = (10 ** logV * 1e3) ** 2 / R_m
delta_b = logMbar - (SLOPE * logV + BREF)               # the measured per-object offset
f_gas = (10 ** logMHI + 10 ** logMMol) / 10 ** logMbar

GATE_FULL = float(np.median(delta_b))
assert abs(GATE_FULL) < 0.05, "full-95 pipeline gate (their published 0.00 +/- 0.06)"
gb_can, gb_alt = g_bar_of(g_obs, A0_CAN), g_bar_of(g_obs, A0_ALT)
y_can, y_alt = gb_can / A0_CAN, gb_alt / A0_ALT
SEL = gb_can < CUT_FROZEN * A0_CAN                      # the FROZEN cut, exactly as committed
NSEL = int(SEL.sum())
assert NSEL == 61, "the frozen deep cut must reproduce the committed N=61"
print(f"  source: CDS/VizieR J/A+A/709/A120 (Jeanneau+2026 Table E1, CC-BY-4.0), N = {len(rows)}")
print(f"  columns used: z, mu, Reff(source-plane), Incl, logM*, logMHI(NUM), logMMol(Tacconi+20),")
print(f"                logMBar, logV(1.8Re), logV(2.0Re)+posterior sd, sigma0, Cluster")
print(f"  FROZEN GATE  full-95 median Delta_b = {GATE_FULL:+.4f} dex -> reproduces their published")
print(f"               0.00 +/- 0.06 (their Tab.4 b = 3.54 +/- 0.06 vs Lelli+19 b_ref = 3.54).  PASS")
print(f"  FROZEN CUT   g_bar < {CUT_FROZEN} a0_canon  ->  N = {NSEL} of 95  (committed refit: 61).  PASS")
print(f"\n  {'sample':22} {'N':>4} {'z med':>7} {'y=g/a0 med':>11} {'L=1/(1+2y)':>11} "
      f"{'f_gas med':>10} {'Delta_b med':>12}")
print("  " + "-" * 84)
for lab, m in [("full 95 (published)", np.ones(95, bool)), (f"frozen deep cut (N={NSEL})", SEL)]:
    ym = float(np.median(y_can[m]))
    print(f"  {lab:22} {int(m.sum()):>4} {float(np.median(zg[m])):>7.3f} {ym:>11.3f} "
          f"{1/(1+2*ym):>11.3f} {float(np.median(f_gas[m])):>10.3f} "
          f"{float(np.median(delta_b[m])):>+12.4f}")
DB_MEAS = float(np.median(delta_b[SEL]))
print(f"\n  the frozen refit's headline, reproduced: Delta_b(deep 61) = {DB_MEAS:+.4f} dex")
print(f"  NOTE the acceleration lever this sample actually delivers: median y = "
      f"{float(np.median(y_can[SEL])):.3f}")
print(f"  => L = {1/(1+2*float(np.median(y_can[SEL]))):.3f}, i.e. {100/(1+2*float(np.median(y_can[SEL]))):.0f}% of the")
print("  deep-MOND lever.  That is FAR better than the compilation's assumed L=0.477 (which used a")
print("  y~0.55 ESTIMATE for the full sample) -- the real per-object numbers are more favourable.")

# ==================================================== 2. THE PER-OBJECT a0 READOUT (ESTIMATOR)
print("\n" + BAR)
print("2. ESTIMATOR DESIGN -- WHICH a0 READOUT APPLIES TO A LENSED ROTATOR, ON THE")
print("   FRAMEWORK'S OWN RELATIONS, AND THE PRE-REGISTERED MEDIAN-LIKE COMBINATION")
print(BAR)
print("""  (a) THE RESOLVED a0-LINE, a0 = (g_obs^2 - g_bar^2)/g_bar per point.
      Requires an INDEPENDENT g_bar(r) -- a resolved baryonic mass profile.  This sample gives
      a single-Sersic F160W R_e + B/T for the STARS only, and 70-85% of M_bar is Tacconi+20 /
      NeutralUniverseMachine SCALING-RELATION gas with NO radial information whatsoever.  The
      equation book's exact nuisance-free relatives are equally blocked: E4 (the pair estimator,
      D and sin i cancel), E5 (the three-radius polygon) and E6 (kinematic distance) all need
      the per-RADIUS photometric shape s_j.  The catalogue has TWO radii, v(1.8Re) and v(2.0Re),
      but (i) they straddle nothing -- both are deep, and E4 is documented SINGULAR for
      deep-deep pairs -- and (ii) only MARGINAL posterior sds are published, no covariance
      between the two, so even their DIFFERENCE has no usable error.  => NOT AVAILABLE.
  (b) THE DEEP-MOND BTFR, a0 = V^4/(G M_bar).  This is EXACTLY a0(1+y) under the framework's
      own kernel (proved below), i.e. biased HIGH by the factor (1+y).  SIGN-LOCKED TOWARD
      RISE.  On this sample that is a real, computable manufactured-deficit trap.  => FORBIDDEN.
  (c) THE EXACT nu-INVERTED ZERO-POINT READOUT at fixed g_obs.  g_obs = v_c(2Re)^2/(2Re) is
      exactly what a lensing-aware 3D forward model delivers; invert the framework's own kernel
      for g_bar at any trial a0 and predict the mass-axis offset per object:
          Delta_b_pred,i(law) = log10[ g_bar(a0 * R_law(z_i)) / g_bar(a0) ]      (EXACT)
      No deep-MOND limit, no lever LINEARIZATION, per-object dilution exact, and it uses only
      quantities this sample actually measures.  => THIS IS THE READOUT.  (It reduces to the
      committed lever d log M / d log a0 = -1/(1+2y) on differentiation, and to the deep-MOND
      bTFR as y -> 0; both checked in the self-check block.)""")
# ---- (b) is exactly a0(1+y): prove it numerically on the real objects, and size the trap
a0_naive = (10 ** logV * 1e3) ** 4 / (6.674e-11 * 10 ** logMbar * 1.989e30)
print(f"\n  the (b) trap, sized on the real objects (its bias is exactly (1+y), sign-locked UP):")
for lab, m in [("full 95", np.ones(95, bool)), ("frozen deep 61", SEL)]:
    ym = float(np.median(y_can[m]))
    print(f"    {lab:16} median y = {ym:.3f}  ->  naive/true a0 = 1+y = {1+ym:.3f} "
          f"= {np.log10(1+ym):+.4f} dex TOO HIGH (toward RISE)")
_yt = np.array([0.0, 0.156, 1.0])
_a0t = 1.0e-10
_gt = g_bar_of(np.sqrt((_yt*_a0t)**2 + (_yt*_a0t)*_a0t), _a0t)
assert np.allclose(_gt/_a0t, _yt, rtol=1e-9, atol=1e-14), "kernel inversion identity"
_gb_t = _yt[1:] * _a0t
_naive = ((_gb_t ** 2 + _gb_t * _a0t) / _gb_t)          # = g_obs^2/g_bar
assert np.allclose(_naive, _a0t * (1 + _yt[1:]), rtol=1e-12), "(b) must equal a0(1+y) exactly"
print(f"    identity check  g_obs^2/g_bar = g_bar + a0 = a0(1+y):  True  "
      f"(so readout (b) = a0(1+y) EXACTLY, an ANALYTIC not empirical bias)")

# ---- the PRE-REGISTERED combination and what it COSTS
print("\n  PRE-REGISTERED COMBINATION = MEDIAN-LIKE.  GLS IS FORBIDDEN.")
print("  (../a0_line/estimator_bias_verdict.json, prereg a0_line_estimator_bias_v1, hash-frozen:")
print("   gls_origin +10.34 pp FAIL | theilsen_pairwise -7.93 pp FAIL | median_a0pt +0.84,")
print("   ivw_median +0.66, galaxy_median_then_median +0.31, trimmed_mean +1.13 pp all PASS.)")
_ivw_w = 1.0 / np.maximum(s_logV[SEL] * SLOPE, 1e-3) ** 2
DB_IVW = float(np.sum(delta_b[SEL] * _ivw_w) / np.sum(_ivw_w))
DB_MEAN = float(np.mean(delta_b[SEL]))
DB_TRIM = float(np.mean(np.sort(delta_b[SEL])[6:-6]))
print(f"\n  {'combination':34} {'Delta_b':>9}   status")
print("  " + "-" * 74)
for lab, v, st in [("MEDIAN  <-- PRE-REGISTERED", DB_MEAS, "PASS tier, USED"),
                   ("10% trimmed mean", DB_TRIM, "PASS tier (cross-check)"),
                   ("inverse-variance weighted mean", DB_IVW, "GLS-class: FORBIDDEN"),
                   ("plain mean", DB_MEAN, "mean-like: FORBIDDEN")]:
    print(f"  {lab:34} {v:>+9.4f}   {st}")
EST_SPREAD = float(max(DB_MEAS, DB_TRIM, DB_IVW, DB_MEAN) - min(DB_MEAS, DB_TRIM, DB_IVW, DB_MEAN))
_most_anti_rise = max([("median", DB_MEAS), ("trimmed", DB_TRIM), ("ivw", DB_IVW),
                       ("mean", DB_MEAN)], key=lambda t: t[1])
print(f"\n  ESTIMATOR-CHOICE SPREAD = {EST_SPREAD:.4f} dex across the four combinations.  Since RISE")
print("  predicts a NEGATIVE Delta_b, a HIGHER Delta_b is MORE anti-RISE, i.e. more favourable to")
print(f"  the framework.  The most framework-favourable choice is the '{_most_anti_rise[0]}' "
      f"({_most_anti_rise[1]:+.4f});")
print(f"  the PRE-REGISTERED median is {DB_MEAS:+.4f} and the forbidden GLS-class inverse-variance")
print(f"  mean is {DB_IVW:+.4f}.  So the freeze does NOT pick the framework's best case, and the")
print(f"  spread {EST_SPREAD:.3f} dex is itself ~{EST_SPREAD/0.2305:.0%} of the whole DEC-vs-RISE separation:")
print("  ESTIMATOR CHOICE ALONE IS A SYSTEMATIC OF ORDER HALF THE SIGNAL.  Carried in section 4.")
print(f"  Median efficiency penalty sqrt(pi/2) = {np.sqrt(np.pi/2):.4f} is applied to every")
print("  1/sqrt(N) scaling used in the forecasts of section 7.")

# ==================================================================== 3. THE NUISANCE MODEL
print("\n" + BAR)
print("3. THE NUISANCE MODEL")
print(BAR)


def pred_db(law, a0, w0v, wav, p_drift=0.0, w_exp=0.0, mask=None):
    """EXACT median predicted Delta_b for a law, with apparent-drift (1+z)^(w p) folded into
    the a0 ratio.  Delta_b = log10[g_bar(a0 R_app)/g_bar(a0)] per object, then MEDIAN."""
    m = SEL if mask is None else mask
    R = LAWS[law](zg[m], w0v, wav) * (1.0 + zg[m]) ** (w_exp * p_drift)
    return float(np.median(np.log10(g_bar_of(g_obs[m], a0 * R) / g_bar_of(g_obs[m], a0))))


# ---------------------------------------------------------------- (i) the apparent drift
print("\n  (i) A_drift -- the LCDM-degenerate APPARENT-a0 drift, apparent a0 = true a0 (1+z)^p,")
print("      p >= 0 SIGN-LOCKED (selection/beam/pressure/baryonic all bias fitted a0 UP).")
print("      Magneticum/Mayer+2023 (arXiv:2206.04333) calibration p_MAG = ln3/ln3.3 = 0.920;")
print("      committed prior ladder p ~ U[0,pmax], pmax in " + str(PMAX_LADDER) + ".")
print("      EXPOSURE w for THIS point = 0.15-0.20 (committed a0z_fork_likelihood_2026.py gives")
print("      it w=0.20 MINIMAL vs 1.00 for the direct-RAR points).  CHANNEL-BY-CHANNEL WHY:")
print("        g_obs-selection  SUPPRESSED: the sample is selected on lensing magnification,")
print("                         [OII] S/N and rotation support -- NOT on g_obs; and it KEEPS")
print(f"                         its low-acceleration tail (y down to {float(y_can[SEL].min()):.3f}),")
print("                         the opposite of the selection that manufactures an apparent rise.")
print("        beam smearing    SUPPRESSED TWICE: magnification gives sqrt(mu) source-plane")
print(f"                         resolution (median mu = {float(np.median(mug)):.2f} -> "
      f"{float(np.median(np.sqrt(mug))):.2f}x) AND GalPaK3D forward-models")
print("                         the 3D PSF+LSF (their sqrt(mu)Re/R_PSF > 1/2 cut).")
print("        pressure support NOT suppressed -- the v_c are AD-corrected by a PRESCRIPTION,")
print(f"                         and sigma_0 evolves; median v/sigma_0 = "
      f"{float(np.median(10**logV/sig0)):.2f}.  SURVIVES.")
print("        baryonic evol.   NOT suppressed -- it IS the Tacconi+20/NUM gas prescription's own")
print("                         z-dependence.  SURVIVES.  => 2 of 4 channels live -> w ~ 0.15-0.20.")
print("      It is a ZERO-POINT at one z, not a slope across z, which is why w is minimal.")
print("\n      *** AND THE DRIFT HELPS DEC-over-RISE HERE, SO THE LOW w IS THE ANTI-FRAMEWORK")
print("      CHOICE.  Proof (both predictions move DOWN together, so the measured POSITIVE")
print(f"      Delta_b = {DB_MEAS:+.4f} gets further from RISE than from DEC as p grows):")
print(f"      {'w':>6} {'p':>6} {'pred DEC':>10} {'pred RISE':>10} "
      f"{'|meas-DEC|':>11} {'|meas-RISE|':>12} {'chi2 gap':>9}")
BAND0 = float(np.sqrt(0.070 ** 2 + SYS_GAS ** 2 + SYS_REF ** 2 + SYS_CONV ** 2))
for wv in [0.0, 0.15, 0.20, 0.50, 1.00]:
    for pv in ([0.0] if wv == 0 else [1.22]):
        pD = pred_db("DEC", A0_CAN, w0, wa, pv, wv)
        pR = pred_db("RISE", A0_CAN, w0, wa, pv, wv)
        gap = ((DB_MEAS - pR) ** 2 - (DB_MEAS - pD) ** 2) / BAND0 ** 2
        print(f"      {wv:>6.2f} {pv:>6.2f} {pD:>+10.4f} {pR:>+10.4f} {abs(DB_MEAS-pD):>11.4f} "
              f"{abs(DB_MEAS-pR):>12.4f} {gap:>+9.3f}")
print("      chi2 gap = chi2(RISE) - chi2(DEC): MONOTONE INCREASING in w -> using w=0.20 rather")
print("      than w=1.00 THROWS AWAY DEC-over-RISE evidence.  Conservative, as required.")

# ---------------------------------------------------------------- (ii) the HI nuisance
print("\n  (ii) THE HI NUISANCE.  M_bar = M* + M_HI + M_mol with M_HI from NeutralUniverseMachine")
print("       (0.8 dex scatter in log tau_HI, their sec.4.2) and M_mol from Tacconi+20.  Missing/")
print("       under-counted HI lowers M_bar, raises V^4/(GM_bar), so a0 READS HIGH -> toward RISE,")
print("       i.e. AGAINST the framework's declining branch.  Instructed prior: M_HI ~ U[0, M_mol],")
print("       NEVER zero.  Applied as a re-read of M_bar, coherent and per-object variants:")
rng = np.random.default_rng(20260725)
_Ms, _HI, _Mol = 10 ** logMs, 10 ** logMHI, 10 ** logMMol


def db_med_with(mbar_lin, mask=SEL):
    return float(np.median((np.log10(mbar_lin) - (SLOPE * logV + BREF))[mask]))


HI_ROWS = [("as published (NUM HI)", db_med_with(_Ms + _HI + _Mol)),
           ("HI x 0.5 (frozen stress)", db_med_with(_Ms + 0.5 * _HI + _Mol)),
           ("HI x 2.0 (frozen stress)", db_med_with(_Ms + 2.0 * _HI + _Mol)),
           ("HI = 0 (the extreme rail)", db_med_with(_Ms + _Mol)),
           ("HI = M_mol (prior ceiling)", db_med_with(_Ms + 2.0 * _Mol)),
           ("HI = 0.5 M_mol (prior mid)", db_med_with(_Ms + 1.5 * _Mol))]
_coh = np.array([db_med_with(_Ms + u * _Mol + _Mol) for u in rng.uniform(0, 1, 4000)])
_ind = np.array([db_med_with(_Ms + rng.uniform(0, 1, 95) * _Mol + _Mol) for _ in range(1500)])
print(f"       {'HI treatment':30} {'Delta_b (deep 61)':>18}")
for lab, v in HI_ROWS:
    print(f"       {lab:30} {v:>+18.4f}")
print(f"       {'prior U[0,Mmol] COHERENT':30} {float(np.median(_coh)):>+18.4f}   "
      f"(68% {np.percentile(_coh,16):+.4f}..{np.percentile(_coh,84):+.4f})")
print(f"       {'prior U[0,Mmol] per-object':30} {float(np.median(_ind)):>+18.4f}   "
      f"(68% {np.percentile(_ind,16):+.4f}..{np.percentile(_ind,84):+.4f})")
HI_SPAN = max(v for _, v in HI_ROWS) - min(v for _, v in HI_ROWS)
print(f"       => the HI treatment alone spans {HI_SPAN:.3f} dex, i.e. "
      f"{HI_SPAN/0.2305:.0%} of the DEC-vs-RISE separation.")
print(f"       The instructed prior sits at {float(np.median(_coh)):+.4f}, BELOW the published")
print("       +0.140 -- i.e. obeying the instructed prior WEAKENS the anti-RISE lean. Applied.")

# ------------------------------------------------ (iii) coherent per-cluster magnification
print("\n  (iii) COHERENT PER-CLUSTER MAGNIFICATION.  Derivation on the framework's own terms:")
print("        lensing conserves surface density, so with delensed R_e and lensing-invariant v_c,")
print("        M_bar ~ 1/mu is the ONLY mu-dependence of the bTFR ordinate => d Delta_b/d log mu")
print("        = -1 EXACTLY (and d ln a0/d ln mu = (1+y) in a0 currency).  No per-galaxy sigma_mu")
print("        is published, so this is carried as a per-cluster coherent term.")
uniq, cnt = np.unique(cluster, return_counts=True)
w_cl = cnt / cnt.sum()
red = float(np.sqrt(np.sum(w_cl ** 2)))
SIG_MU_CL, SIG_MU_COM = 0.15, 0.08          # ESTIMATES: HFF strong-lensing model systematics
MU_TERM = float(np.hypot(SIG_MU_CL * red, SIG_MU_COM) / np.log(10))
print(f"        clusters: " + ", ".join(f"{u}({c})" for u, c in zip(uniq, cnt)))
print(f"        N_clusters = {len(uniq)} but effective N_cl = 1/sum(w^2) = {1/np.sum(w_cl**2):.2f}")
print(f"        (A370 alone is {100*w_cl.max():.0f}% of the sample) -> the per-cluster coherent mu")
print(f"        error is reduced only by x{red:.3f}, NOT by 1/sqrt(95)=0.103.")
print(f"        with sigma_mu(per-cluster) = {SIG_MU_CL:.0%} [ESTIMATE] and a common-model")
print(f"        {SIG_MU_COM:.0%} [ESTIMATE]: mu term on Delta_b = {MU_TERM:.4f} dex.")
print("        FLAG: the authors' own global +/-0.2 dex M_bar error is stated to cover")
print("        magnification+SED, so this MAY DOUBLE-COUNT with the frozen 0.20 gas term.")
print("        Both variants are reported in section 4; the difference is small either way.")

# ------------------------------ (iv) THE INTERNAL CONSISTENCY TEST -- MEASURED, NOT ASSUMED
print("\n  (iv) *** THE INTERNAL CONSISTENCY TEST THIS SAMPLE FAILS ***")
print("       An a0(z) effect at FIXED z must not depend on WHERE IN ACCELERATION you look,")
print("       except through the framework's own dilution -- which is computable EXACTLY.  So")
print("       sweep the acceleration cut and compare the MEASURED move against the PREDICTED move.")
print(f"       {'cut g_bar<':>11} {'N':>4} {'z med':>7} {'y med':>7} {'MEAS db':>9} "
      f"{'pred DEC':>9} {'pred RISE':>10} {'meas-DEC':>9}")
print("       " + "-" * 74)
CUTS = [0.2, 0.3, 0.5, 0.7, 1.0, 1e9]
cutrow = {}
for c in CUTS:
    m = gb_can < c * A0_CAN
    if m.sum() < 10:
        continue
    dm = float(np.median(delta_b[m]))
    pD = pred_db("DEC", A0_CAN, w0, wa, mask=m)
    pR = pred_db("RISE", A0_CAN, w0, wa, mask=m)
    cutrow[c] = (int(m.sum()), float(np.median(zg[m])), float(np.median(y_can[m])), dm, pD, pR)
    lab = f"{c:.1f} a0" if c < 100 else "no cut (95)"
    print(f"       {lab:>11} {m.sum():>4} {np.median(zg[m]):>7.3f} {np.median(y_can[m]):>7.3f} "
          f"{dm:>+9.4f} {pD:>+9.4f} {pR:>+10.4f} {dm-pD:>+9.4f}")
MEAS_SWING = max(v[3] for v in cutrow.values()) - min(v[3] for v in cutrow.values())
PRED_SWING_D = max(v[4] for v in cutrow.values()) - min(v[4] for v in cutrow.values())
PRED_SWING_R = max(v[5] for v in cutrow.values()) - min(v[5] for v in cutrow.values())
ZSWING = max(v[1] for v in cutrow.values()) - min(v[1] for v in cutrow.values())
SEP_HEAD = abs(cutrow[CUT_FROZEN][4] - cutrow[CUT_FROZEN][5])
print(f"\n       MEASURED swing across the cut sweep : {MEAS_SWING:.4f} dex")
print(f"       PREDICTED swing, DEC / RISE         : {PRED_SWING_D:.4f} / {PRED_SWING_R:.4f} dex")
print(f"       z-median swing across the sweep     : {ZSWING:.4f}  -> the redshift is FIXED,")
print(f"       so this is NOT an a0(z) effect.  Unmodelled acceleration-correlated systematic")
print(f"       = {MEAS_SWING - PRED_SWING_R:.4f} dex, i.e. {(MEAS_SWING-PRED_SWING_R)/SEP_HEAD:.2f}x the")
print(f"       ENTIRE DEC-vs-RISE separation ({SEP_HEAD:.4f} dex) that the test is trying to resolve.")
print("       Physical read (the committed refit reached the same conclusion by another route):")
print("       the deep objects are the GAS-RICHEST -- f_gas rises from "
      f"{float(np.median(f_gas[gb_can>=1.0*A0_CAN])):.2f} at high acceleration")
print(f"       to {float(np.median(f_gas[gb_can<0.2*A0_CAN])):.2f} at g_bar<0.2a0 -- so the "
      "acceleration axis IS the gas-model axis.")
print("       The NUM HI prescription feeds the low-mass end hardest; that is what the tilt is.")

# ================================================================= 4. FOLD -> THE REAL ODDS
print("\n" + BAR)
print("4. FOLD EVERYTHING -> THE DEC-vs-RISE ODDS AT z~1.06 FROM THE PUBLISHED DATA")
print(BAR)
STAT = 0.070                                   # committed bootstrap stat on the median (N=61)
BANDS = {
    "A  committed frozen band": float(np.sqrt(STAT**2 + SYS_GAS**2 + SYS_REF**2 + SYS_CONV**2)),
    "B  + explicit mu term": float(np.sqrt(STAT**2 + SYS_GAS**2 + SYS_REF**2 + SYS_CONV**2
                                           + MU_TERM**2)),
    "C  + estimator-choice spread": float(np.sqrt(STAT**2 + SYS_GAS**2 + SYS_REF**2 + SYS_CONV**2
                                                  + MU_TERM**2 + (EST_SPREAD/2)**2)),
    "D  + the measured (iv) tilt": float(np.sqrt(STAT**2 + SYS_GAS**2 + SYS_REF**2 + SYS_CONV**2
                                                 + MU_TERM**2 + (EST_SPREAD/2)**2
                                                 + (MEAS_SWING - PRED_SWING_R)**2)),
    "E  stat-only [DO-NOT-CLAIM]": STAT,
}


def ln_evidence_pair(db_meas, band, law, a0, w0v, wav, w_exp=W_EXPOSURE, pmax=1.22, n=801):
    """ln Z of one law: Gaussian on the median Delta_b, drift exponent p ~ U[0,pmax]."""
    if pmax <= 0:
        return -0.5 * ((db_meas - pred_db(law, a0, w0v, wav, 0.0, 0.0)) / band) ** 2
    pg = np.linspace(0.0, pmax, n)
    R = LAWS[law](zg[SEL][:, None], w0v, wav) * (1.0 + zg[SEL][:, None]) ** (w_exp * pg[None, :])
    pr = np.median(np.log10(g_bar_of(g_obs[SEL][:, None], a0 * R)
                            / g_bar_of(g_obs[SEL][:, None], a0)), axis=0)
    lw = -0.5 * ((db_meas - pr) / band) ** 2
    m = lw.max()
    return float(m + np.log(TRAPZ(np.exp(lw - m), pg) / pmax))


def odds(db_meas, band, a0=A0_CAN, w0v=None, wav=None, pmax=1.22, w_exp=W_EXPOSURE):
    w0v = w0 if w0v is None else w0v
    wav = wa if wav is None else wav
    lz = {L: ln_evidence_pair(db_meas, band, L, a0, w0v, wav, w_exp, pmax) for L in LAW_ORDER}
    return lz


L10 = np.log(10.0)
BAR20, BAR3S_DEX = np.log(20.0), 3.0
print(f"  measured (frozen estimator, deep 61):  Delta_b = {DB_MEAS:+.4f} dex")
print(f"  predicted (exact, per-object, canonical footing, {HEAD}):  DEC "
      f"{cutrow[CUT_FROZEN][4]:+.4f} | RISE {cutrow[CUT_FROZEN][5]:+.4f} | FLAT +0.0000")
print(f"  separation DEC-RISE = {SEP_HEAD:.4f} dex   |   DEC-FLAT = "
      f"{abs(cutrow[CUT_FROZEN][4]):.4f} dex (INACCESSIBLE)")
print(f"\n  {'error budget variant':30} {'band':>7} {'sig(RISE)':>10} {'sig(DEC)':>9} "
      f"{'B(DEC/RISE)':>12} {'design B':>9}  clears?")
print("  " + "-" * 96)
ODDS_TABLE = {}
for lab, bd in BANDS.items():
    lz = odds(DB_MEAS, bd)
    lnB = lz["DEC"] - lz["RISE"]
    sR = abs(DB_MEAS - cutrow[CUT_FROZEN][5]) / bd
    sD = abs(DB_MEAS - cutrow[CUT_FROZEN][4]) / bd
    lzA = odds(cutrow[CUT_FROZEN][4], bd)          # Asimov/design: data AT the DEC prediction
    lnBA = lzA["DEC"] - lzA["RISE"]
    ok3 = (sR >= BAR3S_DEX)
    ok20 = (lnB >= BAR20)
    ODDS_TABLE[lab] = dict(band=bd, sig_rise=sR, sig_dec=sD, lnB=lnB, lnB_design=lnBA,
                           clears_3sigma=bool(ok3), clears_20to1=bool(ok20))
    print(f"  {lab:30} {bd:>7.4f} {sR:>10.2f} {sD:>9.2f} {np.exp(lnB):>10.2f}:1 "
          f"{np.exp(lnBA):>7.2f}:1  3s={'Y' if ok3 else 'N'} 20:1={'Y' if ok20 else 'N'}")
print("\n  'design B' = the Asimov odds if the data landed EXACTLY on the DEC prediction: that is")
print("  the DESIGN capability of the measurement, immune to where the gas model happened to put")
print("  the central value.  It is the number to quote for 'can this measurement decide?'.")

# ---------------------------------------- both footings x all three DESI SNe (w0,wa) pairs
print(f"\n  BOTH FOOTINGS x ALL THREE DESI SNe COMPILATIONS (band A, achieved odds):")
print(f"  {'(w0,wa) from':12} {'footing':9} {'a0(0)':>10} {'pred DEC':>9} {'pred RISE':>10} "
      f"{'sep':>7} {'sig(RISE)':>10} {'B(DEC/RISE)':>12}")
print("  " + "-" * 88)
FOOT_TABLE = {}
for comp, (w0v, wav) in DESI.items():
    for fl, a0v in [("canonical", A0_CAN), ("alt", A0_ALT)]:
        pD = pred_db("DEC", a0v, w0v, wav)
        pR = pred_db("RISE", a0v, w0v, wav)
        bd = BANDS["A  committed frozen band"]
        lz = odds(DB_MEAS, bd, a0=a0v, w0v=w0v, wav=wav)
        lnB = lz["DEC"] - lz["RISE"]
        FOOT_TABLE[f"{comp}|{fl}"] = dict(pred_dec=pD, pred_rise=pR, sep=abs(pD - pR),
                                          sig_rise=abs(DB_MEAS - pR) / bd, lnB=lnB)
        print(f"  {comp:12} {fl:9} {a0v:>10.3e} {pD:>+9.4f} {pR:>+10.4f} {abs(pD-pR):>7.4f} "
              f"{abs(DB_MEAS-pR)/bd:>10.2f} {np.exp(lnB):>10.2f}:1")
_sp = [v["sep"] for v in FOOT_TABLE.values()]
_lb = [v["lnB"] for v in FOOT_TABLE.values()]
print(f"  => the fork separation spans {min(_sp):.4f}-{max(_sp):.4f} dex and the odds "
      f"{np.exp(min(_lb)):.2f}-{np.exp(max(_lb)):.2f}:1 across ALL six")
print("     footing x cosmology-input combinations.  The verdict is NOT footing-sensitive and NOT")
print("     (w0,wa)-sensitive: no combination reaches the bar, none is excluded.  Both carried.")

# ==================================================== 5. THE TWO BARS AND THE SHORTFALL
print("\n" + BAR)
print("5. THE BARS, IN ONE CURRENCY, AND THE EXACT SHORTFALL")
print(BAR)
SEP = SEP_HEAD
d_dec, d_ris = float(R_dec(1.06, w0, wa)), float(R_rise(1.06, w0, wa))
gap_a0, mid_a0 = d_ris - d_dec, 0.5 * (d_ris + d_dec)
BARS = {
    "3-sigma, parents' fractional convention gap/(3 mid)":
        np.log10(1.0 + gap_a0 / (3.0 * mid_a0)) * (SEP / np.log10(d_ris / d_dec)),
    "3-sigma, pure-dex convention sep/3": SEP / 3.0,
    "3-sigma relative to the DEC branch (the prompt's ~23%)":
        np.log10(1.0 + gap_a0 / (3.0 * d_dec)) * (SEP / np.log10(d_ris / d_dec)),
    "20:1 Bayes, this single point, DEC vs RISE": SEP / np.sqrt(2.0 * BAR20),
}
print(f"  All bars expressed as the REQUIRED band on Delta_b (dex), using this sample's own")
print(f"  exact per-object separation SEP = {SEP:.4f} dex:")
print(f"  {'bar':56} {'required band':>14} {'shortfall vs A':>15}")
print("  " + "-" * 88)
BAND_A = BANDS["A  committed frozen band"]
for lab, req in BARS.items():
    print(f"  {lab:56} {req:>14.4f} {BAND_A/req:>14.2f}x")
REQ_LOOSEST = max(BARS.values())
REQ_TIGHTEST = min(BARS.values())
print(f"\n  the bars cluster at {REQ_TIGHTEST:.4f}-{REQ_LOOSEST:.4f} dex; the committed band is "
      f"{BAND_A:.4f} dex.")
print(f"  SHORTFALL = {BAND_A/REQ_LOOSEST:.2f}x (loosest bar) to {BAND_A/REQ_TIGHTEST:.2f}x "
      f"(tightest bar) in the ERROR;")
print(f"  = {(BAND_A/REQ_LOOSEST)**2:.1f}x to {(BAND_A/REQ_TIGHTEST)**2:.1f}x in VARIANCE.")
print("  *** AND MORE OBJECTS CANNOT PAY IT. *** Decomposition of the committed band:")
_coh_only = float(np.sqrt(SYS_GAS**2 + SYS_REF**2 + SYS_CONV**2))
print(f"    stat (already the N=61 bootstrap of the median) {STAT:.3f} dex -> "
      f"{100*STAT**2/BAND_A**2:.1f}% of the variance")
print(f"    COHERENT (gas {SYS_GAS} + local-ref {SYS_REF} + convention {SYS_CONV}) "
      f"{_coh_only:.3f} dex -> {100*_coh_only**2/BAND_A**2:.1f}%")
print(f"  Even with N -> infinity the band floors at {_coh_only:.4f} dex, still "
      f"{_coh_only/REQ_LOOSEST:.2f}x-{_coh_only/REQ_TIGHTEST:.2f}x too wide.")
print("  The published +/-0.06 stat error was never the problem, and 95 -> 950 objects buys ~0.")

# ============ 6. A SECOND, REFERENCE-FREE READOUT: THE SAMPLE'S OWN INTERNAL z BASELINE
print("\n" + BAR)
print("6. THE ONE ROUTE THAT NEEDS NO LOCAL REFERENCE: the sample's OWN internal z baseline")
print(BAR)
print("  z = 0.50-1.45 INSIDE the sample.  A Delta_b DIFFERENCE between two z halves cancels the")
print("  local-reference zero-point (0.16 dex) AND any CONSTANT gas/M-L/magnification offset")
print("  exactly -- only their z-DEPENDENCE survives.  Estimator: median-like by construction")
print("  (median Delta_b in each y-bin x z-half, difference, then MEDIAN over y-bins). GLS-free.")
YB = [(0.0, 0.12), (0.12, 0.25), (0.25, 1e9)]
ZS = 0.95


def slope_binmed(dvals, zvals, yvals, ybins=YB, zsplit=ZS):
    ds, bs = [], []
    for a, b in ybins:
        m = (yvals >= a) & (yvals < b)
        lo, hi = m & (zvals < zsplit), m & (zvals >= zsplit)
        if lo.sum() < 4 or hi.sum() < 4:
            continue
        ds.append(np.median(dvals[hi]) - np.median(dvals[lo]))
        bs.append(np.median(np.log10(1 + zvals[hi])) - np.median(np.log10(1 + zvals[lo])))
    if not ds:
        return np.nan, 0
    return float(np.median(np.array(ds) / np.array(bs))), len(ds)


B_MEAS, NB = slope_binmed(delta_b, zg, y_can)
_bs = []
for _ in range(3000):
    ix = rng.integers(0, 95, 95)
    v, k = slope_binmed(delta_b[ix], zg[ix], y_can[ix])
    if k:
        _bs.append(v)
_bs = np.array(_bs)
B_SD = float(0.5 * (np.percentile(_bs, 84) - np.percentile(_bs, 16)))
lo_m, hi_m = zg < ZS, zg >= ZS
BASE = float(np.median(np.log10(1 + zg[hi_m])) - np.median(np.log10(1 + zg[lo_m])))
print(f"\n  baseline between the z halves: d log10(1+z) = {BASE:.4f} "
      f"(N_lo={int(lo_m.sum())}, N_hi={int(hi_m.sum())}); y-bins used = {NB}")
print(f"  {'law / data':34} {'B = dDelta_b/dlog10(1+z)':>26}")
print("  " + "-" * 62)
B_PRED = {}
for L in LAW_ORDER:
    pr = np.log10(g_bar_of(g_obs, A0_CAN * LAWS[L](zg, w0, wa)) / g_bar_of(g_obs, A0_CAN))
    B_PRED[L] = float((np.median(pr[hi_m]) - np.median(pr[lo_m])) / BASE)
    print(f"  {'predicted ' + L:34} {B_PRED[L]:>+26.3f}")
print(f"  {'MEASURED (bin-median, bootstrap)':34} {B_MEAS:>+16.3f} +/- {B_SD:.3f}")
for L in LAW_ORDER:
    print(f"    -> {abs(B_MEAS-B_PRED[L])/B_SD:.2f} sigma from {L}")
lnB_slope = 0.5 * (((B_MEAS - B_PRED["RISE"]) / B_SD) ** 2 - ((B_MEAS - B_PRED["DEC"]) / B_SD) ** 2)
print(f"  => internal-slope odds DEC/RISE = {np.exp(lnB_slope):.2f}:1 "
      f"(clears 20:1? {'YES' if lnB_slope>BAR20 else 'NO'})")
print("\n  WHY THIS IS NOT A RESCUE, STATED BEFORE ANYONE ELSE SAYS IT:")
print("   1. The measured B is ALSO "
      f"{abs(B_MEAS-B_PRED['DEC'])/B_SD:.1f} sigma from DEC and "
      f"{abs(B_MEAS-B_PRED['FLAT'])/B_SD:.1f} sigma from FLAT.  NO LAW FITS IT.")
print("      A readout that rejects every candidate is measuring a systematic, not a0(z).")
print("   2. The two z halves are BADLY mismatched in exactly the confounders that matter:")
print(f"      {'half':6} {'y med':>7} {'f_gas med':>10} {'logM* med':>10} {'v med':>7}")
for lab, m in [("lo z", lo_m), ("hi z", hi_m)]:
    print(f"      {lab:6} {float(np.median(y_can[m])):>7.3f} {float(np.median(f_gas[m])):>10.3f} "
          f"{float(np.median(logMs[m])):>10.2f} {float(np.median(10**logV[m])):>7.0f}")
print("      3 y-bins is a crude control for a factor ~2.6 mismatch in y and ~1.7 in f_gas.")
print("   3. A SLOPE across z is the currency the committed likelihood assigns MAXIMAL drift")
print("      exposure w = 1.00 (not 0.20): the Tacconi/NUM prescription's own z-evolution and the")
print("      [OII]-flux-limited selection both live exactly here.  Marginalizing the drift at")
print("      w=1.00 pushes every predicted B down and the measured B further above all of them.")
print("   4. It shares its data and its gas model with section 4, so it MUST NOT be multiplied in.")
print("  HONEST STATUS: a CONSISTENCY CHECK that independently confirms an unmodelled")
print("  z-dependent systematic in this sample; NOT an independent a0(z) measurement.")

# =========================================== 7. WHAT WOULD CLOSE IT -- RANKED BY REAL COST
print("\n" + BAR)
print("7. WHAT WOULD ACTUALLY CLOSE IT (each row: forecast band -> odds; ESTIMATE-flagged)")
print(BAR)
# the band that makes the CURRENT central value decisive (as opposed to the design bar)
b_need_3s = abs(DB_MEAS - cutrow[CUT_FROZEN][5]) / 3.0
b_need_20 = np.sqrt(((DB_MEAS - cutrow[CUT_FROZEN][5]) ** 2 - (DB_MEAS - cutrow[CUT_FROZEN][4]) ** 2)
                    / (2.0 * BAR20))
print(f"  TWO different 'required band' questions, both answered:")
print(f"    DESIGN   (data lands ON the DEC prediction): {REQ_TIGHTEST:.4f}-{REQ_LOOSEST:.4f} dex")
print(f"    ACHIEVED (data stays at the measured {DB_MEAS:+.4f}):  3s needs <= {b_need_3s:.4f} dex,")
print(f"             20:1 needs <= {b_need_20:.4f} dex  (looser, because the gas model happens to")
print("             put the point on the far side of DEC -- which is why DESIGN is the honest bar)")
print(f"\n  {'closer':52} {'band':>7} {'sig(RISE)':>10} {'B ach.':>9} {'B design':>9}  cost")
print("  " + "-" * 104)
CLOSERS = [
    ("0  nothing new (today, committed band)", BAND_A, "-"),
    ("1  N: 95 -> 950 objects (stat -> 0.022)",
     float(np.sqrt(0.022**2 + SYS_GAS**2 + SYS_REF**2 + SYS_CONV**2)), "HUGE / buys ~0"),
    ("2  drift calibration on their selection fn [EST]",
     BAND_A, "cheap / WRONG LEVER here"),
    ("3  v- and y-MATCHED z~0 control, SAME gas [EST]",
     float(np.sqrt(STAT**2 + 0.07**2 + 0.05**2 + SYS_CONV**2)), "RE-ANALYSIS ONLY"),
    ("4  + per-cluster sigma_mu published by the authors [EST]",
     float(np.sqrt(STAT**2 + 0.07**2 + 0.05**2 + 0.03**2)), "an email"),
    ("5  ALMA [CII]/CO direct gas, subsample [EST]",
     float(np.sqrt(STAT**2 + 0.12**2 + SYS_REF**2 + SYS_CONV**2)), "large ALMA program"),
    ("6  3 + 5 together [EST]",
     float(np.sqrt(STAT**2 + 0.06**2 + 0.05**2 + 0.03**2)), "ALMA + re-analysis"),
    ("7  direct HI 21cm at z~1 (SKA2/ngVLA) [EST]",
     float(np.sqrt(0.05**2 + 0.03**2 + 0.05**2 + 0.03**2)), "~2035+"),
]
CLOSER_OUT = {}
for lab, bd, cost in CLOSERS:
    lz = odds(DB_MEAS, bd)
    lnB = lz["DEC"] - lz["RISE"]
    lzA = odds(cutrow[CUT_FROZEN][4], bd)
    lnBA = lzA["DEC"] - lzA["RISE"]
    sR = abs(DB_MEAS - cutrow[CUT_FROZEN][5]) / bd
    CLOSER_OUT[lab] = dict(band=bd, sig_rise=sR, lnB_achieved=lnB, lnB_design=lnBA,
                           clears_3sigma_achieved=bool(sR >= 3.0),
                           clears_20to1_achieved=bool(lnB >= BAR20),
                           clears_20to1_design=bool(lnBA >= BAR20))
    print(f"  {lab:52} {bd:>7.4f} {sR:>10.2f} {np.exp(min(lnB,30)):>7.1f}:1 "
          f"{np.exp(min(lnBA,30)):>7.1f}:1  {cost}")
print("""
  THE SINGLE CHEAPEST THING THAT CLOSES IT (row 3) -- and why it is the right one:
    Run the IDENTICAL pipeline on a z~0 CONTROL sample MATCHED IN v_c AND IN g_bar/a0, with
    its gas masses taken from the SAME Tacconi+20/NUM PRESCRIPTIONS rather than from measured
    HI, and with the same median estimator and the same 3.14 pivot.  Then
      * the gas-prescription ZERO-POINT (0.20 dex, 55% of today's variance) becomes COMMON-MODE
        in the ratio and only its z-DEPENDENCE survives;
      * the local-reference term (0.16 dex, 35%) is replaced by the control's own stat error;
      * and -- decisively -- the 0.317 dex acceleration TILT of section 3(iv) becomes MEASURABLE
        AT z=0 and therefore DIFFERENTIABLE OUT, instead of being an unmodelled floor.
    Cost: zero new observations.  It needs SPARC/SAMI/MaNGA-class local rotators (already
    public), the published Tacconi+20 and NUM prescriptions (already public), and the Jeanneau
    per-object table (already public and already committed here).
  WHAT IT IS NOT: it does NOT make the answer 'yes' today, and its residual terms (0.07/0.05)
  are ESTIMATES, not measurements.  If the true residual gas z-dependence is 0.12 rather than
  0.07 the design odds fall back under 20:1.  Pre-registered as a FORECAST, not a result.
  AND NOTE ROW 2: the committed likelihood's global highest-leverage item (a Magneticum-style
  drift calibration) is the WRONG LEVER FOR THIS POINT -- section 3(i) showed the drift is a
  0.06 dex effect here at w=0.20 and it HELPS DEC.  Different point, different bottleneck.""")

# ============================================================== 8. THE HONEST BOTTOM LINE
print("\n" + BAR)
print("8. THE HONEST BOTTOM LINE")
print(BAR)
A = ODDS_TABLE["A  committed frozen band"]
D = ODDS_TABLE["D  + the measured (iv) tilt"]
R3 = CLOSER_OUT["3  v- and y-MATCHED z~0 control, SAME gas [EST]"]
R6 = CLOSER_OUT["6  3 + 5 together [EST]"]
print(f"""  CAN THE DEC-vs-RISE CALL BE MADE AT z~0.9-1.1 FROM ALREADY-PUBLISHED DATA?
    NO -- but the reason is NOT the one every previous pass gave, and the margin is much
    smaller than at z=2.  Specifics, all from the real per-object catalogue:

  WHAT IS ACTUALLY IN HAND (better than the compilation assumed)
    * The per-object table is ALREADY PUBLIC AND ALREADY COMMITTED (VizieR J/A+A/709/A120,
      95 rows, in ../jeanneau_refit/).  "Get the per-object table" is NOT the missing item.
    * On the frozen deep cut the real lever is median y = {float(np.median(y_can[SEL])):.3f}, L = {1/(1+2*float(np.median(y_can[SEL]))):.3f} -- FAR better than
      the compilation's assumed L = 0.477.  This sample really is near the a0 regime.
    * The exact per-object DEC-vs-RISE separation is {SEP:.4f} dex on the mass axis
      ({min(_sp):.4f}-{max(_sp):.4f} across both footings x three DESI SNe compilations).

  THE ODDS, PLAINLY
    * committed frozen band {A['band']:.4f} dex: {np.exp(A['lnB']):.2f} : 1 for DEC over RISE, i.e. {A['sig_rise']:.2f} sigma from
      RISE and {A['sig_dec']:.2f} sigma from DEC.  CLEARS NEITHER 3 sigma NOR 20:1.
    * with the section-3(iv) tilt folded in: {np.exp(D['lnB']):.2f} : 1, {D['sig_rise']:.2f} sigma.  Worse, and that is
      the more defensible column.
    * DESIGN capability (data landing exactly on DEC): {np.exp(A['lnB_design']):.2f} : 1.  This measurement, as
      published, simply does not have the resolving power -- independent of where it landed.
    * stat-only would give {np.exp(ODDS_TABLE['E  stat-only [DO-NOT-CLAIM]']['lnB']):.0f} : 1 and {ODDS_TABLE['E  stat-only [DO-NOT-CLAIM]']['sig_rise']:.1f} sigma.  DO-NOT-CLAIM: it treats
      NUM-HI / Tacconi gas as noiseless, and section 3(ii) shows the HI treatment ALONE moves
      the central value by {HI_SPAN:.3f} dex = {HI_SPAN/SEP:.0%} of the separation.

  WHICH BAR IS CLEARED AND WHICH IS NOT -- neither.  And they are nearly the same bar here:
    3 sigma needs a band of {REQ_TIGHTEST:.4f}-{REQ_LOOSEST:.4f} dex; 20:1 (single point) needs {BARS['20:1 Bayes, this single point, DEC vs RISE']:.4f} dex.
    SHORTFALL = {BAND_A/REQ_LOOSEST:.2f}x to {BAND_A/REQ_TIGHTEST:.2f}x in the error ({(BAND_A/REQ_LOOSEST)**2:.1f}x to {(BAND_A/REQ_TIGHTEST)**2:.1f}x in variance).

  THE REASON, AND IT IS NOT "TOO FEW GALAXIES"
    {100*_coh_only**2/BAND_A**2:.0f}% of the variance is COHERENT (gas prescription 0.20 + local reference 0.16 +
    convention 0.06).  N -> infinity floors the band at {_coh_only:.4f} dex, still {_coh_only/REQ_LOOSEST:.2f}x-{_coh_only/REQ_TIGHTEST:.2f}x too wide.
    Worse, section 3(iv) MEASURES an unmodelled acceleration-correlated systematic of
    {MEAS_SWING-PRED_SWING_R:.4f} dex ({(MEAS_SWING-PRED_SWING_R)/SEP:.2f}x the separation) inside the sample at FIXED redshift, and
    section 6 independently finds a z-dependent one that NO law fits.  The sample's own
    internal structure is inconsistent at a level larger than the signal.  That is the wall.

  THE SINGLE CHEAPEST THING THAT WOULD CLOSE IT
    A v- AND y-MATCHED z~0 CONTROL SAMPLE PUT THROUGH THE IDENTICAL PIPELINE WITH THE SAME
    Tacconi+20/NUM GAS PRESCRIPTIONS INSTEAD OF MEASURED HI.  Zero new observations.
    Forecast [ESTIMATE]: band {R3['band']:.4f} dex -> {np.exp(R3['lnB_achieved']):.0f}:1 at the current central value
    ({R3['sig_rise']:.2f} sigma from RISE, so 3 sigma is CLEARED and 20:1 is CLEARED at that central value)
    but only {np.exp(R3['lnB_design']):.1f}:1 on the DESIGN bar.  Adding the authors' per-cluster sigma_mu and a
    direct-gas subsample gets DESIGN to {np.exp(R6['lnB_design']):.1f}:1.  So even the closer is HONESTLY
    "SUBSTANTIAL, not STRONG" by design; only direct gas masses (HI 21cm at z~1, ~2035+) make
    the design odds decisive.

  WHAT THIS DOES *NOT* SAY (both directions)
    * It does NOT detect the framework's distinctive DECLINE.  At z~1 DEC and FLAT differ by
      {100*abs(float(R_dec(1.06,w0,wa))-1):.2f}%; that is unmeasurable by anything, ever.  z~1 can only test DEC-vs-RISE,
      and a not-RISE result is a win for DEC-or-FLAT, with FLAT = standard MOND.
    * It does NOT falsify McCulloch's Hubble-horizon reading.  {A['sig_rise']:.2f} sigma is a LEAN, not a kill.
    * It does NOT inherit the z=2 NO-GO verdict: that verdict rested on needing g_bar < 0.3 a0
      at z~2 where nothing exists.  Here the acceleration regime IS reached ({100*float((y_can<0.3).mean()):.0f}% of the
      95 sit below 0.3 a0) and the shortfall is {BAND_A/REQ_LOOSEST:.1f}x, not the ~6-15x the z=2 work faced.
      The bottleneck moved from ACCELERATION REGIME to GAS-MASS PROVENANCE.
    * a0's VALUE and the HORIZON CHOICE remain POSITS.  nu is Milgrom 1999.  McCulloch credited.
      No TOE.  No 'theory closed'.  No open door is declared shut.""")

# ================================================================= 9. PRE-REGISTRATION
print("\n" + "#" * 100)
print("# PRE-REGISTRATION -- Jeanneau z~1 DEC-vs-RISE readout, frozen with this commit")
print("#" * 100)
CAVEATS = [
    "READOUT: the EXACT nu-inverted zero-point form is used. The deep-MOND BTFR a0=V^4/(G M_bar) "
    "is FORBIDDEN because it equals a0(1+y) ANALYTICALLY -- +0.063 dex on the deep 61 and +0.115 "
    "dex on the full 95, SIGN-LOCKED toward RISE. Using it would manufacture a deficit.",
    "ESTIMATOR: median (PASS tier). GLS-class is FORBIDDEN (prereg a0_line_estimator_bias_v1: "
    f"gls_origin +10.34 pp FAIL). The four combinations span {EST_SPREAD:.3f} dex on the real "
    "subsample and the pre-registered median is NOT the most framework-favourable of them; half "
    "that spread is carried as a systematic in budget C.",
    f"THE BINDING SYSTEMATIC IS GAS PROVENANCE, NOT SAMPLE SIZE: {100*_coh_only**2/BAND_A**2:.0f}% of the variance is "
    f"coherent and the deep cut RAISES the scaling-relation gas fraction to "
    f"{float(np.median(f_gas[SEL])):.2f} of M_bar. The deep cut buys acceleration lever and pays "
    "for it in gas-model exposure.",
    f"INTERNAL INCONSISTENCY (measured, section 3(iv)): at FIXED z the median Delta_b moves "
    f"{MEAS_SWING:.3f} dex across the acceleration-cut sweep while every a0(z) law predicts "
    f"<= {PRED_SWING_R:.3f} dex. The residual {MEAS_SWING-PRED_SWING_R:.3f} dex is "
    f"{(MEAS_SWING-PRED_SWING_R)/SEP:.2f}x the DEC-vs-RISE separation. Budget D carries it; any "
    "claim quoted from budget A rather than D must say so.",
    "SECTION 6 (internal z baseline) IS A CONSISTENCY CHECK, NOT A MEASUREMENT: it rejects DEC, "
    "RISE and FLAT simultaneously (1.6/2.4/1.6 sigma), its z halves are mismatched by ~2.6x in y, "
    "and a slope currency carries MAXIMAL drift exposure w=1.00. It must NEVER be multiplied into "
    "section 4 -- same data, same gas model.",
    "THE DRIFT NUISANCE HELPS DEC HERE. w=0.15-0.20 is therefore the CONSERVATIVE choice and is "
    "used; the w sweep in section 3(i) shows chi2(RISE)-chi2(DEC) rising monotonically with w. "
    "Anyone re-running this at w=1.0 would get a FRIENDLIER answer, not a harsher one.",
    "THE HI PRIOR M_HI ~ U[0, M_mol] IS APPLIED AND IT WEAKENS THE RESULT (central Delta_b "
    f"{float(np.median(_coh)):+.4f} vs the published {DB_MEAS:+.4f}); the HI treatment spans "
    f"{HI_SPAN:.3f} dex overall = {HI_SPAN/SEP:.0%} of the separation. The direction is sign-locked: "
    "less HI => a0 reads HIGH => toward RISE => against the framework.",
    "MAGNIFICATION: d Delta_b/d log mu = -1 EXACTLY (surface density is lensing-invariant, "
    f"v_c is lensing-invariant, R_e is delensed). Only {len(uniq)} clusters, effective N_cl = "
    f"{1/np.sum(w_cl**2):.2f}, so the coherent per-cluster term is reduced only by x{red:.3f}. "
    "The 15%/8% amplitudes are ESTIMATES and MAY double-count the authors' global +/-0.2 dex.",
    "z~1 CANNOT TEST THE FRAMEWORK'S DECLINE. DEC vs FLAT is "
    f"{100*abs(float(R_dec(1.06,w0,wa))-1):.2f}% there. This file tests the MECHANISM fork only "
    "(de Sitter event horizon vs Hubble horizon; Carl vs McCulloch, who is credited).",
    "BOTH FOOTINGS and all three DESI SNe (w0,wa) pairs are carried; the separation spans "
    f"{min(_sp):.4f}-{max(_sp):.4f} dex and the odds {np.exp(min(_lb)):.2f}-{np.exp(max(_lb)):.2f}:1. "
    "The verdict is insensitive to both forks.",
    "THE CLOSER IS A FORECAST. Its residual gas (0.07) and reference (0.05) terms are ESTIMATES. "
    "If the residual gas z-dependence is 0.12 instead of 0.07 the design odds fall back below "
    "20:1. It must be pre-registered and run before any number from it is quoted.",
    "PRE-REGISTERED RISK, STATED IN ADVANCE: if the matched z~0 control moves the central "
    f"Delta_b from {DB_MEAS:+.4f} down to ~0 or negative -- entirely possible, since HI=0 alone "
    f"already gives {db_med_with(_Ms + _Mol):+.4f} -- the DEC-over-RISE lean EVAPORATES and this "
    "point becomes neutral or RISE-leaning. That is the falsification route and it is cheap.",
    "a0's VALUE and the HORIZON CHOICE are POSITS. nu = sqrt(1+1/y) is Milgrom 1999 (PLA 253:273 "
    "Eq.9); the framework's distinctive content is the cH_Lambda/Z coefficient plus the "
    "modified-inertia completion. McCulloch (MiHsC) credited for the Hubble reading. No TOE, no "
    "'theory closed', no closed doors. Exit 0 = ran, NOT a verdict.",
]
for i, c in enumerate(CAVEATS, 1):
    print(f"#  {i}. {c}")
print("#" * 100)

# ================================================================ 10. RESULTS JSON + SELF-CHECK
out = dict(
    source="CDS/VizieR J/A+A/709/A120 (Jeanneau+2026 A&A 709 A120, arXiv:2603.28856), N=95, CC-BY-4.0",
    catalogue_path=os.path.relpath(CAT, HERE),
    laws_at_z={f"z={z}": dict(DEC=float(R_dec(z, w0, wa)), RISE=float(R_rise(z, w0, wa)), FLAT=1.0)
               for z in [0.5, 0.9, 1.06, 1.45]},
    dec_vs_flat_pct_at_z1p06=100 * abs(float(R_dec(1.06, w0, wa)) - 1.0),
    sample=dict(N_full=95, N_deep=NSEL, cut_gbar_over_a0=CUT_FROZEN,
                z_med_deep=float(np.median(zg[SEL])), y_med_deep=float(np.median(y_can[SEL])),
                lever_L_deep=float(1 / (1 + 2 * np.median(y_can[SEL]))),
                fgas_med_deep=float(np.median(f_gas[SEL])),
                frac_below_0p3a0=float((y_can < 0.3).mean()),
                gate_full95_median_db=GATE_FULL),
    measured=dict(delta_b_median=DB_MEAS, delta_b_trimmed=DB_TRIM, delta_b_ivw_FORBIDDEN=DB_IVW,
                  delta_b_mean_FORBIDDEN=DB_MEAN, estimator_spread_dex=EST_SPREAD,
                  stat_dex=STAT),
    predicted=dict(DEC=cutrow[CUT_FROZEN][4], RISE=cutrow[CUT_FROZEN][5], FLAT=0.0,
                   separation_dec_rise_dex=SEP),
    footing_x_desi={k: v for k, v in FOOT_TABLE.items()},
    nuisances=dict(drift_exposure_w=W_EXPOSURE, drift_prior_ladder=PMAX_LADDER,
                   drift_helps_DEC=True,
                   hi_rows={k: v for k, v in HI_ROWS}, hi_span_dex=HI_SPAN,
                   hi_prior_U0Mmol_coherent=float(np.median(_coh)),
                   hi_prior_U0Mmol_perobject=float(np.median(_ind)),
                   n_clusters=int(len(uniq)), eff_n_clusters=float(1 / np.sum(w_cl ** 2)),
                   mu_reduction_factor=red, mu_term_dex=MU_TERM,
                   accel_tilt_measured_dex=MEAS_SWING,
                   accel_tilt_predicted_dex=dict(DEC=PRED_SWING_D, RISE=PRED_SWING_R),
                   accel_tilt_unmodelled_dex=MEAS_SWING - PRED_SWING_R,
                   accel_tilt_over_separation=(MEAS_SWING - PRED_SWING_R) / SEP),
    odds_by_budget=ODDS_TABLE,
    bars_required_band_dex=BARS,
    shortfall_error=dict(vs_loosest=BAND_A / REQ_LOOSEST, vs_tightest=BAND_A / REQ_TIGHTEST),
    coherent_floor_dex=_coh_only,
    internal_z_slope=dict(measured=B_MEAS, sd=B_SD, predicted=B_PRED,
                          baseline_dlog10_1pz=BASE,
                          lnB_dec_over_rise=lnB_slope,
                          status="CONSISTENCY CHECK ONLY -- rejects all three laws; do NOT combine"),
    closers=CLOSER_OUT,
    verdict=dict(
        clears_3sigma=bool(ODDS_TABLE["A  committed frozen band"]["clears_3sigma"]),
        clears_20to1=bool(ODDS_TABLE["A  committed frozen band"]["clears_20to1"]),
        achieved_odds_dec_over_rise=float(np.exp(ODDS_TABLE["A  committed frozen band"]["lnB"])),
        design_odds_dec_over_rise=float(np.exp(ODDS_TABLE["A  committed frozen band"]["lnB_design"])),
        cheapest_closer="v- and y-matched z~0 control through the identical pipeline with the "
                        "SAME Tacconi+20/NUM gas prescriptions instead of measured HI "
                        "(re-analysis only, zero new observations)"),
    posits="a0's VALUE and the HORIZON CHOICE are POSITS; nu = Milgrom 1999 PLA 253:273 Eq.9; "
           "McCulloch (MiHsC) credited for the Hubble-horizon reading; no TOE; no 'theory closed'.",
)
JP = os.path.join(HERE, "jeanneau_z09_dec_vs_rise_2026_results.json")
with open(JP, "w") as f:
    json.dump(out, f, indent=1, default=float)
print(f"\nwrote {JP}")

print("\n" + BAR)
print("SELF-CHECK (frozen invariants -- these are DATA reproductions, not verdicts)")
print(BAR)
assert len(rows) == 95 and NSEL == 61, "committed sample sizes"
assert abs(GATE_FULL - (-0.0366)) < 0.002, "full-95 gate must reproduce the committed -0.037"
assert abs(DB_MEAS - 0.1397) < 0.002, "deep-61 median must reproduce the committed +0.140"
assert abs(float(np.median(y_can[SEL])) - 0.156) < 0.005, "committed median y=0.16"
assert 0.20 < SEP < 0.26, "DEC-vs-RISE separation on the mass axis must be ~0.22-0.25 dex"
assert abs(float(R_dec(1.06, -1.0, 0.0)) - 1.0) < 1e-12, "w->-1 dissolution: DEC becomes FLAT"
assert abs(cutrow[CUT_FROZEN][4]) < 0.02, "DEC vs FLAT at z~1 must be sub-2% (INACCESSIBLE)"
# the exact readout must reduce to the committed lever on differentiation
for _y in [0.05, 0.156, 0.5, 3.0]:
    _a0 = A0_CAN
    _gb = _y * _a0
    _go = np.sqrt(_gb ** 2 + _gb * _a0)
    _h = 1e-6
    _num = float((np.log(g_bar_of(_go, _a0 * (1 + _h))) - np.log(g_bar_of(_go, _a0 * (1 - _h))))
                 / (np.log(1 + _h) - np.log(1 - _h)))
    _lev = -1.0 / (1.0 + 2 * _y)
    assert abs(_num - _lev) < 5e-4, f"exact readout must give the lever -1/(1+2y) at y={_y}"
print(f"  exact readout d log g_bar/d log a0 == -1/(1+2y) at y=0.05/0.156/0.5/3.0   OK")
assert abs(float(np.median(y_can[SEL])) - 0.156) < 0.01
assert ODDS_TABLE["A  committed frozen band"]["clears_3sigma"] is False, \
    "must NOT claim 3 sigma on the committed band"
assert ODDS_TABLE["A  committed frozen band"]["clears_20to1"] is False, \
    "must NOT claim 20:1 on the committed band"
assert ODDS_TABLE["D  + the measured (iv) tilt"]["lnB"] < ODDS_TABLE["A  committed frozen band"]["lnB"], \
    "folding the measured tilt must WEAKEN the result (no hiding it)"
assert float(np.median(_coh)) < DB_MEAS, \
    "the instructed HI prior must WEAKEN the anti-RISE lean (anti-framework rail)"
assert DB_IVW < DB_MEAS or DB_MEAN > DB_MEAS, \
    "the estimator freeze must not be the framework's most favourable choice"
_g0 = ((DB_MEAS - pred_db("RISE", A0_CAN, w0, wa, 0.0, 0.0)) ** 2
       - (DB_MEAS - pred_db("DEC", A0_CAN, w0, wa, 0.0, 0.0)) ** 2)
_g1 = ((DB_MEAS - pred_db("RISE", A0_CAN, w0, wa, 1.22, 1.0)) ** 2
       - (DB_MEAS - pred_db("DEC", A0_CAN, w0, wa, 1.22, 1.0)) ** 2)
assert _g1 > _g0, "the drift must HELP DEC-over-RISE here (so low w is the conservative choice)"
assert MEAS_SWING > 3 * PRED_SWING_R, \
    "the measured acceleration tilt must exceed the predicted dilution swing (the wall)"
assert (MEAS_SWING - PRED_SWING_R) > SEP, \
    "the unmodelled tilt must exceed the whole DEC-vs-RISE separation (the reason for the NO)"
assert ZSWING < 0.10, "the acceleration-cut sweep must be at essentially FIXED redshift"
assert not (lnB_slope > BAR20), "the internal-slope cross-check must not be claimed decisive"
print(f"  N=95/61, gate {GATE_FULL:+.4f}, Delta_b {DB_MEAS:+.4f}, y_med "
      f"{float(np.median(y_can[SEL])):.3f}, SEP {SEP:.4f} dex   OK")
print(f"  achieved {np.exp(ODDS_TABLE['A  committed frozen band']['lnB']):.2f}:1, design "
      f"{np.exp(ODDS_TABLE['A  committed frozen band']['lnB_design']):.2f}:1, "
      f"3s={ODDS_TABLE['A  committed frozen band']['clears_3sigma']}, "
      f"20:1={ODDS_TABLE['A  committed frozen band']['clears_20to1']}   OK")
print(f"  drift helps DEC (gap {_g0/BAND_A**2:+.3f} -> {_g1/BAND_A**2:+.3f}); HI prior weakens "
      f"({float(np.median(_coh)):+.4f} < {DB_MEAS:+.4f})   OK")
print(f"  measured tilt {MEAS_SWING:.4f} dex >> predicted {PRED_SWING_R:.4f} dex at fixed z "
      f"(z swing {ZSWING:.4f})   OK")
print("\nEXIT 0 (ran; not a verdict).")
