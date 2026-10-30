#!/usr/bin/env python3
"""GH7 lens selection (catalogues only): DESI DR1 BGS + CIGALE, MW-mass centrals over the whole ACT range. No map, no velocity."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data")
W = os.path.join(EXT, "gh7_work"); os.makedirs(W, exist_ok=True)
h = fits.open(os.path.join(EXT, "desi_dr1_bgs", "BGS_BRIGHT_full_HPmapcut.dat.fits"), memmap=True)[1].data
ra, de, z, zw, dc = [np.array(h[k]) for k in ("RA", "DEC", "Z_not4clus", "ZWARN", "DELTACHI2")]; tid = np.array(h["TARGETID"])
g = (zw == 0) & (dc > 40) & (z > 0.005) & (z < 0.6); ra, de, z, tid = ra[g], de[g], z[g], tid[g]
c = fits.open(os.path.join(EXT, "desi_dr1_cigale", "IronPhysProp_v1.2.fits"), memmap=True)[1].data
ct, cm, cf = np.array(c["TARGETID"]), np.array(c["LOGM"]), np.array(c["LOGSFR"])
k = (np.char.strip(np.array(c["SURVEY"]).astype(str)) == "main") & (np.char.strip(np.array(c["PROGRAM"]).astype(str)) == "bright"); ct, cm, cf = ct[k], cm[k], cf[k]
s = np.argsort(ct); i = np.searchsorted(ct[s], tid); i[i >= len(s)] = 0; ok = ct[s][i] == tid
lm, sf = np.full(len(z), np.nan), np.full(len(z), np.nan); lm[ok] = cm[s][i[ok]]; sf[ok] = cf[s][i[ok]]
m = np.isfinite(lm); ra, de, z, lm, sf = ra[m], de[m], z[m], lm[m], sf[m]
U = np.c_[np.cos(np.radians(de)) * np.cos(np.radians(ra)), np.cos(np.radians(de)) * np.sin(np.radians(ra)), np.sin(np.radians(de))]; T = cKDTree(U)
zz = np.linspace(0, 1, 4001); E = np.sqrt(.3085 * (1 + zz) ** 3 + .6915); ch = np.r_[0, np.cumsum(.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))] * 299792.458 / 67.9
DA = np.interp(z, zz, ch) / (1 + z)
L = np.where((lm >= 10.6) & (lm <= 11) & (z >= .1) & (z <= .5))[0]; cen = np.ones(len(L), bool)
for c0 in range(0, len(L), 5000):
    J = L[c0:c0 + 5000]; nb = T.query_ball_point(U[J], 2 * np.sin(1.0 / DA[J] / 2))
    for j, lst in enumerate(nb):
        q = np.asarray(lst); i0 = J[j]; q = q[q != i0]; q = q[np.abs(z[q] - z[i0]) / (1 + z[i0]) * 299792.458 < 2000]
        cen[c0 + j] = not np.any(lm[q] > lm[i0])
np.savez(os.path.join(W, "gh7_lenses.npz"), ra=ra[L][cen], dec=de[L][cen], z=z[L][cen], lm=lm[L][cen], sfr=sf[L][cen])
print("mass-selected", len(L), "central", int(cen.sum()), f"fraction {cen.mean():.3f}")
