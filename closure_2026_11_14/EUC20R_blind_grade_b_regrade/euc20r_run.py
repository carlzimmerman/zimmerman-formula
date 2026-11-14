#!/usr/bin/env python3
"""EUC20R runner: every route and mode in its own low-priority process, then the H1 check after each run.

  python3 -I -B euc20r_run.py --modes f1            (the harness first)
  python3 -I -B euc20r_run.py --modes primary,F1a,F1b,invert
  then: python3 -I -B euc20r_collect.py ; EUC20R_MUTATE=invert python3 -I -B euc20r_collect.py (exit 1)
LNJ1 is not run under invert (no twin of its own); EUC5 A1 is not run under the brackets (it carries no word).
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import argparse, builtins, json, os, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc20r_common as C

SRC = [C.rel(C.DIRS[k]) for k in ("EUC1", "EUC4", "EUC5", "EUC6", "EUC8", "EUC10", "EUC17", "EUC19", "LNJ1", "JNT2", "PD1")]
PLAN = {"euc8": C.MODES, "euc5a1": ("f1", "primary", "invert"), "lnj1": ("f1", "primary", "F1a", "F1b")}


def env():
    e = {k: v for k, v in os.environ.items() if not k.endswith("_MUTATE")}
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
        e[v] = "1"
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    return e


def h1(run, log):
    r = subprocess.run(["git", "status", "--porcelain", "--"] + SRC, cwd=C.REPO, capture_output=True, text=True)
    log.append(dict(run=run, porcelain=r.stdout, time=time.strftime("%H:%M:%S")))
    print("  H1 after %-22s %s" % (run, "clean" if not r.stdout.strip() else "DIRTY:\n" + r.stdout), flush=True)


def go(cmd, out, err, run, log):
    t0 = time.time()
    with builtins.open(out, "w") as fo, builtins.open(err, "w") as fe:
        p = subprocess.run(["nice", "-n", "19", sys.executable, "-I", "-B"] + cmd, cwd=C.REPO, stdout=fo, stderr=fe, env=env())
    print("%-24s exit %d (%.0f s)" % (run, p.returncode, time.time() - t0), flush=True)
    h1(run, log)
    return p.returncode


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--modes", required=True); a = ap.parse_args()
    modes = [m for m in a.modes.split(",") if m]
    lp = os.path.join(HERE, "runs", "h1_log.json"); os.makedirs(os.path.dirname(lp), exist_ok=True)
    log = json.load(builtins.open(lp)) if os.path.exists(lp) else []
    log = [r for r in log if r["run"].split("/")[0] not in modes and not (r["run"] == "shift" and "f1" in modes)]
    h1("before", log)
    if "f1" in modes:                                            # the exact-shift script writes every mode at once
        go([os.path.join(HERE, "euc20r_shift.py")], os.path.join(HERE, "runs", "shift_stdout.txt"), os.path.join(HERE, "runs", "shift_stderr.txt"), "shift", log)
    for mode in modes:
        for lane, ms in PLAN.items():
            if mode not in ms: continue
            d = os.path.join(HERE, "runs", mode, lane); os.makedirs(d, exist_ok=True)
            go([os.path.join(HERE, "euc20r_route.py"), "--lane", lane, "--mode", mode], os.path.join(d, "stdout.txt"), os.path.join(d, "stderr.txt"), "%s/%s" % (mode, lane), log)
    with builtins.open(lp, "w") as f:
        json.dump(log, f, indent=1)


if __name__ == "__main__":
    main()
