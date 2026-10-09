#!/usr/bin/env python3
"""CFG535 forecasts F1 (stacked outer shape S) and F2 (population self-calibration, joint amplitude A and shape S); FROZEN_CRITERIA.md section 4.
No data are scored. Shared nuisances are drawn per mock.  kappa = 1/2 FITTED."""
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

SEED, NN, NM = 535, 400, 400
FOOT = {"canonical": H.A0C, "alt": H.A0A}
KERN = {"nu_mono": H.NU, "nu_plain": lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))}
LAWS = ("FLAT", "H(z)", "PROXY")
SIG_A = 0.01
SIG_S_SET = (0.05, 0.03, 0.10)

c = pd.read_csv(os.path.join(REPO, "data_assembly/kmos3d_phibss/kmos3d_catalog.csv"))
s = c[(c.Z >= 1.4) & (c.Z <= 2.1) & (c.LMSTAR >= 9.8) & (c.RHALF > 0)].reset_index(drop=True)
z = s.Z.values.astype(float); lM = s.LMSTAR.values.astype(float)
Re = s.RHALF.values * np.array([H.kpc_per_arcsec(zz) for zz in z])
Rd = Re / H.XN
mu0 = 10 ** (0.06 - 3.3 * (np.log10(1 + z) - 0.65) ** 2 - 0.41 * (lM - 10.7))
RAT = {L: np.array([H.LAWS[L](zz) for zz in z]) for L in LAWS}
R1, R2 = 2.2 * Rd, 6.0 * Rd


def draw(rng, n):
    return dict(dM=rng.normal(0, 0.15, n), dmu=rng.normal(0, 0.25, n), fR=rng.uniform(1, 2, n),
                sig=45 + rng.normal(0, 8, n), PK=rng.random(n) < 0.5)


def alpha(R, Re_, PK, P0=False):
    if P0:
        return np.zeros_like(R)
    x = R / Re_ - 1
    aK = -0.146 * x ** 2 + 1.204 * x + 1.475
    aB = 2 * R / (Re_ / H.XN)
    return np.where(PK, aK, aB)


def predict(th, a0, nu, law, P0=False):
    """returns A (median log V_rot(2.2Rd)), S (median dlogV/dlogR 2.2-6 Rd), floored fraction, median y at 6 Rd; vectorised over draws."""
    Ms = 10 ** (lM[None, :] + th["dM"][:, None])
    Mg = Ms * mu0[None, :] * 10 ** th["dmu"][:, None]
    Rg = th["fR"][:, None] * Re[None, :]
    out = {}
    vr = []
    floored = 0
    for R in (R1, R2):
        RR = np.broadcast_to(R[None, :], Ms.shape)
        v2 = H.disc_v2(Ms, Re[None, :], RR) + H.disc_v2(Mg, Rg, RR)
        gN = v2 / RR * H.G2SI
        y = gN / (a0 * RAT[law][None, :])
        vc2 = v2 * nu(y)
        al = alpha(RR, Re[None, :], th["PK"][:, None], P0)
        vrot2 = vc2 - al * th["sig"][:, None] ** 2
        floored = floored + (vrot2 < 100.0)
        vr.append(np.sqrt(np.maximum(vrot2, 100.0)))
        if R is R2:
            out["y6"] = np.median(y, axis=1)
    Sg = np.log10(vr[1] / vr[0]) / np.log10(6.0 / 2.2)
    out["A"] = np.median(np.log10(vr[0]), axis=1)
    out["S"] = np.median(Sg, axis=1)
    out["floored_frac"] = (floored > 0).mean(axis=1)
    return out


def chi2(x, mean, cov):
    d = x - mean
    return np.einsum("...i,ij,...j->...", d, np.linalg.inv(cov), d)


res = {"lane": "CFG535 forecasts", "n_galaxies": int(len(s)), "z_median": float(np.median(z)), "logMstar_median": float(np.median(lM)),
       "Re_median_kpc": float(np.median(Re)), "mu0_median": float(np.median(mu0)), "cells": {}}
for fn, a0 in FOOT.items():
    for kn, nu in KERN.items():
        key = f"{fn}|{kn}"
        rng = np.random.default_rng([SEED, list(FOOT).index(fn), list(KERN).index(kn)])
        thc = draw(rng, NN)  # cloud draws (shared by all laws)
        clouds = {L: predict(thc, a0, nu, L) for L in LAWS}
        cell = {"clouds": {L: {"A_mean": float(clouds[L]["A"].mean()), "A_sd": float(clouds[L]["A"].std()),
                               "S_mean": float(clouds[L]["S"].mean()), "S_sd": float(clouds[L]["S"].std()),
                               "S_p16_p84": [float(np.percentile(clouds[L]["S"], 16)), float(np.percentile(clouds[L]["S"], 84))],
                               "floored_frac_mean": float(clouds[L]["floored_frac"].mean()), "y6_median": float(np.median(clouds[L]["y6"]))}
                           for L in LAWS}}
        th0 = dict(dM=np.zeros(1), dmu=np.zeros(1), fR=np.full(1, 1.5), sig=np.full(1, 45.0), PK=np.array([True]))
        th0B = dict(th0, PK=np.array([False]))
        cell["central"] = {L: {"S_PK": float(predict(th0, a0, nu, L)["S"][0]), "S_PB": float(predict(th0B, a0, nu, L)["S"][0]),
                               "S_P0": float(predict(th0, a0, nu, L, P0=True)["S"][0]), "A": float(predict(th0, a0, nu, L)["A"][0]),
                               "y6": float(predict(th0, a0, nu, L)["y6"][0])} for L in LAWS}
        # mocks: each draws its own shared nuisances
        thm = draw(rng, NM)
        F = {}
        for sigS in SIG_S_SET:
            blk = {}
            for truth, wrong in (("FLAT", "H(z)"), ("H(z)", "FLAT")):
                pm = predict(thm, a0, nu, truth)
                A = pm["A"] + rng.normal(0, SIG_A, NM)
                S = pm["S"] + rng.normal(0, sigS, NM)
                stats = {}
                for name, idx in (("A_only", [0]), ("S_only", [1]), ("joint", [0, 1])):
                    X = np.stack([A, S], 1)[:, idx]
                    c2 = {}
                    for L in (truth, wrong):
                        Y = np.stack([clouds[L]["A"], clouds[L]["S"]], 1)[:, idx]
                        cov = np.atleast_2d(np.cov(Y.T)) + np.diag([[SIG_A ** 2, sigS ** 2][i] for i in idx])
                        c2[L] = chi2(X, Y.mean(0), cov)
                    dc = c2[wrong] - c2[truth]
                    md = float(np.median(dc))
                    stats[name] = {"median_dchi2": md, "frac_gt4": float((dc > 4).mean()), "frac_gt9": float((dc > 9).mean()),
                                   "Z_eff": float(np.sign(md) * np.sqrt(abs(md)))}
                blk[f"truth_{truth}"] = stats
            F[f"sigS_{sigS}"] = blk
        cell["F2"] = F
        # F1 single-statistic Z_eff (separation / sqrt(stat^2 + shared^2))
        sep = clouds["FLAT"]["S"].mean() - clouds["H(z)"]["S"].mean()
        shared = max(clouds["FLAT"]["S"].std(), clouds["H(z)"]["S"].std())
        cell["F1"] = {"sep_S_flat_minus_rival": float(sep), "shared_sd": float(shared),
                      "Z_eff": {str(sg): float(abs(sep) / np.hypot(sg, shared)) for sg in SIG_S_SET}}
        sepA = clouds["FLAT"]["A"].mean() - clouds["H(z)"]["A"].mean()
        sharedA = max(clouds["FLAT"]["A"].std(), clouds["H(z)"]["A"].std())
        cell["A_single"] = {"sep_A_flat_minus_rival": float(sepA), "shared_sd": float(sharedA), "Z_eff": float(abs(sepA) / np.hypot(SIG_A, sharedA))}
        res["cells"][key] = cell

def cls(zv):
    return "CRISP" if zv >= 3 else "USEFUL" if zv >= 2 else "WEAK"

summ = {}
for name in ("A_only", "S_only", "joint"):
    zz = {k: min(v["F2"]["sigS_0.05"]["truth_FLAT"][name]["Z_eff"], v["F2"]["sigS_0.05"]["truth_H(z)"][name]["Z_eff"]) for k, v in res["cells"].items()}
    summ[name] = {"Z_eff_min_over_truths": zz, "class_primary_both_footings": cls(min(zz[f"canonical|nu_mono"], zz[f"alt|nu_mono"]))}
res["summary_F2_sigS0.05"] = summ
res["F1_class"] = cls(min(res["cells"]["canonical|nu_mono"]["F1"]["Z_eff"]["0.05"], res["cells"]["alt|nu_mono"]["F1"]["Z_eff"]["0.05"]))
zj = {k: summ["joint"]["Z_eff_min_over_truths"][k] for k in res["cells"]}
za = {k: summ["A_only"]["Z_eff_min_over_truths"][k] for k in res["cells"]}
res["hand_estimates"] = {"HE-F1_ZeffS_lt2_both_footings": all(res["cells"][k]["F1"]["Z_eff"]["0.05"] < 2 for k in res["cells"]),
                         "HE-F2_joint_ge_1.3xA_and_lt3": all(zj[k] >= 1.3 * za[k] and zj[k] < 3 for k in res["cells"])}
json.dump(res, open(os.path.join(HERE, "cfg535_forecast_results.json"), "w"), indent=1)

print(f"CFG535 forecasts: N {len(s)} galaxies, z_med {np.median(z):.2f}, logM* med {np.median(lM):.2f}, R_e med {np.median(Re):.2f} kpc, mu0 med {np.median(mu0):.2f}")
for k, v in res["cells"].items():
    print(f"\n== {k}")
    for L in LAWS:
        cl, ce = v["clouds"][L], v["central"][L]
        print(f"  {L:6s} cloud S {cl['S_mean']:+.3f}+-{cl['S_sd']:.3f}  A {cl['A_mean']:.3f}+-{cl['A_sd']:.3f}  floored {cl['floored_frac_mean']:.2f}  y6 {cl['y6_median']:.2f} | "
              f"central S_PK {ce['S_PK']:+.3f} S_PB {ce['S_PB']:+.3f} S_P0 {ce['S_P0']:+.3f}  A {ce['A']:.3f}")
    print(f"  F1: sep S {v['F1']['sep_S_flat_minus_rival']:+.3f}, shared sd {v['F1']['shared_sd']:.3f}, Z_eff {v['F1']['Z_eff']}")
    print(f"  A single: sep {v['A_single']['sep_A_flat_minus_rival']:+.3f}, shared sd {v['A_single']['shared_sd']:.3f}, Z_eff {v['A_single']['Z_eff']:.2f}")
    for sg, blk in v["F2"].items():
        print("  F2 " + sg + ": " + " | ".join(f"{t}: " + ", ".join(f"{n} Z {blk[t][n]['Z_eff']:+.2f} f9 {blk[t][n]['frac_gt9']:.2f}" for n in blk[t]) for t in blk))
print("\nsummary F2 (sigS 0.05):", json.dumps(summ, indent=None))
print("F1 class:", res["F1_class"])
print("hand estimates:", res["hand_estimates"])
