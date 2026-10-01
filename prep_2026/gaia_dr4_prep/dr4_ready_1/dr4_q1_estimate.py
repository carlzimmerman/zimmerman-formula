#!/usr/bin/env python3
"""DR4-READY-1, item 1 of DR4_Q1_TOOLING_DESIGN_FROZEN.md (6742d206d): the run-time ESTIMATOR for the owner's pre-brief (NEW file; OFFLINE; no archive contact).
Prints the expected queries, serial hours and MB of the Q1 cone fetch from the real candidate count (the pairs that reach cut 13: the driver's --dump-candidates), low / central / high, with suggested hard caps.  The rates are the two committed DR3 runs pooled
(manifest_q1_full.json, manifest_q1_delta.json); the density factor for the larger DR4 catalogue and the pace are ASSUMPTIONS, printed as such.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/dr4_q1_estimate.py --n-pairs 49000   |   --pairs-csv <candidates.csv>   [--json OUT]"""
import sys
sys.dont_write_bytecode = True
import argparse, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dr4_archive_fetch as F

ap = argparse.ArgumentParser()
ap.add_argument("--n-pairs", type=int)
ap.add_argument("--pairs-csv")
ap.add_argument("--json", default=None)
a = ap.parse_args()
if (a.n_pairs is None) == (a.pairs_csv is None):
    raise SystemExit("give exactly one of --n-pairs and --pairs-csv")
n = a.n_pairs if a.n_pairs is not None else len(F.read_pairs(a.pairs_csv)[0])
txt, d = F.pre_brief(n)
print(txt)
if a.json:
    Path(a.json).write_text(json.dumps(d, indent=1) + "\n")
