#!/usr/bin/env python3
"""CFG530 launcher (FROZEN_CRITERIA.md).  The CFG527 engine is IMPORTED unchanged from CFG527_law_respecting_engine/cfg527_pm.py
(sha256 checked before every job); only its output folder WORK (and the read-only Delta_ta table path) is pointed at
_external_data/cfg530_work/runs/<job>/.
  python3 run_530.py queue JOB [JOB ...]   claim-based queue (mkdir claims/<job>); start up to 4 of these detached (nohup) for <= 256^3
  python3 run_530.py serial JOB [JOB ...]  512^3 jobs: waits until no other job of this lane runs, then runs each alone (8 threads)
  python3 run_530.py one JOB               run one job in this process (used by the two modes above)
Job names: <RUN>_L<box>_N<mesh>  RUN in S0, LRcan, LRalt (study, NSEED 512, RMIN = CFG527 value per box), BXcan, BXalt (L100, RMIN 1.56),
MUTA (SC draw + MIXA, canonical, NSEED 512);  REPcan_L100 / REPcan_L200 / REPalt_L100 / REPalt_L200 (N256, NSEED 256, CFG527 reproduction)."""
import os, sys, time, json, shutil, hashlib, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "CFG527_law_respecting_engine", "cfg527_pm.py"))
ENGINE_SHA = "aeabd0ba4ca5ff1a3b1cc3c17a895821670608397928cfa42d3f03707bd50df0"
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
WORK = os.path.join(EXT, "cfg530_work"); os.makedirs(WORK, exist_ok=True)
DTA_SRC = os.path.join(EXT, "cfg527_work", "cfg361_delta_ta_table.json")
RMIN_STUDY = {100.0: 2 * 100.0 / 256, 200.0: 1.56}

def jobspec(job):
    """-> dict(switch, draw, mix, foot, mode, nocomp, L, N, nseed, rmin)"""
    if job.startswith("REP"):
        run, b = job.split("_L"); L = float(b)
        foot = "canonical" if run == "REPcan" else "alt"
        return dict(switch="RES", draw="SHELL", mix="NOFILT", foot=foot, mode="census", nocomp="0", L=L, N=256, nseed=256,
                    rmin=(1.56 if L == 200.0 else 2 * L / 256))           # = CFG527 run_527.py exactly
    run, rest = job.split("_L"); b, n = rest.split("_N"); L, N = float(b), int(n)
    d = dict(switch="RES", draw="SHELL", mix="NOFILT", foot="canonical", mode="census", nocomp="0", L=L, N=N, nseed=512, rmin=RMIN_STUDY[L])
    if run == "S0": d.update(switch="S0")
    elif run == "LRcan": pass
    elif run == "LRalt": d.update(foot="alt")
    elif run in ("BXcan", "BXalt"): d.update(foot="canonical" if run == "BXcan" else "alt", rmin=1.56)
    elif run == "MUTA": d.update(draw="SC", mix="MIXA")
    else: raise ValueError(job)
    return d

def jobdir(job): return os.path.join(WORK, "runs", job)
def result(job):
    d = jobdir(job)
    if not os.path.isdir(d): return None
    js = [f for f in os.listdir(d) if f.startswith("cfg527_") and f.endswith(".json")]
    return os.path.join(d, js[0]) if js else None
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def run_one(job):
    s = jobspec(job)
    if sha(ENGINE) != ENGINE_SHA:
        raise SystemExit(f"engine sha256 mismatch: {sha(ENGINE)}")
    th = "8" if s["N"] >= 512 else os.environ.get("CFG530_THREADS", "4")
    os.environ.update(CFG527_THREADS=th, CFG527_NSEED=str(s["nseed"]), CFG527_FRET_MODE=s["mode"], CFG527_NOCOMP=s["nocomp"],
                      CFG527_DRAW=s["draw"], CFG527_L=f"{s['L']:g}", CFG527_RMIN=repr(s["rmin"]), CFG527_MUTATE="0")
    d = jobdir(job); os.makedirs(d, exist_ok=True)
    dta = os.path.join(d, "cfg361_delta_ta_table.json"); shutil.copyfile(DTA_SRC, dta)
    assert sha(dta) == sha(DTA_SRC)
    spec = importlib.util.spec_from_file_location("cfg527_pm", ENGINE); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.WORK = d; mod.DTA_FILE = dta                                   # output folder only (engine code untouched)
    mod.RC = 0.0; mod.MIX = s["mix"]; mod.FRETX = 1.0                   # = cfg527_pm.py __main__ with argv RES FLAT foot N 0 MIX
    json.dump(dict(job=job, spec=s, engine=ENGINE.split("zimmerman-formula/")[-1], engine_sha256=ENGINE_SHA, threads=th,
                   start=time.strftime("%Y-%m-%d %H:%M")), open(os.path.join(d, "job.json"), "w"), indent=1)
    mod.run(s["switch"], "FLAT", s["foot"], s["N"], 1.0)

def spawn(job):
    log = open(os.path.join(WORK, f"cfg530_{job}.log"), "w")
    return subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.abspath(__file__), "one", job], stdout=log, stderr=subprocess.STDOUT,
                            env=dict(os.environ))
def claim(job):
    os.makedirs(os.path.join(WORK, "claims"), exist_ok=True)
    if result(job): return False
    try:
        os.mkdir(os.path.join(WORK, "claims", job)); return True
    except FileExistsError:
        return False
def others_running():
    out = []
    for pat in ("run_530.py one", "run_530.py queue"):                   # any job or queue worker of this lane
        out += subprocess.run(["pgrep", "-f", pat], capture_output=True, text=True).stdout.split()
    return [p for p in out if p.strip() and int(p) != os.getpid()]

if __name__ == "__main__":
    mode, jobs = sys.argv[1], sys.argv[2:]
    if mode == "one":
        run_one(jobs[0]); sys.exit(0)
    with open(os.path.join(WORK, "run_530_launcher.log"), "a") as lg:
        print("start", mode, time.strftime("%Y-%m-%d %H:%M"), os.getpid(), jobs, file=lg, flush=True)
        for job in jobs:
            if mode == "serial":
                while others_running():
                    time.sleep(60)
            if not claim(job):
                print(job, "skipped (claimed or done)", file=lg, flush=True); continue
            print(job, "claimed", os.getpid(), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
            print(job, "rc", spawn(job).wait(), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
