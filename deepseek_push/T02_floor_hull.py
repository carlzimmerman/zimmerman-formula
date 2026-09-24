#!/usr/bin/env python3
"""T02 -- constant-floor hull check: is c* = 0.28177 valid BETWEEN the cloud points?
Door: R02's registered caveat ("validity CHECKED only at the 6 landed cloud R values;
R=1 extrapolation is a family choice") -- the UNEXECUTED SWAVE_BRIEF S03 door.
Kills pre-registered in T-WAVE_BRIEF.md BEFORE this run.
Inputs runtime-read only: Q03_results.json (clouds: R_i, d_i), K12_results.json (se chain
se_D per cloud -- the volume_q10 binding row has margin/margin_in_se = 0/0, exactly why the
brief routed the se chain through K12), R02_results.json (c_registered, c_conservative).
Registered assumption (recorded, not a theorem): B(R) = piecewise-LINEAR interpolation of
b_i = d_i + 3*se_i between cloud points, tested on a 2000-pt grid over the hull."""
import json, os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(label, ok, d=""):
    checks.append({"name": label, "pass": bool(ok), "detail": d})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

# K3: runtime reads
q03 = json.load(open(os.path.join(BASE, "Q03_results.json")))
k12 = json.load(open(os.path.join(BASE, "K12_results.json")))["measurements"]
r02 = json.load(open(os.path.join(BASE, "R02_results.json")))
c_reg = r02["best"]["c_registered"]
c_con = r02["best"]["c_conservative"]
clouds = q03["floor_check"]
k3 = len(clouds) == 6
check("K3 six clouds runtime-read (Q03) + se chain from K12 + c* from R02", k3,
      f"n_clouds={len(clouds)}, c_reg={c_reg:.8f}, c_con={c_con:.8f}")

pts, se_consistent = [], True
for cl in clouds:
    d = cl["d"]; R = cl["R"]
    se = k12[cl["cloud"]]["se_D"]
    if cl["margin_in_se"] > 0:  # 0/0 at the binding cloud volume_q10: se taken from K12 directly
        if abs(se - cl["margin"] / cl["margin_in_se"]) > 1e-12: se_consistent = False
    pts.append((R, d + 3.0 * se, cl["cloud"], d, se))
check("K3b se chain consistent (margin/margin_in_se == K12 se_D where defined)", se_consistent)

pts.sort(key=lambda t: t[0])
Rs = np.array([p[0] for p in pts]); bs = np.array([p[1] for p in pts])
print("\ncloud hull points (R, b = d + 3*se_D):")
for (R, b, name, d, se) in pts: print(f"  {name:12s} R={R:9.4f}  d={d:.6f}  se={se:.6g}  b={b:.6f}")

# K1: interior hull violation test on the interpolated bound
Rg = np.linspace(Rs[0], Rs[-1], 2000)
B = np.interp(Rg, Rs, bs)
minmargin = float(np.min(B - c_reg))
worst = float(Rg[np.argmin(B - c_reg)])
k1 = bool(np.all(B >= c_reg))
check("K1 no interior hull violation (c* <= B(R) on 2000-pt grid)", k1,
      f"min margin = {minmargin:.6f} at R = {worst:.4f}" + (" -> hull HOLDS" if k1 else " -> DOWNGRADE (pointwise-only)"))

# K2: coverage; R=1 certified only if inside the hull (no extrapolation claim)
cov_lo, cov_hi = float(Rs[0]), float(Rs[-1])
inside = cov_lo <= 1.0 <= cov_hi
check("K2 hull R-coverage reported; R=1 certified only if inside hull", True,
      f"hull = [{cov_lo:.4f}, {cov_hi:.4f}] of [0,1]; R=1 {'INSIDE' if inside else 'OUTSIDE (no extrapolation claim; R02 family-choice caveat stands for R<%.2f)' % cov_lo}")

Bc = np.interp(Rg, Rs, bs)
minm_con = float(np.min(Bc - c_con))
k1c = bool(np.all(Bc >= c_con))
print(f"\ninformational: conservative c_con = {c_con:.8f} -> min margin {minm_con:.6f}, holds={k1c}")

verdict = ("HULL-HOLDS (constant floor c* = 0.28177 valid on the interpolated hull over "
           f"[{cov_lo:.4f}, {cov_hi:.4f}]; R02 interior caveat CLOSED within the registered linear assumption)"
           if k1 else "DOWNGRADE (constant floor valid pointwise-only; R02 caveat stands unresolved)")
print(f"\nVERDICT: {verdict}")

res = {"lane": "T02_floor_hull", "c_registered": c_reg, "c_conservative": c_con,
       "registered_assumption": "piecewise-linear interpolation of b_i = d_i + 3*se_i (assumption, not theorem)",
       "hull_points": [{"cloud": n, "R": R, "d": d, "se": se, "b": b} for (R, b, n, d, se) in pts],
       "hull_range": [cov_lo, cov_hi], "R1_inside_hull": bool(inside),
       "min_margin_registered": minmargin, "min_margin_R": worst,
       "min_margin_conservative": minm_con, "conservative_holds": k1c,
       "verdict": verdict, "checks": checks,
       "exit0": bool(k3 and se_consistent and all(c["pass"] for c in checks))}
json.dump(res, open(os.path.join(BASE, "T02_floor_hull.json"), "w"), indent=1)
print("T02 COMPLETE")
print("EXIT", 0 if res["exit0"] else 1)
