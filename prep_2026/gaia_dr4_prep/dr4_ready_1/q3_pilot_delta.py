#!/usr/bin/env python3
"""DR4-READY-1: the approved Q3 pilot in its MINIMAL form (NEW file; networked; needs --owner-go-recorded).

The approved Q3 pilot is chunk 0 of the frozen extract query WITHOUT 'AND phot_g_mean_mag IS NOT NULL' (about 35 MB), the base of Amendment 15(c)'s all-source variant.
Its rows are exactly (a) the frozen chunk 0 that is already on disk (329,234 rows, none without a G magnitude, same columns, same DR3 release) plus (b) the rows that
satisfy the same WHERE but have NO G magnitude.  Only (b) has to come from the archive:
    SELECT <frozen COLS> FROM gaiadr3.gaia_source WHERE parallax > 3.5 AND parallax_over_error > 5 AND parallax_error < 2 AND phot_g_mean_mag IS NULL AND ABS(b) > 10
           AND source_id >= lo AND source_id < hi
over source_id pieces of the level-0 pixel 0 span [0, 2^35 x 4^12): synchronous queries (the anonymous async queue is blocked; the upload joins stall), each answering
in seconds because the source_id range hits the primary-key index; the synchronous endpoint returns at most 2000 rows silently, so a result of exactly 2000 rows is
TRUNCATED, discarded and its piece halved (never used); a piece that has not answered within 120 s is cut and retried, then halved.  The download is the (small) delta, at
most 5 MB by a hard cap, instead of about 35 MB.  The result is assembled LOCALLY: chunk_00.fits in the (gitignored) dr3_extract_allsource_15c/ = the frozen chunk 0 rows
followed by the delta rows, in the frozen column order and dtypes.  The row set equals what the approved query would return (DR3 is static); the archive's row ORDER is not
reproduced (the frozen chunk 0 is not sorted either), which the pilot's builder does not depend on (it sorts).  Delta rows are validated locally against the WHERE (G absent,
parallax, parallax_over_error, parallax_error, |b| > 10, source_id < LEVEL0) and are disjoint from the frozen rows.
Guards.  Needs --owner-go-recorded; --plan-only is offline; refuses if the frozen WHERE text changed; 5 MB cap on all bytes received; at most 2500 queries.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q3_pilot_delta.py --owner-go-recorded [--plan-only]
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

WB = REPO / "real_research" / "data" / "widebinaries"
PRIMARY = WB / "dr3_extract" / "chunk_00.fits"
VAR = WB / "dr3_extract_allsource_15c"
MAN = HERE / "manifest_q3_delta.json"
DROP = "AND phot_g_mean_mag IS NOT NULL "
CAP_BYTES = 5_000_000
MAX_QUERIES = 2500
PAUSE_S = 0.5
W0, MAX_W, MIN_W = FE.LEVEL0 // 128, FE.LEVEL0 // 16, 2 ** 39     # initial / largest / smallest piece width in source_id (MIN_W = 16 level-12 pixels)


def where_null():
    assert DROP in FE.WHERE, "the frozen WHERE text changed; refusing"
    return FE.WHERE.replace(DROP, "AND phot_g_mean_mag IS NULL ")


def fetch_delta(man):
    from astropy.table import vstack
    where = where_null()
    st = dict(calls=0, truncated=0, cut_or_failed=0, received=0, rows=0, t0=time.time())
    parts, lo, w = [], 0, W0
    tmp = VAR / "q3_tmp.fits"

    def stop(why):
        man["stopped"] = why
        MAN.write_text(json.dumps(man, indent=1) + "\n")
        raise SystemExit("STOPPED: " + why + " -- report to the owner before continuing")

    while lo < FE.LEVEL0:
        hi = min(lo + w, FE.LEVEL0)
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
        if st["received"] > CAP_BYTES:
            stop(f"received {st['received'] / 1e6:.2f} MB after {st['calls']} queries against the {CAP_BYTES / 1e6:.2f} MB cap")
        if st["calls"] > MAX_QUERIES:
            stop(f"more than {MAX_QUERIES} queries")
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
        if st["calls"] % 20 == 0 or lo >= FE.LEVEL0:
            print(f"  source_id {lo / FE.LEVEL0:6.1%} of the span: {st['calls']} queries, {st['truncated']} truncated, {st['cut_or_failed']} cut/failed, {st['rows']} delta rows, "
                  f"received {st['received'] / 1e6:.3f} MB, {time.time() - st['t0']:.0f} s", flush=True)
        time.sleep(PAUSE_S)
    st["seconds"] = round(time.time() - st["t0"], 1)
    return (vstack(parts, join_type="exact") if parts else None), st


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def validate_delta(D):
    """Local check of the delta rows against the WHERE they were asked for; returns a dict of violation counts (all must be 0)."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    g = np.asarray(D["phot_g_mean_mag"], float)
    par, pe = np.asarray(D["parallax"], float), np.asarray(D["parallax_error"], float)
    b = SkyCoord(np.asarray(D["ra"], float) * u.deg, np.asarray(D["dec"], float) * u.deg, frame="icrs").galactic.b.deg
    sid = np.asarray(D["source_id"], np.int64)
    return dict(has_G=int((~np.isnan(g)).sum()), parallax_le_3p5=int((par <= 3.5).sum()), poe_le_5=int((par / pe <= 5).sum()), parallax_error_ge_2=int((pe >= 2).sum()),
                abs_b_le_10=int((np.abs(b) <= 10 - 1e-6).sum()), source_id_out_of_span=int(((sid < 0) | (sid >= FE.LEVEL0)).sum()), duplicates=int(len(sid) - len(np.unique(sid))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-go-recorded", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    a = ap.parse_args()
    where = where_null()
    print(f"query (per source_id piece): SELECT <{len(FE.COLS.split(','))} frozen columns> FROM gaiadr3.gaia_source WHERE {where} AND source_id >= lo AND source_id < hi\n"
          f"span [0, {FE.LEVEL0}); first piece width {W0} ({FE.LEVEL0 // W0} pieces), adaptive between {MAX_W} and {MIN_W}; frozen chunk 0 on disk: {PRIMARY.name} "
          f"{'present' if PRIMARY.exists() else 'MISSING'}", flush=True)
    if a.plan_only:
        return
    if not a.owner_go_recorded:
        raise SystemExit("refused: pass --owner-go-recorded (the owner's go for the Q3 pilot)")
    from astropy.table import Table, Column, vstack
    man = {"approval": "owner's go for the Q3 pilot (chunk 0 without the G condition, about 35 MB), 2026-09-29; fetched as only the rows the approved query adds to the frozen chunk 0 "
                       "(no G magnitude), as synchronous source_id-piece queries (the approved async form is blocked)",
           "where_delta": where, "primary_file": str(PRIMARY.relative_to(REPO)) if REPO in PRIMARY.parents else PRIMARY.name, "cap_bytes": CAP_BYTES}
    VAR.mkdir(parents=True, exist_ok=True)
    (VAR / ".gitignore").write_text("*\n!.gitignore\n")
    D, st = fetch_delta(man)
    P = Table.read(PRIMARY, format="fits")
    if D is None or len(D) == 0:
        D = P[:0].copy()
    bad = validate_delta(D) if len(D) else {}
    assert all(v == 0 for v in bad.values()), f"delta rows violate the WHERE: {bad}"
    assert set(D.colnames) == set(P.colnames), "delta and frozen chunk 0 columns differ"
    D2 = Table()
    for c in P.colnames:
        col = np.asarray(D[c].filled(np.nan) if hasattr(D[c], "filled") and D[c].dtype.kind == "f" else D[c])
        D2[c] = Column(col.astype(P[c].dtype), name=c)
    assert np.intersect1d(np.asarray(P["source_id"], np.int64), np.asarray(D2["source_id"], np.int64)).size == 0, "delta rows overlap the frozen chunk 0"
    U = vstack([P, D2], join_type="exact", metadata_conflicts="silent")
    out = VAR / "chunk_00.fits"
    U.write(out, format="fits", overwrite=True)
    dout = VAR / "q3_delta_no_G.fits"
    D2.write(dout, format="fits", overwrite=True)
    man.update(rows_frozen_chunk0=int(len(P)), rows_delta=int(len(D2)), rows_union=int(len(U)), delta_violations=bad, queries=st["calls"], truncated_results_discarded=st["truncated"],
               pieces_cut_or_failed=st["cut_or_failed"], received_bytes=st["received"], seconds=st["seconds"],
               sha256_frozen_chunk0=sha256(PRIMARY), sha256_delta=sha256(dout), sha256_union=sha256(out), bytes_union=out.stat().st_size,
               file_union=str(out.relative_to(REPO)) if REPO in out.parents else out.name)
    MAN.write_text(json.dumps(man, indent=1) + "\n")
    print(f"delta rows (no G, same WHERE) {len(D2):,d}; union {len(U):,d} = {len(P):,d} frozen + {len(D2):,d}; {st['calls']} queries ({st['truncated']} truncated results discarded, "
          f"{st['cut_or_failed']} pieces cut/failed), received {st['received'] / 1e6:.3f} MB, {st['seconds']:.0f} s; wrote {out.name}, manifest {MAN.name}", flush=True)


if __name__ == "__main__":
    main()
