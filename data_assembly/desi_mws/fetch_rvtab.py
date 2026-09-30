#!/usr/bin/env python3
"""Fetch the per-pixel DESI DR1 MWS rvtab files (rv_output/240520/healpix/main/{bright,backup}/<hpx//100>/<hpx>/rvtab_coadd-main-<program>-<hpx>.fits) for the nside-64 pixels that hold
our window stars (G 16-19.2 in main-bright pixels, G 11-19.2 in main-backup pixels).  Files go to ~/new_physics/_external_data/desi_mws/rvtab/ ; a manifest with size and sha256 is written.  8 threads, retries."""
import csv, glob, json, os, hashlib, time, urllib.request, urllib.error, concurrent.futures as cf, numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); WB = os.path.join(HERE, "..", "..", "real_research", "data", "widebinaries", "dr3_extract")
OUT = os.path.expanduser("~/new_physics/_external_data/desi_mws/rvtab"); os.makedirs(OUT, exist_ok=True)
pix = {k: set(v) for k, v in json.load(open(os.path.join(HERE, "desi_mws_pixels_by_survey_program.json"))).items()}
ids = set()
for fn in ("wide_binaries_dr3.csv", "wide_binaries_dr3_elbadryR.csv"):
    for r in csv.DictReader(open(os.path.join(WB, fn))): ids |= {int(r["source_id1"]), int(r["source_id2"])}
G = {}
for f in sorted(glob.glob(os.path.join(WB, "chunk_*.fits"))):
    d = fits.open(f, memmap=True)[1].data; sid = np.array(d["source_id"]); m = np.isin(sid, list(ids))
    for i in np.where(m)[0]: G[int(sid[i])] = float(d["phot_g_mean_mag"][i])
need = {("bright", i >> 47) for i in ids if 16 <= G[i] < 19.2 and (i >> 47) in pix["main/bright"]} | {("backup", i >> 47) for i in ids if 11 <= G[i] < 19.2 and (i >> 47) in pix["main/backup"]}
need = sorted(need); print("files to fetch:", len(need), "bright", sum(1 for p, h in need if p == "bright"), "backup", sum(1 for p, h in need if p == "backup"), flush=True)
B = "https://data.desi.lbl.gov/public/dr1/vac/dr1/mws/iron/v1.0/rv_output/240520/healpix/main/"
def get(pg_h):
    pg, h = pg_h; fn = f"rvtab_coadd-main-{pg}-{h}.fits"; path = os.path.join(OUT, fn)
    if os.path.exists(path) and os.path.getsize(path) > 0: return fn, os.path.getsize(path), None
    u = f"{B}{pg}/{h // 100}/{h}/{fn}"
    for k in range(5):
        try:
            data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read(); open(path, "wb").write(data); return fn, len(data), None
        except Exception as e: err = str(e); time.sleep(1 + 2 * k)
    return fn, 0, err
t0 = time.time(); res = []
with cf.ThreadPoolExecutor(8) as ex:
    for k, r in enumerate(ex.map(get, need)):
        res.append(r)
        if (k + 1) % 200 == 0: print(k + 1, "done", round(time.time() - t0), "s", flush=True)
bad = [r for r in res if r[2]]; print("failed:", len(bad), bad[:3]); tot = sum(r[1] for r in res); print("total bytes", tot, "files", len(res))
man = {fn: dict(bytes=n, sha256=hashlib.sha256(open(os.path.join(OUT, fn), "rb").read()).hexdigest()) for fn, n, e in res if n}
json.dump(man, open(os.path.join(HERE, "rvtab_manifest.json"), "w"), indent=0)
