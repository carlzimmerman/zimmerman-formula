#!/usr/bin/env python3
"""CFG518 analysis (FROZEN_CRITERIA.md): depletion-consistent (census f_ret) phantom source + census edge in the CFG424 engine.
256^3 seed 359 vs CFG359 S0 N256 (CFG361 cuts); K1 (f_ret = 1) vs CFG424 TA-can; 512^3 DC-can vs CFG411 S0 N512 if present.
CFG518_MUTATE=1 writes cfg518_analysis_MUTATE.out / cfg518_results_MUTATE.json: the decision is re-applied with the MUTATE run in the
DC-can slot (no compensation must not be GROWTH OK, so the lane must not PASS)."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg518_work"); MUT = os.environ.get("CFG518_MUTATE", "0") == "1"
S0 = os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")
S0_512 = os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")
REF424 = os.path.join(EXT, "cfg424_work", "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json")

def rat(p, p0):
    d = json.load(open(p)); s, s0 = d["snap"]["z0"], json.load(open(p0))["snap"]["z0"]
    k, P = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    sn = d["snap"]
    return dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
                overdraw=s.get("overdraw_mass"), q_max=s.get("q_max"),
                q_max_all=max((v.get("q_max") or 0.0) for v in sn.values()),
                overdraw_all=max((v.get("overdraw_mass") or 0.0) for v in sn.values()),
                cap_any=any(bool(v.get("cap_active")) for v in sn.values()),
                e_sum_z0=s.get("e_sum"), fret_catch_z0=s.get("fret_mass_mean_catch"), fret_min_z0=s.get("fret_min"),
                e_sum={k_: v.get("e_sum") for k_, v in sn.items()}, runtime_s=d.get("runtime_s"))
cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")

F = {"DC-can": "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json",
     "DC-alt": "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_alt_N256.json",
     "MUTATE (no compensation)": "cfg518_RES_TA_NOCOMP_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json",
     "K1 (f_ret = 1)": "cfg518_RES_TA_MIXA_MASSCONS_fretone_FLAT_canonical_N256.json"}
F512 = "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N512.json"
L, OUT = [], {"mutate_analysis": MUT}
def P(s=""): print(s); L.append(s)
P("CFG518: census f_ret phantom source + census edge, CFG424 engine (RC = 0), 256^3 seed 359, vs CFG359 S0 N256 (CFG361 cuts)")
for n, f in F.items():
    p = os.path.join(W, f)
    if not os.path.exists(p): P(f"  {n}: PENDING"); OUT[n] = None; continue
    r = rat(p, S0); r["verdict"] = cat(r); OUT[n] = r
    P(f"  {n:26s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}")
    P(f"  {'':26s}  q_max(z0) {r['q_max'] if r['q_max'] is not None else float('nan'):.3f}  q_max(all snaps) {r['q_max_all']:.3f}  "
      f"overdraw {r['overdraw_all']:.4f}  cap acted {r['cap_any']}  mean f_ret in catchments(z0) "
      f"{r['fret_catch_z0'] if r['fret_catch_z0'] is not None else float('nan'):.3f}  min {r['fret_min_z0'] if r['fret_min_z0'] is not None else float('nan'):.3f}")

# K1 engine control vs CFG424 TA-can
k1 = OUT["K1 (f_ret = 1)"]; K1ok = None
if k1 and os.path.exists(REF424):
    ref = rat(REF424, S0); OUT["CFG424 TA-can (reference)"] = ref
    d_p, d_s = abs(k1["pdev"] - ref["pdev"]), abs(k1["s8"] - ref["s8"])
    K1ok = d_p <= 0.002 and d_s <= 0.001
    P(f"\n  K1 vs CFG424 TA-can: max|P-1| {k1['pdev']:.4f} vs {ref['pdev']:.4f} (|d| {d_p:.2e} <= 0.002), s8 {k1['s8']:.4f} vs {ref['s8']:.4f} "
      f"(|d| {d_s:.2e} <= 0.001) -> {'PASS' if K1ok else 'FAIL'}")
    OUT["K1_pass"] = K1ok
dc = OUT["DC-can"]
if dc and k1 and dc.get("e_sum_z0") and k1.get("e_sum_z0"):
    P(f"  phantom excess Sum e (capped) census / f_ret=1: z1 {dc['e_sum']['z1'] / k1['e_sum']['z1']:.3f}  z0.5 {dc['e_sum']['z0.5'] / k1['e_sum']['z0.5']:.3f}  "
      f"z0 {dc['e_sum_z0'] / k1['e_sum_z0']:.3f}  (reported)")

# decision
c, al, mu = OUT["DC-can"], OUT["DC-alt"], OUT["MUTATE (no compensation)"]
if MUT:
    c = mu; P("\n  MUTATE ANALYSIS: the no-compensation run is placed in the DC-can slot.")
if c and al and mu and K1ok is not None:
    ok = [x["verdict"] == "GROWTH OK" for x in (c, al)]
    v = ("INVALID (K1 fails)" if not K1ok else
         "INCONCLUSIVE (MUTATE passes: confinement alone does it)" if mu["verdict"] == "GROWTH OK" else
         "PASS (256^3)" if all(ok) else "PARTIAL" if any(ok) else "FAIL")
else:
    v = "PENDING"
OUT["verdict_256"] = v; P(f"\nLANE VERDICT (256^3): {v}")

p5 = os.path.join(W, F512)
if os.path.exists(p5) and os.path.exists(S0_512):
    r5 = rat(p5, S0_512); r5["verdict"] = cat(r5); OUT["DC-can 512^3"] = r5
    P(f"  DC-can 512^3 vs CFG411 S0 N512: s8 {r5['s8']:.4f}  max|P-1| {r5['pdev']:.4f}  P@0.1/0.3/1 {r5['P'][0]:.3f}/{r5['P'][1]:.3f}/{r5['P'][2]:.3f} "
      f"-> {r5['verdict']}  q_max(all) {r5['q_max_all']:.3f} overdraw {r5['overdraw_all']:.4f} cap acted {r5['cap_any']}")
    v5 = ("CONFIRMED" if r5["verdict"] == "GROWTH OK" else "NOT CONFIRMED") if v.startswith("PASS") else "n/a (256^3 did not pass)"
else:
    v5 = "PENDING" if v.startswith("PASS") else "not run (256^3 did not pass)"
OUT["verdict_512"] = v5; P(f"LANE VERDICT (512^3): {v5}")
P("\nkappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed.")
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cfg518_analysis{sfx}.out"), "w").write("\n".join(L) + "\n")
json.dump(OUT, open(os.path.join(HERE, f"cfg518_results{sfx}.json"), "w"), indent=1)
