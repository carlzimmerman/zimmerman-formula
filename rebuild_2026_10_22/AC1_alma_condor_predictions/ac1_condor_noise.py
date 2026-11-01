#!/usr/bin/env python3
"""AC1: real noise of a public CONDOR cube from its first complete channels, against the archive's listed figure. Needs only a truncated FITS file.
    python3 -I ac1_condor_noise.py PARTIAL.fits LISTED_mJy_per_10kms OUT.json"""
import json, math, os, sys
import numpy as np
f, listed, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
b = open(f, "rb"); H = {}; nb = 0; done = False
while not done:
    blk = b.read(2880); nb += 2880
    for i in range(0, 2880, 80):
        l = blk[i:i + 80].decode("ascii", "replace"); k = l[:8].strip()
        if k == "END": done = True; break
        if l[8:10] == "= ": H[k] = l[10:].split("/")[0].strip().strip("'").strip()
nx, ny, nz = int(H["NAXIS1"]), int(H["NAXIS2"]), int(H["NAXIS3"]); assert H["BITPIX"] == "-32"
size = os.path.getsize(f); nch = (size - nb) // (nx * ny * 4)
nu0, dnu = float(H["CRVAL3"]) + (1 - float(H["CRPIX3"])) * float(H["CDELT3"]), float(H["CDELT3"]); dv = abs(dnu) / abs(nu0) * 299792.458; pix = abs(float(H["CDELT2"])) * 3600
print(f"cube {nx}x{ny}x{nz}, pix {pix:.4f}\", beam {float(H['BMAJ']) * 3600:.4f}x{float(H['BMIN']) * 3600:.4f}\", dv {dv:.2f} km/s, {H.get('OBJECT')}; complete channels in the partial file {nch}; first {nu0 / 1e9:.3f} GHz")
d = np.memmap(f, dtype=">f4", mode="r", offset=nb, shape=(nch, ny, nx))
yy, xx = np.indices((ny, nx)); r = np.hypot(xx - nx // 2, yy - ny // 2) * pix
mad = lambda a: 1.4826 * np.median(np.abs(a - np.median(a)))
skip = min(10, nch // 4); R = {}
for lo, hi in ((1.5, 4), (4, 8), (8, 14), (14, 20)):
    m = (r > lo) & (r < hi)
    if not m.any(): continue
    v = [mad(x[np.isfinite(x)]) for x in (np.asarray(d[k])[m] for k in range(skip, nch, max(1, (nch - skip) // 12))) if np.isfinite(x).any()]
    R[f"{lo}-{hi}"] = dict(rms_mJy_ch=1e3 * float(np.median(v)), per_10kms=1e3 * float(np.median(v)) * math.sqrt(dv / 10), n=len(v)); print(f"r {lo}-{hi}\": rms/ch {R[f'{lo}-{hi}']['rms_mJy_ch']:.3f} mJy, scaled to 10 km/s {R[f'{lo}-{hi}']['per_10kms']:.3f}")
# channel correlation: bin an inner annulus box in frequency; scale check. Off the phase centre by 2-6 arcsec.
h = int(2 / pix); c = int(4 / pix); sub = np.array(d[skip:nch, ny // 2 - h:ny // 2 + h, nx // 2 + c - h:nx // 2 + c + h], dtype=np.float32); B = {}
for k in (1, 2, 4, 8):
    n = sub.shape[0] // k
    if n < 2: continue
    s = sub[:n * k].reshape(n, k, *sub.shape[1:]).mean(axis=1); x = mad(s[np.isfinite(s)]) * 1e3; B[str(k)] = dict(dv=k * dv, rms=float(x), per_10kms=float(x) * math.sqrt(k * dv / 10)); print(f"bin {k}: dv {k * dv:.1f}, rms {x:.3f} mJy, scaled to 10 km/s {B[str(k)]['per_10kms']:.3f}")
best = B[max(B, key=int)]["per_10kms"]; ratio = listed / best
print(f"listed {listed:.3f} mJy/beam per 10 km/s; measured {best:.3f} (widest bin); listed/measured {ratio:.2f}")
json.dump(dict(header={k: H.get(k) for k in ("OBJECT", "NAXIS1", "NAXIS2", "NAXIS3", "BMAJ", "BMIN", "CDELT2", "CDELT3")}, n_channels=nch, dv=dv, annuli=R, bins=B, listed=listed, measured=best, ratio=ratio), open(out, "w"), indent=0)
