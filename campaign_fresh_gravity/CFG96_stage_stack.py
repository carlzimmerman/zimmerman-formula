#!/usr/bin/env python3
"""CFG96 stage: isolation flags at |dchi| < 10 / 20 / 30 Mpc and ONE stacking pass over the June lenses, sums kept per window.

Criteria frozen and committed before this stage ran: campaign_fresh_gravity/CFG96_FROZEN_CRITERIA.md (cb2876df0).
  isolation  the logic of real_research/reviews/lensing_rar/lr_esd_remeasure.py stage_lens (v4, +0.15 dex fluxscale), vectorised: a lens
             is isolated at window W if no pool galaxy with log M* > log M*_lens - 1 lies within 3 Mpc transverse (angular radius
             3/chi_lens on the unit sphere) with |dchi| < W.  The W = 10 set must reproduce lr_lenses.npz exactly (C1).
  stack      the estimator of real_research/reviews/lensing_rar/agentK_jackknife_stack.py stage_stack, verbatim per lens, in the same lens
             order, with the June patch labels (assign_patches on the base sample); sums accumulated for the base sample (W = 10, must
             reproduce lr_esd_jackknife.npz exactly, C2) and for the W = 20 and W = 30 subsets.
  outputs    real_research/data/lensing_rar/cfg96_isoflags.npz and cfg96_stack.npz (git-ignored; big data stay out of git).
Run: python3 -u campaign_fresh_gravity/CFG96_stage_stack.py   (about 15-40 min; prints progress)
"""
import os, sys, time
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
D = os.path.join(REPO, "real_research", "data", "lensing_rar")
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc
NPATCH = 50
WINDOWS = (10, 20, 30)
T0 = time.time()


def say(s):
    print(f"[{time.time() - T0:7.1f} s] {s}", flush=True)


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


# ================================================================== 1. isolation flags (stage_lens logic, vectorised)
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
say(f"lens selection {len(il):,}; neighbour pool {len(ip):,}")
PI_l, DCH_l = [], []
CH = 20000
for i0 in range(0, len(il), CH):
    slc = pos[i0:i0 + CH]
    lists = tree.query_ball_point(xyzP[slc], r=3.0 / chiP[slc])
    lens_k = np.repeat(np.arange(len(slc)), [len(x) for x in lists])
    js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(sum(len(x) for x in lists)))
    ii = slc[lens_k]
    keep = (js != ii) & (logMP[js] > logMP[ii] - 1.0)
    PI_l.append((i0 + lens_k)[keep]); DCH_l.append(np.abs(chiP[ii[keep]] - chiP[js[keep]]))
PI = np.concatenate(PI_l); dchi = np.concatenate(DCH_l)
say(f"candidate satellite pairs (proj < 3 Mpc, mass-qualified): {len(PI):,}")
iso = {}
for W in WINDOWS:
    f = np.ones(len(il), bool); f[np.unique(PI[dchi < W])] = False
    iso[W] = f
    say(f"  |dchi| < {W:3d} Mpc: isolated {f.sum():,} ({100 * f.mean():.1f}%)")
base = iso[10]
zS = zP[pos]; logMS = logMP[pos]; chiL = chiP[pos]; urS = ur[il]
typ = np.where(urS > 2.0, 1, 0)
fcold = 10 ** (-0.69 * logMS + 6.63); Mgal = 10 ** logMS * (1 + fcold)
ln = np.load(os.path.join(D, 'lr_lenses.npz'))
c1 = (int(base.sum()) == len(ln['ra'])) and all(
    np.array_equal(a, ln[k]) for a, k in ((ra[il][base], 'ra'), (dec[il][base], 'dec'), (zS[base], 'z'),
                                           (Mgal[base], 'Mgal'), (typ[base], 'typ'), (chiL[base], 'chi')))
say(f"C1: W = 10 isolated set reproduces lr_lenses.npz exactly: {c1} ({int(base.sum()):,} vs {len(ln['ra']):,})")
f20, f30 = iso[20][base], iso[30][base]
np.savez(os.path.join(D, 'cfg96_isoflags.npz'), f20=f20, f30=f30, c1=c1, n=np.array([int(base.sum()), int(f20.sum()), int(f30.sum())]))
if not c1:
    sys.exit("C1 failed: the isolation recomputation does not reproduce lr_lenses.npz; stopping before the stack")

# ================================================================== 2. one stacking pass (agentK estimator, verbatim per lens)
patch = assign_patches(np.array(ln['ra'], dtype='f8'), np.array(ln['dec'], dtype='f8'))
J = np.load(os.path.join(D, 'lr_esd_jackknife.npz'))
say(f"patch labels equal the June ones: {np.array_equal(patch, J['patch'])}")
F = os.path.join(D, 'KiDS_DR4.1_SOM_gold_WL_cat.fits')
h = fits.open(F, memmap=True); s = h[1].data
cols = {cc.name.upper(): cc.name for cc in h[1].columns}


def col(*names):
    for n in names:
        if n.upper() in cols: return np.array(s[cols[n.upper()]], dtype='f8')
    raise KeyError(names)


raS = col('RAJ2000', 'ALPHA_J2000', 'RA'); decS = col('DECJ2000', 'DELTA_J2000', 'DEC')
e1 = col('e1', 'BIAS_CORRECTED_E1'); e2 = col('e2', 'BIAS_CORRECTED_E2')
w = col('weight', 'RECAL_WEIGHT', 'LFWEIGHT'); zB = col('Z_B', 'ZB', 'Z_B_BPZ')
say(f"sources: {len(raS):,}")
zl = ln['z']; chil = ln['chi']
treeS = cKDTree(np.c_[np.radians(raS), np.radians(decS)])
say("source tree built")
gbar_edges = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)
SUMS = {W: dict(wgE=np.zeros((NPATCH, 2, 15)), W=np.zeros((NPATCH, 2, 15)), NN=np.zeros((NPATCH, 2, 15))) for W in WINDOWS}
FL = {10: np.ones(len(zl), bool), 20: f20, 30: f30}
chunk = 2000
for i0 in range(0, len(zl), chunk):
    sl = slice(i0, min(i0 + chunk, len(zl)))
    for j, (rl, dl, zl_, chil_, Mg, ty, pa) in enumerate(zip(ln['ra'][sl], ln['dec'][sl], zl[sl], chil[sl],
                                                          ln['Mgal'][sl], ln['typ'][sl], patch[sl])):
        ty = int(ty); pa = int(pa); gi = i0 + j
        theta_max = 3.0 * (1 + zl_) / chil_
        ii = treeS.query_ball_point([np.radians(rl), np.radians(dl)], theta_max)
        ii = np.array(ii, dtype=int)
        if ii.size < 5: continue
        back = zB[ii] > zl_ + 0.2
        ii = ii[back]
        if ii.size < 5: continue
        dra = (np.radians(raS[ii]) - np.radians(rl)) * np.cos(np.radians(dl)); dde = np.radians(decS[ii]) - np.radians(dl)
        R = np.hypot(dra, dde) * chil_ / (1 + zl_)
        phi = np.arctan2(dde, dra)
        et = -(e1[ii] * np.cos(2 * phi) - e2[ii] * np.sin(2 * phi))
        chis = DC(zB[ii]); Dls = (chis - chil_) / (1 + zB[ii]); Dl = chil_ / (1 + zl_); Ds = chis / (1 + zB[ii])
        inv_sc = np.clip(4 * np.pi * G / (c ** 2) * (Dl * Mpc) * (Dls / Ds), 0, None)
        gbar = G * Mg * Msun / (R * Mpc) ** 2
        k = np.digitize(gbar, gbar_edges) - 1
        ok = (k >= 0) & (k < 15) & (inv_sc > 0)
        ww = w[ii] * inv_sc ** 2
        vg = (ww * et / np.where(inv_sc > 0, inv_sc, 1))[ok]; vw = ww[ok]; kk = k[ok]
        for Wd in WINDOWS:
            if not FL[Wd][gi]: continue
            S = SUMS[Wd]
            np.add.at(S['wgE'][pa, ty], kk, vg); np.add.at(S['W'][pa, ty], kk, vw); np.add.at(S['NN'][pa, ty], kk, 1)
    if (i0 // chunk) % 10 == 0 or i0 + chunk >= len(zl):
        say(f"  lenses {min(i0 + chunk, len(zl)):,}/{len(zl):,}")
dev = max(float(np.max(np.abs(SUMS[10][k] - J[k]) / np.maximum(np.abs(J[k]), 1e-300))) for k in ('wgE', 'W', 'NN'))
say(f"C2: the W = 10 re-stack reproduces the June sums: max relative deviation {dev:.1e}")
np.savez(os.path.join(D, 'cfg96_stack.npz'), **{f"{k}_{W}": SUMS[W][k] for W in WINDOWS for k in ('wgE', 'W', 'NN')},
         patch=patch, gbar_edges=gbar_edges, c2dev=dev)
say("wrote cfg96_stack.npz")
