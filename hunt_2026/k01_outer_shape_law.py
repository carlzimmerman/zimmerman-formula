#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k01_outer_shape_law.py -- ANGLE 4, CANDIDATE K1: THE OUTER-CURVE SHAPE LAW.

DERIVATION (from the field equation, not from data).  In QUMOND/AQUAL the in-plane field obeys the algebraic
relation g_obs = nu(y) g_bar, y = g_bar/a_0, wherever the symmetry makes the curl field vanish (exactly for
spherical / cylindrical / plane symmetry; to a few per cent for a thin disc -- that residual is candidate K4).
Differentiate in ln r.  With

    s_bar = d ln g_bar / d ln r      (a SHAPE of the baryon distribution: amplitude-free, so Upsilon-light)
    sigma = d ln v    / d ln r       (the rotation curve's log slope: distance-free AND inclination-free)
    L(y)  = d ln nu   / d ln y

and v^2 = r g_obs, one gets the EXACT identity

        2 sigma  =  1 + (1 + L(y)) s_bar                                     (*)

Route A, nu(y) = 1/(1 - e^{-sqrt y}).  Put s = sqrt(y).  Then, in closed form,

        nu = 1/(1 - e^{-s}),   x = g_obs/a_0 = y nu = s^2/(1 - e^{-s}),   L = -(s/2)/(e^s - 1)

so L runs monotonically from -1/2 (deep) to 0 (Newtonian) and x from 0 to infinity.  ELIMINATING s between
sigma and x gives a UNIVERSAL PARAMETER-FREE CURVE between two measured quantities.  Beyond the baryons the
system is a point mass, s_bar = -2 exactly, and (*) collapses to

        sigma  =  -1/2 - L(y)   =   -1/2 + s/(2(e^s - 1)),      x = v^2/(a_0 r) = s^2/(1 - e^{-s})

i.e.  sigma = F(v^2/(a_0 r))  with NO baryonic mass, NO stellar M/L, NO geometry factor anywhere.
Equivalently: M_N(r) = r^2 a_0 y(x)/G is CONSTANT with radius outside the baryons -- Gauss's law for the
modified field, read backwards from the rotation curve alone.

WHAT IS TESTED HERE.  Per SPARC galaxy, over an OUTER window: measure sigma from v(r), measure s_bar from the
SPARC V_gas/V_disk/V_bul profiles (a shape, not an amplitude), take x = <g_obs>/a_0, and compare the measured
sigma with the prediction of (*).  Then fit a_0 by minimising the same residual -- an a_0 measurement whose
d log a_0 / d log Upsilon is essentially zero by construction, because Upsilon enters only through s_bar.

CHECKS THAT CAN FAIL; MUTATIONS (a_0 x3, a_0 /3, nu = 1 Newtonian, kernel swapped for alpha=1); BOTH FOOTINGS;
the Newtonian/LambdaCDM alternative computed beside the framework; the Upsilon lever computed numerically.
"""
import os, math, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(4001)

# ------------------------------------------------------------------ the kernel, in the s = sqrt(y) variable
def nu_s_(s):   return 1.0/(1.0 - np.exp(-s))
def x_of_s(s):  return s*s/(1.0 - np.exp(-s))
def L_of_s(s):  return -(s/2.0)/np.expm1(s)
def s_of_x(x):
    """invert x = s^2/(1-e^{-s}); x is monotone increasing in s."""
    if x <= 0: return 0.0
    lo, hi = 1e-8, 1.0
    while x_of_s(hi) < x: hi *= 2.0
    return brentq(lambda t: x_of_s(t) - x, lo, hi, xtol=1e-14, rtol=1e-14)
# alpha = 1 kernel (the equation book's nu = sqrt(1+1/y)) for the mutation control
def L_alpha1_of_y(y): return -0.5/(1.0 + y)                      # d ln nu / d ln y for nu = sqrt(1+1/y)
def x_alpha1_of_y(y): return y*math.sqrt(1.0 + 1.0/y)
def y_of_x_alpha1(x):  return 0.5*(math.sqrt(x*x*4 + 1) - 1)/1.0 if False else brentq(lambda t: x_alpha1_of_y(t)-x, 1e-12, 1e12)

P("="*118); P("CANDIDATE K1 -- the outer-curve shape law:  2 dlnv/dlnr = 1 + (1 + L(y)) dln g_bar/dln r"); P("="*118)
# --- self-consistency of the closed forms (checks that CAN fail)
for s in [0.05, 0.3, 1.0, 2.5, 6.0]:
    y = s*s
    num = (math.log(nu_s_(s*1.000001)) - math.log(nu_s_(s*0.999999)))/(math.log((s*1.000001)**2) - math.log((s*0.999999)**2))
    ck(f"L(y) closed form at s={s}", abs(num - L_of_s(s)) < 1e-6, f"numeric {num:.9f} vs closed {L_of_s(s):.9f}")
ck("L -> -1/2 deep", abs(L_of_s(1e-6) + 0.5) < 1e-6, f"{L_of_s(1e-6):.9f}")
ck("L -> 0 Newtonian", abs(L_of_s(40.0)) < 1e-15, f"{L_of_s(40.0):.3e}")
ck("x(s) = y nu(y)", abs(x_of_s(1.3) - 1.3**2*nu_s_(1.3)) < 1e-14)
P("")
P("  the parameter-free curve sigma = F(x) for a point mass (s_bar = -2):")
P(f"  {'g_obs/a_0':>10} {'y=g_bar/a_0':>12} {'L':>9} {'sigma=dlnv/dlnr':>16} {'Newtonian sigma':>16}")
for s in [0.2, 0.4, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]:
    P(f"  {x_of_s(s):10.3f} {s*s:12.3f} {L_of_s(s):9.4f} {-0.5 - L_of_s(s):16.4f} {-0.5:16.4f}")
P("")

# ------------------------------------------------------------------ SPARC
def slopes(gal, ups_d, ups_b, frac_outer=0.5, nmin=5):
    """Return per-galaxy outer-window (sigma, err, s_bar, <g_obs>, <g_bar>, r) with the given M/L."""
    r, vo, ev = gal["r"], gal["vobs"], gal["ev"]
    gb = (gal["vg"]*np.abs(gal["vg"]) + ups_d*gal["vd"]**2 + ups_b*gal["vb"]**2)/r*KMS2_KPC
    go = vo**2/r*KMS2_KPC
    m = (gb > 0) & (vo > 0) & (ev > 0)
    r, vo, ev, gb, go = r[m], vo[m], ev[m], gb[m], go[m]
    n = len(r)
    if n < nmin: return None
    k = max(nmin, int(math.ceil(frac_outer*n)))
    sl = slice(n - k, n)
    R, V, EV, GB, GO = r[sl], vo[sl], ev[sl], gb[sl], go[sl]
    if R[-1]/R[0] < 1.25: return None                       # need a lever arm in ln r
    lr = np.log(R); w = (V/np.maximum(EV, 0.02*V + 0.5))**2   # weights on ln v (error floor: 2% or 0.5 km/s)
    A = np.vstack([lr, np.ones_like(lr)]).T
    W = np.diag(w)
    try: cov = np.linalg.inv(A.T @ W @ A)
    except np.linalg.LinAlgError: return None
    beta = cov @ (A.T @ W @ np.log(V))
    sig, esig = beta[0], math.sqrt(abs(cov[0, 0]))
    sb = np.polyfit(lr, np.log(GB), 1)[0]                    # baryonic shape slope (photometric, smooth)
    return dict(name=gal["name"], sigma=sig, esigma=esig, sbar=sb, gobs=float(np.exp(np.mean(np.log(GO)))),
                gbar=float(np.exp(np.mean(np.log(GB)))), rmid=float(np.exp(np.mean(lr))), n=k, Mb=gal["Mb"],
                D=gal["D"], eD=gal["eD"], Q=gal["Q"], fgas=1.33*gal["MHI"]*1e9/max(gal["Mb"], 1.0))

def sigma_pred(x, sbar):
    """predicted d ln v/d ln r from the measured acceleration x = g_obs/a_0 and the baryonic shape slope."""
    s = s_of_x(x); return 0.5*(1.0 + (1.0 + L_of_s(s))*sbar)

gals = load_sparc(qmax=2, incmin=30, npts=8)
P(f"  SPARC: {len(gals)} galaxies with Q<=2, i>=30 deg, >=8 points")

def build(ups_d, ups_b=UPS_B, frac=0.5):
    out = []
    for g in gals:
        d = slopes(g, ups_d, ups_b, frac_outer=frac)
        if d is not None: out.append(d)
    return out
S = build(UPS_D)
P(f"  outer-window slope measurable in {len(S)} galaxies (outer 50% of points, >=5 points, r range >=1.25x)")
sb = np.array([d["sbar"] for d in S])
P(f"  baryonic shape slope s_bar over the window: median {np.median(sb):.2f}, 16-84% {np.percentile(sb,16):.2f} to {np.percentile(sb,84):.2f}")
P(f"  (point mass would be exactly -2.00; a razor-thin exponential disc is steeper than -2 inside ~4 R_d)")
P("")

# ------------------------------------------------------------------ the law test, both footings + mutations
def test(S, a0, label, kernel="routeA", quiet=False):
    obs, pred, err, xs = [], [], [], []
    for d in S:
        x = d["gobs"]/a0
        if kernel == "routeA":
            sp = sigma_pred(x, d["sbar"])
        elif kernel == "newton":
            sp = 0.5*(1.0 + d["sbar"])
        elif kernel == "alpha1":
            y = y_of_x_alpha1(x); sp = 0.5*(1.0 + (1.0 + L_alpha1_of_y(y))*d["sbar"])
        obs.append(d["sigma"]); pred.append(sp); err.append(d["esigma"]); xs.append(x)
    obs, pred, err, xs = map(np.array, (obs, pred, err, xs))
    res = obs - pred
    rms = res.std(); med = np.median(res)
    # regression of observed on predicted (1.00 = the law holds with the right amplitude)
    A = np.vstack([pred, np.ones_like(pred)]).T
    beta, *_ = np.linalg.lstsq(A, obs, rcond=None)
    r_ = np.corrcoef(pred, obs)[0, 1]
    chi2 = float(np.sum((res/np.maximum(err, 1e-3))**2))
    if not quiet:
        P(f"  {label:44} N={len(obs):3d}  median resid {med:+.4f}  rms {rms:.4f}  r={r_:+.3f}  "
          f"regression {beta[0]:.3f}  chi2/N {chi2/len(obs):8.2f}")
    return dict(med=med, rms=rms, r=r_, slope=beta[0], chi2=chi2, n=len(obs), res=res, pred=pred, obs=obs, x=xs)

P("  THE TEST -- observed outer slope vs the prediction of (*), no baryonic amplitude used:")
R = {}
for foot, a0 in A0.items():
    R[foot] = test(S, a0, f"Route A, {foot} a_0 = {a0:.3e}")
R["newton"] = test(S, A0["canonical"], "NEWTONIAN alternative (nu = 1)", kernel="newton")
R["alpha1"] = test(S, A0["canonical"], "MUTATION: alpha=1 kernel nu=sqrt(1+1/y)", kernel="alpha1")
R["mutx3"]  = test(S, 3*A0["canonical"], "MUTATION: a_0 x 3")
R["mutd3"]  = test(S, A0["canonical"]/3, "MUTATION: a_0 / 3")
R["deep"]   = test(S, 1e-30, "MUTATION: a_0 -> 0 (pure deep MOND, L=-1/2)")
P("")
ck("Route A beats the Newtonian alternative in rms", R["canonical"]["rms"] < R["newton"]["rms"],
   f"{R['canonical']['rms']:.4f} vs {R['newton']['rms']:.4f}")
ck("Route A beats a_0 x 3 in rms", R["canonical"]["rms"] < R["mutx3"]["rms"], f"{R['canonical']['rms']:.4f} vs {R['mutx3']['rms']:.4f}")
ck("Route A beats a_0 / 3 in rms", R["canonical"]["rms"] < R["mutd3"]["rms"], f"{R['canonical']['rms']:.4f} vs {R['mutd3']['rms']:.4f}")
ck("Route A beats pure deep MOND in rms", R["canonical"]["rms"] < R["deep"]["rms"], f"{R['canonical']['rms']:.4f} vs {R['deep']['rms']:.4f}")
ck("law scatter <= 0.10 in d ln v/d ln r", R["canonical"]["rms"] <= 0.10, f"rms {R['canonical']['rms']:.4f}")
ck("regression of observed on predicted within 20% of 1", abs(R["canonical"]["slope"] - 1) < 0.2, f"{R['canonical']['slope']:.3f}")
P("")

# ------------------------------------------------------------------ a_0 measured from SHAPE alone
def fit_a0(S, ups_d=UPS_D, frac=0.5, boot=0, kernel="routeA"):
    SS = build(ups_d, frac=frac) if (ups_d != UPS_D or frac != 0.5) else S
    def cost(la0):
        a0 = 10**la0
        c = 0.0
        for d in SS:
            sp = sigma_pred(d["gobs"]/a0, d["sbar"])
            c += ((d["sigma"] - sp)/max(d["esigma"], 0.02))**2
        return c
    r = minimize_scalar(cost, bounds=(-11.5, -8.5), method="bounded", options=dict(xatol=1e-6))
    best = r.x
    if boot:
        vals = []
        for _ in range(boot):
            idx = rng.integers(0, len(SS), len(SS)); sub = [SS[i] for i in idx]
            def c2(la0):
                a0 = 10**la0; return sum(((d["sigma"] - sigma_pred(d["gobs"]/a0, d["sbar"]))/max(d["esigma"], 0.02))**2 for d in sub)
            vals.append(minimize_scalar(c2, bounds=(-11.5, -8.5), method="bounded", options=dict(xatol=1e-5)).x)
        return best, float(np.std(vals)), np.array(vals)
    return best, None, None

la, sa, _ = fit_a0(S, boot=200)
P(f"  a_0 MEASURED FROM ROTATION-CURVE SHAPE ALONE (no baryonic amplitude, no M/L):")
P(f"    log10 a_0 = {la:.4f} +- {sa:.4f}   ->   a_0 = {10**la:.3e}  [{10**(la-sa):.2e}, {10**(la+sa):.2e}] m/s^2")
P(f"    canonical 9.36e-11 is {(la - math.log10(A0['canonical']))/sa:+.2f} sigma away; "
  f"alt 1.13e-10 is {(la - math.log10(A0['alt']))/sa:+.2f} sigma away")
ck("shape-only a_0 is within 0.3 dex of a footing",
   min(abs(la - math.log10(A0['canonical'])), abs(la - math.log10(A0['alt']))) < 0.3,
   f"nearest footing {min(abs(la-math.log10(A0['canonical'])), abs(la-math.log10(A0['alt']))):.3f} dex")
P("")

# ------------------------------------------------------------------ THE UPSILON LEVER, numerically
P("  THE UPSILON LEVER (the thing that killed three earlier candidates):")
lev = []
for u in [0.3, 0.4, 0.5, 0.6, 0.7]:
    l_, _, _ = fit_a0(S, ups_d=u)
    lev.append((u, l_))
    P(f"    Upsilon_disk = {u:.2f}   ->   log10 a_0 = {l_:.4f}   (a_0 = {10**l_:.3e})")
lu = np.log10([u for u, _ in lev]); la_ = np.array([l for _, l in lev])
slope_ups = np.polyfit(lu, la_, 1)[0]
P(f"    d log a_0 / d log Upsilon = {slope_ups:+.4f}      (deep-tail rung: -0.647; KiDS dwarf lens stack: -1.046)")
ck("Upsilon lever |d log a_0/d log Upsilon| < 0.15", abs(slope_ups) < 0.15, f"{slope_ups:+.4f}")
P("")
# window robustness
P("  window robustness (fraction of each curve used as the 'outer' window):")
for fr in [0.35, 0.5, 0.65]:
    l_, _, _ = fit_a0(S, frac=fr)
    P(f"    outer {int(100*fr)}% of points  ->  log10 a_0 = {l_:.4f}   (N = {len(build(UPS_D, frac=fr))})")
P("")

# ------------------------------------------------------------------ is there any information beyond 'the curve is flat'?
P("  IS THERE INFORMATION BEYOND 'the outer curve is flat'?  (the restatement guard)")
P("  v^4 = G M_b a_0 predicts sigma = 0 identically.  Compare that null with the law:")
res_flat = np.array([d["sigma"] for d in S])
P(f"    sigma = 0 (deep-MOND/BTFR limit):        rms {res_flat.std():.4f}, median {np.median(res_flat):+.4f}")
P(f"    Route A shape law, canonical:            rms {R['canonical']['rms']:.4f}, median {R['canonical']['med']:+.4f}")
P(f"    Newtonian shape law (nu = 1):            rms {R['newton']['rms']:.4f}, median {R['newton']['med']:+.4f}")
ck("the shape law beats sigma = 0 (so it is NOT the BTFR restated)", R["canonical"]["rms"] < res_flat.std(),
   f"{R['canonical']['rms']:.4f} vs {res_flat.std():.4f}")
P("")

# ------------------------------------------------------------------ the point-mass (fully baryon-free) subsample
P("  THE FULLY BARYON-FREE FORM: galaxies whose outer window really is point-mass-like (s_bar in [-2.25,-1.75])")
PM = [d for d in S if -2.25 <= d["sbar"] <= -1.75]
if len(PM) >= 8:
    o = np.array([d["sigma"] for d in PM]); e = np.array([d["esigma"] for d in PM])
    x = np.array([d["gobs"]/A0["canonical"] for d in PM])
    p = np.array([-0.5 - L_of_s(s_of_x(xx)) for xx in x])
    P(f"    N = {len(PM)};  observed sigma range {o.min():+.3f} to {o.max():+.3f};  predicted {p.min():+.3f} to {p.max():+.3f}")
    P(f"    rms(obs - pred) = {(o-p).std():.4f};  r = {np.corrcoef(o,p)[0,1]:+.3f};  "
      f"regression {np.polyfit(p,o,1)[0]:.3f}")
    def cost_pm(la0):
        a0 = 10**la0
        return sum(((d["sigma"] - (-0.5 - L_of_s(s_of_x(d["gobs"]/a0))))/max(d["esigma"], 0.02))**2 for d in PM)
    rr = minimize_scalar(cost_pm, bounds=(-11.5, -8.5), method="bounded", options=dict(xatol=1e-6))
    P(f"    a_0 from this fully baryon-free subsample: {10**rr.x:.3e} m/s^2   (log10 {rr.x:.4f})")
    P(f"    d log a_0/d log Upsilon here is EXACTLY 0 -- no baryonic quantity of any kind enters")
    ck("baryon-free subsample has >= 8 galaxies", True, f"N={len(PM)}")
else:
    P(f"    only {len(PM)} galaxies -- not enough")
    ck("baryon-free subsample has >= 8 galaxies", False, f"N={len(PM)}")
P("")
# ------------------------------------------------------------------ where does the 0.16 rms come from?
P("  ANATOMY OF THE RESIDUAL (is it measurement noise, or does the law genuinely fail?)")
res = R["canonical"]["res"]; err = np.array([d["esigma"] for d in S])
P(f"    rms residual {res.std():.4f} against a median slope error of {np.median(err):.4f}  ->  chi2/N = {R['canonical']['chi2']/len(S):.1f}")
P(f"    so the residual is {res.std()/np.median(err):.1f}x the formal slope errors: the scatter is REAL, not noise")
P("    split by baryonic shape slope s_bar (how close the window is to the point-mass regime):")
for lo, hi in [(-3.0,-1.75), (-1.75,-1.25), (-1.25,-0.75), (-0.75,0.5)]:
    sub = [i for i,d in enumerate(S) if lo <= d["sbar"] < hi]
    if len(sub) < 6: continue
    P(f"      s_bar in [{lo:+.2f},{hi:+.2f})  N={len(sub):3d}  median resid {np.median(res[sub]):+.4f}  rms {res[sub].std():.4f}")
P("    split by gas fraction (Upsilon matters least where gas dominates):")
for lo, hi in [(0.0,0.3),(0.3,0.6),(0.6,2.0)]:
    sub = [i for i,d in enumerate(S) if lo <= d["fgas"] < hi]
    if len(sub) < 6: continue
    P(f"      f_gas in [{lo:.1f},{hi:.1f})   N={len(sub):3d}  median resid {np.median(res[sub]):+.4f}  rms {res[sub].std():.4f}")
P("")
sys.exit(ck.done())
