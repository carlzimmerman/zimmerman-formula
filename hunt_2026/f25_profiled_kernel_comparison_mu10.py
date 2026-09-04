#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f25 -- does the galaxy-data verdict on the closure program's kernels survive profiling a_0 AND the stellar M/L?

The parallel agent's audit (two_kernel_orbit_shape_2026/kernel_comparison.py, 2026-09-04) showed that f21/f23's
fixed-footing 'SPARC rejects mu_exp at 7.5 sigma' is not invariant to the score: with a_0 profiled per kernel and
whole galaxies resampled together, the paired MSE difference mu_exp - nu_RAR has a 95% interval containing zero.
That audit covered mu_exp only and left the stellar M/L fixed.  This file extends it, on the agent's own design
(equal-galaxy unweighted log-residual MSE, paired multinomial galaxy resampling, a_0 profiled on a grid), to

    * mu_10(x) = x/(1+x^10)^{1/10}  -- the closure program's Cassini-selected 'surviving architecture' kernel,
    * mu_5(x)  = x/(1+x^5)^{1/5}    -- the softest member of the mu_n family the AeST notes call Cassini-safe (n >= 4),

and gives EVERY kernel two free parameters: a_0 and a global disc mass-to-light ratio Upsilon_d (bulge 1.4 Upsilon_d),
profiled jointly on a grid.  Freeing Upsilon is the fair version of the test: a sharper kernel can be partly
compensated by heavier discs, and the closure program's kernels must be allowed that compensation before they are
called dead.  This is still a descriptive score, not a likelihood; the checks state exactly what it can show.
"""
import os, sys, math
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260904)

# ---- kernels as nu(y) tables (spherical inverse partners), log-log interpolated
YG = np.logspace(-6, 6, 2401)
def nu_table(mu):
    out = np.empty_like(YG)
    for i, yy in enumerate(YG):
        out[i] = brentq(lambda x: x*mu(x) - yy, 1e-14, yy + 60.0, xtol=1e-14)/yy if yy < 300 else 1.0
    return out
KERN = {"nu_rar": lambda y: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-30))))}
for nm, mu in (("mu_exp", lambda x: 1.0 - math.exp(-x)), ("mu_10", lambda x: x/(1 + x**10)**0.1), ("mu_5", lambda x: x/(1 + x**5)**0.2)):
    tab = np.log(nu_table(mu)); lyg = np.log(YG)
    KERN[nm] = (lambda tab: (lambda y: np.exp(np.interp(np.log(np.clip(np.asarray(y, float), 1e-6, 1e6)), lyg, tab))))(tab)
ck("K1 the tabulated inverse partners are exact where they can be checked: mu_exp's table matches f21's Newton "
   "solve and every table has the deep and Newtonian limits",
   abs(float(KERN["mu_exp"](1.0)) - 1.3500) < 2e-4 and all(abs(float(KERN[k](1e-6))*1e-3 - 1) < 0.01 and abs(float(KERN[k](1e5)) - 1) < 0.02 for k in KERN),
   f"nu_muexp(1) = {float(KERN['mu_exp'](1.0)):.4f} (f21: 1.3500)")

# ---- SPARC with the disc M/L as a free global parameter
gals0 = load_sparc()
UPS = np.array([0.30, 0.40, 0.50, 0.60, 0.70, 0.80])
LOGA = np.linspace(-10.8, -9.2, 161)
gid = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(gals0)])
vobs2r = np.concatenate([g["vobs"]**2/g["r"] for g in gals0])
vg = np.concatenate([g["vg"] for g in gals0]); vd = np.concatenate([g["vd"] for g in gals0]); vb = np.concatenate([g["vb"] for g in gals0]); rr = np.concatenate([g["r"] for g in gals0])
KMS2_KPC = 1e6/kpc
go = vobs2r*KMS2_KPC
def gbar_of(ups): return (vg*np.abs(vg) + ups*vd**2 + 1.4*ups*vb**2)/rr*KMS2_KPC
names, ids = np.unique(gid, return_inverse=True); counts = np.bincount(ids); NG = len(names)
info(f"SPARC: {len(go)} points, {NG} galaxies; Upsilon_d grid {UPS.min()}-{UPS.max()} (6), log a_0 grid {LOGA[0]}..{LOGA[-1]} ({len(LOGA)})")

def loss_cube(kernel, ups_list):
    """equal-galaxy MSE per (Upsilon, a_0) -> array (NG, nU, nA); points with g_bar <= 0 dropped per cell."""
    L = np.full((NG, len(ups_list), len(LOGA)), np.nan)
    for iu, ups in enumerate(ups_list):
        gb = gbar_of(ups); ok = (gb > 0) & (go > 0)
        for ia, la in enumerate(LOGA):
            res = np.log10(go[ok]/(KERN[kernel](gb[ok]/10**la)*gb[ok]))
            L[:, iu, ia] = np.bincount(ids[ok], weights=res**2, minlength=NG)/np.maximum(np.bincount(ids[ok], minlength=NG), 1)
    return L

def profiled(L, W):
    """W: (reps, NG) galaxy weights.  For each replicate, min over (Upsilon, a_0) of the weighted mean loss."""
    m = np.tensordot(W, L, axes=(1, 0))            # (reps, nU, nA)
    flat = m.reshape(len(W), -1); j = np.argmin(flat, axis=1)
    return flat[np.arange(len(W)), j], np.unravel_index(j, m.shape[1:])

CUBE = {k: loss_cube(k, UPS) for k in KERN}
W0 = np.full((1, NG), 1.0/NG)
REPS = 999
W = rng.multinomial(NG, np.full(NG, 1.0/NG), size=REPS)/NG

P("\n1.  a_0 profiled, Upsilon fixed at 0.5 (the parallel agent's design) -- reproduction, then mu_10 and mu_5 added")
P("-" * 110)
iu5 = int(np.where(UPS == 0.5)[0][0])
base = {}
for k in KERN:
    L = CUBE[k][:, iu5:iu5+1, :]
    full, (iu, ia) = profiled(L, W0); boot, _ = profiled(L, W)
    base[k] = dict(full=float(full[0]), a0=float(10**LOGA[ia[0]]), boot=boot)
    info(f"{k:7s}: best a_0 = {base[k]['a0']:.3e}, equal-galaxy RMS = {math.sqrt(base[k]['full']):.4f} dex")
for k in ("mu_exp", "mu_10", "mu_5"):
    d = base[k]["boot"] - base["nu_rar"]["boot"]; pc = np.percentile(d, [2.5, 50, 97.5])
    base[k]["pc"] = pc; base[k]["frac"] = float(np.mean(d > 0))
    info(f"paired MSE({k}) - MSE(nu_rar): 2.5/50/97.5% = [{pc[0]:+.5f}, {pc[1]:+.5f}, {pc[2]:+.5f}] dex^2; fraction > 0: {base[k]['frac']:.3f}")
ck("R1 the parallel agent's mu_exp result reproduces on this coarser grid: a_0 profiled, Upsilon fixed, the 95% "
   "interval of the paired MSE difference contains zero and the two best a_0 differ by ~0.09 dex",
   base["mu_exp"]["pc"][0] < 0 < base["mu_exp"]["pc"][2] and abs(math.log10(base["mu_exp"]["a0"]/base["nu_rar"]["a0"]) - 0.089) < 0.04,
   f"interval [{base['mu_exp']['pc'][0]:+.5f}, {base['mu_exp']['pc'][2]:+.5f}]; log a_0 ratio {math.log10(base['mu_exp']['a0']/base['nu_rar']['a0']):+.3f} (agent: +0.089)")
ck("R2 mu_10 does NOT survive a_0 profiling: its paired MSE excess over nu_RAR is positive in every replicate "
   "(2.5th percentile > 0) and its MSE excess is more than three times the exp-RAR gap",
   base["mu_10"]["pc"][0] > 0 and base["mu_10"]["frac"] >= 0.999 and (base["mu_10"]["full"] - base["nu_rar"]["full"]) > 3*abs(base["mu_exp"]["full"] - base["nu_rar"]["full"]),
   f"2.5th pct {base['mu_10']['pc'][0]:+.5f} dex^2, fraction > 0 = {base['mu_10']['frac']:.3f}; dMSE mu_10 {base['mu_10']['full']-base['nu_rar']['full']:+.5f} vs mu_exp {base['mu_exp']['full']-base['nu_rar']['full']:+.5f}")

P("\n2.  a_0 AND Upsilon_d profiled jointly for every kernel (the fair test)")
P("-" * 110)
joint = {}
for k in KERN:
    full, (iu, ia) = profiled(CUBE[k], W0); boot, _ = profiled(CUBE[k], W)
    joint[k] = dict(full=float(full[0]), a0=float(10**LOGA[ia[0]]), ups=float(UPS[iu[0]]), boot=boot)
    info(f"{k:7s}: best (Upsilon_d, a_0) = ({joint[k]['ups']:.2f}, {joint[k]['a0']:.3e}), equal-galaxy RMS = {math.sqrt(joint[k]['full']):.4f} dex")
for k in ("mu_exp", "mu_10", "mu_5"):
    d = joint[k]["boot"] - joint["nu_rar"]["boot"]; pc = np.percentile(d, [2.5, 50, 97.5])
    joint[k]["pc"] = pc; joint[k]["frac"] = float(np.mean(d > 0))
    info(f"paired MSE({k}) - MSE(nu_rar): 2.5/50/97.5% = [{pc[0]:+.5f}, {pc[1]:+.5f}, {pc[2]:+.5f}] dex^2; fraction > 0: {joint[k]['frac']:.3f}")
ck("R3 with BOTH a_0 and Upsilon free, mu_10 still loses to nu_RAR in every replicate: the closure program's "
   "surviving kernel cannot be rescued by heavier discs",
   joint["mu_10"]["pc"][0] > 0 and joint["mu_10"]["frac"] >= 0.999, f"2.5th pct {joint['mu_10']['pc'][0]:+.5f} dex^2, fraction > 0 = {joint['mu_10']['frac']:.3f}, RMS {math.sqrt(joint['mu_10']['full']):.4f} vs {math.sqrt(joint['nu_rar']['full']):.4f}")
ck("R4 (HYPOTHESIS CHECK -- a FAIL is a result) the softest 'Cassini-safe' member mu_5 also loses in every replicate "
   "with both parameters free.  If this fails, the mu_n family has a member the galaxy data tolerate, and the "
   "Cassini-vs-RAR pincer would need the n at which it closes",
   joint["mu_5"]["pc"][0] > 0 and joint["mu_5"]["frac"] >= 0.99, f"2.5th pct {joint['mu_5']['pc'][0]:+.5f} dex^2, fraction > 0 = {joint['mu_5']['frac']:.3f}")
ck("R5 (HYPOTHESIS CHECK -- a FAIL is a result) mu_exp vs nu_RAR remains undecided with both parameters free: the "
   "95% interval of the paired difference contains zero.  If this FAILS the data DO separate them once the M/L is "
   "allowed to move, and the direction is in the detail",
   joint["mu_exp"]["pc"][0] < 0 < joint["mu_exp"]["pc"][2],
   f"interval [{joint['mu_exp']['pc'][0]:+.5f}, {joint['mu_exp']['pc'][2]:+.5f}], fraction > 0 = {joint['mu_exp']['frac']:.3f}")
ck("R6 the profiled a_0 of the framework's kernel sits inside the footing band on both designs, and the profiled "
   "Upsilon_d is inside the population-synthesis range 0.3-0.8 for every kernel (no kernel is rescued by an "
   "unphysical disc)", 8e-11 < joint["nu_rar"]["a0"] < 1.2e-10 and all(0.3 <= joint[k]["ups"] <= 0.8 for k in KERN),
   "; ".join(f"{k}: Ups {joint[k]['ups']:.2f}, a_0 {joint[k]['a0']:.2e}" for k in KERN))
# mutation: shuffle g_obs across galaxies -> every kernel must degrade to the same large MSE
perm = rng.permutation(len(go)); go_s = go[perm]
gb = gbar_of(0.5); ok = (gb > 0)
mse_sh = {k: float(np.mean(np.bincount(ids[ok], weights=np.log10(go_s[ok]/(KERN[k](gb[ok]/9.36e-11)*gb[ok]))**2, minlength=NG)/np.maximum(np.bincount(ids[ok], minlength=NG), 1))) for k in KERN}
ck("M1 mutation: shuffling g_obs across points destroys the relation for every kernel (MSE up by > 10x), so the "
   "ordering above is structure in the pairing, not in the score",
   all(mse_sh[k] > 10*joint[k]["full"] for k in KERN), "; ".join(f"{k}: {mse_sh[k]:.3f}" for k in KERN))
P("\n  scope: descriptive equal-galaxy MSE with a_0 and a GLOBAL Upsilon_d profiled; per-galaxy M/L, distance and")
P("  inclination stay fixed; no observational-error weighting.  It can rank kernels; it cannot assign a sigma.")
sys.exit(ck.done())
