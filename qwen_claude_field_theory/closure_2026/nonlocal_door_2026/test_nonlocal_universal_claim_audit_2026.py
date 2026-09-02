#!/usr/bin/env python3
"""Regression tests for the adversarial audit of the claimed nonlocal theorem."""

from nonlocal_universal_claim_audit_2026 import derive_nonlocal_claim_audit


def test_local_aqual_exterior_flux_carries_enclosed_mass_without_a_dark_field():
    result = derive_nonlocal_claim_audit()

    assert result["aqual"]["primitive_residual"] == 0
    assert result["aqual"]["euler_residual"] == 0
    assert result["aqual"]["vacuum_flux_derivative"] == 0
    assert result["aqual"]["exterior_flux_contains_mass"] is True


def test_ratio_lock_is_conditional_on_a_shared_unsourced_flux():
    result = derive_nonlocal_claim_audit()

    assert result["ratio_lock"]["shared_flux_ratio_derivative"] == 0
    assert result["ratio_lock"]["sourced_ratio_derivative"] != 0


def test_retarded_kernel_is_not_a_single_copy_action_hessian_inverse():
    result = derive_nonlocal_claim_audit()

    assert result["variational_causality"]["retarded_is_symmetric"] is False
    assert result["variational_causality"]["inverse_hessian_is_symmetric"] is True
    assert result["variational_causality"]["single_copy_retarded_action_exists"] is False


def test_standard_localization_has_an_indefinite_regular_kinetic_block():
    result = derive_nonlocal_claim_audit()

    assert result["localization"]["hessian_det"] != 0
    assert result["localization"]["hessian_rank"] == 2
    assert result["localization"]["primary_constraint_count"] == 0
    assert result["localization"]["eigenvalue_product"] < 0


def test_standard_localization_dirac_count_closes_in_both_momentum_sectors():
    result = derive_nonlocal_claim_audit()
    localization = result["localization"]

    assert localization["primary_constraints"] == []
    assert localization["secondary_constraints"] == []
    assert localization["poisson_bracket_matrix"].shape == (0, 0)
    assert localization["first_class_count"] == 0
    assert localization["second_class_count"] == 0
    assert localization["configuration_dof"] == 2
    assert localization["diagonal_kinetic_hessian"].det() < 0
    assert localization["mode_sectors"]["k=0"]["configuration_dof"] == 2
    assert localization["mode_sectors"]["k!=0"]["configuration_dof"] == 2


def test_toy_response_does_not_compute_alpha3_or_gravitational_dof():
    result = derive_nonlocal_claim_audit()

    assert result["ppn"]["response_matches_retarded_template"] is True
    assert result["ppn"]["alpha3_derived"] is False
    assert result["ppn"]["gravitational_dof_derived"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
