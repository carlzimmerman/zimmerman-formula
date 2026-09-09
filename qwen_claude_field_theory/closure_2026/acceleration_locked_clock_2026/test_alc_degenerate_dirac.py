#!/usr/bin/env python3
"""Tests for the exact-luminal ADM/Dirac gate."""

from alc_degenerate_dirac import derive_gate


def test_adm_contractions_are_derived_not_assumed():
    result = derive_gate()
    assert result["adm"]["decomposition_residual"] == 0
    assert result["scalar_dirac"]["coefficient_residual"] == 0


def test_exact_luminal_branch_splits_instantaneous_from_degenerate():
    result = derive_gate()
    assert result["adm"]["density_ho_exact_luminal_and_c123_zero"] == 0
    scalar = result["scalar_dirac"]
    assert scalar["pb_rank_exact_luminal_c123_nonzero"] == 2
    assert scalar["secondary_degenerate"] == 0
    assert scalar["pb_rank_degenerate"] == 0
    assert scalar["L_zero_mode"] == 0
    assert scalar["zero_mode_constraint_count"] == 1


def test_exponential_kernel_is_exact_and_has_finite_background_hessian():
    result = derive_gate()["exponential"]
    assert result["flux_residual"] == 0
    assert result["finite_y_hessian_nonzero"] != 0
    assert result["longitudinal_positive_transform"] != 0
    assert result["ALC_H_hessian_at_y_half"] < 0
    assert result["ALC_H_hessian_at_y_two"] > 0


if __name__ == "__main__":
    tests = [value for name, value in globals().items()
             if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
