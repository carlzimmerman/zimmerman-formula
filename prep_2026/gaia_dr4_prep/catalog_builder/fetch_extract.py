#!/usr/bin/env python3
"""Step 1 of the DR4 wide-binary catalog chain: pull the source extract.

Usage:
    python3 fetch_extract.py --release dr3      # validation run (now)
    python3 fetch_extract.py --release dr4      # 2 Dec 2026: same query, new table

The query is El-Badry, Rix & Heintz (2021, MNRAS 506, 2269), Sec. 2:
    parallax > P_MIN AND parallax_over_error > 5 AND parallax_error < 2
    AND phot_g_mean_mag IS NOT NULL
with two volume restrictions chosen so that every FROZEN_DR4_CUTS pair is
fully contained with margin:
    * parallax > 3.5 mas. A frozen pair has mean distance < 250 pc and
      parallax S/N >= 40, so both components have parallax > 4 - 3*0.1 = 3.7.
    * |b| > 10 deg. Frozen pairs have |b| > 15; the 1-deg sky-density
      feature and the 5-pc cluster search (<= 1.15 deg at 250 pc) stay inside.
Known limitation: the triple screen (co-moving third source, G < 20) can
miss a faint third star whose parallax scatters below 3.5 mas near 250 pc.

The sky is split into the 12 HEALPix level-0 pixels by source_id range
(source_id // 2^35 is the level-12 nested index), so that no single job
approaches the archive row limit.  Chunks already on disk are skipped.

Also fetched: the El-Badry Sigma_18 sky-density input, i.e. counts of
initial-query sources (parallax > 1, same quality cuts) with G < 18 per
HEALPix level-7 pixel, aggregated server side.

Outputs go to real_research/data/widebinaries/<release>_extract/ (gitignored);
a manifest with query text, row counts and sha256 is written next to this
script and is committed.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
COLS = ("source_id, ra, dec, parallax, parallax_error, pmra, pmdec, pmra_error, "
        "pmdec_error, pmra_pmdec_corr, phot_g_mean_mag, bp_rp, ruwe, "
        "ipd_frac_multi_peak, radial_velocity, radial_velocity_error, non_single_star")
WHERE = ("parallax > 3.5 AND parallax_over_error > 5 AND parallax_error < 2 "
         "AND phot_g_mean_mag IS NOT NULL AND ABS(b) > 10")
LEVEL0 = 2 ** 35 * 4 ** 12          # source_id span of one HEALPix level-0 pixel


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def run_job(q, path, attempts=5):
    """Async archive job with retries: a dropped connection or TLS timeout
    (seen on the DR3 run, chunk 8) must not abort a release-day fetch."""
    from astroquery.gaia import Gaia
    for k in range(attempts):
        try:
            job = Gaia.launch_job_async(q, dump_to_file=True, output_file=str(path),
                                        output_format="fits")
            job.get_results()
            return
        except Exception as exc:                      # network / archive hiccup
            if path.exists():
                path.unlink()
            wait = 30 * (k + 1)
            print(f"  attempt {k + 1} failed ({type(exc).__name__}: {exc}); retrying in {wait} s")
            time.sleep(wait)
    raise RuntimeError(f"archive job failed {attempts} times: {q[:80]}...")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", choices=("dr3", "dr4"), required=True)
    args = ap.parse_args()
    from astroquery.gaia import Gaia

    table = f"gaia{args.release}.gaia_source"
    out = REPO / "real_research" / "data" / "widebinaries" / f"{args.release}_extract"
    out.mkdir(parents=True, exist_ok=True)
    (out / ".gitignore").write_text("*\n!.gitignore\n")
    manifest_path = HERE / f"manifest_{args.release}.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest.update({"table": table, "columns": COLS, "where": WHERE,
                     "sigma18_where": "parallax > 1 AND parallax_over_error > 5 AND "
                                      "parallax_error < 2 AND phot_g_mean_mag < 18"})
    chunks = manifest.setdefault("chunks", {})

    for k in range(12):
        path = out / f"chunk_{k:02d}.fits"
        if path.exists() and str(k) in chunks and chunks[str(k)].get("sha256") == sha256(path):
            print(f"chunk {k}: present, skipped")
            continue
        q = (f"SELECT {COLS} FROM {table} WHERE {WHERE} "
             f"AND source_id >= {k * LEVEL0} AND source_id < {(k + 1) * LEVEL0}")
        t0 = time.time()
        run_job(q, path)
        from astropy.io import fits
        with fits.open(path, memmap=True) as h:
            n = len(h[1].data)
        chunks[str(k)] = {"query": q, "rows": n, "sha256": sha256(path),
                          "seconds": round(time.time() - t0, 1),
                          "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"chunk {k}: {n:,d} rows in {chunks[str(k)]['seconds']} s")

    path = out / "sigma18_hpx7.fits"
    if not path.exists():
        q = (f"SELECT GAIA_HEALPIX_INDEX(7, source_id) AS hpx7, COUNT(*) AS n FROM {table} "
             f"WHERE {manifest['sigma18_where']} GROUP BY hpx7")
        t0 = time.time()
        run_job(q, path)
        manifest["sigma18"] = {"query": q, "sha256": sha256(path),
                               "seconds": round(time.time() - t0, 1)}
        print(f"sigma18 counts in {manifest['sigma18']['seconds']} s")
    manifest["total_rows"] = sum(c["rows"] for c in chunks.values())
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"total rows {manifest['total_rows']:,d}")


if __name__ == "__main__":
    main()
