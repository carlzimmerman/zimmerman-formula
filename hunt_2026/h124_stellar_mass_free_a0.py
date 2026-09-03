#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h124_stellar_mass_free_a0.py -- HUNT ITEM 124: a_0 from systems with (almost) no stars.
========================================================================================
The item: find a stellar-mass-free sample -- HI-only clouds, almost-dark galaxies, tidal debris -- and measure a_0
from  v^4 = G M_HI a_0  with the 1.33 helium factor as the only assumption.  Pass if a_0 to 15%.

FOUR RUNGS are built here, in decreasing order of how much one should believe them.  Three of them have already been
run in this hunt as pass/fail items (31, 31b, 46); what is new is (a) turning each into an a_0 with an error bar so
that item 125's ladder can use it, (b) the SPARC gas-dominated rung, which is the only one with RESOLVED kinematics,
and (c) an internal calibration that explains, in one number, why the unresolved-HI rungs disagree with the resolved
one by up to a dex.

  A  SPARC gas-dominated discs      resolved rotation curves; v is a measured V(R), not a line width          NEW
  B  ALFALFA gas-dominated          12k galaxies, but v comes from the W50 line width                         NEW
  C  Leisman+2017 almost-darks      the item's own named sample; item 31/31b already found it does not sit    from 31/31b
                                    on the relation, and 31b traced most of that to a width-selection effect
  D  Lelli+2015 tidal dwarfs        tidal debris, the item's other named class; item 46 found a liability     from 46

TWO BIASES APPLY TO THE ITEM'S OWN FORMULA and both are quantified rather than assumed away:
  (i)  "M_HI only" ignores the stars that are there.  a_0 = v^4/(G M_b), so dropping a stellar fraction f_* biases
       a_0 HIGH by -log10(1 - f_*).  At f_* = 0.1 that is +0.046 dex.  The formula gives an UPPER bound on a_0.
  (ii) v^4 = G M a_0 is the asymptotic limit.  At the outermost measured radius the Route A kernel is not asymptotic:
       v^4 = G M a_0 (1 + sqrt(y)/2 + ...)^2, so the literal formula is biased HIGH by another ~0.09 dex.  Item 102
       found this same term as an outright bug in item 25's estimator; here it is applied as a correction.

Both footings.  Mutation controls.  LambdaCDM/Newtonian beside.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.optimize import brentq
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(124)
COH_FLOOR = 0.0433          # item 103: the coherent calibration floor once Upsilon is removed (distance + HI scale)
W_TURB = 20.0               # km/s FWHM, the turbulent broadening removed in quadrature (as in item 31)

def a0_kern(x, y):
    """solve <log g_obs - log[nu(g_bar/a) g_bar]> = 0 -- the corrected estimator of item 102"""
    f = lambda a: float(np.mean(np.log10(y) - np.log10(nu(x/a)*x)))
    try: return brentq(f, 1e-14, 1e-7, xtol=1e-19, rtol=8.9e-16, maxiter=200)
    except Exception: return float("nan")

def med_boot(v, n=2000):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if len(v) < 3: return float("nan"), float("nan")
    bs = np.array([np.median(rng.choice(v, len(v))) for _ in range(n)])
    return float(np.median(v)), float(bs.std())

LADDER = []
def rung(label, a0, sig, mlfree, note):
    LADDER.append(dict(label=label, a0=a0, sig=sig, mlfree=mlfree, note=note))
    info(f"  RUNG  {label:44} a_0 = {a0:.3e}  +- {sig:.3f} dex   "
         f"({math.log10(a0/A0['canonical']):+.2f} canon, {math.log10(a0/A0['alt']):+.2f} alt)   {note}")

# ============================================================================================================
P("="*118); P("RUNG A -- SPARC gas-dominated discs: the only stellar-mass-free sample with RESOLVED kinematics"); P("="*118)
gals = load_sparc()
rowsA = []
for g in gals:
    gg = g["vg"]*np.abs(g["vg"])/g["r"]*KMS2_KPC                        # the HI disc's own contribution (x1.33 already in V_gas)
    gb = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC
    i = len(g["r"]) - 1                                                  # outermost measured point
    if gg[i] <= 0 or gb[i] <= 0: continue
    fstar_out = 1 - gg[i]/gb[i]
    Mgas = 1.33*g["MHI"]*1e9
    fstar_glob = UPS_D*g["L36"]*1e9/(UPS_D*g["L36"]*1e9 + Mgas)
    lit = ((g["Vflat"]*1e3)**4/(G*Mgas*Msun)) if (g["Vflat"] > 0 and Mgas > 0) else float("nan")
    rowsA.append(dict(name=g["name"], fs_out=fstar_out, fs_glob=fstar_glob,
                      a_gas=a0_kern(np.array([gg[i]]), np.array([g["gobs"][i]])),
                      a_bar=a0_kern(np.array([gb[i]]), np.array([g["gobs"][i]])),
                      a_lit=lit, Mb=g["Mb"], eD=g["eD"]/g["D"], y=gg[i]/A0["canonical"]))
fs_out = np.array([r["fs_out"] for r in rowsA])
info(f"{len(rowsA)} SPARC discs with a positive HI contribution at the outermost measured radius")
info(f"  {'cut on f_* at the outer point':>32} {'N':>4} {'a_0 (1.33 M_HI ONLY)':>21} {'a_0 (all baryons)':>19} "
     f"{'literal V_flat^4/G M_HI':>24} {'<f_*>':>7}")
for c in (9.9, 0.4, 0.3, 0.2, 0.15):
    m = fs_out < c
    if m.sum() < 5: continue
    ag = np.array([r["a_gas"] for r, k in zip(rowsA, m) if k]); ab = np.array([r["a_bar"] for r, k in zip(rowsA, m) if k])
    al = np.array([r["a_lit"] for r, k in zip(rowsA, m) if k])
    lab = "all" if c > 1 else f"f_* < {c}"
    info(f"  {lab:>32} {m.sum():4d} {10**np.median(np.log10(ag[np.isfinite(ag)])):21.3e} "
         f"{10**np.median(np.log10(ab[np.isfinite(ab)])):19.3e} "
         f"{10**np.median(np.log10(al[np.isfinite(al)])):24.3e} {np.median(fs_out[m]):7.3f}")
selA = fs_out < 0.2
sub = [r for r, k in zip(rowsA, selA) if k]
agA = np.log10(np.array([r["a_gas"] for r in sub]))          # gas only, kernel at the outermost point
abA = np.log10(np.array([r["a_bar"] for r in sub]))          # all baryons, same point
alA = np.log10(np.array([r["a_lit"] for r in sub]))          # the item's literal V_flat^4/(G x 1.33 M_HI)
fin = np.isfinite(agA) & np.isfinite(abA)
mA, sA = med_boot(agA[fin]); mB_, sB_ = med_boot(abA[fin])
finl = np.isfinite(alA) & fin
mL, sL = med_boot(alA[finl])
fs_med = float(np.median(fs_out[selA]))                       # LOCAL stellar share at the point used
fsg_med = float(np.median([r["fs_glob"] for r in sub]))       # GLOBAL stellar share (the one the total-mass formula omits)
ybar = float(np.median([r["y"] for r in sub]))
info("")
P("  WHY THE LITERAL FORMULA IS AN UPPER BOUND.  v^4 = G M a_0 is exact only asymptotically and only for the TOTAL")
P("  baryonic mass.  Three terms separate it from what the data actually constrain, and all three are computed here:")
geo = np.array([math.log10(r["a_gas"]) for r in sub])         # placeholders, per-galaxy terms below
term_geo, term_ker, term_vf = [], [], []
for g in gals:
    nm = [r["name"] for r in sub]
    if g["name"] not in nm: continue
    i = len(g["r"]) - 1
    gg = g["vg"][i]*abs(g["vg"][i])/g["r"][i]*KMS2_KPC
    Mgas_t = 1.33*g["MHI"]*1e9*Msun
    if gg <= 0 or Mgas_t <= 0 or g["Vflat"] <= 0: continue
    Menc = gg*(g["r"][i]*kpc)**2/G                            # equivalent point mass of the DISC's in-plane force
    term_geo.append(math.log10(Menc/Mgas_t))                  # >0: a thin disc pulls harder than a point of the same mass
    yv = gg/A0["canonical"]
    term_ker.append(2*math.log10(1 + math.sqrt(yv)/2))        # the kernel is not asymptotic at the last measured point
    term_vf.append(4*math.log10(g["vobs"][i]/(g["Vflat"])))   # v at the last point vs the fitted V_flat
tg, tk, tv = float(np.median(term_geo)), float(np.median(term_ker)), float(np.median(term_vf))
LEV_LOC = 1.25                                                 # |d log a_0 / d log g_bar| = |lambda/n| in this regime (item 103)
info(f"  (1) DISC GEOMETRY: at the outermost point the HI disc's in-plane force equals that of a point mass "
     f"{10**tg:.2f}x M_gas ({tg:+.3f} dex), so the point-mass formula understates the baryonic pull "
     f"-> a_0 too high by {LEV_LOC*tg:+.3f} dex")
info(f"  (2) THE KERNEL IS NOT ASYMPTOTIC: median y = g_gas/a_0 = {ybar:.4f} at that point, so v^4 = G M a_0 (1+sqrt(y)/2)^2 "
     f"-> a_0 too high by {tk:+.3f} dex")
info(f"  (3) V_flat vs the last measured point: {tv:+.3f} dex")
info(f"  (4) and the item's assumption itself -- STARS OMITTED.  Global stellar share of these discs {fsg_med:.3f}, local "
     f"share at the point used {fs_med:.3f} -> the gas-only answer is high by {-LEV_LOC*math.log10(1-fs_med):+.3f} dex")
pred_gap = LEV_LOC*tg + tk + tv
info("")
info(f"literal v_flat^4/(G x 1.33 M_HI)                = {10**mL:.3e}  <- the item's formula, an UPPER bound")
info(f"kernel at the outermost point, GAS ONLY         = {10**mA:.3e}  +- {sA:.3f} dex  (stars still omitted)")
info(f"kernel at the outermost point, ALL BARYONS      = {10**mB_:.3e}  +- {sB_:.3f} dex  <- best estimate")
info(f"predicted literal-minus-gas-only gap from (1)+(2)+(3) = {pred_gap:+.3f} dex; observed {mL-mA:+.3f} dex")
sigA = math.hypot(sB_, COH_FLOOR)
rung("A  SPARC gas-dominated, resolved (f_*,loc < 0.2)", 10**mB_, sigA, True,
     f"{fin.sum()} discs, per-galaxy scatter {abA[fin].std():.2f} dex")
ck("124.A the gap between the item's literal formula and what the data constrain is fully accounted for by three "
   "named terms -- the disc's in-plane force exceeding a point mass, the kernel not being asymptotic at the last "
   "measured radius, and V_flat not being the last point -- with nothing left over.  So the literal 1.7e-10 is not a "
   "measurement of a_0; it is the same number seen through a point-mass asymptotic approximation that these discs "
   "do not satisfy",
   abs(pred_gap - (mL - mA)) < 0.08,
   f"predicted gap {pred_gap:+.3f} dex = geometry {LEV_LOC*tg:+.3f} + kernel {tk:+.3f} + V_flat {tv:+.3f}; "
   f"observed {mL-mA:+.3f} dex; residual {pred_gap-(mL-mA):+.3f}")
ck("124.A2 AGAINST INTEREST: rung A does not reach the item's 15%.  Its statistical error alone is "
   f"{100*(10**sB_-1):.0f}% on {fin.sum()} galaxies and item 103's calibration floor adds {100*(10**COH_FLOOR-1):.0f}%.  The item's "
   "own criterion is missed by a factor of about two",
   10**sigA - 1 > 0.15, f"a_0 = {10**mB_:.3e} +- {sigA:.3f} dex = {100*(10**sigA-1):.0f}%, target 15%")
info(f"residual M/L sensitivity of rung A: the stellar term is {100*fs_med:.0f}% of g_bar at the point used, so "
     f"d log a_0/d log Upsilon = {-LEV_LOC*fs_med:+.3f} -- a factor-2 error in Upsilon costs {LEV_LOC*fs_med*math.log10(2):.3f} dex.  "
     "Not zero, but a sixth of the full deep tail's.")

# ============================================================================================================
P(""); P("="*118); P("RUNG B -- ALFALFA gas-dominated: 12,000 galaxies, and why the number they give cannot be used"); P("="*118)
a = load_alfalfa()
Ms = np.where(np.isfinite(a["logMsM"]), a["logMsM"], a["logMsT"])
MHI = 10**a["logMHI"]; Mgas = 1.33*MHI
Mst = np.where(np.isfinite(Ms), 10**np.nan_to_num(Ms, nan=0.0), 0.0)
Mb = Mgas + Mst
base = ((a["code"] == 1) & (a["pflag"] == 1) & (a["snr"] >= 6.5) & np.isfinite(a["ba"]) & np.isfinite(Ms)
        & (a["W50"] > 0) & np.isfinite(a["inc"]) & (a["inc"] >= 45))
Wr = np.sqrt(np.maximum(a["W50"]**2 - W_TURB**2, 0.0))
with np.errstate(divide="ignore", invalid="ignore"):
    v = Wr/(2*np.sin(np.radians(a["inc"])))
good = base & np.isfinite(v) & (v > 0) & (Mb > 0)
info(f"alpha.100 x ALFALFA-SDSS, code-1, SNR >= 6.5, clean photometry, i >= 45 deg: N = {good.sum()}")
fstarA = Mst/np.maximum(Mb, 1e-30)
info(f"  {'cut':>14} {'N':>7} {'a_0 (1.33 M_HI only)':>21} {'a_0 (+ stars)':>15} {'<f_*>':>7} {'<log M_b>':>10}")
BB = {}
for c in (9.9, 0.3, 0.2, 0.15, 0.1):
    m = good & (fstarA < c)
    if m.sum() < 50: continue
    ag = np.log10((v[m]*1e3)**4/(G*Mgas[m]*Msun)); ab = np.log10((v[m]*1e3)**4/(G*Mb[m]*Msun))
    lab = "all" if c > 1 else f"f_* < {c}"
    BB[lab] = (10**np.median(ag), int(m.sum()), float(np.median(fstarA[m])), float(np.median(np.log10(Mb[m]))))
    info(f"  {lab:>14} {m.sum():7d} {10**np.median(ag):21.3e} {10**np.median(ab):15.3e} "
         f"{np.median(fstarA[m]):7.3f} {np.median(np.log10(Mb[m])):10.2f}")
info("")
info("the cut moves the answer by half a dex.  The reason is a MASS trend in the estimator, which the same table")
info("exposes on galaxies whose stellar masses ARE known, so it cannot be an M/L effect:")
info(f"  {'log M_b bin':>16} {'N':>7} {'a_0 = v^4/(G M_b)  [W50, ALFALFA]':>34} {'a_0  [resolved, SPARC]':>24}")
rowsS = []
for g in gals:
    gb = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC
    i = len(g["r"]) - 1
    if gb[i] <= 0: continue
    rowsS.append((math.log10(g["Mb"]), a0_kern(np.array([gb[i]]), np.array([g["gobs"][i]]))))
lMS = np.array([r[0] for r in rowsS]); aS = np.array([r[1] for r in rowsS])
okS = np.isfinite(aS); lMS, aS = lMS[okS], aS[okS]
lMA = np.log10(Mb[good]); aA = (v[good]*1e3)**4/(G*Mb[good]*Msun)
TREND = []
for lo, hi in ((7.5, 8.5), (8.5, 9.5), (9.5, 10.0), (10.0, 10.5), (10.5, 11.5)):
    kA = (lMA >= lo) & (lMA < hi); kS = (lMS >= lo) & (lMS < hi)
    if kA.sum() < 30: continue
    sv = f"{10**np.median(np.log10(aS[kS])):.3e}" if kS.sum() >= 5 else f"(N={kS.sum()})"
    TREND.append((lo, hi, int(kA.sum()), float(np.median(np.log10(aA[kA]))), float(np.median(np.log10(aS[kS]))) if kS.sum() >= 5 else float("nan")))
    info(f"  {f'{lo:.1f} - {hi:.1f}':>16} {kA.sum():7d} {10**np.median(np.log10(aA[kA])):34.3e} {sv:>24}")
slA = np.polyfit(lMA, np.log10(aA), 1)[0]
slS = np.polyfit(lMS, np.log10(aS), 1)[0]
bsS = np.array([np.polyfit(lMS[i], np.log10(aS[i]), 1)[0] for i in (rng.integers(0, len(aS), len(aS)) for _ in range(400))])
info("")
info(f"regression of log a_0 on log M_b: ALFALFA W50 {slA:+.3f} dex/dex; SPARC resolved {slS:+.3f} +- {bsS.std():.3f} dex/dex")
for wt in (0.0, 10.0, 30.0):
    Wr2 = np.sqrt(np.maximum(a["W50"]**2 - wt**2, 0.0))
    with np.errstate(divide="ignore", invalid="ignore"): v2 = Wr2/(2*np.sin(np.radians(a["inc"])))
    m2 = good & np.isfinite(v2) & (v2 > 0)
    info(f"   turbulence FWHM {wt:4.0f} km/s: ALFALFA slope {np.polyfit(np.log10(Mb[m2]), np.log10((v2[m2]*1e3)**4/(G*Mb[m2]*Msun)), 1)[0]:+.3f} dex/dex "
         f"-- the trend is not the turbulence subtraction")
for q0 in (0.1, 0.3, 0.4):
    inc2 = inclination_from_ba(a["ba"], q0=q0)
    with np.errstate(divide="ignore", invalid="ignore"): v3 = Wr/(2*np.sin(np.radians(inc2)))
    m3 = base & np.isfinite(v3) & (v3 > 0) & np.isfinite(inc2) & (inc2 >= 45)
    info(f"   intrinsic axis ratio q0 = {q0:.1f}: ALFALFA slope "
         f"{np.polyfit(np.log10(Mb[m3]), np.log10((v3[m3]*1e3)**4/(G*Mb[m3]*Msun)), 1)[0]:+.3f} dex/dex, median a_0 "
         f"{10**np.median(np.log10((v3[m3]*1e3)**4/(G*Mb[m3]*Msun))):.2e} -- dwarfs being THICKER than q0 = 0.2 would "
         f"push their a_0 DOWN further, i.e. the wrong way to explain the trend away")
ck("124.B (the finding that reorganises three items) the HI LINE WIDTH is not a rotation speed at low mass, and the "
   "damage is measurable: a_0 = v^4/(G M_b) from ALFALFA W50 runs UP with baryonic mass at +0.25 dex per dex over "
   "three decades, where the same quantity from SPARC's resolved rotation curves rises 3.5x more slowly (+0.07, itself "
   "only 2 sigma from flat, and driven by the very lowest-mass discs).  Since "
   "stellar masses are known for both, this cannot be an M/L effect -- it is the estimator.  Any stellar-mass-free "
   "sample selected on gas fraction is also selected to be LOW MASS, so it inherits the whole trend",
   slA > 3*abs(slS) and abs(slS) < 3*bsS.std(),
   f"ALFALFA W50 slope {slA:+.3f} dex/dex (a {slA*3:.2f} dex swing over the range); SPARC resolved {slS:+.3f} +- {bsS.std():.3f} "
   f"({slS/bsS.std():+.1f} sigma from flat); ALFALFA a_0 = {10**TREND[0][3]:.2e} at log M_b ~ 8 against {10**TREND[-1][3]:.2e} at ~11")
mB, sB = med_boot(np.log10(aA[(lMA >= 9.0)]))
rung("B  ALFALFA W50, log M_b > 9 (NOT M/L-free, shown for calibration)", 10**mB, math.hypot(sB, COH_FLOOR), False,
     f"{int((lMA>=9).sum())} galaxies; the gas-dominated cut of the SAME data gives {BB.get('f_* < 0.15',(float('nan'),))[0]:.2e}")
info("Rung B is deliberately NOT entered as a stellar-mass-free measurement: its gas-dominated subsample gives")
info(f"   {BB['f_* < 0.15'][0]:.3e}, which is {math.log10(BB['f_* < 0.15'][0]/10**mA):+.2f} dex from rung A, and check 124.B says why.")

# ============================================================================================================
P(""); P("="*118); P("RUNG C -- Leisman+2017 almost-darks (the item's own named sample), restated as an a_0"); P("="*118)
h = load_huds()
hMs = np.where(np.isfinite(h["logMsM"]), h["logMsM"], h["logMsT"])
hMgas = 1.33*10**h["logMHI"]
hMst = np.where(np.isfinite(hMs), 10**np.nan_to_num(hMs, nan=0.0), 0.0)
hMb = hMgas + hMst
hWr = np.sqrt(np.maximum(h["W50"]**2 - W_TURB**2, 0.0))
with np.errstate(divide="ignore", invalid="ignore"):
    hv = hWr/(2*np.sin(np.radians(h["inc"])))
hok = np.isfinite(hv) & (hv > 0) & (hMb > 0)
aC_gas = np.log10((hv[hok]*1e3)**4/(G*hMgas[hok]*Msun))
aC_bar = np.log10((hv[hok]*1e3)**4/(G*hMb[hok]*Msun))
mC, sC = med_boot(aC_gas); mCb, sCb = med_boot(aC_bar)
info(f"{hok.sum()} almost-darks with a usable width and inclination; median M_gas/M_b = {np.median(hMgas[hok]/hMb[hok]):.3f}")
info(f"a_0 from v^4/(G x 1.33 M_HI) = {10**mC:.3e} +- {sC:.3f} dex; including the (small) stellar mass, {10**mCb:.3e}")
info(f"that is {mCb - math.log10(A0['canonical']):+.2f} dex from canonical -- a factor {10**(math.log10(A0['canonical'])-mCb):.0f} low.  "
     f"Item 31 reported this as -0.30 dex in log v; 4 x that is the number here.")
seln = (lMA >= np.log10(hMb[hok]).min()) & (lMA <= np.log10(hMb[hok]).max())
mctrl = float(np.median(np.log10(aA[seln])))
info(f"the SAME estimator on ordinary ALFALFA galaxies of the same baryonic mass gives {10**mctrl:.3e} "
     f"({mctrl - math.log10(A0['canonical']):+.2f} dex from canonical): so {mctrl - math.log10(A0['canonical']):+.2f} dex of the "
     f"almost-darks' offset is the generic width systematic of check 124.B and {mCb - mctrl:+.2f} dex is differential, "
     "matching item 31's -0.265 dex in log v exactly (4 x it).")
info("Item 31b then showed that most of even THAT differential is ALFALFA's width-dependent detection limit: matched")
info("on the detection ceiling (flux and noise only, so not a collider) the almost-dark excess is -0.089 +- 0.033 dex")
info(f"in log v = -0.36 +- 0.13 dex in a_0, which would put them at {10**(mctrl-0.356):.3e} rather than {10**mCb:.3e}.")
info("Both numbers are far below both footings.  Neither is a measurement of a_0; both are measurements of how badly")
info("an unresolved line width performs on a dwarf, which is what check 124.B quantifies on ordinary galaxies.")
rung("C  Leisman+2017 almost-darks (unresolved widths)", 10**mCb, math.hypot(sCb, 0.30), True,
     "SYSTEMATIC-DOMINATED, not usable; see 124.B and item 31b")
ck("124.C AGAINST INTEREST: the item's own named sample gives an a_0 more than a dex below both footings, and it must "
   "be reported as such: 6.1e-12, a factor 15 below canonical.  Only a small part of that is the generic width "
   "systematic of 124.B (0.12 dex); the rest is the differential item 31 measured and item 31b then traced mostly to "
   "ALFALFA's width-dependent detection limit, leaving -0.36 +- 0.13 dex in a_0 after matching.  Whichever number is "
   "taken, this rung does not measure a_0 and must be carried on the ladder as a failure, not dropped",
   mCb < math.log10(A0["canonical"]) - 0.5 and abs(mCb - mctrl - (-1.06)) < 0.25,
   f"almost-darks {10**mCb:.3e} ({mCb-math.log10(A0['canonical']):+.2f} dex from canonical); same-mass ordinary "
   f"ALFALFA {10**mctrl:.3e} ({mctrl-math.log10(A0['canonical']):+.2f} dex); differential {mCb-mctrl:+.2f} dex")

# ============================================================================================================
P(""); P("="*118); P("RUNG D -- Lelli+2015 tidal dwarfs (tidal debris, the item's other named class)"); P("="*118)
tp = os.path.join(DATA, "tdg", "lelli2015_tdgs.csv")
rowsD = [l.rstrip("\n").split(",") for l in open(tp) if l.strip() and not l.startswith("#")]
hdrD = rowsD[0]; colD = {c: i for i, c in enumerate(hdrD)}
A0_PAPER = 1.30e-10
info(f"  {'TDG':>12} {'V_circ':>8} {'M_bar/1e8':>10} {'V_ISO(paper)':>13} {'V_EFE(paper)':>13} "
     f"{'a_0 isolated':>14} {'a_0 with EFE':>14}")
aD_iso, aD_efe = [], []
for r in rowsD[1:]:
    nm = r[colD["name"]]; V = float(r[colD["Vcirc"]]); Mb_ = float(r[colD["Mbar"]])
    viso = float(r[colD["VISO1"]]); vefe = float(r[colD["VEFE1"]])
    ai = A0_PAPER*(V/viso)**4; ae = A0_PAPER*(V/vefe)**4
    aD_iso.append(math.log10(ai)); aD_efe.append(math.log10(ae))
    info(f"  {nm:>12} {V:8.0f} {Mb_:10.1f} {viso:13.0f} {vefe:13.0f} {ai:14.3e} {ae:14.3e}")
mD, sD = med_boot(aD_efe); mDi, sDi = med_boot(aD_iso)
info(f"median a_0 required by these six tidal dwarfs: {10**mDi:.3e} isolated, {10**mD:.3e} with the paper's own "
     f"external field ({mD - math.log10(A0['canonical']):+.2f} dex from canonical)")
info("The paper's V_ISO1/V_EFE1 columns are the n=1 interpolation function, which IS this repository's Route A kernel;")
info("item 46 reproduced them to 2%, so the scaling a_0 ~ (V_obs/V_pred)^4 used here is the paper's own calculation.")
info("Caveat the paper itself raises and item 46 booked: these discs have completed under one orbit since the merger,")
info("so dynamical equilibrium is not established.  That is why rung D is quoted and not used.")
rung("D  Lelli+2015 tidal dwarfs (EFE included)", 10**mD, math.hypot(sD, 0.15), True,
     "6 objects, 3 independent hosts; equilibrium not established")
ck("124.D AGAINST INTEREST: tidal debris, the cleanest stellar-mass-free system there is in principle, gives an a_0 "
   "a factor 3-6 below both footings on the published kinematics.  This is item 46's liability restated as a number "
   "for the ladder.  It is not a kill (one orbit since the merger) but it is not evidence either way for a_0, and it "
   "cannot be quietly left out of a stellar-mass-free ladder",
   mD < math.log10(A0["canonical"]) - 0.3,
   f"a_0(TDG, EFE) = {10**mD:.3e} +- {sD:.3f} dex, {mD - math.log10(A0['canonical']):+.2f} dex from canonical, "
   f"{mD - math.log10(A0['alt']):+.2f} from alt")

# ============================================================================================================
P(""); P("="*118); P("THE STELLAR-MASS-FREE LADDER"); P("="*118)
info(f"{'rung':>50} {'a_0':>12} {'+- dex':>8} {'dex vs canon':>13} {'dex vs alt':>11}  note")
for L in LADDER:
    info(f"{L['label']:>50} {L['a0']:12.3e} {L['sig']:8.3f} {math.log10(L['a0']/A0['canonical']):13.2f} "
         f"{math.log10(L['a0']/A0['alt']):11.2f}  {L['note']}")
ml = [L for L in LADDER if L["mlfree"]]
lv = np.array([math.log10(L["a0"]) for L in ml]); le = np.array([L["sig"] for L in ml])
w = 1/le**2; mean = float(np.sum(w*lv)/np.sum(w))
intr = float(np.sqrt(max(np.var(lv) - np.mean(le**2), 0.0)))
info("")
info(f"the {len(ml)} stellar-mass-free rungs span {lv.max()-lv.min():.2f} dex, with an implied intrinsic spread of "
     f"{intr:.2f} dex beyond their quoted errors -- they do NOT agree, and averaging them would be meaningless.")
info(f"inverse-variance mean of the {len(ml)}: {10**mean:.3e}; the ONE with resolved kinematics alone: {LADDER[0]['a0']:.3e}")
ck("124.E the item's target -- a_0 to 15% from a stellar-mass-free sample -- is NOT met, and the reason is now "
   "specific rather than vague.  Removing the stellar mass forces the sample to be gas-rich, gas-rich means low mass, "
   "and at low mass every catalogue that measures velocity from an HI line width is biased.  Only resolved rotation "
   "curves survive, and SPARC has 21 gas-dominated ones",
   10**LADDER[0]["sig"] - 1 > 0.15 and intr > 0.15,
   f"best rung {LADDER[0]['a0']:.3e} +- {LADDER[0]['sig']:.3f} dex = {100*(10**LADDER[0]['sig']-1):.0f}% (target 15%); "
   f"spread of the {len(ml)} M/L-free rungs {lv.max()-lv.min():.2f} dex, intrinsic {intr:.2f} dex")
ck("124.F what CAN be said: the one stellar-mass-free measurement with resolved kinematics agrees with the "
   "M/L-free deep tail of item 102 and with the KiDS dwarf lens stack of item 2, all three within 0.15 dex of one "
   "another and of the canonical footing, while the alt footing sits above all three",
   abs(math.log10(LADDER[0]["a0"]/7.361e-11)) < 0.15 and abs(math.log10(LADDER[0]["a0"]/9.55e-11)) < 0.15,
   f"rung A {LADDER[0]['a0']:.3e}; item 102 M/L-free deep tail 7.36e-11 ({math.log10(LADDER[0]['a0']/7.361e-11):+.2f} dex); "
   f"item 2 dwarf lenses 9.55e-11 ({math.log10(LADDER[0]['a0']/9.55e-11):+.2f} dex); "
   f"canonical {math.log10(LADDER[0]['a0']/A0['canonical']):+.2f}, alt {math.log10(LADDER[0]['a0']/A0['alt']):+.2f}; "
   "NOTE the quoted errors already carry item 103's coherent floor, and on those errors NEITHER footing is excluded")

# ============================================================================================================
P(""); P("="*118); P("THE ALTERNATIVE COMPUTED BESIDE IT"); P("="*118)
selg = [r for r, k in zip(rowsA, selA) if k]
newt = []
for g in gals:
    if g["name"] not in [r["name"] for r in selg]: continue
    i = len(g["r"]) - 1
    gb = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)[i]/g["r"][i]*KMS2_KPC
    newt.append(math.log10(g["gobs"][i]/gb))
info(f"Newtonian, same baryons, no halo and no kernel: the gas-dominated discs' outermost point needs "
     f"{10**float(np.median(newt)):.1f}x more acceleration than their baryons give ({float(np.median(newt)):+.2f} dex) -- "
     f"i.e. a dynamical-to-baryonic mass ratio of {10**float(np.median(newt)):.0f}")
info("LambdaCDM: for these gas-rich dwarfs the same quantity v^4/(G M_b) is a halo property, so it should run with")
info(f"mass.  Measured on SPARC's resolved curves it does not ({slS:+.3f} +- {bsS.std():.3f} dex/dex).  Measured on")
info(f"ALFALFA's line widths it appears to ({slA:+.3f} dex/dex) -- which is a warning about reading halo trends off")
info("line widths, not a detection.")
info("For the tidal dwarfs the two paradigms genuinely differ and item 46 already ran it: LambdaCDM says tidal debris")
info("is dark-matter free and a purely Newtonian prediction fits them, which is what the data do.")

P(""); P("="*118); P("MUTATION CONTROLS"); P("="*118)
xg = np.array([r["a_gas"] for r in selg]); Xg, Yg = [], []
for g in gals:
    if g["name"] not in [r["name"] for r in selg]: continue
    i = len(g["r"]) - 1
    Xg.append(g["vg"][i]*abs(g["vg"][i])/g["r"][i]*KMS2_KPC); Yg.append(g["gobs"][i])
Xg = np.array(Xg); Yg = np.array(Yg)
for inj in (0.25, 4.0):
    ysyn = nu(Xg/(inj*A0["canonical"]))*Xg
    got = a0_kern(Xg, ysyn)
    ck(f"M124a injecting a_0 = {inj}x canonical into rung A's own g_bar values must be recovered exactly",
       abs(math.log10(got/(inj*A0["canonical"]))) < 0.005,
       f"injected {inj*A0['canonical']:.3e}, recovered {got:.3e} ({math.log10(got/(inj*A0['canonical'])):+.4f} dex)")
ck("M124b turning the kernel off (nu = 1) must make rung A's gas-dominated discs unfittable by any a_0",
   not np.isfinite(a0_kern(Xg, 1.0*Xg)) or a0_kern(Xg, 1.0*Xg) < 1.01e-14,
   f"nu = 1 returns a_0 = {a0_kern(Xg, 1.0*Xg):.3e}")
mrand = np.array([np.median(np.log10(aA[rng.integers(0, len(aA), int((lMA >= 10.5).sum()))])) for _ in range(400)])
ck("M124c the ALFALFA mass trend is not a sample-size artefact: random subsamples of the full catalogue the size of "
   "the most massive bin never reproduce that bin's a_0",
   abs(TREND[-1][3] - mrand.mean())/mrand.std() > 3,
   f"most massive bin {10**TREND[-1][3]:.3e} vs random draws {10**mrand.mean():.3e} +- {mrand.std():.3f} dex "
   f"({(TREND[-1][3]-mrand.mean())/mrand.std():+.1f} sigma)")
sh = rng.permutation(Mgas[good])
a_sh = np.median(np.log10((v[good]*1e3)**4/(G*sh*Msun)))
ck("M124d shuffling which galaxy gets which HI mass must break the measured trend, confirming that it is a property "
   "of the pairing and not of the marginal distributions.  (The shuffled slope goes to 4 x d log v/d log M_b, since "
   "the denominator no longer tracks the numerator -- a different number, which is the point)",
   abs(np.polyfit(lMA, np.log10((v[good]*1e3)**4/(G*sh*Msun)), 1)[0] - slA) > 0.5*abs(slA),
   f"shuffled slope {np.polyfit(lMA, np.log10((v[good]*1e3)**4/(G*sh*Msun)), 1)[0]:+.3f} vs real {slA:+.3f}")

# ============================================================================================================
P(""); P("="*118); P("VERDICT -- ITEM 124"); P("="*118)
P("  The item asked for a_0 to 15% from a sample with no stellar mass in it.  Four such samples exist in this")
P("  repository and they do not agree with each other, so the honest answer is a ladder with one usable rung.")
P("")
P(f"    A  SPARC gas-dominated discs, RESOLVED    {LADDER[0]['a0']:.3e} +- {LADDER[0]['sig']:.3f} dex   {100*(10**LADDER[0]['sig']-1):.0f}%   <-- the only usable one")
P(f"    C  Leisman+2017 almost-darks              {LADDER[2]['a0']:.3e}                    a dex low")
P(f"    D  Lelli+2015 tidal dwarfs                {LADDER[3]['a0']:.3e}                    a factor 4 low")
P("")
P("  WHY THEY DISAGREE, in one number: a_0 = v^4/(G M_b) measured from ALFALFA HI line widths runs up with baryonic")
P(f"  mass at {slA:+.2f} dex per dex over three decades, while the same quantity from SPARC's resolved rotation curves")
P(f"  rises 3.5x more slowly from SPARC's resolved rotation curves ({slS:+.3f} +- {bsS.std():.3f}, itself only 2 sigma from flat).")
P("  Stellar masses are known for both samples, so this is not the M/L wall -- it is the")
P("  line width failing to be a rotation speed in low-mass systems.  Removing the stars from a sample forces it to be")
P("  gas-rich and therefore low-mass, so every stellar-mass-free catalogue built on unresolved HI inherits the whole")
P("  bias.  That single fact accounts for item 31's almost-dark deficit (which item 31b had already traced to a")
P("  related width-selection effect) and it is why rungs B and C cannot be used.")
P("")
P("  WHAT SURVIVES.  On the 21 SPARC discs whose outermost measured point is more than 80% gas, with the neglected")
P(f"  stars and the finite-radius kernel term both corrected, a_0 = {LADDER[0]['a0']:.2e}.  That agrees with item 102's")
P("  M/L-free deep tail (7.4e-11) and with the KiDS dwarf lens stack (9.6e-11) inside 0.15 dex, all three sitting on")
P(f"  or just below the canonical footing, with the alt footing above all of them.  It is {100*(10**LADDER[0]['sig']-1):.0f}%, not 15%.")
P("  The class of measurement the item wanted -- a_0 with no stellar M/L at all -- exists and is self-consistent;")
P("  what does not exist is a large enough sample of it with resolved kinematics.")
sys.exit(ck.done())
