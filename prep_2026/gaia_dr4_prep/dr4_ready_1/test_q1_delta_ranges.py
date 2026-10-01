#!/usr/bin/env python3
"""DR4-READY-1: OFFLINE test of q1_delta_ranges.py (the DR3 delta Q1) against a synthetic archive that mimics the synchronous endpoint (NEW file; NO NETWORK, socket guard).

The fake archive holds (a) the REAL local-extract (stage A) sources inside the first 300 DELTA pairs' cones with their REAL source_ids and (b) random synthetic sources in discs around each component (20 % of the pairs 3x denser), each with a
source_id from its level-12 HEALPix pixel.  It answers the script's literal source_id-range queries, SILENTLY TRUNCATES any result to 2000 rows, raises once (a dropped connection), hangs once (cut by the client's 1 s alarm) and, in the resume
test, CRASHES the first run (a KeyboardInterrupt) after 20 queries.  Checks (PASS/FAIL):
  T1 the fetch (with a crash and a resume) returns exactly the brute-force rows inside the exact cones, pair_id = the row index in q1_delta_pairs.csv; T2 the truncation path was exercised; T3 no truncated result reached the output;
  T4 every local-extract source in the cones is in the output; T5 / T5b / T5c the accepted-bytes, transfer and query-count caps (the module's DELTA constants) stop the run, write the reason and keep the cache; T6 the flaky query was retried;
  T7 the hung query was cut and retried; T8 the crashed first run left a cache and the second run RESUMED from it; T9 a cache from a different plan is refused;
  D1 without --owner-go-recorded text the script refuses and issues no query; D2 --plan-only issues no query; D3 q1_full_ranges' module constants are restored after a finished run, a stopped run and a crashed run;
  D4 the caps the fetch loop actually sees during the real run are the DELTA caps (100 MB / 130 MB / 4000), not the full-size Q1's (200 MB / 260 MB / 9000); D5 a pairs file whose sha256 differs from the recorded one is refused before any query.  D6 the real manifests are untouched.
MUTATE=1: truncation detection disabled (SYNC_CAP -> 10**9): T1 must FAIL.  MUTATE=2: the plan reads the FINAL pairs file instead of the delta list: T1 must FAIL.  MUTATE=3: the caps are NOT pointed at the delta values (the context
manager does nothing): T5 and D4 must FAIL.  Outputs go to separate files.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_q1_delta_ranges.py"""
import sys
sys.dont_write_bytecode = True
import json, os, socket, tempfile, time
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline test (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import q1_delta_ranges as QD
import q1_full_ranges as QF
import q1_pilot_ranges as Q1
from astropy.table import Table
from scipy.spatial import cKDTree
import healpy as hp

MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, CHK = [], {}
import hashlib
_sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest() if Path(p).exists() else None
REAL_MANIFESTS = {p: _sha(p) for p in (HERE / 'manifest_q1_full.json', HERE / 'manifest_q1_delta.json')}      # the test must never touch the real manifests
_safe = Path(tempfile.mkdtemp())
QF.MAN, QF.OUT = _safe / 'full_manifest_must_stay_untouched.json', _safe                                    # so that even a MUTATED path cannot write into the real manifest or data directory
FULL_DEFAULTS = {k: getattr(QF, k) for k in QD._PointFullQ1AtDelta.NAMES}
DELTA_CAPS = (QD.CAP_ACCEPTED_BYTES, QD.CAP_TRANSFER_BYTES, QD.MAX_QUERIES)


def P(s):
    print(s, flush=True); LOG.append(s)


def C(name, ok):
    CHK[name.split()[0]] = bool(ok); P(f"{name}: {'PASS' if ok else 'FAIL'}")


rng = np.random.default_rng(1711)
NP = 300
if MUT == "2":
    QD.PAIRS_CSV = QD.WB / "dr3_extract" / "wide_binaries_dr3.csv"                  # the plan reads the FINAL pairs file (fields source_id1, source_id2 as well)
    plan_truth_csv = Q1.IN_DIR / "q1_delta_pairs.csv"
else:
    plan_truth_csv = QD.PAIRS_CSV
plan = QD.plan_delta(plan_truth_csv, NP)                                           # the truth is always built for the DELTA pairs
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
P("DR3 DELTA Q1: offline test against a synthetic archive" + (f"   *** MUTATE={MUT}: " + {"1": "truncation detection disabled (T1 must FAIL)", "2": "the plan reads the FINAL pairs file (T1 must FAIL)",
                                                                                        "3": "the caps are not pointed at the delta values (T5 and D4 must FAIL)"}[MUT] + " ***" if MUT else ""))
P(f"synthetic archive: {len(CAT):,d} sources ({len(real)} real local-extract ones) for the first {NP} delta pairs; brute-force truth: {len(truth):,d} (pair, comp, source) rows; {len(plan['rng'])} planned ranges")
STAT = dict(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0, crash_at=None, caps_seen=None)
TRUE_CAP = 2000


def fake_launch(q, path):
    STAT["calls"] += 1
    if STAT["caps_seen"] is None:
        STAT["caps_seen"] = (QF.CAP_ACCEPTED_BYTES, QF.CAP_TRANSFER_BYTES, QF.MAX_QUERIES)       # what the fetch loop sees at its first query
    if STAT["crash_at"] and STAT["calls"] == STAT["crash_at"]:
        raise KeyboardInterrupt("simulated crash")
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
    CAT[idx].write(path, format="fits", overwrite=True)


Q1.launch_query = fake_launch
Q1.TIMEOUT_S = 1
Q1.PAUSE_S = 0.0
QD.PAUSE_S = 0.0
QF.PAUSE_S = 0.0
FULL_DEFAULTS["PAUSE_S"] = 0.0
time.sleep = lambda s: None
if MUT == "1":
    Q1.SYNC_CAP = 10 ** 9
if MUT == "3":
    QD._PointFullQ1AtDelta.__enter__ = lambda self: self
    QD._PointFullQ1AtDelta.__exit__ = lambda self, *e: False


def run(td, go="test: offline mock archive", extra=()):
    QD.OUT = Path(td); QD.CACHE = Path(td) / "q1_delta_cache"; QD.MAN = Path(td) / "manifest.json"
    sys.argv = ["q1_delta_ranges.py", *(["--owner-go-recorded", go] if go is not None else []), "--max-pairs", str(NP), *extra]
    try:
        QD.main()
        return None
    except SystemExit as e:
        return str(e)
    except KeyboardInterrupt:
        return "CRASH"
    except AssertionError as e:
        return "ASSERT: " + str(e)


def result(td):
    f = Path(td) / "q1_delta_neighbours.fits"
    if not f.exists():
        return None, {}
    E = Table.read(f, format="fits")
    man = json.loads((Path(td) / "manifest.json").read_text()) if (Path(td) / "manifest.json").exists() else {}
    return set(zip(np.asarray(E["pair_id"], np.int64).tolist(), np.asarray(E["comp"], np.int64).tolist(), np.asarray(E["source_id"], np.int64).tolist())), man


restored = lambda: all(getattr(QF, k) == v for k, v in FULL_DEFAULTS.items())
with tempfile.TemporaryDirectory() as td:
    STAT.update(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0, crash_at=20, caps_seen=None)
    errA = run(td)
    callsA = STAT["calls"]
    rest_crash = restored()
    cache_files = sorted((Path(td) / "q1_delta_cache").glob("b*.fits"))
    P(f"run A ended with: {errA} after {callsA} calls; the cache holds {len(cache_files)} accepted batches")
    STAT.update(crash_at=None); STAT["calls"] = 0
    errB = run(td)
    callsB = STAT["calls"]
    rest_done = restored()
    got, man = result(td)
    P(f"run B (resume) ended with: {errB}; {callsB} new calls; manifest queries_total {man.get('queries_total')}; truncated by the endpoint in total {STAT['truncated']}")
    t1 = got == truth if got is not None else False
    miss_n = len(truth - got) if got is not None else "n/a"; spur_n = len(got - truth) if got is not None else "n/a"
    C(f"T1 the fetch (crash + resume) equals the brute-force truth, pair_id = the row index of the delta pairs file (missing {miss_n}, spurious {spur_n})", t1)
    C(f"T2 the truncation path was exercised ({STAT['truncated']} truncated results in total)", STAT["truncated"] > 0)
    C(f"T3 no truncated result reached the output (manifest counts {man.get('truncated_results_discarded')} discarded, endpoint truncated {STAT['truncated']})", t1 and man.get("truncated_results_discarded") == STAT["truncated"])
    C(f"T4 every local-extract source in the cones is in the output (missing {man.get('local_extract_sources_missing_from_fetch')} of {man.get('local_extract_sources_in_cones')})", man.get("local_extract_sources_missing_from_fetch") == 0)
    C("T6 the flaky query was retried (hit 1)", STAT["flaky_hit"] == 1)
    C("T7 the hung query was cut by the client timeout and retried (hit 1)", STAT["hang_hit"] == 1)
    C(f"T8 the crashed run A left a cache ({len(cache_files)} batches) and run B RESUMED from it (batches_resumed_from_cache {man.get('batches_resumed_from_cache')}) with fewer queries than a fresh run needs ({man.get('queries_total')} in total)",
      errA == "CRASH" and len(cache_files) > 0 and man.get("batches_resumed_from_cache", 0) > 0 and callsB < man.get("queries_total", 0))
    C(f"D3a q1_full_ranges' module constants are restored after a CRASHED run ({rest_crash}) and after a FINISHED run ({rest_done})", rest_crash and rest_done)
    C(f"D4 the caps the fetch loop sees during the real run are the DELTA caps {DELTA_CAPS} = (100 MB, 130 MB, 4000), not the full-size Q1's {tuple(FULL_DEFAULTS[k] for k in ('CAP_ACCEPTED_BYTES', 'CAP_TRANSFER_BYTES', 'MAX_QUERIES'))} (seen {STAT['caps_seen']})",
      STAT["caps_seen"] == DELTA_CAPS == (100_000_000, 130_000_000, 4000))
    # T9: a cache from a different plan is refused
    (Path(td) / "q1_delta_cache" / "state.json").write_text(json.dumps({"plan_hash": "0" * 16}))
    try:
        run_t9 = run(td)
        refused = bool(run_t9) and "different plan" in run_t9
    except AssertionError as e:
        refused = "different plan" in str(e)
    C("T9 a cache that belongs to a different plan is refused", refused)

    # T5 / T5b / T5c: the (delta) caps stop the run, write the reason and keep the cache
    saved = (QD.CAP_ACCEPTED_BYTES, QD.CAP_TRANSFER_BYTES, QD.MAX_QUERIES)
    with tempfile.TemporaryDirectory() as td2:
        QD.CAP_ACCEPTED_BYTES = 300_000
        STAT.update(calls=0, flaky_done=True, hang_done=True)
        err5 = run(td2)
        man5 = json.loads((Path(td2) / "manifest.json").read_text()) if (Path(td2) / "manifest.json").exists() else {}
        C(f"T5 the accepted-bytes cap stops the run, writes the reason and keeps the cache ({err5[:80] if err5 else None})", bool(err5) and "STOPPED" in err5 and "stopped" in man5 and len(list((Path(td2) / "q1_delta_cache").glob("b*.fits"))) > 0)
        rest_stop = restored()
        QD.CAP_ACCEPTED_BYTES = saved[0]
    with tempfile.TemporaryDirectory() as td3:
        QD.CAP_TRANSFER_BYTES = 400_000
        STAT.update(calls=0)
        err5b = run(td3)
        C(f"T5b the transfer cap stops the run ({err5b[:80] if err5b else None})", bool(err5b) and "STOPPED" in err5b)
        QD.CAP_TRANSFER_BYTES = saved[1]
    with tempfile.TemporaryDirectory() as td4:
        QD.MAX_QUERIES = 5
        STAT.update(calls=0)
        err5c = run(td4)
        C(f"T5c the query-count cap stops the run ({err5c[:80] if err5c else None})", bool(err5c) and "STOPPED" in err5c and "more than 5 queries" in err5c)
        QD.MAX_QUERIES = saved[2]
    C(f"D3b q1_full_ranges' module constants are restored after a run STOPPED by a cap ({rest_stop})", rest_stop)

    # D1 / D2 / D5: refusals and plan-only issue no query
    with tempfile.TemporaryDirectory() as td5:
        STAT.update(calls=0)
        errD1 = run(td5, go=None)
        C(f"D1 without --owner-go-recorded the script refuses and issues no query ({errD1[:70] if errD1 else None}; queries {STAT['calls']})", bool(errD1) and "refused" in errD1 and STAT["calls"] == 0)
        STAT.update(calls=0)
        errD1b = run(td5, go="   ")
        C(f"D1b a blank --owner-go-recorded text is refused too (queries {STAT['calls']})", bool(errD1b) and "refused" in errD1b and STAT["calls"] == 0)
        STAT.update(calls=0)
        errD2 = run(td5, extra=("--plan-only",))
        C(f"D2 --plan-only issues no query and writes no output (queries {STAT['calls']}; output file exists: {(Path(td5) / 'q1_delta_neighbours.fits').exists()})", errD2 is None and STAT["calls"] == 0 and not (Path(td5) / "q1_delta_neighbours.fits").exists())
    with tempfile.TemporaryDirectory() as td6:
        QD.OUT = Path(td6); QD.CACHE = Path(td6) / "c"; QD.MAN = Path(td6) / "m.json"
        old_json = QD.PAIRS_JSON
        bad = Path(td6) / "pairs.json"; bad.write_text(json.dumps({"sha256": "0" * 64}))
        QD.PAIRS_JSON = bad
        STAT.update(calls=0)
        sys.argv = ["q1_delta_ranges.py", "--owner-go-recorded", "test"]                   # no --max-pairs: the hash guard applies
        try:
            QD.main(); got_assert = ""
        except AssertionError as e:
            got_assert = str(e)
        finally:
            QD.PAIRS_JSON = old_json
        C(f"D5 a pairs file whose sha256 differs from the recorded one is refused before any query (queries {STAT['calls']}: {got_assert[:60]})", "is not the file" in got_assert and STAT["calls"] == 0)

C("D6 the real manifests (manifest_q1_full.json, manifest_q1_delta.json) are exactly as before the test", all(_sha(p) == h for p, h in REAL_MANIFESTS.items()))
if MUT:
    expect = {"1": ("T1",), "2": ("T1",), "3": ("T5", "D4")}[MUT]
    bit = all(not CHK.get(k, True) for k in expect)
    P(f"\n[MUTATE CONTROL] MUTATE={MUT}: {', '.join(expect)} {'FAILED as designed' if bit else 'did NOT fail: the control does not bite'}; checks that failed: {[k for k, v in CHK.items() if not v]}")
    ok = bit
else:
    ok = all(CHK.values())
    P(f"\n{sum(CHK.values())}/{len(CHK)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}")
(HERE / f"test_q1_delta_ranges{SFX}.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
