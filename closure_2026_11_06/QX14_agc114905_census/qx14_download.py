#!/usr/bin/env python3
"""QX14 download: the owner-approved census queries only (FROZEN_CRITERIA.md, 922b5e8167).
NED (name lookup + TAP cone), HyperLEDA (SQL cone), ALFALFA a.100 (VizieR, J/ApJ/861/49), 2MPZ (SSA freeform SQL).
usage: python3 -I qx14_download.py OUTDIR    (OUTDIR: _external_data/qx14_agc114905, empty at first run)
Writes raw files into OUTDIR and QUERY_LOG.json next to this script. kappa = 1/2 FITTED; not theory closed."""
import datetime, hashlib, json, math, os, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.abspath(sys.argv[1])
UA = {"User-Agent": "research-script/1.0"}
RAD = 0.75                       # deg, cone (> 0.7286 = 1 Mpc at 78.7 Mpc)
LOG = dict(note="owner-approved 11-06 (QX4_udg/NEEDS_OWNER.md); generic User-Agent", queries=[])


def get(url, data=None, timeout=300, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r: return r.read()
        except Exception as e:
            print(f"   try {k + 1} failed: {e}", flush=True); time.sleep(20)
    raise SystemExit(f"download failed: {url[:120]}")


def save(tag, url, raw, fname, nrows, post=None):
    open(os.path.join(OUT, fname), "wb").write(raw)
    LOG["queries"].append(dict(tag=tag, url=url, post=post, file=fname, bytes=len(raw), rows=nrows,
                               sha256=hashlib.sha256(raw).hexdigest(), utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    print(f"{tag}: {nrows} rows, {len(raw)} bytes -> {fname}", flush=True)


def lines(raw): return [l for l in raw.decode("utf-8", "replace").splitlines() if l.strip() and not l.startswith("#")]


# 1. NED name lookup
u = "https://ned.ipac.caltech.edu/srs/ObjectLookup"; post = 'json={"name":{"v":"AGC 114905"}}'
raw = get(u, data=post.encode()); save("NED lookup", u, raw, "ned_lookup.json", 1, post=post)
J = json.loads(raw); RA0 = J["Preferred"]["Position"]["RA"]; DE0 = J["Preferred"]["Position"]["Dec"]

# 2. NED TAP cone (objects with a redshift)
adql = ("SELECT prefname, ra, dec, prefphytype, z, zunc, zflag, n_crosref FROM NEDTAP.objdir WHERE "
        f"CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {RA0:.6f}, {DE0:.6f}, {RAD})) = 1 AND z IS NOT NULL")
u = "https://ned.ipac.caltech.edu/tap/sync?" + urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=adql))
raw = get(u); save("NED TAP cone", u, raw, "ned_cone.csv", len(lines(raw)) - 1)

# 3. HyperLEDA SQL cone (box in al2000 hours / de2000 deg, then cut to the cone in the grader)
dra = RAD / math.cos(math.radians(DE0))
sql = (f"al2000 between {(RA0 - dra) / 15:.6f} and {(RA0 + dra) / 15:.6f} and de2000 between {DE0 - RAD:.6f} and {DE0 + RAD:.6f}")
u = "http://atlas.obs-hp.fr/hyperleda/fG.cgi?" + urllib.parse.urlencode(dict(n="meandata", c="o", of="1,leda,simbad", nra="l", nakd="1",
    d="pgc,objname,al2000,de2000,objtype,v,e_v,vopt,vrad,kt,e_kt,btc,e_bt,logd25,m21c", sql=sql, ob="", a="csv[,]"))
raw = get(u); save("HyperLEDA cone", u, raw, "hyperleda_cone.csv", len(lines(raw)) - 1)

# 4. ALFALFA a.100 (VizieR J/ApJ/861/49 table2), cone; CDS then the CfA mirror
q = urllib.parse.urlencode({"-source": "J/ApJ/861/49/table2", "-c": f"{RA0:.6f} {DE0:+.6f}", "-c.rd": f"{RAD}", "-out.all": "", "-out.max": "unlimited"})
raw = None
for host in ("https://vizier.cfa.harvard.edu", "https://vizier.cds.unistra.fr"):
    u = f"{host}/viz-bin/asu-tsv?{q}"
    try: raw = get(u, tries=2); break
    except SystemExit as e: print(e, flush=True)
if raw is None: raise SystemExit("ALFALFA: no VizieR host answered")
save("ALFALFA a.100 cone", u, raw, "alfalfa_a100_cone.tsv", len([l for l in lines(raw) if not l.startswith("-")]) - 2)

# 5. 2MPZ cone (SSA freeform SQL, as NV2)
X, Y, Z = (math.cos(math.radians(DE0)) * math.cos(math.radians(RA0)), math.cos(math.radians(DE0)) * math.sin(math.radians(RA0)), math.sin(math.radians(DE0)))
sql = (f"SELECT twomassID, ra, dec, kCorr, zPhoto, zSpec FROM TWOMPZ..twompzPhotoz WHERE dec BETWEEN {DE0 - RAD:.6f} AND {DE0 + RAD:.6f} "
       f"AND (cx*({X:.12f}) + cy*({Y:.12f}) + cz*({Z:.12f})) >= {math.cos(math.radians(RAD)):.12f}")
u = "http://ssa.roe.ac.uk:8080/ssa/SSASQL"; post = dict(action="freeform", server="amachine", sqlstmt=sql, emailAddress="", format="CSV", compress="NONE", rows="30")
page = get(u, data=urllib.parse.urlencode(post).encode()).decode("latin-1")
import re
link = re.findall(r'href="([^"]+\.csv[^"]*)"', page)
if not link: open(os.path.join(OUT, "twompz_page.html"), "w").write(page); raise SystemExit("2MPZ: no CSV link in archive page (saved)")
lu = link[0] if link[0].startswith("http") else urllib.parse.urljoin(u, link[0])
raw = get(lu); save("2MPZ cone", u + " -> " + lu, raw, "twompz_cone.csv", len(lines(raw)) - 1, post=sql)

LOG["target"] = dict(ra=RA0, dec=DE0, z=J["Preferred"]["Redshift"]["Value"], name=J["Preferred"]["Name"])
json.dump(LOG, open(os.path.join(HERE, "QUERY_LOG.json"), "w"), indent=1)
print("done", flush=True)
