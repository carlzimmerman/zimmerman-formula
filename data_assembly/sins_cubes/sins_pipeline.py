#!/usr/bin/env python3
"""Rotation-curve pipeline for the SINS/zC-SINF AO Halpha cubes, exactly as fixed in FROZEN_CRITERIA_2026-09-30.md (commit f9290e8d4).
process(data, noise, wave_um, z, sigma_tot, sini, fwhm_arcsec, snr_cut) -> dict with the accepted velocity map, systemic velocity, kinematic PA (cube frame) and major-axis profile."""
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit
C = 299792.458; PIX = 0.05
LHA, LN2, LN1 = 0.6564614, 0.6585271, 0.6549860      # vacuum wavelengths in micron (Halpha, [NII]6583, [NII]6548)
def model(lam, v, sig, aha, an2, c0, c1, lam_ref):
    out = c0 + c1 * (lam - lam_ref)
    for l0, a in ((LHA, aha), (LN2, an2), (LN1, an2 / 3.0)):
        lc = l0 * (1 + z_glob[0]) * (1 + v / C); s = lc * sig / C
        out = out + a * np.exp(-0.5 * ((lam - lc) / s) ** 2)
    return out
z_glob = [0.0]
def smooth_cube(data, noise, fwhm):
    s = fwhm / 2.3548 / PIX; d = np.empty_like(data); 
    for k in range(data.shape[0]): d[k] = gaussian_filter(np.nan_to_num(data[k]), s)
    # noise reduction factor for independent pixels: sqrt(sum kernel^2) of a 2D Gaussian with sigma s (pixels)
    f = 1.0 / (2 * np.sqrt(np.pi) * s) if s > 0.3 else 1.0
    n = np.nan_to_num(noise, nan=np.nanmedian(noise)) * f
    return d, n
def fit_spaxel(lam, spec, err, z, sig0, v0=0.0):
    z_glob[0] = z; lref = LHA * (1 + z)
    win = np.abs((lam / lref - 1) * C) < 1800
    l, y, e = lam[win], spec[win], err[win]; e = np.where(e > 0, e, np.nanmedian(e))
    # numerical scaling only: flux in units of the median error, wavelength slope per 0.01 micron (the data are ~1e-19 W/m2/um)
    sc = float(np.nanmedian(e)); y = y / sc; e = e / sc
    off = np.abs((l / lref - 1) * C) > 1200
    cont = np.nanmedian(y[off]) if np.any(off) else np.nanmedian(y)
    amp = np.nanmax(y) - cont
    if not np.isfinite(amp) or amp <= 0: return None
    k = np.nanargmax(np.convolve(y - cont, np.ones(5) / 5, mode="same")); vstart = ((l[k] / lref) - 1) * C
    p0 = [vstart, max(sig0, 60.0), amp * 0.5, amp * 0.2, cont, 0.0]
    f_ = lambda x, v, s, a, an, c0, c1: model(x, v, s, a, an, c0, c1 * 100.0, lref)
    try:
        p, cov = curve_fit(f_, l, y, p0=p0, sigma=e, absolute_sigma=True, maxfev=4000, x_scale=[50, 30, max(amp, 1), max(amp, 1), max(abs(cont), 1), 1.0],
                           bounds=([-1500, 15, 0, 0, -np.inf, -np.inf], [1500, 600, np.inf, np.inf, np.inf, np.inf]))
    except Exception: return None
    p = np.array(p); 
    er = np.sqrt(np.diag(cov))
    if not np.all(np.isfinite(er)): return None
    return dict(v=p[0], sig=p[1], aha=p[2] * sc, an=p[3] * sc, ev=er[0], esig=er[1], eaha=er[2] * sc)
def process(data, noise, wave, z, sigma_tot, sini, fwhm=0.15, snr_cut=5.0, centre=None, strip=0.15, step=0.15):
    d, n = smooth_cube(data, noise, fwhm); ny, nx = d.shape[1:]
    if centre is None: centre = (nx / 2.0, ny / 2.0)
    # spaxels with a preliminary peak signal to noise above 2.5 are fitted
    lref = LHA * (1 + z); win = np.abs((wave / lref - 1) * C) < 1800
    V = np.full((ny, nx), np.nan); EV = V.copy(); SIG = V.copy(); SN = V.copy()
    for j in range(ny):
        for i in range(nx):
            sp = d[win, j, i]; er = n[win, j, i]
            if not np.any(np.isfinite(sp)) or np.nanmax(sp - np.nanmedian(sp)) < 2.5 * np.nanmedian(er): continue
            f = fit_spaxel(wave, d[:, j, i], n[:, j, i], z, sigma_tot)
            if f is None: continue
            SN[j, i] = f["aha"] / f["eaha"] if f["eaha"] > 0 else np.nan; V[j, i] = f["v"]; EV[j, i] = f["ev"]; SIG[j, i] = f["sig"]
    acc = (SN > snr_cut) & (SIG > 20) & (SIG < 400) & (EV < 40)
    out = dict(V=V, EV=EV, SIG=SIG, SN=SN, acc=acc, nacc=int(acc.sum()))
    if acc.sum() < 5: out["status"] = "too few accepted spaxels"; return out
    # systemic velocity: fit of the integrated spectrum of the accepted spaxels
    mask = acc[None, :, :]; spec = np.nansum(np.where(mask, d, 0), axis=(1, 2)); err = np.sqrt(np.nansum(np.where(mask, n ** 2, 0), axis=(1, 2)))
    g = fit_spaxel(wave, spec, err, z, sigma_tot); vsys = g["v"] if g else float(np.nanmedian(V[acc]))
    Vr = V - vsys
    # kinematic PA: weighted plane fit of the accepted velocity map; cube frame: dx along +x (columns), dy along +y (rows)
    jj, ii = np.where(acc); x = (ii - centre[0]) * PIX; y = (jj - centre[1]) * PIX; w = 1 / np.maximum(EV[acc], 3.0) ** 2
    A = np.column_stack([np.ones_like(x), x, y]); W = np.sqrt(w); coef = np.linalg.lstsq(A * W[:, None], Vr[acc] * W, rcond=None)[0]
    theta = np.degrees(np.arctan2(-coef[1], coef[2])) % 360        # angle of the gradient from +y toward -x (PA-like in the cube frame)
    th = np.radians(theta); ex, ey = -np.sin(th), np.cos(th)       # unit vector of the gradient in (x, y)
    s_par = x * ex + y * ey; s_perp = -x * ey + y * ex
    # profile
    sel = np.abs(s_perp) < strip; edges = np.arange(-np.ceil(np.max(np.abs(s_par)) / step) * step - step / 2, np.ceil(np.max(np.abs(s_par)) / step) * step + step, step)
    prof = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = sel & (s_par >= a) & (s_par < b)
        if m.sum() == 0: continue
        ww = 1 / np.maximum(EV[acc][m], 3.0) ** 2; v = np.sum(ww * Vr[acc][m]) / np.sum(ww); ev = np.sqrt(1 / np.sum(ww))
        prof.append(dict(R_arcsec=float((a + b) / 2), n=int(m.sum()), Vlos=float(v), eVlos=float(ev), sigma=float(np.mean(SIG[acc][m]))))
    out.update(status="ok", vsys=float(vsys), theta_cube=float(theta), grad=float(np.hypot(coef[1], coef[2])), profile=prof, sini=sini)
    return out
