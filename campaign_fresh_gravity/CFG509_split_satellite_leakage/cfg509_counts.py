#!/usr/bin/env python3
"""CFG509 step 1 (MODEL-INDEPENDENT; no lensing is read): the photometric companion excess around the KiDS stack-P lenses,
measured SEPARATELY for the early (u - r > 2.0) and late classes, with CFG502's method verbatim:
  pool galaxies MORE massive than the lens within R_p < 0.5 Mpc (comoving), 10 < |dchi_phot| < 600 Mpc, minus the 4-6 Mpc annulus
  scaled by area (0.25 / 20). Per-lens counts are CFG502's staged arrays (cfg502_stage.npz: cin, can, can50), not recomputed.
Step 2 (the conversion, declared): CFG502's halo-model prediction per lens (pred_sat = leaked-satellite companions for f_W,
pred_2h = centrals' two-halo companions from the locally measured density) is read from cfg502_env_table.npz; the class
leakage scale is lambda_c = (meas_c - pred_2h,c) / pred_sat,c, so f_c(M*, z) = lambda_c f_W(M*, z).
Weights: the stack weight of each lens (sum over g_bar bins of WW, CFG502's 'wlens'); unweighted reported.
Errors: 50-patch jackknife (lr_esd_jackknife patches). Mass-matched and z-matched comparisons reported.
Weights from the shear catalogue (WW) are pair weights only; no shear value enters.
Output: cfg509_counts.out, cfg509_counts_results.json. Run: nice -n 15 python3 cfg509_counts.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import json, math
import numpy as np
from scipy.interpolate import RegularGridInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
W2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, RES, CHK = [], {"lane": "CFG509", "script": "cfg509_counts"}, {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


S = np.load(os.path.join(W2, "cfg502_stage.npz"))
ET = np.load(os.path.join(W2, "cfg502_env_table.npz"))
ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
iso = S["iso_idx"]
zl, lml, typ = S["z"][iso], S["logM"][iso], S["typ"][iso]
check("C0 staged ISO lenses = lr_lenses.npz order (z, logM, typ exact)",
      np.array_equal(zl, ln["z"]) and np.array_equal(lml, ln["logM"]) and np.array_equal(typ, ln["typ"]), f"N = {len(zl):,}")
area_in, area_an = math.pi * 0.25, math.pi * 20.0
cin, can, can50 = S["cin"], S["can"], S["can50"]
meas = cin - can * area_in / area_an
wl = S["WW"][iso].sum(1)
LMS, ZG = ET["LMS"], ET["ZG"]


def I2(tab):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(lml, LMS[0], LMS[-1]), np.clip(zl, ZG[0], ZG[-1])])


pred_sat = I2(ET["W10_pred_count"]); fW = I2(ET["W10_f"]); bc = I2(ET["W10_bc"]); bh = I2(ET["W10_bh"])
n3d = can50 / (area_an * 100.0)
beff = (1 - fW) * bc + fW * bh
pred_2h = n3d * beff * bc * np.interp(zl, ZG, ET["WPD"])
pred = pred_sat + pred_2h
rw = float((wl * meas).sum() / (wl * pred).sum())
check("C1 the all-lens stack-weighted measured/predicted ratio reproduces CFG502's 0.845 (+-0.001)", abs(rw - 0.845) < 0.001, f"{rw:.4f}")
NP = 50


def stat(mask, w):
    """stack-weighted (or unweighted) means and the class scale lambda with jackknife SDs."""
    def core(m):
        ww = w[m]
        a, ps, p2, f, bkg = ((ww * x[m]).sum() / ww.sum() for x in (meas, pred_sat, pred_2h, fW, can * area_in / area_an))
        return np.array([a, ps, p2, (a - p2) / ps, a / (ps + p2), f, ((a - p2) / ps) * f, bkg, (ww * cin[m]).sum() / ww.sum()])
    full = core(mask)
    jk = np.array([core(mask & (patch != k)) for k in range(NP)])
    sd = np.sqrt((NP - 1) / NP * ((jk - jk.mean(0)) ** 2).sum(0))
    return full, sd, jk


NAMES = ["meas_excess", "pred_sat", "pred_2h", "lambda", "meas_over_pred", "fW_model", "f_leak", "background", "raw_inner"]
CL = {"late": typ == 0, "early": typ == 1, "all": np.ones(len(typ), bool)}
RES["classes"] = {}
for wname, w in (("stack_weighted", wl), ("unweighted", np.ones_like(wl))):
    P(f"\n=== {wname}: more-massive companions within 0.5 Mpc (10 < |dchi| < 600), excess over the 4-6 Mpc annulus, per lens ===")
    P("  class   N        raw_in   bkg      EXCESS (jk)        pred_sat  pred_2h  meas/pred  lambda (jk)       f_W(model)  f_leak = lambda f_W")
    RES["classes"][wname] = {}
    jks = {}
    for c, m in CL.items():
        v, sd, jk = stat(m, w); jks[c] = jk
        RES["classes"][wname][c] = dict(N=int(m.sum()), **{n: float(x) for n, x in zip(NAMES, v)}, **{n + "_jk": float(x) for n, x in zip(NAMES, sd)})
        P(f"  {c:6s} {int(m.sum()):7d}  {v[8]:.4f}  {v[7]:.4f}  {v[0]:.4f} +- {sd[0]:.4f}   {v[1]:.4f}   {v[2]:.4f}   {v[4]:.3f}     "
          f"{v[3]:.3f} +- {sd[3]:.3f}    {v[5]:.3f}       {v[6]:.3f} +- {sd[6]:.3f}")
    for i, n in ((0, "excess"), (3, "lambda"), (6, "f_leak")):
        d = jks["early"][:, i] - jks["late"][:, i]
        full = RES["classes"][wname]["early"][NAMES[i]] - RES["classes"][wname]["late"][NAMES[i]]
        sd = math.sqrt((NP - 1) / NP * ((d - d.mean()) ** 2).sum())
        rat = RES["classes"][wname]["early"][NAMES[i]] / RES["classes"][wname]["late"][NAMES[i]]
        RES["classes"][wname][f"early_minus_late_{n}"] = dict(diff=full, jk=sd, ratio=rat)
        P(f"  early - late {n:7s}: {full:+.4f} +- {sd:.4f} ({full / sd:+.1f} sigma); early / late = {rat:.3f}")

# ------------------------------------------------------------------ matched comparisons (reported)
P("\n=== matched comparisons (stack-weighted): excess and lambda per class in log M* x z cells ===")
MB = [9.0, 9.75, 10.25, 10.5, 10.75, 11.01]
ZBn = [0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
cells = []
P("  log M*        z          N_late  N_early  excess_late  excess_early  lambda_late  lambda_early  ratio(lambda)")
for i in range(len(MB) - 1):
    for j in range(len(ZBn) - 1):
        m = (lml >= MB[i]) & (lml < MB[i + 1]) & (zl >= ZBn[j]) & (zl < ZBn[j + 1])
        ml, me = m & (typ == 0), m & (typ == 1)
        if ml.sum() < 300 or me.sum() < 300:
            continue
        r = {}
        for c, mm in (("late", ml), ("early", me)):
            ww = wl[mm]
            a, ps, p2 = ((ww * x[mm]).sum() / ww.sum() for x in (meas, pred_sat, pred_2h))
            r[c] = dict(N=int(mm.sum()), w=float(ww.sum()), excess=float(a), lam=float((a - p2) / ps))
        cells.append(dict(lm=[MB[i], MB[i + 1]], z=[ZBn[j], ZBn[j + 1]], **r))
        P(f"  {MB[i]:5.2f}-{MB[i + 1]:5.2f}  {ZBn[j]:.2f}-{ZBn[j + 1]:.2f}  {r['late']['N']:7d}  {r['early']['N']:7d}  {r['late']['excess']:10.4f}  "
          f"{r['early']['excess']:11.4f}  {r['late']['lam']:10.3f}  {r['early']['lam']:11.3f}  {r['early']['lam'] / r['late']['lam']:8.3f}")
# common-weight (matched) class ratio: each cell weighted by min of the two classes' stack weights
wc = np.array([min(c["late"]["w"], c["early"]["w"]) for c in cells])
le = np.array([c["early"]["lam"] for c in cells]); ll = np.array([c["late"]["lam"] for c in cells])
xe = np.array([c["early"]["excess"] for c in cells]); xl = np.array([c["late"]["excess"] for c in cells])
RES["matched"] = dict(cells=cells, lambda_early=float((wc * le).sum() / wc.sum()), lambda_late=float((wc * ll).sum() / wc.sum()),
                      excess_early=float((wc * xe).sum() / wc.sum()), excess_late=float((wc * xl).sum() / wc.sum()))
M = RES["matched"]
P(f"  matched (common cell weights): excess early {M['excess_early']:.4f} vs late {M['excess_late']:.4f} (ratio {M['excess_early'] / M['excess_late']:.3f}); "
  f"lambda early {M['lambda_early']:.3f} vs late {M['lambda_late']:.3f} (ratio {M['lambda_early'] / M['lambda_late']:.3f})")

# ------------------------------------------------------------------ radial split of the excess (reported; same area-scaled background)
P("\n  (reported) raw inner count split is not available per radius in the staged arrays; only R < 0.5 Mpc is staged (CFG502).")
RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, "cfg509_counts_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg509_counts.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(c["ok"] for c in CHK.values()) else 1)
