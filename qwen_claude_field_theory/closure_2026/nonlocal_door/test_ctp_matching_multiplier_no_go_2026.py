#!/usr/bin/env python3
"""Tests for the explicit-multiplier attempt to constrain the CTP difference field."""

from ctp_matching_multiplier_no_go_2026 import derive_matching_multiplier_gate


def test_matching_multiplier_removes_the_driven_equation_instead_of_deriving_it():
    result = derive_matching_multiplier_gate()

    assert result["variation"]["difference_equation_residual"] == 0
    assert result["variation"]["matching_constraint_residual"] == 0
    assert result["variation"]["multiplier_solution_contains_c_acceleration"] is True
    assert result["variation"]["physical_response_is_determined"] is False


def test_dirac_chain_is_not_a_second_class_completion_in_both_mode_sectors():
    result = derive_matching_multiplier_gate()

    assert result["dirac"]["is_closed"] is True
    assert result["dirac"]["is_second_class"] is False
    assert result["mode_sectors"]["k=0"]["is_second_class"] is False
    assert result["mode_sectors"]["k!=0"]["is_second_class"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
