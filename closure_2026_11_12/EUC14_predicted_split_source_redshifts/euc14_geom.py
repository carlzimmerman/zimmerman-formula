#!/usr/bin/env python3
"""EUC14 geometry: position angle per dither (ESA dr1.raw_frame `pa` by pointing id) and the projection of a sky offset
on each dither's dispersion direction."""
import csv, math, os
import numpy as np
import euc14_core as C

def load_pa(data_dir):
    """pointing id -> (pa, ra, dec, grism) from the NISP spectroscopic frames; rows of one pointing must agree"""
    out, bad = {}, set()
    with open(os.path.join(data_dir, "euc14", "pa_table.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["grism_wheel_pos"] not in C.POS: continue
            k = int(r["pointing_id"]); v = (float(r["pa"]), float(r["ra"]), float(r["dec"]), r["grism_wheel_pos"])
            if k in out and (abs(out[k][0] - v[0]) > 0.01 or out[k][3] != v[3]): bad.add(k)
            out.setdefault(k, v)
    for k in bad: out.pop(k, None)
    return out

def tan_offset(ra, de, ra0, de0):
    """offset (east, north) in arcsec of (ra, de) from (ra0, de0), tangent plane at (ra0, de0)"""
    xi, eta = C.tangent(ra, de, ra0, de0)
    return np.array([math.degrees(xi) * 3600.0, math.degrees(eta) * 3600.0])

def dither_dirs(raw, PA, conv, ra, de):
    """unit vector (east, north) of increasing wavelength for every dither, nan where the pointing has no frame or the
    grism disagrees"""
    U = np.full((len(raw["dptg"]), 2), np.nan)
    for i, (p, g, t) in enumerate(zip(raw["dptg"], raw["dpos"], raw["dtilt"])):
        v = PA.get(int(p))
        if v is None or v[3] != str(g).strip() or not np.isfinite(t): continue
        U[i] = C.unit(C.dispersion_pa(v[0], g, float(t), conv, ra, de, v[1], v[2]))
    return U

def proj(U, off):
    return U @ np.asarray(off, float)

CONVS = [(c0, st) for c0 in (0.0, 90.0, 180.0, 270.0) for st in (1.0, -1.0, 0.0)]
