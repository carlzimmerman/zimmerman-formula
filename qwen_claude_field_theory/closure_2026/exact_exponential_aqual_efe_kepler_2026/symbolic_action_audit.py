#!/usr/bin/env python3
"""Symbolically vary the exponential AQUAL action and audit the EFD laws."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def run_symbolic_audit() -> dict[str, object]:
    y = sp.symbols("y", positive=True)
    primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu = 1 - sp.exp(-y)
    constitutive_residual = sp.simplify(sp.diff(primitive, y) / (2 * y) - mu)

    # Direct first variation of the gradient part of
    # L=-a0^2 G(|grad Phi|/a0)/(8 pi G)-rho Phi.
    px, py, pz = sp.symbols("p_x p_y p_z", real=True)
    a0, newton_G = sp.symbols("a_0 G_N", positive=True)
    norm_p = sp.sqrt(px**2 + py**2 + pz**2)
    primitive_p = (norm_p / a0) ** 2 + 2 * (1 + norm_p / a0) * sp.exp(-norm_p / a0) - 2
    lagrangian_gradient = -a0**2 * primitive_p / (8 * sp.pi * newton_G)
    mu_p = 1 - sp.exp(-norm_p / a0)
    momenta = sp.Matrix([sp.diff(lagrangian_gradient, p) for p in (px, py, pz)]).applyfunc(sp.simplify)
    expected_momenta = -mu_p * sp.Matrix([px, py, pz]) / (4 * sp.pi * newton_G)
    momentum_residual = sp.simplify(momenta - expected_momenta)

    # The actual flux Jacobian, evaluated only after differentiating, exposes
    # the transverse and longitudinal eigenvalues without inserting a rank.
    flux = mu_p * sp.Matrix([px, py, pz])
    flux_jacobian = sp.simplify(flux.jacobian([px, py, pz]))
    eta = sp.symbols("eta", positive=True)
    background_jacobian = sp.simplify(flux_jacobian.subs({px: 0, py: 0, pz: a0 * eta}))
    mu_e = 1 - sp.exp(-eta)
    longitudinal = sp.simplify(mu_e + eta * sp.exp(-eta))
    expected_jacobian = sp.diag(mu_e, mu_e, longitudinal)
    jacobian_residual = sp.simplify(background_jacobian - expected_jacobian)
    eigenvalues = background_jacobian.eigenvals()

    # Derive the eccentric-anomaly average used by the secular node law.
    # tan(E/2)=t reduces the seed integral to a rational real-line integral.
    t, aa, bb = sp.symbols("t a b", real=True, positive=True)
    seed_integral = sp.integrate(2 / (aa + bb * t**2), (t, -sp.oo, sp.oo)) / (2 * sp.pi)
    e, s = sp.symbols("e s", positive=True)
    I0 = sp.simplify(seed_integral.subs({aa: 1 - e, bb: 1 + e}))
    # In the physical 0<e<1 branch, I0=1/s with s=sqrt(1-e^2).
    C1 = e / s**3  # d I0/de = <cos(E)/(1-e cos(E))^2>
    I1 = 1 / s**3
    C2 = (I1 - 2 / s + 1) / e**2
    cos2f_average = (1 + s**2) * C2 - 2 * e * C1 + (e**2 - s**2) * I1
    cos2f_on_shell = sp.factor(cos2f_average.subs(e**2, 1 - s**2))
    alpha_squared = (1 - s) / (1 + s)
    eccentric_average_residual = sp.simplify(cos2f_on_shell - alpha_squared)

    # Exact deep-EFE uniform-core coefficients from the oblate ellipsoid.
    n_parallel_deep = 2 - sp.pi / 2
    n_perpendicular_deep = (1 - n_parallel_deep) / 2
    core_frequency_ratio_squared = sp.simplify(n_parallel_deep / (2 * n_perpendicular_deep))
    core_period_ratio = sp.sqrt(sp.simplify(1 / core_frequency_ratio_squared))

    # Parameterize the complete physical domain 0<s<=1 by s=1/(1+u),
    # u>=0.  Then 0<=alpha^2<1 and, for every real omega, the bracket is
    # its strictly positive margin plus a manifestly nonnegative square.
    u = sp.symbols("u", nonnegative=True)
    omega = sp.symbols("omega", real=True)
    physical_s = 1 / (1 + u)
    physical_alpha_squared = sp.factor(alpha_squared.subs(s, physical_s))
    geometry_margin = sp.simplify(1 - alpha_squared)
    expected_margin = sp.simplify(2 * s / (1 + s))
    physical_margin = sp.factor(expected_margin.subs(s, physical_s))
    bracket_minus_margin = sp.simplify(
        1
        - physical_alpha_squared * sp.cos(2 * omega)
        - physical_margin
    )
    expected_bracket_excess = sp.simplify(
        2 * physical_alpha_squared * sp.sin(omega) ** 2
    )
    alpha_nonnegative = sp.ask(sp.Q.nonnegative(physical_alpha_squared)) is True
    alpha_below_one = sp.ask(sp.Q.positive(1 - physical_alpha_squared)) is True
    geometry_margin_positive = sp.ask(sp.Q.positive(physical_margin)) is True
    bracket_excess_nonnegative = sp.ask(sp.Q.nonnegative(expected_bracket_excess)) is True

    checks = {
        "constitutive_identity": constitutive_residual == 0,
        "action_gradient_variation": momentum_residual == sp.zeros(3, 1),
        "flux_hessian_eigenvalues": jacobian_residual == sp.zeros(3, 3),
        "eccentric_anomaly_seed_integral": sp.simplify(I0 - 1 / sp.sqrt(1 - e**2)) == 0,
        "eccentric_anomaly_average": eccentric_average_residual == 0,
        "geometry_alpha_physical_range": alpha_nonnegative and alpha_below_one,
        "geometry_bracket_lower_bound": (
            sp.trigsimp(bracket_minus_margin - expected_bracket_excess) == 0
            and bracket_excess_nonnegative
        ),
        "geometry_bracket_positive": (
            sp.simplify(geometry_margin - expected_margin) == 0 and geometry_margin_positive
        ),
        "deep_core_ratio": sp.simplify(
            core_frequency_ratio_squared - (4 - sp.pi) / (sp.pi - 2)
        ) == 0,
    }
    return {
        "status": (
            "PASS_NONRELATIVISTIC_EFD_SYMBOLIC_AUDIT"
            if all(checks.values())
            else "FAIL_NONRELATIVISTIC_EFD_SYMBOLIC_AUDIT"
        ),
        "checks": checks,
        "derived": {
            "G_prime_over_2y": str(sp.simplify(sp.diff(primitive, y) / (2 * y))),
            "EL_flux_momentum": [str(value) for value in momenta],
            "background_flux_jacobian": str(background_jacobian),
            "background_flux_eigenvalues_with_multiplicity": {
                str(key): int(value) for key, value in eigenvalues.items()
            },
            "cos_2f_eccentric_anomaly_average": str(cos2f_on_shell),
            "alpha_squared": str(alpha_squared),
            "physical_alpha_squared_u": str(physical_alpha_squared),
            "geometry_bracket_lower_bound_u": str(physical_margin),
            "geometry_bracket_excess": str(expected_bracket_excess),
            "deep_core_frequency_ratio_squared": str(core_frequency_ratio_squared),
            "deep_core_period_ratio": str(core_period_ratio),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    audit = run_symbolic_audit()
    rendered = json.dumps(audit, indent=2, sort_keys=True)
    print(rendered)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if audit["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
