#!/usr/bin/env python3
"""FN4a stage 0: read the LITTLE THINGS IC 1613 cube plane by plane (raw reads, header-only metadata), crop 30' x 30' about
Oh+15's centre, bin 4x4, measure the noise, build the 3D mask and the chi2 grid (AMENDMENTS A5), the gas map (A7) and the
V-band stellar profile (A1). Then S0a (HI mass) and S0b (Oh+15's V(R_max), A2). Writes cache/prep.npz, fn4a_s0.json/.out.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4a_prep.py [--cube R]   (R: the robust cube, for the resolution check)
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy import ndimage
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
import fn4a_core as C

ROB = "--cube" in sys.argv and sys.argv[sys.argv.index("--cube") + 1] == "R"
TAG = "_R" if ROB else ""
OUT = []; R = {}; T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return f"[{time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]"

P(f"FN4a stage 0{' (robust cube)' if ROB else ''}. kappa = 1/2 FITTED; not theory closed.")
cf = os.path.join(C.DATA, "IC1613_R_ICL001.FITS" if ROB else "IC1613_NA_ICL001.FITS")
with fits.open(cf, memmap=True, lazy_load_hdus=True) as h:
    hdr = h[0].header.copy(); off = h.fileinfo(0)["datLoc"]
n1, n2, n3 = hdr["NAXIS1"], hdr["NAXIS2"], hdr["NAXIS3"]; assert hdr["BITPIX"] == -32 and hdr.get("BSCALE", 1) == 1 and hdr.get("BZERO", 0) == 0
w = WCS(hdr).celestial
xc, yc = w.world_to_pixel(SkyCoord(C.OH15["ra"] * u.deg, C.OH15["dec"] * u.deg, frame="fk5"))
xc, yc = float(xc), float(yc); H = 600
x_lo = int(round(xc)) - H; y_lo = int(round(yc)) - H; NB = 2 * H // C.BIN
assert 0 <= x_lo and x_lo + 2 * H <= n1 and 0 <= y_lo and y_lo + 2 * H <= n2
cdel1, cdel2 = hdr["CDELT1"] * 3600, hdr["CDELT2"] * 3600
v = (hdr["CRVAL3"] + (np.arange(n3) + 1 - hdr["CRPIX3"]) * hdr["CDELT3"]) / 1000.0
jb = np.arange(NB) * C.BIN + 1.5
XE = ((x_lo + jb[None, :]) - xc) * cdel1 * np.ones((NB, 1)); YN = ((y_lo + jb[:, None]) - yc) * cdel2 * np.ones((1, NB))
P(f"cube {os.path.basename(cf)}: {n1} x {n2} x {n3}, pixel {abs(cdel1):.2f}\", channel {hdr['CDELT3'] / 1000:+.3f} km/s; Oh+15 centre at pixel ({xc:.1f}, {yc:.1f}); crop 1200 px, bin 4 -> {NB} x {NB} of 6\"")
def rbin(a): return a.reshape(NB, C.BIN, NB, C.BIN).mean(axis=(1, 3))
cube = np.zeros((n3, NB, NB), np.float32); nanfrac = []
with open(cf, "rb") as f:
    for k in range(n3):
        f.seek(off + k * n1 * n2 * 4); pl = np.frombuffer(f.read(n1 * n2 * 4), dtype=">f4").reshape(n2, n1)
        cr = np.array(pl[y_lo:y_lo + 2 * H, x_lo:x_lo + 2 * H], dtype=np.float64); nanfrac.append(float(np.isnan(cr).mean())); cr[~np.isfinite(cr)] = 0.0
        cube[k] = rbin(cr)
P(f"cube read and binned {rss()}; NaN fraction in crop, median over channels {np.median(nanfrac):.3f}")
ends = np.r_[0:15, n3 - 15:n3]
def rstd(x): x = x[np.isfinite(x)]; return float(1.4826 * np.median(np.abs(x - np.median(x))))
noise = rstd(cube[ends].ravel())
sm = ndimage.gaussian_filter(cube, (0, 1.70, 1.70)); sm = ndimage.uniform_filter1d(sm, 3, axis=0); ns = rstd(sm[ends].ravel())
m0 = sm > 3 * ns
lab, nl = ndimage.label(m0); sizes = np.bincount(lab.ravel()); sizes[0] = 0; keep = sizes >= 0.01 * sizes.max(); m0 = keep[lab]
st = np.zeros((5, 5, 5), bool); yy, xx = np.mgrid[-2:3, -2:3]; disk = (yy * yy + xx * xx) <= 4
for dk in range(5): st[dk] = disk
mask = ndimage.binary_dilation(m0, structure=st)
ks = np.nonzero(mask.any(axis=(1, 2)))[0]; kmin, kmax = int(ks.min()), int(ks.max())
P(f"noise per binned voxel {noise * 1e3:.3f} mJy/beam; smoothed {ns * 1e3:.3f}; mask {int(mask.sum()):,} voxels in channels {kmin}-{kmax} (v {v[kmax]:.1f} to {v[kmin]:.1f} km/s)")
cube = cube[kmin:kmax + 1]; mask = mask[kmin:kmax + 1]; vv = v[kmin:kmax + 1]
gy, gx = np.mgrid[0:NB, 0:NB]; g2 = (gy % 2 == 0) & (gx % 2 == 0); grid = g2[None] & ((np.arange(len(vv)) % 2 == 0)[:, None, None])
Sobs = (cube * mask).sum(0)
# moment maps (binned), gas map
def readmap(name):
    with fits.open(os.path.join(C.DATA, name), memmap=True, lazy_load_hdus=True) as hh:
        o = hh.fileinfo(0)["datLoc"]; hd = hh[0].header
    with open(os.path.join(C.DATA, name), "rb") as ff:
        ff.seek(o); a = np.frombuffer(ff.read(hd["NAXIS1"] * hd["NAXIS2"] * 4), dtype=">f4").reshape(hd["NAXIS2"], hd["NAXIS1"]).astype(np.float64)
    return a
mom0f = readmap("IC1613_NA_X0_P_R.FITS") / 1000.0; mom1f = readmap("IC1613_NA_XMOM1.FITS") / 1000.0; mom2f = readmap("IC1613_NA_XMOM2.FITS") / 1000.0
def cropbin(a, nan_to=np.nan):
    c = a[y_lo:y_lo + 2 * H, x_lo:x_lo + 2 * H].copy()
    with np.errstate(all="ignore"): return np.nanmean(c.reshape(NB, C.BIN, NB, C.BIN).transpose(0, 2, 1, 3).reshape(NB, NB, -1), axis=2)
m0b = cropbin(mom0f); m1b = cropbin(mom1f); m2b = cropbin(mom2f)
TB = 1.222e6 / ((hdr["RESTFREQ"] / 1e9) ** 2 * C.BMAJ * C.BMIN)
gas_sky = 1.33 * 1.823e18 * TB * np.nan_to_num(np.clip(m0b, 0, None)) / 1.249e20
# S0a: HI mass from the full primary-beam-corrected moment 0, D 0.7 (Oh+15)
beam_px = 1.1331 * C.BMAJ * C.BMIN / (abs(cdel1) * abs(cdel2)); Sint = float(np.nansum(np.clip(mom0f, 0, None)) / beam_px)
MHI = 2.356e5 * C.OH15["D"] ** 2 * Sint; ref = C.OH15["Mgas"] / C.OH15["He"]; s0a = abs(MHI / ref - 1) <= 0.10
R["S0a"] = dict(S_int_Jykms=Sint, MHI_D07=MHI, Oh15_MHI=ref, ratio=MHI / ref, passed=bool(s0a), TB_K_per_Jybeam=TB)
P(f"S0a: S_int {Sint:.1f} Jy km/s; M_HI(0.7 Mpc) {MHI:.3e} against Oh+15 {ref:.3e} (M_gas / 1.4): ratio {MHI / ref:.3f}, line 10 % -> {'PASS' if s0a else 'FAIL'}")
# S0b: rings on moment 1 at Oh+15's geometry (A2)
mm2d = mask.any(0)
Rr, cth, sth = C.disc_coords(XE, YN, 0.0, 0.0, C.OH15["pa"], C.OH15["inc"]); si = math.sin(math.radians(C.OH15["inc"]))
rc = (np.arange(80) + 0.5) * C.RING; Vr = np.full(80, np.nan); sg = np.full(80, np.nan); Sg = np.full(80, np.nan); cov = np.zeros(80)
for k in range(80):
    rin = (Rr >= k * C.RING) & (Rr < (k + 1) * C.RING); ok = rin & np.isfinite(m1b) & mm2d & (np.abs(cth) >= 0.5)
    cov[k] = float((rin & mm2d).sum() / max(rin.sum(), 1))
    if ok.sum() >= 8:
        dvv = m1b[ok] - C.OH15["vsys"]; Vr[k] = float(np.sum(dvv * cth[ok]) / (si * np.sum(cth[ok] ** 2)))
    okk = rin & mm2d & np.isfinite(m2b)
    if okk.sum() >= 8: sg[k] = float(np.nanmean(m2b[okk])); Sg[k] = float(np.nanmean(np.nan_to_num(m0b[rin])))
Rmax_as = C.OH15["Rmax_kpc"] * 1e3 / (C.OH15["D"] * 1e6 * math.pi / (180 * 3600))
def sm3(a): b = a.copy(); b[1:-1] = (a[:-2] + a[1:-1] + a[2:]) / 3; return b
lnq = np.log(np.clip(sm3(Sg) * sm3(sg) ** 2, 1e-30, None)); dl = np.gradient(lnq, np.log(rc))
vc2 = Vr ** 2 - sm3(sg) ** 2 * dl; Vc = np.sqrt(np.clip(vc2, 0, None))
okr = np.isfinite(Vr) & np.isfinite(Vc)
v_unc = float(np.interp(Rmax_as, rc[okr], Vr[okr])); v_cor = float(np.interp(Rmax_as, rc[okr], Vc[okr])); s0b = abs(v_cor - C.OH15["Vmax"]) <= 2.0
R["S0b"] = dict(Rmax_arcsec=Rmax_as, V_rot_uncorrected=v_unc, V_c_corrected=v_cor, Oh15=C.OH15["Vmax"], passed=bool(s0b),
                rings=dict(R=rc[okr].tolist(), V=Vr[okr].tolist(), Vc=Vc[okr].tolist(), sigma=sg[okr].tolist()))
P(f"S0b: ring fit on moment 1 at Oh+15's geometry: V_rot({Rmax_as:.0f}\") {v_unc:.2f} km/s, asymmetric-drift corrected {v_cor:.2f} against Oh+15 16.9; line 2 km/s -> {'PASS' if s0b else 'FAIL'}")
# R_out: the outer edge of the last ring with >= 50 % of its azimuth in the mask (A6). The first run counted rings
# contiguously from the centre and returned 0 because of IC 1613's central HI hole; that bug is fixed here (README).
kk = int(np.nonzero(cov >= 0.5)[0].max()) + 1 if np.any(cov >= 0.5) else 0
R_out = kk * C.RING
R["ring_coverage"] = cov[:kk + 3].round(3).tolist()
P(f"R_out (last ring with >= 50 % azimuth in the mask): {R_out:.0f}\" ({C.arcsec_to_pc(R_out) / 1e3:.2f} kpc at 0.73 Mpc); M_free rings {kk}; inner rings below 50 %: {int(np.sum(cov[:kk] < 0.5))}")
# stellar profile from V (A1)
hv = fits.getheader(os.path.join(C.DATA, "ic1613v.fits")); Vimg = fits.getdata(os.path.join(C.DATA, "ic1613v.fits")).astype(np.float64)
wv = WCS(hv); yy, xx = np.mgrid[0:Vimg.shape[0], 0:Vimg.shape[1]]; sc = wv.pixel_to_world(xx.ravel(), yy.ravel())
cen = SkyCoord(C.OH15["ra"] * u.deg, C.OH15["dec"] * u.deg, frame="fk5")
dE = ((sc.ra.deg - cen.ra.deg) * math.cos(math.radians(cen.dec.deg)) * 3600).reshape(Vimg.shape); dN = ((sc.dec.deg - cen.dec.deg) * 3600).reshape(Vimg.shape)
Rv, _, _ = C.disc_coords(dE, dN, 0.0, 0.0, C.OH15["pa"], C.OH15["inc"]); fin = np.isfinite(Vimg)
bk = Vimg[fin & (Rv > 1500)]; bkg = float(np.median(bk)); P(f"V image: background median {bkg:.2f} counts from {bk.size:,} pixels at R_disc > 1500\"")
sR = (np.arange(90) + 0.5) * C.RING; sp = np.zeros(90)
for k in range(90):
    q = fin & (Rv >= k * C.RING) & (Rv < (k + 1) * C.RING)
    if q.sum() > 20: sp[k] = float(np.median(Vimg[q]) - bkg)
first_neg = np.nonzero(sp <= 0)[0]; cut = int(first_neg[0]) if len(first_neg) else len(sp); sp[cut:] = 0.0
pc = C.arcsec_to_pc(1.0); norm = float(np.sum(sp * 2 * math.pi * sR * C.RING) * pc * pc)
R["stars"] = dict(background=bkg, profile_cut_arcsec=float(cut * C.RING), half_light_arcsec=float(np.interp(0.5, np.cumsum(sp * sR) / max(np.sum(sp * sR), 1e-30), sR)))
P(f"V profile: positive out to {cut * C.RING:.0f}\"; half-light radius {R['stars']['half_light_arcsec']:.0f}\" (disc plane, Oh+15 geometry) {rss()}")
np.savez(os.path.join(C.CACHE, f"prep{TAG}.npz"), cube=cube.astype(np.float64), v=vv, mask=mask, grid=grid, XE=XE, YN=YN, noise=noise, mom0=np.clip(Sobs, 0, None),
         mom1=m1b, mom2=m2b, gas_sky=gas_sky, star_R=sR, star_prof=sp, star_norm=norm, R_out=R_out, nring=kk)
R.update(noise=noise, mask_voxels=int(mask.sum()), chi2_voxels=int((grid & mask).sum()), channels=[kmin, kmax], R_out_arcsec=R_out, n_rings=kk,
         crop=dict(x_lo=x_lo, y_lo=y_lo, size=2 * H, bin=C.BIN))
P(f"chi2 voxels on the beam-sampled grid {R['chi2_voxels']:,}; done {rss()}")
json.dump(R, open(os.path.join(HERE, f"fn4a_s0{TAG}.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"fn4a_s0{TAG}.out"), "w").write("\n".join(OUT) + "\n")
