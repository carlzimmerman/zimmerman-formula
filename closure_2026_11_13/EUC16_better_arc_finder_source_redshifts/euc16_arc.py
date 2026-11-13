#!/usr/bin/env python3
"""EUC16 arc finder (image only).  Frozen in FROZEN_CRITERIA.md section 2; the lane uses `arc_euc16` and nothing else.

Every finder here reads one VIS box (64 x 64 pixels, 0.1 arcsec per pixel, background-subtracted mosaic) and returns
one sky offset (east, north) in arcsec from the lens object (the spectrum's extraction centre).  `arc_v1` is EUC15's
procedure (euc14.truth_arc) with vectorised offsets; `arc_find` with other options gives the candidates compared on
image evidence before the freeze (euc16_finder_dev.py).  Nothing here reads a spectrum.
"""
import math
import numpy as np
from scipy.ndimage import gaussian_filter

PIX = 0.1                     # arcsec per VIS mosaic pixel
SMOOTH = 1.5                  # Gaussian smoothing of the residual, pixels (as EUC14 / EUC15)
ANN_W = 0.1                   # width of the model annuli, arcsec (as EUC14 / EUC15)
ANN = (0.5, 1.5)              # search annulus in units of theta_E (as EUC14 / EUC15)
CEN_R = 0.3                   # centroid radius about the peak, arcsec (as EUC14 / EUC15)
# --- added by EUC16
CEN_AP, CEN_IT, CEN_MAX = 0.3, 5, 0.5   # light-centre aperture (arcsec), iterations, largest accepted shift (arcsec)
MOM_R = (0.3, 0.5)            # moment aperture: semi-major axis max(0.3 arcsec, 0.5 theta_E)
MOM_IT = 5                    # iterations of the elliptical moment aperture
Q_MIN = 0.3                   # floor on the lens-light axis ratio
SIG_W = 0.2                   # width (arcsec, elliptical radius) of the annuli for the local scatter
SIG_FLOOR = 1.0               # local scatter never below the sky scatter of the smoothed residual (candidates "neg", "mad")
EPS = 0.03                    # frozen: model-mismatch fraction in the noise of the significance map

def offsets(path, ra0, de0):
    """image and per-pixel (east, north) offsets in arcsec from (ra0, de0), tangent plane at (ra0, de0)"""
    from astropy.io import fits
    from astropy.wcs import WCS
    with fits.open(path) as hl:
        h = next(x for x in hl if x.data is not None and x.data.ndim == 2)
        img = np.array(h.data, float); w = WCS(h.header)
    ny, nx = img.shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    ra, de = w.all_pix2world(xx.ravel(), yy.ravel(), 0)
    ra, de, a0, d0 = np.radians(ra), np.radians(de), math.radians(ra0), math.radians(de0)
    cc = np.sin(de) * math.sin(d0) + np.cos(de) * math.cos(d0) * np.cos(ra - a0)
    xi = np.cos(de) * np.sin(ra - a0) / cc
    eta = (np.sin(de) * math.cos(d0) - np.cos(de) * math.sin(d0) * np.cos(ra - a0)) / cc
    E_ = np.degrees(xi).reshape(ny, nx) * 3600.0; N_ = np.degrees(eta).reshape(ny, nx) * 3600.0
    return img, E_, N_

def _median_model(img, good, rad, w):
    model = np.zeros_like(img)
    idx = np.floor(rad / w).astype(int)
    for k in np.unique(idx[good]):
        m = good & (idx == k)
        model[m] = np.median(img[m])
    return model

def _centroid(res, E_, N_, j):
    near = (np.hypot(E_ - E_[j], N_ - N_[j]) <= CEN_R) & (res > 0)
    wgt = res[near]
    return np.array([float(np.sum(E_[near] * wgt) / np.sum(wgt)), float(np.sum(N_[near] * wgt) / np.sum(wgt))])

def arc_v1(img, E_, N_, thE):
    """EUC15: circular median model, brightest smoothed residual in 0.5 to 1.5 theta_E, centroid within 0.3 arcsec"""
    good = np.isfinite(img); R = np.hypot(E_, N_)
    model = _median_model(img, good, R, ANN_W)
    res = gaussian_filter(np.where(good, img - model, 0.0), SMOOTH)
    ann = (R >= ANN[0] * thE) & (R <= ANN[1] * thE) & good
    j = np.unravel_index(int(np.argmax(np.where(ann, res, -np.inf))), res.shape)
    return _centroid(res, E_, N_, j)

def lens_centre(img, good, E_, N_, thE):
    """flux-weighted centroid of positive pixels within CEN_AP of the current centre, iterated CEN_IT times from the
    lens object"""
    c = np.zeros(2)
    for _ in range(CEN_IT):
        m = good & (np.hypot(E_ - c[0], N_ - c[1]) <= CEN_AP) & (img > 0)
        if m.sum() < 5: return np.zeros(2)
        w = img[m]; c = np.array([np.sum(E_[m] * w) / w.sum(), np.sum(N_[m] * w) / w.sum()])
    return c if np.hypot(*c) <= CEN_MAX else np.zeros(2)

def lens_shape(img, good, E_, N_, thE):
    """axis ratio q and major-axis angle th (radians from east towards north) of the lens light about the current
    origin: flux-weighted second moments of positive pixels inside an elliptical aperture of semi-major axis
    max(0.3, 0.5 theta_E) arcsec, iterated MOM_IT times from a circle"""
    a = max(MOM_R[0], MOM_R[1] * thE); q, th = 1.0, 0.0
    for _ in range(MOM_IT):
        c, s = math.cos(th), math.sin(th)
        x = E_ * c + N_ * s; y = -E_ * s + N_ * c
        m = good & (np.hypot(x, y / q) <= a) & (img > 0)
        if m.sum() < 5: return 1.0, 0.0
        w = img[m]; ex, ny_ = E_[m], N_[m]
        mxx = np.sum(w * ex * ex) / w.sum(); myy = np.sum(w * ny_ * ny_) / w.sum(); mxy = np.sum(w * ex * ny_) / w.sum()
        tr = mxx + myy; dt = math.sqrt(max((mxx - myy) ** 2 / 4.0 + mxy * mxy, 0.0))
        l1, l2 = tr / 2.0 + dt, max(tr / 2.0 - dt, 1e-12)
        q = max(Q_MIN, math.sqrt(l2 / l1)); th = 0.5 * math.atan2(2.0 * mxy, mxx - myy)
    return q, th

def ell_radius(E_, N_, q, th):
    c, s = math.cos(th), math.sin(th)
    x = E_ * c + N_ * s; y = -E_ * s + N_ * c
    return np.hypot(x * math.sqrt(q), y / math.sqrt(q))            # circularised radius: area-preserving

def arc_find(img, E_, N_, thE, recentre=True, ellip=True, norm="model", info=False, eps=EPS):
    """lens-light model about the light centre (recentre) with elliptical annuli (ellip); smoothed residual; optionally
    divided by a noise (norm: None; "model" = sqrt(sky^2 + (eps x smoothed |lens model|)^2), sky = robust scatter of the
    smoothed residual over the box; "mad" / "neg" = robust scatter of the smoothed residual in its own annulus of
    elliptical radius, from all / from the negative residuals, never below the sky scatter); the peak in
    0.5 to 1.5 theta_E about the lens object; centroid of positive smoothed residual within 0.3 arcsec of it.  The arc
    is returned as an offset from the lens object (the extraction centre)."""
    good = np.isfinite(img) & (img != 0); R = np.hypot(E_, N_)
    c0 = lens_centre(img, good, E_, N_, thE) if recentre else np.zeros(2)
    e, n = E_ - c0[0], N_ - c0[1]
    q, th = lens_shape(img, good, e, n, thE) if ellip else (1.0, 0.0)
    rho = ell_radius(e, n, q, th)
    model = _median_model(img, good, rho, ANN_W)
    res = gaussian_filter(np.where(good, img - model, 0.0), SMOOTH)
    sig = res
    if norm:
        sky = 1.4826 * np.median(np.abs(res[good] - np.median(res[good])))
        loc = np.full_like(img, sky)
        if norm == "model": loc = np.sqrt(sky ** 2 + (eps * gaussian_filter(np.abs(model), SMOOTH)) ** 2)
        idx = np.floor(rho / SIG_W).astype(int)
        for k in (np.unique(idx[good]) if norm != "model" else []):
            m = good & (idx == k)
            if norm == "mad": s_ = 1.4826 * float(np.median(np.abs(res[m] - np.median(res[m]))))
            else:
                ng = res[m][res[m] < 0]
                s_ = 1.4826 * float(np.median(-ng)) if ng.size >= 5 else sky
            loc[m] = max(SIG_FLOOR * sky, s_)
        sig = res / np.maximum(loc, 1e-30)
    ann = (R >= ANN[0] * thE) & (R <= ANN[1] * thE) & good
    j = np.unravel_index(int(np.argmax(np.where(ann, sig, -np.inf))), res.shape)
    a = _centroid(res, E_, N_, j)
    if info: return a, dict(q=q, th=th, c0=c0, peak=float(sig[j]))
    return a


def arc_euc16(img, E_, N_, thE):
    """THE FROZEN FINDER (FROZEN_CRITERIA.md section 2): recentred, elliptical, noise model with eps = 0.03"""
    return arc_find(img, E_, N_, thE, recentre=True, ellip=True, norm="model", eps=EPS)
