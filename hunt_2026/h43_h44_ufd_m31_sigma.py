#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h43_h44_ufd_m31_sigma.py -- HUNT ITEMS 43 and 44: the satellite sigma(M_b, D_host) law, on the ultra-faint dwarfs and on the
                            M31 satellite system.
==================================================================================================================================
Item 43 (UFDs): a pressure-supported satellite has, in the framework, a velocity dispersion fixed by TWO measured numbers -- its
        baryonic mass and its distance from its host -- with a_0 the only constant and Upsilon_V the only nuisance.  If that
        three-variable law holds with RAR-class scatter over the ultra-faints (M_V > -7.7, L_V < 1e5 Lsun, the faintest galaxies
        known) it is a second Kepler-grade regularity.  ULTRA-FAINT sample = the Local Volume Database (Pace 2024), which is the
        maintained superset of the Simon 2019 ARA&A table named in the hunt list.
Item 44 (M31): the same law with M31's external field instead of the Milky Way's.  Primary sample = Collins+2013 (the source named
        in the hunt list, VizieR J/ApJ/768/172); cross-check sample = the LVD M31 satellites.

WHAT IS NEW HERE RELATIVE TO ITEM 8 (h8_h42_h96_dwarfs.py) -- and it matters:
    h8 predicted the EFE-suppressed dispersion with  G_eff = nu(g_ext_TRUE/a_0) G.  That is wrong twice over:
      (i) in QUMOND the interpolation function nu takes the NEWTONIAN field as its argument, not the true (already-modified) one;
     (ii) the leading EFE term is not nu(y_e) but nu(y_e)*(1 + dln(nu)/dln(y)|_{y_e}), which in the deep-MOND regime is HALF of
          nu(y_e) -- this is exactly the "the simple nu(x_ext) prescription over-predicts by ~2x" warning recorded in h8.
    This script uses instead the published one-dimensional QUMOND EFE formula, Famaey & McGaugh 2012 eq. 60, in the form used by
    Lelli et al. 2015 (A&A 584, A113) for tidal dwarfs:
          a_int = g_Ni * nu((g_Ni+g_Ne)/a0)  +  g_Ne * [ nu((g_Ni+g_Ne)/a0) - nu(g_Ne/a0) ]
    with g_Ni = G M_half / r_h^2 the internal NEWTONIAN field and g_Ne = G M_host,bar / D_host^2 the external NEWTONIAN field.
    Route A, nu(y) = 1/(1-exp(-sqrt(y))), IS the n=1 member of the McGaugh 2008 family that Lelli+2015 used, so this script's
    kernel and that published EFE calculation are the same function -- which is what makes the item-46 replication possible.
    Dispersion estimator (Wolf et al. 2010, generalised to modified gravity):  sigma^2 = a_int(r_h) * r_h / 3,  r_h = 4/3 R_e,circ.
    Both a_0 footings.  Checks CAN fail.  Mutation controls at the end.
"""
import sys, math, csv
import numpy as np
from hunt_lib import *
ck = Check()

# ---------------------------------------------------------------------------------------------------------------- the estimator
MW_MB, M31_MB = 6.0e10, 1.2e11          # baryonic masses of the hosts, Msun (McGaugh 2016; the same values h8 used)
UPS_V = 2.0                             # stellar M/L in V for an old population -- the ONE nuisance, scanned later

def a_int(gNi, gNe, a0):
    """QUMOND one-dimensional external-field formula (Famaey & McGaugh 2012 eq. 60; Lelli+2015 eq. 8).
    gNe = 0 gives the isolated case a = nu(g_N/a0) g_N."""
    nt = nu_s((gNi + gNe)/a0)
    ne = nu_s(gNe/a0) if gNe > 0 else 0.0
    return gNi*nt + gNe*(nt - ne)

def sigma_pred(Mb_Msun, rh_pc, D_host_kpc, M_host, a0, efe=True, nu_arg_true=False):
    """sigma_los in km/s.  Mb = TOTAL baryonic mass; half of it sits inside r_h (mass follows light).
    nu_arg_true=True reproduces the h8 prescription (nu evaluated at the TRUE external field, no (1+L) factor)."""
    Mh = 0.5*Mb_Msun*Msun
    rh = rh_pc*3.0857e16
    gNi = G*Mh/rh**2
    if not efe or M_host is None or D_host_kpc is None or D_host_kpc <= 0:
        return math.sqrt(a_int(gNi, 0.0, a0)*rh/3.0)/1e3, gNi, 0.0
    gNe = G*M_host*Msun/(D_host_kpc*kpc)**2
    if nu_arg_true:                                          # <- the h8 recipe, kept only so the difference can be quoted
        g_true = math.sqrt(G*M_host*Msun*a0)/(D_host_kpc*kpc)
        return math.sqrt(nu_s(g_true/a0)*G*Mh/(3*rh))/1e3, gNi, gNe
    return math.sqrt(a_int(gNi, gNe, a0)*rh/3.0)/1e3, gNi, gNe

def sigma_newt(Mb_Msun, rh_pc):
    return math.sqrt(G*(0.5*Mb_Msun*Msun)/(3*rh_pc*3.0857e16))/1e3

P("="*128); P("0. the estimator, validated against the two analytic limits BEFORE any data is touched"); P("="*128)
# isolated deep-MOND limit must reproduce sigma^4 = (4/81) G M_b a_0
tst = []
for Mb in (1e4, 1e6, 1e8):
    for rh in (30.0, 300.0, 3000.0):
        s = sigma_pred(Mb, rh, None, None, A0["canonical"], efe=False)[0]
        s_an = ((4/81)*G*Mb*Msun*A0["canonical"])**0.25/1e3
        gN = G*(0.5*Mb*Msun)/(rh*3.0857e16)**2
        if gN/A0["canonical"] < 0.02: tst.append(s/s_an)      # only where the deep-MOND limit actually applies
tst = np.array(tst)
info(f"isolated deep-MOND check: sigma(estimator)/sigma((4/81 G M a0)^1/4) = {tst.mean():.4f} +- {tst.std():.4f} over {len(tst)} (M_b, r_h) pairs")
ck("V1 estimator validation -- in the isolated deep-MOND limit the Wolf-style estimator sigma^2 = a(r_h) r_h/3 reproduces the exact "
   "MOND relation sigma^4 = (4/81) G M_b a_0 to better than 10%",
   abs(tst.mean() - 1.0) < 0.10 and tst.std() < 0.02, f"ratio {tst.mean():.4f} +- {tst.std():.4f}")
# EFE-dominated limit: the effective G must be nu(y_e)(1+L_e) ~ nu(y_e)/2, i.e. HALF the naive nu(y_e) G
ratios = []
for ye in (0.003, 0.01, 0.03, 0.1):
    gNe = ye*A0["canonical"]; gNi = 1e-6*gNe
    Geff = a_int(gNi, gNe, A0["canonical"])/gNi
    ratios.append(Geff/nu_s(ye))
ratios = np.array(ratios)
info(f"EFE-dominated limit: G_eff/[nu(y_e) G] = {ratios.min():.3f} - {ratios.max():.3f} over y_e = 0.003-0.1 (deep-MOND value 1/2)")
ck("V2 estimator validation -- the correct EFE-dominated effective G is nu(y_e)(1+dln nu/dln y) ~ nu(y_e)/2, i.e. the naive "
   "G_eff = nu(y_ext) G over-predicts the EFE-suppressed acceleration by a factor 2.  This is the h8 warning, now derived",
   0.45 < ratios.min() and ratios.max() < 0.60, f"ratio range {ratios.min():.3f}-{ratios.max():.3f}, deep-MOND asymptote 0.500")

# ---------------------------------------------------------------------------------------------------------------------- the data
def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None

def load_lvd(fname, host_mb, host_name):
    rows = list(csv.DictReader(open(os.path.join(DATA, "dsph", fname))))
    out = []
    for r in rows:
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
        rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or Dh is None or sig <= 0: continue
        em = fnum(r["vlos_sigma_em"]) or 0.2*sig; ep = fnum(r["vlos_sigma_ep"]) or 0.2*sig
        MHI = fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, LV=10**(0.4*(4.83 - MV)), rh=rh, D=Dh, sig=sig,
                        esig=0.5*(em + ep), MHI=(10**MHI if MHI is not None else 0.0),
                        host_mb=host_mb, host=host_name, src="LVD"))
    return out

mw  = load_lvd("lvd_dwarf_mw.csv",  MW_MB,  "MW")
m31 = load_lvd("lvd_dwarf_m31.csv", M31_MB, "M31")

def load_lvd_field():
    """The isolated Local-Group dwarfs: an EFE-FREE control on the same estimator and the same catalogue."""
    rows = list(csv.DictReader(open(os.path.join(DATA, "dsph", "lvd_dwarf_local_field.csv"))))
    out = []
    for r in rows:
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
        rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0: continue
        em = fnum(r["vlos_sigma_em"]) or 0.2*sig; ep = fnum(r["vlos_sigma_ep"]) or 0.2*sig
        MHI = fnum(r["mass_HI"]); Dgc = fnum(r["distance_gc"]); Dm31 = fnum(r["distance_m31"])
        out.append(dict(name=r["name"], MV=MV, LV=10**(0.4*(4.83 - MV)), rh=rh, D=None, sig=sig,
                        esig=0.5*(em + ep), MHI=(10**MHI if MHI is not None else 0.0),
                        host_mb=None, host="field", src="LVD", Dgc=Dgc, Dm31=Dm31))
    return out
fld = load_lvd_field()

# Collins+2013, the source the hunt list names for item 44
col = []
for line in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv"), encoding="latin-1"):
    if line.startswith("#") or not line.strip(): continue
    f = line.split("\t")
    if len(f) < 25 or not f[0].strip().isdigit(): continue
    try:
        MV = float(f[7]); rh = float(f[8]); Dist = float(f[11]); sig = float(f[18]); Esig = float(f[19]); esig = float(f[21])
    except ValueError: continue
    if sig <= 0: continue                                    # sigV = 0.0 rows are unresolved dispersions = upper limits
    col.append(dict(name=f[1].strip(), MV=MV, LV=10**(0.4*(4.83 - MV)), rh=rh, D=None, D_helio=Dist, sig=sig,
                    esig=0.5*(Esig + esig), MHI=0.0, host_mb=M31_MB, host="M31", src="Collins13",
                    ra=f[5].strip(), dec=f[6].strip()))
# M31-centric distance for the Collins dwarfs: 3-D separation from M31 (RA 00 42 44.3, Dec +41 16 09, D = 785 kpc)
def sph2cart(ra_hms, dec_dms, d):
    h, m, s = [float(x) for x in ra_hms.split()]; ra = (h + m/60 + s/3600)*15.0
    sgn = -1.0 if dec_dms.strip().startswith("-") else 1.0
    dd, dm, ds = [abs(float(x)) for x in dec_dms.replace("+", "").replace("-", "").split()]
    dec = sgn*(dd + dm/60 + ds/3600)
    ra, dec = math.radians(ra), math.radians(dec)
    return np.array([d*math.cos(dec)*math.cos(ra), d*math.cos(dec)*math.sin(ra), d*math.sin(dec)])
M31_XYZ = sph2cart("00 42 44.3", "+41 16 09", 785.0)
for d in col:
    d["D"] = float(np.linalg.norm(sph2cart(d["ra"], d["dec"], d["D_helio"]) - M31_XYZ))

UFD_CUT = -7.7                                               # Simon 2019's ultra-faint boundary, L_V < 1e5 Lsun
ufd = [d for d in mw if d["MV"] > UFD_CUT]
cls = [d for d in mw if d["MV"] <= UFD_CUT]
P(""); P("="*128); P("1. the samples"); P("="*128)
info(f"LVD Milky Way satellites with a measured (not upper-limit) dispersion: {len(mw)}  ->  {len(ufd)} ULTRA-FAINT (M_V > {UFD_CUT}) "
     f"+ {len(cls)} classical;   M_V range {min(d['MV'] for d in mw):+.1f} to {max(d['MV'] for d in mw):+.1f}")
info(f"LVD M31 satellites with a measured dispersion: {len(m31)};   Collins+2013 (item 44's named source): {len(col)} of 18 rows "
     f"({18-len(col)} carry sigV = 0.0, i.e. an unresolved dispersion, and are excluded as upper limits)")
info(f"D_host range: MW {min(d['D'] for d in mw):.0f}-{max(d['D'] for d in mw):.0f} kpc; "
     f"M31(LVD) {min(d['D'] for d in m31):.0f}-{max(d['D'] for d in m31):.0f} kpc; "
     f"M31(Collins, 3-D from RA/Dec/D) {min(d['D'] for d in col):.0f}-{max(d['D'] for d in col):.0f} kpc")
# how EFE-free the isolated control really is -- computed, not asserted
fx = []
for d in fld:
    gNe = G*MW_MB*Msun/(d["Dgc"]*kpc)**2 + G*M31_MB*Msun/(d["Dm31"]*kpc)**2
    gNi = G*(0.5*UPS_V*d["LV"]*Msun)/((4.0/3.0)*d["rh"]*3.0857e16)**2
    fx.append(gNe/gNi)
info(f"LVD isolated local-field dwarfs with a measured dispersion: {len(fld)}.  Their combined MW+M31 external Newtonian field is "
     f"{100*min(fx):.2f}%-{100*max(fx):.2f}% of their own internal one (median {100*np.median(fx):.2f}%), so they are an EFE-FREE "
     f"control: any failure there is a failure of the isolated law, not of the external-field term.")

def resid(sample, a0, ups=UPS_V, efe=True, nu_arg_true=False, newt=False):
    out = []
    for d in sample:
        Mb = ups*d["LV"] + 1.33*d["MHI"]
        rh = (4.0/3.0)*d["rh"]                               # 3-D half-light radius from the projected one
        sp = sigma_newt(Mb, rh) if newt else sigma_pred(Mb, rh, d["D"], d["host_mb"], a0, efe, nu_arg_true)[0]
        out.append(math.log10(d["sig"]/sp))
    return np.array(out)

def line(tag, sample, a0):
    r_efe = resid(sample, a0); r_iso = resid(sample, a0, efe=False); r_N = resid(sample, a0, newt=True)
    r_h8 = resid(sample, a0, nu_arg_true=True)
    info(f"{tag:34} N={len(sample):3d}  median log10(sigma_obs/sigma_pred):  EFE {np.median(r_efe):+.3f} (rms {r_efe.std():.3f})"
         f" | isolated {np.median(r_iso):+.3f} | Newtonian {np.median(r_N):+.3f} | [h8 recipe {np.median(r_h8):+.3f}]")
    return r_efe

P(""); P("="*128); P("2. ITEM 43 -- the ultra-faints, and the Milky Way satellites as a whole"); P("="*128)
res = {}
for foot, a0 in A0.items():
    P(f"  --- {foot} a_0 = {a0:.3e} m/s^2, Upsilon_V = {UPS_V} ---")
    res[(foot, "ufd")] = line("MW ultra-faint (M_V > -7.7)", ufd, a0)
    res[(foot, "cls")] = line("MW classical dSph", cls, a0)
    res[(foot, "mw")]  = line("MW all", mw, a0)

def centring_ups(sample, a0):
    grid = np.geomspace(0.2, 200.0, 240)
    sc = sorted((abs(np.median(resid(sample, a0, u))), u, resid(sample, a0, u).std()) for u in grid)
    return sc[0][1], sc[0][2]
cu = {}
for foot, a0 in A0.items():
    for tag, s in (("ufd", ufd), ("cls", cls), ("mw", mw)):
        cu[(foot, tag)] = centring_ups(s, a0)
    info(f"{foot:10} Upsilon_V that centres the EFE law:  ultra-faints {cu[(foot,'ufd')][0]:7.1f} (scatter {cu[(foot,'ufd')][1]:.3f} dex)"
         f" | classical {cu[(foot,'cls')][0]:6.1f} (scatter {cu[(foot,'cls')][1]:.3f})"
         f" | all MW {cu[(foot,'mw')][0]:6.1f} (scatter {cu[(foot,'mw')][1]:.3f})")

ck("43a AGAINST INTEREST -- the ultra-faint sigma(M_b, D_host) law is NOT Kepler-grade and NOT even close: at a stellar-population "
   "Upsilon_V = 2 the measured dispersions sit far ABOVE the framework's EFE prediction, and centring the relation needs a stellar "
   "mass-to-light ratio of order 10-100, i.e. the ultra-faints are as anomalous for this framework as they are for Newton.  This "
   "reproduces (does not discover) the long-standing MOND problem with the faintest MW satellites (Angus 2008; McGaugh & Wolf 2010)",
   all(cu[(f, "ufd")][0] > 5.0 for f in A0),
   "; ".join(f"{f}: median offset {np.median(res[(f,'ufd')]):+.3f} dex at Ups=2, centring Ups_V = {cu[(f,'ufd')][0]:.1f}" for f in A0))
ck("43b the Kepler-grade scatter test (the actual promotion criterion: <= 0.1 dex in sigma with a_0 the only constant) FAILS by a "
   "factor 3-4 even after the mass-to-light ratio is tuned away, so the item cannot be promoted on ANY choice of Upsilon_V",
   all(cu[(f, "ufd")][1] > 0.10 for f in A0),
   "; ".join(f"{f}: best-case scatter {cu[(f,'ufd')][1]:.3f} dex (need <= 0.100)" for f in A0))
ck("43c the classical dSphs are much closer to the law than the ultra-faints -- the failure is luminosity-dependent, which is the "
   "signature of a sample problem (binaries, tides, tiny N_star) rather than of the acceleration law itself; reported as a "
   "reason NOT to book 43 as a clean kill of the framework either",
   all(cu[(f, "cls")][0] < cu[(f, "ufd")][0] for f in A0),
   "; ".join(f"{f}: classical centring Ups = {cu[(f,'cls')][0]:.1f} vs ultra-faint {cu[(f,'ufd')][0]:.1f}" for f in A0))

# does the residual know about the distance?  If the EFE term is right, it must not.  But log(D_host) and M_V are themselves
# correlated in a magnitude-limited satellite census, so the raw correlation is reported AND the M_V-controlled one.
def ols_t(y, X):
    """multiple regression y = X b (X already has a constant column); returns b and the t of every coefficient."""
    n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b; s2 = (r @ r)/max(n - k, 1)
    C = s2*np.linalg.pinv(X.T @ X)
    return b, b/np.sqrt(np.maximum(np.diag(C), 1e-300))
P("")
dcorr = {}
for foot, a0 in A0.items():
    for tag, s in (("MW ultra-faint", ufd), ("MW classical", cls), ("MW all", mw), ("M31 LVD", m31)):
        r = resid(s, a0, cu[(foot, "mw")][0]); x = np.log10([d["D"] for d in s]); mv = np.array([d["MV"] for d in s])
        rho = float(np.corrcoef(x, r)[0, 1]); n = len(s)
        t = rho*math.sqrt(max(n-2, 1)/max(1-rho**2, 1e-9))
        b, tt = ols_t(r, np.vstack([x, mv, np.ones(n)]).T)
        raw = float(np.polyfit(x, r, 1)[0])
        info(f"{foot:10} {tag:16} residual vs log D_host: slope {raw:+.3f}, r = {rho:+.3f} (t = {t:+.2f}, N = {n})"
             f"   |   controlling for M_V: slope {b[0]:+.3f} (t = {tt[0]:+.2f}); corr(log D, M_V) = {np.corrcoef(x, mv)[0,1]:+.3f}")
        dcorr[(foot, tag)] = (raw, t, b[0], tt[0])
ck("43d AGAINST INTEREST -- the external-field term is the one piece of the law this sample can test on its OWN, and it FAILS: "
   "the residual knows the host distance.  The sign says the framework gives distant satellites too much boost relative to close "
   "ones, i.e. the external-field suppression is too strong at small D (or the close satellites are tidally heated).  Part of the "
   "raw trend is the magnitude-limited census -- log D and M_V are correlated -- but it SURVIVES controlling for M_V at 3.0 sigma "
   "over all 45 MW satellites, on both footings (section 2b below shows the rank-based version of the same test is 2.0-2.5 sigma, "
   "which is the number that should be quoted).  M31, whose satellites span a wider distance range, shows no such trend.  "
   "The check asserts the FAILURE, in the house convention: it passes because the trend is real and significant",
   abs(dcorr[("canonical", "MW all")][3]) > 2.5 and abs(dcorr[("alt", "MW all")][3]) > 2.5,
   f"canonical ultra-faints: raw slope {dcorr[('canonical','MW ultra-faint')][0]:+.3f} dex/dex (t = "
   f"{dcorr[('canonical','MW ultra-faint')][1]:+.2f}), M_V-controlled t = {dcorr[('canonical','MW ultra-faint')][3]:+.2f}.  "
   f"All 45 MW: raw t = {dcorr[('canonical','MW all')][1]:+.2f}, M_V-controlled t = {dcorr[('canonical','MW all')][3]:+.2f} "
   f"(alt footing {dcorr[('alt','MW all')][3]:+.2f}).  M31 LVD: raw t = {dcorr[('canonical','M31 LVD')][1]:+.2f}, "
   f"M_V-controlled t = {dcorr[('canonical','M31 LVD')][3]:+.2f}")

P("")
P("-"*128)
P("2b. ROBUSTNESS OF 43d -- a contamination found in this script's own sample, and a rank test, before the trend is believed")
P("-"*128)
info("A Wolf half-mass estimator assumes a pressure-supported, non-rotating system.  The LVD Milky Way satellite list carries")
info("the LMC and the SMC, which are ROTATING (V_rot ~ 90 and ~ 60 km/s against sigma ~ 20 and ~ 28), so their line-of-sight")
info("dispersion is not their support and this estimator does not apply to them.  They also sit at the small-D end of the very")
info("axis 43d regresses on.  They are dropped here and the trend is re-measured; the drop is stated as a correction to this")
info("script, not as a choice made after seeing which way it moved.")
info("REPORTED AGAINST MY OWN EXPECTATION: I added this section expecting the two Magellanic Clouds to be manufacturing the")
info("trend, because they sit at the small-D end and their residuals are negative.  Dropping them does NOT weaken it -- the")
info("rank correlation gets STRONGER.  The section is kept, with that stated, rather than quietly deleted.")
ROT = {"LMC", "SMC"}
mw_nr = [d for d in mw if d["name"] not in ROT]
rank = lambda v: (np.argsort(np.argsort(np.asarray(v, float))) + 1.0)
def spearman(x, y):
    rho = float(np.corrcoef(rank(x), rank(y))[0, 1]); n = len(x)
    return rho, rho*math.sqrt(max(n - 2, 1)/max(1 - rho**2, 1e-12))
rob = {}
for tag, s in (("all 45 MW", mw), ("MW minus LMC/SMC", mw_nr),
               ("MW minus LMC/SMC, D>30 kpc", [d for d in mw_nr if d["D"] > 30.0]),
               ("MW ultra-faint only", ufd)):
    r = resid(s, A0["canonical"], cu[("canonical", "mw")][0]); x = np.log10([d["D"] for d in s])
    mv = np.array([d["MV"] for d in s]); n = len(s)
    b, tt = ols_t(r, np.vstack([x, mv, np.ones(n)]).T)
    rho, ts = spearman(x, r)
    # rank-space version of the SAME M_V-controlled regression: the nonparametric analogue of the t that matters
    _, ttr = ols_t(rank(r), np.vstack([rank(x), rank(mv), np.ones(n)]).T)
    info(f"  {tag:28} N={n:3d}  M_V-controlled slope {b[0]:+.3f} (t = {tt[0]:+.2f})  |  raw Spearman {rho:+.3f} (t = {ts:+.2f})"
         f"  |  M_V-controlled rank t = {ttr[0]:+.2f}")
    rob[tag] = (b[0], tt[0], rho, ts, ttr[0], n)
ck("43d-ROB the host-distance trend of 43d SURVIVES every cut I could think of to kill it, including the one I expected to kill "
   "it: the sign and the slope (-0.21 to -0.25 dex/dex) are unchanged by dropping the two rotating Magellanic satellites that a "
   "pressure-support estimator has no business including, by restricting to D_host > 30 kpc where the point-mass host field is "
   "safe, or by moving to rank statistics.  But its SIGNIFICANCE never exceeds 3.0 sigma once luminosity is controlled for, and "
   "on the ultra-faints alone it is 2.0 -- so 43d is a 2-3 sigma indication that the external-field term is mis-shaped, not a "
   "3-sigma result.  The headline of item 43 stays the 0.8-dex normalisation offset, which no cut touches",
   all(v[0] < -0.15 for v in rob.values()) and max(abs(v[1]) for v in rob.values()) < 3.2,
   "; ".join(f"{k}: slope {v[0]:+.3f}, M_V-controlled t = {v[1]:+.2f}, rank t = {v[4]:+.2f} (N={v[5]})"
             for k, v in rob.items()))

# the LambdaCDM / Newtonian alternative, stated beside it
mldyn = [ (3*(d["sig"]*1e3)**2*(4.0/3.0)*d["rh"]*3.0857e16/G/Msun) / (0.5*d["LV"]) for d in ufd ]
info(f"the alternative, computed beside it: the Wolf dynamical mass-to-light ratio inside r_h for these {len(ufd)} ultra-faints is "
     f"M/L_V = {np.min(mldyn):.0f} - {np.max(mldyn):.0f} (median {np.median(mldyn):.0f}).  LambdaCDM absorbs every one of those with "
     f"a free halo per dwarf; the framework has no free parameter left after a_0 and Upsilon_V, which is why it fails here and "
     f"LambdaCDM does not.  That is a LIABILITY, and it is the same liability item 8 already booked.")

P(""); P("="*128); P("3. ITEM 44 -- the M31 satellites (Collins+2013, and the LVD M31 sample)"); P("="*128)
for foot, a0 in A0.items():
    P(f"  --- {foot} a_0 = {a0:.3e} m/s^2, Upsilon_V = {UPS_V} ---")
    res[(foot, "col")] = line("M31 Collins+2013", col, a0)
    res[(foot, "m31")] = line("M31 LVD", m31, a0)
for foot, a0 in A0.items():
    for tag, s in (("col", col), ("m31", m31)):
        cu[(foot, tag)] = centring_ups(s, a0)
    info(f"{foot:10} Upsilon_V that centres the EFE law:  Collins+2013 {cu[(foot,'col')][0]:6.1f} (scatter {cu[(foot,'col')][1]:.3f} dex)"
         f" | LVD M31 {cu[(foot,'m31')][0]:6.1f} (scatter {cu[(foot,'m31')][1]:.3f} dex)")

ck("44a the M31 satellites do NOT reach Kepler grade either: the scatter is 0.25 dex against a 0.10 dex bar, and centring still "
   "needs Upsilon_V ~ 20.  They are better behaved than the Milky Way's whole census but no better than its classical dSphs.  "
   "Reported as found, both footings",
   all(cu[(f, "col")][1] > 0.10 for f in A0),
   "; ".join(f"{f}: Collins+2013 centring Ups_V = {cu[(f,'col')][0]:.1f}, scatter {cu[(f,'col')][1]:.3f} dex "
             f"(median offset {np.median(res[(f,'col')]):+.3f} dex at Ups=2)" for f in A0))
ck("44b the two independent M31 samples agree with each other, so the M31 numbers are not a compilation artefact",
   all(abs(cu[(f, "col")][0] - cu[(f, "m31")][0]) < 0.6*max(cu[(f, "col")][0], cu[(f, "m31")][0]) for f in A0),
   "; ".join(f"{f}: Collins Ups {cu[(f,'col')][0]:.1f} vs LVD Ups {cu[(f,'m31')][0]:.1f}" for f in A0))

# MW-vs-M31 is only a fair comparison at matched luminosity: the MW census is dominated by ultra-faints that M31's is not.
P("")
MVLO, MVHI = -13.0, -8.0
mwL  = [d for d in mw  if MVLO <= d["MV"] <= MVHI]
m31L = [d for d in m31 if MVLO <= d["MV"] <= MVHI]
colL = [d for d in col if MVLO <= d["MV"] <= MVHI]
for foot, a0 in A0.items():
    for tag, s in (("mwL", mwL), ("m31L", m31L), ("colL", colL)):
        cu[(foot, tag)] = centring_ups(s, a0)
    info(f"{foot:10} LUMINOSITY-MATCHED ({MVHI:.0f} >= M_V >= {MVLO:.0f}) centring Upsilon_V:  MW (N={len(mwL)}) "
         f"{cu[(foot,'mwL')][0]:5.1f} (scatter {cu[(foot,'mwL')][1]:.3f}) | M31 LVD (N={len(m31L)}) {cu[(foot,'m31L')][0]:5.1f} "
         f"({cu[(foot,'m31L')][1]:.3f}) | M31 Collins (N={len(colL)}) {cu[(foot,'colL')][0]:5.1f} ({cu[(foot,'colL')][1]:.3f})")
info("the raw MW-vs-M31 gap seen above is therefore MOSTLY a census effect, not a host effect: at matched luminosity the two")
info("satellite systems ask for similar mass-to-light ratios.  Reported this way round because the un-matched comparison would")
info("have looked like a much sharper kill than it is.")
ck("44c AGAINST INTEREST, in the direction that WEAKENS the apparent kill: the framework demands ONE Upsilon_V for every old "
   "stellar population in the Local Group, and the raw MW and M31 samples appear to demand very different ones -- but once the "
   "two samples are matched in luminosity the gap largely closes.  The surviving statement is the weaker (and true) one: BOTH "
   "systems need a mass-to-light ratio of order 10, several times any stellar population, with ~0.25 dex of irreducible scatter",
   all(cu[(f, "mwL")][0] > 3.0 and cu[(f, "m31L")][0] > 3.0 for f in A0),
   "; ".join(f"{f}: matched MW {cu[(f,'mwL')][0]:.1f} vs M31 {cu[(f,'m31L')][0]:.1f} (ratio {cu[(f,'mwL')][0]/cu[(f,'m31L')][0]:.2f}x), "
             f"unmatched ratio was {cu[(f,'mw')][0]/cu[(f,'col')][0]:.1f}x" for f in A0))

P(""); P("="*128); P("4. the EFE-FREE control: the isolated Local-Group dwarfs"); P("="*128)
for foot, a0 in A0.items():
    r = resid(fld, a0); ci = centring_ups(fld, a0); cu[(foot, "fld")] = ci
    gp = [d for d in fld if d["MHI"] < 0.3*UPS_V*d["LV"]]
    rg = resid(gp, a0); cg = centring_ups(gp, a0); cu[(foot, "fldgp")] = cg
    info(f"{foot:10} isolated field dwarfs (N={len(fld)}): at Ups_V=2, median {np.median(r):+.3f} dex, scatter {r.std():.3f} dex; "
         f"centring Ups_V = {ci[0]:.1f} (scatter {ci[1]:.3f} dex).   gas-poor subset (N={len(gp)}: "
         f"{', '.join(d['name'] for d in gp)}): at Ups_V=2 median {np.median(rg):+.3f}, scatter {rg.std():.3f} dex; "
         f"centring Ups_V = {cg[0]:.1f} (scatter {cg[1]:.3f} dex)")
    if foot == "canonical": fld_c, fldgp_c, nfld, ngp, rg_c = ci, cg, len(fld), len(gp), rg
info("caveat both ways: the gas-rich members of this control (NGC 6822, WLM, IC 1613, Leo A, Pegasus, Sag dIrr) are ROTATING, so")
info("their line-of-sight sigma understates the support and the framework is being handed an easy target there; the gas-poor")
info("subset is the honest one and it is only a handful of galaxies.")
ck("43e the EFE-free control localises the failure: the ISOLATED Local-Group dwarfs, where the external-field term is switched "
   "off entirely, sit far closer to the framework's isolated law than the satellites do.  So the ultra-faint liability is NOT a "
   "failure of a_0 or of the kernel -- it is concentrated in satellites, where tides, binaries and the EFE all act at once",
   fld_c[0] < 0.5*cu[("canonical", "mw")][0],
   f"canonical: isolated field centring Upsilon_V = {fld_c[0]:.1f} (N={nfld}, scatter {fld_c[1]:.3f} dex) and gas-poor "
   f"{fldgp_c[0]:.1f} (N={ngp}), against {cu[('canonical','mw')][0]:.1f} for the MW satellites and "
   f"{cu[('canonical','ufd')][0]:.1f} for the ultra-faints")
ck("43f the one place a Kepler-grade scatter DOES appear is the gas-poor isolated dwarfs -- and it is UNDERPOWERED, not a hit: "
   "five galaxies with one free Upsilon_V is 4 degrees of freedom, so a sub-0.1-dex scatter there is not evidence of anything.  "
   "Recorded so that nobody quotes it as a second law.  What it IS good for is the contrast with the satellites, which is large",
   ngp < 10,
   f"canonical gas-poor isolated: scatter {fldgp_c[1]:.3f} dex on N={ngp} at centring Upsilon_V = {fldgp_c[0]:.1f}; a 0.1-dex "
   f"bar needs N of order 30 before it means anything, and the whole isolated Local Group offers {nfld}")

P(""); P("="*128); P("5. the correction to item 8, quantified"); P("="*128)
for foot, a0 in A0.items():
    d8 = resid(mw, a0, nu_arg_true=True) - resid(mw, a0)
    info(f"{foot:10} the h8 EFE recipe [nu evaluated at the TRUE external field, no (1+L) factor] gives dispersions "
         f"{np.median(d8):+.3f} dex ({10**np.median(d8):.2f}x) different from the QUMOND eq.-60 recipe used here; "
         f"h8's centring Upsilon_V should therefore be read as {10**(-2*np.median(d8)):.2f}x its printed value")
d8c = resid(mw, A0["canonical"], nu_arg_true=True) - resid(mw, A0["canonical"])
info("the factor-2 warning in h8 is REAL but applies only in the EFE-DOMINATED limit (check V2 above).  Local Group satellites are "
     "not deeply in that limit -- their own internal field is comparable to the host's -- so on THIS data the two prescriptions")
info(f"differ by only {np.median(d8c):+.3f} dex in sigma.  h8's headline number is therefore not an artefact of its EFE recipe; the "
     f"gap between h8's printed Upsilon_V = 23.8 and this script's {cu[('canonical','mw')][0]:.1f} is a SAMPLE effect (this run adds "
     f"{len(ufd)} ultra-faints that h8's catalogue did not carry) plus the 4/3 deprojection of r_half.")
ck("8-CORR bookkeeping, reported against my own expectation: I expected the corrected QUMOND external-field formula to remove much "
   "of item 8's liability, and it does NOT -- on Local Group satellites the two prescriptions agree to ~0.05 dex, because these "
   "systems are not deeply EFE-dominated.  Item 8's liability stands, and is confirmed here on a 2x larger and newer sample",
   abs(np.median(d8c)) < 0.10 and cu[("canonical", "mw")][0] > 5.0,
   f"prescription difference {np.median(d8c):+.3f} dex in sigma ({10**(2*abs(np.median(d8c))):.2f}x in Upsilon_V); corrected "
   f"all-MW centring Upsilon_V = {cu[('canonical','mw')][0]:.1f} on N={len(mw)}, MW-classical-only "
   f"{cu[('canonical','cls')][0]:.1f} on N={len(cls)} (h8 printed 23.8 on 46 Local Group dwarfs, mostly classical)")

P(""); P("="*128); P("6. mutation controls"); P("="*128)
rng = np.random.default_rng(4344)
sh = [dict(d) for d in mw]; perm = rng.permutation([d["sig"] for d in mw])
for i, d in enumerate(sh): d["sig"] = perm[i]
r_real = resid(mw, A0["canonical"], cu[("canonical", "mw")][0]); r_sh = resid(sh, A0["canonical"], cu[("canonical", "mw")][0])
ck("M1 mutation -- shuffling the measured dispersions between satellites must inflate the scatter of the law",
   r_sh.std() > 1.25*r_real.std(), f"shuffled {r_sh.std():.3f} vs real {r_real.std():.3f} dex")
r_a10 = resid(mw, 10*A0["canonical"], cu[("canonical", "mw")][0])
ck("M2 mutation -- a_0 inflated 10x must move the law's zero point by ~0.25 dex (sigma ~ a_0^{1/4} in the deep-MOND limit)",
   abs(np.median(r_a10) - np.median(r_real)) > 0.10,
   f"median shifts {np.median(r_real):+.3f} -> {np.median(r_a10):+.3f} dex ({np.median(r_real)-np.median(r_a10):+.3f})")
r_newt = resid(mw, A0["canonical"], cu[("canonical", "mw")][0], newt=True)
ck("M3 mutation -- switching the kernel off (nu = 1, pure Newton with the same baryons) must make the fit worse, not better",
   abs(np.median(r_newt)) > abs(np.median(r_real)),
   f"Newtonian median offset {np.median(r_newt):+.3f} dex vs framework {np.median(r_real):+.3f} dex at the same Upsilon_V")

P(""); P("="*128); P("VERDICT"); P("="*128)
P("  ITEM 43 -- NOT a second law, and a LIABILITY.  The ultra-faint dwarfs do not lie on a sigma(M_b, D_host) line with a single")
P("  a_0 and a stellar-population mass-to-light ratio: at Upsilon_V = 2 they sit 0.83 dex above the framework's external-field")
P(f"  prediction, centring needs Upsilon_V ~ {cu[('canonical','ufd')][0]:.0f}, and even after Upsilon_V is tuned freely the residual scatter is {cu[('canonical','ufd')][1]:.2f} dex --")
P("  two to three times the 0.1-dex Kepler-grade bar.  This is the known MOND ultra-faint problem, reproduced on a larger and newer")
P("  sample (Local Volume Database) with the correct QUMOND external-field formula, not a new discovery.  LambdaCDM absorbs the")
P(f"  same data with one free halo per dwarf (the Wolf M/L_V runs {np.min(mldyn):.0f}-{np.max(mldyn):.0f}).  A SECOND negative found here, and it is the weaker of the two: the")
P("  residual correlates with the host distance at 2.0-3.0 sigma after controlling for luminosity (3.0 in least squares on all 45,")
P("  2.0-2.5 in the rank version and on the ultra-faints alone; sign and slope robust to every cut in section 2b), so the")
P("  external-field term itself is")
P("  mis-shaped on the Milky Way's satellites, not merely mis-normalised.")
P(f"  ITEM 44 -- also NOT Kepler-grade: Collins+2013's M31 dSphs need Upsilon_V ~ {cu[('canonical','col')][0]:.0f} with {cu[('canonical','col')][1]:.2f} dex of scatter.  My first")
P("  framing of this -- 'the MW and M31 demand different mass-to-light ratios, which a one-constant law cannot survive' -- did NOT")
P("  hold up: matched in luminosity the two systems agree to 20%, and the apparent gap was a census effect.  The surviving")
P("  statement is the weaker and true one, that BOTH satellite systems need a mass-to-light ratio of order 10-20 and carry 0.25 dex")
P("  of irreducible scatter.  Booked as a LIABILITY on both footings, but a shared Local-Group one rather than a host-dependent one.")
P("  THE ONE RESULT THAT CUTS THE OTHER WAY, and it is the most interesting thing in the run: switch the external field OFF and the")
P(f"  same estimator on the same catalogue lands on the ISOLATED Local-Group dwarfs at Upsilon_V = {cu[('canonical','fld')][0]:.1f} (gas-poor subset {cu[('canonical','fldgp')][0]:.1f}) with")
P(f"  {cu[('canonical','fld')][1]:.2f} dex of scatter.  The satellite liability is therefore localised in satellites -- tides, binaries and the EFE -- and is")
P("  NOT a failure of a_0 or of the Route A kernel.  That subsample is only 13 galaxies (5 gas-poor) and is recorded as")
P("  UNDERPOWERED, not as a hit; it is a target for a future pass, not a claim.")
P("  ITEM 8 CORRECTION -- h8's external-field prescription (nu evaluated at the TRUE field rather than the Newtonian one, with no")
P("  (1+dln nu/dln y) factor) is not the QUMOND one, and the factor-2 warning h8 recorded is real -- but only in the EFE-DOMINATED")
P("  limit, which Local Group satellites are not in.  On this data the two recipes differ by 0.05 dex, so item 8's liability is not")
P("  an artefact of its recipe.  It stands.")
P("  Caveats stated both ways: the ultra-faint dispersions are themselves contested (binaries, tidal heating, N_star ~ 10-100),")
P("  the point-mass approximation for the host field is marginal for the innermost satellites, eq. 60 is a one-dimensional EFE")
P("  formula that neglects the direction of the external field, and the gas-rich isolated dwarfs rotate, so their line-of-sight")
P("  dispersion understates their support and flatters the framework.")
sys.exit(ck.done())
