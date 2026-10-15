#!/usr/bin/env python3
"""Exact algebra for a background-subtracted pressureless Poisson/Gauss toy."""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rho1, rho2, g0, p = s.symbols("rho1 rho2 g0 p", positive=True)
    zeta1, zeta2, ratio = s.symbols("zeta1 zeta2 ratio", real=True)
    v = s.Matrix([s.sqrt(rho1), s.sqrt(rho2)])
    u = s.Matrix([zeta1 * s.sqrt(rho1), zeta2 * s.sqrt(rho2)])
    matrix = u * u.T / p - g0 * v * v.T
    checks = []

    def check(name, expression):
        residual = s.factor(expression)
        assert residual == 0, (name, residual)
        checks.append(name)

    expected = -g0 * rho1 * rho2 * (zeta1 - zeta2)**2 / p
    check("direct_determinant", matrix.det() - expected)
    check("critical_charge_ratio_reduction", expected.subs(zeta2, ratio * zeta1).subs(zeta1**2, g0) + g0**2 * rho1 * rho2 * (ratio - 1)**2 / p)
    neutral = s.Matrix([zeta2 * s.sqrt(rho2), -zeta1 * s.sqrt(rho1)])
    check("charge_neutral_displacement", (u.T * neutral)[0])
    check("independent_negative_quadratic_direction", (neutral.T * matrix * neutral)[0] + g0 * rho1 * rho2 * (zeta1 - zeta2)**2)
    omega = s.symbols("omega_squared")
    equal = matrix.subs(zeta2, zeta1)
    check("equal_ratio_spectrum", (omega * s.eye(2) - equal).det() - omega * (omega - (rho1 + rho2) * (zeta1**2 / p - g0)))
    rows = []
    for rr, r1, r2, pp in [
        (s.Rational(93906542194, 100000000), s.Integer(1), s.Rational(1, 1000), s.Rational(1, 4)),
        (s.Integer(2), s.Integer(1), s.Integer(1), s.Rational(1, 2)),
        (s.Integer(-1), s.Integer(2), s.Integer(3), s.Integer(1)),
        (s.Rational(1, 2), s.Rational(1, 100), s.Integer(3), s.Rational(81, 100)),
    ]:
        mm = matrix.subs({g0: 1, zeta1: 1, zeta2: rr, rho1: r1, rho2: r2, p: pp})
        determinant = s.factor(mm.det())
        assert determinant.is_negative is True
        rows.append({"zeta2_over_zeta1": str(rr), "rho1": str(r1), "rho2": str(r2), "p": str(pp), "determinant": str(determinant), "inertia": "one positive and one negative omega_squared"})
    result = {
        "status": "exact frozen-surrogate identities and examples passed",
        "symbolic_identity_count": len(checks), "symbolic_checks": checks,
        "exact_examples": rows,
        "non_claims": [
            "The subtracted homogeneous charged background is not a solved RTM background.",
            "No actual halo instability, mode growth rate, remnant outcome, metric completion or theory rejection is established.",
            "Pressure, gradients, supporting-force perturbations, conversion and finite boundaries are omitted by definition.",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "symbolic_identity_count": len(checks), "exact_example_count": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
