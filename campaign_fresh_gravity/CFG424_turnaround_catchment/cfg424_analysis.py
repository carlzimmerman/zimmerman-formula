#!/usr/bin/env python3
"""CFG424 analysis (FROZEN_CRITERIA.md): per-catchment mass conservation in turnaround spheres, 256^3 seed 359, vs CFG359 S0."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
def rat(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
                overdraw=s.get("overdraw_mass"), q_max=s.get("q_max"))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
S0 = os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"); W = os.path.join(E, "cfg424_work")
F = {"TA-can": "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json", "TA-alt": "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_alt_N256.json",
     "MUTATE (no compensation)": "cfg424_RES_TA_NOCOMP_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json"}
L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for n, f in F.items():
    p = os.path.join(W, f)
    if not os.path.exists(p): P(f"  {n}: PENDING"); OUT[n] = None; continue
    r = rat(p, S0); r["verdict"] = cat(r); OUT[n] = r
    P(f"  {n:25s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}"
      + (f"  overdraw {r['overdraw']:.4f} q_max {r['q_max']:.3f}" if r["overdraw"] is not None else ""))
c, al, mu = OUT["TA-can"], OUT["TA-alt"], OUT["MUTATE (no compensation)"]
if c and al and mu:
    ok = [x["verdict"] == "GROWTH OK" for x in (c, al)]
    v = ("INCONCLUSIVE (MUTATE passes: confinement alone does it)" if mu["verdict"] == "GROWTH OK" else
         "ZERO-KNOB PASS" if all(ok) else "PARTIAL" if any(ok) else "FAIL")
else: v = "PENDING"
OUT["verdict"] = v; P(f"\nLANE VERDICT: {v}")
open(os.path.join(HERE, "cfg424_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg424_results.json"), "w"), indent=1)
