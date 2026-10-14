"""CFG765: pre-flight -- can the record's z ~ 2-2.7 KMOS3D fits (CFG270 T1) separate the orbital and universal formation clocks?

Criteria: FROZEN_CRITERIA.md (committed alone, 66b7ab21a). D_orb = nu(y); D_uni = 1 + f (nu - 1), f = 1 - exp(-a/3.47 Gyr).
kappa = 1/2 FITTED; not "theory closed".  Run: python3 cfg765.py   (CFG765_MUTATE=1: y := 0.01; exit 1 iff P1 then DIAGNOSTIC)
"""
import os, sys, csv, json, math

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG4_common as C4  # noqa: E402

MUT = os.environ.get("CFG765_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
rows = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG270_kmos3d_cube_fits", "cfg270_points_stageB.csv"))) if r["tier"] == "T1"]
y = np.array([0.01 if MUT else float(r["y"]) for r in rows])
nu = np.array([float(C4.nu_mono(v)) for v in y])
out = {"lane": "CFG765", "mutate": MUT, "n": len(rows)}
lines = [__doc__.strip(), f"\nfits (T1): {len(rows)}; y median {np.median(y):.2f} (16-84%: {np.percentile(y, 16):.2f}-{np.percentile(y, 84):.2f})"]
for a in (1.0, 3.0):
    f = 1 - math.exp(-a / 3.47)
    d = np.log10(nu) - np.log10(1 + f * (nu - 1))
    out[f"a{a:g}"] = dict(f=f, median_dex=float(np.median(d)), max_dex=float(d.max()), p84_dex=float(np.percentile(d, 84)))
    lines.append(f"  baryon age {a:g} Gyr: f_uni = {f:.3f}; separation median {np.median(d):.3f} dex, 84th pct {np.percentile(d, 84):.3f}, max {d.max():.3f}")
# y needed for 0.30 dex at a = 1 Gyr
f1 = 1 - math.exp(-1 / 3.47)
ys = 10 ** np.linspace(-4, 1, 5001)
sep = np.array([math.log10(float(C4.nu_mono(v))) - math.log10(1 + f1 * (float(C4.nu_mono(v)) - 1)) for v in ys])
yneed = float(ys[np.where(sep >= 0.30)[0][-1]]) if (sep >= 0.30).any() else None
out["y_needed_for_0.30dex"] = yneed
ds = np.log10(np.array([float(r["D"]) for r in rows]))
out["pooled_stat_err_dex"] = float(np.std(ds) / math.sqrt(len(ds)))
lines.append(f"  y needed for a 0.30-dex separation (a = 1 Gyr): y <= {yneed:.4f};  pooled statistical error of log D: {out['pooled_stat_err_dex']:.3f} dex "
             "(the shared +-0.15 dex baryon band does not average down)")
p1 = out["a1"]["median_dex"] >= 0.30
out["P1"] = "DIAGNOSTIC" if p1 else "NOT DIAGNOSTIC"
lines.append(f"\nVERDICT: P1 {out['P1']}")
print("\n".join(lines))
open(os.path.join(HERE, f"cfg765{TAG}.out"), "w").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, f"cfg765_results{TAG}.json"), "w"), indent=1)
sys.exit(1 if (MUT and p1) else 0)
