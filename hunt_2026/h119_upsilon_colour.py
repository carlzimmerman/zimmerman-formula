#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h119_upsilon_colour.py -- HUNT ITEM 119: A STELLAR MASS-TO-LIGHT / COLOUR RELATION DERIVED FROM THE COSMOLOGICAL CONSTANT.
==========================================================================================================================
THE ITEM.  Item 76 showed that with a_0 fixed by Planck's rho_Lambda the deep tail of SPARC's rotation curves PREDICTS the
population-average 3.6 um stellar mass-to-light ratio with no fitting.  Item 119 asks for the per-galaxy version: fix a_0,
solve EACH galaxy's rotation curve for its OWN Upsilon_disk, and plot the answer against colour.  If the framework is right,
that is a Upsilon(colour) relation DERIVED from Lambda -- a stellar-population relation obtained from gravity -- and it must
agree with the one stellar-population synthesis gives (Bell & de Jong 2001; McGaugh & Schombert 2014; Meidt+2014;
Schombert, McGaugh & Lelli 2019) in BOTH slope and zero-point.

THE ESTIMATOR.  For each galaxy, with a_0 held FIXED (no per-galaxy a_0, no free acceleration scale anywhere):
    g_bar(r; U) = [ V_gas|V_gas| + U V_disk^2 + 1.4 U V_bul^2 ] / r        (SPARC rotmod columns, Upsilon_bul = 1.4 Upsilon_disk)
    V_pred(r)   = sqrt( g_bar nu(g_bar/a_0) r ),   nu(y) = 1/(1 - e^{-sqrt y})     [Route A]
    Upsilon     = argmin_U  sum_i (V_obs,i - V_pred,i)^2 / eV_i^2 ,  1-sigma from Delta chi^2 = 1.
The ONLY free parameter per galaxy is U itself; a_0 is a constant of nature here, not a fit parameter.

THE COLOUR.  SPARC's master table carries no colour (checked: L[3.6] is a luminosity, and prep_2026/a0_line_mlpriors/SETUP.md
records the same absence).  Fetched this session from the VizieR CfA mirror and cross-matched on SIMBAD positions:
    sparc_lelli2016_table1_pos.tsv    J/AJ/152/157/table1   SPARC master table WITH positions
    rc3_devaucouleurs1991_colors.tsv  VII/155/rc3           RC3: (B-V)_T, (B-V)_oT, B_T, T
94 of the 175 SPARC galaxies have an RC3 (B-V)_T inside 40 arcsec (median separation 6 arcsec).  BOTH colours are carried:
(B-V)_T is the observed total colour and (B-V)_oT is corrected for Galactic AND internal extinction -- and the internal
correction is a function of INCLINATION, which also enters Upsilon, so a spurious correlation is possible.  Using both, and
testing log Upsilon against inclination directly, is how that trap is checked rather than assumed away.  Hubble type T is
also carried as the fallback proxy the item allows, on the larger 120-galaxy sample, with d(B-V)/dT measured from the
overlap so the T-slope can be read as a colour slope.

WHAT IS BEING CLAIMED AND WHAT IS NOT (bug pattern 5, stated up front).  The hunt's fifth recurring bug is "a result that is
really about the stellar mass-to-light ratio wearing a_0's clothes".  This item is that result ON PURPOSE: it is a
measurement OF Upsilon.  The lever is exact and is quoted rather than hidden -- in the deep-MOND limit g_obs^2 = a_0 g_bar
so Upsilon ~ 1/a_0, i.e. d log Upsilon / d log a_0 = -1.  Consequence, and it is the point of the item:
    * the ZERO-POINT of the derived relation is footing-dependent (canonical and alt differ by 0.082 dex by construction);
    * the SLOPE against colour is footing-INSENSITIVE, because a change in a_0 slides every galaxy by nearly the same amount.
"Nearly", and the script measures how nearly rather than assuming it -- see M119-3, which is a control that FAILED as first
written and is corrected in place.  The exponent is -1 only in the deep-MOND limit; SPARC is not entirely there, so the
measured d log Upsilon/d log a_0 is about -0.78 and, because redder galaxies sit at higher g_bar/a_0 and therefore move
LESS, a change in a_0 tilts the relation as well as sliding it.  Across the two footings (0.082 dex) that tilt is 0.038,
one sixth of the slope's own error, so the footing choice does not touch the conclusion.  Across a factor of three in a_0
it is 0.58, which is larger than the slope itself.  The correct statement is therefore the narrow one: the slope is
insensitive to a_0 over the range the two footings span, and NOT a_0-free in general.

Both footings on every number.  Mutation controls.  The Newtonian/LambdaCDM alternative computed beside.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from hunt_lib import *
from hunt_lib import _f

ck = Check(); rng = np.random.default_rng(119)

# ---- stellar-population anchors.  PROVENANCE, stated because it matters to how the checks below are posed:
# Upsilon_[3.6] = 0.5 +- 0.1 with ~0.1 dex TOTAL scatter is this repository's own committed SPS anchor
# (prep_2026/a0_line_mlpriors/SETUP.md, from McGaugh & Schombert 2014; Meidt+2014; Schombert-McGaugh-Lelli 2019).
# The colour SLOPE is quoted from the published colour-M/L tables (Bell & de Jong 2001; Bell+2003 Table 7), which are NOT
# in VizieR and so are not machine-verifiable in this environment.  Rather than lean on one remembered decimal, the check
# is posed against BRACKETS wide enough to contain every published calibration of each kind:
SPS_U, SPS_U_E = 0.50, 0.10          # Upsilon_[3.6], SPS
SPS_SCATTER = 0.10                   # dex, total SPS scatter at 3.6 um
SHALLOW = (0.00, 0.30)               # d log Upsilon / d(B-V): every published NEAR-IR / 3.6 um calibration (K-band ~0.135)
STEEP   = (0.60, 1.80)               # what the same coefficient is in OPTICAL bands (B-band ~1.7): the "wrong band" answer

P("="*118); P("ITEM 119 -- per-galaxy Upsilon solved from the rotation curve with a_0 fixed, against colour"); P("="*118)

# ------------------------------------------------------------------ data
gals = load_sparc()
def _tsv(fname):
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fname), encoding="latin-1")
            if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    return [{hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))} for r in rows[3:]]
spos = _tsv("sparc_lelli2016_table1_pos.tsv")
rc3  = _tsv("rc3_devaucouleurs1991_colors.tsv")
pos = {r["Name"].strip(): (_f(r["_RAJ2000"]), _f(r["_DEJ2000"])) for r in spos}
ra3 = np.array([_f(r["_RAJ2000"]) for r in rc3]); de3 = np.array([_f(r["_DEJ2000"]) for r in rc3])
bvT = np.array([_f(r["B-VT"]) for r in rc3]); bvO = np.array([_f(r["B-VoT"]) for r in rc3])
ebv = np.array([_f(r["e_B-VT"]) for r in rc3])
MATCH_AS = 40.0
COL, SEP = {}, []
for nm, (ra, de) in pos.items():
    if not np.isfinite(ra): continue
    d = np.hypot((ra3 - ra)*math.cos(math.radians(de)), de3 - de)*3600
    i = int(np.nanargmin(d))
    if d[i] < MATCH_AS and np.isfinite(bvT[i]):
        COL[nm] = (bvT[i], bvO[i], ebv[i]); SEP.append(d[i])
info(f"SPARC: {len(gals)} galaxies pass the standard cuts (Q <= 2, i >= 30 deg, >= 6 rotation-curve points)")
info(f"RC3 cross-match within {MATCH_AS:.0f} arcsec: {len(COL)} SPARC galaxies get a (B-V)_T "
     f"(median separation {np.median(SEP):.1f} arcsec, worst {max(SEP):.1f}); "
     f"{sum(1 for v in COL.values() if np.isfinite(v[1]))} also get the extinction-corrected (B-V)_oT")

# ------------------------------------------------------------------ the estimator
def fit_ups(g, a0, ratio=1.4, sD=1.0, sI=1.0, newton=False, lo=0.02, hi=6.0):
    """Upsilon_disk from one rotation curve at FIXED a_0.  sD rescales the distance, sI rescales the inclination
    correction (V_obs -> V_obs * sin i / sin i').  Returns (U, U_lo, U_hi, chi2/N, N)."""
    r = g["r"]*sD; vo = g["vobs"]*sI; ev = np.maximum(g["ev"], 2.0)*sI
    s = math.sqrt(sD); vg = g["vg"]*s; vd = g["vd"]*s; vb = g["vb"]*s
    def chi2(u):
        gb = np.maximum((vg*np.abs(vg) + u*vd**2 + ratio*u*vb**2)/r*KMS2_KPC, 1e-18)
        vp = np.sqrt(gb*(1.0 if newton else nu(gb/a0))*r/KMS2_KPC)
        return float(np.sum(((vo - vp)/ev)**2))
    res = minimize_scalar(chi2, bounds=(lo, hi), method="bounded", options={"xatol": 1e-4})
    u, c0 = res.x, res.fun
    f = lambda x: chi2(x) - c0 - 1.0
    try: uhi = brentq(f, u, hi) if f(hi) > 0 else hi
    except Exception: uhi = hi
    try: ulo = brentq(f, lo, u) if f(lo) > 0 else lo
    except Exception: ulo = lo
    return u, ulo, uhi, c0/len(r), len(r)

# fractional contribution of the STELLAR DISC to g_bar at the fiducial Upsilon: if this is small the fit cannot see U
def f_disk(g):
    num = UPS_D*g["vd"]**2
    den = np.maximum(g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2, 1e-9)
    return float(np.mean(num/den))

RAIL_LO, RAIL_HI, FDISK_MIN = 0.03, 5.9, 0.35
FIT = {}
for foot, a0 in A0.items():
    rows = []
    for g in gals:
        u, ul, uh, rc2, n = fit_ups(g, a0)
        c = COL.get(g["name"], (np.nan, np.nan, np.nan))
        rows.append(dict(name=g["name"], U=u, Ulo=ul, Uhi=uh, rchi2=rc2, n=n, fd=f_disk(g),
                         T=g["T"], L36=g["L36"], D=g["D"], eD=g["eD"], inc=g["inc"], einc=g["einc"],
                         MHI=g["MHI"], bvT=c[0], bvO=c[1], ebv=c[2], g=g))
    FIT[foot] = rows

# ------------------------------------------------------------------ sample, rails, honest attrition
r0 = FIT["canonical"]
rail = [x for x in r0 if x["U"] <= RAIL_LO or x["U"] >= RAIL_HI]
lowd = [x for x in r0 if x["fd"] < FDISK_MIN]
info(f"per-galaxy fits at fixed a_0: {len(r0)} attempted; {len(rail)} rail against the "
     f"[{RAIL_LO}, {RAIL_HI}] bounds; {len(lowd)} have a stellar disc contributing < {FDISK_MIN:.0%} of g_bar "
     f"(gas-dominated: Upsilon is barely visible in the curve and those are exactly item 121's calibrators)")
info("railed / disc-invisible galaxies: " + ", ".join(sorted(set([x['name'] for x in rail] + [x['name'] for x in lowd])))[:400])

def sel(rows, need_colour=True, col="bvO"):
    out = []
    for x in rows:
        if x["U"] <= RAIL_LO or x["U"] >= RAIL_HI: continue
        if x["fd"] < FDISK_MIN: continue
        if need_colour and not np.isfinite(x[col]): continue
        out.append(x)
    return out

# ------------------------------------------------------------------ the error budget on log Upsilon, per galaxy
P(""); info("--- error budget on log10 Upsilon, per galaxy: statistical (Delta chi^2 = 1), distance, inclination ---")
BUD = {}
for foot, a0 in A0.items():
    st, ed, ei = [], [], []
    for x in sel(FIT[foot], need_colour=False):
        g = x["g"]
        st.append((math.log10(x["Uhi"]) - math.log10(max(x["Ulo"], 1e-3)))/2)
        fD = min(g["eD"]/g["D"], 0.45)
        up = fit_ups(g, a0, sD=1 + fD)[0]; um = fit_ups(g, a0, sD=max(1 - fD, 0.2))[0]
        ed.append(abs(math.log10(max(up, 1e-3)/max(um, 1e-3)))/2)
        i0 = math.radians(g["inc"]); di = math.radians(min(g["einc"], 20))
        sp = math.sin(i0)/math.sin(min(i0 + di, math.radians(89.5)))
        sm = math.sin(i0)/math.sin(max(i0 - di, math.radians(5)))
        uip = fit_ups(g, a0, sI=sp)[0]; uim = fit_ups(g, a0, sI=sm)[0]
        ei.append(abs(math.log10(max(uip, 1e-3)/max(uim, 1e-3)))/2)
        for k, v in (("e_stat", st[-1]), ("e_D", ed[-1]), ("e_i", ei[-1])):
            x[k] = v if np.isfinite(v) else 0.30
        x["e_tot"] = math.sqrt(x["e_stat"]**2 + x["e_D"]**2 + x["e_i"]**2)
    st, ed, ei = [np.array(v)[np.isfinite(v)] for v in (st, ed, ei)]
    BUD[foot] = (np.median(st), np.median(ed), np.median(ei))
    info(f"{foot:10} median per-galaxy sigma(log Upsilon): statistical {np.median(st):.3f} dex, "
         f"distance {np.median(ed):.3f}, inclination {np.median(ei):.3f} -> combined {np.median(np.sqrt(np.array(st)**2+np.array(ed)**2+np.array(ei)**2)):.3f} dex")

# ------------------------------------------------------------------ the derived relation
def wls(x, y, w=None):
    """weighted straight-line fit.  Weights are applied as sqrt(w) row scaling and solved by lstsq rather than by
    forming A^T W A -- the normal-equation form trips numpy's matmul on the 70x70 diagonal and is worse conditioned."""
    A = np.vstack([x, np.ones_like(x)]).T
    if w is None: co = np.linalg.lstsq(A, y, rcond=None)[0]
    else:
        rw = np.sqrt(np.asarray(w, dtype=float))
        co = np.linalg.lstsq(A*rw[:, None], y*rw, rcond=None)[0]
    res = y - (co[0]*x + co[1])
    return co[0], co[1], res.std(ddof=2)

RES = {}
P(""); P("-"*118)
info(f"{'footing':>10} {'colour':>10} {'N':>4} {'median U':>9} {'sd logU':>8} "
     f"{'slope dlogU/d(B-V)':>20} {'+-':>7} {'U at median colour':>19} {'resid dex':>10}")
for foot, a0 in A0.items():
    for cname, ckey in (("(B-V)_T", "bvT"), ("(B-V)_oT", "bvO")):
        s = sel(FIT[foot], col=ckey)
        if len(s) < 20: continue
        c = np.array([x[ckey] for x in s]); lu = np.log10(np.array([x["U"] for x in s]))
        sl, ic, rsd = wls(c, lu)
        idx = [rng.integers(0, len(c), len(c)) for _ in range(2000)]
        bsl = np.array([wls(c[i], lu[i])[0] for i in idx])
        cmed = float(np.median(c)); u_at = 10**(sl*cmed + ic)
        bzp = np.array([10**(wls(c[i], lu[i])[0]*cmed + wls(c[i], lu[i])[1]) for i in idx[:600]])
        info(f"{foot:>10} {cname:>10} {len(s):4d} {np.median([x['U'] for x in s]):9.3f} {lu.std():8.3f} "
             f"{sl:20.3f} {bsl.std():7.3f} {u_at:19.3f} {rsd:10.3f}")
        RES[(foot, ckey)] = dict(N=len(s), sl=sl, esl=float(bsl.std()), ic=ic, rsd=rsd, cmed=cmed,
                                 u_at=u_at, eu_at=float(bzp.std()), med=float(np.median([x["U"] for x in s])),
                                 sdlog=float(lu.std()), c=c, lu=lu, s=s)

# error-weighted version.  The weight carries an intrinsic-scatter floor S_INT: without it a handful of galaxies with
# tiny distance errors dominate and the slope's variance EXPLODES (checked: +-0.64 unfloored against +-0.24 unweighted).
S_INT = 0.15
P("")
for foot in A0:
    s = RES[(foot, "bvO")]["s"]
    w = np.array([1.0/(max(float(x["e_tot"]), 0.02)**2 + S_INT**2) for x in s])
    c = np.array([x["bvO"] for x in s]); lu = np.log10(np.array([x["U"] for x in s]))
    slw, icw, _ = wls(c, lu, w)
    idx = [rng.integers(0, len(c), len(c)) for _ in range(1500)]
    bsw = np.array([wls(c[i], lu[i], w[i])[0] for i in idx])
    tight = np.array([x["e_tot"] < 0.15 for x in s])
    slt = wls(c[tight], lu[tight])[0] if tight.sum() > 15 else float("nan")
    bslt = np.array([wls(c[tight][i], lu[tight][i])[0]
                     for i in (rng.integers(0, tight.sum(), tight.sum()) for _ in range(1000))]) if tight.sum() > 15 else np.array([np.nan])
    info(f"{foot:10} error-WEIGHTED slope against (B-V)_oT (1/[budget^2 + {S_INT}^2]): {slw:+.3f} +- {bsw.std():.3f}; "
         f"best-measured subset only (budget < 0.15 dex, N = {tight.sum()}): {slt:+.3f} +- {bslt.std():.3f}; "
         f"unweighted {RES[(foot,'bvO')]['sl']:+.3f} +- {RES[(foot,'bvO')]['esl']:.3f}")
    RES[(foot, "bvO")]["slw"] = slw; RES[(foot, "bvO")]["eslw"] = float(bsw.std())

# ------------------------------------------------------------------ the "plot": binned, printed
P(""); info("--- the plot the item asks for, printed: derived Upsilon versus colour, canonical footing, (B-V)_oT ---")
s = RES[("canonical", "bvO")]["s"]
c = np.array([x["bvO"] for x in s]); u = np.array([x["U"] for x in s])
edges = np.percentile(c, [0, 20, 40, 60, 80, 100])
info(f"{'(B-V)_oT bin':>18} {'N':>4} {'<B-V>':>7} {'median Upsilon':>15} {'16-84%':>19} {'log sd':>8}")
for i in range(5):
    m = (c >= edges[i]) & (c <= edges[i+1] if i == 4 else c < edges[i+1])
    if m.sum() < 3: continue
    info(f"{f'{edges[i]:.2f} - {edges[i+1]:.2f}':>18} {m.sum():4d} {c[m].mean():7.3f} {np.median(u[m]):15.3f} "
         f"{f'{np.percentile(u[m],16):.2f} - {np.percentile(u[m],84):.2f}':>19} {np.log10(u[m]).std():8.3f}")
info("ASCII scatter (x = (B-V)_oT 0.2-1.0, y = log10 Upsilon -1.0 .. +0.8):")
W, H = 62, 17
grid = [[" "]*W for _ in range(H)]
for cc, uu in zip(c, u):
    ix = int(round((cc - 0.2)/0.8*(W-1))); iy = int(round((0.8 - math.log10(uu))/1.8*(H-1)))
    if 0 <= ix < W and 0 <= iy < H: grid[iy][ix] = "*" if grid[iy][ix] == " " else "#"
slc, icc = RES[("canonical", "bvO")]["sl"], RES[("canonical", "bvO")]["ic"]
for ix in range(W):
    cc = 0.2 + ix*0.8/(W-1); iy = int(round((0.8 - (slc*cc + icc))/1.8*(H-1)))
    if 0 <= iy < H and grid[iy][ix] == " ": grid[iy][ix] = "-"
    iy2 = int(round((0.8 - math.log10(SPS_U))/1.8*(H-1)))
    if 0 <= iy2 < H and grid[iy2][ix] == " ": grid[iy2][ix] = "."
for iy in range(H):
    info(f"   {0.8 - iy*1.8/(H-1):+5.2f} |" + "".join(grid[iy]))
info("         " + "+" + "-"*W)
info("          0.2" + " "*22 + "0.6" + " "*30 + "1.0     ('-' = derived relation, '.' = SPS 0.5)")

# ------------------------------------------------------------------ footing dependence: zero-point moves, slope does not
P(""); P("-"*118)
sc_can, sc_alt = RES[("canonical", "bvO")]["sl"], RES[("alt", "bvO")]["sl"]
zp_can, zp_alt = RES[("canonical", "bvO")]["u_at"], RES[("alt", "bvO")]["u_at"]
info(f"footing dependence, measured: zero-point (Upsilon at the median colour) {zp_can:.3f} canonical -> {zp_alt:.3f} alt "
     f"= {math.log10(zp_alt/zp_can):+.3f} dex, against the -log10(a0_alt/a0_can) = "
     f"{-math.log10(A0['alt']/A0['canonical']):+.3f} dex the deep-MOND lever d log U/d log a_0 = -1 predicts")
info(f"                              slope {sc_can:+.3f} canonical -> {sc_alt:+.3f} alt, a change of {abs(sc_alt-sc_can):.3f} "
     f"against a bootstrap error of {RES[('canonical','bvO')]['esl']:.3f} -- the slope is footing-free, as the algebra says")

# ------------------------------------------------------------------ CHECKS
P(""); P("="*118); P("CHECKS"); P("="*118)
Rc, Ra = RES[("canonical", "bvO")], RES[("alt", "bvO")]
d_can = abs(math.log10(Rc["u_at"]/SPS_U)); d_alt = abs(math.log10(Ra["u_at"]/SPS_U))
ck("119a (a WORKS, and it is the item's zero-point test) with a_0 FIXED by the cosmological constant and nothing else free, "
   "solving each SPARC rotation curve for its own stellar mass-to-light ratio returns a population that sits on the "
   "stellar-population value: the derived Upsilon at the sample's median colour is within 0.1 dex of 0.5 on BOTH footings",
   d_can < 0.10 and d_alt < 0.10,
   f"canonical Upsilon(median colour) = {Rc['u_at']:.3f} +- {Rc['eu_at']:.3f} ({math.log10(Rc['u_at']/SPS_U):+.3f} dex from "
   f"SPS 0.50 +- 0.10); alt {Ra['u_at']:.3f} +- {Ra['eu_at']:.3f} ({math.log10(Ra['u_at']/SPS_U):+.3f} dex); "
   f"medians {Rc['med']:.3f} / {Ra['med']:.3f} over N = {Rc['N']} / {Ra['N']}")

in_shallow = SHALLOW[0] - Rc["esl"] <= Rc["sl"] <= SHALLOW[1] + Rc["esl"]
steep_sig = (STEEP[0] - Rc["sl"])/Rc["esl"]
ck("119b the SLOPE of the derived relation is shallow, which is what the near-infrared stellar-population calibrations say "
   "and is the OPPOSITE of the steep optical colour-M/L relations -- and this is the footing-independent half of the "
   "measurement, so a_0's own factor-1.2 ambiguity cannot move it",
   in_shallow and abs(Rc["sl"]) < 0.35,
   f"d log Upsilon_[3.6] / d(B-V)_oT = {Rc['sl']:+.3f} +- {Rc['esl']:.3f} (canonical), {Ra['sl']:+.3f} +- {Ra['esl']:.3f} (alt); "
   f"near-IR bracket {SHALLOW}, optical-band bracket {STEEP}; with the observed colour, {RES[('canonical','bvT')]['sl']:+.3f} "
   f"+- {RES[('canonical','bvT')]['esl']:.3f}.  AGAINST INTEREST, the CENTRAL VALUE is estimator-dependent: weighting by "
   f"the measurement budget moves it to {Rc['slw']:+.3f} +- {Rc['eslw']:.3f}, i.e. to zero.  What is robust is the "
   f"BRACKET -- every version lands inside the near-infrared one -- not the coincidence with any particular published "
   f"coefficient, and this item must not be quoted as reproducing 0.135")

ck("119c AGAINST INTEREST -- the POWER, stated so the pass above is not over-read: the steep optical-like slope is only "
   f"{steep_sig:.1f} sigma away, so this measurement CONFIRMS the shallow near-infrared calibration without EXCLUDING the "
   "steep one at 3 sigma.  The relation is derived, but it is not yet a discriminating measurement of the colour term",
   steep_sig < 3.0,
   f"slope {Rc['sl']:+.3f} +- {Rc['esl']:.3f}; the shallow near-IR value sits at "
   f"{(0.135 - Rc['sl'])/Rc['esl']:+.1f} sigma, the low edge of the optical bracket at {steep_sig:+.1f} sigma; "
   f"3 sigma would need sigma(slope) < {abs(STEEP[0]-Rc['sl'])/3:.3f}, i.e. {int(Rc['N']*(Rc['esl']/(abs(STEEP[0]-Rc['sl'])/3))**2)} "
   f"galaxies at this scatter, or the same {Rc['N']} with the distance budget removed")

# scatter versus SPS
sd_obs = Rc["rsd"]
etot = np.array([x["e_tot"] for x in Rc["s"]])
sd_meas = float(np.sqrt(np.mean(etot**2)))
sd_int = math.sqrt(max(sd_obs**2 - sd_meas**2, 0.0))
rchi = np.array([x["rchi2"] for x in Rc["s"]])
ck("119d the SCATTER is consistent with stellar populations too -- but this is a BOUND, not a measurement, and the check "
   "text is written to say so.  The observed 0.25 dex scatter about the derived relation is almost entirely accounted "
   "for by the distance and inclination budgets alone; what is left is 0.12 dex against the 0.10 dex stellar "
   "populations allow at 3.6 um.  Since the budget nearly saturates the observed scatter, this sample has essentially "
   "NO power to detect an intrinsic Upsilon spread, and the agreement is a non-detection rather than a confirmation",
   sd_int < 2*SPS_SCATTER,
   f"scatter about the derived relation {sd_obs:.3f} dex; measurement budget (stat {BUD['canonical'][0]:.3f}, distance "
   f"{BUD['canonical'][1]:.3f}, inclination {BUD['canonical'][2]:.3f}) = {sd_meas:.3f} dex rms; implied intrinsic "
   f"{sd_int:.3f} dex against the SPS allowance of {SPS_SCATTER:.2f}.  A 10% error in the budget moves the intrinsic "
   f"figure between {math.sqrt(max(sd_obs**2-(1.1*sd_meas)**2,0)):.3f} and {math.sqrt(max(sd_obs**2-(0.9*sd_meas)**2,0)):.3f} "
   f"dex, which is the whole allowed range -- that is what 'no power' looks like numerically.  And the median reduced "
   f"chi^2 of the fits is {np.median(rchi):.2f} (mean {rchi.mean():.2f}), so some of the residual is model error -- "
   f"non-circular motions and radial M/L gradients a single Upsilon per galaxy cannot absorb -- which pushes the true "
   f"intrinsic M/L scatter DOWN, not up.  The distance budget is the thing to remove: TRGB/Cepheid distances would")
info("      cut the dominant 0.138 dex line and turn this bound into a measurement, which is exactly what item 103 asks for.")

# ------------------------------------------------------------------ is the colour trend really about luminosity?
c = Rc["c"]; lu = Rc["lu"]; lL = np.log10(np.array([x["L36"] for x in Rc["s"]]))
X = np.vstack([c, lL, np.ones_like(c)]).T
co = np.linalg.lstsq(X, lu, rcond=None)[0]
idx = [rng.integers(0, len(c), len(c)) for _ in range(1500)]
bco = np.array([np.linalg.lstsq(np.vstack([c[i], lL[i], np.ones_like(c[i])]).T, lu[i], rcond=None)[0] for i in idx])
inc_arr = np.array([x["inc"] for x in Rc["s"]])
r_inc = float(np.corrcoef(inc_arr, lu - (Rc["sl"]*c + Rc["ic"]))[0, 1])
ck("119e the colour trend is not luminosity or inclination in disguise: controlling for log L[3.6] leaves the colour "
   "coefficient where it was, the luminosity coefficient is consistent with zero, and the residual does not correlate "
   "with inclination -- which is the trap the extinction-corrected colour could have set, since its internal-extinction "
   "term is itself a function of inclination",
   abs(co[1]) < 3*bco[:, 1].std() and abs(r_inc) < 0.30,
   f"joint fit: colour {co[0]:+.3f} +- {bco[:,0].std():.3f} (alone {Rc['sl']:+.3f}), log L[3.6] {co[1]:+.3f} +- "
   f"{bco[:,1].std():.3f} ({co[1]/bco[:,1].std():+.1f} sigma); residual-vs-inclination r = {r_inc:+.3f} over N = {len(c)}")

# ------------------------------------------------------------------ Hubble type on the larger sample
sT = sel(FIT["canonical"], need_colour=False)
tt = np.array([float(x["T"]) for x in sT]); luT = np.log10(np.array([x["U"] for x in sT]))
slT, icT, rsdT = wls(tt, luT)
bslT = np.array([wls(tt[i], luT[i])[0] for i in (rng.integers(0, len(tt), len(tt)) for _ in range(2000))])
sC = [x for x in Rc["s"]]
tc = np.array([float(x["T"]) for x in sC]); cc = np.array([x["bvO"] for x in sC])
dcdT, _, _ = wls(tc, cc)
P(""); info(f"Hubble-type proxy on the larger sample (the fallback the item allows): N = {len(tt)}, "
            f"d log Upsilon/dT = {slT:+.4f} +- {bslT.std():.4f} dex per type unit, scatter {rsdT:.3f} dex")
info(f"the overlap measures d(B-V)_oT/dT = {dcdT:+.4f} mag per type unit, so the type slope maps onto a colour slope of "
     f"{slT/dcdT:+.3f} +- {bslT.std()/abs(dcdT):.3f} -- consistent with the direct colour fit, on a 1.7x larger sample")
ck("119f the Hubble-type version, on the 1.7x larger sample that needs no colour cross-match, gives the same answer: a "
   "shallow trend of the derived Upsilon with type, which converts through the measured d(B-V)/dT into a colour slope "
   "consistent with the direct one and still inside the near-infrared bracket",
   abs(slT/dcdT - Rc["sl"]) < 3*math.sqrt((bslT.std()/abs(dcdT))**2 + Rc["esl"]**2) and abs(slT/dcdT) < 0.45,
   f"type slope {slT:+.4f} +- {bslT.std():.4f}/type -> colour slope {slT/dcdT:+.3f} +- {bslT.std()/abs(dcdT):.3f} vs the "
   f"direct {Rc['sl']:+.3f} +- {Rc['esl']:.3f}")

# ------------------------------------------------------------------ estimator-choice systematic against item 76
def tail_a0(ups_d, cut=1e-11):
    num = []
    for g in gals:
        gb = (g["vg"]*np.abs(g["vg"]) + ups_d*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC
        m = (gb > 0) & (gb < cut)
        if m.sum(): num.append(np.log10(g["gobs"][m]) - 0.5*np.log10(gb[m]))
    return 10**(2*float(np.mean(np.concatenate(num))))
U76 = {}
for foot, a0 in A0.items():
    try: U76[foot] = brentq(lambda u: tail_a0(u) - a0, 0.15, 3.0, xtol=1e-3)
    except ValueError: U76[foot] = float("nan")
P(""); info(f"item 76's deep-tail estimator on the same data requires Upsilon = {U76['canonical']:.3f} (canonical) / "
            f"{U76['alt']:.3f} (alt); this item's full-curve per-galaxy fit gives medians {Rc['med']:.3f} / {Ra['med']:.3f}")
est_sys = abs(math.log10(U76["canonical"]/Rc["med"]))
ck("119g AGAINST INTEREST -- an estimator-choice systematic on the headline number of item 76, found here and not there.  "
   "The deep-tail intercept and the full-curve per-galaxy fit are two ways of reading the SAME rotation curves at the "
   "SAME fixed a_0, and they disagree by about 0.1 dex in Upsilon.  Item 76's '0.656 canonical / 0.504 alt' therefore "
   "carries an estimator systematic of that size which was not quoted, and the 'mildly prefers the alt footing' reading "
   "is inside it",
   est_sys > 0.05,
   f"deep-tail {U76['canonical']:.3f} vs full-curve median {Rc['med']:.3f} = {est_sys:.3f} dex (canonical); "
   f"{U76['alt']:.3f} vs {Ra['med']:.3f} = {abs(math.log10(U76['alt']/Ra['med'])):.3f} dex (alt).  The two footings are "
   f"{abs(math.log10(A0['alt']/A0['canonical'])):.3f} dex apart, i.e. comparable to the estimator systematic itself")

# ------------------------------------------------------------------ MUTATION CONTROLS
P(""); P("="*118); P("MUTATION CONTROLS"); P("="*118)
bsh = np.array([wls(rng.permutation(c), lu)[0] for _ in range(2000)])
pval = float(np.mean(np.abs(bsh) >= abs(Rc["sl"])))
ck("M119-1 the colour-shuffle null, and it says the trend is NOT detected.  Randomly reassigning the colours produces a "
   "slope as large as the measured one 55% of the time.  That is the honest reading of a shallow relation and it is "
   "reported as such: what this item establishes is the ZERO-POINT of the derived Upsilon and a BOUND on its colour "
   "term, not a detection of a colour trend",
   pval > 0.05,
   f"shuffled slopes: mean {bsh.mean():+.3f}, spread {bsh.std():.3f}; the measured {Rc['sl']:+.3f} is "
   f"{Rc['sl']/bsh.std():+.1f} sigma from the null and is matched or exceeded in {100*pval:.0f}% of shuffles")

a0_bad = 3.0*A0["canonical"]
bad = [fit_ups(x["g"], a0_bad)[0] for x in Rc["s"]]
lub = np.log10(np.array(bad)); slb, icb, _ = wls(c, lub)
ck("M119-2 the ZERO-POINT can fail and does: tripling a_0 moves the derived Upsilon by the -1 power the algebra demands "
   "and takes it far outside the stellar-population range, so check 119a is a real test of the value of a_0 and not a "
   "tautology of the fitting procedure",
   abs(math.log10(np.median(bad)/SPS_U)) > 0.3,
   f"a_0 x 3 -> median Upsilon {np.median(bad):.3f} ({math.log10(np.median(bad)/SPS_U):+.2f} dex from SPS), against "
   f"{Rc['med']:.3f} at the true value; measured d log U/d log a_0 = "
   f"{math.log10(np.median(bad)/Rc['med'])/math.log10(3.0):+.2f} (algebra says -1 in the deep-MOND limit)")
dsl_foot = abs(RES[("alt", "bvO")]["sl"] - Rc["sl"]); dla_foot = abs(math.log10(A0["alt"]/A0["canonical"]))
ck("M119-3 MY OWN CLAIM, CORRECTED BY ITS OWN CONTROL.  This check was first written as 'the slope survives a factor-3 "
   "change in a_0 untouched', and it FAILED: the slope moves from +0.14 to +0.72.  The reason is real and is now stated "
   "instead of hidden -- SPARC is not entirely in the deep-MOND limit, redder galaxies sit at higher g_bar/a_0 and so "
   "respond LESS to a change in a_0, and a wrong a_0 therefore TILTS the relation as well as sliding it.  What is "
   "actually true, and is what the item needs, is the narrow statement: over the range the two footings span the tilt "
   "is a sixth of the slope's own error.  The slope is footing-insensitive; it is NOT a_0-free in general, and a large "
   "a_0 error would masquerade as a colour term",
   dsl_foot < 0.5*Rc["esl"] and abs(slb - Rc["sl"]) > Rc["esl"],
   f"across the actual footing range ({dla_foot:.3f} dex in a_0) the slope moves {dsl_foot:.3f}, against its bootstrap "
   f"error {Rc['esl']:.3f}; across a factor of 3 ({math.log10(3):.3f} dex) it moves {abs(slb-Rc['sl']):.3f}, i.e. more "
   f"than the slope itself ({slb:+.3f} vs {Rc['sl']:+.3f}).  Implied sensitivity d(slope)/d log a_0 = "
   f"{dsl_foot/dla_foot:.2f} locally, {abs(slb-Rc['sl'])/math.log10(3):.2f} over the wide range -- non-linear, as the "
   f"kernel's curvature requires")

newt = [fit_ups(x["g"], A0["canonical"], newton=True) for x in Rc["s"]]
un = np.array([v[0] for v in newt]); rc_n = np.array([v[3] for v in newt])
frac_hi = float(np.mean(un > 2*SPS_U))
ck("M119-4 the kernel is load-bearing.  With nu = 1 -- pure Newton, no dark matter, the same curves, the same fits -- "
   "the mass-to-light ratio the discs would need is nearly three times the stellar-population value and the fits are "
   "five times worse.  So the Upsilon that lands on stellar populations in check 119a comes from the kernel and the "
   "value of a_0, not from the rotation curves alone",
   np.median(un) > 2*SPS_U and np.median(rc_n) > 3*np.median(rchi),
   f"Newtonian fits: median Upsilon {np.median(un):.2f} = {math.log10(np.median(un)/SPS_U):+.2f} dex from SPS "
   f"({100*frac_hi:.0f}% of galaxies above 2x SPS), median reduced chi^2 {np.median(rc_n):.1f} against "
   f"{np.median(rchi):.2f} with the kernel; and the Newtonian Upsilon has no reason to sit anywhere in particular, "
   f"which is the point -- its spread is {np.log10(un).std():.2f} dex against {Rc['sdlog']:.2f} with the kernel")

# ------------------------------------------------------------------ the alternative, computed beside
P(""); P("="*118); P("THE LambdaCDM / NEWTONIAN ALTERNATIVE, COMPUTED BESIDE"); P("="*118)
maxd = []
for x in Rc["s"]:
    g = x["g"]
    ratio = g["vobs"]**2/np.maximum(g["vd"]**2 + 1.4*g["vb"]**2, 1e-6)
    m = g["r"] < 2.2*max(g["Rdisk"], 1e-3)
    if m.sum() == 0: m = np.ones_like(g["r"], dtype=bool)
    maxd.append(float(np.min(ratio[m])))
maxd = np.array(maxd)
info(f"With a dark halo the rotation curve does NOT determine Upsilon at all -- the halo absorbs any value below the "
     f"maximum-disc bound.  That bound, computed here inside 2.2 disc scale lengths, has median {np.median(maxd):.2f} and "
     f"spans {np.percentile(maxd,5):.2f} - {np.percentile(maxd,95):.2f}: it is an UPPER LIMIT per galaxy, not a value, and "
     f"{100*np.mean(maxd > SPS_U):.0f}% of the sample has it above the stellar-population 0.5, i.e. no information.")
info(f"So the LambdaCDM side of this item has no prediction to compare: a Upsilon(colour) relation cannot be derived from "
     f"rotation curves in a theory with a free halo.  The framework's derivation exists only because a_0 is fixed by Lambda "
     f"and the kernel leaves no other freedom.  That is the asymmetry the item is testing, and it is real -- but it also "
     f"means this item cannot DISCRIMINATE between the theories, only demonstrate that one of them makes the prediction.")

P(""); P("="*118); P("VERDICT"); P("="*118)
P(f"  The relation exists and it is derived, not fitted: a_0 = c/2 sqrt(G rho_DE) fixed, one parameter per galaxy, and the")
P(f"  answer lands on stellar populations.  Zero-point Upsilon(median colour) = {Rc['u_at']:.3f} (canonical) / {Ra['u_at']:.3f} (alt)")
P(f"  against SPS 0.50 +- 0.10; slope d log Upsilon/d(B-V)_oT = {Rc['sl']:+.3f} +- {Rc['esl']:.3f}, inside the near-infrared")
P(f"  bracket and footing-insensitive.  Four things are recorded AGAINST it.  (1) The colour trend is NOT detected: a")
P(f"  shuffle of the colours reproduces it in {100*pval:.0f}% of trials, so what stands is the zero-point and a BOUND on the colour")
P(f"  term, and the steep optical-band value is only {steep_sig:.1f} sigma away.  (2) The per-galaxy scatter agrees with stellar")
P(f"  populations ({sd_int:.2f} dex intrinsic against 0.10) only because the distance and inclination budget already saturates")
P(f"  the observed 0.25 dex -- a non-detection, not a confirmation.  (3) The slope's a_0-independence is LOCAL, not exact:")
P(f"  a factor-3 error in a_0 tilts it by {abs(slb-Rc['sl']):.2f}, more than the slope itself, because SPARC is not entirely deep-MOND.")
P(f"  (4) The same curves read with item 76's deep-tail estimator give a Upsilon {est_sys:.2f} dex away -- an estimator systematic")
P(f"  comparable to the whole gap between the two footings, which item 76 did not quote and which this item found.")
sys.exit(ck.done())
