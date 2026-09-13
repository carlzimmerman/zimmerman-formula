#!/usr/bin/env python3
"""Regression checks for Door 04's derived curvature-action fork."""

import sympy as sp

from metric_curvature_gate import derive


def test_static_variation_and_exact_no_slip_fork():
    out = derive()
    static = out["static"]
    assert all(item == 0 for item in static["equation_residuals"])
    assert static["no_slip_solution_for_a"] == [0]
    assert sp.factor(static["gamma_minus_one"]) != 0


def test_source_homogeneity_and_spectrum_are_derived():
    out = derive()
    assert out["scaling"]["linear_source_ratio"] == sp.Symbol("scale", positive=True)
    assert out["scaling"]["linear_degree"] != out["scaling"]["deep_mond_degree"]
    assert out["spectrum"]["scalar_pole"]
    assert out["spectrum"]["tt_poles"] == [0, -sp.Symbol("F", positive=True, nonzero=True) / sp.Symbol("b", real=True)]
    assert out["spectrum"]["tt_massless_residue"] * out["spectrum"]["tt_massive_residue"] < 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
