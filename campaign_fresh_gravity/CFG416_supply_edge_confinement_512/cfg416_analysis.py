#!/usr/bin/env python3
"""CFG416 analysis (FROZEN_CRITERIA.md decision): census supply edge at 512^3 vs CFG411 512^3 S0 (canonical S0 serves alt: S0 has no a0)."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
S0 = os.path.join(E, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"); L, OUT = [], {}
def P(s): print(s); L.append(s)
for f in ("canonical", "alt"):
    p = os.path.join(E, "cfg416_work", f"cfg416_RES_Rc3_MIXA_SUPPLY_FLAT_{f}_N512.json")
    if not os.path.exists(p): P(f"  {f}: PENDING"); OUT[f] = None; continue
    r = rat(p, S0); r["verdict"] = cat(r); OUT[f] = r; P(f"  {f:9s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f} -> {r['verdict']}")
v = [OUT[f]["verdict"] for f in OUT if OUT[f]]
OUT["verdict"] = "CONFIRMED" if len(v) == 2 and all(x == "GROWTH OK" for x in v) else ("NOT CONFIRMED" if len(v) == 2 else "PROVISIONAL")
P(f"\nLANE VERDICT: {OUT['verdict']}")
open(os.path.join(HERE, "cfg416_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg416_results.json"), "w"), indent=1)
