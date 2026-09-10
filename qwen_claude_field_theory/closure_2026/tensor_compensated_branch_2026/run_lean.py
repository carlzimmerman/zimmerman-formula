"""Run the Lean finite-k tensor-compensator certificate."""

from pathlib import Path
import subprocess

root = Path(__file__).parent
project = root.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "TensorCompensatedBranchFormal.lean"
proc = subprocess.run(["lake", "env", "lean", str(source)], cwd=project,
                      text=True, capture_output=True)
print(proc.stdout, end="")
print(proc.stderr, end="")
print(f"LEAN_TENSOR_COMPENSATED_BRANCH_EXIT_STATUS={proc.returncode}")
raise SystemExit(proc.returncode)
