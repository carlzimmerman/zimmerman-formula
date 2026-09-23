#!/usr/bin/env python3
"""Compile the untouched PD02 source and independent replacement; save evidence."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "fable_independent_2026/lean_2026"
OUT = Path(sys.argv[1]).resolve()
sources = {
    "original": ROOT / "deepseek_push/lean/PD02_channel_count.lean",
    "reconstruction": Path(__file__).with_name("PDNormalization.lean"),
}
results = {}
for name, source in sources.items():
    argv = ["lake", "env", "lean", str(source)]
    start = time.monotonic()
    run = subprocess.run(argv, cwd=PROJECT, capture_output=True, text=True, timeout=50)
    (OUT / (name + ".stdout.txt")).write_text(run.stdout)
    (OUT / (name + ".stderr.txt")).write_text(run.stderr)
    results[name] = {"argv": argv, "cwd": str(PROJECT), "exit_code": run.returncode,
                     "elapsed_seconds": time.monotonic() - start,
                     "error_count": run.stdout.count("error:"),
                     "contains_sorry_axiom": "sorryAx" in run.stdout}
    if name == "reconstruction":
        assert run.returncode == 0, run.stdout + run.stderr
        assert "sorryAx" not in run.stdout, run.stdout
        assert "#print axioms" in source.read_text()
    else:
        assert run.returncode != 0, "Original unexpectedly compiles; re-evaluate original-status finding."
version = subprocess.run(["lake", "env", "lean", "--version"], cwd=PROJECT,
                         capture_output=True, text=True, check=True).stdout.strip()
payload = {"lean_version": version, "results": results,
           "scope": "Algebraic response slopes and matching identities only; no physical channel or stress-energy theorem."}
(OUT / "result.json").write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
