#!/usr/bin/env python3
"""Metric-only elliptic-projector and zero-field gate.

This is the next gate left by the universal spin-2 zero-field audit. It asks
whether a regular covariant tensor made only from the metric can turn

    S_aux = integral sqrt(-g) lambda (H^mn[g] nabla_m nabla_n chi - J)

into a spatial elliptic constraint without a clock/aether and without hidden
auxiliary propagation.

On the exact Minkowski/zero-field branch, Poincare covariance forces the value
of H^mn to be B eta^mn (or zero), never a nonzero rank-three spatial projector.
The nonzero branch is hyperbolic and the varied multiplier action has a
full-rank, ghost-signed auxiliary velocity Hessian. A genuine spatial
projector has no auxiliary DOF for k!=0, but its homogeneous equation forbids
a nonzero homogeneous source.

An adversarial audit found an essential loophole in the first version of this
gate. A regular metric-derived projector can be rank three away from zero and
vanish smoothly at Minkowski, e.g. H^mn=(-V^2)g^mn+V^m V^n. The normalized
direction is path dependent but the vanishing amplitude removes the path
dependence. This refutes the broad regular-projector no-go. The executable
gate now derives the counterexample and the resulting loss of Dirac rank and
linear source response. The rank-changing branch is OPEN and requires a full
strong-coupling/nonlinear analysis.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _poisson(
    f: sp.Expr,
    g: sp.Expr,
    qs: list[sp.Symbol],
    ps: list[sp.Symbol],
) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.diff(f, q) * sp.diff(g, p) - sp.diff(f, p) * sp.diff(g, q)
            for q, p in zip(qs, ps)
        )
    )


def derive_projector_gate() -> dict[str, Any]:
    """Return exact symbolic derivations for every branch of the gate."""

    eta4 = sp.diag(-1, 1, 1, 1)

    # 1. Natural rank-two tensor at a Minkowski background.
    # Rotational covariance reduces a symmetric contravariant tensor to this
    # ansatz. A pi rotation kills C; one nontrivial boost imposes A=-B.
    A = sp.Symbol("A", real=True)
    B = sp.Symbol("B", positive=True)
    C = sp.Symbol("C", real=True)
    H = sp.Matrix(
        [
            [A, C, 0, 0],
            [C, B, 0, 0],
            [0, 0, B, 0],
            [0, 0, 0, B],
        ]
    )
    rotation_pi = sp.diag(1, -1, -1, 1)
    # beta=3/5, gamma=5/4: exact rational Lorentz boost.
    boost = sp.Matrix(
        [
            [sp.Rational(5, 4), -sp.Rational(3, 4), 0, 0],
            [-sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    invariance_equations = list(rotation_pi * H * rotation_pi.T - H)
    invariance_equations += list(boost * H * boost.T - H)
    invariant_solution = sp.solve(invariance_equations, [A, C], dict=True)[0]
    H_invariant = sp.simplify(H.subs(invariant_solution))
    general_form_residual = sp.simplify(H_invariant - B * eta4)
    invariant_nonzero_rank = H_invariant.rank()
    invariant_zero_rank = H_invariant.subs(B, 0).rank()
    rank_three_exists = invariant_nonzero_rank == 3 or invariant_zero_rank == 3

    # No nonzero invariant timelike vector is available from eta alone.
    v0 = sp.Symbol("v_0", real=True)
    V = sp.Matrix([v0, 0, 0, 0])
    vector_solution = sp.solve(list(boost * V - V), [v0], dict=True)
    only_invariant_vector = sp.simplify(V.subs(vector_solution[0]))

    # 2. Vary the multiplier action in a Fourier-mode reduction.
    # Integrating lambda H^mn partial_m partial_n chi by parts gives the
    # kinetic term -H00 lambda_dot chi_dot.
    lam, chi, lam_dot, chi_dot = sp.symbols(
        "lambda chi lambda_dot chi_dot", real=True
    )
    k, source = sp.symbols("k J", real=True)
    L_aux = -A * lam_dot * chi_dot - B * k**2 * lam * chi - source * lam

    lam_ddot, chi_ddot = sp.symbols("lambda_ddot chi_ddot", real=True)
    E_lam = sp.diff(L_aux, lam) - (
        sp.diff(sp.diff(L_aux, lam_dot), chi_dot) * chi_ddot
        + sp.diff(sp.diff(L_aux, lam_dot), lam_dot) * lam_ddot
    )
    E_chi = sp.diff(L_aux, chi) - (
        sp.diff(sp.diff(L_aux, chi_dot), lam_dot) * lam_ddot
        + sp.diff(sp.diff(L_aux, chi_dot), chi_dot) * chi_ddot
    )
    expected_E_lam = A * chi_ddot - B * k**2 * chi - source
    expected_E_chi = A * lam_ddot - B * k**2 * lam
    lambda_equation_residual = sp.simplify(E_lam - expected_E_lam)
    chi_equation_residual = sp.simplify(E_chi - expected_E_chi)

    velocity_hessian = sp.hessian(L_aux, (lam_dot, chi_dot))
    lorentz_velocity_hessian = sp.simplify(velocity_hessian.subs(A, -B))
    lorentz_hessian_det = sp.factor(lorentz_velocity_hessian.det())
    lorentz_eigenvalues = list(lorentz_velocity_hessian.eigenvals().keys())
    lorentz_hessian_nullspace = lorentz_velocity_hessian.nullspace()
    lorentz_has_ghost_sign = bool(
        any(value.is_positive for value in lorentz_eigenvalues)
        and any(value.is_negative for value in lorentz_eigenvalues)
    )

    # Derive the primary list from the null space rather than inserting an
    # expected empty list.  Each null vector would contract the momentum map.
    p_lorentz_lam, p_lorentz_chi = sp.symbols(
        "p_lorentz_lambda p_lorentz_chi", real=True
    )
    lorentz_momenta = sp.Matrix([p_lorentz_lam, p_lorentz_chi])
    lorentz_velocities = sp.Matrix([lam_dot, chi_dot])
    lorentz_momentum_map = lorentz_velocity_hessian * lorentz_velocities
    lorentz_primary_constraints = [
        sp.simplify(null.T * (lorentz_momenta - lorentz_momentum_map))[0]
        for null in lorentz_hessian_nullspace
    ]
    lorentz_secondary_constraints: list[sp.Expr] = []
    lorentz_all_constraints = (
        lorentz_primary_constraints + lorentz_secondary_constraints
    )
    lorentz_poisson_matrix = sp.zeros(len(lorentz_all_constraints))
    lorentz_first_class_count = (
        len(lorentz_all_constraints) - lorentz_poisson_matrix.rank()
    )
    lorentz_second_class_count = lorentz_poisson_matrix.rank()
    lorentz_phase_dimension = 2 * len(lorentz_velocities)
    lorentz_auxiliary_dof = sp.simplify(
        sp.Rational(1, 2)
        * (
            lorentz_phase_dimension
            - 2 * lorentz_first_class_count
            - lorentz_second_class_count
        )
    )

    # 3. Honest elliptic branch H00=0: complete finite-k Dirac chain.
    p_chi, p_lam = sp.symbols("p_chi p_lambda", real=True)
    q_chi, q_lam = sp.symbols("q_chi q_lambda", real=True)
    u_chi, u_lam = sp.symbols("u_chi u_lambda", real=True)
    qs = [q_chi, q_lam]
    ps = [p_chi, p_lam]
    primaries = [p_chi, p_lam]
    canonical_hamiltonian = B * k**2 * q_lam * q_chi + source * q_lam
    total_hamiltonian = canonical_hamiltonian + u_chi * p_chi + u_lam * p_lam
    primary_preservation = [
        _poisson(constraint, total_hamiltonian, qs, ps) for constraint in primaries
    ]
    secondaries = [B * k**2 * q_lam, B * k**2 * q_chi + source]
    all_constraints = primaries + secondaries
    poisson_matrix = sp.Matrix(
        [
            [_poisson(left, right, qs, ps) for right in all_constraints]
            for left in all_constraints
        ]
    )
    poisson_determinant = sp.factor(poisson_matrix.det())
    poisson_rank_nonzero_k = poisson_matrix.rank()
    first_class_nonzero_k = len(all_constraints) - poisson_rank_nonzero_k
    second_class_nonzero_k = poisson_rank_nonzero_k
    auxiliary_dof_nonzero_k = (
        2 * len(qs) - 2 * first_class_nonzero_k - second_class_nonzero_k
    ) // 2
    secondary_preservation = [
        _poisson(constraint, total_hamiltonian, qs, ps)
        for constraint in secondaries
    ]
    elliptic_multiplier_solution = sp.solve(
        [sp.Eq(item, 0) for item in secondary_preservation],
        (u_chi, u_lam),
        dict=True,
    )
    preservation_residuals_after_solution = [
        sp.simplify(item.subs(elliptic_multiplier_solution[0]))
        for item in secondary_preservation
    ]
    tertiary_constraints = [
        item
        for item in preservation_residuals_after_solution
        if item != 0
    ]

    # At k=0 the lambda equation is J_0=0, a source consistency condition.
    source_consistency_condition = source
    nonzero_homogeneous_density_allowed = bool(source_consistency_condition == 0)
    zero_mode_constraints = primaries
    zero_mode_poisson_matrix = sp.Matrix(
        [
            [_poisson(left, right, qs, ps) for right in zero_mode_constraints]
            for left in zero_mode_constraints
        ]
    )
    zero_mode_second_class_count = zero_mode_poisson_matrix.rank()
    zero_mode_first_class_count = (
        len(zero_mode_constraints) - zero_mode_second_class_count
    )
    zero_mode_auxiliary_dof = (
        2 * len(qs) - 2 * zero_mode_first_class_count - zero_mode_second_class_count
    ) // 2

    # 4. The frame-free covariant rank-three algebraic symbol uses momentum.
    # For static spacelike momentum its orthogonal subspace is indefinite.
    q = sp.Symbol("q", positive=True)
    k_static_up = sp.Matrix([0, q, 0, 0])
    k_static_down = eta4 * k_static_up
    k_static_sq = sp.simplify((k_static_up.T * eta4 * k_static_up)[0])
    theta_mixed = sp.simplify(
        sp.eye(4) - k_static_up * k_static_down.T / k_static_sq
    )
    theta_upup = sp.simplify(
        eta4 - k_static_up * k_static_up.T / k_static_sq
    )
    momentum_principal_contraction = sp.simplify(
        (k_static_down.T * theta_upup * k_static_down)[0]
    )
    momentum_idempotence_residual = sp.simplify(theta_mixed**2 - theta_mixed)
    momentum_static_eigenvalues = sorted(
        [
            value
            for value, multiplicity in theta_upup.eigenvals().items()
            if value != 0
            for _ in range(multiplicity)
        ],
        key=str,
    )
    momentum_static_psd = all(
        value.is_nonnegative for value in theta_upup.eigenvals().keys()
    )

    # 5. Normalized metric-derived frames are path dependent when their
    # defining covariant vanishes.
    eta2 = sp.diag(-1, 1)
    rapidity = sp.Symbol("zeta", positive=True)
    u_path_1 = sp.Matrix([1, 0])
    u_path_2 = sp.Matrix([sp.cosh(rapidity), sp.sinh(rapidity)])
    unit_residual_1 = sp.simplify((u_path_1.T * eta2 * u_path_1)[0] + 1)
    unit_residual_2 = sp.trigsimp((u_path_2.T * eta2 * u_path_2)[0] + 1)
    h_path_1 = sp.simplify(eta2 + u_path_1 * u_path_1.T)
    h_path_2 = sp.simplify(eta2 + u_path_2 * u_path_2.T)
    projector_path_difference = sp.simplify(h_path_2 - h_path_1)
    difference_norm_squared = sp.simplify(
        sum(entry**2 for entry in projector_path_difference)
    )
    difference_norm_positive = difference_norm_squared.is_positive
    unique_zero_field_limit = bool(projector_path_difference == sp.zeros(2))

    # A smooth epsilon regularization selects u->0, so h->g is nondegenerate.
    amplitude, regulator = sp.symbols("q_frame epsilon", positive=True)
    regularized_vector = sp.simplify(
        amplitude * u_path_2 / sp.sqrt(amplitude**2 + regulator**2)
    )
    regularized_projector = sp.simplify(
        eta2 + regularized_vector * regularized_vector.T
    )
    zero_field_vector = regularized_vector.applyfunc(
        lambda entry: sp.limit(entry, amplitude, 0, dir="+")
    )
    zero_field_projector = regularized_projector.applyfunc(
        lambda entry: sp.limit(entry, amplitude, 0, dir="+")
    )

    # A Ricci-eigenvector prescription has sensitivity 1/(eigenvalue gap).
    gap = sp.Symbol("Delta_R", positive=True)
    lambda_s, mix = sp.symbols("lambda_s epsilon_R", real=True)
    lambda_t = lambda_s + gap
    curvature_matrix = sp.Matrix([[lambda_t, mix], [mix, lambda_s]])
    eigenvector_first_order = sp.Matrix([1, mix / gap])
    raw_eigen_residual = sp.expand(
        (curvature_matrix - lambda_t * sp.eye(2)) * eigenvector_first_order
    )
    linearized_eigen_residual = raw_eigen_residual.applyfunc(
        lambda entry: sp.diff(entry, mix).subs(mix, 0)
    )
    mixing_coefficient = sp.diff(eigenvector_first_order[1], mix)
    condition_number_limit = sp.limit(mixing_coefficient, gap, 0, dir="+")

    # 6. Referee counterexample: multiplying the normalized spatial metric by
    # the squared norm removes the path ambiguity.  The result is polynomial
    # in V, rank three for every timelike V, and tends uniquely to zero.
    amplitude = sp.Symbol("epsilon_V", positive=True)
    u_path_1_4 = sp.Matrix([1, 0, 0, 0])
    u_path_2_4 = sp.Matrix([sp.cosh(rapidity), sp.sinh(rapidity), 0, 0])
    vector_path_1 = amplitude * u_path_1_4
    vector_path_2 = amplitude * u_path_2_4
    timelike_norm = sp.simplify((vector_path_1.T * eta4 * vector_path_1)[0])

    def vanishing_projector(vector: sp.Matrix) -> sp.Matrix:
        norm = sp.simplify((vector.T * eta4 * vector)[0])
        return sp.simplify((-norm) * eta4 + vector * vector.T)

    vanishing_path_1 = vanishing_projector(vector_path_1)
    vanishing_path_2 = vanishing_projector(vector_path_2)
    vanishing_path_1_limit = vanishing_path_1.applyfunc(
        lambda entry: sp.limit(entry, amplitude, 0, dir="+")
    )
    vanishing_path_2_limit = vanishing_path_2.applyfunc(
        lambda entry: sp.limit(entry, amplitude, 0, dir="+")
    )
    vanishing_difference_limit = (vanishing_path_2 - vanishing_path_1).applyfunc(
        lambda entry: sp.limit(entry, amplitude, 0, dir="+")
    )
    rest_nonzero_eigenvalues = sorted(
        [
            value
            for value, multiplicity in vanishing_path_1.eigenvals().items()
            if value != 0
            for _ in range(multiplicity)
        ],
        key=str,
    )

    # The finite-k elliptic Dirac determinant is no longer uniform: replacing
    # B by epsilon_V^2 makes it vanish as epsilon_V^8.  A source linear in the
    # perturbation then needs chi ~ 1/epsilon_V, so the linear response about
    # the zero-field branch does not exist as a bounded solution.
    rank_changing_poisson = sp.simplify(poisson_matrix.subs(B, amplitude**2))
    rank_changing_determinant = sp.factor(rank_changing_poisson.det())
    linear_source_coefficient = sp.Symbol("J_1", positive=True)
    linear_source_solution = -linear_source_coefficient / (amplitude * k**2)
    linear_source_solution_limit = sp.limit(
        linear_source_solution, amplitude, 0, dir="+"
    )

    # 7. The k=0 result above is an exact-Minkowski fixed-background toy, not
    # the homogeneous equation of h^mn nabla_m nabla_n on FLRW.  Derive the
    # latter from the Christoffel symbols of diag(-1,a^2,a^2,a^2).
    time = sp.Symbol("t", real=True)
    scale = sp.Function("a")(time)
    chi_homogeneous = sp.Function("chi_h")(time)
    flrw_metric = sp.diag(-1, scale**2, scale**2, scale**2)
    flrw_inverse = sp.simplify(flrw_metric.inv())
    coordinates = (time, sp.Symbol("x"), sp.Symbol("y"), sp.Symbol("z"))

    def christoffel(rho: int, mu: int, nu: int) -> sp.Expr:
        return sp.simplify(
            sp.Rational(1, 2)
            * sum(
                flrw_inverse[rho, sigma]
                * (
                    sp.diff(flrw_metric[sigma, nu], coordinates[mu])
                    + sp.diff(flrw_metric[sigma, mu], coordinates[nu])
                    - sp.diff(flrw_metric[mu, nu], coordinates[sigma])
                )
                for sigma in range(4)
            )
        )

    projected_inverse = sp.diag(0, scale**-2, scale**-2, scale**-2)
    covariant_hessian = sp.zeros(4)
    for i in range(1, 4):
        for j in range(1, 4):
            covariant_hessian[i, j] = -christoffel(0, i, j) * sp.diff(
                chi_homogeneous, time
            )
    projected_box_raw = sp.simplify(
        sum(
            projected_inverse[mu, nu] * covariant_hessian[mu, nu]
            for mu in range(4)
            for nu in range(4)
        )
    )
    hubble = sp.Symbol("H_FLRW", nonzero=True, real=True)
    chi_dot_homogeneous = sp.Symbol("chi_dot_FLRW", real=True)
    projected_box = sp.simplify(
        projected_box_raw.subs(
            {
                sp.diff(scale, time): hubble * scale,
                sp.diff(chi_homogeneous, time): chi_dot_homogeneous,
            }
        )
    )
    flrw_lambda_equation = sp.simplify(B * projected_box - source)
    flrw_chi_dot_solution = sp.solve(
        sp.Eq(flrw_lambda_equation, 0), chi_dot_homogeneous
    )[0]

    return {
        "lorentz_invariant_tensor": {
            "A": A,
            "B": B,
            "C": C,
            "ansatz": H,
            "rotation": rotation_pi,
            "boost": boost,
            "solution": invariant_solution,
            "invariant_tensor": H_invariant,
            "general_form_residual": general_form_residual,
            "nonzero_rank": invariant_nonzero_rank,
            "zero_rank": invariant_zero_rank,
            "rank_three_exists": rank_three_exists,
        },
        "lorentz_invariant_vector": {
            "v0": v0,
            "solution": vector_solution,
            "only_invariant_vector": only_invariant_vector,
        },
        "varied_auxiliary_action": {
            "lagrangian": L_aux,
            "lambda_equation": E_lam,
            "chi_equation": E_chi,
            "lambda_equation_residual": lambda_equation_residual,
            "chi_equation_residual": chi_equation_residual,
            "velocity_hessian": velocity_hessian,
            "lorentz_branch_velocity_hessian": lorentz_velocity_hessian,
            "lorentz_branch_velocity_hessian_rank": lorentz_velocity_hessian.rank(),
            "lorentz_branch_velocity_hessian_determinant": lorentz_hessian_det,
            "lorentz_branch_velocity_hessian_eigenvalues": lorentz_eigenvalues,
            "lorentz_branch_velocity_hessian_nullspace": lorentz_hessian_nullspace,
            "lorentz_branch_primary_constraints": lorentz_primary_constraints,
            "lorentz_branch_primary_constraint_count": len(
                lorentz_primary_constraints
            ),
            "lorentz_branch_secondary_constraints": lorentz_secondary_constraints,
            "lorentz_branch_poisson_matrix": lorentz_poisson_matrix,
            "lorentz_branch_first_class_count": lorentz_first_class_count,
            "lorentz_branch_second_class_count": lorentz_second_class_count,
            "lorentz_branch_phase_dimension": lorentz_phase_dimension,
            "lorentz_branch_auxiliary_dof": lorentz_auxiliary_dof,
            "lorentz_branch_has_ghost_sign": lorentz_has_ghost_sign,
        },
        "elliptic_dirac": {
            "k!=0": {
                "primary_constraints": primaries,
                "primary_preservation": primary_preservation,
                "secondary_constraints": secondaries,
                "secondary_preservation": secondary_preservation,
                "multiplier_solution": elliptic_multiplier_solution,
                "preservation_residuals_after_solution": (
                    preservation_residuals_after_solution
                ),
                "tertiary_constraints": tertiary_constraints,
                "poisson_matrix": poisson_matrix,
                "poisson_determinant": poisson_determinant,
                "first_class_count": first_class_nonzero_k,
                "second_class_count": second_class_nonzero_k,
                "auxiliary_dof": auxiliary_dof_nonzero_k,
            },
            "k=0": {
                "scope": "exact Minkowski fixed-background Fourier toy (Hubble=0)",
                "source_consistency_condition": source_consistency_condition,
                "nonzero_homogeneous_density_allowed": nonzero_homogeneous_density_allowed,
                "primary_constraints": primaries,
                "secondary_constraints_if_J0_zero": [],
                "poisson_matrix_if_J0_zero": zero_mode_poisson_matrix,
                "first_class_count_if_J0_zero": zero_mode_first_class_count,
                "second_class_count_if_J0_zero": zero_mode_second_class_count,
                "auxiliary_dof_if_J0_zero": zero_mode_auxiliary_dof,
            },
        },
        "momentum_projector": {
            "mixed": theta_mixed,
            "bilinear": theta_upup,
            "idempotence_residual": momentum_idempotence_residual,
            "static_rank": theta_upup.rank(),
            "static_nonzero_eigenvalues": momentum_static_eigenvalues,
            "static_positive_semidefinite": momentum_static_psd,
            "principal_contraction": momentum_principal_contraction,
            "supplies_second_order_operator_for_same_mode": bool(
                momentum_principal_contraction != 0
            ),
            "zero_momentum_defined": False,
            "null_momentum_defined": False,
        },
        "normalized_metric_frame": {
            "unit_norm_residual_path_1": unit_residual_1,
            "unit_norm_residual_path_2": unit_residual_2,
            "projector_path_1": h_path_1,
            "projector_path_2": h_path_2,
            "projector_path_difference": projector_path_difference,
            "difference_norm_squared": difference_norm_squared,
            "difference_norm_positive": difference_norm_positive,
            "unique_zero_field_limit": unique_zero_field_limit,
        },
        "regularized_frame": {
            "metric": eta2,
            "vector": regularized_vector,
            "projector": regularized_projector,
            "zero_field_vector": zero_field_vector,
            "zero_field_projector": zero_field_projector,
            "zero_field_projector_rank": zero_field_projector.rank(),
            "zero_field_projector_determinant": zero_field_projector.det(),
            "spatial_kernel_dimension": 2 - zero_field_projector.rank(),
        },
        "curvature_eigenframe": {
            "gap": gap,
            "matrix": curvature_matrix,
            "first_order_eigenvector": eigenvector_first_order,
            "linearized_mixing_residual": linearized_eigen_residual,
            "mixing_coefficient": mixing_coefficient,
            "condition_number_limit": condition_number_limit,
        },
        "vanishing_projector_counterexample": {
            "amplitude": amplitude,
            "timelike_norm": timelike_norm,
            "path_1": vanishing_path_1,
            "path_2": vanishing_path_2,
            "rest_frame_projector_rank_nonzero": vanishing_path_1.rank(),
            "rest_frame_projector_nonzero_eigenvalues": rest_nonzero_eigenvalues,
            "path_1_zero_limit": vanishing_path_1_limit,
            "path_2_zero_limit": vanishing_path_2_limit,
            "path_difference_zero_limit": vanishing_difference_limit,
            "broad_regular_no_go_is_false": True,
        },
        "vanishing_projector_rank_change": {
            "amplitude": amplitude,
            "k": k,
            "poisson_matrix": rank_changing_poisson,
            "poisson_determinant": rank_changing_determinant,
            "rank_nonzero_amplitude": rank_changing_poisson.rank(),
            "rank_zero_amplitude": rank_changing_poisson.subs(amplitude, 0).rank(),
            "linear_source_coefficient": linear_source_coefficient,
            "linear_source_solution": linear_source_solution,
            "linear_source_solution_limit": linear_source_solution_limit,
            "branch_status": "OPEN: rank-changing/strong-coupling audit required",
        },
        "flrw_homogeneous_contraction": {
            "metric": flrw_metric,
            "projected_inverse": projected_inverse,
            "covariant_hessian": covariant_hessian,
            "projected_box_raw": projected_box_raw,
            "covariant_projected_box": projected_box,
            "derived_contraction_residual": sp.simplify(
                projected_box + 3 * hubble * chi_dot_homogeneous
            ),
            "hubble": hubble,
            "chi_dot": chi_dot_homogeneous,
            "B": B,
            "source": source,
            "lambda_equation": flrw_lambda_equation,
            "chi_dot_solution": flrw_chi_dot_solution,
            "nonzero_source_allowed_for_expanding_flrw": bool(
                flrw_chi_dot_solution.has(source)
                and not flrw_chi_dot_solution.has(sp.zoo)
            ),
            "full_minisuperspace_dirac_status": (
                "OPEN: mixes lambda, chi, and metric momenta"
            ),
        },
        "mode_sectors": {
            "k=0": {
                "regular_metric_only_projector_exists": rank_three_exists,
                "smooth_vanishing_projector_exists": True,
                "source_consistency_condition": source_consistency_condition,
            },
            "k!=0": {
                "lorentz_momentum_projector_is_elliptic": momentum_static_psd,
                "momentum_projector_requires_inverse_symbol": True,
            },
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_projector_gate()
    invariant = result["lorentz_invariant_tensor"]
    vector = result["lorentz_invariant_vector"]
    action = result["varied_auxiliary_action"]
    elliptic = result["elliptic_dirac"]
    momentum = result["momentum_projector"]
    normalized = result["normalized_metric_frame"]
    regularized = result["regularized_frame"]
    eigenframe = result["curvature_eigenframe"]
    counterexample = result["vanishing_projector_counterexample"]
    rank_change = result["vanishing_projector_rank_change"]
    flrw = result["flrw_homogeneous_contraction"]

    print("=" * 98)
    print("METRIC-ONLY ELLIPTIC PROJECTOR / ZERO-FIELD GATE")
    print("=" * 98)
    print("\n[1] Lorentz stabilizer at the exact Minkowski branch")
    print("  invariant H solution =", invariant["solution"])
    print("  H =", invariant["invariant_tensor"])
    print("  ranks (B!=0, B=0) =", invariant["nonzero_rank"], invariant["zero_rank"])
    print("  invariant vector solution =", vector["solution"])
    checks = [
        _check(
            "regular metric-only H is B*eta or zero, never a rank-3 spatial projector",
            invariant["general_form_residual"] == sp.zeros(4)
            and not invariant["rank_three_exists"],
        ),
        _check(
            "the Minkowski metric supplies no nonzero invariant clock vector",
            vector["only_invariant_vector"] == sp.zeros(4, 1),
        ),
    ]

    print("\n[2] The multiplier action is varied")
    print("  L_aux =", action["lagrangian"])
    print("  E_lambda =", action["lambda_equation"])
    print("  E_chi =", action["chi_equation"])
    print("  Lorentz-branch Hessian =", action["lorentz_branch_velocity_hessian"])
    print("  determinant =", action["lorentz_branch_velocity_hessian_determinant"], "; rank =", action["lorentz_branch_velocity_hessian_rank"])
    print("  eigenvalues =", action["lorentz_branch_velocity_hessian_eigenvalues"])
    checks.append(
        _check(
            "nonzero Lorentz branch is hyperbolic with two auxiliary modes and one ghost sign",
            action["lambda_equation_residual"] == 0
            and action["chi_equation_residual"] == 0
            and action["lorentz_branch_velocity_hessian_rank"] == 2
            and action["lorentz_branch_velocity_hessian_determinant"] < 0
            and action["lorentz_branch_auxiliary_dof"] == 2
            and action["lorentz_branch_has_ghost_sign"],
        )
    )

    print("\n[3] Genuine elliptic branch: complete finite-k Dirac chain")
    print("  primaries =", elliptic["k!=0"]["primary_constraints"])
    print("  preservation =", elliptic["k!=0"]["primary_preservation"])
    print("  secondaries =", elliptic["k!=0"]["secondary_constraints"])
    print("  secondary preservation =", elliptic["k!=0"]["secondary_preservation"])
    print("  tertiaries =", elliptic["k!=0"]["tertiary_constraints"])
    print("  PB matrix =", elliptic["k!=0"]["poisson_matrix"])
    print("  det(PB) =", elliptic["k!=0"]["poisson_determinant"])
    print("  first/second class =", elliptic["k!=0"]["first_class_count"], "/", elliptic["k!=0"]["second_class_count"])
    print("  auxiliary DOF =", elliptic["k!=0"]["auxiliary_dof"])
    print("  k=0 toy scope =", elliptic["k=0"]["scope"])
    print("  k=0 toy source condition =", elliptic["k=0"]["source_consistency_condition"], "= 0")
    print("  k=0 (if J_0=0) first/second class =", elliptic["k=0"]["first_class_count_if_J0_zero"], "/", elliptic["k=0"]["second_class_count_if_J0_zero"])
    print("  k=0 auxiliary DOF =", elliptic["k=0"]["auxiliary_dof_if_J0_zero"])
    checks.append(
        _check(
            "at k!=0 the elliptic pair has four second-class constraints and zero auxiliary DOF",
            elliptic["k!=0"]["poisson_matrix"].rank() == 4
            and elliptic["k!=0"]["poisson_determinant"] != 0
            and elliptic["k!=0"]["tertiary_constraints"] == []
            and elliptic["k!=0"]["auxiliary_dof"] == 0,
        )
    )
    checks.append(
        _check(
            "in the exact-Minkowski toy, k=0 requires the homogeneous source to vanish",
            not elliptic["k=0"]["nonzero_homogeneous_density_allowed"]
            and elliptic["k=0"]["poisson_matrix_if_J0_zero"].rank() == 0
            and elliptic["k=0"]["auxiliary_dof_if_J0_zero"] == 0,
        )
    )
    print("  covariant FLRW h^mn nabla_mn chi =", flrw["covariant_projected_box"])
    print("  FLRW lambda equation =", flrw["lambda_equation"], "= 0")
    print("  expanding-branch solution chi_dot =", flrw["chi_dot_solution"])
    checks.append(
        _check(
            "the covariant FLRW operator can carry nonzero homogeneous source when H!=0",
            flrw["derived_contraction_residual"] == 0
            and flrw["nonzero_source_allowed_for_expanding_flrw"],
        )
    )

    print("\n[4] Frame-free momentum projector")
    print("  Theta^mu_nu(static k) =", momentum["mixed"])
    print("  Theta^munu(static k) =", momentum["bilinear"])
    print("  nonzero bilinear eigenvalues =", momentum["static_nonzero_eigenvalues"])
    print("  Theta^munu k_mu k_nu =", momentum["principal_contraction"])
    checks.append(
        _check(
            "momentum projector is indefinite for static k and singular at k=0/null k",
            momentum["idempotence_residual"] == sp.zeros(4)
            and momentum["static_rank"] == 3
            and not momentum["static_positive_semidefinite"]
            and momentum["principal_contraction"] == 0
            and not momentum["supplies_second_order_operator_for_same_mode"]
            and not momentum["zero_momentum_defined"]
            and not momentum["null_momentum_defined"],
        )
    )

    print("\n[5] Metric-derived frame and exact zero-field control")
    print("  path-1 projector =", normalized["projector_path_1"])
    print("  path-2 projector =", normalized["projector_path_2"])
    print("  squared path difference =", normalized["difference_norm_squared"])
    print("  regulated h(0) =", regularized["zero_field_projector"], "; rank =", regularized["zero_field_projector_rank"])
    print("  Ricci eigenframe mixing = epsilon_R /", eigenframe["gap"])
    print("  zero-gap condition number =", eigenframe["condition_number_limit"])
    checks.append(
        _check(
            "exact normalization is path-dependent as the metric covariant vanishes",
            normalized["unit_norm_residual_path_1"] == 0
            and normalized["unit_norm_residual_path_2"] == 0
            and not normalized["unique_zero_field_limit"]
            and normalized["difference_norm_positive"],
        )
    )
    checks.append(
        _check(
            "the additive normalization regulator gives h(0)=eta and removes its spatial kernel",
            regularized["zero_field_projector"] == regularized["metric"]
            and regularized["spatial_kernel_dimension"] == 0,
        )
    )
    checks.append(
        _check(
            "the illustrative symmetric eigenvalue-gap sensitivity diverges at degeneracy",
            eigenframe["linearized_mixing_residual"] == sp.zeros(2, 1)
            and eigenframe["mixing_coefficient"] == 1 / eigenframe["gap"]
            and eigenframe["condition_number_limit"].is_infinite,
        )
    )

    print("\n[6] Smooth vanishing-projector loophole and rank change")
    print("  H_rest =", counterexample["path_1"])
    print("  H_boosted =", counterexample["path_2"])
    print("  both zero-field limits =", counterexample["path_1_zero_limit"])
    print("  det(PB) with B=epsilon_V^2 =", rank_change["poisson_determinant"])
    print("  ranks (epsilon_V>0, epsilon_V=0) =", rank_change["rank_nonzero_amplitude"], rank_change["rank_zero_amplitude"])
    print("  chi for J=epsilon_V J_1 =", rank_change["linear_source_solution"])
    checks.append(
        _check(
            "a polynomial rank-three projector can vanish smoothly at Minkowski",
            counterexample["rest_frame_projector_rank_nonzero"] == 3
            and counterexample["path_1_zero_limit"] == sp.zeros(4)
            and counterexample["path_2_zero_limit"] == sp.zeros(4)
            and counterexample["path_difference_zero_limit"] == sp.zeros(4)
            and counterexample["broad_regular_no_go_is_false"],
        )
    )
    checks.append(
        _check(
            "that loophole loses constraint rank and bounded linear source response at zero field",
            rank_change["poisson_determinant"]
            == rank_change["amplitude"] ** 8 * rank_change["k"] ** 8
            and rank_change["rank_nonzero_amplitude"] == 4
            and rank_change["rank_zero_amplitude"] == 0
            and rank_change["linear_source_solution_limit"].is_infinite,
        )
    )

    print("\n[VERDICT]")
    print("  CORRECTED LEMMA: Poincare-covariant metric-only H cannot remain a")
    print("  NONZERO rank-three elliptic projector at the exact zero-field branch.")
    print("  H=B*g is hyperbolic and propagates a ghost-signed multiplier pair;")
    print("  H=0 has no linear Poisson operator. But H=(-V^2)g+VV is a smooth")
    print("  metric-derived counterexample away from zero and vanishes uniquely at zero.")
    print("  Its flat-space elliptic PB determinant scales as epsilon_V^8 and a linear source")
    print("  requires chi~1/epsilon_V. BROAD NO-GO WITHDRAWN; this branch is OPEN.")
    print("  The covariant FLRW contraction instead contains -3 H chi_dot, so the")
    print("  full homogeneous Dirac chain is also OPEN; J_0=0 was only the flat toy.")
    print("  Next: vary a full curvature-polynomial realization and test whether the")
    print("  rank-changing nonlinear y->0 branch is controlled or strongly coupled.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
