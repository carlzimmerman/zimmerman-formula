#!/usr/bin/env python3
"""DSB1 (criteria 2c7beb7b92): the hosted dwarf classes regraded against form B with a full systematics budget, frozen blind.

    nice -n 19 python3 dsb1.py            -> dsb1.json / dsb1.out             (known answers, grading, variants, width table)
    nice -n 19 python3 dsb1.py --mutate   -> dsb1_MUTATE.json / dsb1_MUTATE.out (M1 T1 removed, M2 a0 doubled, M3 planted +0.60)

Form B (RB2's definition, copied, not imported): isolated law nu(y) = 1/2 + sqrt(1/4 + 1/y) inside the Jacobi radius r_J,
g_iso(r_J)/r_J = k G M_host(<d)/d^3; outside, baryons plus the phantom kept inside r_J.  Loaders, X1's Monte Carlo build,
classes, edges and Coma constants are copied from rb2.py (which copied X1 / S1 / SE2 / XF1).  Data files are read as data.
kappa = 1/2 FITTED; not theory closed; footings never pooled; no particle.  Relabels nothing.  Adopts nothing."""
import os, sys, json, math, csv, time, re
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.dirname(HERE); REPO = os.path.dirname(CL)
MUT = "--mutate" in sys.argv
TAG = "dsb1_MUTATE" if MUT else "dsb1"
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"{name} {'PASS' if ok else 'FAIL'}  {msg}")
trapz = getattr(np, "trapezoid", None) or np.trapz

# ============================================================== constants and loaders (copied from rb2.py / X1)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
NMC = 2000
FW_N = 2.0 * (4 / 3) ** 3 / (1 + (4 / 3) ** 2) ** 1.5
R12 = 4.0 / 3.0
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
X1D = os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount")
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
def _row(r, host, s, sem, sep, ul):
    rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
    ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
    if not rh or rh <= 0: return None
    if ms is None and mv is not None: ms = 0.4 * (4.83 - mv) + 0.301
    if ms is None: return None
    rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
    rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
    return dict(name=r["name"], host=host, sigma=s, sem=sem, sep=sep, ul=ul,
                rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")), mv=mv, dm31=fl(r.get("distance_m31")),
                mvem=fl(r.get("M_V_em")) or 0.1, mvep=fl(r.get("M_V_ep")) or 0.1,
                hi=fl(r.get("mass_HI")), hiul=fl(r.get("mass_HI_ul")), _raw=r)
def load_lvd():
    rows, cens = [], []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma")); u = fl(r.get("vlos_sigma_ul"))
            if s and s > 0:
                x = _row(r, host, s, fl(r.get("vlos_sigma_em")) or 0.1 * s, fl(r.get("vlos_sigma_ep")) or 0.1 * s, bool(r.get("vlos_sigma_ul")))
                if x: x["cens"] = None; rows.append(x)
            elif u and u > 0:
                x = _row(r, host, u, 0.0, 0.0, True)
                if x: x["cens"] = u; cens.append(x)
    return rows, cens
ALL, CENS_ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, mvrule=False):
    """X1's build, copied verbatim (via rb2.py)."""
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC)); Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl_, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl_, gu
        b = 1.0
        ufd = (r["mv"] is not None and r["mv"] > -7.7)
        if binmode == "free": b = arr_free.get(r["name"], med_free if (ufd or not mvrule) else 1.0)
        elif binmode == "f07": b = arr_f07.get(r["name"], med_f07 if (ufd or not mvrule) else 1.0)
        fD = 10 ** (split_normal(rng, 0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(rng, s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(rng, r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar); Md[i] = gobs * r12 ** 2 / G / MSUN; Ms_[i] = ms
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, Md=Md, Ms=Ms_, rows=keep)
def Rh_X1(r):
    if r["host"] == "field": return r["dist"] * KPC
    if r["dhost"]: return r["dhost"] * KPC
    if r["host"] == "M31" and r["dm31"]: return r["dm31"] * KPC
    return r["dist"] * KPC
CLASSICAL = {"Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"}
INDIV = ["Crater II", "Antlia II", "Canes Venatici I", "Sagittarius"]
EXCL = {"LMC", "SMC", "M 32"}
DES = {"NGC 147", "NGC 185", "NGC 205"}
def klass(r):
    n = r["name"]
    if n in EXCL: return None
    if r["host"] == "MW":
        if n in CLASSICAL: return "MW classical"
        if n in INDIV: return "indiv:" + n
        if r["mv"] is not None and r["mv"] > -7.7: return "MW ultra-faint"
        return "MW other"
    if r["host"] == "M31":
        if n in DES: return "M31 dE"
        return "bright M31" if r["logms"] >= 5.0 else "M31 others"
    return "LG field"
SMP = [r for r in ALL if klass(r) is not None]
CENS = [r for r in CENS_ALL if klass(r) is not None]
X1CSV = list(csv.DictReader(open(os.path.join(X1D, "x1_per_system.csv"))))
def boot_median(vals, sds, nb=4000, seed=11):
    """XF1's boot_median (copied via rb2.py)."""
    rng = np.random.default_rng(seed); vals = np.asarray(vals); sds = np.asarray(sds); n = len(vals); meds = np.empty(nb)
    for b in range(nb):
        ix = rng.integers(0, n, n); meds[b] = np.median(vals[ix] + rng.normal(0, 1, n) * sds[ix])
    q = np.percentile(meds, [2.5, 50, 97.5])
    return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], contains0=bool(q[0] <= 0 <= q[2]), n=int(n))

# ============================================================== form B (copied from rb2.py)
def gl(gN):
    gN = np.asarray(gN, float); return 0.5 * gN + np.sqrt(0.25 * gN * gN + gN)
def gNp(r, y):
    return y * r / (1.0 + r * r) ** 1.5
def solve_rJ(hfun, K, lo=-12.0, hi=12.0, it=90):
    K = np.asarray(K, float); lo = np.full(K.shape, lo); hi = np.full(K.shape, hi)
    for _ in range(it):
        mid = 0.5 * (lo + hi); above = hfun(10 ** mid) > K
        lo = np.where(above, mid, lo); hi = np.where(above, hi, mid)
    return np.where(K > 0, 10 ** (0.5 * (lo + hi)), np.inf)
def rJ_iso(y, K):
    y = np.asarray(y, float); K = np.broadcast_to(np.asarray(K, float), y.shape)
    return solve_rJ(lambda r: gl(gNp(r, y)) / r, K)
def gB(r, y, rJ):
    y = np.asarray(y, float); rJ = np.broadcast_to(np.asarray(rJ, float), y.shape)
    gi = gl(gNp(r, y))
    fin = np.isfinite(rJ); rJs = np.where(fin, rJ, 1.0)
    gt = gNp(r, y) + (gl(gNp(rJs, y)) - gNp(rJs, y)) * rJs ** 2 / r ** 2
    return np.where(fin & (rJs < r), gt, gi)
RV = np.geomspace(1e-5, 1e5, 24000); RHO = (3 / (4 * np.pi)) * (1 + RV * RV) ** -2.5
def vir_B(y, rJ):
    g = gB(RV, np.full(RV.shape, float(y)), np.full(RV.shape, float(rJ)))
    return float(trapz(RHO * RV * g * 4 * np.pi * RV * RV, RV) / 3.0)

# ============================================================== edges (copied from rb2.py)
VC = {"MW": 200.0, "M31": 230.0}
M31_RADEC = (10.6847, 41.2690)
def sky_angle(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(math.radians, (ra1, de1, ra2, de2))
    c = math.sin(de1) * math.sin(de2) + math.cos(de1) * math.cos(de2) * math.cos(ra1 - ra2)
    return math.acos(max(-1.0, min(1.0, c)))
def m31_distance():
    cands = []
    for r in SMP:
        if r["host"] != "M31" or not r["dm31"] or not r["dist"]: continue
        R = r["_raw"]; th = sky_angle(float(R["ra"]), float(R["dec"]), *M31_RADEC)
        D, dm = r["dist"], r["dm31"]; disc = dm * dm - (D * math.sin(th)) ** 2
        if disc < 0: continue
        cands.append((D * math.cos(th) - math.sqrt(disc), D * math.cos(th) + math.sqrt(disc)))
    grid = np.arange(600.0, 1000.0, 0.1)
    cost = [sum(min(abs(a - g), abs(b - g)) for a, b in cands) for g in grid]
    return float(grid[int(np.argmin(cost))]), len(cands)
def mw_pericentres(rows, nmc=500, seed=20261109):
    import astropy.units as u
    from astropy.coordinates import SkyCoord, Galactocentric
    rng = np.random.default_rng(seed); out = {}
    Vc = VC["MW"]
    for r in rows:
        if r["host"] != "MW": continue
        R = r["_raw"]; v = {k: fl(R.get(k)) for k in ("ra", "dec", "distance_modulus", "pmra", "pmdec", "vlos_systemic")}
        if any(v[k] is None for k in v):
            out[r["name"]] = None; continue
        e = lambda k: 0.5 * ((fl(R.get(k + "_em")) or 0.0) + (fl(R.get(k + "_ep")) or 0.0))
        dm = split_normal(rng, v["distance_modulus"], fl(R.get("distance_modulus_em")) or 0.0, fl(R.get("distance_modulus_ep")) or 0.0, nmc)
        D = 10 ** ((dm + 5) / 5) / 1e3
        pmra = v["pmra"] + rng.normal(0, 1, nmc) * e("pmra"); pmdec = v["pmdec"] + rng.normal(0, 1, nmc) * e("pmdec")
        vl = v["vlos_systemic"] + rng.normal(0, 1, nmc) * e("vlos_systemic")
        D = np.concatenate([[10 ** ((v["distance_modulus"] + 5) / 5) / 1e3], D]); pmra = np.concatenate([[v["pmra"]], pmra])
        pmdec = np.concatenate([[v["pmdec"]], pmdec]); vl = np.concatenate([[v["vlos_systemic"]], vl])
        c = SkyCoord(ra=np.full(D.shape, v["ra"]) * u.deg, dec=np.full(D.shape, v["dec"]) * u.deg, distance=D * u.kpc,
                     pm_ra_cosdec=pmra * u.mas / u.yr, pm_dec=pmdec * u.mas / u.yr, radial_velocity=vl * u.km / u.s, frame="icrs")
        gc = c.transform_to(Galactocentric())
        x = np.vstack([gc.x.to_value(u.kpc), gc.y.to_value(u.kpc), gc.z.to_value(u.kpc)]).T
        w = np.vstack([gc.v_x.to_value(u.km / u.s), gc.v_y.to_value(u.km / u.s), gc.v_z.to_value(u.km / u.s)]).T
        rn = np.linalg.norm(x, axis=1); L = np.linalg.norm(np.cross(x, w), axis=1); E = 0.5 * np.sum(w * w, axis=1) + Vc ** 2 * np.log(rn)
        f = lambda rr: Vc ** 2 * np.log(rr) + L ** 2 / (2 * rr * rr) - E
        lo = np.full(rn.shape, 1e-3); hi = np.minimum(rn, np.maximum(L / Vc, 1e-3))
        for _ in range(80):
            mid = np.sqrt(lo * hi); pos = f(mid) > 0
            lo = np.where(pos, mid, lo); hi = np.where(pos, hi, mid)
        peri = np.sqrt(lo * hi); peri = np.where(f(np.full(rn.shape, 1e-3)) <= 0, 1e-3, peri)
        out[r["name"]] = dict(p16=float(np.percentile(peri[1:], 16)))
    return out

# ============================================================== Coma (copied from rb2.py / S1)
KPC_C = 3.0857e19; G_, MSUN_, PC_ = 6.674e-11, 1.989e30, 3.0857e16
KEV, MP = 1.602176634e-16, 1.67262e-27
BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6)
CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP)
def g_beta(d_kpc):
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB * r / (r * r + rc * rc)
_rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "freundlich2022_coma_udgs.tsv"), encoding="utf-8")
         if l.strip() and not l.startswith("#")]
_hd = {h: i for i, h in enumerate(_rows[0])}
COMA = []
for r in _rows[1:]:
    g_ = lambda k: float(r[_hd[k]])
    Ms = g_("L_1e8") * 1e8 * g_("ML"); Re = g_("Re_kpc")
    COMA.append(dict(name=r[_hd["name"]], Ms=Ms, Re=Re, sig=g_("sig"), esig=g_("esig"), dproj=g_("d_kpc"), dmean=g_("dmean_kpc"),
                     admit=(Re >= 1.5) and (3e7 <= Ms <= 3e8)))
ADM = [c for c in COMA if c["admit"]]

# ============================================================== DSB1 machinery
GRADED = ("MW ultra-faint", "MW classical", "bright M31", "Coma UDGs")
REPORTED = ("M31 others", "LG field")
READINGS = ("prim", "weak", "strong")
TERMS = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18"]
M31D, nM31 = m31_distance()
PERI = mw_pericentres(SMP + CENS)
def edge_of(r):
    if r["host"] == "MW":
        p = PERI.get(r["name"])
        return ("orbit", p["p16"]) if p else ("SE2", None)
    if r["host"] == "M31":
        R = r["_raw"]; th = sky_angle(float(R["ra"]), float(R["dec"]), *M31_RADEC)
        return ("proj", M31D * math.sin(th))
    return (None, None)
def bnom(r):
    ufd = (r["mv"] is not None and r["mv"] > -7.7)
    return arr_free.get(r["name"], med_free if ufd else 1.0)
def norm_name(s):
    s = s.lower().replace("andromeda", "and")
    return re.sub(r"[\s\(\)\-]", "", s)
def alt_sigma():
    alt = {}
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv"))):
        s = fl(r.get("sigma*"))
        if s and s > 0: alt.setdefault("MW", {})[norm_name(r["Name"])] = s
    for l in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv"), encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) < 20 or not p[0].strip().isdigit(): continue
        s = fl(p[18])
        if s and s > 0: alt.setdefault("M31", {})[norm_name(p[1].strip())] = s
    return alt
ALT = alt_sigma()
def membership_widths():
    out = {}; pool = []
    for cls in ("MW ultra-faint", "MW classical", "bright M31"):
        cat = ALT.get("M31" if cls == "bright M31" else "MW", {})
        v = [math.log10(r["sigma"] / cat[norm_name(r["name"])]) for r in SMP if klass(r) == cls and norm_name(r["name"]) in cat]
        out[cls] = v; pool += v
    res = {}
    for cls, v in out.items():
        use = v if len(v) >= 3 else pool
        mu = float(np.mean(use)); rms = float(np.std(use)); res[cls] = dict(m_c=math.sqrt(mu ** 2 + (rms / math.sqrt(len(use))) ** 2),
                                                                          n_match=len(v), pooled=len(v) < 3, mu=mu, rms=rms)
    res["M31 others"] = res["bright M31"]; res["LG field"] = res["MW classical"]
    return res
MEMB = membership_widths()

def dsph_rows(cls, with_cens=True):
    rr = [r for r in SMP if klass(r) == cls]
    if with_cens: rr += [r for r in CENS if klass(r) == cls]
    return rr

def eq_flag_dsph(r):
    if r["host"] not in VC: return False
    s = (r["cens"] or r["sigma"]) * 1e3; Re = r["rh"] * PC; d = Rh_X1(r); Vc = VC[r["host"]] * 1e3
    Mw = 4 * s * s * Re / G; Mh = Vc * Vc * d / G
    rJ = d * (Mw / (3 * Mh)) ** (1 / 3)
    return bool(Re / rJ >= 0.375 or (R12 * Re / s) > 0.1 * 2 * math.pi * d / Vc)
def eq_flag_coma(c, a0):
    Re = c["Re"] * KPC_C; s = c["sig"] * 1e3; d = c["dmean"] * KPC_C; g = g_beta(c["dmean"])
    Mw = 4 * s * s * Re / G_; Mh = g * d * d / G_; rJ = d * (Mw / (3 * Mh)) ** (1 / 3)
    V = math.sqrt(g * d)
    return bool(Re / rJ >= 0.375 or (R12 * Re / s) > 0.1 * 2 * math.pi * d / V)

def rJ_reading(y, a_m, d_m, Vc_kms, a0, reading, edge, kfac_v=1.0):
    """dSph r_J (a units) under a reading, RB2's rules."""
    K = lambda k, dd: k * (Vc_kms * 1e3 * kfac_v) ** 2 / dd ** 2 * a_m / a0
    if reading == "iso": return np.full(np.shape(y), np.inf)
    if reading == "weak": return rJ_iso(y, K(2.0, d_m))
    rJ = rJ_iso(y, K(3.0, d_m))
    if reading == "prim": return rJ
    kind, ds = edge
    cand = rJ / 3 ** (2 / 3)
    if ds is not None:
        cand2 = rJ_iso(y, K(3.0, ds * KPC))
        cand = np.minimum(cand2, rJ) if kind == "orbit" else np.minimum(cand, cand2)
    return cand

def central_dsph(r, a0, reading="prim", newton=False):
    """nominal residual (no MC, X1's nominal data side) and the quantities T13 needs."""
    s = r["cens"] or r["sigma"]
    ms = 10 ** r["logms"]; a_m = r["rh"] * PC; y = G * ms * MSUN / (a_m ** 2 * a0)
    gobs = 3.0 * (s * bnom(r) * 1e3) ** 2 / (R12 * a_m)
    if newton: rJ = np.array([1e-300])
    elif r["host"] in VC: rJ = rJ_reading(np.array([y]), a_m, Rh_X1(r), VC[r["host"]], a0, reading, edge_of(r))
    else: rJ = np.array([np.inf])
    g = float(gB(R12, np.array([y]), rJ)[0])
    return math.log10(gobs / a0) - math.log10(g), y, float(rJ[0])

def a_c_class(rows, a0, coma=False):
    v = []
    for r in rows:
        if coma:
            a = r["Re"] * KPC_C; y = G_ * r["Ms"] * MSUN_ / (a * a * a0)
            K = 3.0 * g_beta(r["dmean"]) / (r["dmean"] * KPC_C) * a / a0; rJ = float(rJ_iso(np.array([y]), np.array([K]))[0])
        else:
            if r["cens"]: continue
            _, y, rJ = central_dsph(r, a0)
        sw = R12 * float(gB(R12, np.array([y]), rJ)[0]) / 3.0; sv = vir_B(y, rJ)
        v.append(abs(math.log10(sv / sw)))
    return float(np.median(v))

def coma_resid(Ms, Re, sig, d_kpc, a0, k, ghfac=1.0, gofac=1.0):
    Ms, Re, sig, d_kpc = np.broadcast_arrays(*(np.asarray(v, float) for v in (Ms, Re, sig, d_kpc)))
    a = Re * KPC_C; y = G_ * Ms * MSUN_ / (a * a * a0)
    K = k * g_beta(d_kpc) * ghfac / (d_kpc * KPC_C) * a / a0
    rJ = rJ_iso(y, K)
    g = gB(R12, y, rJ)
    gobs = 3.0 * (sig * 1e3) ** 2 / (R12 * a) * gofac
    return np.log10(gobs / a0) - np.log10(g)
def coma_kw(d, reading):
    return 2 * d ** 2 / (d ** 2 + BETA["rc"] ** 2) if reading == "weak" else 3.0
def coma_smem(a0):
    m = lambda smp: float(np.mean([coma_resid(c["Ms"], c["Re"], np.array([c["sig"]]), np.array([c["dmean"]]), a0, 3.0)[0] for c in smp]))
    return abs(m(COMA) - m(ADM))

def run_class(cls, f, reading, N=4000, seed=0, off=(), only=None, a0=None, cens_mode="draw", drop_flag=False, mock=None):
    """Monte Carlo over the frozen budget + bootstrap over systems; returns the N class statistics.
    off: terms switched off; only: if given, every term not in it is off (measurement terms T5/T7/T8 included);
    mock: dict name -> sigma (planted mock dispersions, censored rows dropped)."""
    a0 = A0[f] if a0 is None else a0
    on = (lambda t: t in only) if only is not None else (lambda t: t not in off)
    rng = np.random.default_rng(seed)
    if cls == "Coma UDGs":
        rows = list(ADM)
        if drop_flag: rows = [c for c in rows if not eq_flag_coma(c, A0[f])]
        n = len(rows); ix = rng.integers(0, n, (N, n)); L = N * n; ixf = ix.ravel()
        col = lambda k: np.array([c[k] for c in rows], float)[ixf]
        rep = lambda v: np.repeat(v, n)
        Ms, Re, sig, esig, dproj, dmean = col("Ms"), col("Re"), col("sig"), col("esig"), col("dproj"), col("dmean")
        if mock is not None: sig = np.array([mock[c["name"]] for c in rows])[ixf]; esig = esig * sig / col("sig")
        flag = np.array([eq_flag_coma(c, A0[f]) for c in rows])[ixf]
        if on("T1"): Ms = Ms * rep(10 ** rng.normal(0, 0.20, N))
        if on("T2"): Ms = Ms * 10 ** rng.normal(0, 0.10, L)
        fD = rep(1.05 ** rng.normal(0, 1, N)) if on("T6") else 1.0
        Ms = Ms * fD ** 2; Re = Re * fD; dproj = dproj * fD; dmean = dmean * fD
        if on("T7"): Re = Re * 10 ** rng.normal(0, 0.04, L)
        if on("T8"): sig = np.abs(sig + rng.normal(0, 1, L) * esig)
        if on("T9"):
            w = rep(rng.normal(0, 90.0, N)); sig = np.sqrt(np.maximum(sig * sig - w, 0.01 * sig * sig))
        if on("T17"): sig = sig * rep(1.15 ** rng.normal(0, 1, N))
        go = np.ones(L)
        if on("T11"): go *= rep(10 ** rng.normal(0, COMA_SMEM[f], N))
        if on("T12"): go *= 10 ** rng.normal(0, 0.090, L)
        if on("T13"): go *= rep(10 ** rng.normal(0, AC[f]["Coma UDGs"], N))
        if on("T14"): go *= np.where(flag, 10 ** rng.normal(0, 0.20, L), 1.0)
        gh = rep(10 ** rng.normal(0, 0.08, N)) if on("T15") else 1.0
        if reading == "strong": d = dproj
        elif on("T16"): d = dproj + rng.random(L) * 2 * (dmean - dproj)
        else: d = dmean
        res = coma_resid(Ms, Re, sig, d, a0, coma_kw(d, reading), gh, go).reshape(N, n)
        return res.mean(axis=1)
    rows = dsph_rows(cls, with_cens=(cens_mode != "drop" and mock is None))
    if drop_flag: rows = [r for r in rows if not eq_flag_dsph(r)]
    n = len(rows); ix = rng.integers(0, n, (N, n)); L = N * n; ixf = ix.ravel()
    col = lambda k: np.array([(r[k] if r[k] is not None else np.nan) for r in rows], float)[ixf]
    rep = lambda v: np.repeat(v, n)
    s, sem, sep = col("sigma"), col("sem"), col("sep")
    if mock is not None:
        ms_ = np.array([mock[r["name"]] for r in rows])[ixf]; sem = sem * ms_ / s; sep = sep * ms_ / s; s = ms_
    cens = np.array([r["cens"] is not None for r in rows])[ixf]
    ufd = np.array([(r["mv"] is not None and r["mv"] > -7.7) for r in rows])[ixf]
    bfree = np.array([bnom(r) for r in rows])[ixf]
    bf07 = np.array([arr_f07.get(r["name"], med_f07 if (r["mv"] is not None and r["mv"] > -7.7) else 1.0) for r in rows])[ixf]
    flag = np.array([eq_flag_dsph(r) for r in rows])[ixf]
    hosts = [r["host"] for r in rows]
    Vc = np.array([VC.get(h, 0.0) for h in hosts])[ixf]
    dh = np.array([Rh_X1(r) for r in rows])[ixf]
    logms = col("logms")
    # --- distance (T5 independent, T6 coherent) and radius (T7)
    dDM = split_normal(rng, 0.0, col("dmem"), col("dmep"), L) if on("T5") else np.zeros(L)
    if on("T6"): dDM = dDM + rep(rng.normal(0, 0.10, N))
    fD = 10 ** (dDM / 5.0)
    rh = (np.abs(split_normal(rng, col("rh"), col("rhem"), col("rhep"), L)) if on("T7") else col("rh")) * fD
    # --- baryonic mass (T1, T2, T3, T4)
    lm = logms.copy()
    if on("T1"): lm += rep(rng.normal(0, 0.30, N))
    if on("T2"): lm += rng.normal(0, 0.10, L)
    if on("T3"): lm += -0.4 * split_normal(rng, 0.0, col("mvem"), col("mvep"), L)
    ms = 10 ** lm * fD ** 2
    if on("T4"):
        hi, hiul = col("hi"), col("hiul")
        MHI = np.where(np.isfinite(hi), 10 ** np.nan_to_num(hi), np.where(np.isfinite(hiul), rng.random(L) * 10 ** np.nan_to_num(hiul), 0.0))
        ms = ms + 2 * rng.random(L) * 0.5 * 1.33 * MHI
    # --- dispersion (T8, T18, T9, T11, T10)
    if mock is None and on("T18") and cens_mode == "draw":
        sc = s * (1.0 - rng.random(L))
    else:
        sc = s
    sig = np.where(cens, sc, np.abs(split_normal(rng, s, sem, sep, L)) if on("T8") else s)
    if on("T9"):
        w = rep(rng.normal(0, 1.3, N)); sig = np.sqrt(np.maximum(sig * sig - w, 0.01 * sig * sig))
    if on("T11"): sig = sig * rep(10 ** rng.normal(0, MEMB[cls]["m_c"], N))
    lb = np.log10(bfree)
    if on("T10"):
        t = rep(rng.uniform(-1, 1, N)); sm = rep(rng.uniform(0, 0.30, N))
        lb_ufd = np.where(t >= 0, np.log10(bfree) + t * (np.log10(bf07) - np.log10(bfree)), np.log10(bfree) * (1 + t))
        s0 = np.where(cens, s, col("sigma"))
        lb_oth = np.log10(bfree) - np.where((s0 >= 4) & (s0 < 10), np.log10(1 + sm), 0.0)
        lb = np.where(ufd, lb_ufd, lb_oth)
    sig = sig * 10 ** lb
    # --- observed acceleration multipliers (T12, T13, T14)
    go = np.ones(L)
    if on("T12"): go *= 10 ** rng.normal(0, 0.090, L)
    if on("T13"): go *= rep(10 ** rng.normal(0, AC[f][cls], N))
    if on("T14"): go *= np.where(flag, 10 ** rng.normal(0, 0.20, L), 1.0)
    vf = rep(10 ** rng.normal(0, 0.04, N)) if on("T15") else 1.0
    # --- prediction
    a_m = rh * PC; y = G * ms * MSUN / (a_m ** 2 * a0)
    rJ = np.full(L, np.inf)
    hosted = Vc > 0
    for i, r in enumerate(rows):
        if r["host"] not in VC: continue
        m = (ixf == i)
        if not m.any(): continue
        vfi = vf[m] if np.ndim(vf) else 1.0
        rJ[m] = rJ_reading(y[m], a_m[m], dh[m], VC[r["host"]], a0, reading, edge_of(r), vfi)
    g = gB(R12, y, rJ)
    gobs = 3.0 * (sig * 1e3) ** 2 / (R12 * a_m) * go
    with np.errstate(divide="ignore"):
        res = (np.log10(gobs / a0) - np.log10(g)).reshape(N, n)
    return np.median(res, axis=1)

def summ(stat):
    q = np.percentile(stat, [2.5, 50, 97.5]); return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], width95=float(q[2] - q[0]))
def mdo(stat, line_grid=np.arange(0.0, 2.0001, 0.01)):
    q = np.percentile(stat, [2.5, 50, 97.5]); e = stat - q[1]; lo_off, hi_off = q[0] - q[1], q[2] - q[1]
    best = {}
    for sgn in (+1, -1):
        best[sgn] = None
        for dl in line_grid:
            m = sgn * dl + e
            det = np.mean((m + lo_off > 0) | (m + hi_off < 0))
            if det >= 0.8: best[sgn] = float(dl); break
    vals = [v for v in best.values()]
    return None if any(v is None for v in vals) else max(vals)
def label_of(st, md):
    lo, hi = st["ci95"]
    if lo > 0: return "B FAILS HIGH"
    if hi < 0: return "B FAILS LOW"
    if md is None or md > 0.30: return "NO POWER"
    return "B CONSISTENT"
def seed_of(cls, f, rd, extra=0):
    ci = (GRADED + REPORTED).index(cls); return 20261110 + 1000 * ci + 100 * FOOTS.index(f) + 10 * (READINGS.index(rd) if rd in READINGS else 9) + extra

# ============================================================== precomputed class widths (T11 Coma, T13)
AC = {f: {cls: a_c_class(dsph_rows(cls), A0[f]) for cls in GRADED[:3] + REPORTED} for f in FOOTS}
for f in FOOTS: AC[f]["Coma UDGs"] = a_c_class(ADM, A0[f], coma=True)
COMA_SMEM = {f: coma_smem(A0[f]) for f in FOOTS}

RES = dict(lane="DSB1", tag=TAG, criteria="2c7beb7b92", note="TEST lane: relabels nothing; kappa = 1/2 FITTED; not theory closed. Adopts nothing.",
           rows={cls: dict(measured=[r["name"] for r in SMP if klass(r) == cls], censored=[(r["name"], r["cens"]) for r in CENS if klass(r) == cls])
                 for cls in GRADED[:3] + REPORTED},
           coma_rows=[c["name"] for c in ADM], membership=MEMB, a_c=AC, coma_s_mem=COMA_SMEM,
           eq_flagged={"dSph": [r["name"] for r in SMP + CENS if klass(r) in GRADED and eq_flag_dsph(r)],
                       "Coma": {f: [c["name"] for c in ADM if eq_flag_coma(c, A0[f])] for f in FOOTS}},
           m31_distance_kpc=M31D, KA={}, footings={}, MUTATE={})
P(f"DSB1 {'MUTATE' if MUT else 'MAIN'}: form B on the hosted dwarf classes with the frozen budget. kappa = 1/2 FITTED; not theory closed.")
P(f"rows: " + "; ".join(f"{c} {len(v['measured'])} measured + {len(v['censored'])} censored" for c, v in RES["rows"].items()) + f"; Coma {len(ADM)}")
P(f"censored rows: {[(r['name'], r['cens'], klass(r)) for r in CENS]}")
P(f"membership m_c (T11): " + "; ".join(f"{c} {v['m_c']:.3f} dex (n {v['n_match']}{', pooled' if v['pooled'] else ''})" for c, v in MEMB.items()))
P(f"a_c (T13): " + "; ".join(f"{f[:3]} " + ", ".join(f"{c} {v:.3f}" for c, v in AC[f].items()) for f in FOOTS))
P(f"Coma s_mem (T11): " + ", ".join(f"{f[:3]} {v:.3f} dex" for f, v in COMA_SMEM.items()))
P(f"T14 flagged: {RES['eq_flagged']}")

# ============================================================== known answers
def known_answers():
    # KA-a: X1's build copied, budget off, Newton
    RNG = np.random.default_rng(20261031); DS = {}
    for f in FOOTS:
        DS[f] = build(SMP, A0[f], RNG, mvrule=True)
        build(SMP, A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True, mvrule=True)
    X1ROW = {(r["footing"], r["name"]): r for r in X1CSV}
    dmax = 0.0; nrow = 0; dc = []
    for f in FOOTS:
        X = DS[f]
        for i, r in enumerate(X["rows"]):
            xr = X1ROW[(f, r["name"])]; nrow += 1
            v = X["lb"][i] - math.log10(FW_N)
            dmax = max(dmax, abs(float(np.median(v)) - float(xr["Delta[Newton]"])), abs(float(np.std(v)) - float(xr["sdMC[Newton]"])))
            dc.append(abs(central_dsph(r, A0[f], newton=True)[0] - float(xr["Delta[Newton]"])))
    ok_a = nrow == len(X1CSV) and dmax <= 1e-9 and float(np.median(dc)) <= 0.01 and max(dc) <= 0.06
    check("KA-a", ok_a, f"X1 per-system Delta[Newton] and sdMC reproduced over {nrow} rows: max |d| {dmax:.1e} (line 1e-9); "
          f"central-value residual function vs X1 medians: median |d| {np.median(dc):.4f}, max {max(dc):.4f} dex (lines 0.01 / 0.06)")
    RES["KA"]["KA-a"] = dict(rows=nrow, max_abs=dmax, central_median=float(np.median(dc)), central_max=float(max(dc)))
    # KA-b: Fornax Wolf mass
    fx = [r for r in SMP if r["name"] == "Fornax"][0]
    M = 3 * (fx["sigma"] * 1e3) ** 2 * R12 * fx["rh"] * PC / G / MSUN; lM = math.log10(M); lvd = fl(fx["_raw"]["mass_dynamical_wolf"])
    check("KA-b", abs(lM - 7.88) <= 0.15 and abs(lM - lvd) <= 0.05,
          f"Fornax log M_1/2 {lM:.3f} vs Campbell+2017 Wolf 7.88 (|d| {abs(lM-7.88):.3f}, line 0.15; PROVISIONAL) and LVD {lvd:.2f} (|d| {abs(lM-lvd):.3f}, line 0.05)")
    RES["KA"]["KA-b"] = dict(logM=lM, campbell=7.88, lvd=lvd)
    # KA-c: limits and planted offset
    yv = np.geomspace(1e-6, 1e3, 50)
    l1 = float(np.max(np.abs(gB(R12, yv, np.inf) - gl(gNp(R12, yv))))); l2 = float(np.max(np.abs(np.log10(gB(R12, yv, 1e-30) / gNp(R12, yv)))))
    l3 = abs(vir_B(1e-9, np.inf) / ((2.0 / 9.0) * math.sqrt(1e-9)) - 1)
    rec = {}; off_err = 0.0; ok_rec = True
    for f in FOOTS:
        for cls in GRADED:
            mock = mock_sigmas(cls, f, 0.40)
            off_err = max(off_err, mock["_check"])
            st = summ(run_class(cls, f, "prim", N=1000, seed=seed_of(cls, f, "prim", 7), mock=mock))
            rec[f"{f}|{cls}"] = st["median"]; ok_rec &= abs(st["median"] - 0.40) <= 0.10
    ok_c = l1 == 0.0 and l2 < 1e-12 and l3 < 1e-3 and off_err <= 1e-6 and ok_rec
    check("KA-c", ok_c, f"limits: r_J inf -> iso {l1:.1e}, r_J 0 -> Newton {l2:.1e}, deep virial {l3:.1e}; planted +0.40: budget off max |d| {off_err:.1e} "
          f"(line 1e-6); full budget recovered " + ", ".join(f"{k} {v:+.3f}" for k, v in rec.items()) + " (line 0.10)")
    RES["KA"]["KA-c"] = dict(limits=[l1, l2, l3], budget_off_err=off_err, recovered=rec)
    return all(CHK[k]["ok"] for k in ("KA-a", "KA-b", "KA-c")), DS

def mock_sigmas(cls, f, delta):
    """dispersions that put every measured row at B primary (nominal side) x 10^delta."""
    a0 = A0[f]; out = {}; err = 0.0
    if cls == "Coma UDGs":
        for c in ADM:
            r0 = float(coma_resid(c["Ms"], c["Re"], np.array([c["sig"]]), np.array([c["dmean"]]), a0, 3.0)[0])
            out[c["name"]] = c["sig"] * 10 ** ((delta - r0) / 2)
            err = max(err, abs(float(coma_resid(c["Ms"], c["Re"], np.array([out[c["name"]]]), np.array([c["dmean"]]), a0, 3.0)[0]) - delta))
    else:
        for r in dsph_rows(cls, with_cens=False):
            r0 = central_dsph(r, a0)[0]; out[r["name"]] = r["sigma"] * 10 ** ((delta - r0) / 2)
            r2 = dict(r); r2["sigma"] = out[r["name"]]; err = max(err, abs(central_dsph(r2, a0)[0] - delta))
    out["_check"] = err
    return out

def budget_off_rb2(DS):
    """budget off in RB2's convention: X1-built per-system medians / sds under B primary, XF1 boot_median; Coma mean E +- 1.96 se."""
    o = {}
    for f in FOOTS:
        X = DS[f]; per = {}
        for i, r in enumerate(X["rows"]):
            if klass(r) not in GRADED + REPORTED: continue
            y = 10 ** X["ly"][i]; a_m = 10 ** X["la"][i] * PC
            if r["host"] in VC: rJ = rJ_reading(y, a_m, Rh_X1(r), VC[r["host"]], A0[f], "prim", edge_of(r))
            else: rJ = np.full(y.shape, np.inf)
            v = X["lb"][i] - np.log10(gB(R12, y, rJ) / (y / (2 * R12 ** 2)))
            per[r["name"]] = (float(np.median(v)), float(np.std(v)))
        o[f] = {}
        for cls in GRADED[:3] + REPORTED:
            nm = [r["name"] for r in X["rows"] if klass(r) == cls]
            o[f][cls] = boot_median([per[n][0] for n in nm], [per[n][1] for n in nm])
        E = np.array([float(coma_resid(c["Ms"], c["Re"], np.array([c["sig"]]), np.array([c["dmean"]]), A0[f], 3.0)[0]) for c in ADM])
        sE = np.array([2 * c["esig"] / c["sig"] / math.log(10) for c in ADM])
        se = max(float(np.std(E, ddof=1) / math.sqrt(len(E))), float(math.sqrt(np.sum(sE ** 2)) / len(E)))
        o[f]["Coma UDGs"] = dict(median=float(E.mean()), ci95=[float(E.mean() - 1.96 * se), float(E.mean() + 1.96 * se)], n=len(E), se=se)
    return o

def lane_label(lab):
    """lab[f][cls] primary labels on graded classes."""
    both = lambda L: [c for c in GRADED if all(lab[f][c] == L for f in FOOTS)]
    anyf = lambda L: [c for c in GRADED if any(lab[f][c] == L for f in FOOTS)]
    hi, lo = both("B FAILS HIGH"), both("B FAILS LOW")
    if hi: return "HIGH ROWS STAND", dict(high=hi, low=lo)
    if lo: return "LOW ROWS", dict(low=lo)
    if not anyf("B FAILS HIGH") and not anyf("B FAILS LOW"):
        cons = both("B CONSISTENT")
        return ("HIGH ROWS DO NOT STAND" if len(cons) >= 2 else "NO POWER"), dict(consistent_both=cons)
    return "SPLIT", dict(high_any=anyf("B FAILS HIGH"), low_any=anyf("B FAILS LOW"))

# ============================================================== main
if not MUT:
    P("\n=== KNOWN ANSWERS ===")
    ok, DS = known_answers(); RES["KA_ok"] = ok
    if not ok:
        P("A KNOWN ANSWER FAILED: grading stops (FROZEN section 5).")
    else:
        P("\n=== GRADING (primary graded; weak / strong reported) ===")
        LAB = {f: {} for f in FOOTS}
        for f in FOOTS:
            FR = RES["footings"][f] = {}
            for cls in GRADED + REPORTED:
                C = FR[cls] = {}
                for rd in READINGS:
                    if cls == "LG field" and rd != "prim": continue
                    st = run_class(cls, f, rd, seed=seed_of(cls, f, rd)); S = summ(st); md = mdo(st)
                    C[rd] = dict(S, MDO=md, label=label_of(S, md))
                lab = C["prim"]["label"]
                if cls in GRADED: LAB[f][cls] = lab
                # reported variants (primary)
                V = C["variants"] = {}
                if cls not in ("Coma UDGs",):
                    for cm in ("at_UL", "drop"):
                        if cm == "at_UL":
                            st = run_class(cls, f, "prim", seed=seed_of(cls, f, "prim", 1), off=("T18",))
                        else:
                            st = run_class(cls, f, "prim", seed=seed_of(cls, f, "prim", 2), cens_mode="drop")
                        V["censored_" + cm] = summ(st)
                st = run_class(cls, f, "prim", seed=seed_of(cls, f, "prim", 3), drop_flag=True); V["flagged_dropped"] = summ(st)
                P(f"[{f[:3]}] {cls:15s} prim {C['prim']['median']:+.3f} [{C['prim']['ci95'][0]:+.3f}, {C['prim']['ci95'][1]:+.3f}] "
                  f"MDO {C['prim']['MDO']} -> {lab} | weak {C.get('weak', {}).get('median', float('nan')):+.3f} {C.get('weak', {}).get('label', '-')} "
                  f"| strong {C.get('strong', {}).get('median', float('nan')):+.3f} [{C.get('strong', {}).get('ci95', [float('nan')]*2)[0]:+.3f}, "
                  f"{C.get('strong', {}).get('ci95', [float('nan')]*2)[1]:+.3f}] {C.get('strong', {}).get('label', '-')} | "
                  + " ".join(f"{k} {v['median']:+.3f} [{v['ci95'][0]:+.3f}, {v['ci95'][1]:+.3f}]" for k, v in V.items()))
        RES["labels"] = LAB
        cl = {c: (LAB["canonical"][c] if LAB["canonical"][c] == LAB["alt"][c] else f"SPLIT ({LAB['canonical'][c]} / {LAB['alt'][c]})") for c in GRADED}
        RES["class_labels"] = cl
        ll, det = lane_label(LAB); RES["lane_label"] = ll; RES["lane_detail"] = det
        P(f"\nLANE LABEL: {ll} {det}")
        P("class labels: " + "; ".join(f"{c}: {v}" for c, v in cl.items()))
        # budget off, RB2 convention
        P("\n=== BUDGET OFF (RB2 convention, reported) ===")
        BO = budget_off_rb2(DS); RES["budget_off_rb2_convention"] = BO
        for f in FOOTS:
            P(f"[{f[:3]}] " + "; ".join(f"{c} {v['median']:+.3f} [{v['ci95'][0]:+.3f}, {v['ci95'][1]:+.3f}]" for c, v in BO[f].items()))
        # width table (graded, primary, N 2000)
        P("\n=== WIDTH TABLE (95 % width, primary; all on / each term removed / each term alone; N 2000) ===")
        WT = RES["width_table"] = {}
        for f in FOOTS:
            WT[f] = {}
            for cls in GRADED:
                base = summ(run_class(cls, f, "prim", N=2000, seed=seed_of(cls, f, "prim", 5)))["width95"]
                rm = {t: summ(run_class(cls, f, "prim", N=2000, seed=seed_of(cls, f, "prim", 5), off=(t,)))["width95"] for t in TERMS}
                al = {t: summ(run_class(cls, f, "prim", N=2000, seed=seed_of(cls, f, "prim", 5), only=(t,)))["width95"] for t in TERMS}
                nil = summ(run_class(cls, f, "prim", N=2000, seed=seed_of(cls, f, "prim", 5), only=()))["width95"]
                WT[f][cls] = dict(all=base, removed=rm, alone=al, none=nil)
                top = sorted(al.items(), key=lambda kv: -kv[1])[:4]
                P(f"[{f[:3]}] {cls:15s} all {base:.3f} | bootstrap only {nil:.3f} | alone top: " + ", ".join(f"{t} {w:.3f}" for t, w in top)
                  + " | removed: " + ", ".join(f"{t} {rm[t]:.3f}" for t, _ in top))
else:
    P("\n=== MUTATE ===")
    M = RES["MUTATE"]
    m1 = {}; m2 = {}; m3 = {}
    for f in FOOTS:
        for cls in GRADED:
            base = run_class(cls, f, "prim", seed=seed_of(cls, f, "prim")); sb = summ(base); md = mdo(base)
            s1 = summ(run_class(cls, f, "prim", seed=seed_of(cls, f, "prim"), off=("T1",)))
            m1[f"{f}|{cls}"] = (sb["width95"], s1["width95"])
            s2 = summ(run_class(cls, f, "prim", seed=seed_of(cls, f, "prim"), a0=2 * A0[f]))
            m2[f"{f}|{cls}"] = (sb["median"], s2["median"])
            mk = mock_sigmas(cls, f, 0.60)
            s3 = summ(run_class(cls, f, "prim", seed=seed_of(cls, f, "prim", 8), mock=mk))
            m3[f"{f}|{cls}"] = (label_of(s3, md), md, s3["median"], s3["ci95"])
    b1 = all(b < a for a, b in m1.values()); b2 = all(b < a for a, b in m2.values())
    b3 = all(v[0] == "B FAILS HIGH" for v in m3.values() if v[1] is not None and v[1] <= 0.60)
    check("M1", b1, "T1 removed narrows the 95 % width: " + ", ".join(f"{k} {a:.3f}->{b:.3f}" for k, (a, b) in m1.items()))
    check("M2", b2, "a0 doubled lowers the class residual: " + ", ".join(f"{k} {a:+.3f}->{b:+.3f}" for k, (a, b) in m2.items()))
    check("M3", b3, "planted +0.60 read FAILS HIGH where MDO <= 0.60: " + ", ".join(f"{k} {v[0]} (MDO {v[1]}, {v[2]:+.3f})" for k, v in m3.items()))
    M.update(M1=m1, M2=m2, M3={k: list(v) for k, v in m3.items()}, bite=dict(M1=b1, M2=b2, M3=b3))

RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
P(f"\nruntime {RES['runtime_s']:.0f} s. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=lambda o: o if not isinstance(o, np.generic) else o.item())
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
