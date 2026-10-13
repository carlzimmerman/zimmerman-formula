#!/usr/bin/env python3
"""CFG679D resumable downloader (HTTP range requests into the public DES Y3 HDF5 files; no whole-file download).

Each job is (file, dataset, piece index): a piece is one HDF5 chunk (chunked datasets) or a 1,000,000-row slice (contiguous datasets).
Every piece is fetched with one range request, checked for its exact length, its SHA-256 is logged, and it is stored as float32 (or
int32 / int64 for integer columns) in campaign_fresh_gravity/_external_data/cfg679_des/<tag>/<col>/<piece>.npy. A piece already on
disk is skipped (resume). Pieces of the same row slice are fetched together so that a partial run leaves complete row slices.
Order: given by --order (seeded random permutation of slices, so any partial completion is a random subset of the sky tiles).
Memory guard (cfg679_lib.guard) before every slice. Log: <data>/download_<tag>.log (repo-relative paths only).

Usage: python3 cfg679_download.py <tag> [--threads 2] [--max-gb X]
  tags: sm (stellar-mass catalogue: ra, dec, z, mstar), smid (its coadd_obj_id, for the GOLD match),
        mcal (metacal unsheared ra, dec, e_1, e_2, weight), resp (unsheared R11, R22 on 20 seeded random 1M-row chunks),
        gold (GOLD 2.2 coadd_object_id + g, r, i magnitudes chosen by `listcols gold`, or GOLD_COLS env),
        listcols --file gold|index (metadata only: column list -> <file>_columns.json; for gold also gold_choice.json),
        index (index select_bin1..4 row lists, any HDF5 layout, read through h5py in 1M-element slices),
        selresp (select_1p/1m/2p/2m rows inside the 20 response chunks, by a coarse sample + window reads; optional input).
Modes added 2026-10-13 (smid, resp, listcols, index, selresp; chunked datasets of any chunk length): the mcal path is unchanged.
"""
import os, sys, json, time, hashlib, argparse, threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg679_lib as L                                                      # noqa: E402

ROWS = 1_000_000
SPEC = {
    "sm": ("stellar_mass/DESY3_stellar_mass_catalog.hdf5", "", ["ra", "dec", "z", "mstar"]),
    "mcal": ("y3kp_cats/DESY3_metacal_v03-004.h5", "catalog/unsheared/", ["ra", "dec", "e_1", "e_2", "weight"]),
    "gold": ("y3kp_cats/DESY3_GOLD_2_2.1.h5", "catalog/gold/", []),        # from gold_choice.json (listcols gold) or GOLD_COLS env
    "smid": ("stellar_mass/DESY3_stellar_mass_catalog.hdf5", "", ["coadd_obj_id"]),
    "resp": ("y3kp_cats/DESY3_metacal_v03-004.h5", "catalog/unsheared/", ["R11", "R22"]),
}
FILES = {"gold": "y3kp_cats/DESY3_GOLD_2_2.1.h5", "index": "y3kp_cats/DESY3_indexcat.h5"}
NRESP, RESP_SEED = 20, 6790
ap = argparse.ArgumentParser()
ap.add_argument("tag"); ap.add_argument("--threads", type=int, default=2); ap.add_argument("--max-gb", type=float, default=30.0)
ap.add_argument("--seed", type=int, default=679)
ap.add_argument("--light-guard", action="store_true", help="network-only job: pause only when free+inactive < 8 GB (orchestrator line), not on every big PM run")
ap.add_argument("--file", default="", help="listcols: gold or index")
A = ap.parse_args()
if A.tag in ("listcols", "index", "selresp"):
    import cfg679_download_meta as DM                                       # noqa: E402  (metadata / generic-layout modes)
    sys.exit(DM.main(A))
path, grp, cols = SPEC[A.tag]
if A.tag == "gold":
    cols = [c for c in os.environ.get("GOLD_COLS", "").split(",") if c]
    if not cols:
        _gc = os.path.join(L.DATA, "gold_choice.json")
        if not os.path.exists(_gc):
            print("gold: no GOLD_COLS and no gold_choice.json; run `cfg679_download.py listcols --file gold` first"); sys.exit(2)
        _gj = json.load(open(_gc))
        cols = _gj["columns"]
        if _gj.get("compressed"):                 # compressed GOLD layout: the generic h5py slice reader (same piece files, 1M rows)
            import cfg679_download_meta as DM                                   # noqa: E402
            sys.exit(DM.generic(A, "gold", path, [grp + c for c in cols], cols))
OUT = os.path.join(L.DATA, A.tag)
os.makedirs(OUT, exist_ok=True)
LOGP = os.path.join(L.DATA, f"download_{A.tag}.log")
lock = threading.Lock()


def say(s):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {s}"
    with lock:
        print(line, flush=True)
        open(LOGP, "a").write(line + "\n")


url = L.BASE + path
PIECES = {}                                   # col -> list of (offset, nbytes, nrows, dtype)
PJ = os.path.join(OUT, "pieces.json")
if os.path.exists(PJ):                        # resume: reuse the chunk map, skip the slow HDF5 metadata reads
    _pj = json.load(open(PJ))
    PIECES = {c: [tuple(p) for p in _pj[c]] for c in cols if c in _pj}
    say(f"{A.tag}: chunk map reused from pieces.json for {sorted(PIECES)}")
todo = [c for c in cols if c not in PIECES]
if todo:
    f = L.RangeFile(url, block=256 * 1024, nblocks=4096)
    h = h5py.File(f, "r")
for c in todo:
    d = h[grp + c]
    n = d.shape[0]
    if d.chunks is None:
        off = d.id.get_offset()
        it = d.dtype.itemsize
        PIECES[c] = [(off + i * ROWS * it, min(ROWS, n - i * ROWS) * it, min(ROWS, n - i * ROWS), d.dtype.str)
                     for i in range((n + ROWS - 1) // ROWS)]
    else:
        assert d.compression is None, (c, d.chunks, d.compression)   # compressed layouts go through the generic h5py reader
        CR = d.chunks[0]                                                # 1,000,000 for metacal (unchanged); any length otherwise
        nch = d.id.get_num_chunks()
        info = sorted((d.id.get_chunk_info(i) for i in range(nch)), key=lambda x: x.chunk_offset[0])
        PIECES[c] = []
        for ci in info:
            r0 = ci.chunk_offset[0]
            nr = min(CR, n - r0)
            PIECES[c].append((ci.byte_offset, nr * d.dtype.itemsize, nr, d.dtype.str))   # last chunk: only valid rows
    say(f"{A.tag}/{c}: {len(PIECES[c])} pieces, dtype {d.dtype.str}, rows {n:,}")
    json.dump({c: [list(map(lambda x: x if not isinstance(x, np.integer) else int(x), p)) for p in v] for c, v in PIECES.items()},
              open(PJ, "w"))                  # saved after each column, so a crash keeps the finished maps
NP = len(PIECES[cols[0]])
assert all(len(v) == NP for v in PIECES.values())
order = np.random.default_rng(A.seed).permutation(NP)
if A.tag == "resp":                           # 20 seeded random chunks (FROZEN_CRITERIA section 3); the list is stored for the measurement
    order = np.sort(np.random.default_rng(RESP_SEED).choice(NP, NRESP, replace=False))
    json.dump({"chunks": [int(i) for i in order], "seed": RESP_SEED, "rows_per_chunk": ROWS}, open(os.path.join(L.DATA, "resp_chunks.json"), "w"))
say(f"{A.tag}: meta bytes so far {L.BYTES['n'] / 1e6:.1f} MB; {NP} slices x {len(cols)} columns; order seed {A.seed}")
tot_planned = sum(PIECES[c][int(i)][1] for c in cols for i in order)
say(f"{A.tag}: planned bytes {tot_planned / 1e9:.2f} GB")
if tot_planned > A.max_gb * 1e9:
    say("ABORT: plan exceeds --max-gb"); sys.exit(2)


def fetch(i, c):
    fn = os.path.join(OUT, c, f"{i:04d}.npy")
    if os.path.exists(fn):
        return 0
    off, nb, nr, dt = PIECES[c][i]
    raw = L.get_range(url, off, off + nb)
    sha = hashlib.sha256(raw).hexdigest()
    a = np.frombuffer(raw, dtype=dt)
    assert a.size == nr
    a = a.astype(np.float32) if a.dtype.kind == "f" else a.astype(np.int64)
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    np.save(fn + ".tmp.npy", a)
    os.replace(fn + ".tmp.npy", fn)
    say(f"  piece {A.tag}/{c}/{i:04d} rows {nr} bytes {nb} sha256 {sha}")
    return nb


t0 = time.time(); got = 0
with ThreadPoolExecutor(A.threads) as ex:
    for k, i in enumerate(order):
        if A.light_guard:
            while L.free_inactive_gb() < 8.0:
                say("[light-guard] PAUSE: free+inactive < 8 GB"); time.sleep(120)
        else:
            L.guard(say)
        got += sum(ex.map(lambda c: fetch(int(i), c), cols))
        if k % 5 == 0:
            el = time.time() - t0
            say(f"{A.tag}: {k + 1}/{NP} slices, this run {got / 1e9:.3f} GB, {got / max(el, 1) / 1e6:.2f} MB/s")
say(f"{A.tag}: COMPLETE; this run {got / 1e9:.3f} GB in {(time.time() - t0) / 3600:.2f} h; session bytes {L.BYTES['n'] / 1e9:.3f} GB")
