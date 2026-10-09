#!/usr/bin/env python3
"""CFG505 stage: ONE pass of the June KiDS stacking estimator (CFG110_stage_perlens.py, verbatim per lens: same sources, background cut,
Sigma_crit weights, lensfit weights, the 15 g_bar bins) over the 181,477 stack-P lenses, binning each lens's pairs in
g_bar = G M_gal / R^2 for EVERY mass set of cfg505_masses.py at once (the source pairs, et, weights are computed once per lens; only the
g_bar bin assignment differs between sets).

Mass sets are read from ../../../_external_data/cfg505_work/cfg505_masses.npz (key 'Mgal_<set>'); per set it writes
cfg505_perlens_<set>.npz with WG, WW, NN (181,477 x 15) to the same data dir (not in git).
Control (in cfg505_score.py): the set 'M0' (catalogue LePhare, = lr_lenses Mgal) must reproduce cfg110_perlens.npz exactly.
Run: nice -n 15 python3 cfg505_stage.py   (about 5-8 min, one process)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import time
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D = os.path.join(REPO, "real_research", "data", "lensing_rar")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg505_work"))
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc
T0 = time.time()


def say(s):
    print(f"[{time.time() - T0:7.1f} s] {s}", flush=True)


def DC(z, n=2048):                     # agentK / CFG110 verbatim
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c / H0) / Mpc
    return np.interp(z, zz, chi)


ln = np.load(os.path.join(D, 'lr_lenses.npz'))
MS = np.load(os.path.join(WORK, "cfg505_masses.npz"))
SETS = [k[5:] for k in MS.files if k.startswith("Mgal_")]
MG = {s: MS["Mgal_" + s].astype(float) for s in SETS}
assert np.array_equal(MG["M0"], ln["Mgal"]), "set M0 must be the catalogue Mgal"
say(f"mass sets: {SETS}")
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
NL = len(zl)
OUT = {st: (np.zeros((NL, 15)), np.zeros((NL, 15)), np.zeros((NL, 15))) for st in SETS}
with np.errstate(divide="ignore"):
    for gi, (rl, dl, zl_, chil_) in enumerate(zip(ln['ra'], ln['dec'], zl, chil)):
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
        ww = w[ii] * inv_sc ** 2
        vg_all = ww * et / np.where(inv_sc > 0, inv_sc, 1)
        R2 = (R * Mpc) ** 2
        for st in SETS:
            gbar = G * MG[st][gi] * Msun / R2
            k = np.digitize(gbar, gbar_edges) - 1
            ok = (k >= 0) & (k < 15) & (inv_sc > 0)
            WG, WW, NNL = OUT[st]
            kk = k[ok]
            np.add.at(WG[gi], kk, vg_all[ok]); np.add.at(WW[gi], kk, ww[ok]); np.add.at(NNL[gi], kk, 1)
        if gi % 20000 == 0:
            say(f"  lenses {gi:,}/{NL:,}")
say(f"  lenses {NL:,}/{NL:,}")
for st in SETS:
    WG, WW, NNL = OUT[st]
    np.savez(os.path.join(WORK, f'cfg505_perlens_{st}.npz'), WG=WG, WW=WW, NN=NNL, gbar_edges=gbar_edges)
say(f"wrote cfg505_perlens_<set>.npz for {SETS}")
