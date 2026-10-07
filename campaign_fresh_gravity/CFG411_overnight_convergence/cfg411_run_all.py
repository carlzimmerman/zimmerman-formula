#!/usr/bin/env python3
"""CFG411 overnight launcher: waits for every other PM job (cfg378/cfg410/...), then (a) HOT1 x 2 footings at 256^3 (2 parallel x 2 threads),
then (b) S0 and RES MIXA at 512^3 canonical, one at a time with 8 threads.  Criteria: FROZEN_CRITERIA.md.  Run from this directory."""
import os, sys, subprocess, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg411_work"))
def busy():
    out = subprocess.run(["pgrep", "-f", r"cfg3[0-9][0-9]_(run_all|pm)|cfg410_(run_all|pm)|cfg44[0-9]_.*pm"], capture_output=True, text=True).stdout.split()
    return [p for p in out if int(p) != os.getpid()]
def go(args, tag, threads, nseed):
    if os.path.exists(os.path.join(WORK, f"cfg411_{tag}.json")):
        return tag + " (exists)"
    env = dict(os.environ, CFG411_THREADS=str(threads), CFG411_MUTATE="0", CFG411_NSEED=str(nseed))
    with open(os.path.join(WORK, f"cfg411_{tag}.log"), "w") as lg:
        rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg411_pm.py")] + args, stdout=lg, stderr=subprocess.STDOUT, env=env)
    return f"{tag} rc={rc}"
if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "cfg411_launcher.log"), "a") as lg:
        while busy():
            print(f"waiting ({time.strftime('%H:%M')})", file=lg, flush=True); time.sleep(600)
        A = [(["RES", "FLAT", f, "256", "3.0", "HOT1"], f"RES_Rc3_HOT1_FLAT_{f}_N256") for f in ("canonical", "alt")]
        with ThreadPoolExecutor(2) as ex:
            for m in ex.map(lambda a: go(a[0], a[1], 2, 256), A):
                print(m, file=lg, flush=True)
        for args, tag in ((["S0", "FLAT", "canonical", "512", "3.0", "MIXA"], "S0_Rc3_MIXA_FLAT_canonical_N512"),
                          (["RES", "FLAT", "canonical", "512", "3.0", "MIXA"], "RES_Rc3_MIXA_FLAT_canonical_N512")):
            print(go(args, tag, 8, 512), file=lg, flush=True)
