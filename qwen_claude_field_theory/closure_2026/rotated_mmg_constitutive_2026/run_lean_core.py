"""Compile the pure-Lean RMMG rank-jump witness."""

from pathlib import Path
import subprocess

root = Path(__file__).parent
proc = subprocess.run(
    ["lean", str(root / "RMMGCore.lean")],
    cwd=root,
    text=True,
    capture_output=True,
)
print(proc.stdout, end="")
print(proc.stderr, end="")
print(f"LEAN_EXIT_STATUS={proc.returncode}")
raise SystemExit(proc.returncode)
