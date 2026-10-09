#!/usr/bin/env python3
"""CFG527 launcher (FROZEN_CRITERIA.md), run detached (nohup): runs the named jobs one after another; start up to 4 launchers on the same job
list -- each job is claimed atomically (mkdir WORK/claims/<job>) and skipped if claimed or if its result JSON exists.
256^3 seed 359 NSEED 256, 4 threads (CFG527_LAUNCH_THREADS), nice 10.  Job names <RUN>_L<box>:
  LRcan / LRalt  draw SHELL, NOFILT, census          K1   SHELL, NOFILT, f_ret = 1, canonical
  MUTA           draw SC, MIXA (= cfg521 DC-can)      MUTB no compensation, NOFILT, canonical
  SHF            draw SHELL, MIXA, canonical (attribution / stability control)
'512LR': L = 200 canonical LR at 512^3, NSEED 512, 8 threads (only after both footings PASS at 256^3; one 512^3 job at a time)."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg527_work"))
os.makedirs(WORK, exist_ok=True)
#        draw,   mix,     foot,        mode,     nocomp
RUNS = {"LRcan": ("SHELL", "NOFILT", "canonical", "census", "0"), "LRalt": ("SHELL", "NOFILT", "alt", "census", "0"),
        "K1": ("SHELL", "NOFILT", "canonical", "one", "0"), "MUTA": ("SC", "MIXA", "canonical", "census", "0"),
        "MUTB": ("SHELL", "NOFILT", "canonical", "census", "1"), "SHF": ("SHELL", "MIXA", "canonical", "census", "0")}
def jobspec(job):
    if job == "512LR":
        return RUNS["LRcan"] + (200.0, 512, "512")
    r, b = job.split("_L"); return RUNS[r] + (float(b), 256, "256")
def result_json(job):
    draw, mix, foot, mode, nc, L, npg, _ = jobspec(job)
    return os.path.join(WORK, f"cfg527_RES_TA{'_NOCOMP' if nc == '1' else ''}_{mix}_MASSCONS_fret{mode}_FLAT_{foot}_N{npg}"
                        + (f"_L{L:g}" if L != 200.0 else "") + f"_draw{draw}.json")
def claim(job):
    os.makedirs(os.path.join(WORK, "claims"), exist_ok=True)
    if os.path.exists(result_json(job)): return False
    try:
        os.mkdir(os.path.join(WORK, "claims", job)); return True
    except FileExistsError:
        return False
def start(job):
    draw, mix, foot, mode, nc, L, npg, nseed = jobspec(job)
    rmin = 1.56 if L == 200.0 else 2 * L / 256
    th = "8" if npg == 512 else os.environ.get("CFG527_LAUNCH_THREADS", "4")
    env = dict(os.environ, CFG527_THREADS=th, CFG527_NSEED=nseed, CFG527_FRET_MODE=mode, CFG527_NOCOMP=nc, CFG527_DRAW=draw,
               CFG527_L=f"{L:g}", CFG527_RMIN=repr(rmin), CFG527_MUTATE="0")
    return subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg527_pm.py"), "RES", "FLAT", foot, str(npg), "0", mix],
                            stdout=open(os.path.join(WORK, f"cfg527_{job}.log"), "w"), stderr=subprocess.STDOUT, env=env)
with open(os.path.join(WORK, "run_527_launcher.log"), "a") as lg:
    print("start", time.strftime("%Y-%m-%d %H:%M"), os.getpid(), sys.argv[1:], file=lg, flush=True)
    for job in sys.argv[1:]:
        if not claim(job):
            print(job, "skipped (claimed or done)", file=lg, flush=True); continue
        print(job, "claimed", os.getpid(), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
        print(job, "rc", start(job).wait(), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
