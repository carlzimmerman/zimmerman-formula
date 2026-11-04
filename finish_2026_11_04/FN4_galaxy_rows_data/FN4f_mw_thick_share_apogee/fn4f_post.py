#!/usr/bin/env python3
"""FN4f POST-RESULT diagnostic (after fn4f_share.py read NOT MEASURABLE; no label change; not in FROZEN_CRITERIA.md).
Two questions. (1) Was the failure the frozen trough finder? Re-run the same count-ratio estimator with a literature
high/low-alpha line, [Mg/Fe] = 0.12 - 0.13 [Fe/H] for [Fe/H] < 0 and 0.12 above (APOGEE convention, PROVISIONAL, from memory),
on the same sample and the same join. (2) Is the share measurable at all without a selection function? Show the share's
dependence on the assumed thin scale height h_lo, which the ratio slope kappa = 1/h_hi - 1/h_lo cannot fix.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4f_post.py -> fn4f_post.out / .json. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); A = dict(np.load(os.path.join(HERE, "cache", "cols.npz")))
R0, ZSUN = 8.122, 0.0208; OUT = []; RES = {}
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
dpos = np.hypot((A["RA"] - A["nn_RA"]) * np.cos(np.radians(A["DEC"])), A["DEC"] - A["nn_DEC"]) * 3600
idj = (A["APOGEE_ID"] == A["nn_APOGEE_ID"]) & (A["TELESCOPE"] == A["nn_TELESCOPE"])
fe = A["FE_H"]; mg = A["MG_FE"]; d = A["nn_weighted_dist"] / 1000
base = ((A["EXTRATARG"] == 0) & ((A["ASPCAPFLAG"] >> 23) & 1 == 0) & (A["SNR"] >= 70) & (A["LOGG"] >= 1.0) & (A["LOGG"] <= 3.5) & (A["TEFF"] >= 3900)
        & (A["TEFF"] <= 5500) & np.isfinite(fe) & np.isfinite(mg) & (A["FE_H_FLAG"] == 0) & (A["MG_FE_FLAG"] == 0) & (fe >= -1.0) & (fe <= 0.5)
        & np.isfinite(d) & (d > 0) & (A["nn_weighted_dist_error"] / A["nn_weighted_dist"] <= 0.2))
l = np.radians(A["GLON"]); b = np.radians(A["GLAT"]); x = R0 - d * np.cos(b) * np.cos(l); y = d * np.cos(b) * np.sin(l); Rg = np.hypot(x, y); az = np.abs(d * np.sin(b) + ZSUN)
P("FN4f POST-RESULT diagnostic (no label change). kappa = 1/2 FITTED; not theory closed.")
for jname, jm in (("frozen join (ID, telescope, position <= 1\")", idj & (dpos <= 1.0)), ("ID and telescope only (100 % of rows)", idj)):
    sel = base & jm & (Rg >= R0 - 1) & (Rg <= R0 + 1)
    hi = mg > np.where(fe < 0, 0.12 - 0.13 * fe, 0.12)
    edges = np.r_[np.arange(0.2, 2.41, 0.2), 2.5]; nh = np.histogram(az[sel & hi], edges)[0]; nl = np.histogram(az[sel & ~hi], edges)[0]
    zm = np.histogram(az[sel], edges, weights=az[sel])[0] / np.maximum(np.histogram(az[sel], edges)[0], 1)
    ok = (nh >= 5) & (nl >= 5); yv = np.log(nh[ok] / nl[ok]); w = 1 / (1 / nh[ok] + 1 / nl[ok]); X = np.c_[np.ones(ok.sum()), -zm[ok]]
    beta = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * yv)); r0, kap = math.exp(beta[0]), beta[1]
    rows = []
    for hlo in (0.20, 0.25, 0.30, 0.35, 0.40):
        den = kap + 1 / hlo; hhi = 1 / den if den > 0 else float("inf"); sN = r0 * hhi / (r0 * hhi + hlo) if np.isfinite(hhi) else 1.0
        rows.append(dict(h_lo=hlo, h_hi=hhi, share=sN))
    RES[jname] = dict(n=int(sel.sum()), n_hi=int((sel & hi).sum()), r0=r0, kappa=kap, by_hlo=rows, ratio_by_bin=(nh / np.maximum(nl, 1)).round(4).tolist())
    P(f"\n{jname}: solar-cylinder stars {int(sel.sum()):,} (high-alpha {int((sel & hi).sum()):,}); r0 {r0:.4f}, kappa {kap:.3f} per kpc")
    P("   h_lo (kpc) -> h_hi (kpc), share: " + "; ".join(f"{q['h_lo']:.2f} -> {q['h_hi']:.2f}, {q['share']:.3f}" for q in rows))
P("\nReading: the slope of the count ratio fixes only 1/h_hi - 1/h_lo. Each population's own vertical profile needs the selection")
P("function, so the share is set by the assumed thin scale height, not by the data.")
json.dump(RES, open(os.path.join(HERE, "fn4f_post.json"), "w"), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, "fn4f_post.out"), "w").write("\n".join(OUT) + "\n")
