#!/usr/bin/env python3
"""CFG498 launcher (FROZEN_CRITERIA.md d9c739010): the 256^3 queue, two workers x 3 threads (6 threads total), nice 10.
Scored: V1-CAP / V2-CAP on both footings; MUTATE-N (no compensation, no cap; must fail).  Control C1 = MUTATE-U (cap removed:
reproduces CFG487 POST-HOC V1-CATCH canonical).  Reported: MUTA-CAP (FRW-firing clock with the cap).
Outputs and logs go to ../_external_data/cfg498_work (not committed)."""
import os, sys, subprocess, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg498_work"))
NP = sys.argv[1] if len(sys.argv) > 1 else "256"
#        name          SW     CAP  NOCOMP foot
QUEUE = [("V1CAP",    "V1",   "1", "0", "canonical"), ("MUTN",  "V1",   "1", "1", "canonical"),
         ("V1CAP",    "V1",   "1", "0", "alt"),       ("MUTU",  "V1",   "0", "0", "canonical"),
         ("V2CAP",    "V2",   "1", "0", "canonical"), ("V2CAP", "V2",   "1", "0", "alt"),
         ("MUTACAP",  "MUTA", "1", "0", "canonical")]
if len(sys.argv) > 2:
    QUEUE = [q for q in QUEUE if f"{q[0]}_{q[4]}" in sys.argv[2].split(",")]


def one(job):
    name, sw, cap, nocomp, foot = job
    env = dict(os.environ, CFG498_THREADS="3", CFG498_SW=sw, CFG498_CONF="CAP", CFG498_CAP=cap, CFG498_NOCOMP=nocomp,
               CFG498_NSEED=str(max(256, int(NP))))
    log = os.path.join(WORK, f"cfg498_{name}_{foot}_N{NP}.log")
    t = time.time()
    rc = subprocess.call(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg498_pm.py"), "RES", "FLAT", foot, NP, "0", "MIXA"],
                         stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env)
    with open(os.path.join(WORK, "run_498_launcher.log"), "a") as lg:
        print(f"{name} {foot} N{NP} rc {rc} {time.time() - t:.0f} s", file=lg, flush=True)
    return rc


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        print(list(ex.map(one, QUEUE)))
