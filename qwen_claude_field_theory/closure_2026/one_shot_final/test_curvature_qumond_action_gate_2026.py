#!/usr/bin/env python3
"""Regression tests for the curvature-sourced QUMOND action gate."""

from curvature_qumond_action_gate_2026 import derive_curvature_qumond_gate


def test_varied_static_action_yields_exact_exponential_mond_without_direct_matter_coupling():
    result = derive_curvature_qumond_gate()

    assert result["constitutive"]["q_derivative_residual"] == 0
    assert result["static_variation"]["action_residuals"] == (0, 0, 0, 0)
    assert result["static_variation"]["mond_flux_residual"] == 0
    assert result["matter_ward"]["auxiliary_matter_variation"] == 0


def test_full_metric_and_foliation_gates_falsify_the_candidate():
    result = derive_curvature_qumond_gate()

    assert result["no_slip"]["q_tf_stress"] != 0
    assert result["no_slip"]["rnn_tf_stress_on_constant_gradient_patch"] == 0
    assert result["fixed_foliation"]["alpha2_like_coefficient"] != 0
    assert result["clock_flrw"]["velocity_hessian_det"] != 0
    assert result["clock_flrw"]["eigenvalue_product"] < 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
