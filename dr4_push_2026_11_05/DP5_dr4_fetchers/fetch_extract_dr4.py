#!/usr/bin/env python3
"""DP5 (criteria FROZEN_CRITERIA.md, c4c56e708e): the stage-A extract fetch with a spec'd column list.

NEW file. The frozen `prep_2026/gaia_dr4_prep/catalog_builder/fetch_extract.py` builds the same query, but with a fixed
column list that selects `non_single_star` from gaia_source; the DR4 draft data model (2026-06-26) has that column only in
`all_source_flags`, and DR4 does not read it (cut 12 is the nss_* union). This tool keeps the frozen WHERE, the 12 level-0
chunks, the Sigma_18 query and the output layout, and takes the table and columns from a spec.

Every query needs the owner's go (--owner-go-recorded). Transports: the frozen async job with retries (default), or
--sync-ranges (sync queries over finer source_id ranges; a result of exactly the sync cap is discarded and split).

  python3 -B dr4_push_2026_11_05/DP5_dr4_fetchers/fetch_extract_dr4.py --release dr4 --print-queries
  python3 -B ... --release dr4 [--spec-json fix.json] [--sync-ranges] --manifest <path> --owner-go-recorded "<text>"
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

FROZEN_COLS = ("source_id, ra, dec, parallax, parallax_error, pmra, pmdec, pmra_error, "
               "pmdec_error, pmra_pmdec_corr, phot_g_mean_mag, bp_rp, ruwe, "
               "ipd_frac_multi_peak, radial_velocity, radial_velocity_error, non_single_star")
WHERE = ("parallax > 3.5 AND parallax_over_error > 5 AND parallax_error < 2 "
         "AND phot_g_mean_mag IS NOT NULL AND ABS(b) > 10")
SIGMA18_WHERE = "parallax > 1 AND parallax_over_error > 5 AND parallax_error < 2 AND phot_g_mean_mag < 18"
LEVEL0 = 2 ** 35 * 4 ** 12
SYNC_CAP = 2000


def _drop(cols, name):
    return ", ".join(c for c in (x.strip() for x in cols.split(",")) if c != name)


SPECS = {
    "dr3": dict(table="gaiadr3.gaia_source", columns=FROZEN_COLS),
    "dr4": dict(table="gaiadr4.gaia_source", columns=_drop(FROZEN_COLS, "non_single_star"),
                note="draft 2026-06-26: non_single_star only in all_source_flags and not read for DR4; confirm names on the day"),
}


def load_spec(release, spec_json=None):
    spec = dict(SPECS[release])
    sha = None
    if spec_json:
        raw = Path(spec_json).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        spec.update(json.loads(raw))
    return spec, sha


def chunk_query(spec, k, lo=None, hi=None):
    lo = k * LEVEL0 if lo is None else lo
    hi = (k + 1) * LEVEL0 if hi is None else hi
    return (f"SELECT {spec['columns']} FROM {spec['table']} WHERE {WHERE} "
            f"AND source_id >= {lo} AND source_id < {hi}")


def sigma18_query(spec):
    return (f"SELECT GAIA_HEALPIX_INDEX(7, source_id) AS hpx7, COUNT(*) AS n FROM {spec['table']} "
            f"WHERE {SIGMA18_WHERE} GROUP BY hpx7")


def fetch_sync_ranges(spec, k, sync, n_start=64, cap=SYNC_CAP, detect_truncation=True, log=None):
    """sync(query) -> dict of equal-length arrays (the rows). Returns the rows of chunk k as a list of dicts-of-arrays,
    plus counts. A piece returning exactly `cap` rows is discarded and split in two (never used)."""
    lo0, hi0 = k * LEVEL0, (k + 1) * LEVEL0
    step = (hi0 - lo0) // n_start
    todo = [(lo0 + i * step, lo0 + (i + 1) * step if i < n_start - 1 else hi0) for i in range(n_start)]
    parts, n_q, n_trunc = [], 0, 0
    while todo:
        lo, hi = todo.pop()
        rows = sync(chunk_query(spec, k, lo, hi))
        n_q += 1
        n = len(next(iter(rows.values()))) if rows else 0
        if detect_truncation and n >= cap:
            n_trunc += 1
            if hi - lo < 2:
                raise RuntimeError(f"a single source_id returned the cap: {lo}")
            mid = (lo + hi) // 2
            todo += [(lo, mid), (mid, hi)]
            continue
        parts.append(rows)
    if log:
        log(f"chunk {k}: {n_q} sync queries, {n_trunc} truncated results discarded and split")
    return parts, dict(queries=n_q, truncated=n_trunc)


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", choices=sorted(SPECS), required=True)
    ap.add_argument("--spec-json", default=None)
    ap.add_argument("--print-queries", action="store_true")
    ap.add_argument("--sync-ranges", action="store_true")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--owner-go-recorded", default="")
    a = ap.parse_args(argv)
    spec, sha = load_spec(a.release, a.spec_json)
    if a.print_queries:
        for k in range(12):
            print(chunk_query(spec, k))
        print(sigma18_query(spec))
        return 0
    if not a.owner_go_recorded.strip() or not a.manifest:
        raise SystemExit("a fetch needs --manifest and --owner-go-recorded (the owner's go, verbatim)")
    import numpy as np
    from astroquery.gaia import Gaia
    from astropy.table import Table
    out = Path(a.out_dir) if a.out_dir else REPO / "real_research" / "data" / "widebinaries" / f"{a.release}_extract"
    out.mkdir(parents=True, exist_ok=True)
    (out / ".gitignore").write_text("*\n!.gitignore\n")
    mp = Path(a.manifest)
    man = json.loads(mp.read_text()) if mp.exists() else {}
    man.update(table=spec["table"], columns=spec["columns"], where=WHERE, sigma18_where=SIGMA18_WHERE,
               spec_json=a.spec_json, spec_json_sha256=sha, transport="sync-ranges" if a.sync_ranges else "async",
               owner_go=a.owner_go_recorded, tool=str(Path(__file__).relative_to(REPO)))
    chunks = man.setdefault("chunks", {})

    def run_async(q, path, attempts=5):
        for i in range(attempts):
            try:
                job = Gaia.launch_job_async(q, dump_to_file=True, output_file=str(path), output_format="fits")
                job.get_results()
                return
            except Exception as exc:
                if path.exists():
                    path.unlink()
                print(f"  attempt {i + 1} failed ({type(exc).__name__}: {exc}); retrying in {30 * (i + 1)} s")
                time.sleep(30 * (i + 1))
        raise RuntimeError(f"archive job failed {attempts} times: {q[:80]}...")

    def sync(q):
        t = Gaia.launch_job(q).get_results()
        return {c: np.asarray(t[c]) for c in t.colnames}

    for k in range(12):
        path = out / f"chunk_{k:02d}.fits"
        if path.exists() and str(k) in chunks and chunks[str(k)].get("sha256") == _sha(path):
            print(f"chunk {k}: present, skipped")
            continue
        t0 = time.time()
        if a.sync_ranges:
            parts, cnt = fetch_sync_ranges(spec, k, sync, log=print)
            cols = list(parts[0]) if parts else [c.strip() for c in spec["columns"].split(",")]
            Table({c: np.concatenate([p[c] for p in parts]) for c in cols}).write(str(path), overwrite=True)
            extra = cnt
        else:
            run_async(chunk_query(spec, k), path)
            extra = {}
        from astropy.io import fits
        with fits.open(path, memmap=True) as h:
            n = len(h[1].data)
        chunks[str(k)] = dict(query=chunk_query(spec, k), rows=n, sha256=_sha(path), seconds=round(time.time() - t0, 1),
                              fetched_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **extra)
        mp.write_text(json.dumps(man, indent=2) + "\n")
        print(f"chunk {k}: {n:,d} rows")
    path = out / "sigma18_hpx7.fits"
    if not path.exists():
        run_async(sigma18_query(spec), path)
        man["sigma18"] = dict(query=sigma18_query(spec), sha256=_sha(path))
    man["total_rows"] = sum(c["rows"] for c in chunks.values())
    mp.write_text(json.dumps(man, indent=2) + "\n")
    print(f"total rows {man['total_rows']:,d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
