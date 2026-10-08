#!/usr/bin/env python3
"""CFG502 stage (FROZEN_CRITERIA.md, cacadd50d): photometry and lensing staging; no model is evaluated here.

  1. isolation rebuild (CFG96_stage_stack.py logic, verbatim) for every lens candidate (ALL); W = 10 must reproduce lr_lenses.npz (C5).
  2. photo-z leakage: Delta chi_phot histograms of close pairs (R_p < 0.3 Mpc comoving, companion log M* > log M*_lens - 1) and of the
     4-6 Mpc annulus (same cuts), per lens-z bin, for a seeded random 100k subsample of ALL.
  3. companion counts around every ISO lens: pool galaxies MORE massive than the lens within R_p < 0.5 Mpc and in the 4-6 Mpc annulus,
     10 < |Delta chi| < 600 Mpc; plus the annulus count with |Delta chi| < 50 Mpc (for n_3D).
  4. pool completeness: 5th percentile of pool log M* in |z - z0| < 0.01, z0 = 0.10..0.50 step 0.01.
  5. the ALL lensing stack: CFG110's per-lens estimator verbatim for every lens candidate (per-lens WG, WW, NN); C6: the ISO lenses
     reproduce cfg110_perlens.npz.
Outputs (git-ignored, large): ../../../_external_data/cfg502_work/cfg502_stage.npz.  Log: cfg502_stage.out.
Run: nice -n 15 python3 -u cfg502_stage.py   (single thread; about 15-30 min)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import time, json
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D = os.path.join(REPO, "real_research", "data", "lensing_rar")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
os.makedirs(WORK, exist_ok=True)
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc
NPATCH = 50
T0 = time.time()
LOG = []


def say(s):
    s = f"[{time.time() - T0:7.1f} s] {s}"; print(s, flush=True); LOG.append(s)


def DC(z, n=2048):                     # lr_esd_remeasure.py / agentK verbatim
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c / H0) / Mpc
    return np.interp(z, zz, chi)


def assign_patches(ra, dec, npatch=NPATCH):   # agentK verbatim
    south = dec < -15.0
    ra_u = np.where(south, (ra + 180.0) % 360.0, ra)
    patch = np.zeros(len(ra), dtype=np.int64); off = 0
    for m in (~south, south):
        npr = npatch // 2
        q = np.quantile(ra_u[m], np.linspace(0, 1, npr + 1)); q[0] -= 1e-6; q[-1] += 1e-6
        patch[m] = off + np.clip(np.searchsorted(q, ra_u[m], side='right') - 1, 0, npr - 1)
        off += npr
    return patch


CHK = {}


def check(name, ok, msg):
    CHK[name] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


# ============================================================ 1. isolation rebuild (CFG96 verbatim logic)
b = fits.open(os.path.join(D, 'KiDS_DR4_brightsample.fits'))[1].data
L = fits.open(os.path.join(D, 'KiDS_DR4_brightsample_LePhare.fits'))[1].data
assert np.array_equal(b['ID'], L['ID'])
r = b['MAG_AUTO_CALIB']; z = np.array(b['zphot_ANNz2'], dtype='f8'); masked = b['masked']
logM = np.array(L['MASS_MED'], dtype='f8') + 0.15
ur = np.array(L['MAG_ABS_u'] - L['MAG_ABS_r'], dtype='f8')
ra = np.array(b['RAJ2000'], dtype='f8'); dec = np.array(b['DECJ2000'], dtype='f8')
pool = (r < 20) & (z > 0.1) & (z < 0.5) & (masked == 0) & np.isfinite(logM) & (logM > 7)
sel = pool & (logM < 11.0) & np.isfinite(ur)
ip = np.where(pool)[0]; il = np.where(sel)[0]
zP = z[ip]; logMP = logM[ip]; chiP = DC(zP)
raP, decP = np.radians(ra[ip]), np.radians(dec[ip])
xyzP = np.c_[np.cos(decP) * np.cos(raP), np.cos(decP) * np.sin(raP), np.sin(decP)]
tree = cKDTree(xyzP)
pos = np.searchsorted(ip, il)
NA = len(il)
say(f"lens candidates (ALL) {NA:,}; neighbour pool {len(ip):,}")
PI_l, DCH_l = [], []
CH = 20000
for i0 in range(0, NA, CH):
    slc = pos[i0:i0 + CH]
    lists = tree.query_ball_point(xyzP[slc], r=3.0 / chiP[slc])
    lens_k = np.repeat(np.arange(len(slc)), [len(x) for x in lists])
    js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(sum(len(x) for x in lists)))
    ii = slc[lens_k]
    keep = (js != ii) & (logMP[js] > logMP[ii] - 1.0)
    PI_l.append((i0 + lens_k)[keep]); DCH_l.append(np.abs(chiP[ii[keep]] - chiP[js[keep]]))
PI = np.concatenate(PI_l); dchi = np.concatenate(DCH_l)
iso = {}
for W in (10, 20, 30):
    f = np.ones(NA, bool); f[np.unique(PI[dchi < W])] = False
    iso[W] = f
    say(f"  |dchi| < {W:3d} Mpc: isolated {f.sum():,} ({100 * f.mean():.1f}%)")
del PI, dchi, PI_l, DCH_l
zS = zP[pos]; logMS = logMP[pos]; chiL = chiP[pos]; urS = ur[il]; raS_, decS_ = ra[il], dec[il]
typ = np.where(urS > 2.0, 1, 0)
fcold = 10 ** (-0.69 * logMS + 6.63); Mgal = 10 ** logMS * (1 + fcold)
ln = np.load(os.path.join(D, 'lr_lenses.npz'))
base = iso[10]
c5 = (int(base.sum()) == len(ln['ra'])) and all(
    np.array_equal(a, ln[k]) for a, k in ((raS_[base], 'ra'), (decS_[base], 'dec'), (zS[base], 'z'),
                                           (Mgal[base], 'Mgal'), (typ[base], 'typ'), (chiL[base], 'chi'), (logMS[base], 'logM')))
check("C5 isolation rebuild reproduces lr_lenses.npz exactly", c5, f"{int(base.sum()):,} vs {len(ln['ra']):,}")
f30_ok = np.array_equal(iso[30][base], np.load(os.path.join(D, 'cfg96_isoflags.npz'))['f30'])
check("C5b W = 30 flags reproduce cfg96_isoflags f30", f30_ok, "exact")

# ============================================================ 4. pool completeness
Z0 = np.round(np.arange(0.10, 0.5001, 0.01), 2)
mlim = np.array([np.percentile(logMP[np.abs(zP - z0) < 0.01], 5) for z0 in Z0])
say("pool completeness log M*_lim(z) (5th pct): " + " ".join(f"{z0:.2f}:{m:.2f}" for z0, m in zip(Z0[::5], mlim[::5])))

# ============================================================ 2 + 3. pair statistics
ZB = np.round(np.arange(0.10, 0.5001, 0.05), 2)                # lens-z bins (8)
DE = np.arange(-600.0, 600.0 + 1e-9, 5.0)                      # Delta chi edges (240 bins)
NZB = len(ZB) - 1
H_in = np.zeros((NZB, len(DE) - 1)); H_an = np.zeros((NZB, len(DE) - 1)); NLZ = np.zeros(NZB)
rng = np.random.default_rng(502)
SUB = np.sort(rng.choice(NA, 100000, replace=False))
iso_idx = np.where(base)[0]
cin = np.zeros(len(iso_idx)); can = np.zeros(len(iso_idx)); can50 = np.zeros(len(iso_idx))


def pairs(idx):
    """for lens-candidate indices idx: (lens k, pool j, R_com [Mpc], dchi [Mpc]) for pool galaxies within 6 Mpc comoving."""
    slc = pos[idx]
    lists = tree.query_ball_point(xyzP[slc], r=6.0 / chiP[slc])
    lens_k = np.repeat(np.arange(len(slc)), [len(x) for x in lists])
    js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(sum(len(x) for x in lists)))
    ii = slc[lens_k]
    keep = js != ii
    lens_k, js, ii = lens_k[keep], js[keep], ii[keep]
    d = np.linalg.norm(xyzP[js] - xyzP[ii], axis=1)
    Rc = 2 * np.arcsin(np.minimum(d / 2, 1.0)) * chiP[ii]
    return lens_k, js, ii, Rc, chiP[js] - chiP[ii]


t = time.time()
for i0 in range(0, len(SUB), 5000):
    idx = SUB[i0:i0 + 5000]
    k, js, ii, Rc, dc = pairs(idx)
    q = logMP[js] > logMP[ii] - 1.0
    zb = np.clip(np.digitize(zP[ii], ZB) - 1, 0, NZB - 1)
    m_in = q & (Rc < 0.3); m_an = q & (Rc >= 4.0) & (Rc < 6.0)
    for zz in range(NZB):
        H_in[zz] += np.histogram(dc[m_in & (zb == zz)], DE)[0]
        H_an[zz] += np.histogram(dc[m_an & (zb == zz)], DE)[0]
    np.add.at(NLZ, np.clip(np.digitize(zP[pos[idx]], ZB) - 1, 0, NZB - 1), 1)
say(f"close-pair histograms done ({time.time() - t:.0f} s); inner pairs {H_in.sum():.0f}, annulus pairs {H_an.sum():.0f}")
t = time.time()
for i0 in range(0, len(iso_idx), 5000):
    idx = iso_idx[i0:i0 + 5000]
    k, js, ii, Rc, dc = pairs(idx)
    mm = logMP[js] > logMP[ii]
    adc = np.abs(dc)
    out = mm & (adc > 10) & (adc < 600)
    cin[i0:i0 + len(idx)] = np.bincount(k[out & (Rc < 0.5)], minlength=len(idx))
    can[i0:i0 + len(idx)] = np.bincount(k[out & (Rc >= 4.0) & (Rc < 6.0)], minlength=len(idx))
    can50[i0:i0 + len(idx)] = np.bincount(k[mm & (adc < 50) & (Rc >= 4.0) & (Rc < 6.0)], minlength=len(idx))
say(f"companion counts done ({time.time() - t:.0f} s): mean inner {cin.mean():.4f}, annulus x area ratio {can.mean() * 0.25 / 20:.4f}")

# ============================================================ 5. ALL lensing stack (CFG110 per-lens estimator verbatim)
patch_all = assign_patches(raS_, decS_)
F = os.path.join(D, 'KiDS_DR4.1_SOM_gold_WL_cat.fits')
h = fits.open(F, memmap=True); s = h[1].data
cols = {cc.name.upper(): cc.name for cc in h[1].columns}


def col(*names):
    for n in names:
        if n.upper() in cols: return np.array(s[cols[n.upper()]], dtype='f8')
    raise KeyError(names)


raW = col('RAJ2000', 'ALPHA_J2000', 'RA'); decW = col('DECJ2000', 'DELTA_J2000', 'DEC')
e1 = col('e1', 'BIAS_CORRECTED_E1'); e2 = col('e2', 'BIAS_CORRECTED_E2')
w = col('weight', 'RECAL_WEIGHT', 'LFWEIGHT'); zBs = col('Z_B', 'ZB', 'Z_B_BPZ')
say(f"sources: {len(raW):,}")
treeS = cKDTree(np.c_[np.radians(raW), np.radians(decW)])
say("source tree built")
gbar_edges = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)
WG = np.zeros((NA, 15)); WWa = np.zeros((NA, 15)); NNL = np.zeros((NA, 15))
with np.errstate(divide="ignore"):
    for gi, (rl, dl, zl_, chil_, Mg) in enumerate(zip(raS_, decS_, zS, chiL, Mgal)):
        theta_max = 3.0 * (1 + zl_) / chil_
        ii = treeS.query_ball_point([np.radians(rl), np.radians(dl)], theta_max)
        ii = np.array(ii, dtype=int)
        if ii.size < 5: continue
        back = zBs[ii] > zl_ + 0.2
        ii = ii[back]
        if ii.size < 5: continue
        dra = (np.radians(raW[ii]) - np.radians(rl)) * np.cos(np.radians(dl)); dde = np.radians(decW[ii]) - np.radians(dl)
        R = np.hypot(dra, dde) * chil_ / (1 + zl_)
        phi = np.arctan2(dde, dra)
        et = -(e1[ii] * np.cos(2 * phi) - e2[ii] * np.sin(2 * phi))
        chis = DC(zBs[ii]); Dls = (chis - chil_) / (1 + zBs[ii]); Dl = chil_ / (1 + zl_); Ds = chis / (1 + zBs[ii])
        inv_sc = np.clip(4 * np.pi * G / (c ** 2) * (Dl * Mpc) * (Dls / Ds), 0, None)
        gbar = G * Mg * Msun / (R * Mpc) ** 2
        k = np.digitize(gbar, gbar_edges) - 1
        ok = (k >= 0) & (k < 15) & (inv_sc > 0)
        ww = w[ii] * inv_sc ** 2
        vg = (ww * et / np.where(inv_sc > 0, inv_sc, 1))[ok]; vw = ww[ok]; kk = k[ok]
        np.add.at(WG[gi], kk, vg); np.add.at(WWa[gi], kk, vw); np.add.at(NNL[gi], kk, 1)
        if gi % 50000 == 0:
            say(f"  lenses {gi:,}/{NA:,}")
pl = np.load(os.path.join(D, 'cfg110_perlens.npz'))
dev = max(float(np.max(np.abs(a[base] - pl[k_]) / np.maximum(np.abs(pl[k_]), 1e-300))) for a, k_ in ((WG, 'WG'), (WWa, 'WW')))
check("C6 ALL stack: the ISO lenses reproduce cfg110_perlens WG / WW", dev <= 1e-9, f"max relative deviation {dev:.1e}")

np.savez(os.path.join(WORK, 'cfg502_stage.npz'), ra=raS_, dec=decS_, z=zS, logM=logMS, Mgal=Mgal, typ=typ, chi=chiL,
         iso10=iso[10], iso20=iso[20], iso30=iso[30], WG=WG, WW=WWa, NN=NNL, patch_all=patch_all, gbar_edges=gbar_edges,
         ZB=ZB, DE=DE, H_in=H_in, H_an=H_an, NLZ=NLZ, sub=SUB, iso_idx=iso_idx, cin=cin, can=can, can50=can50, Z0=Z0, mlim=mlim)
say(f"wrote {os.path.join('_external_data', 'cfg502_work', 'cfg502_stage.npz')}")
json.dump(dict(checks=CHK, n_all=int(NA), n_iso10=int(iso[10].sum()), n_iso30=int(iso[30].sum())),
          open(os.path.join(HERE, 'cfg502_stage_results.json'), 'w'), indent=1)
open(os.path.join(HERE, 'cfg502_stage.out'), 'w').write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
