#!/usr/bin/env python3
"""Exact source-coefficient and independent angular checks; no QCD fit."""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def poly(xs):
    return tuple(F(x) for x in xs)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(c, a):
    return tuple(c * x for x in a)


def strings(a):
    return [str(x) for x in a]


def simpson(fn, intervals):
    h = math.pi / intervals
    total = fn(0.0) + fn(math.pi)
    total += 4 * math.fsum(fn(h * i) for i in range(1, intervals, 2))
    total += 2 * math.fsum(fn(h * i) for i in range(2, intervals, 2))
    return h * total / 3


def main():
    data = json.loads((HERE / "source_coefficients.json").read_text())
    e, b = data["electric"], data["magnetic"]
    elog = sub(poly(e["xp"]), poly(e["xn"]))
    econst = mul(F(1, 8), sub(poly(e["yp"]), poly(e["yn"])))
    blog = mul(F(3), sub(poly(b["xp"]), poly(b["xn"])))
    bconst = mul(F(1, 4), sub(poly(b["yp"]), poly(b["yn"])))
    source10 = data["source_difference_formula_10"]
    for name, observed in [
        ("electric_minus_magnetic_log", sub(elog, blog)),
        ("electric_minus_magnetic_constant", sub(econst, bconst)),
        ("electric_plus_magnetic_log", add(elog, blog)),
        ("electric_plus_magnetic_constant", add(econst, bconst)),
    ]:
        assert observed == poly(source10[name]), (name, observed)

    # Independent exact contraction: E^2=(1+2x^2), B^2=2(1-x^2).
    # Angular measure is sqrt(1-x^2)dx; its moments / pi are 1/2, 1/8.
    angular = []
    for a, beta in [(F(1), F(0)), (F(0), F(1)),
                    (F(2, 3), F(-5, 7)), (F(7, 9), F(7, 9))]:
        local_constant = a - 2 * beta
        local_x2 = 2 * (a + beta)
        direct_over_pi = local_constant / 2 + local_x2 / 8
        # Parent scalar tensor: -3[b-(a+b)x^2]+(1-x^2)(a+b).
        scalar_constant = -3 * beta + a + beta
        scalar_x2 = 3 * (a + beta) - (a + beta)
        scalar_over_pi = scalar_constant / 2 + scalar_x2 / 8
        expected_over_pi = F(3, 4) * (a - beta)
        assert direct_over_pi == scalar_over_pi == expected_over_pi
        residuals = []
        for n in (1024, 4096):
            observed = simpson(lambda theta: math.sin(theta) ** 2 * (
                float(a) * (3 * math.cos(theta) ** 2 + math.sin(theta) ** 2)
                - 2 * float(beta) * math.sin(theta) ** 2), n)
            residual = abs(observed - math.pi * float(expected_over_pi))
            assert residual < 2e-13
            residuals.append(residual)
        angular.append({"a": str(a), "b": str(beta),
                        "integral_over_pi": str(direct_over_pi),
                        "simpson_abs_residuals": residuals})

    # Radial integral and conventions, represented without floating pi.
    # parent: 1/(32 pi^3 m) * 8 pi m * (3 pi/4) * (K^4/2).
    shell_coefficient_times_pi = F(1, 32) * 8 * F(3, 4) * F(1, 2)
    # worldline: 2pi*(3/2) * volume_ball/(2pi)^4;
    # volume_ball=pi^2 K^4/2.
    action_coefficient_times_pi = 2 * F(3, 2) * F(1, 32)
    assert shell_coefficient_times_pi == action_coefficient_times_pi == F(3, 32)

    # Charge swap keeps vacuum flavor invariants exactly, at rational charges.
    charges = [F(2, 3), F(-1, 3), F(-1, 3)]
    swapped = [charges[1], charges[0], charges[2]]
    assert sum(charges) == sum(swapped)
    assert sum(q*q for q in charges) == sum(q*q for q in swapped)
    assert (charges[0] + charges[1]) / 2 == (swapped[0] + swapped[1]) / 2
    assert (charges[0] - charges[1]) / 2 == -(swapped[0] - swapped[1]) / 2

    # Exact log coefficient: 3/(32pi) * [0,-6]/(96pi^3).
    mass_log_coefficient_pi4 = mul(F(3, 32 * 96), sub(elog, blog))
    assert mass_log_coefficient_pi4 == (F(0), F(-3, 512))
    scalar_log_coefficient_pi4 = mul(F(1, 2), mass_log_coefficient_pi4)
    assert scalar_log_coefficient_pi4 == (F(0), F(-3, 1024))
    result = {
        "status": "finite algebra and quadrature assertions passed",
        "source_delta_coefficients_in_units_gA2_over_96pi3F2m": {
            "electric_log": strings(elog), "electric_constant": strings(econst),
            "magnetic_log": strings(blog), "magnetic_constant": strings(bconst),
            "difference_log": strings(sub(elog, blog)),
            "difference_constant": strings(sub(econst, bconst))},
        "soft_mass_coefficient_times_pi": str(shell_coefficient_times_pi),
        "mass_log_coefficient_in_units_gA2_over_pi4F2m": strings(mass_log_coefficient_pi4),
        "ml_derivative_coefficient_in_same_units": strings(scalar_log_coefficient_pi4),
        "charge_invariants": {"TrQ": str(sum(charges)),
                              "TrQ2": str(sum(q*q for q in charges))},
        "angular_checks": angular,
        "non_claims": ["No QCD path integral was numerically evaluated",
                       "No full M_u, A_rho, R or physical alpha is computed",
                       "No fitted LEC or empirical polarizability is input",
                       "Numerical quadrature is a finite diagnostic, not interval proof",
                       "Exact symmetry proof and chiral remainder hypotheses are separate"]}
    output = Path(sys.argv[1])
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": "passed", "mass_log_rational": strings(mass_log_coefficient_pi4),
                      "maximum_quadrature_residual": max(r for row in angular for r in row["simpson_abs_residuals"])}))


if __name__ == "__main__":
    main()
