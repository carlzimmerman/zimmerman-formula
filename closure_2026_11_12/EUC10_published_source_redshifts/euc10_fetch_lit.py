#!/usr/bin/env python3
"""EUC10 routes R2 and R3: fetch VizieR tables (CfA mirror, ASU tsv) and primary-literature sources
(arXiv e-print source; Euclid DR1 paper PDF).  Criteria 21578af22b section 2.

  python3 -I euc10_fetch_lit.py --out <dir> {arxiv|euclid|vizier-meta|vizier ID...}

One paced stream per service (>= 3 s for arXiv, >= 1.2 s otherwise), generic User-Agent, stop on HTTP 429.
Every file is appended to <dir>/MANIFEST.txt with URL, bytes, sha256, UTC date and licence note.
"""
import argparse, hashlib, os, sys, time, urllib.request, urllib.error, datetime

UA = {"User-Agent": "generic-research-client/1.0"}
ARXIV = ["2205.05307", "2503.08041", "2602.11068", "2509.15012", "2509.18089", "2509.18086", "2509.18078",
         "2505.16158", "2307.12470", "2503.15324", "2007.09006", "2206.09902", "2603.12810", "1803.07601",
         "1810.04480", "2206.07714", "1711.03971", "2012.10051"]
EUCLID = ["https://pubs.euclid-ec.org/public/dr1/bergamini.pdf"]
VIZ = "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv"
TOTAL_CAP = 200 * 1024 * 1024

def get(url, out, licence):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 429: sys.exit("HTTP 429: stopping")
        print("HTTP %d for %s" % (e.code, url)); return None
    d = os.path.dirname(out)
    # downloads so far = bytes in this MANIFEST + the NED cone files one level up (extracted copies do not count)
    man = os.path.join(d, "MANIFEST.txt")
    tot = sum(int(l.split("\t")[2]) for l in open(man)) if os.path.exists(man) else 0
    up = os.path.dirname(os.path.abspath(d))
    tot += sum(os.path.getsize(os.path.join(up, f)) for f in os.listdir(up) if f.startswith("ned_cones_") and f.endswith(".csv"))
    if tot + len(data) > TOTAL_CAP: sys.exit("download cap of 200 MB would be exceeded: stopping")
    open(out, "wb").write(data)
    with open(os.path.join(d, "MANIFEST.txt"), "a") as m:
        m.write("%s\t%s\t%d\t%s\t%s\t%s\n" % (os.path.basename(out), url, len(data), hashlib.sha256(data).hexdigest(),
                                             datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), licence))
    print("%-40s %9d bytes" % (os.path.basename(out), len(data)), flush=True)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("what", nargs="+")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    if a.what[0] == "arxiv":
        ids = a.what[1:] or ARXIV
        for i in ids:
            p = os.path.join(a.out, "arxiv_%s.src" % i)
            if not os.path.exists(p):
                get("https://arxiv.org/e-print/%s" % i, p, "arXiv e-print (author licence; read only, not redistributed)")
                time.sleep(3.5)
    elif a.what[0] == "euclid":
        for u in EUCLID:
            p = os.path.join(a.out, "euclid_dr1_" + os.path.basename(u))
            if not os.path.exists(p): get(u, p, "Euclid Consortium public DR1 paper (read only)")
    elif a.what[0] == "vizier-meta":
        for cid in a.what[1:]:
            p = os.path.join(a.out, "vizier_meta_%s.txt" % cid.replace("/", "_"))
            if not os.path.exists(p):
                get("%s?-source=%s&-meta.all" % (VIZ, cid), p, "VizieR/CDS metadata"); time.sleep(1.2)
    elif a.what[0] == "vizier":
        for tab in a.what[1:]:
            p = os.path.join(a.out, "vizier_%s.tsv" % tab.replace("/", "_"))
            if not os.path.exists(p):
                get("%s?-source=%s&-out.all&-out.max=unlimited&-oc.form=dec&-out.form=|" % (VIZ, tab), p,
                    "VizieR/CDS table (CC BY 4.0 per CDS policy)"); time.sleep(1.2)

if __name__ == "__main__":
    main()
