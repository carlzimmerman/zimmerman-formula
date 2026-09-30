#!/usr/bin/env python3
"""DR4-READY-1: the Q1 pilot in the archive's DOCUMENTED efficient cone-join form (NEW file; networked; needs the owner's go recorded).

Why.  The approved Q1 pilot (neighbour cones around 500 pairs) used a PER-ROW radius (CIRCLE(..., u.radius_deg)) and did not return (the single 1,000-cone job
timed out; batch 0 of the 5-batch split ran > 1 h).  This script fetches the SAME 500 pairs' neighbourhoods with ONE cone per pair centred on the pair's midpoint,
radius R + theta/2 (which contains both 30 kAU / d cones), using a literal constant radius per radius-class batch (radius ratio <= 1.25 within a batch), i.e. the
upload cone-join form the archive documents.  The result is a superset of the exact two-cone set; it is re-filtered LOCALLY to the exact cones (radius 30 kAU / d
around each component, R = 30 x parallax_primary arcsec) and written in the original schema (pair_id, comp, columns) to q1_pilot_neighbours.fits, so
wp1_cut13_pilot_dr3.py runs unchanged.  Offline plan (no network): 500 pairs, 8 batches (129, 135, 94, 71, 37, 19, 10, 5), 9.4 deg2 of cones against 12.9 deg2
of duplicated two-cone area in the approved form; at 10-40k sources / deg2 that is about 9-36 MB (about 14-22 MB at typical |b| > 10 densities).
Scope: the same 500 seeded pairs; refuses more.  Full-size Q1 and Q3 need a separate go.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_pilot_midpoint.py --owner-go-recorded [--plan-only]
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, hashlib, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import cut13_allsource as W1

WB = REPO / "real_research" / "data" / "widebinaries"
OUT = WB / "dr3_extract" / "dr4_ready_1"
MAN = HERE / "manifest_q1_midpoint.json"
COLS = W1.COLS
KEEP = ("source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error", "phot_g_mean_mag")


def vec(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], -1)


def plan(n_max=500):
    S = np.load(WB / "dr3_extract" / "stage_A.npz")
    order = np.argsort(S["source_id"])
    row = lambda s: order[np.searchsorted(S["source_id"][order], s)]
    Z = np.load(OUT / "q1_pilot_pairs.npz")
    assert len(Z["pick"]) <= n_max, "the approved pilot is 500 pairs"
    ia, ib = row(Z["source_id_a"]), row(Z["source_id_b"])
    assert np.all(S["source_id"][ia] == Z["source_id_a"]) and np.all(S["source_id"][ib] == Z["source_id_b"])
    va, vb = vec(S["ra"][ia], S["dec"][ia]), vec(S["ra"][ib], S["dec"][ib])
    theta = np.degrees(np.arccos(np.clip((va * vb).sum(1), -1, 1))) * 3600
    R = W1.radius_arcsec(S["parallax"][ia])
    mid = va + vb
    mid /= np.linalg.norm(mid, axis=1)[:, None]
    ra_m = np.degrees(np.arctan2(mid[:, 1], mid[:, 0])) % 360
    de_m = np.degrees(np.arcsin(np.clip(mid[:, 2], -1, 1)))
    rad = (R + theta / 2) * 1.0005                                  # tiny margin; the exact cones are re-applied locally
    o = np.argsort(rad)
    batches, start = [], 0
    for i in range(1, len(o) + 1):
        if i == len(o) or rad[o[i]] > 1.25 * rad[o[start]]:
            batches.append(o[start:i])
            start = i
    return dict(S=S, ia=ia, ib=ib, va=va, vb=vb, R=R, theta=theta, ra_m=ra_m, de_m=de_m, rad=rad, batches=batches, pick=Z["pick"], sa=Z["source_id_a"], sb=Z["source_id_b"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-go-recorded", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    a = ap.parse_args()
    P = plan()
    rad_deg_b = [float(P["rad"][b].max() / 3600) for b in P["batches"]]
    print(f"plan: {len(P['pick'])} pairs in {len(P['batches'])} batches {[len(b) for b in P['batches']]}; batch radii (arcsec) "
          f"{[round(r * 3600) for r in rad_deg_b]}; total cone area {sum(len(b) * np.pi * r ** 2 for b, r in zip(P['batches'], rad_deg_b)):.2f} deg2")
    if a.plan_only:
        return
    if not a.owner_go_recorded:
        raise SystemExit("refused: pass --owner-go-recorded (the owner's go for the Q1 pilot in this form)")
    from astropy.table import Table, vstack
    from astroquery.gaia import Gaia
    man = {"approval": "owner's go for the Q1 pilot (500 pairs) 2026-09-29; this midpoint / constant-radius form: see the go recorded in the calculation chat", "batches": []}
    raw_parts = []
    for k, b in enumerate(P["batches"]):
        r_deg = rad_deg_b[k]
        up = OUT / f"q1_mid_upload_b{k}.xml"
        Table({"pair_id": P["pick"][b].astype(np.int64), "ra": P["ra_m"][b], "dec": P["de_m"][b]}).write(up, format="votable", overwrite=True)
        cols = ", ".join(f"s.{c}" for c in KEEP)
        q = (f"SELECT u.pair_id, {cols} FROM tap_upload.pairs AS u JOIN gaiadr3.gaia_source AS s "
             f"ON 1 = CONTAINS(POINT('ICRS', s.ra, s.dec), CIRCLE('ICRS', u.ra, u.dec, {r_deg:.6f}))")
        pth = OUT / f"q1_mid_b{k}.fits"
        t0 = time.time()
        for att in range(4):
            try:
                job = Gaia.launch_job_async(q, upload_resource=str(up), upload_table_name="pairs", dump_to_file=True, output_file=str(pth), output_format="fits")
                job.get_results()
                break
            except Exception as exc:
                if pth.exists():
                    pth.unlink()
                print(f"  batch {k} attempt {att + 1} failed ({type(exc).__name__}: {str(exc)[:120]}); retrying in {30 * (att + 1)} s", flush=True)
                time.sleep(30 * (att + 1))
        else:
            raise RuntimeError(f"batch {k} failed 4 times")
        T = Table.read(pth, format="fits")
        raw_parts.append(T)
        man["batches"].append(dict(batch=k, n_pairs=int(len(b)), radius_deg=r_deg, rows=int(len(T)), bytes=pth.stat().st_size, seconds=round(time.time() - t0, 1),
                                   sha256=hashlib.sha256(open(pth, "rb").read()).hexdigest(), query=q, file=str(pth.relative_to(REPO))))
        print(f"  batch {k}: {len(b)} pairs, radius {r_deg * 3600:.0f}\", {len(T):,d} rows, {man['batches'][-1]['seconds']:.0f} s", flush=True)
    # exact re-filter to the two cones per pair, in the original schema
    T = vstack(raw_parts)
    pid = np.asarray(T["pair_id"], np.int64)
    where = {int(p): i for i, p in enumerate(P["pick"])}
    idx = np.array([where[int(p)] for p in pid])
    vs = vec(np.asarray(T["ra"], float), np.asarray(T["dec"], float))
    rows, comps = [], []
    for c, vc in ((0, P["va"]), (1, P["vb"])):
        d = np.degrees(np.arccos(np.clip((vs * vc[idx]).sum(1), -1, 1))) * 3600
        m = d <= P["R"][idx]
        rows.append(np.flatnonzero(m)); comps.append(np.full(int(m.sum()), c))
    sel = np.concatenate(rows)
    E = T[sel]
    E["comp"] = np.concatenate(comps)
    E = E["pair_id", "comp", *KEEP]
    out = OUT / "q1_pilot_neighbours.fits"
    E.write(out, format="fits", overwrite=True)
    man.update(rows_raw=int(len(T)), rows_exact=int(len(E)), file=str(out.relative_to(REPO)), sha256=hashlib.sha256(open(out, "rb").read()).hexdigest(), bytes=out.stat().st_size)
    MAN.write_text(json.dumps(man, indent=1) + "\n")
    print(f"exact two-cone rows {len(E):,d} (from {len(T):,d} raw); wrote {out.name}, manifest {MAN.name}")


if __name__ == "__main__":
    main()
