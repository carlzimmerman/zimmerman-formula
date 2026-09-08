#!/usr/bin/env python3
"""
L5 -- can the cluster residual be a LONG-RANGE ENHANCEMENT OF G rather than a MOND kernel?
==========================================================================================
L2 (this lane, 2026-09-08) inverted the static law on the corrected X-COP profiles and found that what
clusters require is NOT an interpolation function: the required boost is Delta_req ~ 5.5 s^0.81, i.e.
J_Y ~ 0.13-0.18 nearly constant, i.e. g_obs ~ 6.9 g_N -- a CONSTANT RESCALING OF G, extra mass tracing
the baryons.  Its log-slope sits 3.9 sigma above the 1/2 that any kernel with a deep-MOND limit is
capped at, and at the same accelerations clusters demand 2.2-5.1x the boost galaxies are measured to
have (worst |z| = 13, footing-independent).

A constant enhancement of G at large radii and none at small radii is exactly what ONE structure gives:
a long-range force, i.e. a scalar of finite range lambda (Yukawa).  That is the constructive reading of
L2's negative, and it has not been run in this repository as a script.  This is that test.

THE MODEL (two parameters, no kernel).  For a source of enclosed baryonic mass M_b(r),
    g(r) = G_bare M_b(r)/r^2 * f(r/lambda),   f(x) = 1 + alpha (1 + x) e^-x,
the standard Yukawa force with range lambda and strength alpha.  Newton's constant is MEASURED locally,
at r << lambda (Solar System, laboratory), so
    G_local = G_bare f(0) = G_bare (1 + alpha),
and the OBSERVABLE enhancement relative to the locally measured constant is
    R(r) = f(r/lambda) / (1 + alpha),   R(0) = 1,   R(inf) = 1/(1 + alpha).
alpha < 0 therefore gives MORE gravity at large r than the locally measured G would predict, which is
the sign clusters need.  R(inf) = 6.9 requires alpha = -0.855.

THE UNAVOIDABLE PRICE, and the point of this script.  The homogeneous background is the r -> infinity
limit: a scalar of range lambda << horizon is Yukawa-suppressed on cosmological scales and does not
propagate there, so the Friedmann equation runs on G_bare, while every laboratory measurement returns
G_local.  Hence
    G_cosmo / G_local = 1 / (1 + alpha) = R(inf),
the SAME factor that fixes the clusters.  Big-bang nucleosynthesis measures the expansion rate at
T ~ 1 MeV through the helium abundance, H propto sqrt(G rho), and bounds G_BBN/G_0.  So the cluster
requirement and the BBN bound are the same number and cannot be decoupled.

  L0 [control]   the fitter recovers injected (alpha, lambda) from synthetic Yukawa data to 5%;
  L1 [shape]     a single (alpha, lambda) reproduces the corrected X-COP enclosed-mass ratios over
                 40-1000 kpc to better than 0.15 dex rms -- i.e. the SHAPE of the residual is that of a
                 finite-range force at all (if this fails, the route dies on shape alone);
  L2c [galaxies] the fitted transition leaves the radial acceleration relation alone: the predicted
                 enhancement at SPARC radii (5-100 kpc) stays inside the relation's observed 0.11 dex
                 scatter (Lelli, McGaugh & Schombert 2017);
  L3c [BBN]      the implied G_cosmo/G_local satisfies the conservative BBN bound |G/G_0 - 1| < 0.2;
  L4c [verdict]  the route survives all three of shape, galaxies and BBN simultaneously.
Both a0 footings are carried, though note that the REQUIRED enhancement is a ratio of measured
accelerations and is therefore footing-independent (L2's C5); the footing enters only the comparison
with the framework's own kernel.
FAIL marks a requirement the route does not meet.  A PASS on L4c would be a live mechanism for the
cluster residual and would be the most valuable outcome in this lane.
"""
import numpy as np, math, json, os, sys
from scipy.optimize import curve_fit
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kpc = 3.0857e19
print("=" * 118); print("L5 -- is the cluster residual a long-range enhancement of G (a finite-range force) rather than a kernel?"); print("=" * 118, flush=True)

# ---------------- the Yukawa observable ----------------
def R_of(r_kpc, alpha, lam_kpc):
    """enhancement relative to the LOCALLY measured G: R = f(r/lambda)/(1+alpha)."""
    x = np.asarray(r_kpc, float)/lam_kpc
    return (1.0 + alpha*(1.0 + x)*np.exp(-x))/(1.0 + alpha)

# ---------------- L0: control on synthetic data ----------------
r_syn = np.geomspace(40, 1000, 12); a_true, l_true = -0.855, 300.0
R_syn = R_of(r_syn, a_true, l_true)*(1 + 0.0)          # noiseless
p0 = [-0.5, 200.0]
try:
    popt, _ = curve_fit(lambda r, a, l: R_of(r, a, l), r_syn, R_syn, p0=p0, maxfev=40000,
                        bounds=([-0.999, 10.0], [-1e-4, 5000.0]))
    err_a = abs(popt[0]/a_true - 1); err_l = abs(popt[1]/l_true - 1); ok0 = err_a < 0.05 and err_l < 0.05
except Exception as e:
    popt = [float('nan'), float('nan')]; err_a = err_l = float('nan'); ok0 = False
print(f"    L0: injected alpha = {a_true}, lambda = {l_true:.0f} kpc  ->  recovered {popt[0]:.4f}, {popt[1]:.1f} kpc")
check("L0 [control] the fitter recovers injected (alpha, lambda) from synthetic Yukawa data to 5%", ok0,
      f"errors {100*err_a:.2f}% and {100*err_l:.2f}%")

# ---------------- the corrected cluster requirement ----------------
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
ROWS = CLJ["rows"]; RADII = np.array(CLJ["radii_kpc"], float); A0 = CLJ["a0_m_s2"]
keys = sorted(ROWS[0].keys())
print(f"    inputs: {len(ROWS)} corrected X-COP rows, radii {RADII.astype(int).tolist()} kpc, footings {A0}")
print(f"            row fields: {keys}")
# required enhancement R_req = g_HSE / g_baryon, per row (footing-independent: a0 cancels)
def rowval(rw, *names):
    for n in names:
        if n in rw: return rw[n]
    return None
REQ = {}
for rw in ROWS:
    gh = rowval(rw, "g_hse_over_a0", "g_hse", "g_obs_over_a0"); gb = rowval(rw, "g_baryon_over_a0", "g_bar_over_a0", "g_baryon")
    rr = rowval(rw, "radius_kpc", "r_kpc", "radius"); foot = rowval(rw, "footing", "foot") or "canonical"
    if gh is None or gb is None or rr is None or gb == 0: continue
    REQ.setdefault(foot, []).append((float(rr), float(gh)/float(gb)))
for foot in REQ: REQ[foot] = np.array(sorted(REQ[foot]))
foots = sorted(REQ)
for foot in foots:
    A = REQ[foot]; rb = np.unique(A[:, 0])
    med = [np.median(A[A[:, 0] == r][:, 1]) for r in rb]
    print(f"    required enhancement R_req = g_HSE/g_bar, {foot}: " + ", ".join(f"{int(r)}kpc {m:.2f}" for r, m in zip(rb, med)), flush=True)

# ---------------- L1: does a single (alpha, lambda) reproduce the shape? ----------------
FIT = {}
for foot in foots:
    A = REQ[foot]; rb = np.unique(A[:, 0]); med = np.array([np.median(A[A[:, 0] == r][:, 1]) for r in rb])
    try:
        popt, _ = curve_fit(lambda r, a, l: R_of(r, a, l), rb, med, p0=[-0.8, 300.0], maxfev=60000,
                            bounds=([-0.999, 10.0], [-1e-4, 5000.0]))
        pred = R_of(rb, *popt); rms = float(np.sqrt(np.mean((np.log10(pred) - np.log10(med))**2)))
    except Exception as e:
        popt = [float('nan'), float('nan')]; pred = med*0 + float('nan'); rms = float('inf')
    FIT[foot] = dict(alpha=popt[0], lam=popt[1], rms=rms, Rinf=1.0/(1.0 + popt[0]), rb=rb, med=med, pred=pred)
    print(f"    L1 {foot}: alpha = {popt[0]:.4f}, lambda = {popt[1]:.0f} kpc, R(inf) = G_cosmo/G_local = {1/(1+popt[0]):.2f}, fit rms = {rms:.3f} dex")
    print(f"        required : " + ", ".join(f"{m:.2f}" for m in med))
    print(f"        Yukawa   : " + ", ".join(f"{p:.2f}" for p in pred), flush=True)
check("L1 [shape] a single (alpha, lambda) reproduces the corrected cluster enhancement over 40-1000 kpc to better than 0.15 dex rms",
      all(FIT[f]["rms"] < 0.15 for f in foots), ", ".join(f"{f} {FIT[f]['rms']:.3f} dex" for f in foots))

# ---------------- L2c: the galaxies ----------------
RAR_SCATTER = 0.11                                   # dex, Lelli, McGaugh & Schombert 2017
GAL_R = np.array([5.0, 10.0, 30.0, 100.0])
gal = {}
for foot in foots:
    dev = np.log10(R_of(GAL_R, FIT[foot]["alpha"], FIT[foot]["lam"]))
    gal[foot] = dev
    print(f"    L2c {foot}: predicted RAR offset at r = 5, 10, 30, 100 kpc = " + ", ".join(f"{d:+.3f}" for d in dev) + f" dex (observed scatter {RAR_SCATTER} dex)")
check("L2c [galaxies] the fitted transition leaves the radial acceleration relation inside its observed 0.11 dex scatter at every SPARC radius",
      all(np.all(np.abs(gal[f]) < RAR_SCATTER) for f in foots),
      ", ".join(f"{f} max {np.max(np.abs(gal[f])):.3f} dex at {GAL_R[int(np.argmax(np.abs(gal[f])))]:.0f} kpc" for f in foots))

# ---------------- L3c: BBN ----------------
BBN_TOL = 0.20                                        # conservative |G_BBN/G_0 - 1| bound
bbn = {f: FIT[f]["Rinf"] for f in foots}
for foot in foots:
    Rinf = bbn[foot]; print(f"    L3c {foot}: G_cosmo/G_local = {Rinf:.2f}  ->  expansion rate at BBN up by sqrt = {math.sqrt(Rinf):.2f}x  (bound |G/G0 - 1| < {BBN_TOL})")
check("L3c [BBN] the implied cosmological Newton constant satisfies the conservative BBN bound |G/G_0 - 1| < 0.2",
      all(abs(bbn[f] - 1) < BBN_TOL for f in foots),
      ", ".join(f"{f} G_cosmo/G_local = {bbn[f]:.2f} ({abs(bbn[f]-1)/BBN_TOL:.0f}x the bound)" for f in foots))
check("L4c [verdict] the long-range-force route survives shape, galaxies and BBN simultaneously",
      all(FIT[f]["rms"] < 0.15 for f in foots) and all(np.all(np.abs(gal[f]) < RAR_SCATTER) for f in foots) and all(abs(bbn[f] - 1) < BBN_TOL for f in foots),
      "the cluster requirement and the cosmological Newton constant are the SAME number, R(inf); they cannot be decoupled within a single-Yukawa force")
print("\n  what this does and does not close: it closes a SINGLE finite-range force of fixed strength, which is the minimal"
      "\n  realisation of L2's 'constant rescaling of G'.  It does NOT close a screened/chameleon-type force whose strength"
      "\n  depends on the local density or potential -- there the cosmological and cluster values are decoupled by construction,"
      "\n  and that is a different model with a new function, not this one.  Recorded as the adjacent door, untested here.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
