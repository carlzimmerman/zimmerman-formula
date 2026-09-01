#!/usr/bin/env python3
"""Tests for the frame-free spin-2 nonlocal MOND audit."""

from spin2_no_slip_linearity_gate_2026 import derive_spin2_gate


def test_spin2_action_derives_no_slip_without_a_scalar_pole():
    result = derive_spin2_gate()

    assert result["field_equations"]["tracefree_residual"] == 0
    assert result["field_equations"]["gamma_minus_one"] == 0
    assert result["spectrum"]["form_factor_has_zeros"] is False


def test_field_independent_kernel_fails_exact_deep_mond_source_scaling():
    result = derive_spin2_gate()

    assert result["scaling"]["linear_kernel_degree"] != result["scaling"]["mond_degree"]
    assert result["scaling"]["btfr_exponent_linear_kernel"] != result["scaling"]["btfr_exponent_mond"]


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
