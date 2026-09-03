#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_adversarial_confound_refutation.py
===========================================================================================================
ADVERSARIAL VERIFICATION of check A1b in g05_dsph_prescription_fixed_and_expanded.py.

THE CLAIM UNDER ATTACK (A1b, verbatim intent):
  "Support type and acceleration DEPTH are completely confounded in the Local Group, so no Local Group
   comparison can separate them.  36 of 50 pressure objects sit below SPARC's deepest coverage; their median
   raw residual is +0.731 dex, the 14 inside coverage sit at +0.114 dex -- a factor 6.4 in the same currency
   with support type held fixed."

MY BRIEF: attack the ESTIMATOR and the arithmetic.  Re-derive the central numbers from the raw catalogue
columns through an INDEPENDENT code path (no call to g05's dsph_row / g_qumond_sphere for the data numbers),
then ask whether the quoted statistic can carry the claim.

WHAT IS TESTED, and what each test can prove:
  V1  arithmetic reproduction from raw CSV, independent implementation of Wolf+2010 and of the QUMOND sphere
      average.  If g05's numbers do not come back, the arithmetic is wrong and the claim falls on that alone.
  V2  the two medians, the split threshold, and whether "below SPARC's coverage" is literally true.
  V3  NULL INJECTION.  Replace every observed dispersion by the one the framework itself predicts, plus SPARC's
      own 0.13 dex scatter.  A clean estimator must return kept ~ dropped ~ 0 and a ratio near 1.
  V4  CONSTANT-OFFSET INJECTION -- THE DECISIVE ONE.  Inject a purely SUPPORT-TYPE effect: a depth-INDEPENDENT
      +0.40 dex on every pressure object, on top of a framework-consistent baseline.  If the A1b statistic
      still reports a large "factor", then that statistic cannot distinguish depth from support and the
      inference drawn from it is void.
  V5  the ratio is a ratio of dex, i.e. of a zero-point-dependent quantity.  Recompute on BOTH a_0 footings and
      bootstrap it.  A statistic whose 68 per cent interval is unbounded is not a measurement.
  V6  CLASS COMPOSITION of the dropped set -- is +0.731 dex depth, or is it the M31 satellites the file's own
      reliability table calls "the class most likely to be inflating the result"?
  V7  THE COUNTEREXAMPLE INSIDE g05 ITSELF.  Outer-halo globular clusters are pressure-supported, are in the
      Local Group, and sit at x_i = 0.01-1.2, i.e. NOT deep.  If they exist, "pressure-supported" and "deep"
      are NOT the same set in the Local Group and the confound is not complete.
  V8  is the Local Group comparison at fixed depth actually IMPOSSIBLE, or merely UNDERPOWERED?  Those are
      different claims and only one of them is what g05 demonstrated.

DATA: identical to g05 -- Local Volume Database (Pace 2024, ApJS 273, 15), SPARC (Lelli, McGaugh & Schombert
2016, AJ 152, 157), Baumgardt & Hilker 2018 / Jordi et al. 2009 / Frank et al. 2012 for the clusters.
Wolf et al. 2010, MNRAS 406, 1220 for M_1/2 = 3 sigma^2 r_1/2 / G.  BOTH a_0 FOOTINGS.  MUTATION CONTROLS.
Checks here PASS when the claim SURVIVES and FAIL when it does not; several fail.
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
P("PART 0.  AN INDEPENDENT IMPLEMENTATION OF THE PREDICTION, WRITTEN WITHOUT LOOKING AT g05's QUADRATURE.")
P("="*122)
info("g05's sphere average is  <g_r> = -(1/2) INT nu(|x_e zhat - x_i rhat|) (x_e zhat - x_i rhat).rhat sin th dth.")
info("I implement it here by GAUSS-LEGENDRE in mu = cos(theta) instead of a trapezoid in theta, which is a")
info("different quadrature rule on a different variable, so an error in either shows up as a disagreement.")

_GLMU, _GLW = np.polynomial.legendre.leggauss(400)
_GLST = np.sqrt(np.maximum(1.0 - _GLMU*_GLMU, 0.0))
_GLCACHE = {}
def g_sphere_gl(x_i, x_e, n=400):
    """Sphere-averaged radial QUMOND acceleration in units of a_0.  Gauss-Legendre in mu = cos(theta).
       <g_r> = -(1/2) INT_{-1}^{1} nu(|gN|) (gN . rhat) dmu,  gN = x_e zhat - x_i rhat.
       Memoised on (x_i, x_e): the function is pure, so the cache cannot change any number."""
    key = (x_i, x_e)
    v = _GLCACHE.get(key)
    if v is not None: return v
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        v = nu_s(x_i)*x_i
    else:
        mu, w, st = _GLMU, _GLW, _GLST
        gx, gz = -x_i*st, x_e - x_i*mu
        v = -0.5*float(np.sum(w*nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*mu)))
    _GLCACHE[key] = v
    return v

# g05's own routine, imported by execution so the comparison is against the committed code, not a copy
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_g05src", os.path.join(HERE, "g05_dsph_prescription_fixed_and_expanded.py"))
# do NOT import g05 (it runs a 5 s analysis and sys.exits); re-implement its trapezoid rule verbatim instead
def g_sphere_trapz(x_i, x_e, ntheta=2001):
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    th = np.linspace(0.0, math.pi, ntheta)
    st, ctm = np.sin(th), np.cos(th)
    gx, gz = -x_i*st, x_e - x_i*ctm
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*ctm)
    return -float(np.trapz(Sr*st, th)/np.trapz(st, th))

pairs = [(1e-4, 1e-3), (1e-3, 1e-2), (0.01, 0.03), (0.03, 0.02), (0.1, 0.05), (1.0, 0.02), (30.0, 0.01)]
dev = [abs(g_sphere_gl(a, b)/g_sphere_trapz(a, b) - 1) for a, b in pairs]
ck("V0 two independent quadrature rules (Gauss-Legendre in cos theta against g05's trapezoid in theta) agree on the sphere-averaged QUMOND acceleration to better than 1e-6 at every (x_i, x_e) that occurs in the sample, so the PREDICTED side of every residual is arithmetically sound",
   max(dev) < 1e-6, f"worst fractional disagreement {max(dev):.2e} over {len(pairs)} (x_i,x_e) pairs")

m1 = [(-0.5*float(np.sum(_GLW*((-xi*_GLST)*_GLST + (xe - xi*_GLMU)*_GLMU))))/xi
      for xi, xe in ((0.01, 0.1), (0.001, 1.0), (0.5, 0.02))]
ck("M-A MUTATION CONTROL on my own quadrature: with nu = 1 it must return the internal Newtonian field EXACTLY at any external field, so my machinery is not manufacturing a coupling either",
   max(abs(v - 1) for v in m1) < 1e-10, "Newtonian sphere average / x_i = " + ", ".join(f"{v:.12f}" for v in m1))

# ==========================================================================================================
P(""); P("="*122)
P("PART 1.  THE SAMPLE AND THE RESIDUALS, RE-DERIVED FROM THE RAW CATALOGUE COLUMNS.")
P("="*122)

def fnum(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def load(fname, host_mb, host_name):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fname))):
        sig, ul = fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
        MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
        if fnum(r["confirmed_galaxy"]) != 1: continue
        lMs, lMHI = fnum(r["mass_stellar"]), fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, rh=rh, sig=sig,
                        Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
                        MHI=(10**lMHI if lMHI is not None else 0.0),
                        Dhost=fnum(r["distance_host"]) or fnum(r["distance_gc"]),
                        Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                        host=host_name, host_mb=host_mb))
    return out

ROT = {"LMC", "SMC"}; DIS = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
def classify(d, host):
    if d["name"] in ROT or d["name"] in DIS: return None
    if d["MHI"] > 0.3*d["Ms"]: return None
    if host == "field": return "isolated"
    if host == "M31":   return "m31"
    return "classical" if d["MV"] <= -7.7 else "ultrafaint"

classes = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
for src, host in ((load("lvd_dwarf_mw.csv", MW_MB, "MW"), "MW"),
                  (load("lvd_dwarf_m31.csv", M31_MB, "M31"), "M31"),
                  (load("lvd_dwarf_local_field.csv", None, "field"), "field")):
    for d in src:
        c = classify(d, host)
        if c: classes[c].append(d)
KEYS = ["classical", "m31", "isolated"]
info(f"reconstructed sample: classical {len(classes['classical'])}, M31 {len(classes['m31'])}, "
     f"isolated {len(classes['isolated'])}, ultrafaint {len(classes['ultrafaint'])}; "
     f"the A1b universe is classical+M31+isolated = {sum(len(classes[k]) for k in KEYS)}")

def row(d, a0, sig=None, ups=UPS_V, gobs_override=None):
    """(residual dex, x_i, x_e, g_obs).  Wolf et al. 2010 with r_1/2 = (4/3) R_e, ENCLOSED baryonic mass M_b/2."""
    r12 = (4.0/3.0)*d["rh"]*PC
    Mb = (ups/UPS_V)*d["Ms"] + 1.33*d["MHI"]
    x_i = G*(0.5*Mb*Msun)/r12**2/a0
    if d["host_mb"] is not None and d["Dhost"] and d["Dhost"] > 0:
        x_e = G*d["host_mb"]*Msun/(d["Dhost"]*kpc)**2/a0
    else:
        x_e = ((G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0) +
               (G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0))/a0
    s = d["sig"] if sig is None else sig
    g_obs = (3.0*(s*1e3)**2/r12) if gobs_override is None else gobs_override
    gp = g_sphere_gl(x_i, x_e)*a0
    return math.log10(g_obs/gp), x_i, x_e, g_obs

a0c = A0["canonical"]
gals = load_sparc()
LY = np.concatenate([np.log10(g["gbar"]/a0c) for g in gals])
RRp = np.concatenate([np.log10(g["gobs"]/(nu(g["gbar"]/a0c)*g["gbar"])) for g in gals])

def inside(xi, ly=LY, w=MATCH_W, nmin=MATCH_N):
    return int(np.sum(np.abs(ly - math.log10(xi)) < w)) >= nmin

recs = []
for k in KEYS:
    for d in classes[k]:
        r, xi, xe, go = row(d, a0c)
        recs.append(dict(name=d["name"], cls=k, res=r, xi=xi, xe=xe, gobs=go, obj=d))
kept = [t for t in recs if inside(t["xi"])]
drop = [t for t in recs if not inside(t["xi"])]
mk, md = float(np.median([t["res"] for t in kept])), float(np.median([t["res"] for t in drop]))
info(f"INDEPENDENT RE-DERIVATION: N = {len(recs)}, kept {len(kept)}, dropped {len(drop)}")
info(f"   kept median raw residual {mk:+.3f} dex   dropped median {md:+.3f} dex   ratio {md/mk:.2f}   difference {md-mk:+.3f} dex")
info(f"   g05 reported                +0.114                        +0.731            6.4")
ck("V1 the A1b arithmetic REPRODUCES through a completely independent code path -- catalogue columns read again, Wolf+2010 re-implemented, the sphere average done by a different quadrature rule on a different variable.  N = 50 splits 14/36 and the two medians come back to 0.005 dex.  There is no arithmetic error in the central number",
   len(recs) == 50 and len(kept) == 14 and len(drop) == 36 and abs(mk - 0.114) < 0.01 and abs(md - 0.731) < 0.01,
   f"N={len(recs)}, {len(kept)}/{len(drop)}, kept {mk:+.4f} (g05 +0.114), dropped {md:+.4f} (g05 +0.731)")

xk = sorted(t["xi"] for t in kept); xd = sorted(t["xi"] for t in drop)
ck("V2 the split is a clean threshold in x_i and the words 'below SPARC's coverage' are literally true: every dropped object has a smaller internal acceleration than every kept one, so the kept/dropped label carries no information beyond depth",
   max(xd) < min(xk), f"deepest KEPT x_i = {min(xk):.5f}; shallowest DROPPED x_i = {max(xd):.5f}; "
   f"kept span {min(xk):.5f}-{max(xk):.3f}, dropped span {min(xd):.6f}-{max(xd):.5f}")

# ==========================================================================================================
P(""); P("="*122)
P("PART 2.  WHAT THE A1b STATISTIC DOES TO KNOWN INPUTS.  Injection tests: the only way to find out whether a")
P("         'factor 6.4 with support type held fixed' can mean what it is being asked to mean.")
P("="*122)

def stat(res_by_name):
    """The A1b statistic applied to a supplied set of residuals: (kept median, dropped median, ratio, difference)."""
    k = [res_by_name[t["name"]] for t in kept]; d = [res_by_name[t["name"]] for t in drop]
    a, b = float(np.median(k)), float(np.median(d))
    return a, b, b/a if abs(a) > 1e-9 else float("inf"), b - a

SC = 0.13   # SPARC's own intrinsic RAR scatter, dex (Lelli et al. 2017, ApJ 836, 152: 0.11-0.13 dex)
info(f"(a) NULL INJECTION.  Every object's observed acceleration is REPLACED by the framework's own prediction")
info(f"    times lognormal scatter of {SC} dex (SPARC's intrinsic RAR scatter, Lelli et al. 2017, ApJ 836, 152).")
info(f"    By construction there is NO support-type effect and NO depth effect.  A clean statistic must return")
info(f"    kept ~ dropped ~ 0 and a ratio near 1.")
null_k, null_d, null_r = [], [], []
for _ in range(2000):
    rbn = {}
    for t in recs:
        gp = g_sphere_gl(t["xi"], t["xe"])*a0c
        rbn[t["name"]] = row(t["obj"], a0c, gobs_override=gp*10**rng.normal(0, SC))[0]
    a, b, r_, dd = stat(rbn)
    null_k.append(a); null_d.append(b); null_r.append(dd)
info(f"    null kept median {np.mean(null_k):+.4f} +- {np.std(null_k):.4f};  null dropped median "
     f"{np.mean(null_d):+.4f} +- {np.std(null_d):.4f};  null DIFFERENCE {np.mean(null_r):+.4f} +- {np.std(null_r):.4f}")
ck("V3 the estimator is UNBIASED under the null: fed accelerations that obey the framework exactly plus SPARC's own scatter, the kept and dropped medians both come back at zero and their difference at zero.  The +0.617 dex kept-minus-dropped difference is therefore NOT manufactured by the estimator; something real separates the deep objects from the shallow ones",
   abs(np.mean(null_k)) < 0.02 and abs(np.mean(null_d)) < 0.02 and abs(np.mean(null_r)) < 0.02,
   f"null difference {np.mean(null_r):+.4f} +- {np.std(null_r):.4f} dex over 2000 realisations; the measured "
   f"difference is {md-mk:+.3f} dex, {abs(md-mk-np.mean(null_r))/np.std(null_r):.1f} null-sigma out")

P("")
INJ = 0.40
info(f"(b) CONSTANT-OFFSET INJECTION -- THE DECISIVE TEST.  Same framework-consistent baseline, but now with a")
info(f"    depth-INDEPENDENT +{INJ} dex added to EVERY pressure object.  That is a pure SUPPORT-TYPE effect with")
info(f"    ZERO depth dependence by construction.  If the A1b statistic still reports a large 'factor', then the")
info(f"    factor cannot be read as evidence that the split is 'at least as much about depth as about support'.")
inj_k, inj_d, inj_ratio, inj_diff = [], [], [], []
for _ in range(2000):
    rbn = {}
    for t in recs:
        gp = g_sphere_gl(t["xi"], t["xe"])*a0c
        rbn[t["name"]] = row(t["obj"], a0c, gobs_override=gp*10**(INJ + rng.normal(0, SC)))[0]
    a, b, r_, dd = stat(rbn)
    inj_k.append(a); inj_d.append(b); inj_ratio.append(r_); inj_diff.append(dd)
info(f"    injected PURE support-type effect, no depth dependence at all:")
info(f"       kept median {np.mean(inj_k):+.3f}, dropped median {np.mean(inj_d):+.3f}")
info(f"       RATIO (A1b's headline currency)  {np.mean(inj_ratio):.2f} +- {np.std(inj_ratio):.2f}")
info(f"       DIFFERENCE                        {np.mean(inj_diff):+.3f} +- {np.std(inj_diff):.3f} dex")
ck("V4 (PASSES -- AND IT IS A POINT FOR A1b, RECORDED AS SUCH) I tried to show that a purely depth-INDEPENDENT support-type effect would fake A1b's factor.  It does not.  Injected on a framework-consistent baseline, a flat +0.40 dex returns a ratio of 1.0 and a difference of zero, exactly as it should.  So the measured factor of 6.4 and the measured +0.617 dex difference are NOT what a constant support-type offset looks like; there really is depth structure in the residuals.  This attack fails and A1b keeps the underlying finding",
   abs(np.mean(inj_ratio) - 1.0) < 0.2 and abs(np.mean(inj_diff)) < 0.05,
   f"pure-support injection at +{INJ} dex: kept {np.mean(inj_k):+.3f}, dropped {np.mean(inj_d):+.3f}, ratio "
   f"{np.mean(inj_ratio):.2f} +- {np.std(inj_ratio):.2f}, difference {np.mean(inj_diff):+.3f} +- {np.std(inj_diff):.3f} dex.  "
   f"Measured values are {md/mk:.2f} and {md-mk:+.3f} dex, so the depth structure is real and is not an artefact of a flat offset")

P("")
info("(c) HOW UNCERTAIN IS THE 'FACTOR 6.4'?  Bootstrap both medians (10000 resamples of the 14 and the 36).")
bk, bd, br = [], [], []
rk = np.array([t["res"] for t in kept]); rd = np.array([t["res"] for t in drop])
for _ in range(10000):
    a = float(np.median(rng.choice(rk, len(rk), replace=True)))
    b = float(np.median(rng.choice(rd, len(rd), replace=True)))
    bk.append(a); bd.append(b); br.append(b/a if abs(a) > 1e-9 else np.inf)
br = np.array(br); bdif = np.array(bd) - np.array(bk)
neg = int(np.sum(br < 0)); huge = int(np.sum(np.abs(br) > 50))
info(f"    kept median  {mk:+.3f}, bootstrap 16-84 per cent {np.percentile(bk,16):+.3f} to {np.percentile(bk,84):+.3f}")
info(f"    dropped      {md:+.3f}, bootstrap 16-84 per cent {np.percentile(bd,16):+.3f} to {np.percentile(bd,84):+.3f}")
info(f"    RATIO        {md/mk:.2f}, bootstrap 16-84 per cent {np.percentile(br,16):.2f} to {np.percentile(br,84):.2f}; "
     f"{100*neg/len(br):.1f} per cent of resamples give a NEGATIVE ratio and {100*huge/len(br):.1f} per cent give |ratio| > 50")
info(f"    DIFFERENCE   {md-mk:+.3f}, bootstrap 16-84 per cent {np.percentile(bdif,16):+.3f} to {np.percentile(bdif,84):+.3f}")
ck("V5 (FAILS) the quoted 'factor 6.4' has no usable error bar: the kept median it divides by is +0.114 dex with a bootstrap 68 per cent interval that reaches to within 0.03 dex of zero, so the ratio's own 68 per cent interval runs over a factor of several and a non-negligible fraction of resamples put it negative or above 50.  A ratio whose denominator is consistent with zero is not a measurement.  The DIFFERENCE, +0.617 dex, is well determined and is what the claim should rest on",
   np.percentile(br, 84)/np.percentile(br, 16) < 3.0 and neg == 0 and huge == 0,
   f"ratio 68 per cent interval {np.percentile(br,16):.2f}-{np.percentile(br,84):.2f} (span x{np.percentile(br,84)/max(np.percentile(br,16),1e-9):.1f}), "
   f"{neg} of 10000 resamples negative, {huge} above 50 in absolute value; difference interval "
   f"{np.percentile(bdif,16):+.3f} to {np.percentile(bdif,84):+.3f} dex is tight by comparison")

P("")
info("(d) BOTH a_0 FOOTINGS.  A ratio of dex is zero-point dependent, so it must move when a_0 moves; the")
info("    difference must not.  This is the same complaint, measured rather than asserted.")
foot_out = {}
for fname, a0 in A0.items():
    ly = np.concatenate([np.log10(g["gbar"]/a0) for g in gals])
    kk, dd_ = [], []
    for k in KEYS:
        for d in classes[k]:
            r, xi, _, _ = row(d, a0)
            (kk if inside(xi, ly=ly) else dd_).append(r)
    a, b = float(np.median(kk)), float(np.median(dd_))
    foot_out[fname] = (a, b, b/a, b - a, len(kk), len(dd_))
    info(f"    {fname:10} a_0={a0:.3g}: kept {a:+.3f} (N={len(kk)}), dropped {b:+.3f} (N={len(dd_)}), "
         f"RATIO {b/a:.2f}, DIFFERENCE {b-a:+.3f} dex")
rat_span = abs(foot_out["alt"][2] - foot_out["canonical"][2])
dif_span = abs(foot_out["alt"][3] - foot_out["canonical"][3])
ck("V6 (FAILS) a 21 per cent change in a_0 -- the two footings this repository requires everywhere -- moves the headline 'factor' by more than a whole unit while moving the difference by a few hundredths of a dex.  The number chosen for the headline is the footing-sensitive one",
   rat_span < 0.5, f"ratio {foot_out['canonical'][2]:.2f} (canonical) against {foot_out['alt'][2]:.2f} (alt), "
   f"moves by {rat_span:.2f}; difference {foot_out['canonical'][3]:+.3f} against {foot_out['alt'][3]:+.3f}, moves by {dif_span:.3f} dex")

# ==========================================================================================================
P(""); P("="*122)
P("PART 3.  IS IT DEPTH, OR IS IT THE M31 SATELLITES?  The dropped set's class composition.")
P("="*122)
info("g05's own reliability table says of the M31 class: 'Dispersions of 3-5 km/s sit near the instrumental")
info("floor, Milky Way foreground contamination biases small-N dispersions HIGH ... the class most likely to be")
info("inflating the result.'  Then 35 of the 36 DROPPED objects are... let us count.")
info(f"{'class':12} {'N kept':>7} {'median':>9} {'N dropped':>10} {'median':>9}")
comp = {}
for k in KEYS:
    a = [t["res"] for t in kept if t["cls"] == k]; b = [t["res"] for t in drop if t["cls"] == k]
    comp[k] = (len(a), float(np.median(a)) if a else float("nan"), len(b), float(np.median(b)) if b else float("nan"))
    info(f"{k:12} {len(a):7d} {comp[k][1]:+9.3f} {len(b):10d} {comp[k][3]:+9.3f}")
f_m31_drop = comp["m31"][2]/len(drop)
# depth trend WITHIN the M31 class alone, and WITHIN the non-M31 dropped objects alone
nonm31_drop = [t["res"] for t in drop if t["cls"] != "m31"]
ck("V7 the dropped set is 69 per cent M31 satellites, the one class g05's own reliability note flags as biased HIGH -- but the depth split is NOT reducible to that: the classical Milky Way dwarfs that are dropped sit at a large positive median on their own, and the non-M31 dropped objects do too.  The composition is lopsided and worth stating, but it does not explain the difference away",
   f_m31_drop > 0.5 and float(np.median(nonm31_drop)) > 0.3,
   f"dropped set: {comp['m31'][2]} M31 ({100*f_m31_drop:.0f} per cent, median {comp['m31'][3]:+.3f}), "
   f"{comp['classical'][2]} classical (median {comp['classical'][3]:+.3f}), {comp['isolated'][2]} isolated "
   f"(median {comp['isolated'][3]:+.3f}); non-M31 dropped median {float(np.median(nonm31_drop)):+.3f} dex on N={len(nonm31_drop)}")

# ==========================================================================================================
P(""); P("="*122)
P("PART 4.  THE COUNTEREXAMPLE THAT IS ALREADY INSIDE g05.  'Pressure-supported' and 'deep' are NOT the same")
P("         set in the Local Group, and g05 section 4e proves it on g05's own data.")
P("="*122)
info("Outer-halo globular clusters: pressure-supported, Local Group, and at x_i = 0.01-1.2 they are NOT deep.")
info("Structural parameters Baumgardt & Hilker 2018 / Baumgardt et al. 2019-2023; extinction Harris 2010;")
info("dispersions Jordi et al. 2009, AJ 137, 4586 (Pal 14, 16 members) and Frank et al. 2012, MNRAS 423, 2917")
info("(Pal 4, 23 members).  Pal 3 and NGC 2419 from Baumgardt N-body fits, MODEL-DEPENDENT.  Upsilon_V = 2.")
GC = [("Pal 4", 101.39, 104.05, 14.23, 0.01, 15.88, 0.87),
      ("Pal 14", 73.58, 68.55, 14.13, 0.04, 27.63, 0.38),
      ("Pal 3", 94.84, 98.17, 14.56, 0.04, 20.16, 0.80),
      ("NGC 2419", 88.47, 95.93, 10.56, 0.08, 19.76, 5.10)]
gcr, gcx = [], []
for nm, Dsun, Rgc, V, EBV, rhl, sob in GC:
    MV = V - 5*math.log10(Dsun*1e3/10.0) - 3.1*EBV
    M = UPS_V*10**(0.4*(4.83 - MV))
    r12 = (4.0/3.0)*rhl*PC
    xi = G*(0.5*M*Msun)/r12**2/a0c
    xe = G*MW_MB*Msun/(Rgc*kpc)**2/a0c
    sp = math.sqrt(g_sphere_gl(xi, xe)*a0c*r12/3.0)/1e3
    r = 2.0*math.log10(sob/sp)
    gcr.append(r); gcx.append(xi)
    info(f"      {nm:10} x_i = {xi:.4f}  sigma_obs {sob:.2f}  sigma_pred {sp:.2f}  residual {r:+.3f} dex  "
         f"[{'INSIDE' if inside(xi) else 'outside'} SPARC coverage]")
gc_in = [r for r, x in zip(gcr, gcx) if inside(x)]
dsph_ov = [t["res"] for t in recs if min(gcx) <= t["xi"] <= max(gcx)]
ck("V8 (FAILS -- AND IT REFUTES THE WORD 'COMPLETELY') the confound is NOT complete.  Four pressure-supported Local Group systems sit squarely INSIDE the acceleration range SPARC covers, at exactly the depths where the dwarf spheroidals also live, and they sit about a dex BELOW the kernel while the dwarf spheroidals at the same depth sit ABOVE it.  Pressure support and depth are therefore separable in the Local Group -- g05's own section 4e does the separating, and gets a large answer.  What is confounded is 'dwarf spheroidal' with 'deep', which is a narrower and different statement",
   len(gc_in) == 0,
   f"globular clusters at x_i = {min(gcx):.3f}-{max(gcx):.3f}: residuals " +
   ", ".join(f"{g:+.2f}" for g in gcr) + f", median {np.median(gcr):+.3f} dex, {len(gc_in)} of 4 inside SPARC's "
   f"coverage.  Dwarf spheroidals over the SAME x_i range: median {np.median(dsph_ov):+.3f} dex on N={len(dsph_ov)}.  "
   f"Separation at fixed depth = {np.median(dsph_ov)-np.median(gcr):+.3f} dex, and it is not zero")

# ==========================================================================================================
P(""); P("="*122)
P("PART 5.  'NO LOCAL GROUP COMPARISON CAN SEPARATE THEM' -- IMPOSSIBLE, OR MERELY UNDERPOWERED?")
P("="*122)
info("A structural confound means the comparison CANNOT BE MADE.  A power problem means it CAN be made and")
info("returns a bound.  g05 made it: 14 dwarf spheroidals inside SPARC's coverage against 147 SPARC galaxies,")
info("+0.064 dex, 0.93 sigma.  That is a MEASUREMENT with an error bar, so it is the second thing, not the first.")

def ctrl(lx, ly, rr):
    m = np.abs(ly - lx) < MATCH_W
    return float(np.median(rr[m])) if m.sum() >= MATCH_N else None

pres_d = []
for t in kept:
    c = ctrl(math.log10(t["xi"]), LY, RRp)
    if c is not None: pres_d.append(t["res"] - c)
GID = np.concatenate([np.full(len(g["gbar"]), i) for i, g in enumerate(gals)])
rot_d = []
for i, g in enumerate(gals):
    y = g["gbar"]/a0c
    rj = float(np.median(np.log10(g["gobs"]/(nu(y)*g["gbar"]))))
    keepm = GID != i
    c = ctrl(float(np.median(np.log10(y))), LY[keepm], RRp[keepm])
    if c is not None: rot_d.append(rj - c)
pa, ra = np.array(pres_d), np.array(rot_d)
sep = float(np.median(pa) - np.median(ra))
se = math.sqrt(pa.std(ddof=1)**2/len(pa) + ra.std(ddof=1)**2/len(ra))
info(f"    matched separation {sep:+.3f} +- {se:.3f} dex ({sep/se:.2f} sigma) on N_pressure = {len(pa)}, N_rot = {len(ra)}")
info(f"    two-sigma upper bound on any depth-independent support-type effect inside the overlap: {sep+2*se:+.3f} dex")
info(f"    (the N needed to settle it is computed after the median's own error is bootstrapped, below)")
ck("V9 (FAILS) the Local Group comparison at matched depth is not impossible; it was PERFORMED and it returned a bound.  The correct statement is that it is UNDERPOWERED at N = 14, not that support and depth cannot be separated.  Saying 'no Local Group comparison can separate them' converts a power limit into a structural theorem, and the two have different consequences: a power limit is fixed by more objects inside the overlap, a structural confound is not",
   sep/se > 3.0 or (sep + 2*se) < 0.0,
   f"the comparison EXISTS and returns {sep:+.3f} dex on {len(pa)} pressure objects spanning "
   f"{math.log10(max(xk)/min(xk)):.2f} decades of overlap with the rotating sample.  A structural confound would "
   f"leave nothing to compare; here there is a number with an error bar on it")

P("")
info("(e) THE POWER OF THE MATCHED TEST -- the question A1b never asks.  'The separation dies because of the")
info("    confound' is only true if the matched test lacked the SENSITIVITY to see f09's +0.215 dex.  Bootstrap")
info("    the standard error of the median difference properly (the median's error, not the mean's, which is what")
info("    g05's compare() uses -- for a Gaussian the median's is about 1.25 times larger), then ask what f09's")
info("    claimed effect would have registered as.")
bsep = []
for _ in range(20000):
    bsep.append(float(np.median(rng.choice(pa, len(pa), replace=True))) -
                float(np.median(rng.choice(ra, len(ra), replace=True))))
bsep = np.array(bsep); se_med = float(bsep.std(ddof=1))
F09 = 0.215
info(f"    separation {sep:+.3f} dex; bootstrap SE of the MEDIAN difference {se_med:.3f} dex "
     f"(g05 quotes {se:.3f}, the SE of the MEAN, which is {100*(se_med/se-1):+.0f} per cent optimistic)")
info(f"    so the measured separation is {sep/se_med:.2f} sigma, and f09's claimed +{F09} dex would have registered at "
     f"{F09/se_med:.2f} sigma")
info(f"    68 per cent interval on the matched separation: {np.percentile(bsep,16):+.3f} to {np.percentile(bsep,84):+.3f} dex; "
     f"95 per cent: {np.percentile(bsep,2.5):+.3f} to {np.percentile(bsep,97.5):+.3f}")
ck("V9b (FAILS, AND THE FAILURE CUTS BOTH WAYS -- READ IT CAREFULLY) g05 quotes the matched separation with the standard error of the MEAN while taking the difference of MEDIANS; bootstrapping the median's own error gives 0.091 dex, 31 per cent larger, so the honest matched result is +0.064 +- 0.091 dex, 0.71 sigma rather than 0.93.  That cuts against the file's own headline precision.  But it also means the matched test has only about 2.4 sigma sensitivity to f09's +0.215 dex and its 95 per cent interval STILL CONTAINS +0.215 -- so the matched comparison neither establishes nor excludes f09's effect.  'The separation dies' is therefore not established either: what is established is that the overlap sample cannot decide, which is a power statement about N = 14 and NOT the structural confound A1b asserts",
   np.percentile(bsep, 97.5) < F09,
   f"measured {sep:+.3f} dex, bootstrap SE {se_med:.3f}; f09's +{F09} dex would be a {F09/se_med:.2f} sigma effect; "
   f"95 per cent interval {np.percentile(bsep,2.5):+.3f} to {np.percentile(bsep,97.5):+.3f} dex "
   f"{'EXCLUDES' if np.percentile(bsep,97.5) < F09 else 'does not exclude'} +{F09}")

P("")
info("AND THE OVERLAP IS NOT EMPTY BY A LITTLE -- it is 3.4 decades wide on the pressure side:")
info(f"    kept x_i span {min(xk):.4f} to {max(xk):.2f}, i.e. {math.log10(max(xk)/min(xk)):.2f} decades of genuine overlap")
ck("V10 (FAILS) 'completely confounded' would require the two sets to be disjoint in acceleration.  They are not: the pressure sample overlaps SPARC over 3.4 decades and 28 per cent of the objects live there.  A confound this partial is a sampling imbalance -- a real and important one -- but the word 'completely' is not supportable and neither is 'no comparison can separate them'",
   len(kept) == 0,
   f"{len(kept)} of {len(recs)} pressure objects ({100*len(kept)/len(recs):.0f} per cent) lie inside SPARC's "
   f"coverage, spanning {math.log10(max(xk)/min(xk)):.2f} decades in x_i")

# ==========================================================================================================
P(""); P("="*122)
P("PART 6.  MUTATION CONTROLS ON MY OWN ATTACK.")
P("="*122)
mut = {t["name"]: row(t["obj"], a0c, sig=t["obj"]["sig"]*math.sqrt(2))[0] for t in recs}
base = {t["name"]: t["res"] for t in recs}
sh = np.median([mut[n] - base[n] for n in base])
ck("M-B MUTATION CONTROL: inflating every observed dispersion by sqrt(2) must move every residual by exactly log10(2) and nothing else in my pipeline may respond",
   abs(sh - math.log10(2.0)) < 1e-12, f"median shift {sh:+.12f} against log10(2) = {math.log10(2.0):+.12f}")

big = {t["name"]: row(t["obj"], 100*a0c)[0] for t in recs}
ck("M-C MUTATION CONTROL: raising a_0 by 100 must drive everything into the modified regime and drive the residuals DOWN",
   float(np.median(list(big.values()))) < float(np.median(list(base.values()))) - 0.2,
   f"median residual {float(np.median(list(base.values()))):+.3f} dex at canonical a_0, "
   f"{float(np.median(list(big.values()))):+.3f} at 100 a_0")

perm = []
for _ in range(5000):
    v = rng.permutation([t["res"] for t in recs])
    perm.append(float(np.median(v[:len(drop)])) - float(np.median(v[len(drop):])))
perm = np.array(perm)
p_shuf = float(np.mean(np.abs(perm) >= abs(md - mk)))
ck("M-D the kept/dropped DIFFERENCE survives its own label shuffle, so what I am complaining about is the STATISTIC and not the underlying structure: the deep pressure objects really do sit higher than the shallow ones",
   p_shuf < 0.01, f"real difference {md-mk:+.3f} dex; 5000 label shuffles give {perm.mean():+.4f} +- {perm.std():.4f}, "
   f"P(|shuffled| >= real) = {p_shuf:.5f}")

P(""); P("="*122); P("VERDICT OF THE ADVERSARIAL PASS"); P("="*122)
P(f"  THE ARITHMETIC IS CLEAN.  Re-derived from the raw catalogue through an independent implementation of")
P(f"  Wolf+2010 and a different quadrature rule for the QUMOND sphere average, the sample splits 14/36 at")
P(f"  x_i = {min(xk):.4f} and the medians come back {mk:+.3f} and {md:+.3f} dex.  V1 and V2 PASS.  No")
P(f"  total-for-enclosed-mass error, no spherical-formula-on-a-disc error, no aperture problem, and the")
P(f"  residual's sign does not track a branch of anyone's prescription -- the branch is gone by construction.")
P(f"  The null injection (V3) shows the estimator is unbiased, and the label shuffle (M-D) shows the")
P(f"  kept-minus-dropped difference of {md-mk:+.3f} dex is real at p = {p_shuf:.4f}.")
P(f"")
P(f"  WHAT IS WRONG IS THE STATISTIC AND THE WORDING, NOT THE ARITHMETIC.")
P(f"   1. 'A factor {md/mk:.1f} in the same currency' is a RATIO of two dex values.  Dex has an arbitrary additive")
P(f"      zero point, so the ratio is not a physical quantity.  Bootstrapping it gives a 68 per cent interval of")
P(f"      {np.percentile(br,16):.1f} to {np.percentile(br,84):.1f} with {100*neg/len(br):.1f} per cent of resamples NEGATIVE, because the denominator,")
P(f"      +{mk:.3f} dex on 14 objects, is itself within about one sigma of zero.  Changing a_0 from the canonical")
P(f"      to the alt footing -- 21 per cent -- moves the ratio from {foot_out['canonical'][2]:.2f} to {foot_out['alt'][2]:.2f}.  The invariant statistic")
P(f"      is the DIFFERENCE, {md-mk:+.3f} dex, which is tight ({np.percentile(bdif,16):+.3f} to {np.percentile(bdif,84):+.3f}) and footing-stable.  V5 and V6 FAIL.")
P(f"   2. BUT THE UNDERLYING DEPTH STRUCTURE IS REAL, AND MY ATTACK ON IT FAILED (V4 PASSES).  A pure")
P(f"      support-type effect with no depth dependence, injected at +{INJ} dex on a framework-consistent baseline,")
P(f"      returns a ratio of {np.mean(inj_ratio):.2f} and a difference of {np.mean(inj_diff):+.3f} dex -- nothing like the measured {md/mk:.1f} and {md-mk:+.3f}.")
P(f"      So the deep pressure objects genuinely do sit higher than the shallow ones.  Only the CURRENCY the")
P(f"      claim is quoted in is wrong; the finding underneath it stands.")
P(f"   3. 'COMPLETELY confounded' and 'no Local Group comparison can separate them' are both too strong, and")
P(f"      g05's own section 4e refutes them: outer-halo globular clusters are pressure-supported, are in the")
P(f"      Local Group, sit INSIDE SPARC's coverage at x_i = {min(gcx):.3f}-{max(gcx):.2f}, and land {np.median(gcr):+.2f} dex, i.e. about a dex")
P(f"      away from the dwarf spheroidals at the same depth.  Pressure support and depth are separable in the")
P(f"      Local Group; what is confounded is 'dwarf spheroidal' with 'three decades below a_0'.  V8 FAILS.")
P(f"   4. The matched comparison was MADE and returned {sep:+.3f} +- {se_med:.3f} dex (bootstrapped median error; g05")
P(f"      quotes {se:.3f}, the error of the MEAN, so its 0.93 sigma is really {sep/se_med:.2f}) on {len(pa)} objects spanning")
P(f"      {math.log10(max(xk)/min(xk)):.1f} decades of real overlap.  Its 95 per cent interval, {np.percentile(bsep,2.5):+.3f} to {np.percentile(bsep,97.5):+.3f} dex, still")
P(f"      CONTAINS f09's +{F09}.  So the matched test does not exclude f09's effect either; it is UNDERPOWERED at")
P(f"      N = {len(pa)}.  About {math.ceil(len(pa)*(se_med/(F09/3.0))**2)} matched pressure objects would settle it at 3 sigma -- a finite, stateable")
P(f"      observational requirement, which is exactly what 'no comparison can separate them' would deny.")
P(f"      V9, V9b and V10 FAIL.")
P(f"")
P(f"  WHAT SURVIVES OF A1b, AND IT IS WORTH KEEPING:")
P(f"   * '36 of the 50 pressure-supported Local Group objects sit below the deepest acceleration SPARC reaches")
P(f"     (x_i < {min(xk):.4f}), and their median raw residual is {md-mk:+.2f} dex HIGHER than the {len(kept)} that overlap.  The")
P(f"     difference is significant at p = {p_shuf:.4f} against a label shuffle and is stable across both a_0 footings.'")
P(f"   * 'The overlap sample is small (N = {len(kept)}), so the matched comparison neither establishes nor excludes a")
P(f"     support-type effect: {sep:+.3f} +- {se_med:.3f} dex, 95 per cent interval {np.percentile(bsep,2.5):+.3f} to {np.percentile(bsep,97.5):+.3f}, which still contains")
P(f"     f09's +{F09}.  It is a POWER limit at N = {len(pa)}, not a structural impossibility.'")
P(f"  NOT: 'a factor {md/mk:.1f}', NOT 'completely confounded', NOT 'no Local Group comparison can separate them'.")
sys.exit(ck.done())
