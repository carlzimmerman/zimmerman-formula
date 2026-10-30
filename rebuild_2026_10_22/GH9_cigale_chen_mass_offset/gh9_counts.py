#!/usr/bin/env python3
"""GH9 post-hoc check (NOT frozen): is the Wisconsin table on Zhang's scale? Compare sky densities with Zhang+24 Table FULL_spec counts on 4010 deg2."""
import os, json
import numpy as np, healpy as hp
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data")
w = fits.open(os.path.join(EXT, "sdss_wisconsin_pca", "wisconsin_pca_bc03-26.fits.gz"), memmap=False)[1].data
m, z, ra, de, wa, lt, sp, e = [np.array(w[n]) for n in ("MSTELLAR_MEDIAN", "Z", "RA", "DEC", "WARNING", "LEGACY_TARGET1", "SPECPRIMARY", "MSTELLAR_ERR")]; del w
q = np.isfinite(m) & (wa == 0) & (e > 0) & (sp == 1) & ((lt & 64) > 0); m, z, ra, de = m[q], z[q], ra[q], de[q]; print("MGS-targeted primaries", int(q.sum()))
NS = 64; pa = hp.nside2pixarea(NS, degrees=True); pix = hp.ang2pix(NS, ra, de, lonlat=True); n = np.bincount(pix, minlength=hp.nside2npix(NS)); 
for cut in (1, 20, 40): print(f"area, pixels with >= {cut} targets: {(n >= cut).sum() * pa:.0f} deg2")
area = float((n >= 20).sum() * pa); BINS = [(10.5, 11, .02, .10, 45248), (11, 11.25, .02, .15, 34046), (11.25, 11.5, .03, .19, 24098), (10, 10.5, .01, .06, 11922)]
RES = {"area": area, "scan": []}; print("area used", round(area))
for s in np.arange(-.35, .151, .05):
    o = []
    for a, b, z0, z1, N in BINS:
        c = ((m + s >= a) & (m + s < b) & (z >= z0) & (z < z1)).sum() / area; o.append(c / (N / 4010))
    RES["scan"].append((round(float(s), 3), [round(float(x), 3) for x in o])); print(f"shift {s:+.2f} (added to Wisconsin): density ratio to Zhang", np.round(o, 3))
json.dump(RES, open(os.path.join(HERE, "gh9_counts.json"), "w"), indent=1)
