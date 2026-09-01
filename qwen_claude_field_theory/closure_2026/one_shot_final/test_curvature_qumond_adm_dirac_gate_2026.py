#!/usr/bin/env python3
"""Regression tests for the full ADM gate of curvature-sourced QUMOND."""

import sympy as sp

from curvature_qumond_adm_dirac_gate_2026 import derive_adm_dirac_gate


def test_velocity_hessian_is_derived_and_has_no_lambda_primary_constraint():
    result = derive_adm_dirac_gate()
    kinetic = result["kinetic"]

    assert kinetic["hessian"] == sp.hessian(
        kinetic["lagrangian"], kinetic["velocity_vector"]
    )
    assert kinetic["determinant"] != 0
    assert kinetic["rank"] == len(kinetic["velocity_vector"])
    assert kinetic["nullity"] == 0
    assert all(residual == 0 for residual in kinetic["momentum_inverse_residuals"])
    assert kinetic["negative_eigenvalues_for_A_positive"] == 1


def test_nonzero_k_auxiliary_poisson_matrix_and_dof_are_computed():
    result = derive_adm_dirac_gate()
    sector = result["k_nonzero"]

    # The raw chi equation differentiates the Q flux
    # (1-mu) grad(chi)=exp(-y) grad(chi).  The positive MOND tensor belongs
    # only to the effective equation after eliminating lambda and the metric.
    assert sector["raw_chi_transverse"] == sp.exp(-sector["y"])
    assert sector["raw_chi_parallel"] == (1 - sector["y"]) * sp.exp(-sector["y"])
    assert sp.simplify(
        sector["pb_matrix"].det() - sector["constitutive_symbol"] ** 2
    ) == 0
    assert sector["pb_rank"] == sector["pb_matrix"].rank()
    assert sector["pb_rank"] == len(sector["constraints"])
    assert sp.simplify(sp.exp(sector["y"]) * sector["effective_mu"]) == sp.exp(sector["y"]) - 1
    assert sp.simplify(
        sp.exp(sector["y"]) * sector["effective_lambda_parallel"]
    ) == sector["y"] + sp.exp(sector["y"]) - 1
    assert sector["rank_loss_kperp_squared"] == (sector["y"] - 1) * sector["k_parallel"] ** 2
    assert sector["y_one_pure_longitudinal_residual"] == 0
    assert sector["supercritical_cone_residual"] == 0
    assert "not computed" in sector["stabilization_scope"]


def test_luminal_minkowski_scalar_dirac_chain_leaves_one_propagating_pole():
    result = derive_adm_dirac_gate()
    scalar = result["minkowski_scalar"]

    k = sp.symbols("k", positive=True, real=True)
    zeta, ell, chi, alpha, beta = sp.symbols(
        "zeta ell chi alpha beta", real=True
    )
    zeta_dot, ell_dot = sp.symbols("zeta_dot ell_dot", real=True)
    p_zeta, p_ell, p_chi, p_alpha, p_beta = sp.symbols(
        "p_zeta p_ell p_chi p_alpha p_beta", real=True
    )
    u_chi, u_alpha, u_beta = sp.symbols(
        "u_chi u_alpha u_beta", real=True
    )
    expected_lagrangian = sp.expand(
        -6 * zeta_dot**2
        + 6 * zeta_dot * ell_dot
        - 4 * k**2 * beta * zeta_dot
        + 2 * k**2 * beta * ell_dot
        + 2 * k**2 * zeta**2
        + 4 * k**2 * alpha * zeta
        - 2 * k**2 * alpha * ell
        + 2 * k**2 * ell * chi
        + k**2 * chi**2
    )
    expected_primaries = (p_chi, p_alpha, p_beta)
    expected_secondaries = (
        2 * k**2 * (chi + ell),
        -2 * k**2 * (ell - 2 * zeta),
        k**2 * (4 * beta * k**2 + p_zeta) / 3,
    )
    expected_pb = sp.Matrix(
        [
            [0, 0, 0, -2 * k**2, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, -4 * k**4 / 3],
            [2 * k**2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4 * k**4 / 3],
            [0, 0, 4 * k**4 / 3, 0, -4 * k**4 / 3, 0],
        ]
    )
    expected_preservation = (
        k**2 * (2 * p_ell + p_zeta + 6 * u_chi) / 3,
        -k**2 * (4 * beta * k**2 + p_zeta) / 3,
        4 * k**4 * (alpha + u_beta + zeta) / 3,
    )

    assert sp.expand(scalar["lagrangian"] - expected_lagrangian) == 0
    assert scalar["lagrangian"] == sp.expand(sum(scalar["action_terms"].values()))
    assert scalar["q_quadratic_coefficient"] == sp.Rational(1, 2)
    assert scalar["action_terms"]["EH_kinetic"] == sp.expand(
        sp.trace(scalar["extrinsic_curvature"] * scalar["extrinsic_curvature"])
        - scalar["trace_extrinsic_curvature"] ** 2
    )
    assert scalar["velocity_hessian"] == sp.hessian(
        scalar["lagrangian"], scalar["all_velocities"]
    )
    assert scalar["primaries"] == expected_primaries
    assert scalar["secondaries"] == expected_secondaries
    assert scalar["constraint_pb_matrix"] == expected_pb
    assert scalar["secondary_preservation"] == expected_preservation
    closed_preservation = tuple(
        sp.simplify(
            expression.subs(
                {
                    u_chi: -(2 * p_ell + p_zeta) / 6,
                    u_beta: -alpha - zeta,
                    beta: -p_zeta / (4 * k**2),
                }
            )
        )
        for expression in scalar["secondary_preservation"]
    )
    assert closed_preservation == (0, 0, 0)
    assert scalar["velocity_rank"] == 2
    assert scalar["primary_count"] == 3
    assert scalar["secondary_count"] == 3
    assert scalar["constraint_pb_rank"] == 4
    assert scalar["first_class_count"] == 2
    assert scalar["second_class_count"] == 4
    assert scalar["physical_scalar_dof"] == 1
    assert sp.expand(scalar["reduced_lagrangian"] - (6 * scalar["zeta_dot"] ** 2 - 2 * scalar["k"] ** 2 * scalar["zeta"] ** 2)) == 0
    assert scalar["sound_speed_squared"] == sp.Rational(1, 3)
    restored = scalar["spatial_gauge_restored"]
    E_dot, p_E = sp.symbols("E_dot p_E", real=True)
    expected_restored_lagrangian = sp.expand(
        expected_lagrangian
        + 4 * k**2 * zeta_dot * E_dot
        - 2 * k**2 * E_dot * ell_dot
    )
    expected_restored_secondaries = (
        2 * k**2 * (chi + ell),
        -2 * k**2 * (ell - 2 * zeta),
        -p_E,
    )
    expected_restored_pb = sp.Matrix(
        [
            [0, 0, 0, -2 * k**2, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [2 * k**2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
    )
    expected_restored_preservation = (
        k**2 * (2 * p_ell + p_zeta + 6 * u_chi) / 3,
        p_E,
        sp.Integer(0),
    )
    assert sp.expand(restored["lagrangian"] - expected_restored_lagrangian) == 0
    assert restored["velocity_hessian"] == sp.hessian(
        restored["lagrangian"], restored["velocities"]
    )
    assert restored["primaries"] == expected_primaries
    assert restored["secondaries"] == expected_restored_secondaries
    assert restored["constraint_pb_matrix"] == expected_restored_pb
    assert restored["secondary_preservation"] == expected_restored_preservation
    restored_closed_preservation = tuple(
        sp.simplify(
            expression.subs(
                {
                    u_chi: -(2 * p_ell + p_zeta) / 6,
                    p_E: 0,
                }
            )
        )
        for expression in restored["secondary_preservation"]
    )
    assert restored_closed_preservation == (0, 0, 0)
    assert restored["constraint_pb_rank"] == 2
    assert restored["first_class_count"] == 4
    assert restored["second_class_count"] == 2
    assert restored["physical_scalar_dof"] == 1
    assert restored["reduced_lagrangian"] == scalar["reduced_lagrangian"]


def test_k_zero_rejects_de_sitter_and_y_zero_degeneracy_is_in_effective_mond_operator():
    result = derive_adm_dirac_gate()
    homogeneous = result["k_zero_flrw"]
    zero_field = result["y_zero"]

    assert homogeneous["lambda_constraint"] == 3 * homogeneous["a_ddot"] / homogeneous["a"]
    assert homogeneous["de_sitter_residual"] != 0
    assert homogeneous["coasting_condition"] == 0
    assert homogeneous["coasting_constraint_residual"] == 0
    assert homogeneous["coasting_H"] != 0
    assert "accelerating_flrw_allowed" not in homogeneous
    assert "coasting_expansion_allowed" not in homogeneous
    assert zero_field["raw_auxiliary_pb_rank"] == 2
    assert zero_field["effective_mond_symbol"] == 0
    assert zero_field["generic_effective_mond_symbol_matrix"].rank() == zero_field[
        "generic_effective_mond_rank"
    ]
    assert zero_field["zero_effective_mond_symbol_matrix"].rank() == zero_field[
        "zero_effective_mond_rank"
    ]
    assert zero_field["effective_mond_rank_loss"] == (
        zero_field["generic_effective_mond_rank"]
        - zero_field["zero_effective_mond_rank"]
    )
    assert zero_field["effective_mond_rank_loss"] > 0


def test_matter_ward_statement_is_labeled_analytic_not_computed_by_this_gate():
    result = derive_adm_dirac_gate()

    assert "matter_ward" not in result
    assert result["matter_ward_scope"]["computed_by_this_gate"] is False


def test_tensor_speed_and_exact_static_kernel_are_not_assumed():
    result = derive_adm_dirac_gate()
    tensor = result["tensor"]
    vector = result["vector"]
    static = result["static"]

    assert sp.simplify(tensor["c_T_squared"] - 1) != 0
    assert sp.solve(sp.Eq(tensor["c_T_squared"], 1), tensor["lambda_background"]) == [0]
    assert vector["constraint_pb_matrix"] == sp.zeros(2)
    assert vector["secondary_preservation"] == 0
    assert vector["first_class_count_per_polarization"] == 2
    assert vector["physical_dof_per_polarization"] == 0
    assert static["mu_residual"] == 0
    assert static["preferred_primitive_residual"] == 0
    assert static["newtonian_limit"] == 1
    assert static["deep_mond_limit"] == 1
    assert static["spherical_deep_flux_ratio"] == 1
    assert static["btfr_solution"] == static["G"] * static["a0"] * static["M_b"]


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
