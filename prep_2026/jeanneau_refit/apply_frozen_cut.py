#!/usr/bin/env python3
"""
apply_frozen_cut.py -- LANE D: apply the PRE-FROZEN acceleration cut (FROZEN_CUTS.md,
frozen 2026-07-16 BEFORE any per-galaxy number was read) to the real Jeanneau+26
(MUSE-DARK II, A&A 709, A120; arXiv:2603.28856) per-galaxy catalog fetched from CDS
(VizieR J/A+A/709/A120/catalog = their Table E1, CC-BY-4.0; 95 rows = exactly their
fiducial bTFR fit sample, Tab. 4: a=3.14 (Lelli+19), b_ref=3.54, b=3.54+-0.06, N=95).

Everything numerical here follows FROZEN_CUTS.md mechanically:
  cut       : g_bar < 0.5*a0_canon, g_bar from inverting g_obs = v^2/R through the
              framework's OWN nu (g_obs = sqrt(g_bar^2+g_bar*a0)) at a0_canon;
              v = v_c(2Re) (their fiducial bTFR velocity, GalPaK3D+lensing,
              pressure-support corrected), R = 2*Re (their intrinsic source-plane
              F160W Sersic Re, arcsec -> kpc with THE PAPER'S cosmology 0.3/0.7/70).
  estimator : median_i[ logMbar_i - (3.14*logV2.0_i + 3.54) ]  (their reference line)
  gate      : full-95 median must reproduce their 0.00 within +-0.05 dex.
  errors    : bootstrap 1e4 + coherent {gas 0.20, local-ref 0.16, convention 0.06}.
  footings  : BOTH, each with ITS OWN a0 (canonical 9.36e-11; ALT 1.13e-10),
              parent anchors re-asserted before any refit number is printed.
Deviations from the frozen file (logged in DATA.md): none in the selection/estimator;
fallbacks used exactly as pre-specified (no per-galaxy sigma_mu in the catalog).
Exit 0.
"""
import csv
import numpy as np

DIR = "/Users/carlzimmerman/new_physics/prep_2026/jeanneau_refit"

# ------------- frozen constants (FROZEN_CUTS.md section 7) -------------
A0_CANON = 9.36e-11          # m/s^2
A0_ALT = 1.13e-10            # m/s^2
CUT_GBAR = 0.5 * A0_CANON    # 4.68e-11
SLOPE = 3.14                 # Lelli+19, as adopted by Jeanneau+26
BREF = 3.54                  # Jeanneau+26 Tab.4 local-reference zero-point (Lelli+19)
SYS_GAS, SYS_REF, SYS_CONV = 0.20, 0.16, 0.06
NBOOT = 10000
KPC = 3.0857e19              # m
ALPHA_SIZE = 0.75            # vdW+14, cross-check only
Om_P, OL_P = 0.315, 0.685    # parent/banked cosmology (fork predictions)
W0, WA = -0.752, -0.86       # DESI DR2 CPL (canonical-CPL variant)
# Paper's own cosmology, used ONLY for the arcsec->kpc conversion of THEIR Re:
Om_J, OL_J, H0_J = 0.30, 0.70, 70.0

# ------------- parent machinery, re-asserted (banked anchors) -------------
def f_DE(z, w0=W0, wa=WA):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def E_z(z, w0=W0, wa=WA):
    return np.sqrt(Om_P * (1 + np.asarray(z, float)) ** 3 + OL_P * f_DE(z, w0, wa))

r3 = float(np.sqrt(f_DE(3.0)))
assert abs(r3 - 0.74) < 0.01
assert abs(0.25 * np.log10(r3) - (-0.033)) < 0.001, "canonical dlogV(3) anchor"
assert abs(0.25 * np.log10(E_z(3.0)) - 0.164) < 0.003, "ALT dlogV(3) anchor"
assert np.allclose(np.sqrt(f_DE(np.array([1., 2., 3.]), w0=-1.0, wa=0.0)), 1.0)
print("[OK] banked fork anchors reproduced (canonical -0.033 / ALT +0.164 at z=3)")

def Delta_c(z):
    z = np.asarray(z, float)
    Ez2 = Om_P * (1 + z) ** 3 + OL_P
    x = Om_P * (1 + z) ** 3 / Ez2 - 1
    return 18 * np.pi ** 2 + 82 * x - 39 * x ** 2

def dlogM_lcdm_halo(z):
    Ez = np.sqrt(Om_P * (1 + np.asarray(z, float)) ** 3 + OL_P)
    return -np.log10(Ez * np.sqrt(Delta_c(z) / Delta_c(0.0)))

assert abs(float(dlogM_lcdm_halo(1.0)) - (-0.34)) < 0.03
print("[OK] LCDM halo anchor reproduced (-0.34 dex at z=1, Jeanneau Eq.9 quote)")

def g_bar_of(g_obs, a0):
    """Invert the framework's OWN nu: g_obs = sqrt(g_bar^2 + g_bar*a0)."""
    return 0.5 * (-a0 + np.sqrt(a0 ** 2 + 4.0 * np.asarray(g_obs, float) ** 2))

# angular diameter distance, paper cosmology (flat)
def D_A_kpc_per_arcsec(z, Om=Om_J, OL=OL_J, H0=H0_J):
    c = 299792.458  # km/s
    zz = np.linspace(0.0, z, 4096)
    Ez = np.sqrt(Om * (1 + zz) ** 3 + OL)
    Dc = c / H0 * np.trapz(1.0 / Ez, zz)             # Mpc comoving
    DA = Dc / (1 + z)                                # Mpc
    return DA * 1e3 * np.pi / (180 * 3600)           # kpc per arcsec

# ------------- load the REAL catalog (CDS J/A+A/709/A120) -------------
rows = list(csv.DictReader(open(DIR + "/jeanneau26_catalog_cds.csv")))
assert len(rows) == 95, "catalog must be exactly Jeanneau+26's fiducial N=95"
z = np.array([float(r["zR21"]) for r in rows])
mu = np.array([float(r["muR21"]) for r in rows])
Re_as = np.array([float(r["Reff"]) for r in rows])          # intrinsic (source-plane), arcsec
logV = np.array([float(r["logV2_0"]) for r in rows])        # log10 v_c(2Re), km/s
s_logV = np.array([float(r["s_logV2_0"]) for r in rows])
logMs = np.array([float(r["logM*"]) for r in rows])
logMHI = np.array([float(r["logMHI"]) for r in rows])       # incl. He
logMMol = np.array([float(r["logMMol"]) for r in rows])
logMbar = np.array([float(r["logMBar"]) for r in rows])
ids = np.array([r["IdR21"] for r in rows])
clus = np.array([r["Cluster"] for r in rows])
# internal consistency of THEIR mass bookkeeping (not a cut):
mb_re = np.log10(10 ** logMs + 10 ** logMHI + 10 ** logMMol)
assert np.max(np.abs(mb_re - logMbar)) < 0.02, "Mbar = M* + MHI + Mmol bookkeeping"
print("[OK] catalog loaded: N=95, Mbar bookkeeping verified (max dev %.4f dex)"
      % np.max(np.abs(mb_re - logMbar)))

# ------------- the frozen acceleration cut -------------
kpc_as = np.array([D_A_kpc_per_arcsec(zi) for zi in z])
R_kpc = 2.0 * Re_as * kpc_as                                # R = 2*Re, physical kpc
v_ms = 10 ** logV * 1e3
g_obs = v_ms ** 2 / (R_kpc * KPC)                           # m/s^2
gbar_can = g_bar_of(g_obs, A0_CANON)
sel = gbar_can < CUT_GBAR
N = int(sel.sum())

# ------------- zero-point estimator -------------
delta = logMbar - (SLOPE * logV + BREF)

# validity gate: full-95 must reproduce their 0.00 +- 0.05
full_med = float(np.median(delta))
print("\n[GATE] full-95 median offset vs Lelli+19(3.14, 3.54): %+0.3f dex "
      "(their fit 0.00+-0.06) -> %s" % (full_med, "PASS" if abs(full_med) < 0.05 else "FAIL"))
assert abs(full_med) < 0.05, "pipeline convention gate"

rng = np.random.default_rng(20260716)
def boot_median(x, n=NBOOT):
    m = np.median(rng.choice(x, size=(n, x.size), replace=True), axis=1)
    return np.percentile(m, [16, 50, 84])

d = delta[sel]
lo, med, hi = boot_median(d)
stat = 0.5 * (hi - lo)
mad = float(np.median(np.abs(d - np.median(d))))
w = 1.0 / (SLOPE ** 2 * s_logV[sel] ** 2 + 0.2 ** 2)        # their +-0.2 dex Mbar error
wmean = float(np.sum(w * d) / np.sum(w))
band = float(np.sqrt(stat ** 2 + SYS_GAS ** 2 + SYS_REF ** 2 + SYS_CONV ** 2))

# free-slope check (orthogonal least squares on the subsample)
xs, ys = logV[sel], logMbar[sel]
xm, ym = xs.mean(), ys.mean()
sxx, syy, sxy = np.sum((xs - xm) ** 2), np.sum((ys - ym) ** 2), np.sum((xs - xm) * (ys - ym))
beta = (syy - sxx + np.sqrt((syy - sxx) ** 2 + 4 * sxy ** 2)) / (2 * sxy)   # TLS slope
zp_free = ym - beta * xm
d_free = float(ym - (SLOPE * xm + BREF))    # offset at the subsample centroid, fixed slope

# ------------- fork predictions on the subsample (both footings, own a0) -------------
def pred_exact(gobs, zz, a0, ratio):
    return np.log10(g_bar_of(gobs, a0 * ratio(zz)) / g_bar_of(gobs, a0))

one = lambda zz: np.ones_like(np.asarray(zz, float))
cpl = lambda zz: np.sqrt(f_DE(zz))
alt = lambda zz: E_z(zz)
p_can = pred_exact(g_obs[sel], z[sel], A0_CANON, one)       # == 0 identically
p_cpl = pred_exact(g_obs[sel], z[sel], A0_CANON, cpl)
p_alt = pred_exact(g_obs[sel], z[sel], A0_ALT, alt)

# size-term residual check (must ~cancel in the deep regime; canonical const-a0)
def pred_size(gobs_v, R_m, zz, a0, ratio, alpha=ALPHA_SIZE):
    v2 = gobs_v * R_m
    R0 = R_m * (1 + zz) ** alpha
    return np.log10(g_bar_of(v2 / R_m, a0 * ratio(zz)) * R_m ** 2 /
                    (g_bar_of(v2 / R0, a0) * R0 ** 2))
p_size_can = pred_size(g_obs[sel], R_kpc[sel] * KPC, z[sel], A0_CANON, one)
# same quantity for the FULL sample, for contrast
p_size_full = pred_size(g_obs, R_kpc * KPC, z, A0_CANON, one)

# dilution factors, each footing its OWN a0 (parent VERIFY correction honored)
def dilution(gobs, a0):
    x = a0 / g_bar_of(gobs, a0)
    return x / (2 + x)
dil_can = dilution(g_obs[sel], A0_CANON)
dil_alt = dilution(g_obs[sel], A0_ALT)

# ------------- stress tests (frozen section 4) -------------
def med_sub(mbar_new):
    return float(np.median((mbar_new - (SLOPE * logV + BREF))[sel]))
m_hi_half = np.log10(10 ** logMs + 10 ** logMMol + 0.5 * 10 ** logMHI)
m_hi_dbl = np.log10(10 ** logMs + 10 ** logMMol + 2.0 * 10 ** logMHI)
gas_lo, gas_hi = med_sub(m_hi_half), med_sub(m_hi_dbl)

# selection stress: Re +-0.14 dex (their OII-vs-broadband structural MAD; no per-galaxy
# sigma_mu exists -> frozen fallback), and Planck-vs-paper cosmology on the conversion
def sel_of(scale_R, Om=Om_J, OL=OL_J, H0=H0_J):
    ka = np.array([D_A_kpc_per_arcsec(zi, Om, OL, H0) for zi in z])
    gg = v_ms ** 2 / (2.0 * Re_as * scale_R * ka * KPC)
    return g_bar_of(gg, A0_CANON) < CUT_GBAR
sel_Rlo, sel_Rhi = sel_of(10 ** -0.14), sel_of(10 ** 0.14)
sel_planck = sel_of(1.0, 0.315, 0.685, 67.4)
gas_frac = (10 ** logMHI + 10 ** logMMol) / 10 ** logMbar

# ------------- report -------------
print("\n" + "=" * 88)
print("FROZEN CUT APPLIED: g_bar < 0.5*a0_canon = 4.68e-11 (g_obs < 8.11e-11 m/s^2)")
print("=" * 88)
print("  subsample N = %d of 95  (parent forecast: 'roughly a third')" % N)
print("  z range: %.2f - %.2f (median %.2f)" % (z[sel].min(), z[sel].max(),
                                                np.median(z[sel])))
print("  logM* range: %.1f - %.1f;  median gas fraction %.2f (full 95: %.2f)"
      % (logMs[sel].min(), logMs[sel].max(),
         np.median(gas_frac[sel]), np.median(gas_frac)))
print("  g_bar/a0_canon: %.2f - %.2f (median %.2f)"
      % ((gbar_can[sel] / A0_CANON).min(), (gbar_can[sel] / A0_CANON).max(),
         np.median(gbar_can[sel] / A0_CANON)))
print("  dilution (canonical a0): median %.2f (range %.2f-%.2f)"
      % (np.median(dil_can), dil_can.min(), dil_can.max()))
print("  dilution (ALT own a0)  : median %.2f (range %.2f-%.2f)"
      % (np.median(dil_alt), dil_alt.min(), dil_alt.max()))
print("  cut-boundary stress: N=%d (Re-0.14dex) / %d (frozen) / %d (Re+0.14dex); "
      "N=%d (Planck conversion)" % (sel_Rlo.sum(), N, sel_Rhi.sum(), sel_planck.sum()))

print("\nZERO-POINT (mass axis, vs Lelli+19 slope 3.14, b_ref 3.54 -- their line):")
print("  PRIMARY  median offset  : %+0.3f dex  (bootstrap 68%%: %+0.3f .. %+0.3f; "
      "stat +-%.3f; MAD %.3f)" % (med, lo, hi, stat, mad))
print("  weighted mean (check)   : %+0.3f dex" % wmean)
print("  free-slope TLS (check)  : slope %.2f (vs 3.14), centroid offset %+0.3f dex"
      % (beta, d_free))
print("  full-95 median (gate)   : %+0.3f dex (reproduces their 0.00+-0.06)" % full_med)
print("  HONEST BAND = sqrt(%.3f^2 + %.2f^2 + %.2f^2 + %.2f^2) = +-%.3f dex"
      % (stat, SYS_GAS, SYS_REF, SYS_CONV, band))
print("  gas stress (HI x0.5 / x2): median -> %+0.3f / %+0.3f dex" % (gas_lo, gas_hi))

print("\nFORK PREDICTIONS on this subsample (exact per-galaxy, framework nu, own a0):")
print("  canonical pure-Lambda : %+0.3f dex (identically 0)" % np.median(p_can))
print("  canonical DESI-CPL    : %+0.3f dex (median; range %+0.3f..%+0.3f)"
      % (np.median(p_cpl), p_cpl.min(), p_cpl.max()))
print("  ALT rho_tot/cH0       : %+0.3f dex (median; range %+0.3f..%+0.3f)"
      % (np.median(p_alt), p_alt.min(), p_alt.max()))
print("  size-term residual (canonical, vdW14 a=%.2f): subsample median %+0.3f dex "
      "(full-95 %+0.3f) -> deep-regime cancellation check" % (
          ALPHA_SIZE, np.median(p_size_can), np.median(p_size_full)))
print("  LCDM halo term at subsample median z: %+0.3f dex (does NOT cancel; "
      "ALT remains LCDM-degenerate on the negative side)"
      % float(dlogM_lcdm_halo(np.median(z[sel]))))

# ------------- mechanical decision rule (frozen section 5) -------------
D_ALT = float(np.median(p_alt))
sig_can = abs(med - 0.0) / band
sig_alt = abs(med - D_ALT) / band
print("\nDECISION RULE (mechanical, FROZEN_CUTS.md section 5):")
print("  Delta_b = %+0.3f, honest band B = %.3f, fork separation |Delta_ALT| = %.3f"
      % (med, band, abs(D_ALT)))
print("  distance from canonical(0): %.2f sigma;  from ALT(%+0.3f): %.2f sigma"
      % (sig_can, D_ALT, sig_alt))
if band > abs(D_ALT):
    verdict = ("STILL-UNDERPOWERED: honest band (%.3f) exceeds the fork separation "
               "(%.3f). The deep cut did not deliver the forecast power." % (band, abs(D_ALT)))
elif sig_can < 1.0 and sig_alt >= 1.0:
    verdict = ("ALT-SIDE CONSTRAINT: consistent with canonical (%.2f sigma), "
               "inconsistent with ALT at %.2f sigma." % (sig_can, sig_alt))
elif sig_can < 1.0 and sig_alt < 1.0:
    lean = "canonical" if sig_can < sig_alt else "ALT"
    verdict = ("UNDERPOWERED LEAN (%s side): both footings inside the band "
               "(%.2f vs %.2f sigma)." % (lean, sig_can, sig_alt))
elif sig_alt < 1.0 <= sig_can:
    verdict = ("ALT-FAVORED: sits at ALT within the band (%.2f sigma) and away from "
               "canonical (%.2f sigma)." % (sig_alt, sig_can))
else:
    verdict = ("INCONSISTENT WITH BOTH at >=1 sigma (%.2f vs %.2f) -- report straight."
               % (sig_can, sig_alt))
if N < 15:
    verdict += " [N=%d < 15: weaker than the parent forecast third]" % N
print("  VERDICT: " + verdict)
# stat-only contrast (transparency; NOT the claim)
print("  [stat-only, DO-NOT-CLAIM alone] distance from ALT: %.2f sigma; "
      "from canonical: %.2f sigma" % (abs(med - D_ALT) / stat, abs(med) / stat))

# ------------- flagged-check diagnostics (frozen sections 3-5 flags) -------------
print("\nDIAGNOSTICS (flags raised by the frozen checks):")
# (i) free-slope flag: bootstrap the TLS slope on the subsample
def tls_slope(x, y):
    xm_, ym_ = x.mean(), y.mean()
    sxx_, syy_ = np.sum((x - xm_) ** 2), np.sum((y - ym_) ** 2)
    sxy_ = np.sum((x - xm_) * (y - ym_))
    return (syy_ - sxx_ + np.sqrt((syy_ - sxx_) ** 2 + 4 * sxy_ ** 2)) / (2 * sxy_)
bs = []
for _ in range(2000):
    j = rng.integers(0, xs.size, xs.size)
    bs.append(tls_slope(xs[j], ys[j]))
b16, b50, b84 = np.percentile(bs, [16, 50, 84])
sig_slope = (b50 - SLOPE) / (0.5 * (b84 - b16))
print("  free-slope TLS bootstrap: %.2f (68%%: %.2f..%.2f) -> %.1f sigma from 3.14 %s"
      % (b50, b16, b84, sig_slope,
         "[FLAG >2sigma: the cut correlates with velocity; fixed-slope ZP is the "
         "headline per the freeze, flag carried]" if abs(sig_slope) > 2 else "[ok]"))
# (ii) magnification profile of the subsample (faint-third sensitivity)
print("  magnification mu: subsample median %.1f (range %.1f-%.1f) vs full-95 median %.1f"
      % (np.median(mu[sel]), mu[sel].min(), mu[sel].max(), np.median(mu)))
# (iii) verdict stability under the selection stresses (recompute median offset)
for tag, s_ in (("Re-0.14dex sel (N=%d)" % sel_Rlo.sum(), sel_Rlo),
                ("Re+0.14dex sel (N=%d)" % sel_Rhi.sum(), sel_Rhi),
                ("Planck-conv sel (N=%d)" % sel_planck.sum(), sel_planck)):
    dd = delta[s_]
    l_, m_, h_ = boot_median(dd)
    palt_ = np.median(pred_exact(g_obs[s_], z[s_], A0_ALT, alt))
    print("  %-24s: median %+0.3f (68%% %+0.3f..%+0.3f), ALT pred %+0.3f"
          % (tag, m_, l_, h_, palt_))
# (iv) both frozen decision rules that fired (the freeze did not anticipate Delta_b>0)
print("  rule collision note: B(%.3f) > |Delta_ALT|(%.3f) [STILL-UNDERPOWERED] AND "
      "|Delta_b-Delta_ALT|(%.3f) > B with |Delta_b|<B [ALT-side, %.2f sigma] fire "
      "together because Delta_b landed POSITIVE (away from BOTH footings); the "
      "structural verdict (UNDERPOWERED) is the headline, the %.2f sigma ALT-side "
      "distance is reported as a lean, not a constraint."
      % (band, abs(D_ALT), abs(med - D_ALT), sig_alt, sig_alt))

# ------------- write subsample.csv -------------
with open(DIR + "/subsample.csv", "w", newline="") as f:
    wcsv = csv.writer(f)
    wcsv.writerow(["Cluster", "IdR21", "z", "mu", "Re_arcsec", "R2.0_kpc",
                   "logV2.0", "s_logV2.0", "logMstar", "logMHI", "logMMol", "logMbar",
                   "g_obs_ms2", "g_bar_canon_ms2", "gbar_over_a0canon",
                   "dilution_canon", "dilution_alt_own_a0",
                   "delta_b_dex", "pred_ALT_dex", "pred_CPL_dex"])
    idx = np.where(sel)[0]
    for k, i in enumerate(idx):
        wcsv.writerow([clus[i], ids[i], "%.4f" % z[i], "%.3f" % mu[i],
                       "%.4f" % Re_as[i], "%.3f" % R_kpc[i],
                       "%.4f" % logV[i], "%.4f" % s_logV[i],
                       "%.3f" % logMs[i], "%.3f" % logMHI[i], "%.3f" % logMMol[i],
                       "%.3f" % logMbar[i],
                       "%.3e" % g_obs[i], "%.3e" % gbar_can[i],
                       "%.3f" % (gbar_can[i] / A0_CANON),
                       "%.3f" % dil_can[k], "%.3f" % dil_alt[k],
                       "%.4f" % delta[i], "%.4f" % p_alt[k], "%.4f" % p_cpl[k]])
print("\nWrote %s/subsample.csv (N=%d rows)" % (DIR, N))
print("EXIT 0")
