#!/usr/bin/env python3
"""CFG679D probe: HDF5 metadata of the DES Y3 public catalogues by HTTP range requests (no data columns read).
Targeted (a full visititems of the metacal file did not finish in 50 min at the server's ~0.1-0.4 MB/s per connection):
group listings, then shape / dtype / chunking / compression / contiguous offset for the datasets this lane may need.
Output (incremental): cfg679_probe.out, cfg679_probe.json
Run: python3 cfg679_probe.py [key ...]
"""
import json, os, sys, time
import h5py

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import cfg679_lib as L

PLAN = {
    "stellar_mass": ("stellar_mass/DESY3_stellar_mass_catalog.hdf5", [""], []),
    "index": ("y3kp_cats/DESY3_indexcat.h5", ["", "index"],
              ["index/select", "index/select_bin1", "index/select_bin2", "index/select_bin3", "index/select_bin4",
               "index/metacal/select", "index/metacal/select_bin1", "index/metacal/select_bin4"]),
    "metacal": ("y3kp_cats/DESY3_metacal_v03-004.h5", [""],
                [f"catalog/unsheared/{c}" for c in ("ra", "dec", "e_1", "e_2", "R11", "R22", "weight", "flags_select",
                                                            "coadd_object_id", "snr", "size_ratio")]),
    "sompz": ("y3kp_cats/DESY3_sompz_v0.50.h5", ["", "catalog"],
              ["catalog/sompz/unsheared/bhat", "catalog/sompz/unsheared/cell_wide", "catalog/sompz/unsheared/coadd_object_id"]),
    "gold": ("y3kp_cats/DESY3_GOLD_2_2.1.h5", [""],
             [f"catalog/gold/{c}" for c in ("coadd_object_id", "ra", "dec", "sof_cm_mag_corrected_g", "sof_cm_mag_corrected_r",
                                            "sof_cm_mag_corrected_i", "sof_cm_mag_corrected_z", "flags_gold", "extended_class_mash_sof",
                                            "dnf_zmean_sof", "bpz_zmean_sof")]),
}
ONLY = sys.argv[1:] or list(PLAN)
JS = os.path.join(H, "cfg679_probe.json")
OUT = json.load(open(JS)) if os.path.exists(JS) else {}
LOGF = open(os.path.join(H, "cfg679_probe.out"), "a")


def say(s):
    print(s, flush=True); LOGF.write(s + "\n"); LOGF.flush()


def desc(o):
    try:
        off = o.id.get_offset()
    except Exception:
        off = None
    return dict(shape=list(o.shape), dtype=str(o.dtype), chunks=o.chunks, compression=o.compression, offset=off,
                nbytes=int(o.size * o.dtype.itemsize))


for key in ONLY:
    path, groups, dsets = PLAN[key]
    n0, t0 = L.BYTES["n"], time.time()
    f = L.RangeFile(L.BASE + path, block=128 * 1024, nblocks=4096)
    rec = {"path": path, "size": f.size, "groups": {}, "datasets": {}}
    say(f"== {key}: {path} ({f.size / 1e9:.2f} GB)")
    with h5py.File(f, "r") as h:
        for g in groups:
            try:
                obj = h[g] if g else h
                ks = list(obj.keys())
                rec["groups"][g] = ks
                say(f"  [{g or '/'}] {len(ks)} keys: {', '.join(ks[:400])}")
                if key == "stellar_mass":
                    for k in ks:
                        rec["datasets"][k] = desc(obj[k]); say(f"    {k} {rec['datasets'][k]}")
            except Exception as e:
                say(f"  [{g}] ERROR {e!r}")
        for d in dsets:
            try:
                o = h[d]
                if isinstance(o, h5py.Dataset):
                    rec["datasets"][d] = desc(o); say(f"    {d} {rec['datasets'][d]}")
                else:
                    say(f"    {d} is a group: {list(o.keys())[:20]}")
            except Exception as e:
                say(f"    {d} MISSING ({e.__class__.__name__})")
    rec["meta_bytes"] = L.BYTES["n"] - n0
    say(f"  metadata bytes {rec['meta_bytes'] / 1e6:.1f} MB, {time.time() - t0:.0f} s")
    OUT[key] = rec
    json.dump(OUT, open(JS, "w"), indent=1, default=str)
say(f"session probe bytes {L.BYTES['n'] / 1e6:.1f} MB")
