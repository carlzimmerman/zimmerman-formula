#!/usr/bin/env python3
"""AS065 supervisor: enforce wall <= 150 s and RSS <= 512 MiB on the lane child.

macOS 26 rejects in-process RLIMIT_AS lowering, so the 512 MiB ceiling is
enforced from outside: poll the child's RSS (ps -o rss=, KB) every 0.1 s and
SIGKILL on exceedance.  Also a wall guard at 150 s (the child's own
RLIMIT_CPU=110 s is the primary CPU bound).  Records the observed max RSS and
any kill event to the run dir.
"""
import subprocess
import sys
import time

RUNDIR = sys.argv[1]
LANE = sys.argv[2]
RSS_LIMIT_KB = 512 * 1024      # 512 MiB
WALL_LIMIT_S = 150.0

t0 = time.time()
child = subprocess.Popen([sys.executable, LANE, RUNDIR],
                         stdout=open(f"{RUNDIR}/AS065_lane_stdout.txt", "w"),
                         stderr=open(f"{RUNDIR}/AS065_lane_stderr.txt", "w"))
max_rss_kb = 0
killed = None
while child.poll() is None:
    try:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(child.pid)],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if out:
            kb = int(out.split()[0])
            max_rss_kb = max(max_rss_kb, kb)
            if kb > RSS_LIMIT_KB:
                killed = f"RSS {kb} KB > 512 MiB"
                child.kill()
                break
    except Exception:
        pass
    if time.time() - t0 > WALL_LIMIT_S:
        killed = f"wall {time.time() - t0:.1f} s > 150 s"
        child.kill()
        break
    time.sleep(0.1)
child.wait()
wall = time.time() - t0
with open(f"{RUNDIR}/AS065_supervisor.json", "w") as f:
    import json
    json.dump({"max_rss_kb": max_rss_kb, "wall_s": round(wall, 2),
               "rss_limit_kb": RSS_LIMIT_KB, "wall_limit_s": WALL_LIMIT_S,
               "kill_event": killed, "child_exit": child.returncode}, f, indent=1)
print(f"supervisor: wall {wall:.2f} s, max RSS {max_rss_kb / 1024:.1f} MiB, "
      f"kill_event={killed}, child_exit={child.returncode}")
sys.exit(child.returncode if killed is None else 2)
