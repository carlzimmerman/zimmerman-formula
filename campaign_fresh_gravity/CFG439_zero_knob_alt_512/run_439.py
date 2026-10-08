#!/usr/bin/env python3
"""CFG439 launcher: A (FLAT alt) then B (DE canonical), 512^3, 8 threads, niced; then resumes CFG419's launcher."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_pm.py")
LOG = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg424_work"))
with open(os.path.join(LOG, "run_439_launcher.log"), "a") as lg:
    for br, ft, n in (("FLAT", "alt", "A"), ("DE", "canonical", "B")):
        env = dict(os.environ, CFG424_THREADS="8", CFG424_FRET="1.0", CFG424_NSEED="512", CFG424_SEED="359", CFG424_NOCOMP="0")
        rc = subprocess.call(["nice", "-n", "10", sys.executable, ENG, "RES", br, ft, "512", "0", "MIXA"],
                             stdout=open(os.path.join(LOG, f"cfg439_{n}.log"), "w"), stderr=subprocess.STDOUT, env=env)
        print(n, "rc", rc, file=lg, flush=True)
    d419 = os.path.join(HERE, "..", "CFG419_supply_edge_de_branch_512")
    subprocess.Popen([sys.executable, "cfg419_run_all.py"], cwd=d419, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("CFG419 resumed", file=lg, flush=True)
