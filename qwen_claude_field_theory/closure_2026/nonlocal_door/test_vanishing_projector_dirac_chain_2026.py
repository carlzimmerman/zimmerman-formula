#!/usr/bin/env python3
"""Regression tests for the vanishing-projector Dirac-chain correction."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


SCRIPT = Path(__file__).with_name("vanishing_projector_dirac_chain_2026.py")


def _load_script_module():
    """Load the legacy script even before its top-level exit is guarded."""

    spec = importlib.util.spec_from_file_location(
        "vanishing_projector_dirac_chain_2026", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except SystemExit as exc:
        assert exc.code == 0
    return module


def test_ppn_status_requires_a_boosted_metric_solution_not_an_instantaneous_denominator():
    """Catches reintroduction of a PPN value from the static auxiliary response."""

    module = _load_script_module()
    audit = module.derive_ppn_provenance_audit()

    assert audit["boosted_ppn_complete"] is False
    assert audit["boosted_ppn_status"] == "UNCOMPUTED"
    assert audit["alpha_1"] == "UNCOMPUTED"
    assert audit["alpha_2"] == "UNCOMPUTED"
    assert audit["alpha_3"] == "UNCOMPUTED"
    assert audit["missing_outputs"] == audit["required_outputs"]


def test_zero_field_equation_loses_rank_while_linear_source_scaling_keeps_a_path_dependent_limit():
    """Catches illegal cancellation of X before evaluating the X=0 branch."""

    module = _load_script_module()
    result = module.derive_zero_field_response_limit(source_power=1)
    symbols = result["symbols"]

    assert result["exact_zero_equation"] == 0
    assert result["exact_zero_chi_coefficient"] == 0
    assert result["chi_selected_at_exact_zero"] is False
    assert result["source_path_gap_limit"] == 0
    assert sp.simplify(result["finite_X_response"].subs(symbols["k"], 2)) == -sp.Rational(1, 4)
    assert sp.simplify(
        result["field_path_gap_limit"].subs(
            {symbols["k"]: 2, symbols["delta_Jtilde"]: 3}
        )
    ) == -sp.Rational(3, 4)
    assert result["path_dependent_zero_field_limit"] is True


def test_faster_source_switch_off_is_a_negative_control_for_the_finite_path_memory():
    """Catches a discontinuity predicate that cannot distinguish source scaling."""

    module = _load_script_module()
    mutation = module.derive_zero_field_response_limit(source_power=2)

    assert mutation["source_path_gap_limit"] == 0
    assert mutation["finite_X_response_limit"] == 0
    assert mutation["field_path_gap_limit"] == 0
    assert mutation["path_dependent_zero_field_limit"] is False


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
