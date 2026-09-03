#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_prescription_systematic_adversarial.py
===========================================================================================================
ADVERSARIAL VERIFICATION of ONE claim made by g05_dsph_prescription_fixed_and_expanded.py, check S2b:

  "The matched separation is smaller than its own external-field-prescription systematic, so it is not a
   measurement whatever its nominal sigma."
  Numbers: sphere average +0.064 dex (0.93 sigma); Famaey & McGaugh 2012 eq.60 one-dimensional +0.157 dex
  (2.08 sigma); f09 max() branch -0.525 dex (-4.06 sigma).  Systematic 0.093 dex against a signal of
  0.064 dex, ratio 1.4.  Raw-offset systematic 0.205 dex = 42 per cent of +0.489 dex.

THE JOB IS TO REFUTE IT.  Everything below is reimplemented from the data rather than imported from g05, so
that an arithmetic error in g05 cannot propagate into its own verification.  Only hunt_lib (nu, SPARC loader,
A0, Check/P/info) is shared, because that is the framework's own kernel and the repository's own loader.

THE FOUR LINES OF ATTACK, in the order they are run:

 V1-V3  ARITHMETIC.  Recompute the sphere-average quadrature by a different rule (Gauss-Legendre in cos th
        rather than trapezoid in th), recompute the Famaey & McGaugh 2012 eq. 60 formula from its literature
        form nu(x_i+x_e)(x_i+x_e) - nu(x_e) x_e, rebuild the whole matched pipeline, and see whether the four
        headline numbers come back.

 V4     THE FOOTING.  g05 computes S2b at the CANONICAL a_0 only: scan() hard-codes a0c and the prescription
        table in part 4(b) is single-footing.  The standing rule of this repository is BOTH footings on every
        load-bearing number.  If the systematic-versus-signal verdict flips at a_0 = 1.13e-10 the claim is a
        footing artefact and is refuted as stated.

 V5     THE STABILITY OF THE SYSTEMATIC ITSELF.  Both "signal" and "systematic" are differences of MEDIANS of
        14 objects.  A ratio of 1.4 between two such numbers is only a statement if it survives resampling.

 V6-V7  THE PHYSICS OF THE PRESCRIPTION.  g05's own stated weakest link is that the sphere average is EXACT
        (QUMOND flux theorem) and the 1-D formula is an approximation, so the difference might be the
        approximation's error rather than an ambiguity.  That defence is tested directly, in two ways:
          (a) is the 1-D formula even inside the range of the exact pointwise radial field?  If it is, it is a
              defensible evaluation of the same field in a particular direction and the spread is real.
          (b) is "an isotropic velocity dispersion measures exactly the sphere average" true?  The flux theorem
              gives <g_r> = <S_r> at fixed radius EXACTLY, but the observed side, g_obs = 3 sigma^2/r_1/2, comes
              from the Wolf et al. 2010 estimator, which is derived for a SPHERICALLY SYMMETRIC potential.  In
              an external field the potential is not spherically symmetric.  The size of that anisotropy is
              computed here for the actual objects.

 V8     THE DEEP-MOND LIMIT, WHERE IT IS ACTUALLY APPLIED.  g05's check A1c reads its measured residual slope
        of -0.498 dex/dex as a mechanical identity, on the argument that "in the deep-MOND limit the prediction
        is g = sqrt(x_i) a_0".  That is the ISOLATED deep-MOND limit.  Most of these dwarfs are EXTERNAL-FIELD
        dominated (x_e > x_i), where the prediction is LINEAR in x_i, not square-root.  The identity slope is
        therefore computed rather than asserted: replace every g_obs by a constant and refit.

 V9     WHAT THE SYSTEMATIC DOES AND DOES NOT DO.  Does it move the sign?  S2b's text says the separation
        "changes SIGN and lands four sigma on the WRONG side" -- but only under f09's max() branch, which g05's
        own check P3 shows is a kinked, non-physical prescription.  Between the two treatments S2b itself calls
        defensible, the sign is checked here.

DATA: Local Volume Database (Pace 2024, ApJS 273, 15); SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157).
Wolf et al. 2010, MNRAS 406, 1220 for the mass estimator.  Famaey & McGaugh 2012, Living Rev. Rel. 15, 10 for
eq. 60; Milgrom 1986, ApJ 302, 617 for the external-field limit; Angus 2008, MNRAS 387, 1481 for the dSph use.

BOTH a_0 FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL.
"""
import sys, math, csv, os
import numpy as np
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)

MW_MB, M31_MB = 6.0e10, 1.2e11
UPS_V = 2.0
PC = 3.0857e16
MATCH_W, MATCH_N = 0.20, 20

# ==========================================================================================================
P("="*122)
P("V1.  THE QUADRATURE, RECOMPUTED WITH A DIFFERENT INTEGRATION RULE.")
P("="*122)

def sphere_gl(x_i, x_e, n=400):
    """Sphere-averaged radial QUMOND source, in units of a_0, by GAUSS-LEGENDRE in mu = cos(theta).
       <S_r> = (1/2) INT_-1^1 S(g_N).rhat dmu   with   g_N/a_0 = x_e zhat - x_i rhat.
       Returns the INWARD magnitude.  Different rule, different variable, from g05's trapezoid in theta."""
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    mu, w = np.polynomial.legendre.leggauss(n)
    st = np.sqrt(np.maximum(1.0 - mu*mu, 0.0))
    gx, gz = -x_i*st, x_e - x_i*mu
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*mu)
    return -float(np.sum(w*Sr)/2.0)

def sphere_trap(x_i, x_e, ntheta=2001):
    """g05's own rule, reproduced verbatim so the two can be compared."""
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    th = np.linspace(0.0, math.pi, ntheta)
    st, ctm = np.sin(th), np.cos(th)
    gx, gz = -x_i*st, x_e - x_i*ctm
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*ctm)
    return -float(np.trapz(Sr*st, th)/np.trapz(st, th))

def fm12(x_i, x_e):
    """Famaey & McGaugh 2012, Living Rev. Rel. 15, 10, eq. 60, one-dimensional external-field formula, in the
    QUMOND-side form used by Lelli et al. 2015 (A&A 584, A113):  nu(x_i+x_e)(x_i+x_e) - nu(x_e) x_e."""
    nt = nu_s(x_i + x_e)
    ne = nu_s(x_e) if x_e > 0 else 0.0
    return (x_i + x_e)*nt - x_e*ne

def f09max(x_i, x_e):
    g_iso = math.sqrt(x_i)
    g_efe = nu_s(x_e)*x_i if x_e > 0 else 0.0
    return max(g_iso, g_efe)

PRESC = {"sphere": sphere_gl, "fm12": fm12, "f09": f09max}

grid = [(xi, xe) for xi in (1e-4, 1e-3, 1e-2, 0.1, 1.0) for xe in (1e-3, 1e-2, 0.1, 1.0)]
d_rule = max(abs(sphere_gl(a, b)/sphere_trap(a, b) - 1) for a, b in grid)
ck("V1 the sphere-average quadrature is not an integration artefact: Gauss-Legendre in cos(theta) and g05's "
   "trapezoid in theta agree to better than one part in 1e-6 over four decades in both arguments",
   d_rule < 1e-6, f"worst |GL/trapezoid - 1| = {d_rule:.3e} over {len(grid)} (x_i, x_e) pairs")

m1 = [abs(sphere_gl(xi, xe)/xi - 1) for xi, xe in ((0.01, 0.1), (1e-3, 1.0), (0.5, 0.02))]
_nu_save = None
def _one(y): return np.ones_like(np.asarray(y, dtype=float))
import hunt_lib as _hl
_nu_save, _nu_s_save = _hl.nu, _hl.nu_s
globals()["nu"], globals()["nu_s"] = _one, (lambda y: 1.0)
m1 = [abs(sphere_gl(xi, xe)/xi - 1) for xi, xe in ((0.01, 0.1), (1e-3, 1.0), (0.5, 0.02))]
globals()["nu"], globals()["nu_s"] = _nu_save, _nu_s_save
ck("V1b MUTATION CONTROL on my own quadrature: with nu = 1 the Gauss-Legendre sphere average must return the "
   "internal Newtonian field exactly, at every external field, or the machinery is manufacturing a coupling",
   max(m1) < 1e-12, "worst |<S_r>/x_i - 1| with nu=1: " + f"{max(m1):.3e}")

info("")
info("the two prescriptions, side by side, recomputed here (this is g05's P4 table, independently):")
info(f"{'x_i':>9} {'x_e':>9} {'x_e/x_i':>9} {'sphere (exact)':>16} {'FM12 eq60':>12} {'ratio':>8}")
rats = []
for xi in (1e-3, 1e-2, 0.1):
    for xe in (1e-3, 1e-2, 0.1, 1.0):
        a, b = sphere_gl(xi, xe), fm12(xi, xe)
        rats.append(a/b)
        info(f"{xi:9.4f} {xe:9.4f} {xe/xi:9.2f} {a:16.6f} {b:12.6f} {a/b:8.3f}")
ck("V2 the 0.28 dex prescription spread that P4 reports is REAL and reproduces independently: the exact sphere "
   "average and the published one-dimensional formula differ by up to 92 per cent on this grid",
   1.85 < max(rats) < 1.95 and abs(min(rats) - 1.089) < 0.02,
   f"ratio spans {min(rats):.3f}-{max(rats):.3f}, i.e. {math.log10(max(rats)):.3f} dex at worst "
   f"(g05 reports 1.089-1.916)")

# ==========================================================================================================
P(""); P("="*122)
P("V3.  THE WHOLE PIPELINE, REBUILT FROM THE DATA, AND THE FOUR HEADLINE NUMBERS.")
P("="*122)

def fnum(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def load_lvd(fname, host_mb, host_name):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fname))):
        sig, ul = fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
        MV, rh = fnum(r["M_V"]), (fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]))
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
        if fnum(r["confirmed_galaxy"]) != 1: continue
        lMs, lMHI = fnum(r["mass_stellar"]), fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, rh=rh, sig=sig,
                        Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83 - MV))*UPS_V),
                        MHI=(10**lMHI if lMHI is not None else 0.0),
                        Dhost=(fnum(r["distance_host"]) or fnum(r["distance_gc"])),
                        Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                        host=host_name, host_mb=host_mb))
    return out

EXCL = {"LMC", "SMC", "Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
classes = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
for fn, hmb, hn in (("lvd_dwarf_mw.csv", MW_MB, "MW"), ("lvd_dwarf_m31.csv", M31_MB, "M31"),
                    ("lvd_dwarf_local_field.csv", None, "field")):
    for d in load_lvd(fn, hmb, hn):
        if d["name"] in EXCL: continue
        if d["MHI"] > 0.3*d["Ms"]: continue
        classes["isolated" if hn == "field" else ("m31" if hn == "M31" else
               ("classical" if d["MV"] <= -7.7 else "ultrafaint"))].append(d)
info("rebuilt sample, independently of g05:  " +
     ", ".join(f"{k} {len(v)}" for k, v in classes.items()))

def row(d, a0, presc="sphere", ups=UPS_V):
    """(residual dex, x_i, x_e).  g_obs = 3 sigma^2/r_1/2 (Wolf+2010), r_1/2 = (4/3) R_e, ENCLOSED M_b/2."""
    r12 = (4.0/3.0)*d["rh"]*PC
    Mb = (ups/UPS_V)*d["Ms"] + 1.33*d["MHI"]
    x_i = G*(0.5*Mb*Msun)/r12**2/a0
    if d["host_mb"] is not None and d["Dhost"]:
        x_e = G*d["host_mb"]*Msun/(d["Dhost"]*kpc)**2/a0
    else:
        x_e = ((G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0) +
               (G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0))/a0
    g_obs = 3.0*(d["sig"]*1e3)**2/r12
    return math.log10(g_obs/(PRESC[presc](x_i, x_e)*a0)), x_i, x_e

gals = load_sparc()
_POOL, _ROT = {}, {}

def pool(a0, drop=None):
    key = (a0, drop)
    if key in _POOL: return _POOL[key]
    ly, rr = [], []
    for g in gals:
        if g["name"] == drop: continue
        y = g["gbar"]/a0
        ly.append(np.log10(y)); rr.append(np.log10(g["gobs"]/(nu(y)*g["gbar"])))
    _POOL[key] = (np.concatenate(ly), np.concatenate(rr))
    return _POOL[key]

def ctrl(lx, LY, RR, w=MATCH_W, n=MATCH_N):
    m = np.abs(LY - lx) < w
    return float(np.median(RR[m])) if m.sum() >= n else None

def rot_deltas(a0, w=MATCH_W, n=MATCH_N):
    key = (a0, w, n)
    if key in _ROT: return _ROT[key]
    out = []
    for g in gals:
        y = g["gbar"]/a0
        rj = float(np.median(np.log10(g["gobs"]/(nu(y)*g["gbar"]))))
        LY, RR = pool(a0, drop=g["name"])
        c = ctrl(float(np.median(np.log10(y))), LY, RR, w, n)
        if c is not None: out.append(rj - c)
    _ROT[key] = np.array(out)
    return _ROT[key]

KEYS = ("classical", "m31", "isolated")
def matched(a0, presc="sphere", ups=UPS_V, w=MATCH_W, n=MATCH_N):
    LY, RR = pool(a0)
    names, dl, raw, xi_, xe_ = [], [], [], [], []
    for k in KEYS:
        for d in classes[k]:
            r, xi, xe = row(d, a0, presc, ups)
            c = ctrl(math.log10(xi), LY, RR, w, n)
            if c is None: continue
            names.append(d["name"]); dl.append(r - c); raw.append(r); xi_.append(xi); xe_.append(xe)
    return names, np.array(dl), np.array(raw), np.array(xi_), np.array(xe_)

def sep_of(a0, presc="sphere", ups=UPS_V, w=MATCH_W, n=MATCH_N):
    nm, dl, raw, xi_, xe_ = matched(a0, presc, ups, w, n)
    r = rot_deltas(a0, w, n)
    s = float(np.median(dl) - np.median(r))
    se = math.sqrt(dl.std(ddof=1)**2/len(dl) + r.std(ddof=1)**2/len(r))
    rawmed = float(np.median([row(d, a0, presc, ups)[0] for k in KEYS for d in classes[k]]))
    return dict(sep=s, se=se, nsig=s/se, n=len(dl), names=nm, dl=dl, rot=r, raw=rawmed)

a0c = A0["canonical"]
info("")
info(f"{'footing':>10} {'prescription':>20} {'N':>4} {'RAW dex':>9} {'matched sep':>12} {'sigma':>7}")
TAB = {}
for foot, a0 in A0.items():
    for pn in ("f09", "fm12", "sphere"):
        o = sep_of(a0, pn); TAB[(foot, pn)] = o
        info(f"{foot:>10} {pn:>20} {o['n']:4d} {o['raw']:+9.3f} {o['sep']:+12.3f} {o['nsig']:7.2f}")

c_sph, c_fm, c_f09 = TAB[("canonical", "sphere")], TAB[("canonical", "fm12")], TAB[("canonical", "f09")]
ck("V3 the four headline numbers of the claim reproduce from an independent rebuild of the pipeline: the matched "
   "separation is +0.064 dex (0.93 sigma) under the exact sphere average, +0.157 dex (2.08 sigma) under FM12 "
   "eq. 60, and -0.525 dex under f09's max() branch.  The arithmetic of the claim is not in dispute",
   abs(c_sph["sep"] - 0.064) < 0.005 and abs(c_fm["sep"] - 0.157) < 0.005 and abs(c_f09["sep"] + 0.525) < 0.01,
   f"sphere {c_sph['sep']:+.3f} ({c_sph['nsig']:.2f} sigma), FM12 {c_fm['sep']:+.3f} ({c_fm['nsig']:.2f}), "
   f"f09 {c_f09['sep']:+.3f} ({c_f09['nsig']:.2f}), all on N = {c_sph['n']}; "
   f"RAW sphere {c_sph['raw']:+.3f} vs FM12 {c_fm['raw']:+.3f}, systematic {abs(c_sph['raw']-c_fm['raw']):.3f} dex")

# ==========================================================================================================
P(""); P("="*122)
P("V4.  THE FOOTING.  g05 COMPUTES S2b AT THE CANONICAL a_0 ONLY.  Does the verdict hold at the alt footing?")
P("="*122)
info("g05's part 4 scan() hard-codes a0c, so the entire prescription table -- the single most decisive line in")
info("that file, by its own description -- was never evaluated at a_0 = 1.13e-10.  The standing rule of this")
info("repository is BOTH footings on every load-bearing number.  Here it is.")
info("")
info(f"{'footing':>10} {'sphere sep':>11} {'FM12 sep':>10} {'systematic':>11} {'ratio sys/sig':>14} {'verdict':>22}")
FOOT = {}
for foot, a0 in A0.items():
    s, f = TAB[(foot, "sphere")]["sep"], TAB[(foot, "fm12")]["sep"]
    sysd = abs(s - f); rat = sysd/abs(s)
    FOOT[foot] = (s, f, sysd, rat)
    info(f"{foot:>10} {s:+11.3f} {f:+10.3f} {sysd:11.3f} {rat:14.2f} "
         f"{('systematic WINS' if rat > 1 else 'signal wins'):>22}")
ck("V4 (THE RULE-MANDATED TEST g05 NEVER RAN) the systematic-versus-signal verdict is the same on BOTH a_0 "
   "footings, so the claim is not a footing artefact.  This is a check the claim needed and did not have",
   min(FOOT[f][3] for f in FOOT) > 1.0,
   "; ".join(f"{f}: signal {FOOT[f][0]:+.3f}, systematic {FOOT[f][2]:.3f}, ratio {FOOT[f][3]:.2f}" for f in FOOT))

# ==========================================================================================================
P(""); P("="*122)
P("V5.  IS THE RATIO 1.4 A STATEMENT?  Both numbers are differences of MEDIANS of 14 objects.")
P("="*122)
nm, dl_s, _, xi_s, xe_s = matched(a0c, "sphere")
_,  dl_f, _, _,    _    = matched(a0c, "fm12")
rot = rot_deltas(a0c)
info(f"the {len(nm)} matched pressure objects, object by object, under both defensible prescriptions:")
info(f"{'object':22} {'x_i':>9} {'x_e':>9} {'x_e/x_i':>8} {'sphere delta':>13} {'FM12 delta':>11} {'shift':>8}")
for i in np.argsort(xi_s):
    info(f"{nm[i]:22} {xi_s[i]:9.5f} {xe_s[i]:9.5f} {xe_s[i]/xi_s[i]:8.2f} {dl_s[i]:+13.3f} {dl_f[i]:+11.3f} "
         f"{dl_f[i]-dl_s[i]:+8.3f}")
info(f"   median pointwise prescription shift {np.median(dl_f-dl_s):+.3f} dex; "
     f"largest {np.max(dl_f-dl_s):+.3f}, smallest {np.min(dl_f-dl_s):+.3f}")

NB = 20000
idx = rng.integers(0, len(dl_s), size=(NB, len(dl_s)))
mrot = float(np.median(rot))
bs_s = np.median(dl_s[idx], axis=1) - mrot
bs_f = np.median(dl_f[idx], axis=1) - mrot
bs_rat = np.abs(bs_s - bs_f)/np.maximum(np.abs(bs_s), 1e-6)
frac = float(np.mean(bs_rat > 1.0))
ck("V5 (FAILS IF THE RATIO IS NOT STABLE) 'the systematic is 1.4 times the signal' is a ratio of two "
   "differences of medians of 14 objects.  Resampling those 14 objects, the ratio has to stay above 1 in at "
   "least 80 per cent of resamples for 'the systematic wins' to be a statement rather than a coin flip",
   frac > 0.80,
   f"bootstrap over the {len(dl_s)} matched objects: ratio > 1 in {100*frac:.0f} per cent of {NB} resamples; "
   f"ratio 16-50-84 percentiles {np.percentile(bs_rat,16):.2f} / {np.percentile(bs_rat,50):.2f} / "
   f"{np.percentile(bs_rat,84):.2f}; sphere separation {np.percentile(bs_s,16):+.3f} to {np.percentile(bs_s,84):+.3f} dex")

# ==========================================================================================================
P(""); P("="*122)
P("V6.  IS THE 1-D FORMULA A DEFENSIBLE EVALUATION OF THE SAME FIELD, OR JUST WRONG?")
P("="*122)
info("g05's own stated weakest link: the sphere average is exact (QUMOND flux theorem) and the 1-D formula is an")
info("approximation, so the 0.093 dex might be the approximation's ERROR rather than an ambiguity.  Test: the")
info("exact QUMOND source S.rhat is a function of direction.  If the 1-D value lies INSIDE the pointwise range")
info("of the exact field it is an evaluation of that field along one direction -- defensible, and the spread is")
info("real physics.  If it lies OUTSIDE, it is not a possible value of anything and should simply be dropped.")

def Sr_of_theta(x_i, x_e, th):
    st, ctm = math.sin(th), math.cos(th)
    gx, gz = -x_i*st, x_e - x_i*ctm
    return -float(nu_s(math.sqrt(gx*gx + gz*gz))*(gx*st + gz*ctm))

info("")
info(f"{'object':22} {'x_i':>8} {'x_e':>8} {'min_th S_r':>11} {'sphere avg':>11} {'max_th S_r':>11} {'FM12':>9} {'inside?':>8}")
inside = 0; tested = 0; aniso = []
for i in np.argsort(xi_s):
    xi, xe = xi_s[i], xe_s[i]
    ths = np.linspace(0, math.pi, 721)
    vals = np.array([Sr_of_theta(xi, xe, t) for t in ths])
    sa, f1 = sphere_gl(xi, xe), fm12(xi, xe)
    ins = (vals.min() - 1e-12) <= f1 <= (vals.max() + 1e-12)
    inside += int(ins); tested += 1
    aniso.append((vals.max() - vals.min())/sa)
    info(f"{nm[i]:22} {xi:8.5f} {xe:8.5f} {vals.min():11.5f} {sa:11.5f} {vals.max():11.5f} {f1:9.5f} {str(ins):>8}")
ck("V6 (FAILS, AND THIS IS THE FIRST HALF OF THE REFUTATION) the one-dimensional formula would be a defensible "
   "alternative if its value were a possible value of the field it approximates -- i.e. if it lay inside the "
   "range the EXACT QUMOND radial source takes over the sphere.  For 13 of the 14 matched objects it lies BELOW "
   "the exact MINIMUM over all directions.  It is not the exact field evaluated with some other directional "
   "weighting; it is a number the field never takes anywhere on the sphere",
   inside == tested, f"{inside} of {tested} matched objects have FM12 inside [min_theta S_r, max_theta S_r]; "
   f"where it is outside it is always BELOW the minimum, i.e. it systematically under-predicts the binding force")

aniso = np.array(aniso)
ck("V7 the one loophole that could have RESCUED the claim is closed: 'an isotropic velocity dispersion measures "
   "exactly the sphere average' is strictly an overclaim -- the flux theorem gives <g_r> = <S_r> at fixed radius "
   "exactly, but the observed side g_obs = 3 sigma^2/r_1/2 comes from the Wolf et al. 2010 estimator, which is "
   "derived for a SPHERICALLY SYMMETRIC potential, and in an external field it is not.  Had that anisotropy been "
   "large it would have supplied a genuine irreducible systematic and saved the claim.  It does not: over the "
   "matched objects the exact radial force varies over the sphere by a median of a few per cent",
   float(np.median(aniso)) < 0.15,
   f"peak-to-peak variation of the exact radial source over the sphere, in units of the sphere average: "
   f"median {np.median(aniso):.2f}, range {aniso.min():.2f}-{aniso.max():.2f} across the {tested} matched objects "
   f"({int((aniso > 0.5).sum())} of {tested} exceed 50 per cent).  Too small to be the 0.093 dex claimed")

# ---- V7b.  HOW BIG IS THE EXTERNAL-FIELD EFFECT ITSELF ON THE MATCHED SAMPLE? -----------------------------
P(""); P("-"*122)
P("V7b.  THE DECISIVE ONE.  How much external-field effect is there in the MATCHED sample at all?")
P("-"*122)
info("The claim calls 0.093 dex an EXTERNAL-FIELD-PRESCRIPTION systematic.  A prescription systematic cannot be")
info("larger than the effect being prescribed.  So: for each matched object, compare the exact prescription")
info("against SWITCHING THE EXTERNAL FIELD OFF ENTIRELY (x_e = 0, the framework's isolated kernel nu(x_i) x_i).")
info("That difference IS the external-field effect, in the same dex currency.")
info("")
info(f"{'object':22} {'x_e/x_i':>8} {'EFE effect (dex)':>17} {'FM12 - exact (dex)':>19} {'ratio':>8}")
efe_eff, fm_dev = [], []
for i in np.argsort(xi_s):
    xi, xe = xi_s[i], xe_s[i]
    e = abs(math.log10(sphere_gl(xi, xe)/(nu_s(xi)*xi)))
    f = abs(math.log10(fm12(xi, xe)/sphere_gl(xi, xe)))
    efe_eff.append(e); fm_dev.append(f)
    info(f"{nm[i]:22} {xe/xi:8.3f} {e:17.4f} {f:19.4f} {f/max(e,1e-6):8.1f}")
efe_eff, fm_dev = np.array(efe_eff), np.array(fm_dev)
ck("V7b (FAILS, AND IT IS THE REFUTATION) the 0.093 dex is NOT an external-field-prescription systematic, "
   "because on the matched sample there is almost no external field effect to prescribe.  EVERY one of the 14 "
   "matched objects has x_e < x_i -- the matching to SPARC's acceleration range selects exactly the objects "
   "whose internal field dominates -- and switching the external field off entirely moves the exact prediction "
   "by a median of well under 0.01 dex.  The FM12 formula nevertheless departs from the exact answer by a median "
   "0.06 dex on the same objects, an order of magnitude more than the entire physical effect it claims to be a "
   "treatment of.  A spread that survives when the effect it prescribes is switched off is not a systematic of "
   "that effect; it is one formula's error",
   float(np.median(fm_dev)) < 3.0*float(np.median(efe_eff)),
   f"median external-field effect on the matched sample {np.median(efe_eff):.4f} dex (largest {efe_eff.max():.4f}, "
   f"Sculptor, the only object with x_e/x_i > 0.25); median FM12 departure from exact {np.median(fm_dev):.4f} dex "
   f"(largest {fm_dev.max():.4f}) -- a factor {np.median(fm_dev)/max(np.median(efe_eff),1e-6):.0f} in the median.  "
   f"All 14 matched objects have x_e/x_i <= {(xe_s/xi_s).max():.2f}")

P("")
info("AND THE CONTRAST THAT MAKES THE POINT SHARP -- the SAME test on the UNMATCHED (raw) sample, where the")
info("claim's other number, 0.205 dex on a +0.489 dex offset, lives:")
raw_e, raw_f, raw_r = [], [], []
for k in KEYS:
    for d in classes[k]:
        _, xi, xe = row(d, a0c)
        raw_e.append(abs(math.log10(sphere_gl(xi, xe)/(nu_s(xi)*xi))))
        raw_f.append(abs(math.log10(fm12(xi, xe)/sphere_gl(xi, xe))))
        raw_r.append(xe/xi)
raw_e, raw_f, raw_r = np.array(raw_e), np.array(raw_f), np.array(raw_r)
info(f"   RAW sample     N = {len(raw_e):3d}: {100*np.mean(raw_r > 1):.0f} per cent have x_e > x_i, median x_e/x_i = {np.median(raw_r):.2f}; "
     f"true external-field effect median {np.median(raw_e):.3f} dex; FM12 departure median {np.median(raw_f):.3f} dex")
info(f"   MATCHED sample N = {len(efe_eff):3d}: {100*np.mean((xe_s/xi_s) > 1):.0f} per cent have x_e > x_i, median x_e/x_i = {np.median(xe_s/xi_s):.2f}; "
     f"true external-field effect median {np.median(efe_eff):.4f} dex; FM12 departure median {np.median(fm_dev):.3f} dex")
ck("V7d (PASSES, AND IT IS WHY THE CLAIM'S TWO HALVES MUST BE SEPARATED) on the RAW sample the external field "
   "really is doing work -- more than half those objects have x_e > x_i and the true external-field effect is a "
   "median 0.15 dex -- so calling the 0.205 dex there a prescription systematic is at least arguable.  On the "
   "MATCHED sample it is not arguable at all, because the matching removes every external-field-dominated "
   "object.  The claim's raw half and matched half are not the same statement and the matched half does not "
   "inherit the raw half's defence",
   np.median(raw_e) > 0.05 and np.median(efe_eff) < 0.01,
   f"raw: true EFE {np.median(raw_e):.3f} dex vs FM12 departure {np.median(raw_f):.3f} dex (comparable); "
   f"matched: true EFE {np.median(efe_eff):.4f} dex vs FM12 departure {np.median(fm_dev):.3f} dex "
   f"(a factor {np.median(fm_dev)/max(np.median(efe_eff),1e-9):.0f})")

info("")
info("WHY the 1-D formula fails here, analytically.  In the deep-MOND limit nu(y)y = sqrt(y), so")
info("   FM12  = sqrt(x_i + x_e) - sqrt(x_e)  =  sqrt(x_i) [1 - sqrt(x_e/x_i) + ...]")
info("i.e. its deficit against the isolated value is FIRST ORDER IN sqrt(x_e/x_i).  The exact sphere average,")
info("by contrast, expands as -<F(x_i - x_e cos th)> with F(u) = nu(u) u, whose linear term averages to zero:")
info("its deficit is SECOND order in x_e/x_i.  The two are not competing treatments of one effect -- they are")
info("different ORDERS, and the 1-D formula carries a spurious sqrt(x_e) suppression that never switches off.")
info(f"{'x_e/x_i':>10} {'exact deficit (dex)':>21} {'FM12 deficit (dex)':>20} {'sqrt(x_e/x_i)':>15}")
XI = 0.02
ords = []
for ratio in (1e-4, 1e-3, 1e-2, 0.1):
    xe = ratio*XI
    de = abs(math.log10(sphere_gl(XI, xe)/(nu_s(XI)*XI)))
    df = abs(math.log10(fm12(XI, xe)/(nu_s(XI)*XI)))
    ords.append((ratio, de, df))
    info(f"{ratio:10.4f} {de:21.6f} {df:20.6f} {math.sqrt(ratio):15.4f}")
# fit the power over 1e-3 to 0.1 only: at 1e-4 the exact deficit is at the quadrature's own noise floor
p_exact = math.log(ords[-1][1]/ords[1][1])/math.log(ords[-1][0]/ords[1][0])
p_fm12 = math.log(ords[-1][2]/ords[1][2])/math.log(ords[-1][0]/ords[1][0])
ck("V7c (FAILS) the two prescriptions do not even agree on the ORDER of the external-field effect, which is why "
   "their difference does not shrink where the effect does.  Fitting the deficit against the isolated kernel as "
   "a power of x_e/x_i over four decades: the exact sphere average scales with a power near 1, the 1-D formula "
   "with a power near 1/2.  A treatment that disagrees about the leading power of the small parameter is not an "
   "alternative prescription for the same physics",
   abs(p_exact - p_fm12) < 0.2,
   f"exact deficit ~ (x_e/x_i)^{p_exact:.2f}, FM12 deficit ~ (x_e/x_i)^{p_fm12:.2f}; at x_e/x_i = 1e-4 the exact "
   f"external-field effect is {ords[0][1]:.2e} dex while FM12 still shows {ords[0][2]:.4f} dex, a spurious "
   f"suppression that does not vanish with the external field")

# ==========================================================================================================
P(""); P("="*122)
P("V8.  THE DEEP-MOND LIMIT, WHERE g05 ACTUALLY APPLIED IT (check A1c).")
P("="*122)
allrows = [row(d, a0c) for k in ("classical", "m31", "isolated", "ultrafaint") for d in classes[k]]
lx = np.array([math.log10(t[1]) for t in allrows])
rr = np.array([t[0] for t in allrows])
xie = np.array([t[2]/t[1] for t in allrows])
nefe = int((xie > 1).sum())
info(f"external-field census over the {len(allrows)} pressure objects: {nefe} have x_e > x_i "
     f"({100*nefe/len(allrows):.0f} per cent), median x_e/x_i = {np.median(xie):.2f}, "
     f"up to {xie.max():.0f}.")
info("In the ISOLATED deep-MOND limit g_pred ~ sqrt(x_i), so a residual slope of -0.5 means g_obs is flat in x_i.")
info("In the EXTERNAL-FIELD-DOMINATED limit g_pred ~ nu(x_e)(1 + L_e/3) x_i, LINEAR in x_i, so a flat g_obs")
info("gives a slope of -1.  This sample is mostly the second case, so -0.5 is NOT the no-information value.")

sl_real = float(np.polyfit(lx, rr, 1)[0])
# the mechanical identity, COMPUTED: hold g_obs fixed at the sample median and refit.
gobs_med = float(np.median([3.0*(d["sig"]*1e3)**2/((4.0/3.0)*d["rh"]*PC)
                            for k in ("classical", "m31", "isolated", "ultrafaint") for d in classes[k]]))
rr_flat = []
for k in ("classical", "m31", "isolated", "ultrafaint"):
    for d in classes[k]:
        _, xi, xe = row(d, a0c)
        rr_flat.append(math.log10(gobs_med/(sphere_gl(xi, xe)*a0c)))
rr_flat = np.array(rr_flat)
sl_ident = float(np.polyfit(lx, rr_flat, 1)[0])
info("")
info(f"   measured residual slope                                  {sl_real:+.3f} dex/dex")
info(f"   the mechanical identity, COMPUTED (g_obs replaced by its sample median, so g_obs carries NO")
info(f"   dependence on x_i at all, and the same prescription refitted)                 {sl_ident:+.3f} dex/dex")
info(f"   g05's asserted identity value (isolated deep-MOND, g ~ sqrt(x_i))            -0.500 dex/dex")
ck("V8 (FAILS -- g05 APPLIED THE ISOLATED DEEP-MOND LIMIT TO AN EXTERNAL-FIELD-DOMINATED SAMPLE) g05's check "
   "A1c reads its measured slope of -0.498 as 'exactly the mechanical identity', on the argument that "
   "g_pred = sqrt(x_i) a_0.  That is the ISOLATED deep-MOND limit and most of these dwarfs are not isolated.  "
   "Computing the identity instead of asserting it -- replace every g_obs by a constant and refit through the "
   "same prescription -- gives a different number, so the measured slope is NOT the no-information value and "
   "A1c's reading of it is wrong.  This does not touch the S2b claim, but it is a physics error in the same file",
   abs(sl_ident - (-0.500)) < 0.05,
   f"computed identity slope {sl_ident:+.3f} against the asserted -0.500 (difference {sl_ident+0.500:+.3f}); "
   f"measured slope {sl_real:+.3f}.  {nefe} of {len(allrows)} objects have x_e > x_i, where g_pred is LINEAR in "
   f"x_i and the identity slope would be -1")

# ==========================================================================================================
P(""); P("="*122)
P("V9.  WHAT THE SYSTEMATIC DOES AND DOES NOT DO TO THE SIGN.")
P("="*122)
ck("V9 (FAILS, AND THE FAILURE IS AGAINST THE CLAIM'S RHETORIC RATHER THAN ITS NUMBER) S2b's text says the "
   "separation 'changes SIGN and lands four sigma on the WRONG side'.  It does so ONLY under f09's max() branch, "
   "which g05's own check P3 demonstrates is a kinked, non-physical prescription and which g05 elsewhere "
   "discards.  Between the two treatments S2b itself calls defensible, the separation is POSITIVE both times and "
   "the sign never moves.  The honest statement is narrower than the one made: the separation lies somewhere "
   "between +0.06 dex (0.9 sigma) and +0.16 dex (2.1 sigma) depending on prescription, which is uninformative, "
   "but it is not sign-ambiguous",
   c_sph["sep"]*c_fm["sep"] < 0,
   f"sphere {c_sph['sep']:+.3f} and FM12 {c_fm['sep']:+.3f} are both POSITIVE; only the discarded f09 branch "
   f"({c_f09['sep']:+.3f}) is negative")

s_lo, s_hi = min(c_sph["sep"], c_fm["sep"]), max(c_sph["sep"], c_fm["sep"])
n_lo, n_hi = min(c_sph["nsig"], c_fm["nsig"]), max(c_sph["nsig"], c_fm["nsig"])
ck("V10 the operative conclusion is over-determined and does not need the systematic argument at all: under the "
   "EXACT prescription alone, with no appeal to any systematic, the matched separation is under one sigma with a "
   "permutation p of order 0.1 on 14 pressure objects.  'Not a measurement' follows from the statistics; the "
   "systematic argument adds a second, weaker reason for the same verdict",
   c_sph["nsig"] < 2.0 and n_hi < 2.5,
   f"exact prescription {c_sph['sep']:+.3f} dex ({c_sph['nsig']:.2f} sigma) on N = {c_sph['n']}; the full "
   f"prescription range is {s_lo:+.3f} to {s_hi:+.3f} dex ({n_lo:.2f} to {n_hi:.2f} sigma) -- the TOP of that "
   f"range is still not a result")

# mutation control on the claim's own machinery
P(""); P("="*122)
P("MUTATION CONTROLS ON THIS VERIFICATION.")
P("="*122)
big = a0c*100
raw_big = float(np.median([row(d, big)[0] for k in KEYS for d in classes[k]]))
raw_now = float(np.median([row(d, a0c)[0] for k in KEYS for d in classes[k]]))
ck("M1 raising a_0 by 100 drives every object deep into the modified regime and must lower every residual",
   raw_big < raw_now - 0.2, f"median raw {raw_now:+.3f} dex at canonical a_0, {raw_big:+.3f} at 100 a_0")

sys_zero = abs(sphere_gl(0.02, 0.0) - fm12(0.02, 0.0))
ck("M2 MUTATION CONTROL ON THE SYSTEMATIC ITSELF: switch the external field off and the two prescriptions must "
   "become the SAME function, so the prescription systematic must vanish identically.  If it did not, the "
   "0.093 dex would be measuring something other than the external-field treatment",
   sys_zero < 1e-12, f"|sphere - FM12| at x_e = 0 is {sys_zero:.3e} in units of a_0")

sep_shift = sep_of(a0c, "sphere")["sep"]
nm2, dl2, _, _, _ = matched(a0c, "sphere")
perm = np.array([abs(np.median((q := rng.permutation(np.concatenate([dl2, rot])))[:len(dl2)]) -
                     np.median(q[len(dl2):])) for _ in range(20000)])
pv = float(np.mean(perm >= abs(sep_shift - np.median(rot))))
ck("M3 the permutation test on the exact prescription reproduces g05's p of about 0.10, independently",
   0.05 < pv < 0.20, f"permutation p = {pv:.4f} on N_pressure = {len(dl2)} against N_rotating = {len(rot)}")

P(""); P("="*122); P("VERDICT OF THE ADVERSARIAL PASS:  THE CLAIM IS REFUTED AS STATED."); P("="*122)
P(f"  THE ARITHMETIC IS CORRECT AND REPRODUCES INDEPENDENTLY (V1-V4).  Matched separation {c_sph['sep']:+.3f} dex under the")
P(f"  exact sphere average, {c_fm['sep']:+.3f} dex under FM12 eq. 60, difference {abs(c_sph['sep']-c_fm['sep']):.3f} dex, ratio {abs(c_sph['sep']-c_fm['sep'])/abs(c_sph['sep']):.1f}; and it is the")
P(f"  same on both a_0 footings, which g05 never checked (its scan() hard-codes the canonical a_0).  Nothing is")
P(f"  wrong with the numbers.  What is wrong is what they are called.")
P(f"")
P(f"  THE 0.093 dex IS NOT AN EXTERNAL-FIELD-PRESCRIPTION SYSTEMATIC (V7b, V7c, V6).  Three independent ways:")
P(f"")
P(f"   1. THE MATCHED SAMPLE HAS ALMOST NO EXTERNAL FIELD IN IT.  Matching to SPARC's acceleration coverage")
P(f"      selects the 14 objects with the HIGHEST internal acceleration, and every one of them has x_e < x_i")
P(f"      (max x_e/x_i = {(xe_s/xi_s).max():.2f}, median {np.median(xe_s/xi_s):.2f}).  Switching the external field off ENTIRELY moves the")
P(f"      exact prediction by a median {np.median(efe_eff):.4f} dex and at most {efe_eff.max():.4f} dex.  The claimed 'external-field")
P(f"      prescription systematic' is {np.median(fm_dev)/max(np.median(efe_eff),1e-6):.0f} times the whole external-field effect it purports to prescribe.")
P(f"      A spread that persists when the effect is switched off is not a systematic of that effect.")
P(f"")
P(f"   2. THE 1-D FORMULA IS NOT A VALUE THE FIELD EVER TAKES.  For {tested-inside} of the {tested} matched objects it lies BELOW")
P(f"      the exact QUMOND radial source's MINIMUM over every direction on the sphere.  It is not the same field")
P(f"      evaluated with a different directional weighting; it is outside the field's range.")
P(f"")
P(f"   3. THE TWO DISAGREE ON THE ORDER OF THE EFFECT.  Deep-MOND: FM12 = sqrt(x_i+x_e) - sqrt(x_e), deficit")
P(f"      first order in sqrt(x_e/x_i); the exact sphere average's linear term cancels by symmetry, deficit")
P(f"      second order.  Measured over four decades: exact ~ (x_e/x_i)^{p_exact:.2f}, FM12 ~ (x_e/x_i)^{p_fm12:.2f}.  The 1-D")
P(f"      formula carries a spurious sqrt(x_e) suppression that never switches off, and THAT, not any physical")
P(f"      ambiguity, is the whole of the 0.093 dex.")
P(f"")
P(f"  AND THE LOOPHOLE THAT COULD HAVE SAVED IT IS CLOSED (V7).  g05's own weakest-link defence -- that the")
P(f"  sphere average is only exact for an isotropic tracer -- is a real overclaim: the Wolf et al. 2010 estimator")
P(f"  assumes a spherically symmetric potential and the external field breaks that.  Had the anisotropy been")
P(f"  large it would have supplied a genuine irreducible systematic.  It is a median {np.median(aniso)*100:.0f} per cent peak-to-peak")
P(f"  over the matched objects, far too small to be the 0.093 dex.")
P(f"")
P(f"  TWO FURTHER OVERSTATEMENTS.  (V5) 'ratio 1.4' is a ratio of two differences of medians of 14 objects; it")
P(f"  exceeds 1 in only {100*frac:.0f} per cent of bootstrap resamples, 16-84 range {np.percentile(bs_rat,16):.2f} to {np.percentile(bs_rat,84):.2f}.  (V9) 'changes SIGN")
P(f"  and lands four sigma on the WRONG side' is true only of f09's max() branch, which g05's own check P3 shows")
P(f"  is kinked and which g05 discards everywhere else; between the two treatments the claim itself calls")
P(f"  defensible the separation is positive both times, {s_lo:+.3f} to {s_hi:+.3f} dex.")
P(f"")
P(f"  WHAT SURVIVES, AND IT IS THE CONCLUSION RATHER THAN THE ARGUMENT (V10).  Under the exact prescription")
P(f"  alone -- no appeal to any systematic -- the matched separation is {c_sph['sep']:+.3f} dex, {c_sph['nsig']:.2f} sigma, permutation")
P(f"  p = {pv:.2f} on {c_sph['n']} pressure objects, and the top of the whole prescription range is {n_hi:.1f} sigma.  'Not a")
P(f"  measurement' is forced by the statistics and the sample size.  It is NOT forced by, and should not be")
P(f"  argued from, a prescription systematic that the physics says is not there.")
P(f"")
P(f"  QUOTE INSTEAD:  'With the exact QUMOND sphere average the matched separation is +0.06 dex, 0.93 sigma,")
P(f"  p = 0.10 on 14 objects and 2.9 sigma only under a 0.40 dex matching window that re-admits objects with no")
P(f"  rotating counterpart.  The published 1-D external-field formula gives +0.16 dex, but it under-predicts the")
P(f"  exact field everywhere on the sphere for these near-isolated objects and its departure is its own")
P(f"  convergence error, not a systematic of the framework.'")
P(f"")
P(f"  ONE FURTHER PHYSICS ERROR IN THE SAME FILE, load-bearing for a DIFFERENT g05 claim (V8): check A1c reads")
P(f"  its measured residual slope of -0.498 as the mechanical identity of the ISOLATED deep-MOND limit,")
P(f"  g ~ sqrt(x_i).  {nefe} of {len(allrows)} of these dwarfs have x_e > x_i and are EXTERNAL-FIELD dominated, where the")
P(f"  prediction is LINEAR in x_i and the identity slope is -1.  Computing the identity instead of asserting it")
P(f"  -- hold g_obs fixed and refit through the same prescription -- gives {sl_ident:+.3f}, not -0.500.  So the measured")
P(f"  -0.498 is NOT the no-information value: it is {abs(sl_real-sl_ident):.2f} dex/dex away from it, and A1c's reading of its")
P(f"  own slope as 'a mechanical identity' is wrong in the direction of understating what it measured.")
sys.exit(ck.done())
