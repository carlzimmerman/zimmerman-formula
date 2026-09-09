#!/usr/bin/env python3
"""Regression tests for the on-shell ALC mimetic no-go."""

from alc_mimetic_acceleration_nogo import derive_gate


def test_gradient_unit_normal_is_geodesic_by_derived_identity():
    result = derive_gate()
    assert result["covariant"]["identity_holds"]
    assert all(item == 0 for item in result["covariant"]["identity_residual"])


def test_linear_mimetic_constraint_kills_static_acceleration_source():
    result = derive_gate()["static_linear"]
    assert result["acceleration_on_constraint"] == 0
    assert result["static_constraint_solution"] == [0]
    assert result["spatial_potential_does_not_enter_constraint_at_linear_order"]


def test_alc_correction_has_no_linear_source_at_zero_acceleration():
    result = derive_gate()
    correction = result["alc_correction"]
    assert correction["H_at_zero"] == 0
    assert correction["H_prime_at_zero"] == 0
    assert result["projectable"]["spatial_acceleration"] == 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items()
             if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
