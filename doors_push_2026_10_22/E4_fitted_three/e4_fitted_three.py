#!/usr/bin/env python3
"""E4_fitted_three -- measurement audit of the screened theory's three fitted constants (kappa, L*, u) under the owner's
raw-data rule, their dependency structure (Jacobian rank) and the forced-relation test.

Criteria: FROZEN_CRITERIA.md (committed alone first, 9cc8fcae21; AMENDMENT A1 pre-result, 9b3dfb1000).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 e4_fitted_three.py [--mutate]
  --mutate : the native kernel nu_L is replaced by nu_RAR everywhere it is used; K5 must fail.
Deterministic, no network, single thread. kappa = 1/2 FITTED. Footings never pooled. Cold energy, no particle.
Not theory closed.
"""
import os, sys, math, json, csv, warnings
import numpy as np
from scipy.optimize import brentq

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(ROOT, "campaign_fresh_gravity")
sys.path.insert(0, CFG)
import CFG4_common as C4                                   # noqa: E402  (nu_mono, the two footings; read-only)

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
LANE = "E4_FITTED_THREE"
OUT, CHECKS, RES = [], [], {"lane": LANE, "mutate": MUT, "criteria": ["9cc8fcae21", "9b3dfb1000"]}
_trapz = getattr(np, "trapezoid", None) or np.trapz


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def check(cid, ok, value, thr, label):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=value, threshold=thr, label=label))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr} :: {label}")


def rel(p):
    return os.path.relpath(p, ROOT)


# ============================================================================ kernels
def nu_L(y):                    # the screened theory's law g_N = g^2/(g + a0)  ->  nu = (1 + sqrt(1 + 4/y))/2
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def nu_RAR(y):                  # McGaugh+16 RAR fitting function (CFG820/821's kernel) -- STANDARD-MOND / empirical
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


NU_NATIVE = nu_RAR if MUT else nu_L
NU_MONO = C4.nu_mono
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}           # record footing values (FP0)
assert abs(C4.A0["canonical"] - A0["canonical"]) < 1e-15 and abs(C4.A0["alt"] - A0["alt"]) < 1e-15

P(f"{LANE}  (kappa, L*, u): measurement audit, dependency, forced relations" + ("  [MUTATE: nu_native := nu_RAR]" if MUT else ""))

# K5: the native kernel is the law
yy = np.logspace(-4, 4, 4001)
gN_from_law = lambda g: g * g / (g + 1.0)                   # units of a0
res5 = float(np.max(np.abs(gN_from_law(yy * NU_NATIVE(yy)) / yy - 1.0)))
check("K5", res5 < 1e-12, f"{res5:.2e}", "<1e-12", "native kernel satisfies g_N = g^2/(g+a0) on y in [1e-4, 1e4]")

# ============================================================================ PART A: kappa
P("\n=== PART A: kappa (galaxy gas routes, CFG493; cluster channel excluded as circular, A81 sec. 9.4)")
J493 = json.load(open(os.path.join(CFG, "CFG493_kappa_combined", "cfg493_kappa_combined_results.json")))
SH = {"S_gas": 0.0473, "S_star": 0.068, "S_HF": 0.0174}     # CFG493 line 233 (shared prior sigmas, dex)
ROUTES = []
for name, r in J493["routes"].items():
    ROUTES.append(dict(name=name, L=r["L"], U=r["unique"], lev=r["levers"]))


def cov(routes):
    n = len(routes); Cm = np.zeros((n, n))
    for i, r in enumerate(routes):
        Cm[i, i] += sum(v ** 2 for v in r["U"].values())
    for k in sorted(set(k for r in routes for k in r["lev"])):
        l = np.array([r["lev"].get(k, 0.0) for r in routes]); Cm += np.outer(l, l) * SH.get(k, 0.0) ** 2
    return Cm


def gls(routes, Lv=None):
    Lv = np.array([r["L"] for r in routes]) if Lv is None else np.asarray(Lv)
    Ci = np.linalg.inv(cov(routes)); one = np.ones(len(routes))
    w = Ci @ one / (one @ Ci @ one)
    return float(w @ Lv), float(1 / math.sqrt(one @ Ci @ one)), w


L0, s0, w0 = gls(ROUTES)
check("K1", abs(L0 + 10.10732) < 1e-4 and abs(s0 - 0.098475) < 1e-4, f"{L0:.5f}+-{s0:.6f}", "-10.10732+-0.098475 (1e-4)",
      "CFG493 GLS reproduced from its JSON with its own covariance")
lev_HF = np.array([r["lev"].get("S_HF", 0.0) for r in ROUTES])
Lv0 = np.array([r["L"] for r in ROUTES])
L_v6, _, _ = gls(ROUTES, Lv0 + lev_HF * math.log10(73.04 / 67.4))
check("K2", abs(L_v6 + 10.0621) < 0.002, f"{L_v6:.4f}", "-10.0621+-0.002", "CFG493 V6 (HF distances at H0 73.04) by lever arithmetic")

c_SI, G_SI, MPC = 2.99792458e8, 6.67430e-11, 3.0856775814913673e22
den = lambda h, OmL: c_SI * (100e3 * h / MPC) * math.sqrt(3 * OmL / (8 * math.pi))   # c sqrt(G rho), rho = 3H^2 OmL/(8piG)
DEN_REC = {"canonical": 2 * A0["canonical"], "alt": 2 * A0["alt"]}                  # CFG493's normalisation (record footings)
J886 = json.load(open(os.path.join(CFG, "CFG886_ratio_fret_without_planck", "cfg886_results.json")))
BG = {}
for lab, key in (("BAO+BBN (CFG886 T2a)", "T2a"), ("SH0ES h + BAO Om (CFG886 T2b, variant)", "T2b")):
    pr = J886[key]["primary"]
    BG[lab] = dict(h=pr["h"]["mean"], sh=pr["h"]["sd"], Om=pr["Om"]["mean"], sOm=pr["Om"]["sd"])
LN10 = math.log(10)
KAP = {}
for foot in ("canonical", "alt"):
    k_rec = 10 ** L0 / DEN_REC[foot]; sk_rec = k_rec * s0 * LN10
    KAP[foot] = dict(record=dict(kappa=k_rec, sigma=sk_rec, a0=10 ** L0, log_a0=L0, sigma_dex=s0))
    P(f"  [{foot}] record (Planck rho, HF at H0 67.4): a0 {10 ** L0:.4e} (log {L0:.4f} +- {s0:.4f}); kappa {k_rec:.4f} +- {sk_rec:.4f}")
    for lab, b in BG.items():
        Lc, sc, _ = gls(ROUTES, Lv0 + lev_HF * math.log10(b["h"] / 0.674))
        OmL_rec = 0.685 if foot == "canonical" else 1.0
        OmL_new = (1 - b["Om"]) if foot == "canonical" else 1.0
        den_new = DEN_REC[foot] * den(b["h"], OmL_new) / den(0.674, OmL_rec)
        k = 10 ** Lc / den_new
        # background error: d ln kappa = (HF-weighted lever - 1) d ln h  - 1/2 d ln OmL
        w_lev = float(np.dot(gls(ROUTES)[2], lev_HF))
        sbg = math.hypot((w_lev - 1.0) * b["sh"] / b["h"], (0.5 * b["sOm"] / (1 - b["Om"])) if foot == "canonical" else 0.0)
        sk = k * math.hypot(sc * LN10, sbg)
        shift = (k - k_rec) / sk_rec
        KAP[foot][lab] = dict(kappa=k, sigma=sk, a0=10 ** Lc, log_a0=Lc, sigma_dex=sc, bg_frac_err=sbg, shift_sigma=shift,
                              h=b["h"], Om=b["Om"], weighted_HF_lever=w_lev, pull_half=(0.5 - k) / sk, pull_Z4pi=(0.460659 - k) / sk)
        P(f"  [{foot}] {lab}: a0 {10 ** Lc:.4e} (log {Lc:.4f}); kappa {k:.4f} +- {sk:.4f}; shift {shift:+.2f} sigma_CFG493; "
          f"pull of 1/2 {(0.5 - k) / sk:+.2f}, of Z/4pi {(0.460659 - k) / sk:+.2f}" if foot == "canonical" else
          f"  [{foot}] {lab}: a0 {10 ** Lc:.4e} (log {Lc:.4f}); kappa_crit {k:.4f} +- {sk:.4f}; shift {shift:+.2f} sigma_CFG493; pull of 1/2 {(0.5 - k) / sk:+.2f}")
    KAP[foot]["line"] = "kappa ROBUST" if abs(KAP[foot]["BAO+BBN (CFG886 T2a)"]["shift_sigma"]) < 0.5 else "kappa SHIFTS"
    P(f"  [{foot}] LINE: {KAP[foot]['line']}")
# kernel bound: a0 under nu_L reproducing nu_mono's g_obs/g_bar at fixed g_bar
KB = {}
for y in (0.03, 0.072, 0.3):
    target = float(NU_MONO(y))
    # g_bar = y a0_ref; find a0' with nu_L(g_bar/a0') = target
    r = brentq(lambda f: float(nu_L(y / f)) - target, 0.3, 3.0)
    KB[str(y)] = dict(nu_mono=target, nu_L=float(nu_L(y)), a0_ratio_L_over_mono=r, dex=math.log10(r))
    P(f"  kernel bound at y={y}: nu_mono {target:.4f}, nu_L {float(nu_L(y)):.4f}; a0(nu_L)/a0(nu_mono) = {r:.4f} ({math.log10(r):+.4f} dex)")
RES["kappa"] = dict(record_and_clean=KAP, kernel_bound=KB,
                    note="kappa = a0/(c sqrt(G rho)); the raw-data fitted constant is a0 at the stated distance convention.")

# ============================================================================ PART B: L* (CFG820 / CFG821)
P("\n=== PART B: L* (CFG820 globular floor; CFG821 dSph ceiling, conditional)")
Gc, Msun, kpc, PCm = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16            # CFG820 constants (verbatim)
UPS_V, MW_MB, WID = 1.6, 6.0e10, 0.15
GC = json.load(open(os.path.join(CFG, "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))["clusters"]
GCP = [g for g in GC if g["name"] != "Pal 3"]
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])


def Sfun(s):                                                   # CFG691 screening table (framework-native point-mass solve)
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))


def wolf(M, rhl): return math.sqrt(Gc * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PCm)) / 1e3
def gext(R): return Gc * MW_MB * Msun / (R * kpc) ** 2


def gc_pred(g, a0, L, kern, efe, ups=UPS_V):
    M = ups * g["LV"]; sN = wolf(M, g["rhl"])
    y = Gc * (M * Msun / 2) / ((4.0 / 3.0) * g["rhl"] * PCm) ** 2 / a0 + (gext(g["RGC"]) / a0 if efe else 0.0)
    B = float(kern(y))
    if L is None: return sN
    rM = math.sqrt(Gc * M * Msun / a0) / PCm; lg = L ** 2 / (2 * rM); s = (4.0 / 3.0) * g["rhl"] / lg
    return sN * math.sqrt(1 + Sfun(s) * (B - 1))


vU = (math.log(10) * WID / 2) ** 2


def chi2_gc(gcs, a0, L, kern, efe, ups=UPS_V):
    return sum((math.log(g["so"]) - math.log(gc_pred(g, a0, L, kern, efe, ups))) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in gcs)


GRID = np.geomspace(5.75, 3000, 6000)


def floor95(gcs, a0, kern, efe, ups=UPS_V):
    c = np.array([chi2_gc(gcs, a0, L, kern, efe, ups) for L in GRID]); cN = chi2_gc(gcs, a0, None, kern, efe, ups)
    cmin = min(c.min(), cN); ok = np.where(c - cmin <= 3.84)[0]
    if len(ok) == 0: return float("nan"), cmin
    i = ok[0]
    if i == 0: return float(GRID[0]), cmin
    f = lambda L: chi2_gc(gcs, a0, L, kern, efe, ups) - cmin - 3.84
    return float(brentq(f, GRID[i - 1], GRID[i], xtol=1e-6)), cmin


LS = {}
LTH = {"canonical": 23.43, "alt": 19.38}                      # thermal L* (A76/D8), labelled premise values
for foot, a0 in A0.items():
    r0, _ = floor95(GCP, a0, nu_RAR, True)
    n1, c1 = floor95(GCP, a0, NU_NATIVE, False)
    n2, _ = floor95(GCP, a0, NU_NATIVE, True)
    up_, _ = floor95(GCP, a0, NU_NATIVE, False, UPS_V * 10 ** 0.15)
    dn_, _ = floor95(GCP, a0, NU_NATIVE, False, UPS_V * 10 ** -0.15)
    p_, _ = floor95(GCP, a0 * 1.05, NU_NATIVE, False); m_, _ = floor95(GCP, a0 / 1.05, NU_NATIVE, False)
    dlnL = (math.log(p_) - math.log(m_)) / (2 * math.log(1.05))
    dchi_th = chi2_gc(GCP, a0, LTH[foot], NU_NATIVE, False) - c1
    line = "L* FLOOR STABLE" if abs(math.log(n1 / r0)) <= 0.05 else "L* FLOOR MOVES"
    LS[foot] = dict(R0_record_machinery=r0, N1_native=n1, N2_native_plus_EFE_recipe=n2, N1_ups_plus=up_, N1_ups_minus=dn_,
                    dlnL95_dlna0=dlnL, dchi2_N1_at_thermal=dchi_th, thermal_Lstar=LTH[foot], line=line,
                    ln_ratio_N1_R0=math.log(n1 / r0))
    P(f"  [{foot}] L*_95: R0 (nu_RAR + EFE recipe) {r0:.3f} pc | N1 native (nu_L, no recipe) {n1:.3f} pc | N2 (nu_L + recipe, reported) {n2:.3f} pc")
    P(f"  [{foot}]   Upsilon_V x10^+0.15 -> {up_:.3f} pc; x10^-0.15 -> {dn_:.3f} pc; d ln L*_95/d ln a0 = {dlnL:+.3f}; "
      f"Delta chi2_N1 at thermal {LTH[foot]} pc = {dchi_th:.3f} ({'excluded' if dchi_th > 3.84 else 'allowed'}) -> {line}")
k3 = abs(LS["canonical"]["R0_record_machinery"] - 23.641) < 0.02 and abs(LS["alt"]["R0_record_machinery"] - 24.476) < 0.02
check("K3", k3, f"{LS['canonical']['R0_record_machinery']:.3f}/{LS['alt']['R0_record_machinery']:.3f}", "23.641/24.476 +-0.02",
      "CFG820 fine-grid floor reproduced (record machinery)")
# per-cluster boost under each machinery (canonical, L* -> 0)
BOOST = {}
for g in GCP:
    a0 = A0["canonical"]; M = UPS_V * g["LV"]
    yi = Gc * (M * Msun / 2) / ((4.0 / 3.0) * g["rhl"] * PCm) ** 2 / a0; ye = gext(g["RGC"]) / a0
    BOOST[g["name"]] = dict(y_int=yi, y_ext_recipe=ye, B_RAR_EFE=float(nu_RAR(yi + ye)), B_native_iso=float(NU_NATIVE(yi)))
    P(f"    {g['name']:9s} y_int {yi:.4f}, y_ext(recipe) {ye:.4f}: B_RAR+EFE {float(nu_RAR(yi + ye)):.3f}, B_L iso {float(NU_NATIVE(yi)):.3f}, "
      f"sigma_obs/sigma_N {g['so'] / wolf(M, g['rhl']):.3f}")
# CFG821 (conditional) with the native kernel, isolated
UPS_D = 2.0
DS = []


def fnum(x):
    try: return float(x)
    except Exception: return None


for r in csv.DictReader(open(os.path.join(ROOT, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))):
    MV, s_, es = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_em"))
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")); rgc = fnum(r.get("distance_gc"))
    if MV is None or s_ is None or rh is None or MV > -7.7 or r["name"] in ("LMC", "SMC", "Sagittarius"): continue
    DS.append(dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), so=s_, eso=es or 0.1 * s_, rhl=rh, RGC=rgc or 100.0))
D821 = {}
for foot, a0 in A0.items():
    c = np.array([chi2_gc(DS, a0, L, NU_NATIVE, False, UPS_D) for L in GRID]); c0 = chi2_gc(DS, a0, 1e-6, NU_NATIVE, False, UPS_D)
    cmin = min(c.min(), c0); ok = GRID[c - cmin <= 3.84]
    D821[foot] = dict(n=len(DS), chi2_unscreened=c0, L95_up=float(ok.max()) if len(ok) else float("nan"), chi2_min=float(cmin))
    P(f"  CFG821 native [{foot}] n={len(DS)}: chi2 unscreened {c0:.1f} for {len(DS)} dSphs; 95% upper L* {D821[foot]['L95_up']:.1f} pc "
      "(CONDITIONAL: no bound cold mass; reported only)")
RES["Lstar"] = dict(CFG820=LS, CFG821_native=D821, boosts_canonical=BOOST)

# ============================================================================ PART C: u (eRASS1 x KiDS MID band)
P("\n=== PART C: u (CFG687 eRASS1 x KiDS stack; D6/A21 inversion)")
G6, MSUN6, MPC6 = 6.674e-11, 1.989e30, 3.0857e22
KG = MSUN6 / (3.0857e16) ** 2
d = np.load(os.path.join(CFG, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
D, E, PLrec, PNrec, MG, ZC, RA, R500 = (d[k] for k in ("D", "E", "PL", "PN", "mg", "z", "ra", "R500"))
NCL = D.shape[0]
W = np.where((E > 0) & (E < 1e8), 1.0 / E ** 2, 0.0)
ORD = np.argsort(RA); PATCH = np.empty(NCL, int); PATCH[ORD] = np.arange(NCL) * 30 // NCL
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1]); MID = [3, 4, 5]
RGRID = np.logspace(-3, np.log10(30), 3000); RM = RGRID * MPC6; U_GRID = np.linspace(0, 1, 4001)
P(f"  {NCL} clusters; MID band = bins {MID}: R = {EDGES[3]:.3f}-{EDGES[6]:.3f} Mpc (fixed physical radii; centres "
  + ", ".join(f"{RC[j]:.3f}" for j in MID) + " Mpc). No r_sp, r200 or NFW quantity enters u_MID.")


def sigma_proj(rhoL, R):
    umax = np.arccosh(RGRID[-1] / R); uu = U_GRID * umax; rr = R * np.cosh(uu)
    pos = rhoL > 0
    rho_u = np.exp(np.interp(np.log(rr), np.log(RGRID[pos]), np.log(rhoL[pos])))
    return 2 * _trapz(rho_u * rr * MPC6, uu)


def dsigma(Mtot, rho, Rs):
    out = []
    for R in Rs:
        sel = RGRID > R; rr = RM[sel]
        M2 = np.interp(R, RGRID, Mtot) + _trapz(4 * np.pi * rr ** 2 * rho[sel] * (1 - np.sqrt(np.maximum(0.0, 1 - (R * MPC6 / rr) ** 2))), rr)
        out.append((M2 / (np.pi * (R * MPC6) ** 2) - sigma_proj(rho, R)) / KG)
    return np.array(out)


def baryon(R500i, Mgas, beta=2 / 3, rcf=0.15, fs=0.20):     # CFG687's model, verbatim convention
    rc = rcf * R500i; shape = (1 + (RGRID / rc) ** 2) ** (-1.5 * beta); shape[RGRID > 3.0] = 0.0
    dm = 4 * np.pi * RM ** 2 * shape
    M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]
    return M * (Mgas * MSUN6 / np.interp(R500i, RGRID, M)) * (1 + fs)


def rho_of(M): return np.gradient(M, RM) / (4 * np.pi * RM ** 2)


def model(a0, kern, mg=MG, r500=R500, fs=0.20, rc_bins=RC):
    PL_, PN_ = [], []
    for i in range(NCL):
        Mb = baryon(r500[i], mg[i], fs=fs); gb = G6 * Mb / RM ** 2
        ML = gb * kern(gb / a0) * RM ** 2 / G6
        PL_.append(dsigma(ML, rho_of(ML), rc_bins[MID])); PN_.append(dsigma(Mb, rho_of(Mb), rc_bins[MID]))
    return np.array(PL_), np.array(PN_)


DM = D[:, MID]; WM = W[:, MID]


def u_mid(PL_, PN_, Dm=DM):
    def f(mask):
        return ((WM[mask] * PL_[mask]).sum() - (WM[mask] * PN_[mask]).sum()) / ((WM[mask] * Dm[mask]).sum() - (WM[mask] * PN_[mask]).sum())
    full = f(np.ones(NCL, bool)); reps = np.array([f(PATCH != p) for p in range(30)])
    return float(full), float(np.sqrt(29 / 30 * np.sum((reps - reps.mean()) ** 2)))


U = {}
BASE = {}
for foot, a0 in A0.items():
    PLm, PNm = model(a0, NU_MONO); BASE[foot] = (PLm, PNm)
    U[foot] = dict(record_kernel=u_mid(PLm, PNm))
k4 = abs(U["canonical"]["record_kernel"][0] - 0.47157) < 1e-3 and abs(U["alt"]["record_kernel"][0] - 0.5234) < 2e-3
check("K4", k4, f"{U['canonical']['record_kernel'][0]:.5f}/{U['alt']['record_kernel'][0]:.4f}", "0.47157(1e-3)/0.5234(2e-3)",
      "D6 u_MID reproduced (nu_mono, record conventions)")
hB = BG["BAO+BBN (CFG886 T2a)"]["h"]; fh = hB / 0.674
for foot, a0 in A0.items():
    u0, su0 = U[foot]["record_kernel"]
    runs = {}
    runs["native kernel nu_L [A1]"] = u_mid(*model(a0, NU_NATIVE))
    runs["a0 x1.05"] = u_mid(*model(a0 * 1.05, NU_MONO)); runs["a0 /1.05"] = u_mid(*model(a0 / 1.05, NU_MONO))
    runs["M_gas x1.10 (survey)"] = u_mid(*model(a0, NU_MONO, mg=MG * 1.10))
    runs["R500 x10^+0.033 (LCDM-processed)"] = u_mid(*model(a0, NU_MONO, r500=R500 * 10 ** 0.033))
    runs["R500 x10^-0.033 (LCDM-processed)"] = u_mid(*model(a0, NU_MONO, r500=R500 * 10 ** -0.033))
    runs["f_s 0.10 (external)"] = u_mid(*model(a0, NU_MONO, fs=0.10)); runs["f_s 0.30 (external)"] = u_mid(*model(a0, NU_MONO, fs=0.30))
    runs["background Planck->BAO+BBN (LCDM-processed, 1st order)"] = u_mid(*model(a0, NU_MONO, mg=MG * fh ** -2.5, r500=R500 / fh, rc_bins=RC / fh), Dm=DM * fh)
    dlnu = (math.log(runs["a0 x1.05"][0]) - math.log(runs["a0 /1.05"][0])) / (2 * math.log(1.05))
    dlnu_mg = math.log(runs["M_gas x1.10 (survey)"][0] / u0) / math.log(1.10)
    lcdm_keys = [k for k in runs if "LCDM-processed" in k]
    max_lcdm = max(abs(runs[k][0] - u0) for k in lcdm_keys)
    d_kern = abs(runs["native kernel nu_L [A1]"][0] - u0)
    line = "u CLEAN" if (max_lcdm < su0 and d_kern < su0) else "u CONTAMINATION-SENSITIVE"
    U[foot].update(runs={k: dict(u=v[0], sigma=v[1], shift=v[0] - u0, shift_sigma=(v[0] - u0) / su0) for k, v in runs.items()},
                   dlnu_dlna0=dlnu, dlnu_dlnMgas=dlnu_mg, max_LCDM_shift=max_lcdm, kernel_shift=d_kern, line=line)
    P(f"  [{foot}] u_MID (record kernel nu_mono) = {u0:.4f} +- {su0:.4f}")
    for k, v in runs.items():
        P(f"  [{foot}]   {k:52s}: {v[0]:.4f} +- {v[1]:.4f}  (shift {v[0] - u0:+.4f} = {(v[0] - u0) / su0:+.2f} sigma)")
    P(f"  [{foot}]   d ln u/d ln a0 = {dlnu:+.3f}; d ln u/d ln M_gas = {dlnu_mg:+.3f}; max LCDM-bracket shift {max_lcdm:.4f}; "
      f"kernel shift {d_kern:.4f} -> {line}")
RES["u"] = {f: dict(u_MID_record=U[f]["record_kernel"], **{k: v for k, v in U[f].items() if k != "record_kernel"}) for f in U}
RES["u_band_Mpc"] = [float(EDGES[3]), float(EDGES[6])]

# ============================================================================ PART D: Jacobian
P("\n=== PART D: dependency structure -- Jacobian of observables w.r.t. (ln a0, ln L*, ln u), canonical footing")
a0c = A0["canonical"]; Lref = 30.0; uref = RES["u"]["canonical"]["runs"]["native kernel nu_L [A1]"]["u"]


def gal_obs(la0, lL, lu, M=1e10, r_kpc=10.0):
    a0 = math.exp(la0); L = math.exp(lL)
    gN = Gc * M * Msun / (r_kpc * kpc) ** 2
    rM = math.sqrt(Gc * M * Msun / a0) / PCm; lg = L ** 2 / (2 * rM); s = r_kpc * 1e3 / lg
    return math.log(gN * (1 + Sfun(s) * (float(NU_NATIVE(gN / a0)) - 1)))


def gc_obs(name):
    g = [x for x in GCP if x["name"] == name][0]
    return lambda la0, lL, lu: math.log(gc_pred(g, math.exp(la0), math.exp(lL), NU_NATIVE, False))


PLn_c, PNn_c = model(a0c, NU_NATIVE)
PLp, PNp = model(a0c * 1.01, NU_NATIVE); PLq, PNq = model(a0c / 1.01, NU_NATIVE)
Mcl = float(np.median(MG)) / 0.11                               # representative M500 for the cluster screening term


def cl_obs(la0, lL, lu):
    a0 = math.exp(la0); L = math.exp(lL); u = math.exp(lu)
    if abs(la0 - math.log(a0c)) < 1e-12: PL_, PN_ = PLn_c, PNn_c
    elif la0 > math.log(a0c): PL_, PN_ = PLp, PNp
    else: PL_, PN_ = PLq, PNq
    rM = math.sqrt(Gc * Mcl * Msun / a0) / PCm; lg = L ** 2 / (2 * rM); s = 0.8e6 / lg
    S = Sfun(s)
    return math.log((WM * (PN_ + S * (PL_ - PN_) / u)).sum() / WM.sum())


ROWS = [("galaxy g (1e10 Msun, 10 kpc)", gal_obs), ("NGC 2419 sigma", gc_obs("NGC 2419")), ("Pal 14 sigma", gc_obs("Pal 14")),
        ("cluster MID DeltaSigma", cl_obs)]
x0 = np.array([math.log(a0c), math.log(Lref), math.log(uref)])
steps = [math.log(1.01), 1e-3, 1e-3]
Jm = np.zeros((len(ROWS), 3))
for i, (lab, f) in enumerate(ROWS):
    for j in range(3):
        xp = x0.copy(); xm = x0.copy(); xp[j] += steps[j]; xm[j] -= steps[j]
        Jm[i, j] = (f(*xp) - f(*xm)) / (2 * steps[j])
    P(f"  {lab:30s}: d/dln a0 {Jm[i, 0]:+.4f}  d/dln L* {Jm[i, 1]:+.3e}  d/dln u {Jm[i, 2]:+.4f}")
sv = np.linalg.svd(Jm, compute_uv=False); rank = int(np.sum(sv > 1e-3 * sv[0]))
P(f"  singular values {', '.join(f'{x:.4g}' for x in sv)}; rank {rank} of 3 (tol 1e-3 x largest)")
k6 = Jm[0, 2] == 0.0 and Jm[1, 2] == 0.0 and Jm[2, 2] == 0.0 and abs(Jm[3, 1]) < 1e-3
check("K6", k6, f"u-col gal/gc {Jm[0, 2]:.1e},{Jm[1, 2]:.1e},{Jm[2, 2]:.1e}; L*-col cluster {Jm[3, 1]:.1e}", "0,0,0; <1e-3",
      "Jacobian structural zeros")
# screening variable: s = (8/3) r_h r_M / L*^2, r_M ∝ a0^-1/2  -> at fixed s, d ln L*/d ln a0 = -1/4 (analytic)
RES["jacobian"] = dict(rows=[r[0] for r in ROWS], params=["ln a0", "ln L*", "ln u"], J=Jm.tolist(), singular_values=sv.tolist(),
                       rank=rank, point=dict(a0=a0c, Lstar_pc=Lref, u=uref),
                       screening_fixed_s_dlnL_dlna0=-0.25,
                       measured_dlnL95_dlna0={f: LS[f]["dlnL95_dlna0"] for f in LS},
                       measured_dlnu_dlna0={f: U[f]["dlnu_dlna0"] for f in U})
P(f"  measurement coupling: d ln L*_95/d ln a0 = {LS['canonical']['dlnL95_dlna0']:+.3f} (canonical) / {LS['alt']['dlnL95_dlna0']:+.3f} (alt); "
  f"screening-only (fixed s) = -0.250; d ln u_MID/d ln a0 = {U['canonical']['dlnu_dlna0']:+.3f} / {U['alt']['dlnu_dlna0']:+.3f}")

# ============================================================================ PART E: forced relations (record-based classification)
FR = [
    dict(rel="L* = sigma_c^2/a0", cls="POSIT", src="A76/A65 premise; D8: not in the action, no tethered-state term; D8b: sigma not one constant"),
    dict(rel="I(y_t) = 8 pi/kappa^2", cls="POSIT (P5 closure)", src="D7: one-to-one relabelling of kappa; y_t has no independent observable today"),
    dict(rel="u = f(a0) or f(L*)", cls="NONE in the action", src="P4 is a posit on the cold sector; no action term carries u (THEORY P4; D6 H-VR is a new posit). "
         "The measured u_MID depends on a0 through the inversion (Part C), a measurement coupling, not a relation."),
    dict(rel="eta = gamma", cls="NOT FORCED", src="A69/A77: action invariant for arbitrary (eta, gamma)"),
    dict(rel="screening variable s = (8/3) r_h r_M / L*^2", cls="FORCED combination (reparametrisation)",
         src="gamma = K L*^2/2 with saturation scale a0/K: L* enters observables only via L*^2 a0^(1/2) at fixed system; "
             "it fixes the degeneracy direction d ln L*/d ln a0 = -1/4 at fixed s, removes no constant, and predicts no new number"),
]
RES["forced_relations"] = FR
P("\n=== PART E: forced relations among (kappa, L*, u)")
for f in FR:
    P(f"  {f['rel']:45s} -> {f['cls']}: {f['src']}")
P("  => no relation among kappa, L* and u follows from the action without inserting a number. LEE / second prediction: not applicable.")

# ============================================================================ POST-RESULT additions (reported only; never a line or a check)
P("\n=== POST-RESULT (added after the first run; reported only, no line or check depends on it)")
a0_clean = KAP["canonical"]["BAO+BBN (CFG886 T2a)"]["a0"]; sdex_clean = KAP["canonical"]["BAO+BBN (CFG886 T2a)"]["sigma_dex"]
u_at_clean = u_mid(*model(a0_clean, NU_NATIVE))
POST = dict(a0_clean=a0_clean, sigma_dex_clean=sdex_clean, u_native_at_clean_a0=u_at_clean)
P(f"  galaxy-measured a0 (clean background, footing-free) = {a0_clean:.4e} m/s^2 (+-{sdex_clean:.4f} dex)")
P(f"  u_MID (native kernel) at that a0 = {u_at_clean[0]:.4f} +- {u_at_clean[1]:.4f} (stat)")
for foot in ("canonical", "alt"):
    R = U[foot]["runs"]
    half = lambda a, b: 0.5 * abs(R[a]["u"] - R[b]["u"])
    sys_terms = {"R500 (LCDM-processed)": half("R500 x10^+0.033 (LCDM-processed)", "R500 x10^-0.033 (LCDM-processed)"),
                 "f_s (external)": half("f_s 0.10 (external)", "f_s 0.30 (external)"),
                 "M_gas 10% (survey)": abs(R["M_gas x1.10 (survey)"]["shift"]),
                 "background (LCDM-processed)": abs(R["background Planck->BAO+BBN (LCDM-processed, 1st order)"]["shift"])}
    sq = math.sqrt(sum(v ** 2 for v in sys_terms.values()))
    kap_prop = U[foot]["dlnu_dlna0"] * sdex_clean * LN10 * R["native kernel nu_L [A1]"]["u"]
    POST[f"u_sys_{foot}"] = dict(terms=sys_terms, quadrature=sq, from_a0_error=kap_prop)
    P(f"  [{foot}] u systematic brackets in quadrature = {sq:.4f} (stat {U[foot]['record_kernel'][1]:.4f}); "
      f"u error carried from the galaxy a0 error ({sdex_clean:.4f} dex) = {kap_prop:.4f}")
    Ls = LS[foot]
    POST[f"Lstar_floor_span_{foot}"] = dict(native_iso=Ls["N1_native"], native_recipe=Ls["N2_native_plus_EFE_recipe"],
                                             ups_minus=Ls["N1_ups_minus"], ups_plus=Ls["N1_ups_plus"])
    P(f"  [{foot}] L*_95 floor: EFE treatment {Ls['N2_native_plus_EFE_recipe']:.1f}-{Ls['N1_native']:.1f} pc; "
      f"coherent Upsilon_V +-0.15 dex {Ls['N1_ups_minus']:.1f}-{Ls['N1_ups_plus']:.1f} pc")
RES["post_result_reported_only"] = POST

# ============================================================================ verdict
lines = [KAP["canonical"]["line"], KAP["alt"]["line"], LS["canonical"]["line"], LS["alt"]["line"], U["canonical"]["line"], U["alt"]["line"]]
crisp = any(x in ("kappa SHIFTS", "L* FLOOR MOVES", "u CONTAMINATION-SENSITIVE") for x in lines)
RES["lines"] = lines
RES["verdict_mapping"] = "CRISP FINDING" if crisp else "SCOPED NO-GO (unless a record error is listed in the README)"
P(f"\nLINES: {lines}")
P(f"VERDICT (frozen mapping, script part): {RES['verdict_mapping']}")
npass = sum(c["pass_"] for c in CHECKS)
P(f"{LANE} COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
RES["checks"] = CHECKS
json.dump(RES, open(os.path.join(HERE, f"e4_fitted_three_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"e4_fitted_three{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
