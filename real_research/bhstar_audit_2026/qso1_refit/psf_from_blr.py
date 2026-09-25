"""Measure the PSF at H-alpha directly from the FULL QSO1 cube (Zenodo 19402518,
output_cube_mMSA_manMask_0.02px_cgs_s3d.fits, 6.4 GB, md5 ba79ff16aa19c41d2d915c1b1effc6b3; gitignored).

Two independent point-source images (both unresolved at 0.02" by orders of magnitude):
  (1) the BROAD H-alpha wings, 650 < |v| < 2500 km/s about z_sys = 7.0367, [NII] +/-150 km/s masked (beyond ~625 km/s
      the extended intermediate/outflow component, FWHM ~490, has died away; the FWHM ~1800 BLR component -- light-days
      across -- dominates), each spaxel continuum-subtracted (median of line-free sidebands);
  (2) the red CONTINUUM in those sidebands (AGN-dominated, stellar < 10% per Juodzbalis+26).
Each is fitted with an elliptical 2D Gaussian + constant; the NARROW-line core of the published narrow-only cube is
fitted the same way.  A narrow core SHARPER than the point-source PSF is physically impossible and would mark a
processing artifact in the narrow-only product.
Sidebands avoid [NII] 6548/6583 (-730/+940), He I 6678 (+5185) and [SII] 6716/6731 (+6950/+7600 km/s).
"""
import os, json, hashlib
import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FULL = os.path.join(REPO, "real_research", "data", "qso1", "output_cube_mMSA_manMask_0.02px_cgs_s3d.fits")
NARROW = os.path.join(REPO, "real_research", "data", "qso1", "Halpha_nr_only_cube_02px.fits")
MD5 = "ba79ff16aa19c41d2d915c1b1effc6b3"
C = 299792.458
LAM0 = 0.6564614 * (1 + 7.0367)
PIX = 0.02


def md5sum(path, chunk=1 << 24):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def gauss2d(xy, A, x0, y0, sx, sy, th, B):
    x, y = xy
    ct, st = np.cos(th), np.sin(th)
    xr = (x - x0) * ct + (y - y0) * st
    yr = -(x - x0) * st + (y - y0) * ct
    return (A * np.exp(-0.5 * ((xr / sx) ** 2 + (yr / sy) ** 2)) + B).ravel()


def fit_img(img, yc, xc, half=20):
    y0, y1 = max(0, yc - half), min(img.shape[0], yc + half + 1)
    x0, x1 = max(0, xc - half), min(img.shape[1], xc + half + 1)
    cut = np.nan_to_num(img[y0:y1, x0:x1])
    yy, xx = np.mgrid[y0:y1, x0:x1]
    p0 = [cut.max(), xc, yc, 4.0, 4.0, 0.0, np.median(cut)]
    p, cov = curve_fit(gauss2d, (xx, yy), cut.ravel(), p0=p0, maxfev=20000)
    A, xm, ym, sx, sy, th, B = p
    e = np.sqrt(np.diag(cov))
    f = 2.3548 * PIX
    return {"x": float(xm), "y": float(ym), "fwhm_a": float(f * max(abs(sx), abs(sy))), "fwhm_b": float(f * min(abs(sx), abs(sy))),
            "fwhm_geo": float(f * np.sqrt(abs(sx * sy))), "err_geo": float(f * 0.5 * np.sqrt(abs(sx * sy)) * np.hypot(e[3] / sx, e[4] / sy)),
            "theta_deg": float(np.degrees(th) % 180), "sx_px": float(abs(sx)), "sy_px": float(abs(sy)), "th_rad": float(th)}


def main(verify=True):
    out = {}
    if verify:
        m = md5sum(FULL)
        out["md5_ok"] = (m == MD5)
        print("md5", m, "OK" if m == MD5 else "MISMATCH")
        assert m == MD5, "full cube checksum mismatch"
    h = fits.open(FULL, memmap=True)
    sci = h["SCI"].data
    hd = h["SCI"].header
    lam = hd["CRVAL3"] + np.arange(hd["NAXIS3"]) * hd["CDELT3"]
    v = (lam / LAM0 - 1) * C
    side = ((v > -7000) & (v < -4000)) | ((v > 3500) & (v < 4800))
    wing = (((v > -2500) & (v < -650)) | ((v > 650) & (v < 2500))) & (np.abs(v - 940) > 150) & (np.abs(v + 730) > 150)
    idx_s, idx_w = np.where(side)[0], np.where(wing)[0]
    lo, hi = min(idx_s.min(), idx_w.min()), max(idx_s.max(), idx_w.max()) + 1
    block = np.array(sci[lo:hi], dtype=float)                          # (nch, ny, nx) slab around H-alpha only
    vv = v[lo:hi]
    s_m, w_m = side[lo:hi], wing[lo:hi]
    ok = np.isfinite(block).all(axis=0)
    # per-spaxel robust continuum (median of the sidebands)
    cont = np.nanmedian(block[s_m], axis=0)
    broad = np.nansum(block[w_m], axis=0) - w_m.sum() * cont
    contimg = cont.copy()
    broad[~ok] = np.nan; contimg[~ok] = np.nan
    # QSO1 = the H-alpha line-core peak (the global argmax of the wing image is a hot pixel far from the source)
    core = np.nansum(np.array(sci[np.where(np.abs(v) < 250)[0].min():np.where(np.abs(v) < 250)[0].max() + 1], dtype=float), axis=0)
    core = np.where(ok, core, np.nan)
    yq, xq = np.unravel_index(np.nanargmax(np.nan_to_num(core, nan=-np.inf, posinf=-np.inf)), core.shape)
    sub = np.nan_to_num(broad[yq - 10:yq + 11, xq - 10:xq + 11], nan=-np.inf)
    dy, dx = np.unravel_index(np.argmax(sub), sub.shape)
    yb, xb = yq - 10 + dy, xq - 10 + dx
    out["qso1_core_peak_yx"] = [int(yq), int(xq)]
    out["broad_peak_yx"] = [int(yb), int(xb)]
    out["psf_broad"] = fit_img(broad, yb, xb)
    out["psf_continuum"] = fit_img(contimg, yb, xb)
    # narrow core of the published narrow-only cube (its own grid)
    hn = fits.open(NARROW)
    dn = hn["SCI"].data; hdn = hn["SCI"].header
    lamn = hdn["CRVAL3"] + np.arange(dn.shape[0]) * hdn["CDELT3"]
    vn = (lamn / LAM0 - 1) * C
    nimg = np.nansum(dn[np.abs(vn) < 250], axis=0)
    yn, xn = np.unravel_index(np.nanargmax(nimg), nimg.shape)
    out["narrow_core"] = fit_img(nimg, yn, xn, half=12)
    # locate the narrow cutout in the full grid by cross-correlating its image with the full-cube narrow window
    fullnarrow = np.nan_to_num(core, nan=0.0, posinf=0.0, neginf=0.0)
    best = None
    ny, nx = nimg.shape
    a = (nimg - np.nanmean(nimg)).ravel()
    for oy in range(0, fullnarrow.shape[0] - ny):
        for ox in range(0, fullnarrow.shape[1] - nx):
            b = np.nan_to_num(fullnarrow[oy:oy + ny, ox:ox + nx]); b = (b - b.mean()).ravel()
            cc = float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-30))
            if best is None or cc > best[0]:
                best = (cc, oy, ox)
    out["cutout_offset_yx"] = [best[1], best[2]]; out["cutout_corr"] = best[0]
    out["narrow_peak_in_full_yx"] = [int(yn + best[1]), int(xn + best[2])]
    out["narrow_minus_broad_peak_px"] = [out["narrow_peak_in_full_yx"][0] - int(yb), out["narrow_peak_in_full_yx"][1] - int(xb)]
    # robustness of the PSF to the wing window, and the RAW line-core size (narrow + broad, continuum-subtracted)
    vvv = v[lo:hi]
    nii = (np.abs(vvv - 940) > 150) & (np.abs(vvv + 730) > 150)
    wins = {"650-2500 both": (np.abs(vvv) > 650) & (np.abs(vvv) < 2500) & nii,
            "blue 650-2500": (vvv < -650) & (vvv > -2500) & nii, "red 650-2500": (vvv > 650) & (vvv < 2500) & nii,
            "800-2000 both": (np.abs(vvv) > 800) & (np.abs(vvv) < 2000) & nii,
            "1000-3000 both": (np.abs(vvv) > 1000) & (np.abs(vvv) < 3000) & nii,
            "500-1500 both": (np.abs(vvv) > 500) & (np.abs(vvv) < 1500) & nii}
    out["psf_window_robustness"] = {}
    for k, m in wins.items():
        im = np.nansum(block[m], axis=0) - m.sum() * cont; im[~ok] = np.nan
        out["psf_window_robustness"][k] = fit_img(im, int(yq), int(xq), half=15)["fwhm_geo"]
    out["raw_line_core"] = {}
    for w in (100, 150, 250):
        m = np.abs(vvv) < w
        im = np.nansum(block[m], axis=0) - m.sum() * cont; im[~ok] = np.nan
        out["raw_line_core"][str(w)] = fit_img(im, int(yq), int(xq), half=15)["fwhm_geo"]
    out["published_narrow_core"] = {}
    for w in (100, 150, 250):
        im = np.nansum(dn[np.abs(vn) < w], axis=0); y_, x_ = np.unravel_index(np.nanargmax(im), im.shape)
        out["published_narrow_core"][str(w)] = fit_img(im, y_, x_, half=12)["fwhm_geo"]
    json.dump(out, open(os.path.join(HERE, "psf_from_blr.json"), "w"), indent=1)
    for k in ("psf_broad", "psf_continuum", "narrow_core"):
        r = out[k]
        print(f"{k:14s}: FWHM {r['fwhm_a']:.3f}\" x {r['fwhm_b']:.3f}\"  (geo {r['fwhm_geo']:.3f} +/- {r['err_geo']:.3f}\")  PA {r['theta_deg']:.0f} deg")
    print("cutout offset (y, x) =", out["cutout_offset_yx"], "corr", round(out["cutout_corr"], 3),
          "| narrow - broad peak (px):", out["narrow_minus_broad_peak_px"])
    return out


if __name__ == "__main__":
    main(verify=os.environ.get("NOVERIFY") != "1")
