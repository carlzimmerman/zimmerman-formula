"""Run the kernel checker for the homogeneous DBI clock theorem."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent
PROJECT = ROOT.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
SOURCE = ROOT / "DBIClockUniqueSpeed.lean"
OUTPUT = ROOT / "run_001" / "lean_result.json"

proc = subprocess.run(
    ["lake", "env", "lean", str(SOURCE)],
    cwd=PROJECT,
    text=True,
    capture_output=True,
)

result = {
    "source": str(SOURCE.relative_to(ROOT)),
    "lean_project": str(PROJECT.relative_to(ROOT.parent.parent)),
    "lean_command": ["lake", "env", "lean", str(SOURCE)],
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "exit_status": proc.returncode,
    "theorem_present": "theorem dbi_clock_unique_speed" in SOURCE.read_text(),
    "stdout": proc.stdout,
    "stderr": proc.stderr,
    "status": "KERNEL_CHECKED" if proc.returncode == 0 else "FAILED",
    "scope": "homogeneous DBI clock current only",
    "nonclaims": [
        "not a proof of the full covariant metric equations",
        "not a proof of nonlinear Dirac/HDA closure",
        "not a PPN or perturbative stability proof",
        "not a proof that the complete gravity theory exists",
    ],
}
OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(proc.returncode)
