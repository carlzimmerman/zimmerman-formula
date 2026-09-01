#!/usr/bin/env python3
"""Tests for the tensor nonlocal-localization ghost gate."""

from tensor_nonlocal_localization_gate_2026 import derive_tensor_localization_gate


def test_tensor_multiplier_localization_has_indefinite_tt_kinetic_block():
    result = derive_tensor_localization_gate()

    assert result["kinetic"]["determinant"] != 0
    assert result["kinetic"]["eigenvalue_product"] < 0


def test_retarded_condition_is_not_a_dirac_constraint_on_the_tensor_pair():
    result = derive_tensor_localization_gate()

    assert result["retarded"]["same_jet_different_history"] is True
    assert result["retarded"]["is_dirac_constraint"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
