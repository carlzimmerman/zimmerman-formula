#!/usr/bin/env python3
"""CFG503 POST-HOC diagnostics (not a verdict, nothing tuned): where the primary LCDM misfit sits relative to each lens's r_ta.
Reads cfg503_score_results.json (MAIN) and the CFG503 tables; recomputes the stack-P / ALL jackknife covariances (CFG502 code).
Output: cfg503_posthoc.out, cfg503_posthoc_results.json.   Run: nice -n 15 python3 cfg503_posthoc.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import json
import numpy as np
from scipy import stats
from scipy.interpolate import RegularGridInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG = []; RES = {"lane": "CFG503", "script": "cfg503_posthoc", "post_hoc": True}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2


def esd_full_loo(WG, WW, patch, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


M = json.load(open(os.path.join(HERE, "cfg503_score_results.json")))["MAIN"]
ET = np.load(os.path.join(WORK, "cfg503_env_table.npz")); OT = np.load(os.path.join(WORK, "cfg503_own_tables.npz"))
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
d, Cv = esd_full_loo(WG, WW, patch, np.ones(len(WW), bool))
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
Rm = np.array(J377["primary"]["meanR"])
gi, GS, GZ = OT["gi"], OT["GS"], OT["GZ"]
f = RegularGridInterpolator((ET["LMS"], ET["ZG"]), ET["moster_RTA"], bounds_error=False, fill_value=None)
rta_g = f(np.c_[np.clip(GS, 8.5, 11.0), np.clip(GZ, 0.1, 0.5)])
P("1. Pair-weighted r_ta (LCDM-equivalent, Moster) of the lenses contributing to each stack-P bin, and the primary LCDM pull:")
P("   R [Mpc] | r_ta 16/50/84% [Mpc] | R / median r_ta | pull (data - LCDM) / sigma")
lc = np.array(M["P"]["canonical"]["LCDM"]["model"]); sig = np.sqrt(np.diag(Cv))
rows = []
for k in range(15):
    w = np.bincount(gi, weights=WW[:, k], minlength=len(GS))
    o = np.argsort(rta_g); cw = np.cumsum(w[o]) / w.sum()
    q = [float(rta_g[o][np.searchsorted(cw, x)]) for x in (0.16, 0.5, 0.84)]
    rows.append(dict(R=float(Rm[k]), rta_q=q, pull=float((d[k] - lc[k]) / sig[k])))
    P(f"   {Rm[k]:6.3f}  | {q[0]:.2f} / {q[1]:.2f} / {q[2]:.2f}       | {Rm[k] / q[1]:5.2f}           | {(d[k] - lc[k]) / sig[k]:+5.2f}")
RES["bins"] = rows
# chi2 without the two r_ta-transition bins (1.04, 1.38 Mpc), Moster data covariance (post-hoc)
keep = ~np.isin(np.arange(15), [2, 3])
r = (d - lc)[keep]
c13 = float(hart(13) * r @ np.linalg.solve(Cv[np.ix_(keep, keep)], r))
r2 = d - lc
c2b = float(hart(15) * r2 @ np.linalg.solve(Cv, r2))
P(f"\n2. Primary LCDM on stack P, data covariance only: chi2 {c2b:.2f} / 15 with all bins; {c13:.2f} / 13 without the 1.04 and 1.38 Mpc bins "
  f"(p {stats.chi2.sf(c13, 13):.3f}). POST-HOC: dropping bins is not a validation.")
RES["chi2_15"] = c2b; RES["chi2_13_drop_rta_bins"] = c13; RES["p_13"] = float(stats.chi2.sf(c13, 13))
E = np.array(M["E_nlz_P"]); E0 = np.array(M["E_cfg502_P"])
P("\n3. E (stack P) at 1.82 / 1.38 / 1.04 / 0.78 Mpc: nonlinear " + " / ".join(f"{x:.3f}" for x in E[1:5]) + "; CFG502 linear "
  + " / ".join(f"{x:.3f}" for x in E0[1:5]) + ". The nonlinear term raises E beyond ~1.6 Mpc but LOWERS it at 1.0-1.4 Mpc: with a sharp "
  "exclusion at r_ta, the extra mass just outside r_ta projects to a negative Delta Sigma just inside it.")
RES["E_nlz"] = E.tolist(); RES["E_cfg502"] = E0.tolist()
json.dump(RES, open(os.path.join(HERE, "cfg503_posthoc_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg503_posthoc.out"), "w").write("\n".join(LOG) + "\n")
