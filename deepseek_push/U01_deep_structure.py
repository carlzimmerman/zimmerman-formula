#!/usr/bin/env python3
# fix-forward (run-1): K1 fired (bin2 n=10 < 15) yet run-1 recorded a verdict field;
# rerun forces UNDECIDABLE per the pre-registered K1, numbers kept informational.
# Same fix-forward pattern as Q01/R01 (recorded in-script, house rule 3).
"""U01 -- MIGHTEE deep-band structure test (Q02 analog on the mirror channel).
Is the S02 channel offset (+1.33) a CONSTANT zero-point within the MIGHTEE deep
band, or g_bar-dependent (onset-like)?  Kills pre-registered in U-WAVE_BRIEF.md
BEFORE this run: K1 bin n<15 -> UNDECIDABLE; K2 both-ways |z_slope|>=3 ->
STRUCTURE-ONSET else CONSTANT-WITHIN-CHANNEL; K3 machinery L06 1e-6 / N05 1e-9."""
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
def ratio_stat(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    return float((np.mean(y*y) - np.mean(x*x)) / (A0 * np.mean(x)))
def boot(g, stat, n=NBOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    uniq = np.unique(g); vals = np.empty(n)
    for i in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        m = np.isin(g, pick)
        vals[i] = stat(m)
    return vals

l06 = json.load(open(os.path.join(BASE := os.path.dirname(os.path.abspath(__file__)), "L06_results.json")))
n05 = json.load(open(os.path.join(BASE, "N05_results.json")))
X, Y, C = [], [], []
with open(os.path.join(BASE, "data2", "mightee2025_rar_digitized_points.csv")) as fh:
    for row in csv.DictReader(fh):
        X.append(10.0**float(row["log10_gbar"])); Y.append(10.0**float(row["log10_gobs"]))
        C.append(f"{row['color_r']}|{row['color_g']}|{row['color_b']}")
X = np.array(X); Y = np.array(Y); C = np.array(C)
ok = np.isfinite(X) & np.isfinite(Y)
X, Y, C = X[ok], Y[ok], C[ok]

# K3 machinery (identical conventions to S02)
r_mig = [r for r in l06["results"] if "MIGHTEE" in r.get("name", "")][0]
D_full = float(np.mean(Y*Y - X*X - A0*X))
k3a = abs(D_full/r_mig["Delta"] - 1.0) < 1e-6
check("K3a full Delta matches L06 (1e-6)", k3a, f"rebuild={D_full:.6e} stored={r_mig['Delta']:.6e}")
dm = X < DEEP*A0
Xd, Yd, Cd = X[dm], Y[dm], C[dm]
ratio = ratio_stat(Xd, Yd)
k3b = abs(ratio - n05["mightee_deep"]["a0eff_a0"]) < 1e-9
check("K3b deep ratio matches N05 (1e-9)", k3b, f"rebuild={ratio:.6f} stored={n05['mightee_deep']['a0eff_a0']:.6f}")

lg = np.log10(Xd / A0)
b1 = lg < -1.0; b2 = (lg >= -1.0) & (lg < np.log10(DEEP))
n1, n2 = int(b1.sum()), int(b2.sum())
check("K1 both bins n >= 15", n1 >= 15 and n2 >= 15, f"n1={n1} n2={n2} (deep N={len(Xd)})")
r1, r2 = ratio_stat(Xd[b1], Yd[b1]), ratio_stat(Xd[b2], Yd[b2])
mlg1, mlg2 = float(lg[b1].mean()), float(lg[b2].mean())
slope = (r2 - r1) / (mlg2 - mlg1)

def slope_stat(m):  # bootstrap over colour groups
    if m[b1].sum() < 3 or m[b2].sum() < 3: return np.nan
    a, b = ratio_stat(Xd[m & b1], Yd[m & b1]), ratio_stat(Xd[m & b2], Yd[m & b2])
    return (b - a) / (mlg2 - mlg1)
vals = boot(Cd, slope_stat)
v = vals[~np.isnan(vals)]
se_slope = float(v.std(ddof=1)); n_ok = int(len(v))
z_slope = slope / se_slope if se_slope > 0 else float("inf")
q02 = json.load(open(os.path.join(BASE, "Q02_results.json")))["main"]
z_diff = (slope - q02["slope_per_dex"]) / np.hypot(se_slope, q02["slope_se"])
verdict = ("UNDECIDABLE (K1 power: a bin n < 15 -> no verdict forced; slope informational only)"
           if not (n1 >= 15 and n2 >= 15)
           else ("STRUCTURE-ONSET" if abs(z_slope) >= 3.0 else "CONSTANT-WITHIN-CHANNEL"))
print(f"\nbin1 [lg<-1.0): r1={r1:.4f} (n={n1}, <lg>={mlg1:.3f})")
print(f"bin2 [-1.0,-0.699): r2={r2:.4f} (n={n2}, <lg>={mlg2:.3f})")
print(f"slope = {slope:.4f} +/- {se_slope:.4f} per dex ({n_ok}/{NBOOT} valid draws) -> z = {z_slope:+.2f}")
print(f"vs Q02 SPARC slope 0.3396+/-0.1204: z_diff = {z_diff:+.2f} (informational)")
print(f"VERDICT (pre-registered): {verdict}")
k1_ok = n1 >= 15 and n2 >= 15
check("K2 verdict recorded (either outcome a result)", True, f"{verdict}; z_slope={z_slope:.2f}")
res = {"lane": "U01_deep_structure", "N_deep": int(len(Xd)), "bins": {
        "bin1": {"n": n1, "ratio": r1, "mean_lg": mlg1}, "bin2": {"n": n2, "ratio": r2, "mean_lg": mlg2}},
    "slope": slope, "slope_se": se_slope, "boot_valid_draws": n_ok, "z_slope": float(z_slope),
    "q02_slope_comp": {"q02_slope": q02["slope_per_dex"], "q02_se": q02["slope_se"], "z_diff": float(z_diff)},
    "verdict": verdict, "checks": checks,
    "exit0": bool(all(c["pass"] for c in checks) and k3a and k3b and n_ok > 1000)}  # exit0 False when K1 fires: UNDECIDABLE is the honest outcome
json.dump(res, open(os.path.join(BASE, "U01_deep_structure_results.json"), "w"), indent=1)
print("U01 COMPLETE"); print("EXIT", 0 if res["exit0"] else 1)
