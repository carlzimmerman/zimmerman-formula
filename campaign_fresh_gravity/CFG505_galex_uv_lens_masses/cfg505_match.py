#!/usr/bin/env python3
"""CFG505 match: the per-lens GALEX table and the match statistics (no lensing quantity is read or computed here).

Inputs: ../../../_external_data/cfg505_work/xm_galex_ais.csv (GUVcat_AIS) and xm_gr5_mis.csv (GR5 MIS), from cfg505_fetch.py;
        lr_lenses.npz (stack P) and the KiDS bright-sample LePhare file (rest-frame magnitudes, K-corrections) for the rest-frame NUV - r.
Rules (written before the masses or any lensing re-score; repeated in FROZEN_CRITERIA.md):
  join      a match row joins to the lens whose uploaded (RA, Dec) it echoes (KD-tree, < 1e-6 deg); the NEAREST counterpart within 3" is kept.
  source    MIS is used where the lens has an MIS counterpart with a smaller NUV error than its AIS counterpart; else AIS.
  coverage  0.5 x 0.5 deg cells (RA, Dec): a cell is covered by a survey if >= 2 of its lenses have a counterpart in that survey.
            A lens with no counterpart in a covered cell is a NON-DETECTION (kept, with an upper limit); in no covered cell: NO COVERAGE.
  depth     the cell's 5-sigma NUV limit = median over its matched sources of m + 2.5 log10((1.0857/e_m)/5); survey median where a cell has
            fewer than 5 matched sources.
  colours   Galactic extinction: A_NUV = 7.95 E(B-V), A_FUV = 8.06 E(B-V) (E(B-V) of the GALEX row; for non-detections the cell median).
            rest-frame NUV - r: M_NUV = NUV_0 - DM(z) + 2.5 log10(1+z) (flat-f_nu K-correction), M_r = MAG_AUTO_CALIB - DM(z) - K_COR_r
            (LePhare), DM with H0 = 70, Om = 0.3 (the lens pipeline's cosmology). r is not extinction-corrected (bracket +-0.1 mag).
  classes   UV star-forming: detected and (NUV - r)_rest < 4; UV quiescent: detected and >= 5, or a lower limit >= 5; else green/unknown.
Output: ../../../_external_data/cfg505_work/cfg505_uv_table.npz ; cfg505_match.out / cfg505_match_results.json (this folder)
Run: nice -n 15 python3 cfg505_match.py
"""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import numpy as np
import pandas as pd
from astropy.io import fits
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg505_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG = []
RES = {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
ra, dec, z, typ = ln["ra"].astype(float), ln["dec"].astype(float), ln["z"].astype(float), ln["typ"].astype(int)
NL = len(ra)
b = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"))[1].data
L = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"))[1].data
tb = cKDTree(np.c_[np.asarray(b["RAJ2000"], float), np.asarray(b["DECJ2000"], float)])
dd, ib = tb.query(np.c_[ra, dec])
assert dd.max() == 0.0 and len(np.unique(ib)) == NL
rAUTO = np.asarray(b["MAG_AUTO_CALIB"], float)[ib]
Kr = np.asarray(L["K_COR_r"], float)[ib]
ur = np.asarray(L["MAG_ABS_u"], float)[ib] - np.asarray(L["MAG_ABS_r"], float)[ib]
Mr_gaap = np.asarray(L["MAG_ABS_r"], float)[ib]


def DM(zz):
    zg = np.linspace(0, 0.8, 4001); E = np.sqrt(0.3 * (1 + zg) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zg))]) * 299792.458 / 70.0   # Mpc
    dl = (1 + zz) * np.interp(zz, zg, chi)
    return 5 * np.log10(dl * 1e6 / 10)


dm = DM(z)
tl = cKDTree(np.c_[ra, dec])


def load(fn, cols):
    t = pd.read_csv(os.path.join(WORK, fn))
    d_, il = tl.query(np.c_[t["ra"].values, t["dec"].values])
    assert d_.max() < 1e-6, f"{fn}: a match row does not echo a lens coordinate ({d_.max():.2e} deg)"
    t["lens"] = il
    nmult = np.bincount(il, minlength=NL)
    t = t.sort_values(["lens", "angDist"]).drop_duplicates("lens", keep="first")
    out = {k: np.full(NL, np.nan) for k in cols}
    for k, c in cols.items():
        out[k][t["lens"].values] = t[c].values.astype(float)
    det = np.zeros(NL, bool); det[t["lens"].values] = True
    return out, det, nmult


A, detA, multA = load("xm_galex_ais.csv", dict(nuv="NUVmag", enuv="e_NUVmag", fuv="FUVmag", efuv="e_FUVmag", ebv="E(B-V)",
                                               sep="angDist", nafl="Nafl", fafl="Fafl", nexp="NUVexp"))
M, detM, multM = load("xm_gr5_mis.csv", dict(nuv="nuv_mag", enuv="nuv_magerr", fuv="fuv_mag", efuv="fuv_magerr", ebv="E_bv", sep="angDist",
                                             nafl="nuv_artifact", fafl="fuv_artifact"))
for D_ in (A, M):
    for k in ("fuv", "efuv"):
        bad = ~(D_[k] > 0) | (D_[k] > 90)
        D_[k][bad] = np.nan
P(f"CFG505 match statistics (stack P, {NL} lenses; late {int((typ == 0).sum())}, early {int((typ == 1).sum())})")
P(f"  AIS (GUVcat II/335): {int(detA.sum())} lenses with a counterpart within 3\" ({100 * detA.mean():.1f}%); lenses with >1 counterpart {int((multA > 1).sum())}; "
  f"median separation {np.nanmedian(A['sep']):.2f}\"; FUV also detected {int(np.isfinite(A['fuv']).sum())}")
P(f"  MIS (GR5 II/312):    {int(detM.sum())} lenses ({100 * detM.mean():.1f}%); >1 counterpart {int((multM > 1).sum())}; median sep {np.nanmedian(M['sep']):.2f}\"; "
  f"FUV {int(np.isfinite(M['fuv']).sum())}")
P(f"  both AIS and MIS: {int((detA & detM).sum())}; NUV mag median AIS {np.nanmedian(A['nuv']):.2f} (e {np.nanmedian(A['enuv']):.2f}), "
  f"MIS {np.nanmedian(M['nuv']):.2f} (e {np.nanmedian(M['enuv']):.2f})")
# false-match rate from the separation distribution: counterparts at 2.5-3.0" vs a uniform-density expectation (density x 2 pi r dr)
for nm, D_, det in (("AIS", A, detA), ("MIS", M, detM)):
    s = D_["sep"][det]
    n_out = np.sum((s > 2.5) & (s <= 3.0)); dens = n_out / NL / (math.pi * (3.0 ** 2 - 2.5 ** 2))   # per arcsec^2 per lens (upper bound)
    fm = dens * math.pi * 9.0
    P(f"  {nm}: counterparts at 2.5-3.0\" imply at most {fm:.4f} chance matches per lens within 3\" ({100 * fm / max(det.mean(), 1e-9):.1f}% of matches, "
      "an upper bound: true counterparts also populate the annulus)")
    RES[f"false_match_upper_{nm}"] = float(fm / max(det.mean(), 1e-9))
    mult = multA if nm == "AIS" else multM
    sec = float((mult > 1).sum()) / NL                      # a second source within 3": an empirical chance-coincidence rate per lens
    P(f"  {nm}: lenses with a SECOND counterpart within 3\": {sec:.4f} per lens, i.e. a chance-match rate of about {100 * sec / max(det.mean(), 1e-9):.1f}% "
      "of matches (the estimate used)")
    RES[f"false_match_second_{nm}"] = float(sec / max(det.mean(), 1e-9))

# ------------------------------------------------------------------ coverage and depth (0.5 deg cells)
cell = (np.floor(ra / 0.5).astype(np.int64) * 1000 + np.floor((dec + 90) / 0.5).astype(np.int64))
uc, ci = np.unique(cell, return_inverse=True)
cov, lim = {}, {}
for nm, D_, det in (("AIS", A, detA), ("MIS", M, detM)):
    ncell = np.bincount(ci, weights=det.astype(float), minlength=len(uc))
    cov[nm] = (ncell >= 2)[ci]
    m5 = D_["nuv"] + 2.5 * np.log10((1.0857 / D_["enuv"]) / 5.0)
    glob = float(np.nanmedian(m5[det]))
    lim_c = np.full(len(uc), glob)
    df = pd.DataFrame(dict(c=ci[det], m5=m5[det], e=D_["ebv"][det]))
    g = df.groupby("c")
    med = g["m5"].median(); cnt = g["m5"].count()
    ok = cnt[cnt >= 5].index.values
    lim_c[ok] = med.loc[ok].values
    lim[nm] = lim_c[ci]
    ebv_c = np.full(len(uc), float(np.nanmedian(D_["ebv"][det])))
    em = g["e"].median(); ebv_c[em.index.values] = em.values
    D_["ebv_cell"] = ebv_c[ci]
    P(f"  {nm} coverage: {100 * cov[nm].mean():.1f}% of lenses in covered cells ({int(cov[nm].sum())}); detected fraction inside coverage "
      f"{100 * det[cov[nm]].mean():.1f}%; 5-sigma NUV limit median {np.median(lim[nm][cov[nm]]):.2f} (16-84%: "
      f"{np.percentile(lim[nm][cov[nm]], 16):.2f}-{np.percentile(lim[nm][cov[nm]], 84):.2f})")
    RES[f"coverage_{nm}"] = float(cov[nm].mean()); RES[f"det_in_cov_{nm}"] = float(det[cov[nm]].mean())
    RES[f"nuv_lim5_median_{nm}"] = float(np.median(lim[nm][cov[nm]]))

# ------------------------------------------------------------------ combined UV record
useM = detM & (~detA | (M["enuv"] < A["enuv"]))
src = np.where(useM, 2, np.where(detA, 1, 0))
pick = lambda k: np.where(useM, M[k], A[k])
nuv, enuv, fuv, efuv = pick("nuv"), pick("enuv"), pick("fuv"), pick("efuv")
ebv = np.where(src > 0, pick("ebv"), np.where(cov["MIS"], M["ebv_cell"], A["ebv_cell"]))
covered = cov["AIS"] | cov["MIS"]
mlim = np.where(cov["MIS"], lim["MIS"], lim["AIS"])
det = src > 0
nondet = covered & ~det
nocov = ~covered & ~det
P(f"  combined: detected {int(det.sum())} ({100 * det.mean():.1f}%; MIS used for {int((src == 2).sum())}); covered non-detections {int(nondet.sum())} "
  f"({100 * nondet.mean():.1f}%); no coverage {int(nocov.sum())} ({100 * nocov.mean():.1f}%); detected outside a covered cell {int((det & ~covered).sum())}")
nuv0 = np.where(det, nuv, mlim) - 7.95 * ebv
fuv0 = fuv - 8.06 * ebv
Mnuv = nuv0 - dm + 2.5 * np.log10(1 + z)
Mr_tot = rAUTO - dm - Kr
nuvr = Mnuv - Mr_tot
is_lim = ~det
nuvr[nocov] = np.nan
fs = (Mr_gaap - Mr_tot) / 2.5
P(f"  check: total-vs-GAaP r flux scale (M_r,GAaP - M_r,AUTO)/2.5 median {np.median(fs):+.3f} dex (16-84% {np.percentile(fs, 16):+.3f} to "
  f"{np.percentile(fs, 84):+.3f}); the record's constant fluxscale is +0.15 dex")
RES["fluxscale_median_dex"] = float(np.median(fs))
UVSF = det & (nuvr < 4.0)
UVQ = (det & (nuvr >= 5.0)) | (is_lim & ~nocov & (nuvr >= 5.0))
for c, nm in ((0, "late"), (1, "early")):
    m = typ == c
    P(f"  {nm:5s}: detected {100 * det[m].mean():5.1f}%, covered non-det {100 * nondet[m].mean():5.1f}%, no coverage {100 * nocov[m].mean():4.1f}%; "
      f"(NUV-r)_rest of detections median {np.nanmedian(nuvr[m & det]):.2f} (16-84 {np.nanpercentile(nuvr[m & det], 16):.2f}-"
      f"{np.nanpercentile(nuvr[m & det], 84):.2f}); limits median > {np.nanmedian(nuvr[m & nondet]):.2f}; UV star-forming (<4) {100 * UVSF[m].mean():.1f}% "
      f"of the class; UV quiescent (>=5, incl. limits) {100 * UVQ[m].mean():.1f}%; FUV+NUV with e <= 0.25 both: "
      f"{int((m & det & (enuv <= 0.25) & (efuv <= 0.25)).sum())}")
    RES[f"{nm}"] = dict(det=float(det[m].mean()), nondet=float(nondet[m].mean()), nocov=float(nocov[m].mean()),
                        nuvr_med_det=float(np.nanmedian(nuvr[m & det])), uvsf=float(UVSF[m].mean()), uvq=float(UVQ[m].mean()))
zt = np.quantile(z, [1 / 3, 2 / 3])
for lo, hi, nm in ((0, zt[0], "z low third"), (zt[0], zt[1], "z mid third"), (zt[1], 1, "z high third")):
    m = (z >= lo) & (z < hi)
    P(f"  {nm} ({lo:.3f}-{hi:.3f}): detected {100 * det[m].mean():.1f}% (late {100 * det[m & (typ == 0)].mean():.1f}%, early {100 * det[m & (typ == 1)].mean():.1f}%)")
rho = spearmanr(nuvr[det], ur[det]).correlation
P(f"  Spearman rho((NUV-r)_rest, u-r) over detections: {rho:+.3f}  (MUTATE reference: shuffling destroys it)")
RES["rho_nuvr_ur"] = float(rho)
RES["n"] = dict(det=int(det.sum()), nondet=int(nondet.sum()), nocov=int(nocov.sum()), mis=int((src == 2).sum()), ais=int((src == 1).sum()),
                fuv_det=int(np.isfinite(fuv[det]).sum()), beta_ok=int((det & (enuv <= 0.25) & (efuv <= 0.25)).sum()))
np.savez(os.path.join(WORK, "cfg505_uv_table.npz"), src=src, nuv=nuv, enuv=enuv, fuv=fuv, efuv=efuv, ebv=ebv, mlim=mlim, covered=covered,
         det=det, nondet=nondet, nocov=nocov, nuvr=nuvr, is_lim=is_lim, uvsf=UVSF, uvq=UVQ, ib=ib, ur=ur, sepA=A["sep"], sepM=M["sep"],
         naflA=A["nafl"], fs=fs)
P("  wrote cfg505_uv_table.npz (data dir)")
json.dump(RES, open(os.path.join(HERE, "cfg505_match_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg505_match.out"), "w").write("\n".join(LOG) + "\n")
