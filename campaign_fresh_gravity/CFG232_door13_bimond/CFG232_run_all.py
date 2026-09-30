#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG232_run_all -- re-run every CFG232 script (main runs, then the nine MUTATE controls) and print the exit codes.
Main runs: exit 0 = all reproduction controls passed (a control failure exits 1 and is kept, e.g. A3 none, A6 C6 as frozen).  MUTATE runs: exit 1 = the control bites.
Set ZF_REPO to the repository root if this directory is not inside it.  Total runtime about 6 minutes (A1's five runs dominate).
Usage:  python3 CFG232_run_all.py [--fast]      (--fast skips the two slow scripts' MUTATE re-runs)
"""
import os, sys, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
MAINS = ["A1_static_reduction", "A2_spectrum_flat_and_mond_background", "A3_cold_coupling", "A4_cosmology", "A5_lambda_tie",
         "A6_solar_system", "A7_scalar_tensor_13c", "A8_energy"]
MUTATES = [("A1_static_reduction", m) for m in ("M1", "M2", "M3", "M4")] + [("A2_spectrum_flat_and_mond_background", m) for m in ("M1", "M3", "M8")] + \
          [("A3_cold_coupling", "M5"), ("A4_cosmology", "M6"), ("A4_cosmology", "M7"), ("A5_lambda_tie", "M6"), ("A5_lambda_tie", "M7"), ("A7_scalar_tensor_13c", "M9")]
fast = "--fast" in sys.argv


def run(script, mut=None):
    env = dict(os.environ)
    env.pop("MUTATE", None)
    if mut:
        env["MUTATE"] = mut
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(HERE, f"CFG232_{script}.py")], env=env, capture_output=True, text=True)
    return p.returncode, time.time() - t0


print("main runs (exit 0 expected unless a reproduction control failed and is kept):")
for s in MAINS:
    rc, dt = run(s)
    print(f"  {s:42s} exit {rc}  {dt:6.1f}s")
print("MUTATE runs (exit 1 = the control bites; exit 0 = declared non-biting control):")
for s, m in MUTATES:
    if fast and s.startswith(("A2", "A4")):
        continue
    rc, dt = run(s, m)
    print(f"  {s:42s} MUTATE={m:3s} exit {rc}  {dt:6.1f}s")
rc = subprocess.run([sys.executable, os.path.join(HERE, "CFG232_verdict.py")]).returncode
sys.exit(0)
