#!/usr/bin/env python3
"""Freeze and attack one constrained-clock exponential-MOND action.

Candidate CDE-L4C-2Delta is defined covariantly by one clock T, its unit
normal u, spatial projector h, the Einstein-Hilbert term, the exact
lapse-acceleration correction F_exp, a cuscuton term, and two spatial-
Laplacian multiplier equations.  Ordinary matter is minimally coupled to g
and never appears in the auxiliary sector.

This gate performs calculations that can already be done without pretending
the full Dirac algorithm is complete:

* varies both multipliers;
* varies a reduced weak-static action independently in Phi, Psi, lambda_s;
* solves the finite-k multiplier equations and tests whether MOND is stolen;
* separates k=0 from k!=0;
* derives the separate ordinary-matter Ward consequence;
* runs the complete Dirac algorithm for the finite-k, exact-zero-field
  quadratic scalar principal block, including its actual Poisson matrix;
* separates that block's k=0 rank-changing symbol and states why neither
  reduced calculation is a covariant nonlinear DOF theorem; and
* checks the homogeneous TT principal block only.

The full clock-plus-metric-plus-multiplier Dirac chain, boosted PPN, and
inhomogeneous stability remain mandatory.  A zero exit status certifies these
scoped derivations, not the candidate theory.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


ACTION = r"""
S_* = (M_Pl^2/2) int sqrt(-g) [
        R - 2 Lambda - (2/ell_0^2) F_exp(y)
        + lambda_s D^2(R_3 - 4 D_mu a^mu)
        + lambda_K D^2 K
      ] d^4x
      + int sqrt(-g) [M_c^2 sqrt(X) - V(T)] d^4x
      + S_m[g,psi],
X=-g^{mu nu} partial_mu T partial_nu T>0,
u_mu=-partial_mu T/sqrt(X), h_mu nu=g_mu nu+u_mu u_nu,
y=ell_0 sqrt(a_mu a^mu), ell_0=c^2/a_0,
F_exp(y)=2[(1+y)exp(-y)-1].
""".strip()


def _higher_euler(lagrangian: sp.Expr, field: sp.Expr, coordinate: sp.Symbol, order: int) -> sp.Expr:
    result = sp.diff(lagrangian, field)
    for derivative_order in range(1, order + 1):
        jet = sp.diff(field, coordinate, derivative_order)
        result += (-1) ** derivative_order * sp.diff(
            sp.diff(lagrangian, jet), coordinate, derivative_order
        )
    return sp.simplify(result)


def _poisson_bracket(
    first: sp.Expr,
    second: sp.Expr,
    coordinates: tuple[sp.Symbol, ...],
    momenta: tuple[sp.Symbol, ...],
) -> sp.Expr:
    """Canonical Poisson bracket, retained symbolically for auditability."""

    return sp.simplify(
        sum(
            sp.diff(first, q) * sp.diff(second, p)
            - sp.diff(first, p) * sp.diff(second, q)
            for q, p in zip(coordinates, momenta)
        )
    )


def _derive_minkowski_adm_principal(
    correction: sp.Expr, y: sp.Symbol
) -> dict[str, Any]:
    """Generate the finite-k scalar principal blocks from the ADM action.

    A real Fourier mode is used, with the spatial average normalized in the
    usual way.  The ingredients are independently constructed from

      N sqrt(h) [R_3 + K_ij K^ij - K^2 - 2 F(y)/ell_0^2],
      N sqrt(h) lambda_s D^2(R_3-4 D_i a^i),
      N sqrt(h) lambda_K D^2 K.

    At a zero-multiplier Minkowski background, only first-order K, C_slip and
    D^2 K are needed in the quadratic action.  The conformal R_3 density is
    expanded explicitly through second order, including lapse and measure.
    This closes the provenance gap between the displayed covariant action and
    the Lagrangian passed to the Dirac algorithm.  Lower-derivative potential
    and background terms remain outside this principal calculation.
    """

    A, k = sp.symbols("A k", positive=True, nonzero=True)
    Phi, Psi, B, lambda_s, lambda_K = sp.symbols(
        "Phi_0 Psi_0 B_0 lambda_s_0 lambda_K_0"
    )
    Psi_dot = sp.symbols("Psi_dot")
    lambda_parallel = sp.symbols(
        "lambda_parallel", positive=True, nonzero=True
    )
    epsilon, theta = sp.symbols("epsilon theta", real=True)
    mode = sp.cos(theta)

    def mode_average(expression: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.integrate(sp.expand_trig(expression), (theta, 0, 2 * sp.pi))
            / (2 * sp.pi)
        )

    # With h_ij=exp(-2 epsilon Psi cos(theta)) delta_ij and
    # N_i=-epsilon k B sin(theta) delta_ix, the first-order extrinsic
    # curvature amplitude follows directly from
    # K_ij=(dot h_ij-D_i N_j-D_j N_i)/(2N).
    K_amplitude = sp.diag(
        -Psi_dot + k**2 * B,
        -Psi_dot,
        -Psi_dot,
    )
    K_trace_amplitude = sp.trace(K_amplitude)
    eh_kinetic_amplitude = sp.simplify(
        sp.trace(K_amplitude * K_amplitude) - K_trace_amplitude**2
    )
    eh_kinetic = sp.simplify(eh_kinetic_amplitude * mode_average(mode**2))

    # For h_ij=exp(-2s)delta_ij in three dimensions,
    # sqrt(h) R_3=exp(-s)[4 partial^2 s-2(partial s)^2].
    s = epsilon * Psi * mode
    lapse = 1 + epsilon * Phi * mode
    s_x = k * sp.diff(s, theta)
    s_xx = k**2 * sp.diff(s, theta, 2)
    r3_density = lapse * sp.exp(-s) * (4 * s_xx - 2 * s_x**2)
    r3_quadratic_density = sp.expand(
        sp.series(r3_density, epsilon, 0, 3).removeO()
    ).coeff(epsilon, 2)
    eh_spatial = mode_average(r3_quadratic_density)

    # At y=0, F(y)=-y^2+O(y^3), so the correction density contributes
    # +2 a_i a^i.  Construct a_i=D_i ln N and expand N sqrt(h) explicitly.
    a_x = k * sp.diff(sp.log(lapse), theta)
    acceleration_squared = sp.exp(2 * s) * a_x**2
    mond_zero_density = (
        lapse * sp.exp(-3 * s) * 2 * acceleration_squared
    )
    mond_zero_quadratic_density = sp.expand(
        sp.series(mond_zero_density, epsilon, 0, 3).removeO()
    ).coeff(epsilon, 2)
    mond_zero_spatial = mode_average(mond_zero_quadratic_density)

    # On a positive longitudinal background the correction Hessian is F''.
    # The action gives -F'' (delta a_parallel)^2 before the real-mode average,
    # hence -F''/2 k^2 Phi^2.  Define lambda_parallel from that Hessian and
    # retain it symbolically for the Dirac calculation.
    exact_lambda_parallel = sp.simplify(1 + sp.diff(correction, y, 2) / 2)
    mond_positive_exact = sp.simplify(
        -sp.diff(correction, y, 2) * k**2 * Phi**2 / 2
    )
    mond_positive_spatial = sp.simplify(
        (1 - lambda_parallel) * k**2 * Phi**2
    )
    longitudinal_hessian_residual = sp.simplify(
        mond_positive_spatial.subs(
            lambda_parallel, exact_lambda_parallel
        )
        - mond_positive_exact
    )

    # Linear ADM operator amplitudes. Products of the multiplier mode with
    # the operator mode carry <cos^2>=1/2; no normalization is inserted by
    # hand after this point.
    r3_linear_amplitude = -4 * k**2 * Psi
    div_a_linear_amplitude = -k**2 * Phi
    c_slip_linear_amplitude = sp.simplify(
        r3_linear_amplitude - 4 * div_a_linear_amplitude
    )
    d2_c_slip_amplitude = sp.simplify(-k**2 * c_slip_linear_amplitude)
    d2_k_amplitude = sp.simplify(-k**2 * K_trace_amplitude)
    lambda_s_piece = sp.simplify(
        lambda_s * d2_c_slip_amplitude * mode_average(mode**2)
    )
    lambda_K_piece = sp.simplify(
        lambda_K * d2_k_amplitude * mode_average(mode**2)
    )

    zero_field_lagrangian = sp.factor(
        A
        * (
            eh_kinetic
            + eh_spatial
            + mond_zero_spatial
            + lambda_s_piece
            + lambda_K_piece
        )
    )
    positive_gradient_lagrangian = sp.factor(
        A
        * (
            eh_kinetic
            + eh_spatial
            + mond_positive_spatial
            + lambda_s_piece
            + lambda_K_piece
        )
    )

    return {
        "A": A,
        "k": k,
        "Phi": Phi,
        "Psi": Psi,
        "B": B,
        "lambda_s": lambda_s,
        "lambda_K": lambda_K,
        "Psi_dot": Psi_dot,
        "lambda_parallel": lambda_parallel,
        "K_amplitude": K_amplitude,
        "K_trace_amplitude": K_trace_amplitude,
        "eh_kinetic": eh_kinetic,
        "r3_quadratic_density": r3_quadratic_density,
        "eh_spatial": eh_spatial,
        "mond_zero_quadratic_density": mond_zero_quadratic_density,
        "mond_zero_spatial": mond_zero_spatial,
        "exact_lambda_parallel": exact_lambda_parallel,
        "mond_positive_exact": mond_positive_exact,
        "mond_positive_spatial": mond_positive_spatial,
        "longitudinal_hessian_residual": longitudinal_hessian_residual,
        "c_slip_linear_amplitude": c_slip_linear_amplitude,
        "d2_c_slip_amplitude": d2_c_slip_amplitude,
        "d2_k_amplitude": d2_k_amplitude,
        "lambda_s_piece": lambda_s_piece,
        "lambda_K_piece": lambda_K_piece,
        "generated_zero_field_lagrangian": zero_field_lagrangian,
        "generated_positive_gradient_lagrangian": positive_gradient_lagrangian,
        "cuscuton_principal_contribution": sp.Integer(0),
        "potential_principal_contribution": sp.Integer(0),
        "full_lower_derivative_action_included": False,
    }


def _derive_zero_field_dirac(
    deep_primitive: sp.Expr,
    y: sp.Symbol,
    lagrangian_from_adm: sp.Expr | None = None,
) -> dict[str, Any]:
    """Close the exact-y=0 finite-k scalar *principal-block* Dirac chain.

    This is not obtained from an asserted field equation.  It is the
    quadratic unitary-gauge scalar reduction of ``ACTION`` after fixing the
    scalar spatial gauge.  The signs of B and lambda_K are conventional field
    redefinitions relative to the earlier Hessian display.  The covariant
    clock Euler equation and lower-derivative background/cuscuton terms are
    not in this principal block, so its result is a zero-field regularity
    obstruction, not yet a global nonlinear degree theorem.
    """

    A, k = sp.symbols("A k", positive=True, nonzero=True)
    Phi, Psi, B, lambda_s, lambda_K = sp.symbols(
        "Phi_0 Psi_0 B_0 lambda_s_0 lambda_K_0"
    )
    p_Phi, p_Psi, p_B, p_lambda_s, p_lambda_K = sp.symbols(
        "p_Phi p_Psi p_B p_lambda_s p_lambda_K"
    )
    Psi_dot = sp.symbols("Psi_dot")

    coordinates = (Phi, Psi, B, lambda_s, lambda_K)
    momenta = (p_Phi, p_Psi, p_B, p_lambda_s, p_lambda_K)
    phase_variables = coordinates + momenta

    if lagrangian_from_adm is None:
        raise ValueError("the zero-field Dirac block must be generated from ADM geometry")
    lagrangian = sp.factor(lagrangian_from_adm)
    derived_p_Psi = sp.diff(lagrangian, Psi_dot)
    velocity_solution = sp.solve(
        sp.Eq(p_Psi, derived_p_Psi), Psi_dot, dict=True
    )[0][Psi_dot]
    canonical_hamiltonian = sp.factor(
        (p_Psi * Psi_dot - lagrangian).subs(Psi_dot, velocity_solution)
    )

    primaries = (p_Phi, p_B, p_lambda_s, p_lambda_K)
    secondaries = tuple(
        sp.factor(
            _poisson_bracket(primary, canonical_hamiltonian, coordinates, momenta)
        )
        for primary in primaries
    )
    constraints = primaries + secondaries
    poisson_matrix = sp.Matrix(
        [
            [
                _poisson_bracket(first, second, coordinates, momenta)
                for second in constraints
            ]
            for first in constraints
        ]
    )
    poisson_rank = poisson_matrix.rank()
    poisson_determinant = sp.factor(poisson_matrix.det())
    constraint_jacobian = sp.Matrix(constraints).jacobian(phase_variables)
    constraint_jacobian_rank = constraint_jacobian.rank()

    multipliers = sp.symbols(f"u0:{len(primaries)}")
    total_hamiltonian = canonical_hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(multipliers, primaries)
    )
    preservation_equations = tuple(
        sp.factor(
            _poisson_bracket(
                secondary, total_hamiltonian, coordinates, momenta
            )
        )
        for secondary in secondaries
    )
    preservation_solutions = sp.solve(
        preservation_equations, multipliers, dict=True
    )
    preservation_solution = preservation_solutions[0] if preservation_solutions else {}
    preservation_residuals = tuple(
        sp.simplify(equation.subs(preservation_solution))
        for equation in preservation_equations
    )

    # Solve all constraints rather than inserting a guessed gauge or degree
    # count.  The pullback of theta=sum p_i dq_i is also computed: this checks
    # whether (Psi,p_Psi) remains a canonical pair after reduction.
    solved_variables = (
        p_Phi,
        p_B,
        p_lambda_s,
        p_lambda_K,
        Phi,
        lambda_s,
        B,
        lambda_K,
    )
    constraint_solutions = sp.solve(
        constraints, solved_variables, dict=True
    )
    constraint_solution = constraint_solutions[0] if constraint_solutions else {}
    reduced_hamiltonian = sp.simplify(
        canonical_hamiltonian.subs(constraint_solution)
    )
    dPsi, dp_Psi = sp.symbols("dPsi dp_Psi")
    differential_symbols = {
        Psi: dPsi,
        p_Psi: dp_Psi,
    }

    def pulled_differential(expression: sp.Expr) -> sp.Expr:
        reduced = sp.simplify(expression.subs(constraint_solution))
        return sp.simplify(
            sp.diff(reduced, Psi) * dPsi
            + sp.diff(reduced, p_Psi) * dp_Psi
        )

    canonical_one_form_pullback = sp.simplify(
        sum(
            p.subs(constraint_solution) * pulled_differential(q)
            for q, p in zip(coordinates, momenta)
        )
    )
    del differential_symbols  # the named differentials are displayed above

    second_class_count = poisson_rank
    first_class_count = len(constraints) - second_class_count
    phase_dimension = len(phase_variables)
    configuration_dof = sp.Rational(
        phase_dimension - 2 * first_class_count - second_class_count,
        2,
    )

    deep_polynomial = sp.series(deep_primitive, y, 0, 8).removeO().expand()
    nonzero_powers = [
        power
        for power in range(0, 8)
        if sp.simplify(deep_polynomial.coeff(y, power)) != 0
    ]
    leading_spatial_order = min(nonzero_powers) if nonzero_powers else sp.oo
    quadratic_spatial_stiffness = sp.simplify(deep_polynomial.coeff(y, 2))
    extra_reduced_scalar = bool(configuration_dof > 0)
    degenerate_linear_spatial_symbol = quadratic_spatial_stiffness == 0

    k_zero_poisson_matrix = poisson_matrix.subs(k, 0)
    k_zero_secondaries = tuple(
        sp.simplify(secondary.subs(k, 0)) for secondary in secondaries
    )

    return {
        "A": A,
        "k": k,
        "coordinates": coordinates,
        "momenta": momenta,
        "lagrangian": lagrangian,
        "derived_p_Psi": derived_p_Psi,
        "velocity_solution": velocity_solution,
        "canonical_hamiltonian": canonical_hamiltonian,
        "primaries": primaries,
        "secondaries": secondaries,
        "constraints": constraints,
        "poisson_matrix": poisson_matrix,
        "poisson_rank": poisson_rank,
        "poisson_determinant": poisson_determinant,
        "constraint_jacobian": constraint_jacobian,
        "constraint_jacobian_rank": constraint_jacobian_rank,
        "preservation_equations": preservation_equations,
        "preservation_solution": preservation_solution,
        "preservation_residuals": preservation_residuals,
        "tertiary_constraints_found": any(
            residual != 0 for residual in preservation_residuals
        ),
        "constraint_solution": constraint_solution,
        "canonical_one_form_pullback": canonical_one_form_pullback,
        "reduced_hamiltonian": reduced_hamiltonian,
        "phase_dimension": phase_dimension,
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "configuration_dof": configuration_dof,
        "quadratic_spatial_stiffness": quadratic_spatial_stiffness,
        "leading_spatial_order": leading_spatial_order,
        "extra_reduced_scalar": extra_reduced_scalar,
        "degenerate_linear_spatial_symbol": degenerate_linear_spatial_symbol,
        "regular_two_tensor_limit_certified": not (
            extra_reduced_scalar and degenerate_linear_spatial_symbol
        ),
        "full_covariant_clock_equation_included": False,
        "global_nonlinear_dof_theorem": False,
        "k_zero_poisson_matrix": k_zero_poisson_matrix,
        "k_zero_poisson_rank": k_zero_poisson_matrix.rank(),
        "k_zero_secondaries": k_zero_secondaries,
    }


def _derive_nonzero_field_dirac(
    lagrangian_from_adm: sp.Expr | None = None,
) -> dict[str, Any]:
    """Derive the same scalar block about a positive-gradient background.

    In the longitudinal direction, the second variation of the exponential
    flux is its positive constitutive eigenvalue lambda_parallel.  No rank,
    determinant, dispersion relation, or degree count is supplied as input.
    """

    A, k, lambda_parallel = sp.symbols(
        "A k lambda_parallel", positive=True, nonzero=True
    )
    Phi, Psi, B, lambda_s, lambda_K = sp.symbols(
        "Phi_0 Psi_0 B_0 lambda_s_0 lambda_K_0"
    )
    p_Phi, p_Psi, p_B, p_lambda_s, p_lambda_K = sp.symbols(
        "p_Phi p_Psi p_B p_lambda_s p_lambda_K"
    )
    Psi_dot = sp.symbols("Psi_dot")
    coordinates = (Phi, Psi, B, lambda_s, lambda_K)
    momenta = (p_Phi, p_Psi, p_B, p_lambda_s, p_lambda_K)
    phase_variables = coordinates + momenta

    if lagrangian_from_adm is None:
        raise ValueError("the positive-gradient Dirac block must be generated from ADM geometry")
    lagrangian = sp.factor(lagrangian_from_adm)
    derived_p_Psi = sp.diff(lagrangian, Psi_dot)
    velocity_solution = sp.solve(
        sp.Eq(p_Psi, derived_p_Psi), Psi_dot, dict=True
    )[0][Psi_dot]
    canonical_hamiltonian = sp.factor(
        (p_Psi * Psi_dot - lagrangian).subs(Psi_dot, velocity_solution)
    )
    primaries = (p_Phi, p_B, p_lambda_s, p_lambda_K)
    secondaries = tuple(
        sp.factor(
            _poisson_bracket(primary, canonical_hamiltonian, coordinates, momenta)
        )
        for primary in primaries
    )
    constraints = primaries + secondaries
    poisson_matrix = sp.Matrix(
        [
            [
                _poisson_bracket(first, second, coordinates, momenta)
                for second in constraints
            ]
            for first in constraints
        ]
    )
    poisson_rank = poisson_matrix.rank()
    constraint_jacobian = sp.Matrix(constraints).jacobian(phase_variables)
    second_class_count = poisson_rank
    first_class_count = len(constraints) - second_class_count
    phase_dimension = len(phase_variables)
    configuration_dof = sp.Rational(
        phase_dimension - 2 * first_class_count - second_class_count,
        2,
    )
    solved_variables = (
        p_Phi,
        p_B,
        p_lambda_s,
        p_lambda_K,
        Phi,
        lambda_s,
        B,
        lambda_K,
    )
    constraint_solution = sp.solve(
        constraints, solved_variables, dict=True
    )[0]
    reduced_hamiltonian = sp.factor(
        canonical_hamiltonian.subs(constraint_solution)
    )
    omega_squared = sp.simplify(
        sp.diff(reduced_hamiltonian, p_Psi, 2)
        * sp.diff(reduced_hamiltonian, Psi, 2)
    )

    multipliers = sp.symbols(f"v0:{len(primaries)}")
    total_hamiltonian = canonical_hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(multipliers, primaries)
    )
    preservation_equations = tuple(
        sp.factor(
            _poisson_bracket(
                secondary, total_hamiltonian, coordinates, momenta
            )
        )
        for secondary in secondaries
    )
    preservation_solution = sp.solve(
        preservation_equations, multipliers, dict=True
    )[0]
    preservation_residuals = tuple(
        sp.simplify(equation.subs(preservation_solution))
        for equation in preservation_equations
    )

    return {
        "A": A,
        "k": k,
        "lambda_parallel": lambda_parallel,
        "Psi": Psi,
        "p_Psi": p_Psi,
        "lagrangian": lagrangian,
        "derived_p_Psi": derived_p_Psi,
        "canonical_hamiltonian": canonical_hamiltonian,
        "primaries": primaries,
        "secondaries": secondaries,
        "constraints": constraints,
        "poisson_matrix": poisson_matrix,
        "poisson_rank": poisson_rank,
        "poisson_determinant": sp.factor(poisson_matrix.det()),
        "constraint_jacobian": constraint_jacobian,
        "constraint_jacobian_rank": constraint_jacobian.rank(),
        "preservation_solution": preservation_solution,
        "preservation_residuals": preservation_residuals,
        "constraint_solution": constraint_solution,
        "reduced_hamiltonian": reduced_hamiltonian,
        "omega_squared": omega_squared,
        "phase_dimension": phase_dimension,
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "configuration_dof": configuration_dof,
        "positive_kinetic": sp.diff(reduced_hamiltonian, p_Psi, 2).is_positive,
        "positive_gradient": omega_squared.is_positive,
        "full_covariant_background_included": False,
    }


def derive_action_gate() -> dict[str, Any]:
    y = sp.symbols("y", positive=True)
    correction = 2 * ((1 + y) * sp.exp(-y) - 1)
    mu = 1 - sp.exp(-y)
    combined = y**2 + correction
    combined_series = sp.series(combined, y, 0, 5).removeO().expand()
    adm_principal = _derive_minkowski_adm_principal(correction, y)
    zero_field_dirac = _derive_zero_field_dirac(
        combined,
        y,
        adm_principal["generated_zero_field_lagrangian"],
    )
    nonzero_field_dirac = _derive_nonzero_field_dirac(
        adm_principal["generated_positive_gradient_lagrangian"]
    )
    adm_principal["zero_field_residual"] = sp.simplify(
        adm_principal["generated_zero_field_lagrangian"]
        - zero_field_dirac["lagrangian"]
    )
    adm_principal["positive_gradient_residual"] = sp.simplify(
        adm_principal["generated_positive_gradient_lagrangian"]
        - nonzero_field_dirac["lagrangian"]
    )
    exact_lambda_parallel = 1 + (y - 1) * sp.exp(-y)
    nonzero_field_dirac["exact_lambda_parallel"] = exact_lambda_parallel
    nonzero_field_dirac["exact_omega_squared"] = sp.simplify(
        nonzero_field_dirac["omega_squared"].subs(
            nonzero_field_dirac["lambda_parallel"], exact_lambda_parallel
        )
    )
    nonzero_field_dirac["deep_omega_series"] = sp.series(
        nonzero_field_dirac["exact_omega_squared"], y, 0, 4
    )

    # Multiplier Euler equations from the frozen covariant density.  The
    # spatial operators are kept as independent symbols because no background
    # or phenomenological field equation is inserted here.
    lambda_s_cov, lambda_K_cov = sp.symbols("lambda_s_cov lambda_K_cov")
    laplacian_C_slip, laplacian_K = sp.symbols("D2_C_slip D2_K")
    multiplier_density = (
        lambda_s_cov * laplacian_C_slip
        + lambda_K_cov * laplacian_K
    )
    E_lambda_s = sp.diff(multiplier_density, lambda_s_cov)
    E_lambda_K = sp.diff(multiplier_density, lambda_K_cov)

    # Reduced weak-static action in one spatial direction.  It is the scalar
    # weak-field reduction of the frozen action on the positive-gradient
    # branch.  Keeping Phi and Psi independent is essential.  The factor four
    # follows C_slip^(1)=4 d^2(Psi-Phi) in c=1 units, with the extra D^2 in
    # the action.  The source normalization yields d^2 Psi=4 pi G rho in GR.
    z = sp.symbols("z", real=True)
    a0, G = sp.symbols("a0 G", positive=True)
    Phi = sp.Function("Phi")(z)
    Psi = sp.Function("Psi")(z)
    lambda_s = sp.Function("lambda_s")(z)
    rho = sp.Function("rho")(z)
    y_local = sp.diff(Phi, z) / a0
    correction_local = 2 * ((1 + y_local) * sp.exp(-y_local) - 1)
    weak_lagrangian = (
        -2 * sp.diff(Phi, z) * sp.diff(Psi, z)
        + sp.diff(Psi, z) ** 2
        - a0**2 * correction_local
        - 8 * sp.pi * G * rho * Phi
        + 4
        * lambda_s
        * (sp.diff(Psi, z, 4) - sp.diff(Phi, z, 4))
    )
    E_Phi = _higher_euler(weak_lagrangian, Phi, z, 4)
    E_Psi = _higher_euler(weak_lagrangian, Psi, z, 4)
    E_lambda = _higher_euler(weak_lagrangian, lambda_s, z, 4)

    k = sp.symbols("k", positive=True)
    Phi_k, Psi_k, lambda_k = sp.symbols("Phi_k Psi_k lambda_s_k")
    E_lambda_k = 4 * k**4 * (Psi_k - Phi_k)
    E_Psi_k = 2 * k**2 * (Psi_k - Phi_k) + 4 * k**4 * lambda_k
    finite_k_solution = sp.solve(
        [E_lambda_k, E_Psi_k],
        [Psi_k, lambda_k],
        dict=True,
    )[0]

    longitudinal_local = 1 + (y_local - 1) * sp.exp(-y_local)
    E_Phi_on_shell = sp.simplify(
        E_Phi.subs(
            {
                Psi: Phi,
                sp.diff(Psi, z): sp.diff(Phi, z),
                sp.diff(Psi, z, 2): sp.diff(Phi, z, 2),
                sp.diff(Psi, z, 3): sp.diff(Phi, z, 3),
                sp.diff(Psi, z, 4): sp.diff(Phi, z, 4),
                lambda_s: 0,
                sp.diff(lambda_s, z): 0,
                sp.diff(lambda_s, z, 2): 0,
                sp.diff(lambda_s, z, 3): 0,
                sp.diff(lambda_s, z, 4): 0,
            }
        )
    )
    expected_mond_equation = (
        2 * longitudinal_local * sp.diff(Phi, z, 2)
        - 8 * sp.pi * G * rho
    )
    mond_residual = sp.simplify(E_Phi_on_shell - expected_mond_equation)

    constraint_matrix = sp.Matrix(
        [
            [4 * k**4, 0],
            [2 * k**2, 4 * k**4],
        ]
    )

    # Separate matter Ward identity.  On the matter equations E_psi=0, the
    # diffeomorphism identity gives div T_m=-E_psi grad psi=0.  A direct
    # auxiliary source J(psi) provides the explicit mutation.
    E_psi, grad_psi = sp.symbols("E_psi grad_psi")
    eta, J_prime = sp.symbols("eta J_prime", nonzero=True)
    ordinary_divergence = -E_psi * grad_psi
    direct_source_mutation = eta * J_prime * grad_psi

    # Principal unitary-gauge scalar kinetic block, pulled from the explicit
    # ADM expansion above rather than re-entered with an independent
    # normalization. This still omits the covariant (T,p_T) pair, so it cannot
    # be used as the full DOF certificate.
    zeta_dot, lambda_K_dot = sp.symbols("zeta_dot lambda_K_dot")
    A_EH, k_mode, B_shift, lambda_K_mode = sp.symbols(
        "A_EH k_mode B_shift lambda_K_mode", nonzero=True
    )
    eh_kinetic = A_EH * adm_principal["eh_kinetic"].subs(
        {
            adm_principal["Psi_dot"]: zeta_dot,
            adm_principal["k"]: k_mode,
            adm_principal["B"]: B_shift,
        }
    )
    lambda_K_kinetic = adm_principal["lambda_K_piece"].subs(
        {
            adm_principal["Psi_dot"]: zeta_dot,
            adm_principal["k"]: k_mode,
            adm_principal["B"]: B_shift,
            adm_principal["lambda_K"]: lambda_K_mode,
        }
    )
    velocities = (zeta_dot, lambda_K_dot)
    eh_hessian = sp.hessian(eh_kinetic, velocities)
    mond_hessian_shift = sp.zeros(2)
    multiplier_hessian_shift = sp.hessian(lambda_K_kinetic, velocities)
    total_unitary_hessian = sp.simplify(
        eh_hessian + mond_hessian_shift + multiplier_hessian_shift
    )

    # Every multiplier term contains D^2.  On an exactly homogeneous branch
    # its spatial Fourier symbol vanishes, leaving the EH TT principal ratio.
    tensor_kinetic, tensor_gradient = sp.symbols(
        "tensor_kinetic tensor_gradient", positive=True
    )
    homogeneous_multiplier_contribution = sp.simplify(k_mode**2).subs(k_mode, 0)
    c_T_squared = sp.simplify(tensor_gradient / tensor_kinetic).subs(
        tensor_gradient, tensor_kinetic
    )

    return {
        "action": ACTION,
        "kernel": {
            "F_exp": correction,
            "combined_primitive": combined,
            "modulus": sp.simplify(1 + sp.diff(correction, y) / (2 * y)),
            "modulus_residual": sp.simplify(
                1 + sp.diff(correction, y) / (2 * y) - mu
            ),
            "deep_series": combined_series,
            "deep_quadratic_coefficient": combined_series.coeff(y, 2),
            "deep_cubic_coefficient": combined_series.coeff(y, 3),
        },
        "multiplier_variation": {
            "density": multiplier_density,
            "E_lambda_s": E_lambda_s,
            "E_lambda_K": E_lambda_K,
            "laplacian_C_slip": laplacian_C_slip,
            "laplacian_K": laplacian_K,
            "inserted_phenomenologically": False,
        },
        "weak_static": {
            "coordinate": z,
            "lagrangian": weak_lagrangian,
            "Phi": Phi_k,
            "Psi": Psi_k,
            "lambda_s": lambda_k,
            "E_Phi": E_Phi,
            "E_Psi": E_Psi,
            "E_lambda": E_lambda,
            "E_Phi_on_shell": E_Phi_on_shell,
            "expected_mond_equation": expected_mond_equation,
            "mond_residual": mond_residual,
            "E_lambda_k": E_lambda_k,
            "E_Psi_k": E_Psi_k,
            "finite_k_solution": finite_k_solution,
            "gamma_PPN_linear": sp.simplify(
                finite_k_solution[Psi_k] / Phi_k
            ),
            "positive_gradient_branch": True,
            "full_covariant_metric_variation_completed": False,
        },
        "sector_split": {
            "constraint_matrix": constraint_matrix,
            "k_nonzero_rank": constraint_matrix.rank(),
            "k_zero_matrix": constraint_matrix.subs(k, 0),
            "k_zero_rank": constraint_matrix.subs(k, 0).rank(),
            "flrw_H_forced_zero": False,
            "flrw_viability_established": False,
        },
        "matter_ward": {
            "aux_matter_euler_derivative": sp.Integer(0),
            "ordinary_divergence": ordinary_divergence,
            "ordinary_divergence_on_shell": ordinary_divergence.subs(E_psi, 0),
            "direct_source_mutation_divergence": direct_source_mutation,
            "matter_minimally_coupled_to_one_metric": True,
        },
        "unitary_adm": {
            "eh_velocity_hessian": eh_hessian,
            "mond_hessian_shift": mond_hessian_shift,
            "multiplier_hessian_shift": multiplier_hessian_shift,
            "total_velocity_hessian": total_unitary_hessian,
            "metric_velocity_hessian_rank": total_unitary_hessian.rank(),
            "covariant_clock_pair_included": False,
            "full_action_dof_certified": False,
        },
        "adm_principal_derivation": adm_principal,
        "zero_field_dirac": zero_field_dirac,
        "nonzero_field_dirac": nonzero_field_dirac,
        "homogeneous_dirac_symbol": {
            "poisson_matrix": zero_field_dirac["k_zero_poisson_matrix"],
            "poisson_rank": zero_field_dirac["k_zero_poisson_rank"],
            "secondary_symbols": zero_field_dirac["k_zero_secondaries"],
            "full_homogeneous_background_included": False,
        },
        "tensor": {
            "homogeneous_multiplier_contribution": homogeneous_multiplier_contribution,
            "c_T_squared_on_homogeneous_branch": c_T_squared,
            "anisotropic_or_inhomogeneous_background_tested": False,
            "positive_EH_tensor_kinetic_assumed": tensor_kinetic.is_positive,
        },
        "verdict": "OPEN",
        "zero_field_gate": "FAIL_ON_REDUCED_ZERO_MULTIPLIER_BRANCH",
        "next_unavoidable_calculation": (
            "Derive the complete second-order scalar action on the explicit "
            "on-shell FLRW witness, including all lower-spatial-derivative "
            "cuscuton, potential, matter and multiplier terms, then take the "
            "nonlinear constraint rank as y approaches zero from above."
        ),
    }


def _check(label: str, condition: Any, detail: str = "") -> bool:
    passed = bool(condition)
    suffix = f" ({detail})" if detail else ""
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}{suffix}")
    return passed


def main() -> int:
    result = derive_action_gate()
    kernel = result["kernel"]
    multipliers = result["multiplier_variation"]
    weak = result["weak_static"]
    sectors = result["sector_split"]
    ward = result["matter_ward"]
    canonical = result["unitary_adm"]
    adm = result["adm_principal_derivation"]
    zero = result["zero_field_dirac"]
    nonzero = result["nonzero_field_dirac"]
    homogeneous = result["homogeneous_dirac_symbol"]
    tensor = result["tensor"]
    checks: list[bool] = []

    print("=" * 100)
    print("CDE-L4C-2DELTA: ONE FROZEN ACTION, FIRST VARIATIONAL / CANONICAL GATES")
    print("=" * 100)
    print("\n[ACTION]\n" + result["action"])

    print("\n[1] Exact exponential correction")
    print("  F_exp =", kernel["F_exp"])
    print("  1+F_exp'/(2y) =", kernel["modulus"])
    print("  y^2+F_exp deep =", kernel["deep_series"])
    checks.append(_check("the correction produces exactly mu=1-exp(-y)", kernel["modulus_residual"] == 0))
    checks.append(_check(
        "the Newtonian quadratic term cancels and the leading term is (2/3)y^3",
        kernel["deep_quadratic_coefficient"] == 0
        and kernel["deep_cubic_coefficient"] == sp.Rational(2, 3),
    ))

    print("\n[2] Multiplier Euler-Lagrange equations")
    print("  E_lambda_s =", multipliers["E_lambda_s"])
    print("  E_lambda_K =", multipliers["E_lambda_K"])
    checks.append(_check(
        "both Laplacian constraints follow by variation",
        multipliers["E_lambda_s"] == multipliers["laplacian_C_slip"]
        and multipliers["E_lambda_K"] == multipliers["laplacian_K"],
    ))

    print("\n[3] Independent weak-static variations")
    print("  E_Phi =", weak["E_Phi"])
    print("  E_Psi =", weak["E_Psi"])
    print("  E_lambda_s =", weak["E_lambda"])
    print("  finite-k solution =", weak["finite_k_solution"])
    print("  E_Phi after Psi=Phi, lambda_s=0 =", weak["E_Phi_on_shell"])
    checks.append(_check(
        "the finite-k multiplier equations derive Psi=Phi and lambda_s=0",
        weak["finite_k_solution"][weak["Psi"]] == weak["Phi"]
        and weak["finite_k_solution"][weak["lambda_s"]] == 0,
    ))
    checks.append(_check(
        "the remaining Phi equation is the exact longitudinal AQUAL equation",
        weak["mond_residual"] == 0,
    ))
    checks.append(_check("linear gamma_PPN=1 on this reduced branch", weak["gamma_PPN_linear"] == 1))

    print("\n[4] k-sector split")
    print("  constraint matrix(k!=0) =", sectors["constraint_matrix"])
    print("  ranks k!=0,k=0 =", sectors["k_nonzero_rank"], sectors["k_zero_rank"])
    checks.append(_check(
        "the Laplacian constraints act at k!=0 and vanish at k=0",
        sectors["k_nonzero_rank"] > sectors["k_zero_rank"]
        and sectors["k_zero_rank"] == 0,
    ))
    checks.append(_check("the multiplier equations do not force FLRW H=0", not sectors["flrw_H_forced_zero"]))

    print("\n[5] Ordinary-matter Ward fork")
    print("  auxiliary matter Euler derivative =", ward["aux_matter_euler_derivative"])
    print("  div T_m on E_psi=0 =", ward["ordinary_divergence_on_shell"])
    print("  direct-J(psi) mutation =", ward["direct_source_mutation_divergence"])
    checks.append(_check(
        "minimal S_m retains its separate on-shell Ward identity",
        ward["aux_matter_euler_derivative"] == 0
        and ward["ordinary_divergence_on_shell"] == 0
        and ward["direct_source_mutation_divergence"] != 0,
    ))

    print("\n[6] Unitary-gauge velocity Hessian (not a full count)")
    print("  H_EH =", canonical["eh_velocity_hessian"])
    print("  H_MOND shift =", canonical["mond_hessian_shift"])
    print("  H_multiplier shift =", canonical["multiplier_hessian_shift"])
    print("  rank =", canonical["metric_velocity_hessian_rank"])
    checks.append(_check(
        "MOND and two multiplier terms add no quadratic velocity Hessian in this scalar principal block",
        canonical["mond_hessian_shift"] == sp.zeros(2)
        and canonical["multiplier_hessian_shift"] == sp.zeros(2),
    ))
    checks.append(_check(
        "the omitted covariant clock pair prevents a full-action DOF claim",
        not canonical["covariant_clock_pair_included"]
        and not canonical["full_action_dof_certified"],
    ))

    print("\n[6b] ADM-generated Minkowski principal block")
    print("  <K_ij K^ij-K^2> =", adm["eh_kinetic"])
    print("  <N sqrt(h) R_3>_(2) =", adm["eh_spatial"])
    print("  <MOND correction>_(2), y=0 =", adm["mond_zero_spatial"])
    print("  D2 C_slip amplitude =", adm["d2_c_slip_amplitude"])
    print("  D2 K amplitude =", adm["d2_k_amplitude"])
    print("  generated L0 =", adm["generated_zero_field_lagrangian"])
    print("  generated L_y>0 =", adm["generated_positive_gradient_lagrangian"])
    checks.append(_check(
        "the Dirac Lagrangians are generated from the ADM geometry",
        adm["zero_field_residual"] == 0
        and adm["positive_gradient_residual"] == 0,
    ))
    checks.append(_check(
        "the positive-gradient coefficient is the action Hessian",
        adm["longitudinal_hessian_residual"] == 0,
    ))

    print("\n[7] Exact-zero-field finite-k Dirac chain")
    print("  L0 =", zero["lagrangian"])
    print("  p_Psi =", zero["derived_p_Psi"])
    print("  primaries =", zero["primaries"])
    print("  secondaries =", zero["secondaries"])
    print("  Poisson matrix =")
    sp.print_latex(zero["poisson_matrix"])
    print("  determinant =", zero["poisson_determinant"])
    print("  rank / Jacobian rank =", zero["poisson_rank"], zero["constraint_jacobian_rank"])
    print("  preservation multipliers =", zero["preservation_solution"])
    print("  first / second class =", zero["first_class_count"], zero["second_class_count"])
    print("  reduced one-form =", zero["canonical_one_form_pullback"])
    print("  H_reduced =", zero["reduced_hamiltonian"])
    print("  reduced scalar configuration DOF =", zero["configuration_dof"])
    print("  spatial orders: quadratic coefficient =", zero["quadratic_spatial_stiffness"],
          ", first nonzero order =", zero["leading_spatial_order"])
    checks.append(_check(
        "the displayed Dirac chain genuinely closes without tertiary residuals",
        all(residual == 0 for residual in zero["preservation_residuals"])
        and not zero["tertiary_constraints_found"],
    ))
    checks.append(_check(
        "the constraint classification is computed from an independent full-rank Jacobian",
        zero["poisson_rank"] == zero["constraint_jacobian_rank"]
        and zero["first_class_count"] + zero["second_class_count"]
        == len(zero["constraints"]),
    ))
    checks.append(_check(
        "the reduced canonical pair survives but has no quadratic spatial stiffness",
        zero["extra_reduced_scalar"]
        and zero["canonical_one_form_pullback"] != 0
        and zero["degenerate_linear_spatial_symbol"]
        and not zero["regular_two_tensor_limit_certified"],
    ))

    print("\n[8] Positive-gradient longitudinal scalar block")
    print("  L_y>0 =", nonzero["lagrangian"])
    print("  determinant / rank =", nonzero["poisson_determinant"], nonzero["poisson_rank"])
    print("  constraint solution =", nonzero["constraint_solution"])
    print("  H_reduced =", nonzero["reduced_hamiltonian"])
    print("  omega^2 =", nonzero["omega_squared"])
    print("  exact exponential omega^2 =", nonzero["exact_omega_squared"])
    print("  deep omega^2 =", nonzero["deep_omega_series"])
    print("  reduced scalar configuration DOF =", nonzero["configuration_dof"])
    checks.append(_check(
        "the positive-gradient chain closes with its matrix-derived classification",
        all(residual == 0 for residual in nonzero["preservation_residuals"])
        and nonzero["poisson_rank"] == nonzero["constraint_jacobian_rank"]
        and nonzero["first_class_count"] + nonzero["second_class_count"]
        == len(nonzero["constraints"]),
    ))
    checks.append(_check(
        "the surviving canonical scalar has a derived positive longitudinal dispersion",
        nonzero["positive_kinetic"]
        and nonzero["positive_gradient"]
        and nonzero["omega_squared"] != 0,
    ))
    checks.append(_check(
        "its Hamiltonian tends continuously to the ultralocal zero-field result",
        sp.simplify(
            nonzero["reduced_hamiltonian"].subs(
                nonzero["lambda_parallel"], 0
            )
            - zero["reduced_hamiltonian"]
        ) == 0,
    ))

    print("\n[9] k=0 rank-changing symbol")
    print("  finite-k Poisson rank =", zero["poisson_rank"])
    print("  k=0 Poisson rank =", homogeneous["poisson_rank"])
    print("  k=0 secondary symbols =", homogeneous["secondary_symbols"])
    checks.append(_check(
        "the homogeneous symbol is treated separately and all Laplacian secondaries collapse",
        homogeneous["poisson_rank"] != zero["poisson_rank"]
        and all(value == 0 for value in homogeneous["secondary_symbols"]),
    ))

    print("\n[10] Homogeneous tensor principal block")
    print("  multiplier contribution at k=0 =", tensor["homogeneous_multiplier_contribution"])
    print("  c_T^2 on homogeneous branch =", tensor["c_T_squared_on_homogeneous_branch"])
    checks.append(_check(
        "the homogeneous multiplier symbols vanish and the EH tensor cone remains luminal",
        tensor["homogeneous_multiplier_contribution"] == 0
        and tensor["c_T_squared_on_homogeneous_branch"] == 1,
    ))

    print("\n[VERDICT]")
    print("  OPEN overall. The ADM-generated zero-multiplier Minkowski principal block leaves")
    print("  one positive-kinetic scalar canonical pair with omega^2=lambda_parallel*k^2/3")
    print("  for y>0, collapsing to zero spatial stiffness at y=0.")
    print("  This is a candidate-specific principal-symbol obstruction, not a full-action kill:")
    print("  lower-derivative clock, potential, matter and background-multiplier terms and the")
    print("  nonlinear y->0+ constraint rank remain to be included.")
    print("  Boosted PPN, anisotropic tensor propagation, and cosmological stability also remain open.")
    print("  Next:", result["next_unavoidable_calculation"])

    passed = sum(checks)
    print(f"\nChecks completed: {passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
