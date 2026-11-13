"""EUC12 construction A, stage 1: one chunked pass over the DESI DR1 CIGALE catalogue.
Pulls (a) every row whose TARGETID is a chosen EUC5R spectrum of an S lens, (b) every row within 1.5" of an Auger
SLACS lens, (c) the same for the SLACS positions shifted +60" in Dec (K2 null).  Writes euc12_cigale_rows.csv.
Run from the repo root.  Memory: one chunk of ~200k rows x 427 B at a time."""
import math, os, sys
import numpy as np
import pandas as pd
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euc12_common import euclid_chosen, load_slacs_pos

CIG = "../_external_data/desi_dr1_cigale/IronPhysProp_v1.2.fits"
COLS = ["TARGETID", "SURVEY", "PROGRAM", "RA", "DEC", "Z", "CHI2", "LOGM", "LOGM_ERR", "FLAG_MASSPDF",
        "FLUX_Z", "FLUX_W1", "MW_TRANSMISSION_Z", "MW_TRANSMISSION_W1"]
TFORM = {"K": ">i8", "J": ">i4", "I": ">i2", "D": ">f8", "E": ">f4"}


def struct_dtype(hdu):
    names, fmts, offs, o = [], [], [], 0
    for c in hdu.columns:
        f = c.format
        if f.endswith("A"):
            dt, size = f"S{int(f[:-1])}", int(f[:-1])
        else:
            dt = TFORM[f]
            size = np.dtype(dt).itemsize
        names.append(c.name); fmts.append(dt); offs.append(o); o += size
    return np.dtype(dict(names=names, formats=fmts, offsets=offs, itemsize=o))


def main():
    h = fits.open(CIG, memmap=True)
    hdu = h[1]
    dt = struct_dtype(hdu)
    nrow = hdu.header["NAXIS2"]
    assert dt.itemsize == hdu.header["NAXIS1"], (dt.itemsize, hdu.header["NAXIS1"])
    off = hdu._data_offset
    h.close()
    mm = np.memmap(CIG, dtype=dt, mode="r", offset=off, shape=(nrow,))
    eu = euclid_chosen()
    tids = set(int(t) for t in eu.targetid)
    sl = load_slacs_pos()
    sra, sde = np.array([s["ra"] for s in sl]), np.array([s["dec"] for s in sl])
    sets = {"slacs": (sra, sde), "slacs_shift": (sra, sde + 60.0 / 3600.0)}
    out = []
    CH = 200_000
    for i0 in range(0, nrow, CH):
        blk = np.array(mm[i0:i0 + CH][["TARGETID", "RA", "DEC"]])
        tid = blk["TARGETID"].astype(np.int64)
        hit = np.isin(tid, np.fromiter(tids, np.int64))
        idx = list(np.nonzero(hit)[0])
        tag = ["euclid"] * len(idx)
        ra, de = blk["RA"].astype(float), blk["DEC"].astype(float)
        for name, (pr, pd_) in sets.items():
            # coarse box then exact separation
            for k in range(len(pr)):
                if not np.isfinite(pr[k]):
                    continue
                m = (np.abs(de - pd_[k]) < 2.0 / 3600) & (np.abs((ra - pr[k] + 180) % 360 - 180) * math.cos(math.radians(pd_[k])) < 2.0 / 3600)
                for j in np.nonzero(m)[0]:
                    idx.append(j); tag.append(f"{name}:{sl[k]['name']}")
        if idx:
            rows = np.array(mm[i0:i0 + CH])[np.array(idx)]
            for r, t in zip(rows, tag):
                d = {c: (r[c].decode().strip() if isinstance(r[c], bytes) else r[c].item()) for c in COLS}
                d["tag"] = t
                out.append(d)
        if (i0 // CH) % 10 == 0:
            print(f"rows {i0:,}/{nrow:,}  hits so far {len(out)}", flush=True)
    del mm
    pd.DataFrame(out).to_csv(f"{HERE}/euc12_cigale_rows.csv", index=False)
    print("done", len(out))


if __name__ == "__main__":
    main()
