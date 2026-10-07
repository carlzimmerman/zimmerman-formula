#!/usr/bin/env python3
"""CFG425 analysis (FROZEN_CRITERIA.md). Engine outputs land in cfg424_work (engine WORK path)."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), overdraw=s.get("overdraw_mass"))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
W = os.path.join(E, "cfg424_work"); B = "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N"
RUNS = {"R1 256^3 seed 360": (B + "256_seed360.json", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360.json"),
        "R2 256^3 seed 361": (B + "256_seed361.json", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361.json"),
        "R3 512^3 seed 359": (B + "512.json", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")}
L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for n, (f, s0) in RUNS.items():
    p = os.path.join(W, f)
    if not os.path.exists(p): P(f"  {n}: PENDING"); OUT[n] = None; continue
    r = rat(p, os.path.join(E, s0)); r["verdict"] = cat(r); OUT[n] = r
    P(f"  {n}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f} -> {r['verdict']}  overdraw {r['overdraw']}")
v = [OUT[n]["verdict"] for n in RUNS if OUT[n]]
OUT["verdict"] = ("NOT CONFIRMED" if any(x != "GROWTH OK" for x in v) else "CONFIRMED" if len(v) == 3 else
                  "PROVISIONAL (R1/R2 GROWTH OK; R3 pending)" if len(v) == 2 and OUT["R3 512^3 seed 359"] is None else "PENDING")
P(f"\nLANE VERDICT: {OUT['verdict']}")
open(os.path.join(HERE, "cfg425_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg425_results.json"), "w"), indent=1)
