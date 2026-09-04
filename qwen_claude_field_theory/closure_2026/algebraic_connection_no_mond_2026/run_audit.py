#!/usr/bin/env python3
"""Run scoped computations and preserve failures, commands, output and hashes.

Execution success is NOT a full-theory PASS. Run from any working directory;
repository paths are resolved from this script. Old gates run with a temporary
working directory so their certificate files cannot overwrite repository data.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import tempfile
import time

import sympy
import numpy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def record_job(argv, cwd, timeout=180):
    started = time.perf_counter()
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(argv, cwd=cwd, env=environment, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   timeout=timeout, check=False)
        output, status, timed_out = completed.stdout, completed.returncode, False
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        status, timed_out = 124, True
    return {"argv": [str(v) for v in argv], "command": shlex.join([str(v) for v in argv]),
            "cwd": str(cwd), "environment_override": {"PYTHONDONTWRITEBYTECODE": "1"},
            "exit_status": status, "timed_out": timed_out,
            "runtime_seconds": time.perf_counter() - started, "output": output}


def fingerprint(path):
    record = {"path": str(path.relative_to(ROOT)), "sha256": None}
    try:
        record["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        record["error"] = f"{type(error).__name__}: {error}"
    return record


def main():
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip())
    closure = ROOT / "qwen_claude_field_theory/closure_2026"
    jobs = [
        ([sys.executable, "-m", "unittest", "discover", "-s", str(HERE), "-v"], ROOT),
        ([sys.executable, str(HERE / "connection_checks.py"), "--output",
          str(HERE / "connection_results.json")], ROOT),
        ([sys.executable, str(HERE / "metric_branch_checks.py")], ROOT),
        ([sys.executable, str(HERE / "spectral_escape_checks.py")], ROOT),
    ]
    legacy = [
        closure / "mond_compiler_2026/stage2b/s2b_palatini_identity_2026.py",
        closure / "mond_compiler_2026/stage2b/s2b_degenerate_branch_2026.py",
        closure / "nonlocal_door/ricci_polynomial_projector_gate_2026.py",
        closure / "nonlocal_door/vanishing_projector_dirac_chain_2026.py",
        closure / "nonlocal_door/metric_only_elliptic_projector_gate_2026.py",
    ]
    input_paths = sorted(list(HERE.glob("*.py")) + legacy + [ROOT / "hunt_2026/hunt_lib.py"])
    input_snapshots = [fingerprint(path) for path in input_paths]
    records = []
    with tempfile.TemporaryDirectory(prefix="algebraic-connection-audit-") as scratch:
        jobs.extend(([sys.executable, str(path)], Path(scratch)) for path in legacy)
        for argv, cwd in jobs:
            print("RUN", shlex.join(argv), flush=True)
            record = record_job(argv, cwd)
            records.append(record)
            print(f"exit={record['exit_status']} elapsed={record['runtime_seconds']:.3f}s", flush=True)
    log_parts = []
    for record in records:
        log_parts.append(f"COMMAND: {record['command']}\nCWD: {record['cwd']}\n"
                         f"EXIT: {record['exit_status']}  TIMEOUT: {record['timed_out']}\n"
                         f"SECONDS: {record['runtime_seconds']:.6f}\n{record['output']}\n")
    (HERE / "audit_output.txt").write_text("\n".join(log_parts).rstrip() + "\n")
    sources_unchanged = input_snapshots == [fingerprint(path) for path in input_paths]
    all_inputs_readable = all(record["sha256"] is not None for record in input_snapshots)
    all_success = (all(record["exit_status"] == 0 for record in records)
                   and sources_unchanged and all_inputs_readable)
    output_paths = sorted(path for path in HERE.iterdir()
                          if path.is_file() and path.name != "computation_manifest.json"
                          and path.suffix in (".py", ".md", ".json", ".txt"))
    manifest = {
        "schema_version": 1,
        "claim_id": "algebraic-connection-no-mond-and-spectral-obstructions-2026-09-04",
        "repository": {"commit": revision, "dirty": dirty},
        "command": f"python3 {HERE.relative_to(ROOT)}/run_audit.py",
        "environment": {"software": [f"Python {platform.python_version()}", f"SymPy {sympy.__version__}",
                                     f"NumPy {numpy.__version__} (legacy hunt_lib import)"],
                        "hardware": f"{platform.machine()}; {platform.platform()}"},
        "mathematics": {
            "assertion_tested": "Exact component/frame/canonical auxiliary identities; independent metric geometry and local spectral/source obstructions. General proof is in REPORT.md.",
            "coefficient_domain": "exact rationals and symbolic functions; new checks use no randomness, two legacy gates use seeded rational metric samples",
            "conventions": "(-+++), c=1, torsion-free unrestricted connection, mu_exp(y)=1-exp(-y)",
            "inputs": input_snapshots,
            "bounds": {"connection_dimensions": [1, 2, 3, 4], "frame_dimension": 4,
                       "canonical_sector": "4D frozen regular algebraic auxiliary block only",
                       "spectral_boundary": "exact local paths specified in spectral_escape_checks.py"},
            "non_claims": ["No full relativistic MOND theory or global novelty certification.",
                           "No gravitational DOF count inferred from auxiliary-only brackets.",
                           "No full PPN or perturbative-health computation.",
                           "No universal nonlocal/elliptic MOND no-go."]},
        "randomness": {"used": True, "generator": "Python random.Random in two legacy gates only; new computations are symbolic",
                       "seed": {"s2b_palatini_identity_2026.py": [11, 23, 37, 101],
                                "s2b_degenerate_branch_2026.py": [5]}},
        "run": {"started_at": started_at, "runtime_seconds": time.perf_counter() - started,
                "exit_status": 0 if all_success else 1, "source_inputs_unchanged": sources_unchanged,
                "all_inputs_readable": all_inputs_readable},
        "outputs": [fingerprint(path) for path in output_paths],
        "checks": [{key: value for key, value in record.items() if key != "output"} for record in records],
        "result": "Component tests reproduced in stated scope; interpret the action-class failure using REPORT.md." if all_success
                  else "A computation failed/timed out or executable inputs changed during the run; inspect before interpreting.",
        "residual_risks": ["Legacy green totals contain claims broader than their actual computations; see REPORT.md.",
                           "The exponential nonzero null branch is not C2 and has no regular Dirac certificate here.",
                           "The next projector/source action and its complete mixed constraint algebra remain open."]}
    (HERE / "computation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Recorded {len(records)} jobs. All exited zero: {all_success}. This is NOT a theory PASS.")
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
