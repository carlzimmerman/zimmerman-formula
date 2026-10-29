#!/usr/bin/env python3
"""Scores PREREG_cf_mass_slope_2026-10-29.md (23095bf23a) on X48's A4 ng64 analysis: slope d ln c_f / d ln M between 1e12
and 1e14 from per-mass seed medians; 68% seed-bootstrap (2000 draws, seed 0). PASS: slope > 0 and the 68% interval contains
0.077. FAIL: the 68% interval is entirely <= 0. Otherwise NOT DECIDED. The level c_f(1e12) vs 4.0 is reported.
    python3 score_prereg_cf_slope.py ../X48_native_cf_zoom/x48_analyze_results_ng64_A4.json
"""
import json, math, sys
import numpy as np
A = json.load(open(sys.argv[1]))
by = {}
for k, r in A["runs"].items():
    if r.get("ng") == 64 and r.get("flag") == "ok" and r.get("cf") is not None:
        by.setdefault(round(math.log10(r["M"]), 3), []).append(r["cf"])
for l in sorted(by): print(f"M 1e{l:g}: n {len(by[l])}, c_f median {np.median(by[l]):.3f}, seeds {[round(c, 2) for c in by[l]]}")
if 12.0 not in by or 14.0 not in by: sys.exit("NOT DECIDED: need 1e12 and 1e14 ng64 seeds")
s0 = math.log(np.median(by[14.0]) / np.median(by[12.0])) / math.log(100)
rng = np.random.default_rng(0); bs = []
for _ in range(2000):
    a = rng.choice(by[12.0], len(by[12.0])); b = rng.choice(by[14.0], len(by[14.0]))
    bs.append(math.log(np.median(b) / np.median(a)) / math.log(100))
lo, hi = np.percentile(bs, [16, 84])
v = "PASS" if (s0 > 0 and lo <= 0.077 <= hi) else ("FAIL" if hi <= 0 else "NOT DECIDED")
print(f"slope {s0:+.3f} (68% {lo:+.3f} .. {hi:+.3f}); predicted +0.077 -> {v}; level c_f(1e12) {np.median(by[12.0]):.2f} vs 4.0")
json.dump(dict(slope=s0, ci68=[lo, hi], verdict=v, level_1e12=float(np.median(by[12.0]))), open("prereg_cf_slope_score.json", "w"), indent=1)
