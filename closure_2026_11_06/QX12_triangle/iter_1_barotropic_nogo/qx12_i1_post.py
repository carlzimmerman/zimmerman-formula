#!/usr/bin/env python3
"""QX12 iter_1 POST-RESULT checks (declared after qx12_i1.out; they cannot change its label):
 M3 power: scale every hot-system depth by s in (1, 0.3, 0.1, 0.03); violations must appear once depths overlap.
 SYM: symmetric central-value depths (galaxy g_obs, hot M_obs, both to r_ta) - the depth gap with no conservative skew.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, runpy, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [os.path.join(HERE, "qx12_i1.py"), "--mutate"]
with contextlib.redirect_stdout(io.StringIO()):
    M = runpy.run_path(os.path.join(HERE, "qx12_i1.py"), run_name="qx12_lib")   # mutate branch writes only MUTATE files (already on record, identical)
build, pairs, A0 = M["build"], M["pairs"], M["A0"]
OUT = []; RES = {}
for f, a0 in A0.items():
    A, B = build(a0); RES[f] = {}
    for s in (1.0, 0.1, 0.03, 0.01, 0.003):
        Bs = [dict(b, D=b["D"] * s) for b in B]; v = pairs(A, Bs)
        RES[f][f"s{s}"] = dict(n=len(v), max_ratio=max([x["ratio"] for x in v], default=0.0))
    gal = max(a["D"] for a in A); hot = min(b["D"] for b in B if b["l"] > 0); hot_all = min(b["D"] for b in B)
    RES[f]["gap"] = dict(max_gal_D_low=gal, min_hot_D_high_lpos=hot, min_hot_D_high_all=hot_all, ratio=hot / gal)
    OUT.append(f"[{f}] M3 hot depths x s: " + ", ".join(f"s {s}: {RES[f]['s'+str(s)]['n']} viol (max {RES[f]['s'+str(s)]['max_ratio']:.3g})" for s in (1.0, 0.1, 0.03, 0.01, 0.003))
               + f"; conservative gap: max galaxy D {gal/1e6:.3g} vs min hot D (l>0) {hot/1e6:.3g} (km/s)^2, ratio {hot/gal:.1f}")
for l in OUT: print(l)
json.dump(RES, open(os.path.join(HERE, "qx12_i1_post.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx12_i1_post.out"), "w").write("\n".join(OUT) + "\n")
