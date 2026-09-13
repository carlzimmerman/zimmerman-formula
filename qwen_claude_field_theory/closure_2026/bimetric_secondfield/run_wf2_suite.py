#!/usr/bin/env python3
"""Run the derivative-bimetric second-field gates and record raw evidence.

This is an orchestration/provenance script, not a pass/fail oracle.  It does
not encode expected ranks, determinants, PPN values, or degree-of-freedom
counts.  Each child performs its own symbolic or numerical calculation; this
script records only the exact child command, return code, runtime, source
hash, and captured output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_GATES = (
    "wf2_indep_bdghost_reverify.py",
    "wf2_vecghost_hel1.py",
    "wf2_coupledlens_alpha3.py",
    "wf2_tensor_cT_gate.py",
    "wf2_adjudicator_vecghost_indep.py",
    "wf2_nonlinear_vector_background.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run_gate(path: Path, timeout: int) -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-B", str(path)]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=str(ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "script": str(path.relative_to(ROOT)),
        "command": command,
        "source_sha256": sha256(path),
        "returncode": completed.returncode,
        "runtime_s": round(time.monotonic() - started, 6),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "wf2_suite_results.json")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    records = []
    for name in DEFAULT_GATES:
        records.append(run_gate(HERE / name, args.timeout))
    result = {
        "suite": "derivative-bimetric-secondfield-gates",
        "scope": "bounded symbolic/numerical rerun of repository gates; no universal theorem asserted",
        "python": sys.version,
        "platform": platform.platform(),
        "gates": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output),
                      "returncodes": [record["returncode"] for record in records]}, indent=2))
    return 0 if all(record["returncode"] == 0 for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
