#!/usr/bin/env python3
"""CFG460 analysis (FROZEN_CRITERIA.md)."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg424_work"))
T = json.load(open(os.path.join(W, "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json")))["snap"]["z0"]
S = json.load(open(os.path.join(W, "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json")))["snap"]["z0"]
k = np.array(T["k"]); m = k <= 1; pr = np.array(T["P"])[m] / np.interp(k[m], np.array(S["k"]), np.array(S["P"]))
s8 = T["sigma8"] / S["sigma8"]; pd = float(np.max(np.abs(pr - 1)))
v = "FAIL" if abs(s8 - 1) > 0.2 else ("GROWTH OK" if abs(s8 - 1) <= 0.05 and pd <= 0.10 else "TENSION")
out = dict(s8=s8, pdev=pd, q_max=T.get("q_max"), overdraw=T.get("overdraw_mass"), verdict=("CONFIRMED (second realisation)" if v == "GROWTH OK" else "NOT CONFIRMED"), cut=v)
L = f"  512^3 seed 360: s8 {s8:.4f}  max|P-1| {pd:.4f} -> {v}; q_max {out['q_max']}; overdraw {out['overdraw']}\nLANE VERDICT: {out['verdict']}"
print(L); open(os.path.join(HERE, "cfg460_analysis.out"), "w").write(L + "\n"); json.dump(out, open(os.path.join(HERE, "cfg460_results.json"), "w"), indent=1)
