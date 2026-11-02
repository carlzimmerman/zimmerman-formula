#!/usr/bin/env python3
"""K3: README numbers against their source JSONs. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
p, r, b, k = J("ux2_part2.json"), J("ux2_rows.json"), J("ux2_bench.json"), J("ux2_k2.json"); c = lambda n: J(f"cells/{n}.json")
T = [("omega_x", p["omega_x"]["median"], 0.1197, 5e-5), ("ratio", p["ratio"]["median"], 5.35, 5e-3), ("zeq", p["zeq"], 3397, 1), ("rho0", p["history"][0]["rho_x_kg_m3"], 2.249e-27, 1e-30), ("rho1090", p["history"][6]["rho_x_kg_m3"], 2.92e-18, 1e-20),
 ("xcop can", r["xcop"]["canonical"]["PC1,PC2 f=x"]["mean"], 0.406, 5e-4), ("xcop alt", r["xcop"]["alt"]["PC1,PC2 f=x"]["mean"], 0.376, 5e-4), ("U can", r["sparc"]["canonical"]["PC1,PC2 f=x"]["U"], 0.411, 5e-4), ("U alt", r["sparc"]["alt"]["PC1,PC2 f=x"]["U"], 0.377, 5e-4), ("U ls1 can", r["sparc"]["canonical"]["PC3 ls=1"]["U"], 0.461, 5e-4), ("U ls1 alt", r["sparc"]["alt"]["PC3 ls=1"]["U"], 0.416, 5e-4),
 ("IC can", r["ic1613"]["canonical"]["PC1,PC2 f=x"]["48.0"], -0.618, 5e-4), ("IC alt", r["ic1613"]["alt"]["PC1,PC2 f=x"]["48.0"], -0.655, 5e-4), ("bao PC1", b["B-Cosh"]["bao"], 28.6, 0.05), ("plik PC1g", b["B-Cosh-g"]["plik"], 681.35, 5e-3), ("bao PC2g", b["B-Exp-g"]["bao"], 42.0, 0.05), ("K2", k["d"], 2.16, 5e-3),
 ("w0", c("w+0")["chi2"]["plik"], 582.74, 5e-3), ("w+1e-3 bao", c("w+0.001")["chi2"]["bao"], 12.7, 0.05), ("cs2 1e-4", c("cs20.0001")["chi2"]["plik"], 717.60, 5e-3), ("control", c("control_noX")["chi2"]["plik"], 128270, 1)]
bad = 0
for n, v, w, t in T:
    ok = abs(v - w) <= t; bad += not ok; print(f"{'ok ' if ok else 'BAD'} {n}: {v:.6g} vs {w}")
readme = open(os.path.join(H, "README.md")).read(); print("K3", "PASS" if not bad else f"FAIL {bad}"); sys.exit(1 if bad else 0)
