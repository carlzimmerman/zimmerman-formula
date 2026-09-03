#!/usr/bin/env python3
"""Identity tests for the exact real-mode FLRW ADM geometry.

These tests intentionally recompute identities from the exact, unexpanded
objects returned by the implementation.  They do not certify a stored list
of quadratic coefficients.
"""

import sympy as sp

from cde_l4c_2delta_full_flrw_adm_2026 import (
    derive_full_flrw_adm_geometry,
    exact_real_mode_average,
    series_coefficient,
)


def _zero_matrix(matrix: sp.MatrixBase) -> bool:
    return matrix.applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def _assert_first_order_spatial_identities(geometry):
    """Check three independently written, nonzero geometric formulas."""

    epsilon = geometry["epsilon"]
    theta = geometry["theta"]
    scale = geometry["scale_factor"]
    k = geometry["k"]
    Phi = geometry["Phi"]
    Psi = geometry["Psi"]
    B = geometry["B"]
    H = geometry["H"]
    Psi_dot = geometry["Psi_dot"]

    acceleration_linear = series_coefficient(
        geometry["acceleration_covector"], epsilon, 1
    )
    D2_C_linear = series_coefficient(geometry["D2_C"], epsilon, 1)
    D2_K_linear = series_coefficient(geometry["D2_K"], epsilon, 1)

    expected_acceleration = sp.Matrix(
        [-k * Phi * sp.sin(theta), 0, 0]
    )
    expected_D2_C = (
        4 * k**4 * (Psi - Phi) * sp.cos(theta) / scale**4
    )
    expected_D2_K = (
        k**2
        * (-B * k**2 + 3 * scale**2 * (H * Phi + Psi_dot))
        * sp.cos(theta)
        / scale**4
    )

    assert not _zero_matrix(acceleration_linear)
    assert D2_C_linear != 0
    assert D2_K_linear != 0
    assert _zero_matrix(acceleration_linear - expected_acceleration)
    assert sp.simplify(D2_C_linear - expected_D2_C) == 0
    assert sp.simplify(D2_K_linear - expected_D2_K) == 0


def test_series_and_real_mode_average_are_computed_not_tabulated():
    epsilon, theta, z = sp.symbols("epsilon theta z", real=True)
    assert series_coefficient(sp.exp(epsilon * z), epsilon, 2) == z**2 / 2
    expression = z * sp.cos(theta) ** 2 + (1 - z) * sp.sin(theta) ** 2
    assert exact_real_mode_average(expression, theta) == sp.Rational(1, 2)


def test_exact_fields_freeze_the_real_mode_and_shift_convention():
    geometry = derive_full_flrw_adm_geometry()
    epsilon = geometry["epsilon"]
    theta = geometry["theta"]
    scale = geometry["scale_factor"]
    Phi = geometry["Phi"]
    Psi = geometry["Psi"]
    B = geometry["B"]
    k = geometry["k"]

    mode = sp.cos(theta)
    conformal_factor = scale**2 * sp.exp(-2 * epsilon * Psi * mode)
    assert geometry["lapse"] == 1 + epsilon * Phi * mode
    assert geometry["spatial_metric"] == conformal_factor * sp.eye(3)
    assert geometry["shift_covector"] == sp.Matrix(
        [-epsilon * k * B * sp.sin(theta), 0, 0]
    )

    # These are exact objects, present before any epsilon expansion.
    for name in (
        "spatial_inverse",
        "spatial_determinant",
        "acceleration_covector",
        "three_curvature",
        "extrinsic_curvature",
        "D2_C",
        "D2_K",
    ):
        assert name in geometry
        assert geometry[name] is not None


def test_metric_inverse_and_determinant_are_exact_identities():
    geometry = derive_full_flrw_adm_geometry()
    h = geometry["spatial_metric"]
    h_inverse = geometry["spatial_inverse"]
    scale = geometry["scale_factor"]
    s = geometry["conformal_exponent"]
    assert _zero_matrix(h * h_inverse - sp.eye(3))
    independent_determinant = scale**6 * sp.exp(-6 * s)
    assert sp.simplify(
        geometry["spatial_determinant"] - independent_determinant
    ) == 0


def test_three_curvature_matches_independent_conformal_formula():
    geometry = derive_full_flrw_adm_geometry()
    epsilon = geometry["epsilon"]
    theta = geometry["theta"]
    scale = geometry["scale_factor"]
    Psi = geometry["Psi"]
    k = geometry["k"]

    s = epsilon * Psi * sp.cos(theta)
    flat_laplacian_s = k**2 * sp.diff(s, theta, 2)
    flat_gradient_s_squared = (k * sp.diff(s, theta)) ** 2
    conformal_formula = sp.exp(2 * s) / scale**2 * (
        4 * flat_laplacian_s - 2 * flat_gradient_s_squared
    )
    assert sp.simplify(geometry["three_curvature"] - conformal_formula) == 0


def test_extrinsic_trace_agrees_with_direct_index_contraction():
    geometry = derive_full_flrw_adm_geometry()
    assert sp.simplify(
        geometry["extrinsic_trace_direct"]
        - geometry["extrinsic_trace_matrix"]
    ) == 0


def test_nonzero_first_order_spatial_operators_and_zero_mutations():
    geometry = derive_full_flrw_adm_geometry()
    _assert_first_order_spatial_identities(geometry)

    mutations = {
        "acceleration_covector": sp.zeros(3, 1),
        "D2_C": sp.Integer(0),
        "D2_K": sp.Integer(0),
    }
    for field, zero_value in mutations.items():
        mutated = dict(geometry)
        mutated[field] = zero_value
        mutation_failed = False
        try:
            _assert_first_order_spatial_identities(mutated)
        except AssertionError:
            mutation_failed = True
        assert mutation_failed, f"zeroing {field} escaped the identity gate"


def test_k_zero_perturbation_sector_kills_every_spatial_operator():
    geometry = derive_full_flrw_adm_geometry()
    zero_mode = {geometry["k"]: 0}

    # This is not epsilon=0: lapse and spatial-metric perturbations remain.
    assert geometry["lapse"].subs(zero_mode) != 1
    assert geometry["spatial_metric"].subs(zero_mode) != (
        geometry["scale_factor"] ** 2 * sp.eye(3)
    )
    assert sp.simplify(geometry["three_curvature"].subs(zero_mode)) == 0
    assert _zero_matrix(geometry["acceleration_covector"].subs(zero_mode))
    assert sp.simplify(geometry["D2_C"].subs(zero_mode)) == 0
    assert sp.simplify(geometry["D2_K"].subs(zero_mode)) == 0


def test_unperturbed_flrw_limit_retains_K_equal_three_H():
    geometry = derive_full_flrw_adm_geometry()
    unperturbed = {geometry["epsilon"]: 0}
    assert sp.simplify(geometry["three_curvature"].subs(unperturbed)) == 0
    assert _zero_matrix(geometry["acceleration_covector"].subs(unperturbed))
    assert sp.simplify(geometry["D2_C"].subs(unperturbed)) == 0
    assert sp.simplify(geometry["D2_K"].subs(unperturbed)) == 0
    assert sp.simplify(
        geometry["extrinsic_trace_direct"].subs(unperturbed)
        - 3 * geometry["H"]
    ) == 0


def test_callers_cannot_poison_cached_exact_geometry_by_mutation():
    first = derive_full_flrw_adm_geometry()
    original_D2_C = first["D2_C"]
    first["D2_C"] = sp.Integer(0)
    first["acceleration_covector"][0] = 0

    fresh = derive_full_flrw_adm_geometry()
    assert fresh["D2_C"] != 0
    assert sp.simplify(fresh["D2_C"] - original_D2_C) == 0
    _assert_first_order_spatial_identities(fresh)


def test_shift_sign_mutation_flips_the_derived_B_Psidot_mixing():
    baseline = derive_full_flrw_adm_geometry(shift_sign=-1)
    mutated = derive_full_flrw_adm_geometry(shift_sign=1)

    def mixed_coefficient(geometry):
        quadratic_density = series_coefficient(
            geometry["eh_kinetic_density"], geometry["epsilon"], 2
        )
        averaged_density = exact_real_mode_average(
            quadratic_density, geometry["theta"]
        )
        return sp.simplify(
            sp.diff(
                averaged_density,
                geometry["B"],
                geometry["Psi_dot"],
            )
        )

    baseline_coefficient = mixed_coefficient(baseline)
    mutated_coefficient = mixed_coefficient(mutated)
    assert baseline_coefficient != 0
    assert mutated_coefficient != baseline_coefficient
    assert sp.simplify(mutated_coefficient + baseline_coefficient) == 0


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
