#!/usr/bin/env python3
"""CFG366 launcher (resumable): 4 PM runs (RES x R_c {1,3} x {canonical, alt}, A0-FLAT, 256^3), 2 at a time x 2 FFT threads,
niced (orchestrator's CPU request: CFG361 is running). Criteria: FROZEN_CRITERIA.md (5f3a22464). Run from this directory."""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg366_work"))
RUNS = [(rc, f) for rc in (1.0, 3.0) for f in ("canonical", "alt")]
def go(r):
    rc, f = r
    t = f"RES_Rc{rc:g}_FLAT_{f}_N256"
    if os.path.exists(os.path.join(WORK, f"cfg366_{t}.json")):
        return t + " (exists)"
    env = dict(os.environ, CFG366_THREADS="2", CFG366_MUTATE="0")
    with open(os.path.join(WORK, f"cfg366_{t}.log"), "w") as lg:
        rc_ = subprocess.call([sys.executable, os.path.join(HERE, "cfg366_pm.py"), "RES", "FLAT", f, "256", str(rc)], stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc_}"
if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with ThreadPoolExecutor(2) as ex:
        for m in ex.map(go, RUNS):
            print(m, flush=True)
