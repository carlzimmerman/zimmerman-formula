#!/usr/bin/env python3
"""Independent robustness audit for L232's parameter-free integer-slope test.

This deliberately changes the aggregation rule: L232 pools all radii, while this
audit gives each galaxy equal weight and then bootstraps galaxies.  No fitted
scale, mass-to-light ratio, or expected winner is inserted.  The purpose is to
measure whether the claimed integer selection is driven by a few long curves.
"""
from __future__ import annotations

import glob
import json
import math
import os
from dataclasses import dataclass

import numpy as np


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
KPC = 3.0857e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
C = 2.99792458e8
G = 6.674e-11
H0 = 67.4 * 1000 / 3.0857e22
RHO_CRIT = 3 * H0**2 / (8 * math.pi * G)
RHO_LAMBDA = 0.685 * RHO_CRIT
SCALES = {
    "Lambda": C * math.sqrt(G * RHO_LAMBDA),
    "critical": C * math.sqrt(G * RHO_CRIT),
}
NS = (1, 2, 3, 4)


@dataclass
class Curve:
    name: str
    gbar: np.ndarray
    gobs: np.ndarray


def load_curves() -> list[Curve]:
    curves: list[Curve] = []
    for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(fn, comments="#")
        except (OSError, ValueError):
            continue
        if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3:
            continue
        R, vo, evo, vg, vd, vb = (d[:, i] for i in range(6))
        m = (R > 0) & (vo > 0) & (evo > 0) & (evo / vo < 0.10)
        if m.sum() < 3:
            continue
        R, vo, vg, vd, vb = R[m], vo[m], vg[m], vd[m], vb[m]
        vb2 = vg * np.abs(vg) + UPS_D * vd * np.abs(vd) + UPS_B * vb * np.abs(vb)
        ok = vb2 > 0
        if ok.sum() < 3:
            continue
        r = R[ok] * KPC
        curves.append(Curve(os.path.basename(fn), vb2[ok] * KMS**2 / r,
                            vo[ok] ** 2 * KMS**2 / r))
    return curves


def predict(gbar: np.ndarray, scale: float, n: int, steps: int = 80) -> np.ndarray:
    """Solve [1-(1+g/scale)^(-n)] g = gbar by bracketed bisection."""
    lo = np.zeros_like(gbar)
    hi = np.maximum(gbar, 1e-30) * 2 + np.sqrt(np.maximum(gbar, 0) * scale / n) * 10
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        f = mid * (1.0 - (1.0 + mid / scale) ** (-n)) - gbar
        lo = np.where(f < 0, mid, lo)
        hi = np.where(f < 0, hi, mid)
    return 0.5 * (lo + hi)


def curve_rms(curve: Curve, scale: float, n: int) -> float:
    residual = np.log10(curve.gobs) - np.log10(predict(curve.gbar, scale, n))
    return float(np.sqrt(np.mean(residual**2)))


def equal_galaxy_scores(curves: list[Curve], scale: float) -> dict[int, float]:
    vals = {n: [curve_rms(c, scale, n) for c in curves] for n in NS}
    return {n: float(np.mean(vals[n])) for n in NS}


def bootstrap_winners(curves: list[Curve], scale: float, draws: int = 1000,
                      seed: int = 232) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    per_curve = np.asarray([[curve_rms(c, scale, n) for n in NS] for c in curves])
    wins = {n: 0 for n in NS}
    margins: list[float] = []
    for _ in range(draws):
        sample = rng.integers(0, len(curves), len(curves))
        scores = per_curve[sample].mean(axis=0)
        order = np.argsort(scores)
        wins[NS[int(order[0])]] += 1
        margins.append(float(scores[order[1]] - scores[order[0]]))
    return {
        "draws": draws,
        "seed": seed,
        "wins": wins,
        "winner_fraction": {str(n): wins[n] / draws for n in NS},
        "margin_median_dex": float(np.median(margins)),
        "margin_p05_dex": float(np.quantile(margins, 0.05)),
    }


def main() -> int:
    curves = load_curves()
    if not curves:
        raise RuntimeError("no SPARC curves loaded")
    result: dict[str, object] = {
        "ngal": len(curves),
        "mass_to_light": {"disk": UPS_D, "bulge": UPS_B},
        "scales": SCALES,
        "candidates": list(NS),
        "equal_galaxy": {},
        "bootstrap": {},
    }
    print(f"loaded {len(curves)} curves; equal-galaxy and bootstrap audit")
    for label, scale in SCALES.items():
        scores = equal_galaxy_scores(curves, scale)
        winner = min(scores, key=scores.get)
        boot = bootstrap_winners(curves, scale)
        result["equal_galaxy"][label] = {"scores_dex": scores, "winner": winner}
        result["bootstrap"][label] = boot
        print(f"{label}: equal-galaxy scores={scores}; winner={winner}")
        print(f"{label}: bootstrap winner fractions={boot['winner_fraction']}; "
              f"median margin={boot['margin_median_dex']:.5f} dex")
    out = os.path.join(HERE, "L232_robustness_results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
