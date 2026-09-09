#!/usr/bin/env python3
"""Probe and, when available, compile the Lean algebraic core.

Exit status 0 means Lean compiled the file.  Exit status 2 is an explicit
toolchain-unavailable result; it is not treated as a mathematical pass.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "ClockConstitutiveGate.lean"
RESULT = HERE / "run_001" / "lean_gate_results.json"


def main() -> int:
    lean = shutil.which("lean")
    lake = shutil.which("lake")
    result = {
        "source": str(SOURCE.relative_to(HERE.parent.parent.parent.parent)),
        "lean_found": bool(lean),
        "lake_found": bool(lake),
        "status": "UNCOMPILED_TOOLCHAIN_UNAVAILABLE",
        "exit_status": 2,
        "scope": [
            "exponential constitutive identity",
            "positive constitutive eigenvalues for y>0",
            "flat linear equation determinant factorization",
            "rational subluminal witness",
        ],
        "non_claims": [
            "the gravity theory is not fully formalized",
            "no full covariant action variation",
            "no nonlinear Dirac closure or PPN theorem",
            "no y=0 endpoint, FLRW perturbation, or empirical fit",
        ],
    }
    if lake:
        proc = subprocess.run([lake, "env", "lean", SOURCE.name], cwd=HERE,
                              text=True, capture_output=True)
        result["status"] = "COMPILED" if proc.returncode == 0 else "LEAN_COMPILE_FAILED"
        result["exit_status"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
    elif lean:
        proc = subprocess.run([lean, str(SOURCE)], cwd=HERE,
                              text=True, capture_output=True)
        result["status"] = "COMPILED" if proc.returncode == 0 else "LEAN_COMPILE_FAILED"
        result["exit_status"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return int(result["exit_status"])


if __name__ == "__main__":
    raise SystemExit(main())
