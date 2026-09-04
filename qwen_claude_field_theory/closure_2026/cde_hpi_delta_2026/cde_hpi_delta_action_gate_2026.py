#!/usr/bin/env python3
r"""Construct/falsify the one-constraint HPI-Delta exponential-MOND prototype.

This file is deliberately a *bounded gate*, not a completed theory.  It freezes a
first-order, spatially covariant ADM action with one local auxiliary constraint,

    C_pi = D^2(pi/sqrt(h)),

and derives its nonzero-mode scalar Dirac chain.  The central test is whether
preserving C_pi produces weak-field no slip while lapse preservation gives AQUAL.
Nothing in this file is a PPN or nonlinear functional-Dirac certificate.

The Laplacian trace-momentum architecture is known MMG machinery: compare
Yao--Oliosi--Gao--Mukohyama, arXiv:2011.00805, and the Laplacian-multiplier
construction of Sangtawee--De Felice--Karwan, arXiv:2607.26031.  No novelty claim
is made here.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import sympy as sp


ACTION = r"""
S_HPIΔ = ∫dt d^3x [
    pi^{ij} dot(h_ij) + p_psi dot(psi)
  - N ( H_GR[h,pi] + H_exp[h,N] + H_m[h,psi,p_psi] )
  - N^i ( H_i^GR + H_i^m )
  - sqrt(h) lambda_pi D^2( pi/sqrt(h) )
],

H_GR = 2/(M_Pl^2 sqrt(h)) (pi_ij pi^ij - pi^2/2)
       - (M_Pl^2/2) sqrt(h) (R_3 - 2 Lambda),
M_Pl^2 = 1/(8 pi G_bare),
H_exp = (M_Pl^2/ell_0^2) sqrt(h) F_exp(y),
a_i=D_i ln N, y=ell_0 sqrt(h^{ij}a_i a_j), ell_0=c^2/a_0,
F_exp(y)=2[(1+y)exp(-y)-1],
C_pi=D^2(pi/sqrt(h)), pi=h_ij pi^{ij},
S_m is minimally coupled to the same ADM metric.

The foliation is nondynamical structure in this prototype (S_clock=0).  A
covariant clock/Stueckelberg completion and its degree count are NOT supplied.
""".strip()


def _higher_euler(
    lagrangian: sp.Expr,
    field: sp.Expr,
    coordinate: sp.Symbol,
    order: int,
) -> sp.Expr:
    result = sp.diff(lagrangian, field)
    for derivative_order in range(1, order + 1):
        jet = sp.diff(field, coordinate, derivative_order)
        result += (-1) ** derivative_order * sp.diff(
            sp.diff(lagrangian, jet), coordinate, derivative_order
        )
    return sp.factor(result)


def _poisson_bracket(
    first: sp.Expr,
    second: sp.Expr,
    coordinates: tuple[sp.Symbol, ...],
    momenta: tuple[sp.Symbol, ...],
) -> sp.Expr:
    return sp.factor(
        sum(
            sp.diff(first, coordinate) * sp.diff(second, momentum)
            - sp.diff(first, momentum) * sp.diff(second, coordinate)
            for coordinate, momentum in zip(coordinates, momenta)
        )
    )


def _rank_witness(matrix: sp.MatrixBase) -> dict[str, Any]:
    """Produce a nonzero minor at the rank SymPy actually finds."""

    rank = matrix.rank()
    if rank == 0:
        return {
            "size": 0,
            "rows": (),
            "columns": (),
            "matrix": sp.zeros(0),
            "determinant": sp.Integer(1),
        }
    columns = tuple(matrix.rref()[1])
    column_basis = matrix[:, columns]
    rows = tuple(column_basis.T.rref()[1])
    witness = matrix.extract(rows, columns)
    determinant = sp.factor(witness.det())
    if determinant == 0:
        raise RuntimeError("computed rank did not yield a nonzero witness minor")
    return {
        "size": rank,
        "rows": rows,
        "columns": columns,
        "matrix": witness,
        "determinant": determinant,
    }


def _sample_rank(matrix: sp.MatrixBase, substitutions: dict[sp.Symbol, Any]) -> int:
    """Independent exact-rational rank sample; no target rank is passed in."""

    return int(matrix.subs(substitutions, simultaneous=True).rank())


def _classify_linear_constraints(
    constraints: tuple[sp.Expr, ...],
    coordinates: tuple[sp.Symbol, ...],
    momenta: tuple[sp.Symbol, ...],
    sample: dict[sp.Symbol, Any],
) -> dict[str, Any]:
    phase_variables = coordinates + momenta
    matrix = sp.Matrix(
        [
            [
                _poisson_bracket(first, second, coordinates, momenta)
                for second in constraints
            ]
            for first in constraints
        ]
    )
    solution_list = sp.solve(
        constraints, phase_variables, dict=True, simplify=False
    )
    surface = solution_list[0] if solution_list else {}
    matrix_surface = matrix.subs(surface, simultaneous=True).applyfunc(sp.factor)
    jacobian = sp.Matrix(constraints).jacobian(phase_variables)
    poisson_rank = matrix_surface.rank()
    jacobian_rank = jacobian.rank()
    nullspace = tuple(matrix_surface.nullspace())
    first_class_generators = tuple(
        sp.factor(sum(vector[index] * constraints[index] for index in range(len(constraints))))
        for vector in nullspace
    )
    first_class_residuals = tuple(
        sp.factor(
            _poisson_bracket(generator, constraint, coordinates, momenta).subs(
                surface, simultaneous=True
            )
        )
        for generator in first_class_generators
        for constraint in constraints
    )
    first_class_count = len(nullspace)
    second_class_count = poisson_rank
    phase_dimension = len(phase_variables)
    configuration_dof = sp.Rational(
        phase_dimension - 2 * first_class_count - second_class_count, 2
    )
    return {
        "phase_variables": phase_variables,
        "phase_dimension": phase_dimension,
        "constraints": constraints,
        "constraint_solution": surface,
        "constraint_jacobian": jacobian,
        "constraint_jacobian_rank": jacobian_rank,
        "constraint_jacobian_sample_rank": _sample_rank(jacobian, sample),
        "poisson_matrix": matrix,
        "poisson_matrix_on_constraint_surface": matrix_surface,
        "poisson_rank": poisson_rank,
        "poisson_sample_rank": _sample_rank(matrix_surface, sample),
        "poisson_nullspace": nullspace,
        "first_class_generators": first_class_generators,
        "first_class_bracket_residuals": first_class_residuals,
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "configuration_dof": configuration_dof,
        "rank_witness": _rank_witness(matrix_surface),
    }


def _derive_kernel() -> dict[str, Any]:
    y = sp.symbols("y", positive=True)
    correction = 2 * ((1 + y) * sp.exp(-y) - 1)
    combined = y**2 + correction
    exact_primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    modulus = sp.factor(1 + sp.diff(correction, y) / (2 * y))
    mu = 1 - sp.exp(-y)
    longitudinal = sp.factor(1 + sp.diff(correction, y, 2) / 2)
    return {
        "y": y,
        "F_exp": correction,
        "combined_primitive": combined,
        "exact_primitive": exact_primitive,
        "primitive_residual": sp.simplify(combined - exact_primitive),
        "mu": mu,
        "modulus": modulus,
        "modulus_residual": sp.simplify(modulus - mu),
        "lambda_parallel": longitudinal,
        "lambda_parallel_expected": 1 + (y - 1) * sp.exp(-y),
        "lambda_parallel_residual": sp.simplify(
            longitudinal - (1 + (y - 1) * sp.exp(-y))
        ),
        "newtonian_limit": sp.limit(modulus, y, sp.oo),
        "deep_ratio": sp.limit(modulus / y, y, 0, dir="+"),
        "zero_field_modulus": sp.limit(modulus, y, 0, dir="+"),
        "zero_field_longitudinal": sp.limit(longitudinal, y, 0, dir="+"),
    }


def _derive_weak_static(kernel: dict[str, Any]) -> dict[str, Any]:
    """Vary a one-dimensional weak-static reduction before imposing slip."""

    z = sp.symbols("z", real=True)
    a0, G = sp.symbols("a_0 G", positive=True)
    Phi = sp.Function("Phi")(z)
    Psi = sp.Function("Psi")(z)
    rho = sp.Function("rho_b")(z)
    gradient = sp.diff(Phi, z)
    y_local = gradient / a0  # oriented positive-gradient branch
    correction_local = 2 * ((1 + y_local) * sp.exp(-y_local) - 1)
    lagrangian = (
        -2 * sp.diff(Phi, z) * sp.diff(Psi, z)
        + sp.diff(Psi, z) ** 2
        - a0**2 * correction_local
        - 8 * sp.pi * G * rho * Phi
    )
    E_Phi = _higher_euler(lagrangian, Phi, z, 2)
    E_Psi = _higher_euler(lagrangian, Psi, z, 2)
    expected_E_Psi = 2 * (sp.diff(Phi, z, 2) - sp.diff(Psi, z, 2))
    slip_substitution = {
        Psi: Phi,
        sp.diff(Psi, z): sp.diff(Phi, z),
        sp.diff(Psi, z, 2): sp.diff(Phi, z, 2),
    }
    E_Phi_on_slip = sp.factor(E_Phi.subs(slip_substitution, simultaneous=True))
    mu_local = 1 - sp.exp(-y_local)
    expected_aqual = sp.factor(
        2 * sp.diff(mu_local * sp.diff(Phi, z), z) - 8 * sp.pi * G * rho
    )

    r, enclosed_mass, g = sp.symbols("r M_b g", positive=True)
    mu_g = 1 - sp.exp(-g / a0)
    integrated_flux = r**2 * mu_g * g - G * enclosed_mass
    spherical_law = mu_g * g - G * enclosed_mass / r**2
    g_newton = G * enclosed_mass / r**2
    return {
        "coordinate": z,
        "lagrangian": lagrangian,
        "E_Phi": E_Phi,
        "E_Psi": E_Psi,
        "no_slip_residual": sp.simplify(E_Psi - expected_E_Psi),
        "derived_no_slip_equation": expected_E_Psi,
        "E_Phi_on_derived_slip": E_Phi_on_slip,
        "expected_aqual": expected_aqual,
        "E_Phi_on_derived_slip_residual": sp.simplify(E_Phi_on_slip - expected_aqual),
        "aqual_flux_residual": sp.simplify(
            expected_aqual / 2
            - (sp.diff(mu_local * sp.diff(Phi, z), z) - 4 * sp.pi * G * rho)
        ),
        "integrated_spherical_flux": integrated_flux,
        "spherical_law": spherical_law,
        "spherical_flux_residual": sp.simplify(integrated_flux / r**2 - spherical_law),
        "deep_mond_residual": sp.simplify(
            sp.limit(mu_g * g / (g**2 / a0), g, 0, dir="+") - 1
        ),
        "g_newton": g_newton,
        "conditional_high_acceleration_G_if_3d_extension_holds": sp.solve(
            sp.Eq(
                4 * sp.pi * sp.Symbol("G_measured") * rho,
                4 * sp.pi * G * rho,
            ),
            sp.Symbol("G_measured"),
        )[0],
        "bare_G_normalization": sp.Eq(
            sp.Symbol("M_Pl_sq"), 1 / (8 * sp.pi * G)
        ),
        "measured_G_from_full_theory": None,
        "measured_G_is_conditional_on_3d_extension": True,
        "spherical_relation_is_symmetry_extension_not_varied_here": True,
        "one_dimensional_reduction_only": True,
        "positive_gradient_branch": True,
        "boundary_condition_for_no_slip": "Phi-Psi -> 0 at spatial infinity",
    }


def _base_scalar_lagrangian(
    *, restore_spatial_gauge: bool
) -> dict[str, Any]:
    """Derive the finite-k quadratic scalar action from ADM mode geometry."""

    A, k, longitudinal = sp.symbols(
        "A k lambda_parallel", positive=True, nonzero=True
    )
    Phi, Psi, B = sp.symbols("Phi Psi B", real=True)
    Psi_dot = sp.symbols("Psi_dot", real=True)
    E = sp.symbols("E", real=True)
    E_dot = sp.symbols("E_dot", real=True)
    shear = B - E_dot if restore_spatial_gauge else B

    epsilon, theta = sp.symbols("epsilon theta", real=True)
    mode = sp.cos(theta)

    def mode_average(expression: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.integrate(sp.expand_trig(expression), (theta, 0, 2 * sp.pi))
            / (2 * sp.pi)
        )

    # K^i_j=diag(-Psi_dot+k^2 Sigma,-Psi_dot,-Psi_dot) for the real mode;
    # <cos^2>=1/2 is already included in the following ADM scalar density.
    K_amplitude = sp.diag(
        -Psi_dot + k**2 * shear,
        -Psi_dot,
        -Psi_dot,
    )
    K_trace = sp.trace(K_amplitude)
    kinetic = sp.factor(
        sp.Rational(1, 2)
        * (sp.trace(K_amplitude * K_amplitude) - K_trace**2)
    )

    # Derive the EH spatial term from the exact conformal metric rather than
    # entering its Phi-Psi coefficients.  For h_ij=e^{-2s}delta_ij,
    # sqrt(h)R_3=e^{-s}[4 d^2s-2(ds)^2].
    s = epsilon * Psi * mode
    lapse = 1 + epsilon * Phi * mode
    s_x = k * sp.diff(s, theta)
    s_xx = k**2 * sp.diff(s, theta, 2)
    r3_density = lapse * sp.exp(-s) * (4 * s_xx - 2 * s_x**2)
    r3_quadratic = sp.expand(
        sp.series(r3_density, epsilon, 0, 3).removeO()
    ).coeff(epsilon, 2)
    eh_spatial = mode_average(r3_quadratic)

    # The longitudinal second variation of -F_exp is
    # (1-lambda_parallel) k^2 Phi^2, with lambda_parallel derived from
    # 1+F_exp''/2 in _derive_kernel.
    y_hessian = sp.symbols("y_hessian", positive=True)
    F_hessian = 2 * ((1 + y_hessian) * sp.exp(-y_hessian) - 1)
    longitudinal_from_action = 1 + sp.diff(F_hessian, y_hessian, 2) / 2
    mond_spatial = (1 - longitudinal) * k**2 * Phi**2
    spatial = sp.factor(eh_spatial + mond_spatial)
    expected_spatial = k**2 * (
        (1 - longitudinal) * Phi**2 - 2 * Phi * Psi + Psi**2
    )
    lagrangian = sp.factor(A * (kinetic + spatial))
    expected = A * (
        -3 * Psi_dot**2
        + 2 * k**2 * shear * Psi_dot
        + spatial
    )
    return {
        "A": A,
        "k": k,
        "lambda_parallel": longitudinal,
        "Phi": Phi,
        "Psi": Psi,
        "B": B,
        "E": E,
        "Psi_dot": Psi_dot,
        "E_dot": E_dot,
        "shear": shear,
        "K_amplitude": K_amplitude,
        "K_trace": K_trace,
        "kinetic": kinetic,
        "r3_quadratic_density": r3_quadratic,
        "eh_spatial": eh_spatial,
        "mond_spatial": mond_spatial,
        "longitudinal_from_action": longitudinal_from_action,
        "mond_hessian_residual": sp.simplify(
            mond_spatial.subs(
                longitudinal, longitudinal_from_action
            )
            + sp.diff(F_hessian, y_hessian, 2)
            * k**2
            * Phi**2
            / 2
        ),
        "spatial": spatial,
        "spatial_reduction_residual": sp.simplify(spatial - expected_spatial),
        "lagrangian": lagrangian,
        "adm_reduction_residual": sp.simplify(lagrangian - expected),
    }


def _derive_gauge_restored_chain() -> dict[str, Any]:
    base = _base_scalar_lagrangian(restore_spatial_gauge=True)
    A, k, longitudinal = base["A"], base["k"], base["lambda_parallel"]
    Phi, Psi, B, E = base["Phi"], base["Psi"], base["B"], base["E"]
    Psi_dot, E_dot = base["Psi_dot"], base["E_dot"]
    eta = sp.symbols("eta_pi", real=True)
    source = sp.symbols("J_rho", real=True)
    Phi_dot, B_dot, eta_dot = sp.symbols("Phi_dot B_dot eta_dot", real=True)
    p_Phi, p_Psi, p_B, p_E, p_eta = sp.symbols(
        "p_Phi p_Psi p_B p_E p_eta", real=True
    )
    coordinates = (Phi, Psi, B, E, eta)
    momenta = (p_Phi, p_Psi, p_B, p_E, p_eta)

    lagrangian = base["lagrangian"] - source * Phi
    derived_p_Psi = sp.factor(sp.diff(lagrangian, Psi_dot))
    derived_p_E = sp.factor(sp.diff(lagrangian, E_dot))
    velocity_solution = sp.solve(
        (sp.Eq(p_Psi, derived_p_Psi), sp.Eq(p_E, derived_p_E)),
        (Psi_dot, E_dot),
        dict=True,
        simplify=False,
    )[0]
    H0 = sp.factor(
        (p_Psi * Psi_dot + p_E * E_dot - lagrangian).subs(
            velocity_solution, simultaneous=True
        )
    )

    # From p_Psi=-2 pi for h_ij=e^{-2Psi}delta_ij,
    # -sqrt(h)lambda D^2(pi/sqrt(h)) is +eta k^2 p_Psi after rescaling eta.
    C_pi_symbol = k**2 * p_Psi
    canonical_hamiltonian = sp.factor(H0 + eta * C_pi_symbol)
    primaries = (p_Phi, p_B, p_eta)
    derived_primaries = tuple(
        momentum
        for momentum, derivative in zip(
            primaries,
            (
                sp.diff(lagrangian, Phi_dot),
                sp.diff(lagrangian, B_dot),
                sp.diff(lagrangian, eta_dot),
            ),
        )
        if derivative == 0
    )
    primary_velocity_derivatives = (
        sp.diff(lagrangian, Phi_dot),
        sp.diff(lagrangian, B_dot),
        sp.diff(lagrangian, eta_dot),
    )
    secondaries = tuple(
        _poisson_bracket(primary, canonical_hamiltonian, coordinates, momenta)
        for primary in primaries
    )
    C_N, C_shift, C_pi = secondaries
    trace_preservation = _poisson_bracket(
        C_pi, canonical_hamiltonian, coordinates, momenta
    )
    slip_expression = 2 * A * k**4 * (Phi - Psi)

    # Generate the next constraint by multiplier compatibility, rather than
    # inserting eta=0.  The coefficients below are obtained by differentiation
    # of the two actual preservation equations.
    u_Phi, u_B, u_eta = sp.symbols("u_Phi u_B u_eta", real=True)
    multipliers = (u_Phi, u_B, u_eta)
    total_hamiltonian = canonical_hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(multipliers, primaries)
    )
    dot_C_N = _poisson_bracket(C_N, total_hamiltonian, coordinates, momenta)
    dot_slip = _poisson_bracket(
        trace_preservation, total_hamiltonian, coordinates, momenta
    )
    coeff_N = sp.diff(dot_C_N, u_Phi)
    coeff_slip = sp.diff(dot_slip, u_Phi)
    compatibility_raw = sp.factor(coeff_slip * dot_C_N - coeff_N * dot_slip)
    stage_constraints = primaries + secondaries + (trace_preservation,)
    stage_surface = sp.solve(
        stage_constraints, coordinates + momenta, dict=True, simplify=False
    )[0]
    compatibility_constraint = sp.factor(
        compatibility_raw.subs(stage_surface, simultaneous=True)
    )
    constraints = stage_constraints + (compatibility_constraint,)
    sample = {
        A: sp.Rational(5, 3),
        k: sp.Rational(7, 5),
        longitudinal: sp.Rational(2, 3),
        source: sp.Rational(11, 7),
    }
    classified = _classify_linear_constraints(
        constraints, coordinates, momenta, sample
    )

    surface = classified["constraint_solution"]
    preservation_equations = tuple(
        sp.factor(
            _poisson_bracket(
                constraint, total_hamiltonian, coordinates, momenta
            ).subs(surface, simultaneous=True)
        )
        for constraint in constraints
    )
    multiplier_solutions = sp.solve(
        preservation_equations, multipliers, dict=True, simplify=False
    )
    multiplier_solution = multiplier_solutions[0] if multiplier_solutions else {}
    final_residuals = tuple(
        sp.simplify(equation.subs(multiplier_solution, simultaneous=True))
        for equation in preservation_equations
    )
    unfixed = tuple(
        multiplier for multiplier in multipliers if multiplier not in multiplier_solution
    )
    # If all final residuals vanish after multiplier fixing, the left-null
    # compatibility projection is identically zero and yields no new constraint.
    new_after_final = tuple(
        residual for residual in final_residuals if residual != 0
    )

    weak_E_Psi_mode = -2 * k**2 * (Phi - Psi)
    return {
        **classified,
        "A": A,
        "k": k,
        "lambda_parallel": longitudinal,
        "source": source,
        "base": base,
        "lagrangian": lagrangian,
        "derived_p_Psi": derived_p_Psi,
        "derived_p_E": derived_p_E,
        "velocity_solution": velocity_solution,
        "canonical_hamiltonian": canonical_hamiltonian,
        "C_pi_symbol": C_pi_symbol,
        "symplectic_trace_relation": sp.Eq(
            p_Psi, -2 * sp.Symbol("pi_trace")
        ),
        "C_pi_fourier_from_trace": k**2 * p_Psi / 2,
        "C_pi_rescaling_residual": sp.simplify(
            C_pi_symbol - 2 * (k**2 * p_Psi / 2)
        ),
        "primaries": primaries,
        "derived_primaries": derived_primaries,
        "primaries_preselected_by_first_order_canonical_action": True,
        "primary_check_is_velocity_absence_not_hessian_discovery": True,
        "primary_velocity_derivatives": primary_velocity_derivatives,
        "secondaries": secondaries,
        "trace_preservation": trace_preservation,
        "trace_preservation_slip_residual": sp.simplify(
            trace_preservation - slip_expression
        ),
        "trace_preservation_vs_weak_E_Psi_residual": sp.simplify(
            trace_preservation + A * k**2 * weak_E_Psi_mode
        ),
        "trace_preservation_independent_before_closure": (
            sp.Matrix(stage_constraints).jacobian(coordinates + momenta).rank()
            > sp.Matrix(primaries + secondaries).jacobian(coordinates + momenta).rank()
        ),
        "slip_inserted_as_constraint": False,
        "compatibility_raw": compatibility_raw,
        "lambda_constraint": compatibility_constraint,
        "lambda_constraint_was_generated": (
            compatibility_constraint != 0
            and sp.diff(compatibility_constraint, eta) != 0
        ),
        "total_hamiltonian": total_hamiltonian,
        "primary_multipliers": multipliers,
        "shift_primary_multiplier": u_B,
        "preservation_equations": preservation_equations,
        "multiplier_solution": multiplier_solution,
        "unfixed_primary_multipliers": unfixed,
        "final_preservation_residuals": final_residuals,
        "new_constraints_after_final_stage": new_after_final,
        "local_scalar_pair_survives": bool(classified["configuration_dof"] > 0),
    }


def _derive_spatial_gauge_fixed_chain() -> dict[str, Any]:
    """Independent E=0 chain; it must agree with the restored-gauge count."""

    base = _base_scalar_lagrangian(restore_spatial_gauge=False)
    A, k, longitudinal = base["A"], base["k"], base["lambda_parallel"]
    Phi, Psi, B = base["Phi"], base["Psi"], base["B"]
    Psi_dot = base["Psi_dot"]
    eta = sp.symbols("eta_pi_gf", real=True)
    source = sp.symbols("J_rho_gf", real=True)
    p_Phi, p_Psi, p_B, p_eta = sp.symbols(
        "p_Phi_gf p_Psi_gf p_B_gf p_eta_gf", real=True
    )
    coordinates = (Phi, Psi, B, eta)
    momenta = (p_Phi, p_Psi, p_B, p_eta)
    lagrangian = base["lagrangian"] - source * Phi
    derived_p_Psi = sp.factor(sp.diff(lagrangian, Psi_dot))
    velocity_solution = sp.solve(
        sp.Eq(p_Psi, derived_p_Psi), Psi_dot, dict=True, simplify=False
    )[0]
    H0 = sp.factor(
        (p_Psi * Psi_dot - lagrangian).subs(
            velocity_solution, simultaneous=True
        )
    )
    # k^2 is absorbed in eta only in this finite-k gauge-fixed cross-check.
    canonical_hamiltonian = sp.factor(H0 + eta * p_Psi)
    primaries = (p_Phi, p_B, p_eta)
    secondaries = tuple(
        _poisson_bracket(primary, canonical_hamiltonian, coordinates, momenta)
        for primary in primaries
    )
    tertiary = _poisson_bracket(
        secondaries[-1], canonical_hamiltonian, coordinates, momenta
    )
    u_Phi, u_B, u_eta = sp.symbols("u_Phi_gf u_B_gf u_eta_gf")
    multipliers = (u_Phi, u_B, u_eta)
    total = canonical_hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(multipliers, primaries)
    )

    # A raw {tertiary,H_c} is not by itself a new constraint because both
    # dot(C_N) and dot(tertiary) contain the primary multiplier u_Phi.  Project
    # out that multiplier using coefficients differentiated from H_T.  The
    # resulting compatibility condition, not the raw bracket, is quaternary.
    C_N = secondaries[0]
    dot_C_N = _poisson_bracket(C_N, total, coordinates, momenta)
    dot_tertiary = _poisson_bracket(
        tertiary, total, coordinates, momenta
    )
    coeff_N = sp.diff(dot_C_N, u_Phi)
    coeff_tertiary = sp.diff(dot_tertiary, u_Phi)
    quaternary_raw = sp.factor(
        coeff_tertiary * dot_C_N - coeff_N * dot_tertiary
    )
    # k!=0 and lambda_parallel>0 on this branch.  Divide only the derived,
    # nowhere-zero overall factor to display the primitive constraint.
    quaternary = sp.factor(
        -3 * quaternary_raw / (2 * A * k**4 * longitudinal)
    )
    constraints = primaries + secondaries + (tertiary, quaternary)
    sample = {
        A: sp.Rational(7, 4),
        k: sp.Rational(5, 3),
        longitudinal: sp.Rational(3, 5),
        source: sp.Rational(13, 11),
    }
    classified = _classify_linear_constraints(
        constraints, coordinates, momenta, sample
    )
    surface = classified["constraint_solution"]
    preservation = tuple(
        sp.factor(
            _poisson_bracket(constraint, total, coordinates, momenta).subs(
                surface, simultaneous=True
            )
        )
        for constraint in constraints
    )
    multiplier_solution = sp.solve(
        preservation, multipliers, dict=True, simplify=False
    )[0]
    residuals = tuple(
        sp.simplify(value.subs(multiplier_solution, simultaneous=True))
        for value in preservation
    )
    expected_tertiary = 2 * A * k**2 * (Phi - Psi)
    expected_quaternary = 2 * A * B * k**2 + 6 * A * eta - p_Psi
    return {
        **classified,
        "base": base,
        "lagrangian": lagrangian,
        "derived_p_Psi": derived_p_Psi,
        "velocity_solution": velocity_solution,
        "canonical_hamiltonian": canonical_hamiltonian,
        "primaries": primaries,
        "secondaries": secondaries,
        "tertiary": tertiary,
        "quaternary_raw": quaternary_raw,
        "raw_tertiary_preservation": dot_tertiary,
        "raw_lapse_constraint_preservation": dot_C_N,
        "quaternary": quaternary,
        "tertiary_slip_residual": sp.simplify(tertiary - expected_tertiary),
        "quaternary_residual": sp.simplify(quaternary - expected_quaternary),
        "poisson_determinant": sp.factor(classified["poisson_matrix"].det()),
        "total_hamiltonian": total,
        "multiplier_solution": multiplier_solution,
        "final_preservation_residuals": residuals,
    }


def _derive_exact_zero_field_branch() -> dict[str, Any]:
    """Re-run lambda_parallel=0 and isolate its sourced inconsistency."""

    base = _base_scalar_lagrangian(restore_spatial_gauge=False)
    A, k = base["A"], base["k"]
    Phi, Psi, B = base["Phi"], base["Psi"], base["B"]
    Psi_dot = base["Psi_dot"]
    eta = sp.symbols("eta_pi_zero", real=True)
    p_Phi, p_Psi, p_B, p_eta = sp.symbols(
        "p_Phi_zero p_Psi_zero p_B_zero p_eta_zero", real=True
    )
    source = sp.symbols("J_rho_zero", real=True)
    coordinates = (Phi, Psi, B, eta)
    momenta = (p_Phi, p_Psi, p_B, p_eta)
    lagrangian = sp.factor(
        base["lagrangian"].subs(base["lambda_parallel"], 0)
        - source * Phi
    )
    derived_p_Psi = sp.diff(lagrangian, Psi_dot)
    velocity = sp.solve(sp.Eq(p_Psi, derived_p_Psi), Psi_dot, dict=True)[0]
    H0 = sp.factor((p_Psi * Psi_dot - lagrangian).subs(velocity))
    H = sp.factor(H0 + eta * p_Psi)
    primaries = (p_Phi, p_B, p_eta)
    sourced_secondaries = tuple(
        _poisson_bracket(primary, H, coordinates, momenta)
        for primary in primaries
    )
    C_N_sourced, _, C_pi_sourced = sourced_secondaries
    trace_preservation_sourced = _poisson_bracket(
        C_pi_sourced, H, coordinates, momenta
    )
    source_obstruction = sp.factor(
        trace_preservation_sourced - C_N_sourced
    )

    # A consistent exact-zero quadratic constraint surface therefore exists
    # only in vacuum.  Restart the branch after the *derived* condition J=0;
    # do not silently drop the source before detecting it.
    H_vacuum = sp.factor(H.subs(source, 0))
    secondaries = tuple(
        sp.factor(constraint.subs(source, 0))
        for constraint in sourced_secondaries
    )
    C_N, _, C_pi = secondaries
    trace_preservation = sp.factor(
        trace_preservation_sourced.subs(source, 0)
    )
    # In this finite-k E=0 cross-check the k^2 multiplying C_pi was absorbed
    # into eta, so dot(C_pi) and C_N coincide at lambda_parallel=0.
    trace_dependence_residual = sp.simplify(trace_preservation - C_N)
    # At y=0 the apparent slip tertiary is already C_N.  With the *total*
    # Hamiltonian, preserving C_N fixes u_Phi=eta; the raw {C_N,H_c} must not
    # be misclassified as a new constraint.
    constraints = primaries + secondaries
    sample = {A: sp.Rational(4, 3), k: sp.Rational(9, 7)}
    classified = _classify_linear_constraints(
        constraints, coordinates, momenta, sample
    )
    u_Phi, u_B, u_eta = sp.symbols(
        "u_Phi_zero u_B_zero u_eta_zero", real=True
    )
    multipliers = (u_Phi, u_B, u_eta)
    total_hamiltonian = H_vacuum + sum(
        multiplier * primary
        for multiplier, primary in zip(multipliers, primaries)
    )
    preservation = tuple(
        sp.factor(
            _poisson_bracket(
                constraint, total_hamiltonian, coordinates, momenta
            ).subs(classified["constraint_solution"], simultaneous=True)
        )
        for constraint in constraints
    )
    multiplier_solution = sp.solve(
        preservation, multipliers, dict=True, simplify=False
    )[0]
    preservation_residuals = tuple(
        sp.simplify(value.subs(multiplier_solution, simultaneous=True))
        for value in preservation
    )
    return {
        **classified,
        "base": base,
        "lagrangian": lagrangian,
        "canonical_hamiltonian_sourced": H,
        "canonical_hamiltonian": H_vacuum,
        "source": source,
        "sourced_secondaries": sourced_secondaries,
        "trace_preservation_sourced": trace_preservation_sourced,
        "source_obstruction": source_obstruction,
        "source_obstruction_requires_vacuum": source_obstruction == source,
        "vacuum_only": True,
        "primaries": primaries,
        "secondaries": secondaries,
        "trace_preservation": trace_preservation,
        "trace_preservation_dependence_residual": trace_dependence_residual,
        "generated_quaternary": None,
        "total_hamiltonian": total_hamiltonian,
        "preservation_equations": preservation,
        "multiplier_solution": multiplier_solution,
        "final_preservation_residuals": preservation_residuals,
        "new_constraints_after_final_stage": tuple(
            value for value in preservation_residuals if value != 0
        ),
        "strong_coupling_not_excluded": True,
    }


def _derive_no_constraint_mutation() -> dict[str, Any]:
    base = _base_scalar_lagrangian(restore_spatial_gauge=True)
    A, k, longitudinal = base["A"], base["k"], base["lambda_parallel"]
    Phi, Psi, B, E = base["Phi"], base["Psi"], base["B"], base["E"]
    Psi_dot, E_dot = base["Psi_dot"], base["E_dot"]
    source = sp.symbols("J_mutation", real=True)
    p_Phi, p_Psi, p_B, p_E = sp.symbols(
        "p_Phi_mut p_Psi_mut p_B_mut p_E_mut", real=True
    )
    coordinates = (Phi, Psi, B, E)
    momenta = (p_Phi, p_Psi, p_B, p_E)
    L = base["lagrangian"] - source * Phi
    equations = (
        sp.Eq(p_Psi, sp.diff(L, Psi_dot)),
        sp.Eq(p_E, sp.diff(L, E_dot)),
    )
    velocities = sp.solve(equations, (Psi_dot, E_dot), dict=True)[0]
    H = sp.factor((p_Psi * Psi_dot + p_E * E_dot - L).subs(velocities))
    primaries = (p_Phi, p_B)
    secondaries = tuple(
        _poisson_bracket(primary, H, coordinates, momenta)
        for primary in primaries
    )
    constraints = primaries + secondaries
    sample = {
        A: sp.Rational(3, 2),
        k: sp.Rational(4, 3),
        longitudinal: sp.Rational(1, 2),
        source: sp.Rational(2, 5),
    }
    return _classify_linear_constraints(constraints, coordinates, momenta, sample)


def _derive_k_zero_and_mutations(kernel: dict[str, Any], no_constraint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    Mpl2, scale, lapse = sp.symbols(
        "M_Pl_sq a N", positive=True, nonzero=True
    )
    Hubble = sp.symbols("H", real=True)
    K_flrw = 3 * Hubble / lapse
    pi_over_sqrt_h = -Mpl2 * K_flrw
    pi_trace = scale**3 * pi_over_sqrt_h
    k = sp.symbols("k", real=True)
    C_pi_mode = -k**2 * pi_over_sqrt_h
    C_pi_zero = sp.simplify(C_pi_mode.subs(k, 0))
    k_zero = {
        "K_flrw": K_flrw,
        "flrw_trace_momentum": pi_trace,
        "C_pi_mode": C_pi_mode,
        "C_pi": C_pi_zero,
        "C_pi_on_flrw": C_pi_zero,
        "expansion_allowed_by_C_pi": (
            C_pi_zero == 0 and sp.solve(sp.Eq(C_pi_zero, 0), Hubble) == []
        ),
        "C_pi_does_not_algebraically_force_H_zero": C_pi_zero == 0,
        "fresh_homogeneous_hessian_dirac_restart_performed": False,
        "viable_flrw_derived": False,
        "interpretation": "D^2 removes the homogeneous multiplier/constraint symbol; a fresh k=0 Hessian/Dirac and background variation are still owed",
    }

    H_solution_no_laplacian = sp.solve(
        sp.Eq(pi_over_sqrt_h, 0), Hubble, dict=True
    )
    H_solution_lambda_K = sp.solve(sp.Eq(K_flrw, 0), Hubble, dict=True)
    y = kernel["y"]
    remove_mond_modulus = sp.Integer(1)
    mutations = {
        "no_laplacian": {
            "constraint_on_flrw": pi_over_sqrt_h,
            "H_solution": H_solution_no_laplacian,
            "forces_H_zero": bool(
                H_solution_no_laplacian
                and H_solution_no_laplacian[0].get(Hubble) == 0
            ),
        },
        "lagrangian_lambda_K": {
            "constraint_on_flrw": K_flrw,
            "H_solution": H_solution_lambda_K,
            "forces_H_zero": bool(
                H_solution_lambda_K
                and H_solution_lambda_K[0].get(Hubble) == 0
            ),
            "reason": "delta_lambda S gives K=0, including the homogeneous mode",
        },
        "remove_mond": {
            "modulus": remove_mond_modulus,
            "modulus_residual": sp.simplify(
                remove_mond_modulus - kernel["mu"]
            ),
        },
        "remove_trace_constraint": no_constraint,
    }
    return k_zero, mutations


def _derive_matter_ward() -> dict[str, Any]:
    E_matter, grad_matter = sp.symbols("E_matter grad_matter", real=True)
    eta_direct, J_prime = sp.symbols(
        "eta_direct J_prime", real=True, nonzero=True
    )
    divergence = -E_matter * grad_matter
    return {
        "off_shell_identity": divergence,
        "on_shell_divergence": sp.simplify(divergence.subs(E_matter, 0)),
        "auxiliary_direct_matter_derivative": sp.Integer(0),
        "direct_coupling_mutation_defect": eta_direct * J_prime * grad_matter,
        "explicit_matter_action_varied": False,
        "conditional_on_diffeomorphism_invariant_minimal_Sm": True,
        "scope": "Noether template only; an explicit matter action and gravitational refoliation completion remain open",
    }


def _derive_tensor_block() -> dict[str, Any]:
    A_T, k_T, h_T, hdot_T = sp.symbols(
        "A_T k_T h_T hdot_T", positive=True, nonzero=True
    )
    lagrangian = A_T * (hdot_T**2 - k_T**2 * h_T**2)
    kinetic = sp.diff(lagrangian, hdot_T, 2)
    gradient = -sp.diff(lagrangian, h_T, 2) / k_T**2
    speed_squared = sp.simplify(gradient / kinetic)
    return {
        "lagrangian": lagrangian,
        "kinetic_coefficient": kinetic,
        "gradient_coefficient": gradient,
        "positive_kinetic": bool(kinetic.is_positive),
        "speed_squared": speed_squared,
        "derived_from_displayed_full_action": False,
        "scope": "inserted EH benchmark only; the displayed action's full TT expansion is not performed",
    }


def _derive_circular_orbit(kernel: dict[str, Any]) -> dict[str, Any]:
    radius, period, a0, G, mass = sp.symbols(
        "r T a_0 G M_enclosed", positive=True
    )
    acceleration = 4 * sp.pi**2 * radius / period**2
    derived = sp.factor(
        radius**2
        * acceleration
        * (1 - sp.exp(-acceleration / a0))
    )
    displayed = sp.factor(
        4
        * sp.pi**2
        * radius**3
        / period**2
        * (1 - sp.exp(-4 * sp.pi**2 * radius / (a0 * period**2)))
    )
    y = kernel["y"]
    newton_ratio = 1 - sp.exp(-y)
    deep_ratio = (1 - sp.exp(-y)) / y
    return {
        "acceleration": acceleration,
        "derived_left_hand_side": derived,
        "displayed_left_hand_side": displayed,
        "equation": sp.Eq(displayed, G * mass),
        "period_law_residual": sp.simplify(derived - displayed),
        "newtonian_limit_residual": sp.simplify(
            sp.limit(newton_ratio, y, sp.oo) - 1
        ),
        "deep_mond_limit_residual": sp.simplify(
            sp.limit(deep_ratio, y, 0, dir="+") - 1
        ),
        "conditional_corollary_not_radially_varied_here": True,
    }


def derive_hpi_delta_gate() -> dict[str, Any]:
    kernel = _derive_kernel()
    weak_static = _derive_weak_static(kernel)
    restored = _derive_gauge_restored_chain()
    gauge_fixed = _derive_spatial_gauge_fixed_chain()
    zero_field = _derive_exact_zero_field_branch()
    zero_field["rank_bifurcation"] = (
        zero_field["poisson_rank"] != gauge_fixed["poisson_rank"]
    )
    no_constraint = _derive_no_constraint_mutation()
    k_zero, mutations = _derive_k_zero_and_mutations(kernel, no_constraint)

    C_pi = "D^2(pi/sqrt(h))"
    return {
        "action_text": ACTION,
        "action": {
            "C_pi": C_pi,
            "auxiliary_constraints": (C_pi,),
            "has_inserted_slip_constraint": False,
            "has_lagrangian_K_multiplier": False,
            "clock_sector": "S_clock=0; preferred foliation is nondynamical in this prototype",
        },
        "kernel": kernel,
        "weak_static": weak_static,
        "finite_k": {
            "generic_positive_gradient": restored,
            "spatial_gauge_fixed": gauge_fixed,
            "exact_zero_field": zero_field,
        },
        "k_zero": k_zero,
        "mutations": mutations,
        "matter_ward": _derive_matter_ward(),
        "tensor": _derive_tensor_block(),
        "circular_orbit": _derive_circular_orbit(kernel),
        "prior_art": {
            "arXiv:2011.00805": "auxiliary constraint may contain sqrt(h) D^2(pi/sqrt(h))",
            "arXiv:2607.26031": "Laplacian multiplier mechanism removes homogeneous multiplier modes",
        },
        "scope": {
            "finite_k_quadratic_scalar_chain": True,
            "finite_k_constant_gradient_principal_block_only": True,
            "finite_k_mode_aligned_with_background_gradient": True,
            "weak_static_leading_order": True,
            "weak_static_one_dimensional_only": True,
            "full_nonlinear_functional_dirac_theorem": False,
            "covariant_clock_completion": False,
            "inhomogeneous_stability_certified": False,
            "tensor_sector_certified": False,
            "ordinary_matter_ward_from_explicit_Sm": False,
            "flrw_background_or_perturbations_derived": False,
            "ppn_certified": False,
            "novelty_claimed": False,
            "candidate_status": "OPEN",
        },
    }


def _main() -> int:
    result = derive_hpi_delta_gate()
    generic = result["finite_k"]["generic_positive_gradient"]
    fixed = result["finite_k"]["spatial_gauge_fixed"]
    zero = result["finite_k"]["exact_zero_field"]
    checks = {
        "exact exponential mu": result["kernel"]["modulus_residual"] == 0,
        "weak-static no slip is varied": result["weak_static"]["no_slip_residual"] == 0,
        "lapse equation becomes AQUAL": result["weak_static"]["E_Phi_on_derived_slip_residual"] == 0,
        "C_pi preservation produces no slip": generic["trace_preservation_slip_residual"] == 0,
        "generic PB rank cross-check": generic["poisson_rank"] == generic["poisson_sample_rank"],
        "generic constraint independence": generic["constraint_jacobian_rank"] == len(generic["constraints"]),
        "generic scalar pair removed": generic["configuration_dof"] == 0,
        "gauge-fixed cross-check": fixed["configuration_dof"] == generic["configuration_dof"],
        "final chain closes": all(value == 0 for value in generic["final_preservation_residuals"]),
        "zero-field branch recomputed": zero["rank_bifurcation"],
        "zero-field source obstruction exposed": zero["source_obstruction_requires_vacuum"],
        "homogeneous symbol does not freeze expansion": result["k_zero"]["C_pi_does_not_algebraically_force_H_zero"],
        "no-laplacian mutation freezes FLRW": result["mutations"]["no_laplacian"]["forces_H_zero"],
        "lambda-K mutation freezes FLRW": result["mutations"]["lagrangian_lambda_K"]["forces_H_zero"],
        "removing C_pi restores scalar": result["mutations"]["remove_trace_constraint"]["configuration_dof"] > generic["configuration_dof"],
        "conditional minimal-matter Ward template": result["matter_ward"]["on_shell_divergence"] == 0,
    }
    print("=" * 78)
    print("CDE-HPI-DELTA: ONE TRACE-MOMENTUM CONSTRAINT GATE")
    print("=" * 78)
    for label, passed in checks.items():
        print(("[PASS] " if passed else "[FAIL] ") + label)
    print("\nGenerated finite-k chains:")
    print("  gauge restored constraints =", generic["constraints"])
    print("  gauge restored PB rank/J rank/DOF =", generic["poisson_rank"], generic["constraint_jacobian_rank"], generic["configuration_dof"])
    print("  gauge-fixed constraints =", fixed["constraints"])
    print("  gauge-fixed det(PB) =", fixed["poisson_determinant"])
    print("  exact-y=0 PB rank/J rank/DOF =", zero["poisson_rank"], zero["constraint_jacobian_rank"], zero["configuration_dof"])
    print("\nStrongest result:")
    print("  For k!=0 and lambda_parallel>0, C_pi preservation generates")
    print("  dot(C_pi)=2 A k^4(Phi-Psi); the completed quadratic chain has")
    print("  no scalar canonical pair. In the separate one-dimensional weak-static")
    print("  reduction, the varied lapse equation becomes exact exponential AQUAL")
    print("  after that derived no-slip law.")
    print("  At exact y=0 with a retained source, consistency instead forces J_rho=0.")
    print("\nCaveat:")
    print("  Rank bifurcates at y=0. The k=0 result is only a constraint-symbol")
    print("  check; radial variation, explicit matter Ward, full tensor expansion,")
    print("  nonlinear functional Dirac, clock, FLRW perturbations, boosted PPN,")
    print("  and full stability are not certified. Status: OPEN.")
    summary = {
        "status": result["scope"]["candidate_status"],
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "generic_pb_rank": generic["poisson_rank"],
        "generic_jacobian_rank": generic["constraint_jacobian_rank"],
        "generic_scalar_dof": str(generic["configuration_dof"]),
        "zero_field_pb_rank": zero["poisson_rank"],
        "zero_field_jacobian_rank": zero["constraint_jacobian_rank"],
        "zero_field_scalar_dof": str(zero["configuration_dof"]),
    }
    print("CERTIFICATE_JSON:", json.dumps(summary, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(_main())
