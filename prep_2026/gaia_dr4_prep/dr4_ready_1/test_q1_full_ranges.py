#!/usr/bin/env python3
"""DR4-READY-1: OFFLINE test of q1_full_ranges.py (the full-size Q1, with the resume) against a synthetic archive that mimics the synchronous endpoint (NEW file; NO NETWORK, socket guard).

The fake archive holds (a) the REAL local-extract (stage A) sources inside the first 300 final pairs' cones with their REAL source_ids and (b) random synthetic sources in discs around each component
(20 % of the pairs 3x denser), each given a source_id from its level-12 HEALPix pixel.  It answers the script's literal source_id-range queries, SILENTLY TRUNCATES any result to 2000 rows, raises once
(a dropped connection), hangs once (cut by the client's 1 s alarm) and, in the resume test, CRASHES the process's first run (a KeyboardInterrupt) after 20 queries.  Checks (PASS/FAIL):
  T1 the fetch (with a crash and a resume) returns exactly the brute-force rows inside the exact cones; T2 the truncation path was exercised; T3 no truncated result reached the output;
  T4 every local-extract source in the cones is in the output; T5 the byte caps stop the run, write the reason and keep the cache; T6 the flaky query was retried; T7 the hung query was cut and retried;
  T8 the crashed first run left a cache and the second run RESUMED from it (batches_resumed_from_cache > 0) and needed fewer queries than a fresh run; T9 a cache from a different plan is refused.
MUTATE control (--mutate, outputs named *_MUTATE): the script's truncation detection is disabled (SYNC_CAP -> 10**9) while the fake still truncates: T1 must FAIL.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_q1_full_ranges.py [--mutate]
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
import q1_full_ranges as Q
import q1_pilot_ranges as Q1
from astropy.table import Table
from scipy.spatial import cKDTree
import healpy as hp

MUTATE = "--mutate" in sys.argv
LOG, CHK = [], []


def P(s):
    print(s, flush=True); LOG.append(s)


def C(name, ok):
    CHK.append(bool(ok)); P(f"{name}: {'PASS' if ok else 'FAIL'}")


rng = np.random.default_rng(1711)
NP = 300
plan = Q.plan_full(NP)
A = plan["A"]
cols = {k: [] for k in Q1.KEEP}


def add(sid, ra, dec):
    m = len(sid)
    cols["source_id"].append(np.asarray(sid, np.int64)); cols["ra"].append(ra); cols["dec"].append(dec)
    cols["parallax"].append(rng.uniform(0.1, 6, m)); cols["parallax_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32))
    cols["pmra"].append(rng.normal(0, 8, m)); cols["pmdec"].append(rng.normal(0, 8, m))
    cols["pmra_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32)); cols["pmdec_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32))
    cols["phot_g_mean_mag"].append(rng.uniform(8, 21, m).astype(np.float32))


dense = rng.random(NP) < 0.20
dens = np.where(dense, 3 * 7.0e3, 7.0e3)
for k in range(NP):
    for v in (plan["va"][k], plan["vb"][k]):
        rad = (plan["R"][k] + 45.0) / 3600.0
        m = rng.poisson(dens[k] * np.pi * rad ** 2)
        if m == 0:
            continue
        th = np.sqrt(rng.random(m)) * np.radians(rad); ph = rng.random(m) * 2 * np.pi
        e1 = np.cross(v, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(v, e1)
        pts = v[None, :] * np.cos(th)[:, None] + np.sin(th)[:, None] * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
        ra = np.degrees(np.arctan2(pts[:, 1], pts[:, 0])) % 360; dec = np.degrees(np.arcsin(np.clip(pts[:, 2], -1, 1)))
        pix = hp.ang2pix(2 ** Q1.LEVEL, ra, dec, nest=True, lonlat=True)
        add(pix.astype(np.int64) * Q1.DIV + rng.integers(0, Q1.DIV, m), ra, dec)
tree_A = cKDTree(Q1.vec(np.asarray(A["ra"], float), np.asarray(A["dec"], float)))
real = set()
for k in range(NP):
    for v in (plan["va"][k], plan["vb"][k]):
        real.update(tree_A.query_ball_point(v, r=2 * np.sin(np.radians((plan["R"][k] + 45.0) / 3600) / 2)))
real = np.array(sorted(real), int)
add(np.asarray(A["source_id"])[real], np.asarray(A["ra"], float)[real], np.asarray(A["dec"], float)[real])
CAT = Table({k: np.concatenate(v) for k, v in cols.items()})
CAT = CAT[np.argsort(np.asarray(CAT["source_id"]))]
_, u = np.unique(np.asarray(CAT["source_id"]), return_index=True)
CAT = CAT[np.sort(u)]
SID = np.asarray(CAT["source_id"], np.int64)
tree = cKDTree(Q1.vec(np.asarray(CAT["ra"], float), np.asarray(CAT["dec"], float)))
truth = set()
for k in range(NP):
    chord = 2 * np.sin(np.radians(plan["R"][k] / 3600) / 2)
    for c, vc in ((0, plan["va"][k]), (1, plan["vb"][k])):
        for j in tree.query_ball_point(vc, r=chord):
            truth.add((int(plan["pick"][k]), c, int(SID[j])))
P(f"synthetic archive: {len(CAT):,d} sources ({len(real)} real local-extract ones) for {NP} pairs; brute-force truth: {len(truth):,d} (pair, comp, source) rows; {len(plan['rng'])} planned ranges")
STAT = dict(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0, crash_at=None, sizes=[])
TRUE_CAP = 2000


def fake_launch(q, path):
    STAT["calls"] += 1
    if STAT["crash_at"] and STAT["calls"] == STAT["crash_at"]:
        raise KeyboardInterrupt("simulated crash")                                # a BaseException: it propagates out of run_query's retry loop like a killed process
    if STAT["calls"] == 5 and not STAT["flaky_done"]:
        STAT["flaky_done"] = True; STAT["flaky_hit"] += 1
        raise ConnectionError("simulated dropped connection")
    if STAT["calls"] == 9 and not STAT["hang_done"]:
        STAT["hang_done"] = True; STAT["hang_hit"] += 1
        t_end = time.time() + 4.0
        while time.time() < t_end:
            pass
    rs = Q1.RANGE_RE.findall(q)
    assert rs, "the query carries no source_id ranges"
    idx = np.concatenate([np.arange(np.searchsorted(SID, int(lo), "left"), np.searchsorted(SID, int(hi), "left")) for lo, hi in rs])
    if len(idx) > TRUE_CAP:
        idx = idx[:TRUE_CAP]; STAT["truncated"] += 1
    STAT["sizes"].append(len(idx))
    CAT[idx].write(path, format="fits", overwrite=True)


Q1.launch_query = fake_launch
Q1.TIMEOUT_S = 1
Q1.PAUSE_S = 0.0
Q.PAUSE_S = 0.0
time.sleep = lambda s: None
if MUTATE:
    Q1.SYNC_CAP = 10 ** 9


def run(td, argv_extra=()):
    Q.OUT = Path(td); Q.CACHE = Path(td) / "q1_full_cache"; Q.MAN = Path(td) / "manifest.json"
    sys.argv = ["q1_full_ranges.py", "--owner-go-recorded", "--max-pairs", str(NP), *argv_extra]
    try:
        Q.main()
        return None
    except SystemExit as e:
        return str(e)
    except KeyboardInterrupt:
        return "CRASH"


def result(td):
    f = Path(td) / "q1_full_neighbours.fits"
    if not f.exists():
        return None, None
    E = Table.read(f, format="fits")
    return set(zip(np.asarray(E["pair_id"], np.int64).tolist(), np.asarray(E["comp"], np.int64).tolist(), np.asarray(E["source_id"], np.int64).tolist())), \
        (json.loads((Path(td) / "manifest.json").read_text()) if (Path(td) / "manifest.json").exists() else {})


with tempfile.TemporaryDirectory() as td:
    # run A: a fresh run that CRASHES after 20 queries; run B resumes
    STAT.update(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0, crash_at=20)
    errA = run(td)
    callsA = STAT["calls"]
    cache_files = sorted((Path(td) / "q1_full_cache").glob("b*.fits"))
    P(f"run A ended with: {errA} after {callsA} calls; the cache holds {len(cache_files)} accepted batches")
    STAT.update(crash_at=None)
    STAT["calls"] = 0
    errB = run(td)
    callsB = STAT["calls"]
    got, man = result(td)
    P(f"run B (resume) ended with: {errB}; {callsB} new calls; manifest queries_total {man.get('queries_total') if man else None}; truncated by the endpoint in total {STAT['truncated']}")
    t1 = got == truth if got is not None else False
    if MUTATE:
        P(f"T1 the output equals the brute-force truth (missing {len(truth - got) if got is not None else 'n/a'}, spurious {len(got - truth) if got is not None else 'n/a'}): {'PASS' if t1 else 'FAIL'}")
        P("MUTATE: truncation detection disabled; T1 must FAIL for the test to be able to catch a missing split: " + ("OK (T1 failed as required)" if not t1 else "PROBLEM: T1 passed with detection disabled"))
        ok = not t1
    else:
        C(f"T1 the fetch (crash + resume) equals the brute-force truth (missing {len(truth - got) if got else 'n/a'}, spurious {len(got - truth) if got else 'n/a'})", t1)
        C(f"T2 the truncation path was exercised ({STAT['truncated']} truncated results in total)", STAT["truncated"] > 0)
        C(f"T3 no truncated result reached the output (manifest counts {man.get('truncated_results_discarded')} discarded, endpoint truncated {STAT['truncated']})", t1 and man.get("truncated_results_discarded") == STAT["truncated"])
        C(f"T4 every local-extract source in the cones is in the output (missing {man.get('local_extract_sources_missing_from_fetch')} of {man.get('local_extract_sources_in_cones')})", man.get("local_extract_sources_missing_from_fetch") == 0)
        C("T6 the flaky query was retried (hit 1)", STAT["flaky_hit"] == 1)
        C("T7 the hung query was cut by the client timeout and retried (hit 1)", STAT["hang_hit"] == 1)
        C(f"T8 the crashed run A left a cache ({len(cache_files)} batches) and run B RESUMED from it (batches_resumed_from_cache {man.get('batches_resumed_from_cache')}) with fewer queries than a fresh run needs ({man.get('queries_total')} in total)",
          errA == "CRASH" and len(cache_files) > 0 and man.get("batches_resumed_from_cache", 0) > 0 and callsB < man.get("queries_total", 0))
        # T9: a cache from a different plan is refused
        st = json.loads((Path(td) / "q1_full_cache" / "state.json").read_text())
        (Path(td) / "q1_full_cache" / "state.json").write_text(json.dumps({"plan_hash": "0" * 16}))
        try:
            run(td)
            refused = False
        except AssertionError as e:
            refused = "different plan" in str(e)
        C("T9 a cache that belongs to a different plan is refused", refused)
        # T5: the caps stop the run, write the reason and keep the cache
        with tempfile.TemporaryDirectory() as td2:
            Q.CAP_ACCEPTED_BYTES = 300_000
            STAT.update(calls=0, flaky_done=True, hang_done=True)
            err5 = run(td2)
            man5 = json.loads((Path(td2) / "manifest.json").read_text()) if (Path(td2) / "manifest.json").exists() else {}
            C(f"T5 the accepted-bytes cap stops the run, writes the reason and keeps the cache ({err5[:70] if err5 else None})", err5 and "STOPPED" in err5 and "stopped" in man5 and len(list((Path(td2) / "q1_full_cache").glob("b*.fits"))) > 0)
            Q.CAP_ACCEPTED_BYTES = 200_000_000; Q.CAP_TRANSFER_BYTES = 400_000
        with tempfile.TemporaryDirectory() as td3:
            STAT.update(calls=0, flaky_done=True, hang_done=True)
            err5b = run(td3)
            C(f"T5b the transfer cap stops the run ({err5b[:70] if err5b else None})", err5b and "STOPPED" in err5b)
        ok = all(CHK)
P("RESULT: " + ("all checks behave as required" if ok else "CHECK FAILED"))
(HERE / ("test_q1_full_ranges" + ("_MUTATE" if MUTATE else "") + ".out")).write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
