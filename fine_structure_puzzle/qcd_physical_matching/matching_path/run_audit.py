#!/usr/bin/env python3
"""Bounded local evidence capture without invoking Git or network tools."""
import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path

import mpmath
import sympy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, help="Fresh directory name within this lane")
    args = parser.parse_args()
    lane = Path(__file__).resolve().parent
    root = lane.parents[2]
    out = lane / args.run
    out.mkdir(exist_ok=False)
    rel = lambda p: str(p.relative_to(root))
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    paths = [lane / x for x in ["check_matching.py", "run_audit.py", "contract.json", "INPUTS.json", "SOURCES.json"]]
    paths += [root/x["path"] for x in json.loads((lane/"INPUTS.json").read_text())["inputs"]]
    before = {rel(p):digest(p) for p in paths}
    command = [sys.executable, rel(lane/"check_matching.py"), "--output", rel(out/"result.json")]
    contract = json.loads((lane/"contract.json").read_text())
    env = os.environ.copy()
    for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        env[k] = "1"
    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (20,20))
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    t0 = time.monotonic()
    status = "completed"
    try:
        done = subprocess.run(command, cwd=root, env=env, capture_output=True, timeout=30, preexec_fn=limits)
        stdout, stderr, exit_status = done.stdout, done.stderr, done.returncode
        if exit_status:
            status = "failed"
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, exit_status, status = exc.stdout or b"", exc.stderr or b"", -1, "timeout"
    runtime = time.monotonic()-t0
    (out/"stdout.txt").write_bytes(stdout)
    (out/"stderr.txt").write_bytes(stderr)
    after = {rel(p):digest(p) for p in paths}
    if status == "completed" and before != after:
        status = "inputs-changed"
    result = json.loads((out/"result.json").read_text()) if (out/"result.json").is_file() else None
    if status == "completed" and result is None:
        status = "result-missing"
    manifest = {
        "schema_version":2, "claim_id":contract["claim_id"],
        "repository":{"commit":"unavailable; Git commands excluded by task", "dirty":True,
                      "dirty_basis":"Conservative true flag; exact repository dirty state was not inspected. New lane artifacts were written in this run."},
        "command":command,
        "environment":{"software":[{"name":"Python", "version":platform.python_version()},
                                     {"name":"SymPy", "version":sympy.__version__},
                                     {"name":"mpmath", "version":mpmath.__version__}],
                       "hardware":platform.machine()+"; "+platform.system()+" "+platform.release()},
        "mathematics":contract["mathematics"], "randomness":contract["randomness"],
        "run":{"started_at":started,"runtime_seconds":runtime,"exit_status":exit_status,"status":status,
               "resource_limits":{"memory_bytes":None,"cpu_seconds":20,"max_cores":None,"max_threads":1},
               "wall_timeout_seconds":30,"capture":"subprocess capture; finite program has bounded output; no hard output-byte cap"},
        "outputs":[{"path":rel(p),"sha256":digest(p),"kind":"result" if p.name=="result.json" else "log"}
                   for p in [out/"stdout.txt",out/"stderr.txt",out/"result.json"] if p.is_file()],
        "checks":result["checks"] if result else [],
        "result":result["interpretation"] if result else "No usable result produced",
        "residual_risks":["No interval roundoff certification", "Source-to-QCD applicability requires separately stated physical hypotheses", "Exact Git state unobserved; content hashes supply file-level provenance"],
        "input_artifacts":[{"path":p,"sha256":h,"sha256_after":after[p]} for p,h in before.items()],
        "declared_results":[rel(out/"result.json")],
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"status":status,"runtime_seconds":runtime,"check_count":len(manifest["checks"]),"manifest":rel(out/"manifest.json")}))
    sys.exit(0 if status=="completed" else 1)


if __name__ == "__main__":
    main()
