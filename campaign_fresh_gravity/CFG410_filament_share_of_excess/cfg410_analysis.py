#!/usr/bin/env python3
"""CFG410 analysis (frozen criteria): BASE (corrected MIX-A) and VETO ratios to S0 (CFG359, read-only); X = share of the BASE P(k=1) excess removed by the veto."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W, W9 = os.path.join(E, "_external_data", "cfg410_work"), os.path.join(E, "_external_data", "cfg359_work")
r0 = json.load(open(os.path.join(W9, "cfg359_S0_FLAT_canonical_N256.json")))["snap"]["z0"]
def rat(tag):
    s = json.load(open(os.path.join(W, f"cfg410_{tag}.json")))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(r0["k"]), np.array(r0["P"]))
    return dict(s8=s["sigma8"] / r0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P1=float(np.interp(1.0, k[m], pr)), mass_on=s["mass_on"])
def cat(r): return "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
L, OUT = [], {}
for f in ("canonical", "alt"):
    b, v = rat(f"RES_Rc3_MIXA_FLAT_{f}_N256"), rat(f"RES_Rc3_MIXA_VETO_FLAT_{f}_N256")
    X = 1 - (v["P1"] - 1) / (b["P1"] - 1); cls = "FILAMENT-DOMINATED" if X >= 0.6 else ("SHARED" if X >= 0.3 else "HOST-DOMINATED")
    mut = 1 - v["mass_on"] / b["mass_on"]
    OUT[f] = dict(BASE=b, VETO=v, X=X, cls=cls, BASE_verdict=cat(b), VETO_verdict=cat(v), veto_on_mass_drop=mut, mutate_pass=mut > 0.5)
    L.append(f"{f:9s}: BASE s8 {b['s8']:.4f} max|P-1| {b['pdev']:.3f} -> {cat(b)} | VETO s8 {v['s8']:.4f} max|P-1| {v['pdev']:.3f} -> {cat(v)} | X = {X:.2f} ({cls}) | ON-mass drop {mut:.0%} (MUTATE {'PASS' if mut > 0.5 else 'FAIL'})")
print("\n".join(L)); open(os.path.join(HERE, "cfg410_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg410_results.json"), "w"), indent=1)
