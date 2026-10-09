#!/usr/bin/env python3
"""CFG505 masses: the mass sets of FROZEN_CRITERIA.md section 2 (398405fc8) and the mass comparison (no lensing quantity here).

M0 LePhare MASS_MED + 0.15 | M1 Bell+03 g-i -> M/L_i | M1b u-r -> M/L_K | M1c g-r -> M/L_r | M2 = M1 + UV dust (Meurer IRX-beta, Calzetti)
where beta is measured | M2i the selection-bias bracket | M2_MUT the shuffled-UV MUTATE set. M_gal = M* (1 + f_cold(log M*)).
Inputs: lr_lenses.npz, the KiDS bright-sample LePhare file, ../../../_external_data/cfg505_work/cfg505_uv_table.npz (cfg505_match.py).
Output: ../../../_external_data/cfg505_work/cfg505_masses.npz ; cfg505_masses.out / cfg505_masses_results.json
Run: nice -n 15 python3 cfg505_masses.py
"""
import os, sys, json, math, re
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg505_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, CHK, RES = [], {}, {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
UV = np.load(os.path.join(WORK, "cfg505_uv_table.npz"))
typ, z, lM0 = ln["typ"].astype(int), ln["z"].astype(float), ln["logM"].astype(float)
NL = len(typ)
L = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"))[1].data
ib = UV["ib"]
assert np.allclose(np.asarray(L["MASS_MED"], float)[ib] + 0.15, lM0, atol=0, rtol=0)
mag = {b: np.asarray(L["MAG_ABS_" + b], float)[ib] for b in ("u", "g", "r", "i", "Ks")}
fcold = lambda lm: 10 ** (-0.69 * lm + 6.63)

# ------------------------------------------------------------------ Bell+03 Table 7 coefficients, checked against the copy on disk
TEX = os.path.join(REPO, "deepseek_push", "G114_data", "bell2003b", "lf.tex")
src = open(TEX).read()
def row(colour):
    line = [l for l in src.splitlines() if l.strip().startswith("$" + colour.replace("-", " - ") + "$")][0]
    nums = [float(x.replace("$-$", "-").replace("$", "").replace("\\\\", "").strip()) for x in line.split("&")[1:]]
    return dict(zip(["ag", "bg", "ar", "br", "ai", "bi", "az", "bz", "aJ", "bJ", "aH", "bH", "aK", "bK"], nums))
B = {c: row(c) for c in ("g-i", "u-r", "g-r")}
USED = dict(gi=(-0.152, 0.518), urK=(-0.273, 0.091), grr=(-0.306, 1.097))
okc = (abs(B["g-i"]["ai"] - USED["gi"][0]) < 1e-9 and abs(B["g-i"]["bi"] - USED["gi"][1]) < 1e-9 and abs(B["u-r"]["aK"] - USED["urK"][0]) < 1e-9
       and abs(B["u-r"]["bK"] - USED["urK"][1]) < 1e-9 and abs(B["g-r"]["ar"] - USED["grr"][0]) < 1e-9 and abs(B["g-r"]["br"] - USED["grr"][1]) < 1e-9)
IMF, FLUX = -0.15, 0.15
MSUN = dict(i=4.53, r=4.65, K=3.28)


def m_gi(g, i):
    return USED["gi"][0] + USED["gi"][1] * (g - i) + IMF + 0.4 * (MSUN["i"] - i) + FLUX


lM1 = m_gi(mag["g"], mag["i"])
lM1b = USED["urK"][0] + USED["urK"][1] * (mag["u"] - mag["r"]) + IMF + 0.4 * (MSUN["K"] - (mag["Ks"] - 1.85)) + FLUX
lM1c = USED["grr"][0] + USED["grr"][1] * (mag["g"] - mag["r"]) + IMF + 0.4 * (MSUN["r"] - mag["r"]) + FLUX


# ------------------------------------------------------------------ the UV dust term
def kcal(lam):
    lam = np.asarray(lam, float)
    blue = 2.659 * (-2.156 + 1.509 / lam - 0.198 / lam ** 2 + 0.011 / lam ** 3) + 4.05
    red = 2.659 * (-1.857 + 1.040 / lam) + 4.05
    return np.where(lam < 0.63, blue, red)


K16, KG_, KI_ = float(kcal(0.16)), float(kcal(0.477)), float(kcal(0.7625))


def afuv_of(rec):
    """A_FUV per lens from a UV record (dict of arrays); 0 where beta is not measured."""
    ok = rec["det"] & (rec["enuv"] <= 0.25) & (rec["efuv"] <= 0.25) & np.isfinite(rec["fuv"]) & np.isfinite(rec["nuv"])
    f0 = rec["fuv"] - 8.06 * rec["ebv"]; n0 = rec["nuv"] - 7.95 * rec["ebv"]
    beta = (f0 - n0) / 0.4303 - 2.0
    A = np.where(ok, np.clip(4.43 + 1.99 * beta, 0.0, 5.0), 0.0)
    return A, ok, np.where(ok, beta, np.nan)


def m2_from_A(A):
    Es = A / K16
    Ag, Ai = KG_ * Es, KI_ * Es
    return m_gi(mag["g"] - Ag, mag["i"] - Ai)          # (g-i)_0 = (g-i) - (A_g - A_i); M_i,0 = M_i - A_i


REC = {k: UV[k] for k in ("det", "enuv", "efuv", "fuv", "nuv", "ebv", "covered", "nondet", "nocov", "nuvr", "uvsf")}
A2, okb, beta = afuv_of(REC)
lM2 = m2_from_A(A2)
# M2i: covered lenses without a measured beta get their class's median A_FUV of the beta-measured lenses
Ai_ = A2.copy()
for c in (0, 1):
    med = float(np.median(A2[okb & (typ == c)]))
    Ai_[(typ == c) & REC["covered"] & ~okb] = med
    RES[f"M2i_imputed_AFUV_class{c}"] = med
lM2i = m2_from_A(Ai_)
# M2_MUT: the per-lens UV record permuted (seed 5050)
perm = np.random.default_rng(5050).permutation(NL)
RECM = {k: v[perm] for k, v in REC.items()}
A2m, okbm, _ = afuv_of(RECM)
lM2m = m2_from_A(A2m)

dz = float(np.max(np.abs(m2_from_A(np.zeros(NL)) - lM1)))
check("C4 Bell+03 coefficients equal the table on disk; M2 with A_FUV = 0 equals M1 exactly",
      okc and dz == 0.0, f"g-i (a_i, b_i) = ({B['g-i']['ai']}, {B['g-i']['bi']}); u-r (a_K, b_K) = ({B['u-r']['aK']}, {B['u-r']['bK']}); "
      f"g-r (a_r, b_r) = ({B['g-r']['ar']}, {B['g-r']['br']}); max |M2(A=0) - M1| = {dz:.1e}; Calzetti k(0.16, 0.477, 0.7625 um) = "
      f"{K16:.3f}, {KG_:.3f}, {KI_:.3f}; dlog M*/dA_FUV = {(-0.518 * (KG_ - KI_) + 0.4 * KI_) / K16:+.4f}")
P(f"  beta measured (FUV and NUV e <= 0.25): {int(okb.sum())} lenses (late {int((okb & (typ == 0)).sum())}, early {int((okb & (typ == 1)).sum())}); "
  f"beta median {np.nanmedian(beta):+.2f} (16-84 {np.nanpercentile(beta, 16):+.2f}..{np.nanpercentile(beta, 84):+.2f}); A_FUV median "
  f"{np.median(A2[okb]):.2f} (16-84 {np.percentile(A2[okb], 16):.2f}-{np.percentile(A2[okb], 84):.2f}; clipped at 0: {100 * np.mean(A2[okb] == 0):.0f}%, at 5: "
  f"{100 * np.mean(A2[okb] == 5):.0f}%); M2i imputes A_FUV {RES['M2i_imputed_AFUV_class0']:.2f} (late) / {RES['M2i_imputed_AFUV_class1']:.2f} (early)")
RES["beta"] = dict(n=int(okb.sum()), n_late=int((okb & (typ == 0)).sum()), n_early=int((okb & (typ == 1)).sum()),
                   beta_med=float(np.nanmedian(beta)), A_med=float(np.median(A2[okb])), clip0=float(np.mean(A2[okb] == 0)))

SETS = {"M0": lM0, "M1": lM1, "M1b": lM1b, "M1c": lM1c, "M2": lM2, "M2i": lM2i, "M2_MUT": lM2m}
ur = mag["u"] - mag["r"]
status = np.where(okb, "beta", np.where(REC["det"], "det_other", np.where(REC["nondet"], "nondet", "nocov")))
zt = np.quantile(z, [1 / 3, 2 / 3])
zbin = np.digitize(z, zt)


def rs(x): return float(1.4826 * np.median(np.abs(x - np.median(x))))


P("\nMASS COMPARISON: d = log M*(set) - log M*(M0, LePhare + 0.15)   [median | robust sd | slope vs u-r | Spearman rho(d, u-r)]")
for nm, lm in SETS.items():
    if nm == "M0":
        continue
    d = lm - lM0
    sl = float(np.polyfit(ur, d, 1)[0])
    rr = float(spearmanr(d, ur).correlation)
    line = {"all": (float(np.median(d)), rs(d), sl, rr)}
    for c, cn in ((0, "late"), (1, "early")):
        m = typ == c
        line[cn] = (float(np.median(d[m])), rs(d[m]), float(np.polyfit(ur[m], d[m], 1)[0]), float(spearmanr(d[m], ur[m]).correlation))
    for st in ("beta", "det_other", "nondet", "nocov"):
        m = status == st
        line[st] = (float(np.median(d[m])), rs(d[m]))
    for k in range(3):
        m = zbin == k
        line[f"z{k}"] = (float(np.median(d[m])), rs(d[m]))
    line["mean_all"] = float(np.mean(d)); line["mean_late"] = float(np.mean(d[typ == 0])); line["mean_early"] = float(np.mean(d[typ == 1]))
    line["diff_early_minus_late_mean"] = line["mean_early"] - line["mean_late"]
    line["diff_early_minus_late_median"] = line["early"][0] - line["late"][0]
    RES[f"cmp_{nm}"] = line
    P(f"  {nm:6s} all   {line['all'][0]:+.3f} | {line['all'][1]:.3f} | {line['all'][2]:+.3f} | {line['all'][3]:+.2f}   (mean {line['mean_all']:+.3f})")
    P(f"         late  {line['late'][0]:+.3f} | {line['late'][1]:.3f} | {line['late'][2]:+.3f} | {line['late'][3]:+.2f};  early {line['early'][0]:+.3f} | "
      f"{line['early'][1]:.3f} | {line['early'][2]:+.3f} | {line['early'][3]:+.2f};  early - late (median) {line['diff_early_minus_late_median']:+.3f}, "
      f"(mean) {line['diff_early_minus_late_mean']:+.3f}")
    P(f"         by UV status: beta {line['beta'][0]:+.3f} ({line['beta'][1]:.3f}), other det {line['det_other'][0]:+.3f}, non-det {line['nondet'][0]:+.3f}, "
      f"no cov {line['nocov'][0]:+.3f};  by z third: {line['z0'][0]:+.3f}, {line['z1'][0]:+.3f}, {line['z2'][0]:+.3f}")
for nm, ref in (("M2", "M1"), ("M2i", "M1"), ("M2_MUT", "M1")):
    d = SETS[nm] - SETS[ref]
    el = float(np.mean(d[typ == 1]) - np.mean(d[typ == 0]))
    RES[f"uvonly_{nm}"] = dict(mean=float(np.mean(d)), mean_late=float(np.mean(d[typ == 0])), mean_early=float(np.mean(d[typ == 1])), early_minus_late=el,
                               mean_beta=float(np.mean(d[okb])) if nm != "M2_MUT" else float(np.mean(d[okbm])), max=float(np.max(d)))
    P(f"  UV-only {nm} - {ref}: mean {np.mean(d):+.4f} dex (late {np.mean(d[typ == 0]):+.4f}, early {np.mean(d[typ == 1]):+.4f}; early - late {el:+.4f}); "
      f"over the beta-measured lenses {RES[f'uvonly_{nm}']['mean_beta']:+.4f}; max {np.max(d):+.3f}")
nuvr = REC["nuvr"]; detm = RECM["det"]
rho_m = float(spearmanr(RECM["nuvr"][detm & np.isfinite(RECM["nuvr"])], ur[detm & np.isfinite(RECM["nuvr"])]).correlation)
RES["rho_mut"] = rho_m
P(f"  shuffled UV record: Spearman rho((NUV-r), u-r) over (shuffled) detections {rho_m:+.3f} (real {UV['nuvr'][UV['det']].size and float(spearmanr(nuvr[REC['det']], ur[REC['det']]).correlation):+.3f})")
for nm, lm in SETS.items():
    P(f"  {nm:6s}: log M* median late {np.median(lm[typ == 0]):.3f}, early {np.median(lm[typ == 1]):.3f}; range {lm.min():.2f}-{lm.max():.2f}")

out = {}
for nm, lm in SETS.items():
    out["logM_" + nm] = lm
    out["Mgal_" + nm] = (ln["Mgal"].astype(float) if nm == "M0" else 10 ** lm * (1 + fcold(lm)))
out["uvsf"] = REC["uvsf"]; out["uvsf_mut"] = RECM["uvsf"]; out["beta_ok"] = okb; out["AFUV"] = A2
np.savez(os.path.join(WORK, "cfg505_masses.npz"), **out)
P("  wrote cfg505_masses.npz (data dir)")
RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, "cfg505_masses_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg505_masses.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(c["ok"] for c in CHK.values()) else 1)
