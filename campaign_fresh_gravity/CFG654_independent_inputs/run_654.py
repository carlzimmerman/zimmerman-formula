#!/usr/bin/env python3
"""CFG654 launcher = run_650.py (same guards) pointed at cfg654_pm.py and _external_data/cfg654_work/<JOB>/, plus the CFG654_INPUTS switch.
Validation (256^3 lean L100 NSEED512 RMIN 0.78125, 3 threads, ONE process, RSS kill 3 GB, nice 10):
  V0i  inherited inputs, modules OFF, RES canonical  -> must equal CFG596 VLr bit for bit
  VNs  native inputs, S0 canonical                   -> native control (zi amplitude check vs cfg654_ics prediction)
  VN12 native inputs, M1+M2 (the T12 set), RES canonical -> PREVIEW only (vs VNs)
Production (1024^3; DEFINED, NOT STARTED by this lane; frozen criteria FROZEN_CRITERIA.md):
  N12  native inputs, M1+M2, RES canonical          NS0  native inputs, S0 canonical (shares the native ICs)
Addendum A1 (2026-10-13): PRIMARY native = CMB omega_b/omega_c pair: VNcs / VNc12 (256^3), NC12 / NCS0 (1024^3, NOT started);
  the BBN-omega_b jobs (VNs, VN12, N12, NS0) are the declared bracket.
  python3 run_654.py serial JOB [JOB ...]"""
import os, sys, subprocess, time, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "cfg654_pm.py")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg654_work"))
RSS_MAX_GB = 52.0; SWAP_GROW_MB = 4096.0
_V = dict(sw="RES", foot="canonical", N=256, MODE="lean", L="100", NSEED="512", RMIN="0.78125", THREADS="3", RSSMAX=3.0, SWAPGROW=1024.0, IC="sigma8", INPUTS="inherited")
_P = dict(sw="RES", N=1024, MODE="lean", L="100", NSEED="1024", RMIN="0.78125", THREADS="14", SPILL="1", IC="sigma8", INPUTS="native")
def _j(base, mods, **kw):
    d = dict(base, MODS=mods); d.update(kw); return d
JOBS = {
    "V0i": _j(_V, ""), "VNs": _j(_V, "", sw="S0", INPUTS="native"), "VN12": _j(_V, "12", INPUTS="native"),
    "N12": _j(_P, "12", foot="canonical"), "NS0": _j(_P, "", sw="S0", foot="canonical"),
    # addendum A1 (2026-10-13): primary native set = CMB omega_b/omega_c pair (CFG654_INPUTS=native_cmb); N12/NS0/VNs/VN12 = BBN bracket
    "VNcs": _j(_V, "", sw="S0", INPUTS="native_cmb"), "VNc12": _j(_V, "12", INPUTS="native_cmb"),
    "NC12": _j(_P, "12", foot="canonical", INPUTS="native_cmb"), "NCS0": _j(_P, "", sw="S0", foot="canonical", INPUTS="native_cmb"),
}

def swap_used_mb():
    out = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"used = ([\d.]+)M", out); return float(m.group(1)) if m else 0.0
import ctypes, shutil
_LP = ctypes.CDLL("/usr/lib/libproc.dylib")
class _RU(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in ("ut", "st", "piw", "iw", "pageins", "wired", "resident", "footprint")] + [("pad", ctypes.c_uint64 * 40)]
def footprint_gb(pid):
    ru = _RU(); return ru.footprint / 1e9 if _LP.proc_pid_rusage(int(pid), 2, ctypes.byref(ru)) == 0 else -1.0
def disk_free_gb():
    return shutil.disk_usage(WORK).free / 1e9
def rss_gb(pid):
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return float(out) / 1e6 if out else 0.0                     # ps rss in KiB

def start(job):
    s = JOBS[job]; d = os.path.join(WORK, job); os.makedirs(d, exist_ok=True)
    env = dict(os.environ, CFG596_MODE=s["MODE"], CFG596_L=s["L"], CFG596_NSEED=s["NSEED"], CFG596_RMIN=s["RMIN"], CFG596_THREADS=s["THREADS"],
               CFG596_WORK=d, CFG596_SPILL=s.get("SPILL", "0"), CFG596_MAXSTEPS=s.get("MAXSTEPS", "100000"),
               CFG596_PROFILE=s.get("PROFILE", "0"), CFG650_IC=s["IC"], CFG654_INPUTS=s["INPUTS"],
               **{f"CFG650_M{i}": ("1" if str(i) in s["MODS"] else "0") for i in (1, 2, 3, 4)})
    json.dump(dict(job=job, spec=s, start=time.strftime("%Y-%m-%d %H:%M")), open(os.path.join(d, "job.json"), "w"), indent=1)
    log = open(os.path.join(d, "engine.log"), "w")
    p = subprocess.Popen(["nice", "-n", "10", sys.executable, ENGINE, s["sw"], s["foot"], str(s["N"])], stdout=log, stderr=subprocess.STDOUT, env=env)
    return dict(job=job, p=p, d=d, swap0=swap_used_mb(), peak=0.0, rmax=s.get("RSSMAX", RSS_MAX_GB), sgrow=s.get("SWAPGROW", SWAP_GROW_MB), wl=open(os.path.join(d, "watch.log"), "a"))

def watch(runs):
    while any(r["p"].poll() is None for r in runs):
        for r in runs:
            if r["p"].poll() is not None: continue
            g = rss_gb(r["p"].pid); sw = swap_used_mb(); r["peak"] = max(r["peak"], g); fp = footprint_gb(r["p"].pid); df = disk_free_gb()
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"rss {g:.2f} GB peak {r['peak']:.2f} swap_used {sw:.0f} MB (start {r['swap0']:.0f}) footprint {fp:.2f} GB disk_free {df:.1f} GB", file=r["wl"], flush=True)
            if g > r["rmax"] or sw - r["swap0"] > r["sgrow"]:
                print("ABORT (frozen rule): rss", g, "swap growth", sw - r["swap0"], file=r["wl"], flush=True); r["p"].kill()
            elif df < 3.0:
                print("ABORT (disk guard): free disk", df, "GB", file=r["wl"], flush=True); r["p"].kill()
        time.sleep(20)
    for r in runs:
        print("exit", r["p"].returncode, "peak_rss_gb", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=r["wl"], flush=True)
        td = os.path.join(r["d"], "tmp")                           # remove disk-backed temporaries left by a killed job
        if os.path.isdir(td):
            for f in os.listdir(td):
                if f.startswith("df_"): os.remove(os.path.join(td, f))

if __name__ == "__main__":
    mode, jobs = sys.argv[1], sys.argv[2:]
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "run_654_launcher.log"), "a") as lg:
        print("start", mode, jobs, time.strftime("%Y-%m-%d %H:%M"), os.getpid(), file=lg, flush=True)
        if mode == "par":
            rs = [start(j) for j in jobs]; watch(rs)
            for r in rs: print(r["job"], "rc", r["p"].returncode, "peak", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
        else:
            for j in jobs:
                if JOBS[j]["N"] >= 1024 and disk_free_gb() < 18.0:
                    print(j, "not started: free disk", round(disk_free_gb(), 1), "GB < 18 GB", file=lg, flush=True); break
                r = start(j); watch([r])
                print(j, "rc", r["p"].returncode, "peak", round(r["peak"], 2), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
                if r["p"].returncode != 0:
                    print("stopping the serial queue after a failure", file=lg, flush=True); break
