"""CFG366 analysis: ratios to S0 (CFG359, read-only), CFG361's decision cuts verbatim, controls C1 per snapshot, overdraw,
and the T5 comparison (CFG361 JSONs, read-only). Criteria: FROZEN_CRITERIA.md (5f3a22464). Run after cfg366_run_all.py."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W366, W361, W359 = (os.path.join(EXT, d) for d in ("cfg366_work", "cfg361_work", "cfg359_work"))
lines, out = [], {"rows": {}}
def P(s=""):
    print(s); lines.append(s)

S0 = json.load(open(os.path.join(W359, "cfg359_S0_FLAT_canonical_N256.json")))
def ratios(r):
    z0, s0 = r["snap"]["z0"], S0["snap"]["z0"]
    k = np.array(z0["k"]); pr = np.array(z0["P"]) / np.array(s0["P"])
    at = lambda kk: float(np.exp(np.interp(np.log(kk), np.log(k), np.log(pr))))
    m = k <= 1.0
    return dict(s8=z0["sigma8"] / s0["sigma8"], Pdev=float(np.max(np.abs(pr[m] - 1))), P01=at(0.1), P03=at(0.3), P1=at(1.0),
                s8_z05=r["snap"]["z0.5"]["sigma8"] / S0["snap"]["z0.5"]["sigma8"], s8_z1=r["snap"]["z1"]["sigma8"] / S0["snap"]["z1"]["sigma8"])

P("CFG366 reservoir rule, nonlinear PM -- ratios to S0 (CFG359 S0_FLAT_canonical_N256, read-only)")
P("=" * 100)
ctrl_ok = True
for rc in (1.0, 3.0):
    for f in ("canonical", "alt"):
        t = f"RES_Rc{rc:g}_FLAT_{f}_N256"
        p = os.path.join(W366, f"cfg366_{t}.json")
        if not os.path.exists(p):
            P(f"  {t}: MISSING"); continue
        r = json.load(open(p)); q = ratios(r)
        c1 = [r["snap"][s].get("C1_band_ratio", np.nan) for s in ("z1", "z0.5", "z0")]
        ok1 = all(x <= 0.01 for x in c1); ctrl_ok &= ok1
        od = [r["snap"][s].get("overdraw_mass", np.nan) for s in ("z1", "z0.5", "z0")]
        on = r["snap"]["z0"]
        q.update(C1=c1, overdraw=od, phantom_dom=on.get("mass_on_phantom_dom"), mass_on=on.get("mass_on"))
        out["rows"][t] = q
        P(f"  {t}: s8 {q['s8']:.4f}  Pdev {q['Pdev']:.4f}  P@0.1/0.3/1 {q['P01']:.3f}/{q['P03']:.3f}/{q['P1']:.3f} | z0.5 {q['s8_z05']:.4f} z1 {q['s8_z1']:.4f}"
          f" | C1 {max(c1):.1e} [{'ok' if ok1 else 'FAIL'}] | overdraw z1/z0.5/z0 {od[0]:.3f}/{od[1]:.3f}/{od[2]:.3f}")
for f in ("canonical", "alt"):
    p = os.path.join(W361, f"cfg361_T5_FLAT_{f}_N256.json")
    if os.path.exists(p):
        q = ratios(json.load(open(p))); out["rows"][f"T5_{f}(CFG361)"] = q
        P(f"  comparison T5_FLAT_{f} (CFG361, read-only): s8 {q['s8']:.4f}  P@0.1/0.3/1 {q['P01']:.3f}/{q['P03']:.3f}/{q['P1']:.3f}")

def decide(rc):
    rs = [out["rows"].get(f"RES_Rc{rc:g}_FLAT_{f}_N256") for f in ("canonical", "alt")]
    if any(r is None for r in rs):
        return "INCOMPLETE"
    ds = max(abs(r["s8"] - 1) for r in rs); dp = max(r["Pdev"] for r in rs)
    if ds > 0.20:
        return f"FAIL (max |s8-1| {ds:.3f})"
    if ds <= 0.05 and dp <= 0.10:
        return f"GROWTH OK (max |s8-1| {ds:.3f}, max |P-1| {dp:.3f})"
    return f"TENSION (max |s8-1| {ds:.3f}, max |P-1| {dp:.3f})"

P("\nDECISION (CFG361's cuts verbatim; both footings; never pooled)")
v1, v3 = decide(1.0), decide(3.0)
P(f"  R_c = 1 Mpc/h [LANE VERDICT]: {v1}")
P(f"  R_c = 3 Mpc/h: {v3}")
P(f"  S8 shift (fixed Om) = sigma8 ratio at z = 0; see rows.")
P(f"\nControls: C1 per snapshot {'PASS' if ctrl_ok else 'FAIL'}; field-level C0-C3 in cfg366_checks.out")
out.update(verdict_Rc1=v1, verdict_Rc3=v3, controls_C1=ctrl_ok, S0_sigma8=S0["snap"]["z0"]["sigma8"])
json.dump(out, open(os.path.join(HERE, "cfg366_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg366_analysis.out"), "w").write("\n".join(lines) + "\n")
