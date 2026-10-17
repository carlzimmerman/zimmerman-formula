#!/usr/bin/env python3
"""ARGON11 launcher.  usage: argon11_run.py R1|R2|...|R8   (criteria: FROZEN_CRITERIA.md, commit 2153ca9e0)
Starts frag3d with the frozen parameters, with a watchdog: if a 1024^3 run (CFG650/654/596-type) appears, the job is stopped
and resumed from its last checkpoint once the run is gone."""
import subprocess, sys, time, math, os
from argon11_common import coexistence, background

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/carlzimmerman/new_physics/_external_data/argon11_work"
RUNS = {  # id: (s, N, dx, seed, eps, t_end, Lq_flip)
    "R1": (0.1, 96, 1.0, 1, 1e-4, 700, False),
    "R2": (0.1, 96, 1.0, 2, 1e-4, 700, False),
    "R3": (0.1, 128, 0.75, 1, 1e-4, 700, False),
    "R4": (0.5, 96, 1.0, 1, 1e-4, 500, False),
    "R5": (0.1, 64, 1.0, 1, 1e-4, 700, True),
    "R6": (0.1, 64, 1.0, 1, 1e-4, 700, False),
    "R7": (0.1, 64, 1.0, 1, 1e-6, 800, False),
    "R8": (0.1, 128, 1.0, 3, 1e-4, 700, False),
}
BUSY = r"run_650|run_654|cfg6[0-9][0-9]_pm|cfg596_pm|cfg7[0-9][0-9]\.py"
def busy(): return subprocess.run(["pgrep", "-f", BUSY], capture_output=True).returncode == 0

rid = sys.argv[1]
s, N, dx, seed, eps, tend, flip = RUNS[rid]
M = 100; dt = 0.01
Istar, w2s = coexistence(M)
Lq = (2 + 1.0/M) if flip else (2 - 1.0/M)
I0 = s*Istar
L, a, chi0, om2 = background(M, I0, Lq)
cmd = ["nice", "-n", "10", os.path.join(HERE, "frag3d"), rid, str(N), str(dx), str(dt), str(M), repr(L), repr(a), repr(I0), repr(chi0),
       repr(math.sqrt(om2)), repr(eps), str(seed), str(tend), "25", OUT]
resume = False
while True:
    while busy():
        print(time.strftime("%H:%M:%S"), rid, "waiting: 1024^3-type run live", flush=True); time.sleep(120)
    p = subprocess.Popen(cmd + (["resume"] if resume else []))
    stopped = False
    while p.poll() is None:
        time.sleep(20)
        if busy():
            p.terminate(); p.wait(); stopped = True; print(time.strftime("%H:%M:%S"), rid, "STOPPED: 1024^3-type run appeared", flush=True); break
    if not stopped:
        print(rid, "finished rc", p.returncode, flush=True); sys.exit(p.returncode)
    resume = True
