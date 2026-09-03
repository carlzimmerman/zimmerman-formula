#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_exact-relations_efe_environment.py -- COMPUTE STAGE, angle "exact-relations", candidate K3.

THE CANDIDATE.  For a system whose own internal Newtonian field is much weaker than its host's, QUMOND forces
the enclosed dynamical-to-baryonic mass ratio to be a function of the ENVIRONMENT ALONE:

    M_dyn/M_b = nu(y_e) * (1 + L(y_e)/3),   y_e = g_ext,N/a_0,   L = dln nu / dln y

Route A closed form:  [1 - s_e/(6(e^{s_e}-1))] / (1 - e^{-s_e}),  s_e = sqrt(y_e).

THE BITE claimed by the proposer: the discrepancy depends only on the host-centric position, NOT on the
system's own mass, size, surface brightness or internal acceleration.  So d log(M_dyn/M_b)/d log g_bar,own
must be ~0 where the isolated RAR would give ~-1/2.

WHAT THIS SCRIPT ADDS OVER hunt_2026/k03_efe_phantom_theorem.py (the propose-stage script):

  1. THE SHAPE TEST ON COMA IS CONFOUNDED IN EXACTLY THE WAY THE PROPOSER FLAGGED FOR THE LOCAL GROUP AND
     THEN DID NOT CHECK FOR COMA.  Regressing log(g_obs/g_bar) on log(g_bar) shares g_bar between ordinate
     and abscissa (bug pattern 5).  With measurement error sigma_e in log g_bar and true spread sigma_b,
        slope_measured = (beta_true*sigma_b^2 - sigma_e^2)/(sigma_b^2 + sigma_e^2).
     On this sample sigma_e ~ sigma_b, so the induced term is order -1/2 -- the same size as the entire
     signal being claimed.  This script measures the confound by Monte Carlo under BOTH hypotheses and
     reports the observed slope against those two distributions, instead of against the unconfounded
     predictions.
  2. THE UNCONFOUNDED FORM of the same test: regress log g_obs on log g_bar (no shared variable), where the
     EFE law predicts slope 1+beta = 0.979 and the isolated RAR predicts 0.522, both attenuated by the same
     known regression-dilution factor -- a clean discriminator that the propose stage did not run.
  3. A SECOND, INDEPENDENT SHAPE AXIS: d log(M_dyn/M_b)/d log g_ext.  The host-centric distance is measured
     from projected position and shares NOTHING with g_obs or g_bar, so this axis carries no bug-pattern-5
     confound at all.  Not run at the propose stage for Coma.
  4. THE EXTERNAL FIELD DONE THREE WAYS, because it moves the prediction by half a dex: the cluster's
     DYNAMICAL field 2 sigma^2/r; the NEWTONIAN field that produces it (kernel inverted -- the quantity
     QUMOND's nu actually takes); and the anisotropy floor nu_e(1+L_e) ... nu_e.
  5. THE LOCAL-GROUP CONFOUND MEASURED rather than argued: a no-physics Monte Carlo with pure distance and
     luminosity errors, to see how much of the measured +0.695/-0.509 it manufactures.

Both footings; mutation controls; Newtonian and LCDM alternatives beside the framework; Upsilon lever at x1.5.
"""
import os, math, sys, csv
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(20260903)
P("=" * 118)
P("K3 (exact-relations compute) -- the external-field phantom-mass theorem as an ENVIRONMENT-ONLY law")
P("=" * 118)

# ------------------------------------------------------------------ kernel pieces (scalar, independent impl)
def nu_y(y):
    s = math.sqrt(max(y, 1e-300))
    return 1.0 / s if s < 1e-8 else 1.0 / (1.0 - math.exp(-s))
def L_y(y):
    s = math.sqrt(max(y, 1e-300))
    if s < 1e-8: return -0.5
    if s > 700.0: return 0.0
    return -(s / 2.0) / math.expm1(s)
def R_theory(y):   return nu_y(y) * (1.0 + L_y(y) / 3.0)
def R_para(y):     return nu_y(y) * (1.0 + L_y(y))          # local ratio ALONG the external field
def R_perp(y):     return nu_y(y)                            # local ratio ACROSS it

def gN_from_gobs(gobs, a0):
    """Invert g_obs = nu(g_N/a0) g_N for g_N (the Newtonian field that QUMOND's nu actually takes)."""
    lo, hi = 1e-9 * gobs, 10.0 * gobs
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if nu_y(mid / a0) * mid < gobs: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

# ------------------------------------------------------------------ (A) the theorem, verified independently
P("\n  (A) THE THEOREM, verified by exact closed-surface flux integration with NO expansion (Gauss-Legendre,")
P("      a different quadrature from the propose-stage script).  Units a_0 = 1, G M_b = 1.")
_GL = {}
def _gl(n):
    if n not in _GL: _GL[n] = np.polynomial.legendre.leggauss(n)
    return _GL[n]
def flux_ratio(y_e, R, n=400):
    mu, w = _gl(n)                                          # nodes on cos(theta) in [-1,1]
    eps = 1.0 / R**2
    gx = y_e + eps * mu
    gt = eps * np.sqrt(np.maximum(0.0, 1.0 - mu**2))
    gmag = np.sqrt(gx**2 + gt**2)
    nuv = np.array([nu_y(g) for g in gmag])
    # outward radial component of nu*g_N on the sphere; r_hat . (g_x xhat + g_t that) = gx*mu + gt*sqrt(1-mu^2)
    radial = nuv * (gx * mu + gt * np.sqrt(np.maximum(0.0, 1.0 - mu**2)))
    return 0.5 * float(np.sum(w * radial)) * R**2           # (1/4pi) * 2pi * int dmu ... * R^2

P("   y_e        nu_e        L_e   theorem   |   exact flux at R = 10, 30, 100, 300")
for y_e in (0.01, 0.1, 0.3, 1.0, 3.0, 10.0):
    th = R_theory(y_e)
    fl = [flux_ratio(y_e, R) for R in (10.0, 30.0, 100.0, 300.0)]
    P(f"   {y_e:6.3g} {nu_y(y_e):10.4f} {L_y(y_e):10.4f} {th:10.6f}   |  " + "  ".join(f"{f:10.6f}" for f in fl))
    ck(f"flux -> theorem as R grows (y_e={y_e})", abs(fl[-1] / th - 1.0) < 3e-5,
       f"R=300 gives {fl[-1]:.6f} vs {th:.6f} ({fl[-1]/th-1:+.2e})")
ck("deep external field limit is (5/6) nu_e", abs(R_theory(1e-12) / nu_y(1e-12) - 5.0 / 6.0) < 1e-6,
   f"{R_theory(1e-12)/nu_y(1e-12):.9f}   (the limit is approached as O(sqrt y), so it must be taken at y<<1e-8)")
ck("Newtonian external field limit is 1", abs(R_theory(1e6) - 1.0) < 1e-6, f"{R_theory(1e6):.9f}")

# ------------------------------------------------------------------ (B) THE RESTATEMENT TEST, EXECUTED
P("\n  (B) RESTATEMENT TEST -- executed, not asserted.  Try to derive the candidate from v^4 = G M_b a_0.")
P("      v^4 = G M_b a_0 is the ISOLATED deep-MOND limit.  Written as a discrepancy it says")
P("          M_dyn/M_b = nu(y_own) -> sqrt(a_0/g_bar,own)  in the deep limit,")
P("      i.e.  d log(M_dyn/M_b)/d log g_bar,own = -1/2 EXACTLY, and it contains NO external field.")
P("      The candidate says that slope is ~0 and the ratio is set by g_ext instead.  The derivation cannot")
P("      close: the BTFR has no g_ext in it and the theorem has no M_b in it.  ==> NOT a restatement of the")
P("      BTFR/RAR/deep-MOND limit.  is_restatement = FALSE on that axis.")
y_own_grid = np.array([1e-3, 3e-3, 1e-2])
slope_rar = np.polyfit(np.log10(y_own_grid), np.log10([nu_y(y) for y in y_own_grid]), 1)[0]
P(f"      numerically: isolated-RAR slope over the UDGs' own y range = {slope_rar:+.4f} (deep limit -0.500)")
ck("restatement test executed: BTFR slope in own g_bar is -1/2, theorem's is ~0 -- they differ",
   abs(slope_rar - 0.0) > 0.3, f"BTFR gives {slope_rar:+.3f}, theorem gives ~0.00")
P("      LITERATURE, against interest: the total-phantom-mass-in-an-external-field result IS published --")
P("      Milgrom 1986 (ApJ 302, 617) and Milgrom 2009 (arXiv:0906.4817) beta(eta); the anisotropic operator")
P("      nu_e(delta_ij + L_e n_i n_j) is Milgrom 1986/2010.  CRITERION (4) FAILS FOR THE THEOREM ITSELF.")
P("      Only the Route A closed form and the population SHAPE test are unstated -- and (see below) the")
P("      shape test is what this script kills.")

# ------------------------------------------------------------------ (C) Coma UDGs
P("\n  (C) COMA UDGs (Freundlich+2022, on disk).  log g_bar and log g_obs at R_e are tabulated INDEPENDENTLY")
P("      and the distance is the cluster's, common to every object.")
rows = []
for ln in open(os.path.join(DATA, "freundlich2022_coma_udgs.tsv"), encoding="latin-1"):
    if ln.startswith("#") or not ln.strip(): continue
    f = ln.rstrip("\n").split("\t")
    if f[0] == "name": hdr = f; continue
    rows.append({hdr[i]: f[i] for i in range(len(hdr))})
name  = np.array([r["name"] for r in rows])
dmean = np.array([float(r["dmean_kpc"]) for r in rows])
lgbar = np.array([float(r["lgbar"]) for r in rows]); elgbar = np.array([float(r["elgbar"]) for r in rows])
lgobs = np.array([float(r["lgobs"]) for r in rows]); elgobs = np.array([float(r["elgobs"]) for r in rows])
MLtab = np.array([float(r["ML"]) for r in rows])
N = len(rows); P(f"      {N} UDGs read")

SIG_COMA = 1.0e6                                             # 1000 km/s, Coma velocity dispersion
def g_ext_dyn(r_kpc):  return 2.0 * SIG_COMA**2 / (r_kpc * kpc)   # SIS dynamical (observed) field

def coma_prediction(a0, ml_scale=1.0, ye_mode="newtonian", a0_kernel=None):
    """Returns (logratio_obs, logratio_pred, y_e, log g_bar).  ml_scale rescales the stellar M/L, which
    moves g_bar (and hence the ratio) but not g_ext."""
    ak = a0 if a0_kernel is None else a0_kernel
    lb = lgbar + math.log10(ml_scale)                        # UDGs are stellar-dominated -> g_bar ~ Upsilon
    gd = np.array([g_ext_dyn(r) for r in dmean])
    if   ye_mode == "dynamical": ye = gd / a0
    elif ye_mode == "newtonian": ye = np.array([gN_from_gobs(g, ak) for g in gd]) / a0
    else: raise ValueError(ye_mode)
    pred = np.array([math.log10(R_theory(y)) for y in ye])
    return (lgobs - lb), pred, ye, lb

def wls_slope(x, y, ey=None, nboot=4000):
    """OLS slope with a bootstrap error (11 points: the bootstrap is the honest error)."""
    s = np.polyfit(x, y, 1)[0]
    bs = []
    for _ in range(nboot):
        i = rng.integers(0, len(x), len(x))
        if np.ptp(x[i]) < 1e-9: continue
        bs.append(np.polyfit(x[i], y[i], 1)[0])
    return s, float(np.std(bs))

P("\n      --- amplitude, both footings, both external-field conventions ---")
amp = {}
for fname, a0 in A0.items():
    for mode in ("dynamical", "newtonian"):
        lr, pr, ye, lb = coma_prediction(a0, ye_mode=mode)
        res = lr - pr
        amp[(fname, mode)] = (np.median(res), res.std(), np.median(ye), np.median(pr))
        P(f"      {fname:9s} y_e from {mode:9s}: median y_e {np.median(ye):6.3f}  predicted log ratio "
          f"{np.median(pr):+.3f}  observed {np.median(lr):+.3f}  ==> residual {np.median(res):+.3f} dex "
          f"(scatter {res.std():.3f}, {abs(np.median(res))/(res.std()/math.sqrt(N)):.1f} sigma)")
best = min(amp.items(), key=lambda kv: abs(kv[1][0]))
P(f"      MOST FAVOURABLE convention for the framework: {best[0]} -> {best[1][0]:+.3f} dex")
P("      anisotropy floor (the local ratio runs from nu_e(1+L_e) to nu_e; the sphere average sits between):")
lr, pr, ye, lb = coma_prediction(A0["canonical"], ye_mode="newtonian")
P(f"        at median y_e = {np.median(ye):.3f}:  parallel {math.log10(R_para(np.median(ye))):+.3f} dex, "
  f"perpendicular {math.log10(R_perp(np.median(ye))):+.3f} dex, sphere-average {math.log10(R_theory(np.median(ye))):+.3f} dex"
  f"  -> modelling floor {math.log10(R_perp(np.median(ye)))-math.log10(R_para(np.median(ye))):.3f} dex")
ck("Coma UDG amplitude matches the theorem within 0.3 dex (any convention, any footing)",
   abs(best[1][0]) < 0.3, f"best is {best[0]} at {best[1][0]:+.3f} dex")

# ---- the shape test, and the confound the propose stage did not check for Coma
P("\n      --- SHAPE TEST 1: does the discrepancy ignore the UDG's OWN baryons? ---")
P("      THE CONFOUND (bug pattern 5): the ordinate log(g_obs/g_bar) contains the abscissa log(g_bar).")
lr, pr, ye, lb = coma_prediction(A0["canonical"], ye_mode="newtonian")
s_obs, s_err = wls_slope(lgbar, lr)
var_b_tot = float(np.var(lgbar, ddof=1)); var_e = float(np.mean(elgbar**2))
var_b_true = max(var_b_tot - var_e, 1e-6)
P(f"      Var(log g_bar) measured = {var_b_tot:.5f};  mean measurement variance = {var_e:.5f}")
P(f"      ==> the TRUE spread in log g_bar is only {math.sqrt(var_b_true):.3f} dex against a {math.sqrt(var_e):.3f} dex")
P(f"          measurement error.  The error is {math.sqrt(var_e/var_b_true):.2f}x the signal.")
beta_efe = -0.021
lo, hi = np.log10(ye.min()), np.log10(ye.max())
# measure the theorem's own predicted own-g_bar slope directly (should be ~0 -- g_bar does not enter)
beta_efe_meas = np.polyfit(lgbar, pr, 1)[0]
beta_rar = float(np.polyfit(np.log10(10**lgbar / A0["canonical"]),
                            np.log10([nu_y(10**b / A0["canonical"]) for b in lgbar]), 1)[0])
P(f"      unconfounded predictions:  EFE theorem {beta_efe_meas:+.4f}   isolated RAR {beta_rar:+.4f}")
def confounded_slope_mc(beta_true, n=4000):
    """Monte Carlo: draw true log g_bar from the sample's TRUE spread, build log g_obs from beta_true,
    add the tabulated measurement errors, regress the RATIO on the MEASURED g_bar."""
    out = []
    b0 = np.mean(lgbar)
    for _ in range(n):
        bt = b0 + rng.normal(0, math.sqrt(var_b_true), N)
        ot = np.mean(lgobs) + (1.0 + beta_true) * (bt - b0)
        B = bt + rng.normal(0, 1, N) * elgbar
        O = ot + rng.normal(0, 1, N) * elgobs
        out.append(np.polyfit(B, O - B, 1)[0])
    return np.array(out)
mc_efe = confounded_slope_mc(beta_efe_meas); mc_rar = confounded_slope_mc(beta_rar)
P(f"      OBSERVED slope of log(g_obs/g_bar) on log(g_bar): {s_obs:+.3f} +- {s_err:.3f} (bootstrap)")
P(f"      Monte Carlo under EFE-law truth    : {mc_efe.mean():+.3f} +- {mc_efe.std():.3f}   "
  f"-> observed is {(s_obs-mc_efe.mean())/mc_efe.std():+.2f} sigma")
P(f"      Monte Carlo under isolated-RAR truth: {mc_rar.mean():+.3f} +- {mc_rar.std():.3f}   "
  f"-> observed is {(s_obs-mc_rar.mean())/mc_rar.std():+.2f} sigma")
sep = abs(mc_efe.mean() - mc_rar.mean()) / math.sqrt(0.5 * (mc_efe.std()**2 + mc_rar.std()**2))
P(f"      SEPARATION between the two hypotheses AFTER the confound: {sep:.2f} sigma")
P("      -> the shared-g_bar confound drags BOTH predictions to the same place; the propose stage compared")
P("         the observed -0.187 against the UNCONFOUNDED -0.021 and -0.478 and called it 'closer to the EFE")
P("         law'.  Against the confounded distributions it is not.")
ck("the Coma own-g_bar shape test separates the two hypotheses at >= 2 sigma", sep >= 2.0, f"{sep:.2f} sigma")

P("\n      --- SHAPE TEST 1b: the UNCONFOUNDED form -- regress log g_obs on log g_bar (no shared variable) ---")
s2, s2e = wls_slope(lgbar, lgobs)
atten = var_b_true / var_b_tot
P(f"      predicted slope   EFE theorem {1.0+beta_efe_meas:.3f}   isolated RAR {1.0+beta_rar:.3f}"
  f"   (both x the regression-dilution factor {atten:.3f} = {atten*(1+beta_efe_meas):.3f} / {atten*(1+beta_rar):.3f})")
P(f"      OBSERVED: {s2:+.3f} +- {s2e:.3f}")
z_efe = (s2 - atten * (1 + beta_efe_meas)) / s2e; z_rar = (s2 - atten * (1 + beta_rar)) / s2e
P(f"      -> {z_efe:+.2f} sigma from the EFE law, {z_rar:+.2f} sigma from the isolated RAR")
ck("unconfounded shape test prefers the EFE law over the isolated RAR by >= 2 sigma",
   abs(z_rar) - abs(z_efe) >= 2.0, f"|z_RAR|-|z_EFE| = {abs(z_rar)-abs(z_efe):+.2f}")

P("\n      --- SHAPE TEST 2: the ENVIRONMENT axis (NEW here; shares nothing with g_obs or g_bar) ---")
lgext = np.log10(ye)
pred_env_slope = np.polyfit(lgext, pr, 1)[0]
s3, s3e = wls_slope(lgext, lr)
P(f"      theorem predicts d log(M_dyn/M_b)/d log g_ext = {pred_env_slope:+.4f}")
P(f"      isolated RAR (no environment at all) predicts  {0.0:+.4f}")
P(f"      OBSERVED: {s3:+.3f} +- {s3e:.3f}   -> {(s3-pred_env_slope)/s3e:+.2f} sigma from the theorem, "
  f"{s3/s3e:+.2f} sigma from no-environment")
ck("the environment axis detects the predicted g_ext dependence at >= 2 sigma", abs(s3 / s3e) >= 2.0,
   f"{abs(s3/s3e):.2f} sigma from zero, and the theorem's own prediction is only {pred_env_slope:+.3f}")
P("      NOTE against interest: the theorem's own environment slope is only -0.3 over a sample spanning")
P(f"      {np.ptp(lgext):.2f} dex in g_ext, i.e. a {abs(pred_env_slope)*np.ptp(lgext):.3f} dex swing against a")
P(f"      {lr.std():.3f} dex scatter.  The axis is clean but the lever is small.")

# ---- Upsilon lever, measured
P("\n      --- UPSILON LEVER, measured by re-running the whole pipeline at Upsilon x1.5 ---")
for scale in (1.0, 1.5):
    lrx, prx, yex, lbx = coma_prediction(A0["canonical"], ml_scale=scale, ye_mode="newtonian")
    sx, _ = wls_slope(lbx, lrx); sx2, _ = wls_slope(lbx, lgobs); sx3, _ = wls_slope(np.log10(yex), lrx)
    P(f"        Upsilon x{scale:.1f}: median residual {np.median(lrx-prx):+.3f} dex   own-g_bar slope {sx:+.3f}   "
      f"g_obs-on-g_bar slope {sx2:+.3f}   g_ext slope {sx3:+.3f}")
lr1, pr1, _, lb1 = coma_prediction(A0["canonical"], ml_scale=1.0, ye_mode="newtonian")
lr2, pr2, _, lb2 = coma_prediction(A0["canonical"], ml_scale=1.5, ye_mode="newtonian")
lever_amp = (np.median(lr2 - pr2) - np.median(lr1 - pr1)) / math.log10(1.5)
s1s, _ = wls_slope(lb1, lr1); s2s, _ = wls_slope(lb2, lr2)
P(f"      d log(M_dyn/M_b)/d log Upsilon = {lever_amp:+.4f}  (exact value -1.000: Upsilon is the denominator)")
P(f"      d(shape slope)/d log Upsilon    = {(s2s-s1s)/math.log10(1.5):+.4f}  (a global Upsilon shift translates")
P("        every point vertically and cannot change a slope -- the discriminating half is Upsilon-immune)")
ck("amplitude Upsilon lever is -1.000 as predicted", abs(lever_amp + 1.0) < 0.02, f"{lever_amp:+.4f}")
ck("shape Upsilon lever is 0.000 as predicted", abs((s2s - s1s) / math.log10(1.5)) < 0.05,
   f"{(s2s-s1s)/math.log10(1.5):+.4f}")

# ---- mutations and the alternatives
P("\n      --- MUTATIONS and the NEWTONIAN / LCDM alternatives ---")
for lab, a0 in (("canonical", A0["canonical"]), ("alt", A0["alt"]), ("a_0 x 3", 3 * A0["canonical"]),
                ("a_0 / 3", A0["canonical"] / 3), ("a_0 x 30", 30 * A0["canonical"])):
    lrm, prm, yem, _ = coma_prediction(a0, ye_mode="newtonian", a0_kernel=a0)
    P(f"        {lab:12s}: median y_e {np.median(yem):7.4f}  predicted {np.median(prm):+.3f}  "
      f"residual {np.median(lrm-prm):+.3f} dex")
res_can = np.median(coma_prediction(A0["canonical"], ye_mode="newtonian")[0] -
                    coma_prediction(A0["canonical"], ye_mode="newtonian")[1])
res_x3 = np.median(coma_prediction(3 * A0["canonical"], ye_mode="newtonian", a0_kernel=3 * A0["canonical"])[0] -
                   coma_prediction(3 * A0["canonical"], ye_mode="newtonian", a0_kernel=3 * A0["canonical"])[1])
ck("MUTATION: a_0 x 3 is WORSE than the canonical footing", abs(res_x3) > abs(res_can),
   f"|{res_x3:+.3f}| vs |{res_can:+.3f}| -- REPORTED AGAINST INTEREST: the mutation control FAILS. "
   "The Coma amplitude prefers a LARGER a_0; it nulls somewhere between 3x and 30x canonical, the same "
   "direction as the cluster residual (item 56 needed 18.4x).  A test whose best fit is 10x the footing "
   "is not measuring a_0.")
P(f"        NEWTONIAN alternative (nu = 1): predicted log ratio 0.000 -> residual {np.median(lr):+.3f} dex")
P("        LCDM alternative: the discrepancy is set by the halo the UDG sits in, i.e. by its own M_b through")
P("        abundance matching, and by cluster tides -- it PREDICTS an own-mass dependence where the theorem")
P("        forbids one.  With the confound above, the Coma sample cannot tell the two apart.")

# ------------------------------------------------------------------ (D) the Local Group, confound measured
P("\n  (D) LOCAL GROUP dwarfs -- the propose stage argued the confound; here it is MEASURED.")
dw = []
with open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv")) as fh:
    for r in csv.DictReader(fh):
        try:
            D = float(r["D"]); VM = float(r["VMag"]); R2 = float(r["R2"]); sg = float(r["sigma*"])
        except (ValueError, KeyError, TypeError): continue
        if r["SubG"] not in ("MW", "M31") or R2 <= 0 or sg <= 0: continue
        MHI = 0.0
        try: MHI = float(r["M.HI"]) * 1e6
        except (ValueError, TypeError): pass
        dw.append(dict(sub=r["SubG"], D=D, LV=10**(0.4 * (4.83 - VM)), rh=R2 / 1000.0, sig=sg * 1e3, MHI=MHI))
P(f"      {len(dw)} MW+M31 dwarfs with sigma and half-light radius")
def lg_observed(ups_V=2.0):
    lr_, lb_, lge_ = [], [], []
    for d in dw:
        Mdyn = 3.0 * d["sig"]**2 * (d["rh"] * kpc) / G / Msun    # Wolf: ENCLOSED half-light mass
        Mb = 0.5 * (ups_V * d["LV"] + 1.33 * d["MHI"])           # enclosed baryons (half of the total)
        if Mb <= 0 or Mdyn <= 0: continue
        Mhost = 1.0e12 if d["sub"] == "MW" else 1.5e12
        gext = G * Mhost * Msun / (d["D"] * kpc)**2
        lr_.append(math.log10(Mdyn / Mb)); lb_.append(math.log10(Mb)); lge_.append(math.log10(gext))
    return np.array(lr_), np.array(lb_), np.array(lge_)
lrLG, lbLG, lgeLG = lg_observed()
sM = np.polyfit(lbLG, lrLG, 1)[0]; sE = np.polyfit(lgeLG, lrLG, 1)[0]
P(f"      MEASURED (Upsilon_V = 2): N={len(lrLG)}  own-mass slope {sM:+.3f}   g_ext slope {sE:+.3f}")
P("      A GENUINE NULL, built from a CONTROLLED TRUTH rather than from the data: for each dwarf take its")
P("      catalogue distance as truth, IMPOSE the theorem's ratio exactly, synthesise the luminosity that")
P("      follows, then let a mock observer mis-measure the distance by 0.10 dex and the flux by 0.10 dex.")
P("      NOTE WHAT THE 'input slope' COLUMN SHOWS BELOW.  With the theorem EXACTLY true and NO errors at")
P("      all, plotting M_dyn/M_b against M_b still returns -0.54, not 0 -- because the abscissa is the")
P("      ordinate's own denominator and the dwarfs' M_dyn spans decades.  The propose stage compared the")
P("      measured -0.509 against a nominal 0.000; the correct comparison is against -0.54.  The 'signal'")
P("      is the plotting geometry, before any measurement error is added at all.")
resid_obs = float(np.std(lrLG - np.polyval(np.polyfit(lbLG, lrLG, 1), lbLG)))
P(f"      observed residual scatter about the own-mass fit: {resid_obs:.3f} dex -- the mock is given an")
P("      intrinsic M_b scatter of the same size, so that its error bars are comparable to the data's.")
def lg_null(truth, a0=A0["canonical"], D_err=0.10, F_err=0.10, ups_V=2.0, sig_int=None):
    """truth = 'efe' (ratio fixed by g_ext alone) or 'rar' (ratio fixed by the dwarf's own g_bar)."""
    if sig_int is None: sig_int = resid_obs
    lr_, lb_, lge_, tr_ = [], [], [], []
    for d in dw:
        Dt = d["D"]; theta = d["rh"] / Dt                    # true angular half-light size
        Mdyn_t = 3.0 * d["sig"]**2 * (d["rh"] * kpc) / G / Msun
        Mhost = 1.0e12 if d["sub"] == "MW" else 1.5e12
        gext_t = G * Mhost * Msun / (Dt * kpc)**2
        if truth == "efe":
            Rt = R_theory(gN_from_gobs(gext_t, a0) / a0)
        else:
            Mb_seed = max(0.5 * (ups_V * d["LV"] + 1.33 * d["MHI"]), 1.0)
            gbar_t = G * Mb_seed * Msun / (d["rh"] * kpc)**2
            Rt = nu_y(gbar_t / a0)
        Mb_t = Mdyn_t / Rt                                   # the baryons the truth demands
        Mb_t *= 10**rng.normal(0, sig_int)                    # intrinsic spread, matched to the data
        flux = Mb_t / Dt**2                                  # what the observer actually measures
        fD = 10**rng.normal(0, D_err); fF = 10**rng.normal(0, F_err)
        Do = Dt * fD; rho = theta * Do
        Mdyn_o = 3.0 * d["sig"]**2 * (rho * kpc) / G / Msun
        Mb_o = flux * fF * Do**2
        gext_o = G * Mhost * Msun / (Do * kpc)**2
        if Mb_o <= 0: continue
        lr_.append(math.log10(Mdyn_o / Mb_o)); lb_.append(math.log10(Mb_o)); lge_.append(math.log10(gext_o))
        tr_.append(math.log10(Mdyn_t / Mb_t));
    return np.array(lr_), np.array(lb_), np.array(lge_), np.array(tr_)
P("      truth  |  input slope (no errors)  ->  slope a mock observer RECOVERS  |  manufactured shift")
store = {}
for truth in ("efe", "rar"):
    a0_, b0_, c0_, t0_ = lg_null(truth, D_err=0.0, F_err=0.0, sig_int=0.0)   # noiseless: the input slopes
    inM = np.polyfit(b0_, t0_, 1)[0]; inE = np.polyfit(c0_, t0_, 1)[0]
    nm, ne = [], []
    for _ in range(400):
        a, b, c, t = lg_null(truth)
        nm.append(np.polyfit(b, a, 1)[0]); ne.append(np.polyfit(c, a, 1)[0])
    nm = np.array(nm); ne = np.array(ne); store[truth] = (nm, ne)
    P(f"      {truth:4s}   own-mass {inM:+.3f} -> {nm.mean():+.3f} +- {nm.std():.3f}   shift {nm.mean()-inM:+.3f}")
    P(f"             g_ext    {inE:+.3f} -> {ne.mean():+.3f} +- {ne.std():.3f}   shift {ne.mean()-inE:+.3f}")
nm_efe, ne_efe = store["efe"]; nm_rar, ne_rar = store["rar"]
sepM = abs(nm_efe.mean() - nm_rar.mean()) / math.sqrt(0.5 * (nm_efe.std()**2 + nm_rar.std()**2))
sepE = abs(ne_efe.mean() - ne_rar.mean()) / math.sqrt(0.5 * (ne_efe.std()**2 + ne_rar.std()**2))
P(f"      observed: own-mass {sM:+.3f} (efe {(sM-nm_efe.mean())/nm_efe.std():+.1f} sigma, "
  f"rar {(sM-nm_rar.mean())/nm_rar.std():+.1f} sigma)")
P(f"      observed: g_ext    {sE:+.3f} (efe {(sE-ne_efe.mean())/ne_efe.std():+.1f} sigma, "
  f"rar {(sE-ne_rar.mean())/ne_rar.std():+.1f} sigma)")
P(f"      SEPARATION between the two truths after the confound: own-mass {sepM:.2f} sigma, g_ext {sepE:.2f} sigma")
P("      READ THIS AGAINST INTEREST: a 0.10 dex distance error alone manufactures roughly -0.5 in the")
P("      own-mass slope where the theorem's truth is 0.000, which is exactly where the data sit.  Neither")
P("      truth reproduces BOTH axes, so the Local Group sample is not merely confounded -- it rejects both")
P("      hypotheses, which means the modelling (Upsilon_V, the host mass, the Wolf estimator) dominates.")
ck("the Local Group data are consistent with at least ONE of the two truths on BOTH axes at < 3 sigma",
   (abs((sM - nm_efe.mean()) / nm_efe.std()) < 3 and abs((sE - ne_efe.mean()) / ne_efe.std()) < 3) or
   (abs((sM - nm_rar.mean()) / nm_rar.std()) < 3 and abs((sE - ne_rar.mean()) / ne_rar.std()) < 3),
   "neither truth fits both axes" )

# ---- what it would take
P("\n  (E) WHAT WOULD MAKE THE SHAPE TEST DECISIVE (a power calculation, not a wish).")
sig_scat = float(lr.std())
delta = abs(beta_rar - beta_efe_meas)
P(f"      the two hypotheses differ by {delta:.3f} in d log(M_dyn/M_b)/d log g_bar,own.")
P(f"      residual scatter about the relation on the clean sample: {sig_scat:.3f} dex.")
P(f"      the Coma sample's TRUE spread in log g_bar is {math.sqrt(var_b_true):.3f} dex "
  f"(the proposer's own data note asked for >= 1.5 dex -- it is {1.5/math.sqrt(var_b_true):.0f}x short).")
for rng_dex in (0.1, 0.3, 0.5, 1.0, 1.5):
    sx = rng_dex / math.sqrt(12.0)                          # sd of a uniform spread of that width
    Nreq = (3.0 * sig_scat / (delta * sx))**2
    P(f"        intrinsic spread {rng_dex:4.1f} dex in own g_bar  ->  N = {Nreq:8.0f} systems for a 3-sigma decision")
P("      and every one of them must have log g_bar measured to much better than the spread, or the")
P("      shared-variable confound above eats the signal whatever N is.")

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 118)
P("  VERDICT ON K3")
P("=" * 118)
P(f"  (1) measured quantities?  YES -- g_obs/g_bar at R_e and host-centric distance, both tabulated.")
P(f"  (2) a_0 with a PREDICTED coefficient?  YES in form, but the amplitude misses by "
  f"{best[1][0]:+.2f} dex ({10**abs(best[1][0]):.0f}x) on the most favourable convention.")
P(f"  (3) RAR-class scatter?  NO -- residual scatter {lr.std():.3f} dex about a prediction that is "
  f"{abs(best[1][0]):.2f} dex off.")
P(f"  (4) unstated?  NO -- Milgrom 1986/2009 has the theorem; Freundlich+2022 has the Coma failure.")
P(f"  (5) restatement of v^4 = G M_b a_0?  NO (executed above: the BTFR forces -1/2 in own g_bar, the")
P(f"      theorem forces ~0; they are different statements).")
P(f"  THE DISCRIMINATING HALF -- the shape test -- is Upsilon-immune but CONFOUNDED and UNDERPOWERED:")
P(f"      the two hypotheses separate by only {sep:.2f} sigma on the clean sample after the shared-g_bar")
P(f"      confound is modelled, and the environment axis gives {abs(s3/s3e):.2f} sigma from zero.")
P("  ==> CANDIDATE K3 FAILS.  The theorem is real and exactly verified; the law it implies is already")
P("      credited to Milgrom; its amplitude is refuted at ~1 dex; and the one novel part -- the population")
P("      shape test -- cannot be decided by the only clean sample on disk.")
sys.exit(ck.done())
