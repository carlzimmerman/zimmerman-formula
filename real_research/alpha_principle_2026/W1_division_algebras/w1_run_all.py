#!/usr/bin/env python3
"""w1_run_all -- re-runs every W1 script (real run must exit 0, MUTATE run must exit 1) and prints a table.
Run: python3 w1_run_all.py        -> exit 0 if all 10 runs behave as declared, 1 otherwise.  Writes nothing."""
import os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
scripts = ["w1_1_cl6_ladder.py", "w1_2_gen3_action.py", "w1_3_dixon_fh.py", "w1_4_jordan_f4_e6.py", "w1_5_couplings_and_scale.py"]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
bad = 0
for sc in scripts:
    for mode, want in (("", 0), ("MUTATE", 1)):
        cmd = [sys.executable, os.path.join(HERE, sc)] + ([mode] if mode else [])
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        last = [l for l in r.stdout.strip().splitlines() if l.startswith("SUMMARY")]
        ok = r.returncode == want
        bad += (not ok)
        print(f"{'OK ' if ok else 'BAD'} {sc:34s} {mode or 'real':7s} exit {r.returncode} (want {want})  {last[-1] if last else ''}")
sys.exit(1 if bad else 0)
