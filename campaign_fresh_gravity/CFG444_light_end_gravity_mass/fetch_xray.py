#!/usr/bin/env python3
"""CFG444 fetch step (D3 X-ray readiness). Run once; writes data/xray_lookup.csv and data/positions.csv,
appends sha256 of every raw response to data/xray_fetch_manifest.csv. Raw VOTables go to
../_external_data/cfg444/xray/ (git-ignored). Sources: CDS Sesame (positions for names not in vdB16),
VizieR J/ApJS/235/4 (Swift/BAT 105-month, Oh+2018), HEASARC TAP tables numaster, xmmmaster, xmmssc (4XMM).
Candidates: every vdB16 (J/ApJ/831/134) table2/3 object with 8.477 <= log M <= 9.477, the GRAVITY rows of
data/gravity_masses.csv, and CFG394's compiled spin objects (route B)."""
import os, io, csv, hashlib, time, urllib.request, urllib.parse
import warnings
warnings.filterwarnings("ignore")
from astropy.io.votable import parse_single_table

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "_external_data", "cfg444", "xray"); os.makedirs(RAW, exist_ok=True)
MAN = []


def get(url, tag):
    for k in range(4):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "cfg444"}), timeout=120).read(); break
        except Exception as e:
            if k == 3: raise
            time.sleep(5)
    open(os.path.join(RAW, tag), "wb").write(b)
    MAN.append(dict(tag=tag, url=url, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), date=time.strftime("%Y-%m-%d")))
    return b


def vdb(fn):
    L = [l for l in open(os.path.join(HERE, "data", fn)) if not l.startswith("#") and l.strip()]
    h = L[0].rstrip("\n").split("\t")
    return [dict(zip(h, [x.strip() for x in l.rstrip("\n").split("\t")])) for l in L[3:]]


cands = {}
for fn in ("vdb16_t2.tsv", "vdb16_t3.tsv"):
    for r in vdb(fn):
        try: m = float(r["logBHMass"])
        except ValueError: continue
        if 8.477 <= m <= 9.477:
            cands[r["Name"]] = (float(r["_RA"]), float(r["_DE"]), "vdB16 SIMBAD column")
sesame = {"J0529-4351": "SMSS J052915.80-435152.0", "J0920+0657": "SDSS J092034.17+065718.0", "3C273": "3C 273",
          "H1821+643": "H 1821+643", "Q2237+305": "QSO B2237+0305", "PG1426+015": "PG 1426+015", "PG0804+761": "PG 0804+761",
          "PG2112+059": "PG 2112+059", "1H0419-577": "1H 0419-577"}
for n, s in sesame.items():
    if n in cands: continue
    t = get("https://cds.unistra.fr/cgi-bin/nph-sesame/-oI/SNV?" + urllib.parse.quote(s), f"sesame_{n}.txt").decode()
    j = [l for l in t.splitlines() if l.startswith("%J ")][0].split()
    cands[n] = (float(j[1]), float(j[2]), f"Sesame '{s}'")


def tap(q, tag):
    u = "https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync?" + urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", QUERY=q))
    return parse_single_table(io.BytesIO(get(u, tag))).to_table()


out = []
for n, (ra, de, src) in cands.items():
    safe = n.replace("+", "p").replace("(", "").replace(")", "")
    circ = lambda r: f"CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{de},{r}))=1"
    nu = tap(f"SELECT obsid,exposure_a,status FROM numaster WHERE {circ(3/60)}", f"nu_{safe}.xml")
    nu_ks = sum(float(x["exposure_a"]) for x in nu if str(x["status"]).strip() in ("archived", "processed", "observed") and str(x["exposure_a"]) not in ("--", "nan")) / 1e3
    xm = tap(f"SELECT obsid,pn_time,duration,status FROM xmmmaster WHERE {circ(10/60)}", f"xmm_{safe}.xml")
    xm_ks = sum(float(x["duration"]) for x in xm if str(x["duration"]) not in ("--", "nan")) / 1e3
    sc = tap(f"SELECT ep_4_flux,ep_5_flux,ep_flux FROM xmmssc WHERE {circ(15/3600)}", f"4xmm_{safe}.xml")
    f210 = sorted(float(x["ep_4_flux"]) + float(x["ep_5_flux"]) for x in sc if str(x["ep_4_flux"]) not in ("--", "nan") and str(x["ep_5_flux"]) not in ("--", "nan"))
    bt = get(f"https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/235/4/table3&-c={ra}+{de:+}&-c.rm=6&-out=Swift,Flux,z,logL,Type,CName&-sort=_r", f"bat_{safe}.tsv").decode()
    rows = [l.split("\t") for l in bt.splitlines() if l and not l.startswith("#") and not l.startswith("-")]
    bat = rows[2] if len(rows) > 2 else None
    out.append(dict(name=n, ra=ra, dec=de, pos_src=src, nustar_ks_3arcmin=round(nu_ks, 1), n_nustar=len(nu),
                    xmm_ks_10arcmin=round(xm_ks, 1), n_xmm=len(xm), n_4xmm_det=len(f210),
                    f2_12_4xmm_median=f210[len(f210) // 2] if f210 else "", f2_12_4xmm_max=f210[-1] if f210 else "",
                    bat_name=bat[0].strip() if bat else "", bat_flux_1e12cgs=bat[1].strip() if bat else "",
                    bat_z=bat[2].strip() if bat else "", bat_logL=bat[3].strip() if bat else "", bat_type=bat[4].strip() if bat else "",
                    bat_cname=bat[5].strip() if bat else ""))
    print(n, out[-1]["nustar_ks_3arcmin"], out[-1]["xmm_ks_10arcmin"], out[-1]["f2_12_4xmm_median"], out[-1]["bat_flux_1e12cgs"], flush=True)
# BAT105 flux distribution for the non-detection limit sanity check
fl = get("https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/235/4/table3&-out=Flux&-out.max=unlimited", "bat_all_flux.tsv").decode()
open(os.path.join(HERE, "data", "bat105_fluxes.txt"), "w").write("\n".join(l.strip() for l in fl.splitlines() if l.strip() and not l.startswith("#") and l.strip()[0].isdigit()) + "\n")
with open(os.path.join(HERE, "data", "xray_lookup.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, list(out[0])); w.writeheader(); w.writerows(out)
with open(os.path.join(HERE, "data", "xray_fetch_manifest.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, list(MAN[0])); w.writeheader(); w.writerows(MAN)
print(len(out), "objects;", len(MAN), "responses")
