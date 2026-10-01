#!/usr/bin/env python3
"""B4.3b -- SU(2) V-method (secondary definition, pre-registration section (a)): flat-histogram run in O = A + F near the junction, two-parameter reweighting, the three phases
I < II < III made equally probable; (beta_F, beta_A) of the direct three-phase equal-weight point at each L.  Usage: python3 b4_3_vertex.py L bF0 bA0   (writes results/su2V_L<L>.json)"""
import sys
sys.dont_write_bytecode = True
import os
import json
import time
import numpy as np
import b4_lib as B

HERE = os.path.dirname(os.path.abspath(__file__))
L = int(sys.argv[1]); bF0 = float(sys.argv[2]); bA0 = float(sys.argv[3])
exe = B.build("su2m", flags=("-DZFLIP",))
Np = 6.0 * L ** 4
m = B.Model(exe, f"su2V{L}", dict(L=L, bF=f"{bF0:.4f}"), "bA", bA0, Np, bw=1.0, obounds=(None, 2.0 * Np))
PAR = {4: dict(nchain=4, nsw=40000, every=2, ref_nsw=15000, nth=400, target=24, maxb=14, rr=12), 6: dict(nchain=4, nsw=60000, every=4, ref_nsw=30000, nth=500, target=10, maxb=14, rr=12)}[L]
t0 = time.time()
# the pilot runs below/above the base value in beta_A at fixed beta_F; the sampled range is wide enough to contain phases I, II and III only if the upper pilot run (cold start) sits in III:
# for the V-method the pilot 'high' phase must be phase III, so a cold start at a larger beta_F is used for the range (mean + 6 sigma of the pilot run at beta_F = bF0 + 0.25, beta_A = bA0 + 0.1)
r = B.run_point(m, 0.12, nb="auto", nchain=PAR["nchain"], nth=PAR["nth"], nsw=PAR["nsw"], every=PAR["every"], ref_nsw=PAR["ref_nsw"], target_trav=PAR["target"], max_batches=PAR["maxb"], log=lambda s: print(s, flush=True), ref_rounds=PAR["rr"])
pool = r["pool"]
v = B.vertex_jk(pool)
out = dict(group="su2V", L=L, bF0=bF0, bA0=bA0, ntrav=r["ntrav"], flat=r["flat"], seconds=time.time() - t0)
if v is None:
    out["dropped"] = True
    print(f"V-method L={L}: three-phase solution failed (fewer than three peaks or no root)", flush=True)
else:
    out.update(bF=v["bF"], bA=v["bA"], sF=v["sF"], sA=v["sA"], z=v["z"], cuts=v["cuts"])
    print(f"V-method L={L}: (beta_F, beta_A) = ({v['bF']:.4f} +- {v['sF']:.4f}, {v['bA']:.4f} +- {v['sA']:.4f}); phase weights {np.round(v['z'], 3)}; traversals {r['ntrav']}; flat {r['flat']:.2f}", flush=True)
json.dump(out, open(os.path.join(HERE, "results", f"su2V_L{L}.json"), "w"), indent=1, default=float)
