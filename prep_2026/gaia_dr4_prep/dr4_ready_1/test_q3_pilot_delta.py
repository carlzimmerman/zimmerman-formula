#!/usr/bin/env python3
"""DR4-READY-1: OFFLINE test of q3_pilot_delta.py against a synthetic archive that mimics the synchronous endpoint (NEW file; NO NETWORK, socket guard).

The fake archive is a synthetic gaia_source-like table (400k rows, the frozen column list and dtypes) in which the frozen WHERE's conditions each remove some rows and a random 0.03 %
of the rows plus a dense cluster of 3,500 rows have no G magnitude.  It answers the script's literal source_id-piece queries by APPLYING the query's own conditions, SILENTLY TRUNCATES
any result to 2000 rows, raises once (a dropped connection) and hangs once (a stalled query, cut by the client's 1 s alarm).  The 'frozen chunk 0' is built from the same table
(the rows that pass the frozen WHERE with a G magnitude, shuffled).  Checks (PASS/FAIL):
  T1 the assembled union is exactly the rows that pass the frozen WHERE WITHOUT the G condition (what the approved query would return); T2 the truncation path was exercised;
  T3 the union starts with the frozen rows unchanged and the delta rows all lack G; T4 the union's column names and dtypes equal the frozen file's; T5 the byte cap stops the run and
  writes the reason; T6 the dropped connection was retried; T7 the hung query was cut by the alarm and retried.
MUTATE control (--mutate, outputs named *_MUTATE): the script's truncation detection is disabled (SYNC_CAP -> 10**9) while the fake still truncates: T1 must FAIL.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_q3_pilot_delta.py [--mutate]
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
import q3_pilot_delta as Q
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


rng = np.random.default_rng(3305)
FE = Q.FE
N = 400_000
sid = rng.integers(0, FE.LEVEL0, N)
ra = rng.random(N) * 360; dec = np.degrees(np.arcsin(rng.uniform(-1, 1, N)))
par = np.where(rng.random(N) < 0.55, rng.uniform(3.6, 12, N), rng.uniform(0.05, 3.4, N))
pe = np.where(rng.random(N) < 0.01, rng.uniform(2, 3, N), rng.uniform(0.01, 0.6, N)).astype(np.float32)
g = rng.uniform(8, 20, N).astype(np.float32)
g[rng.random(N) < 0.0003] = np.nan
# a dense cluster of G-less rows (3,500) inside one source_id neighbourhood, all passing the other conditions, to force splits
c0 = int(0.37 * FE.LEVEL0)
K = 3500
ra_c = rng.random(K) * 360; dec_c = np.degrees(np.arcsin(rng.uniform(-0.7, 0.7, K)))             # |dec| < 44.4 deg; |b| filtered below by the same rule as the rest
sid = np.concatenate([sid, c0 + rng.integers(0, 2 ** 42, K)])
ra = np.concatenate([ra, ra_c]); dec = np.concatenate([dec, dec_c])
par = np.concatenate([par, rng.uniform(3.6, 12, K)]); pe = np.concatenate([pe, rng.uniform(0.01, 0.6, K).astype(np.float32)])
g = np.concatenate([g, np.full(K, np.nan, np.float32)])
n = len(sid)
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
assert list(tab) == [c.strip() for c in FE.COLS.split(",")], "the synthetic table must follow the frozen column list"
CAT = Table(tab)
passes = (par > 3.5) & (par / pe > 5) & (pe < 2) & (np.abs(b) > 10) & (sid >= 0) & (sid < FE.LEVEL0)
has_g = ~np.isnan(g)
expected = set(sid[passes].tolist())                                                     # the approved query's rows
frozen_idx = np.flatnonzero(passes & has_g)
rng.shuffle(frozen_idx)
FROZEN = CAT[frozen_idx]
P(f"synthetic archive: {n:,d} rows; rows passing the frozen WHERE without the G condition {int(passes.sum()):,d}; with a G magnitude (the 'frozen chunk 0') {len(frozen_idx):,d}; "
  f"without G (the delta the script must fetch) {int((passes & ~has_g).sum()):,d}")
# ---- the fake synchronous endpoint ------------------------------------------------------------------------------------------------------------------------------------
STAT = dict(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0)
TRUE_CAP = 2000
NEEDED = ("parallax > 3.5", "parallax_over_error > 5", "parallax_error < 2", "phot_g_mean_mag IS NULL", "ABS(b) > 10")


def fake_launch(q, path):
    STAT["calls"] += 1
    if STAT["calls"] == 4 and not STAT["flaky_done"]:
        STAT["flaky_done"] = True; STAT["flaky_hit"] += 1
        raise ConnectionError("simulated dropped connection")
    if STAT["calls"] == 7 and not STAT["hang_done"]:
        STAT["hang_done"] = True; STAT["hang_hit"] += 1
        t_end = time.time() + 4.0
        while time.time() < t_end:
            pass
    assert all(s in q for s in NEEDED) and "IS NOT NULL" not in q, "the query does not carry the expected delta conditions"
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


def run_once():
    with tempfile.TemporaryDirectory() as td:
        Q.PRIMARY = Path(td) / "frozen_chunk_00.fits"; FROZEN.write(Q.PRIMARY, format="fits", overwrite=True)
        Q.VAR = Path(td) / "variant"; Q.MAN = Path(td) / "manifest.json"
        STAT.update(calls=0, truncated=0, flaky_done=False, flaky_hit=0, hang_done=False, hang_hit=0)
        sys.argv = ["q3_pilot_delta.py", "--owner-go-recorded"]
        try:
            Q.main()
            U = Table.read(Q.VAR / "chunk_00.fits", format="fits")
            man = json.loads(Q.MAN.read_text())
            FZ = Table.read(Q.PRIMARY, format="fits")
            return U, FZ, man, None
        except SystemExit as e:
            man = json.loads(Q.MAN.read_text()) if Q.MAN.exists() else {}
            return None, None, man, str(e)


U, FZ, man, err = run_once()
P(f"main run ended with: {err}" if err else "main run completed")
got = set(np.asarray(U["source_id"], np.int64).tolist()) if U is not None else set()
n_trunc, n_hit, n_hang = STAT["truncated"], STAT["flaky_hit"], STAT["hang_hit"]
P(f"fetch: {STAT['calls']} queries, {n_trunc} truncated by the endpoint; union rows {len(got):,d}")
t1 = got == expected
if MUTATE:
    P(f"T1 the union equals the rows the approved query would return (missing {len(expected - got)}, spurious {len(got - expected)}): {'PASS' if t1 else 'FAIL'}")
    P("MUTATE: truncation detection disabled; T1 must FAIL for the test to be able to catch a missing split: " + ("OK (T1 failed as required)" if not t1 else "PROBLEM: T1 passed with detection disabled"))
    ok = not t1
else:
    C(f"T1 the union equals the rows the approved query would return (missing {len(expected - got)}, spurious {len(got - expected)})", t1)
    C(f"T2 the truncation path was exercised ({n_trunc} truncated results; manifest counts {man.get('truncated_results_discarded')} discarded)", n_trunc > 0 and man.get("truncated_results_discarded") == n_trunc)
    nf = len(FZ)
    same_head = all(np.array_equal(np.asarray(U[c][:nf]), np.asarray(FZ[c]), equal_nan=(np.asarray(FZ[c]).dtype.kind == "f")) for c in FZ.colnames)
    tail_noG = bool(np.all(np.isnan(np.asarray(U["phot_g_mean_mag"][nf:], float))))
    C(f"T3 the union starts with the {nf:,d} frozen rows unchanged and its {len(U) - nf:,d} appended rows all lack G", same_head and tail_noG and len(U) - nf == int((passes & ~has_g).sum()))
    C("T4 the union's column names, order and dtypes equal the frozen file's", U.colnames == FZ.colnames and all(U[c].dtype == FZ[c].dtype for c in FZ.colnames))
    C(f"T6 the dropped connection was retried (hit {n_hit}, run completed)", n_hit == 1 and U is not None)
    C(f"T7 the hung query was cut by the client timeout and retried (hangs {n_hang}, run completed)", n_hang == 1 and U is not None)
    Q.CAP_BYTES = 30_000
    U2, FZ2, man2, err2 = run_once()
    C(f"T5 the byte cap stops the run and writes the reason ({err2[:70] if err2 else None})", err2 and "STOPPED" in err2 and "stopped" in man2)
    ok = all(CHK)
P("RESULT: " + ("all checks behave as required" if ok else "CHECK FAILED"))
(HERE / ("test_q3_pilot_delta" + ("_MUTATE" if MUTATE else "") + ".out")).write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
