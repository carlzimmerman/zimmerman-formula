#!/usr/bin/env python3
"""DR4-READY-1: FULL-SIZE Q3 in its delta form, chunks 1-11 (NEW file; networked; needs --owner-go-recorded).

The pilot (q3_pilot_delta.py, chunk 0) showed that the approved Q3 (the frozen extract query WITHOUT 'AND phot_g_mean_mag IS NOT NULL') equals the frozen chunk already on disk
plus the rows that satisfy the same WHERE but have NO G magnitude (216 rows in chunk 0, 0.47 MB received, 34 synchronous queries, no truncation).  This tool does the same for the
other eleven level-0 source_id spans [k x 2^35 x 4^12, (k + 1) x ...):
    SELECT <frozen COLS> FROM gaiadr3.gaia_source WHERE parallax > 3.5 AND parallax_over_error > 5 AND parallax_error < 2 AND phot_g_mean_mag IS NULL AND ABS(b) > 10
           AND source_id >= lo AND source_id < hi
over adaptive source_id pieces (the same synchronous-endpoint handling as the pilot: a result of exactly 2000 rows is truncated, discarded and its piece halved; 120 s timeout with retries).
Per chunk the delta is validated locally against the WHERE, checked disjoint from the frozen chunk's rows, and the union (frozen rows first, then the delta, in the frozen column order and
dtypes) is written to the gitignored dr3_extract_allsource_15c/chunk_kk.fits with the small delta alone as q3_delta_no_G_chunk_kk.fits.  A chunk whose outputs and manifest entry exist is
skipped (a resume).  Guards: needs --owner-go-recorded; --plan-only is offline; refuses if the frozen WHERE changed; caps 2 MB received per chunk and 15 MB in total; at most 2500 queries per chunk.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q3_delta_chunks.py --owner-go-recorded [--chunks 1-11] [--plan-only]
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
sys.path.insert(0, str(PREP / "catalog_builder"))
sys.path.insert(0, str(HERE))
import fetch_extract as FE                                       # read-only: COLS, WHERE, LEVEL0
import q1_pilot_ranges as Q1                                     # run_query (timeout + retries), SYNC_CAP
import q3_pilot_delta as Q3                                      # where_null(), constants of the pilot

WB = REPO / "real_research" / "data" / "widebinaries"
EXTRACT = WB / "dr3_extract"
VAR = WB / "dr3_extract_allsource_15c"
MAN = HERE / "manifest_q3_delta_chunks.json"
CAP_CHUNK, CAP_TOTAL, MAX_QUERIES = 2_000_000, 15_000_000, 2500
PAUSE_S = 0.5
W0, MAX_W, MIN_W = FE.LEVEL0 // 128, FE.LEVEL0 // 16, 2 ** 39


def parse_chunks(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    assert all(0 <= k <= 11 for k in out), "chunks are 0-11"
    return sorted(set(out))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def validate_delta(D, k):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    g = np.asarray(D["phot_g_mean_mag"], float)
    par, pe = np.asarray(D["parallax"], float), np.asarray(D["parallax_error"], float)
    b = SkyCoord(np.asarray(D["ra"], float) * u.deg, np.asarray(D["dec"], float) * u.deg, frame="icrs").galactic.b.deg
    sid = np.asarray(D["source_id"], np.int64)
    return dict(has_G=int((~np.isnan(g)).sum()), parallax_le_3p5=int((par <= 3.5).sum()), poe_le_5=int((par / pe <= 5).sum()), parallax_error_ge_2=int((pe >= 2).sum()),
                abs_b_le_10=int((np.abs(b) <= 10 - 1e-6).sum()), source_id_out_of_span=int(((sid < k * FE.LEVEL0) | (sid >= (k + 1) * FE.LEVEL0)).sum()),
                duplicates=int(len(sid) - len(np.unique(sid))))


def fetch_delta_chunk(k, where, tmp):
    from astropy.table import vstack
    lo0, hi0 = k * FE.LEVEL0, (k + 1) * FE.LEVEL0
    st = dict(calls=0, truncated=0, cut_or_failed=0, received=0, rows=0, t0=time.time())
    parts, lo, w = [], lo0, W0
    while lo < hi0:
        hi = min(lo + w, hi0)
        q = f"SELECT {FE.COLS} FROM gaiadr3.gaia_source WHERE {where} AND source_id >= {lo} AND source_id < {hi}"
        t0 = time.time()
        try:
            T, nb = Q1.run_query(q, tmp)
        except RuntimeError:                                       # three failed or timed-out attempts: halve the piece
            st["cut_or_failed"] += 1
            if w <= MIN_W:
                raise
            w = max(w // 2, MIN_W)
            continue
        el = time.time() - t0
        st["calls"] += 1
        st["received"] += nb
        if st["received"] > CAP_CHUNK:
            raise SystemExit(f"STOPPED: chunk {k} received {st['received'] / 1e6:.2f} MB after {st['calls']} queries against the {CAP_CHUNK / 1e6:.2f} MB per-chunk cap -- report to the owner before continuing")
        if st["calls"] > MAX_QUERIES:
            raise SystemExit(f"STOPPED: chunk {k}: more than {MAX_QUERIES} queries")
        if len(T) >= Q1.SYNC_CAP:                                  # truncated by the synchronous cap: discard, never use
            st["truncated"] += 1
            if w <= MIN_W:
                raise RuntimeError("a minimum-width piece hit the 2000-row cap")
            w = max(w // 2, MIN_W)
            continue
        parts.append(T)
        st["rows"] += len(T)
        lo = hi
        w = min(w * 2, MAX_W) if el < 3.0 else (max(w // 2, MIN_W) if el > 25.0 else w)
        time.sleep(PAUSE_S)
    st["seconds"] = round(time.time() - st["t0"], 1)
    return (vstack(parts, join_type="exact") if parts else None), st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-go-recorded", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--chunks", default="1-11")
    a = ap.parse_args()
    chunks = parse_chunks(a.chunks)
    where = Q3.where_null()
    print(f"query (per source_id piece): SELECT <{len(FE.COLS.split(','))} frozen columns> FROM gaiadr3.gaia_source WHERE {where} AND source_id >= lo AND source_id < hi\n"
          f"chunks {chunks}; frozen chunk files on disk: " + ", ".join(f"{k}:{'ok' if (EXTRACT / f'chunk_{k:02d}.fits').exists() else 'MISSING'}" for k in chunks), flush=True)
    if a.plan_only:
        return
    if not a.owner_go_recorded:
        raise SystemExit("refused: pass --owner-go-recorded (the owner's go for the full-size Q3, delta form)")
    from astropy.table import Table, Column, vstack
    man = json.loads(MAN.read_text()) if MAN.exists() else {}
    man["approval"] = ("owner's go for the full-size Q3 in the delta form (the rows with no G magnitude of chunks 1-11, about 400 small synchronous queries, about 6 MB received; the frozen chunks "
                       "are already on disk), given in the calculation chat 2026-09-30; caps 2 MB per chunk and 15 MB in total")
    man["where_delta"] = where
    man.setdefault("chunks", {})
    VAR.mkdir(parents=True, exist_ok=True)
    (VAR / ".gitignore").write_text("*\n!.gitignore\n")
    total = sum(v.get("received_bytes", 0) for v in man["chunks"].values())
    for k in chunks:
        out, dout = VAR / f"chunk_{k:02d}.fits", VAR / f"q3_delta_no_G_chunk_{k:02d}.fits"
        if str(k) in man["chunks"] and out.exists() and dout.exists():
            print(f"chunk {k}: already done (manifest entry and outputs exist); skipping", flush=True)
            continue
        primary = EXTRACT / f"chunk_{k:02d}.fits"
        assert primary.exists(), f"the frozen chunk {k} is missing"
        D, st = fetch_delta_chunk(k, where, VAR / "q3_tmp.fits")
        total += st["received"]
        if total > CAP_TOTAL:
            raise SystemExit(f"STOPPED: {total / 1e6:.2f} MB received in total against the {CAP_TOTAL / 1e6:.0f} MB cap -- report to the owner before continuing")
        P = Table.read(primary, format="fits")
        sid_p = np.asarray(P["source_id"], np.int64)
        assert np.all((sid_p >= k * FE.LEVEL0) & (sid_p < (k + 1) * FE.LEVEL0)), f"frozen chunk {k} has source_ids outside its span"
        assert not np.isnan(np.asarray(P["phot_g_mean_mag"], float)).any(), f"frozen chunk {k} has rows without G"
        if D is None or len(D) == 0:
            D = P[:0].copy()
        bad = validate_delta(D, k) if len(D) else {}
        assert all(v == 0 for v in bad.values()), f"chunk {k}: delta rows violate the WHERE: {bad}"
        assert set(D.colnames) == set(P.colnames), "delta and frozen chunk columns differ"
        D2 = Table()
        for c in P.colnames:
            col = np.asarray(D[c].filled(np.nan) if hasattr(D[c], "filled") and D[c].dtype.kind == "f" else D[c])
            D2[c] = Column(col.astype(P[c].dtype), name=c)
        assert np.intersect1d(sid_p, np.asarray(D2["source_id"], np.int64)).size == 0, f"chunk {k}: delta rows overlap the frozen rows"
        U = vstack([P, D2], join_type="exact", metadata_conflicts="silent")
        U.write(out, format="fits", overwrite=True)
        D2.write(dout, format="fits", overwrite=True)
        man["chunks"][str(k)] = dict(rows_frozen=int(len(P)), rows_delta=int(len(D2)), rows_union=int(len(U)), delta_violations=bad, queries=st["calls"],
                                     truncated_results_discarded=st["truncated"], pieces_cut_or_failed=st["cut_or_failed"], received_bytes=st["received"], seconds=st["seconds"],
                                     sha256_frozen=sha256(primary), sha256_delta=sha256(dout), sha256_union=sha256(out), bytes_union=out.stat().st_size)
        MAN.write_text(json.dumps(man, indent=1) + "\n")
        print(f"chunk {k}: delta rows {len(D2):,d}; union {len(U):,d} = {len(P):,d} frozen + {len(D2):,d}; {st['calls']} queries ({st['truncated']} truncated, {st['cut_or_failed']} cut/failed), "
              f"received {st['received'] / 1e6:.3f} MB, {st['seconds']:.0f} s; total received so far {total / 1e6:.2f} MB", flush=True)
    print("done; manifest", MAN.name, flush=True)


if __name__ == "__main__":
    main()
