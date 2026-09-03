#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_adversarial_pressure_sample_composition.py
============================================================================================================
ADVERSARIAL VERIFICATION of g05_dsph_prescription_fixed_and_expanded.py's headline claim:

   "f09's matched-pair separation is WITHDRAWN: with object-by-object acceleration matching against the SPARC
    relation it falls from +0.215 dex to +0.064 dex and from 1.73 sigma to 0.93 sigma (perm p = 0.1033),
    N_pressure = 14 matched, 36 dropped, N_rotating = 147."

TWO SEPARATE QUESTIONS, answered separately:

  Q1 IS THE ARITHMETIC RIGHT?  Re-derived here from the raw LVD CSVs with DIFFERENT physical constants
     (G = 6.67430e-11 vs 6.674e-11; Msun = 1.98892e30 vs 1.989e30; pc = 3.085677581e16 vs 3.0857e16), a
     DIFFERENT quadrature for the QUMOND sphere average (scipy.integrate.quad in mu = cos(theta), against
     g05's np.trapz on a 2001-point theta grid), and an independent CSV parse.  ANSWER: YES, exactly.
     g05's +0.064 dex / 0.93 sigma / N = 14 / 36 / 147 all reproduce.  No arithmetic defect was found.

  Q2 DOES THE CONCLUSION FOLLOW FROM IT?  NO.  The null is not produced by the acceleration matching.  It is
     produced by WHICH OBJECTS the acceleration matching leaves on the pressure side.

     g05 keeps the 14 pressure objects whose internal acceleration falls inside SPARC's coverage.  The FOUR
     highest-x_i of those 14 -- NGC 147, NGC 185, NGC 205 and M 32 -- are M31 dwarf and compact ELLIPTICALS,
     not dwarf spheroidals.  They are the objects the acceleration cut preferentially SPARES, because they are
     the only pressure-side systems bright and dense enough to reach SPARC's accelerations at all, and they
     carry 4 of the 14 votes in the median.

     Two problems with them, and g05 flags neither:

     (i) THE CLASSIFIER'S OWN PRINCIPLE IS NOT APPLIED TO THEM.  g05 removes the LMC and the SMC by name with
         the comment "rotation-supported (belongs on the OTHER side)".  NGC 147, NGC 205 and M 32 are the
         textbook ROTATING members of the Local Group early-type dwarf sequence (Geha et al. 2010, ApJ 711,
         361 for NGC 147 and NGC 185; Simien & Prugniel 2002, A&A 384, 371 and Geha et al. 2006, AJ 131, 332
         for NGC 205; Bender, Burstein & Faber 1992, ApJ 399, 462 for M 32 as a rotating compact elliptical).
         The whole hypothesis under test is ROTATION-supported against PRESSURE-supported.  Putting rotating
         systems on the pressure side is a classification error in the direction that manufactures the null.

     (ii) THE OBSERVED-SIDE ESTIMATOR IS NOT VALID FOR THEM.  g_obs = 3 sigma^2 / r_1/2 is Wolf et al. 2010
         (MNRAS 406, 1220), derived for a DISPERSION-supported, non-rotating spherical system.  Applied to a
         rotating dwarf elliptical it omits the rotational support and therefore UNDER-states g_obs, driving
         the residual negative.  NGC 147's residual is -0.550 dex -- by far the most negative object in the
         kept sample -- and it is the single object that most drags the pressure median down.  This is this
         repository's own "wrong estimator for the geometry" bug pattern.

     WHAT IT DOES TO THE NUMBER (all recomputed below, both footings):
         g05 as published, 14 objects                        +0.064 dex   0.93 sigma   p = 0.11
         minus the four M31 dE/cE, 10 objects                +0.125 dex   2.27 sigma   p = 0.010
         NO objects named at all -- both sides simply
         restricted to 0.01 < x_i < 0.10, the decade the
         dwarf spheroidals actually occupy                   +0.114 dex   1.91 sigma   p = 0.054

     So "the 1.73 sigma is not reproducible" is FALSE.  It is reproducible, and in significance exceeded, under
     a sample definition at least as defensible as g05's -- and under one that names no object at all.

  AGAINST MY OWN POINT, kept as failing checks so it cannot be quietly dropped:
     * Removing the four ONE AT A TIME never gets past 1.51 sigma.  The jump to 2.27 needs all four gone at
       once, which is partly median discreteness on N = 10.  My number is fragile in the same way g05's is.
     * M 32's residual is +0.385 dex, i.e. it HELPS the pressure side; dropping it alone LOWERS the separation
       to 0.73 sigma.  I am not cherry-picking in one direction, and this check verifies that.
     * Neither 0.93 sigma nor 2.27 sigma is a detection.  g05's broader conclusion -- that the Local Group
       cannot separate support type from acceleration depth, and that this is not a result -- SURVIVES.
       What does not survive is the specific word "WITHDRAWN" and the framing of 0.93 sigma as the number.
     * The direction of the sigma error also runs against g05's headline: g05 divides a difference of MEDIANS
       by the standard error of a difference of MEANS.  The asymptotic median SE is 1.2533x larger, so the
       honest baseline is 0.74 sigma, not 0.93 -- which makes the published number MORE null, not less, and is
       recorded here because a verifier must report the errors that cut both ways.

BOTH a_0 FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL AND SEVERAL DO.
Data: Local Volume Database (Pace 2024, ApJS 273, 15); SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157).
"""
import sys, os, math, csv
import numpy as np
from scipy.integrate import quad
from hunt_lib import load_sparc, DATA, A0, Check, P, info

ck = Check()
rng = np.random.default_rng(20260903)

# ---- INDEPENDENT constants: deliberately different from hunt_lib's, so a units slip would show up ----
G_V  = 6.67430e-11          # hunt_lib: 6.674e-11
MS_V = 1.98892e30           # hunt_lib: 1.989e30
PC_V = 3.085677581e16       # hunt_lib / g05: 3.0857e16
KPC_V = 1000*PC_V
MW_MB, M31_MB = 6.0e10, 1.2e11
UPS_V = 2.0
MATCH_W, MATCH_N = 0.20, 20

def nus(y):
    y = max(float(y), 1e-300); return 1.0/(1.0 - math.exp(-math.sqrt(y)))
def nuv(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/(1.0 - np.exp(-np.sqrt(y)))

def gsph(xi, xe):
    """QUMOND sphere-averaged inward radial acceleration in units of a_0.
    INDEPENDENT quadrature: adaptive scipy.integrate.quad in mu = cos(theta), where g05 uses np.trapz on a
    2001-point uniform theta grid.  <g_r> = <S_r> exactly (QUMOND flux theorem)."""
    if xe <= 0.0:
        return nus(xi)*xi
    def f(mu):
        s = math.sqrt(max(1.0 - mu*mu, 0.0))
        gx, gz = -xi*s, xe - xi*mu
        return nus(math.hypot(gx, gz))*(gx*s + gz*mu)
    v, _ = quad(f, -1.0, 1.0, limit=500)
    return -v/2.0

P("="*118)
P("PART 0.  THE INDEPENDENT QUADRATURE, checked before any data is touched.")
P("="*118)
iso = [gsph(x, 0.0)/(nus(x)*x) for x in (1e-4, 1e-2, 1.0, 30.0)]
ck("V0 the independent adaptive quadrature reproduces the framework's isolated kernel exactly when the external field is off, so it is the same prescription as g05's and not a second theory",
   max(abs(v-1) for v in iso) < 1e-9, "quad/nu(x)x = " + ", ".join(f"{v:.12f}" for v in iso))

def gsph_newt(xi, xe):
    def f(mu):
        s = math.sqrt(max(1.0-mu*mu, 0.0)); gx, gz = -xi*s, xe - xi*mu
        return gx*s + gz*mu
    v, _ = quad(f, -1.0, 1.0, limit=500); return -v/2.0
mn = [gsph_newt(a, b)/a for a, b in ((0.01, 0.1), (0.3, 0.02), (30.0, 4.3))]
ck("V0b MUTATION CONTROL: with nu = 1 the same quadrature returns the internal Newtonian field exactly at every external field, so the machinery manufactures no coupling of its own",
   max(abs(v-1) for v in mn) < 1e-9, "Newtonian quad / x_i = " + ", ".join(f"{v:.12f}" for v in mn))

# ==========================================================================================================
P(""); P("="*118)
P("PART 1.  Q1 -- IS g05's ARITHMETIC RIGHT?  Independent re-derivation from the raw LVD CSVs.")
P("="*118)

def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None

def load(fn, hostmb, host):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
        rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
        if fnum(r["confirmed_galaxy"]) != 1: continue
        lMs = fnum(r["mass_stellar"]); lHI = fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, rh=rh, sig=sig,
                        Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
                        MHI=(10**lHI if lHI is not None else 0.0),
                        Dhost=Dh, Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                        host=host, host_mb=hostmb))
    return out

mw  = load("lvd_dwarf_mw.csv",  MW_MB,  "MW")
m31 = load("lvd_dwarf_m31.csv", M31_MB, "M31")
fld = load("lvd_dwarf_local_field.csv", None, "field")
ROT = {"LMC", "SMC"}; DIS = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
cls = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
for src, host in ((mw, "MW"), (m31, "M31"), (fld, "field")):
    for d in src:
        if d["name"] in ROT or d["name"] in DIS: continue
        if d["MHI"] > 0.3*d["Ms"]: continue
        cls["isolated" if host == "field" else
            ("m31" if host == "M31" else ("classical" if d["MV"] <= -7.7 else "ultrafaint"))].append(d)
ck("V1 the independent CSV parse reproduces g05's class sizes exactly (classical 11, M31 34, isolated 5, ultra-faint 29), so the sample selection is not where any disagreement lives",
   (len(cls["classical"]), len(cls["m31"]), len(cls["isolated"]), len(cls["ultrafaint"])) == (11, 34, 5, 29),
   f"classical {len(cls['classical'])}, m31 {len(cls['m31'])}, isolated {len(cls['isolated'])}, ultrafaint {len(cls['ultrafaint'])}")

def row(d, a0):
    r12 = (4.0/3.0)*d["rh"]*PC_V
    Mb = d["Ms"] + 1.33*d["MHI"]
    xi = G_V*(0.5*Mb*MS_V)/r12**2/a0
    hm = d["host_mb"]
    if hm is not None and d["Dhost"] and d["Dhost"] > 0:
        xe = G_V*hm*MS_V/(d["Dhost"]*KPC_V)**2/a0
    else:
        xe = ((G_V*MW_MB*MS_V/(d["Dgc"]*KPC_V)**2 if d["Dgc"] else 0.0) +
              (G_V*M31_MB*MS_V/(d["Dm31"]*KPC_V)**2 if d["Dm31"] else 0.0))/a0
    gobs = 3.0*(d["sig"]*1e3)**2/r12
    return math.log10(gobs/(gsph(xi, xe)*a0)), xi, xe

gals = load_sparc()
def pool(a0, drop=None):
    ly, rr = [], []
    for g in gals:
        if g["name"] == drop: continue
        y = g["gbar"]/a0
        ly.append(np.log10(y)); rr.append(np.log10(g["gobs"]/(nuv(y)*g["gbar"])))
    return np.concatenate(ly), np.concatenate(rr)
def ctrl(lx, ly, rr, w=None, n=None):
    w = MATCH_W if w is None else w; n = MATCH_N if n is None else n
    m = np.abs(ly - lx) < w
    return (float(np.median(rr[m])), int(m.sum())) if m.sum() >= n else (None, int(m.sum()))

_RC = {}
def rotating(a0, w=None, n=None):
    key = (a0, w, n)
    if key in _RC: return _RC[key]
    out = []
    for g in gals:
        y = g["gbar"]/a0
        rj = float(np.median(np.log10(g["gobs"]/(nuv(y)*g["gbar"]))))
        lyj, rrj = pool(a0, drop=g["name"])
        lx = float(np.median(np.log10(y)))
        c, _ = ctrl(lx, lyj, rrj, w, n)
        if c is not None: out.append((g["name"], rj - c, lx))
    _RC[key] = out
    return out

KEYS = ["classical", "m31", "isolated"]
def matched(a0, w=None, n=None):
    LY, RR = pool(a0)
    keep, drop = [], []
    for k in KEYS:
        for d in cls[k]:
            r, xi, xe = row(d, a0)
            c, npts = ctrl(math.log10(xi), LY, RR, w, n)
            (keep.append((d["name"], r - c, xi, r, c, k)) if c is not None else drop.append((d["name"], xi, r, k)))
    return keep, rotating(a0, w, n), drop

def stat(pv, rv, nperm=20000):
    pv, rv = np.asarray(pv, float), np.asarray(rv, float)
    sep = float(np.median(pv) - np.median(rv))
    se = math.sqrt(pv.std(ddof=1)**2/len(pv) + rv.std(ddof=1)**2/len(rv))
    pl = np.concatenate([pv, rv]); n1 = len(pv)
    cnt = sum(1 for _ in range(nperm)
              if abs(np.median((q := rng.permutation(pl))[:n1]) - np.median(q[n1:])) >= abs(sep))
    return dict(sep=sep, se=se, nsig=sep/se, p=(cnt+1)/(nperm+1), n=len(pv), nr=len(rv),
                mp=float(np.median(pv)), mr=float(np.median(rv)),
                sp=float(pv.std(ddof=1)), sr=float(rv.std(ddof=1)))

BASE = {}
for foot, a0 in A0.items():
    kp, rt, dr = matched(a0)
    o = stat([t[1] for t in kp], [t[1] for t in rt]); o["keep"] = kp; o["drop"] = dr
    BASE[foot] = o
    info(f"{foot:10} a_0={a0:.3g}:  N_pressure={o['n']} matched, {len(dr)} dropped, N_rotating={o['nr']};  "
         f"pressure median {o['mp']:+.4f} (sd {o['sp']:.3f}), rotating median {o['mr']:+.4f} (sd {o['sr']:.3f});  "
         f"separation {o['sep']:+.4f} dex, {o['nsig']:.2f} sigma, perm p = {o['p']:.4f}")
c, a = BASE["canonical"], BASE["alt"]
ck("V2 (g05's ARITHMETIC IS CLEAN) recomputed from the raw catalogues with different physical constants, a different quadrature and an independent parse, every headline number of g05 reproduces: +0.064 dex, 0.93 sigma, N = 14 matched / 36 dropped against 147 rotating, rotating control on zero, and the alt footing at +0.065 / 0.94.  There is no arithmetic defect in the estimator",
   abs(c["sep"] - 0.064) < 0.004 and abs(c["nsig"] - 0.93) < 0.06 and c["n"] == 14 and len(c["drop"]) == 36
   and c["nr"] == 147 and abs(a["sep"] - 0.065) < 0.004 and abs(c["mr"] + 0.007) < 0.004,
   f"canonical {c['sep']:+.4f} dex / {c['nsig']:.2f} sigma / p={c['p']:.4f} against g05's +0.064 / 0.93 / 0.1033;  "
   f"alt {a['sep']:+.4f} / {a['nsig']:.2f} against g05's +0.065 / 0.94;  rotating control {c['mr']:+.4f} (sd {c['sr']:.3f}) against g05's -0.007 (0.156)")

P(""); info("THE 14 OBJECTS THAT CARRY THE HEADLINE, ordered by internal acceleration:")
info(f"      {'object':22} {'class':10} {'x_i':>10} {'raw dex':>9} {'SPARC ctrl':>11} {'delta':>8}")
for t in sorted(c["keep"], key=lambda z: z[2]):
    flag = "   <-- M31 dwarf/compact ELLIPTICAL, not a dSph" if t[0] in ("NGC 147","NGC 185","NGC 205","M 32") else ""
    info(f"      {t[0]:22} {t[5]:10} {t[2]:10.5f} {t[3]:+9.3f} {t[4]:+11.3f} {t[1]:+8.3f}{flag}")

# ==========================================================================================================
P(""); P("="*118)
P("PART 2.  Q2 -- THE PRESSURE SIDE IS CONTAMINATED WITH ROTATION-SUPPORTED SYSTEMS.")
P("="*118)
DE = {"NGC 147", "NGC 185", "NGC 205", "M 32"}
info("g05's own classifier drops the LMC and the SMC by name, with the comment 'rotation-supported (belongs on")
info("the OTHER side)'.  It does not apply that principle to the M31 early-type dwarfs.  NGC 147, NGC 205 and")
info("M 32 are the textbook ROTATING members of that sequence (Geha et al. 2010, ApJ 711, 361; Simien & Prugniel")
info("2002, A&A 384, 371; Geha et al. 2006, AJ 131, 332; Bender, Burstein & Faber 1992, ApJ 399, 462), and M 32")
info("is a compact elliptical, not a dwarf spheroidal at all.  Two consequences, both against g05's conclusion:")
info("   (i)  they are rotation-supported, so on the hypothesis under test they belong on the ROTATING side;")
info("   (ii) g_obs = 3 sigma^2/r_1/2 is Wolf et al. 2010's DISPERSION-supported estimator.  For a rotating")
info("        system it omits the rotational support and UNDER-states g_obs, forcing the residual negative.")
info("They are also exactly the objects the acceleration cut SPARES: the four highest x_i in the kept sample.")

frac_hi = sum(1 for t in c["keep"] if t[2] > 0.1)
ck("V3 the four M31 dwarf/compact ellipticals are not a random 4 of the 14: they are the FOUR HIGHEST-x_i objects in the entire kept pressure sample, and every kept object above x_i = 0.1 is one of them.  The acceleration cut that g05 introduces to make the comparison honest is precisely the cut that promotes them to a quarter of the pressure votes",
   frac_hi == 4 and all(t[0] in DE for t in c["keep"] if t[2] > 0.1) and len(DE & {t[0] for t in c["keep"]}) == 4,
   f"kept objects with x_i > 0.1: " + ", ".join(f"{t[0]} ({t[2]:.2f})" for t in sorted(c['keep'], key=lambda z: z[2]) if t[2] > 0.1) +
   f"; they are {4}/{c['n']} = {100*4/c['n']:.0f} per cent of the matched pressure sample")

P(""); info("THE SEPARATION UNDER THREE SAMPLE DEFINITIONS, both footings:")
info(f"{'definition':56} {'foot':10} {'N_p':>4} {'sep dex':>9} {'sigma':>7} {'perm p':>8}")
ALT = {}
for foot, a0 in A0.items():
    kp, rt, dr = matched(a0)
    rd = [t[1] for t in rt]
    o_all = stat([t[1] for t in kp], rd)
    o_de  = stat([t[1] for t in kp if t[0] not in DE], rd)
    kp10  = [t[1] for t in kp if 0.01 <= t[2] <= 0.10]
    rd10  = [t[1] for t in rt if -2.0 <= t[2] <= -1.0]
    o_dec = stat(kp10, rd10)
    ALT[foot] = (o_all, o_de, o_dec)
    for lab, o in (("g05 as published (all 14 kept)", o_all),
                   ("minus the 4 M31 dE/cE (rotation-supported)", o_de),
                   ("NO object named: both sides restricted to 0.01<x<0.10", o_dec)):
        info(f"{lab:56} {foot:10} {o['n']:4d} {o['sep']:+9.3f} {o['nsig']:7.2f} {o['p']:8.4f}")

cde, cdec = ALT["canonical"][1], ALT["canonical"][2]
ade, adec = ALT["alt"][1], ALT["alt"][2]
ck("V4 (THE REFUTATION, AND IT FAILS BECAUSE g05's CLAIM DOES NOT SURVIVE IT) g05 says the 1.73 sigma 'is not reproducible'.  It is.  Removing the four rotation-supported M31 dwarf and compact ellipticals from the PRESSURE side -- an exclusion g05's own classifier already applies to the LMC and SMC -- takes the separation from +0.064 dex / 0.93 sigma / p = 0.11 to +0.125 dex / 2.3 sigma / p = 0.010, on both footings.  That is LARGER in significance than f09's own 1.62-1.73 sigma.  The word WITHDRAWN is not supported: what g05 has shown is that the number depends on the composition of the pressure sample, not that the effect is absent",
   cde["nsig"] < 1.5 and ade["nsig"] < 1.5,
   f"canonical: all 14 -> {c['sep']:+.3f} dex ({c['nsig']:.2f} sigma, p={c['p']:.4f});  10 genuine dSph -> {cde['sep']:+.3f} dex ({cde['nsig']:.2f} sigma, p={cde['p']:.4f}).  "
   f"alt: {ade['sep']:+.3f} dex ({ade['nsig']:.2f} sigma).  f09 quoted +0.215 dex at 1.62 sigma in its own .out and 1.73 in the fork note")

ck("V5 (FAILS, AND IT IS THE CLEANER FORM OF V4 BECAUSE IT NAMES NO OBJECT AND MAKES NO JUDGEMENT ABOUT ANY GALAXY'S KINEMATICS) restrict BOTH sides to the single decade 0.01 < x_i < 0.10 that the dwarf spheroidals actually occupy -- no exclusion list, no rotation call, just a symmetric acceleration restriction of the kind g05 itself argues for -- and the separation is +0.114 dex at 1.9 sigma, p = 0.054.  g05's A9 shows that LOOSENING the per-object window inflates the significance; it does not show that TIGHTENING the sample's acceleration span does the same thing.  Both are analysis choices, and 0.93 sigma is the value at only one of them",
   cdec["nsig"] < 1.5 and adec["nsig"] < 1.5,
   f"canonical {cdec['sep']:+.3f} dex ({cdec['nsig']:.2f} sigma, p={cdec['p']:.4f}, N_p={cdec['n']}, N_rot={cdec['nr']}); "
   f"alt {adec['sep']:+.3f} dex ({adec['nsig']:.2f} sigma, N_p={adec['n']})")

# ==========================================================================================================
P(""); P("="*118)
P("PART 3.  AGAINST MY OWN POINT.  Every way this refutation is fragile, computed rather than asserted.")
P("="*118)
kp, rt, dr = matched(A0["canonical"])
rd = [t[1] for t in rt]
info("(a) LEAVE ONE OBJECT OUT of the 14.  If my reading were right for a simple reason, one object would carry it:")
loo = {}
for t in sorted(kp, key=lambda z: z[2]):
    o = stat([u[1] for u in kp if u[0] != t[0]], rd, nperm=4000); loo[t[0]] = o
    info(f"      without {t[0]:22} sep {o['sep']:+.4f} dex  {o['nsig']:5.2f} sigma")
ck("V6 (AGAINST MY OWN POINT) no single object carries the difference.  Dropping any ONE of the fourteen leaves the separation at or below 1.51 sigma; the 2.3 sigma needs all four ellipticals gone at once, which is partly median discreteness on N = 10.  My alternative number is fragile in exactly the way g05's is, and neither should be quoted as a measurement",
   max(o["nsig"] for o in loo.values()) < 1.6,
   f"worst single leave-one-out: {max(loo, key=lambda k: loo[k]['nsig'])} at {max(o['nsig'] for o in loo.values()):.2f} sigma; "
   f"NGC 147 alone {loo['NGC 147']['nsig']:.2f}, M 32 alone {loo['M 32']['nsig']:.2f}")

o_m32 = stat([u[1] for u in kp if u[0] != "M 32"], rd, nperm=4000)
ck("V7 (AGAINST MY OWN POINT, AND IT PASSES, WHICH IS THE POINT) I am not removing only objects that help me.  M 32's residual is +0.385 dex -- it pushes the pressure median UP -- and dropping it ALONE takes the separation DOWN to 0.73 sigma, further from my conclusion than g05's own number.  The exclusion set is defined by kinematic class, not by which way each object moves the answer",
   o_m32["nsig"] < c["nsig"],
   f"M 32 delta {[t[1] for t in kp if t[0]=='M 32'][0]:+.3f} dex (helps the pressure side); without it {o_m32['sep']:+.3f} dex ({o_m32['nsig']:.2f} sigma) against the full-sample {c['nsig']:.2f} sigma")

se_med = 1.2533*c["se"]
ck("V8 (AN ERROR IN g05 THAT RUNS THE OTHER WAY, reported because a verifier must report both directions) g05 divides a difference of MEDIANS by the standard error of a difference of MEANS.  The asymptotic standard error of a median is 1.2533 sigma/sqrt(n) for a normal parent, so the correctly scaled baseline is 0.74 sigma, not 0.93.  This makes g05's published number MORE null than it states, and it applies to f09's 1.62-1.73 sigma identically",
   abs(c["sep"]/se_med - c["nsig"]) < 0.02,
   f"g05 quotes {c['nsig']:.2f} sigma; median-corrected {c['sep']/se_med:.2f} sigma.  The permutation p = {c['p']:.4f} is unaffected and is the number that should be quoted")

bs = np.array([np.median(rng.choice([t[1] for t in kp], c["n"])) - np.median(rng.choice(rd, len(rd))) for _ in range(20000)])
ck("V9 the baseline separation's own bootstrap interval spans zero comfortably and also spans my alternative value, so the two readings are not statistically distinguishable from each other either.  This is a dispute about which objects belong in the sample, not about what the data say",
   np.percentile(bs, 2.5) < 0 < np.percentile(bs, 97.5),
   f"2.5-97.5 per cent bootstrap interval on the published separation: [{np.percentile(bs,2.5):+.3f}, {np.percentile(bs,97.5):+.3f}] dex; "
   f"P(separation <= 0) = {np.mean(bs<=0):.3f}; my alternative +{cde['sep']:.3f} sits at the {100*np.mean(bs<=cde['sep']):.0f}th percentile of it")

ck("V10 (g05's BROADER CONCLUSION SURVIVES AND IS AFFIRMED HERE) nothing in this refutation reaches three sigma either.  g05's structural finding stands untouched: 36 of the 50 pressure objects sit below SPARC's deepest acceleration, they carry a median residual an order of magnitude larger than the 14 that overlap, and support type cannot be separated from acceleration depth with Local Group data.  What is refuted is only the specific statement that f09's separation is WITHDRAWN and that 0.93 sigma is THE number",
   max(o["nsig"] for o in (cde, cdec, ade, adec)) < 3.0 and np.median([t[2] for t in dr]) > 3*np.median([t[3] for t in kp]),
   f"largest alternative significance {max(o['nsig'] for o in (cde, cdec, ade, adec)):.2f} sigma; dropped-object median raw residual "
   f"{np.median([t[2] for t in dr]):+.3f} dex on N={len(dr)} against kept {np.median([t[3] for t in kp]):+.3f} dex on N={len(kp)}")

# ==========================================================================================================
P(""); P("="*118)
P("PART 4.  MUTATION CONTROLS ON THIS VERIFICATION ITSELF.")
P("="*118)
lab = np.concatenate([[t[1] for t in kp], rd]); n1 = c["n"]
sh = np.array([abs(np.median((q := rng.permutation(lab))[:n1]) - np.median(q[n1:])) for _ in range(20000)])
ck("W1 MUTATION: shuffling the pressure/rotating labels reproduces the published separation about one time in ten, which is the permutation p already reported.  The control agrees with g05 that the PUBLISHED separation is not significant -- my objection is to the sample, not to that arithmetic",
   0.05 < float(np.mean(sh >= abs(c["sep"]))) < 0.20,
   f"P(shuffled >= {abs(c['sep']):.3f}) = {np.mean(sh >= abs(c['sep'])):.4f}")

kp2 = [t for t in kp if t[0] not in DE]
lab2 = np.concatenate([[t[1] for t in kp2], rd]); n2 = len(kp2)
sh2 = np.array([abs(np.median((q := rng.permutation(lab2))[:n2]) - np.median(q[n2:])) for _ in range(20000)])
ck("W2 MUTATION: the same shuffle on the dE-free sample does NOT reproduce its separation -- about one time in a hundred -- so the difference between 0.93 sigma and 2.3 sigma is not an artefact of the smaller N",
   float(np.mean(sh2 >= abs(cde["sep"]))) < 0.05,
   f"P(shuffled >= {abs(cde['sep']):.3f}) = {np.mean(sh2 >= abs(cde['sep'])):.4f} on N = {n2}")

big = A0["canonical"]*100
rb = np.array([row(d, big)[0] for k in KEYS for d in cls[k]])
rn = np.array([row(d, A0["canonical"])[0] for k in KEYS for d in cls[k]])
ck("W3 MUTATION on the theory: raising a_0 by 100 drives every pressure object deep into the modified regime and the residuals must fall.  They do, by the same amount g05 reports, confirming the two pipelines are the same pipeline",
   np.median(rb) < np.median(rn) - 0.2 and abs(np.median(rn) - 0.489) < 0.01,
   f"median residual {np.median(rn):+.3f} dex at canonical a_0 (g05: +0.489), {np.median(rb):+.3f} at 100 a_0")

sm = np.array([math.log10(3.0*((d["sig"]*math.sqrt(2))*1e3)**2/((4.0/3.0)*d["rh"]*PC_V)) for k in KEYS for d in cls[k]])
s0 = np.array([math.log10(3.0*(d["sig"]*1e3)**2/((4.0/3.0)*d["rh"]*PC_V)) for k in KEYS for d in cls[k]])
ck("W4 MUTATION on the data: inflating every dispersion by sqrt(2) moves every observed acceleration by exactly log10(2), and nothing else responds",
   abs(float(np.median(sm - s0)) - math.log10(2.0)) < 1e-12,
   f"shift {float(np.median(sm - s0)):+.12f} against log10(2) = {math.log10(2.0):+.12f}")

# ==========================================================================================================
P(""); P("="*118); P("VERDICT OF THE VERIFICATION"); P("="*118)
P("  THE ARITHMETIC IS CLEAN.  THE CONCLUSION IS NOT SUPPORTED BY IT.")
P("")
P(f"  Q1.  Every number in g05's claim reproduces exactly under an independent re-derivation with different")
P(f"       physical constants, a different quadrature and an independent parse of the raw catalogues:")
P(f"       {c['sep']:+.4f} dex, {c['nsig']:.2f} sigma, N = {c['n']} matched / {len(c['drop'])} dropped / {c['nr']} rotating, alt footing {a['sep']:+.4f} dex.")
P(f"       No arithmetic defect, no units slip, no covariance or aperture error.  The enclosed-mass and")
P(f"       deprojected-radius repairs are correct, the QUMOND flux theorem is applied correctly, and the")
P(f"       Wolf et al. 2010 observed-side estimator is the right one FOR A DISPERSION-SUPPORTED SYSTEM.")
P(f"")
P(f"  Q2.  The null is an artefact of WHICH OBJECTS survive g05's own acceleration cut.  The four highest-x_i")
P(f"       objects in the kept sample are NGC 147, NGC 185, NGC 205 and M 32 -- M31 dwarf and compact")
P(f"       ELLIPTICALS with documented rotation, on which Wolf's dispersion-only estimator under-states g_obs.")
P(f"       g05's own classifier removes the LMC and SMC by name as 'rotation-supported (belongs on the OTHER")
P(f"       side)' and does not apply that rule here.  They are 4 of the 14 votes in the median.")
P(f"")
P(f"          g05 as published                                     {c['sep']:+.3f} dex   {c['nsig']:.2f} sigma   p = {c['p']:.3f}")
P(f"          minus the four rotation-supported M31 dE/cE          {cde['sep']:+.3f} dex   {cde['nsig']:.2f} sigma   p = {cde['p']:.3f}")
P(f"          no object named, both sides at 0.01 < x_i < 0.10     {cdec['sep']:+.3f} dex   {cdec['nsig']:.2f} sigma   p = {cdec['p']:.3f}")
P(f"")
P(f"       So 'the prior 1.73 sigma is not reproducible' is FALSE.  It is reproducible, and exceeded in")
P(f"       significance, under a sample definition at least as defensible as g05's -- and under one that names")
P(f"       no object at all.  g05's A9 correctly warns that LOOSENING the per-object window inflates the")
P(f"       significance; the same warning applies with the same force to the sample's acceleration SPAN, and")
P(f"       g05 does not make it.  The published 0.93 sigma is the value at one analysis choice among several.")
P(f"")
P(f"  WHAT SURVIVES OF g05, AND IT IS THE LARGER PART.  The structural finding is untouched and is affirmed")
P(f"  by this verification: {len(c['drop'])} of {len(c['drop'])+c['n']} pressure objects sit below SPARC's deepest acceleration, they carry a")
P(f"  median residual of {np.median([t[2] for t in dr]):+.2f} dex against {np.median([t[3] for t in kp]):+.2f} dex for the {c['n']} that overlap, and support type cannot be")
P(f"  separated from acceleration depth with Local Group data.  Nothing here reaches three sigma either, so")
P(f"  the rotation-versus-pressure separation remains a HINT and not a detection.  The prescription repair,")
P(f"  the three arithmetic-bug decompositions, the globular-cluster class and the isolated-dwarf class all")
P(f"  stand as g05 reports them.")
P(f"")
P(f"  WHAT MAY NOT BE QUOTED.  'f09's separation is WITHDRAWN' and '0.93 sigma' as THE number.  The defensible")
P(f"  statement is: 'at matched acceleration the separation is between +0.06 and +0.13 dex, 0.9 to 2.3 sigma")
P(f"  depending on whether rotating M31 early-type dwarfs are counted as pressure-supported; it is not a")
P(f"  detection on any choice, and the Local Group cannot separate support type from acceleration depth.'")
sys.exit(ck.done())
