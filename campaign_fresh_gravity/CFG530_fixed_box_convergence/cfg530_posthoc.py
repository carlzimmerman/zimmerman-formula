#!/usr/bin/env python3
"""CFG530 post-hoc (REPORTED, not gating; added 2026-10-09 after the first 512^3 profile): is the box-size / resolution difference in
core R a halo-sample (host mass) effect of the statistic?  The CFG526 statistic takes the 100 densest scored hosts, so a larger box (or a
finer mesh, which scores more hosts) samples different masses.  Here: median core R (scored radii <= 2 cells) and median R at the
1-cell radius restricted to the COMMON log M_ta window of each pair.  Writes cfg530_posthoc.json / .out."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import cfg530_profiles as CP
import numpy as np
H = {}
for N in (128, 256, 512):
    table, rmin, mix, names = CP.tables(N); CP.setup(N, table, rmin, mix)
    for short in table:
        if table[short][4] == "S0" or not os.path.exists(os.path.join(CP.C.WORK, f"cfg526_{short}.npz")): continue
        res, h = CP.C.analyse(short)
        if h is not None: H[names[short]] = h
L_, OUT = [], {}
def P(s): print(s); L_.append(s)
def window(h, lo, hi):
    m = (h["lM"] >= lo) & (h["lM"] <= hi)
    core = h["scored"] & (np.array(CP.C.RPROF)[None, :] <= 2.0) & m[:, None]
    c = h["R"][core]; r1 = h["R"][m & h["scored"][:, 0], 0]
    return dict(n=int(m.sum()), core_R=float(np.median(c)) if c.size else None, R_1cell=float(np.median(r1)) if r1.size else None)
PAIRS = [(f"{t}_L200_N256", f"{t}_L200_N512") for t in ("LRcan", "LRalt")] + [(f"{t}_L100_N256", f"{t}_L100_N512") for t in ("LRcan", "LRalt")] + \
        [(f"BX{f}_L100_N256", f"LR{f}_L200_N512") for f in ("can", "alt")] + [(f"BX{f}_L100_N128", f"LR{f}_L200_N256") for f in ("can", "alt")]
P("core R in the common log M_ta window of each pair (CFG526 R = M_grav/M_law; reported, post-hoc)")
for a, b in PAIRS:
    if a not in H or b not in H: P(f"  {a} vs {b}: PENDING"); continue
    lo = max(H[a]["lM"].min(), H[b]["lM"].min()); hi = min(H[a]["lM"].max(), H[b]["lM"].max())
    wa, wb = window(H[a], lo, hi), window(H[b], lo, hi)
    d = None if not (wa["core_R"] and wb["core_R"]) else math.log10(wb["core_R"]) - math.log10(wa["core_R"])
    OUT[f"{a}|{b}"] = dict(window=[lo, hi], A=wa, B=wb, dlog_core=d)
    P(f"  {a} vs {b}: log M_ta [{lo:.2f}, {hi:.2f}]  n {wa['n']}/{wb['n']}  core R {wa['core_R']} -> {wb['core_R']}  "
      f"(d log {d if d is None else round(d, 3)});  R(1 cell) {wa['R_1cell']} -> {wb['R_1cell']}")
json.dump(OUT, open(os.path.join(HERE, "cfg530_posthoc.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg530_posthoc.out"), "w").write("\n".join(L_) + "\n")
