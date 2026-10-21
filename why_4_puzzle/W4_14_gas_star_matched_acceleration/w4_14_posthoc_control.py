#!/usr/bin/env python3
"""W4-14 POST-HOC control (added after the frozen MUTATE's M2 failed by design; NO verdict weight).
Planted acceleration-only world a0(g_bar) = a0* (g_bar/1e-11)^0.25 (no type dependence), now WITH per-point measurement noise
(sigma_log g = 2 e_V/(V ln10), seed 64), and the within-galaxy gap computed over each galaxy's FULL range (p64-style), not only
the matched range. Question: can the matched-bin statistic tell an acceleration-only world from the data at all?
Run: OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_14_gas_star_matched_acceleration/w4_14_posthoc_control.py"""
import importlib.util, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("w414", os.path.join(HERE, "w4_14.py"))
src = open(os.path.join(HERE, "w4_14.py")).read().split("GAL = [g for g in C.load_sparc()")[0]   # functions only, no run
ns = {"__file__": os.path.join(HERE, "w4_14.py"), "__name__": "w414_funcs"}
exec(compile(src, "w4_14_funcs", "exec"), ns)
C, KPC, S_RHO, accel, classes, analyse = ns["C"], ns["KPC"], ns["S_RHO"], ns["accel"], ns["classes"], ns["analyse"]
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Inc"] >= 30]
rng = np.random.default_rng(64)
planted = []
for g in GAL:
    h = dict(g); go, gb = accel(g); m = gb > 0
    a0g = 0.5 * S_RHO * (np.where(m, gb, 1e-11) / 1e-11) ** 0.25
    gp = np.where(m, gb * 0.5 * (1 + np.sqrt(1 + 4 * a0g / np.where(m, gb, 1.0))), go)
    sl = 2 * np.clip(g["eV"], 1, None) / (np.clip(g["Vobs"], 1, None) * math.log(10))
    gp = gp * 10 ** (sl * rng.standard_normal(len(gp)))
    h["Vobs"] = np.where(m, np.sqrt(gp * g["R"] * KPC) / 1e3, g["Vobs"])
    planted.append(h)
print("W4-14 POST HOC control (no verdict weight): noisy planted acceleration-only world")
r = analyse(planted, "post-hoc planted world (noise; slope 0.25)")
# full-range within-galaxy gap (p64-style sample: >= 3 valid points of each class)
dg = []
for h in planted:
    go, gb = accel(h); gm, sm = classes(h); v = (gb > 0) & (go > gb)
    a, b = np.log10((go * (go - gb) / gb)[gm & v]), np.log10((go * (go - gb) / gb)[sm & v])
    if len(a) >= 3 and len(b) >= 3:
        dg.append(np.median(a) - np.median(b))
dg = np.array(dg); rb = np.random.default_rng(64)
sd = np.std([np.median(dg[rb.integers(0, len(dg), len(dg))]) for _ in range(2000)])
print(f"\nfull-range within-galaxy gap in the planted world: {np.median(dg):+.3f} +- {sd:.3f} dex ({len(dg)} galaxies)")
print(f"matched Delta in the planted world: {r['delta_match']:+.3f} +- {r['sigma']:.3f} -> "
      f"{'the matched statistic reads ~0 while the within-galaxy gap appears: the test separates the two' if abs(r['delta_match']) < 2 * r['sigma'] and abs(np.median(dg)) > 2 * sd else 'separation NOT demonstrated'}")
