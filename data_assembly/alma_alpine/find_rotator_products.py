#!/usr/bin/env python3
"""List the ALMA archive FITS products of the ALPINE rotators (corpus tier 1): CG32, DC396844, DC494057, DC552206, DC881725, VC5110377875, HZ9 (J0817 is a different programme and is handled separately)."""
import csv, re, json, urllib.parse, urllib.request, time, xml.etree.ElementTree as ET
def get(u, data=None):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(u, data=data, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read().decode("utf8", "ignore")
        except Exception as e: time.sleep(2 + 3 * k)
    return ""
names = {"CG32": "%GOODSS_32%", "DC396844": "%COSMOS_396844", "DC494057": "%COSMOS_494057", "DC552206": "%COSMOS_552206", "DC881725": "%COSMOS_881725", "VC5110377875": "%5110377875%", "HZ9": "%HZ9%"}
out = []
for k, pat in names.items():
    q = f"SELECT DISTINCT target_name, member_ous_uid, proposal_id FROM ivoa.obscore WHERE target_name LIKE '{pat}' AND proposal_id='2017.1.00428.L'"
    t = get("https://almascience.eso.org/tap/sync", urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=q)).encode())
    for r in csv.DictReader(t.splitlines()):
        x = get("https://almascience.org/datalink/sync?ID=" + urllib.parse.quote(r["member_ous_uid"], safe=":/"))
        try: root = ET.fromstring(x)
        except Exception: print(k, "datalink parse failed", r); continue
        N = "{http://www.ivoa.net/xml/VOTable/v1.3}"; fields = [f.get("name") for f in root.iter(N + "FIELD")]
        for tr in root.iter(N + "TR"):
            d = dict(zip(fields, ["".join(td.itertext()) for td in tr])); u = d.get("access_url", "")
            if re.search(r"\.fits", u, re.I) and r["target_name"].lower() in u.lower() or (re.search(r"\.fits", u, re.I) and k.lower() in u.lower()):
                out.append(dict(rotator=k, target=r["target_name"], mous=r["member_ous_uid"], url=u, bytes=d.get("content_length"), semantics=d.get("semantics", ""), desc=d.get("description", "")[:60]))
with open("alpine_rotator_products.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["rotator", "target", "mous", "url", "bytes", "semantics", "desc"]); w.writeheader(); w.writerows(out)
print(len(out), "FITS products;", round(sum(int(o["bytes"] or 0) for o in out) / 1e9, 2), "GB")
for k in names:
    L = [o for o in out if o["rotator"] == k]; print(k, len(L), round(sum(int(o["bytes"] or 0) for o in L) / 1e6), "MB", [o["url"].split("/")[-1][:70] for o in L][:4])
