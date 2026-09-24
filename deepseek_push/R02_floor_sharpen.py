#!/usr/bin/env python3
"""R02 -- GEOMETRY-FREE FLOOR SHARPENING beyond linear (door: Q03, f(1)/central_floor = 0.3305).
Kills pre-registered in RWAVE_BRIEF.md. All inputs runtime-read from Q03_results.json (K3).
Family: f_p(R) = c_p * R^p, c_p = min_i (d_i + 3 se_i)/R_i^p  [registered criterion
f(R_i) <= d_i + 3 se_i]; conservative variant c_p' = min_i d_i / R_i^p (f <= d exactly).
K1: claimed floor violating validity on ANY cloud -> INVALID.
K2: gain claimed only if f(1)/0.20710678 beats the linear 0.33048 by >= 5% relative."""
import json, os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
q3 = json.load(open(os.path.join(BASE, 'Q03_results.json')))
k12 = json.load(open(os.path.join(BASE, 'K12_results.json')))
CENTRAL_FLOOR_R1 = q3['central_floor_R1']          # 0.20710678118654757 (runtime-read)
LIN_POWER = q3['relative_power_at_R1']             # 0.3304754643963084 (runtime-read)

# K3: build (cloud, d, R, se) from Q03's floor_check + rederivation blocks
se_map = {}
for row in q3['rederivation']:
    c = row['cloud']
    if row['nse_rederived'] != 0:
        se_map[c] = abs(row['lo_rederived'] - row['d']) / abs(row['nse_rederived'])
    else:
        se_map[c] = None  # binding cloud: se not recoverable this way
# se_i = margin/margin_in_se where positive (Q03 definition)
for row in q3['floor_check']:
    c = row['cloud']
    if row['margin_in_se'] and row['margin_in_se'] > 0:
        s = row['margin'] / row['margin_in_se']
        if se_map.get(c) is None:
            se_map[c] = s
        else:
            assert abs(s - se_map[c]) < 1e-12 * max(1, abs(s)), f"se mismatch {c}"
clouds = [(row['cloud'], row['d'], row['R']) for row in q3['floor_check']]
print("clouds (name, d, R, se):")
for (c, d, R) in clouds:
    print(f"  {c}: d={d:.6f} R={R:.6f} se={se_map[c]:.3e}")

ps = np.arange(0, 1.5001, 0.001)
best = None
table = []
for p in ps:
    cp_reg = min((d + 3*se_map[c]) / R**p for (c, d, R) in clouds)
    cp_cons = min(d / R**p for (c, d, R) in clouds)
    # validity re-check (K1) at the chosen c
    ok_reg = all(cp_reg * R**p <= d + 3*se_map[c] + 1e-15 for (c, d, R) in clouds)
    ok_cons = all(cp_cons * R**p <= d + 1e-15 for (c, d, R) in clouds)
    row = {"p": float(p), "c_registered": cp_reg, "c_conservative": cp_cons,
           "f1_registered": cp_reg, "f1_conservative": cp_cons,
           "valid_registered": bool(ok_reg), "valid_conservative": bool(ok_cons)}
    table.append(row)
    if ok_reg and (best is None or cp_reg > best["c_registered"]):
        best = row
# f(1) = c_p * 1^p = c_p
gain = best["f1_registered"] / CENTRAL_FLOOR_R1
gain_lin = LIN_POWER
rel_gain = gain / gain_lin - 1.0
verdict_gain = "GAIN" if rel_gain >= 0.05 else "NO-MEANINGFUL-GAIN"
print(f"\nbest p = {best['p']:.3f}  c* = {best['c_registered']:.8f}")
print(f"f(1)/central_floor = {gain:.6f}  (linear floor {gain_lin:.6f}; rel gain {rel_gain:+.4%})")
print("verdict:", verdict_gain)
# K1 final validity audit on the claimed floor
viol = [(c, d, R, best['c_registered']*R**best['p'] - (d + 3*se_map[c]))
        for (c, d, R) in clouds if best['c_registered']*R**best['p'] > d + 3*se_map[c] + 1e-15]
k1_ok = len(viol) == 0
for v in viol: print("K1 VIOLATION:", v)
# conservative floor at best p
cons_f1 = best["c_conservative"]
print(f"conservative (f<=d exact) floor at p={best['p']}: f(1) = {cons_f1:.8f} -> power {cons_f1/CENTRAL_FLOOR_R1:.6f}")

checks = [
 {"name": "K1 validity of claimed floor on every cloud", "pass": bool(k1_ok),
  "detail": f"p={best['p']}, c={best['c_registered']}"},
 {"name": "K2 gain verdict recorded", "pass": True,
  "detail": f"{verdict_gain}: f(1)/central={gain:.6f} vs linear {gain_lin:.6f}, rel {rel_gain:+.4%}"},
 {"name": "K3 inputs runtime-read from Q03_results.json", "pass": True,
  "detail": f"{len(clouds)} clouds; se per cloud from Q03 margins"},
]
result = {"lane": "R02_floor_sharpen", "best": best, "conservative_f1_at_best_p": cons_f1,
          "f1_over_central": gain, "rel_gain_vs_linear": rel_gain, "verdict": verdict_gain,
          "checks": checks, "exit0": bool(all(c["pass"] for c in checks))}
with open(os.path.join(BASE, 'R02_results.json'), 'w') as f: json.dump(result, f, indent=1)
print("EXIT", 0 if result["exit0"] else 1)
