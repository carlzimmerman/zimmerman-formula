#!/usr/bin/env python3
"""NV2 download (owner-approved, the only one): 2MPZ (Bilicki+14) cones around the 12 X-COP clusters from the SuperCOSMOS Science Archive,
table TWOMPZ..twompzPhotoz, freeform SQL. FROZEN_CRITERIA, "The download".
  nv2_download.py count            COUNT(*) per cone (size check; stops if > ~20 MB)
  nv2_download.py fetch OUTDIR     one CSV per cone into OUTDIR (a new empty directory), DOWNLOAD_LOG.json with queries, timestamp, rows, sha256
Run with python3 -I. Writes nothing in OUTDIR except the CSVs and the log. kappa = 1/2 FITTED; not theory closed."""
import datetime, gzip, hashlib, io, json, math, os, re, sys, time, urllib.parse, urllib.request
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
URL = "http://ssa.roe.ac.uk:8080/ssa/SSASQL"; RS = 30.0; H0 = 73.0; CK = 299792.458; MAXMB = 20.0; BYTES_PER_ROW = 70
COLS = "twomassID, ra, dec, kCorr, zPhoto, zSpec"

def dc(z, n=20001):
    import numpy as np
    zg = np.linspace(0, 1, n); E = np.sqrt(0.3 * (1 + zg) ** 3 + 0.7); c = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zg))]) * CK / H0
    return float(np.interp(z, zg, c))
def clusters():
    from astropy.io import fits
    D = os.path.join(REPO, "real_research", "data", "xcop"); o = []
    for n in sorted(os.listdir(D)):
        p = os.path.join(D, n, f"{n}_hydro_mass.fits")
        if not os.path.exists(p): continue
        h = fits.open(p)[1].header; th = 1.2 * math.degrees(math.asin(RS / dc(h["REDSHIFT"])))
        o.append(dict(name=n, ra=float(h["RA"]), dec=float(h["DEC"]), z=float(h["REDSHIFT"]), r500_kpc=float(h["R500"]), theta_q_deg=th))
    return o
def where(c):
    ra, de = math.radians(c["ra"]), math.radians(c["dec"]); X, Y, Z = math.cos(de) * math.cos(ra), math.cos(de) * math.sin(ra), math.sin(de)
    t = c["theta_q_deg"]   # the dec band is implied by the cone (redundant); it lets the archive use its dec index (a plain dot-product scan timed out)
    return f"dec BETWEEN {c['dec'] - t:.6f} AND {c['dec'] + t:.6f} AND (cx*({X:.12f}) + cy*({Y:.12f}) + cz*({Z:.12f})) >= {math.cos(math.radians(t)):.12f}"
def post(sql, fmt="HTML", rows=30, tries=4):
    for k in range(tries):
        pg = _post(sql, fmt, rows)
        if "SQL Error" not in pg: return pg
        print(f"   archive SQL error (try {k + 1}/{tries}): {re.sub(r'<[^>]+>', ' ', pg[pg.find('SQL Error'):pg.find('SQL Error') + 200]).strip()[:150]}", flush=True); time.sleep(45)
    return pg
def _post(sql, fmt, rows):
    data = urllib.parse.urlencode(dict(action="freeform", server="amachine", sqlstmt=sql, emailAddress="", format=fmt, compress="NONE", rows=str(rows))).encode()
    with urllib.request.urlopen(urllib.request.Request(URL, data=data), timeout=600) as r: return r.read().decode("latin-1")
def fail_check(page):
    low = page.lower()
    for k in ("captcha", "login", "password", "sign in"):
        if k in low: sys.exit(f"STOP: archive page mentions '{k}'; no other source is sought")
def count():
    out = []; tot = 0
    for c in clusters():
        sql = f"SELECT COUNT(*) FROM TWOMPZ..twompzPhotoz WHERE {where(c)}"; pg = post(sql); fail_check(pg)
        txt = re.sub(r"<[^>]+>", " ", pg); m = re.findall(r"\b(\d+)\b", txt[txt.lower().find("count") if "count" in txt.lower() else 0:])
        nums = [int(x) for x in re.findall(r"<td[^>]*>\s*(\d+)\s*</td>", pg, flags=re.I)]
        n = nums[0] if nums else None; out.append(dict(c, n=n, sql=sql)); tot += n or 0
        print(f"{c['name']:8s} theta_q {c['theta_q_deg']:.2f} deg: COUNT {n}", flush=True)
        if n is None: print(pg[:3000]); sys.exit("STOP: could not parse the count")
    mb = tot * BYTES_PER_ROW / 1e6; print(f"total rows {tot} (with overlaps), estimated {mb:.1f} MB at {BYTES_PER_ROW} B/row; limit {MAXMB} MB -> {'OK' if mb <= MAXMB else 'STOP'}")
    json.dump(dict(cones=out, total=tot, est_MB=mb), open(os.path.join(HERE, "nv2_download_count.json"), "w"), indent=1)
    return mb <= MAXMB
def fetch(outdir):
    # resume: cones already written by an interrupted run of this script (archive-side cancellations) are kept and re-hashed; any other file stops it
    if os.path.exists(outdir) and any(not (f.startswith("twompz_cone_") and f.endswith(".csv")) for f in os.listdir(outdir)): sys.exit("STOP: OUTDIR holds foreign files")
    os.makedirs(outdir, exist_ok=True); log = dict(source=URL, table="TWOMPZ..twompzPhotoz", server="Full SSA (amachine)", columns=COLS, R_s_Mpc=RS, started=datetime.datetime.utcnow().isoformat() + "Z", cones=[])
    for c in clusters():
        sql = f"SELECT {COLS} FROM TWOMPZ..twompzPhotoz WHERE {where(c)}"; fn = os.path.join(outdir, f"twompz_cone_{c['name']}.csv")
        if os.path.exists(fn):
            raw = open(fn, "rb").read(); nrow = sum(1 for l in raw.decode("latin-1").splitlines() if l.strip() and not l.startswith("#")) - 1
            e = dict(c, sql=sql, link="(first run, link not kept)", file=os.path.basename(fn), bytes=len(raw), rows=nrow, sha256=hashlib.sha256(raw).hexdigest(), utc=datetime.datetime.utcfromtimestamp(os.path.getmtime(fn)).isoformat() + "Z", resumed=True)
            log["cones"].append(e); print(f"{c['name']:8s} kept from the first run: rows {nrow}", flush=True); continue
        pg = post(sql, fmt="CSV", rows=1, tries=8); fail_check(pg)
        links = re.findall(r'href="([^"]+\.csv(?:\.gz)?)"', pg, flags=re.I)
        if not links: print(pg[:3000]); sys.exit(f"STOP: no CSV link for {c['name']}")
        link = urllib.parse.urljoin(URL, links[0]); raw = urllib.request.urlopen(link, timeout=600).read()
        if link.endswith(".gz"): raw = gzip.decompress(raw)
        open(fn, "wb").write(raw)
        nrow = sum(1 for l in raw.decode("latin-1").splitlines() if l.strip() and not l.startswith("#")) - 1
        e = dict(c, sql=sql, link=link, file=os.path.basename(fn), bytes=len(raw), rows=nrow, sha256=hashlib.sha256(raw).hexdigest(), utc=datetime.datetime.utcnow().isoformat() + "Z"); log["cones"].append(e)
        print(f"{c['name']:8s} rows {nrow} bytes {len(raw)} sha256 {e['sha256'][:16]}", flush=True); time.sleep(2)
    log["finished"] = datetime.datetime.utcnow().isoformat() + "Z"; log["total_rows"] = sum(x["rows"] for x in log["cones"]); log["total_bytes"] = sum(x["bytes"] for x in log["cones"])
    json.dump(log, open(os.path.join(outdir, "DOWNLOAD_LOG.json"), "w"), indent=1); json.dump(log, open(os.path.join(HERE, "nv2_download.json"), "w"), indent=1)
    print(f"total rows {log['total_rows']}, bytes {log['total_bytes']}")
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "count": count()
    elif m == "fetch": fetch(sys.argv[2])
