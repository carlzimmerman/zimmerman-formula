#!/usr/bin/env python3
"""CB1 Part B MUTATE: targets permuted, same fits on call 0's test set; separate output. Exit 1 unless every baseline's test R2 stays below 0.1."""
import json, os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from cb1_part_b import models, feats, fitpred, r2_rmse
HERE = os.path.dirname(os.path.abspath(__file__)); Z = np.load(os.path.join(HERE, "cb1_counts.npz")); D = {k: Z[k] for k in ("N", "counts", "mdm", "main")}
y = np.random.default_rng(20261030).permutation(Z["y"]); test = np.array(json.load(open(os.path.join(HERE, "cb1_part_a_results.json")))["test0"]); tr = np.setdiff1d(np.arange(len(y)), test)
F = feats(D); L = ["CB1 Part B MUTATE, permuted targets"]; ok = True
for n, (k, make) in models().items():
    r = r2_rmse(y[test], fitpred(make, F[k][tr], y[tr], F[k][test]))[0]; ok &= r < 0.1; L.append(f"  {n:12s} test R2 {r:+.3f}")
L.append("bites" if ok else "NO BITE"); open(os.path.join(HERE, "cb1_part_b_MUTATE.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(0 if ok else 1)
