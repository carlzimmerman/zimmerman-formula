#!/usr/bin/env python3
"""DR4-READY-1, WP3 DR3 dry run: the join path must reproduce the reference DR3 build EXACTLY.

Plan: PLAN.md in this directory (c45c8d2ae).  NEW file; PREREGISTRATION_DR4.md, hash files, amendments,
catalog_builder/*.py and wide_binary_pipeline.py are imported read-only (bytecode writing disabled) and never edited.
No network: every input is the cached DR3 build (stage_A-F npz, the correlation cache, the A_V cache).

  R0  reference: stage G re-run exactly as build_catalog.main() does it, from the cached stages  -> CSV bytes (sha256);
      compared with the committed-to-disk wide_binaries_dr3.csv (reported; the join test compares with R0).
  J1  the four join columns (ruwe, ipd_frac_multi_peak, radial_velocity, radial_velocity_error) are REMOVED from the
      extract, written to a second table in shuffled order, rejoined by source_id with join_columns.py, and stage G is
      re-run: the CSV must be byte-identical to R0 (the pass line), and the join report must show 0 unmatched ids.
  Controls (each must be caught; exit 0 only if all are):
      K1  a needed column absent from every table            -> the join must RAISE
      K2  duplicated source_ids in the second table            -> the join must RAISE
      K3  1% of the ids dropped from the second table          -> the report must COUNT them, and the CSV must DIFFER
DR3 numbers here are a code-path test, not a result (Amendment 7(e)): no verdict word.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/wp3_join_dryrun_dr3.py   (a few minutes: stage G's Monte Carlo)
"""
import sys
sys.dont_write_bytecode = True                                  # never write __pycache__ into the frozen folders
import os, io, csv, json, time, hashlib, contextlib, socket
from pathlib import Path
import numpy as np


# NETWORK GUARD (added after the first attempt stalled, idle, inside stage G): this dry run must never contact the Gaia
# archive -- any archive query needs the owner's explicit go.  Every outgoing connection attempt raises.
class NoNetwork(RuntimeError):
    pass


def _blocked(*a, **k):
    raise NoNetwork("network access attempted during an offline dry run (blocked by design)")


socket.socket.connect = _blocked
socket.socket.connect_ex = _blocked
socket.create_connection = _blocked
socket.getaddrinfo = _blocked

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
sys.path.insert(0, str(PREP / "catalog_builder"))
sys.path.insert(0, str(PREP))
sys.path.insert(0, str(HERE))
import build_catalog as B                                       # read-only import of the frozen builder
from join_columns import join_by_source_id


CORR_NOTE = {}


def fetch_correlations_offline(release, source_ids, cache):
    """replaces B.fetch_correlations IN THIS PROCESS ONLY (the frozen file is not edited) and never queries the archive.
    Found on the first attempt: the frozen builder's cache (stage_G_corr.npz) holds only its LAST query's ids (it is
    overwritten, not merged), so it lacks 14 ids of today's primary selection, and the frozen function would query the
    archive for them.  Offline source (declared): the union of the two on-disk caches stage_G_corr.npz and
    stage_G_corr_elbadry.npz (identical values on their 20,496 shared ids); ids in neither get ZERO parallax-PM
    correlations (NaN breaks the frozen Monte Carlo's Cholesky step; zero keeps the covariance positive definite and
    touches at most those few pairs' sigma(vtilde)) -- IDENTICALLY in R0 and J1, so the join test stays exact.  Their count is
    recorded; fetching them would be an archive query, which needs the owner's go."""
    zs = [np.load(cache.parent / f) for f in ("stage_G_corr.npz", "stage_G_corr_elbadry.npz")]
    sid = np.concatenate([z["source_id"] for z in zs])
    cols = ("parallax_pmra_corr", "parallax_pmdec_corr")
    val = {c: np.concatenate([z[c] for z in zs]) for c in cols}
    u, first = np.unique(sid, return_index=True)
    ids = np.unique(np.asarray(source_ids))
    pos = np.searchsorted(u, ids)
    pos_c = np.clip(pos, 0, len(u) - 1)
    hit = (pos < len(u)) & (u[pos_c] == ids)
    out = {"source_id": ids}
    for c in cols:
        v = np.zeros(len(ids))                                  # declared: zero correlation for ids in neither cache
        v[hit] = val[c][first[pos_c[hit]]]
        out[c] = v
    CORR_NOTE.setdefault("n_uncovered", []).append(int((~hit).sum()))
    return out


B.fetch_correlations = fetch_correlations_offline

EXT = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract"
JOIN_COLS = ("ruwe", "ipd_frac_multi_peak", "radial_velocity", "radial_velocity_error")
T0 = time.time()
LOG = []


def P(s=""):
    print(s, flush=True)
    LOG.append(s)


def stage_g(S, F):
    """stage G exactly as build_catalog.main() runs it (copied, not edited), returning the CSV bytes and the cut flow."""
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx = np.flatnonzero(pre)
    extra["third"][idx] = B.third_star_flags(S, F["a"][idx], F["b"][idx])
    pre2, _, tab0 = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx2 = np.flatnonzero(pre2)
    corr = B.fetch_correlations("dr3", np.concatenate([S["source_id"][F["a"][idx2]], S["source_id"][F["b"][idx2]]]),
                                EXT / "stage_G_corr.npz")
    sig_vt = B.vt_error_mc(S, F["a"][idx2], F["b"][idx2], F["th"][idx2], corr)
    from wide_binary_pipeline import G as GN, MSUN, AU
    vc0 = np.sqrt(GN * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * MSUN / (tab0["sep_kAU"][idx2] * 1e3 * AU)) / 1e3
    vt0 = tab0["v_perp_kms"][idx2] / vc0
    ok = np.zeros(len(F["a"]), bool)
    ok[idx2] = sig_vt <= 0.1 * np.maximum(1.0, vt0 / 2)
    extra["vt_err_ok"] = ok
    z = B.av_sfd98(S, EXT / "AV_sfd98.npz")
    if z is not None:
        extra["AV_ok"] = (z["av"][F["a"]] < 0.5) & (z["av"][F["b"]] < 0.5)
    keepG, flow, table = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    cols = list(table)
    w.writerow(cols)
    for i in np.flatnonzero(keepG):
        w.writerow([table[c][i] for c in cols])
    return buf.getvalue().encode(), flow


def sha(b):
    return hashlib.sha256(b).hexdigest()


P(__doc__.split("Run: python3")[0].strip())
S = dict(np.load(EXT / "stage_A.npz", allow_pickle=False))
F = dict(np.load(EXT / "stage_F.npz", allow_pickle=False))
P(f"\n[load] {len(S['ra']):,d} sources, {len(F['a']):,d} pairs with R computed  ({time.time() - T0:.0f} s)")
missing = [c for c in JOIN_COLS if c not in S]
if missing:
    raise SystemExit(f"the DR3 extract lacks {missing}: cannot run the join test")

# ---------------------------------------------------------------- R0 reference
with contextlib.redirect_stdout(io.StringIO()):
    ref_bytes, ref_flow = stage_g(S, F)
disk = (EXT / "wide_binaries_dr3.csv").read_bytes()
n_ref = ref_bytes.count(b"\n") - 1
P(f"[R0] stage G re-run from the cached stages: {n_ref:,d} pairs; sha256 {sha(ref_bytes)[:16]}; "
  f"the on-disk wide_binaries_dr3.csv {'IS byte-identical' if disk == ref_bytes else 'DIFFERS (reported; J1 compares with R0)'} "
  f"({disk.count(b'\n') - 1:,d} pairs, sha256 {sha(disk)[:16]})  ({time.time() - T0:.0f} s)")

# ---------------------------------------------------------------- J1 the join path
rng = np.random.default_rng(20261202)
perm = rng.permutation(len(S["source_id"]))
ext_table = {"source_id": S["source_id"][perm], **{c: S[c][perm] for c in JOIN_COLS}}
base = {k: v for k, v in S.items() if k not in JOIN_COLS}
S_j, rep = join_by_source_id(base, [("dr3_second_table", ext_table)], JOIN_COLS)
with contextlib.redirect_stdout(io.StringIO()):
    j_bytes, j_flow = stage_g(S_j, F)
ok_j1 = j_bytes == ref_bytes and all(v["n_unmatched"] == 0 for v in rep["columns"].values())
P(f"[J1] join path: columns {list(JOIN_COLS)} removed, rejoined from a shuffled second table; report "
  + ", ".join(f"{c}: {v['n_matched']:,d} matched / {v['n_unmatched']} unmatched" for c, v in rep["columns"].items())
  + f";  CSV {'BYTE-IDENTICAL to R0' if j_bytes == ref_bytes else 'DIFFERS from R0'}  -> {'PASS' if ok_j1 else 'FAIL'}  ({time.time() - T0:.0f} s)")

# ---------------------------------------------------------------- controls
res = {}
try:
    join_by_source_id(base, [("t", {"source_id": ext_table["source_id"], "ruwe": ext_table["ruwe"]})], JOIN_COLS)
    res["K1"] = False
except KeyError as e:
    res["K1"] = True
P(f"[K1] a needed column absent from every table -> the join {'RAISES (caught)' if res['K1'] else 'DID NOT RAISE (control failed)'}")
try:
    dup = {k: np.concatenate([v, v[:5]]) for k, v in ext_table.items()}
    join_by_source_id(base, [("t", dup)], JOIN_COLS)
    res["K2"] = False
except ValueError:
    res["K2"] = True
P(f"[K2] duplicated source_ids in the second table -> the join {'RAISES (caught)' if res['K2'] else 'DID NOT RAISE (control failed)'}")
drop = rng.random(len(ext_table["source_id"])) < 0.01
thin = {k: v[~drop] for k, v in ext_table.items()}
S_k, rep_k = join_by_source_id(base, [("t", thin)], JOIN_COLS)
with contextlib.redirect_stdout(io.StringIO()):
    k_bytes, k_flow = stage_g(S_k, F)
counted = all(v["n_unmatched"] == int(drop.sum()) for v in rep_k["columns"].values())
res["K3"] = counted and (k_bytes != ref_bytes)
P(f"[K3] {int(drop.sum()):,d} ids (1%) dropped from the second table -> unmatched counted per column: {counted}; "
  f"CSV differs from R0: {k_bytes != ref_bytes} ({k_bytes.count(b'\n') - 1:,d} pairs)  -> {'caught' if res['K3'] else 'NOT caught'}")

ok = ok_j1 and all(res.values())
P(f"\n[verdict of the dry run, code path only] J1 {'PASS' if ok_j1 else 'FAIL'}; controls K1 {res['K1']}, K2 {res['K2']}, K3 {res['K3']}"
  f"  -> WP3 {'READY on DR3' if ok else 'NOT READY'}  (total {time.time() - T0:.0f} s)")
P(f"[corr] offline correlation source: ids in neither on-disk cache (zero correlation, identical in every run): {CORR_NOTE.get('n_uncovered')}")
out = dict(corr_uncovered=CORR_NOTE.get("n_uncovered"), R0=dict(n_pairs=n_ref, sha256=sha(ref_bytes), on_disk_identical=disk == ref_bytes, on_disk_sha256=sha(disk),
                   cut_flow=ref_flow),
           J1=dict(pass_=ok_j1, sha256=sha(j_bytes), report=rep), controls=res, K3_report=rep_k, ready=ok,
           seconds=round(time.time() - T0, 1))
(HERE / "wp3_join_dryrun_dr3_results.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
(HERE / "wp3_join_dryrun_dr3.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
