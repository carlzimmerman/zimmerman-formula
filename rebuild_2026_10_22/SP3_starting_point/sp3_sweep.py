#!/usr/bin/env python3
"""SP3: the native cells, sequential, one thread; cached per cell, so a stop only loses the cell in hand. Then the frozen refit by bisection. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from sp3_native import cell, HERE
TG = ("A_c2b_refit", "B_cfg886_bg")
for mp in ("EM1", "E1", "C1", "FAIR200", "AM1"):
    for mn in ("tot", "fc1"):
        for fq in (0.0, 0.872): cell(mp, mn, fq); print("done", mp, mn, fq, flush=True)
cell("EM1", "tot", 0.872, 2); print("MUTATE done", flush=True)
# refit: EM1 + delta for U = 0.50 on both backgrounds; FITTED, an inversion, not a scan. Bisection in steps the U grid (0.01) can resolve.
O = {}
for mn in ("tot", "fc1"):
    lo, hi = -0.8, 0.0; tr = []
    for i in range(7):
        d = round(0.5 * (lo + hi), 4); r = cell("EM1", mn, 0.872, 1, d); u = min(r["sparc"][t]["U_median"] for t in TG); tr.append((d, u)); print("refit", mn, d, u, flush=True)
        if u >= 0.50: lo = d
        else: hi = d
    O[mn] = dict(delta=lo, trace=tr)
json.dump(O, open(os.path.join(HERE, "sp3_refit.json"), "w"), indent=1); print("sweep done", flush=True)
