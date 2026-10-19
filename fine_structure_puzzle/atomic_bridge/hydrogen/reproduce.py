#!/usr/bin/env python3
"""Reproduce into a fresh run directory, preserving previous evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--run", required=True, help="new directory name below hydrogen, e.g. run003")
args = parser.parse_args()
if Path(args.run).name != args.run or (here / args.run).exists():
    parser.error("--run must be a new single directory name")
skill = Path("/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit")
contract = json.loads((here / "contract.json").read_text())
rel = here.relative_to(root)
dest = rel / args.run
cmd = [sys.executable, str(skill / "scripts/run_experiment.py"), "--root", str(root),
       "--contract", str(rel / "contract.json")]
for item in contract["execution_artifacts"]:
    cmd += ["--input", item]
cmd += ["--output", str(dest), "--result", str(dest / "results.json"), "--timeout", "45",
        "--max-output-bytes", "1048576", "--max-threads", "1", "--", sys.executable,
        str(rel / "compute.py"), "--output", str(dest / "results.json")]
subprocess.run(cmd, cwd=root, check=True)
subprocess.run([sys.executable, str(skill / "scripts/validate_manifest.py"),
                str(dest / "manifest.json"), "--root", str(root)], cwd=root, check=True)
