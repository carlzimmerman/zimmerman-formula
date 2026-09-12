#!/usr/bin/env python3
"""Compile the exact polynomial certificate with existing, pinned Lean libraries."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).with_name("CounterflowCone.lean"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    project = root / "qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026"
    version = (project / "lean-toolchain").read_text().strip()
    executable = Path.home()/".elan/toolchains"/version.replace("/", "--").replace(":", "---")/"bin/lean"
    packages = project/".lake/packages"
    libraries = sorted(p/".lake/build/lib/lean" for p in packages.iterdir()
                       if (p/".lake/build/lib/lean").is_dir())
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, libraries)))
    print("toolchain", version, flush=True)
    completed = subprocess.run([str(executable), str(args.source.resolve())], env=env, timeout=120)
    sys.exit(completed.returncode)


if __name__ == "__main__":
    main()
