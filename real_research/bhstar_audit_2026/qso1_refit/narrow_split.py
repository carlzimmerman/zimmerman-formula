"""Spectral narrow/intermediate split of the PSF-consistent re-extracted QSO1 cube (V2), and the fair spectroastrometry test.

1. Fit the integrated V2 spectrum (r <= 10 px) with a narrow + an intermediate Gaussian (LSF included) -> global shapes.
2. Per spaxel, weighted LINEAR least squares on [G_n(v), dG_n/dv, G_i(v)]: the narrow line with a free small velocity
   shift (the derivative term, so narrow kinematics are PRESERVED) and the intermediate (outflow) template.
3. Narrow-only cube N = V2 - a_i(x) G_i(v): only the smooth intermediate component is removed.
4. Spectroastrometry: red/blue (|v - v_n| in 12-88 km/s) channel-image centroids within r <= 7 px; the separation's
   uncertainty from REAL line-free noise blocks of the same cube (the per-realisation scatter / sqrt(2), since noise is
   added on top of noisy data), and the |separation| noise floor sigma * sqrt(pi/2).
Compared with the same measurement on the released narrow-only product.
"""
import os, json
import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "qso1")
C = 299792.458
LAM0 = 0.6564614 * (1 + 7.0367)
SIG_LSF = C / 3700 / 2.3548


def load(fn):
    h = fits.open(os.path.join(DATA, fn))
    d = h["SCI"].data.astype(float); e = h["ERR"].data.astype(float); hd = h["SCI"].header
    v = ((hd["CRVAL3"] + np.arange(d.shape[0]) * hd["CDELT3"]) / LAM0 - 1) * C
    return d, e, v


def binned_gauss(v, dv, mu, sig):
    s2 = np.sqrt(2) * np.sqrt(sig ** 2 + SIG_LSF ** 2)
    return 0.5 * (erf((v + dv / 2 - mu) / s2) - erf((v - dv / 2 - mu) / s2))


def centroid(img, yc, xc, r=7):
    yy, xx = np.indices(img.shape)
    w = np.where((np.hypot(yy - yc, xx - xc) <= r) & np.isfinite(img), img, 0.0)
    w = np.clip(w, 0, None); s = w.sum()
    return np.array([np.sum(w * yy) / s, np.sum(w * xx) / s])


def spectroastrometry(d, v, vn, yc, xc, noise_blocks):
    red = (v - vn > 12) & (v - vn < 88); blue = (v - vn < -12) & (v - vn > -88)
    ir, ib = np.nansum(d[red], 0), np.nansum(d[blue], 0)
    sep_vec = centroid(ir, yc, xc) - centroid(ib, yc, xc)
    sep = float(np.hypot(*sep_vec) * 0.02)
    nr, nb = int(red.sum()), int(blue.sum())
    vecs = []
    for blk in noise_blocks:
        if len(blk) < nr + nb:
            continue
        a = centroid(ir + np.nansum(d[blk[:nr]], 0), yc, xc)
        b = centroid(ib + np.nansum(d[blk[nr:nr + nb]], 0), yc, xc)
        vecs.append(a - b)
    vecs = np.array(vecs)
    sig = float(np.mean(np.std(vecs, axis=0)) / np.sqrt(2) * 0.02)     # per-axis 1-sigma of the separation (arcsec)
    return {"sep_arcsec": sep, "sigma_per_axis_arcsec": sig, "noise_floor_arcsec": sig * np.sqrt(np.pi / 2),
            "significance": float(np.hypot(*sep_vec) * 0.02 / sig), "n_noise": len(vecs)}


def main():
    out = {}
    d, e, v = load("qso1_narrow_V2_smooth_noabs.fits")
    dv = float(np.median(np.diff(v)))
    core = np.nansum(d[np.abs(v) < 250], 0); yc, xc = np.unravel_index(np.nanargmax(core), core.shape)
    yy, xx = np.indices(core.shape); ap = np.hypot(yy - yc, xx - xc) <= 10
    win = np.abs(v) < 700
    spec = np.nansum(d[win][:, ap], axis=1); err = np.sqrt(np.nansum(e[win][:, ap] ** 2, axis=1)) * 1.77

    def two(vv, an, mn, sn, ai, mi, si):
        return an * binned_gauss(vv, dv, mn, sn) + ai * binned_gauss(vv, dv, mi, si)
    p, _ = curve_fit(two, v[win], spec, p0=[spec.max(), -10, 30, spec.max() / 2, -30, 200], sigma=err,
                     bounds=([0, -150, 0, 0, -400, 100], [np.inf, 150, 90, np.inf, 400, 500]), maxfev=40000)
    an, mn, sn, ai, mi, si = map(float, p)
    out["global"] = {"narrow": {"mu": mn, "sigma": sn}, "intermediate": {"mu": mi, "sigma": si}, "flux_ratio_i_over_n": ai / an}
    print(f"global: narrow mu {mn:.1f} sigma {sn:.1f} | intermediate mu {mi:.1f} sigma {si:.1f} | flux ratio I/N {ai/an:.2f}")
    Gn = binned_gauss(v, dv, mn, sn); Gi = binned_gauss(v, dv, mi, si)
    Gd = (binned_gauss(v, dv, mn + 5, sn) - binned_gauss(v, dv, mn - 5, sn)) / 10.0
    N = d.copy()
    lw = np.abs(v) < 700
    for y in range(d.shape[1]):
        for x in range(d.shape[2]):
            s_ = d[lw, y, x]; w = 1 / np.where(np.isfinite(e[lw, y, x]) & (e[lw, y, x] > 0), e[lw, y, x], np.inf) ** 2
            if not np.isfinite(s_).all():
                continue
            A = np.vstack([Gn[lw], Gd[lw], Gi[lw]]).T
            coef = np.linalg.lstsq(A * np.sqrt(w)[:, None], s_ * np.sqrt(w), rcond=None)[0]
            N[:, y, x] = d[:, y, x] - coef[2] * Gi
    # real noise: line-free channel blocks of the same cube
    good = np.isfinite(d).all(axis=(1, 2)) & (np.abs(v) > 1500) & (np.abs(v) < 6000)
    idx = np.where(good)[0]
    blocks = [idx[k:k + 8] for k in range(0, len(idx) - 8, 8)]
    for name, cube in (("V2_narrow_split", N), ("V2_with_intermediate", d)):
        r = spectroastrometry(cube, v, mn, yc, xc, blocks)
        out[name] = r
        print(f"{name:22s}: separation {r['sep_arcsec']*1000:.1f} mas, 1-sigma/axis {r['sigma_per_axis_arcsec']*1000:.1f} mas, "
              f"noise floor {r['noise_floor_arcsec']*1000:.1f} mas, significance {r['significance']:.1f} (N_noise {r['n_noise']})")
    dp, ep, vp = load("Halpha_nr_only_cube_02px.fits")
    cp = np.nansum(dp[np.abs(vp) < 250], 0); ycp, xcp = np.unravel_index(np.nanargmax(cp), cp.shape)
    goodp = np.isfinite(dp).all(axis=(1, 2)) & (np.abs(vp) > 1500) & (np.abs(vp) < 6000)
    idxp = np.where(goodp)[0]
    r = spectroastrometry(dp, vp, mn, ycp, xcp, [idxp[k:k + 8] for k in range(0, len(idxp) - 8, 8)])
    out["published_product"] = r
    print(f"{'published_product':22s}: separation {r['sep_arcsec']*1000:.1f} mas, 1-sigma/axis {r['sigma_per_axis_arcsec']*1000:.1f} mas, "
          f"noise floor {r['noise_floor_arcsec']*1000:.1f} mas, significance {r['significance']:.1f}")
    json.dump(out, open(os.path.join(HERE, "narrow_split.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
