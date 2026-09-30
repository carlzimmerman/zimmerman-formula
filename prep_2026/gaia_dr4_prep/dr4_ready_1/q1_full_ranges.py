#!/usr/bin/env python3
"""DR4-READY-1: FULL-SIZE Q1 (the 30 kAU / d neighbour cones around ALL final DR3 pairs) fetched as synchronous index-friendly source_id RANGE queries (NEW file; networked; needs --owner-go-recorded).

The pilot (q1_pilot_ranges.py: 500 pairs, 207 queries, 1,048 s, 9.19 MB kept, 4 truncated results discarded, every local-extract source in the cones present) showed the form works on the
real archive; the owner gave the go for the full-size run in the calculation chat on 2026-09-30 (about 120-140 MB kept, about 2,600 queries, hard caps 200 MB kept and 260 MB received).
Everything about the query form, the 2000-row truncation handling (a result of exactly 2000 rows is discarded and its batch halved, a single range is split at its midpoint), the 120 s timeout
with retries and the exact-cone re-filter is reused from q1_pilot_ranges.py.  New here: (1) ALL final pairs of wide_binaries_dr3.csv (pair_id = the pair's index in that file, as in the pilot);
(2) a RESUME: every accepted batch is written to q1_full_cache/ and logged in index.jsonl, so a crash, a sleep or a stop at a cap continues where it left off (a run whose plan differs from the
cache's is refused); (3) a total cap of 200 MB of accepted bytes and 260 MB received, at most 9000 queries.  The local completeness check (every stage-A source inside the exact cones must be
in the output) is repeated at full size.  Output: q1_full_neighbours.fits in the gitignored dr4_ready_1 data directory; manifest manifest_q1_full.json here.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_full_ranges.py --owner-go-recorded [--plan-only]      (for long runs: caffeinate -i python3 ...)
"""
import sys
sys.dont_write_bytecode = True
import argparse, csv, hashlib, json, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
sys.path.insert(0, str(HERE))
import cut13_allsource as W1
import q1_pilot_ranges as Q1

WB = Q1.WB
OUT = Q1.IN_DIR
CACHE = OUT / "q1_full_cache"
MAN = HERE / "manifest_q1_full.json"
CAP_ACCEPTED_BYTES, CAP_TRANSFER_BYTES, MAX_QUERIES = 200_000_000, 260_000_000, 9000
PAUSE_S = 0.5


def plan_full(max_pairs=None):
    import healpy as hp
    S = np.load(WB / "dr3_extract" / "stage_A.npz")
    A = {k: S[k] for k in ("source_id", "ra", "dec", "parallax")}
    rows = list(csv.DictReader(open(WB / "dr3_extract" / "wide_binaries_dr3.csv")))
    sa = np.array([int(r["source_id1"]) for r in rows], np.int64); sb = np.array([int(r["source_id2"]) for r in rows], np.int64)
    if max_pairs:
        sa, sb = sa[:max_pairs], sb[:max_pairs]
    order = np.argsort(A["source_id"])
    row = lambda s: order[np.searchsorted(A["source_id"][order], s)]
    ia, ib = row(sa), row(sb)
    assert np.all(A["source_id"][ia] == sa) and np.all(A["source_id"][ib] == sb)
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


def plan_hash(P):
    h = hashlib.sha256()
    h.update(json.dumps([Q1.LEVEL, Q1.MARGIN_ARCSEC, len(P["pick"]), P["rng"][:50], P["rng"][-50:], len(P["rng"])]).encode())
    return h.hexdigest()[:16]


def fetch_all_full(P, man, cache):
    from astropy.table import Table, vstack
    cache.mkdir(parents=True, exist_ok=True)
    idx_path, state_path = cache / "index.jsonl", cache / "state.json"
    ph = plan_hash(P)
    if state_path.exists():
        assert json.loads(state_path.read_text())["plan_hash"] == ph, "the cache belongs to a different plan: refusing to resume (move or delete the cache directory)"
    else:
        state_path.write_text(json.dumps({"plan_hash": ph}))
    cols = ", ".join(Q1.KEEP)
    done, files = set(), []
    st = dict(calls=0, truncated=0, rows=0, accepted_bytes=0, received_bytes=0, seq=0, resumed_batches=0, t0=time.time())
    if idx_path.exists():
        for line in idx_path.read_text().splitlines():
            rec = json.loads(line)
            st["calls"] += 1
            if rec["type"] == "batch":
                done.update((lo, hi) for lo, hi in rec["ranges"])
                st["rows"] += rec["rows"]; st["accepted_bytes"] += rec["bytes"]; st["received_bytes"] += rec["bytes"]
                st["seq"] = max(st["seq"], rec["seq"] + 1); st["resumed_batches"] += 1; files.append(cache / rec["file"])
            else:
                st["received_bytes"] += rec["bytes"]; st["truncated"] += 1
    if st["resumed_batches"]:
        print(f"RESUME: {st['resumed_batches']} batches already in the cache ({len(done)} ranges, {st['rows']:,d} rows, {st['accepted_bytes'] / 1e6:.1f} MB)", flush=True)
    rng = [r for r in P["rng"] if r not in done]
    n_total = len(P["rng"])
    i, n = 0, 30

    def log(rec):
        with open(idx_path, "a") as f:
            f.write(json.dumps(rec) + "\n")

    def stop(why):
        man["stopped"] = why
        MAN.write_text(json.dumps(man, indent=1) + "\n")
        raise SystemExit("STOPPED: " + why + " -- the cache keeps every accepted batch; report to the owner before continuing")

    while i < len(rng):
        batch = rng[i:i + n]
        where = " OR ".join(f"(source_id >= {lo} AND source_id < {hi})" for lo, hi in batch)
        T, nb = Q1.run_query(f"SELECT {cols} FROM gaiadr3.gaia_source WHERE {where}", OUT / "q1_full_tmp.fits")
        st["calls"] += 1
        st["received_bytes"] += nb
        if st["received_bytes"] > CAP_TRANSFER_BYTES:
            stop(f"received {st['received_bytes'] / 1e6:.2f} MB in {st['calls']} queries against the {CAP_TRANSFER_BYTES / 1e6:.0f} MB transfer cap")
        if st["calls"] > MAX_QUERIES:
            stop(f"more than {MAX_QUERIES} queries")
        if len(T) >= Q1.SYNC_CAP:                                   # truncated by the synchronous cap: discard, never use
            st["truncated"] += 1
            log(dict(type="trunc", bytes=nb))
            if len(batch) > 1:
                n = max(1, len(batch) // 2)
            else:
                lo, hi = batch[0]
                if hi - lo < 2:
                    raise RuntimeError("a one-integer source_id range hit the 2000-row cap")
                rng[i:i + 1] = [(lo, (lo + hi) // 2), ((lo + hi) // 2, hi)]
            continue
        fn = f"b{st['seq']:06d}.fits"
        T.write(cache / fn, format="fits", overwrite=True)
        log(dict(type="batch", seq=st["seq"], file=fn, rows=int(len(T)), bytes=int(nb), ranges=[list(r) for r in batch]))
        files.append(cache / fn)
        st["seq"] += 1
        st["rows"] += len(T)
        st["accepted_bytes"] += nb
        if st["accepted_bytes"] > CAP_ACCEPTED_BYTES:
            stop(f"accepted {st['accepted_bytes'] / 1e6:.2f} MB ({st['rows']:,d} rows) after {st['calls']} queries against the {CAP_ACCEPTED_BYTES / 1e6:.0f} MB cap")
        i += len(batch)
        frac = (n_total - (len(rng) - i)) / n_total
        proj = st["accepted_bytes"] / max(frac, 1e-9)
        if frac >= 0.2 and proj > 1.25 * CAP_ACCEPTED_BYTES:
            stop(f"projected {proj / 1e6:.1f} MB accepted against the {CAP_ACCEPTED_BYTES / 1e6:.0f} MB cap after {100 * frac:.0f}% of the ranges")
        n = int(np.clip(Q1.TARGET_ROWS / max(len(T) / len(batch), 0.5), 4, min(250, 2 * len(batch))))
        if st["calls"] % 25 == 0:
            print(f"  {100 * frac:5.1f}% of the ranges: {st['calls']} queries, {st['truncated']} truncated, {st['rows']:,d} rows, accepted {st['accepted_bytes'] / 1e6:.1f} MB, "
                  f"received {st['received_bytes'] / 1e6:.1f} MB, {time.time() - st['t0']:.0f} s this session", flush=True)
        time.sleep(PAUSE_S)
    st["seconds_this_session"] = round(time.time() - st["t0"], 1)
    parts = [Table.read(f, format="fits") for f in files]
    return vstack(parts), st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-go-recorded", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--max-pairs", type=int, default=None, help="for offline tests only")
    a = ap.parse_args()
    P = plan_full(a.max_pairs)
    print(f"plan: {len(P['pick'])} pairs; {P['n_pix']} level-{Q1.LEVEL} pixels, {len(P['rng'])} source_id ranges; {P['area']:.1f} deg2; "
          f"pilot density 9.8k rows/deg2 -> about {P['area'] * 9.8e3 / 1e6:.2f} million unique rows, about {P['area'] * 9.8e3 * 72 / 1e6:.0f} MB kept (caps {CAP_ACCEPTED_BYTES / 1e6:.0f} / {CAP_TRANSFER_BYTES / 1e6:.0f} MB)", flush=True)
    loc = Q1.local_in_cones(P)
    tot, miss = Q1.plan_coverage(P, loc)
    print(f"coverage: {tot} local-extract sources inside the exact cones; {miss} have a source_id outside every planned range", flush=True)
    assert miss == 0, "the planned source_id ranges miss local-extract sources: widen the margin before any query"
    if a.plan_only:
        return
    if not a.owner_go_recorded:
        raise SystemExit("refused: pass --owner-go-recorded (the owner's go for the full-size Q1)")
    from scipy.spatial import cKDTree
    man = {"approval": "owner's go for the full-size Q1 (all final DR3 pairs, about 120-140 MB, about 2,600 synchronous source_id-range queries, hard caps 200 MB kept / 260 MB received), given in the "
                       "calculation chat 2026-09-30", "level": Q1.LEVEL, "margin_arcsec": Q1.MARGIN_ARCSEC, "sync_cap_rows": Q1.SYNC_CAP, "target_rows_per_query": Q1.TARGET_ROWS,
           "cap_accepted_bytes": CAP_ACCEPTED_BYTES, "cap_transfer_bytes": CAP_TRANSFER_BYTES, "n_pairs": int(len(P["pick"])), "n_ranges": len(P["rng"]), "plan_hash": plan_hash(P)}
    T, st = fetch_all_full(P, man, CACHE)
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
    out = OUT / "q1_full_neighbours.fits"
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
