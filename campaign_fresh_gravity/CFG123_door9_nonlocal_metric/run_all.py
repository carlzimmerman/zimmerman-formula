#!/usr/bin/env python3
"""re-run everything in place:  ZF_REPO=/path/to/zimmerman-formula python3 run_all.py   (about 12 minutes).  Prints each script's exit code.
Main runs exit 0 iff every pre-registered claim holds (a falsified prediction exits 1 and is kept); MUTATE runs must exit 1; exit 3 = mode not applicable."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
main = ["A1_localised_action.py", "A2_static_linear_response.py", "A3_nonlinear_static.py", "A4_cosmo_background_growth.py", "A5_reciprocity_energy.py", "A6_constants_tie.py", "A7_wellposed.py"]
mut = [("A1_localised_action.py", "b"), ("A2_static_linear_response.py", "a"), ("A2_static_linear_response.py", "b"), ("A2_static_linear_response.py", "d"),
       ("A3_nonlinear_static.py", "c"), ("A6_constants_tie.py", "a"), ("A7_wellposed.py", "e")]
posthoc = ["POSTHOC_1_notes.py"]
rc = {}
for s in main:
    r = subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, env=dict(os.environ))
    open(os.path.join(HERE, s[:-3] + ".stdout"), "w").write(r.stdout + r.stderr); rc[s] = r.returncode
    print(f"{s:36s} main   exit {r.returncode}", flush=True)
for s, m in mut:
    env = dict(os.environ, MUTATE=m)
    r = subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, env=env)
    print(f"{s:36s} MUTATE={m} exit {r.returncode}", flush=True)
for s in posthoc:
    if os.path.exists(os.path.join(HERE, s)):
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, env=dict(os.environ))
        print(f"{s:36s} posthoc exit {r.returncode}", flush=True)
