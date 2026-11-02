#!/usr/bin/env python3
"""UX5 post-result, no label: law's U in the 60-150 bins by distance method and inclination; MAP with wider priors not run. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
import numpy as np
sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS",): os.environ[v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); UL = os.path.join(os.path.dirname(HERE), "UL1_measured_upsilon_test"); sys.path.insert(0, UL); import ul1_core as C
G = C.load(); UPS = C.UPS; O = []; R = {}
vf = np.array([q["meta"]["Vflat"] for q in G]); Q = np.array([q["meta"]["Q"] for q in G]); I = np.array([q["meta"]["Inc"] for q in G]); fD = np.array([q["meta"]["fD"] for q in G]); eD = np.array([q["meta"]["eD"] / q["meta"]["D"] for q in G]); fb = np.array([q["Vbul"][-1] ** 2 / max(q["Vdisk"][-1] ** 2 + q["Vbul"][-1] ** 2, 1e-9) for q in G]); T = 1 + 0.4 * fb; Qs = (Q <= 2) & (I >= 30) & (vf > 0); S = Qs & (vf >= 60) & (vf < 150)
fs = np.array([q["Vdisk"][-1] ** 2 * 0.5 / max(q["Vdisk"][-1] ** 2 * 0.5 + abs(q["Vgas"][-1]) ** 2 * np.sign(q["Vgas"][-1]) + 0.7 * q["Vbul"][-1] ** 2, 1e-9) for q in G])
for f in ("canonical", "alt"):
    z = np.load(os.path.join(UL, "rows", f"law_{f}.npz")); m = np.where(z["A_c2b_refit_ws"] > 0, z["A_c2b_refit_wr2"] / np.maximum(z["A_c2b_refit_ws"], 1e-300), np.inf); u = UPS[np.argmin(m, axis=1)] * T
    def row(n, s):
        v = u[S & s]; b = np.random.default_rng(1).choice(v, (2000, len(v))) if len(v) else None; e = float(np.std(np.median(b, axis=1))) if len(v) else None; R[f + "|" + n] = dict(n=int(len(v)), U=float(np.median(v)) if len(v) else None, e=e); O.append(f"[{f}] {n}: n {len(v)} U_tot {np.median(v) if len(v) else float('nan'):.3f} +- {e if e else float('nan'):.3f}")
    row("all 60-150", S); row("Hubble flow fD=1", fD == 1); row("TRGB, Cepheid, SN, UMa fD>=2", fD >= 2); row("eD/D <= 0.10", eD <= 0.10); row("Inc >= 60", I >= 60); row("Inc < 60", I < 60); row("star share >= 0.5", fs >= 0.5); row("star share < 0.5", fs < 0.5); row("star share >= 0.5, fD>=2", (fs >= 0.5) & (fD >= 2))
open(os.path.join(HERE, "ux5_post.out"), "w").write("\n".join(O) + "\n"); json.dump(R, open(os.path.join(HERE, "ux5_post.json"), "w"), indent=1); print("\n".join(O))
