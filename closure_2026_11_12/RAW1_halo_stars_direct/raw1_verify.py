#!/usr/bin/env python3
"""
RAW1 independent SI check of the key numbers (separate code path from raw1.py).
Usage: python3 -I -B raw1_verify.py <MWS_BHB.fits>     Writes raw1_verify.out.
1. Line-of-sight dispersion in 20-30 kpc by the moment estimator sqrt(var(v) - <e^2>), own frame transform
   (astropy Galactocentric with velocities, not the affine matrix of raw1.py).
2. Predicted sigma_r at 25 kpc for the framework census line (canonical) with scipy.integrate.quad in SI,
   and the bin's mean projection factor, so f can be rebuilt by hand.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, math, json, warnings
warnings.simplefilter("ignore")
import numpy as np
from scipy.integrate import quad
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianDifferential
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import raw1_model as MOD
out = open(os.path.join(HERE, "raw1_verify.out"), "w")
def say(s): print(s); out.write(s + "\n")
R = json.load(open(os.path.join(HERE, "raw1_results.json")))
h = fits.open(sys.argv[1]); rv, fm = h["RVTAB"].data, h["FIBERMAP"].data
m = rv["PRIMARY"].astype(bool) & np.isfinite(rv["VRAD"]) & (rv["VRAD_ERR"] > 0) & (fm["DIST"] > 0)
gc = Galactocentric(galcen_distance=8.122 * u.kpc, z_sun=20.8 * u.pc, galcen_v_sun=CartesianDifferential([12.9, 245.6, 7.78] * u.km / u.s))
c = SkyCoord(ra=rv["TARGET_RA"][m] * u.deg, dec=rv["TARGET_DEC"][m] * u.deg, distance=fm["DIST"][m] * u.kpc,
             pm_ra_cosdec=np.zeros(m.sum()) * u.mas / u.yr, pm_dec=np.zeros(m.sum()) * u.mas / u.yr,
             radial_velocity=rv["VRAD"][m] * u.km / u.s, frame="icrs")
g = c.transform_to(gc)
x = np.vstack([g.x.to_value(u.kpc), g.y.to_value(u.kpc), g.z.to_value(u.kpc)]).T
v = np.vstack([g.v_x.to_value(u.km / u.s), g.v_y.to_value(u.km / u.s), g.v_z.to_value(u.km / u.s)]).T
sun = gc.galcen_distance  # line of sight from the Sun's Galactocentric position
cs = SkyCoord(ra=0 * u.deg, dec=0 * u.deg, distance=1e-9 * u.kpc, frame="icrs").transform_to(gc)
xs = np.array([cs.x.to_value(u.kpc), cs.y.to_value(u.kpc), cs.z.to_value(u.kpc)])
n = x - xs; n /= np.linalg.norm(n, axis=1)[:, None]
vgsr = np.sum(v * n, axis=1)   # with zero proper motion, v.n is the GSR line-of-sight velocity
r = np.linalg.norm(x, axis=1)
gal = c.galactic; l, b = np.radians(gal.l.deg), np.radians(gal.b.deg)
from astropy.coordinates.matrix_utilities import rotation_matrix
M = np.diag([1., 1., -1.]) @ rotation_matrix((180 + 14.111534) * u.deg, "z") @ rotation_matrix((90 - 13.46) * u.deg, "x") @ rotation_matrix((180 + 3.75) * u.deg, "z")
Bsgr = np.degrees(np.arcsin((M @ np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)]))[2]))
e = rv["VRAD_ERR"][m]
sel = (np.abs(Bsgr) >= 15) & (r >= 20) & (r < 30) & (np.abs(vgsr) <= 400)
sig_mom = math.sqrt(np.var(vgsr[sel]) - np.mean(e[sel] ** 2))
d0 = R["nominal"]["disp"][0]
say(f"1. bin 20-30: N {sel.sum()} (raw1: {d0['n']}); moment sigma_los {sig_mom:.2f} km/s; raw1 ML {d0['sigma']:.2f} [{d0['lo']:.2f}, {d0['hi']:.2f}]")
rh = x / r[:, None]; sin2 = 1 - np.sum(n * rh, axis=1) ** 2
alpha, beta = R["nominal"]["alpha"]["alpha"], R["nominal"]["beta"]
G, KPC = 6.674e-11, 3.0857e19
def gfw(s_kpc, a0=9.36e-11):
    Mb = MOD.M_sph(round(float(s_kpc), 1)) if s_kpc <= 200 else MOD.M_sph(200.0)
    gb = G * Mb / (s_kpc * KPC) ** 2; y = gb / a0
    return gb / (1 - math.exp(-math.sqrt(y)))
def sr2(rk):
    I = quad(lambda s: s ** (2 * beta - alpha) * gfw(s) * KPC, rk, 200, limit=200)[0] + quad(lambda s: s ** (2 * beta - alpha) * gfw(s) * KPC, 200, 2e4, limit=200)[0]
    return I / rk ** (2 * beta - alpha) / 1e6
rr = r[sel]; s2 = sin2[sel]
pred = [math.sqrt(sr2(q) * (1 - beta * w)) for q, w in zip(rr[::20], s2[::20])]
f_hand = sig_mom / math.sqrt(np.mean(np.square(pred)))
f0 = R["nominal"]["f"]["FW_census/canonical"][0]["f"]
say(f"2. FW census canonical, alpha {alpha:.3f}, beta {beta:.3f}: sigma_r(25 kpc) = {math.sqrt(sr2(25.0)):.2f} km/s (quad, SI);"
    f" rms predicted sigma_los over every 20th star of the bin {math.sqrt(np.mean(np.square(pred))):.2f}; hand f = {f_hand:.3f} vs raw1 ML f {f0:.3f}")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
out.close()
