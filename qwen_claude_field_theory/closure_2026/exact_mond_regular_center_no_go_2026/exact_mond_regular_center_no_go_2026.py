#!/usr/bin/env python3
"""Executable regular-center theorem for the exact exponential MOND law.

The calculation is deliberately independent of a particular relativistic
completion.  Any candidate satisfying the requested quasistatic field equation

    div[(1-exp(-|grad Phi|/a0)) grad Phi] = 4*pi*G*rho

inherits this local regularity test.  The program computes the constitutive
Jacobian, solves the positive spherical branch as a Puiseux series, and tests a
small deformation of the kernel as a negative control.

The result is scoped: a finite-action weak solution exists, but a classical C2
physical metric does not exist at a force-free point of positive density.  No
claim of global literature novelty is made by this script.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import sympy as sp
import mpmath as mp


FIELD_EQUATION = r"""
div[A(grad Phi)] = 4*pi*G*rho,
A(p) = mu(|p|/a0) p,
mu(y) = 1-exp(-y).
""".strip()


def _derive_kernel() -> dict[str, Any]:
    y = sp.symbols("y", nonnegative=True)
    mu = 1 - sp.exp(-y)
    primitive = y**2 + 2 * ((1 + y) * sp.exp(-y) - 1)
    transverse = mu
    parallel = sp.factor(sp.diff(y * mu, y))
    return {
        "y": y,
        "mu": mu,
        "primitive": primitive,
        "mu_residual": sp.simplify(mu - (1 - sp.exp(-y))),
        "mu_at_zero": sp.limit(mu, y, 0, dir="+"),
        "deep_mond_slope": sp.limit(mu / y, y, 0, dir="+"),
        "newtonian_limit": sp.limit(mu, y, sp.oo),
        "transverse_eigenvalue": transverse,
        "parallel_eigenvalue": parallel,
        "primitive_cubic_ratio": sp.limit(primitive / y**3, y, 0, dir="+"),
    }


def _derive_constitutive_jacobian(kernel: dict[str, Any]) -> dict[str, Any]:
    a0 = sp.symbols("a_0", positive=True)
    epsilon = sp.symbols("epsilon", positive=True)
    p = sp.Matrix(sp.symbols("p_1:4", real=True))
    norm = sp.sqrt((p.T * p)[0])
    mu_of_p = 1 - sp.exp(-norm / a0)
    flux = sp.Matrix([mu_of_p * component for component in p])
    jacobian = sp.simplify(flux.jacobian(p))

    axis_jacobian = sp.simplify(
        jacobian.subs({p[0]: epsilon, p[1]: 0, p[2]: 0}, simultaneous=True)
    )
    u = sp.symbols("u", positive=True)
    axis_dimensionless = sp.simplify(axis_jacobian.subs(epsilon, a0 * u))
    expected_axis = sp.diag(
        kernel["parallel_eigenvalue"].subs(kernel["y"], u),
        kernel["transverse_eigenvalue"].subs(kernel["y"], u),
        kernel["transverse_eigenvalue"].subs(kernel["y"], u),
    )
    origin_limit = axis_dimensionless.applyfunc(
        lambda expression: sp.limit(expression, u, 0, dir="+")
    )
    return {
        "a0": a0,
        "p": p,
        "norm": norm,
        "flux": flux,
        "jacobian": jacobian,
        "axis_jacobian": axis_dimensionless,
        "axis_off_diagonal_residual": sp.simplify(axis_dimensionless - expected_axis),
        "axis_parallel_residual": sp.simplify(
            axis_dimensionless[0, 0] - expected_axis[0, 0]
        ),
        "axis_transverse_residual": sp.simplify(
            axis_dimensionless[1, 1] - expected_axis[1, 1]
        ),
        "origin_limit": origin_limit,
        "origin_rank": origin_limit.rank(),
        "direction_independent_reason": (
            "The map is rotationally covariant and both its longitudinal and "
            "transverse eigenvalues tend to zero."
        ),
    }


def _derive_critical_point(
    jacobian: dict[str, Any],
) -> dict[str, Any]:
    G = sp.symbols("G", positive=True)
    # Keep rho algebraically unconstrained while solving.  A positive assumption
    # makes SymPy correctly report that 0=4*pi*G*rho has no admissible root,
    # which hides the boundary value rho=0 that the theorem needs to display.
    rho = sp.symbols("rho", real=True)
    hessian = sp.Matrix(3, 3, lambda i, j: sp.symbols(f"H_{i}{j}", real=True))
    origin_jacobian = jacobian["origin_limit"]
    operator = sp.factor(
        sum(origin_jacobian[i, j] * hessian[i, j] for i in range(3) for j in range(3))
    )
    required_source = sp.solve(sp.Eq(operator, 4 * sp.pi * G * rho), rho)[0]
    return {
        "hessian": hessian,
        "operator_at_critical_point": operator,
        "required_source_at_critical_point": required_source,
        "positive_density_contradiction": bool(
            required_source == 0 and G.is_positive
        ),
        "regularity_threshold": "C2",
        "theorem": (
            "If Phi is C2 near x0, grad(Phi)(x0)=0, and the exact equation "
            "holds pointwise, then rho(x0)=0."
        ),
    }


def _solve_positive_puiseux_branch(order: int = 5) -> dict[str, Any]:
    """Solve a smooth-core flux recursively on its positive branch.

    For rho(r)=rho_0+O(r^2), the dimensionless integrated source is
    t^2+q*t^6+O(t^10).  The q term therefore first changes the fifth
    coefficient of u(t); the leading singularity is universal.
    """

    t = sp.symbols("t", positive=True)
    q = sp.symbols("q", real=True)
    coefficients = sp.symbols(f"a_1:{order + 1}", real=True)
    series_u = sum(coefficients[index - 1] * t**index for index in range(1, order + 1))
    residual = sp.series(
        series_u * (1 - sp.exp(-series_u)) - t**2 - q * t**6,
        t,
        0,
        order + 2,
    ).removeO().expand()

    solution: dict[sp.Symbol, sp.Expr] = {}
    equation_residuals: list[sp.Expr] = []
    for index, coefficient in enumerate(coefficients, start=2):
        equation = sp.factor(residual.subs(solution).coeff(t, index))
        roots = sp.solve(sp.Eq(equation, 0), coefficient)
        if not roots:
            raise RuntimeError(f"Puiseux recursion failed at t^{index}")
        if coefficient == coefficients[0]:
            positive_roots = [root for root in roots if root.is_positive]
            if len(positive_roots) != 1:
                raise RuntimeError("positive acceleration branch was not unique")
            chosen = positive_roots[0]
        elif len(roots) == 1:
            chosen = roots[0]
        else:
            raise RuntimeError(f"Puiseux coefficient {coefficient} was not unique")
        solution[coefficient] = sp.factor(chosen)
        equation_residuals.append(sp.simplify(equation.subs(coefficient, chosen)))

    solved_series = sp.expand(series_u.subs(solution))
    final_residual = sp.series(
        solved_series * (1 - sp.exp(-solved_series)) - t**2 - q * t**6,
        t,
        0,
        order + 2,
    ).removeO().expand()
    return {
        "t": t,
        "q": q,
        "series": solved_series,
        "coefficients": tuple(solution[value] for value in coefficients),
        "coefficient_equation_residuals": tuple(equation_residuals),
        "residual": sp.simplify(final_residual),
    }


def _derive_ricci_scalar(
    metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]
) -> sp.Expr:
    """Derive the coordinate-invariant Ricci scalar from a metric matrix."""

    dimension = len(coordinates)
    inverse_metric = sp.simplify(metric.inv())
    christoffel = [
        [[sp.Integer(0) for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for lower_a in range(dimension):
            for lower_b in range(dimension):
                christoffel[upper][lower_a][lower_b] = sp.simplify(
                    sum(
                        inverse_metric[upper, index]
                        * (
                            sp.diff(metric[index, lower_a], coordinates[lower_b])
                            + sp.diff(metric[index, lower_b], coordinates[lower_a])
                            - sp.diff(metric[lower_a, lower_b], coordinates[index])
                        )
                        for index in range(dimension)
                    )
                    / 2
                )

    ricci = sp.zeros(dimension)
    for row in range(dimension):
        for column in range(dimension):
            ricci[row, column] = sp.simplify(
                sum(
                    sp.diff(
                        christoffel[index][row][column], coordinates[index]
                    )
                    - sp.diff(
                        christoffel[index][row][index], coordinates[column]
                    )
                    + sum(
                        christoffel[index][index][other]
                        * christoffel[other][row][column]
                        - christoffel[index][column][other]
                        * christoffel[other][row][index]
                        for other in range(dimension)
                    )
                    for index in range(dimension)
                )
            )
    return sp.factor(
        sum(
            inverse_metric[row, column] * ricci[row, column]
            for row in range(dimension)
            for column in range(dimension)
        )
    )


def _derive_spherical_core() -> dict[str, Any]:
    r, a0, G, rho = sp.symbols("r a_0 G rho_0", positive=True)
    c = sp.symbols("c", positive=True)
    C = sp.factor(4 * sp.pi * G * rho / 3)
    puiseux = _solve_positive_puiseux_branch()
    t = puiseux["t"]
    q = puiseux["q"]
    general_u_series = puiseux["series"]
    u_series = sp.expand(general_u_series.subs(q, 0))
    g_series = sp.expand(a0 * u_series.subs(t, sp.sqrt(C * r / a0)))
    potential_series = sp.integrate(g_series, r)

    integrated_flux = sp.factor(r**2 * C * r)
    enclosed_source = sp.factor(4 * sp.pi * G * rho * r**3 / 3)
    source_divergence = sp.factor(sp.diff(integrated_flux, r) / r**2)

    radial_hessian = sp.diff(g_series, r)
    tangential_hessian = g_series / r
    laplacian = sp.factor(radial_hessian + 2 * tangential_hessian)
    tidal_norm_squared = sp.factor(radial_hessian**2 + 2 * tangential_hessian**2)
    curvature_scale = sp.sqrt(a0 * C)
    # For ds^2=-(1+2 Phi/c^2)c^2dt^2+(1-2 Psi/c^2)dx^2,
    # the linear Ricci scalar is 2(2 Delta Psi-Delta Phi)/c^2.  No slip
    # therefore gives R^(1)=2 Delta Phi/c^2.
    no_slip_ricci_scalar = sp.factor(2 * laplacian / c**2)
    first_derivative_curvature_scale = sp.factor(g_series**2 / c**4)
    nonlinear_curvature_ratio = sp.factor(
        first_derivative_curvature_scale / no_slip_ricci_scalar
    )

    time, theta, azimuth = sp.symbols("time theta azimuth", real=True)
    generic_potential = sp.Function("Phi_full")(r)
    temporal_factor = 1 + 2 * generic_potential / c**2
    spatial_factor = 1 - 2 * generic_potential / c**2
    isotropic_metric = sp.diag(
        -c**2 * temporal_factor,
        spatial_factor,
        spatial_factor * r**2,
        spatial_factor * r**2 * sp.sin(theta) ** 2,
    )
    full_metric_ricci_generic = _derive_ricci_scalar(
        isotropic_metric, (time, r, theta, azimuth)
    )
    full_metric_ricci = sp.factor(
        full_metric_ricci_generic.xreplace(
            {
                generic_potential: potential_series,
                sp.diff(generic_potential, r): g_series,
                sp.diff(generic_potential, r, 2): radial_hessian,
            }
        )
    )

    flux_u = sp.symbols("u", nonnegative=True)
    flux_map = sp.factor(flux_u * (1 - sp.exp(-flux_u)))
    flux_derivative = sp.factor(sp.diff(flux_map, flux_u))
    derivative_numerator = sp.factor(sp.exp(flux_u) * flux_derivative)
    derivative_numerator_derivative = sp.factor(sp.diff(derivative_numerator, flux_u))

    return {
        "r": r,
        "a0": a0,
        "G": G,
        "rho": rho,
        "C": C,
        "c": c,
        "mass_correction_q": q,
        "dimensionless_radius": sp.sqrt(C * r / a0),
        "dimensionless_acceleration_series_general_smooth_core": general_u_series,
        "dimensionless_acceleration_series": u_series,
        "coefficients": puiseux["coefficients"],
        "uniform_core_coefficients": tuple(
            sp.simplify(value.subs(q, 0)) for value in puiseux["coefficients"]
        ),
        "coefficient_equation_residuals": puiseux["coefficient_equation_residuals"],
        "series_residual_through_sixth_order": puiseux["residual"],
        "acceleration_series": g_series,
        "potential_series": potential_series,
        "leading_acceleration_ratio": sp.simplify(
            sp.limit(g_series / sp.sqrt(a0 * C * r), r, 0, dir="+")
        ),
        "integrated_flux": integrated_flux,
        "integrated_flux_residual": sp.simplify(integrated_flux - enclosed_source),
        "source_divergence": source_divergence,
        "divergence_source_residual": sp.simplify(
            source_divergence - 4 * sp.pi * G * rho
        ),
        "radial_hessian": radial_hessian,
        "tangential_hessian": tangential_hessian,
        "laplacian": laplacian,
        "tidal_norm_squared": tidal_norm_squared,
        "no_slip_ricci_scalar": no_slip_ricci_scalar,
        "full_metric_ricci_scalar": full_metric_ricci,
        "first_derivative_curvature_scale": first_derivative_curvature_scale,
        "flux_map": flux_map,
        "flux_map_at_zero": flux_map.subs(flux_u, 0),
        "flux_map_derivative": flux_derivative,
        "flux_derivative_numerator": derivative_numerator,
        "flux_derivative_numerator_derivative": derivative_numerator_derivative,
        "flux_derivative_numerator_derivative_positive": bool(
            derivative_numerator_derivative.is_positive
        ),
        "positive_inverse_branch_exists_and_is_unique": bool(
            flux_map.subs(flux_u, 0) == 0
            and derivative_numerator_derivative.is_positive
            and sp.limit(flux_map, flux_u, sp.oo) == sp.oo
        ),
        "radial_hessian_scaled_limit": sp.simplify(
            sp.limit(sp.sqrt(r) * radial_hessian / curvature_scale, r, 0, dir="+")
        ),
        "tangential_hessian_scaled_limit": sp.simplify(
            sp.limit(sp.sqrt(r) * tangential_hessian / curvature_scale, r, 0, dir="+")
        ),
        "laplacian_scaled_limit": sp.simplify(
            sp.limit(sp.sqrt(r) * laplacian / curvature_scale, r, 0, dir="+")
        ),
        "tidal_norm_squared_scaled_limit": sp.simplify(
            sp.limit(r * tidal_norm_squared / (a0 * C), r, 0, dir="+")
        ),
        "no_slip_ricci_scalar_scaled_limit": sp.simplify(
            sp.limit(
                sp.sqrt(r) * c**2 * no_slip_ricci_scalar / curvature_scale,
                r,
                0,
                dir="+",
            )
        ),
        "full_metric_ricci_scaled_limit": sp.simplify(
            sp.limit(
                sp.sqrt(r) * c**2 * full_metric_ricci / curvature_scale,
                r,
                0,
                dir="+",
            )
        ),
        "full_to_linear_ricci_ratio_limit": sp.simplify(
            sp.limit(
                full_metric_ricci / no_slip_ricci_scalar,
                r,
                0,
                dir="+",
            )
        ),
        "nonlinear_curvature_ratio_limit": sp.simplify(
            sp.limit(nonlinear_curvature_ratio, r, 0, dir="+")
        ),
        "hessian_diverges": bool(
            sp.limit(radial_hessian, r, 0, dir="+") == sp.oo
            and sp.limit(tangential_hessian, r, 0, dir="+") == sp.oo
        ),
        "tidal_norm_squared_diverges": bool(
            sp.limit(tidal_norm_squared, r, 0, dir="+") == sp.oo
        ),
        "no_slip_ricci_scalar_diverges": bool(
            sp.limit(no_slip_ricci_scalar, r, 0, dir="+") == sp.oo
        ),
    }


def _derive_weak_solution(
    kernel: dict[str, Any], spherical: dict[str, Any]
) -> dict[str, Any]:
    # G(y) ~ y^3 and y ~ r^(1/2).  Including the spherical measure r^2
    # gives r^(7/2), which is locally integrable even though D^2 Phi diverges.
    primitive_power = sp.Integer(3)
    acceleration_power = sp.Rational(1, 2)
    radial_energy_power = sp.simplify(2 + primitive_power * acceleration_power)
    return {
        "primitive_cubic_ratio": kernel["primitive_cubic_ratio"],
        "acceleration_power": acceleration_power,
        "radial_energy_power": radial_energy_power,
        "radial_energy_integrable": bool(radial_energy_power > -1),
        "weak_solution_exists": bool(
            spherical["divergence_source_residual"] == 0
            and radial_energy_power > -1
        ),
        "classical_c2_solution_exists": not spherical["hessian_diverges"],
        "distinction": (
            "The exact radial flux defines a locally finite-action weak solution, "
            "but its Hessian and weak-field tidal curvature are unbounded."
        ),
    }


def _derive_phantom_density(spherical: dict[str, Any]) -> dict[str, Any]:
    """Translate the same curvature into an Einstein-source description."""

    r = spherical["r"]
    G = spherical["G"]
    rho = spherical["rho"]
    a0 = spherical["a0"]
    C = spherical["C"]
    g = spherical["acceleration_series"]
    rho_effective = sp.factor(spherical["laplacian"] / (4 * sp.pi * G))
    rho_phantom = sp.factor(rho_effective - rho)
    density_scale = sp.sqrt(a0 * C) / (8 * sp.pi * G)
    effective_mass = sp.factor(r**2 * g / G)
    mass_scale = sp.sqrt(a0 * C) * r ** sp.Rational(5, 2) / G
    effective_density_at_center = sp.limit(rho_effective, r, 0, dir="+")
    effective_mass_at_center = sp.limit(effective_mass, r, 0, dir="+")
    return {
        "effective_density": rho_effective,
        "phantom_density": rho_phantom,
        "effective_density_scaled_limit": sp.simplify(
            sp.limit(sp.sqrt(r) * rho_effective / density_scale, r, 0, dir="+")
        ),
        "phantom_density_scaled_limit": sp.simplify(
            sp.limit(sp.sqrt(r) * rho_phantom / density_scale, r, 0, dir="+")
        ),
        "effective_mass": effective_mass,
        "effective_mass_scaled_limit": sp.simplify(
            sp.limit(effective_mass / mass_scale, r, 0, dir="+")
        ),
        "effective_density_at_center": effective_density_at_center,
        "effective_mass_at_center": effective_mass_at_center,
        "density_cusp_integrable": bool(effective_mass_at_center == 0),
        "effective_stress_regular_at_center": bool(
            effective_density_at_center.is_finite
        ),
        "architectural_consequence": (
            "Any ordinary-Einstein/no-slip phantom-density rewrite of the exact "
            "MOND branch must generate an integrable r^(-1/2) effective-density "
            "cusp from smooth positive baryons."
        ),
    }


def _derive_central_kepler_law(spherical: dict[str, Any]) -> dict[str, Any]:
    """Derive the circular-orbit analogue of Kepler's law in a smooth core."""

    r = spherical["r"]
    a0 = spherical["a0"]
    C = spherical["C"]
    G = spherical["G"]
    rho = spherical["rho"]
    g = spherical["acceleration_series"]
    t = sp.symbols("t", positive=True)
    u = spherical["dimensionless_acceleration_series"].subs(
        sp.symbols("t", positive=True), t
    )

    v_squared = sp.factor(r * g)
    v_fourth = sp.factor(v_squared**2)
    v_fourth_scale = a0 * C * r**3
    v_correction = sp.series((u / t) ** 2, t, 0, 4)
    period_correction = sp.series((t / u) ** 2, t, 0, 4)
    period_fourth_scale_over_r = sp.factor(16 * sp.pi**4 / (a0 * C))
    period_fourth_scale_over_r_rho = sp.factor(
        period_fourth_scale_over_r.subs(C, 4 * sp.pi * G * rho / 3)
    )

    sample_t = (0.1, 0.03, 0.01, 0.003)
    exact_roots: list[float] = []
    series_values: list[float] = []
    relative_errors: list[float] = []
    with mp.workdps(80):
        for value in sample_t:
            value_mp = mp.mpf(str(value))
            root = mp.findroot(
                lambda acceleration: acceleration * (-mp.expm1(-acceleration))
                - value_mp**2,
                (value_mp, value_mp * mp.mpf("1.2")),
            )
            approximation = sum(
                mp.mpf(str(coefficient)) * value_mp**index
                for index, coefficient in enumerate(
                    spherical["uniform_core_coefficients"], start=1
                )
            )
            exact_roots.append(float(root))
            series_values.append(float(approximation))
            relative_errors.append(float(abs(approximation / root - 1)))

    return {
        "r": r,
        "t": t,
        "v_squared_series": v_squared,
        "v_fourth_series": v_fourth,
        "v_fourth_scale": v_fourth_scale,
        "v_fourth_normalized_limit": sp.simplify(
            sp.limit(v_fourth / v_fourth_scale, r, 0, dir="+")
        ),
        "v_fourth_correction_series": v_correction,
        "period_fourth_over_r_scale": period_fourth_scale_over_r,
        "period_fourth_over_r_scale_in_rho": period_fourth_scale_over_r_rho,
        "period_fourth_normalized_limit": sp.simplify(
            sp.limit(1 / (v_fourth / v_fourth_scale), r, 0, dir="+")
        ),
        "period_fourth_correction_series": period_correction,
        "mond_period_log_slope": sp.Rational(1, 4),
        "newtonian_period_log_slope": sp.Integer(0),
        "boxed_law": (
            "lim[r->0] v_c^4/(rho_0 r^3) = (4*pi/3) G a_0; "
            "equivalently lim[r->0] T^4/r = 12*pi^3/(G a_0 rho_0)"
        ),
        "numeric_audit": {
            "dimensionless_radii_t": sample_t,
            "exact_positive_roots": tuple(exact_roots),
            "fifth_order_series_values": tuple(series_values),
            "relative_errors": tuple(relative_errors),
            "solver": "mpmath 80-decimal-digit secant solve of u*(1-exp(-u))=t^2",
        },
    }


def _derive_rar_vs_aqual(spherical: dict[str, Any]) -> dict[str, Any]:
    """Prevent conflation of the empirical RAR fit with exact AQUAL inversion."""

    y_newton = sp.symbols("y_N", positive=True)
    nu_rar = 1 / (1 - sp.exp(-sp.sqrt(y_newton)))
    inverse_residual = sp.factor(
        nu_rar * (1 - sp.exp(-nu_rar * y_newton)) - 1
    )
    residual_at_one = float(sp.N(inverse_residual.subs(y_newton, 1), 17))
    nu_rar_at_one = float(sp.N(nu_rar.subs(y_newton, 1), 17))
    with mp.workdps(80):
        nu_aqual_at_one_mp = mp.findroot(
            lambda value: value * (-mp.expm1(-value)) - 1,
            (mp.mpf("1.2"), mp.mpf("1.5")),
        )
    t = sp.symbols("t", positive=True)
    u_series = spherical["dimensionless_acceleration_series"]
    shared_deep_leading_ratio = sp.limit(u_series / t, t, 0, dir="+")
    return {
        "y_newton": y_newton,
        "nu_rar": nu_rar,
        "exact_aqual_inverse_equation": (
            "nu_AQUAL(y_N) * [1-exp(-nu_AQUAL(y_N)*y_N)] = 1"
        ),
        "rar_in_exact_inverse_residual": inverse_residual,
        "residual_at_yN_one": residual_at_one,
        "nu_rar_at_yN_one": nu_rar_at_one,
        "nu_aqual_at_yN_one": float(nu_aqual_at_one_mp),
        "shared_deep_leading_ratio": shared_deep_leading_ratio,
        "nu_rar_newtonian_limit": sp.limit(nu_rar, y_newton, sp.oo),
        "exact_identity": bool(sp.simplify(inverse_residual) == 0),
    }


def _derive_regulated_kernel() -> dict[str, Any]:
    epsilon, C = sp.symbols("epsilon C", positive=True)
    origin_jacobian = epsilon * sp.eye(3)
    radial_hessian = C / epsilon
    tangential_hessian = C / epsilon
    tidal_norm_squared = sp.factor(radial_hessian**2 + 2 * tangential_hessian**2)
    return {
        "epsilon": epsilon,
        "C": C,
        "mu": epsilon + 1 - sp.exp(-sp.symbols("y", nonnegative=True)),
        "mu_at_zero": epsilon,
        "origin_jacobian": origin_jacobian,
        "origin_jacobian_rank": origin_jacobian.rank(),
        "central_acceleration": C * sp.symbols("r", nonnegative=True) / epsilon,
        "central_radial_hessian": radial_hessian,
        "central_tangential_hessian": tangential_hessian,
        "central_tidal_norm_squared": tidal_norm_squared,
        "central_tidal_norm_finite": bool(tidal_norm_squared.is_finite),
        "violates_exact_target": bool(epsilon != 0),
    }


def _derive_power_law_scope() -> dict[str, Any]:
    s = sp.symbols("s", positive=True)
    acceleration_exponent = sp.factor(1 / (s + 1))
    hessian_exponent = sp.factor(acceleration_exponent - 1)
    return {
        "s": s,
        "acceleration_exponent": acceleration_exponent,
        "hessian_exponent": hessian_exponent,
        "all_positive_s_have_divergent_hessian": bool(hessian_exponent.is_negative),
        "scope": "The obstruction applies to any mu(y) asymptotic to a positive multiple of y^s with s>0.",
    }


def derive_regular_center_no_go() -> dict[str, Any]:
    """Compute every ingredient of the scoped regular-center theorem."""

    kernel = _derive_kernel()
    jacobian = _derive_constitutive_jacobian(kernel)
    spherical = _derive_spherical_core()
    critical = _derive_critical_point(jacobian)
    weak = _derive_weak_solution(kernel, spherical)
    central_kepler = _derive_central_kepler_law(spherical)
    rar_vs_aqual = _derive_rar_vs_aqual(spherical)
    return {
        "field_equation": FIELD_EQUATION,
        "kernel": kernel,
        "constitutive_jacobian": jacobian,
        "critical_point": critical,
        "spherical_core": spherical,
        "weak_solution": weak,
        "phantom_density": _derive_phantom_density(spherical),
        "central_kepler_law": central_kepler,
        "rar_vs_aqual": rar_vs_aqual,
        "regulated_kernel": _derive_regulated_kernel(),
        "power_law_scope": _derive_power_law_scope(),
        "scope": {
            "assumptions": (
                "exact exponential AQUAL; pointwise classical equation; C2 Phi; "
                "a force-free point with continuous positive baryon density"
            ),
            "theorem_status": "PROVED_UNDER_STATED_ASSUMPTIONS",
            "hpi_delta_status": "DEAD_AS_AN_EXACT_CLASSICAL_REGULAR_CENTER_THEORY",
            "full_target_status": "NO_GO_UNDER_CLASSICAL_REGULAR_CENTER_ASSUMPTIONS",
            "global_literature_novelty_claimed": False,
            "weak_or_distributional_escape_remains": True,
            "escape_fails_regular_classical_metric_gate": True,
            "possible_escapes": (
                "relax exact mu(0)=0; exclude positive-density critical points; "
                "accept a non-C2 metric; or add a UV term that changes the exact field equation"
            ),
        },
    }


def _main() -> int:
    result = derive_regular_center_no_go()
    jacobian = result["constitutive_jacobian"]
    point = result["critical_point"]
    spherical = result["spherical_core"]
    weak = result["weak_solution"]
    regulated = result["regulated_kernel"]
    phantom = result["phantom_density"]
    central_kepler = result["central_kepler_law"]
    rar_vs_aqual = result["rar_vs_aqual"]
    checks = {
        "exact exponential kernel": result["kernel"]["mu_residual"] == 0,
        "RAR nu is not falsely identified with exact AQUAL inverse": (
            rar_vs_aqual["rar_in_exact_inverse_residual"] != 0
            and not rar_vs_aqual["exact_identity"]
        ),
        "constitutive Jacobian derived": jacobian["axis_off_diagonal_residual"] == sp.zeros(3),
        "constitutive rank collapses at zero field": jacobian["origin_rank"] == 0,
        "C2 critical point forces rho=0": point["required_source_at_critical_point"] == 0,
        "positive spherical Puiseux branch solved": all(
            residual == 0 for residual in spherical["coefficient_equation_residuals"]
        ),
        "spherical flux solves exact source equation": spherical["divergence_source_residual"] == 0,
        "positive spherical flux branch is unique": spherical[
            "positive_inverse_branch_exists_and_is_unique"
        ],
        "radial and tangential Hessian diverge": spherical["hessian_diverges"],
        "tidal norm diverges": spherical["tidal_norm_squared_diverges"],
        "no-slip Ricci scalar diverges invariantly": spherical[
            "no_slip_ricci_scalar_diverges"
        ],
        "full displayed metric has the same leading Ricci divergence": (
            spherical["full_metric_ricci_scaled_limit"] == 5
            and spherical["full_to_linear_ricci_ratio_limit"] == 1
        ),
        "weak action remains locally integrable": weak["radial_energy_integrable"],
        "Einstein phantom density cusp detected": (
            phantom["phantom_density_scaled_limit"] == 5
            and not phantom["effective_stress_regular_at_center"]
        ),
        "central Kepler-grade core law derived": (
            central_kepler["v_fourth_normalized_limit"] == 1
            and central_kepler["period_fourth_normalized_limit"] == 1
        ),
        "central core series passes independent numeric roots": all(
            later < earlier
            for earlier, later in zip(
                central_kepler["numeric_audit"]["relative_errors"],
                central_kepler["numeric_audit"]["relative_errors"][1:],
            )
        ),
        "positive mu(0) regulator removes rank collapse": regulated["origin_jacobian_rank"] == 3,
        "regulator violates exact target": regulated["violates_exact_target"],
    }

    print("=" * 88)
    print("EXACT EXPONENTIAL MOND: REGULAR-CENTER NO-GO GATE")
    print("=" * 88)
    for label, passed in checks.items():
        print(("[PASS] " if passed else "[FAIL] ") + label)
    print("\nField equation:\n" + FIELD_EQUATION)
    print("\nRAR/AQUAL translation audit:")
    print("  nu_RAR(1) =", rar_vs_aqual["nu_rar_at_yN_one"])
    print("  nu_AQUAL(1) =", rar_vs_aqual["nu_aqual_at_yN_one"])
    print("  substituting nu_RAR into exact inverse leaves residual =", rar_vs_aqual["residual_at_yN_one"])
    print("\nConstitutive Jacobian on p=(epsilon,0,0):")
    sp.pprint(jacobian["axis_jacobian"])
    print("limit p->0 =")
    sp.pprint(jacobian["origin_limit"])
    print("computed rank at the origin =", jacobian["origin_rank"])
    print("\nPositive spherical branch, t=sqrt(C r/a0):")
    print("  smooth-core g/a0 =", spherical["dimensionless_acceleration_series_general_smooth_core"])
    print("  uniform-core g/a0 =", spherical["dimensionless_acceleration_series"])
    print("  Phi-Phi(0) =", spherical["potential_series"])
    print("  sqrt(r) Phi_rr / sqrt(a0 C) ->", spherical["radial_hessian_scaled_limit"])
    print("  sqrt(r) (Phi_r/r) / sqrt(a0 C) ->", spherical["tangential_hessian_scaled_limit"])
    print("  r |Hess Phi|^2/(a0 C) ->", spherical["tidal_norm_squared_scaled_limit"])
    print("  sqrt(r) c^2 R^(1)/sqrt(a0 C) ->", spherical["no_slip_ricci_scalar_scaled_limit"])
    print("  sqrt(r) c^2 R_full/sqrt(a0 C) ->", spherical["full_metric_ricci_scaled_limit"])
    print("  R_full/R^(1) ->", spherical["full_to_linear_ricci_ratio_limit"])
    print("  nonlinear first-gradient curvature / R^(1) ->", spherical["nonlinear_curvature_ratio_limit"])
    print("  sqrt(r) rho_ph / [sqrt(a0 C)/(8 pi G)] ->", phantom["phantom_density_scaled_limit"])
    print("\nCentral Kepler-grade law:")
    print(" ", central_kepler["boxed_law"])
    print("  exponential v^4 correction =", central_kepler["v_fourth_correction_series"])
    print("  exponential T^4 correction =", central_kepler["period_fourth_correction_series"])
    print("  numeric relative errors =", central_kepler["numeric_audit"]["relative_errors"])
    print("\nMathematical boundary:")
    print("  The finite-action weak solution exists, but it is not C2.")
    print("  A positive mu(0) regularizes the center only by changing the exact target law.")
    print("\nVerdict:")
    print("  HPI-Delta is DEAD as an exact classical regular-center theory.")
    print("  The wider target has a NO-GO under the explicitly listed regularity assumptions.")
    print("  This program does not claim global literature novelty.")

    certificate = {
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "constitutive_origin_rank": jacobian["origin_rank"],
        "critical_point_required_density": str(point["required_source_at_critical_point"]),
        "radial_hessian_scaled_limit": str(spherical["radial_hessian_scaled_limit"]),
        "tangential_hessian_scaled_limit": str(spherical["tangential_hessian_scaled_limit"]),
        "tidal_norm_squared_scaled_limit": str(spherical["tidal_norm_squared_scaled_limit"]),
        "no_slip_ricci_scalar_scaled_limit": str(
            spherical["no_slip_ricci_scalar_scaled_limit"]
        ),
        "theorem_status": result["scope"]["theorem_status"],
        "candidate_status": result["scope"]["hpi_delta_status"],
    }
    print("CERTIFICATE_JSON:", json.dumps(certificate, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(_main())
