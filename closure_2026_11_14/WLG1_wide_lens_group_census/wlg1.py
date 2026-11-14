#!/usr/bin/env python3
"""WLG1: are Euclid's wide lenses fast groups? (FROZEN_CRITERIA.md, commit 8ca77a609e). TEST lane; adopts nothing.

Owners' code imported read-only: EUC1's euc1.py (cosmology, Sersic, law S, quadrature) and JNT2's jnt2_common.py (v*,
v_L). FRZ1's halo and LNJ1's cylinder projection are copied from LNJ1's lnj1.py (checked by KA-2).
Inputs: ECLIPSE catalogues, EUC6R's cones and tables, EUC17's mask fractions, LNJ1's and EUC8's per-lens tables, and
this lane's photo-z / physical-parameter files (_external_data/wlg1_phz_by_id/, from wlg1_fetch.py).

Run:  nice -n 19 python3 -I wlg1.py            (main; writes wlg1.out / wlg1.json / wlg1_per_lens.csv)
      WLG1_MUTATE=ZS  nice -n 19 python3 -I wlg1.py   (photo-z shuffle twin; separate outputs; exit 1)
      WLG1_MUTATE=INJ nice -n 19 python3 -I wlg1.py   (amount injection twin; separate outputs; exit 1)
Footings never pooled. kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, csv, io, gzip, json, math, hashlib, time, warnings, importlib.util
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
def load_mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E = load_mod("euc1_ro", os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling", "euc1.py"))
J = load_mod("jnt2_common_ro", os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_common.py"))
DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
CONES = os.path.join(REPO, "_external_data", "euclid_dr1_mer_cones_euc6r")
PHZ = os.path.join(REPO, "_external_data", "wlg1_phz_by_id")
R6 = os.path.join(REPO, "closure_2026_11_12", "EUC6R_blind_regrade")
EUC17 = os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_per_lens.csv")
LNJ1 = os.path.join(REPO, "closure_2026_11_13", "LNJ1_joint_switch_on_euclid_lenses", "lnj1_per_lens.csv")
EUC8 = os.path.join(REPO, "closure_2026_11_12", "EUC8_wide_lens_residual_profile", "euc8_wide_per_lens.csv")

MUT = os.environ.get("WLG1_MUTATE", "")
TAG = "" if not MUT else "_MUTATE_" + MUT
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

# ------------------------------------------------------------------ constants (frozen)
G, MSUN, PC, KPC, ARCSEC = E.G, E.MSUN, E.PC, E.KPC, E.ARCSEC
MPC_M = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
XC = 5.41
SHIFT_COMMON = 0.036
SEED = 20261114; NBOOT = 2000
FLUX_CUT, PLP_CUT, DQF_CUT = 5.75, 0.7, 4
R_IN0 = 30.0; R_BG = (600.0, 1000.0); R_CLIP = (100.0, 600.0)
W_PRIMARY = 0.08
GAS = {"MID": {"W": 5.2e12, "C": 0.0}, "0": {"W": 0.0, "C": 0.0}, "HI": {"W": 8.3e12, "C": 3.0e12}}
EDGE_FRAC = 0.40; COVER_MIN = 0.80
LINE = 0.10
W_SLOW = "GROUPS TOO SLOW: ROW 40 FAILS"
W_SHORT = "HALO SHORT: ROW 40 FAILS"
W_PASS = "WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES"
W_NV = "NO VERDICT"; W_NE = "NOT EVALUABLE"
GLX, GLW = E.GLX, E.GLW
P("WLG1: group census around Euclid's wide lenses, scorecard row 40 (criteria 8ca77a609e). TEST lane; POST HOC; adopts nothing.")
P("kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Footings canonical a0 9.3603e-11 / alt 1.1312e-10, never pooled.")
if MUT: P(f"*** MUTATION RUN: {MUT} (separate outputs; exits 1) ***")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()
def fl(v):
    try: return float(v)
    except Exception: return float("nan")

# ------------------------------------------------------------------ ECLIPSE (LNJ1's loader)
for fn, hx in E.SHA.items():
    ok = sha256(os.path.join(DATA, fn)) == hx
    P(f"  sha256 {fn}: {'matches EUC1 frozen hash' if ok else 'MISMATCH'}")
    if not ok: sys.exit("data hash mismatch")
obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(os.path.join(DATA, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8"))}
ROWS = {}
for r in csv.DictReader(open(os.path.join(DATA, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8")):
    o = obj.get(r["unique_identifier"])
    if o is None: continue
    ROWS[r["unique_identifier"]] = dict(id=r["unique_identifier"], grade=r["lens_grade"].strip(), success=r["lens_model_success"].strip() == "True",
        final=r["final_sample"].strip() == "True", large=o["large_system_warning"].strip() == "True",
        z=fl(r["eclipse_median_phz"]), lm=fl(r["eclipse_log_survived_mass_med"]), tE=fl(r["eclipse_effective_einstein_radius"]),
        te=fl(r["eclipse_effective_radius"]), n=fl(r["eclipse_sersic_index"]), mer=o["MER_object_id"].strip())
def in_S(r):
    return (r["grade"] in ("A", "B") and r["success"] and r["final"] and not r["large"] and r["tE"] > 0 and r["te"] > 0
            and 0.6 <= r["n"] <= 10.0 and r["z"] > 0 and r["lm"] > 0)
S_ids = [k for k, r in ROWS.items() if in_S(r)]
W_ids = sorted(k for k in S_ids if ROWS[k]["tE"] >= 1.7)
P(f"  sample S {len(S_ids)}; W (theta_E >= 1.7\") {len(W_ids)}")

F17 = {}
for r in csv.DictReader(open(EUC17, newline="")):
    if r["row"] in ("P", "W_B"): F17[r["unique_identifier"]] = float(r["log10_f"])

# ------------------------------------------------------------------ EUC6R targets, counts, manifest
TG = list(csv.DictReader(open(os.path.join(R6, "euc6r_targets.csv"), newline="")))
CN = {r["target"]: r for r in csv.DictReader(open(os.path.join(R6, "euc6r_counts.csv"), newline=""))}
M6 = {r["target"]: r for r in csv.DictReader(open(os.path.join(R6, "euc6r_manifest.csv"), newline=""))}
MANW = {r["target"]: r for r in csv.DictReader(open(os.path.join(HERE, "wlg1_fetch_manifest.csv"), newline=""))}
P(f"  EUC6R targets {len(TG)} (W {sum(t['kind']=='W' for t in TG)}, C {sum(t['kind']=='C' for t in TG)}, L {sum(t['kind']=='L' for t in TG)}, R {sum(t['kind']=='R' for t in TG)}); photo-z files {len(MANW)}")

# EUC6R's distances (H0 67.74, Om 0.3089, quad) for the projected radii, so KA-3 is exact
H0E, OME, CKMS = 67.74, 0.3089, 299792.458
def d_a_mpc(z):
    v, _ = quad(lambda x: 1.0 / math.sqrt(OME * (1 + x) ** 3 + 1 - OME), 0.0, z, limit=500, epsabs=0, epsrel=1e-10)
    return CKMS / H0E * v / (1 + z)
def sep_rad(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    a = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
def DL_rel(z):  # luminosity distance (catalogue cosmology), metres
    return E.EUCLID.DL(z)

# ------------------------------------------------------------------ read cones + photo-z
def read_target(t):
    raw = open(os.path.join(CONES, M6[t["target"]]["file"]), "rb").read()
    rows = list(csv.DictReader(io.StringIO(gzip.decompress(raw).decode())))
    oid = np.array([int(o["object_id"]) for o in rows], dtype=np.int64)
    ra = np.array([fl(o["right_ascension"]) for o in rows]); de = np.array([fl(o["declination"]) for o in rows])
    fx = np.array([fl(o["flux_h_templfit"]) for o in rows]); sp = np.array([fl(o["spurious_flag"]) for o in rows])
    dq = np.array([fl(o["det_quality_flag"]) for o in rows]); pl = np.array([fl(o["point_like_prob"]) for o in rows])
    ok = (fx > FLUX_CUT) & (sp == 0) & (dq < DQF_CUT) & (pl < PLP_CUT)
    z = float(t["z"]); kpr = d_a_mpc(z) * 1000.0
    R = sep_rad(float(t["ra"]), float(t["dec"]), ra, de) * kpr
    ph = {}
    mw = MANW.get(t["target"])
    if mw is not None:
        for o in csv.DictReader(io.StringIO(gzip.decompress(open(os.path.join(PHZ, mw["file"]), "rb").read()).decode())):
            ph[int(o["object_id"])] = o
    return dict(oid=oid, R=R, ok=ok, fx=fx, ph=ph, z=z, ra=ra, de=de)

TD = {}
for t in TG:
    TD[t["target"]] = read_target(t)
P(f"  cones read ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ KA-3: EUC6R's counts and paired richness
AREA_RATIO = (300.0 ** 2 - 30.0 ** 2) / (R_BG[1] ** 2 - R_BG[0] ** 2)
KA = {}
mism = 0; NBG = {}
for t in TG:
    d = TD[t["target"]]
    n_in = int(((d["R"] >= 30) & (d["R"] < 300) & d["ok"]).sum()); n_bg = int(((d["R"] >= 600) & (d["R"] < 1000) & d["ok"]).sum())
    NBG[t["target"]] = n_bg
    c = CN[t["target"]]
    if n_in != int(c["n_in"]) or n_bg != int(c["n_bg"]): mism += 1
ref_bg = float(np.median([NBG[t["target"]] for t in TG if t["kind"] in ("W", "C", "L")]))
def edge_ok(key): return NBG[key] >= EDGE_FRAC * ref_bg
pairs = {}
for t in TG:
    if t["kind"] in ("W", "C") and int(t["pair"]) >= 0: pairs.setdefault(int(t["pair"]), {})[t["kind"]] = t["target"]
Dl = []
for p in sorted(pairs):
    q = pairs[p]
    if "W" in q and "C" in q and edge_ok(q["W"]) and edge_ok(q["C"]):
        dW = float(CN[q["W"]]["n_in"]) - AREA_RATIO * NBG[q["W"]]
        dC = float(CN[q["C"]]["n_in"]) - AREA_RATIO * NBG[q["C"]]
        dWm = int(((TD[q["W"]]["R"] >= 30) & (TD[q["W"]]["R"] < 300) & TD[q["W"]]["ok"]).sum()) - AREA_RATIO * NBG[q["W"]]
        dCm = int(((TD[q["C"]]["R"] >= 30) & (TD[q["C"]]["R"] < 300) & TD[q["C"]]["ok"]).sum()) - AREA_RATIO * NBG[q["C"]]
        Dl.append(dWm - dCm)
KA["KA-3"] = dict(count_mismatches=mism, pairs=len(Dl), median_D=float(np.median(Dl)),
                  pass_=bool(mism == 0 and len(Dl) == 242 and abs(np.median(Dl) - 3.59) <= 0.01))
P(f"KA-3 EUC6R counts: {mism} target mismatches of {len(TG)}; pairs {len(Dl)}; median D {np.median(Dl):+.3f} (target +3.59 on 242): {'pass' if KA['KA-3']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ lens geometry, law S, FRZ1 halo (LNJ1's code)
class Lenses:
    def __init__(self, ids):
        self.ids = ids
        self.z = np.array([ROWS[k]["z"] for k in ids]); self.lm = np.array([ROWS[k]["lm"] for k in ids])
        self.tE = np.array([ROWS[k]["tE"] for k in ids]); te = np.array([ROWS[k]["te"] for k in ids]); n = np.array([ROWS[k]["n"] for k in ids])
        DA = E.EUCLID.DA(self.z); self.RE = self.tE * ARCSEC * DA; REFF = te * ARCSEC * DA
        U = np.arccosh(np.maximum(1.0e6 * KPC / self.RE, 1.0 + 1e-9))
        self.RN = self.RE[:, None] * np.cosh(GLX[None, :] * U[:, None]); self.PREF = self.RE ** 2 / G * U
        self.GN1 = G * MSUN * E.M3D_frac(self.RN, REFF[:, None], n[:, None]) / self.RN ** 2
        self.F2D = E.M2D_frac(self.RE, REFF, n)
        self.EZ = np.array([J.E(z) for z in self.z])
    def M2D_g(self, g): return self.PREF * np.sum(GLW[None, :] * g, axis=1) / MSUN   # Msun (run-1 fix: was kg)
    def m_law(self, Ms, a0): return self.M2D_g(E.g_law(Ms[:, None] * self.GN1, a0, "S"))
    def m_obs(self, zs): return math.pi * self.RE ** 2 * E.EUCLID.sigcr(self.z, zs) / MSUN   # Msun (run-1 fix: was kg)
    def c_cyl(self, Mc_sun, rs, rta):
        r = np.minimum(self.RN, rta[:, None]); Cr = (Mc_sun * MSUN)[:, None] * m_nfw(r / rs[:, None]) / m_nfw(rta / rs)[:, None]
        return self.M2D_g(G * Cr / self.RN ** 2)

hh = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / hh ** 2; FB = om_b / (om_b + om_c); RHO_M = Om * 2.77536627e11
m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def Omz(z): return Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om)
def conc_fn(z, cfac=1.0): return lambda M: cfac * 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
def halo_basics_z(M, conc, dta, omz):
    c = conc(M); r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-12)
    return dict(rs=r2 / c, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc)
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
def halo_interp(X, Mb_sun, z, cfac=1.0):
    lmta, lrs, lrta = halo_table(cfac)
    t = np.log10(X * np.maximum(Mb_sun, 1.0) * hh / (1 - FB)); zi = np.clip(np.searchsorted(ZG, z) - 1, 0, len(ZG) - 2); w = (z - ZG[zi]) / (ZG[zi + 1] - ZG[zi])
    out = []
    for arr in (lrs, lrta):
        v0 = np.array([np.interp(t[k], lmta[zi[k]], arr[zi[k]]) for k in range(len(t))])
        v1 = np.array([np.interp(t[k], lmta[zi[k] + 1], arr[zi[k] + 1]) for k in range(len(t))])
        out.append(10 ** ((1 - w) * v0 + w * v1))
    return out[0], out[1]

LW = Lenses(W_ids)
C_ids = [t["lens_id"] for t in TG if t["kind"] == "C"]
LC = Lenses(C_ids)
for cf in (1.0, 0.7, 1.4): halo_table(cf)
P(f"  halo tables built ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ KA-1, KA-2, KA-4, KA-5, KA-7
LN = {r["unique_identifier"]: r for r in csv.DictReader(open(LNJ1, newline=""))}
lmc = LW.lm + SHIFT_COMMON
s1 = {ft: np.array([J.vL_kms(10 ** lmc[i], LW.z[i]) / J.vstar_kms(ft, LW.z[i]) for i in range(len(W_ids))]) for ft in FOOTS}
d1 = max(max(abs(s1["canonical"][i] - float(LN[k]["s_model_can"])), abs(s1["alt"][i] - float(LN[k]["s_model_alt"]))) for i, k in enumerate(W_ids))
n1 = (int((s1["canonical"] >= 1).sum()), int((s1["alt"] >= 1).sum()))
KA["KA-1"] = dict(max_diff=d1, above=n1, pass_=bool(d1 <= 1e-4 and n1 == (1, 0)))
P(f"KA-1 lens stars only: max |s - LNJ1| {d1:.2e}; above v* {n1[0]} / {n1[1]} (target 1 / 0): {'pass' if KA['KA-1']['pass_'] else 'FAIL'}")
mo = LW.m_obs(E.ZS_INF); Ms = 10 ** lmc
ml = {ft: LW.m_law(Ms, A0[ft]) for ft in FOOTS}
rs, rta = halo_interp(XC, Ms, LW.z, 1.0); mj = Ms * LW.F2D + LW.c_cyl(XC * Ms, rs, rta)
d2 = 0.0
for i, k in enumerate(W_ids):
    r = LN[k]
    for a, b in ((np.log10(mo[i]), "logM_obs_inf"), (np.log10(ml["canonical"][i]), "logM_law_can"), (np.log10(ml["alt"][i]), "logM_law_alt"), (np.log10(mj[i]), "logM_joint_X5.41_can")):
        if r[b] not in ("", "nan"): d2 = max(d2, abs(a - float(r[b])))
KA["KA-2"] = dict(max_diff_dex=d2, pass_=bool(d2 <= 1e-3))
P(f"KA-2 LNJ1 projections (obs, law can/alt, joint X 5.41) on W: max diff {d2:.2e} dex: {'pass' if KA['KA-2']['pass_'] else 'FAIL'}")
v0 = (J.vstar0_kms("canonical"), J.vstar0_kms("alt"))
KA["KA-4"] = dict(v=v0, pass_=bool(abs(v0[0] - 668.53) <= 0.01 and abs(v0[1] - 807.93) <= 0.01))
P(f"KA-4 v*(0) {v0[0]:.2f} / {v0[1]:.2f}: {'pass' if KA['KA-4']['pass_'] else 'FAIL'}")
E8 = {r["unique_identifier"]: r for r in csv.DictReader(open(EUC8, newline=""))}
rel = []
for ft, col in (("canonical", "excess_far_canonical_Msun"), ("alt", "excess_far_alt_Msun")):
    ex = mo - LW.m_law(10 ** LW.lm, E.FOOT[ft])
    for i, k in enumerate(W_ids):
        rel.append(abs(ex[i] / float(E8[k][col]) - 1))
KA["KA-5"] = dict(median_rel=float(np.median(rel)), max_rel=float(np.max(rel)), pass_=bool(np.median(rel) <= 1e-3))
P(f"KA-5 EUC8 far excess per lens: median rel diff {np.median(rel):.2e} (max {np.max(rel):.2e}): {'pass' if KA['KA-5']['pass_'] else 'FAIL'}")
def R200c_kpc(Mtot_sun, z): return (G * Mtot_sun * MSUN / (100 * (J.H0 * J.E(z)) ** 2)) ** (1 / 3) / KPC
k7 = max(abs(math.sqrt(G * M * MSUN / (R200c_kpc(M, z) * KPC)) / 1e3 / ((10 * G * M * MSUN * J.H0 * J.E(z)) ** (1 / 3) / 1e3) - 1) for M, z in ((1e12, 0.3), (3e13, 0.6), (1e14, 1.0)))
KA["KA-7"] = dict(max_rel=k7, pass_=bool(k7 <= 1e-9))
P(f"KA-7 virial definition: max rel {k7:.1e}: {'pass' if KA['KA-7']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ lens masses, PP calibration (Delta), member tables
TGW = {t["lens_id"]: t["target"] for t in TG if t["kind"] == "W"}
def lens_logm(k, corrected=True):
    return ROWS[k]["lm"] + SHIFT_COMMON - (F17.get(k, 0.0) if corrected else 0.0)
def pp_logm_at(o, zl):
    m = fl(o["phz_pp_median_stellarmass"]); zp = fl(o["phz_pp_median_redshift"])
    if not (math.isfinite(zp) and zp > 0): zp = fl(o["phz_median"])
    if not (math.isfinite(m) and m > 0 and math.isfinite(zp) and zp > 0): return float("nan")
    return m + 2 * math.log10(DL_rel(zl) / DL_rel(zp))
# KA-6 and Delta
have = 0; tot = 0; dcor, dunc = [], []
for t in TG:
    if t["kind"] not in ("W", "C"): continue
    k = t["lens_id"]; tot += 1; mer = ROWS[k]["mer"]; d = TD[t["target"]]
    o = d["ph"].get(int(mer)) if mer else None
    if o is not None:
        have += 1
        v = pp_logm_at(o, d["z"])
        if math.isfinite(v): dcor.append(lens_logm(k, True) - v); dunc.append(lens_logm(k, False) - v)
KA["KA-6"] = dict(found=have, of=tot, frac=have / tot, pass_=bool(have / tot >= 0.90))
P(f"KA-6 lens MER objects with a photo-z row: {have} / {tot} = {have / tot:.3f}: {'pass' if KA['KA-6']['pass_'] else 'FAIL'}")
DELTA = {"cor": float(np.median(dcor)), "unc": float(np.median(dunc)), "raw": 0.0}
P(f"  scale Delta (lens primary - lens PP at z_l): {DELTA['cor']:+.3f} dex (N {len(dcor)}, 16-84 % {np.percentile(dcor,16):+.3f} to {np.percentile(dcor,84):+.3f}); "
  f"against uncorrected lens masses {DELTA['unc']:+.3f}")

# lane-wide M/L_H for objects without a PP mass (window members, primary window, class 2)
def obj_table(key, zc, w):
    """members candidates: arrays R, logM_PP at z_l (nan if none), logflux, in-window & class-2 & cut & not lens."""
    d = TD[key]; t = TGI[key]
    lensmer = ROWS[t["lens_id"]]["mer"] if t["kind"] in ("W", "C", "L") else ""
    lensid = int(lensmer) if lensmer else None
    idx = np.where(d["ok"])[0]
    Rk, lm, lf, inwin, has = [], [], [], [], []
    ncut = len(idx); nph = 0
    for i in idx:
        o = d["ph"].get(int(d["oid"][i]))
        if o is None: continue
        nph += 1
        if lensid is not None and int(d["oid"][i]) == lensid: continue
        try: cls = int(float(o["phz_classification"]))
        except Exception: cls = -1
        zp = fl(o["phz_median"])
        if cls != 2 or not math.isfinite(zp): continue
        if abs(zp - zc) > w * (1 + zc): continue
        Rk.append(d["R"][i]); lm.append(pp_logm_at(o, d["z"])); lf.append(math.log10(d["fx"][i]))
    return dict(R=np.array(Rk), lm=np.array(lm), lf=np.array(lf), ncut=ncut, nph=nph)
TGI = {t["target"]: t for t in TG}
_ml = []
for t in TG:
    ot = obj_table(t["target"], TD[t["target"]]["z"], W_PRIMARY)
    g = np.isfinite(ot["lm"])
    if g.any(): _ml.extend(list(ot["lm"][g] - ot["lf"][g] - 2 * math.log10(DL_rel(TD[t["target"]]["z"]))))
KML = float(np.median(_ml))
P(f"  fallback log(M/L_H) constant from {len(_ml)} window members: {KML:.4f}")
def member_masses(ot, zl, delta):
    lm = ot["lm"].copy(); bad = ~np.isfinite(lm)
    lm[bad] = ot["lf"][bad] + 2 * math.log10(DL_rel(zl)) + KML
    return 10 ** (lm + delta), int(bad.sum())

CACHE = {}
def members(key, w, delta_key, zshift=None):
    """net member stellar mass function M_mem(R) for one target: returns (callable, info)."""
    zl = TD[key]["z"]; zc = zl if zshift is None else zshift
    ck = (key, w, delta_key, zc)
    if ck in CACHE: return CACHE[ck]
    ot = obj_table(key, zc, w)
    m, nfb = member_masses(ot, zl, DELTA[delta_key]) if len(ot["R"]) else (np.array([]), 0)
    R = ot["R"]
    bg = m[(R >= R_BG[0]) & (R < R_BG[1])].sum() / (math.pi * (R_BG[1] ** 2 - R_BG[0] ** 2))
    order = np.argsort(R); Rs = R[order]; cm = np.concatenate([[0.0], np.cumsum(m[order])])
    def f(Rsys):
        n = np.searchsorted(Rs, Rsys, side="left"); n0 = np.searchsorted(Rs, R_IN0, side="left")
        return (cm[n] - cm[n0]) - bg * math.pi * (Rsys ** 2 - R_IN0 ** 2)
    info = dict(ncut=ot["ncut"], nph=ot["nph"], nfb=nfb, nmem=len(R))
    CACHE[ck] = (f, info); return CACHE[ck]

def coverage_ok(key):
    _, info = members(key, W_PRIMARY, "cor")
    return info["ncut"] > 0 and info["nph"] / info["ncut"] >= COVER_MIN

# ------------------------------------------------------------------ systems: radius, baryons, speed, amount
def systems(cls, keys, Lz, cfg, zperm=None):
    """cfg: gas, corr, delta, w, radius ('self' | 300 | 600), layout ('A'|'B'), cfac, zs, starplus."""
    n = len(keys); out = dict(Rsys=np.zeros(n), Mmem=np.zeros(n), Mb=np.zeros(n), Ml=np.zeros(n), clip=np.zeros(n, bool))
    gas = GAS[cfg["gas"]][cls]
    for i, key in enumerate(keys):
        k = TGI[key]["lens_id"]; zl = TD[key]["z"]
        Ml = 10 ** lens_logm(k, cfg["corr"])
        f, _ = members(key, cfg["w"], cfg["delta"], None if zperm is None else zperm[i])
        sf = 1.4 if cfg["starplus"] else 1.0
        if cfg["radius"] == "self":
            R = 300.0
            for _ in range(30):
                Mb = Ml + sf * f(R) + gas
                Rn = min(max(R200c_kpc((1 + XC) * max(Mb, 1.0), zl), R_CLIP[0]), R_CLIP[1])
                if abs(Rn - R) < 0.1: R = Rn; break
                R = Rn
            out["clip"][i] = R <= R_CLIP[0] + 1e-9 or R >= R_CLIP[1] - 1e-9
        else:
            R = float(cfg["radius"])
        Mm = sf * f(R)
        out["Rsys"][i] = R; out["Mmem"][i] = Mm; out["Ml"][i] = Ml; out["Mb"][i] = Ml + Mm + gas
    out["gas"] = gas
    z = Lz.z
    out["s"] = {ft: np.array([J.vL_kms(max(out["Mb"][i], 1.0), z[i]) / J.vstar_kms(ft, z[i]) for i in range(n)]) for ft in FOOTS}
    out["s_H"] = {ft: out["s"][ft] * 2.0 for ft in FOOTS}; out["s_D"] = {ft: out["s"][ft] * 0.5 for ft in FOOTS}
    # amount (each lens treated as fast)
    Mobs = Lz.m_obs(E.ZS_INF if cfg["zs"] == "inf" else np.maximum(2.0, z + 0.5))
    if cfg["layout"] == "A":
        Mh = np.maximum(out["Mb"], 1.0)
        rs, rta = halo_interp(XC, Mh, z, cfg["cfac"])
        base = {ft: out["Ml"] * Lz.F2D for ft in FOOTS}
    else:
        Mh = np.maximum(out["Mb"] - out["Ml"], 1.0)
        rs, rta = halo_interp(XC, Mh, z, cfg["cfac"])
        base = {ft: Lz.m_law(out["Ml"], A0[ft]) for ft in FOOTS}
    cold = Lz.c_cyl(XC * Mh * (Mh > 1.0), rs, rta)
    gasc = Lz.c_cyl(np.full(n, gas), rs, rta) if gas > 0 else np.zeros(n)
    out["Mobs"] = Mobs; out["cold_cyl"] = cold; out["gas_cyl"] = gasc
    out["Mref"] = {ft: base[ft] + cold + gasc for ft in FOOTS}
    if MUT == "INJ": Mobs = out["Mref"]["canonical"]; out["Mobs_inj"] = True
    out["r"] = {ft: np.log10((out["Mref"][ft] if MUT == "INJ" else Mobs) / out["Mref"][ft]) for ft in FOOTS}
    out["missing_newton"] = Mobs - out["Ml"] * Lz.F2D
    out["supply_ratio"] = (cold + gasc) / out["missing_newton"]
    return out

def med_ci(v, seed=SEED):
    v = np.asarray(v, float); rng = np.random.default_rng(seed)
    b = np.median(v[rng.integers(0, len(v), size=(NBOOT, len(v)))], axis=1)
    return float(np.median(v)), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
def amount_word(ci):
    m, lo, hi = ci
    if lo > LINE: return "UNDER"
    if hi < -LINE: return "OVER"
    if lo <= LINE and hi >= -LINE: return "FITS"
    return "FITS"
def speed_word(ci):
    m, lo, hi = ci
    return "FAST" if lo >= 1 else ("SLOW" if hi < 1 else "MIXED")

# graded lenses
Wkeys = [TGW[k] for k in W_ids]
gW = [i for i, key in enumerate(Wkeys) if edge_ok(key) and coverage_ok(key)]
Ckeys = [t["target"] for t in TG if t["kind"] == "C"]
gC = [i for i, key in enumerate(Ckeys) if edge_ok(key) and coverage_ok(key)]
P(f"  graded W {len(gW)} of {len(Wkeys)} (edge: {sum(not edge_ok(k) for k in Wkeys)}, coverage: {sum(edge_ok(k) and not coverage_ok(k) for k in Wkeys)}); graded C {len(gC)} of {len(Ckeys)}")
def sub(L, idx):
    s = Lenses([L.ids[i] for i in idx]); return s
LWg = sub(LW, gW); LCg = sub(LC, gC)
Wg = [Wkeys[i] for i in gW]; Cg = [Ckeys[i] for i in gC]

BASE = dict(gas="MID", corr=True, delta="cor", w=W_PRIMARY, radius="self", layout="A", cfac=1.0, zs="inf", starplus=False)
BRK = {"G-0": dict(gas="0"), "G-HI": dict(gas="HI"), "B-UNC": dict(corr=False, delta="unc"), "B-RAW": dict(delta="raw"),
       "B-W05": dict(w=0.05), "B-W12": dict(w=0.12), "R300": dict(radius=300), "R600": dict(radius=600), "N-B": dict(layout="B"),
       "B-C07": dict(cfac=0.7), "B-C14": dict(cfac=1.4), "B-ZS2": dict(zs="2"), "B-STAR+": dict(starplus=True)}

ZPERM = None
if MUT == "ZS":
    rng = np.random.default_rng(SEED); zz = LWg.z.copy()
    while True:
        p = rng.permutation(len(zz))
        if not np.any(p == np.arange(len(zz))): break
    ZPERM = zz[p]

def evaluate(cfg, name):
    oW = systems("W", Wg, LWg, cfg, ZPERM); oC = systems("C", Cg, LCg, cfg)
    res = dict(cfg=cfg, foot={})
    for ft in FOOTS:
        sc = med_ci(oW["s"][ft]); rc = med_ci(oW["r"][ft])
        sw = speed_word(sc); aw = amount_word(rc)
        fastC = oC["s"][ft] >= 1; nfc = int(fastC.sum())
        if nfc >= 20:
            crc = med_ci(oC["r"][ft][fastC]); cond = bool(crc[1] <= LINE and crc[2] >= -LINE)
        else:
            crc = None; cond = True
        fastW = oW["s"][ft] >= 1
        rfast = med_ci(oW["r"][ft][fastW]) if fastW.sum() >= 20 else None
        if sw == "SLOW": word = W_SLOW
        elif aw == "UNDER": word = W_SHORT
        elif sw == "FAST" and aw == "FITS" and cond: word = W_PASS
        else: word = W_NV
        res["foot"][ft] = dict(speed=sc, speed_word=sw, amount=rc, amount_word=aw, word=word,
                               frac_fast_W=float(fastW.mean()), n_fast_W=int(fastW.sum()), r_fast_W=rfast,
                               frac_fast_C=float(fastC.mean()), n_fast_C=nfc, r_fast_C=crc, control_ok=cond,
                               speed_C=med_ci(oC["s"][ft]), amount_C=med_ci(oC["r"][ft]),
                               speed_H=speed_word(med_ci(oW["s_H"][ft])), speed_D=speed_word(med_ci(oW["s_D"][ft])),
                               supply_ratio=med_ci(oW["supply_ratio"]))
    res["W"] = dict(Rsys=med_ci(oW["Rsys"]), clipped=int(oW["clip"].sum()), Mmem=med_ci(oW["Mmem"]), Mlens=float(np.median(oW["Ml"])),
                    Mb=med_ci(oW["Mb"]), Mobs=float(np.median(oW["Mobs"])), cold_cyl=float(np.median(oW["cold_cyl"])),
                    gas_cyl=float(np.median(oW["gas_cyl"])), missing=float(np.median(oW["missing_newton"])),
                    Mmem_mean=float(np.mean(oW["Mmem"])))
    res["C"] = dict(Rsys=med_ci(oC["Rsys"]), Mmem=med_ci(oC["Mmem"]), Mlens=float(np.median(oC["Ml"])), Mb=med_ci(oC["Mb"]))
    return res, oW, oC

def show(name, res):
    w = res["W"]
    P(f"  [{name}] W: R_sys {w['Rsys'][0]:.0f} kpc (clipped {w['clipped']}); M*_lens {w['Mlens']:.3g}; net members {w['Mmem'][0]:.3g} [{w['Mmem'][1]:.3g}, {w['Mmem'][2]:.3g}] (mean {w['Mmem_mean']:.3g}); "
      f"M_b {w['Mb'][0]:.3g} [{w['Mb'][1]:.3g}, {w['Mb'][2]:.3g}]; M_obs {w['Mobs']:.3g}; halo cyl {w['cold_cyl']:.3g} + gas cyl {w['gas_cyl']:.3g}; missing (Newtonian) {w['missing']:.3g}")
    for ft in FOOTS:
        f = res["foot"][ft]
        P(f"    {ft:9s} s {f['speed'][0]:.3f} [{f['speed'][1]:.3f}, {f['speed'][2]:.3f}] {f['speed_word']} (fast {f['n_fast_W']}/{len(Wg)}); "
          f"r {f['amount'][0]:+.3f} [{f['amount'][1]:+.3f}, {f['amount'][2]:+.3f}] {f['amount_word']}; supply {f['supply_ratio'][0]:.2f}; "
          f"C: s {f['speed_C'][0]:.3f}, fast {f['n_fast_C']}, r {f['amount_C'][0]:+.3f}{'' if f['r_fast_C'] is None else ' (fast C r %+.3f [%+.3f, %+.3f])' % f['r_fast_C']}; "
          f"TW-H {f['speed_H']}, TW-D {f['speed_D']} -> {f['word']}")

P("")
P("=== MAIN (N-A, self-consistent R_200c, w 0.08, EUC17-corrected lens stars, gas G-MID, c x 1, z_s infinity)")
MAIN, oWm, oCm = evaluate(dict(BASE), "main")
show("main", MAIN)
P("")
P("=== BRACKETS (one change each)")
BR = {}
for name, ch in BRK.items():
    cfg = dict(BASE); cfg.update(ch)
    BR[name], _, _ = evaluate(cfg, name)
    show(name, BR[name])

# ------------------------------------------------------------------ instrument checks and twins (inside the main run)
P("")
P("=== INSTRUMENT CHECKS")
Rkeys = [t["target"] for t in TG if t["kind"] == "R" and edge_ok(t["target"]) and coverage_ok(t["target"])]
mR = np.array([members(k, W_PRIMARY, "cor")[0](300.0) for k in Rkeys])
N1 = dict(n=len(Rkeys), median=float(np.median(mR)), pass_=bool(abs(np.median(mR)) <= 1.0e11))
P(f"N1 blank fields: N {len(Rkeys)}, median net member mass in 300 kpc {np.median(mR):+.3g} Msun (|.| <= 1e11): {'pass' if N1['pass_'] else 'FAIL'}")
Lkeys = [t["target"] for t in TG if t["kind"] == "L" and edge_ok(t["target"]) and coverage_ok(t["target"])]
mL = np.array([members(k, W_PRIMARY, "cor")[0](300.0) for k in Lkeys])
mC = np.array([members(k, W_PRIMARY, "cor")[0](300.0) for k in Cg])
mW = np.array([members(k, W_PRIMARY, "cor")[0](300.0) for k in Wg])
rng = np.random.default_rng(SEED)
bd = np.median(mL[rng.integers(0, len(mL), (NBOOT, len(mL)))], axis=1) - np.median(mC[rng.integers(0, len(mC), (NBOOT, len(mC)))], axis=1)
N2 = dict(nL=len(Lkeys), L=float(np.median(mL)), C=float(np.median(mC)), lo=float(np.percentile(bd, 2.5)), pass_=bool(np.percentile(bd, 2.5) > 0))
P(f"N2 positive control: L median {np.median(mL):.3g} (N {len(Lkeys)}) vs C {np.median(mC):.3g}; difference lower bound {N2['lo']:+.3g}: {'pass' if N2['pass_'] else 'FAIL'}")
P(f"  reported: W median net member mass in 300 kpc {np.median(mW):.3g} (mean {np.mean(mW):.3g}); paired W - C (graded pairs) below")
pr = []
for p in sorted(pairs):
    q = pairs[p]
    if "W" in q and "C" in q and q["W"] in Wg and q["C"] in Cg:
        pr.append(members(q["W"], W_PRIMARY, "cor")[0](300.0) - members(q["C"], W_PRIMARY, "cor")[0](300.0))
PAIR = med_ci(pr)
P(f"  paired W - C net member mass in 300 kpc: {PAIR[0]:+.3g} [{PAIR[1]:+.3g}, {PAIR[2]:+.3g}] on {len(pr)} pairs")
# TW-ZS gate (computed here; the MUTATE run writes its own outputs)
rng2 = np.random.default_rng(SEED); zz = LWg.z.copy()
while True:
    p = rng2.permutation(len(zz))
    if not np.any(p == np.arange(len(zz))): break
mWs = np.array([members(k, W_PRIMARY, "cor", zz[p][i])[0](300.0) for i, k in enumerate(Wg)])
TWZS = dict(main=float(np.median(mW)), shuffled=float(np.median(mWs)), bites=bool(np.median(mWs) <= 0.5 * np.median(mW)))
P(f"TW-ZS photo-z shuffle: W median net member mass in 300 kpc {np.median(mW):.3g} -> {np.median(mWs):.3g} (must fall to <= half): {'bites' if TWZS['bites'] else 'DOES NOT BITE'}")
TWINJ = dict(bites=True, note="run WLG1_MUTATE=INJ for the separate outputs; by construction r = 0 for every lens, so (A) reads FITS")
if MUT == "INJ":
    TWINJ["bites"] = all(MAIN["foot"][ft]["amount_word"] == "FITS" for ft in FOOTS)

# ------------------------------------------------------------------ final words
KA_ALL = all(v["pass_"] for v in KA.values())
CHK = KA_ALL and N1["pass_"] and N2["pass_"] and TWZS["bites"] and TWINJ["bites"] and len(gW) >= 150
P("")
P("=== WORDS")
FINAL = {}
for ft in FOOTS:
    w0 = MAIN["foot"][ft]["word"] if CHK else W_NE
    diff = [n for n in BRK if BR[n]["foot"][ft]["word"] != MAIN["foot"][ft]["word"]]
    FINAL[ft] = dict(word=w0, fragile=bool(diff) and CHK, brackets_differing={n: BR[n]["foot"][ft]["word"] for n in diff})
    P(f"  {ft:9s}: {w0}{', FRAGILE' if FINAL[ft]['fragile'] else ''}" + (f"   (brackets differing: {FINAL[ft]['brackets_differing']})" if diff else ""))
P(f"  checks: known answers {'all pass' if KA_ALL else 'FAIL'}; N1 {N1['pass_']}; N2 {N2['pass_']}; TW-ZS {TWZS['bites']}; TW-INJ {TWINJ['bites']}; graded W {len(gW)}")
P("kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Adopts nothing.")
P(f"elapsed {time.time() - T0:.0f} s")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
RES = dict(lane="WLG1", criteria="8ca77a609e", mutate=MUT, KA=KA, N1=N1, N2=N2, TW_ZS=TWZS, TW_INJ=TWINJ, delta=DELTA, kml=KML,
           graded=dict(W=len(gW), C=len(gC)), pair_W_minus_C_300=PAIR, main=MAIN, brackets=BR, final=FINAL,
           note="TEST lane; POST HOC; adopts nothing; kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed")
json.dump(clean(RES), open(os.path.join(HERE, f"wlg1{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"wlg1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if not MUT:
    with open(os.path.join(HERE, "wlg1_per_lens.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["unique_identifier", "grade", "z_l", "theta_E_arcsec", "logM_lens_primary", "R_sys_kpc", "M_mem_net", "M_gas", "M_b",
                     "s_can", "s_alt", "logM_obs_inf", "logM_ref", "r_can", "M_mem_net_300kpc"])
        for i, key in enumerate(Wg):
            k = TGI[key]["lens_id"]
            wr.writerow([k, ROWS[k]["grade"], "%.3f" % ROWS[k]["z"], "%.3f" % ROWS[k]["tE"], "%.4f" % lens_logm(k, True), "%.1f" % oWm["Rsys"][i],
                         "%.4e" % oWm["Mmem"][i], "%.3e" % oWm["gas"], "%.4e" % oWm["Mb"][i], "%.4f" % oWm["s"]["canonical"][i], "%.4f" % oWm["s"]["alt"][i],
                         "%.4f" % np.log10(oWm["Mobs"][i]), "%.4f" % np.log10(oWm["Mref"]["canonical"][i]), "%.4f" % oWm["r"]["canonical"][i], "%.4e" % mW[i]])
sys.exit(1 if MUT else 0)
