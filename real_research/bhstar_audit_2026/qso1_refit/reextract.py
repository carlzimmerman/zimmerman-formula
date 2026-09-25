"""PSF-consistent re-extraction of the QSO1 narrow/extended H-alpha cube from the FULL cube (Zenodo 19402518).

Method (spatial deblending, no spectral-shape prior): every unresolved component (the BLR, the absorber in front of it,
the AGN continuum) has the SAME spatial profile, the PSF P(x), measured from the broad-line wings (psf_from_blr.py).
In every channel v the continuum-subtracted cube is fitted as
        d(x, v) = s(v) P(x) + e(v) Q_R(x) + noise,        Q_R = P (x) exp(-r/R)   (an extended nuisance shape)
by weighted linear least squares; R is chosen once by minimum total chi^2 over the line channels.  The narrow/extended
cube is  n(x, v) = d(x, v) - s(v) P(x)  -- nothing extended is ever subtracted, so it is PSF-consistent by construction.
Irreducible limit (reported, not hidden): a genuinely UNRESOLVED narrow nucleus is indistinguishable from the point
source and goes into s(v); its size is measured as the excess of s(v) over a smooth broad profile at |v| < 150 km/s.

Output: qso1_narrow_reextracted.fits (gitignored), same 35x35 cutout and spectral axis as the published narrow cube, so
model.load(path) reads it unchanged.  PSF_KIND = "empirical" (smoothed broad-wing image) or "gauss" (fitted Gaussian).
"""
import os, json
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from scipy.signal import fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(REPO, "real_research", "data", "qso1")
FULL = os.path.join(DATA, "output_cube_mMSA_manMask_0.02px_cgs_s3d.fits")
NARROW = os.path.join(DATA, "Halpha_nr_only_cube_02px.fits")
C = 299792.458
LAM0 = 0.6564614 * (1 + 7.0367)
OY, OX, NS = 100, 99, 35            # the published cutout's offset in the full grid (psf_from_blr.py) and size
PAD = 12                            # decompose on a padded region, crop to the cutout


def build(psf_kind="empirical", out_name="qso1_narrow_reextracted.fits", verbose=True, smooth_template=True,
          absorber=True):
    psf = json.load(open(os.path.join(HERE, "psf_from_blr.json")))
    h = fits.open(FULL, memmap=True)
    sci, err = h["SCI"].data, h["ERR"].data
    hd = h["SCI"].header
    v = (hd["CRVAL3"] + np.arange(hd["NAXIS3"]) * hd["CDELT3"]) / LAM0 * C - C
    y0, y1, x0, x1 = OY - PAD, OY + NS + PAD, OX - PAD, OX + NS + PAD
    side = ((v > -7000) & (v < -4000)) | ((v > 3500) & (v < 4800))
    sl = np.where((v > -7500) & (v < 5000))[0]; lo, hi = sl.min(), sl.max() + 1
    D = np.array(sci[lo:hi, y0:y1, x0:x1], dtype=float); E = np.array(err[lo:hi, y0:y1, x0:x1], dtype=float)
    vv = v[lo:hi]
    cont = np.nanmedian(D[side[lo:hi]], axis=0)
    d = D - cont[None]
    good = np.isfinite(d) & np.isfinite(E) & (E > 0)
    # ---- the PSF image P(x) on the padded grid
    ny, nx = d.shape[1:]
    yy, xx = np.mgrid[0:ny, 0:nx]
    yc, xc = psf["broad_peak_yx"][0] - y0, psf["broad_peak_yx"][1] - x0
    nii = (np.abs(vv - 940) > 150) & (np.abs(vv + 730) > 150)
    wing = (np.abs(vv) > 650) & (np.abs(vv) < 2500) & nii
    if psf_kind == "empirical":
        P = np.nansum(np.where(good[wing], d[wing], 0.0), axis=0)
        P = gaussian_filter(P, 1.0)
        P[np.hypot(yy - yc, xx - xc) > 15] = 0.0
        P = np.clip(P, 0, None)
    else:
        pb = psf["psf_broad"]
        ct, st = np.cos(pb["th_rad"]), np.sin(pb["th_rad"])
        xr = (xx - xc) * ct + (yy - yc) * st; yr = -(xx - xc) * st + (yy - yc) * ct
        P = np.exp(-0.5 * ((xr / pb["sx_px"]) ** 2 + (yr / pb["sy_px"]) ** 2))
    P /= P.sum()

    def Q_of(Rpx):
        k = np.exp(-np.hypot(yy - yc, xx - xc) / max(Rpx, 0.5))
        Q = fftconvolve(k, P, mode="same"); return Q / Q.sum()

    line = np.abs(vv) < 1500

    def solve(Q):
        s = np.zeros(len(vv)); e = np.zeros(len(vv)); chi = 0.0; vs = np.full(len(vv), np.inf)
        for c in np.where(line)[0]:
            w = np.where(good[c], 1 / E[c] ** 2, 0.0)
            A = np.array([[np.sum(w * P * P), np.sum(w * P * Q)], [np.sum(w * P * Q), np.sum(w * Q * Q)]])
            b = np.array([np.sum(w * P * np.nan_to_num(d[c])), np.sum(w * Q * np.nan_to_num(d[c]))])
            s[c], e[c] = np.linalg.solve(A, b)
            vs[c] = np.linalg.inv(A)[0, 0]
            r = np.nan_to_num(d[c]) - s[c] * P - e[c] * Q
            chi += float(np.sum(w * r * r))
        solve.var = vs
        return s, e, chi

    grid = [1, 2, 3, 5, 8, 12, 18, 25]
    chis = {}
    for R in grid:
        chis[R] = solve(Q_of(R))[2]
    Rbest = min(chis, key=chis.get)
    Q = Q_of(Rbest)
    s, e, chi = solve(Q)
    # point-source spectrum at all channels within +/-3000 (s from wings beyond the line window by projection on P)
    for c in np.where((np.abs(vv) >= 1500) & (np.abs(vv) < 3000))[0]:
        w = np.where(good[c], 1 / E[c] ** 2, 0.0)
        s[c] = np.sum(w * P * np.nan_to_num(d[c])) / np.sum(w * P * P)
    s_var = solve.var
    if smooth_template:
        # smooth point-source template: two Gaussians (broad + intermediate), times the literature absorber applied to the
        # point source incl. its continuum c0 (continuum already subtracted per spaxel => s = A(B + c0) - c0)
        from scipy.optimize import least_squares
        wv = np.isfinite(s_var) & (np.abs(vv) < 1500)
        c0 = float(np.nansum(np.where(np.isfinite(cont), cont, 0) * P) / np.sum(P * P) * 1.0)
        def tmpl(p, x):
            a1, m1, s1, a2, m2, s2 = p
            B = a1 * np.exp(-0.5 * ((x - m1) / s1) ** 2) + a2 * np.exp(-0.5 * ((x - m2) / s2) ** 2)
            if absorber:
                tau = 1.9 * np.exp(-((x + 36.0) / 100.0) ** 2)
                Aabs = 1 - 0.55 * (1 - np.exp(-tau))
                return Aabs * (B + c0) - c0
            return B
        p0 = [np.nanmax(s[wv]) * 0.6, 0, 350, np.nanmax(s[wv]) * 0.3, 0, 900]    # both components forced BROAD (sigma >= 250)
        fitr = least_squares(lambda p: (tmpl(p, vv[wv]) - s[wv]) / np.sqrt(s_var[wv]), p0,
                             bounds=([0, -600, 250, 0, -1000, 400], [np.inf, 600, 1500, np.inf, 1000, 3000]))
        s_fit = tmpl(fitr.x, vv)
        s_fit[np.abs(vv) >= 3000] = 0.0
        tmpl_par = list(map(float, fitr.x)); red_chi2 = float(np.sum(fitr.fun ** 2) / max(1, wv.sum() - 6))
        s_use = s_fit
    else:
        s_use, tmpl_par, red_chi2, c0 = s, None, None, None
    n = d - s_use[:, None, None] * P[None]
    # unresolved-narrow-nucleus diagnostic: excess of s(v) over a smooth (median-filtered, 7 channels) broad profile
    from scipy.ndimage import median_filter
    smooth = median_filter(s, size=9)
    core = np.abs(vv) < 150
    unres = float(np.sum((s - smooth)[core]))
    ext_core = float(np.sum(e[core]))
    # write the cutout, full spectral axis (outside the slab: data - continuum, i.e. real noise)
    hn = fits.open(NARROW)
    out_sci = np.full(hn["SCI"].data.shape, np.nan)
    out_err = np.full(hn["ERR"].data.shape, np.nan)
    cy0, cx0 = PAD, PAD
    full_cont = cont[cy0:cy0 + NS, cx0:cx0 + NS]
    # line-free channels for the noise model: read the full-cube cutout minus its continuum
    allsci = np.array(sci[:, OY:OY + NS, OX:OX + NS], dtype=float)
    out_sci[:] = allsci - full_cont[None]
    out_err[:] = np.array(err[:, OY:OY + NS, OX:OX + NS], dtype=float)
    out_sci[lo:hi] = n[:, cy0:cy0 + NS, cx0:cx0 + NS]
    hdu = fits.HDUList([fits.PrimaryHDU(), fits.ImageHDU(out_sci, header=hn["SCI"].header, name="SCI"),
                        fits.ImageHDU(out_err, header=hn["ERR"].header, name="ERR")])
    path = os.path.join(DATA, out_name)
    hdu.writeto(path, overwrite=True)
    res = {"psf_kind": psf_kind, "smooth_template": smooth_template, "absorber": absorber, "template_params": tmpl_par,
           "template_red_chi2": red_chi2, "c0_point_continuum": c0, "R_best_px": Rbest, "chi2_by_R": chis, "unresolved_nucleus_excess": unres,
           "extended_core_flux": ext_core, "s_v": dict(zip(map(lambda x: round(float(x), 1), vv[np.abs(vv) < 1000]),
                                                         map(float, s[np.abs(vv) < 1000]))), "out": out_name}
    if verbose:
        print(f"[{psf_kind} smooth={smooth_template} abs={absorber}] template {None if tmpl_par is None else [round(x,1) for x in tmpl_par]} "
              f"red.chi2 {red_chi2}")
        print(f"[{psf_kind}] R_best = {Rbest} px; unresolved-nucleus excess in s(v) (|v|<150) = {unres:.3f} vs extended "
              f"component flux there {ext_core:.3f}  -> wrote {out_name}")
    return res


if __name__ == "__main__":
    out = {}
    # the bracket (the unresolved-nucleus degeneracy cannot be broken without a prior):
    out["V1_raw_s"] = build("empirical", "qso1_narrow_V1_raws.fits", smooth_template=False)       # all unresolved removed
    out["V2_smooth_noabs"] = build("empirical", "qso1_narrow_V2_smooth_noabs.fits", absorber=False)  # nucleus kept
    out["V3_smooth_abs"] = build("empirical", "qso1_narrow_V3_smooth_abs.fits", absorber=True)       # nucleus kept, absorber
    json.dump(out, open(os.path.join(HERE, "reextract.json"), "w"), indent=1)
