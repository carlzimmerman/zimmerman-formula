#!/usr/bin/env python3
"""Fetch EVERY per-pixel SINGLE-EPOCH (spectra) DESI DR1 MWS rvtab file (all surveys and programs) for the nside-64 pixels that contain any of our wide-binary components (both pair files).
rvtab only (the rvmod model spectra are skipped).  Destination ~/new_physics/_external_data/desi_mws/rvtab_spectra/ ; manifest rvtab_spectra_manifest.json (size, sha256); resumable."""
import csv, json, os, hashlib, time, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); WB = os.path.join(HERE, "..", "..", "real_research", "data", "widebinaries", "dr3_extract")
OUT = os.path.expanduser("~/new_physics/_external_data/desi_mws/rvtab_spectra"); os.makedirs(OUT, exist_ok=True)
pix = {k: set(v) for k, v in json.load(open(os.path.join(HERE, "desi_mws_pixels_by_survey_program.json"))).items()}
ids = set()
for fn in ("wide_binaries_dr3.csv", "wide_binaries_dr3_elbadryR.csv"):
    for r in csv.DictReader(open(os.path.join(WB, fn))): ids |= {int(r["source_id1"]), int(r["source_id2"])}
ours = {i >> 47 for i in ids}
need = sorted((k.split("/")[0], k.split("/")[1], h) for k, S in pix.items() for h in ours & S)
print("files:", len(need), flush=True)
B = "https://data.desi.lbl.gov/public/dr1/vac/dr1/mws/iron/v1.0/rv_output/240521/healpix/"
def get(t):
    sv, pg, h = t; fn = f"rvtab_spectra-{sv}-{pg}-{h}.fits"; path = os.path.join(OUT, fn)
    if os.path.exists(path) and os.path.getsize(path) > 0: return fn, os.path.getsize(path), None
    u = f"{B}{sv}/{pg}/{h // 100}/{h}/{fn}"; err = None
    for k in range(5):
        try:
            data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read(); open(path, "wb").write(data); return fn, len(data), None
        except Exception as e: err = str(e); time.sleep(1 + 2 * k)
    return fn, 0, err
t0 = time.time(); res = []
with cf.ThreadPoolExecutor(6) as ex:
    for k, r in enumerate(ex.map(get, need)):
        res.append(r)
        if (k + 1) % 250 == 0: print(k + 1, "done", round(time.time() - t0), "s", sum(x[1] for x in res) / 1e6, "MB", flush=True)
bad = [r for r in res if r[2]]; print("failed", len(bad), bad[:5]); print("total MB", sum(r[1] for r in res) / 1e6, "files", len(res), flush=True)
json.dump({fn: dict(bytes=n, sha256=hashlib.sha256(open(os.path.join(OUT, fn), "rb").read()).hexdigest()) for fn, n, e in res if n}, open(os.path.join(HERE, "rvtab_spectra_manifest.json"), "w"), indent=0)
print("DONE", flush=True)
