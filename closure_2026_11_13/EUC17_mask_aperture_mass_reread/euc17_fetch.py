#!/usr/bin/env python3
"""EUC17 fetch.  Frozen criteria: FROZEN_CRITERIA.md (commit 8b31c449c9), section 1.

For every lens in the union of the four committed per-lens files, fetch the released modelling record
  https://euclid-eclipse-lenses.org/files/<lens_model_tile_id>/dataset/info.json
(one stream, paced, generic client name, three tries).  Raw bodies go to --raw-dir (outside git) with a manifest;
the lane table euc17_masks.csv is written next to this script.

Run:
  python3 -I euc17_fetch.py --data-dir <dir with the two ECLIPSE csv files> --raw-dir <new empty dir outside git>

Nothing is graded here.  The bodies are parsed as JSON and only three keys are read.
"""
import argparse, csv, hashlib, http.client, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
HOST = "euclid-eclipse-lenses.org"
AGENT = "python-research-client/1.0"
PACE = 0.05
SOURCES = [
    ("closure_2026_11_12/EUC1_eclipse_saturation_ceiling/euc1_per_lens.csv", "unique_identifier"),
    ("closure_2026_11_12/EUC4_wide_lenses/euc4_per_lens.csv", "unique_identifier"),
    ("closure_2026_11_13/EUC16_better_arc_finder_source_redshifts/euc16_sources.csv", "unique_identifier"),
    ("closure_2026_11_12/EUC10_published_source_redshifts/euc10_per_lens.csv", "eclipse_id"),
]
KEYFILE = "eclipse_dr1_catalogue_key_v20261103.csv"
KEYSHA = "65338917534c9c767c4f45732d29937d2dfb7fd68083cdfd05aec994ee4fa9ab"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def wanted_ids():
    ids, per = [], {}
    for rel, col in SOURCES:
        with open(os.path.join(REPO, rel), newline="") as f:
            rows = [r[col].strip() for r in csv.DictReader(f)]
        per[os.path.basename(rel)] = len(rows)
        ids.extend(rows)
    seen, out = set(), []
    for i in ids:
        if i and i not in seen:
            seen.add(i); out.append(i)
    return out, per


class Stream:
    def __init__(self):
        self.c = None
    def get(self, path):
        for attempt in range(3):
            try:
                if self.c is None:
                    self.c = http.client.HTTPSConnection(HOST, timeout=30)
                self.c.request("GET", path, headers={"User-Agent": AGENT, "Accept": "application/json"})
                r = self.c.getresponse()
                body = r.read()
                if r.status == 200:
                    return 200, body
                if r.status in (404, 403, 410):
                    return r.status, body
                status = r.status
            except Exception as e:                      # network error: reconnect and retry
                status = -1
                try:
                    self.c.close()
                except Exception:
                    pass
                self.c = None
            time.sleep(1.0 + 2.0 * attempt)
        return status, b""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--limit", type=int, default=0, help="debug: fetch only the first N lenses")
    a = ap.parse_args()
    key = os.path.join(a.data_dir, KEYFILE)
    if sha256_file(key) != KEYSHA:
        print("key catalogue sha256 mismatch"); sys.exit(2)
    tile = {}
    with open(key, newline="") as f:
        for r in csv.DictReader(f):
            tile[r["unique_identifier"].strip()] = r["lens_model_tile_id"].strip()
    ids, per = wanted_ids()
    print("lenses per source file:", per)
    print("union: %d lenses; with a tile id in the key catalogue: %d" % (len(ids), sum(1 for i in ids if tile.get(i))))
    if a.limit:
        ids = ids[:a.limit]
    os.makedirs(a.raw_dir, exist_ok=True)
    s = Stream()
    rows, t0, nfetch = [], time.time(), 0
    for k, i in enumerate(ids):
        t = tile.get(i, "")
        raw = os.path.join(a.raw_dir, i + ".json")
        status, body = 0, b""
        if not t:
            status = -2                                  # no tile id in the key catalogue
        elif os.path.exists(raw) and os.path.getsize(raw) > 0:
            with open(raw, "rb") as f:
                body = f.read()
            status = 200
        else:
            status, body = s.get("/files/%s/dataset/info.json" % t)
            nfetch += 1
            if status == 200:
                with open(raw, "wb") as f:
                    f.write(body)
            time.sleep(PACE)
        rad = cy = cx = pix = ""
        ok = False
        if status == 200:
            try:
                d = json.loads(body.decode("utf-8"))
                rad = float(d["mask_radius"]); pix = float(d["pixel_scale"])
                cy, cx = float(d["mask_centre"][0]), float(d["mask_centre"][1])
                ok = rad > 0.0
            except Exception:
                ok = False
        rows.append(dict(unique_identifier=i, lens_model_tile_id=t, http_status=status, has_mask=int(ok),
                         mask_radius_arcsec=rad, mask_centre_0=cy, mask_centre_1=cx, pixel_scale=pix,
                         bytes=len(body), sha256=hashlib.sha256(body).hexdigest() if body else ""))
        if (k + 1) % 500 == 0:
            print("  %5d / %d  (%.0f s, %d requests)" % (k + 1, len(ids), time.time() - t0, nfetch), flush=True)
    out = os.path.join(HERE, "euc17_masks.csv" if not a.limit else "euc17_masks_debug.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(a.raw_dir, "MANIFEST.txt"), "w") as f:
        f.write("EUC17 mask records. Source: https://%s/files/<lens_model_tile_id>/dataset/info.json\n" % HOST)
        f.write("One file per lens, named <unique_identifier>.json. sha256 per file in the lane's euc17_masks.csv.\n")
        f.write("Lenses: %d; HTTP 200 with a positive mask radius: %d; total bytes: %d\n"
                % (len(rows), sum(r["has_mask"] for r in rows), sum(r["bytes"] for r in rows)))
    st = {}
    for r in rows:
        st[r["http_status"]] = st.get(r["http_status"], 0) + 1
    print("status counts:", st)
    print("with mask: %d of %d; total bytes %d; requests %d; %.0f s"
          % (sum(r["has_mask"] for r in rows), len(rows), sum(r["bytes"] for r in rows), nfetch, time.time() - t0))
    print("table:", os.path.basename(out))


if __name__ == "__main__":
    main()
