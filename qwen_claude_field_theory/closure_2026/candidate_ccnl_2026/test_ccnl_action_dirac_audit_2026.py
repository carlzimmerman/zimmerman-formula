#!/usr/bin/env python3
"""Regression tests for the action-level CCNL falsification audit."""

from ccnl_action_dirac_audit_2026 import derive_ccnl_action_audit


def test_exact_exponential_kernel_is_derived():
    result = derive_ccnl_action_audit()
    kernel = result["kernel"]
    assert kernel["mu_residual"] == 0
    assert kernel["deep_mond_residual"] == 0
    assert kernel["newtonian_limit"] == 1


def test_localized_auxiliary_pair_is_regular_and_indefinite():
    result = derive_ccnl_action_audit()
    local = result["localization"]
    assert local["hessian_det"] < 0
    assert local["hessian_rank"] == 2
    assert local["eigenvalue_product"] == local["hessian_det"]
    assert local["primary_constraints"] == []
    assert local["secondary_constraints"] == []
    assert local["configuration_dof"] == 2
    assert all(sector["configuration_dof"] == 2 for sector in local["mode_sectors"].values())


def test_candidate_specific_hessian_never_becomes_degenerate():
    result = derive_ccnl_action_audit()
    local = result["localization"]
    assert local["candidate_hessian_det"] == -1
    assert local["candidate_hessian_rank"] == 2
    assert local["candidate_eigenvalue_product"] == -1


def test_homogeneous_metric_mixing_does_not_restore_degeneracy():
    result = derive_ccnl_action_audit()
    mini = result["minisuperspace"]
    assert mini["determinant_residual"] == 0
    assert mini["background_determinant"] > 0
    assert mini["background_rank"] == 3


def test_retarded_history_is_not_a_dirac_constraint():
    result = derive_ccnl_action_audit()
    causal = result["variational_causality"]
    assert causal["ordinary_inverse_hessian_is_symmetric"]
    assert not causal["retarded_kernel_is_symmetric"]
    assert not causal["retarded_history_is_phase_space_constraint"]


def test_zero_M_initial_data_do_not_generically_give_M_equals_minus_f():
    result = derive_ccnl_action_audit()
    transport = result["dw_transport"]
    assert transport["transport_residual"] == 0
    assert transport["minus_f_residual"] != 0
    assert not transport["M_equals_minus_f_generically"]


def test_exact_no_slip_and_ppn_are_not_certified():
    result = derive_ccnl_action_audit()
    slip = result["slip"]
    ppn = result["ppn_provenance"]
    assert slip["trace_free_source_norm_sq"] != 0
    assert not slip["exact_no_slip"]
    assert not ppn["beta_derived"]
    assert not ppn["preferred_frame_parameters_derived"]


def test_zero_field_continuation_is_not_twice_differentiable():
    result = derive_ccnl_action_audit()
    zero = result["zero_field"]
    assert zero["value_continuous"]
    assert zero["first_derivative_continuous"]
    assert not zero["finite_second_derivative"]


if __name__ == "__main__":
    tests = [
        test_exact_exponential_kernel_is_derived,
        test_localized_auxiliary_pair_is_regular_and_indefinite,
        test_candidate_specific_hessian_never_becomes_degenerate,
        test_homogeneous_metric_mixing_does_not_restore_degeneracy,
        test_retarded_history_is_not_a_dirac_constraint,
        test_zero_M_initial_data_do_not_generically_give_M_equals_minus_f,
        test_exact_no_slip_and_ppn_are_not_certified,
        test_zero_field_continuation_is_not_twice_differentiable,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
