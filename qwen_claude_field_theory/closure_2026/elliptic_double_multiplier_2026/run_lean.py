"""Run the Lean checker for the constructive elliptic double-multiplier branch."""

from pathlib import Path
import subprocess

root = Path(__file__).parent
project = root.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "EllipticDoubleMultiplierFormal.lean"
proc = subprocess.run(["lake", "env", "lean", str(source)], cwd=project,
                      text=True, capture_output=True)
print(proc.stdout, end="")
print(proc.stderr, end="")
print(f"LEAN_ELLIPTIC_DOUBLE_MULTIPLIER_EXIT_STATUS={proc.returncode}")
raise SystemExit(proc.returncode)
