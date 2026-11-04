"""LAM10 core (criteria e70770e272): the single-slope chi2 profile fit over LAM9's 13-value Gamma_b grid, on LAM9's sample,
masks, templates, kinematics and alpha rule. LAM9's lam9_core is imported read-only. κ = ½ FITTED; not theory closed."""
import os, sys, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); L9DIR = os.path.join(RB, "LAM9_imf_from_spectra")
sys.path.insert(0, L9DIR)
import numpy as np
from ppxf.ppxf import ppxf
import lam9_core as L9
WORK = os.path.join(L9.EXT, "lam10_work_2026_11_04")
GAM = np.array([0.30, 0.50, 0.80, 1.30, 1.50, 1.80, 2.00, 2.30, 2.50, 2.80, 3.00, 3.30, 3.50])

def slope_alpha(w, cols, n_t):
    """LAM9's alpha rule on one slope's step-b weights (light weights in V; m = w / n_t)."""
    T = L9.tlib(); m = w / n_t[cols]; s = w.sum()
    alpha = float(np.sum(m * T["mass"][cols]) / np.sum(m * T["Lr"][cols] * T["ups_r13"][cols]))
    la = float(np.sum(w * np.log10(T["age"][cols] * 1e9)) / s); mh = float(np.sum(w * T["metal"][cols]) / s)
    ia = int(np.argmin(np.abs(np.log10(T["tab_age"]) + 9 - la))); im = int(np.argmin(np.abs(T["tab_mh"] - mh)))
    return dict(alpha=alpha, alpha_ku2=alpha * float(T["ratio_CH"][ia, im]), alpha_tian=alpha * float(T["ratio_KU"][ia, im]), lage=la, mh=mh)

def profile(p, tpl, lam_t, n_t, kin, variant, flux=None, dh4=0.0):
    good = p["goodA"] if variant == "A" else p["goodB"]; f = p["flux"] if flux is None else flux; st = L9.kin_start(kin, dh4); T = L9.tlib()
    chi2, dof, A = np.zeros(len(GAM)), np.zeros(len(GAM)), []
    for k, g in enumerate(GAM):
        cols = np.flatnonzero(np.abs(T["gamma"] - g) < 1e-9); tg = tpl[:, cols]   # 84 templates, (age, [M/H]) order
        pa = ppxf(tg, f, p["noise"], L9.VELSCALE, st, moments=6, fixed=[1] * 6, degree=-1, mdegree=10, goodpixels=good, lam=p["lam"], lam_temp=lam_t, quiet=True)
        chi2[k] = float(pa.chi2) * float(pa.dof); dof[k] = float(pa.dof); mp = pa.mpoly
        pb = ppxf(tg.reshape(tg.shape[0], 14, 6), f / mp, p["noise"] / mp * np.sqrt(float(pa.chi2)), L9.VELSCALE, st, moments=6, fixed=[1] * 6, degree=-1,
                  mdegree=0, regul=100, reg_dim=(14, 6), goodpixels=good, lam=p["lam"], lam_temp=lam_t, quiet=True)
        A.append(slope_alpha(np.asarray(pb.weights, float).ravel(), cols, n_t))
    j = int(np.argmin(chi2)); s = chi2[j] / dof[j]
    i3 = [0, 1, 2] if j == 0 else ([len(GAM) - 3, len(GAM) - 2, len(GAM) - 1] if j == len(GAM) - 1 else [j - 1, j, j + 1])
    edge = "low" if j == 0 else ("high" if j == len(GAM) - 1 else "")
    a, b, _ = np.polyfit(GAM[i3], chi2[i3] - chi2[j], 2)
    if edge: gbest = float(GAM[j])
    else: gbest = float(np.clip(-b / (2 * a), GAM[j - 1], GAM[j + 1])) if a > 0 else float(GAM[j])
    sigma = float(1 / np.sqrt(a / s)) if a > 0 else float("nan")
    pr = np.exp(-(chi2 - chi2[j]) / (2 * s)); gchi = float(np.sum(pr * GAM) / np.sum(pr))
    la_all = np.log10([x["alpha"] for x in A]); lalpha_chi = float(np.interp(gchi, GAM, la_all))
    best = A[j]
    return dict(gamma_best=gbest, gamma_grid=float(GAM[j]), j=j, edge=edge, sigma=sigma, s=float(s), chi2=chi2.tolist(), dof=dof.tolist(),
                alpha=best["alpha"], alpha_ku2=best["alpha_ku2"], alpha_tian=best["alpha_tian"], lage=best["lage"], mh=best["mh"],
                gamma_chi=gchi, lalpha_chi=lalpha_chi, alpha_all=[x["alpha"] for x in A])
