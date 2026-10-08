#!/usr/bin/env python3
"""CFG501 launcher (FROZEN_CRITERIA.md 7b71dd9b5): the 256^3 queue, two workers x 3 threads (6 threads total), nice 10.
Scored: V1-U / V2-U (draw from UNSETTLED cold energy, capped) on both footings; MUTATE-N (no compensation, no cap; must fail).
Control C1: PROP (CFG498's weight, cap on, V1 canonical) must reproduce CFG498's V1-CAP canonical bit for bit.
Outputs and logs go to ../_external_data/cfg501_work (not committed)."""
import os, sys, subprocess, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg501_work"))
NP = sys.argv[1] if len(sys.argv) > 1 else "256"
#        name     SW    DRAW         NOCOMP foot
QUEUE = [("PROP", "V1", "PROP",      "0", "canonical"), ("V1U", "V1", "UNSETTLED", "0", "canonical"),
         ("V1U",  "V1", "UNSETTLED", "0", "alt"),       ("V2U", "V2", "UNSETTLED", "0", "canonical"),
         ("V2U",  "V2", "UNSETTLED", "0", "alt"),       ("MUTN", "V1", "UNSETTLED", "1", "canonical")]
if len(sys.argv) > 2:
    QUEUE = [q for q in QUEUE if f"{q[0]}_{q[4]}" in sys.argv[2].split(",")]


def one(job):
    name, sw, draw, nocomp, foot = job
    env = dict(os.environ, CFG501_THREADS="3", CFG501_SW=sw, CFG501_CONF="CAP", CFG501_CAP="1", CFG501_NOCOMP=nocomp,
               CFG501_DRAW=draw, CFG501_NSEED=str(max(256, int(NP))))
    log = os.path.join(WORK, f"cfg501_{name}_{foot}_N{NP}.log")
    t = time.time()
    rc = subprocess.call(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg501_pm.py"), "RES", "FLAT", foot, NP, "0", "MIXA"],
                         stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env)
    with open(os.path.join(WORK, "run_501_launcher.log"), "a") as lg:
        print(f"{name} {foot} N{NP} rc {rc} {time.time() - t:.0f} s", file=lg, flush=True)
    return rc


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        print(list(ex.map(one, QUEUE)))
