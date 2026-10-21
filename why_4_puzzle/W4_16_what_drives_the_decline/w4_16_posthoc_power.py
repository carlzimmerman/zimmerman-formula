#!/usr/bin/env python3
"""W4-16 POST-HOC power check (added after the frozen M1 failed; NO verdict weight): can the D1 statistic rho(s, log V_flat) detect
planted pressure support at all? Plants V'^2 = V^2 - 2 sigma^2 beyond R_disk with sigma = 10, 20, 30 km/s.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_16_what_drives_the_decline/w4_16_posthoc_power.py"""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "w4_16.py")).read().split("def run(label")[0]           # functions and data load only
ns = {"__file__": os.path.join(HERE, "w4_16.py"), "__name__": "w416_funcs"}
exec(compile(src, "w4_16_funcs", "exec"), ns)
GAL, slope, perm_rho = ns["GAL"], ns["slope"], ns["perm_rho"]
print("W4-16 POST HOC power check for D1 (no verdict weight)")
for sig in (0.0, 10.0, 20.0, 30.0):
    s_, v_ = [], []
    for g in GAL:
        V = g["Vobs"].copy(); out = g["R"] > g["meta"]["Rdisk"]
        V[out] = np.sqrt(np.clip(V[out] ** 2 - 2 * sig ** 2, 1.0, None))
        s = slope(g, vobs=V)
        if s is not None and g["meta"]["Vflat"] > 0:
            s_.append(s); v_.append(np.log10(g["meta"]["Vflat"]))
    r, p = perm_rho(np.array(s_), np.array(v_), n=5000)
    print(f"  sigma {sig:4.0f} km/s: median s {np.median(s_):+.3f}; rho(s, log V_flat) {r:+.3f}, p {p:.4f} ({len(s_)} galaxies)")
