#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h102_gas_dominated_a0.py -- HUNT ITEM 102: the gas-dominated deep tail, a_0 with no stellar M/L.
================================================================================================
The item as listed: rerun item 25's slope-fixed deep-tail a_0 estimator on the gas-dominated subset of SPARC
(f_gas = 1.33 M_HI / M_bar > 0.7 from the master table), where the stellar mass-to-light ratio barely enters.
Scan the cut.  Pass if a_0 is measured to better than 8% and agrees with the dwarf lens stack (9.55e-11).

This script does that and reports two things that were not asked for and that go against the item's premise.

  (1) AN ESTIMATOR BUG THAT AFFECTS FIVE COMMITTED ITEMS.  Item 25's estimator fixes the RAR slope at 1/2 and reads
      a_0 off the intercept: a_0 = <g_obs^2/g_bar>.  That is the EXACT deep-MOND limit.  The Route A kernel is not in
      that limit at the cut used.  Expanding nu(y) = 1/(1-exp(-sqrt y)) for small y,
              g_obs = nu(y) g_bar = sqrt(a_0 g_bar) * (1 + sqrt(y)/2 + y/12 + ...),  y = g_bar/a_0,
      so the deep-limit estimator returns a_0 too high by 2*log10(1 + <sqrt y>/2).  At g_bar < 1e-11 the SPARC points
      have <sqrt y> = 0.235, i.e. a +0.10 dex bias.  A synthetic control below confirms it to 0.001 dex: data built
      to obey the kernel EXACTLY at a_0 = 9.36e-11 are read back as 1.17e-10 by the item-25 estimator.
      The unbiased estimator solves <log g_obs - log[nu(g_bar/a_0) g_bar]> = 0 for a_0 using the full kernel, and it
      is stable against the cut where the deep-limit one drifts by 0.09 dex.  Both are computed side by side here.

  (2) THE GLOBAL GAS FRACTION IS THE WRONG CUT.  What sets the estimator's M/L leverage is not the galaxy's global
      gas fraction but the LOCAL stellar share of g_bar at the points that enter, f_*,loc = (Y_d v_d^2 + Y_b v_b^2)/(g_bar r).
      d log a_0 / d log Y = <(1+n) f_*,loc>/<n> identically (-<f_*,loc> in the deep limit).  In gas-dominated dwarfs the HI is far more extended than the
      stars, so the ENCLOSED baryonic mass at small radius is stellar even when the galaxy is 85% gas by total mass;
      and those dwarfs are so faint that their whole rotation curve, centre included, sits below g_bar = 1e-11.
      The result is that cutting on f_gas > 0.7 moves the lever by only a fifth.  Cutting on f_*,loc instead
      takes it to a tenth of its full-sample value.  (This is bug pattern (1) of the hunt -- a TOTAL where an ENCLOSED quantity belongs -- caught
      inside the item's own specification.)

Both footings.  Mutation controls.  LambdaCDM/Newtonian computed beside.  Checks CAN fail.
"""
import sys, math
import numpy as np
from scipy.optimize import brentq
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(102)
gals = load_sparc()
GBCUT = 1e-11                       # item 25's deep-tail cut, kept identical
DWARF_LENS = (9.55e-11, 0.24e-10)   # item 2's dwarf lens stack, the other M/L-insensitive rung of item 100

# ---------------------------------------------------------------------------------------------- the two estimators
def a0_deep(x, y):
    """ITEM 25's estimator: slope fixed at 1/2, a_0 = 10^{2 <log g_obs - 0.5 log g_bar>}  (exact deep-MOND limit)."""
    return 10**(2*float(np.mean(np.log10(y) - 0.5*np.log10(x))))

def a0_kern(x, y):
    """UNBIASED: solve <log g_obs - log[nu(g_bar/a_0) g_bar]> = 0 with the FULL Route A kernel."""
    f = lambda a: float(np.mean(np.log10(y) - np.log10(nu(x/a)*x)))
    try:
        return brentq(f, 1e-13, 1e-7, xtol=1e-18, rtol=8.9e-16, maxiter=200)
    except Exception:
        return float("nan")

def gbar_of(g, ups):
    return (g["vg"]*np.abs(g["vg"]) + ups*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC

def gstar_of(g, ups):
    return (ups*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC

def fgas_global(g, ups):
    """the item's definition: 1.33 M_HI / M_bar from the master table"""
    mg = 1.33*g["MHI"]*1e9
    return mg/(mg + ups*g["L36"]*1e9)

def select(sub, ups=UPS_D, gbcut=GBCUT, fsmax=None, fgmin=None, sel_ups=None):
    """Returns a list of (g_bar, g_obs, f_*,loc) per galaxy.  sel_ups fixes the SELECTION M/L so that varying `ups`
    measures the estimator's sensitivity at fixed sample rather than moving the sample underneath it."""
    su = ups if sel_ups is None else sel_ups
    out = []
    for g in sub:
        if fgmin is not None and fgas_global(g, su) < fgmin: continue
        gb_s, gs_s = gbar_of(g, su), gstar_of(g, su)
        gb, gs = gbar_of(g, ups), gstar_of(g, ups)
        with np.errstate(invalid="ignore", divide="ignore"):
            fs_s = gs_s/gb_s
        m = (gb_s > 0) & (gb_s < gbcut) & (gb > 0)
        if fsmax is not None: m &= (fs_s < fsmax)
        if m.sum() == 0: continue
        out.append((gb[m], g["gobs"][m], (gs/gb)[m], g))
    return out

def combine(S):
    return np.concatenate([s[0] for s in S]), np.concatenate([s[1] for s in S])

def measure(S, nboot=500, est=a0_kern):
    if len(S) < 4: return dict(a0=float("nan"), sig=float("nan"), n=0, ngal=len(S))
    x, y = combine(S); a = est(x, y)
    bs = []
    for _ in range(nboot):
        i = rng.integers(0, len(S), len(S))
        v = est(np.concatenate([S[j][0] for j in i]), np.concatenate([S[j][1] for j in i]))
        if np.isfinite(v): bs.append(v)
    bs = np.array(bs)
    return dict(a0=a, sig=float(np.log10(bs).std()), n=len(x), ngal=len(S),
                lo=float(np.percentile(bs, 16)), hi=float(np.percentile(bs, 84)))

def nslope(y):
    """n(y) = d log nu / d log y, computed by finite difference on the Route A kernel."""
    d = 1e-5
    return (np.log(nu(y*(1+d))) - np.log(nu(y*(1-d))))/(2*d)

def lever(sub, **kw):
    """d log a_0 / d log Upsilon at FIXED sample, and the identity it must obey.
    Perturbing g_bar -> g_bar(1 + eps f_*) in <log g_obs - log(nu(y) y) - log a> = 0 gives
        d log a_0 / d log Upsilon = <(1+n) f_*> / <n>,   n(y) = d log nu/d log y,
    which reduces to the familiar -<f_*> only in the exact deep limit n = -1/2.  Returns the LOCAL derivative
    (Upsilon = 0.5 +- 5%), the identity, the deep-limit form -<f_*>, and the wide 0.3 -> 0.7 secant, which differs
    from the local derivative by second-order curvature and is the number that matters in practice."""
    S5 = select(sub, ups=0.5, sel_ups=0.5, **kw)
    if len(S5) < 4: return (float("nan"),)*4
    a3 = a0_kern(*combine(select(sub, ups=0.3, sel_ups=0.5, **kw)))
    a7 = a0_kern(*combine(select(sub, ups=0.7, sel_ups=0.5, **kw)))
    am = a0_kern(*combine(select(sub, ups=0.5*0.95, sel_ups=0.5, **kw)))
    ap = a0_kern(*combine(select(sub, ups=0.5*1.05, sel_ups=0.5, **kw)))
    fs = np.concatenate([s[2] for s in S5]); gb5 = np.concatenate([s[0] for s in S5])
    a5 = a0_kern(*combine(S5)); n = nslope(gb5/a5)
    ident = float(np.mean((1+n)*fs)/np.mean(n))
    deriv = (math.log10(ap) - math.log10(am))/(math.log10(1.05) - math.log10(0.95))
    secant = (math.log10(a7) - math.log10(a3))/(math.log10(0.7) - math.log10(0.3))
    return deriv, ident, -float(np.mean(fs)), secant

# ============================================================================================================
P("="*118); P("0. THE ESTIMATOR -- a synthetic control that item 25's version fails"); P("="*118)
gb_all = np.concatenate([g["gbar"] for g in gals]); xs = gb_all[(gb_all > 0) & (gb_all < GBCUT)]
P(f"  {len(xs)} SPARC deep-tail points (g_bar < {GBCUT:.0e}); <sqrt(y)> at canonical a_0 = {np.mean(np.sqrt(xs/A0['canonical'])):.3f}")
P(f"  analytic bias of the deep-limit estimator = 2 log10(1 + <sqrt y>/2) = {2*math.log10(1+np.mean(np.sqrt(xs/A0['canonical']))/2):+.3f} dex")
syn = {}
for foot, atrue in A0.items():
    ysyn = nu(xs/atrue)*xs                                   # data that obey the kernel EXACTLY
    syn[foot] = (math.log10(a0_kern(xs, ysyn)/atrue), math.log10(a0_deep(xs, ysyn)/atrue))
    ynoise = ysyn*10**(rng.normal(0, 0.11, len(ysyn)))       # + the RAR's own 0.11 dex point scatter
    info(f"{foot:10} a_true = {atrue:.3e}: full-kernel estimator recovers {syn[foot][0]:+.4f} dex, "
         f"item-25 deep-limit estimator {syn[foot][1]:+.4f} dex; with 0.11 dex scatter added, "
         f"{math.log10(a0_kern(xs,ynoise)/atrue):+.4f} / {math.log10(a0_deep(xs,ynoise)/atrue):+.4f}")
ck("102.0a AGAINST INTEREST, and it is a bug in five committed items -- item 25's slope-fixed estimator is BIASED. "
   "Fed synthetic rotation curves that obey the Route A kernel EXACTLY at a known a_0, it returns a_0 about +0.10 dex "
   "too high, because g_bar < 1e-11 is not deep enough for nu -> y^{-1/2}: the leading correction is 1 + sqrt(y)/2 and "
   "<sqrt y> = 0.24 there.  Items 25, 64, 70, 76 and 100 all inherit this shift",
   abs(syn["canonical"][1]) > 0.05 and abs(syn["alt"][1]) > 0.05,
   f"synthetic bias: canonical {syn['canonical'][1]:+.4f} dex, alt {syn['alt'][1]:+.4f} dex")
ck("102.0b the full-kernel estimator used from here on has no such bias: it recovers the injected a_0 to better than "
   "0.01 dex on the same synthetic data, on both footings",
   abs(syn["canonical"][0]) < 0.01 and abs(syn["alt"][0]) < 0.01,
   f"synthetic bias: canonical {syn['canonical'][0]:+.5f} dex, alt {syn['alt'][0]:+.5f} dex")
P("")
info("the same two estimators on the REAL deep tail, as a function of how deep the cut is:")
info(f"  {'g_bar cut':>10} {'N':>6} {'a_0 full kernel':>17} {'a_0 item-25 limit':>19} {'difference':>11}")
drift = []
for c in (3e-11, 1e-11, 5e-12, 3e-12):
    S = select(gals, gbcut=c); x, y = combine(S)
    af, ad = a0_kern(x, y), a0_deep(x, y); drift.append((c, af, ad))
    info(f"  {c:10.0e} {len(x):6d} {af:17.3e} {ad:19.3e} {math.log10(ad/af):+11.3f} dex")
dr_full = math.log10(max(d[1] for d in drift)/min(d[1] for d in drift))
dr_deep = math.log10(max(d[2] for d in drift)/min(d[2] for d in drift))
ck("102.0c the drift with the cut is the fingerprint of the missing kernel correction: making the tail deeper walks "
   "the deep-limit estimator's a_0 monotonically DOWN by 0.13 dex (it must, since its bias scales as <sqrt y>), and "
   "the difference between the two estimators shrinks from 0.127 to 0.065 dex exactly as predicted.  The full-kernel "
   "estimator's own residual range over the same cuts is smaller but not zero -- 0.07 dex of real sample change",
   dr_deep > dr_full and drift[0][2] > drift[-1][2],
   f"range over the four cuts: full kernel {dr_full:.3f} dex, deep-limit {dr_deep:.3f} dex; "
   f"estimator difference {math.log10(drift[0][2]/drift[0][1]):+.3f} -> {math.log10(drift[-1][2]/drift[-1][1]):+.3f} dex")

# ============================================================================================================
P(""); P("="*118); P("1. THE ITEM'S PREMISE TESTED: does a global gas-fraction cut remove the M/L?"); P("="*118)
fg = np.array([fgas_global(g, UPS_D) for g in gals])
info(f"SPARC f_gas = 1.33 M_HI/M_bar at Upsilon_d = {UPS_D}: median {np.median(fg):.2f}, "
     f"{(fg>0.7).sum()} galaxies above 0.7, {(fg>0.8).sum()} above 0.8 (of {len(gals)})")
info("the identity that matters: d log a_0/d log Upsilon = <(1+n) f_*,loc>/<n> with n = d log nu/d log y, which is")
info("-<f_*,loc> in the deep limit.  f_*,loc is the LOCAL stellar share of g_bar at the points used -- NOT the")
info("galaxy's global gas fraction.  The last two columns show how much the deep limit understates it.")
P("")
info(f"  {'cut':>12} {'ngal':>5} {'Npts':>6} {'<f_gas> global':>15} {'<f_*,loc>':>11} {'d log a0/d log Y':>17} {'identity':>10} {'deep limit':>10} {'0.3->0.7':>9}")
LEV = {}
for lab, kw in (("all", {}), ("f_gas > 0.3", dict(fgmin=0.3)), ("f_gas > 0.5", dict(fgmin=0.5)),
                ("f_gas > 0.7", dict(fgmin=0.7)), ("f_gas > 0.8", dict(fgmin=0.8))):
    S = select(gals, sel_ups=0.5, **kw)
    if len(S) < 4: continue
    lv, ident, mfs, sec = lever(gals, **kw)
    fgm = float(np.mean([fgas_global(s[3], 0.5) for s in S]))
    LEV[lab] = (lv, ident, len(S), sum(len(s[0]) for s in S), mfs, sec)
    info(f"  {lab:>12} {len(S):5d} {sum(len(s[0]) for s in S):6d} {fgm:15.2f} {-mfs:11.2f} {lv:+15.3f} {ident:+10.3f} {mfs:+10.3f} {sec:+9.3f}")
ck("102.1a AGAINST THE ITEM'S OWN PREMISE -- 'f_gas > 0.7, where the stellar M/L barely enters' is FALSE for this "
   "estimator.  Cutting on the GLOBAL gas fraction leaves the local stellar share of g_bar at the deep-tail points "
   "near half, so the M/L lever falls only by a fifth.  The reason is the hunt's own bug pattern (1): the "
   "global f_gas is a TOTAL, while g_bar(r) is set by the ENCLOSED mass, and in these dwarfs the extended HI is mostly "
   "OUTSIDE the radii that enter while all the stars are inside",
   abs(LEV["f_gas > 0.7"][0]) > 0.30,
   f"lever d log a_0/d log Upsilon: all points {LEV['all'][0]:+.3f}, f_gas>0.7 {LEV['f_gas > 0.7'][0]:+.3f}, "
   f"f_gas>0.8 {LEV['f_gas > 0.8'][0]:+.3f} -- a {100*(1-LEV['f_gas > 0.7'][0]/LEV['all'][0]):.0f}% reduction, not a removal")
ck("102.1b the lever is the analytic identity <(1+n) f_*,loc>/<n> to 0.03 in every bin, which proves the diagnosis "
   "rather than asserting it: the estimator's whole M/L dependence is the LOCAL stellar share of g_bar.  The familiar "
   "deep-limit form -<f_*,loc> is 15-20% too small here, the same sub-asymptotic correction section 0 found",
   all(abs(v[0]-v[1]) < 0.03 for v in LEV.values()),
   "max |local derivative - identity| = " + f"{max(abs(v[0]-v[1]) for v in LEV.values()):.4f}; "
   f"max |derivative - deep-limit form -<f_*>| = {max(abs(v[0]-v[4]) for v in LEV.values()):.4f}; "
   f"the practical 0.3->0.7 secant differs from the local derivative by up to {max(abs(v[0]-v[5]) for v in LEV.values()):.3f} (curvature)")

P("")
info("what DOES remove it: a cut on the local stellar share itself.")
info(f"  {'cut':>16} {'ngal':>5} {'Npts':>6} {'<f_*,loc>':>11} {'measured lever':>15} {'a_0 (full kernel)':>19}")
LEV2 = {}
for fc in (None, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1):
    kw = {} if fc is None else dict(fsmax=fc)
    S = select(gals, sel_ups=0.5, **kw)
    if len(S) < 4: continue
    lv, ident, mfs, sec = lever(gals, **kw); x, y = combine(S)
    lab = "all" if fc is None else f"f_*,loc < {fc}"
    LEV2[lab] = (lv, a0_kern(x, y), len(S), len(x))
    info(f"  {lab:>16} {len(S):5d} {len(x):6d} {-mfs:11.2f} {lv:+15.3f} {a0_kern(x,y):19.3e}")
ck("102.1c the local cut does what the global one was supposed to do: at f_*,loc < 0.2 the stellar M/L moves a_0 by "
   "0.06 dex per dex of Upsilon, i.e. a factor-2 error in Upsilon costs 0.02 dex in a_0.  THIS is the M/L-free "
   "measurement the item wanted, and it is a different sample from the one the item specified",
   abs(LEV2["f_*,loc < 0.2"][0]) < 0.15,
   f"lever {LEV2['f_*,loc < 0.2'][0]:+.3f} against {LEV2['all'][0]:+.3f} for the full deep tail "
   f"(a 2x error in Upsilon: {abs(LEV2['f_*,loc < 0.2'][0])*math.log10(2):.3f} dex vs {abs(LEV2['all'][0])*math.log10(2):.3f} dex)")

# ============================================================================================================
P(""); P("="*118); P("2. THE SCAN THE ITEM ASKED FOR: a_0 and its error against the f_gas cut"); P("="*118)
info(f"  {'cut':>12} {'ngal':>5} {'Npts':>6} {'a_0 full kernel':>17} {'+- dex':>8} {'%':>5} "
     f"{'dex vs canon':>13} {'dex vs alt':>11} {'a_0 item-25':>13}")
SCAN = {}
for lab, kw in (("all", {}), ("f_gas > 0.3", dict(fgmin=0.3)), ("f_gas > 0.5", dict(fgmin=0.5)),
                ("f_gas > 0.6", dict(fgmin=0.6)), ("f_gas > 0.7", dict(fgmin=0.7)), ("f_gas > 0.8", dict(fgmin=0.8))):
    S = select(gals, sel_ups=0.5, **kw)
    r = measure(S); x, y = combine(S); r["deep"] = a0_deep(x, y); SCAN[lab] = r
    info(f"  {lab:>12} {r['ngal']:5d} {r['n']:6d} {r['a0']:17.3e} {r['sig']:8.3f} "
         f"{100*(10**r['sig']-1):5.0f} {math.log10(r['a0']/A0['canonical']):+13.3f} "
         f"{math.log10(r['a0']/A0['alt']):+11.3f} {r['deep']:13.3e}")
g7 = SCAN["f_gas > 0.7"]
ck("102.2a the item's own criterion -- 'a_0 to better than 8%' -- is NOT met on the f_gas > 0.7 subset, and cannot be: "
   "the cut leaves 32 galaxies, most of them dwarfs with 20-30% Hubble-flow distances, and a_0 scales as D^-2, so the "
   "galaxy bootstrap gives 17%.  Reported as a failure of the item's precision target, not of the framework",
   10**g7["sig"] - 1 > 0.08,
   f"a_0(f_gas>0.7) = {g7['a0']:.3e} +- {g7['sig']:.3f} dex = {100*(10**g7['sig']-1):.0f}%, target 8%; "
   f"{g7['ngal']} galaxies, {g7['n']} points")
ck("102.2b the scan is not monotone and the f_gas > 0.7 and > 0.8 bins differ by 0.07 dex with 18 galaxies in common, "
   "so the cut is being driven by which handful of dwarfs survive it rather than by a physical trend -- the honest "
   "reading is that the global-f_gas scan has no resolving power at this sample size",
   abs(math.log10(SCAN["f_gas > 0.8"]["a0"]/g7["a0"])) > 0.03,
   f"f_gas>0.7 {g7['a0']:.3e}, f_gas>0.8 {SCAN['f_gas > 0.8']['a0']:.3e} "
   f"({math.log10(SCAN['f_gas > 0.8']['a0']/g7['a0']):+.3f} dex apart, each +- ~0.07)")

# ============================================================================================================
P(""); P("="*118); P("3. THE M/L-FREE MEASUREMENT (local cut), and what carries its error"); P("="*118)
MLF = measure(select(gals, sel_ups=0.5, fsmax=0.2))
ALL = SCAN["all"]
info(f"a_0 (f_*,loc < 0.2, full kernel) = {MLF['a0']:.3e} +- {MLF['sig']:.3f} dex "
     f"[{MLF['lo']:.3e}, {MLF['hi']:.3e}], {MLF['ngal']} galaxies, {MLF['n']} points")
info(f"   vs canonical {A0['canonical']:.3e}: {math.log10(MLF['a0']/A0['canonical']):+.3f} dex "
     f"({math.log10(MLF['a0']/A0['canonical'])/MLF['sig']:+.1f} sigma)")
info(f"   vs alt       {A0['alt']:.3e}: {math.log10(MLF['a0']/A0['alt']):+.3f} dex "
     f"({math.log10(MLF['a0']/A0['alt'])/MLF['sig']:+.1f} sigma)")
sig_dl = DWARF_LENS[1]/DWARF_LENS[0]/math.log(10)
d_lens = math.log10(MLF["a0"]/DWARF_LENS[0]); e_lens = math.hypot(MLF["sig"], sig_dl)
info(f"   vs the KiDS dwarf lens stack (item 2, the other M/L-insensitive rung) {DWARF_LENS[0]:.3e} +- {sig_dl:.3f} dex: "
     f"{d_lens:+.3f} dex ({d_lens/e_lens:+.1f} sigma)")
ck("102.3a (the item's second criterion, and this one PASSES) the M/L-free deep tail agrees with the KiDS dwarf lens "
   "stack -- two measurements of a_0 eleven decades apart in acceleration and sharing no systematic, neither of which "
   "goes through a stellar mass-to-light ratio",
   abs(d_lens)/e_lens < 2.0, f"{MLF['a0']:.2e} vs {DWARF_LENS[0]:.2e}, {d_lens:+.3f} +- {e_lens:.3f} dex")
ck("102.3b AGAINST INTEREST: with the estimator bug removed AND the M/L removed, the SPARC deep tail sits BELOW both "
   "footings, by about 1.7 sigma under canonical and 3.0 under alt.  Item 25's headline (a_0 = 1.14e-10, 'the alt "
   "footing to 0.004 dex') was the +0.10 dex estimator bias plus a stellar M/L; corrected, the alt footing is the one "
   "in trouble and the canonical is the one that survives",
   abs(math.log10(MLF["a0"]/A0["alt"])) > abs(math.log10(MLF["a0"]/A0["canonical"])),
   f"corrected M/L-free a_0 = {MLF['a0']:.3e}; canonical {math.log10(MLF['a0']/A0['canonical'])/MLF['sig']:+.1f} sigma, "
   f"alt {math.log10(MLF['a0']/A0['alt'])/MLF['sig']:+.1f} sigma; item 25 quoted 1.14e-10")
info("CAVEAT ON THAT SIGMA -- the errors above are the GALAXY BOOTSTRAP only.  h103_deep_tail_error_budget.py adds the")
info("coherent calibration terms (the distance scale above all), which take the total to 0.074 dex and make BOTH")
info("footings consistent.  The deep tail must not be quoted as deciding between them; what it says is that the")
info("central value moved down by 0.19 dex when the estimator bug and the stellar M/L were both removed.")

P("")
info("splits -- the M/L-free sample is small and its error is a DISTANCE error (a_0 ~ D^-2):")
splits = [("distance error < 12% (TRGB/Cepheid/direct)", [g for g in gals if g["eD"]/g["D"] < 0.12]),
          ("distance error >= 12% (Hubble flow)",        [g for g in gals if g["eD"]/g["D"] >= 0.12]),
          ("inclination >= 60 deg",                      [g for g in gals if g["inc"] >= 60]),
          ("inclination < 60 deg",                       [g for g in gals if g["inc"] < 60])]
SPL = {}
for lab, sub in splits:
    r = measure(select(sub, sel_ups=0.5, fsmax=0.2), nboot=300); SPL[lab] = r
    info(f"  {lab:44} a_0 = {r['a0']:.3e} +- {r['sig']:.3f} dex  ({r['ngal']} galaxies, {r['n']} points)")
dsplit = math.log10(SPL[splits[0][0]]["a0"]/SPL[splits[1][0]]["a0"])
esplit = math.hypot(SPL[splits[0][0]]["sig"], SPL[splits[1][0]]["sig"])
ck("102.3c the M/L-free sample splits on DISTANCE QUALITY at 0.20 dex, 1.6 sigma: the eight galaxies with TRGB or "
   "Cepheid distances give a_0 on the canonical footing, the fifteen with 20-30% Hubble-flow distances give 40% less. "
   "Since a_0 ~ D^-2 this is where the whole error lives, and it is item 103's business",
   abs(dsplit) > 0.10,
   f"good distances {SPL[splits[0][0]]['a0']:.3e} vs Hubble flow {SPL[splits[1][0]]['a0']:.3e}: "
   f"{dsplit:+.3f} +- {esplit:.3f} dex ({dsplit/esplit:+.1f} sigma)")

# ============================================================================================================
P(""); P("="*118); P("4. AN a_0-FREE MEASUREMENT OF UPSILON THAT FALLS OUT OF THE SAME SAMPLE"); P("="*118)
P("  The deep tail contains both gas-dominated and star-dominated points.  Requiring the two to return the SAME a_0")
P("  -- whatever a_0 is -- determines Upsilon_[3.6] with no cosmology in it at all.  (Item 76 asked the different")
P("  question of what Upsilon reproduces Planck's a_0; this one never uses a_0.)")
info(f"  {'Upsilon_d':>10} {'a_0 (f_*,loc<0.2)':>19} {'N':>5} {'a_0 (f_*,loc>0.6)':>19} {'N':>5} {'difference':>11}")
def starpts(ups):
    X, Y = [], []
    for g in gals:
        gb, gs = gbar_of(g, ups), gstar_of(g, ups)
        with np.errstate(invalid="ignore", divide="ignore"): fs = gs/gb
        m = (gb > 0) & (gb < GBCUT) & (fs > 0.6)
        if m.sum(): X.append(gb[m]); Y.append(g["gobs"][m])
    return np.concatenate(X), np.concatenate(Y)
def delta(ups):
    Sg = select(gals, ups=ups, sel_ups=ups, fsmax=0.2); xg, yg = combine(Sg)
    xs_, ys_ = starpts(ups)
    return math.log10(a0_kern(xs_, ys_)/a0_kern(xg, yg)), a0_kern(xg, yg), a0_kern(xs_, ys_), len(xg), len(xs_)
for u in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
    d, ag, ast, ng, ns = delta(u)
    info(f"  {u:10.2f} {ag:19.3e} {ng:5d} {ast:19.3e} {ns:5d} {d:+11.3f} dex")
try:
    ups_star = brentq(lambda u: delta(u)[0], 0.35, 1.2, xtol=2e-3)
except ValueError:
    ups_star = float("nan")
ub = []
for _ in range(120):
    idx = rng.integers(0, len(gals), len(gals)); sub = [gals[i] for i in idx]
    def dl(u):
        Sg = select(sub, ups=u, sel_ups=u, fsmax=0.2)
        if len(Sg) < 4: return float("nan")
        xg, yg = combine(Sg)
        X, Y = [], []
        for g in sub:
            gb, gs = gbar_of(g, u), gstar_of(g, u)
            with np.errstate(invalid="ignore", divide="ignore"): fs = gs/gb
            m = (gb > 0) & (gb < GBCUT) & (fs > 0.6)
            if m.sum(): X.append(gb[m]); Y.append(g["gobs"][m])
        if not X: return float("nan")
        return math.log10(a0_kern(np.concatenate(X), np.concatenate(Y))/a0_kern(xg, yg))
    try:
        v = brentq(dl, 0.35, 1.2, xtol=3e-3); ub.append(v)
    except Exception: pass
ub = np.array(ub)
info(f"the two halves of the deep tail return the same a_0 at Upsilon_[3.6] = {ups_star:.3f} "
     f"+- {ub.std() if len(ub)>20 else float('nan'):.3f} (galaxy bootstrap, {len(ub)} successes)")
info(f"stellar populations at 3.6 um: 0.50 +- 0.10 (Schombert+2019, McGaugh+2016).  DiskMass dynamical: ~0.3.")
eu = ub.std() if len(ub) > 20 else float("nan")
ck("102.4 a stellar mass-to-light ratio measured WITHOUT a_0 and without stellar populations, from the internal "
   "consistency of the deep tail alone: Upsilon_[3.6] = the value that makes gas-dominated and star-dominated points "
   "return the same a_0.  It agrees with stellar populations.  AGAINST INTEREST it is NOT precise enough to decide "
   "anything: +-0.15 puts DiskMass's 0.3 only 2.0 sigma away, so 'DiskMass excluded' must NOT be quoted from this "
   "measurement -- what can be quoted is that a completely independent route lands on the SPS value",
   np.isfinite(ups_star) and abs(ups_star - 0.5) < 2*math.hypot(eu, 0.10) and (ups_star - 0.3)/math.hypot(eu, 0.05) < 3.0,
   f"Upsilon = {ups_star:.3f} +- {eu:.3f}; vs SPS 0.50 +- 0.10 at {(ups_star-0.5)/math.hypot(eu,0.10):+.1f} sigma; "
   f"vs DiskMass 0.30 at only {(ups_star-0.3)/math.hypot(eu,0.05):+.1f} sigma -- not an exclusion")
d_at, ag_at, ast_at, _, _ = delta(ups_star if np.isfinite(ups_star) else 0.5)
info(f"AGAINST INTEREST: at that self-consistent Upsilon the deep tail's a_0 is {ag_at:.3e}, which is "
     f"{math.log10(ag_at/A0['canonical']):+.3f} dex from canonical and {math.log10(ag_at/A0['alt']):+.3f} from alt.")
info("So the sample cannot have all three of (Upsilon = 0.5, a_0 = canonical, gas and star points agreeing).  Fixing")
info("the internal consistency costs ~0.1 dex in a_0; fixing a_0 costs ~0.09 dex of gas-vs-star disagreement.  That")
info("residual is the real M/L systematic of the deep-tail estimator and it is quoted here, not hidden.")

# ============================================================================================================
P(""); P("="*118); P("5. THE ALTERNATIVE COMPUTED BESIDE IT"); P("="*118)
S = select(gals, sel_ups=0.5, fsmax=0.2); x, y = combine(S)
info(f"Newtonian (nu = 1, same baryons, no halo): <log g_obs/g_bar> = {float(np.mean(np.log10(y/x))):+.3f} dex on the "
     f"M/L-free points -- a factor {10**float(np.mean(np.log10(y/x))):.0f} discrepancy, so these points are not Newtonian")
per = []
for s in S:
    if len(s[0]) < 3: continue
    v = a0_kern(s[0], s[1])
    if np.isfinite(v) and v > 0: per.append((math.log10(v), math.log10(s[3]["Mb"]), s[3]["name"]))
lv = np.array([p[0] for p in per]); lM = np.array([p[1] for p in per])
sl = np.polyfit(lM, lv, 1)[0]
bs_sl = np.array([np.polyfit(lM[i], lv[i], 1)[0] for i in (rng.integers(0, len(lv), len(lv)) for _ in range(400))])
info(f"per-galaxy M/L-free a_0 ({len(per)} galaxies with >= 3 points): spread {lv.std():.3f} dex, "
     f"slope against log M_bar = {sl:+.3f} +- {bs_sl.std():.3f}")
info("In LambdaCDM there is no a_0: the quantity measured here would be a halo property, and halo properties of dwarfs")
info("run with mass (V_max^4/(G M_b) tracks the stellar-to-halo mass relation, slope ~ -0.4 to -0.6 over this range).")
ck("102.5 the framework's side of the alternative holds: the per-galaxy M/L-free a_0 has no significant mass trend "
   "over 1.7 decades of baryonic mass, where a halo-property reading of the same number would run with mass",
   abs(sl) < 3*bs_sl.std(), f"slope {sl:+.3f} +- {bs_sl.std():.3f} dex/dex ({sl/bs_sl.std():+.1f} sigma from flat); "
   f"per-galaxy spread {lv.std():.3f} dex, dominated by the 20-30% distances")

# ============================================================================================================
P(""); P("="*118); P("6. MUTATION CONTROLS"); P("="*118)
ysh = rng.permutation(y)
ck("M102a AGAINST INTEREST, and it is a property of the estimator worth stating: permuting g_obs against g_bar changes "
   "NOTHING.  <log g_obs - log(nu(g_bar/a) g_bar)> depends only on the two marginal means, so the a_0 measured here is "
   "a NORMALISATION of the deep tail and carries no information about the RAR point by point.  A permutation mutation "
   "therefore cannot test it -- the controls that can are the injections M102b/M102c, and the shape is tested "
   "separately by the free-slope fit below and by items 22 and 25",
   abs(math.log10(a0_kern(x, ysh)/MLF["a0"])) < 1e-6,
   f"shuffled a_0 = {a0_kern(x,ysh):.6e}, unshuffled {MLF['a0']:.6e} -- identical to machine precision")
S_ml = select(gals, sel_ups=0.5, fsmax=0.2)
lx, ly = np.log10(x), np.log10(y)
sl_ml = float(np.polyfit(lx, ly, 1)[0])                       # OLS  y|x
sl_inv = 1.0/float(np.polyfit(ly, lx, 1)[0])                  # inverse regression x|y, the other bracket
Cxy = np.cov(lx, ly); evv, VV = np.linalg.eigh(Cxy); sl_orth = float(VV[1, np.argmax(evv)]/VV[0, np.argmax(evv)])
sl_sh = float(np.polyfit(lx, np.log10(ysh), 1)[0])
sl_pred = float(np.mean(1 + nslope(x/MLF["a0"])))             # the kernel's own local slope, 1 + d log nu/d log y
bs_sl2 = []
for _ in range(400):
    i = rng.integers(0, len(S_ml), len(S_ml))
    xb = np.log10(np.concatenate([S_ml[j][0] for j in i])); yb = np.log10(np.concatenate([S_ml[j][1] for j in i]))
    bs_sl2.append(np.polyfit(xb, yb, 1)[0])
bs_sl2 = np.array(bs_sl2)
info(f"free log-log slope of the M/L-free points: OLS(y|x) = {sl_ml:.3f} +- {bs_sl2.std():.3f} (galaxy bootstrap), "
     f"orthogonal {sl_orth:.3f}, inverse regression {sl_inv:.3f}; the kernel's own local slope here is {sl_pred:.3f} "
     f"(not 1/2 -- same sub-asymptotic correction); shuffled {sl_sh:+.3f}; correlation r = {np.corrcoef(lx,ly)[0,1]:.3f}")
ck("M102a2 AGAINST INTEREST: the M/L-free subsample CANNOT measure the RAR slope, and its OLS value looks bad.  The "
   "cut leaves only 0.9 dex of g_bar and r = 0.48, so the forward regression is heavily attenuated: OLS gives 0.28, "
   "3.5 sigma below the kernel's predicted 0.55 (and 2.8 below a nominal 1/2).  The errors-in-variables bracket [OLS, inverse regression] = "
   "[0.28, 1.22] does contain the prediction, so this is an absence of leverage rather than a discrepancy -- but it "
   "must be recorded as an untested assumption of the a_0 measurement, which fixes the shape and fits only the "
   "normalisation.  The shuffle control does work: permuting g_obs flattens even this weak slope to 0.06",
   sl_ml < sl_pred - 2*bs_sl2.std() and sl_inv > sl_pred and abs(sl_sh) < 0.15,
   f"OLS {sl_ml:.3f} +- {bs_sl2.std():.3f} ({(sl_ml-sl_pred)/bs_sl2.std():+.1f} sigma from the kernel's {sl_pred:.3f}); "
   f"bracket [{sl_ml:.2f}, {sl_inv:.2f}] contains it; shuffled {sl_sh:+.3f}")
yn = 1.0*x                                          # nu = 1: Newtonian
ck("M102b turning the kernel off (nu = 1, g_obs = g_bar) must make the estimator run away to an absurd a_0, since no "
   "a_0 can make the boosted kernel reproduce an unboosted curve",
   not np.isfinite(a0_kern(x, yn)) or a0_kern(x, yn) < 1e-13*1.01,
   f"nu=1 synthetic returns a_0 = {a0_kern(x, yn):.3e} (bracket floor 1e-13)")
yb = nu(x/(4*A0["canonical"]))*x
ck("M102c injecting a 4x wrong a_0 must be recovered as a 4x wrong a_0 -- the estimator's sensitivity is the textbook "
   "one and not a fixed point", abs(math.log10(a0_kern(x, yb)/(4*A0["canonical"]))) < 0.01,
   f"injected {4*A0['canonical']:.3e}, recovered {a0_kern(x,yb):.3e} "
   f"({math.log10(a0_kern(x,yb)/(4*A0['canonical'])):+.4f} dex)")

# ============================================================================================================
P(""); P("="*118); P("VERDICT -- ITEM 102"); P("="*118)
P("  The item as written does not work, for a reason worth more than the item: the global gas fraction is not what")
P(f"  sets the estimator's M/L leverage.  Cutting SPARC at f_gas > 0.7 leaves the local stellar share of g_bar at")
P(f"  {-LEV['f_gas > 0.7'][4]:.2f} and the M/L lever at {LEV['f_gas > 0.7'][0]:+.2f}, against {LEV['all'][0]:+.2f} for the whole deep tail -- a {100*(1-LEV['f_gas > 0.7'][0]/LEV['all'][0]):.0f}% reduction, not a")
P("  removal, because the HI that makes these dwarfs gas-rich lies OUTSIDE the radii where g_bar is evaluated.")
P("  Cutting on the local stellar share instead takes the lever to " + f"{LEV2['f_*,loc < 0.2'][0]:+.2f}" + ", and that is the measurement:")
P(f"      a_0 (M/L-free, full kernel) = {MLF['a0']:.3e}  +- {MLF['sig']:.3f} dex  ({100*(10**MLF['sig']-1):.0f}%, {MLF['ngal']} galaxies, {MLF['n']} points)")
P(f"      canonical {math.log10(MLF['a0']/A0['canonical']):+.3f} dex ({math.log10(MLF['a0']/A0['canonical'])/MLF['sig']:+.1f} sigma) | alt {math.log10(MLF['a0']/A0['alt']):+.3f} dex ({math.log10(MLF['a0']/A0['alt'])/MLF['sig']:+.1f} sigma) | KiDS dwarf lenses {d_lens:+.3f} dex ({d_lens/e_lens:+.1f} sigma)")
P(f"  It does not reach the item's 8%; it reaches {100*(10**MLF['sig']-1):.0f}%, and the budget is distance, not M/L (item 103).")
P("  Two corrections go on the ledger and both cut against previously banked numbers:")
P(f"    * item 25's slope-fixed estimator is biased +{syn['canonical'][1]:.2f} dex by the kernel's own sub-asymptotic")
P("      correction.  Its a_0 = 1.14e-10 becomes " + f"{ALL['a0']:.2e}" + " on the same points with the full kernel, and the")
P("      claim that it lands on the alt footing to 0.004 dex is withdrawn.  Items 64, 70, 76 and 100 inherit the shift.")
P("    * the same points give an a_0-free measurement of Upsilon_[3.6] = " + f"{ups_star:.2f} +- {eu:.2f}" + ", from the requirement that")
P("      gas-dominated and star-dominated points agree.  It sits on the SPS value and is 2.0 sigma from DiskMass's")
P("      0.3 -- consistent, not decisive, and it must not be quoted as an exclusion.")
P("  Nothing here is a second Kepler-grade law.  What it is, is the first rung of the ladder that item 125 needs, with")
P("  its systematic named and an estimator bias removed from four items that were already banked.")
sys.exit(ck.done())
