"""CFG668 fetch: per-pointing galaxy lists (r, photo-z, separation) within 6' from SDSS DR18 SkyServer.
Pointings = redMaPPer clusters + random footprint points. Raw counts only; no cosmology."""
import json, sys, time, random, urllib.parse, urllib.request, os
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch"
def q(sql):
    for t in range(4):
        try:
            u = URL + "?" + urllib.parse.urlencode({"cmd": sql, "format": "json"})
            return json.load(urllib.request.urlopen(u, timeout=120))[0]["Rows"]
        except Exception as e:
            time.sleep(3 * (t + 1)); err = e
    raise err
def gals(ra, dec):
    sql = (f"select n.distance as d, g.dered_r as r, p.z as zp from dbo.fGetNearbyObjEq({ra},{dec},6) n "
           f"join Galaxy g on g.objid=n.objid join Photoz p on p.objid=g.objid "
           f"where g.dered_r between 17 and 21.5 and g.clean=1 and p.z>0 and p.zErr<0.15")
    return [(x["d"], x["r"], x["zp"]) for x in q(sql)]
cl = []
for line in open(os.path.join(HERE, "redmapper_lam60_z01_03.tsv")):
    f = line.rstrip("\n").split("\t")
    if len(f) == 5 and f[0].startswith("RMJ"):
        cl.append(dict(name=f[0], ra=float(f[1]), dec=float(f[2]), z=float(f[3]), lam=float(f[4])))
# random footprint points: offset each cluster by 1-3 deg in a random direction (same footprint/depth/extinction),
# rejected if within 15' of any lambda>20 redMaPPer cluster is NOT checked here -> checked in analysis via clean fields
random.seed(668)
rnd = []
for c in cl:
    for _ in range(2):
        import math
        a = random.uniform(0, 2 * math.pi); s = random.uniform(1.0, 3.0)
        rnd.append(dict(name=c["name"] + f"_R{len(rnd)}", ra=(c["ra"] + s * math.cos(a) / max(0.2, math.cos(math.radians(c["dec"])))) % 360,
                        dec=max(-89, min(89, c["dec"] + s * math.sin(a))), z=c["z"], lam=0.0))
pts = [("cl", c) for c in cl] + [("rnd", r) for r in rnd]
def job(p):
    kind, c = p
    try: return dict(kind=kind, **c, gals=gals(c["ra"], c["dec"]))
    except Exception as e: return dict(kind=kind, **c, gals=None, err=str(e))
with ThreadPoolExecutor(6) as ex: out = list(ex.map(job, pts))
json.dump(out, open(os.path.join(HERE, "cfg668_counts_raw.json"), "w"))
print(len(out), "pointings;", sum(o["gals"] is None for o in out), "failed;", sum(len(o["gals"] or []) for o in out), "galaxies")
