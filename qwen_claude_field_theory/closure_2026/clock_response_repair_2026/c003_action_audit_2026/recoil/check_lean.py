#!/usr/bin/env python3
"""Use existing installed Lean and compiled dependencies without invoking Lake."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[5]
    packages = root / "qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/.lake/packages"
    libdirs = sorted(p / ".lake/build/lib/lean" for p in packages.iterdir() if (p / ".lake/build/lib/lean").is_dir())
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(str(p) for p in libdirs)
    lean = "/Users/carlzimmerman/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean"
    source = Path(__file__).with_name("RecoilAccounting.lean")
    started = time.monotonic()
    completed = subprocess.run([lean, str(source)], env=env, text=True, capture_output=True, timeout=180)
    result = {"argv": [lean, str(source)], "LEAN_PATH": env["LEAN_PATH"],
              "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr,
              "elapsed_seconds": time.monotonic()-started,
              "scope": "algebraic certificates only, stock Lean kernel with existing Mathlib build",
              "trust_boundary": "Lean kernel, standard classical/propext/quotient axioms, existing compiled Mathlib; no user-added axioms or sorry"}
    args.result.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    sys.exit(completed.returncode)


if __name__ == "__main__":
    main()
