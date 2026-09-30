#!/usr/bin/env python3
"""DR4-READY-1: OFFLINE test of q1_pilot_ranges.py against a synthetic archive that mimics the synchronous endpoint (NEW file; NO NETWORK, socket guard).

The fake archive holds (a) the REAL local-extract (stage A) sources inside the pilot's cones with their REAL source_ids and (b) random synthetic sources in discs around each
component (7k sources/deg2, half the real field density so that the mock stays inside the 20 MB accepted cap; 20 % of the pairs 3x denser, so that some batches exceed the endpoint's 2000-row cap), each given a source_id from its level-12 HEALPix pixel.  It answers the
script's literal source_id-range queries and SILENTLY TRUNCATES any result to 2000 rows, and it raises once mid-run (a flaky connection) and hangs once (a stalled query, cut by the client's 1 s alarm).  Checks (each PASS/FAIL):
  T1 the fetch returns exactly the brute-force rows inside the exact cones (no row lost, no spurious row); T2 the truncation path was exercised (some results were discarded);
  T3 no truncated result reached the output; T4 every local-extract source in the cones is in the output (the script's own completeness count is 0); T5 the transfer/accepted
  caps stop the run and write the reason to the manifest; T6 the flaky query was retried; T7 the hung query was cut by the alarm and retried.
MUTATE control (--mutate, outputs named *_MUTATE): the script's truncation detection is disabled (SYNC_CAP -> 10**9) while the fake still truncates: T1 must FAIL (rows lost),
otherwise the test could not catch a missing split.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_q1_pilot_ranges.py [--mutate]
"""
import sys
sys.dont_write_bytecode = True
import json, socket, tempfile, time
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline test (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import q1_pilot_ranges as R
from astropy.table import Table
from scipy.spatial import cKDTree
import healpy as hp

MUTATE = "--mutate" in sys.argv
LOG, CHK = [], []


def P(s):
    print(s, flush=True); LOG.append(s)


def C(name, ok):
    CHK.append(bool(ok)); P(f"{name}: {'PASS' if ok else 'FAIL'}")


rng = np.random.default_rng(1305)
plan = R.plan()
A, n_pair = plan["A"], len(plan["pick"])
# ---- the synthetic archive -------------------------------------------------------------------------------------------------------------------------------------------
cols = {k: [] for k in R.KEEP}
def add(sid, ra, dec):
    m = len(sid)
    cols["source_id"].append(np.asarray(sid, np.int64)); cols["ra"].append(ra); cols["dec"].append(dec)
    cols["parallax"].append(rng.uniform(0.1, 6, m)); cols["parallax_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32))
    cols["pmra"].append(rng.normal(0, 8, m)); cols["pmdec"].append(rng.normal(0, 8, m))
    cols["pmra_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32)); cols["pmdec_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32))
    cols["phot_g_mean_mag"].append(rng.uniform(8, 21, m).astype(np.float32))

dense = rng.random(n_pair) < 0.20
dens = np.where(dense, 3 * 7.0e3, 7.0e3)                                    # sources per deg2
for k in range(n_pair):
    for v in (plan["va"][k], plan["vb"][k]):
        rad = (plan["R"][k] + 45.0) / 3600.0                                    # deg
        m = rng.poisson(dens[k] * np.pi * rad ** 2)
        if m == 0:
            continue
        # uniform points in a small-angle disc around v
        th = np.sqrt(rng.random(m)) * np.radians(rad); ph = rng.random(m) * 2 * np.pi
        e1 = np.cross(v, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(v, e1)
        pts = v[None, :] * np.cos(th)[:, None] + np.sin(th)[:, None] * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
        ra = np.degrees(np.arctan2(pts[:, 1], pts[:, 0])) % 360; dec = np.degrees(np.arcsin(np.clip(pts[:, 2], -1, 1)))
        pix = hp.ang2pix(2 ** R.LEVEL, ra, dec, nest=True, lonlat=True)
        add(pix.astype(np.int64) * R.DIV + rng.integers(0, R.DIV, m), ra, dec)
# the real local-extract sources near the cones, with their REAL source_ids
tree_A = cKDTree(R.vec(np.asarray(A["ra"], float), np.asarray(A["dec"], float)))
real = set()
for k in range(n_pair):
    for v in (plan["va"][k], plan["vb"][k]):
        real.update(tree_A.query_ball_point(v, r=2 * np.sin(np.radians((plan["R"][k] + 45.0) / 3600) / 2)))
real = np.array(sorted(real), int)
add(np.asarray(A["source_id"])[real], np.asarray(A["ra"], float)[real], np.asarray(A["dec"], float)[real])
CAT = Table({k: np.concatenate(v) for k, v in cols.items()})
CAT = CAT[np.argsort(np.asarray(CAT["source_id"]))]
_, u = np.unique(np.asarray(CAT["source_id"]), return_index=True)
CAT = CAT[np.sort(u)]
SID = np.asarray(CAT["source_id"], np.int64)
P(f"synthetic archive: {len(CAT):,d} sources ({len(real)} real local-extract ones), {int(dense.sum())} of {n_pair} pairs 3x denser")
# ---- the brute-force truth --------------------------------------------------------------------------------------------------------------------------------------------
tree = cKDTree(R.vec(np.asarray(CAT["ra"], float), np.asarray(CAT["dec"], float)))
truth = set()
for k in range(n_pair):
    chord = 2 * np.sin(np.radians(plan["R"][k] / 3600) / 2)
    for c, vc in ((0, plan["va"][k]), (1, plan["vb"][k])):
        for j in tree.query_ball_point(vc, r=chord):
            truth.add((int(plan["pick"][k]), c, int(SID[j])))
P(f"brute-force truth: {len(truth):,d} (pair, comp, source) rows inside the exact cones")
# ---- the fake synchronous endpoint ------------------------------------------------------------------------------------------------------------------------------------
STAT = dict(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0, sizes=[])


def fake_launch(q, path):
    STAT["calls"] += 1
    if STAT["calls"] == 5 and not STAT["flaky_done"]:
        STAT["flaky_done"] = True; STAT["flaky_hit"] += 1
        raise ConnectionError("simulated dropped connection")
    if STAT["calls"] == 9 and not STAT["hang_done"]:
        STAT["hang_done"] = True; STAT["hang_hit"] += 1
        t_end = time.time() + 4.0
        while time.time() < t_end:                                              # a hung archive: only the client's alarm can end this
            pass
    rs = R.RANGE_RE.findall(q)
    assert rs, "the query carries no source_id ranges"
    idx = np.concatenate([np.arange(np.searchsorted(SID, int(lo), "left"), np.searchsorted(SID, int(hi), "left")) for lo, hi in rs]) if rs else np.array([], int)
    if len(idx) > R.SYNC_CAP_TRUE:
        idx = idx[:R.SYNC_CAP_TRUE]; STAT["truncated"] += 1                     # the endpoint silently truncates
    STAT["sizes"].append(len(idx))
    CAT[idx].write(path, format="fits", overwrite=True)


R.SYNC_CAP_TRUE = 2000                                                          # what the fake endpoint enforces
R.launch_query = fake_launch
R.PAUSE_S = 0.0
R.TIMEOUT_S = 1                                                                 # the fake hangs once for 4 s
time.sleep = lambda s: None                                                     # no real waiting on retries
if MUTATE:
    R.SYNC_CAP = 10 ** 9                                                        # the script can no longer see truncation
res = {}


def run_once(tag):
    with tempfile.TemporaryDirectory() as td:
        R.OUT = Path(td); R.MAN = Path(td) / "manifest.json"
        STAT.update(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0, sizes=[])
        sys.argv = ["q1_pilot_ranges.py", "--owner-go-recorded"]
        try:
            R.main()
            E = Table.read(Path(td) / "q1_pilot_neighbours.fits", format="fits")
            man = json.loads((Path(td) / "manifest.json").read_text())
            return E, man, None
        except SystemExit as e:
            man = json.loads((Path(td) / "manifest.json").read_text()) if (Path(td) / "manifest.json").exists() else {}
            return None, man, str(e)


E, man, err = run_once("main")
P(f"main run ended with: {err}" if err else "main run completed")
got = set(zip(np.asarray(E["pair_id"], np.int64).tolist(), np.asarray(E["comp"], np.int64).tolist(), np.asarray(E["source_id"], np.int64).tolist())) if E is not None else set()
P(f"fetch: {STAT['calls']} queries, {STAT['truncated']} truncated by the endpoint, result sizes max {max(STAT['sizes'])}; script rows {len(got):,d}")
t1 = got == truth
n_trunc, n_hit, n_hang = STAT["truncated"], STAT["flaky_hit"], STAT["hang_hit"]
if MUTATE:
    P(f"T1 exact set equals the brute-force truth (missing {len(truth - got)}, spurious {len(got - truth)}): {'PASS' if t1 else 'FAIL'}")
    P("MUTATE: truncation detection disabled; T1 must FAIL for the test to be able to catch a missing split: " + ("OK (T1 failed as required)" if not t1 else "PROBLEM: T1 passed with detection disabled"))
    ok = not t1
else:
    C(f"T1 exact set equals the brute-force truth (missing {len(truth - got)}, spurious {len(got - truth)})", t1)
    C(f"T2 the truncation path was exercised ({n_trunc} truncated results)", n_trunc > 0)
    C(f"T3 no truncated result reached the output (manifest counts {man.get('truncated_results_discarded')} discarded, endpoint truncated {n_trunc})",
      man.get("truncated_results_discarded") == n_trunc and t1)
    C(f"T4 every local-extract source in the cones is in the output (script count: missing {man.get('local_extract_sources_missing_from_fetch')} of {man.get('local_extract_sources_in_cones')})",
      man.get("local_extract_sources_missing_from_fetch") == 0)
    C(f"T6 the flaky query was retried (hit {n_hit}, run completed)", n_hit == 1 and E is not None)
    C(f"T7 a hung query was cut by the client timeout and retried (hangs {n_hang}, run completed)", n_hang == 1 and E is not None)
    R.CAP_ACCEPTED_BYTES = 200_000
    E2, man2, err2 = run_once("cap")
    C(f"T5 the accepted-bytes cap stops the run and writes the reason ({err2[:70] if err2 else None})", err2 and "STOPPED" in err2 and "stopped" in man2)
    R.CAP_ACCEPTED_BYTES = 20_000_000; R.CAP_TRANSFER_BYTES = 300_000
    E3, man3, err3 = run_once("transfer")
    C(f"T5b the transfer cap stops the run ({err3[:70] if err3 else None})", err3 and "STOPPED" in err3 and "stopped" in man3)
    ok = all(CHK)
P("RESULT: " + ("all checks behave as required" if ok else "CHECK FAILED"))
(HERE / ("test_q1_pilot_ranges" + ("_MUTATE" if MUTATE else "") + ".out")).write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
