#!/usr/bin/env python3
"""Reproduce positive algebra checks AND expected physics-certification failures."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CASES = [
    ("physical action audit", ["physical_action_audit.py"], 0),
    ("full closure requested", ["physical_action_audit.py", "--require-closure"], 1),
    ("historical action bridges", ["cuscuton_acceleration_mond_gate.py"], 1),
    ("historical surrogate only", ["cuscuton_acceleration_mond_gate.py", "--historical-block-only"], 0),
    ("physical regression controls", ["-m", "unittest", "-v", "test_physical_action_audit.py"], 0),
    ("historical algebra regression", ["-m", "unittest", "-v", "test_cuscuton_acceleration_mond.py"], 0),
    ("Lean certificates", ["run_cuscuton_acceleration_lean.py"], 0),
    ("restricted clock kinematics", ["clock_principal_gate.py"], 0),
    ("conditional circular law", ["kepler_prediction_gate.py"], 0),
    ("EH reduction", ["eh_static_reduction_gate.py"], 0),
    ("existing closure regressions", [
        "-m", "unittest", "discover", "-v", "-s",
        "../tensor_compensated_branch_2026", "-p", "test_*.py"], 0),
]


def main():
    records = []
    for name, argv, expected in CASES:
        command = [sys.executable, "-B", *argv]
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        print(f"\nCASE: {name}\nARGV: {json.dumps(command)}\nCWD: {ROOT}", flush=True)
        print(proc.stdout, end="")
        print(proc.stderr, end="")
        record = {"name": name, "argv": command, "cwd": str(ROOT),
                  "exit_status": proc.returncode, "expected_exit": expected,
                  "execution_as_expected": proc.returncode == expected}
        records.append(record)
        print("CASE_RESULT=" + json.dumps(record), flush=True)
    print("SUITE_RESULTS=" + json.dumps(records))
    print("PHYSICS_STATUS=NOT_CLOSED; audit success includes expected certification failures.")
    return 0 if all(r["execution_as_expected"] for r in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
