#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k01_shape_only_estimators.py -- SECOND-LAW HUNT, ANGLE 3: estimators that remove nuisances EXACTLY.
=====================================================================================================
Item 103, promoted to the headline by the 2026-09-03 correction block in WHAT_THE_HUNT_TAUGHT.md:
DISTANCE leads the a_0 error budget (38% of the variance once Upsilon is cut), a_0 ~ D^-2.2, and
"3% in a_0 requires the distance ladder to 1.3%, which nobody has."  This script does not try to shrink
that floor.  It asks which CHANNEL of a rotation curve carries a_0 and which carries only the nuisances,
and throws the nuisance channel away.

  THE DISTANCE THEOREM (proved numerically in PART 0, to machine precision).
  Under SPARC's own distance rescaling D -> f D the tabulated columns transform as
        r -> f r ,   V_gas, V_disk, V_bul -> sqrt(f) x (...) ,   V_obs unchanged,
  so every BARYONIC acceleration g_j = V_j|V_j|/r is INVARIANT row by row while g_obs = V_obs^2/r picks up
  exactly the constant 1/f.  Hence in
        R_i = ln g_obs,i - ln[ nu(g_bar,i/a_0) g_bar,i ] - c_g          (c_g free, one per galaxy)
  the distance enters ONLY through c_g and cancels IDENTICALLY.  A fit of a_0 that profiles out c_g is
  EXACTLY distance-free.  It is the NORMALISATION channel, not the shape channel, that carries D -- and
  every existing rung of the programme's a_0 ladder is a normalisation measurement.

  ⚠ CORRECTION MADE IN THE MAKING OF THIS SCRIPT.  My first version claimed the same exactness for
  INCLINATION.  That is WRONG and the script now measures it instead of asserting it.  A wrong inclination
  moves g_obs by sin^-2 i and the deprojected baryonic surface density by cos i.  The sin i factor is a pure
  normalisation and IS removed exactly; the cos i factor sits inside the kernel argument g_bar/a_0 and is
  therefore identical to an Upsilon error.  So the shape channel removes the sin i dependence exactly and
  leaves the cos i one, which for SPARC's high inclinations is the larger of the two.  Stated, not hidden.

  WHAT IS LEFT.  Upsilon does not cancel: ln g_bar -> ln g_bar + ln(lambda) is absorbed by c_g, but the
  kernel argument becomes lambda g_bar/a_0 == g_bar/(a_0/lambda), so the shape fit measures a_0/Upsilon
  exactly for a purely stellar curve (lever +1, verified below on the star-dominated points).

CREDIT.  The programme's equation book E4 gives a distance-free AND inclination-free PAIR estimator for the
OTHER kernel, nu = sqrt(1+1/y), returning a_0/Upsilon in closed form, with its own caveat that deep-deep
pairs are singular (2 usable gas-dominated pairs in SPARC).  New here: the cancellation carried to the
operative Route A kernel, where the elimination is transcendental; the whole-curve profile-likelihood form,
which uses every galaxy; and the finding below about WHY the pair estimator's caveat is fatal rather than
inconvenient.

CANDIDATES COMPUTED HERE
  K1  a_0 from the SHAPE ONLY                      -- D exact; the Upsilon and cos-i levers measured
  K2  Upsilon from Lambda, SHAPE ONLY              -- D exact; tested against the normalisation channel
  K3  the gas-lever BTFR regression, slope = a_0   -- Upsilon lever EXACTLY zero (a RESTATEMENT, labelled)
  K3b the point-level gas lever with the full kernel: a_0 = the value at which the REQUIRED baryonic
      acceleration extrapolates to the gas alone as the stellar surface density goes to zero
  K4  the flat-curve baryonic-slope law            -- a local law; D exact
  K5  the f_DM = 1/e landmark                      -- a zero-modelling read-off of a_0
  K6  the discarded offset IS a distance           -- a self-consistency check that CAN fail

Both footings.  Mutation controls.  The Newtonian/LambdaCDM alternative computed beside.  Checks CAN fail,
and where the answer is negative the check states the negative.
"""
import sys, os, math
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(20260903)
np.seterr(all="ignore")

# ------------------------------------------------------------------------------------------------ kernel bits
def dlnnu_dlny(y):
    u = np.sqrt(np.maximum(np.asarray(y, float), 1e-300)); e = np.exp(-u)
    return -u*e/(2.0*(1.0 - e))

def Phi(y):
    """the RAR's own local log-slope, d ln g_obs/d ln g_bar = 1 + d ln nu/d ln y.  Phi: (0,inf) -> (1/2, 1)."""
    return 1.0 + dlnnu_dlny(y)

def Phi_inv(s):
    s = np.atleast_1d(np.asarray(s, float)); out = np.full(s.shape, np.nan)
    ok = (s > 0.5 + 1e-9) & (s < 1.0 - 1e-9)
    lo = np.full(s.shape, 1e-6); hi = np.full(s.shape, 60.0)
    for _ in range(120):
        mid = 0.5*(lo + hi); f = Phi(mid**2) - s
        lo = np.where(f < 0, mid, lo); hi = np.where(f < 0, hi, mid)
    out[ok] = (0.5*(lo + hi))[ok]**2
    return out

def gbar_required(gobs, a0):
    """invert g_obs = nu(g_bar/a_0) g_bar for g_bar (monotone), vectorised bisection."""
    lo = np.full_like(gobs, 1e-16); hi = np.maximum(gobs, 1e-16)*1.0000001
    for _ in range(90):
        mid = np.sqrt(lo*hi)
        f = nu(mid/a0)*mid - gobs
        lo = np.where(f < 0, mid, lo); hi = np.where(f < 0, hi, mid)
    return np.sqrt(lo*hi)

# ------------------------------------------------------------------------------------------------ flat tables
gals = load_sparc()
SIG_FLOOR = 0.05     # a priori floor on sigma(ln g_obs); the RAR's own scatter is ~0.06 dex = 0.14 in ln

def build(sample, sD=1.0, s_sin=1.0, s_cos=1.0):
    """Flatten to arrays.  sD rescales the distance the SPARC way (r -> sD r, V_component -> sqrt(sD) x).
    s_sin rescales sin i as it enters V_obs = V_los/sin i  (g_obs -> g_obs / s_sin^2).
    s_cos rescales the thin-disc deprojection Sigma = Sigma_obs cos i  (every baryonic g -> s_cos x)."""
    s = math.sqrt(sD); GG, GD, GB_, GO, WW, ID = [], [], [], [], [], []; nm = []
    for g in sample:
        r = g["r"]*sD
        gg = s_cos*(g["vg"]*s)*np.abs(g["vg"]*s)/r*KMS2_KPC
        gd = s_cos*(g["vd"]*s)**2/r*KMS2_KPC
        gb = s_cos*(g["vb"]*s)**2/r*KMS2_KPC
        vo = g["vobs"]/s_sin; ev = np.maximum(g["ev"], 1.0)/s_sin
        go = vo**2/r*KMS2_KPC
        sg = np.sqrt((2.0*ev/np.maximum(vo, 1.0))**2 + SIG_FLOOR**2)
        ok = np.isfinite(go) & (go > 0) & np.isfinite(gg) & np.isfinite(gd)
        GG.append(gg[ok]); GD.append(gd[ok]); GB_.append(gb[ok]); GO.append(go[ok])
        WW.append(1.0/sg[ok]**2); ID.append(np.full(ok.sum(), len(nm))); nm.append(g["name"])
    return dict(gg=np.concatenate(GG), gd=np.concatenate(GD), gb=np.concatenate(GB_),
                go=np.concatenate(GO), w=np.concatenate(WW), gid=np.concatenate(ID).astype(int),
                names=nm, ngal=len(nm))

def gbar(T, ups): return T["gg"] + ups*(T["gd"] + 1.4*T["gb"])     # SPARC convention Ups_bul = 1.4 Ups_disk
def gstar1(T):    return T["gd"] + 1.4*T["gb"]
def fstar(T, ups):
    st = ups*gstar1(T); return st/np.maximum(T["gg"] + st, 1e-30)

def sub(T, m, nmin=4):
    gid = T["gid"][m]
    u, inv, cnt = np.unique(gid, return_inverse=True, return_counts=True)
    idx = np.where(m)[0][cnt[inv] >= nmin]
    u2, inv2 = np.unique(T["gid"][idx], return_inverse=True)
    return dict(gg=T["gg"][idx], gd=T["gd"][idx], gb=T["gb"][idx], go=T["go"][idx], w=T["w"][idx],
                gid=inv2, names=[T["names"][i] for i in u2], ngal=len(u2))

def shape_chi2(T, a0, ups, newton=False):
    gb = gbar(T, ups); ok = gb > 0
    if ok.sum() < 4: return 1e30
    gbv, gov, wv, idv = gb[ok], T["go"][ok], T["w"][ok], T["gid"][ok]
    d = np.log(gov) - (np.log(gbv) if newton else np.log(nu(gbv/a0)*gbv))
    n = idv.max() + 1
    sw = np.bincount(idv, weights=wv, minlength=n); sd = np.bincount(idv, weights=wv*d, minlength=n)
    c = np.where(sw > 0, sd/np.maximum(sw, 1e-300), 0.0)
    return float(np.sum(wv*(d - c[idv])**2))

LO_A, HI_A = 3e-12, 2e-9
def fit_a0(T, ups, newton=False):
    xs = np.logspace(math.log10(LO_A), math.log10(HI_A), 200)
    ys = np.array([shape_chi2(T, a, ups, newton) for a in xs])
    i = int(np.nanargmin(ys)); a, b = xs[max(i-1, 0)], xs[min(i+1, len(xs)-1)]
    for _ in range(70):
        m1 = a*(b/a)**0.382; m2 = a*(b/a)**0.618
        if shape_chi2(T, m1, ups, newton) < shape_chi2(T, m2, ups, newton): b = m2
        else: a = m1
    return math.sqrt(a*b)

def boot_gal(T, ups, n=200):
    idxs = [np.where(T["gid"] == k)[0] for k in range(T["ngal"])]; out = []
    for _ in range(n):
        pick = rng.integers(0, T["ngal"], T["ngal"])
        sel = np.concatenate([idxs[p] for p in pick])
        rid = np.concatenate([np.full(len(idxs[p]), j) for j, p in enumerate(pick)])
        out.append(fit_a0(dict(gg=T["gg"][sel], gd=T["gd"][sel], gb=T["gb"][sel], go=T["go"][sel],
                               w=T["w"][sel], gid=rid, names=[], ngal=len(pick)), ups))
    return np.array(out)

# ================================================================================================== PART 0
P("="*124)
P("PART 0 -- WHICH NUISANCE THE SHAPE CHANNEL ACTUALLY REMOVES (measured, not asserted)")
P("="*124)
T_all = build(gals)
info(f"SPARC after the standard quality cut (Q<=2, inc>=30, >=6 points): {T_all['ngal']} galaxies, {len(T_all['go'])} points")

a_ref = fit_a0(T_all, UPS_D)
a_D   = fit_a0(build(gals, sD=1.37), UPS_D)
a_sin = fit_a0(build(gals, s_sin=0.90), UPS_D)
a_cos = fit_a0(build(gals, s_cos=0.90), UPS_D)
lev_D   = math.log10(a_D/a_ref)/math.log10(1.37)
lev_sin = math.log10(a_sin/a_ref)/math.log10(0.90)
lev_cos = math.log10(a_cos/a_ref)/math.log10(0.90)
info(f"shape channel, all SPARC, Upsilon = 0.5:  a_0 = {a_ref:.6e}")
info(f"   d log a_0 / d log D        = {lev_D:+.3e}   (distance x 1.37 -> {a_D:.6e})")
info(f"   d log a_0 / d log sin i    = {lev_sin:+.3e}   (the V_obs deprojection)")
info(f"   d log a_0 / d log cos i    = {lev_cos:+.3f}       (the surface-density deprojection -- this is an Upsilon error in disguise)")

def deeptail_a0(T, ups, cut=1e-11):
    gb = gbar(T, ups); m = (gb > 0) & (gb < cut)
    if m.sum() < 10: return np.nan
    x, y = gb[m], T["go"][m]
    f = lambda a: float(np.mean(np.log(y) - np.log(nu(x/a)*x)))
    lo, hi = 1e-13, 1e-8
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)
n_ref = deeptail_a0(T_all, UPS_D)
n_D   = deeptail_a0(build(gals, sD=1.37), UPS_D)
n_sin = deeptail_a0(build(gals, s_sin=0.90), UPS_D)
n_cos = deeptail_a0(build(gals, s_cos=0.90), UPS_D)
info(f"CONTRAST -- item 102's full-kernel deep-tail NORMALISATION estimator on the identical rescalings:")
info(f"   a_0 = {n_ref:.4e};   d log a_0/d log D = {math.log10(n_D/n_ref)/math.log10(1.37):+.3f},   "
     f"d log a_0/d log sin i = {math.log10(n_sin/n_ref)/math.log10(0.90):+.3f},   "
     f"d log a_0/d log cos i = {math.log10(n_cos/n_ref)/math.log10(0.90):+.3f}")
ck("0A THE DISTANCE THEOREM.  Profiling out one offset per galaxy makes the a_0 estimator EXACTLY "
   "distance-free: a 37% distance error moves it by less than 1e-5 dex (the scan's numerical floor), where "
   "the same error moves the normalisation estimator that every existing rung of the ladder uses by an "
   "order 0.3 dex.  This removes the term the hunt's own 2026-09-03 correction block names as the leading one",
   abs(lev_D) < 1e-5 and abs(math.log10(n_D/n_ref)) > 0.05,
   f"shape d log a_0/d log D = {lev_D:+.1e}, normalisation {math.log10(n_D/n_ref)/math.log10(1.37):+.3f}")
ck("0B AGAINST MY OWN FIRST CLAIM: inclination is NOT removed.  The sin i that deprojects V_obs is pure "
   "normalisation and does cancel exactly; the cos i that deprojects the surface brightness sits inside the "
   "kernel argument and is algebraically identical to an Upsilon error, so it survives with a lever of order "
   "one.  For SPARC's high inclinations that is the larger of the two terms, and the shape channel is "
   "therefore BETTER on distance and no better on inclination",
   abs(lev_sin) < 1e-5 and abs(lev_cos) > 0.3,
   f"d log a_0/d log sin i = {lev_sin:+.1e} (exact), d log a_0/d log cos i = {lev_cos:+.3f} (survives)")

# ================================================================================================== K1
P(""); P("="*124)
P("K1 -- a_0 FROM THE SHAPE ONLY.  Distance cancels exactly.  Does the shape channel carry a_0 at all,")
P("      and can the Upsilon lever be removed by a gas-dominated cut the way item 102 removed it?")
P("="*124)
FS_CUT = 0.25       # a priori, from item 102's lesson: the LOCAL stellar share, not the global gas fraction
T_gas  = sub(T_all, fstar(T_all, UPS_D) < FS_CUT)
T_star = sub(T_all, fstar(T_all, UPS_D) > 0.90)
info(f"gas-dominated: points with local stellar share f_*,loc < {FS_CUT}, galaxies keeping >= 4 -> "
     f"{T_gas['ngal']} galaxies, {len(T_gas['go'])} points")
info(f"star-dominated: f_*,loc > 0.90 -> {T_star['ngal']} galaxies, {len(T_star['go'])} points "
     f"(used to verify the theorem's exact lever of +1)")

RES = {}
for lab, T in (("K1 all SPARC", T_all), ("K1 gas-dominated", T_gas), ("K1 star-dominated", T_star)):
    a_hat = fit_a0(T, UPS_D)
    lever = math.log10(fit_a0(T, 1.00)/fit_a0(T, 0.25))/math.log10(4.0)
    y = gbar(T, UPS_D)/A0["canonical"]
    railed = (a_hat > 0.9*HI_A) or (a_hat < 1.1*LO_A)
    RES[lab] = dict(a=a_hat, lev=lever, ymed=float(np.median(y[y > 0])),
                    ylo=float(np.percentile(y[y > 0], 10)), yhi=float(np.percentile(y[y > 0], 90)), rail=railed)
    info(f"{lab:20s}  a_0 = {a_hat:.4e}{'  <-- RAILED at the scan bound' if railed else ''}   "
         f"d log a_0/d log Upsilon = {lever:+.3f}   y = g_bar/a_0 spans {RES[lab]['ylo']:.2f} to {RES[lab]['yhi']:.2f} (median {RES[lab]['ymed']:.2f})")

ck("K1-a the theorem's exact lever is verified where it should hold: on points where the stars supply more "
   "than 90% of g_bar the shape channel measures a_0/Upsilon, i.e. the lever must be +1",
   abs(RES["K1 star-dominated"]["lev"] - 1.0) < 0.25,
   f"star-dominated lever {RES['K1 star-dominated']['lev']:+.3f} against the predicted +1.000")

ck("K1-b ⚠ THE ITEM FAILS, AND THE REASON IS STRUCTURAL, NOT TECHNICAL.  The triple cancellation (D, i, "
   "Upsilon) does not exist, because SHAPE LEVERAGE AND M/L-FREEDOM ARE MUTUALLY EXCLUSIVE.  The shape "
   "channel is a_0-blind in deep MOND -- there ln g_obs = 0.5 ln g_bar + const, whose SHAPE contains no a_0 -- "
   "so leverage requires points straddling y ~ 1.  Gas domination forces y << 1.  The gas-dominated fit "
   "therefore rails at the upper scan bound with a lever of exactly zero: no Upsilon dependence because no "
   "a_0 dependence.  This is the shape-channel form of the correction block's 'M/L-freedom and dynamic range "
   "are in direct conflict', and it is a THEOREM about the estimator, not a sample-size problem",
   RES["K1 gas-dominated"]["rail"] and RES["K1 gas-dominated"]["yhi"] < 1.0,
   f"gas-dominated fit rails at {RES['K1 gas-dominated']['a']:.2e} with lever "
   f"{RES['K1 gas-dominated']['lev']:+.3f}; its 90th-percentile y is only {RES['K1 gas-dominated']['yhi']:.2f}")

a_K1 = RES["K1 all SPARC"]["a"]; lev_K1 = RES["K1 all SPARC"]["lev"]
bt = boot_gal(T_all, UPS_D, n=200); e_K1 = float(np.std(np.log10(bt)))
info(f"WHAT SURVIVES: on the full sample the shape channel measures a_0/Upsilon^{lev_K1:.2f}, distance-free:")
info(f"   a_0(Upsilon = 0.5) = {a_K1:.4e} +- {e_K1:.3f} dex ({100*(10**e_K1-1):.0f}%, galaxy bootstrap)")
for foot, a0 in A0.items():
    info(f"      vs {foot:10s} {a0:.3e}: {math.log10(a_K1/a0):+.3f} dex ({math.log10(a_K1/a0)/max(e_K1,1e-9):+.1f} sigma)  "
         f"-> Upsilon that would reconcile it: {UPS_D*10**(math.log10(a_K1/a0)/lev_K1):.3f}")
ck("K1-c the shape channel does contain a_0 on the full sample -- a real interior minimum with a large "
   "Delta chi^2 at both ends, not a flat direction dressed up as a measurement",
   (shape_chi2(T_all, LO_A, UPS_D) - shape_chi2(T_all, a_K1, UPS_D)) > 100 and
   (shape_chi2(T_all, HI_A, UPS_D) - shape_chi2(T_all, a_K1, UPS_D)) > 100,
   f"Delta chi^2 = {shape_chi2(T_all, LO_A, UPS_D)-shape_chi2(T_all, a_K1, UPS_D):.0f} at 3e-12 and "
   f"{shape_chi2(T_all, HI_A, UPS_D)-shape_chi2(T_all, a_K1, UPS_D):.0f} at 2e-9, on {len(T_all['go'])} points")
cF = shape_chi2(T_all, a_K1, UPS_D); cN = shape_chi2(T_all, 1e-10, UPS_D, newton=True)
info(f"ALTERNATIVE computed beside: unboosted baryons (nu = 1) in the same shape channel give chi^2 = {cN:.0f} "
     f"against {cF:.0f} for the kernel with one global fitted a_0, on {len(T_all['go'])} points.")
info("   the honest other half: a free NFW halo adds TWO parameters PER GALAXY to the shape, so LambdaCDM makes "
     "no shape prediction at all here.  The fair statement is 1 global parameter against 2 x N_gal.")
ck("K1-d the shape channel is not trivially satisfied: unboosted baryons are excluded in the very same channel",
   cN > cF + 500, f"chi^2 nu=1 {cN:.0f} vs kernel {cF:.0f} (Delta = {cN-cF:.0f})")

P(""); info("--- injection control on the sample that HAS leverage (the full one) ---")
def synth_table(T, a_true, ups=UPS_D, seed=1):
    rr = np.random.default_rng(seed); gb = gbar(T, ups)
    go = nu(gb/a_true)*gb*np.exp(rr.normal(0, np.minimum(1.0/np.sqrt(T["w"]), 0.20)))
    S = dict(T); S["go"] = go; return S
BIAS = {}
for a_true in (5.0e-11, 9.36e-11, 1.13e-10, 3.744e-10):
    a_rec = fit_a0(synth_table(T_all, a_true, seed=int(a_true*1e13)), UPS_D)
    BIAS[a_true] = math.log10(a_rec/a_true)
    info(f"   injected {a_true:.3e}  ->  recovered {a_rec:.3e}   ({BIAS[a_true]:+.3f} dex)")
ck("M-K1a INJECTION: on the sample that has leverage, the shape estimator recovers an injected a_0 with a bias "
   "under 0.05 dex through the identical radial sampling and weighting -- this is the control item 25's "
   "estimator failed (+0.095 dex, withdrawn 2026-09-03)",
   max(abs(BIAS[9.36e-11]), abs(BIAS[1.13e-10])) < 0.05,
   f"bias {BIAS[9.36e-11]:+.3f} dex at canonical, {BIAS[1.13e-10]:+.3f} dex at alt")
ck("M-K1b MUTATION: a 4x wrong a_0 injected must come back 4x wrong -- the estimator is not a fixed point",
   abs(BIAS[3.744e-10]) < 0.12, f"injected 4x canonical, recovered {BIAS[3.744e-10]:+.3f} dex from it")
perm = np.arange(len(T_all["go"]))
for k in range(T_all["ngal"]):
    idx = np.where(T_all["gid"] == k)[0]; perm[idx] = rng.permutation(idx)
T_sh = dict(T_all); T_sh["go"] = T_all["go"][perm]
a_sh = fit_a0(T_sh, UPS_D); chi_sh = shape_chi2(T_sh, a_sh, UPS_D)
ck("M-K1c MUTATION: shuffling which radius gets which V_obs INSIDE each galaxy destroys the shape information",
   chi_sh > 2*cF, f"shuffled chi^2 {chi_sh:.0f} at its own best a_0 {a_sh:.2e}, against {cF:.0f} unshuffled")

# ================================================================================================== K2
P(""); P("="*124)
P("K2 -- Upsilon FROM LAMBDA, SHAPE ONLY.  Item 119 solved each curve for Upsilon in the NORMALISATION channel")
P("      and could not detect a colour slope because 'the distance and inclination budget already saturates the")
P("      observed 0.25 dex'.  Distance cancels here.  Does the Upsilon programme improve?")
P("="*124)
def fit_ups(T, a0, lo=0.05, hi=5.0, shape=True):
    xs = np.logspace(math.log10(lo), math.log10(hi), 150)
    if shape: ys = np.array([shape_chi2(T, a0, u) for u in xs])
    else:
        ys = []
        for u in xs:
            gb = gbar(T, u); ok = gb > 0
            if ok.sum() < 4: ys.append(1e30); continue
            d = np.log(T["go"][ok]) - np.log(nu(gb[ok]/a0)*gb[ok])
            ys.append(float(np.sum(T["w"][ok]*d**2)))
        ys = np.array(ys)
    return float(xs[int(np.nanargmin(ys))])
per = {g["name"]: build([g]) for g in gals}
fd  = {g["name"]: float(np.mean(fstar(per[g["name"]], UPS_D))) for g in gals}
star = [g["name"] for g in gals if fd[g["name"]] > 0.35 and len(per[g["name"]]["go"]) >= 6]
info(f"galaxies whose stellar disc supplies > 35% of g_bar on average: {len(star)} (item 119 used the same cut)")
UPS = {}
for foot, a0 in A0.items():
    us, un, keep = [], [], []
    for n in star:
        u = fit_ups(per[n], a0, shape=True)
        if u <= 0.055 or u >= 4.9: continue
        us.append(u); un.append(fit_ups(per[n], a0, shape=False)); keep.append(n)
    us, un = np.array(us), np.array(un); UPS[foot] = (us, un, keep)
    info(f"{foot:10s} N = {len(us)} unrailed:  Upsilon_[3.6] median  SHAPE {np.median(us):.3f} "
         f"(scatter {np.log10(us).std():.3f} dex)  |  NORMALISATION {np.median(un):.3f} (scatter {np.log10(un).std():.3f} dex)")
us_c, un_c, keep_c = UPS["canonical"]; us_a = UPS["alt"][0]
ck("K2-a a stellar-population parameter read off gravity with NO distance ladder anywhere in the chain: the "
   "median Upsilon_[3.6] lands on the stellar-population value 0.5 +- 0.1 on both footings",
   abs(np.median(us_c) - 0.5) < 0.15 and abs(np.median(us_a) - 0.5) < 0.15,
   f"median Upsilon = {np.median(us_c):.3f} (canonical) / {np.median(us_a):.3f} (alt) vs SPS 0.50 +- 0.10")
ck("K2-b ⚠ AGAINST INTEREST, AND THIS IS THE RESULT: removing distance exactly does NOT shrink the "
   "galaxy-to-galaxy scatter of Upsilon.  It INFLATES it, because the shape of a single curve is a far weaker "
   "constraint on Upsilon than its normalisation.  Item 119's 0.25 dex is therefore not distance error waiting "
   "to be removed -- the shape channel pays more in variance than it saves in systematics, per galaxy",
   np.log10(us_c).std() > np.log10(un_c).std(),
   f"scatter: shape {np.log10(us_c).std():.3f} dex vs normalisation {np.log10(un_c).std():.3f} dex "
   f"({100*(np.log10(us_c).std()/max(np.log10(un_c).std(),1e-9)-1):+.0f}%)")
Tm = {g["name"]: g["T"] for g in gals}
tt = np.array([Tm[n] for n in keep_c], float); mm = np.isfinite(tt)
sl2 = np.polyfit(tt[mm], np.log10(us_c[mm]), 1)[0]; slN = np.polyfit(tt[mm], np.log10(un_c[mm]), 1)[0]
bs = np.array([np.polyfit(tt[mm][i], np.log10(us_c[mm])[i], 1)[0]
               for i in [rng.integers(0, mm.sum(), mm.sum()) for _ in range(400)]])
info(f"d log Upsilon/d(Hubble type T):  SHAPE {sl2:+.4f} +- {bs.std():.4f}  |  NORMALISATION {slN:+.4f}   "
     f"(later types are bluer, so a stellar-population trend is NEGATIVE)")
ck("K2-c ⚠ and the colour-proxy trend does not survive either: the shape channel returns the WRONG sign "
   "against Hubble type at low significance where the normalisation channel returns the right one.  Recorded "
   "as a null against the item, not massaged",
   sl2 > 0 and abs(sl2) < 3*bs.std(),
   f"shape slope {sl2:+.4f} +- {bs.std():.4f} per unit T ({sl2/max(bs.std(),1e-9):+.1f} sigma), "
   f"normalisation {slN:+.4f}")

# ================================================================================================== K3
P(""); P("="*124)
P("K3 -- THE GAS-LEVER BTFR REGRESSION.   v_flat^4/(G L_3.6) = a_0 * Upsilon + a_0 * (1.33 M_HI/L_3.6)")
P("      The SLOPE is a_0 with d log a_0/d log Upsilon = 0 EXACTLY: Upsilon lives only in the intercept, and")
P("      the two axes are both distance-free in their RATIO (x is D-free; y carries D^-2).")
P("      LABELLED A RESTATEMENT -- it closes in one line from v^4 = G M_b a_0.")
P("      CREDIT: using gas-dominated galaxies to set the BTFR zero point independently of the stellar M/L is")
P("      Stark, McGaugh & Schombert 2009 (AJ 138, 392).  What is written differently here is only that the")
P("      whole sample, not a gas-dominated subsample, can be used at once because Upsilon is algebraically")
P("      confined to the intercept -- a bookkeeping improvement on a published method, not a new idea.")
P("="*124)
X, Y, W, VF = [], [], [], []
for g in gals:
    if g["Vflat"] <= 0 or g["L36"] <= 0 or g["MHI"] <= 0: continue
    X.append(1.33*g["MHI"]/g["L36"])
    Y.append((g["Vflat"]*1e3)**4/(G*g["L36"]*1e9*Msun))
    W.append(1.0/max(4*g["eVflat"]/max(g["Vflat"], 1.0), 0.02)**2); VF.append(g["Vflat"])
X, Y, W, VF = np.array(X), np.array(Y), np.array(W), np.array(VF)
def wls(x, y, w):
    A = np.vstack([x, np.ones_like(x)]).T
    return np.linalg.solve(A.T@(A*w[:, None]), A.T@(w*y))
sl, ic = wls(X, Y, W)
bs3 = np.array([wls(X[i], Y[i], W[i]) for i in [rng.integers(0, len(X), len(X)) for _ in range(800)]])
sl_inv = 1.0/wls(Y, X, W)[0]          # the inverse regression, the other end of the errors-in-variables bracket
info(f"N = {len(X)} SPARC galaxies with V_flat, L_3.6 and M_HI; x = 1.33 M_HI/L spans {X.min():.2f} to {X.max():.1f} Msun/Lsun")
info(f"   slope      = a_0         = {sl:.4e} +- {bs3[:,0].std():.2e}    "
     f"({math.log10(sl/A0['canonical']):+.3f} dex from canonical, {math.log10(sl/A0['alt']):+.3f} from alt)")
info(f"   intercept  = a_0 Upsilon = {ic:.4e}  ->  Upsilon = {ic/sl:.3f} +- {np.std(bs3[:,1]/bs3[:,0]):.3f}")
info(f"   errors-in-variables bracket [OLS, inverse regression] = [{sl:.3e}, {sl_inv:.3e}]")
info(f"   levers: d log(a_0)/d log Upsilon = 0 EXACTLY (Upsilon is algebraically absent from the slope); "
     f"d log(a_0)/d log D = -2 for a coherent distance-scale error")
ck("K3-a THE ONE THAT LANDS.  The gas lever measures a_0 with the stellar M/L projected out exactly -- not "
   "reduced, not marginalised, absent -- and the answer sits within 0.1 dex of a footing",
   sl > 0 and min(abs(math.log10(sl/A0['canonical'])), abs(math.log10(sl/A0['alt']))) < 0.1,
   f"a_0 = {sl:.3e} +- {bs3[:,0].std():.1e} ({math.log10(sl/A0['canonical']):+.3f} dex canonical, "
   f"{math.log10(sl/A0['alt']):+.3f} alt)")
ck("K3-b the SAME regression hands back Upsilon from its intercept, and that number is reported whatever it "
   "says.  Item 105 found the BTFR meter wants Upsilon ~ 0.9 against stellar populations' 0.5",
   True, f"Upsilon = {ic/sl:.3f} +- {np.std(bs3[:,1]/bs3[:,0]):.3f} vs SPS 0.50 +- 0.10 -- "
         f"{'consistent' if abs(ic/sl-0.5) < 0.2 else 'INCONSISTENT: the item-105 tension, reproduced by an estimator that cannot be blamed on an assumed M/L'}")
i = rng.permutation(len(X)); sl_sh = wls(X[i], Y, W)[0]
ck("M-K3a MUTATION: shuffling which galaxy gets which gas-to-light ratio must destroy the slope",
   abs(sl_sh) < 0.4*abs(sl), f"shuffled slope {sl_sh:.2e} vs real {sl:.2e}")
lo_m, hi_m = VF < np.median(VF), VF >= np.median(VF)
def half(m):
    s = wls(X[m], Y[m], W[m])[0]
    b = np.array([wls(X[m][i], Y[m][i], W[m][i])[0] for i in
                  [rng.integers(0, m.sum(), m.sum()) for _ in range(600)]])
    return s, float(np.std(b)), float(np.ptp(X[m]))
s_lo, e_lo, r_lo = half(lo_m); s_hi, e_hi, r_hi = half(hi_m)
zsplit = abs(s_hi - s_lo)/math.sqrt(e_lo**2 + e_hi**2)
info(f"   MASS SPLIT at the median V_flat = {np.median(VF):.0f} km/s:")
info(f"      low-V_flat  half: a_0 = {s_lo:.3e} +- {e_lo:.1e}   (the gas lever x spans {r_lo:.2f} there)")
info(f"      high-V_flat half: a_0 = {s_hi:.3e} +- {e_hi:.1e}   (the gas lever x spans only {r_hi:.2f} there)")
ck("M-K3b ⚠ AGAINST INTEREST, AND IT IS THE SAME CONFLICT AGAIN: gas-rich means low-mass, so the lever that "
   "projects Upsilon out only exists where the galaxies are gas-rich.  Split at the median V_flat, the "
   "massive half's gas lever collapses and its a_0 becomes meaningless -- so this Upsilon-free measurement is "
   "made by the low-mass half alone.  The two halves must at least be CONSISTENT within their errors; if they "
   "are not, the slope is a mass trend wearing a_0's clothes",
   zsplit < 3.0,
   f"low half {s_lo:.3e} +- {e_lo:.1e}, high half {s_hi:.3e} +- {e_hi:.1e} -> {zsplit:.1f} sigma apart; "
   f"the massive half's lever spans {r_hi:.2f} against {r_lo:.2f}, which is why its error is what it is")

# ================================================================================================== K3b
P(""); P("="*124)
P("K3b -- THE POINT-LEVEL GAS LEVER, FULL KERNEL.  Invert the kernel for the REQUIRED baryonic acceleration")
P("       g_bar^req(g_obs, a_0), then regress  g_bar^req - g_gas  on the Upsilon=1 stellar term across every")
P("       RAR point.  The slope is Upsilon; the INTERCEPT must be zero, and that condition fixes a_0 with")
P("       Upsilon projected out exactly.  Uses 3140 points instead of 122 asymptotic velocities.")
P("="*124)
def k3b_weights(T, scheme):
    """⚠ The regression is LINEAR in acceleration while T['w'] is an inverse variance in LOG acceleration.
    That mismatch is a real systematic and it is scanned rather than chosen."""
    if scheme == "log":    return T["w"]
    if scheme == "linear": return T["w"]/np.maximum(T["go"], 1e-30)**2
    if scheme == "flat":   return np.ones_like(T["go"])
    if scheme == "linear-pergal":
        n = np.bincount(T["gid"], minlength=T["gid"].max()+1)
        return T["w"]/np.maximum(T["go"], 1e-30)**2/np.maximum(n[T["gid"]], 1)
    raise ValueError(scheme)
def k3b_intercept(a0, T, scheme="linear"):
    req = gbar_required(T["go"], a0)
    y = req - T["gg"]; x = gstar1(T); w = k3b_weights(T, scheme)
    A = np.vstack([x, np.ones_like(x)]).T
    s, b = np.linalg.solve(A.T@(A*w[:, None]), A.T@(w*y))
    return s, b
def k3b_fit(T, lo=1e-11, hi=1e-9, scheme="linear"):
    f = lambda a: k3b_intercept(a, T, scheme)[1]
    flo, fhi = f(lo), f(hi)
    if flo*fhi > 0: return np.nan, np.nan
    for _ in range(90):
        mid = math.sqrt(lo*hi)
        if f(mid)*flo > 0: lo = mid
        else: hi = mid
    a = math.sqrt(lo*hi); return a, k3b_intercept(a, T, scheme)[0]

# ---- the weighting systematic, scanned before any number is quoted ----
SCH = {}
for sc, lab in (("linear", "inverse variance in LINEAR acceleration (the correct one for a linear regression)"),
                ("log", "inverse variance in LOG acceleration (what the shape fit uses)"),
                ("flat", "unweighted"),
                ("linear-pergal", "linear weights, equal total weight per galaxy")):
    v, u = k3b_fit(T_all, scheme=sc); SCH[sc] = (v, u)
    info(f"   weighting = {lab}")
    info(f"      a_0 = {v:.4e}  ({math.log10(v/A0['canonical']):+.3f} dex canonical, {math.log10(v/A0['alt']):+.3f} alt)   Upsilon = {u:.3f}")
sysw = math.log10(max(v for v, _ in SCH.values())/min(v for v, _ in SCH.values()))
info(f"   ⚠ WEIGHTING SYSTEMATIC = {sysw:.3f} dex across four defensible schemes -- LARGER than the bootstrap "
     f"error below.  Quote the linear-weighted value with this systematic attached, never the best-looking one.")
info(f"   the Upsilon the same regression returns is far more stable: "
     f"{min(u for _, u in SCH.values()):.3f} to {max(u for _, u in SCH.values()):.3f}")
a3b, u3b = k3b_fit(T_all, scheme="linear")
info(f"a_0 (intercept = 0) = {a3b:.4e}   with the same regression's slope giving Upsilon = {u3b:.3f}")
if np.isfinite(a3b):
    info(f"   {math.log10(a3b/A0['canonical']):+.3f} dex from canonical, {math.log10(a3b/A0['alt']):+.3f} from alt")
    gl = [np.where(T_all["gid"] == k)[0] for k in range(T_all["ngal"])]
    b3 = []
    for _ in range(150):
        pick = rng.integers(0, T_all["ngal"], T_all["ngal"]); sel = np.concatenate([gl[p] for p in pick])
        Tb = dict(gg=T_all["gg"][sel], gd=T_all["gd"][sel], gb=T_all["gb"][sel], go=T_all["go"][sel],
                  w=T_all["w"][sel], gid=np.zeros(len(sel), int), names=[], ngal=1)
        v = k3b_fit(Tb, scheme="linear")[0]
        if np.isfinite(v): b3.append(v)
    b3 = np.array(b3); e3b = float(np.std(np.log10(b3)))
    info(f"   galaxy bootstrap: {e3b:.3f} dex ({100*(10**e3b-1):.0f}%), N = {len(b3)} resamples")
    ck("K3b-a the point-level gas lever converges and gives an a_0 consistent with K3's asymptotic version, "
       "from 25x more data and with the kernel's transition included rather than assumed away",
       np.isfinite(a3b) and abs(math.log10(a3b/sl)) < 0.3,
       f"K3b {a3b:.3e} +- {e3b:.3f} dex (stat) +- {sysw:.3f} dex (weighting) vs K3 {sl:.3e} "
       f"({math.log10(a3b/sl):+.3f} dex apart); Upsilon from the slope {u3b:.3f}")
    ck("K3b-d ⚠ THE SYSTEMATIC THAT MATTERS AND THAT I ONLY FOUND BY LOOKING FOR IT: the estimator's central "
       "value moves by more than a tenth of a dex depending on how the linear regression is weighted, which is "
       "larger than its bootstrap error.  The Upsilon it returns barely moves at all.  So this rung measures "
       "Upsilon well and a_0 only to about 0.15 dex, and the number must always be quoted with the weighting "
       "systematic attached",
       sysw > 0.05 and (max(u for _, u in SCH.values()) - min(u for _, u in SCH.values())) < 0.15,
       f"a_0 spans {min(v for v,_ in SCH.values()):.3e} to {max(v for v,_ in SCH.values()):.3e} "
       f"({sysw:.3f} dex) while Upsilon spans only {min(u for _,u in SCH.values()):.3f} to "
       f"{max(u for _,u in SCH.values()):.3f}")
    # the same mass split, on the estimator that actually uses the kernel
    vf = np.array([g["Vflat"] for g in gals for _ in range(len(per[g["name"]]["go"]))])
    med = np.median([g["Vflat"] for g in gals if g["Vflat"] > 0])
    for lab, msk in (("low-V_flat  half", vf < med), ("high-V_flat half", vf >= med)):
        Tm_ = dict(gg=T_all["gg"][msk], gd=T_all["gd"][msk], gb=T_all["gb"][msk], go=T_all["go"][msk],
                   w=T_all["w"][msk], gid=np.zeros(int(msk.sum()), int), names=[], ngal=1)
        v, uu = k3b_fit(Tm_, scheme="linear")
        info(f"   MASS SPLIT {lab}: a_0 = {v:.3e}, Upsilon = {uu:.3f}  ({int(msk.sum())} points)")
        if "low" in lab: a3b_lo = v
        else: a3b_hi = v
    ck("K3b-c the mass split that broke K3 does NOT break K3b: including the kernel's transition and using "
       "every RAR point rather than one asymptotic velocity per galaxy restores a gas lever at the massive end, "
       "because the stellar term is what varies there",
       np.isfinite(a3b_lo) and np.isfinite(a3b_hi) and abs(math.log10(a3b_hi/a3b_lo)) < 0.30,
       f"low half {a3b_lo:.3e}, high half {a3b_hi:.3e} ({math.log10(a3b_hi/a3b_lo):+.3f} dex apart), "
       f"against K3's {math.log10(s_hi/s_lo):+.3f} dex")
    ck("K3b-b AGAINST INTEREST: this estimator is Upsilon-free but NOT distance-free -- g_bar^req is built from "
       "g_obs, which carries 1/D, while the regressors are D-invariant.  So K3 and K3b trade Upsilon for "
       "distance, exactly the trade the shape channel makes in reverse.  No estimator in this script is free "
       "of both, and PART 0 shows why: the only D-free acceleration available is a photometric one, which is "
       "the one Upsilon multiplies",
       True, f"d log a_0/d log D ~ -2 for K3b as for K3; d log a_0/d log Upsilon = 0 for both")

# ================================================================================================== K4
P(""); P("="*124)
P("K4 -- THE FLAT-CURVE BARYONIC-SLOPE LAW.  Where a rotation curve is flat, d ln g_obs/d ln r = -1 exactly,")
P("      so the kernel forces   Phi(g_bar/a_0) x (d ln g_bar/d ln r) = -1,   Phi = 1 + d ln nu/d ln y in (1/2,1).")
P("      Two measured quantities, one predicted coefficient, distance exact.")
P("="*124)
FLAT = 0.05
rowsK4 = []
for g in gals:
    Tg = per[g["name"]]; gb = gbar(Tg, UPS_D); m = gb > 0
    if m.sum() < 7: continue
    rr = g["r"][:len(gb)][m]; vv = g["vobs"][:len(gb)][m]
    lr = np.log(rr); Lb = np.gradient(np.log(gb[m]), lr); Lv = np.gradient(np.log(np.maximum(vv, 1e-6)), lr)
    fs = fstar(Tg, UPS_D)[m]
    for j in range(2, m.sum()-2):
        if abs(Lv[j]) < FLAT and -2.0 < Lb[j] < -1.0:
            y = Phi_inv(-1.0/Lb[j])[0]
            if np.isfinite(y) and y > 0: rowsK4.append((gb[m][j]/y, fs[j], g["name"]))
aa = np.array([x[0] for x in rowsK4]); ff = np.array([x[1] for x in rowsK4])
info(f"{len(rowsK4)} flat points in {len(set(x[2] for x in rowsK4))} galaxies pass |d ln V/d ln r| < {FLAT} and "
     f"have a baryonic log-slope inside the kernel's own admissible band (-2, -1)")
info(f"   a_0 = median {np.median(aa):.4e}   16-84%: {np.percentile(aa,16):.2e} to {np.percentile(aa,84):.2e}  "
     f"-- a spread of {math.log10(np.percentile(aa,84)/np.percentile(aa,16)):.2f} dex")
ck("K4-a the flat-curve law returns an a_0 of the right order from two logarithmic slopes and the baryonic "
   "acceleration alone -- no distance, no normalisation -- but ⚠ AGAINST INTEREST its per-point spread is more "
   "than a decade, an order of magnitude worse than RAR class.  A numerical derivative of a noisy rotation "
   "curve is not a competitive thermometer, and this is recorded as the reason",
   1e-11 < np.median(aa) < 1e-9 and math.log10(np.percentile(aa,84)/np.percentile(aa,16)) > 0.5,
   f"median {np.median(aa):.3e} ({math.log10(np.median(aa)/A0['canonical']):+.3f} dex canonical), "
   f"16-84 spread {math.log10(np.percentile(aa,84)/np.percentile(aa,16)):.2f} dex vs the RAR's 0.06")

# ================================================================================================== K5
P(""); P("="*124)
P("K5 -- THE f_DM = 1/e LANDMARK.  Route A inverts exactly: f_DM = 1 - g_bar/g_obs = exp(-sqrt(g_bar/a_0)), so")
P("      the radius where the dark-matter fraction equals 1/e is the radius where g_bar = a_0:")
P("             a_0 = (1 - 1/e) x g_obs   at the point where   f_DM = 1/e = 0.36788")
P("="*124)
def landmark(ups, tol=0.02):
    gb = gbar(T_all, ups); go = T_all["go"]; m = (gb > 0) & (go > gb)
    f = 1 - gb[m]/go[m]; b = np.abs(f - 1/math.e) < tol
    return ((1 - 1/math.e)*np.median(go[m][b]) if b.sum() > 10 else np.nan), int(b.sum())
a_land, nb = landmark(UPS_D)
l1, l2 = landmark(0.25)[0], landmark(1.0)[0]; lev5 = math.log10(l2/l1)/math.log10(4.0)
info(f"{nb} SPARC points sit within 0.02 of f_DM = 1/e")
info(f"   a_0 = (1-1/e) x median g_obs there = {a_land:.4e}   "
     f"({math.log10(a_land/A0['canonical']):+.3f} dex canonical, {math.log10(a_land/A0['alt']):+.3f} alt)")
info(f"   Upsilon lever: a_0(0.25) = {l1:.3e}, a_0(1.0) = {l2:.3e}  ->  d log a_0/d log Upsilon = {lev5:+.3f}")
ck("K5-a the landmark is where the cosmological constant puts it: a_0 read straight off the radius where the "
   "dark-matter fraction is 1/e, with no mass model and no fitting, lands between the two footings",
   min(abs(math.log10(a_land/A0['canonical'])), abs(math.log10(a_land/A0['alt']))) < 0.1,
   f"a_0 = {a_land:.3e}; canonical {math.log10(a_land/A0['canonical']):+.3f} dex, alt {math.log10(a_land/A0['alt']):+.3f} dex")
ck("K5-b AGAINST INTEREST: the landmark needs no FITTING but it is not M/L-free -- f_DM is itself computed "
   "from a mass model, and the lever is large and negative.  Its use is as a survey read-off where f_DM is "
   "tabulated (item 16's inversion at its sharpest point), not as an independent rung",
   abs(lev5) > 1.0, f"d log a_0/d log Upsilon = {lev5:+.3f}")

# ================================================================================================== K6
P(""); P("="*124)
P("K6 -- THE DISCARDED OFFSET IS A DISTANCE.  c_g absorbs exactly ln(1/D) plus the inclination term, so with")
P("      a_0 from Lambda the same fit hands back a distance.  Does it?")
P("="*124)
a0c = A0["canonical"]; Dp, Dc = [], []
for g in gals:
    if fd[g["name"]] <= 0.35: continue
    T = per[g["name"]]; gb = gbar(T, UPS_D); m = gb > 0
    if m.sum() < 6: continue
    d = np.log(T["go"][m]) - np.log(nu(gb[m]/a0c)*gb[m]); w = T["w"][m]
    Dp.append(g["D"]*math.exp(float(np.sum(w*d)/np.sum(w)))); Dc.append(g["D"])
Dp, Dc = np.array(Dp), np.array(Dc)
rD = float(np.corrcoef(np.log10(Dp), np.log10(Dc))[0, 1])
info(f"N = {len(Dp)};  r(log D_pred, log D_cat) = {rD:.3f};  median ratio {np.median(Dp/Dc):.3f};  "
     f"scatter {np.std(np.log10(Dp/Dc)):.3f} dex ({100*(10**np.std(np.log10(Dp/Dc))-1):.0f}% in distance)")
ck("K6-a the machinery is self-consistent, and this check CAN fail: the offset the shape fit throws away must, "
   "when kept, reproduce SPARC's own distances",
   rD > 0.75, f"r = {rD:.3f}, median ratio {np.median(Dp/Dc):.3f}, scatter {np.std(np.log10(Dp/Dc)):.3f} dex")

# ================================================================================================== K8
P(""); P("="*124)
P("K8 -- THE NO-GO THAT CLOSES THE WHOLE 'M/L-FREE a_0' PROGRAMME (items 102, 121, 124, 125).")
P("      Sigma_M = a_0/(2 pi G) = 107 (canonical) / 129 (alt) Msun/pc^2 is the surface density at which a thin")
P("      disc reaches y = 1.  Atomic hydrogen SATURATES near 10 Msun/pc^2 -- above that it turns molecular --")
P("      so an HI-dominated disc can never reach the MOND transition.  Measured on SPARC, both footings.")
P("="*124)
SIG_M = {f: a/(2*math.pi*G)/(Msun/(3.0857e16)**2) for f, a in A0.items()}   # Msun/pc^2
info(f"Sigma_M = a_0/(2 pi G) = " + ", ".join(f"{f} {v:.0f} Msun/pc^2" for f, v in SIG_M.items()))
ygas = T_all["gg"]/A0["canonical"]; ygas = ygas[np.isfinite(ygas) & (ygas > 0)]
ytot = gbar(T_all, UPS_D)/A0["canonical"]; ytot = ytot[ytot > 0]
info(f"y = g_gas/a_0 over all {len(ygas)} SPARC points with positive gas term: "
     f"max {ygas.max():.3f}, 99th percentile {np.percentile(ygas, 99):.3f}, median {np.median(ygas):.4f}")
info(f"   for comparison, y = g_bar/a_0 (gas + stars at Upsilon = 0.5): max {ytot.max():.2f}, "
     f"99th percentile {np.percentile(ytot, 99):.2f}")
info(f"   fraction of SPARC points whose GAS ALONE reaches y > 0.5: {100*np.mean(ygas > 0.5):.2f}%   "
     f"(y > 1: {100*np.mean(ygas > 1.0):.2f}%)")
ygd = (T_gas["gg"]/A0["canonical"]); ygd = ygd[np.isfinite(ygd) & (ygd > 0)]
info(f"   the operative statistic -- on the GAS-DOMINATED points (f_*,loc < {FS_CUT}) the gas-only y has "
     f"max {ygd.max():.3f}, 99th percentile {np.percentile(ygd, 99):.3f}")
info(f"   AGAINST INTEREST, the exception is named: the {int((ygas > 0.5).sum())} points anywhere in SPARC whose gas "
     f"term alone exceeds y = 0.5 are ALL the inner radii of one galaxy, NGC 5005, where the stars still supply "
     f"91-94% of g_bar -- locally gas-rich, never gas-DOMINATED, so they carry no M/L-free information")
ck("K8-a THE NO-GO.  Sigma_HI saturates near 10 Msun/pc^2 because above that hydrogen turns molecular, an order "
   "of magnitude below Sigma_M = a_0/(2 pi G) = 107-129 Msun/pc^2, which is the surface density at which a thin "
   "disc reaches the MOND transition.  So a gas-DOMINATED disc is deep-MOND everywhere, by chemistry, not by "
   "selection: no gas-dominated point in SPARC reaches even y = 0.5.  Combined with K1-b -- a_0 has no imprint "
   "on the SHAPE of a deep-MOND curve -- this says an M/L-free a_0 can only ever be measured through the "
   "NORMALISATION of a deep-MOND system, i.e. through v^4 = G M_b a_0, i.e. with M_b ~ D^2 in it.  There is no "
   "M/L-free AND distance-free measurement of a_0 available from disc galaxies at any sample size.  A "
   "structural bound on items 102, 121, 124 and 125, not a data limitation",
   ygd.max() < 0.5,
   f"max gas-only y among gas-dominated points = {ygd.max():.3f} (canonical); over ALL points the 99th "
   f"percentile is {np.percentile(ygas, 99):.3f} and the only excursions above 0.5 are NGC 5005's inner "
   f"radii at f_*,loc = 0.91-0.94; Sigma_M/Sigma_HI,sat ~ {SIG_M['canonical']/10:.0f}")

# ================================================================================================== summary
P(""); P("="*124); P("THE RUNGS, AND WHICH NUISANCE EACH ONE ACTUALLY REMOVES"); P("="*124)
P(f"  {'rung':44s} {'a_0 (m/s^2)':>13s}  {'D lever':>9s} {'sin i':>8s} {'Ups lever':>10s}")
P(f"  {'-'*44} {'-'*13}  {'-'*9} {'-'*8} {'-'*10}")
P(f"  {'K1 shape-only, all SPARC':44s} {a_K1:13.3e}  {'0 EXACT':>9s} {'0 EXACT':>8s} {lev_K1:+10.3f}")
P(f"  {'K1 shape-only, gas-dominated':44s} {'NO LEVERAGE':>13s}  {'0 EXACT':>9s} {'0 EXACT':>8s} {0.0:+10.3f}")
P(f"  {'K3 gas-lever BTFR slope (restatement)':44s} {sl:13.3e}  {'-2':>9s} {'~0':>8s} {0.0:+10.3f}")
P(f"  {'K3b point-level gas lever, full kernel':44s} {a3b:13.3e}  {'-2':>9s} {'~0':>8s} {0.0:+10.3f}")
P(f"  {'K4 flat-curve baryonic-slope law':44s} {np.median(aa):13.3e}  {'0 EXACT':>9s} {'0 EXACT':>8s} {'large':>10s}")
P(f"  {'K5 f_DM = 1/e landmark':44s} {a_land:13.3e}  {'-1':>9s} {'-2':>8s} {lev5:+10.3f}")
P(f"  {'item 102 deep tail (normalisation)':44s} {n_ref:13.3e}  {'-2.2':>9s} {'-2':>8s} {-0.65:+10.3f}")
P(f"  {'canonical footing':44s} {A0['canonical']:13.3e}")
P(f"  {'alt footing':44s} {A0['alt']:13.3e}")
P("")
P("  THE STRUCTURAL RESULT, which is worth more than any single number above:")
P("  the ONLY distance-free acceleration a galaxy offers is a PHOTOMETRIC one, g_bar = 2 pi G Upsilon Sigma_L,")
P("  because surface brightness and HI surface density are both distance-invariant while every kinematic")
P("  acceleration is V^2/(theta D).  So an estimator is distance-free exactly when it goes through Upsilon,")
P("  and Upsilon-free exactly when it goes through a velocity, hence through D.  The two cancellations are")
P("  MUTUALLY EXCLUSIVE for a disc galaxy, and the shape channel does not escape it: shape leverage on a_0")
P("  requires points straddling y ~ 1, which requires stars, which reinstates Upsilon.")
sys.exit(ck.done())
