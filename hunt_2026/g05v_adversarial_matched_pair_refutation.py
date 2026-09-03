#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_adversarial_matched_pair_refutation.py
==========================================================================================================
ADVERSARIAL VERIFICATION of the headline of g05_dsph_prescription_fixed_and_expanded.py.

THE CLAIM UNDER ATTACK.  "f09's matched-pair separation is WITHDRAWN: with object-by-object acceleration
matching against the SPARC relation it falls from +0.215 dex to +0.064 dex and from 1.73 sigma to 0.93
sigma; permutation p = 0.1033; N_pressure = 14 matched (36 dropped as outside SPARC's range) against
N_rotating = 147."

This is a NEGATIVE claim -- a withdrawal.  The repository's working rule says a deficit must be verified as
hard as a win, and the symmetric failure mode for a withdrawal is a MANUFACTURED NULL: an analysis choice
that destroys a real separation rather than a data statement that there is none.  So the attack lines are:

  V1  Is the DROP CRITERION honest?  36 of 50 pressure objects are discarded for having fewer than
      MATCH_N = 20 SPARC points within MATCH_W = 0.20 dex.  Exactly four of f09's own eight classical
      dwarfs (Draco, Carina, Ursa Minor, Sextans) are among the discarded -- and they are the four with the
      LARGEST residuals.  Count the SPARC points at each dropped object's x_i directly.  If SPARC has
      plenty of points there, the threshold, not the data, killed the result.

  V2  Is MATCH_N = 20 load-bearing?  g05's own sensitivity scan (A9) moves the WINDOW w and n together and
      never scans n alone at w = 0.20.  Scan n alone.

  V3  Is the surviving matched sample even capable of showing the effect?  Of the 14 kept objects, five
      (M 32 at x_i = 29.7, NGC 205 at 1.43, NGC 185 at 0.52, NGC 147 at 0.27, and arguably Leo I at 0.073)
      sit at or above the MOND transition, where NO version of the fork predicts anything: Milgrom's
      modified-inertia/modified-gravity theorem is a DEEP-MOND statement.  Loading a "matched pressure
      sample" with near-Newtonian dwarf ellipticals dilutes any deep-MOND signal by construction.  Restrict
      to x_i < 1, < 0.3, < 0.1 and see whether the null holds.

  V4  Is the reported SIGMA right?  compare() forms se = sqrt(s_p^2/n_p + s_r^2/n_r) -- the standard error
      of a MEAN -- but the statistic is a difference of MEDIANS.  For a Gaussian the SE of a median is
      1.2533/sqrt(N) times sigma, so the quoted sigma is INFLATED by ~25 per cent.  Recompute by bootstrap.
      Note also that the quoted "0.93 sigma" and the quoted permutation p = 0.1033 are not the same
      statement: p = 0.1033 two-sided is z = 1.63.  Which number should a referee quote?

  V5  THE SELECTION-ON-THE-OUTCOME OBJECTION, which is the one that matters.  g05's own check A1c reports
      that the pressure sample's residual runs with log10(x_i) at slope -0.498, and explains why: in deep
      MOND residual = log10(g_obs) - 0.5 log10(x_i) - log10(a_0), so a slope of -1/2 is what you get if
      g_obs carries no x_i dependence at all.  If that is so, then CUTTING ON x_i IS CUTTING ON THE
      RESIDUAL.  Selecting the 14 highest-x_i objects is arithmetically the same operation as selecting the
      14 lowest-residual objects.  This repository's own bug list names exactly this pattern: "a residual
      whose sign tracks a branch of your own prescription rather than the data."  Test it: is the kept-set
      median predictable from the x_i cut alone, with the residuals REPLACED by the -0.5 line?

  V6  MUTATION CONTROL and BOTH FOOTINGS throughout.

Nothing here is a new physical measurement.  This file only asks whether g05's number is what g05 says it is.
"""
import sys, math, csv, os
import numpy as np
from scipy.special import erfcinv
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)

MW_MB, M31_MB = 6.0e10, 1.2e11
UPS_V = 2.0
PC = 3.0857e16

# ---------------------------------------------------------------------------------------------------------
# Re-implement g05's pipeline from its own definitions so the numbers are recomputed, not imported.
# ---------------------------------------------------------------------------------------------------------
def g_qumond_sphere(x_i, x_e, ntheta=2001):
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    th = np.linspace(0.0, math.pi, ntheta)
    st, ctm = np.sin(th), np.cos(th)
    gx = -x_i*st
    gz = x_e - x_i*ctm
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*ctm)
    return -float(np.trapz(Sr*st, th)/np.trapz(st, th))

def fnum(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def load_lvd(fname, host_mb, host_name):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fname))):
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
        MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
        if fnum(r["confirmed_galaxy"]) != 1: continue
        lMs = fnum(r["mass_stellar"]); lMHI = fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, rh=rh, sig=sig,
                        Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
                        MHI=(10**lMHI if lMHI is not None else 0.0),
                        Dhost=Dh, Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                        host=host_name, host_mb=host_mb))
    return out

mw_all  = load_lvd("lvd_dwarf_mw.csv",  MW_MB,  "MW")
m31_all = load_lvd("lvd_dwarf_m31.csv", M31_MB, "M31")
fld_all = load_lvd("lvd_dwarf_local_field.csv", None, "field")

ROTATING_EXCLUDE = {"LMC", "SMC"}
DISRUPTING       = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
GAS_RATIO_MAX    = 0.3

def classify(d, host):
    if d["name"] in ROTATING_EXCLUDE: return None
    if d["name"] in DISRUPTING:       return None
    if d["MHI"] > GAS_RATIO_MAX*d["Ms"]: return None
    if host == "field":               return "isolated"
    if host == "M31":                 return "m31"
    return "classical" if d["MV"] <= -7.7 else "ultrafaint"

classes = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
for src, host in ((mw_all, "MW"), (m31_all, "M31"), (fld_all, "field")):
    for d in src:
        c = classify(d, host)
        if c: classes[c].append(d)

def dsph_row(d, a0, ups=UPS_V):
    r12 = (4.0/3.0)*d["rh"]*PC
    Mb = (ups/UPS_V)*d["Ms"] + 1.33*d["MHI"]
    x_i = G*(0.5*Mb*Msun)/r12**2/a0
    hm = d["host_mb"]
    if hm is not None and d["Dhost"] and d["Dhost"] > 0:
        x_e = G*hm*Msun/(d["Dhost"]*kpc)**2/a0
    else:
        gg = (G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0) + \
             (G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0)
        x_e = gg/a0
    g_obs = 3.0*(d["sig"]*1e3)**2/r12
    gp = g_qumond_sphere(x_i, x_e)*a0
    return math.log10(g_obs/gp), x_i, x_e

gals = load_sparc()
KEYS = ("classical", "m31", "isolated")

_POOL = {}
def build_pool(a0, drop_name=None):
    key = (a0, drop_name)
    if key in _POOL: return _POOL[key]
    ly, rr = [], []
    for g in gals:
        if g["name"] == drop_name: continue
        y = g["gbar"]/a0
        ly.append(np.log10(y)); rr.append(np.log10(g["gobs"]/(nu(y)*g["gbar"])))
    _POOL[key] = (np.concatenate(ly), np.concatenate(rr))
    return _POOL[key]

def ctrl(lx, ly, rr, w, nmin):
    m = np.abs(ly - lx) < w
    return (float(np.median(rr[m])), int(m.sum())) if m.sum() >= nmin else (None, int(m.sum()))

_RC = {}
def rotating_deltas(a0, w, nmin):
    key = (a0, w, nmin)
    if key in _RC: return _RC[key]
    rot = []
    for g in gals:
        y = g["gbar"]/a0
        rj = float(np.median(np.log10(g["gobs"]/(nu(y)*g["gbar"]))))
        lyj, rrj = build_pool(a0, drop_name=g["name"])
        c, n = ctrl(float(np.median(np.log10(y))), lyj, rrj, w, nmin)
        if c is not None: rot.append((g["name"], rj - c))
    _RC[key] = rot
    return rot

def matched(rows, a0, w=0.20, nmin=20):
    LY, RR = build_pool(a0)
    pres, oor = [], []
    for nm, r, xi in rows:
        c, n = ctrl(math.log10(xi), LY, RR, w, nmin)
        (pres.append((nm, r - c, xi, r, c)) if c is not None else oor.append((nm, xi, n, r)))
    return pres, rotating_deltas(a0, w, nmin), oor

def compare(pres, rot, nperm=20000):
    p = np.array([t[1] for t in pres]); r = np.array([t[1] for t in rot])
    sep = float(np.median(p) - np.median(r))
    se = math.sqrt(p.std(ddof=1)**2/len(p) + r.std(ddof=1)**2/len(r))
    pool = np.concatenate([p, r]); n1 = len(p)
    cnt = sum(1 for _ in range(nperm)
              if abs(np.median((q := rng.permutation(pool))[:n1]) - np.median(q[n1:])) >= abs(sep))
    return dict(sep=sep, nsig=sep/se, p=(cnt+1)/(nperm+1), np_=len(p), nr=len(r),
                mp=float(np.median(p)), mr=float(np.median(r)),
                sp=float(p.std(ddof=1)), sr=float(r.std(ddof=1)), parr=p, rarr=r)

a0c = A0["canonical"]
allrows = {a0: [(d["name"],) + dsph_row(d, a0)[:2] for k in KEYS for d in classes[k]] for a0 in A0.values()}

P("="*120)
P("PART 0.  INDEPENDENT RECOMPUTATION OF THE HEADLINE NUMBER.")
P("="*120)
rep = {}
for foot, a0 in A0.items():
    pres, rot, oor = matched(allrows[a0], a0)
    o = compare(pres, rot); rep[foot] = (o, oor, pres)
    info(f"{foot:10}: sep {o['sep']:+.4f} dex, {o['nsig']:.3f} sigma, perm p = {o['p']:.4f}, "
         f"N_pres = {o['np_']} kept / {len(oor)} dropped, N_rot = {o['nr']}, rot median {o['mr']:+.4f}")
c_all = rep["canonical"][0]; a_all = rep["alt"][0]
ck("V0 the headline numbers reproduce independently from the LVD and SPARC files: +0.064 dex / 0.93 sigma / "
   "p = 0.103 canonical, +0.065 / 0.94 alt, 14 kept against 36 dropped, 147 rotating.  The arithmetic of the "
   "claim is not in dispute; only its meaning is",
   abs(c_all["sep"] - 0.064) < 0.005 and abs(c_all["nsig"] - 0.93) < 0.05 and c_all["np_"] == 14
   and len(rep["canonical"][1]) == 36 and c_all["nr"] == 147 and abs(a_all["sep"] - 0.065) < 0.005,
   f"canonical {c_all['sep']:+.4f} dex / {c_all['nsig']:.2f} sigma / p={c_all['p']:.4f}; "
   f"alt {a_all['sep']:+.4f} / {a_all['nsig']:.2f}; kept {c_all['np_']}, dropped {len(rep['canonical'][1])}")

# =========================================================================================================
P(""); P("="*120)
P("V1.  IS THE DROP CRITERION HONEST?  Direct SPARC point counts at each dropped object's acceleration.")
P("="*120)
LY, RR = build_pool(a0c)
info(f"SPARC pooled points: {len(LY)}; log10(g_bar/a_0) spans {LY.min():+.3f} to {LY.max():+.3f} "
     f"(g_bar/a_0 = {10**LY.min():.5f} to {10**LY.max():.1f})")
for q in (0.1, 0.5, 1.0, 2.0, 5.0):
    info(f"   fraction of SPARC points below g_bar/a_0 = {10**np.percentile(LY,q):.5f} is {q} per cent")
F09_EIGHT = ["Draco", "Sculptor", "Fornax", "Carina", "Sextans", "Leo I", "Leo II", "Ursa Minor"]
P("")
info("f09's OWN EIGHT, each with the number of SPARC points inside +-0.20 dex of its internal acceleration:")
info(f"   {'dwarf':13} {'x_i':>9} {'SPARC pts':>10} {'kept?':>7} {'raw resid':>10}")
eight = []
for nm in F09_EIGHT:
    d = [x for x in classes["classical"] if x["name"] == nm][0]
    r, xi, _ = dsph_row(d, a0c)
    _, n = ctrl(math.log10(xi), LY, RR, 0.20, 20)
    eight.append((nm, xi, n, r))
    info(f"   {nm:13} {xi:9.5f} {n:10d} {'YES' if n >= 20 else 'no':>7} {r:+10.3f}")
kept8 = [t for t in eight if t[2] >= 20]; drop8 = [t for t in eight if t[2] < 20]
info(f"   kept {len(kept8)} of 8, median raw residual {np.median([t[3] for t in kept8]):+.3f} dex; "
     f"dropped {len(drop8)}, median raw residual {np.median([t[3] for t in drop8]):+.3f} dex")
ck("V1a (FAILS -- AND THIS IS THE FIRST HALF OF THE REFUTATION) TESTED PROPOSITION: the four of f09's eight "
   "that g05 discards are discarded because SPARC has essentially NO data at their internal accelerations, "
   "so a bar of 5 points, or 1, would still drop them.  IT IS FALSE.  SPARC has 12 points within 0.20 dex of "
   "Draco and 12 of Carina.  They are not outside SPARC's range -- SPARC runs down to g_bar/a_0 = "
   "0.0022, three times deeper than Draco -- they are in a thinly sampled part of it, and it is the "
   "UNDISCLOSED 20-point bar, not SPARC's coverage, that removes them",
   max(t[2] for t in drop8) <= 5,
   "dropped: " + ", ".join(f"{t[0]} x_i={t[1]:.5f} -> {t[2]} SPARC points" for t in drop8) +
   "; kept: " + ", ".join(f"{t[0]} {t[2]}" for t in kept8) +
   f".  SPARC's own floor is g_bar/a_0 = {10**LY.min():.5f}, deeper than three of the four dropped objects")

alldrop = rep["canonical"][1]
maxn = max(t[2] for t in alldrop)
nz = sum(1 for t in alldrop if t[2] == 0)
ck("V1b (FAILS) TESTED PROPOSITION: the same holds for the whole dropped set -- the great majority of the 36 "
   "discarded objects have ZERO SPARC points in the window and none has more than a handful.  IT IS FALSE.  "
   "Only 10 of 36 have zero.  The largest count among the dropped is 19 -- ONE POINT below the bar of 20.  A "
   "threshold sitting one unit above the top of the distribution it cuts is the single most fragile place it "
   "could have been put, and g05's own sensitivity scan never tests below it",
   maxn <= 8 and nz >= 25,
   f"{nz} of {len(alldrop)} dropped objects have 0 SPARC points in window; the largest count among all "
   f"dropped objects is {maxn} (bar is 20).  So {len(alldrop)-nz} of the 36 are inside SPARC's sampled range and are "
   f"removed by the threshold, not by the data.  The claim's phrase 'dropped as outside SPARC's range' is "
   f"accurate for {nz} of them and inaccurate for {len(alldrop)-nz}")

# =========================================================================================================
P(""); P("="*120)
P("V2.  IS MATCH_N LOAD-BEARING?  g05's A9 scan moves w and n TOGETHER and never scans n alone at w = 0.20.")
P("="*120)
info(f"{'w':>6} {'n_min':>7} {'N kept':>7} {'N rot':>6} {'sep dex':>9} {'sigma':>7} {'perm p':>8}")
n_scan = {}
for nmin in (1, 3, 5, 10, 20, 40, 80):
    pres, rot, oor = matched(allrows[a0c], a0c, w=0.20, nmin=nmin)
    o = compare(pres, rot, nperm=4000); n_scan[nmin] = o
    info(f"{0.20:6.2f} {nmin:7d} {o['np_']:7d} {o['nr']:6d} {o['sep']:+9.3f} {o['nsig']:7.2f} {o['p']:8.4f}")
ck("V2 (FAILS -- THIS IS THE REFUTATION) TESTED PROPOSITION: the minimum-point bar is not what produces the "
   "null, so scanning it alone at fixed window width leaves the separation under two sigma.  IT IS FALSE, "
   "and by a wide margin.  Holding the window at g05's own 0.20 dex and moving ONLY the point bar, the "
   "separation runs from -0.03 dex at n >= 80 to +0.214 dex at n >= 1 -- and at n >= 5, where the local SPARC "
   "relation is still estimated from five real points, it is +0.202 dex at 2.96 sigma, p = 0.0002.  That "
   "REPRODUCES f09's +0.215 dex at higher significance than f09 claimed.  The headline 0.93 sigma is the "
   "value at one particular setting of an undisclosed knob, and g05's published sensitivity table (A9) scans "
   "n only at 20, 30 and 50 -- never below 20, which is the entire region where the result returns",
   max(o["nsig"] for o in n_scan.values()) < 2.0 and abs(n_scan[1]["np_"] - n_scan[20]["np_"]) <= 4,
   "; ".join(f"n>={k}: N={n_scan[k]['np_']}, {n_scan[k]['sep']:+.3f} dex ({n_scan[k]['nsig']:.2f} sigma, p={n_scan[k]['p']:.4f})"
             for k in (1, 3, 5, 10, 20, 40, 80)))

P(""); info("THE SAME SCAN ON THE ALT FOOTING, because one footing is not a scan:")
info(f"{'w':>6} {'n_min':>7} {'N kept':>7} {'sep dex':>9} {'sigma':>7} {'perm p':>8}")
n_scan_alt = {}
a0a = A0["alt"]
for nmin in (1, 5, 20, 80):
    pres, rot, oor = matched(allrows[a0a], a0a, w=0.20, nmin=nmin)
    o = compare(pres, rot, nperm=4000); n_scan_alt[nmin] = o
    info(f"{0.20:6.2f} {nmin:7d} {o['np_']:7d} {o['sep']:+9.3f} {o['nsig']:7.2f} {o['p']:8.4f}")
ck("V2b (FAILS on both footings, so it is not an a_0 artefact) TESTED PROPOSITION: the point-bar sensitivity "
   "is peculiar to the canonical footing.  IT IS FALSE -- the alt footing behaves identically, which is the "
   "point: a_0 is not what sets this number, the undisclosed threshold is",
   max(o["nsig"] for o in n_scan_alt.values()) < 2.0,
   "; ".join(f"n>={k}: {n_scan_alt[k]['sep']:+.3f} dex ({n_scan_alt[k]['nsig']:.2f} sigma, N={n_scan_alt[k]['np_']})"
             for k in (1, 5, 20, 80)))

P(""); P("-"*120)
P("V2c.  THE FAIRNESS CHECK I OWE THE AUTHOR: is a 12-point window really 12 INDEPENDENT comparisons,")
P("      or is it one galaxy's outer disc?  If the latter, the 20-point bar has a defence.")
P("-"*120)
gal_ly = {g["name"]: np.log10(g["gbar"]/a0c) for g in gals}
info(f"   {'object':22} {'x_i':>9} {'pts':>5} {'galaxies':>9} {'admitted at n>=':>16} {'raw dex':>9}")
newly = []
for nm, xi, n, r in sorted(rep["canonical"][1], key=lambda t: -t[2]):
    if n < 3: continue
    ngal = sum(1 for g, l in gal_ly.items() if np.abs(l - math.log10(xi)).min() < 0.20)
    newly.append((nm, xi, n, ngal, r))
    info(f"   {nm:22} {xi:9.5f} {n:5d} {ngal:9d} {n:16d} {r:+9.3f}")
ndistinct = [t[3] for t in newly]
ck("V2c (FAILS -- the defence does not hold) TESTED PROPOSITION: the objects admitted below the 20-point bar "
   "are compared against one or two galaxies' outer discs, so the bar is protecting against an N=1 control.  "
   "IT IS FALSE.  Every object with at least three SPARC points in its window draws them from several "
   "distinct galaxies, and Draco's and Carina's 12 points come from a handful of independent systems.  Thin "
   "is not the same as degenerate, and a bar set at 20 discards real independent comparisons",
   len(ndistinct) > 0 and max(ndistinct) <= 2,
   "; ".join(f"{t[0]} {t[2]} points from {t[3]} galaxies (raw {t[4]:+.3f} dex)" for t in newly[:8]) +
   f".  Median number of contributing galaxies across the {len(newly)} objects with >=3 points: "
   f"{np.median(ndistinct):.1f}")

# =========================================================================================================
P(""); P("="*120)
P("V3.  CAN THE SURVIVING SAMPLE SHOW THE EFFECT AT ALL?  The fork is a DEEP-MOND statement.")
P("="*120)
info("Milgrom's theorem (1994; 2011, arXiv:1111.1611) says modified inertia and modified gravity agree exactly")
info("for circular orbits IN THE DEEP-MOND LIMIT and differ for other orbits.  At x_i >~ 1 both reduce to")
info("Newton and neither predicts anything, so a near-Newtonian object carries no information about the fork")
info("but does carry a vote in the median.  Here is the kept sample, ordered by depth:")
pres_c = rep["canonical"][2]
info(f"   {'object':22} {'x_i':>10} {'raw dex':>9} {'delta vs SPARC':>15}")
for nm, dl, xi, r, c in sorted(pres_c, key=lambda t: t[2]):
    info(f"   {nm:22} {xi:10.5f} {r:+9.3f} {dl:+15.3f}")
cuts = {}
for xcut in (100.0, 1.0, 0.3, 0.1, 0.05):
    sub = [t for t in pres_c if t[2] < xcut]
    if len(sub) < 3: continue
    o = compare(sub, rotating_deltas(a0c, 0.20, 20), nperm=8000)
    cuts[xcut] = o
    info(f"   restricting to x_i < {xcut:<6}: N={o['np_']:3d}  sep {o['sep']:+.3f} dex ({o['nsig']:.2f} sigma, p={o['p']:.4f})")
ck("V3 (FAILS -- THE SECOND HALF OF THE REFUTATION) TESTED PROPOSITION: the null survives when the matched "
   "sample is restricted to the deep-MOND side, where the fork actually has content.  IT IS FALSE.  Four of "
   "the fourteen kept objects are M31's dwarf ellipticals and compact elliptical -- M 32 at x_i = 29.7, "
   "NGC 205 at 1.43, NGC 185 at 0.52, NGC 147 at 0.27 -- at or above the MOND transition, where modified "
   "inertia and modified gravity are BOTH Newton and neither predicts anything.  They carry votes in the "
   "median all the same.  Cutting to x_i < 0.1 gives +0.125 dex at 2.27 sigma (p = 0.009); to x_i < 0.05, "
   "+0.202 dex at 3.68 sigma.  CAVEAT AGAINST MY OWN POINT: a cut on x_i is also a cut on the residual "
   "(see V5), so this restoration is no more trustworthy than the null it displaces -- which is exactly why "
   "neither number may be quoted as the answer",
   all(o["nsig"] < 2.0 for o in cuts.values()),
   "; ".join(f"x_i<{k}: {cuts[k]['sep']:+.3f} dex, {cuts[k]['nsig']:.2f} sigma, p={cuts[k]['p']:.4f}, N={cuts[k]['np_']}"
             for k in sorted(cuts)))

# =========================================================================================================
P(""); P("="*120)
P("V4.  IS THE QUOTED SIGMA RIGHT?  The statistic is a difference of MEDIANS; the error bar is a MEAN's.")
P("="*120)
p_, r_ = c_all["parr"], c_all["rarr"]
se_mean = math.sqrt(p_.std(ddof=1)**2/len(p_) + r_.std(ddof=1)**2/len(r_))
bs = np.array([np.median(rng.choice(p_, len(p_), replace=True)) - np.median(rng.choice(r_, len(r_), replace=True))
               for _ in range(40000)])
se_boot = float(bs.std(ddof=1))
z_perm = float(math.sqrt(2)*erfcinv(c_all["p"]))
info(f"   separation                     {c_all['sep']:+.4f} dex")
info(f"   g05's se (mean formula)        {se_mean:.4f}  ->  {c_all['sep']/se_mean:.2f} sigma   [the quoted number]")
info(f"   bootstrap se of the MEDIANS    {se_boot:.4f}  ->  {c_all['sep']/se_boot:.2f} sigma")
info(f"   permutation p = {c_all['p']:.4f}          ->  {z_perm:.2f} sigma equivalent")
ck("V4 (FAILS) TESTED PROPOSITION: g05's three reported statistics for the same separation agree with each "
   "other.  THEY DO NOT.  g05 quotes '0.93 sigma' from a "
   "standard error built for MEANS while the statistic is a difference of MEDIANS, and quotes a permutation "
   "p = 0.103 alongside it, which is 1.63 sigma two-sided.  The three numbers disagree with each other by "
   "more than a factor two.  A referee quoting the permutation test -- the appropriate one for a median -- "
   "would write 1.6 sigma, not 0.9.  The claim's own headline pairs '0.93 sigma' with 'p = 0.1033' in the "
   "same sentence, and those two numbers are not the same statement about the same data",
   abs(z_perm - c_all["sep"]/se_mean) < 0.3,
   f"quoted {c_all['sep']/se_mean:.2f} sigma; bootstrap-median {c_all['sep']/se_boot:.2f} sigma; "
   f"permutation-equivalent {z_perm:.2f} sigma.  Spread of {abs(z_perm - c_all['sep']/se_mean):.2f} sigma "
   f"between the file's own two reported statistics")

# =========================================================================================================
P(""); P("="*120)
P("V5.  SELECTION ON THE OUTCOME.  Is the x_i cut arithmetically a residual cut?")
P("="*120)
info("g05's A1c reports slope -0.498 of residual against log10(x_i) across the pressure sample, and explains")
info("that -1/2 is what you get if g_obs carries NO x_i dependence.  If that holds, then keeping the highest-")
info("x_i objects is the same operation as keeping the lowest-residual objects, and the kept median is")
info("predictable WITHOUT LOOKING AT THE DISPERSIONS AT ALL.  Test that directly.")
rows_all = allrows[a0c]
lx = np.array([math.log10(t[2]) for t in rows_all]); rr_ = np.array([t[1] for t in rows_all])
sl, ic = np.polyfit(lx, rr_, 1)
# the surrogate: replace every measured residual by the -0.5 line through the sample, keep x_i, redo the cut
sur = ic + sl*lx
_keptnames = {t[0] for t in pres_c}
kept_mask = np.array([nm in _keptnames for nm, _, _ in rows_all])
info(f"   fitted slope {sl:+.3f} dex/dex, intercept {ic:+.3f}; r = {np.corrcoef(lx, rr_)[0,1]:+.3f} on N={len(rows_all)}")
info(f"   REAL      kept median raw residual {np.median(rr_[kept_mask]):+.3f}, dropped {np.median(rr_[~kept_mask]):+.3f}")
info(f"   SURROGATE (residuals replaced by the fitted line, dispersions never consulted):")
info(f"             kept median {np.median(sur[kept_mask]):+.3f}, dropped {np.median(sur[~kept_mask]):+.3f}")
gap_real = np.median(rr_[~kept_mask]) - np.median(rr_[kept_mask])
gap_sur  = np.median(sur[~kept_mask]) - np.median(sur[kept_mask])
ck("V5 (FAILS -- AND THE FAILURE IS A POINT IN g05's FAVOUR, WHICH I REPORT AS READILY AS THE OTHERS) "
   "TESTED PROPOSITION: the kept-versus-dropped split in raw residual is purely mechanical -- a surrogate "
   "that throws away every measured dispersion and replaces it by the fitted line in log10(x_i) reproduces "
   "the gap, so cutting on acceleration IS cutting on the residual and the null is circular.  IT IS ONLY "
   "HALF TRUE.  The line-surrogate reproduces about half the real gap; the other half is genuine excess "
   "residual in the dropped objects beyond the mechanical trend.  So the acceleration cut is partly, but not "
   "wholly, a cut on the outcome.  My circularity objection is therefore WEAKER than I expected and g05's "
   "matching is not circular by construction -- which makes the threshold sensitivity in V2 the whole case",
   abs(gap_real - gap_sur) < 0.10,
   f"real kept-vs-dropped gap {gap_real:+.3f} dex; line-surrogate gap {gap_sur:+.3f} dex; unexplained excess "
   f"{abs(gap_real-gap_sur):.3f} dex, i.e. {100*(1-gap_sur/gap_real):.0f} per cent of the split is NOT mechanical")

# does the DELTA (matched residual) still run with x_i inside the kept set?
kx = np.array([math.log10(t[2]) for t in pres_c]); kd = np.array([t[1] for t in pres_c])
ks, kc = np.polyfit(kx, kd, 1)
kr = float(np.corrcoef(kx, kd)[0, 1])
ck("V5b (FAILS -- also in g05's favour) TESTED PROPOSITION: the depth trend continues inside the kept set, "
   "so the kept median is just an accident of where those 14 objects sit in x_i.  IT IS FALSE.  Inside the "
   "matched range the trend is essentially flat (slope -0.03, r = -0.12).  The pressure objects that overlap "
   "SPARC really do sit near the rotating relation with no residual gradient, which is a real and clean "
   "result and is the strongest thing g05 has.  The dispute is entirely about which objects are allowed in",
   abs(kr) > 0.4,
   f"inside the kept set: slope {ks:+.3f} dex per dex, r = {kr:+.3f} on N={len(kx)}; "
   f"deltas run {kd.min():+.3f} to {kd.max():+.3f} dex over x_i = {10**kx.min():.4f} to {10**kx.max():.1f}")

# =========================================================================================================
P(""); P("="*120)
P("V6.  THE DISCRIMINANT QUESTION, put to the withdrawal itself.")
P("="*120)
info("The lens is: does the claim distinguish the framework's failure mode from ordinary cold dark matter?")
info("A WITHDRAWAL is the assertion that a previously claimed discriminant does not discriminate, so it")
info("cannot fail that test -- but it can be checked for the opposite error, a manufactured null.  The single")
info("cleanest cross-check available is g05's own globular-cluster class, recomputed here from the same")
info("numbers: pressure-supported, and dark-matter-free under LCDM.")
GC = [("Pal 4", 101.39, 104.05, 14.23, 0.01, 15.88, 0.87),
      ("Pal 14", 73.58, 68.55, 14.13, 0.04, 27.63, 0.38),
      ("Pal 3", 94.84, 98.17, 14.56, 0.04, 20.16, 0.80),
      ("NGC 2419", 88.47, 95.93, 10.56, 0.08, 19.76, 5.10)]
gc_res = []
for nm, Dsun, Rgc, V, EBV, rhl, sob in GC:
    MV = V - 5*math.log10(Dsun*1e3/10.0) - 3.1*EBV
    M = UPS_V*10**(0.4*(4.83 - MV))
    r12 = (4.0/3.0)*rhl*PC
    xi = G*(0.5*M*Msun)/r12**2/a0c
    xe = G*MW_MB*Msun/(Rgc*kpc)**2/a0c
    sp = math.sqrt(g_qumond_sphere(xi, xe)*a0c*r12/3.0)/1e3
    gc_res.append((nm, 2.0*math.log10(sob/sp), xi))
    info(f"   {nm:10} x_i={xi:8.4f}  sigma_obs={sob:5.2f}  sigma_pred={sp:5.2f}  {2.0*math.log10(sob/sp):+7.3f} dex")
over = [t for t in pres_c if 0.01 <= t[2] <= 1.2]
ck("V6 the globular clusters reproduce and they do cut against support-type as the organising variable: at "
   "OVERLAPPING internal accelerations the dark-matter-dominated dwarf spheroidals sit above the kernel and "
   "the dark-matter-free clusters far below it.  Support type does not predict the sign; dark-matter content "
   "does.  So the withdrawal is not merely 'the number got smaller' -- an independent class argues the same "
   "way, and ordinary cold dark matter reproduces the whole pattern",
   np.median([t[1] for t in gc_res]) < -0.3 and np.median([t[3] for t in over]) > 0.05,
   f"GC median {np.median([t[1] for t in gc_res]):+.3f} dex on N=4 (16-23 stars apiece, two of four from "
   f"model-dependent N-body fits); dSph over x_i = 0.01-1.2 median {np.median([t[3] for t in over]):+.3f} dex on "
   f"N={len(over)}")

# =========================================================================================================
P(""); P("="*120)
P("V7.  MUTATION CONTROLS on this verification.")
P("="*120)
sh = []
for _ in range(4000):
    perm = rng.permutation(len(rows_all))
    fake = [(rows_all[i][0], rr_[perm][i], rows_all[i][2]) for i in range(len(rows_all))]
    pres_f, rot_f, _ = matched(fake, a0c)
    sh.append(np.median([t[1] for t in pres_f]) - np.median([t[1] for t in rot_f]))
sh = np.array(sh)
ck("M1 MUTATION CONTROL (FAILS my stated expectation, and again in g05's favour) TESTED PROPOSITION: "
   "shuffling the residuals across the pressure objects while holding every x_i fixed, then re-running the "
   "identical matching, leaves the separation where it is -- i.e. the kept set is a random draw.  IT IS "
   "FALSE.  The shuffled separation centres on +0.46 dex and the real kept value sits well below it.  The "
   "kept objects genuinely are the low-residual ones, so the matching is doing real work and is not a "
   "relabelling.  The machinery is sound; the disputed choice is the threshold",
   abs(c_all["sep"] - np.median(sh)) < 2.0*sh.std(),
   f"real {c_all['sep']:+.3f} dex; residual-shuffle-through-the-same-matching gives {np.median(sh):+.3f} "
   f"+- {sh.std():.3f}, i.e. the real value is {abs(c_all['sep']-np.median(sh))/sh.std():.2f} shuffle-sigma out")

info("MUTATION CONTROL: multiply every dwarf-spheroidal dispersion by 10^(0.5*0.215), which injects exactly")
info("   f09's claimed +0.215 dex offset into the pressure side, and check the matched test recovers it.")
boost = 10**(0.5*0.215)
rows_b = []
for k in KEYS:
    for d in classes[k]:
        d2 = dict(d); d2["sig"] = d["sig"]*boost
        rows_b.append((d["name"],) + dsph_row(d2, a0c)[:2])
pres_b, rot_b, _ = matched(rows_b, a0c)
ob = compare(pres_b, rot_b, nperm=4000)
ck("M2 the boosted-dispersion mutation lands where arithmetic says it must",
   abs((ob["sep"] - c_all["sep"]) - 0.215) < 0.01,
   f"separation {c_all['sep']:+.3f} -> {ob['sep']:+.3f} dex, shift {ob['sep']-c_all['sep']:+.4f} against the "
   f"injected {0.215:+.3f}; injected significance {ob['nsig']:.2f} sigma, so the matched test WOULD have "
   f"detected a genuine f09-sized offset in the kept sample at that strength")

# =========================================================================================================
P(""); P("="*120); P("VERDICT OF THE ADVERSARIAL PASS"); P("="*120)
P(f"  THE CLAIM IS REFUTED.  Not its arithmetic -- that reproduces to the last digit -- but the withdrawal.")
P(f"")
P(f"  WHAT REPRODUCES.  At g05's settings (window 0.20 dex, at least 20 SPARC points in it) the separation is")
P(f"  {c_all['sep']:+.4f} dex, {c_all['nsig']:.2f} sigma, permutation p = {c_all['p']:.4f}, 14 kept / 36 dropped against 147 rotating;")
P(f"  alt footing {a_all['sep']:+.4f} dex, {a_all['nsig']:.2f} sigma.  Every number in the claim is correct as computed.")
P(f"")
P(f"  THE SPECIFIC ERROR: A SECOND FREE PARAMETER, UNDISCLOSED AND UNSCANNED, DOES ALL THE WORK.")
P(f"  g05 declares MATCH_W = 0.20 and MATCH_N = 20 on one line and treats only the WINDOW as an analysis")
P(f"  choice -- its A9 sensitivity table scans n at 20, 30 and 50 and NEVER BELOW 20.  Holding the window at")
P(f"  g05's own 0.20 dex and moving only the point bar:")
P(f"")
for k in (1, 3, 5, 10, 20, 40, 80):
    P(f"        n >= {k:<3d}  N_pres = {n_scan[k]['np_']:3d}  N_rot = {n_scan[k]['nr']:3d}   {n_scan[k]['sep']:+.3f} dex   {n_scan[k]['nsig']:5.2f} sigma   p = {n_scan[k]['p']:.4f}"
      + ("   <-- the value the claim reports" if k == 20 else ""))
P(f"")
P(f"  At n >= 5 the separation is {n_scan[5]['sep']:+.3f} dex, {n_scan[5]['nsig']:.2f} sigma, p = {n_scan[5]['p']:.4f} on N = {n_scan[5]['np_']} pressure objects.")
P(f"  That REPRODUCES f09's +0.215 dex at HIGHER significance than f09 itself claimed, on the alt footing too")
P(f"  ({n_scan_alt[5]['sep']:+.3f} dex, {n_scan_alt[5]['nsig']:.2f} sigma).  A claim of withdrawal cannot rest on the one setting of an")
P(f"  undisclosed knob at which the effect vanishes when a neighbouring setting restores the predecessor's")
P(f"  number outright.")
P(f"")
P(f"  AND THE STATED REASON FOR THE DROPS IS NOT WHAT THE DATA SAY.  The claim says 36 objects were 'dropped")
P(f"  as outside SPARC's range'.  Only {nz} of the 36 have zero SPARC points in the window.  The largest count")
P(f"  among the dropped is {maxn} -- ONE POINT below the bar of 20.  SPARC's own floor is g_bar/a_0 = {10**LY.min():.5f},")
P(f"  three times deeper than Draco sits.  Draco and Carina -- two of f09's own eight -- each have 12 SPARC")
P(f"  points within 0.20 dex, drawn from 8 DISTINCT GALAXIES apiece, so the bar is not protecting against a")
P(f"  degenerate one-galaxy control (V2c): every object with three or more points draws them from a median of")
P(f"  {np.median(ndistinct):.0f} independent systems.  The four members of f09's eight that the bar removes have a median raw")
P(f"  residual of {np.median([t[3] for t in drop8]):+.3f} dex against {np.median([t[3] for t in kept8]):+.3f} for the four it keeps.")
P(f"")
P(f"  A SECOND, INDEPENDENT ROUTE TO THE SAME PLACE.  The fork is a DEEP-MOND statement; Milgrom's theorem")
P(f"  concerns the deep-MOND limit.  Four of the fourteen survivors (M 32 at x_i = 29.7, NGC 205 at 1.43,")
P(f"  NGC 185 at 0.52, NGC 147 at 0.27) are M31 dwarf/compact ellipticals at or above the MOND transition,")
P(f"  where both arms reduce to Newton and neither predicts anything -- yet they vote in the median.")
P(f"  Restricting to x_i < 0.1 gives {cuts[0.1]['sep']:+.3f} dex at {cuts[0.1]['nsig']:.2f} sigma (p = {cuts[0.1]['p']:.4f}); to x_i < 0.05, {cuts[0.05]['sep']:+.3f} dex at {cuts[0.05]['nsig']:.2f} sigma.")
P(f"")
P(f"  THE REPORTED SIGNIFICANCE IS ALSO THE WEAKEST OF THREE INCONSISTENT STATISTICS.  A difference of")
P(f"  MEDIANS was given a difference-of-MEANS standard error ({c_all['sep']/se_mean:.2f} sigma).  Bootstrapping the medians")
P(f"  gives {c_all['sep']/se_boot:.2f} sigma.  The file's own permutation p = {c_all['p']:.4f} is {z_perm:.2f} sigma.  The claim's headline")
P(f"  sentence quotes '0.93 sigma' and 'p = 0.1033' side by side; they differ by {abs(z_perm - c_all['sep']/se_mean):.2f} sigma.")
P(f"")
P(f"  WHERE I ATTACKED AND FAILED, REPORTED AS READILY AS THE REST.  Three of my own lines went against me:")
P(f"   * The circularity objection is only half right (V5).  A line-surrogate in log10(x_i) reproduces only")
P(f"     {100*gap_sur/gap_real:.0f} per cent of the kept-versus-dropped gap; the rest is genuine excess residual.  The matching")
P(f"     is NOT circular by construction.")
P(f"   * Inside the kept range the depth trend is flat (V5b: slope {ks:+.2f}, r = {kr:+.2f}).  The pressure objects that")
P(f"     genuinely overlap SPARC really do sit on the rotating relation with no gradient.  That is a clean")
P(f"     result and it is g05's strongest card.")
P(f"   * The residual-shuffle mutation (M1) shows the matching does real work, and the injected-offset")
P(f"     mutation (M2) shows the test would have caught an f09-sized separation in the kept sample at {ob['nsig']:.1f} sigma.")
P(f"     The machinery is sound.  The dispute is entirely about which objects are admitted.")
P(f"")
P(f"  AND ONE THING THE CLAIM GETS RIGHT THAT SURVIVES ALL OF THIS.  The globular clusters are the only")
P(f"  genuine discriminant in the file and they argue against the whole rotation/pressure reading: dark-")
P(f"  matter-free, pressure-supported outer-halo clusters sit {np.median([t[1] for t in gc_res]):+.2f} dex BELOW the kernel while dark-")
P(f"  matter-dominated dwarf spheroidals at the same accelerations sit {np.median([t[3] for t in over]):+.2f} dex above it.  Support type")
P(f"  does not predict the sign; dark-matter content does.  Ordinary cold dark matter reproduces the entire")
P(f"  pattern.  So f09's split was never a discriminant -- but that is a DIFFERENT argument from the one the")
P(f"  claim makes, and it does not license the sentence 'it falls to 0.93 sigma'.")
P(f"")
P(f"  WHAT MAY BE SAID INSTEAD.  'Under object-by-object matching the rotation-versus-pressure separation is")
P(f"  not a stable number: it spans {min(n_scan[k]['sep'] for k in n_scan):+.3f} to {max(n_scan[k]['sep'] for k in n_scan):+.3f} dex and {min(n_scan[k]['nsig'] for k in n_scan):.1f} to {max(n_scan[k]['nsig'] for k in n_scan):.1f} sigma across defensible settings of the")
P(f"  matching window, the minimum-count threshold, and the acceleration range admitted, with no principled")
P(f"  way to choose among them.  f09's 1.73 sigma is not confirmed and is not withdrawn; it is undetermined.")
P(f"  The comparison does not measure the modified-inertia fork in either direction, and the globular-cluster")
P(f"  class argues that dark-matter content, not support type, organises the residuals.'")
sys.exit(ck.done())
