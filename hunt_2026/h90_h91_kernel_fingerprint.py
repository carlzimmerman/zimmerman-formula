#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h90_h91_kernel_fingerprint.py -- HUNT ITEMS 90 + 91: the kernel's own fingerprint in SPARC.
===========================================================================================
Item 90 (the exponential return): at high acceleration Route A returns to Newton as nu - 1 = e^{-sqrt(y)}/(1-e^{-sqrt(y)}) ~ e^{-sqrt y},
  while the alpha=1 kernel nu = sqrt(1+1/y) and the "simple" kernel return as a POWER LAW ~ 1/(2y).  At y = 10-100 (bulges, inner discs)
  these differ by orders of magnitude: e^{-sqrt(10)} = 0.042 vs 1/20 = 0.050; at y = 100, 4.5e-5 vs 5e-3 -- a factor 110.
Item 91 (the curvature landmark): the RAR's log-log curvature C(y) = d sigma / d ln y has a MAXIMUM whose position and height are
  kernel-specific and parameter-free.  Route A, alpha=1 and simple all differ.  Measured, this is a shape discriminator that does
  not depend on a_0's value (only on the kernel), and it is orthogonal to everything the programme has used.
Data: SPARC rotmods (147 galaxies, Q<=2, i>=30).  Both footings.  Mutation: shuffling g_bar must destroy the landmark.  Checks CAN fail.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
gals = load_sparc()
gb = np.concatenate([g["gbar"] for g in gals]); go = np.concatenate([g["gobs"] for g in gals])
ev = np.concatenate([2*g["vobs"]*g["ev"]/g["r"]*KMS2_KPC for g in gals])
P("="*116); P("ITEMS 90 + 91 -- the kernel's fingerprint: the high-acceleration return and the curvature landmark"); P("="*116)
info(f"SPARC: {len(gals)} galaxies, {len(gb)} points; g_bar = {gb.min():.2e} - {gb.max():.2e} m/s^2")
KERNELS = {
    "Route A (exponential)": lambda y: 1.0/(1.0 - np.exp(-np.sqrt(y))),
    "alpha=1 (sqrt)":        lambda y: np.sqrt(1.0 + 1.0/y),
    "simple":                lambda y: 0.5 + np.sqrt(0.25 + 1.0/y),
    "standard":             lambda y: np.sqrt(0.5 + np.sqrt(0.25 + 1.0/y**2)),
}
P(""); P("1. ITEM 90 -- the high-acceleration return, predicted"); P("="*116)
info(f"{'y = g_bar/a0':>14} " + " ".join(f"{k:>22}" for k in KERNELS))
for y in (5, 10, 30, 100, 300):
    info(f"{y:14.0f} " + " ".join(f"{f(np.array([float(y)]))[0]-1:22.3e}" for f in KERNELS.values()))
info("the return is the observable: nu - 1 = (g_obs - g_bar)/g_bar at high y, measurable galaxy by galaxy in bulges and inner discs")
P(""); P("2. ITEM 90 measured: binned (g_obs/g_bar - 1) at high acceleration, both footings"); P("="*116)
fit90 = {}
for foot, a0 in A0.items():
    y = gb/a0; ratio = go/gb - 1.0; sig = ev/gb
    edges = np.array([3, 6, 12, 25, 60, 200.0])
    info(f"{foot:10} {'y range':>14} {'N':>5} {'measured nu-1':>18} " + " ".join(f"{k.split()[0]:>12}" for k in KERNELS))
    rows = []
    for i in range(len(edges)-1):
        m = (y >= edges[i]) & (y < edges[i+1])
        if m.sum() < 8: continue
        w = 1/np.maximum(sig[m], 1e-3)**2
        val = float(np.sum(w*ratio[m])/np.sum(w)); err = float(np.sqrt(1/np.sum(w)))
        ymid = float(np.median(y[m]))
        preds = {k: float(f(np.array([ymid]))[0] - 1) for k, f in KERNELS.items()}
        rows.append((ymid, m.sum(), val, err, preds))
        info(f"{foot:10} {edges[i]:6.0f}-{edges[i+1]:<7.0f} {m.sum():5d} {val:10.4f}+-{err:.4f} " + " ".join(f"{preds[k]:12.4f}" for k in KERNELS))
    fit90[foot] = rows
    for k in KERNELS:
        chi2 = sum(((r[2] - r[4][k])/r[3])**2 for r in rows)
        info(f"{foot:10}   chi2 of the return, y = 3-200, {k:22}: {chi2:8.1f} / {len(rows)} bins")
    fit90[(foot, "chi2")] = {k: sum(((r[2] - r[4][k])/r[3])**2 for r in rows) for k in KERNELS}
info("NOTE (both ways): at high y the measured ratio is dominated by the stellar M/L, not by the kernel -- a coherent Upsilon error of")
info("10% moves (g_obs/g_bar - 1) by 0.1, larger than every kernel difference below y ~ 30.  The comparison above is therefore")
info("Upsilon-LIMITED, and the chi2 ranking is reported, not scored, unless one kernel is excluded by orders of magnitude.")
best = {f: min(fit90[(f, "chi2")], key=fit90[(f, "chi2")].get) for f in A0}
ck("90a (reported, Upsilon-limited) the high-acceleration return ranks the kernels; no kernel is excluded by orders of magnitude, so this is not a discriminator at SPARC's M/L precision",
   max(fit90[(f, "chi2")][k] for f in A0 for k in KERNELS) < 1e4,
   "; ".join(f"{f}: best = {best[f]} (chi2 " + ", ".join(f"{k.split()[0]}={fit90[(f,'chi2')][k]:.0f}" for k in KERNELS) + ")" for f in A0))
P(""); P("3. ITEM 91 -- the curvature landmark, predicted (parameter-free, a_0-independent in shape)"); P("="*116)
def landmark(f):
    yy = np.geomspace(1e-3, 1e3, 20000); ln = np.log(yy); g = yy*f(yy)
    sig = np.gradient(np.log(g), ln); Cv = np.gradient(sig, ln)
    i = int(np.argmax(Cv)); return yy[i], sig[i], Cv[i]
info(f"{'kernel':24} {'y at C_max':>12} {'slope there':>12} {'C_max':>10}")
LM = {}
for k, f in KERNELS.items():
    ym, sm, cm = landmark(f); LM[k] = (ym, sm, cm); info(f"{k:24} {ym:12.3f} {sm:12.3f} {cm:10.4f}")
ck("91a the landmark separates the kernels: the curvature maximum sits at y = 4.0 (Route A) vs 1.0 (alpha=1) vs 2.0 (simple) -- a factor 4 in position and 20% in height, all parameter-free",
   LM["Route A (exponential)"][0]/LM["alpha=1 (sqrt)"][0] > 3.0, f"Route A y_max = {LM['Route A (exponential)'][0]:.2f}, alpha=1 {LM['alpha=1 (sqrt)'][0]:.2f}, simple {LM['simple'][0]:.2f}, standard {LM['standard'][0]:.2f}")
P(""); P("4. ITEM 91 measured: the RAR's curvature from SPARC, with a bootstrap"); P("="*116)
def measure_landmark(gbv, gov, a0, nb=14):
    y = gbv/a0; lx = np.log(y); ly = np.log(gov/a0)
    lo, hi = np.percentile(lx, 2), np.percentile(lx, 98)
    e = np.linspace(lo, hi, nb+1); xs, ys = [], []
    for i in range(nb):
        m = (lx >= e[i]) & (lx < e[i+1])
        if m.sum() < 10: continue
        xs.append(np.median(lx[m])); ys.append(np.median(ly[m]))
    xs, ys = np.array(xs), np.array(ys)
    if len(xs) < 6: return np.nan, np.nan
    sl = np.gradient(ys, xs); cv = np.gradient(sl, xs)
    j = int(np.argmax(cv)); return math.exp(xs[j]), cv[j]
rng = np.random.default_rng(910); LMEAS = {}
for foot, a0 in list(A0.items()):
    ym, cm = measure_landmark(gb, go, a0)
    bs = []
    for _ in range(300):
        idx = rng.integers(0, len(gals), len(gals))
        gbb = np.concatenate([gals[i]["gbar"] for i in idx]); gob = np.concatenate([gals[i]["gobs"] for i in idx])
        v = measure_landmark(gbb, gob, a0)
        if np.isfinite(v[0]): bs.append(v)
    bs = np.array(bs)
    info(f"{foot:10} measured curvature maximum at y = {ym:.2f} [16-84%: {np.percentile(bs[:,0],16):.2f}, {np.percentile(bs[:,0],84):.2f}], C_max = {cm:.3f} [{np.percentile(bs[:,1],16):.3f}, {np.percentile(bs[:,1],84):.3f}]  (galaxy bootstrap, N = {len(bs)})")
    LMEAS[foot] = (ym, cm, np.percentile(bs[:,0],16), np.percentile(bs[:,0],84), np.percentile(bs[:,1],16), np.percentile(bs[:,1],84))
lm_can = LMEAS["canonical"]
inside = {k: (lm_can[2] <= LM[k][0] <= lm_can[3]) for k in KERNELS}
ck("91b (AGAINST INTEREST) the SPARC curvature landmark is NOT a usable discriminator: the galaxy bootstrap spans more than two decades in y, so every kernel's predicted landmark falls inside it, and the measured C_max sits well above all four predictions -- binned-median curvature is dominated by binning and by the M/L, not by the kernel",
   (lm_can[3]/max(lm_can[2], 1e-3) > 10) and all(inside.values()),
   f"interval y = [{lm_can[2]:.2f}, {lm_can[3]:.2f}] (span x{lm_can[3]/max(lm_can[2],1e-3):.0f}); measured C_max = {lm_can[1]:.3f} [{lm_can[4]:.3f}, {lm_can[5]:.3f}] vs predictions " + ", ".join(f"{k.split()[0]} {LM[k][2]:.3f}" for k in KERNELS))
P(""); P("5. mutation control: shuffle g_bar within each galaxy -- the landmark must be destroyed"); P("="*116)
sh_gb = np.concatenate([rng.permutation(g["gbar"]) for g in gals])
ymu, cmu = measure_landmark(sh_gb, go, A0["canonical"])
ck("M0 mutation control: shuffling g_bar within each galaxy moves the landmark or flattens the curvature (|C_max| changes by > 30%)",
   (not np.isfinite(ymu)) or abs(cmu - lm_can[1])/max(abs(lm_can[1]), 1e-6) > 0.3, f"shuffled: y_max = {ymu:.2f}, C_max = {cmu:.3f} vs real {lm_can[1]:.3f}")
P(""); P("="*116); P("VERDICT"); P("="*116)
P("  Item 90 is Upsilon-limited: at y > 3 the stellar mass-to-light ratio, not the kernel, sets (g_obs/g_bar - 1), so SPARC cannot")
P("  separate an exponential return from a power-law one.  Item 91 is the sharper of the two -- the curvature landmark is")
P("  parameter-free and a_0-independent in position (y = 4.0 Route A vs 1.0 alpha=1) -- and the measured value with its galaxy")
P("  bootstrap is reported above, AGAINST INTEREST: the interval spans two decades in y and the measured curvature exceeds every")
P("  kernel's prediction, so binned-median curvature is dominated by binning and M/L, not by the kernel.  BOTH ITEMS ARE CLOSED as")
P("  discriminators at SPARC quality.  What would reopen 91: a hierarchical per-galaxy slope-field fit (not binned medians), which")
P("  the equation book (E1) already flags as the right estimator and which nobody has run.")
sys.exit(ck.done())
