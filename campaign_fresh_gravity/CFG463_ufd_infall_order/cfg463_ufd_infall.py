#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG463 -- DOES THE ULTRA-FAINTS' BARE-LAW EXCESS RISE WITH LATER INFALL?  The per-object test of CFG344.

CFG344 explains the Milky Way ultra-faints' bare-law excess by post-reionisation cold accretion onto reionisation fossils; the
accretion stops at infall, so with one formation epoch a LATER infaller carries MORE cold mass (3.7e8 / 5.75e8 / 8.8e8 Msun at
z_inf = 3 / 2 / 1).  Prediction, object by object: the excess x = log10(sigma_obs / sigma_law) ANTI-correlates with the infall
lookback time.  Everything is frozen in FROZEN_CRITERIA.md (committed e201f79eb, before this script and before any infall time).
In one line each:
  SAMPLE   S1 (verdict): FG001's resolved ultra-faints with a Fritz+18 Table 2 entry (21).  Reported: S2 (+5 upper limits), S3
           (no LMC candidates), S4 (all 31 resolved with the LVD's EDR3 motions; data veto).
  EXCESS   FG001's isolated law of the stars (sigma_pred, efe=False; Upsilon_V 2; r = 4/3 r_half), exec'd read-only as in CFG28.
  ORBITS   Fritz's frame (R0 8.2 kpc, v_sun (11, 248, 7.3) km/s, z_sun 25 pc); 300 Gaussian draws + central (seed 463); in-plane KDK
           leapfrog backward, dt 0.5 Myr, to the lookback at z_f = 8.
  HOSTS    L6 (PRIMARY): nu_mono(g_N/a0) g_N, M_b(t) = 6.0e10 h(z); L7: 7.3e10; L6s: M_b fixed (reported); N: Newtonian NFW
           M_200c = 9.82e11 h(z), DM14 c(M, z) (reported).  h(z) = CFG344's own Correa+15 MAH at 9.82e11 (exec'd read-only).
  INFALL   the largest lookback at which r <= R_200c(z) of 9.82e11 h(z) (first entry); B300: fixed 300 kpc (reported).
  STAT     Spearman rho(x, median t_inf); Z = atanh(rho) sqrt((N-3)/1.06); CFG344 predicts rho < 0.
  VERDICT  SUPPORTED: Z <= -2 in L6/L7 x canonical/alt, f_neg >= 0.84 (L6, both), rho < 0 for L6s and N, no S4 veto, controls
           pass.  CONTRADICTED: the mirror.  Else NOT DIAGNOSTIC, with the power to see CFG344's own slope.
MUTATE (CFG463_MUTATE=1): each object's infall-time block permuted across objects (seed 4631) -> must read NOT DIAGNOSTIC.
kappa = 1/2 FITTED.  No dark-matter particle: the cold fluid's MASS is still required.  Nothing here says the theory is closed or that
the data favour the framework.
Run: python3 campaign_fresh_gravity/CFG463_ufd_infall_order/cfg463_ufd_infall.py   (CFG463_MUTATE=1 for the control; ~10 min)
"""
import sys
sys.dont_write_bytecode = True
import os, io, math, csv, json, re, time, hashlib, contextlib
import numpy as np
from scipy.stats import spearmanr, theilslopes, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL

MUT = os.environ.get("CFG463_MUTATE", "0") == "1"
R = C.Report("cfg463_ufd_infall", MUT)
P, check = R.P, R.check
T0 = time.time()
P(__doc__.split("Run: python3")[0].strip())
if MUT:
    P("\n  *** MUTATE: each object's infall-time block is permuted across objects (seed 4631); the verdict must be NOT DIAGNOSTIC ***")
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()} (committed e201f79eb)")

FOOTS = ("canonical", "alt")
NMC, DT, ZF, EPS = 300, 0.5, 8.0, 0.5
M0_MW, MB6, MB7 = 9.82e11, 6.0e10, 7.3e10
LMC_CAND = ["Carina II", "Carina III", "Horologium I", "Hydrus I", "Reticulum II", "Tucana II"]
LB_KEYS = [("L6", "canonical"), ("L6", "alt"), ("L7", "canonical"), ("L7", "alt")]

# ================================================================================================ 1. the excess (FG001, read-only)
FGP = os.path.join(LANES, "CFG7_hierarchy_fg001.py")
_k1 = next(l for l in open(FGP).read().splitlines() if "K1 h43" in l).split(" reproduced")[0]
ns = {"np": np, "math": math, "os": os, "csv": csv, "C": C, "HL": HL}
ns = C.C4.exec_slices(FGP, [("G, kpc, Msun, A0H = HL.G", _k1), ("MW_MB, M31_MB, UPS_V = 6.0e10", "REF43 = {")], ns=ns, name="fg001_slices")[0]
A0H, UPS_V, resid, sigma_pred, fnum = ns["A0H"], ns["UPS_V"], ns["resid"], ns["sigma_pred"], ns["fnum"]
G_SI, MSUN_SI = ns["G"], ns["Msun"]
UFD = ns["ufd"]
FG = json.load(open(os.path.join(LANES, "CFG7_hierarchy_fg001_results.json")))["numbers"]
DSPH = ns["DSPH"]
UL = []
for r in csv.DictReader(open(os.path.join(DSPH, "lvd_dwarf_mw.csv"))):           # CFG28's limit loader (same cut)
    ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if ul is None or MV is None or rh is None or Dh is None or MV <= -7.7:
        continue
    MHI = fnum(r["mass_HI"])
    UL.append(dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, D=Dh, sig_ul=ul,
                   MHI=(10 ** MHI if MHI is not None else 0.0), host_mb=ns["MW_MB"]))


def spred(d, a0):
    Mb = UPS_V * d["LV"] + 1.33 * d["MHI"]
    return sigma_pred(Mb, (4.0 / 3.0) * d["rh"], d.get("D"), d["host_mb"], a0, efe=False)


R.banner("C-X  FG001's committed resolved ultra-faint median")
dev = max(abs(float(np.median(resid(UFD, A0H[f], efe=False))) - FG["SAT"][f"{f}|ufd"]["med_iso"]) for f in FOOTS)
check("C-X: FG001's committed resolved ultra-faint isolated median (+0.355 / +0.334) reproduced to 1e-9", f"max |d| {dev:.1e}; "
      f"{len(UFD)} resolved, {len(UL)} limits", dev <= 1e-9)
EXC = {}
for d in UFD:
    EXC[d["name"]] = dict(kind="res", MV=d["MV"], elog=0.4343 * d["esig"] / d["sig"],
                          x={f: math.log10(d["sig"] / spred(d, A0H[f])) for f in FOOTS})
for d in UL:
    EXC[d["name"]] = dict(kind="ul", MV=d["MV"], elog=0.0, x={f: math.log10(d["sig_ul"] / spred(d, A0H[f])) for f in FOOTS})

# ================================================================================================ 2. Fritz+18 Tables 1-3
TEX = os.path.join(C.REPO, "..", "_external_data", "cfg433_work", "src", "UFDsmot_arx_final.tex")
SHA_LOG = "5e958fa5eaf60ecab083ab0accddef0c0e807015edd25695cdd67c98eb591197"
txt = open(TEX).read()
sha = hashlib.sha256(txt.encode()).hexdigest()


def table_rows(label, end=r"\end{array}"):
    i0 = txt.index(label); i1 = txt.index(end, i0)
    out = []
    for line in txt[i0:i1].splitlines():
        line = line.strip()
        if "&" not in line or line.startswith("&") or line.startswith("name") or line.startswith("satellite"):
            continue
        c = [x.strip() for x in line.rstrip().rstrip("\\").split("&")]
        if len(c) >= 7:
            out.append(c)
    return out


def pm3(s):
    a = s.replace(" ", "").split(r"\pm")
    return [float(v) for v in a]


def asym(s):
    m = re.match(r"([-\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}", s.replace(" ", "").rstrip("\\"))
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def norm_t1(s):
    return s.replace('\\"{o}', "o").replace("\\", "").strip()


T1 = [(norm_t1(c[0]), pm3(c[6])) for c in table_rows(r"\label{KapSou}")]
T2 = []
for c in table_rows(r"\label{KapSou2}"):
    pa, pd, vl = pm3(c[2]), pm3(c[3]), pm3(c[5])
    vr = pm3(c[7]); vt = asym(c[8])
    T2.append(dict(abbr=c[0], d=float(c[1]), pa=pa[0], spa=pa[1], sys=pa[2], pd=pd[0], spd=pd[1], C=float(c[4]), vlos=vl[0],
                   evlos=vl[1], vrad=vr[0], evrad=vr[1], vtan=vt[0], evtan=0.5 * (vt[1] + vt[2])))
T3 = {}
for c in table_rows(r"\label{KapSou3}"):
    T3[c[0]] = dict(p16=float(re.match(r"([-\d.]+)", c[1]).group(1)), p08=float(re.match(r"([-\d.]+)", c[4]).group(1)))
FR = {  # Fritz abbreviation -> (Table 1 name, LVD name)
    "AquII": ("Aquarius II", "Aquarius II"), "BooI": ("Bootes I", "Bootes I"), "BooII": ("Bootes II", "Bootes II"),
    "CVenII": ("CanVen II", "Canes Venatici II"), "CarII": ("Carina II", "Carina II"), "CarIII": ("Carina III", "Carina III"),
    "CBerI": ("Coma Berenices I", "Coma Berenices"), "EriII": ("Eridanus II", "Eridanus II"), "GruI": ("Grus I", "Grus I"),
    "HerI": ("Hercules I", "Hercules"), "HorI": ("Horologium I", "Horologium I"), "HyiI": ("Hydrus I", "Hydrus I"),
    "LeoIV": ("Leo IV", "Leo IV"), "LeoV": ("Leo V", "Leo V"), "PisII": ("Pisces II", "Pisces II"),
    "RetII": ("Reticulum II", "Reticulum II"), "Seg1": ("Segue 1", "Segue 1"), "TucII": ("Tucana II", "Tucana II"),
    "UMaI": ("Ursa Major I", "Ursa Major I"), "UMaII": ("Ursa Major II", "Ursa Major II"), "Wil1": ("Willman 1", "Willman 1"),
    "DraII": ("Draco II", "Draco II"), "HyaII": ("Hydra II", "Hydra II"), "Seg2": ("Segue 2", "Segue 2"),
    "TriII": ("Triangulum II", "Triangulum II"), "TucIII": ("Tucana III", "Tucana III")}
order_ok = len(T1) == len(T2) == 39 and all(T1[i][0] == FR[T2[i]["abbr"]][0] for i in range(len(T2)) if T2[i]["abbr"] in FR)
R.banner("C-DATA  the Fritz+18 source and its tables")
check("C-DATA: the LaTeX source's sha256 equals FETCH_LOG.md's; Tables 1 and 2 parse to 39 rows each, in the same order",
      f"sha256 {sha[:8]}...{sha[-4:]} (log {SHA_LOG[:8]}...{SHA_LOG[-4:]}); rows {len(T1)} / {len(T2)} / Table 3 {len(T3)}; "
      f"order {order_ok}", sha == SHA_LOG and order_ok)
DM = {T2[i]["abbr"]: T1[i][1] for i in range(len(T2))}
T2D = {t["abbr"]: t for t in T2}
LVD = {r["name"]: r for r in csv.DictReader(open(os.path.join(DSPH, "lvd_dwarf_mw.csv")))}
LV2FR = {v[1]: k for k, v in FR.items()}
S1 = [d["name"] for d in UFD if d["name"] in LV2FR]
S2 = S1 + [d["name"] for d in UL if d["name"] in LV2FR]
S3 = [n for n in S1 if n not in LMC_CAND]
S4 = [d["name"] for d in UFD if fnum(LVD[d["name"]]["pmra"]) is not None and fnum(LVD[d["name"]]["pmdec"]) is not None]
S4_drop = [d["name"] for d in UFD if d["name"] not in S4]
P(f"\n  S1 {len(S1)}: " + ", ".join(S1))
P(f"  S2 {len(S2)} (adds the limits " + ", ".join(S2[len(S1):]) + f"); S3 {len(S3)}; S4 {len(S4)}"
  + (f" (dropped, no proper motion: {', '.join(S4_drop)})" if S4_drop else ""))
R.num("samples", dict(S1=S1, S2=S2, S3=S3, S4=S4, S4_drop=S4_drop))

# ================================================================================================ 3. phase space and the frame
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianDifferential
GCF = Galactocentric(galcen_distance=8.2 * u.kpc, galcen_v_sun=CartesianDifferential([11.0, 248.0, 7.3] * u.km / u.s), z_sun=25.0 * u.pc)


def to_rv(ra, dec, dist, pmra, pmdec, vlos):
    sc = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, distance=dist * u.kpc, pm_ra_cosdec=pmra * u.mas / u.yr, pm_dec=pmdec * u.mas / u.yr,
                  radial_velocity=vlos * u.km / u.s, frame="icrs")
    g = sc.transform_to(GCF)
    X = np.stack([g.x.to_value(u.kpc), g.y.to_value(u.kpc), g.z.to_value(u.kpc)], 1)
    V = np.stack([g.v_x.to_value(u.km / u.s), g.v_y.to_value(u.km / u.s), g.v_z.to_value(u.km / u.s)], 1)
    r = np.linalg.norm(X, axis=1)
    vr = np.sum(X * V, 1) / r
    vt = np.linalg.norm(np.cross(X, V), axis=1) / r
    return r, vr, vt


rng = np.random.default_rng(463)
cols = {k: [] for k in ("ra", "dec", "dist", "pmra", "pmdec", "vlos")}
for n in S2:
    t = T2D[LV2FR[n]]; dm, edm = DM[LV2FR[n]]
    ra, dec = fnum(LVD[n]["ra"]), fnum(LVD[n]["dec"])
    dmd = np.concatenate([[dm], dm + math.hypot(edm, 0.1) * rng.standard_normal(NMC)])
    sa, sd = math.hypot(t["spa"], t["sys"]), math.hypot(t["spd"], t["sys"])
    cov = np.array([[sa ** 2, t["C"] * t["spa"] * t["spd"]], [t["C"] * t["spa"] * t["spd"], sd ** 2]])
    pm = rng.multivariate_normal([t["pa"], t["pd"]], cov, NMC)
    vl = np.concatenate([[t["vlos"]], t["vlos"] + t["evlos"] * rng.standard_normal(NMC)])
    cols["ra"].append(np.full(NMC + 1, ra)); cols["dec"].append(np.full(NMC + 1, dec))
    cols["dist"].append(10 ** (dmd / 5 + 1) / 1e3)
    cols["pmra"].append(np.concatenate([[t["pa"]], pm[:, 0]])); cols["pmdec"].append(np.concatenate([[t["pd"]], pm[:, 1]]))
    cols["vlos"].append(vl)
RF, VRF, VTF = to_rv(*[np.concatenate(cols[k]) for k in ("ra", "dec", "dist", "pmra", "pmdec", "vlos")])
NO = len(S2)
RF, VRF, VTF = (a.reshape(NO, NMC + 1) for a in (RF, VRF, VTF))

R.banner("C-FRITZ  the frame conversion against Fritz Table 2")
worst = dict(d=0.0, vr=0.0, vt=0.0); rows_vt = 0
for i, n in enumerate(S2):
    t = T2D[LV2FR[n]]
    worst["d"] = max(worst["d"], abs(RF[i, 0] - t["d"])); worst["vr"] = max(worst["vr"], abs(VRF[i, 0] - t["vrad"]))
    if t["evtan"] < 30:
        rows_vt += 1
        worst["vt"] = max(worst["vt"], abs(VTF[i, 0] - t["vtan"]) / max(5.0, 0.05 * t["vtan"]))
    P(f"    {n:18s} d_GC {RF[i, 0]:6.1f} (Fritz {t['d']:4.0f})  V_rad {VRF[i, 0]:+7.1f} (Fritz {t['vrad']:+5.0f} +- {t['evrad']:.0f})  "
      f"V_tan {VTF[i, 0]:6.1f} (Fritz {t['vtan']:4.0f} +- {t['evtan']:.0f})")
check("C-FRITZ: |d_GC - Fritz| <= 1.5 kpc and |V_rad - Fritz| <= 3 km/s for all 26; |V_tan - Fritz| <= max(5 km/s, 5%) where its error < 30",
      f"max |dd| {worst['d']:.2f} kpc; max |dV_rad| {worst['vr']:.2f} km/s; worst V_tan / tolerance {worst['vt']:.2f} ({rows_vt} rows)",
      worst["d"] <= 1.5 and worst["vr"] <= 3.0 and worst["vt"] <= 1.0)
# POST-HOC diagnostic (added after a dry run of sections 1-4 showed the V_rad clause failing; no orbit or statistic had been computed):
# split the V_rad residual by measurement quality, and test whether Fritz's quoted value is the Monte Carlo median.
_wm = [i for i, n in enumerate(S2) if T2D[LV2FR[n]]["evtan"] < 30]
_pm = [i for i in range(NO) if i not in _wm]
_dv = lambda ii, col: max(abs(col[i] - T2D[LV2FR[S2[i]]]["vrad"]) for i in ii)
_vrmed = np.median(VRF[:, 1:], axis=1)
_zv = [abs(VRF[i, 0] - T2D[LV2FR[S2[i]]]["vrad"]) / T2D[LV2FR[S2[i]]]["evrad"] for i in range(NO)]
check("C-FRITZ diagnostic (POST-HOC, reported): the V_rad residual by measurement quality",
      f"V_tan error < 30 km/s ({len(_wm)} objects): max |dV_rad| {_dv(_wm, VRF[:, 0]):.2f} km/s; the other {len(_pm)}: max {_dv(_pm, VRF[:, 0]):.2f}; "
      f"with our MC median instead of the central value: {_dv(_pm, _vrmed):.2f}; largest |dV_rad| / Fritz's quoted error {max(_zv):.2f}; "
      f"objects off by > 3 km/s: " + ", ".join(f"{S2[i]} ({VRF[i, 0] - T2D[LV2FR[S2[i]]]['vrad']:+.1f})" for i in range(NO)
                                               if abs(VRF[i, 0] - T2D[LV2FR[S2[i]]]['vrad']) > 3), True, load_bearing=False)

# S4: the LVD's own (EDR3) motions, two-piece errors as CFG286
rng4 = np.random.default_rng(463)


def two_piece(c, em, ep, n):
    em = em if em is not None else ep; ep = ep if ep is not None else em
    if em is None:
        return np.full(n, c)
    z = rng4.standard_normal(n)
    return c + np.where(z > 0, z * ep, z * em)


c4 = {k: [] for k in ("ra", "dec", "dist", "pmra", "pmdec", "vlos")}
for n in S4:
    r_ = LVD[n]
    c4["ra"].append(np.full(NMC + 1, fnum(r_["ra"]))); c4["dec"].append(np.full(NMC + 1, fnum(r_["dec"])))
    for k, col in (("dist", "distance"), ("pmra", "pmra"), ("pmdec", "pmdec"), ("vlos", "vlos_systemic")):
        c_ = fnum(r_[col])
        v = np.concatenate([[c_], two_piece(c_, fnum(r_[col + "_em"]), fnum(r_[col + "_ep"]), NMC)])
        if k == "dist":
            v = np.maximum(v, 0.1 * c_)
        c4[k].append(v)
R4, VR4, VT4 = (a.reshape(len(S4), NMC + 1) for a in to_rv(*[np.concatenate(c4[k]) for k in ("ra", "dec", "dist", "pmra", "pmdec", "vlos")]))

# ================================================================================================ 4. host growth, boundary, cosmic time
ns344 = {"math": math, "np": np}
from scipy.optimize import brentq
ns344["brentq"] = brentq
P344 = os.path.join(LANES, "CFG344_postreion_cold_accretion", "cfg344_accretion.py")
ns344 = C.C4.exec_slices(P344, [("from colossus.cosmology import cosmology", 'check("C0 dD/dz')], ns=ns344, name="cfg344_mah")[0]
ab, M_of = ns344["ab"], ns344["M_of"]
aMW, bMW = ab(M0_MW)
LC = C.LCDM
T_NOW = float(LC.t(1.0)) * C.UNIT_GYR
ZG = np.linspace(0.0, ZF, 8001)
TLG = T_NOW - np.array([float(LC.t(1.0 / (1.0 + z))) for z in ZG]) * C.UNIT_GYR       # lookback (Gyr), increasing with z
TMAX = float(TLG[-1]) * 1e3                                                           # Myr
HG = (1.0 + ZG) ** aMW * np.exp(bMW * ZG)
RHOC = LC.rhoc0 * np.array([float(LC.E(1.0 / (1.0 + z))) ** 2 for z in ZG])             # Msun/Mpc^3
R200G = (3 * M0_MW * HG / (4 * math.pi * 200 * RHOC)) ** (1 / 3.) * 1e3              # kpc
H_DM = 0.674


def c_dm14(M, z):
    z = np.minimum(z, 5.0)
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * (np.log10(M * H_DM) - 12.0))


CG = c_dm14(M0_MW * HG, ZG)
TAUG = TLG * 1e3                                                                      # Myr grid


def z_of_tl(tl_gyr):
    return np.interp(tl_gyr, TLG, ZG)


R.banner("C-MAH  the MW's growth, its R_200c boundary and the NFW concentration")
mof_dev = max(abs(M_of(z, M0_MW) / M0_MW / ((1 + z) ** aMW * math.exp(bMW * z)) - 1) for z in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0))
src36 = open(os.path.join(LANES, "CFG36_colour_split_collapse.py")).read()
expr36 = re.search(r"c = (10 \*\* \(0\.905.*?\))\n", src36).group(1)
c36dev = max(abs(eval(expr36, {"math": math, "M200c": M}) / float(c_dm14(M, 0.0)) - 1) for M in (1e11, 9.82e11, 1e13))
zhalf = float(np.interp(0.5, HG[::-1], ZG[::-1]))
okmah = abs(HG[0] - 1) <= 1e-12 and bool(np.all(np.diff(HG) < 0)) and 200 <= R200G[0] <= 220 and c36dev <= 1e-12 and mof_dev <= 1e-12
check("C-MAH: h(0) = 1, h monotone over z 0..8, R_200c(0) in 200-220 kpc, DM14 at z = 0 equals CFG36's c(M) (and h equals CFG344's M_of)",
      f"alpha {aMW:.4f} beta {bMW:.4f}; h(0)-1 {HG[0] - 1:.1e}; monotone {bool(np.all(np.diff(HG) < 0))}; R_200c(0) {R200G[0]:.1f} kpc; "
      f"c(0) {CG[0]:.2f}; |DM14 - CFG36| {c36dev:.1e}; |h - M_of/M0| {mof_dev:.1e}; z_1/2 {zhalf:.2f}; t_max {TMAX / 1e3:.3f} Gyr "
      f"(z_f {ZF:.0f}); R_200c at z 1/2/3 = {np.interp(1, ZG, R200G):.0f}/{np.interp(2, ZG, R200G):.0f}/{np.interp(3, ZG, R200G):.0f} kpc",
      okmah)
R.num("MAH", dict(alpha=aMW, beta=bMW, R200_0=float(R200G[0]), c0=float(CG[0]), zhalf=zhalf, tmax_gyr=TMAX / 1e3))

# ================================================================================================ 5. hosts and the integrator (kpc, Myr, Msun)
KPC_M, MYR_S = 3.0857e19, 3.15576e13
KMS = 1e3 * MYR_S / KPC_M
G_K = G_SI * MSUN_SI * MYR_S ** 2 / KPC_M ** 3
ACC = MYR_S ** 2 / KPC_M
EPS2 = EPS ** 2


class Host:
    def __init__(self, kind, Mb0=None, foot=None, grow=True):
        self.kind, self.Mb0, self.foot, self.grow = kind, Mb0, foot, grow
        self.a0 = A0H[foot] * ACC if foot else None

    def g(self, r, tau):
        if self.kind == "law":
            h = float(np.interp(tau, TAUG, HG)) if self.grow else 1.0
            gN = G_K * self.Mb0 * h * r / (r * r + EPS2) ** 1.5
            return C.nu_mono(gN / self.a0) * gN
        M = M0_MW * float(np.interp(tau, TAUG, HG)); Rv = float(np.interp(tau, TAUG, R200G)); c = float(np.interp(tau, TAUG, CG))
        rr = np.maximum(r, 1e-3); x = rr * c / Rv
        return G_K * M * (np.log1p(x) - x / (1 + x)) / (math.log1p(c) - c / (1 + c)) / rr ** 2


BOUNDS = {"R200": lambda tau: float(np.interp(tau, TAUG, R200G)), "B300": lambda tau: 300.0}


def integrate(r0, vr0, vt0, host, dt=DT, tmax=TMAX):
    """in-plane KDK leapfrog backward in time (lookback tau increasing); returns t_inf (Gyr) and the censored flag per boundary."""
    n = len(r0)
    X = np.stack([r0, np.zeros(n)], 1).astype(float); V = -np.stack([vr0, vt0], 1) * KMS
    r = np.hypot(X[:, 0], X[:, 1]); a = -(host.g(r, 0.0) / r)[:, None] * X
    tinf = {b: np.zeros(n) for b in BOUNDS}
    fprev = {b: BOUNDS[b](0.0) - r for b in BOUNDS}
    nst = int(round(tmax / dt))
    for k in range(1, nst + 1):
        tau = k * dt
        V += 0.5 * dt * a; X += dt * V
        r = np.hypot(X[:, 0], X[:, 1]); a = -(host.g(r, tau) / r)[:, None] * X; V += 0.5 * dt * a
        for b in BOUNDS:
            f = BOUNDS[b](tau) - r
            ex = (fprev[b] >= 0) & (f < 0)
            if ex.any():
                tinf[b][ex] = tau - dt + dt * fprev[b][ex] / (fprev[b][ex] - f[ex])
            fprev[b] = f
    cens = {b: fprev[b] >= 0 for b in BOUNDS}
    for b in BOUNDS:
        tinf[b][cens[b]] = nst * dt
        tinf[b] = tinf[b] / 1e3
    return tinf, cens


def static_checks(r0, vr0, vt0, host, dt=DT, tmax=TMAX):
    """static host: energy drift |E_end - E_0| / (v0^2 / 2) and the most recent pericentre."""
    lnr = np.linspace(math.log(0.01), math.log(1e5), 40001); rg = np.exp(lnr)
    gr = host.g(rg, 0.0) * rg
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (gr[1:] + gr[:-1]) * np.diff(lnr))])
    Phi = lambda rr: np.interp(np.log(rr), lnr, phi)
    n = len(r0)
    X = np.stack([r0, np.zeros(n)], 1).astype(float); V = -np.stack([vr0, vt0], 1) * KMS
    r = np.hypot(X[:, 0], X[:, 1]); a = -(host.g(r, 0.0) / r)[:, None] * X
    E0 = 0.5 * np.sum(V ** 2, 1) + Phi(r); K0 = 0.5 * np.sum(V ** 2, 1)
    rp = np.full(n, np.nan); rprev2 = None; rprev = r.copy()
    for k in range(1, int(round(tmax / dt)) + 1):
        V += 0.5 * dt * a; X += dt * V
        r = np.hypot(X[:, 0], X[:, 1]); a = -(host.g(r, 0.0) / r)[:, None] * X; V += 0.5 * dt * a
        if rprev2 is not None:
            hit = np.isnan(rp) & (rprev < rprev2) & (rprev <= r)
            rp[hit] = rprev[hit]
        rprev2, rprev = rprev, r
    E1 = 0.5 * np.sum(V ** 2, 1) + Phi(r)
    return np.abs(E1 - E0) / K0, rp


# ================================================================================================ 6. C-ORB and the runs
R.banner("C-ORB  integrator checks (central S2 orbits)")
drift, _ = static_checks(RF[:, 0], VRF[:, 0], VTF[:, 0], Host("law", MB6, "canonical", grow=False))
check("C-ORB (a): static L6 host, central S2 orbits: |E_end - E_0| / (v0^2/2) <= 1e-4 over t_max",
      f"max {drift.max():.1e} (median {np.median(drift):.1e}) over {TMAX / 1e3:.2f} Gyr", float(drift.max()) <= 1e-4)
ta, _ = integrate(RF[:, 0], VRF[:, 0], VTF[:, 0], Host("law", MB6, "canonical"))
tb, _ = integrate(RF[:, 0], VRF[:, 0], VTF[:, 0], Host("law", MB6, "canonical"), dt=DT / 2)
dtd = np.abs(ta["R200"] - tb["R200"])
frac = float(np.mean(dtd <= 0.05))
bad = [f"{S2[i]} ({ta['R200'][i]:.2f} vs {tb['R200'][i]:.2f})" for i in np.where(dtd > 0.05)[0]]
check("C-ORB (b): dt halved: >= 90% of the central L6-canonical S2 orbits keep t_inf within 0.05 Gyr",
      f"{frac * 100:.0f}% within; max |dt_inf| {dtd.max():.3f} Gyr" + (f"; outside: {', '.join(bad)}" if bad else ""), frac >= 0.9)

HOSTS = {("L6", f): Host("law", MB6, f) for f in FOOTS}
HOSTS.update({("L7", f): Host("law", MB7, f) for f in FOOTS})
HOSTS.update({("L6s", f): Host("law", MB6, f, grow=False) for f in FOOTS})
HOSTS[("N", None)] = Host("nfw")
TI = {}                                                    # (host, foot, sample-set, boundary) -> (N_obj, NMC+1) t_inf
CEN = {}
for key, host in HOSTS.items():
    t1 = time.time()
    ti, ce = integrate(RF.ravel(), VRF.ravel(), VTF.ravel(), host)
    for b in BOUNDS:
        TI[key + ("F", b)] = ti[b].reshape(NO, NMC + 1); CEN[key + ("F", b)] = ce[b].reshape(NO, NMC + 1)
    P(f"  integrated {key[0]}{'' if key[1] is None else ' ' + key[1]} on S2 ({NO * (NMC + 1)} orbits) in {time.time() - t1:.0f} s")
for f in FOOTS:
    t1 = time.time()
    ti, ce = integrate(R4.ravel(), VR4.ravel(), VT4.ravel(), HOSTS[("L6", f)])
    for b in BOUNDS:
        TI[("L6", f, "E", b)] = ti[b].reshape(len(S4), NMC + 1); CEN[("L6", f, "E", b)] = ce[b].reshape(len(S4), NMC + 1)
    P(f"  integrated L6 {f} on S4 ({len(S4) * (NMC + 1)} orbits) in {time.time() - t1:.0f} s")

# ================================================================================================ 7. MUTATE: permute infall-time blocks
if MUT:
    prm = np.random.default_rng(4631)
    permF = prm.permutation(NO); permE = prm.permutation(len(S4))
    for k in list(TI):
        pm_ = permF if k[2] == "F" else permE
        TI[k] = TI[k][pm_]; CEN[k] = CEN[k][pm_]
    P(f"  MUTATE permutation (S2 order): " + ", ".join(f"{S2[i]}<-{S2[permF[i]]}" for i in range(NO)))

# ================================================================================================ 8. statistics
def zof(rho, n):
    rho = max(min(rho, 0.999999), -0.999999)
    return math.atanh(rho) * math.sqrt((n - 3) / 1.06)


def rho_of(x, t):
    if np.ptp(t) == 0 or np.ptp(x) == 0:
        return float("nan")
    return float(spearmanr(x, t).correlation)


def sub(names, base):
    return [base.index(n) for n in names]


IDX = {"S1": sub(S1, S2), "S2": list(range(NO)), "S3": sub(S3, S2)}
epsr = np.random.default_rng(4630).standard_normal((len(S4) + NO, NMC))


def reading(hk, foot, sname, b="R200", with_mc=True, with_perm=True):
    if sname == "S4":
        names = S4; T = TI[(hk, foot, "E", b)]; Cn = CEN[(hk, foot, "E", b)]; idx = list(range(len(S4)))
    else:
        names = [S2[i] for i in IDX[sname]]; T = TI[(hk, None if hk == "N" else foot, "F", b)][IDX[sname]]
        Cn = CEN[(hk, None if hk == "N" else foot, "F", b)][IDX[sname]]
    x = np.array([EXC[n]["x"][foot] for n in names]); el = np.array([EXC[n]["elog"] for n in names])
    that = np.median(T, axis=1)
    n = len(names); rho = rho_of(x, that); Z = zof(rho, n)
    out = dict(n=n, rho=rho, Z=Z, t_med=float(np.median(that)), cens=float(np.mean(Cn)), names=names, x=x.tolist(), that=that.tolist(),
               t16=np.percentile(T, 16, axis=1).tolist(), t84=np.percentile(T, 84, axis=1).tolist())
    if with_mc:
        e = epsr[:n]
        rk = np.array([rho_of(x + el * e[:, k - 1], T[:, k]) for k in range(1, NMC + 1)])
        out.update(fneg=float(np.mean(rk < 0)), fpos=float(np.mean(rk > 0)), rho_mc_med=float(np.nanmedian(rk)))
    if with_perm:
        pr = np.random.default_rng(4632)
        rx = rankdata(x); rt = rankdata(that); rx = (rx - rx.mean()) / rx.std(); rt = (rt - rt.mean()) / rt.std()
        Pm = np.array([pr.permutation(n) for _ in range(10000)])
        rs = (rt[Pm] * rx[None, :]).mean(1)
        out.update(p_perm=float(np.mean(np.abs(rs) >= abs(rho) - 1e-12)),
                   null_rate=float(np.mean(np.abs(np.arctanh(np.clip(rs, -0.999999, 0.999999)) * math.sqrt((n - 3) / 1.06)) >= 2)))
    return out


RD = {}
for (hk, f) in [("L6", f) for f in FOOTS] + [("L7", f) for f in FOOTS] + [("L6s", f) for f in FOOTS] + [("N", f) for f in FOOTS]:
    for s in ("S1", "S2", "S3"):
        RD[(hk, f, s)] = reading(hk, f, s)
for f in FOOTS:
    RD[("L6", f, "S4")] = reading("L6", f, "S4")
    RD[("L6", f, "S1B300")] = reading("L6", f, "S1", b="B300")


def fmt(d):
    s = f"N {d['n']:2d}  rho {d['rho']:+.3f}  Z {d['Z']:+.2f}  p_perm {d.get('p_perm', float('nan')):.3f}"
    if "fneg" in d:
        s += f"  f_neg {d['fneg']:.2f}  MC-median rho {d['rho_mc_med']:+.3f}"
    return s + f"  median t_inf {d['t_med']:.2f} Gyr  censored {d['cens'] * 100:.1f}%"


R.banner("PER-OBJECT TABLE (S2; t_inf = median [16-84%] lookback in Gyr; x canonical / alt; * = upper limit; L = LMC candidate)")
P(f"    {'object':18s} {'x can':>6s} {'x alt':>6s} {'ELOG':>5s} {'r_now':>6s} {'v_r':>6s} {'v_t':>6s}   "
  f"{'L6 can':>18s} {'L6 alt':>18s} {'N':>18s} {'L6s can':>8s} {'B300':>6s}")
for i, n in enumerate(S2):
    def tt(k):
        T = TI[k][i]
        return f"{np.median(T):5.2f} [{np.percentile(T, 16):5.2f},{np.percentile(T, 84):5.2f}]"
    P(f"    {n + (' *' if EXC[n]['kind'] == 'ul' else '') + (' L' if n in LMC_CAND else ''):18s} {EXC[n]['x']['canonical']:+6.3f} "
      f"{EXC[n]['x']['alt']:+6.3f} {EXC[n]['elog']:5.3f} {RF[i, 0]:6.1f} {VRF[i, 0]:+6.0f} {VTF[i, 0]:6.0f}   "
      f"{tt(('L6', 'canonical', 'F', 'R200'))} {tt(('L6', 'alt', 'F', 'R200'))} {tt(('N', None, 'F', 'R200'))} "
      f"{np.median(TI[('L6s', 'canonical', 'F', 'R200')][i]):8.2f} {np.median(TI[('L6', 'canonical', 'F', 'B300')][i]):6.2f}")
R.num("per_object", {n: dict(x=EXC[n]["x"], elog=EXC[n]["elog"], kind=EXC[n]["kind"], r_now=float(RF[i, 0]), v_r=float(VRF[i, 0]),
                            v_t=float(VTF[i, 0]), t_inf={f"{k[0]}|{k[1]}|{k[3]}": [float(np.median(TI[k][i])), float(np.percentile(TI[k][i], 16)),
                                                                                       float(np.percentile(TI[k][i], 84))]
                                                         for k in TI if k[2] == "F"}) for i, n in enumerate(S2)})

R.banner("READINGS (S1 = verdict sample; Spearman rho(x, median t_inf); CFG344 predicts rho < 0)")
for (hk, f, s), d in RD.items():
    tag = "LOAD-BEARING" if (hk, f) in LB_KEYS and s == "S1" else "reported"
    P(f"    {hk:4s} {f:9s} {s:6s} {fmt(d)}   [{tag}]")
R.num("readings", {f"{k[0]}|{k[1]}|{k[2]}": {kk: vv for kk, vv in v.items() if kk not in ("x", "that", "t16", "t84")} for k, v in RD.items()})

# ================================================================================================ 9. controls on the statistic
R.banner("C-SIGN / C-NULL")
tt0 = np.array(RD[("L6", "canonical", "S1")]["that"])
rs = rho_of(-tt0, tt0)
check("C-SIGN: x = -t_inf gives rho = -1", f"rho {rs:+.6f}", abs(rs + 1) < 1e-12)
nr = RD[("L6", "canonical", "S1")]["null_rate"]
check("C-NULL: 10,000 shuffles of t_inf (L6 canonical, S1): P(|Z| >= 2) <= 0.07", f"{nr:.4f}", nr <= 0.07)

# ================================================================================================ 10. reported rows
R.banner("REPORTED ROWS (none is a verdict)")
REP = {}
for f in FOOTS:
    d = RD[("L6", f, "S1")]
    x = np.array(d["x"]); t = np.array(d["that"]); n = len(x)
    rgc = np.array([RF[S2.index(nm), 0] for nm in d["names"]]); mv = np.array([EXC[nm]["MV"] for nm in d["names"]])

    def partial(cv):
        rxt, rxc, rtc = rho_of(x, t), rho_of(x, cv), rho_of(t, cv)
        pr_ = (rxt - rxc * rtc) / math.sqrt((1 - rxc ** 2) * (1 - rtc ** 2))
        return pr_, math.atanh(max(min(pr_, 0.999999), -0.999999)) * math.sqrt((n - 4) / 1.06), rxc, rtc
    pR = partial(np.log10(rgc)); pM = partial(mv)
    loo = [zof(rho_of(np.delete(x, i), np.delete(t, i)), n - 1) for i in range(n)]
    ts = theilslopes(x, t)[0]
    br = np.random.default_rng(4634); bs = []
    for _ in range(2000):
        ii = br.integers(0, n, n)
        if np.ptp(t[ii]) > 0:
            bs.append(theilslopes(x[ii], t[ii])[0])
    REP[f] = dict(partial_logr=pR, partial_MV=pM, loo_min=min(loo), loo_max=max(loo), theil=ts, theil_err=float(np.std(bs)),
                  rho_x_rgc=rho_of(x, rgc))
    P(f"    {f:9s} partial | log r_GC: rho {pR[0]:+.3f} (Z {pR[1]:+.2f}; rho(x, r) {pR[2]:+.3f}, rho(t, r) {pR[3]:+.3f});  partial | M_V: "
      f"rho {pM[0]:+.3f} (Z {pM[1]:+.2f}; rho(x, M_V) {pM[2]:+.3f}, rho(t, M_V) {pM[3]:+.3f})")
    P(f"    {f:9s} leave-one-out Z range [{min(loo):+.2f}, {max(loo):+.2f}];  Theil-Sen dx/dt_inf {ts:+.4f} +- {np.std(bs):.4f} dex/Gyr;  "
      f"Spearman(x, r_GC) on S1 {rho_of(x, rgc):+.3f} (CFG28's T2 on the 31: -0.22)")

# CFG344's predicted shift, the predicted slope and the power
J344 = json.load(open(os.path.join(LANES, "CFG344_postreion_cold_accretion", "cfg344_accretion_results.json")))
H8 = J344["HIST"]["8.0"]; M0f = H8["M0"]
OFF = {p: [J344["RUNS"][f"zf8_zinf{z}"]["rows"][p]["P1"]["canonical"][0] for z in (3, 2, 1)] for p in ("nfw", "sis")}
LMg = np.array([math.log10(M_of(z, M0f)) for z in (3.0, 2.0, 1.0)])
lmdev = max(abs(LMg[i] - math.log10(H8["M"][f"{z:.1f}"])) for i, z in enumerate((3.0, 2.0, 1.0)))
af, bf = ab(M0f)


def dx_pred(z, prof):
    z = np.minimum(np.asarray(z, float), ZF)
    lm = np.log10(M0f) + af * np.log10(1 + z) + bf * z / math.log(10)
    o = np.array(OFF[prof])
    s0 = (o[1] - o[0]) / (LMg[1] - LMg[0]); s1 = (o[2] - o[1]) / (LMg[2] - LMg[1])
    off = np.where(lm < LMg[0], o[0] + s0 * (lm - LMg[0]), np.where(lm > LMg[2], o[2] + s1 * (lm - LMg[2]), np.interp(lm, LMg, o)))
    return -(off - o[1])


P(f"\n    CFG344 committed offsets (P1 canonical; z_inf 3/2/1): NFW {OFF['nfw'][0]:+.4f}/{OFF['nfw'][1]:+.4f}/{OFF['nfw'][2]:+.4f}; "
  f"SIS {OFF['sis'][0]:+.4f}/{OFF['sis'][1]:+.4f}/{OFF['sis'][2]:+.4f}; log M_c {LMg[0]:.3f}/{LMg[1]:.3f}/{LMg[2]:.3f} "
  f"(vs its JSON HIST: max |d| {lmdev:.1e})")
d = RD[("L6", "canonical", "S1")]
x = np.array(d["x"]); t = np.array(d["that"]); n = len(x)
T = TI[("L6", "canonical", "F", "R200")][IDX["S1"]]
POW = {}
for prof in ("nfw", "sis"):
    pslope = theilslopes(dx_pred(z_of_tl(t), prof), t)[0]
    pw = np.random.default_rng(4633); Zs, rhos = [], []
    for _ in range(2000):
        kk = pw.integers(1, NMC + 1, n)
        ttrue = T[np.arange(n), kk]
        xm = x[pw.permutation(n)] + dx_pred(z_of_tl(ttrue), prof)
        r_ = rho_of(xm, t); rhos.append(r_); Zs.append(zof(r_, n))
    Zs = np.array(Zs)
    POW[prof] = dict(power=float(np.mean(Zs <= -2)), rho_pred=float(np.median(rhos)), Z_pred=float(np.median(Zs)), slope_pred=float(pslope),
                     dx_range=[float(dx_pred(z_of_tl(t), prof).min()), float(dx_pred(z_of_tl(t), prof).max())])
    P(f"    POWER ({prof.upper()} cold-mass profile, L6 canonical, S1, N {n}): P(Z <= -2) = {POW[prof]['power']:.3f}; predicted rho "
      f"{POW[prof]['rho_pred']:+.3f} (median Z {POW[prof]['Z_pred']:+.2f}); predicted Theil-Sen slope {pslope:+.4f} dex/Gyr "
      f"(observed {REP['canonical']['theil']:+.4f} +- {REP['canonical']['theil_err']:.4f}); predicted shifts span "
      f"{POW[prof]['dx_range'][0]:+.3f}..{POW[prof]['dx_range'][1]:+.3f} dex")
R.num("power", POW); R.num("reported", REP)

# static NFW pericentres against Fritz Table 3 (sanity only; different potential)
_, rpN = static_checks(RF[:, 0], VRF[:, 0], VTF[:, 0], Host("nfw"), tmax=4000.0)
P("\n    static NFW (9.82e11, c {:.1f}) central pericentre vs Fritz Table 3 (0.8e12 / 1.6e12 potentials), kpc:".format(CG[0]))
P("    " + "; ".join(f"{n} {rpN[i]:.0f} ({T3[LV2FR[n]]['p08']:.0f}/{T3[LV2FR[n]]['p16']:.0f})" for i, n in enumerate(S2)))

# ================================================================================================ 11. verdict
def verdict(RDx, controls_ok):
    res = {}
    for sign, name in ((-1, "SUPPORTED"), (+1, "CONTRADICTED")):
        lb = all(sign * RDx[(h, f, "S1")]["Z"] >= 2 for h, f in LB_KEYS)
        fr = all(RDx[("L6", f, "S1")]["fneg" if sign < 0 else "fpos"] >= 0.84 for f in FOOTS)
        sc = all(sign * RDx[(h, f, "S1")]["rho"] > 0 for h in ("L6s", "N") for f in FOOTS)
        veto = any(-sign * RDx[("L6", f, "S4")]["Z"] >= 2 for f in FOOTS)
        res[name] = dict(load_bearing=lb, mc_sign=fr, sign_conditions=sc, veto=veto, all=lb and fr and sc and not veto and controls_ok)
    v = "SUPPORTED" if res["SUPPORTED"]["all"] else "CONTRADICTED" if res["CONTRADICTED"]["all"] else "NOT DIAGNOSTIC"
    return v, res


lb_controls = [c for c in R.checks if c["load_bearing"]]
controls_ok = all(c["ok"] for c in lb_controls)
V, VRES = verdict(RD, controls_ok)
R.banner("VERDICT")
for h, f in LB_KEYS:
    P(f"    {h} {f:9s}: Z {RD[(h, f, 'S1')]['Z']:+.2f}")
P(f"    sign conditions: L6s rho {RD[('L6s', 'canonical', 'S1')]['rho']:+.3f} / {RD[('L6s', 'alt', 'S1')]['rho']:+.3f};  N rho "
  f"{RD[('N', 'canonical', 'S1')]['rho']:+.3f} / {RD[('N', 'alt', 'S1')]['rho']:+.3f};  S4 veto Z {RD[('L6', 'canonical', 'S4')]['Z']:+.2f} / "
  f"{RD[('L6', 'alt', 'S4')]['Z']:+.2f};  MC f_neg {RD[('L6', 'canonical', 'S1')]['fneg']:.2f} / {RD[('L6', 'alt', 'S1')]['fneg']:.2f}")
for k, v in VRES.items():
    P(f"    {k:12s}: " + ", ".join(f"{kk} {vv}" for kk, vv in v.items()))
P(f"\n    VERDICT: {V}   (load-bearing controls {'pass' if controls_ok else 'FAIL'}; power for CFG344's slope: NFW profile "
  f"{POW['nfw']['power']:.2f}, SIS profile {POW['sis']['power']:.2f}, N = {RD[('L6', 'canonical', 'S1')]['n']})")
R.num("VERDICT", V); R.num("VRES", VRES)
if MUT:
    okm = V == "NOT DIAGNOSTIC" and all(abs(RD[(h, f, "S1")]["Z"]) < 2 for h, f in LB_KEYS)
    check("MUTATE: with the infall-time blocks permuted the verdict is NOT DIAGNOSTIC and |Z| < 2 in all four load-bearing readings",
          f"verdict {V}; Z " + " / ".join(f"{RD[(h, f, 'S1')]['Z']:+.2f}" for h, f in LB_KEYS), okm)
P(f"\n  kappa = 1/2 FITTED.  No dark-matter particle; the cold fluid's MASS is still required.  Runtime {time.time() - T0:.0f} s.")
nf = R.write(HERE)
sys.exit(1 if nf else 0)
