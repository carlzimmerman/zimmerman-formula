#!/usr/bin/env python3
"""DR4-READY-1: the DR3 DELTA Q1 -- the 30 kAU / d neighbour cones around the cut-13 CANDIDATE pairs that are NOT final pairs (DR3: 4,021 of the 10,231 that reach cut 13), fetched with the SAME query form as the full-size Q1
(NEW file; networked; needs --owner-go-recorded "<where and when the owner said yes>").

Why.  The builder applies cut 13 to every pair that passes the other cuts before the vtilde-error Monte Carlo, and the driver's cones path refuses to treat a pair without a cone as 'no third star' (ConeCoverageError: 4,021 of 10,231
pairs uncovered with the final-pair cones only).  q1_delta_pairs_dr3.py writes the 4,021 pairs (from the driver's own dump of the pairs that reach cut 13) as q1_delta_pairs.csv; this script fetches their cones.
The QUERY FORM is unchanged from the approved full-size Q1 (q1_full_ranges.py, run on 2026-09-30: 3,122 queries, 135 MB accepted): SYNCHRONOUS literal `source_id >= lo AND source_id < hi` ranges (a level-12 HEALPix pixel is a contiguous source_id
range, so the primary-key index is used), the same ten columns of gaiadr3.gaia_source, a result of exactly 2,000 rows (the synchronous cap) is discarded and its batch halved, a 120 s timeout with retries, a 0.5 s pause between queries, a
RESUME cache.  Only the set of ranges differs: every level-12 pixel overlapping either component's 30 kAU / d cone (R = 30 x parallax_primary arcsec, plus a 30 arcsec margin) of the delta pairs.  The fetch loop is the full-size Q1's own
(q1_full_ranges.fetch_all_full, imported; its module constants are pointed at the delta caps, manifest and temporary file for the duration of the run and restored afterwards); the pixels the full-size Q1 already holds are NOT subtracted
(0.5 % of the delta pixels), so the delta file is self-contained.  The result is a superset of the exact cones, re-filtered LOCALLY to the exact cones and written in the original schema (pair_id = the row index in q1_delta_pairs.csv, comp 0 = source_id1,
comp 1 = source_id2, the ten columns) to q1_delta_neighbours.fits in the gitignored data directory; the manifest is manifest_q1_delta.json here.  The local completeness check (every stage-A source inside the exact cones must be in the output)
is repeated.
Guards.  HARD CAPS 100 MB of accepted result bytes, 130 MB received (truncated results included), 4,000 queries (the plan: about 70 MB, about 1,600 queries, about 2 h); it stops, writes the reason into the manifest and keeps the cache if one
would be passed; needs --owner-go-recorded with a non-empty text (recorded in the manifest); --plan-only is offline; the pairs file must match the sha256 recorded by q1_delta_pairs_dr3.py.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_delta_ranges.py --plan-only
     caffeinate -i python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_delta_ranges.py --owner-go-recorded "<text>"      (resumable: run it again after a stop or a crash)
"""
import sys
sys.dont_write_bytecode = True
import argparse, csv, hashlib, json, shutil, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import cut13_allsource as W1
import q1_pilot_ranges as Q1
import q1_full_ranges as QF

WB = Q1.WB
OUT = Q1.IN_DIR
PAIRS_CSV = OUT / "q1_delta_pairs.csv"
CACHE = OUT / "q1_delta_cache"
MAN = HERE / "manifest_q1_delta.json"
PAIRS_JSON = HERE / "q1_delta_pairs_dr3.json"
CAP_ACCEPTED_BYTES, CAP_TRANSFER_BYTES, MAX_QUERIES = 100_000_000, 130_000_000, 4000
PAUSE_S = 0.5


def read_pairs(path, max_pairs=None):
    rows = list(csv.DictReader(open(path)))
    sa = np.array([int(r["source_id1"]) for r in rows], np.int64); sb = np.array([int(r["source_id2"]) for r in rows], np.int64)
    return (sa[:max_pairs], sb[:max_pairs]) if max_pairs else (sa, sb)


def plan_delta(pairs_csv, max_pairs=None):
    """the same plan as q1_full_ranges.plan_full, for the pairs of `pairs_csv` (pair_id = the row index)."""
    import healpy as hp
    S = np.load(WB / "dr3_extract" / "stage_A.npz")
    A = {k: S[k] for k in ("source_id", "ra", "dec", "parallax")}
    sa, sb = read_pairs(pairs_csv, max_pairs)
    order = np.argsort(A["source_id"])
    row = lambda s: order[np.searchsorted(A["source_id"][order], s)]
    ia, ib = row(sa), row(sb)
    assert np.all(A["source_id"][ia] == sa) and np.all(A["source_id"][ib] == sb), "a pair of the delta list is not in stage A"
    va, vb = Q1.vec(A["ra"][ia], A["dec"][ia]), Q1.vec(A["ra"][ib], A["dec"][ib])
    R = W1.radius_arcsec(A["parallax"][ia])
    pix = set()
    for k in range(len(R)):
        for v in (va[k], vb[k]):
            pix.update(hp.query_disc(2 ** Q1.LEVEL, v, np.radians((R[k] + Q1.MARGIN_ARCSEC) / 3600), inclusive=True, nest=True).tolist())
    pix = np.array(sorted(pix), np.int64)
    brk = np.flatnonzero(np.diff(pix) != 1)
    st = np.concatenate([[0], brk + 1]); en = np.concatenate([brk, [len(pix) - 1]])
    rng = [(int(pix[a] * Q1.DIV), int((pix[b] + 1) * Q1.DIV)) for a, b in zip(st, en)]
    area = len(pix) * hp.nside2pixarea(2 ** Q1.LEVEL, degrees=True)
    return dict(A=A, va=va, vb=vb, R=R, pick=np.arange(len(R)), rng=rng, n_pix=int(len(pix)), area=float(area))


class _PointFullQ1AtDelta:
    """for the duration of the run, point q1_full_ranges' module constants (caps, manifest, temporary file, pause) at the DELTA values; restored on exit."""
    NAMES = ("CAP_ACCEPTED_BYTES", "CAP_TRANSFER_BYTES", "MAX_QUERIES", "MAN", "OUT", "PAUSE_S")

    def __enter__(self):
        self.old = {k: getattr(QF, k) for k in self.NAMES}
        QF.CAP_ACCEPTED_BYTES, QF.CAP_TRANSFER_BYTES, QF.MAX_QUERIES = CAP_ACCEPTED_BYTES, CAP_TRANSFER_BYTES, MAX_QUERIES
        QF.MAN, QF.OUT, QF.PAUSE_S = MAN, OUT, PAUSE_S
        return self

    def __exit__(self, *exc):
        for k, v in self.old.items():
            setattr(QF, k, v)
        return False


def estimate(P):
    """size / queries / time from the full-size Q1's own manifest (rows per level-12 pixel of its union)."""
    mf = json.load(open(HERE / "manifest_q1_full.json")); pl = json.load(open(HERE / "q1_delta_plan_dr3.json"))
    rows_per_pix = mf["rows_raw_unique"] / pl["pixels"]["final"]
    rows = P["n_pix"] * rows_per_pix
    return dict(rows=rows, mb=rows * mf["accepted_bytes"] / mf["rows_raw_unique"] / 1e6, queries=rows * mf["queries_total"] / mf["rows_raw_unique"],
                hours=rows * mf["seconds_this_session"] / mf["rows_raw_unique"] / 3600)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-go-recorded", type=str, default="", help="where and when the owner said yes (recorded in the manifest); required for any query")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--max-pairs", type=int, default=None, help="for offline tests only")
    a = ap.parse_args()
    if not a.max_pairs and PAIRS_JSON.exists():
        want = json.loads(PAIRS_JSON.read_text())["sha256"]
        have = hashlib.sha256(open(PAIRS_CSV, "rb").read()).hexdigest()
        assert have == want, f"q1_delta_pairs.csv ({have[:16]}) is not the file q1_delta_pairs_dr3.json recorded ({want[:16]}): rerun q1_delta_pairs_dr3.py"
    P = plan_delta(PAIRS_CSV, a.max_pairs)
    est = estimate(P)
    print(f"plan: {len(P['pick'])} delta pairs; {P['n_pix']} level-{Q1.LEVEL} pixels, {len(P['rng'])} source_id ranges; {P['area']:.1f} deg2; ESTIMATE from the full-size Q1's own densities: about {est['rows'] / 1e3:.0f}k raw rows, "
          f"{est['mb']:.0f} MB accepted, {est['queries']:.0f} queries, {est['hours']:.1f} h (hard caps {CAP_ACCEPTED_BYTES / 1e6:.0f} MB accepted / {CAP_TRANSFER_BYTES / 1e6:.0f} MB received / {MAX_QUERIES} queries)", flush=True)
    loc = Q1.local_in_cones(P)
    tot, miss = Q1.plan_coverage(P, loc)
    print(f"coverage: {tot} local-extract sources inside the exact cones; {miss} have a source_id outside every planned range", flush=True)
    assert miss == 0, "the planned source_id ranges miss local-extract sources: widen the margin before any query"
    if a.plan_only:
        return
    if not a.owner_go_recorded.strip():
        raise SystemExit("refused: pass --owner-go-recorded \"<where and when the owner said yes to this download>\" (nothing is fetched without it)")
    free = shutil.disk_usage(OUT).free
    assert free > 2_000_000_000, f"only {free / 1e9:.1f} GB free"
    from scipy.spatial import cKDTree
    man = {"approval": a.owner_go_recorded.strip(), "what": "DR3 delta Q1: the 30 kAU / d neighbour cones of the cut-13 candidate pairs that are not final pairs; the SAME query form as the full-size Q1 (synchronous literal source_id ranges)",
           "level": Q1.LEVEL, "margin_arcsec": Q1.MARGIN_ARCSEC, "sync_cap_rows": Q1.SYNC_CAP, "target_rows_per_query": Q1.TARGET_ROWS, "cap_accepted_bytes": CAP_ACCEPTED_BYTES,
           "cap_transfer_bytes": CAP_TRANSFER_BYTES, "max_queries": MAX_QUERIES, "n_pairs": int(len(P["pick"])), "n_ranges": len(P["rng"]), "n_pixels": P["n_pix"], "plan_hash": QF.plan_hash(P),
           "pairs_csv_sha256": hashlib.sha256(open(PAIRS_CSV, "rb").read()).hexdigest(), "estimate": est}
    with _PointFullQ1AtDelta():
        T, st = QF.fetch_all_full(P, man, CACHE)
    _, first = np.unique(np.asarray(T["source_id"], np.int64), return_index=True)
    T = T[np.sort(first)]
    tree = cKDTree(Q1.vec(np.asarray(T["ra"], float), np.asarray(T["dec"], float)))
    rows, pid, cmp = [], [], []
    for k in range(len(P["pick"])):
        chord = 2 * np.sin(np.radians(P["R"][k] / 3600) / 2)
        for c, vc in ((0, P["va"][k]), (1, P["vb"][k])):
            js = tree.query_ball_point(vc, r=chord)
            rows.extend(js); pid.extend([int(P["pick"][k])] * len(js)); cmp.extend([c] * len(js))
    E = T[np.array(rows, int)]
    E["pair_id"] = np.array(pid, np.int64)
    E["comp"] = np.array(cmp, np.int64)
    E = E["pair_id", "comp", *Q1.KEEP]
    have = set(zip(np.asarray(E["pair_id"], np.int64).tolist(), np.asarray(E["comp"], np.int64).tolist(), np.asarray(E["source_id"], np.int64).tolist()))
    lost = sum(1 for x in loc if x not in have)
    out = OUT / "q1_delta_neighbours.fits"
    E.write(out, format="fits", overwrite=True)
    man.update(rows_raw_unique=int(len(T)), rows_exact=int(len(E)), file=str(out.relative_to(REPO)) if REPO in out.parents else out.name,
               sha256=hashlib.sha256(open(out, "rb").read()).hexdigest(), bytes=out.stat().st_size, queries_total=st["calls"], truncated_results_discarded=st["truncated"],
               accepted_bytes=st["accepted_bytes"], received_bytes=st["received_bytes"], batches_resumed_from_cache=st["resumed_batches"], seconds_this_session=st["seconds_this_session"],
               local_extract_sources_in_cones=tot, local_extract_sources_missing_from_fetch=lost)
    MAN.write_text(json.dumps(man, indent=1) + "\n")
    print(f"exact two-cone rows {len(E):,d} from {len(T):,d} unique raw rows; {st['calls']} queries ({st['truncated']} truncated results discarded), accepted {st['accepted_bytes'] / 1e6:.1f} MB, "
          f"received {st['received_bytes'] / 1e6:.1f} MB; local-extract sources in the cones missing from the fetch: {lost} of {tot}; wrote {out.name}, manifest {MAN.name}", flush=True)
    if lost:
        print("WARNING: the fetch is missing local-extract sources; do not use it", flush=True)


if __name__ == "__main__":
    main()
