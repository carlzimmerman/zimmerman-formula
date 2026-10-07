#!/usr/bin/env python3
"""CFG445 fetch: WALLABY kinematic + source catalogues (CADC youcat TAP) and 2MASS XSC rows (VizieR asu-tsv cone, 20 arcsec)
for every unique WALLABY kinematic galaxy.  Writes data/ and appends FETCH_LOG.md (URL, date, bytes, sha256).
Criteria: FROZEN_CRITERIA.md (a1a2a05ac).  Run once; re-running overwrites data/ and rewrites FETCH_LOG.md."""
import csv
import datetime
import hashlib
import os
import subprocess
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
TAP = "https://ws-uv.canfar.net/youcat/sync"
LOG = []


def curl(url, out):
    for k in range(4):
        r = subprocess.run(["curl", "-s", "-m", "110", "-o", out, url])
        if r.returncode == 0 and os.path.getsize(out) > 0:
            return
        time.sleep(3)
    raise RuntimeError("fetch failed: " + url)


def log(fn, url):
    b = open(fn, "rb").read()
    LOG.append((os.path.relpath(fn, HERE), url, len(b), hashlib.sha256(b).hexdigest()))


for t in ("Wallaby_dr2_kinematic_catalogue", "Wallaby_dr2_source_catalogue"):
    q = urllib.parse.urlencode(dict(LANG="ADQL", FORMAT="csv", QUERY=f"SELECT * FROM cirada.{t}"))
    url = TAP + "?" + q
    fn = os.path.join(DATA, t.lower() + ".csv")
    curl(url, fn)
    log(fn, url)

rows = list(csv.DictReader(open(os.path.join(DATA, "wallaby_dr2_kinematic_catalogue.csv"))))
pos = {}
for r in rows:
    pos[r["name"]] = (float(r["ra"]), float(r["dec"]))
xfn = os.path.join(DATA, "xsc_wallaby_cones.tsv")
tmp = os.path.join(DATA, "_xsc_tmp.tsv")
with open(xfn, "w", encoding="utf-8") as fo:
    fo.write("# 2MASS XSC (VizieR VII/233/xsc) cone 20 arcsec around each WALLABY kinematic galaxy; one block per galaxy\n")
    fo.write("# URL pattern: https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=VII/233/xsc&-c=<ra>,<dec>&-c.rs=20"
             "&-out=_r,2MASX,RAJ2000,DEJ2000,K.ext,e_K.ext,Kr.eff,r.ext&-sort=_r\n")
    fo.write("wallaby_name\t_r\t2MASX\tRAJ2000\tDEJ2000\tK.ext\te_K.ext\tKr.eff\tr.ext\n")
    for n in sorted(pos):
        ra, de = pos[n]
        url = ("https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=VII/233/xsc&-c=" + f"{ra:.6f},{de:+.6f}"
               + "&-c.rs=20&-out=_r,2MASX,RAJ2000,DEJ2000,K.ext,e_K.ext,Kr.eff,r.ext&-sort=_r")
        curl(url.replace("+", "%2B"), tmp)
        hdr, st = None, 0
        for line in open(tmp, encoding="utf-8", errors="replace"):
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if hdr is None:
                hdr = f
                continue
            if st < 2:
                st += 1
                continue
            fo.write(n + "\t" + "\t".join(x.strip() for x in f) + "\n")
        time.sleep(0.2)
os.remove(tmp)
log(xfn, "VizieR VII/233/xsc cones (pattern in file header), %d galaxies" % len(pos))

today = datetime.date.today().isoformat()
with open(os.path.join(HERE, "FETCH_LOG.md"), "w", encoding="utf-8") as fh:
    fh.write("# CFG445 FETCH_LOG\n\nFetched %s by cfg445_fetch.py (curl). Owner-approved data fetch for this lane. sha256 of the file as saved.\n\n" % today)
    fh.write("| file (lane-relative) | URL | bytes | sha256 |\n|---|---|---|---|\n")
    for fn, url, nb, sh in LOG:
        fh.write(f"| {fn} | {url} | {nb} | {sh} |\n")
    fh.write("\nReused read-only (not refetched): CFG393_group_catalogue_rar/data/{kt2017_table2,kt2017_table3,t15_table3}.tsv, "
             "CFG393's cfg393_match_table.csv, and campaign_fresh_gravity/_external_data/cfg393/t15_table5.tsv "
             "(sha256 1cbe2e33aa6a1c79ce93fb968b7f17e5682255c5d6d46f21a6f85afb2877f292, CFG393 FETCH_LOG).\n")
print("done", LOG)
