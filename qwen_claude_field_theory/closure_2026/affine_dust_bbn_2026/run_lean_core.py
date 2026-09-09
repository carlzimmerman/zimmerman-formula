#!/usr/bin/env python3
"""Run the dependency-light Lean kernel gate and record its exit status."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "L84_BBN_Core.lean"
OUT = ROOT / "run_001" / "lean_core_results.json"


def main() -> int:
    lean = shutil.which("lean")
    started = time.time()
    if lean is None:
        result = {
            "gate": "L84-affine-dust-bbn-lean-core",
            "status": "TOOLCHAIN_MISSING",
            "exit_status": None,
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        return 1

    proc = subprocess.run(
        [lean, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    result = {
        "gate": "L84-affine-dust-bbn-lean-core",
        "status": "COMPILED" if proc.returncode == 0 else "LEAN_COMPILE_FAILED",
        "exit_status": proc.returncode,
        "elapsed_seconds": round(time.time() - started, 6),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "scope": "Pure Lean core arithmetic; no Mathlib dependency and no sorry/axiom declarations.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"])
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

