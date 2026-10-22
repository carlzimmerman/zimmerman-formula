#!/usr/bin/env python3
"""CFG960 launcher for the pre-registered 1024^3 SCT-M shear test (FROZEN_CRITERIA_1024.md).  A NEW runner: CFG654's launcher is not
edited.  Same guards as CFG654's launcher (RSS > 52 GB or swap growth > 4 GB -> kill; disk guard 3 GB), engine cfg960_sctm_pm.py,
work folders _external_data/cfg960_work/<JOB>/ (outputs named by job).  The engine resumes bit-identically from its rolling
checkpoint (<tag>_ckpt, written after every step whose next force call refreshes the census) when the same job is started again.
  python3 run_960.py serial SC1x [SC2x]
Jobs (production, 1024^3, NOT started by CFG960):
  SC1x  SCT-M (CFG953 R0-R9 as FROZEN_CRITERIA.md S1-S13), M3 unchanged, native_cmb, CANONICAL footing a0 9.3603e-11
  SC2x  the same on the ALT footing a0 1.1312e-10
  (A5: own baryons = CFG953 census f_ret for SC1x / SC2x; SC1m / SC2m = the M2-condensed variant, secondary, reported only, not queued)
Control: NCS0 (CFG654, existing; native_cmb, same ICs; S0 never reads the footing).
A6 (2026-10-22, pre-result): engine with compact body painting (bit-identical); extra abort at footprint > 52 GB (tightening only).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, subprocess, time, json, re, shutil, ctypes
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "cfg960_sctm_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg960_work"))
RSS_MAX_GB = 52.0; SWAP_GROW_MB = 4096.0; DISK_START_GB = 45.0
FOOTPRINT_MAX_GB = 52.0   # A6 (2026-10-22): the 52 GB rule also read through the macOS footprint (counts compressed pages; ps RSS does not)
_P = dict(MODE="lean", L="100", NSEED="1024", RMIN="0.78125", THREADS="14", SPILL="1", INPUTS="native_cmb", M3="1", CONVERT="1", MUTATE="none", N=1024, OWNB="fret")
JOBS = {"SC1x": dict(_P, foot="canonical"), "SC2x": dict(_P, foot="alt"),                      # A5 primary: own baryons = census f_ret
        "SC1m": dict(_P, foot="canonical", OWNB="cond"), "SC2m": dict(_P, foot="alt", OWNB="cond")}   # A5 secondary (M2 condensed): registered, NOT queued

def swap_used_mb():
    out = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"used = ([\d.]+)M", out); return float(m.group(1)) if m else 0.0
_LP = ctypes.CDLL("/usr/lib/libproc.dylib")
class _RU(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in ("ut", "st", "piw", "iw", "pageins", "wired", "resident", "footprint")] + [("pad", ctypes.c_uint64 * 40)]
def footprint_gb(pid):
    ru = _RU(); return ru.footprint / 1e9 if _LP.proc_pid_rusage(int(pid), 2, ctypes.byref(ru)) == 0 else -1.0
def disk_free_gb():
    return shutil.disk_usage(WORK).free / 1e9
def rss_gb(pid):
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return float(out) / 1e6 if out else 0.0

def start(job):
    s = JOBS[job]; d = os.path.join(WORK, job); os.makedirs(d, exist_ok=True)
    env = dict(os.environ, CFG596_MODE=s["MODE"], CFG596_L=s["L"], CFG596_NSEED=s["NSEED"], CFG596_RMIN=s["RMIN"], CFG596_THREADS=s["THREADS"],
               CFG596_WORK=d, CFG596_SPILL=s["SPILL"], CFG596_CKPT="1", CFG654_INPUTS=s["INPUTS"], CFG960_M3=s["M3"], CFG960_CONVERT=s["CONVERT"],
               CFG960_MUTATE=s["MUTATE"], CFG960_OWNB=s["OWNB"], CFG960_RSSMAX=str(RSS_MAX_GB), MallocSpaceEfficient="1")   # A1 allocator mode (RSS = live memory)
    json.dump(dict(job=job, spec=s, start=time.strftime("%Y-%m-%d %H:%M")), open(os.path.join(d, "job.json"), "w"), indent=1)
    log = open(os.path.join(d, "engine.log"), "a")
    p = subprocess.Popen(["nice", "-n", "10", sys.executable, ENGINE, "SCT", s["foot"], str(s["N"])], stdout=log, stderr=subprocess.STDOUT, env=env)
    return dict(job=job, p=p, d=d, swap0=swap_used_mb(), peak=0.0, wl=open(os.path.join(d, "watch.log"), "a"))

def watch(r):
    while r["p"].poll() is None:
        g = rss_gb(r["p"].pid); sw = swap_used_mb(); r["peak"] = max(r["peak"], g); fp = footprint_gb(r["p"].pid); df = disk_free_gb()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"rss {g:.2f} GB peak {r['peak']:.2f} swap_used {sw:.0f} MB (start {r['swap0']:.0f}) footprint {fp:.2f} GB disk_free {df:.1f} GB", file=r["wl"], flush=True)
        if g > RSS_MAX_GB or sw - r["swap0"] > SWAP_GROW_MB:
            print("ABORT (frozen rule): rss", g, "swap growth", sw - r["swap0"], file=r["wl"], flush=True); r["p"].kill()
        elif fp > FOOTPRINT_MAX_GB:
            print("ABORT (A6 footprint rule): footprint", fp, "GB", file=r["wl"], flush=True); r["p"].kill()
        elif df < 3.0:
            print("ABORT (disk guard): free disk", df, "GB", file=r["wl"], flush=True); r["p"].kill()
        time.sleep(20)
    print("exit", r["p"].returncode, "peak_rss_gb", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=r["wl"], flush=True)
    td = os.path.join(r["d"], "tmp")
    if os.path.isdir(td):
        for f in os.listdir(td):
            if f.startswith(("df_", "lab_")): os.remove(os.path.join(td, f))

if __name__ == "__main__":
    mode, jobs = sys.argv[1], sys.argv[2:]
    assert mode == "serial" and jobs and all(j in JOBS for j in jobs), "usage: run_960.py serial SC1x [SC2x]   (secondary: SC1m SC2m)"
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "run_960_launcher.log"), "a") as lg:
        print("start", mode, jobs, time.strftime("%Y-%m-%d %H:%M"), os.getpid(), file=lg, flush=True)
        rc = 0
        for j in jobs:
            if disk_free_gb() < DISK_START_GB:
                print(j, "not started: free disk", round(disk_free_gb(), 1), f"GB < {DISK_START_GB} GB", file=lg, flush=True); rc = 4; break
            r = start(j); watch(r)
            print(j, "rc", r["p"].returncode, "peak", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
            if r["p"].returncode != 0:
                print("stopping the serial queue after a failure", file=lg, flush=True); rc = 1; break
    sys.exit(rc)
