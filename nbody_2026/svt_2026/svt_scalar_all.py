#!/usr/bin/env python3
"""Runner: full v7 scalar-sector SVT derivation. Exit 0 iff every stage passes with no [FAIL]."""
import subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
stages = ["svt_scalar_master.py", "svt_scalar_reduce.py", "svt_scalar_physical.py"]
rc_all = 0
for s in stages:
    print("="*30, "RUNNING", s, "="*30, flush=True)
    r = subprocess.run([sys.executable, "-u", s], capture_output=True, text=True, timeout=900)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0 or "[FAIL]" in r.stdout:
        rc_all = 1
        print("*** STAGE FAILED:", s)
print("\nALL STAGES:", "PASS" if rc_all == 0 else "FAIL")
sys.exit(rc_all)
