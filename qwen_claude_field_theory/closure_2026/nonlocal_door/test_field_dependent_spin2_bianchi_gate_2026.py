#!/usr/bin/env python3
"""Tests for the curvature-dependent spin-2 completion gate."""

from field_dependent_spin2_bianchi_gate_2026 import derive_bianchi_gate


def test_naive_field_dependent_einstein_multiplier_is_not_conserved():
    result = derive_bianchi_gate()

    assert result["naive_multiplier"]["bianchi_residual"] != 0


def test_action_completion_has_scalar_trace_and_no_slip_requires_constant_f_r():
    result = derive_bianchi_gate()

    assert result["f_r_action"]["scalar_kinetic_coefficient"] != 0
    assert result["weak_field"]["no_slip_tf_source"] != 0
    assert result["weak_field"]["constant_f_r_implies"] is True


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
