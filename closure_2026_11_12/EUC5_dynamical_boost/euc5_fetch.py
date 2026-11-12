#!/usr/bin/env python3
"""EUC5 fetch: SDSS DR17 spectroscopic rows (redshift, velocity dispersion) within 1 arcsec of Euclid lenses.

Frozen criteria: FROZEN_CRITERIA.md (commit 7fa4e74869), section 1.  NOIRLab Data Lab TAP, anonymous, paced.
Every lens of EUC1's sample S with Dec > -15 is searched; the quality cuts are applied later, in euc5.py.

Run:  python3 -I euc5_fetch.py --data-dir <dir with the two ECLIPSE csv files>
"""
import argparse, csv, io, math, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
TAP = "https://datalab.noirlab.edu/tap/sync"
COLS = ["specobjid", "ra", "dec", "z", "zerr", "zwarning", "class", "veldisp", "veldisperr", "snmedian", "instrument",
        "survey", "programname", "plate", "mjd", "fiberid", "scienceprimary"]
RAD = 1.0 / 3600.0

def query(adql, tries=6):
    for k in range(tries):
        time.sleep(1.0)
        try:
            r = requests.get(TAP, params=dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=adql),
                             headers={"User-Agent": "generic-client"}, timeout=180)
            if r.status_code == 200 and r.text.lstrip().lower().startswith("specobjid"): return r.text
            if r.status_code == 429: time.sleep(60.0)
            err = "HTTP %d: %s" % (r.status_code, r.text[:200].replace("\n", " "))
        except Exception as ex:
            err = type(ex).__name__
        time.sleep(5.0 * (k + 1))
    raise RuntimeError("TAP query failed: %s" % err)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--batch", type=int, default=30)
    a = ap.parse_args()
    rows, _ = E.load(a.data_dir)
    Sm, _ = E.select(rows, ("A", "B")); ids = {r["id"] for r in Sm}
    pos = {}
    with open(os.path.join(a.data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["Unique_Identifier"] in ids and float(r["DEC_obj"]) > -15.0:
                pos[r["Unique_Identifier"]] = (float(r["RA_obj"]), float(r["DEC_obj"]))
    lens = sorted(pos); print("lenses of S with Dec > -15: %d" % len(lens), flush=True)
    out = []; t0 = time.time()
    for i in range(0, len(lens), a.batch):
        chunk = lens[i:i + a.batch]
        # the service does not translate ADQL CONTAINS for this table: coordinate boxes, then the 1 arcsec cut locally
        cond = " OR ".join("(ra BETWEEN %.7f AND %.7f AND dec BETWEEN %.7f AND %.7f)" % (
            pos[l][0] - RAD / math.cos(math.radians(pos[l][1])), pos[l][0] + RAD / math.cos(math.radians(pos[l][1])),
            pos[l][1] - RAD, pos[l][1] + RAD) for l in chunk)
        txt = query("SELECT %s FROM sdss_dr17.specobj WHERE %s" % (", ".join(COLS), cond))
        for rec in csv.DictReader(io.StringIO(txt)):
            ra, dec = float(rec["ra"]), float(rec["dec"]); best = None
            for l in chunk:
                sep = 3600.0 * math.hypot((ra - pos[l][0]) * math.cos(math.radians(pos[l][1])), dec - pos[l][1])
                if sep <= 1.0 and (best is None or sep < best[1]): best = (l, sep)
            if best: out.append(dict(rec, unique_identifier=best[0], sep_arcsec="%.3f" % best[1]))
        if (i // a.batch) % 10 == 0: print("  %d / %d lenses, %d rows  (%.0f s)" % (min(i + a.batch, len(lens)), len(lens), len(out), time.time() - t0), flush=True)
    with open(os.path.join(HERE, "euc5_sdss_matches.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["unique_identifier", "sep_arcsec"] + COLS); w.writeheader(); w.writerows(out)
    print("done: %d SDSS rows on %d lenses (%.0f s)" % (len(out), len({o["unique_identifier"] for o in out}), time.time() - t0), flush=True)

if __name__ == "__main__":
    main()
