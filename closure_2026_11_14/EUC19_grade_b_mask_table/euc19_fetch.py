#!/usr/bin/env python3
"""EUC19 fetch: the modelling-circle record of every grade-B lens of sample S that EUC17's table does not hold.

Data step only (owner's go, 2026-11-14: "fetch the rest of the grade-B masks too").  Nothing is graded here.

Lenses: grade B passing EUC1's cuts (EUC1's own `select`), minus those with a mask in
closure_2026_11_13/EUC17_mask_aperture_mass_reread/euc17_masks.csv.
Source: https://euclid-eclipse-lenses.org/files/<lens_model_tile_id>/dataset/info.json  (about 134 bytes each).
One stream, paced, generic client name, three tries.  Raw bodies go to --raw-dir (outside git) with a manifest;
the table euc19_masks.csv (same columns as EUC17's) is written next to this script.

  python3 -I euc19_fetch.py --data-dir <dir with the two ECLIPSE csv files> --raw-dir <new empty dir outside git>
"""
import argparse, csv, hashlib, http.client, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E          # noqa: E402
HOST = "euclid-eclipse-lenses.org"
AGENT = "python-research-client/1.0"
PACE = 0.05
EUC17_TABLE = os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv")
KEYFILE = "eclipse_dr1_catalogue_key_v20261103.csv"


class Stream:
    def __init__(self):
        self.c = None
    def get(self, path):
        status = -1
        for attempt in range(3):
            try:
                if self.c is None:
                    self.c = http.client.HTTPSConnection(HOST, timeout=30)
                self.c.request("GET", path, headers={"User-Agent": AGENT, "Accept": "application/json"})
                r = self.c.getresponse()
                body = r.read()
                if r.status == 200 or r.status in (403, 404, 410):
                    return r.status, body
                status = r.status
            except Exception:
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
    rows, _ = E.load(a.data_dir)          # checks both catalogue hashes
    Bm, _ = E.select(rows, ("B",))
    have = set()
    with open(EUC17_TABLE, newline="") as f:
        for r in csv.DictReader(f):
            if r["has_mask"] == "1":
                have.add(r["unique_identifier"])
    ids = [r["id"] for r in Bm if r["id"] not in have]
    tile = {}
    with open(os.path.join(a.data_dir, KEYFILE), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tile[r["unique_identifier"].strip()] = r["lens_model_tile_id"].strip()
    print("grade B passing EUC1's cuts: %d; already in EUC17's table: %d; to fetch: %d; with a tile id: %d"
          % (len(Bm), len(Bm) - len(ids), len(ids), sum(1 for i in ids if tile.get(i))), flush=True)
    if a.limit:
        ids = ids[:a.limit]
    os.makedirs(a.raw_dir, exist_ok=True)
    s = Stream()
    out_rows, t0, nreq = [], time.time(), 0
    for k, i in enumerate(ids):
        t = tile.get(i, "")
        raw = os.path.join(a.raw_dir, i + ".json")
        status, body = 0, b""
        if not t:
            status = -2
        elif os.path.exists(raw) and os.path.getsize(raw) > 0:
            with open(raw, "rb") as f:
                body = f.read()
            status = 200
        else:
            status, body = s.get("/files/%s/dataset/info.json" % t)
            nreq += 1
            if status == 200:
                with open(raw, "wb") as f:
                    f.write(body)
            time.sleep(PACE)
        rad = c0 = c1 = pix = ""
        ok = False
        if status == 200:
            try:
                d = json.loads(body.decode("utf-8"))
                rad = float(d["mask_radius"]); pix = float(d["pixel_scale"])
                c0, c1 = float(d["mask_centre"][0]), float(d["mask_centre"][1])
                ok = rad > 0.0
            except Exception:
                ok = False
        out_rows.append(dict(unique_identifier=i, lens_model_tile_id=t, http_status=status, has_mask=int(ok),
                             mask_radius_arcsec=rad, mask_centre_0=c0, mask_centre_1=c1, pixel_scale=pix,
                             bytes=len(body), sha256=hashlib.sha256(body).hexdigest() if body else ""))
        if (k + 1) % 500 == 0:
            print("  %5d / %d  (%.0f s, %d requests)" % (k + 1, len(ids), time.time() - t0, nreq), flush=True)
    out = os.path.join(HERE, "euc19_masks.csv" if not a.limit else "euc19_masks_debug.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader(); w.writerows(out_rows)
    with open(os.path.join(a.raw_dir, "MANIFEST.txt"), "w") as f:
        f.write("EUC19 mask records (grade-B lenses of sample S not in EUC17's table).\n")
        f.write("Source: https://%s/files/<lens_model_tile_id>/dataset/info.json\n" % HOST)
        f.write("One file per lens, named <unique_identifier>.json. sha256 per file in the lane's euc19_masks.csv.\n")
        f.write("Lenses: %d; HTTP 200 with a positive mask radius: %d; total bytes: %d\n"
                % (len(out_rows), sum(r["has_mask"] for r in out_rows), sum(r["bytes"] for r in out_rows)))
    st = {}
    for r in out_rows:
        st[r["http_status"]] = st.get(r["http_status"], 0) + 1
    print("status counts:", st)
    print("with mask: %d of %d; total bytes %d; requests %d; %.0f s"
          % (sum(r["has_mask"] for r in out_rows), len(out_rows), sum(r["bytes"] for r in out_rows), nreq, time.time() - t0))
    print("table:", os.path.basename(out))


if __name__ == "__main__":
    main()
