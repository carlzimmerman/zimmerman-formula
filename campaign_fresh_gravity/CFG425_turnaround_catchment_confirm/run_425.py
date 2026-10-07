#!/usr/bin/env python3
"""CFG425 launcher (FROZEN_CRITERIA.md): R1/R2 (256^3 seeds 360/361, 4 threads each) now; R3 (512^3, 8 threads) after other 512^3 PM jobs end."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg425_work"))
os.environ["CFG425_WORK"] = WORK
def start(npg, seed, th, name):
    env = dict(os.environ, CFG424_THREADS=th, CFG424_FRET="1.0", CFG424_NSEED=str(max(256, npg)), CFG424_SEED=str(seed), CFG424_NOCOMP="0")
    return subprocess.Popen(["nice", "-n", "10", sys.executable, ENG, "RES", "FLAT", "canonical", str(npg), "0", "MIXA"],
                            stdout=open(os.path.join(WORK, f"cfg425_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
def busy():
    out = subprocess.run(["pgrep", "-f", r"cfg41[0-9]_(run_all|pm)"], capture_output=True, text=True).stdout.split()
    return [p for p in out if int(p) != os.getpid()]
with open(os.path.join(WORK, "run_425_launcher.log"), "a") as lg:
    ps = [("R1", start(256, 360, "4", "R1")), ("R2", start(256, 361, "4", "R2"))]
    for n, p in ps:
        print(n, "rc", p.wait(), file=lg, flush=True)
    while busy():
        print(f"R3 waiting ({time.strftime('%H:%M')})", file=lg, flush=True); time.sleep(600)
    print("R3 rc", start(512, 359, "8", "R3").wait(), file=lg, flush=True)
