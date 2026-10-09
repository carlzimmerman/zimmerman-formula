#!/usr/bin/env python3
"""CFG518 launcher (FROZEN_CRITERIA.md), run detached (nohup): 256^3 seed 359, 4 threads each, nice 10.
Stage 1: DC-can + DC-alt in parallel.  Stage 2: MUTATE (no compensation, census, canonical) + K1 (f_ret = 1, canonical) in parallel.
'512' as argv[1]: DC-can at 512^3, NSEED 512, 8 threads (only after a 256^3 PASS and when no other 512^3 job runs)."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg518_work"))
os.makedirs(WORK, exist_ok=True)
def start(foot, name, npg=256, th="4", nseed="256", mode="census", nocomp="0"):
    env = dict(os.environ, CFG518_THREADS=th, CFG518_NSEED=nseed, CFG518_FRET_MODE=mode, CFG518_NOCOMP=nocomp)
    return subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg518_pm.py"), "RES", "FLAT", foot, str(npg), "0", "MIXA"],
                            stdout=open(os.path.join(WORK, f"cfg518_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(WORK, "run_518_launcher.log"), "a") as lg:
    print("start", time.strftime("%Y-%m-%d %H:%M"), sys.argv[1:], file=lg, flush=True)
    if len(sys.argv) > 1 and sys.argv[1] == "512":
        print("DC-can-512 rc", start("canonical", "DCcan512", 512, "8", "512").wait(), time.strftime("%H:%M"), file=lg, flush=True)
    else:
        for stage in (lambda: [("DC-can", start("canonical", "DCcan")), ("DC-alt", start("alt", "DCalt"))],
                      lambda: [("MUTATE", start("canonical", "MUTATE", nocomp="1")), ("K1", start("canonical", "K1", mode="one"))]):
            for n, p in stage():
                print(n, "rc", p.wait(), time.strftime("%H:%M"), file=lg, flush=True)
