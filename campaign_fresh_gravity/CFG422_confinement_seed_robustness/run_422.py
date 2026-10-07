#!/usr/bin/env python3
"""CFG422 launcher: CFG414 engine at 256^3, x = 0.4, seeds 359/360/361 x canonical/alt; 3 at a time x 2 threads.  Outputs in ../_external_data/cfg414_work/."""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, "..", "CFG414_confined_switch_512", "cfg414_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg414_work"))
RUNS = [(sd, f) for sd in (359, 360, 361) for f in ("canonical", "alt")]
def go(r):
    sd, f = r; tag = f"RES_Rc3_MIXA_X0.4_FLAT_{f}_N256" + (f"_seed{sd}" if sd != 359 else "")
    if os.path.exists(os.path.join(WORK, f"cfg414_{tag}.json")): return tag + " (exists)"
    env = dict(os.environ, CFG414_THREADS="2", CFG414_SEED=str(sd), CFG414_NSEED="256", CFG414_MUTATE="0")
    with open(os.path.join(WORK, f"cfg414_{tag}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, ENG, "RES", "FLAT", f, "256", "3.0", "MIXA", "0.4"], stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{tag} rc={rc}"
with open(os.path.join(WORK, "run_422_launcher.log"), "a") as lg, ThreadPoolExecutor(3) as ex:
    for m in ex.map(go, RUNS): print(m, file=lg, flush=True)
