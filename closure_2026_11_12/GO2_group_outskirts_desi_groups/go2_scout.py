"""GO2 pre-freeze scout (disclosed in FROZEN_CRITERIA.md): counts only. DESI DR1 bgs-groups centrals in the KiDS-1000 N box x ACT strip,
KiDS source coverage, and how many survive candidate isolation cuts. No shear, no y, no stacked or graded number.
python3 -I go2_scout.py <bgs-groups fits> <kids column dir>. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
FITS, COLS = sys.argv[1], sys.argv[2]
zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54/0.70
def DM(z): return pch(np.minimum(np.asarray(z, float), 2.33))*RD
d = fits.open(FITS, memmap=True)[1].data
ra, de, z, M, sat = (np.asarray(d[c]) for c in ("RA", "DEC", "Z", "M_HALO", "IS_SAT"))
c = ~sat; ra, de, z, M = ra[c], de[c], z[c], M[c]; lm = np.log10(M)
def xyz(r, d_): r, d_ = np.radians(r), np.radians(d_); return np.c_[np.cos(d_)*np.cos(r), np.cos(d_)*np.sin(r), np.sin(d_)]
# DESI footprint proxy: 0.25 deg cells holding any DESI galaxy (all galaxies, satellites included)
ga, gd = np.asarray(d["RA"]), np.asarray(d["DEC"]); occ = set(zip((ga*4).astype(int), (np.floor(gd*4)).astype(int)))
# KiDS coverage proxy: 0.25 deg cells with sources
ks_ra = np.load(os.path.join(COLS, "kids_ra.npy")); ks_de = np.load(os.path.join(COLS, "kids_dec.npy"))
kocc = set(zip((ks_ra[::20]*4).astype(int), np.floor(ks_de[::20]*4).astype(int)))
tree = cKDTree(xyz(ra, de))
box = (ra >= 125) & (ra <= 240) & (de >= -6) & (de <= 3.5)
def frac_cov(r0, d0, th_deg, cells):
    g = np.mgrid[-1:1.0001:0.1, -1:1.0001:0.1].reshape(2, -1); g = g[:, (g**2).sum(0) <= 1]
    rr = r0 + g[0]*th_deg/math.cos(math.radians(d0)); dd = d0 + g[1]*th_deg
    return np.mean([((int(a*4), int(math.floor(b*4))) in cells) for a, b in zip(rr, dd)])
for (zlo, zhi), (mlo, mhi) in [((0.05, 0.30), (13.3, 14.3)), ((0.05, 0.30), (13.5, 14.5)), ((0.05, 0.20), (13.3, 14.3))]:
    s = np.where(box & (z >= zlo) & (z <= zhi) & (lm >= mlo) & (lm < mhi))[0]
    res = {}
    for Rp, dv, fr in [(10.0, 2000.0, 0.5), (10.0, 3000.0, 0.5), (10.0, 2000.0, 1.0), (5.0, 2000.0, 0.5)]:
        nk = ni = nf = 0
        for i in s:
            Dl = float(DM(z[i]))/(1 + z[i]); th = Rp/Dl
            if frac_cov(ra[i], de[i], math.degrees(1.5*14.0*0.66/Dl) if False else math.degrees(16*0.66/Dl), kocc) < 0.5: continue
            nk += 1
            if frac_cov(ra[i], de[i], math.degrees(th), occ) < 0.9: continue
            nf += 1
            jj = np.array(tree.query_ball_point(xyz(ra[i:i+1], de[i:i+1])[0], 2*math.sin(th/2)), int); jj = jj[jj != i]
            dvv = np.abs(z[jj] - z[i])/(1 + z[i])*2.998e5
            if not np.any((dvv <= dv) & (M[jj] >= fr*M[i])): ni += 1
        res[(Rp, dv, fr)] = (nk, nf, ni)
    print(f"z {zlo}-{zhi}, log M_HALO {mlo}-{mhi}: centrals in box {len(s)}; (R_proj Mpc, dv km/s, M_nb/M) -> (KiDS-covered, DESI-complete disc, isolated): {res}", flush=True)
