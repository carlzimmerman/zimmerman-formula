#!/usr/bin/env python3
"""Price the public ALMA Science Archive products of the ALPINE large programme (2017.1.00428.L, 61 member OUS) via TAP + DataLink (read-only): per MOUS the product files, sizes, and which are FITS cubes."""
import csv, re, json, subprocess, urllib.parse, urllib.request, concurrent.futures as cf, xml.etree.ElementTree as ET
def get(u, data=None):
    req = urllib.request.Request(u, data=data, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=180).read().decode("utf8", "ignore")
q = "SELECT DISTINCT member_ous_uid, target_name FROM ivoa.obscore WHERE proposal_id='2017.1.00428.L'"
t = get("https://almascience.eso.org/tap/sync", urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=q)).encode())
rows = list(csv.DictReader(t.splitlines())); mous = sorted({r["member_ous_uid"] for r in rows}); tg = {}
for r in rows: tg.setdefault(r["member_ous_uid"], set()).add(r["target_name"])
print("MOUS", len(mous), "targets", len({x for v in tg.values() for x in v}))
def dl(m):
    import time
    x = ""; out = []
    for k in range(5):
        try: x = get("https://almascience.org/datalink/sync?ID=" + urllib.parse.quote(m, safe=":/")); break
        except Exception as e: time.sleep(2 + 3 * k)
    ns = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}
    try: root = ET.fromstring(x)
    except Exception: return m, []
    fields = [f.get("name") for f in root.iter("{http://www.ivoa.net/xml/VOTable/v1.3}FIELD")] or [f.get("name") for f in root.iter("FIELD")]
    for tr in list(root.iter("{http://www.ivoa.net/xml/VOTable/v1.3}TR")) or list(root.iter("TR")):
        tds = ["".join(td.itertext()) for td in tr]; out.append(dict(zip(fields, tds)))
    return m, out
res = {}
with cf.ThreadPoolExecutor(3) as ex:
    for m, o in ex.map(dl, mous): res[m] = o
tot = {"cube_fits": 0, "all": 0}; n = {"cube_fits": 0, "all": 0}; per = []
for m, o in res.items():
    cs = 0; cn = 0; al = 0
    for r in o:
        name = r.get("access_url", "") + " " + r.get("description", ""); size = int(float(r.get("content_length") or 0)); al += size
        if re.search(r"\.(cube|image)\.pbcor\.fits|cube.*\.fits|\.cube\.I\.pbcor", name.lower()) or "fits" in name.lower() and "cube" in name.lower():
            cs += size; cn += 1
    per.append(dict(mous=m, targets=";".join(sorted(tg[m])), n_files=len(o), total_GB=round(al / 1e9, 2), cube_files=cn, cube_GB=round(cs / 1e9, 2))); tot["all"] += al; tot["cube_fits"] += cs; n["cube_fits"] += cn
with open("alpine_alma_archive_pricing.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(per[0].keys())); w.writeheader(); w.writerows(per)
print("total all products GB", round(tot["all"] / 1e9, 1), "| cube-like FITS files", n["cube_fits"], "GB", round(tot["cube_fits"] / 1e9, 1))
ex0 = next(iter(res.values())); print("example fields:", list(ex0[0].keys()) if ex0 else None); print([ (r.get('access_url','')[-60:], r.get('content_length')) for r in ex0[:8]])
