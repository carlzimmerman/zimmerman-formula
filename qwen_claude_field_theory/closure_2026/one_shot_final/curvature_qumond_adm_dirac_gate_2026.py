#!/usr/bin/env python3
"""ADM/Dirac falsification of the curvature-sourced QUMOND candidate.

The covariant candidate is

    S = (16 pi G)^-1 int sqrt(-g) [R - 2 Lambda
        - 2 lambda (Delta_h chi - R_mn n^m n^n)
        + 2 a0^2 Q(Y)] + S_m[g,psi],

where ``n_mu=-grad_mu T/sqrt(-grad T squared)``,
``h_mn=g_mn+n_m n_n``, ``Y=h^mn grad_m chi grad_n chi/a0^2``, and

    Q(Y)=1-(1+sqrt(Y))*exp(-sqrt(Y)).

The companion ``curvature_qumond_action_gate_2026.py`` derives the exact
static exponential MOND equation in the scalar-isotropic reduction.  Its
partial auxiliary trace-free diagnostic is not a complete second-order
no-slip equation.  This file attacks independent questions: the velocity Hessian, the principal
auxiliary constraint bracket, an exact finite-momentum scalar Dirac chain,
the homogeneous mode, the tensor cone, and the rank-changing zero-field
point.

Conventions
-----------
In unitary clock gauge and with
``K_ij=(dot(gamma)_ij-L_shift gamma_ij)/(2N)``, Raychaudhuri gives

    R_nn = -L_n K - K_ij K^ij + N^-1 D^2 N.

After integrating the ``L_n K`` term by parts, the complete velocity density
(irrelevant positive constants suppressed) is

    L_kin = (1-2 lambda)(K_ij K^ij-K^2) + 2 K L_n lambda.

Every Hessian, determinant, inverse, Poisson bracket, rank, and count printed
below is constructed from these expressions.  The script does not hard-code a
desired rank or degree count.  The load-bearing result is a complete scalar
Dirac chain derived from the quadratic action on the luminal Minkowski branch.
The separate frozen-background ``(p_chi,C_chi)`` calculation is explicitly
only the principal diagonal bracket entry, not a claimed nonlinear closure.

Scope
-----
The exact MOND/tensor-luminality companion kills this explicit scalar
curvature-QUMOND action.  The scalar result here is for the displayed flat
luminal branch; its clock classification is performed in the separate
Stueckelberg gate.  Nothing here is a universal no-go for other local,
tensorial, or genuinely nonlocal architectures.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _poisson_bracket(
    left: sp.Expr,
    right: sp.Expr,
    pairs: tuple[tuple[sp.Symbol, sp.Symbol], ...],
) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.diff(left, q) * sp.diff(right, p)
            - sp.diff(left, p) * sp.diff(right, q)
            for q, p in pairs
        )
    )


def _kinetic_gate() -> dict[str, Any]:
    """Derive the complete gamma_ij/lambda velocity Hessian."""

    A = sp.symbols("A", positive=True, real=True)
    k11, k22, k33, k12, k13, k23, lambda_n = sp.symbols(
        "K_11 K_22 K_33 K_12 K_13 K_23 lambda_n", real=True
    )
    velocities = sp.Matrix((k11, k22, k33, k12, k13, k23, lambda_n))
    trace_k = k11 + k22 + k33
    kij_squared = k11**2 + k22**2 + k33**2 + 2 * (k12**2 + k13**2 + k23**2)
    lagrangian = sp.expand(A * (kij_squared - trace_k**2) + 2 * trace_k * lambda_n)
    hessian = sp.hessian(lagrangian, velocities)
    determinant = sp.factor(hessian.det())
    rank = hessian.rank()
    nullity = len(hessian.nullspace())

    momenta = sp.Matrix(sp.symbols("p_11 p_22 p_33 p_12 p_13 p_23 p_lambda"))
    inverse_velocities = sp.simplify(hessian.inv() * momenta)
    inverse_residuals = tuple(sp.simplify(item) for item in hessian * inverse_velocities - momenta)

    # The determinant never crosses zero for A>0, so the signature can be
    # obtained at the exact rational benchmark A=1 and is constant throughout
    # that connected healthy-tensor region.
    benchmark = hessian.subs(A, 1)
    eigenvalues_at_one = benchmark.eigenvals()
    negative = sum(multiplicity for value, multiplicity in eigenvalues_at_one.items() if value.is_negative)
    positive = sum(multiplicity for value, multiplicity in eigenvalues_at_one.items() if value.is_positive)

    return {
        "A": A,
        "velocity_vector": velocities,
        "lagrangian": lagrangian,
        "hessian": hessian,
        "determinant": determinant,
        "rank": rank,
        "nullity": nullity,
        "momenta": momenta,
        "inverse_velocities": inverse_velocities,
        "momentum_inverse_residuals": inverse_residuals,
        "eigenvalues_at_A_one": eigenvalues_at_one,
        "negative_eigenvalues_for_A_positive": negative,
        "positive_eigenvalues_for_A_positive": positive,
    }


def _nonzero_momentum_auxiliary_block() -> dict[str, Any]:
    """Generate the principal ``p_chi``/``C_chi`` bracket at ``k!=0``.

    The full secondary also contains ``D^2 lambda`` and metric perturbations.
    Those terms have zero derivative with respect to ``chi`` and hence do not
    change the displayed diagonal PB entry, but they do enter stabilization.
    Consequently this function diagnoses the principal rank only; the exact
    closed chain is calculated in ``_minkowski_scalar_dirac_gate``.
    """

    y = sp.symbols("y", positive=True, real=True)
    k_parallel = sp.symbols("k_parallel", positive=True, real=True)
    k_perp = sp.symbols("k_perp", nonnegative=True, real=True)
    chi, p_chi = sp.symbols("chi p_chi", real=True)
    effective_mu = 1 - sp.exp(-y)
    effective_lambda_parallel = sp.simplify(
        effective_mu + y * sp.diff(effective_mu, y)
    )
    # The primary-secondary bracket is controlled by the RAW chi equation.
    # Since 2 Q_Y=1-mu=exp(-y), its flux is exp(-y) grad(chi), whose
    # transverse and longitudinal derivatives differ from the final MOND
    # operator obtained only after eliminating lambda and the metric.
    raw_chi_transverse = sp.exp(-y)
    raw_chi_parallel = (1 - y) * sp.exp(-y)
    constitutive_symbol = sp.simplify(
        raw_chi_parallel * k_parallel**2
        + raw_chi_transverse * k_perp**2
    )
    effective_mond_symbol = sp.simplify(
        effective_lambda_parallel * k_parallel**2
        + effective_mu * k_perp**2
    )

    primary = p_chi
    omitted_source = sp.symbols("C_source_independent_of_chi", real=True)
    secondary = constitutive_symbol * chi + omitted_source
    constraints = (primary, secondary)
    pairs = ((chi, p_chi),)
    pb_matrix = sp.Matrix(
        [
            [_poisson_bracket(left, right, pairs) for right in constraints]
            for left in constraints
        ]
    )
    # Exact real rank-loss loci of the principal coefficient.  The y=1
    # longitudinal ray and the y>1 cone are calculated from M_chi=0 rather
    # than inferred from a numerical sample.
    rank_loss_kperp_squared = sp.solve(
        sp.Eq(sp.exp(y) * constitutive_symbol, 0),
        k_perp**2,
    )[0]
    y_one_pure_longitudinal_residual = sp.simplify(
        constitutive_symbol.subs({y: 1, k_perp: 0})
    )
    supercritical_cone_residual = sp.simplify(
        constitutive_symbol.subs(k_perp**2, (y - 1) * k_parallel**2)
    )

    return {
        "y": y,
        "k_parallel": k_parallel,
        "k_perp": k_perp,
        "raw_chi_transverse": raw_chi_transverse,
        "raw_chi_parallel": raw_chi_parallel,
        "effective_mu": effective_mu,
        "effective_lambda_parallel": effective_lambda_parallel,
        "constitutive_symbol": constitutive_symbol,
        "effective_mond_symbol": effective_mond_symbol,
        "primary": primary,
        "secondary": secondary,
        "omitted_source": omitted_source,
        "constraints": constraints,
        "pb_matrix": pb_matrix,
        "pb_determinant": sp.factor(pb_matrix.det()),
        "pb_rank": pb_matrix.rank(),
        "rank_loss_kperp_squared": rank_loss_kperp_squared,
        "y_one_pure_longitudinal_residual": y_one_pure_longitudinal_residual,
        "supercritical_cone_residual": supercritical_cone_residual,
        "stabilization_scope": (
            "not computed here: D^2 lambda and metric pieces of C_chi are "
            "retained in the exact Minkowski chain"
        ),
    }


def _minkowski_scalar_dirac_gate() -> dict[str, Any]:
    """Close the full finite-k scalar chain on the luminal Minkowski branch.

    Use unitary clock gauge ``T=t`` and the scalar spatial gauge
    ``gamma_ij=exp(2 zeta) delta_ij``.  With ``N=1+alpha`` and
    ``N_i=partial_i beta``, retain the multiplier perturbation ``ell`` and the
    elliptic scalar ``chi``.  At background ``lambda=0`` and ``y=0``, the
    complete quadratic scalar density of the displayed action is derived
    term by term below.  Its result is

      -6 zdot^2 + 6 zdot elldot - 4 k^2 beta zdot + 2 k^2 beta elldot
      +2 k^2 zeta^2 +4 k^2 alpha zeta -2 k^2 alpha ell
      +2 k^2 ell chi + k^2 chi^2.

    The last term follows from ``2 a0^2 Q(Y)=|grad chi|^2+O(chi^3)``.
    Lapse, shift, and chi are retained through the Dirac algorithm rather than
    substituted before their primary constraints are identified.
    """

    k, a0 = sp.symbols("k a0", positive=True, real=True)
    zeta, ell, chi, alpha, beta = sp.symbols(
        "zeta ell chi alpha beta", real=True
    )
    zeta_dot, ell_dot, chi_dot, alpha_dot, beta_dot = sp.symbols(
        "zeta_dot ell_dot chi_dot alpha_dot beta_dot", real=True
    )
    all_velocities = sp.Matrix(
        (zeta_dot, ell_dot, chi_dot, alpha_dot, beta_dot)
    )
    # Choose the Fourier wave-vector along x.  The result is rotationally
    # invariant and depends only on k^2.  K_ij is constructed from its ADM
    # definition rather than entering the reduced kinetic coefficients by
    # hand.
    identity_three = sp.eye(3)
    beta_hessian = sp.diag(-k**2 * beta, 0, 0)
    extrinsic_curvature = zeta_dot * identity_three - beta_hessian
    trace_k = sp.trace(extrinsic_curvature)
    eh_kinetic = sp.expand(
        sp.trace(extrinsic_curvature * extrinsic_curvature) - trace_k**2
    )
    lambda_kinetic = sp.expand(2 * trace_k * ell_dot)

    # For gamma_ij=exp(2 zeta)delta_ij,
    # sqrt(gamma) R^(3)=exp(zeta)[-4 Delta zeta-2(grad zeta)^2].
    # A bookkeeping epsilon extracts its integrated quadratic coefficient,
    # including the lapse perturbation N=1+alpha.
    epsilon = sp.symbols("epsilon", real=True)
    conformal_curvature_density = sp.expand(
        (1 + epsilon * alpha)
        * sp.exp(epsilon * zeta)
        * (4 * epsilon * k**2 * zeta - 2 * epsilon**2 * k**2 * zeta**2)
    )
    eh_spatial = sp.expand(
        sp.diff(conformal_curvature_density, epsilon, 2).subs(epsilon, 0) / 2
    )

    # The integrated spatial pieces of the multiplier action are
    # -2 D ell.D alpha +2 D ell.D chi at quadratic order.
    lambda_lapse = -2 * k**2 * alpha * ell
    lambda_elliptic = 2 * k**2 * ell * chi

    # Derive the quadratic term of 2 a0^2 Q(Y), with
    # sqrt(Y)=epsilon*k*chi/a0 on a fixed-sign ray.  Q''(0)/2=1/2;
    # the nonanalytic cubic and higher terms are irrelevant here.
    q_argument = sp.symbols("q_argument", real=True)
    q_function = 1 - (1 + q_argument) * sp.exp(-q_argument)
    q_quadratic_coefficient = sp.simplify(
        sp.diff(q_function, q_argument, 2).subs(q_argument, 0) / 2
    )
    q_spatial = sp.simplify(
        2 * a0**2
        * q_quadratic_coefficient
        * (k * chi / a0) ** 2
    )

    action_terms = {
        "EH_kinetic": eh_kinetic,
        "lambda_kinetic": lambda_kinetic,
        "EH_spatial": eh_spatial,
        "lambda_lapse": lambda_lapse,
        "lambda_elliptic": lambda_elliptic,
        "Q_spatial": q_spatial,
    }
    lagrangian = sp.expand(sum(action_terms.values()))
    velocity_hessian = sp.hessian(lagrangian, all_velocities)
    velocity_rank = velocity_hessian.rank()
    velocity_nullity = len(velocity_hessian.nullspace())

    p_zeta, p_ell, p_chi, p_alpha, p_beta = sp.symbols(
        "p_zeta p_ell p_chi p_alpha p_beta", real=True
    )
    momenta = (
        sp.diff(lagrangian, zeta_dot),
        sp.diff(lagrangian, ell_dot),
        sp.diff(lagrangian, chi_dot),
        sp.diff(lagrangian, alpha_dot),
        sp.diff(lagrangian, beta_dot),
    )
    regular_solution = sp.solve(
        (sp.Eq(p_zeta, momenta[0]), sp.Eq(p_ell, momenta[1])),
        (zeta_dot, ell_dot),
        dict=True,
    )[0]
    hamiltonian = sp.factor(
        (p_zeta * zeta_dot + p_ell * ell_dot - lagrangian).subs(
            regular_solution
        )
    )

    pairs = (
        (zeta, p_zeta),
        (ell, p_ell),
        (chi, p_chi),
        (alpha, p_alpha),
        (beta, p_beta),
    )
    primaries = (p_chi, p_alpha, p_beta)
    secondaries = tuple(
        sp.factor(_poisson_bracket(primary, hamiltonian, pairs))
        for primary in primaries
    )
    constraints = primaries + secondaries
    constraint_pb = sp.Matrix(
        [
            [_poisson_bracket(left, right, pairs) for right in constraints]
            for left in constraints
        ]
    )
    constraint_pb_rank = constraint_pb.rank()
    first_class_count = len(constraints) - constraint_pb_rank
    second_class_count = constraint_pb_rank

    u_chi, u_alpha, u_beta = sp.symbols(
        "u_chi u_alpha u_beta", real=True
    )
    total_hamiltonian = hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(
            (u_chi, u_alpha, u_beta), primaries
        )
    )
    secondary_preservation = tuple(
        sp.factor(_poisson_bracket(secondary, total_hamiltonian, pairs))
        for secondary in secondaries
    )

    phase_dimension = 2 * len(pairs)
    physical_scalar_phase_dimension = sp.simplify(
        phase_dimension - 2 * first_class_count - second_class_count
    )
    physical_scalar_dof = sp.simplify(physical_scalar_phase_dimension / 2)

    reduced_lagrangian = sp.factor(
        lagrangian.subs(
            {
                ell: 2 * zeta,
                ell_dot: 2 * zeta_dot,
                chi: -2 * zeta,
            },
            simultaneous=True,
        )
    )
    kinetic_coefficient = sp.simplify(
        sp.diff(reduced_lagrangian, zeta_dot, 2) / 2
    )
    gradient_coefficient = sp.simplify(
        -sp.diff(reduced_lagrangian, zeta, 2) / (2 * k**2)
    )
    sound_speed_squared = sp.simplify(
        gradient_coefficient / kinetic_coefficient
    )

    # Restore the scalar spatial shear E to verify that the pole is not an
    # artifact of imposing the scalar spatial gauge before the Dirac count.
    # The extrinsic-curvature sector depends on E and beta through E_dot-beta.
    E, E_dot, p_E = sp.symbols("E E_dot p_E", real=True)
    restored_lagrangian = sp.expand(
        lagrangian
        + 4 * k**2 * zeta_dot * E_dot
        - 2 * k**2 * E_dot * ell_dot
    )
    restored_velocities = sp.Matrix(
        (zeta_dot, ell_dot, E_dot, chi_dot, alpha_dot, beta_dot)
    )
    restored_momenta = (
        sp.diff(restored_lagrangian, zeta_dot),
        sp.diff(restored_lagrangian, ell_dot),
        sp.diff(restored_lagrangian, E_dot),
        sp.diff(restored_lagrangian, chi_dot),
        sp.diff(restored_lagrangian, alpha_dot),
        sp.diff(restored_lagrangian, beta_dot),
    )
    restored_regular_solution = sp.solve(
        (
            sp.Eq(p_zeta, restored_momenta[0]),
            sp.Eq(p_ell, restored_momenta[1]),
            sp.Eq(p_E, restored_momenta[2]),
        ),
        (zeta_dot, ell_dot, E_dot),
        dict=True,
    )[0]
    restored_hamiltonian = sp.factor(
        (
            p_zeta * zeta_dot
            + p_ell * ell_dot
            + p_E * E_dot
            - restored_lagrangian
        ).subs(restored_regular_solution)
    )
    restored_pairs = (
        (zeta, p_zeta),
        (ell, p_ell),
        (E, p_E),
        (chi, p_chi),
        (alpha, p_alpha),
        (beta, p_beta),
    )
    restored_primaries = (p_chi, p_alpha, p_beta)
    restored_secondaries = tuple(
        sp.factor(
            _poisson_bracket(primary, restored_hamiltonian, restored_pairs)
        )
        for primary in restored_primaries
    )
    restored_constraints = restored_primaries + restored_secondaries
    restored_constraint_pb = sp.Matrix(
        [
            [
                _poisson_bracket(left, right, restored_pairs)
                for right in restored_constraints
            ]
            for left in restored_constraints
        ]
    )
    restored_pb_rank = restored_constraint_pb.rank()
    restored_first_class = len(restored_constraints) - restored_pb_rank
    restored_second_class = restored_pb_rank
    restored_phase_dimension = 2 * len(restored_pairs)
    restored_physical_dof = sp.Rational(
        restored_phase_dimension
        - 2 * restored_first_class
        - restored_second_class,
        2,
    )
    restored_total_hamiltonian = restored_hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(
            (u_chi, u_alpha, u_beta), restored_primaries
        )
    )
    restored_preservation = tuple(
        sp.factor(
            _poisson_bracket(
                secondary, restored_total_hamiltonian, restored_pairs
            )
        )
        for secondary in restored_secondaries
    )
    restored_reduced_lagrangian = sp.factor(
        restored_lagrangian.subs(
            {
                ell: 2 * zeta,
                ell_dot: 2 * zeta_dot,
                chi: -2 * zeta,
            },
            simultaneous=True,
        )
    )
    spatial_gauge_restored = {
        "E": E,
        "E_dot": E_dot,
        "lagrangian": restored_lagrangian,
        "velocities": restored_velocities,
        "velocity_hessian": sp.hessian(
            restored_lagrangian, restored_velocities
        ),
        "momenta": restored_momenta,
        "regular_velocity_solution": restored_regular_solution,
        "hamiltonian": restored_hamiltonian,
        "primaries": restored_primaries,
        "secondaries": restored_secondaries,
        "constraints": restored_constraints,
        "constraint_pb_matrix": restored_constraint_pb,
        "constraint_pb_rank": restored_pb_rank,
        "first_class_count": restored_first_class,
        "second_class_count": restored_second_class,
        "secondary_preservation": restored_preservation,
        "physical_scalar_dof": restored_physical_dof,
        "reduced_lagrangian": restored_reduced_lagrangian,
    }

    return {
        "k": k,
        "zeta": zeta,
        "zeta_dot": zeta_dot,
        "lagrangian": lagrangian,
        "action_terms": action_terms,
        "extrinsic_curvature": extrinsic_curvature,
        "trace_extrinsic_curvature": trace_k,
        "conformal_curvature_density_with_epsilon": conformal_curvature_density,
        "q_quadratic_coefficient": q_quadratic_coefficient,
        "all_velocities": all_velocities,
        "velocity_hessian": velocity_hessian,
        "velocity_rank": velocity_rank,
        "velocity_nullity": velocity_nullity,
        "momenta": momenta,
        "regular_velocity_solution": regular_solution,
        "hamiltonian": hamiltonian,
        "primaries": primaries,
        "primary_count": len(primaries),
        "secondaries": secondaries,
        "secondary_count": len(secondaries),
        "constraints": constraints,
        "constraint_pb_matrix": constraint_pb,
        "constraint_pb_rank": constraint_pb_rank,
        "constraint_pb_nullity": len(constraint_pb.nullspace()),
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "secondary_preservation": secondary_preservation,
        "physical_scalar_phase_dimension": physical_scalar_phase_dimension,
        "physical_scalar_dof": physical_scalar_dof,
        "reduced_lagrangian": reduced_lagrangian,
        "kinetic_coefficient": kinetic_coefficient,
        "gradient_coefficient": gradient_coefficient,
        "sound_speed_squared": sound_speed_squared,
        "spatial_gauge_restored": spatial_gauge_restored,
        "background_assumptions": (
            "Minkowski, Lambda=0, background lambda=0, constant chi, k!=0"
        ),
    }


def _homogeneous_and_zero_field(auxiliary: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Treat k=0 FLRW and y=0 rank loss independently."""

    a = sp.symbols("a", positive=True, real=True)
    a_ddot = sp.symbols("a_ddot", real=True)
    H = sp.symbols("H", positive=True, real=True)
    # On FLRW, Delta_h chi=0 and R_nn=-3 a_ddot/a.  Delta_h chi-R_nn=0
    # therefore enforces 3 a_ddot/a=0.
    lambda_constraint = sp.simplify(3 * a_ddot / a)
    de_sitter_residual = sp.simplify(lambda_constraint.subs(a_ddot, a * H**2))
    coasting_solution = sp.solve(sp.Eq(lambda_constraint, 0), a_ddot)
    t = sp.symbols("t", nonnegative=True, real=True)
    coasting_slope, coasting_intercept = sp.symbols(
        "coasting_slope coasting_intercept", positive=True, real=True
    )
    coasting_scale_factor = coasting_slope * t + coasting_intercept
    coasting_acceleration = sp.diff(coasting_scale_factor, t, 2)
    coasting_hubble = sp.simplify(
        sp.diff(coasting_scale_factor, t) / coasting_scale_factor
    )
    coasting_constraint_residual = sp.simplify(
        lambda_constraint.subs(
            {a: coasting_scale_factor, a_ddot: coasting_acceleration}
        )
    )

    zero_substitutions = {auxiliary["y"]: 0}
    zero_pb = sp.simplify(auxiliary["pb_matrix"].subs(zero_substitutions))
    zero_rank = zero_pb.rank()
    zero_effective_mond_symbol = sp.simplify(
        auxiliary["effective_mond_symbol"].subs(zero_substitutions)
    )
    generic_effective_mond_symbol_matrix = sp.Matrix(
        [[auxiliary["effective_mond_symbol"]]]
    )
    zero_effective_mond_symbol_matrix = sp.simplify(
        generic_effective_mond_symbol_matrix.subs(zero_substitutions)
    )
    generic_effective_mond_rank = generic_effective_mond_symbol_matrix.rank()
    zero_effective_mond_rank = zero_effective_mond_symbol_matrix.rank()

    homogeneous = {
        "a": a,
        "a_ddot": a_ddot,
        "H": H,
        "R_nn": sp.simplify(-3 * a_ddot / a),
        "Delta_h_chi": sp.Integer(0),
        "lambda_constraint": lambda_constraint,
        "de_sitter_residual": de_sitter_residual,
        "coasting_solution": coasting_solution,
        "coasting_condition": coasting_solution[0],
        "coasting_scale_factor": coasting_scale_factor,
        "coasting_H": coasting_hubble,
        "coasting_constraint_residual": coasting_constraint_residual,
        "scope": (
            "lambda equation only: coasting H!=0 survives, but the remaining "
            "background equations and perturbative viability are not solved"
        ),
    }
    zero_field = {
        "raw_auxiliary_pb_matrix": zero_pb,
        "raw_auxiliary_pb_rank": zero_rank,
        "generic_raw_auxiliary_pb_rank": auxiliary["pb_rank"],
        "effective_mond_symbol": zero_effective_mond_symbol,
        "generic_effective_mond_symbol_matrix": generic_effective_mond_symbol_matrix,
        "zero_effective_mond_symbol_matrix": zero_effective_mond_symbol_matrix,
        "generic_effective_mond_rank": generic_effective_mond_rank,
        "zero_effective_mond_rank": zero_effective_mond_rank,
        "effective_mond_rank_loss": sp.simplify(
            generic_effective_mond_rank - zero_effective_mond_rank
        ),
    }
    return homogeneous, zero_field


def _tensor_gate() -> dict[str, Any]:
    lambda_background = sp.symbols("lambda_background", real=True)
    kinetic_coefficient = 1 - 2 * lambda_background
    gradient_coefficient = sp.Integer(1)
    c_t_squared = sp.simplify(gradient_coefficient / kinetic_coefficient)
    return {
        "lambda_background": lambda_background,
        "kinetic_coefficient": kinetic_coefficient,
        "gradient_coefficient": gradient_coefficient,
        "c_T_squared": c_t_squared,
        "c_T_minus_one": sp.simplify(c_t_squared - 1),
        "positive_tensor_condition": sp.Gt(kinetic_coefficient, 0),
    }


def _vector_gate() -> dict[str, Any]:
    """Close one transverse vector polarization about the same background.

    For a wave along x, write the transverse spatial metric perturbation as
    ``gamma_xy=partial_x F`` and the transverse shift as ``N_y=S``.  The
    action depends only on the gauge-invariant combination ``F_dot-S``.
    The second transverse polarization is identical.
    """

    A, k = sp.symbols("A k", positive=True, real=True)
    F, S, F_dot, S_dot = sp.symbols("F S F_dot S_dot", real=True)
    p_F, p_S = sp.symbols("p_F p_S", real=True)
    lagrangian = sp.expand(A * k**2 * (F_dot - S) ** 2 / 2)
    velocities = sp.Matrix((F_dot, S_dot))
    velocity_hessian = sp.hessian(lagrangian, velocities)
    momenta = (sp.diff(lagrangian, F_dot), sp.diff(lagrangian, S_dot))
    regular_velocity = sp.solve(sp.Eq(p_F, momenta[0]), F_dot)[0]
    hamiltonian = sp.factor(
        (p_F * F_dot - lagrangian).subs(F_dot, regular_velocity)
    )
    pairs = ((F, p_F), (S, p_S))
    primary = p_S
    secondary = sp.factor(_poisson_bracket(primary, hamiltonian, pairs))
    u_S = sp.symbols("u_S", real=True)
    total_hamiltonian = hamiltonian + u_S * primary
    secondary_preservation = sp.factor(
        _poisson_bracket(secondary, total_hamiltonian, pairs)
    )
    constraints = (primary, secondary)
    constraint_pb = sp.Matrix(
        [
            [_poisson_bracket(left, right, pairs) for right in constraints]
            for left in constraints
        ]
    )
    first_class_count = len(constraints) - constraint_pb.rank()
    physical_phase_dimension = sp.simplify(
        2 * len(pairs) - 2 * first_class_count - constraint_pb.rank()
    )
    return {
        "A": A,
        "k": k,
        "lagrangian": lagrangian,
        "velocities": velocities,
        "velocity_hessian": velocity_hessian,
        "velocity_rank": velocity_hessian.rank(),
        "momenta": momenta,
        "hamiltonian": hamiltonian,
        "constraints": constraints,
        "secondary_preservation": secondary_preservation,
        "constraint_pb_matrix": constraint_pb,
        "constraint_pb_rank": constraint_pb.rank(),
        "first_class_count_per_polarization": first_class_count,
        "physical_dof_per_polarization": sp.simplify(
            physical_phase_dimension / 2
        ),
        "polarizations": sp.Integer(2),
    }


def _static_gate() -> dict[str, Any]:
    y = sp.symbols("y", positive=True, real=True)
    g, g_N, a0 = sp.symbols("g g_N a0", positive=True, real=True)
    G, M_b, radius, v4 = sp.symbols(
        "G M_b r v_fourth", positive=True, real=True
    )
    mu = 1 - sp.exp(-y)
    Q = 1 - (1 + y) * sp.exp(-y)
    Q_Y = sp.simplify(sp.diff(Q, y) / (2 * y))
    preferred_primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu_of_g = mu.subs(y, g / a0)
    spherical_deep_flux_ratio = sp.limit(
        mu_of_g * g / (g**2 / a0), g, 0, dir="+"
    )
    btfr_solution = sp.solve(
        sp.Eq(v4 / (a0 * radius**2), G * M_b / radius**2),
        v4,
    )[0]
    return {
        "y": y,
        "g": g,
        "g_N": g_N,
        "a0": a0,
        "G": G,
        "M_b": M_b,
        "radius": radius,
        "Q": Q,
        "Q_Y": Q_Y,
        "mu": mu,
        "mu_residual": sp.simplify(2 * Q_Y - (1 - mu)),
        "preferred_primitive": preferred_primitive,
        "preferred_primitive_residual": sp.simplify(
            sp.diff(preferred_primitive, y) / (2 * y) - mu
        ),
        "spherical_relation": sp.Eq(mu_of_g * g, g_N),
        "spherical_deep_flux_ratio": spherical_deep_flux_ratio,
        "btfr_solution": btfr_solution,
        "newtonian_limit": sp.limit(mu, y, sp.oo),
        "deep_mond_limit": sp.limit(mu / y, y, 0, dir="+"),
        "measured_G_over_bare_G_high_acceleration": sp.limit(1 / mu, y, sp.oo),
    }


def derive_adm_dirac_gate() -> dict[str, Any]:
    kinetic = _kinetic_gate()
    auxiliary = _nonzero_momentum_auxiliary_block()
    homogeneous, zero_field = _homogeneous_and_zero_field(auxiliary)
    minkowski_scalar = _minkowski_scalar_dirac_gate()
    return {
        "action": (
            "(16 pi G)^-1 int sqrt(-g)[R-2 Lambda-2 lambda(Delta_h chi-R_nn)"
            "+2 a0^2 Q(Y)] + S_m[g,psi]"
        ),
        "adm_identity": "R_nn=-L_n K-K_ij K^ij+N^-1 D^2 N",
        "kinetic": kinetic,
        "k_nonzero": auxiliary,
        "minkowski_scalar": minkowski_scalar,
        "k_zero_flrw": homogeneous,
        "y_zero": zero_field,
        "tensor": _tensor_gate(),
        "vector": _vector_gate(),
        "static": _static_gate(),
        "matter_ward_scope": {
            "computed_by_this_gate": False,
            "status": (
                "analytic Noether-Ward consequence of the separately "
                "diffeomorphism-invariant minimally coupled S_m; this ADM "
                "script does not computationally certify the covariant identity"
            ),
        },
        "a0_relation": "external input; not derived",
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'CHECK' if passed else 'ERROR'}] {label}")
    return passed


def main() -> int:
    result = derive_adm_dirac_gate()
    kinetic = result["kinetic"]
    sector = result["k_nonzero"]
    scalar = result["minkowski_scalar"]
    flrw = result["k_zero_flrw"]
    zero = result["y_zero"]
    tensor = result["tensor"]
    vector = result["vector"]
    static = result["static"]

    print("=" * 96)
    print("CURVATURE-QUMOND FULL ADM/DIRAC GATE")
    print("=" * 96)
    print("Action:", result["action"])
    print("ADM identity:", result["adm_identity"])

    print("\n[1] Complete gamma_ij/lambda velocity Hessian")
    print("  L_kin =", kinetic["lagrangian"])
    print("  Hessian =")
    print(kinetic["hessian"])
    print("  det(H) =", kinetic["determinant"])
    print("  rank/nullity =", kinetic["rank"], "/", kinetic["nullity"])
    print("  exact inverse residuals =", kinetic["momentum_inverse_residuals"])
    print("  eigenvalues at A=1 =", kinetic["eigenvalues_at_A_one"])

    print("\n[2] Generic k!=0 principal auxiliary bracket (not a full nonlinear chain)")
    print("  primary =", sector["primary"])
    print("  secondary =", sector["secondary"])
    print("  raw chi transverse coefficient =", sector["raw_chi_transverse"])
    print("  raw chi longitudinal coefficient =", sector["raw_chi_parallel"])
    print("  raw chi constitutive symbol =", sector["constitutive_symbol"])
    print("  effective MOND mu =", sector["effective_mu"])
    print("  effective MOND lambda_parallel =", sector["effective_lambda_parallel"])
    print("  effective MOND symbol =", sector["effective_mond_symbol"])
    print("  PB matrix =")
    print(sector["pb_matrix"])
    print("  det/rank =", sector["pb_determinant"], "/", sector["pb_rank"])
    print("  rank-loss solution k_perp^2 =", sector["rank_loss_kperp_squared"])
    print("  y=1 pure-longitudinal residual =", sector["y_one_pure_longitudinal_residual"])
    print("  y>1 cone residual =", sector["supercritical_cone_residual"])
    print("  stabilization scope =", sector["stabilization_scope"])

    print("\n[3] Complete luminal-Minkowski scalar Dirac chain")
    print("  background assumptions =", scalar["background_assumptions"])
    print("  action-derived quadratic terms =", scalar["action_terms"])
    print("  quadratic scalar L =", scalar["lagrangian"])
    print("  velocity Hessian =")
    print(scalar["velocity_hessian"])
    print("  velocity rank/nullity =", scalar["velocity_rank"], "/", scalar["velocity_nullity"])
    print("  primaries =", scalar["primaries"])
    print("  secondaries =", scalar["secondaries"])
    print("  constraint PB matrix =")
    print(scalar["constraint_pb_matrix"])
    print("  PB rank/nullity =", scalar["constraint_pb_rank"], "/", scalar["constraint_pb_nullity"])
    print("  preservation of secondaries =", scalar["secondary_preservation"])
    print("  first/second class =", scalar["first_class_count"], "/", scalar["second_class_count"])
    print("  physical scalar DOF =", scalar["physical_scalar_dof"])
    print("  reduced scalar L =", scalar["reduced_lagrangian"])
    print("  scalar c_s^2 =", scalar["sound_speed_squared"])
    restored = scalar["spatial_gauge_restored"]
    print("  restored-shear secondaries =", restored["secondaries"])
    print("  restored-shear PB rank =", restored["constraint_pb_rank"])
    print("  restored-shear first/second class =", restored["first_class_count"], "/", restored["second_class_count"])
    print("  restored-shear physical scalar DOF =", restored["physical_scalar_dof"])
    print("  restored-shear reduced L =", restored["reduced_lagrangian"])

    print("\n[4] Separate k=0 FLRW and y=0 sectors")
    print("  R_nn(FLRW) =", flrw["R_nn"])
    print("  lambda equation Delta_h chi-R_nn =", flrw["lambda_constraint"])
    print("  de Sitter residual =", flrw["de_sitter_residual"])
    print("  allowed homogeneous acceleration a_ddot =", flrw["coasting_condition"])
    print("  explicit coasting H =", flrw["coasting_H"])
    print("  coasting lambda-equation residual =", flrw["coasting_constraint_residual"])
    print("  FLRW scope =", flrw["scope"])
    print("  raw auxiliary PB rank at generic y,k!=0 =", zero["generic_raw_auxiliary_pb_rank"])
    print("  raw auxiliary PB matrix at y=0 =", zero["raw_auxiliary_pb_matrix"], "; rank =", zero["raw_auxiliary_pb_rank"])
    print("  effective MOND symbol at y=0 =", zero["effective_mond_symbol"], "; rank loss =", zero["effective_mond_rank_loss"])

    print("\n[5] Tensor, vector, and static limits")
    print("  tensor kinetic coefficient =", tensor["kinetic_coefficient"])
    print("  c_T^2 =", tensor["c_T_squared"])
    print("  c_T^2-1 =", tensor["c_T_minus_one"])
    print("  vector L per polarization =", vector["lagrangian"])
    print("  vector constraints per polarization =", vector["constraints"])
    print("  vector PB matrix =", vector["constraint_pb_matrix"])
    print("  vector secondary preservation =", vector["secondary_preservation"])
    print("  propagating vector DOF per polarization =", vector["physical_dof_per_polarization"])
    print("  Q(Y) =", static["Q"], "; 2 Q_Y-(1-mu) =", static["mu_residual"])
    print("  preferred G(y) primitive residual =", static["preferred_primitive_residual"])
    print("  spherical law =", static["spherical_relation"])
    print("  deep spherical flux ratio =", static["spherical_deep_flux_ratio"])
    print("  derived v^4 =", static["btfr_solution"])
    print("  mu/y at y->0 =", static["deep_mond_limit"])
    print("  mu at y->infinity =", static["newtonian_limit"])
    print("  G_measured/G_bare at high acceleration =", static["measured_G_over_bare_G_high_acceleration"])

    checks = [
        _check("the lambda/metric velocity Hessian is generated and nondegenerate", kinetic["determinant"] != 0 and kinetic["nullity"] == 0),
        _check("the generic principal p_chi-C_chi bracket is nonzero away from its computed loci", sector["pb_rank"] == len(sector["constraints"])),
        _check("the complete luminal-Minkowski Dirac chain leaves one gauge-independent scalar pole", scalar["physical_scalar_dof"] == 1 and scalar["sound_speed_squared"] == sp.Rational(1, 3) and restored["physical_scalar_dof"] == 1 and restored["reduced_lagrangian"] == scalar["reduced_lagrangian"]),
        _check("the homogeneous lambda equation excludes de Sitter", flrw["de_sitter_residual"] != 0),
        _check("the exact y=0 point degenerates the eliminated MOND response, not the raw chi pair", zero["raw_auxiliary_pb_rank"] == sector["pb_rank"] and zero["effective_mond_rank_loss"] > 0),
        _check("luminal tensors require the special background lambda=0", sp.solve(sp.Eq(tensor["c_T_squared"], 1), tensor["lambda_background"]) == [0]),
        _check("the transverse vector constraints leave no vector pole", vector["physical_dof_per_polarization"] == 0),
        _check("the same action retains exact exponential MOND, spherical, and BTFR limits", static["mu_residual"] == 0 and static["preferred_primitive_residual"] == 0 and static["deep_mond_limit"] == 1 and static["newtonian_limit"] == 1 and static["spherical_deep_flux_ratio"] == 1 and static["btfr_solution"] == static["G"] * static["a0"] * static["M_b"]),
    ]

    print("\n[VERDICT]")
    print("  The scalar-isotropic reduction reproduces the requested exponential law.  The full")
    print("  nonlinear no-slip/PPN result is not asserted by this ADM script.  The curvature multiplier")
    print("  participates in a regular metric/lambda velocity block, and the complete finite-k scalar")
    print("  Dirac chain on the special luminal Minkowski branch leaves one propagating scalar with")
    print("  c_s^2=1/3; the separate Stueckelberg gate identifies its clock status.  No generic")
    print("  nonlinear DOF number is asserted: the separate principal chi bracket is not a full closure")
    print("  and changes rank on the displayed y>=1 loci.")
    print("  Independently, its k=0 lambda equation imposes R_nn=0, excluding de Sitter and ordinary")
    print("  accelerating Lambda-FLRW but not coasting H!=0; this is not a complete FLRW viability test.")
    print("  At y=0 the raw chi pair stays second class but the eliminated")
    print("  MOND response loses rank; no nonlinear zero-field evolution prescription is supplied.  The raw")
    print("  indefinite Hessian is recorded as an adverse stability signal, not promoted to a reduced")
    print("  physical-ghost theorem.  Candidate death rests independently on the exact MOND/tensor-")
    print("  luminality obstruction.  The a0-Lambda relation is input, never derived.")
    print(f"  Diagnostic checks: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
