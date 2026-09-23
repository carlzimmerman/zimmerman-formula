"""Binned narrow-Halpha velocity field with REAL-noise centroid errors."""
import numpy as np, json
from scipy.optimize import curve_fit
from scipy.special import erf
from model import load, SIG_LSF
import noise as calib

D = load()
d, v, dv = D["data"], D["v"], D["dv"]
NB = 5                                           # 5x5 px = 0.1" bins
ny, nx = d.shape[1:]
YC, XC = 19, 20


def gline(vv, A, mu, sig):
    s2 = np.sqrt(2) * np.sqrt(sig ** 2 + SIG_LSF ** 2)
    return A * 0.5 * (erf((vv + dv / 2 - mu) / s2) - erf((vv - dv / 2 - mu) / s2))


def fit(spec):
    try:
        p, _ = curve_fit(gline, v, spec, p0=[max(spec.max(), 1e-3) * 3, 0.0, 40.0],
                         bounds=([0, -300, 0], [np.inf, 300, 300]), maxfev=20000)
        return p
    except Exception:
        return None


noise = [calib.noise_block(k) for k in range(len(calib.BLOCKS))]
rows = []
for by in range(0, ny - NB + 1, NB):
    for bx in range(0, nx - NB + 1, NB):
        spec = d[:, by:by + NB, bx:bx + NB].sum(axis=(1, 2))
        p = fit(spec)
        if p is None:
            continue
        A, mu, sig = p
        model = gline(v, *p)
        mus = []
        for nb in noise:
            q = fit(model + nb[:, by:by + NB, bx:bx + NB].sum(axis=(1, 2)))
            if q is not None:
                mus.append(q[1])
        emu = float(np.std(mus)) if len(mus) > 5 else np.nan
        cy, cx = by + NB / 2 - 0.5, bx + NB / 2 - 0.5
        rows.append(dict(bx=bx, by=by, dx_arcsec=(cx - XC) * 0.02, dy_arcsec=(cy - YC) * 0.02, flux=float(A),
                         v=float(mu), ev=emu, sig=float(sig), snr=float(A / np.std([nb[:, by:by + NB, bx:bx + NB].sum(axis=(1, 2)).sum() for nb in noise]))))
json.dump(rows, open("vfield.json", "w"), indent=1)
print(" dx(\")  dy(\")   flux   v(km/s)  +/-ev   sig   (v/ev)")
for r in rows:
    flag = "*" if np.isfinite(r["ev"]) and abs(r["v"] - (-22)) / r["ev"] > 3 else " "
    print(f"{r['dx_arcsec']:+.2f} {r['dy_arcsec']:+.2f} {r['flux']:7.2f} {r['v']:+8.1f} {r['ev']:6.1f} {r['sig']:6.1f} {flag}")
