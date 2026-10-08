#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG492 part A: inventory and cross-match of every on-disk catalogue that can put SEVERAL independent measurements on the SAME
object.  No downloads.  No law is scored here; this script only counts overlaps and records which quantity each source supplies.

Domains and match rules (stated before any count was read):
  HIGH-Z (z > 0.5): union-find over all entries.  Edge if (a) the alias-normalised names are equal, or (b) both have coordinates,
     separation <= 1.0 arcsec and, when both have z, |dz| <= 0.01 (1 + z).  Alias normalisation: upper case; spaces, '_' and '-'
     removed; 'DEEP3A' -> 'D3A'; field prefixes 'Q\d{4}' and 'SSA22A?' dropped for BX/BM/MD names.  RC100/RC41/Genzel+17 carry no
     coordinates; they are placed through these names only.
  LOCAL GALAXIES (SPARC reference, 175): name (normalised catalogue designation) or coordinates <= 30 arcsec with |dcz| <= 300 km/s
     when both velocities exist (<= 30 arcsec alone otherwise).
  EARLY TYPES (SLUGGS + PN + X-ray + ATLAS3D): NGC number.
  CLUSTERS (X-COP reference, 12): name; coordinates <= 3 arcmin with |dz| <= 0.01 for the coordinate-only catalogues.
Quantity codes:  K_* = kinematics (tracer: Ha-KMOS, Ha-SINF(-AO), Ha-OSIRIS, Ha-JWST, CO, CII, HI, STAR, GC, PN), G = measured gas
(CO / [CI] / dust / HI), M = stellar mass, X = X-ray mass, L = lensing, D = galaxy-dynamics cluster mass, SZ = SZ mass.
Sources that re-use the SAME data are flagged as not independent (RC100, RC41, Genzel+17 and our KMOS3D cube fits all use KMOS3D or
SINS Ha cubes).

MUTATE=1: every coordinate of the second catalogue in each pair is shifted by +60 arcsec in Dec (name matches untouched); the
coordinate-only overlaps must collapse.  Separate outputs (_MUTATE).
"""
import os, re, sys, json, math, csv, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
RD = os.path.join(REPO, "real_research", "data")
DA = os.path.join(REPO, "data_assembly")
MUTATE = os.environ.get("MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


def fnum(x):
    try:
        return float(x)
    except Exception:
        return float("nan")


def hms(s):
    s = s.strip().replace("h", " ").replace("m", " ").replace("s", " ").replace(":", " ")
    p = [float(x) for x in s.split()]
    return 15.0 * (p[0] + p[1] / 60 + (p[2] if len(p) > 2 else 0) / 3600)


def dms(s):
    s = s.strip().replace("[", "").replace("]", "").replace(" ", " ")
    sg = -1.0 if s.lstrip().startswith("-") else 1.0
    s = s.replace("+", " ").replace("-", " ").replace(":", " ").replace("d", " ").replace("'", " ").replace('"', " ")
    p = [float(x) for x in s.split()]
    return sg * (p[0] + p[1] / 60 + (p[2] if len(p) > 2 else 0) / 3600)


def vizier(path):
    rows = [l.rstrip("\n") for l in open(path, encoding="latin-1") if l.strip() and not l.startswith("#")]
    k = next(i for i, l in enumerate(rows) if l.replace("\t", "").strip() and set(l.replace("\t", "").strip()) <= set("-"))
    hdr = [h.strip() for h in rows[k - 2].split("\t")]
    return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in rows[k + 1:]]


def rcsv(path):
    return list(csv.DictReader(open(path, encoding="utf-8", errors="replace")))


def sep_arcsec(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    s = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(s, 0, 1)))) * 3600


def hz_alias(n):
    n = n.upper().replace(" ", "").replace("_", "").replace("-", "")
    n = n.replace("DEEP3A", "D3A")
    n = re.sub(r"^Q\d{4}(?=(BX|BM|MD))", "", n)
    n = re.sub(r"^SSA22A?(?=MD)", "", n)
    n = re.sub(r"^HDF(?=BX)", "", n)
    return n


def loc_alias(n):
    n = n.upper().replace(" ", "").replace("_", "").replace("-", "")
    m = re.match(r"^(NGC|UGC|IC|DDO|ESO|UGCA|PGC|F|D)0*(\d.*)$", n)
    if m:
        return m.group(1) + m.group(2)
    return n


SHIFT = 60.0 / 3600 if MUTATE else 0.0   # applied to the 'other' side of every coordinate match

# =====================================================================================================================
# HIGH-Z
# =====================================================================================================================
HZ = []   # entries: dict(cat, name, ra, dec, z, q)


def add(cat, name, ra, dec, z, q):
    HZ.append(dict(cat=cat, name=str(name), ra=fnum(ra), dec=fnum(dec), z=fnum(z), q=q))


CATS_HZ = {}   # cat -> (description, quantities, independent-data group)
def cat(name, desc, q, grp):
    CATS_HZ[name] = (desc, q, grp)


cat("KMOS3D_cat", "KMOS3D catalogue (Wisnioski+19), positions, z, SED M*", "M", "KMOS3D")
for r in rcsv(os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv")):
    add("KMOS3D_cat", r["ID"], r["RA"], r["DEC"], r["Z"], "M")
POS_K3D = {hz_alias(e["name"]): e for e in HZ if e["cat"] == "KMOS3D_cat"}

cat("KMOS3D_fit", "our KMOS3D cube fits (CFG270; 192 discs, arctan V(r), PSF-limited)", "K_Ha-KMOS", "KMOS3D")
for r in rcsv(os.path.join(DA, "kmos3d_cubes", "k3d_fits_main_final_flags.csv")):
    e = POS_K3D.get(hz_alias(r["ID"]))
    add("KMOS3D_fit", r["ID"], e["ra"] if e else "nan", e["dec"] if e else "nan", r["Z"], "K_Ha-KMOS")

cat("SINS_AO", "SINS/zC-SINF AO sample (Foerster Schreiber+18) + our AO profiles", "K_Ha-SINF-AO,M", "SINS")
for r in rcsv(os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table1_sample.csv")):
    add("SINS_AO", r["source"], hms(r["ra"]), dms(r["dec"]), r["z_Halpha"], "K_Ha-SINF-AO,M")
POS_SINS = {hz_alias(e["name"]): e for e in HZ if e["cat"] == "SINS_AO"}

cat("SINS2009", "SINS seeing-limited dynamics (Foerster Schreiber+09)", "K_Ha-SINF", "SINS")
for r in rcsv(os.path.join(DA, "high_z_tf_tables", "sins2009_dynamics.csv")):
    e = POS_SINS.get(hz_alias(r["name"]))
    add("SINS2009", r["name"], e["ra"] if e else "nan", e["dec"] if e else "nan", e["z"] if e else "nan", "K_Ha-SINF")

cat("PHIBSS13", "PHIBSS 2013 (Tacconi+13) CO(3-2) gas, M*, CO-based V_rot", "G_CO,M,K_CO", "PHIBSS13")
for r in rcsv(os.path.join(DA, "kmos3d_phibss", "phibss13_joined.csv")):
    q = "M,K_CO" + ("" if r.get("co_upper_limit", "").strip().lower() in ("true", "1") else ",G_CO")
    add("PHIBSS13", r["name"], r["ra_deg"], r["dec_deg"], r["z_co"], q)
POS_PH13 = {hz_alias(e["name"]): e for e in HZ if e["cat"] == "PHIBSS13"}

cat("PHIBSS2", "PHIBSS2 z 0.5-0.8 (Freundlich+19) CO(2-1) gas, M*, HST sizes, integrated CO FWHM", "G_CO,M", "PHIBSS2")
for r in rcsv(os.path.join(DA, "phibss2_z05_08", "phibss2_z05_08.csv")):
    q = "M" + ("" if r["flag"] == "nondetection" else ",G_CO")
    add("PHIBSS2", r["id"], hms(r["ra"]), dms(r["dec"]), r["z_optical"], q)

cat("NOEMA3D", "NOEMA3D (Jolly+26) CO rotation curves + resolved CO/[CI]/dust + M*", "K_CO,G_CO,M", "NOEMA3D")
for r in rcsv(os.path.join(DA, "noema3d", "noema3d_per_galaxy.csv")):
    add("NOEMA3D", r["id"], r["ra_deg"], r["dec_deg"], r["z"], "K_CO,G_CO,M")


def place(name):
    a = hz_alias(name)
    for d in (POS_K3D, POS_SINS, POS_PH13):
        if a in d:
            return d[a]["ra"], d[a]["dec"]
    return float("nan"), float("nan")


cat("RC100", "RC100 (Nestor Shachar+23) V_c(R_e), f_DM, M_bar (KMOS3D/SINS/LUCI/NOEMA data; model values)", "K_model", "KMOS3D+SINS")
for r in rcsv(os.path.join(RD, "rc100_nestorshachar2023_table3_CORRECTED.csv")):
    ra, de = place(r["name"])
    add("RC100", r["name"], ra, de, r["z"], "K_model")
cat("RC41", "RC41 (Price+21) model fits; gas mixes measured CO and scaling relations (no flag)", "K_model,M", "KMOS3D+SINS")
for r in rcsv(os.path.join(DA, "price2021_rc41", "price2021_rc41.csv")):
    ra, de = place(r["id"])
    add("RC41", r["id"], ra, de, r["z"], "K_model,M")
cat("Genzel17", "Genzel+17 six deep outer curves (digitised CFG400)", "K_Ha-deep", "KMOS3D+SINS")
for nm in sorted({r["galaxy"] for r in rcsv(os.path.join(REPO, "campaign_fresh_gravity", "CFG400_genzel17_selfcal", "cfg400_points.csv"))}):
    ra, de = place(nm)
    add("Genzel17", nm, ra, de, "nan", "K_Ha-deep")
cat("Lelli23", "Lelli+23 ALMA CO/[CI] rotation curves + mass models", "K_CO,G_CO", "Lelli23")
for nm in ("zC-400569", "zC-488879"):
    ra, de = place(nm)
    add("Lelli23", nm, ra, de, "nan", "K_CO,G_CO")

cat("KURVS", "KURVS-CDFS (Puglisi+23) deep Ha curves to 6 R_d", "K_Ha-KMOS-deep,M", "KURVS")
for r in rcsv(os.path.join(DA, "arxiv_tables", "kurvs_positions", "kurvs_positions.csv")):
    add("KURVS", "KURVS" + r["kurvs_id"], r["ra_deg"], r["dec_deg"], r["z_halpha"], "K_Ha-KMOS-deep,M")
cat("ALPAKA", "ALPAKA I (Rizzo+23) ALMA CO/[CI] curves, L' (gas needs alpha)", "K_CO,G_CO,M", "ALPAKA")
for r in rcsv(os.path.join(DA, "arxiv_tables", "alpaka1_sample.csv")):
    add("ALPAKA", r["name"], r["ra_deg"], r["dec_deg"], r["z"], "K_CO,G_CO,M")
cat("CRISTAL", "ALMA-CRISTAL (z 4-6) [CII] kinematics, M*", "K_CII,M", "CRISTAL")
for r in rcsv(os.path.join(DA, "arxiv_tables", "cristal2025_sample.csv")):
    add("CRISTAL", r["name"], r["ra_deg"], r["dec_deg"], r["z_cii"], "K_CII,M")
cat("MSA3D", "MSA-3D JWST slit-stepping Ha kinematics", "K_Ha-JWST,M", "MSA3D")
for r in rcsv(os.path.join(DA, "arxiv_tables", "msa3d_galaxies.csv")):
    add("MSA3D", "MSA3D_" + r["id"], r["ra_deg"], r["dec_deg"], r["z"], "K_Ha-JWST,M")
cat("KROSS", "KROSS (Harrison+17 v2) Ha KMOS z~0.9", "K_Ha-KMOS,M", "KROSS")
for r in rcsv(os.path.join(DA, "high_z_tf_tables", "kross_v2.csv")):
    add("KROSS", r["name"], r["ra_deg"], r["dec_deg"], r["z_halpha"], "K_Ha-KMOS,M")
cat("GOODSALMA2", "GOODS-ALMA 2.0 1.1 mm continuum (dust -> gas), M*", "G_dust,M", "GOODSALMA2")
for r in rcsv(os.path.join(DA, "goodsalma_crossmatch", "goodsalma2_catalogue.csv")):
    add("GOODSALMA2", r["id"], r["ra_deg"], r["dec_deg"], r["z"], "G_dust,M")
cat("ACE", "ACE z~2.3 COSMOS ALMA CO(3-2) + dust + M*", "G_CO,M", "ACE")
for r in rcsv(os.path.join(DA, "multitracer_gas", "ace_dust_2609.21040.csv")):
    add("ACE", "ACE" + r["id"], r["ra"], r["dec"], r["z"], "G_CO,M")
cat("Bourne19", "Bourne+19 z~1 [CI]+CO+dust, M*", "G_CO,M", "Bourne19")
for r in rcsv(os.path.join(DA, "multitracer_gas", "bourne2019_z1_CI_CO_dust.csv")):
    add("Bourne19", "B19_" + r["cid"], hms(r["ra"]), dms(r["dec"]), r["z"], "G_CO,M")
cat("RO23", "Roman-Oliveira+23 [CII] discs z~4.3", "K_CII,G_CO", "RO23")
for r in rcsv(os.path.join(DA, "arxiv_tables", "romanoliveira2023_sample.csv")):
    add("RO23", r["id"], hms(r["ra"]), dms(r["dec"]), r["z"], "K_CII,G_CO")
cat("MIGHTEE_hz", "MIGHTEE-HI z 0.25-0.5 HI detections", "G_HI,K_HI-width,M", "MIGHTEE")
for r in rcsv(os.path.join(DA, "mightee_hi_highz", "mightee_hi_highz.csv")):
    add("MIGHTEE_hz", "MHz" + r["id"], hms(r["ra"]), dms(r["dec"]), r["z"], "G_HI,K_HI-width,M")
cat("ALMA_arch", "ALMA archive rows (CFG403 metadata; COVERAGE of a line/continuum, not a measured gas mass)", "G_cov", "ALMA_arch")
_alma = rcsv(os.path.join(EXT, "cfg403_work", "alma_rows.csv"))
seen = set()
for r in _alma:
    k = (round(fnum(r["s_ra"]), 4), round(fnum(r["s_dec"]), 4))
    if k in seen:
        continue
    seen.add(k)
    add("ALMA_arch", r["target_name"], r["s_ra"], r["s_dec"], "nan", "G_cov")

# --------------------------------------------------- union-find
N = len(HZ)
par = list(range(N))
def fnd(i):
    while par[i] != i:
        par[i] = par[par[i]]; i = par[i]
    return i
def uni(i, j):
    a, b = fnd(i), fnd(j)
    if a != b:
        par[b] = a

ali = {}
for i, e in enumerate(HZ):
    if e["cat"] in ("ALMA_arch",):
        continue
    ali.setdefault(hz_alias(e["name"]), []).append(i)
for k, ii in ali.items():
    for j in ii[1:]:
        uni(ii[0], j)
RA = np.array([e["ra"] for e in HZ]); DE = np.array([e["dec"] for e in HZ]); Z = np.array([e["z"] for e in HZ])
CATI = np.array([e["cat"] for e in HZ])
ok = np.isfinite(RA) & np.isfinite(DE)
idx = np.where(ok)[0]
# grid hash on 2 arcsec cells
cell = 2.0 / 3600
grid = {}
for i in idx:
    grid.setdefault((int(math.floor(RA[i] * math.cos(math.radians(DE[i])) / cell)), int(math.floor(DE[i] / cell))), []).append(i)
n_coord_edges = 0
for i in idx:
    # MUTATE: compare entry i (unshifted) against shifted positions of all others: emulate by shifting the query position
    rq, dq = RA[i], DE[i] + SHIFT
    cx, cy = int(math.floor(rq * math.cos(math.radians(dq)) / cell)), int(math.floor(dq / cell))
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for j in grid.get((cx + dx, cy + dy), []):
                if j <= i and not MUTATE:
                    continue
                if j == i or CATI[j] == CATI[i]:
                    continue
                s = sep_arcsec(rq, dq, RA[j], DE[j])
                if s <= 1.0:
                    if np.isfinite(Z[i]) and np.isfinite(Z[j]) and abs(Z[i] - Z[j]) > 0.01 * (1 + Z[i]):
                        continue
                    uni(i, j); n_coord_edges += 1

comps = {}
for i in range(N):
    comps.setdefault(fnd(i), []).append(i)

INDEP_K = lambda qs: {q for q in qs if q.startswith("K_") and q != "K_model"}
rows_hz = []
for root, ii in comps.items():
    cats = sorted({HZ[i]["cat"] for i in ii})
    if len([c for c in cats if c != "ALMA_arch"]) < 2:
        continue
    qs = set()
    for i in ii:
        qs |= set(HZ[i]["q"].split(","))
    zz = [HZ[i]["z"] for i in ii if np.isfinite(HZ[i]["z"])]
    names = sorted({HZ[i]["name"] for i in ii if HZ[i]["cat"] != "ALMA_arch"})
    ktr = sorted({q[2:] for q in qs if q.startswith("K_")})
    grp = sorted({CATS_HZ[c][2] for c in cats if c != "ALMA_arch"})
    rows_hz.append(dict(names="|".join(names), z=round(float(np.median(zz)), 3) if zz else "", catalogues="|".join(cats),
                        n_cat=len([c for c in cats if c != "ALMA_arch"]), n_indep_data_groups=len([g for g in grp]),
                        kin_tracers="|".join(ktr),
                        has_K=int(any(q.startswith("K_") for q in qs)),
                        has_K_obs=int(bool(INDEP_K(qs))),
                        has_Gmeas=int(any(q in ("G_CO", "G_dust", "G_HI") for q in qs)),
                        has_Gcov=int("G_cov" in qs), has_M=int("M" in qs),
                        has_deep=int(any(q in ("K_Ha-deep", "K_Ha-KMOS-deep") for q in qs)),
                        has_AO_or_JWST=int(any(q in ("K_Ha-SINF-AO", "K_Ha-JWST") for q in qs)),
                        has_KCO_and_KHa=int(any(q in ("K_CO", "K_CII") for q in qs) and any(q.startswith("K_Ha") for q in qs) or
                                            (("K_CO" in qs or "K_CII" in qs) and "K_model" in qs))))
rows_hz.sort(key=lambda r: (-r["n_cat"], str(r["z"])))

P("=" * 110)
P("CFG492 A -- multi-source inventory and cross-match (on-disk only)" + ("   *** MUTATE: +60 arcsec Dec shift ***" if MUTATE else ""))
P("=" * 110)
P("\nHIGH-Z catalogues read (entries):")
for c, (d, q, g) in CATS_HZ.items():
    n = int((CATI == c).sum()); npos = int(((CATI == c) & ok).sum())
    P(f"  {c:12} {n:6d} entries ({npos:6d} with coordinates)  [{q}]  {d}")
P(f"  coordinate edges (<= 1.0 arcsec, |dz| <= 0.01(1+z)): {n_coord_edges}")
cnt = {}
def C(key, cond):
    cnt[key] = int(sum(1 for r in rows_hz if cond(r)))
C("objects in >= 2 catalogues (ALMA archive coverage not counted)", lambda r: True)
C(">= 3 catalogues", lambda r: r["n_cat"] >= 3)
C(">= 4 catalogues", lambda r: r["n_cat"] >= 4)
C("K (any kinematics) + measured gas + M*", lambda r: r["has_K"] and r["has_Gmeas"] and r["has_M"])
C("K observed (not model-only) + measured gas + M*", lambda r: r["has_K_obs"] and r["has_Gmeas"] and r["has_M"])
C("K + ALMA archive coverage only (gas not yet measured)", lambda r: r["has_K"] and r["has_Gcov"] and not r["has_Gmeas"])
C("two independent kinematic tracers (CO/[CII] and Ha)", lambda r: r["has_KCO_and_KHa"])
C("AO/JWST inner + deep outer", lambda r: r["has_AO_or_JWST"] and r["has_deep"])
C("AO/JWST inner + deep outer + measured gas (CFG385 specification)", lambda r: r["has_AO_or_JWST"] and r["has_deep"] and r["has_Gmeas"])
C("deep outer + measured gas + M*", lambda r: r["has_deep"] and r["has_Gmeas"] and r["has_M"])
P("\nHIGH-Z overlap counts:")
for k, v in cnt.items():
    P(f"  {k:70}: {v}")
P("\nHIGH-Z objects in >= 3 catalogues, or with K + measured gas + M*:")
for r in rows_hz:
    if r["n_cat"] >= 3 or (r["has_K"] and r["has_Gmeas"] and r["has_M"]):
        P(f"  z {str(r['z']):6} | {r['names'][:60]:60} | {r['catalogues']} | K:{r['kin_tracers']} G:{'meas' if r['has_Gmeas'] else ('cov' if r['has_Gcov'] else '-')}")

# =====================================================================================================================
# LOCAL GALAXIES (SPARC reference)
# =====================================================================================================================
sp_pos = json.load(open(os.path.join(RD, "sparc_positions_merged.json")))
SP = {}
for r in rcsv(os.path.join(RD, "sparc_master_clean.csv")):
    p = sp_pos.get(r["name"], {})
    SP[r["name"]] = dict(ra=fnum(p.get("ra")), dec=fnum(p.get("dec")), cz=fnum(p.get("cz")) if p.get("cz") is not None else float("nan"), Q=r["Q"])
LOC = {}   # cat -> list of (alias, ra, dec, cz)
DESC_L = {}
def lcat(c, d, q, ents):
    LOC[c] = ents; DESC_L[c] = (d, q)

ents = []
for r in vizier(os.path.join(RD, "diskmass_bershady2010_sample.tsv")):
    ents.append(("UGC" + r["UGC"].lstrip("0"), hms(r["RAJ2000"]), dms(r["DEJ2000"]), fnum(r["HRV"])))
lcat("DiskMass_sample", "DiskMass parent sample (Bershady+10): sample/photometry; NO dynamical disc mass on disk", "M_phot", ents)
ents = []
for r in vizier(os.path.join(RD, "diskmass_swaters2025_dmsXI.tsv")):
    ents.append(("UGC" + r["UGC"].lstrip("0"), fnum(r["_RA"]), fnum(r["_DE"]), fnum(r["Vsys"])))
lcat("DMS_XI", "DiskMass XI (Swaters+25) Ha velocity fields: V_rot, inclination, iiTF", "K_Ha", ents)
ents = []
for l in open(os.path.join(EXT, "little_things_oh2015", "table1.dat")):
    p = l.split("|")
    if len(p) > 2:
        c = p[1].split()
        ents.append((loc_alias(p[0].strip()), hms(" ".join(c[0:3])), dms(" ".join(c[3:6])), float("nan")))
lcat("LITTLE_THINGS", "LITTLE THINGS (Oh+15) HI rotation curves + mass models", "K_HI,G_HI,M", ents)
ents = []
for l in open(os.path.join(RD, "diteodoro2023_massive_spirals.tsv")):
    if l.startswith("#") or l.startswith("name"):
        continue
    ents.append((loc_alias(l.split("\t")[0]), float("nan"), float("nan"), float("nan")))
lcat("DiTeodoro23", "Di Teodoro+23 massive spirals HI curves", "K_HI,G_HI,M", ents)
ents = []
for l in open(os.path.join(RD, "xgass", "xGASS_representative_sample.ascii")):
    if l.startswith("#") or not l.strip():
        continue
    p = l.split()
    ents.append(("AGC" + p[1], fnum(p[6]), fnum(p[7]), fnum(p[8]) * 299792.458))
lcat("xGASS", "xGASS (Catinella+18) HI masses, M*", "G_HI,M", ents)
ents = []
for r in rcsv(os.path.join(DA, "alfalfa_sdss_local_control", "alfalfa_sdss.csv")):
    ents.append(("AGC" + r["agc"], fnum(r["ra_oc_deg"]) if fnum(r["ra_oc_deg"]) == fnum(r["ra_oc_deg"]) else fnum(r["ra_hi_deg"]),
                 fnum(r["dec_oc_deg"]) if fnum(r["dec_oc_deg"]) == fnum(r["dec_oc_deg"]) else fnum(r["dec_hi_deg"]), fnum(r["vhel_kms"])))
lcat("ALFALFA_SDSS", "ALFALFA a100 x SDSS (Haynes+18, Durbala+20): HI mass, W50, M*", "G_HI,K_HI-width,M", ents)
ents = []
for r in rcsv(os.path.join(EXT, "wallaby_dr2", "wallaby_dr2_kinematic_catalogue.csv")):
    ents.append((r["name"], fnum(r["ra"]), fnum(r["dec"]), fnum(r["Vsys_model"])))
lcat("WALLABY_kin", "WALLABY DR2 kinematic models (HI rotation curves)", "K_HI,G_HI", ents)
ents = []
for r in rcsv(os.path.join(DA, "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")):
    ents.append(("MIG" + r["ID_catalogue"], fnum(r["RA_deg"]), fnum(r["Dec_deg"]), float("nan")))
lcat("MIGHTEE_DR1", "MIGHTEE-HI DR1 COSMOS catalogue (widths, M_HI, M*)", "G_HI,K_HI-width,M", ents)
ents = []
for r in rcsv(os.path.join(EXT, "cosmicflows4", "sesame_sparc.csv")):
    ents.append((loc_alias(r["sparc_name"]), fnum(r["ra_deg"]), fnum(r["dec_deg"]), float("nan")))
lcat("CF4_sesame", "Cosmicflows-4 resolver positions for SPARC names (distance table in table2.dat)", "Dist", ents)
ents = []
for r in vizier(os.path.join(RD, "ungc_karachentsev2013.tsv")):
    ents.append((loc_alias(r["Name"]), fnum(r["_RAJ2000"]), fnum(r["_DEJ2000"]), fnum(r["HRV"])))
lcat("UNGC", "Updated Nearby Galaxy Catalog (D <= 11 Mpc): TRGB/Cepheid distances, L_K, M_HI", "Dist,M,G_HI", ents)
ents = []
for r in vizier(os.path.join(RD, "s4g_morph_buta2015_cvrhs.tsv")):
    ents.append((loc_alias(r["Name"]), fnum(r["_RA"]), fnum(r["_DE"]), float("nan")))
lcat("S4G", "S4G 3.6um morphology (Buta+15)", "M_phot", ents)
ents = []
for l in open(os.path.join(RD, "atlas3d_fj_table.tsv")):
    if l.startswith("#") or l.startswith("name") or not l.strip():
        continue
    ents.append((loc_alias(l.split("\t")[0]), float("nan"), float("nan"), float("nan")))
lcat("ATLAS3D", "ATLAS3D JAM M/L, SPS M/L (early types)", "K_STAR,M", ents)
kids = None
try:
    from astropy.io import fits
    with fits.open(os.path.join(RD, "lensing_rar", "KiDS_DR4_brightsample.fits"), memmap=True) as h:
        cols = h[1].columns.names
        rc = [c for c in cols if c.upper() in ("RAJ2000", "RA", "ALPHA_J2000")][0]
        dc = [c for c in cols if c.upper() in ("DECJ2000", "DEC", "DELTA_J2000")][0]
        kids = (np.asarray(h[1].data[rc], float), np.asarray(h[1].data[dc], float))
except Exception as ex:
    P(f"  KiDS bright sample not read: {ex}")
if kids is not None:
    lcat("KiDS_bright", "KiDS-1000 bright galaxy sample (lens positions; per-object lensing S/N << 1)", "L_stack", [("KIDS", a, b, float("nan")) for a, b in zip(*kids)])

LM = {}
for c, ents in LOC.items():
    al = {}
    for e in ents:
        al.setdefault(e[0], []).append(e)
    ra = np.array([e[1] for e in ents]); de = np.array([e[2] for e in ents]); cz = np.array([e[3] for e in ents])
    m = np.isfinite(ra) & np.isfinite(de)
    LM[c] = (al, ra[m], de[m] + SHIFT, cz[m])
TOL_L = 30.0
match_L = {s: {} for s in SP}
for s, p in SP.items():
    for c, (al, ra, de, cz) in LM.items():
        how = None
        if loc_alias(s) in al:
            how = "name"
        elif np.isfinite(p["ra"]) and len(ra):
            near = np.abs(de - p["dec"]) < TOL_L / 3600 * 1.5
            if near.any():
                ss = sep_arcsec(p["ra"], p["dec"], ra[near], de[near])
                czn = cz[near]
                okk = ss <= TOL_L
                if np.isfinite(p["cz"]):
                    okk &= ~(np.isfinite(czn) & (np.abs(czn - p["cz"]) > 300))
                if okk.any():
                    how = f"pos {ss[okk].min():.1f}\""
        if how:
            match_L[s][c] = how
P("\nLOCAL (SPARC reference, 175 galaxies): matches per catalogue (name, or <= 30 arcsec with |dcz| <= 300 km/s)")
cntL = {}
for c in LOC:
    nn = sum(1 for s in SP if c in match_L[s])
    cntL[c] = nn
    P(f"  SPARC x {c:16}: {nn:4d}   [{DESC_L[c][1]}]  {DESC_L[c][0]}")
multi = {s: v for s, v in match_L.items() if len([c for c in v if c not in ("CF4_sesame", "S4G", "KiDS_bright")]) >= 1}
P(f"  SPARC galaxies with >= 1 independent-kinematics/gas/mass source beyond SPARC (CF4/S4G/KiDS not counted): {len(multi)}")
indepK = {s for s, v in match_L.items() if any(c in v for c in ("DMS_XI", "LITTLE_THINGS", "DiTeodoro23", "WALLABY_kin"))}
P(f"  SPARC galaxies with an INDEPENDENT rotation curve (DMS XI / LITTLE THINGS / Di Teodoro / WALLABY): {len(indepK)} -> {sorted(indepK)}")
P(f"  SPARC galaxies with KiDS lens positions: {cntL.get('KiDS_bright', 0)} (per-object weak lensing is not measurable; FP21: 2,036 stacked z~0.026 lenses gave S/N 0.1)")
dyn = {s for s, v in match_L.items() if "DiskMass_sample" in v}
P(f"  SPARC x DiskMass parent sample: {len(dyn)} -> {sorted(dyn)} (the stellar-dispersion disc masses, Martinsson+13, are NOT on disk)")

# =====================================================================================================================
# EARLY TYPES (SLUGGS GC + PN + X-ray + ATLAS3D JAM)
# =====================================================================================================================
def ngc_set_from_tsv(path, col, pat=r"NGC\s*0*(\d+)"):
    s = set()
    for r in vizier(path):
        m = re.search(pat, r.get(col, ""))
        if m:
            s.add(int(m.group(1)))
    return s
ETG = {}
ETG["SLUGGS_GC"] = {int(r["NGC"]) for r in vizier(os.path.join(RD, "sluggs_forbes2017_galaxies.tsv")) if r["NGC"].isdigit()}
ETG["PN_Coccato09"] = ngc_set_from_tsv(os.path.join(RD, "pn_coccato2009_sampleA.tsv"), "PNS-EPN")
ETG["PN_N1023_N08"] = {1023}
ETG["PN_N3379_S06"] = ngc_set_from_tsv(os.path.join(RD, "pn_ngc3379_3384_sluis2006.tsv"), "Galaxy")
ETG["PN_N4494_N09"] = {4494}
ETG["Xray_Humphrey06"] = {int(re.sub(r"\D", "", l.split("\t")[0])) for l in open(os.path.join(RD, "humphrey2006_ellipticals.tsv"))
                          if l.startswith("NGC")}
ETG["ATLAS3D_JAM"] = {int(re.sub(r"\D", "", l.split("\t")[0])) for l in open(os.path.join(RD, "atlas3d_fj_table.tsv"))
                      if l.startswith("NGC")}
try:
    ETG["Lx_OSullivan01"] = ngc_set_from_tsv(os.path.join(EXT, "osullivan2001_lx", "osullivan2001_table3.tsv"), "Name")
except Exception:
    ETG["Lx_OSullivan01"] = set()
ETG["HI_denHeijer15"] = {int(re.sub(r"\D", "", l.split("\t")[0])) for l in open(os.path.join(RD, "denheijer2015_etg_hi_tfr.tsv"))
                         if l.startswith("NGC")}
allE = sorted(set().union(*ETG.values()))
rows_etg = []
for n in allE:
    have = [c for c in ETG if n in ETG[c]]
    pn = any(c.startswith("PN_") for c in have)
    rows_etg.append(dict(ngc=n, sources="|".join(have), GC="SLUGGS_GC" in have, PN=pn, X="Xray_Humphrey06" in have,
                         JAM="ATLAS3D_JAM" in have, HI="HI_denHeijer15" in have))
P("\nEARLY TYPES (by NGC number): catalogue sizes " + ", ".join(f"{c} {len(v)}" for c, v in ETG.items()))
cE = {
    "GC + PN (two independent outer tracers)": [r["ngc"] for r in rows_etg if r["GC"] and r["PN"]],
    "GC + PN + ATLAS3D JAM (inner anchor)": [r["ngc"] for r in rows_etg if r["GC"] and r["PN"] and r["JAM"]],
    "GC + X-ray (Humphrey)": [r["ngc"] for r in rows_etg if r["GC"] and r["X"]],
    "GC + X-ray + JAM": [r["ngc"] for r in rows_etg if r["GC"] and r["X"] and r["JAM"]],
    "PN + X-ray": [r["ngc"] for r in rows_etg if r["PN"] and r["X"]],
    "GC + PN + X-ray": [r["ngc"] for r in rows_etg if r["GC"] and r["PN"] and r["X"]],
    "PN + JAM (PN-only law test)": [r["ngc"] for r in rows_etg if r["PN"] and r["JAM"]],
    "HI ring + JAM (+GC)": [r["ngc"] for r in rows_etg if r["HI"] and r["JAM"]],
}
for k, v in cE.items():
    P(f"  {k:42}: {len(v):3d} -> {['NGC%d' % x for x in v]}")

# =====================================================================================================================
# CLUSTERS (X-COP reference)
# =====================================================================================================================
xc = json.load(open(os.path.join(RD, "xcop", "xcop_r500_ettori2019.json")))
GRO = vizier(os.path.join(RD, "groener2016_cluster_concentrations.tsv"))
def cl_alias(n):
    n = n.upper().replace(" ", "").replace("ABELL", "A").replace("ZWCL", "ZW").replace('"', "")
    n = re.sub(r"^A0*(\d)", r"A\1", n)
    return n
XC = {}
for k, v in xc.items():
    a = cl_alias(k)
    if a.startswith("ZW1215"):
        a = "ZW1215"
    XC[k] = dict(alias=a, z=v["z"], ra=float("nan"), dec=float("nan"))
for r in GRO:
    a = cl_alias(r["Cluster"])
    a = "ZW1215" if a.startswith("ZW1215") else a
    for k, v in XC.items():
        if v["alias"] == a and not np.isfinite(v["ra"]):
            v["ra"], v["dec"] = hms(r["RAJ2000"]), dms(r["DEJ2000"])
if "RXC1825" in XC and not np.isfinite(XC["RXC1825"]["ra"]):
    XC["RXC1825"]["ra"], XC["RXC1825"]["dec"] = hms("18 25 18"), dms("+30 26 00")   # from the RXC J1825.3+3026 designation
CL = {k: {} for k in XC}
for r in GRO:
    a = cl_alias(r["Cluster"]); a = "ZW1215" if a.startswith("ZW1215") else a
    for k, v in XC.items():
        if v["alias"] == a:
            CL[k].setdefault("groener_" + r["Method"], []).append(r["Ref"])
wings = {}
for r in rcsv(os.path.join(RD, "wings_spe_cava2009.csv")):
    wings.setdefault(cl_alias(r["Cluster"]), 0)
    wings[cl_alias(r["Cluster"])] += 1
for k, v in XC.items():
    if v["alias"] in wings:
        CL[k]["WINGS_members"] = [wings[v["alias"]]]
def coord_cat(name, ra, de, z, tol_am=3.0):
    ra = np.asarray(ra, float); de = np.asarray(de, float) + SHIFT; z = np.asarray(z, float)
    for k, v in XC.items():
        if not np.isfinite(v["ra"]):
            continue
        s = sep_arcsec(v["ra"], v["dec"], ra, de) / 60
        m = (s <= tol_am) & ~(np.isfinite(z) & (np.abs(z - v["z"]) > 0.01))
        if m.any():
            CL[k][name] = [round(float(s[m].min()), 2)]
psz = vizier(os.path.join(RD, "psz2_union.tsv"))
coord_cat("PSZ2_SZ", [fnum(r["RAJ2000"]) for r in psz], [fnum(r["DEJ2000"]) for r in psz], [fnum(r["z"]) if fnum(r["z"]) > 0 else float("nan") for r in psz])
try:
    from astropy.io import fits
    with fits.open(os.path.join(RD, "erass1cl_primary_v3.2.fits"), memmap=True) as h:
        d = h[1].data
        coord_cat("eRASS1_X", d["RA"], d["DEC"], d["BEST_Z"])
except Exception as ex:
    P(f"  eRASS1 not read: {ex}")
P(f"\nCLUSTERS (X-COP reference: {len(XC)} entries in xcop_r500_ettori2019.json = the 12 X-COP clusters + Hydra A): which other sources supply the same cluster")
P("  (groener_<Method>: literature compilation (Groener+16) entry by method; WINGS: spectroscopic member count (Cava+09);")
P("   PSZ2/eRASS1: coordinate match <= 3 arcmin, |dz| <= 0.01; X-COP itself supplies the hydrostatic X-ray + SZ-pressure mass profile)")
rows_cl = []
for k, v in XC.items():
    s = CL[k]
    rows_cl.append(dict(cluster=k, z=v["z"], sources="|".join(sorted(s)), WL=int(any(m in s for m in ("groener_WL", "groener_WL+SL", "groener_SL"))),
                        DYN=int(any(m in s for m in ("groener_LOSVD", "groener_CM")) or "WINGS_members" in s),
                        XLIT=int("groener_X-ray" in s)))
    P(f"  {k:8} z {v['z']:.4f} | " + "; ".join(f"{m}({len(x) if m.startswith('groener') else x[0]})" for m, x in sorted(s.items())))
cC = {"X-COP x lensing (WL/SL)": sum(r["WL"] for r in rows_cl),
      "X-COP x galaxy dynamics (LOSVD/caustic/WINGS members)": sum(r["DYN"] for r in rows_cl),
      "X-COP x lensing x dynamics": sum(1 for r in rows_cl if r["WL"] and r["DYN"])}
for k, v in cC.items():
    P(f"  {k:55}: {v}")

# =====================================================================================================================
P("\nSUMMARY JSON written.")
json.dump(dict(mutate=MUTATE, highz_counts=cnt, highz_catalogues={c: dict(desc=d, q=q, group=g, n=int((CATI == c).sum())) for c, (d, q, g) in CATS_HZ.items()},
               local_counts=cntL, local_indepK=sorted(indepK), local_diskmass=sorted(dyn),
               etg_counts={k: v for k, v in cE.items()}, cluster_counts=cC),
          open(os.path.join(HERE, f"cfg492_inventory{TAG}_results.json"), "w"), indent=1, default=str)
def wcsv(fn, rows):
    if not rows:
        return
    with open(os.path.join(HERE, fn), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
if not MUTATE:
    wcsv("cfg492_overlap_highz.csv", rows_hz)
    wcsv("cfg492_overlap_etg.csv", rows_etg)
    wcsv("cfg492_overlap_clusters.csv", rows_cl)
    wcsv("cfg492_overlap_sparc.csv", [dict(sparc=s, **{c: match_L[s].get(c, "") for c in LOC}) for s in SP if match_L[s]])
open(os.path.join(HERE, f"cfg492_inventory{TAG}.out"), "w").write("\n".join(OUT) + "\n")
