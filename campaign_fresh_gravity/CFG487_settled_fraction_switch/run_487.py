#!/usr/bin/env python3
"""CFG487 launcher (FROZEN_CRITERIA.md): the 256^3 queue, two workers at 3 threads each (6 threads total), nice 10.
Scored: V1/V2 EDGE on both footings; MUTATE-A (FRW-firing, canonical); control C1 (T1REPRO, canonical).
Reported: V1-SA and MUTATE-B-SA (switch alone, canonical).  Logs and outputs go to ../_external_data/cfg487_work."""
import os, sys, subprocess, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg487_work"))
NP = sys.argv[1] if len(sys.argv) > 1 else "256"
QUEUE = [("T1REPRO", "EDGE", "canonical"), ("V1", "EDGE", "canonical"), ("V2", "EDGE", "canonical"),
         ("MUTA", "EDGE", "canonical"), ("V1", "EDGE", "alt"), ("V2", "EDGE", "alt"),
         ("V1", "SA", "canonical"), ("MUTA", "SA", "canonical")]
# POST-HOC queue (added after MUTATE-A came back GROWTH OK; README): the switch x the turnaround catchment, no edge balls,
# and its FRW-firing control.  Run with: python3 run_487.py 256 posthoc
POSTHOC = [("V1", "CATCH", "canonical"), ("MUTA", "CATCH", "canonical"), ("V1", "CATCH", "alt")]
if len(sys.argv) > 2 and sys.argv[2] == "posthoc":
    QUEUE = POSTHOC


def one(job):
    sw, conf, foot = job
    env = dict(os.environ, CFG487_THREADS="3", CFG487_SW=sw, CFG487_CONF=conf, CFG487_NSEED=str(max(256, int(NP))))
    log = os.path.join(WORK, f"cfg487_{sw}_{conf}_{foot}_N{NP}.log")
    t = time.time()
    rc = subprocess.call(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg487_pm.py"), "RES", "FLAT", foot, NP, "0", "MIXA"],
                         stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env)
    with open(os.path.join(WORK, "run_487_launcher.log"), "a") as lg:
        print(f"{sw} {conf} {foot} N{NP} rc {rc} {time.time() - t:.0f} s", file=lg, flush=True)
    return rc


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        print(list(ex.map(one, QUEUE)))
