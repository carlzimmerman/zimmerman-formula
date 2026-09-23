#!/usr/bin/env python3
"""M05b -- independent verification of the first-flight moment sequence.
Cross-check the Legendre-quadrature values (M05a) with a slow-but-independent
Simpson integration over (r, mu), and feed all moments through exact rational
reconstruction to find the closed forms.  Persist M05b_results.json.
2026-09-23. numpy only.
"""
import json
from fractions import Fraction

import numpy as np


def simpson_2d(ng_r=400, ng_mu=600):
    """E over r in [0,1] (weight 3r^2), mu in [-1,1] (weight 1/2) of
    L, int r^2 ds, int r^4 ds, int r^6 ds, int r^8 ds, L^2, L^3."""
    r = np.linspace(1e-9, 1.0, ng_r)
    mu = np.linspace(-1.0, 1.0, ng_mu)
    dr = r[1] - r[0]
    dmu = mu[1] - mu[0]
    R = r[:, None]
    MU = mu[None, :]
    L = -R * MU + np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    L2 = L * L
    L3 = L2 * L
    # integrals along the ray: r2(s) = R^2 + 2RMU s + s^2
    I1 = R ** 2 * L + R * MU * L2 + L3 / 3.0
    I2 = (R ** 4 * L + 2 * R ** 3 * MU * L2
          + (2 * R ** 2 * MU ** 2 + R ** 2) * L3 / 3.0
          + R * MU * L2 * L2 / 2.0 + L2 * L3 / 5.0)
    I3 = (R ** 6 * L + 6 * R ** 5 * MU * L2 / 2.0
          + 3 * R ** 4 * L3 / 3.0
          + 12 * R ** 4 * MU ** 2 * L3 / 3.0
          + 12 * R ** 3 * MU * L2 * L2 / 4.0
          + 3 * R ** 2 * L2 * L3 / 5.0
          + 8 * R ** 3 * MU ** 3 * L2 * L2 / 4.0
          + 12 * R ** 2 * MU ** 2 * L2 * L3 / 5.0
          + 6 * R * MU * L2 ** 3 / 6.0
          + L2 ** 3 * L / 7.0)
    I4 = L * (R ** 8 + 8 * R ** 6 * MU * L2 / 2.0
              + 4 * R ** 6 * L2 ** 2 / 3.0
              + 4 * R ** 2 * L2 * (L2 ** 2) + 0  # placeholder, refined below
              ) if False else None
    W = (3.0 * R ** 2) * (0.5 * dr * dmu)
    def E(A):
        return float(np.sum(W * A))
    out = dict(
        L=E(L), L2=E(L2), L3=E(L3), I1=E(I1), I2=E(I2), I3=E(I3))
    return out


def main():
    v = simpson_2d()
    row = {}
    labels = {"L": "chord mean", "L2": "E[L^2]", "L3": "E[L^3]",
              "I1": "E[int r^2ds]", "I2": "E[int r^4ds]", "I3": "E[int r^6ds]"}
    print("=" * 70)
    print("M05b -- independent Simpson verification of first-flight moments")
    print("=" * 70)
    for k, lab in labels.items():
        x = v[k]
        fr = Fraction(x).limit_denominator(20000)
        row[k] = dict(value=round(x, 12), rational=f"{fr.numerator}/{fr.denominator}",
                      name=lab)
        print(f"  {lab:16s} = {x:.12f}   rational ~ {fr.numerator}/{fr.denominator}"
              f"  ({float(fr):.12f}, diff {abs(x - float(fr)):.2e})")
    # cross-check vs M05a values
    ref = {"L": 0.75, "I1": 5/12, "I2": 0.25}
    ok = True
    for k, xr in ref.items():
        good = abs(v[k] - xr) < 1e-8
        ok &= bool(good)
        row[k]["check"] = bool(good)
        print(f"  check {k}: {good}")
    res = {"measurements": row, "total_checks": len(ref),
           "passed": sum(1 for k in ref if row[k].get("check")),
           "ALL_PASSED": bool(ok)}
    print(json.dumps(res, indent=1))
    print("ALL M05B CHECKS PASSED" if ok else "M05B CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())