#!/usr/bin/env python3
"""Execute the derivations, adversarial controls, and Lean certificate together."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from current_action import calculate
from variation import derive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    result = {"construction": calculate(), "variation": derive(), "commands": []}
    commands = [[sys.executable, "-B", str(directory/"variation.py")],
                [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(directory),
                 "-p", "test_current_action.py", "-v"],
                [sys.executable, "-B", str(directory/"check_lean.py")]]
    for command in commands:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=120)
        result["commands"].append({"argv": command, "returncode": completed.returncode,
                                   "stdout": completed.stdout, "stderr": completed.stderr})
        print("COMMAND", command, "EXIT", completed.returncode, flush=True)
        print(completed.stdout, completed.stderr, flush=True)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2)+"\n")
    sys.exit(0 if all(item["returncode"] == 0 for item in result["commands"]) else 1)


if __name__ == "__main__":
    main()
