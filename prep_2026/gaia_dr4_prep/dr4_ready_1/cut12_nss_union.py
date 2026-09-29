#!/usr/bin/env python3
"""DR4-READY-1, WP4 (offline half): the cut-12 NSS union driven by the release-day manifest (Amendment 15(b), 16(c)).

NEW file.  NO NETWORK.  Reads per-table source-id lists from local files named in the manifest and calls
catalog_builder_dr4/cut12_stub.py's nss_union_flags / pair_nss_flags.  The list of COUNTED tables and the reasons for every
EXCLUDED table must be declared in the manifest BEFORE any id file is opened (cut12_stub refuses an empty list, the
placeholder, unknown tables and unaccounted tables).  Table names are run-time data: DR3 has nss_two_body_orbit,
nss_acceleration_astro, nss_non_linear_spectro, nss_vim_fl; ESA's DR4 page names nss_acceleration_astro,
nss_two_body_orbit, nss_resolved_pair, nss_multiplicity, nss_multiple_orbits, nss_masses (data chat, d9ac3a13f) --
nothing here assumes either list.

load_ids(path)            -> numpy int64 array of source_id from .npz (key 'source_id'), .csv/.txt (column 'source_id'),
                             or .fits (column 'source_id')
run(manifest, pair_ids_a, pair_ids_b) -> (pair flags, report); the report is written back into manifest['cut12_nss']
"""
import sys
sys.dont_write_bytecode = True
import csv
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "catalog_builder_dr4"))
import cut12_stub                                               # read-only


def load_ids(path):
    p = Path(path)
    if p.suffix == ".npz":
        return np.asarray(np.load(p)["source_id"], dtype=np.int64)
    if p.suffix in (".csv", ".txt"):
        with open(p, newline="") as f:
            return np.array([int(r["source_id"]) for r in csv.DictReader(f)], dtype=np.int64)
    if p.suffix in (".fits", ".fit"):
        from astropy.io import fits
        with fits.open(p, memmap=True) as h:
            return np.asarray(h[1].data["source_id"], dtype=np.int64)
    raise ValueError(f"unsupported id file type: {p.name}")


def run(manifest, pair_ids_a, pair_ids_b):
    c12 = manifest["cut12_nss"]
    counted, excluded = c12.get("counted_tables"), c12.get("excluded") or {}
    if not counted:
        raise ValueError("manifest['cut12_nss']['counted_tables'] must be declared before any NSS id file is opened")
    files = c12.get("id_files") or {}
    for t in list(counted) + list(excluded):
        if t not in files:
            raise KeyError(f"no id file declared for table {t!r}")
    ids_by_table = {t: load_ids(files[t]) for t in list(counted) + list(excluded)}
    sids = np.unique(np.concatenate([np.asarray(pair_ids_a, np.int64), np.asarray(pair_ids_b, np.int64)]))
    res = cut12_stub.nss_union_flags(sids, ids_by_table, counted, excluded)
    flag_of = dict(zip(sids.tolist(), np.asarray(res.flag).tolist()))
    pair_flags = np.array([flag_of[int(x)] or flag_of[int(y)] for x, y in zip(pair_ids_a, pair_ids_b)], bool)
    c12["row_counts"] = {t: int(len(v)) for t, v in ids_by_table.items()}
    c12["n_components_flagged"] = int(np.sum(res.flag))
    c12["stub_report"] = res.report
    c12["n_pairs_flagged"] = int(pair_flags.sum())
    return pair_flags, c12
