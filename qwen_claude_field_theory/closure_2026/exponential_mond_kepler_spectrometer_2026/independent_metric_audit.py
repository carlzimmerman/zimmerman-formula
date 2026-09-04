#!/usr/bin/env python3
"""Independent exact-metric audit of the weak curvature/clock identities.

This file intentionally does not import the production derivation.  It builds
the exact Christoffel and Riemann tensors of

  ds^2=-(1+2 eps f(r))dt^2+(1-2 eps f(r))(dr^2+r^2 dOmega^2)

in spherical coordinates, differentiates at eps=0, and contracts with the
background inverse metric.  Therefore curvilinear-coordinate connection terms
and their cancellations are included rather than copied from a Cartesian
linearized-curvature formula.
"""

from __future__ import annotations

import json
from typing import Any

import sympy as sp


def audit() -> dict[str, Any]:
    t, r, theta, azimuth, eps = sp.symbols(
        "t r theta azimuth eps", real=True
    )
    f = sp.Function("f")(r)
    coords = (t, r, theta, azimuth)
    n = 4
    metric = sp.diag(
        -(1 + 2 * eps * f),
        1 - 2 * eps * f,
        (1 - 2 * eps * f) * r**2,
        (1 - 2 * eps * f) * r**2 * sp.sin(theta) ** 2,
    )
    inverse = sp.simplify(metric.inv())

    gamma = [[[
        sp.simplify(
            sum(
                inverse[a, d]
                * (
                    sp.diff(metric[d, c], coords[b])
                    + sp.diff(metric[d, b], coords[c])
                    - sp.diff(metric[b, c], coords[d])
                )
                for d in range(n)
            )
            / 2
        )
        for c in range(n)] for b in range(n)] for a in range(n)]

    ricci = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            ricci[a][b] = sp.simplify(
                sum(
                    sp.diff(gamma[c][a][b], coords[c])
                    - sp.diff(gamma[c][a][c], coords[b])
                    + sum(
                        gamma[c][c][d] * gamma[d][a][b]
                        - gamma[c][b][d] * gamma[d][a][c]
                        for d in range(n)
                    )
                    for c in range(n)
                )
            )
    scalar_exact = sp.simplify(
        sum(inverse[a, b] * ricci[a][b] for a in range(n) for b in range(n))
    )
    scalar_linear = sp.simplify(sp.diff(scalar_exact, eps).subs(eps, 0))

    # Differentiate R^a_bcd first, then lower its first index with g(eps=0).
    riemann_up_linear: dict[tuple[int, int, int, int], sp.Expr] = {}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    component = (
                        sp.diff(gamma[a][b][d], coords[c])
                        - sp.diff(gamma[a][b][c], coords[d])
                        + sum(
                            gamma[a][j][c] * gamma[j][b][d]
                            - gamma[a][j][d] * gamma[j][b][c]
                            for j in range(n)
                        )
                    )
                    linear = sp.simplify(sp.diff(component, eps).subs(eps, 0))
                    if linear != 0:
                        riemann_up_linear[(a, b, c, d)] = linear

    metric0 = metric.subs(eps, 0)
    inverse0 = inverse.subs(eps, 0)
    riemann_low_linear: dict[tuple[int, int, int, int], sp.Expr] = {}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    component = sp.simplify(
                        sum(
                            metric0[a, j]
                            * riemann_up_linear.get((j, b, c, d), 0)
                            for j in range(n)
                        )
                    )
                    if component != 0:
                        riemann_low_linear[(a, b, c, d)] = component

    kretschmann_quadratic = sp.Integer(0)
    for (a, b, c, d), left in riemann_low_linear.items():
        for (aa, bb, cc, dd), right in riemann_low_linear.items():
            raising = (
                inverse0[a, aa]
                * inverse0[b, bb]
                * inverse0[c, cc]
                * inverse0[d, dd]
            )
            if raising != 0:
                kretschmann_quadratic += raising * left * right
    kretschmann_quadratic = sp.simplify(kretschmann_quadratic)

    fp = sp.diff(f, r)
    fpp = sp.diff(f, (r, 2))
    expected_R = 2 * fpp + 4 * fp / r
    expected_K = 12 * fpp**2 + 16 * fp * fpp / r + 32 * fp**2 / r**2
    residual_R = sp.simplify(scalar_linear - expected_R)
    residual_K = sp.simplify(kretschmann_quadratic - expected_K)

    # The orbit clocks are obtained independently from V_eff=f+l^2/(2r^2).
    ell = sp.symbols("ell", positive=True)
    V_eff = f + ell**2 / (2 * r**2)
    ell2_circle = r**3 * fp
    kappa2 = sp.simplify(sp.diff(V_eff, r, 2).subs(ell**2, ell2_circle))
    omega2 = fp / r
    clock_R = sp.simplify(2 * (kappa2 - omega2))
    clock_K = sp.simplify(
        4 * (3 * kappa2**2 - 14 * kappa2 * omega2 + 23 * omega2**2)
    )
    clock_residual_R = sp.simplify(scalar_linear - clock_R)
    clock_residual_K = sp.simplify(kretschmann_quadratic - clock_K)

    A = sp.symbols("A", positive=True)
    profiles = {
        "newton": -A / r,
        "deep_mond": A * sp.log(r),
        "regular_center": sp.Rational(2, 3) * A * r ** sp.Rational(3, 2),
    }
    fingerprints: dict[str, dict[str, str]] = {}
    for name, profile in profiles.items():
        substitutions = {
            f: profile,
            fp: sp.diff(profile, r),
            fpp: sp.diff(profile, (r, 2)),
        }
        Om = sp.simplify(omega2.subs(substitutions))
        fingerprints[name] = {
            "R_over_Omega2": str(sp.simplify(scalar_linear.subs(substitutions) / Om)),
            "K_over_Omega4": str(
                sp.simplify(kretschmann_quadratic.subs(substitutions) / Om**2)
            ),
        }

    results = {
        "status": "PASS" if all(
            x == 0
            for x in (residual_R, residual_K, clock_residual_R, clock_residual_K)
        ) else "FAIL",
        "exact_metric_R_linear": str(scalar_linear),
        "exact_metric_K_quadratic": str(kretschmann_quadratic),
        "R_formula_residual": str(residual_R),
        "K_formula_residual": str(residual_K),
        "R_clock_residual": str(clock_residual_R),
        "K_clock_residual": str(clock_residual_K),
        "nonzero_Riemann_components": len(riemann_low_linear),
        "fingerprints": fingerprints,
    }
    return results


def main() -> int:
    results = audit()
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
