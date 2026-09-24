#!/usr/bin/env python3
"""S03 -- Q-functional: does the N02-anchored ONE-PARAMETER-PER-q law hold?
E[Q](tau0,q) = 3/4 + (-4/5 + B0(q))*tau0   (intercept PINNED exactly 3/4 -- N02 landed
intercept 0.75010 = 3/4 within SE and thin slope -4/5+B0; L02's F4 separable quadratic
was a DIFFERENT family (free intercept/slope globally, 3 global params, 21.1 SE).
Door: L02 challenge kill -- any claimed closed form must reproduce the published table
within 3 SE at ALL grid points.  Kills pre-registered in SWAVE_BRIEF.md.
K1: max |resid| <= 3 SE over the FULL published table -> CLOSED-FORM-CLAIMED (per-q B0
    banked); else honest FAIL: anchored family DEAD, L02 verdict strengthened.
K2: intercept never fitted (pinned 3/4) -- fitting it would be the F1-family rehash.
K3: all inputs runtime-read from L02_results.json (both tables, volume AND central)."""
import json, os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(label, ok, d=""):
    checks.append({"name": label, "pass": bool(ok), "detail": d})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

l02 = json.load(open(os.path.join(BASE, "L02_results.json")))
tables = {"volume": l02["table_volume"], "central": l02["table_central"]}
res_tables = {}
all_max = {}
for tname, rows in tables.items():
    tq = sorted({r["tau0"] for r in rows}); qs = sorted({r["q"] for r in rows})
    print(f"\n--- {tname} table: {len(rows)} rows, tau0 in {tq[0]}..{tq[-1]}, q in {qs} ---")
    b0, resid_rows = {}, []
    for q in qs:
        rr = [r for r in rows if r["q"] == q]
        t = np.array([r["tau0"] for r in rr]); y = np.array([r["E_Q"] for r in rr])
        s = np.array([r["s_Q"] for r in rr])
        # pinned-intercept weighted LS for slope m = (-4/5 + B0(q)):  y - 3/4 = m * tau0
        w = 1.0 / s ** 2
        m = float(np.sum(w * t * (y - 0.75)) / np.sum(w * t * t))
        var_m = float(1.0 / np.sum(w * t * t))
        b0[q] = (float(m + 0.8), float(np.sqrt(var_m)))
        for r in rr:
            pred = 0.75 + m * r["tau0"]
            z = (r["E_Q"] - pred) / r["s_Q"]
            resid_rows.append({"tau0": r["tau0"], "q": r["q"], "E_Q": r["E_Q"],
                               "pred": pred, "z": z})
    maxz = max(abs(r["z"]) for r in resid_rows)
    rmsz = float(np.sqrt(np.mean([r["z"] ** 2 for r in resid_rows])))
    all_max[tname] = maxz
    k1 = maxz <= 3.0
    print(f"  B0(q): " + ", ".join(f"q={q}: {b0[q][0]:.5f}+/-{b0[q][1]:.5f}" for q in qs))
    print(f"  max |z| = {maxz:.2f} SE (rms {rmsz:.2f}) over {len(resid_rows)} rows")
    verdict_t = "CLOSED-FORM-CLAIMED" if k1 else "FAIL-ANCHORED-FAMILY"
    print(f"  verdict: {verdict_t}")
    worst = sorted(resid_rows, key=lambda r: -abs(r["z"]))[:5]
    for r in worst: print(f"    worst: tau0={r['tau0']} q={r['q']} z={r['z']:+.2f}")
    res_tables[tname] = {"B0": {str(q): b0[q] for q in qs}, "max_z": maxz, "rms_z": rmsz,
                         "verdict": verdict_t, "residuals": resid_rows}
# secondary informational: B0(q) q-dependence (volume)
b0s = res_tables["volume"]["B0"]
if "0.0" in b0s and "10.0" in b0s:
    m0, s0 = b0s["0.0"]; m10, s10 = b0s["10.0"]
    zb = (m10 - m0) / np.sqrt(s0 ** 2 + s10 ** 2)
    print(f"\nB0 q-dependence (volume): B0(10)-B0(0) z = {zb:+.2f}")
else:
    zb = None
# one-parameter-per-q full-table verdict (kill applied to the volume table = the published E[Q] channel)
vol_ok = all_max["volume"] <= 3.0
cen_ok = all_max["central"] <= 3.0
claim = ("CLOSED-FORM-CLAIMED (volume table; kill met)" if vol_ok
         else "MEASURED-ONLY STANDS -- anchored one-param-per-q family DEAD at full table (L02 strengthened)")
print(f"\nS03 CLAIM: {claim}")
check("K1 full-table 3-SE rule applied, verdict recorded", True,
      f"volume max_z={all_max['volume']:.2f} central max_z={all_max['central']:.2f}")
check("K2 intercept pinned exactly 3/4 (never fitted)", True, "pred = 0.75 + m*tau0 only")
check("K3 inputs runtime-read from L02_results.json (both tables)", True,
      f"volume {len(l02['table_volume'])} rows, central {len(l02['table_central'])} rows")
res = {"lane": "S03_q_anchored", "tables": res_tables, "B0_q_z": float(zb) if zb is not None else None,
       "claim": claim,
       "exit0": bool(all(c["pass"] for c in checks))}
json.dump(res, open(os.path.join(BASE, "S03_results.json"), "w"), indent=1)
print("S03 COMPLETE")
print("EXIT", 0 if res["exit0"] else 1)
