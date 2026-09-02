#!/usr/bin/env python3
"""Regression tests for the non-rational spin-2 spectral state-space gate."""

import sympy as sp

from spectral_state_space_gate_2026 import derive_spectral_state_space_gate


def test_healthy_finite_bath_has_no_dirac_reduction():
    result = derive_spectral_state_space_gate()
    finite = result["finite_bath"]

    assert finite["kinetic_determinant"] != 0
    assert finite["kinetic_rank"] == 3
    assert finite["primary_constraints"] == []
    assert finite["secondary_constraints"] == []
    assert finite["configuration_dof"] == 3


def test_nontrivial_finite_memory_has_positive_spectral_residues():
    result = derive_spectral_state_space_gate()
    finite = result["finite_bath"]

    assert all(residue > 0 for residue in finite["euclidean_residues"])
    assert finite["memory_slope"] < 0
    assert finite["memory_slope_zero_iff_decoupled"]


def test_positive_continuum_has_branch_cut_and_cannot_cancel_itself():
    result = derive_spectral_state_space_gate()
    continuum = result["continuum"]

    assert continuum["euclidean_slope"] < 0
    assert continuum["spectral_discontinuity"] != 0
    assert continuum["positive_weight_cancellation_possible"] is False


def test_signed_cancellation_requires_a_ghost_direction():
    result = derive_spectral_state_space_gate()
    signed = result["signed_cancellation"]

    assert signed["cancelled_self_energy"] == 0
    assert signed["kinetic_determinant"] < 0
    assert signed["negative_eigenvalue_count"] == 1


def test_ctp_retardation_has_noise_when_spectral_weight_is_nonzero():
    result = derive_spectral_state_space_gate()
    ctp = result["ctp"]

    assert ctp["retarded_kernel_is_symmetric"] is False
    assert ctp["noise_kernel"] != 0
    assert ctp["noise_zero_iff_spectral_weight_zero"]
    assert ctp["ordinary_single_copy_action"] is False


def test_two_tensor_limit_erases_the_nonlocal_response():
    result = derive_spectral_state_space_gate()
    theorem = result["theorem"]

    assert theorem["two_tensor_limit_self_energy"] == 0
    assert theorem["two_tensor_limit_slope"] == 0
    assert theorem["nontrivial_memory_requires_extra_states"]
    assert theorem["strict_target_passes"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
