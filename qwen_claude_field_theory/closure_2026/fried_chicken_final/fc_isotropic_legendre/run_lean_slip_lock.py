"""Compile the C4 slip-lock multiplier certificate."""

from pathlib import Path
import subprocess

root = Path(__file__).parent
project = root.parent.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "SlipLockMultiplierFormal.lean"
proc = subprocess.run(
    ["lake", "env", "lean", str(source)],
    cwd=project,
    text=True,
    capture_output=True,
)
print(proc.stdout, end="")
print(proc.stderr, end="")
print(f"LEAN_SLIP_LOCK_EXIT_STATUS={proc.returncode}")
raise SystemExit(proc.returncode)
