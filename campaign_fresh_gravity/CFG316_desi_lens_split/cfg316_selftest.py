#!/usr/bin/env python3
"""CFG316 SELFTEST: synthetic shear through the lane's estimator (the June agentK estimator, per lens) and split statistic.  The real
e1/e2 are NOT read: only source positions, lensfit weights and Z_B (pair geometry and Sigma_crit weights).  For every kept lens-source
pair the synthetic tangential ellipticity is e_t = Sigma_crit^-1 * DeltaSigma_inj(g_bar) + n, n ~ N(0, 0.28) (independent per pair).
  injected  DeltaSigma_inj(g) = 30 (g / 1e-13 m s^-2)^0.5 Msun/pc^2 (a deep-regime shape), the SAME function for both classes (D = 0),
            and a planted split: early x 1.5 (D = 0.5 ESD_late).
  lens sets  (i) the 48,497 matched good-mass lenses (geometry of the full overlap; class (b)); (ii) the frozen ISO-P set (296 lenses), the
            only non-empty frozen sample, with 50 noise realisations to calibrate the 30-patch jackknife chi2 at that size.
PRE-DECLARED tolerances
  T1  noiseless: the recovered per-class ESD equals the independently computed pair-weighted mean of DeltaSigma_inj to 1e-9 relative, and
      the noiseless D(equal) on K1 is below 3% of ESD_late in every bin (within-bin g distribution differences only).
  T2  noisy, set (i): equal injection -> chi2(D = 0) on K1 with the 30-patch jackknife has p > 0.01; planted split -> the amplitude
      A = D.C^-1.T / T.C^-1.T (template T = noiseless planted D) within 2 sigma of 1, and chi2(D = 0) rejects at p < 0.01.
  T3  set (ii): over 50 realisations of the equal injection, the mean Hartlap chi2 on K1 lies within 7 +- 30% (4.9-9.1), and the planted
      split's mean amplitude is within 2 sigma(mean) of 1.
Run from the repository root: python3 -u campaign_fresh_gravity/CFG316_desi_lens_split/cfg316_selftest.py
"""
import os, sys, json
import numpy as np
from scipy.stats import chi2 as CHI2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg316_common import *   # noqa
sys.path.insert(0, CFG)
import CFG7_common as C7       # noqa: E402

R = C7.Report("cfg316_selftest", False)
P, check = R.P, R.check
P(__doc__.split("Run from")[0].strip())
SIGE = 0.28
L = np.load(os.path.join(WORK, "cfg316_lenses.npz"))
S = read_shear_columns(["RAJ2000", "DECJ2000", "weight", "Z_B"])
S = {k: v.astype("f8") for k, v in S.items()}
zero = np.zeros(1)
st = Stacker(S["RAJ2000"], S["DECJ2000"], zero, zero, S["weight"], S["Z_B"])
say(f"sources {len(S['Z_B']):,} (positions, weights, Z_B only)")


def inj(g):
    return 30.0 * np.sqrt(g / 1e-13) * KG          # kg/m^2


def perlens_syn(idx, cls, factor_early, rng, nreal=1):
    """per-lens sums for synthetic shear: returns PLs (nreal, N, 4, 15) for noisy, PL0 (N, 4, 15) noiseless, and the independent
    pair-weighted mean of the injected DeltaSigma per (class, bin)."""
    N = len(idx)
    PL0 = np.zeros((N, 4, 15)); PLn = np.zeros((nreal, N, 4, 15))
    num = np.zeros((2, 15)); den = np.zeros((2, 15))
    for t, i in enumerate(idx):
        k, ww, isc, gb = st.pairs(L["ra"][i], L["dec"][i], L["z"][i], L["chi"][i], L["Mgal"][i])
        if len(k) == 0: continue
        fac = factor_early if cls[t] == 1 else 1.0
        sig = fac * inj(gb)
        et0 = isc * sig
        np.add.at(PL0[t, 0], k, ww * et0 / isc); np.add.at(PL0[t, 1], k, ww); np.add.at(PL0[t, 2], k, 1)
        np.add.at(num[cls[t]], k, ww * sig); np.add.at(den[cls[t]], k, ww)
        for r in range(nreal):
            et = et0 + rng.normal(0, SIGE, len(k)); ex = rng.normal(0, SIGE, len(k))
            np.add.at(PLn[r, t, 0], k, ww * et / isc); np.add.at(PLn[r, t, 1], k, ww); np.add.at(PLn[r, t, 3], k, ww * ex / isc)
    return PL0, PLn, num / np.maximum(den, 1e-300) / KG


def split_stats(PL, cls, patch, T=None):
    sel = np.ones(len(cls), bool)
    Sx = class_patch_sums(PL, cls, patch, sel)
    esd, loo = esd_loo(Sx)
    D = (esd[1] - esd[0])[K1]
    Cd = jk_cov(loo[:, 1, K1] - loo[:, 0, K1])
    h = hartlap(NPATCH, len(K1))
    x2 = float(D @ np.linalg.solve(Cd, D)) * h
    out = dict(esd=esd, D=D, C=Cd, chi2=x2, p=float(CHI2.sf(x2, len(K1))))
    if T is not None:
        Ci = np.linalg.inv(Cd)
        out["A"] = float(T @ Ci @ D) / float(T @ Ci @ T)
        out["sA"] = float(1 / np.sqrt(float(T @ Ci @ T) * h))
    return out


rng = np.random.default_rng(316)
# ------------------------------------------------------------------ set (i): the matched good-mass overlap lenses
mm = np.where(L["mass_ok"] & L["matched"])[0]
cls_i = L["clsb"][mm].astype(int); pat_i = L["patch"][mm]
R.banner(f"SET (i): {len(mm):,} matched good-mass lenses (early {int(cls_i.sum()):,}); 30 patches")
res = {}
for nm, fe in (("equal", 1.0), ("planted", 1.5)):
    PL0, PLn, wmean = perlens_syn(mm, cls_i, fe, rng, nreal=1)
    s0 = split_stats(PL0, cls_i, pat_i)
    dev = float(np.nanmax(np.abs(s0["esd"][:, K1] / wmean[:, K1] - 1)))
    res[nm] = dict(PL0=PL0, PLn=PLn[0], s0=s0, dev=dev, wmean=wmean)
    P(f"  {nm:8s} noiseless: ESD_late K1 {np.round(s0['esd'][0, K1], 2).tolist()}; D {np.round(s0['D'], 3).tolist()}; "
      f"max |ESD / pair-weighted mean - 1| {dev:.1e}")
Tpl = res["planted"]["s0"]["D"]
relD = float(np.max(np.abs(res["equal"]["s0"]["D"]) / res["equal"]["s0"]["esd"][0, K1]))
check("T1 SELFTEST noiseless: recovered ESD = the pair-weighted mean of the injected DeltaSigma to 1e-9; |D(equal)| < 3% of ESD_late per K1 bin",
      f"max deviation {max(res['equal']['dev'], res['planted']['dev']):.1e}; max |D_equal| / ESD_late {relD:.4f}; planted D / (0.5 ESD_late) "
      f"{np.round(Tpl / (0.5 * res['planted']['s0']['esd'][0, K1]), 3).tolist()}",
      max(res["equal"]["dev"], res["planted"]["dev"]) < 1e-9 and relD < 0.03)
se = split_stats(res["equal"]["PLn"], cls_i, pat_i, T=Tpl)
sp = split_stats(res["planted"]["PLn"], cls_i, pat_i, T=Tpl)
P(f"  noisy equal:   D {np.round(se['D'], 2).tolist()} +- {np.round(np.sqrt(np.diag(se['C'])), 2).tolist()}; chi2 {se['chi2']:.2f}/7 p {se['p']:.3f}; "
  f"A {se['A']:.3f} +- {se['sA']:.3f}")
P(f"  noisy planted: D {np.round(sp['D'], 2).tolist()}; chi2(0) {sp['chi2']:.2f}/7 p {sp['p']:.2e}; A {sp['A']:.3f} +- {sp['sA']:.3f}")
check("T2 SELFTEST noisy (set i): equal -> chi2(D=0) p > 0.01; planted -> A within 2 sigma of 1 and chi2(D=0) p < 0.01",
      f"equal p {se['p']:.3f}; planted A {sp['A']:.3f} +- {sp['sA']:.3f} ((A-1)/s {(sp['A'] - 1) / sp['sA']:+.2f}), p(0) {sp['p']:.1e}",
      se["p"] > 0.01 and abs(sp["A"] - 1) < 2 * sp["sA"] and sp["p"] < 0.01)

# ------------------------------------------------------------------ set (ii): the frozen ISO-P sample, 50 realisations
hb = L["mass_ok"] & L["matched"] & L["complete"]
ip = np.where(hb & L["isoP"])[0]
cls_p = L["clsb"][ip].astype(int); pat_p = L["patch"][ip]
R.banner(f"SET (ii): the frozen ISO-P sample, {len(ip)} lenses (early {int(cls_p.sum())}); 50 noise realisations")
NR = 50
PLe0, PLe, _ = perlens_syn(ip, cls_p, 1.0, rng, nreal=NR)
PLp0, PLp, _ = perlens_syn(ip, cls_p, 1.5, rng, nreal=NR)
Tp = split_stats(PLp0, cls_p, pat_p)["D"]
x2e, Ap, sAp = [], [], []
for r in range(NR):
    a = split_stats(PLe[r], cls_p, pat_p)
    b = split_stats(PLp[r], cls_p, pat_p, T=Tp)
    x2e.append(a["chi2"]); Ap.append(b["A"]); sAp.append(b["sA"])
x2e, Ap, sAp = map(np.array, (x2e, Ap, sAp))
mA, smA = float(np.mean(Ap)), float(np.std(Ap) / np.sqrt(NR))
P(f"  equal: Hartlap chi2 on K1 mean {x2e.mean():.2f}, median {np.median(x2e):.2f}, fraction p < 0.01 {np.mean(CHI2.sf(x2e, 7) < 0.01):.2f}")
P(f"  planted: amplitude mean {mA:.3f} +- {smA:.3f} (scatter {np.std(Ap):.3f}; median quoted sigma_A {np.median(sAp):.3f})")
check("T3 SELFTEST (set ii, ISO-P size): mean Hartlap chi2 of the equal injection in 4.9-9.1; planted mean amplitude within 2 sigma(mean) of 1",
      f"mean chi2 {x2e.mean():.2f}; mean A {mA:.3f} +- {smA:.3f}; per-realisation sigma_A ~ {np.median(sAp):.2f} (so a KiDS-size split is "
      f"{1 / np.median(sAp):.1f} sigma_A at this sample size, before shared systematics)",
      4.9 <= x2e.mean() <= 9.1 and abs(mA - 1) < 2 * smA)
R.num("T1", dict(dev=max(res["equal"]["dev"], res["planted"]["dev"]), relD=relD))
R.num("T2", dict(equal_p=se["p"], planted_A=sp["A"], planted_sA=sp["sA"], planted_p=sp["p"]))
R.num("T3", dict(mean_chi2=float(x2e.mean()), mean_A=mA, sem_A=smA, median_sA=float(np.median(sAp))))
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
