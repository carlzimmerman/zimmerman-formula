#!/usr/bin/env python3
"""Parallel 256^3 launcher for CFG420 (seeds 360/361: S0 + RES MIXA, canonical) and CFG421 (RES MIXA, branch DE, both footings).
3 at a time x 2 threads, niced (engine), alongside the 512^3 CFG414 run.  Engine: CFG411 (seed via CFG411_SEED).  Outputs in ../_external_data/cfg411_work/."""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, "..", "CFG411_overnight_convergence", "cfg411_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg411_work"))
RUNS = [("S0", "FLAT", "canonical", 360), ("RES", "FLAT", "canonical", 360), ("S0", "FLAT", "canonical", 361), ("RES", "FLAT", "canonical", 361),
        ("RES", "DE", "canonical", 359), ("RES", "DE", "alt", 359)]
def go(r):
    sw, br, ft, sd = r; tag = f"{sw}_Rc3_MIXA_{br}_{ft}_N256" + (f"_seed{sd}" if sd != 359 else "")
    if os.path.exists(os.path.join(WORK, f"cfg411_{tag}.json")): return tag + " (exists)"
    env = dict(os.environ, CFG411_THREADS="2", CFG411_SEED=str(sd), CFG411_NSEED="256")
    with open(os.path.join(WORK, f"cfg411_{tag}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, ENG, sw, br, ft, "256", "3.0", "MIXA"], stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{tag} rc={rc}"
with open(os.path.join(WORK, "run_420_421_launcher.log"), "a") as lg, ThreadPoolExecutor(3) as ex:
    for m in ex.map(go, RUNS): print(m, file=lg, flush=True)
