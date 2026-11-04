#!/usr/bin/env python3
"""NV1 environment leaves E1-E4 per system, from files on disk only (FROZEN_CRITERIA). Missing = NaN = NOT COMPUTABLE, never imputed.
E2 copies CX1's E-leaf formula (CX1_leaf_collision/cx1_rows.py, lines 16-31, 62, 76-78, 139-141, 117, 128) with attribution; values from BS1.
Read-only on every other lane. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, re, sys
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
CRGI = os.path.join(RB, "CRG1_clean_room_regrade", "inputs")
CANDS = ("E1", "E2", "E3", "E4")
SIG = dict(E2=0.15, E3=0.10, E4=0.30)          # E1's sigma is per system (half the noclu-maxclu bracket)
NAN = float("nan")

# ---------- CX1's E-leaf constants and helpers (copied from cx1_rows.py, read-only source)
BS1 = json.load(open(os.path.join(RB, "BS1_basin_switch", "bs1_basin_switch_results.json")))
LG_LGM = BS1["LG"]["basin"]["lgM"]; R0D = BS1["LG"]["R0_data_kpc"]; FIELD_R = BS1["LG"]["field_R_kpc"]
BASIN_SP = BS1["primary_basins"]["lgM_basin_sparc"]["A_c2b_refit"]; NODIST = set(BS1["primary_basins"]["no_dist"])
EM1 = (11.18, 0.90)
def lgM200(lMb): return EM1[0] + EM1[1] * (lMb - 10.0)
def mb_of_mstar(Ms):
    l = math.log10(Ms); return Ms * (1.0 + 10 ** (-0.69 * l + 6.63)) if 8.5 <= l <= 11.0 else 1.2 * Ms      # BS1's A1
def norm(n): n = n.upper().replace(" ", ""); return re.sub(r"(?<=[A-Z])0+(?=\d)", "", n)
ALIAS = {norm(a): norm(b) for a, b in [("DDO 50", "UGC04305"), ("DDO 87", "UGC05918"), ("DDO 126", "UGC07559"), ("Haro 29", "UGCA281"),
                                        ("WLM", "UGCA444"), ("DDO 210", "Aquarius"), ("DDO 216", "Pegasus dIrr")]}
def sysid(n): k = norm(n); return ALIAS.get(k, k)
LG_IDENT = {sysid(x) for x in ("IC 1613", "Aquarius", "Pegasus dIrr", "UGCA444")}

# ---------- SPARC table (CX1's mrt(), CRG1 inputs)
def _mrt():
    T = {}
    for l in open(os.path.join(CRGI, "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) != 19: continue
        try: T[t[0]] = dict(D=float(t[2]), L36=float(t[7]), MHI=float(t[13]))
        except ValueError: continue
    return T
MRT = _mrt()
SPARC_NAMES = sorted(os.path.basename(f).replace("_rotmod.dat", "") for f in os.listdir(os.path.join(CRGI, "sparc", "rotmod")) if f.endswith("_rotmod.dat"))
def sparc_alias(name):
    sid = sysid(name); sp = [n for n in SPARC_NAMES if sysid(n) == sid]; return sp[0] if sp else None

# ---------- E1: record's 2M++ + MCXC external field (gext_vectors_2026), mean of the two logs, sigma half the bracket
GEXT = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "gext_vectors_2026", "data", "gext_vectors.csv")))}
def _e1(n):
    r = GEXT.get(n)
    if r is None: return NAN, NAN
    a, b = float(r["log_eN_noclu"]), float(r["log_eN_maxclu"]); return 0.5 * (a + b), 0.5 * abs(b - a)

# ---------- E3: host potential depth, RQ3's host masses, X1's d_host
GZ, MSZ, KPCZ, CL = 6.67430e-11, 1.989e30, 3.0856775814913673e19, 299792458.0; MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}; A_H = 3.0
X1 = {}
for _r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))):
    if _r["footing"] == "canonical": X1[_r["name"]] = _r
def _e3_dwarf(name, host=None):
    r = X1.get(name)
    if r is None or r["d_host_kpc"] in ("", None): return NAN
    h = host if host is not None else r["host"]; M = MHOST[h if h in MHOST else "field"]; d = float(r["d_host_kpc"])
    return math.log10(GZ * M * MSZ / ((d + A_H) * KPCZ) / CL ** 2)

# ---------- E4: UNGC tidal index Theta1 (Ti1); Theta5 reported only
E4_ALIAS = {"ANDROMEDA": "AND", "URSAMAJORI": "UMAI", "URSAMAJORII": "UMAII", "URSAMINOR": "UMIN", "CANESVENATICII": "CVNI", "CANESVENATICIII": "CVNII", "COMABERENICES": "COMAI",
            "SEXTANS": "SEXDSPH", "SAGITTARIUS": "SAGDSPH", "SAGITTARIUSDIRR": "SAGDIR", "PEGASUSDIRR": "PEGASUS", "DDO216": "PEGASUS", "AQUARIUS": "DDO210", "DDO210": "DDO210"}
def e4key(n):
    k = norm(n)
    if k.startswith("ANDROMEDA"): k = "AND" + k[len("ANDROMEDA"):]
    return E4_ALIAS.get(k, k)
UNGC = {}
for _l in open(os.path.join(REPO, "real_research", "data", "ungc_karachentsev2013.tsv")):
    if _l.startswith("#") or not _l.strip(): continue
    _p = _l.rstrip("\n").split("\t")
    if len(_p) < 17 or _p[0].strip() in ("Name", "") or _p[0].startswith("-"): continue
    try: ra, de = float(_p[1]), float(_p[2])
    except ValueError: continue
    def _f(x):
        try: return float(x)
        except ValueError: return NAN
    UNGC[norm(_p[0].strip())] = dict(name=_p[0].strip(), ra=ra, dec=de, D=_f(_p[7]), Ti1=_f(_p[14]), MD=_p[15].strip(), Ti5=_f(_p[16]))
_UK = list(UNGC); _UXYZ = None
def _xyz(ra, de): ra, de = np.radians(ra), np.radians(de); return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], -1)
def ungc_by_pos(ra, de, tol=0.1):
    global _UXYZ
    if _UXYZ is None: _UXYZ = _xyz(np.array([UNGC[k]["ra"] for k in _UK]), np.array([UNGC[k]["dec"] for k in _UK]))
    c = _UXYZ @ _xyz(ra, de); i = int(np.argmax(c)); ang = math.degrees(math.acos(min(1.0, float(c[i])))); return (UNGC[_UK[i]], ang) if ang <= tol else (None, ang)
def _e4_sparc(n):
    r = GEXT.get(n)
    if r is None: return None
    u, _ = ungc_by_pos(float(r["ra"]), float(r["dec"])); return u
def _e4_name(n): return UNGC.get(e4key(n))

# ---------- per system kind
def sparc_E(n, c):
    if c == "E1": return _e1(n)[0]
    if c == "E2":
        if n in BASIN_SP: return float(BASIN_SP[n])
        if n in NODIST or n not in MRT: return NAN
        t = MRT[n]; return lgM200(math.log10((0.5 * t["L36"] + 1.33 * t["MHI"]) * 1e9))
    if c == "E3": return NAN
    if c == "E4": u = _e4_sparc(n); return u["Ti1"] if u else NAN
def lt_E(n, c):
    sid = sysid(n); sp = sparc_alias(n)
    if c == "E1": return _e1(sp)[0] if sp else NAN
    if c == "E2":
        if sid in LG_IDENT: return LG_LGM
        return sparc_E(sp, "E2") if sp else NAN
    if c == "E3":
        for k in X1:
            if sysid(k) == sid: return _e3_dwarf(k)
        return NAN
    if c == "E4":
        u = _e4_name(n)
        if u is None and sp: u = _e4_sparc(sp)
        return u["Ti1"] if u else NAN
def dwarf_E(name, host, lgMs, c):
    if c == "E1": return NAN
    if c == "E2":
        if host in ("MW", "M31"): return LG_LGM
        Rk = FIELD_R.get(name); return LG_LGM if (Rk is not None and Rk < R0D) else lgM200(math.log10(mb_of_mstar(10 ** lgMs)))
    if c == "E3": return _e3_dwarf(name, host)
    if c == "E4": u = _e4_name(name); return u["Ti1"] if u else NAN
def xcop_E(name, c):
    if c != "E2": return NAN
    return CX1_E()[("X", name)]
def group_E(lgMb, c): return lgM200(lgMb) if c == "E2" else NAN
def lens_E_from_mass(lgMb, c): return lgM200(lgMb) if c == "E2" else NAN
def lgsys_E(c): return LG_LGM if c == "E2" else NAN      # Milky Way and the planets: inside the LG basin (E2 only)
def sigma_E(c, system_E1_sigma=None): return system_E1_sigma if c == "E1" else SIG[c]

_CX = {}
def CX1_E():
    """CX1's own lE per (line, name), canonical footing (E is footing-free). Imported read-only."""
    if _CX: return _CX
    sys.path.insert(0, os.path.join(RB, "CX1_leaf_collision")); import cx1_rows as CR
    for s in CR.systems("canonical"): _CX[(s.line, s.name)] = float(s.lE)
    return _CX

# ---------- BF1 row indices -> names
def xcop_names():
    D = os.path.join(REPO, "real_research", "data", "xcop"); return sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits")))
def sl1_lt_names():
    import pickle
    return [g["name"] for g in pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["lt"]]
def sl1_sparc_names():
    import pickle
    return sorted(g["name"] for g in pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"])
def bf1_E(A, kind, c):
    """E per BF1 row: kind 'S' (SPARC, col 4 = index into sorted SL1 names), 'X' (X-COP, col 4 = index into sorted X-COP dirs), 'LT' (col 4 = SL1 lt index)."""
    idx = A[:, 4].astype(int)
    if kind == "S": N = sl1_sparc_names(); f = lambda i: sparc_E(N[i], c)
    elif kind == "X": N = xcop_names(); f = lambda i: xcop_E(N[i], c)
    else: N = sl1_lt_names(); f = lambda i: lt_E(N[i], c)
    m = {i: f(i) for i in np.unique(idx)}; return np.array([m[i] for i in idx], float), np.array([N[i] for i in idx])

# ---------- RQ3 lookup table for the candidate loader
def xcop_r500_map():
    """RQ3 rows_xcop's r5 per cluster (FITS hydro-mass header R500 x 1e3 x pc in m), same expression as RQ3."""
    from astropy.io import fits
    D = os.path.join(REPO, "real_research", "data", "xcop"); PCm = 3.0857e16; o = {}
    for n in xcop_names():
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: o[n] = float(h[1].header["R500"]) * 1e3 * PCm
    return o
def rq3_table_build(c):
    T = dict(cand=c, disc={n: sparc_E(n, c) for n in SPARC_NAMES}, cluster_r500=[[r5, xcop_E(n, c), n] for n, r5 in xcop_r500_map().items()], MW=lgsys_E(c), planet=lgsys_E(c), group="EM1" if c == "E2" else None, lens="EM1" if c == "E2" else None)
    lt = [r["name"] for r in csv.DictReader(open(os.path.join(CRGI, "little_things", "oh2015_table2.csv")))]; T["dwarf disc"] = {n: lt_E(n, c) for n in lt}
    T["dwarf"] = {}
    for r in X1.values(): T["dwarf"][r["name"]] = dwarf_E(r["name"], r["host"], float(r["logMstar"]), c)   # RQ3 rows_dwarfs reads X1_hosted_recount/x1_per_system.csv
    return T

if __name__ == "__main__":
    for c in CANDS:
        T = rq3_table_build(c); print(c, {k: (sum(np.isfinite(v) for v in T[k].values()), len(T[k])) for k in ("disc", "dwarf disc", "dwarf")}, "X-COP", sum(np.isfinite(x[1]) for x in T["cluster_r500"]))
