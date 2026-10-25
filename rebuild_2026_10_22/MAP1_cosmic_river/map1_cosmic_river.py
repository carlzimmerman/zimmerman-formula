#!/usr/bin/env python3
"""MAP1_cosmic_river: a descriptive map of the measured local flow field (the "cosmic river") from Cosmicflows-4, with the
record's SPARC galaxies and nearby eRASS1 clusters placed on it. Descriptive only: no fit, no verdict.

Inputs (read-only):
  ../_external_data/cosmicflows4/table2.dat   Tully+2023, VizieR J/ApJ/944/94 table2 (galaxies; fixed-width, ReadMe bytes)
  ../_external_data/cosmicflows4/sesame_sparc.csv   SPARC positions (CDS Sesame)
  rebuild_2026_10_22/X33_system_atlas/x33_atlas.csv  SPARC distances and law residuals (X33)
  real_research/data/erass1cl_primary_v3.2.fits      eRASS1 primary clusters (z, positions)

Method:
  * Galaxy distance d = 10^((DM-25)/5) Mpc from CF4's combined DM. Galaxies are averaged into CF4 groups (1PGC):
    inverse-variance mean DM, mean Vcmb.
  * Hubble constant: self-calibrated so the median group log(cz / d) is 0 in the shell 40 < cz/H < 150 Mpc, with
    data from this table only (CF4's own distance zero point). The value is printed.
  * Peculiar velocity (Watkins & Feldman 2015 estimator): v_pec = cz ln(cz / (H d)), with its error from e_DM.
  * Groups are placed at their redshift distance cz/H in supergalactic Cartesian coordinates (SGX, SGY, SGZ).
  * Slice |SGZ| < 25 Mpc, R < 160 Mpc. Smoothed radial-flow field on a 4 Mpc grid: Gaussian kernel (sigma 10 Mpc),
    weights 1/err^2, shown only where the kernel's effective count is >= 3.
  * SPARC galaxies at their X33 distance; eRASS1 clusters with z < 0.037 (cz/H < 160 Mpc) at cz/H.
Output: map1_cosmic_river.json (+ .out). Run: OMP_NUM_THREADS=1 nice -n 15 python3 map1_cosmic_river.py
kappa = 1/2 FITTED; this map makes no claim about the theory; the cold component is called cold dark energy.
"""
import csv, json, math, os, sys
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "cosmicflows4")
C = 299792.458
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

def fnum(line, a, b):
    t = line[a - 1:b].strip()
    return float(t) if t else None

rows = []
with open(os.path.join(EXT, "table2.dat")) as fh:
    for line in fh:
        rows.append(dict(pgc=int(line[0:7]), g=int(line[8:15]), v=fnum(line, 23, 27), dm=fnum(line, 29, 34), edm=fnum(line, 36, 40),
                         sgl=fnum(line, 174, 181), sgb=fnum(line, 183, 190)))
P(f"CF4 table2 rows {len(rows)}")
groups = {}
for r in rows:
    if r["dm"] is None or r["edm"] is None or r["v"] is None or r["sgl"] is None: continue
    groups.setdefault(r["g"], []).append(r)
G = []
for gid, m in groups.items():
    w = np.array([1 / max(x["edm"], 0.01) ** 2 for x in m]); dm = float(np.sum(w * [x["dm"] for x in m]) / np.sum(w))
    edm = float(1 / math.sqrt(np.sum(w))); v = float(np.mean([x["v"] for x in m]))
    dom = next((x for x in m if x["pgc"] == gid), m[0])
    G.append(dict(g=gid, n=len(m), dm=dm, edm=edm, v=v, sgl=dom["sgl"], sgb=dom["sgb"]))
P(f"groups {len(G)}")
d = np.array([10 ** ((x["dm"] - 25) / 5) for x in G]); v = np.array([x["v"] for x in G])
ok = v > 300
# self-calibrated H: median log(cz/d) = 0 in 40-150 Mpc (redshift distance with H trial 75)
Htr = 75.0
for _ in range(5):
    sh = ok & (v / Htr > 40) & (v / Htr < 150)
    Htr = float(np.exp(np.median(np.log(v[sh] / d[sh]))))
H = Htr
P(f"self-calibrated H (CF4 distance scale) = {H:.2f} km/s/Mpc from {int(sh.sum())} groups")
recs = []
for x, di in zip(G, d):
    if x["v"] <= 300: continue
    vpec = x["v"] * math.log(x["v"] / (H * di)); evp = x["v"] * (math.log(10) / 5) * x["edm"]
    R = x["v"] / H; L = math.radians(x["sgl"]); B = math.radians(x["sgb"])
    X, Y, Z = R * math.cos(B) * math.cos(L), R * math.cos(B) * math.sin(L), R * math.sin(B)
    recs.append(dict(x=X, y=Y, z=Z, R=R, vp=vpec, ev=evp, n=x["n"], g=x["g"]))
sl = [r for r in recs if abs(r["z"]) < 25 and r["R"] < 160]
P(f"slice |SGZ|<25, R<160: {len(sl)} groups; median |v_pec| err {np.median([r['ev'] for r in sl]):.0f} km/s")
# smoothed field
xs = np.arange(-160, 160.1, 4.0); ys = xs.copy(); sig = 10.0
px = np.array([r["x"] for r in sl]); py = np.array([r["y"] for r in sl]); pv = np.array([r["vp"] for r in sl]); pw = 1 / np.array([r["ev"] for r in sl]) ** 2
field = np.full((len(ys), len(xs)), np.nan); dens = np.zeros((len(ys), len(xs)))
for j, yy in enumerate(ys):
    for i, xx in enumerate(xs):
        if math.hypot(xx, yy) > 160: continue
        k = np.exp(-((px - xx) ** 2 + (py - yy) ** 2) / (2 * sig ** 2)); dens[j, i] = k.sum()
        if dens[j, i] >= 3:
            ww = k * pw; field[j, i] = float(np.sum(ww * pv) / np.sum(ww))
P(f"field grid {len(xs)}x{len(ys)}; cells with data {int(np.isfinite(field).sum())}; field range {np.nanmin(field):.0f} .. {np.nanmax(field):.0f} km/s")
# SPARC
atlas = {r["id"]: r for r in csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X33_system_atlas", "x33_atlas.csv"))) if r["class"] == "SPARC"}
sp = []
for r in csv.DictReader(open(os.path.join(EXT, "sesame_sparc.csv"))):
    a = atlas.get(r["sparc_name"])
    if not a or not r["ra_deg"]: continue
    c = SkyCoord(ra=float(r["ra_deg"]) * u.deg, dec=float(r["dec_deg"]) * u.deg).supergalactic
    D = float(a["D_Mpc"]); L = c.sgl.rad; B = c.sgb.rad
    X, Y, Z = D * math.cos(B) * math.cos(L), D * math.cos(B) * math.sin(L), D * math.sin(B)
    res = float(a["resid_dex_can"]) if a["resid_dex_can"] not in ("", "nan") else None
    sp.append(dict(name=r["sparc_name"], x=X, y=Y, z=Z, D=D, res=res, inslice=abs(Z) < 25))
P(f"SPARC placed {len(sp)}; in slice {sum(s['inslice'] for s in sp)}")
# eRASS1 nearby clusters
E = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
names = E.columns.names
zc = "BEST_Z" if "BEST_Z" in names else [n for n in names if n.upper().startswith("BEST_Z") or n.upper() == "Z"][0]
ra = "RA" if "RA" in names else [n for n in names if n.upper().startswith("RA")][0]
de = "DEC" if "DEC" in names else [n for n in names if n.upper().startswith("DEC")][0]
cl = []
for row in E:
    z = float(row[zc])
    if not (0 < z < 160 * H / C): continue
    c = SkyCoord(ra=float(row[ra]) * u.deg, dec=float(row[de]) * u.deg).supergalactic
    R = C * z / H; L = c.sgl.rad; B = c.sgb.rad
    X, Y, Z = R * math.cos(B) * math.cos(L), R * math.cos(B) * math.sin(L), R * math.sin(B)
    cl.append(dict(name=str(row["NAME"]) if "NAME" in names else "", x=X, y=Y, z=Z, zred=z, inslice=abs(Z) < 25))
P(f"eRASS1 clusters with cz/H < 160 Mpc: {len(cl)} (eRASS1 covers the western Galactic hemisphere only); in slice {sum(c['inslice'] for c in cl)}")
res = dict(H=H, slice=dict(sgz=25, R=160), grid=dict(x=xs.tolist(), y=ys.tolist(), sigma=sig,
           field=[[None if not math.isfinite(v_) else round(v_, 1) for v_ in row] for row in field.tolist()]),
           groups=[[round(r["x"], 2), round(r["y"], 2), round(r["vp"]), round(r["ev"]), r["n"]] for r in sl],
           sparc=[[s["name"], round(s["x"], 2), round(s["y"], 2), round(s["z"], 2), s["D"], None if s["res"] is None else round(s["res"], 3)] for s in sp],
           clusters=[[c["name"], round(c["x"], 2), round(c["y"], 2), round(c["z"], 2), round(c["zred"], 4)] for c in cl],
           note="descriptive; v_pec noisy per group (median error printed); field smoothed sigma 10 Mpc")
json.dump(res, open(os.path.join(HERE, "map1_cosmic_river.json"), "w"), separators=(",", ":"))
open(os.path.join(HERE, "map1_cosmic_river.out"), "w").write("\n".join(OUT) + "\n")
P("MAP1 done")
