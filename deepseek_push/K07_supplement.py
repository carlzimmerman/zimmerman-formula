#!/usr/bin/env python3
"""K07 boundary supplement: dense MC E[D] bracketing the R_v = 4/3 crossings
per q.  Exact A_v by quadrature; crossing by linear interpolation of exact-R
points with delta-method SE.  Output: K07_supplement.json + stdout."""
import json
import math
import os
import sys
from multiprocessing import get_context

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import simulate
from K07_vol_window import A_vol_quadrature

TASKS = [(5.5, 0.0), (6.0, 0.0), (6.5, 0.0), (7.0, 0.0), (7.5, 0.0),
         (2.2, 3.0), (2.5, 3.0), (2.8, 3.0), (0.9, 10.0), (1.05, 10.0)]


def mc(a):
    n, t, q, s = a
    r = simulate(n, t, q, "volume", seed=s)
    D = r["D"]
    return dict(tau0=t, q=q,
                ED=float(np.mean(D)),
                sD=float(np.std(D, ddof=1) / np.sqrt(len(D))))


def main():
    tasks = [(600000, t, q, 5000 + int(t * 100) + int(q * 3))
             for t, q in TASKS]
    ctx = get_context("forkserver")
    with ctx.Pool(12) as p:
        res = p.map(mc, tasks)
    print("supplement: exact R = -ln A_v / E[D] (MC E[D], quadrature A)")
    jc = {}
    for q in (0.0, 3.0, 10.0):
        pts = sorted([m for m in res if m["q"] == q],
                     key=lambda m: m["tau0"])
        prev = None
        for m in pts:
            t = m["tau0"]
            lnA = -math.log(A_vol_quadrature(t, q, ng=160))
            R = lnA / m["ED"]
            sR = lnA * m["sD"] / m["ED"] ** 2
            print(f'  q={q:4.0f} tau0={t:4.2f}: E[D]={m["ED"]:.5f}+-'
                  f'{m["sD"]:.6f}  -lnA={lnA:.4f}  R={R:.4f}+-{sR:.4f}')
            if prev is not None and (prev["R"] - 4 / 3) * (R - 4 / 3) < 0:
                t1, R1, s1 = prev["tau0"], prev["R"], prev["sR"]
                w = (4 / 3 - R1) / (R - R1)
                tstar = t1 + w * (t - t1)
                sstar = math.sqrt(((1 - w) * s1) ** 2 + (w * sR) ** 2)
                jc[int(q)] = dict(tstar=round(tstar, 4), se=round(sstar, 4))
            prev = dict(tau0=t, R=R, sR=sR)
    print("crossings R=4/3 (linear interp of exact-R points):")
    for q in (0.0, 3.0, 10.0):
        if q in jc:
            print(f'  q={q:4.0f}: tau0* = {jc[q]["tstar"]} +- {jc[q]["se"]}')
        else:
            print(f"  q={q:4.0f}: not bracketed")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "K07_supplement.json"), "w") as f:
        json.dump({"supplement": res, "crossings": jc}, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())