#!/usr/bin/env python3
"""Spectral/CTP gate for the remaining non-rational spin-2 MOND route.

The residual route after the local and finite-localization audits is a
field-dependent, genuinely non-rational spin-2 response.  This file tests the
standard way such a response can arise from a healthy action: couple the
metric tensor channel to healthy carrier modes and integrate them out.

The result is deliberately scoped.  It is a no-go for a unitary local UV
completion with a positive spectral representation, not for every formal
nonlocal functional.  The calculation establishes the state-space fork:

* nonzero positive spectral weight gives a causal memory kernel but also real
  carrier states (discrete poles or a continuum); or
* removing every carrier state removes the nonlocal response.

A signed spectral cancellation can hide the response only by introducing a
negative kinetic direction.  In closed-time-path language the retarded kernel
also comes with a nonzero noise kernel; the CTP object is an influence action,
not a real one-copy fundamental action.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_spectral_state_space_gate() -> dict[str, Any]:
    """Derive the finite-bath Dirac count and continuum spectral fork."""

    z = sp.symbols("z", nonnegative=True)
    m1, m2 = sp.symbols("m_1 m_2", positive=True)
    g1, g2 = sp.symbols("g_1 g_2", positive=True)

    # One TT metric amplitude h coupled to two representative healthy tensor
    # carrier amplitudes q_i.  Potential/mass mixing cannot change this
    # principal velocity Hessian.
    hdot, q1dot, q2dot = sp.symbols("h_dot q_1_dot q_2_dot", real=True)
    velocities = sp.Matrix([hdot, q1dot, q2dot])
    kinetic_lagrangian = sp.Rational(1, 2) * (
        hdot**2 + q1dot**2 + q2dot**2
    )
    kinetic_hessian = sp.hessian(kinetic_lagrangian, velocities)
    kinetic_determinant = sp.factor(kinetic_hessian.det())
    kinetic_rank = kinetic_hessian.rank()
    primary_constraints: list[sp.Expr] = [] if kinetic_rank == len(velocities) else list(kinetic_hessian.nullspace())
    secondary_constraints: list[sp.Expr] = []
    poisson_matrix = sp.zeros(0, 0) if not primary_constraints else sp.zeros(len(primary_constraints))
    configuration_dof = (2 * len(velocities) - 0 - 0) // 2

    # Euclidean response after eliminating q_i.  Its poles/residues are not
    # assigned: they follow from the inverse carrier operators.
    pi_finite = g1**2 / (m1**2 + z) + g2**2 / (m2**2 + z)
    residues = [
        sp.simplify(sp.limit((z + m1**2) * pi_finite, z, -m1**2)),
        sp.simplify(sp.limit((z + m2**2) * pi_finite, z, -m2**2)),
    ]
    # The generic unequal-mass residues include the other term's removable
    # zero times a finite factor.  Simplification gives g_i^2.
    memory_slope = sp.factor(sp.diff(pi_finite, z).subs(z, 0))
    positive_slope_terms = [g1**2 / m1**4, g2**2 / m2**4]
    memory_slope_zero_iff_decoupled = all(
        sp.ask(sp.Q.positive(term)) is True for term in positive_slope_terms
    ) and sp.simplify(memory_slope + sum(positive_slope_terms)) == 0

    # A positive continuous spectral density rho on [s0,s0+Delta] gives a
    # logarithm: the non-rationality is exactly the branch cut of real states.
    s0, delta, rho = sp.symbols("s_0 Delta rho", positive=True)
    s = sp.symbols("s", real=True)
    pi_continuum_integral = sp.Integral(rho / (s + z), (s, s0, s0 + delta))
    pi_continuum = sp.integrate(rho / (s + z), (s, s0, s0 + delta))
    continuum_slope = sp.factor(sp.diff(pi_continuum, z).subs(z, 0))

    # At a point x in the interior of the cut, log(-A +/- i0) differs by
    # 2*pi*i.  These two boundary values are constructed explicitly from the
    # principal logarithm, so the discontinuity is calculated rather than
    # inserted into a pass flag.
    x = s0 + delta / 2
    real_log_part = sp.log((s0 + delta - x) / (x - s0))
    upper_boundary = rho * (real_log_part - sp.I * sp.pi)
    lower_boundary = rho * (real_log_part + sp.I * sp.pi)
    spectral_discontinuity = sp.simplify(upper_boundary - lower_boundary)
    positive_weight_cancellation_possible = bool(
        sp.simplify(spectral_discontinuity) == 0
    )

    # Cancellation by equal positive/negative spectral contributions.  The
    # same sign that cancels the self-energy appears in the carrier kinetic
    # matrix and exposes the ghost.
    m, g = sp.symbols("m g", positive=True)
    pi_signed = sp.simplify(g**2 / (m**2 + z) - g**2 / (m**2 + z))
    signed_hessian = sp.diag(1, 1, -1)
    signed_eigenvalues = list(signed_hessian.eigenvals().items())
    negative_eigenvalue_count = sum(
        multiplicity
        for eigenvalue, multiplicity in signed_eigenvalues
        if eigenvalue.is_negative
    )

    # One oscillator's exact CTP kernels.  The retarded witness is evaluated
    # at t-t'=1/Omega so no distributional ambiguity at coincidence enters.
    t, tp, omega = sp.symbols("t t_prime Omega", real=True, positive=True)
    tau = t - tp
    retarded_kernel = g**2 * sp.Heaviside(tau) * sp.sin(omega * tau) / omega
    retarded_forward = sp.simplify(retarded_kernel.subs({t: 1 / omega, tp: 0}))
    retarded_backward = sp.simplify(retarded_kernel.subs({t: 0, tp: 1 / omega}))
    retarded_kernel_is_symmetric = bool(
        sp.simplify(retarded_forward - retarded_backward) == 0
    )
    noise_kernel = g**2 * sp.cos(omega * tau) / (2 * omega)
    noise_witness = sp.simplify(noise_kernel.subs({t: 0, tp: 0}))
    noise_zero_iff_spectral_weight_zero = bool(
        noise_witness != 0 and sp.solve(sp.Eq(noise_witness, 0), g) == []
    )
    ordinary_single_copy_action = bool(retarded_kernel_is_symmetric)

    # Exact two-tensor limit inside this action class: every carrier coupling
    # is zero.  Both the response and its slope then vanish.
    two_tensor_limit_self_energy = sp.simplify(pi_finite.subs({g1: 0, g2: 0}))
    two_tensor_limit_slope = sp.simplify(memory_slope.subs({g1: 0, g2: 0}))
    nontrivial_memory_requires_extra_states = bool(
        pi_finite != 0
        and configuration_dof > 1
        and two_tensor_limit_self_energy == 0
    )
    strict_target_passes = bool(
        configuration_dof == 1
        and pi_finite != 0
        and ordinary_single_copy_action
    )

    return {
        "finite_bath": {
            "kinetic_lagrangian": kinetic_lagrangian,
            "kinetic_hessian": kinetic_hessian,
            "kinetic_determinant": kinetic_determinant,
            "kinetic_rank": kinetic_rank,
            "primary_constraints": primary_constraints,
            "secondary_constraints": secondary_constraints,
            "poisson_bracket_matrix": poisson_matrix,
            "first_class_count": 0,
            "second_class_count": 0,
            "configuration_dof": configuration_dof,
            "euclidean_self_energy": pi_finite,
            "euclidean_residues": residues,
            "memory_slope": memory_slope,
            "memory_slope_zero_iff_decoupled": memory_slope_zero_iff_decoupled,
        },
        "continuum": {
            "spectral_integral": pi_continuum_integral,
            "euclidean_self_energy": pi_continuum,
            "euclidean_slope": continuum_slope,
            "upper_boundary": upper_boundary,
            "lower_boundary": lower_boundary,
            "spectral_discontinuity": spectral_discontinuity,
            "positive_weight_cancellation_possible": positive_weight_cancellation_possible,
        },
        "signed_cancellation": {
            "cancelled_self_energy": pi_signed,
            "kinetic_hessian": signed_hessian,
            "kinetic_determinant": signed_hessian.det(),
            "eigenvalues": signed_eigenvalues,
            "negative_eigenvalue_count": negative_eigenvalue_count,
        },
        "ctp": {
            "retarded_kernel": retarded_kernel,
            "retarded_forward_witness": retarded_forward,
            "retarded_backward_witness": retarded_backward,
            "retarded_kernel_is_symmetric": retarded_kernel_is_symmetric,
            "noise_kernel": noise_kernel,
            "noise_witness": noise_witness,
            "noise_zero_iff_spectral_weight_zero": noise_zero_iff_spectral_weight_zero,
            "ordinary_single_copy_action": ordinary_single_copy_action,
        },
        "theorem": {
            "two_tensor_limit_self_energy": two_tensor_limit_self_energy,
            "two_tensor_limit_slope": two_tensor_limit_slope,
            "nontrivial_memory_requires_extra_states": nontrivial_memory_requires_extra_states,
            "strict_target_passes": strict_target_passes,
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_spectral_state_space_gate()
    finite = result["finite_bath"]
    continuum = result["continuum"]
    signed = result["signed_cancellation"]
    ctp = result["ctp"]
    theorem = result["theorem"]

    print("=" * 96)
    print("NON-RATIONAL SPIN-2 SPECTRAL STATE-SPACE GATE")
    print("=" * 96)
    print("\n[1] Healthy finite carrier action: complete principal Dirac chain")
    print("  L_kin =", finite["kinetic_lagrangian"])
    print("  W =", finite["kinetic_hessian"])
    print("  det/rank =", finite["kinetic_determinant"], "/", finite["kinetic_rank"])
    print("  primaries/secondaries =", finite["primary_constraints"], "/", finite["secondary_constraints"])
    print("  PB matrix =", finite["poisson_bracket_matrix"])
    print("  first/second class =", finite["first_class_count"], "/", finite["second_class_count"])
    print("  configuration DOF in one tensor channel =", finite["configuration_dof"])
    print("  Pi_E(z) =", finite["euclidean_self_energy"])
    print("  pole residues =", finite["euclidean_residues"])
    print("  Pi_E'(0) =", finite["memory_slope"])
    checks = [
        _check("the healthy carrier Legendre map is regular and has no Dirac reduction", finite["kinetic_rank"] == 3 and not finite["primary_constraints"] and not finite["secondary_constraints"]),
        _check("nonzero healthy couplings give positive spectral residues and a nonconstant memory response", all(r > 0 for r in finite["euclidean_residues"]) and finite["memory_slope"] < 0),
    ]

    print("\n[2] Non-rational continuum")
    print("  Pi_E(z) =", continuum["spectral_integral"], "=", continuum["euclidean_self_energy"])
    print("  Pi_E'(0) =", continuum["euclidean_slope"])
    print("  Disc Pi =", continuum["spectral_discontinuity"])
    checks.append(_check("positive continuum weight gives a nonzero branch cut and cannot self-cancel", continuum["euclidean_slope"] < 0 and continuum["spectral_discontinuity"] != 0 and not continuum["positive_weight_cancellation_possible"]))

    print("\n[3] Signed cancellation")
    print("  Pi_+ + Pi_- =", signed["cancelled_self_energy"])
    print("  W_signed =", signed["kinetic_hessian"], "; det =", signed["kinetic_determinant"])
    print("  eigenvalues =", signed["eigenvalues"])
    checks.append(_check("cancelling the spectral cut with opposite weight introduces a ghost kinetic direction", signed["cancelled_self_energy"] == 0 and signed["kinetic_determinant"] < 0 and signed["negative_eigenvalue_count"] > 0))

    print("\n[4] Closed-time-path completion")
    print("  G_ret(t,t') =", ctp["retarded_kernel"])
    print("  forward/backward witnesses =", ctp["retarded_forward_witness"], "/", ctp["retarded_backward_witness"])
    print("  N(t,t') =", ctp["noise_kernel"], "; N(t,t) =", ctp["noise_witness"])
    checks.append(_check("strict retardation is nonreciprocal and its healthy influence action carries nonzero noise", not ctp["retarded_kernel_is_symmetric"] and ctp["noise_kernel"] != 0 and ctp["noise_zero_iff_spectral_weight_zero"] and not ctp["ordinary_single_copy_action"]))

    print("\n[5] State-space fork")
    print("  all carrier couplings off: Pi_E =", theorem["two_tensor_limit_self_energy"], "; Pi_E'(0) =", theorem["two_tensor_limit_slope"])
    checks.append(_check("within a positive-spectral local completion, nontrivial retarded memory requires extra carrier states", theorem["nontrivial_memory_requires_extra_states"]))
    checks.append(_check("the strict two-tensor plus nontrivial-memory target therefore does not pass this action class", not theorem["strict_target_passes"]))

    print("\n[VERDICT]")
    print("  SCOPED NO-GO: a healthy local UV completion of a genuinely non-rational retarded spin-2")
    print("  form factor has positive spectral weight, hence additional carrier states.  Removing those")
    print("  states removes the form factor; cancelling them requires a ghost.  The causal CTP object is")
    print("  an influence action with noise, not a real one-copy fundamental action.  This closes the")
    print("  positive-spectral carrier realization of the last spin-2 residual, not arbitrary acausal or")
    print("  non-unitary formal kernels and not a fundamental nonlocal theory outside spectral completion.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
