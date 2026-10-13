#!/usr/bin/env python3
"""CFG652 staging (no statistic computed): extract the KiDS-1000 DR4.1 SOM-gold sources in the eFEDS/KiDS-G9 box
(RA 124-148, Dec -5 to +7) into ../../../_external_data/cfg652_work/cfg652_sources.npz (not committed). Chunked memmap read so
the process stays well below 1.5 GB. Columns kept: RAJ2000, DECJ2000, e1, e2, weight, Z_B.
Run from the repository root:  nice -n 10 python3 -u campaign_fresh_gravity/CFG652_hot_group_discriminator/cfg652_stage.py"""
import os, time
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
F = os.path.join(REPO, "real_research", "data", "lensing_rar", "KiDS_DR4.1_SOM_gold_WL_cat.fits")
OUT = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg652_work"))
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
BOX = (124.0, 148.0, -5.0, 7.0)
COLS = ("RAJ2000", "DECJ2000", "e1", "e2", "weight", "Z_B")
h = fits.open(F, memmap=True)
d = h[1].data
n = h[1].header["NAXIS2"]
CH = 400_000
keep = {c: [] for c in COLS}
for i0 in range(0, n, CH):
    blk = d[i0:i0 + CH]
    ra = np.asarray(blk["RAJ2000"], "f8"); de = np.asarray(blk["DECJ2000"], "f8")
    m = (ra >= BOX[0]) & (ra <= BOX[1]) & (de >= BOX[2]) & (de <= BOX[3])
    if m.any():
        for c in COLS:
            keep[c].append(np.asarray(blk[c], "f8")[m])
    del blk
    if (i0 // CH) % 10 == 0:
        print(f"[{time.time() - T0:6.0f} s] rows {i0:,}/{n:,}; kept {sum(len(x) for x in keep['Z_B']):,}", flush=True)
out = {c: np.concatenate(v) if v else np.zeros(0) for c, v in keep.items()}
np.savez(os.path.join(OUT, "cfg652_sources.npz"), **out)
print(f"[{time.time() - T0:6.0f} s] wrote {len(out['Z_B']):,} sources", flush=True)
