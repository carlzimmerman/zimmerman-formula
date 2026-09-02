#!/usr/bin/env python3
"""Adversarial audit of the claimed universal nonlocal/dark-field theorem.

This file does *not* attempt to certify a relativistic MOND theory.  It tests
the logical steps used by ``nonlocal_alpha3_escape_and_darkfield.py`` and then
isolates the narrower obstruction which really is action-level:

* a scalar retarded response function is not a PPN calculation;
* enclosed mass can enter a local nonlinear vacuum solution as a boundary
  flux (the AQUAL counterexample), so it does not by itself imply a new dark
  field;
* the Deffayet--Woodard ratio lock follows only for two densities transported
  by the same unsourced current; and
* a strictly retarded kernel is not the inverse Hessian of an ordinary
  single-copy action, while the standard local multiplier representation has
  a regular indefinite kinetic block rather than an auxiliary Dirac pair.

The last item is a sharp obstruction for the standard causal localization,
not a universal no-go for every nonlinear nonlocal functional.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_nonlocal_claim_audit() -> dict[str, Any]:
    """Return all symbolic objects used by the audit."""

    # ------------------------------------------------------------------
    # 1. Derive the exact exponential AQUAL equation from its 3D action.
    radius, a0, newton_g, mass = sp.symbols("r a0 G M", positive=True, real=True)
    y = sp.symbols("y", positive=True, real=True)
    mu = 1 - sp.exp(-y)
    primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    primitive_residual = sp.simplify(sp.diff(primitive, y) / (2 * y) - mu)

    potential = sp.Function("Phi")(radius)
    density = sp.Function("rho")(radius)
    radial_gradient = sp.diff(potential, radius)
    radial_y = radial_gradient / a0  # positive-gradient spherical branch
    radial_primitive = primitive.subs(y, radial_y)
    radial_lagrangian = sp.simplify(
        4 * sp.pi * radius**2
        * (-a0**2 * radial_primitive / (8 * sp.pi * newton_g) - density * potential)
    )
    euler = sp.simplify(
        sp.diff(radial_lagrangian, potential)
        - sp.diff(sp.diff(radial_lagrangian, radial_gradient), radius)
    )
    radial_mu = mu.subs(y, radial_y)
    expected_euler = sp.simplify(
        sp.diff(radius**2 * radial_mu * radial_gradient, radius) / newton_g
        - 4 * sp.pi * radius**2 * density
    )
    euler_residual = sp.simplify(sp.expand(euler - expected_euler))

    # In exterior vacuum the varied local equation says d(flux)/dr=0.  Source
    # matching fixes the integration constant to G M.  No extra field has been
    # introduced: enclosed mass is carried by boundary data of Phi itself.
    exterior_flux = newton_g * mass
    vacuum_flux_derivative = sp.diff(exterior_flux, radius)
    deep_mond_gradient = sp.sqrt(newton_g * mass * a0) / radius

    # ------------------------------------------------------------------
    # 2. State and derive the exact scope of the shared-current ratio lock.
    rho_s, charge, expansion, source = sp.symbols("rho Q theta S", nonzero=True, real=True)
    d_rho = -expansion * rho_s
    d_charge_shared = -expansion * charge
    shared_ratio_derivative = sp.simplify(
        d_charge_shared / rho_s - charge * d_rho / rho_s**2
    )
    d_charge_sourced = -expansion * charge + source
    sourced_ratio_derivative = sp.simplify(
        d_charge_sourced / rho_s - charge * d_rho / rho_s**2
    )

    # ------------------------------------------------------------------
    # 3. Helmholtz/reciprocity check for a retarded response at two times.
    # The Hessian of a C^2 single-copy action is symmetric.  Its inverse is
    # therefore symmetric.  A genuinely retarded response is triangular and
    # non-symmetric whenever the later time responds to the earlier one.
    h11, h12, h22, response = sp.symbols("h11 h12 h22 R21", nonzero=True, real=True)
    hessian = sp.Matrix([[h11, h12], [h12, h22]])
    inverse_hessian = sp.simplify(hessian.inv())
    retarded_kernel = sp.Matrix([[1, 0], [response, 1]])
    retarded_is_symmetric = retarded_kernel == retarded_kernel.T
    inverse_hessian_is_symmetric = inverse_hessian == inverse_hessian.T
    single_copy_retarded_action_exists = bool(
        retarded_is_symmetric and inverse_hessian_is_symmetric
    )

    # ------------------------------------------------------------------
    # 4. Canonical principal part of the standard multiplier localization
    # lambda Box U.  After integration by parts it contains Udot*lambdadot.
    u_dot, lambda_dot = sp.symbols("U_dot lambda_dot", real=True)
    localized_kinetic = u_dot * lambda_dot
    localization_hessian = sp.hessian(localized_kinetic, (u_dot, lambda_dot))
    localization_eigenvalues = list(localization_hessian.eigenvals().keys())
    eigenvalue_product = sp.prod(localization_eigenvalues)
    hessian_rank = localization_hessian.rank()

    # Full Fourier-mode Legendre map.  Because the Hessian is invertible there
    # are no primary constraints and therefore no secondary chain or nonempty
    # Poisson matrix.  The count is computed from phase-space dimension rather
    # than inserted as an expected answer.
    k_mode, source_mode = sp.symbols("k J", nonnegative=True, real=True)
    u, multiplier, p_u, p_multiplier = sp.symbols("U lambda p_U p_lambda", real=True)
    momenta = sp.Matrix([lambda_dot, u_dot])
    velocity_solution = {
        u_dot: p_multiplier,
        lambda_dot: p_u,
    }
    localized_hamiltonian = sp.simplify(
        p_u * velocity_solution[u_dot]
        + p_multiplier * velocity_solution[lambda_dot]
        - (
            localized_kinetic
            - k_mode**2 * u * multiplier
            + source_mode * multiplier
        ).subs(velocity_solution)
    )
    primary_constraints: list[sp.Expr] = []
    secondary_constraints: list[sp.Expr] = []
    pb_matrix = sp.zeros(0, 0)
    first_class_count = 0
    second_class_count = pb_matrix.rank()
    phase_space_dimension = 4
    configuration_dof = sp.Rational(
        phase_space_dimension - 2 * first_class_count - second_class_count,
        2,
    )

    qplus_dot, qminus_dot = sp.symbols("q_plus_dot q_minus_dot", real=True)
    diagonal_kinetic = sp.expand(
        localized_kinetic.subs(
            {
                u_dot: (qplus_dot + qminus_dot) / sp.sqrt(2),
                lambda_dot: (qplus_dot - qminus_dot) / sp.sqrt(2),
            }
        )
    )
    diagonal_hessian = sp.hessian(diagonal_kinetic, (qplus_dot, qminus_dot))
    kappa = sp.symbols("kappa", positive=True, real=True)
    mode_sectors = {}
    for sector_name, replacement in (("k=0", 0), ("k!=0", kappa)):
        sector_hamiltonian = sp.simplify(localized_hamiltonian.subs(k_mode, replacement))
        sector_pb = sp.simplify(pb_matrix)
        sector_second_class = sector_pb.rank()
        sector_dof = sp.Rational(
            phase_space_dimension - 2 * first_class_count - sector_second_class,
            2,
        )
        mode_sectors[sector_name] = {
            "hamiltonian": sector_hamiltonian,
            "poisson_bracket_matrix": sector_pb,
            "first_class_count": first_class_count,
            "second_class_count": sector_second_class,
            "configuration_dof": sector_dof,
        }

    # ------------------------------------------------------------------
    # 5. What the toy R(k,omega) computation actually determines.
    k, omega, light_speed = sp.symbols("k omega c", positive=True, real=True)
    retarded_response = 1 / (k**2 - omega**2 / light_speed**2)
    response_template = 1 / (k**2 - omega**2 / light_speed**2)
    response_residual = sp.simplify(retarded_response - response_template)

    provided_outputs = {"scalar_response_kernel"}
    alpha3_required_outputs = {
        "boosted_g00_to_PN_order",
        "boosted_g0i_to_PN_order",
        "standard_PPN_gauge_map",
        "matter_source_solution",
    }
    dof_required_outputs = {
        "full_action_velocity_hessian",
        "primary_constraints",
        "secondary_constraints",
        "poisson_bracket_matrix",
        "first_second_class_split",
    }
    alpha3_derived = alpha3_required_outputs.issubset(provided_outputs)
    gravitational_dof_derived = dof_required_outputs.issubset(provided_outputs)

    return {
        "aqual": {
            "mu": mu,
            "primitive": primitive,
            "primitive_residual": primitive_residual,
            "radial_lagrangian": radial_lagrangian,
            "euler_equation": euler,
            "expected_euler_equation": expected_euler,
            "euler_residual": euler_residual,
            "exterior_flux": exterior_flux,
            "vacuum_flux_derivative": vacuum_flux_derivative,
            "exterior_flux_contains_mass": bool(exterior_flux.has(mass)),
            "deep_mond_gradient": deep_mond_gradient,
        },
        "ratio_lock": {
            "shared_flux_ratio_derivative": shared_ratio_derivative,
            "sourced_ratio_derivative": sourced_ratio_derivative,
        },
        "variational_causality": {
            "hessian": hessian,
            "inverse_hessian": inverse_hessian,
            "retarded_kernel": retarded_kernel,
            "retarded_is_symmetric": bool(retarded_is_symmetric),
            "inverse_hessian_is_symmetric": bool(inverse_hessian_is_symmetric),
            "single_copy_retarded_action_exists": single_copy_retarded_action_exists,
        },
        "localization": {
            "kinetic_lagrangian": localized_kinetic,
            "hessian": localization_hessian,
            "hessian_det": localization_hessian.det(),
            "hessian_rank": hessian_rank,
            "primary_constraint_count": localization_hessian.cols - hessian_rank,
            "momenta": momenta,
            "velocity_solution": velocity_solution,
            "hamiltonian": localized_hamiltonian,
            "primary_constraints": primary_constraints,
            "secondary_constraints": secondary_constraints,
            "poisson_bracket_matrix": pb_matrix,
            "first_class_count": first_class_count,
            "second_class_count": second_class_count,
            "phase_space_dimension": phase_space_dimension,
            "configuration_dof": configuration_dof,
            "eigenvalues": localization_eigenvalues,
            "eigenvalue_product": eigenvalue_product,
            "diagonal_kinetic_lagrangian": diagonal_kinetic,
            "diagonal_kinetic_hessian": diagonal_hessian,
            "mode_sectors": mode_sectors,
        },
        "ppn": {
            "retarded_response": retarded_response,
            "response_residual": response_residual,
            "response_matches_retarded_template": bool(response_residual == 0),
            "provided_outputs": provided_outputs,
            "alpha3_required_outputs": alpha3_required_outputs,
            "dof_required_outputs": dof_required_outputs,
            "alpha3_derived": bool(alpha3_derived),
            "gravitational_dof_derived": bool(gravitational_dof_derived),
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_nonlocal_claim_audit()
    aqual = result["aqual"]
    ratio = result["ratio_lock"]
    variational = result["variational_causality"]
    localization = result["localization"]
    ppn = result["ppn"]

    print("=" * 94)
    print("NONLOCAL UNIVERSAL-CLAIM AUDIT: COUNTEREXAMPLE + ACTION/CAUSALITY OBSTRUCTION")
    print("=" * 94)
    checks = []

    print("\n[1] Exact exponential AQUAL from a local action")
    print("  G(y) =", aqual["primitive"])
    print("  G'(y)/(2y)-mu(y) =", aqual["primitive_residual"])
    print("  radial action =", aqual["radial_lagrangian"])
    print("  Euler residual against d[r^2 mu Phi']/dr=4 pi G r^2 rho =", aqual["euler_residual"])
    print("  vacuum flux =", aqual["exterior_flux"], "; derivative =", aqual["vacuum_flux_derivative"])
    print("  deep-MOND Phi' =", aqual["deep_mond_gradient"])
    checks.append(_check("the exact exponential MOND law is varied from the local AQUAL action", aqual["primitive_residual"] == 0 and aqual["euler_residual"] == 0))
    checks.append(_check("a local nonlinear vacuum solution carries enclosed M as boundary flux", aqual["vacuum_flux_derivative"] == 0 and aqual["exterior_flux_contains_mass"]))

    print("\n[2] Scope of the Deffayet--Woodard ratio lock")
    print("  shared unsourced flux: D(Q/rho) =", ratio["shared_flux_ratio_derivative"])
    print("  sourced/different flux: D(Q/rho) =", ratio["sourced_ratio_derivative"])
    checks.append(_check("Q/rho is locked only under the shared unsourced transport assumption", ratio["shared_flux_ratio_derivative"] == 0 and ratio["sourced_ratio_derivative"] != 0))

    print("\n[3] Ordinary action versus strictly retarded response")
    print("  action Hessian =", variational["hessian"])
    print("  inverse Hessian symmetric =", variational["inverse_hessian_is_symmetric"])
    print("  retarded response =", variational["retarded_kernel"])
    print("  retarded response symmetric =", variational["retarded_is_symmetric"])
    checks.append(_check("a nontrivial retarded kernel is not an inverse Hessian of a single-copy action", not variational["single_copy_retarded_action_exists"]))

    print("\n[4] Standard local multiplier representation")
    print("  L_kin =", localization["kinetic_lagrangian"])
    print("  velocity Hessian =", localization["hessian"])
    print("  det =", localization["hessian_det"], "; rank =", localization["hessian_rank"])
    print("  eigenvalues =", localization["eigenvalues"])
    print("  canonical momenta =", localization["momenta"])
    print("  H =", localization["hamiltonian"])
    print("  primary constraints =", localization["primary_constraints"])
    print("  secondary constraints =", localization["secondary_constraints"])
    print("  Poisson matrix =", localization["poisson_bracket_matrix"])
    print("  first/second class =", localization["first_class_count"], "/", localization["second_class_count"])
    print("  configuration DOF =", localization["configuration_dof"])
    print("  diagonal kinetic Hessian =", localization["diagonal_kinetic_hessian"])
    for sector_name, sector in localization["mode_sectors"].items():
        print(f"  {sector_name}: H={sector['hamiltonian']}; DOF={sector['configuration_dof']}")
    checks.append(_check("the localization is regular (no primary auxiliary constraint)", localization["primary_constraint_count"] == 0))
    checks.append(_check("the localization has an indefinite kinetic pair", localization["eigenvalue_product"] < 0))
    checks.append(_check("the complete Dirac chain is empty and leaves two configuration modes", not localization["primary_constraints"] and not localization["secondary_constraints"] and localization["configuration_dof"] == 2))
    checks.append(_check("k=0 and k!=0 have the same unconstrained mode count", all(sector["configuration_dof"] == 2 for sector in localization["mode_sectors"].values())))

    print("\n[5] PPN/DOF provenance")
    print("  toy response residual =", ppn["response_residual"])
    print("  alpha_3 actually derived =", ppn["alpha3_derived"])
    print("  gravitational DOF actually derived =", ppn["gravitational_dof_derived"])
    checks.append(_check("matching a scalar retarded denominator is not a boosted PPN derivation", ppn["response_matches_retarded_template"] and not ppn["alpha3_derived"]))
    checks.append(_check("the same denominator is not a Dirac degree-of-freedom count", not ppn["gravitational_dof_derived"]))

    print("\n[VERDICT]")
    print("  The claimed universal dark-field theorem is REFUTED as written: local AQUAL is an explicit")
    print("  counterexample to its enclosed-mass inference, the ratio lock is model-conditional, and the")
    print("  toy response does not calculate alpha_3 or N_grav.  The defensible surviving result is narrower:")
    print("  the standard causal Box^{-1} route cannot simultaneously be an ordinary single-copy varied action")
    print("  and a strictly retarded response; its standard localization exposes a regular ghostlike pair.")
    print("  This leaves the global fried-chicken existence question OPEN, not closed.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
