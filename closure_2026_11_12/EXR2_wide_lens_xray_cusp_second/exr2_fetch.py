#!/usr/bin/env python3
"""EXR2 fetch.  Frozen criteria: FROZEN_CRITERIA.md (commit 512015c599).

Asks the eRODat upper-limit service for counts, background and exposure at ESZ1's wide lenses, ESZ1's controls and
8 offsets 0.3 deg from each (bands 022 and 024, DR1 eRASS1), for the DR2 three-survey limit at the wide lenses
(band 024), and fetches the catalogue sources of check K2 with their look-ups.  One stream, 1.5 s between requests.
Raw answers go to --cache-dir (outside git); a manifest is written beside this script.

  python3 -I exr2_fetch.py --data-dir <ECLIPSE csv dir> --cache-dir <dir outside git>
"""
import argparse, csv, datetime, hashlib, io, json, math, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
UL = "https://erosita.mpe.mpg.de/erodat/upperlimit/service_multi"
SCS = "https://erosita.mpe.mpg.de/erodat/catalogue/SCS"
HDR = {"User-Agent": "python-requests"}
FIELDS = [(35.0, -45.0), (45.0, -35.0), (50.0, -50.0), (60.0, -40.0), (65.0, -55.0), (75.0, -45.0), (80.0, -35.0), (55.0, -30.0)]
PAUSE = 1.5

def offsets(ra, dec, rad=0.3):
    out = []
    for k in range(8):
        ph = math.radians(45.0 * k)
        out.append(((ra + rad * math.sin(ph) / math.cos(math.radians(dec))) % 360.0, dec + rad * math.cos(ph)))
    return out

def targets(data_dir):
    """ESZ1's wide lenses and ESZ1's controls, with positions; W first, each list in ESZ1's file order."""
    key = {}
    with open(os.path.join(data_dir, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): key[r["unique_identifier"]] = (float(r["ra"]), float(r["dec"]))
    rows = list(csv.DictReader(open(os.path.join(HERE, "..", "ESZ1_wide_lens_gas_pressure", "esz1_per_lens.csv"))))
    W = [r["unique_identifier"] for r in rows if r["is_W"] == "1"]
    C = [(r["unique_identifier"], r["control_of"]) for r in rows if r["control_of"]]
    T = [dict(id=i, cls="W", pair=i, ra=key[i][0], dec=key[i][1]) for i in W]
    T += [dict(id=i, cls="C", pair=w, ra=key[i][0], dec=key[i][1]) for i, w in C]
    return T

def positions(T):
    P = []
    for t in T:
        P.append(dict(id=t["id"], cls=t["cls"], k=0, ra=t["ra"], dec=t["dec"]))
        for k, (a, d) in enumerate(offsets(t["ra"], t["dec"])): P.append(dict(id=t["id"], cls=t["cls"], k=k + 1, ra=a, dec=d))
    return P

MAN = []
def save(cache, name, content, url, method, n):
    with open(os.path.join(cache, name), "wb") as f: f.write(content)
    MAN.append(dict(file=name, url=url, method=method, lookups=n, bytes=len(content), sha256=hashlib.sha256(content).hexdigest(),
                    utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("  %-28s %9d bytes  %6d look-ups" % (name, len(content), n), flush=True)

def post(cache, name, query):
    path = os.path.join(cache, name)
    if os.path.exists(path):
        c = open(path, "rb").read(); save(cache, name, c, UL, "POST (cached)", len(query)); return json.loads(c)
    time.sleep(PAUSE)
    r = requests.post(UL, json=query, headers=HDR, timeout=600)
    if r.status_code != 200: sys.exit("%s: HTTP %d" % (name, r.status_code))
    res = r.json()
    if str(res.get("error")) != "None" or len(res.get("limits", [])) != len(query): sys.exit("%s: service error %s" % (name, res.get("error")))
    save(cache, name, r.content, UL, "POST", len(query))
    with open(os.path.join(cache, name.replace(".json", "_query.json")), "w") as f: json.dump(query, f)
    return res

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--cache-dir", required=True); a = ap.parse_args()
    os.makedirs(a.cache_dir, exist_ok=True)
    T = targets(a.data_dir); P = positions(T)
    print("targets %d (W %d, C %d); positions %d" % (len(T), sum(t["cls"] == "W" for t in T), sum(t["cls"] == "C" for t in T), len(P)))
    for band in ("022", "024"):
        post(a.cache_dir, "ul_dr1_%s.json" % band, [dict(ra=p["ra"], dec=p["dec"], band=band, dr_survey="DR1_eRASS1") for p in P])
    post(a.cache_dir, "ul_dr2_024.json", [dict(ra=t["ra"], dec=t["dec"], band="024", dr_survey="DR2_eRASSc3") for t in T if t["cls"] == "W"])
    # check K2: catalogue sources in eight fixed fields
    from astropy.io.votable import parse_single_table
    src = {}
    for j, (ra, de) in enumerate(FIELDS):
        name = "cone_%d.xml" % j; path = os.path.join(a.cache_dir, name); url = "%s?CAT=DR1_Main&RA=%s&DEC=%s&SR=1.0&VERB=3" % (SCS, ra, de)
        if os.path.exists(path): c = open(path, "rb").read(); save(a.cache_dir, name, c, url, "GET (cached)", 1)
        else:
            time.sleep(PAUSE); r = requests.get(url, headers=HDR, timeout=600)
            if r.status_code != 200: sys.exit("%s: HTTP %d" % (name, r.status_code))
            c = r.content; save(a.cache_dir, name, c, url, "GET", 1)
        t = parse_single_table(io.BytesIO(c)).to_table()
        for row in t:
            fl = float(row["ml_flux_1"]); ex = float(row["ext"])
            if ex == 0.0 and 1.0e-13 <= fl <= 1.0e-12:
                src[str(row["detuid"])] = dict(detuid=str(row["detuid"]), ra=float(row["ra"]), dec=float(row["dec"]), ml_flux_1=fl, det_like_0=float(row["det_like_0"]), field=j)
    S = [src[k] for k in sorted(src)]
    with open(os.path.join(a.cache_dir, "k2_sources.json"), "w") as f: json.dump(S, f)
    print("K2 sources (ext = 0, ml_flux_1 in 1e-13..1e-12): %d" % len(S))
    q = [dict(ra=s["ra"], dec=s["dec"], band="024", dr_survey="DR1_eRASS1") for s in S] + [dict(ra=s["ra"], dec=s["dec"] + 0.1, band="024", dr_survey="DR1_eRASS1") for s in S]
    post(a.cache_dir, "ul_k2_024.json", q)
    json.dump(dict(lane="EXR2", criteria_commit="512015c599", note="raw answers are kept outside git in the cache directory", requests=MAN,
                   n_targets=len(T), n_positions=len(P), n_k2_sources=len(S)), open(os.path.join(HERE, "exr2_fetch_manifest.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
