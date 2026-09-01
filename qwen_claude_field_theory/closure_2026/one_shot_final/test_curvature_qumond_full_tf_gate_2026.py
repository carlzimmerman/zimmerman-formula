#!/usr/bin/env python3
"""Regression tests for the complete static trace-free metric gate."""

import sympy as sp

from curvature_qumond_full_tf_gate_2026 import derive_full_tf_gate


def test_exact_static_tf_equation_keeps_every_same_order_term():
    result = derive_full_tf_gate()
    s = result["symbols"]

    expected_exact = (
        s["N"] * (-sp.diff(s["zeta"], s["x"], 2) + sp.diff(s["zeta"], s["x"]) ** 2)
        - sp.diff(s["N"], s["x"], 2)
        + 2 * sp.diff(s["zeta"], s["x"]) * sp.diff(s["N"], s["x"])
        + 2 * s["N"] * sp.diff(s["lambda"], s["x"]) * sp.diff(s["chi"], s["x"])
        + 2 * s["lambda"] * sp.diff(s["N"], s["x"]) * sp.diff(s["chi"], s["x"])
        - 2 * sp.diff(s["lambda"], s["x"]) * sp.diff(s["N"], s["x"])
        + s["N"] * sp.exp(-s["y"]) * sp.diff(s["chi"], s["x"]) ** 2
    )
    assert sp.simplify(result["exact"]["radial_minus_transverse"] - expected_exact) == 0

    expected_linear = sp.diff(s["psi"] - s["phi"], s["x"], 2)
    assert sp.simplify(result["weak_expansion"]["E1"] - expected_linear) == 0

    expected_quadratic = (
        sp.diff(s["p2"] - s["n2"], s["x"], 2)
        + s["phi"] * sp.diff(s["psi"], s["x"], 2)
        + sp.diff(s["psi"], s["x"]) ** 2
        - 2 * sp.diff(s["psi"], s["x"]) * sp.diff(s["phi"], s["x"])
        + 2 * sp.diff(s["ell"], s["x"]) * sp.diff(s["c"] - s["phi"], s["x"])
        + sp.exp(-sp.diff(s["c"], s["x"]) / s["abar"]) * sp.diff(s["c"], s["x"]) ** 2
    )
    assert sp.simplify(result["weak_expansion"]["E2"] - expected_quadratic) == 0


def test_linear_gamma_is_one_while_quadratic_slip_is_a_separate_source():
    result = derive_full_tf_gate()
    s = result["symbols"]
    u = s["u"]
    mu = 1 - sp.exp(-sp.diff(u, s["x"]) / s["abar"])

    expected_shell = (
        sp.diff(s["p2"] - s["n2"], s["x"], 2)
        + u * sp.diff(u, s["x"], 2)
        - mu * sp.diff(u, s["x"]) ** 2
    )
    assert sp.simplify(result["weak_expansion"]["E2_on_leading_shell"] - expected_shell) == 0
    assert result["linear_gate"]["gamma"] == 1
    assert result["linear_gate"]["auxiliary_tf_order"] == 2

    expected_log_equal = -(1 + mu) * sp.diff(u, s["x"]) ** 2
    assert sp.simplify(result["second_order"]["equal_log_potential_residual"] - expected_log_equal) == 0
    assert result["second_order"]["nonlinear_no_slip_certified"] is False
    assert result["verdict"]["fatal_no_slip_obstruction"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
