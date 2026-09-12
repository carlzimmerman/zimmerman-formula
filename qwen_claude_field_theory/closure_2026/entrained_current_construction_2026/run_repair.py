#!/usr/bin/env python3
"""Record repaired-sector derivation with both old and new regression tests."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from density_repair import calculate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    result = {"repair": calculate(), "commands": []}
    commands = [[sys.executable, "-B", "-m", "unittest", "discover", "-s", str(directory),
                 "-p", "test_*.py", "-v"],
                [sys.executable, "-B", str(directory/"check_lean.py")],
                [sys.executable, "-B", str(directory/"check_lean.py"), "--source", str(directory/"DensityRepair.lean")]]
    for command in commands:
        run = subprocess.run(command, text=True, capture_output=True, timeout=120)
        result["commands"].append({"argv": command, "returncode": run.returncode,
                                   "stdout": run.stdout, "stderr": run.stderr})
        print("COMMAND", command, "EXIT", run.returncode, flush=True)
        if run.stdout.strip():
            print(run.stdout.strip(), flush=True)
        if run.stderr.strip():
            print(run.stderr.strip(), flush=True)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2)+"\n")
    sys.exit(0 if all(item["returncode"] == 0 for item in result["commands"]) else 1)
