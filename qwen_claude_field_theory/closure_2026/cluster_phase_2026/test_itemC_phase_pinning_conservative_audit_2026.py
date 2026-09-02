#!/usr/bin/env python3
"""Regression tests for the action-versus-dissipation audit of item C."""

from itemC_phase_pinning_conservative_audit_2026 import derive_phase_pinning_audit


def test_gamma_two_is_a_controlled_leading_limit_not_an_exact_eos():
    result = derive_phase_pinning_audit()
    eos = result["exact_eos"]

    assert eos["gamma_limit"] == 2
    assert eos["quadratic_eos_residual"] != 0
    assert eos["cluster_gamma_error"] < 2e-5
    assert eos["cluster_pressure_ratio_error"] < 2e-5


def test_positive_lane_emden_branch_remains_a_mass_continuum():
    result = derive_phase_pinning_audit()
    family = result["positive_family"]

    assert family["surface_radius_depends_on_central_density"] is False
    assert family["mass_derivative"] != 0
    assert family["positivity_selects_unique_mass"] is False


def test_inviscid_action_flow_has_no_attractor_but_damped_flow_can_relax():
    result = derive_phase_pinning_audit()
    dynamics = result["dynamics"]

    assert dynamics["hamiltonian_energy_derivative"] == 0
    assert dynamics["hamiltonian_flow_divergence"] == 0
    assert dynamics["damped_energy_derivative"] < 0
    assert dynamics["damped_flow_divergence"] < 0


def test_published_numerical_pin_uses_artificial_viscosity_at_fixed_mass():
    result = derive_phase_pinning_audit()
    provenance = result["simulation_provenance"]

    assert provenance["uses_artificial_viscosity"] is True
    assert provenance["renormalizes_each_profile_to_fixed_mass"] is True
    assert provenance["action_derived_pin_established"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
