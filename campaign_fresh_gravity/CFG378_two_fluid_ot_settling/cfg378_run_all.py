#!/usr/bin/env python3
"""CFG378 launcher (resumable; FROZEN_CRITERIA.md 18bfc1a98).  Waits until no cfg376 process is running, then:
DEV 128^3 (not scored): S0 g0 canonical, TWO g0 canonical/alt (C2 + R0 baselines), TWO g1 canonical/alt, TWO g0.1 canonical, TWO g1 canonical MUTATE;
FROZEN 256^3: TWO g1 canonical/alt (primary), TWO g0.1 canonical/alt; then TWO g0 canonical/alt at 256^3 (R0 baselines, stated).
At most 2 processes x 2 threads, niced.  Usage: python3 cfg378_run_all.py [dev|frozen|all]"""
import os, sys, subprocess, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg378_work"))
DEV = [("S0", "canonical", 128, 0, "DEV", 0), ("TWO", "canonical", 128, 0, "DEV", 0), ("TWO", "alt", 128, 0, "DEV", 0),
       ("TWO", "canonical", 128, 1, "DEV", 0), ("TWO", "alt", 128, 1, "DEV", 0), ("TWO", "canonical", 128, 0.1, "DEV", 0),
       ("TWO", "canonical", 128, 1, "DEV", 1)]
FROZEN = [("TWO", "canonical", 256, 1, "", 0), ("TWO", "alt", 256, 1, "", 0), ("TWO", "canonical", 256, 0.1, "", 0),
          ("TWO", "alt", 256, 0.1, "", 0), ("TWO", "canonical", 256, 0, "", 0), ("TWO", "alt", 256, 0, "", 0)]
def busy():
    return any(subprocess.run(["pgrep", "-f", p], capture_output=True).stdout.strip() for p in ("cfg376_run_all", "cfg376_pm"))
def go(r):
    mode, foot, npg, g, tag, mut = r
    t = f"{mode}_g{g:g}_FLAT_{foot}_N{npg}" + (f"_{tag}" if tag else "") + ("_MUTATE" if mut else "")
    if os.path.exists(os.path.join(WORK, f"cfg378_{t}.json")):
        return t + " (exists)"
    while busy():
        time.sleep(60)
    env = dict(os.environ, CFG378_THREADS="2", CFG378_MUTATE=str(mut), CFG378_TAG=tag)
    with open(os.path.join(WORK, f"cfg378_{t}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg378_pm.py"), mode, foot, str(npg), str(g)], stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{t} rc={rc}"
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    runs = (DEV if which in ("dev", "all") else []) + (FROZEN if which in ("frozen", "all") else [])
    os.makedirs(WORK, exist_ok=True)
    while busy():
        time.sleep(60)
    with open(os.path.join(WORK, "cfg378_launcher.log"), "a") as lg, ThreadPoolExecutor(2) as ex:
        for m in ex.map(go, runs):
            print(m, file=lg, flush=True)
