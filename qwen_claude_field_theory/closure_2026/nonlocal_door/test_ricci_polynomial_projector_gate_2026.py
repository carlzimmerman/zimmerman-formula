#!/usr/bin/env python3
"""Regression tests for the Ricci-polynomial vanishing-projector gate."""

import sympy as sp

from ricci_polynomial_projector_gate_2026 import (
    derive_ricci_polynomial_projector_gate,
    main,
)


def test_isotropic_ricci_polynomial_is_rank_three_but_vanishes_at_flat_space():
    result = derive_ricci_polynomial_projector_gate()
    isotropic = result["isotropic_projector"]
    d = isotropic["d"]

    assert isotropic["trace_s_squared"] == 12 * d**2
    assert isotropic["mixed_projector"] == sp.diag(0, 8 * d**2, 8 * d**2, 8 * d**2)
    assert isotropic["scaled_idempotence_residual"] == sp.zeros(4)
    assert isotropic["rank_nonzero_curvature"] == 3
    assert isotropic["rank_zero_curvature"] == 0
    assert isotropic["flat_limit"] == sp.zeros(4)


def test_anisotropy_turns_on_a_ghost_signed_time_principal_block():
    result = derive_ricci_polynomial_projector_gate()
    anisotropic = result["anisotropic_projector"]
    s1, s2, s3 = anisotropic["spatial_eigenvalues"]
    e = anisotropic["anisotropy"]

    expected_p0 = (
        (s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2
    ) / 4
    assert sp.simplify(anisotropic["time_mixed_eigenvalue"] - expected_p0) == 0
    assert anisotropic["time_mixed_eigenvalue_is_sum_of_squares"] is True
    assert anisotropic["time_contravariant_example"] == -sp.Rational(3, 2) * e**2
    assert anisotropic["auxiliary_velocity_hessian_example"].det() == (
        -sp.Rational(9, 4) * e**4
    )
    assert anisotropic["auxiliary_velocity_hessian_rank"] == 2
    assert anisotropic["auxiliary_velocity_hessian_has_opposite_signs"] is True
    assert anisotropic["isotropic_auxiliary_velocity_hessian_rank"] == 0


def test_bianchi_i_metric_acceleration_hessian_is_nondegenerate_on_both_shears():
    result = derive_ricci_polynomial_projector_gate()
    bianchi = result["bianchi_i_highest_derivative"]

    assert bianchi["trace_s_squared_residual"] == 0
    assert bianchi["spatial_projector_trace_residual"] == 0
    assert bianchi["acceleration_hessian"] * bianchi["trace_direction"] == (
        4 * bianchi["overall_coefficient"] * bianchi["trace_direction"]
    )
    for direction in bianchi["shear_directions"]:
        assert bianchi["acceleration_hessian"] * direction == (
            sp.Rational(5, 2)
            * bianchi["overall_coefficient"]
            * direction
        )
    assert bianchi["shear_hessian_rank"] == 2


def test_ostrogradsky_shear_dirac_chain_closes_with_two_extra_modes():
    result = derive_ricci_polynomial_projector_gate()
    ostro = result["ostrogradsky_shear_dirac"]

    assert ostro["acceleration_hessian_rank"] == 2
    assert ostro["acceleration_hessian_determinant"] != 0
    assert len(ostro["primary_constraints"]) == 1
    assert len(ostro["secondary_constraints"]) == 1
    assert ostro["poisson_matrix"].rank() == 2
    assert ostro["poisson_determinant_on_constraint_surface"] != 0
    assert ostro["tertiary_constraints"] == []
    assert ostro["first_class_count"] == 0
    assert ostro["second_class_count"] == 2
    assert ostro["physical_dof"] == 4
    assert ostro["baseline_shear_dof"] == 2
    assert ostro["extra_dof"] == 2
    assert ostro["hamiltonian_linear_in_ostro_momenta"] is True


def test_multiplier_stress_and_matter_ward_trilemma_is_derived():
    result = derive_ricci_polynomial_projector_gate()
    trilemma = result["multiplier_ward_trilemma"]

    assert trilemma["bare_multiplier_lambda_solution"] == 0
    assert trilemma["bare_multiplier_on_shell_stress_coefficient"] == 0
    assert trilemma["rescued_multiplier_lambda_solution"] != 0
    assert trilemma["direct_matter_source_divergence"] != 0
    assert trilemma["metric_only_source_divergence"] == 0
    assert trilemma["bare_branch_status"] == "DEAD: no effective stress"
    assert trilemma["direct_source_rescue_status"] == (
        "DEAD under separate ordinary-matter conservation"
    )
    assert trilemma["metric_source_rescue_status"] == (
        "OPEN in general; this Ricci-polynomial candidate fails stability"
    )


def test_report_runs_to_completion():
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
