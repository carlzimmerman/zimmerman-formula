#!/usr/bin/env python3
"""Audit the action-level meaning of the published AeST phase-pinning claim.

The published calculation correctly identifies the leading small-field
polytropic equation and a positive free-surface family.  This audit asks two
narrower questions which the numerical hydro run does not itself decide:

1. Is the gamma=2 equation exact for K(Q)=K2(Q-Q0)^2?
2. Does the conservative action dynamically select a unique Helmholtz phase,
   or does the observed relaxation use added dissipation at fixed mass?

All algebraic conclusions below are computed.  Source-provenance booleans are
obtained by inspecting the committed simulation rather than assumed.
"""

from __future__ import annotations

import pathlib
import sys
from typing import Any

import sympy as sp


def derive_phase_pinning_audit() -> dict[str, Any]:
    """Return exact EOS, Lane--Emden family, and flow/provenance diagnostics."""

    # Exact k-essence thermodynamics for L=A u^2, u=Q-Q0.
    amplitude, q0, u = sp.symbols("A Q0 u", positive=True, real=True)
    pressure = amplitude * u**2
    density = amplitude * (2 * q0 * u + u**2)
    sound_speed_sq = sp.simplify(sp.diff(pressure, u) / sp.diff(density, u))
    gamma_effective = sp.simplify(
        density / pressure * sp.diff(pressure, u) / sp.diff(density, u)
    )
    gamma_limit = sp.limit(gamma_effective, u, 0, dir="+")
    leading_polytrope = density**2 / (4 * amplitude * q0**2)
    quadratic_eos_residual = sp.factor(pressure - leading_polytrope)

    density_symbol = sp.symbols("rho", nonnegative=True, real=True)
    u_of_density = -q0 + sp.sqrt(q0**2 + density_symbol / amplitude)
    exact_pressure_of_density = sp.simplify(amplitude * u_of_density**2)
    exact_eos_inversion_residual = sp.simplify(
        density.subs(u, u_of_density) - density_symbol
    )

    # Cluster potentials have u/Q0 about |Psi| about 10^-5.  Report the
    # actual error of the leading gamma=2 and pressure laws at that point.
    epsilon = sp.Rational(1, 100000)
    gamma_cluster = sp.simplify(gamma_effective.subs(u, epsilon * q0))
    pressure_ratio_cluster = sp.simplify(
        (pressure / leading_polytrope).subs(u, epsilon * q0)
    )
    cluster_gamma_error = abs(float(sp.N(gamma_cluster - 2, 30)))
    cluster_pressure_ratio_error = abs(float(sp.N(pressure_ratio_cluster - 1, 30)))

    # Positive n=1 Lane--Emden profiles: positivity and the first-zero surface
    # fix the shape/radius but leave central density, hence total mass, free.
    radius, mu, rho_c = sp.symbols("r mu rho_c", positive=True, real=True)
    profile = rho_c * sp.sin(mu * radius) / (mu * radius)
    surface_radius = sp.pi / mu
    total_mass = sp.simplify(
        4 * sp.pi * sp.integrate(radius**2 * profile, (radius, 0, surface_radius))
    )
    mass_derivative = sp.simplify(sp.diff(total_mass, rho_c))
    radius_density_derivative = sp.simplify(sp.diff(surface_radius, rho_c))
    positivity_selects_unique_mass = bool(mass_derivative == 0)

    # Conservative one-mode phase dynamics versus an explicitly dissipative
    # regularization.  A Hamiltonian flow preserves energy and phase-space
    # volume, so a hydrostatic point cannot be a generic attractor.  Damping
    # supplies the missing negative energy derivative and phase-space volume
    # contraction.
    coordinate, momentum, omega, damping = sp.symbols(
        "q p omega nu", positive=True, real=True
    )
    hamiltonian = (momentum**2 + omega**2 * coordinate**2) / 2
    hamiltonian_flow = sp.Matrix([momentum, -omega**2 * coordinate])
    damped_flow = sp.Matrix([momentum, -omega**2 * coordinate - damping * momentum])
    grad_h = sp.Matrix([sp.diff(hamiltonian, coordinate), sp.diff(hamiltonian, momentum)])
    hamiltonian_energy_derivative = sp.simplify((grad_h.T * hamiltonian_flow)[0])
    damped_energy_derivative_symbolic = sp.simplify((grad_h.T * damped_flow)[0])
    hamiltonian_flow_divergence = sp.simplify(
        sp.diff(hamiltonian_flow[0], coordinate) + sp.diff(hamiltonian_flow[1], momentum)
    )
    damped_flow_divergence_symbolic = sp.simplify(
        sp.diff(damped_flow[0], coordinate) + sp.diff(damped_flow[1], momentum)
    )
    hamiltonian_jacobian = hamiltonian_flow.jacobian((coordinate, momentum))
    damped_jacobian = damped_flow.jacobian((coordinate, momentum))
    conservative_eigenvalues = list(hamiltonian_jacobian.eigenvals().keys())
    representative_damped_eigenvalues = list(
        damped_jacobian.subs(damping, omega).eigenvals().keys()
    )

    # Inspect the exact published implementation.  The profile is explicitly
    # rescaled to M_dust and an artificial compression viscosity q is added.
    source_path = pathlib.Path(__file__).with_name("itemC_phase_pinning_dynamics_2026.py")
    source_text = source_path.read_text(encoding="utf-8")
    uses_artificial_viscosity = (
        "artificial viscosity" in source_text
        and "cq=2.0" in source_text
        and "cq*rho*dv**2" in source_text
    )
    renormalizes_each_profile_to_fixed_mass = (
        "m *= M_dust*Msun/m.sum()" in source_text
    )
    action_derived_pin_established = bool(
        not uses_artificial_viscosity
        and not renormalizes_each_profile_to_fixed_mass
        and hamiltonian_flow_divergence < 0
    )

    return {
        "exact_eos": {
            "pressure": pressure,
            "density": density,
            "sound_speed_sq": sound_speed_sq,
            "gamma_effective": gamma_effective,
            "gamma_limit": gamma_limit,
            "leading_polytrope": leading_polytrope,
            "quadratic_eos_residual": quadratic_eos_residual,
            "u_of_density": u_of_density,
            "exact_pressure_of_density": exact_pressure_of_density,
            "exact_eos_inversion_residual": exact_eos_inversion_residual,
            "cluster_gamma": gamma_cluster,
            "cluster_pressure_ratio": pressure_ratio_cluster,
            "cluster_gamma_error": cluster_gamma_error,
            "cluster_pressure_ratio_error": cluster_pressure_ratio_error,
        },
        "positive_family": {
            "profile": profile,
            "surface_radius": surface_radius,
            "total_mass": total_mass,
            "mass_derivative": mass_derivative,
            "surface_radius_density_derivative": radius_density_derivative,
            "surface_radius_depends_on_central_density": bool(radius_density_derivative != 0),
            "positivity_selects_unique_mass": positivity_selects_unique_mass,
        },
        "dynamics": {
            "hamiltonian": hamiltonian,
            "hamiltonian_flow": hamiltonian_flow,
            "damped_flow": damped_flow,
            "hamiltonian_energy_derivative": hamiltonian_energy_derivative,
            "damped_energy_derivative_symbolic": damped_energy_derivative_symbolic,
            "damped_energy_derivative": float(damped_energy_derivative_symbolic.subs({damping: 1, momentum: 1})),
            "hamiltonian_flow_divergence": hamiltonian_flow_divergence,
            "damped_flow_divergence_symbolic": damped_flow_divergence_symbolic,
            "damped_flow_divergence": float(damped_flow_divergence_symbolic.subs(damping, 1)),
            "conservative_eigenvalues": conservative_eigenvalues,
            "representative_damped_eigenvalues": representative_damped_eigenvalues,
        },
        "simulation_provenance": {
            "source_path": str(source_path),
            "uses_artificial_viscosity": uses_artificial_viscosity,
            "renormalizes_each_profile_to_fixed_mass": renormalizes_each_profile_to_fixed_mass,
            "action_derived_pin_established": action_derived_pin_established,
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_phase_pinning_audit()
    eos = result["exact_eos"]
    family = result["positive_family"]
    dynamics = result["dynamics"]
    provenance = result["simulation_provenance"]
    checks = []

    print("=" * 96)
    print("AeST CLUSTER PHASE AUDIT: EXACT EOS, MASS CONTINUUM, AND CONSERVATIVE DYNAMICS")
    print("=" * 96)
    print("\n[1] Exact quadratic-k-essence EOS")
    print("  p(u) =", eos["pressure"])
    print("  rho(u) =", eos["density"])
    print("  c_s^2 =", eos["sound_speed_sq"])
    print("  gamma_eff = d ln p / d ln rho =", eos["gamma_effective"])
    print("  gamma_eff(u->0) =", eos["gamma_limit"])
    print("  exact p(rho) =", eos["exact_pressure_of_density"])
    print("  residual from exact p=K rho^2 =", eos["quadratic_eos_residual"])
    print("  at u/Q0=1e-5: gamma error =", eos["cluster_gamma_error"], "; pressure-law error =", eos["cluster_pressure_ratio_error"])
    checks.append(_check("gamma=2 is the controlled small-field limit", eos["gamma_limit"] == 2 and eos["quadratic_eos_residual"] != 0))
    checks.append(_check("the finite-field correction is negligible at cluster depth", eos["cluster_gamma_error"] < 2e-5 and eos["cluster_pressure_ratio_error"] < 2e-5))

    print("\n[2] Positive Lane--Emden family")
    print("  rho(r) =", family["profile"])
    print("  first-zero radius =", family["surface_radius"])
    print("  total mass =", family["total_mass"])
    print("  dM/d rho_c =", family["mass_derivative"])
    checks.append(_check("positivity fixes the shape and radius but not the captured mass", not family["surface_radius_depends_on_central_density"] and not family["positivity_selects_unique_mass"]))

    print("\n[3] Conservative action flow versus dissipative relaxation")
    print("  H =", dynamics["hamiltonian"])
    print("  dH/dt (Hamiltonian) =", dynamics["hamiltonian_energy_derivative"])
    print("  div flow (Hamiltonian) =", dynamics["hamiltonian_flow_divergence"])
    print("  conservative eigenvalues =", dynamics["conservative_eigenvalues"])
    print("  dH/dt (damped) =", dynamics["damped_energy_derivative_symbolic"])
    print("  div flow (damped) =", dynamics["damped_flow_divergence_symbolic"])
    print("  representative damped eigenvalues =", dynamics["representative_damped_eigenvalues"])
    checks.append(_check("the inviscid action flow has no phase-space contraction or attractor", dynamics["hamiltonian_energy_derivative"] == 0 and dynamics["hamiltonian_flow_divergence"] == 0))
    checks.append(_check("added damping supplies both energy loss and phase-space contraction", dynamics["damped_energy_derivative"] < 0 and dynamics["damped_flow_divergence"] < 0))

    print("\n[4] Published simulation provenance")
    print("  uses artificial viscosity =", provenance["uses_artificial_viscosity"])
    print("  renormalizes every IC profile to fixed M_dust =", provenance["renormalizes_each_profile_to_fixed_mass"])
    print("  action-derived unique pin established =", provenance["action_derived_pin_established"])
    checks.append(_check("the observed numerical relaxation is conditional on explicit viscosity and fixed captured mass", provenance["uses_artificial_viscosity"] and provenance["renormalizes_each_profile_to_fixed_mass"] and not provenance["action_derived_pin_established"]))

    print("\n[VERDICT]")
    print("  The hydrostatic polytrope and its cluster-scale numbers survive: gamma=2 is accurate to")
    print("  O(10^-5).  The stronger dynamical wording does not.  Positivity selects a positive family,")
    print("  not a unique mass, and the published attractor uses non-action artificial viscosity while")
    print("  holding total captured mass fixed.  The defensible statement is CONDITIONAL PINNING:")
    print("  given captured mass and a specified dissipative/UV shock prescription, the flow relaxes")
    print("  near the corresponding positive polytrope.  Action-derived mass selection remains OPEN.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
