#!/usr/bin/env python3
"""DR4-READY-1: the list of the DR3 pairs the DELTA Q1 needs neighbour cones for (NEW file; OFFLINE, the driver's socket guard stays; nothing is fetched).

The builder applies cut 13 to EVERY pair that passes the other cuts before the vtilde-error Monte Carlo (the driver's --dump-candidates writes exactly those pairs: DR3 10,231).  The full-size Q1 holds the cones of the
6,210 FINAL pairs only.  The pairs that reach cut 13 but are not final (4,021) have no cone.  This script writes them, taken from the driver's OWN dump of the pairs that reach cut 13 (so the list is tied to the exact array the cones
path will evaluate), as q1_delta_pairs.csv (source_id1, source_id2; sorted; the row index is the pair_id of the delta cones) in the gitignored data directory, and records counts and the file's sha256 in q1_delta_pairs_dr3.json.
DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_delta_pairs_dr3.py"""
import sys
sys.dont_write_bytecode = True
import csv, hashlib, json, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dry_run_driver as D
import cones_cut13 as CC
import q1_pilot_ranges as Q1

D.init(False)
T0 = time.time()
ext = D.extract_dir("dr3", "primary")
tmp = Path(tempfile.mkdtemp()) / "candidates.csv"
b_ref, r_ref = D.run("dr3", "primary", "extract-builder", None, False, dump_candidates=str(tmp))
assert r_ref["sha256"].startswith("6fff64d964ebaa72"), "the driver's reference CSV changed: refusing to plan on it"
c1, c2 = CC.read_pairs_csv(tmp)
cand = set(zip(c1.tolist(), c2.tolist()))
f1, f2 = CC.read_pairs_csv(ext / "wide_binaries_dr3.csv")
final = set(zip(f1.tolist(), f2.tolist()))
assert len(cand) == len(c1) == 10231, "the candidate dump is not the 10,231 pairs of the rehearsal"
assert len(final) == len(f1) == 6210 and final <= cand, "every final pair must be among the candidates"
delta = sorted(cand - final)
out = Q1.IN_DIR / "q1_delta_pairs.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["source_id1", "source_id2"])
    w.writerows(delta)
sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
summ = dict(candidates=len(cand), final=len(final), delta=len(delta), final_not_in_candidates=len(final - cand), candidates_dump_from="dry_run_driver --dump-candidates, cut13 kind extract-builder, reference CSV sha256 prefix 6fff64d964ebaa72",
            file="real_research/data/widebinaries/dr3_extract/dr4_ready_1/q1_delta_pairs.csv (gitignored)", sha256=sha, bytes=out.stat().st_size, seconds=round(time.time() - T0, 1))
(HERE / "q1_delta_pairs_dr3.json").write_text(json.dumps(summ, indent=1) + "\n")
print(f"candidates (pairs that reach cut 13, from the driver's own dump) {len(cand):,d}; final {len(final):,d}; delta {len(delta):,d}; wrote {out.name} (sha256 {sha[:16]}), q1_delta_pairs_dr3.json  [{time.time() - T0:.0f} s]")
