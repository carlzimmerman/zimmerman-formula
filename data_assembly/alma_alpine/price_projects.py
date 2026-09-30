#!/usr/bin/env python3
"""Price the public ALMA archive products of selected z 2-5 kinematics projects (TAP + DataLink, read-only): ASPECS LP 2016.1.00324.L, SDP.81 science verification 2011.0.00016.SV, SPT0418-47 [CII] 2016.1.01499.S.
For each project: member OUS, number of product files, total GB, and GB of FITS cube-like products."""
import csv, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
def get(u, data=None):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(u, data=data, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read().decode("utf8", "ignore")
        except Exception as e: time.sleep(2 + 3 * k)
    return ""
out = []
for pid in sys.argv[1:]:
    t = get("https://almascience.eso.org/tap/sync", urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=f"SELECT DISTINCT member_ous_uid, target_name FROM ivoa.obscore WHERE proposal_id='{pid}'")).encode())
    rows = list(csv.DictReader(t.splitlines())); mous = sorted({r["member_ous_uid"] for r in rows}); tg = sorted({r["target_name"] for r in rows})
    tot = cube = n = 0; ncube = 0; ex = []
    for m in mous:
        x = get("https://almascience.org/datalink/sync?ID=" + urllib.parse.quote(m, safe=":/"))
        try: root = ET.fromstring(x)
        except Exception: continue
        N = "{http://www.ivoa.net/xml/VOTable/v1.3}"; fields = [f.get("name") for f in root.iter(N + "FIELD")]
        for tr in root.iter(N + "TR"):
            d = dict(zip(fields, ["".join(td.itertext()) for td in tr])); u = d.get("access_url", ""); s = int(float(d.get("content_length") or 0)); tot += s; n += 1
            if re.search(r"cube", u, re.I) and re.search(r"\.fits", u, re.I): cube += s; ncube += 1; ex.append((u.split("/")[-1][:90], s))
    print(f"{pid}: {len(mous)} MOUS, {len(tg)} targets {tg[:6]}, {n} files, total {tot/1e9:.1f} GB, cube FITS {ncube} files {cube/1e9:.1f} GB", flush=True)
    for e in ex[:4]: print("    ", e)
    out.append((pid, len(mous), n, tot / 1e9, ncube, cube / 1e9))
w = csv.writer(open("project_pricing.csv", "a", newline="")); [w.writerow(o) for o in out]
