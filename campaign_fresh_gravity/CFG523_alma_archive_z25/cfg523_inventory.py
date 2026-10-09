"""CFG523 inventory: public ALMA products covering CO/[CI]/[CII] of z 2-3 parent discs, with a predicted reach y = g_N(2 R_e)/a0.
Criteria: FROZEN_CRITERIA.md (429b1d7a6). Metadata only (ALMA TAP ivoa.obscore); rows cached in ../../../_external_data/cfg523_work/ (sha256 in FETCH_LOG.md).
Run: nice -n 10 python3 cfg523_inventory.py ; MUTATE=1 shifts every parent +60" in Dec (G2 matches must fall to <= 10% of the main run; rc 1).
"""
import csv, hashlib, io, json, math, os, re, subprocess, sys, time
import numpy as np
from scipy.special import i0, i1, k0, k1
from astropy.cosmology import Planck18

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg523_work"))
os.makedirs(WORK, exist_ok=True)
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
DDEC = 60 / 3600 if MUTATE else 0.0
FOOT = {"A": 9.36e-11, "B": 1.13e-10}
G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; C_KMS = 299792.458
LINES = {"CO(3-2)": 345.796, "CO(4-3)": 461.041, "CO(5-4)": 576.268, "CO(6-5)": 691.473, "CO(7-6)": 806.652,
         "[CI](1-0)": 492.161, "[CI](2-1)": 809.342, "[CII]": 1900.537}
out, checks = [], []
def say(s=""):
    print(s); out.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")
def sep(ra1, de1, ra2, de2):
    return 3600 * np.hypot((np.asarray(ra1) - ra2) * np.cos(np.radians(de2)), np.asarray(de1) - de2)
def fl(x):
    try: return float(x)
    except (TypeError, ValueError): return float("nan")

# ---------------- baryon reach predictor (G3) ----------------
def mu_gas(z, lm):          # Tacconi+2018 main-sequence scaling (predictor only)
    return 10 ** (0.12 - 3.62 * (math.log10(1 + z) - 0.66) ** 2 - 0.35 * (lm - 10.7))
def g_freeman(M_msun, Rd_kpc, R_kpc):
    y = R_kpc / (2 * Rd_kpc)
    v2 = 2 * G * M_msun * MSUN / (Rd_kpc * KPC) * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / (R_kpc * KPC)
# DATED NOTE 2026-10-09: the first run's C1 (10 R_d within 3% of a point mass) was mis-specified (a thin disc exceeds Kepler by ~6% there); replaced by the far-field limit.
check("C1 Freeman disc: g at 100 R_d within 0.5% of point mass", abs(g_freeman(1e11, 1, 100) / (G * 1e11 * MSUN / (100 * KPC) ** 2) - 1) < 0.005,
      f"{g_freeman(1e11, 1, 100) / (G * 1e11 * MSUN / (100 * KPC) ** 2):.4f}")
check("C2 CO(3-2) at z 2.2 -> 108.06 GHz", abs(LINES["CO(3-2)"] / 3.2 - 108.06) < 0.01, f"{LINES['CO(3-2)'] / 3.2:.3f}")

# ---------------- parents ----------------
def sexa(s, hours):
    s = s.replace("[+]", "+").replace("[", "").replace("]", "").replace("−", "-").strip()
    sign = -1 if s.startswith("-") else 1
    p = [float(x) for x in re.split(r"[:\s]+", s.lstrip("+-").strip())]
    return sign * (p[0] + p[1] / 60 + p[2] / 3600) * (15 if hours else 1)
DA = os.path.join(REPO, "data_assembly")
P = []
for r in csv.DictReader(open(os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv"))):
    z = fl(r["Z"]); lm = fl(r["LMSTAR"]); rh = fl(r["RHALF"])
    if math.isfinite(z):
        kpc_as = Planck18.angular_diameter_distance(z).value * 1e3 * math.pi / 648000 if math.isfinite(z) and z > 0 else float("nan")
        P.append(dict(id=r["ID"], src="KMOS3D", ra=fl(r["RA"]), dec=fl(r["DEC"]), z=z, lm=lm, re_kpc=rh * kpc_as))
sz = {r["source"]: fl(r["Re_kpc_1G"]) for r in csv.DictReader(open(os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table5_sizes.csv")))}
for r in csv.DictReader(open(os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table1_sample.csv"))):
    P.append(dict(id=r["source"], src="SINS-AO", ra=sexa(r["ra"], True), dec=sexa(r["dec"], False), z=fl(r["z_Halpha"]),
                  lm=math.log10(fl(r["Mstar_1e10Msun"]) * 1e10) if fl(r["Mstar_1e10Msun"]) > 0 else float("nan"), re_kpc=sz.get(r["source"], float("nan"))))
props = {r["id"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "alpaka1_properties.csv")))}
for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "alpaka1_sample.csv"))):
    m = fl(props.get(r["id"], {}).get("mstar_1e10msun"))
    P.append(dict(id="ALPAKA-" + r["id"] + ":" + r["name"], src="ALPAKA", ra=fl(r["ra_deg"]), dec=fl(r["dec_deg"]), z=fl(r["z"]),
                  lm=math.log10(m * 1e10) if m > 0 else float("nan"), re_kpc=float("nan")))
P = [p for p in P if 2.0 <= p["z"] <= 3.0]
GAL = []
for p in P:
    hit = next((g for g in GAL if sep(g["ra"], g["dec"] - DDEC, p["ra"], p["dec"]) < 1.0), None)
    if hit:
        hit["srcs"].add(p["src"]); hit["ids"].append(p["id"])
        for k in ("lm", "re_kpc"):
            if not math.isfinite(hit[k]) and math.isfinite(p[k]): hit[k] = p[k]
    else:
        GAL.append(dict(ra=p["ra"], dec=p["dec"] + DDEC, z=p["z"], lm=p["lm"], re_kpc=p["re_kpc"], srcs={p["src"]}, ids=[p["id"]]))
say(f"G1 parents 2.0 <= z <= 3.0: {len(P)} rows -> {len(GAL)} unique (KMOS3D {sum('KMOS3D' in g['srcs'] for g in GAL)}, "
    f"SINS-AO {sum('SINS-AO' in g['srcs'] for g in GAL)}, ALPAKA {sum('ALPAKA' in g['srcs'] for g in GAL)})")
for g in GAL:
    g["kpc_as"] = Planck18.angular_diameter_distance(g["z"]).value * 1e3 * math.pi / 648000
    if math.isfinite(g["lm"]) and math.isfinite(g["re_kpc"]) and g["re_kpc"] > 0:
        mu = mu_gas(g["z"], g["lm"]); Mb = 10 ** g["lm"] * (1 + mu); Rd = g["re_kpc"] / 1.678
        g.update(mu=mu, Mbar=Mb, y_out={k: g_freeman(Mb, Rd, 2 * g["re_kpc"]) / a for k, a in FOOT.items()},
                 y_in={k: g_freeman(Mb, Rd, 0.5 * g["re_kpc"]) / a for k, a in FOOT.items()},
                 y_out_gx2={k: g_freeman(10 ** g["lm"] * (1 + 2 * mu), Rd, 2 * g["re_kpc"]) / a for k, a in FOOT.items()},
                 y_out_gh={k: g_freeman(10 ** g["lm"] * (1 + 0.5 * mu), Rd, 2 * g["re_kpc"]) / a for k, a in FOOT.items()})
    else:
        g.update(mu=None, Mbar=None, y_out=None, y_in=None)

# ---------------- ALMA rows (cached) ----------------
COLS = ("proposal_id,obs_id,target_name,s_ra,s_dec,s_fov,s_resolution,frequency_support,sensitivity_10kms,data_rights,obs_release_date,"
        "member_ous_uid,band_list,t_exptime,is_mosaic,pi_name,scientific_category,science_keyword,obs_title")
def tap(adql):
    for _ in range(4):
        r = subprocess.run(["curl", "-sSL", "-m", "900", "https://almascience.eso.org/tap/sync", "--data-urlencode", "REQUEST=doQuery", "--data-urlencode", "LANG=ADQL",
                            "--data-urlencode", "FORMAT=csv", "--data-urlencode", "QUERY=" + adql], capture_output=True, text=True)
        if r.stdout.startswith("proposal_id") or r.stdout.startswith("n"):
            return r.stdout
        time.sleep(10)
    raise SystemExit("ALMA TAP failed: " + r.stdout[:300] + r.stderr[:300])
cache = os.path.join(WORK, "alma_rows_parents.csv")
if not os.path.exists(cache):
    if MUTATE:
        raise SystemExit("run the main pass first (it builds the ALMA cache)")
    groups = []
    for g in GAL:
        h = next((x for x in groups if sep(x["ra"], x["dec"], g["ra"], g["dec"]) < 0.7 * 3600), None)
        (h["m"].append(g) if h else groups.append(dict(ra=g["ra"], dec=g["dec"], m=[g])))
    txt_all = None
    for x in groups:
        ra = float(np.mean([m["ra"] for m in x["m"]])); de = float(np.mean([m["dec"] for m in x["m"]]))
        rad = max(sep(ra, de, m["ra"], m["dec"]) for m in x["m"]) / 3600 + 0.05
        txt = tap(f"SELECT {COLS} FROM ivoa.obscore WHERE 1=INTERSECTS(s_region, CIRCLE('ICRS', {ra}, {de}, {rad})) AND s_resolution <= 0.6")
        body = txt.split("\n", 1)
        txt_all = txt if txt_all is None else txt_all + (body[1] if len(body) > 1 else "")
        say(f"  ALMA group RA {ra:.3f} Dec {de:+.3f} r {rad:.3f} deg: {txt.count(chr(10)) - 1} rows")
    open(cache, "w").write("\n".join(l for l in txt_all.split("\n") if l.strip()) + "\n")
AL = list(csv.DictReader(open(cache)))
say(f"ALMA rows (s_resolution <= 0.6\") in the parent fields: {len(AL)}; cache sha256 {hashlib.sha256(open(cache, 'rb').read()).hexdigest()[:16]}")
ara = np.array([fl(a["s_ra"]) for a in AL]); ade = np.array([fl(a["s_dec"]) for a in AL]); afov = np.nan_to_num(np.array([fl(a["s_fov"]) for a in AL]))
WIN = re.compile(r"\[([\d.]+)\.\.([\d.]+)GHz,[^,]*,([\d.]+)(u|m)Jy/beam@10km/s")
def windows(fs):
    return [(float(a), float(b), float(s) * (1e-3 if u == "u" else 1.0)) for a, b, s, u in WIN.findall(fs)]
for g in GAL:
    d = sep(ara, ade, g["ra"], g["dec"])
    hits = []
    for i in np.where(d <= 0.5 * 3600 * afov)[0]:
        a = AL[i]
        for ln, nu in LINES.items():
            nuo = nu / (1 + g["z"]); m = nuo * 300 / C_KMS
            for lo, hi, s in windows(a["frequency_support"]):
                if lo + m <= nuo <= hi - m:
                    hits.append(dict(proposal=a["proposal_id"], line=ln, res=round(fl(a["s_resolution"]), 3), sens_mJy=round(s, 3), rights=a["data_rights"],
                                     ous=a["member_ous_uid"], released=a["obs_release_date"][:10], band=a["band_list"], target=a["target_name"],
                                     texp_s=round(fl(a["t_exptime"]), 1), dist_as=round(float(d[i]), 2), pi=a["pi_name"], title=a["obs_title"]))
    uniq = {}
    for h in hits:
        k = (h["proposal"], h["line"], h["ous"])
        if k not in uniq or h["sens_mJy"] < uniq[k]["sens_mJy"]: uniq[k] = h
    g["cov_all"] = sorted(uniq.values(), key=lambda h: (h["res"], h["sens_mJy"]))
    g["cov_pub03"] = [h for h in g["cov_all"] if h["rights"] == "Public" and h["res"] <= 0.30]
    g["cov_pub06"] = [h for h in g["cov_all"] if h["rights"] == "Public" and 0.30 < h["res"] <= 0.60]
    g["cov_prop"] = [h for h in g["cov_all"] if h["rights"] != "Public"]
    g["G2"] = bool(g["cov_pub03"])
    g["G3"] = g["y_out"] is not None and g["y_out"]["A"] <= 2.0
    g["G3_relaxed"] = g["y_out"] is not None and g["y_out"]["A"] <= 4.0
    g["G4"] = g["G2"] and math.isfinite(g["re_kpc"]) and 2 * g["re_kpc"] / g["kpc_as"] >= 1.5 * min(h["res"] for h in g["cov_pub03"])
n2 = sum(g["G2"] for g in GAL); n3 = sum(g["G3"] for g in GAL); nb = sum(g["y_out"] is not None for g in GAL)
SL = sorted([g for g in GAL if g["G2"] and g["G3"] and g["G4"]], key=lambda g: (g["y_out"]["A"], g["cov_pub03"][0]["sens_mJy"]))
SLr = sorted([g for g in GAL if g["G2"] and g["G3_relaxed"] and g["G4"] and not g["G3"]], key=lambda g: g["y_out"]["A"])
say(f"G2 (public, covered line, <= 0.30\"): {n2}   [0.30-0.60\" only: {sum((not g['G2']) and bool(g['cov_pub06']) for g in GAL)}; "
    f"proprietary-only coverage: {sum((not g['cov_pub03']) and (not g['cov_pub06']) and bool(g['cov_prop']) for g in GAL)}]")
say(f"G3 (y_pred(2 R_e) <= 2 at 9.36e-11): {n3} of {nb} with M* and R_e;  G2*G3: {sum(g['G2'] and g['G3'] for g in GAL)};  "
    f"G2*G3*G4 SHORTLIST: {len(SL)};  relaxed (y <= 4) extra: {len(SLr)}")
def row(g):
    h = g["cov_pub03"][0]
    lines_ = sorted({x["line"] for x in g["cov_pub03"]}); progs = sorted({x["proposal"] for x in g["cov_pub03"]})
    yo = g["y_out"]; yi = g["y_in"]
    return (f"  {'/'.join(g['ids'])[:40]:40s} z {g['z']:.3f} logM* {g['lm']:.2f} mu {g['mu']:.2f} R_e {g['re_kpc']:.2f} kpc ({g['re_kpc']/g['kpc_as']:.2f}\")  "
            f"y(2Re) {yo['A']:.2f}/{yo['B']:.2f}  y(Re/2) {yi['A']:.1f}  best {h['res']}\" {h['sens_mJy']} mJy/b  lines {lines_} progs {progs}")
say("\nSHORTLIST (G1-G4), ranked by y_pred(2 R_e) at 9.36e-11:")
for g in SL: say(row(g))
say("\nRelaxed (2 < y_pred <= 4; reported, not shortlisted):")
for g in SLr: say(row(g))
say("\nG2 parents failing G3 or G4 (y_pred / reason):")
for g in [g for g in GAL if g["G2"] and g not in SL and g not in SLr]:
    say(f"  {'/'.join(g['ids'])[:40]:40s} z {g['z']:.3f} y(2Re) {('%.2f' % g['y_out']['A']) if g['y_out'] else 'no M*/R_e'} G3 {g['G3']} G4 {g['G4']} "
        f"lines {sorted({x['line'] for x in g['cov_pub03']})} res {g['cov_pub03'][0]['res']}")
if MUTATE:
    base = json.load(open(os.path.join(HERE, "cfg523_inventory_results.json")))["counts"]["G2"]
    check("MUTATE premise: G2 falls to <= 10% of the main run", n2 <= 0.10 * max(base, 1), f"{n2} vs main {base}")
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": n2})
else:
    check("C3 every parent evaluated", all("G2" in g for g in GAL), len(GAL))
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} checks pass" + ("  (MUTATE)" if MUTATE else ""))
ser = [{k: (sorted(v) if isinstance(v, set) else v) for k, v in g.items()} for g in GAL]
json.dump({"lane": "CFG523", "stage": "inventory", "mutate": MUTATE, "footings": FOOT,
           "counts": dict(parents=len(GAL), with_baryons=nb, G2=n2, G3=n3, shortlist=len(SL), relaxed=len(SLr)),
           "shortlist": [s for s in ser if any(s["ids"] == g["ids"] for g in SL)],
           "relaxed": [s for s in ser if any(s["ids"] == g["ids"] for g in SLr)],
           "g2_all": [s for s in ser if s["G2"]],
           "cov06_only": [dict(ids=s["ids"], z=s["z"], y_out=s["y_out"], cov=s["cov_pub06"][:3]) for s in ser if (not s["G2"]) and s["cov_pub06"]],
           "checks": checks}, open(os.path.join(HERE, f"cfg523_inventory_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg523_inventory{TAG}.out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if n == len(checks) else 1)
