#!/usr/bin/env python3
"""CFG426 analysis (FROZEN_CRITERIA.md)."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), overdraw=s.get("overdraw_mass"))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
W = os.path.join(E, "cfg424_work"); T = "cfg424_RES_TA_MIXA_MASSCONS_fret1_{b}_{f}_N256{s}.json"
S0 = {359: "cfg359_work/cfg359_S0_FLAT_canonical_N256.json", 360: "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360.json",
      361: "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361.json"}
RUNS = {"D1 DE canonical 359": ("DE", "canonical", 359), "D2 DE alt 359": ("DE", "alt", 359), "A1 FLAT alt 360": ("FLAT", "alt", 360), "A2 FLAT alt 361": ("FLAT", "alt", 361)}
L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for n, (b, f, sd) in RUNS.items():
    p = os.path.join(W, T.format(b=b, f=f, s="" if sd == 359 else f"_seed{sd}"))
    if not os.path.exists(p): P(f"  {n}: PENDING"); OUT[n] = None; continue
    r = rat(p, os.path.join(E, S0[sd])); r["verdict"] = cat(r); OUT[n] = r
    P(f"  {n}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f} -> {r['verdict']}  overdraw {r['overdraw']}")
if all(OUT.values()):
    ok = {n: OUT[n]["verdict"] == "GROWTH OK" for n in RUNS}
    v = "ROBUST" if all(ok.values()) else ("DE-SENSITIVE" if ok["A1 FLAT alt 360"] and ok["A2 FLAT alt 361"] else "NOT ROBUST")
else: v = "PENDING"
OUT["verdict"] = v; P(f"\nLANE VERDICT: {v}")
open(os.path.join(HERE, "cfg426_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg426_results.json"), "w"), indent=1)
