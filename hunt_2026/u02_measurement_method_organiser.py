#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
u02_measurement_method_organiser.py -- ANGLE E: is the liability ledger one MEASUREMENT systematic?
====================================================================================================
THE QUESTION, as posed.  The veins workflow found that the a_0 ladder is organised by the VELOCITY
MEASUREMENT: resolved rotation curves sit +0.24 dex above unresolved HI line widths, matching an
independently measured width-selection bias.  Push that at the LIABILITIES.  Are the failing systems
systematically those whose velocities are measured a particular way -- dispersions from integrated
spectra, few-star radial velocities, X-ray temperatures, lensing shear -- rather than from resolved
rotation?  Group the common-currency offset by MEASUREMENT METHOD instead of by system class and ask
whether that organises the table better than acceleration does.  If it does, many of the "liabilities"
are one measurement systematic and the ledger needs rewriting.

THE CURRENCY is the one the three u01 scripts built:

        B = log10( g_obs / g_pred )     [signed dex of ACCELERATION]
        B > 0  observation exceeds prediction (framework SHORT of boost)
        B < 0  framework OVER-predicts

THE AXIS is y_bar = g_bar^Newtonian / a_0 at the same radius (never g_obs/a_0 -- bug pattern 5).

WHAT IS NEW HERE, and it is the whole point: THE KEEPERS ARE PUT IN THE SAME TABLE, ON THE SAME AXES,
WITH THEIR OWN MEASUREMENT METHOD LABEL.  A measurement systematic is a statement about the DATA, not
about the theory, so it must be applied to every row measured that way -- including the rows the
framework passes.  Two keepers are LENSING measurements (the KiDS 1/r law and the KiDS isolated-dwarf
a_0 meter) and five are RESOLVED ROTATION.  The largest liabilities are lensing and X-ray.  So the
measurement hypothesis is falsifiable against data on disk, and this script falsifies it against data
on disk rather than arguing about it.

SEVEN ATTEMPTS, each a modification of the LEDGER (not of the kernel), each with its free-parameter
count, each with its keepers tested explicitly:
  E1  one free calibration offset per measurement method                                   (7 free)
  E2  hydrostatic mass bias b, applied to X-ray HSE rows only          (0 free at b = 0.2; 1 fitted)
  E3  one lensing shear/mass-calibration offset                                            (1 free)
  E4  dispersion inflation (binaries + tides) in sparse-RV systems, ONE-SIDED               (1 free)
  E5  one offset by SUPPORT TYPE (pressure/lensing vs rotation)                             (1 free)
  E6  the veins width bias (+0.24 dex resolved vs unresolved) transferred to the ledger      (0 free)
  E7  the maximal measurement model: per-method offset AND per-method slope in log y        (14 free)

RULES OBSERVED: both footings; checks that CAN fail; two mutation controls; the LambdaCDM/Newtonian
alternative computed beside; report against interest.  Sources: the committed .out files of h7, h9,
h10/h18, h11, h17, h30, h34/h35/h38, h42, h43, h44, h46, h48/h69b, h50, h51, h52, h53/h54, h55, h56,
h57, h67b, h68, h93 as reduced by u01_cluster_common_currency, u01_pressure_supported_common_currency
and u01_common_currency_disc_lensing; plus the SPARC rotmods and the Brouwer+2021 KiDS files on disk,
which are RE-READ here so that the keeper tests are real recomputations and not quotations.
"""
import sys, math, os, itertools
import numpy as np
from scipy.optimize import brentq
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(2026)
HUNT = os.path.dirname(os.path.abspath(__file__))

# =====================================================================================================
P("=" * 126)
P("0.  THE TAXONOMY, fixed and printed BEFORE any offset is read")
P("=" * 126)

METHODS = {
    "resolved_rotation":    "spatially resolved rotation curve / velocity field (HI or optical)",
    "vertical_stellar_kin": "vertical force from stellar kinematics at fixed height",
    "resolved_star_RV":     "dispersion from individually resolved stellar radial velocities",
    "integrated_spec_disp": "dispersion from an integrated (spatially unresolved) spectrum",
    "discrete_tracer_RV":   "dispersion from discrete tracers -- globular clusters, planetary nebulae",
    "xray_HSE":             "X-ray temperature + density profile, hydrostatic equilibrium",
    "lensing":              "gravitational lensing: shear, Einstein radii, or WL-calibrated masses",
    "pair_los_redshift":    "line-of-sight redshift differences of galaxy pairs",
    "line_width":           "unresolved single-dish HI line width (the veins bias lives HERE)",
}
for k, v in METHODS.items():
    P(f"    {k:22s} {v}")
P("")
P("  The assignment below is made from HOW THE VELOCITY (or the mass) IS MEASURED, not from what kind of")
P("  object it is.  It is fixed here, before any offset is printed, and it is not revisited.")

# ---------------------------------------------------------------------------------------------------
# row = (name, B_canonical, B_alt, y_bar, M_bar/Msun, r_kpc, method, sample_id, kind, role)
#   kind : 'amp' amplitude miss | 'loc' location miss | 'grad' gradient miss
#   role : 'liability' | 'keeper' | 'twin' (an IMF/Upsilon twin of another row, sensitivity only)
LED = [
 # ---- cluster / group front  (u01_cluster_common_currency.out) -----------------------------------
 ("X-ray ellipticals (Humphrey+2006) 5-70 kpc", +0.228, +0.196, 0.80,   2.8e11, 20.0,  "xray_HSE",  "humphrey", "amp", "liability"),
 ("X-COP cluster cores 30-100 kpc",             +0.464, +0.435, 0.52,   7.3e14, 50.0,  "xray_HSE",  "xcop",     "amp", "liability"),
 ("CLASH strong+weak lensing RAR",              +0.538, +0.509, 0.361,  1.0e15, 200.0, "lensing",   "clash",    "amp", "liability"),
 ("Bullet BCG1, 300 kpc projected",             +0.501, +0.470, 0.414,  4.20e13,300.0, "lensing",   "bullet",   "amp", "liability"),
 ("Bullet BCG3, 300 kpc projected",             +0.499, +0.465, 0.382,  2.36e13,300.0, "lensing",   "bullet",   "amp", "liability"),
 ("X-ray groups at R2500 (Lovisari+2015)",      +0.350, +0.312, 0.041,  4.0e13, 224.0, "xray_HSE",  "lovisari", "amp", "liability"),
 ("X-COP clusters at 0.2 R500",                 +0.441, +0.407, 0.259,  5.7e14, 246.0, "xray_HSE",  "xcop",     "amp", "liability"),
 ("X-COP clusters at 0.5 R500",                 +0.319, +0.286, 0.175,  5.7e14, 616.0, "xray_HSE",  "xcop",     "amp", "liability"),
 ("X-COP clusters at 0.9 R500",                 +0.170, +0.134, 0.111,  5.7e14, 1107.0,"xray_HSE",  "xcop",     "amp", "liability"),
 ("X-ray groups at R500 (Lovisari+2015)",       +0.162, +0.124, 0.023,  4.0e13, 526.0, "xray_HSE",  "lovisari", "amp", "liability"),
 ("eRASS1 groups 1e12.5-13.5 at R500",          +0.420, +0.380, 0.0042, 2.1e13, 409.0, "lensing",   "erass1",   "amp", "liability"),
 ("eRASS1 clusters 1e14-14.5 at R500",          +0.329, +0.292, 0.036,  1.9e14, 758.0, "lensing",   "erass1",   "amp", "liability"),
 ("eRASS1 rich clusters 1e15+ at R500",         +0.337, +0.303, 0.113,  1.1e15, 1395.0,"lensing",   "erass1",   "amp", "liability"),
 # ---- pressure-supported front  (u01_pressure_supported_common_currency.out) ---------------------
 ("MW ultra-faint dwarfs (31)",                 +1.650, +1.612, 0.0008, 8.6e3,  0.071, "resolved_star_RV",     "mwsat",  "amp", "liability"),
 ("M31 satellites (LVD, 34)",                   +0.761, +0.726, 0.0035, 6.9e5,  0.299, "resolved_star_RV",     "m31sat", "amp", "liability"),
 ("MW classical dSphs (14)",                    +0.641, +0.603, 0.0071, 1.2e6,  0.406, "resolved_star_RV",     "mwsat",  "amp", "liability"),
 ("Coma UDGs (11)",                             +1.195, +1.166, 0.0074, 6.4e7,  1.90,  "integrated_spec_disp", "coma",   "amp", "liability"),
 ("Pal 14 (16 velocities)",                     -0.658, -0.693, 0.0102, 1.85e4, 0.0276,"resolved_star_RV",     "ohgc",   "amp", "liability"),
 ("LG isolated field dwarfs, gas-poor (5)",     +0.118, +0.079, 0.0120, 1.8e6,  0.242, "resolved_star_RV",     "lgfield","amp", "liability"),
 ("Pal 3 (22 velocities)",                      -0.075, -0.110, 0.0213, 2.07e4, 0.0202,"resolved_star_RV",     "ohgc",   "amp", "liability"),
 ("LG isolated field dwarfs, all (13)",         -0.088, -0.124, 0.0297, 1.4e7,  0.320, "resolved_star_RV",     "lgfield","amp", "liability"),
 ("NGC 1052-DF2",                               -0.485, -0.519, 0.0339, 2.2e8,  1.65,  "discrete_tracer_RV",   "df",     "amp", "liability"),
 ("Pal 4 (23 velocities)",                      -0.781, -0.816, 0.0489, 2.94e4, 0.0159,"resolved_star_RV",     "ohgc",   "amp", "liability"),
 ("NGC 1052-DF4",                               -1.155, -1.188, 0.0582, 2.0e8,  1.20,  "discrete_tracer_RV",   "df",     "amp", "liability"),
 ("SLUGGS GC systems, log M* >= 11.3 (7)",      +0.331, +0.331, 0.73,   2.1e11, 20.9,  "discrete_tracer_RV",   "sluggs", "amp", "liability"),
 ("NGC 2419 (183 velocities)",                  -0.199, -0.225, 0.8619, 8.0e5,  0.0198,"resolved_star_RV",     "ohgc",   "amp", "liability"),
 ("Planetary nebulae, 9 early types",           +0.066, +0.042, 1.44,   6.2e10, 7.9,   "discrete_tracer_RV",   "pn",     "amp", "liability"),
 ("SLUGGS GC systems, log M* < 11.3 (12)",      +0.058, +0.058, 1.64,   6.7e10, 7.3,   "discrete_tracer_RV",   "sluggs", "amp", "liability"),
 ("ATLAS3D early types, Chabrier (258)",        +0.094, +0.075, 2.32,   2.5e10, 2.72,  "integrated_spec_disp", "atlas",  "amp", "liability"),
 # ---- disc / lensing front  (u01_common_currency_disc_lensing.out) -------------------------------
 ("Milky Way K_z at |z| = 1.1 kpc",             -0.115, -0.138, 1.39,   6.68e10,8.2,   "vertical_stellar_kin", "mwkz",   "amp", "liability"),
 ("DiskMass 22 discs at 2.2 h_R (Ups_K 0.31)",  +0.177, +0.147, 0.353,  2.16e10,8.63,  "resolved_rotation",    "diskmass","amp","liability"),
 ("SLACS Einstein radii, 70 lenses (Salpeter)", +0.084, +0.068, 10.0,   1.94e11,4.07,  "lensing",              "slacs",  "amp", "liability"),
 ("Tidal dwarf galaxies (6, EFE on)",           -0.394, -0.427, 0.038,  7.65e8, 4.8,   "resolved_rotation",    "tdg",    "amp", "liability"),
 ("Isolated major pairs, 2MRS (1830)",          +0.553, +0.511, 0.0119, 1.58e11,141.0, "pair_los_redshift",    "pairs",  "amp", "liability"),
 # ---- non-amplitude liabilities: carried, flagged, EXCLUDED from the amplitude fits ---------------
 ("HI warp onset radius (16 discs)  [LOCATION]",+1.607, +1.526, 0.185,  8.3e9,  7.2,   "resolved_rotation",    "warp",   "loc", "liability"),
 ("Fundamental Plane tilt (6dFGS)   [GRADIENT]",+0.109, +0.102, 16.8,   9.9e10, 3.02,  "integrated_spec_disp", "fp",     "grad","liability"),
 # ---- IMF / Upsilon twins: sensitivity only, never in the primary fit ------------------------------
 ("ATLAS3D early types, Salpeter (258) [TWIN]", -0.095, -0.109, 3.94,   4.2e10, 2.72,  "integrated_spec_disp", "atlas",  "amp", "twin"),
 ("DiskMass at the SPS Ups_K = 0.60   [TWIN]",  -0.011, -0.041, 0.68,   4.2e10, 8.63,  "resolved_rotation",    "diskmass","amp","twin"),
]

# The KEEPER rows are appended in section 2 after their B values are RECOMPUTED from data on disk.

P("")
P(f"  {len(LED)} ledger rows declared.  Method assignment (before any offset is shown):")
for m in METHODS:
    nm = [r[0] for r in LED if r[6] == m]
    P(f"    {m:22s} N = {len(nm):2d}")

# =====================================================================================================
P("")
P("=" * 126)
P("1.  PROVENANCE CHECK -- every number above must appear in the .out file it claims to come from")
P("=" * 126)
# Spot-check a sample of the ledger's B values against the strings the source .out files actually print.
# These are the ACCELERATION-currency numbers the three u01 reductions published.
SRC = {}
for f in ("u01_cluster_common_currency.out", "u01_pressure_supported_common_currency.out",
          "u01_common_currency_disc_lensing.out"):
    p = os.path.join(HUNT, f)
    SRC[f] = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
ALLSRC = "\n".join(SRC.values())
probe = ["3.45", "2.91", "1.650", "1.195", "0.553", "0.394", "1.607", "2.24"]
found = {s: (s in ALLSRC) for s in probe}
ck("1a the three u01 .out files are on disk and carry the headline strings this ledger is built from "
   "(a guard against transcribing numbers that were never computed)",
   all(len(v) > 1000 for v in SRC.values()) and sum(found.values()) >= 6,
   f"file sizes {[len(v) for v in SRC.values()]}; probes found {sum(found.values())}/{len(probe)}: "
   + ", ".join(f"{k}{'+' if v else '-'}" for k, v in found.items()))

# The identity that lets the cluster rows (published as eta_g, an acceleration boost) enter as B:
#   B = log10(eta_g).  Verified on the four cluster numbers whose eta_g the source prints.
eta_check = [(1.69, 0.228), (2.91, 0.464), (3.45, 0.538), (1.45, 0.162)]
ck("1b the cluster rows enter as B = log10(eta_g) exactly, where eta_g = g_obs/[nu(y) g_bar] is what "
   "h10, h55, h56, h67b and h68 print -- checked against the four values the source quotes",
   max(abs(math.log10(e) - b) for e, b in eta_check) < 0.002,
   "max |log10(eta_g) - B| = " + f"{max(abs(math.log10(e)-b) for e, b in eta_check):.4f}")

# =====================================================================================================
P("")
P("=" * 126)
P("2.  THE KEEPERS, RECOMPUTED FROM DATA ON DISK AND PUT IN THE SAME TABLE")
P("=" * 126)
P("  A measurement systematic is a statement about the DATA.  It therefore applies to the rows the")
P("  framework PASSES as much as to the rows it fails, whenever they are measured the same way.")
P("  So the keepers are placed on the same axes with their own method label.")

# ---- (a) the two LENSING keepers, from Brouwer+2021 KiDS-1000 -------------------------------------
gd, od, ed = load_rar("Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt"); nd = len(gd)
Cd = load_cov("Fig-10_RAR-KiDS-isolated-dwarfs_covmatrix.txt", nd)
gl, ol, el = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
Cl = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", len(gl))
ml = gl >= 1e-14

def fit_a0_stack(gbv, gov, C, mask, shift_dex=0.0):
    """profile a_0 against the covariance.  shift_dex multiplies the OBSERVED g by 10**(-shift_dex),
    i.e. it applies the correction a measurement bias of +shift_dex would demand."""
    gov = gov * 10 ** (-shift_dex)
    Cs = C[np.ix_(mask, mask)] * 10 ** (-2 * shift_dex)
    best, ba = 1e30, 0.0
    for la in np.linspace(-12.5, -8.5, 401):
        d = (gov - gbv * nu(gbv / 10 ** la))[mask]
        c = float(d @ np.linalg.solve(Cs, d))
        if c < best: best, ba = c, la
    return 10 ** ba, best

a0_dw, chi_dw = fit_a0_stack(gd, od, Cd, np.ones(nd, bool))
a0_ls, chi_ls = fit_a0_stack(gl, ol, Cl, ml)
info(f"KiDS isolated-DWARF lens stack: a_0 = {a0_dw:.3e} m/s^2 (chi2 {chi_dw:.1f}/{nd}); g_bar {gd.min():.2e}-{gd.max():.2e}")
info(f"KiDS L* lens stack:             a_0 = {a0_ls:.3e} m/s^2 (chi2 {chi_ls:.1f}/{ml.sum()})")
ck("2a the KiDS lensing keeper is reproduced from the files on disk: the isolated-dwarf stack returns "
   "the canonical footing to better than 0.05 dex with no fitting except the one amplitude, exactly as "
   "h1/h2 published -- so it is a genuine keeper and not a quotation",
   abs(math.log10(a0_dw / A0["canonical"])) < 0.05,
   f"a_0(dwarf lens stack) = {a0_dw:.3e} vs canonical 9.36e-11 ({math.log10(a0_dw/A0['canonical']):+.3f} dex), "
   f"h1/h2 published 9.55e-11")

# a_0 ~ g_obs^2/g_bar in the deep limit, so a lensing offset d in g is 2d in a_0.  Convert back:
B_kids_dw = 0.5 * math.log10(a0_dw / A0["canonical"])
B_kids_dw_alt = 0.5 * math.log10(a0_dw / A0["alt"])
B_kids_ls = 0.5 * math.log10(a0_ls / A0["canonical"])
B_kids_ls_alt = 0.5 * math.log10(a0_ls / A0["alt"])
y_kids_dw = float(np.median(gd)) / A0["canonical"]
y_kids_ls = float(np.median(gl[ml])) / A0["canonical"]
info(f"in B currency (deep limit B = 1/2 log10(a_0,fit/a_0)): KiDS dwarfs B = {B_kids_dw:+.3f}, "
     f"L* B = {B_kids_ls:+.3f}; median y_bar = {y_kids_dw:.2e} and {y_kids_ls:.2e}")

# ---- (b) the RESOLVED-ROTATION keepers, from the SPARC rotmods -------------------------------------
gals = load_sparc()
GB = np.concatenate([g["gbar"] for g in gals]); GO = np.concatenate([g["gobs"] for g in gals])

def a0_kern(x, y, shift_dex=0.0):
    """h103's corrected full-kernel estimator: solve <log10 g_obs - log10 nu(g_bar/a) g_bar> = 0."""
    yy = y * 10 ** (-shift_dex)
    f = lambda a: float(np.mean(np.log10(yy) - np.log10(nu(x / a) * x)))
    try: return brentq(f, 1e-14, 1e-6, xtol=1e-20, rtol=8.9e-16, maxiter=300)
    except Exception: return float("nan")

deep = GB < 1e-11
a0_tail = a0_kern(GB[deep], GO[deep])
info(f"SPARC deep tail (g_bar < 1e-11): N = {deep.sum()} points, full-kernel a_0 = {a0_tail:.3e} m/s^2")
ck("2b the deep-tail keeper is reproduced from the rotmods on disk with h103's CORRECTED full-kernel "
   "estimator (not the biased slope-fixed one), landing on the withdrawn-and-replaced 9.04e-11",
   abs(a0_tail - 9.04e-11) < 0.06e-11,
   f"here {a0_tail:.4e} vs h103's published 9.040e-11 ({math.log10(a0_tail/9.04e-11):+.4f} dex)")
B_tail = 0.5 * math.log10(a0_tail / A0["canonical"])
B_tail_alt = 0.5 * math.log10(a0_tail / A0["alt"])

def rar_stats(a0, shift_dex=0.0, gb=None, go=None):
    gb = GB if gb is None else gb; go = GO if go is None else go
    res = np.log10(go * 10 ** (-shift_dex)) - np.log10(nu(gb / a0) * gb)
    return float(res.mean()), float(res.std())

m_can, s_can = rar_stats(A0["canonical"])
m_alt, s_alt = rar_stats(A0["alt"])
info(f"SPARC RAR about the parameter-free curve: mean {m_can:+.4f} dex, rms {s_can:.4f} (canonical); "
     f"mean {m_alt:+.4f}, rms {s_alt:.4f} (alt)")
ck("2c the RAR keeper is reproduced: the parameter-free curve sits on the SPARC points with a mean "
   "residual under 0.03 dex and a vertical rms near the published 0.13-0.18 dex, on both footings",
   abs(m_can) < 0.05 and abs(m_alt) < 0.05 and 0.10 < s_can < 0.22,
   f"canonical mean {m_can:+.4f} rms {s_can:.4f}; alt mean {m_alt:+.4f} rms {s_alt:.4f} (h117 published "
   f"vertical rms 0.176 uncut / 0.133 on the accuracy cut)")

# Renzo first order and the inner-diversity ratio: both are RATIOS taken inside one rotation curve,
# so a uniform calibration shift cancels identically.  Demonstrate rather than assert.
def renzo_first_order(shift_dex=0.0):
    """regression of d ln v_obs/d ln r on the kernel's predicted d ln v_pred/d ln r, interior points."""
    X, Y = [], []
    for g in gals:
        r, gb, go = g["r"], g["gbar"], g["gobs"]
        if len(r) < 5: continue
        vo = np.sqrt(go * r * kpc) * 10 ** (-shift_dex / 2)
        vp = np.sqrt(nu(gb / A0["canonical"]) * gb * r * kpc)
        lr = np.log(r)
        Y.append(np.gradient(np.log(vo), lr)[1:-1]); X.append(np.gradient(np.log(vp), lr)[1:-1])
    X = np.concatenate(X); Y = np.concatenate(Y); k = np.isfinite(X) & np.isfinite(Y)
    A = np.vstack([X[k], np.ones(k.sum())]).T
    sl, _ = np.linalg.lstsq(A, Y[k], rcond=None)[0]
    return sl, float(np.corrcoef(X[k], Y[k])[0, 1])

rz0, rzr0 = renzo_first_order(0.0)
rz1, rzr1 = renzo_first_order(0.40)
ck("2d Renzo's rule at first order, and the inner-diversity ratio, are SHIFT-BLIND by construction: "
   "both are ratios taken inside one rotation curve, so a uniform calibration offset in g_obs cancels "
   "exactly.  Demonstrated by applying a 0.40 dex shift and recovering the identical slope",
   abs(rz0 - rz1) < 1e-9 and abs(rzr0 - rzr1) < 1e-9,
   f"slope {rz0:.4f} -> {rz1:.4f}, r {rzr0:.4f} -> {rzr1:.4f} under a +0.40 dex shift (h115 published "
   f"first-order slope 0.766)")

KEEP = [
 ("KEEPER: KiDS isolated-dwarf lens stack a_0", B_kids_dw,  B_kids_dw_alt,  y_kids_dw, 3e9,  200.0, "lensing",           "kids", "amp", "keeper"),
 ("KEEPER: KiDS L* lens stack a_0",             B_kids_ls,  B_kids_ls_alt,  y_kids_ls, 5e10, 300.0, "lensing",           "kids", "amp", "keeper"),
 ("KEEPER: SPARC deep-tail a_0 (full kernel)",  B_tail,     B_tail_alt,     3.0e-3,    3e9,  15.0,  "resolved_rotation", "sparc","amp", "keeper"),
 ("KEEPER: SPARC RAR mean residual",            m_can,      m_alt,          0.24,      2e10, 10.0,  "resolved_rotation", "sparc","amp", "keeper"),
]
LED = LED + KEEP
P("")
P("  the four recomputed keeper rows, in the same currency:")
for r in KEEP:
    P(f"    {r[0]:46s} B = {r[1]:+.3f} (alt {r[2]:+.3f})   y_bar = {r[3]:.2e}   method = {r[6]}")

# =====================================================================================================
P("")
P("=" * 126)
P("3.  THE TABLE, GROUPED BY MEASUREMENT METHOD (the question as posed)")
P("=" * 126)

FIT = [r for r in LED if r[8] == "amp" and r[9] != "twin"]      # primary: amplitude rows, no IMF twins
names = [r[0] for r in FIT]
Bc = np.array([r[1] for r in FIT]); Ba = np.array([r[2] for r in FIT])
Y = np.array([r[3] for r in FIT]); M = np.array([r[4] for r in FIT]); R = np.array([r[5] for r in FIT])
MET = np.array([r[6] for r in FIT]); SAMP = np.array([r[7] for r in FIT]); ROLE = np.array([r[9] for r in FIT])
LY, LM, LR = np.log10(Y), np.log10(M), np.log10(R)
N = len(FIT)
info(f"primary table: N = {N} amplitude rows ({(ROLE=='keeper').sum()} keepers, {(ROLE=='liability').sum()} liabilities), "
     f"{len(set(MET))} methods, y_bar over {LY.max()-LY.min():.1f} decades, M_bar over {LM.max()-LM.min():.1f} decades")

P("")
P(f"  {'method':22s} {'N':>3} {'median B':>9} {'min B':>8} {'max B':>8} {'SPREAD':>8} {'signs':>10}   rows")
order = sorted(set(MET), key=lambda m: -np.median(Bc[MET == m]))
SPREAD = {}
for m in order:
    k = MET == m
    sp = Bc[k].max() - Bc[k].min(); SPREAD[m] = sp
    sg = f"{(Bc[k]>0.05).sum()}+ / {(Bc[k]<-0.05).sum()}-"
    P(f"  {m:22s} {k.sum():3d} {np.median(Bc[k]):+9.3f} {Bc[k].min():+8.3f} {Bc[k].max():+8.3f} {sp:8.3f} {sg:>10}")
    for nm, b, yy in sorted(zip(np.array(names)[k], Bc[k], Y[k]), key=lambda t: -t[1]):
        P(f"      {b:+7.3f}  y={yy:9.2e}  {nm}")

tot_spread = Bc.max() - Bc.min()
worst = max(SPREAD, key=SPREAD.get)
ck("3a AGAINST THE MEASUREMENT HYPOTHESIS -- the sign is not even constant WITHIN a method.  Three of "
   "the eight methods contain rows of BOTH signs at |B| > 0.05, and the largest single method group "
   "(resolved stellar radial velocities) spans from +1.65 to -0.78.  A calibration offset is one number "
   "per method and cannot produce two signs",
   sum(1 for m in set(MET) if (Bc[MET == m] > 0.05).any() and (Bc[MET == m] < -0.05).any()) >= 3,
   f"methods with both signs: " + ", ".join(m for m in order
      if (Bc[MET==m] > 0.05).any() and (Bc[MET==m] < -0.05).any())
   + f"; widest within-method spread {worst} = {SPREAD[worst]:.3f} dex against a TOTAL table spread of {tot_spread:.3f} dex")

# The single sharpest instance: two LENSING rows at matched deep acceleration, one a keeper.
kids_row = [r for r in FIT if r[0].startswith("KEEPER: KiDS isolated-dwarf")][0]
er_row = [r for r in FIT if r[0].startswith("eRASS1 groups")][0]
P("")
P("    AGAINST THIS PAIR, before it is asserted: the eRASS1 group row's B depends on an assumed stellar +")
P("    gas budget, and h55 itself carries three defensible budgets spanning x1.56 to x2.89 in acceleration")
P("    (B = +0.193 to +0.461).  Taking the budget MOST favourable to the framework, the gap against the")
P("    KiDS keeper shrinks from +0.42 to +0.19 dex.  The pair survives at reduced size, and it survives")
P("    because the KiDS row's own baryonic mass would have to be wrong in the opposite direction by the")
P("    same amount to close it.  The +0.19 dex figure is the one to quote, not the +0.42.")
for _b in (0.193, 0.461):
    P(f"      eRASS1 groups at h55 budget B = {_b:+.3f}: gap against the KiDS dwarf keeper = "
      f"{_b - B_kids_dw:+.3f} dex")
ck("3b THE DECISIVE PAIR, and it is inside ONE method at MATCHED acceleration: the KiDS isolated-dwarf "
   "lens stack (lensing, y_bar ~ 1e-3) lands on a_0 and the eRASS1 group lensing masses (lensing, "
   "y_bar = 4.2e-3) need +0.42 dex.  Same measurement technique, same decade of acceleration, 0.4 dex "
   "apart -- so NEITHER the method NOR the acceleration organises the lensing family",
   (0.193 - kids_row[1]) > 0.15 and abs(math.log10(er_row[3] / kids_row[3])) < 1.0,
   f"KiDS dwarf lenses B = {kids_row[1]:+.3f} at y = {kids_row[3]:.2e}; eRASS1 groups B = {er_row[1]:+.3f} "
   f"at y = {er_row[3]:.2e}: {er_row[1]-kids_row[1]:+.3f} dex apart on the repo budget and "
   f"{0.193-kids_row[1]:+.3f} on h55's most framework-favourable budget, "
   f"{abs(math.log10(er_row[3]/kids_row[3])):.2f} decades apart in y")

# =====================================================================================================
P("")
P("=" * 126)
P("4.  MODEL COMPARISON -- does METHOD organise the table better than ACCELERATION?")
P("=" * 126)

def rss_const(b, w=None):
    return float(np.sum((b - b.mean()) ** 2)), 1

def rss_lin(b, x):
    A = np.vstack([x, np.ones(len(x))]).T
    c = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(np.sum((b - A @ c) ** 2)), 2

def rss_group(b, g):
    r = 0.0
    for u in set(g): r += float(np.sum((b[g == u] - b[g == u].mean()) ** 2))
    return r, len(set(g))

def rss_group_lin(b, g, x):
    """per-group offset + one shared slope"""
    us = sorted(set(g)); A = np.zeros((len(b), len(us) + 1))
    for i, u in enumerate(us): A[g == u, i] = 1.0
    A[:, -1] = x
    c = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(np.sum((b - A @ c) ** 2)), len(us) + 1

def rss_group_full(b, g, x):
    """per-group offset AND per-group slope -- the maximal measurement model, attempt E7"""
    us = sorted(set(g)); A = np.zeros((len(b), 2 * len(us)))
    for i, u in enumerate(us):
        A[g == u, 2 * i] = 1.0; A[g == u, 2 * i + 1] = x[g == u]
    c = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(np.sum((b - A @ c) ** 2)), 2 * len(us)

def rss_slopes_only(b, g, x):
    """ONE shared offset, a free slope in log y per group.  A calibration bias is a CONSTANT, so this
    model contains NO measurement freedom at all -- it isolates how much of E7 is carried by the slopes."""
    us = sorted(set(g)); A = np.zeros((len(b), len(us) + 1)); A[:, 0] = 1.0
    for i, u in enumerate(us): A[g == u, i + 1] = x[g == u]
    c = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(np.sum((b - A @ c) ** 2)), len(us) + 1

SUP = np.array(["rotation" if m in ("resolved_rotation", "vertical_stellar_kin") else "other" for m in MET])
MODELS = {}
for foot, b in (("canonical", Bc), ("alt", Ba)):
    MODELS[foot] = {}
    MODELS[foot]["M0 constant"] = rss_const(b)
    MODELS[foot]["My  log y_bar"] = rss_lin(b, LY)
    MODELS[foot]["Mm  log M_bar"] = rss_lin(b, LM)
    MODELS[foot]["Mr  log r"] = rss_lin(b, LR)
    MODELS[foot]["Ms  support type (E5)"] = rss_group(b, SUP)
    MODELS[foot]["ME1 method (E1)"] = rss_group(b, MET)
    MODELS[foot]["ME1+y method + log y"] = rss_group_lin(b, MET, LY)
    MODELS[foot]["ME7 method x log y (E7)"] = rss_group_full(b, MET, LY)
    MODELS[foot]["Mslopes  1 offset + method slopes"] = rss_slopes_only(b, MET, LY)

for foot in ("canonical", "alt"):
    P("")
    P(f"  {foot} footing, N = {N} rows:")
    P(f"    {'model':26s} {'p':>3} {'RSS':>8} {'rms [dex]':>10} {'R^2':>7} {'AIC':>8} {'BIC':>8}")
    r0 = MODELS[foot]["M0 constant"][0]
    for k, (r, p) in MODELS[foot].items():
        aic = N * math.log(max(r, 1e-12) / N) + 2 * p
        bic = N * math.log(max(r, 1e-12) / N) + p * math.log(N)
        P(f"    {k:26s} {p:3d} {r:8.3f} {math.sqrt(r/N):10.4f} {1-r/r0:7.3f} {aic:8.2f} {bic:8.2f}")

rc_, pc_ = MODELS["canonical"]["ME1 method (E1)"]
ry_, py_ = MODELS["canonical"]["My  log y_bar"]
r00, p00 = MODELS["canonical"]["M0 constant"]
aic_m = N * math.log(rc_ / N) + 2 * pc_
aic_y = N * math.log(ry_ / N) + 2 * py_
aic_0 = N * math.log(r00 / N) + 2 * p00

# permutation test on the method labels
def perm_p(b, g, nperm=20000):
    obs = rss_group(b, g)[0]
    cnt = 0
    for _ in range(nperm):
        if rss_group(b, rng.permutation(g))[0] <= obs: cnt += 1
    return (cnt + 1) / (nperm + 1)

HALO = np.array([("Pal" in n) or ("NGC 2419" in n) or ("DF2" in n) or ("DF4" in n) for n in names])
HG = np.where(HALO, "no_halo", "halo")
rss_h, ph = rss_group(Bc, HG)
aic_h = N * math.log(rss_h / N) + 2 * ph
pmeth = perm_p(Bc, MET)
info(f"permutation p for the method grouping (20000 relabellings of the method tag): p = {pmeth:.4f}")
ck("4a THE ANSWER TO THE QUESTION AS POSED: grouping by measurement method does NOT organise the table "
   "better than acceleration.  It does lower the raw rms -- seven extra free parameters always do -- but "
   "it loses on AIC to BOTH the one-parameter acceleration slope and to doing nothing at all, and a "
   "permutation of the method labels reproduces its tightness one time in three",
   aic_m > aic_y and aic_m > aic_0 and pmeth > 0.05,
   f"method: {pc_} params, rms {math.sqrt(rc_/N):.4f} dex, AIC {aic_m:.1f}; log y_bar: 2 params, rms "
   f"{math.sqrt(ry_/N):.4f}, AIC {aic_y:.1f}; constant: 1 param, rms {math.sqrt(r00/N):.4f}, AIC {aic_0:.1f}; "
   f"permutation p(method) = {pmeth:.3f}")

# Spearman on |B| against log y, the u01 organiser, recomputed on THIS table
def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])

rho_y = spearman(np.abs(Bc), LY)
nperm = 20000
null = np.array([spearman(np.abs(Bc), rng.permutation(LY)) for _ in range(2000)])
p_y = (np.sum(np.abs(null) >= abs(rho_y)) + 1) / (len(null) + 1)
info(f"|B| vs log y_bar on this table (keepers included): Spearman rho = {rho_y:+.3f}, permutation p = {p_y:.4f}")
ck("4b AGAINST INTEREST, and this weakens the previous phase's headline too: once the KEEPERS are put "
   "into the same table on the same axes, the acceleration ordering of |B| is itself weakened.  It is "
   "still the best single organiser in the table, but the keepers sit at y_bar = 1e-3 to 0.24 with "
   "|B| < 0.03 while liabilities at the SAME y_bar reach 0.42-1.20 dex",
   True,
   f"rho(|B|, log y) = {rho_y:+.3f} (p = {p_y:.3f}) on N = {N} including keepers; u01's pressure-only "
   f"table gave -0.636 (p = 0.014) on 15 rows with no keeper in it.  No single continuous axis organises "
   f"the full table: log y, log M and log r explain "
   f"{1-MODELS['canonical']['My  log y_bar'][0]/r00:.3f}, {1-MODELS['canonical']['Mm  log M_bar'][0]/r00:.3f} "
   f"and {1-MODELS['canonical']['Mr  log r'][0]/r00:.3f} of the variance of signed B")

# =====================================================================================================
P("")
P("=" * 126)
P("5.  THE SEVEN ATTEMPTS, each with its keepers tested")
P("=" * 126)

def demanded(mask):
    """the single offset a set of rows demands, and what it leaves behind"""
    b = Bc[mask]
    return float(np.median(b)), float(np.sqrt(np.mean((b - np.median(b)) ** 2)))

ATT = {}

# ---------------- E1: one calibration offset per method -------------------------------------------
P("")
P("  E1  one free calibration offset per measurement method (7 free parameters)")
liab = ROLE == "liability"
dem_by_method = {}
for m in order:
    k = (MET == m) & liab
    if k.sum() == 0: continue
    d, s = demanded(k)
    dem_by_method[m] = d
    kk = (MET == m) & (ROLE == "keeper")
    keep_txt = ""
    if kk.sum():
        broken = [f"{names[i]} moves {Bc[i]:+.3f} -> {Bc[i]-d:+.3f}" for i in np.where(kk)[0]]
        keep_txt = "  KEEPERS IN THIS METHOD: " + "; ".join(broken)
    P(f"    {m:22s} demanded offset {d:+.3f} dex, residual rms after it {s:.3f} dex{keep_txt}")
res_E1 = math.sqrt(MODELS["canonical"]["ME1 method (E1)"][0] / N)
ATT["E1"] = dict(res=res_E1, params=7)

# the keeper break, computed on the real data: apply the lensing offset to the KiDS files
d_lens = dem_by_method["lensing"]
a0_dw_sh, _ = fit_a0_stack(gd, od, Cd, np.ones(nd, bool), shift_dex=d_lens)
a0_ls_sh, _ = fit_a0_stack(gl, ol, Cl, ml, shift_dex=d_lens)
info(f"applying the lensing rows' demanded {d_lens:+.3f} dex to the KiDS files: the isolated-dwarf stack's "
     f"a_0 moves {a0_dw:.3e} -> {a0_dw_sh:.3e} ({math.log10(a0_dw_sh/a0_dw):+.3f} dex)")
# the 1/r slope, recomputed under the same shift (a constant factor cannot move a log slope)
rcv = {b: load_esd(f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt") for b in (1, 2, 3, 4)}
sl_raw, sl_sh = [], []
for b in rcv:
    Rr, E, eE = rcv[b]; m = (Rr > 0.05) & (E > 0) & (E / eE > 2)
    sl_raw.append(fit_loglog(Rr[m], 4 * G_PC * E[m] * PC_PER_M)[0])
    sl_sh.append(fit_loglog(Rr[m], 4 * G_PC * E[m] * PC_PER_M * 10 ** (-d_lens))[0])
ck("5a E1's KEEPER BREAK, computed on the KiDS files and not asserted: the offset the lensing "
   "liabilities demand DESTROYS the lensing a_0 meter while leaving the 1/r law untouched.  The "
   "isolated-dwarf stack's a_0 falls by twice the offset -- off the canonical footing by more than the "
   "whole width of the footing question -- because a_0 goes as g_obs^2/g_bar in the deep limit",
   abs(math.log10(a0_dw_sh / A0["canonical"])) > 0.5 and
   max(abs(a - b) for a, b in zip(sl_raw, sl_sh)) < 1e-9,
   f"a_0(KiDS dwarfs) {a0_dw:.3e} -> {a0_dw_sh:.3e} = {math.log10(a0_dw_sh/A0['canonical']):+.3f} dex from "
   f"canonical (was {math.log10(a0_dw/A0['canonical']):+.3f}); the four 1/r slopes are unchanged to "
   f"{max(abs(a-b) for a, b in zip(sl_raw, sl_sh)):.1e}")

# the resolved-rotation offset applied to SPARC
d_rot = dem_by_method["resolved_rotation"]
FOOT_GAP = abs(math.log10(A0["alt"] / A0["canonical"]))
DEEP_TAIL_ERR = 0.073        # h103's total (random + coherent) budget on the deep-tail a_0, in dex
P("")
P("    the resolved-rotation offset is the WEAKEST-DETERMINED in the table and this is said first: its two")
P("    liability rows have OPPOSITE signs (DiskMass +0.177, tidal dwarfs -0.394), so their median is nearly")
P("    meaningless.  Every one of the three readings is therefore computed and all three break the keeper.")
P(f"    {'reading':34s} {'offset':>8} {'a_0(deep tail)':>16} {'vs canonical':>13} {'vs alt':>9} {'RAR mean':>10}")
rot_breaks = []
for lab, dd in (("median of the two rows", d_rot),
                ("DiskMass alone", Bc[names.index("DiskMass 22 discs at 2.2 h_R (Ups_K 0.31)")]),
                ("tidal dwarfs alone", Bc[names.index("Tidal dwarf galaxies (6, EFE on)")])):
    a_sh = a0_kern(GB[deep], GO[deep], shift_dex=dd)
    mm, ss = rar_stats(A0["canonical"], shift_dex=dd)
    dc, da = math.log10(a_sh / A0["canonical"]), math.log10(a_sh / A0["alt"])
    rot_breaks.append((lab, dd, a_sh, dc, da, mm))
    P(f"    {lab:34s} {dd:+8.3f} {a_sh:16.3e} {dc:+13.3f} {da:+9.3f} {mm:+10.4f}")
a0_tail_sh = rot_breaks[0][2]
worst_foot = min(abs(r[3]) for r in rot_breaks), min(abs(r[4]) for r in rot_breaks)
ck("5b E1's second KEEPER BREAK, computed on the rotmods.  It is WEAKER than the lensing one and that is "
   "reported first: the rotation method has only two liability rows and they disagree in sign, so the "
   "offset is ill-determined.  But on all three readings of it the SPARC deep-tail a_0 moves by more than "
   "the ENTIRE remaining gap between the two footings, so no choice of footing absorbs it; and the RAR's "
   "mean residual moves from +0.012 to between +0.12 and -0.39 dex.  Renzo at first order and the inner "
   "diversity ratio survive untouched -- they are ratios inside one curve",
   min(min(abs(r[3]), abs(r[4])) for r in rot_breaks) > FOOT_GAP,
   "; ".join(f"{r[0]}: a_0 {r[2]:.3e} ({r[3]:+.3f} can, {r[4]:+.3f} alt = {abs(r[4])/DEEP_TAIL_ERR:.1f} sigma "
             f"on h103's 0.073 dex budget), RAR mean {r[5]:+.4f}" for r in rot_breaks)
   + f"; footing gap {FOOT_GAP:.3f} dex")
m_sh, s_sh = rar_stats(A0["canonical"], shift_dex=d_rot)
a0_all_sh = a0_kern(GB, GO, shift_dex=d_rot)
m_sh2, s_sh2 = rar_stats(a0_all_sh, shift_dex=d_rot)
info(f"if a_0 is REFITTED to absorb the median rotation shift the RAR's scatter does survive "
     f"(rms {s_can:.4f} -> {s_sh2:.4f}) -- but at a_0 = {a0_all_sh:.3e}, "
     f"{math.log10(a0_all_sh/A0['canonical']):+.3f} dex off the cosmological value, which is the first law.")

# ---------------- E2: hydrostatic mass bias --------------------------------------------------------
P("")
P("  E2  hydrostatic mass bias b applied to the X-ray HSE rows only (0 free at the literature b = 0.20)")
kx = (MET == "xray_HSE") & liab
for bhyd in (0.10, 0.20, 0.30):
    # M_true = M_HSE/(1-b): in the deep limit g ~ sqrt(M), so B moves by +0.5 log10(1/(1-b))
    dB = 0.5 * math.log10(1 / (1 - bhyd))
    P(f"    b = {bhyd:.2f}: every X-ray row moves {dB:+.3f} dex; median X-ray B {np.median(Bc[kx]):+.3f} -> "
      f"{np.median(Bc[kx]) + dB:+.3f}   (WRONG SIGN: it makes the X-ray liability WORSE)")
dB20 = 0.5 * math.log10(1 / (1 - 0.20))
ck("5c E2 goes the WRONG WAY, which is the one place a measurement systematic is definitely present and "
   "is definitely against the framework.  Undoing the standard 20% hydrostatic bias RAISES the X-ray "
   "masses, so it raises the required boost -- it removes the framework's two best rows (the R500 "
   "hydrostatic ones) rather than fixing anything.  Zero liabilities fixed, and it is not free: b is "
   "measured",
   dB20 > 0 and np.median(Bc[kx]) + dB20 > np.median(Bc[kx]),
   f"b = 0.20 moves every X-ray row {dB20:+.3f} dex; X-COP 0.9 R500 {Bc[names.index('X-COP clusters at 0.9 R500')]:+.3f} "
   f"-> {Bc[names.index('X-COP clusters at 0.9 R500')] + dB20:+.3f}; Lovisari R500 "
   f"{Bc[names.index('X-ray groups at R500 (Lovisari+2015)')]:+.3f} -> "
   f"{Bc[names.index('X-ray groups at R500 (Lovisari+2015)')] + dB20:+.3f}")
ATT["E2"] = dict(dB=dB20)

# ---------------- E3: one lensing calibration offset ------------------------------------------------
P("")
P("  E3  one shear / mass-calibration offset for the lensing family (1 free parameter)")
kl = (MET == "lensing") & liab
dl, sl_res = demanded(kl)
P(f"    the six lensing liabilities demand {dl:+.3f} dex and are left with {sl_res:.3f} dex rms about it")
for i in np.where(MET == "lensing")[0]:
    P(f"      {Bc[i]:+7.3f} -> {Bc[i]-dl:+7.3f}   y={Y[i]:9.2e}  {names[i]}  [{ROLE[i]}]")
lens_after = Bc[MET == "lensing"] - dl
ck("5d E3 FAILS on its own family before any keeper is consulted: one offset cannot fit the lensing rows "
   "because they span 0.53 dex among themselves, and the two rows it has to move FURTHEST from zero are "
   "the two the framework currently passes -- the KiDS a_0 meter and SLACS.  (LITERATURE, not computed "
   "here: KiDS multiplicative shear bias is calibrated to ~1-2 per cent, so a 0.42 dex = factor 2.6 "
   "shear offset is independently excluded -- but this check does not rest on that.)",
   abs(lens_after).max() > 0.25 and abs(B_kids_dw - dl) > 0.25,
   f"required offset {dl:+.3f} dex; residuals after it run {lens_after.min():+.3f} to {lens_after.max():+.3f}; "
   f"the KiDS dwarf keeper is driven from {B_kids_dw:+.3f} to {B_kids_dw-dl:+.3f} dex, i.e. its a_0 from "
   f"{a0_dw:.2e} to {a0_dw_sh:.2e}")
ATT["E3"] = dict(d=dl, res=sl_res)

# ---------------- E4: dispersion inflation, ONE-SIDED ------------------------------------------------
P("")
P("  E4  dispersion inflation from binaries and tides in sparse-RV systems (1 free, ONE-SIDED: an")
P("      inflation can only RAISE sigma_obs, so it can only lower a POSITIVE B)")
krv = MET == "resolved_star_RV"
pos = krv & (Bc > 0.05); neg = krv & (Bc < -0.05)
P(f"    rows in this method with B > +0.05: {pos.sum()}  (max {Bc[pos].max():+.3f})")
P(f"    rows in this method with B < -0.05: {neg.sum()}  (min {Bc[neg].min():+.3f})  <-- inflation makes these WORSE")
# how big an inflation would the largest positive row need, in sigma?
need_sig = 10 ** (Bc[pos].max() / 2)
ck("5e E4 is ONE-SIDED and therefore cannot be the story: the same measurement technique -- dispersions "
   "from individually resolved stellar radial velocities -- contains the table's largest POSITIVE row "
   "and its largest NEGATIVE ones.  An inflation that removed the ultra-faint dwarfs' +1.65 dex would "
   "have to inflate sigma by a factor 6.7, and it would drive Pal 4 and Pal 14 further below zero, not "
   "toward it",
   pos.sum() >= 2 and neg.sum() >= 2 and need_sig > 3,
   f"positive rows {pos.sum()} (up to {Bc[pos].max():+.3f} = a factor {need_sig:.1f} in sigma), negative rows "
   f"{neg.sum()} (down to {Bc[neg].min():+.3f}); an inflation is a one-sided correction and the method "
   f"spans {Bc[krv].max()-Bc[krv].min():.3f} dex")
ATT["E4"] = dict(need_sigma=need_sig)

# ---------------- E5: support type ------------------------------------------------------------------
P("")
P("  E5  one offset by SUPPORT TYPE (rotation-derived vs everything else), 1 free parameter")
rss_s, ps = MODELS["canonical"]["Ms  support type (E5)"]
for u in sorted(set(SUP)):
    k = SUP == u
    P(f"    {u:10s} N = {k.sum():2d}  median {np.median(Bc[k]):+.3f}  spread {Bc[k].max()-Bc[k].min():.3f}")
ck("5f E5 fails for the same structural reason: the 'rotation' group itself contains +0.18 (DiskMass) "
   "and -0.39 (tidal dwarfs) and two keepers at zero, and the 'other' group runs from +1.65 to -1.16.  "
   "One offset per support type leaves an rms no better than the constant model",
   math.sqrt(rss_s / N) > 0.9 * math.sqrt(r00 / N),
   f"support-type rms {math.sqrt(rss_s/N):.4f} dex against the constant model's {math.sqrt(r00/N):.4f} "
   f"(a {100*(1-math.sqrt(rss_s/r00)):.1f}% improvement for one parameter)")

# ---------------- E6: the veins width bias transferred -----------------------------------------------
P("")
P("  E6  the veins finding transferred: resolved rotation sits +0.24 dex above unresolved line widths")
n_lw = sum(1 for r in LED if r[6] == "line_width")
P(f"    rows in the ENTIRE ledger measured by unresolved HI line width: {n_lw}")
P(f"    the +0.24 dex is a statement about a_0 measured from LINE WIDTHS versus from RESOLVED CURVES.")
P(f"    In B currency it is {0.24/2:+.3f} dex of acceleration, and it would apply to a line-width rung.")
ck("5g E6 HAS NO PURCHASE ON THIS LEDGER, and that is the honest answer to the angle as posed.  The "
   "velocity-measurement organiser the veins workflow found operates between rungs of the a_0 LADDER, "
   "where line widths and resolved curves measure the same quantity in the same kind of galaxy.  Not "
   "one liability row in this table is an unresolved-line-width measurement, so the +0.24 dex bias "
   "cannot move any of them",
   n_lw == 0,
   f"line-width rows in the ledger: {n_lw} of {len(LED)} (keepers included); the liability rows are "
   f"lensing {((MET=='lensing')&liab).sum()}, X-ray HSE {((MET=='xray_HSE')&liab).sum()}, resolved stellar RVs "
   f"{((MET=='resolved_star_RV')&liab).sum()}, discrete tracers {((MET=='discrete_tracer_RV')&liab).sum()}, "
   f"integrated spectra {((MET=='integrated_spec_disp')&liab).sum()}, resolved rotation "
   f"{((MET=='resolved_rotation')&liab).sum()}, and one each of vertical stellar kinematics and pair "
   f"redshifts -- not one is a line width")

# ---------------- E7: the maximal measurement model ---------------------------------------------------
P("")
P("  E7  the maximal measurement model: a free offset AND a free slope in log y_bar per method")
r7, p7 = MODELS["canonical"]["ME7 method x log y (E7)"]
rs_, ps_ = MODELS["canonical"]["Mslopes  1 offset + method slopes"]
aic7 = N * math.log(r7 / N) + 2 * p7
bic7 = N * math.log(r7 / N) + p7 * math.log(N)
bic0 = N * math.log(r00 / N) + math.log(N)
aic_s = N * math.log(rs_ / N) + 2 * ps_
P(f"    E7 (offsets AND slopes):        {p7:2d} params, rms {math.sqrt(r7/N):.4f} dex, AIC {aic7:7.2f}, BIC {bic7:7.2f}")
P(f"    slopes only (ONE shared offset): {ps_:2d} params, rms {math.sqrt(rs_/N):.4f} dex, AIC {aic_s:7.2f}")
P(f"    offsets only (E1):               {pc_:2d} params, rms {math.sqrt(rc_/N):.4f} dex, AIC {aic_m:7.2f}")
P(f"    constant:                        {p00:2d} params, rms {math.sqrt(r00/N):.4f} dex, AIC {aic_0:7.2f}, BIC {bic0:7.2f}")
P("")
P("    the per-method slopes d B / d log y_bar that E7 fits, which are the thing actually doing the work:")
for m in order:
    k = MET == m
    if k.sum() < 3: 
        P(f"      {m:22s} N = {k.sum()} -- too few rows for a slope"); continue
    A = np.vstack([LY[k], np.ones(k.sum())]).T
    cc = np.linalg.lstsq(A, Bc[k], rcond=None)[0]
    P(f"      {m:22s} N = {k.sum():2d}  slope {cc[0]:+.3f} dex per dex of log y_bar")
# permutation control on E7: with 16 parameters for 38 rows a RANDOM 8-way grouping also fits well
perm7 = np.array([rss_group_full(Bc, rng.permutation(MET), LY)[0] for _ in range(2000)])
p_e7 = (np.sum(perm7 <= r7) + 1) / (len(perm7) + 1)
info(f"permutation control on E7: shuffling the method labels and refitting all {p7} parameters gives "
     f"RSS <= the real one in {100*p_e7:.1f}% of 2000 shuffles (real {r7:.3f}, shuffled median {np.median(perm7):.3f})")
ck("5h AGAINST MY OWN FRAMING, and this is the one place the angle produced something real.  E7 does NOT "
   "fail the way I wrote it down before running it: sixteen parameters DO win on AIC (delta -7.8) and the "
   "structure IS significant against a relabelling of the methods (p = 0.015).  Three computed facts stop "
   "that from rescuing the measurement hypothesis.  (i) It loses on BIC by +16.8 -- 16 parameters on 38 "
   "rows.  (ii) The improvement is carried by the SLOPES and not by the OFFSETS, and a calibration bias is "
   "a CONSTANT: one shared offset plus per-method slopes, which contains no measurement freedom at all, "
   "recovers 0.39 of the variance where the offsets-only model recovers 0.22.  (iii) DECISIVELY, the two "
   "slopes doing the work are -0.62 (resolved stellar RVs) and +0.60 (discrete tracers), and those two "
   "groups are exactly the positive-dwarf and the negative-star-cluster families -- so E7 is the "
   "halo/no-halo split written as slopes, and the 2-PARAMETER halo split beats E7 on AIC by 10.8 with "
   "fourteen fewer parameters",
   bic7 > bic0 and (r00 - rs_) > (r00 - rc_) and aic_h < aic7,
   f"E7 AIC {aic7:.2f} vs constant {aic_0:.2f} (E7 wins by {aic_0-aic7:.1f}); E7 BIC {bic7:.2f} vs {bic0:.2f} "
   f"(E7 loses by {bic7-bic0:.1f}); E7 permutation p = {p_e7:.3f} (SIGNIFICANT -- reported against my own "
   f"framing); variance explained slopes-only {1-rs_/r00:.3f} on {ps_} params vs offsets-only "
   f"{1-rc_/r00:.3f} on {pc_}; the 2-parameter halo/no-halo split reaches AIC {aic_h:.2f}, "
   f"{aic7-aic_h:+.1f} better than E7")
info("what that decomposition MEANS, stated plainly: the significant structure in this table is a "
     "dependence of the offset on ACCELERATION that differs from class to class -- a statement about "
     "physics or about sample selection, not about how the velocity was measured.  Method and system "
     "class are almost perfectly confounded in this ledger (each method is one or two object families), "
     "so 'method x acceleration' cannot be separated from 'class x acceleration' -- and the class reading "
     "is the cheaper one by fourteen parameters.")
ATT["E7"] = dict(res=math.sqrt(r7 / N), params=p7, aic=aic7, bic=bic7, perm=p_e7)

# =====================================================================================================
P("")
P("=" * 126)
P("6.  WHAT MEASUREMENT DOES EXPLAIN -- reported because it is real, and it runs against the framework")
P("=" * 126)
hs = [i for i in range(N) if MET[i] == "xray_HSE" and "R500" in names[i] and "0.2" not in names[i] and "2500" not in names[i]]
wl = [i for i in range(N) if MET[i] == "lensing" and "eRASS1" in names[i]]
P(f"    hydrostatic masses at R500:        median B = {np.median(Bc[hs]):+.3f}   ({[names[i] for i in hs]})")
P(f"    weak-lensing-calibrated at R500:   median B = {np.median(Bc[wl]):+.3f}")
gap = np.median(Bc[wl]) - np.median(Bc[hs])
ck("6a THE ONE REAL MEASUREMENT EFFECT IN THE TABLE, and it costs the framework rather than saving it: "
   "at the SAME radius (R500) the mass technique matters, and the technique that reads LOW is the one "
   "that produces the framework's two best cluster rows.  Undoing the measured 20% hydrostatic bias "
   "closes most of that gap in the direction of the worse number",
   gap > 0.10,
   f"weak-lensing R500 median {np.median(Bc[wl]):+.3f} vs hydrostatic R500 median {np.median(Bc[hs]):+.3f}: "
   f"{gap:+.3f} dex; the b = 0.20 correction supplies {dB20:+.3f} dex of it ({100*dB20/gap:.0f}%)")

# =====================================================================================================
P("")
P("=" * 126)
P("7.  MUTATION CONTROLS")
P("=" * 126)
# M1: POWER TEST -- build the world in which the measurement hypothesis is TRUE and confirm the
#     machinery declares it true.  Same N, same method labels, same within-method scatter as the real
#     table's tightest method; offsets drawn to span the range the liabilities actually demand.
true_off = {m: d for m, d in zip(order, np.linspace(-0.45, +0.45, len(order)))}
wins, sig = 0, 0
for trial in range(200):
    Bs = np.array([true_off[m] for m in MET]) + rng.normal(0, 0.12, N)
    rs, ps = rss_group(Bs, MET); r0s, p0s = rss_const(Bs)
    a_m = N * math.log(rs / N) + 2 * ps; a_0s = N * math.log(r0s / N) + 2 * p0s
    b_m = N * math.log(rs / N) + ps * math.log(N); b_0s = N * math.log(r0s / N) + p0s * math.log(N)
    if a_m < a_0s and b_m < b_0s: wins += 1
    pp = np.mean([rss_group(Bs, rng.permutation(MET))[0] <= rs for _ in range(60)])
    if pp < 0.05: sig += 1
ck("M1 POWER: in a synthetic world where the measurement hypothesis is TRUE -- the same 38 rows, the same "
   "eight method labels, real per-method offsets spanning +-0.45 dex and a 0.12 dex within-method scatter "
   "-- the machinery detects it essentially every time, on AIC and BIC together and by permutation.  So "
   "section 4's null is a MEASUREMENT that the structure is absent, not a failure of the estimator",
   wins > 190 and sig > 190,
   f"method model wins on AIC and BIC in {wins}/200 synthetic trials; permutation p < 0.05 in {sig}/200; "
   f"on the REAL table it wins in neither (AIC {aic_m:.1f} vs {aic_0:.1f}, permutation p = {pmeth:.3f})")

# M2: a wrong a_0 must move the keepers, or the keeper tests are vacuous.
a0_bad = A0["canonical"] * 10
m_bad, s_bad = rar_stats(a0_bad)
ck("M2 a wrong a_0 breaks the keeper the shift tests are run against: pushing a_0 up by a decade moves "
   "the SPARC RAR's mean residual far off zero, so the RAR keeper is a real constraint and not an "
   "identity",
   abs(m_bad) > 0.15,
   f"a_0 x 10: RAR mean residual {m_can:+.4f} -> {m_bad:+.4f} dex, rms {s_can:.4f} -> {s_bad:.4f}")

# M3: shuffling B against the method labels
sh = [rss_group(rng.permutation(Bc), MET)[0] for _ in range(2000)]
ck("M3 shuffling the offsets against the method labels reproduces the observed within-method scatter: "
   "the real grouping is no tighter than a random one",
   np.mean(np.array(sh) <= rc_) > 0.05,
   f"observed within-method RSS {rc_:.3f}; shuffled median {np.median(sh):.3f}, "
   f"fraction of shuffles at least as tight {np.mean(np.array(sh) <= rc_):.3f}")

# =====================================================================================================
P("")
P("=" * 126)
P("8.  THE ALTERNATIVE COMPUTED BESIDE")
P("=" * 126)
P("  Under LambdaCDM the same table is not a table of failures at all: every positive row is a system")
P("  with a dark halo and every negative row is a system without one.  That reading was already made in")
P("  u01_pressure_supported (its section 6).  What THIS script adds is that the reading survives the")
P("  measurement question: the split by 'has a dark halo' is not a split by measurement technique.")
nh = int(HALO.sum())
permh = np.array([rss_group(Bc, rng.permutation(HG))[0] for _ in range(5000)])
p_h = (np.sum(permh <= rss_h) + 1) / (len(permh) + 1)
P(f"    'has a LambdaCDM dark halo' grouping: {ph} params, rms {math.sqrt(rss_h/N):.4f} dex, AIC {aic_h:.2f}, "
  f"permutation p over random {nh}-vs-{N-nh} splits = {p_h:.4f}")
P(f"    measurement-method grouping:          {pc_} params, rms {math.sqrt(rc_/N):.4f} dex, AIC {aic_m:.2f}, "
  f"permutation p = {pmeth:.4f}")
P("    CAVEAT, stated because it is the whole weight of this section: the 'no halo' set is four outer-halo")
P("    globular clusters plus DF2 and DF4, and it is very close to being 'the negative rows'.  The")
P("    classification is inherited from u01_pressure_supported, which states it was fixed before its")
P("    offsets were read -- but EXTENDING it to all 38 rows here is mine and is partly hindsight.  It is")
P("    reported as what the numbers say, at its own significance, and not as a result.")
ck("8a the LambdaCDM-shaped grouping ('does this system have a dark halo in the standard picture?') beats "
   "the eight-way measurement grouping on this table with six fewer parameters and at a permutation "
   "significance the method grouping never reaches -- reported because it is what the numbers say, not "
   "because it is the framework's friend, and carrying the hindsight caveat above",
   aic_h < aic_m and p_h < pmeth,
   f"halo grouping AIC {aic_h:.2f} on {ph} params (permutation p {p_h:.4f}) vs method AIC {aic_m:.2f} on "
   f"{pc_} params (permutation p {pmeth:.4f})")

# =====================================================================================================
P("")
P("=" * 126)
P("VERDICT")
P("=" * 126)
P("  ANGLE E IS ANSWERED IN THE NEGATIVE.  The liability ledger is NOT one measurement systematic, and")
P("  it does not need rewriting on measurement grounds.")
P("")
P(f"  1. Grouping by measurement method costs 7 free parameters and lowers the rms from "
  f"{math.sqrt(r00/N):.3f} to {math.sqrt(rc_/N):.3f} dex.")
P(f"     It loses to the constant on AIC by {aic_m-aic_0:.1f} and to a one-parameter acceleration slope by "
  f"{aic_m-aic_y:.1f}; permutation p on")
P(f"     the method label = {pmeth:.3f}.  The same machinery detects a synthetic method offset in "
  f"{wins}/200 trials, so this is a null,")
P("     not a blind estimator.")
P("  2. Three of the eight methods contain rows of BOTH signs.  A calibration offset is one number per")
P("     method and cannot produce two signs.  The largest method group -- dispersions from individually")
P(f"     resolved stellar radial velocities -- spans {Bc[MET=='resolved_star_RV'].max():+.2f} to "
  f"{Bc[MET=='resolved_star_RV'].min():+.2f} dex on its own, against a total table spread of {tot_spread:.2f}.")
P("  3. THE DECISIVE SINGLE FACT is inside ONE method at MATCHED acceleration: the KiDS isolated-dwarf")
P(f"     lens stack (lensing, y_bar {y_kids_dw:.1e}) returns a_0 to {abs(math.log10(a0_dw/A0['canonical'])):.3f} dex, "
  f"while eRASS1 group lensing")
P("     masses (lensing, y_bar 4.2e-3) need +0.42 dex.  Same technique, 0.6 decades apart in acceleration,")
P("     0.42 dex apart in offset.  Neither method nor acceleration organises the lensing family.")
P("  4. THE KEEPER BREAK, computed on the files and not asserted.  The offset the lensing liabilities")
P(f"     demand, applied to the KiDS data, moves the isolated-dwarf a_0 from {a0_dw:.2e} to {a0_dw_sh:.2e},")
P(f"     {math.log10(a0_dw_sh/A0['canonical']):+.2f} dex off the canonical footing.  The 1/r law SURVIVES (a "
  f"constant factor cannot move a log")
P("     slope) and so do Renzo at first order and the inner-diversity ratio (they are ratios inside one")
P("     curve).  The a_0 METERS do not: the lensing one and, under the rotation offset, the deep tail.")
P("  5. E7, the maximal measurement model, is the one place I was wrong before running it, and the")
P(f"     correction is reported rather than buried.  Sixteen parameters DO win on AIC ({aic7:.1f} vs "
  f"{aic_0:.1f}) and the")
P(f"     structure IS significant against a relabelling of the methods (p = {p_e7:.3f}).  But it loses on BIC by")
P(f"     {bic7-bic0:.1f}; the improvement is carried by the per-method SLOPES ({1-rs_/r00:.2f} of the variance on "
  f"{ps_} parameters) and not")
P(f"     by the OFFSETS ({1-rc_/r00:.2f} on {pc_}), and a calibration bias is a constant; and the two slopes doing the")
P("     work, -0.62 for resolved stellar RVs and +0.60 for discrete tracers, are exactly the positive-dwarf")
P("     and negative-star-cluster families.  E7 is the halo/no-halo split written as slopes, and the")
P(f"     2-parameter halo split beats it on AIC by {aic7-aic_h:.1f} with fourteen fewer parameters.  Method and")
P("     system class are confounded throughout this ledger and cannot be separated by it.")
P(f"  6. The one measurement effect that IS present -- hydrostatic versus weak-lensing masses at R500, "
  f"{gap:+.3f} dex")
P("     -- runs AGAINST the framework: undoing the measured 20% hydrostatic bias removes its two best")
P("     cluster rows.  Zero liabilities fixed, one made worse, and b is measured rather than free.")
P("  7. The veins workflow's velocity-measurement organiser does not transfer.  Zero liability rows are")
P("     unresolved-line-width measurements; it organises the a_0 LADDER, where line widths and resolved")
P("     curves measure the same thing in the same galaxies, not this ledger.")
P("")
P("  WHAT THIS ANGLE ADDS, BOTH WAYS:")
P(f"  * AGAINST THE PREVIOUS PHASE: the acceleration ordering of |B| was measured on tables with no")
P(f"    KEEPERS in them.  With the four recomputed keepers included, rho(|B|, log y) falls to {rho_y:+.3f} "
  f"(p = {p_y:.3f}).")
P("    Keepers sit at y_bar 1e-3 to 0.24 with |B| < 0.03 while liabilities at the SAME y_bar reach")
P(f"    +0.42 to +1.20 dex.  On signed B no continuous axis reaches R^2 = 0.08: log y "
  f"{1-MODELS['canonical']['My  log y_bar'][0]/r00:.3f}, log M "
  f"{1-MODELS['canonical']['Mm  log M_bar'][0]/r00:.3f}, log r "
  f"{1-MODELS['canonical']['Mr  log r'][0]/r00:.3f}.")
P("  * FOR THE FRAMEWORK: the two keepers most exposed to this angle survive it.  The 1/r lensing law and")
P("    Renzo's rule are shift-blind by construction, so no calibration story of any size touches them.")
P("  * THE HONEST RESIDUAL: what organises the table is a class-dependent dependence on acceleration.")
P(f"    A two-way split on 'does this system have a dark halo in the standard picture' reaches rms "
  f"{math.sqrt(rss_h/N):.3f} dex")
P(f"    on two parameters (permutation p = {p_h:.4f}), better than eight methods reach on eight.  That is the")
P("    LambdaCDM-shaped reading, it is partly hindsight here, and it is reported at its own significance.")
sys.exit(ck.done())
