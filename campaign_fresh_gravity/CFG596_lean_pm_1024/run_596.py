#!/usr/bin/env python3
"""CFG596 launcher (FROZEN_CRITERIA.md, f6c27d401).  Each job runs cfg596_pm.py under nice 10 in its own folder
_external_data/cfg596_work/<JOB>/ with a memory watchdog: the job is killed if its resident memory exceeds 50 GB or if system swap use
grows by more than 4 GB during the job (frozen abort rule).  Watchdog samples go to <JOB>/watch.log.
  python3 run_596.py serial JOB [JOB ...]     run jobs one after another (production: P0 then P1 [then P2]), start detached with nohup
  python3 run_596.py par JOB [JOB ...]        run jobs at the same time (small validation jobs only)
Jobs:  VEa  exact RES can N256 L200 NSEED256 RMIN 1.56   (CFG527 reproduction, gate V-E(a), V-G)
       VEb  exact S0      N256 L100 NSEED512 RMIN 0.78125 (CFG530 S0_L100_N256 reproduction, gate V-E(b))
       VLs / VLr  lean S0 / RES can, N256 L100 NSEED512 RMIN 0.78125 (gate V-L vs CFG530)
       VMs  lean S0 N512 L100 NSEED512 (full run, V-M + reported comparison with CFG530 S0_L100_N512)
       VMr  lean RES can N512 L100 NSEED512, first 12 force calls (V-M)
       P0 / P1 / P2  production: lean S0 / RES can / RES alt, N1024 L100 NSEED1024 RMIN 0.78125, 14 threads, spill on."""
import os, sys, subprocess, time, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "cfg596_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg596_work"))
RSS_MAX_GB = 50.0; SWAP_GROW_MB = 4096.0
JOBS = {
    "VEa": dict(sw="RES", foot="canonical", N=256, MODE="exact", L="200", NSEED="256", RMIN="1.56", THREADS="3"),
    "VEb": dict(sw="S0", foot="canonical", N=256, MODE="exact", L="100", NSEED="512", RMIN="0.78125", THREADS="3"),
    "VLs": dict(sw="S0", foot="canonical", N=256, MODE="lean", L="100", NSEED="512", RMIN="0.78125", THREADS="3"),
    "VLr": dict(sw="RES", foot="canonical", N=256, MODE="lean", L="100", NSEED="512", RMIN="0.78125", THREADS="3"),
    "VMs": dict(sw="S0", foot="canonical", N=512, MODE="lean", L="100", NSEED="512", RMIN="0.78125", THREADS="12", SPILL="1"),
    "VMr": dict(sw="RES", foot="canonical", N=512, MODE="lean", L="100", NSEED="512", RMIN="0.78125", THREADS="12", SPILL="1", MAXSTEPS="12"),
    "P0": dict(sw="S0", foot="canonical", N=1024, MODE="lean", L="100", NSEED="1024", RMIN="0.78125", THREADS="14", SPILL="1"),
    "P1": dict(sw="RES", foot="canonical", N=1024, MODE="lean", L="100", NSEED="1024", RMIN="0.78125", THREADS="14", SPILL="1"),
    "P2": dict(sw="RES", foot="alt", N=1024, MODE="lean", L="100", NSEED="1024", RMIN="0.78125", THREADS="14", SPILL="1"),
}

def swap_used_mb():
    out = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"used = ([\d.]+)M", out); return float(m.group(1)) if m else 0.0
def rss_gb(pid):
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return float(out) / 1e6 if out else 0.0                     # ps rss in KiB

def start(job):
    s = JOBS[job]; d = os.path.join(WORK, job); os.makedirs(d, exist_ok=True)
    env = dict(os.environ, CFG596_MODE=s["MODE"], CFG596_L=s["L"], CFG596_NSEED=s["NSEED"], CFG596_RMIN=s["RMIN"], CFG596_THREADS=s["THREADS"],
               CFG596_WORK=d, CFG596_SPILL=s.get("SPILL", "0"), CFG596_MAXSTEPS=s.get("MAXSTEPS", "100000"))
    json.dump(dict(job=job, spec=s, start=time.strftime("%Y-%m-%d %H:%M")), open(os.path.join(d, "job.json"), "w"), indent=1)
    log = open(os.path.join(d, "engine.log"), "w")
    p = subprocess.Popen(["nice", "-n", "10", sys.executable, ENGINE, s["sw"], s["foot"], str(s["N"])], stdout=log, stderr=subprocess.STDOUT, env=env)
    return dict(job=job, p=p, d=d, swap0=swap_used_mb(), peak=0.0, wl=open(os.path.join(d, "watch.log"), "a"))

def watch(runs):
    while any(r["p"].poll() is None for r in runs):
        for r in runs:
            if r["p"].poll() is not None: continue
            g = rss_gb(r["p"].pid); sw = swap_used_mb(); r["peak"] = max(r["peak"], g)
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"rss {g:.2f} GB peak {r['peak']:.2f} swap_used {sw:.0f} MB (start {r['swap0']:.0f})", file=r["wl"], flush=True)
            if g > RSS_MAX_GB or sw - r["swap0"] > SWAP_GROW_MB:
                print("ABORT (frozen rule): rss", g, "swap growth", sw - r["swap0"], file=r["wl"], flush=True); r["p"].kill()
        time.sleep(20)
    for r in runs:
        print("exit", r["p"].returncode, "peak_rss_gb", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=r["wl"], flush=True)

if __name__ == "__main__":
    mode, jobs = sys.argv[1], sys.argv[2:]
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "run_596_launcher.log"), "a") as lg:
        print("start", mode, jobs, time.strftime("%Y-%m-%d %H:%M"), os.getpid(), file=lg, flush=True)
        if mode == "par":
            rs = [start(j) for j in jobs]; watch(rs)
            for r in rs: print(r["job"], "rc", r["p"].returncode, "peak", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
        else:
            for j in jobs:
                r = start(j); watch([r])
                print(j, "rc", r["p"].returncode, "peak", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
                if r["p"].returncode != 0:
                    print("stopping the serial queue after a failure", file=lg, flush=True); break
