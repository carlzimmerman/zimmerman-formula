#!/usr/bin/env python3
"""
mmu_access.py -- ACCESS + SCHEMA report for the MultimodalUniverse/manga HF dataset.

Confirms (LIVE, via huggingface_hub -- HF access WORKS in this environment):
  - the dataset is hosted as 12 parquet shards (~4.2 GB) holding ONLY 20 galaxies
    (1-2 per shard), NOT the ~10k full MaNGA survey;
  - the per-galaxy schema (object_id=plate-IFU, z, spaxel_size, spaxels[], images[],
    maps[]) and that `maps[].group/.label` are stored as literal bytes-reprs
    (the 6-char string  b'stellar_vel' ), which clean() normalises;
  - the DAP kinematic maps needed by the framework tests are present + populated:
    stellar_vel, stellar_sigma, stellar_sigmacorr_fit, emline_gvel_ha_6564,
    emline_gsigma_ha_6564, and DAP-precomputed deprojected geometry spx_ellcoo
    (elliptical_radius/arcsec, r/re, r_h/kpc, elliptical_azimuth/deg) + spx_mflux weight.

exit 0.  Prints the census + the kinematic-map inventory for one real galaxy.
"""
import sys
import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem
import _mmu

WANT = ["stellar_vel", "stellar_sigma", "stellar_sigmacorr_fit",
        "emline_gvel_ha_6564", "emline_gsigma_ha_6564",
        "spx_ellcoo_elliptical_radius", "spx_ellcoo_r/re", "spx_ellcoo_r_h/kpc",
        "spx_ellcoo_elliptical_azimuth", "spx_mflux", "spx_snr", "bin_snr"]


def main():
    print("=" * 78)
    print("MMU/manga ACCESS + SCHEMA (live via huggingface_hub)")
    print("=" * 78)
    fs = HfFileSystem()
    tot = 0
    print("shards:")
    for i in range(_mmu.NFILES):
        path = f"datasets/{_mmu.REPO}/manga/train-{i:05d}-of-{_mmu.NFILES:05d}.parquet"
        pf = pq.ParquetFile(fs.open(path))
        tot += pf.metadata.num_rows
        print(f"  shard {i:2d}: rows={pf.metadata.num_rows} size={fs.info(path)['size']/1e6:.0f}MB")
    print(f"TOTAL galaxies hosted on HF: {tot}  (full MaNGA survey is ~10,010 -- MMU hosts a SUBSET)")

    print("\ncensus (plate-IFU, z):")
    for c in _mmu.census():
        tag = "  <-- BAD z" if c["z"] < 0 else ""
        print(f"  shard {c['shard']:2d} row {c['row']} | {c['plateifu']:12s} z={c['z']:+.4f}{tag}")

    # kinematic-map inventory for one real galaxy (shard 8 cached first)
    p = _mmu.shard_path(8)
    g = _mmu.load_galaxy(p, 0)
    print(f"\nkinematic-map inventory for {g['plateifu']} (z={g['z']:.4f}):")
    for lab in WANT:
        if lab in g["maps"]:
            fl, iv = g["maps"][lab]
            fin = np.isfinite(fl) & (fl != 0)
            ivn = int(np.sum(np.isfinite(iv) & (iv > 0))) if iv is not None else 0
            rng = (float(fl[fin].min()), float(fl[fin].max())) if fin.any() else (0., 0.)
            print(f"  {lab:32s} present  nonzero={int(fin.sum()):4d} iv>0={ivn:4d}  range %.3g..%.3g" % rng)
        else:
            print(f"  {lab:32s} MISSING")
    print("\nNOTE: no NSA metadata columns (elpetro_th50/ba/sersic_mass/objra/dec) are")
    print("  stored; geometry (Re, inclination, PA) is recovered from the DAP spx_ellcoo")
    print("  maps directly (see pilot_extract.py), or cross-matched externally by plate-IFU.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
