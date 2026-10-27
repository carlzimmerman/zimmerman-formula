#!/usr/bin/env python3
"""Bounded v2 provenance wrapper; deliberately makes no Git calls."""
import datetime
import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LANE = Path(__file__).resolve().parent.relative_to(ROOT)


def digest(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def limit_child():
    resource.setrlimit(resource.RLIMIT_CPU, (10, 10))


def main():
    contract = json.loads((ROOT / LANE / "COMPUTATION_CONTRACT.json").read_text())
    inputs = [{"path": p, "sha256": digest(p)}
              for p in contract["execution_artifacts"]]
    out = LANE / "run_clean_001"
    (ROOT / out).mkdir()
    result = out / "result.json"
    command = [sys.executable, str(LANE / "check_photon_mass_clean.py"), str(result)]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    begin = time.monotonic()
    child_env = dict(os.environ)
    for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]:
        child_env[key] = "1"
    status = "completed"
    with (ROOT / out / "stdout.txt").open("wb") as stdout, \
         (ROOT / out / "stderr.txt").open("wb") as stderr:
        p = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                             stdout=stdout, stderr=stderr, env=child_env,
                             start_new_session=True, preexec_fn=limit_child)
        try:
            code = p.wait(timeout=20)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            code = p.wait()
            status = "timeout"
    elapsed = time.monotonic() - begin
    if status == "completed" and code != 0:
        status = "failed"
    for row in inputs:
        row["sha256_after"] = digest(row["path"])
    unchanged = all(r["sha256"] == r["sha256_after"] for r in inputs)
    if status == "completed" and not unchanged:
        status = "inputs-changed"
    if status == "completed" and not (ROOT / result).is_file():
        status = "result-missing"
    outputs = []
    for name, kind in [(out / "stdout.txt", "log"),
                       (out / "stderr.txt", "log"), (result, "result")]:
        if (ROOT / name).is_file():
            outputs.append({"path": str(name), "sha256": digest(name), "kind": kind})
    manifest = {
        "schema_version": 2,
        "claim_id": contract["claim_id"],
        "repository": {
            "commit": "unavailable: Git inspection prohibited by review scope",
            "dirty": True,
            "dirty_observation": "not measured; conservative true marker because reviewer creates files; no claim of observed Git state"},
        "command": command,
        "environment": {"software": [{"name": "Python / stdlib fractions", "version": platform.python_version()}],
                        "hardware": platform.platform()},
        "mathematics": contract["mathematics"],
        "randomness": contract["randomness"],
        "run": {"started_at": started, "runtime_seconds": elapsed,
                "exit_status": code, "status": status, "timeout_seconds": 20,
                "resource_limits": {"memory_bytes": None, "cpu_seconds": 10,
                                    "max_cores": None, "max_threads": 1}},
        "execution_artifacts": contract["execution_artifacts"],
        "input_artifacts": inputs,
        "declared_results": [str(result)],
        "outputs": outputs,
        "checks": [{"check": "all listed before/after hashes unchanged", "passed": unchanged},
                   {"check": "child exited zero within limits", "passed": code == 0 and status == "completed"}],
        "result": "Finite exact algebra only; interpret together with SOURCECRITICAL.md and REVIEW.md.",
        "residual_risks": [
            "Git revision and dirty state were not queried; dirty=true is a conservative schema marker, not an observation.",
            "CPU limit is per process; this child creates no descendants.",
            "No RLIMIT_AS requested on macOS.",
            "No output-byte hard cap; reviewed program emits a fixed bounded summary.",
            "Successful execution does not establish QCD or EFT remainder hypotheses.",
            "New-lane math/code preceded new author packet; parent contact hint arrived before durable pretarget pin, as recorded."]}
    (ROOT / out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": status, "exit_status": code,
                      "runtime_seconds": elapsed, "manifest": str(out / "manifest.json")}))
    return 0 if status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
