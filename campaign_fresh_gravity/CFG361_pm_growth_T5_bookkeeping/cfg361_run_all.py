#!/usr/bin/env python3
"""
CFG361 launcher (resumable): runs every PM run with no result JSON in ../_external_data/cfg361_work/, 4 at a time with 2
FFT threads each (niced to 10 inside the engine), in priority order.  Normal runs first, then the MUTATE pair
(CFG361_MUTATE=1 set per run).  Criteria: FROZEN_CRITERIA.md (6373544c3).  Run from the repository root:
    nohup python3 campaign_fresh_gravity/CFG361_pm_growth_T5_bookkeeping/cfg361_run_all.py > /dev/null 2>&1 &
"""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg361_work"))
FOOTS = ("canonical", "alt")
RUNS = [("T5", "FLAT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("ADD", "FLAT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("T5", "FLAT", f, 256, 1.0, 1) for f in FOOTS]                     # MUTATE: s_c := 0 in the max
RUNS += [("S", "FLAT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("T5", "FLAT", "canonical", 256, 0.01, 0), ("S0", "FLAT", "canonical", 128, 1.0, 0), ("T5", "FLAT", "canonical", 128, 1.0, 0)]
RUNS += [("S1T5", "FLAT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("T5", "CRIT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("S", "CRIT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("T5F", "FLAT", f, 256, 1.0, 0) for f in FOOTS]
RUNS += [("T5", "DE", f, 256, 1.0, 0) for f in FOOTS]

def tag(sw, br, ft, n, amp, mut):
    return f"{sw}_{br}_{ft}_N{n}" + (f"_amp{amp:g}" if amp != 1 else "") + ("_MUTATE" if mut else "")

def go(r):
    t = tag(*r)
    if os.path.exists(os.path.join(WORK, f"cfg361_{t}.json")):
        return t + " (exists)"
    env = dict(os.environ, CFG361_THREADS="2", CFG361_MUTATE=str(r[5]))
    with open(os.path.join(WORK, f"cfg361_{t}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg361_pm.py"), r[0], r[1], r[2], str(r[3]), str(r[4])],
                             stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc}"

if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "cfg361_launcher.log"), "a") as lg, ThreadPoolExecutor(4) as ex:
        for msg in ex.map(go, RUNS):
            print(msg, file=lg, flush=True)
