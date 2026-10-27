#!/usr/bin/env python3
"""
CFG359 launcher: runs every PM run that has no result JSON in ../_external_data/cfg359_work/, 4 at a time with 2 FFT
threads each (at most 8 processes), niced.  CFG359_MUTATE=1 launches the MUTATE runs (T1, Delta_ta := 1) instead.
Run from the repository root:
    python3 campaign_fresh_gravity/CFG359_native_pm_growth/cfg359_run_all.py
    CFG359_MUTATE=1 python3 campaign_fresh_gravity/CFG359_native_pm_growth/cfg359_run_all.py
"""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg359_work"))
MUTATE = os.environ.get("CFG359_MUTATE", "0") == "1"
FOOTS, BRANCHES = ("canonical", "alt"), ("FLAT", "CRIT", "DE")
if MUTATE:
    RUNS = [("T1", "FLAT", f, 256, 1.0) for f in FOOTS]
else:
    RUNS = [("S0", "FLAT", "canonical", 256, 1.0), ("S0", "FLAT", "canonical", 256, 0.01)]
    RUNS += [("T1", b, f, 256, 1.0) for b in BRANCHES for f in FOOTS]
    RUNS += [("T1V", "FLAT", f, 256, 1.0) for f in FOOTS]
    RUNS += [("S1", b, f, 256, 1.0) for b in BRANCHES for f in FOOTS]
    RUNS += [("S0", "FLAT", "canonical", 128, 1.0), ("T1", "FLAT", "canonical", 128, 1.0)]

def tag(sw, br, ft, n, amp):
    return f"{sw}_{br}_{ft}_N{n}" + (f"_amp{amp:g}" if amp != 1 else "") + ("_MUTATE" if MUTATE else "")

def go(r):
    t = tag(*r)
    if os.path.exists(os.path.join(WORK, f"cfg359_{t}.json")):
        return t + " (exists)"
    env = dict(os.environ, CFG359_THREADS="2")
    with open(os.path.join(WORK, f"cfg359_{t}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg359_pm.py"), r[0], r[1], r[2], str(r[3]), str(r[4])],
                             stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc}"

if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with ThreadPoolExecutor(4) as ex:
        for msg in ex.map(go, RUNS):
            print(msg, flush=True)
