#!/usr/bin/env python3
"""Run a set of X8 production runs (FROZEN_CRITERIA §2, §4), at most --par at once, each OMP_NUM_THREADS=1 nice -n 15,
resumed from its checkpoint whenever it exits 3 (the 27-min guard). A job is skipped when runs/<tag>.json exists.
Before each start the machine's free+inactive memory must be >= 6 GB (vm_stat), else it waits.

  python3 x8_batch.py --set main|mutate|numtests [--par 3] [--h 20,10,5]
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--set", required=True, choices=["main", "mutate", "numtests"])
ap.add_argument("--par", type=int, default=3)
ap.add_argument("--h", default="20,10,5")
a = ap.parse_args()
hs = [float(x) for x in a.h.split(",")]

jobs = []
if a.set in ("main", "mutate"):
    for h in hs:
        for foot in ("canonical", "alt"):
            for orb in ("O1", "O2"):
                for ti in (3, 6, 9):
                    jobs.append(dict(foot=foot, orbit=orb, ti=ti, h=h, extra=[], mutate=(a.set == "mutate")))
else:
    for flag in ("--dt-half", "--box-half", "--tol-tight"):
        jobs.append(dict(foot="canonical", orbit="O2", ti=3, h=10.0, extra=[flag], mutate=False))


def tag_of(j):
    t = f"{j['foot']}_{j['orbit']}_ti{j['ti']}_h{int(j['h'])}"
    t += "".join({"--dt-half": "_dthalf", "--box-half": "_boxhalf", "--tol-tight": "_toltight"}[e] for e in j["extra"])
    return t + ("_MUTATE" if j["mutate"] else "")


def free_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout.splitlines()
    page = int(out[0].split("page size of")[1].split()[0])
    val = {ln.split(":")[0].strip(): int(ln.split(":")[1].strip().rstrip(".")) for ln in out[1:] if ":" in ln}
    return (val.get("Pages free", 0) + val.get("Pages inactive", 0)) * page / 1e9


def launch(j, resume):
    cmd = ["nice", "-n", "15", sys.executable, str(HERE / "x8_run.py"), "--foot", j["foot"], "--orbit", j["orbit"],
           "--ti", str(j["ti"]), "--h", str(j["h"])] + j["extra"] + (["--resume"] if resume else [])
    env = dict(os.environ, OMP_NUM_THREADS="1", MallocMediumZone="0")
    if j["mutate"]:
        env["X8_MUTATE"] = "1"
    log = open(HERE / "work" / f"{tag_of(j)}.stdout", "a")
    return subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT)


(HERE / "work").mkdir(exist_ok=True)
pending = [j for j in jobs if not (HERE / "runs" / f"{tag_of(j)}.json").exists()]
running = []
print(f"{len(pending)} jobs to run ({len(jobs) - len(pending)} already done)", flush=True)
while pending or running:
    for p, j in list(running):
        rc = p.poll()
        if rc is None:
            continue
        running.remove((p, j))
        if rc == 3:
            print(f"  resume {tag_of(j)}", flush=True)
            running.append((launch(j, True), j))
        elif rc == 0:
            print(f"  done   {tag_of(j)}", flush=True)
        else:
            print(f"  FAILED {tag_of(j)} exit {rc}", flush=True)
    while pending and len(running) < a.par:
        if free_gb() < 6.0:
            print(f"  waiting: free+inactive {free_gb():.1f} GB", flush=True)
            time.sleep(60)
            break
        j = pending.pop(0)
        print(f"  start  {tag_of(j)}", flush=True)
        running.append((launch(j, False), j))
    time.sleep(5)
print("batch finished", flush=True)
