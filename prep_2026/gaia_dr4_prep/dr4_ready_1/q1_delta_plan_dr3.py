#!/usr/bin/env python3
"""DR4-READY-1: the PLAN (offline, no network, nothing fetched) of a DR3 delta Q1: the neighbour cones of the cut-13 candidate pairs that are NOT final pairs (DR3: 4,021 of the 10,231 pairs that pass every cut except A_V, the vtilde error and
cut 13), minus the source_id ranges the full-size Q1 already holds.  Reports the pairs, the pixel ranges still uncovered, and a size / time estimate from the full Q1's own densities.  NEW file.  DR3 numbers are code-path tests (Amendment 7(e)).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/q1_delta_plan_dr3.py"""
import sys
sys.dont_write_bytecode = True
import csv, json, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dry_run_driver as D
import q1_pilot_ranges as Q1
import cut13_allsource as W1
D.init(False)
B = D.B
ext = D.extract_dir("dr3", "primary")
T0 = time.time()
S = dict(np.load(ext / "stage_A.npz")); F = dict(np.load(ext / "stage_F.npz"))
extra = {"third": np.zeros(len(F["a"]), bool)}
pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
idx = np.flatnonzero(pre)
sid = S["source_id"]
cand = {(int(sid[F["a"][i]]), int(sid[F["b"][i]])) for i in idx}
final = {(int(r["source_id1"]), int(r["source_id2"])) for r in csv.DictReader(open(ext / "wide_binaries_dr3.csv"))}
delta = sorted(cand - final)
print(f"candidates (pass every cut except A_V, vtilde error, cut 13): {len(cand):,d}; final pairs: {len(final):,d}; candidates not final: {len(delta):,d} (final not among the candidates: {len(final - cand)})")


def plan_for(pairs):
    import healpy as hp
    order = np.argsort(S["source_id"])
    row = lambda s: order[np.searchsorted(S["source_id"][order], s)]
    sa = np.array([p[0] for p in pairs], np.int64); sb = np.array([p[1] for p in pairs], np.int64)
    ia, ib = row(sa), row(sb)
    va, vb = Q1.vec(S["ra"][ia], S["dec"][ia]), Q1.vec(S["ra"][ib], S["dec"][ib])
    R = W1.radius_arcsec(S["parallax"][ia])
    pix = set()
    for k in range(len(R)):
        for v in (va[k], vb[k]):
            pix.update(hp.query_disc(2 ** Q1.LEVEL, v, np.radians((R[k] + Q1.MARGIN_ARCSEC) / 3600), inclusive=True, nest=True).tolist())
    pix = np.array(sorted(pix), np.int64)
    return pix, hp.nside2pixarea(2 ** Q1.LEVEL, degrees=True)


pix_final, pa = plan_for(sorted(final))
pix_delta, _ = plan_for(delta)
new_pix = np.setdiff1d(pix_delta, pix_final)
print(f"level-{Q1.LEVEL} pixels: final-pair cones {len(pix_final):,d} ({len(pix_final) * pa:.1f} deg^2 union); delta-pair cones {len(pix_delta):,d} ({len(pix_delta) * pa:.1f} deg^2 union); delta pixels NOT already covered by the final-pair cones {len(new_pix):,d} ({len(new_pix) * pa:.1f} deg^2)")
# the source_id intervals the full Q1 accepted (from its cache index), for the exact subtraction at range level
idxp = ext.parent / "dr3_extract" / "dr4_ready_1" / "q1_full_cache" / "index.jsonl"
rng_done = []
for line in idxp.read_text().splitlines():
    rec = json.loads(line)
    if rec["type"] == "batch":
        rng_done += [tuple(r) for r in rec["ranges"]]
rng_done.sort()
merged = []
for lo, hi in rng_done:
    if merged and lo <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], hi)
    else:
        merged.append([lo, hi])
need = [(int(p) * Q1.DIV, (int(p) + 1) * Q1.DIV) for p in pix_delta]
mlo = np.array([m[0] for m in merged]); mhi = np.array([m[1] for m in merged])
unc = []
for lo, hi in need:
    j = np.searchsorted(mlo, lo, side="right") - 1
    if not (j >= 0 and mhi[j] >= hi):
        unc.append((lo, hi))
print(f"pixel-level check against the full Q1's accepted source_id intervals ({len(merged):,d} merged intervals): delta pixels not fully covered {len(unc):,d} of {len(need):,d}")
man = json.load(open(HERE / "manifest_q1_full.json"))
area_union = len(pix_final) * pa
dens_rows = man["rows_raw_unique"] / area_union
est_rows = len(unc) * pa * dens_rows
est_bytes = est_rows * 80
rate = man["seconds_this_session"] / man["rows_raw_unique"]
print(f"full Q1 reference: {man['rows_raw_unique']:,d} raw unique rows over {area_union:.1f} deg^2 union = {dens_rows:,.0f} rows/deg^2; {man['seconds_this_session']:.0f} s")
print(f"ESTIMATE for the delta (pixels not yet covered): {est_rows:,.0f} raw rows, about {est_bytes / 1e6:.0f} MB, about {est_rows * rate / 3600:.1f} h at the full Q1's rate ({rate * 1e3:.2f} ms per raw row); an upper bound without any reuse of the full Q1's ranges: {len(pix_delta) * pa * dens_rows:,.0f} rows")
out = dict(candidates=len(cand), final=len(final), delta_pairs=len(delta), pixels=dict(final=int(len(pix_final)), delta=int(len(pix_delta)), delta_not_in_final_cones=int(len(new_pix)), delta_not_fully_covered_by_q1_ranges=len(unc)),
           estimate=dict(raw_rows=float(est_rows), megabytes=float(est_bytes / 1e6), hours=float(est_rows * rate / 3600), upper_bound_rows=float(len(pix_delta) * pa * dens_rows)), seconds=round(time.time() - T0, 1))
(HERE / "q1_delta_plan_dr3.json").write_text(json.dumps(out, indent=1) + "\n")
