#!/usr/bin/env python3
"""Phase A estimate: how many of our wide-binary components could be in the DESI DR1 MWS?  Inputs (all local or from directory indexes): the pair CSVs, the Gaia chunks (ra, dec, G, Gaia RVS) and the list of HEALPix pixels (nside 64 nested,
equal to Gaia source_id >> 47 and to the DESI HEALPIX column, verified on 8 DESI rows) that hold DESI DR1 MWS per-pixel RV files.  A pixel having a file is necessary, NOT sufficient: DESI observed only a fraction of the targets in each pixel."""
import csv, json, glob, os, numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); WB = os.path.join(HERE, "..", "..", "real_research", "data", "widebinaries", "dr3_extract")
pix = {k: set(v) for k, v in json.load(open(os.path.join(HERE, "desi_mws_pixels_by_survey_program.json"))).items()}
def load_pairs(fn): 
    r = list(csv.DictReader(open(os.path.join(WB, fn)))); return [(int(x["source_id1"]), int(x["source_id2"])) for x in r]
sets = {"wide_binaries_dr3.csv": load_pairs("wide_binaries_dr3.csv"), "wide_binaries_dr3_elbadryR.csv": load_pairs("wide_binaries_dr3_elbadryR.csv")}
need = set(i for p in sets.values() for pr in p for i in pr); print("unique component ids in both files:", len(need))
info = {}
for f in sorted(glob.glob(os.path.join(WB, "chunk_*.fits"))):
    d = fits.open(f, memmap=True)[1].data; sid = np.array(d["source_id"]); m = np.isin(sid, list(need))
    for i in np.where(m)[0]: info[int(sid[i])] = (float(d["ra"][i]), float(d["dec"][i]), float(d["phot_g_mean_mag"][i]), float(d["radial_velocity"][i]), float(d["radial_velocity_error"][i]))
print("components found in the Gaia chunks:", len(info))
allmws = set().union(*pix.values()); main = pix["main/bright"] | pix["main/backup"] | pix["main/dark"]
def stat(name, pairs):
    comp = sorted({i for pr in pairs for i in pr}); n = len(comp); hp = {i: i >> 47 for i in comp}
    rows = {"n_pairs": len(pairs), "n_components": n, "unique_nside64_pixels": len({h for h in hp.values()})}
    for lab, S in (("main-bright", pix["main/bright"]), ("main-backup", pix["main/backup"]), ("main-dark", pix["main/dark"]), ("any main program", main), ("any DESI DR1 MWS pixel (all surveys)", allmws)):
        c = [i for i in comp if hp[i] in S]; rows[f"components in pixel set: {lab}"] = len(c)
        both = sum(1 for a, b in pairs if a >> 47 in S and b >> 47 in S); rows[f"pairs with both in pixel set: {lab}"] = both
    G = {i: info[i][2] for i in comp if i in info}
    gb = lambda lo, hi: [i for i in comp if i in G and lo <= G[i] < hi and hp[i] in pix["main/bright"]]
    rows["components with G in [16,19.2) in main-bright pixels"] = len(gb(16, 19.2)); rows["pairs with both G in [16,19.2) in main-bright pixels"] = sum(1 for a, b in pairs if a in G and b in G and 16 <= G[a] < 19.2 and 16 <= G[b] < 19.2 and a >> 47 in pix["main/bright"] and b >> 47 in pix["main/bright"])
    gbk = lambda i: i in G and 11 <= G[i] < 19.2 and hp[i] in pix["main/backup"]
    rows["components with G in [11,19.2) in main-backup pixels"] = sum(1 for i in comp if gbk(i)); rows["pairs with both G in [11,19.2) in main-backup pixels"] = sum(1 for a, b in pairs if gbk(a) and gbk(b))
    anyc = lambda i: i in G and ((16 <= G[i] < 19.2 and hp[i] in pix["main/bright"]) or (11 <= G[i] < 19.2 and hp[i] in pix["main/backup"]))
    rows["components in (bright G 16-19.2) OR (backup G 11-19.2) windows"] = sum(1 for i in comp if anyc(i)); rows["pairs with both components in those windows"] = sum(1 for a, b in pairs if anyc(a) and anyc(b))
    rv = [i for i in comp if i in info and np.isfinite(info[i][3])]; rows["components with a Gaia DR3 RVS radial_velocity"] = len(rv)
    rows["pairs with both components having Gaia RVS"] = sum(1 for a, b in pairs if a in info and b in info and np.isfinite(info[a][3]) and np.isfinite(info[b][3]))
    rows["G median / 16th-84th percentile"] = [round(float(np.median(list(G.values()))), 2), round(float(np.percentile(list(G.values()), 16)), 2), round(float(np.percentile(list(G.values()), 84)), 2)]
    rows["components with G >= 19.2"] = sum(1 for v in G.values() if v >= 19.2); rows["components with G < 11"] = sum(1 for v in G.values() if v < 11)
    return rows
res = {k: stat(k, v) for k, v in sets.items()}
json.dump(res, open(os.path.join(HERE, "footprint_estimate.json"), "w"), indent=1)
for k, v in res.items():
    print("=====", k)
    for a, b in v.items(): print("  ", a, ":", b)

# ---- extra: where would DESI add a radial velocity that Gaia RVS lacks, and the nearby (parallax > 10 mas) stars ----
import csv as _csv
plx = {}
for f in sorted(glob.glob(os.path.join(WB, "chunk_*.fits"))):
    d = fits.open(f, memmap=True)[1].data; sid = np.array(d["source_id"]); m = np.isin(sid, list(need))
    for i in np.where(m)[0]: plx[int(sid[i])] = float(d["parallax"][i])
ext = {}
for k, pairs in sets.items():
    comp = sorted({i for pr in pairs for i in pr}); hp = {i: i >> 47 for i in comp}
    norv = [i for i in comp if not np.isfinite(info[i][3])]
    win = lambda i: (16 <= info[i][2] < 19.2 and hp[i] in pix["main/bright"]) or (11 <= info[i][2] < 19.2 and hp[i] in pix["main/backup"])
    anymain = lambda i: hp[i] in main
    near = [i for i in comp if plx[i] > 10]
    hasrv_or_desi = lambda i: np.isfinite(info[i][3]) or win(i)
    ext[k] = {"components without Gaia RVS": len(norv), "of those in a DESI bright/backup window": sum(1 for i in norv if win(i)),
              "of those in any main-program pixel (any magnitude)": sum(1 for i in norv if anymain(i)),
              "pairs lacking an RV on at least one component": sum(1 for a, b in pairs if not (np.isfinite(info[a][3]) and np.isfinite(info[b][3]))),
              "pairs where both components would have an RV if DESI supplies the window stars": sum(1 for a, b in pairs if hasrv_or_desi(a) and hasrv_or_desi(b)),
              "pairs with both RVs from Gaia alone": sum(1 for a, b in pairs if np.isfinite(info[a][3]) and np.isfinite(info[b][3])),
              "components with parallax > 10 mas (d < 100 pc)": len(near), "of those in any main-program pixel": sum(1 for i in near if anymain(i)),
              "components with Gaia RV and G < 11 in main pixels (DESI saturates/ not targeted)": sum(1 for i in comp if np.isfinite(info[i][3]) and info[i][2] < 11 and anymain(i))}
json.dump(ext, open(os.path.join(HERE, "footprint_estimate_extra.json"), "w"), indent=1)
for k, v in ext.items():
    print("=====", k)
    for a, b in v.items(): print("  ", a, ":", b)
