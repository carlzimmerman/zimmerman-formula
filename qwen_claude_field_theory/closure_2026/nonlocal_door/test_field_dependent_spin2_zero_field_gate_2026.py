#!/usr/bin/env python3
"""Tests for the universal field-dependent spin-2 zero-field gate."""

from field_dependent_spin2_zero_field_gate_2026 import derive_zero_field_gate


def test_exact_exponential_law_is_derived_from_the_primitive():
    result = derive_zero_field_gate()
    kernel = result["kernel"]

    assert kernel["mu_residual"] == 0
    assert kernel["deep_mond_residual"] == 0
    assert kernel["newtonian_limit"] == 1


def test_two_tensor_hessian_is_healthy_at_nonzero_acceleration():
    result = derive_zero_field_gate()
    tensor = result["tensor"]

    assert tensor["generic_rank"] == 2
    assert tensor["generic_determinant_positive"]
    assert tensor["tensor_speed_squared"] == 1


def test_general_covariant_projectors_make_no_slip_force_universality():
    result = derive_zero_field_gate()
    projector = result["projector"]

    assert projector["projector_idempotence_residual"] == 0
    assert projector["projector_orthogonality_residual"] == 0
    assert projector["gamma_minus_one_numerator"] != 0
    assert projector["no_slip_solution"] == [projector["spin2_form_factor"]]
    assert projector["common_response_ratio"] == 1 / projector["spin2_form_factor"]


def test_exact_zero_field_branch_loses_both_tensor_kinetic_terms():
    result = derive_zero_field_gate()
    zero = result["zero_field"]

    assert zero["hessian_rank"] == 0
    assert len(zero["primary_constraints"]) == 2
    assert zero["secondary_constraints"] == []
    assert zero["poisson_bracket_matrix"].rank() == 0
    assert zero["first_class_count"] == 2
    assert zero["quadratic_tensor_dof"] == 0


def test_rank_loss_occurs_in_homogeneous_and_inhomogeneous_sectors():
    result = derive_zero_field_gate()
    sectors = result["zero_field"]["mode_sectors"]

    assert sectors["k=0"]["rank"] == 0
    assert sectors["k!=0"]["rank"] == 0


def test_propagator_residue_diverges_toward_zero_field():
    result = derive_zero_field_gate()
    strong = result["strong_coupling"]

    assert strong["inverse_kinetic_limit"].is_infinite
    assert strong["quadratic_action_starts_above_second_order"]


def test_positive_floor_breaks_the_exact_mond_law():
    result = derive_zero_field_gate()
    floor = result["floor_repair"]

    assert floor["tensor_hessian_rank_at_zero"] == 2
    assert floor["mond_residual"] != 0
    assert floor["deep_mond_flux_ratio_limit"].is_infinite
    assert floor["exact_target_preserved"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
