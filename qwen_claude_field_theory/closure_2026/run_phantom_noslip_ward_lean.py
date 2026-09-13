#!/usr/bin/env python3
"""Compile the scoped no-slip/Ward phantom trilemma Lean certificate."""

from pathlib import Path
import subprocess


root = Path(__file__).resolve().parent
project = root / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "PhantomNoSlipWardFormal.lean"
raise SystemExit(subprocess.run(["lake", "env", "lean", str(source)], cwd=project).returncode)
