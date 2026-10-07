#!/usr/bin/env python3
"""CFG423 launcher (FROZEN_CRITERIA.md): P1 (R_c=3) and P2 (R_c=1) in parallel, 4 threads each, then MUTATE (f_ret=0.01, R_c=3)."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg423_work"))
def start(rc, fret, name):
    env = dict(os.environ, CFG423_THREADS="4", CFG423_FRET=fret, CFG423_NSEED="256")
    return subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg423_pm.py"), "RES", "FLAT", "canonical", "256", rc, "MIXA"],
                            stdout=open(os.path.join(WORK, f"cfg423_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(WORK, "run_423_launcher.log"), "a") as lg:
    ps = [("P1", start("3.0", "1.0", "P1")), ("P2", start("1.0", "1.0", "P2"))]
    for n, p in ps:
        print(n, "rc", p.wait(), file=lg, flush=True)
    print("MUTATE rc", start("3.0", "0.01", "MUTATE").wait(), file=lg, flush=True)
