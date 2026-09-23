"""REAL noise blocks: consecutive line-free channels of the same cube (4.60-5.43 um, all emission lines +/-1200 km/s and
spikes excluded), normalised by ERR and rescaled to the Halpha-window ERR: spatial + spectral correlations are the real ones."""
import numpy as np
from model import *

D0 = load()
fd, fe, fv = D0["full_data"], D0["full_err"], D0["full_v"]
lam_obs = 0.6564614 * (1 + Z_SYS)
w_full = lam_obs * (1 + fv / C_KMS)
bad = np.zeros(len(fv), bool)
for lam_rest in (6564.614, 6585.27, 6549.86, 6718.29, 6732.67, 6302.05, 6365.54, 5877.25, 6680.0, 7067.0):
    lc = lam_rest * 1e-4 * (1 + Z_SYS)
    bad |= np.abs(w_full / lc - 1) * C_KMS < 1200
spike = np.abs(np.nansum(fd, axis=(1, 2))) > 5 * np.nanstd(np.nansum(fd, axis=(1, 2)))
good = np.isfinite(fd).all(axis=(1, 2)) & (np.abs(fd).sum(axis=(1, 2)) > 0) & ~bad & ~spike & (w_full > 4.60) & (w_full < 5.43)
NCH = D0["data"].shape[0]
starts_ok = [s for s in range(len(fv) - NCH) if good[s:s + NCH].all()]
BLOCKS = starts_ok[::NCH]            # non-overlapping


def noise_block(k):
    s = BLOCKS[k % len(BLOCKS)]
    z = fd[s:s + NCH] / fe[s:s + NCH]
    z = z - z.mean(axis=0, keepdims=True)                 # remove any residual per-spaxel continuum
    return z * (D0["err"] / 1.6)                          # real correlated noise at the Halpha error level


