#!/usr/bin/env python3
"""Run a set of X10 runs, at most --par at once, each OMP_NUM_THREADS=1 nice -n 15 MallocMediumZone=0, resumed from its
checkpoint whenever a production run exits 3 (the 27-min guard). A job is skipped when its output json exists. Before each
start the machine's free+inactive memory must be >= 6 GB (vm_stat), else it waits. (Follows X8's x8_batch.py.)

  python3 x10_batch.py --set repro|single|single_mutate|main|numtests|mutate [--par 3] [--h 20,10,5]
  python3 x10_batch.py --set numtests --case canonical,O2,3        (the (b) deciding case, FROZEN §4)
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
X8DIR = HERE.parent / "X8_soft_side_caustics"
ap = argparse.ArgumentParser()
ap.add_argument("--set", required=True, choices=["repro", "single", "single_mutate", "main", "numtests", "mutate"])
ap.add_argument("--par", type=int, default=3)
ap.add_argument("--h", default="20,10,5")
ap.add_argument("--case", default="canonical,O2,3")
a = ap.parse_args()
hs = [int(float(x)) for x in a.h.split(",")]
REPRO_OUT = HERE / "work" / "x8repro"


def job_run(foot, orbit, ti, h, extra=(), start="comoving", mutate=False):
    tag = f"{foot}_{orbit}_ti{ti}_h{h}"
    tag += "".join({"--dt-half": "_dthalf", "--box-half": "_boxhalf", "--tol-tight": "_toltight"}[e] for e in extra)
    tag += ("_rest" if start == "rest" else "") + ("_MUTATE" if mutate else "")
    cmd = [str(HERE / "x10_run.py"), "--foot", foot, "--orbit", orbit, "--ti", str(ti), "--h", str(h), "--start", start]
    cmd += list(extra)
    return {"tag": tag, "cmd": cmd, "out": HERE / "runs" / f"{tag}.json", "env": {"X10_MUTATE": "1"} if mutate else {},
            "resumable": True}


def job_x8(foot, orbit, ti, h):
    tag = f"x8repro_{foot}_{orbit}_ti{ti}_h{h}"
    cmd = [str(X8DIR / "x8_run.py"), "--foot", foot, "--orbit", orbit, "--ti", str(ti), "--h", str(float(h))]
    return {"tag": tag, "cmd": cmd, "out": REPRO_OUT / "runs" / f"{foot}_{orbit}_ti{ti}_h{h}.json",
            "env": {"X8_OUT": str(REPRO_OUT)}, "resumable": True}


def job_single(mode, mass, foot, h, mutate=False):
    suf = "_MUTATE" if mutate else ""
    tag = f"single_{mode}_{mass}_{foot}_h{h}{suf}"
    cmd = [str(HERE / "x10_validate.py"), "--single", mode, "--mass", mass, "--foot", foot, "--h", str(h)]
    return {"tag": tag, "cmd": cmd, "out": HERE / "work" / f"{tag}.json", "env": {"X10_MUTATE": "1"} if mutate else {},
            "resumable": False}


jobs = []
if a.set == "repro":
    REPRO_OUT.mkdir(parents=True, exist_ok=True)
    for foot, orb, ti in (("canonical", "O2", 3), ("canonical", "O1", 9)):
        jobs.append(job_x8(foot, orb, ti, 10))
        jobs.append(job_run(foot, orb, ti, 10, start="rest"))
elif a.set in ("single", "single_mutate"):
    modes = ("vcm", "iso") if a.set == "single" else ("vcm",)
    for h in hs:
        for mode in modes:
            for mass in ("MW", "M31"):
                for foot in ("canonical", "alt"):
                    jobs.append(job_single(mode, mass, foot, h, mutate=(a.set == "single_mutate")))
elif a.set == "main":
    for h in hs:
        for foot in ("canonical", "alt"):
            for orb in ("O1", "O2"):
                for ti in (3, 6, 9):
                    jobs.append(job_run(foot, orb, ti, h))
elif a.set == "mutate":
    for foot in ("canonical", "alt"):
        for orb in ("O1", "O2"):
            for ti in (3, 6, 9):
                jobs.append(job_run(foot, orb, ti, 10, mutate=True))
else:
    foot, orb, ti = a.case.split(",")
    for flag in ("--dt-half", "--box-half", "--tol-tight"):
        jobs.append(job_run(foot, orb, int(ti), 10, extra=(flag,)))


def free_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout.splitlines()
    page = int(out[0].split("page size of")[1].split()[0])
    val = {ln.split(":")[0].strip(): int(ln.split(":")[1].strip().rstrip(".")) for ln in out[1:] if ":" in ln}
    return (val.get("Pages free", 0) + val.get("Pages inactive", 0)) * page / 1e9


def launch(j, resume):
    cmd = ["nice", "-n", "15", sys.executable] + j["cmd"] + (["--resume"] if resume else [])
    env = dict(os.environ, OMP_NUM_THREADS="1", MallocMediumZone="0", **j["env"])
    (HERE / "work").mkdir(exist_ok=True)
    logf = open(HERE / "work" / f"{j['tag']}.stdout", "a")
    return subprocess.Popen(cmd, env=env, stdout=logf, stderr=subprocess.STDOUT)


pending = [j for j in jobs if not j["out"].exists()]
running = []
print(f"{len(pending)} jobs to run ({len(jobs) - len(pending)} already done)", flush=True)
while pending or running:
    for p, j in list(running):
        rc = p.poll()
        if rc is None:
            continue
        running.remove((p, j))
        if rc == 3 and j["resumable"]:
            print(f"  resume {j['tag']}", flush=True)
            running.append((launch(j, True), j))
        elif rc == 0:
            print(f"  done   {j['tag']}", flush=True)
        else:
            print(f"  FAILED {j['tag']} exit {rc}", flush=True)
    while pending and len(running) < a.par:
        if free_gb() < 6.0:
            print(f"  waiting: free+inactive {free_gb():.1f} GB", flush=True)
            time.sleep(60)
            break
        j = pending.pop(0)
        print(f"  start  {j['tag']}", flush=True)
        running.append((launch(j, False), j))
    time.sleep(5)
print("batch finished", flush=True)
