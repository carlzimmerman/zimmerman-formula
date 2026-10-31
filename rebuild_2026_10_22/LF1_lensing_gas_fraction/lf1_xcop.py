#!/usr/bin/env python3
"""LF1 bracket, labelled, never graded: X-COP's hydrostatic baryon share in 3D, and eRASS1's own catalogue share. A same-cylinder read isn't possible without X-COP's mass outside its profile. kappa = 1/2 FITTED; not theory closed."""
import glob, os
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); F = sorted(glob.glob(os.path.join(REPO, "real_research", "data", "xcop", "*", "*_fgas_profile.fits"))); rows = []
print("files", len(F)); h0 = fits.open(F[0])[1]; print("columns", h0.columns.names)
for f in F:
    h = fits.open(f)[1]; d = h.data; x = np.asarray(d["RADIUS"], float); fg = np.asarray(d["FGAS"], float) if "FGAS" in h.columns.names else None
    if fg is None: continue
    ok = fg > 0; rows.append((os.path.basename(f).split("_")[0], float(np.interp(1, x[ok], fg[ok])), float(np.interp(1.5, x[ok], fg[ok])), float(x.max())))
for r in rows: print(r)
a = np.array([r[1] for r in rows]); b = np.array([r[2] for r in rows if r[3] >= 1.5])
for fs in (0.034, 0.0615): print(f"f* {fs}: X-COP f_b at R500 median {np.median(a) * (1 + fs):.4f}, at 1.5 R500 median {np.median(b) * (1 + fs):.4f}; log Y {np.log10(np.median(a) * (1 + fs) / 0.15945):+.3f}, {np.log10(np.median(b) * (1 + fs) / 0.15945):+.3f}")
