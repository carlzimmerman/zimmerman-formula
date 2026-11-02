#!/usr/bin/env python3
"""BF1 checks after the L3 run: planted recovery by value, and the real run's prefilter hits against every gate. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
sys.argv = [sys.argv[0], sys.argv[1]]
import numpy as np
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bf1.py")).read().split('if __name__ == "__main__"')[0])
W = os.path.join(HERE, "chunks", MODE + os.environ.get("BF1_SUF", "")); names = json.load(open(os.path.join(W, "names.json")))
d0 = np.log10(ST[:, 1] / law(ST[:, 0], A0)); RT = np.sqrt((d0 ** 2).mean()); best = []; seen = set()
if MODE == "planted":
    n = 0
    for l in open(os.path.join(W, "hits.jsonl")):
        i, o, j, w = json.loads(l)
        if w != 3 or o != "*" or not (names[i] == "(f+1.0)" or names[j] == "(f+1.0)"): continue
        s = f"({names[i]}{o}{names[j]})"; d = full(s, w, ST); r = float(np.sqrt((d ** 2).mean())); best.append((r, s))
    best.sort(); print("planted H = (1 + f) log1p(1/y), W3; hits with that factor, lowest rms:", best[:3]); sys.exit(0 if best and best[0][0] < 1e-9 else 1)
for l in open(os.path.join(W, "hits.jsonl")):
    i, o, j, w = json.loads(l); s = f"({names[i]}{o}{names[j]})"; d = full(s, w, ST); dx = full(s, w, XT); dh = full(s, w, SH); dxh = full(s, w, XH); e = full(s, w, np.array([[1e-10, 1, 1e-8, .5, 0]]))
    print(f"W{w} {s[:58]:58s} X train {dx.mean():+.3f},{np.sqrt((dx**2).mean()):.3f} SPARC train {np.sqrt((d**2).mean()):.3f}/{RT:.3f} med {np.median(d):+.3f} | X hold {dxh.mean():+.3f},{np.sqrt((dxh**2).mean()):.3f} SPARC hold {np.sqrt((dh**2).mean()):.3f}")
