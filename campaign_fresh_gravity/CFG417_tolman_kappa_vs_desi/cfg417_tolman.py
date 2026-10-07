#!/usr/bin/env python3
"""CFG417: kappa_eff = 1/|1+3 w0| (Tolman reading) from DESI DR2 chains vs measured kappa.  Frozen: FROZEN_CRITERIA.md.  CFG417_MUTATE=1 sets w0 = -1."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CH = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "desi_dr2_chains"))
MUT = os.environ.get("CFG417_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
K, SK = 0.530, 0.037; L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for nm in ("cmb", "pantheonplus", "union3", "desy5"):
    hdr = open(os.path.join(CH, nm, "chain.1.txt")).readline().lstrip("#").split(); iw, iw0 = hdr.index("weight"), hdr.index("w")
    x = np.vstack([np.loadtxt(os.path.join(CH, nm, f"chain.{k}.txt"))[:, [iw, iw0]][int(0.3 * len(np.loadtxt(os.path.join(CH, nm, f"chain.{k}.txt")))):] for k in range(1, 5)])
    w0 = np.full(len(x), -1.0) if MUT else x[:, 1]; wt = x[:, 0]
    ke = 1.0 / np.abs(1 + 3 * w0)
    o = np.argsort(ke); c = np.cumsum(wt[o]) / wt.sum()
    med, lo, hi = (float(ke[o][np.searchsorted(c, q)]) for q in (0.5, 0.16, 0.84))
    s = max((hi - lo) / 2, 1e-9); z = (med - K) / math.hypot(SK, s)
    v = "COMPATIBLE" if abs(z) < 2 else ("EXCLUDED" if abs(z) >= 3 else "TENSION")
    OUT[nm] = dict(w0_med=float(np.median(w0)), kappa_eff_med=med, kappa_eff_68=[lo, hi], z=z, verdict=v)
    P(f"  {nm:12s}: w0 ~ {np.average(w0, weights=wt):+.3f} -> kappa_eff {med:.3f} [{lo:.3f},{hi:.3f}]  z = {z:+.2f} vs 0.530 +- 0.037 -> {v}")
P(f"  reference w = -1: kappa_eff = 0.500 (z = {(0.5 - K) / SK:+.2f})")
P(f"  per-footing measured kappa: 0.465 +- 0.076 (rho_Lambda footing), 0.55 +- 0.17 (alt) -- reported")
sn = [OUT[k]["verdict"] for k in ("pantheonplus", "union3", "desy5")]
OUT["reading"] = "EXCLUDED with DESI evolving w0 (all SN chains)" if all(v == "EXCLUDED" for v in sn) else ("COMPATIBLE" if all(v == "COMPATIBLE" for v in sn) else "MIXED")
P(f"\n{'MUTATE ' if MUT else ''}LANE: Tolman reading vs DESI SN chains: {OUT['reading']}")
open(os.path.join(HERE, f"cfg417_tolman{SUF}.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, f"cfg417_tolman{SUF}.json"), "w"), indent=1)
