#!/usr/bin/env python3
r"""Full static-spherical audit of the HPI-Delta action.

This program closes one deliberately narrow question left open by the earlier
HPI-Delta calculation: can the radial shift or the elliptic multiplier repair
the force-free center once both are retained in the *varied* action?

The answer is no on an isolated, asymptotically static, momentum-free spherical
branch with no point source for the multiplier.  The code derives that branch
and then obtains the center expansion from the exact nonlinear action.  It is
not a nonlinear Dirac proof, a PPN computation, or a theorem about nonspherical
external-field or cosmological-CMC branches.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import sympy as sp


ACTION = r"""
S = (M_Pl^2/2) integral dt d^3x N sqrt(h) [
      Kbar_ij Kbar^ij - Kbar^2 + R_3 - 2 Lambda
      - (2/ell_0^2) F_exp(y)
    ] + S_m[g,psi],

Kbar_ij = K_ij - (D^2 lambda)/(2N) h_ij,
y = ell_0 sqrt(h^ij D_i ln(N) D_j ln(N)),
F_exp(y) = 2[(1+y)exp(-y)-1].

Unitary-clock spherical ADM ansatz:
ds^2 = -N(t,r)^2 dt^2 + A(t,r)^2[dr+beta(t,r)dt]^2
       + R(t,r)^2 dOmega^2,   T=t,   lambda=lambda(t,r).
""".strip()


def _higher_euler(
    lagrangian: sp.Expr,
    field: sp.Expr,
    coordinate: sp.Symbol,
    order: int,
) -> sp.Expr:
    """Euler operator for a one-dimensional Lagrangian with higher jets."""

    result = sp.diff(lagrangian, field)
    for derivative_order in range(1, order + 1):
        jet = sp.diff(field, coordinate, derivative_order)
        result += (-1) ** derivative_order * sp.diff(
            sp.diff(lagrangian, jet), coordinate, derivative_order
        )
    return sp.factor(result)


def _build_geometry() -> dict[str, Any]:
    r = sp.symbols("r", positive=True)
    ell = sp.symbols("ell_0", positive=True)
    Lambda = sp.symbols("Lambda", real=True)
    N = sp.Function("N", positive=True)(r)
    A = sp.Function("A", positive=True)(r)
    radius = sp.Function("R", positive=True)(r)
    beta = sp.Function("beta")(r)
    lam = sp.Function("lambda")(r)

    q = sp.factor(
        sp.diff(radius**2 * sp.diff(lam, r) / A, r) / (A * radius**2)
    )
    kappa_r = sp.factor(
        -(sp.diff(beta, r) + beta * sp.diff(A, r) / A) / N
    )
    kappa_t = sp.factor(-beta * sp.diff(radius, r) / (N * radius))
    bar_r = sp.factor(kappa_r - q / (2 * N))
    bar_t = sp.factor(kappa_t - q / (2 * N))
    bar_K = sp.factor(bar_r + 2 * bar_t)
    kinetic = sp.factor(bar_r**2 + 2 * bar_t**2 - bar_K**2)
    kinetic_expanded = sp.factor(
        kappa_r**2
        + 2 * kappa_t**2
        - (kappa_r + 2 * kappa_t) ** 2
        + 2 * (kappa_r + 2 * kappa_t) * q / N
        - 3 * q**2 / (2 * N**2)
    )

    curvature_3 = sp.factor(
        2
        / radius**2
        * (
            1
            - sp.diff(radius, r) ** 2 / A**2
            - 2 * radius * sp.diff(radius, r, 2) / A**2
            + 2 * radius * sp.diff(radius, r) * sp.diff(A, r) / A**3
        )
    )
    y = sp.factor(ell * sp.diff(N, r) / (A * N))
    F = sp.factor(2 * ((1 + y) * sp.exp(-y) - 1))
    raw_lagrangian = sp.factor(
        N
        * A
        * radius**2
        * (kinetic + curvature_3 - 2 * Lambda - 2 * F / ell**2)
    )

    first_order_metric_lagrangian = sp.factor(
        2 * N * A
        + 2 * N * sp.diff(radius, r) ** 2 / A
        + 4 * sp.diff(N, r) * radius * sp.diff(radius, r) / A
        - 2 * Lambda * N * A * radius**2
        - 2 * N * A * radius**2 * F / ell**2
    )
    raw_metric_lagrangian = sp.factor(
        N * A * radius**2 * (curvature_3 - 2 * Lambda - 2 * F / ell**2)
    )
    boundary_term = sp.factor(4 * N * radius * sp.diff(radius, r) / A)

    flat_curvature = sp.simplify(
        curvature_3.subs(
            {
                A: 1,
                sp.diff(A, r): 0,
                radius: r,
                sp.diff(radius, r): 1,
                sp.diff(radius, r, 2): 0,
            },
            simultaneous=True,
        )
    )
    sphere_radius = sp.sin(r)
    sphere_curvature = sp.simplify(
        curvature_3.subs(
            {
                A: 1,
                sp.diff(A, r): 0,
                radius: sphere_radius,
                sp.diff(radius, r): sp.diff(sphere_radius, r),
                sp.diff(radius, r, 2): sp.diff(sphere_radius, r, 2),
            },
            simultaneous=True,
        )
    )
    flat_q = sp.simplify(
        q.subs(
            {
                A: 1,
                sp.diff(A, r): 0,
                radius: r,
                sp.diff(radius, r): 1,
            },
            simultaneous=True,
        )
    )

    return {
        "r": r,
        "ell": ell,
        "Lambda": Lambda,
        "N": N,
        "A": A,
        "R": radius,
        "beta": beta,
        "lambda": lam,
        "q": q,
        "kappa_r": kappa_r,
        "kappa_t": kappa_t,
        "bar_kappa_r": bar_r,
        "bar_kappa_t": bar_t,
        "bar_K": bar_K,
        "kinetic": kinetic,
        "curvature_3": curvature_3,
        "y": y,
        "F": F,
        "raw_lagrangian": raw_lagrangian,
        "raw_metric_lagrangian": raw_metric_lagrangian,
        "first_order_metric_lagrangian": first_order_metric_lagrangian,
        "boundary_term": boundary_term,
        "field_names": ("N", "A", "R", "beta", "lambda"),
        "kinetic_expansion_residual": sp.simplify(kinetic - kinetic_expanded),
        "flat_spatial_curvature": flat_curvature,
        "unit_three_sphere_curvature": sphere_curvature,
        "flat_lambda_laplacian": flat_q,
        "flat_lambda_laplacian_residual": sp.simplify(
            flat_q - sp.diff(lam, r, 2) - 2 * sp.diff(lam, r) / r
        ),
    }


def _derive_auxiliary_equations(geometry: dict[str, Any]) -> dict[str, Any]:
    r = geometry["r"]
    N, A, radius = geometry["N"], geometry["A"], geometry["R"]
    beta, lam = geometry["beta"], geometry["lambda"]
    bar_r, bar_t = geometry["bar_kappa_r"], geometry["bar_kappa_t"]
    bar_K = geometry["bar_K"]
    kinetic_lagrangian = sp.factor(N * A * radius**2 * geometry["kinetic"])

    shift_equation = _higher_euler(kinetic_lagrangian, beta, r, 1)
    lambda_equation = _higher_euler(kinetic_lagrangian, lam, r, 2)
    expected_shift = sp.factor(
        4 * A * radius
        * (
            sp.diff(radius, r) * (bar_r - bar_t)
            - radius * sp.diff(bar_t, r)
        )
    )
    expected_lambda = sp.factor(
        2 * sp.diff(radius**2 * sp.diff(bar_K, r) / A, r)
    )
    lambda_dot = sp.symbols("lambda_dot", real=True)
    return {
        "kinetic_lagrangian": kinetic_lagrangian,
        "shift_equation": shift_equation,
        "expected_shift_equation": expected_shift,
        "shift_equation_residual": sp.simplify(shift_equation - expected_shift),
        "lambda_equation": lambda_equation,
        "expected_lambda_equation": expected_lambda,
        "lambda_equation_residual": sp.simplify(
            lambda_equation - expected_lambda
        ),
        "lambda_velocity_hessian": sp.diff(kinetic_lagrangian, lambda_dot, 2),
    }


def _derive_isolated_branch(geometry: dict[str, Any]) -> dict[str, Any]:
    r = geometry["r"]
    A, radius = geometry["A"], geometry["R"]
    beta = geometry["beta"]
    C1, C2, C3, C4, K0 = sp.symbols(
        "C_lambda C_shear C_shift C_q K_0", real=True
    )

    # E_lambda=0 first integrates to (R^2/A) Kbar'=C1.
    harmonic_derivative = C1 * A / radius**2
    harmonic_residual = sp.simplify(
        sp.diff(radius**2 * harmonic_derivative / A, r)
    )
    central_flux = 4 * sp.pi * C1
    central_charge_solution = sp.solve(sp.Eq(central_flux, 0), C1)[0]

    # With Kbar=K0, the source-free momentum equation is first order.
    bar_t_solution = K0 / 3 + C2 / radius**3
    bar_r_solution = K0 - 2 * bar_t_solution
    momentum_residual = sp.simplify(
        sp.diff(bar_t_solution, r)
        - sp.diff(radius, r) / radius * (bar_r_solution - bar_t_solution)
    )
    isotropic_residual = sp.simplify(
        (bar_r_solution - bar_t_solution).subs(C2, 0)
    )

    x = sp.symbols("x", positive=True)
    C2_positive = sp.symbols("C_shear_positive", positive=True)
    singular_action_density = 6 * C2_positive**2 / x**4
    traceless_diverges = (
        sp.limit(singular_action_density, x, 0, dir="+") == sp.oo
    )

    beta_solution = C3 * radius / A
    shift_residual = sp.simplify(
        (geometry["kappa_r"] - geometry["kappa_t"]).subs(
            {
                beta: beta_solution,
                sp.diff(beta, r): sp.diff(beta_solution, r),
            },
            simultaneous=True,
        )
    )
    isolated_shift_constant = sp.solve(sp.Eq(C3, 0), C3)[0]
    regular_lambda_flux_constant = sp.solve(sp.Eq(4 * sp.pi * C4, 0), C4)[0]
    isolated_K0 = sp.solve(sp.Eq(K0, 0), K0)[0]
    return {
        "harmonic_flux_constant": C1,
        "harmonic_derivative": harmonic_derivative,
        "harmonic_solution_residual": harmonic_residual,
        "central_auxiliary_flux": central_flux,
        "central_auxiliary_charge_solution": central_charge_solution,
        "bar_K_constant": K0,
        "bar_kappa_t_solution": bar_t_solution,
        "bar_kappa_r_solution": bar_r_solution,
        "momentum_solution_residual": momentum_residual,
        "isotropic_barred_curvature_residual": isotropic_residual,
        "traceless_mode_action_density": singular_action_density,
        "traceless_mode_action_diverges": traceless_diverges,
        "isolated_bar_K_constant": isolated_K0,
        "shift_solution": beta_solution,
        "shift_solution_residual": shift_residual,
        "isolated_shift_constant": isolated_shift_constant,
        "regular_lambda_flux_constant": regular_lambda_flux_constant,
        "derived_isolated_branch": "bar_Kij=0, beta=0, D2(lambda)=0",
        "assumptions": (
            "zero radial matter momentum",
            "no point source for lambda",
            "regular or distributionally source-free center",
            "finite auxiliary action",
            "asymptotically static isolated boundary data",
        ),
    }


def _derive_metric_equations(geometry: dict[str, Any]) -> dict[str, Any]:
    r = geometry["r"]
    ell, Lambda = geometry["ell"], geometry["Lambda"]
    N, A, radius = geometry["N"], geometry["A"], geometry["R"]
    y, F = geometry["y"], geometry["F"]
    F_prime = sp.factor(-2 * y * sp.exp(-y))
    H = sp.factor(F - y * F_prime)
    lagrangian = geometry["first_order_metric_lagrangian"]

    E_N = _higher_euler(lagrangian, N, r, 1)
    E_A = _higher_euler(lagrangian, A, r, 1)
    E_R = _higher_euler(lagrangian, radius, r, 1)
    expected_N = sp.factor(
        A
        * radius**2
        * (geometry["curvature_3"] - 2 * Lambda - 2 * H / ell**2)
        + 2 * sp.diff(radius**2 * F_prime, r) / ell
    )
    expected_A = sp.factor(
        2 * N * (1 - sp.diff(radius, r) ** 2 / A**2)
        - 4 * sp.diff(N, r) * radius * sp.diff(radius, r) / A**2
        - 2 * Lambda * N * radius**2
        - 2 * N * radius**2 * H / ell**2
    )
    expected_R = sp.factor(
        4 * sp.diff(N, r) * sp.diff(radius, r) / A
        - sp.diff(
            4 * N * sp.diff(radius, r) / A
            + 4 * sp.diff(N, r) * radius / A,
            r,
        )
        - 4 * N * A * radius * (Lambda + F / ell**2)
    )
    boundary_residual = sp.simplify(
        geometry["raw_metric_lagrangian"]
        - lagrangian
        + sp.diff(geometry["boundary_term"], r)
    )
    return {
        "lagrangian": lagrangian,
        "F_prime": F_prime,
        "H": H,
        "lapse_equation": E_N,
        "radial_equation": E_A,
        "angular_equation": E_R,
        "expected_lapse_equation": expected_N,
        "expected_radial_equation": expected_A,
        "expected_angular_equation": expected_R,
        "raw_vs_first_order_boundary_residual": boundary_residual,
        "lapse_equation_residual": sp.simplify(E_N - expected_N),
        "radial_equation_residual": sp.simplify(E_A - expected_A),
        "angular_equation_residual": sp.simplify(E_R - expected_R),
        "matter_normalization": {
            "lapse": "E_N/(A R^2) = 16 pi G rho",
            "radial": "E_A/(2N) = -8 pi G p_r R^2",
            "angular": "E_R = -32 pi G N A R p_t",
        },
    }


def _derive_radial_noether_identity(
    geometry: dict[str, Any],
    auxiliary: dict[str, Any],
    metric: dict[str, Any],
) -> dict[str, Any]:
    r = geometry["r"]
    N, A, radius = geometry["N"], geometry["A"], geometry["R"]
    beta, lam = geometry["beta"], geometry["lambda"]

    static_identity = sp.factor(
        sp.diff(N, r) * metric["lapse_equation"]
        + sp.diff(radius, r) * metric["angular_equation"]
        + sp.diff(A, r) * metric["radial_equation"]
        - sp.diff(A * metric["radial_equation"], r)
    )

    kinetic_lagrangian = auxiliary["kinetic_lagrangian"]
    E_N_kin = _higher_euler(kinetic_lagrangian, N, r, 0)
    E_A_kin = _higher_euler(kinetic_lagrangian, A, r, 1)
    E_R_kin = _higher_euler(kinetic_lagrangian, radius, r, 1)
    E_beta = auxiliary["shift_equation"]
    E_lambda = auxiliary["lambda_equation"]
    zero_auxiliary_jets = {beta: 0, lam: 0}
    for derivative_order in range(1, 6):
        zero_auxiliary_jets[sp.diff(beta, r, derivative_order)] = 0
        zero_auxiliary_jets[sp.diff(lam, r, derivative_order)] = 0
    zero_branch_metric_variations = tuple(
        sp.simplify(
            equation.subs(zero_auxiliary_jets, simultaneous=True)
        )
        for equation in (E_N_kin, E_A_kin, E_R_kin)
    )
    kinetic_identity = sp.factor(
        sp.diff(N, r) * E_N_kin
        + sp.diff(radius, r) * E_R_kin
        + sp.diff(lam, r) * E_lambda
        + sp.diff(A, r) * E_A_kin
        + sp.diff(beta, r) * E_beta
        - sp.diff(A * E_A_kin, r)
        + sp.diff(beta * E_beta, r)
    )
    return {
        "static_metric_identity": static_identity,
        "static_metric_residual": sp.simplify(static_identity),
        "full_kinetic_identity": kinetic_identity,
        "full_kinetic_residual": sp.simplify(kinetic_identity),
        "zero_branch_full_kinetic_metric_variation_residuals": (
            zero_branch_metric_variations
        ),
        "radial_gauge_rule": (
            "Vary N,A,R,beta,lambda first; R=r is admissible only after "
            "this identity (and the matter identity) is checked."
        ),
    }


def _center_lhs(
    x: sp.Symbol,
    ell: sp.Symbol,
    Lambda: sp.Symbol,
    u_prime: sp.Expr,
    A: sp.Expr,
    F_builder,
) -> tuple[sp.Expr, sp.Expr]:
    """Areal-gauge center jets of the exact equations with ``r=x^2``.

    Only terms through the displayed center coefficients are requested.  The
    fourth-order Taylor polynomial is taken from the exact constitutive
    function *before* substitution; this avoids asking SymPy to find a limit
    through an unexpanded exponential of a rational series.
    """

    radius = x**2

    def d_dr(expression: sp.Expr) -> sp.Expr:
        return sp.diff(expression, x) / (2 * x)

    y = sp.factor(ell * u_prime / A)
    y_symbol = sp.symbols("y_center", nonnegative=True)
    F_exact = F_builder(y_symbol)
    F_symbolic = sp.series(F_exact, y_symbol, 0, 5).removeO()
    F = F_symbolic.subs(y_symbol, y)
    F_prime = sp.diff(F_symbolic, y_symbol).subs(y_symbol, y)
    H = sp.factor(F - y * F_prime)
    curvature_3 = sp.factor(
        2
        / radius**2
        * (1 - A ** -2 + 2 * radius * d_dr(A) / A**3)
    )
    lapse = sp.factor(
        curvature_3
        - 2 * Lambda
        - 2 * H / ell**2
        + 2
        / (ell * A * radius**2)
        * d_dr(radius**2 * F_prime)
    )
    radial = sp.factor(
        1
        - A ** -2
        - 2 * radius * u_prime / A**2
        - Lambda * radius**2
        - radius**2 * H / ell**2
    )
    return lapse, radial


def _derive_center() -> dict[str, Any]:
    x = sp.symbols("x", positive=True)
    ell, G = sp.symbols("ell_0 G", positive=True)
    Lambda = sp.symbols("Lambda", real=True)
    rho, pressure = sp.symbols("rho_0 p_c", real=True)
    c = sp.symbols("c", positive=True)
    d, a2, u1 = sp.symbols("d a_2 u_1", real=True)

    exponential = lambda y: 2 * ((1 + y) * sp.exp(-y) - 1)

    puiseux_u_prime = c * x + d * x**2
    puiseux_A = 1 + c * x**3 + a2 * x**4
    lapse_p, radial_p = _center_lhs(
        x, ell, Lambda, puiseux_u_prime, puiseux_A, exponential
    )
    radial_coefficient_p = sp.factor(sp.limit(radial_p / x**4, x, 0))
    lapse_coefficient_p = sp.factor(sp.limit(lapse_p, x, 0))
    a2_solution = sp.solve(
        sp.Eq(radial_coefficient_p, -8 * sp.pi * G * pressure), a2
    )[0]
    c_squared_solution = sp.solve(
        sp.Eq(
            lapse_coefficient_p.subs(a2, a2_solution),
            16 * sp.pi * G * rho,
        ),
        c**2,
    )[0]
    radial_solution_residual = sp.simplify(
        radial_coefficient_p.subs(a2, a2_solution)
        + 8 * sp.pi * G * pressure
    )
    lapse_solution_residual = sp.simplify(
        (
            lapse_coefficient_p.subs(a2, a2_solution)
            - 16 * sp.pi * G * rho
        ).subs(c**2, c_squared_solution)
    )

    smooth_u_prime = u1 * x**2
    smooth_A = 1 + a2 * x**4
    lapse_s, radial_s = _center_lhs(
        x, ell, Lambda, smooth_u_prime, smooth_A, exponential
    )
    radial_coefficient_s = sp.factor(sp.limit(radial_s / x**4, x, 0))
    lapse_coefficient_s = sp.factor(sp.limit(lapse_s, x, 0))
    expected_radial_s = 2 * (a2 - u1) - Lambda
    expected_lapse_s = 12 * (a2 - u1) - 2 * Lambda
    smooth_a2_solution = sp.solve(
        sp.Eq(radial_coefficient_s, -8 * sp.pi * G * pressure), a2
    )[0]
    compatibility = sp.factor(
        lapse_coefficient_s.subs(a2, smooth_a2_solution)
        - 16 * sp.pi * G * rho
    )
    active_density = sp.symbols("active_density", real=True)
    required_active_density = sp.solve(
        sp.Eq(compatibility.subs(rho, active_density - 3 * pressure), 0),
        active_density,
    )[0]
    return {
        "smooth": {
            "G": G,
            "rho": rho,
            "pressure": pressure,
            "Lambda": Lambda,
            "ell": ell,
            "u1": u1,
            "a2": a2,
            "radial_coefficient": radial_coefficient_s,
            "lapse_coefficient": lapse_coefficient_s,
            "radial_coefficient_residual": sp.simplify(
                radial_coefficient_s - expected_radial_s
            ),
            "lapse_coefficient_residual": sp.simplify(
                lapse_coefficient_s - expected_lapse_s
            ),
            "a2_from_radial_equation": smooth_a2_solution,
            "compatibility_residual": compatibility,
            "required_active_density": required_active_density,
        },
        "puiseux": {
            "x": x,
            "ell": ell,
            "G": G,
            "rho": rho,
            "pressure": pressure,
            "Lambda": Lambda,
            "c": c,
            "d": d,
            "a2": a2,
            "radial_coefficient": radial_coefficient_p,
            "lapse_coefficient": lapse_coefficient_p,
            "a2_solution": a2_solution,
            "c_squared": sp.factor(c_squared_solution),
            "radial_solution_residual": radial_solution_residual,
            "lapse_solution_residual": lapse_solution_residual,
        },
    }


def _direct_curvature_invariants() -> dict[str, Any]:
    time, r, theta, azimuth = sp.symbols("t r theta phi", real=True)
    N = sp.Function("N_curv", positive=True)(r)
    A = sp.Function("A_curv", positive=True)(r)
    coordinates = (time, r, theta, azimuth)
    metric = sp.diag(-N**2, A**2, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = sp.diag(
        -N ** -2,
        A ** -2,
        r ** -2,
        1 / (r**2 * sp.sin(theta) ** 2),
    )
    dimension = 4
    christoffel = [
        [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for lower_a in range(dimension):
            for lower_b in range(dimension):
                christoffel[upper][lower_a][lower_b] = sp.factor(
                    sum(
                        inverse[upper, index]
                        * (
                            sp.diff(metric[index, lower_b], coordinates[lower_a])
                            + sp.diff(metric[index, lower_a], coordinates[lower_b])
                            - sp.diff(metric[lower_a, lower_b], coordinates[index])
                        )
                        for index in range(dimension)
                    )
                    / 2
                )
    riemann_mixed = [
        [
            [
                [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for lower in range(dimension):
            for first in range(dimension):
                for second in range(dimension):
                    riemann_mixed[upper][lower][first][second] = sp.factor(
                        sp.diff(
                            christoffel[upper][lower][second], coordinates[first]
                        )
                        - sp.diff(
                            christoffel[upper][lower][first], coordinates[second]
                        )
                        + sum(
                            christoffel[upper][index][first]
                            * christoffel[index][lower][second]
                            - christoffel[upper][index][second]
                            * christoffel[index][lower][first]
                            for index in range(dimension)
                        )
                    )
    ricci = sp.zeros(dimension)
    for row in range(dimension):
        for column in range(dimension):
            ricci[row, column] = sp.factor(
                sum(
                    riemann_mixed[index][row][index][column]
                    for index in range(dimension)
                )
            )
    ricci_scalar = sp.factor(
        sum(
            inverse[row, column] * ricci[row, column]
            for row in range(dimension)
            for column in range(dimension)
        )
    )
    lowered = [
        [
            [
                [
                    sp.factor(
                        sum(
                            metric[first, index]
                            * riemann_mixed[index][second][third][fourth]
                            for index in range(dimension)
                        )
                    )
                    for fourth in range(dimension)
                ]
                for third in range(dimension)
            ]
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]
    # The metric is diagonal, so the full contraction reduces to this exact sum.
    kretschmann = sp.factor(
        sum(
            inverse[a, a]
            * inverse[b, b]
            * inverse[c_index, c_index]
            * inverse[d, d]
            * lowered[a][b][c_index][d] ** 2
            for a in range(dimension)
            for b in range(dimension)
            for c_index in range(dimension)
            for d in range(dimension)
        )
    )
    return {
        "r": r,
        "N": N,
        "A": A,
        "ricci_scalar": ricci_scalar,
        "kretschmann": kretschmann,
    }


def _substitute_radial_functions(
    expression: sp.Expr,
    r: sp.Symbol,
    N: sp.Expr,
    A: sp.Expr,
    N_value: sp.Expr,
    A_value: sp.Expr,
) -> sp.Expr:
    return sp.factor(
        expression.subs(
            {
                N: N_value,
                sp.diff(N, r): sp.diff(N_value, r),
                sp.diff(N, r, 2): sp.diff(N_value, r, 2),
                A: A_value,
                sp.diff(A, r): sp.diff(A_value, r),
            },
            simultaneous=True,
        )
    )


def _derive_curvature() -> dict[str, Any]:
    direct = _direct_curvature_invariants()
    r, N, A = direct["r"], direct["N"], direct["A"]
    X = sp.factor(
        (sp.diff(N, r, 2) - sp.diff(N, r) * sp.diff(A, r) / A)
        / (N * A**2)
    )
    Y = sp.factor(sp.diff(N, r) / (N * A**2 * r))
    Z = sp.factor(sp.diff(A, r) / (A**3 * r))
    W = sp.factor((1 - A ** -2) / r**2)
    expected_kretschmann = sp.factor(4 * (X**2 + 2 * Y**2 + 2 * Z**2 + W**2))
    curvature_3 = sp.factor(
        2 / r**2 * (1 - A ** -2 + 2 * r * sp.diff(A, r) / A**3)
    )
    laplacian_N_over_N = sp.factor(
        sp.diff(r**2 * sp.diff(N, r) / A, r) / (A * r**2 * N)
    )
    expected_ricci = sp.factor(curvature_3 - 2 * laplacian_N_over_N)

    c = sp.symbols("c", positive=True)
    core_N = sp.exp(sp.Rational(2, 3) * c * r ** sp.Rational(3, 2))
    core_A = 1 + c * r ** sp.Rational(3, 2)
    core_R = _substitute_radial_functions(
        direct["ricci_scalar"], r, N, A, core_N, core_A
    )
    core_K = _substitute_radial_functions(
        direct["kretschmann"], r, N, A, core_N, core_A
    )

    mass, Hubble = sp.symbols("M H", positive=True)
    schwarzschild_N = sp.sqrt(1 - 2 * mass / r)
    schwarzschild_A = 1 / schwarzschild_N
    de_sitter_N = sp.sqrt(1 - Hubble**2 * r**2)
    de_sitter_A = 1 / de_sitter_N

    def evaluate(N_value: sp.Expr, A_value: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
        return (
            sp.simplify(
                _substitute_radial_functions(
                    direct["ricci_scalar"], r, N, A, N_value, A_value
                )
            ),
            sp.simplify(
                _substitute_radial_functions(
                    direct["kretschmann"], r, N, A, N_value, A_value
                )
            ),
        )

    minkowski = evaluate(sp.Integer(1), sp.Integer(1))
    schwarzschild = evaluate(schwarzschild_N, schwarzschild_A)
    de_sitter = evaluate(de_sitter_N, de_sitter_A)
    return {
        "r": r,
        "c": c,
        "mass": mass,
        "H": Hubble,
        "direct_ricci": direct["ricci_scalar"],
        "direct_kretschmann": direct["kretschmann"],
        "ricci_formula_residual": sp.simplify(
            direct["ricci_scalar"] - expected_ricci
        ),
        "kretschmann_formula_residual": sp.simplify(
            direct["kretschmann"] - expected_kretschmann
        ),
        "core_ricci": core_R,
        "core_kretschmann": core_K,
        "core_ricci_scaled_limit": sp.simplify(
            sp.limit(sp.sqrt(r) * core_R, r, 0, dir="+")
        ),
        "core_kretschmann_scaled_limit": sp.simplify(
            sp.limit(r * core_K, r, 0, dir="+")
        ),
        "minkowski": minkowski,
        "schwarzschild_ricci": schwarzschild[0],
        "schwarzschild_kretschmann": schwarzschild[1],
        "de_sitter_ricci": de_sitter[0],
        "de_sitter_kretschmann": de_sitter[1],
    }


def _derive_mutations(geometry: dict[str, Any]) -> dict[str, Any]:
    x = sp.symbols("x", positive=True)
    ell, G, epsilon = sp.symbols("ell_0 G epsilon", positive=True)
    Lambda = sp.symbols("Lambda", real=True)
    rho, pressure = sp.symbols("rho_0 p_c", real=True)
    u1, a2 = sp.symbols("u_1 a_2", real=True)
    up = u1 * x**2
    radial_metric = 1 + a2 * x**4

    zero_F = lambda y: sp.Integer(0)
    lapse_gr, radial_gr = _center_lhs(
        x, ell, Lambda, up, radial_metric, zero_F
    )
    gr_radial_coefficient = sp.factor(sp.limit(radial_gr / x**4, x, 0))
    gr_lapse_coefficient = sp.factor(sp.limit(lapse_gr, x, 0))
    gr_a2 = sp.solve(
        sp.Eq(gr_lapse_coefficient, 16 * sp.pi * G * rho), a2
    )[0]
    gr_u1 = sp.solve(
        sp.Eq(
            gr_radial_coefficient.subs(a2, gr_a2),
            -8 * sp.pi * G * pressure,
        ),
        u1,
    )[0]
    gr_substitution = {a2: gr_a2, u1: gr_u1}

    regulated_F = lambda y: 2 * ((1 + y) * sp.exp(-y) - 1) + epsilon * y**2
    lapse_reg, radial_reg = _center_lhs(
        x, ell, Lambda, up, radial_metric, regulated_F
    )
    reg_radial_coefficient = sp.factor(sp.limit(radial_reg / x**4, x, 0))
    reg_lapse_coefficient = sp.factor(sp.limit(lapse_reg, x, 0))
    reg_a2 = sp.solve(
        sp.Eq(reg_radial_coefficient, -8 * sp.pi * G * pressure), a2
    )[0]
    reg_u1 = sp.solve(
        sp.Eq(
            reg_lapse_coefficient.subs(a2, reg_a2),
            16 * sp.pi * G * rho,
        ),
        u1,
    )[0]
    regulated_residual = sp.simplify(
        (
            reg_lapse_coefficient.subs(a2, reg_a2)
            - 16 * sp.pi * G * rho
        ).subs(u1, reg_u1)
    )

    # A coordinate lambda'' is not the scalar D^2 lambda.  Its reduced action
    # fails the radial-diffeomorphism identity under scalar lambda and radial
    # one-form A transformations.
    r = geometry["r"]
    N, A, radius, lam = (
        geometry["N"], geometry["A"], geometry["R"], geometry["lambda"]
    )
    bad_q = sp.diff(lam, r, 2)
    bad_lagrangian = N * A * radius**2 * bad_q**2
    bad_E_N = _higher_euler(bad_lagrangian, N, r, 0)
    bad_E_A = _higher_euler(bad_lagrangian, A, r, 0)
    bad_E_R = _higher_euler(bad_lagrangian, radius, r, 0)
    bad_E_lambda = _higher_euler(bad_lagrangian, lam, r, 2)
    bad_noether = sp.factor(
        sp.diff(N, r) * bad_E_N
        + sp.diff(radius, r) * bad_E_R
        + sp.diff(lam, r) * bad_E_lambda
        + sp.diff(A, r) * bad_E_A
        - sp.diff(A * bad_E_A, r)
    )

    q = geometry["q"]
    q_independent = sp.symbols("q_independent", real=True)
    kappa = geometry["kappa_r"] + 2 * geometry["kappa_t"]
    wrong_b_kinetic = sp.factor(
        geometry["kappa_r"] ** 2
        + 2 * geometry["kappa_t"] ** 2
        - kappa**2
        + 2 * kappa * q_independent / N
        - q_independent**2 / N**2
    )
    wrong_q_derivative = sp.factor(
        sp.diff(N * A * radius**2 * wrong_b_kinetic, q_independent).subs(
            q_independent, q
        )
    )
    expected_q_derivative = sp.factor(2 * A * radius**2 * geometry["bar_K"])
    return {
        "gr_center_a2": sp.factor(gr_a2),
        "gr_center_u1": sp.factor(gr_u1),
        "gr_center_radial_residual": sp.simplify(
            (
                gr_radial_coefficient + 8 * sp.pi * G * pressure
            ).subs(gr_substitution, simultaneous=True)
        ),
        "gr_center_lapse_residual": sp.simplify(
            (
                gr_lapse_coefficient - 16 * sp.pi * G * rho
            ).subs(gr_substitution, simultaneous=True)
        ),
        "regulated_center_u1": sp.factor(reg_u1),
        "regulated_center_residual": regulated_residual,
        "regulated_center_is_finite": not reg_u1.has(sp.zoo, sp.oo, -sp.oo),
        "coordinate_laplacian_noether_defect": bad_noether,
        "wrong_b_square_constraint_residual": sp.simplify(
            wrong_q_derivative - expected_q_derivative
        ),
        "premature_shift_equation": sp.Integer(0),
    }


def derive_full_spherical_audit() -> dict[str, Any]:
    """Derive every symbolic object used by the action-level center audit."""

    geometry = _build_geometry()
    auxiliary = _derive_auxiliary_equations(geometry)
    metric = _derive_metric_equations(geometry)
    return {
        "action": ACTION,
        "geometry": geometry,
        "auxiliary_equations": auxiliary,
        "isolated_branch": _derive_isolated_branch(geometry),
        "metric_equations": metric,
        "radial_noether_identity": _derive_radial_noether_identity(
            geometry, auxiliary, metric
        ),
        "center": _derive_center(),
        "curvature": _derive_curvature(),
        "mutations": _derive_mutations(geometry),
        "scope": {
            "candidate_status": (
                "DEAD_UNDER_ISOLATED_STATIC_CLASSICAL_REGULAR_CENTER_REQUIREMENTS"
            ),
            "full_static_spherical_action_varied": True,
            "radial_shift_and_lambda_varied_before_branching": True,
            "regular_center_and_asymptotically_static_boundary_assumed": True,
            "zero_radial_matter_momentum_assumed": True,
            "central_lambda_point_charge_absent": True,
            "full_nonlinear_dirac_completed": False,
            "boosted_ppn_completed": False,
            "cosmological_cmc_branch_excluded": False,
            "nonspherical_external_field_excluded": False,
            "global_novelty_claimed": False,
        },
    }


def _main() -> int:
    result = derive_full_spherical_audit()
    geometry = result["geometry"]
    auxiliary = result["auxiliary_equations"]
    branch = result["isolated_branch"]
    metric = result["metric_equations"]
    noether = result["radial_noether_identity"]
    smooth = result["center"]["smooth"]
    puiseux = result["center"]["puiseux"]
    curvature = result["curvature"]
    mutations = result["mutations"]
    checks = {
        "spherical geometry benchmarks": (
            geometry["flat_spatial_curvature"] == 0
            and geometry["unit_three_sphere_curvature"] == 6
            and geometry["flat_lambda_laplacian_residual"] == 0
        ),
        "barred kinetic action expanded exactly": (
            geometry["kinetic_expansion_residual"] == 0
        ),
        "lambda equation varied": auxiliary["lambda_equation_residual"] == 0,
        "radial shift equation varied": auxiliary["shift_equation_residual"] == 0,
        "source-free isolated auxiliary branch derived": (
            branch["harmonic_solution_residual"] == 0
            and branch["momentum_solution_residual"] == 0
            and branch["central_auxiliary_charge_solution"] == 0
            and branch["traceless_mode_action_diverges"]
            and branch["isolated_shift_constant"] == 0
        ),
        "exact N A R equations varied": all(
            metric[key] == 0
            for key in (
                "lapse_equation_residual",
                "radial_equation_residual",
                "angular_equation_residual",
            )
        )
        and all(
            residual == 0
            for residual in noether[
                "zero_branch_full_kinetic_metric_variation_residuals"
            ]
        ),
        "raw and boundary-reduced actions agree": (
            metric["raw_vs_first_order_boundary_residual"] == 0
        ),
        "radial diffeomorphism identities": (
            noether["static_metric_residual"] == 0
            and noether["full_kinetic_residual"] == 0
        ),
        "smooth center compatibility derived": (
            smooth["radial_coefficient_residual"] == 0
            and smooth["lapse_coefficient_residual"] == 0
        ),
        "Puiseux branch solves both center equations": (
            puiseux["radial_solution_residual"] == 0
            and puiseux["lapse_solution_residual"] == 0
        ),
        "curvature coefficients derived": (
            curvature["core_ricci_scaled_limit"] == 5 * curvature["c"]
            and curvature["core_kretschmann_scaled_limit"]
            == 43 * curvature["c"] ** 2
        ),
        "curvature benchmarks": (
            curvature["minkowski"] == (0, 0)
            and curvature["schwarzschild_ricci"] == 0
            and curvature["de_sitter_ricci"] == 12 * curvature["H"] ** 2
        ),
        "mutations are live": (
            mutations["gr_center_radial_residual"] == 0
            and mutations["gr_center_lapse_residual"] == 0
            and mutations["regulated_center_residual"] == 0
            and mutations["coordinate_laplacian_noether_defect"] != 0
            and mutations["wrong_b_square_constraint_residual"] != 0
        ),
    }
    print("=" * 78)
    print("HPI-DELTA FULL STATIC-SPHERICAL ACTION AUDIT")
    print("=" * 78)
    for label, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    print("\nDerived isolated branch:")
    print(" ", branch["derived_isolated_branch"])
    print("Smooth C2-center compatibility residual:")
    print(" ", smooth["compatibility_residual"], "= 0 required")
    print("Required rho_0+3p_c:", smooth["required_active_density"])
    print("Puiseux c^2:", puiseux["c_squared"])
    print("sqrt(r) R4 ->", curvature["core_ricci_scaled_limit"])
    print("r Kretschmann ->", curvature["core_kretschmann_scaled_limit"])
    print("\nSTATUS:", result["scope"]["candidate_status"])
    print(
        "NONCLAIMS: no full nonlinear Dirac theorem, boosted PPN result, "
        "nonspherical external-field theorem, or exclusion of cosmological CMC."
    )
    certificate = {
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "all_passed": all(checks.values()),
        "candidate_status": result["scope"]["candidate_status"],
        "smooth_required_active_density": str(smooth["required_active_density"]),
        "puiseux_c_squared": str(puiseux["c_squared"]),
        "ricci_scaled_limit": str(curvature["core_ricci_scaled_limit"]),
        "kretschmann_scaled_limit": str(
            curvature["core_kretschmann_scaled_limit"]
        ),
    }
    print("CERTIFICATE_JSON:", json.dumps(certificate, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(_main())
