#!/usr/bin/env python3
"""
a0z_drift_nuisance_dilution_2026.py
===================================================================================================
THE LCDM-DEGENERATE APPARENT-a0 DRIFT NUISANCE + THE ACCELERATION-DILUTION WEIGHTS,
and the resulting THREE-MODEL LIKELIHOOD COMPARISON on the 11 real high-z a0(z) constraints.

Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework (its OWN kernel nu=sqrt(1+1/y),
a0 = c H_Lambda / Z, Z = sqrt(32pi/3)).  Wellhead credit: nu = Milgrom 1999 PLA 253:273 Eq.9;
McCulloch (MiHsC / quantised inertia) credited for the Hubble-horizon rising reading.

BUILDS ON (does NOT modify) the committed parents:
  prep_2026/a0z_crossscale/highz_a0_fork_confront_2026.py       (the 11 cited constraints)
  prep_2026/a0z_crossscale/highz_a0z_fork_placement_2026.py     (fork placement machinery)
  prep_2026/a0z_crossscale/desitter_unruh_horizon_fork_2026.py  (the two horizon branches)
  prep_2026/a0z_crossscale/a0z_prediction_band_2026.py          (frozen footing-independent band)
  prep_2026/highz_tfr_fork/data_ledger.csv                      (gbar/a0 + dilution per study)
  prep_2026/a0z_crossscale/highz_systematics_floor.py           (the deep-MOND amplifications)
  prep_2026/a0z_crossscale/bigwheel_update.py                   (Big Wheel is y~0.7-1.3, NOT deep-MOND)

THE THREE ZERO-FREE-PARAMETER MODELS (a0(z)/a0(0)):
  M-DEC   sqrt(rho_DE(z)/rho_DE0), CPL at DESI DR2 central   [framework de Sitter / future horizon]
  M-RISE  E(z) = H(z)/H0                                     [McCulloch Hubble horizon]
  M-FLAT  1                                                  [standard MOND == framework w->-1 limit]
All three have ZERO free parameters -> a clean likelihood ratio, no Occam penalty.

WHAT THIS FILE ADDS (its role):
 (a) A QUANTITATIVE, TWICE-CALIBRATED apparent-a0 drift nuisance A_drift(z) = (1+z)^p with a
     defensible, explicitly anti-tuned prior on p.
 (b) An EXPOSURE weight w_i in [0,1] per constraint, built from a driver decomposition, not vibes.
 (c) An ACCELERATION-DILUTION lever L_i per constraint, DERIVED from the framework's own kernel
     and VALIDATED against the committed ledger's dilution column.
 (d) The joint likelihood, marginalized over p, and the Bayes factors at face value vs marginalized.

HARD CALIBRATION (a manufactured declining win and a manufactured rising deficit are penalized
EQUALLY -- both are failure):
  * p is calibrated to Magneticum/Mayer+2023 (arXiv:2206.04333) INDEPENDENTLY of the data, and
    CROSS-CHECKED against MSA-3D's own internal g_obs-selection decomposition. The fiducial is
    the SMALLER (more conservative, less MUSE-absorbing) of the two calibrations.
  * The p prior is CAPPED at the largest RAW apparent slope ever measured (+2.13, MSA-3D raw), so
    the nuisance CANNOT be inflated until MUSE vanishes. That cap is the anti-tuning guard.
  * p is a SINGLE SHARED nuisance -- it cannot be re-tuned per point to rescue any model.
  * MUSE-DARK III's face-value rise is treated as a REAL measurement: the p=0 odds are printed in
    full, at their true (overwhelming) strength, and the verdict's MOVEMENT is the headline.
  * The sign-unknown gas/M-L calibration systematics are NOT added as a second nuisance because the
    quoted errors are already systematics-inclusive -- double counting would be a manufactured win.
  * The RATIO a0(z)/a0(0) is footing-independent (sympy-proved in the parent); both footings printed.
  * No TOE. No "theory closed". Exit 0 = ran, NOT a verdict.
===================================================================================================
"""
import os, json
import numpy as np
import sympy as sp

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LEDGER = os.path.join(REPO, "prep_2026", "highz_tfr_fork", "data_ledger.csv")
DEX = np.log(10.0)
bar = "=" * 100

# ---------------------------------------------------------------------------------------
# COSMOLOGY / BRANCHES  (identical machinery + constants to the committed parents)
# ---------------------------------------------------------------------------------------
OM, OL = 0.315, 0.685
W0, WA = -0.838, -0.62                     # DESI DR2 w0waCDM + Pantheon+ central (the fork head)
Z_CONST = np.sqrt(32 * np.pi / 3)
A0_CAN, A0_ALT = 9.355e-11, 1.131e-10      # canonical cH_Lambda/Z ; alt cH0/Z

def rho_de_ratio(z, w0=W0, wa=WA):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def R_DEC(z, w0=W0, wa=WA):   return np.sqrt(rho_de_ratio(z, w0, wa))
def R_RISE(z, w0=W0, wa=WA):  return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3
                                             + OL * rho_de_ratio(z, w0, wa))
def R_FLAT(z, w0=W0, wa=WA):  return np.ones_like(np.asarray(z, float))

MODELS = {"M-DEC": R_DEC, "M-RISE": R_RISE, "M-FLAT": R_FLAT}

def loglog_slope(fn, zlo, zhi, n=400, **kw):
    z = np.linspace(zlo, zhi, n)
    return float(np.polyfit(np.log10(1 + z), np.log10(fn(z, **kw)), 1)[0])

print(bar)
print("APPARENT-a0 DRIFT NUISANCE + ACCELERATION-DILUTION WEIGHTS -> 3-MODEL LIKELIHOOD (2026-07-25)")
print(bar)
print(f"  a0 = cH_Lambda/Z, Z={Z_CONST:.5f}. canonical a0(0)={A0_CAN:.3e} | alt a0(0)={A0_ALT:.3e} m/s^2.")
print("  The RATIO a0(z)/a0(0) is FOOTING-INDEPENDENT (sympy-proved in a0z_prediction_band_2026.py):")
print("  Z, a0(0), c, H all cancel -> ONE ratio band, so every number below holds on BOTH footings.")
print(f"  branch ratios:  z=1  DEC={R_DEC(1.):.3f} RISE={R_RISE(1.):.3f} FLAT=1.000  |  "
      f"z=2  DEC={R_DEC(2.):.3f} RISE={R_RISE(2.):.3f}  |  z=3  DEC={R_DEC(3.):.3f} RISE={R_RISE(3.):.3f}")

# =======================================================================================
# S0 -- THE ACCELERATION-DILUTION LEVER, DERIVED FROM THE FRAMEWORK'S OWN KERNEL (sympy)
#       NOT from McGaugh's nu. The framework's exact a0-line identity is
#           g_obs^2 - g_bar^2 = a0 * g_bar        [ <=> nu(y) = sqrt(1+1/y), y = g_bar/a0 ]
#       so the a0-dependent EXCESS is  g_obs^2 - g_bar^2 = g_bar^2 / y : at g_bar >> a0 the
#       excess is only ~1/y of g_bar^2 -- that is the dilution, quantified below.
# =======================================================================================
print("\n" + bar)
print("S0 -- ACCELERATION-DILUTION LEVERS from the framework's OWN kernel (sympy, exact)")
print(bar)
a0s, ys, Vs, Rs, Ms, Gs, gbs = sp.symbols("a0 y V R M G g_bar", positive=True)
gobs_s = sp.sqrt(gbs**2 + gbs * a0s)                  # the framework's exact a0-line
# (i) fractional a0-dependent excess of g_obs^2 over g_bar^2, in terms of y = g_bar/a0
excess = sp.simplify(((gobs_s**2 - gbs**2) / gbs**2).subs(gbs, a0s*ys))
# (ii) velocity/RAR currency: how much does log g_obs move per unit log a0 at FIXED g_bar?
lev_g = sp.simplify((sp.diff(sp.log(gobs_s), a0s) * a0s).subs(gbs, a0s*ys))
lev_g_deepmond = sp.limit(lev_g, ys, 0)
L_g = sp.simplify(lev_g / lev_g_deepmond)
# (iii) MASS-axis (bTFR/sTFR zero-point) currency: at FIXED V and R, how much does log M
#       move per unit log a0?  V^4 = R^2 g_bar (g_bar + a0), g_bar = G M / R^2
V4 = Rs**2 * (Gs*Ms/Rs**2) * (Gs*Ms/Rs**2 + a0s)
dM_da0 = sp.simplify(-sp.diff(V4, a0s) / sp.diff(V4, Ms))          # implicit d M / d a0 at fixed V,R
lev_M = sp.simplify((dM_da0 * a0s / Ms).subs(Ms, a0s*ys*Rs**2/Gs))  # -> d log M / d log a0
L_M = sp.simplify(-lev_M / sp.limit(-lev_M, ys, 0))
print(f"  (g_obs^2 - g_bar^2)/g_bar^2                       = {excess}          <- the 1/y excess")
print(f"  d log g_obs / d log a0                            = {sp.simplify(lev_g)}")
print(f"     deep-MOND limit (y->0)                         = {lev_g_deepmond}")
print(f"     RAR/velocity-currency lever  L_g(y)            = {sp.simplify(L_g)}   = 1/(1+y)")
print(f"  d log M_bar / d log a0 at fixed (V,R)             = {lev_M}")
print(f"     mass-axis (bTFR zero-point) lever  L_M(y)      = {L_M}   = 1/(1+2y) = x/(2+x), x=a0/g_bar")
assert sp.simplify(L_M - 1/(1+2*ys)) == 0, "mass-axis lever must be 1/(1+2y)"
assert sp.simplify(L_g - 1/(1+ys)) == 0,   "RAR lever must be 1/(1+y)"
assert sp.simplify(excess - 1/ys) == 0,    "excess must be exactly 1/y"

def L_mass(y):  return 1.0 / (1.0 + 2.0*np.asarray(y, float))     # bTFR/sTFR mass-axis lever
def L_rar(y):   return 1.0 / (1.0 + np.asarray(y, float))          # RAR / log-g_obs lever

print("\n  CONSEQUENCE (the whole point):  a model's PREDICTED signal in a mass-axis zero-point is")
print("  Delta_b_pred = -L_M(y) * log10(a0(z)/a0(0)).  The point's a0 INFORMATION therefore scales as")
print("  L_M^2 at fixed measurement error -> a g_bar>>a0 sample is quadratically de-weighted.")
print("  Equivalently (inverse view, matching highz_systematics_floor.py's committed amplifications")
print("  d lnA0/d lnV = 4(y+1), d lnA0/d lnG_bar = -(2y+1)): reading a0 OFF such a sample amplifies")
print("  every coherent error by 1/L -- the SAME factor, seen from the other side.")

# ---- validate L_M against the COMMITTED ledger's own dilution column -------------------
print("\n  VALIDATION vs the committed ledger prep_2026/highz_tfr_fork/data_ledger.csv:")
import csv as _csv
led, nchk, worst = [], 0, 0.0
with open(LEDGER) as f:
    for row in _csv.DictReader(f):
        try:
            y_l = float(row["gbar_over_a0_typ"]); d_l = float(row["dilution_typ"])
        except (ValueError, KeyError, TypeError):
            continue
        mine = float(L_mass(y_l)); worst = max(worst, abs(mine - d_l)); nchk += 1
        led.append((row["study"], row["z_eff"], row["relation"], y_l, d_l, mine))
for st, ze, rel, y_l, d_l, mine in led[:6]:
    print(f"    {st:16} z={ze:>4} {rel:14} y={y_l:>4.1f}  ledger dilution={d_l:.2f}  1/(1+2y)={mine:.3f}")
print(f"    ... {nchk} ledger rows checked; MAX |mine - ledger| = {worst:.3f}")
assert worst <= 0.06, f"my lever disagrees with the committed ledger by {worst:.3f} -- reconcile first"
print("    => the lever 1/(1+2y) REPRODUCES the committed ledger convention (max dev "
      f"{worst:.3f}, from the ledger's 2-decimal rounding). No new convention introduced.")

# =======================================================================================
# S1 -- (a) THE LCDM-DEGENERATE APPARENT-a0 DRIFT NUISANCE  A_drift(z) = (1+z)^p
#       TWO INDEPENDENT CALIBRATIONS, one from a simulation and one from the data itself.
# =======================================================================================
print("\n" + bar)
print("S1 -- (a) THE APPARENT-a0 DRIFT NUISANCE  A_drift(z) = (1+z)^p   [calibration + prior]")
print(bar)
print("""  WHAT IT MODELS: an apparent (NOT fundamental) rise of the FITTED a0 with redshift that a pure
  LCDM universe with NO fundamental a0 already produces, driven by g_obs-selection, beam smearing,
  pressure support and baryonic structural evolution. It is a NUISANCE EVERY model inherits: the
  observable is  a0_apparent(z)/a0(0) = R_model(z) * A_drift(z)^w_i,  with w_i the point's exposure.

  PARAMETRIC FORM: A_drift(z) = (1+z)^p.  Chosen because p IS the drift's log-log slope,
    p = d log10 A_drift / d log10(1+z),
  i.e. p lives in EXACTLY the currency the two direct a0(z) probes report (MSA-3D reports a
  d log10 a0 / d log10(1+z) slope; MSA-3D's own selection decomposition is quoted in that same
  currency). No conversion, no shape assumption smuggled in beyond a power law.""")

# ---- CALIBRATION 1: Magneticum / Mayer et al. 2023 (arXiv:2206.04333, MNRAS) --------------
MAG_FACTOR, MAG_Z = 3.0, 2.3          # apparent-a0 rise ~x3 by z=2.3 in pure LCDM, NO fundamental a0
p_mag = float(np.log(MAG_FACTOR) / np.log(1.0 + MAG_Z))
# ---- CALIBRATION 2: MSA-3D's OWN internal g_obs-selection decomposition -------------------
# Espejo Salcedo+2026 (arXiv:2606.27853) + committed msa3d_a0z_selection_decomposition.py:
#   RAW slope +2.13 = g_obs-SELECTION +1.13  +  h(f_DM) +1.00 ; genuine residual +0.91.
# The +1.13 selection term IS an apparent-drift slope measured ON REAL DATA, same units as p.
p_msa3d_sel = 1.13
P_RAW_CAP = 2.13                      # largest RAW apparent slope ever measured -> the prior cap
print(f"\n  CALIBRATION 1 (SIMULATION, data-independent): Magneticum/Mayer+2023 -- apparent a0 rises")
print(f"    x{MAG_FACTOR:.0f} by z={MAG_Z} in pure LCDM with NO fundamental a0.")
print(f"    (1+{MAG_Z})^p = {MAG_FACTOR:.0f}  =>  p_mag = ln{MAG_FACTOR:.0f}/ln{1+MAG_Z:.1f} = {p_mag:.3f}")
print(f"  CALIBRATION 2 (DATA-INTERNAL, independent of the sim): MSA-3D's own decomposition of its")
print(f"    RAW +2.13 slope isolates a g_obs-SELECTION component  p_sel = +{p_msa3d_sel:.2f} in the same units.")
print(f"  => two INDEPENDENT routes give p = {p_mag:.2f} (sim) and {p_msa3d_sel:.2f} (data): agreement to "
      f"{100*abs(p_msa3d_sel-p_mag)/p_mag:.0f}%.")
print(f"     This agreement is NOT tuned -- neither number was fitted to any a0(z) model.")

P_CAL = p_mag                          # FIDUCIAL = the SMALLER (more conservative) of the two
print(f"\n  FIDUCIAL CENTRAL: p_cal = {P_CAL:.3f} -- deliberately the SMALLER of the two calibrations.")
print(f"    Using the data-internal {p_msa3d_sel:.2f} instead would ABSORB MORE of MUSE-DARK III's rise,")
print(f"    i.e. it would be MORE favourable to the declining branch. Taking the smaller value is the")
print(f"    anti-tuning choice; the larger one is carried in S6 as a sensitivity, not as the baseline.")

# ---- cross-check against the committed linear-in-z fiducial (slope_mag = 0.80) ------------
zz_mu = np.linspace(0.33, 1.44, 400)                       # MUSE-DARK III z-support
slope_lin_mine = float(np.polyfit(zz_mu, (1+zz_mu)**P_CAL, 1)[0])
SLOPE_MAG_COMMITTED = 0.80
print(f"\n  CROSS-CHECK vs the committed fiducial: over MUSE-DARK III's range z=0.33-1.44, (1+z)^{P_CAL:.2f}")
print(f"    has a LINEAR-in-z slope of {slope_lin_mine:+.2f}/z; the committed scripts carry {SLOPE_MAG_COMMITTED:+.2f}/z")
print(f"    (highz_a0_fork_confront_2026.py SLOPE_MAG). Mine is {100*(slope_lin_mine/SLOPE_MAG_COMMITTED-1):+.0f}% LARGER.")
print(f"    FLAGGED, not hidden: a larger drift is MORE forgiving to the declining branch. It comes from")
print(f"    an independent power-law fit to the SAME x3-at-z=2.3 anchor, not from tuning. The committed")
print(f"    0.80 is carried in S6 as the conservative sensitivity variant.")

# ---- where does MUSE-DARK III's own measured slope sit relative to the drift? -------------
MU_A1, MU_A1_STAT = 1.59, 0.105        # Ciocan+2026 a0(z)=a0(0)+a1 z [x1e-10], LCDM-mass route
p_muse = float(np.polyfit(np.log10(1+zz_mu), np.log10(1.0 + MU_A1*zz_mu), 1)[0])
JAC_MU = p_muse / MU_A1                # a1 -> log-log slope Jacobian over the range (near-linear)
print(f"\n  MUSE-DARK III IN THE SAME CURRENCY: a0(z)=1+{MU_A1:.2f}z over z=0.33-1.44 has log-log slope")
print(f"    p_MUSE = {p_muse:+.3f} +/- {MU_A1_STAT*JAC_MU:.3f} (stat).  Compare the drift calibrations:")
print(f"    p_mag={p_mag:.2f} (sim) and p_sel={p_msa3d_sel:.2f} (MSA-3D data) -- i.e. the ENTIRE measured MUSE")
print(f"    slope is only {p_muse-p_mag:+.2f} above the simulated pure-LCDM drift and {p_muse-p_msa3d_sel:+.2f} above the")
print(f"    data-measured selection drift. THAT is the quantitative meaning of 'LCDM-degenerate'.")

# ---- THE PRIOR ON p ----------------------------------------------------------------------
SIG_TRANSFER = 0.50                   # sample-to-sample selection-strength transfer (fractional)
SIG_CALSPREAD = abs(p_msa3d_sel - p_mag)   # sim-vs-data calibration spread
SIG_P = float(np.hypot(SIG_CALSPREAD, SIG_TRANSFER * P_CAL))
P_LO, P_HI = -0.30, P_RAW_CAP
print(f"\n  THE PRIOR:  p ~ Normal({P_CAL:.2f}, {SIG_P:.2f}) TRUNCATED to [{P_LO:+.2f}, {P_HI:+.2f}].  Justification, term by term:")
print(f"    CENTRE {P_CAL:.2f}   : Magneticum's x3-at-z=2.3, the smaller of two independent calibrations.")
print(f"    WIDTH  {SIG_P:.2f}   : sqrt( calibration spread {SIG_CALSPREAD:.2f}^2  +  transfer "
      f"{SIG_TRANSFER:.0%} x {P_CAL:.2f} = {SIG_TRANSFER*P_CAL:.2f}^2 ).")
print(f"                 The transfer term dominates and is the honest one: the drift amplitude scales")
print(f"                 with how hard a given sample's selection bites, which differs sample to sample")
print(f"                 by tens of percent. A width much SMALLER than this would be overconfident.")
print(f"    LOWER  {P_LO:+.2f}  : a modestly NEGATIVE drift is physically real and must be allowed --")
print(f"                 UNCORRECTED beam smearing and pressure support both SUPPRESS the outer velocity")
print(f"                 and therefore the apparent a0. Magneticum's NET is positive, so the negative")
print(f"                 tail is short, but banning it outright would be a one-sided prior.")
print(f"    UPPER  {P_HI:+.2f}  : *** THE ANTI-TUNING GUARD ***  capped at the LARGEST RAW apparent slope")
print(f"                 ever measured (MSA-3D raw +2.13). Nothing in hand -- sim or data -- supports a")
print(f"                 steeper apparent drift, so the nuisance is structurally UNABLE to be inflated")
print(f"                 until MUSE-DARK III vanishes. Note p_MUSE={p_muse:.2f} < cap, so the cap does NOT")
print(f"                 by itself protect the declining branch; it only forbids running away past 2.13.")
print(f"    NOT centred on 0 and NOT centred on p_MUSE: centring on 0 would assert the Magneticum result")
print(f"    is inapplicable (a manufactured rising deficit); centring on p_MUSE would assert the whole")
print(f"    measured rise is artefact (a manufactured declining win). Both are refused.")

# prior on a grid (used by the marginalization)
PGRID = np.linspace(P_LO, P_HI, 1201)
PRIOR = np.exp(-0.5*((PGRID - P_CAL)/SIG_P)**2)
PRIOR /= np.trapz(PRIOR, PGRID)
q = np.cumsum(PRIOR)*np.gradient(PGRID)[0]; q /= q[-1]
p16, p50, p84 = np.interp([0.16, 0.5, 0.84], q, PGRID)
print(f"\n  truncated-prior summary: median p={p50:.2f}, 68% [{p16:.2f},{p84:.2f}]; "
      f"P(p<0)={float(np.trapz(PRIOR*(PGRID<0),PGRID)):.3f}, "
      f"P(p>p_MUSE)={float(np.trapz(PRIOR*(PGRID>p_muse),PGRID)):.3f}")
print(f"  => the prior puts {float(np.trapz(PRIOR*(PGRID>p_muse),PGRID)):.0%} of its mass ABOVE MUSE's own measured slope:")
print(f"     the drift CAN absorb MUSE without any tuning. That is a PROPERTY OF THE CALIBRATION, and it")
print(f"     is exactly why the face-value odds must be reported alongside the marginalized ones.")

# =======================================================================================
# S2 -- (b) THE EXPOSURE TABLE  w_i  =  f_sel * s_i  +  f_beam * b_i
#       Built from a DRIVER DECOMPOSITION so each number is traceable to the observable's
#       CONSTRUCTION, not to a judgement call about which answer we want.
#
#   DRIVER SHARES.  Magneticum's TOTAL apparent drift (p=0.92) is statistically indistinguishable
#   from MSA-3D's g_obs-SELECTION component ALONE (p=1.13) -> selection dominates the drift.
#   Fiducial shares f_sel=0.82 / f_beam=0.18 (swept in S6).  The remaining physical driver,
#   gas/M-L calibration evolution, is deliberately EXCLUDED from w: it is SIGN-UNKNOWN and is
#   ALREADY inside every quoted systematics-inclusive error bar (Jeanneau's +/-0.27 explicitly
#   contains the Tacconi+20/NUM gas model, Ubler's +/-0.35 the gas scaling, Amvrosiadis's +/-0.30
#   the alpha_CO).  Folding it into a POSITIVE-centred coherent drift as well would double-count
#   it in the direction that flatters the declining branch -- refused.
#
#   s_i = exposure to g_obs / rotation-detectability SELECTION      (the dominant driver)
#   b_i = exposure to beam-smearing + pressure-support RESIDUAL     (the sub-dominant driver)
# =======================================================================================
F_SEL, F_BEAM = 0.82, 0.18

# --------------------------------------------------------------------------------------
# THE 11 REAL CITED CONSTRAINTS (numbers taken verbatim from the committed compilation
# highz_a0_fork_confront_2026.py / highz_a0z_fork_placement_2026.py / data_ledger.csv /
# galaxy_a0z.py -- NOTHING invented).  Three currencies:
#   "slope" : measured d log10(a0)/d log10(1+z)          -> compared to model log-log slope + w*p
#   "db"    : bTFR/sTFR MASS-AXIS zero-point offset, dex -> predicted -L_M*(log10 R + w*p*log10(1+z))
#   "lr"    : directly-estimated log10 a0(z)/a0(0), dex  -> predicted  log10 R + w*p*log10(1+z)
# --------------------------------------------------------------------------------------
DATA = [
 dict(tag="MSA-3D", cite="Espejo Salcedo+26 arXiv:2606.27853", z=1.10, zlo=0.58, zhi=1.68,
      cur="slope", obs=+0.91, sig=0.79, y=1.1, s=0.20, b=0.50, N=23,
      why_s="JWST/NIRSpec, non-lensed, rotation-selected -> raw exposure MAXIMAL; but the value used "
            "(+0.91) is ALREADY the g_obs-selection-DECONVOLVED residual (raw +2.13 = selection +1.13 "
            "+ h(f_DM) +1.00), so only the RESIDUAL uncertainty of that correction is exposed -> s=0.20. "
            "Using the RAW +2.13 instead demands s=1.00 (carried in S6).",
      why_b="NIRSpec IFU PSF + 3D modelling: better than seeing-limited MUSE/KMOS, worse than ALMA.",
      why_L="fitted-a0 currency: the a0-line is exact at any y, so L=1 in the MAPPING; the dilution "
            "instead AMPLIFIES coherent errors by 2(1+y) -- which is the quantitative reason s,b are "
            "exposures at all. y~1.1 (its own g_bar/a0 span 0.2-6, log-mid)."),
 dict(tag="MUSE-DARK III", cite="Ciocan+26 A&A 709 L16 arXiv:2604.22613", z=0.90, zlo=0.33, zhi=1.44,
      cur="slope", obs=+p_muse, sig=MU_A1_STAT*JAC_MU, y=1.3, s=1.00, b=1.00, N=79,
      why_s="*** MAXIMAL ***  non-lensed, flux+resolved-rotation-selected MUSE HUDF SFGs, DIRECT RAR "
            "fit, NO selection deconvolution published. This is EXACTLY the construction Magneticum "
            "mimics (fit a0 to a g_obs-selected SFG sample at increasing z) -> s=1.00 by definition of "
            "the calibration. Its a0 is read at y~1.3, where a coherent d ln g_obs is amplified into "
            "d ln a0 by 2(1+y)=4.6x -- the largest amplification of any DIRECT point here.",
      why_b="MUSE seeing-limited (~0.6in ~ 5 kpc at z=1) on compact SFGs, warm ionized Halpha/OII "
            "tracer with the steepest sigma_0(z) rise -> beam + pressure exposure MAXIMAL.",
      why_L="fitted-a0 currency -> L=1 in the mapping (see MSA-3D). y~1.3 is an ESTIMATE (its M*>10^8.8 "
            "non-lensed sample sits between Jeanneau's lensed y=0.5 and KMOS3D's y=1.7); swept in S6."),
 dict(tag="MUSE-DARK II (Jeanneau)", cite="Jeanneau+26 A&A arXiv:2603.28856", z=0.90, zlo=0.56, zhi=1.37,
      cur="db", obs=0.00, sig=0.27, y=0.5, s=0.20, b=0.25, N=95,
      why_s="*** MINIMAL ***  95 LENSED galaxies: magnification (mu~2-10) pushes the detection limit "
            "1-2.5 mag fainter, so the sample reaches M*=10^8.1-10.3 -- the LOWEST-mass, LOWEST-g_obs "
            "sample in hand. Lensing is precisely what DEFEATS a g_obs-selection drift: the selection "
            "boundary is moved, not tracked. Residual s=0.20 for the magnification-dependent residual.",
      why_b="lensed -> effective resolution boosted by ~sqrt(mu); 3D GalPaK3D + lensing forward model; "
            "Dalcanton-Stilp pressure correction APPLIED -> beam/pressure exposure near-minimal.",
      why_L="mass-axis bTFR zero-point -> L_M=1/(1+2y). y=0.5 (ledger) = the only NEAR-a0 bTFR in hand, "
            "hence the LARGEST lever of any zero-point point (L=0.50)."),
 dict(tag="Ubler z0.9", cite="Ubler+17 ApJ 842,121 arXiv:1703.04321", z=0.90, zlo=0.70, zhi=1.10,
      cur="db", obs=-0.44, sig=0.35, y=1.7, s=1.00, b=0.60, N=65,
      why_s="*** MAXIMAL ***  KMOS3D, non-lensed, with an EXPLICIT rotation cut v_rot/sigma_0 > sqrt(4.4) "
            "(ledger column) -- a literal g_obs-like selection, applied at z but NOT at the local "
            "reference, and never deconvolved. This is the drift's textbook entry point.",
      why_b="Halpha warm tracer, beam-corrected models but seeing-limited; sigma_0-correction applied "
            "(2 sigma_0^2 r/Rd) so the RESIDUAL not the raw term is exposed.",
      why_L="mass-axis bTFR ZP; y=1.7 (ledger) -> L_M=0.227: only 23% of the deep-MOND lever."),
 dict(tag="Ubler z2.3", cite="Ubler+17 ApJ 842,121 arXiv:1703.04321", z=2.30, zlo=1.90, zhi=2.70,
      cur="db", obs=-0.27, sig=0.35, y=2.3, s=1.00, b=0.70, N=46,
      why_s="same construction as its z=0.9 row -> s=1.00.",
      why_b="same tracer, but sigma_0(z) is larger and the angular size smaller at z=2.3, so the "
            "beam+pressure residual is worse -> b=0.70 > 0.60.",
      why_L="mass-axis bTFR ZP; y=2.3 (ledger) -> L_M=0.179."),
 dict(tag="Amvrosiadis z2.4", cite="Amvrosiadis+25 MNRAS arXiv:2312.08959", z=2.40, zlo=1.20, zhi=4.70,
      cur="db", obs=-0.26, sig=0.30, y=6.4, s=0.80, b=0.15, N=12,
      why_s="ALESS DSFGs are submm-flux-selected extreme dusty starbursts, N=12, 'extreme high-mass' "
            "(ledger). An extreme-luminosity selection at fixed z drives g_bar and g_obs up just as a "
            "g_obs cut does -> s=0.80, high but below the explicit rotation cuts.",
      why_b="ALMA CO, high-resolution VISIBILITY-space dynamical fit, COLD tracer (sigma_0 ~0.6x warm) "
            "-> beam/pressure exposure the LOWEST in the compilation.",
      why_L="mass-axis bTFR ZP; y=6.4 (ledger) -> L_M=0.0725: the most acceleration-DILUTED point here."),
 dict(tag="Tiley z1.0 matched", cite="Tiley+19 MNRAS 482,2166 arXiv:1810.07202", z=1.00, zlo=0.60, zhi=1.00,
      cur="db", obs=-0.05, sig=0.10, y=0.8, s=0.15, b=0.20, N=250,
      why_s="*** MINIMAL BY CONSTRUCTION ***  the paper's whole method is to DEGRADE local SAMI data to "
            "KROSS quality and re-measure with an IDENTICAL pipeline. That EMPIRICALLY removes the "
            "resolution/selection-driven apparent evolution (it moves the local relation by -0.50+/-0.10 "
            "mag). It is a drift-CONTROLLED measurement -> s=0.15 residual (the matching's imperfection).",
      why_b="matched + beam-corrected v2.2 -> low; no pressure correction applied, hence not 0.",
      why_L="mass-axis (STELLAR TFR, not the clean bTFR); y=0.8 (ledger) -> L_M=0.385."),
 dict(tag="Big Wheel z3.25", cite="arXiv:2409.17956 + 2605.04144 (ALMA dyn. model)", z=3.25, zlo=3.20, zhi=3.30,
      cur="lr", obs=np.log10(1.15), sig=0.22, y=0.95, s=0.35, b=0.20, N=1,
      why_s="N=1, found because it is an extreme giant disc: a SIZE/luminosity selection, not a g_obs "
            "cut. At fixed mass a larger size LOWERS g_bar (pushing apparent a0 the other way), while "
            "'discovered because exceptional' pushes V up -> partial, s=0.35. Its dominant systematic is "
            "NOT the drift but the 0.37-dex M* ambiguity the discovery paper itself flags.",
      why_b="ALMA high-resolution dynamical model, cold tracer -> low.",
      why_L="directly-estimated a0 via the a0-line -> L=1 in the mapping. *** HONESTY FLAG *** the "
            "committed bigwheel_update.py shows this object is y=0.68 (dynamical M*) to 1.27 (SED M*) -- "
            "TRANSITIONAL, NOT deep-MOND as the compilation's label suggests. At y~0.95 its mass-axis "
            "lever would be only 0.34 and its a0 error is amplified by (1+2y)=2.9x, so the quoted "
            "+/-0.22 dex is OPTIMISTIC: the committed MC spans ratio 1.3-3.1 across the M* ambiguity "
            "(~+/-0.40 dex). This CUTS AGAINST the framework (it weakens the strongest FLAT-leaning "
            "clean point); the +/-0.40 dex variant is run in S6."),
 dict(tag="Di Teodoro z1.0", cite="Di Teodoro+16 A&A 594 A77", z=1.00, zlo=0.80, zhi=1.20,
      cur="db", obs=0.00, sig=0.15, y=1.0, s=0.70, b=0.25, N=18,
      why_s="non-lensed heterogeneous z~1 Halpha compilation with a rotation-dominance requirement and "
            "no selection deconvolution -> substantially exposed, s=0.70; below Ubler because no "
            "explicit v/sigma threshold is imposed as a sample cut.",
      why_b="3D TILTED-RING modelling (3DBAROLO, the method built specifically to beat beam smearing) "
            "-> beam exposure low, b=0.25.",
      why_L="mass-axis TFR ZP; y~1.0 (ledger analogue for its mass range) -> L_M=0.333."),
]
# The remaining 2 of the 11 are ONE-SIDED BOUNDS with no quotable central+sigma; they are carried
# as CONTEXT and as an S6 sensitivity, never in the baseline likelihood (see S6/S7).
BOUNDS = [
 dict(tag="McGaugh+24", cite="arXiv:2406.17930", note="BTFR/f_DM to z~2.5: 'no clear evolution'. Inherits "
      "the literature samples' selection (exposure ~0.4-0.6) -> a FLAT-leaning bound, not an independent "
      "point; including it would partly double-count Ubler/Tiley/Di Teodoro."),
 dict(tag="Milgrom17 / Sharma+24", cite="arXiv:1703.06110 / arXiv:2406.08934", note="Milgrom: direct high-z "
      "RCs 'all but exclude' a x4 a0 rise AND the (1+z)^1.5 law -> a one-sided bound that would hit M-RISE "
      "hard. Sharma: a FREE-slope bTFR ZP can flip sign vs Ubler -> demonstrates fixed-slope ZPs are not "
      "clean a0 reads. Both EXCLUDED from the baseline: quantifying Milgrom's 'all but' as a sigma would "
      "be inventing a number, and it points AGAINST M-RISE i.e. it would FLATTER the framework."),
]

print("\n" + bar)
print("S2 -- (b) EXPOSURE WEIGHTS to the apparent-a0 drift:  w_i = %.2f*s_i + %.2f*b_i" % (F_SEL, F_BEAM))
print(bar)
print(f"  {'#':>2} {'constraint':24} {'z':>5} {'cur':>5} {'N':>4} {'s_i':>5} {'b_i':>5} {'w_i':>6}   exposure class")
print("  " + "-"*96)
for i, d in enumerate(DATA, 1):
    d["w"] = F_SEL*d["s"] + F_BEAM*d["b"]
    cls = ("MAXIMAL (direct-RAR, g_obs-selected)" if d["w"] >= 0.95 else
           "HIGH (uncorrected selection)"        if d["w"] >= 0.70 else
           "MODERATE"                            if d["w"] >= 0.45 else
           "LOW"                                 if d["w"] >= 0.25 else
           "MINIMAL (lensed / drift-controlled)")
    print(f"  {i:>2} {d['tag']:24} {d['z']:>5.2f} {d['cur']:>5} {d['N']:>4} {d['s']:>5.2f} {d['b']:>5.2f} "
          f"{d['w']:>6.3f}   {cls}")
print("  " + "-"*96)
print("  ORDERING CHECK (required by the brief): maximal for the DIRECT-RAR and the diluted-bTFR points,")
print("  minimal for the clean lensed near-a0 bTFR and the deep-MOND-ish object.")
_w = {d["tag"]: d["w"] for d in DATA}
assert _w["MUSE-DARK III"] == max(_w.values()), "the direct-RAR g_obs-selected point must carry MAX exposure"
assert _w["MUSE-DARK II (Jeanneau)"] < 0.30 and _w["Tiley z1.0 matched"] < 0.30, "clean points must be MINIMAL"
assert _w["Ubler z0.9"] > 0.85 and _w["Ubler z2.3"] > 0.85, "the diluted bTFR points must be HIGH"
assert _w["Big Wheel z3.25"] < 0.45, "the deep-MOND-ish object must be LOW"
print(f"    PASSED: MUSE-DARK III {_w['MUSE-DARK III']:.2f} (max) > Ubler {_w['Ubler z2.3']:.2f} > "
      f"Amvrosiadis {_w['Amvrosiadis z2.4']:.2f} > Di Teodoro {_w['Di Teodoro z1.0']:.2f} > "
      f"Big Wheel {_w['Big Wheel z3.25']:.2f} > MSA-3D {_w['MSA-3D']:.2f} > "
      f"Jeanneau {_w['MUSE-DARK II (Jeanneau)']:.2f} > Tiley {_w['Tiley z1.0 matched']:.2f}")
print("\n  PER-POINT JUSTIFICATION (from the observable's CONSTRUCTION):")
for i, d in enumerate(DATA, 1):
    print(f"\n   [{i}] {d['tag']}  ({d['cite']})   s={d['s']:.2f} b={d['b']:.2f} -> w={d['w']:.3f}")
    print(f"       SELECTION: {d['why_s']}")
    print(f"       BEAM/PRESS: {d['why_b']}")
for b in BOUNDS:
    print(f"\n   [--] {b['tag']} ({b['cite']}) -- CONTEXT ONLY: {b['note']}")

# =======================================================================================
# S3 -- (c) THE ACCELERATION-DILUTION TABLE  L_i  and the resulting INFORMATION weights
# =======================================================================================
print("\n" + bar)
print("S3 -- (c) ACCELERATION-DILUTION per point:  L_M = 1/(1+2y) = x/(2+x),  x = a0/g_bar,  y = g_bar/a0")
print(bar)
print("  a0 INFORMATION at fixed measurement error scales as L^2 (the predicted signal is L x the")
print("  deep-MOND signal, so the signal-to-noise is L x, and the chi2 lever L^2 x).")
print("  For the two DIRECTLY-FITTED-a0 points the a0-line is exact at any y, so L=1 in the MAPPING and")
print("  the dilution appears instead as the COHERENT-ERROR AMPLIFICATION A = 2(1+y) on g_obs and")
print("  (1+2y) on g_bar -- which is precisely why their drift EXPOSURE is maximal.")
print(f"\n  {'constraint':24} {'z':>5} {'y=g_bar/a0':>11} {'x=a0/g_bar':>11} {'L_M':>7} {'L_M^2':>8} "
      f"{'info vs':>9} {'amp 2(1+y)':>11} {'used L':>7}")
print(f"  {'':24} {'':>5} {'':>11} {'':>11} {'':>7} {'':>8} {'Jeanneau':>9} {'on g_obs':>11} {'':>7}")
print("  " + "-"*98)
L_REF = float(L_mass(0.5))                    # Jeanneau, the cleanest near-a0 zero-point = the reference
for d in DATA:
    y = d["y"]
    d["L_M"] = float(L_mass(y)); d["L_g"] = float(L_rar(y)); d["amp"] = 2.0*(1.0+y)
    d["L_used"] = 1.0 if d["cur"] in ("slope", "lr") else d["L_M"]     # exact-a0 currencies: L=1
    rel = (d["L_M"]/L_REF)**2
    print(f"  {d['tag']:24} {d['z']:>5.2f} {y:>11.2f} {1.0/y:>11.2f} {d['L_M']:>7.3f} {d['L_M']**2:>8.4f} "
          f"{rel:>8.3f}x {d['amp']:>11.2f} {d['L_used']:>7.3f}")
print("  " + "-"*98)
print("  THE HEADLINE DILUTION NUMBERS the brief asks for, all from the framework's OWN kernel:")
_d = {x["tag"]: x for x in DATA}
for t in ["Ubler z0.9", "Ubler z2.3", "Amvrosiadis z2.4"]:
    x = _d[t]
    print(f"    {t:18} y={x['y']:.1f}  L_M={x['L_M']:.3f}  -> carries only {x['L_M']**2/L_REF**2:.3f}x the a0 "
          f"information of Jeanneau: {L_REF**2/x['L_M']**2:>5.1f}x LESS.")
for t in ["MUSE-DARK II (Jeanneau)", "Big Wheel z3.25"]:
    x = _d[t]
    print(f"    {t:18} y={x['y']:.2f} L_M={x['L_M']:.3f}  -> the REFERENCE-class lever "
          f"({'the largest zero-point lever in hand' if 'Jeanneau' in t else 'transitional, NOT deep-MOND'}).")
print("\n  WHAT THE DILUTION DOES TO THE 'RISING' bTFR POINTS (the reason they cannot be used at naive")
print("  strength in EITHER direction):  a measured mass-axis offset Delta_b, DE-DILUTED, implies")
print("     log10(a0(z)/a0(0)) = -Delta_b / L_M   +/-  sigma(Delta_b) / L_M")
for t in ["Ubler z0.9", "Ubler z2.3", "Amvrosiadis z2.4", "MUSE-DARK II (Jeanneau)"]:
    x = _d[t]
    c, e = -x["obs"]/x["L_M"], x["sig"]/x["L_M"]
    print(f"    {t:24} Delta_b={x['obs']:+.2f}+/-{x['sig']:.2f} dex -> log10 R = {c:+.2f} +/- {e:.2f} dex "
          f"= ratio {10**c:.2f} (x{10**e:.0f} band)")
print("    => the naive 'a0 rose x1.9-2.8' readings are what you get by IGNORING the lever. De-diluted,")
print("       the SAME numbers demand implausible ratios with error bars of 1.5-4 DEX -- i.e. they carry")
print("       essentially NO a0 information. This is why the forward direction (dilute the PREDICTION,")
print("       the committed ledger's convention) is the only usable one, and it is what S4 does.")

# =======================================================================================
# S4 -- (d) THE JOINT LIKELIHOOD.  Forward model per point (the committed ledger convention:
#      DILUTE THE PREDICTION, never de-dilute the datum):
#
#   slope currency :  obs  ~  Normal( d log10 R_M/d log10(1+z) |_[zlo,zhi]  +  w_i * p ,  sig )
#   db  currency   :  obs  ~  Normal( -L_M(y) * [ log10 R_M(z) + w_i*p*log10(1+z) ]      ,  sig )
#   lr  currency   :  obs  ~  Normal(          log10 R_M(z) + w_i*p*log10(1+z)           ,  sig )
#
#   All three models have ZERO free parameters. p is a SINGLE SHARED nuisance with the S1 prior.
#   Marginal likelihood  Z_M = INT dp  pi(p)  PROD_i  N( obs_i | mu_i(M,p), sig_i ).
# =======================================================================================
def mu_point(d, Rfun, p, w0=W0, wa=WA):
    """model prediction for point d under branch Rfun and drift exponent p."""
    if d["cur"] == "slope":
        s_model = loglog_slope(Rfun, d["zlo"], d["zhi"], w0=w0, wa=wa)
        return s_model + d["w"] * p
    lr = float(np.log10(Rfun(d["z"], w0=w0, wa=wa))) + d["w"] * p * np.log10(1.0 + d["z"])
    return -d["L_M"] * lr if d["cur"] == "db" else lr

def chi2_model(Rfun, p, data=DATA, w0=W0, wa=WA, sigscale=None):
    tot = 0.0
    for d in data:
        s = d["sig"] if sigscale is None else sigscale.get(d["tag"], d["sig"])
        tot += ((d["obs"] - mu_point(d, Rfun, p, w0, wa)) / s) ** 2
    return tot

def lnZ(Rfun, data=DATA, pgrid=PGRID, prior=PRIOR, w0=W0, wa=WA, sigscale=None):
    """ln of the p-marginalized likelihood (up to the common 1/(sqrt(2pi)sig) factors, which
    cancel exactly in every Bayes factor because all models share the same data + errors)."""
    c2 = np.array([chi2_model(Rfun, p, data, w0, wa, sigscale) for p in pgrid])
    l = -0.5 * (c2 - c2.min())
    return float(np.log(np.trapz(np.exp(l) * prior, pgrid)) - 0.5 * c2.min()), c2

def pairs(lz):
    out = {}
    for a, b in [("M-DEC", "M-RISE"), ("M-DEC", "M-FLAT"), ("M-RISE", "M-FLAT")]:
        out[f"{a} vs {b}"] = lz[a] - lz[b]
    return out

def fmt_bf(lnb):
    """report as odds, always 'X:1 for the FAVOURED model'."""
    if lnb >= 0: return f"{np.exp(min(lnb, 700)):.3g}:1", "first"
    return f"{np.exp(min(-lnb, 700)):.3g}:1", "second"

def show(title, lz, note=""):
    print(f"\n  [{title}]" + (f"   {note}" if note else ""))
    best = max(lz, key=lz.get)
    for m in ["M-DEC", "M-RISE", "M-FLAT"]:
        print(f"     ln Z({m:6}) = {lz[m]:>12.3f}   Delta ln Z vs best = {lz[m]-lz[best]:>10.3f}"
              + ("   <-- BEST" if m == best else ""))
    for k, v in pairs(lz).items():
        o, who = fmt_bf(v)
        a, b = k.split(" vs ")
        print(f"     BF {k:20} = {o:>14}  for {(a if who=='first' else b)}   (ln BF = {v:+.2f})")
    return best

print("\n" + bar)
print("S4 -- (d) THE THREE-MODEL LIKELIHOOD  (9 numeric constraints, 0 free parameters each)")
print(bar)
print(f"  {'constraint':24} {'cur':>5} {'obs':>8} {'sig':>6} {'w_i':>6} {'L_used':>7} | "
      f"{'mu(DEC)':>8} {'mu(RISE)':>9} {'mu(FLAT)':>9}   [at p = p_cal]")
print("  " + "-"*98)
for d in DATA:
    print(f"  {d['tag']:24} {d['cur']:>5} {d['obs']:>+8.3f} {d['sig']:>6.3f} {d['w']:>6.3f} {d['L_used']:>7.3f} | "
          f"{mu_point(d,R_DEC,P_CAL):>+8.3f} {mu_point(d,R_RISE,P_CAL):>+9.3f} {mu_point(d,R_FLAT,P_CAL):>+9.3f}")

# ---------- (A) FACE VALUE: p == 0, i.e. ASSERT there is NO LCDM-degenerate drift ----------
lzA = {m: -0.5*chi2_model(f, 0.0) for m, f in MODELS.items()}
print("\n" + "-"*100)
print("  (A) FACE VALUE  --  p FIXED AT 0 (systematics minimal: assert NO apparent-a0 drift at all),")
print("      and MUSE-DARK III at its STAT-ONLY error. This is the strongest possible reading of the")
print("      rising measurement and it is reported at FULL strength, not softened.")
bestA = show("A: face value, p=0, stat-only", lzA)
for m, f in MODELS.items():
    print(f"       chi2({m:6}) = {chi2_model(f,0.0):>10.2f}  (9 points, 0 params)")
print("      MUSE-DARK III alone at p=0: "
      f"{abs(MU_A1*JAC_MU - loglog_slope(R_DEC,0.33,1.44))/ (MU_A1_STAT*JAC_MU):.1f}s from DEC, "
      f"{abs(MU_A1*JAC_MU - loglog_slope(R_RISE,0.33,1.44))/(MU_A1_STAT*JAC_MU):.1f}s from RISE, "
      f"{abs(MU_A1*JAC_MU)/(MU_A1_STAT*JAC_MU):.1f}s from FLAT")
print("      READ PLAINLY: at face value the data pick M-RISE overwhelmingly, and the odds against the")
print("      framework's declining branch are astronomical. That is the honest face-value number.")
print("      It is NOT the honest FINAL number, for one stated reason: p=0 asserts zero LCDM-degenerate")
print("      drift, which BOTH independent calibrations contradict (sim 0.92, MSA-3D's own data 1.13).")

# ---------- (B) DRIFT AT ITS CALIBRATED CENTRAL, NOT marginalized ----------
lzB = {m: -0.5*chi2_model(f, P_CAL) for m, f in MODELS.items()}
print("\n" + "-"*100)
print(f"  (B) DRIFT AT THE CALIBRATED CENTRAL  --  p FIXED AT p_cal = {P_CAL:.2f} (Magneticum), no marginalization")
bestB = show(f"B: p fixed = {P_CAL:.2f}", lzB)
for m, f in MODELS.items():
    print(f"       chi2({m:6}) = {chi2_model(f,P_CAL):>10.2f}")

# ---------- (C) FULLY MARGINALIZED over the S1 prior on p ----------
lzC, c2C = {}, {}
for m, f in MODELS.items():
    lzC[m], c2C[m] = lnZ(f)
print("\n" + "-"*100)
print(f"  (C) FULLY MARGINALIZED over p ~ N({P_CAL:.2f},{SIG_P:.2f}) truncated [{P_LO:+.2f},{P_HI:+.2f}]  ** THE HEADLINE **")
bestC = show("C: p marginalized", lzC)
print("\n     posterior on the SHARED drift exponent p under each model (what each model NEEDS p to be):")
for m in ["M-DEC", "M-RISE", "M-FLAT"]:
    post = np.exp(-0.5*(c2C[m]-c2C[m].min()))*PRIOR
    post /= np.trapz(post, PGRID)
    cdf = np.cumsum(post)*np.gradient(PGRID)[0]; cdf /= cdf[-1]
    a16, a50, a84 = np.interp([0.16,0.5,0.84], cdf, PGRID)
    print(f"       {m:6}: p = {a50:+.2f}  68% [{a16:+.2f},{a84:+.2f}]   "
          f"prior tension = {abs(a50-P_CAL)/SIG_P:.2f} sigma"
          + ("   <- needs a drift ABOVE the calibration" if a50 > P_CAL + SIG_P else
             "   <- needs a drift BELOW/AGAINST the calibration" if a50 < P_CAL - SIG_P else
             "   <- sits INSIDE the calibrated prior"))
print("\n     HOW THE VERDICT MOVES (this sensitivity IS the result, per the brief):")
for k in pairs(lzA):
    oa, wa_ = fmt_bf(pairs(lzA)[k]); ob, wb_ = fmt_bf(pairs(lzB)[k]); oc, wc_ = fmt_bf(pairs(lzC)[k])
    a, b = k.split(" vs ")
    fa = a if wa_=="first" else b; fb = a if wb_=="first" else b; fc = a if wc_=="first" else b
    print(f"       {k:20}  face value {oa:>12} ({fa:6}) -> p=p_cal {ob:>10} ({fb:6}) -> marginalized {oc:>10} ({fc:6})")
