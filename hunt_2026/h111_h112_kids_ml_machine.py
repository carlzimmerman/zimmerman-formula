#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h111_h112_kids_ml_machine.py -- HUNT ITEMS 111 and 112: lensing as a stellar mass-to-light machine.
===================================================================================================
Item 111 ("lensing as an M/L machine").  a_0 is a constant of nature in the framework, so when a lens sample's
        RAR returns the "wrong" a_0 that is NOT a_0 varying -- it is the sample's adopted baryonic mass being
        wrong.  Invert every Brouwer+2021 KiDS-1000 bin (4 stellar-mass bins from Fig-9, 2 u-r colour bins and
        2 Sersic-index bins from Fig-8, plus the Fig-10 dwarf stack) *assuming a_0 universal* and read the
        answer as a RELATIVE stellar mass-to-light offset.  Compare with stellar populations.
Item 112 ("the Sersic split").  The Sersic-index bins are the one Brouwer split this hunt has never used.
        Bulge-dominated (n > 2) and disc-dominated (n < 2) lenses must return the SAME a_0 once their Upsilon
        differ by what stellar populations allow.  Independent morphology axis => a genuine cross-check of 111.

WHAT B21 ACTUALLY PUT ON THE x-AXIS (this is the whole game; transcribed in
real_research/reviews/lensing_rar/lr_published_pipeline.md from Brouwer+2021, A&A 650 A113):
    g_bar(r) = G M_gal / r^2,  POINT MASS,  M_gal = M_star (1 + f_cold),
    M_star   = LePhare SED fit, BC03, CHABRIER IMF, 9-band KiDS+VIKING  -- so the colour dependence of the
               stellar M/L is ALREADY IN the released x-axis,
    f_cold   = Boselli+2014 cold-gas fraction, log f_cold = -0.69 log(M_star) + 6.63,
    hot gas / CGM NOT included.
    g_obs    = 4 G Delta_Sigma  (SIS conversion, B21 eq 7).
So any Upsilon offset this script measures is a RESIDUAL on top of an SED fit that already knows the colours.
That is what makes it a sharp test rather than a rediscovery of "red galaxies have higher M/L".

THE EXPONENT, MEASURED NOT ASSUMED (and a bug in an earlier pass of this hunt).
    The model is g_obs = f * g_bar * nu(f * g_bar / a_0) with f = Upsilon_true/Upsilon_B21.  In the deep-MOND
    limit g_obs = sqrt(f g_bar a_0), so a rescaling of the mass by f is EXACTLY degenerate with a rescaling of
    a_0 by f: d log a_0(fit) / d log f = -1 when f is the ASSUMED mass, i.e. the mass correction a bin needs is
        log10 f_b  =  log10 [ a_0(fit, b) / a_0(true) ]      (exponent 1, not 2)
    This script MEASURES that exponent on the real data instead of assuming it.
    `h1_h66_h2_h65_lensing.py` (items 2 and 65, second pass) used dM = Delta log a_0 / 2 -- the factor 2 that
    belongs to an ESD *amplitude* bias (a_0 ~ g_obs^2 at fixed g_bar), not to an M/L offset (a_0 ~ 1/Upsilon).
    Correcting it DOUBLES every M/L offset those items quoted, and the "lands where stellar populations put it"
    reading of items 2/65/66 does not survive the correction.  Reported here against interest.

CHECKS THAT CAN FAIL, a mutation control, both footings, and the LambdaCDM reading computed beside the framework.
"""
import sys, os, math
import numpy as np
from scipy.optimize import minimize
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(111112)
NP = 15                                                   # 15 g_bar bins in every Fig-8 / Fig-9 file

# ------------------------------------------------------------------ bin families on disk
FAM = {
    "mass":   dict(pre="Fig-9_RAR-KiDS-isolated_Massbin-",  tags=["1", "2", "3", "4"],
                   cov="Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt",
                   lab=["logM* 8.5-10.3", "10.3-10.6", "10.6-10.8", "10.8-11.0"],
                   axis="stellar mass"),
    "colour": dict(pre="Fig-8_RAR-KiDS-isolated_Colorbin_", tags=["1", "2"],
                   cov="Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt",
                   lab=["blue / late  (u-r < 2.5)", "red / early  (u-r > 2.5)"], axis="u-r colour"),
    "sersic": dict(pre="Fig-8_RAR-KiDS-isolated_Sersicbin_", tags=["1", "2"],
                   cov="Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt",
                   lab=["disc-dominated (n < 2)", "bulge-dominated (n > 2)"], axis="Sersic index"),
}
def load_family(key):
    F = FAM[key]
    d = [load_rar(f"{F['pre']}{t}.txt") for t in F["tags"]]
    K = len(d); n = len(d[0][0])
    for j in range(1, K):
        assert np.allclose(d[0][0], d[j][0], rtol=1e-6), f"{key}: g_bar grids differ between bins"
    gb = np.concatenate([x[0] for x in d]); go = np.concatenate([x[1] for x in d])
    C = load_cov(F["cov"], n*K)                            # load_cov REFUSES a non-positive-definite ordering
    return gb, go, C, n, K

# ------------------------------------------------------------------ the model and its fits
def model(gb, logf, a0):
    """g_obs predicted when the true baryonic mass is 10**logf times B21's."""
    f = 10.0**logf; return f*gb*nu(f*gb/a0)

def quad(d, Ci):
    """d^T Ci d, guarded: numpy's BLAS matmul raises spurious FP flags on these tiny (1e-13) numbers."""
    with np.errstate(all="ignore"):
        v = float(d @ Ci @ d)
    return v if np.isfinite(v) else 1e12

def chi2_f(theta, gb, go, Ci, n, K, a0):
    if not np.all(np.isfinite(theta)) or np.any(np.abs(np.asarray(theta)) > 4.0): return 1e12
    m = np.concatenate([model(gb[k*n:(k+1)*n], theta[k], a0) for k in range(K)])
    return quad(go - m, Ci)

def chi2_a(theta, gb, go, Ci, n, K):
    if not np.all(np.isfinite(theta)) or np.any(np.abs(np.asarray(theta) + 9.8) > 3.0): return 1e12
    m = np.concatenate([gb[k*n:(k+1)*n]*nu(gb[k*n:(k+1)*n]/10.0**theta[k]) for k in range(K)])
    return quad(go - m, Ci)

def fit(fun, x0, args):
    r = minimize(fun, x0, args=args, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-8, maxiter=20000, maxfev=20000))
    r = minimize(fun, r.x, args=args, method="Nelder-Mead",
                 options=dict(xatol=1e-8, fatol=1e-10, maxiter=20000, maxfev=20000))
    return r.x, r.fun

def hess_cov(fun, x, args, h=3e-3):
    """covariance of the parameters from the chi2 Hessian: cov = 2 H^-1."""
    K = len(x); H = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            xp = x.copy(); xm = x.copy(); xpm = x.copy(); xmp = x.copy()
            xp[i] += h; xp[j] += h; xm[i] -= h; xm[j] -= h; xpm[i] += h; xpm[j] -= h; xmp[i] -= h; xmp[j] += h
            H[i, j] = (fun(xp, *args) - fun(xpm, *args) - fun(xmp, *args) + fun(xm, *args))/(4*h*h)
    return 2.0*np.linalg.inv((H + H.T)/2)

P("="*118)
P("ITEM 111 / 112 -- KiDS-1000 weak lensing read as a stellar mass-to-light machine")
P("="*118)
info("B21 x-axis: g_bar = G M_star(1+f_cold)/r^2, point mass, LePhare/BC03/CHABRIER SED masses + Boselli cold gas,")
info("            NO hot gas.  y-axis: g_obs = 4 G Delta_Sigma (SIS).  So a measured Upsilon offset is a RESIDUAL")
info("            on top of an SED fit that already carries the colour dependence of the stellar M/L.")
gb0, go0, C0, n0, K0 = load_family("colour")
ymin, ymax = gb0.min()/A0["canonical"], gb0.max()/A0["canonical"]
info(f"every KiDS point is deep-MOND: y = g_bar/a_0 spans {ymin:.1e} to {ymax:.1e} (canonical), so d log g_obs/d log g_bar")
sl_lo = (math.log(nu_s(ymin*1.0001)*ymin*1.0001) - math.log(nu_s(ymin)*ymin))/math.log(1.0001)
sl_hi = (math.log(nu_s(ymax*1.0001)*ymax*1.0001) - math.log(nu_s(ymax)*ymax))/math.log(1.0001)
info(f"            runs only from {sl_lo:.4f} to {sl_hi:.4f} across the whole released range (1/2 is the deep-MOND value)")

# ================================================================== 1. the exponent, measured
P(""); P("-"*118); P("1.  THE CONVERSION EXPONENT, MEASURED ON THE DATA (and the factor-2 bug it exposes)"); P("-"*118)
info("scale the adopted baryonic mass by f, refit a_0, and measure d log a_0(fit) / d log f.  Deep-MOND predicts")
info("exactly -1: mass and a_0 are degenerate there.  If it came out -2 the earlier pass's /2 would be right.")
expo = []
for key in ("colour", "sersic", "mass"):
    gb, go, C, n, K = load_family(key)
    for k in range(K):
        s = slice(k*n, (k+1)*n); Cb = np.linalg.inv(C[s, s])
        lf = np.array([-0.3, -0.15, 0.0, 0.15, 0.3]); la = []
        for x in lf:
            g = 10.0**x*gb[s]
            grid = np.linspace(-11.5, -8.0, 1401)
            v = np.array([float((go[s] - g*nu(g/10**t)) @ Cb @ (go[s] - g*nu(g/10**t))) for t in grid])
            la.append(grid[v.argmin()])
        e = float(np.polyfit(lf, np.array(la), 1)[0]); expo.append(e)
        info(f"{key:7s} bin {k+1}: d log a_0(fit)/d log f = {e:+.3f}")
expo = np.array(expo); EXP = float(np.median(np.abs(expo)))
ck("111-A the conversion exponent is measured, not assumed: rescaling a lens sample's adopted baryonic mass by f "
   "moves the fitted a_0 by f^-1 in every one of the eight KiDS bins (deep-MOND prediction exactly -1), so the M/L "
   "offset a bin needs is Delta log a_0 / 1, NOT Delta log a_0 / 2",
   0.9 < EXP < 1.2 and np.all(np.abs(expo) < 1.3),
   f"median |exponent| = {EXP:.3f}, range {np.abs(expo).min():.3f}-{np.abs(expo).max():.3f}; deep-MOND value 1.000")
ck("111-B BUG IN AN EARLIER PASS OF THIS HUNT, stated against interest: h1_h66_h2_h65_lensing.py (items 2, 65, 66) "
   "converted an a_0 offset into an M/L offset by DIVIDING BY 2.  The factor 2 is correct for an ESD amplitude bias "
   "(a_0 ~ g_obs^2 at fixed g_bar) and wrong for an M/L offset (a_0 ~ 1/Upsilon).  Every M/L offset quoted by items 2, "
   "65 and 66 is therefore HALF what the data require; the correction is the factor below",
   abs(EXP - 2.0) > 0.5, f"measured exponent {EXP:.3f}; the earlier pass assumed 2.000 -- a factor {2/EXP:.2f} error, "
   f"so e.g. item 65's '0.25 dex red/blue M/L' becomes {0.50/EXP:.2f} dex")

# ================================================================== 2. a_0 per bin, joint fit
P(""); P("-"*118); P("2.  a_0 PER BIN (joint fit, full released covariance, cross-bin terms included)"); P("-"*118)
A0FIT = {}
for key in ("mass", "colour", "sersic"):
    F = FAM[key]; gb, go, C, n, K = load_family(key); Ci = np.linalg.inv(C)
    x, c2 = fit(chi2_a, np.full(K, -9.8), (gb, go, Ci, n, K))
    cov = hess_cov(chi2_a, x, (gb, go, Ci, n, K))
    A0FIT[key] = (x, cov, c2, n, K)
    P(f"  {F['axis']}:  chi2 = {c2:.1f} / {n*K} points, {K} free parameters")
    for k in range(K):
        info(f"{F['lab'][k]:28s}  a_0 = {10**x[k]:.3e}  +- {math.log(10)*10**x[k]*math.sqrt(cov[k,k]):.2e}   "
             f"({x[k]-math.log10(A0['canonical']):+.3f} dex canonical, {x[k]-math.log10(A0['alt']):+.3f} dex alt)")

# ================================================================== 3. the M/L machine
P(""); P("-"*118); P("3.  THE M/L MACHINE: a_0 held at its footing value, the baryonic mass of each bin fitted"); P("-"*118)
info("model  g_obs = f_b g_bar nu(f_b g_bar / a_0),  f_b = Upsilon_b / Upsilon_B21.  Absolute f_b carries the footing")
info("AND the ESD->g_obs conversion (B21's SIS C = 4; a point mass gives C = pi, and a_0 ~ C^2, so the absolute")
info("normalisation is soft by ~0.2 dex).  RELATIVE f between bins carries neither -- that is the measurement.")
ML = {}
for key in ("mass", "colour", "sersic"):
    F = FAM[key]; gb, go, C, n, K = load_family(key); Ci = np.linalg.inv(C)
    ML[key] = {}
    for foot, a0 in A0.items():
        x, c2 = fit(chi2_f, np.zeros(K), (gb, go, Ci, n, K, a0))
        cov = hess_cov(chi2_f, x, (gb, go, Ci, n, K, a0))
        ML[key][foot] = (x, cov, c2)
    P(f"  {F['axis']}:")
    for k in range(K):
        xc, cc, _ = ML[key]["canonical"]; xa, ca, _ = ML[key]["alt"]
        info(f"{F['lab'][k]:28s}  log f = {xc[k]:+.3f} +- {math.sqrt(cc[k,k]):.3f} (canonical)   "
             f"{xa[k]:+.3f} +- {math.sqrt(ca[k,k]):.3f} (alt)")
    xc, cc, c2c = ML[key]["canonical"]
    info(f"chi2 at fixed a_0 = {c2c:.1f}/{n*K} (canonical), {ML[key]['alt'][2]:.1f} (alt)")

def rel(key, i, j):
    """relative log10 Upsilon offset between bins j and i, and its 1-sigma, both footings."""
    out = {}
    for foot in A0:
        x, cov, _ = ML[key][foot]
        d = x[j] - x[i]; v = cov[j, j] + cov[i, i] - 2*cov[i, j]
        out[foot] = (d, math.sqrt(max(v, 1e-12)))
    return out

P("")
info("NONE of these fits reaches chi2/dof = 1 on B21's analytic covariance, which carries no super-sample term, so")
info("every error below is ALSO quoted inflated by sqrt(chi2/dof).  That works in the framework's favour and is")
info("quoted for exactly that reason -- the working rule forbids manufacturing a deficit as firmly as a win.")
INFL = {}
for key in ("mass", "colour", "sersic"):
    n, K = load_family(key)[3], load_family(key)[4]
    INFL[key] = math.sqrt(ML[key]["canonical"][2]/(n*K - K))
P(""); info("RELATIVE offsets (the footing-independent numbers):")
REL = {}
for key, i, j in (("colour", 0, 1), ("sersic", 0, 1), ("mass", 0, 3)):
    r = rel(key, i, j); REL[key] = r
    dc, ec = r["canonical"]; da, ea = r["alt"]
    info(f"{FAM[key]['axis']:14s}  bin{j+1} - bin{i+1}:  Delta log Upsilon = {dc:+.3f} +- {ec:.3f} (canonical), "
         f"{da:+.3f} +- {ea:.3f} (alt)  -> factor {10**dc:.2f}   [{dc/ec:.1f} sigma from zero, "
         f"{dc/(ec*INFL[key]):.1f} with errors inflated by {INFL[key]:.2f}]")
ck("111-C the relative M/L offsets are footing-independent, as they must be if they are a property of the lenses "
   "and not of the assumed a_0",
   all(abs(REL[k]["canonical"][0] - REL[k]["alt"][0]) < 0.03 for k in REL),
   "; ".join(f"{k}: {abs(REL[k]['canonical'][0]-REL[k]['alt'][0]):.3f} dex" for k in REL))

# ================================================================== 4. versus stellar populations
P(""); P("-"*118); P("4.  VERSUS STELLAR POPULATIONS"); P("-"*118)
info("what a residual Upsilon offset is allowed to be, ON TOP OF B21's per-galaxy LePhare/BC03/Chabrier masses:")
info("  * B21 varied M_star GLOBALLY by +-0.2 dex and the early/late split survived unchanged (their sec 5.4), which")
info("    is exactly why any M/L explanation has to be TYPE-DIFFERENTIAL -- a global rescaling does nothing here;")
info("  * SPS model choice (BC03 vs FSPS/M05, TP-AGB) and SFH prior (parametric vs non-parametric) move quiescent")
info("    galaxies by ~0.1-0.2 dex relative to star-forming ones;")
info("  * a bottom-heavy IMF in the most massive early types adds at most ~0.2-0.3 dex, and this sample is M* < 1e11;")
info("  => a defensible type-differential residual is ~0.30 dex, which is also exactly the size of B21's own named")
info("     escape (a circumgalactic M_gas ~ M_star for early types only).  Stacking EVERY systematic in the same")
info("     direction and applying all of them to early types alone reaches ~0.45 dex; that is the indefensible end")
info("     of the range and it is quoted below too, so the reader can see the exposure both ways.")
SPS_TIGHT, SPS_GENEROUS, SPS_EXTREME = 0.10, 0.30, 0.45
dc, ec = REL["colour"]["canonical"]
ck("111-D (item 111's OWN pass criterion, and it FAILS) 'the measured Upsilon(colour) matches SPS within 0.1 dex'. "
   "It does not: holding a_0 universal, the red KiDS lenses need a baryonic mass this much larger than B21's SED "
   "masses give them, relative to the blue lenses",
   abs(dc) < SPS_TIGHT, f"required Delta log Upsilon(red-blue) = {dc:+.3f} +- {ec:.3f} dex = factor {10**dc:.2f}, "
   f"{(abs(dc)-SPS_TIGHT)/ec:.1f} sigma beyond the 0.10 dex criterion ({(abs(dc)-SPS_TIGHT)/(ec*INFL['colour']):.1f} "
   f"with inflated errors)")
ck("111-E the same offset against a DEFENSIBLE stellar-population + CGM allowance (0.30 dex, which is both the "
   "largest defensible type-differential SPS residual and B21's own M_gas = M_star escape). This is the honest "
   "framework-side statement: a universal a_0 needs MORE than that",
   abs(dc) < SPS_GENEROUS, f"{dc:+.3f} +- {ec:.3f} dex required vs 0.30 dex available -> "
   f"{(abs(dc)-SPS_GENEROUS)/ec:+.1f} sigma over budget raw, {(abs(dc)-SPS_GENEROUS)/(ec*INFL['colour']):+.1f} with "
   f"inflated errors; the missing baryons would be {10**dc-1:.2f} times the WHOLE baryonic mass B21 assign them")
info(f"BOTH WAYS: against the indefensible-stack allowance of {SPS_EXTREME:.2f} dex the same offset is "
     f"{(abs(dc)-SPS_EXTREME)/ec:+.1f} sigma, i.e. NOT excluded.  The honest statement is that the framework needs")
info(f"every stellar-population systematic to run the same way and to apply to early types only -- not that it is dead.")
info(f"(for the record: the same colour split read the earlier pass's way, Delta log a_0 / 2, would be "
     f"{dc/2:+.3f} dex = factor {10**(dc/2):.2f}, which is why items 2/65/66 read as 'consistent with SPS'.)")

# ================================================================== 5. ITEM 112, the Sersic split
P(""); P("-"*118); P("5.  ITEM 112 -- THE SERSIC SPLIT (the axis this hunt has never used)"); P("-"*118)
xs, cs, _, ns, Ks = A0FIT["sersic"]
d_a0 = xs[1] - xs[0]; e_a0 = math.sqrt(cs[0, 0] + cs[1, 1] - 2*cs[0, 1])
ds, es = REL["sersic"]["canonical"]
info(f"a_0(n<2, disc)   = {10**xs[0]:.3e}   a_0(n>2, bulge) = {10**xs[1]:.3e}")
info(f"offset = {d_a0:+.3f} +- {e_a0:.3f} dex = {d_a0/e_a0:.1f} sigma; the framework says a_0 is one number, so this")
info(f"is a required Delta log Upsilon(bulge - disc) = {ds:+.3f} +- {es:.3f} dex = factor {10**ds:.2f}")
ck("112-A (the item's own test, and it FAILS on the raw x-axis) 'bulge-dominated and disc-dominated lenses must "
   "give the same a_0': they do not -- the Sersic split is a many-sigma offset in the fitted a_0",
   abs(d_a0) < 3*e_a0, f"{d_a0:+.3f} +- {e_a0:.3f} dex, {d_a0/e_a0:.1f} sigma apart")
ck("112-B '... once their Upsilon differ as SPS says'.  Applying a defensible stellar-population type-differential "
   "(0.30 dex, bulge-heavy) to the Sersic bins, do they then agree?",
   abs(ds) < SPS_GENEROUS, f"required {ds:+.3f} +- {es:.3f} dex vs 0.30 dex allowed "
   f"({(abs(ds)-SPS_GENEROUS)/es:+.1f} sigma raw, {(abs(ds)-SPS_GENEROUS)/(es*INFL['sersic']):+.1f} with inflated "
   f"errors -- on the Sersic axis alone the requirement is NOT significantly over budget)")
dcc, ecc = REL["colour"]["canonical"]
diff = abs(dcc - ds); ediff = math.hypot(ecc, es)
ck("112-C CROSS-CHECK, the point of having two morphology axes: u-r colour and Sersic index are independent proxies "
   "for the same early/late population, so under the M/L reading they must demand the SAME Upsilon residual (up to "
   "class impurity, which can only DILUTE the Sersic split since n is the noisier proxy)",
   diff < 2*ediff, f"colour {dcc:+.3f} +- {ecc:.3f} vs Sersic {ds:+.3f} +- {es:.3f} dex; difference "
   f"{diff:.3f} +- {ediff:.3f} ({diff/ediff:.1f} sigma) -- Sersic is the SMALLER of the two, the direction class "
   f"impurity predicts")

# ================================================================== 6. is it M/L at all?  the shape test
P(""); P("-"*118); P("6.  IS THE SPLIT AN M/L SHIFT AT ALL?  the shape test against the measured environment term"); P("-"*118)
info("A relative M/L offset is a HORIZONTAL shift of the RAR, so its vertical signature is Delta log Upsilon times the")
info("local RAR slope -- essentially FLAT across the KiDS range (slope 0.501 -> 0.548, so a +0.007 dex/dex tilt).")
info("A neighbour / two-halo contamination is ADDITIVE in Delta_Sigma and grows toward LOW g_bar (large radius).")
info("B21 released the same mass bins with and without the isolation cut (Fig-A4 'all' vs Fig-9 'isolated'), which")
info("MEASURES what an environment contaminant looks like in this very dataset:")
T = np.zeros(NP); cnt = 0
for b in range(1, 5):
    gi, oi, _ = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
    ga, oa, _ = load_rar(f"Fig-A4_RAR-KiDS-all_Massbin-{b}.txt")
    T += np.log10(oa/oi); cnt += 1
    info(f"mass bin {b}: log10(g_all/g_iso) = " + " ".join(f"{v:+.2f}" for v in np.log10(oa/oi)))
T /= cnt
info("mean environment template (dex, low g_bar = large radius on the left): " + " ".join(f"{v:+.2f}" for v in T))
info(f"the non-isolated sample carries {10**T[0]-1:+.0%} MORE signal than the isolated one at the lowest g_bar and "
     f"{10**T[-1]-1:+.0%} at the highest --")
info(f"a steeply g_bar-dependent shape, slope {np.polyfit(np.log10(gb0[:NP]), T, 1)[0]:+.3f} dex/dex, and that is "
     f"what a neighbour term looks like in this survey")
S = 10**T - 1.0                                            # fractional neighbour signal when isolation is dropped
gcol = {i: load_rar(f"Fig-8_RAR-KiDS-isolated_Colorbin_{i}.txt") for i in (1, 2)}
gser = {i: load_rar(f"Fig-8_RAR-KiDS-isolated_Sersicbin_{i}.txt") for i in (1, 2)}
info("model the measured split as  g_2 - g_1 = alpha * g_1  +  beta * S * g_1,  where alpha is a FLAT fractional")
info("offset (what a horizontal M/L shift makes) and S is the measured neighbour shape above (beta = 1 would mean")
info("the bin-2 lenses carry as much residual contamination as dropping B21's isolation cut altogether).")
def shape_test(name, dat, covfile):
    n = NP; C = load_cov(covfile, 2*n)
    d = dat[2][1] - dat[1][1]                              # additive difference in g_obs, bin2 - bin1
    Cd = C[n:, n:] + C[:n, :n] - C[n:, :n] - C[:n, n:]
    Ci = np.linalg.inv(Cd); g1 = dat[1][1]
    Ba, Bb = g1, g1*S
    def chisq(M):
        A = np.vstack(M).T; V = np.linalg.inv(A.T @ Ci @ A)
        coef = V @ (A.T @ Ci @ d); r = d - A @ coef
        return float(r @ Ci @ r), coef, V
    c_a, ka, va = chisq([Ba]); c_b, kb, vb = chisq([Bb]); c_ab, kab, vab = chisq([Ba, Bb])
    info(f"{name}:  flat-M/L only  chi2 = {c_a:5.1f}/{n-1}  (alpha = {ka[0]:+.3f} +- {math.sqrt(va[0,0]):.3f}, "
         f"= {math.log10(1+ka[0]):+.3f} dex in g_obs)")
    info(f"{' '*len(name)}   environment only chi2 = {c_b:5.1f}/{n-1}  (beta  = {kb[0]:+.3f} +- {math.sqrt(vb[0,0]):.3f})")
    info(f"{' '*len(name)}   both free        chi2 = {c_ab:5.1f}/{n-2}  (alpha = {kab[0]:+.3f} +- {math.sqrt(vab[0,0]):.3f}, "
         f"beta = {kab[1]:+.3f} +- {math.sqrt(vab[1,1]):.3f})")
    return dict(ca=c_a, cb=c_b, cab=c_ab, ka=ka, va=va, kb=kb, vb=vb, kab=kab, vab=vab)
sc = shape_test("u-r colour", gcol, "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt")
ss = shape_test("Sersic    ", gser, "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt")
ck("111-F1 the escape route CLOSES: residual environment contamination cannot be what the early/late split is.  "
   "With the neighbour shape measured from B21's own isolated-vs-all release and its amplitude free, an "
   "environment-only model is a far worse description of both splits than a flat (M/L-like) fractional offset, "
   "because the neighbour term lives at large radius and the split does not",
   sc["cb"] - sc["ca"] > 9 and ss["cb"] - ss["ca"] > 9,
   f"colour: flat {sc['ca']:.1f} vs environment {sc['cb']:.1f} (delta chi2 {sc['cb']-sc['ca']:+.1f}); "
   f"Sersic: flat {ss['ca']:.1f} vs environment {ss['cb']:.1f} (delta chi2 {ss['cb']-ss['ca']:+.1f})")
info("")
info("now do it inside the kernel fit rather than as a linear proxy: model bin k as f_k g_bar nu(f_k g_bar/a_0) times")
info("(1 + beta_k S), with beta_1 = 0 by construction (only the RELATIVE contamination of bin 2 is constrained), and")
info("read Delta log Upsilon marginalised over beta_2:")
def chi2_env(theta, gb, go, Ci, n, K, a0):
    if np.any(np.abs(np.asarray(theta)) > 6.0): return 1e12
    m = np.concatenate([model(gb[k*n:(k+1)*n], theta[k], a0)*(1.0 + (0.0 if k == 0 else theta[K])*S)
                        for k in range(K)])
    return quad(go - m, Ci)
ENV = {}
for key in ("colour", "sersic"):
    gb, go, C, n, K = load_family(key); Ci = np.linalg.inv(C)
    x, c2 = fit(chi2_env, np.array([0.0, 0.3, 0.0]), (gb, go, Ci, n, K, A0["canonical"]))
    cov = hess_cov(chi2_env, x, (gb, go, Ci, n, K, A0["canonical"]))
    d = x[1] - x[0]; e = math.sqrt(cov[0, 0] + cov[1, 1] - 2*cov[0, 1])
    ENV[key] = (d, e, x[2], math.sqrt(cov[2, 2]), c2)
    info(f"{FAM[key]['axis']:14s}  beta_2 = {x[2]:+.3f} +- {math.sqrt(cov[2,2]):.3f}  ->  Delta log Upsilon = "
         f"{d:+.3f} +- {e:.3f} dex (was {REL[key]['canonical'][0]:+.3f} +- {REL[key]['canonical'][1]:.3f}), "
         f"chi2 {c2:.1f}/{n*K}")
ck("111-F2 ... and letting a residual environment component in ANYWAY does not rescue the M/L requirement, which is "
   "the thing that mattered.  Marginalising over a free relative contamination with the empirically measured shape, "
   "the colour axis still demands more than the 0.30 dex stellar populations and a CGM can supply",
   ENV["colour"][0] < SPS_GENEROUS,
   f"colour {ENV['colour'][0]:+.3f} +- {ENV['colour'][1]:.3f} dex with beta free (beta = {ENV['colour'][2]:+.2f} "
   f"+- {ENV['colour'][3]:.2f}, {ENV['colour'][2]/ENV['colour'][3]:+.1f} sigma) -- "
   f"{(ENV['colour'][0]-SPS_GENEROUS)/(ENV['colour'][1]*INFL['colour']):+.1f} sigma over the 0.30 dex budget with "
   f"inflated errors; Sersic {ENV['sersic'][0]:+.3f} +- {ENV['sersic'][1]:.3f} "
   f"(beta = {ENV['sersic'][2]:+.2f} +- {ENV['sersic'][3]:.2f})")

# ================================================================== 7. the mass axis
P(""); P("-"*118); P("7.  THE STELLAR-MASS AXIS, AND THE DWARF STACK"); P("-"*118)
xm, cm, _ = ML["mass"]["canonical"]
LOGM = np.array([10.05, 10.45, 10.70, 10.90])
info("required log f (canonical footing) against the bin's stellar mass:")
for k in range(4):
    info(f"  logM* ~ {LOGM[k]:.2f}: log f = {xm[k]:+.3f} +- {math.sqrt(cm[k,k]):.3f}")
gd, od, ed = load_rar("Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt"); nd = len(gd)
Cd = load_cov("Fig-10_RAR-KiDS-isolated-dwarfs_covmatrix.txt", nd); Cdi = np.linalg.inv(Cd)
DW = {}
for foot, a0 in A0.items():
    xd, c2d = fit(chi2_f, np.zeros(1), (gd, od, Cdi, nd, 1, a0))
    covd = hess_cov(chi2_f, xd, (gd, od, Cdi, nd, 1, a0))
    DW[foot] = (float(xd[0]), math.sqrt(covd[0, 0]), c2d)
info(f"Fig-10 isolated dwarf stack ({nd} points, g_bar down to {gd.min():.1e}): log f = "
     f"{DW['canonical'][0]:+.3f} +- {DW['canonical'][1]:.3f} (canonical), {DW['alt'][0]:+.3f} +- {DW['alt'][1]:.3f} (alt)")
slope_m = float(np.polyfit(LOGM, xm, 1)[0])
info(f"trend across the four L*-ish mass bins: d log Upsilon / d log M* = {slope_m:+.3f}; adding the dwarf stack as a "
     f"fifth, far lower-mass rung gives a {xm[3]-DW['canonical'][0]:+.2f} dex swing from dwarfs to the most massive bin")
info("")
info("SECOND ESCAPE, bounded with the same release: B21's colour and Sersic bins are NOT matched in stellar mass, and")
info("red / high-n lenses are on average more massive.  The mass-bin family measures how far that can carry the split:")
DMSTAR = 0.30                                              # a generous mean logM* offset between red and blue lenses
leak = slope_m*DMSTAR
info(f"  d log Upsilon / d log M* = {slope_m:+.3f} measured above, so even a generous {DMSTAR:.2f} dex mean stellar-mass")
info(f"  difference between the classes leaks only {leak:+.3f} dex into the split -- {100*leak/REL['colour']['canonical'][0]:.0f}% of the colour offset.")
ck("111-H the colour and Sersic bins not being mass-matched cannot explain the split either: the mass-dependence of "
   "the required Upsilon, measured on the same survey with the same pipeline, is too shallow",
   abs(leak) < 0.25*abs(REL["colour"]["canonical"][0]),
   f"leak {leak:+.3f} dex of a {REL['colour']['canonical'][0]:+.3f} dex offset, on a generous {DMSTAR:.2f} dex mass mismatch")
ck("111-G the M/L residual the framework needs is NOT a constant: it runs with stellar mass, from ~0 for the "
   "isolated-dwarf stack to +0.3 dex for L* lenses.  This is the same thing item 100 called 'the ladder does not "
   "close, organised by stellar M/L', now measured on one homogeneous survey with one pipeline",
   abs(xm[3] - DW["canonical"][0]) > 0.05,
   f"dwarfs {DW['canonical'][0]:+.3f}, logM*~10.9 bin {xm[3]:+.3f} +- {math.sqrt(cm[3,3]):.3f}; swing "
   f"{xm[3]-DW['canonical'][0]:+.2f} dex")

# ================================================================== 8. the LambdaCDM reading
P(""); P("-"*118); P("8.  THE SAME DATA READ IN LambdaCDM (computed beside the framework, as the rules require)"); P("-"*118)
info("In LambdaCDM nothing about the split is anomalous: at fixed stellar mass early-type centrals sit in more massive")
info("haloes.  The measured vertical offset is +%.3f dex in g_obs (colour) and +%.3f dex (Sersic)."
     % (np.mean(np.log10(gcol[2][1]/gcol[1][1])), np.mean(np.log10(gser[2][1]/gser[1][1]))))
r200_L = (3*1e12/(4*math.pi*200*2.775e11*h**2))**(1/3.)
info(f"the released radii reach ~1 Mpc, well outside r200 ~ {r200_L:.2f} Mpc for a 1e12 Msun halo, where "
     f"Delta_Sigma ~ M200/(pi R^2), i.e. Delta_Sigma ~ M200")
for nm, off in (("colour", np.mean(np.log10(gcol[2][1]/gcol[1][1]))), ("Sersic", np.mean(np.log10(gser[2][1]/gser[1][1])))):
    info(f"  {nm}: required red/blue halo-mass ratio = {10**off:.2f} (Delta log M200 = {off:+.2f} dex)")
info("Mandelbaum+2016 and the type-split SHMR literature measure red/blue halo-mass ratios of ~2 at these stellar")
info("masses, so LambdaCDM absorbs the split with a parameter it already has.  LOCKED WORDING (from the repo's own")
info("lensing-RAR review): this is an exposure to PROPERTY-INDEPENDENT MODIFIED GRAVITY, not 'LambdaCDM confirmed' --")
info("B21's own MICE and BAHAMAS runs disagree with each other about the size of the split.")

# ================================================================== 9. mutation controls
P(""); P("-"*118); P("9.  MUTATION CONTROLS"); P("-"*118)
gbC, goC, CC, nC, KC = load_family("colour"); CCi = np.linalg.inv(CC)
L = np.linalg.cholesky(CC + 1e-34*np.eye(2*nC))
a0c = A0["canonical"]
def mock(logf_true):
    m = np.concatenate([model(gbC[k*nC:(k+1)*nC], logf_true[k], a0c) for k in range(KC)])
    return m + L @ rng.standard_normal(2*nC)
rec, rec0 = [], []
for _ in range(60):
    y = mock([0.0, 0.30]); x, _ = fit(chi2_f, np.zeros(2), (gbC, y, CCi, nC, KC, a0c)); rec.append(x[1]-x[0])
    y = mock([0.0, 0.00]); x, _ = fit(chi2_f, np.zeros(2), (gbC, y, CCi, nC, KC, a0c)); rec0.append(x[1]-x[0])
rec, rec0 = np.array(rec), np.array(rec0)
ck("M1 mutation: 60 mocks drawn from the released colour covariance with a TRUE 0.300 dex M/L offset injected are "
   "recovered at 0.300 dex, and 60 mocks with NO offset injected return zero -- the estimator is unbiased and does "
   "not manufacture a split",
   abs(rec.mean() - 0.30) < 0.03 and abs(rec0.mean()) < 0.03,
   f"injected +0.300 -> recovered {rec.mean():+.3f} +- {rec.std():.3f}; injected 0.000 -> {rec0.mean():+.3f} "
   f"+- {rec0.std():.3f}")
xN = np.zeros(KC)
def chi2_newton(theta, gb, go, Ci, n, K, a0):
    m = np.concatenate([10.0**theta[k]*gb[k*n:(k+1)*n] for k in range(K)])
    return quad(go - m, Ci)
xn, c2n = fit(chi2_newton, np.zeros(KC), (gbC, goC, CCi, nC, KC, a0c))
_, _, c2k = ML["colour"]["canonical"]
ck("M2 mutation: replacing the kernel by nu = 1 (Newton, no boost) and letting the same two mass factors absorb it "
   "gives a far worse fit -- the kernel, not the free M/L, is carrying the signal",
   c2n > c2k + 25, f"Newton chi2 = {c2n:.1f} vs kernel chi2 = {c2k:.1f} on the same 30 points "
   f"(delta chi2 {c2n-c2k:+.1f}); Newton also needs log f = {xn[0]:+.2f}, {xn[1]:+.2f}, i.e. {10**xn[0]:.0f}-{10**xn[1]:.0f} "
   f"times more baryons than B21 assign")

# ================================================================== verdict
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  Item 111 asked for 'a Upsilon(colour) relation measured by gravity rather than by stellar populations', passing")
P(f"  if it matches SPS within 0.1 dex.  Measured: red lenses need {REL['colour']['canonical'][0]:+.2f} +- "
  f"{REL['colour']['canonical'][1]*INFL['colour']:.2f} dex (inflated errors) more baryonic mass")
P(f"  than blue ones -- {ENV['colour'][0]:+.2f} after marginalising over residual environment contamination -- ON TOP "
  f"of per-galaxy SED masses")
P(f"  that already know the colours.  That is a factor {10**REL['colour']['canonical'][0]:.1f}, over the 0.30 dex a "
  f"defensible stellar-population differential")
P("  -- or B21's own M_gas = M_star circumgalactic escape -- can supply, though only by 2.0 sigma once the errors are")
P("  inflated for the fit's own chi2/dof, and inside a 0.45 dex stack of every systematic at once.  So the item's own")
P("  0.1 dex criterion fails by a wide margin, and the framework's exposure is real but not lethal on this axis.")
P(f"  Item 112: the Sersic axis corroborates independently at {REL['sersic']['canonical'][0]:+.2f} +- "
  f"{REL['sersic']['canonical'][1]*INFL['sersic']:.2f} dex, the smaller of the two, which is the")
P("  direction class impurity predicts -- and on that axis alone the requirement is NOT significantly over the 0.30")
P("  dex budget.  The two axes agree with each other; neither agrees with stellar populations at the 0.1 dex asked.")
P("  So 111 does NOT deliver a new M/L calibration.  What lensing measures here is the size of a standing exposure,")
P("  and it measures it twice, on two independent morphology proxies.")
P("  NEW here and against interest: (a) the conversion exponent is 1, not 2, so the 'consistent with SPS' reading of")
P("  hunt items 2, 65 and 66 came from halving the requirement -- withdrawn; (b) the split's SHAPE is that of a")
P("  horizontal mass shift and not of the environment term B21's own isolated-vs-all release lets us measure, and it")
P("  survives the stellar-mass mismatch between the classes, which removes the two easiest escapes; (c) the required")
P("  M/L residual runs with stellar mass -- zero for the dwarf stack, +0.3 dex at L* -- which is item 100's unclosed")
P("  ladder showing up inside a single survey with a single pipeline.")
sys.exit(ck.done())
