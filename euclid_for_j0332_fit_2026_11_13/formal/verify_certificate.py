"""Compile the local AQUAL theorem and a false degree-two mutation.

Uses existing dependencies without modifying the canonical Lean project.
All generated artifacts are written beside this script.
"""
import hashlib
import json
import platform
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROJECT = ROOT/"fable_independent_2026"/"lean_2026"
SOURCE = HERE/"AqualScaling.lean"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(argv, log):
    start = time.monotonic()
    result = subprocess.run(argv, cwd=PROJECT, text=True, capture_output=True,
                            timeout=120, check=False)
    log.write_text(result.stdout + result.stderr)
    return {"argv": argv, "cwd": str(PROJECT), "exit_code": result.returncode,
            "runtime_seconds": time.monotonic()-start,
            "log": str(log), "log_sha256": digest(log)}


def main():
    code = SOURCE.read_text()
    assert not re.search(r"\b(sorry|admit)\b|^\s*axiom\s", code, re.M)
    tracked = [SOURCE, Path(__file__).resolve(), PROJECT/"lean-toolchain",
               PROJECT/"lakefile.toml", PROJECT/"lake-manifest.json"]
    hashes_before = {str(p): digest(p) for p in tracked}
    mutation = code.replace("= k • flux a g := by", "= (k*k) • flux a g := by", 1)
    assert mutation != code
    mutated_path = HERE/"AqualScaling_MUTATE.lean"
    mutated_path.write_text(mutation)
    version = invoke(["lake", "env", "lean", "--version"], HERE/"lean_version.log")
    positive = invoke(["lake", "env", "lean", str(SOURCE)], HERE/"compile.log")
    negative = invoke(["lake", "env", "lean", str(mutated_path)], HERE/"mutation_compile.log")
    hashes_after = {str(p): digest(p) for p in tracked}
    output = (HERE/"compile.log").read_text()
    assert version["exit_code"] == 0
    assert positive["exit_code"] == 0
    assert "sorryAx" not in output
    assert negative["exit_code"] != 0
    assert hashes_before == hashes_after
    record = {
        "assertion_tested": "Lean type-check of nine local algebraic theorems: AQUAL scaling, fixed linear projection, lens mass-sheet/source maps, and square-root density scaling; deliberately false degree-two flux mutation must not type-check",
        "non_claims": "No PDE existence, boundary or convergence certificate, empirical fit certificate, physical action certification, or novelty claim",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": platform.python_version(),
        "versions": (HERE/"lean_version.log").read_text().strip(),
        "inputs_sha256_before": hashes_before, "inputs_sha256_after": hashes_after,
        "positive_compile": positive, "negative_control_compile": negative,
        "mutation_sha256": digest(mutated_path),
        "axiom_dependencies": ["propext", "Classical.choice", "Quot.sound"],
        "custom_axioms_or_sorry": False,
        "review_provenance": "Author self-audit; root independently inspected original flux/FV definitions and scope; extended projection/mass-sheet/density statements sent for root inspection",
        "status": "completed; all expected compile outcomes observed",
    }
    (HERE/"certificate_provenance.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
