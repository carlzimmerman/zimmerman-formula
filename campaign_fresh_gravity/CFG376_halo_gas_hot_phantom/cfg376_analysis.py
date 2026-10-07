#!/usr/bin/env python3
"""CFG376 analysis: frozen decision (CFG361 cuts) per variant and footing, never pooled, plus the CMB-lensing proxy as in cfg374_analysis.py
(mean P ratio at k = 0.05-0.2 h/Mpc at z = 1, 0.5, 0; reported, not scored).  S0 = CFG359 256^3 JSON read-only.  Frozen: FROZEN_CRITERIA.md (2f4c18600)."""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg376_work"))
W9 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg359_work"))
LOG, OUT = [], {"lane": "CFG376", "frozen": "2f4c18600", "runs": {}}
def P(s=""): print(s); LOG.append(s)
r0 = json.load(open(os.path.join(W9, "cfg359_S0_FLAT_canonical_N256.json")))["snap"]
def ratios(s, zn):
    k, p = np.array(s[zn]["k"]), np.array(s[zn]["P"]); k0, p0 = np.array(r0[zn]["k"]), np.array(r0[zn]["P"]); m = k <= 1
    pr = p[m] / np.interp(k[m], k0, p0)
    return dict(s8=s[zn]["sigma8"] / r0[zn]["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
                lens=float(np.mean(pr[(k[m] >= 0.05) & (k[m] <= 0.2)])))
def cat(r):
    ds = abs(r["s8"] - 1)
    if ds > 0.20: return "FAIL"
    if ds <= 0.05 and r["pdev"] <= 0.10: return "GROWTH OK"
    return "TENSION"
P("CFG376 -- RES R_c = 3 Mpc/h, phantom from phase-filtered baryons with the collapsed phase split (halo gas 0.10 hot, stars+cold 0.08); ratios to S0 at z = 0")
verd = {}
for T in ("HALOA", "HALOB"):
    for f in ("canonical", "alt"):
        p = os.path.join(W, f"cfg376_RES_Rc3_{T}_FLAT_{f}_N256.json")
        if not os.path.exists(p):
            P(f"  {T} {f}: MISSING"); continue
        s = json.load(open(p))["snap"]; z0 = ratios(s, "z0"); z1 = ratios(s, "z1"); zh = ratios(s, "z0.5")
        c = cat(z0); verd[(T, f)] = c
        OUT["runs"][f"{T}|{f}"] = dict(z0=z0, z05=zh, z1=z1, verdict=c)
        P(f"  {T} {f:9s}: s8 {z0['s8']:.4f}  max|P-1| k<=1 {z0['pdev']:.3f}  P@0.1/0.3/1 {z0['P'][0]:.3f}/{z0['P'][1]:.3f}/{z0['P'][2]:.3f}  "
          f"(z0.5 s8 {zh['s8']:.4f}, z1 {z1['s8']:.4f}) -> {c}")
for T, lab in (("HALOA", "LANE VERDICT (primary, T_halo 10^6.5 K)"), ("HALOB", "conservative, T_halo 10^6 K")):
    vs = [verd.get((T, f)) for f in ("canonical", "alt")]
    if None in vs: v = "INCOMPLETE"
    elif "FAIL" in vs: v = "FAIL"
    elif all(x == "GROWTH OK" for x in vs): v = "GROWTH OK"
    else: v = "TENSION"
    OUT[f"verdict_{T}"] = v; P(f"  {T}: {v}  [{lab}]")
P("  compare CFG374 MIX-A (collapsed unfiltered): s8 1.015/1.019, P(k=1) 1.124/1.156 (TENSION); CFG372 pure 1e6 K: 1.009/1.011, P 7.6/8.9% (GROWTH OK)")
P("\nCMB-lensing proxy (reported, not scored)")
for key, r in OUT["runs"].items():
    P(f"  {key}: mean P ratio k 0.05-0.2: z1 {r['z1']['lens']:.3f}, z0.5 {r['z05']['lens']:.3f}, z0 {r['z0']['lens']:.3f}"
      f"  -> A_lens - 1 <~ {r['z05']['lens'] - 1:+.3f}")
open(os.path.join(HERE, "cfg376_analysis.out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg376_results.json"), "w"), indent=1)
