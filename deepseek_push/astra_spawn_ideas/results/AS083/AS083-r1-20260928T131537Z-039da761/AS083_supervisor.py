#!/usr/bin/env python3
"""
AS083 bound supervisor: spawns AS083_checks.py as a single-threaded child and
enforces the declared prototype bounds:

  wall   <= 120 s   (supervisor kill at 120 s + in-process RLIMIT_CPU 115 s)
  memory <= 512 MiB (RSS poll every 0.1 s, SIGKILL above 524288 KiB)
  threads = 1       (no child spawns; OMP/OPENBLAS/MKL/VECLIB pinned to 1)

macOS 26.5.2 refuses in-process RLIMIT_AS/RLIMIT_DATA/RLIMIT_RSS lowering
(verified empirically in AS065), so memory is enforced externally here.
Records ACTUALLY enforced bounds in AS083_bounds.json.
"""
import json
import os
import resource
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.join(HERE, "AS083_checks.py")
OUT_JSON = os.path.join(HERE, "AS083_bounds.json")

WALL_LIMIT_S = 120.0
MEM_LIMIT_BYTES = 512 * 1024 * 1024
POLL_S = 0.1

env = dict(os.environ)
for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    env[var] = "1"

t0 = time.monotonic()
proc = subprocess.Popen(
    [sys.executable, "-u", LANE],
    stdout=open(os.path.join(HERE, "AS083_lane_stdout.txt"), "wb"),
    stderr=open(os.path.join(HERE, "AS083_lane_stderr.txt"), "wb"),
    env=env, cwd=HERE)

max_rss_kib = 0
killed_mem = killed_wall = False
wall_elapsed = None
rc = None
while True:
    try:
        rc = proc.wait(timeout=POLL_S)
        wall_elapsed = time.monotonic() - t0
        break
    except subprocess.TimeoutExpired:
        wall_elapsed = time.monotonic() - t0
        if wall_elapsed > WALL_LIMIT_S:
            proc.kill()
            killed_wall = True
            proc.wait()
            break
        try:
            rss = int(open(f"/proc/{proc.pid}/status").read().split("VmRSS:")[1]
                      .split()[0]) * 1024
        except Exception:
            # macOS: ps -o rss=
            rss = int(subprocess.check_output(
                ["ps", "-o", "rss=", "-p", str(proc.pid)]).split()[0]) * 1024
        max_rss_kib = max(max_rss_kib, rss // 1024)
        if rss > MEM_LIMIT_BYTES:
            proc.kill()
            killed_mem = True
            proc.wait()
            break

bounds = {
    "declared_wall_s": 120,
    "declared_mem_mib": 512,
    "declared_threads": 1,
    "enforced_wall_s": round(wall_elapsed, 3) if wall_elapsed is not None else None,
    "wall_killed": killed_wall,
    "enforced_mem_max_kib": max_rss_kib,
    "mem_killed": killed_mem,
    "threads": "1 (single process; OMP/OPENBLAS/MKL/VECLIB/NUMEXPR pinned to 1; "
               "no spawns)",
    "exit_code": rc,
    "notes": "in-process RLIMIT_CPU soft=hard=115 s set in lane; macOS refuses "
             "RLIMIT_AS/RLIMIT_DATA/RLIMIT_RSS lowering, memory enforced "
             "externally by this supervisor (poll 0.1 s, SIGKILL above 512 MiB)",
}
with open(OUT_JSON, "w") as f:
    json.dump(bounds, f, indent=1)
print(json.dumps(bounds, indent=1))
print(f"exit_code={rc}  wall={wall_elapsed:.2f}s  max_rss={max_rss_kib} KiB")
sys.exit(rc)
