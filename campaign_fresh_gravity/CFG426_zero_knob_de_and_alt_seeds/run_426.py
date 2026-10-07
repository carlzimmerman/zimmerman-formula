#!/usr/bin/env python3
"""CFG426 launcher (FROZEN_CRITERIA.md): two at a time, 4 threads each, niced."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_pm.py")
LOG = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg424_work"))
def start(branch, foot, seed, name):
    env = dict(os.environ, CFG424_THREADS="4", CFG424_FRET="1.0", CFG424_NSEED="256", CFG424_SEED=str(seed), CFG424_NOCOMP="0")
    return subprocess.Popen(["nice", "-n", "10", sys.executable, ENG, "RES", branch, foot, "256", "0", "MIXA"],
                            stdout=open(os.path.join(LOG, f"cfg426_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(LOG, "run_426_launcher.log"), "a") as lg:
    for pair in ((("DE", "canonical", 359, "D1"), ("DE", "alt", 359, "D2")), (("FLAT", "alt", 360, "A1"), ("FLAT", "alt", 361, "A2"))):
        ps = [(p[3], start(*p)) for p in pair]
        for n, p in ps:
            print(n, "rc", p.wait(), file=lg, flush=True)
