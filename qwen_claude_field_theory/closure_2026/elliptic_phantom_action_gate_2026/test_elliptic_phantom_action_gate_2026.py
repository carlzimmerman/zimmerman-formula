#!/usr/bin/env python3
"""Regression tests for the variational elliptic-phantom gate."""

from elliptic_phantom_action_gate_2026 import derive_candidate


def test_candidate_derives_exact_exponential_mond_and_a_closed_k_nonzero_dirac_block():
    result = derive_candidate()

    assert result["mond_flux_residual"] == 0
    assert result["k_nonzero"]["primary_constraints"] == len(result["k_nonzero"]["primary_names"])
    assert result["k_nonzero"]["secondary_constraints"] == len(result["k_nonzero"]["secondary_names"])
    assert result["k_nonzero"]["dirac_pb_rank"] == result["k_nonzero"]["dirac_pb_matrix"].rows
    assert result["k_nonzero"]["closure_multipliers"] == (0, 0, 0, 0)


def test_candidate_falsifies_no_slip_conservation_and_homogeneous_flrw_without_hard_coded_verdicts():
    result = derive_candidate()

    assert result["slip"]["radial_stress_coefficient"] != 0
    assert result["ward"]["bare_matter_force_coefficient"] != 0
    assert result["flrw"]["homogeneous_elliptic_residual"] != 0
    assert result["k_zero"]["source_compatible"] is False


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
