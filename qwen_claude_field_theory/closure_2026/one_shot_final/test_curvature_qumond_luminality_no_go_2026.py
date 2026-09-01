#!/usr/bin/env python3
"""Regression tests for the curvature-QUMOND MOND/luminality obstruction."""

import sympy as sp

from curvature_qumond_luminality_no_go_2026 import derive_luminality_no_go


def test_exact_constitutive_law_derives_nonconstant_multiplier():
    result = derive_luminality_no_go()
    static = result["static_spherical_branch"]

    assert result["constitutive"]["exact_law_residual"] == 0
    assert static["chi_euler_residual"] == 0
    assert static["regular_flux_constant"] == 0
    assert static["lambda_radial_derivative"].is_negative
    assert static["lambda_radial_derivative_nonzero"] is True


def test_exact_tensor_luminality_contradicts_the_mond_branch():
    result = derive_luminality_no_go()
    tensor = result["tensor_principal_part"]
    obstruction = result["obstruction"]

    assert tensor["kinetic_coefficient"] == 1 - 2 * tensor["lambda"]
    assert tensor["gradient_coefficient"] == 1
    assert tensor["luminal_lambda_solutions"] == [0]
    assert obstruction["luminality_implied_lambda_derivative"] == 0
    assert obstruction["derivative_contradiction"].is_negative
    assert obstruction["contradiction_nonzero"] is True


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
