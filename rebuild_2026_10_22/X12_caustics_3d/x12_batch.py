#!/usr/bin/env python3
"""X12 batch driver: runs a set of x12_run.py jobs, at most --par (<= 2) at once, `nice -n 15`, one thread, resuming any
run that checkpointed at its wall guard (exit 3). Waits while the machine's free memory (heavy-queue status, read only) is
below 6 GB. Sets (FROZEN §4 order of work):
  validate  V-a1 (static, both footings, h 20/15/10) + V-cm (MW, M31, canonical, h 20/15/10)
  wake      case W, both footings, h 20/15/10
  b0        case E b = 0, both footings, h 20/15/10
  bpos      case E b = 50, 150, both footings, h 20/15/10
  numtests  N-dt / N-box / N-tol at h 15 on (canonical, W) and (canonical, E b = 150)
  mutate    X12_MUTATE=1: V-cm (MW, M31, canonical, h 15/10), W (both footings, h 20/10), E b = 0 (canonical, h 20)
  a1        AMENDMENT A1 (POST-RESULT diagnostics): A1-loc (M31, frozen box, h 15/10), A1-box (MW, M31, h 15/10)
  mutate_vcm  the MUTATE V-cm runs only (the lane stopped at V-cm, FROZEN §4)
"""
import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
HS = (20, 15, 10)
FEET = ("canonical", "alt")


def jobs(name):
    J = []
    if name == "validate":
        J += [(["--kind", "static", "--foot", f, "--h", str(h)], {}) for f in FEET for h in HS]
        J += [(["--kind", "vcm", "--mass", m, "--foot", "canonical", "--h", str(h)], {}) for m in ("MW", "M31") for h in HS]
    elif name == "wake":
        J += [(["--kind", "wake", "--foot", f, "--h", str(h)], {}) for h in HS for f in FEET]
    elif name == "b0":
        J += [(["--kind", "enc", "--b", "0", "--foot", f, "--h", str(h)], {}) for h in HS for f in FEET]
    elif name == "bpos":
        J += [(["--kind", "enc", "--b", str(b), "--foot", f, "--h", str(h)], {}) for h in HS for b in (50, 150)
              for f in FEET]
    elif name == "numtests":
        for v in ("--dt-half", "--box-half", "--tol-tight"):
            J.append((["--kind", "wake", "--foot", "canonical", "--h", "15", v], {}))
            J.append((["--kind", "enc", "--b", "150", "--foot", "canonical", "--h", "15", v], {}))
    elif name == "mutate":
        mu = {"X12_MUTATE": "1"}
        J += [(["--kind", "vcm", "--mass", m, "--foot", "canonical", "--h", str(h)], mu) for m in ("MW", "M31")
              for h in (15, 10)]
        J += [(["--kind", "wake", "--foot", f, "--h", str(h)], mu) for f in FEET for h in (20, 10)]
        J += [(["--kind", "enc", "--b", "0", "--foot", "canonical", "--h", "20"], mu)]
    elif name == "a1":
        J += [(["--kind", "vcm", "--mass", "M31", "--foot", "canonical", "--h", str(h), "--a1", "loc"], {}) for h in (15, 10)]
        J += [(["--kind", "vcm", "--mass", m, "--foot", "canonical", "--h", str(h), "--a1", "box"], {})
              for m in ("MW", "M31") for h in (15, 10)]
    elif name == "a2":
        J += [(["--kind", "vcm", "--mass", "M31", "--foot", "canonical", "--h", "10", "--a2", v], {}) for v in ("mir", "dt")]
    elif name == "mutate_vcm":
        J += [(["--kind", "vcm", "--mass", m, "--foot", "canonical", "--h", str(h)], {"X12_MUTATE": "1"})
              for m in ("MW", "M31") for h in (15, 10)]
    return J


def tag_of(a, env):
    d = dict(zip(a[::2], a[1::2]))
    k = d["--kind"]
    h = d["--h"]
    if k == "static":
        t = f"static_M31_{d['--foot']}_h{h}"
    elif k == "vcm":
        t = f"vcm_{d['--mass']}_{d['--foot']}_h{h}"
    elif k == "wake":
        t = f"wake_{d['--foot']}_h{h}"
    else:
        t = f"enc_b{d['--b']}_{d['--foot']}_h{h}"
    for v, s in (("--dt-half", "_dthalf"), ("--box-half", "_boxhalf"), ("--tol-tight", "_toltight")):
        if v in a:
            t += s
    if "--a1" in d:
        t += f"_A1{d['--a1']}"
    if "--a2" in d:
        t += f"_A2{d['--a2']}"
    return t + ("_MUTATE" if env.get("X12_MUTATE") == "1" else "")


def free_gb():
    try:
        out = subprocess.run([sys.executable, str(ROOT / "compute_queue" / "heavyq.py"), "status"], capture_output=True,
                             text=True, timeout=60).stdout
        m = re.search(r"free\+inactive ([\d.]+) GB", out)
        return float(m.group(1)) if m else 99.0
    except Exception:
        return 99.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True)
    ap.add_argument("--par", type=int, default=2)
    ap.add_argument("--only", default=None, help="regex on tags")
    a = ap.parse_args()
    par = min(a.par, 2)
    todo = []
    for args, env in jobs(a.set):
        t = tag_of(args, env)
        if a.only and not re.search(a.only, t):
            continue
        if (HERE / "runs" / f"{t}.json").exists():
            print(f"skip {t} (done)", flush=True)
            continue
        todo.append((t, args, env))
    running = {}
    while todo or running:
        for t, (p, args, env) in list(running.items()):
            rc = p.poll()
            if rc is None:
                continue
            del running[t]
            if rc == 3:
                print(f"{time.strftime('%H:%M:%S')} {t}: checkpointed, resuming", flush=True)
                todo.insert(0, (t, args + ["--resume"] if "--resume" not in args else args, env))
            else:
                print(f"{time.strftime('%H:%M:%S')} {t}: exit {rc}", flush=True)
        while todo and len(running) < par:
            if free_gb() < 6.0:
                print(f"{time.strftime('%H:%M:%S')} low free memory; waiting", flush=True)
                time.sleep(120)
                break
            t, args, env = todo.pop(0)
            e = dict(os.environ, OMP_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                     MKL_NUM_THREADS="1", MallocMediumZone="0", **env)
            lf = open(HERE / "work" / f"{t}.stdout", "a")
            p = subprocess.Popen(["nice", "-n", "15", sys.executable, str(HERE / "x12_run.py")] + args, env=e,
                                 stdout=lf, stderr=subprocess.STDOUT, cwd=str(HERE))
            running[t] = (p, args, env)
            print(f"{time.strftime('%H:%M:%S')} start {t} {' '.join(args)}", flush=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
