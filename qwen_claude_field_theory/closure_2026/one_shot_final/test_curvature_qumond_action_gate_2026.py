#!/usr/bin/env python3
"""Regression tests for the curvature-sourced QUMOND action gate."""

from curvature_qumond_action_gate_2026 import derive_curvature_qumond_gate


def test_varied_static_reduction_yields_exact_exponential_mond():
    result = derive_curvature_qumond_gate()

    assert result["constitutive"]["q_derivative_residual"] == 0
    assert result["static_variation"]["action_residuals"] == (0, 0, 0, 0)
    assert result["static_variation"]["mond_flux_residual"] == 0


def test_auxiliary_tf_and_foliation_diagnostics_are_generated_without_overclaim():
    result = derive_curvature_qumond_gate()
    diagnostic = result["auxiliary_tf_diagnostic"]

    # This is only the auxiliary algebraic constant-gradient contribution.
    # It must not be labelled a complete second-order no-slip equation because
    # the same-order nonlinear Einstein and metric-potential terms are absent.
    assert diagnostic["elliptic_curvature_tf_on_shell"] == 0
    assert diagnostic["auxiliary_tf_stress_on_shell"] == diagnostic["q_tf_stress"]
    assert diagnostic["auxiliary_tf_stress_on_shell"] != 0
    assert diagnostic["full_second_order_metric_equation_included"] is False
    assert diagnostic["no_slip_verdict"] == "UNRESOLVED"
    assert result["fixed_foliation"]["alpha2_like_coefficient"] != 0
    assert result["clock_flrw"]["velocity_hessian_det"] != 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
