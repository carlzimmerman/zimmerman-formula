"""F1 step 1 (own reader, independent of cfg686_extract.py): stream the KiDS-1000 SOM-gold FITS in small raw-byte chunks
(page cache bypassed on macOS), keep RA, DEC, e1, e2, weight, Z_B for finite rows with weight > 0 and Z_B <= 1.2, and write
them as float32/float64 npy columns sorted by a 0.2 deg sky cell, plus the cell index, into argv[1] (session scratch, not the repo).
Peak RSS < 0.6 GB."""
import os, sys, fcntl, numpy as np
from astropy.io import fits
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(REPO, "..", "_external_data", "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
CELL = 0.2; NRA = int(round(360/CELL))
h = fits.open(F, memmap=True); hd = h[1].header; N = hd["NAXIS2"]; ROW = hd["NAXIS1"]; LOC = h.fileinfo(1)["datLoc"]
_d = h[1].columns.dtype                                    # astropy reports native-order fields; the file is big-endian
dt = np.dtype({"names": list(_d.names), "formats": [_d.fields[n][0].newbyteorder(">") for n in _d.names],
               "offsets": [_d.fields[n][1] for n in _d.names], "itemsize": _d.itemsize})
COLS = {"ra": "RAJ2000", "dec": "DECJ2000", "e1": "e1", "e2": "e2", "w": "weight", "zb": "Z_B"}
assert dt.itemsize == ROW, (dt.itemsize, ROW)
_chk = {k: np.asarray(h[1].data[v][:5], float) for k, v in COLS.items()}; h.close()
step = 40000; tmp = {k: open(os.path.join(OUT, f"_tmp_{k}.bin"), "wb") for k in list(COLS) + ["cell"]}
nkeep = 0
with open(F, "rb", buffering=0) as fh:
    try: fcntl.fcntl(fh.fileno(), getattr(fcntl, "F_NOCACHE", 48), 1)
    except OSError: pass
    fh.seek(LOC); buf = bytearray(step*ROW)
    for i in range(0, N, step):
        n = min(step, N - i); mv = memoryview(buf)[:n*ROW]; got = fh.readinto(mv); assert got == n*ROW
        rec = np.frombuffer(mv, dtype=dt, count=n)
        if i == 0: assert all(np.allclose(rec[v][:5].astype(float), _chk[k], equal_nan=True) for k, v in COLS.items()), "byte order"
        c = {k: rec[v].astype(np.float64) for k, v in COLS.items()}
        ok = np.isfinite(c["ra"]) & np.isfinite(c["dec"]) & np.isfinite(c["e1"]) & np.isfinite(c["e2"]) & (c["w"] > 0) & (c["zb"] <= 1.2)
        cell = (np.floor((c["dec"][ok] + 90)/CELL).astype(np.int64)*NRA + np.floor((c["ra"][ok] % 360)/CELL).astype(np.int64)).astype(np.int32)
        for k in COLS: tmp[k].write(c[k][ok].astype(np.float64 if k in ("ra", "dec") else np.float32).tobytes())
        tmp["cell"].write(cell.tobytes()); nkeep += int(ok.sum())
        if (i//step) % 50 == 0: print(f"  {i+n:,}/{N:,} kept {nkeep:,}", flush=True)
for f in tmp.values(): f.close()
cell = np.fromfile(os.path.join(OUT, "_tmp_cell.bin"), np.int32); order = np.argsort(cell, kind="stable")
np.save(os.path.join(OUT, "cell.npy"), cell[order]); del cell
for k in COLS:
    dtp = np.float64 if k in ("ra", "dec") else np.float32
    a = np.fromfile(os.path.join(OUT, f"_tmp_{k}.bin"), dtp); np.save(os.path.join(OUT, f"{k}.npy"), a[order]); del a
    os.remove(os.path.join(OUT, f"_tmp_{k}.bin"))
os.remove(os.path.join(OUT, "_tmp_cell.bin"))
print(f"rows {N:,} kept {nkeep:,} (finite, w > 0, Z_B <= 1.2)")
