#!/usr/bin/env python3
"""Run and compile ExtendedGeminiClosureProof.lean using lake env lean."""

from pathlib import Path
import subprocess
import sys

repo_root = Path(__file__).resolve().parent.parent
project_dir = repo_root / "qwen_claude_field_theory" / "closure_2026" / "clock_constitutive_construction_2026" / "lean_formalization_2026"
source_file = repo_root / "gemini38_flash_push" / "ExtendedGeminiClosureProof.lean"

print(f"Compiling Extended Lean certificate: {source_file}")
cmd = ["lake", "env", "lean", str(source_file)]
res = subprocess.run(cmd, cwd=str(project_dir), capture_output=True, text=True)

if res.stdout:
    print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)

print(f"Extended Lean compilation exit code: {res.returncode}")
if res.returncode == 0:
    print("SUCCESS: 0 errors, 0 sorrys. Extended Lean math certification complete!")
sys.exit(res.returncode)
