#!/usr/bin/env python3
"""Q02 -- DEEP-REGIME ONSET TEST (doors: L06 4.2-sigma deep tension = OPEN; N05 sign-mirror).
Is the deep deficit a CONSTANT OFFSET (a0_eff/a0 flat across the deep band) or
STRUCTURE (onset/gradient)? Not the density-locality door (KILLED, N01): this tests
regime structure of the deficit inside SPARC, no rho->a0 law.
Kills pre-registered in QWAVE_BRIEF.md (K1 control, K2 slope verdict, K3 O04b consistency), written before this run."""
import json, math, os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 9.3619e-11
KMS2_KPC_TO_MS2 = 1.0e6 / 3.0856775814913673e19   # (km/s)^2/kpc -> m/s^2
rng = np.random.default_rng(20260924)

def build_rings():
    with open('/Users/carlzimmerman/new_physics/zimmerman-formula/glm53_push/data/rotation_curve_corpus_v7.json') as f:
        corpus = json.load(f)
    X, Y, gal = [], [], []
    for g in corpus['galaxies']:
        if g['survey'] != 'SPARC':
            continue
        m2l = g.get('m2l_disk')
        m2l = 0.5 if m2l is None else m2l
        name = g['galaxy']
        for row in g['data']:
            Vobs, Vgas, Vdisk, Vbul, Rad = row.get('Vobs'), row.get('Vgas'), row.get('Vdisk'), row.get('Vbul'), row.get('Rad')
            if Vobs is None or Rad is None or Vobs <= 0 or Rad <= 0:
                continue
            Vgas = 0.0 if Vgas is None else Vgas
            Vdisk = 0.0 if Vdisk is None else Vdisk
            Vbul = 0.0 if Vbul is None else Vbul
            vb2 = math.copysign(1.0, Vgas) * Vgas * Vgas + m2l * (Vdisk * Vdisk + Vbul * Vbul)
            if vb2 <= 0:
                continue
            conv = KMS2_KPC_TO_MS2
            X.append(vb2 / Rad * conv)
            Y.append(Vobs * Vobs / Rad * conv)
            gal.append(name)
    return np.array(X), np.array(Y), np.array(gal)

BINS = [(-2.5, -2.0), (-2.0, -1.5), (-1.5, -1.0), (-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5)]

def a0eff_bin(x, y, idx, boot_idx=None):
    if boot_idx is None:
        return (np.mean(y[idx]**2) - np.mean(x[idx]**2)) / np.mean(x[idx])
    b = idx[boot_idx[idx]]  # FIX-FORWARD 2026-09-24: boot_idx is a galaxy-membership BOOLEAN mask; first run indexed y directly with it -> IndexError dim 3389 vs 409
    return (np.mean(y[b]**2) - np.mean(x[b]**2)) / np.mean(x[b])

def run_ensemble(X, Y, gal, label):
    lg = np.log10(X / A0)
    rows = []
    B = 2000
    galaxies = np.unique(gal)
    gidx = {g: i for i, g in enumerate(galaxies)}
    gnum = np.array([gidx[g] for g in gal])
    for lo, hi in BINS:
        idx = np.where((lg >= lo) & (lg < hi))[0]
        N = len(idx)
        row = {"bin": f"[{lo},{hi})", "N": N, "status": "NOT-RESOLVED" if N < 100 else "resolved"}
        if N >= 100:
            point = a0eff_bin(X, Y, idx) / A0
            boots = np.empty(B)
            for b in range(B):
                draw = rng.choice(len(galaxies), size=len(galaxies), replace=True)
                mask = np.isin(gnum, draw)
                boots[b] = a0eff_bin(X, Y, idx, boot_idx=mask) / A0
            se = float(np.std(boots, ddof=1))
            row.update({"a0eff_over_a0": float(point), "se": se,
                        "z_vs_1": float((point - 1.0) / se),
                        "mean_lg": float(np.mean(lg[idx]))})
        rows.append(row)
    out = {"ensemble": label, "bins": rows}
    res = [r for r in rows if r["status"] == "resolved"]
    if len(res) >= 3:
        c = np.array([r["mean_lg"] for r in res])
        v = np.array([r["a0eff_over_a0"] for r in res])
        s = np.array([r["se"] for r in res])
        w = 1.0 / s**2
        slope_boots = []
        for b in range(B):
            vb = v + rng.standard_normal(len(v)) * s   # parametric bootstrap on bin values
            slope_boots.append(np.polyfit(c, vb, 1, w=np.sqrt(w))[0])
        slope = float(np.polyfit(c, v, 1, w=np.sqrt(w))[0])
        slope_se = float(np.std(slope_boots, ddof=1))
        out["slope_per_dex"] = slope
        out["slope_se"] = slope_se
        out["slope_z"] = slope / slope_se
        wmean = float(np.sum(w * v) / np.sum(w))
        wmean_se = float(np.sqrt(1.0 / np.sum(w)))
        out["weighted_mean"] = wmean
        out["weighted_mean_se"] = wmean_se
    return out

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

X, Y, gal = build_rings()
main = run_ensemble(X, Y, gal, "SPARC rings (real, corpus v7, L06/G071 conventions)")

# K1: synthetic line control, identical machinery
n = 8000
rng2 = np.random.default_rng(20260924 + 1)
Xs = A0 * 10.0 ** rng2.uniform(-12.4 + 10, -9.3 + 10, size=n)
Ys = np.sqrt(Xs**2 + A0 * Xs) * (1.0 + rng2.normal(0, 0.04, size=n))
gals = np.repeat(np.arange(n // 40), 40)
ctrl = run_ensemble(Xs, Ys, np.array([f"c{i}" for i in gals]), "SYNTHETIC LINE CONTROL (4% scatter)")

# K1 verdict: control a0_eff/a0 within 3 SE of 1 in every resolved bin
k1 = all(abs(r["a0eff_over_a0"] - 1.0) < 3 * r["se"] for r in ctrl["bins"] if r["status"] == "resolved") and len(ctrl["bins"]) == len(BINS)
k1 = k1 and all(r["status"] == "resolved" for r in ctrl["bins"])
check("K1 synthetic control passes (a0eff/a0=1 within 3 SE, all bins resolved)", k1,
      json.dumps(ctrl["bins"]))

# K2 verdict from slope
if "slope_per_dex" in main:
    verdict = "CONSTANT-OFFSET" if abs(main["slope_z"]) < 3.0 else "STRUCTURE"
    check("K2 slope verdict recorded", True,
          f"slope={main['slope_per_dex']:.4f}+/-{main['slope_se']:.4f}/dex z={main['slope_z']:.2f} -> {verdict}")
else:
    verdict = "NOT-RESOLVED"
    check("K2 slope verdict recorded", False, "fewer than 3 resolved bins in real ensemble")

# K3: weighted mean vs O04b joint 0.7172 +/- 0.0593
o04b, o04b_se = 0.7172, 0.0593
k3_note = ""
if "weighted_mean" in main:
    z_o04b = (main["weighted_mean"] - o04b) / math.sqrt(main["weighted_mean_se"]**2 + o04b_se**2)
    k3_note = f"weighted_mean={main['weighted_mean']:.4f}+/-{main['weighted_mean_se']:.4f} vs O04b 0.7172+/-0.0593, z={z_o04b:.2f}"
check("K3 consistency vs O04b recorded", True, k3_note)

resolved = [r for r in main["bins"] if r["status"] == "resolved"]
all_pass = k1
result = {
    "lane": "Q02_deep_onset", "seed": 20260924, "nboot": 2000, "a0": A0,
    "N_rings": int(len(X)), "N_galaxies": int(len(np.unique(gal))),
    "main": main, "control": ctrl, "verdict": verdict,
    "checks": checks, "exit0": all_pass,
}
with open(os.path.join(BASE, 'Q02_results.json'), 'w') as f:
    json.dump(result, f, indent=1)
print("Q02 COMPLETE;", "N_rings =", len(X), "N_galaxies =", len(np.unique(gal)))
print("verdict:", verdict)
for r in main["bins"]:
    print(r)
if "slope_per_dex" in main:
    print("slope:", main["slope_per_dex"], "+/-", main["slope_se"], "z:", main["slope_z"])
    print("weighted mean:", main["weighted_mean"], "+/-", main["weighted_mean_se"])
print("K1:", k1, "| K3:", k3_note)
print("EXIT", 0 if all_pass else 1)
