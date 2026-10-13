#!/usr/bin/env python3
"""CFG679D downloader, metadata and generic-layout modes (called from cfg679_download.py; same log / resume / SHA-256 rules).

  listcols --file gold   : keys of catalog/gold -> gold_columns.json; the magnitude choice of FROZEN_CRITERIA section 2 is made here,
                           from the column list alone, before any lens is selected -> gold_choice.json (coadd_object_id + g, r, i).
                           Rule: sof_cm_mag_corrected_<b> (SOF corrected); if absent, the GOLD 2.2 default model magnitudes
                           (BDF: first of bdf_mag_*corrected_<b>, bdf_mag_dered_<b>, bdf_mag_<b>).
  listcols --file index  : keys of / and index (one level down) -> index_columns.json, with layout of every select* dataset.
  index                  : select_bin1..4 (fiducial selection + tomographic bin) read through h5py in 1M-element slices (any layout);
                           stored as int64 under <data>/index/<name>/NNNN.npy; SHA-256 of the stored array bytes logged per slice.
  selresp                : select_1p/1m/2p/2m (per-bin names if they exist, else the global lists) restricted to the 20 response chunks
                           (resp_chunks.json): a coarse sample every STEP elements, then window reads; requires sorted lists.
Paths in logs are repo-relative. Light guard (free+inactive >= 8 GB) as for the metacal job when --light-guard is passed.
"""
import os, re, sys, json, time, hashlib
import numpy as np
import h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg679_lib as L                                                      # noqa: E402

FILES = {"gold": "y3kp_cats/DESY3_GOLD_2_2.1.h5", "index": "y3kp_cats/DESY3_indexcat.h5",
         "mcal": "y3kp_cats/DESY3_metacal_v03-004.h5"}
SL = 1_000_000
STEP = 500_000


def _say(tag):
    logp = os.path.join(L.DATA, f"download_{tag}.log")
    def say(s):
        line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {s}"
        print(line, flush=True)
        open(logp, "a").write(line + "\n")
    return say


def _wait(A, say):
    if getattr(A, "light_guard", False):
        while L.free_inactive_gb() < 8.0:
            say("[light-guard] PAUSE: free+inactive < 8 GB"); time.sleep(120)
    else:
        L.guard(say)


def _desc(o):
    return dict(shape=list(o.shape), dtype=str(o.dtype), chunks=o.chunks, compression=o.compression,
                nbytes=int(o.size * o.dtype.itemsize))


def _open(path, block=256 * 1024, nblocks=4096):
    return h5py.File(L.RangeFile(L.BASE + path, block=block, nblocks=nblocks), "r")


def choose_gold(keys):
    out = {"id": "coadd_object_id" if "coadd_object_id" in keys else None}
    for b in "gri":
        pick = None
        for pat in (rf"^sof_cm_mag_corrected_{b}$", rf"^bdf_mag_.*corrected_{b}$", rf"^bdf_mag_dered_{b}$", rf"^bdf_mag_{b}$"):
            hit = sorted(k for k in keys if re.match(pat, k))
            if hit:
                pick = hit[0]; break
        out[b] = pick
    return out


def listcols(A):
    say = _say("listcols")
    which = A.file
    h = _open(FILES[which])
    if which == "gold":
        keys = sorted(h["catalog/gold"].keys())
        json.dump({"group": "catalog/gold", "keys": keys}, open(os.path.join(L.DATA, "gold_columns.json"), "w"), indent=1)
        say(f"gold: {len(keys)} columns under catalog/gold")
        ch = choose_gold(keys)
        if None in ch.values():
            say(f"gold: magnitude/id choice INCOMPLETE {ch}; no gold_choice.json written"); return 2
        cols = [ch["id"], ch["g"], ch["r"], ch["i"]]
        lay = {c: _desc(h["catalog/gold/" + c]) for c in cols}
        comp = any(v["compression"] is not None for v in lay.values())
        json.dump({"columns": cols, "bands": ch, "layout": lay, "compressed": comp,
                   "rule": "sof_cm_mag_corrected_<b>; else GOLD 2.2 default model (BDF) magnitudes; chosen from the column list only"},
                  open(os.path.join(L.DATA, "gold_choice.json"), "w"), indent=1, default=str)
        say(f"gold: choice {ch}; layout {lay}")
        return 0
    if which == "index":
        rec = {"/": sorted(h.keys())}
        for g in rec["/"]:
            if isinstance(h[g], h5py.Group):
                rec[g] = sorted(h[g].keys())
                for k in rec[g]:
                    o = h[g][k]
                    if isinstance(o, h5py.Group):
                        rec[f"{g}/{k}"] = sorted(o.keys())
        lay = {}
        for g, ks in list(rec.items()):
            if g == "/":
                continue
            for k in ks:
                if k.startswith("select"):
                    o = h[f"{g}/{k}"]
                    if isinstance(o, h5py.Dataset):
                        lay[f"{g}/{k}"] = _desc(o)
        json.dump({"groups": rec, "layout": lay}, open(os.path.join(L.DATA, "index_columns.json"), "w"), indent=1, default=str)
        say(f"index: groups {list(rec)}; {len(lay)} select* datasets")
        return 0
    print("listcols needs --file gold|index"); return 2


def _index_names():
    js = json.load(open(os.path.join(L.DATA, "index_columns.json")))
    lay = js["layout"]
    def find(name):
        for pre in ("index/", "index/metacal/", "index/unsheared/"):
            if pre + name in lay:
                return pre + name
        return None
    return lay, find


def generic(A, tag, path, dsets, names):
    """1M-element slices of datasets of any HDF5 layout through h5py over range reads (8 MB blocks); resumable."""
    say = _say(tag)
    h = _open(path, block=8 << 20, nblocks=6)
    t0, got = time.time(), 0
    plan = sum(h[ds].size * h[ds].dtype.itemsize for ds in dsets)
    say(f"{tag}: planned (uncompressed) {plan / 1e9:.2f} GB")
    if plan > getattr(A, "max_gb", 30.0) * 1e9:
        say("ABORT: plan exceeds --max-gb"); return 2
    for ds, nm in zip(dsets, names):
        d = h[ds]
        n = d.shape[0]
        ns = (n + SL - 1) // SL
        say(f"{tag}/{nm}: {ns} slices, dtype {d.dtype}, rows {n:,}, chunks {d.chunks}, compression {d.compression}")
        os.makedirs(os.path.join(L.DATA, tag, nm), exist_ok=True)
        for i in range(ns):
            fn = os.path.join(L.DATA, tag, nm, f"{i:04d}.npy")
            if os.path.exists(fn):
                continue
            _wait(A, say)
            a = np.asarray(d[i * SL:min(n, (i + 1) * SL)])
            a = a.astype(np.float32) if a.dtype.kind == "f" else (a if a.dtype.kind == "b" else a.astype(np.int64))
            sha = hashlib.sha256(a.tobytes()).hexdigest()
            np.save(fn + ".tmp.npy", a); os.replace(fn + ".tmp.npy", fn)
            got += a.nbytes
            say(f"  slice {tag}/{nm}/{i:04d} rows {a.size} sha256(stored) {sha}")
    say(f"{tag}: COMPLETE; this run {got / 1e9:.3f} GB stored in {(time.time() - t0) / 3600:.2f} h; session bytes {L.BYTES['n'] / 1e9:.3f} GB")
    return 0


def index(A):
    lay, find = _index_names()
    names = [f"select_bin{b}" for b in range(1, 5)]
    ds = [find(n) for n in names]
    if None in ds:
        _say("index")(f"index: select_bin lists not found in index_columns.json ({dict(zip(names, ds))})"); return 2
    return generic(A, "index", FILES["index"], ds, names)


def selresp(A):
    say = _say("selresp")
    lay, find = _index_names()
    chunks = json.load(open(os.path.join(L.DATA, "resp_chunks.json")))["chunks"]
    want = {}
    for sh in ("1p", "1m", "2p", "2m"):
        per = [find(f"select_bin{b}_{sh}") or find(f"select_{sh}_bin{b}") for b in range(1, 5)]
        if None not in per:
            for b, p in zip(range(1, 5), per):
                want[f"bin{b}_{sh}"] = p
        elif find(f"select_{sh}"):
            want[f"all_{sh}"] = find(f"select_{sh}")
    if not want:
        say("selresp: no sheared selection lists in the index file -> selection response NEGLECTED (FROZEN_CRITERIA section 3)")
        json.dump({"present": False}, open(os.path.join(L.DATA, "selresp_done.json"), "w")); return 0
    h = _open(FILES["index"], block=256 * 1024, nblocks=64)
    out = os.path.join(L.DATA, "selresp"); os.makedirs(out, exist_ok=True)
    for nm, p in want.items():
        d = h[p]; n = d.shape[0]
        cfn = os.path.join(out, f"{nm}_coarse.npy")
        if os.path.exists(cfn):
            pos, val = np.load(cfn)
        else:
            pos = np.unique(np.r_[np.arange(0, n, STEP), n - 1])
            val = np.array([int(d[int(q)]) for q in pos])
            np.save(cfn, np.vstack([pos, val]))
        if np.any(np.diff(val) < 0):
            say(f"selresp: {p} is not sorted; window method not valid -> selection response NEGLECTED")
            json.dump({"present": True, "usable": False, "why": f"{p} unsorted"}, open(os.path.join(L.DATA, "selresp_done.json"), "w"))
            return 0
        for c in chunks:
            fn = os.path.join(out, nm, f"{c:04d}.npy")
            if os.path.exists(fn):
                continue
            _wait(A, say)
            lo_row, hi_row = c * SL, (c + 1) * SL
            a = int(pos[max(0, np.searchsorted(val, lo_row, "left") - 1)])
            b = int(pos[min(len(pos) - 1, np.searchsorted(val, hi_row, "right"))]) + 1
            w = np.asarray(d[a:b]).astype(np.int64)
            keep = w[(w >= lo_row) & (w < hi_row)]
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            np.save(fn + ".tmp.npy", keep); os.replace(fn + ".tmp.npy", fn)
            say(f"  selresp {nm} chunk {c:04d}: window {b - a} elements, {keep.size} rows, sha256(stored) {hashlib.sha256(keep.tobytes()).hexdigest()}")
    json.dump({"present": True, "usable": True, "lists": want, "chunks": chunks}, open(os.path.join(L.DATA, "selresp_done.json"), "w"))
    say(f"selresp: COMPLETE; session bytes {L.BYTES['n'] / 1e9:.3f} GB")
    return 0


def main(A):
    if A.tag == "listcols":
        return listcols(A)
    if A.tag == "index":
        return index(A)
    if A.tag == "selresp":
        return selresp(A)
    return 2
