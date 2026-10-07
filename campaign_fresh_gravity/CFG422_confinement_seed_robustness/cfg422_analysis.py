#!/usr/bin/env python3
"""CFG422 analysis (frozen criteria FROZEN_CRITERIA.md): x = 0.4 confined switch at 256^3, seeds 359/360/361 x canonical/alt,
vs same-seed S0 (CFG359 for 359; CFG420 = cfg411 seed runs for 360/361) and the unconfined run where one exists."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
S0 = {359: "cfg359_work/cfg359_S0_FLAT_canonical_N256.json", 360: "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360.json",
      361: "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361.json"}
UNC = {(359, "canonical"): "cfg410_work/cfg410_RES_Rc3_MIXA_FLAT_canonical_N256.json", (359, "alt"): "cfg410_work/cfg410_RES_Rc3_MIXA_FLAT_alt_N256.json",
       (360, "canonical"): "cfg411_work/cfg411_RES_Rc3_MIXA_FLAT_canonical_N256_seed360.json",
       (361, "canonical"): "cfg411_work/cfg411_RES_Rc3_MIXA_FLAT_canonical_N256_seed361.json"}
L, OUT, ok, deltas, worse = [], {}, 0, [], False
def P(s=""): print(s); L.append(s)
P(" seed foot      | confined s8  max|P-1| verdict   | unconfined max|P-1| | benefit D")
for sd in (359, 360, 361):
    for f in ("canonical", "alt"):
        tag = "" if sd == 359 else f"_seed{sd}"
        c = rat(os.path.join(E, "cfg414_work", f"cfg414_RES_Rc3_MIXA_X0.4_FLAT_{f}_N256{tag}.json"), os.path.join(E, S0[sd]))
        c["verdict"] = cat(c); ok += c["verdict"] == "GROWTH OK"; row = dict(confined=c)
        u = UNC.get((sd, f)); us = ""
        if u:
            ur = rat(os.path.join(E, u), os.path.join(E, S0[sd])); d = ur["pdev"] - c["pdev"]; row.update(unconfined=ur, delta=d)
            deltas.append(d); worse |= d < 0; us = f"{ur['pdev']:.3f} ({cat(ur)})  | {d:+.3f}"
        else:
            us = "none (S0 only)        | -"
        OUT[f"{sd}_{f}"] = row
        P(f" {sd} {f:9s} | {c['s8']:.4f}  {c['pdev']:.3f}   {c['verdict']:9s} | {us}")
rob = all(d >= 0.05 for d in deltas) and not worse
OUT.update(verdict="ROBUST BENEFIT" if rob else "NOT ROBUST", growth_ok_count=f"{ok}/6", n_comparisons=len(deltas))
P(f"\nGROWTH OK {ok}/6 confined runs (reported).  LANE VERDICT: {OUT['verdict']} (min D {min(deltas):+.3f} over {len(deltas)} comparisons)")
open(os.path.join(HERE, "cfg422_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg422_results.json"), "w"), indent=1)
