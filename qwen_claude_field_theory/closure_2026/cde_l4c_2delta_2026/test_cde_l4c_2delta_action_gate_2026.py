#!/usr/bin/env python3
"""Tests for the frozen CDE-L4C-2Delta action and its first kill gates."""

import sympy as sp

from cde_l4c_2delta_action_gate_2026 import derive_action_gate, main


def test_exponential_term_is_the_correction_not_a_double_counted_primitive():
    result = derive_action_gate()
    kernel = result["kernel"]
    assert kernel["modulus_residual"] == 0
    assert kernel["deep_quadratic_coefficient"] == 0
    assert kernel["deep_cubic_coefficient"] == sp.Rational(2, 3)


def test_multiplier_equations_are_euler_lagrange_equations_of_frozen_action():
    result = derive_action_gate()
    equations = result["multiplier_variation"]
    assert equations["E_lambda_s"] == equations["laplacian_C_slip"]
    assert equations["E_lambda_K"] == equations["laplacian_K"]
    assert equations["inserted_phenomenologically"] is False


def test_reduced_static_action_derives_phi_and_psi_separately():
    result = derive_action_gate()
    weak = result["weak_static"]
    assert weak["E_Phi"] != weak["E_Psi"]
    assert weak["E_lambda"] != 0
    assert weak["finite_k_solution"][weak["Psi"]] == weak["Phi"]
    assert weak["finite_k_solution"][weak["lambda_s"]] == 0
    assert weak["mond_residual"] == 0
    assert weak["gamma_PPN_linear"] == 1


def test_zero_mode_is_not_mistaken_for_the_finite_k_constraint():
    result = derive_action_gate()
    sectors = result["sector_split"]
    assert sectors["k_nonzero_rank"] > sectors["k_zero_rank"]
    assert sectors["k_zero_rank"] == 0
    assert sectors["flrw_H_forced_zero"] is False


def test_minimal_matter_has_a_separate_ward_identity_and_mutation_fails_it():
    result = derive_action_gate()
    ward = result["matter_ward"]
    assert ward["aux_matter_euler_derivative"] == 0
    assert ward["ordinary_divergence_on_shell"] == 0
    assert ward["direct_source_mutation_divergence"] != 0


def test_unitary_adm_velocity_hessian_does_not_supply_a_full_dof_count():
    result = derive_action_gate()
    canonical = result["unitary_adm"]
    assert canonical["mond_hessian_shift"] == sp.zeros(2)
    assert canonical["multiplier_hessian_shift"] == sp.zeros(2)
    assert canonical["metric_velocity_hessian_rank"] == 1
    assert canonical["covariant_clock_pair_included"] is False
    assert canonical["full_action_dof_certified"] is False


def test_minkowski_principal_block_is_generated_from_adm_geometry():
    result = derive_action_gate()
    adm = result["adm_principal_derivation"]
    zero = result["zero_field_dirac"]
    nonzero = result["nonzero_field_dirac"]

    # Compare independently constructed ADM pieces to the Lagrangians fed to
    # the Dirac algorithm. No expected coefficient, rank, or determinant is
    # supplied by this test.
    assert adm["zero_field_residual"] == 0
    assert adm["positive_gradient_residual"] == 0
    assert adm["generated_zero_field_lagrangian"] == zero["lagrangian"]
    assert adm["generated_positive_gradient_lagrangian"] == nonzero["lagrangian"]
    assert adm["cuscuton_principal_contribution"] == 0
    assert adm["potential_principal_contribution"] == 0
    assert adm["full_lower_derivative_action_included"] is False


def test_homogeneous_tensor_principal_block_is_einstein_but_not_a_global_claim():
    result = derive_action_gate()
    tensor = result["tensor"]
    assert tensor["homogeneous_multiplier_contribution"] == 0
    assert tensor["c_T_squared_on_homogeneous_branch"] == 1
    assert tensor["anisotropic_or_inhomogeneous_background_tested"] is False


def test_zero_field_dirac_result_is_derived_from_the_actual_brackets():
    result = derive_action_gate()
    zero = result["zero_field_dirac"]

    # These identities deliberately do not encode an expected determinant,
    # rank, or degree count.  They force the report to expose the matrices
    # from which its classification is recomputed.
    assert zero["poisson_matrix"] + zero["poisson_matrix"].T == sp.zeros(
        len(zero["constraints"])
    )
    assert zero["poisson_rank"] == zero["poisson_matrix"].rank()
    assert zero["poisson_determinant"] == sp.factor(
        zero["poisson_matrix"].det()
    )
    assert zero["constraint_jacobian_rank"] == zero["constraint_jacobian"].rank()
    assert zero["first_class_count"] + zero["second_class_count"] == len(
        zero["constraints"]
    )
    independently_counted_dof = sp.Rational(
        zero["phase_dimension"]
        - 2 * zero["first_class_count"]
        - zero["second_class_count"],
        2,
    )
    assert zero["configuration_dof"] == independently_counted_dof
    assert zero["reduced_hamiltonian"] == sp.simplify(
        zero["canonical_hamiltonian"].subs(zero["constraint_solution"])
    )
    assert zero["quadratic_spatial_stiffness"] == 0
    assert zero["leading_spatial_order"] > 2


def test_k_zero_and_finite_k_dirac_sectors_are_not_conflated():
    result = derive_action_gate()
    finite = result["zero_field_dirac"]
    homogeneous = result["homogeneous_dirac_symbol"]
    assert homogeneous["poisson_matrix"] == finite["poisson_matrix"].subs(
        finite["k"], 0
    )
    assert homogeneous["poisson_rank"] == homogeneous["poisson_matrix"].rank()
    assert homogeneous["poisson_rank"] != finite["poisson_rank"]


def test_nonzero_field_scalar_dispersion_is_derived_and_has_zero_field_limit():
    result = derive_action_gate()
    finite = result["nonzero_field_dirac"]
    zero = result["zero_field_dirac"]
    matrix = finite["poisson_matrix"]

    assert (matrix + matrix.T).applyfunc(sp.simplify) == sp.zeros(
        len(finite["constraints"])
    )
    assert finite["poisson_rank"] == matrix.rank()
    assert finite["poisson_determinant"] == sp.factor(matrix.det())
    assert finite["configuration_dof"] == sp.Rational(
        finite["phase_dimension"]
        - 2 * finite["first_class_count"]
        - finite["second_class_count"],
        2,
    )
    assert finite["omega_squared"] == sp.simplify(
        sp.diff(finite["reduced_hamiltonian"], finite["p_Psi"], 2)
        * sp.diff(finite["reduced_hamiltonian"], finite["Psi"], 2)
    )
    assert finite["omega_squared"].is_positive
    assert finite["exact_omega_squared"] == sp.simplify(
        finite["omega_squared"].subs(
            finite["lambda_parallel"], finite["exact_lambda_parallel"]
        )
    )
    exact_y = next(iter(finite["exact_lambda_parallel"].free_symbols))
    assert sp.limit(finite["exact_omega_squared"], exact_y, 0, dir="+") == 0
    assert sp.simplify(
        finite["reduced_hamiltonian"].subs(finite["lambda_parallel"], 0)
        - zero["reduced_hamiltonian"]
    ) == 0


def test_candidate_status_stays_open_until_complete_dirac_closure():
    result = derive_action_gate()
    assert result["verdict"] == "OPEN"
    assert "on-shell FLRW" in result["next_unavoidable_calculation"]
    assert "zero" in result["next_unavoidable_calculation"]
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
