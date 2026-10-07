#!/usr/bin/env python3
"""CFG423 analysis (FROZEN_CRITERIA.md): mass-conserving edge, 256^3 seed 359 canonical, vs CFG359 S0; comparison CFG410 BASE."""
import os, json, glob, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)])
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
S0 = os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"); W = os.path.join(E, "cfg423_work")
F = {"P1 (R_c=3)": "cfg423_RES_Rc3_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json", "P2 (R_c=1)": "cfg423_RES_Rc1_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json",
     "MUTATE (f_ret 0.01)": "cfg423_RES_Rc3_MIXA_MASSCONS_fret0.01_FLAT_canonical_N256.json"}
L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for n, f in F.items():
    p = os.path.join(W, f)
    if not os.path.exists(p): P(f"  {n}: PENDING"); OUT[n] = None; continue
    r = rat(p, S0); r["verdict"] = cat(r); OUT[n] = r
    xs = [v.get("x_med") for v in json.load(open(p))["snap"].values() if isinstance(v, dict) and v.get("x_med") is not None]
    P(f"  {n:20s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.3f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}" + (f"  x_med(z0) {xs[-1]:.3f}" if xs else ""))
b = rat(os.path.join(E, "cfg410_work", "cfg410_RES_Rc3_MIXA_FLAT_canonical_N256.json"), S0); OUT["comparison_BASE"] = b
P(f"  comparison CFG410 BASE (unconfined): s8 {b['s8']:.4f} max|P-1| {b['pdev']:.3f} -> {cat(b)}")
p1, p2, mu = OUT["P1 (R_c=3)"], OUT["P2 (R_c=1)"], OUT["MUTATE (f_ret 0.01)"]
if p1 and p2 and mu:
    if mu["verdict"] == "GROWTH OK": v = "INCONCLUSIVE (control broken)"
    elif p1["verdict"] != "GROWTH OK": v = "FAIL"
    elif p2["verdict"] == "GROWTH OK" and abs(p1["pdev"] - p2["pdev"]) <= 0.03: v = "ZERO-KNOB PASS"
    else: v = "PASS, R_c-DEPENDENT"
else: v = "PENDING"
OUT["verdict"] = v; P(f"\nLANE VERDICT: {v}")
open(os.path.join(HERE, "cfg423_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg423_results.json"), "w"), indent=1)
