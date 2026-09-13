#!/usr/bin/env python3
"""Compile the finite-k AeST scalar Lean certificate."""

import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent
project = root.parent.parent / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source = root / "AestMetricScalarFormal.lean"
cmd = ["lake", "env", "lean", str(source)]
proc = subprocess.run(cmd, cwd=project, text=True)
raise SystemExit(proc.returncode)
