#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02 -- THE ESTIMATOR-AMPLIFICATION LAW, AND WHY EVERY HIGH-REDSHIFT a_0 DISAGREES WITH EVERY OTHER.
Second-law hunt, angle 9 (the redshift axis).

THE CLOSED FORM UNDER TEST (derived here, then confronted with data)
    Write the kernel's local logarithmic slope   m(y) = d ln nu / d ln y,  y = g_bar/a_0.
    For Route A, nu(y) = 1/(1 - e^{-sqrt y}),      m(y) = - u / (2 (e^u - 1)),   u = sqrt(y),
    which runs from -1/2 (deep MOND) to 0^- (Newtonian).  Then for ANY estimator that reads a_0 off
    g_obs = g_bar nu(g_bar/a_0) at acceleration y, a coherent multiplicative error in the baryonic
    acceleration (stellar M/L, IMF, the gas correction, a squared distance error) propagates as

        LAMBDA(y)  ==  d ln a_0 / d ln Upsilon  =  (1 + m(y)) / m(y)

        LAMBDA(0) = -1 exactly ;  LAMBDA(0.065) = -1.28 ;  LAMBDA(1) = -2.3 ;  LAMBDA(3) = -4.3 ;
        LAMBDA(10) = -9.9 ;  LAMBDA -> -(1 + 2(e^u-1)/u) -> -infinity as y -> infinity.

    The framework therefore makes a PREDICTION ABOUT ITS OWN MEASURABILITY: a_0 can be read cleanly
    only where y is small, and high-redshift discs are observed at R_e where y ~ 1-3.  Everything a
    z ~ 1-2.5 survey reports about a_0 is its stellar mass calibration multiplied by 3-5.

WHAT THIS IS AND IS NOT.  LAMBDA(y) is a corollary of the radial acceleration relation, so it is NOT
an independent law of nature -- it is a theorem about measurement, and it is labelled that way here.
Its value is that it is FALSIFIABLE (the measured lever per survey must equal the predicted one), that
it quantitatively accounts for a disagreement item 101 could only report, and that it fixes the design
of the decisive z ~ 2.5 test.

BOTH FOOTINGS everywhere; mutation controls; the LambdaCDM alternative beside the framework.  No git.
"""
import os, sys, math, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hunt_lib import Check, P, info, A0, load_sparc, kpc, G, Msun
DATA = os.path.join(HERE, '..', 'real_research', 'data')

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0 / (-np.expm1(-np.sqrt(y)))
def mslope(y):
    """m(y) = d ln nu / d ln y = -u/(2(e^u - 1)), u = sqrt(y)."""
    u = np.sqrt(np.maximum(np.asarray(y, float), 1e-300))
    return np.where(u < 1e-6, -0.5 + u / 4.0, -u / (2.0 * np.expm1(u)))
def LAM(y):
    m = mslope(y); return (1.0 + m) / m

def fnum(s):
    try: return float(s)
    except Exception: return float('nan')

# ---------------------------------------------------------------- the a0 estimator used throughout
def a0_fit(gbar, gobs, w=None, grid=None):
    """Least-squares a0 in log g_obs at the sample's own g_bar values (no binning, no mass model)."""
    if grid is None: grid = 10.0 ** np.linspace(-12.5, -8.0, 4501)
    lg = np.log10(gobs)
    if w is None: w = np.ones_like(lg)
    best, bc = np.nan, np.inf
    for a0 in grid:
        r = lg - np.log10(gbar * nu(gbar / a0))
        c = float(np.sum(w * (r - np.average(r, weights=w) * 0.0) ** 2))
        if c < bc: bc, best = c, a0
    return best, bc

def a0_median_closed(gbar, gobs):
    """Per-object closed form: a0 = g_obs^2/g_bar in the deep limit, exact through the kernel otherwise.
    Solve nu(g_bar/a0) = g_obs/g_bar for a0 object by object (monotone -> bisection)."""
    gbar = np.asarray(gbar, float); gobs = np.asarray(gobs, float)
    R = gobs / gbar
    out = np.full_like(gbar, np.nan)
    ok = R > 1.0
    lo, hi = np.full(gbar.shape, -14.0), np.full(gbar.shape, -7.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        val = nu(gbar / 10.0 ** mid)              # increases with a0
        up = val < R
        lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    out[ok] = 10.0 ** (0.5 * (lo + hi))[ok]
    return out

# ================================================================================================
def main():
    ck = Check()
    P("=" * 122)
    P("PART 0 -- the amplification law, derived and then verified numerically before any data is touched")
    P("=" * 122)
    info("nu = 1/(1-e^-u), u = sqrt(y)  =>  d ln nu/du = -1/(e^u - 1),  d ln y = 2 du/u")
    info("                              =>  m(y) = d ln nu/d ln y = -u/(2(e^u - 1))")
    info("A coherent shift ln g_bar -> ln g_bar + d moves ln g_obs by (1+m) d at fixed a_0;")
    info("a shift ln a_0 -> ln a_0 + A moves it by -m A.  Compensation gives A = (1+m) d / m.")
    P("")
    P("        y = g_bar/a0        m(y)      LAMBDA(y) = d ln a0 / d ln Upsilon")
    for y in (1e-4, 1e-3, 0.01, 0.065, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 30.0):
        P(f"        {y:12.4g}   {float(mslope(y)):9.4f}      {float(LAM(y)):+10.3f}")
    # numerical verification of the analytic lever on the actual estimator
    errs = []; broke = []
    for ytest in (0.02, 0.065, 0.2, 1.0, 2.0, 3.0, 5.0, 10.0):
        a0t = A0['canonical']; gb = np.array([ytest * a0t])
        go = gb * nu(gb / a0t)
        d = 0.005                                    # small enough that the linearisation holds even at large y
        a_p = a0_median_closed(gb * 10 ** d, go)[0]; a_m = a0_median_closed(gb * 10 ** (-d), go)[0]
        lev = (math.log10(a_p) - math.log10(a_m)) / (2 * d)
        if np.isfinite(lev):
            errs.append(abs(lev - float(LAM(ytest))) / abs(float(LAM(ytest))))
            P(f"        numerical check at y = {ytest:6.3f}: analytic {float(LAM(ytest)):+9.4f}   "
              f"finite-difference on the exact inversion {lev:+9.4f}   (frac diff {errs[-1]:.2e})")
        else:
            broke.append(ytest)
            P(f"        numerical check at y = {ytest:6.3f}: analytic {float(LAM(ytest)):+9.4f}   "
              f"THE INVERSION HAS NO SOLUTION under a {d:.3f} dex baryonic-mass error -- g_obs falls below g_bar")
    ck("k02-0 the amplification law is DERIVED and then verified against a finite difference on the exact kernel "
       "inversion across three decades in y -- if the analytic form were wrong this fails",
       len(errs) >= 6 and max(errs) < 0.02,
       f"max fractional |analytic - numerical| = {max(errs):.2e} over the {len(errs)} values that invert")
    P("")
    P("    THE HARD EDGE.  The inversion exists only while g_obs > g_bar, i.e. while the coherent baryonic-mass")
    P("    error d (dex) stays below the boost the kernel supplies at that acceleration: d < log10 nu(y).")
    P(f"    {'y':>8}{'boost log10 nu(y) (dex)':>26}{'max tolerable mass error':>27}{'|LAMBDA|':>11}")
    edge = []
    for yv in (0.065, 0.2, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0):
        dmax = float(np.log10(nu(yv)))
        edge.append((yv, dmax))
        P(f"    {yv:>8.3f}{dmax:>26.4f}{dmax:>27.4f}{abs(float(LAM(yv))):>11.2f}")
    demo = [yv for yv, dm in edge if dm < 0.05]
    # demonstrate: at y = 10 a 0.05 dex mass error must destroy the inversion outright
    gb10 = np.array([10.0 * A0['canonical']]); go10 = gb10 * nu(gb10 / A0['canonical'])
    a_break = a0_median_closed(gb10 * 10 ** 0.05, go10)[0]
    ck("k02-0b AND THE HARD EDGE IS ITSELF A RESULT: the inversion exists only while the coherent baryonic-mass "
       "error is smaller than the boost, d < log10 nu(y).  At y = 10 that budget is 0.018 dex -- four percent in "
       "stellar mass -- so a survey observing at y >~ 5 cannot report a_0 at all, only a lower limit",
       (not np.isfinite(a_break)) and all(dm < 0.05 for _, dm in edge if _ >= 5.0),
       f"at y = 10 the whole budget is {float(np.log10(nu(10.0))):.4f} dex and a 0.05 dex mass error returns "
       f"{a_break}; the y with a 0.13 dex budget (the decisive test's own target) is "
       f"{float(np.interp(-0.13, -np.log10(nu(10**np.linspace(-3,2,20001))), 10**np.linspace(-3,2,20001))):.2f}")

    # ------------------------------------------------------------ PART 1: where each survey sits
    P("")
    P("=" * 122)
    P("PART 1 -- where each survey actually sits on that curve, and therefore what it can measure")
    P("=" * 122)
    surveys = {}

    gals = load_sparc()
    sp_re, sp_last = [], []
    for g in gals:
        Re, r = g['Reff'], g['r']
        if Re > 0 and r.min() <= Re <= r.max():
            gb = math.exp(float(np.interp(math.log(Re), np.log(r), np.log(g['gbar']))))
            go = math.exp(float(np.interp(math.log(Re), np.log(r), np.log(g['gobs']))))
            if go > gb > 0: sp_re.append((0.0, gb, go))
        gb, go = g['gbar'][-1], g['gobs'][-1]
        if go > gb > 0: sp_last.append((0.0, gb, go))
    surveys['SPARC at R_e (z~0)'] = sp_re
    surveys['SPARC last point (z~0)'] = sp_last

    rc = []
    for r in csv.DictReader(open(os.path.join(DATA, 'rc100_nestorshachar2023_table3.csv'))):
        f, go, z = fnum(r['fDM_within_Re']), fnum(r['g_Re_ms2']), fnum(r['z'])
        if np.isfinite(f * go * z) and 0 < f < 1: rc.append((z, (1 - f) * go, go))
    surveys['RC100 (z 0.6-2.5)'] = rc

    ms, msg = [], []
    for r in csv.DictReader(open(os.path.join(DATA, 'msa3d_2026_rotation_curves.csv'))):
        z, Re, s0, vr, f = (fnum(r['z']), fnum(r['Re_disk_kpc']), fnum(r['sigma0']),
                            fnum(r['Vrot_Re']), fnum(r['fDM_Re']))
        if not np.isfinite(z * Re * s0 * vr * f) or not (0 < f < 1): continue
        go = (vr**2 + 2.0 * s0**2 * 1.678) * 1e6 / (Re * kpc)
        ms.append((z, (1 - f) * go, go))
        if r['sample'] == 'golden': msg.append((z, (1 - f) * go, go))
    surveys['MSA-3D golden (z 0.6-1.7)'] = msg

    kr = []
    for r in csv.DictReader(open(os.path.join(DATA, 'kross_harrison2017.csv'))):
        z, Ms, V, Re = fnum(r['z']), fnum(r['Mstar']), fnum(r['VC_kms']), fnum(r['Reff_kpc'])
        if not np.isfinite(z * Ms * V * Re) or Ms <= 0 or Re <= 0: continue
        go = (V * 1e3) ** 2 / (Re * kpc)
        gb = G * Ms * Msun / (Re * kpc) ** 2                 # stars only, point mass: an UPPER bound on y is not
        kr.append((z, gb, go))                               # implied -- flagged below, gas is missing
    surveys['KROSS stars-only (z~0.9)'] = kr

    # MUSE-DARK II (Jeanneau+2026): gravitationally lensed, dwarf-dominated, z = 0.5-1.45.  g_bar built
    # INDEPENDENTLY from the catalogue's own M_bar with the exact thin exponential disc at R = 2 R_e = 3.356 R_d
    # (see k03 for the full treatment); this entry exists so that Part 4's gate is not over-claimed.
    from scipy.special import i0 as _i0, i1 as _i1, k0 as _k0, k1 as _k1
    def _eps(rrd):
        yy = rrd / 2.0
        return 4.0 * yy**3 * (_i0(yy) * _k0(yy) - _i1(yy) * _k1(yy))
    def _kpa(zv, Om=0.30, OL=0.70, H0=70.0):
        cc = 299792.458; zs_ = np.linspace(0.0, zv, 4096)
        Dc = cc / H0 * np.trapz(1.0 / np.sqrt(Om * (1 + zs_) ** 3 + OL), zs_)
        return Dc / (1 + zv) * 1e3 * np.pi / (180 * 3600)
    md = []
    _cat = os.path.join(HERE, '..', 'prep_2026', 'jeanneau_refit', 'jeanneau26_catalog_cds.csv')
    _e = float(_eps(2 * 1.678))
    for r in csv.DictReader(open(_cat)):
        zv = fnum(r['zR21']); Re = fnum(r['Reff']) * _kpa(zv); V = 10 ** fnum(r['logV2_0']) * 1e3
        Mb = 10 ** fnum(r['logMBar']) * Msun
        if not np.isfinite(zv * Re * V * Mb) or Re <= 0: continue
        Rm = 2.0 * Re * kpc
        md.append((zv, _e * G * Mb / Rm ** 2, V ** 2 / Rm))
    surveys['MUSE-DARK II lensed (z 0.5-1.45)'] = md

    P(f"    {'survey':30}{'N':>5}{'<z>':>7}{'median y':>11}{'16-84% y':>20}{'LAMBDA(median y)':>19}{'<LAMBDA> per obj':>18}")
    prof = {}
    for k, v in surveys.items():
        if not v: continue
        z = np.array([a[0] for a in v]); gb = np.array([a[1] for a in v]); go = np.array([a[2] for a in v])
        y = gb / A0['canonical']
        lam = LAM(y)
        prof[k] = dict(z=z, gb=gb, go=go, y=y, lam=lam)
        P(f"    {k:30}{len(v):5d}{z.mean():7.2f}{np.median(y):11.3f}"
          f"{f'{np.percentile(y,16):.3f} - {np.percentile(y,84):.3f}':>20}"
          f"{float(LAM(np.median(y))):+19.2f}{np.median(lam):+18.2f}")
    ck("k02-1 THE STRUCTURAL FINDING, and it is against the whole redshift front: the high-redshift surveys sit "
       "one to two decades higher in y than the local rotation curves that calibrate a_0, so their stellar-mass "
       "lever is several times larger.  a_0 is not measured at high z on the same footing as at z = 0",
       abs(np.median(prof['RC100 (z 0.6-2.5)']['lam'])) > 2.0 * abs(np.median(prof['SPARC last point (z~0)']['lam'])),
       f"SPARC last point median y = {np.median(prof['SPARC last point (z~0)']['y']):.3f}, LAMBDA = "
       f"{np.median(prof['SPARC last point (z~0)']['lam']):+.2f};  RC100 median y = "
       f"{np.median(prof['RC100 (z 0.6-2.5)']['y']):.3f}, LAMBDA = {np.median(prof['RC100 (z 0.6-2.5)']['lam']):+.2f};  "
       f"MSA-3D LAMBDA = {np.median(prof['MSA-3D golden (z 0.6-1.7)']['lam']):+.2f}")

    # y versus redshift inside the high-z surveys
    P("")
    hz = np.concatenate([prof['RC100 (z 0.6-2.5)']['z'], prof['MSA-3D golden (z 0.6-1.7)']['z']])
    hy = np.concatenate([prof['RC100 (z 0.6-2.5)']['y'], prof['MSA-3D golden (z 0.6-1.7)']['y']])
    A = np.vstack([hz, np.ones_like(hz)]).T
    sl, ic = np.linalg.lstsq(A, np.log10(hy), rcond=None)[0]
    slope_y, ic_y = sl, ic
    P(f"    d log10 y / dz across the two high-z surveys = {sl:+.3f} per unit z "
      f"(y at z=0.6: {10**(sl*0.6+ic):.2f}; at z=2.5: {10**(sl*2.5+ic):.2f})")
    P(f"    => |LAMBDA| at z=0.6 is {abs(float(LAM(10**(sl*0.6+ic)))):.2f} and at z=2.5 is "
      f"{abs(float(LAM(10**(sl*2.5+ic)))):.2f}: the measurement gets HARDER exactly where the decisive test lives.")

    # ------------------------------------------------------------ PART 2: measured vs predicted lever
    P("")
    P("=" * 122)
    P("PART 2 -- the lever MEASURED on each survey against the lever PREDICTED by LAMBDA (a check that can fail)")
    P("=" * 122)
    P("    PER OBJECT: each galaxy's own a_0 refitted with its g_bar moved +-0.005 dex, against LAMBDA(y_i).")
    P(f"    {'survey':30}{'N invert':>10}{'N lost':>8}{'median pred':>13}{'median meas':>13}{'median |frac diff|':>20}")
    bad = []
    for k, p in prof.items():
        a0i = a0_median_closed(p['gb'], p['go'])
        d = 0.005
        ap = a0_median_closed(p['gb'] * 10 ** d, p['go']); am = a0_median_closed(p['gb'] * 10 ** (-d), p['go'])
        lev = (np.log10(ap) - np.log10(am)) / (2 * d)
        yi = p['gb'] / a0i
        pred = LAM(yi)
        good = np.isfinite(lev) & np.isfinite(pred) & np.isfinite(a0i)
        fr = np.abs(lev[good] - pred[good]) / np.abs(pred[good])
        bad.append(float(np.median(fr)))
        P(f"    {k:30}{good.sum():10d}{int(np.isfinite(a0i).sum()-good.sum()):8d}"
          f"{float(np.median(pred[good])):+13.2f}{float(np.median(lev[good])):+13.2f}{float(np.median(fr)):20.2e}")
    ck("k02-2 the predicted lever is confronted with the measured one GALAXY BY GALAXY and matches to a fraction "
       "of a percent in every survey -- the amplification is a property of the kernel, not a story",
       max(bad) < 0.02, f"largest median fractional discrepancy across the five samples {max(bad):.2e}")
    P("    (the SAMPLE-median lever differs from the per-object one because objects near y ~ 5 drop out of the")
    P("     inversion when g_bar is raised -- the k02-0b breakdown showing up inside real data.)")

    # ------------------------------------------------------------ PART 3: the diagnosis of item 101's gap
    P("")
    P("=" * 122)
    P("PART 3 -- the diagnosis: what stellar-mass offset does the measured survey-to-survey a_0 gap correspond to?")
    P("=" * 122)
    a0_rc = float(np.nanmedian(a0_median_closed(prof['RC100 (z 0.6-2.5)']['gb'], prof['RC100 (z 0.6-2.5)']['go'])))
    a0_ms = float(np.nanmedian(a0_median_closed(prof['MSA-3D golden (z 0.6-1.7)']['gb'],
                                                prof['MSA-3D golden (z 0.6-1.7)']['go'])))
    a0_sp = float(np.nanmedian(a0_median_closed(prof['SPARC at R_e (z~0)']['gb'], prof['SPARC at R_e (z~0)']['go'])))
    gap = math.log10(a0_ms / a0_rc)
    P(f"    median a_0: SPARC(R_e) {a0_sp:.3e}   RC100 {a0_rc:.3e}   MSA-3D {a0_ms:.3e}")
    P(f"    MSA-3D minus RC100 = {gap:+.3f} dex  (item 101 measured +0.404 dex on the same closed form)")
    # solve, on the REAL g_bar and g_obs, for the symmetric relative baryonic-mass offset that closes the gap
    def gap_of(delta):
        aR = float(np.nanmedian(a0_median_closed(prof['RC100 (z 0.6-2.5)']['gb'] * 10 ** (-delta / 2),
                                                 prof['RC100 (z 0.6-2.5)']['go'])))
        aM = float(np.nanmedian(a0_median_closed(prof['MSA-3D golden (z 0.6-1.7)']['gb'] * 10 ** (+delta / 2),
                                                 prof['MSA-3D golden (z 0.6-1.7)']['go'])))
        return math.log10(aM / aR)
    # solve for the offset that makes the two surveys AGREE: gap_of(delta) = 0.  gap_of is decreasing in delta.
    lo, hi = -1.5, 1.5
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if gap_of(mid) > 0: lo = mid
        else: hi = mid
    dM_needed = 0.5 * (lo + hi)
    lamR = float(np.median(LAM(prof['RC100 (z 0.6-2.5)']['gb'] / a0_rc)))
    lamM = float(np.median(LAM(prof['MSA-3D golden (z 0.6-1.7)']['gb'] / a0_ms)))
    P(f"    the two surveys' SELF-CONSISTENT levers (LAMBDA at each survey's own fitted a_0): RC100 {lamR:+.2f}, "
      f"MSA-3D {lamM:+.2f}")
    P(f"    solved on the real data: raising MSA-3D's baryonic masses by {dM_needed/2:+.3f} dex and lowering "
      f"RC100's by the same amount ({dM_needed:+.3f} dex relative) makes the two surveys' a_0 AGREE EXACTLY "
      f"(residual {gap_of(dM_needed):+.4f} dex)")
    P(f"    at SPARC's own LAMBDA = {float(np.median(prof['SPARC last point (z~0)']['lam'])):+.2f} the same "
      f"{abs(dM_needed):.3f} dex mass difference would produce only "
      f"{abs(dM_needed*float(np.median(prof['SPARC last point (z~0)']['lam']))):.3f} dex of a_0.")
    ck("k02-3 THE DIAGNOSIS, and it is quantitative: the 0.4 dex survey-to-survey a_0 gap that item 101 could only "
       "report is what a baryonic-mass calibration difference of about 0.1 dex each way -- ordinary between two "
       "SED pipelines with different IMF, SFH and gas treatments -- produces once the high-z amplification is "
       "applied.  Nothing about a_0 is required, and this check fails if the required offset is implausible",
       abs(dM_needed) < 0.35,
       f"required relative offset {dM_needed:+.3f} dex ({dM_needed/2:+.3f} each way), against a typical "
       f"SED-code-to-SED-code systematic of 0.1-0.3 dex; verified by solving on the real g_bar and g_obs")

    # ------------------------------------------------------------ PART 4: the deep-MOND gate
    P("")
    P("=" * 122)
    P("PART 4 -- the gate the law implies: keep only points with |LAMBDA| <= 1.5, and see whether the surveys agree")
    P("=" * 122)
    ygate = float(10 ** np.interp(-1.5, LAM(10 ** np.linspace(-4, 2, 20001))[::-1], np.linspace(-4, 2, 20001)[::-1]))
    ys = 10 ** np.linspace(-4, 2, 200001)
    ygate = float(ys[np.argmin(np.abs(LAM(ys) + 1.5))])
    P(f"    |LAMBDA| <= 1.5  <=>  y <= {ygate:.3f}  <=>  g_bar <= {ygate*A0['canonical']:.3e} (canonical) / "
      f"{ygate*A0['alt']:.3e} (alt) m/s^2")
    P(f"    {'survey':30}{'N total':>9}{'N gated':>9}{'frac':>8}{'median a0 (gated)':>20}{'dex vs canon':>14}")
    gated = {}
    for k, p in prof.items():
        g = p['y'] <= ygate
        a0g = float(np.nanmedian(a0_median_closed(p['gb'][g], p['go'][g]))) if g.sum() >= 3 else np.nan
        gated[k] = (int(g.sum()), a0g)
        P(f"    {k:30}{len(p['y']):9d}{g.sum():9d}{g.mean():8.2f}"
          f"{(f'{a0g:.3e}' if np.isfinite(a0g) else '--'):>20}"
          f"{(f'{math.log10(a0g/A0["canonical"]):+.3f}' if np.isfinite(a0g) else '--'):>14}")
    nrc, nms = gated['RC100 (z 0.6-2.5)'][0], gated['MSA-3D golden (z 0.6-1.7)'][0]
    nmd = gated['MUSE-DARK II lensed (z 0.5-1.45)'][0]
    ck("k02-4 THE GATE SPLITS THE HIGH-REDSHIFT ARCHIVE IN TWO, and that is the finding: not one of the 123 "
       "galaxies in the two resolved-kinematics surveys is observed at an acceleration where a_0 can be read "
       "with a lever near -1, while the LENSED dwarf sample passes in bulk.  The redshift axis is not "
       "systematics-limited by accident; the massive-disc surveys are observed in the wrong regime, and lensed "
       "low-mass galaxies are the class that is not",
       nrc + nms == 0 and nmd > 10,
       f"RC100 {nrc}/{len(prof['RC100 (z 0.6-2.5)']['y'])} and MSA-3D {nms}/{len(prof['MSA-3D golden (z 0.6-1.7)']['y'])} "
       f"pass y <= {ygate:.3f}, against MUSE-DARK II {nmd}/{len(prof['MUSE-DARK II lensed (z 0.5-1.45)']['y'])} and "
       f"SPARC's last points {gated['SPARC last point (z~0)'][0]}/{len(prof['SPARC last point (z~0)']['y'])}")

    # ------------------------------------------------------------ PART 5: joint a0(z) with per-survey levels
    P("")
    P("=" * 122)
    P("PART 5 -- the joint a0(z) done correctly: a free level per survey, so only WITHIN-survey redshift counts")
    P("=" * 122)
    labs = ['RC100 (z 0.6-2.5)', 'MSA-3D golden (z 0.6-1.7)']
    zz = np.concatenate([prof[l]['z'] for l in labs])
    aa = np.concatenate([a0_median_closed(prof[l]['gb'], prof[l]['go']) for l in labs])
    idx = np.concatenate([np.full(len(prof[l]['z']), i) for i, l in enumerate(labs)])
    ok = np.isfinite(aa) & (aa > 0)
    zz, la, idx = zz[ok], np.log10(aa[ok]), idx[ok]
    # design matrix: one intercept per survey + one common slope
    X = np.zeros((len(zz), len(labs) + 1))
    for i in range(len(labs)): X[:, i] = (idx == i)
    X[:, -1] = zz
    beta, *_ = np.linalg.lstsq(X, la, rcond=None)
    res = la - X @ beta
    s2 = res @ res / (len(zz) - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    sl, sle = beta[-1], math.sqrt(cov[-1, -1])
    # naive stacked slope (no per-survey level) for contrast
    Xn = np.vstack([np.ones_like(zz), zz]).T
    bn, *_ = np.linalg.lstsq(Xn, la, rcond=None)
    rn = la - Xn @ bn; s2n = rn @ rn / (len(zz) - 2)
    cn = s2n * np.linalg.inv(Xn.T @ Xn); sln, slne = bn[1], math.sqrt(cn[1, 1])
    P(f"    N = {len(zz)} high-z galaxies, {len(labs)} surveys, one free level each")
    for i, l in enumerate(labs):
        P(f"       level({l:28}) = {beta[i]:+8.3f}  ->  a_0 = {10**(beta[i]):.3e} at z = 0")
    P(f"    common d log a_0/dz  (per-survey levels free) = {sl:+.4f} +- {sle:.4f}")
    P(f"    naive stacked slope  (one level for all)      = {sln:+.4f} +- {slne:.4f}   <- what item 101's M1 showed is the survey ladder")
    P(f"    item 16's RC100-only slope (committed)        = -0.112 +- 0.063")
    for nm, pr in (("FRAMEWORK, a_0 constant", 0.0), ("LambdaCDM-native rise", +0.131), ("MUSE-DARK III", +0.295)):
        P(f"       {nm:28} predicts {pr:+.3f} dex/z  ->  {(sl-pr)/sle:+6.2f} sigma")
    # bootstrap and z-shuffle
    rng2 = np.random.default_rng(20260903)
    bs = []
    for _ in range(2000):
        j = rng2.integers(0, len(zz), len(zz))
        b, *_ = np.linalg.lstsq(X[j], la[j], rcond=None); bs.append(b[-1])
    bs = np.array(bs)
    sh = []
    for _ in range(2000):
        lz = zz.copy()
        for i in range(len(labs)):
            k_ = idx == i; v = lz[k_]; rng2.shuffle(v); lz[k_] = v
        Xs = X.copy(); Xs[:, -1] = lz
        b, *_ = np.linalg.lstsq(Xs, la, rcond=None); sh.append(b[-1])
    sh = np.array(sh)
    P(f"    bootstrap on the same fit: {bs.mean():+.4f} +- {bs.std():.4f} dex/z (2000 resamples)")
    P(f"    WITHIN-survey z-shuffle:   {sh.mean():+.4f} +- {sh.std():.4f} dex/z -- the mutation, and it fires")
    fdm_rc = 1 - prof['RC100 (z 0.6-2.5)']['gb'] / prof['RC100 (z 0.6-2.5)']['go']
    a_rc = a0_median_closed(prof['RC100 (z 0.6-2.5)']['gb'], prof['RC100 (z 0.6-2.5)']['go'])
    rr = np.corrcoef(np.log10(a_rc), fdm_rc)[0, 1]
    P(f"    THE CAVEAT that sizes it, carried from item 16c: inside RC100 corr(log a_0, f_DM) = {rr:+.3f}, so this "
      f"slope is")
    P("    a monotone restatement of that survey's own falling dark-matter fractions and inherits their systematics.")
    ck("M5 the z-shuffle mutation fires: permuting redshift WITHIN each survey destroys the slope, so what is "
       "measured is a redshift trend inside the surveys and not the two surveys' different levels",
       abs(sh.mean()) < 0.3 * abs(sl) or abs(sh.mean()) < 0.02,
       f"real {sl:+.4f}, shuffled {sh.mean():+.4f} +- {sh.std():.4f}")
    ck("k02-5 the joint high-z slope done with a free level per survey (the only defensible combination once the "
       "levels disagree by 0.4 dex) is consistent with a CONSTANT a_0 and does not separate the rivals; it is "
       "reported beside the naive stacked slope, which is the survey ladder read as a line",
       abs(sl) < 2 * sle,
       f"per-survey-level slope {sl:+.4f} +- {sle:.4f} dex/z ({abs(sl/sle):.2f}s from flat); naive stacked "
       f"{sln:+.4f} +- {slne:.4f}")

    # ------------------------------------------------------------ PART 6: what z ~ 2.5 needs
    P("")
    P("=" * 122)
    P("PART 6 -- the design rule the law gives for the decisive z ~ 2.5 measurement")
    P("=" * 122)
    P("    Target: a_0 at z ~ 2.5 to +-0.13 dex (framework 0.00 against a LambdaCDM-native +0.33).")
    P(f"    {'stellar-mass systematic':28}{'|LAMBDA| allowed':>18}{'y required':>14}{'R/R_e required*':>18}")
    yre = float(np.median(prof['RC100 (z 0.6-2.5)']['y']))
    for dM in (0.02, 0.05, 0.10, 0.13, 0.15, 0.20, 0.30):
        need = 0.13 / dM
        if need <= 1.0:
            P(f"    {dM:>10.2f} dex{'':14}{need:>18.2f}{'IMPOSSIBLE':>14}{'--':>18}")
            continue
        yv = ys[np.argmin(np.abs(np.abs(LAM(ys)) - need))]
        rr = math.sqrt(yre / yv)
        P(f"    {dM:>10.2f} dex{'':14}{need:>18.2f}{yv:>14.4f}{rr:>18.2f}")
    P("")
    P("    A HARD FLOOR falls out of the same law and it is worth stating on its own: |LAMBDA(y)| >= 1 for every y,")
    P("    with equality only in the deep-MOND limit.  So a_0 can NEVER be measured to better precision than the")
    P("    baryonic mass scale it is read against -- at any acceleration, in any survey, at any redshift.")
    ck("k02-6 the hard floor, proved numerically over five decades in y: |LAMBDA| >= 1 everywhere, so no a_0 "
       "measurement can beat its own baryonic-mass calibration.  The decisive +-0.13 dex test therefore REQUIRES "
       "the baryonic mass at z ~ 2.5 to better than 0.13 dex, whatever else is done",
       float(np.min(np.abs(LAM(ys)))) >= 0.9999,
       f"min |LAMBDA| over y = 1e-3 to 100 is {float(np.min(np.abs(LAM(ys)))):.6f}, attained at y = "
       f"{float(ys[np.argmin(np.abs(LAM(ys)))]):.2e}")
    P("    *R/R_e for a point-mass baryon field, using RC100's own median y(R_e); a real disc needs a little more.")
    P("    Read plainly: with a 0.15 dex stellar-mass systematic the decisive test needs the rotation curve measured")
    P("    at roughly 3-5 effective radii, not at one -- which is exactly the regime no z ~ 2.5 survey reaches today.")

    # ------------------------------------------------------------ PART 7: mutations
    P("")
    P("=" * 122)
    P("PART 7 -- mutation controls")
    P("=" * 122)
    # M1: synthesise both surveys from ONE a0 with a per-survey mass offset; must reproduce the observed gap
    # M1: the TRUE world is "both surveys share one a_0, and their catalogued masses are wrong by -/+ delta/2".
    # Build g_obs from the CORRECTED g_bar at the common a_0, then read a_0 back off the CATALOGUED g_bar.
    a0_common = float(np.nanmedian(a0_median_closed(prof[labs[0]]['gb'] * 10 ** (-dM_needed / 2), prof[labs[0]]['go'])))
    P(f"    (the common a_0 the two surveys share once corrected: {a0_common:.3e} = "
      f"{math.log10(a0_common/A0['canonical']):+.2f} dex from canonical, {math.log10(a0_common/A0['alt']):+.2f} from alt)")
    def syn_gap(delta):
        out = []
        for l, d in ((labs[0], -delta / 2), (labs[1], +delta / 2)):
            gbt = prof[l]['gb'] * 10 ** d                   # the TRUE baryonic acceleration
            go = gbt * nu(gbt / a0_common)                  # obeys ONE a0 exactly
            out.append(float(np.nanmedian(a0_median_closed(prof[l]['gb'], go))))   # read with the CATALOGUED g_bar
        return math.log10(out[1] / out[0])
    gap_syn = syn_gap(dM_needed)
    ck("M1 the mechanism, injected and recovered: two synthetic surveys built to obey ONE a_0 exactly at their own "
       "real g_bar values, differing only by the solved baryonic-mass offset, reproduce the observed level gap to "
       "within 15% -- so the gap needs no a_0 physics",
       abs(gap_syn - gap) < 0.15 * abs(gap),
       f"a relative mass error of {dM_needed:+.3f} dex on synthetic one-a_0 data reproduces {gap_syn:+.3f} dex "
       f"against the observed {gap:+.3f} dex")
    ck("M2 closure: with NO offset the same two synthetic surveys agree exactly, so the gap in M1 is the offset "
       "and not the different y-distributions of the two samples",
       abs(syn_gap(0.0)) < 0.02, f"no-offset synthetic gap {syn_gap(0.0):+.4f} dex")
    # M3: wrong a0 in the gate
    for foot in ('canonical', 'alt'):
        yg = prof['RC100 (z 0.6-2.5)']['gb'] / A0[foot]
        P(f"    footing {foot:10s}: RC100 median y = {np.median(yg):.3f}, median LAMBDA = {np.median(LAM(yg)):+.2f}")
    ck("M3 both footings: the conclusion is footing-independent -- the high-z samples sit at y ~ 1-2 on either "
       "footing and the amplification is 3-4 either way",
       abs(np.median(LAM(prof['RC100 (z 0.6-2.5)']['gb'] / A0['alt']))) > 2.0,
       f"canonical LAMBDA {np.median(LAM(prof['RC100 (z 0.6-2.5)']['gb']/A0['canonical'])):+.2f}, "
       f"alt {np.median(LAM(prof['RC100 (z 0.6-2.5)']['gb']/A0['alt'])):+.2f}")
    # M4: the simple nu must give the same qualitative law
    def nu_simple(y): return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)))
    def m_simple(y):
        h = 1e-5; return (np.log(nu_simple(y * (1 + h))) - np.log(nu_simple(y))) / np.log(1 + h)
    ls = (1 + m_simple(2.0)) / m_simple(2.0)
    ck("M4 kernel swap AGAINST INTEREST: the amplification is not special to Route A -- the 'simple' interpolation "
       "function gives the same law with a similar value at y = 2, so this is a property of ANY interpolating "
       "kernel measured out of the deep regime and cannot be escaped by changing nu",
       abs(ls) > 1.5, f"Route A LAMBDA(2) = {float(LAM(2.0)):+.2f}; simple-nu LAMBDA(2) = {float(ls):+.2f}")

    # ------------------------------------------------------------ PART 8: LambdaCDM beside the framework
    P("")
    P("=" * 122)
    P("PART 8 -- the LambdaCDM alternative computed beside the framework")
    P("=" * 122)
    info("LambdaCDM reads the same numbers as f_DM(<R_e), not as a_0.  The amplification is then absent by "
         "construction: f_DM is linear in g_bar, so d f_DM/d ln Upsilon = -(1-f_DM), a lever of order 0.3-0.7,")
    info("not 3-5.  That asymmetry is real and it is against the framework: the SAME data support a much more "
         "stable statement in LambdaCDM's variable than in the framework's.  The framework's compensation is that")
    info("its variable is supposed to be a CONSTANT, so its scatter is a test and f_DM's is not.")
    fdm = 1 - prof['RC100 (z 0.6-2.5)']['gb'] / prof['RC100 (z 0.6-2.5)']['go']
    lev_f = -(1 - fdm)
    P(f"    RC100: d f_DM/d ln Upsilon has median {np.median(lev_f):+.3f} against the framework's d ln a_0/d ln Upsilon "
      f"= {np.median(prof['RC100 (z 0.6-2.5)']['lam']):+.2f}")
    P(f"    sd(log a_0) inside RC100 = {np.std(np.log10(a0_median_closed(prof['RC100 (z 0.6-2.5)']['gb'], prof['RC100 (z 0.6-2.5)']['go']))):.3f} dex; "
      f"sd(f_DM) = {np.std(fdm):.3f}")

    P("")
    P("=" * 122)
    P("VERDICT (k02)")
    P("=" * 122)
    P("  LAMBDA(y) = (1 + m)/m is exact, verified numerically, and confronted survey by survey.  It says:")
    P(f"   * SPARC's outer points sit at y = {np.median(prof['SPARC last point (z~0)']['y']):.3f}, LAMBDA = "
      f"{np.median(prof['SPARC last point (z~0)']['lam']):+.2f};  RC100 at R_e sits at y = "
      f"{np.median(prof['RC100 (z 0.6-2.5)']['y']):.2f}, LAMBDA = {np.median(prof['RC100 (z 0.6-2.5)']['lam']):+.2f}.")
    P(f"   * the 0.4 dex RC100-vs-MSA-3D gap is what a {dM_needed:+.2f} dex baryonic-mass difference produces.  It is")
    P("     not evidence about a_0 and must never be quoted as such.")
    P(f"   * y RISES with redshift at d log10 y/dz = {slope_y:+.3f}, so |LAMBDA| runs from {abs(float(LAM(10**(slope_y*0.6+ic_y)))):.1f} at z = 0.6")
    P(f"     to {abs(float(LAM(10**(slope_y*2.5+ic_y)))):.1f} at z = 2.5: the amplification is worst exactly where the decisive test lives.")
    P("  This is a THEOREM ABOUT MEASUREMENT derived from the RAR, not an independent second law.  Its product is")
    P("  the design rule in Part 6 and the retirement of every existing high-z a_0 'level' as a measurement.")
    P("=" * 122)
    return ck.done()

if __name__ == '__main__':
    sys.exit(main())
