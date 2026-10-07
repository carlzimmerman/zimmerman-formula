#!/usr/bin/env python3
"""CFG414 launcher: x = 0.4 at 512^3, canonical then alt, one at a time with 8 threads, niced (engine).  Waits for other PM jobs."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg414_work"))
def busy():
    out = subprocess.run(["pgrep", "-f", r"cfg3[0-9][0-9]_(run_all|pm)|cfg41[0-3]_(run_all|pm)|cfg44[0-9]_.*pm"], capture_output=True, text=True).stdout.split()
    return [p for p in out if int(p) != os.getpid()]
os.makedirs(WORK, exist_ok=True)
with open(os.path.join(WORK, "cfg414_launcher.log"), "a") as lg:
    while busy():
        print(f"waiting ({time.strftime('%H:%M')})", file=lg, flush=True); time.sleep(300)
    for f in ("canonical", "alt"):
        tag = f"RES_Rc3_MIXA_X0.4_FLAT_{f}_N512"
        if os.path.exists(os.path.join(WORK, f"cfg414_{tag}.json")):
            print(tag + " (exists)", file=lg, flush=True); continue
        env = dict(os.environ, CFG414_THREADS="8", CFG414_MUTATE="0", CFG414_NSEED="512")
        with open(os.path.join(WORK, f"cfg414_{tag}.log"), "w") as o:
            rc = subprocess.call([sys.executable, os.path.join(HERE, "cfg414_pm.py"), "RES", "FLAT", f, "512", "3.0", "MIXA", "0.4"], stdout=o, stderr=subprocess.STDOUT, env=env)
        print(f"{tag} rc={rc}", file=lg, flush=True)
