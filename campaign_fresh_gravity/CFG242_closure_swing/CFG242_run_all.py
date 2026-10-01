#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG242_run_all -- re-run every CFG242 script (main runs, then every MUTATE control), print observed vs the frozen expected exit code, then the two verdict scripts.
Usage:  ZF_REPO=<repo root> python3 CFG242_run_all.py [A|B]      (inside the repository the root is found by walking up; no argument = both routes; about 2 minutes)
Main runs exit 0 (every reproduction control passed).  MUTATE runs exit 1 iff the control BITES; the declared non-biting controls (MA7, MB3, MB4, MB5) exit 0.
No output prints an absolute home path (<repo> / <lane> are substituted)."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
A_MAIN = ["A_controls", "A_g0_legality", "A_g4_ledger", "A_g3_exchange", "A_g5_solar_stability", "A_g1_target"]
A_MUT = [("A_g0_legality", "MA1", 1), ("A_g0_legality", "MA2", 1), ("A_g0_legality", "MA3", 1), ("A_g0_legality", "MA6", 1),
         ("A_g4_ledger", "MA4", 1), ("A_g3_exchange", "MA3", 1), ("A_g3_exchange", "MA5", 1), ("A_g1_target", "MA7", 0)]
B_MAIN = ["B_controls", "B_g5a_ghost", "B_g4_ledger", "B_not_reached"]
B_MUT = [("B_g5a_ghost", "MB1", 1), ("B_g5a_ghost", "MB2", 1), ("B_g5a_ghost", "MB3", 0), ("B_not_reached", "MB4", 0), ("B_not_reached", "MB5", 0)]
which = sys.argv[1] if len(sys.argv) > 1 else "AB"


def run(script, mut=None):
    env = dict(os.environ); env.pop("MUTATE", None)
    if mut:
        env["MUTATE"] = mut
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(HERE, f"CFG242_{script}.py")], env=env, capture_output=True, text=True)
    return p.returncode, time.time() - t0


bad = 0
for route, mains, muts in (("A", A_MAIN, A_MUT), ("B", B_MAIN, B_MUT)):
    if route not in which:
        continue
    print(f"route {route}: main runs (exit 0 expected)")
    for s in mains:
        rc, dt = run(s); bad += (rc != 0)
        print(f"  {s:26s} exit {rc}  {dt:6.1f}s  {'ok' if rc == 0 else 'UNEXPECTED'}")
    print(f"route {route}: MUTATE runs (exit 1 = bites; expected shown)")
    for s, m, exp in muts:
        rc, dt = run(s, m); bad += (rc != exp)
        print(f"  {s:26s} MUTATE={m:4s} exit {rc} (expected {exp})  {dt:6.1f}s  {'ok' if rc == exp else 'UNEXPECTED'}")
    rc = subprocess.run([sys.executable, os.path.join(HERE, f"CFG242_{route}_verdict.py")], env={k: v for k, v in os.environ.items() if k != "MUTATE"}).returncode
print(f"unexpected outcomes: {bad}")
sys.exit(0)
