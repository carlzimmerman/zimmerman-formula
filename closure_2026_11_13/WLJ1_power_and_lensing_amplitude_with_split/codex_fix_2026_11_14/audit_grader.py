#!/usr/bin/env python3
"""Bounded-run entry point: real-grader regression, mutation and reproduction.

The audit receives an existing fresh runner output directory. It never runs a
grader in the historical lane. The fault mutation is reconstructed test-only
pooling, not claimed to be an authenticated historical source revision.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    lane = Path(__file__).resolve().parent.parent
    test = lane / "test_wlj1_grade.py"
    grader = lane / "wlj1_grade.py"
    spec = importlib.util.spec_from_file_location("wlj1_regression", test)
    regression = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(regression)

    # Record the corrected implementation as observed; do not edit production.
    source = grader.read_text()
    (output / "wlj1_grade_verified.py").write_text(source)
    assignment = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name) and target.value.id == "KA"
                and isinstance(target.slice, ast.Constant) and target.slice.value == "C4"
                for target in node.targets)
    ]
    if len(assignment) != 1:
        raise AssertionError("Expected exactly one top-level C4 known-answer assignment")
    lines = source.splitlines(keepends=True)
    lines.insert(assignment[0].end_lineno,
                 'KA["C4"] = {ft: all(KA["C4"].values()) for ft in FOOTS}  # TEST-ONLY BUG\n')
    mutant = output / "wlj1_grade_shared_flag_mutant.py"
    mutant.write_text("".join(lines))
    red_command = [sys.executable, "-I", "-B", str(test), "--grader-script", str(mutant),
                   "FootingIsolationTests.test_frozen_canonical_roundoff_does_not_downgrade_alt", "-v"]
    red = subprocess.run(red_command, capture_output=True, text=True, timeout=30)
    (output / "regression_red.txt").write_text(red.stdout + red.stderr)
    if red.returncode != 1 or "C4|REF|alt" not in red.stderr or "AssertionError" not in red.stderr:
        raise AssertionError("Shared-flag mutant did not fail the actual alt C4 grade as expected")

    green_command = [sys.executable, "-I", "-B", str(test), "-v"]
    green = subprocess.run(green_command, capture_output=True, text=True, timeout=60)
    (output / "regression_green.txt").write_text(green.stdout + green.stderr)
    if green.returncode != 0 or "Ran 7 tests" not in green.stderr:
        raise AssertionError("Current grader regression suite failed")

    amended, amended_files = regression.run_grader()
    frozen, frozen_files = regression.run_grader(as_frozen=True)
    generated = {**amended_files, **frozen_files}
    comparisons = {}
    for name in regression.OUTPUTS:
        original = (lane / name).read_bytes()
        actual = generated[name]
        (output / name).write_bytes(actual)
        comparisons[name] = {"historical_sha256": sha(original),
                             "reproduced_sha256": sha(actual), "byte_equal": original == actual}
    if not all(value["byte_equal"] for value in comparisons.values()):
        raise AssertionError("Saved output differs from re-executed grader")
    report = {
        "assertion_tested": "Per-footing C4 guards isolate failed checks, and both grading modes reproduce saved outputs.",
        "production_source_changed": False,
        "mutant_kind": "Reconstructed shared-flag bug: pool the computed C4 checks across footings.",
        "red_command": red_command, "red_exit_status": red.returncode,
        "red_expected_failure": "C4|REF|alt: NO VERDICT instead of ROW HOLDS WITH THE SPLIT",
        "green_command": green_command, "green_exit_status": green.returncode,
        "green_test_count": 7, "comparisons": comparisons,
        "as_frozen_C4_known_answers": frozen["KA"]["C4"],
        "amended_C4_known_answers": amended["KA"]["C4"],
        "graded_rows": {mode: {key: value for key, value in result["rows"].items()
                                if any(f"|{case}|" in key for case in ("S1.25", "S2", "S3"))}
                        for mode, result in (("as_frozen", frozen), ("amended", amended))},
        "non_claims": ["No upstream numerical stage or independent physical model was rerun.",
                       "No theory-closure, model-selection or new successful split prediction follows."],
    }
    (output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Shared-flag mutation: expected alt C4 grading failure detected.")
    print("Current grader: 7 regression tests passed; all 6 saved outputs byte-identical.")


if __name__ == "__main__":
    main()
