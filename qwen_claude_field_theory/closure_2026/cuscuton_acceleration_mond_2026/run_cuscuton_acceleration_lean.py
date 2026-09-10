"""Run the Lean certificates for the constructive acceleration branch."""

from pathlib import Path
import subprocess

root = Path(__file__).parent
project = root.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
status = 0
for filename in ("CuscutonAccelerationMondFormal.lean", "PhysicalActionAuditFormal.lean"):
    proc = subprocess.run(
        ["lake", "env", "lean", str(root / filename)],
        cwd=project, text=True, capture_output=True,
    )
    print(proc.stdout, end="")
    print(proc.stderr, end="")
    print(f"{filename}: EXIT_STATUS={proc.returncode}")
    status = max(status, proc.returncode)
print(f"LEAN_CUSCUTON_ACCELERATION_EXIT_STATUS={status}")
raise SystemExit(status)
