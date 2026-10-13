"""CFG668 A1 fetch (criteria 461d16c55): KiDS DR5 + DES Y6 cones (6') around SDSS redMaPPer lambda>30 clusters and blank fields.
Stores per pointing: separation (arcmin), r mag, photo-z. Raw data only; no cosmology."""
import json, math, os, random, sys, time, urllib.parse, urllib.request
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); SURVEY = sys.argv[1]
SVC = {"kids": ("https://archive.eso.org/tap_cat/sync", "json"), "des": ("https://datalab.noirlab.edu/tap/sync", "csv")}[SURVEY]
def sql(ra, dec):
    if SURVEY == "kids":
        return (f"SELECT RAJ2000 AS ra, DECJ2000 AS dec, MAG_AUTO AS r, Z_B AS z FROM \"KiDS_DR5_0_ugriZYJHKs_cat_fits\" "
                f"WHERE CONTAINS(POINT('ICRS',RAJ2000,DECJ2000),CIRCLE('ICRS',{ra},{dec},0.1))=1 AND SG_FLAG=1 AND MASK=0 AND MAG_AUTO BETWEEN 20 AND 24")
    return (f"SELECT ra, dec, mag_auto_r AS r, dnf_z AS z FROM des_dr2.y6_gold WHERE 't'=q3c_radial_query(ra,dec,{ra},{dec},0.1) "
            f"AND ext_mash>=3 AND flags_gold=0 AND mag_auto_r BETWEEN 20 AND 24")
def fetch(ra, dec):
    body = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": SVC[1], "MAXREC": 200000, "QUERY": sql(ra, dec)}).encode()
    for t in range(5):
        try:
            txt = urllib.request.urlopen(SVC[0], body, timeout=300).read().decode()
            if SVC[1] == "json":
                rows = json.loads(txt)["data"]
            else:
                lines = txt.strip().split("\n")
                if not lines[0].startswith("ra"): raise RuntimeError(txt[:200])
                rows = [list(map(float, l.split(","))) for l in lines[1:] if l]
            a = np.array([[float(x) for x in r] for r in rows]) if rows else np.zeros((0, 4))
            d = np.degrees(np.arccos(np.clip(np.sin(np.radians(dec))*np.sin(np.radians(a[:,1])) + np.cos(np.radians(dec))*np.cos(np.radians(a[:,1]))*np.cos(np.radians(a[:,0]-ra)), -1, 1))) * 60
            return np.c_[d, a[:, 2], a[:, 3]].astype(np.float32)
        except Exception as e:
            err = e; time.sleep(5 * (t + 1))
    raise err
def inbox(ra, dec):
    if SURVEY == "kids": return 125 <= ra <= 240 and -6 <= dec <= 6
    return (ra >= 300 or ra <= 100) and -70 <= dec <= 6
cl = []
for line in open(os.path.join(HERE, "redmapper_lam30_z01_03.tsv")):
    f = line.rstrip("\n").split("\t")
    c = dict(name=f[0], ra=float(f[1]), dec=float(f[2]), z=float(f[3]), lam=float(f[4]))
    if inbox(c["ra"], c["dec"]): cl.append(c)
random.seed(668); rnd = []
for c in cl:
    for _ in range(2):
        a = random.uniform(0, 2*math.pi); s = random.uniform(1.0, 3.0)
        rnd.append(dict(name=c["name"] + f"_R{len(rnd)}", ra=(c["ra"] + s*math.cos(a)/max(0.2, math.cos(math.radians(c["dec"])))) % 360,
                        dec=c["dec"] + s*math.sin(a), z=c["z"], lam=0.0))
pts = [("cl", c) for c in cl] + [("rnd", r) for r in rnd]
print(SURVEY, len(cl), "candidate clusters,", len(pts), "pointings", flush=True)
def job(p):
    try: return p, fetch(p[1]["ra"], p[1]["dec"])
    except Exception as e: return p, None
with ThreadPoolExecutor(4) as ex: res = list(ex.map(job, pts))
meta = [dict(kind=k, **c, ok=g is not None, n=0 if g is None else len(g)) for (k, c), g in res]
arrs = {f"p{i}": g for i, (_, g) in enumerate(res) if g is not None}
np.savez_compressed(os.path.join(HERE, f"cfg668_a1_{SURVEY}_raw.npz"), **arrs)
json.dump(meta, open(os.path.join(HERE, f"cfg668_a1_{SURVEY}_meta.json"), "w"))
print(SURVEY, "done:", sum(m["ok"] for m in meta), "ok,", sum(not m["ok"] for m in meta), "failed,", sum(m["n"] for m in meta), "galaxies;",
      sum(m["n"] > 0 for m in meta if m["kind"] == "cl"), "clusters with data", flush=True)
