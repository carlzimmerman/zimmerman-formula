#!/usr/bin/env python3
"""Compile the certificates, inspect axioms, and reject three damaged proofs."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LAKE = ROOT / "fable_independent_2026/lean_2026"
SOURCE = HERE / "Architecture.lean"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def main():
    out = Path(sys.argv[1]).resolve()
    if not out.is_relative_to(HERE) or not out.is_dir():
        raise ValueError("Output must be an existing run directory below this package")
    source = SOURCE.read_text()
    if re.search(r"\b(sorry|admit|native_decide|implemented_by)\b", source):
        raise ValueError("Unadmitted proof source required")
    if re.search(r"^\s*(axiom|opaque)\s", source, re.M):
        raise ValueError("No new axioms or opaque declarations allowed")
    names = re.findall(r"^theorem (\w+)", source, re.M)
    prints = re.findall(r"^#print axioms GravityArchitecture\.(\w+)", source, re.M)
    if not names or names != prints:
        raise ValueError("Every theorem must have one ordered axiom report")
    cases = [("main", SOURCE, 0)]
    mutations = [
        ("wrong_coefficient", "Λ * c ^ 4 / (32 * Real.pi)", "Λ * c ^ 4 / (16 * Real.pi)"),
        ("wrong_derivative", "HasDerivAt (tailColdMass A Mb) A r", "HasDerivAt (tailColdMass A Mb) (2 * A) r"),
        ("missing_supply_premise", "(hsupply : tailColdMass A Mb r ≤ S)", "(hsupply : 0 ≤ S)"),
    ]
    for name, old, new in mutations:
        if source.count(old) != 1:
            raise ValueError("Mutation anchor is not unique: " + name)
        path = out / (name + ".lean")
        path.write_text(source.replace(old, new))
        cases.append((name, path, 1))
    results = []
    for name, path, expected in cases:
        argv = ["lake", "env", "lean", "-j", "1", str(path)]
        proc = subprocess.run(argv, cwd=LAKE, text=True, capture_output=True, timeout=180)
        log = proc.stdout + proc.stderr
        (out / (name + ".log")).write_text(log)
        if name == "main":
            reports = re.findall(
                r"'GravityArchitecture\.(\w+)' depends on axioms: \[([^\]]*)\]", log
            )
            if [n for n, _ in reports] != names:
                raise ValueError("Missing theorem dependency reports; inspect main.log")
            for theorem, deps in reports:
                axioms = {a.strip() for a in deps.split(",") if a.strip()}
                if not axioms <= ALLOWED:
                    raise ValueError("Unexpected axiom in " + theorem + ": " + repr(axioms))
            passed = proc.returncode == 0 and "error:" not in log and "warning:" not in log
        else:
            passed = proc.returncode == expected and "error:" in log
        results.append({"case": name, "argv": argv, "exit_status": proc.returncode,
                        "expected_exit_status": expected, "passed": passed,
                        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        print(name + ": " + ("PASS" if passed else "FAIL"), flush=True)
    summary = {"theorem_count": len(names), "theorems": names,
               "allowed_standard_axioms": sorted(ALLOWED), "cases": results,
               "all_passed": all(x["passed"] for x in results),
               "scope": "Conditional real-algebra, calculus and conservation implications only; no empirical or complete-physics certification."}
    (out / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
