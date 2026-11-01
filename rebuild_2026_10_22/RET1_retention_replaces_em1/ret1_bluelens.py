#!/usr/bin/env python3
"""RET1: BL1's blue lens sample, weighted lg M*, lg M_b as BL1 enters EM1 (M* + M_cold), S2 read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S2 = os.path.join(os.path.dirname(H), "S2_v3_lowg_lensing", "s2_v3_lowg_lensing.py"); sys.argv = [S2]; T = open(S2).read(); N = {"__file__": S2, "__name__": "s2_ro"}; exec(compile(T[:T.index("# ---- K2: forward model of an isolated point mass")], S2, "exec"), N)
O = {}
for k in ("blue", "red", "all"):
    m = N["MEMB"]["typ"][k]; w = N["WW"][m].sum(1); l = np.asarray(N["logM70"])[m]; s = np.argsort(l); c = np.cumsum(w[s]); q = [float(l[s][np.searchsorted(c, f * c[-1])]) for f in (0.16, 0.5, 0.84)]; O[k] = dict(lMs=q, lMb=[float(math.log10(10 ** x * (1 + 10 ** (-0.69 * x + 6.63)))) for x in q])
print(O); json.dump(O, open(os.path.join(H, "ret1_bluelens.json"), "w"), indent=1)
