#!/usr/bin/env python3
"""EUC2 fetch: public DESI DR1 spectra at the positions of Euclid's strong lenses (NOIRLab SPARCL, anonymous).

Frozen criteria: FROZEN_CRITERIA.md (commit 364e9d08c9), section 1.
  flagged   = every ECLIPSE row with a desi_deflector_specz (any grade)
  extension = every lens of EUC1's sample S that is not flagged
For each lens: every DESI-DR1 spectrum within 1.5 arcsec.  Spectra go to <data-dir>/desi_spectra/ (outside git);
the match table euc2_matches.csv is written next to this script.

Run:  python3 -I euc2_fetch.py --data-dir <dir with the two ECLIPSE csv files>
Resumable: finished position searches and retrieved spectra are skipped.  One request stream, paced; a 429 from the
service is obeyed (wait, then slower).  --stage flagged does the flagged lenses only.
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

API = "https://astrosparcl.datalab.noirlab.edu/api"
UA = {"User-Agent": "generic-client", "Content-Type": "application/json"}
RAD = 1.5 / 3600.0
OUTF = ["sparcl_id", "specid", "ra", "dec", "redshift", "redshift_err", "redshift_warning", "spectype", "specprimary",
        "targetid", "survey", "program", "healpix"]
INC = "sparcl_id,specid,flux,ivar,wavelength,model,mask,wave_sigma"

PACE = [0.6]      # seconds between requests; raised when the service answers 429 (too many requests)

def post(url, payload, tries=12, timeout=120):
    for k in range(tries):
        time.sleep(PACE[0])
        try:
            r = requests.post(url, json=payload, headers=UA, timeout=timeout)
            if r.status_code == 200: return r.json()
            err = "HTTP %d" % r.status_code
            if r.status_code == 429:           # the service's rate limit: wait as told, then go slower
                wait = float(r.headers.get("Retry-After", 60) or 60)
                PACE[0] = min(PACE[0] * 1.5, 5.0)
                print("  429 from the service: waiting %.0f s, pace now %.1f s" % (wait, PACE[0]), flush=True)
                time.sleep(min(wait, 600.0)); continue
        except Exception as ex:
            err = type(ex).__name__
        time.sleep(5.0 * (k + 1))
    raise RuntimeError("request failed: %s" % err)

def find_one(t):
    lid, ra, dec = t
    dra = RAD / max(math.cos(math.radians(dec)), 1e-3)
    res = post(API + "/find/?limit=50", dict(outfields=OUTF, search=[["data_release", "DESI-DR1"],
               ["ra", ra - dra, ra + dra], ["dec", dec - RAD, dec + RAD]]))
    out = []
    for rec in res[1:]:
        sep = 3600.0 * math.hypot((rec["ra"] - ra) * math.cos(math.radians(dec)), rec["dec"] - dec)
        if sep <= 1.5:
            rec = dict(rec); rec["sep_arcsec"] = sep; out.append(rec)
    return lid, out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--stage", default="all", choices=("flagged", "all"))
    a = ap.parse_args()
    sdir = os.path.join(a.data_dir, "desi_spectra"); os.makedirs(sdir, exist_ok=True)
    rows, _ = E.load(a.data_dir)
    Sm, _ = E.select(rows, ("A", "B")); Pm, _ = E.select(rows, ("A",))
    inS = {r["id"] for r in Sm}; inP = {r["id"] for r in Pm}
    obj = {}
    with open(os.path.join(a.data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): obj[r["Unique_Identifier"]] = r
    targets = {}
    for lid, o in obj.items():
        flagged = bool(o["desi_deflector_specz"].strip())
        if flagged or lid in inS:
            targets[lid] = dict(ra=float(o["RA_obj"]), dec=float(o["DEC_obj"]), grade=o["Expert_Grade"].strip(), flagged=flagged,
                                zcat=o["desi_deflector_specz"].strip(), inP=lid in inP, inS=lid in inS)
    nfl = sum(t["flagged"] for t in targets.values())
    print("targets: %d (flagged %d, extension %d)" % (len(targets), nfl, len(targets) - nfl), flush=True)

    cache_p = os.path.join(sdir, "_find_cache.json")
    cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    todo = [(lid, t["ra"], t["dec"]) for lid, t in sorted(targets.items(), key=lambda kv: not kv[1]["flagged"])
            if lid not in cache and (a.stage == "all" or t["flagged"])]
    print("position searches to run: %d (one stream, paced)" % len(todo), flush=True)
    t0 = time.time(); done = 0
    for t in todo:
        lid, recs = find_one(t)
        cache[lid] = recs; done += 1
        if done % 100 == 0:
            json.dump(cache, open(cache_p, "w")); print("  %d / %d  (%.0f s)" % (done, len(todo), time.time() - t0), flush=True)
    json.dump(cache, open(cache_p, "w"))

    matches = []
    for lid, t in targets.items():
        for rec in cache.get(lid, []):
            matches.append(dict(unique_identifier=lid, grade=t["grade"], flagged=t["flagged"], in_P=t["inP"], in_S=t["inS"],
                                desi_deflector_specz=t["zcat"], sparcl_id=rec["sparcl_id"], specid=rec["specid"],
                                targetid=rec.get("targetid"), sep_arcsec="%.3f" % rec["sep_arcsec"], z_desi=rec["redshift"],
                                z_err=rec.get("redshift_err"), zwarn=rec["redshift_warning"], spectype=rec["spectype"],
                                specprimary=rec["specprimary"], survey=rec.get("survey"), program=rec.get("program"),
                                healpix=rec.get("healpix")))
    with open(os.path.join(HERE, "euc2_matches.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(matches[0].keys())); w.writeheader(); w.writerows(matches)
    nl = len({m["unique_identifier"] for m in matches})
    print("spectra matched: %d on %d lenses (flagged lenses with a spectrum: %d; extension lenses: %d)"
          % (len(matches), nl, len({m["unique_identifier"] for m in matches if m["flagged"]}),
             len({m["unique_identifier"] for m in matches if not m["flagged"]})), flush=True)

    need = [m["sparcl_id"] for m in matches if not os.path.exists(os.path.join(sdir, m["sparcl_id"] + ".npz"))]
    need = sorted(set(need)); print("spectra to retrieve: %d" % len(need), flush=True)
    for i in range(0, len(need), 10):
        chunk = need[i:i + 10]
        res = post(API + "/spectras/?include=%s&format=json&dataset_list=DESI-DR1" % INC, chunk, timeout=300)
        for rec in res[1:]:
            np.savez_compressed(os.path.join(sdir, rec["sparcl_id"] + ".npz"),
                                wavelength=np.array(rec["wavelength"], np.float64), flux=np.array(rec["flux"], np.float32),
                                ivar=np.array(rec["ivar"], np.float32), model=np.array(rec["model"], np.float32),
                                mask=np.array(rec["mask"], np.int32), wave_sigma=np.array(rec["wave_sigma"], np.float32))
        print("  retrieved %d / %d" % (min(i + 10, len(need)), len(need)), flush=True)
        time.sleep(0.3)
    have = sum(os.path.exists(os.path.join(sdir, m["sparcl_id"] + ".npz")) for m in matches)
    print("done: %d of %d matched spectra on disk (%.0f s)" % (have, len(matches), time.time() - t0), flush=True)

if __name__ == "__main__":
    main()
