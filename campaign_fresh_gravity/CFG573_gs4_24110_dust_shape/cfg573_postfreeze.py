#!/usr/bin/env python3
"""CFG573 POST-FREEZE (reported only, never a verdict): the frozen run found no >=5 sigma detection at 0.13". Two follow-ups:
(1) a size LOWER bound from the peak limit and the expected total flux; (2) image-plane smoothing to 0.3/0.5/0.8" with peak S/N (noise from the same smoothed annulus)."""
import os, json, math
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
D = os.path.join(ROOT, "data_assembly", "gs4_24110_cubes")
h = fits.getheader(os.path.join(D, "gs4_24110_cont.I.pbcor.fits")); img = np.squeeze(fits.getdata(os.path.join(D, "gs4_24110_cont.I.pbcor.fits"))).astype(float)
pb = np.squeeze(fits.getdata(os.path.join(D, "gs4_24110_cont.I.pb.fits.gz"))).astype(float)
w = WCS(h).celestial; pix = abs(h["CDELT1"]) * 3600; bmaj, bmin = h["BMAJ"] * 3600, h["BMIN"] * 3600; tb = math.sqrt(bmaj * bmin)
dc = 2.99792458e5 / 70 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, 1.9972)[0]; kas = dc / 2.9972 * 1e3 / 206264.806
x0, y0 = w.world_to_pixel_values(53.166889, -27.798733); yy, xx = np.mgrid[:img.shape[0], :img.shape[1]]; rr = np.hypot(xx - x0, yy - y0) * pix
out = []; P = lambda s: (print(s), out.append(s))
img0 = np.where(np.isfinite(img), img, 0.0)
S_exp = 342e-6 * (264.93 / 242.6) ** 3.8; R = {}
for th in (None, 0.3, 0.5, 0.8):
    if th is None: im, bm = img0, tb
    else:
        k = math.sqrt(max(th ** 2 - tb ** 2, 0)) / 2.3548 / pix; im = gaussian_filter(img0, k) * (th ** 2 / tb ** 2); bm = th   # Jy/beam at the new beam
    ann = (rr > 2) & (rr < 6) & (pb >= 0.5); s = 1.4826 * np.median(np.abs(im[ann] - np.median(im[ann])))
    pk = im[rr <= 0.5].max(); R[str(th)] = dict(beam=bm, peak_uJy=pk * 1e6, rms_uJy=s * 1e6, snr=pk / s, expected_peak_if_point_uJy=S_exp * 1e6)
    P(f"beam {bm:.2f}\": peak {pk * 1e6:6.1f} uJy/beam, rms {s * 1e6:5.1f}, S/N {pk / s:4.1f}; a point source of the expected {S_exp * 1e6:.0f} uJy would give S/N {S_exp / s:.1f}")
pk_up = (R["None"]["peak_uJy"] + 2 * R["None"]["rms_uJy"]) * 1e-6; S_lo = (342e-6 - 2 * 34e-6) * (264.93 / 242.6) ** 3.8
fr = pk_up / S_lo; ts = tb * math.sqrt(max(1 / fr - 1, 0)); Re_lo = ts / 2 * kas
P(f"size LOWER bound (peak + 2 sigma = {pk_up * 1e6:.0f} uJy/beam vs total >= {S_lo * 1e6:.0f} uJy): FWHM >= {ts:.2f}\" -> R_e,dust >= {Re_lo:.2f} kpc (stellar/Halpha R_e 7.39 kpc)")
R["Re_lower_kpc"] = Re_lo
json.dump(R, open(os.path.join(HERE, "cfg573_postfreeze_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg573_postfreeze.out"), "w").write("\n".join(out) + "\n")

# crude size from the smoothed peaks (peak = S theta^2/(theta^2+theta_s^2), S = expected total): reported only, all at ~3 sigma
ths = {}
for th in ("0.3", "0.5", "0.8"):
    p = R[th]["peak_uJy"] * 1e-6; t = float(th); ths[th] = math.sqrt(max(S_exp * t * t / p - t * t, 0))
P("crude dust FWHM from smoothed peaks (~3 sigma each): " + ", ".join(f"{k}\" beam -> {v:.2f}\" (R_e {v / 2 * kas:.1f} kpc)" for k, v in ths.items()))
# what a gas disc of that size does to Delta_v (dust-route gas 10^10.51, M* 10.89, canon), vs CFG572's R_g = R_d = 4.40 kpc
import sys; sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity", "CFG44_fluid_target"))
from scipy.special import i0, i1, k0, k1
G = 4.30091e-6; RE = 7.39; Bf = lambda y: y * y * (i0(y) * k0(y) - i1(y) * k1(y)); v2 = lambda M, Rd: 2 * G * M / Rd * Bf(RE / (2 * Rd))
J5 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]["GS4_24110"]["10.89"]
for Reg in (7.39, 2.9, 2.0):
    vb = v2(10 ** 10.89, RE / 1.678) + v2(10 ** 10.51, Reg / 1.678)
    row = {m: math.log10(vb / (10 ** J5[f"canon 9.36e-11|{m}"]["logVbar2R_G"] * G / RE)) for m in ("F-DESI", "R-H")}
    P(f"  gas R_e {Reg:.1f} kpc: Delta_v F-DESI {row['F-DESI']:+.2f}, a0~H(z) {row['R-H']:+.2f}, Newton {math.log10(vb / 206.0 ** 2):+.2f}")
open(os.path.join(HERE, "cfg573_postfreeze.out"), "w").write("\n".join(out) + "\n")
