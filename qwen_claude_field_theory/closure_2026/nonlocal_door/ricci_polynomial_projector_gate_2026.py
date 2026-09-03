#!/usr/bin/env python3
"""Action and Hamiltonian gate for a smooth Ricci-polynomial projector.

The earlier Minkowski stabilizer lemma leaves open a projector that is spatial
away from zero curvature and vanishes smoothly at zero.  This file constructs
one explicitly,

    S^mu_nu = R^mu_nu - (R/4) delta^mu_nu,
    P^mu_nu = (3/4 tr(S^2)) delta^mu_nu - (S^2)^mu_nu,

and puts it in the varied auxiliary sector

    S_aux = int sqrt(-g) [lambda(P^mn nabla_m nabla_n chi - J) + U(chi)].

The calculation does not claim to classify all metric spectral projectors.
It derives why this polynomial candidate fails: anisotropic curvature turns on
a ghost-signed time-principal auxiliary block, and its Bianchi-I action is
nondegenerate in both physical shear accelerations.  A reduced Ostrogradsky
Dirac calculation carries the latter chain to closure.  It also derives the
multiplier/effective-stress/matter-Ward fork instead of assuming a phantom
source appears in Einstein's equations.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _poisson(
    left: sp.Expr,
    right: sp.Expr,
    coordinates: list[sp.Symbol],
    momenta: list[sp.Symbol],
) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.diff(left, q) * sp.diff(right, p)
            - sp.diff(left, p) * sp.diff(right, q)
            for q, p in zip(coordinates, momenta)
        )
    )


def derive_ricci_polynomial_projector_gate() -> dict[str, Any]:
    """Return exact symbolic objects for every branch of the gate."""

    # 1. Isotropic Segre {1,(111)} branch.
    d = sp.Symbol("d", nonzero=True, real=True)
    identity4 = sp.eye(4)
    s_isotropic = sp.diag(-3 * d, d, d, d)
    trace_s_squared = sp.simplify(sp.trace(s_isotropic**2))
    p_isotropic = sp.simplify(
        sp.Rational(3, 4) * trace_s_squared * identity4 - s_isotropic**2
    )
    scaled_idempotence_residual = sp.simplify(
        p_isotropic**2 - 8 * d**2 * p_isotropic
    )

    # 2. Generic diagonal anisotropy.  The mixed time eigenvalue becomes a
    # sum of spatial-eigenvalue differences squared.  Raising its second index
    # with (-+++) makes P^{00} negative.
    s1, s2, s3 = sp.symbols("s_1 s_2 s_3", real=True)
    s0 = -s1 - s2 - s3
    s_anisotropic = sp.diag(s0, s1, s2, s3)
    trace_anisotropic_squared = sp.simplify(sp.trace(s_anisotropic**2))
    p_anisotropic = sp.simplify(
        sp.Rational(3, 4) * trace_anisotropic_squared * identity4
        - s_anisotropic**2
    )
    p0_mixed = sp.factor(p_anisotropic[0, 0])
    p0_sum_squares = sp.expand(
        ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 4
    )
    p0_sum_squares_residual = sp.simplify(p0_mixed - p0_sum_squares)

    anisotropy = sp.Symbol("epsilon_aniso", positive=True)
    example_substitution = {s1: d + anisotropy, s2: d - anisotropy, s3: d}
    p0_mixed_example = sp.simplify(p0_mixed.subs(example_substitution))
    p00_contravariant_example = -p0_mixed_example
    lambda_dot, chi_dot = sp.symbols("lambda_dot chi_dot", real=True)
    frozen_principal_lagrangian = sp.simplify(
        -p00_contravariant_example * lambda_dot * chi_dot
    )
    auxiliary_velocity_hessian = sp.hessian(
        frozen_principal_lagrangian, (lambda_dot, chi_dot)
    )
    auxiliary_velocity_eigenvalues = list(
        auxiliary_velocity_hessian.eigenvals().keys()
    )

    # 3. Highest metric derivatives in Bianchi I.  At a point with N=1 and
    # a_i=1, retain A_i=dot(H_i).  The displayed R^mu_nu entries are the
    # highest-derivative pieces; lower-H terms cannot change this Hessian.
    acceleration = sp.Matrix(sp.symbols("A_1 A_2 A_3", real=True))
    acceleration_sum = sp.simplify(sum(acceleration))
    ricci_principal = sp.diag(
        acceleration_sum, acceleration[0], acceleration[1], acceleration[2]
    )
    ricci_trace_principal = sp.trace(ricci_principal)
    s_bianchi = sp.simplify(
        ricci_principal - ricci_trace_principal * identity4 / 4
    )
    trace_s_bianchi_squared = sp.simplify(sp.trace(s_bianchi**2))
    acceleration_squared_sum = sp.simplify(sum(item**2 for item in acceleration))
    p_bianchi = sp.simplify(
        sp.Rational(3, 4) * trace_s_bianchi_squared * identity4 - s_bianchi**2
    )
    spatial_projector_trace = sp.simplify(sum(p_bianchi[i, i] for i in range(1, 4)))
    expected_spatial_projector_trace = sp.simplify(
        sp.Rational(5, 4) * acceleration_squared_sum
        + sp.Rational(1, 4) * acceleration_sum**2
    )
    overall_coefficient = sp.Symbol("C_BI", nonzero=True, real=True)
    bianchi_highest_lagrangian = sp.expand(
        overall_coefficient * spatial_projector_trace
    )
    acceleration_hessian = sp.simplify(
        sp.hessian(bianchi_highest_lagrangian, tuple(acceleration))
    )
    trace_direction = sp.Matrix([1, 1, 1])
    shear_directions = (sp.Matrix([1, -1, 0]), sp.Matrix([1, 1, -2]))
    shear_basis = sp.Matrix.hstack(*shear_directions)
    shear_hessian = sp.simplify(
        shear_basis.T * acceleration_hessian * shear_basis
    )

    # 4. Principal Ostrogradsky/Dirac chain for those two physical shears.
    # q_i and v_i=qdot_i are independent Ostrogradsky coordinates.  lambda is
    # retained as a multiplier instead of being frozen.
    q1, q2, v1, v2, lam = sp.symbols("q_1 q_2 v_1 v_2 lambda", real=True)
    a1, a2 = sp.symbols("a_1 a_2", real=True)
    kappa = sp.Symbol("kappa_shear", positive=True)
    source = sp.Symbol("J_shear", positive=True)
    shear_lagrangian = sp.simplify(
        kappa * lam * (a1**2 + a2**2) / 2 - lam * source
    )
    shear_acceleration_hessian = sp.hessian(shear_lagrangian, (a1, a2))
    pi1, pi2 = sp.symbols("pi_1 pi_2", real=True)
    acceleration_solution = sp.solve(
        [
            sp.Eq(pi1, sp.diff(shear_lagrangian, a1)),
            sp.Eq(pi2, sp.diff(shear_lagrangian, a2)),
        ],
        (a1, a2),
        dict=True,
    )[0]
    p1, p2, p_lam = sp.symbols("P_1 P_2 p_lambda", real=True)
    canonical_hamiltonian = sp.simplify(
        p1 * v1
        + p2 * v2
        + pi1 * acceleration_solution[a1]
        + pi2 * acceleration_solution[a2]
        - shear_lagrangian.subs(acceleration_solution)
    )
    multiplier = sp.Symbol("u_lambda", real=True)
    total_hamiltonian = canonical_hamiltonian + multiplier * p_lam
    ostro_coordinates = [q1, q2, v1, v2, lam]
    ostro_momenta = [p1, p2, pi1, pi2, p_lam]
    primary_constraints = [p_lam]
    primary_preservation = _poisson(
        p_lam, total_hamiltonian, ostro_coordinates, ostro_momenta
    )
    secondary_constraints = [sp.factor(primary_preservation)]
    ostro_constraints = primary_constraints + secondary_constraints
    ostro_poisson_matrix = sp.Matrix(
        [
            [
                _poisson(left, right, ostro_coordinates, ostro_momenta)
                for right in ostro_constraints
            ]
            for left in ostro_constraints
        ]
    )
    momentum_norm_squared = pi1**2 + pi2**2
    constraint_surface_substitution = {
        momentum_norm_squared: 2 * kappa * lam**2 * source
    }
    poisson_determinant_on_constraint_surface = sp.factor(
        sp.factor(ostro_poisson_matrix.det()).subs(
            constraint_surface_substitution
        )
    )
    secondary_preservation = _poisson(
        secondary_constraints[0],
        total_hamiltonian,
        ostro_coordinates,
        ostro_momenta,
    )
    multiplier_solution = sp.solve(
        sp.Eq(secondary_preservation, 0), multiplier, dict=True
    )
    first_class_count = len(ostro_constraints) - ostro_poisson_matrix.rank()
    second_class_count = ostro_poisson_matrix.rank()
    phase_dimension = 2 * len(ostro_coordinates)
    physical_dof = sp.simplify(
        sp.Rational(1, 2)
        * (phase_dimension - 2 * first_class_count - second_class_count)
    )
    baseline_shear_dof = len(shear_directions)

    # 5. Multiplier/effective-stress/Ward trilemma.  For a frozen elliptic
    # eigenvalue f>0 and k!=0, variation with respect to chi fixes lambda.
    # Without U it fixes lambda=0; every metric variation of this sector is
    # proportional to lambda (or derivatives thereof), so its on-shell stress
    # vanishes under standard homogeneous boundary data.
    f, wave_number = sp.symbols("f k", positive=True)
    chi, multiplier_field = sp.symbols("chi lambda_aux", real=True)
    source_aux = sp.Symbol("J", real=True)
    potential_prime = sp.Symbol("U_prime", nonzero=True, real=True)
    bare_mode_lagrangian = (
        -f * wave_number**2 * multiplier_field * chi
        - source_aux * multiplier_field
    )
    bare_chi_equation = sp.diff(bare_mode_lagrangian, chi)
    bare_lambda_solution = sp.solve(
        sp.Eq(bare_chi_equation, 0), multiplier_field
    )[0]
    rescued_mode_lagrangian = bare_mode_lagrangian + potential_prime * chi
    rescued_chi_equation = sp.diff(rescued_mode_lagrangian, chi)
    rescued_lambda_solution = sp.solve(
        sp.Eq(rescued_chi_equation, 0), multiplier_field
    )[0]

    # The separate S_m Ward identity is div(T_m)=E_m grad(psi).  The full
    # matter equation for -lambda J(psi) is E_m-lambda J_psi=0, hence the
    # ordinary S_m tensor exchanges momentum whenever J_psi != 0.
    j_psi = sp.Symbol("delta_J_over_delta_psi", nonzero=True, real=True)
    grad_psi = sp.Symbol("nabla_psi", nonzero=True, real=True)
    direct_matter_source_divergence = sp.simplify(
        rescued_lambda_solution * j_psi * grad_psi
    )
    metric_only_source_divergence = sp.simplify(
        direct_matter_source_divergence.subs(j_psi, 0)
    )

    return {
        "action": (
            "S_EH[g]+S_m[g,psi]+int sqrt(-g) "
            "{lambda[P^mn(g) nabla_m nabla_n chi-J(g,T)]+U(chi)}"
        ),
        "isotropic_projector": {
            "d": d,
            "traceless_ricci": s_isotropic,
            "trace_s_squared": trace_s_squared,
            "mixed_projector": p_isotropic,
            "scaled_idempotence_residual": scaled_idempotence_residual,
            "rank_nonzero_curvature": p_isotropic.rank(),
            "rank_zero_curvature": p_isotropic.subs(d, 0).rank(),
            "flat_limit": p_isotropic.subs(d, 0),
        },
        "anisotropic_projector": {
            "spatial_eigenvalues": (s1, s2, s3),
            "anisotropy": anisotropy,
            "mixed_projector": p_anisotropic,
            "time_mixed_eigenvalue": p0_mixed,
            "time_mixed_sum_of_squares": p0_sum_squares,
            "time_mixed_sum_of_squares_residual": p0_sum_squares_residual,
            "time_mixed_eigenvalue_is_sum_of_squares": bool(
                p0_sum_squares_residual == 0
            ),
            "time_mixed_example": p0_mixed_example,
            "time_contravariant_example": p00_contravariant_example,
            "frozen_principal_lagrangian_example": frozen_principal_lagrangian,
            "auxiliary_velocity_hessian_example": auxiliary_velocity_hessian,
            "auxiliary_velocity_hessian_eigenvalues": auxiliary_velocity_eigenvalues,
            "auxiliary_velocity_hessian_rank": auxiliary_velocity_hessian.rank(),
            "auxiliary_velocity_hessian_has_opposite_signs": bool(
                any(value.is_positive for value in auxiliary_velocity_eigenvalues)
                and any(value.is_negative for value in auxiliary_velocity_eigenvalues)
            ),
            "isotropic_auxiliary_velocity_hessian_rank": (
                auxiliary_velocity_hessian.subs(anisotropy, 0).rank()
            ),
        },
        "bianchi_i_highest_derivative": {
            "accelerations": acceleration,
            "traceless_ricci": s_bianchi,
            "trace_s_squared": trace_s_bianchi_squared,
            "trace_s_squared_residual": sp.simplify(
                trace_s_bianchi_squared - acceleration_squared_sum
            ),
            "mixed_projector": p_bianchi,
            "spatial_projector_trace": spatial_projector_trace,
            "spatial_projector_trace_residual": sp.simplify(
                spatial_projector_trace - expected_spatial_projector_trace
            ),
            "highest_derivative_lagrangian": bianchi_highest_lagrangian,
            "overall_coefficient": overall_coefficient,
            "acceleration_hessian": acceleration_hessian,
            "trace_direction": trace_direction,
            "shear_directions": shear_directions,
            "shear_hessian": shear_hessian,
            "shear_hessian_rank": shear_hessian.rank(),
            "scope": (
                "N=1 local Bianchi-I principal sector; lapse-retaining full "
                "Dirac completion remains required"
            ),
        },
        "ostrogradsky_shear_dirac": {
            "lagrangian": shear_lagrangian,
            "acceleration_hessian": shear_acceleration_hessian,
            "acceleration_hessian_rank": shear_acceleration_hessian.rank(),
            "acceleration_hessian_determinant": sp.factor(
                shear_acceleration_hessian.det()
            ),
            "acceleration_solution": acceleration_solution,
            "canonical_hamiltonian": canonical_hamiltonian,
            "primary_constraints": primary_constraints,
            "primary_preservation": primary_preservation,
            "secondary_constraints": secondary_constraints,
            "secondary_preservation": secondary_preservation,
            "multiplier_solution": multiplier_solution,
            "tertiary_constraints": [],
            "poisson_matrix": ostro_poisson_matrix,
            "poisson_determinant": sp.factor(ostro_poisson_matrix.det()),
            "poisson_determinant_on_constraint_surface": (
                poisson_determinant_on_constraint_surface
            ),
            "first_class_count": first_class_count,
            "second_class_count": second_class_count,
            "phase_dimension": phase_dimension,
            "physical_dof": physical_dof,
            "baseline_shear_dof": baseline_shear_dof,
            "extra_dof": sp.simplify(physical_dof - baseline_shear_dof),
            "hamiltonian_linear_in_ostro_momenta": bool(
                sp.diff(canonical_hamiltonian, p1) == v1
                and sp.diff(canonical_hamiltonian, p2) == v2
                and sp.diff(canonical_hamiltonian, p1, 2) == 0
                and sp.diff(canonical_hamiltonian, p2, 2) == 0
            ),
        },
        "multiplier_ward_trilemma": {
            "bare_mode_lagrangian": bare_mode_lagrangian,
            "bare_chi_equation": bare_chi_equation,
            "bare_multiplier_lambda_solution": bare_lambda_solution,
            "bare_multiplier_on_shell_stress_coefficient": sp.simplify(
                multiplier_field.subs(multiplier_field, bare_lambda_solution)
            ),
            "rescued_mode_lagrangian": rescued_mode_lagrangian,
            "rescued_chi_equation": rescued_chi_equation,
            "rescued_multiplier_lambda_solution": rescued_lambda_solution,
            "direct_matter_source_divergence": direct_matter_source_divergence,
            "metric_only_source_divergence": metric_only_source_divergence,
            "bare_branch_status": "DEAD: no effective stress",
            "direct_source_rescue_status": (
                "DEAD under separate ordinary-matter conservation"
            ),
            "metric_source_rescue_status": (
                "OPEN in general; this Ricci-polynomial candidate fails stability"
            ),
        },
        "global_status": (
            "RICCI-POLYNOMIAL CANDIDATE DEAD; GENERAL RANK-CHANGING "
            "METRIC-SPECTRAL BRANCH OPEN"
        ),
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_ricci_polynomial_projector_gate()
    isotropic = result["isotropic_projector"]
    anisotropic = result["anisotropic_projector"]
    bianchi = result["bianchi_i_highest_derivative"]
    ostro = result["ostrogradsky_shear_dirac"]
    trilemma = result["multiplier_ward_trilemma"]

    print("=" * 104)
    print("RICCI-POLYNOMIAL VANISHING PROJECTOR: ACTION / DIRAC / WARD GATE")
    print("=" * 104)
    print("Action:", result["action"])

    print("\n[1] Isotropic construction")
    print("  S =", isotropic["traceless_ricci"])
    print("  tr(S^2) =", isotropic["trace_s_squared"])
    print("  P =", isotropic["mixed_projector"])
    print("  ranks (d!=0,d=0) =", isotropic["rank_nonzero_curvature"], isotropic["rank_zero_curvature"])
    checks = [
        _check(
            "P is a smooth rank-three scaled spatial projector off flat space",
            isotropic["scaled_idempotence_residual"] == sp.zeros(4)
            and isotropic["rank_nonzero_curvature"] == 3
            and isotropic["rank_zero_curvature"] == 0,
        )
    ]

    print("\n[2] Anisotropic causal-type gate")
    print("  P^0_0 =", anisotropic["time_mixed_eigenvalue"])
    print("  sum-of-squares form =", anisotropic["time_mixed_sum_of_squares"])
    print("  example P^{00} =", anisotropic["time_contravariant_example"])
    print("  auxiliary velocity Hessian =", anisotropic["auxiliary_velocity_hessian_example"])
    print("  eigenvalues =", anisotropic["auxiliary_velocity_hessian_eigenvalues"])
    checks.append(
        _check(
            "generic spatial Ricci anisotropy activates a ghost-signed time block",
            anisotropic["time_mixed_eigenvalue_is_sum_of_squares"]
            and anisotropic["auxiliary_velocity_hessian_rank"] == 2
            and anisotropic["auxiliary_velocity_hessian_has_opposite_signs"]
            and anisotropic["isotropic_auxiliary_velocity_hessian_rank"] == 0,
        )
    )

    print("\n[3] Bianchi-I highest metric derivatives")
    print("  tr(S^2) =", bianchi["trace_s_squared"])
    print("  sum_i P^i_i =", bianchi["spatial_projector_trace"])
    print("  acceleration Hessian =", bianchi["acceleration_hessian"])
    print("  shear restriction =", bianchi["shear_hessian"])
    print("  scope =", bianchi["scope"])
    checks.append(
        _check(
            "both physical Bianchi-I shear accelerations have nonzero Hessian",
            bianchi["trace_s_squared_residual"] == 0
            and bianchi["spatial_projector_trace_residual"] == 0
            and bianchi["shear_hessian_rank"] == 2,
        )
    )

    print("\n[4] Reduced higher-derivative shear Dirac closure")
    print("  L_shear =", ostro["lagrangian"])
    print("  acceleration Hessian =", ostro["acceleration_hessian"])
    print("  H_canonical =", ostro["canonical_hamiltonian"])
    print("  primaries =", ostro["primary_constraints"])
    print("  secondaries =", ostro["secondary_constraints"])
    print("  PB matrix =", ostro["poisson_matrix"])
    print("  det(PB)|constraint =", ostro["poisson_determinant_on_constraint_surface"])
    print("  multiplier solution =", ostro["multiplier_solution"])
    print("  first/second class =", ostro["first_class_count"], ostro["second_class_count"])
    print("  physical/baseline/extra DOF =", ostro["physical_dof"], ostro["baseline_shear_dof"], ostro["extra_dof"])
    checks.append(
        _check(
            "the principal shear chain closes with two extra Ostrogradsky modes",
            ostro["poisson_matrix"].rank() == 2
            and ostro["poisson_determinant_on_constraint_surface"] != 0
            and ostro["tertiary_constraints"] == []
            and ostro["extra_dof"] == 2
            and ostro["hamiltonian_linear_in_ostro_momenta"],
        )
    )

    print("\n[5] Effective-stress / Ward fork")
    print("  bare E_chi =", trilemma["bare_chi_equation"])
    print("  bare lambda =", trilemma["bare_multiplier_lambda_solution"])
    print("  with U': lambda =", trilemma["rescued_multiplier_lambda_solution"])
    print("  div(T_m) for J[psi] =", trilemma["direct_matter_source_divergence"])
    print("  div(T_m) for J[g] =", trilemma["metric_only_source_divergence"])
    checks.append(
        _check(
            "bare multiplier has no stress; direct-matter rescue exchanges momentum",
            trilemma["bare_multiplier_lambda_solution"] == 0
            and trilemma["bare_multiplier_on_shell_stress_coefficient"] == 0
            and trilemma["rescued_multiplier_lambda_solution"] != 0
            and trilemma["direct_matter_source_divergence"] != 0
            and trilemma["metric_only_source_divergence"] == 0,
        )
    )

    print("\n[VERDICT]")
    print(" ", result["global_status"])
    print("  The broad regular-projector no-go stays withdrawn. This explicit P fails")
    print("  away from exact isotropy and has two extra higher-derivative shear modes.")
    print("  Bare lambda cannot source Einstein; U(chi) makes lambda nonzero, while")
    print("  J[T(g,psi)] then violates separate ordinary-matter conservation.")
    print("  A nonanalytic exact spectral projector with a metric-only source remains")
    print("  outside this candidate-specific calculation and is therefore OPEN.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
