#!/usr/bin/env python3
"""Split the VizieR ASU-TSV dump of J/MNRAS/517/962 (Dunne+2022, 'Metal-rich galaxies dust, CO and [CI]'; fetched 2026-09-30 from vizier.cds.unistra.fr, file in ~/new_physics/_external_data/cds_tables/) into one CSV per table
and count galaxies by redshift and by tracer combination.  Nothing is recomputed: the values are the catalogue's (luminosities, dust fluxes, per-galaxy optimised conversion factors and M_H2)."""
import csv, os, re, json, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.expanduser("~/new_physics/_external_data/cds_tables/dunne2022_J_MNRAS_517_962_asu.tsv"); OUT = os.path.join(HERE, "dunne2022")
lines = open(SRC, encoding="utf8", errors="ignore").read().split("\n"); tables = {}; cur = None; hdr = None; i = 0
while i < len(lines):
    ln = lines[i]
    m = re.match(r"#Name: J/MNRAS/517/962/(\w+)", ln)
    if m: cur = m.group(1); tables[cur] = dict(title="", header=None, rows=[])
    m = re.match(r"#Title: (.*)", ln)
    if m and cur and not tables[cur]["title"]: tables[cur]["title"] = m.group(1)
    if cur and not ln.startswith("#") and ln.strip():
        if tables[cur]["header"] is None: tables[cur]["header"] = [h.strip() for h in ln.split("\t")]
        elif not set(ln.replace("\t", "")) <= set("- "): tables[cur]["rows"].append([c.strip() for c in ln.split("\t")])
    i += 1
summ = {}
for t, d in tables.items():
    with open(os.path.join(OUT, f"dunne2022_{t}.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(d["header"]); w.writerows(d["rows"])
    summ[t] = dict(title=d["title"], rows=len(d["rows"]), columns=len(d["header"]))
    print(t, len(d["rows"]), "rows;", d["title"])
M = [dict(zip(tables["master"]["header"], r)) for r in tables["master"]["rows"]]
def f(x):
    try: return float(x)
    except: return None
cnt = collections.Counter(); bins = [(0, 0.1), (0.1, 0.5), (0.5, 1), (1, 2), (2, 3), (3, 5), (5, 10)]
def b(z):
    for lo, hi in bins:
        if lo <= z < hi: return f"{lo}-{hi}"
rows = []
for r in M:
    z = f(r["z"]); co = f(r["logLCO"]) is not None; ci = f(r["logLCI"]) is not None and f(r["logLCI"]) > 0; du = f(r["logL850py"]) is not None
    ntr = co + ci + du
    rows.append((z, co, ci, du))
    if z is None: continue
    cnt[(b(z), "all")] += 1
    if ntr >= 2: cnt[(b(z), ">=2")] += 1
    if co and ci and du: cnt[(b(z), "3")] += 1
    if co and du: cnt[(b(z), "CO+dust")] += 1
    if co and ci: cnt[(b(z), "CO+CI")] += 1
    if ci and du: cnt[(b(z), "CI+dust")] += 1
out = {"tables": summ, "master_rows": len(M), "counts": {f"{k[0]} | {k[1]}": v for k, v in sorted(cnt.items(), key=lambda x: (x[0][0] or "", x[0][1]))}}
json.dump(out, open(os.path.join(OUT, "dunne2022_counts.json"), "w"), indent=1)
hdrs = ["all", ">=2", "3", "CO+dust", "CO+CI", "CI+dust"]
print("z bin | " + " | ".join(hdrs))
for lo, hi in bins: k = f"{lo}-{hi}"; print(k, "|", " | ".join(str(cnt[(k, h)]) for h in hdrs))
print("total", [sum(cnt[(f"{lo}-{hi}", h)] for lo, hi in bins) for h in hdrs])
json.dump({"src": os.path.basename(SRC), "sha256": hashlib.sha256(open(SRC, "rb").read()).hexdigest(), "bytes": os.path.getsize(SRC), "url": "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/517/962&-out.max=unlimited&-out.meta=h", "fetched": "2026-09-30"}, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
