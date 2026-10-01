#!/usr/bin/env python3
"""3-D forward-model rotation-curve fit for KMOS3D cubes, as fixed in FROZEN_CRITERIA_2026-09-30.md (commit d73236046).
Implementation details not spelled out there: model oversampling 0.1 arcsec; V_a bounded to [5, 800] km/s; the 8 starts run with max_nfev=30 and the best two are polished to convergence;
channel integration by sampling the Gaussian at channel centres; the Halpha rest wavelength is vacuum 0.6564614 um, [NII] 0.6585271 and 0.6549860 um."""
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.optimize import least_squares
from scipy.signal import fftconvolve
from scipy.ndimage import zoom
C = 299792.458; PIXS = 0.2; OS = 2; MS = PIXS / OS
LHA, LN2, LN1 = 0.6564614, 0.6585271, 0.6549860
class Cube:
    def __init__(self, path, z, ra, dec, rhalf, q, specres, q0=0.2, window=1800.0, specres_fallback=3870.0):
        h = fits.open(path); self.flux = h[1].data.astype(float); self.noise = h[2].data.astype(float); psf = h[4].data.astype(float)
        hd = h[1].header; nz, ny, nx = self.flux.shape
        self.lam = hd["CRVAL3"] + (np.arange(nz) + 1 - hd["CRPIX3"]) * hd["CDELT3"]; self.dlam = hd["CDELT3"]
        w = WCS(hd, naxis=2); px, py = w.all_world2pix(ra, dec, 0); self.xc, self.yc = float(px), float(py)   # catalogue position in pixel coordinates (0-based)
        self.notes = []
        if not (0 <= self.xc < nx and 0 <= self.yc < ny):   # post-run fix: catalogue position outside the cube footprint -> use the cube reference pixel
            self.xc, self.yc = hd["CRPIX1"] - 1, hd["CRPIX2"] - 1; self.notes.append("position outside cube: cube centre used")
        if not (specres > 0):   # post-run fix: catalogue SPEC_RES missing (0): median of the positive K-band values at z>=1.9 (3870)
            specres = specres_fallback; self.notes.append("SPEC_RES missing: 3870 used")
        self.z = z; self.rd = rhalf / 1.68; self.rhalf = rhalf; self.ny, self.nx = ny, nx
        cos2 = (q ** 2 - q0 ** 2) / (1 - q0 ** 2); self.cosi = np.sqrt(max(cos2, np.cos(np.radians(85)) ** 2)); self.sini = np.sqrt(1 - self.cosi ** 2)
        self.sig_lsf = C / (2.355 * specres)
        lref = LHA * (1 + z); v = (self.lam / lref - 1) * C
        # empirical noise scale from line-free channels (beyond 2500 km/s of Halpha), sky-line channels (noise > 2x median) masked
        med = np.nanmedian(self.noise); good = (np.isfinite(self.noise).mean(axis=(1, 2)) > 0.5) & (np.nanmedian(self.noise, axis=(1, 2)) < 2 * med)
        far = (np.abs(v) > 2500) & good
        x = self.flux[far]; mad = np.nanmedian(np.abs(x - np.nanmedian(x, axis=0)))
        self.scale = float(1.4826 * mad / np.nanmedian(self.noise[far])) if far.sum() > 20 else 1.0
        win = (np.abs(v) < window) & good
        self.win = np.where(win)[0]; self.lamw = self.lam[self.win]
        self.d = self.flux[self.win]; self.s = self.noise[self.win] * self.scale
        self.ok = np.isfinite(self.d) & np.isfinite(self.s) & (self.s > 0)
        self.d = np.where(self.ok, self.d, 0.0); self.winv = np.where(self.ok, 1.0 / np.where(self.s > 0, self.s, 1), 0.0)
        # PSF resampled to the model grid (0.1 arcsec), normalised
        p = zoom(np.clip(np.nan_to_num(psf, nan=0.0), 0, None), OS, order=1); p /= p.sum(); self.psf = p
        # model grid covering the cube, in arcsec offsets from the cube centre pixel (pixel centres at integers)
        gy = (np.arange(ny * OS) + 0.5) / OS - 0.5; gx = (np.arange(nx * OS) + 0.5) / OS - 0.5
        self.gx, self.gy = np.meshgrid(gx, gy)       # pixel coordinates of the model sub-pixels
        self.lref = lref
    def model(self, p, nlam=None):
        x0, y0, pa, va, rt, s0, dv, ftot, nii = p
        # sky offsets in arcsec (east, north); east is to the left (x decreases with RA increasing)
        dE = -(self.gx - (self.xc + x0 / PIXS)) * PIXS; dN = (self.gy - (self.yc + y0 / PIXS)) * PIXS
        pa_r = np.radians(pa); s = dE * np.sin(pa_r) + dN * np.cos(pa_r); m = -dE * np.cos(pa_r) + dN * np.sin(pa_r)
        r = np.hypot(s, m / self.cosi); r_safe = np.maximum(r, 1e-6); cosphi = s / r_safe
        vrot = (2 / np.pi) * va * np.arctan(r / rt); vlos = vrot * self.sini * cosphi + dv
        sb = np.exp(-r / self.rd); sb = sb / sb.sum()                       # flux fraction per sub-pixel
        sig = np.sqrt(s0 ** 2 + self.sig_lsf ** 2)
        lam = self.lamw[:, None, None]; out = np.zeros((len(self.lamw),) + sb.shape)
        for l0, a in ((LHA, 1.0), (LN2, nii), (LN1, nii / 3.0)):
            lc = l0 * (1 + self.z) * (1 + vlos / C); sl = lc * sig / C
            out += (a * sb)[None] * np.exp(-0.5 * ((lam - lc[None]) / sl[None]) ** 2) / (sl[None] * np.sqrt(2 * np.pi))
        out = fftconvolve(out, self.psf[None], mode="same", axes=(1, 2))
        out = out.reshape(len(self.lamw), self.ny, OS, self.nx, OS).sum(axis=(2, 4))      # sum sub-pixels into 0.2 arcsec pixels
        return ftot * out
    def resid(self, p):
        m = self.model(p); r = (self.d - m) * self.winv
        # analytic per-spaxel linear continuum (variable projection)
        u0 = self.winv; u1 = (self.lamw[:, None, None] - self.lref) * self.winv
        a00 = (u0 * u0).sum(0); a01 = (u0 * u1).sum(0); a11 = (u1 * u1).sum(0); b0 = (u0 * r).sum(0); b1 = (u1 * r).sum(0)
        det = a00 * a11 - a01 ** 2; det = np.where(det > 0, det, np.inf)
        c0 = (a11 * b0 - a01 * b1) / det; c1 = (a00 * b1 - a01 * b0) / det
        r = r - (c0[None] * u0 + c1[None] * u1)
        return r[self.ok]
BOUNDS_LO = [-0.4, -0.4, -720, 5, 0.02, 10, -400, 0, 0]; BOUNDS_HI = [0.4, 0.4, 720, 800, 3.0, 250, 400, 1e4, 1.5]
def fit(cube, f0, polish=2, pa_offset=0.0):
    starts = []
    for pa0 in np.arange(0, 360, 45) + pa_offset:
        starts.append([0, 0, pa0, 150, 0.5, 60, 0, f0, 0.2])
    res = []
    for p0 in starts:
        try: r = least_squares(cube.resid, p0, bounds=(BOUNDS_LO, BOUNDS_HI), x_scale=[0.1, 0.1, 30, 50, 0.3, 30, 50, max(f0, 1), 0.3], max_nfev=30, method="trf"); res.append(r)
        except Exception: pass
    res.sort(key=lambda r: r.cost); best = None
    for r in res[:polish]:
        try: rr = least_squares(cube.resid, r.x, bounds=(BOUNDS_LO, BOUNDS_HI), x_scale=[0.1, 0.1, 30, 50, 0.3, 30, 50, max(f0, 1), 0.3], max_nfev=200, method="trf")
        except Exception: rr = r
        if best is None or rr.cost < best.cost: best = rr
    return best
def summarize(cube, r):
    p = r.x; n = len(r.fun); dof = max(n - len(p), 1); chi2r = 2 * r.cost / dof
    J = r.jac; 
    try: cov = np.linalg.inv(J.T @ J) * max(1.0, chi2r)
    except Exception: cov = np.full((len(p), len(p)), np.nan)
    err = np.sqrt(np.clip(np.diag(cov), 0, None))
    def v_at(rr, va=p[3], rt=p[4]): return (2 / np.pi) * va * np.arctan(rr / rt)
    out = dict(x0=p[0], y0=p[1], PA=p[2] % 360, Va=p[3], rt=p[4], sig0=p[5], dv=p[6], Ftot=p[7], nii=p[8], eVa=err[3], ert=err[4], esig0=err[5], chi2r=chi2r, nfit=n,
               edge=bool(any(np.isclose(p[i], BOUNDS_LO[i], atol=1e-3 * (abs(BOUNDS_LO[i]) + 1)) or np.isclose(p[i], BOUNDS_HI[i], atol=1e-3 * (abs(BOUNDS_HI[i]) + 1)) for i in (0, 1, 3, 4, 5, 6))),
               inc_deg=float(np.degrees(np.arccos(cube.cosi))), rd=cube.rd, rhalf=cube.rhalf, noise_scale=cube.scale, notes="; ".join(cube.notes))
    for name, rr in (("V22", 2.2 * cube.rd), ("Vre", cube.rhalf)):
        out[name] = v_at(rr)
        g = np.zeros(len(p)); eps = 1e-3
        for i in (3, 4):
            q = p.copy(); q[i] += eps * (abs(p[i]) + 1); g[i] = ((2 / np.pi) * q[3] * np.arctan(rr / q[4]) - out[name]) / (eps * (abs(p[i]) + 1))
        out["e" + name] = float(np.sqrt(max(g @ cov @ g, 0)))
    # last radius where the model line-integrated S/N per 0.2 arcsec pixel exceeds 1
    sigl = LHA * (1 + cube.z) * np.sqrt(p[5] ** 2 + cube.sig_lsf ** 2) / C; nl = max(2.355 * sigl / cube.dlam, 1.0)
    sF = np.sqrt(nl) * np.nanmedian(cube.s) * cube.dlam
    rr = np.linspace(0.02, 3.0, 300); sbr = p[7] * np.exp(-rr / cube.rd) / (2 * np.pi * cube.rd ** 2 * cube.cosi) * PIXS ** 2
    sel = rr[sbr / sF > 1]; out["rmax"] = float(sel.max()) if len(sel) else 0.0
    # integrated model line sigma (flux-weighted second moment of the whole model cube about its mean), km/s
    m = cube.model(p); spec = m.sum(axis=(1, 2)); v = (cube.lamw / cube.lref - 1) * C
    sel = np.abs(v - p[6]) < 600; w = np.clip(spec[sel], 0, None); mu = (w * v[sel]).sum() / w.sum(); out["sig_int"] = float(np.sqrt((w * (v[sel] - mu) ** 2).sum() / w.sum()))
    return out
