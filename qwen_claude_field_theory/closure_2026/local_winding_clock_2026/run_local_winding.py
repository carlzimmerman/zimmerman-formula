"""Run every implemented local-winding-clock gate and write a JSON checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import sympy as sp

from action_variation import derive_action, static_branch
from dirac_gate import dirac_report
from flrw_winding_gate import flrw_report
from stability_causality_gate import stability_report
from weak_field_ward_gate import ward_report, weak_field_report
from winding_calibration import calibration_report
from winding_no_go import no_go_report


PACKAGE_ROOT = Path(__file__).resolve().parent


def encode(value):
    """Convert exact SymPy output to deterministic JSON without losing strings."""
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[encode(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    return value


def _source_hashes():
    hashes = {}
    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        if path.name.startswith("test_"):
            continue
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def build_results():
    action = derive_action()
    action["static"] = static_branch()
    dirac = {
        mode: dirac_report(mode) for mode in ("k_nonzero", "k_zero")
    }
    weak_field = weak_field_report()
    ward = ward_report()
    flrw = flrw_report()
    calibration = calibration_report()
    stability = stability_report()
    no_go = no_go_report()

    # This is intentionally OPEN: the missing gates are part of the result,
    # not silently treated as passing because the first gates are green.
    open_gates = [
        "full_ADM_DOF",
        "PPN_alpha",
        "nonlinear_stability",
        "causal_propagation",
        "memory_clock_stability",
        "strict_local_winding_architecture",
        "full_metric_Ward_identity",
        "empirical_own_clock_cosmology",
    ]
    return {
        "status": "OPEN",
        "route_verdict": "DEAD_FOR_SEPARATE_COLD_TRANSMISSION; OWN_CLOCK_CMB_DOOR_OPEN",
        "implemented_gates": [
            "action_variation",
            "static_exponential_branch",
            "homogeneous_Dirac_chain",
            "weak_field_Ward_representative",
            "expanding_FLRW_branch",
            "assembly_history_calibration",
            "principal_symbol_stress_test",
        ],
        "open_gates": open_gates,
        "non_claims": {
            "full_closure": True,
            "PPN_certification": True,
            "stability_certification": True,
            "Lean_compilation": True,
        },
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "source_hashes": _source_hashes(),
        "action": action,
        "dirac": dirac,
        "weak_field": weak_field,
        "ward": ward,
        "flrw": flrw,
        "calibration": calibration,
        "stability": stability,
        "no_go": no_go,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir", default="run_001",
        help="directory for local_winding_results.json (relative to this package)",
    )
    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = PACKAGE_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    results = build_results()
    target = output_dir / "local_winding_results.json"
    target.write_text(json.dumps(encode(results), indent=2, sort_keys=True) + "\n")
    print(f"wrote {target}")
    print(f"status={results['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
