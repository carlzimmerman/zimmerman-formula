#!/usr/bin/env python3
"""CFG316 Stage A: lens counts after each frozen cut, the spectroscopic isolation flags, and the analytic power for D.  NO shear value is
read: from the KiDS-1000 shear catalogue only positions (RAJ2000, DECJ2000), MASK and the photo-z Z_B are read (footprint, source
density, source n(z) for the power estimate).

Frozen criteria: FROZEN_CRITERIA.md (c57c69a81), decisions D1-D9 binding.
  D1  good redshift: ZWARN == 0, DELTACHI2 > 40, SPECTYPE == 'GALAXY', COADD_FIBERSTATUS == 0.
  D2  KiDS footprint = HEALPix nside 1024 pixels holding SOM-gold sources; 0.1 < z < 0.5.
  D3  class (b) headline: KiDS LePhare u - r > 2.0 on lenses matched to the KiDS-bright catalogue; (a) variant: CIGALE rest-frame
      u - r = -2.5 log10(LNU_U / LNU_R), valley transferred by matching on the overlap (quantile map of the KiDS early fraction).
  D4  ISO-S: no neighbour with M* > 0.1 M*_lens within 3 Mpc physical transverse and |dv| < 1000 km/s; ISO-S4: 4 Mpc, |dv| < 2000 km/s;
      a BGS target without a good redshift counts as a neighbour if, placed at the lens redshift with the lens-class median M/L, it
      exceeds 0.1 M*_lens (frozen text); C1 contrast ISO-P: the committed KiDS photo-z rule (|dchi| < 10 Mpc, lr_esd_remeasure v4).
  D5  lenses whose 0.1 M*_lens neighbour census is not complete at r < 19.5 are DROPPED.
  D6  M* bins log M* 10.0-10.5, 10.5-11.0.
  CIGALE quality: the frozen text's proposal (not changed by D1-D9): 1/5 <= FLAG_MASSPDF <= 5 and AGNFRAC < 0.1.
Outputs (outside git): ../_external_data/cfg316_work/cfg316_lenses.npz; in this folder cfg316_stageA.out / cfg316_stageA_results.json.
Run from the repository root: python3 -u campaign_fresh_gravity/CFG316_desi_lens_split/cfg316_stageA.py
"""
import os, sys, json
import numpy as np
import fitsio, healpy as hp
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg316_common import *          # noqa
sys.path.insert(0, CFG)
import CFG7_common as C7             # noqa: E402

R = C7.Report("cfg316_stageA", False)
P, check = R.P, R.check
P(__doc__.split("Run from")[0].strip())
NSIDE = 1024

# ================================================================== 1. KiDS footprint (positions only)
R.banner("1. KiDS-1000 SOM-gold footprint (positions, MASK, Z_B only; no shear value read)")
K = read_shear_columns(["RAJ2000", "DECJ2000", "MASK", "Z_B"])
nsrc = len(K["RAJ2000"])
mu, mc = np.unique(K["MASK"], return_counts=True)
P(f"  sources {nsrc:,}; MASK values (top 6 by count): " + ", ".join(f"{int(a)}: {int(b):,}" for a, b in sorted(zip(mu, mc), key=lambda t: -t[1])[:6]))
pixK = hp.ang2pix(NSIDE, K["RAJ2000"], K["DECJ2000"], lonlat=True)
fpK = np.zeros(hp.nside2npix(NSIDE), bool); fpK[pixK] = True
apix = hp.nside2pixarea(NSIDE, degrees=True)
areaK = fpK.sum() * apix
P(f"  KiDS footprint: {fpK.sum():,} nside-{NSIDE} pixels = {areaK:.1f} deg2; raw source density {nsrc / areaK / 3600:.2f} arcmin^-2")
zbh, zbe = np.histogram(K["Z_B"], bins=np.linspace(0, 3, 301))
del K, pixK

# ================================================================== 2. DESI BGS_BRIGHT full + CIGALE
R.banner("2. DESI DR1 BGS_BRIGHT full (LSS v1.5) and the CIGALE VAC")
fb = fitsio.FITS(F_BGS)
B = fb[1].read(columns=["TARGETID", "RA", "DEC", "Z_not4clus", "ZWARN", "DELTACHI2", "SPECTYPE", "COADD_FIBERSTATUS",
                        "FLUX_R", "MW_TRANSMISSION_R"])
fb.close()
NB = len(B)
ra, dec, zsp = B["RA"].astype("f8"), B["DEC"].astype("f8"), B["Z_not4clus"].astype("f8")
spt = np.char.strip(B["SPECTYPE"].astype(str))
good = (B["ZWARN"] == 0) & (B["DELTACHI2"] > 40) & (spt == "GALAXY") & (B["COADD_FIBERSTATUS"] == 0)    # D1
with np.errstate(divide="ignore", invalid="ignore"):
    fr = B["FLUX_R"].astype("f8") / B["MW_TRANSMISSION_R"].astype("f8")
    rmag = 22.5 - 2.5 * np.log10(fr)
logF = np.log10(np.where(fr > 0, fr, np.nan))
tid = B["TARGETID"]
del B
pixB = hp.ang2pix(NSIDE, ra, dec, lonlat=True)
inK = fpK[pixB]
# overlap area: KiDS pixels inside the DESI target coverage (coverage at nside 256, where a pixel holds ~45 BGS targets)
cov256 = np.zeros(hp.nside2npix(256), bool); cov256[hp.ang2pix(256, ra, dec, lonlat=True)] = True
pk = np.where(fpK)[0]
th, ph = hp.pix2ang(NSIDE, pk)
area_ov = float(cov256[hp.ang2pix(256, th, ph)].sum() * apix)
P(f"  BGS_BRIGHT full: {NB:,} targets; D1-good {good.sum():,} ({100 * good.mean():.1f}%); in the KiDS footprint {inK.sum():,} "
  f"(D1-good {np.sum(inK & good):,}, {100 * np.sum(inK & good) / inK.sum():.1f}%)")
check("A0 (reported) the KiDS-1000 x BGS overlap area vs arXiv:2512.15960 Table 3 (448.2 deg2, nside 1024)",
      f"KiDS pixels inside the BGS coverage (nside-256 occupancy): {area_ov:.1f} deg2", True, load_bearing=False)

fc = fitsio.FITS(F_CIG)
CG = fc[1].read(columns=["TARGETID", "SURVEY", "PROGRAM", "LOGM", "FLAG_MASSPDF", "AGNFRAC", "LNU_U", "LNU_R"])
fc.close()
mb = (np.char.strip(CG["SURVEY"].astype(str)) == "main") & (np.char.strip(CG["PROGRAM"].astype(str)) == "bright")
CG = CG[mb]
o = np.argsort(CG["TARGETID"]); CG = CG[o]
assert len(np.unique(CG["TARGETID"])) == len(CG)
j = np.searchsorted(CG["TARGETID"], tid); j = np.clip(j, 0, len(CG) - 1)
hasC = CG["TARGETID"][j] == tid
logM = np.where(hasC, CG["LOGM"][j], np.nan).astype("f8")
flagm = np.where(hasC, CG["FLAG_MASSPDF"][j], np.nan)
agn = np.where(hasC, CG["AGNFRAC"][j], np.nan)
with np.errstate(divide="ignore", invalid="ignore"):
    ur_c = np.where(hasC, -2.5 * np.log10(CG["LNU_U"][j] / CG["LNU_R"][j]), np.nan)
del CG
flag_ok = hasC & (flagm >= 0.2) & (flagm <= 5) & np.isfinite(logM)
mass_ok = flag_ok & (agn < 0.1)                                                     # the frozen proposal
P(f"  CIGALE main/bright joined: {hasC.sum():,} of {NB:,}; FLAG_MASSPDF in [1/5, 5]: {flag_ok.sum():,}; and AGNFRAC < 0.1: {mass_ok.sum():,}")

# ================================================================== 3. KiDS-bright match (class b) and the KiDS photo-z pool (ISO-P)
R.banner("3. KiDS-bright LePhare match (class b) and the committed photo-z isolation rule (ISO-P)")
kb = fitsio.FITS(F_KB)[1].read(columns=["ID", "RAJ2000", "DECJ2000", "MAG_AUTO_CALIB", "zphot_ANNz2", "masked"])
kl = fitsio.FITS(F_KBL)[1].read(columns=["ID", "MASS_MED", "MAG_ABS_u", "MAG_ABS_r"])
assert np.array_equal(kb["ID"], kl["ID"])
kra, kdec = kb["RAJ2000"].astype("f8"), kb["DECJ2000"].astype("f8")
kz = kb["zphot_ANNz2"].astype("f8"); kr = kb["MAG_AUTO_CALIB"]; kmask = kb["masked"]
klm = kl["MASS_MED"].astype("f8") + FLUXSCALE_DEX
kur = (kl["MAG_ABS_u"] - kl["MAG_ABS_r"]).astype("f8")


def unitv(r_, d_):
    r_, d_ = np.radians(r_), np.radians(d_)
    return np.c_[np.cos(d_) * np.cos(r_), np.cos(d_) * np.sin(r_), np.sin(d_)]


treeKB = cKDTree(unitv(kra, kdec))

# ================================================================== 4. the lens sample, cut by cut
R.banner("4. Lens counts after each cut")
zwin = (zsp > 0.1) & (zsp < 0.5)
base0 = inK & good & zwin                                                           # D2 footprint, D1, D2 z
cnt = {}
cnt["BGS targets in the KiDS footprint (D2 footprint)"] = int(inK.sum())
cnt["+ D1 good redshift"] = int((inK & good).sum())
cnt["+ D2 0.1 < z < 0.5"] = int(base0.sum())
cnt["+ CIGALE main/bright match"] = int((base0 & hasC).sum())
cnt["+ CIGALE FLAG_MASSPDF in [1/5, 5]"] = int((base0 & flag_ok).sum())
cnt["+ CIGALE AGNFRAC < 0.1 (frozen proposal)"] = int((base0 & mass_ok).sum())
mrange = (logM > 8.0) & (logM < 11.0)
cnt["+ 8 < log M* < 11 (the original KiDS lens limit M* < 1e11)"] = int((base0 & mass_ok & mrange).sum())
# stack candidates: everything any sample or variant needs (no AGN cut, no D5, no match requirement)
cand = base0 & flag_ok & mrange
ic = np.where(cand)[0]
dd, kk = treeKB.query(unitv(ra[ic], dec[ic]), k=1)
sep = np.degrees(dd) * 3600
mt = (sep < 1.0) & (kmask[kk] == 0) & np.isfinite(kur[kk]) & np.isfinite(klm[kk])
kidx = np.where(mt, kk, -1)
clsb = np.where(mt, (kur[kk] > UR_SPLIT).astype(int), -1)
cnt["+ matched to KiDS-bright (< 1 arcsec, masked == 0, finite u-r)"] = int(np.sum(mt & mass_ok[ic]))
P(f"  match separations of the matched set: median {np.median(sep[mt]):.3f}\", 99th pct {np.percentile(sep[mt], 99):.3f}\"; "
  f"unmatched within 1\": {np.sum(sep < 1.0) - mt.sum():,} (masked or no u-r)")

# class (a): CIGALE rest-frame u - r, valley transferred by quantile-matching the KiDS early fraction on the matched overlap
mm = mt & mass_ok[ic]
fe_K = float(np.mean(clsb[mm] == 1))
t_a = float(np.quantile(ur_c[ic][mm], 1 - fe_K))
cls_a_all = (ur_c > t_a).astype(int)
agree = float(np.mean((ur_c[ic][mm] > t_a).astype(int) == clsb[mm]))
P(f"  class (a) valley: KiDS early fraction on the matched overlap {fe_K:.3f} -> CIGALE u-r threshold {t_a:.3f}; "
  f"agreement with class (b) {100 * agree:.1f}%")

# lens-class median M/L in the r band (observed frame, at the lens z), from all D1-good galaxies with a sane CIGALE mass
DLz = lambda z: chi_of(z) * (1 + z)
logU = logM - (logF + 2 * np.log10(DLz(np.clip(zsp, 1e-4, None))))
zb_ml = np.arange(0.05, 0.56, 0.01)
src = good & flag_ok & np.isfinite(logU) & (zsp > 0.05) & (zsp < 0.55)
MLT = np.full((2, len(zb_ml) - 1), np.nan)
for cl in (0, 1):
    s = src & (cls_a_all == cl)
    ib = np.digitize(zsp[s], zb_ml) - 1
    for b in range(len(zb_ml) - 1):
        v = logU[s][ib == b]
        if len(v) > 50: MLT[cl, b] = np.median(v)
zc_ml = 0.5 * (zb_ml[1:] + zb_ml[:-1])
for cl in (0, 1):
    bad = ~np.isfinite(MLT[cl]); MLT[cl, bad] = np.interp(zc_ml[bad], zc_ml[~bad], MLT[cl, ~bad])
P(f"  median log(M*/F_r D_L^2) early - late at z = 0.15 / 0.25 / 0.35: "
  + ", ".join(f"{np.interp(z, zc_ml, MLT[1]) - np.interp(z, zc_ml, MLT[0]):+.2f}" for z in (0.15, 0.25, 0.35)) + " dex")


def logU_at(z, cl):
    return np.where(cl == 1, np.interp(z, zc_ml, MLT[1]), np.interp(z, zc_ml, MLT[0]))


# per candidate lens: the M/L class = class (b) where matched, else class (a)
zl = zsp[ic]; lml = logM[ic]
cls_ml = np.where(clsb >= 0, clsb, cls_a_all[ic])
# D5 completeness: r magnitude of a 0.1 M*_lens galaxy at z_lens with the lens-class median M/L must be < 19.5
logF_lim = (lml - 1.0) - logU_at(zl, cls_ml) - 2 * np.log10(DLz(zl))
r_lim = 22.5 - 2.5 * logF_lim
complete = r_lim < 19.5
logF_lim_e = (lml - 1.0) - logU_at(zl, np.ones_like(cls_ml)) - 2 * np.log10(DLz(zl))
complete_e = (22.5 - 2.5 * logF_lim_e) < 19.5
cnt["+ D5 completeness (0.1 M*_lens census complete at r < 19.5)"] = int(np.sum(mm & complete))

# ================================================================== 5. spectroscopic isolation (ISO-S, ISO-S4)
R.banner("5. Spectroscopic isolation over all 6.4 M BGS_BRIGHT targets (observed and unobserved)")
treeB = cKDTree(unitv(ra, dec))
chil = chi_of(zl)
nb_logM_obs = np.where(good & flag_ok, logM, np.nan)          # CIGALE mass for good-z neighbours with a sane mass PDF
CH = 4000
hitS_o = np.zeros(len(ic), bool); hitS_u = np.zeros(len(ic), bool)
hitS4_o = np.zeros(len(ic), bool); hitS4_u = np.zeros(len(ic), bool)
npairs = 0
for i0 in range(0, len(ic), CH):
    s = slice(i0, min(i0 + CH, len(ic)))
    th4 = 4.0 * (1 + zl[s]) / chil[s]
    lists = treeB.query_ball_point(unitv(ra[ic[s]], dec[ic[s]]), r=2 * np.sin(th4 / 2))
    nper = np.array([len(x) for x in lists])
    lk = np.repeat(np.arange(len(nper)), nper)
    js = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=int(nper.sum()))
    gi = ic[s][lk]
    keep = js != gi
    lk, js, gi = lk[keep], js[keep], gi[keep]
    npairs += len(js)
    # projected physical separation at the lens distance
    v1 = unitv(ra[gi], dec[gi]); v2 = unitv(ra[js], dec[js])
    ang = 2 * np.arcsin(np.clip(np.linalg.norm(v1 - v2, axis=1) / 2, 0, 1))
    Rp = ang * chil[s][lk] / (1 + zl[s][lk])
    zL = zl[s][lk]; lmL = lml[s][lk]; clL = cls_ml[s][lk]
    gn = good[js]
    m_est = logU_at(zL, clL) + logF[js] + 2 * np.log10(DLz(zL))
    m_n = np.where(gn & np.isfinite(nb_logM_obs[js]), nb_logM_obs[js], m_est)
    q = np.where(np.isfinite(m_n), m_n > lmL - 1.0, False)
    dv = CKMS * np.abs(zsp[js] - zL) / (1 + zL)
    so = q & gn & (Rp < 3.0) & (dv < 1000); su = q & ~gn & (Rp < 3.0)
    s4o = q & gn & (Rp < 4.0) & (dv < 2000); s4u = q & ~gn & (Rp < 4.0)
    for arr, m in ((hitS_o, so), (hitS_u, su), (hitS4_o, s4o), (hitS4_u, s4u)):
        arr[i0 + np.unique(lk[m])] = True
    if (i0 // CH) % 10 == 0:
        say(f"  isolation: lenses {min(i0 + CH, len(ic)):,}/{len(ic):,}; pairs so far {npairs:,}")
isoS = ~(hitS_o | hitS_u); isoS4 = ~(hitS4_o | hitS4_u)
onlyU_S = hitS_u & ~hitS_o; onlyU_S4 = hitS4_u & ~hitS4_o

# ================================================================== 6. ISO-P: the committed KiDS photo-z rule on the same lenses
pool = (kr < 20) & (kz > 0.1) & (kz < 0.5) & (kmask == 0) & np.isfinite(klm) & (klm > 7)
ipl = np.where(pool)[0]
chiP_all = DC(kz[ipl])                                                     # lr_esd_remeasure: DC over the pool
treeP = cKDTree(unitv(kra[ipl], kdec[ipl]))
isoP = np.zeros(len(ic), bool)
im = np.where(mt)[0]
kz_l = kz[kidx[im]]
chi_l = chi_of(kz_l)                                                       # same cosmology, at the counterpart's photo-z
lists = treeP.query_ball_point(unitv(kra[kidx[im]], kdec[kidx[im]]), r=3.0 / chi_l)
inpool_pos = -np.ones(len(kb), np.int64); inpool_pos[ipl] = np.arange(len(ipl))
for t_, js in enumerate(lists):
    js = np.asarray(js, dtype=np.int64)
    self_ = inpool_pos[kidx[im[t_]]]
    js = js[js != self_]
    hit = np.any((klm[ipl][js] > klm[kidx[im[t_]]] - 1.0) & (np.abs(chiP_all[js] - chi_l[t_]) < 10))
    isoP[im[t_]] = not hit
P(f"  ISO-P computed for {len(im):,} matched candidates ({np.sum(pool[kidx[im]]):,} of them inside the KiDS lens pool)")

# ================================================================== 7. counts table
hb = mm & complete                                                         # headline base: matched, good mass, complete
for nm, f in (("ISO-S (3 Mpc, 1000 km/s) [headline]", isoS), ("ISO-S4 (4 Mpc, 2000 km/s) [strict]", isoS4),
              ("ISO-P (KiDS photo-z rule) [C1 contrast]", isoP)):
    cnt[f"+ {nm}"] = int(np.sum(hb & f))
P("  cut sequence (headline class (b) path):")
for k_, v in cnt.items():
    P(f"    {k_:72s} {v:>10,}")
samples = {"S": hb & isoS, "S4": hb & isoS4, "P": hb & isoP}
rows = {}
for nm, f in samples.items():
    e = f & (clsb == 1); l = f & (clsb == 0)
    b1 = (lml >= 10.0) & (lml < 10.5); b2 = (lml >= 10.5) & (lml < 11.0)
    rows[nm] = dict(N=int(f.sum()), early=int(e.sum()), late=int(l.sum()),
                    fe=float(e.sum() / max(f.sum(), 1)),
                    medM_e=float(np.median(lml[e])) if e.any() else None, medM_l=float(np.median(lml[l])) if l.any() else None,
                    bin1_e=int((e & b1).sum()), bin1_l=int((l & b1).sum()), bin2_e=int((e & b2).sum()), bin2_l=int((l & b2).sum()),
                    iso_frac=float(f.sum() / max(hb.sum(), 1)))
    r_ = rows[nm]
    P(f"  {nm:3s}: N {r_['N']:,} (early {r_['early']:,}, late {r_['late']:,}; early fraction {r_['fe']:.3f}); median log M* early "
      f"{r_['medM_e']} / late {r_['medM_l']}; M* bins 10.0-10.5 e/l {r_['bin1_e']:,}/{r_['bin1_l']:,}, 10.5-11.0 e/l "
      f"{r_['bin2_e']:,}/{r_['bin2_l']:,}; isolated fraction of the complete base {r_['iso_frac']:.3f}")
check("R1 (reported) counts per sample, early fraction, median log M* per class, isolated fraction", json.dumps(rows), True, load_bearing=False)
r2 = dict(onlyU_S=int(np.sum(hb & onlyU_S)), onlyU_S4=int(np.sum(hb & onlyU_S4)), base_complete=int(hb.sum()),
          completeness_loss=int(np.sum(mm & ~complete)), base_before_D5=int(mm.sum()),
          complete_with_early_ML=int(np.sum(mm & complete_e)),
          isoS_obs_only=int(np.sum(hb & ~hitS_o)), isoS4_obs_only=int(np.sum(hb & ~hitS4_o)))
check("R2 (reported) lenses excluded ONLY by unobserved neighbours; the completeness-cut loss",
      f"ISO-S: {r2['onlyU_S']:,} of {r2['base_complete']:,} complete lenses excluded only by unobserved targets "
      f"(isolated if unobserved targets were ignored: {r2['isoS_obs_only']:,}); ISO-S4: {r2['onlyU_S4']:,} (ignored: {r2['isoS4_obs_only']:,}); "
      f"D5 drops {r2['completeness_loss']:,} of {r2['base_before_D5']:,} (with the early-type M/L for every lens: {r2['complete_with_early_ML']:,} kept)",
      True, load_bearing=False)
nest = bool(np.all(isoS[isoS4]))
check("C3 CONTROL: ISO-S4 within ISO-S (nested definitions)", f"ISO-S4 {int(np.sum(hb & isoS4)):,} subset of ISO-S {int(np.sum(hb & isoS)):,}: {nest}", nest)
# variant without the AGN cut (reported)
hbv = mt & flag_ok[ic] & complete
rowsv = {nm: int(np.sum(hbv & f)) for nm, f in (("S", isoS), ("S4", isoS4), ("P", isoP))}
check("R-AGN (reported, variant) the same samples without the AGNFRAC < 0.1 cut",
      f"base {int(hbv.sum()):,}; ISO-S {rowsv['S']:,}; ISO-S4 {rowsv['S4']:,}; ISO-P {rowsv['P']:,}; AGNFRAC < 0.1 keeps "
      f"{100 * np.mean(mass_ok[ic][mt & flag_ok[ic]]):.1f}% of matched lenses (early {100 * np.mean(mass_ok[ic][mt & flag_ok[ic] & (clsb == 1)]):.1f}%, "
      f"late {100 * np.mean(mass_ok[ic][mt & flag_ok[ic] & (clsb == 0)]):.1f}%)", True, load_bearing=False)
# R3: CIGALE vs KiDS LePhare (+0.15) M* on matched lenses per class
dm = lml - klm[np.clip(kidx, 0, None)]
q3 = {cl: float(np.median(dm[mm & (clsb == cl)])) for cl in (0, 1)}
check("R3 (reported) CIGALE minus KiDS LePhare(+0.15) log M* on matched lenses, per class (Q = early - late; Mistele Q = 1.4 = +0.15 dex)",
      f"late {q3[0]:+.3f}, early {q3[1]:+.3f} dex; class-dependent offset {q3[1] - q3[0]:+.3f} dex", True, load_bearing=False)

# ================================================================== 8. patches (D7: N = 30) on the headline base sample
pb = assign_patches(ra[ic][hb], dec[ic][hb])
south_any = bool(np.any(dec[ic][hb] < -15))
qedges = np.quantile(ra[ic][hb], np.linspace(0, 1, NPATCH + 1)); qedges[0] -= 1e-6; qedges[-1] += 1e-6
patch_all = np.clip(np.searchsorted(qedges, ra[ic], side="right") - 1, 0, NPATCH - 1)
assert south_any is False and np.array_equal(patch_all[hb], pb)
cntp = np.bincount(pb, minlength=NPATCH)
P(f"  patches: {NPATCH} RA-quantile stripes on the headline base (all lenses in KiDS-N: {not south_any}); base lenses per patch "
  f"min/median/max {cntp.min()}/{int(np.median(cntp))}/{cntp.max()}")

# ================================================================== 9. analytic power for D
R.banner("9. Expected statistical power for D (analytic scaling of the June KiDS jackknife; no shear value of these lenses read)")
PM = PowerModel(zbh, zbe)
Mg_l = 10 ** lml * (1 + fcold(lml))
lamJ = PM.lamJ
P(f"  calibration of the scaling on the June sample itself (no cross-class term, Hartlap 41/49): lambda vs D_B = "
  f"{lamJ['canonical']:.1f} / {lamJ['alt']:.1f} (CFG95 re-measured chi2 26.68 / 24.79)")
POW = {}
for nm, f in samples.items():
    POW[nm] = PM.rows(Mg_l, zl, clsb, f, P, nm)
check("P1 (reported) expected power for D (scaling sigma^2 ∝ 1/sum M_gal n_src(>z+0.2) Sigma_crit^-2 / D_A^2 per class from CFG88's "
      "June per-class jackknife; Hartlap 21/29; a KiDS-size split assumed true)", json.dumps(POW)[:2000], True, load_bearing=False)

# ================================================================== write the lens table (outside git)
np.savez(os.path.join(WORK, "cfg316_lenses.npz"),
         tid=tid[ic], ra=ra[ic], dec=dec[ic], z=zl, chi=DC(zl), logM=lml, Mgal=Mg_l, rmag=rmag[ic], clsb=clsb, clsa=cls_a_all[ic],
         ur_c=ur_c[ic], kidx=kidx, klogM=np.where(kidx >= 0, klm[np.clip(kidx, 0, None)], np.nan),
         kur=np.where(kidx >= 0, kur[np.clip(kidx, 0, None)], np.nan), mass_ok=mass_ok[ic], matched=mt, complete=complete,
         complete_e=complete_e, isoS=isoS, isoS4=isoS4, isoP=isoP, onlyU_S=onlyU_S, onlyU_S4=onlyU_S4, hitS_o=hitS_o, hitS4_o=hitS4_o,
         patch=patch_all, qedges=qedges, t_a=t_a, fe_K=fe_K, zbh=zbh, zbe=zbe)
fpk_pix = np.where(fpK)[0]
np.save(os.path.join(WORK, "cfg316_kids_footprint_pix.npy"), fpk_pix)
cov_pix = np.where(cov256)[0]
np.save(os.path.join(WORK, "cfg316_bgs_cov256_pix.npy"), cov_pix)
P(f"\n  wrote ../_external_data/cfg316_work/cfg316_lenses.npz ({len(ic):,} stack candidates) and the footprint pixel lists")
R.num("counts", cnt); R.num("R1", rows); R.num("R2", r2); R.num("R3", q3); R.num("power", POW); R.num("power_calibration_june", lamJ)
R.num("area", dict(kids=areaK, overlap=area_ov)); R.num("class_a", dict(t_a=t_a, fe_K=fe_K, agree=agree)); R.num("variant_noAGN", rowsv)
R.num("patches", dict(n=NPATCH, per_patch=cntp.tolist()))
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
