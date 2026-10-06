#!/usr/bin/env python3
"""CFG374 launcher (resumable): RES R_c = 3, A0-FLAT, 256^3, T in {1e6 (primary), 1e4} K x {canonical, alt}; 2 at a time x 2 threads, niced.
Criteria: FROZEN_CRITERIA.md (733d27623).  Run from this directory."""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg374_work"))
RUNS = [(T, f) for T in ("MIXA", "MIXB") for f in ("canonical", "alt")]
def go(r):
    T, f = r; t = f"RES_Rc3_{T}_FLAT_{f}_N256"
    if os.path.exists(os.path.join(WORK, f"cfg374_{t}.json")):
        return t + " (exists)"
    env = dict(os.environ, CFG374_THREADS="2", CFG374_MUTATE="0")
    with open(os.path.join(WORK, f"cfg374_{t}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg374_pm.py"), "RES", "FLAT", f, "256", "3.0", T], stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc}"
if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "cfg374_launcher.log"), "a") as lg, ThreadPoolExecutor(4) as ex:
        for m in ex.map(go, RUNS):
            print(m, file=lg, flush=True)
