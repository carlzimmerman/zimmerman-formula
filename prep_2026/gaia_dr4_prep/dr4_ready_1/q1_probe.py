#!/usr/bin/env python3
"""DR4-READY-1: a TIMING PROBE for the approved Q1 pilot (a subset of the same 500 pairs; same ADQL).  NEW file; the only networked script besides
q_fetch_dr3.py.  Why: the single 1,000-cone job timed out after ~1h45m and batch 0 (200 cones) had run 30 minutes without a result; this runs the same
query form on the first N pairs of the pilot (default 3 pairs = 6 cones) to see whether the archive's cone join is slow per cone (index problem with the
variable radius) or the queue is slow.  Output is gitignored; the timing goes to manifest_q1_probe.json (committed).  Scope: at most 10 pairs.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_probe.py --n 3 --owner-go-recorded
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, time, hashlib
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import cut13_allsource as W1

WB = REPO / "real_research" / "data" / "widebinaries"
OUT = WB / "dr3_extract" / "dr4_ready_1"
ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=3)
ap.add_argument("--owner-go-recorded", action="store_true")
a = ap.parse_args()
if not a.owner_go_recorded or a.n > 10:
    raise SystemExit("refused: needs --owner-go-recorded (the Q1 pilot go) and n <= 10")
from astropy.table import Table
from astroquery.gaia import Gaia
S = np.load(WB / "dr3_extract" / "stage_A.npz")
order = np.argsort(S["source_id"])
Z = np.load(OUT / "q1_pilot_pairs.npz")
pick, sa, sb = Z["pick"][: a.n], Z["source_id_a"][: a.n], Z["source_id_b"][: a.n]
row = lambda s: order[np.searchsorted(S["source_id"][order], s)]
ia, ib = row(sa), row(sb)
upt = W1.upload_table(pick, S["ra"][ia], S["dec"][ia], S["ra"][ib], S["dec"][ib], S["parallax"][ia])
up = OUT / "q1_probe_upload.xml"
Table(upt).write(up, format="votable", overwrite=True)
q = W1.adql_cones("gaiadr3.gaia_source", upload="pairs")
p = OUT / "q1_probe_neighbours.fits"
t0 = time.time()
job = Gaia.launch_job_async(q, upload_resource=str(up), upload_table_name="pairs", dump_to_file=True, output_file=str(p), output_format="fits")
jid = getattr(job, "jobid", None)
res = job.get_results()
dt = time.time() - t0
rec = dict(n_pairs=int(a.n), n_cones=int(len(upt["pair_id"])), radius_arcsec=[float(upt["radius_deg"].min() * 3600), float(upt["radius_deg"].max() * 3600)],
           rows=int(len(res)), seconds=round(dt, 1), sha256=hashlib.sha256(open(p, "rb").read()).hexdigest(), query=q, jobid=str(jid),
           note="timing probe for the approved Q1 pilot (owner's go, 2026-09-29): the same pairs and ADQL as the pilot's first pairs")
(HERE / "manifest_q1_probe.json").write_text(json.dumps(rec, indent=1) + "\n")
print(json.dumps({k: v for k, v in rec.items() if k != "query"}))
