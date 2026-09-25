#!/usr/bin/env python3
"""
W02 -- FLOOR-FAMILY CAVEAT QUANTIFICATION (R02/V02 "family-bound caveat")
2026-09-25.  Conductor-run lane (W-WAVE_BRIEF.md, kills pre-registered there).

Door: V02 banked the maximal POWER-LAW floor p=0.6719, c=0.205581 (retention
0.993 at R=1) with a registered family-bound caveat.  This lane scans the
pre-registered family set on the SAME extended 11-cloud set (pure reanalysis,
no new MC) and quantifies the family-choice sensitivity of f(1)/central_floor.

Kills (pre-registered in W-WAVE_BRIEF.md):
  K1 machinery: recompute V02's stored extended-floor p/c to 1e-9 with the SAME
     scan grid; inputs runtime-read (V02/K12/Q03 JSONs).
  K2 both-ways: if ANY pre-registered family achieves retention > 0.993 + 0.05
     -> FAMILY-FRAGILE (V02's R=1 resolution carries an explicit family caveat
     with numbers); else FAMILY-STABLE.  Either outcome banked; no re-tuning.
  K3: floor-channel claim only; families fixed BEFORE scanning.
"""
import json, math, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
res = {"lane": "W02_floor_family", "prereg": "W-WAVE_BRIEF.md",
       "checks": {}, "families": {}, "t_start": time.strftime("%Y-%m-%d %H:%M:%S")}
checks = res["checks"]
def rec(name, ok, detail):
    checks[name] = {"pass": bool(ok), "detail": detail}
    print("  [%s] %s   %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)

V02 = json.load(open(os.path.join(HERE, "V02_floor_extension_results.json")))
K12 = json.load(open(os.path.join(HERE, "K12_results.json")))
Q03 = json.load(open(os.path.join(HERE, "Q03_results.json")))
CENTRAL_FLOOR_R1 = 0.20710678118654757

# ------------------------------------------------------------- extended set
clouds = []
for k, m in K12["measurements"].items():
    clouds.append(dict(name=k, E_D=m["E_D"], se_D=m["se_D"], E_v2=m["E_v2"]))
for k, m in V02["new_clouds"].items():
    clouds.append(dict(name=k, E_D=m["E_D"], se_D=m["se_D"], E_v2=m["E_v2"]))
for c in clouds:
    c["b"] = c["E_D"] + 3.0 * c["se_D"]
Rs = np.array([c["E_v2"] for c in clouds]); Bs = np.array([c["b"] for c in clouds])
print("extended set: %d clouds (V02 says %d)" % (len(clouds), V02["extended_floor"]["n_clouds"]), flush=True)
if len(clouds) != V02["extended_floor"]["n_clouds"]:
    print("K1 FAIL: cloud count mismatch -> lane INVALID", flush=True)
    res["exit"] = 1
    json.dump(res, open(os.path.join(HERE, "W02_floor_family_results.json"), "w"), indent=1)
    raise SystemExit(1)

# ------------------------------------------------------------- K1 recompute
def maxpowerlaw():
    # EXACT V02 scan: stage-1 grid then refine +-0.0025 around the stage-1 best
    best = None
    for p in np.linspace(-3.0, 3.0, 1201):
        cp = float(np.min(Bs / Rs ** p))
        ret = cp / 0.20710678118654757
        if best is None or ret > best["retention"]:
            best = dict(p=float(p), c=cp, retention=float(ret))
    for p in np.linspace(best["p"] - 0.0025, best["p"] + 0.0025, 501):
        cp = float(np.min(Bs / Rs ** p))
        ret = cp / 0.20710678118654757
        if ret > best["retention"]:
            best = dict(p=float(p), c=cp, retention=float(ret))
    return best
pl = maxpowerlaw()
st = V02["extended_floor"]
match = abs(pl["p"] - st["p"]) < 1e-9 and abs(pl["c"] - st["c"]) < 1e-9
rec("K1_recompute_V02_powerlaw_1e-9", match,
    "p=%.10f c=%.12f vs stored p=%.10f c=%.12f" % (pl["p"], pl["c"], st["p"], st["c"]))
if not match:
    print("K1 FAIL -> lane INVALID", flush=True)
    res["exit"] = 1
    json.dump(res, open(os.path.join(HERE, "W02_floor_family_results.json"), "w"), indent=1)
    raise SystemExit(1)

def binding(cfun):
    vals = [cfun(c["E_v2"]) for c in clouds]
    m = min(vals)
    return [c["name"] for c, v in zip(clouds, vals) if abs(v - m) < 1e-12]

# ------------------------------------------------------------- family scans
res["families"]["F1_powerlaw"] = dict(p=pl["p"], c=pl["c"], retention=pl["retention"],
    binding=binding(lambda R: pl["c"] * R ** pl["p"]), form="c*R^p")
best_h = None
for c1 in np.linspace(1e-4, 1.0, 2001):
    c0 = float(np.min(Bs - c1 * Rs))
    if c0 < 0: continue
    f1 = max(c0, c1) / 0.20710678118654757
    if best_h is None or f1 > best_h["retention"]:
        best_h = dict(c0=c0, c1=float(c1), retention=float(f1))
bh = best_h
rec("F2_hinge_valid_on_all_11", bh is not None and bh["retention"] > 0,
    "c0=%.10f c1=%.10f retention=%.4f" % (bh["c0"], bh["c1"], bh["retention"]))
res["families"]["F2_hinge"] = dict(c0=bh["c0"], c1=bh["c1"], retention=bh["retention"],
    binding=binding(lambda R: max(bh["c0"], bh["c1"] * R)), form="max(c0, c1*R)")
best_a = None
for c1 in np.linspace(1e-4, 1.0, 2001):
    c0 = float(np.min(Bs - c1 * Rs))
    f1 = (c0 + c1) / 0.20710678118654757
    if best_a is None or f1 > best_a["retention"]:
        best_a = dict(c0=c0, c1=float(c1), retention=float(f1))
res["families"]["F3_affine"] = dict(c0=best_a["c0"], c1=best_a["c1"],
    retention=best_a["retention"],
    binding=binding(lambda R: best_a["c0"] + best_a["c1"] * R), form="c0+c1*R")
best4 = None
for p in np.linspace(0.0, 1.0, 251):
    for c1 in np.linspace(1e-3, 1.0, 501):
        c0 = float(np.min(Bs - c1 * Rs ** p))
        if c0 < 0: continue
        f1 = (c0 + c1) / 0.20710678118654757
        if best4 is None or f1 > best4["retention"]:
            best4 = dict(c0=c0, c1=float(c1), p=float(p), retention=float(f1))
res["families"]["F4_floor_plus_power"] = dict(c0=best4["c0"], c1=best4["c1"], p=best4["p"],
    retention=best4["retention"],
    binding=binding(lambda R: best4["c0"] + best4["c1"] * R ** best4["p"]),
    form="c0+c*R^p")

for fam, d in res["families"].items():
    print("%-22s retention f(1)/central = %.4f  (%s)" % (fam, d["retention"], d["form"]), flush=True)

# ------------------------------------------------------------- K2 both-ways
V02_RET = st["retention_vs_central_R1"]
over = {f: d["retention"] for f, d in res["families"].items() if d["retention"] > V02_RET + 0.05}
res["family_fragile"] = bool(over)
rec("K2_family_sensitivity_rule", True,
    ("FAMILY-FRAGILE: families beating power-law retention by > 0.05: %s"
     if over else "FAMILY-STABLE: no family beats %.4f by > 0.05 (max spread %.4f)")
    % (V02_RET, max(d["retention"] for d in res["families"].values()) - V02_RET))

ok = all(v["pass"] for v in checks.values())
res["exit"] = 0 if ok else 1
print("WROTE W02_floor_family_results.json", flush=True)
print("ALL W02 CHECKS PASSED" if ok else "W02 CHECKS FAILED", flush=True)
json.dump(res, open(os.path.join(HERE, "W02_floor_family_results.json"), "w"), indent=1)
raise SystemExit(0 if ok else 1)
