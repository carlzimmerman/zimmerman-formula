#!/usr/bin/env python3
"""Regression tests for the metric-only elliptic-projector zero-field gate."""

import sympy as sp

from metric_only_elliptic_projector_gate_2026 import derive_projector_gate, main


def test_lorentz_invariance_forbids_a_rank_three_spatial_tensor_at_minkowski():
    result = derive_projector_gate()
    invariant = result["lorentz_invariant_tensor"]

    assert invariant["solution"] == {
        invariant["A"]: -invariant["B"],
        invariant["C"]: 0,
    }
    assert invariant["general_form_residual"] == sp.zeros(4)
    assert invariant["nonzero_rank"] == 4
    assert invariant["zero_rank"] == 0
    assert invariant["rank_three_exists"] is False


def test_no_nonzero_lorentz_invariant_clock_vector_exists():
    result = derive_projector_gate()
    vector = result["lorentz_invariant_vector"]

    assert vector["solution"] == [{vector["v0"]: 0}]
    assert vector["only_invariant_vector"] == sp.zeros(4, 1)


def test_varied_lorentz_covariant_auxiliary_action_is_hyperbolic_and_ghost_signed():
    result = derive_projector_gate()
    action = result["varied_auxiliary_action"]

    assert action["lambda_equation_residual"] == 0
    assert action["chi_equation_residual"] == 0
    assert action["lorentz_branch_velocity_hessian_rank"] == 2
    assert action["lorentz_branch_velocity_hessian_determinant"] < 0
    assert action["lorentz_branch_velocity_hessian_nullspace"] == []
    assert action["lorentz_branch_primary_constraints"] == []
    assert action["lorentz_branch_primary_constraint_count"] == (
        2 - action["lorentz_branch_velocity_hessian_rank"]
    )
    assert action["lorentz_branch_auxiliary_dof"] == 2
    assert action["lorentz_branch_auxiliary_dof"] == sp.Rational(1, 2) * (
        action["lorentz_branch_phase_dimension"]
        - 2 * action["lorentz_branch_first_class_count"]
        - action["lorentz_branch_second_class_count"]
    )
    assert action["lorentz_branch_has_ghost_sign"] is True


def test_elliptic_branch_dirac_chain_closes_only_for_nonzero_spatial_momentum():
    result = derive_projector_gate()
    elliptic = result["elliptic_dirac"]

    assert len(elliptic["k!=0"]["primary_constraints"]) == 2
    assert len(elliptic["k!=0"]["secondary_constraints"]) == 2
    assert elliptic["k!=0"]["poisson_matrix"].rank() == 4
    assert elliptic["k!=0"]["poisson_determinant"] != 0
    assert elliptic["k!=0"]["multiplier_solution"] != []
    assert elliptic["k!=0"]["preservation_residuals_after_solution"] == [0, 0]
    assert elliptic["k!=0"]["tertiary_constraints"] == []
    assert elliptic["k!=0"]["first_class_count"] == 0
    assert elliptic["k!=0"]["second_class_count"] == 4
    assert elliptic["k!=0"]["auxiliary_dof"] == 0
    assert elliptic["k=0"]["source_consistency_condition"] != 0
    assert elliptic["k=0"]["nonzero_homogeneous_density_allowed"] is False
    assert elliptic["k=0"]["poisson_matrix_if_J0_zero"].rank() == 0
    assert elliptic["k=0"]["first_class_count_if_J0_zero"] == 2
    assert elliptic["k=0"]["second_class_count_if_J0_zero"] == 0
    assert elliptic["k=0"]["auxiliary_dof_if_J0_zero"] == 0


def test_fixed_flat_zero_mode_is_not_misreported_as_the_covariant_flrw_equation():
    """Catches omission of the extrinsic-curvature term in h^mn nabla_mn chi."""
    result = derive_projector_gate()
    homogeneous = result["flrw_homogeneous_contraction"]

    assert homogeneous["derived_contraction_residual"] == 0
    assert homogeneous["covariant_projected_box"] == (
        -3 * homogeneous["hubble"] * homogeneous["chi_dot"]
    )
    assert homogeneous["lambda_equation"] == (
        -3
        * homogeneous["B"]
        * homogeneous["hubble"]
        * homogeneous["chi_dot"]
        - homogeneous["source"]
    )
    assert homogeneous["chi_dot_solution"] == (
        -homogeneous["source"]
        / (3 * homogeneous["B"] * homogeneous["hubble"])
    )
    assert homogeneous["nonzero_source_allowed_for_expanding_flrw"] is True
    assert result["elliptic_dirac"]["k=0"]["scope"] == (
        "exact Minkowski fixed-background Fourier toy (Hubble=0)"
    )


def test_momentum_projector_is_not_a_regular_elliptic_slice_projector():
    result = derive_projector_gate()
    momentum = result["momentum_projector"]

    assert momentum["idempotence_residual"] == sp.zeros(4)
    assert momentum["static_rank"] == 3
    assert momentum["static_nonzero_eigenvalues"] == [-1, 1, 1]
    assert momentum["static_positive_semidefinite"] is False
    assert momentum["zero_momentum_defined"] is False
    assert momentum["null_momentum_defined"] is False
    assert momentum["principal_contraction"] == 0
    assert momentum["supplies_second_order_operator_for_same_mode"] is False


def test_metric_derived_normalized_frame_has_a_path_dependent_zero_field_limit():
    result = derive_projector_gate()
    normalized = result["normalized_metric_frame"]

    assert normalized["unit_norm_residual_path_1"] == 0
    assert normalized["unit_norm_residual_path_2"] == 0
    assert normalized["projector_path_difference"] != sp.zeros(2)
    assert normalized["difference_norm_squared"].is_positive
    assert normalized["unique_zero_field_limit"] is False


def test_regularization_removes_the_spatial_kernel_at_zero_field():
    result = derive_projector_gate()
    regularized = result["regularized_frame"]

    assert regularized["zero_field_vector"] == sp.zeros(2, 1)
    assert regularized["zero_field_projector"] == regularized["metric"]
    assert regularized["zero_field_projector_rank"] == 2
    assert regularized["zero_field_projector_determinant"] != 0
    assert regularized["spatial_kernel_dimension"] == 0


def test_smooth_vanishing_projector_refutes_the_broad_regular_projector_claim():
    """Catches the missed branch H=(-V^2)g+VV, which stays regular by vanishing."""
    result = derive_projector_gate()
    counterexample = result["vanishing_projector_counterexample"]

    assert counterexample["timelike_norm"] < 0
    assert counterexample["rest_frame_projector_rank_nonzero"] == 3
    assert counterexample["rest_frame_projector_nonzero_eigenvalues"] == [
        counterexample["amplitude"] ** 2,
        counterexample["amplitude"] ** 2,
        counterexample["amplitude"] ** 2,
    ]
    assert counterexample["path_1_zero_limit"] == sp.zeros(4)
    assert counterexample["path_2_zero_limit"] == sp.zeros(4)
    assert counterexample["path_difference_zero_limit"] == sp.zeros(4)
    assert counterexample["broad_regular_no_go_is_false"] is True


def test_vanishing_projector_loses_dirac_rank_and_linear_source_response():
    """Catches any attempt to relabel a smooth rank-changing branch as closed."""
    result = derive_projector_gate()
    rank_change = result["vanishing_projector_rank_change"]

    assert rank_change["poisson_determinant"] == (
        rank_change["amplitude"] ** 8 * rank_change["k"] ** 8
    )
    assert rank_change["rank_nonzero_amplitude"] == 4
    assert rank_change["rank_zero_amplitude"] == 0
    assert rank_change["linear_source_solution"].has(
        1 / rank_change["amplitude"]
    )
    assert rank_change["linear_source_solution_limit"].is_infinite
    assert rank_change["branch_status"] == "OPEN: rank-changing/strong-coupling audit required"


def test_curvature_eigenframe_is_singular_when_the_minkowski_gap_closes():
    result = derive_projector_gate()
    eigenframe = result["curvature_eigenframe"]

    assert eigenframe["linearized_mixing_residual"] == sp.zeros(2, 1)
    assert eigenframe["mixing_coefficient"] == 1 / eigenframe["gap"]
    assert eigenframe["condition_number_limit"].is_infinite


def test_gate_separates_homogeneous_and_inhomogeneous_sectors():
    result = derive_projector_gate()
    sectors = result["mode_sectors"]

    assert sectors["k=0"]["regular_metric_only_projector_exists"] is False
    assert sectors["k!=0"]["lorentz_momentum_projector_is_elliptic"] is False
    assert sectors["k!=0"]["momentum_projector_requires_inverse_symbol"] is True


def test_main_runs_the_rank_changing_diagnostic_to_completion():
    """Catches report-only name errors that unit-level derivations do not reach."""
    assert main() == 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
