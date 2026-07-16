#!/usr/bin/env python3
"""
_mmu.py -- shared loader for the MultimodalUniverse/manga HF dataset (SCOUT lane).

MMU stores every DAP map's `group` and `label` as the *repr of a bytes object*, i.e.
the literal 6-char string  b'stellar_vel'  (quotes and the leading b included).  clean()
undoes that.  All access is via huggingface_hub; if HF is unreachable the caller should
report that plainly (this lane does NOT fabricate).

The MaNGA DAP MAPS datamodel (SDSS DR17) is the schema authority for what each label
means:  https://www.sdss4.org/dr17/manga/manga-data/data-model/  (extensions
STELLAR_VEL, STELLAR_SIGMA, STELLAR_SIGMACORR, EMLINE_GVEL[ha_6564], SPX_ELLCOO,
SPX_MFLUX, SPX_SNR, BINID).  Read-only; no writes to the frozen repo.
"""
import os, numpy as np
import pyarrow.parquet as pq

REPO = "MultimodalUniverse/manga"
NFILES = 12
# 20 galaxies -> (shard, plate-ifu, z) from mmu_access.py census (bad z=-9999 flagged).
SNAP = None  # filled by _snapshot()


def clean(s):
    if isinstance(s, bytes):
        s = s.decode()
    if s.startswith("b'") and s.endswith("'"):
        s = s[2:-1]
    return s


def shard_path(i, download=True):
    """Local path to shard i; downloads via hf_hub_download if needed (cached)."""
    from huggingface_hub import hf_hub_download, HfApi
    fn = f"manga/train-{i:05d}-of-{NFILES:05d}.parquet"
    if download:
        return hf_hub_download(REPO, fn, repo_type="dataset")
    # try cache-only
    return hf_hub_download(REPO, fn, repo_type="dataset", local_files_only=True)


def census(download_meta=True):
    """(shard, plate-ifu, z, spaxel_size) for all rows, via cheap column range-reads."""
    from huggingface_hub import HfFileSystem
    fs = HfFileSystem()
    rows = []
    for i in range(NFILES):
        path = f"datasets/{REPO}/manga/train-{i:05d}-of-{NFILES:05d}.parquet"
        pf = pq.ParquetFile(fs.open(path))
        t = pf.read(columns=["object_id", "z", "spaxel_size"])
        for j in range(t.num_rows):
            rows.append(dict(shard=i, row=j,
                             plateifu=t["object_id"][j].as_py(),
                             z=float(t["z"][j].as_py()),
                             spaxel=float(t["spaxel_size"][j].as_py())))
    return rows


# labels we care about (DAP)
KIN_LABELS = {
    "stellar_vel", "stellar_sigma",
    "stellar_sigmacorr_fit", "stellar_sigmacorr_resolution_difference",
    "emline_gvel_ha_6564", "emline_gsigma_ha_6564",
    "spx_skycoo_on_sky_x", "spx_skycoo_on_sky_y",
    "spx_ellcoo_elliptical_radius", "spx_ellcoo_r/re", "spx_ellcoo_r_h/kpc",
    "spx_ellcoo_elliptical_azimuth",
    "spx_mflux", "spx_snr", "bin_snr",
    "binid_binned_spectra",
}


def load_galaxy(shard_local_path, row):
    """Return dict: meta (object_id,z,spaxel) + {label: (flux2d, ivar2d)} for KIN_LABELS."""
    t = pq.read_table(shard_local_path,
                      columns=["object_id", "z", "spaxel_size", "maps"])
    out = dict(plateifu=t["object_id"][row].as_py(),
               z=float(t["z"][row].as_py()),
               spaxel=float(t["spaxel_size"][row].as_py()),
               maps={})
    maps = t["maps"][row].as_py()
    for m in maps:
        lab = clean(m["label"])
        if lab in KIN_LABELS:
            fl = np.array(m["flux"], dtype=float)
            iv = np.array(m["ivar"], dtype=float) if m["ivar"] is not None else None
            out["maps"][lab] = (fl, iv)
    return out


if __name__ == "__main__":
    rows = census()
    print(f"MMU/{REPO}: {len(rows)} galaxies")
    for r in rows:
        print(f"  shard {r['shard']} row {r['row']} | {r['plateifu']:12s} | z={r['z']:.4f}")
