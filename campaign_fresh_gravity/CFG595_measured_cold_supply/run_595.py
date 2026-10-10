#!/usr/bin/env python3
"""CFG595 launcher (FROZEN_CRITERIA.md).  Runs this lane's engine copy cfg595_pm.py (CFG527 engine + the CFG595_SUPPLY switch)
with CFG530's study settings (NSEED 512, RMIN = 2 L / 256 at L100, 1.56 at L200, NOFILT, SHELL draw, census f_ret, RC = 0).
Outputs go to ../_external_data/cfg595_work/runs/<job>/.
  nice -n 10 python3 run_595.py one JOB          JOB = <SUP>_<foot>_L<box>_N<mesh>, SUP in ASSUMED | MEAS | ZERO, foot in can | alt
Threads: CFG595_THREADS (default 4)."""
import os, sys, time, json, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "cfg595_pm.py")
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
WORK = os.path.join(EXT, "cfg595_work"); os.makedirs(WORK, exist_ok=True)
DTA_SRC = os.path.join(EXT, "cfg527_work", "cfg361_delta_ta_table.json")
RMIN_STUDY = {100.0: 2 * 100.0 / 256, 200.0: 1.56}                 # = CFG530 run_530.py

def jobspec(job):
    sup, foot, b, n = job.split("_")
    L, N = float(b[1:]), int(n[1:])
    return dict(supply=sup, foot={"can": "canonical", "alt": "alt"}[foot], L=L, N=N, nseed=512, rmin=RMIN_STUDY[L])

def run_one(job):
    s = jobspec(job)
    th = os.environ.get("CFG595_THREADS", "4")
    os.environ.update(CFG527_THREADS=th, CFG527_NSEED=str(s["nseed"]), CFG527_FRET_MODE="census", CFG527_NOCOMP="0",
                      CFG527_DRAW="SHELL", CFG527_L=f"{s['L']:g}", CFG527_RMIN=repr(s["rmin"]), CFG527_MUTATE="0", CFG595_SUPPLY=s["supply"])
    d = os.path.join(WORK, "runs", job); os.makedirs(d, exist_ok=True)
    dta = os.path.join(d, "cfg361_delta_ta_table.json"); shutil.copyfile(DTA_SRC, dta)
    sp = importlib.util.spec_from_file_location("cfg595_pm", ENGINE); mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    mod.WORK = d; mod.DTA_FILE = dta
    mod.RC = 0.0; mod.MIX = "NOFILT"; mod.FRETX = 1.0
    json.dump(dict(job=job, spec=s, engine="campaign_fresh_gravity/CFG595_measured_cold_supply/cfg595_pm.py", threads=th,
                   start=time.strftime("%Y-%m-%d %H:%M")), open(os.path.join(d, "job.json"), "w"), indent=1)
    mod.run("RES", "FLAT", s["foot"], s["N"], 1.0)

if __name__ == "__main__":
    if sys.argv[1] == "one":
        run_one(sys.argv[2])
