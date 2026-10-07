#!/usr/bin/env python3
"""CFG410 launcher: waits until no other PM launcher/engine is running, then 4 runs (BASE/VETO x canonical/alt), 2 at a time x 2 threads, niced.
Criteria: FROZEN_CRITERIA.md.  Run from this directory."""
import os, sys, subprocess, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg410_work"))
RUNS = [(v, f) for v in ("", "VETO") for f in ("canonical", "alt")]
def busy():
    out = subprocess.run(["pgrep", "-f", r"cfg3[0-9][0-9]_(run_all|pm)|cfg44[0-9]_.*pm"], capture_output=True, text=True).stdout.split()
    return [p for p in out if int(p) != os.getpid()]
def go(r):
    v, f = r; t = f"RES_Rc3_MIXA{'_VETO' if v else ''}_FLAT_{f}_N256"
    if os.path.exists(os.path.join(WORK, f"cfg410_{t}.json")):
        return t + " (exists)"
    env = dict(os.environ, CFG410_THREADS="2", CFG410_MUTATE="0")
    args = [sys.executable, os.path.join(HERE, "cfg410_pm.py"), "RES", "FLAT", f, "256", "3.0", "MIXA"] + (["VETO"] if v else [])
    with open(os.path.join(WORK, f"cfg410_{t}.log"), "w") as lg:
        rc = subprocess.call(args, stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc}"
if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "cfg410_launcher.log"), "a") as lg:
        while busy():
            print(f"waiting for other PM jobs ({time.strftime('%H:%M')})", file=lg, flush=True); time.sleep(600)
        with ThreadPoolExecutor(2) as ex:
            for m in ex.map(go, RUNS):
                print(m, file=lg, flush=True)
