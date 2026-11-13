#!/usr/bin/env python3
"""LNJ1 readings (written after lnj1.py ran; REPORTED ONLY, no word depends on them): read lnj1_per_lens.csv and describe
who sits above v*(z) on each rule, and where the ceiling-breaking lenses sit in s.  python3 lnj1_readings.py -> lnj1_readings.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = list(csv.DictReader(open(os.path.join(HERE, "lnj1_per_lens.csv"))))
col = lambda k: np.array([float(r[k]) for r in R])
z, tE, lm = col("z_l"), col("theta_E_arcsec"), col("log_Mstar_common")
OUT = []
def P(s): print(s); OUT.append(s)
for ft, sfx in (("canonical", "can"), ("alt", "alt")):
    sm, sx, ab = col("s_model_" + sfx), col("s_meas_" + sfx), col("above_band_" + sfx).astype(bool)
    P(f"[{ft}]")
    for nm, msk in (("theta_E < 1.0", tE < 1.0), ("1.0 <= theta_E < 1.3", (tE >= 1.0) & (tE < 1.3)), ("1.3 <= theta_E < 1.7", (tE >= 1.3) & (tE < 1.7)), ("theta_E >= 1.7", tE >= 1.7)):
        P(f"  {nm:22s} N {msk.sum():5d}: s_model median {np.median(sm[msk]):.3f} (max {sm[msk].max():.3f}, >= 1: {int((sm[msk] >= 1).sum())}); "
          f"s_meas median {np.median(sx[msk]):.3f} (>= 1: {int((sx[msk] >= 1).sum())}); above band {ab[msk].mean():.3f}")
    P(f"  lenses above the band (z_s infinity): {ab.sum()}; of them at s_model >= 1: {int((ab & (sm >= 1)).sum())}; at s_meas >= 1: {int((ab & (sx >= 1)).sum())}")
    up = sm >= 1
    if up.any():
        P(f"  model-rule lenses at s >= 1: N {up.sum()}; z_l {np.min(z[up]):.2f}-{np.max(z[up]):.2f} (median {np.median(z[up]):.2f}); log M* {np.min(lm[up]):.2f}-{np.max(lm[up]):.2f} (median {np.median(lm[up]):.2f}); theta_E median {np.median(tE[up]):.2f}\"")
    upx = sx >= 1
    if upx.any():
        P(f"  measured-rule lenses at s >= 1: N {upx.sum()}; z_l median {np.median(z[upx]):.2f}; log M* median {np.median(lm[upx]):.2f}; theta_E median {np.median(tE[upx]):.2f}\" (min {np.min(tE[upx]):.2f})")
    P(f"  Spearman-like rank correlation of s_model with log M*: {np.corrcoef(np.argsort(np.argsort(sm)), np.argsort(np.argsort(lm)))[0, 1]:.3f}; with z_l: {np.corrcoef(np.argsort(np.argsort(sm)), np.argsort(np.argsort(z)))[0, 1]:.3f}")
open(os.path.join(HERE, "lnj1_readings.out"), "w").write("\n".join(OUT) + "\nReported only. Adopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
