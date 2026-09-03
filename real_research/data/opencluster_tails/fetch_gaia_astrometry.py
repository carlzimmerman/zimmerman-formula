#!/usr/bin/env python3
"""Cross-match the Roeser+2019 Hyades and Praesepe tidal-tail member lists (VizieR, no parallaxes) to Gaia DR3
astrometry by source_id.  Writes <name>_gaia.csv next to the VizieR tables.  Run once; the outputs are on disk."""
import urllib.parse, urllib.request, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://gea.esac.esa.int/tap-server/tap/sync"
def read_vizier(fn, idcol):
    lines = [l.rstrip("\n") for l in open(os.path.join(HERE, fn)) if l.strip()]
    out = []
    for h, l in enumerate(lines):
        if not l.startswith("recno\t"): continue
        hdr = l.split("\t")
        if idcol not in hdr: continue
        j = hdr.index(idcol)
        for row in lines[h+3:]:
            if row.startswith("#") or not row.strip(): break
            f = row.split("\t")
            if len(f) != len(hdr): break
            out.append((f[j].strip(), dict(zip(hdr, [x.strip() for x in f]))))
    return out
def query(ids):
    q = ("SELECT source_id,ra,dec,parallax,parallax_error,pmra,pmdec,radial_velocity,phot_g_mean_mag "
         "FROM gaiadr3.gaia_source WHERE source_id IN (" + ",".join(ids) + ")")
    d = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": q}).encode()
    with urllib.request.urlopen(urllib.request.Request(URL, data=d), timeout=300) as r:
        return r.read().decode()
for fn, idcol, out in (("hyades_roeser2019.tsv", "Source", "hyades_roeser2019_gaia.csv"),
                       ("praesepe_roeser2019.tsv", "Source", "praesepe_roeser2019_gaia.csv"),
                       ("hyades_jerabkova2021.tsv", "GaiaEDR3", "hyades_jerabkova2021_gaia.csv")):
    rows = read_vizier(fn, idcol); ids = sorted({r[0] for r in rows if r[0].isdigit()})
    print(fn, len(rows), "rows,", len(ids), "unique ids", flush=True)
    hdr = None; body = []
    for i in range(0, len(ids), 400):
        txt = query(ids[i:i+400]).strip().splitlines()
        if hdr is None: hdr = txt[0]
        body += txt[1:]
        print("  ", i + 400, "->", len(body), flush=True)
    open(os.path.join(HERE, out), "w").write(hdr + "\n" + "\n".join(body) + "\n")
    print("  wrote", out, len(body), "matched", flush=True)
