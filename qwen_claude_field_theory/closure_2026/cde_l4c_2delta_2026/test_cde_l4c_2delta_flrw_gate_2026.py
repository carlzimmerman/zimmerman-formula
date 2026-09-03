#!/usr/bin/env python3
"""Regression tests for the on-shell FLRW/principal-symbol follow-on gate."""

import sympy as sp

from cde_l4c_2delta_flrw_gate_2026 import derive_flrw_gate, main


def test_homogeneous_multiplier_equations_are_identities_and_do_not_fix_zero_modes():
    result = derive_flrw_gate()
    background = result["background"]

    assert background["a_squared"] == 0
    assert background["R3"] == 0
    assert background["D2_C_slip"] == 0
    assert background["D2_K"] == 0
    assert background["E_lambda_s"] == 0
    assert background["E_lambda_K"] == 0
    assert background["multiplier_coefficient_matrix"].rank() == 0
    assert background["homogeneous_multipliers_fixed"] is False


def test_cuscuton_and_friedmann_equations_are_varied_from_minisuperspace():
    result = derive_flrw_gate()
    mini = result["minisuperspace"]

    assert mini["E_T"] == sp.simplify(
        sp.diff(mini["L"], mini["T"])
        - sp.diff(sp.diff(mini["L"], mini["T_dot"]), mini["t"])
    )
    assert mini["E_N"] == sp.diff(mini["L"], mini["N"])
    assert mini["friedmann_residual"] == 0
    assert mini["cuscuton_residual"] == 0
    assert mini["raychaudhuri_residual"] == 0
    assert mini["nonzero_H_allowed"] is True


def test_expanding_flrw_witness_solves_all_three_background_equations():
    result = derive_flrw_gate()
    witness = result["minisuperspace"]["vacuum_expanding_witness"]

    assert witness["parameter_solution"]
    assert all(residual == 0 for residual in witness["equation_residuals"])
    assert witness["H_witness"] != 0
    assert sp.simplify(
        sp.diff(witness["scale_factor"], witness["t"])
        / witness["scale_factor"]
        - witness["H_witness"]
    ) == 0


def test_flrw_principal_family_reduces_to_the_zero_background_block():
    result = derive_flrw_gate()
    principal = result["principal"]

    reduced = sp.simplify(
        principal["lagrangian"].subs(
            {
                principal["H"]: 0,
                principal["lambda_s_bar"]: 0,
                principal["lambda_K_bar"]: 0,
            }
        )
        - principal["zero_background_lagrangian"]
    )
    assert reduced == 0
    assert principal["background_shift_identity_s"] == 0
    assert principal["background_shift_identity_K"] == 0
    assert principal["minkowski_adm_source_residual"] == 0


def test_dirac_classification_is_recomputed_and_background_independent():
    result = derive_flrw_gate()
    principal = result["principal"]
    matrix = principal["poisson_matrix"]

    assert matrix + matrix.T == sp.zeros(matrix.rows)
    assert principal["poisson_determinant"] == sp.factor(matrix.det())
    assert principal["poisson_rank"] == matrix.rank()
    assert principal["constraint_jacobian_rank"] == principal[
        "constraint_jacobian"
    ].rank()
    assert all(
        sp.diff(principal["poisson_determinant"], parameter) == 0
        for parameter in (
            principal["H"],
            principal["lambda_s_bar"],
            principal["lambda_K_bar"],
        )
    )
    independently_counted = sp.Rational(
        principal["phase_dimension"]
        - 2 * principal["first_class_count"]
        - principal["second_class_count"],
        2,
    )
    assert principal["configuration_dof"] == independently_counted


def test_constraint_solution_and_reduced_symplectic_structure_are_derived():
    result = derive_flrw_gate()
    principal = result["principal"]

    assert all(
        sp.simplify(constraint.subs(principal["constraint_solution"])) == 0
        for constraint in principal["constraints"]
    )
    assert principal["canonical_one_form_pullback"] != 0
    assert principal["reduced_hamiltonian"] == sp.simplify(
        principal["canonical_hamiltonian"].subs(
            principal["constraint_solution"]
        )
    )
    assert not principal["tertiary_constraints_found"]


def test_k_zero_and_lower_derivative_scope_are_not_overclaimed():
    result = derive_flrw_gate()
    principal = result["principal"]

    assert principal["k_zero_poisson_rank"] == principal[
        "poisson_matrix"
    ].subs(principal["q"], 0).rank()
    assert principal["k_zero_poisson_rank"] != principal["poisson_rank"]
    homogeneous = principal["homogeneous_restart"]
    assert homogeneous["lapse_secondary"] != 0
    assert homogeneous["lapse_secondary"].has(principal["H"])
    assert principal["finite_k_matrix_substitution_is_homogeneous_chain"] is False
    assert result["scope"]["highest_spatial_derivative_flrw_family_derived"] is False
    assert result["scope"]["geometry_motivated_principal_family"] is True
    assert result["scope"]["full_finite_k_flrw_action_derived"] is False
    assert result["scope"]["cuscuton_lower_derivative_terms_in_principal_rank"] is False
    assert result["scope"]["global_nonlinear_dof_theorem"] is False
    assert result["verdict"] == "CONDITIONAL_OBSTRUCTION_ON_FLRW_PRINCIPAL_FAMILY"


def test_executable_report_returns_success_for_its_scoped_checks():
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
