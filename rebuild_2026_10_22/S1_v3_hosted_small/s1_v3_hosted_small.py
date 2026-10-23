#!/usr/bin/env python3
"""S1_v3_hosted_small -- batch R1 of N0: v3's small systems in their host's field.
Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (committed alone first, 25c5861b57).

Tile 26 (dwarf satellites, E3's 45/46) and tile 29 (Coma UDGs, CFG933's 9) are solved with v3's static equation
(stiffened AQUAL, mu = x/(1+x), L* stiffness) as Plummer spheres in a uniform TOTAL host field, the response solved
(D10's solver, imported read-only; F2's AQUAL solver as the independent cross-check).  Chain, one step at a time:
kernel -> geometry (AQUAL solve) -> EFE -> native screening (= v3) -> mu_K^2 bound -> native H0.
Tile 19 (TDGs, DF2/DF4) is lane P4's and is not computed here.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 s1_v3_hosted_small.py            (-> .out, _results.json, CSVs)
      OMP_NUM_THREADS=1 nice -n 15 python3 s1_v3_hosted_small.py --mutate   (checks only; the solver background is the
                                                                             Newtonian y_e instead of the total x_e)
Deterministic (seeded), no network.  kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import csv, json, math, os, resource, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing"))
import d10_solver as S   # noqa: E402  (read-only)
import f2_aqual as F2    # noqa: E402  (read-only)

MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(k, ok, val, thr, what):
    CHK[k] = dict(ok=bool(ok), value=val, threshold=thr, what=what)
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")

# ------------------------------------------------------------------ constants
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16       # E3's
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LFLOOR = {"canonical": 21.68, "alt": 22.85}                        # D10 central L*_95
def LSETS(f): return [("floor", LFLOOR[f]), ("24", 24.0), ("90", 90.0)]
A_H = 3.0 * KPC
GE2_8KPC = 2.0592e-10                                             # D10 / D7b: E2 kinematic total at 8 kpc
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
MUK = 14.8 * 0.6856 / (1e3 * KPC)                                 # BS24 Eq. 39 cap, h = 0.6856 (F3/L1 model B), 1/m
NMC, NBOOT = 2000, 4000
DY, DL = 0.6, 0.3                                                 # MC grid half-widths (dex) in y and Lambda
FW_N = 2.0 * (4 / 3) ** 3 / (1 + (4 / 3) ** 2) ** 1.5            # Plummer M(<r12)/(M/2): Newtonian E-W vs E3's g_bar
FV_N = math.pi / 4.0                                              # Plummer Newtonian E-V vs E3's g_bar
R12 = 4.0 / 3.0

# ------------------------------------------------------------------ solver wrappers
GR = S.Grid2D(nper=24, Nt=16)
WORST = [0.0]; NSOLVE = [0]
def bg(xe):
    return (xe * xe / (1 + xe)) if (MUT and xe > 0) else xe        # MUTATE: Newtonian y_e passed as the total field

def solve(y, xe, Lam, grid=None, tol=1e-10, track=True):
    grid = GR if grid is None else grid
    iso = xe <= 0
    sv = S.Solver2D(grid, y, 0.0 if iso else bg(xe), Lam, isolated=iso)
    U, res, it = sv.solve(tol=tol)
    if track:
        WORST[0] = max(WORST[0], res); NSOLVE[0] += 1
    rf, gr = sv.field_monopole()
    _, vir, wo = S.jeans(rf, gr, [])
    return dict(rf=rf, gr=gr, vir=vir, wo=wo, res=res)

def logG(y, xe, Lam):
    """log10 of g_pred / g_bar(E3 convention: G(M/2)/r12^2) for E-W and E-V; solver units a = 1, a0 = 1."""
    d = solve(y, xe, Lam)
    return math.log10(6 * d["wo"] * R12 / y), math.log10(6 * d["vir"] * R12 / y)

def law_logG(y):
    """isolated algebraic law through the same Jeans machinery (reference for K2)."""
    rf = GR.re[1:-1]; gl = S.law_v(S.plummer_gN(rf, y)); _, vir, wo = S.jeans(rf, gl, [])
    return math.log10(6 * wo * R12 / y), math.log10(6 * vir * R12 / y)

def lin3(x, xs, v):
    """piecewise-linear interpolation on 3 nodes with linear extrapolation (vectorised over x)."""
    x = np.asarray(x, float)
    s0 = (v[1] - v[0]) / (xs[1] - xs[0]); s1 = (v[2] - v[1]) / (xs[2] - xs[1])
    return np.where(x < xs[1], v[1] + s0 * (x - xs[1]), v[1] + s1 * (x - xs[1]))

def interp2(ly, lL, ys, Ls, T):
    """T[iy, iL] on 3x3 nodes -> value at (ly, lL) arrays: along Lambda first, then y."""
    rows = [lin3(lL, Ls, T[i]) for i in range(3)]
    s0 = (rows[1] - rows[0]) / (ys[1] - ys[0]); s1 = (rows[2] - rows[1]) / (ys[2] - ys[1])
    return np.where(ly < ys[1], rows[1] + s0 * (ly - ys[1]), rows[1] + s1 * (ly - ys[1]))

# ------------------------------------------------------------------ host fields
def g_host(R_m, Mb, a0):
    gN = G * Mb * MSUN / (R_m + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
def Mb_hi(a0):
    gN = GE2_8KPC ** 2 / (GE2_8KPC + a0)
    return gN * (8 * KPC + A_H) ** 2 / G / MSUN
def host_mass(host, ek, a0):
    base = MHOST[host]
    frac = {"E_lo": 4.0e10 / 6.0e10, "E_mid": 1.0, "E_hi": Mb_hi(a0) / 6.0e10}[ek]
    return base * frac
def rho_host_local(R_m, Mb, a0):
    """phantom-inclusive local dynamical density of the law field: (1/4 pi G r^2) d(r^2 g)/dr."""
    h = 1e-4 * R_m
    f = lambda r: r * r * g_host(r, Mb, a0)
    return (f(R_m + h) - f(R_m - h)) / (2 * h) / (4 * math.pi * G * R_m * R_m)

KEV, MP = 1.602176634e-16, 1.67262e-27
BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6)                  # L23 / CFG948 constants
CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP)
KPC_C = 3.0857e19                                                 # CFG933/L23 kpc
def g_beta(d_kpc):
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB * r / (r * r + rc * rc)
def rho_beta(d_kpc):
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB / (4 * math.pi * G) * (r * r + 3 * rc * rc) / (r * r + rc * rc) ** 2

R = dict(lane="S1_v3_hosted_small", mutate=MUT, frozen="25c5861b57",
         constants=dict(G=G, MSUN=MSUN, PC=PC, a0=A0, L_floor=LFLOOR, mu_K_per_m=MUK, NMC=NMC, NBOOT=NBOOT, DY=DY, DL=DL,
                        FW_N=FW_N, FV_N=FV_N, beta_model=BETA, MHOST=MHOST))
P("=" * 110)
P("S1_v3_hosted_small: v3 small systems in their host's field (tiles 26, 29)" + ("   *** MUTATE: Newtonian y_e as the background ***" if MUT else ""))
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled; tile 19 is lane P4's")
P("=" * 110)

# ================================================================== VALIDATION CHECKS K2-K6 (solver)
P("\n--- solver validation (D10 solver read-only; F2 AQUAL read-only) ---")
k2 = []
for y in (3e-4, 3e-3, 3e-2):
    d = solve(y, 0.0, 0.0, track=False); lw, lv = law_logG(y)
    a, b = abs(10 ** (0.5 * (math.log10(6 * d["wo"] * R12 / y) - lw)) - 1), abs(10 ** (0.5 * (math.log10(6 * d["vir"] * R12 / y) - lv)) - 1)
    k2.append(max(a, b)); P(f"   K2 y {y:.0e}: |d sigma/sigma| E-W {a:.2e} E-V {b:.2e} (res {d['res']:.1e})")
check("K2", max(k2) < 2e-3, f"{max(k2):.2e}", "< 2e-3", "isolated L*=0 2D solve vs the algebraic law (E-W, E-V)")

k3 = []
for xe in (0.1, 0.5):
    y = 100.0
    d = solve(y, xe, 0.0, track=False)
    ye = xe * xe / (1 + xe)
    f2 = F2.solve_efe(ye)
    for s in (3.0, 10.0):
        ra = s * math.sqrt(y)
        Md10 = ra * ra * float(np.interp(math.log(ra), np.log(d["rf"]), d["gr"])) / y
        Mf2 = float(np.interp(math.log(s), np.log(f2["r"]), f2["M"]))
        k3.append(abs(Md10 / Mf2 - 1))
        P(f"   K3 x_e {xe} (F2 y_e {ye:.4f}, x_e {f2['x_e']:.4f}, it {f2['iters']}) r/r_M {s}: M_eff D10 {Md10:.5f} F2 {Mf2:.5f} rel {k3[-1]:.2e}")
check("K3", max(k3) < 2e-2, f"{max(k3):.2e}", "< 2e-2", "embedded AQUAL: D10 2D vs F2's independent point-mass AQUAL solver (angle-averaged M_eff)")

k4 = []
for xe in (0.05, 0.5):
    for Lam in (0.0, 0.5, 2.0):
        y = 1e-4 * xe
        d = solve(y, xe, Lam, tol=1e-14, track=False)
        Fv, newt = S.routeF_monopole(y, xe, Lam, 1.0)
        g2 = float(np.interp(0.0, np.log(d["rf"]), d["gr"]))
        k4.append(abs(g2 / Fv - 1)); P(f"   K4 x_e {xe} Lam {Lam}: 2D {g2:.6e} Route F {Fv:.6e} rel {k4[-1]:.2e}")
check("K4", max(k4) < 2e-2, f"{max(k4):.2e}", "< 2e-2", "linear EFE: D10 2D monopole at r = a vs Route F (C6 kernel)")

k5 = []
FINE, FAR = S.Grid2D(nper=48, Nt=32), S.Grid2D(nper=24, Nt=16, rout=1e5)
for (y, xe, Lam, lab) in ((3e-3, 0.1, 0.3, "UFD-like"), (0.03, 0.6, 0.02, "UDG-like")):
    b = solve(y, xe, Lam, track=False); fn = solve(y, xe, Lam, grid=FINE, track=False); fa = solve(y, xe, Lam, grid=FAR, track=False)
    dd = [abs(math.sqrt(o[k] / b[k]) - 1) for o in (fn, fa) for k in ("wo", "vir")]
    k5.append(max(dd)); P(f"   K5 {lab}: max |d sigma/sigma| (fine, far; E-W, E-V) {max(dd):.2e}")
check("K5", max(k5) < 5e-3, f"{max(k5):.2e}", "< 5e-3", "convergence: grid doubling and r_out x 10")

d = solve(3e-3, 0.1, 1e4, track=False)
_, virN, woN = S.jeans(d["rf"], S.plummer_gN(d["rf"], 3e-3), [])
k6 = max(abs(math.sqrt(d["wo"] / woN) - 1), abs(math.sqrt(d["vir"] / virN) - 1))
check("K6", k6 < 2e-3, f"{k6:.2e}", "< 2e-3", "Newton limit Lambda = 1e4 (x_e 0.1, y 3e-3)")
R["validation"] = dict(K2=k2, K3=k3, K4=k4, K5=k5, K6=k6)

# ================================================================== SATELLITE DATA (E3's code path, own implementation)
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
def load_lvd():
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s,
                             sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s, ul=bool(r.get("vlos_sigma_ul")),
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance"))))
    return rows
ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
def sample(a0):
    mcrit = a0 * (24.0 * PC) ** 2 / G / MSUN
    return [r for r in ALL if r["logms"] < math.log10(mcrit)]
SAMP = {f: sample(A0[f]) for f in FOOTS}
RNG = np.random.default_rng(20261023)
def split_normal(c, em, ep, n):
    z = RNG.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False):
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC)); Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl, gu
        b = 1.0
        if binmode == "free": b = arr_free.get(r["name"], med_free)
        elif binmode == "f07": b = arr_f07.get(r["name"], med_f07)
        fD = 10 ** (split_normal(0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar); Md[i] = gobs * r12 ** 2 / G / MSUN; Ms_[i] = ms
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, Md=Md, Ms=Ms_, rows=keep)
def boot_ix(N):
    return RNG.integers(0, N, (NBOOT, N)), RNG.integers(0, NMC, (NBOOT, N))
def boot_median(X, ix):
    idx, col = ix
    meds = np.median(X[idx, col], axis=1)
    return float(np.median(meds)), float(np.std(meds))

# ---- E3's CFG691 recipe (K1 reproduction)
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-30); return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))
def Sfun(s):
    s = np.asarray(s, float)
    out = np.interp(np.log(np.clip(s, 0.01, 1000)), np.log(ST_s), ST_S)
    out = np.where(s <= 0.01, s / 2, out)
    return np.where(s >= 1000, 1 - 1 / np.maximum(s, 1e-300), out)
def B_scr(Ms, r12, a0, Lst):
    gb = G * (Ms / 2) * MSUN / r12 ** 2; nv = nu1(gb / a0)
    if Lst is None: return nv
    rM = np.sqrt(G * Ms * MSUN / a0); lg = (Lst * PC) ** 2 / (2 * rM)
    return 1 + Sfun(r12 / lg) * (nv - 1)

DATASETS = {}
for f in FOOTS:
    a0 = A0[f]
    DATASETS[(f, "primary")] = build(SAMP[f], a0)
    DATASETS[(f, "raw")] = build(SAMP[f], a0, binmode="none")
    DATASETS[(f, "W")] = build(SAMP[f], a0, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True)
BOOT = {k: boot_ix(len(v["rows"])) for k, v in DATASETS.items()}

P("\n--- K1: E3 reproduced with this lane's own code (CFG691 recipe, isolated) ---")
E3REF = {"canonical": dict(L24=0.886, L90=1.518, law=0.557, EN=2.013), "alt": dict(L24=0.846, L90=1.489, law=0.508, EN=1.998)}
k1, S0 = [], {}
for f in FOOTS:
    X = DATASETS[(f, "primary")]; ix = BOOT[(f, "primary")]
    Ms = X["Ms"]; r12 = R12 * 10 ** X["la"] * PC
    vals = {}
    for lab, Lst in (("L24", 24.0), ("L90", 90.0), ("law", None)):
        vals[lab] = boot_median(X["lb"] - np.log10(B_scr(Ms, r12, A0[f], Lst)), ix)
    vals["EN"] = boot_median(X["lb"], ix)
    S0[f] = vals
    for lab in ("L24", "L90", "law", "EN"):
        k1.append(abs(vals[lab][0] - E3REF[f][lab]))
    P(f"   {f:9s} N {len(X['rows'])}: above CFG691 L*24 {vals['L24'][0]:+.3f}+-{vals['L24'][1]:.3f}, L*90 {vals['L90'][0]:+.3f}, "
      f"law {vals['law'][0]:+.3f}; clean E_N {vals['EN'][0]:+.3f}")
nok = len(SAMP["canonical"]) == 45 and len(SAMP["alt"]) == 46
check("K1", nok and max(k1) <= 0.02, f"N {len(SAMP['canonical'])}/{len(SAMP['alt'])}; max |diff| {max(k1):.3f} dex", "45/46 and <= 0.02",
      "E3 reproduced (own code): Delta above CFG691 recipe L*24/90, unscreened law; clean E_N")
R["K1_E3"] = {f: {k: list(v) for k, v in S0[f].items()} for f in FOOTS}

# ================================================================== COMA DATA (CFG933's admission) + K7/K8
_rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "freundlich2022_coma_udgs.tsv"), encoding="utf-8")
         if l.strip() and not l.startswith("#")]
_hd = {h: i for i, h in enumerate(_rows[0])}
COMA = []
for r in _rows[1:]:
    g_ = lambda k: float(r[_hd[k]])
    Ms = g_("L_1e8") * 1e8 * g_("ML"); Re = g_("Re_kpc")
    adm = (Re >= 1.5) and (3e7 <= Ms <= 3e8)
    COMA.append(dict(name=r[_hd["name"]], Ms=Ms, Re=Re, sig=g_("sig"), esig=g_("esig"), dproj=g_("d_kpc"), dmean=g_("dmean_kpc"), admit=adm))
EXPECT = {"DFX1", "J125848.94+281037.1", "J125904.20+281507.7", "J125929.89+274303.0", "J125937.23+274815.2", "J130005.40+275333.0",
          "J130026.26+272735.2", "J130028.34+274820.5", "J130038.63+272835.3"}
ADM = [c for c in COMA if c["admit"]]
G_, MSUN_, PC_ = 6.674e-11, 1.989e30, 3.0857e16                   # CFG933's constants for the sealed estimator
def nu_e(y): return 1.0 / (-np.expm1(-np.sqrt(np.asarray(y, float))))
def coma_old(c, a0, mfac=1.0, dfac=1.0, sfac=1.0, kern="e"):
    Ms = c["Ms"] * mfac * dfac ** 2; Re = c["Re"] * dfac; sig = c["sig"] * sfac; e = c["esig"] * sfac
    r12 = R12 * Re * 1e3 * PC_; gb = G_ * (Ms / 2) * MSUN_ / r12 ** 2
    nv = float(nu_e(gb / a0)) if kern == "e" else float(nu1(gb / a0))
    sl = math.sqrt(r12 * gb * nv / 3) / 1e3
    return 2 * math.log(sig / sl), 2 * e / sig
def se_conv(E, sE):
    n = len(E); t_sd = float(np.std(E, ddof=1) / math.sqrt(n)); t_me = float(math.sqrt(np.sum(np.asarray(sE) ** 2)) / n)
    return max(t_sd, t_me)
R933 = json.load(open(os.path.join(CFG, "CFG933_udg_sealed_test", "cfg933_results.json")))
R948 = json.load(open(os.path.join(CFG, "CFG948_nocapture_vs_udgs", "cfg948_results.json")))
k7, k8 = [], []
P("\n--- K7/K8: CFG933 and CFG948 reproduced (isolated nu_e law) ---")
for f in FOOTS:
    ref = {p["name"]: p["E_obs"] for p in R933["byfoot"][f]["per_galaxy"] if p.get("pop") == "Coma"}
    Es = [coma_old(c, A0[f]) for c in ADM]
    for c, (E, _) in zip(ADM, Es):
        k7.append(abs(E - ref[c["name"]]))
    mE = float(np.mean([e for e, _ in Es])); se = se_conv([e for e, _ in Es], [s for _, s in Es])
    sm = R933["byfoot"][f]["primary"]["samples"]["coma"]
    k7 += [abs(mE - sm["mean_Eobs"]) * 1e-3, abs(se - sm["se_obs"]) * 1e-3]   # scaled so the 1e-6 line maps to 1e-9
    def mean_var(**kw): return float(np.mean([coma_old(c, A0[f], **kw)[0] for c in ADM]))
    sM = abs(mean_var(mfac=10 ** 0.2) - mean_var(mfac=10 ** -0.2)) / 2
    sA = abs(mean_var(sfac=1.15) - mean_var(sfac=1 / 1.15)) / 2
    sD = abs(mean_var(dfac=1.05) - mean_var(dfac=0.95)) / 2
    su = R948["byfoot"][f]["primary"]["sys_up"]
    k8 += [abs(sM - su["s_M"]), abs(sA - su["s_A"]), abs(sD - su["s_D"])]
    P(f"   {f:9s} <E> {mE:+.6f} (CFG933 {sm['mean_Eobs']:+.6f}) se {se:.6f} ({sm['se_obs']:.6f}); sigma_sys s_M {sM:.4f} ({su['s_M']:.4f}) "
      f"s_A {sA:.4f} ({su['s_A']:.4f}) s_D {sD:.4f} ({su['s_D']:.4f})")
memok = {c["name"] for c in ADM} == EXPECT
check("K7", memok and max(k7) <= 1e-9, f"membership {'==' if memok else '!='} CFG933; max |diff| {max(k7):.1e}", "<= 1e-9 (mean/se <= 1e-6)",
      "CFG933 per-galaxy E_obs, <E>, se_obs reproduced (isolated nu_e, Wolf)")
check("K8", max(k8) <= 2e-3, f"{max(k8):.1e}", "<= 2e-3", "CFG948 sigma_sys components s_M, s_A, s_D reproduced (isolated nu_e)")

if MUT:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
    check("K10", rss < 1.0, f"{rss:.3f} GB", "< 1 GB", "peak RSS")
    npass = sum(v["ok"] for v in CHK.values())
    P(f"\nS1_V3_HOSTED_SMALL COMPLETE: {npass}/{len(CHK)} checks PASS.  (MUTATE: checks only)  {time.time() - T0:.0f} s")
    R["checks"] = CHK
    json.dump(R, open(os.path.join(HERE, f"s1_v3_hosted_small_results{SFX}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"s1_v3_hosted_small{SFX}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if npass == len(CHK) else 1)

# ================================================================== SATELLITES: per-system native tables
P("\n--- satellites: native v3 tables per system (3x3 MC grids in log y, log Lambda) ---")
TAB = {}
for f in FOOTS:
    a0 = A0[f]
    for r in SAMP[f]:
        M0 = 10 ** r["logms"]; a = r["rh"] * PC
        y0 = G * M0 * MSUN / (a * a * a0)
        Rh = (r["dhost"] if r["dhost"] else r["dist"]) * KPC
        xe = {ek: g_host(Rh, host_mass(r["host"], ek, a0), a0) / a0 for ek in ("E_lo", "E_mid", "E_hi")}
        ys = math.log10(y0) + np.array([-DY, 0.0, DY])
        t = dict(y0=y0, xe=xe, ys=ys, Rh_kpc=Rh / KPC)
        # L* = 0 isolated and embedded (1-D in y)
        t["iso0"] = np.array([logG(10 ** ly_, 0.0, 0.0) for ly_ in ys])          # (3, 2) [E-W, E-V]
        t["emb0"] = np.array([logG(10 ** ly_, xe["E_mid"], 0.0) for ly_ in ys])
        for lab, Lst in LSETS(f):
            L0 = Lst / r["rh"]; Ls = math.log10(L0) + np.array([-DL, 0.0, DL])
            t[f"Ls_{lab}"] = Ls
            t[f"iso_{lab}"] = np.array([[logG(10 ** ly_, 0.0, 10 ** lL) for lL in Ls] for ly_ in ys])     # (3, 3, 2)
            t[f"emb_{lab}"] = np.array([[logG(10 ** ly_, xe["E_mid"], 10 ** lL) for lL in Ls] for ly_ in ys])
        for ek in ("E_lo", "E_hi"):
            t[f"{ek}_0"] = np.array(logG(y0, xe[ek], 0.0))
            for lab, Lst in LSETS(f):
                t[f"{ek}_{lab}"] = np.array(logG(y0, xe[ek], Lst / r["rh"]))
        TAB[(f, r["name"])] = t
    P(f"   [{f}] {len(SAMP[f])} systems tabulated ({NSOLVE[0]} solves so far, worst scaled residual {WORST[0]:.1e}, {time.time() - T0:.0f} s)")

def pred_draws(f, X, key, est, Lst=None, shift=None):
    """per-draw log10(g_pred/g_bar) for dataset X under table `key` ('iso0','emb0','iso_floor',...); est 0 = E-W, 1 = E-V."""
    out = np.empty_like(X["lb"])
    for i, r in enumerate(X["rows"]):
        t = TAB[(f, r["name"])]
        if key in ("iso0", "emb0"):
            v = lin3(X["ly"][i], t["ys"], t[key][:, est])
        else:
            lab = key.split("_", 1)[1]
            lL = math.log10(Lst) - X["la"][i]
            v = interp2(X["ly"][i], lL, t["ys"], t[f"Ls_{lab}"], t[key][:, :, est])
        if shift is not None:
            v = v + shift(t, est)
        out[i] = v
    return out

P("\n--- satellites: the chain (bootstrap median over systems of log10 g_obs/g_pred; +- bootstrap sd) ---")
SAT = {}
def rec(f, ds, lab, D):
    X = DATASETS[(f, ds)]; m, s = boot_median(D, BOOT[(f, ds)])
    SAT[f"{f}|{ds}|{lab}"] = dict(Delta=m, sd=s, z=m / s if s > 0 else float("nan"), N=len(X["rows"]))
    return m, s
for f in FOOTS:
    for ds in ("primary", "raw", "W"):
        X = DATASETS[(f, ds)]; ix = BOOT[(f, ds)]
        Ms = X["Ms"]; r12m = R12 * 10 ** X["la"] * PC
        rec(f, ds, "S0 Newton (E3 g_bar)", X["lb"])
        rec(f, ds, "S0 E3 unscreened law (nu1, algebraic)", X["lb"] - np.log10(B_scr(Ms, r12m, A0[f], None)))
        for lab, Lst in LSETS(f):
            rec(f, ds, f"S0 E3 CFG691 recipe L*{lab}", X["lb"] - np.log10(B_scr(Ms, r12m, A0[f], Lst)))
        for est, en in ((0, "E-W"), (1, "E-V")):
            rec(f, ds, f"S2 AQUAL isolated L*0 {en}", X["lb"] - pred_draws(f, X, "iso0", est))
            rec(f, ds, f"S3 AQUAL + EFE (E_mid) L*0 {en}", X["lb"] - pred_draws(f, X, "emb0", est))
            for lab, Lst in LSETS(f):
                rec(f, ds, f"S4 v3: AQUAL + EFE + screening L*{lab} {en}", X["lb"] - pred_draws(f, X, f"emb_{lab}", est, Lst))
                rec(f, ds, f"side: isolated native screening L*{lab} {en}", X["lb"] - pred_draws(f, X, f"iso_{lab}", est, Lst))
                for ek in ("E_lo", "E_hi"):
                    sh = (lambda t, e, ek=ek, lab=lab: t[f"{ek}_{lab}"][e] - t[f"emb_{lab}"][1, 1, e])
                    rec(f, ds, f"bracket {ek} L*{lab} {en}", X["lb"] - pred_draws(f, X, f"emb_{lab}", est, Lst, shift=sh))
            for ek in ("E_lo", "E_hi"):
                sh0 = (lambda t, e, ek=ek: t[f"{ek}_0"][e] - t["emb0"][1, e])
                rec(f, ds, f"bracket {ek} L*0 {en}", X["lb"] - pred_draws(f, X, "emb0", est, shift=sh0))
        rec(f, ds, "Newton E-V (exact Plummer virial)", X["lb"] - math.log10(FV_N))
    for k in [k for k in SAT if k.startswith(f + "|primary|")]:
        v = SAT[k]; P(f"   {f:9s} {k.split('|', 2)[2]:52s} Delta {v['Delta']:+.3f} +- {v['sd']:.3f}  ({v['z']:+.1f} sd)")
    for ds in ("W", "raw"):
        for lab, _ in LSETS(f):
            v = SAT[f"{f}|{ds}|S4 v3: AQUAL + EFE + screening L*{lab} E-W"]
            P(f"   {f:9s} [{ds:3s}] S4 v3 L*{lab:5s} E-W                                Delta {v['Delta']:+.3f} +- {v['sd']:.3f}  ({v['z']:+.1f} sd)")
R["satellites"] = SAT

# ---- per-system central table (clean primary central data) + S5 bounds
P("\n--- satellites: per-system central values (canonical) and S5 bounds ---")
PER = []; S5 = {}
for f in FOOTS:
    a0 = A0[f]; rat, eps = [], []
    for r in SAMP[f]:
        t = TAB[(f, r["name"])]
        b = arr_free.get(r["name"], med_free); sig = r["sigma"] * b * 1e3
        r12 = R12 * r["rh"] * PC; M = 10 ** r["logms"]
        lb0 = math.log10(3 * sig ** 2 / r12 / (G * (M / 2) * MSUN / r12 ** 2))
        lab0 = LSETS(f)[0][0]
        gW = t[f"emb_{lab0}"][1, 1, 0]
        Mdyn = 3 * sig ** 2 * r12 / G / MSUN; Mpred = 10 ** gW * M / 2
        rho_need = (Mdyn - Mpred) * MSUN / (4 / 3 * math.pi * r12 ** 3)
        Rh = t["Rh_kpc"] * KPC
        rho_h = rho_host_local(Rh, host_mass(r["host"], "E_hi", a0), a0)
        ratio = rho_h / rho_need if rho_need > 0 else float("inf")
        xe = t["xe"]["E_mid"]; ep = MUK ** 2 * (3 * r12) ** 2 / (xe / (1 + xe))
        rat.append(ratio); eps.append(ep)
        row = dict(footing=f, name=r["name"], host=r["host"], d_host_kpc=t["Rh_kpc"], logMstar=r["logms"], rh_pc=r["rh"], y_plummer=t["y0"],
                   x_e_mid=xe, x_e_lo=t["xe"]["E_lo"], x_e_hi=t["xe"]["E_hi"], Lam_floor=LSETS(f)[0][1] / r["rh"], Lam_90=90 / r["rh"],
                   log_gobs_gbar=lb0, logG_E3_L24=math.log10(float(B_scr(np.array([M]), np.array([r12]), a0, 24.0)[0])),
                   logG_iso0=t["iso0"][1, 0], logG_emb0=t["emb0"][1, 0])
        for lab, _ in LSETS(f):
            row[f"logG_v3_L{lab}"] = t[f"emb_{lab}"][1, 1, 0]; row[f"logG_iso_L{lab}"] = t[f"iso_{lab}"][1, 1, 0]
            row[f"Delta_v3_L{lab}"] = lb0 - t[f"emb_{lab}"][1, 1, 0]
        row.update(rho_host_over_rho_need=ratio, eps_muK=ep)
        PER.append(row)
    fin = [x for x in rat if math.isfinite(x)]
    S5[f] = dict(eps_max=float(max(eps)), rho_ratio_median=float(np.median(rat)), rho_ratio_max_finite=float(max(fin)) if fin else None,
                 n_overpredicted=int(sum(1 for x in rat if not math.isfinite(x))))
    P(f"   [{f}] S5: eps = mu_K^2 (3 r12)^2 / mu(x_e) max {S5[f]['eps_max']:.1e}; host local density / needed density: median "
      f"{S5[f]['rho_ratio_median']:.1e}, max {S5[f]['rho_ratio_max_finite']:.1e} (systems already at/above prediction: {S5[f]['n_overpredicted']})")
R["satellites_S5"] = S5
for row in [p for p in PER if p["footing"] == "canonical"]:
    P(f"   {row['name']:20s} {row['host']:5s} d {row['d_host_kpc']:6.1f} x_e {row['x_e_mid']:.3f} y {row['y_plummer']:.1e} Lam_fl {row['Lam_floor']:.2f} "
      f"| obs {row['log_gobs_gbar']:+.2f} | E3 L24 {row['logG_E3_L24']:+.2f} law {row['logG_iso0']:+.2f} EFE {row['logG_emb0']:+.2f} "
      f"v3 fl/24/90 {row['logG_v3_Lfloor']:+.2f}/{row['logG_v3_L24']:+.2f}/{row['logG_v3_L90']:+.2f} | Delta_v3(fl) {row['Delta_v3_Lfloor']:+.2f}")
with open(os.path.join(HERE, "s1_per_system.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(PER[0].keys())); w.writeheader(); [w.writerow(p) for p in PER]

# ================================================================== COMA UDGs
P("\n--- Coma UDGs: the chain (unweighted mean E = 2 ln(sigma_obs/sigma_pred) over the 9; se_obs CFG933; sigma_sys CFG948 recipe) ---")
def coma_pred(c, a0, xe_fac=1.0, pos="dmean", Lst=0.0, mfac=1.0, dfac=1.0, iso=False):
    Ms = c["Ms"] * mfac * dfac ** 2; Re = c["Re"] * dfac; a = Re * 1e3 * PC_
    y = G_ * Ms * MSUN_ / (a * a * a0)
    xe = 0.0 if iso else xe_fac * g_beta(c[pos] * dfac) / a0
    d = solve(y, xe, Lst * PC_ / a if Lst else 0.0)
    return math.sqrt(d["wo"] * a0 * a) / 1e3, math.sqrt(d["vir"] * a0 * a) / 1e3, xe, y
def coma_stats(f, pos="dmean", Lst=0.0, xe_fac=1.0, iso=False, est=0, sample=None, dfac=1.0, sysd=True):
    a0 = A0[f]; smp = ADM if sample is None else sample
    def Es(mfac=1.0, dfx=1.0, sfac=1.0):
        out = []
        for c in smp:
            sw, sv, xe, y = coma_pred(c, a0, xe_fac, pos, Lst, mfac, dfac * dfx, iso)
            sp = (sw, sv)[est]; s_obs = c["sig"] * sfac; e = c["esig"] * sfac
            out.append((2 * math.log(s_obs / sp), 2 * e / s_obs, xe, y))
        return out
    base = Es(); E = [x[0] for x in base]; sE = [x[1] for x in base]
    mE = float(np.mean(E)); se = se_conv(E, sE)
    res = dict(meanE=mE, meanE_dex=mE / math.log(10), se=se, z_stat=mE / se, per=[(c["name"], x[0], x[1], x[2], x[3]) for c, x in zip(smp, base)])
    if sysd:
        mv = lambda **kw: float(np.mean([x[0] for x in Es(**kw)]))
        sM = abs(mv(mfac=10 ** 0.2) - mv(mfac=10 ** -0.2)) / 2
        sA = abs(mv(sfac=1.15) - mv(sfac=1 / 1.15)) / 2
        sD = abs(mv(dfx=1.05) - mv(dfx=0.95)) / 2
        ss = math.sqrt(sM ** 2 + sA ** 2 + sD ** 2)
        res.update(s_M=sM, s_A=sA, s_D=sD, sigma_sys=ss, z_sys=mE / math.hypot(se, ss))
    return res
COMA_R = {}
for f in FOOTS:
    a0 = A0[f]
    Eo = [coma_old(c, a0) for c in ADM]; E1 = [coma_old(c, a0, kern="1") for c in ADM]
    COMA_R[f"{f}|S0 old: isolated nu_e law (CFG933)"] = dict(meanE=float(np.mean([e for e, _ in Eo])), se=se_conv([e for e, _ in Eo], [s for _, s in Eo]))
    COMA_R[f"{f}|S1 kernel nu1 (algebraic)"] = dict(meanE=float(np.mean([e for e, _ in E1])), se=se_conv([e for e, _ in E1], [s for _, s in E1]))
    COMA_R[f"{f}|S2 AQUAL isolated L*0 E-W"] = coma_stats(f, iso=True)
    for pos in ("dmean", "dproj"):
        COMA_R[f"{f}|S3 AQUAL + EFE {pos} L*0 E-W"] = coma_stats(f, pos=pos)
        for lab, Lst in LSETS(f):
            COMA_R[f"{f}|S4 v3 {pos} L*{lab} E-W"] = coma_stats(f, pos=pos, Lst=Lst)
        lab0, L0 = LSETS(f)[0]
        COMA_R[f"{f}|v3 {pos} L*{lab0} E-V"] = coma_stats(f, pos=pos, Lst=L0, est=1)
        COMA_R[f"{f}|v3 {pos} L*{lab0} field/2"] = coma_stats(f, pos=pos, Lst=L0, xe_fac=0.5)
        COMA_R[f"{f}|S6 native H0 (D x 70/67.9, ASSUMED) {pos} L*{lab0}"] = coma_stats(f, pos=pos, Lst=L0, dfac=70.0 / 67.9)
        COMA_R[f"{f}|v3 all 11 Coma {pos} L*{lab0}"] = coma_stats(f, pos=pos, Lst=L0, sample=COMA)
    COMA_R[f"{f}|isolated bound (x_e = 0) L*{LSETS(f)[0][0]}"] = coma_stats(f, Lst=LSETS(f)[0][1], iso=True)
    for k in [k for k in COMA_R if k.startswith(f + "|")]:
        v = COMA_R[k]
        extra = f"  sigma_sys {v['sigma_sys']:.3f} (M {v['s_M']:.3f} A {v['s_A']:.3f} D {v['s_D']:.3f})  z_stat {v['z_stat']:+.2f}  z_sys {v['z_sys']:+.2f}" if "z_sys" in v else ""
        P(f"   {f:9s} {k.split('|', 1)[1]:52s} <E> {v['meanE']:+.3f} ln ({v['meanE'] / math.log(10):+.3f} dex)  se {v['se']:.3f}{extra}")
# Coma per-galaxy + S5 bounds
CPER = []; CS5 = {}
for f in FOOTS:
    a0 = A0[f]; rat, eps = [], []
    lab0, L0 = LSETS(f)[0]
    v = COMA_R[f"{f}|S4 v3 dmean L*{lab0} E-W"]
    for c, (nm, E, sE, xe, y) in zip(ADM, v["per"]):
        r12 = R12 * c["Re"] * 1e3 * PC_
        Mdyn = 3 * (c["sig"] * 1e3) ** 2 * r12 / G_
        Mpred = Mdyn * math.exp(-E)
        rho_need = (Mdyn - Mpred) / (4 / 3 * math.pi * r12 ** 3)
        ratio = rho_beta(c["dmean"]) / rho_need if rho_need > 0 else float("inf")
        ep = MUK ** 2 * (3 * r12) ** 2 / (xe / (1 + xe)); rat.append(ratio); eps.append(ep)
        CPER.append(dict(footing=f, name=nm, Mstar=c["Ms"], Re_kpc=c["Re"], sigma=c["sig"], esig=c["esig"], d_mean_kpc=c["dmean"], d_proj_kpc=c["dproj"],
                         x_e_dmean=xe, y_plummer=y, E_old=coma_old(c, a0)[0], E_v3_dmean=E, sE=sE,
                         E_v3_dproj=[p[1] for p in COMA_R[f"{f}|S4 v3 dproj L*{lab0} E-W"]["per"] if p[0] == nm][0],
                         rho_host_over_rho_need=ratio, eps_muK=ep))
    fin = [x for x in rat if math.isfinite(x)]
    CS5[f] = dict(eps_max=float(max(eps)), rho_ratio_mean=float(np.mean(fin)) if fin else None, rho_ratio_max=float(max(fin)) if fin else None)
    P(f"   [{f}] S5: eps max {CS5[f]['eps_max']:.1e}; Coma local density / needed density: mean {CS5[f]['rho_ratio_mean']:.1e}, max {CS5[f]['rho_ratio_max']:.1e}")
with open(os.path.join(HERE, "s1_coma_per_galaxy.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(CPER[0].keys())); w.writeheader(); [w.writerow(p) for p in CPER]
for p in [p for p in CPER if p["footing"] == "canonical"]:
    P(f"   {p['name']:22s} x_e {p['x_e_dmean']:.3f} y {p['y_plummer']:.4f}  E old {p['E_old']:+.3f}  v3 dmean {p['E_v3_dmean']:+.3f}  dproj {p['E_v3_dproj']:+.3f}  (sE {p['sE']:.3f})")
R["coma"] = {k: {kk: vv for kk, vv in v.items()} for k, v in COMA_R.items()}
R["coma_S5"] = CS5

# ================================================================== production convergence, RSS
check("K9", WORST[0] < 1e-8, f"{WORST[0]:.1e} over {NSOLVE[0]} solves", "< 1e-8", "every production solve converged")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K10", rss < 1.0, f"{rss:.3f} GB", "< 1 GB", "peak RSS")
VALID = all(CHK[k]["ok"] for k in ("K2", "K3", "K4", "K5", "K6"))

# ================================================================== VERDICTS (frozen lines)
P("\n--- verdict lines (frozen) ---")
V = {}
# tile 26
prim = {(f, lab): SAT[f"{f}|primary|S4 v3: AQUAL + EFE + screening L*{lab} E-W"] for f in FOOTS for lab, _ in LSETS(f)}
c_all3 = all(abs(v["Delta"]) >= 3 * v["sd"] for v in prim.values())
c_W = all(abs(SAT[f"{f}|W|S4 v3: AQUAL + EFE + screening L*floor E-W"]["Delta"]) >= 2 * SAT[f"{f}|W|S4 v3: AQUAL + EFE + screening L*floor E-W"]["sd"] for f in FOOTS)
cells = {f: [SAT[f"{f}|primary|S4 v3: AQUAL + EFE + screening L*floor E-W"]] + [SAT[f"{f}|primary|bracket {ek} L*floor E-W"] for ek in ("E_lo", "E_hi")] for f in FOOTS}
c_br = all(min(abs(c["Delta"]) / c["sd"] for c in cells[f]) >= 3 for f in FOOTS)
c_pass = all(abs(prim[(f, "floor")]["Delta"]) <= 2 * prim[(f, "floor")]["sd"] for f in FOOTS)
s5_nd = any(S5[f]["rho_ratio_median"] >= 1 for f in FOOTS)
if not VALID or s5_nd:
    v26 = "NOT DECIDABLE" + (" (solver validation failed)" if not VALID else " (host local density could supply the median gap: mu_K^2 zero point decides)")
elif c_all3 and c_W and c_br:
    v26 = "FAIL"
elif c_pass:
    v26 = "PASS"
else:
    why = []
    if not c_all3: why.append("not >= 3 sd at every L* and footing")
    if not c_W: why.append("worst-clean W within 2 sd")
    if not c_br: why.append("a host-bracket cell below 3 sd")
    v26 = "CONDITIONAL (" + "; ".join(why) + ")"
v26_EV = all(abs(SAT[f"{f}|primary|S4 v3: AQUAL + EFE + screening L*{lab} E-V"]["Delta"]) >= 3 * SAT[f"{f}|primary|S4 v3: AQUAL + EFE + screening L*{lab} E-V"]["sd"]
             for f in FOOTS for lab, _ in LSETS(f))
V["tile26"] = dict(verdict=v26, all3=c_all3, W_2sd=c_W, bracket_3sd=c_br, pass_line=c_pass, s5_not_decidable=s5_nd, EV_also_3sd_everywhere=v26_EV,
                   old="FAIL (E3 +0.89 / +0.85 dex at L*24, CFG691 isolated recipe, no EFE)")
for f in FOOTS:
    P(f"   tile 26 [{f}] v3 Delta (E-W): " + ", ".join(f"L*{lab} {prim[(f, lab)]['Delta']:+.3f}+-{prim[(f, lab)]['sd']:.3f}" for lab, _ in LSETS(f))
      + f" | W at floor {SAT[f'{f}|W|S4 v3: AQUAL + EFE + screening L*floor E-W']['Delta']:+.3f}+-{SAT[f'{f}|W|S4 v3: AQUAL + EFE + screening L*floor E-W']['sd']:.3f}"
      + f" | best bracket cell {min(abs(c['Delta']) / c['sd'] for c in cells[f]):.1f} sd")
P(f"   TILE 26 (dwarf satellites): old FAIL -> v3 {v26}   [E-V also >= 3 sd everywhere: {v26_EV}]")
# tile 29
zz = {(f, pos, lab): COMA_R[f"{f}|S4 v3 {pos} L*{lab} E-W"] for f in FOOTS for pos in ("dmean", "dproj") for lab, _ in LSETS(f)}
c_fail = all(abs(v["z_sys"]) >= 3 for v in zz.values())
c_pass29 = all(abs(v["z_stat"]) <= 2 for v in zz.values())
c_rob = all(abs(COMA_R[f"{f}|v3 {pos} L*{LSETS(f)[0][0]} field/2"]["z_sys"]) >= 3 for f in FOOTS for pos in ("dmean", "dproj"))
s5c = any((CS5[f]["rho_ratio_mean"] or 0) >= 1 for f in FOOTS)
if not VALID or s5c:
    v29 = "NOT DECIDABLE" + (" (solver validation failed)" if not VALID else " (host local density could supply the mean gap)")
elif c_fail:
    v29 = "FAIL, " + ("ROBUST" if c_rob else "FIELD-DEPENDENT")
elif c_pass29:
    v29 = "PASS"
else:
    v29 = "CONDITIONAL (" + ("z_stat >= 3 but z_sys < 3 somewhere: systematics-limited" if all(abs(v["z_stat"]) >= 3 for v in zz.values()) else "2-3 sigma or a footing/position split") + ")"
V["tile29"] = dict(verdict=v29, fail_line=c_fail, pass_line=c_pass29, robust_field_half=c_rob, s5_not_decidable=s5c,
                   old="UNDEC (CFG933 NOT DIAGNOSTIC / CFG948 CONTROL-LIMITED; isolated EFE-free law)")
for f in FOOTS:
    P(f"   tile 29 [{f}] v3 z_sys (z_stat): " + ", ".join(f"{pos} L*{lab} {zz[(f, pos, lab)]['z_sys']:+.2f} ({zz[(f, pos, lab)]['z_stat']:+.2f})"
                                                    for pos in ("dmean", "dproj") for lab, _ in LSETS(f)))
P(f"   TILE 29 (Coma UDGs): old UNDEC -> v3 {v29}")
V["tile19"] = "lane P4 (not computed here)"
R["verdict"] = V

npass = sum(v["ok"] for v in CHK.values())
R["checks"] = CHK; R["runtime_s"] = time.time() - T0; R["solves"] = NSOLVE[0]; R["worst_residual"] = WORST[0]
P(f"\nS1_V3_HOSTED_SMALL COMPLETE: {npass}/{len(CHK)} checks PASS.  {time.time() - T0:.0f} s, {NSOLVE[0]} production solves")
json.dump(R, open(os.path.join(HERE, f"s1_v3_hosted_small_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"s1_v3_hosted_small{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
