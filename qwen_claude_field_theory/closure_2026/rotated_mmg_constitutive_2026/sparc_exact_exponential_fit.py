"""Repository-local SPARC fit for the exact implicit exponential law.

The Lambda-derived a0 is fixed.  Only the stellar disk mass-to-light ratio is
scanned, with the bulge ratio tied to 1.4 times the disk ratio as in the
existing repository analysis.  This is a bounded empirical check, not a
claim that the catalogue fit establishes the relativistic theory.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


G_NEWTON = 6.674e-11
KPC = 3.0857e19
A0_LAMBDA = 9.36e-11


def invert_exponential(g_bar, a0=A0_LAMBDA):
    """Solve y(1-exp(-y))=g_bar/a0 by vectorized Newton iteration."""

    z = np.maximum(np.asarray(g_bar, dtype=float) / a0, 1e-30)
    y = np.sqrt(z) + z / 4.0
    for _ in range(40):
        e = np.exp(-y)
        f = y * (1.0 - e) - z
        df = 1.0 - e + y * e
        y = np.maximum(y - f / df, 1e-14)
    return a0 * y


def load_rows():
    data_dir = Path(__file__).parents[3] / "real_research" / "data" / "sparc_data"
    rows = []
    for path in sorted(data_dir.glob("*_rotmod.dat")):
        try:
            d = np.genfromtxt(path, comments="#")
        except (OSError, ValueError):
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        rows.append((d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]))
    return rows


def scatter(ud, rows, a0=A0_LAMBDA):
    residuals = []
    weights = []
    for radius, vobs, ev, vgas, vdisk, vbul in rows:
        vbar2 = np.sign(vgas) * vgas**2 + ud * vdisk**2 + 1.4 * ud * vbul**2
        gb = vbar2 * 1e6 / (radius * KPC)
        go = (vobs * 1e3) ** 2 / (radius * KPC)
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (vobs > 0)
        if not np.any(ok):
            continue
        pred = invert_exponential(gb[ok], a0)
        residuals.extend(np.log10(go[ok]) - np.log10(pred))
        frac = np.clip(ev[ok], 1.0, None) / np.clip(vobs[ok], 1.0, None)
        weights.extend(1.0 / frac**2)
    residuals = np.asarray(residuals)
    weights = np.asarray(weights)
    return float(np.sqrt(np.sum(weights * residuals**2) / np.sum(weights))), int(residuals.size)


def fit():
    rows = load_rows()
    grid = np.linspace(0.3, 1.2, 91)
    values = [(float(ud),) + scatter(float(ud), rows) for ud in grid]
    best = min(values, key=lambda item: item[1])
    return {
        "n_galaxies": len(rows),
        "a0_fixed": A0_LAMBDA,
        "grid": [0.3, 1.2, 91],
        "best_disk_ml": best[0],
        "best_scatter_dex": best[1],
        "n_points": best[2],
        "bulge_to_disk_ml": 1.4,
        "law": "mu(g/a0)*g=g_bar, mu=1-exp(-g/a0)",
    }


if __name__ == "__main__":
    result = fit()
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "sparc_exact_exponential_fit.json").write_text(json.dumps(result, indent=2) + "\n")
    print("SPARC_EXACT_EXPONENTIAL_FIT")
    print(json.dumps(result, indent=2))
