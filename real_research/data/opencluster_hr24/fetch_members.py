#!/usr/bin/env python3
"""Fetch Hunt & Reffert 2024 (J/A+A/686/A42) member-star astrometry for the nearby open clusters used by
hunt_2026/k_cross-scale_opencluster.py.  VizieR CfA mirror, one request per cluster (the mirror does not
accept a comma-separated Name list).  Writes one TSV per cluster; re-running skips files already on disk."""
import os, sys, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..")
COLS = ("Name,GaiaDR3,inrj,inrt,Prob,RA_ICRS,DE_ICRS,pmRA,e_pmRA,pmDE,e_pmDE,pmRApmDECor,"
        "Plx,e_Plx,RUWE,NSS,Gmag,BP-RP,RV,e_RV,Mass50,Mass16,Mass84")
BASE = "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/A%2BA/686/A42/members&-out.max=unlimited&-out=" + urllib.parse.quote(COLS, safe=",")

def read_clusters():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "oc_hunt2024_clusters.tsv"),
            encoding="latin-1") if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    return [{hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))} for r in rows[3:]]

def f(v):
    try: return float(v)
    except Exception: return float("nan")

def main():
    dmax = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
    cl = read_clusters()
    sel = [c for c in cl if c["Type"] == "o" and f(c["dist50"]) < dmax and f(c["NJ"]) >= 50
           and f(c["probJ"]) > 0.5 and f(c["MassJ"]) > 0]
    print(f"{len(sel)} clusters selected (type o, d < {dmax} pc, NJ >= 50, probJ > 0.5)", flush=True)
    out = os.path.join(HERE, "members"); os.makedirs(out, exist_ok=True)
    for i, c in enumerate(sel):
        nm = c["Name"]; fn = os.path.join(out, nm.replace("/", "_") + ".tsv")
        if os.path.exists(fn) and os.path.getsize(fn) > 2000: continue
        url = BASE + "&Name=" + urllib.parse.quote(nm)
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=180) as r:
                    txt = r.read().decode("latin-1")
                if txt.count("\n") > 5:
                    open(fn, "w").write(txt); break
            except Exception as e:
                print(f"  retry {nm}: {e}", flush=True); time.sleep(5)
        if i % 25 == 0: print(f"  [{i}/{len(sel)}] {nm}", flush=True)
    print("done", flush=True)

main()
