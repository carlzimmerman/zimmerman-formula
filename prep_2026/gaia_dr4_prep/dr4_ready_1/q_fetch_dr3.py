#!/usr/bin/env python3
"""DR4-READY-1: the three APPROVED read-only DR3 archive queries (NEW file; the only DR4-READY-1 script that opens the network).

The owner's go was given in the calculation chat on 2026-09-29 for exactly: Q2 (the final DR3 sample's component ids against
DR3's four nss_* tables, < 1 MB), the Q1 pilot (cut-13 neighbour cones around 500 pairs, ~10-20 MB) and the Q3 pilot (one sky
chunk of the frozen extract query without 'phot_g_mean_mag IS NOT NULL', ~35 MB).  Full-size Q1 and Q3 need a SEPARATE go and
are refused here.  Nothing frozen is edited; catalog_builder/fetch_extract.py is imported read-only for its column list, WHERE
text and chunk boundaries so the Q3 pilot differs from chunk 0 ONLY by the dropped G condition.
Outputs (gitignored): real_research/data/widebinaries/dr3_extract/dr4_ready_1/  and  .../dr3_extract_allsource_15c/chunk_00.fits
Manifest (committed): manifest_q_dr3.json in this directory (query text, row counts, sha256, times).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q_fetch_dr3.py --q2 --q1-pilot --q3-pilot --owner-go-recorded
"""
import sys
sys.dont_write_bytecode = True
import argparse, csv, hashlib, json, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
sys.path.insert(0, str(PREP / "catalog_builder"))
sys.path.insert(0, str(HERE))
import fetch_extract as FE                                      # read-only: COLS, WHERE, LEVEL0
import cut13_allsource as W1

WB = REPO / "real_research" / "data" / "widebinaries"
OUT = WB / "dr3_extract" / "dr4_ready_1"
VAR = WB / "dr3_extract_allsource_15c"
MAN = HERE / "manifest_q_dr3.json"
NSS_DR3 = ("nss_two_body_orbit", "nss_acceleration_astro", "nss_non_linear_spectro", "nss_vim_fl")
APPROVAL = ("owner's go, calculation chat, 2026-09-29: Q2 + Q1 pilot (500 pairs) + Q3 pilot (1 chunk); full-size Q1/Q3 need "
            "a separate go")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def run(q, out_path, upload=None, upload_name=None, attempts=4):
    from astroquery.gaia import Gaia
    for k in range(attempts):
        try:
            kw = dict(dump_to_file=True, output_file=str(out_path), output_format="fits")
            if upload:
                kw.update(upload_resource=str(upload), upload_table_name=upload_name)
            job = Gaia.launch_job_async(q, **kw)
            job.get_results()
            return
        except Exception as exc:
            if out_path.exists():
                out_path.unlink()
            print(f"  attempt {k + 1} failed ({type(exc).__name__}: {str(exc)[:160]}); retrying in {20 * (k + 1)} s", flush=True)
            time.sleep(20 * (k + 1))
    raise RuntimeError(f"archive job failed {attempts} times")


def nrows(p):
    from astropy.io import fits
    with fits.open(p, memmap=True) as h:
        return int(len(h[1].data))


def final_pairs():
    rows = list(csv.DictReader(open(WB / "dr3_extract" / "wide_binaries_dr3.csv")))
    return np.array([int(r["source_id1"]) for r in rows], np.int64), np.array([int(r["source_id2"]) for r in rows], np.int64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q2", action="store_true")
    ap.add_argument("--q1-pilot", action="store_true")
    ap.add_argument("--q3-pilot", action="store_true")
    ap.add_argument("--owner-go-recorded", action="store_true", help="required: the owner's go for exactly these three")
    ap.add_argument("--n-pilot-pairs", type=int, default=500)
    ap.add_argument("--q1-batches", type=int, default=1,
                    help="split the Q1 pilot's pairs into this many separate jobs (same pairs, same query form; owner's go 2026-09-29 "
                         "after the single 1,000-cone job timed out at the archive after ~1h45m)")
    args = ap.parse_args()
    if not args.owner_go_recorded:
        raise SystemExit("refused: pass --owner-go-recorded (the owner's go for Q2 + the two pilots, given in the calculation chat)")
    if args.n_pilot_pairs > 500:
        raise SystemExit("refused: the approved Q1 pilot is 500 pairs; full-size Q1 needs a separate go")
    from astropy.table import Table
    OUT.mkdir(parents=True, exist_ok=True)
    man = json.loads(MAN.read_text()) if MAN.exists() else {}
    man["approval"] = APPROVAL
    man.setdefault("queries", {})
    a_ids, b_ids = final_pairs()

    if args.q2:
        ids = np.unique(np.concatenate([a_ids, b_ids]))
        up = OUT / "q2_upload_ids.xml"
        Table({"source_id": ids}).write(up, format="votable", overwrite=True)
        for t in NSS_DR3:
            q = f"SELECT u.source_id FROM tap_upload.ids AS u JOIN gaiadr3.{t} AS t ON t.source_id = u.source_id"
            p = OUT / f"q2_{t}.fits"
            t0 = time.time()
            run(q, p, upload=up, upload_name="ids")
            man["queries"][f"Q2_{t}"] = dict(query=q, n_upload=int(len(ids)), rows=nrows(p), sha256=sha256(p),
                                             bytes=p.stat().st_size, seconds=round(time.time() - t0, 1), file=str(p.relative_to(REPO)))
            print(f"Q2 {t}: {man['queries'][f'Q2_{t}']['rows']} rows ({p.stat().st_size} bytes)", flush=True)

    if args.q1_pilot:
        S = np.load(WB / "dr3_extract" / "stage_A.npz")
        order = np.argsort(S["source_id"])
        def row(sid):
            i = np.searchsorted(S["source_id"][order], sid)
            return order[i]
        rng = np.random.default_rng(20261202)
        pick = np.sort(rng.choice(len(a_ids), size=args.n_pilot_pairs, replace=False))
        ia, ib = row(a_ids[pick]), row(b_ids[pick])
        assert np.all(S["source_id"][ia] == a_ids[pick]) and np.all(S["source_id"][ib] == b_ids[pick])
        upt = W1.upload_table(pick, S["ra"][ia], S["dec"][ia], S["ra"][ib], S["dec"][ib], S["parallax"][ia])
        up = OUT / "q1_pilot_upload.xml"
        Table(upt).write(up, format="votable", overwrite=True)
        np.savez(OUT / "q1_pilot_pairs.npz", pick=pick, source_id_a=a_ids[pick], source_id_b=b_ids[pick])
        q = W1.adql_cones("gaiadr3.gaia_source", upload="pairs")
        p = OUT / "q1_pilot_neighbours.fits"
        t0 = time.time()
        if args.q1_batches <= 1:
            run(q, p, upload=up, upload_name="pairs")
            batches = None
        else:
            from astropy.table import vstack
            parts, batches = [], []
            for kb, sub in enumerate(np.array_split(np.arange(len(pick)), args.q1_batches)):
                ub = Table({k: v[np.repeat(sub, 2) * 2 + np.tile([0, 1], len(sub))] for k, v in upt.items()})
                upb = OUT / f"q1_pilot_upload_b{kb}.xml"
                ub.write(upb, format="votable", overwrite=True)
                pb = OUT / f"q1_pilot_neighbours_b{kb}.fits"
                tb = time.time()
                run(q, pb, upload=upb, upload_name="pairs")
                parts.append(Table.read(pb, format="fits"))
                batches.append(dict(batch=kb, n_pairs=int(len(sub)), rows=nrows(pb), sha256=sha256(pb), bytes=pb.stat().st_size,
                                    seconds=round(time.time() - tb, 1), file=str(pb.relative_to(REPO))))
                print(f"  Q1 batch {kb}: {batches[-1]['rows']:,d} rows in {batches[-1]['seconds']:.0f} s", flush=True)
            vstack(parts).write(p, format="fits", overwrite=True)
        man["queries"]["Q1_pilot"] = dict(query=q, n_pairs=int(len(pick)), n_upload_rows=int(len(upt["pair_id"])), rows=nrows(p),
                                          sha256=sha256(p), bytes=p.stat().st_size, seconds=round(time.time() - t0, 1),
                                          seed=20261202, file=str(p.relative_to(REPO)),
                                          radius_arcsec_range=[float(upt["radius_deg"].min() * 3600), float(upt["radius_deg"].max() * 3600)],
                                          batches=batches,
                                          history="2026-09-29: the single 1,000-cone job timed out after ~1h45m (TimeoutError); its "
                                                  "automatic retry was stopped and, on the owner's go, the same 500 pairs were resubmitted "
                                                  "as separate batch jobs")
        print(f"Q1 pilot: {man['queries']['Q1_pilot']['rows']:,d} rows ({p.stat().st_size / 1e6:.1f} MB)", flush=True)

    if args.q3_pilot:
        drop = "AND phot_g_mean_mag IS NOT NULL "
        assert drop in FE.WHERE, "the frozen WHERE text changed; refusing"
        where = FE.WHERE.replace(drop, "")
        VAR.mkdir(parents=True, exist_ok=True)
        (VAR / ".gitignore").write_text("*\n!.gitignore\n")
        q = (f"SELECT {FE.COLS} FROM gaiadr3.gaia_source WHERE {where} AND source_id >= 0 AND source_id < {FE.LEVEL0}")
        p = VAR / "chunk_00.fits"
        t0 = time.time()
        run(q, p)
        man["queries"]["Q3_pilot"] = dict(query=q, frozen_where=FE.WHERE, dropped=drop.strip(), rows=nrows(p), sha256=sha256(p),
                                          bytes=p.stat().st_size, seconds=round(time.time() - t0, 1), file=str(p.relative_to(REPO)))
        print(f"Q3 pilot: {man['queries']['Q3_pilot']['rows']:,d} rows ({p.stat().st_size / 1e6:.1f} MB)", flush=True)

    MAN.write_text(json.dumps(man, indent=1) + "\n")
    print("manifest written:", MAN.name)


if __name__ == "__main__":
    main()
