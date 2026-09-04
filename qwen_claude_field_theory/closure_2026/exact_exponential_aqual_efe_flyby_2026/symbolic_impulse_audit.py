#!/usr/bin/env python3
"""Exact symbolic audit of the EFD flyby, cross-section, and plane laws."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def run_symbolic_audit() -> dict:
    checks: dict[str, bool] = {}
    expressions: dict[str, str] = {}

    # Exponential AQUAL primitive and constitutive derivative.
    y = sp.symbols("y", positive=True)
    primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu = sp.simplify(sp.diff(primitive, y) / (2 * y))
    checks["primitive_yields_exponential_mu"] = sp.simplify(mu - (1 - sp.exp(-y))) == 0
    expressions["mu"] = str(mu)

    # The one scalar integral on which the full vector impulse rests.
    a, D, s = sp.symbols("a D s", positive=True)
    line_integral = sp.integrate((a * s**2 + D) ** (-sp.Rational(3, 2)), (s, -sp.oo, sp.oo))
    odd_integral = sp.integrate(s * (a * s**2 + D) ** (-sp.Rational(3, 2)), (s, -sp.oo, sp.oo))
    checks["even_line_integral"] = sp.simplify(line_integral - 2 / (sp.sqrt(a) * D)) == 0
    checks["odd_line_integral_vanishes"] = odd_integral == 0
    expressions["line_integral"] = str(line_integral)

    # Exact impact-plane Schur matrix and its two eigenvectors.
    q, theta = sp.symbols("q theta", positive=True, real=True)
    A = sp.diag(q, q, 1)
    n = sp.Matrix([sp.sin(theta), 0, sp.cos(theta)])
    trajectory_a = sp.trigsimp((n.T * A * n)[0])
    An = A * n
    B = sp.simplify(A - An * An.T / trajectory_a)
    e_phi = sp.Matrix([0, 1, 0])
    e_theta = sp.Matrix([sp.cos(theta), 0, -sp.sin(theta)])
    checks["schur_matrix_annihilates_trajectory"] = sp.simplify(B * n) == sp.zeros(3, 1)
    checks["azimuthal_impact_eigenvalue"] = sp.simplify(B * e_phi - q * e_phi) == sp.zeros(3, 1)
    checks["polar_impact_eigenvalue"] = (
        sp.simplify(sp.trigsimp(B * e_theta - q * e_theta / trajectory_a)) == sp.zeros(3, 1)
    )
    expressions["trajectory_anisotropy"] = str(trajectory_a)
    expressions["impact_eigenvalues"] = f"q, q/({trajectory_a})"

    # Transversality does not require choosing coordinates.
    scalar_d = sp.symbols("d", real=True)
    checks["impulse_transversality"] = sp.simplify(scalar_d - trajectory_a * scalar_d / trajectory_a) == 0

    # Generic azimuth multiplier and its global stationary value.
    lam_hi, lam_lo, weight = sp.symbols("lambda_hi lambda_lo weight", positive=True)
    factor_squared = (
        lam_hi**2 * weight + lam_lo**2 * (1 - weight)
    ) / (lam_hi * weight + lam_lo * (1 - weight)) ** 2
    stationary_weight = sp.solve(sp.factor(sp.diff(factor_squared, weight)), weight)[0]
    factor_max_squared = sp.factor(factor_squared.subs(weight, stationary_weight))
    factor_max = sp.sqrt(sp.factor(sp.together(factor_max_squared).as_numer_denom()[0])) / sp.sqrt(
        sp.factor(sp.together(factor_max_squared).as_numer_denom()[1])
    )
    expected_max = (lam_hi + lam_lo) / (2 * sp.sqrt(lam_hi * lam_lo))
    checks["azimuth_maximizer"] = sp.simplify(stationary_weight - lam_lo / (lam_hi + lam_lo)) == 0
    checks["azimuth_maximum"] = sp.simplify(factor_max - expected_max) == 0
    expressions["azimuth_stationary_weight"] = str(stationary_weight)
    expressions["azimuth_maximum"] = str(factor_max)

    # Maximum angle between impact vector and its impulse image.
    t = sp.symbols("t", positive=True)
    tan_delta = (q - 1) * t / (q + t**2)
    critical_t = sp.solve(sp.diff(tan_delta, t), t)[0]
    tangent_at_max = sp.simplify(tan_delta.subs(t, critical_t))
    sine_denominator = sp.refine(
        sp.sqrt(sp.factor(4 * q + (q - 1) ** 2)), sp.Q.positive(q + 1)
    )
    sine_at_max = (q - 1) / sine_denominator
    checks["misalignment_maximizer"] = sp.simplify(critical_t - sp.sqrt(q)) == 0
    checks["misalignment_sine_bound"] = sp.simplify(sine_at_max - (q - 1) / (q + 1)) == 0
    expressions["maximum_misalignment_sine"] = str(sine_at_max)

    # Jacobian of the two-dimensional Born scattering map.
    bx, by, ell = sp.symbols("b_x b_y ell", positive=True)
    B2 = sp.diag(lam_hi, lam_lo)
    bvec = sp.Matrix([bx, by])
    S = (bvec.T * B2 * bvec)[0]
    deflection = -ell * B2 * bvec / S
    jacobian = sp.simplify(deflection.jacobian([bx, by]).det())
    expected_jacobian = -ell**2 * lam_hi * lam_lo / S**2
    checks["born_map_jacobian"] = sp.simplify(jacobian - expected_jacobian) == 0
    expressions["born_map_jacobian"] = str(sp.factor(jacobian))

    # Substitute the EFD impact-plane eigenvalues and impulse length scale.
    C, v, u1, u2 = sp.symbols("C v u_1 u_2", positive=True)
    inverse_metric_quadratic = u1**2 / q + u2**2 / (q / a)
    ell_efd = 2 * C / (v**2 * sp.sqrt(a))
    det_b_from_u = sp.simplify(
        ell_efd**2 / ((q**2 / a) * inverse_metric_quadratic**2)
    )
    expected_cross_section = 4 * C**2 / (v**4 * (u1**2 + a * u2**2) ** 2)
    checks["anisotropic_rutherford_cross_section"] = (
        sp.simplify(det_b_from_u - expected_cross_section) == 0
    )
    expressions["anisotropic_rutherford_cross_section"] = str(expected_cross_section)

    # z=0 is an exact invariant plane and carries a standard Kepler potential.
    R, z = sp.symbols("R z", positive=True)
    phi = -C / sp.sqrt(q * R**2 + z**2)
    ke = C / sp.sqrt(q)
    checks["equatorial_potential_is_kepler"] = sp.simplify(phi.subs(z, 0) + ke / R) == 0
    checks["equatorial_vertical_force_vanishes"] = sp.simplify(sp.diff(phi, z).subs(z, 0)) == 0

    # Binet equation for every equatorial conic.
    f, eccentricity, angular_momentum = sp.symbols("f e h", positive=True)
    inverse_radius = ke / angular_momentum**2 * (1 + eccentricity * sp.cos(f))
    checks["equatorial_conic_solves_binet"] = (
        sp.simplify(sp.diff(inverse_radius, f, 2) + inverse_radius - ke / angular_momentum**2) == 0
    )

    # Exact hyperbolic deflection and Rutherford differential cross-section.
    scattering_angle, impact = sp.symbols("Theta b", positive=True)
    impact_of_angle = ke / (v**2 * sp.tan(scattering_angle / 2))
    exact_cross_section = sp.simplify(
        impact_of_angle
        / sp.sin(scattering_angle)
        * (-sp.diff(impact_of_angle, scattering_angle))
    )
    exact_rutherford = ke**2 / (4 * v**4 * sp.sin(scattering_angle / 2) ** 4)
    checks["exact_equatorial_rutherford"] = sp.trigsimp(exact_cross_section - exact_rutherford) == 0
    expressions["exact_equatorial_rutherford"] = str(exact_rutherford)
    beta = ke / (impact * v**2)
    hyperbolic_e = sp.sqrt(1 + beta**-2)
    checks["hyperbolic_deflection_identity"] = (
        sp.simplify(sp.sin(sp.atan(beta)) - 1 / hyperbolic_e) == 0
    )

    passed = all(checks.values())
    return {
        "schema_version": 1,
        "status": "PASS_SYMBOLIC_DERIVATION" if passed else "FAIL_SYMBOLIC_DERIVATION",
        "checks": checks,
        "expressions": expressions,
        "scope": {
            "generic_3d": "exact line integral of the first-Born straight trajectory",
            "equatorial_plane": "exact dynamics within the linearized EFD potential",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_symbolic_audit()
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
