#!/usr/bin/env python3
"""W4-15 POST-HOC power check (added after the frozen M1 failed by design; NO verdict weight). The frozen M1 added
beta (log e_N - mean) to the real slopes, which already anti-correlate with e_N (rho -0.25), so it could not produce rho ~ 0.3.
Here: shuffle the slopes first (uncorrelated baseline, seed 64), then add the planted term; 200 realisations; report the median
achieved rho and the fraction detected at p < 0.05 and p < 0.0027 (permutation, 2000 shuffles each).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_15_outward_decline_vs_external_field/w4_15_posthoc_power.py"""
import json, os
import numpy as np
from scipy.stats import rankdata
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "w4_15_results.json")))
s = np.array([r["s"] for r in d["rows"]]); x = np.array([r["eN_max"] for r in d["rows"]])
rng = np.random.default_rng(64)
rx = rankdata(x)
rhos, p05, p3 = [], 0, 0
for k in range(200):
    sb = rng.permutation(s)
    beta = 0.3 * np.std(sb) / np.std(x)            # the frozen recipe, now on an uncorrelated baseline
    rs = rankdata(sb + beta * (x - x.mean()))
    r0 = np.corrcoef(rs, rx)[0, 1]
    null = [np.corrcoef(rs, rng.permutation(rx))[0, 1] for _ in range(2000)]
    p = (np.sum(np.abs(null) >= abs(r0)) + 1) / 2001
    rhos.append(r0); p05 += p < 0.05; p3 += p < 0.0027
print("W4-15 POST HOC power check (no verdict weight): frozen planting recipe on an uncorrelated (shuffled) baseline")
print(f"  median achieved rho {np.median(rhos):+.3f}; detected at p < 0.05 in {p05 / 2:.0f}% and at p < 0.0027 in {p3 / 2:.0f}% of 200 realisations")
print("  (the recipe's 0.3 std(s)/std(x) is not rho = 0.3 for heavy-tailed slopes; the achieved rho is the operative power point)")
