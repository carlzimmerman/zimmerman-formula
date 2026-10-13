#!/usr/bin/env python3
"""Export the Part-3 F115W cutout, noise, PSF and A position for the PyAutoLens Part 4 run (criteria c29c55493)."""
import os, sys, json, numpy as np
from astropy.io import fits
os.environ["CFG669_BAND"] = "f115w"
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg669_lensmodel_v3.py")).read().split("# blurring matrix")[0]
g = {"__file__": os.path.join(HERE, "cfg669_lensmodel_v3.py"), "__name__": "x"}
exec(compile(src, "v3", "exec"), g)
OUTD = os.path.join(g["DATA"], "pyautolens_inputs"); os.makedirs(OUTD, exist_ok=True)
D, E, psf, sc = np.flipud(g["D"]), np.flipud(g["E"]), np.flipud(g["psf"]), g["scale"]   # PyAutoLens: row 0 = top
fits.writeto(os.path.join(OUTD, "f115w_data.fits"), D.astype("f8"), overwrite=True)
fits.writeto(os.path.join(OUTD, "f115w_noise.fits"), E.astype("f8"), overwrite=True)
fits.writeto(os.path.join(OUTD, "f115w_psf.fits"), psf.astype("f8"), overwrite=True)
nx, ny, AX, AY = g["nx"], g["ny"], g["AX"], g["AY"]
c = (D.shape[1] - 1) / 2, (D.shape[0] - 1) / 2
meta = dict(pixel_scale=sc, shape=list(D.shape), nucleus_arcsec_yx=[(ny - c[1]) * sc, (nx - c[0]) * sc],
            A_arcsec_yx=[(AY - c[1]) * sc, (AX - c[0]) * sc], pixar_sr=g["pixar"], psf_src=g["psf_src"],
            note="PyAutoLens convention: (y, x) arcsec, origin at the image centre; image row index increases with y here (origin lower)")
json.dump(meta, open(os.path.join(OUTD, "f115w_meta.json"), "w"), indent=1); print(json.dumps(meta, indent=1))
