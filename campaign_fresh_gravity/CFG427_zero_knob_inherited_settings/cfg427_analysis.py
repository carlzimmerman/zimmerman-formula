#!/usr/bin/env python3
"""CFG427 analysis (FROZEN_CRITERIA.md)."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), overdraw=s.get("overdraw_mass"))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
W = os.path.join(E, "cfg424_work"); S0 = os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")
RUNS = {"E1 eps 0.0385": "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256_eps0.0385.json",
        "E2 eps 0.154": "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256_eps0.154.json",
        "G1 MIXB": "cfg424_RES_TA_MIXB_MASSCONS_fret1_FLAT_canonical_N256.json", "G2 HOT1": "cfg424_RES_TA_HOT1_MASSCONS_fret1_FLAT_canonical_N256.json"}
L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for n, f in RUNS.items():
    p = os.path.join(W, f)
    if not os.path.exists(p): P(f"  {n}: PENDING"); OUT[n] = None; continue
    r = rat(p, S0); r["verdict"] = cat(r); OUT[n] = r
    P(f"  {n:14s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f} (vs 0.027) -> {r['verdict']}  overdraw {r['overdraw']}")
if all(OUT.values()):
    bad = [n for n in RUNS if OUT[n]["verdict"] != "GROWTH OK"]
    v = "INSENSITIVE" if not bad else "SENSITIVE (" + ", ".join(bad) + ")"
else: v = "PENDING"
OUT["verdict"] = v; P(f"\nLANE VERDICT: {v}")
open(os.path.join(HERE, "cfg427_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg427_results.json"), "w"), indent=1)
