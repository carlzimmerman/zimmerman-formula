#!/usr/bin/env python3
"""DR4-READY-1: the approved Q1 pilot (neighbour data around 500 pairs), fetched with SYNCHRONOUS index-friendly source_id RANGE queries (NEW file; networked).

Why this form.  The approved per-row-radius upload cone join (CIRCLE(..., u.radius_deg)) never returned: the single 1,000-cone job, the 5-batch split, and a 6-cone probe
all stalled, as did a constant-radius upload join and a HEALPix-range UPLOAD join on the synchronous endpoint; a trivial synchronous primary-key query returned in
3 s, a trivial ASYNC job did not return in 170 s (the anonymous async queue is blocked by the earlier jobs), and a 3-pair test with the source_id ranges written as
LITERALS in the WHERE clause (no upload) returned 821 rows in 4.5 s.  Gaia's source_id encodes the level-12 HEALPix pixel (source_id // 2^35), so a pixel is a
contiguous source_id range and the query hits the primary-key index.  The synchronous endpoint returns at most 2000 rows, silently: a result of exactly 2000 rows is
TRUNCATED, is discarded and its batch is halved (a single range is split at its midpoint), so nothing truncated is ever used.
What it fetches.  For each of the same 500 seeded pairs, every level-12 pixel overlapping either component's 30 kAU / d cone (radius R = 30 x parallax_primary arcsec,
plus a 30 arcsec margin for the source_id position); adjacent pixels are merged into ranges, and batches of ranges are sent, sized (from the last accepted batch's rows per
range, growing at most 2x per step) to return about 500 rows.  The result is a superset of the exact cones and is re-filtered LOCALLY to the exact cones, written in the original schema
(pair_id, comp, columns) to q1_pilot_neighbours.fits so wp1_cut13_pilot_dr3.py runs unchanged.  Offline plan: 54,960 pixels, 8,411 ranges, 11.3 deg2, about 10-20 MB at
14.5k-30k sources / deg2.
Completeness checks (offline, on the local extract stage A): the planned ranges must cover the source_id of EVERY stage-A source inside the exact cones (they do: 3,513 of
3,513, so the source_id epoch shift is not an issue at the 30 arcsec margin), and after the fetch every such source must be present in the returned rows.
Guards.  The same 500 pairs (refuses more); a HARD CAP of 20 MB on the accepted result bytes (the approved size was 'about 10-20 MB') and of 30 MB on every byte received
(truncated results included): it stops and reports if either would be passed; needs --owner-go-recorded; --plan-only is offline.  Full-size Q1 needs a separate go.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_pilot_ranges.py --owner-go-recorded [--plan-only]
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, hashlib, re, signal, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import cut13_allsource as W1

WB = REPO / "real_research" / "data" / "widebinaries"
IN_DIR = WB / "dr3_extract" / "dr4_ready_1"                  # the seeded 500-pair list and the local extract (inputs)
OUT = IN_DIR                                                 # outputs (the offline test points this elsewhere)
MAN = HERE / "manifest_q1_ranges.json"
LEVEL, MARGIN_ARCSEC = 12, 30.0
SYNC_CAP = 2000                                              # rows the synchronous endpoint returns at most; exactly 2000 means truncated
TARGET_ROWS = 500                                            # aim for about a quarter of the cap per query so that a truncation (a wasted transfer of up to 2000 rows) is rare
CAP_ACCEPTED_BYTES = 20_000_000                              # the approved size ('about 10-20 MB'): accepted result bytes
CAP_TRANSFER_BYTES = 30_000_000                              # every byte received, truncated results included
PAUSE_S = 0.5
TIMEOUT_S = 120                                              # a query that has not returned in this long is abandoned and retried (a legitimate one takes seconds)
DIV = 2 ** 35 * 4 ** (12 - LEVEL)
KEEP = ("source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error", "phot_g_mean_mag")
RANGE_RE = re.compile(r"source_id >= (\d+) AND source_id < (\d+)")


def vec(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], -1)


def plan():
    import healpy as hp
    S = np.load(WB / "dr3_extract" / "stage_A.npz")
    A = {k: S[k] for k in ("source_id", "ra", "dec", "parallax")}       # read each array once
    order = np.argsort(A["source_id"])
    row = lambda s: order[np.searchsorted(A["source_id"][order], s)]
    Z = np.load(IN_DIR / "q1_pilot_pairs.npz")
    assert len(Z["pick"]) <= 500, "the approved pilot is 500 pairs"
    ia, ib = row(Z["source_id_a"]), row(Z["source_id_b"])
    assert np.all(A["source_id"][ia] == Z["source_id_a"]) and np.all(A["source_id"][ib] == Z["source_id_b"])
    va, vb = vec(A["ra"][ia], A["dec"][ia]), vec(A["ra"][ib], A["dec"][ib])
    R = W1.radius_arcsec(A["parallax"][ia])
    pix = set()
    for k in range(len(R)):
        for v in (va[k], vb[k]):
            pix.update(hp.query_disc(2 ** LEVEL, v, np.radians((R[k] + MARGIN_ARCSEC) / 3600), inclusive=True, nest=True).tolist())
    pix = np.array(sorted(pix), np.int64)
    brk = np.flatnonzero(np.diff(pix) != 1)
    st = np.concatenate([[0], brk + 1]); en = np.concatenate([brk, [len(pix) - 1]])
    rng = [(int(pix[a] * DIV), int((pix[b] + 1) * DIV)) for a, b in zip(st, en)]
    area = len(pix) * hp.nside2pixarea(2 ** LEVEL, degrees=True)
    return dict(A=A, va=va, vb=vb, R=R, pick=Z["pick"], rng=rng, n_pix=int(len(pix)), area=float(area))


def local_in_cones(P):
    """(pair_id, comp, source_id) of every local-extract (stage A) source inside the exact 30 kAU / d cones."""
    from scipy.spatial import cKDTree
    A = P["A"]
    tree = cKDTree(vec(np.asarray(A["ra"], float), np.asarray(A["dec"], float)))
    out = []
    for k in range(len(P["pick"])):
        chord = 2 * np.sin(np.radians(P["R"][k] / 3600) / 2)
        for c, vc in ((0, P["va"][k]), (1, P["vb"][k])):
            out.extend((int(P["pick"][k]), c, int(A["source_id"][j])) for j in tree.query_ball_point(vc, r=chord))
    return out


def plan_coverage(P, loc):
    """How many local-extract sources in the cones have a source_id outside every planned range (must be 0)."""
    lo = np.array([r[0] for r in P["rng"]], np.int64); hi = np.array([r[1] for r in P["rng"]], np.int64)
    ids = np.array([s for _, _, s in loc], np.int64)
    j = np.clip(np.searchsorted(lo, ids, side="right") - 1, 0, len(lo) - 1)
    ok = (ids >= lo[j]) & (ids < hi[j])
    return int(len(ids)), int((~ok).sum())


def launch_query(q, path):
    """One synchronous archive query written to a FITS file (the offline test replaces this function)."""
    from astroquery.gaia import Gaia
    Gaia.ROW_LIMIT = -1
    Gaia.launch_job(q, dump_to_file=True, output_file=str(path), output_format="fits")


class QueryTimeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise QueryTimeout(f"no answer within {TIMEOUT_S} s")


def run_query(q, tmp):
    """One query with a hard timeout (SIGALRM, main thread) and three attempts; returns (astropy Table, bytes received)."""
    from astropy.table import Table
    for att in range(3):
        old = signal.signal(signal.SIGALRM, _on_alarm)
        signal.alarm(TIMEOUT_S)
        try:
            launch_query(q, tmp)
            signal.alarm(0)
            nb = tmp.stat().st_size
            T = Table.read(tmp, format="fits")
            tmp.unlink()
            return T, nb
        except Exception as exc:
            signal.alarm(0)
            print(f"  query attempt {att + 1} failed ({type(exc).__name__}: {str(exc)[:120]}); retrying in {20 * (att + 1)} s", flush=True)
            if tmp.exists():
                tmp.unlink()
            time.sleep(20 * (att + 1))
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old)
    raise RuntimeError("a query failed 3 times")


def fetch_all(P, man):
    from astropy.table import vstack
    cols = ", ".join(KEEP)
    rng = list(P["rng"])
    n_total = len(rng)
    st = dict(calls=0, truncated=0, rows=0, accepted_bytes=0, received_bytes=0, t0=time.time())
    parts, i, n = [], 0, 30

    def stop(why):
        man["stopped"] = why
        MAN.write_text(json.dumps(man, indent=1) + "\n")
        raise SystemExit("STOPPED: " + why + " -- report to the owner before continuing")

    while i < len(rng):
        batch = rng[i:i + n]
        where = " OR ".join(f"(source_id >= {lo} AND source_id < {hi})" for lo, hi in batch)
        T, nb = run_query(f"SELECT {cols} FROM gaiadr3.gaia_source WHERE {where}", OUT / "q1_rng_tmp.fits")
        st["calls"] += 1
        st["received_bytes"] += nb
        if st["received_bytes"] > CAP_TRANSFER_BYTES:
            stop(f"received {st['received_bytes'] / 1e6:.2f} MB in {st['calls']} queries against the {CAP_TRANSFER_BYTES / 1e6:.2f} MB transfer cap")
        if len(T) >= SYNC_CAP:                                     # truncated by the synchronous cap: discard, never use
            st["truncated"] += 1
            if len(batch) > 1:
                n = max(1, len(batch) // 2)
            else:
                lo, hi = batch[0]
                if hi - lo < 2:
                    raise RuntimeError("a one-integer source_id range hit the 2000-row cap")
                rng[i:i + 1] = [(lo, (lo + hi) // 2), ((lo + hi) // 2, hi)]
            continue
        parts.append(T)
        st["rows"] += len(T)
        st["accepted_bytes"] += nb
        if st["accepted_bytes"] > CAP_ACCEPTED_BYTES:
            stop(f"accepted {st['accepted_bytes'] / 1e6:.2f} MB ({st['rows']:,d} rows) after {st['calls']} queries against the {CAP_ACCEPTED_BYTES / 1e6:.2f} MB cap")
        i += len(batch)
        proj = st["accepted_bytes"] * n_total / max(i, 1)
        if i >= 0.2 * n_total and proj > 1.25 * CAP_ACCEPTED_BYTES:
            stop(f"projected {proj / 1e6:.1f} MB accepted against the {CAP_ACCEPTED_BYTES / 1e6:.0f} MB cap after {i} of {n_total} ranges")
        n = int(np.clip(TARGET_ROWS / max(len(T) / len(batch), 0.5), 4, min(200, 2 * len(batch))))     # grow at most 2x per step
        if st["calls"] % 10 == 0 or i >= len(rng):
            print(f"  {i}/{len(rng)} ranges: {st['calls']} queries, {st['truncated']} truncated, {st['rows']:,d} rows, accepted {st['accepted_bytes'] / 1e6:.2f} MB, "
                  f"received {st['received_bytes'] / 1e6:.2f} MB, {time.time() - st['t0']:.0f} s", flush=True)
        time.sleep(PAUSE_S)
    st["seconds"] = round(time.time() - st["t0"], 1)
    return vstack(parts), st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-go-recorded", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    a = ap.parse_args()
    P = plan()
    print(f"plan: {len(P['pick'])} pairs; {P['n_pix']} level-{LEVEL} pixels, {len(P['rng'])} source_id ranges; {P['area']:.2f} deg2; "
          f"est. {P['area'] * 14.5e3 * 64 / 1e6:.0f}-{P['area'] * 30e3 * 64 / 1e6:.0f} MB at 14.5k-30k sources/deg2 (accepted cap {CAP_ACCEPTED_BYTES / 1e6:.2f} MB)", flush=True)
    loc = local_in_cones(P)
    tot, miss = plan_coverage(P, loc)
    print(f"coverage: {tot} local-extract sources inside the exact cones; {miss} have a source_id outside every planned range", flush=True)
    assert miss == 0, "the planned source_id ranges miss local-extract sources: widen the margin before any query"
    if a.plan_only:
        return
    if not a.owner_go_recorded:
        raise SystemExit("refused: pass --owner-go-recorded (the owner's go for the Q1 pilot)")
    man = {"approval": "owner's go for the Q1 pilot (500 pairs, about 10-20 MB), 2026-09-29; fetched as synchronous source_id-range queries (the approved cone-join forms stalled)",
           "level": LEVEL, "margin_arcsec": MARGIN_ARCSEC, "sync_cap_rows": SYNC_CAP, "target_rows_per_query": TARGET_ROWS,
           "cap_accepted_bytes": CAP_ACCEPTED_BYTES, "cap_transfer_bytes": CAP_TRANSFER_BYTES}
    from astropy.table import Table
    from scipy.spatial import cKDTree
    T, st = fetch_all(P, man)
    _, first = np.unique(np.asarray(T["source_id"], np.int64), return_index=True)
    T = T[np.sort(first)]
    # exact re-filter to the two 30 kAU / d cones per pair, original schema (pair_id, comp, columns)
    tree = cKDTree(vec(np.asarray(T["ra"], float), np.asarray(T["dec"], float)))
    rows, pid, cmp = [], [], []
    for k in range(len(P["pick"])):
        chord = 2 * np.sin(np.radians(P["R"][k] / 3600) / 2)
        for c, vc in ((0, P["va"][k]), (1, P["vb"][k])):
            js = tree.query_ball_point(vc, r=chord)
            rows.extend(js); pid.extend([int(P["pick"][k])] * len(js)); cmp.extend([c] * len(js))
    E = T[np.array(rows, int)]
    E["pair_id"] = np.array(pid, np.int64)
    E["comp"] = np.array(cmp, np.int64)
    E = E["pair_id", "comp", *KEEP]
    have = set(zip(np.asarray(E["pair_id"], np.int64).tolist(), np.asarray(E["comp"], np.int64).tolist(), np.asarray(E["source_id"], np.int64).tolist()))
    lost = sum(1 for x in loc if x not in have)
    out = OUT / "q1_pilot_neighbours.fits"
    E.write(out, format="fits", overwrite=True)
    man.update(rows_raw_unique=int(len(T)), rows_exact=int(len(E)), file=str(out.relative_to(REPO)) if REPO in out.parents else out.name,
               sha256=hashlib.sha256(open(out, "rb").read()).hexdigest(), bytes=out.stat().st_size, queries=st["calls"], truncated_results_discarded=st["truncated"],
               accepted_bytes=st["accepted_bytes"], received_bytes=st["received_bytes"], seconds=st["seconds"],
               local_extract_sources_in_cones=tot, local_extract_sources_missing_from_fetch=lost)
    MAN.write_text(json.dumps(man, indent=1) + "\n")
    print(f"exact two-cone rows {len(E):,d} from {len(T):,d} unique raw rows; {st['calls']} queries ({st['truncated']} truncated results discarded), accepted "
          f"{st['accepted_bytes'] / 1e6:.2f} MB, received {st['received_bytes'] / 1e6:.2f} MB, {st['seconds']:.0f} s; "
          f"local-extract sources in the cones missing from the fetch: {lost} of {tot}; wrote {out.name}, manifest {MAN.name}", flush=True)
    if lost:
        print("WARNING: the fetch is missing local-extract sources; do not use it for the pilot", flush=True)


if __name__ == "__main__":
    main()
