#!/usr/bin/env python3
"""Independent regressions for the intrinsic-elliptic DW falsifier."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


MODULE = Path(__file__).with_name("dw_intrinsic_elliptic_gate_2026.py")


def _load():
    spec = importlib.util.spec_from_file_location("dw_intrinsic_elliptic_gate", MODULE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_kernel_and_controlled_zero_field_limit_are_differentiated():
    module = _load()
    result = module.derive_exact_kernel()
    y = result["symbols"]["y"]

    assert sp.simplify(result["f_Z"] - sp.exp(-y) / 2) == 0
    assert sp.simplify(result["mu_eff"] - (1 - sp.exp(-y))) == 0
    assert result["ellipticity_origin"] == (0, 0)
    assert result["f_ZZ_zero_limit"] == -sp.oo
    assert result["deep_slope"] == 1
    assert result["newtonian_limit"] == 1


def test_reduced_static_branch_varies_to_mond_and_btfr():
    module = _load()
    result = module.derive_static_mond_law()
    s = result["symbols"]

    assert sp.simplify(
        result["flux"] + 4 * s["A"] * (1 - sp.exp(-s["y"])) * s["p"]
    ) == 0
    measured = result["poisson_source_coefficient"].subs(
        s["A"], 1 / (16 * sp.pi * s["G"])
    )
    assert sp.simplify(measured - 4 * sp.pi * s["G"]) == 0
    assert sp.simplify(result["btfr"] - s["G"] * s["a0"] * s["M"]) == 0


def test_clock_retaining_principal_density_and_all_euler_equations_are_varied():
    module = _load()
    action = module.derive_quadratic_action()
    euler = module.derive_euler_lagrange_equations()
    s = action["symbols"]

    expected_clock = s["n"] * (
        2 * s["ell"]
        + 2 * s["lambda_bar"] * (3 * s["z"] - s["k"] ** 2 * s["E"])
        - s["lambda_bar"] * s["n"]
    )
    assert sp.expand(action["unit_clock_sector"] - expected_clock) == 0
    assert action["delta_Z_metric"] == -8 * s["y_background"] ** 2 * s["z"]
    assert len(euler["equations"]) == 7
    assert sp.simplify(euler["equations"][s["ell"]] + 2 * s["n"]) == 0
    assert euler["covariant_xi_equation"].startswith("D_i D^i X")


def test_finite_k_legendre_map_and_constraint_generation_come_from_one_L():
    module = _load()
    result = module.derive_finite_k_dirac()
    s = result["symbols"]

    assert sp.factor(result["velocity_hessian"].det()) == -12 * s["A"] * s["k"] ** 4
    for momentum, differentiated in zip(result["momenta"], result["dL_dvelocities"]):
        assert sp.simplify(differentiated.subs(result["inverse_legendre"]) - momentum) == 0
    for velocity, recovered in result["inverse_legendre_check"].items():
        assert sp.simplify(recovered - velocity) == 0
    generated = result["primary_preservation"]
    secondaries = result["secondary_constraints"]
    assert all(
        sp.simplify(left - right) == 0
        for left, right in zip(
            secondaries,
            [generated[0], -generated[1], -generated[2], generated[3] / 2],
        )
    )
    assert result["tertiary_constraints"] == []


def test_actual_finite_k_pb_matrix_is_regularly_classified():
    module = _load()
    result = module.derive_finite_k_dirac()
    s = result["symbols"]
    constraints = result["primary_constraints"] + result["secondary_constraints"]

    assert result["constraint_jacobian_rank"] == len(constraints)
    assert result["poisson_matrix"].rank() == 6
    assert result["maximal_nonzero_minor"] == 16 * s["beta"] ** 2 * s["k"] ** 4
    assert result["first_class_count"] == 2
    assert result["second_class_count"] == 6
    assert result["physical_scalar_dof"] == 2
    assert result["preservation_after_constraints"] == [0, 0, 0, 0]


def test_shift_is_retained_and_separates_wave_from_conserved_charge():
    module = _load()
    result = module.derive_reduced_scalar()
    s = result["symbols"]
    y = s["y"]

    assert sp.simplify(
        result["shift_constraint"]
        - s["k"] ** 2 * (4 * s["A"] * s["zd"] + s["xid"])
    ) == 0
    assert result["zero_frequency_multiplicity"] == 2
    assert sp.simplify(result["exact_speed"] - (sp.exp(y) - 1) / 3) == 0
    assert result["finite_mode_no_ghost"] is True
    assert result["gradient_stable_for_positive_y"] is True
    assert result["conserved_charge_velocity"] == 0
    assert result["energy_unbounded_across_charge_sectors"] is True
    assert result["luminal_crossing"] == sp.log(4)
    assert result["newtonian_speed_limit"] == sp.oo


def test_transport_primaries_are_derived_without_promoting_Q_branch_to_constraint():
    module = _load()
    result = module.derive_transport_dirac()

    assert result["metric_mixing_present"] is True
    momenta = result["transport_momenta_from_lagrangian"]
    assert momenta[0] == 0
    assert sp.simplify(momenta[1] + result["Q_constraint"]) == 0
    assert result["transport_constraint_order"] == ("p_M", "p_nu+Q")
    assert result["transport_poisson_matrix"] == sp.Matrix([[0, -1], [1, 0]])
    assert result["transport_rank"] == 2
    assert result["transport_tertiary_constraints"] == []
    assert result["Q_zero_is_branch_not_dirac_constraint"] is True
    assert result["p_nu_preservation"] == 0
    assert sp.simplify(result["nu_euler_lagrange"] + result["Q_time_derivative"]) == 0
    assert result["combined_constraint_jacobian_rank"] == 10
    assert result["combined_rank"] == 8
    assert result["combined_scalar_configuration_dof"] == 3


def test_k_zero_clock_chain_is_restarted_and_closes_separately():
    module = _load()
    result = module.derive_zero_mode()
    s = result["symbols"]

    assert result["velocity_hessian"].rank() == 2
    assert sp.factor(result["velocity_hessian"].det()) == -9 * s["a"] ** 4 / s["N"] ** 2
    assert result["poisson_matrix"].rank() == 4
    assert result["maximal_nonzero_minor"] == s["a"] ** 12 * (s["N"] ** 2 + 1) ** 4 / s["N"] ** 8
    assert result["tertiary_constraints"] == []
    assert result["homogeneous_configuration_dof"] == 2


def test_intrinsic_homogeneous_equation_proves_coasting_only():
    module = _load()
    result = module.derive_zero_mode()
    s = result["symbols"]

    assert result["intrinsic_laplacian_on_homogeneous_X"] == 0
    assert result["variation_geometry_residual"] == 0
    assert sp.simplify(
        result["sigma_euler_lagrange"] - s["N"] * s["a"] ** 3 * result["R_nn"]
    ) == 0
    expected_acceleration = (
        s["addot"] / s["N"] ** 2
        - s["adot"] * s["Ndot"] / s["N"] ** 3
    )
    assert sp.simplify(result["proper_time_acceleration"] - expected_acceleration) == 0
    assert sp.simplify(result["de_sitter_residual"] + 3 * s["H"] ** 2) == 0
    assert result["de_sitter_allowed"] is False
    proper_equation = result["proper_time_scale_factor_equation"]
    assert proper_equation.rhs == 0
    assert sp.simplify(proper_equation.lhs - expected_acceleration) == 0


def test_curvature_vertex_is_load_bearing_and_favorable_tt_ward_gates_survive():
    module = _load()
    mutation = module.derive_mutation_controls()
    tensor = module.derive_tensor_and_ward_gates()

    assert mutation["coupling_on_hessian_rank"] == 3
    assert mutation["coupling_off_hessian_rank"] == 2
    assert mutation["coupling_on_determinant"] != 0
    assert mutation["coupling_off_determinant"] == 0
    assert tensor["tensor_polarizations"] == 2
    assert tensor["c_T_squared"] == 1
    assert tensor["auxiliary_direct_matter_euler_derivative"] == 0


def test_status_distinguishes_dead_candidate_from_open_parent_program():
    module = _load()
    result = module.derive_all()

    assert result["candidate_status"] == "DEAD"
    assert result["parent_program_status"] == "OPEN"
    assert result["analyzed_unitary_gauge_scalar_configuration_count"] == 3
    assert result["full_covariant_gravitational_dof"].startswith("UNRESOLVED")
    assert result["gamma_PPN"].startswith("UNCOMPUTED")
    assert any("viable FLRW" in reason for reason in result["candidate_dead_reasons"])


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
