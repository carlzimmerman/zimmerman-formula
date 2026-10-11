#!/usr/bin/env python3
"""CFG624 launcher (FROZEN_CRITERIA.md 803cef306): serial PM jobs, 4 threads, nice 10, L = 100 Mpc/h, seed 359, NSEED 512.
Jobs: <SWITCH>_<foot>_N<N>, SWITCH in T1 (NCE-S), S1 (NCE-E), S0 (a0 -> 0 MUTATE).  Memory gate for N = 512: no CFG596 job running and
free + inactive memory >= 25 GB at launch; a 512^3 job is stopped if swap grows by more than 2 GB.  Usage: nohup python3 run_624.py JOB ..."""
import os, sys, subprocess, time, re
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg624_work"))
os.makedirs(WORK, exist_ok=True)


def mem_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    pg = int(re.search(r"page size of (\d+)", out).group(1))
    v = {k: int(re.search(rf"{k}:\s+(\d+)", out).group(1)) for k in ("Pages free", "Pages inactive", "Pages speculative")}
    return (v["Pages free"] + v["Pages inactive"] + v["Pages speculative"]) * pg / 1e9


def swap_mb():
    out = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    return float(re.search(r"used = ([\d.]+)M", out).group(1))


def cfg596_running():
    out = subprocess.run(["ps", "-Ao", "command"], capture_output=True, text=True).stdout
    return any(("cfg596_pm.py" in l or "run_596.py" in l) for l in out.splitlines())


def run(job, lg):
    sw, foot, n = job.split("_"); n = int(n[1:])
    if n >= 512 and (cfg596_running() or mem_gb() < 25.0):
        print(job, "SKIPPED by the memory gate", round(mem_gb(), 1), "GB", "cfg596 running" if cfg596_running() else "", file=lg, flush=True)
        return None
    env = dict(os.environ, CFG527_THREADS="4", CFG527_NSEED="512", CFG527_L="100", CFG527_SEED="359")
    log = open(os.path.join(WORK, f"cfg624_{job}.log"), "w")
    p = subprocess.Popen(["nice", "-n", "10", sys.executable, os.path.join(HERE, "cfg624_pm.py"), sw, "FLAT", foot, str(n), "1", "NOFILT"],
                         stdout=log, stderr=subprocess.STDOUT, env=env, cwd=WORK)
    s0 = swap_mb()
    while p.poll() is None:
        time.sleep(20)
        if n >= 512 and swap_mb() - s0 > 2048:
            p.kill(); print(job, "KILLED by the swap rule", swap_mb() - s0, file=lg, flush=True)
    return p.returncode


with open(os.path.join(WORK, "run_624_launcher.log"), "a") as lg:
    print("start", time.strftime("%Y-%m-%d %H:%M"), os.getpid(), sys.argv[1:], round(mem_gb(), 1), "GB free+inactive", file=lg, flush=True)
    for job in sys.argv[1:]:
        print(job, "rc", run(job, lg), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
