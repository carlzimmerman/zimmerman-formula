#!/usr/bin/env python3
"""T03 -- MIGHTEE deep-subpopulation attribution: is the z = +7 channel offset
(S02 CHANNEL-DEPENDENT verdict) a population property or carried by a few colour groups?
Kills pre-registered in T-WAVE_BRIEF.md BEFORE this run.
K1 (machinery): whole-deep ratio must equal N05 mightee_deep a0eff_a0 within 1e-9.
K2 (both-ways): leave-one-colour-group-out jackknife; excluding the single largest-drop
group moves a0_eff/a0 DOWN by > 50% of the gap to the Q02 anchor 0.8314 -> CONCENTRATION-DRIVEN
(selection-artifact flag on the S02 verdict); else DIFFUSE. Either outcome a result.
K3: per-group table informational only; no group-level law claimed."""
import csv, json, os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 9.3619e-11
DEEP = 0.2
checks = []
def check(label, ok, d=""):
    checks.append({"name": label, "pass": bool(ok), "detail": d})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

def ratio_stat(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    return float((np.mean(y * y) - np.mean(x * x)) / (A0 * np.mean(x)))

# runtime reads
n05 = json.load(open(os.path.join(BASE, "N05_results.json")))["mightee_deep"]
q02 = json.load(open(os.path.join(BASE, "Q02_results.json")))
ANCHOR = q02["main"]["weighted_mean"]

X, Y, C = [], [], []
with open(os.path.join(BASE, "data2", "mightee2025_rar_digitized_points.csv")) as fh:
    for row in csv.DictReader(fh):
        X.append(10.0 ** float(row["log10_gbar"]))
        Y.append(10.0 ** float(row["log10_gobs"]))
        C.append(f"{row['color_r']}|{row['color_g']}|{row['color_b']}")
X = np.array(X); Y = np.array(Y); C = np.array(C)
ok = np.isfinite(X) * np.isfinite(Y)  # elementwise finite mask
X, Y, C = X[ok], Y[ok], C[ok]
dm = X < DEEP * A0
Xd, Yd, Cd = X[dm], Y[dm], C[dm]

r_full = ratio_stat(Xd, Yd)
k1 = abs(r_full - n05["a0eff_a0"]) < 1e-9
check("K1 whole-deep ratio = N05 stored (1e-9)", k1, f"rebuild={r_full:.9f} stored={n05['a0eff_a0']:.9f}")

gap = r_full - ANCHOR
groups = np.unique(Cd)
drops = []
for gname in groups:
    m = Cd != gname
    drops.append((r_full - ratio_stat(Xd[m], Yd[m]), gname, int(np.sum(Cd == gname))))
drops.sort(reverse=True)
maxdrop, wg, ng = drops[0]
sizes = sorted(((g, int(np.sum(Cd == g))) for g in groups), key=lambda t: -t[1])
print("\ngroup sizes (top 8): " + ", ".join(f"{g[:12]}:{n}" for g, n in sizes[:8]) + " ...")
print("leave-one-group-out: largest drops (a0_eff/a0 moves DOWN by):")
for d, g, n in drops[:5]:
    print(f"  excl {g[:22]}: drop {d:.4f} (n={n}) -> r_excl = {r_full - d:.4f}")

maxdrop_frac = maxdrop / gap if gap > 0 else float("nan")
verdict = "CONCENTRATION-DRIVEN" if maxdrop_frac > 0.5 else "DIFFUSE"
check("K2 both-ways rule (either outcome a result)", True,
      f"max single-group drop = {maxdrop:.4f} = {100*maxdrop_frac:.1f}% of gap {gap:.4f} (excl. {wg[:22]}, n={ng}) -> {verdict}")

# K3 informational per-group table (n >= 5)
print("\nper-group deep ratios (n >= 5, informational):")
tbl = []
for g in groups:
    m = Cd == g
    if int(m.sum()) >= 5:
        r = ratio_stat(Xd[m], Yd[m])
        tbl.append({"group": g, "n": int(m.sum()), "a0eff_a0": r})
        print(f"  {g}: n={int(m.sum())} a0_eff/a0 = {r:.4f}")

res = {"lane": "T03_mightee_subpop", "N_deep": int(len(Xd)), "n_groups": int(len(groups)),
       "r_full": r_full, "anchor_q02": ANCHOR, "gap": gap,
       "max_drop": maxdrop, "max_drop_group": wg, "max_drop_group_n": ng,
       "max_drop_frac_of_gap": maxdrop_frac, "verdict": verdict,
       "leave_one_out": [{"group": g, "n": n, "drop": d} for (d, g, n) in drops],
       "per_group_n_ge5": tbl, "checks": checks,
       "exit0": bool(k1 and all(c["pass"] for c in checks))}
json.dump(res, open(os.path.join(BASE, "T03_mightee_subpop.json"), "w"), indent=1)
print("\nT03 COMPLETE")
print("EXIT", 0 if res["exit0"] else 1)
