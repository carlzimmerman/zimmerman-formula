#!/usr/bin/env python3
"""CFG460 launcher: S0 then TA, 512^3, seed 360, 8 threads, niced; then the analysis."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_pm.py")
LOG = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg424_work"))
with open(os.path.join(LOG, "run_460_launcher.log"), "a") as lg:
    for sw, n in (("S0", "S0"), ("RES", "TA")):
        env = dict(os.environ, CFG424_THREADS="8", CFG424_FRET="1.0", CFG424_NSEED="512", CFG424_SEED="360", CFG424_NOCOMP="0")
        rc = subprocess.call(["nice", "-n", "10", sys.executable, ENG, sw, "FLAT", "canonical", "512", "0", "MIXA"],
                             stdout=open(os.path.join(LOG, f"cfg460_{n}.log"), "w"), stderr=subprocess.STDOUT, env=env)
        print(n, "rc", rc, file=lg, flush=True)
