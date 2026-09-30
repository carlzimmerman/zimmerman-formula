#!/usr/bin/env python3
"""DR4-READY-1: OFFLINE test of q3_delta_chunks.py (the full-size Q3 in its delta form) against a synthetic archive that mimics the synchronous endpoint (NEW file; NO NETWORK, socket guard).

The fake archive is a synthetic gaia_source-like table over the WHOLE source_id span of the twelve level-0 chunks (500k rows, the frozen column list and dtypes) in which each of the frozen
WHERE's conditions removes some rows, a random 0.03 % of the rows plus a dense cluster of 3,500 rows in chunk 11 have no G magnitude.  It answers the script's literal source_id-piece queries by
APPLYING the query's own conditions, SILENTLY TRUNCATES any result to 2000 rows, raises once and hangs once.  The 'frozen chunks' 2 and 11 are built from the same table.  Checks:
  T1 for each tested chunk the assembled union is exactly the rows that pass the frozen WHERE WITHOUT the G condition inside that chunk's span; T2 the truncation path was exercised;
  T3 each union starts with the frozen rows unchanged and its appended rows all lack G; T4 column names and dtypes equal the frozen file's; T5 the per-chunk byte cap stops the run and writes
  nothing for the chunk; T6 the dropped connection was retried; T7 the hung query was cut by the alarm and retried; T8 a second run skips the finished chunks (zero queries).
MUTATE control (--mutate, outputs named *_MUTATE): the script's truncation detection is disabled (SYNC_CAP -> 10**9) while the fake still truncates: T1 must FAIL.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_q3_delta_chunks.py [--mutate]
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
import q3_delta_chunks as Q
import q1_pilot_ranges as Q1
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u

MUTATE = "--mutate" in sys.argv
LOG, CHK = [], []


def P(s):
    print(s, flush=True); LOG.append(s)


def C(name, ok):
    CHK.append(bool(ok)); P(f"{name}: {'PASS' if ok else 'FAIL'}")


rng = np.random.default_rng(4407)
FE = Q.FE
L0 = FE.LEVEL0
TESTED = (2, 11)
N = 500_000
sid = rng.integers(0, 12 * L0, N)
ra = rng.random(N) * 360; dec = np.degrees(np.arcsin(rng.uniform(-1, 1, N)))
par = np.where(rng.random(N) < 0.55, rng.uniform(3.6, 12, N), rng.uniform(0.05, 3.4, N))
pe = np.where(rng.random(N) < 0.01, rng.uniform(2, 3, N), rng.uniform(0.01, 0.6, N)).astype(np.float32)
g = rng.uniform(8, 20, N).astype(np.float32)
g[rng.random(N) < 0.0003] = np.nan
K = 3500
c0 = 11 * L0 + int(0.37 * L0)
ra_c = rng.random(K) * 360; dec_c = np.degrees(np.arcsin(rng.uniform(-0.7, 0.7, K)))
sid = np.concatenate([sid, c0 + rng.integers(0, 2 ** 42, K)])
ra = np.concatenate([ra, ra_c]); dec = np.concatenate([dec, dec_c])
par = np.concatenate([par, rng.uniform(3.6, 12, K)]); pe = np.concatenate([pe, rng.uniform(0.01, 0.6, K).astype(np.float32)])
g = np.concatenate([g, np.full(K, np.nan, np.float32)])
_, keep = np.unique(sid, return_index=True); keep = np.sort(keep)
sid, ra, dec, par, pe, g = sid[keep], ra[keep], dec[keep], par[keep], pe[keep], g[keep]
n = len(sid)
b = SkyCoord(ra * u.deg, dec * u.deg, frame="icrs").galactic.b.deg
tab = {"source_id": sid.astype(">i8"), "ra": ra.astype(">f8"), "dec": dec.astype(">f8"), "parallax": par.astype(">f8"), "parallax_error": pe.astype(">f4"),
       "pmra": rng.normal(0, 30, n).astype(">f8"), "pmdec": rng.normal(0, 30, n).astype(">f8"), "pmra_error": rng.uniform(0.01, 0.5, n).astype(">f4"),
       "pmdec_error": rng.uniform(0.01, 0.5, n).astype(">f4"), "pmra_pmdec_corr": rng.uniform(-1, 1, n).astype(">f4"), "phot_g_mean_mag": g.astype(">f4"),
       "bp_rp": rng.uniform(0, 3, n).astype(">f4"), "ruwe": rng.uniform(0.8, 2, n).astype(">f4"), "ipd_frac_multi_peak": rng.integers(0, 60, n).astype(">i2"),
       "radial_velocity": np.where(rng.random(n) < 0.8, np.nan, rng.normal(0, 30, n)).astype(">f4"), "radial_velocity_error": rng.uniform(0.1, 5, n).astype(">f4"),
       "non_single_star": rng.integers(0, 2, n).astype(">i2")}
assert list(tab) == [c.strip() for c in FE.COLS.split(",")]
CAT = Table(tab)
passes = (par > 3.5) & (par / pe > 5) & (pe < 2) & (np.abs(b) > 10)
has_g = ~np.isnan(g)
span = {k: (sid >= k * L0) & (sid < (k + 1) * L0) for k in TESTED}
expected = {k: set(sid[passes & span[k]].tolist()) for k in TESTED}
FROZEN = {}
for k in TESTED:
    idx = np.flatnonzero(passes & has_g & span[k]); rng.shuffle(idx); FROZEN[k] = CAT[idx]
P(f"synthetic archive: {n:,d} rows over 12 chunks; tested chunks {TESTED}; rows to fetch (no G, passing the WHERE): " + ", ".join(f"chunk {k}: {int((passes & ~has_g & span[k]).sum())}" for k in TESTED))
STAT = dict(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0)
TRUE_CAP = 2000
NEEDED = ("parallax > 3.5", "parallax_over_error > 5", "parallax_error < 2", "phot_g_mean_mag IS NULL", "ABS(b) > 10")


def fake_launch(q, path):
    STAT["calls"] += 1
    if STAT["calls"] == 4 and not STAT["flaky_done"]:
        STAT["flaky_done"] = True; STAT["flaky_hit"] += 1
        raise ConnectionError("simulated dropped connection")
    if STAT["calls"] == 9 and not STAT["hang_done"]:
        STAT["hang_done"] = True; STAT["hang_hit"] += 1
        t_end = time.time() + 4.0
        while time.time() < t_end:
            pass
    assert all(s in q for s in NEEDED) and "IS NOT NULL" not in q
    lo, hi = (int(x) for x in q.split("source_id >= ")[1].replace(" AND source_id < ", " ").split())
    m = (sid >= lo) & (sid < hi) & (par > 3.5) & (par / pe > 5) & (pe < 2) & np.isnan(g) & (np.abs(b) > 10)
    idx = np.flatnonzero(m)
    if len(idx) > TRUE_CAP:
        idx = idx[:TRUE_CAP]; STAT["truncated"] += 1
    CAT[idx].write(path, format="fits", overwrite=True)


Q1.launch_query = fake_launch
Q1.TIMEOUT_S = 1
Q.PAUSE_S = 0.0
time.sleep = lambda s: None
if MUTATE:
    Q1.SYNC_CAP = 10 ** 9


def run(argv_chunks, td, cap_chunk=None):
    Q.EXTRACT = Path(td) / "extract"; Q.EXTRACT.mkdir(exist_ok=True)
    for k in TESTED:
        if not (Q.EXTRACT / f"chunk_{k:02d}.fits").exists():
            FROZEN[k].write(Q.EXTRACT / f"chunk_{k:02d}.fits", format="fits", overwrite=True)
    Q.VAR = Path(td) / "variant"; Q.MAN = Path(td) / "manifest.json"
    if cap_chunk is not None:
        Q.CAP_CHUNK = cap_chunk
    sys.argv = ["q3_delta_chunks.py", "--owner-go-recorded", "--chunks", argv_chunks]
    try:
        Q.main()
        return None
    except SystemExit as e:
        return str(e)


with tempfile.TemporaryDirectory() as td:
    STAT.update(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0)
    err = run("2,11", td, cap_chunk=50_000_000)                     # the mock's artificial 3,000-row cluster needs more than the production 2 MB per-chunk cap
    P(f"first run ended with: {err}" if err else "first run completed")
    man = json.loads(Q.MAN.read_text()) if Q.MAN.exists() else {"chunks": {}}
    n_trunc, n_hit, n_hang, calls1 = STAT["truncated"], STAT["flaky_hit"], STAT["hang_hit"], STAT["calls"]
    ok_all = True
    res = {}
    for k in TESTED:
        f = Q.VAR / f"chunk_{k:02d}.fits"
        if not f.exists():
            ok_all = False; res[k] = None; continue
        U = Table.read(f, format="fits"); FZ = Table.read(Q.EXTRACT / f"chunk_{k:02d}.fits", format="fits")
        got = set(np.asarray(U["source_id"], np.int64).tolist())
        res[k] = (U, FZ, got)
    P(f"fetch: {calls1} queries, {n_trunc} truncated by the endpoint")
    if MUTATE:
        t1 = all(res[k] is not None and res[k][2] == expected[k] for k in TESTED)
        P("T1 each union equals the rows the approved query would return in that chunk: " + ("PASS" if t1 else "FAIL"))
        P("MUTATE: truncation detection disabled; T1 must FAIL for the test to be able to catch a missing split: " + ("OK (T1 failed as required)" if not t1 else "PROBLEM: T1 passed with detection disabled"))
        ok = not t1
    else:
        for k in TESTED:
            U, FZ, got = res[k]
            C(f"T1 chunk {k}: the union equals the rows the approved query would return (missing {len(expected[k] - got)}, spurious {len(got - expected[k])})", got == expected[k])
            nf = len(FZ)
            same_head = all(np.array_equal(np.asarray(U[c][:nf]), np.asarray(FZ[c]), equal_nan=(np.asarray(FZ[c]).dtype.kind == "f")) for c in FZ.colnames)
            tail_noG = bool(np.all(np.isnan(np.asarray(U["phot_g_mean_mag"][nf:], float))))
            C(f"T3 chunk {k}: the union starts with the {nf:,d} frozen rows unchanged and its {len(U) - nf:,d} appended rows all lack G", same_head and tail_noG and len(U) - nf == int((passes & ~has_g & span[k]).sum()))
            C(f"T4 chunk {k}: column names, order and dtypes equal the frozen file's", U.colnames == FZ.colnames and all(U[c].dtype == FZ[c].dtype for c in FZ.colnames))
        C(f"T2 the truncation path was exercised ({n_trunc} truncated results; the manifests count {sum(v['truncated_results_discarded'] for v in man['chunks'].values())} discarded)",
          n_trunc > 0 and sum(v["truncated_results_discarded"] for v in man["chunks"].values()) == n_trunc)
        C(f"T6 the dropped connection was retried (hit {n_hit}, run completed)", n_hit == 1 and err is None)
        C(f"T7 the hung query was cut by the client timeout and retried (hangs {n_hang}, run completed)", n_hang == 1 and err is None)
        # T8: a second run over the same directory skips the finished chunks
        STAT["calls"] = 0
        err2 = run("2,11", td, cap_chunk=50_000_000)
        C(f"T8 a second run skips the finished chunks (queries {STAT['calls']}, ended with {err2})", STAT["calls"] == 0 and err2 is None)
    if not MUTATE:
        with tempfile.TemporaryDirectory() as td2:
            STAT.update(calls=0, flaky_done=True, hang_done=True)
            err3 = run("11", td2, cap_chunk=30_000)
            done11 = (Q.VAR / "chunk_11.fits").exists()
            C(f"T5 the per-chunk byte cap stops the run and writes nothing for the chunk ({err3[:60] if err3 else None}; output present: {done11})", err3 is not None and "STOPPED" in err3 and not done11)
        ok = all(CHK)
P("RESULT: " + ("all checks behave as required" if ok else "CHECK FAILED"))
(HERE / ("test_q3_delta_chunks" + ("_MUTATE" if MUTATE else "") + ".out")).write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
