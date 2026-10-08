#!/usr/bin/env python3
"""CFG427 launcher (FROZEN_CRITERIA.md): two at a time, 4 threads each, niced."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_pm.py")
LOG = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg424_work"))
def start(eps, mix, name):
    env = dict(os.environ, CFG424_THREADS="4", CFG424_FRET="1.0", CFG424_NSEED="256", CFG424_SEED="359", CFG424_NOCOMP="0", CFG424_EPS=eps)
    return subprocess.Popen(["nice", "-n", "10", sys.executable, ENG, "RES", "FLAT", "canonical", "256", "0", mix],
                            stdout=open(os.path.join(LOG, f"cfg427_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(LOG, "run_427_launcher.log"), "a") as lg:
    for pair in ((("0.0385", "MIXA", "E1"), ("0.154", "MIXA", "E2")), (("0.077", "MIXB", "G1"), ("0.077", "HOT1", "G2"))):
        ps = [(p[2], start(*p)) for p in pair]
        for n, p in ps:
            print(n, "rc", p.wait(), file=lg, flush=True)
