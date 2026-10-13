"""CFG686 step 1: one chunked pass over the KiDS-1000 SOM-gold FITS -> cached columns (RA, DEC, e1, e2, weight, Z_B) as float32/64 npy
in the session scratch (not the repo). No selection beyond finite values."""
import os, sys, numpy as np
from astropy.io import fits
F = os.path.join(os.path.dirname(__file__), "..", "..", "..", "_external_data", "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
h = fits.open(F, memmap=True); d = h[1].data; N = len(d); names = {c.name.upper(): c.name for c in h[1].columns}
want = {"ra": ("RAJ2000", "ALPHA_J2000"), "dec": ("DECJ2000", "DELTA_J2000"), "e1": ("E1", "AUTOCAL_E1"), "e2": ("E2", "AUTOCAL_E2"),
        "w": ("WEIGHT", "RECAL_WEIGHT"), "zb": ("Z_B",)}
cn = {k: next(names[n] for n in v if n in names) for k, v in want.items()}; print("columns:", cn, "rows", N, flush=True)
arr = {k: np.empty(N, np.float64 if k in ("ra", "dec") else np.float32) for k in cn}
step = 1_000_000
for i in range(0, N, step):
    ch = d[i:i+step]
    for k, c in cn.items(): arr[k][i:i+len(ch)] = ch[c]
    print(f"  {min(i+step, N):,}/{N:,}", flush=True)
for k in arr: np.save(os.path.join(OUT, f"kids_{k}.npy"), arr[k])
print("done")
