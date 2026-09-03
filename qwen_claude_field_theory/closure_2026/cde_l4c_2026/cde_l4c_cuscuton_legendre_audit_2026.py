#!/usr/bin/env python3
"""Audit the cuscuton premise used in the CDE-L4C DOF certificate.

The structural gate inferred a primary constraint from the finite
large-velocity asymptote of the momentum. An asymptote is not degeneracy. The
full momentum is not globally bounded: it diverges at the null boundary. For
the covariant cuscuton density, the Legendre map is invertible when the spatial
gradient is nonzero and becomes degenerate only in the homogeneous sector.
Standard cuscuton nonpropagation can still follow after the complete
gravity-plus-cuscuton constraint analysis; it does not follow from the
candidate's displayed one-variable Hessian argument.

This script also parses the subsequent CDE-L4C rank program and verifies that
its declared phase space omits (chi,p_chi). Therefore that 4x4 matrix is not a
DOF certificate for the same full action.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Any

import sympy as sp


def _assigned_name_list(tree: ast.AST, target_name: str) -> list[str]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == target_name for target in node.targets):
            continue
        if isinstance(node.value, ast.List):
            return [
                element.id
                for element in node.value.elts
                if isinstance(element, ast.Name)
            ]
    raise ValueError(f"assignment {target_name}=[...] not found")


def derive_cuscuton_audit() -> dict[str, Any]:
    """Derive the branch-dependent Legendre map and inspect the certificate."""

    M2, N, spatial_norm, sqrt_gamma, spatial_gradient = sp.symbols(
        "M2 N S sqrt_gamma D_chi", positive=True
    )
    qdot = sp.Symbol("chi_dot", real=True)
    shift = sp.Symbol("N_shift", real=True)
    potential = sp.Symbol("V_chi", real=True)
    normal_velocity = qdot - shift * spatial_gradient
    radicand = normal_velocity**2 - N**2 * spatial_norm

    # sqrt(-g)=N*sqrt(gamma), A=chi_dot-N^i D_i chi, and the timelike
    # branch has A^2>N^2 S. Keep the potential and shift in the Hamiltonian.
    covariant_density = sqrt_gamma * M2 * sp.sqrt(radicand)
    lapse_form = (
        N
        * sqrt_gamma
        * M2
        * sp.sqrt(normal_velocity**2 / N**2 - spatial_norm)
    )
    covariant_density_residual = sp.simplify(covariant_density - lapse_form)
    full_density = covariant_density - N * sqrt_gamma * potential

    momentum = sp.simplify(sp.diff(full_density, qdot))
    velocity_hessian = sp.factor(sp.diff(momentum, qdot))
    momentum_limit = sp.limit(momentum, qdot, sp.oo)

    # The old structural script omitted the ADM measure factor N and the
    # positive sqrt(gamma) density factor. This changes normalization, not the
    # decisive fact that the S>0 Hessian is nonzero.
    old_density = M2 * sp.sqrt(qdot**2 / N**2 - spatial_norm)
    old_momentum = sp.diff(old_density, qdot)
    old_momentum_limit = sp.limit(old_momentum, qdot, sp.oo)
    normalization_mismatch = sp.simplify(momentum_limit - old_momentum_limit)

    # Parameterize the physical timelike domain to establish the Hessian sign
    # without asking SymPy to infer qdot^2>N^2 S.
    timelike_margin = sp.Symbol("u", positive=True)
    hessian_physical = sp.simplify(
        velocity_hessian.subs(
            qdot,
            shift * spatial_gradient
            + N * sp.sqrt(spatial_norm + timelike_margin**2),
        )
    )
    hessian_is_negative = hessian_physical.is_negative is True
    momentum_near_null = sp.simplify(
        momentum.subs(
            qdot,
            shift * spatial_gradient
            + N * sp.sqrt(spatial_norm + timelike_margin**2),
        )
    )
    momentum_near_null_limit = sp.limit(
        momentum_near_null, timelike_margin, 0, dir="+"
    )
    momentum_is_globally_bounded = bool(
        momentum_near_null_limit.is_finite is True
    )

    # Explicit inverse map in the inhomogeneous sector,
    # p^2>gamma*M2^2 on the positive-normal-velocity branch.
    p = sp.Symbol("p_chi", positive=True)
    density_scale_squared = sp.expand((sqrt_gamma * M2) ** 2)
    inverse_velocity = (
        shift * spatial_gradient
        + N
        * p
        * sp.sqrt(spatial_norm)
        / sp.sqrt(p**2 - density_scale_squared)
    )
    inverse_velocity_residual = sp.factor(
        momentum.subs(qdot, inverse_velocity) ** 2 - p**2
    )
    canonical_hamiltonian = sp.simplify(
        (p * qdot - full_density).subs(qdot, inverse_velocity)
    )
    expected_hamiltonian = (
        shift * p * spatial_gradient
        + N * sp.sqrt(spatial_norm) * sp.sqrt(p**2 - density_scale_squared)
        + N * sqrt_gamma * potential
    )
    momentum_margin = sp.Symbol("r_p", positive=True)
    physical_momentum = sp.sqrt(density_scale_squared + momentum_margin**2)
    hamiltonian_residual = sp.simplify(
        (canonical_hamiltonian - expected_hamiltonian).subs(
            p,
            physical_momentum,
        )
    )
    primary_constraint_inhomogeneous = bool(velocity_hessian == 0)

    # Homogeneous branch: S=0. Parameterize positive A explicitly.
    positive_normal_velocity = sp.Symbol("A_positive", positive=True)
    positive_branch = {
        qdot: shift * spatial_gradient + positive_normal_velocity,
        spatial_norm: 0,
    }
    zero_momentum = sp.simplify(momentum.subs(positive_branch))
    zero_hessian = sp.simplify(velocity_hessian.subs(spatial_norm, 0))
    zero_primary = p - sqrt_gamma * M2
    zero_primary_residual = sp.simplify(zero_primary.subs(p, zero_momentum))
    branch_rank_change = bool(
        zero_hessian == 0 and velocity_hessian != 0
    )

    # Algebraic a0(chi)F(y) changes neither branch's velocity Hessian. It also
    # cannot turn a nonzero inhomogeneous Hessian into a primary constraint.
    chi, a0 = sp.symbols("chi a0", real=True)
    algebraic_coupling = sp.Function("U")(chi, a0)
    coupling_hessian_shift = sp.diff(algebraic_coupling, qdot, 2)
    inhomogeneous_hessian_after_coupling = sp.simplify(
        velocity_hessian + coupling_hessian_shift
    )
    nonpropagation_certified = bool(
        inhomogeneous_hessian_after_coupling == 0
    )

    # Parse the actual follow-on certificate rather than trusting its prose.
    certificate_path = (
        Path(__file__).resolve().parent
        / "gateA"
        / "cde_l4c_covariant_dirac_rank.py"
    )
    certificate_tree = ast.parse(certificate_path.read_text(encoding="utf-8"))
    coordinate_names = _assigned_name_list(certificate_tree, "Q")
    momentum_names = _assigned_name_list(certificate_tree, "Pm")
    contains_chi = "chi" in coordinate_names
    contains_p_chi = "p_chi" in momentum_names or "pchi" in momentum_names
    full_action_dof_certified = contains_chi and contains_p_chi

    # Rebuild the displayed four-constraint subsystem and expose its missed
    # determinant-zero surface and unproven momentum-constraint closure.
    Phi, pPhi, Psi, pPsi, B_field, pB, lam, plam = sp.symbols(
        "Phi pPhi Psi pPsi B pB lambda p_lambda", real=True
    )
    coordinates = [Phi, Psi, B_field, lam]
    momenta = [pPhi, pPsi, pB, plam]

    def pb(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sum(
                sp.diff(left, q) * sp.diff(right, mom)
                - sp.diff(left, mom) * sp.diff(right, q)
                for q, mom in zip(coordinates, momenta)
            )
        )

    wave_number = sp.Symbol("k_mode", positive=True)
    longitudinal = sp.Symbol("L_parallel", positive=True)
    a0_squared = sp.Symbol("a0_squared", positive=True)
    B_p = sp.Symbol("B_p", real=True)
    c_s = sp.Symbol("c_s", nonzero=True, real=True)
    rho_b, K0 = sp.symbols("rho_b K0", real=True)
    p_N = pPhi
    c_slip = c_s * wave_number * (Phi - Psi)
    c_K = pPsi - K0
    c_mond = (
        longitudinal * a0_squared * wave_number * Phi
        + B_p * wave_number * (Phi + Psi)
        + pPsi
        + rho_b
    )
    rank_constraints = [p_N, c_mond, c_K, c_slip]
    rank_matrix = sp.Matrix(
        [
            [pb(left, right) for right in rank_constraints]
            for left in rank_constraints
        ]
    )
    rank_determinant = sp.factor(rank_matrix.det())
    cancellation_substitution = {
        B_p: -longitudinal * a0_squared / 2
    }
    cancellation_matrix = sp.simplify(
        rank_matrix.subs(cancellation_substitution)
    )
    momentum_constraint = wave_number * (pPsi - pB)
    momentum_constraint_brackets = [
        pb(momentum_constraint, constraint) for constraint in rank_constraints
    ]
    momentum_first_class_certified = all(
        bracket == 0 for bracket in momentum_constraint_brackets
    )

    return {
        "adm": {
            "M2": M2,
            "N": N,
            "S": spatial_norm,
            "sqrt_gamma": sqrt_gamma,
            "spatial_gradient": spatial_gradient,
            "shift": shift,
            "potential": potential,
            "normal_velocity": normal_velocity,
            "covariant_density": covariant_density,
            "full_density": full_density,
            "lapse_form": lapse_form,
            "covariant_density_residual": covariant_density_residual,
            "momentum": momentum,
            "momentum_limit": momentum_limit,
            "momentum_near_null": momentum_near_null,
            "momentum_near_null_limit": momentum_near_null_limit,
            "momentum_is_globally_bounded": momentum_is_globally_bounded,
            "old_script_density": old_density,
            "old_script_momentum_limit": old_momentum_limit,
            "normalization_mismatch": normalization_mismatch,
        },
        "k!=0": {
            "velocity_hessian": velocity_hessian,
            "hessian_on_timelike_domain": hessian_physical,
            "velocity_hessian_is_negative": hessian_is_negative,
            "primary_constraint_exists_from_cuscuton_alone": primary_constraint_inhomogeneous,
            "inverse_velocity": inverse_velocity,
            "inverse_velocity_residual": inverse_velocity_residual,
            "hamiltonian": canonical_hamiltonian,
            "expected_hamiltonian": expected_hamiltonian,
            "shift": shift,
            "potential": potential,
            "physical_momentum_parameterization": physical_momentum,
            "hamiltonian_residual": hamiltonian_residual,
        },
        "k=0": {
            "momentum": zero_momentum,
            "velocity_hessian": zero_hessian,
            "primary_constraint": zero_primary,
            "primary_constraint_residual": zero_primary_residual,
        },
        "branch_rank_change": branch_rank_change,
        "a0_coupling": {
            "lagrangian_term": algebraic_coupling,
            "velocity_hessian_shift": coupling_hessian_shift,
            "inhomogeneous_hessian_after_coupling": inhomogeneous_hessian_after_coupling,
            "nonpropagation_certified": nonpropagation_certified,
        },
        "certificate_audit": {
            "path": str(certificate_path),
            "coordinate_names": coordinate_names,
            "momentum_names": momentum_names,
            "declared_phase_space_pairs": len(coordinate_names),
            "contains_chi": contains_chi,
            "contains_p_chi": contains_p_chi,
            "full_action_dof_certified": full_action_dof_certified,
            "name_presence_is_only_a_necessary_test": True,
        },
        "certificate_rank_surface": {
            "matrix": rank_matrix,
            "determinant": rank_determinant,
            "generic_rank": rank_matrix.rank(),
            "cancellation_substitution": cancellation_substitution,
            "cancellation_matrix": cancellation_matrix,
            "cancellation_rank": cancellation_matrix.rank(),
            "B_p": B_p,
            "L_parallel": longitudinal,
            "a0_squared": a0_squared,
            "c_s": c_s,
            "k": wave_number,
            "momentum_constraint": momentum_constraint,
            "momentum_constraint_brackets": momentum_constraint_brackets,
            "momentum_first_class_certified": momentum_first_class_certified,
            "mond_constraint_provenance": (
                "assigned principal surrogate, not derived from one frozen nonlinear action"
            ),
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_cuscuton_audit()
    adm = result["adm"]
    finite = result["k!=0"]
    zero = result["k=0"]
    coupling = result["a0_coupling"]
    certificate = result["certificate_audit"]
    rank_surface = result["certificate_rank_surface"]

    print("=" * 96)
    print("CDE-L4C CUSCUTON LEGENDRE-MAP / CERTIFICATE AUDIT")
    print("=" * 96)

    print("\n[1] Correct ADM density")
    print("  L_cusc,kin =", adm["covariant_density"])
    print("  lapse-form residual =", adm["covariant_density_residual"])
    print("  p_chi =", adm["momentum"])
    print("  large-velocity lim p_chi =", adm["momentum_limit"])
    print("  null-boundary lim p_chi =", adm["momentum_near_null_limit"])
    print("  old no-measure limit =", adm["old_script_momentum_limit"])
    checks = [
        _check(
            "the full ADM density fixes normalization but the momentum is not globally bounded",
            adm["covariant_density_residual"] == 0
            and adm["momentum_limit"] == adm["sqrt_gamma"] * adm["M2"]
            and adm["normalization_mismatch"] != 0
            and adm["momentum_near_null_limit"].is_infinite
            and not adm["momentum_is_globally_bounded"],
        )
    ]

    print("\n[2] Inhomogeneous branch")
    print("  d p_chi/d chi_dot =", finite["velocity_hessian"])
    print("  on chi_dot=N*sqrt(S+u^2):", finite["hessian_on_timelike_domain"])
    print("  inverse chi_dot(p) =", finite["inverse_velocity"])
    print("  H_cusc =", finite["hamiltonian"])
    checks.append(
        _check(
            "for S>0 the Hessian is nonzero/negative and the velocity is invertible",
            finite["velocity_hessian"] != 0
            and finite["velocity_hessian_is_negative"]
            and not finite["primary_constraint_exists_from_cuscuton_alone"]
            and finite["inverse_velocity_residual"] == 0,
        )
    )
    checks.append(
        _check(
            "the Legendre transform includes the shift, density factor, and potential",
            finite["hamiltonian_residual"] == 0,
        )
    )

    print("\n[3] Homogeneous branch")
    print("  p_chi(S=0) =", zero["momentum"])
    print("  Hessian(S=0) =", zero["velocity_hessian"])
    print("  primary =", zero["primary_constraint"])
    checks.append(
        _check(
            "only S=0 has the displayed primary constraint; the Hessian rank changes",
            zero["velocity_hessian"] == 0
            and zero["primary_constraint_residual"] == 0
            and result["branch_rank_change"],
        )
    )

    print("\n[4] Algebraic a0 coupling")
    print("  Hessian shift =", coupling["velocity_hessian_shift"])
    print("  total inhomogeneous Hessian =", coupling["inhomogeneous_hessian_after_coupling"])
    checks.append(
        _check(
            "a0(chi)F(y) preserves the Hessian but does not manufacture an inhomogeneous primary",
            coupling["velocity_hessian_shift"] == 0
            and coupling["inhomogeneous_hessian_after_coupling"] != 0
            and not coupling["nonpropagation_certified"],
        )
    )

    print("\n[5] Parse the advertised 4x4 rank certificate")
    print("  Q =", certificate["coordinate_names"])
    print("  P =", certificate["momentum_names"])
    print("  contains chi,p_chi =", certificate["contains_chi"], certificate["contains_p_chi"])
    checks.append(
        _check(
            "the rank certificate omits (chi,p_chi), so it does not count the displayed full action",
            certificate["declared_phase_space_pairs"] == 4
            and not certificate["contains_chi"]
            and not certificate["contains_p_chi"]
            and not certificate["full_action_dof_certified"],
        )
    )

    print("\n[6] Hidden determinant and momentum-constraint surfaces")
    print("  Delta =", rank_surface["matrix"])
    print("  det Delta =", rank_surface["determinant"])
    print("  cancellation =", rank_surface["cancellation_substitution"])
    print("  rank(generic,cancellation) =", rank_surface["generic_rank"], rank_surface["cancellation_rank"])
    print("  H_mom brackets =", rank_surface["momentum_constraint_brackets"])
    checks.append(
        _check(
            "the displayed subsystem drops from rank four to two on its cancellation surface",
            rank_surface["generic_rank"] == 4
            and rank_surface["cancellation_rank"] == 2
            and rank_surface["determinant"].subs(
                rank_surface["cancellation_substitution"]
            )
            == 0,
        )
    )
    checks.append(
        _check(
            "the displayed nonzero H_mom brackets do not certify first-class closure",
            rank_surface["momentum_constraint_brackets"] != [0, 0, 0, 0]
            and not rank_surface["momentum_first_class_certified"],
        )
    )

    print("\n[VERDICT]")
    print("  CERTIFICATE REFUTED, CANDIDATE NOT YET FALSIFIED.")
    print("  A finite large-velocity momentum asymptote is not a primary constraint;")
    print("  the momentum actually diverges at the null boundary for D_i chi != 0.")
    print("  Standard cuscuton nonpropagation requires the complete coupled Dirac")
    print("  analysis. The current CDE-L4C 4x4 matrix omits that canonical pair,")
    print("  has an unreported rank-2 surface, and does not establish H_mom closure.")
    print("  No single nonlinear action/four-constraint set is frozen in the directory;")
    print("  N_grav=2 is OPEN for the same explicit action, not established.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
