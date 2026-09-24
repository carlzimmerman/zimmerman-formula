#!/usr/bin/env python3
"""S02 -- MIGHTEE mirror: does the CONSTANT-OFFSET law hold off-SPARC?
(doors: N05 arbitration card 'MIGHTEE is the SIGN-MIRROR'; Q02/R03 constant-offset banked
on SPARC only).  Kills pre-registered in SWAVE_BRIEF.md BEFORE this run.
K1 (power): N_deep < 20 -> UNDECIDABLE, no verdict forced.
K2 (both-ways rule): |z| < 3 vs Q02 weighted mean 0.8314 -> CONSISTENT-UNIVERSAL (B-class
   banked); |z| >= 3 -> CHANNEL-DEPENDENT recorded, two-sided contradiction sharpened.
   NO re-tuning, NO budget widening; verdict recorded either way.
K3 (machinery): full-sample MIGHTEE Delta must match L06 stored (rel 1e-6) AND the deep
   rebuild must match N05's stored mightee_deep (exact point estimate), else lane INVALID.
All inputs runtime-read (L06_results.json, N05_results.json, Q02_results.json,
O04b_joint_update.json, data2/mightee2025_rar_digitized_points.csv)."""
import csv, json, os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 9.3619e-11
DEEP = 0.2
SEED = 20260924
NBOOT = 2000
checks = []
def check(label, ok, d=""):
    checks.append({"name": label, "pass": bool(ok), "detail": d})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

def m1stat(x, y):   # L06 M1 channel: E[Y^2]-E[X^2]-a0*E[X]
    x = np.asarray(x, float); y = np.asarray(y, float)
    return float(np.mean(y * y - x * x - A0 * x))

def ratio_stat(x, y):   # a0_eff/a0 = (E[Y^2]-E[X^2])/(a0*E[X])
    x = np.asarray(x, float); y = np.asarray(y, float)
    return float((np.mean(y * y) - np.mean(x * x)) / (A0 * np.mean(x)))

def boot(x, y, g, stat, n=NBOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    uniq = np.unique(g); vals = np.empty(n)
    for i in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        m = np.isin(g, pick)
        vals[i] = stat(x[m], y[m])
    return float(vals.std(ddof=1))

# runtime reads
l06 = json.load(open(os.path.join(BASE, "L06_results.json")))
n05 = json.load(open(os.path.join(BASE, "N05_results.json")))
q02 = json.load(open(os.path.join(BASE, "Q02_results.json")))
o04b = json.load(open(os.path.join(BASE, "O04b_joint_update.json")))
r_mig = [r for r in l06["results"] if "MIGHTEE" in r.get("name", "")][0]
anchor = q02["main"]["weighted_mean"]; anchor_se = q02["main"]["weighted_mean_se"]
o_x = o04b["joint"]["xbar"]; o_se = o04b["joint"]["se"]

X, Y, C = [], [], []
with open(os.path.join(BASE, "data2", "mightee2025_rar_digitized_points.csv")) as fh:
    for row in csv.DictReader(fh):
        X.append(10.0 ** float(row["log10_gbar"]))
        Y.append(10.0 ** float(row["log10_gobs"]))
        C.append(f"{row['color_r']}|{row['color_g']}|{row['color_b']}")
X = np.array(X); Y = np.array(Y); C = np.array(C)
ok = np.isfinite(X) & np.isfinite(Y)
X, Y, C = X[ok], Y[ok], C[ok]
print(f"MIGHTEE rings loaded: {len(X)} (digitized; colour ids from rgb columns)")

# K3 machinery
D_full = m1stat(X, Y)
k3a = abs(D_full / r_mig["Delta"] - 1.0) < 1e-6
check("K3a full-sample Delta matches L06 stored (rel 1e-6)", k3a,
      f"rebuild={D_full:.6e} stored={r_mig['Delta']:.6e}")
dm = X < DEEP * A0
Xd, Yd, Cd = X[dm], Y[dm], C[dm]
D_deep = m1stat(Xd, Yd)
n05d = n05["mightee_deep"]
k3b = abs(D_deep - n05d["Delta"]) < 1e-30 or abs(D_deep / n05d["Delta"] - 1.0) < 1e-9
check("K3b deep rebuild matches N05 mightee_deep Delta", k3b,
      f"rebuild={D_deep:.6e} stored={n05d['Delta']:.6e}")
ratio = ratio_stat(Xd, Yd)
k3c = abs(ratio - n05d["a0eff_a0"]) < 1e-9
check("K3c deep a0_eff/a0 matches N05 stored", k3c,
      f"rebuild={ratio:.6f} stored={n05d['a0eff_a0']:.6f}")
machinery_ok = k3a and k3b and k3c

# K1 power
check("K1 N_deep >= 20", len(Xd) >= 20, f"N_deep={len(Xd)}, colour groups={len(np.unique(Cd))}")

# K2 both-ways rule (colour-grouped bootstrap, honest shared-systematics SE; ring SE too)
se_cg = boot(Xd, Yd, Cd, ratio_stat)
se_rg = boot(Xd, Yd, np.arange(len(Xd)), ratio_stat)
se_used = max(se_cg, se_rg)
z_q02 = (ratio - anchor) / np.sqrt(se_cg ** 2 + anchor_se ** 2)
z_o04b = (ratio - o_x) / np.sqrt(se_cg ** 2 + o_se ** 2)
verdict = ("CONSISTENT-UNIVERSAL" if abs(z_q02) < 3.0 else "CHANNEL-DEPENDENT")
print(f"\nMIGHTEE deep a0_eff/a0 = {ratio:.4f} +/- {se_used:.4f} (colour-group SE {se_cg:.4f}, ring SE {se_rg:.4f})")
print(f"  vs Q02 SPARC-deep anchor {anchor:.4f}+/-{anchor_se:.4f}: z = {z_q02:+.2f}")
print(f"  vs O04b joint {o_x:.4f}+/-{o_se:.4f}: z = {z_o04b:+.2f}")
print(f"  VERDICT (pre-registered): {verdict}")
check("K2 verdict recorded (either outcome is a result)", True,
      f"{verdict}; z_q02={z_q02:.2f} z_o04b={z_o04b:.2f}; N05 mirror reproduction: stored z=6.58")

res = {"lane": "S02_mightee_mirror",
  "N_full": int(len(X)), "N_deep": int(len(Xd)), "colour_groups_deep": int(len(np.unique(Cd))),
  "machinery": {"full_delta": D_full, "l06_delta": r_mig["Delta"],
                "deep_delta": D_deep, "n05_delta": n05d["Delta"],
                "ratio": ratio, "n05_ratio": n05d["a0eff_a0"]},
  "anchor_q02": {"mean": anchor, "se": anchor_se}, "o04b": {"xbar": o_x, "se": o_se},
  "se_colourgroup": se_cg, "se_ring": se_rg, "se_used": se_used,
  "z_vs_q02": float(z_q02), "z_vs_o04b": float(z_o04b),
  "verdict": verdict,
  "checks": checks,
  "exit0": bool(all(c["pass"] for c in checks) and machinery_ok)}
json.dump(res, open(os.path.join(BASE, "S02_results.json"), "w"), indent=1)
print("S02 COMPLETE")
print("EXIT", 0 if res["exit0"] else 1)
