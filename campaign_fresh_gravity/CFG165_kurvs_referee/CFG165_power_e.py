#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG165 attack (e): power / calibration of the decision statistic at the decision cell, as frozen (N=20000, seed 165, re-run
seed 166).  ZF_REPO=<repo> python3 CFG165_power_e.py > CFG165_power.out ; rc 0."""
import os
import sys
import json
import math
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import gaussian_kde, norm
import CFG165_referee_kurvs_p4 as M

P = lambda *a: print(*a, flush=True)
N = 20000
SEEDS = (165, 166)
S = M.load_kurvs()
AS = M.load_sparc_anchor()
LN10 = M.LN10
p4 = M.SP["P4"]
xK = S.R / S.Reff - 1
al0 = M.alpha_K(xK)[None, :]
n = len(S.ids)

# analysis quantities that do not depend on the mock
gb0 = M.gbar(S, 0.67, 0.0)
aF = M.A0["canonical"] * np.ones(n)
aH = M.A0["canonical"] * M.E_of_z(S.z)
gpF, gpH = M.gpred(gb0, aF), M.gpred(gb0, aH)
emF = S.mass_err * np.abs(M.slope(gb0, aF))
emH = S.mass_err * np.abs(M.slope(gb0, aH))
ap = M.anchor_pool(p4, 0.0, "canonical", AS)["flat"]
AP0, AE = ap[0], ap[1]
cot = 1.0 / np.tan(S.inc)
real = M.cell(S, AS, p4, 0.67, 0.0, "canonical")
OBS_DP, OBS_SIG = real["flat"]["dprime"], real["flat"]["sigma"]
OBS_Z, OBS_ZH = real["flat"]["z"], real["H"]["z"]
P(f"observed (my main run): Delta'_flat {OBS_DP:+.4f} +-{OBS_SIG:.4f} ({OBS_Z:+.2f}s), Delta'_H {real['H']['dprime']:+.4f} ({OBS_ZH:+.2f}s); anchor {AP0:+.4f}+-{AE:.4f}")


def pool2(d, e):
    w = 1.0 / e ** 2
    m = np.sum(w * d, 1) / np.sum(w, 1)
    err = 1.0 / np.sqrt(np.sum(w, 1))
    chi = np.sum(w * (d - m[:, None]) ** 2, 1) / (n - 1)
    return m, err * np.sqrt(np.maximum(chi, 1.0))


def run(law, fam, seed, drop=False):
    rng = np.random.default_rng(seed)
    logM = S.logM[None, :] + rng.normal(0, 0.15, (N, n))
    Ms = 10.0 ** logM
    if fam == "ideal":
        mu = np.full((N, 1), 0.67)
        alpha_true = np.broadcast_to(al0, (N, n)).copy()
    else:
        med = 1.0 if fam == "N1" else 2.0
        mu = 10 ** rng.normal(math.log10(med), 0.3, (N, 1))
        alpha_true = al0 * np.exp(rng.normal(0, 0.4, (N, n))) * np.exp(rng.normal(0, 0.2, (N, 1)))
    Mb = Ms * M.enclosed(S.R / S.Rd)[None, :] + mu * Ms * M.enclosed(S.R / (2 * S.Rd))[None, :]
    gbt = M.G * Mb * M.MSUN / (S.R * M.KPC) ** 2
    a = aF if law == "flat" else aH
    off = AP0 + rng.normal(0, AE, (N, 1))
    gtrue = M.nu_mono(gbt / a[None, :]) * gbt * 10.0 ** off
    Vc2 = gtrue * (S.R * M.KPC) / 1e6
    V2 = Vc2 - alpha_true * S.sig[None, :] ** 2
    floor_mask = V2 < 0.0025 * Vc2
    floored = float(np.mean(floor_mask))
    V2 = np.maximum(V2, 0.0025 * Vc2)
    dinc = rng.normal(0, S.einc[None, :], (N, n))
    Vobs = np.sqrt(V2) * np.sin(S.inc)[None, :] / np.sin(S.inc[None, :] + dinc) + rng.normal(0, S.eV[None, :], (N, n))
    Vobs = np.maximum(Vobs, 1.0)
    sig = np.maximum(S.sig[None, :] + rng.normal(0, S.esig[None, :], (N, n)), 1.0)
    # analysis: exactly the P4 pipeline
    Vc2a = Vobs ** 2 + al0 * sig ** 2
    gobs = Vc2a * 1e6 / (S.R * M.KPC)
    ev = 2 * Vobs * S.eV[None, :] / Vc2a / LN10
    es = 2 * al0 * sig * S.esig[None, :] / Vc2a / LN10
    ei = (2 * Vobs ** 2 / Vc2a / LN10) * cot[None, :] * S.einc[None, :]
    res = {}
    for nm, gp, em in (("flat", gpF, emF), ("H", gpH, emH)):
        d = np.log10(gobs) - np.log10(gp)[None, :]
        e = np.sqrt(ev ** 2 + es ** 2 + ei ** 2 + em[None, :] ** 2)
        if drop:
            e = np.where(floor_mask, 1e6, e)
        m, err = pool2(d, e)
        dp = m - AP0
        sg = np.sqrt(err ** 2 + AE ** 2)
        res[nm] = (dp, sg)
    return res, floored


def classes(zf, zh):
    fw, rw = np.abs(zf) <= 2, np.abs(zh) <= 2
    lf = fw & (zh < -2)
    lr = rw & (zf > 2)
    nd = ~(lf | lr)
    return lr.mean(), lf.mean(), nd.mean()


OUT = {}
P("families: truth law x {ideal (mu=0.67, alpha exact), N1 (mu_true lognormal median 1.0, 0.3 dex; alpha x lognormal(0,.4) per galaxy x coherent lognormal(0,.2)), N2 (same, median 2.0)}")
P(f"N = {N} trials per family; seeds {SEEDS}")
for seed in SEEDS:
    P("\n" + "=" * 100 + f"\nseed {seed}\n" + "=" * 100)
    store = {}
    for fam in ("ideal", "N1", "N2"):
        for law in ("flat", "H"):
            res, fl_ = run(law, fam, seed)
            dpf, sgf = res["flat"]
            dph, sgh = res["H"]
            zf, zh = dpf / sgf, dph / sgh
            lr, lf, nd = classes(zf, zh)
            store[(fam, law)] = dpf
            row = dict(mean_dpf=float(dpf.mean()), sd_dpf=float(dpf.std()), mean_dph=float(dph.mean()), mean_sig=float(sgf.mean()),
                       P_z_ge_3p3=float(np.mean(zf >= 3.3)), P_dp_ge_obs=float(np.mean(dpf >= OBS_DP)),
                       P_lean_rival=float(lr), P_lean_flat=float(lf), P_nondiag=float(nd), P_zH_within_0p5=float(np.mean(np.abs(zh) <= 0.5)),
                       P_both=float(np.mean((zf >= 3.3) & (np.abs(zh) <= 2))), frac_V2_floored=fl_)
            OUT[f"{seed}|{fam}|{law}"] = row
            P(f"  truth={law:4s} {fam:5s}: Delta'_flat mean {row['mean_dpf']:+.3f} sd {row['sd_dpf']:.3f} (mean sigma {row['mean_sig']:.3f}); Delta'_H mean {row['mean_dph']:+.3f};  P(z_flat>=3.3)={row['P_z_ge_3p3']:.4f}  P(Delta'>=obs)={row['P_dp_ge_obs']:.4f}  classes [lean rival {lr:.3f}, lean flat {lf:.3f}, non-diag {nd:.3f}]  V2 floored {fl_:.4f}")
    P("\n  likelihood ratio at the observed Delta'_flat (rival-truth density / flat-truth density)")
    for fam in ("ideal", "N1", "N2"):
        a, b = store[(fam, "flat")], store[(fam, "H")]
        lg = norm.pdf(OBS_DP, a.mean(), a.std())
        lh = norm.pdf(OBS_DP, b.mean(), b.std())
        kde_f, kde_h = gaussian_kde(a[:8000])(OBS_DP)[0], gaussian_kde(b[:8000])(OBS_DP)[0]
        OUT[f"{seed}|{fam}|LR"] = dict(gauss=float(lh / lg) if lg > 0 else float("inf"), kde=float(kde_h / kde_f) if kde_f > 0 else float("inf"))
        P(f"   {fam:5s}: LR Gaussian-fit {lh/lg if lg>0 else float('inf'):10.3g}   KDE {kde_h/kde_f if kde_f>0 else float('inf'):10.3g}")

P("\n-- EXTRA, NOT FROZEN (disclosed): trials where the truth gives V^2<0.0025 Vc^2 (pressure term exceeds the whole circular speed) treat that galaxy as unobservable (dropped from the pool)")
for fam in ("ideal", "N1", "N2"):
    for law in ("flat", "H"):
        res, fl_ = run(law, fam, 165, drop=True)
        dpf, sgf = res["flat"]
        dph, sgh = res["H"]
        lr, lf, nd = classes(dpf / sgf, dph / sgh)
        OUT[f"165|drop|{fam}|{law}"] = dict(mean_dpf=float(dpf.mean()), sd_dpf=float(dpf.std()), P_lean_rival=float(lr), P_lean_flat=float(lf), P_nondiag=float(nd), P_dp_ge_obs=float(np.mean(dpf >= OBS_DP)))
        P(f"  drop truth={law:4s} {fam:5s}: Delta'_flat mean {dpf.mean():+.3f} sd {dpf.std():.3f}  P(Delta'>=obs) {np.mean(dpf >= OBS_DP):.4f}  classes [lean rival {lr:.3f}, lean flat {lf:.3f}, non-diag {nd:.3f}]")
P("\n-- PRE-DECLARED READING (seed 165)")
for fam in ("N1", "N2"):
    pf = OUT[f"165|{fam}|flat"]["P_lean_rival"]
    ph = OUT[f"165|{fam}|H"]["P_lean_rival"]
    P(f"  {fam}: P(lean rival | flat truth) = {pf:.3f} (need < 0.05), P(lean rival | rival truth) = {ph:.3f} (need > 0.3): "
      + ("'conditional lean' JUSTIFIED as stated" if (pf < 0.05 and ph > 0.3) else "NOT justified as stated (weak evidence)" if pf >= 0.10 else "borderline"))
json.dump(OUT, open(os.path.join(M.HERE, "CFG165_power_results.json"), "w"), indent=1)
P("\nwritten CFG165_power_results.json")
