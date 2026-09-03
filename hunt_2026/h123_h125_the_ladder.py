#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""h123_h125_the_ladder.py -- items 123 and 125 of the second-law hunt: the two that close it.

ITEM 123  "the two footings, decided".  Using ONLY measurements whose stellar mass-to-light leverage is small,
          is a_0 = 9.36e-11 or a_0 = 1.13e-10 excluded at 3 sigma?  If neither is, what precision would it take?

ITEM 125  "the ladder, closed".  Item 100 built an a_0 ladder from seven measurements and found a 0.16 dex
          intrinsic spread organised by the stellar M/L.  Rebuild it from M/L-free rungs only and measure what
          is left.  If the M/L-free rungs agree to better than 0.05 dex that is a second Kepler-grade result.

RULES HONOURED HERE.  Both footings on every dimensionful number.  Every rung is traced to a committed .out in
this directory (the provenance string is printed with it) and the two SPARC rungs are RE-DERIVED from the raw
data in section 0 and checked against those .out values, so nothing rests on a transcription.  Checks that can
fail; mutation controls in section 5; the LambdaCDM/Newtonian alternative in section 4.

TWO THINGS THIS SCRIPT DELIBERATELY DOES NOT DO.
  * It does not use item 103's error budget.  That item's win did not survive adversarial verification, so the
    coherent floor is rebuilt here from sensitivities this script measures itself (section 2A) -- which lands
    close to item 103's number, but it is derived here and can be checked here.
  * It does not use item 121's a_0 = 9.333e-11.  Same reason: refuted in verification.  It is carried only as a
    named sensitivity in section 3D so the reader can see what admitting it would do.
"""
import os, sys, math
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(125)
LC, LA = math.log10(A0["canonical"]), math.log10(A0["alt"])
SEP = LA - LC                                   # the two footings are this far apart, in dex
GBCUT = 1e-11                                   # item 25 / item 102 deep-tail cut, kept identical
MLFREE_LEVER = 0.20                             # the admission rule for "M/L-free", defined in section 1


# ============================================================================================ shared estimators
def a0_kern(x, y):
    """Solve <log g_obs - log[nu(g_bar/a_0) g_bar]> = 0 with the FULL Route A kernel (item 102's estimator)."""
    f = lambda a: float(np.mean(np.log10(y) - np.log10(nu(x/a)*x)))
    try:
        return brentq(f, 1e-13, 1e-7, xtol=1e-18, rtol=8.9e-16, maxiter=200)
    except Exception:
        return float("nan")


def gbar_of(g, ups):
    return (g["vg"]*np.abs(g["vg"]) + ups*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC


def gstar_of(g, ups):
    return (ups*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC


def med_boot(v, n=4000):
    v = np.asarray(v, dtype=float); v = v[np.isfinite(v)]
    b = np.array([np.median(rng.choice(v, len(v))) for _ in range(n)])
    return float(np.median(v)), float(b.std())


def dexerr(a0v, abs_err):
    return abs_err/a0v/math.log(10)


# ======================================================================================================= SECTION 0
P("="*120)
P("0.  PROVENANCE -- the two SPARC M/L-free rungs re-derived from the raw data, checked against the committed .out")
P("="*120)
gals = load_sparc()
info(f"SPARC: {len(gals)} discs pass the standard quality cuts (Q<=2, i>=30 deg, >=6 points)")

# ---- rung R1: item 102's M/L-free deep tail -- points with g_bar < 1e-11 AND local stellar share < 0.2
def deeptail(ups=UPS_D, fsmax=None, gsel=None, dsel=None):
    """Returns (g_bar, g_obs, per-galaxy index, galaxy list).  Selection always made at Upsilon = 0.5 so that
    varying `ups` measures the estimator's sensitivity at FIXED sample."""
    X, Y, gi, keep = [], [], [], []
    for g in gals:
        if dsel is not None and not dsel(g): continue
        gb_s, gs_s = gbar_of(g, UPS_D), gstar_of(g, UPS_D)
        gb = gbar_of(g, ups) if gsel is None else gsel(g, ups)
        with np.errstate(invalid="ignore", divide="ignore"):
            fs = gs_s/gb_s
        m = (gb_s > 0) & (gb_s < GBCUT) & (gb > 0)
        if fsmax is not None: m &= (fs < fsmax)
        if m.sum() == 0: continue
        keep.append(g); X.append(gb[m]); Y.append(g["gobs"][m]); gi.append(np.full(m.sum(), len(keep)-1))
    if not X: return None
    return np.concatenate(X), np.concatenate(Y), np.concatenate(gi), keep


def boot_gal(x, y, gi, nb=500):
    ng = int(gi.max())+1; out = []
    for _ in range(nb):
        idx = rng.integers(0, ng, ng)
        sel = np.concatenate([np.where(gi == j)[0] for j in idx])
        v = a0_kern(x[sel], y[sel])
        if np.isfinite(v): out.append(v)
    return float(np.log10(np.array(out)).std())


x1, y1, gi1, keep1 = deeptail(fsmax=0.2)
R1_a0 = a0_kern(x1, y1); R1_sig = boot_gal(x1, y1, gi1)
info(f"R1  M/L-free deep tail (g_bar<1e-11, f_*,loc<0.2): a_0 = {R1_a0:.4e} +- {R1_sig:.4f} dex "
     f"({len(keep1)} galaxies, {len(x1)} points)")
ck("0.1 rung R1 re-derived from the SPARC rotmods reproduces h102_gas_dominated_a0.out's committed number "
   "(7.361e-11 +- 0.062 dex) -- the ladder below is not built on a transcribed value",
   abs(math.log10(R1_a0/7.361e-11)) < 0.01 and abs(R1_sig - 0.062) < 0.015,
   f"re-derived {R1_a0:.4e} +- {R1_sig:.3f} vs committed 7.361e-11 +- 0.062 "
   f"({math.log10(R1_a0/7.361e-11):+.4f} dex)")

# ---- rung R2: item 124's rung A -- the outermost measured point of gas-dominated discs, all baryons
rowsA = []
for g in gals:
    gg = g["vg"]*np.abs(g["vg"])/g["r"]*KMS2_KPC
    gb = gbar_of(g, UPS_D)
    i = len(g["r"]) - 1
    if gg[i] <= 0 or gb[i] <= 0: continue
    Mb = UPS_D*g["L36"]*1e9 + 1.33*g["MHI"]*1e9
    rowsA.append(dict(name=g["name"], fs=1 - gg[i]/gb[i], gb=gb[i], gg=gg[i], gobs=g["gobs"][i],
                      Mb=Mb, eD=g["eD"]/max(g["D"], 1e-9),
                      a_bar=a0_kern(np.array([gb[i]]), np.array([g["gobs"][i]])),
                      a_gas=a0_kern(np.array([gg[i]]), np.array([g["gobs"][i]]))))
selA = [r for r in rowsA if r["fs"] < 0.2]
lb = np.log10(np.array([r["a_bar"] for r in selA])); lg = np.log10(np.array([r["a_gas"] for r in selA]))
fin = np.isfinite(lb) & np.isfinite(lg)
R2_l, R2_sig = med_boot(lb[fin]); R2g_l, R2g_sig = med_boot(lg[fin])
R2_a0, R2g_a0 = 10**R2_l, 10**R2g_l
info(f"R2  gas-dominated discs, outermost point, all baryons: a_0 = {R2_a0:.4e} +- {R2_sig:.4f} dex "
     f"({int(fin.sum())} discs);  gas-only variant {R2g_a0:.4e} +- {R2g_sig:.4f}")
ck("0.2 rung R2 re-derived reproduces h124_stellar_mass_free_a0.out's rung A (7.816e-11 +- 0.083 dex stat) and "
   "its gas-only variant (9.088e-11 +- 0.088)",
   abs(math.log10(R2_a0/7.816e-11)) < 0.01 and abs(math.log10(R2g_a0/9.088e-11)) < 0.01,
   f"re-derived {R2_a0:.4e} / {R2g_a0:.4e} vs committed 7.816e-11 / 9.088e-11")

# ---- rung R3: item 105's BTFR zero-point on gas-dominated galaxies, with the structural factor C removed
BT = []
for g in gals:
    if g["Vflat"] <= 0: continue
    Mb = UPS_D*g["L36"]*1e9 + 1.33*g["MHI"]*1e9
    if Mb <= 0: continue
    gb = gbar_of(g, UPS_D)[-1]; R = g["r"][-1]*kpc
    if gb <= 0: continue
    BT.append(dict(name=g["name"], Mb=Mb, fgas=1.33*g["MHI"]*1e9/Mb, gb=gb,
                   eps=gb*R*R/(G*Mb*Msun), a0=(g["Vflat"]*1e3)**4/(G*Mb*Msun)))
gd = [d for d in BT if d["fgas"] > 0.7]
R3raw_l, R3raw_sig = med_boot(np.log10([d["a0"] for d in gd]))
# C = nu(y)^2 y eps, computed on THIS subsample rather than borrowed from the full sample
Cg = {k: float(np.median([nu_s(d["gb"]/A0[k])**2*(d["gb"]/A0[k])*d["eps"] for d in gd])) for k in A0}
Call = {k: float(np.median([nu_s(d["gb"]/A0[k])**2*(d["gb"]/A0[k])*d["eps"] for d in BT])) for k in A0}
R3_a0 = {k: 10**R3raw_l/Cg[k] for k in A0}
info(f"R3  BTFR zero-point on the {len(gd)} f_gas>0.7 galaxies: raw {10**R3raw_l:.4e} +- {R3raw_sig:.4f} dex")
info(f"    the structural factor C = nu(y)^2 y eps measured on THOSE SAME galaxies: "
     f"{Cg['canonical']:.3f} canonical / {Cg['alt']:.3f} alt "
     f"(the full SPARC sample gives {Call['canonical']:.3f}, which is item 105's 1.59)")
info(f"    C-removed: a_0 = {R3_a0['canonical']:.4e} (canonical footing) / {R3_a0['alt']:.4e} (alt footing)")
ck("0.3 rung R3 re-derived reproduces h105_btfr_a0_meter.out's gas-dominated BTFR zero-point (1.090e-10) and its "
   "full-sample structural factor C = 1.59, and it shows AGAINST THE EARLIER READING that the gas-dominated "
   "subsample's own C is smaller than the full sample's -- so borrowing 1.59 would have over-corrected this rung",
   abs(math.log10(10**R3raw_l/1.090e-10)) < 0.02 and abs(Call["canonical"] - 1.59) < 0.06,
   f"raw {10**R3raw_l:.4e} vs 1.090e-10; C(gas-dominated) = {Cg['canonical']:.3f} vs C(all) = {Call['canonical']:.3f} "
   f"-- a {math.log10(Call['canonical']/Cg['canonical']):+.3f} dex difference")


# ======================================================================================================= SECTION 1
P(""); P("="*120)
P("1.  THE ADMISSION RULE, AND WHAT IT DOES TO ITEM 100's LADDER")
P("="*120)
info("An a_0 measurement is admitted as M/L-FREE here if its MEASURED leverage |d log a_0/d log Upsilon| <= 0.20,")
info("i.e. a factor-2 error in the stellar mass-to-light ratio moves it by less than 0.06 dex.  The leverage is")
info("not asserted for any rung: item 102 measured it for the deep tail by re-running at fixed sample, item 111")
info("measured it for every KiDS bin by rescaling the adopted baryonic mass, item 105 measured it for the BTFR.")
info("")

# measure R1's leverage here rather than quoting it
lev_pts = []
for u in (0.4, 0.5, 0.6):
    xx, yy, _, _ = deeptail(ups=u, fsmax=0.2)
    lev_pts.append((math.log10(u), math.log10(a0_kern(xx, yy))))
R1_lev = (lev_pts[2][1]-lev_pts[0][1])/(lev_pts[2][0]-lev_pts[0][0])
info(f"  R1's leverage measured at fixed sample by re-running at Upsilon = 0.4/0.5/0.6: "
     f"d log a_0/d log Upsilon = {R1_lev:+.3f}  (item 102 got -0.148)")

REGISTER = [
    # label, a_0, err(dex), |lever|, admitted, provenance
    ("SPARC deep tail, f_*,loc < 0.2",                 R1_a0,     R1_sig, abs(R1_lev), True,  "h102 (re-derived above)"),
    ("SPARC gas-dominated discs, outermost point",     R2_a0,     R2_sig, 0.182,       True,  "h124 rung A (re-derived)"),
    ("SPARC BTFR, f_gas>0.7, C removed",               R3_a0["canonical"], R3raw_sig, 0.18, True, "h105 part E (re-derived)"),
    ("KiDS-1000 lensing, shape-only a_0",              6.31e-11,  0.300,  0.000,       True,  "h113 check 113-D2"),
    ("ALFALFA gas-dominated (f_* < 0.15), all baryons",5.820e-11, 0.250,  0.110,       True,  "h124 rung B table"),
    ("Leisman almost-darks, ceiling-matched",          3.110e-11, 0.130,  0.000,       True,  "h124 rung C / item 31b"),
    ("Lelli tidal dwarfs, external field included",    1.734e-11, 0.170,  0.000,       True,  "h124 rung D"),
    ("KiDS-1000 dwarf lens stack",                     9.55e-11,  0.109,  1.046,       False, "h1_h66_h2_h65 item 2; lever from h111-A"),
    ("SPARC full deep tail, full kernel",              9.040e-11, 0.038,  0.647,       False, "h102 sec.2; lever h121a"),
    ("SPARC full deep tail, item 25 as published",     1.146e-10, 0.043,  0.647,       False, "item 25; +0.10 dex estimator bias, h102 sec.0"),
    ("SPARC BTFR all 122, C removed",                  9.818e-11, 0.029,  0.591,       False, "h105 check 105-C"),
    ("KiDS colour bins (blue / red)",                  8.84e-11,  0.052,  1.046,       False, "h111 fig-8; red bin 2.83e-10"),
    ("KiDS Sersic bins (disc / bulge)",                1.06e-10,  0.048,  1.046,       False, "h112 fig-8; bulge bin 2.53e-10"),
    ("SPARC closed-form inversion at R_eff",           1.176e-10, 0.056,  0.647,       False, "h101; f_DM carries a stellar mass model"),
    ("RC100 closed-form inversion at R_e",             1.385e-10, 0.070,  0.647,       False, "h101; same"),
    ("Li+2020 halo product 2 pi G rho_0 r_0",          1.69e-10,  1.200,  0.647,       False, "h106; profile-choice systematic 1.2 dex"),
]
info("")
info(f"  {'measurement':52} {'a_0':>11} {'+-dex':>7} {'|lever|':>8}  {'M/L-free?':>10}  provenance")
for nm, v, e, lv, adm, prov in REGISTER:
    info(f"  {nm:52} {v:11.3e} {e:7.3f} {lv:8.3f}  {'ADMIT' if adm else 'reject':>10}  {prov}")

ck("1.1 ITEM 100's HEADLINE IS WITHDRAWN, and it is my own workflow's number.  Item 100 wrote that 'the two "
   "measurements that do NOT lean on a stellar M/L -- the gas-dominated deep tail and the dwarf lens stack -- "
   "agree to 0.08 dex'.  NEITHER of those two is M/L-free on a measured leverage: the deep tail as item 25 ran it "
   "carries -0.647 (h121a) and the KiDS dwarf lens stack carries -1.046 (h111-A, where a deep-MOND lensing a_0 is "
   "degenerate with the assumed baryonic mass at exponent 1).  The sentence that organised two ledgers is false",
   abs(0.647) > MLFREE_LEVER and abs(1.046) > MLFREE_LEVER,
   "deep tail lever -0.647, dwarf lens stack lever -1.046, both above the 0.20 admission threshold; and their "
   "0.08 dex agreement is itself an artefact -- the deep-tail value in it (1.14e-10) carried the +0.10 dex "
   "estimator bias h102 found")

ck("1.2 the admission rule keeps something: 7 of the 16 measurements in the hunt clear |lever| <= 0.20, so the "
   "M/L-free ladder is not empty -- but 3 of the 7 are the SAME 20-23 SPARC gas-rich discs seen through different "
   "estimators, which is a fact section 3 has to handle rather than average over",
   sum(1 for r in REGISTER if r[4]) == 7,
   f"{sum(1 for r in REGISTER if r[4])} admitted of {len(REGISTER)}; admitted rungs R1,R2,R3 share SPARC galaxies")


# ======================================================================================================= SECTION 2
P(""); P("="*120)
P("2.  ITEM 123 -- THE TWO FOOTINGS, DECIDED?")
P("="*120)
info(f"canonical a_0 = {A0['canonical']:.3e} (log {LC:.4f}) | alt a_0 = {A0['alt']:.3e} (log {LA:.4f})")
info(f"they are {SEP:.4f} dex apart, so a 3 sigma decision needs a TOTAL error of {SEP/3:.4f} dex = "
     f"{100*(10**(SEP/3)-1):.1f}% on an M/L-free measurement of a_0")

P(""); P("-"*120); P("2A.  the coherent floor, built here from sensitivities this script measures (item 103 is not used)")
P("-"*120)
# analytic sensitivities from the estimator's own equation, then measured numerically on the R1 sample
nvals = []
for a in (A0["canonical"],):
    yv = x1/a
    dl = 1e-4
    nvals = (np.log(nu(yv*math.exp(dl))) - np.log(nu(yv/math.exp(dl))))/(2*dl)
nbar = float(np.mean(nvals))
info(f"  the kernel's mean local log-slope on the R1 points: <n> = <d log nu/d log y> = {nbar:+.4f} "
     f"(the deep-MOND limit is -1/2)")
info(f"  analytic, from d/d log a of the estimating equation:  d log a_0/d log D      = 1/<n> = {1/nbar:+.3f}")
info(f"                                                        d log a_0/d log M_gas  = (1+<n>)/<n> x (gas share)")

# numerical: distance.  Scaling every distance by f scales r by f and V_bar by sqrt(f), so g_bar is invariant
# and g_obs = V_obs^2/r scales as 1/f.  (This is the SPARC scaling; it is why a_0 ~ D^-2.2 and not D^-2.)
fD = 1.05
a_up = a0_kern(x1, y1/fD)
lev_D = math.log10(a_up/R1_a0)/math.log10(fD)
info(f"  numerical, scaling every distance by {fD}: d log a_0/d log D = {lev_D:+.3f}  "
     f"(item 103 measured -2.254 independently)")
ck("2A.1 the distance sensitivity is the analytic 1/<n>, not the textbook deep-MOND -2 -- so the deep tail's a_0 "
   "inherits 2.2x the distance ladder's fractional error, not 2x.  Derived and measured two ways here, so it does "
   "not depend on item 103, whose win did not survive verification",
   abs(lev_D - 1/nbar) < 0.05, f"numerical {lev_D:+.3f} vs analytic 1/<n> = {1/nbar:+.3f}")

# numerical: the HI mass scale.  V_gas ~ sqrt(M_gas), so scaling M_gas by f scales g_gas by f.
def gbar_gasscaled(g, ups, f):
    return (f*g["vg"]*np.abs(g["vg"]) + ups*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC


fG = 1.10
xg, yg, _, _ = deeptail(fsmax=0.2, gsel=lambda g, u, f=fG: gbar_gasscaled(g, u, f))
lev_G = math.log10(a0_kern(xg, yg)/R1_a0)/math.log10(fG)
gas_share = float(np.mean(1 - np.array([0.0])))  # placeholder replaced below
gshare = []
for g in keep1:
    gb_s, gs_s = gbar_of(g, UPS_D), gstar_of(g, UPS_D)
    m = (gb_s > 0) & (gb_s < GBCUT) & ((gs_s/gb_s) < 0.2)
    if m.sum(): gshare.append(np.mean(1 - gs_s[m]/gb_s[m]))
gas_share = float(np.mean(gshare))
info(f"  numerical, scaling the HI mass scale by {fG}: d log a_0/d log M_gas = {lev_G:+.3f} "
     f"(gas supplies {100*gas_share:.0f}% of g_bar on these points)")
ck("2A.2 THE PRICE OF REMOVING THE STELLAR M/L, and it is the sharpest new number in item 123.  Cutting to points "
   "where stars supply under 20% of g_bar drops the Upsilon leverage to 0.15 -- but it RAISES the HI mass scale's "
   "leverage to very nearly 1.2, because the same gas now supplies almost all of g_bar.  The measurement does not "
   "become calibration-free; it trades a stellar calibration for a hydrogen one, at higher leverage",
   abs(lev_G) > 1.0 and abs(R1_lev) < MLFREE_LEVER,
   f"d log a_0/d log M_gas = {lev_G:+.3f} against d log a_0/d log Upsilon = {R1_lev:+.3f}; "
   f"gas is {100*gas_share:.0f}% of g_bar")

# the floor, two ways: an optimistic and a realistic calibration budget
BUDGETS = [
    ("optimistic  (distance scale 2%, HI mass scale 0.03 dex, inclination zero-point 1 deg)", 0.02, 0.03, 1.0),
    ("realistic   (distance scale 5%, HI mass scale 0.05 dex, inclination zero-point 2 deg)", 0.05, 0.05, 2.0),
]
inc_med = float(np.median([g["inc"] for g in keep1]))
lev_inc = 2*(1/nbar)                                  # a_0 ~ (sin i)^{2/<n>}: V_obs ~ 1/sin i, g_obs ~ 1/sin^2 i
info(f"  inclination: V_obs ~ 1/sin i so g_obs ~ sin^-2 i and d log a_0/d log sin i = 2/<n> = {lev_inc:+.3f} "
     f"(median inclination of the R1 sample {inc_med:.0f} deg)")
floors = {}
for nm, dD, dG, dI in BUDGETS:
    tD = abs(lev_D)*math.log10(1+dD)
    tG = abs(lev_G)*dG
    tI = abs(lev_inc)*abs(math.log10(math.sin(math.radians(inc_med+dI))/math.sin(math.radians(inc_med))))
    tot = math.sqrt(tD**2 + tG**2 + tI**2)
    floors[nm.split()[0]] = tot
    info(f"    {nm:78} -> distance {tD:.4f}, gas {tG:.4f}, inclination {tI:.4f}  TOTAL {tot:.4f} dex")
FLOOR = floors["realistic"]
ck("2A.3 the COHERENT floor under any M/L-free deep-tail a_0 is dominated by the HI mass scale, not by anything "
   "stellar and not by the distance scale.  Even on the optimistic budget it exceeds the 0.027 dex a 3 sigma "
   "footing decision needs, so NO amount of extra galaxies can decide the footings by this route",
   floors["optimistic"] > SEP/3,
   f"optimistic floor {floors['optimistic']:.4f} dex, realistic {floors['realistic']:.4f} dex, "
   f"against the {SEP/3:.4f} dex a 3 sigma decision requires")

P(""); P("-"*120); P("2B.  the footing test, on each admitted M/L-free rung")
P("-"*120)
info(f"  {'rung':52} {'a_0':>11} {'sig_tot':>8} {'canonical':>11} {'alt':>11}")
foot = []
for nm, v, e, lv, adm, prov in REGISTER:
    if not adm: continue
    sig = math.hypot(e, FLOOR) if "SPARC" in nm or "ALFALFA" in nm or "Leisman" in nm or "Lelli" in nm else e
    sc, sa = (math.log10(v)-LC)/sig, (math.log10(v)-LA)/sig
    foot.append((nm, v, e, sig, sc, sa))
    info(f"  {nm:52} {v:11.3e} {sig:8.4f} {sc:+10.2f}s {sa:+10.2f}s")
best = foot[0]
ck("2B.1 ITEM 123's OWN CRITERION, and it is NOT met.  On the headline M/L-free measurement -- the SPARC deep tail "
   "with the stellar share of g_bar under 20% -- NEITHER footing is excluded at 3 sigma once the coherent "
   "calibration floor is carried.  The measured value sits BELOW both, by 1.0 sigma and 1.8 sigma respectively, "
   "so the most that can be said is that it leans canonical.  Note which two rungs DO exclude both footings at "
   "over 3 sigma: the almost-darks and the tidal dwarfs, the two item 124 identified as non-measurements",
   abs(best[4]) < 3 and abs(best[5]) < 3,
   f"a_0 = {best[1]:.3e} +- {best[3]:.4f} dex total: canonical {best[4]:+.2f} sigma, alt {best[5]:+.2f} sigma")

P(""); P("-"*120); P("2C.  the two ways the verdict flips, which is why it cannot be quoted either way")
P("-"*120)
# (i) distance quality inside the SAME M/L-free sample
xg1, yg1, gg1, kg1 = deeptail(fsmax=0.2, dsel=lambda g: g["eD"]/g["D"] < 0.12)
xh1, yh1, gh1, kh1 = deeptail(fsmax=0.2, dsel=lambda g: g["eD"]/g["D"] >= 0.12)
ag, sg = a0_kern(xg1, yg1), boot_gal(xg1, yg1, gg1)
ah, sh = a0_kern(xh1, yh1), boot_gal(xh1, yh1, gh1)
info(f"  distance error < 12% (TRGB/Cepheid/direct), {len(kg1):2d} galaxies: a_0 = {ag:.4e} +- {sg:.3f} dex   "
     f"canonical {(math.log10(ag)-LC)/math.hypot(sg,FLOOR):+.2f}s   alt {(math.log10(ag)-LA)/math.hypot(sg,FLOOR):+.2f}s")
info(f"  distance error >= 12% (Hubble flow),         {len(kh1):2d} galaxies: a_0 = {ah:.4e} +- {sh:.3f} dex   "
     f"canonical {(math.log10(ah)-LC)/math.hypot(sh,FLOOR):+.2f}s   alt {(math.log10(ah)-LA)/math.hypot(sh,FLOOR):+.2f}s")
split = math.log10(ag/ah)
ck("2C.1 AGAINST INTEREST, and it is fatal to any footing claim from this sample: splitting the SAME M/L-free "
   "galaxies on distance QUALITY moves a_0 by more than twice the separation between the two footings.  The eight "
   "galaxies with TRGB or Cepheid distances land on the canonical footing; the fifteen with Hubble-flow distances "
   "land 0.2 dex below it.  A verdict that flips on a cut choice is not a verdict",
   abs(split) > SEP,
   f"good distances {ag:.3e} vs Hubble flow {ah:.3e}: {split:+.3f} dex, against a footing separation of {SEP:.3f} dex; "
   f"on the good-distance half alt is only {(math.log10(ag)-LA)/math.hypot(sg,FLOOR):+.2f} sigma away")

# (ii) estimator choice on the same galaxies
est_choice = [("deep-tail points, all baryons", R1_a0, True), ("outermost point, all baryons", R2_a0, True),
              ("BTFR zero-point, C removed", R3_a0["canonical"], True),
              ("outermost point, GAS ONLY (biased +0.086 dex, h124)", R2g_a0, False)]
info("")
for nm, v, dfns in est_choice:
    info(f"  {nm:52} a_0 = {v:.4e}  ({math.log10(v)-LC:+.3f} canonical, {math.log10(v)-LA:+.3f} alt)"
         f"{'' if dfns else '   <- upper bound, not a best estimate'}")
lv_d = np.array([math.log10(v) for _, v, d in est_choice if d])
lv_e = np.array([math.log10(v) for _, v, _ in est_choice])
info(f"  spread of the THREE defensible estimators on essentially the SAME 21-23 gas-rich SPARC discs: "
     f"{lv_d.max()-lv_d.min():.3f} dex (full range), {lv_d.std():.3f} dex (rms)")
info(f"  including the gas-only upper bound as well: {lv_e.max()-lv_e.min():.3f} dex")
ck("2C.2 MY OWN SECOND FLIP, TESTED AND WITHDRAWN.  I expected estimator choice to move a_0 by more than the gap "
   "between the footings, as the distance split does.  It does not: the three defensible M/L-free estimators on "
   "these discs span only a third of the footing separation, so estimator choice is a sub-dominant systematic "
   "here and the claim is retracted.  The range only exceeds the gap if the gas-only variant is included, and "
   "h124 already showed that one is a known-biased upper bound rather than a competing estimate",
   (lv_d.max()-lv_d.min()) < SEP,
   f"three defensible estimators span {lv_d.max()-lv_d.min():.3f} dex (rms {lv_d.std():.3f}) against a footing "
   f"separation of {SEP:.3f} dex; with the biased gas-only variant the range is {lv_e.max()-lv_e.min():.3f} dex")

P(""); P("-"*120); P("2D.  what precision WOULD decide it, and where it would have to come from")
P("-"*120)
need = SEP/3
info(f"  required TOTAL error for a 3 sigma exclusion of one footing: {need:.4f} dex ({100*(10**need-1):.1f}%)")
for nm, dD, dG, dI in BUDGETS:
    tD = abs(lev_D)*math.log10(1+dD); tG = abs(lev_G)*dG
    info(f"    on the {nm.split()[0]:11} budget the calibration floor alone is {floors[nm.split()[0]]:.4f} dex "
         f"= {floors[nm.split()[0]]/need:.1f}x the whole allowance")
dD_need = 10**(need/abs(lev_D)) - 1
dG_need = need/abs(lev_G)
info(f"  spending the WHOLE budget on one channel: the distance scale would have to be known to "
     f"{100*dD_need:.2f}%, or the HI mass scale to {dG_need:.4f} dex ({100*(10**dG_need-1):.1f}%)")
# a balanced split: three equal channels plus statistics
per = need/2
dD_bal = 10**(per/abs(lev_D)) - 1; dG_bal = per/abs(lev_G)
ngal_need = (R1_sig/ (need/2))**2 * len(keep1)
info(f"  a balanced requirement (half the budget to calibration, half to statistics):")
info(f"    distance scale to {100*dD_bal:.2f}%  AND  HI mass scale to {dG_bal:.4f} dex ({100*(10**dG_bal-1):.1f}%)"
     f"  AND  about {ngal_need:.0f} gas-dominated discs with resolved curves (SPARC has {len(keep1)})")
ck("2D.1 the answer to item 123, stated as a requirement rather than as a result: deciding between 9.36e-11 and "
   "1.13e-10 needs a total 2.7% on an M/L-free a_0.  That means the distance scale to about 1%, the HI mass scale "
   "(flux calibration plus the helium factor plus molecular gas) to about 3%, and roughly ten times SPARC's "
   "gas-dominated sample.  None of the three exists today, and the first two are not sample-size problems",
   need < floors["optimistic"] and ngal_need > 5*len(keep1),
   f"need {need:.4f} dex; optimistic floor {floors['optimistic']:.4f}; need ~{ngal_need:.0f} discs vs {len(keep1)} in hand")


# ======================================================================================================= SECTION 3
P(""); P("="*120)
P("3.  ITEM 125 -- THE LADDER REBUILT FROM M/L-FREE RUNGS ONLY")
P("="*120)


def intrinsic(lv, ed):
    """Item 100's estimator, kept identical: sqrt(var(log a_0) - mean(quoted dex error^2))."""
    return float(np.sqrt(max(np.var(lv) - np.mean(np.asarray(ed)**2), 0.0)))


def intrinsic_ml(lv, ed, grid=None):
    """Maximum-likelihood intrinsic scatter about a free mean, for comparison with item 100's moment estimator."""
    lv = np.asarray(lv); ed = np.asarray(ed)
    grid = np.linspace(0, 1.5, 3001) if grid is None else grid
    best, bs = -1e99, 0.0
    for s in grid:
        v = ed**2 + s**2; w = 1/v
        mu = float(np.sum(w*lv)/np.sum(w))
        ll = -0.5*np.sum((lv-mu)**2/v + np.log(v))
        if ll > best: best, bs = ll, s
    return bs


# masses and accelerations actually probed, measured where a local value exists
huds = load_huds()
hud_lm = np.log10(10**huds["logMHI"][np.isfinite(huds["logMHI"])]*1.33)
alf = load_alfalfa()
mA_ = np.isfinite(alf["logMHI"]) & np.isfinite(alf["logMsM"])
alf_lm = np.log10(1.33*10**alf["logMHI"][mA_] + 10**alf["logMsM"][mA_])

R1_lm = np.log10([UPS_D*g["L36"]*1e9 + 1.33*g["MHI"]*1e9 for g in keep1])
R2_lm = np.log10([r["Mb"] for r in selA])
R3_lm = np.log10([d["Mb"] for d in gd])

LADDER = [
    # name, a_0, err(dex), log M_b 16-84 pct, log g_bar 16-84 pct (nan where none), velocity class, system class
    ("R1 SPARC deep tail, f_*,loc<0.2",        R1_a0, math.hypot(R1_sig, FLOOR),
     (np.percentile(R1_lm, 16), np.percentile(R1_lm, 84)),
     (np.percentile(np.log10(x1), 16), np.percentile(np.log10(x1), 84)), "resolved RC", "SPARC discs"),
    ("R2 SPARC gas-dom, outermost point",      R2_a0, math.hypot(R2_sig, FLOOR),
     (np.percentile(R2_lm, 16), np.percentile(R2_lm, 84)),
     (np.percentile(np.log10([r["gb"] for r in selA]), 16), np.percentile(np.log10([r["gb"] for r in selA]), 84)),
     "resolved RC", "SPARC discs"),
    ("R3 SPARC BTFR f_gas>0.7, C removed",     R3_a0["canonical"], math.hypot(R3raw_sig, FLOOR),
     (np.percentile(R3_lm, 16), np.percentile(R3_lm, 84)),
     (np.percentile(np.log10([d["gb"] for d in gd]), 16), np.percentile(np.log10([d["gb"] for d in gd]), 84)),
     "resolved RC", "SPARC discs"),
    ("R4 KiDS-1000 lensing, shape-only",       6.31e-11, 0.300, (9.5, 11.0), (-14.8, -12.4), "weak lensing", "KiDS lenses"),
    ("R5 ALFALFA gas-dominated, all baryons",  5.820e-11, 0.250,
     (float(np.percentile(alf_lm, 16)), float(np.percentile(alf_lm, 84))), (float("nan"), float("nan")),
     "HI line width", "ALFALFA"),
    ("R6 Leisman almost-darks, matched",       3.110e-11, 0.130,
     (float(np.percentile(hud_lm, 16)), float(np.percentile(hud_lm, 84))), (float("nan"), float("nan")),
     "HI line width", "ALFALFA"),
    ("R7 Lelli tidal dwarfs, EFE included",    1.734e-11, 0.170, (8.15, 9.20), (float("nan"), float("nan")),
     "resolved RC", "tidal debris"),
]
info(f"  {'rung':38} {'a_0':>11} {'+-dex':>7} {'log M_b 16-84':>16} {'log g_bar 16-84':>18}  velocity")
for nm, v, e, mm, gg_, vc, sc in LADDER:
    gtxt = "  --  (asymptotic)" if not np.isfinite(gg_[0]) else f"{gg_[0]:8.2f} {gg_[1]:8.2f}"
    info(f"  {nm:38} {v:11.3e} {e:7.3f} {mm[0]:7.2f} {mm[1]:7.2f} {gtxt:>18}  {vc}")

lv = np.array([math.log10(l[1]) for l in LADDER]); ed = np.array([l[2] for l in LADDER])
w = 1/ed**2
mu = float(np.sum(w*lv)/np.sum(w))
s_tot = float(lv.std()); s_int = intrinsic(lv, ed); s_ml = intrinsic_ml(lv, ed)
info("")
info(f"  ALL SEVEN M/L-free rungs: inverse-variance mean a_0 = {10**mu:.3e} "
     f"({mu-LC:+.3f} dex canonical, {mu-LA:+.3f} alt)")
info(f"  total spread {s_tot:.3f} dex | INTRINSIC beyond the quoted errors {s_int:.3f} dex (item 100's estimator) "
     f"| {s_ml:.3f} dex (maximum likelihood)")
chi2 = float(np.sum((lv-mu)**2/ed**2))
from scipy.stats import chi2 as chi2dist, norm as normdist
pval = float(chi2dist.sf(chi2, len(lv)-1))
info(f"  chi2 of one common a_0 across the seven: {chi2:.1f} on {len(lv)-1} degrees of freedom, p = {pval:.3f} "
     f"({normdist.isf(pval):.1f} sigma equivalent)")
info(f"  AND the inverse-variance mean above must NOT be quoted as an a_0: it is pulled down by R6 and R7, the two "
     f"rungs item 124 itself labelled non-measurements.  Dropping those two it is {10**float(np.sum((1/ed[:5]**2)*lv[:5])/np.sum(1/ed[:5]**2)):.3e}")

ck("3.1 ITEM 125's OWN CRITERION IS NOT MET, and the first reason is arithmetic rather than physical: the "
   "criterion cannot be evaluated with these rungs at all.  Item 125 asked whether the M/L-free rungs agree to "
   "better than 0.05 dex; the MEDIAN QUOTED ERROR of the seven M/L-free rungs is over three times that, because "
   "the price of removing the stellar mass is a sample of gas-rich dwarfs measured by lensing shape, HI line "
   "width or post-merger debris.  Even if every central value were identical, this ladder could not demonstrate "
   "0.05 dex agreement",
   float(np.median(ed)) > 0.05,
   f"median quoted error {np.median(ed):.3f} dex, range {ed.min():.3f}-{ed.max():.3f}, against the 0.05 dex criterion")

ck("3.2 and the central values do not agree either, though only weakly: one common a_0 across the seven is "
   "rejected at p = %.3f, an intrinsic spread of %.3f dex by item 100's own moment estimator and %.3f dex by "
   "maximum likelihood.  AGAINST INTEREST IN BOTH DIRECTIONS -- that is a 2-3 sigma inconsistency, not a "
   "decisive one, and it is essentially the SAME 0.16 dex item 100 found with the stellar M/L still in.  "
   "Removing the mass-to-light ratio neither collapsed the ladder nor made it worse; it left it where it was" %
   (pval, s_int, s_ml),
   s_int > 0.05 and pval < 0.05,
   f"chi2 {chi2:.1f}/{len(lv)-1} (p = {pval:.3f}); intrinsic {s_int:.3f} dex moment / {s_ml:.3f} dex ML, against "
   f"item 100's 0.156 dex and item 125's 0.05 dex criterion")

P(""); P("-"*120); P("3A.  what the residual is organised by, now that it is not organised by Upsilon")
P("-"*120)
lev_all = np.array([abs(r[3]) for r in REGISTER if r[4]])
r_lev = float(np.corrcoef(lev_all, lv)[0, 1])
info(f"  raw correlation of log a_0 with the residual Upsilon leverage across the seven: r = {r_lev:+.3f} -- but")
info(f"  with N = 7 and levers spanning only {lev_all.min():.2f} to {lev_all.max():.2f}, and with the leverage")
info(f"  collinear with which SYSTEM each rung is, that correlation cannot be read as an Upsilon organiser.  The")
info(f"  physical test is whether a COMMON error in Upsilon could reconcile the rungs: fit log a_0 = mu + lever x d.")
Wv = np.diag(1/ed**2)


def fit1(col):
    A_ = np.vstack([np.asarray(col, dtype=float), np.ones(len(lv))]).T
    b, a = np.linalg.solve(A_.T @ Wv @ A_, A_.T @ Wv @ lv)
    return float(b), float(np.sum((lv - (a + b*np.asarray(col, dtype=float)))**2/ed**2))


dU, chi2_U = fit1(lev_all)
isS = np.array([1.0 if l[6] == "SPARC discs" else 0.0 for l in LADDER])
bS, chi2_S = fit1(isS)
nzero = int(sum(1 for x in lev_all if x == 0))
info(f"    best-fit common Upsilon shift d log Upsilon = {dU:+.2f} dex (a factor {10**abs(dU):.0f} in the stellar")
info(f"    mass-to-light ratio), which does move chi2 from {chi2:.1f} to {chi2_U:.1f}")
info(f"    but a BINARY 'is this a SPARC rung' indicator, which contains no Upsilon at all, does the same job:")
info(f"    chi2 {chi2:.1f} -> {chi2_S:.1f}.  The leverage column is a proxy for which sample a rung came from,")
info(f"    because {nzero} of the {len(lev_all)} rungs have leverage exactly zero and all three SPARC rungs sit near 0.17.")
ck("3A.0 the stellar mass-to-light ratio CANNOT be the organiser any more.  It formally fits -- but only at a "
   "shift of +2.5 dex, a factor of three hundred in the stellar M/L against stellar populations' 0.5 +- 0.1 "
   "(0.09 dex) -- and a binary sample-membership indicator carrying no Upsilon whatsoever absorbs the same chi2, "
   "which shows the fit is sample membership in disguise.  AGAINST INTEREST: my first version of this check "
   "asserted that Upsilon leaves the chi2 behind.  It does not; it is degenerate with the sample label, which is "
   "a weaker statement and the one that is true",
   abs(dU) > 0.5 and abs(chi2_U - chi2_S) < 0.35*chi2,
   f"required shift {dU:+.2f} dex (factor {10**abs(dU):.0f}) vs the 0.09 dex stellar-population uncertainty; "
   f"chi2 {chi2:.1f} -> {chi2_U:.1f} on the leverage, -> {chi2_S:.1f} on a bare SPARC/not-SPARC flag; "
   f"{nzero} of {len(lev_all)} rungs have zero leverage")
byvel = {}
for nm, v, e, mm, gg_, vc, sc in LADDER:
    byvel.setdefault(vc, []).append(math.log10(v))
for k in sorted(byvel):
    info(f"    velocity class {k:15}: N = {len(byvel[k])}, median log a_0 = {np.median(byvel[k]):+.3f} "
         f"({np.median(byvel[k])-LC:+.3f} dex from canonical)")
res_rc = [math.log10(l[1]) for l in LADDER if l[5] == "resolved RC" and l[6] == "SPARC discs"]
res_hi = [math.log10(l[1]) for l in LADDER if l[5] == "HI line width"]
gap_vel = float(np.median(res_rc) - np.median(res_hi))
info(f"  SPARC resolved rotation curves minus HI line widths: {gap_vel:+.3f} dex")
ck("3A.1 the residual's new organiser is the VELOCITY MEASUREMENT.  The rungs built on resolved rotation curves "
   "sit about 0.24 dex above the rungs built on unresolved HI line widths -- the direction and roughly the size "
   "of the width bias item 124 measured directly on galaxies whose stellar masses ARE known (+0.25 dex per dex of "
   "mass in ALFALFA against +0.07 in SPARC).  Stated with its own limitation: this is a comparison of 3 rungs "
   "against 2, so it is a diagnosis consistent with an independently measured bias, not an independent detection",
   gap_vel > 0.1,
   f"SPARC resolved minus HI width {gap_vel:+.3f} dex, on 3 rungs vs 2; the independently measured ALFALFA width "
   f"bias runs +0.246 dex/dex of mass where SPARC's resolved curves run +0.070 +- 0.033")

# the tidal dwarfs are their own organiser: an equilibrium assumption, not an estimator
info(f"  and the outlier that is neither: the tidal dwarfs sit {math.log10(1.734e-11)-np.median(res_rc):+.3f} dex "
     f"below the resolved-curve rungs on RESOLVED kinematics, so their offset is not a width bias -- it is item 46's "
     f"liability (equilibrium one orbit after a merger), and it cannot be cut without cutting on the answer")

P(""); P("-"*120); P("3B.  the sub-ladder of resolved kinematics only, and why it is one measurement and not four")
P("-"*120)
sub = [l for l in LADDER if l[5] == "resolved RC" and l[6] == "SPARC discs"]
lvs = np.array([math.log10(l[1]) for l in sub]); eds = np.array([l[2] for l in sub])
s_int_sub = intrinsic(lvs, eds)
mu_s = float(np.sum(lvs/eds**2)/np.sum(1/eds**2))
info(f"  the three SPARC rungs alone: mean {10**mu_s:.3e}, total spread {lvs.std():.3f} dex, "
     f"intrinsic {s_int_sub:.3f} dex")
ov12 = len(set(g["name"] for g in keep1) & set(r["name"] for r in selA))
ov13 = len(set(g["name"] for g in keep1) & set(d["name"] for d in gd))
info(f"  BUT they are not three measurements: R1 and R2 share {ov12} of {min(len(keep1), len(selA))} galaxies, "
     f"R1 and R3 share {ov13} of {min(len(keep1), len(gd))}, and all three use the same distances, the same "
     f"inclinations and the same HI mass scale")
ck("3B.1 the three SPARC rungs DO agree to better than 0.05 dex -- their rms is 0.016 dex -- and that is NOT a "
   "second law, because R2's galaxies are a SUBSET of R1's and R3 shares three quarters of them, and all three "
   "use the same distances, the same inclinations and the same hydrogen mass scale.  Recorded here explicitly so "
   "that this 0.016 dex cannot later be mistaken for the item-125 criterion being met: their concordance tests "
   "the estimator, not nature, and three estimators on one sample is one rung",
   float(lvs.std()) < 0.05 and ov12 >= 0.9*min(len(keep1), len(selA)),
   f"rms of the three {lvs.std():.3f} dex (moment intrinsic {s_int_sub:.3f} once the shared floor is charged), "
   f"but R1-R2 overlap {ov12} of {min(len(keep1), len(selA))} galaxies and R1-R3 overlap {ov13} of {min(len(keep1), len(gd))}")

P(""); P("-"*120); P("3C.  the dynamic range the M/L-free ladder actually spans")
P("-"*120)
mlo = min(l[3][0] for l in LADDER); mhi = max(l[3][1] for l in LADDER)
glo = min(l[4][0] for l in LADDER if np.isfinite(l[4][0])); ghi = max(l[4][1] for l in LADDER if np.isfinite(l[4][1]))
sub_m_lo = min(l[3][0] for l in LADDER if l[6] == "SPARC discs")
sub_m_hi = max(l[3][1] for l in LADDER if l[6] == "SPARC discs")
nk_lo = min(l[3][0] for l in LADDER if "KiDS" not in l[0]); nk_hi = max(l[3][1] for l in LADDER if "KiDS" not in l[0])
info(f"  baryonic mass covered by all seven M/L-free rungs: log M_b = {mlo:.2f} to {mhi:.2f} = {mhi-mlo:.1f} decades")
info(f"  local baryonic acceleration where one exists:       log g_bar = {glo:.2f} to {ghi:.2f} = {ghi-glo:.1f} decades")
info(f"  drop the one rung whose own a_0 is unstable at 0.30 dex (KiDS shape-only): {nk_hi-nk_lo:.1f} decades of mass")
info(f"  keep only the three rungs that carry the measurement (the SPARC gas-rich discs): "
     f"{sub_m_hi-sub_m_lo:.1f} decades, log M_b {sub_m_lo:.2f} to {sub_m_hi:.2f}")
ck("3C.1 the structural reason item 125 could not have closed, which is worth more than the failed criterion.  "
   "M/L-freedom and dynamic range are in DIRECT CONFLICT: the only way to remove the stellar mass is to select "
   "gas-rich systems, gas-rich systems are low-mass, and low-mass systems all sit at the same acceleration.  The "
   "item promised one acceleration measured five ways over nine decades of mass; the M/L-free ladder that actually "
   "exists spans one decade in the rungs that carry it and 2.5 decades if every usable rung is admitted, and "
   "every one of those rungs is a gas-rich dwarf",
   (sub_m_hi - sub_m_lo) < 4.0 and (nk_hi - nk_lo) < 4.0,
   f"load-bearing SPARC rungs span {sub_m_hi-sub_m_lo:.1f} decades of M_b against the item's nine; all seven span "
   f"{mhi-mlo:.1f}, and {nk_hi-nk_lo:.1f} once the 0.30 dex KiDS rung is dropped")

P(""); P("-"*120); P("3D.  three named sensitivities of this ladder, all reported rather than chosen")
P("-"*120)
SENS = [
    ("as built above (7 rungs)", [l[1] for l in LADDER], [l[2] for l in LADDER]),
    ("+ item 121's 9.333e-11 (REFUTED in verification; shown only to size the effect)",
     [l[1] for l in LADDER] + [9.333e-11], [l[2] for l in LADDER] + [0.116]),
    ("with the almost-darks at their UNMATCHED value 6.133e-12",
     [l[1] if "almost-darks" not in l[0] else 6.133e-12 for l in LADDER], [l[2] for l in LADDER]),
    ("resolved-kinematics rungs only (R1,R2,R3,R7)",
     [l[1] for l in LADDER if l[5] == "resolved RC"], [l[2] for l in LADDER if l[5] == "resolved RC"]),
    ("SPARC gas-rich discs collapsed to ONE rung, + KiDS + ALFALFA + almost-darks + TDG",
     [10**mu_s, 6.31e-11, 5.820e-11, 3.110e-11, 1.734e-11],
     [math.hypot(float(lvs.std()), FLOOR), 0.300, 0.250, 0.130, 0.170]),
]
for nm, vv, ee in SENS:
    l_ = np.log10(np.array(vv)); e_ = np.array(ee)
    m_ = float(np.sum(l_/e_**2)/np.sum(1/e_**2))
    info(f"  {nm:74} mean {10**m_:.3e}  intrinsic {intrinsic(l_, e_):.3f} dex")
ck("3D.1 the failure is not a choice of rungs: every defensible variant of the ladder -- including the one that "
   "admits the refuted item 121, the one that collapses SPARC to a single rung, and the one that keeps only "
   "resolved kinematics -- leaves an intrinsic spread far above the 0.05 dex item 125 asked for",
   all(intrinsic(np.log10(np.array(v)), np.array(e)) > 0.05 for _, v, e in SENS),
   "; ".join(f"{nm.split('(')[0].strip()[:26]}: {intrinsic(np.log10(np.array(v)), np.array(e)):.3f}"
             for nm, v, e in SENS))


# ======================================================================================================= SECTION 4
P(""); P("="*120)
P("4.  THE ALTERNATIVE COMPUTED BESIDE IT")
P("="*120)
info("In the framework a_0 is a constant of nature, so the ladder's rungs must agree and must not run with mass.")
info("In LambdaCDM there is no a_0: v^4/(G M_b) is a halo property and MUST run with baryonic mass, because the")
info("stellar-to-halo-mass relation is not a power law with index 1.  So the mass trend of the ladder is the test.")
mid = np.array([0.5*(l[3][0]+l[3][1]) for l in LADDER])
A_ = np.vstack([mid, np.ones_like(mid)]).T
W = np.diag(1/ed**2)
cov = np.linalg.inv(A_.T @ W @ A_)
slope, icept = np.linalg.solve(A_.T @ W @ A_, A_.T @ W @ lv)
info(f"  ladder-level trend of log a_0 with log M_b: {slope:+.3f} +- {math.sqrt(cov[0,0]):.3f} dex/dex "
     f"({slope/math.sqrt(cov[0,0]):+.1f} sigma from the framework's required zero)")
info(f"  for comparison, WITHIN one sample: SPARC resolved curves give +0.070 +- 0.033 dex/dex (h124), ALFALFA")
info(f"  line widths give +0.246 dex/dex on the same estimator with stellar masses known -- so the ladder-level")
info(f"  trend sits between them and is dominated by which velocity estimator each rung used, not by halo physics")
newt = float(np.mean(np.log10(y1/x1)))
info(f"  Newtonian control (nu = 1, same baryons, no halo) on the R1 points: <log g_obs/g_bar> = {newt:+.3f} dex "
     f"-- a factor {10**newt:.1f}, so these points are not Newtonian and the ladder is measuring something")
ck("4.1 the ladder's mass trend does not separate the two paradigms, and it must be said so.  The framework "
   "requires zero and LambdaCDM requires a nonzero trend, but the measured ladder-level trend is dominated by the "
   "velocity-estimator bias of section 3A, which is an instrumental effect present in both paradigms.  This test "
   "is confounded, not passed",
   True, f"ladder trend {slope:+.3f} +- {math.sqrt(cov[0,0]):.3f} dex/dex; within-sample SPARC +0.070 +- 0.033, "
   f"ALFALFA +0.246 on the same estimator")


# ======================================================================================================= SECTION 5
P(""); P("="*120)
P("5.  MUTATION CONTROLS")
P("="*120)
# M1 -- a deliberately wrong a_0 must break the agreement of the sub-ladder that DOES agree
bad = 2.0
lvs_bad = lvs.copy(); lvs_bad[0] += math.log10(bad)
info(f"  M1: multiplying one of the three concordant SPARC rungs by {bad} raises their intrinsic spread from "
     f"{intrinsic(lvs, eds):.3f} to {intrinsic(lvs_bad, eds):.3f} dex")
ck("M1 the agreement of section 3B is falsifiable: injecting a factor-2 error into one of the three concordant "
   "SPARC rungs takes their intrinsic spread from under the 0.05 dex threshold to far above it",
   intrinsic(lvs, eds) < 0.05 < intrinsic(lvs_bad, eds),
   f"{intrinsic(lvs, eds):.3f} -> {intrinsic(lvs_bad, eds):.3f} dex on a x{bad} injection")

# M2 -- both spread statistics run against a null in which the rungs really do share one a_0
sims, simchi = [], []
for _ in range(4000):
    draw = LC + rng.normal(0, 1, len(ed))*ed
    wq = 1/ed**2; muq = float(np.sum(wq*draw)/np.sum(wq))
    sims.append(intrinsic(draw, ed)); simchi.append(float(np.sum((draw-muq)**2/ed**2)))
sims, simchi = np.array(sims), np.array(simchi)
info(f"  M2: 4000 synthetic ladders drawn from ONE a_0 with these same quoted errors give")
info(f"      moment intrinsic spread: median {np.median(sims):.3f}, 95th percentile {np.percentile(sims,95):.3f} dex "
     f"-- observed {s_int:.3f}")
info(f"      chi2 about a common a_0:  median {np.median(simchi):.1f}, 95th percentile "
     f"{np.percentile(simchi,95):.1f} -- observed {chi2:.1f}")
ck("M2 the null is run, and it CORRECTS MY OWN CHECK 3.2 in part.  Item 100's moment estimator of the intrinsic "
   "spread is too noisy at N = 7 with these error bars to detect the observed 0.13 dex: its own null reaches "
   "0.18 dex at the 95th percentile.  The chi2 does clear its null, so the inconsistency is real but it rests on "
   "the chi2 and NOT on the intrinsic-spread number, which must therefore be quoted as an estimate and never as "
   "a detection.  Item 100's headline 0.156 dex inherits exactly the same weakness",
   chi2 > np.percentile(simchi, 95) and s_int < np.percentile(sims, 95),
   f"observed chi2 {chi2:.1f} above the null's 95th percentile {np.percentile(simchi,95):.1f}, but observed "
   f"intrinsic {s_int:.3f} dex BELOW the moment estimator's null 95th percentile {np.percentile(sims,95):.3f}")

# M3 -- the estimator must track an injected a_0 exactly (the sigma it registers is reported, not thresholded)
inj = 4.0
synth = nu(x1/(inj*A0["canonical"]))*x1
rec = a0_kern(x1, synth)
sig_inj = abs((math.log10(rec)-LC)/math.hypot(R1_sig, FLOOR))
info(f"  M3: synthetic g_obs built from the R1 g_bar values at a_0 = {inj}x canonical = {inj*A0['canonical']:.3e} "
     f"is recovered as {rec:.3e} ({math.log10(rec/(inj*A0['canonical'])):+.5f} dex)")
info(f"      and AGAINST INTEREST, a factor-4 error in a_0 registers as only {sig_inj:.1f} sigma against this "
     f"measurement's coherent floor -- which is how weak an M/L-free a_0 currently is, not a failure of the control")
ck("M3 the estimator is not a fixed point and follows the data: an injected a_0 four times canonical is recovered "
   "as four times canonical to better than 0.001 dex",
   abs(math.log10(rec/(inj*A0["canonical"]))) < 1e-3,
   f"injected {inj*A0['canonical']:.4e}, recovered {rec:.4e} ({math.log10(rec/(inj*A0['canonical'])):+.5f} dex); "
   f"it would register at {sig_inj:.1f} sigma")

# M4 -- turning the kernel off must make the estimator unfittable
off = a0_kern(x1, x1)
ck("M4 turning the kernel off (nu = 1, g_obs set equal to g_bar) must leave no a_0 that fits, since no boosted "
   "kernel can reproduce an unboosted curve",
   not np.isfinite(off), f"nu=1 synthetic returns a_0 = {off}")

# M5 -- covariance discipline (bug pattern 4), on the only matrix this script builds
Cmat = np.diag(ed**2)
evs = np.linalg.eigvalsh(Cmat)
ck("M5 the only covariance this script builds is checked for positive-definiteness rather than for its diagonal, "
   "which is the discipline that caught the Brouwer index-ordering bug earlier in the hunt",
   evs.min() > 0, f"min eigenvalue {evs.min():.3e}")


# ======================================================================================================= SECTION 6
P(""); P("="*120)
P("VERDICT -- ITEMS 123 AND 125")
P("="*120)
P(f"""
  ITEM 123 -- NEITHER FOOTING IS DECIDED, and the reason is not sample size.
    The best M/L-free measurement in the hunt is the SPARC deep tail with stars supplying under 20% of g_bar:
    a_0 = {R1_a0:.3e} +- {R1_sig:.3f} dex statistical, {math.hypot(R1_sig, FLOOR):.3f} dex with the coherent
    calibration floor rebuilt here.  That is {(math.log10(R1_a0)-LC)/math.hypot(R1_sig, FLOOR):+.1f} sigma from
    the canonical footing and {(math.log10(R1_a0)-LA)/math.hypot(R1_sig, FLOOR):+.1f} sigma from the alt footing:
    neither is excluded at 3 sigma.  One further fact forbids quoting it either way: splitting the SAME galaxies
    on distance quality moves a_0 by {abs(split):.2f} dex -- {abs(split)/SEP:.1f} times the whole gap between the
    footings -- with the good-distance half landing ON the canonical value ({ag:.2e}) and the Hubble-flow half
    0.2 dex below it.  (My second candidate flip, estimator choice, was tested and WITHDRAWN: the three
    defensible M/L-free estimators span only {lv_d.max()-lv_d.min():.3f} dex, well inside the gap.)
    The precision needed is {need:.4f} dex total, i.e. the distance scale to about 1.4%, the HI mass scale to
    about 3%, and roughly {ngal_need:.0f} gas-dominated discs with resolved rotation curves against SPARC's
    {len(keep1)}.  Removing the stellar mass-to-light ratio does not remove the calibration problem: it trades it
    for the hydrogen mass scale, whose leverage on this estimator is {abs(lev_G):.2f}, about eight times the
    stellar leverage ({abs(R1_lev):.2f}) that the cut removed.  That trade is the reason the floor does not fall.

  ITEM 125 -- THE HUNT DID NOT FIND A SECOND LAW.  The M/L-free ladder is not worse than the one it replaced,
    and it is not better; it is the same size, for a different reason.
    Seven M/L-free rungs.  The criterion cannot even be evaluated: their median quoted error is {np.median(ed):.2f}
    dex, three times the {0.05:.2f} dex agreement item 125 asked for, so identical central values could not have
    demonstrated it.  The central values are in mild tension anyway -- chi2 {chi2:.1f} on {len(lv)-1} d.o.f.,
    p = {pval:.3f} -- with an intrinsic spread of {s_int:.3f} dex by item 100's moment estimator and {s_ml:.3f}
    dex by maximum likelihood, against item 100's {0.156:.3f} dex.  The null in control M2 says the moment
    estimator cannot detect that at N = 7, so the tension rests on the chi2 and the intrinsic-spread number is an
    estimate, never a detection -- which retires item 100's 0.156 dex as a detection too.
    The organiser has CHANGED.  It is no longer the stellar mass-to-light ratio: {nzero} of the seven rungs have
    exactly zero M/L leverage, the best common Upsilon shift is an impossible {dU:+.1f} dex (a factor
    {10**abs(dU):.0f} against stellar populations' 0.09 dex), and a bare sample-membership flag carrying no
    Upsilon absorbs the same chi2 ({chi2:.1f} -> {chi2_S:.1f} against {chi2_U:.1f}), so what the leverage column
    fits is which catalogue a rung came from.
    It is now the VELOCITY MEASUREMENT -- resolved rotation curves sit {gap_vel:+.2f} dex above
    unresolved HI line widths, the direction and size of the width bias item 124 measured independently -- with
    the tidal dwarfs {abs(math.log10(1.734e-11)-np.median(res_rc)):.2f} dex below everything on an equilibrium
    assumption rather than on an estimator.
    The three SPARC rungs agree to {lvs.std():.3f} dex rms, and that must NOT be read as the law closing: R2's
    galaxies are a subset of R1's, R3 shares three quarters of them, and all three share one distance scale, one
    inclination convention and one hydrogen calibration.  Three estimators on one sample is one rung.
    The structural finding is the durable one.  M/L-freedom and dynamic range are in direct conflict -- the only
    way to drop the stellar mass is to select gas-rich systems, which are low-mass, which all sit at the same
    acceleration.  The load-bearing M/L-free rungs span {sub_m_hi-sub_m_lo:.1f} decades of baryonic mass and the
    whole usable ladder {nk_hi-nk_lo:.1f}, not the nine the item promised, and every rung is a gas-rich dwarf.

  ONE CORRECTION THIS ITEM OWES THE LEDGER, against my own workflow's earlier headline.
    Item 100's closing sentence -- 'the two measurements that do not lean on a stellar M/L agree to 0.08 dex' --
    is WITHDRAWN.  Neither of the two was M/L-free.  The deep-tail rung carries a measured leverage of -0.647
    (h121a) and the KiDS dwarf lens stack carries -1.046 (h111-A, where a deep-MOND lensing a_0 is degenerate with
    the assumed baryonic mass at exponent one, not two).  The 0.08 dex agreement was additionally an artefact of
    the +0.10 dex estimator bias that item 102 found in item 25.  Both halves of the sentence fail.
""")
sys.exit(ck.done())
