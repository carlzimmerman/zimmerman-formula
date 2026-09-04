#!/usr/bin/env python3
"""Configuration-space and covariant-lift audit for the HPI-Delta candidate.

This is a bounded construction gate.  It starts from the committed HPI-Delta
first-order ADM Hamiltonian, eliminates the metric momentum exactly, and writes
the resulting configuration action in both ADM and clock-covariant notation.
It then checks the links that can be decided without pretending that a full
nonlinear functional Dirac or boosted PPN calculation has been completed.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import sympy as sp


ACTION_ADM = r"""
S_HPI_Delta = (M_Pl^2/2) integral dt d^3x N sqrt(h) [
    Kbar_ij Kbar^ij - Kbar^2 + R_3 - 2 Lambda
    - (2/ell_0^2) F_exp(y)
] + S_m[g,psi],

Kbar_ij = K_ij - (D^2 lambda)/(2N) h_ij,
y = ell_0 sqrt(h^ij D_i ln(N) D_j ln(N)),
F_exp(y) = 2[(1+y) exp(-y) - 1].
""".strip()


ACTION_COVARIANT = r"""
S_HPI_Delta^cov = (M_Pl^2/2) integral d^4x sqrt(-g) [
    R - 2 Lambda - (2/ell_0^2) F_exp(y) + 2 K b - (3/2) b^2
] + S_m[g,psi],

X = -g^munu nabla_mu T nabla_nu T > 0,
n_mu = -nabla_mu T/sqrt(X),
h_munu = g_munu + n_mu n_nu,
K_munu = h_mu^alpha h_nu^beta nabla_alpha n_beta,
K = h^munu K_munu,
a_mu = n^nu nabla_nu n_mu,
D is the induced spatial connection,
b = sqrt(X) D^2 lambda,
y = ell_0 sqrt(a_mu a^mu).

In unitary clock gauge T=t: sqrt(X)=1/N and b=(D^2 lambda)/N.
Ordinary matter fields psi occur only in S_m and couple minimally to g_munu.
""".strip()


def _euler_first_order(
    lagrangian: sp.Expr, field: sp.Expr, coordinate: sp.Symbol
) -> sp.Expr:
    return sp.factor(
        sp.diff(lagrangian, field)
        - sp.diff(lagrangian, sp.diff(field, coordinate), coordinate)
    )


def _derive_kernel() -> dict[str, Any]:
    y = sp.symbols("y", positive=True)
    F = 2 * ((1 + y) * sp.exp(-y) - 1)
    primitive = sp.factor(y**2 + F)
    mu = sp.factor(sp.diff(primitive, y) / (2 * y))
    lambda_perp = mu
    lambda_parallel = sp.factor(sp.diff(y * mu, y))
    return {
        "y": y,
        "F_exp": F,
        "primitive": primitive,
        "mu": mu,
        "mu_residual": sp.simplify(mu - (1 - sp.exp(-y))),
        "lambda_perp": lambda_perp,
        "lambda_parallel": lambda_parallel,
        "parallel_residual": sp.simplify(
            lambda_parallel - (1 + (y - 1) * sp.exp(-y))
        ),
        "positive_y_derivative": sp.diff(y * mu, y),
        "zero_perpendicular": sp.limit(lambda_perp, y, 0, dir="+"),
        "zero_parallel": sp.limit(lambda_parallel, y, 0, dir="+"),
        "newtonian_mu": sp.limit(mu, y, sp.oo),
        "deep_mu_ratio": sp.limit(mu / y, y, 0, dir="+"),
        "deep_primitive_ratio": sp.limit(primitive / y**3, y, 0, dir="+"),
        "flux_map_derivative": lambda_parallel,
    }


def _legendre_transform_for_lagrangian(
    lagrangian: sp.Expr,
    curvatures: tuple[sp.Symbol, ...],
    lapse: sp.Symbol,
    momentum_symbols: tuple[sp.Symbol, ...],
) -> dict[str, Any]:
    velocities = tuple(2 * lapse * curvature for curvature in curvatures)
    derived_momenta = tuple(
        sp.factor(sp.diff(lagrangian, curvature) / (2 * lapse))
        for curvature in curvatures
    )
    solutions = sp.solve(
        tuple(
            sp.Eq(momentum, derived)
            for momentum, derived in zip(momentum_symbols, derived_momenta)
        ),
        curvatures,
        dict=True,
        simplify=False,
    )
    if len(solutions) != 1:
        raise RuntimeError("metric Legendre map did not have one algebraic branch")
    solution = solutions[0]
    inversion_residuals = tuple(
        sp.simplify(
            (derived - momentum).subs(solution, simultaneous=True)
        )
        for momentum, derived in zip(momentum_symbols, derived_momenta)
    )
    hamiltonian = sp.factor(
        (
            sum(
                momentum * velocity
                for momentum, velocity in zip(momentum_symbols, velocities)
            )
            - lagrangian
        ).subs(solution, simultaneous=True)
    )
    return {
        "velocities": velocities,
        "derived_momenta": derived_momenta,
        "solution": solution,
        "velocity_inversion_residuals": inversion_residuals,
        "hamiltonian": hamiltonian,
    }


def _derive_legendre_lift() -> dict[str, Any]:
    M2, N = sp.symbols("M_Pl_sq N", positive=True, nonzero=True)
    sqrt_h = sp.symbols("sqrt_h", positive=True, nonzero=True)
    z = sp.symbols("z_lambda", real=True)
    K1, K2, K3 = sp.symbols("K_1 K_2 K_3", real=True)
    curvatures = (K1, K2, K3)
    p1, p2, p3 = sp.symbols("p_1 p_2 p_3", real=True)
    momenta = (p1, p2, p3)
    s = z / (2 * N)
    shifted = tuple(curvature - s for curvature in curvatures)
    lagrangian = sp.factor(
        M2
        * N
        * sqrt_h
        / 2
        * (sum(value**2 for value in shifted) - sum(shifted) ** 2)
    )
    transform = _legendre_transform_for_lagrangian(
        lagrangian, curvatures, N, momenta
    )
    trace_momentum = sp.factor(sum(transform["derived_momenta"]))
    expected_trace = -M2 * sqrt_h * (
        sum(curvatures) - 3 * z / (2 * N)
    )
    p_trace = sum(momenta)
    expected_hamiltonian = sp.factor(
        2
        * N
        / (M2 * sqrt_h)
        * (sum(momentum**2 for momentum in momenta) - p_trace**2 / 2)
        + z * p_trace
    )

    # Negative control: deleting the uniquely fixed z^2 term spoils the
    # reconstruction of the first-order trace-constraint coupling.
    gr_kinetic = M2 * N * sqrt_h / 2 * (
        sum(curvature**2 for curvature in curvatures) - sum(curvatures) ** 2
    )
    dropped_square = sp.factor(
        gr_kinetic + M2 * sqrt_h * z * sum(curvatures)
    )
    dropped_transform = _legendre_transform_for_lagrangian(
        dropped_square, curvatures, N, momenta
    )
    dropped_residual = sp.factor(
        dropped_transform["hamiltonian"] - expected_hamiltonian
    )
    return {
        "M2": M2,
        "N": N,
        "sqrt_h": sqrt_h,
        "z": z,
        "curvatures": curvatures,
        "momenta": momenta,
        "trace_shift": s,
        "lagrangian": lagrangian,
        **transform,
        "trace_momentum": trace_momentum,
        "expected_trace_momentum": expected_trace,
        "trace_momentum_residual": sp.simplify(trace_momentum - expected_trace),
        "expected_hamiltonian": expected_hamiltonian,
        "hamiltonian_residual": sp.simplify(
            transform["hamiltonian"] - expected_hamiltonian
        ),
        "constraint_coupling": z * p_trace,
        "drop_b_square_hamiltonian": dropped_transform["hamiltonian"],
        "drop_b_square_residual": dropped_residual,
    }


def _derive_auxiliary_equation() -> dict[str, Any]:
    x = sp.symbols("x", real=True)
    M2 = sp.symbols("M_Pl_sq", positive=True)
    N = sp.Function("N")(x)
    K = sp.Function("K")(x)
    lam = sp.Function("lambda")(x)
    lam_dot = sp.symbols("lambda_dot", real=True)
    z = sp.diff(lam, x, 2)
    lagrangian = M2 * K * z - 3 * M2 * z**2 / (4 * N)
    euler_lambda = sp.factor(
        sp.diff(sp.diff(lagrangian, z), x, 2)
    )
    expected = sp.diff(M2 * (K - 3 * z / (2 * N)), x, 2)
    trace_momentum = -M2 * (K - 3 * z / (2 * N))

    wrong_lagrangian = M2 * K * z - M2 * z**2 / (2 * N)
    wrong_euler = sp.factor(
        sp.diff(sp.diff(wrong_lagrangian, z), x, 2)
    )
    wrong_constraint_residual = sp.simplify(
        wrong_euler + sp.diff(trace_momentum, x, 2)
    )
    return {
        "coordinate": x,
        "N": N,
        "K": K,
        "lambda": lam,
        "z": z,
        "lagrangian": lagrangian,
        "euler_lambda": euler_lambda,
        "expected_euler": expected,
        "euler_residual": sp.simplify(euler_lambda - expected),
        "trace_momentum": trace_momentum,
        "constraint_residual": sp.simplify(
            euler_lambda + sp.diff(trace_momentum, x, 2)
        ),
        "lambda_velocity_hessian": sp.diff(lagrangian, lam_dot, 2),
        "wrong_coefficient_euler": wrong_euler,
        "wrong_coefficient_constraint_residual": wrong_constraint_residual,
    }


def _derive_weak_static(kernel: dict[str, Any]) -> dict[str, Any]:
    x = sp.symbols("x", real=True)
    a0, G = sp.symbols("a_0 G", positive=True)
    Phi = sp.Function("Phi")(x)
    Psi = sp.Function("Psi")(x)
    rho = sp.Function("rho_b")(x)
    gradient = sp.diff(Phi, x)
    y_local = gradient / a0
    F_local = kernel["F_exp"].subs(kernel["y"], y_local)
    lagrangian = (
        -2 * sp.diff(Phi, x) * sp.diff(Psi, x)
        + sp.diff(Psi, x) ** 2
        - a0**2 * F_local
        - 8 * sp.pi * G * rho * Phi
    )
    E_phi = _euler_first_order(lagrangian, Phi, x)
    E_psi = _euler_first_order(lagrangian, Psi, x)
    expected_psi = 2 * sp.diff(Phi - Psi, x, 2)
    mu_local = (1 - sp.exp(-y_local))
    expected_aqual = 2 * sp.diff(mu_local * gradient, x) - 8 * sp.pi * G * rho
    slip_map = {
        Psi: Phi,
        sp.diff(Psi, x): sp.diff(Phi, x),
        sp.diff(Psi, x, 2): sp.diff(Phi, x, 2),
    }
    phi_on_slip = sp.factor(E_phi.subs(slip_map, simultaneous=True))
    return {
        "coordinate": x,
        "lagrangian": lagrangian,
        "E_phi": E_phi,
        "E_psi": E_psi,
        "expected_psi_equation": expected_psi,
        "psi_equation_residual": sp.simplify(E_psi - expected_psi),
        "phi_on_slip": phi_on_slip,
        "expected_aqual": expected_aqual,
        "phi_on_slip_aqual_residual": sp.simplify(phi_on_slip - expected_aqual),
        "slip_inserted_before_variation": False,
        "static_auxiliary_branch": "K=0 and D^2 lambda=0 under isolated boundary data",
    }


def _load_committed_action_gate() -> dict[str, Any]:
    path = (
        Path(__file__).resolve().parents[1]
        / "cde_hpi_delta_2026"
        / "cde_hpi_delta_action_gate_2026.py"
    )
    spec = importlib.util.spec_from_file_location("cde_hpi_delta_action_gate_2026", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load committed HPI-Delta action gate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derive_hpi_delta_gate()


def _load_regular_center_no_go() -> dict[str, Any]:
    path = (
        Path(__file__).resolve().parents[1]
        / "exact_mond_regular_center_no_go_2026"
        / "exact_mond_regular_center_no_go_2026.py"
    )
    spec = importlib.util.spec_from_file_location(
        "exact_mond_regular_center_no_go_2026", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load exact-MOND regular-center gate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derive_regular_center_no_go()


def _derive_finite_k_dirac(legendre: dict[str, Any]) -> dict[str, Any]:
    committed = _load_committed_action_gate()
    chain = committed["finite_k"]["generic_positive_gradient"]
    return {
        "constraints": chain["constraints"],
        "poisson_matrix": chain["poisson_matrix_on_constraint_surface"],
        "constraint_jacobian_rank": chain["constraint_jacobian_rank"],
        "poisson_rank": chain["poisson_rank"],
        "poisson_sample_rank": chain["poisson_sample_rank"],
        "first_class_count": chain["first_class_count"],
        "second_class_count": chain["second_class_count"],
        "scalar_configuration_dof": chain["configuration_dof"],
        "rank_witness_determinant": chain["rank_witness"]["determinant"],
        "legendre_bridge_residual": legendre["hamiltonian_residual"],
        "source_path": committed["action_text"],
        "full_nonlinear_inference_forbidden": True,
    }


def _derive_mode_sectors() -> dict[str, Any]:
    k, p_trace = sp.symbols("k p_trace", real=True)
    symbol = -k**2 * p_trace
    return {
        "k": k,
        "constraint_symbol": symbol,
        "finite_k_constraint_active": sp.simplify(symbol.subs({k: 2, p_trace: 1})) != 0,
        "homogeneous_constraint_symbol": sp.simplify(symbol.subs(k, 0)),
        "homogeneous_restart_required": sp.simplify(symbol.subs(k, 0)) == 0,
    }


def _derive_zero_field_core(kernel: dict[str, Any]) -> dict[str, Any]:
    r, a0, G, rho = sp.symbols("r a_0 G rho", positive=True)
    u = sp.symbols("u", positive=True)
    C = 4 * sp.pi * G * rho / 3
    flux_map = sp.factor(u * (1 - sp.exp(-u)))
    flux_map_derivative = sp.factor(sp.diff(flux_map, u))
    gravitational_flux = C * r
    spherical_flux = sp.factor(r**2 * gravitational_flux)
    source_equation = sp.factor(sp.diff(spherical_flux, r) / r**2)
    deep_acceleration = sp.sqrt(a0 * C * r)
    asymptotic_ratio = sp.sqrt(
        sp.limit(u**2 / flux_map, u, 0, dir="+")
    )
    committed = _load_committed_action_gate()
    regular_center = _load_regular_center_no_go()
    regular_spherical = regular_center["spherical_core"]
    regular_weak = regular_center["weak_solution"]
    quadratic_zero = committed["finite_k"]["exact_zero_field"]
    nonlinear_solution_exists = source_equation == 4 * sp.pi * G * rho
    return {
        "r": r,
        "a0": a0,
        "G": G,
        "rho": rho,
        "C": C,
        "dimensionless_flux_map": flux_map,
        "flux_map_derivative": flux_map_derivative,
        "flux_derivative_residual": sp.simplify(
            flux_map_derivative
            - (1 + (u - 1) * sp.exp(-u))
        ),
        "flux_identity_residual": sp.simplify(spherical_flux - C * r**3),
        "source_equation": source_equation,
        "source_equation_residual": sp.simplify(
            source_equation - 4 * sp.pi * G * rho
        ),
        "deep_acceleration": deep_acceleration,
        "deep_central_ratio": sp.simplify(asymptotic_ratio),
        "flux_at_origin": sp.limit(spherical_flux, r, 0, dir="+"),
        "quadratic_source_obstruction": quadratic_zero["source_obstruction"],
        "quadratic_source_obstruction_requires_vacuum": quadratic_zero[
            "source_obstruction_requires_vacuum"
        ],
        "linearized_source_obstruction_is_not_nonlinear_no_go": bool(
            quadratic_zero["source_obstruction_requires_vacuum"]
            and nonlinear_solution_exists
        ),
        "finite_action_weak_solution_exists": regular_weak["weak_solution_exists"],
        "hessian_diverges": regular_spherical["hessian_diverges"],
        "tidal_norm_squared_diverges": regular_spherical[
            "tidal_norm_squared_diverges"
        ],
        "no_slip_ricci_scalar_diverges": regular_spherical[
            "no_slip_ricci_scalar_diverges"
        ],
        "classical_c2_regular_center_exists": regular_weak[
            "classical_c2_solution_exists"
        ],
        "regular_center_theorem_status": regular_center["scope"]["theorem_status"],
        "interpretation": (
            "The exact exponential p-Laplacian has a unique radial flux branch; "
            "the sourced y=0 quadratic obstruction diagnoses a singular linearization. "
            "A finite-action weak solution exists, but the no-slip metric is not C2 "
            "and its Ricci/tidal curvature diverges at a smooth positive-density center."
        ),
    }


def _derive_flrw(kernel: dict[str, Any]) -> dict[str, Any]:
    scale, scale_dot, N, M2, Lambda = sp.symbols(
        "a a_dot N M_Pl_sq Lambda", positive=True
    )
    H = sp.symbols("H", positive=True)
    p_scale, p_N, p_lambda = sp.symbols("p_a p_N p_lambda0", real=True)
    lambda_zero = sp.symbols("lambda_0", real=True)
    background_lagrangian = (
        -3 * M2 * scale * scale_dot**2 / N
        - M2 * Lambda * N * scale**3
    )
    lapse_equation = sp.diff(background_lagrangian, N)
    lapse_in_H = sp.factor(
        lapse_equation.subs(scale_dot, H * N * scale, simultaneous=True)
    )
    friedmann_expression = H**2 - Lambda / 3

    derived_p_scale = sp.factor(sp.diff(background_lagrangian, scale_dot))
    scale_dot_solution = sp.solve(
        sp.Eq(p_scale, derived_p_scale), scale_dot
    )[0]
    hamiltonian_constraint = sp.factor(
        -p_scale**2 / (12 * M2 * scale) + M2 * Lambda * scale**3
    )
    canonical_hamiltonian = sp.factor(N * hamiltonian_constraint)
    legendre_hamiltonian = sp.factor(
        (p_scale * scale_dot - background_lagrangian).subs(
            scale_dot, scale_dot_solution
        )
    )

    coordinates = (scale, N, lambda_zero)
    momenta = (p_scale, p_N, p_lambda)

    def poisson(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.factor(
            sum(
                sp.diff(left, coordinate) * sp.diff(right, momentum)
                - sp.diff(left, momentum) * sp.diff(right, coordinate)
                for coordinate, momentum in zip(coordinates, momenta)
            )
        )

    primary_constraints = (p_N, p_lambda)
    constraints = primary_constraints + (hamiltonian_constraint,)
    poisson_matrix = sp.Matrix(
        [
            [poisson(left, right) for right in constraints]
            for left in constraints
        ]
    )
    phase_variables = coordinates + momenta
    constraint_jacobian = sp.Matrix(
        [
            [sp.diff(constraint, variable) for variable in phase_variables]
            for constraint in constraints
        ]
    )
    poisson_rank = poisson_matrix.rank()
    second_class_count = poisson_rank
    first_class_count = len(constraints) - second_class_count
    configuration_dof = sp.Rational(
        len(phase_variables) - 2 * first_class_count - second_class_count,
        2,
    )
    return {
        "a": scale,
        "N": N,
        "H": H,
        "acceleration_squared": sp.Integer(0),
        "auxiliary_b": sp.Integer(0),
        "F_background": sp.simplify(kernel["F_exp"].subs(kernel["y"], 0)),
        "lambda_equation": sp.Integer(0),
        "background_lagrangian": background_lagrangian,
        "lapse_equation": lapse_equation,
        "lapse_equation_in_H": lapse_in_H,
        "friedmann_expression": friedmann_expression,
        "friedmann_residual": sp.simplify(
            lapse_in_H / (3 * M2 * scale**3) - friedmann_expression
        ),
        "de_sitter_H": sp.sqrt(Lambda / 3),
        "derived_scale_momentum": derived_p_scale,
        "scale_velocity_solution": scale_dot_solution,
        "hamiltonian_constraint": hamiltonian_constraint,
        "canonical_hamiltonian": canonical_hamiltonian,
        "legendre_hamiltonian_residual": sp.simplify(
            legendre_hamiltonian - canonical_hamiltonian
        ),
        "primary_constraints": primary_constraints,
        "secondary_constraints": (hamiltonian_constraint,),
        "constraints": constraints,
        "primary_preservation_residuals": (
            sp.simplify(poisson(p_N, canonical_hamiltonian) + hamiltonian_constraint),
            sp.simplify(poisson(p_lambda, canonical_hamiltonian)),
        ),
        "secondary_preservation_residual": sp.simplify(
            poisson(hamiltonian_constraint, canonical_hamiltonian)
        ),
        "poisson_matrix": poisson_matrix,
        "poisson_rank": poisson_rank,
        "constraint_jacobian": constraint_jacobian,
        "constraint_jacobian_rank": constraint_jacobian.rank(),
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "homogeneous_gravitational_configuration_dof": configuration_dof,
        "homogeneous_dirac_restart_completed": True,
        "a0_lambda_relation_derived": False,
    }


def _derive_tensor() -> dict[str, Any]:
    M2, scale, N, k = sp.symbols(
        "M_Pl_sq a N k", positive=True, nonzero=True
    )
    h, h_dot = sp.symbols("h_T h_T_dot", real=True)
    lagrangian = (
        M2 * scale**3 * h_dot**2 / (8 * N)
        - M2 * N * scale * k**2 * h**2 / 8
    )
    kinetic = sp.diff(lagrangian, h_dot, 2)
    restoring = -sp.diff(lagrangian, h, 2)
    coordinate_speed_squared = sp.factor(restoring / (kinetic * k**2))
    physical_speed_squared = sp.factor(
        coordinate_speed_squared * scale**2 / N**2
    )
    return {
        "lagrangian_per_polarization": lagrangian,
        "kinetic_coefficient": kinetic,
        "restoring_coefficient": restoring,
        "coordinate_speed_squared": coordinate_speed_squared,
        "speed_squared": physical_speed_squared,
        "positive_kinetic": bool(kinetic.is_positive),
        "auxiliary_tt_coupling": sp.Integer(0),
        "mond_tt_coupling": sp.Integer(0),
        "selection_rule": (
            "On homogeneous FLRW, a_mu=0 and b=0; TT perturbations have delta K=0, "
            "so only the Einstein-Hilbert TT block survives."
        ),
    }


def _derive_high_acceleration(kernel: dict[str, Any]) -> dict[str, Any]:
    y = kernel["y"]
    F = kernel["F_exp"]
    Lambda, ell = sp.symbols("Lambda ell_0", positive=True)
    F_limit = sp.limit(F, y, sp.oo)
    F_prime_limit = sp.limit(sp.diff(F, y), y, sp.oo)
    F_second_limit = sp.limit(sp.diff(F, y, 2), y, sp.oo)
    lambda_effective = Lambda - 2 / ell**2
    limiting_constant = -2 * Lambda - 2 * F_limit / ell**2
    return {
        "F_limit": F_limit,
        "F_prime_limit": F_prime_limit,
        "F_second_limit": F_second_limit,
        "lambda_effective": lambda_effective,
        "limiting_constant": limiting_constant,
        "lambda_effective_residual": sp.simplify(
            limiting_constant + 2 * lambda_effective
        ),
        "cmc_constraint_is_gr_gauge_fixing_only_in_this_limit": bool(
            F_prime_limit == 0 and F_second_limit == 0
        ),
        "ppn_statement": (
            "Formal y->infinity action is GR with Lambda_eff in CMC gauge. "
            "Finite-y boosted PPN coefficients are not computed here."
        ),
    }


def _derive_ward_identity() -> dict[str, Any]:
    E_m, grad_m = sp.symbols("E_m grad_m", real=True)
    E_T = sp.symbols("E_T", real=True)
    grad_T = sp.symbols("grad_T", real=True, nonzero=True)
    E_lambda, grad_lambda = sp.symbols(
        "E_lambda grad_lambda", real=True
    )
    div_metric = sp.symbols("div_metric", real=True)
    matter_divergence = E_m * grad_m
    full_identity = -2 * div_metric + E_T * grad_T + E_lambda * grad_lambda + E_m * grad_m
    clock_on_shell = sp.solve(
        sp.Eq(
            full_identity.subs(
                {div_metric: 0, E_lambda: 0, E_m: 0}, simultaneous=True
            ),
            0,
        ),
        E_T,
    )[0]
    return {
        "matter_off_shell_divergence": matter_divergence,
        "matter_on_shell_divergence": sp.simplify(
            matter_divergence.subs(E_m, 0)
        ),
        "full_diffeomorphism_identity": full_identity,
        "clock_equation_on_other_shells": clock_on_shell,
        "clock_gradient_assumption": "grad_T is timelike and nonzero",
        "auxiliary_depends_on_matter_fields": False,
        "status": "Noether-Ward consequence of separately diffeomorphism-invariant minimal S_m",
    }


def derive_covariant_lift_gate() -> dict[str, Any]:
    """Return the derived candidate data used by the executable audit."""

    kernel = _derive_kernel()
    legendre = _derive_legendre_lift()
    auxiliary = _derive_auxiliary_equation()
    return {
        "action": {
            "adm": ACTION_ADM,
            "covariant": ACTION_COVARIANT,
            "physical_metric_count": 1,
            "matter_minimal_to_physical_metric": True,
            "clock_gradient_required_timelike": True,
            "unitary_gauge_relation": "T=t, sqrt(X)=1/N, b=D^2(lambda)/N",
        },
        "kernel": kernel,
        "legendre_lift": legendre,
        "auxiliary_equation": auxiliary,
        "weak_static": _derive_weak_static(kernel),
        "finite_k_dirac": _derive_finite_k_dirac(legendre),
        "mode_sectors": _derive_mode_sectors(),
        "zero_field_core": _derive_zero_field_core(kernel),
        "flrw": _derive_flrw(kernel),
        "tensor": _derive_tensor(),
        "high_acceleration": _derive_high_acceleration(kernel),
        "ward_identity": _derive_ward_identity(),
        "mutations": {
            "drop_b_square": {
                "hamiltonian_residual": legendre["drop_b_square_residual"]
            },
            "wrong_b_coefficient": {
                "constraint_residual": auxiliary[
                    "wrong_coefficient_constraint_residual"
                ]
            },
            "newtonian_kernel": {"mu": sp.Integer(1)},
        },
        "scope": {
            "configuration_action_legendre_equivalent": (
                legendre["hamiltonian_residual"] == 0
            ),
            "clock_covariant_notation_supplied": True,
            "finite_k_quadratic_dirac_reused_and_bridged": True,
            "static_zero_field_weak_flux_exists": True,
            "static_zero_field_c2_regular": False,
            "conditional_regular_center_no_go_proved": True,
            "flrw_background_derived": True,
            "homogeneous_minisuperspace_dirac_closed": True,
            "tensor_quadratic_block_derived": True,
            "full_nonlinear_functional_dirac_closed": False,
            "boosted_ppn_closed": False,
            "global_stability_closed": False,
            "global_novelty_claimed": False,
            "candidate_status": "DEAD_AS_AN_EXACT_CLASSICAL_REGULAR_CENTER_THEORY",
        },
    }


def _main() -> int:
    result = derive_covariant_lift_gate()
    lift = result["legendre_lift"]
    auxiliary = result["auxiliary_equation"]
    weak = result["weak_static"]
    chain = result["finite_k_dirac"]
    core = result["zero_field_core"]
    flrw = result["flrw"]
    tensor = result["tensor"]
    checks = {
        "configuration action Legendre-reconstructs HPI-Delta": (
            lift["hamiltonian_residual"] == 0
            and lift["trace_momentum_residual"] == 0
            and all(value == 0 for value in lift["velocity_inversion_residuals"])
        ),
        "lambda variation gives D^2(pi/sqrt(h))=0": (
            auxiliary["euler_residual"] == 0
            and auxiliary["constraint_residual"] == 0
        ),
        "lambda has no unitary-gauge velocity": (
            auxiliary["lambda_velocity_hessian"] == 0
        ),
        "exact exponential constitutive law": result["kernel"]["mu_residual"] == 0,
        "Phi and Psi varied separately": weak["psi_equation_residual"] == 0,
        "derived no-slip branch gives AQUAL": weak["phi_on_slip_aqual_residual"] == 0,
        "finite-k PB rank computed consistently": (
            chain["poisson_rank"] == chain["poisson_sample_rank"]
            and chain["rank_witness_determinant"] != 0
        ),
        "finite-k scalar pair absent in bounded chain": (
            chain["scalar_configuration_dof"] == 0
        ),
        "finite-action nonlinear sourced weak core exists": (
            core["source_equation_residual"] == 0
            and core["deep_central_ratio"] == 1
        ),
        "regular-center curvature obstruction detected": (
            core["hessian_diverges"]
            and core["tidal_norm_squared_diverges"]
            and core["no_slip_ricci_scalar_diverges"]
            and not core["classical_c2_regular_center_exists"]
        ),
        "homogeneous and finite-k symbols separated": (
            result["mode_sectors"]["homogeneous_restart_required"]
        ),
        "expanding Einstein-FLRW branch": (
            flrw["friedmann_residual"] == 0 and flrw["de_sitter_H"] != 0
        ),
        "homogeneous k=0 Dirac restart closes": (
            flrw["legendre_hamiltonian_residual"] == 0
            and flrw["primary_preservation_residuals"] == (0, 0)
            and flrw["secondary_preservation_residual"] == 0
            and flrw["constraint_jacobian_rank"] == len(flrw["constraints"])
            and flrw["homogeneous_gravitational_configuration_dof"] == 0
        ),
        "tensor block positive and luminal": (
            tensor["positive_kinetic"] and tensor["speed_squared"] == 1
        ),
        "ordinary minimal-matter Ward identity": (
            result["ward_identity"]["matter_on_shell_divergence"] == 0
        ),
        "negative controls fire": (
            result["mutations"]["drop_b_square"]["hamiltonian_residual"] != 0
            and result["mutations"]["wrong_b_coefficient"]["constraint_residual"] != 0
        ),
    }
    print("=" * 84)
    print("HPI-DELTA CONFIGURATION / CLOCK-COVARIANT LIFT GATE")
    print("=" * 84)
    for label, passed in checks.items():
        print(("[PASS] " if passed else "[FAIL] ") + label)
    print("\nDerived ADM action:\n" + ACTION_ADM)
    print("\nDerived auxiliary Euler equation:")
    print(" ", auxiliary["euler_lambda"], "= 0")
    print("  equals -D^2(pi/sqrt(h)); residual =", auxiliary["constraint_residual"])
    print("\nFinite-k constraint census (values are computed, not targets):")
    print("  constraints =", len(chain["constraints"]))
    print("  Jacobian rank =", chain["constraint_jacobian_rank"])
    print("  Poisson rank =", chain["poisson_rank"])
    print("  first/second class =", chain["first_class_count"], chain["second_class_count"])
    print("  scalar configuration DOF =", chain["scalar_configuration_dof"])
    print("  nonzero witness determinant =", chain["rank_witness_determinant"])
    print("\nHomogeneous k=0 minisuperspace Dirac restart:")
    print("  constraints =", len(flrw["constraints"]))
    print("  Jacobian rank =", flrw["constraint_jacobian_rank"])
    print("  Poisson rank =", flrw["poisson_rank"])
    print(
        "  first/second class =",
        flrw["first_class_count"],
        flrw["second_class_count"],
    )
    print(
        "  homogeneous gravitational configuration DOF =",
        flrw["homogeneous_gravitational_configuration_dof"],
    )
    print("\nNew zero-field result:")
    print("  uniform-density exact flux =", core["C"], "* r")
    print("  div(flux) =", core["source_equation"])
    print("  g(r) ~", core["deep_acceleration"], "as r -> 0+")
    print("  The finite-action weak solution exists, but its Hessian, tidal norm,")
    print("  and no-slip Ricci scalar diverge at the smooth positive-density center.")
    print("  The quadratic J_rho=0 obstruction is a singular-linearization warning;")
    print("  the new result is a classical regular-center curvature no-go.")
    print("\nHonest boundary:")
    print("  This lift is not a full nonlinear functional Dirac proof and not a boosted")
    print("  PPN or global stability certificate. Those later gates are pre-empted:")
    print("  candidate status: DEAD as an exact classical regular-center theory.")
    certificate = {
        "candidate_status": result["scope"]["candidate_status"],
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "constraint_count": len(chain["constraints"]),
        "constraint_jacobian_rank": chain["constraint_jacobian_rank"],
        "poisson_rank": chain["poisson_rank"],
        "first_class_count": chain["first_class_count"],
        "second_class_count": chain["second_class_count"],
        "scalar_configuration_dof": str(chain["scalar_configuration_dof"]),
    }
    print("CERTIFICATE_JSON:", json.dumps(certificate, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(_main())
