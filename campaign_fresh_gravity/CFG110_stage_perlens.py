#!/usr/bin/env python3
"""CFG110 stage: ONE pass of the June KiDS stacking estimator over the 181,477 June lenses, keeping each lens's per-bin sums.

Criteria frozen and committed before this stage ran: campaign_fresh_gravity/CFG110_FROZEN_CRITERIA.md (f870b217a).
  estimator  real_research/reviews/lensing_rar/agentK_jackknife_stack.py stage_stack, verbatim per lens (same sources, background cut,
             Sigma_crit weights, g_bar bins), in the June lens order.  Instead of accumulating per (patch, class, bin), each lens's
             contributions are kept per bin: wgE_l[lens, bin], W_l[lens, bin], NN_l[lens, bin].  Any subset, patch sum, jackknife replicate
             or random halving is then an array sum.  C1 (in the scoring script): summing these by (patch, class) reproduces the June sums.
  output     real_research/data/lensing_rar/cfg110_perlens.npz (git-ignored).
Run: python3 -u campaign_fresh_gravity/CFG110_stage_perlens.py   (about 2 min)
"""
import os, time
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
D = os.path.join(REPO, "real_research", "data", "lensing_rar")
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc
T0 = time.time()


def say(s):
    print(f"[{time.time() - T0:7.1f} s] {s}", flush=True)


def DC(z, n=2048):                     # agentK verbatim
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c / H0) / Mpc
    return np.interp(z, zz, chi)


ln = np.load(os.path.join(D, 'lr_lenses.npz'))
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
WG = np.zeros((NL, 15)); WW = np.zeros((NL, 15)); NNL = np.zeros((NL, 15))
with np.errstate(divide="ignore"):
    for gi, (rl, dl, zl_, chil_, Mg) in enumerate(zip(ln['ra'], ln['dec'], zl, chil, ln['Mgal'])):
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
        np.add.at(WG[gi], kk, vg); np.add.at(WW[gi], kk, vw); np.add.at(NNL[gi], kk, 1)
        if gi % 20000 == 0:
            say(f"  lenses {gi:,}/{NL:,}")
say(f"  lenses {NL:,}/{NL:,}")
np.savez(os.path.join(D, 'cfg110_perlens.npz'), WG=WG, WW=WW, NN=NNL, gbar_edges=gbar_edges)
say("wrote cfg110_perlens.npz")
