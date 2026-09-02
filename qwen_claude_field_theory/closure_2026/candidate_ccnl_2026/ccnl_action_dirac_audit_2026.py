#!/usr/bin/env python3
"""Action-level audit of the condensate-clock nonlocal MOND candidate.

The candidate localizes a causal response with a scalar ``X`` and multiplier
``xi``.  This audit deliberately separates three logically different objects:

* the exact static constitutive map, which is valid;
* the ordinary localized action, whose canonical variables must be counted;
* a strict retarded history prescription, which is boundary data rather than
  a Dirac constraint on one Cauchy slice.

No expected rank, degree-of-freedom count, slip value, or PPN parameter is
inserted.  They are calculated from the displayed principal Lagrangian and
from an explicit inventory of the equations needed for a PPN extraction.
"""

from __future__ import annotations

import pathlib
import sys
from typing import Any

import sympy as sp


def derive_ccnl_action_audit() -> dict[str, Any]:
    """Return the symbolic kernel, Dirac, causality, slip, and provenance audit."""

    # ------------------------------------------------------------------
    # Exact positive-Z constitutive function proposed by CCNL.
    z, y = sp.symbols("Z y", positive=True, real=True)
    f_exp = 4 - 2 * (sp.sqrt(z) + 2) * sp.exp(-sp.sqrt(z) / 2)
    mu = sp.simplify((1 - 2 * sp.diff(f_exp, z)).subs(z, 4 * y**2))
    mu_target = 1 - sp.exp(-y)
    mu_residual = sp.simplify(mu - mu_target)
    deep_mond_residual = sp.simplify(sp.limit(mu / y, y, 0, dir="+") - 1)
    newtonian_limit = sp.limit(mu, y, sp.oo)

    # ------------------------------------------------------------------
    # Canonical principal part of the ordinary local representation.
    # After integrating xi Box X by parts, the most general X self-kinetic
    # coefficient A does not affect the determinant of the mixed block.
    coefficient_a = sp.symbols("A", real=True)
    mixing_b = sp.symbols("b", positive=True, real=True)
    x_dot, xi_dot = sp.symbols("X_dot xi_dot", real=True)
    kinetic_lagrangian = (
        coefficient_a * x_dot**2 / 2 + mixing_b * x_dot * xi_dot
    )
    hessian = sp.hessian(kinetic_lagrangian, (x_dot, xi_dot))
    hessian_det = sp.factor(hessian.det())
    hessian_rank = hessian.rank()
    kinetic_eigenvalues = list(hessian.eigenvals().keys())
    eigenvalue_product = sp.factor(sp.expand(sp.prod(kinetic_eigenvalues)))
    # For the displayed CCNL sign, a0^2 f(Z) with
    # Z=4[-Xdot^2+(grad X)^2]/a0^2 and f'(4y^2)=exp(-y)/2 gives
    # A(y)=-8 f'=-4 exp(-y).  The normalization of xi Box X sets b=1.
    candidate_self_kinetic = -4 * sp.exp(-y)
    candidate_hessian = sp.simplify(
        hessian.subs({coefficient_a: candidate_self_kinetic, mixing_b: 1})
    )
    candidate_hessian_det = sp.factor(candidate_hessian.det())
    candidate_hessian_rank = candidate_hessian.rank()
    candidate_eigenvalues = list(candidate_hessian.eigenvals().keys())
    candidate_eigenvalue_product = sp.factor(
        sp.expand(sp.prod(candidate_eigenvalues))
    )

    # Perform the Legendre transform for a Fourier mode.  The inversion is
    # calculated, so an empty primary list follows from the full-rank Hessian.
    x_mode, xi_mode = sp.symbols("X xi", real=True)
    p_x, p_xi = sp.symbols("p_X p_xi", real=True)
    k, source = sp.symbols("k J", nonnegative=True, real=True)
    mode_lagrangian = (
        coefficient_a * (x_dot**2 - k**2 * x_mode**2) / 2
        + mixing_b * (x_dot * xi_dot - k**2 * x_mode * xi_mode)
        + source * xi_mode
    )
    momenta = sp.Matrix(
        [sp.diff(mode_lagrangian, x_dot), sp.diff(mode_lagrangian, xi_dot)]
    )
    velocity_solution_raw = sp.solve(
        [sp.Eq(p_x, momenta[0]), sp.Eq(p_xi, momenta[1])],
        (x_dot, xi_dot),
        dict=True,
    )
    velocity_solution = velocity_solution_raw[0]
    hamiltonian = sp.factor(
        p_x * velocity_solution[x_dot]
        + p_xi * velocity_solution[xi_dot]
        - mode_lagrangian.subs(velocity_solution)
    )
    primary_constraints: list[sp.Expr] = [] if hessian_rank == 2 else [sp.nan]
    secondary_constraints: list[sp.Expr] = []
    poisson_matrix = sp.zeros(0, 0)
    first_class_count = 0
    second_class_count = poisson_matrix.rank()
    phase_space_dimension = 4
    configuration_dof = sp.Rational(
        phase_space_dimension - 2 * first_class_count - second_class_count, 2
    )

    kappa = sp.symbols("kappa", positive=True, real=True)
    mode_sectors = {}
    for name, replacement in (("k=0", 0), ("k!=0", kappa)):
        sector_hamiltonian = sp.simplify(hamiltonian.subs(k, replacement))
        sector_pb = sp.simplify(poisson_matrix)
        sector_second_class = sector_pb.rank()
        sector_dof = sp.Rational(
            phase_space_dimension - 2 * first_class_count - sector_second_class,
            2,
        )
        mode_sectors[name] = {
            "hamiltonian": sector_hamiltonian,
            "poisson_bracket_matrix": sector_pb,
            "first_class_count": first_class_count,
            "second_class_count": sector_second_class,
            "configuration_dof": sector_dof,
        }

    # Homogeneous metric mixing from the same integrated action.  The
    # xi R_uu term contributes -3 a^2 adot xidot and changes the Einstein
    # coefficient to -6 a(1+xi) adot^2; it does not make the block degenerate.
    scale_factor = sp.symbols("a", positive=True, real=True)
    multiplier_background = sp.symbols("xi_bg", real=True)
    scale_dot = sp.symbols("a_dot", real=True)
    minisuperspace_kinetic = (
        -6 * scale_factor * (1 + multiplier_background) * scale_dot**2
        - 3 * scale_factor**2 * scale_dot * xi_dot
        + scale_factor**3 * x_dot * xi_dot
        - 2 * scale_factor**3 * sp.exp(-y) * x_dot**2
    )
    minisuperspace_hessian = sp.hessian(
        minisuperspace_kinetic, (scale_dot, x_dot, xi_dot)
    )
    minisuperspace_determinant = sp.factor(minisuperspace_hessian.det())
    expected_minisuperspace_determinant = sp.factor(
        12
        * scale_factor**7
        * (1 + multiplier_background + 3 * sp.exp(-y))
    )
    determinant_residual = sp.simplify(
        minisuperspace_determinant - expected_minisuperspace_determinant
    )
    background_hessian = sp.simplify(
        minisuperspace_hessian.subs(multiplier_background, 0)
    )
    background_determinant = sp.factor(background_hessian.det())
    background_rank = background_hessian.rank()

    # Euler equations show the two wave equations carried by the regular pair.
    x_ddot, xi_ddot = sp.symbols("X_ddot xi_ddot", real=True)
    x_equation = sp.expand(
        coefficient_a * (x_ddot + k**2 * x_mode)
        + mixing_b * (xi_ddot + k**2 * xi_mode)
    )
    xi_equation = sp.expand(mixing_b * (x_ddot + k**2 * x_mode) - source)

    # ------------------------------------------------------------------
    # Ordinary action reciprocity versus a strict retarded response.
    h11, h12, h22, response = sp.symbols(
        "h11 h12 h22 R21", nonzero=True, real=True
    )
    ordinary_hessian = sp.Matrix([[h11, h12], [h12, h22]])
    ordinary_inverse = sp.simplify(ordinary_hessian.inv())
    retarded_kernel = sp.Matrix([[1, 0], [response, 1]])
    ordinary_inverse_is_symmetric = ordinary_inverse == ordinary_inverse.T
    retarded_kernel_is_symmetric = retarded_kernel == retarded_kernel.T
    # Retarded/null data restrict histories at an initial boundary.  With no
    # primary constraints above, they are not functions vanishing on each
    # equal-time phase space and generate no Dirac preservation chain.
    retarded_history_is_phase_space_constraint = bool(primary_constraints)

    # ------------------------------------------------------------------
    # Exact translation of Deffayet--Woodard eq. (33): along a flow tube,
    # n(M+f) is conserved.  Setting M_0=0 does not erase the homogeneous
    # transport constant when f_0 is nonzero.
    flow_density, initial_flow_density = sp.symbols(
        "n n_0", positive=True, real=True
    )
    f_value, initial_f_value = sp.symbols("f f_0", nonzero=True, real=True)
    transport_constant = initial_flow_density * initial_f_value
    zero_m_initial_solution = sp.simplify(
        transport_constant / flow_density - f_value
    )
    transport_residual = sp.simplify(
        flow_density * (zero_m_initial_solution + f_value)
        - initial_flow_density * initial_f_value
    )
    minus_f_residual = sp.simplify(zero_m_initial_solution + f_value)
    m_equals_minus_f_generically = bool(minus_f_residual == 0)

    # ------------------------------------------------------------------
    # Exact trace-free stress from the spatial X gradient.  It is second order
    # in weak fields but nonzero at every finite MOND y because f'(4y^2)>0.
    gradient, f_prime = sp.symbols("g_X f_prime", positive=True, real=True)
    vector = sp.Matrix([gradient, 0, 0])
    identity3 = sp.eye(3)
    trace_free_source = sp.simplify(
        f_prime
        * (vector * vector.T - identity3 * (vector.dot(vector)) / 3)
    )
    trace_free_source_norm_sq = sp.factor(
        sum(trace_free_source[i, j] ** 2 for i in range(3) for j in range(3))
    )
    exact_no_slip = bool(trace_free_source_norm_sq == 0)

    # ------------------------------------------------------------------
    # PPN provenance: a suppression estimate is not a boosted 1PN solution.
    provided_outputs = {
        "static_constitutive_function",
        "solar_system_exponential_estimate",
        "clock_density_order_of_magnitude",
        "vacuum_tt_ricci_check",
    }
    beta_required_outputs = {
        "second_order_g00_solution",
        "nonlinear_auxiliary_backreaction",
        "standard_ppn_gauge_map",
    }
    preferred_frame_required_outputs = {
        "boosted_g00_solution",
        "boosted_g0i_solution",
        "boosted_gij_solution",
        "matter_source_solution",
        "standard_ppn_gauge_map",
    }
    beta_derived = beta_required_outputs.issubset(provided_outputs)
    preferred_frame_parameters_derived = preferred_frame_required_outputs.issubset(
        provided_outputs
    )

    # ------------------------------------------------------------------
    # The code's negative-Z extension is odd in the positive branch.  It is C1
    # but not C2 at Z=0, so the exact zero-field perturbation Hessian diverges.
    z_real = sp.symbols("z", real=True)
    f_plus = 4 - 2 * (sp.sqrt(z_real) + 2) * sp.exp(-sp.sqrt(z_real) / 2)
    f_minus = -(
        4 - 2 * (sp.sqrt(-z_real) + 2) * sp.exp(-sp.sqrt(-z_real) / 2)
    )
    right_value = sp.limit(f_plus, z_real, 0, dir="+")
    left_value = sp.limit(f_minus, z_real, 0, dir="-")
    right_first = sp.limit(sp.diff(f_plus, z_real), z_real, 0, dir="+")
    left_first = sp.limit(sp.diff(f_minus, z_real), z_real, 0, dir="-")
    right_second = sp.limit(sp.diff(f_plus, z_real, 2), z_real, 0, dir="+")
    left_second = sp.limit(sp.diff(f_minus, z_real, 2), z_real, 0, dir="-")
    infinite_set = {sp.oo, -sp.oo, sp.zoo, sp.nan}
    finite_second_derivative = bool(
        right_second == left_second
        and right_second not in infinite_set
        and left_second not in infinite_set
    )

    # Source provenance is diagnostic only.  It is derived by inspecting the
    # live proposal and never used to establish the canonical theorem.
    proposal_path = pathlib.Path(__file__).with_name("ccnl_mond_gates_2026.py")
    proposal_text = (
        proposal_path.read_text(encoding="utf-8") if proposal_path.exists() else ""
    )
    provenance = {
        "proposal_path": str(proposal_path),
        "proposal_exists": proposal_path.exists(),
        "contains_or_true": "or True" in proposal_text,
        "asserts_alpha3_by_structure": "alpha_3 = 0 by structure" in proposal_text,
        "admits_boosted_ppn_is_owed": "full boosted-PPN extraction" in proposal_text,
        "admits_localization_direction_is_open": "nonlinear re-excitation" in proposal_text,
    }

    return {
        "kernel": {
            "f_exp": f_exp,
            "mu": mu,
            "mu_target": mu_target,
            "mu_residual": mu_residual,
            "deep_mond_residual": deep_mond_residual,
            "newtonian_limit": newtonian_limit,
        },
        "localization": {
            "kinetic_lagrangian": kinetic_lagrangian,
            "hessian": hessian,
            "hessian_det": hessian_det,
            "hessian_rank": hessian_rank,
            "kinetic_eigenvalues": kinetic_eigenvalues,
            "eigenvalue_product": eigenvalue_product,
            "candidate_self_kinetic": candidate_self_kinetic,
            "candidate_hessian": candidate_hessian,
            "candidate_hessian_det": candidate_hessian_det,
            "candidate_hessian_rank": candidate_hessian_rank,
            "candidate_eigenvalues": candidate_eigenvalues,
            "candidate_eigenvalue_product": candidate_eigenvalue_product,
            "momenta": momenta,
            "velocity_solution": velocity_solution,
            "hamiltonian": hamiltonian,
            "primary_constraints": primary_constraints,
            "secondary_constraints": secondary_constraints,
            "poisson_bracket_matrix": poisson_matrix,
            "first_class_count": first_class_count,
            "second_class_count": second_class_count,
            "configuration_dof": configuration_dof,
            "mode_sectors": mode_sectors,
            "x_equation": x_equation,
            "xi_equation": xi_equation,
        },
        "minisuperspace": {
            "kinetic_lagrangian": minisuperspace_kinetic,
            "hessian": minisuperspace_hessian,
            "determinant": minisuperspace_determinant,
            "expected_determinant": expected_minisuperspace_determinant,
            "determinant_residual": determinant_residual,
            "background_hessian": background_hessian,
            "background_determinant": background_determinant,
            "background_rank": background_rank,
        },
        "variational_causality": {
            "ordinary_hessian": ordinary_hessian,
            "ordinary_inverse_hessian": ordinary_inverse,
            "retarded_kernel": retarded_kernel,
            "ordinary_inverse_hessian_is_symmetric": bool(
                ordinary_inverse_is_symmetric
            ),
            "retarded_kernel_is_symmetric": bool(retarded_kernel_is_symmetric),
            "retarded_history_is_phase_space_constraint": retarded_history_is_phase_space_constraint,
        },
        "dw_transport": {
            "transport_constant": transport_constant,
            "zero_M_initial_solution": zero_m_initial_solution,
            "transport_residual": transport_residual,
            "minus_f_residual": minus_f_residual,
            "M_equals_minus_f_generically": m_equals_minus_f_generically,
        },
        "slip": {
            "trace_free_source": trace_free_source,
            "trace_free_source_norm_sq": trace_free_source_norm_sq,
            "exact_no_slip": exact_no_slip,
        },
        "ppn_provenance": {
            "provided_outputs": provided_outputs,
            "beta_required_outputs": beta_required_outputs,
            "preferred_frame_required_outputs": preferred_frame_required_outputs,
            "beta_derived": bool(beta_derived),
            "preferred_frame_parameters_derived": bool(
                preferred_frame_parameters_derived
            ),
        },
        "zero_field": {
            "right_value": right_value,
            "left_value": left_value,
            "right_first_derivative": right_first,
            "left_first_derivative": left_first,
            "right_second_derivative": right_second,
            "left_second_derivative": left_second,
            "value_continuous": bool(right_value == left_value),
            "first_derivative_continuous": bool(right_first == left_first),
            "finite_second_derivative": finite_second_derivative,
        },
        "source_provenance": provenance,
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_ccnl_action_audit()
    kernel = result["kernel"]
    local = result["localization"]
    mini = result["minisuperspace"]
    causal = result["variational_causality"]
    transport = result["dw_transport"]
    slip = result["slip"]
    ppn = result["ppn_provenance"]
    zero = result["zero_field"]
    provenance = result["source_provenance"]
    checks = []

    print("=" * 96)
    print("CCNL ACTION AUDIT: CONSTITUTIVE PASS, LOCALIZED DIRAC FAILURE")
    print("=" * 96)

    print("\n[1] Exact exponential kernel")
    print("  f_exp(Z) =", kernel["f_exp"])
    print("  mu(y) =", kernel["mu"])
    checks.append(_check("the varied static coefficient is exactly 1-exp(-y)", kernel["mu_residual"] == 0))
    checks.append(_check("deep-MOND and Newtonian limits are exact", kernel["deep_mond_residual"] == 0 and kernel["newtonian_limit"] == 1))

    print("\n[2] Ordinary localized action: full auxiliary Legendre map")
    print("  L_kin =", local["kinetic_lagrangian"])
    print("  W =", local["hessian"])
    print("  det(W) =", local["hessian_det"], "; rank =", local["hessian_rank"])
    print("  eigenvalues =", local["kinetic_eigenvalues"])
    print("  product =", local["eigenvalue_product"])
    print("  CCNL A(y) =", local["candidate_self_kinetic"])
    print("  CCNL W(y) =", local["candidate_hessian"])
    print("  CCNL det/rank =", local["candidate_hessian_det"], "/", local["candidate_hessian_rank"])
    print("  CCNL eigenvalues =", local["candidate_eigenvalues"])
    print("  momenta =", local["momenta"])
    print("  velocities =", local["velocity_solution"])
    print("  H =", local["hamiltonian"])
    print("  primaries =", local["primary_constraints"])
    print("  secondaries =", local["secondary_constraints"])
    print("  PB matrix =", local["poisson_bracket_matrix"])
    print("  first/second class =", local["first_class_count"], "/", local["second_class_count"])
    print("  auxiliary configuration DOF =", local["configuration_dof"])
    print("  delta X equation =", local["x_equation"])
    print("  delta xi equation =", local["xi_equation"])
    for name, sector in local["mode_sectors"].items():
        print(f"  {name}: H={sector['hamiltonian']}; DOF={sector['configuration_dof']}")
    checks.append(_check("the localization is regular and has no primary/secondary auxiliary constraints", local["hessian_rank"] == 2 and not local["primary_constraints"] and not local["secondary_constraints"]))
    checks.append(_check("the kinetic pair is indefinite for every nonzero multiplier coupling", local["hessian_det"] < 0 and local["eigenvalue_product"] < 0))
    checks.append(_check("the actual exponential CCNL Hessian has determinant -1 and rank 2 at every finite y", local["candidate_hessian_det"] == -1 and local["candidate_hessian_rank"] == 2 and local["candidate_eigenvalue_product"] == -1))
    checks.append(_check("both k=0 and k!=0 sectors retain two auxiliary configuration modes", all(sector["configuration_dof"] == 2 for sector in local["mode_sectors"].values())))

    print("\n[3] Homogeneous metric--auxiliary kinetic mixing")
    print("  L_kin,FLRW =", mini["kinetic_lagrangian"])
    print("  W_FLRW =", mini["hessian"])
    print("  det(W_FLRW) =", mini["determinant"])
    print("  xi_bg=0 determinant/rank =", mini["background_determinant"], "/", mini["background_rank"])
    checks.append(_check("including the homogeneous metric velocity leaves a rank-3 block on the xi=0 branch", mini["determinant_residual"] == 0 and mini["background_determinant"] > 0 and mini["background_rank"] == 3))

    print("\n[4] Retarded prescription versus action Hessian")
    print("  ordinary inverse Hessian =", causal["ordinary_inverse_hessian"])
    print("  retarded two-time kernel =", causal["retarded_kernel"])
    print("  retarded history is an equal-time Dirac constraint =", causal["retarded_history_is_phase_space_constraint"])
    checks.append(_check("strict retardation is not the inverse Hessian of an ordinary one-copy action", causal["ordinary_inverse_hessian_is_symmetric"] and not causal["retarded_kernel_is_symmetric"]))
    checks.append(_check("retarded/null history data do not generate a Dirac reduction", not causal["retarded_history_is_phase_space_constraint"]))

    print("\n[5] Deffayet--Woodard transport equation")
    print("  conserved flow-tube quantity =", transport["transport_constant"])
    print("  M for M_0=0 =", transport["zero_M_initial_solution"])
    print("  residual from M=-f =", transport["minus_f_residual"])
    checks.append(_check("M_0=0 gives M=-f only when the initial f_0 contribution vanishes", transport["transport_residual"] == 0 and transport["minus_f_residual"] != 0 and not transport["M_equals_minus_f_generically"]))

    print("\n[6] Slip and PPN provenance")
    print("  TF stress =", slip["trace_free_source"])
    print("  ||TF stress||^2 =", slip["trace_free_source_norm_sq"])
    print("  exact Phi=Psi derived =", slip["exact_no_slip"])
    print("  beta derived =", ppn["beta_derived"])
    print("  alpha_1, alpha_2, alpha_3 derived =", ppn["preferred_frame_parameters_derived"])
    checks.append(_check("the finite-y kernel has nonzero second-order anisotropic stress, so exact no slip is not established", slip["trace_free_source_norm_sq"] != 0 and not slip["exact_no_slip"]))
    checks.append(_check("suppression estimates do not supply beta or the preferred-frame PPN parameters", not ppn["beta_derived"] and not ppn["preferred_frame_parameters_derived"]))

    print("\n[7] Zero-field continuation")
    print("  f(0+), f(0-) =", zero["right_value"], zero["left_value"])
    print("  f'(0+), f'(0-) =", zero["right_first_derivative"], zero["left_first_derivative"])
    print("  f''(0+), f''(0-) =", zero["right_second_derivative"], zero["left_second_derivative"])
    checks.append(_check("the odd continuation is C1 but not C2 at Z=0", zero["value_continuous"] and zero["first_derivative_continuous"] and not zero["finite_second_derivative"]))

    print("\n[8] Live proposal provenance")
    for key, value in provenance.items():
        print(f"  {key} = {value}")
    if provenance["proposal_exists"]:
        checks.append(_check("the live proposal asserts alpha_3 structurally while admitting a localization-sector calculation remains owed", provenance["asserts_alpha3_by_structure"] and provenance["admits_localization_direction_is_open"]))
    else:
        print("  [INFO] proposal source absent; supplementary provenance checks skipped")

    print("\n[VERDICT]")
    print("  The exact exponential static constitutive law survives.  The displayed ordinary localized")
    print("  action does not satisfy the strict target: its X-xi Legendre map is invertible, its complete")
    print("  auxiliary Dirac chain is empty, and it carries two auxiliary configuration modes with one")
    print("  negative kinetic direction in both k sectors.  Retarded/null data are history conditions,")
    print("  not action-derived phase-space constraints.  Exact nonlinear no slip and preferred-frame PPN")
    print("  are also uncomputed.  CCNL is DEAD as the claimed ordinary localized action; a genuinely")
    print("  nonlocal in-in construction with a demonstrated physical phase space remains OPEN.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
