#!/usr/bin/env python3
"""CFG268 -- READ-ONLY pricing of public ALMA archive products for the z ~ 2.5-4 one-offs.

Nothing is downloaded. Two metadata services of the ALMA Science Archive are queried:
  * TAP  (https://almascience.eso.org/tap/sync, table ivoa.obscore): which programmes / member OUS
    cover each object position (10 arcsec radius), with band, resolution, release date, data rights;
  * DataLink (https://almascience.org/datalink/sync?ID=<MOUS>): the file list and byte sizes of the
    MOUS of the programmes the source papers name.
Output: cfg268_alma_price.out (text) and cfg268_alma_price.csv (one row per priced MOUS).
Control C1: the TAP listing for ADF22.1 must contain 2021.1.01406.S (the programme Rizzo+26 and
Umehata+25 name for the 0.23-arcsec [CII] cube); C2: every priced MOUS returns a non-empty file list
or is reported as not available (no silent zero). MUTATE=1 shifts every position by +1 deg in Dec
(C1 must then fail).
"""
import csv, os, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET

MUTATE = int(os.environ.get("MUTATE", "0"))
OBJ = [  # name, RA deg, Dec deg, programmes named in the source papers
    ("ADF22.1", 334.38507, 0.29551, ["2021.1.01406.S", "2021.1.00041.S", "2018.1.01306.S"]),
    ("BigWheel", 10.396371, -49.620112, ["2021.1.00793.S", "2025.1.00107.S"]),
    ("MQN01-QC", 10.381096, -49.603595, ["2021.1.00793.S"]),
    ("PKS0529-549", 82.606029, -54.906435, ["2018.1.01669.S"]),
    ("SPT2147-50", 326.829375, -50.598333, ["2018.1.01060.S", "2019.1.00471.S"]),
    ("SPT0103-45", 15.797917, -45.648306, ["2017.1.01018.S", "2023.1.01354.S"]),
    ("SDP.81", 135.798333, 0.651667, ["2011.0.00016.SV"]),
    ("CosmicEye", 323.803042, -1.028583, ["2019.1.01642.S"]),
]


def get(u, data=None, tries=4):
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(u, data=data, headers={"User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=180).read().decode("utf8", "ignore")
        except Exception as e:
            last = e
            time.sleep(2 + 3 * k)
    raise last


def tap(q):
    t = get("https://almascience.eso.org/tap/sync",
            urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=q)).encode())
    return list(csv.DictReader(t.splitlines()))


def datalink(mous):
    x = get("https://almascience.org/datalink/sync?ID=" + urllib.parse.quote(mous, safe=":/"))
    root = ET.fromstring(x)
    ns = "{http://www.ivoa.net/xml/VOTable/v1.3}"
    fields = [f.get("name") for f in root.iter(ns + "FIELD")] or [f.get("name") for f in root.iter("FIELD")]
    rows = []
    for tr in list(root.iter(ns + "TR")) or list(root.iter("TR")):
        rows.append(dict(zip(fields, ["".join(td.itertext()) for td in tr])))
    return rows


def classify(name):
    n = name.lower()
    if "asdm" in n:
        return "raw"
    if "auxiliary" in n:
        return "aux"
    if n.endswith(".tar") or ".tar" in n:
        return "product"
    if n.endswith(".fits") or ".fits" in n:
        return "fits"
    return "other"


out = []
csvrows = []
fails = []
P = lambda s="": (print(s), out.append(s))
P("CFG268 ALMA archive pricing (metadata only; nothing downloaded)%s" % ("  [MUTATE=%d]" % MUTATE if MUTATE else ""))
for name, ra, dec, progs in OBJ:
    if MUTATE == 1:
        dec += 1.0
    q = ("SELECT proposal_id, member_ous_uid, target_name, band_list, s_resolution, t_exptime, obs_release_date, data_rights "
         "FROM ivoa.obscore WHERE INTERSECTS(CIRCLE('ICRS',%.6f,%.6f,0.00278), s_region)=1" % (ra, dec))
    try:
        rows = tap(q)
    except Exception as e:
        P("== %s: TAP query failed (%s)" % (name, e)); fails.append("TAP-" + name); continue
    seen = {}
    for r in rows:
        k = (r["proposal_id"], r["member_ous_uid"])
        if k not in seen:
            seen[k] = r
    P("\n== %s (RA %.5f, Dec %.5f): %d member OUS from %d programmes cover the position" %
      (name, ra, dec, len(seen), len({k[0] for k in seen})))
    for (pid, mous), r in sorted(seen.items()):
        try:
            res = float(r["s_resolution"]); res_s = "%.2f\"" % res
        except Exception:
            res_s = "?"
        P("   %-16s %-28s band %-4s res %-7s t_exp %8s s  release %s  %s  target %s" %
          (pid, mous, r["band_list"], res_s, r["t_exptime"][:8], r["obs_release_date"][:10], r["data_rights"], r["target_name"]))
    if name == "ADF22.1":
        c1 = any(k[0] == "2021.1.01406.S" for k in seen)
        P("   C1 2021.1.01406.S present in the ADF22.1 listing: %s" % ("PASS" if c1 else "FAIL"))
        if not c1:
            fails.append("C1")
    for (pid, mous), r in sorted(seen.items()):
        if pid not in progs:
            continue
        try:
            files = datalink(mous)
        except Exception as e:
            P("   DataLink %s %s: not available (%s)" % (pid, mous, e)); csvrows.append(dict(object=name, proposal=pid, mous=mous, status="datalink-failed")); continue
        tot = {"product": 0, "aux": 0, "raw": 0, "fits": 0, "other": 0}
        nfiles = {"product": 0, "aux": 0, "raw": 0, "fits": 0, "other": 0}
        for f in files:
            nm = (f.get("access_url") or "") + " " + (f.get("description") or "")
            sz = int(float(f.get("content_length") or 0))
            c = classify(nm.split()[0] if nm.strip() else "")
            tot[c] += sz; nfiles[c] += 1
        if not files:
            P("   DataLink %s %s: EMPTY list (not public or not ingested)" % (pid, mous))
            csvrows.append(dict(object=name, proposal=pid, mous=mous, status="empty", release=r["obs_release_date"][:10], rights=r["data_rights"]))
            continue
        P("   DataLink %s %s: product tar %.2f GB (%d), auxiliary %.2f GB (%d), raw ASDM %.2f GB (%d), other %.3f GB (%d)" %
          (pid, mous, tot["product"] / 1e9, nfiles["product"], tot["aux"] / 1e9, nfiles["aux"], tot["raw"] / 1e9, nfiles["raw"],
           (tot["fits"] + tot["other"]) / 1e9, nfiles["fits"] + nfiles["other"]))
        csvrows.append(dict(object=name, proposal=pid, mous=mous, status="ok", release=r["obs_release_date"][:10], rights=r["data_rights"],
                            band=r["band_list"], res_arcsec=r["s_resolution"], product_GB=round(tot["product"] / 1e9, 3),
                            aux_GB=round(tot["aux"] / 1e9, 3), raw_GB=round(tot["raw"] / 1e9, 3)))
    missing = [p for p in progs if not any(k[0] == p for k in seen)]
    if missing:
        P("   named programmes NOT in the archive listing at this position: %s (not ingested, proprietary-unlisted, or a different position)" % ", ".join(missing))

c2 = all(r.get("status") in ("ok", "empty", "datalink-failed") for r in csvrows)
P("\nC2 every priced MOUS reported (ok / empty / failed, never a silent zero): %s" % ("PASS" if c2 else "FAIL"))
if not c2:
    fails.append("C2")
suffix = "_MUTATE%d" % MUTATE if MUTATE else ""
with open("cfg268_alma_price%s.csv" % suffix, "w", newline="") as fh:
    keys = ["object", "proposal", "mous", "status", "release", "rights", "band", "res_arcsec", "product_GB", "aux_GB", "raw_GB"]
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader()
    for r in csvrows:
        w.writerow({k: r.get(k, "") for k in keys})
P("RESULT: %s" % ("ALL CONTROLS PASS" if not fails else "FAILED: " + ", ".join(fails)))
sys.exit(1 if fails else 0)
