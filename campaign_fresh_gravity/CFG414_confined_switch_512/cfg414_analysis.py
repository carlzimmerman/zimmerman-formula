#!/usr/bin/env python3
"""CFG414 analysis (frozen): x = 0.4 confined switch at 512^3 vs the 512^3 S0 (CFG411, canonical; alt S0 at 512^3 if present, else the
canonical S0 is used and flagged).  Control: CFG411b BASE 512^3.  CFG361 cuts per footing."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W, W11 = os.path.join(E, "_external_data", "cfg414_work"), os.path.join(E, "_external_data", "cfg411_work")
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)])
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for f in ("canonical", "alt"):
    p = os.path.join(W, f"cfg414_RES_Rc3_MIXA_X0.4_FLAT_{f}_N512.json")
    if not os.path.exists(p): P(f"  {f}: PENDING"); OUT[f] = None; continue
    s0 = os.path.join(W11, f"cfg411_S0_Rc3_MIXA_FLAT_{f}_N512.json"); flag = ""
    if not os.path.exists(s0):
        s0 = os.path.join(W11, "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"); flag = " [S0: canonical run used; S0 has no a0, so it is footing-independent]"
    r = rat(p, s0); r["verdict"] = cat(r); OUT[f] = r
    P(f"  {f:9s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.3f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}{flag}")
b = rat(os.path.join(W11, "cfg411_RES_Rc3_MIXA_FLAT_canonical_N512.json"), os.path.join(W11, "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))
P(f"  control BASE 512^3 canonical (no mask): s8 {b['s8']:.4f} max|P-1| {b['pdev']:.3f} -> {cat(b)}")
vs = [OUT[f]["verdict"] for f in ("canonical", "alt") if OUT[f]]
OUT["verdict"] = ("CONFIRMED" if len(vs) == 2 and all(v == "GROWTH OK" for v in vs) else ("NOT CONFIRMED" if len(vs) == 2 else "PROVISIONAL (" + ", ".join(vs) + ")"))
P(f"\nLANE VERDICT: {OUT['verdict']}"); OUT["control"] = b
open(os.path.join(HERE, "cfg414_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg414_results.json"), "w"), indent=1)
