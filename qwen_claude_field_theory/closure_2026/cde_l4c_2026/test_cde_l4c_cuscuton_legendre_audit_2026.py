#!/usr/bin/env python3
"""Tests for the CDE-L4C cuscuton Legendre-map audit."""

import sympy as sp

from cde_l4c_cuscuton_legendre_audit_2026 import derive_cuscuton_audit, main


def test_correct_adm_lapse_factor_changes_the_reported_momentum_normalization():
    result = derive_cuscuton_audit()
    adm = result["adm"]

    assert adm["covariant_density_residual"] == 0
    assert adm["momentum_limit"] == adm["sqrt_gamma"] * adm["M2"]
    assert adm["old_script_momentum_limit"] == adm["M2"] / adm["N"]
    assert adm["normalization_mismatch"] != 0
    assert adm["momentum_near_null_limit"].is_infinite
    assert adm["momentum_is_globally_bounded"] is False


def test_inhomogeneous_cuscuton_legendre_map_is_invertible():
    result = derive_cuscuton_audit()
    legendre = result["k!=0"]

    assert legendre["velocity_hessian"] != 0
    assert legendre["velocity_hessian_is_negative"] is True
    assert legendre["primary_constraint_exists_from_cuscuton_alone"] is False
    assert legendre["inverse_velocity_residual"] == 0
    assert legendre["hamiltonian_residual"] == 0
    assert legendre["hamiltonian"].has(legendre["shift"])
    assert legendre["hamiltonian"].has(legendre["potential"])


def test_homogeneous_branch_is_degenerate_and_rank_changes():
    result = derive_cuscuton_audit()
    zero = result["k=0"]

    assert zero["velocity_hessian"] == 0
    assert zero["primary_constraint"] != 0
    assert zero["primary_constraint_residual"] == 0
    assert result["branch_rank_change"] is True


def test_algebraic_a0_coupling_preserves_hessian_but_does_not_create_constraint():
    result = derive_cuscuton_audit()
    coupling = result["a0_coupling"]

    assert coupling["velocity_hessian_shift"] == 0
    assert coupling["inhomogeneous_hessian_after_coupling"] != 0
    assert coupling["nonpropagation_certified"] is False


def test_existing_four_constraint_certificate_omits_the_cuscuton_pair():
    result = derive_cuscuton_audit()
    certificate = result["certificate_audit"]

    assert certificate["declared_phase_space_pairs"] == 4
    assert certificate["contains_chi"] is False
    assert certificate["contains_p_chi"] is False
    assert certificate["full_action_dof_certified"] is False
    assert certificate["name_presence_is_only_a_necessary_test"] is True


def test_existing_rank_subsystem_has_an_unreported_cancellation_surface():
    result = derive_cuscuton_audit()
    rank = result["certificate_rank_surface"]

    assert rank["determinant"] == (
        rank["c_s"] ** 2
        * rank["k"] ** 4
        * (2 * rank["B_p"] + rank["L_parallel"] * rank["a0_squared"]) ** 2
    )
    assert rank["generic_rank"] == 4
    assert rank["cancellation_rank"] == 2
    assert rank["cancellation_substitution"] == {
        rank["B_p"]: -rank["L_parallel"] * rank["a0_squared"] / 2
    }
    assert rank["momentum_constraint_brackets"] != [0, 0, 0, 0]
    assert rank["momentum_first_class_certified"] is False
    assert rank["mond_constraint_provenance"] == (
        "assigned principal surrogate, not derived from one frozen nonlinear action"
    )


def test_report_runs_the_corrected_full_adm_and_rank_surface_checks():
    assert main() == 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
