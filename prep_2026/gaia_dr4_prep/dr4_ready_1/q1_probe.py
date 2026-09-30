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
ap.add_argument("--constant-radius", action="store_true",
                help="use ONE literal radius (the maximum of the pairs' cones) in CIRCLE() instead of the per-row u.radius_deg: the archive's documented "
                     "upload cone-join form, expected to use the spatial index; the result is a superset of the exact cones (re-filtered locally)")
ap.add_argument("--tag", default="probe")
ap.add_argument("--healpix", action="store_true",
                help="index-friendly source_id RANGE join: upload the level-11 HEALPix source_id ranges covering the pairs' cones and select s.source_id in the ranges "
                     "(gaia source_id encodes the level-12 pixel); the result is a superset, re-filtered locally to the exact cones")
ap.add_argument("--sync", action="store_true", help="use the SYNCHRONOUS TAP endpoint (bypasses the async queue; the archive limits it to short jobs)")
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
up = OUT / f"q1_{a.tag}_upload.xml"
if a.healpix:
    import healpy as hp
    LEVEL = 11
    DIV = 2 ** 35 * 4 ** (12 - LEVEL)
    va = np.stack([np.cos(np.radians(S["dec"][ia])) * np.cos(np.radians(S["ra"][ia])), np.cos(np.radians(S["dec"][ia])) * np.sin(np.radians(S["ra"][ia])),
                   np.sin(np.radians(S["dec"][ia]))], 1)
    vb = np.stack([np.cos(np.radians(S["dec"][ib])) * np.cos(np.radians(S["ra"][ib])), np.cos(np.radians(S["dec"][ib])) * np.sin(np.radians(S["ra"][ib])),
                   np.sin(np.radians(S["dec"][ib]))], 1)
    pix = set()
    Rarc = W1.radius_arcsec(S["parallax"][ia])
    for k in range(len(pick)):
        for v in (va[k], vb[k]):
            pix.update(hp.query_disc(2 ** LEVEL, v, np.radians(Rarc[k] / 3600), inclusive=True, nest=True).tolist())
    pix = np.array(sorted(pix), np.int64)
    brk = np.flatnonzero(np.diff(pix) != 1)
    starts = np.concatenate([[0], brk + 1]); ends = np.concatenate([brk, [len(pix) - 1]])
    lo, hi = pix[starts] * DIV, (pix[ends] + 1) * DIV
    Table({"lo": lo, "hi": hi}).write(up, format="votable", overwrite=True)
    cols = ", ".join(f"s.{c}" for c in W1.COLS)
    q = (f"SELECT {cols}, s.phot_g_mean_mag AS phot_g_mean_mag FROM tap_upload.rng AS u JOIN gaiadr3.gaia_source AS s "
         f"ON s.source_id >= u.lo AND s.source_id < u.hi")
    upt = dict(pair_id=np.repeat(pick, 2), radius_deg=np.repeat(Rarc / 3600, 2))
    print(f"healpix level {LEVEL}: {len(pix)} pixels in {len(lo)} source_id ranges for {len(pick)} pairs", flush=True)
elif a.constant_radius:
    rmax = float(upt["radius_deg"].max())
    Table({k: v for k, v in upt.items() if k != "radius_deg"}).write(up, format="votable", overwrite=True)
    cols = ", ".join(f"s.{c}" for c in W1.COLS)
    q = (f"SELECT u.pair_id, u.comp, {cols}, s.phot_g_mean_mag AS phot_g_mean_mag FROM tap_upload.pairs AS u JOIN gaiadr3.gaia_source AS s "
         f"ON 1 = CONTAINS(POINT('ICRS', s.ra, s.dec), CIRCLE('ICRS', u.ra, u.dec, {rmax:.6f}))")
else:
    Table(upt).write(up, format="votable", overwrite=True)
    q = W1.adql_cones("gaiadr3.gaia_source", upload="pairs")
p = OUT / f"q1_{a.tag}_neighbours.fits"
t0 = time.time()
upname = "rng" if a.healpix else "pairs"
if a.sync:
    job = Gaia.launch_job(q, upload_resource=str(up), upload_table_name=upname, dump_to_file=True, output_file=str(p), output_format="fits")
else:
    job = Gaia.launch_job_async(q, upload_resource=str(up), upload_table_name=upname, dump_to_file=True, output_file=str(p), output_format="fits")
jid = getattr(job, "jobid", None)
res = job.get_results()
dt = time.time() - t0
rec = dict(n_pairs=int(a.n), n_cones=int(len(upt["pair_id"])), radius_arcsec=[float(np.min(upt["radius_deg"]) * 3600), float(np.max(upt["radius_deg"]) * 3600)],
           rows=int(len(res)), seconds=round(dt, 1), sha256=hashlib.sha256(open(p, "rb").read()).hexdigest(), query=q, jobid=str(jid),
           note="timing probe for the approved Q1 pilot (owner's go, 2026-09-29): the same pairs and ADQL as the pilot's first pairs")
rec["constant_radius_deg"] = float(rmax) if a.constant_radius else None
rec["healpix"] = bool(a.healpix)
(HERE / f"manifest_q1_{a.tag}.json").write_text(json.dumps(rec, indent=1) + "\n")
print(json.dumps({k: v for k, v in rec.items() if k != "query"}))
