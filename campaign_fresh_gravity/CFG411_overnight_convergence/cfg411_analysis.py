#!/usr/bin/env python3
"""CFG411 analysis (frozen criteria): (a) HOT1 corrected vs S0 256^3 (CFG359); (b) 512^3 RES MIX-A / S0 512^3 vs CFG410 BASE canonical 256^3."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W = os.path.join(E, "_external_data", "cfg411_work")
def ratio(p, p0):
    s, s0 = json.load(open(p))["snap"]["z0"], json.load(open(p0))["snap"]["z0"]; k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P1=float(np.interp(1.0, k[m], pr)))
def cat(r): return "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
S0_256 = os.path.join(E, "_external_data", "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"); L, OUT = [], {}
for f in ("canonical", "alt"):
    r = ratio(os.path.join(W, f"cfg411_RES_Rc3_HOT1_FLAT_{f}_N256.json"), S0_256); OUT[f"a_{f}"] = dict(r, verdict=cat(r))
    L.append(f"(a) HOT1 corrected {f:9s}: s8 {r['s8']:.4f} max|P-1| {r['pdev']:.3f} P(1) {r['P1']:.3f} -> {cat(r)}")
p512, s512 = os.path.join(W, "cfg411_RES_Rc3_MIXA_FLAT_canonical_N512.json"), os.path.join(W, "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")
if os.path.exists(p512) and os.path.exists(s512):
    hi = ratio(p512, s512); lo = json.load(open(os.path.join(HERE, "..", "CFG410_filament_share_of_excess", "cfg410_results.json")))["canonical"]["BASE"]
    d8, dp = hi["s8"] - lo["s8"], hi["pdev"] - lo["pdev"]
    cls = "CONVERGED" if abs(d8) < 0.02 and abs(dp) < 0.02 else ("GROWS WITH RESOLUTION" if dp >= 0.02 else "SHRINKS")
    OUT["b"] = dict(hi=hi, lo=lo, d_s8=d8, d_pdev=dp, cls=cls, verdict512=cat(hi))
    L.append(f"(b) 512^3 RES MIX-A canonical: s8 {hi['s8']:.4f} max|P-1| {hi['pdev']:.3f} ({cat(hi)}) vs 256^3 {lo['s8']:.4f} / {lo['pdev']:.3f}: d_s8 {d8:+.4f}, d_pdev {dp:+.3f} -> {cls}")
else:
    L.append("(b) 512^3: PENDING (RES run not finished)")
print("\n".join(L)); open(os.path.join(HERE, "cfg411_analysis.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, "cfg411_results.json"), "w"), indent=1)
