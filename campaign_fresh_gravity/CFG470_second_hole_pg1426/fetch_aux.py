#!/usr/bin/env python3
"""CFG470 one-off informational lookup (not a cut; departure 2 in README): 2MASS K magnitude (VizieR II/246, 5 arcsec)
and NuSTAR / XMM archive exposures (HEASARC TAP numaster within 3', xmmmaster within 10') for PG 1426+015 and the
six part-A candidates. Writes data/aux/*.{tsv,xml} and data/aux_manifest.csv (url, bytes, sha256, date)."""
import os, hashlib, urllib.request, urllib.parse, csv, datetime

HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, "data", "aux"); os.makedirs(A, exist_ok=True)
T = {"PG1426+015": (217.27731, 1.28513), "HS0749+1943": (118.0743530, 19.5950990), "1RXSJ072352.4-080623": (110.9711350, -8.1039597),
     "1RXSJ084521.7-353048": (131.3390470, -35.5067240), "3C206": (129.9607680, -12.2428660), "Q1739+184": (265.5289600, 18.4558532),
     "2E233": (14.2914, 14.7695)}
TAP = "https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync?REQUEST=doQuery&LANG=ADQL&QUERY="
man = []
for n, (ra, de) in T.items():
    q = {"2mass": f"https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=II/246/out&-c={ra}+{de:+}&-c.rs=5&-out=2MASS,Jmag,Hmag,Kmag,e_Kmag&-sort=_r",
         "nustar": TAP + urllib.parse.quote_plus(f"SELECT obsid,exposure_a,status FROM numaster WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{de},0.05))=1"),
         "xmm": TAP + urllib.parse.quote_plus(f"SELECT obsid,pn_time,duration,status FROM xmmmaster WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{de},{10/60}))=1")}
    for k, u in q.items():
        fn = os.path.join(A, f"{k}_{n}." + ("tsv" if k == "2mass" else "xml"))
        b = urllib.request.urlopen(u, timeout=60).read(); open(fn, "wb").write(b)
        man.append((os.path.basename(fn), u, len(b), hashlib.sha256(b).hexdigest(), datetime.date.today().isoformat()))
with open(os.path.join(HERE, "data", "aux_manifest.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["file", "url", "bytes", "sha256", "date"]); w.writerows(man)
print(len(man), "files")
