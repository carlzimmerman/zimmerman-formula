"""X7 step 0a (criteria 40ae8ff09f): own KiDS column cache with the PSF and tile columns.
Streams the KiDS-1000 SOM-gold FITS in raw-byte chunks (page cache bypassed on macOS) with F1's filter (finite RA, DEC, e1, e2;
weight > 0; Z_B <= 1.2) and F1's order (stable sort by a 0.2 deg sky cell), and writes ra, dec, e1, e2, w, zb, cell (as F1's
f1_extract.py) plus psf1, psf2 (PSF_e1, PSF_e2), tile (THELI_NAME -> int32 id) and thelint (THELI_INT) into argv[1]
(session scratch, not the repo). E1: the shared columns are byte-identical to F1's cache (argv[2], optional).
Usage: x7_extract.py <out dir> [<F1 KiDS cache dir>] [--mutate]. Single thread, no network.
--mutate (A5): e2 sign flipped in the written cache (use a separate out dir); E1 must FAIL."""
import os, sys, fcntl, json, hashlib, resource, time, numpy as np
from astropy.io import fits
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
F = os.path.join(REPO, "..", "_external_data", "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; OUT = ARGS[0]; F1C = ARGS[1] if len(ARGS) > 1 else None
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
os.makedirs(OUT, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x7_extract{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
CELL = 0.2; NRA = int(round(360/CELL))
h = fits.open(F, memmap=True); hd = h[1].header; N = hd["NAXIS2"]; ROW = hd["NAXIS1"]; LOC = h.fileinfo(1)["datLoc"]
_d = h[1].columns.dtype
dt = np.dtype({"names": list(_d.names), "formats": [_d.fields[n][0].newbyteorder(">") for n in _d.names],
               "offsets": [_d.fields[n][1] for n in _d.names], "itemsize": _d.itemsize})
COLS = {"ra": "RAJ2000", "dec": "DECJ2000", "e1": "e1", "e2": "e2", "w": "weight", "zb": "Z_B", "psf1": "PSF_e1", "psf2": "PSF_e2"}
assert dt.itemsize == ROW, (dt.itemsize, ROW)
_r5 = h[1].data[:5]                                                     # slice rows first: a full-column access maps the whole file
_chk = {k: np.asarray(_r5[v], float) for k, v in COLS.items()}; _chn = [str(x).strip() for x in _r5["THELI_NAME"]]; del _r5; h.close()
DT = {"ra": np.float64, "dec": np.float64, "e1": np.float32, "e2": np.float32, "w": np.float32, "zb": np.float32, "psf1": np.float32, "psf2": np.float32}
step = 40000; tmp = {k: open(os.path.join(OUT, f"_tmp_{k}.bin"), "wb") for k in list(COLS) + ["cell", "tile", "thelint"]}
TILES = {}; PAIRS = set(); NAMEID = set(); nkeep = 0
with open(F, "rb", buffering=0) as fh:
    try: fcntl.fcntl(fh.fileno(), getattr(fcntl, "F_NOCACHE", 48), 1)
    except OSError: pass
    fh.seek(LOC); buf = bytearray(step*ROW)
    for i in range(0, N, step):
        n = min(step, N - i); mv = memoryview(buf)[:n*ROW]; got = fh.readinto(mv); assert got == n*ROW
        rec = np.frombuffer(mv, dtype=dt, count=n)
        if i == 0:
            assert all(np.allclose(rec[v][:5].astype(float), _chk[k], equal_nan=True) for k, v in COLS.items()), "byte order"
            assert [bytes(x).strip(b"\x00 ").decode("ascii", "replace") for x in rec["THELI_NAME"][:5]] == _chn, "THELI_NAME read"
        c = {k: rec[v].astype(np.float64) for k, v in COLS.items()}
        if MUT: c["e2"] = -c["e2"]
        ok = np.isfinite(c["ra"]) & np.isfinite(c["dec"]) & np.isfinite(c["e1"]) & np.isfinite(c["e2"]) & (c["w"] > 0) & (c["zb"] <= 1.2)
        cell = (np.floor((c["dec"][ok] + 90)/CELL).astype(np.int64)*NRA + np.floor((c["ra"][ok] % 360)/CELL).astype(np.int64)).astype(np.int32)
        names = np.asarray(rec["THELI_NAME"][ok]); un, inv = np.unique(names, return_inverse=True)
        ids = np.array([TILES.setdefault(bytes(u).strip(b"\x00 "), len(TILES)) for u in un], np.int32)[inv]
        ti = np.asarray(rec["THELI_INT"][ok]).astype(np.int32)
        for a, b in set(zip(ids.tolist(), ti.tolist())): PAIRS.add((a, b))
        NAMEID.update((bytes(names[j]).strip(b"\x00 "), int(ids[j])) for j in np.unique(inv, return_index=True)[1])
        for k in COLS: tmp[k].write(c[k][ok].astype(DT[k]).tobytes())
        tmp["cell"].write(cell.tobytes()); tmp["tile"].write(ids.astype(np.int32).tobytes()); tmp["thelint"].write(ti.astype(np.int32).tobytes())
        nkeep += int(ok.sum())
        if (i//step) % 50 == 0: say(f"  {i+n:,}/{N:,} kept {nkeep:,} [{time.time()-T0:.0f} s]")
for f in tmp.values(): f.close()
cell = np.fromfile(os.path.join(OUT, "_tmp_cell.bin"), np.int32); order = np.argsort(cell, kind="stable").astype(np.int32)   # int32 index (memory)
np.save(os.path.join(OUT, "cell.npy"), cell[order]); del cell
for k, dtp in list(DT.items()) + [("tile", np.int32), ("thelint", np.int32)]:
    a = np.fromfile(os.path.join(OUT, f"_tmp_{k}.bin"), dtp); np.save(os.path.join(OUT, f"{k}.npy"), a[order]); del a
    os.remove(os.path.join(OUT, f"_tmp_{k}.bin"))
os.remove(os.path.join(OUT, "_tmp_cell.bin")); del order
json.dump({"tiles": {k.decode(): v for k, v in TILES.items()}}, open(os.path.join(OUT, "tiles.json"), "w"))
say(f"rows {N:,} kept {nkeep:,} (finite, w > 0, Z_B <= 1.2); tiles {len(TILES)}")
RES.update(rows=N, kept=nkeep, ntiles=len(TILES))
# ---------------------------------------------------------------- E1: equality with F1's cache (byte-identical shared columns)
def sha_file(p):
    hh = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 24), b""): hh.update(blk)
    return hh.hexdigest()
if F1C:
    same = {}
    for k in ("ra", "dec", "e1", "e2", "w", "zb", "cell"):
        a, b = sha_file(os.path.join(OUT, f"{k}.npy")), sha_file(os.path.join(F1C, f"{k}.npy")); same[k] = (a == b); RES.setdefault("sha256", {})[k] = a
    check("E1", all(same.values()), f"byte-identical to F1's cache: {same}", "all 7 columns identical")
else:
    check("E1", False, "F1 cache dir not given", "all 7 columns identical")
# ---------------------------------------------------------------- E2: tile mapping one-to-one; PSF finiteness
na = len({a for a, _ in NAMEID}); nb = len({b for _, b in NAMEID}); nti = len({b for _, b in PAIRS})
nbad = 0
for a in range(0, nkeep, 2_000_000):                                    # one map per chunk (bounds the touched-page RSS)
    p1 = np.load(os.path.join(OUT, "psf1.npy"), mmap_mode="r"); p2 = np.load(os.path.join(OUT, "psf2.npy"), mmap_mode="r")
    nbad += int((~(np.isfinite(p1[a:a+2_000_000]) & np.isfinite(p2[a:a+2_000_000]))).sum()); del p1, p2
RES.update(name_id_pairs=len(NAMEID), theli_int_values=nti, nonfinite_psf=nbad)
check("E2", len(NAMEID) == na == nb == len(TILES), f"THELI_NAME/tile-id pairs {len(NAMEID)}, names {na}, ids {nb}; non-finite PSF_e rows {nbad:,}"
      f" (THELI_INT has {nti} values for {len(TILES)} names: not a unique tile key, not used)", "one-to-one")
pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
check("E3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X7_EXTRACT COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x7_extract_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
