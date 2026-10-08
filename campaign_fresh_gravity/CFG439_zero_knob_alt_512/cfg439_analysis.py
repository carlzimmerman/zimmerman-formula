#!/usr/bin/env python3
"""CFG439 analysis (FROZEN_CRITERIA.md): zero-knob rule at 512^3, alt FLAT and canonical DE, vs CFG411 512^3 S0."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), overdraw=s.get("overdraw_mass"))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
S0 = os.path.join(E, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"); L, OUT = [], {}
def P(s): print(s); L.append(s)
for n, f in (("A FLAT alt", "FLAT_alt"), ("B DE canonical", "DE_canonical")):
    r = rat(os.path.join(E, "cfg424_work", f"cfg424_RES_TA_MIXA_MASSCONS_fret1_{f}_N512.json"), S0); r["verdict"] = cat(r); OUT[n] = r
    P(f"  {n:15s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f} -> {r['verdict']}  overdraw {r['overdraw']}")
OUT["verdict"] = "CONFIRMED" if all(OUT[n]["verdict"] == "GROWTH OK" for n in OUT) else "NOT CONFIRMED"
P(f"\nLANE VERDICT: {OUT['verdict']}")
open(os.path.join(HERE, "cfg439_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg439_results.json"), "w"), indent=1)
