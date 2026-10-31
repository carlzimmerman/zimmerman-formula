#!/usr/bin/env python3
"""SN1 POST-RESULT 2 (no frozen verdict): flat S inside ET1's lowest band, 52-85. Which M200 lines are admitted, and do any meet EM1's line at lg M* 8, where SPARC's dwarfs sit? +- 0.3 dex stated."""
import contextlib, io, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "sn1_post.py")).read(); src = src[:src.index("Qc = g[")].replace("np.arange(0.8, 3.01, 0.05)", "np.arange(1.70, 1.951, 0.05)")
G0 = {"__file__": os.path.join(HERE, "sn1_post.py"), "__name__": "x"}; exec(compile(src, G0["__file__"], "exec"), G0)
g = G0["g"]; LSG, bilin = G0["LSG"], G0["bilin"]; T = G0["Etable"](g["systems"]("canonical")); RES = {}
for f in g["FEET"]:
    Q = g["systems"](f); idx = g["boot_setup"](Q); lm = np.array([q["lm"] for q in Q]); RES[f] = {}
    for ls in LSG:
        ad = []
        for a in np.round(np.arange(6, 11.01, .05), 2):
            for b in np.round(np.arange(-.6, 2.01, .05), 2):
                z = g["clsZ"](bilin(T, a + b * (lm - 7), np.full(len(Q), ls)), Q, idx); m = max(abs(v[2]) for v in z.values())
                if m < 2: ad.append((a, b, m))
        A = np.array(ad) if ad else np.zeros((0, 3)); R = dict(n=len(ad))
        if ad:
            at = lambda x: A[:, 0] + A[:, 1] * (x - 7); R.update({f"lgM200_lm{x}": [float(at(x).min()), float(at(x).max())] for x in (4, 6, 8)})
            near = A[abs(at(8) - 9.38) < 0.3]; R["n_meet_EM1_lm8"] = len(near)
            if len(near): R.update(meet_b=[float(near[:, 1].min()), float(near[:, 1].max())], meet_lm4=[float((near[:, 0] + near[:, 1] * -3).min()), float((near[:, 0] + near[:, 1] * -3).max())], meet_a=[float(near[:, 0].min()), float(near[:, 0].max())], meet_bestZ=float(near[:, 2].min()))
        RES[f][f"{10**ls:.1f}"] = R; print(f, f"S {10**ls:.1f}", R, flush=True)
json.dump(RES, open(os.path.join(HERE, "sn1_post2_results.json"), "w"), indent=1)
