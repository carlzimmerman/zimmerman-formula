#!/usr/bin/env python3
"""WLG1R (FROZEN_CRITERIA.md, 8a730ebaa1; BLIND_BRIEF.md, ec7fed6252): blind re-grade of WLG1's frozen question.
Do the groups that hold Euclid's wide lenses run faster than v*(z_l), and does the reference cold dark energy halo at the
5.41 share of the group's baryons supply the observed Einstein mass?

Own code from the definitions. Shared code imported read-only: EUC1's euc1.py (cosmology, Sersic fractions, g_law,
Gauss-Legendre nodes) and JNT2's jnt2_common.py (H(z), v*, v_L). LNJ1's FRZ1 halo and cylinder functions copied (marked).
Bytecode writing is off, so nothing is written outside this folder.
  nice -n 19 python3 -I wlg1r.py                       # main run (twin gates computed in-process)
  WLG1R_MUTATE=ZS|INJ|X0 nice -n 19 python3 -I wlg1r.py  # twin run: writes wlg1r_MUTATE_<t>.*, exits 1
TEST lane, blind, POST HOC. Adopts nothing. kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed.
Cold dark energy is a gravitating field component, not a particle."""
import os, sys, csv, gzip, io, json, math, hashlib, warnings, importlib.util, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
os.environ.pop("EUC1_MUTATE", None)
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ECL = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
CONES = os.path.join(REPO, "_external_data", "euclid_dr1_mer_cones_euc6r")
PHZ = os.path.join(REPO, "_external_data", "wlg1r_phz_by_id")
PHZ_OTHER = os.path.join(REPO, "_external_data", "wlg1_phz_by_id")      # untracked data of the other build: rows only
E6R = os.path.join(REPO, "closure_2026_11_12", "EUC6R_blind_regrade")
LNJ1 = os.path.join(REPO, "closure_2026_11_13", "LNJ1_joint_switch_on_euclid_lenses", "lnj1_per_lens.csv")
EUC17 = os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_per_lens.csv")
EUC8 = os.path.join(REPO, "closure_2026_11_12", "EUC8_wide_lens_residual_profile", "euc8_wide_per_lens.csv")
def load_mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E = load_mod("euc1_ro", os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling", "euc1.py"))
J = load_mod("jnt2_common_ro", os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_common.py"))

MUT = os.environ.get("WLG1R_MUTATE", "").strip()
if MUT not in ("", "ZS", "INJ", "X0"): sys.exit("WLG1R_MUTATE must be empty, ZS, INJ or X0")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
G, MSUN, PC, KPC, ARCSEC = E.G, E.MSUN, E.PC, E.KPC, E.ARCSEC
MPC_M = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; A0_EUC = dict(E.FOOT); FOOTS = ("canonical", "alt")
XC = 5.41; ZS_INF = E.ZS_INF; SEED = 20261114; NBOOT = 2000; SHIFT = 0.036
FLUX_CUT, PLP_CUT, DQF_CUT = 5.75, 0.7, 4
R_IN, R_BG = (30.0, 300.0), (600.0, 1000.0); AREA_RATIO = (R_IN[1] ** 2 - R_IN[0] ** 2) / (R_BG[1] ** 2 - R_BG[0] ** 2)
GAS = {"G-MID": dict(W=5.2e12, C=0.0, L=0.0, R=0.0), "G-0": dict(W=0.0, C=0.0, L=0.0, R=0.0), "G-HI": dict(W=8.3e12, C=3.0e12, L=0.0, R=0.0)}
LINE = 0.10
P(f"WLG1R{(' MUTATE ' + MUT) if MUT else ''}: blind re-grade of WLG1's frozen question (criteria 8a730ebaa1). TEST lane, blind, POST HOC. "
  "Adopts nothing. kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed.")

def sha256b(b): return hashlib.sha256(b).hexdigest()
def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()
def fl(v):
    try: return float(v)
    except Exception: return float("nan")

# ============================================================ ECLIPSE sample S (EUC1's cuts; LNJ1's loader logic, re-written)
for fn, hx in E.SHA.items():
    if sha256f(os.path.join(ECL, fn)) != hx: sys.exit("ECLIPSE hash mismatch " + fn)
P("  ECLIPSE key and object catalogues: sha256 match EUC1's frozen hashes")
OBJ = {r["Unique_Identifier"]: r for r in csv.DictReader(open(os.path.join(ECL, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8"))}
KEY = {r["unique_identifier"]: r for r in csv.DictReader(open(os.path.join(ECL, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8"))}
ROWS = []
for uid, r in KEY.items():
    o = OBJ.get(uid)
    if o is None: continue
    ROWS.append(dict(id=uid, grade=r["lens_grade"].strip(), success=r["lens_model_success"].strip() == "True", final=r["final_sample"].strip() == "True",
                     large=o["large_system_warning"].strip() == "True", z=fl(r["eclipse_median_phz"]), lm=fl(r["eclipse_log_survived_mass_med"]),
                     tE=fl(r["eclipse_effective_einstein_radius"]), te=fl(r["eclipse_effective_radius"]), n=fl(r["eclipse_sersic_index"])))
S = [r for r in ROWS if r["grade"] in ("A", "B") and r["success"] and r["final"] and not r["large"] and r["tE"] > 0 and r["te"] > 0
     and 0.6 <= r["n"] <= 10.0 and r["z"] > 0 and r["lm"] > 0]
N = len(S); SIDX = {r["id"]: i for i, r in enumerate(S)}
Z = np.array([r["z"] for r in S]); LM0 = np.array([r["lm"] for r in S]); TE = np.array([r["tE"] for r in S])
THE = np.array([r["te"] for r in S]); NS = np.array([r["n"] for r in S]); GR = np.array([r["grade"] for r in S])
DA = E.EUCLID.DA(Z); RE = TE * ARCSEC * DA; REFF = THE * ARCSEC * DA
P(f"  sample S: N = {N}; W (theta_E >= 1.7\") {int((TE >= 1.7).sum())}")

# ============================================================ law S and projection (LNJ1's construction, re-written)
U = np.arccosh(np.maximum(1.0e6 * KPC / RE, 1.0 + 1e-9))
RN = RE[:, None] * np.cosh(E.GLX[None, :] * U[:, None]); PREF = RE ** 2 / G * U
GN1 = G * MSUN * E.M3D_frac(RN, REFF[:, None], NS[:, None]) / RN ** 2
F2D = E.M2D_frac(RE, REFF, NS)
def m2d(g, idx): return PREF[idx] * np.sum(E.GLW[None, :] * g, axis=1)
def m_law(Ms_sun, a0, idx): return m2d(E.g_law(Ms_sun[:, None] * GN1[idx], a0, "S"), idx)
def m_obs(idx, zs): return math.pi * RE[idx] ** 2 * E.EUCLID.sigcr(Z[idx], zs)

# ============================================================ FRZ1's halo: COPIED from LNJ1 (lnj1.py lines 104-144)
hh = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / hh ** 2; FB = om_b / (om_b + om_c); RHO_M = Om * 2.77536627e11
m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def Omz(z): return Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om)
def conc_fn(z, cfac=1.0): return lambda M: cfac * 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
def halo_basics_z(M, conc, dta, omz):
    c = conc(M); r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc)
ZG = np.round(np.arange(0.0, 3.0001, 0.05), 4); LMG = np.arange(8.5, 16.5001, 0.02)
_TAB = {}
def halo_table(cfac):
    if cfac not in _TAB:
        lmta = np.zeros((len(ZG), len(LMG))); lrs = np.zeros_like(lmta); lrta = np.zeros_like(lmta)
        for i, z in enumerate(ZG):
            conc = conc_fn(z, cfac); dta = dta_of(z); omz = Omz(z); a = MPC_M / hh / (1 + z)
            for j, lMm in enumerate(LMG):
                hb = halo_basics_z(10 ** lMm, conc, dta, omz)
                lmta[i, j] = math.log10(hb["Mta"]); lrs[i, j] = math.log10(hb["rs"] * a); lrta[i, j] = math.log10(hb["rta"] * a)
        _TAB[cfac] = (lmta, lrs, lrta)
    return _TAB[cfac]
def halo_shape(Mhalo_sun, z, cfac=1.0):
    """physical r_s, r_ta (m) of FRZ1's halo whose turnaround mass is Mhalo h / (1 - f_b) (LNJ1's X M_b h / (1 - f_b))."""
    lmta, lrs, lrta = halo_table(cfac)
    t = np.log10(Mhalo_sun * hh / (1 - FB)); zi = np.clip(np.searchsorted(ZG, z) - 1, 0, len(ZG) - 2); w = (z - ZG[zi]) / (ZG[zi + 1] - ZG[zi])
    out = []
    for arr in (lrs, lrta):
        v0 = np.array([np.interp(t[k], lmta[zi[k]], arr[zi[k]]) for k in range(len(t))])
        v1 = np.array([np.interp(t[k], lmta[zi[k] + 1], arr[zi[k] + 1]) for k in range(len(t))])
        out.append(10 ** ((1 - w) * v0 + w * v1))
    return out[0], out[1]
def cyl_frac(idx, rs, rta):
    """fraction of a truncated NFW (unit mass inside turnaround) projected inside R_E (LNJ1's c_cyl per unit mass)."""
    r = np.minimum(RN[idx], rta[:, None]); sh = m_nfw(r / rs[:, None]) / m_nfw(rta / rs)[:, None]
    return m2d(G * sh / RN[idx] ** 2, idx)
# ============================================================ end of copied block

def H_si(z): return J.H0 * np.array([J.E(zz) for zz in np.atleast_1d(z)])
def vstar(ft, z, fac=1.0): return fac * J.vstar0_kms(ft) / np.array([J.E(zz) for zz in np.atleast_1d(z)])
def vL_signed(Mb_sun, z):
    x = 10 * J.G * (1 + J.XS) * np.abs(Mb_sun) * J.MSUN * H_si(z)
    return np.sign(Mb_sun) * x ** (1 / 3) / 1e3
def R200c_kpc(Mtot_sun, z):
    return (J.G * Mtot_sun * J.MSUN / (100 * H_si(z) ** 2)) ** (1 / 3) / KPC

# ============================================================ targets, cones, photo-z rows
TG = list(csv.DictReader(open(os.path.join(E6R, "euc6r_targets.csv"), newline="")))
MAN6 = {m["target"]: m for m in csv.DictReader(open(os.path.join(E6R, "euc6r_manifest.csv"), newline=""))}
CNT6 = {r["target"]: r for r in csv.DictReader(open(os.path.join(E6R, "euc6r_counts.csv"), newline=""))}
PHROW = {}; ndup = 0
MANF = list(csv.DictReader(open(os.path.join(HERE, "wlg1r_fetch_manifest.csv"), newline="")))
for m in MANF:
    body = gzip.open(os.path.join(PHZ, m["file"])).read()
    if sha256b(body) != m["sha256_raw"]: sys.exit("photo-z batch hash mismatch " + m["file"])
    for r in csv.DictReader(io.StringIO(body.decode())):
        k = int(r["object_id"])
        if k in PHROW: ndup += 1; continue
        PHROW[k] = r
P(f"  photo-z rows: {len(PHROW)} distinct objects from {len(MANF)} batches (hashes match the manifest); duplicate rows {ndup}")
def lens_mer(uid):
    v = OBJ[uid]["MER_object_id"].strip()
    if not v: return None
    return int(float(v)) if "e" in v.lower() else int(v)

def sep_rad(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    a = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))

T = []
for t in TG:
    m = MAN6[t["target"]]; body = gzip.open(os.path.join(CONES, m["file"])).read()
    if sha256b(body) != m["sha256_raw"]: sys.exit("cone hash mismatch " + t["target"])
    rd = list(csv.DictReader(io.StringIO(body.decode())))
    oid = np.array([int(o["object_id"]) for o in rd], dtype=np.int64)
    ra = np.array([fl(o["right_ascension"]) for o in rd]); de = np.array([fl(o["declination"]) for o in rd])
    fx = np.array([fl(o["flux_h_templfit"]) for o in rd]); sp = np.array([fl(o["spurious_flag"]) for o in rd])
    dq = np.array([fl(o["det_quality_flag"]) for o in rd]); pl = np.array([fl(o["point_like_prob"]) for o in rd])
    z = float(t["z"]); ok = (fx > FLUX_CUT) & (sp == 0) & (dq < DQF_CUT) & (pl < PLP_CUT)
    R = sep_rad(float(t["ra"]), float(t["dec"]), ra, de) * float(E.EUCLID.DA(z)) / KPC
    d = dict(target=t["target"], kind=t["kind"], lens_id=t["lens_id"], pair=int(t["pair"]), z=z, logm_cat=float(t["logm"]))
    d["n_in"] = int((ok & (R >= R_IN[0]) & (R < R_IN[1])).sum()); d["n_bg"] = int((ok & (R >= R_BG[0]) & (R < R_BG[1])).sum())
    inner = ok & (R < R_BG[1]); has = np.array([int(k) in PHROW for k in oid], dtype=bool)
    d["n_cut_1000"] = int(inner.sum()); d["cover"] = float((inner & has).sum() / max(inner.sum(), 1))
    mer = lens_mer(t["lens_id"]) if t["kind"] in ("W", "C", "L") else None
    d["mer"] = mer; d["mer_in_cone"] = bool(mer is not None and (oid == mer).any())
    d["mer_row"] = PHROW.get(mer) if d["mer_in_cone"] else None
    # census objects: cut, R < 1000 kpc, photo-z row, class 2 (galaxy), finite phz_median, not the lens's own MER object
    rows = [(i, PHROW[int(oid[i])]) for i in np.where(inner & has)[0]]
    rows = [(i, r) for i, r in rows if fl(r["phz_classification"]) == 2 and np.isfinite(fl(r["phz_median"])) and (mer is None or int(oid[i]) != mer)]
    ii = np.array([i for i, _ in rows], dtype=int)
    d["R"] = R[ii]; d["phz"] = np.array([fl(r["phz_median"]) for _, r in rows])
    lmpp = np.array([fl(r["phz_pp_median_stellarmass"]) for _, r in rows]); zpp = np.array([fl(r["phz_pp_median_redshift"]) for _, r in rows])
    good = np.isfinite(lmpp) & (lmpp > 0) & np.isfinite(zpp) & (zpp > 0)
    DLl = float(E.EUCLID.DL(z))
    d["lm_moved"] = np.where(good, lmpp + 2 * np.log10(DLl / E.EUCLID.DL(np.where(good, zpp, 1.0))), np.nan)
    d["logL"] = np.log10(4 * math.pi * DLl ** 2 * np.where(fx[ii] > 0, fx[ii], np.nan))
    T.append(d)
TI = {d["target"]: d for d in T}
P(f"  targets {len(T)} (W {sum(d['kind'] == 'W' for d in T)}, C {sum(d['kind'] == 'C' for d in T)}, L {sum(d['kind'] == 'L' for d in T)}, R {sum(d['kind'] == 'R' for d in T)}); cone hashes match EUC6R's manifest")

# ============================================================ graded lenses (edge rule + photo-z coverage)
ref_bg = float(np.median([d["n_bg"] for d in T if d["kind"] in ("W", "C", "L")])); THR = 0.4 * ref_bg
for d in T: d["edge_ok"] = d["n_bg"] >= THR; d["cover_ok"] = d["cover"] >= 0.80; d["graded"] = d["edge_ok"] and d["cover_ok"]
def grad(kind): return [d for d in T if d["kind"] == kind and d["graded"]]
for k in "WCLR":
    a = [d for d in T if d["kind"] == k]
    P(f"  {k}: {len(a)} targets; edge fail {sum(not d['edge_ok'] for d in a)}; coverage < 80 % {sum(not d['cover_ok'] for d in a)}; graded {sum(d['graded'] for d in a)}; median coverage {np.median([d['cover'] for d in a]):.3f}")
P(f"  edge reference median N_bg {ref_bg:.1f}, threshold {THR:.1f}")

# ============================================================ lens stellar masses
F17 = {r["unique_identifier"]: float(r["f_in_mask"]) for r in csv.DictReader(open(EUC17, newline=""))}
def lens_logm(d, corrected):
    lm = d["logm_cat"] + SHIFT
    if corrected and d["lens_id"] in F17: lm -= math.log10(F17[d["lens_id"]])
    return lm
ncorr = {k: sum(d["lens_id"] in F17 for d in T if d["kind"] == k) for k in "WC"}
P(f"  EUC17 in-mask correction available: W {ncorr['W']} of {sum(d['kind'] == 'W' for d in T)}, C {ncorr['C']} of {sum(d['kind'] == 'C' for d in T)} (rest uncorrected, counted)")

def delta_scale(corrected):
    v = []
    for d in T:
        if d["kind"] not in ("W", "C") or d["mer_row"] is None: continue
        r = d["mer_row"]; lm = fl(r["phz_pp_median_stellarmass"]); zp = fl(r["phz_pp_median_redshift"])
        if not (np.isfinite(lm) and lm > 0 and np.isfinite(zp) and zp > 0): continue
        mv = lm + 2 * math.log10(float(E.EUCLID.DL(d["z"])) / float(E.EUCLID.DL(zp)))
        v.append(lens_logm(d, corrected) - mv)
    return float(np.median(v)), len(v)

# ============================================================ census
def window(d, w, zc=None):
    zc = d["z"] if zc is None else zc
    return np.abs(d["phz"] - zc) <= w * (1 + zc)
def ml_median(w):
    v = []
    for d in T:
        m = window(d, w) & (d["R"] >= 30) & np.isfinite(d["lm_moved"]) & np.isfinite(d["logL"])
        v.append(d["lm_moved"][m] - d["logL"][m])
    return float(np.median(np.concatenate(v)))
def census(d, w, Delta, ml, zc=None):
    """member masses (Msun) and radii in the window; background surface density (Msun / kpc^2)."""
    m = window(d, w, zc) & (d["R"] >= 30)
    lm = np.where(np.isfinite(d["lm_moved"][m]), d["lm_moved"][m], d["logL"][m] + ml) + Delta
    nfb = int((~np.isfinite(d["lm_moved"][m]) & np.isfinite(d["logL"][m])).sum())
    mass = np.where(np.isfinite(lm), 10 ** lm, 0.0); R = d["R"][m]
    bg = (R >= R_BG[0]) & (R < R_BG[1]); sig = mass[bg].sum() / (math.pi * (R_BG[1] ** 2 - R_BG[0] ** 2))
    return R, mass, sig, nfb
def mem_inside(R, mass, sig, Rs):
    return mass[(R >= 30) & (R < Rs)].sum() - sig * math.pi * (Rs ** 2 - 30 ** 2)

def system(d, Ml, Mg, R, mass, sig, rmode, sfac):
    if rmode != "iter":
        Rs = float(rmode); Mm = mem_inside(R, mass, sig, Rs)
        return dict(Rs=Rs, Mmem=Mm, Mb=Ml + sfac * Mm + Mg, conv=True, clip="fixed")
    Rc = 300.0; conv = False
    for _ in range(30):
        Mb = Ml + sfac * mem_inside(R, mass, sig, min(Rc, R_BG[1])) + Mg
        Rn = float(R200c_kpc((1 + XC) * Mb, d["z"])[0]) if Mb > 0 else 100.0
        if abs(Rn - Rc) < 0.1: Rc = Rn; conv = True; break
        Rc = Rn
    clip = "low" if Rc < 100 else ("high" if Rc > 600 else "none")
    Rs = min(max(Rc, 100.0), 600.0); Mm = mem_inside(R, mass, sig, Rs)
    return dict(Rs=Rs, Rraw=Rc, Mmem=Mm, Mb=Ml + sfac * Mm + Mg, conv=conv, clip=clip)

PRIMARY = dict(gas="G-MID", lens="corr", delta="norm", w=0.08, rmode="iter", nest="A", cfac=1.0, zs="inf", sfac=1.0)
BRACKETS = {"G-0": dict(gas="G-0"), "G-HI": dict(gas="G-HI"), "B-UNC": dict(lens="unc"), "B-RAW": dict(delta="raw"), "B-W05": dict(w=0.05),
            "B-W12": dict(w=0.12), "R300": dict(rmode=300.0), "R600": dict(rmode=600.0), "N-B": dict(nest="B"), "B-C07": dict(cfac=0.7),
            "B-C14": dict(cfac=1.4), "B-ZS2": dict(zs="zs2"), "B-STAR+": dict(sfac=1.4)}
_ML = {}; _DEL = {}

def run_kind(cfg, kind, zc_map=None):
    """per-lens system for every graded target of one kind under a configuration."""
    corr = cfg["lens"] == "corr"
    if corr not in _DEL: _DEL[corr] = delta_scale(corr)
    Delta = 0.0 if cfg["delta"] == "raw" else _DEL[corr][0]
    if cfg["w"] not in _ML: _ML[cfg["w"]] = ml_median(cfg["w"])
    ml = _ML[cfg["w"]]
    res = []
    for d in grad(kind):
        Ml = 10 ** lens_logm(d, corr) if kind in ("W", "C", "L") else 0.0
        Mg = GAS[cfg["gas"]][kind]
        zc = None if zc_map is None else zc_map[d["target"]]
        R, mass, sig, nfb = census(d, cfg["w"], Delta, ml, zc)
        s = system(d, Ml, Mg, R, mass, sig, cfg["rmode"], cfg["sfac"])
        s.update(target=d["target"], lens_id=d["lens_id"], z=d["z"], Ml=Ml, Mg=Mg, nfb=nfb, M300=mem_inside(R, mass, sig, 300.0), sig=sig,
                 nmem=int(((R >= 30) & (R < s["Rs"])).sum()))
        res.append(s)
    return res, Delta, ml

def amount(cfg, sysres, ft, x_share=XC, inject=False):
    """r = log10(M_obs / M_ref) per lens (lenses in S only), each treated as fast."""
    idx = np.array([SIDX[s["lens_id"]] for s in sysres]); z = Z[idx]
    Ml = np.array([s["Ml"] for s in sysres]); Mb = np.array([s["Mb"] for s in sysres]); Mg = np.array([s["Mg"] for s in sysres])
    zs = ZS_INF if cfg["zs"] == "inf" else np.maximum(2.0, z + 0.5)
    Mo = m_obs(idx, zs)
    if cfg["nest"] == "A": stars = Ml * MSUN * F2D[idx]; Mcold_shape = XC * Mb
    else: stars = m_law(Ml, A0[ft], idx); Mcold_shape = XC * (Mb - Ml)
    Mcold = (x_share / XC) * Mcold_shape
    shape_M = np.where(Mcold_shape > 0, Mcold_shape, np.where(Mg > 0, XC * Mg, 1e10))
    rs, rta = halo_shape(shape_M, z, cfg["cfac"]); fr = cyl_frac(idx, rs, rta)
    cold = np.where(Mcold_shape > 0, Mcold, 0.0) * MSUN * fr; gas = np.where(Mg > 0, Mg, 0.0) * MSUN * fr
    Mref = stars + cold + gas
    if inject: Mo = Mref.copy()
    miss = Mo - Ml * MSUN * F2D[idx]
    return dict(r=np.log10(Mo / Mref), Mo=Mo, Mref=Mref, halo=cold + gas, miss=miss, n_nonpos_halo=int((Mcold_shape <= 0).sum()))

def med_ci(v):
    v = np.asarray(v, float)
    if len(v) == 0: return dict(n=0, med=float("nan"), lo=float("nan"), hi=float("nan"))
    rng = np.random.default_rng(SEED); bs = np.median(v[rng.integers(0, len(v), (NBOOT, len(v)))], axis=1)
    return dict(n=int(len(v)), med=float(np.median(v)), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)))
def s_line(ci): return "FAST" if ci["lo"] >= 1 else ("SLOW" if ci["hi"] < 1 else "MIXED")
def a_line(ci):
    if ci["n"] == 0: return "NONE"
    if ci["lo"] > LINE: return "UNDER"
    if ci["hi"] < -LINE: return "OVER"
    return "FITS"
W1, W2, W3, W4 = "GROUPS TOO SLOW: ROW 40 FAILS", "HALO SHORT: ROW 40 FAILS", "WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES", "NO VERDICT"

def evaluate(cfgname, cfg, ft, zc_map=None, x_share=XC, inject=False, vfac=1.0):
    key = (cfgname, json.dumps(cfg, sort_keys=True), None if zc_map is None else "zs")
    if key not in _SYS: _SYS[key] = {k: run_kind(cfg, k, zc_map) for k in ("W", "C")}
    (sw, Delta, ml), (sc, _, _) = _SYS[key]["W"], _SYS[key]["C"]
    zw = np.array([s["z"] for s in sw]); zc_ = np.array([s["z"] for s in sc])
    s_w = vL_signed(np.array([s["Mb"] for s in sw]), zw) / vstar(ft, zw, vfac)
    s_c = vL_signed(np.array([s["Mb"] for s in sc]), zc_) / vstar(ft, zc_, vfac)
    aw = amount(cfg, sw, ft, x_share, inject); ac = amount(cfg, sc, ft, x_share, inject)
    S_ci = med_ci(s_w); A_ci = med_ci(aw["r"]); fast = s_w >= 1; cfast = s_c >= 1
    A_fast = med_ci(aw["r"][fast]); C_fast = med_ci(ac["r"][cfast])
    ctrl_met = True if cfast.sum() < 20 else (a_line(C_fast) == "FITS")
    sl, al = s_line(S_ci), a_line(A_ci)
    if sl == "SLOW": word = W1
    elif al == "UNDER": word = W2
    elif sl == "FAST" and al == "FITS" and ctrl_met: word = W3
    else: word = W4
    ok = aw["miss"] > 0
    return dict(config=cfgname, footing=ft, N_W=len(sw), N_C=len(sc), Delta=Delta, ml_H=ml, S=S_ci, S_line=sl, A=A_ci, A_line=al,
                frac_W_fast=float(np.mean(fast)), frac_C_fast=float(np.mean(cfast)), N_W_fast=int(fast.sum()), N_C_fast=int(cfast.sum()),
                A_on_W_fast=A_fast, C_fast_A=C_fast, control_condition_met=bool(ctrl_met), control_trivial=bool(cfast.sum() < 20), word=word,
                halo_over_missing_med=float(np.median(aw["halo"][ok] / aw["miss"][ok])) if ok.any() else float("nan"), n_missing_pos=int(ok.sum()),
                median_Mb_W=float(np.median([s["Mb"] for s in sw])), median_Mmem_W=float(np.median([s["Mmem"] for s in sw])),
                median_Mmem_C=float(np.median([s["Mmem"] for s in sc])), median_Rsys_W=float(np.median([s["Rs"] for s in sw])),
                clip_W=dict(low=sum(s.get("clip") == "low" for s in sw), high=sum(s.get("clip") == "high" for s in sw)),
                nonconv_W=sum(not s["conv"] for s in sw), nonpos_halo_W=aw["n_nonpos_halo"], fallback_mass_W=int(sum(s["nfb"] for s in sw)),
                Mb_nonpos_W=int(sum(s["Mb"] <= 0 for s in sw)),
                _sw=sw, _sc=sc, _s_w=s_w, _s_c=s_c, _aw=aw, _ac=ac)
_SYS = {}
def strip(R): return {k: v for k, v in R.items() if not k.startswith("_")}

# ============================================================ known answers
P("\n[known answers]")
KA = {}
iW = np.where(TE >= 1.7)[0]; LMC = LM0 + SHIFT
ln = {r["unique_identifier"]: r for r in csv.DictReader(open(LNJ1, newline=""))}
k1 = {}
for ft in FOOTS:
    s = vL_signed(10 ** LMC[iW], Z[iW]) / vstar(ft, Z[iW])
    col = "s_model_can" if ft == "canonical" else "s_model_alt"
    ref = np.array([float(ln[S[i]["id"]][col]) for i in iW])
    k1[ft] = dict(maxdiff=float(np.max(np.abs(s - ref))), n_fast=int((s >= 1).sum()))
ok1 = all(k1[f]["maxdiff"] <= 1e-4 for f in FOOTS) and k1["canonical"]["n_fast"] == 1 and k1["alt"]["n_fast"] == 0 and len(iW) == 316
KA["KA1"] = dict(value=k1, pass_=bool(ok1))
P(f"  KA-1 LNJ1 stars-only s: max |diff| {k1['canonical']['maxdiff']:.1e} / {k1['alt']['maxdiff']:.1e}; s >= 1: {k1['canonical']['n_fast']} / {k1['alt']['n_fast']} (1 / 0) -> {'PASS' if ok1 else 'FAIL'}")
lo_inf = np.log10(m_obs(iW, ZS_INF) / MSUN)
law_c = np.log10(m_law(10 ** LMC[iW], A0["canonical"], iW) / MSUN); law_a = np.log10(m_law(10 ** LMC[iW], A0["alt"], iW) / MSUN)
rs_, rta_ = halo_shape(XC * 10 ** LMC[iW], Z[iW]); joint = np.log10((10 ** LMC[iW] * MSUN * F2D[iW] + XC * 10 ** LMC[iW] * MSUN * cyl_frac(iW, rs_, rta_)) / MSUN)
k2 = {}
for nm, mine, col in (("obs_inf", lo_inf, "logM_obs_inf"), ("law_can", law_c, "logM_law_can"), ("law_alt", law_a, "logM_law_alt"), ("joint_can", joint, "logM_joint_X5.41_can")):
    k2[nm] = float(np.max(np.abs(mine - np.array([float(ln[S[i]["id"]][col]) for i in iW]))))
ok2 = all(v <= 1e-3 for v in k2.values()); KA["KA2"] = dict(value=k2, pass_=bool(ok2))
P(f"  KA-2 LNJ1 projections max |diff| dex: {', '.join(f'{k} {v:.1e}' for k, v in k2.items())} -> {'PASS' if ok2 else 'FAIL'}")
mism = [d["target"] for d in T if d["n_in"] != int(CNT6[d["target"]]["n_in"]) or d["n_bg"] != int(CNT6[d["target"]]["n_bg"])]
Wp = {d["pair"]: d for d in T if d["kind"] == "W" and d["pair"] >= 0}; Cp = {d["pair"]: d for d in T if d["kind"] == "C"}
keep = [i for i in sorted(Wp) if Wp[i]["n_bg"] >= THR and Cp[i]["n_bg"] >= THR]
Dp = np.array([(Wp[i]["n_in"] - AREA_RATIO * Wp[i]["n_bg"]) - (Cp[i]["n_in"] - AREA_RATIO * Cp[i]["n_bg"]) for i in keep])
ok3 = (not mism) and len(keep) == 242 and abs(np.median(Dp) - 3.59) <= 0.01
KA["KA3"] = dict(mismatches=len(mism), n_pairs=len(keep), median_D=float(np.median(Dp)), pass_=bool(ok3))
P(f"  KA-3 EUC6R counts: {len(T) - len(mism)} of {len(T)} targets exact; paired median W - C {np.median(Dp):+.2f} on {len(keep)} pairs (+3.59 on 242) -> {'PASS' if ok3 else 'FAIL'}")
v0 = {f: J.vstar0_kms(f) for f in FOOTS}; ok4 = abs(v0["canonical"] - 668.53) <= 0.01 and abs(v0["alt"] - 807.93) <= 0.01
KA["KA4"] = dict(value=v0, pass_=bool(ok4)); P(f"  KA-4 v*(0) {v0['canonical']:.2f} / {v0['alt']:.2f} km/s -> {'PASS' if ok4 else 'FAIL'}")
e8 = {r["unique_identifier"]: r for r in csv.DictReader(open(EUC8, newline=""))}
k5 = {}
for ft, col in (("canonical", "excess_far_canonical_Msun"), ("alt", "excess_far_alt_Msun")):
    mo = m_obs(iW, ZS_INF); lw = m_law(10 ** LM0[iW], A0_EUC[ft], iW); ex = np.where(mo > lw, mo - lw, 0.0) / MSUN
    ref = np.array([float(e8[S[i]["id"]][col]) for i in iW])
    rel = np.where((ref > 0) | (ex > 0), np.abs(ex - ref) / np.maximum(np.maximum(ref, ex), 1.0), 0.0)
    k5[ft] = dict(median_rel=float(np.median(rel)), p90_rel=float(np.percentile(rel, 90)), median_excess=float(np.median(ex)))
ok5 = all(k5[f]["median_rel"] <= 1e-3 for f in FOOTS) and all(S[i]["id"] in e8 for i in iW)
KA["KA5"] = dict(value=k5, pass_=bool(ok5))
P(f"  KA-5 EUC8 far excess: median rel diff {k5['canonical']['median_rel']:.1e} / {k5['alt']['median_rel']:.1e} (90th pct {k5['canonical']['p90_rel']:.1e} / {k5['alt']['p90_rel']:.1e}) -> {'PASS' if ok5 else 'FAIL'}")
k6 = {}
for k in "WC":
    a = [d for d in T if d["kind"] == k]; k6[k] = float(np.mean([d["mer_row"] is not None for d in a]))
ok6 = k6["W"] >= 0.90 and k6["C"] >= 0.90; KA["KA6"] = dict(value=k6, pass_=bool(ok6))
P(f"  KA-6 own MER object in cone with a photo-z row: W {k6['W']:.3f}, C {k6['C']:.3f} (>= 0.90 each) -> {'PASS' if ok6 else 'FAIL'}")
k7 = []
for M in (1e11, 1e13, 1e15):
    Rm = R200c_kpc(M, 0.5)[0] * KPC; a = math.sqrt(J.G * M * J.MSUN / Rm); b = (10 * J.G * M * J.MSUN * H_si(0.5)[0]) ** (1 / 3); k7.append(abs(a / b - 1))
ok7 = max(k7) <= 1e-9; KA["KA7"] = dict(value=k7, pass_=bool(ok7))
P(f"  KA-7 sqrt(G M / R_200c) vs (10 G M H)^(1/3): max rel {max(k7):.1e} -> {'PASS' if ok7 else 'FAIL'}")
KA_ALL = all(v["pass_"] for v in KA.values())
P(f"  known answers: {'all pass' if KA_ALL else 'FAILED -> NOT EVALUABLE'}")

# reported check (no gate): this lane's photo-z rows against the other build's untracked files, first 12 W cones present there
cmp = dict(cones=0, ids_both=0, ids_only_mine=0, ids_only_other=0, value_mismatch=0)
if os.path.isdir(PHZ_OTHER):
    for d in [d for d in T if d["kind"] == "W"][:40]:
        fn = os.path.join(PHZ_OTHER, d["target"].replace(":", "_") + ".csv.gz")
        if not os.path.exists(fn) or cmp["cones"] >= 12: continue
        oth = {int(r["object_id"]): r for r in csv.DictReader(io.StringIO(gzip.open(fn).read().decode()))}
        body = gzip.open(os.path.join(CONES, MAN6[d["target"]]["file"])).read()
        mine_ids = set()
        for o in csv.DictReader(io.StringIO(body.decode())):
            if (fl(o["flux_h_templfit"]) > FLUX_CUT and fl(o["spurious_flag"]) == 0 and fl(o["det_quality_flag"]) < DQF_CUT and fl(o["point_like_prob"]) < PLP_CUT
                    and int(o["object_id"]) in PHROW): mine_ids.add(int(o["object_id"]))
        both = mine_ids & set(oth); cmp["cones"] += 1; cmp["ids_both"] += len(both)
        cmp["ids_only_mine"] += len(mine_ids - set(oth)); cmp["ids_only_other"] += len(set(oth) - mine_ids)
        for k in both:
            a, b = PHROW[k], oth[k]
            for c in ("phz_median", "phz_classification", "phz_pp_median_stellarmass", "phz_pp_median_redshift"):
                x, y = fl(a[c]), fl(b[c])
                if not ((np.isnan(x) and np.isnan(y)) or abs(x - y) <= 1e-6 * max(1, abs(x))): cmp["value_mismatch"] += 1; break
P(f"  reported: rows against the other build's untracked photo-z files ({cmp['cones']} W cones): ids in both {cmp['ids_both']}, only here {cmp['ids_only_mine']}, "
  f"only there {cmp['ids_only_other']}, value mismatches {cmp['value_mismatch']}")

# ============================================================ instrument checks (primary window and scale)
P("\n[instrument checks]")
cfgP = dict(PRIMARY)
sysR, DeltaP, mlP = run_kind(cfgP, "R"); sysL, _, _ = run_kind(cfgP, "L")
evP = {ft: evaluate("primary", cfgP, ft) for ft in FOOTS}
M300_W = np.array([s["M300"] for s in evP["canonical"]["_sw"]]); M300_C = np.array([s["M300"] for s in evP["canonical"]["_sc"]])
M300_R = np.array([s["M300"] for s in sysR]); M300_L = np.array([s["M300"] for s in sysL])
n1 = dict(n=len(M300_R), median=float(np.median(M300_R))); n1["pass_"] = bool(abs(n1["median"]) <= 1.0e11)
rng = np.random.default_rng(SEED)
bs = np.median(M300_L[rng.integers(0, len(M300_L), (NBOOT, len(M300_L)))], axis=1) - np.median(M300_C[rng.integers(0, len(M300_C), (NBOOT, len(M300_C)))], axis=1)
n2 = dict(n_L=len(M300_L), n_C=len(M300_C), diff=float(np.median(M300_L) - np.median(M300_C)), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)))
n2["pass_"] = bool(n2["lo"] > 0)
P(f"  Delta (members to lens scale) {DeltaP:+.4f} dex from {_DEL[True][1]} lenses; median log(M/L_H) {mlP:.4f} (arbitrary units); B-UNC Delta {delta_scale(False)[0]:+.4f}")
P(f"  N1 blank fields: {n1['n']} graded, median net member mass inside 300 kpc {n1['median']:+.3e} Msun (|.| <= 1e11) -> {'PASS' if n1['pass_'] else 'FAIL'}")
P(f"  N2 L minus C inside 300 kpc: {n2['diff']:+.3e} [{n2['lo']:+.3e}, {n2['hi']:+.3e}] Msun (L {n2['n_L']}, C {n2['n_C']}; lower bound > 0) -> {'PASS' if n2['pass_'] else 'FAIL'}")
P(f"  reported: median net member mass inside 300 kpc: W {np.median(M300_W):+.3e}, C {np.median(M300_C):+.3e}, L {np.median(M300_L):+.3e} Msun")
INSTR = n1["pass_"] and n2["pass_"]

# ============================================================ twins (gates computed in-process)
Wg = grad("W"); rngz = np.random.default_rng(SEED); perm = rngz.permutation(len(Wg))
for i in range(len(perm)):
    if perm[i] == i: j = (i + 1) % len(perm); perm[i], perm[j] = perm[j], perm[i]
ZMAP = {Wg[i]["target"]: Wg[perm[i]]["z"] for i in range(len(Wg))}
for d in grad("C"): ZMAP[d["target"]] = d["z"]
twZS = evaluate("TW-ZS", cfgP, "canonical", zc_map=ZMAP)
M300_ZS = np.array([s["M300"] for s in twZS["_sw"]])
zs_bite = bool(np.median(M300_W) > 0 and np.median(M300_ZS) <= 0.5 * np.median(M300_W))
twINJ = {ft: evaluate("primary", cfgP, ft, inject=True) for ft in FOOTS}; inj_bite = all(twINJ[f]["A_line"] == "FITS" for f in FOOTS)
twX0 = {ft: evaluate("primary", cfgP, ft, x_share=0.0) for ft in FOOTS}; x0_bite = all(twX0[f]["A_line"] == "UNDER" for f in FOOTS)
TW_OK = zs_bite and inj_bite and x0_bite
P(f"  TW-ZS: W median net member mass inside 300 kpc {np.median(M300_W):+.3e} -> {np.median(M300_ZS):+.3e} (must fall to <= half) -> {'bites' if zs_bite else 'DOES NOT BITE'}")
P(f"  TW-INJ: (A) {twINJ['canonical']['A_line']} / {twINJ['alt']['A_line']} (must be FITS) -> {'bites' if inj_bite else 'DOES NOT BITE'}")
P(f"  TW-X0: (A) median r {twX0['canonical']['A']['med']:+.3f} [{twX0['canonical']['A']['lo']:+.3f}, {twX0['canonical']['A']['hi']:+.3f}] -> {twX0['canonical']['A_line']} / {twX0['alt']['A_line']} (must be UNDER) -> {'bites' if x0_bite else 'DOES NOT BITE'}")

if MUT:
    tw = dict(ZS=dict(canonical=twZS), INJ=twINJ, X0=twX0)[MUT]
    rep = dict(lane="WLG1R", twin=MUT, note="twin output; exits 1. Adopts nothing. kappa = 1/2 FITTED; not theory closed.",
               bites=dict(ZS=zs_bite, INJ=inj_bite, X0=x0_bite)[MUT], foot={f: strip(v) for f, v in tw.items()})
    if MUT == "ZS": rep.update(M300_W_main=float(np.median(M300_W)), M300_W_twin=float(np.median(M300_ZS)), permutation_fixed_points=int(sum(perm == np.arange(len(perm)))))
    json.dump(rep, open(os.path.join(HERE, f"wlg1r_MUTATE_{MUT}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"wlg1r_MUTATE_{MUT}.out"), "w").write("\n".join(OUT) + f"\nTWIN {MUT}: {'bites' if rep['bites'] else 'DOES NOT BITE'}; exit 1.\n"
                                                                    "Adopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
    sys.exit(1)

# ============================================================ configurations
P("\n[configurations: word per footing; (S) median s [95 %]; (A) median r [95 %] on every graded W lens as if fast]")
RES = dict(lane="WLG1R", criteria="8a730ebaa1", brief="ec7fed6252", note="TEST lane, blind, POST HOC; adopts nothing; kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed",
           footings=A0, known_answers=KA, instrument=dict(N1=n1, N2=n2), twins=dict(ZS=zs_bite, INJ=inj_bite, X0=x0_bite), phz_compare=cmp,
           edge=dict(reference=ref_bg, threshold=THR), foot={})
ALLCFG = {"primary": cfgP}
for b, ov in BRACKETS.items(): c = dict(PRIMARY); c.update(ov); ALLCFG[b] = c
EV = {ft: {} for ft in FOOTS}
for ft in FOOTS:
    for name, c in ALLCFG.items():
        r = evaluate(name, c, ft); EV[ft][name] = r
        P(f"[{ft}] {name:8s} N_W {r['N_W']} | s {r['S']['med']:.3f} [{r['S']['lo']:.3f}, {r['S']['hi']:.3f}] {r['S_line']} (W fast {r['frac_W_fast']:.3f}, C fast {r['frac_C_fast']:.3f} N {r['N_C_fast']}) | "
          f"r {r['A']['med']:+.3f} [{r['A']['lo']:+.3f}, {r['A']['hi']:+.3f}] {r['A_line']} (on W fast: {r['A_on_W_fast']['med']:+.3f}, n {r['A_on_W_fast']['n']}) | "
          f"ctrl {'met' + (' (trivially)' if r['control_trivial'] else '') if r['control_condition_met'] else 'FAILED'} | {r['word']}")
    prim = EV[ft]["primary"]["word"]; flips = [b for b in BRACKETS if EV[ft][b]["word"] != prim]
    nW = EV[ft]["primary"]["N_W"]
    gate = KA_ALL and INSTR and TW_OK and nW >= 150
    final = (prim + (", FRAGILE" if flips else "") + ", BLIND") if gate else "NOT EVALUABLE, BLIND"
    p = EV[ft]["primary"]
    for tf, nm in ((0.5, "TW-H"), (2.0, "TW-D")):
        t = evaluate("primary", cfgP, ft, vfac=tf); RES.setdefault("reported_twins", {}).setdefault(ft, {})[nm] = dict(S=t["S"], S_line=t["S_line"], frac_W_fast=t["frac_W_fast"])
        P(f"[{ft}] {nm} (reported): s {t['S']['med']:.3f} [{t['S']['lo']:.3f}, {t['S']['hi']:.3f}] {t['S_line']}, W fast {t['frac_W_fast']:.3f}")
    P(f"[{ft}] primary: Delta {p['Delta']:+.3f}; median M_b(W) {p['median_Mb_W']:.3e}; median M*_mem W {p['median_Mmem_W']:.3e}, C {p['median_Mmem_C']:.3e}; median R_sys(W) {p['median_Rsys_W']:.0f} kpc; "
      f"clipped low/high {p['clip_W']['low']}/{p['clip_W']['high']}; non-converged {p['nonconv_W']}; M_b <= 0 {p['Mb_nonpos_W']}; non-positive halo {p['nonpos_halo_W']}; H-band fallback members {p['fallback_mass_W']}; "
      f"halo terms / missing mass (median) {p['halo_over_missing_med']:.3f} on {p['n_missing_pos']}; EUC8 law excess median (KA-5 route) {k5[ft]['median_excess']:.3e}")
    RES["foot"][ft] = dict(word=final, primary_word=prim, flips=flips, bracket_words={b: EV[ft][b]["word"] for b in BRACKETS},
                           configs={k: strip(v) for k, v in EV[ft].items()}, gates=dict(KA=KA_ALL, instrument=INSTR, twins=TW_OK, N_W=nW))
    P(f"[{ft}] WORD: {final}   (flips: {flips if flips else 'none'})")
P("\nWLG1R: " + " / ".join(RES["foot"][f]["word"] for f in FOOTS) + " (canonical / alt)")

# ============================================================ per-lens table (primary configuration)
with open(os.path.join(HERE, "wlg1r_per_lens.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["unique_identifier", "kind", "z_l", "theta_E_arcsec", "log_Mstar_lens", "Mgas_Msun", "Mmem_net_Msun", "Mmem_300_Msun", "n_members", "R_sys_kpc",
                "R_sys_raw_kpc", "converged", "clip", "Mb_Msun", "s_can", "s_alt", "logM_obs_inf", "logM_ref_NA", "r_NA", "halo_over_missing"])
    for kind, sk, ak in (("W", "_sw", "_aw"), ("C", "_sc", "_ac")):
        pc, pa = EV["canonical"]["primary"], EV["alt"]["primary"]; sl = pc[sk]; a = pc[ak]
        s_can = pc["_s_w" if kind == "W" else "_s_c"]; s_alt = pa["_s_w" if kind == "W" else "_s_c"]
        for j, s in enumerate(sl):
            i = SIDX[s["lens_id"]]
            w.writerow([s["lens_id"], kind, "%.4f" % s["z"], "%.4f" % TE[i], "%.4f" % math.log10(s["Ml"]), "%.3e" % s["Mg"], "%.4e" % s["Mmem"], "%.4e" % s["M300"], s["nmem"],
                        "%.1f" % s["Rs"], "%.1f" % s.get("Rraw", float("nan")), int(s["conv"]), s["clip"], "%.4e" % s["Mb"], "%.4f" % s_can[j], "%.4f" % s_alt[j],
                        "%.4f" % math.log10(a["Mo"][j] / MSUN), "%.4f" % math.log10(a["Mref"][j] / MSUN), "%.4f" % a["r"][j],
                        "%.4f" % (a["halo"][j] / a["miss"][j]) if a["miss"][j] > 0 else "nan"])
json.dump(RES, open(os.path.join(HERE, "wlg1r.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wlg1r.out"), "w").write("\n".join(OUT) + f"\n(elapsed {time.time() - T0:.0f} s)\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
P(f"(elapsed {time.time() - T0:.0f} s)")
