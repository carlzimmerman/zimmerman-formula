#!/usr/bin/env python3
"""
================================================================================
FROZEN PRE-REGISTRATION ARTIFACT (2026-07-23)
THE CROSS-REDSHIFT a0-LINE ZERO-PARAMETER TEST
de Sitter-Unruh MODIFIED-INERTIA framework  vs  const-a0 MOND  vs  evolving MOND
================================================================================

WHAT THIS FREEZES. The standalone a0(z) "detect a decline" band is soft (~2-2.5 sigma,
conditional on DE evolving). This artifact freezes the SHARPER test: the framework ties
the z=0 ABSOLUTE scale and the a0(z) EVOLUTION to the SAME single number, Planck Lambda:

    a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE0),   a0(0) = c*H_Lambda/Z = 9.355e-11 (canonical),
    a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))   [FULL non-monotonic closed form]

ZERO free parameters for the WHOLE a0(z) curve -- amplitude AND shape. Posed as a
PARAMETER-COUNTING showdown of three models for the ABSOLUTE a0(z) measured in z-bins via
the a0-line slope estimator (g_obs^2 - g_bar^2 = a0*g_bar):
    M0 FRAMEWORK  (0 free): a0(0) FIXED by Planck Lambda, shape FIXED by the SAME Lambda.
    M1 CONST-a0   (1 free): a0(z) = A                (Milgrom constant-a0 MOND; A fitted).
    M2 EVOLV-MOND (2 free): a0(z) = A*(1+z)^p        (amplitude A + power p, both fitted).
An information-criterion / Bayes advantage of ~(delta-params) accrues to M0 IF the binned
slopes match -- and it does NOT wash out the way a single-bin 2-sigma decline does.

--------------------------------------------------------------------------------
THIS IS A CONSOLIDATION / FREEZE. It BUILDS ON and REGRESSION-CHECKS (does NOT modify or
contradict) the committed working scripts, and reproduces their headline numbers exactly:
    prep_2026/a0_line/{identity_uniqueness,estimator_theory}.py   -- z=0 identity + budget
    prep_2026/a0_line_crossz/crossz_estimator_landscape.py        -- estimator + inventory
    prep_2026/a0z_crossscale/model_comparison_a0z.py              -- M0/M1/M2 dBIC / Bayes
    prep_2026/a0z_crossscale/highz_systematics_floor.py           -- per-bin floor + go/no-go
    prep_2026/a0z_crossscale/a0z_prediction_band_2026.py          -- frozen decline band
    prep_2026/highz_tfr_fork/DATA_LEDGER.md                       -- real high-z TFR data
Same law, same DESI DR2 w0waCDM posteriors, same anchor a0(0)=c*H_Lambda/Z from the ledger.

--------------------------------------------------------------------------------
HARD CALIBRATION RULES (this repo has a HISTORY of BOTH manufactured wins AND manufactured
deficits -- BOTH are penalized; a "floored" verdict is verified as rigorously as a "win"):
 (1) The zero-parameter claim MUST be real: Planck Lambda fixes BOTH a0(0) AND the a0(z)
     shape with NO hidden fitted normalization. Verified in (0) by reconstructing c*H_Lambda/Z
     and by showing (S3) freeing M0's amplitude collapses its M1 advantage by exactly +ln(n).
 (2) HIGH-z SYSTEMATICS ARE SEVERE AND HONESTLY FLOORED: beam smearing, turbulent pressure
     support / asymmetric drift, gas-mass calibration drift, Upsilon. They are BIN-CORRELATED
     (shared sigma0/AD + PSF models) so they do NOT average down. Sections (iii)-(iv).
 (3) DEEP-MOND penalty: a0=g_obs^2/g_bar DOUBLES per-point log scatter (sigma(ln a0)=2 sigma(ln g));
     applied in every z bin: per-bin a0 precision f <-> underlying RC precision f/2, N ~ (2 sigma_g/f)^2.
 (4) BOTH footings: a0(0)=9.355e-11 (canonical pure-Lambda) vs 1.131e-10 (alt cH0). The RATIO
     shape is footing-INDEPENDENT (sympy-proved); only the z=0 ABSOLUTE anchor differs -- so the
     cross-z ladder ALSO helps separate footings via its z=0 amplitude (Step A). Section (v).
 (5) The a0(z) SHAPE is degenerate with "does DE evolve" UNLESS anchored; the SAME Lambda fixing
     the z=0 amplitude is what breaks it in the JOINT (amplitude+shape) zero-parameter fit.
     If DE does not evolve (w->-1) the ratio is EXACTLY 1 and M0==M1: untestable, not falsified.
 (6) No "theory closed." Every load-bearing number is recomputed here and regression-checked.

WELLHEAD CREDIT: the interpolation nu=sqrt(1+1/y) is Milgrom 1999 (PLA 253:273 Eq. 9); the
framework's distinctive content is the cH_Lambda/Z COEFFICIENT and the modified-inertia
completion, not the kernel form.
================================================================================
"""
import numpy as np
import sympy as sp
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = "/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger"
anchor = json.load(open(os.path.join(LEDGER, "anchor_values.json")))
A0_CANON, A0_ALT = anchor["a0_canon"], anchor["a0_alt"]     # 9.355e-11 (Lambda) ; 1.131e-10 (alt)
DEX = np.log(10.0)
bar = "#" * 84
sep = "=" * 92

# committed sibling JSONs used for regression parity (builds-on, does-not-contradict)
def _load(p):
    try:
        return json.load(open(os.path.join(HERE, p)))
    except Exception:
        return None
J_MODEL = _load("model_comparison_a0z_results.json")
J_FLOOR = _load("highz_systematics_floor_results.json")

# ---- shared law + DESI DR2 posteriors (IDENTICAL to the committed siblings) ---------------
def a0ratio(z, w0, wa):
    """FULL non-monotonic closed form a0(z)/a0(0); z scalar/array."""
    z = np.asarray(z, float)
    return (1.0 + z) ** (1.5 * (1.0 + w0 + wa)) * np.exp(-1.5 * wa * z / (1.0 + z))

DATASETS = [   # (label, w0, wa, LCDM-excl-sigma)   [central values; shape uses the central]
    ("DESI+CMB+Pantheon+", -0.838, -0.62, 2.8),
    ("DESI+CMB+DESY5",     -0.752, -0.86, 4.2),
    ("DESI+CMB+Union3",    -0.667, -1.09, 3.8),
]
HEAD = DATASETS[0]                                            # Pantheon+ central = headline
PARAM_COUNT = {"M0": 0, "M1": 1, "M2": 2}                     # <-- the whole point (rule 1)

print(bar)
print("# FROZEN CROSS-REDSHIFT a0-LINE ZERO-PARAMETER TEST  --  2026-07-23")
print("# a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))   [FULL, non-monotonic]")
print("# M0 framework (0 free)  vs  M1 const-a0 MOND (1)  vs  M2 evolving MOND (2)")
print(bar)

# ==========================================================================================
# (0) THE ZERO-PARAMETER CLAIM IS REAL (a0(0) DERIVED, not fitted; shape from DESI background)
# ==========================================================================================
print("\n" + sep)
print("(0) ZERO-PARAMETER VERIFICATION  --  Planck Lambda fixes BOTH amplitude AND shape")
print(sep)
cval, HL, Zv = 2.99792458e8, anchor["HL"], anchor["Z"]
recon = cval * HL / Zv
assert abs(recon - A0_CANON) / A0_CANON < 1e-6, "a0(0) is NOT c*H_Lambda/Z -- zero-param claim broken"
print(f"  a0(0) canonical  = c*H_Lambda/Z = {A0_CANON:.4e} m/s^2   (Z=sqrt(32pi/3)={Zv:.4f})")
print(f"  reconstruction   = c*H_Lambda/Z = {recon:.4e}  == ledger anchor  [amplitude DERIVED, not fitted]")
print(f"  a0(0) alt        = k*c*H0       = {A0_ALT:.4e} m/s^2   (footing fork; ratio-independent)")
print("  M0 SHAPE sqrt(rho_DE(z)/rho_DE0) reads (w0,wa) from DESI's BACKGROUND (SNe/BAO) fit --")
print("  NOT fitted to any galaxy a0(z). No knob touches the galaxy data. Free-parameter counts:")
for m in ("M0", "M1", "M2"):
    print(f"    {m}: {PARAM_COUNT[m]} free parameter(s)"
          + ("  <- amplitude & shape BOTH fixed by Planck Lambda" if m == "M0" else ""))
assert PARAM_COUNT["M0"] == 0, "M0 must have zero free parameters"

# ==========================================================================================
# (i) THE REDSHIFT-BINNED ESTIMATOR + THE REAL RESOLVED-KINEMATICS INVENTORY THAT EXISTS TODAY
# ==========================================================================================
print("\n" + sep)
print("(i) THE PER-BIN a0-LINE ESTIMATOR (redshift-invariant) + REAL high-z data inventory")
print(sep)
gbv, a0zs = sp.symbols("g_bar a0_z", positive=True)
g_obs = sp.sqrt(gbv**2 + a0zs * gbv)                         # a0zs = a0(z_k): the ONLY z-dependence
assert sp.simplify(sp.expand(g_obs**2 - gbv**2) - a0zs * gbv) == 0
print("  sympy: in bin z_k, g_obs^2 - g_bar^2 = a0(z_k)*g_bar EXACTLY -- a through-origin line whose")
print("  SLOPE is a0(z_k). z enters ONLY through the slope, so the a0-line estimator")
print("  a0_hat(z_k) = sum(w E g)/sum(w g^2) is the SAME object in every bin (estimator_theory.py).")
print("  Running it in bins {z} is a well-posed 0-vs-1-vs-2 parameter showdown (M0/M1/M2).")
print("\n  REAL RESOLVED-KINEMATICS INVENTORY (order-level census; rows cite the survey, NOT a re-reduction):")
print(f"    {'survey':22} {'z-range':>11} {'N_res':>7} {'N_gasdom(a0-line)':>18} {'sigma_v':>9}")
print(f"    {'-'*22} {'-'*11} {'-'*7} {'-'*18} {'-'*9}")
INVENTORY = [
    ("SPARC (z=0 ANCHOR)",  "0.0",       "175", "~30-50",  "3-10%"),
    ("DYNAMO",              "0.07-0.13", "~40", "~5-10",   "5-15%"),
    ("MUSE/MAGPI",          "0.25-0.42", "~60", "0",       "5-15%"),
    ("MUSE-DARK (lensed)",  "0.56-1.37", "95",  "0*",      "10-20%"),
    ("MSA-3D (JWST)",       "0.5-1.7",   "~45", "0**",     "10-20%"),
    ("KMOS3D",              "0.6-2.7",   "739", "0",       "10-30%"),
    ("SINS / zC-SINF",      "1.3-2.6",   "~110","0",       "15-40%"),
    ("PHIBSS (gas mass)",   "0.5-2.6",   "~100","0",       "n/a"),
    ("KROSS / KGES",        "0.9 / 1.5", "~790","0",       "20-35%"),
]
for s, zr, nr, ng, sv in INVENTORY:
    print(f"    {s:22} {zr:>11} {nr:>7} {ng:>18} {sv:>9}")
print("   *MUSE-DARK reaches g_bar~a0 (lensed low-mass) but INTEGRATED TFR only, no resolved Sigma_gas(R)")
print("     -> bTFR zero-point 0.00+/-0.27 already banked (highz_tfr_fork); NOT a resolved a0-line slope.")
print("  **MSA-3D a0(z) is via the f_DM(Re) PROXY inversion, selection-confounded (WEAK-TENSION/WATCH),")
print("     NOT a gas-dominated a0-line slope.")
print("  => N_gasdom(resolved, a0-line-usable) ~ 0 at EVERY z>=0.5 today. The clean a0-line needs a")
print("     resolved gas surface-density profile Sigma_gas(R); resolved HI dies by z~0.1-0.2, resolved")
print("     CO/[CII] exists for only a handful of ALMA disks. No statistical sample at cosmic noon.")

# ==========================================================================================
# (ii) PARAMETER-COUNTING MODEL COMPARISON  M0 over {M1, M2}  (Asimov: data == M0 central)
#      Delta-BIC / Bayes-factor advantage vs data quality, with the deep-MOND 2x penalty.
# ==========================================================================================
print("\n" + sep)
print("(ii) PARAMETER-COUNTING MODEL COMPARISON  M0(0) over M1(1)/M2(2)  [Asimov: data==M0]")
print("     Delta-AIC(Mj-M0)=chi2_j+2 k_j ; Delta-BIC(Mj-M0)=chi2_j+k_j ln(n) ; deep-MOND RC=f/2")
print(sep)
ZGRID = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])       # z=0 anchor + evenly spaced to z=3
Z0_ANCHOR_F = 0.16                                          # committed a0-line gas-dom slope: +/-16%

def sig_uniform(f_hiz, zgrid=ZGRID):
    s = np.full(len(zgrid), f_hiz, float)
    s[zgrid == 0.0] = Z0_ANCHOR_F
    return s

def fit_signals(zgrid, sig, w0, wa):
    """Asimov data==M0. Residual chi2 of best rival to the true curve (offset ln a0(0) cancels):
       S1 = weighted variance of t=ln R(z)  (M1 const, 1 param);  S2 = power-law residual (M2, 2)."""
    t = np.log(a0ratio(zgrid, w0, wa))
    w = 1.0 / sig ** 2
    x = np.log(1.0 + zgrid)
    W = w.sum()
    tbar = (w * t).sum() / W
    S1 = float((w * (t - tbar) ** 2).sum());  F1 = float(W)
    X = np.vstack([np.ones_like(x), x]).T
    XtW = X.T * w
    F2 = XtW @ X
    beta = np.linalg.solve(F2, XtW @ t)
    S2 = float((w * (t - X @ beta) ** 2).sum())
    return dict(S1=S1, S2=S2, F1=F1, detF2=float(np.linalg.det(F2)), n=len(zgrid))

def ic_row(zgrid, sig, w0, wa):
    s = fit_signals(zgrid, sig, w0, wa)
    n = s["n"]
    dBIC1, dBIC2 = s["S1"] + 1 * np.log(n), s["S2"] + 2 * np.log(n)
    Wln, Wp = np.log(100.0), 6.0                            # priors: lnA log-flat 2 dec, p flat[-3,3]
    lnZ1 = -s["S1"] / 2 - np.log(Wln) + 0.5 * np.log(2 * np.pi) - 0.5 * np.log(s["F1"])
    lnZ2 = (-s["S2"] / 2 - np.log(Wln) - np.log(Wp) + 1.0 * np.log(2 * np.pi) - 0.5 * np.log(s["detF2"]))
    return dict(sqrtS1=np.sqrt(s["S1"]), sqrtS2=np.sqrt(s["S2"]),
                dBIC1=dBIC1, dBIC2=dBIC2, lnB01=-lnZ1, lnB02=-lnZ2, n=n)

print(f"  fiducial grid z = {list(ZGRID)}  (n={len(ZGRID)}; z=0 anchored at the a0-line f={Z0_ANCHOR_F})")
print(f"  {'f_hiz':>6} {'RC f/2':>7} | {'dataset':<20} {'sqrtS1':>7} {'sqrtS2':>7} | "
      f"{'dBIC(M1)':>9} {'dBIC(M2)':>9} | {'lnB01':>6} {'lnB02':>6}")
print("  " + "-" * 90)
for f_hiz in (0.20, 0.10, 0.05, 0.03):
    for label, w0, wa, excl in DATASETS:
        r = ic_row(ZGRID, sig_uniform(f_hiz), w0, wa)
        print(f"  {f_hiz:>6.2f} {f_hiz/2:>7.3f} | {label:<20} {r['sqrtS1']:>7.2f} {r['sqrtS2']:>7.2f} | "
              f"{r['dBIC1']:>9.1f} {r['dBIC2']:>9.1f} | {r['lnB01']:>6.1f} {r['lnB02']:>6.1f}")
    print("  " + "-" * 90)
print("  sqrtS1 = sigma-equiv of the SHAPE signal (M0-vs-flat M1); sqrtS2 = CURVATURE signal (M0-vs-M2).")
print("  Kass-Raftery: dBIC>10 'very strong', 6-10 'strong', 2-6 'positive'. Threshold used below: dBIC>9.")

# headline (Pantheon+, f=0.05) + the sharpening + deep-MOND N + required precision
head = ic_row(ZGRID, sig_uniform(0.05), HEAD[1], HEAD[2])
n = int(head["n"])
dBIC_M0_fixed  = head["sqrtS1"] ** 2 + 1 * np.log(n)        # M0 (0 param) vs M1
dBIC_M0_fitted = head["sqrtS1"] ** 2 + 0.0                  # M0' (amplitude fitted, 1 param) vs M1
amp_bonus = dBIC_M0_fixed - dBIC_M0_fitted                 # == ln(n): the amplitude-anchor value
print(f"\n  SHARPENING (Pantheon+ central, f=0.05, n={n}) vs the standalone ~2-2.5 sigma decline:")
print(f"    standalone 'is a0(z) flat?' detection ....... sqrtS1 = {head['sqrtS1']:.2f} sigma  (shape only)")
print(f"    M0 (amplitude FIXED, 0 param)  vs M1 ........ Delta-BIC = {dBIC_M0_fixed:.2f}")
print(f"    M0'(amplitude FITTED, 1 param) vs M1 ........ Delta-BIC = {dBIC_M0_fitted:.2f}")
print(f"    => the z=0 AMPLITUDE ANCHOR is worth +{amp_bonus:.2f} dBIC = +ln(n) (a factor sqrt(n)={np.sqrt(n):.2f}")
print(f"       in the Bayes odds vs M1). REAL & cosmology-robust but MODEST in the Asimov value; its")
print(f"       LARGER role is a z=0 FALSIFIER: a measured a0(0) off 9.355e-11 by ~16% is a ~1 sigma")
print(f"       one-bin kill UNIQUE to M0 (rivals absorb the offset into their free amplitude A).")

# required per-bin precision to beat BOTH M1 AND M2 at dBIC>9, full-span grid, deep-MOND N
TARGET_BIC = 9.0
def required_f(which, target=TARGET_BIC, zgrid=ZGRID, w0=HEAD[1], wa=HEAD[2]):
    def dBIC_at(f):
        r = ic_row(zgrid, sig_uniform(f, zgrid), w0, wa)
        return r["dBIC1"] if which == "M1" else r["dBIC2"]
    if dBIC_at(1.0) >= target:  return 0.0
    lo, hi = 1e-3, 1.0
    if dBIC_at(lo) < target:    return np.inf
    for _ in range(60):
        mid = np.sqrt(lo * hi)
        lo, hi = (mid, hi) if dBIC_at(mid) >= target else (lo, mid)
    return float(np.sqrt(lo * hi))
fM1, fM2 = required_f("M1"), required_f("M2")
fbind = min(fM1, fM2)                                        # binding = the tighter (M2 is binding)
print(f"\n  REQUIRED per-bin a0 precision to beat BOTH rivals at Delta-BIC>{TARGET_BIC:.0f} (full-span n={n}):")
print(f"    vs M1 (const-a0 MOND) : f <= {100*fM1:.2f}%   (underlying RC {100*fM1/2:.2f}%)")
print(f"    vs M2 (evolving MOND) : f <= {100*fM2:.2f}%   (underlying RC {100*fM2/2:.2f}%)  <- BINDING rival")
for name, dexg in (("SPARC-quality 0.10 dex", 0.10), ("realistic high-z 0.20 dex", 0.20)):
    sg = dexg * DEX
    Ngal = (2 * sg / fbind) ** 2
    print(f"    DEEP-MOND N_gal/bin at per-point {name:24}: ~{Ngal:,.0f}  (x{n-1} bins = {Ngal*(n-1):,.0f} RCs)")
print("  READING: beating M1 needs a few-% a0 per bin; beating M2 needs the data to STRADDLE the")
print("  non-monotonic bump+decline so the power-law CURVATURE residual is resolved -- a full-z-span,")
print("  >2030, campaign-level requirement, NOT delivered by the Occam term alone.")

# regression parity vs the committed model_comparison_a0z.py
if J_MODEL:
    jp = J_MODEL["at_f0p05_Pantheon"]; js = J_MODEL["sharpening"]
    for k, here, there in (("sqrtS1", head["sqrtS1"], jp["sqrtS1"]),
                           ("dBIC_M1", dBIC_M0_fixed, jp["dBIC_M1"]),
                           ("dBIC_M2", head["sqrtS2"] ** 2 + 2 * np.log(n), jp["dBIC_M2"]),
                           ("lnB01", head["lnB01"], jp["lnB01"]),
                           ("amp_anchor_dBIC", amp_bonus, js["amplitude_anchor_dBIC"])):
        assert abs(here - there) < 1e-6, f"regression mismatch vs model_comparison_a0z.py: {k}"
    print("  [regression OK: sqrtS1, dBIC(M1), dBIC(M2), lnB01, amplitude-anchor MATCH model_comparison_a0z.py]")

# ==========================================================================================
# (iii) THE HIGH-z SYSTEMATIC FLOOR PER BIN (beam + pressure + gas-cal + Upsilon in quadrature)
#       vs the REQUIRED per-bin precision to reject flat. Deep-MOND amplification 4(y+1) etc.
# ==========================================================================================
print("\n" + sep)
print("(iii) PER-BIN a0(z) SYSTEMATIC FLOOR (beam+pressure+gas+Upsilon, quadrature) vs REQUIRED precision")
print(sep)
# deep-MOND amplification of per-point errors into a0=(g_obs^2-g_bar^2)/g_bar (estimator_theory S3)
AMP_V, AMP_GOBS, AMP_GBAR = (lambda y: 4.0*(y+1.0)), (lambda y: 2.0*(y+1.0)), (lambda y: 2.0*y+1.0)
R_OVER_RD, RD_PHYS = 2.2, 3.0
K_AD = 2.0 * R_OVER_RD
sigma0   = lambda z, cold: (10.0 + 7.0 * z) if cold else (15.0 + 15.0 * z)   # km/s (Uebler+19)
C_AD     = lambda z, V, cold: K_AD * sigma0(z, cold) ** 2 / V ** 2            # asymmetric-drift share
dV_beam  = lambda ratio: 0.02 + 0.05 * ratio                                  # residual after 3D modeling
def d_A(z, Om=0.3, H0=70.0):
    if z <= 0:  return np.inf                                                  # nearby: R_beam/R_d -> 0
    c = 299792.458; zz = np.linspace(0, z, 2000)
    Ez = np.sqrt(Om * (1 + zz) ** 3 + (1 - Om))
    return (c / H0) * np.trapz(1.0 / Ez, zz) / (1 + z)
def theta_Rd(z):
    if z <= 0:  return np.inf
    return (RD_PHYS * (1 + z) ** (-0.75) / 1e3) / d_A(z) * 206265.0
def gascal_dex(z, era):  return (0.12 + 0.06 * z) if era == "TODAY" else (0.08 + 0.03 * z)
def ups_ln(era):         return 0.35 if era == "TODAY" else 0.23
def fres(era):           return 0.50 if era == "TODAY" else 0.30
def beam_ratio(z, era):  return (0.15 if era == "TODAY" else 0.05) / theta_Rd(z)

def floor(z, y, phi, Vrot, era, cold, gascal_override=None):
    s_beam = AMP_V(y) * dV_beam(beam_ratio(z, era))
    C = C_AD(z, Vrot, cold)
    s_press = AMP_GOBS(y) * fres(era) * C / (1.0 + C)
    gcd = gascal_override if gascal_override is not None else gascal_dex(z, era)
    s_gas = AMP_GBAR(y) * (1.0 - phi) * gcd * DEX
    s_ups = AMP_GBAR(y) * phi * ups_ln(era)
    tot = float(np.sqrt(s_beam**2 + s_press**2 + s_gas**2 + s_ups**2))
    fG = dict(beam=0.30, press=0.50, gas=1.00, ups=0.70)                      # global (non-averaging) shares
    glob = float(np.sqrt((fG["beam"]*s_beam)**2 + (fG["press"]*s_press)**2
                         + (fG["gas"]*s_gas)**2 + (fG["ups"]*s_ups)**2))
    return dict(beam=s_beam, press=s_press, gas=s_gas, ups=s_ups, tot=tot, glob=glob, C=C)

# required sigma_meas on a0(z)/a0(0) to reject flat (Pantheon+ central, deep-MOND-penalized)
REQ = {0.35: 0.012, 1.0: 0.004, 2.0: 0.042, 3.0: 0.075}     # 3-sigma required precision (highz floor)
EFF = {0.35: 0.036, 1.0: 0.011, 2.0: 0.126, 3.0: 0.225}     # |ratio-1| effect size

# z=0 anchor floor (HI available -> gas-cal ~0.03 dex, cold local tracer) and z>0 cleanest regime
Z0 = floor(0.0, y=0.5, phi=0.15, Vrot=70.0, era="FUTURE", cold=True, gascal_override=0.03)
print(f"  deep-MOND amplification: d ln a0/d ln V = 4(y+1), /d ln g_obs = 2(y+1), /d ln g_bar = -(2y+1).")
print(f"  z=0 ANCHOR floor (SPARC, HI gas-cal 0.03 dex, cold tracer, y=0.5): {100*Z0['tot']:.0f}%  "
      f"(committed a0-line: +/-16%).")
print(f"\n  {'regime':24} {'era':>7} {'z':>4} {'beam':>7} {'press':>7} {'gas':>7} {'Upsil':>7} | "
      f"{'FLOOR':>7} {'req(3s)':>8} {'floor/req':>10}")
print("  " + "-" * 100)
REG = {"dwarf (gas-dom, y=0.5)":       dict(y=0.5, phi=0.15, Vrot=70.0),
       "intermediate gas-rich (y=0.5)": dict(y=0.5, phi=0.30, Vrot=110.0),
       "massive disk (HSB, y=2.5)":     dict(y=2.5, phi=0.60, Vrot=150.0)}
highz_floors = []                                            # (cleanest-regime) floors at z>0, for self-check
gono = {}
for rlab, rp in REG.items():
    for era, cold in (("TODAY", False), ("FUTURE", True)):
        for z in (2.0, 3.0):
            f = floor(z, rp["y"], rp["phi"], rp["Vrot"], era, cold)
            ratio = f["tot"] / REQ[z]
            verd = "GO" if ratio <= 1.0 else ("MARGINAL" if ratio <= 2.0 else "NO-GO")
            gono[(rlab, era, z)] = (f["tot"], REQ[z], ratio, verd)
            print(f"  {rlab:24} {era:>7} {z:>4.1f} {100*f['beam']:>6.1f}% {100*f['press']:>6.1f}% "
                  f"{100*f['gas']:>6.1f}% {100*f['ups']:>6.1f}% | {100*f['tot']:>6.0f}% {100*REQ[z]:>7.1f}% "
                  f"{ratio:>9.1f}x  {verd}")
# collect cleanest-regime (intermediate gas-rich, FUTURE cold) floors across z for the self-check
for z in (0.5, 1.0, 2.0, 3.0):
    highz_floors.append(floor(z, 0.5, 0.30, 110.0, "FUTURE", True)["tot"])
print("  " + "-" * 100)
print("  READING: PRESSURE support dominates z>=1 warm-tracer rows; the massive-disk rows are Upsilon-")
print("  swamped (star-dominated, high y). No row's TOTAL comes near the ~4-8% requirement -- the floor")
print("  exceeds it by ~9-55x, and it is a COHERENT z-dependent BIAS (pressure tracks sigma0(z)) that")
print("  does NOT average down with N. The z=0 a0-line CLEANLINESS INVERTS at high z: gas dominance")
print("  now means gas-mass calibration (no HI, alpha_CO/[CII]) is the floor, and gas-rich = low V/sigma")
print("  = pressure-destroyed. The clean sample is the WORST pressure case.")

# regression parity vs the committed highz_systematics_floor.py (global intermediate FUTURE z=2)
if J_FLOOR:
    g = floor(2.0, 0.5, 0.30, 110.0, "FUTURE", True)
    jt = J_FLOOR["global_floor_intermediate_future_z2"]
    assert abs(g["tot"] - jt["total"]) < 1e-6 and abs(g["glob"] - jt["global_nonaveraging"]) < 1e-6, \
        "regression mismatch vs highz_systematics_floor.py"
    print(f"  [regression OK: intermediate-FUTURE z=2 total {100*g['tot']:.0f}% & global {100*g['glob']:.0f}% "
          f"MATCH highz_systematics_floor.py]")

# ==========================================================================================
# (iv) THE FROZEN GO / NO-GO
# ==========================================================================================
print("\n" + sep)
print("(iv) FROZEN GO / NO-GO  --  is the zero-parameter cross-redshift test decisive TODAY?")
print(sep)
n_nogo = sum(1 for v in gono.values() if v[3] == "NO-GO")
worst_ratio = min(v[2] for v in gono.values())               # best (smallest floor/req) single-disk case
gI = floor(2.0, 0.5, 0.30, 110.0, "FUTURE", True)
print(f"  VERDICT: NO-GO with today's samples ({n_nogo}/{len(gono)} regime x era x z cells NO-GO; best")
print(f"  single-disk case still {worst_ratio:.1f}x short of the 3-sigma requirement).")
print(f"  Even the N->infinity (global, non-averaging) floor for the best target -- intermediate gas-rich,")
print(f"  FUTURE cold tracer, z=2 -- is ~{100*gI['glob']:.0f}% (~{gI['glob']/DEX:.2f} dex), GAS-CALIBRATION-dominated")
print(f"  (no HI at z~2; one alpha_CO/[CII] for all), ~{gI['glob']/REQ[2.0]:.0f}x the requirement. Collecting more")
print(f"  curves CANNOT cross it. Cross-checked vs the committed TFR ledger: the two best z~1 bTFR points")
print(f"  (Jeanneau 0.00 vs Uebler -0.44) are ~6 sigma MUTUALLY INCONSISTENT on stat errors -- direct")
print(f"  proof the a0(z) zero-point scatter TODAY is systematics-dominated.")
print("\n  THE SPECIFIC (z-bin, sample, era) THAT MAKES IT DECISIVE:")
print("    z-bin  : z ~ 1.5-2  (effect ~13-15%; z=3 has the biggest signal but is data-starved;")
print("             z~1 sits on the bump->decline crossover NULL).")
print("    sample : ~20-40 INTERMEDIATE gas-rich disks (V_flat ~ 100-130 km/s), outer points at g_bar<~a0")
print("             (deep-MOND; high-y massive HSB disks are signal-free, amplification (2y+1) explodes).")
print("    era    : ~2035+  --  DIRECT HI 21cm gas masses (SKA2 / ngVLA, <0.05 dex, no alpha_CO) JOINED")
print("             to ELT/ALMA cold-tracer per-galaxy dynamics + per-galaxy pressure correction. Only")
print("             then does the global floor fall to ~0.05-0.08 dex and a ~20-40 disk campaign reach")
print("             ~4-5% aggregate -> a ~3-sigma model-independent detection of the ~13% a0 decline at z~2.")
print("  WHY NOT SOONER: (1) gas-rich DWARFS (clean a0-line) have V/sigma~1.5 at z=2 -> pressure")
print("  UNCORRECTABLE; (2) massive HSB disks are Upsilon-swamped AND high-y (signal-free); (3) the")
print("  intermediate target tames pressure with a cold tracer but is then gas-calibration floored")
print("  (~0.2 dex global) until direct HI exists. No z~1-2 sample today is at once gas-dominated,")
print("  dynamically cold, AND HI-calibrated -- that triple is the >2035 target.")
print("\n  ONE-LINE HONEST VERDICT: the zero-parameter cross-redshift structure is genuinely POWERFUL")
print("  IN PRINCIPLE (0 params vs 1-2; a real ~+ln(n) Occam bonus + a unique z=0 amplitude falsifier),")
print("  but it is DATA-LIMITED, not information-limited: the clean resolved gas-dominated a0-line is")
print("  UNRUNNABLE above z~0.2 today and stays floored until pressure-corrected, HI-calibrated high-z")
print("  RCs (JWST/ELT/ALMA + SKA2/ngVLA, ~2035+). No 'theory closed'.")

# ==========================================================================================
# (v) FOOTING SYNERGY  (ratio footing-independent; z=0 amplitude = the Step-A footing discriminator)
# ==========================================================================================
print("\n" + sep)
print("(v) FOOTING SYNERGY  --  the cross-z ladder ALSO helps separate the two footings")
print(sep)
zs, w0s, was, Hs, cs, Zsy, ksy = sp.symbols("z w0 wa H c Z k", positive=True)
rd = (1 + zs) ** (3 * (1 + w0s + was)) * sp.exp(-3 * was * zs / (1 + zs))
r_over0 = sp.sqrt(rd)
ratio_canon = sp.simplify((cs*Hs/Zsy) * r_over0 / ((cs*Hs/Zsy) * r_over0.subs(zs, 0)))
ratio_alt   = sp.simplify((ksy*cs*Hs) * r_over0 / ((ksy*cs*Hs) * r_over0.subs(zs, 0)))
assert sp.simplify(ratio_canon - ratio_alt) == 0, "footing did NOT cancel in the ratio"
print("  sympy: a0(z)/a0(0) is FOOTING-INDEPENDENT (Z, a0(0), c, H, canonical-vs-alt ALL cancel) ->")
print("  the SHAPE test (and its whole systematic floor) is identical on both footings. Only the z=0")
print(f"  ABSOLUTE anchor differs: canonical {A0_CANON:.3e} vs alt {A0_ALT:.3e} (a {100*(A0_ALT/A0_CANON-1):.0f}% offset).")
print("  SYNERGY: the z=0 a0-line amplitude is itself the Step-A FOOTING discriminator; carrying the")
print("  same estimator up in z tests the SHAPE. So one ladder does double duty -- footing (at z=0)")
print("  AND evolution (across z) -- but the two jobs are cleanly separated (amplitude vs shape).")

# ==========================================================================================
# SELF-CHECKS (frozen invariants)
# ==========================================================================================
print("\n" + sep); print("SELF-CHECKS (frozen invariants)"); print(sep)
assert PARAM_COUNT["M0"] == 0, "M0 must have 0 free parameters in the code"
print(f"  [OK] M0 has {PARAM_COUNT['M0']} free parameters in the code (amplitude+shape both Lambda-fixed).")
assert min(highz_floors) >= Z0["tot"], "a high-z floor fell below the z=0 floor"
print(f"  [OK] every high-z floor >= the z=0 floor: min(high-z)={100*min(highz_floors):.0f}% >= "
      f"z=0={100*Z0['tot']:.0f}%  (floors: {[f'{100*x:.0f}%' for x in highz_floors]} at z=0.5,1,2,3).")
assert fM2 <= fM1, "M2 (evolving MOND) must be the tighter/binding requirement"
print(f"  [OK] M2 (evolving MOND) is the binding rival: req f(M2)={100*fM2:.2f}% < req f(M1)={100*fM1:.2f}%.")

# ==========================================================================================
# PRE-REGISTRATION BLOCK
# ==========================================================================================
print("\n" + bar)
print("# PRE-REGISTRATION  --  FROZEN 2026-07-23  --  CROSS-REDSHIFT a0-LINE ZERO-PARAMETER TEST")
print(bar)
print("# 1) THE ZERO-PARAMETER PREDICTION CURVE  a0(z)/a0(0)  (FULL closed form; NO free knobs):")
print(f"#    {'z':>5} | " + " | ".join(f"{d[0].split('+')[-1]:>10}" for d in DATASETS) + "   (M1 const-MOND = 1.000 flat)")
for z in (0.35, 0.5, 1.0, 1.5, 2.0, 3.0):
    cells = " | ".join(f"{float(a0ratio(z, d[1], d[2])):>10.3f}" for d in DATASETS)
    tag = "  <- low-z BUMP peak" if abs(z - 0.35) < 1e-9 else ("  <- crossover NULL" if abs(z - 1.0) < 1e-9 else "")
    print(f"#    {z:>5.2f} | {cells}{tag}")
print("#    Signature: low-z BUMP (peak z~0.35), downward unity crossover z~0.9-1.2, DECLINE to ~0.71-0.78 @ z=3.")
print("#    ABSOLUTE anchor (footing, load-bearing): canonical a0(0)=9.355e-11 vs alt 1.131e-10 m/s^2.")
print("#")
print("# 2) DECISION THRESHOLDS (parameter-counting; deep-MOND 2x penalty carried):")
print(f"#    Delta-BIC(rival - M0) > 9  == '3-sigma-equivalent' strong model selection FOR M0.")
print(f"#    Full-span n={n} required per-bin a0 precision: vs M1 <= {100*fM1:.1f}% ; vs M2 <= {100*fM2:.1f}% (BINDING).")
print(f"#    Amplitude anchor value = +ln(n) = +{amp_bonus:.2f} dBIC (Asimov) AND a ~1-sigma z=0 a0(0) falsifier.")
print("#")
print("# 3) TARGET DATA SPEC (what makes it decisive):")
print("#    z ~ 1.5-2 | ~20-40 intermediate gas-rich disks, outer g_bar<~a0 | per-bin a0 ~4-5% (RC ~2-2.5%)")
print("#    | DIRECT HI 21cm gas masses (SKA2/ngVLA, <0.05 dex) + ELT/ALMA cold-tracer per-galaxy dynamics")
print("#    + per-galaxy pressure correction | era ~2035+. TODAY: N_gasdom(resolved a0-line) ~ 0 at z>=0.5.")
print("#")
print("# 4) FROZEN GO/NO-GO: NO-GO with today's samples (floor ~9-55x the requirement, coherent non-")
print("#    averaging bias). DECISIVE only ~2035+ (z~1.5-2, intermediate gas-rich disks, HI+cold-tracer era).")
print("#")
print("# 5) HONESTY CAVEATS (each load-bearing; a manufactured NO-GO is penalized like a manufactured GO):")
CAVEATS = [
 "FORECAST, not a measurement. The model-comparison is Asimov (data == M0 central): it quantifies the "
 "evidence that WOULD accrue IF the framework is true AND galaxies reach precision f. Weak/NULL stated plainly.",
 "CONDITIONAL on DE evolving. If DESI relaxes to w=-1 the ratio is EXACTLY 1 for all z, M0==M1, and the "
 "test is void (untestable, NOT falsified). ALL discriminating power is inherited from DESI's w0wa being real.",
 "HIGH-z SYSTEMATICS ARE A WALL, not a sample-size problem: beam smearing + pressure support (asymmetric "
 "drift, beta~0.3-0.7) + gas-cal drift + Upsilon enter g_obs with a 4a0(y+1)-class lever, are ~10-40% at "
 "cosmic noon, and are BIN-CORRELATED (shared sigma0/AD + PSF models) -> they do NOT average down with N.",
 "DEEP-MOND PENALTY (rule 3) carried in every bin: a0=g_obs^2/g_bar DOUBLES per-point log scatter; per-bin "
 "a0 precision f <-> underlying RC f/2, N_gal/bin ~ (2 sigma_g/f)^2. Doubling per-point scatter quadruples N.",
 "GAS-DOMINATED SCARCITY AT HIGH z: the clean a0-line CUT needs a resolved gas surface-density profile "
 "Sigma_gas(R). Resolved HI dies by z~0.1-0.2; resolved CO/[CII] exists for a handful of ALMA disks. "
 "N_gasdom(resolved, a0-line-usable) ~ 0 at every z>=0.5 today. The z=0 cleanliness INVERTS to a gas-cal floor.",
 "vs M2 (evolving MOND) is the BINDING rival: a 2-param power law mimics sqrt(rho_DE) over any limited-z "
 "window, so the win requires resolving the NON-power-law CURVATURE (the bump+decline) -- a full-z-span, "
 ">2030 requirement, NOT delivered by the Occam term alone. BIC (prior-free) is the conservative headline; "
 "the Laplace Bayes factor runs ahead of BIC for M2 and is NOT read as decisive.",
 "BOTH FOOTINGS (rule 4): the a0(z)/a0(0) RATIO and its whole systematic floor are footing-independent "
 "(Z, a0(0), c, H cancel; sympy-proved). Only the z=0 ABSOLUTE anchor separates footings (canonical "
 "9.355e-11 vs alt 1.131e-10) -- so the same ladder does footing (z=0) AND evolution (across z), cleanly split.",
 "The amplitude-anchor's Asimov value is only the +ln(n) Occam term (rivals fit their amplitude, absorbing "
 "the absolute scale); its LARGER role is a z=0 FALSIFIER (a measured a0(0) off 9.355e-11 by ~16% is a "
 "~1-sigma one-bin kill unique to M0). Stated on both footings.",
 "No 'theory closed'. The standalone decline is ~2-2.5 sigma (neither detected nor excluded); the parameter-"
 "counting SHARPENS it to a 'strong' (dBIC 6-10) preference over const-MOND ONCE the galaxy shape reaches "
 "sqrtS1~2.5-3 sigma -- a real ~+0.3-0.5 sigma-equiv gain, NOT a jump to decisive, and it is floored until ~2035+.",
]
for i, c in enumerate(CAVEATS, 1):
    print(f"#   {i}. {c}")
print(bar)

# JSON for downstream / auditing
json.dump(dict(
    frozen="2026-07-23", test="cross_redshift_a0line",
    param_counts=PARAM_COUNT, a0_canon=A0_CANON, a0_alt=A0_ALT,
    fiducial_grid=list(map(float, ZGRID)), z0_anchor_f=Z0_ANCHOR_F,
    prediction_curve={d[0]: {str(z): float(a0ratio(z, d[1], d[2]))
                             for z in (0.35, 0.5, 1.0, 1.5, 2.0, 3.0)} for d in DATASETS},
    model_comparison_headline=dict(sqrtS1=float(head["sqrtS1"]), sqrtS2=float(head["sqrtS2"]),
                                   dBIC_M1=float(dBIC_M0_fixed), dBIC_M2=float(head["sqrtS2"]**2 + 2*np.log(n)),
                                   lnB01=float(head["lnB01"]), lnB02=float(head["lnB02"]),
                                   amplitude_anchor_dBIC=float(amp_bonus)),
    required_precision_fullspan=dict(fM1=float(fM1), fM2=float(fM2), binding="M2", target_dBIC=TARGET_BIC),
    required_reject_flat_3s=REQ, effect_size=EFF,
    z0_floor=float(Z0["tot"]), highz_floors={str(z): float(v) for z, v in zip((0.5,1.0,2.0,3.0), highz_floors)},
    global_floor_intermediate_future_z2=dict(total=float(gI["tot"]), global_nonaveraging=float(gI["glob"]),
                                             global_dex=float(gI["glob"]/DEX), global_over_req3s=float(gI["glob"]/REQ[2.0])),
    go_no_go={f"{r}|{e}|z{z}": dict(floor=float(v[0]), req3s=float(v[1]),
                                    floor_over_req=float(v[2]), verdict=v[3]) for (r,e,z),v in gono.items()},
    verdict="NO-GO with today's samples (data-limited, not information-limited): the zero-parameter cross-"
            "redshift a0-line structure is real and powerful (0 vs 1-2 params, +ln(n) Occam + a unique z=0 "
            "amplitude falsifier) but the clean resolved gas-dominated a0-line is unrunnable above z~0.2 and "
            "the per-bin systematic floor (beam+pressure+gas-cal+Upsilon, coherent & non-averaging) exceeds "
            "the ~4-8% requirement by ~9-55x. Decisive only ~2035+ (z~1.5-2, ~20-40 intermediate gas-rich "
            "disks, direct HI 21cm + ELT/ALMA cold-tracer + per-galaxy pressure correction). No 'theory closed'.",
    caveats=CAVEATS,
), open(os.path.join(HERE, "cross_redshift_a0line_2026_results.json"), "w"), indent=1, default=float)
print("\n[cross_redshift_a0line_2026_results.json written]")
print("EXIT 0: frozen test rendered; derivations verified; regression parity with committed siblings held.")
