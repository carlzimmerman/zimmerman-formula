#!/usr/bin/env python3
"""EUC10 route R1: NED TAP 10-arcsec cones at every ECLIPSE position (criteria 21578af22b, sections 2 and 4).

  python3 -I euc10_fetch_ned.py --cat <ECLIPSE_object_catalogue.csv> --out <dir> [--shift 0.0|0.3]

One paced stream (>= 1 s between requests), generic User-Agent, stops on HTTP 429.  60 cones per query.
Raw rows are written to <out>/ned_cones_shift<shift>.csv (data, never committed).  Resumable: finished batches are
skipped on restart.
"""
import argparse, csv, json, os, sys, time, urllib.parse, urllib.request, urllib.error

URL = "https://ned.ipac.caltech.edu/tap/sync"
UA = {"User-Agent": "generic-research-client/1.0"}
R_DEG = 10.0 / 3600.0
BATCH = 60

def query(adql):
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": adql}).encode()
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL, data=data, headers=UA), timeout=180) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                sys.exit("HTTP 429 from NED: stopping as the criteria require")
            time.sleep(10 * (attempt + 1))
        except Exception:
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("NED query failed four times")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cat", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--shift", type=float, default=0.0)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.cat, newline="", encoding="utf-8")))
    pos = [(r["Unique_Identifier"], float(r["RA_obj"]), float(r["DEC_obj"]) + a.shift) for r in rows]
    tag = "shift%.1f" % a.shift
    outp = os.path.join(a.out, "ned_cones_%s.csv" % tag)
    donep = os.path.join(a.out, "ned_cones_%s.done.json" % tag)
    done = set(json.load(open(donep))) if os.path.exists(donep) else set()
    new = not os.path.exists(outp)
    fo = open(outp, "a", newline="", encoding="utf-8"); w = csv.writer(fo)
    if new:
        w.writerow(["batch", "prefname", "prefphytype", "ra", "dec", "z", "zflag", "z_bibcode"])
    nb = (len(pos) + BATCH - 1) // BATCH
    t0 = time.time()
    for b in range(nb):
        if b in done: continue
        chunk = pos[b * BATCH:(b + 1) * BATCH]
        conds = " OR ".join("CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',%.7f,%.7f,%.7f))=1" % (ra, min(dec, 89.99), R_DEG)
                            for _, ra, dec in chunk)
        txt = query("SELECT prefname,prefphytype,ra,dec,z,zflag,z_bibcode FROM NEDTAP.objdir WHERE (%s)" % conds)
        if not txt.startswith("prefname"):
            raise RuntimeError("unexpected NED response in batch %d: %s" % (b, txt[:300]))
        for rr in list(csv.reader(txt.splitlines()))[1:]:
            w.writerow([b] + rr)
        fo.flush(); done.add(b); json.dump(sorted(done), open(donep, "w"))
        if b % 25 == 0:
            print("batch %d / %d  (%.0f s)" % (b, nb, time.time() - t0), flush=True)
        time.sleep(1.1)
    fo.close()
    print("finished %d batches, %s" % (nb, tag))

if __name__ == "__main__":
    main()
