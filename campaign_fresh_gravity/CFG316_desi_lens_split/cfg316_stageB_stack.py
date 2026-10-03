#!/usr/bin/env python3
"""CFG316 Stage B, stacking pass (the real shear is read here, once): per-lens estimator sums for
  (1) C2: the committed June lenses (lr_lenses.npz, 181,477) with the June patch labels -> per-(patch, class, bin) sums vs
      lr_esd_jackknife.npz (must agree to 1e-9 relative);
  (2) the frozen CFG316 lens set: the complete, matched lenses with FLAG_MASSPDF in [1/5, 5] (a superset of the headline base, which adds
      the AGNFRAC < 0.1 cut; it contains every frozen sample: ISO-S, ISO-S4 [both empty, Stage A], ISO-P [C1]);
  (3) C4: 20,000 random points uniform in the KiDS x BGS footprint pixels, each given the (z, M_gal) of a random lens of set (2).
The estimator is agentK_jackknife_stack.py's, per lens (cfg316_common.Stacker.lens); the cross shear is accumulated alongside for C4.
Outputs (outside git): ../_external_data/cfg316_work/cfg316_stack.npz.
Run from the repository root: python3 -u campaign_fresh_gravity/CFG316_desi_lens_split/cfg316_stageB_stack.py
"""
import os, sys
import numpy as np
import healpy as hp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg316_common import *   # noqa

L = np.load(os.path.join(WORK, "cfg316_lenses.npz"))
S = read_shear_columns(["RAJ2000", "DECJ2000", "e1", "e2", "weight", "Z_B"])
S = {k: v.astype("f8") for k, v in S.items()}
say(f"sources {len(S['e1']):,}")
st = Stacker(S["RAJ2000"], S["DECJ2000"], S["e1"], S["e2"], S["weight"], S["Z_B"])
say("source tree built")

# (1) C2: the June lenses
ln = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
PLj = stack_perlens(st, ln["ra"], ln["dec"], ln["z"], ln["chi"], ln["Mgal"], label="June")
Sj = np.zeros((3, 50, 2, 15))
for q in range(3):
    np.add.at(Sj[q], (J["patch"], ln["typ"].astype(int)), PLj[:, q, :])
dev = max(float(np.max(np.abs(Sj[q] - J[k]) / np.maximum(np.abs(J[k]), 1e-300))) for q, k in enumerate(("wgE", "W", "NN")))
say(f"C2: June per-patch sums reproduced, max relative deviation {dev:.1e}")

# (2) the frozen CFG316 lens set
sel = L["matched"] & L["complete"]
idx = np.where(sel)[0]                                     # every Stage A candidate already passed FLAG_MASSPDF in [1/5, 5]
PL = stack_perlens(st, L["ra"][idx], L["dec"][idx], L["z"][idx], L["chi"][idx], L["Mgal"][idx], label="CFG316")

# (3) C4 randoms
rng = np.random.default_rng(3160)
fpk = np.load(os.path.join(WORK, "cfg316_kids_footprint_pix.npy"))
cov = np.zeros(hp.nside2npix(256), bool); cov[np.load(os.path.join(WORK, "cfg316_bgs_cov256_pix.npy"))] = True
th, ph = hp.pix2ang(1024, fpk)
ovl = fpk[cov[hp.ang2pix(256, th, ph)]]
NR = 20000
pix = rng.choice(ovl, NR)
# uniform within each nside-1024 pixel: jitter by sub-pixel sampling at nside 8192
pn = hp.ring2nest(1024, pix)
subn = pn * 64 + rng.integers(0, 64, NR)
rra, rdec = hp.pix2ang(8192, subn, nest=True, lonlat=True)
pick = rng.choice(idx, NR)
rz = L["z"][pick]; rchi = DC(rz); rMg = L["Mgal"][pick]
PLr = stack_perlens(st, rra, rdec, rz, rchi, rMg, label="randoms")
qed = L["qedges"]
rpatch = np.clip(np.searchsorted(qed, rra, side="right") - 1, 0, NPATCH - 1)
np.savez(os.path.join(WORK, "cfg316_stack.npz"), idx=idx, PL=PL, c2dev=dev, Sj=Sj,
         rra=rra, rdec=rdec, rz=rz, rMg=rMg, rpatch=rpatch, PLr=PLr)
say("wrote ../_external_data/cfg316_work/cfg316_stack.npz")
