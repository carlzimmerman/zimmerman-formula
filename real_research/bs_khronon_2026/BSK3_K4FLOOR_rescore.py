#!/usr/bin/env python3
"""
BSK3-K4 CORRECTIVE (2026-09-25): re-score BSK3's K4 dwarf check under the REGISTERED
Fig-10 reading.

BSK3_kiDS_dust_gate.py gated K4 as a mean-fit ("|log10 residual| < 0.25 dex AND
slope(log g_obs, log g_pred) in [0.85, 1.15]").  That conflicts with the programme's
registered deep-dwarf reading (equipartition-law-tests reference, section 2):

    "The mass law predicts g_lens/g_N = 1 + sqrt(a0/g_N) -- mass-independent.
     deep cut g_N < 0.3 a0.  If the median residual is POSITIVE, the zero-parameter
     law is the FLOOR: the free dust (the two-regime picture) carries the excess --
     report the excess factor as the result, do not tune."

Under that reading the law is a FLOOR: khronon dust (the free dust / the phantom) is
supposed to sit ABOVE g_N(1 + sqrt(a0/g_N)); a positive median residual is the
MECHANISM WORKING, with the excess factor as the result.  The correct checks are:

  F1 (floor)      signed median log10(g_obs/g_pred) >= 0 (khronon dust sits at or
                  above the phantom-law floor; negative would kill the dust reading)
  F2 (shape)      log-log slope of g_obs vs g_pred = 1 within 2 sigma (the excess
                  is a multiplicative factor, i.e. the phantom halo follows the
                  law's SHAPE; a slope far from 1 is a genuine shape failure)
  F3 (window)     the deep cut g_N < 0.3 a0 is applied and reported; the slope is
                  cov-weighted (Kirshner-style) with the committed BS3 conventions.

Supersedes K4 of BSK3_kiDS_dust_gate.py for the dwarf question; the BSK3 headline
(the khronon-dust KiDS gate FAIL, K1/K2 +373.7/+90.8) does not depend on K4 and
stands.  Either way the number is the result -- no tuning.
"""
import json, math, os

import numpy as np

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
LANE = "BSK3_K4FLOOR"
results = {"lane": LANE, "checks": {}, "numbers": {}}
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

G = 6.674e-11
MS = 1.989e30
KG_M2_PER_MSUN_PC2 = MS / (3.0857e16) ** 2


def P(*a):
    print(*a, flush=True)


def check(name, measured, ok, reading=""):
    results["checks"][name] = {"ok": bool(ok), "measured": str(measured)}
    P(f"[{'PASS' if ok else 'FAIL'}] {name}")
    P(f"       measured: {measured}")
    if reading:
        P(f"       reading: {reading}")


DF = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar",
                  "Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt")
DCF = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar",
                   "Fig-10_RAR-KiDS-isolated-dwarfs_covmatrix.txt")
d10 = np.genfromtxt(DF, comments="#")
gN10 = d10[:, 0]
ESD10 = d10[:, 1] / d10[:, 4]                      # h70 Msun/pc^2 (BS3 bias convention)
E10 = d10[:, 3] / d10[:, 4]
cv10 = np.genfromtxt(DCF, comments="#")
nb10 = len(gN10)
C10 = (cv10[:, 4] / cv10[:, 6]).reshape(nb10, nb10)
C10 = (C10 + C10.T) / 2
g_obs = 2 * math.pi * G * ESD10 * KG_M2_PER_MSUN_PC2     # B21 2 pi G * ESD convention

P(f"Fig-10 dwarfs: n = {nb10}; g_N range {gN10.min():.3e} .. {gN10.max():.3e} m/s^2 "
  f"({gN10.min()/A0['canonical']:.3f} .. {gN10.max()/A0['canonical']:.3f} a0)")

for foot in ("canonical", "alt"):
    a0 = A0[foot]
    g_pred = gN10 * (1.0 + np.sqrt(a0 / np.maximum(gN10, 1e-300)))
    resid = np.log10(g_obs / np.maximum(g_pred, 1e-300))
    gd = (gN10 > 3e-15) & (gN10 < 0.3 * a0)       # registered deep cut g_N < 0.3 a0
    n = int(gd.sum())
    signed_med = float(np.median(resid[gd]))
    excess = 10.0 ** signed_med
    x = np.log10(g_pred[gd]); y = np.log10(g_obs[gd])
    W = np.linalg.pinv(C10[np.ix_(gd, gd)] + 1e-30 * np.eye(n))    # cov-weighted
    X = np.column_stack([np.ones(n), x])
    XWX = X.T @ W @ X
    beta = np.linalg.pinv(XWX) @ (X.T @ W @ y)
    covb = np.linalg.pinv(XWX)
    slope, s_slope = float(beta[1]), float(math.sqrt(covb[1, 1]))
    results["numbers"][foot] = {"n": n, "signed_med_dex": signed_med, "excess_factor": excess,
                                "slope": slope, "slope_sigma": s_slope,
                                "slope_over_err": (slope - 1.0) / s_slope}
    P(f"  {foot}: n = {n}; signed median = {signed_med:+.3f} dex (excess factor {excess:.2f}); "
      f"cov-weighted slope = {slope:.3f} +/- {s_slope:.3f} ((slope-1)/sigma = {(slope-1.0)/s_slope:+.2f})")

f1 = {"canonical": results["numbers"]["canonical"]["signed_med_dex"],
      "alt": results["numbers"]["alt"]["signed_med_dex"]}
sl = results["numbers"]["canonical"]["slope"]
ss = results["numbers"]["canonical"]["slope_sigma"]
F1_ok = all(v >= 0.0 for v in f1.values())
F2_ok = abs(sl - 1.0) <= 2.0 * ss
wt = results["numbers"]["canonical"]["n"]
check(
    "F1 (floor, registered reading) signed median log10(g_obs/g_pred) >= 0 on the deep cut "
    "g_N < 0.3 a0: khronon dust sits at or above the phantom-law floor; a negative median "
    "would kill the khronon-dust-as-excess reading",
    {k: f"{v:+.3f} dex" for k, v in f1.items()},
    F1_ok,
    "positive median = the mechanism working: the excess factor 10^median is the RESULT to "
    "report (khronon dust carrying the excess), not a fail")
check(
    "F2 (shape) cov-weighted log-log slope of g_obs vs g_pred = 1 within 2 sigma: the excess is "
    "a multiplicative factor (the phantom halo follows the law's SHAPE); slope far from 1 is a "
    "genuine shape failure of the phantom-law family on the dwarfs",
    f"slope = {sl:.3f} +/- {ss:.3f}  ((slope-1)/sigma = {(sl-1.0)/ss:+.2f}, |.| <= 2)",
    F2_ok,
    "the cov matrix (Kirshner weighting) is the honest error; a shape failure here would "
    "contradict the RAR-family on the isolated-dwarf sample and must be reported as such")
check(
    "F3 (window) the registered deep cut g_N < 0.3 a0 is applied and the window reported",
    f"n = {wt} points on g_N in (3e-15, 0.3 a0); full sample {nb10}",
    wt >= 5,
    "the slope is estimated on the registered deep window only")

n_ok = sum(1 for c in results["checks"].values() if c["ok"])
P(f"\n{LANE} COMPLETE: {n_ok}/{len(results['checks'])} checks PASS.")
with open(f"{LANE}_results.json", "w") as f:
    json.dump(results, f, indent=1)
import sys
sys.exit(0 if all(c["ok"] for c in results["checks"].values()) else 1)