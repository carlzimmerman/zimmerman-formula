"""CFG970 POST-HOC (labelled, not graded; written after the frozen run was INVALID): 2" and 1" aperture spectra at the KLASS position and at the
pointing centre (the cube's own target, image A1.4), integrated over +-150 km/s, with S/N from the flat-frame noise. Run: python3 cfg970_posthoc_apertures.py"""
import os, math, gzip, json, warnings, numpy as np
from astropy.io import fits
from astropy.wcs import WCS, FITSFixedWarning
warnings.filterwarnings("ignore", category=FITSFixedWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); DD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data", "alma_2013.1.00582.S_A1.4")
FC = os.path.join(DD, "member.uid___A001_X12b_Xa.MACS1149_A1.4_CO_v_0_3_2_image.pbcor.fits"); FP = FC.replace("pbcor.fits", "flux.fits.gz")
H = fits.getheader(FC); W = WCS(H).celestial; cube = fits.open(FC, memmap=True)[0].data
NX, NY, NC = H["NAXIS1"], H["NAXIS2"], H["NAXIS3"]; pix = abs(H["CDELT1"]) * 3600; bp = 1.1331 * H["BMAJ"] * H["BMIN"] * 3600 ** 2 / pix ** 2
nu0 = 345.79599e9 / 2.4906; f = H["CRVAL3"] + (np.arange(NC) + 1 - H["CRPIX3"]) * H["CDELT3"]; v = 299792.458 * (nu0 - f) / nu0; dv = abs(v[1] - v[0])
hb = fits.getheader(FP); hs = len(hb.tostring())
with gzip.open(FP, "rb") as g: g.seek(hs + NC // 2 * NX * NY * 4); PB = np.frombuffer(g.read(NX * NY * 4), ">f4").reshape(NY, NX).astype(float)
PB[~np.isfinite(PB)] = 0; yy, xx = np.mgrid[0:NY, 0:NX]
LF = list(range(40)) + list(range(NC - 40, NC))
sig = np.median([1.4826 * np.median(np.abs(a - np.median(a))) for a in (np.nan_to_num(np.array(cube[0, c], float)) * PB for c in LF) for a in [a[PB >= 0.9]]])
out = {}
for name, (ra, de) in {"KLASS position": (177.397034, 22.396011), "pointing centre (A1.4)": (H["CRVAL1"], H["CRVAL2"])}.items():
    x, y = (float(t) for t in W.world_to_pixel_values(ra, de))
    for rad in (1.0, 2.0):
        ap = ((xx - x) ** 2 + (yy - y) ** 2 <= (rad / pix) ** 2) & (PB >= 0.3)
        spec = np.array([np.nan_to_num(np.array(cube[0, c], float))[ap].sum() / bp for c in range(NC)])
        sel = np.abs(v) <= 150; S = spec[sel].sum() * dv
        e = sig * math.sqrt((1 / PB[ap] ** 2).sum() / bp) * dv * math.sqrt(sel.sum())
        out[f"{name} r={rad}\""] = dict(Sdv=S, err=e, SN=S / e, PB=float(PB[int(round(y)), int(round(x))]))
        print(f"{name:24s} r={rad:.0f}\": S dv(+-150 km/s) = {S:+.3f} +- {e:.3f} Jy km/s (S/N {S/e:+.2f}); PB {PB[int(round(y)), int(round(x))]:.2f}")
json.dump(dict(flat_rms_Jy=sig, apertures=out), open(os.path.join(HERE, "cfg970_posthoc_apertures.json"), "w"), indent=1)
