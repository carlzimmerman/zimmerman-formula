#!/usr/bin/env python3
"""EV1 readings (criteria 71bbb66c0d): the three environment switches S (M1 x_e, M2 membership, M3 hot atmosphere),
read from data on disk, per footing. Writes readings.json only. Grades nothing; reads no offset.
kappa = 1/2 FITTED; footings never pooled; not theory closed. One thread, seconds."""
import os, json, csv, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); RB = os.path.join(REPO, "rebuild_2026_10_22")
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
A0_GX = 1.2e-10; CKMS = 299792.458; H0 = 73.0
Q24 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX24_environment_key", "iter_1", "qx24.json")))
XC = {f: Q24["foot"][f]["key"]["x_c"] for f in A0}

# ---- MCXC (gext_vectors_2026/data/raw/mcxc.tsv)
MC = []
for ln in open(os.path.join(REPO, "gext_vectors_2026", "data", "raw", "mcxc.tsv")):
    t = ln.rstrip("\n").split("\t")
    if len(t) < 8 or not t[0].startswith("J"): continue
    h, m, s = (float(x) for x in t[2].split()); dd, dm, ds = t[3].split()
    sg = -1 if dd.strip().startswith("-") else 1
    ra = 15 * (h + m / 60 + s / 3600); de = sg * (abs(float(dd)) + float(dm) / 60 + float(ds) / 3600)
    MC.append(dict(id=t[0], name=t[1].strip(), ra=ra, dec=de, z=float(t[4]), R500=float(t[7])))
def sep(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(math.radians, (ra1, de1, ra2, de2))
    return math.acos(min(1.0, math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)))
def mcxc_match(ra, de, D, exclude=None):
    hits = []
    for c in MC:
        if exclude and c["id"] == exclude: continue
        Dc = CKMS * c["z"] / H0
        if abs(D - Dc) > 0.25 * Dc: continue
        Rp = sep(ra, de, c["ra"], c["dec"]) * D
        if Rp < 0.05: continue      # the system's own MCXC entry (centred on it): excluded, per the criteria
        if Rp < 2 * c["R500"]: hits.append(dict(id=c["id"], name=c["name"], Rp_Mpc=Rp, R500=c["R500"], D_cl=Dc))
    return hits

R = dict(criteria="71bbb66c0d", note="kappa = 1/2 FITTED; not theory closed", x_c=XC, H0_rule=H0, systems={})
S = R["systems"]

# ---- SPARC
SPT = {}
for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) < 18: continue
    try: SPT[t[0]] = dict(fD=int(t[4]), Vflat=float(t[15]))
    except ValueError: continue
for r in csv.DictReader(open(os.path.join(REPO, "gext_vectors_2026", "data", "gext_vectors.csv"))):
    n = r["name"]; ra, de, D = float(r["ra"]), float(r["dec"]), float(r["D"])
    hits = mcxc_match(ra, de, D); uma = SPT[n]["fD"] == 4
    d = dict(cls="SPARC", fD=SPT[n]["fD"], Vflat=SPT[n]["Vflat"], mcxc=hits)
    for f, a0 in A0.items():
        xn = 10 ** float(r["log_eN_noclu"]) * A0_GX / a0; xm = 10 ** float(r["log_eN_maxclu"]) * A0_GX / a0
        d[f] = dict(x_e_noclu=xn, x_e_maxclu=xm, M1=int(xn >= XC[f]), M1_maxclu=int(xm >= XC[f]),
                    M2=int(uma or bool(hits)), M3=int(bool(hits)), M3_bracket_vflat200=int(bool(hits) or SPT[n]["Vflat"] >= 200))
    S["SPARC:" + n] = d

# ---- ellipticals (QX24 positions, Humphrey D); x_e from QX24 (recomputed and checked in ev1.py KA2)
HUMD = {}
for ln in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")):
    if ln.startswith("#") or ln.startswith("name"): continue
    t = ln.rstrip("\n").split("\t"); HUMD[t[0]] = float(t[3])
for nm, (ra, de, src) in Q24["ell_positions"].items():
    hits = mcxc_match(ra, de, HUMD[nm]); d = dict(cls="elliptical", pos=[ra, de, src], D=HUMD[nm], mcxc=hits)
    for f in A0:
        p = Q24["foot"][f]["T2"]["per"][nm]
        d[f] = dict(x_e_noclu=p["x_e_noclu"], x_e_maxclu=p["x_e_maxclu"], M1=int(p["x_e_noclu"] >= XC[f]),
                    M1_maxclu=int(p["x_e_maxclu"] >= XC[f]), M2=int(bool(hits)), M3=1)
    S["ELL:" + nm] = d

# ---- dSphs (LW1 classes, X1 x_e_mid / host / d_host)
LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))
X1 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv")))}
for f in A0:
    for n, s in LW["footings"][f]["per_system"].items():
        x = X1.get((f, n)); key = "DSPH:" + n; d = S.setdefault(key, dict(cls=s["cls"]))
        if x is None:
            d[f] = dict(x_e=None, M1=None, M2=None, M3=None, note="not in X1"); continue
        host = x["host"]; dh = float(x["d_host_kpc"]); xe = float(x["x_e_mid"])
        sat = host in ("MW", "M31") and s["cls"] != "LG field"
        d[f] = dict(x_e=xe, x_e_LW1=s["xe"], host=host, d_host_kpc=dh, M1=int(xe >= XC[f]), M2=int(sat), M3=int(sat and dh <= 300.0))

# ---- Coma UDGs (S1)
coma = [c for c in MC if c["id"] == "J1259.7+2756"][0]
for r in csv.DictReader(open(os.path.join(RB, "S1_v3_hosted_small", "s1_coma_per_galaxy.csv"))):
    f = r["footing"]; key = "UDG:" + r["name"]; d = S.setdefault(key, dict(cls="Coma UDG"))
    dm = float(r["d_mean_kpc"]) / 1e3; inside = dm < 2 * coma["R500"]
    d[f] = dict(x_e=float(r["x_e_dmean"]), d_mean_Mpc=dm, inside_2R500=inside, M1=int(float(r["x_e_dmean"]) >= XC[f]),
                M2=int(inside), M3=int(inside))

# ---- Solar System: MW field at the Sun from Eilers+2019 (row nearest 8.1 kpc)
rows = [l.split() for l in open(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv")) if l[0].isdigit()]
rr = min(rows, key=lambda t: abs(float(t[0]) - 8.1)); R0 = float(rr[0]); vc = float(rr[1])
gsun = (vc * 1e3) ** 2 / (R0 * 3.0856775814913673e19)
S["SS:Sun"] = dict(cls="Solar System", R0_kpc=R0, vc_kms=vc, g_MW=gsun,
                   **{f: dict(x_e=gsun / A0[f], M1=int(gsun / A0[f] >= XC[f]), M2=1, M3=1) for f in A0})

# ---- fixed by the criteria
S["XCOP:*"] = dict(cls="X-COP", **{f: dict(M1=None, M2=0, M3=1) for f in A0})
S["GROUP:*"] = dict(cls="groups", **{f: dict(M1=None, M2=0, M3=1) for f in A0})
S["KIDS:early"] = dict(cls="KiDS isolated", **{f: dict(M1=0, M2=0, M3=None) for f in A0})
S["KIDS:late"] = dict(cls="KiDS isolated", **{f: dict(M1=0, M2=0, M3=None) for f in A0})

# ---- summary
summ = {}
for f in A0:
    sm = {}
    for cls in ("SPARC", "elliptical", "MW classical", "bright M31", "LG field", "MW ultra-faint", "M31 others", "Coma UDG"):
        v = [d[f] for d in S.values() if d.get("cls") == cls and f in d]
        sm[cls] = {m: dict(n1=sum(1 for x in v if x.get(m) == 1), n0=sum(1 for x in v if x.get(m) == 0), nNone=sum(1 for x in v if x.get(m) is None))
                   for m in ("M1", "M2", "M3")}
    summ[f] = sm
R["summary"] = summ
json.dump(R, open(os.path.join(HERE, "readings.json"), "w"), indent=1)
for f in A0:
    print(f"[{f}] x_c {XC[f]:.4f}")
    for cls, v in summ[f].items(): print(f"   {cls:15s} " + "  ".join(f"{m}: 1={c['n1']} 0={c['n0']} None={c['nNone']}" for m, c in v.items()))
print("SPARC MCXC matches:", {k[6:]: [h["name"] for h in d["mcxc"]] for k, d in S.items() if k.startswith("SPARC:") and d["mcxc"]})
print("Ellipticals MCXC matches:", {k[4:]: [(h["name"], round(h["Rp_Mpc"], 2)) for h in d["mcxc"]] for k, d in S.items() if k.startswith("ELL:")})
print(f"Sun: R0 {R0} vc {vc} g {gsun:.3e} -> x_e canonical {gsun/A0['canonical']:.2f}")
print("kappa = 1/2 FITTED; not theory closed.")
