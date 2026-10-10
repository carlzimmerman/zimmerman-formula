#!/usr/bin/env python3
"""CFG539 launcher (FROZEN_CRITERIA.md): claim-based queue (mkdir claims under _external_data/cfg539_work/claims), each job a subprocess of
cfg539_pm.py with its environment; nice 10; logs in _external_data/cfg539_work/.  Usage: nohup python3 run_539.py [-t THREADS] JOB [JOB ...] &
JOB names: OFF_L100_N128, A{can,alt}_L200_N256, C{can,alt}_..., Acan_NOEDGE_L100_N128, Acan_mob0.5_L200_N256, ..."""
import os, sys, subprocess, time, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg539_work"))
CLAIMS = os.path.join(WORK, "claims")
RMIN = {100: 0.78125, 200: 1.56}

def jobenv(job, nth):
    parts = job.split("_")
    head = parts[0]; L = int([p for p in parts if re.fullmatch(r"L\d+", p)][0][1:]); N = int([p for p in parts if re.fullmatch(r"N\d+", p)][0][1:])
    eom = "OFF" if head == "OFF" else head[0]
    foot = {"can": "canonical", "alt": "alt"}.get(head[1:], "canonical")
    env = {"CFG539_EOM": eom, "CFG539_L": str(L), "CFG539_RMIN": str(RMIN[L]), "CFG539_NSEED": "512", "CFG539_THREADS": str(nth),
           "CFG539_EDGE": "0" if "NOEDGE" in parts else "1", "CFG539_MOB": "1.0", "CFG539_FRET_MODE": "census", "CFG539_MUTATE": "0"}
    for p in parts:
        if p.startswith("mob"): env["CFG539_MOB"] = p[3:]
    return env, foot, N

if __name__ == "__main__":
    args = sys.argv[1:]; nth = 4
    if args and args[0] == "-t":
        nth = int(args[1]); args = args[2:]
    os.makedirs(CLAIMS, exist_ok=True)
    for job in args:
        try:
            os.mkdir(os.path.join(CLAIMS, job))
        except FileExistsError:
            continue
        env, foot, N = jobenv(job, nth)
        e = dict(os.environ); e.update(env)
        for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
            e[v] = str(nth)
        t0 = time.time()
        with open(os.path.join(WORK, f"cfg539_{job}.log"), "w") as lf:
            lf.write(json.dumps({"job": job, "env": env, "foot": foot, "N": N}) + "\n"); lf.flush()
            rc = subprocess.call(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg539_pm.py"), "FLAT", foot, str(N)],
                                 env=e, stdout=lf, stderr=subprocess.STDOUT, cwd=HERE)
            lf.write(f"EXIT {rc} after {time.time() - t0:.0f}s\n")
