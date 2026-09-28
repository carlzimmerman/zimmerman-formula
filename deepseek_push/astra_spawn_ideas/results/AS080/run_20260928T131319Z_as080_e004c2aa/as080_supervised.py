#!/usr/bin/env python3
"""AS080 supervising wrapper: enforces the memory and wall-time bounds that
macOS refuses to let the payload set itself.

- memory  <= 512 MB: RSS polled every 50 ms via `ps -o rss=` (KB), SIGKILL
  on breach (macOS forbids lowering RLIMIT_AS/RLIMIT_DATA for the process).
- wall    <= 120 s: hard SIGKILL at 120 s.
- CPU     <= 120 s: enforced inside the payload via RLIMIT_CPU (OS-enforced).
- threads = 1: payload pins OMP/OPENBLAS/MKL/NUMEXPR/VECLIB to 1 thread.

Records as080_bounds.json: wall_s, max_rss_kb, killed flags, how each bound
was enforced.
"""
import json
import os
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WALL_S = 120
MEM_KB = 512 * 1024
POLL_S = 0.05

payload = os.path.join(HERE, "as080_hydrostatic_slope.py")
t0 = time.time()
outf = open(os.path.join(HERE, "raw_output.txt"), "w")
errf = open(os.path.join(HERE, "err_and_time.txt"), "w")
p = subprocess.Popen([sys.executable, payload], stdout=outf, stderr=errf)

max_rss_kb = 0
killed = {"memory": False, "wall": False}
while p.poll() is None:
    try:
        rss_kb = int(subprocess.check_output(
            ["ps", "-o", "rss=", "-p", str(p.pid)]).strip() or 0)
    except Exception:
        rss_kb = 0
    max_rss_kb = max(max_rss_kb, rss_kb)
    if rss_kb > MEM_KB:
        os.kill(p.pid, signal.SIGKILL)
        killed["memory"] = True
        break
    if time.time() - t0 > WALL_S:
        os.kill(p.pid, signal.SIGKILL)
        killed["wall"] = True
        break
    time.sleep(POLL_S)
rc = p.wait()
wall = time.time() - t0
outf.close()
errf.close()

bounds = {
    "wall_s": wall, "wall_limit_s": WALL_S,
    "max_rss_kb": max_rss_kb, "memory_limit_kb": MEM_KB,
    "poll_interval_s": POLL_S,
    "killed": killed,
    "exit_code": rc,
    "enforced": {
        "cpu": "RLIMIT_CPU=120 s set inside the payload (OS-enforced "
               "SIGXCPU); macOS refuses RLIMIT_AS lowering for the process",
        "memory": "RSS supervised via `ps -o rss=` every 50 ms + SIGKILL on "
                  "breach (actual enforcement; sampling interval 50 ms)",
        "wall": "SIGKILL at 120 s wall by this wrapper",
        "threads": "OMP/OPENBLAS/MKL/NUMEXPR/VECLIB_MAXIMUM_THREADS=1 set "
                   "before numpy import; single-threaded CPython"}}
with open(os.path.join(HERE, "as080_bounds.json"), "w") as f:
    json.dump(bounds, f, indent=1)
print(json.dumps(bounds, indent=1))
