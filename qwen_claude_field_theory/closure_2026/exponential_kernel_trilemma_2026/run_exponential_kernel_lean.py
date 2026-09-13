#!/usr/bin/env python3
"""Compile the exponential-kernel trilemma Lean certificate."""

from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
project = root.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "ExponentialKernelTrilemmaFormal.lean"
raise SystemExit(subprocess.run(["lake", "env", "lean", str(source)], cwd=project).returncode)
