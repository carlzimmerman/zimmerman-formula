#!/usr/bin/env python3
"""BX1 launcher (FROZEN_CRITERIA.md 21e1c07e9a), modelled on CFG596's run_596.py. Jobs run ONE AT A TIME (serial), each under
nice 10 in its own folder ../_external_data/bx1_work/<JOB>/, with a watchdog sampled every 20 s: the job is killed if its resident
memory exceeds the cap (8 GB at N <= 256, 20 GB at N 512), if system swap use grows by more than 4 GB during the job, or if free
disk falls below 3 GB. A 512^3 job does not start with less than 8 GB of free disk. The engine writes its JSON after every
snapshot (partial output). Watchdog samples go to <JOB>/watch.log.
  python3 bx1_run.py JOB [JOB ...]        (start detached: nohup ... &)
Jobs:
  KA1            copy, options off, S0 lean N256 L100 NSEED512 seed 359 (CFG596's V-L settings)  -> vs CFG530 S0_L100_N256
  fA fAi fB fBi  256^3 L200 NSEED512, fixed amplitudes, seed 7101 / 7101 inverted / 7102 / 7102 inverted
  r1 .. r5       256^3 L200 NSEED512, random amplitudes, seeds 7201 .. 7205
  pA pAi pB pBi  512^3 L200 NSEED512, fixed amplitudes, seed 7101 / 7101 inverted / 7102 / 7102 inverted (production)
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, subprocess, time, json, re, shutil, ctypes
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "bx1_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "bx1_work"))
SWAP_GROW_MB = 4096.0
T256 = dict(sw="S0", foot="canonical", N=256, MODE="lean", L="200", NSEED="512", RMIN="0.78125", THREADS=os.environ.get("BX1_T256", "8"))
P512 = dict(sw="S0", foot="canonical", N=512, MODE="lean", L="200", NSEED="512", RMIN="0.78125", THREADS=os.environ.get("BX1_T512", "12"), SPILL="1")
JOBS = {"KA1": dict(sw="S0", foot="canonical", N=256, MODE="lean", L="100", NSEED="512", RMIN="0.78125", THREADS=os.environ.get("BX1_T256", "8"), SEED="359")}
for nm, seed, fx, inv in (("A", 7101, 1, 0), ("Ai", 7101, 1, 1), ("B", 7102, 1, 0), ("Bi", 7102, 1, 1)):
    JOBS["f" + nm] = dict(T256, SEED=str(seed), FIXAMP=str(fx), INVERT=str(inv))
    JOBS["p" + nm] = dict(P512, SEED=str(seed), FIXAMP=str(fx), INVERT=str(inv))
for i in range(1, 11):                                           # r6..r10: AMENDMENT A1 section 5 (reported only)
    JOBS[f"r{i}"] = dict(T256, SEED=str(7200 + i))
for nm, seed, fx, inv in (("C", 7103, 1, 0), ("Ci", 7103, 1, 1), ("D", 7104, 1, 0), ("Di", 7104, 1, 1)):   # AMENDMENT A1 section 5
    JOBS["f" + nm] = dict(T256, SEED=str(seed), FIXAMP=str(fx), INVERT=str(inv))
RSS_CAP = {256: 8.0, 512: 20.0}

def swap_used_mb():
    out = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"used = ([\d.]+)M", out); return float(m.group(1)) if m else 0.0
_LP = ctypes.CDLL("/usr/lib/libproc.dylib")
class _RU(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in ("ut", "st", "piw", "iw", "pageins", "wired", "resident", "footprint")] + [("pad", ctypes.c_uint64 * 40)]
def footprint_gb(pid):
    ru = _RU(); return ru.footprint / 1e9 if _LP.proc_pid_rusage(int(pid), 2, ctypes.byref(ru)) == 0 else -1.0
def disk_free_gb(): return shutil.disk_usage(WORK).free / 1e9
def rss_gb(pid):
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return float(out) / 1e6 if out else 0.0

def start(job):
    s = JOBS[job]; d = os.path.join(WORK, job); os.makedirs(d, exist_ok=True)
    env = dict(os.environ, CFG596_MODE=s["MODE"], CFG596_L=s["L"], CFG596_NSEED=s["NSEED"], CFG596_RMIN=s["RMIN"], CFG596_THREADS=s["THREADS"],
               CFG596_WORK=d, CFG596_SPILL=s.get("SPILL", "0"), CFG596_SEED=s["SEED"], CFG596_FIXAMP=s.get("FIXAMP", "0"), CFG596_INVERT=s.get("INVERT", "0"),
               CFG596_NOSAVE="1", CFG596_ICCHECK="1")
    json.dump(dict(job=job, spec=s, start=time.strftime("%Y-%m-%d %H:%M")), open(os.path.join(d, "job.json"), "w"), indent=1)
    log = open(os.path.join(d, "engine.log"), "w")
    p = subprocess.Popen(["nice", "-n", "10", sys.executable, ENGINE, s["sw"], s["foot"], str(s["N"])], stdout=log, stderr=subprocess.STDOUT, env=env)
    return dict(job=job, p=p, d=d, cap=RSS_CAP[s["N"]], swap0=swap_used_mb(), peak=0.0, wl=open(os.path.join(d, "watch.log"), "a"))

def watch(r):
    while r["p"].poll() is None:
        g = rss_gb(r["p"].pid); sw = swap_used_mb(); r["peak"] = max(r["peak"], g); fp = footprint_gb(r["p"].pid); df = disk_free_gb()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"rss {g:.2f} GB peak {r['peak']:.2f} swap_used {sw:.0f} MB (start {r['swap0']:.0f}) footprint {fp:.2f} GB disk_free {df:.1f} GB", file=r["wl"], flush=True)
        if g > r["cap"] or sw - r["swap0"] > SWAP_GROW_MB:
            print("ABORT (watchdog): rss", g, "swap growth", sw - r["swap0"], file=r["wl"], flush=True); r["p"].kill()
        elif df < 3.0:
            print("ABORT (disk guard): free disk", df, "GB", file=r["wl"], flush=True); r["p"].kill()
        time.sleep(20)
    print("exit", r["p"].returncode, "peak_rss_gb", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=r["wl"], flush=True)
    td = os.path.join(r["d"], "tmp")                               # disk-backed temporaries left by a killed job
    if os.path.isdir(td):
        for f in os.listdir(td):
            if f.startswith("df_"): os.remove(os.path.join(td, f))

if __name__ == "__main__":
    jobs = sys.argv[1:]; assert all(j in JOBS for j in jobs), jobs
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "bx1_launcher.log"), "a") as lg:
        print("start", jobs, time.strftime("%Y-%m-%d %H:%M"), os.getpid(), file=lg, flush=True)
        for j in jobs:
            if JOBS[j]["N"] >= 512 and disk_free_gb() < 8.0:
                print(j, "not started: free disk", round(disk_free_gb(), 1), "GB < 8 GB", file=lg, flush=True); break
            r = start(j); watch(r)
            print(j, "rc", r["p"].returncode, "peak", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
            if r["p"].returncode != 0:
                print("stopping the serial queue after a failure", file=lg, flush=True); break
