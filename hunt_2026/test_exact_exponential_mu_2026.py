#!/usr/bin/env python3
"""Regression tests for the exact inverse of mu(y)=1-exp(-y)."""

import math

import numpy as np

from exact_exponential_mu_2026 import (
    PREDICTIONS,
    deep_inverse_coefficients,
    derive_prediction_identities,
    exact_inverse_y,
    exact_nu,
    flux_x,
    lambda_parallel,
    lambda_perpendicular,
    logarithmic_mu_slope,
    main,
    route_a_nu,
)


def test_exact_inverse_closes_the_implicit_law_over_many_decades():
    xs = np.logspace(-14, 8, 91)
    ys = exact_inverse_y(xs)
    residual = np.abs(np.array([flux_x(y) for y in ys]) - xs)
    scale = np.maximum(xs, 1e-300)
    assert np.max(residual / scale) < 2e-11
    assert exact_inverse_y(0.0) == 0.0


def test_exact_nu_is_not_the_route_a_shortcut():
    xs = np.array([0.01, 0.1, 1.0, 10.0])
    bias = route_a_nu(xs) / exact_nu(xs) - 1.0
    assert np.max(np.abs(bias)) > 0.1
    assert np.all(bias > 0.0)


def test_constitutive_eigenvalues_are_positive_away_from_zero():
    ys = np.logspace(-12, 5, 101)
    assert np.all(lambda_perpendicular(ys) > 0.0)
    assert np.all(lambda_parallel(ys) > 0.0)
    assert lambda_perpendicular(0.0) == 0.0
    assert lambda_parallel(0.0) == 0.0


def test_logarithmic_slope_is_stable_at_zero_and_extreme_newtonian_field():
    with np.errstate(over="raise", invalid="raise"):
        values = logarithmic_mu_slope(np.array([0.0, 1e-12, 1.0, 1e5]))
    assert values[0] == 1.0
    assert np.all(np.isfinite(values))
    assert values[-1] == 0.0


def test_kernel_functions_reject_unphysical_negative_arguments():
    for function in (flux_x, lambda_perpendicular, lambda_parallel, route_a_nu):
        try:
            function(-1.0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{function.__name__} accepted a negative acceleration")


def test_deep_inverse_series_coefficients_are_derived():
    coeffs = deep_inverse_coefficients()
    assert coeffs == (1, 1 / 4, 7 / 96)


def test_deep_and_newtonian_numeric_limits():
    x_deep = 1e-10
    y_deep = exact_inverse_y(x_deep)
    y_series = math.sqrt(x_deep) + x_deep / 4 + 7 * x_deep ** 1.5 / 96
    assert abs(y_deep / y_series - 1.0) < 1e-9

    x_newton = 20.0
    y_newton = exact_inverse_y(x_newton)
    leading_tail = x_newton * math.exp(-x_newton)
    assert abs((y_newton - x_newton) / leading_tail - 1.0) < 1e-5


def test_prediction_ledger_has_distinct_observable_rails():
    assert len(PREDICTIONS) == 12
    keys = [entry.observable_key for entry in PREDICTIONS]
    assert len(keys) == len(set(keys))
    assert all(entry.scope and entry.observable and entry.equation for entry in PREDICTIONS)


def test_prediction_dependencies_are_explicit_and_acyclic():
    numbers = {entry.number for entry in PREDICTIONS}
    assert numbers == set(range(1, len(PREDICTIONS) + 1))
    assert any(entry.dependencies for entry in PREDICTIONS)
    for entry in PREDICTIONS:
        assert all(dependency in numbers for dependency in entry.dependencies)
        assert all(dependency < entry.number for dependency in entry.dependencies)


def test_nonlinear_bvp_channels_do_not_claim_linear_response_as_sufficient():
    by_number = {entry.number: entry for entry in PREDICTIONS}
    assert 6 not in by_number[9].dependencies
    assert 6 not in by_number[10].dependencies
    assert "not derived from the linear-response channel" in by_number[9].scope
    assert "not derived from the linear-response channel" in by_number[10].scope


def test_bankable_prediction_identities_are_executable_not_only_strings():
    identities = derive_prediction_identities()
    assert identities["spherical_slope_residual"] == 0
    assert identities["epicycle_residual"] == 0
    assert identities["efe_green_vacuum_residual"] == 0
    assert identities["quadrupole_conversion_residual"] == 0
    assert identities["finite_deflection_limit_residual"] == 0
    assert identities["redshift_velocity_residual"] == 0


def test_predictions_are_scoped_not_mislabeled_as_full_action_results():
    assert all(entry.status in {
        "exact-kernel",
        "conditional-AQUAL",
        "conditional-no-slip",
        "conditional-physical-lapse",
    }
               for entry in PREDICTIONS)
    assert not any(entry.status == "closed-relativistic-action" for entry in PREDICTIONS)


def test_report_runs_all_computed_guards():
    assert main() == 0


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
