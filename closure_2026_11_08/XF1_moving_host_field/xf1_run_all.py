#!/usr/bin/env python3
"""XF1 Stage B launcher: runs every line of xf1_runlist.txt, at most 4 at a time, one thread each, nice 10, checkpointed
(a rerun resumes unfinished runs; finished ones exit at once). Stops launching if the free disk falls under 2 GiB
(the lane's rule) and says so. Logs in logs/<tag>.log."""
import os, sys, time, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONHASHSEED="0")
NPAR = int(sys.argv[1]) if len(sys.argv) > 1 else 4
os.makedirs("logs", exist_ok=True)
lines = [l.strip() for l in open("xf1_runlist.txt") if l.strip()]
running = []


def free_gib():
    return shutil.disk_usage(".").free / 2 ** 30


def tag_of(line):
    return line.replace("--", "").replace(" ", "_")


i = 0; stopped = False
while i < len(lines) or running:
    running = [(p, t) for p, t in running if p.poll() is None]
    while len(running) < NPAR and i < len(lines) and not stopped:
        if free_gib() < 2.0:
            print(f"STOP: {free_gib():.2f} GiB free < 2 GiB; not launching run {i + 1}/{len(lines)}", flush=True); stopped = True; break
        line = lines[i]; i += 1
        log = open(os.path.join("logs", tag_of(line) + ".log"), "a")
        p = subprocess.Popen(["nice", "-n", "10", sys.executable, "-B", "xf1_hydro.py"] + line.split(), stdout=log, stderr=subprocess.STDOUT, env=ENV)
        running.append((p, line)); print(f"[{time.strftime('%H:%M:%S')}] start {i}/{len(lines)}: {line}", flush=True)
    if stopped and not running:
        break
    time.sleep(5)
print("ALLDONE" if not stopped else "STOPPED (disk)", flush=True)
