#!/usr/bin/env python3
"""Download the ALPINE PI-provided FITS products (cube image/flux/psf, moment-0, continuum) of the corpus tier-1 rotators listed in spt0418_products.csv from the ALMA Science Archive (public data, project 2017.1.00428.L).
Destination ~/new_physics/_external_data/spt0418_alma/ ; manifest with size and sha256; resumable; 3 parallel streams."""
import csv, os, hashlib, time, json, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.expanduser("~/new_physics/_external_data/spt0418_alma"); rows = list(csv.DictReader(open(os.path.join(HERE, "spt0418_products.csv"))))
def get(r):
    fn = r["url"].split("/")[-1].split("?")[0]; path = os.path.join(OUT, fn); want = int(r["bytes"] or 0)
    if os.path.exists(path) and os.path.getsize(path) == want and want > 0: return fn, want, None
    err = None
    for k in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(r["url"], headers={"User-Agent": "Mozilla/5.0"}), timeout=300) as resp, open(path, "wb") as fh:
                n = 0
                while True:
                    b = resp.read(1 << 20)
                    if not b: break
                    fh.write(b); n += len(b)
            return fn, n, None if (want == 0 or n == want) else f"size {n} != {want}"
        except Exception as e: err = str(e); time.sleep(2 + 3 * k)
    return fn, 0, err
t0 = time.time(); res = []
with cf.ThreadPoolExecutor(2) as ex:
    for k, x in enumerate(ex.map(get, rows)):
        res.append(x)
        if (k + 1) % 9 == 0: print(k + 1, "of", len(rows), round(time.time() - t0), "s", round(sum(a[1] for a in res) / 1e9, 2), "GB", flush=True)
bad = [x for x in res if x[2]]; print("failed/size-mismatch:", len(bad), bad[:4], "total GB", round(sum(x[1] for x in res) / 1e9, 2))
json.dump({fn: dict(bytes=n, sha256=hashlib.sha256(open(os.path.join(OUT, fn), "rb").read()).hexdigest()) for fn, n, e in res if n}, open(os.path.join(HERE, "spt0418_manifest.json"), "w"), indent=0)
print("DONE", flush=True)
