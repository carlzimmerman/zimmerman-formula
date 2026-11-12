#!/usr/bin/env python3
"""EUC9 common: systems, lens objects, redshift intervals and spectrum-quality prerequisites.

Frozen criteria: FROZEN_CRITERIA.md (commit bea4eacfa8), section 2.  Uses the ECLIPSE files and the tables EUC3 cached
under <data-dir>/nisp_tables/ (MER objects within 3 arcsec of every system, quality and photo-z rows).
"""
import csv, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

TRUTH = ("EUCL-DR1-L015763", 1.3657)
LENS_SEP = 0.6
NPIX_MIN, NDITH_ABOVE = 300, 3

def fl(v):
    try: return float(v)
    except Exception: return float("nan")

def read_tab(tdir, key):
    rows = []
    for fn in sorted(os.listdir(tdir)):
        if fn.endswith(".csv") and (fn.startswith(key + "_first_") or fn.startswith(key + "_rest_")):
            with open(os.path.join(tdir, fn), newline="") as f: rows.extend(csv.DictReader(f))
    return rows

def build(data_dir, quiet=True):
    """every system of the lens side (sample S and the truth lens) and of the null (grade X), with its lens object,
    Einstein radius, redshift interval and whether its spectrum passes the quality prerequisites"""
    if quiet: E.P = lambda s="": None
    rows, _ = E.load(data_dir)
    key = {r["id"]: r for r in rows}
    obj = {}
    with open(os.path.join(data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): obj[r["Unique_Identifier"]] = r
    Pm, _ = E.select(rows, ("A",)); Sm, _ = E.select(rows, ("A", "B"))
    inP, inS = {r["id"] for r in Pm}, {r["id"] for r in Sm}
    x_ids = sorted(i for i, o in obj.items() if o["Expert_Grade"].strip() == "X")
    S_sorted = sorted(Sm, key=lambda r: r["id"])
    thE = {r["id"]: r["tE"] for r in Sm}; thE[TRUTH[0]] = key[TRUTH[0]]["tE"]
    for j, i in enumerate(x_ids): thE[i] = S_sorted[(j * len(S_sorted)) // len(x_ids)]["tE"]       # as EUC3 section 2
    tdir = os.path.join(data_dir, "nisp_tables")
    sysrow = {}
    with open(os.path.join(tdir, "systems.csv"), newline="") as f:
        for r in csv.DictReader(f): sysrow[int(r["sid"])] = r
    want = set(inS) | {TRUTH[0]} | set(x_ids)
    near = {}
    for r in read_tab(tdir, "mer"):
        s = sysrow[int(r["sid"])]; lid = s["unique_identifier"]
        if lid not in want: continue
        ra0, de0 = float(s["ra"]), float(s["dec"])
        sep = 3600.0 * math.hypot((fl(r["ra"]) - ra0) * math.cos(math.radians(de0)), fl(r["dec"]) - de0)
        if lid not in near or sep < near[lid][0]: near[lid] = (sep, int(r["object_id"]), fl(r["flux_h_templfit"]))
    qual, phz = {}, {}
    for r in read_tab(tdir, "qual"): qual.setdefault(int(r["object_id"]), []).append(r)
    for r in read_tab(tdir, "phz"): phz.setdefault(int(r["object_id"]), []).append(r)
    SYS = {}
    for lid in sorted(want):
        d = dict(id=lid, grade=obj[lid]["Expert_Grade"].strip(), inP=lid in inP, inS=lid in inS, isX=obj[lid]["Expert_Grade"].strip() == "X",
                 thE=thE[lid], oid=None, why="")
        n = near.get(lid)
        if n is None or n[0] > LENS_SEP: d["why"] = "no lens object"; SYS[lid] = d; continue
        d["oid"] = n[1]; d["fh"] = n[2]
        zs = obj[lid]["desi_deflector_specz"].strip()
        if zs and fl(zs) > 0: iv = (fl(zs) - 0.01, fl(zs) + 0.01, "DESI")
        else:
            los, his, src = [], [], []
            k = key.get(lid)
            if k is not None and k["zlo"] > 0 and k["zhi"] > 0 and k["zhi"] >= k["zlo"]: los.append(k["zlo"]); his.append(k["zhi"]); src.append("ECLIPSE")
            for p in phz.get(n[1], []):
                lo, hi = fl(p["phz_70_int_1"]), fl(p["phz_70_int_2"])
                if lo == lo and hi == hi and lo >= 0 and hi > 0 and hi >= lo: los.append(lo); his.append(hi); src.append("PHZ")
            iv = (min(los), max(his), "+".join(sorted(set(src)))) if los else None
        if iv is None: d["why"] = "no redshift interval"; SYS[lid] = d; continue
        d["zlo"], d["zup"], d["zsrc"] = iv
        q = qual.get(n[1], [])
        okq = [r for r in q if fl(r["spe_npix"]) >= NPIX_MIN and fl(r["spe_n_dith_med"]) > NDITH_ABOVE
               and int(fl(r["spe_error_flag"])) == 0 and int(fl(r["spe_gal_error_flag"])) == 0]
        if not okq: d["why"] = "no spectrum passing the quality prerequisites"; SYS[lid] = d; continue
        d["target"] = True
        SYS[lid] = d
    return dict(SYS=SYS, rows=rows, key=key, obj=obj, Pm=Pm, Sm=Sm, inP=inP, inS=inS, x_ids=x_ids)
