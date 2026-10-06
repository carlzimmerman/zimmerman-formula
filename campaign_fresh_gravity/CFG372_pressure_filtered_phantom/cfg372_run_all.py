#!/usr/bin/env python3
"""CFG372 launcher (resumable): RES R_c = 3, A0-FLAT, 256^3, T in {1e6 (primary), 1e4} K x {canonical, alt}; 2 at a time x 2 threads, niced.
Criteria: FROZEN_CRITERIA.md (733d27623).  Run from this directory."""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg372_work"))
RUNS = [(T, f) for T in (1e6, 1e4) for f in ("canonical", "alt")]
def go(r):
    T, f = r; t = f"RES_Rc3_T{T:.0e}_FLAT_{f}_N256"
    if os.path.exists(os.path.join(WORK, f"cfg372_{t}.json")):
        return t + " (exists)"
    env = dict(os.environ, CFG372_THREADS="2", CFG372_MUTATE="0")
    with open(os.path.join(WORK, f"cfg372_{t}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg372_pm.py"), "RES", "FLAT", f, "256", "3.0", str(T)], stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc}"
if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "cfg372_launcher.log"), "a") as lg, ThreadPoolExecutor(2) as ex:
        for m in ex.map(go, RUNS):
            print(m, file=lg, flush=True)
