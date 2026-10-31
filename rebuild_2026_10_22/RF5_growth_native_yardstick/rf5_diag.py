#!/usr/bin/env python3
"""RF5 reported-only diagnostic, written after the forest numbers were seen (A3): is the forest rise with z_on real linear power, and does it
survive a lower R_J node than the frozen floor? Not in any gate. kappa = 1/2 FITTED; not theory closed.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf5_diag.py"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rf5
out = {"note": "reported only, post hoc", "ratio_P_to_1e6_z3p6": {}, "forest_z3p6_RJ002": {}}
D, F3 = rf5.forest_data()
rf5.FRJ = [0.02]
base = None
for n in ("R1_1000000", "R1_100000", "R1_50000"):
    r = json.load(open(os.path.join(rf5.CELLS, n + ".json")))
    c = {"name": n, "kind": "R1", "zon": r["zon"]}
    o = rf5.run("pkd", c, np.array([r["params"][k] for k in rf5.NAMES]), pk=True, cmb=False)
    a = o["pk"][3.6]
    if base is None:
        base = a
    ks = [0.1, 0.3, 1.0, 3.0, 10.0, 20.0]
    out["ratio_P_to_1e6_z3p6"][n] = {str(k): float(np.interp(k, a[:, 0], a[:, 1]) / np.interp(k, base[:, 0], base[:, 1])) for k in ks}
    bx = F3.Box(rf5.NBOX, rf5.LBOX, 0, rf5.STRIDE)
    t = rf5.forest_table(F3, rf5.Shim(o, 3.6), 3.6, D[3.6]["k"], os.path.join(rf5.WORK, f"diag_{n}.npz"))
    pr = rf5.forest_profile(t, D[3.6], 3.6)
    out["forest_z3p6_RJ002"][n] = pr["free"]
    rf5.jw(os.path.join(HERE, "rf5_diag.json"), out)
print(out)
