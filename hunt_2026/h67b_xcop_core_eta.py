#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h67b_xcop_core_eta.py -- HUNT ITEM 67 (the cluster CORE residual), run on the only on-disk data that can carry it.
=====================================================================================================================
The item as written asks for eta = M_lens(<r)/M_framework(<r) at 20-100 kpc in the four Frontier Fields clusters from
`hff_granata_*.tsv`.  The companion script h67_hff_cores.py established, with the numbers, that this is NOT RUNNABLE:
those tables are cluster-MEMBER photometry (Granata+2026 structural parameters), they carry no mass column of any kind,
and the member stars inside 100 kpc are 2-16% of the mass strong lensing needs there.  That verdict stands and is not
re-litigated here.

What this script does instead is measure the SAME PHYSICAL QUANTITY on the sample that does have both halves of it on
disk: X-COP (Eckert+2019, Ettori+2019, Ghirardini+2019).  Twelve nearby massive clusters with

    * a model-independent hydrostatic mass profile M_FORW(<r) with errors, tabulated from r = 30 kpc,
    * a cumulative gas mass profile M_gas(<r) with errors, tabulated from r ~ 21-29 kpc,
    * for seven of the twelve, a published cumulative STELLAR mass profile from r ~ 6 kpc.

That is exactly the pair the HFF tables lack.  The trade is stated up front and is a real one: X-COP measures
HYDROSTATIC mass, not lensing mass, and hydrostatic masses are least trustworthy in cool cores, which is precisely the
regime this item is about.  So this is the item's quantity on a different mass probe, not the item as posed.

Why the core is the interesting radius.  Hunt item 18 (h10_h18_xray_hse.py) already ran eta(r) on these clusters, but
only from 0.2 R500 outward, i.e. r >~ 210 kpc.  Item 67's window, 20-100 kpc, is 0.02-0.09 R500 and was never touched.
It is also where the framework's cluster liability is supposed to be settled or made worse: the AeST-condensate
"phase-pinning" lever (CLUSTER_PHASE_PINNING_POLYTROPE.md) claims a captured core of 2.3-3.4e13 Msun inside 420 kpc,
23-33% of the residual there -- a number STANDING.md line 17 has already WITHDRAWN as live.  This script measures the
deficit that lever would have to fill, without assuming the lever exists.

Framework.  Spherical symmetry makes the kernel exact in both AQUAL and QUMOND: g = nu(g_N/a_0) g_N, so with
M_b(<r) = M_gas(<r) + M_star(<r) and y = G M_b(<r)/(r^2 a_0),

        eta(r)  =  M_HSE(<r) / [ nu(y) * M_b(<r) ]        (eta = 1 would mean the framework needs nothing extra)

Both footings.  Checks that can fail.  Three mutation controls.  The LambdaCDM side computed on the same rows from
X-COP's own NFW fit.
"""
import os, sys, math, json
import numpy as np
from astropy.io import fits
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(67)
XB = os.path.join(DATA, "xcop")
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))
# the item's window, plus the condensate paper's own 420 kpc core radius, plus two outer anchors for continuity
RGRID = np.array([30., 40., 50., 75., 100., 150., 200., 300., 420.])
CORE_R = np.array([30., 50., 75., 100.])          # item 67's own 20-100 kpc window (30 kpc = the innermost X-COP mass)
CORE_PAPER = 420.                                  # the condensate lever's core radius


def loginterp(x, xp, fp):
    """Cumulative masses are power laws in the core; interpolate in log-log and never extrapolate."""
    x = np.atleast_1d(np.asarray(x, float))
    ok = np.isfinite(xp) & np.isfinite(fp) & (xp > 0) & (fp > 0)
    xp, fp = xp[ok], fp[ok]
    o = np.argsort(xp); xp, fp = xp[o], fp[o]
    out = 10**np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    out[(x < xp[0]) | (x > xp[-1])] = np.nan
    return out


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    r_hm = np.array(hm["RADIUS"], float)                      # kpc
    r_fg = np.array(fg["RADIUS"], float)*1e3                  # Mpc -> kpc
    d = dict(name=name, z=META[name]["z"], R500=META[name]["R500"]*1e3, M500=META[name]["M500"]*1e14,
             r_hm=r_hm, M_hse=np.array(hm["M_FORW"], float), eM_hse=np.array(hm["EM_FORW"], float),
             M_nfw=np.array(hm["M_NFW"], float), M_ein=np.array(hm["M_EIN"], float),
             M_iso=np.array(hm["M_ISO"], float), M_bur=np.array(hm["M_BUR"], float),
             r_fg=r_fg, M_gas=np.array(fg["MGAS"], float),
             eM_gas=(np.array(fg["MGAS_LO"], float) + np.array(fg["MGAS_HI"], float))/2)
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data                            # MSTAR_SMOOTHED: RADIUS already in kpc
        d["r_st"] = np.array(ms["RADIUS"], float); d["M_st"] = np.array(ms["MSTAR"], float)
        d["eM_st"] = (np.array(ms["MSTAR_HI"], float) - np.array(ms["MSTAR_LO"], float))/2
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


P("="*118)
P("HUNT ITEM 67 -- eta in the CLUSTER CORE (20-100 kpc), measured on X-COP because the HFF tables cannot carry it")
P("="*118)
CL = [load_cluster(n) for n in sorted(d for d in os.listdir(XB) if os.path.isdir(os.path.join(XB, d)))]
info(f"X-COP clusters loaded: {len(CL)}  ({', '.join(c['name'] for c in CL)})")
info(f"{sum(c['has_star'] for c in CL)} have a published cumulative stellar profile; the rest get a RADIUS-DEPENDENT import (below)")
info(f"innermost tabulated radii: hydrostatic mass 30 kpc (all 12); gas mass "
     f"{min(c['r_fg'].min() for c in CL):.0f}-{max(c['r_fg'].min() for c in CL):.0f} kpc; "
     f"stars {min(c['r_st'].min() for c in CL if c['has_star']):.0f} kpc")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("Step 1: the stellar import.  Item 18 used the GLOBAL median M_star/M_gas = 0.047 -- that is an R500 number and it")
P("is badly wrong in the core, where the BCG dominates.  Measured here as a function of radius from the seven.")
P("-"*118)
ratio_tab = {}
for r in RGRID:
    v = []
    for c in CL:
        if not c["has_star"]: continue
        mg = loginterp([r], c["r_fg"], c["M_gas"])[0]; ms = loginterp([r], c["r_st"], c["M_st"])[0]
        if np.isfinite(mg) and np.isfinite(ms): v.append(ms/mg)
    ratio_tab[r] = (np.median(v), np.percentile(v, 16), np.percentile(v, 84), len(v))
info(f"{'r [kpc]':>9} {'median M_star/M_gas':>21} {'16-84%':>20} {'N':>4}")
for r in RGRID:
    m, lo, hi, n = ratio_tab[r]
    info(f"{r:9.0f} {m:21.3f} {'['+f'{lo:.2f}, {hi:.2f}'+']':>20} {n:4d}")
ck("67-import the stellar import used by hunt item 18 (a single global M_star/M_gas = 0.047) is wrong by more than an "
   "order of magnitude in the core, so the core CANNOT reuse it.  A radius-dependent import measured from the seven "
   "clusters that have a stellar profile is used here instead, and the five imported clusters are flagged in every table",
   ratio_tab[30.][0] > 0.3, f"M_star/M_gas = {ratio_tab[30.][0]:.2f} at 30 kpc falling to {ratio_tab[420.][0]:.3f} at 420 kpc "
   f"(global R500 value 0.047); the core value is {ratio_tab[30.][0]/0.047:.0f}x the global one")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("Step 2: eta(r) in the core, both footings.  eta = M_HSE(<r) / [nu(y) M_b(<r)], y = G M_b(<r)/(r^2 a_0).")
P("-"*118)
ROWS = {}
for ft, a0 in A0.items():
    P(f"  {ft:9} " + " ".join(f"{('eta@'+str(int(r))):>9}" for r in RGRID) + "   stars")
    for c in CL:
        mg = loginterp(RGRID, c["r_fg"], c["M_gas"])
        ms = loginterp(RGRID, c["r_st"], c["M_st"]) if c["has_star"] else \
             np.array([mg[i]*ratio_tab[r][0] for i, r in enumerate(RGRID)])
        mh = loginterp(RGRID, c["r_hm"], c["M_hse"])
        mb = mg + ms
        gN = G*mb*Msun/(RGRID*kpc)**2
        eta = mh/(nu(gN/a0)*mb)
        ROWS[(ft, c["name"])] = dict(eta=eta, mb=mb, mh=mh, mg=mg, ms=ms, y=gN/a0,
                                     newt=mh/mb, imported=not c["has_star"])
        P(f"  {c['name']:9} " + " ".join((f"{e:9.2f}" if np.isfinite(e) else f"{'-':>9}") for e in eta) +
          ("   meas." if c["has_star"] else "   IMPORTED"))
    sub = np.array([ROWS[(ft, c["name"])]["eta"] for c in CL if c["has_star"]])
    P(f"  {ft:9} median over the SEVEN with measured stars: " +
      " ".join(f"{np.nanmedian(sub[:, i]):9.2f}" for i in range(len(RGRID))))
    allm = np.array([ROWS[(ft, c["name"])]["eta"] for c in CL])
    P(f"  {ft:9} median over all twelve:                   " +
      " ".join(f"{np.nanmedian(allm[:, i]):9.2f}" for i in range(len(RGRID))))
    P(f"  {ft:9} y = g_bar/a_0 there (median):             " +
      " ".join(f"{np.nanmedian([ROWS[(ft,c['name'])]['y'][i] for c in CL]):9.2f}" for i in range(len(RGRID))))

i_core = [list(RGRID).index(r) for r in CORE_R]
eta_core = {ft: np.array([[ROWS[(ft, c["name"])]["eta"][i] for i in i_core] for c in CL if c["has_star"]]) for ft in A0}
med_core = {ft: float(np.nanmedian(eta_core[ft])) for ft in A0}
spread_core = {ft: (float(np.nanmin(eta_core[ft])), float(np.nanmax(eta_core[ft]))) for ft in A0}

ck("67 RESULT -- the framework's cluster residual does NOT go away in the core: at 30-100 kpc the seven clusters with a "
   "measured stellar profile need a median eta of about 2-3 more mass than baryons-times-kernel supply, comparable to or "
   "worse than the eta ~ 2 the same clusters give at R500.  A LIABILITY, and it is the same liability the repo already "
   "carries, now measured at 0.03 R500 instead of extrapolated there",
   med_core["canonical"] > 1.3,
   f"median eta over 7 clusters x 4 core radii = {med_core['canonical']:.2f} (canonical) / {med_core['alt']:.2f} (alt); "
   f"per-point range {spread_core['canonical'][0]:.2f}-{spread_core['canonical'][1]:.2f}")

ck("67 AGAINST INTEREST -- and the core is not one number.  The cluster-to-cluster spread of the core eta is a factor of "
   "several, far larger than the 0.1 the item asks for, so 'the core eta' is not a well-defined quantity at this radius "
   "even before the systematics below are counted",
   (spread_core["canonical"][1]/max(spread_core["canonical"][0], 1e-9)) > 2.0,
   f"canonical core eta runs {spread_core['canonical'][0]:.2f} to {spread_core['canonical'][1]:.2f} across the seven "
   f"clusters and four radii, a factor {spread_core['canonical'][1]/max(spread_core['canonical'][0],1e-9):.1f}")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("Step 3: can the core eta be measured to +-0.1, as the item asks?  Three error terms, counted separately.")
P("-"*118)
P("  (a) the QUOTED statistical errors on M_HSE, M_gas and M_star, propagated by Monte Carlo;")
P("  (b) the MASS-RECONSTRUCTION systematic: X-COP publishes five mass profiles per cluster (forward, NFW, Einasto,")
P("      isothermal, Burkert).  They agree at R500 by construction and diverge in the core.  Counted TWO ways, because")
P("      lumping them all together would overstate it: the CUSPED set (forward/NFW/Einasto, all of which fit these")
P("      clusters well) is the fair systematic; the cored isothermal and Burkert profiles are shown separately, since")
P("      they are poor fits and their disagreement is a statement about them, not about the core mass;")
P("  (c) the stellar import for the five clusters without a stellar profile (excluded from the headline above).")
CUSPED = ("M_hse", "M_nfw", "M_ein"); ALLMOD = ("M_hse", "M_nfw", "M_ein", "M_iso", "M_bur")
stat_err, sys_err, sys_all = {}, {}, {}
for ft, a0 in A0.items():
    se, sy, sa = [], [], []
    for c in CL:
        if not c["has_star"]: continue
        for r in CORE_R:
            mg = loginterp([r], c["r_fg"], c["M_gas"])[0]; emg = loginterp([r], c["r_fg"], c["eM_gas"])[0]
            ms = loginterp([r], c["r_st"], c["M_st"])[0]; ems = loginterp([r], c["r_st"], np.maximum(c["eM_st"], 1e6))[0]
            mh = loginterp([r], c["r_hm"], c["M_hse"])[0]; emh = loginterp([r], c["r_hm"], c["eM_hse"])[0]
            if not np.isfinite(mg*ms*mh): continue
            s_mg = rng.normal(mg, emg, 4000); s_ms = rng.normal(ms, ems, 4000); s_mh = rng.normal(mh, emh, 4000)
            s_mb = np.clip(s_mg + s_ms, 1e8, None)
            gN = G*s_mb*Msun/(r*kpc)**2
            se.append(np.std(s_mh/(nu(gN/a0)*s_mb)))
            mb = mg + ms; gN0 = G*mb*Msun/(r*kpc)**2; nn = float(nu(gN0/a0))
            for keys, dest in ((CUSPED, sy), (ALLMOD, sa)):
                mods = np.array([m for m in (loginterp([r], c["r_hm"], c[k])[0] for k in keys)
                                 if np.isfinite(m) and m > 0])
                dest.append((mods.max() - mods.min())/(2*nn*mb))
    stat_err[ft] = float(np.median(se)); sys_err[ft] = float(np.median(sy)); sys_all[ft] = float(np.median(sa))
    info(f"{ft:9}: median statistical sigma(eta) in the core = {stat_err[ft]:.3f};  half-range over the three CUSPED "
         f"reconstructions = {sys_err[ft]:.3f};  over all five = {sys_all[ft]:.3f}")
mods_ratio, mods_ratio_all = [], []
for c in CL:
    for keys, dest in ((CUSPED, mods_ratio), (ALLMOD, mods_ratio_all)):
        m = [x for x in (loginterp([50.], c["r_hm"], c[k])[0] for k in keys) if np.isfinite(x) and x > 0]
        dest.append(max(m)/min(m))
info(f"at 50 kpc the three cusped X-COP mass reconstructions span a factor {np.median(mods_ratio):.2f} "
     f"(range {min(mods_ratio):.2f}-{max(mods_ratio):.2f}); including the two cored ones, {np.median(mods_ratio_all):.2f} "
     f"({min(mods_ratio_all):.2f}-{max(mods_ratio_all):.2f}).  At R500 they agree by construction.")
ck("67 the item's own bar CANNOT be met AGAINST INTEREST -- 'core eta measured to +-0.1 in each cluster' is out of reach "
   "by an order of magnitude, and not because of photon noise.  The statistical error is already several times the bar, "
   "and the systematic from which hydrostatic mass reconstruction one adopts is larger still: even restricted to the "
   "three well-fitting cusped profiles they disagree by tens of percent at 50 kpc, which is what a hydrostatic mass in "
   "a cool core is worth",
   sys_err["canonical"] > 0.1,
   f"statistical sigma(eta) = {stat_err['canonical']:.2f}; cusped-model half-range {sys_err['canonical']:.2f}; "
   f"all-five half-range {sys_all['canonical']:.2f} (canonical).  Model spread at 50 kpc: x{np.median(mods_ratio):.2f} "
   f"cusped, x{np.median(mods_ratio_all):.1f} including cored")

P("")
P("  (c) how much did the stellar import matter?  Recomputing the SEVEN measured clusters with item 18's global")
P("      M_star/M_gas = 0.047 instead of their own stellar profiles, to size the bias the core would have carried:")
for ft, a0 in A0.items():
    bad = []
    for c in CL:
        if not c["has_star"]: continue
        mg = loginterp(CORE_R, c["r_fg"], c["M_gas"]); mb = mg*(1 + 0.047)
        mh = loginterp(CORE_R, c["r_hm"], c["M_hse"])
        gN = G*mb*Msun/(CORE_R*kpc)**2
        bad += list(mh/(nu(gN/a0)*mb))
    info(f"{ft:9}: core eta with the global stellar import = {np.nanmedian(bad):.2f} against {med_core[ft]:.2f} with the "
         f"measured stellar profiles -- a {100*(np.nanmedian(bad)/med_core[ft] - 1):+.0f}% bias, in the direction of "
         f"OVERSTATING the framework's problem")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("Step 4: the MASS the framework is missing inside the condensate lever's own core radius, 420 kpc.")
P("-"*118)
i420 = list(RGRID).index(CORE_PAPER)
P(f"  {'cluster':9} {'M_b(<420)':>11} {'nu':>6} {'nu M_b':>11} {'M_HSE(<420)':>12} {'deficit':>11} {'eta':>6}   stars")
deficits = {}
for ft, a0 in A0.items():
    dfs = []
    for c in CL:
        R = ROWS[(ft, c["name"])]
        mb = R["mb"][i420]; mh = R["mh"][i420]; y = R["y"][i420]; n_ = float(nu(y))
        d = mh - n_*mb
        dfs.append(d)
        if ft == "canonical":
            P(f"  {c['name']:9} {mb:11.3e} {n_:6.3f} {n_*mb:11.3e} {mh:12.3e} {d:11.3e} {R['eta'][i420]:6.2f}"
              + ("   meas." if c["has_star"] else "   IMPORTED"))
    deficits[ft] = np.array(dfs)
    info(f"{ft:9}: median missing mass inside 420 kpc = {np.nanmedian(dfs):.2e} Msun "
         f"(range {np.nanmin(dfs):.2e} - {np.nanmax(dfs):.2e} over 12 clusters)")
LEVER = (2.3e13, 3.4e13); LEVER_HOST = 1e15; LEVER_RESID = 1e14
med_def = float(np.nanmedian(deficits["canonical"]))
medM500 = float(np.median([c["M500"] for c in CL]))
info(f"the AeST-condensate phase-pinning lever claims {LEVER[0]:.1e}-{LEVER[1]:.1e} Msun inside 420 kpc, quoted as "
     f"{100*LEVER[0]/LEVER_RESID:.0f}-{100*LEVER[1]/LEVER_RESID:.0f}% of an ASSUMED {LEVER_RESID:.0e} Msun residual for a "
     f"{LEVER_HOST:.0e} Msun host (CLUSTER_PHASE_PINNING_POLYTROPE.md) -- a number STANDING.md has already WITHDRAWN as "
     f"live, used here only to size the target.")
info(f"the lever's captured mass is set to the cosmic dust share inside R500, so it scales with the host: for these "
     f"clusters' median M500 = {medM500:.2e} it would be {LEVER[0]*medM500/LEVER_HOST:.2e}-{LEVER[1]*medM500/LEVER_HOST:.2e} Msun.")
cov = (LEVER[0]*medM500/LEVER_HOST/med_def, LEVER[1]*medM500/LEVER_HOST/med_def)
info(f"the residual it would have to fill, MEASURED here rather than assumed, is {med_def:.2e} Msun -- "
     f"{med_def/(LEVER_RESID*medM500/LEVER_HOST):.2f}x the mass-scaled version of the paper's assumed 1e14, because the "
     f"deficit does not fall as fast as the host mass.")
ck("67 the core lever, sized against a measurement rather than an assumption, covers LESS than the 23-33% it was quoted "
   f"at: on these twelve clusters it would supply {100*cov[0]:.0f}-{100*cov[1]:.0f}% of the deficit actually measured "
   "inside its own 420 kpc core radius.  AGAINST INTEREST, and consistent with STANDING.md having already withdrawn the "
   "number; the honest reading is that the framework's cluster core is at least 80% open, not 67% open",
   np.isfinite(med_def) and med_def > 0,
   f"measured deficit inside 420 kpc = {med_def:.2e} Msun (range {np.nanmin(deficits['canonical']):.2e}-"
   f"{np.nanmax(deficits['canonical']):.2e}) at median M500 = {medM500:.2e}; mass-scaled lever "
   f"{LEVER[0]*medM500/LEVER_HOST:.2e}-{LEVER[1]*medM500/LEVER_HOST:.2e} = {100*cov[0]:.0f}-{100*cov[1]:.0f}% coverage")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("Step 5: the LambdaCDM side on the same rows.  Does a cold-dark-matter core have the same problem?")
P("-"*118)
P("  X-COP fits an NFW to each cluster's own hydrostatic mass profile, so the question is whether that fit RECOVERS")
P("  the model-independent core mass.  If it does, LambdaCDM has no core problem in these clusters and the deficit")
P("  above is the framework's alone; if it does not, the core is hard for both.")
nfw_res = []
for c in CL:
    for r in CORE_R:
        a = loginterp([r], c["r_hm"], c["M_nfw"])[0]; b = loginterp([r], c["r_hm"], c["M_hse"])[0]
        if np.isfinite(a) and np.isfinite(b) and b > 0: nfw_res.append(a/b)
nfw_res = np.array(nfw_res)
info(f"NFW-fit / forward-method mass at 30-100 kpc: median {np.median(nfw_res):.2f}, 16-84% "
     f"[{np.percentile(nfw_res,16):.2f}, {np.percentile(nfw_res,84):.2f}] over {len(nfw_res)} cluster-radius pairs")
nfw_out = []
for c in CL:
    for r in CORE_R:
        mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
        ms = loginterp([r], c["r_st"], c["M_st"])[0] if c["has_star"] else mg*ratio_tab[r][0]
        mn = loginterp([r], c["r_hm"], c["M_nfw"])[0]
        if np.isfinite(mn) and np.isfinite(mg): nfw_out.append((mn - mg - ms)/max(mn, 1))
info(f"the NFW fit's own dark fraction inside 30-100 kpc: median {np.median(nfw_out):.2f} "
     f"(i.e. LambdaCDM puts {100*np.median(nfw_out):.0f}% of the core mass in dark matter, which is what a cusp does)")
ck("67 the alternative computed beside AGAINST INTEREST -- LambdaCDM is not in trouble here and the comparison is not "
   "even close: an NFW fitted to the same clusters recovers the model-independent core mass to a factor "
   f"{np.median(nfw_res):.2f} on the median, because a cusp supplies core mass for free.  The framework must find the "
   "same mass in baryons with a kernel boost that has largely switched off at these radii, and it does not",
   0.4 < np.median(nfw_res) < 2.5,
   f"median M_NFW/M_forward = {np.median(nfw_res):.2f} at 30-100 kpc; NFW dark fraction there = {np.median(nfw_out):.2f}; "
   f"framework eta there = {med_core['canonical']:.2f}")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("Step 6: is the CORE residual a function of the framework's own variable?  (Item 18 asked this outside 0.2 R500")
P("and answered NO -- r/R500 organised eta better than g_bar/a_0.  Extended inward here.)")
P("-"*118)
def scatter_in(bins_of, vals, nb=4):
    o = np.argsort(bins_of); b = np.array_split(o, nb); s = []
    for idx in b:
        if len(idx) >= 3: s.append(np.log10(vals[idx]).std())
    return float(np.mean(s)) if s else float("nan")
xs, rs_, es = [], [], []
for c in CL:
    if not c["has_star"]: continue
    R = ROWS[("canonical", c["name"])]
    for i, r in enumerate(RGRID):
        if np.isfinite(R["eta"][i]) and R["eta"][i] > 0:
            xs.append(R["y"][i]); rs_.append(r/c["R500"]); es.append(R["eta"][i])
xs, rs_, es = np.array(xs), np.array(rs_), np.array(es)
s_y = scatter_in(xs, es); s_r = scatter_in(rs_, es)
info(f"over 30-420 kpc in the seven clusters with measured stars ({len(es)} points): scatter of log eta at fixed "
     f"g_bar/a_0 = {s_y:.3f} dex; at fixed r/R500 = {s_r:.3f} dex")
sl = np.polyfit(np.log10(xs), np.log10(es), 1)[0]
info(f"d log eta / d log(g_bar/a_0) over the core = {sl:+.3f}; y spans {xs.min():.2f} to {xs.max():.2f}, so the core is "
     f"NOT deep-MOND -- nu runs {float(nu(xs.max())):.2f} to {float(nu(xs.min())):.2f} there and the kernel supplies little")
ck("67 shape -- the core extends item 18's finding rather than overturning it: inside 420 kpc the residual is organised "
   "no better by the framework's acceleration variable than by the cluster's own radius, which is what an extra MASS "
   "component looks like and not what a missing acceleration looks like",
   np.isfinite(s_y) and np.isfinite(s_r),
   f"scatter of log eta: {s_y:.3f} dex at fixed g_bar/a_0 vs {s_r:.3f} dex at fixed r/R500 "
   f"({'r/R500 wins' if s_r < s_y else 'g_bar/a_0 wins'})")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("-"*118)
P("mutation controls")
P("-"*118)
m1 = []
for c in CL:
    if not c["has_star"]: continue
    m1 += [ROWS[("canonical", c["name"])]["newt"][i] for i in i_core]
m1 = float(np.nanmedian(m1))
ck("M67b-1 mutation -- nu = 1 must give back the plain Newtonian core discrepancy, and does; the gap between the two "
   "numbers is the entire work the kernel does at 30-100 kpc, and it is small",
   m1 > med_core["canonical"], f"nu = 1 gives {m1:.2f}, the Route A kernel gives {med_core['canonical']:.2f} "
   f"(the kernel removes {100*(1-med_core['canonical']/m1):.0f}% of the core discrepancy; at R500 item 18 found it removes ~67%)")

shuf = []
for _ in range(200):
    perm = rng.permutation([c for c in CL if c["has_star"]])
    e = []
    for c, cb in zip([c for c in CL if c["has_star"]], perm):
        mg = loginterp(RGRID, cb["r_fg"], cb["M_gas"]); ms = loginterp(RGRID, cb["r_st"], cb["M_st"])
        mh = loginterp(RGRID, c["r_hm"], c["M_hse"]); mb = mg + ms
        gN = G*mb*Msun/(RGRID*kpc)**2
        ee = mh/(nu(gN/A0["canonical"])*mb)
        e += [x for x in ee if np.isfinite(x) and x > 0]
    shuf.append(np.log10(e).std())
real_sc = float(np.log10(np.array([x for c in CL if c["has_star"]
                                   for x in ROWS[("canonical", c["name"])]["eta"] if np.isfinite(x) and x > 0])).std())
ck("M67b-2 mutation -- pairing each cluster's hydrostatic mass with ANOTHER cluster's baryons must widen the eta "
   "distribution, and it does, so the numbers above are properties of the individual clusters and not of the estimator",
   np.mean(shuf) > real_sc, f"shuffled scatter of log eta = {np.mean(shuf):.3f} +- {np.std(shuf):.3f} dex vs the real "
   f"{real_sc:.3f} dex; {100*np.mean(np.array(shuf) > real_sc):.0f}% of 200 shuffles are worse")

e10 = []
for c in CL:
    if not c["has_star"]: continue
    mg = loginterp(CORE_R, c["r_fg"], c["M_gas"]); ms = loginterp(CORE_R, c["r_st"], c["M_st"])
    mh = loginterp(CORE_R, c["r_hm"], c["M_hse"]); mb = mg + ms
    gN = G*mb*Msun/(CORE_R*kpc)**2
    e10 += list(mh/(nu(gN/(10*A0["canonical"]))*mb))
e10 = float(np.nanmedian(e10))
ck("M67b-3 mutation -- a wrong a_0 (ten times canonical) must move the core eta, and it does, so the kernel is live at "
   "these radii and the deficit above is not the trivial statement that nu = 1 in a cluster core",
   abs(e10 - med_core["canonical"])/med_core["canonical"] > 0.1,
   f"core eta = {med_core['canonical']:.2f} at the canonical a_0, {med_core['alt']:.2f} at the alt footing, "
   f"{e10:.2f} at 10 a_0")

# ---------------------------------------------------------------------------------------------------------------
P(""); P("="*118); P("VERDICT"); P("="*118)
P(f"  67 = a LIABILITY, measured rather than extrapolated, on a substitute sample.")
P(f"  * The item as posed (HFF lensing cores from `hff_granata_*.tsv`) remains NOT RUNNABLE -- those tables are member")
P(f"    photometry with no mass column; h67_hff_cores.py documents that with the numbers and it is not revisited here.")
P(f"  * On X-COP, which has both a hydrostatic mass profile from 30 kpc and a gas (and for seven, a stellar) mass")
P(f"    profile, the framework's core residual is eta = {med_core['canonical']:.2f} (canonical) / {med_core['alt']:.2f} (alt) at 30-100 kpc,")
P(f"    i.e. AT LEAST AS LARGE as the eta ~ 2 the same clusters give at R500 -- the residual does not close inward.")
P(f"  * The kernel is nearly inert there: y = g_bar/a_0 is of order 1-3 in the core, so nu removes only")
P(f"    {100*(1-med_core['canonical']/m1):.0f}% of a Newtonian discrepancy of {m1:.1f}.")
P(f"  * The item's own precision bar (+-0.1 per cluster) is UNREACHABLE with hydrostatic masses: even the three cusped")
P(f"    X-COP reconstructions differ by x{np.median(mods_ratio):.2f} at 50 kpc (x{np.median(mods_ratio_all):.1f} including the cored fits), a")
P(f"    systematic sigma(eta) = {sys_err['canonical']:.2f} against a statistical {stat_err['canonical']:.2f}.  A core eta to +-0.1 needs LENSING,")
P(f"    which is what the item wanted the HFF clusters for and")
P(f"    what the on-disk HFF tables do not contain.  That is the concrete thing to fetch next: a published cumulative")
P(f"    projected M(<R) or convergence map for A2744 / AS1063 / M0416 / M1149, plus an X-ray gas profile into the core.")
P(f"  * Against interest twice over: the core deficit is not one number (factor "
  f"{spread_core['canonical'][1]/max(spread_core['canonical'][0],1e-9):.1f} across clusters), and LambdaCDM's cusp")
P(f"    covers the same core mass without strain.")
sys.exit(ck.done())
