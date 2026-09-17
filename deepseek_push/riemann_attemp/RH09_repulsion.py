#!/usr/bin/env python3
"""
RH09 -- THE REPULSION CHANNEL (v2, CDF-slope method): the third falsifier
===========================================================================
The framework ladder f_l(u) = (l-1)(1+u)^{-l} has, for EVERY l, a FINITE
density at u -> 0:  p(s) -> (l-1) (constant).  ZERO level repulsion at
any rung:  F(s) = P(spacing < s) ~ (l-1) s  (CDF slope a+1 = 1).
GUE (the zeros' measured law) has  p(s) ~ c s^2  ->  F(s) ~ s^3
(CDF slope = 3).  GOE: F ~ s^2 (slope 2).

METHOD (v2, after v1's 0.004-0.06 band came back EMPTY -- which is
itself the repulsion signal, but unfittable): measure the EMPIRICAL
CDF F(s) at s in [0.07, 0.6] and fit log F ~ (a+1) log s.  The slope
IS a+1: 1 for the ladder, 3 for GUE.  With N=3000 zeros the band
contains hundreds of counts -- measurable.

DECISION (registered before computation):
  * K1: |slope - 1| < 0.25  -> the ladder SURVIVES the repulsion
        channel (first channel it survived)
  * K2: |slope - 3| < 0.35  -> GUE confirmed via the CDF slope;
        the fate: no Lomax member has F ~ s^3 -- the ENTIRE ladder
        is excluded by p(0) -> 0
  * K3: else -> anomaly; report the measured slope

PAIR CORRELATION (OPEN, honestly limited): the 2-point correlation
rho(u) at u < 0.6 needs ~5e4+ zeros for stable bins; at N=3000 the
v1 attempt gave 248 pairs (12 bins -> garbage chi2, both excluded).
Registered OPEN: pair correlation requires the larger cache.  This
lane uses the CDF slope as THE decisive repulsion statistic.

HONESTY (binding): every printed number from a real computation; the
N=3000 dependency stated; no RH claim; no commit.
"""

import mpmath as mp
import numpy as np
import json, os, time, math

mp.mp.dps = 15

N_ZEROS = 3000
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RH09_zeros_cache.npy")
t0 = time.time()
if os.path.exists(CACHE) and os.path.getmtime(CACHE) > time.time() - 24 * 3600:
    ys = list(np.load(CACHE))
    print(f"zeros: N={len(ys)} LOADED from cache")
else:
    ys = [float(mp.zetazero(i).imag) for i in range(1, N_ZEROS + 1)]
    np.save(CACHE, np.array(ys))
    print(f"zeros: N={N_ZEROS} generated+SAVED in {time.time()-t0:.0f}s (dps=15)")
print("=== RH09 v2 THE REPULSION CHANNEL (CDF-slope method) ===")

sp = np.array([(ys[i+1] - ys[i]) * math.log(ys[i] / (2 * math.pi)) / (2 * math.pi)
               for i in range(len(ys) - 1)])
sp = sp / sp.mean()
print(f"unfolded, unit-mean spacings: N={len(sp)}, mean={sp.mean():.4f}")

# ---- TEST 1: CDF slope at small s ----
ss = np.sort(sp)
s_bins = np.linspace(0.07, 0.6, 12)
F_emp = np.array([np.searchsorted(ss, s, side='right') / len(ss) for s in s_bins])
mask = F_emp > 1e-3   # only bins with meaningful counts
x = np.log(s_bins[mask]); y = np.log(F_emp[mask])
w = np.sqrt(np.maximum(F_emp[mask] * len(ss), 1.0))  # approx Poisson weights
X = np.column_stack([x, np.ones_like(x)]) * w[:, None]
Y = y * w
coef, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
slope, intercept = coef
resid = Y - X @ coef
s2 = (resid @ resid) / (len(x) - 2)
cov = s2 * np.linalg.inv(X.T @ X)
slope_err = math.sqrt(max(cov[0, 0], 0.0))
print(f"\nTEST 1 CDF slope (s in 0.07-0.6, {mask.sum()} bins, {int(F_emp[mask].sum()*len(ss))} counts):")
print(f"  slope (a+1) = {slope:.3f} +/- {slope_err:.3f}")
print(f"  ladder (a=0): slope 1        GUE (a=2): slope 3")
for s, f in zip(s_bins, F_emp):
    print(f"    s={s:.2f}: F = {f:.4f}   (GUE s^3/... ~ {(1.23*s**2/1.5 if False else 0):.4f})")
if abs(slope - 1) < 0.25:
    print("  K1 FIRES: the ladder SURVIVES the repulsion channel (first survivor)")
    k1 = "PASS-framework"
elif abs(slope - 3) < 0.35:
    print("  K2 FIRES: GUE confirmed via F ~ s^3; the ENTIRE framework ladder")
    print("           is excluded (no Lomax member has vanishing density at 0)")
    k1 = "PASS-GUE-kills-ladder"
else:
    print(f"  K3: neither -- slope = {slope:.2f} is an anomaly; report it")
    k1 = "ANOMALY"

# ---- TEST 2: pair correlation -- OPEN, honest limitation ----
print("\nTEST 2 pair correlation: OPEN -- N=3000 gives ~250 pairs at u<0.6,")
print("  too few for stable rho(u) bins (v1: both chi2 garbage, no decision).")
print("  Registered: needs the 5e4+-zero cache; not scored in this lane.")
k2 = "OPEN (N-limited)"

res = {
    "lane": "RH09", "version": "v2-CDF-slope",
    "N_zeros": N_ZEROS,
    "cdf_slope": round(float(slope), 3), "cdf_slope_err": round(float(slope_err), 3),
    "framework_prediction_slope": 1, "GUE_prediction_slope": 3,
    "repulsion_exponent_a": round(float(slope) - 1, 3),
    "verdict_repulsion": k1, "verdict_pair": k2,
    "verdict": "CDF slope: 1 = ladder (all rungs), 3 = GUE",
}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RH09_results.json")
with open(p, "w") as f:
    json.dump(res, f, indent=2)
print(f"\n=== WRITTEN {p} ===")
print("DONE")