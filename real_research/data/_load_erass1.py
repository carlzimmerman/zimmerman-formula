"""Shared loader for the eRASS1 primary cluster catalog -> clean per-cluster arrays.

DATA (not committed -- 50 MB; download once):
    curl -sL -o erass1cl_primary.fits.tgz \\
      https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/Catalogues_dr1/BulbulE_DR1/erass1cl_primary_v3.2.fits.tgz
    tar xzf erass1cl_primary.fits.tgz      # -> erass1cl_primary_v3.2.fits
Catalog: Bulbul et al. 2024 (A&A 685, A106), eROSITA/SRG eRASS1, 12,247 clusters, z=0.003-1.323.
Columns used: BEST_Z, M500 (1e13 Msun, WL-calibrated), MGAS500 (1e11 Msun), FGAS500, R500 (kpc), KT (keV).
"""
import os
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(__file__)
FITS = os.path.join(HERE, "erass1cl_primary_v3.2.fits")


def _to_f(v):
    try:
        if isinstance(v, bytes):
            v = v.decode().strip()
        if isinstance(v, str) and v.strip() == "":
            return np.nan
        return float(v)
    except Exception:
        return np.nan


def load_raw():
    d = fits.open(FITS)[1].data
    col = lambda c: np.array([_to_f(v) for v in d[c]], dtype=float)
    return dict(z=col("BEST_Z"), zerr=col("BEST_ZERR"), M500=col("M500"),
               M500_L=col("M500_L"), M500_H=col("M500_H"),
               Mgas=col("MGAS500"), fgas=col("FGAS500"), R500=col("R500"), kt=col("KT"))


def load_clean(zmax=1.0, fgas_lo=0.01, fgas_hi=0.30, fstar=0.2):
    """Clean sample + accelerations at R500. fstar = stellar/gas mass ratio (baseline 0.2)."""
    r = load_raw()
    z, M500, Mgas, fgas, R500 = r["z"], r["M500"], r["Mgas"], r["fgas"], r["R500"]
    ok = ((z > 0) & (z < zmax) & np.isfinite(z) & (M500 > 0) & (Mgas > 0) & (R500 > 0)
          & (fgas > fgas_lo) & (fgas < fgas_hi))
    Msun, kpc, G = 1.989e30, 3.086e19, 6.674e-11
    M500_kg = M500[ok]*1e13*Msun
    Mbar_kg = (1+fstar)*Mgas[ok]*1e11*Msun
    R_m = R500[ok]*kpc
    gobs = G*M500_kg/R_m**2
    gbar = G*Mbar_kg/R_m**2
    # fractional 1-sigma error on M500 (-> on gobs) from the asymmetric limits
    eM = (r["M500_H"][ok]-r["M500_L"][ok])/(2*np.maximum(M500[ok], 1e-6))
    return dict(z=z[ok], M500=M500[ok], Mgas=Mgas[ok], fgas=fgas[ok], R500=R500[ok],
                gobs=gobs, gbar=gbar, eM=np.clip(np.nan_to_num(eM, nan=0.25), 0.05, 1.0),
                N=int(ok.sum()))
