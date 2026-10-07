#!/usr/bin/env python3
"""CFG445 POST-HOC power scaling (departure, disclosed; mock residuals only, written before the scoring run).
The frozen dry run scaled only the centrals, but the luminosity-matched control is limited by the few luminous FIELD galaxies,
so resampling centrals alone barely helps.  Here centrals AND field galaxies of each source are resampled x k (k = 2, 3, 4, 6),
same mock scatter (SPARC 0.14, WALLABY 0.18 dex), +0.10 dex step, 200 mocks (100 for k >= 4) x 200 bootstraps.  Reads cfg445_selection.csv.
Outputs cfg445_power_posthoc.out / _results.json.  No verdict weight."""
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg445_common as K  # noqa: E402

A = [r for r in csv.DictReader(open(os.path.join(HERE, "cfg445_selection.csv"))) if r["class"] in ("GC", "F")]
cls = np.array([r["class"] for r in A])
src = np.array([r["source"] for r in A])
logL = np.array([float(r["logL"]) for r in A])
x = np.array([float(r["logMh"]) for r in A])
sig = np.where(src == "SPARC", 0.14, 0.18)
rng = np.random.default_rng(4451)
out, lines = {}, []
for k in (1, 2, 3, 4, 6):
    rr = []
    for _ in range(200 if k <= 3 else 100):
        keep = np.concatenate([np.arange(len(A))] + [rng.permutation(len(A)) for _ in range(k - 1)]) if k > 1 else np.arange(len(A))
        R = rng.normal(0, sig[keep]) + 0.10 * (cls[keep] == "GC")
        D, ngu, _ = K.delta_lm(R, cls[keep], src[keep], logL[keep])
        sD = float(np.nanstd(K.boot_lm(R, cls[keep], src[keep], logL[keep], rng, 200)))
        db, _ = K.dbic_src(x[keep], R, src[keep])
        rr.append((K.verdict(D, sD, db, ngu, int((cls[keep] == "F").sum())), D / sD, db))
    pw = float(np.mean([r[0] == "TWO-REGIME SUPPORTED" for r in rr]))
    out[k] = dict(nGC=int(k * (cls == "GC").sum()), nF=int(k * (cls == "F").sum()), power=pw,
                  fS3=float(np.mean([r[1] > 3 for r in rr])), fdBIC2=float(np.mean([r[2] > 2 for r in rr])))
    s = (f"x{k:2d}: GC {out[k]['nGC']:4d}, F {out[k]['nF']:5d}: power {pw:.3f} (S>3 {out[k]['fS3']:.2f}, dBIC>2 "
         f"{out[k]['fdBIC2']:.2f})")
    print(s, flush=True)
    lines.append(s)
open(os.path.join(HERE, "cfg445_power_posthoc.out"), "w").write(
    "CFG445 POST-HOC power scaling (centrals AND field resampled x k; +0.10 dex; mock only; no verdict weight)\n" + "\n".join(lines) + "\n")
json.dump({str(k): v for k, v in out.items()}, open(os.path.join(HERE, "cfg445_power_posthoc_results.json"), "w"), indent=1)
