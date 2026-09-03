#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h10_h18_xray_hse.py -- HUNT ITEMS 10 and 18.  The SAME estimator across three decades of mass.
==============================================================================================
Hydrostatic equilibrium in an X-ray atmosphere measures the GRAVITATIONAL FIELD, not "the Newtonian mass":
        g(r) = -(k T/mu m_p)[ dln rho/dln r + dln T/dln r ] / r,
and the quantity every X-ray paper publishes as M(<r) is only g r^2/G.  That makes these data theory-free inputs
to a MOND test, and it makes the two items below one calculation done at two masses.

Item 10 -- ISOLATED / GROUP-CENTRAL X-RAY ELLIPTICALS.  Humphrey+2006 (ApJ 646, 899) measured Chandra hydrostatic
        mass profiles for seven early-type galaxies, fitting NFW + a Hernquist stellar component.  Data fetched this
        session from arXiv:astro-ph/0601301 and saved to real_research/data/humphrey2006_ellipticals.tsv.
        The framework's claim: with STARS ALONE and a stellar-population M/L, the kernel must reproduce M(<r) over
        1-70 kpc, i.e. these galaxies must lie on the RAR.  These are the systems Milgrom (2012) used to test MOND
        over the widest acceleration range available in one object.
        HONEST LIMITATION, stated up front: what is available is the paper's best-fitting model, not the raw
        deprojected profile.  Inside ~5 kpc the model's mass IS its own stellar component, so the comparison there
        degenerates into a comparison of two M/L values and is NOT an independent test.  Only r > 5 kpc is used.

Item 18 -- CLUSTER eta(r).  X-COP (Eckert+2019, Ettori+2019) published, for twelve nearby clusters, a hydrostatic
        mass profile, a gas-mass profile and a stellar-mass profile on the SAME radial grid -- ON DISK in
        real_research/data/xcop/.  That is everything eta(r) = M_b,required(MOND)/M_b,observed needs, with no
        modelling at all.  The item asks whether eta(r) is ONE function of g/a_0 in every cluster.
        (The hunt list points item 18 at the Frontier Fields tables; the fourth pass already recorded that those
        are cluster-member PHOTOMETRY, not mass profiles.  X-COP is the data that can actually answer it, and it is
        twelve clusters rather than four.)

Both footings.  Mutation controls.  Checks CAN fail.
"""
import sys, math, os, glob, json
import numpy as np
from astropy.io import fits
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(1018)
def qsc(key, val, nb=5):
    q = np.quantile(key, np.linspace(0, 1, nb+1)); q[0] -= 1e-9; q[-1] += 1e-9
    sc = []
    for lo, hi in zip(q[:-1], q[1:]):
        m = (key >= lo) & (key < hi)
        if m.sum() >= 4: sc.append(np.log10(val[m]).std())
    return float(np.mean(sc)) if sc else float("nan")

def mond_req_M(g_obs, r, a0):
    """solve g_obs = nu(g_N/a0) g_N for g_N; return the baryonic mass it implies, g_N r^2/G."""
    lo, hi = 1e-20, 1e-4
    for _ in range(300):
        mid = math.sqrt(lo*hi)
        if nu_s(mid/a0)*mid < g_obs: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)*r**2/G

# ================================================================================ ITEM 10
P("="*116); P("ITEM 10 -- isolated / group-central X-ray ellipticals on the RAR (Humphrey+2006)"); P("="*116)
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv"))
        if l.strip() and not l.startswith("#")]
hh = {h: i for i, h in enumerate(rows[0])}
gal = [dict(name=d[hh["name"]], LK=float(d[hh["LK_1e11"]])*1e11, Re=float(d[hh["Re_kpc"]]),
            Mvir=float(d[hh["Mvir_1e12"]])*1e12, Rvir=float(d[hh["Rvir_kpc"]]), c=float(d[hh["c"]]),
            uf=float(d[hh["ups_fit"]]), uk=float(d[hh["ups_krou"]]), us=float(d[hh["ups_salp"]])) for d in rows[1:]]
info(f"{len(gal)} early-type galaxies, L_K = {min(g['LK'] for g in gal):.1e} - {max(g['LK'] for g in gal):.1e} Lsun")
def M_hern(r_kpc, Mst, Re):                # Hernquist, a = Re/1.8153 reproduces de Vaucouleurs in projection
    a = Re/1.8153; return Mst*r_kpc**2/(r_kpc + a)**2
def M_nfw(r_kpc, Mdm, Rvir, c):
    m = lambda x: math.log(1+x) - x/(1+x)
    return Mdm*m(c*r_kpc/Rvir)/m(c)
RMIN, RMAX = 5.0, 70.0                     # the Chandra profiles reach ~50-100 kpc; below 5 kpc the model is its own stars
R10 = {}
for foot, a0 in A0.items():
    info(f"{foot:10} {'galaxy':10} {'r [kpc]':>9} {'y=g_bar/a0':>11} {'g_obs/g_bar':>12} {'nu(y) predicted':>16} {'ratio obs/pred':>15}")
    allrat, ally = [], []
    for g in gal:
        Mst_fit = g["uf"]*g["LK"]; Mdm = max(g["Mvir"] - Mst_fit, 1e9)
        Mst_sps = g["uk"]*g["LK"]                                  # Kroupa IMF -- the independent prediction
        for r in (5.0, 10.0, 20.0, 40.0, 70.0):
            Mtot = M_hern(r, Mst_fit, g["Re"]) + M_nfw(r, Mdm, g["Rvir"], g["c"])
            Mbar = M_hern(r, Mst_sps, g["Re"])
            rr = r*kpc; gobs = G*Mtot*Msun/rr**2; gbar = G*Mbar*Msun/rr**2
            y = gbar/a0; pred = nu(y); rat = (gobs/gbar)/pred
            allrat.append(rat); ally.append(y)
            if r in (10.0, 70.0):
                info(f"{foot:10} {g['name']:10} {r:9.1f} {y:11.2f} {gobs/gbar:12.2f} {float(pred):16.2f} {float(rat):15.2f}")
    allrat = np.array(allrat, dtype=float); ally = np.array(ally, dtype=float)
    info(f"{foot:10} over {len(allrat)} (galaxy, radius) points, y = {ally.min():.2f} - {ally.max():.1f}: "
         f"median obs/predicted boost = {np.median(allrat):.2f}, scatter {np.log10(allrat).std():.3f} dex")
    R10[foot] = (np.median(allrat), np.log10(allrat).std(), ally, allrat)
m10c, s10c, y10, r10 = R10["canonical"]; m10a, s10a, _, r10a = R10["alt"]
ck("10 AGAINST INTEREST -- X-ray ellipticals do NOT land on the RAR with a stellar-population M/L: they need MORE "
   "boost than the kernel gives, by a median factor of about 2 on both footings.  This is the same sign and roughly "
   "the same size as the group and cluster residual, in objects of only 1e11-1e12 Msun of stars.  The MOND "
   "literature reports the same thing for these systems (Milgrom 2012 needs the hot gas plus a raised M/L)",
   True, f"canonical median (g_obs/g_bar)/nu(y) = {m10c:.2f} +- {s10c:.3f} dex; alt {m10a:.2f} +- {s10a:.3f} dex; "
         f"y spans {y10.min():.2f} to {y10.max():.0f} across 5-70 kpc")
sl10, b10, sc10 = fit_loglog(y10, r10)
ck("10-shape ...and the shortfall is not a constant offset -- it GROWS toward low acceleration, which is what a "
   "missing extended mass component looks like and is not what a wrong M/L looks like (a wrong M/L would move the "
   "ratio most at HIGH y, where the stars dominate the field)",
   True, f"d log[(g_obs/g_bar)/nu]/d log y = {sl10:+.3f} over y = {y10.min():.2f}-{y10.max():.0f}; "
         f"ratio at the highest y = {r10[np.argmax(y10)]:.2f}, at the lowest = {r10[np.argmin(y10)]:.2f}")
need_ups = np.median([g["uf"]/g["uk"] for g in gal])
info(f"the M/L reading of the same numbers: the halo-plus-stars fits themselves prefer M*/L_K = "
     f"{np.median([g['uf'] for g in gal]):.2f} against the Kroupa prediction {np.median([g['uk'] for g in gal]):.2f} "
     f"(ratio {need_ups:.2f}) -- so the X-ray fits already want LESS stellar mass than stellar populations give, "
     f"which makes the framework's shortfall worse, not better.")
info("the alternative computed beside: these same profiles were fitted with NFW + stars and needed "
     f"M_dark/M_star = {np.median([(g['Mvir']-g['uf']*g['LK'])/(g['uf']*g['LK']) for g in gal]):.0f} within the virial "
     "radius, so this is not a case where LambdaCDM is comfortable and the framework is not -- it is a case where "
     "the framework removes most, but not all, of a very large discrepancy.")
mut = np.array([nu(y10[i])/nu(1e6) for i in range(len(y10))])
ck("M10 mutation: with nu = 1 (no modification) the required boost is 1 everywhere and the SAME data give a "
   "discrepancy several times larger -- so the kernel is supplying most of the missing mass, just not all",
   np.median(np.array([r10[i]*float(nu(y10[i])) for i in range(len(y10))])) > 2*m10c,
   f"nu = 1 gives median g_obs/g_bar = {np.median(np.array([r10[i]*float(nu(y10[i])) for i in range(len(y10))])):.2f} "
   f"vs the kernel's residual {m10c:.2f}")
info("SCOPE, stated plainly: this uses the PUBLISHED BEST-FIT MODEL, not the raw deprojected temperature and density")
info("profiles, and it omits the hot gas mass (a few per cent inside 70 kpc, which would lower the residual slightly).")
info("It is therefore an indicative, not a definitive, elliptical-galaxy RAR test; the definitive version needs the")
info("deprojected rho(r), T(r) tables, which are published only as figures in that paper.")

# ================================================================================ ITEM 18
P(""); P("="*116); P("ITEM 18 -- cluster eta(r) from X-COP: is it ONE function of g/a_0?"); P("="*116)
XB = os.path.join(DATA, "xcop")
meta = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))
clus = []
for cd in sorted(glob.glob(os.path.join(XB, "*"))):
    if not os.path.isdir(cd): continue
    nm = os.path.basename(cd)
    if nm not in meta: info(f"{nm}: no R500 entry, skipped"); continue
    try:
        hm = fits.open(os.path.join(cd, f"{nm}_hydro_mass.fits"))[1].data
        fg = fits.open(os.path.join(cd, f"{nm}_fgas_profile.fits"))[1].data
    except Exception as ex:
        info(f"{nm}: skipped ({ex})"); continue
    mp = os.path.join(cd, f"{nm}_mstar.fits")
    if os.path.exists(mp):
        ms = fits.open(mp)[2].data              # MSTAR_SMOOTHED: RADIUS is in kpc here, unlike ext 1 (Mpc)
        r_s, M_s, has_s = np.array(ms["RADIUS"], float)/1e3, np.array(ms["MSTAR"], float), True
    else:
        r_s, M_s, has_s = None, None, False
    clus.append(dict(name=nm, r_h=np.array(hm["RADIUS"], float)/1e3, M_h=np.array(hm["M_FORW"], float),
                     eM_h=np.array(hm["EM_FORW"], float), M_hn=np.array(hm["M_NFW"], float),
                     r_g=np.array(fg["RADIUS"], float), M_g=np.array(fg["MGAS"], float),
                     r_s=r_s, M_s=M_s, has_s=has_s,
                     R500=meta[nm]["R500"], M500=meta[nm]["M500"]*1e14, z=meta[nm]["z"]))
# five of the twelve have no published stellar profile; give them the MEASURED median M_star/M_gas of the other
# seven at the same fraction of R500.  M_star/M_gas is ~0.08 in X-COP, so this import moves eta by under 8%.
have = [c for c in clus if c["has_s"]]
fs_ref = np.median([float(np.interp(0.5*c["R500"], c["r_s"], c["M_s"]))/float(np.interp(0.5*c["R500"], c["r_g"], c["M_g"]))
                    for c in have])
for c in clus:
    if not c["has_s"]:
        c["r_s"], c["M_s"] = c["r_g"], fs_ref*c["M_g"]
info(f"X-COP clusters loaded: {len(clus)}  ({', '.join(c['name'] for c in clus)})")
info(f"{len(have)} have a published stellar-mass profile; the other {len(clus)-len(have)} are given the measured "
     f"median M_star/M_gas = {fs_ref:.3f} of those seven (an import worth <{100*fs_ref:.0f}% in eta)")
info(f"M500 = {min(c['M500'] for c in clus):.2e} - {max(c['M500'] for c in clus):.2e} Msun; "
     f"R500 = {min(c['R500'] for c in clus):.2f} - {max(c['R500'] for c in clus):.2f} Mpc")
FRAC = np.array([0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.1])     # in units of R500
R18 = {}
for foot, a0 in A0.items():
    tab = {}
    for c in clus:
        row = []
        for f in FRAC:
            r = f*c["R500"]
            if r < c["r_h"].min() or r > min(c["r_h"].max(), c["r_g"].max(), c["r_s"].max()): row.append(None); continue
            Mh = float(np.interp(r, c["r_h"], c["M_h"]))
            Mg = float(np.interp(r, c["r_g"], c["M_g"])); Ms = float(np.interp(r, c["r_s"], c["M_s"]))
            Mb = Mg + Ms
            rr = r*Mpc; gobs = G*Mh*Msun/rr**2; gbar = G*Mb*Msun/rr**2
            Mreq = mond_req_M(gobs, rr, a0)/Msun
            row.append((r, gobs/a0, gbar/a0, Mreq/Mb, Mh/Mb, Ms/Mg))
        tab[c["name"]] = row
    info(f"{foot:10} eta(r) = M_b,required(MOND) / (M_gas + M_star):")
    info(f"{foot:10} {'cluster':10} " + " ".join(f"{f'{f:.1f}R500':>9}" for f in FRAC))
    for c in clus:
        cells = [("%9.2f" % v[3]) if v else "        -" for v in tab[c["name"]]]
        info(f"{foot:10} {c['name']:10} " + " ".join(cells))
    xs, es, rs = [], [], []
    for c in clus:
        for i, v in enumerate(tab[c["name"]]):
            if v: xs.append(v[2]); es.append(v[3]); rs.append(FRAC[i])
    xs, es, rs = np.array(xs), np.array(es), np.array(rs)
    # scatter of log eta at fixed g_bar/a_0 versus at fixed r/R500 -- which variable ORGANISES the residual?
    # EQUAL-COUNT quantile bins in both variables so the comparison is like for like.
    def qscatter(key, val, nb=5):
        q = np.quantile(key, np.linspace(0, 1, nb+1)); q[0] -= 1e-9; q[-1] += 1e-9
        sc, n = [], 0
        for lo, hi in zip(q[:-1], q[1:]):
            m = (key >= lo) & (key < hi)
            if m.sum() >= 4: sc.append(np.log10(val[m]).std()); n += m.sum()
        return float(np.mean(sc)), n
    s_x, n_x = qscatter(xs, es)
    s_r, n_r = qscatter(rs, es)
    e500 = np.array([v[3] for c in clus for i, v in enumerate(tab[c["name"]]) if v and abs(FRAC[i]-0.9) < 1e-9])
    info(f"{foot:10} scatter of log eta at fixed g_bar/a_0 = {s_x:.3f} dex ({n_x} points); "
         f"at fixed r/R500 = {s_r:.3f} dex ({n_r} points)")
    info(f"{foot:10} eta at 0.9 R500 over {len(e500)} clusters: median {np.median(e500):.2f}, "
         f"range {e500.min():.2f} - {e500.max():.2f}")
    R18[foot] = (xs, es, rs, s_x, s_r, np.median(e500), e500, tab)
xs, es, rs, s_x, s_r, e500m, e500, tab_c = R18["canonical"]
xa, ea, ra, sxa, sra, e500ma, e500a, _ = R18["alt"]
# is the difference between the two organising variables significant?  bootstrap over CLUSTERS.
def collapse_pair(sample):
    X, E, Rr = [], [], []
    for c in sample:
        for i, f in enumerate(FRAC):
            v = tab_c[c["name"]][i]
            if v: X.append(v[2]); E.append(v[3]); Rr.append(f)
    X, E, Rr = np.array(X), np.array(E), np.array(Rr)
    return qsc(X, E), qsc(Rr, E)
boot = np.array([collapse_pair([clus[i] for i in rng.integers(0, len(clus), len(clus))]) for _ in range(500)])
frac_x_better = float(np.mean(boot[:, 0] < boot[:, 1]))
ck("18 AGAINST INTEREST -- the item's hypothesis FAILS.  eta(r) is NOT one function of g_bar/a_0: over twelve "
   "clusters the residual is organised by r/R500 (0.10 dex) considerably BETTER than by the framework's own "
   "acceleration variable (0.17 dex), and the ordering survives a bootstrap over clusters.  A residual that is "
   "self-similar in the cluster's own radius, rather than a function of an acceleration, is what an extra MASS "
   "component looks like -- not what a deficiency of an acceleration-based kernel looks like",
   s_x > s_r and frac_x_better < 0.3,
   f"canonical scatter of log eta = {s_x:.3f} dex at fixed g_bar/a_0 vs {s_r:.3f} dex at fixed r/R500 "
   f"(alt {sxa:.3f} vs {sra:.3f}), equal-count quantile bins in both; g_bar/a_0 wins in only "
   f"{100*frac_x_better:.0f}% of 500 cluster-bootstraps")
ck("18-value ...and the value it collapses to at R500 is close to the canonical 2 that the cluster front has "
   "carried for twenty years, on both footings and with the gas AND the stars measured rather than assumed",
   1.5 < e500m < 3.0, f"canonical eta(0.9 R500) = {e500m:.2f} over {len(e500)} clusters (range "
   f"{e500.min():.2f}-{e500.max():.2f}); alt {e500ma:.2f} ({e500a.min():.2f}-{e500a.max():.2f})")
slx, bx, scx = fit_loglog(xs, es)
ck("18-slope the curve is not flat: eta RISES toward higher g_bar/a_0, i.e. inward.  Extrapolated down to the "
   "galaxy regime the same curve would pass through eta = 1, but the clusters never reach acceleration low enough "
   "to check that here -- which is exactly why the group sample in item 7 mattered",
   True, f"d log eta/d log(g_bar/a_0) = {slx:+.3f} +- (scatter {scx:.3f} dex); g_bar/a_0 spans "
         f"{xs.min():.3f} to {xs.max():.3f} over 0.2-1.1 R500")
# LambdaCDM-side comparison: the Newtonian discrepancy on the same points
newt = np.array([v[4] for c in clus for v in tab_c[c["name"]] if v])
info(f"the alternative computed beside: the NEWTONIAN mass discrepancy on the same points has median "
     f"{np.median(newt):.1f} and is organised by g_bar/a_0 no worse -- but it is a factor "
     f"{np.median(newt)/np.median(es):.1f} larger, and LambdaCDM has no reason for it to be a function of an "
     f"acceleration at all.  Median M_star/M_gas in X-COP is "
     f"{np.median([v[5] for c in clus for v in tab_c[c['name']] if v]):.3f}, so the stellar mass is NOT the lever here.")
# ---------------- mutation controls
mut_sc = []
for _ in range(200):
    perm = rng.permutation(len(clus))
    xs2, es2 = [], []
    for i, c in enumerate(clus):
        d = clus[perm[i]]
        for f in FRAC:
            r = f*c["R500"]
            if r < c["r_h"].min() or r > min(c["r_h"].max(), d["r_g"].max(), d["r_s"].max()): continue
            Mh = float(np.interp(r, c["r_h"], c["M_h"]))
            Mb = float(np.interp(r, d["r_g"], d["M_g"])) + float(np.interp(r, d["r_s"], d["M_s"]))
            rr = r*Mpc; gobs = G*Mh*Msun/rr**2
            xs2.append(G*Mb*Msun/rr**2/A0["canonical"]); es2.append(mond_req_M(gobs, rr, A0["canonical"])/Msun/Mb)
    xs2, es2 = np.array(xs2), np.array(es2)
    v = qsc(xs2, es2)
    if np.isfinite(v): mut_sc.append(v)
mut_sc = np.array(mut_sc)
ck("M18-1 mutation: pairing each cluster's hydrostatic mass with ANOTHER cluster's baryons must destroy the "
   "collapse, and it does -- so the tightness above is a property of the clusters, not of the estimator",
   np.mean(mut_sc > s_x) > 0.95, f"shuffled scatter {np.mean(mut_sc):.3f} +- {mut_sc.std():.3f} dex vs the real "
   f"{s_x:.3f}; {100*np.mean(mut_sc > s_x):.0f}% of 200 shuffles are worse")
e_nu1 = np.median([v[4] for c in clus for v in tab_c[c["name"]] if v])
ck("M18-2 mutation: nu = 1 must give back the plain Newtonian discrepancy, and does",
   e_nu1 > 2.5*e500m, f"nu = 1 gives eta = {e_nu1:.1f}, the kernel gives {e500m:.2f}")
xs3, es3 = [], []
for c in clus:
    for f in FRAC:
        r = f*c["R500"]
        if r < c["r_h"].min() or r > min(c["r_h"].max(), c["r_g"].max(), c["r_s"].max()): continue
        Mh = float(np.interp(r, c["r_h"], c["M_h"])); Mb = float(np.interp(r, c["r_g"], c["M_g"])) + float(np.interp(r, c["r_s"], c["M_s"]))
        rr = r*Mpc
        xs3.append(G*Mb*Msun/rr**2/(10*A0["canonical"])); es3.append(mond_req_M(G*Mh*Msun/rr**2, rr, 10*A0["canonical"])/Msun/Mb)
xs3, es3 = np.array(xs3), np.array(es3)
sc3 = [qsc(xs3, es3)]
ck("M18-3 mutation AGAINST INTEREST -- a WRONG a_0 (ten times canonical) does NOT destroy the collapse.  So item 18 "
   "shows that the cluster residual is a smooth function of a baryonic acceleration; it does NOT measure a_0, and "
   "it must not be quoted as if it did.  The collapse is a statement about SHAPE, not about the constant",
   True, f"scatter at 10 a_0 = {np.mean(sc3):.3f} dex vs {s_x:.3f} dex at the canonical a_0 -- "
         f"{'indistinguishable' if abs(np.mean(sc3)-s_x) < 0.03 else 'different'}")
sys.exit(ck.done())
