#!/usr/bin/env python3
"""CFG903 stage A (criteria FROZEN_CRITERIA.md, bb665cf4f; completeness per AMENDMENT_A1.md, 26ecb00ce): isolation rebuild (I0 I1 I2 I5), lens table, neighbour pool,
random clones (mask-emulated), B21-like lens weights, completeness factors, jackknife patches.  No lensing statistic here.
Output (git-ignored, large): ../../../_external_data/cfg903_work/cfg903_stage.npz ; log cfg903_stage.out ; cfg903_stage_results.json
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg903_stage.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import glob, json, math, time
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg903_lib as L

L.start_watchdog("CFG903 stage")
os.makedirs(L.WORK, exist_ok=True)
OUT = []
def P(s=""):
    s = f"[{time.time() - L.T0:7.1f} s, {L.cur_rss() / 1e6:5.0f} MB] {s}"; print(s, flush=True); OUT.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
RES = dict(lane="CFG903", stage="A")

# ================================================================ bright sample (CFG502 verbatim column handling)
HB = fits.open(os.path.join(L.DATA, 'KiDS_DR4_brightsample.fits'), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(L.DATA, 'KiDS_DR4_brightsample_LePhare.fits'), memmap=True); Lp = HL[1].data
assert np.array_equal(np.asarray(b['ID']), np.asarray(Lp['ID']))
r = np.array(b['MAG_AUTO_CALIB'], dtype='f8'); z = np.array(b['zphot_ANNz2'], dtype='f8'); masked = np.array(b['masked']).astype(np.int64)
logM = np.array(Lp['MASS_MED'], dtype='f8') + 0.15
ur = np.array(Lp['MAG_ABS_u'] - Lp['MAG_ABS_r'], dtype='f8')
ra = np.array(b['RAJ2000'], dtype='f8'); dec = np.array(b['DECJ2000'], dtype='f8')
NALL = len(ra)
del b, Lp; HB.close(); HL.close(); import gc; gc.collect()
P(f"bright sample {NALL:,} objects; masked = 1: {int((masked == 1).sum()):,}")

pool = (r < 20) & (z > 0.1) & (z < 0.5) & (masked == 0) & np.isfinite(logM) & (logM > 7)
sel = pool & (logM < 11.0) & np.isfinite(ur)
ip = np.where(pool)[0]; il = np.where(sel)[0]
zP = z[ip]; logMP = logM[ip]; chiP = L.DC(zP)
xyzP = L.unitvec(ra[ip], dec[ip])
pos = np.searchsorted(ip, il)
NA = len(il)
check("K0c candidates = CFG502's 605,531", NA == 605531, f"{NA:,} (pool {len(ip):,})")

# ================================================================ isolation: min |dchi| of more-massive (> 0.1 M*) pool neighbours
treeP = cKDTree(xyzP)
dmin_c = np.full(NA, np.inf); dmin_p = np.full(NA, np.inf)
CH = 500; npairs = 0
for i0 in range(0, NA, CH):
    slc = pos[i0:i0 + CH]
    rq = 3.0 * (1 + zP[slc]) / chiP[slc]                     # physical 3 Mpc (>= comoving 3 Mpc) as a chord radius
    lists = treeP.query_ball_point(xyzP[slc], r=rq)
    cnt = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists))
    k = np.repeat(np.arange(len(slc)), cnt)
    js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(cnt.sum()))
    ii = slc[k]
    keep = (js != ii) & (logMP[js] > logMP[ii] - 1.0)
    k, js, ii = k[keep], js[keep], ii[keep]
    ch = np.linalg.norm(xyzP[js] - xyzP[ii], axis=1)
    dc = np.abs(chiP[ii] - chiP[js])
    mc = ch <= 3.0 / chiP[ii]                               # CFG502: query_ball_point(r = 3/chi) is a <= test
    np.minimum.at(dmin_c, i0 + k[mc], dc[mc])
    np.minimum.at(dmin_p, i0 + k, dc)                        # all pairs here have chord <= 3(1+z)/chi
    npairs += len(k)
P(f"isolation pairs (more massive, within physical 3 Mpc): {npairs:,}")
del treeP, lists, k, js, ii, keep, ch, dc, mc, cnt
I0 = dmin_c >= 10; I1 = dmin_c >= 30; I2 = dmin_p >= 10
WGRID = np.round(np.arange(1.0, 30.0001, 0.1), 1)
cnts = np.array([int((dmin_c >= w).sum()) for w in WGRID])
W_B = float(WGRID[np.argmin(np.abs(cnts - 259383))]); I5 = dmin_c >= W_B
P(f"counts (all candidates, log M* < 11): I0 {I0.sum():,}  I1 {I1.sum():,}  I2 {I2.sum():,}  I5 (W_B = {W_B} Mpc) {I5.sum():,}  [B21: 259,383]")

# K0a / K0b: I0 reproduces lr_lenses; I1 on I0 = cfg96 f30
zS = zP[pos]; logMS = logMP[pos]; chiL = chiP[pos]; raS, decS = ra[il], dec[il]; urS = ur[il]
typ = np.where(urS > 2.0, 1, 0)
Mgal = 10 ** logMS * (1 + L.fcold(logMS))
ln = np.load(os.path.join(L.DATA, 'lr_lenses.npz'))
k0a = (int(I0.sum()) == len(ln['ra'])) and all(np.array_equal(a, ln[kk]) for a, kk in (
    (raS[I0], 'ra'), (decS[I0], 'dec'), (zS[I0], 'z'), (Mgal[I0], 'Mgal'), (typ[I0], 'typ'), (chiL[I0], 'chi'), (logMS[I0], 'logM')))
check("K0a I0 reproduces lr_lenses.npz exactly", k0a, f"{int(I0.sum()):,} vs {len(ln['ra']):,}")
f30 = np.load(os.path.join(L.DATA, 'cfg96_isoflags.npz'))['f30']
k0b = np.array_equal(I1[I0], f30)
check("K0b I1 on I0 equals cfg96 f30", k0b, f"{int(I1[I0].sum()):,} vs {int(f30.sum()):,}")

# ================================================================ lens table: B21 bins, union of samples (I1, I2 subset of I0)
BIN_EDGES = [8.5, 10.3, 10.6, 10.8, 11.0]
binS = np.digitize(logMS, BIN_EDGES) - 1                   # 0..3 inside, -1 below 8.5, 4 never (logM < 11)
U = (I0 | I5) & (binS >= 0) & (binS <= 3)
assert not np.any((I1 | I2) & ~I0)
iu = np.where(U)[0]
NL = len(iu)
lens = dict(ra=raS[iu], dec=decS[iu], z=zS[iu], chi=chiL[iu], logM=logMS[iu], Mgal=Mgal[iu], bin=binS[iu],
            I0=I0[iu], I1=I1[iu], I2=I2[iu], I5=I5[iu])
P(f"lens table (union I0 u I5, B21 bins): {NL:,}; per bin I0 " + " / ".join(str(int(((lens['bin'] == q) & lens['I0']).sum())) for q in range(4))
  + "; I5 " + " / ".join(str(int(((lens['bin'] == q) & lens['I5']).sum())) for q in range(4)))

# ================================================================ neighbour pool (criteria: r < 20, 0.02 <= z <= 0.8, finite log M* > 7; masked either)
nb = (r < 20) & (z >= 0.02) & (z <= 0.8) & np.isfinite(logM) & (logM > 7)
inb = np.where(nb)[0]
NB = dict(xyz=L.unitvec(ra[inb], dec[inb]), chi=L.DC(z[inb]), logMb=np.log10(10 ** logM[inb] * (1 + L.fcold(logM[inb]))),
          logMs=logM[inb], z=z[inb], masked=masked[inb].astype(np.int8))
# lens -> neighbour-pool index (self exclusion): the lens is bright-sample object ip[pos[iu]]
lens_obj = ip[pos[iu]]
self_nb = np.searchsorted(inb, lens_obj)
assert np.all(inb[self_nb] == lens_obj)
lens["self_nb"] = self_nb
P(f"neighbour pool {len(inb):,} (masked = 1: {int((NB['masked'] == 1).sum()):,}); lens self-index matched")
# K0d: the lens's own M_b in the pool equals its Mgal
k0d = np.allclose(10 ** NB["logMb"][self_nb], lens["Mgal"], rtol=1e-12)
check("K0d neighbour-pool M_b of each lens = its Mgal", k0d, "rtol 1e-12")

# ================================================================ randoms: uniform in the two field boxes, mask by nearest object
P('building all-object tree for the random mask'); xyzA = L.unitvec(ra, dec); treeA = cKDTree(xyzA); P('all-object tree built')
rng = np.random.default_rng(903)
south = dec < -15.0
boxes = []
for m in (~south, south):
    rau = np.where(dec[m] < -15.0, (ra[m] + 180.0) % 360.0, ra[m])
    lo, hi = float(rau.min()), float(rau.max()); dlo, dhi = float(dec[m].min()), float(dec[m].max())
    area = np.radians(hi - lo) * (math.sin(math.radians(dhi)) - math.sin(math.radians(dlo)))
    boxes.append((lo, hi, dlo, dhi, area))
pbox = np.array([bx[4] for bx in boxes]); pbox /= pbox.sum()
TH = math.radians(4.0 / 60.0); CHR = 2 * math.sin(TH / 2)
acc_ra, acc_dec = [], []; ntry = 0; nacc = 0
while nacc < NL:
    n = 100000; ntry += n
    fb = rng.random(n) < pbox[1]
    rr = np.empty(n); dd = np.empty(n)
    for q, bx in enumerate(boxes):
        mm = fb if q == 1 else ~fb
        lo, hi, dlo, dhi = bx[:4]
        rau = lo + (hi - lo) * rng.random(mm.sum())
        sd = math.sin(math.radians(dlo)) + (math.sin(math.radians(dhi)) - math.sin(math.radians(dlo))) * rng.random(mm.sum())
        rr[mm] = (rau - 180.0) % 360.0 if q == 1 else rau
        dd[mm] = np.degrees(np.arcsin(sd))
    dist, nn = treeA.query(L.unitvec(rr, dd), k=1)
    ok = (dist < CHR) & (masked[nn] == 0)
    acc_ra.append(rr[ok]); acc_dec.append(dd[ok]); nacc += int(ok.sum())
rra = np.concatenate(acc_ra)[:NL]; rdec = np.concatenate(acc_dec)[:NL]
P(f"randoms: {NL:,} accepted of {ntry:,} drawn (acceptance {nacc / ntry:.3f}); clone k <-> lens k")
del treeA, xyzA

# ================================================================ jackknife patches (agentK scheme on the I0 lenses)
pe = L.patch_edges(raS[I0], decS[I0])
lens["patch"] = L.apply_patches(lens["ra"], lens["dec"], pe)
rnd_patch = L.apply_patches(rra, rdec, pe)
P(f"patches: lenses per patch (I0) min {np.bincount(lens['patch'][lens['I0']], minlength=50).min()}, randoms per patch min {np.bincount(rnd_patch, minlength=50).min()}")

# ================================================================ B21-like per-lens weights (CFG885's S1 source model, fiducial Om 0.2793)
fn = glob.glob(os.path.join(L.EXT, "cfg592_work", "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]
with fits.open(fn) as F:
    nzt = F["NZ_SOURCE"].data; hdr = F["NZ_SOURCE"].header
    ZLO, ZHI = np.array(nzt["Z_LOW"], float), np.array(nzt["Z_HIGH"], float); NZ = [np.array(nzt[f"BIN{i+1}"], float) for i in range(5)]
    NGAL = np.array([float(hdr[f"NGAL_{i+1}"]) for i in range(5)])
ZB_EDGES = [(0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.2)]
ZG = np.linspace(0.0, 6.0, 30001)
def chi_fn(om):                                                    # CFG885 verbatim (no radiation)
    f = 1.0 / np.sqrt(om * (1 + ZG) ** 3 + (1.0 - om))
    cc = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(ZG))]); return lambda zz: np.interp(zz, ZG, cc)
def sinv(chi, zl, zs):                                             # CFG885 verbatim, proportional to Sigma_crit^-1
    cl, cs = chi(zl), chi(zs); return np.where(zs > zl, cl * (cs - cl) / np.maximum(cs, 1e-30) / (1 + zl), 0.0)
SRC = []
for bq, (lo, hi) in enumerate(ZB_EDGES):                           # CFG885 src_S1 verbatim
    sub = (np.arange(10) + 0.5) / 10
    zs = (ZLO[:, None] + (ZHI - ZLO)[:, None] * sub[None, :]).ravel(); w = np.repeat(NZ[bq] / NZ[bq].sum() / 10, 10)
    frac = lambda zl, lo=lo, hi=hi: float(np.clip((hi - max(lo, zl + 0.2)) / (hi - lo), 0.0, 1.0))
    SRC.append((zs, w * NGAL[bq], frac))
cf = chi_fn(0.2793)
ZLG = np.linspace(0.05, 0.6, 221); S2 = np.zeros(len(ZLG))
for i, zl in enumerate(ZLG):
    for zs, w, frac in SRC:
        a = sinv(cf, zl, zs); S2[i] += np.sum(w * frac(zl) * a * a)
WZ = S2 / (cf(ZLG) / (1 + ZLG)) ** 2
WB = np.interp(lens["z"], ZLG, WZ); WB /= WB[lens["I0"]].mean()
lens["W_B21"] = WB
P(f"B21-like weights: W(z) at z 0.15/0.25/0.35/0.45 = " + " / ".join(f"{np.interp(q, ZLG, WZ) / np.interp(0.25, ZLG, WZ):.3f}" for q in (0.15, 0.25, 0.35, 0.45)) + " (relative to z 0.25)")

# ================================================================ completeness (AMENDMENT A1: complete-slab mass function; C1' faint-end up-weighting, C2' whole-sum)
unm = NB["masked"] == 0
Z0 = np.round(np.arange(0.05, 0.6001, 0.01), 2)
mlim = np.array([np.percentile(NB["logMs"][unm & (np.abs(NB["z"] - z0) < 0.01)], 5) for z0 in Z0])   # frozen m_lim definition
Nv = np.vectorize(L.N_of_declared)
ZS = Z0[(Z0 >= 0.10 - 1e-9) & (Z0 <= 0.50 + 1e-9)]; MS = np.interp(ZS, Z0, mlim)
ME = np.round(np.arange(8.5, 12.0001, 0.1), 1)                    # 0.1-dex log M* bins 8.5-12.0
sl = unm & (NB["z"] >= 0.10) & (NB["z"] < 0.50) & (NB["logMs"] >= 8.5) & (NB["logMs"] < 12.0)
lsS, lbS, zS_ = NB["logMs"][sl], NB["logMb"][sl], NB["z"][sl]
MtS = 10 ** lbS * (1 + L.SUP * Nv(lbS))
chi10 = float(L.DC(np.array([0.10, 0.50]))[0])
zc_lit, zc_run, rho = [], [], []
for lo in ME[:-1]:
    ok = MS <= lo + 1e-9
    zc_l = float(ZS[ok].max()) if ok.any() else 0.0                  # amendment's literal: largest z with m_lim(z) <= m
    run = 0
    while run < len(ZS) and MS[run] <= lo + 1e-9: run += 1
    zc_r = float(ZS[run - 1]) if run > 0 else 0.0                   # contiguous from 0.10 (reported)
    zc_lit.append(zc_l); zc_run.append(zc_r)
    if zc_l < 0.12:
        rho.append(np.nan); continue
    m = (lsS >= lo) & (lsS < lo + 0.1) & (zS_ >= 0.10) & (zS_ < zc_l)
    chic = float(L.DC(np.array([zc_l, 0.50]))[0])
    rho.append(float(MtS[m].sum()) / (chic ** 3 - chi10 ** 3))
rho = np.array(rho); keep = np.isfinite(rho)
kf = int(np.argmax(keep)); assert keep[kf:].all(), "kept bins must be contiguous above m_f"
m_f = float(ME[kf])
CUM = np.concatenate([[0.0], np.cumsum(np.where(keep, rho, 0.0) * 0.1)])   # cumulative over ME edges (per dex * 0.1 dex)
def Ccum(m):
    return np.interp(m, ME, CUM)                                     # piecewise-linear inside bins; flat above 12.0
CT = float(CUM[-1])
def f_C1(ml):
    ml = np.asarray(ml, float)
    num = Ccum(ml) - Ccum(m_f); den = Ccum(ml + 0.5) - Ccum(ml)
    return np.where(ml > m_f, num / np.maximum(den, 1e-300), 0.0)
def R_C2(ml):
    ml = np.asarray(ml, float)
    return (CT - Ccum(m_f)) / (CT - Ccum(np.maximum(ml, m_f)))
lens["mlim"] = np.interp(lens["z"], Z0, mlim)
lens["fC1"] = f_C1(lens["mlim"]); lens["RcC2"] = R_C2(lens["mlim"])
check("K0e completeness factors finite for every lens (A1 definitions)", bool(np.all(np.isfinite(lens["fC1"])) and np.all(np.isfinite(lens["RcC2"]))),
      f"f_C1' range {lens['fC1'].min():.3f}-{lens['fC1'].max():.3f}, R_C2' range {lens['RcC2'].min():.3f}-{lens['RcC2'].max():.3f}")
P(f"completeness: m_lim(z) 0.10/0.20/0.30/0.40/0.50 = " + " / ".join(f"{np.interp(q, Z0, mlim):.2f}" for q in (0.1, 0.2, 0.3, 0.4, 0.5))
  + f"; m_lim monotone on 0.10-0.50: {bool(np.all(np.diff(MS) >= 0))}; z_c literal = contiguous: {zc_lit == zc_run}")
P(f"  slab mass function: m_f = {m_f:.1f}; z_c(m) at 8.7/9.0/9.5/10.0/10.5 = " + " / ".join(f"{zc_lit[int(round((q - 8.5) / 0.1))]:.2f}" for q in (8.7, 9.0, 9.5, 10.0, 10.5)))
P(f"  share of rho_tot above log M* 9.5/10.0/10.5/11.0: " + " / ".join(f"{(CT - Ccum(q)) / (CT - Ccum(m_f)):.3f}" for q in (9.5, 10.0, 10.5, 11.0)))
P(f"  f_C1'(z) at z 0.2/0.3/0.4/0.5 = " + " / ".join(f"{float(f_C1(np.interp(q, Z0, mlim))):.3f}" for q in (0.2, 0.3, 0.4, 0.5))
  + "; R_C2'(z) = " + " / ".join(f"{float(R_C2(np.interp(q, Z0, mlim))):.3f}" for q in (0.2, 0.3, 0.4, 0.5)))
for q in range(4):
    m = (lens["bin"] == q) & lens["I0"]
    P(f"  bin {q + 1} (I0): median z {np.median(lens['z'][m]):.3f}, weighted mean m_lim {np.average(lens['mlim'][m], weights=WB[m]):.2f}, f_C1' {np.average(lens['fC1'][m], weights=WB[m]):.3f}, R_C2' {np.average(lens['RcC2'][m], weights=WB[m]):.3f}")

# ================================================================ save
np.savez(os.path.join(L.WORK, "cfg903_stage.npz"),
         **{f"L_{k}": v for k, v in lens.items()}, R_ra=rra, R_dec=rdec, R_patch=rnd_patch,
         NB_xyz=NB["xyz"], NB_chi=NB["chi"], NB_logMb=NB["logMb"], NB_logMs=NB["logMs"], NB_masked=NB["masked"])
RES.update(checks=CHK, n_candidates=int(NA), counts_all=dict(I0=int(I0.sum()), I1=int(I1.sum()), I2=int(I2.sum()), I5=int(I5.sum()), W_B=W_B, B21=259383),
           counts_bins={s: [int(((lens['bin'] == q) & lens[s]).sum()) for q in range(4)] for s in ("I0", "I1", "I2", "I5")},
           n_lens_table=int(NL), n_neighbour_pool=int(len(inb)), random_acceptance=nacc / ntry,
           completeness=dict(Z0=Z0.tolist(), mlim=mlim.tolist(), ME=ME.tolist(), rho_tot=[None if not np.isfinite(x) else float(x) for x in rho], z_c=zc_lit, z_c_contiguous=zc_run, m_f=m_f,
                             f_C1=[float(f_C1(x)) for x in mlim], R_C2=[float(R_C2(x)) for x in mlim]),
           weights=dict(ZLG=ZLG.tolist(), WZ=(WZ / np.interp(0.25, ZLG, WZ)).tolist()),
           runtime_s=round(time.time() - L.T0, 1), peak_current_rss_MB=round(L.PEAK_CUR[0] / 1e6, 1), ru_maxrss_MB=round(L.rss() / 1e6, 1))
json.dump(RES, open(os.path.join(L.HERE, "cfg903_stage_results.json"), "w"), indent=1, default=float)
P(f"done; peak current RSS {L.PEAK_CUR[0] / 1e6:.0f} MB (ru_maxrss incl. file pages {L.rss() / 1e6:.0f} MB); all stage checks {'PASS' if all(CHK.values()) else 'FAIL'}")
open(os.path.join(L.HERE, "cfg903_stage.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
