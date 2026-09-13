#!/usr/bin/env python3
"""Kepler-like apsidal-precession prediction from the exact exponential law.

Starting only from the spherical field equation

    mu(g/a0) g = G M/r^2,   mu(x)=1-exp(-x),

derive the circular and radial epicyclic frequencies.  The resulting
precession curve is dimensionless and parameter-free once rho=r/r_M is given,
with r_M=sqrt(GM/a0).  This is a prediction of the constitutive law, not a
fit to the rotation-curve sample.  Global novelty is not claimed.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


def derive_symbolically() -> dict[str, sp.Expr]:
    x = sp.symbols("x", positive=True)
    mu = 1 - sp.exp(-x)
    # A = d ln(mu*g)/d ln g = 1 + x mu'/mu.
    A = sp.simplify(1 + x * sp.diff(mu, x) / mu)
    kappa_ratio = sp.simplify(3 - 2 / A)  # kappa^2 / Omega^2
    precession = sp.simplify(2 * sp.pi * (1 / sp.sqrt(kappa_ratio) - 1))
    return {"mu": mu, "A": A, "kappa2_over_omega2": kappa_ratio,
            "precession": precession}


def solve_x(rho: float) -> float:
    """Solve x(1-exp(-x))=rho^-2 by monotone bisection."""
    target = rho ** -2
    lo, hi = 0.0, max(2.0, target + 2.0 * math.sqrt(target) + 2.0)
    for _ in range(160):
        mid = 0.5 * (lo + hi)
        val = mid * (-math.expm1(-mid))
        if val < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def prediction_row(rho: float) -> dict[str, float]:
    x = solve_x(rho)
    mu = -math.expm1(-x)
    # Use the negative-exponential form to avoid overflow at high acceleration.
    em = math.exp(-x)
    A = 1.0 + x * em / (1.0 - em)
    ratio = 3.0 - 2.0 / A
    precession = 2.0 * math.pi * (1.0 / math.sqrt(ratio) - 1.0)
    # P/P_Newton at the same M and r follows directly from P^2=4 pi^2 r/g.
    period_ratio = math.sqrt(mu)
    return {"rho": rho, "x": x, "mu": mu, "A": A,
            "kappa2_over_omega2": ratio,
            "period_over_newton": period_ratio,
            "apsidal_shift_rad": precession,
            "apsidal_shift_deg": math.degrees(precession)}


def main() -> int:
    symbolic = derive_symbolically()
    x = next(iter(symbolic["mu"].free_symbols))
    checks = {
        "A_derivation": sp.simplify(symbolic["A"] - (1 + x /
                                                     (sp.exp(x) - 1))) == 0,
        "deep_limit_kappa_ratio": sp.limit(symbolic["kappa2_over_omega2"], x, 0, dir="+") == 2,
        "newton_limit_kappa_ratio": sp.limit(symbolic["kappa2_over_omega2"], x, sp.oo) == 1,
        "deep_limit_period_ratio": sp.limit(sp.sqrt(symbolic["mu"]), x, 0, dir="+") == 0,
        "deep_limit_precession": sp.simplify(
            sp.limit(symbolic["precession"], x, 0, dir="+")
            - 2 * sp.pi * (1 / sp.sqrt(2) - 1)
        ) == 0,
    }
    checks["positive_stability_samples"] = all(
        0 < prediction_row(rho)["kappa2_over_omega2"] <= 2 for rho in (0.03, 0.1, 1.0, 10.0, 100.0)
    )
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print("  A(x)=", symbolic["A"])
    print("  kappa^2/Omega^2=", symbolic["kappa2_over_omega2"])
    print("  Delta-varpi=", symbolic["precession"])
    print()
    print("PREDICTION TABLE (rho=r/r_M; no fitted parameters)")
    rows = [prediction_row(rho) for rho in (0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 100.0)]
    for row in rows:
        print("  rho={rho:6.2f}  x={x:8.4f}  mu={mu:8.5f}  "
              "kappa2/Omega2={kappa2_over_omega2:7.4f}  "
              "Delta-varpi={apsidal_shift_deg:+8.3f} deg  "
              "P/P_N={period_over_newton:7.4f}".format(**row))
    print()
    print("Interpretation: the exact exponential law predicts retrograde apsidal")
    print("precession, tending to 0 in the Newtonian regime and -105.44 degrees/orbit")
    print("in the deep-MOND logarithmic-potential limit.  The transition location")
    print("scales as r_M=sqrt(GM/a0), so mass enters only through the predicted scale.")
    out = Path(__file__).with_name("kepler_precession_results.json")
    out.write_text(json.dumps({"symbolic": {k: str(v) for k, v in symbolic.items()},
                               "checks": checks, "rows": rows}, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
