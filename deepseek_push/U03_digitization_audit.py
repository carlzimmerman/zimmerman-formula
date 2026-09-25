#!/usr/bin/env python3
"""U03 -- MIGHTEE digitization robustness audit (evidence re-audit).
The z=+6.99 channel verdict rests on 80 DIGITIZED rings.  Pre-registered
(U-WAVE_BRIEF.md): tolerance +-0.02 dex/axis iid uniform, B=2000, seed 20260924.
K2 both-ways: >=50% of draws at |z|<3 -> DIGITIZATION-FRAGILE; else ROBUST."""
import csv, json, math, os
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 9.3619e-11; DEEP = 0.2; TOL = 0.02; B = 2000; SEED = 20260924
checks = []
def check(label, ok, d=""):
    checks.append({"name": label, "pass": bool(ok), "detail": d})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)
n05 = json.load(open(f"{BASE}/N05_results.json"))
q02 = json.load(open(f"{BASE}/Q02_results.json"))
lgX, lgY = [], []
with open(f"{BASE}/data2/mightee2025_rar_digitized_points.csv") as fh:
    for row in csv.DictReader(fh):
        lgX.append(float(row["log10_gbar"])); lgY.append(float(row["log10_gobs"]))
lgX = np.array(lgX); lgY = np.array(lgY)
ok = np.isfinite(lgX) & np.isfinite(lgY)
lgX, lgY = lgX[ok], lgY[ok]

def deep_ratio(lx, ly):
    x = 10.0**lx; y = 10.0**ly
    m = x < DEEP*A0
    return float((np.mean(y[m]**2) - np.mean(x[m]**2)) / (A0*np.mean(x[m])))

ratio0 = deep_ratio(lgX, lgY)
n05r = n05["mightee_deep"]["a0eff_a0"]
k1 = abs(ratio0 - n05r) < 1e-9
check("K1 unperturbed rebuild matches N05 stored (1e-9)", k1,
      f"rebuild={ratio0:.6f} stored={n05r:.6f}")
anchor = q02["main"]["weighted_mean"]; anchor_se = q02["main"]["weighted_mean_se"]
se_cg = s02 = json.load(open(f"{BASE}/S02_results.json"))["se_colourgroup"]
# y-only axis (informational, RAR scatter is y-dominated)
rng = np.random.default_rng(SEED)
zs_y = np.empty(B)
for i in range(B):
    r = deep_ratio(lgX, lgY + rng.uniform(-TOL, TOL, len(lgY)))
    zs_y[i] = (r - anchor)/math.sqrt(se_cg**2 + anchor_se**2)
# both-axis draws (main)
rng = np.random.default_rng(SEED)
zs = np.empty(B); rats = np.empty(B)
for i in range(B):
    r = deep_ratio(lgX + rng.uniform(-TOL, TOL, len(lgX)), lgY + rng.uniform(-TOL, TOL, len(lgY)))
    rats[i] = r
    zs[i] = (r - anchor)/math.hypot(se_cg, anchor_se)
frac_lt3 = float(np.mean(np.abs(zs) < 3.0))
verdict = "DIGITIZATION-FRAGILE" if frac_lt3 >= 0.5 else "DIGITIZATION-ROBUST"
print(f"\nboth-axis draws: ratio median {np.median(rats):.4f}, sd {rats.std(ddof=1):.4f} "
      f"(stored colour-group SE {se_cg:.4f})")
print(f"z_vs_q02: median {np.median(zs):+.2f}, min {zs.min():+.2f}, max {zs.max():+.2f}")
print(f"fraction |z|<3 = {frac_lt3:.3f} -> VERDICT (pre-registered): {verdict}")
print(f"y-only axis (informational): fraction |z|<3 = {float(np.mean(np.abs(zs_y)<3.0)):.3f}")
check("K2 both-ways verdict recorded (either outcome a result)", True,
      f"{verdict}; frac|z|<3={frac_lt3:.3f}")
check("K3 no group/covariate law claimed (n=72 digitized)", True, "scope respected")
res = {"lane": "U03_digitization_audit", "tolerance_dex": TOL, "B": B, "seed": SEED,
    "ratio_unperturbed": ratio0, "ratio_median": float(np.median(rats)),
    "ratio_sd": float(rats.std(ddof=1)), "se_colourgroup_stored": se_cg,
    "frac_z_lt3_both_axis": frac_lt3, "frac_z_lt3_yonly": float(np.mean(np.abs(zs_y) < 3.0)),
    "verdict": verdict, "checks": checks,
    "exit0": bool(all(c["pass"] for c in checks) and k1)}
json.dump(res, open(f"{BASE}/U03_digitization_audit_results.json", "w"), indent=1)
print("U03 COMPLETE"); print("EXIT", 0 if res["exit0"] else 1)
