#!/usr/bin/env python3
"""C2 of the frozen criteria: inject a synthetic Halpha+[NII] cube with a known arctangent rotation curve (V_max 200 km/s, r_t 0.4 arcsec, sigma 60 km/s, inclination 50 deg, 0.05 arcsec pixels,
beam 0.2 arcsec), noise at the level of a real SINS noise cube, run the identical pipeline and compare the recovered major-axis V_los with the input projected curve within 1 arcsec."""
import numpy as np, sys, json
from astropy.io import fits
from scipy.ndimage import gaussian_filter
sys.path.insert(0, ".")
import sins_pipeline as P
rng = np.random.default_rng(12345)
nf = "/Users/carlzimmerman/new_physics/_external_data/sins_ao/cubes/SINS-ZCSINF_AO_release/Deep3a-15504_K100_23h00_PA+00_noise_cut.fits"; df = nf.replace("noise_cut", "data_cut")
hd = fits.open(df)[0].header; wave = hd["CRVAL3"] + (np.arange(1001) + 1 - hd["CRPIX3"]) * hd["CDELT3"]
noise_real = fits.open(nf)[0].data; nlev = np.nanmedian(noise_real)
z = 2.2; nx = ny = 60; PIX = P.PIX; inc = np.radians(50); vmax, rt, sig = 200.0, 0.4, 60.0; pa_true = 30.0          # true major axis angle in the cube frame (from +y toward -x)
yy, xx = np.mgrid[0:ny, 0:nx]; x = (xx - 30) * PIX; y = (yy - 30) * PIX
th = np.radians(pa_true); ex, ey = -np.sin(th), np.cos(th); s_par = x * ex + y * ey; s_perp = -x * ey + y * ex
r = np.hypot(s_par, s_perp / np.cos(inc)); cosphi = np.where(r > 0, s_par / np.maximum(r, 1e-9), 0)
vrot = vmax * (2 / np.pi) * np.arctan(r / rt); vlos_true = vrot * np.sin(inc) * cosphi
flux = np.exp(-r / 0.5) * 2.0e-18
cube = np.zeros((1001, ny, nx)); lref = P.LHA * (1 + z)
for l0, a in ((P.LHA, 1.0), (P.LN2, 0.35), (P.LN1, 0.35 / 3)):
    lc = l0 * (1 + z) * (1 + vlos_true / P.C); s = lc * sig / P.C
    cube += a * flux[None] * np.exp(-0.5 * ((wave[:, None, None] - lc[None]) / s[None]) ** 2) / (s[None] * np.sqrt(2 * np.pi)) * 0.000245 * 1.0
cube = np.array([gaussian_filter(c, 0.2 / 2.3548 / PIX) for c in cube])
# scale signal so that the peak Halpha S/N per spaxel is about 15 with the real noise level, then add noise
peak = cube.max(); cube *= (15 * nlev) / peak
import os
CORR = len(sys.argv) > 1 and sys.argv[1] == 'corr'
if CORR:   # white noise smoothed with the 0.2 arcsec beam kernel, rescaled to the real per-channel noise level (correlated pixels)
    w = rng.normal(0, 1, cube.shape); w = np.array([gaussian_filter(c, 0.2 / 2.3548 / PIX) for c in w]); w *= nlev / w.std()
    noisy = cube + w
else: noisy = cube + rng.normal(0, nlev, cube.shape)
noise = np.full(cube.shape, nlev)
out = P.process(noisy, noise, wave, z, 100.0, np.sin(inc), fwhm=0.15, snr_cut=5.0, centre=(30, 30), amend1=CORR)
print("status", out["status"], "accepted", out["nacc"], "theta recovered %.1f (true %.1f)" % (out.get("theta_cube", np.nan), pa_true))
if out["status"] == "ok":
    res = []
    for p in out["profile"]:
        s = p["R_arcsec"]
        if abs(s) > 1.0: continue
        rr = abs(s); vin = vmax * (2 / np.pi) * np.arctan(rr / rt) * np.sin(inc) * np.sign(s)
        # the pipeline's sign follows its own gradient direction, which is the true one here
        res.append((s, vin, p["Vlos"], p["eVlos"]))
    res = np.array(res); rel = (res[:, 2] - res[:, 1]); print("bins", len(res)); print(np.round(res, 1))
    rms = float(np.sqrt(np.mean(rel ** 2))); scale = float(np.sqrt(np.mean(res[:, 1] ** 2))); print("rms difference %.2f km/s; rms of input %.1f km/s; fractional %.3f" % (rms, scale, rms / scale))
    json.dump(dict(accepted=out["nacc"], theta_recovered=out["theta_cube"], theta_true=pa_true, rms=rms, rms_input=scale, frac=rms / scale, pass_10pct=bool(rms / scale < 0.10)), open("C2_injection_result_corr_AMEND1.json" if CORR else "C2_injection_result.json", "w"), indent=1)
