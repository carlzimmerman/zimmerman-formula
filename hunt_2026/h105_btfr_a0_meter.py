#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h105_btfr_a0_meter.py -- HUNT ITEM 105: is the BTFR zero-point an a_0 meter?  Validated on the LOCAL sample first.
====================================================================================================================
The decisive measurement the repo has identified -- a deep-MOND baryonic Tully-Fisher zero-point at z ~ 2.5 to
+-0.13 dex -- will be read through one estimator:

        V_flat^4 = G M_b a_0        =>        a_0 = V_flat^4 / (G M_b)

Item 105's instruction is to validate that estimator locally BEFORE it is used at high z, and to quote the precision
it actually reaches.  This script does exactly that on SPARC, gas included, on the flat part only, and it reports
three things that are all against interest:

  1. The estimator is EXACT only asymptotically.  For a real disc measured at a finite radius,
         V^4/(G M_b a_0) = nu(y)^2 * y * epsilon,     y = g_bar(R)/a_0,   epsilon = g_bar(R) R^2/(G M_b),
     which is computable galaxy by galaxy from the rotmod files.  On SPARC's own outermost points it is 1.59, so the
     BTFR zero-point sits 0.20 dex ABOVE a_0 for a structural reason, not a physical one.  On RC100's own epsilon and
     y, at one effective radius, it is 0.32 dex -- so 0.11 dex does not cancel between a high-z and a local sample.

  2. The statistical precision is 6.4% on 122 galaxies -- close to the item's 5% target -- and it is irrelevant,
     because the estimator's gas-dominated and star-dominated halves disagree by 0.24 dex at the committed
     Upsilon = 0.5 and agree only at Upsilon ~ 0.9.  Item 105 is therefore another instance of the hunt's
     mass-to-light wall, and it is quantified here rather than asserted.

  3. The BTFR slope at Upsilon = 0.5 is 3.55-3.80 depending on the fitting direction, not the 4 the framework
     requires; slope 4 arrives at Upsilon ~ 0.9, which conflicts with item 76's deep-tail Upsilon of 0.50-0.66 and
     with stellar populations' 0.5 +- 0.1.  Two of the framework's own Upsilon-predictors disagree.

Newtonian and LambdaCDM alternatives computed beside the framework.  Both footings.  Mutation controls.  Checks CAN fail.
Convention note: M_b = Upsilon_disk * L[3.6] + 1.33 M_HI, the same convention as hunt_lib and the rest of the hunt
(a single Upsilon on the total 3.6um light -- the master table does not carry a disc/bulge luminosity split, so
bulge-dominated galaxies are treated slightly differently from Lelli+2016b; the effect is named in Part E's scan).
"""
import sys, math
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(105)
LELLI_SLOPE, LELLI_ERR = 3.85, 0.09          # Lelli+2019 orthogonal BTFR slope, quoted for comparison only
TARGET = 0.05                                 # item 105's "returns a_0 to 5%"
DECISIVE = 0.13                               # the repo's decisive z ~ 2.5 BTFR zero-point precision, dex


def build(ups_d, ups_b=None):
    """SPARC galaxies with a measured flat velocity.  Returns per-galaxy dicts; g_bar/g_obs come from the rotmods
    at the OUTERMOST measured point, so the finite-radius correction can be computed from the same data."""
    if ups_b is None: ups_b = min(1.4*ups_d, 1.6)
    gals = load_sparc(ups_d=ups_d, ups_b=ups_b)
    out = []
    for g in gals:
        if g["Vflat"] <= 0: continue
        Mb = ups_d*g["L36"]*1e9 + 1.33*g["MHI"]*1e9
        if Mb <= 0: continue
        V = g["Vflat"]*1e3
        gb, go, R = g["gbar"][-1], g["gobs"][-1], g["r"][-1]*kpc
        eps = gb*R*R/(G*Mb*Msun)
        d = dict(name=g["name"], Mb=Mb, V=g["Vflat"], eV=g["eVflat"], D=g["D"], eD=g["eD"],
                 inc=g["inc"], einc=g["einc"], Q=g["Q"], MHI=g["MHI"], L36=g["L36"],
                 fgas=1.33*g["MHI"]*1e9/Mb, gbar=gb, gobs=go, R=R, eps=eps,
                 a0btfr=V**4/(G*Mb*Msun), vlast=g["vobs"][-1])
        d["fdm"] = 1.0 - gb/go if go > gb > 0 else float("nan")
        out.append(d)
    return out


def a0_at_last(d, ):
    """The kernel inverted at the outermost measured point: a_0 = g_bar/[ln(1/f_DM)]^2 (item 101's closed form)."""
    f = d["fdm"]
    if not (0.02 < f < 0.98): return float("nan")
    return d["gbar"]/math.log(1.0/f)**2


def Cfac(d, a0v):
    """V^4/(G M_b a_0) for a disc measured at radius R: nu(y)^2 * y * epsilon."""
    y = d["gbar"]/a0v
    return nu_s(y)**2*y*d["eps"]


def med_boot(v, n=4000):
    v = np.asarray(v)
    bs = np.array([np.median(v[rng.integers(0, len(v), len(v))]) for _ in range(n)])
    return float(np.median(v)), float(np.std(np.log10(bs)))


def slopes(M, V):
    """BTFR slope three ways: forward OLS (M on V), inverse OLS (V on M, inverted), and total least squares."""
    lM, lV = np.log10(M), np.log10(V)
    fwd = float(np.polyfit(lV, lM, 1)[0])
    inv = 1.0/float(np.polyfit(lM, lV, 1)[0])
    X = np.vstack([lV - lV.mean(), lM - lM.mean()])
    u, s, vt = np.linalg.svd(X @ X.T)
    return fwd, inv, float(u[1, 0]/u[0, 0])


# ==================================================================================================================
P("="*120); P("PART A -- the estimator, and the condition under which it is exact"); P("="*120)
info("MOND makes v(r -> infinity)^4 = G M a_0 EXACT for any isolated system, whatever the interpolation function.")
info("What a survey measures is v at a FINITE radius.  For a disc, with epsilon = g_bar(R) R^2/(G M_b) the ratio of the")
info("actual baryonic field to a point mass's at the same radius,")
info("      V(R)^2 = nu(y) g_bar(R) R,  g_bar = epsilon G M_b/R^2   =>   V^4/(G M_b a_0) = nu(y)^2 * y * epsilon,")
info("so the BTFR estimator returns a_0 times a computable factor C = nu(y)^2 y epsilon that is 1 only as y -> 0 with")
info("epsilon -> 1.  C for a point mass (epsilon = 1), Route A:")
for y in (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0):
    info(f"      y = g_bar/a_0 = {y:5.2f}  ->  C = {nu_s(y)**2*y:6.3f}  ({math.log10(nu_s(y)**2*y):+.3f} dex)")
ck("105-A the estimator's exactness condition, derived before any data: v^4 = G M a_0 holds only asymptotically, and "
   "the finite-radius factor C = nu(y)^2 y epsilon is above 1 everywhere -- 0.13 dex already at y = 0.1 and 0.40 dex "
   "at y = 1.  Any BTFR zero-point measured at finite radius is therefore an UPPER bound on a_0 unless C is removed",
   nu_s(1.0)**2*1.0 > 2.0 and nu_s(0.01)**2*0.01 < 1.15,
   f"C(y=0.01) = {nu_s(0.01)**2*0.01:.3f}, C(0.1) = {nu_s(0.1)**2*0.1:.3f}, C(1) = {nu_s(1.0)**2:.3f}, "
   f"C(10) = {nu_s(10.)**2*10:.2f}")

# ==================================================================================================================
P(""); P("="*120); P("PART B -- the local measurement on SPARC, flat part only, gas included"); P("="*120)
D5 = build(UPS_D)
a0b = np.array([d["a0btfr"] for d in D5]); Mb = np.array([d["Mb"] for d in D5]); Vf = np.array([d["V"] for d in D5])
med, prec = med_boot(a0b)
info(f"N = {len(D5)} SPARC galaxies with a measured V_flat, Q <= 2, i >= 30, Upsilon_disk = {UPS_D}")
info(f"a_0(BTFR) = V_flat^4/(G M_b): median {med:.3e} m/s^2, 16-84% {np.percentile(a0b,16):.2e} - {np.percentile(a0b,84):.2e}, "
     f"sd(log) = {np.std(np.log10(a0b)):.3f} dex")
info(f"statistical precision on the median: {prec:.4f} dex = {100*(10**prec-1):.1f}%   "
     f"(the item asked for {100*TARGET:.0f}%)")
for f_ in ("canonical", "alt"):
    info(f"   vs the {f_:10} footing {A0[f_]:.3e}: {math.log10(med/A0[f_]):+.3f} dex")
info(f"the 0.24 dex per-galaxy spread is the BTFR's OBSERVED vertical scatter; Lelli+2016b quote the same figure and "
     f"an intrinsic scatter of ~0.10 dex after the observational error budget is removed.")
ck("105-B the local BTFR zero-point comes CLOSE to the item's target on statistics alone -- 122 galaxies give a_0 to "
   f"{100*(10**prec-1):.1f}%, not quite the 5% asked for but within a factor 1.3 of it, and the shortfall would be closed by "
   "N alone.  Everything after this part is about why that number is not the precision of the measurement",
   prec < math.log10(1.10), f"median a_0 = {med:.3e}, statistical {prec:.4f} dex = {100*(10**prec-1):.1f}% against a "
                            f"{100*TARGET:.0f}% target ({(10**prec-1)/TARGET:.1f}x); N = {len(D5)}")

# ==================================================================================================================
P(""); P("="*120); P("PART C -- the finite-radius factor measured on the same galaxies"); P("="*120)
a0L = np.array([a0_at_last(d) for d in D5])
ok = np.isfinite(a0L)
Cv = np.array([Cfac(d, A0["canonical"]) for d in D5])
yv = np.array([d["gbar"]/A0["canonical"] for d in D5]); ev = np.array([d["eps"] for d in D5])
medL, precL = med_boot(a0L[ok])
info(f"at SPARC's outermost measured points: y = g_bar/a_0 median {np.median(yv):.3f} (16-84% {np.percentile(yv,16):.3f} - {np.percentile(yv,84):.3f}), "
     f"epsilon median {np.median(ev):.2f}")
info(f"   => C median {np.median(Cv):.2f} = {math.log10(np.median(Cv)):+.3f} dex "
     f"(nu^2 y contributes {math.log10(np.median(nu(yv)**2*yv)):+.3f}, disc geometry epsilon {math.log10(np.median(ev)):+.3f})")
info(f"the same galaxies through the kernel AT the measured radius (item 101's closed form, no asymptotic assumption):")
info(f"   a_0 = {medL:.3e} +- {precL:.4f} dex, i.e. {math.log10(med/medL):+.3f} dex BELOW the naive BTFR zero-point")
info(f"   and {math.log10(medL/A0['canonical']):+.3f} dex from the canonical footing / {math.log10(medL/A0['alt']):+.3f} dex from the alt footing")
info("AGAINST INTEREST, two ways: (i) item 101 showed this same closed form is itself biased HIGH by ~0.05 dex from")
info("truncation at f_DM = 0, so the corrected value is if anything a little lower still; and (ii) item 101's SPARC")
info(f"rung, the identical estimator evaluated at R_eff instead of the last point, gave 1.18e-10 -- a "
     f"{math.log10(1.176e-10/medL):+.2f} dex")
info("radius dependence inside one sample, which is a systematic of the inversion that nothing here removes.")
ck("105-C the BTFR zero-point is NOT a_0: it is a_0 times a structural factor that SPARC's own rotation curves "
   "measure to be 1.55.  Removing it with the framework's own kernel moves the local value from 1.53e-10 to "
   "9.8e-11, which lands on the canonical footing -- but the same estimator moves 0.08 dex if it is evaluated at "
   "R_eff instead of the last point, so no footing is decided here",
   abs(math.log10(med/medL) - math.log10(np.median(Cv))) < 0.06,
   f"C(measured) = {np.median(Cv):.2f} ({math.log10(np.median(Cv)):+.3f} dex) against an observed BTFR-minus-kernel "
   f"gap of {math.log10(med/medL):+.3f} dex; corrected a_0 = {medL:.3e} ({math.log10(medL/A0['canonical']):+.3f} dex from canonical)")
info("")
info("WHY THIS MATTERS FOR z ~ 2.5, which is the whole point of item 105: SPARC's flat points sit at y ~ 0.06.  The")
info("high-z rotation curves that would carry the decisive measurement are sampled at ONE effective radius, where two")
info("things change at once -- y rises to ~2, and epsilon FALLS below 1 because only part of M_bar is inside R_e.")
info("BUG CAUGHT IN THE MAKING OF THIS SCRIPT: the first version assumed epsilon = 1.2 at R_e by analogy with SPARC's")
info("outermost points.  That is bug pattern 1 -- a TOTAL mass where an ENCLOSED one belongs -- and it overstated C by")
info("0.3 dex.  epsilon is computed here from RC100's own tabulated M_bar, R_e and f_DM instead:")
rc_eps, rc_y = [], []
for r in __import__("csv").DictReader(open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv"))):
    try:
        fdm, go_, Re_, lMb = float(r["fDM_within_Re"]), float(r["g_Re_ms2"]), float(r["Re_kpc"]), float(r["logMbar_Msun"])
    except Exception:
        continue
    if not (0.02 < fdm < 0.98): continue
    gb_ = (1 - fdm)*go_
    rc_eps.append(gb_*(Re_*kpc)**2/(G*10**lMb*Msun)); rc_y.append(gb_/A0["canonical"])
rc_eps = np.array(rc_eps); rc_y = np.array(rc_y)
rcC = nu(rc_y)**2*rc_y*rc_eps
info(f"      RC100 at R_e: epsilon = {np.median(rc_eps):.2f} (16-84% {np.percentile(rc_eps,16):.2f} - {np.percentile(rc_eps,84):.2f}), "
     f"y = {np.median(rc_y):.2f}  ->  C = {np.median(rcC):.2f} ({math.log10(np.median(rcC)):+.3f} dex)")
info(f"      SPARC flat  : epsilon = {np.median(ev):.2f}, y = {np.median(yv):.3f}  ->  C = {np.median(Cv):.2f} "
     f"({math.log10(np.median(Cv)):+.3f} dex)")
info(f"      MSA-3D tabulates no M_bar, only M*, so its epsilon is NOT computed here -- with the paper's own median")
info(f"      M_mol/M* ~ 2 it would sit near RC100's, but that is an import and is not used.")
ck("105-C2 the warning the decisive measurement needs, with epsilon MEASURED rather than assumed: applying "
   "v^4 = G M_b a_0 to a velocity taken at ONE effective radius, as every z ~ 1-2.5 kinematic survey does, overstates "
   f"a_0 by {math.log10(np.median(rcC)):+.2f} dex on RC100's own epsilon and y.  Against a local sample measured on a flat outer curve "
   f"({math.log10(np.median(Cv)):+.2f} dex) most of that cancels, but {math.log10(np.median(rcC)/np.median(Cv)):+.2f} dex does not -- and that residual alone eats "
   f"{100*math.log10(np.median(rcC)/np.median(Cv))/DECISIVE:.0f}% of the decisive test's entire +-{DECISIVE:.2f} dex budget.  Stated against my own first "
   "version, which assumed epsilon = 1.2 at R_e and made this look twice as bad as it is",
   math.log10(np.median(rcC)) > DECISIVE and abs(math.log10(np.median(rcC)) - math.log10(np.median(Cv))) > 0.5*DECISIVE,
   f"C(RC100 at R_e) = {np.median(rcC):.2f} = {math.log10(np.median(rcC)):+.3f} dex vs C(SPARC flat) = "
   f"{np.median(Cv):.2f} = {math.log10(np.median(Cv)):+.3f} dex; the non-cancelling difference is "
   f"{math.log10(np.median(rcC)/np.median(Cv)):+.3f} dex against a +-{DECISIVE:.2f} dex target")

# ==================================================================================================================
P(""); P("="*120); P("PART D -- the BTFR slope, three fitting directions, and the mass trend it implies"); P("="*120)
info("The framework requires slope EXACTLY 4 and hence zero mass trend in a_0.  Regressing log a_0 on log M_b would")
info("share M_b between both axes (it enters y with coefficient -1 and x with +1) and is biased toward -1, so the")
info("slope is taken from the M_b-V plane in all three standard directions instead, and converted by 4/alpha - 1:")
fwd, inv, tls = slopes(Mb, Vf)
bs = np.array([slopes(Mb[i], Vf[i])[2] for i in (rng.integers(0, len(Mb), len(Mb)) for _ in range(2000))])
info(f"   forward OLS (M on V) {fwd:.3f}  |  inverse OLS {inv:.3f}  |  total least squares {tls:.3f} +- {bs.std():.3f}")
info(f"   implied mass trend of a_0: {4/fwd-1:+.3f} / {4/inv-1:+.3f} / {4/tls-1:+.3f} dex per dex of M_b")
info(f"   Lelli+2019's orthogonal slope on their stricter sample is {LELLI_SLOPE:.2f} +- {LELLI_ERR:.2f}, consistent with the TLS value here")
# curvature: the framework predicts a straight line
q = np.polyfit(np.log10(Vf), np.log10(Mb), 2)
bq = np.array([np.polyfit(np.log10(Vf[i]), np.log10(Mb[i]), 2)[0] for i in (rng.integers(0, len(Mb), len(Mb)) for _ in range(2000))])
info(f"   curvature of log M_b vs log V_flat: {q[0]:+.3f} +- {bq.std():.3f} (framework requires 0; a LambdaCDM BTFR "
     f"built from abundance matching is curved because M_*/M_halo turns over)")
ck("105-D the slope is NOT 4 at the committed Upsilon: three fitting directions bracket 3.55-3.80, and the framework "
   f"requires 4 exactly.  That is a mass trend of {4/tls-1:+.3f} dex per dex in the a_0 the BTFR reports -- {(4/tls-1)*4:.2f} dex "
   "across SPARC's four decades of baryonic mass, far larger than the +-0.13 dex the decisive test needs",
   abs(tls - 4.0) > 2*bs.std(),
   f"TLS slope {tls:.3f} +- {bs.std():.3f}, {abs(tls-4)/bs.std():.1f} sigma from 4; forward {fwd:.3f}, inverse {inv:.3f}; "
   f"curvature {q[0]:+.3f} +- {bq.std():.3f} (consistent with a straight line)")

# ==================================================================================================================
P(""); P("="*120); P("PART E -- the mass-to-light lever, and the split that exposes it"); P("="*120)
P(f"  {'Ups_d':>7}{'N':>5}{'a_0 all':>12}{'gas-dom':>12}{'star-dom':>12}{'split dex':>11}{'TLS slope':>11}{'trend':>9}")
scan = {}
for ups in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.1):
    Dx = build(ups)
    a = np.array([d["a0btfr"] for d in Dx]); fg = np.array([d["fgas"] for d in Dx])
    M_ = np.array([d["Mb"] for d in Dx]); V_ = np.array([d["V"] for d in Dx])
    gd, sd_ = fg > 0.7, fg < 0.3
    sp = math.log10(np.median(a[sd_])/np.median(a[gd])); tl = slopes(M_, V_)[2]
    scan[ups] = dict(med=float(np.median(a)), split=sp, tls=tl, ngd=int(gd.sum()), nsd=int(sd_.sum()))
    P(f"  {ups:7.1f}{len(Dx):5d}{np.median(a):12.3e}{np.median(a[gd]):12.3e}{np.median(a[sd_]):12.3e}"
      f"{sp:11.3f}{tl:11.3f}{4/tl-1:+9.3f}")
d_dlogUps = (math.log10(scan[0.7]["med"]) - math.log10(scan[0.3]["med"]))/(math.log10(0.7) - math.log10(0.3))
fstar = 1.0 - float(np.median([d["fgas"] for d in D5]))
info(f"  the lever: d log a_0 / d log Upsilon = {d_dlogUps:+.3f}, which is -f_star with f_star = {fstar:.2f} as it must be")
info(f"  the split at the committed Upsilon = 0.5 is {scan[0.5]['split']:+.3f} dex between "
     f"{scan[0.5]['nsd']} star-dominated (f_gas < 0.3) and {scan[0.5]['ngd']} gas-dominated (f_gas > 0.7) galaxies")
ups_close = min(scan, key=lambda u: abs(scan[u]["split"]))
ups_slope4 = min(scan, key=lambda u: abs(scan[u]["tls"] - 4.0))
info(f"  the split closes at Upsilon ~ {ups_close:.1f} and the slope reaches 4 at Upsilon ~ {ups_slope4:.1f}")
ck("105-E BUG PATTERN 5, and it fires hardest here: the BTFR a_0 meter's own internal consistency is a statement "
   "about the stellar mass-to-light ratio.  At the committed Upsilon = 0.5 the gas-dominated and star-dominated "
   "halves disagree by 0.24 dex; they agree, and the slope becomes 4, only at Upsilon ~ 0.9.  That is 0.25 dex above "
   "item 76's deep-tail value (0.50-0.66) and 0.25 dex above stellar populations' 0.5 +- 0.1 -- so two of the "
   "framework's own Upsilon-predictors disagree by 0.13-0.25 dex in Upsilon, and the meter cannot be trusted below "
   "that gap",
   abs(scan[0.5]["split"]) > 0.15 and ups_close > 0.7,
   f"split at Upsilon = 0.5 is {scan[0.5]['split']:+.3f} dex, closes at Upsilon ~ {ups_close:.1f}; "
   f"TLS slope 4 at Upsilon ~ {ups_slope4:.1f}; lever d log a_0/d log Upsilon = {d_dlogUps:+.2f}")

# ==================================================================================================================
P(""); P("="*120); P("PART F -- the error budget, and the precision the meter actually reaches"); P("="*120)
eD = np.array([d["eD"]/d["D"] for d in D5]); einc = np.array([d["einc"] for d in D5])
inc = np.array([d["inc"] for d in D5]); eV = np.array([d["eV"]/d["V"] for d in D5])
sig_ups = 0.10*fstar                                        # SPS Upsilon at +-0.10 dex, coherent
sig_gas = 0.05*(1.0 - fstar)                                # gas mass (He factor + M_HI) at +-0.05 dex, coherent
sig_dscale = 2.0*math.log10(1.02)                           # a 2% coherent distance-scale error, a_0 ~ D^-2
terms = [("statistical (bootstrap median)", prec, "random"),
         ("Upsilon zero-point, +-0.10 dex (SPS)", sig_ups, "COHERENT"),
         ("gas mass, +-0.05 dex", sig_gas, "COHERENT"),
         ("distance scale, 2%", sig_dscale, "COHERENT"),
         ("per-galaxy distance (median %.0f%%)" % (100*np.median(eD)), 2*math.log10(1+np.median(eD))/math.sqrt(len(D5)), "random"),
         ("per-galaxy inclination (median %.0f deg +- %.0f)" % (np.median(inc), np.median(einc)),
          4*math.log10(math.e)*float(np.median(einc*math.pi/180/np.tan(inc*math.pi/180)))/math.sqrt(len(D5)), "random"),
         ("per-galaxy V_flat (median %.0f%%)" % (100*np.median(eV)), 4*math.log10(1+np.median(eV))/math.sqrt(len(D5)), "random")]
P(f"  {'term':46}{'dex':>9}{'%':>9}   nature")
for lab, v, nat in terms:
    P(f"  {lab:46}{v:9.4f}{100*(10**v-1):9.1f}   {nat}")
tot = math.sqrt(sum(v*v for _, v, _ in terms))
P(f"  {'quadrature total (excluding C and the split)':46}{tot:9.4f}{100*(10**tot-1):9.1f}")
P(f"  {'the C correction itself':46}{math.log10(np.median(Cv)):9.4f}{100*(np.median(Cv)-1):9.1f}   STRUCTURAL, framework-computed")
P(f"  {'the gas/star split at Upsilon = 0.5':46}{abs(scan[0.5]['split']):9.4f}{100*(10**abs(scan[0.5]['split'])-1):9.1f}   INTERNAL INCONSISTENCY")
ck("105-F AGAINST INTEREST -- the honest answer to 'what precision does the local BTFR zero-point reach': "
   f"{100*(10**prec-1):.1f}% statistically, {100*(10**tot-1):.0f}% once the coherent mass-to-light, gas and distance-scale terms are "
   "carried, and no better than the 0.24 dex by which the meter disagrees with itself between its gas-rich and "
   "star-rich halves.  The item's 5% is reached only in the one term that does not matter",
   tot > TARGET*0.5 and abs(scan[0.5]["split"]) > tot,
   f"statistical {prec:.4f} dex; coherent total {tot:.4f} dex = {100*(10**tot-1):.0f}%; internal split "
   f"{abs(scan[0.5]['split']):.3f} dex = {100*(10**abs(scan[0.5]['split'])-1):.0f}%")

# ==================================================================================================================
P(""); P("="*120); P("PART G -- the Newtonian and LambdaCDM alternatives computed beside the framework"); P("="*120)
info("NEWTON: with baryons only and no modification there is no asymptotically flat velocity at all -- v ~ R^{-1/2}")
info("beyond the disc -- so 'the BTFR zero-point' is not defined.  The relation's existence is already the result;")
info("its zero-point is the second-order question this item is about.")
info("LambdaCDM: the BTFR is inherited from M_b(M_200) and V_flat(M_200).  V_200 ~ M_200^{1/3} exactly, so a slope of")
info("4 requires M_b ~ M_200^{4/3}, i.e. the baryon fraction must RISE as M_200^{1/3} over four decades, and the")
info("relation must stay straight while abundance matching's M_*/M_200 turns over at both ends.  The measurable")
info("consequences are a curvature and a scatter:")
info(f"   curvature measured here: {q[0]:+.3f} +- {bq.std():.3f} -- consistent with a straight line, as the framework")
info(f"   requires, but the test is UNDERPOWERED: the 2-sigma bound is |curvature| < {2*bq.std():.2f}, wide enough to admit a")
info(f"   substantially bent relation, so straightness is not yet a discriminant on this sample.")
info(f"   observed vertical scatter {np.std(np.log10(a0b)):.3f} dex, of which Lelli+2016b attribute ~0.10 dex to intrinsic scatter;")
info(f"   the framework requires ZERO intrinsic scatter in a_0 and therefore has to spend all 0.10 dex on M/L, gas and distance.")
ck("105-G the framework's two structural BTFR predictions -- a straight line and no intrinsic scatter -- are not "
   "violated, but the straightness test is UNDERPOWERED here and is reported as such; what does NOT survive is "
   "slope 4 at the committed Upsilon.  LambdaCDM's freedom is the other way round: it can fit any slope but has to "
   "arrange the straightness and the tightness by hand",
   abs(q[0]) < 3*bq.std(),
   f"curvature {q[0]:+.3f} +- {bq.std():.3f} ({abs(q[0])/bq.std():.1f} sigma from straight); slope "
   f"{tls:.2f} +- {bs.std():.2f} ({abs(tls-4)/bs.std():.1f} sigma from 4)")

# ==================================================================================================================
P(""); P("="*120); P("PART H -- what this means for the decisive z ~ 2.5 measurement"); P("="*120)
info(f"The decisive test is a deep-MOND BTFR zero-point at z ~ 2.5 to +-{DECISIVE:.2f} dex (framework 0.00, "
     f"LambdaCDM-native +0.33).  What this validation says it needs:")
info(f"  1. velocities on a genuinely FLAT outer curve.  At one R_e the structural factor C is "
     f"{math.log10(np.median(rcC)):+.2f} dex (RC100's own epsilon and y),")
info(f"     against {math.log10(np.median(Cv)):+.2f} dex on a local flat curve, so {math.log10(np.median(rcC)/np.median(Cv)):+.2f} dex does NOT cancel between the two ends "
     f"-- {100*math.log10(np.median(rcC)/np.median(Cv))/DECISIVE:.0f}% of the whole budget.")
info(f"  2. MEASURED gas, not scaling-relation gas.  The local coherent gas term is only {sig_gas:.3f} dex because M_HI is")
info(f"     measured; the repo's own MUSE-DARK II refit carries +-0.20 dex from modelled gas alone, which already")
info(f"     exceeds {DECISIVE:.2f} dex on its own.")
info(f"  3. a differential design.  The Upsilon zero-point ({sig_ups:.3f} dex) cancels between z = 0 and z = 2.5 only if the")
info(f"     SAME Upsilon convention is used at both ends; what does NOT cancel is the EVOLUTION of Upsilon, and the")
info(f"     gas/star split found in Part E says the local Upsilon itself is uncertain by ~0.25 dex.")
need = math.sqrt(max(DECISIVE**2 - sig_ups**2 - sig_gas**2, 1e-6))
info(f"  4. N: with the local per-galaxy spread of {np.std(np.log10(a0b)):.2f} dex, reaching {DECISIVE:.2f} dex statistically needs "
     f"only N ~ {(np.std(np.log10(a0b))*1.25/need)**2:.0f} galaxies")
info(f"     with the coherent terms already at {math.hypot(sig_ups, sig_gas):.3f} dex -- so N is NOT the binding constraint; the gas and")
info(f"     the mass-to-light ratio are.")
ck("105-H the forecast, stated in the item's own currency: the +-0.13 dex decisive measurement is not limited by "
   "sample size (a handful of galaxies would do it statistically) but by two systematics this local validation "
   "measures -- the structural factor C if the velocities are not on a flat curve, and the gas plus mass-to-light "
   "budget, which locally already contributes more than half the target",
   math.hypot(sig_ups, sig_gas) < DECISIVE and (np.std(np.log10(a0b))*1.25/need)**2 < 60,
   f"coherent M/L + gas floor {math.hypot(sig_ups, sig_gas):.3f} dex of a {DECISIVE:.2f} dex target; "
   f"N needed statistically {(np.std(np.log10(a0b))*1.25/need)**2:.0f}; non-cancelling C between R_e and a flat curve "
   f"{math.log10(np.median(rcC)/np.median(Cv)):+.2f} dex")

# ==================================================================================================================
P(""); P("="*120); P("PART I -- mutation controls"); P("="*120)
Msh = rng.permutation(Mb)
a_sh = (Vf*1e3)**4/(G*Msh*Msun)
info(f"   M1 shuffle M_b against V_flat: sd(log a_0) goes {np.std(np.log10(a0b)):.3f} -> {np.std(np.log10(a_sh)):.3f} dex, "
     f"median {np.median(a0b):.3e} -> {np.median(a_sh):.3e}")
ck("M105-1 shuffling which baryonic mass belongs to which rotation speed destroys the meter: the spread rises by "
   "more than a factor 3, so the 0.24 dex the real data show is a real relation and not an artefact of the ranges",
   np.std(np.log10(a_sh)) > 3*np.std(np.log10(a0b)),
   f"real sd {np.std(np.log10(a0b)):.3f} dex vs shuffled {np.std(np.log10(a_sh)):.3f} dex")
# closure: synthesise a BTFR with slope exactly 4 at a known a_0 and recover it
for a_in in (A0["canonical"], A0["alt"]):
    for sc in (0.0, 0.24):
        Msyn = (Vf*1e3)**4/(G*a_in)/Msun*10**rng.normal(0, sc, len(Vf))
        a_out = (Vf*1e3)**4/(G*Msyn*Msun)
        info(f"   closure: injected a_0 = {a_in:.3e} with {sc:.2f} dex of BTFR scatter -> recovered "
             f"{np.median(a_out):.3e} ({math.log10(np.median(a_out)/a_in):+.4f} dex), TLS slope "
             f"{slopes(Msyn, Vf)[2]:.3f}")
        if a_in == A0["canonical"] and sc == 0.0: clo0 = math.log10(np.median(a_out)/a_in); slo0 = slopes(Msyn, Vf)[2]
        if a_in == A0["canonical"] and sc > 0: clos = math.log10(np.median(a_out)/a_in)
ck("M105-2 closure: a synthetic BTFR of slope exactly 4 at a known a_0 is recovered exactly with no scatter and to "
   "better than 0.05 dex with SPARC's own 0.24 dex of scatter -- so the estimator itself is sound and everything "
   "found above is in the data, not in the arithmetic",
   abs(clo0) < 1e-9 and abs(slo0 - 4.0) < 1e-6 and abs(clos) < 0.05,
   f"noiseless recovery {clo0:+.2e} dex with slope {slo0:.6f}; with 0.24 dex scatter {clos:+.4f} dex")

P(""); P("="*120)
P("VERDICT (item 105).  The BTFR zero-point is a usable a_0 meter only with two corrections that item 105 asked to")
P("have measured before the z ~ 2.5 test is designed, and this script measures both:")
P(f"  * STRUCTURAL.  V_flat^4 = G M_b a_0 is exact only asymptotically.  On SPARC's own outermost points it overstates")
P(f"    a_0 by {math.log10(np.median(Cv)):+.2f} dex; at one effective radius, where high-z curves are sampled, RC100's own")
P(f"    epsilon and y make it {math.log10(np.median(rcC)):+.2f} dex, so {math.log10(np.median(rcC)/np.median(Cv)):+.2f} dex does not cancel between the two ends.")
P(f"    Removing it with the kernel gives a_0 = {medL:.2e}, canonical to {abs(math.log10(medL/A0['canonical'])):.2f} dex -- but the same estimator moves")
P(f"    0.08 dex between R_eff and the last point, so this does not decide a footing.")
P(f"  * MASS-TO-LIGHT.  At Upsilon = 0.5 the meter's gas-rich and star-rich halves disagree by {abs(scan[0.5]['split']):.2f} dex and the BTFR")
P(f"    slope is {tls:.2f}, not 4.  Both close at Upsilon ~ {ups_close:.1f}, which contradicts item 76 and stellar populations.")
P(f"  * PRECISION.  {100*(10**prec-1):.1f}% statistical on 122 galaxies; {100*(10**tot-1):.0f}% with the coherent terms; {100*(10**abs(scan[0.5]['split'])-1):.0f}% if the internal split")
P(f"    is taken as the systematic it is.  The item's 5% is reached only in the statistical term.")
P(f"  * FOR z ~ 2.5.  N is not the constraint (about {(np.std(np.log10(a0b))*1.25/need)**2:.0f} galaxies suffice statistically).  Measured gas, a flat")
P(f"    outer curve and a shared Upsilon convention are.  A z ~ 2.5 zero-point built on scaling-relation gas cannot")
P(f"    reach +-{DECISIVE:.2f} dex however many galaxies it has.")
P("="*120)
sys.exit(ck.done())
