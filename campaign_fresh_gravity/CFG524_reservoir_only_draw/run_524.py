#!/usr/bin/env python3
"""CFG524 launcher (FROZEN_CRITERIA.md), run detached (nohup): runs the named jobs one after another (start two launchers for two at once).
256^3 seed 359 NSEED 256, 8 threads, nice 10.  Job names: <RUN>_L<box>, RUN in R2can R2alt R1can R1alt K1 (f_ret = 1, R2) MUTATE (draw SC = cfg521),
box in 50 25 100 200.
Each job is claimed atomically (mkdir WORK/claims/<job>) and skipped if claimed or if its result JSON exists, so several launchers can share
one job list without running a job twice.  CFG524_LAUNCH_THREADS sets the per-run threads (default 8).  '512R2' / '512R1': L = 200 canonical at 512^3, NSEED 512 (only after a 256^3 PASS, one 512^3 job at a time)."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg524_work"))
os.makedirs(WORK, exist_ok=True)
RUNS = {"R2can": ("R2", "canonical", "census"), "R2alt": ("R2", "alt", "census"), "R1can": ("R1", "canonical", "census"),
        "R1alt": ("R1", "alt", "census"), "K1": ("R2", "canonical", "one"), "MUTATE": ("SC", "canonical", "census")}
def jobspec(job):
    if job.startswith("512"):
        draw, foot, mode, L, npg, nseed = job[3:], "canonical", "census", 200.0, 512, "512"
    else:
        r, b = job.split("_L"); draw, foot, mode = RUNS[r]; L, npg, nseed = float(b), 256, "256"
    return draw, foot, mode, L, npg, nseed
def result_json(job):
    draw, foot, mode, L, npg, _ = jobspec(job)
    return os.path.join(WORK, f"cfg524_RES_TA_MIXA_MASSCONS_fret{mode}_FLAT_{foot}_N{npg}" + (f"_L{L:g}" if L != 200.0 else "") + f"_draw{draw}.json")
def claim(job):
    os.makedirs(os.path.join(WORK, "claims"), exist_ok=True)
    if os.path.exists(result_json(job)): return False
    try:
        os.mkdir(os.path.join(WORK, "claims", job)); return True
    except FileExistsError:
        return False
def start(job):
    draw, foot, mode, L, npg, nseed = jobspec(job)
    rmin = 1.56 if L == 200.0 else 2 * L / 256
    env = dict(os.environ, CFG524_THREADS=os.environ.get("CFG524_LAUNCH_THREADS", "8"), CFG524_NSEED=nseed, CFG524_FRET_MODE=mode, CFG524_NOCOMP="0", CFG524_DRAW=draw,
               CFG524_L=f"{L:g}", CFG524_RMIN=repr(rmin))
    return subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg524_pm.py"), "RES", "FLAT", foot, str(npg), "0", "MIXA"],
                            stdout=open(os.path.join(WORK, f"cfg524_{job}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(WORK, "run_524_launcher.log"), "a") as lg:
    print("start", time.strftime("%Y-%m-%d %H:%M"), sys.argv[1:], file=lg, flush=True)
    for job in sys.argv[1:]:
        if not claim(job):
            print(job, "skipped (claimed or done)", file=lg, flush=True); continue
        print(job, "rc", start(job).wait(), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
