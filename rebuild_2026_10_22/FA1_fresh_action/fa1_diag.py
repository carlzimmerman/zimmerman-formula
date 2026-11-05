#!/usr/bin/env python3
"""FA1 post-result diagnostics, no label (written after fa1_results.json). Asks whether G-SEP's fail is a noise or threshold artefact:
f_SP at stricter thresholds (X-COP median, max), with the baryon curve smoothed (3-point running mean of V_b^2 in ln r), outer points only
(last third of each curve), and split by gas share at the point. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
R = json.load(open(os.path.join(HERE, "fa1_results.json"))); zx = np.array([c["zeta"] for c in R["xcop"]["rows"]])
TH = dict(zeta_c=R["zeta_c"], xcop_median=float(np.median(zx)), xcop_max=float(zx.max()))
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); KPC = 3.0857e19; Y = 0.5
def run(a0, smooth, outer):
    z_all, fg_all = [], []
    for f in sorted(glob.glob(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod", "*_rotmod.dat"))):
        a = np.loadtxt(f, comments="#", ndmin=2); Rk, Vg, Vd, Vb = a[:, 0], a[:, 3], a[:, 4], a[:, 5]
        V2 = np.sign(Vg) * Vg ** 2 + Y * Vd ** 2 + 1.4 * Y * Vb ** 2
        if smooth and len(V2) >= 3: V2 = np.r_[V2[0], (V2[:-2] + V2[1:-1] + V2[2:]) / 3.0, V2[-1]]
        M = V2 * Rk; z = np.full(Rk.shape, np.nan); ok = M > 0
        if ok.sum() >= 3: z[ok] = np.gradient(np.log(M[ok]), np.log(Rk[ok])) / 3.0
        gb = V2 * 1e6 / (Rk * KPC); sel = np.isfinite(z) & (gb > 0) & (gb < a0)
        if outer: sel &= np.arange(len(Rk)) >= (2 * len(Rk)) // 3
        fg = np.clip(np.sign(Vg) * Vg ** 2 / np.where(V2 > 0, V2, np.nan), 0, 1)
        z_all.append(z[sel]); fg_all.append(fg[sel])
    return np.concatenate(z_all), np.concatenate(fg_all)
O = {}
for foot, a0 in A0.items():
    for smooth in (False, True):
        for outer in (False, True):
            z, fg = run(a0, smooth, outer); k = f"{foot}|smooth={smooth}|outer={outer}"
            O[k] = dict(n=int(len(z)), **{f"f_{t}": float((z >= v).mean()) for t, v in TH.items()},
                        f_zc_gas_dominated=float((z[fg >= 0.5] >= TH["zeta_c"]).mean()), f_zc_star_dominated=float((z[fg < 0.5] >= TH["zeta_c"]).mean()))
            print(k, {q: round(v, 3) if isinstance(v, float) else v for q, v in O[k].items()})
json.dump(dict(thresholds=TH, rows=O), open(os.path.join(HERE, "fa1_diag.json"), "w"), indent=1, sort_keys=True)
