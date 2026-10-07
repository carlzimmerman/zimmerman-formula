#!/usr/bin/env python3
"""CFG424 launcher (FROZEN_CRITERIA.md): TA-can + TA-alt in parallel (4 threads each), then MUTATE (no compensation, canonical)."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg424_work"))
def start(foot, name, nocomp="0"):
    env = dict(os.environ, CFG424_THREADS="4", CFG424_FRET="1.0", CFG424_NSEED="256", CFG424_NOCOMP=nocomp)
    return subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg424_pm.py"), "RES", "FLAT", foot, "256", "0", "MIXA"],
                            stdout=open(os.path.join(WORK, f"cfg424_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(WORK, "run_424_launcher.log"), "a") as lg:
    ps = [("TA-can", start("canonical", "TAcan")), ("TA-alt", start("alt", "TAalt"))]
    for n, p in ps:
        print(n, "rc", p.wait(), file=lg, flush=True)
    print("MUTATE rc", start("canonical", "MUTATE", "1").wait(), file=lg, flush=True)
