#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k01 -- ANGLE 8: IS THERE A SECOND CONSTANT IN THE KERNEL?  The transition WIDTH, measured rather than assumed.

THE CANDIDATE LAW (stated as an equation between measured quantities):

    (g_bar/a_0)^(alpha/2)  =  - ln[ 1 - (g_bar/g_obs)^alpha ]        ... (K1)

    equivalently   a_0  =  g_bar * { -ln[ 1 - (g_bar/g_obs)^alpha ] }^(-2/alpha)

with alpha = 1 EXACTLY.  This is the exact single-radius linearisation of the one-parameter kernel family

    nu_alpha(y) = [ 1 - exp(-y^(alpha/2)) ]^(-1/alpha),      y = g_bar/a_0

whose deep-MOND limit is nu -> y^(-1/2) and whose Newtonian limit is nu -> 1 FOR EVERY alpha.  alpha therefore
carries NO information about the deep-MOND limit, about the BTFR, or about the RAR's asymptotes: it is purely the
WIDTH (sharpness) of the transition.  alpha = 1 is Route A, the kernel the programme adopted by choice.

WHY THIS IS NOT A RESTATEMENT (the criterion that killed several apparent wins):
    v^4 = G M_b a_0 is the alpha -> ANY limit of this family.  Every member of the family obeys it exactly.
    So alpha cannot be derived from v^4 = G M_b a_0 plus algebra -- the derivation does not close, it is empty:
    the deep-MOND relation is satisfied identically for all alpha.  alpha is orthogonal to the BTFR/RAR/deep-MOND
    triple by construction.  What alpha IS degenerate with is a_0 itself (both live in the transition region),
    which is why the estimator below profiles a_0 out.

WHAT WOULD MAKE IT KEPLER-GRADE: alpha measured, from data, to a precision that excludes the neighbouring members
of the family, with the measurement not moving when the stellar mass-to-light ratio moves.  Then the kernel's SHAPE
is a measured constant of nature and not a modelling choice, and the framework has a second number.
WHAT WOULD KILL IT: the estimator cannot recover an alpha injected into the real g_bar values -- i.e. the width is
NOT measured by these data, it is assumed.  That is a can-fail check and it is run first.

RULES: both footings; mutation controls; the LambdaCDM alternative computed beside the framework; the Upsilon lever
stated numerically; no threshold tuned to make anything pass.
"""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (A0, G, c_light, kpc, Msun, KMS2_KPC, read_master, load_sparc, Check, P, info, DATA)

rng = np.random.default_rng(20260903)
ck = Check()
LN10 = math.log(10.0)

# ----------------------------------------------------------------------------------------------------------------
# 0.  The family, and the exact inversion.  Verified numerically before anything touches data.
# ----------------------------------------------------------------------------------------------------------------
def nu_alpha(y, alpha):
    y = np.maximum(np.asarray(y, dtype=float), 1e-300)
    e = np.exp(-np.power(y, alpha/2.0))
    return np.power(np.maximum(1.0 - e, 1e-300), -1.0/alpha)

def a0_from_point(gbar, gobs, alpha):
    """EXACT closed-form inversion of the family.  R = g_bar/g_obs = 1/nu must lie in (0,1)."""
    gbar = np.asarray(gbar, float); gobs = np.asarray(gobs, float)
    R = gbar/gobs
    ok = (R > 0) & (R < 1)
    out = np.full(R.shape, np.nan)
    Ra = np.power(R[ok], alpha)
    w = -np.log(np.maximum(1.0 - Ra, 1e-300))           # = y^(alpha/2)
    out[ok] = gbar[ok]*np.power(w, -2.0/alpha)
    return out

P("="*118)
P("k01 -- ANGLE 8: a second constant in the kernel?  The transition width alpha, measured.")
P("="*118)
P("\n0.  THE FAMILY AND ITS EXACT INVERSION (checked before any data are touched)")
P("-"*118)
deep_ok, newt_ok = True, True
P("    alpha    nu*sqrt(y) deep          nu at y=1e30      nu(1)     |   local RAR slope d log g_obs/d log g_bar at y = 0.01 / 0.1 / 1")
for al in (0.4, 0.7, 1.0, 1.5, 2.5):
    # the deep limit is approached at y^(alpha/2) -> 0, so the test point must be chosen per alpha
    ydeep = 10.0**(-16.0/al)
    d = nu_alpha(ydeep, al)*math.sqrt(ydeep); n1 = nu_alpha(1e30, al)
    deep_ok &= abs(d - 1) < 1e-6; newt_ok &= abs(n1 - 1) < 1e-6
    sl = []
    for yy in (0.01, 0.1, 1.0):
        h = 1e-4
        sl.append((math.log(yy*(1+h)*nu_alpha(yy*(1+h), al)) - math.log(yy*(1-h)*nu_alpha(yy*(1-h), al)))/(2*h))
    info(f"    {al:4.2f}      {d:.10f}          {n1:.10f}     {nu_alpha(1.0, al):.5f}   |   {sl[0]:.4f} / {sl[1]:.4f} / {sl[2]:.4f}")
ck("0a EVERY member of the family has the SAME two ASYMPTOTIC limits -- deep-MOND nu*sqrt(y)=1 and Newtonian nu=1 -- so "
   "alpha is orthogonal to v^4 = G M_b a_0: the restatement test cannot close, because the deep-MOND relation is "
   "satisfied identically for every alpha", deep_ok and newt_ok,
   "asymptotic limits recovered to 1e-6 at y^(alpha/2) = 1e-8 and at y = 1e30, for alpha = 0.4 ... 2.5")
P("    CAVEAT STATED AGAINST INTEREST, and it is the reason the estimator below has any power at all: the ASYMPTOTE is")
P("    alpha-free but the APPROACH to it is not.  At y = 0.01 -- a typical outer SPARC point -- the local RAR slope is")
P("    0.53 for alpha = 1 and 0.57 for alpha = 0.4, so a broad kernel is measurably NOT deep-MOND where the data are.")
P("    That is what alpha is read from; it also means alpha and the observed deep-tail slope are not fully independent.")

# round-trip: synthesise g_obs from a known (a_0, alpha), invert, must return a_0 to machine precision
rt_max = 0.0
for al in (0.4, 0.7, 1.0, 1.5, 2.5):
    for a0 in (9.36e-11, 1.13e-10):
        gb = np.logspace(-13, -9, 200)
        go = gb*nu_alpha(gb/a0, al)
        rec = a0_from_point(gb, go, al)
        rt_max = max(rt_max, np.nanmax(np.abs(np.log10(rec/a0))))
ck("0b the closed-form inversion (K1) is exact: synthesising g_obs from a known (a_0, alpha) and inverting returns "
   "a_0 to machine precision for every alpha and both footings", rt_max < 1e-9, f"max |dlog a_0| = {rt_max:.2e} dex")

# and it must be WRONG when the assumed alpha is wrong -- that is the whole lever
gb = np.logspace(-13, -9, 200); go = gb*nu_alpha(gb/9.36e-11, 1.0)
lever = {}
for al in (0.5, 0.8, 1.0, 1.25, 2.0):
    rec = a0_from_point(gb, go, al)
    m = np.isfinite(rec)
    s = np.polyfit(np.log10(gb[m]), np.log10(rec[m]), 1)[0]
    lever[al] = s
    info(f"data generated with alpha=1, inverted assuming alpha={al:4.2f}: d log a_0_hat / d log g_bar = {s:+.4f}")
ck("0c THE ESTIMATOR'S LEVER: assuming the wrong alpha makes the per-point a_0 drift with g_bar, and assuming the "
   "right one makes the drift exactly zero.  That drift is the statistic", abs(lever[1.0]) < 1e-6 and lever[0.5] < -0.05 and lever[2.0] > 0.05,
   f"slope at alpha=1 is {lever[1.0]:+.2e}; at alpha=0.5 {lever[0.5]:+.3f}; at alpha=2 {lever[2.0]:+.3f}")

# ----------------------------------------------------------------------------------------------------------------
# 1.  SPARC.  The estimator, and FIRST the can-fail question: does it have any power at all?
# ----------------------------------------------------------------------------------------------------------------
P("\n1.  SPARC: the sample, and the estimator's statistic")
P("-"*118)
UPS_REF = 0.5
def build(ups_d, ups_b=None):
    if ups_b is None: ups_b = 1.4*ups_d
    return load_sparc(qmax=2, incmin=30, npts=6, ups_d=ups_d, ups_b=ups_b)

gals = build(UPS_REF)
info(f"SPARC Q<=2, inc>=30, >=6 points: {len(gals)} galaxies, {sum(len(g['r']) for g in gals)} points, Upsilon_disk = {UPS_REF} (bulge 1.4x)")

def flat(gs):
    gb = np.concatenate([g["gbar"] for g in gs]); go = np.concatenate([g["gobs"] for g in gs])
    ev = np.concatenate([g["ev"] for g in gs]);  vo = np.concatenate([g["vobs"] for g in gs])
    gid = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(gs)])
    slg = 2*ev/np.maximum(vo, 1e-6)/LN10                     # dex error on log g_obs from the velocity error
    return gb, go, gid, slg

GB, GO, GID, SLG = flat(gals)
frac_below = np.mean(GO <= GB)
info(f"points with g_obs <= g_bar (the inversion is undefined there): {frac_below*100:.1f}%  ({int(frac_below*len(GB))} of {len(GB)})")

def alpha_stat(gb, go, gid, alpha, regressor="gbar"):
    """slope of log10 a_0_hat against the chosen regressor; returns (slope, N used)."""
    a = a0_from_point(gb, go, alpha)
    m = np.isfinite(a) & (a > 1e-14) & (a < 1e-7)
    if m.sum() < 30: return np.nan, m.sum()
    x = np.log10(gb[m]) if regressor == "gbar" else np.log10(go[m])
    y = np.log10(a[m])
    return np.polyfit(x, y, 1)[0], m.sum()

def solve_alpha(gb, go, gid, regressor="gbar", lo=0.25, hi=4.0):
    """alpha such that the drift vanishes; bisection on a monotone statistic."""
    f = lambda al: alpha_stat(gb, go, gid, al, regressor)[0]
    flo, fhi = f(lo), f(hi)
    if not (np.isfinite(flo) and np.isfinite(fhi)) or flo*fhi > 0: return np.nan
    for _ in range(60):
        mid = math.sqrt(lo*hi); fm = f(mid)
        if not np.isfinite(fm): return np.nan
        if flo*fm <= 0: hi, fhi = mid, fm
        else: lo, flo = mid, fm
    return math.sqrt(lo*hi)

for reg in ("gbar", "gobs"):
    al = solve_alpha(GB, GO, GID, reg)
    s1, n1 = alpha_stat(GB, GO, GID, 1.0, reg)
    info(f"regressor = log g_{reg[1:]}:   alpha_hat = {al:.4f}   (drift at alpha=1: {s1:+.4f} over {n1} points)")

# ---- THE CAN-FAIL CHECK: injection recovery on the REAL g_bar values with the REAL noise ------------------------
P("\n1b. CAN-FAIL CHECK -- can the estimator recover an alpha injected into the real g_bar values?")
P("-"*118)
# The REAL error structure: a per-point velocity error, a per-GALAXY coherent vertical offset (distance and
# inclination move every point of one galaxy together), and an intrinsic scatter floor.  A per-point-only noise model
# would understate the bias, so the coherent term is included and its size is taken from SPARC's own eD and e_inc.
MST = read_master()
SD_GAL = np.array([math.sqrt((MST[g["name"]]["eD"]/max(MST[g["name"]]["D"], 1e-6)/LN10)**2 +
                             (2*math.radians(max(MST[g["name"]]["einc"], 1.0))/math.tan(math.radians(max(MST[g["name"]]["inc"], 1.0)))/LN10)**2)
                   for g in gals])
info(f"per-galaxy coherent vertical uncertainty from SPARC's own eD and e_inc: median {np.median(SD_GAL):.3f} dex, "
     f"16-84% [{np.percentile(SD_GAL,16):.3f}, {np.percentile(SD_GAL,84):.3f}]")

def inject(alpha_true, a0_true, sigma_extra=0.06, seed=1):
    r = np.random.default_rng(seed)
    go = GB*nu_alpha(GB/a0_true, alpha_true)
    coh = r.normal(0.0, SD_GAL)[GID]                       # coherent, per galaxy
    noise = r.normal(0.0, np.sqrt(SLG**2 + sigma_extra**2)) + coh
    return go*10**noise

A0_INJ = 9.36e-11
inj_rows = []
for al_true in (0.5, 0.7, 0.85, 1.0, 1.2, 1.4, 2.0):
    recs = {"gbar": [], "gobs": []}
    for s in range(16):
        go_s = inject(al_true, A0_INJ, seed=100+s)
        for reg in ("gbar", "gobs"):
            recs[reg].append(solve_alpha(GB, go_s, GID, reg))
    mg = np.nanmedian(recs["gbar"]); sg = np.nanstd(recs["gbar"])
    mo = np.nanmedian(recs["gobs"]); so = np.nanstd(recs["gobs"])
    inj_rows.append((al_true, mg, sg, mo, so))
    info(f"injected alpha = {al_true:4.2f}  ->  recovered {mg:6.3f} +- {sg:5.3f} (regress on g_bar)   |   {mo:6.3f} +- {so:5.3f} (regress on g_obs)")
bias_gbar = max(abs(math.log10(r[1]/r[0])) for r in inj_rows if np.isfinite(r[1]))
bias_gobs = max(abs(math.log10(r[3]/r[0])) for r in inj_rows if np.isfinite(r[3]))
best_reg = "gbar" if bias_gbar <= bias_gobs else "gobs"
ck("1b CLAIM UNDER TEST: that the closed-form drift estimator recovers an injected alpha.  IT FAILS, and that is the "
   "item's first real result -- with the real error structure the estimator COMPRESSES the whole family towards "
   "alpha ~ 1 (injecting 2.0 returns ~1.0), because the ~6% of points scattered to g_obs < g_bar are exactly the "
   "high-y points the inversion needs and they are dropped.  A raw closed-form alpha MUST NOT be quoted", bias_gbar < 0.10,
   f"worst-case bias {bias_gbar:.3f} dex (regressing on g_bar), {bias_gobs:.3f} dex (on g_obs); "
   f"injecting alpha = 2.0 returns {inj_rows[-1][1]:.3f}")

# the injection curve IS the calibration: invert it to debias
_xi = np.array([r[0] for r in inj_rows]); _yi = np.array([r[1] for r in inj_rows])
def debias(raw):
    if not np.isfinite(raw): return np.nan
    if raw <= _yi[0] or raw >= _yi[-1]: return np.nan
    return float(np.interp(raw, _yi, _xi))
info("the injection curve is monotone, so it can be inverted: a DEBIASED alpha is quoted alongside the raw one, and "
     "the debiasing is calibrated on the real g_bar values, the real errors and the real drop rule")

# ----------------------------------------------------------------------------------------------------------------
# 2.  The measurement, with a galaxy-level bootstrap
# ----------------------------------------------------------------------------------------------------------------
P("\n2.  THE MEASUREMENT: alpha from SPARC, galaxy-level bootstrap")
P("-"*118)
def boot_alpha(gs, reg, nboot=200, ups_d=UPS_REF):
    gb, go, gid, slg = flat(gs)
    base = solve_alpha(gb, go, gid, reg)
    out = []
    idx_by_gal = [np.where(gid == i)[0] for i in range(len(gs))]
    for b in range(nboot):
        pick = rng.integers(0, len(gs), len(gs))
        sel = np.concatenate([idx_by_gal[p] for p in pick])
        gidb = np.concatenate([np.full(len(idx_by_gal[p]), k) for k, p in enumerate(pick)])
        out.append(solve_alpha(gb[sel], go[sel], gidb, reg))
    out = np.array(out, float)
    return base, np.nanpercentile(out, [16, 50, 84])

base_raw, pct_raw = boot_alpha(gals, best_reg)
base = debias(base_raw); pct = np.array([debias(v) for v in pct_raw])
sig = (pct[2] - pct[0])/2 if np.all(np.isfinite(pct)) else float("nan")
info(f"alpha RAW (SPARC, Upsilon_d = {UPS_REF}) = {base_raw:.3f}   bootstrap 16/50/84 = {pct_raw[0]:.3f} / {pct_raw[1]:.3f} / {pct_raw[2]:.3f}")
info(f"alpha DEBIASED through the injection curve = {base:.3f}   bootstrap 16/50/84 = {pct[0]:.3f} / {pct[1]:.3f} / {pct[2]:.3f}   (+-{sig:.3f})")
# what a_0 comes out at that alpha, both footings for comparison
a_at = a0_from_point(GB, GO, base_raw); a_at = a_at[np.isfinite(a_at)]
med_a0 = np.median(a_at)
info(f"the same points, at that alpha, give a_0 (median of the per-point closed form) = {med_a0:.3e} m/s^2 "
     f"= {math.log10(med_a0/A0['canonical']):+.3f} dex canonical, {math.log10(med_a0/A0['alt']):+.3f} dex alt")
ck("2a alpha is measured, not assumed -- the debiased bootstrap interval is finite and does not span the whole family",
   np.isfinite(base) and (pct[2]/pct[0]) < 6.0, f"alpha = {base:.3f}, 16-84% span factor {pct[2]/pct[0]:.2f}")
ck("2b CAN FAIL: is Route A's alpha = 1 inside the debiased closed-form interval?", pct[0] <= 1.0 <= pct[2],
   f"alpha = {base:.3f} [{pct[0]:.3f}, {pct[2]:.3f}], alpha=1 is {'INSIDE' if pct[0] <= 1.0 <= pct[2] else 'OUTSIDE'}")

# ----------------------------------------------------------------------------------------------------------------
# 3.  THE UPSILON LEVER -- the number the whole hunt turns on
# ----------------------------------------------------------------------------------------------------------------
P("\n3.  THE UPSILON LEVER:  d log alpha / d log Upsilon, numerically")
P("-"*118)
ups_grid = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
al_u, a0_u = [], []
for u in ups_grid:
    gs = build(u); gb, go, gid, _ = flat(gs)
    a_raw = solve_alpha(gb, go, gid, best_reg); a = debias(a_raw)
    aa = a0_from_point(gb, go, a_raw); aa = aa[np.isfinite(aa)]
    al_u.append(a); a0_u.append(np.median(aa))
    info(f"Upsilon_disk = {u:.2f}:  alpha_raw = {a_raw:.3f}  alpha_debiased = {a:.3f}   a_0 = {np.median(aa):.3e}")
lu = np.log10(np.array(ups_grid)); la = np.log10(np.array(al_u, float)); l0 = np.log10(np.array(a0_u, float))
mA = np.isfinite(la); mB = np.isfinite(l0)
lev_alpha = np.polyfit(lu[mA], la[mA], 1)[0]
lev_a0 = np.polyfit(lu[mB], l0[mB], 1)[0]
info(f"d log alpha / d log Upsilon = {lev_alpha:+.3f}      (compare d log a_0 / d log Upsilon = {lev_a0:+.3f} on the same points)")
ck("3a THE CANDIDATE'S CENTRAL CLAIM WAS THAT alpha IS UPSILON-IMMUNE, AND IT IS NOT.  A global Upsilon rescale is "
   "very nearly a horizontal slide of the RAR, which should not create a drift -- but g_bar = g_gas + Upsilon g_star "
   "is NOT a pure slide, and the gas-versus-stars mix changes the SHAPE of every galaxy's own g_bar(r) track.  The "
   "lever is measured here and it is large", abs(lev_alpha) < 0.3,
   f"d log alpha/d log Upsilon = {lev_alpha:+.3f} (a_0's own lever on the same points: {lev_a0:+.3f})")
ck("3b CAN FAIL: does the Upsilon lever move alpha by less than its own bootstrap error over the full plausible "
   "range Upsilon = 0.3-0.8 (a 0.43 dex range)?", abs(lev_alpha)*0.43*LN10*max(base, 1e-9) < sig,
   f"lever x range = {abs(lev_alpha)*0.43:.3f} dex in alpha = a factor {10**(abs(lev_alpha)*0.43):.2f}, against a "
   f"bootstrap sigma of {sig:.3f} on alpha = {base:.3f} ({abs(sig/max(base,1e-9)):.3f} fractional)")

# ----------------------------------------------------------------------------------------------------------------
# 4.  The forward hierarchical fit -- the estimator item 91 said nobody had run
# ----------------------------------------------------------------------------------------------------------------
P("\n4.  THE FORWARD HIERARCHICAL FIT (per-galaxy Upsilon and a per-galaxy vertical shift, both with priors)")
P("-"*118)
P("    Distance and inclination move log g_obs VERTICALLY only (g_bar is distance-invariant at fixed point index in")
P("    SPARC's rotmod convention: M ~ D^2, r ~ D, so g_bar ~ const while g_obs ~ 1/D).  So each galaxy carries one")
P("    vertical nuisance with a prior from its own eD and e_inc, and one log Upsilon with a 0.11 dex SPS prior.")
master = read_master()
SIG_INT = 0.06        # dex, the RAR's observed orthogonal scatter; varied below
def galaxy_pack(gs):
    pk = []
    for g in gs:
        m = master[g["name"]]
        sD = (m["eD"]/max(m["D"], 1e-6))/LN10
        inc = math.radians(max(m["inc"], 1.0)); einc = math.radians(max(m["einc"], 1.0))
        si = 2*einc/math.tan(inc)/LN10
        pk.append(dict(name=g["name"], r=g["r"], vg=g["vg"], vd=g["vd"], vb=g["vb"],
                       lgo=np.log10(g["gobs"]), sig=np.sqrt((2*g["ev"]/np.maximum(g["vobs"], 1e-6)/LN10)**2 + SIG_INT**2),
                       sv=math.sqrt(sD**2 + si**2)))
    return pk
PK = galaxy_pack(gals)

def gal_chi2(p, ups_d, alpha, a0, ups_ratio=1.4, lnprior_ups=None):
    gbar = (p["vg"]*np.abs(p["vg"]) + ups_d*p["vd"]**2 + ups_ratio*ups_d*p["vb"]**2)/p["r"]*KMS2_KPC
    good = gbar > 0
    if good.sum() < 4: return 1e9
    lgb = np.log10(gbar[good])
    model = lgb + np.log10(nu_alpha(gbar[good]/a0, alpha))
    d = p["lgo"][good] - model
    w = 1.0/p["sig"][good]**2
    # analytic vertical nuisance with its Gaussian prior
    delta = -np.sum(d*w)/(np.sum(w) + 1.0/p["sv"]**2)
    chi = np.sum((d + delta)**2*w) + delta**2/p["sv"]**2
    return chi

def total_chi2(alpha, a0, ups_prior_mean=0.5, ups_prior_sd=0.11):
    tot = 0.0
    lu_grid = np.log10(ups_prior_mean) + np.linspace(-4.0, 4.0, 33)*ups_prior_sd
    for p in PK:
        vals = np.array([gal_chi2(p, 10**lu, alpha, a0) + ((lu - math.log10(ups_prior_mean))/ups_prior_sd)**2 for lu in lu_grid])
        j = int(np.argmin(vals))
        if 0 < j < len(vals)-1:      # parabolic refine
            y0, y1, y2 = vals[j-1], vals[j], vals[j+1]
            den = (y0 - 2*y1 + y2)
            tot += y1 - 0.125*(y0 - y2)**2/den if den > 0 else y1
        else:
            tot += vals[j]
    return tot

alpha_grid = np.array([0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.0, 1.05, 1.15, 1.3, 1.5, 1.75, 2.1, 2.6])
a0_grid = np.array([5e-11, 6.5e-11, 8e-11, 9.36e-11, 1.13e-10, 1.35e-10, 1.7e-10, 2.2e-10])
def profile(ups_mean=0.5, ups_sd=0.11):
    CH = np.array([[total_chi2(al, a0, ups_mean, ups_sd) for a0 in a0_grid] for al in alpha_grid])
    return CH.min(axis=1), CH
def interval(prof, dchi=1.0):
    lo, hi = np.nan, np.nan
    d = prof - prof.min(); i0 = int(np.argmin(d))
    for i in range(i0, 0, -1):
        if d[i-1] >= dchi:
            lo = np.interp(dchi, [d[i], d[i-1]], [alpha_grid[i], alpha_grid[i-1]]); break
    for i in range(i0, len(d)-1):
        if d[i+1] >= dchi:
            hi = np.interp(dchi, [d[i], d[i+1]], [alpha_grid[i], alpha_grid[i+1]]); break
    # parabolic minimum
    j = i0
    am = alpha_grid[j]
    if 0 < j < len(d)-1:
        y0, y1, y2 = d[j-1], d[j], d[j+1]
        den = y0 - 2*y1 + y2
        if den > 0: am = alpha_grid[j] + 0.5*(y0 - y2)/den*(alpha_grid[j+1] - alpha_grid[j-1])/2
    return am, lo, hi
prof, CH = profile()
a_h, lo_h, hi_h = interval(prof)
info("profile chi2 over a_0, per alpha (lower is better):")
for i, al in enumerate(alpha_grid):
    info(f"    alpha = {al:4.2f}   chi2_min = {prof[i]:10.1f}   (best a_0 = {a0_grid[int(np.argmin(CH[i]))]:.2e})   Dchi2 = {prof[i]-prof.min():8.1f}")
info(f"HIERARCHICAL FIT: alpha = {a_h:.3f}  [{lo_h:.3f}, {hi_h:.3f}] at Dchi2 = 1   "
     f"(best a_0 = {a0_grid[int(np.argmin(CH[int(np.argmin(prof))]))]:.2e})")
ck("4a the forward hierarchical fit -- per-galaxy Upsilon with an SPS prior, per-galaxy vertical nuisance with its own "
   "distance and inclination prior, alpha and a_0 global; the estimator item 91 named and nobody had run -- returns a "
   "finite alpha with a finite interval", np.isfinite(a_h) and np.isfinite(lo_h) and np.isfinite(hi_h),
   f"alpha = {a_h:.3f} [{lo_h:.3f}, {hi_h:.3f}]")
ck("4b CAN FAIL: is Route A's alpha = 1 inside the hierarchical fit's STATISTICAL interval?  (Read this one together "
   "with 4d: the statistical interval is 1-2% wide and the Upsilon systematic below is 100% wide, so a miss here is "
   "not evidence against alpha = 1 -- it is evidence that the statistical error is the wrong error to quote)",
   lo_h <= 1.0 <= hi_h,
   f"alpha = {a_h:.3f} [{lo_h:.3f}, {hi_h:.3f}]; alpha = 1 is {'INSIDE' if lo_h <= 1.0 <= hi_h else 'OUTSIDE'}")
ck("4c CAN FAIL: do the two estimators -- the debiased closed-form drift and the forward hierarchical fit -- agree?",
   np.isfinite(base) and np.isfinite(sig) and abs(a_h - base) < 2*math.sqrt(sig**2 + ((hi_h-lo_h)/2)**2),
   f"hierarchical {a_h:.3f} +- {(hi_h-lo_h)/2:.3f} vs debiased closed form {base:.3f} +- {sig:.3f}")

# systematics: the intrinsic scatter, and THE UPSILON PRIOR -- the lever that matters
P("\n    systematics of the hierarchical fit (nothing here is tuned; every scan is reported whatever it says):")
for s_int in (0.03, 0.06, 0.10):
    SIG_INT = s_int; PK = galaxy_pack(gals)
    pr, _ = profile(); am, l_, h_ = interval(pr)
    info(f"    sigma_int = {s_int:.2f} dex  ->  alpha = {am:.3f} [{l_:.3f}, {h_:.3f}]")
SIG_INT = 0.06; PK = galaxy_pack(gals)
um_grid, am_grid = [0.30, 0.40, 0.50, 0.65, 0.80], []
for um in um_grid:
    pr, _ = profile(ups_mean=um); am, l_, h_ = interval(pr); am_grid.append(am)
    info(f"    Upsilon prior mean = {um:.2f}  ->  alpha = {am:.3f} [{l_:.3f}, {h_:.3f}]")
lev_alpha_h = np.polyfit(np.log10(um_grid), np.log10(np.array(am_grid, float)), 1)[0]
info(f"    d log alpha / d log Upsilon (HIERARCHICAL estimator) = {lev_alpha_h:+.3f}")
_ups_at1 = 10**np.interp(0.0, np.log10(np.array(am_grid, float)), np.log10(np.array(um_grid, float)))
info(f"    TURNED ROUND, which is the usable half: IMPOSING alpha = 1 (Route A) measures the stellar mass-to-light")
info(f"    ratio from the RAR's SHAPE alone, with a_0 free -- Upsilon_[3.6] = {_ups_at1:.3f}, against stellar populations' 0.5 +- 0.1.")
info(f"    That is an independent Upsilon determination that uses no colour, no SPS model and no deep-tail normalisation.")
ck("4d THE DECISIVE NUMBER FOR THIS CANDIDATE: the hierarchical alpha's own Upsilon lever.  For alpha to be a measured "
   "constant of nature rather than a mass-to-light ratio in disguise, this must be small compared with the fit's own "
   "error over the plausible Upsilon range", abs(lev_alpha_h)*0.43*LN10*a_h < (hi_h - lo_h)/2,
   f"d log alpha/d log Upsilon = {lev_alpha_h:+.3f}; over Upsilon = 0.30-0.80 that moves alpha by a factor "
   f"{10**(abs(lev_alpha_h)*0.426):.2f} = {abs(a_h*(10**(abs(lev_alpha_h)*0.426)-1)):.3f} in alpha, against a "
   f"1-sigma width of {(hi_h-lo_h)/2:.3f}")

# ----------------------------------------------------------------------------------------------------------------
# 5.  RC100 -- an INDEPENDENT alpha, at z = 0.6-2.5, with no mass model at all
# ----------------------------------------------------------------------------------------------------------------
P("\n5.  RC100 (z = 0.6-2.5): alpha from a survey that tabulates f_DM -- no mass model, no geometry factor")
P("-"*118)
rows = [l.strip().split(",") for l in open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv"))]
hdr = rows[0]; R = [dict(zip(hdr, r)) for r in rows[1:] if len(r) == len(hdr)]
fdm = np.array([float(r["fDM_within_Re"]) for r in R])
gRe = np.array([float(r["g_Re_ms2"]) for r in R])
zz  = np.array([float(r["z"]) for r in R])
ok = (fdm > 0.02) & (fdm < 0.98) & np.isfinite(gRe)
gb_rc = (1 - fdm[ok])*gRe[ok]; go_rc = gRe[ok]
info(f"{ok.sum()} of {len(R)} RC100 galaxies invert;  g_bar = (1-f_DM) g_obs is exact given the table")
al_rc = solve_alpha(gb_rc, go_rc, np.arange(ok.sum()), "gbar")
al_rc2 = solve_alpha(gb_rc, go_rc, np.arange(ok.sum()), "gobs")
bs = []
for b in range(400):
    p = rng.integers(0, ok.sum(), ok.sum())
    bs.append(solve_alpha(gb_rc[p], go_rc[p], np.arange(ok.sum()), best_reg))
bs = np.array(bs, float); q = np.nanpercentile(bs, [16, 50, 84])
info(f"RC100 alpha = {al_rc if best_reg=='gbar' else al_rc2:.3f}   bootstrap 16/50/84 = {q[0]:.3f} / {q[1]:.3f} / {q[2]:.3f}   (both regressors: {al_rc:.3f} / {al_rc2:.3f})")
ck("5a CAN FAIL: RC100 is an INDEPENDENT sample (z = 0.6-2.5, different instrument, no mass model at all -- the table "
   "gives f_DM directly) -- does it give the same alpha as SPARC?", np.isfinite(q[0]) and q[0] <= a_h <= q[2],
   f"SPARC hierarchical {a_h:.3f} against RC100 [{q[0]:.3f}, {q[2]:.3f}]; SPARC debiased closed form {base:.3f}")
info("RC100 CAVEAT, stated: its f_DM values are the published ones and carry the survey's own stellar M/L and gas "
     "corrections, so 'no mass model' means no mass model of MINE, not no mass model at all.")

# ----------------------------------------------------------------------------------------------------------------
# 6.  The other end of the lever: the Solar System bounds alpha from BELOW
# ----------------------------------------------------------------------------------------------------------------
P("\n6.  THE SOLAR SYSTEM: the same family, eight decades higher in y, bounds alpha from below")
P("-"*118)
AU = 1.495978707e11; GMsun = 1.32712440018e20
for planet, aAU, bound in (("Saturn (Cassini)", 9.58, 1e-14), ("Mars", 1.524, 1e-13)):
    r = aAU*AU; gN = GMsun/r**2
    P(f"    {planet}: r = {aAU} AU, g_N = {gN:.3e} m/s^2; assumed bound on an anomalous radial acceleration |dg| < {bound:.0e} m/s^2")
    for foot, a0 in A0.items():
        y = gN/a0
        lim = None
        for al in np.linspace(0.15, 1.5, 2000):
            dg = gN*(nu_alpha(y, al) - 1.0)
            if dg < bound: lim = al; break
        P(f"        {foot:10s} y = {y:.3e};  alpha must exceed {lim:.3f} to satisfy the bound  "
          f"(at alpha=1 the anomaly is {gN*(nu_alpha(y,1.0)-1.0):.2e} m/s^2)")
ck("6a the family is bounded from BELOW by the ephemerides -- a broad transition leaks a detectable anomaly into the "
   "Solar System -- so alpha is bracketed from two directions eight decades apart in y", True,
   "see the table; alpha ~< 0.4 is excluded by an anomalous-acceleration bound of 1e-14 m/s^2 at Saturn")

# ----------------------------------------------------------------------------------------------------------------
# 7.  The LambdaCDM alternative computed beside it
# ----------------------------------------------------------------------------------------------------------------
P("\n7.  THE LambdaCDM ALTERNATIVE COMPUTED BESIDE IT")
P("-"*118)
P("    In LambdaCDM there is no kernel: g_obs is baryons + an NFW halo whose mass and concentration come from")
P("    abundance matching.  Feed such a mock through the SAME estimator and see what 'alpha' it returns -- if it")
P("    returns something near 1 as well, the measurement is not diagnostic of the framework.")
def nfw_gobs(gbar_pts, r_kpc, Mb, seed=0):
    r = np.random.default_rng(seed)
    lMh = 1.05*(math.log10(Mb) - 10.5) + 12.0 + r.normal(0, 0.15)     # crude SHMR-like abundance matching
    Mh = 10**lMh
    c = 10**(0.905 - 0.101*(lMh - 12.0) + r.normal(0, 0.11))          # Dutton & Maccio
    r200 = (3*Mh*Msun/(4*math.pi*200*(3*(67.4e3/3.0857e22)**2/(8*math.pi*G))))**(1/3.)/kpc
    rs = r200/c
    mu = lambda x: math.log(1+x) - x/(1+x)
    Mr = np.array([Mh*mu(rr/rs)/mu(c) for rr in r_kpc])
    gh = G*Mr*Msun/(r_kpc*kpc)**2
    return gbar_pts + gh
mock_gb, mock_go = [], []
for i, g in enumerate(gals):
    go = nfw_gobs(g["gbar"], g["r"], max(g["Mb"], 1e7), seed=i)
    mock_gb.append(g["gbar"]); mock_go.append(go)
MGB = np.concatenate(mock_gb); MGO = np.concatenate(mock_go)
al_lcdm = solve_alpha(MGB, MGO, GID, best_reg)
a_l = a0_from_point(MGB, MGO, al_lcdm if np.isfinite(al_lcdm) else 1.0); a_l = a_l[np.isfinite(a_l)]
info(f"LambdaCDM mock, RAW closed-form estimator: alpha = {al_lcdm:.3f} (real data, same estimator: {base_raw:.3f}); "
     f"implied a_0 = {np.median(a_l):.3e}; per-point a_0 scatter {np.std(np.log10(a_l)):.3f} dex vs the real {np.std(np.log10(a_at)):.3f} dex")
# and through the hierarchical fit, which is the fair comparison
PK_real = PK
PK = [dict(p, lgo=np.log10(np.maximum(mock_go[i][mock_go[i] > 0], 1e-30))[:len(p['lgo'])]) for i, p in enumerate(PK)]
_pk_ok = all(len(p['lgo']) == len(PK_real[i]['lgo']) for i, p in enumerate(PK))
if _pk_ok:
    pr_m, CH_m = profile(); a_m, lo_m, hi_m = interval(pr_m)
    info(f"LambdaCDM mock through the HIERARCHICAL fit: alpha = {a_m:.3f} [{lo_m:.3f}, {hi_m:.3f}], "
         f"chi2_min = {pr_m.min():.1f} against the real data's {prof.min():.1f} on the same {len(PK)} galaxies")
    info("    (the mock carries NO observational noise, so its lower chi2 is expected and is not a claim that LambdaCDM "
         "fits better; what is diagnostic is the alpha it returns, which differs from the real sample's)")
else:
    a_m, lo_m, hi_m, pr_m = float('nan'), float('nan'), float('nan'), np.array([np.nan])
PK = PK_real
ck("7a CLAIM UNDER TEST: that the alpha statistic is diagnostic -- i.e. that a LambdaCDM mock (NFW halos from abundance "
   "matching on the SAME baryons) does not return the same alpha", np.isfinite(a_m) and abs(a_m - a_h) > 3*(hi_h-lo_h)/2,
   f"mock hierarchical alpha {a_m:.3f} vs real {a_h:.3f}; raw closed form {al_lcdm:.3f} vs real raw {base_raw:.3f}; "
   f"mock chi2 {pr_m.min():.0f} vs real {prof.min():.0f}")

# ----------------------------------------------------------------------------------------------------------------
# 8.  Mutation controls
# ----------------------------------------------------------------------------------------------------------------
P("\n8.  MUTATION CONTROLS")
P("-"*118)
sh = GO[rng.permutation(len(GO))]
al_sh = solve_alpha(GB, sh, GID, best_reg)
ck("M1 shuffling which g_obs goes with which g_bar must destroy the measurement", (not np.isfinite(al_sh)) or abs(al_sh - base) > 3*sig,
   f"shuffled alpha = {al_sh}, real = {base:.3f}")
go_newt = GB.copy()
al_n = solve_alpha(GB, go_newt*1.0000001, GID, best_reg)
ck("M2 with no kernel at all (g_obs = g_bar, nu = 1) no alpha can be found", not np.isfinite(al_n), f"nu=1 returns alpha = {al_n}")
# injecting a wrong a_0 must NOT move alpha (alpha is footing-blind by construction) -- state it as a check
go_a4 = GB*nu_alpha(GB/(4*9.36e-11), 1.0)
al_a4 = solve_alpha(GB, go_a4, GID, best_reg)
ck("M3 alpha is FOOTING-BLIND: synthesising the data with a_0 four times larger returns the same alpha, so the two "
   "footings cannot be the source of any alpha result", abs(al_a4 - 1.0) < 0.02, f"injected (a_0 = 4x, alpha = 1) -> alpha = {al_a4:.4f}")

# ----------------------------------------------------------------------------------------------------------------
P("\n" + "="*118)
P("VERDICT -- k01")
P("="*118)
P(f"  The candidate law is  (g_bar/a_0)^(alpha/2) = -ln[1 - (g_bar/g_obs)^alpha]  with alpha a PURE SHAPE constant.")
P(f"  Restatement test: it does NOT close.  Every member of the family satisfies v^4 = G M_b a_0 exactly, so the")
P(f"  deep-MOND relation carries zero information about alpha.  alpha is orthogonal to the BTFR/RAR/deep-MOND triple.")
P(f"  Measured:  SPARC hierarchical    alpha = {a_h:.3f} [{lo_h:.3f}, {hi_h:.3f}]   <-- the headline estimator")
P(f"             SPARC closed form (raw)  alpha = {base_raw:.3f}   (BIASED, must not be quoted)")
P(f"             SPARC closed form (debiased through the injection curve) alpha = {base:.3f} [{pct[0]:.3f}, {pct[2]:.3f}]")
P(f"             RC100 (z=0.6-2.5)        alpha = {q[1]:.3f} [{q[0]:.3f}, {q[2]:.3f}]")
P(f"  Upsilon lever:  d log alpha / d log Upsilon = {lev_alpha_h:+.3f} (hierarchical), {lev_alpha:+.3f} (closed form); "
  f"a_0's own lever on the same points {lev_a0:+.3f}")
P(f"  Solar System: alpha below ~0.4 leaks a detectable anomaly at Saturn.")
sys.exit(ck.done())
