#!/usr/bin/env python3
"""X48 first-principles diagnostic FP2 (reported, not graded): is each seed's r_-2 resolved? Power et al. (2003) two-body criterion
kappa = t_relax(r)/t_H = (sqrt(200)/8) N/lnN (rhobar(<r)/rho_crit(z_f))^-1/2 at r = r_-2 (kappa >~ 1 resolved), and r_-2 / eps.
Uses only committed A2 (ng 48) and A3 (ng 64) analyses and the runs' own snapshots; Omega_m from background A (EM1, read-only)."""
import io, contextlib, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.argv = [sys.argv[0]]
import x48_zoom as Z
with contextlib.redirect_stdout(io.StringIO()): Om = Z.cosmology()["Om"]
OUT, rows = [f"X48 FP2: Power-criterion resolution at r_-2, 1e12 (Omega_m {Om:.4f}); kappa = 1/2 FITTED; not theory closed"], []
for ng, f in ((48, "x48_analyze_results_ng48_A2.json"), (64, "x48_analyze_results_ng64_A3.json")):
    for k, o in sorted(json.load(open(os.path.join(HERE, f)))["runs"].items()):
        if o.get("ng") != ng or o.get("flag") != "ok" or abs(o["M"] / 1e12 - 1) > 1e-6: continue
        z = np.load(os.path.join(HERE, "runs", k, "snap_zf.npz"), allow_pickle=True); meta = json.loads(str(z["meta"])); m = float(np.ravel(z["m"])[0])
        zf = meta["zf"]; rhom0 = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3)
        rc = rhom0 * (1 + zf) ** 3 * (Om * (1 + zf) ** 3 + 1 - Om) / (Om * (1 + zf) ** 3)
        n, r = o["n_inside_rm2"], o["rm2"]; kap = math.sqrt(200) / 8 * n / math.log(n) * (n * m / (4 / 3 * math.pi * r ** 3) / rc) ** -0.5
        rows.append(dict(ng=ng, seed=o["seed"], cf=o["cf"], n_in=n, r_over_eps=r / meta["eps"], kappa=kap))
        OUT.append(f"  ng {ng} seed {o['seed']}: c_f {o['cf']:6.2f}  N(<r_-2) {n:5d}  r_-2/eps {r / meta['eps']:5.1f}  kappa {kap:6.2f}")
c = np.array([r_["cf"] for r_ in rows]); kk = np.array([r_["kappa"] for r_ in rows])
OUT.append(f"  Spearman-free check: median c_f where kappa < 2: {np.median(c[kk < 2]):.2f} (n {int((kk < 2).sum())}); kappa >= 2: {np.median(c[kk >= 2]):.2f} (n {int((kk >= 2).sum())})")
print("\n".join(OUT)); open(os.path.join(HERE, "x48_fp_resolution.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(Om=Om, rows=rows), open(os.path.join(HERE, "x48_fp_resolution.json"), "w"), indent=1)
