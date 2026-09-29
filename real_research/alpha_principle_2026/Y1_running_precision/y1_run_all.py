#!/usr/bin/env python3
"""y1_run_all.py -- re-runs every Y1 script, real run (expected exit 0) and MUTATE control (expected exit 1), and checks the exit codes.
Run:  Y1_SCRATCH=<dir with the downloaded sources> python3 y1_run_all.py        (exit 0 iff all 14 runs behave; the y1_0 script downloads into Y1_SCRATCH if a source is missing)
Note: y1_1 ... y1_6 need only the repository; y1_0 needs the scratch directory (default ./y1_scratch, network access if the files are absent).
Total run time: about 20 minutes (y1_6 dominates).
"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["y1_0_fetch_sources.py", "y1_1_transcription.py", "y1_2_validate_published.py", "y1_3_campaign_compare.py", "y1_4_budget.py", "y1_5_impact.py", "y1_6_x1_hybrid.py"]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
bad = []
for s in SCRIPTS:
    for mode, want in (("", 0), ("MUTATE", 1)):
        cmd = [sys.executable, os.path.join(HERE, s)] + ([mode] if mode else [])
        r = subprocess.run(cmd, cwd=HERE, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ok = r.returncode == want
        print(f"  [{'PASS' if ok else 'FAIL'}] {s} {mode or 'REAL'}: exit {r.returncode} (expected {want})")
        if not ok:
            bad.append((s, mode, r.returncode))
print("all Y1 scripts behave as required" if not bad else f"PROBLEMS: {bad}")
sys.exit(0 if not bad else 1)
