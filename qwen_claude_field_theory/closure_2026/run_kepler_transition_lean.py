#!/usr/bin/env python3
"""Compile the Kepler-transition orbital-law Lean certificate."""

from pathlib import Path
import subprocess


root = Path(__file__).resolve().parent
project = root / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "KeplerTransitionFormal.lean"
raise SystemExit(subprocess.run(["lake", "env", "lean", str(source)], cwd=project).returncode)
