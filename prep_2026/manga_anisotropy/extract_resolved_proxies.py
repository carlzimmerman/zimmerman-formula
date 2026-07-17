#!/usr/bin/env python3
"""
extract_resolved_proxies.py -- resolved anisotropy PROXIES from DR17 DAP MAPS files
(HYB10-MILESHC-MASTARSSP), for the frozen maps_subsample.csv galaxies.

Adapts the proven mmu_scout/pilot_extract.py anisotropy_proxy() machinery from the MMU
parquet layout to the native DR17 MAPS FITS layout:
  STELLAR_SIGMA (+_IVAR/_MASK), STELLAR_SIGMACORR (channel 0), STELLAR_VEL (+_IVAR/_MASK),
  SPX_ELLCOO (ch 0 R arcsec, 1 R/Re, 2 R h/kpc, 3 azimuth deg), SPX_MFLUX.

FROZEN proxies (FROZEN.md sec.3, frozen 2026-07-17T00:21:52Z before any download):
  P1  sigma_maj/sigma_min in the 0.5-1.0 Re annulus (|cos phi|>=0.87 major wedge,
      |cos phi|<=0.5 minor wedge, >=8 valid spaxels each), sigmacorr-corrected,
      SPX_MFLUX flux-weighted.
  P2  d ln sigma_c / d ln R over 0.5<=R/Re<=1.5, unweighted OLS in log-log, >=20 spaxels.
Plus resolved sigma_e (<=1 Re, flux-weighted) and resolved V/sigma (<=1 Re) as
cross-checks of the DAPall-level catalog values.

THE PROXIES ARE NOT beta -- LOS signatures contaminated by inclination/shape/rotation
residuals/M-L gradients (FROZEN.md sec.3 caveat). No regression is run here (firewall).

Output: resolved_proxies.csv. exit 0 if >=80% of the present MAPS files extract cleanly.
"""
import os, sys, glob, math
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(HERE, "data", "maps")


def masked(hdul, name):
    """Return (data, valid) applying the DAP bitmask + ivar>0."""
    d = hdul[name].data.astype(float)
    m = hdul[name + "_MASK"].data if (name + "_MASK") in [h.name for h in hdul] else 0
    iv = hdul[name + "_IVAR"].data.astype(float) if (name + "_IVAR") in [h.name for h in hdul] else None
    valid = np.isfinite(d) & (np.asarray(m) == 0)
    if iv is not None:
        valid &= np.isfinite(iv) & (iv > 0)
    return d, valid


def extract_one(path):
    with fits.open(path) as h:
        names = [x.name for x in h]
        sig, vsig_ok = masked(h, "STELLAR_SIGMA")
        vel, vvel_ok = masked(h, "STELLAR_VEL")
        corr = h["STELLAR_SIGMACORR"].data
        corr = corr[0] if corr.ndim == 3 else corr        # channel 0 = fit correction
        ell = h["SPX_ELLCOO"].data                        # (4, ny, nx)
        r_re, phi = ell[1], ell[3]
        w = h["SPX_MFLUX"].data.astype(float) if "SPX_MFLUX" in names else np.ones_like(sig)
        plateifu = h[0].header.get("PLATEIFU", os.path.basename(path).split("-MAPS")[0].replace("manga-", ""))

    # sigmacorr quadrature correction (proven mmu_scout recipe)
    sig_c = np.sqrt(np.clip(sig ** 2 - np.nan_to_num(corr) ** 2, 0, None))
    valid = vsig_ok & np.isfinite(sig_c) & (sig_c > 0) & np.isfinite(r_re) & np.isfinite(phi)
    if valid.sum() < 50:
        return dict(plateifu=plateifu, ok=0, n_spaxels=int(valid.sum()))
    ww = np.where(np.isfinite(w) & (w > 0), w, 0.0)

    # resolved sigma_e (<=1 Re, flux-weighted)
    inRe = valid & (r_re <= 1.0)
    sig_e = float(np.average(sig_c[inRe], weights=ww[inRe])) if inRe.sum() > 10 else np.nan

    # resolved V/sigma (<=1 Re)
    vsig = np.nan
    vok = vvel_ok & inRe
    if vok.sum() > 10:
        wv = ww.copy(); wv[~vvel_ok] = 0.0
        vsys = float(np.average(vel[wv > 0], weights=wv[wv > 0])) if (wv > 0).sum() > 10 else 0.0
        num = np.sum(ww[vok] * (vel[vok] - vsys) ** 2)
        den = np.sum(ww[vok] * sig_c[vok] ** 2)
        vsig = float(math.sqrt(num / den)) if den > 0 else np.nan

    # P1: major/minor LOS-sigma ratio, 0.5-1.0 Re annulus (frozen wedges)
    cphi = np.cos(np.radians(phi))
    ann = valid & (r_re >= 0.5) & (r_re <= 1.0)
    maj = ann & (np.abs(cphi) >= 0.87)
    mnr = ann & (np.abs(cphi) <= 0.5)
    sig_maj = float(np.average(sig_c[maj], weights=np.clip(ww[maj], 0, None))) if maj.sum() >= 8 else np.nan
    sig_min = float(np.average(sig_c[mnr], weights=np.clip(ww[mnr], 0, None))) if mnr.sum() >= 8 else np.nan
    p1 = sig_maj / sig_min if (np.isfinite(sig_maj) and np.isfinite(sig_min) and sig_min > 0) else np.nan

    # P2: dln sigma / dln R over 0.5-1.5 Re (frozen window), unweighted OLS
    win = valid & (r_re >= 0.5) & (r_re <= 1.5) & (sig_c > 1.0)
    p2, n_win = np.nan, int(win.sum())
    if n_win >= 20:
        b = np.polyfit(np.log10(r_re[win]), np.log10(sig_c[win]), 1)
        p2 = float(b[0])

    return dict(plateifu=plateifu, ok=1, n_spaxels=int(valid.sum()),
                sigma_e_resolved=sig_e, vsig_resolved=vsig,
                sigma_maj=sig_maj, sigma_min=sig_min, P1_sigmaj_over_sigmin=p1,
                P2_dlnsig_dlnR=p2, n_P2_spaxels=n_win,
                n_maj=int(maj.sum()), n_min=int(mnr.sum()))


def main():
    files = sorted(glob.glob(os.path.join(MAPS_DIR, "*.fits.gz")))
    if not files:
        print("FATAL: no MAPS files in", MAPS_DIR); return 1
    print(f"extracting frozen resolved proxies from {len(files)} MAPS files "
          f"(P1 wedge ratio, P2 slope in 0.5-1.5 Re; NOT beta -- see FROZEN.md sec.3)")
    rows, fails = [], []
    for f in files:
        try:
            r = extract_one(f)
        except Exception as e:
            r = dict(plateifu=os.path.basename(f), ok=0, n_spaxels=-1)
            print(f"  ERROR {os.path.basename(f)}: {e}")
        rows.append(r)
        if not r["ok"]:
            fails.append(r["plateifu"])

    cols = ["plateifu", "ok", "n_spaxels", "sigma_e_resolved", "vsig_resolved",
            "sigma_maj", "sigma_min", "P1_sigmaj_over_sigmin",
            "P2_dlnsig_dlnR", "n_P2_spaxels", "n_maj", "n_min"]
    out = os.path.join(HERE, "resolved_proxies.csv")
    with open(out, "w") as fo:
        fo.write(",".join(cols) + "\n")
        for r in rows:
            fo.write(",".join(f"{r.get(c, float('nan')):.5g}" if isinstance(r.get(c), float)
                              else str(r.get(c, "")) for c in cols) + "\n")

    okr = [r for r in rows if r["ok"]]
    p1 = np.array([r["P1_sigmaj_over_sigmin"] for r in okr])
    p2 = np.array([r["P2_dlnsig_dlnR"] for r in okr])
    print(f"wrote {out}: {len(okr)}/{len(rows)} extracted cleanly"
          + (f"  (failed: {fails})" if fails else ""))
    print(f"  P1 sig_maj/sig_min: median {np.nanmedian(p1):.3f}, 16-84% "
          f"[{np.nanpercentile(p1,16):.3f}, {np.nanpercentile(p1,84):.3f}], "
          f"finite {np.isfinite(p1).sum()}/{len(okr)}")
    print(f"  P2 dlnsig/dlnR:     median {np.nanmedian(p2):+.3f}, 16-84% "
          f"[{np.nanpercentile(p2,16):+.3f}, {np.nanpercentile(p2,84):+.3f}], "
          f"finite {np.isfinite(p2).sum()}/{len(okr)}")
    print("  (distribution stats only; the delta-vs-proxy regression is NOT run here -- firewall)")
    return 0 if len(okr) >= 0.8 * len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
