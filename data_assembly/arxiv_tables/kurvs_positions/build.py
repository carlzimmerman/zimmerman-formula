#!/usr/bin/env python3
"""Sky positions of the 22 KURVS-CDFS galaxies, from the paper's own Table 1 (arXiv:2305.04382), and where they fall relative to public ALMA surveys.

Correction to an earlier note of mine: the paper DOES give RA and Dec (Table 1, columns 3-4); the kurvs2023_integrated.csv parse had dropped them.
Independent check: KURVS-21 and -22 (3D-HST IDs GS4_10784 and GS4_16960) are also in the KMOS3D catalogue on disk (kmos3d_phibss/kmos3d_catalog.csv);
the two positions must agree to under 1 arcsec.
Negative control (recorded in README): the CANDELS IDs are NOT the ZFOURGE sequence numbers (a VizieR query for them returned objects at other redshifts).
Coverage: only the geometry stated in the papers' text (see README); no ALMA source table is used here.
Usage: python3 build.py
"""
import csv, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.join(HERE, "..")
TEX = os.path.expanduser("~/new_physics/_external_data/arxiv_src/2305.04382/kurvs_I_arXiv_May2023.tex")
LOG = []


def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)


tex = open(TEX).read()
i0 = tex.index("KURVS ID & CANDELS ID & RA")
rows = []
for line in tex[i0:i0 + 6000].splitlines():
    m = re.match(r"\s*(\d+) & ([A-Za-z0-9\\_]+) & (\d\d):(\d\d):(\d\d\.\d\d) & --?(\d\d):(\d\d):(\d\d\.\d\d) & ([\d.]+) & ([\d.]+) &", line)
    if m:
        k, cid, rh, rm, rs, dd, dm, ds, z, lm = m.groups()
        ra = 15 * (int(rh) + int(rm) / 60 + float(rs) / 3600)
        dec = -(int(dd) + int(dm) / 60 + float(ds) / 3600)
        rows.append(dict(kurvs_id=int(k), candels_id=cid.replace("\\_", "_"), ra_hms=f"{rh}:{rm}:{rs}", dec_dms=f"-{dd}:{dm}:{ds}",
                         ra_deg=round(ra, 6), dec_deg=round(dec, 6), z_halpha=float(z), logMstar=float(lm)))
check(len(rows) == 22 and [r["kurvs_id"] for r in rows] == list(range(1, 23)), "22 rows parsed from Table 1, ids 1..22")

# cross-check against the integrated table already in the repo (same z and mass)
integ = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(TAB, "kurvs2023_integrated.csv")))}
check(all(abs(float(integ[r["kurvs_id"]]["z_halpha"]) - r["z_halpha"]) < 1e-3 and abs(float(integ[r["kurvs_id"]]["logMstar"]) - r["logMstar"]) < 0.01 for r in rows),
      "z and log M* of the position rows equal kurvs2023_integrated.csv for all 22")

# independent position check with KMOS3D catalogue
k3d = {r["ID"]: r for r in csv.DictReader(open(os.path.join(TAB, "..", "kmos3d_phibss", "kmos3d_catalog.csv")))}
def sep_arcsec(ra1, d1, ra2, d2):
    dra = (ra1 - ra2) * math.cos(math.radians((d1 + d2) / 2)) * 3600; dd = (d1 - d2) * 3600
    return math.hypot(dra, dd)
for r in rows:
    if r["candels_id"].startswith("GS4_"):
        c = k3d[r["candels_id"]]
        s = sep_arcsec(r["ra_deg"], r["dec_deg"], float(c["RA"]), float(c["DEC"]))
        r["kmos3d_sep_arcsec"] = round(s, 2)
        check(s < 1.0, f"{r['candels_id']}: KURVS Table-1 position agrees with KMOS3D catalogue to {s:.2f} arcsec")

# geometry from the papers' text (README lists the sources)
GA_RA, GA_DEC = 53.1250, -27.8000            # GOODS-ALMA field centre 03:32:30, -27:48:00; ~10' x 7', area 72.42 arcmin^2 (arXiv:2106.13246 HTML)
GA_INNER, GA_OUTER = 3.5, math.hypot(5.0, 3.5)   # arcmin: inscribed and circumscribed radius of a 10' x 7' rectangle (orientation not stated)
UDF_RA, UDF_DEC = 15 * (3 + 32 / 60 + 39.0 / 3600), -(27 + 47 / 60 + 29 / 3600)   # HUDF centre: NOT from a source I read (UNVERIFIED)
ASPECS_R = 1.0                                # "~1' region within the UDF" (arXiv:1607.06768 abstract page): read as a generous 1-arcmin radius
for r in rows:
    d = sep_arcsec(r["ra_deg"], r["dec_deg"], GA_RA, GA_DEC) / 60
    r["sep_from_GOODSALMA_centre_arcmin"] = round(d, 2)
    r["GOODSALMA_status"] = "inside for any orientation" if d <= GA_INNER else ("outside for any orientation" if d > GA_OUTER else "depends on the mosaic orientation (not stated)")
    du = sep_arcsec(r["ra_deg"], r["dec_deg"], UDF_RA, UDF_DEC) / 60
    r["sep_from_UDF_centre_arcmin_UNVERIFIED"] = round(du, 2)
    r["ASPECS_status"] = "outside (more than 1 arcmin from the UDF centre)" if du > ASPECS_R else "inside the ~1 arcmin ASPECS region"
fields = list(rows[0].keys()); fields += [f for r in rows for f in r if f not in fields]
fields = list(dict.fromkeys(fields))
with open(os.path.join(HERE, "kurvs_positions.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
n = {}
for r in rows: n[r["GOODSALMA_status"]] = n.get(r["GOODSALMA_status"], 0) + 1
LOG.append("GOODS-ALMA status counts: " + str(n)); print(LOG[-1])
LOG.append("ASPECS: " + str(sum(r["ASPECS_status"].startswith("inside") for r in rows)) + " inside"); print(LOG[-1])
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
