#!/usr/bin/env python3
"""Tests for the standard CTP auxiliary Dirac gate."""

from ctp_auxiliary_dirac_gate_2026 import derive_ctp_auxiliary_dirac_gate


def test_ctp_doubled_action_is_regular_before_boundary_data():
    result = derive_ctp_auxiliary_dirac_gate()

    assert result["kinetic"]["hessian_det"] != 0
    assert result["kinetic"]["is_regular"] is True


def test_physical_branch_matching_is_not_a_second_class_reduction():
    result = derive_ctp_auxiliary_dirac_gate()

    assert result["physical_branch"]["is_closed"] is True
    assert result["physical_branch"]["pb_rank"] < result["physical_branch"]["pb_matrix"].rows
    assert result["physical_branch"]["is_second_class"] is False


def test_difference_variation_recovers_the_driven_retarded_equation():
    result = derive_ctp_auxiliary_dirac_gate()

    assert result["variation"]["c_equation_residual"] == 0


def test_matching_fails_to_be_second_class_in_zero_and_nonzero_k_sectors():
    result = derive_ctp_auxiliary_dirac_gate()

    assert result["mode_sectors"]["k=0"]["is_second_class"] is False
    assert result["mode_sectors"]["k!=0"]["is_second_class"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
