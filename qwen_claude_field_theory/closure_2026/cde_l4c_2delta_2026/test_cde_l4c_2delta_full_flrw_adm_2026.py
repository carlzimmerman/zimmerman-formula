#!/usr/bin/env python3
"""Identity tests for the exact real-mode FLRW ADM geometry.

These tests intentionally recompute identities from the exact, unexpanded
objects returned by the implementation.  They do not certify a stored list
of quadratic coefficients.
"""

import sympy as sp

from cde_l4c_2delta_action_gate_2026 import (
    _derive_minkowski_adm_principal,
)
from cde_l4c_2delta_full_flrw_adm_2026 import (
    derive_finite_k_dirac_chain,
    derive_full_quadratic_action,
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


def test_full_action_exposes_eh_cosmological_quadratic_from_exact_geometry():
    """Catches a wrong real-mode normalization or omitted FLRW terms."""

    result = derive_full_quadratic_action()
    symbols = result["symbols"]
    Phi = result["geometry_symbols"]["Phi"]
    Psi = result["geometry_symbols"]["Psi"]
    B = result["geometry_symbols"]["B"]
    H = result["geometry_symbols"]["H"]
    Psi_dot = result["geometry_symbols"]["Psi_dot"]
    q = result["normalization"]["q"]
    Lambda = symbols["Lambda"]

    expected = (
        -3 * Psi_dot**2
        - 6 * H * Phi * Psi_dot
        - 18 * H * Psi * Psi_dot
        - 3 * H**2 * Phi**2
        - 9 * H**2 * Phi * Psi
        - sp.Rational(27, 2) * H**2 * Psi**2
        + 2 * q**2 * B * (Psi_dot + H * Phi)
        - 2 * q**2 * Phi * Psi
        + q**2 * Psi**2
        + 3 * Lambda * Phi * Psi
        - sp.Rational(9, 2) * Lambda * Psi**2
    )
    actual = result["quadratic"]["normalized_pieces"]["eh_cosmological"]
    assert sp.simplify(actual - expected) == 0


def test_exact_exponential_hessian_generates_the_zero_field_quadratic_piece():
    """Catches a phenomenological Phi-gradient term or lost cubic remainder."""

    result = derive_full_quadratic_action()
    exponential = result["exponential"]
    y = exponential["y"]
    amplitude = exponential["amplitude"]
    y_hat = exponential["y_hat"]
    q = result["normalization"]["q"]
    Phi = result["geometry_symbols"]["Phi"]

    independently_differentiated_hessian = sp.diff(
        exponential["primitive"], y, 2
    ).subs(y, 0)
    assert independently_differentiated_hessian == -2
    assert exponential["primitive_hessian_at_zero"] == (
        independently_differentiated_hessian
    )
    assert sp.simplify(
        result["quadratic"]["normalized_pieces"]["exponential"]
        - q**2 * Phi**2
    ) == 0

    remainder = exponential["primitive_remainder"]
    for order in range(3):
        assert series_coefficient(remainder, amplitude, order) == 0
    assert series_coefficient(remainder, amplitude, 3) == (
        sp.Rational(2, 3) * y_hat**3
    )


def test_multiplier_modes_are_expanded_inside_the_exact_action():
    """Catches an asserted effective multiplier or a missing lapse factor."""

    result = derive_full_quadratic_action()
    geometry = result["geometry_symbols"]
    symbols = result["symbols"]
    epsilon = geometry["epsilon"]
    theta = geometry["theta"]
    Phi = geometry["Phi"]
    Psi = geometry["Psi"]
    B = geometry["B"]
    H = geometry["H"]
    Psi_dot = geometry["Psi_dot"]
    q = result["normalization"]["q"]
    lambda_s_bar = symbols["lambda_s_bar"]
    lambda_K_bar = symbols["lambda_K_bar"]
    delta_lambda_s = symbols["delta_lambda_s"]
    delta_lambda_K = symbols["delta_lambda_K"]

    exact_fields = result["exact_multiplier_fields"]
    assert exact_fields["lambda_s"] == (
        lambda_s_bar
        + epsilon * delta_lambda_s * sp.cos(theta)
    )
    assert exact_fields["lambda_K"] == (
        lambda_K_bar
        + epsilon * delta_lambda_K * sp.cos(theta)
    )

    pieces = result["quadratic"]["normalized_pieces"]
    expected_s = (
        -2
        * q**4
        * (delta_lambda_s + lambda_s_bar * Phi)
        * (Phi - Psi)
    )
    expected_K = (
        sp.Rational(1, 2)
        * (delta_lambda_K + lambda_K_bar * Phi)
        * (3 * q**2 * (Psi_dot + H * Phi) - q**4 * B)
    )
    assert sp.simplify(pieces["lambda_s"] - expected_s) == 0
    assert sp.simplify(pieces["lambda_K"] - expected_K) == 0


def test_unitary_cuscuton_and_potential_are_separate_action_contributions():
    """Catches an invented matter term or an erroneous residual lapse in sqrt(X)."""

    result = derive_full_quadratic_action()
    symbols = result["symbols"]
    Psi = result["geometry_symbols"]["Psi"]
    Phi = result["geometry_symbols"]["Phi"]
    Mpl2 = symbols["Mpl2"]
    Mc2 = symbols["Mc2"]
    V = symbols["V"]
    pieces = result["quadratic"]["normalized_pieces"]

    assert sp.simplify(
        pieces["cuscuton"]
        - sp.Rational(9, 2) * Mc2 * Psi**2 / Mpl2
    ) == 0
    assert sp.simplify(
        pieces["potential"]
        - sp.Rational(3, 2) * V * Psi * (2 * Phi - 3 * Psi) / Mpl2
    ) == 0
    assert result["scope"]["matter_perturbations_invented"] is False


def test_background_substitutions_kill_homogeneous_tadpoles_not_cosine_averaging():
    """Catches a kinematic zero-mode average masquerading as an on-shell check."""

    result = derive_full_quadratic_action()
    symbols = result["symbols"]
    geometry = result["geometry_symbols"]
    Mpl2 = symbols["Mpl2"]
    Mc2 = symbols["Mc2"]
    H_dot = symbols["H_dot"]
    scale = geometry["scale_factor"]
    Psi = geometry["Psi"]

    background = result["background"]
    assert background["friedmann_residual_before_solving"] != 0
    assert background["raychaudhuri_residual_before_solving"] != 0
    assert background["friedmann_residual_after_solving"] == 0
    assert background["raychaudhuri_residual_after_solving"] == 0
    assert background["vacuum_witness_residuals"] == (0, 0, 0)

    tadpoles = result["tadpoles"]
    assert tadpoles["finite_mode_spatial_average"] == 0
    assert sp.simplify(
        tadpoles["homogeneous_bulk_after_friedmann"]
        + 3 * scale**3 * (Mc2 + 2 * Mpl2 * H_dot) * Psi
    ) == 0
    assert tadpoles["homogeneous_bulk_on_shell"] == 0
    assert sp.simplify(
        tadpoles["temporal_boundary_primitive"]
        - 6 * Mpl2 * scale**3 * geometry["H"] * Psi
    ) == 0


def test_time_ibp_remainder_needs_raychaudhuri_and_keeps_lambda_K_canonical():
    """Catches a dropped dot(A), premature on-shell step, or time-IBP of lambda_K."""

    result = derive_full_quadratic_action()
    geometry = result["geometry_symbols"]
    symbols = result["symbols"]
    A = result["normalization"]["A"]
    q = result["normalization"]["q"]
    Phi = geometry["Phi"]
    Psi = geometry["Psi"]
    B = geometry["B"]
    H = geometry["H"]
    Psi_dot = geometry["Psi_dot"]
    H_dot = symbols["H_dot"]
    Mpl2 = symbols["Mpl2"]
    Mc2 = symbols["Mc2"]
    lambda_s = symbols["delta_lambda_s"] + symbols["lambda_s_bar"] * Phi
    lambda_K = symbols["delta_lambda_K"] + symbols["lambda_K_bar"] * Phi
    theta = Psi_dot + H * Phi

    expected_bulk = A * (
        -3 * theta**2
        + 2 * q**2 * B * theta
        + q**2 * (Phi - Psi) ** 2
        - 2 * q**4 * lambda_s * (Phi - Psi)
        + sp.Rational(1, 2)
        * lambda_K
        * (3 * q**2 * theta - q**4 * B)
    )
    ibp = result["time_ibp"]
    assert sp.simplify(
        ibp["temporal_boundary_primitive"] + 9 * A * H * Psi**2
    ) == 0
    assert sp.simplify(result["normalization"]["A_dot"] - 3 * H * A) == 0
    assert sp.simplify(
        ibp["bulk_remainder"]
        - 9 * A * (H_dot + 3 * H**2) * Psi**2
    ) == 0
    assert sp.simplify(
        ibp["bulk_after_friedmann"]
        - expected_bulk
        - 9 * A * (H_dot + Mc2 / (2 * Mpl2)) * Psi**2
    ) == 0
    assert sp.simplify(ibp["on_shell_bulk"] - expected_bulk) == 0

    # A canonical time integration by parts must leave the lambda_K velocity.
    assert sp.simplify(
        sp.diff(
            ibp["on_shell_bulk"],
            symbols["delta_lambda_K"],
            Psi_dot,
        )
        - sp.Rational(3, 2) * A * q**2
    ) == 0


def test_minkowski_limit_matches_a_direct_specialized_adm_expansion_by_coefficient():
    """Catches failure of specialization/epsilon-expansion commutation."""

    result = derive_full_quadratic_action()
    comparison = result["minkowski_comparison"][
        "internal_specialization_expansion_commutation"
    ]
    assert comparison["direct_specialization_before_expansion"] != 0
    assert comparison["flrw_simultaneous_limit"] != 0
    assert comparison["coefficient_keys"]
    assert all(
        residual == 0
        for residual in comparison["coefficient_residuals"].values()
    )
    assert sp.simplify(
        comparison["direct_specialization_before_expansion"]
        - comparison["flrw_simultaneous_limit"]
    ) == 0


def test_minkowski_limit_bridges_to_existing_action_gate_generator_by_coefficient():
    """Catches an internal commutation check mislabeled as independent provenance."""

    result = derive_full_quadratic_action()
    bridge = result["minkowski_comparison"][
        "independent_action_gate_bridge"
    ]
    y = sp.symbols("y_existing_gate", positive=True)
    correction = 2 * ((1 + y) * sp.exp(-y) - 1)
    existing = _derive_minkowski_adm_principal(correction, y)
    geometry = result["geometry_symbols"]
    symbols = result["symbols"]
    expected_map = {
        existing["A"]: result["normalization"]["A"],
        existing["k"]: result["normalization"]["q"],
        existing["Phi"]: geometry["Phi"],
        existing["Psi"]: geometry["Psi"],
        existing["B"]: geometry["B"],
        existing["lambda_s"]: symbols["delta_lambda_s"],
        existing["lambda_K"]: symbols["delta_lambda_K"],
        existing["Psi_dot"]: geometry["Psi_dot"],
    }

    assert bridge["source_expression"] == (
        existing["generated_zero_field_lagrangian"]
    )
    assert bridge["symbol_map"] == expected_map
    assert sp.simplify(
        bridge["mapped_expression"]
        - bridge["source_expression"].subs(
            expected_map, simultaneous=True
        )
    ) == 0
    assert bridge["coefficient_keys"]
    assert all(
        residual == 0
        for residual in bridge["coefficient_residuals"].values()
    )
    assert sp.simplify(
        bridge["mapped_expression"]
        - bridge["task2_minkowski_expression"]
    ) == 0


def test_removing_cuscuton_fails_the_on_shell_bulk_identity():
    """Catches a tautological on-shell reduction insensitive to a missing term."""

    result = derive_full_quadratic_action()
    mutation = result["mutation_controls"]["without_cuscuton"]
    A = result["normalization"]["A"]
    H_dot = result["symbols"]["H_dot"]
    Psi = result["geometry_symbols"]["Psi"]

    assert mutation["on_shell_residual"] != 0
    assert sp.simplify(
        mutation["on_shell_residual"] - 9 * A * H_dot * Psi**2
    ) == 0
    assert mutation["identity_survives"] is False


def _canonical_poisson(first, second, coordinates, momenta):
    return sp.factor(
        sum(
            sp.diff(first, coordinate) * sp.diff(second, momentum)
            - sp.diff(first, momentum) * sp.diff(second, coordinate)
            for coordinate, momentum in zip(coordinates, momenta)
        )
    )


def test_E_is_restored_by_a_spatial_diffeomorphism_identity_before_legendre():
    result = derive_finite_k_dirac_chain()
    restoration = result["restoration"]
    canonical = result["canonical"]
    symbols = result["symbols"]

    assert restoration["Sigma"] == (
        symbols["B"] - symbols["a"] ** 2 * symbols["E_dot"]
    )
    assert restoration["lagrangian"].has(symbols["E_dot"])
    assert not restoration["lagrangian"].has(symbols["E"])
    assert restoration["task2_provenance_residual"] == 0
    assert restoration["E_zero_gauge_action_residual"] == 0

    independently_derived_identity = sp.simplify(
        sp.diff(restoration["lagrangian"], symbols["E_dot"])
        + symbols["a"] ** 2
        * sp.diff(restoration["lagrangian"], symbols["B"])
    )
    assert independently_derived_identity == 0
    assert restoration["spatial_diffeomorphism_identity"] == 0

    # No Legendre-transform output is used to establish this identity.
    assert restoration["identity_checked_before_legendre"] is True
    assert canonical["lagrangian"] == restoration["lagrangian"]


def test_all_momenta_hessian_nullspace_and_primaries_are_generated():
    result = derive_finite_k_dirac_chain()
    canonical = result["canonical"]
    lagrangian = canonical["lagrangian"]

    independently_derived_momenta = tuple(
        sp.factor(sp.diff(lagrangian, velocity))
        for velocity in canonical["velocities"]
    )
    assert canonical["derived_momenta"] == independently_derived_momenta

    independently_derived_hessian = sp.hessian(
        lagrangian, canonical["velocities"]
    )
    assert canonical["velocity_hessian"] == independently_derived_hessian
    assert canonical["velocity_hessian_rank"] == (
        independently_derived_hessian.rank()
    )
    assert canonical["velocity_hessian_nullspace"] == (
        independently_derived_hessian.nullspace()
    )
    for null_vector in canonical["velocity_hessian_nullspace"]:
        assert _zero_matrix(independently_derived_hessian * null_vector)

    independently_derived_primaries = tuple(
        sp.factor(
            sum(
                null_vector[index]
                * (
                    canonical["momenta"][index]
                    - independently_derived_momenta[index]
                )
                for index in range(len(canonical["coordinates"]))
            )
        )
        for null_vector in canonical["velocity_hessian_nullspace"]
    )
    assert canonical["primaries"] == independently_derived_primaries

    for index in canonical["regular_velocity_indices"]:
        momentum_equation = (
            canonical["momenta"][index]
            - independently_derived_momenta[index]
        )
        assert sp.simplify(
            momentum_equation.subs(canonical["velocity_solution"])
        ) == 0
    assert canonical["legendre_decomposition_residual"] == 0
    assert sp.simplify(
        canonical["total_hamiltonian"]
        - canonical["canonical_hamiltonian"]
        - sum(
            multiplier * primary
            for multiplier, primary in zip(
                canonical["primary_multipliers"],
                canonical["primaries"],
            )
        )
    ) == 0


def test_final_constraints_and_classification_come_from_actual_matrices():
    result = derive_finite_k_dirac_chain()
    canonical = result["canonical"]
    dirac = result["dirac"]
    classification = result["classification"]
    coordinates = canonical["coordinates"]
    momenta = canonical["momenta"]

    for primary, secondary in zip(
        canonical["primaries"], dirac["secondary_candidates"]
    ):
        independently_preserved = sp.factor(
            result["time_preservation"]["partial_time_operator"](primary)
            + _canonical_poisson(
                primary,
                canonical["canonical_hamiltonian"],
                coordinates,
                momenta,
            )
        )
        assert sp.simplify(secondary - independently_preserved) == 0

    constraints = dirac["constraints"]
    matrix = dirac["poisson_matrix"]
    jacobian = sp.Matrix(constraints).jacobian(
        coordinates + momenta
    )
    assert (matrix + matrix.T).applyfunc(sp.simplify) == sp.zeros(
        len(constraints)
    )
    assert dirac["poisson_rank"] == matrix.rank()
    assert dirac["poisson_determinant"] == sp.factor(matrix.det())
    assert dirac["constraint_jacobian"] == jacobian
    assert dirac["constraint_jacobian_rank"] == jacobian.rank()
    assert dirac["constraint_jacobian_rank"] == len(constraints)

    minor = dirac["rank_witness_minor"]
    rebuilt_minor = matrix.extract(minor["rows"], minor["columns"])
    assert minor["matrix"] == rebuilt_minor
    assert minor["size"] == dirac["poisson_rank"]
    assert minor["determinant"] == sp.factor(rebuilt_minor.det())
    assert minor["determinant"] != 0

    assert all(
        rank == dirac["poisson_rank"]
        for rank in dirac["sampled_exact_ranks"]
    )
    assert all(
        rank == dirac["poisson_rank"]
        for rank in dirac["sampled_numerical_ranks"]
    )

    nullspace = matrix.nullspace()
    assert classification["poisson_nullspace"] == nullspace
    assert classification["first_class_count"] == len(nullspace)
    assert classification["second_class_count"] == matrix.rank()
    assert (
        classification["first_class_count"]
        + classification["second_class_count"]
        == len(constraints)
    )
    independently_counted_dof = sp.Rational(
        classification["phase_dimension"]
        - 2 * classification["first_class_count"]
        - classification["second_class_count"],
        2,
    )
    assert classification["configuration_dof"] == independently_counted_dof
    assert classification["weak_first_class_brackets"] == sp.zeros(
        classification["first_class_count"], len(constraints)
    )


def test_explicit_time_preservation_fixes_only_matrix_selected_multipliers():
    result = derive_finite_k_dirac_chain()
    canonical = result["canonical"]
    dirac = result["dirac"]
    preservation = result["time_preservation"]
    symbols = result["symbols"]

    independently_derived_partials = tuple(
        sp.factor(
            sum(
                sp.diff(constraint, background)
                * background_dot
                for background, background_dot in preservation[
                    "background_derivative_rules"
                ].items()
            )
        )
        for constraint in dirac["constraints"]
    )
    assert all(
        sp.simplify(stored - independent) == 0
        for stored, independent in zip(
            preservation["partial_time_terms"],
            independently_derived_partials,
        )
    )

    independently_derived_totals = tuple(
        sp.factor(
            partial
            + _canonical_poisson(
                constraint,
                canonical["total_hamiltonian"],
                canonical["coordinates"],
                canonical["momenta"],
            )
        )
        for constraint, partial in zip(
            dirac["constraints"], independently_derived_partials
        )
    )
    assert all(
        sp.simplify(stored - independent) == 0
        for stored, independent in zip(
            preservation["total_time_derivatives"],
            independently_derived_totals,
        )
    )
    assert any(term.has(symbols["H_dot"]) for term in independently_derived_partials)
    assert any(
        term.has(symbols["lambda_s_bar_dot"])
        for term in independently_derived_partials
    )
    assert any(
        term.has(symbols["lambda_K_bar_dot"])
        for term in independently_derived_partials
    )

    coefficient_matrix = sp.Matrix(
        [
            [
                sp.diff(equation, multiplier)
                for multiplier in canonical["primary_multipliers"]
            ]
            for equation in preservation["on_constraint_surface"]
        ]
    )
    assert (
        preservation["multiplier_coefficient_matrix"] - coefficient_matrix
    ).applyfunc(sp.simplify) == sp.zeros(*coefficient_matrix.shape)
    assert preservation["multiplier_coefficient_rank"] == coefficient_matrix.rank()
    assert preservation["augmented_rank"] == coefficient_matrix.row_join(
        preservation["multiplier_rhs"]
    ).rank()
    assert preservation["multiplier_coefficient_rank"] == preservation[
        "augmented_rank"
    ]
    fixing_minor = preservation["multiplier_rank_witness_minor"]
    rebuilt_fixing_minor = coefficient_matrix.extract(
        fixing_minor["rows"], fixing_minor["columns"]
    )
    assert fixing_minor["size"] == preservation[
        "multiplier_coefficient_rank"
    ]
    assert (
        fixing_minor["matrix"] - rebuilt_fixing_minor
    ).applyfunc(sp.simplify) == sp.zeros(*rebuilt_fixing_minor.shape)
    assert sp.simplify(
        fixing_minor["determinant"] - rebuilt_fixing_minor.det()
    ) == 0
    assert fixing_minor["determinant"] != 0
    assert all(residual == 0 for residual in preservation["closure_residuals"])
    assert preservation["tertiary_candidates"] == ()
    assert preservation["no_tertiary_evidence"] is True
    assert preservation["free_multipliers"]
    assert preservation["iterations"][-1]["jacobian_rank"] == (
        preservation["iterations"][-2]["jacobian_rank"]
    )


def test_spatial_generator_and_E_zero_gauge_reproduce_gauge_fixed_chain():
    result = derive_finite_k_dirac_chain()
    canonical = result["canonical"]
    gauge = result["spatial_gauge"]
    symbols = result["symbols"]

    generator = gauge["generator"]
    independently_derived_variations = {
        coordinate: _canonical_poisson(
            coordinate,
            generator,
            canonical["coordinates"],
            canonical["momenta"],
        )
        for coordinate in canonical["coordinates"]
    }
    assert gauge["coordinate_variations"] == independently_derived_variations
    assert sp.simplify(
        gauge["coordinate_variations"][symbols["B"]]
        - symbols["a"] ** 2 * gauge["eta_dot"]
    ) == 0
    assert sp.simplify(
        gauge["coordinate_variations"][symbols["E"]] - gauge["eta"]
    ) == 0
    assert gauge["Sigma_variation"] == 0
    assert all(residual == 0 for residual in gauge["weak_generator_brackets"])
    assert gauge["generator_constraint_representation_residual"] == 0

    assert gauge["E_zero_action_residual"] == 0
    assert gauge["E_zero_preservation_equation"].subs(
        symbols["B"], gauge["B_solution"]
    ) == 0
    comparison = gauge["existing_gauge_fixed_comparison"]
    assert comparison["lagrangian_residual"] == 0
    assert comparison["constraint_count_matches"] is True
    assert all(
        residual == 0
        for residual in comparison["proportionality_residuals"]
    )


def test_extended_one_form_and_positive_gradient_branch_are_derived():
    result = derive_finite_k_dirac_chain()
    canonical = result["canonical"]
    reduction = result["reduction"]
    positive = result["positive_gradient"]
    symbols = result["symbols"]

    independently_pulled_extended = sp.simplify(
        reduction["pulled_spatial_one_form"]
        - reduction["reduced_hamiltonian"] * reduction["dt"]
    )
    assert reduction["pulled_extended_one_form"] == independently_pulled_extended
    assert reduction["symplectic_matrix"] == sp.Matrix(
        [
            [
                sp.diff(reduction["one_form_coefficients"][column], row)
                - sp.diff(reduction["one_form_coefficients"][row], column)
                for column in reduction["free_phase_variables"]
            ]
            for row in reduction["free_phase_variables"]
        ]
    )
    assert reduction["symplectic_rank"] == reduction["symplectic_matrix"].rank()
    assert reduction["quotient_symplectic_determinant"] != 0
    assert reduction["symplectic_rank"] == result["classification"][
        "reduced_phase_dimension"
    ]

    independently_derived_positive_momenta = tuple(
        sp.factor(
            sp.diff(positive["lagrangian"], velocity)
        )
        for velocity in canonical["velocities"]
    )
    assert positive["derived_momenta"] == independently_derived_positive_momenta
    omega_squared = sp.simplify(
        sp.diff(
            positive["reduced_hamiltonian"], symbols["p_Psi"], 2
        )
        * sp.diff(
            positive["reduced_hamiltonian"], symbols["Psi"], 2
        )
    )
    assert positive["omega_squared"] == omega_squared
    assert positive["sound_speed_squared"] == sp.simplify(
        omega_squared / symbols["q"] ** 2
    )
    assert positive["exact_sound_speed_squared"] == sp.simplify(
        positive["sound_speed_squared"].subs(
            positive["lambda_parallel"],
            positive["exact_lambda_parallel"],
        )
    )
    assert sp.limit(
        positive["exact_sound_speed_squared"], positive["y"], 0, dir="+"
    ) == 0


def test_dirac_deletion_and_coefficient_mutations_change_generated_results():
    result = derive_finite_k_dirac_chain()
    canonical = result["canonical"]
    baseline = result["dirac"]
    mutations = result["mutation_controls"]

    deletion = mutations["without_lambda_s_coupling"]
    assert deletion["lagrangian_difference"] != 0
    assert deletion["lambda_s_euler_derivative"] == 0
    assert (
        deletion["constraint_jacobian_rank"]
        != baseline["constraint_jacobian_rank"]
        or deletion["poisson_rank"] != baseline["poisson_rank"]
    )

    coefficient = mutations["perturbed_shear_theta_coefficient"]
    assert coefficient["lagrangian_difference"] != 0
    assert coefficient["spatial_diffeomorphism_identity"] == 0
    assert coefficient["derived_momenta"] != canonical["derived_momenta"]
    assert (
        coefficient["poisson_matrix"] != baseline["poisson_matrix"]
        or coefficient["constraints"] != baseline["constraints"]
    )


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
