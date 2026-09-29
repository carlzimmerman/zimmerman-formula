#!/usr/bin/env python3
"""CFG163 -- KURVS-15's cold gas from archival ALMA: the Ibar Band 6 dust continuum (227.3 GHz), under the frozen plan and its addendum.

Frozen plan: CFG163_FROZEN_CRITERIA.md (9ec06b770) with the addendum (5fc3c4d8e), committed before any file was read.
Data: the data chat's download (header facts e58f0d75b) in <repo>/../_external_data/alma_kurvs15/A001_X133d_X7ac/ (outside the repo).
The CO(2-1) cubes were not downloaded, so the CO channel is not run (declared).
  order       sha256 check -> rms by the frozen rule (annulus 3-10", pb >= 0.5, sources masked; robust MAD of pbcor x pb) -> power gate
              (3-sigma limit in mu_dust at 25 K, nominal M*; >= 2.14 -> NON-DIAGNOSTIC before the source pixel is read) -> the source pixel.
  measure     the pixel at KURVS-15's position (primary; point source at the 1.43" x 0.85" beam) and a 1.0"-radius aperture sum (variant).
  detection   >= 4 sigma; otherwise a 3-sigma limit, never zero.  mu_dust from Scoville et al. 2016 (CFG142's conversion) at 227.291 GHz.
MUTATE=1: a point source with mu_dust = 8 injected at KURVS-15 -> must classify 'detected, > 2.14' (exit 0 when it behaves).
MUTATE=2: KURVS-15's pixel and aperture replaced by those at an off-source position -> must classify 'not detected' (exit 0 when it behaves).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG163_kurvs15_dust.py   (MUTATE=1 or MUTATE=2 for the pinned controls)
"""
import os, sys, csv, gzip, math, hashlib
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1", "2")
R = C.Report("CFG163_kurvs15_dust" + (f"_MUTATE{MODE}" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

DDIR = os.environ.get("ALMA_KURVS15_DIR", os.path.join(os.path.dirname(REPO), "_external_data", "alma_kurvs15", "A001_X133d_X7ac"))
F_IMG = "member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw25_27_29_31.cont.I.pbcor.fits"
F_PB = "member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw25_27_29_31.cont.I.pb.fits.gz"
SHA = {F_IMG: "624890158868b9df477c12f9325c252ed2c12c7e9e58957d4761f86ba1403e51",
       F_PB: "3579fedce7450439b5468519629487a68925c94157add5d6ef354bf216cfe62d"}

# ------------------------------------------------------------------ the conversion (CFG142's, identical)
h_, k_, c_ = 6.62607015e-34, 1.380649e-23, 2.99792458e8
NU850 = c_ / 850e-6
H0, OM = 67.66, 0.30966


def d_l_gpc(z, n=20000):
    s = sum(1.0 / math.sqrt(OM * (1 + z * (i + 0.5) / n) ** 3 + 1 - OM) for i in range(n)) * z / n
    return (1 + z) * c_ / 1e3 / H0 * s / 1e3


def gam(nu, z, td):
    x = h_ * nu * (1 + z) / (k_ * td)
    return x / math.expm1(x)


def mism_per_mjy(z, nu_obs, td=25.0):
    return 1.78 * (1 + z) ** -4.8 * (NU850 / nu_obs) ** 3.8 * (gam(NU850, 0, td) / gam(nu_obs, z, td)) * d_l_gpc(z) ** 2 * 1e10


# ------------------------------------------------------------------ C0: the files are the ones the data chat hashed
ok0 = all(hashlib.sha256(open(os.path.join(DDIR, f), "rb").read()).hexdigest() == v for f, v in SHA.items())
check("C0 CONTROL: both files match the data chat's sha256 (e58f0d75b)", ", ".join(SHA), ok0)
img_h = fits.open(os.path.join(DDIR, F_IMG))[0]
with gzip.open(os.path.join(DDIR, F_PB), "rb") as fh:
    pb_h = fits.open(fh)[0]
    pb = np.squeeze(np.array(pb_h.data, float))
img = np.squeeze(np.array(img_h.data, float))
hdr = img_h.header
NU = float(hdr["CRVAL3"])
w = WCS(hdr).celestial
bmaj, bmin = float(hdr["BMAJ"]) * 3600, float(hdr["BMIN"]) * 3600
pix = abs(float(hdr["CDELT2"])) * 3600
beam_pix = math.pi / (4 * math.log(2)) * bmaj * bmin / pix ** 2
check("C2 CONTROL (continuum form): the image is the 227.3-GHz Band 6 continuum the addendum assumed; single plane; beam from the header",
      f"CRVAL3 {NU / 1e9:.3f} GHz; beam {bmaj:.3f}\" x {bmin:.3f}\" ({beam_pix:.1f} px); pixel {pix:.3f}\"; image {img.shape}",
      abs(NU / 1e9 - 227.291) < 0.01 and img.ndim == 2 and pb.shape == img.shape)

POS = {r["kurvs_id"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "kurvs_positions", "kurvs_positions.csv")))}
K = POS["15"]
z, lm = float(K["z_halpha"]), float(K["logMstar"])
x0, y0 = (float(v) for v in w.world_to_pixel_values(float(K["ra_deg"]), float(K["dec_deg"])))
yy, xx = np.indices(img.shape)
rr = np.hypot(xx - x0, yy - y0) * pix
mask = np.zeros(img.shape, bool)
srcs = [(float(r["ra_deg"]), float(r["dec_deg"])) for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "goodsalma_crossmatch", "goodsalma2_catalogue.csv")))]
srcs += [(float(r["ra_deg"]), float(r["dec_deg"])) for k, r in POS.items()]
nmask = 0
for ra, de in srcs:
    xs, ys = (float(v) for v in w.world_to_pixel_values(ra, de))
    if -20 <= xs <= img.shape[1] + 20 and -20 <= ys <= img.shape[0] + 20:
        m = np.hypot(xx - xs, yy - ys) * pix < 2.0
        if m.any():
            mask |= m; nmask += 1

# ------------------------------------------------------------------ the rms rule (frozen) and the power gate, BEFORE the source pixel
ann = (rr >= 3.0) & (rr <= 10.0) & (pb >= 0.5) & np.isfinite(img) & ~mask
flat = img[ann] * pb[ann]                                        # pbcor x pb = the flat-noise (non-pb-corrected) image
sig0 = 1.4826 * np.median(np.abs(flat - np.median(flat)))
std0 = float(np.std(flat))
pb_src = float(pb[int(round(y0)), int(round(x0))])
sigma = sig0 / pb_src * 1e3                                      # mJy/beam at the source
per = mism_per_mjy(z, NU)                                        # Msun per mJy
s_unit = 10 ** lm / per                                          # mJy per unit mu_dust (25 K, nominal M*)
mu3 = 3 * sigma / s_unit
P(f"  rms rule: annulus 3-10\", pb >= 0.5, {nmask} catalogue/KURVS positions masked within the image; {ann.sum()} pixels; robust sigma0 {sig0 * 1e6:.1f} uJy/beam "
  f"(plain std {std0 * 1e6:.1f}); pb at KURVS-15 {pb_src:.4f}; sigma at the source {sigma * 1e3:.1f} uJy/beam (archive estimate 64.6 per window / ~32 over four)")
check("C3 CONTROL (continuum form): the robust MAD sigma and the plain std of the same masked annulus agree within 30%",
      f"MAD {sig0 * 1e6:.1f} vs std {std0 * 1e6:.1f} uJy/beam", abs(std0 / sig0 - 1) < 0.30)
gate = mu3 < 2.14
P(f"  POWER GATE: 3-sigma limit in mu_dust (25 K, nominal M* {lm}) = {mu3:.2f}  ->  {'PASS: the channel can reach below 2.14' if gate else 'FAIL: NON-DIAGNOSTIC, the source pixel is not read for a verdict'}")
R.num("gate", dict(sigma0_uJy=sig0 * 1e6, std_uJy=std0 * 1e6, pb_src=pb_src, sigma_src_uJy=sigma * 1e3, mu_dust_3sigma=mu3, passes=gate, n_ann=int(ann.sum())))

# ------------------------------------------------------------------ C1: injection recovery at an off-source position
def inject(image, xs, ys, peak_jy):
    sx, sy = bmaj / pix / 2.3548, bmin / pix / 2.3548             # beam axes (PA ignored for the injection; declared)
    return image + peak_jy * np.exp(-0.5 * (((xx - xs) / sx) ** 2 + ((yy - ys) / sy) ** 2))


xo, yo = x0 + 6.0 / pix, y0                                      # 6" east-west offset, inside the annulus region
inj = 10 * sig0
rec = inject(img * pb, xo, yo, inj)[int(round(yo)), int(round(xo))] - (img * pb)[int(round(yo)), int(round(xo))]
check("C1 CONTROL (injection): a 10-sigma point source injected 6\" off-source is recovered by the pixel measurement within 15%",
      f"injected {inj * 1e6:.1f} uJy, recovered {rec * 1e6:.1f} uJy ({rec / inj:.3f})", abs(rec / inj - 1) < 0.15)
c4 = 2 * 10 ** 10.07 / mism_per_mjy(1.613, c_ / 1.1e-3)
check("C4 CONTROL: the conversion reproduces CFG142's pre-data table for KURVS-15 at 272.5 GHz (S(mu_dust = 2) = 0.222 mJy)",
      f"{c4:.4f} mJy", abs(c4 - 0.222) < 1.5e-3)

# ------------------------------------------------------------------ the source (read only after the gate)
work = img.copy()
if MODE == "1":
    work = inject(img * pb, x0, y0, 8 * s_unit * 1e-3) / pb        # mu_dust = 8 at the source (Jy/beam in the pbcor image)
if MODE == "2":
    work = img.copy()
    dx = int(round(6.0 / pix))
    work = np.roll(np.roll(img, -dx, axis=1), 0, axis=0)          # the source position now carries the off-source values 6" away
if gate or MODE:
    S_pix = float(work[int(round(y0)), int(round(x0))]) * 1e3    # mJy (peak pixel, point source)
    ap = rr <= 1.0
    S_ap = float(np.nansum(work[ap]) / beam_pix) * 1e3
    snr = S_pix / sigma
    detected = snr >= 4
    mu_nom = (S_pix if detected else 3 * sigma) * per / 10 ** lm
    mu_35 = (S_pix if detected else 3 * sigma) * mism_per_mjy(z, NU, 35.0) / 10 ** lm
    if detected:
        cls = "detected, > 2.14" if mu_nom > 2.14 else ("detected, 0.65-2.14" if mu_nom >= 0.65 else "detected, < 0.65")
    else:
        cls = "not detected, limit < 0.65" if mu_nom < 0.65 else ("not detected, limit 0.65-2.14" if mu_nom < 2.14 else "not detected, NON-DIAGNOSTIC")
    P(f"  KURVS-15: pixel {S_pix * 1e3:+.1f} uJy/beam ({snr:+.1f} sigma); 1.0\" aperture {S_ap * 1e3:+.1f} uJy; "
      f"{'detected' if detected else '3-sigma limit'}: mu_dust {'=' if detected else '<'} {mu_nom:.2f} (25 K, nominal), {mu_35:.2f} (35 K); "
      f"x2 gas-to-dust: {2 * mu_nom:.2f}; M* -0.2 dex: {mu_nom / 10 ** -0.2:.2f}  ->  {cls}")
    R.num("source", dict(S_pix_uJy=S_pix * 1e3, S_ap_uJy=S_ap * 1e3, snr=snr, detected=bool(detected), mu_dust_nominal=mu_nom, mu_dust_35K=mu_35,
                         mu_x2=2 * mu_nom, classification=cls))
else:
    cls = "NON-DIAGNOSTIC (power gate)"
if MODE == "1":
    check("MUTATE=1 [pinned control]: an injected mu_dust = 8 point source classifies 'detected, > 2.14'", cls, cls == "detected, > 2.14")
elif MODE == "2":
    check("MUTATE=2 [pinned control]: the off-source values at the source position classify 'not detected'", cls, cls.startswith("not detected"))
else:
    check("H1 [HEADLINE, reported] KURVS-15's dust-traced gas against the break-evens (0.65 rival, 2.14 flat)", cls, True, load_bearing=False)
R.num("classification", cls)
nf = R.write()
raise SystemExit(1 if nf else 0)
