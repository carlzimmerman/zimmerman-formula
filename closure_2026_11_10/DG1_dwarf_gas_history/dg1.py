#!/usr/bin/env python3
"""DG1 (criteria 3719fe178d): RB2's high dwarf rows under form B -- the data side (Part A) and the gas history (Part B).

    python3 dg1.py            -> dg1.json / dg1.out             (known answers KA1-KA6, Parts A, B, C numbers, D)
    python3 dg1.py --mutate   -> dg1_MUTATE.json / dg1_MUTATE.out (M1 lost gas scrambled within class; M2 stellar-mass power law)

Code paths COPIED (not imported) from: RB2 (closure_2026_11_09/RB2_form_b_hosted_rows/rb2.py: X1's LVD loader and build,
classes, B's law and cut, dsph_reading, XF1's boot_median), P1 (rebuild_2026_10_22/P1_dwarf_chemistry/p1_dwarf_chemistry.py:
the one-zone family grid, e6_equiv, u0_solve, g0_exact, lmdf, lvd_sigma, intervals, mass_g), SE2 (closure_2026_11_06/
SE2_step_as_systematics/se2.py: dsph_admiss, ALT catalogues, dsph_inputs widths, SPEC main, rngs, post_dsph).
Committed tables and JSON of those lanes are read as data.
kappa = 1/2 FITTED; not theory closed; footings never pooled; cold dark energy, no particle.  Relabels nothing."""
import os, sys, json, math, csv, time, re, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.special import exp1, digamma, polygamma
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar, minimize

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.dirname(HERE); REPO = os.path.dirname(CL)
MUT = "--mutate" in sys.argv
TAG = "dg1_MUTATE" if MUT else "dg1"
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
LN10 = math.log(10.0)
CHK = {}
def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"{name} {'PASS' if ok else 'FAIL'}  {msg}")
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)

# =============================================================================== RB2 / X1 (copied verbatim: constants, loader, build)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
NMC, NBOOT = 2000, 4000
FW_N = 2.0 * (4 / 3) ** 3 / (1 + (4 / 3) ** 2) ** 1.5
R12 = 4.0 / 3.0
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
X1D = os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount")
RB2D = os.path.join(CL, "..", "closure_2026_11_09", "RB2_form_b_hosted_rows")
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
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")),
                             mv=mv, dm31=fl(r.get("distance_m31")), _raw=r))
    return rows
def load_ul():
    """DG1 addition: LVD rows with only an upper limit on vlos_sigma (same fields as load_lvd; sigma = the UL, no error)."""
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma")); ul = fl(r.get("vlos_sigma_ul"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if (s and s > 0) or not ul or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=ul, sem=1e-12, sep=1e-12, ul=True, cens=True,
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")),
                             mv=mv, dm31=fl(r.get("distance_m31")), _raw=r))
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
def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, mvrule=False, floor=0.0):
    """X1's build (copied); DG1 adds floor (velocity-error floor delta, km/s, subtracted in quadrature for sigma < 4 km/s)."""
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC)); Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC))
    cens = np.zeros(N, bool)
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        cens[i] = bool(r.get("cens", False))
        if sig_src == "lower" and r["name"] in GEH and not cens[i]:
            gs, gl_, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl_, gu
        if floor > 0 and s < 4.0:
            if s > math.sqrt(2.0) * floor:
                s = math.sqrt(s * s - floor * floor)
            elif not cens[i]:
                cens[i] = True; sem = sep = 1e-12      # a measured sigma at the floor becomes an upper limit at its value
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
    return dict(lb=lb, ly=ly, la=la, Md=Md, Ms=Ms_, rows=keep, cens=cens)
def Rh_X1(r):
    if r["host"] == "field":
        return r["dist"] * KPC
    if r["dhost"]:
        return r["dhost"] * KPC
    if r["host"] == "M31" and r["dm31"]:
        return r["dm31"] * KPC
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
ULR = [r for r in load_ul() if klass(r) is not None]
X1CSV = list(csv.DictReader(open(os.path.join(X1D, "x1_per_system.csv"))))
X1TAB = {f: json.load(open(os.path.join(X1D, f"x1_stage_tables_{f}.json")))["tables"] for f in FOOTS}
RB2J = json.load(open(os.path.join(RB2D, "rb2.json")))
RB2M = json.load(open(os.path.join(RB2D, "rb2_MUTATE.json")))

def boot_median(vals, sds, nb=4000, seed=11):
    rng = np.random.default_rng(seed); vals = np.asarray(vals); sds = np.asarray(sds); n = len(vals); meds = np.empty(nb)
    for b in range(nb):
        ix = rng.integers(0, n, n); meds[b] = np.median(vals[ix] + rng.normal(0, 1, n) * sds[ix])
    q = np.percentile(meds, [2.5, 50, 97.5])
    return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], contains0=bool(q[0] <= 0 <= q[2]), n=int(n))

# B's law (a0 units) and the cut (copied from RB2)
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
VC = {"MW": 200.0, "M31": 230.0}
def K_dsph(k, d_m, a_m, Vc_kms, a0):
    return k * (Vc_kms * 1e3) ** 2 / d_m ** 2 * a_m / a0
def dsph_prim(X, i, r, a0):
    """RB2's dsph_reading(..., 'prim'): per-draw Delta under B (k = 3 cut at today's distance)."""
    y = 10 ** X["ly"][i]; a_m = 10 ** X["la"][i] * PC
    rJ = np.full(y.shape, np.inf)
    if r["host"] in VC:
        rJ = rJ_iso(y, K_dsph(3.0, Rh_X1(r), a_m, VC[r["host"]], a0))
    pred = np.log10(gB(R12, y, rJ) / (y / (2 * R12 ** 2)))
    return X["lb"][i] - pred

# =============================================================================== P1 (copied verbatim: the one-zone family and lmdf)
GAMMA = 0.5772156649015329
LOGY = (-0.5, -0.2, 0.1)
GAS_FAC = 1.33
NQ = 400
_xq, _wq = np.polynomial.legendre.leggauss(NQ)
QW = 0.5 * (_xq + 1.0); QWW = 0.5 * _wq
UINF = 60.0
def lnphi(k, t):
    if k == 0.0:
        return np.log(t)
    return np.log(-np.expm1(-k * t) / k)
def moments(k, U):
    U = np.atleast_1d(np.asarray(U, float))
    Ue = np.where(np.isfinite(U), U, UINF)[:, None]
    t = Ue * QW[None, :] ** 4
    wt = np.exp(-t) * 4.0 * Ue * QW[None, :] ** 3 * QWW[None, :]
    nrm = wt.sum(1)
    lp = lnphi(k, t)
    g = (wt * lp).sum(1) / nrm
    s2 = (wt * (lp - g[:, None]) ** 2).sum(1) / nrm
    return g, s2
def g0_exact(U):
    if not np.isfinite(U):
        return -GAMMA
    if U < 1.0:
        lU, num, fac = math.log(U), 0.0, 1.0
        for n in range(40):
            num += (-1) ** n / fac * U ** (n + 1) * (lU / (n + 1) - 1.0 / (n + 1) ** 2)
            fac *= (n + 1)
        return num / (-math.expm1(-U))
    return (-GAMMA - exp1(U) - math.exp(-U) * math.log(U)) / (-math.expm1(-U))
KG = np.concatenate([[0.0], np.logspace(-3, 3, 601)])
UG = np.concatenate([np.logspace(-4, 2, 1201), [np.inf]])
GG = np.empty((KG.size, UG.size)); S2 = np.empty_like(GG)
for _i, _k in enumerate(KG):
    GG[_i], S2[_i] = moments(_k, UG)
SIG = np.sqrt(S2) / LN10
DEN = np.where(np.isfinite(UG), -np.expm1(-np.where(np.isfinite(UG), UG, 1.0)), 1.0)
SIG_FMAX = float(SIG[0, -1]); SIG_GMIN = float(SIG.min())
def u0_solve(ln_zg_y):
    if ln_zg_y >= -GAMMA:
        return None
    f = lambda s: g0_exact(math.exp(s)) - ln_zg_y
    if f(5.0) < 0:
        return math.exp(5.0)
    return math.exp(brentq(f, -60.0, 5.0, xtol=1e-14, rtol=1e-14))
def e6_equiv(feh, y_log, Ms, Mg, form):
    lzy = feh * LN10 - y_log * LN10
    if Mg > 0:
        r = Ms / Mg
        h = lambda lo: lzy + lo - g0_exact(math.log1p(math.exp(lo) * r))
        if h(0.0) >= 0:
            return 1.0, True, 0.0
        grid = np.linspace(0.0, 12.0 * LN10, 400)
        hv = [h(x) for x in grid]
        j = next(i for i in range(1, len(grid)) if hv[i] >= 0)
        lo = brentq(h, grid[j - 1], grid[j], xtol=1e-14, rtol=1e-14)
        ope = math.exp(lo)
        return (ope * Ms + Mg) / (Ms + Mg), False, math.log1p(ope * r)
    if form == "W1":
        ope = math.exp(-lzy - GAMMA)
        return (ope, False, np.inf) if ope >= 1 else (1.0, True, np.inf)
    u0 = u0_solve(lzy)
    if u0 is None:
        return 1.0, True, np.inf
    Lf = lambda U: math.exp(-lzy + g0_exact(U)) / (-math.expm1(-U))
    Us = u0 * np.logspace(0, math.log10(max(60.0 / u0, 1.0000001)), 3000)
    vals = np.array([Lf(U) for U in Us]); vinf = math.exp(-lzy - GAMMA)
    i = int(np.argmin(vals))
    if vinf < vals[i]:
        return vinf, False, np.inf
    if i == 0:
        return 1.0 / (-math.expm1(-u0)), False, u0
    a, b = math.log(Us[i - 1]), math.log(Us[min(i + 1, Us.size - 1)])
    r = minimize_scalar(lambda s: Lf(math.exp(s)), bounds=(a, b), method="bounded", options=dict(xatol=1e-12))
    return (float(r.fun), False, math.exp(r.x)) if r.fun < vals[i] else (float(vals[i]), False, float(Us[i]))
def lmdf(feh, y_log, Ms, Mg, I):
    y = 10 ** y_log; lnzg = feh * LN10; lzy = lnzg - y_log * LN10
    if I is None:
        return dict(L=None, flag="NOT TESTED")
    lo, hi = I
    if lo > SIG_FMAX:
        L0, under, U0 = e6_equiv(feh, y_log, Ms, Mg, "W1")
        return dict(L=L0, flag="UNDER" if under else "ABOVE", k=0.0, u=U0, eta=L0 - 1 if Mg <= 0 else None, zeta=1.0)
    if lo < SIG_GMIN:
        return dict(L=1.0, flag="NO BOUND", k=None, u=None, eta=None, zeta=None)
    best = dict(L=np.inf)
    if Mg <= 0:
        P0 = np.exp(lnzg - GG)
        allowed = np.where(KG[:, None] == 0, P0 <= y * (1 + 1e-12), P0 < y)
        L = (y / P0) / DEN[None, :]
        cand = allowed & (SIG >= lo) & (SIG <= hi)
        if cand.any():
            Lc = np.where(cand, L, np.inf); j = np.unravel_index(int(np.argmin(Lc)), Lc.shape)
            ope = y / P0[j]; kk = KG[j[0]]
            best = dict(L=float(Lc[j]), k=float(kk), u=float(UG[j[1]]), eta=float(ope - 1),
                        zeta=1.0 if kk == 0 else float(1 + kk * ope / (ope - 1)))
        u0 = u0_solve(lzy)
        if u0 is not None:
            s0 = math.sqrt(moments(0.0, [u0])[1][0]) / LN10
            L0 = 1.0 / (-math.expm1(-u0))
            if lo <= s0 <= hi and L0 < best["L"]:
                best = dict(L=L0, k=0.0, u=u0, eta=0.0, zeta=1.0)
    else:
        r = Ms / Mg; Uf = UG[:-1]
        L0g, underg, U0g = e6_equiv(feh, y_log, Ms, Mg, "W1")
        if not underg and lo > math.sqrt(moments(0.0, [U0g])[1][0]) / LN10:
            return dict(L=L0g, flag="ABOVE", k=0.0, u=U0g, eta=None, zeta=1.0)
        for ik, kk in enumerate(KG):
            Gk = GG[ik, :-1]
            ope = y * np.exp(Gk) / math.exp(lnzg)
            F = Uf - np.log1p(ope * r)
            idx = np.where((F[:-1] < 0) & (F[1:] >= 0))[0]
            if not idx.size:
                continue
            j = idx[0]; a = F[j] / (F[j] - F[j + 1])
            gst = Gk[j] + a * (Gk[j + 1] - Gk[j]); s2st = S2[ik, j] + a * (S2[ik, j + 1] - S2[ik, j])
            Ust = Uf[j] + a * (Uf[j + 1] - Uf[j])
            opest = y * math.exp(gst) / math.exp(lnzg)
            if opest < 1 or (kk > 0 and opest <= 1):
                continue
            sg = math.sqrt(s2st) / LN10
            if lo <= sg <= hi:
                Lv = (opest * Ms + Mg) / (Ms + Mg)
                if Lv < best["L"]:
                    best = dict(L=float(Lv), k=float(kk), u=float(Ust), eta=float(opest - 1),
                                zeta=1.0 if kk == 0 else float(1 + kk * opest / (opest - 1)))
        L0, under, U0 = e6_equiv(feh, y_log, Ms, Mg, "W1")
        if not under:
            s0 = math.sqrt(moments(0.0, [U0])[1][0]) / LN10
            if lo <= s0 <= hi and L0 < best["L"]:
                best = dict(L=L0, k=0.0, u=U0, eta=None, zeta=1.0)
    if not np.isfinite(best["L"]):
        return dict(L=1.0, flag="UNDER", k=None, u=None, eta=None, zeta=None)
    best["flag"] = "OK"
    return best
LVDR = {}
for _f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for _r in csv.DictReader(open(os.path.join(DATA, "dsph", _f))):
        LVDR[_r["name"]] = _r
def lvd_sigma(r):
    s = fl(r.get("metallicity_spectroscopic_sigma")); ul = fl(r.get("metallicity_spectroscopic_sigma_ul"))
    if s is not None:
        return dict(sig=s, em=fl(r.get("metallicity_spectroscopic_sigma_em")), ep=fl(r.get("metallicity_spectroscopic_sigma_ep")),
                    ul=None, src="LVD-spec")
    if ul is not None:
        return dict(sig=None, em=None, ep=None, ul=ul, src="LVD-spec-UL")
    s = fl(r.get("metallicity_photometric_sigma"))
    if s is not None:
        return dict(sig=s, em=fl(r.get("metallicity_photometric_sigma_em")), ep=fl(r.get("metallicity_photometric_sigma_ep")),
                    ul=None, src="LVD-PHOT")
    return None
def intervals(w):
    if w is None or w.get("sig") is None:
        return None, None, None
    s, em, ep = w["sig"], w.get("em"), w.get("ep")
    I0 = (s - 0.005, s + 0.005)
    if em is None or ep is None:
        return I0, I0, I0
    return I0, (max(0.0, s - 2 * em), s + 2 * ep), (s + 2 * ep - 0.005, s + 2 * ep + 0.005)
def mass_g(name):
    mhi = fl(LVDR[name].get("mass_HI")) if name in LVDR else None
    return GAS_FAC * 10 ** mhi if mhi is not None else 0.0
E6 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(REPO, "doors_push_2026_10_22", "E6_native_fret", "e6_per_system.csv")))}
P1CSV = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "P1_dwarf_chemistry", "p1_per_system.csv")))
         if r["footing"] == "canonical"}
def lsys(n, logms_lvd, width_override=None):
    """P1's lsys (copied) with DG1's Ms rule: E6's logMstar for P1's own systems, else LVD mass_stellar."""
    lv = LVDR.get(n); feh = fl(lv.get("metallicity")) if lv else None
    row = E6.get(("canonical", n)) or E6.get(("alt", n))
    Ms = 10 ** fl(row["logMstar"]) if row is not None else 10 ** logms_lvd
    Mg = mass_g(n)
    w = lvd_sigma(lv) if lv else None
    if width_override is not None:
        w = dict(sig=width_override, em=None, ep=None, ul=None, src="imputed class median")
    I0, I2, Ihi = intervals(w)
    res = dict(feh=feh, w=w, Ms=Ms, Mg=Mg, inP1=n in P1CSV)
    if feh is None or I0 is None:
        res["tested"] = False
        return res
    res["tested"] = True
    res["L0"] = lmdf(feh, -0.5, Ms, Mg, I0); res["Llo"] = lmdf(feh, -0.5, Ms, Mg, I2); res["Lhi"] = lmdf(feh, 0.1, Ms, Mg, Ihi)
    return res

# =============================================================================== SE2 (copied: admissibility, alt catalogues, widths, SPEC, rngs)
def norm(n): n = n.lower().replace("andromeda", "and"); return re.sub(r"[\s()\-_]", "", n)
ALT = {"collins": {}, "mcc": {}}
for l in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv")):
    if l.startswith("#") or not l.strip(): continue
    c = l.rstrip("\n").split("\t")
    if c[0].strip() in ("recno", "") or c[0].startswith("-"): continue
    try: sv = float(c[18])
    except ValueError: continue
    if sv > 0: ALT["collins"][norm(c[1].strip())] = sv
for r in csv.DictReader(open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv"))):
    try: sv = float(r["sigma*"])
    except ValueError: continue
    if sv > 0: ALT["mcc"][norm(r["Name"])] = sv
ALTCAT = {"bright M31": "collins", "MW classical": "mcc", "LG field": "mcc", "MW ultra-faint": "mcc", "M31 others": "collins"}
TAU_LINE = 0.375
DCLS = ("bright M31", "MW classical", "LG field", "MW ultra-faint", "M31 others"); SE2_GRADED = ("bright M31", "MW classical"); SE2_CONTROL = ("LG field",)
NDRAW = 20000
SEEDS = {"ellipticals": 101, "KiDS": 102, "X-COP": 103, "groups": 104, "bright M31": 105, "MW classical": 106, "LG field": 107,
         "MW ultra-faint": 108, "M31 others": 109, "Coma UDGs": 110}
def rngs(cls, f): b = SEEDS[cls] * 10 + (0 if f == "canonical" else 1); return np.random.default_rng(b), np.random.default_rng(b + 500000)
def dsph_admiss_v(host, rh_pc, sigma, dhost_kpc, scale=1.0):
    """SE2's dsph_admiss with the row's values passed in (formula verbatim)."""
    if host not in VC: return dict(A1=True, A2=True, tau=None, tc_to=None)
    Re = float(rh_pc); sg = float(sigma); d = float(dhost_kpc) * 1e3; V = VC[host]
    GPC = 4.30091e-3; MW_ = 4 * sg ** 2 * Re / GPC; Mh = V ** 2 * d / GPC
    tau = Re / (d * (MW_ / (3 * Mh)) ** (1 / 3)); tc = (4 / 3) * Re / sg; to = 2 * math.pi * d / V
    return dict(A1=bool(tau * scale < TAU_LINE), A2=bool(tc <= 0.1 * to), tau=tau, tc_to=tc / to)
def se2_widths(f):
    """SE2's dsph_inputs width block (copied), on X1's per-system CSV rows by X1's class."""
    W = {}; pooled = []
    rows = {c: [r for r in X1CSV if r["footing"] == f and r["cls"] == c] for c in DCLS}
    for c in DCLS:
        an = []
        for r in rows[c]:
            ev = r.get("Delta[v3 L*floor E-V]", ""); ew = r.get("Delta[v3 L*floor]", "")
            if ev and ew: an.append(abs(float(ev) - float(ew)))
        cat = ALT[ALTCAT[c]]; lr = [math.log10(float(r["sigma"]) / cat[norm(r["name"])]) for r in rows[c] if norm(r["name"]) in cat]
        if c in SE2_GRADED + SE2_CONTROL: pooled += lr
        W[c] = dict(a_c=float(np.median(an)) if an else 0.0, n_aniso=len(an), memb_lr=lr)
    for c in DCLS:
        lr = W[c]["memb_lr"]; use = lr if len(lr) >= 3 else pooled
        mu = float(np.mean(use)); rms = float(np.sqrt(np.mean(np.square(use))))
        W[c].update(m_c=math.sqrt(mu ** 2 + (rms / math.sqrt(len(use))) ** 2), memb_n=len(lr), memb_pooled=len(lr) < 3, memb_mu=mu, memb_rms=rms)
    return W
SPEC_MAIN = dict(ups=(0.0, 0.30), q=(0.0, 0.5), ul=True, dist=1.0, aniso=1.0, memb=1.0)
def uni(rng, lohi, n): lo, hi = lohi; return np.full(n, lo) if hi == lo else rng.uniform(lo, hi, n)
def dlaw(b, gN):
    """GB1/SE2 delta() in a0 units (same law as gl)."""
    return np.log10(gl(b * gN) / gl(gN))

# =============================================================================== DG1 statistics
def km_median(x, cens):
    """Kaplan-Meier median of left-censored data (cens True: the true value is <= x). Flip to right-censored; median = first
    event time with S <= 0.5 (midpoint to the next event time when S equals 0.5 exactly). Returns (median, flag)."""
    t = -np.asarray(x, float); c = np.asarray(cens, bool)
    order = np.lexsort((c, t))          # ascending t; at equal t events (False) before censorings (True)
    t = t[order]; c = c[order]; n = t.size
    S = 1.0; i = 0
    while i < n:
        j = i
        while j < n and t[j] == t[i]:
            j += 1
        d = int(np.sum(~c[i:j])); atrisk = n - i
        if d > 0:
            S *= (1.0 - d / atrisk)
            if S <= 0.5 + 1e-12:
                if abs(S - 0.5) <= 1e-12:
                    k = j
                    while k < n and c[k]:
                        k += 1
                    if k < n:
                        return -0.5 * (t[i] + t[k]), "ok"
                return -t[i], "ok"
        i = j
    return float(np.min(x)), "S>0.5 (lowest bound used)"
def km_boot(vals, sds, cens, nb=4000, seed=11):
    """XF1's C2 bootstrap with the KM median (same RNG consumption as boot_median: integers then normal per resample)."""
    rng = np.random.default_rng(seed); vals = np.asarray(vals, float); sds = np.asarray(sds, float); cens = np.asarray(cens, bool)
    n = len(vals); meds = np.empty(nb); nflag = 0
    sdu = np.where(cens, 0.0, sds)
    for b in range(nb):
        ix = rng.integers(0, n, n); xb = vals[ix] + rng.normal(0, 1, n) * sdu[ix]
        m, fg = km_median(xb, cens[ix]); meds[b] = m; nflag += fg != "ok"
    q = np.percentile(meds, [2.5, 50, 97.5])
    return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], contains0=bool(q[0] <= 0 <= q[2]), n=int(n),
                n_cens=int(cens.sum()), point=km_median(vals, cens)[0], flagged=int(nflag))
def cens_ml(vals, sds, cens):
    """censored-normal ML on (mu, tau): measured ~ N(mu, tau^2 + sd^2); bounds: P(x <= UL). Profile 95 % interval on mu."""
    from scipy.stats import norm as N_
    v = np.asarray(vals, float); s = np.asarray(sds, float); c = np.asarray(cens, bool)
    def nll(p):
        mu, lt = p; tau = math.exp(lt); sg = np.sqrt(tau ** 2 + s ** 2)
        return -(np.sum(N_.logpdf(v[~c], mu, sg[~c])) + np.sum(N_.logcdf((v[c] - mu) / sg[c])))
    best = minimize(nll, [float(np.median(v)), math.log(0.3)], method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=4000))
    mu0, l0 = best.x; f0 = best.fun
    def prof(mu):
        r = minimize_scalar(lambda lt: nll([mu, lt]), bounds=(-8, 2), method="bounded", options=dict(xatol=1e-8)); return r.fun - f0 - 1.92
    lo = brentq(prof, mu0 - 5, mu0) if prof(mu0 - 5) > 0 else float("nan")
    hi = brentq(prof, mu0, mu0 + 5) if prof(mu0 + 5) > 0 else float("nan")
    return dict(mu=float(mu0), tau=float(math.exp(l0)), ci95=[float(lo), float(hi)], contains0=bool(lo <= 0 <= hi))
def ranks(x):
    x = np.asarray(x, float); o = np.argsort(x, kind="mergesort"); r = np.empty(len(x)); r[o] = np.arange(len(x)); return r
def zrank(x):
    r = ranks(x); r = r - r.mean(); s = math.sqrt(np.sum(r * r)); return r / s if s > 0 else r
def strat_S(groups, yv, xv):
    """sum_c n_c Spearman_c(y, x) / sum n_c over classes with n_c >= 3."""
    num = 0.0; den = 0
    for g in groups:
        if len(g) < 3: continue
        num += len(g) * float(np.sum(zrank(yv[g]) * zrank(xv[g]))); den += len(g)
    return num / den if den else float("nan")
def perm_test(groups, yv, xv, nperm, seed):
    """within-class permutation null for strat_S (x permuted inside each class). One-sided p (S_perm >= S_obs)."""
    rng = np.random.default_rng(seed); S0 = strat_S(groups, yv, xv)
    gs = [g for g in groups if len(g) >= 3]; den = sum(len(g) for g in gs)
    zy = {i: zrank(yv[g]) for i, g in enumerate(gs)}; zx = {i: zrank(xv[g]) for i, g in enumerate(gs)}
    Sp = np.zeros(nperm)
    for i, g in enumerate(gs):
        perms = np.argsort(rng.random((nperm, len(g))), axis=1)
        Sp += len(g) * (zx[i][perms] @ zy[i])
    Sp /= den
    return S0, float((1 + np.sum(Sp >= S0 - 1e-12)) / (nperm + 1)), float((1 + np.sum(np.abs(Sp) >= abs(S0) - 1e-12)) / (nperm + 1))
def demeaned_slope(groups, yv, xv, nb, seed):
    def sl(gl_):
        xs = np.concatenate([xv[g] - xv[g].mean() for g in gl_]); ys = np.concatenate([yv[g] - yv[g].mean() for g in gl_])
        return float(np.sum(xs * ys) / np.sum(xs * xs)) if np.sum(xs * xs) > 0 else float("nan")
    gs = [np.asarray(g) for g in groups if len(g) >= 3]
    s0 = sl(gs); rng = np.random.default_rng(seed); bs = np.empty(nb)
    for b in range(nb):
        bs[b] = sl([g[rng.integers(0, len(g), len(g))] for g in gs])
    q = np.nanpercentile(bs, [2.5, 97.5])
    return dict(slope=s0, ci95=[float(q[0]), float(q[1])], contains1=bool(q[0] <= 1 <= q[1]))
def resid_on(groups, v, z):
    out = v.copy()
    for g in groups:
        if len(g) < 3: continue
        A = np.vstack([np.ones(len(g)), z[g]]).T; c, *_ = np.linalg.lstsq(A, v[g], rcond=None); out[g] = v[g] - A @ c
    return out

# =============================================================================== the history prediction
def hist_NR(gNs, c1, c0):
    """g_hist / gl(gN*) with today's baryons c1 gN* and settled baryons c0 gN* (no response). a0 units."""
    g_today = c1 * gNs; g0 = c0 * gNs
    return (g_today + gl(g0) - g0) / gl(gNs)
RG = np.unique(np.concatenate([np.geomspace(1e-4, 1e4, 3000), [R12]]))   # r_1/2 on the shell grid (run-1 KA4 fix, pre-grading)
PL = RG ** 3 / (1 + RG * RG) ** 1.5
PL12 = R12 ** 3 / (1 + R12 ** 2) ** 1.5
def hist_AD(y, c1, c0, return_check=False):
    """adiabatic edge at one y (a = 1, a0 = 1): settled mu_b0 = c0 y PL, cold mu_c0 = r^2 [gl(mu_b0/r^2) - mu_b0/r^2];
    final baryons c1 y PL; each cold shell keeps r M_tot(<r). Returns g_AD(r12) / gl(gN*(r12))."""
    mb0 = c0 * y * PL; mc0 = RG ** 2 * (gl(mb0 / RG ** 2) - mb0 / RG ** 2); J = RG * (mb0 + mc0)
    lo = np.log10(RG).copy(); hi = np.full(RG.shape, 8.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi); rm = 10 ** mid
        val = rm * (c1 * y * rm ** 3 / (1 + rm * rm) ** 1.5 + mc0) - J
        lo = np.where(val < 0, mid, lo); hi = np.where(val < 0, hi, mid)
    rf = 10 ** (0.5 * (lo + hi))
    mcf = float(np.interp(math.log(R12), np.log(rf), mc0))
    g = (c1 * y * PL12 + mcf) / R12 ** 2
    gs = y * PL12 / R12 ** 2
    if return_check:
        rf_m = rf * (c1 * y * rf ** 3 / (1 + rf * rf) ** 1.5 + mc0)
        return g / float(gl(gs)), float(np.max(np.abs(rf_m / J - 1))), bool(np.all(np.diff(rf) > 0))
    return g / float(gl(gs))
def cfac(L, gas_ratio, q):
    """(c1, c0): today's and settled baryons at r_1/2 in units of the stars' gN*. gas_ratio = 1.33 M_HI / M*."""
    c1 = 1.0 + 2.0 * q * gas_ratio
    eta = (L - 1.0) * (1.0 + gas_ratio)
    return c1, c1 + eta
def P_draws(y, L, gas_ratio, q, edge):
    """log10 g_hist / gl(gN*) per draw; AD through a log-y grid with interpolation."""
    gNs = gNp(R12, y); c1, c0 = cfac(L, gas_ratio, q)
    if edge == "NR":
        return np.log10(hist_NR(gNs, c1, c0))
    ly = np.log10(y); grid = np.linspace(ly.min() - 1e-6, ly.max() + 1e-6, 41)
    vals = np.array([math.log10(hist_AD(10 ** v, c1, c0)) for v in grid])
    return np.interp(ly, grid, vals)
def P_ext(y, L, gas_ratio, q):
    """reported arm: lost gas as a Plummer of scale 2a (NR)."""
    gNs = gNp(R12, y); c1, c0 = cfac(L, gas_ratio, q); eta = c0 - c1
    g2 = eta * y * R12 / (R12 ** 2 + 4.0) ** 1.5
    g0 = c1 * gNs + g2
    return np.log10((c1 * gNs + gl(g0) - g0) / gl(gNs))

# =============================================================================== main build (RB2's stream, exact)
RES = dict(lane="DG1", tag=TAG, criteria="3719fe178d", note="TEST lane: relabels nothing; kappa = 1/2 FITTED; not theory closed",
           footings={}, KA={}, MUTATE={})
P(f"DG1 dwarf data side and gas history under form B {'MUTATE' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
RNG = np.random.default_rng(20261031); DS = {}
for f in FOOTS:
    DS[f] = build(SMP, A0[f], RNG, mvrule=True)
    build(SMP, A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True, mvrule=True)
CLS = {r["name"]: klass(r) for r in SMP}
for r in ULR: CLS[r["name"]] = klass(r)
DSU = {}
for f in FOOTS:                       # upper-limit systems: own stream (does not touch RB2's)
    DSU[f] = build(ULR, A0[f], np.random.default_rng(20261113 + (0 if f == "canonical" else 1)), mvrule=True)
P(f"rows: {len(SMP)} measured (RB2's sample), {len(ULR)} upper-limit-only: " + ", ".join(f"{r['name']} ({CLS[r['name']]}, UL {r['sigma']})" for r in ULR))
GRADED = ("MW ultra-faint", "bright M31", "MW classical")
PER = {}; PERU = {}
for f in FOOTS:
    X = DS[f]; PER[f] = {}
    for i, r in enumerate(X["rows"]):
        v = dsph_prim(X, i, r, A0[f]); PER[f][r["name"]] = dict(med=float(np.median(v)), sd=float(np.std(v)), draws=v, i=i)
    XU = DSU[f]; PERU[f] = {}
    for i, r in enumerate(XU["rows"]):
        v = dsph_prim(XU, i, r, A0[f]); PERU[f][r["name"]] = dict(med=float(np.median(v)), sd=float(np.std(v)), draws=v, i=i)

# =============================================================================== L for every row (P1's copied code)
LS = {}
for r in SMP + ULR:
    LS[r["name"]] = lsys(r["name"], r["logms"])
def Lval(n, key="L0"):
    d = LS.get(n)
    if not d or not d.get("tested"): return None
    return d[key]["L"]
# imputed-width arm (reported): class median LVD width for rows with mean [Fe/H] and no width
IMP = {}
for c in ("bright M31", "MW classical", "LG field", "MW ultra-faint"):
    ws = [LS[r["name"]]["w"]["sig"] for r in SMP if CLS[r["name"]] == c and LS[r["name"]].get("tested") and LS[r["name"]]["w"].get("sig") is not None]
    if not ws: continue
    wmed = float(np.median(ws))
    for r in SMP:
        if CLS[r["name"]] == c and not LS[r["name"]].get("tested") and LS[r["name"]]["feh"] is not None:
            IMP[r["name"]] = lsys(r["name"], r["logms"], width_override=wmed)

if not MUT:
    P("\n=== KNOWN ANSWERS ===")
    # KA1
    d1 = 0.0; nr = 0; dcl = 0.0
    for f in FOOTS:
        ref = {r_["name"]: r_ for r_ in RB2J["footings"][f]["per_system"]}
        for n, v in PER[f].items():
            d1 = max(d1, abs(v["med"] - ref[n]["Delta"]["prim"]), abs(v["sd"] - ref[n]["sd"]["prim"])); nr += 1
        for c in GRADED:
            names = [n for n in PER[f] if CLS[n] == c]
            st = boot_median([PER[f][n]["med"] for n in names], [PER[f][n]["sd"] for n in names])
            dcl = max(dcl, abs(st["median"] - RB2J["footings"][f]["classes"][c]["stats"]["prim"]["median"]))
    KA = {"KA1": dict(rows=nr, max_abs=d1, class_max_abs=dcl)}
    check("KA1", d1 <= 1e-9 and dcl <= 1e-9, f"RB2 per-system Delta[prim], sd reproduced over {nr} rows: max |d| {d1:.1e}; C2 class medians max |d| {dcl:.1e} (line 1e-9)")
    # KA2
    d2 = 0.0; n2 = 0; miss = []
    for n, pr in P1CSV.items():
        if pr["tested"] != "True": continue
        d = LS.get(n) or lsys(n, 0.0)
        for key, col in (("L0", "L_MDF_I0_m05"), ("Llo", "L_MDF_I2_m05"), ("Lhi", "L_MDF_hi_p01")):
            ref = fl(pr[col])
            if ref is None or not d.get("tested"): miss.append((n, col)); continue
            d2 = max(d2, abs(d[key]["L"] / ref - 1)); n2 += 1
    KA["KA2"] = dict(n=n2, max_rel=d2, missing=miss)
    check("KA2", d2 <= 1e-6 and not miss, f"P1's L_MDF (central, 2-sigma-low, upper edge) reproduced by the copied lmdf: {n2} values, max rel {d2:.1e} (line 1e-6); missing {miss}")
    # KA3
    se2j = json.load(open(os.path.join(CL, "..", "closure_2026_11_06", "SE2_step_as_systematics", "se2.json")))
    d3 = 0.0
    for f in FOOTS:
        W = se2_widths(f)
        for c in DCLS:
            ref = se2j["footings"][f]["dsph_widths"][c]
            d3 = max(d3, abs(W[c]["a_c"] - ref["a_c"]), abs(W[c]["m_c"] - ref["m_c"]))
    KA["KA3"] = dict(max_abs=d3)
    check("KA3", d3 <= 1e-9, f"SE2's stored a_c and m_c per class reproduced (copied width block on X1's CSV): max |d| {d3:.1e} (line 1e-9)")
    # KA4
    y = np.geomspace(1e-6, 1e2, 30)
    a = float(np.max(np.abs(np.log10(hist_NR(gNp(R12, y), 1.0, 1.0)))))
    b = max(abs(math.log10(hist_AD(yy, 1.0, 1.0))) for yy in (1e-6, 1e-3, 1.0))
    dl = max(abs(float(np.log10(hist_NR(gNp(R12, 1e-8), 1.0, LL))) - 0.5 * math.log10(LL)) for LL in (2.0, 18.0, 60.0))
    _, inv, mono = hist_AD(1e-3, 1.0, 20.0, return_check=True)
    rise = all(np.diff([float(np.log10(hist_NR(gNp(R12, 1e-3), 1.0, LL))) for LL in (1, 2, 5, 20, 60)]) > 0)
    rise_ad = all(np.diff([math.log10(hist_AD(1e-3, 1.0, LL)) for LL in (1, 2, 5, 20, 60)]) > 0)
    KA["KA4"] = dict(L1_NR=a, L1_AD=b, deep_limit=dl, AD_invariant=inv, AD_monotone=mono, rises=rise and rise_ad)
    check("KA4", a <= 1e-12 and b <= 1e-12 and dl <= 1e-3 and inv <= 1e-9 and mono and rise and rise_ad,
          f"history: L=1 -> P {a:.1e} (NR) / {b:.1e} (AD); deep limit vs (1/2) log L {dl:.1e} (line 1e-3); AD r M(<r) kept to {inv:.1e} (line 1e-9), shells ordered {mono}; P rises with L {rise and rise_ad}")
    # KA5
    rng = np.random.default_rng(5); x = rng.normal(0, 1, 31); x2 = rng.normal(0, 1, 30)
    k1 = abs(km_median(x, np.zeros(31, bool))[0] - np.median(x)); k2 = abs(km_median(x2, np.zeros(30, bool))[0] - np.median(x2))
    xx = np.concatenate([x, np.full(5, 10.0)]); cc = np.concatenate([np.zeros(31, bool), np.ones(5, bool)])
    k3 = abs(km_median(xx, cc)[0] - km_median(x, np.zeros(31, bool))[0])
    kb = km_boot(x, np.full(31, 0.1), np.zeros(31, bool)); bb = boot_median(x, np.full(31, 0.1)); k4 = abs(kb["median"] - bb["median"]) + abs(kb["ci95"][0] - bb["ci95"][0])
    sd = np.full(31, 0.2); ml = cens_ml(x, sd, np.zeros(31, bool))
    from scipy.stats import norm as N_
    mu_w = minimize(lambda p: -np.sum(N_.logpdf(x, p[0], np.sqrt(math.exp(p[1]) ** 2 + sd ** 2))), [0.0, math.log(0.5)], method="Nelder-Mead",
                    options=dict(xatol=1e-10, fatol=1e-12, maxiter=8000)).x[0]
    k5 = abs(ml["mu"] - mu_w)
    KA["KA5"] = dict(odd=k1, even=k2, bounds_above=k3, boot_equal=k4, ml=k5)
    check("KA5", max(k1, k2, k4) <= 1e-12 and k3 <= 1e-12 and k5 <= 1e-6,
          f"KM median = median (odd {k1:.1e}, even {k2:.1e}); bounds above all -> unchanged {k3:.1e}; km_boot = boot_median {k4:.1e}; censored ML with none censored {k5:.1e}")
    KA_OK = all(CHK[k]["ok"] for k in ("KA1", "KA2", "KA3", "KA4", "KA5"))
    RES["KA"] = KA
else:
    KA_OK = True

def class_names(f, c, with_ul=False):
    n = [r["name"] for r in DS[f]["rows"] if CLS[r["name"]] == c]
    if with_ul: n += [r["name"] for r in DSU[f]["rows"] if CLS[r["name"]] == c]
    return n
def per_of(f, n):
    return PER[f][n] if n in PER[f] else PERU[f][n]
def is_cens(n):
    return any(r["name"] == n for r in ULR)

# =============================================================================== PART A
def partA(f):
    a0 = A0[f]; out = {}
    # A1 censoring (RB2's draws for measured; own stream for the bounds)
    A1 = {}
    for c in ("MW ultra-faint", "bright M31", "MW classical", "M31 others"):
        nm = class_names(f, c, True)
        v = [per_of(f, n)["med"] for n in nm]; s = [per_of(f, n)["sd"] for n in nm]; cz = [is_cens(n) for n in nm]
        st = km_boot(v, s, cz); st["bounds"] = {n: per_of(f, n)["med"] for n in nm if is_cens(n)}
        try: st["ml"] = cens_ml(v, s, cz)
        except Exception as e: st["ml"] = dict(error=str(e))
        st["measured_only"] = boot_median([PER[f][n]["med"] for n in class_names(f, c)], [PER[f][n]["sd"] for n in class_names(f, c)])
        A1[c] = st
    out["A1"] = A1
    # A2 arms: one paired rebuild of measured + UL rows per arm (seed 20261110 + footing)
    rows_all = SMP + ULR
    arms = dict(a0=dict(binmode="free"), **{"a+": dict(binmode="off")}, af07=dict(binmode="f07"), alow=dict(binmode="free", sig_src="lower"),
                afl=dict(binmode="free", floor=1.0), adown=dict(binmode="f07", sig_src="lower", floor=1.0))
    A2 = {}
    for arm, kw in arms.items():
        Xa = build(rows_all, a0, np.random.default_rng(20261110 + (0 if f == "canonical" else 1)), mvrule=True, **kw)
        dd = {}
        for i, r in enumerate(Xa["rows"]):
            v = dsph_prim(Xa, i, r, a0); dd[r["name"]] = (float(np.median(v)), float(np.std(v)), bool(Xa["cens"][i]))
        A2[arm] = {}
        for c in ("MW ultra-faint", "bright M31", "MW classical"):
            nm = [n for n in dd if CLS.get(n) == c]
            A2[arm][c] = km_boot([dd[n][0] for n in nm], [dd[n][1] for n in nm], [dd[n][2] for n in nm])
        A2[arm]["_per"] = dd
    out["A2"] = A2
    # A3 SE2 budget re-derived for B (+ sd noise), and A-full with censoring
    W = se2_widths(f)
    def rowinfo(n):
        r = next(x for x in rows_all if x["name"] == n); lv = r["_raw"]
        mhi = fl(lv.get("mass_HI")); ul = fl(lv.get("mass_HI_ul"))
        em, ep = fl(lv.get("distance_modulus_em")), fl(lv.get("distance_modulus_ep"))
        sdd = ((em + ep) / 2 / 5) if (em is not None and ep is not None) else 0.0
        y0 = G * 10 ** r["logms"] * MSUN / ((r["rh"] * PC) ** 2 * a0)
        adm = dsph_admiss_v(r["host"], r["rh"], r["sigma"], Rh_X1(r) / KPC)
        p = per_of(f, n)
        return dict(name=n, D=p["med"], sd=p["sd"], x=float(gNp(R12, y0)), Ms=10 ** r["logms"], MHI=10 ** mhi if mhi is not None else 0.0,
                    UL=(10 ** ul) if (ul is not None and mhi is None) else 0.0, sd_logd=sdd, adm=adm, cens=is_cens(n))
    def post(c, rows, spec, with_sd=True, cens=True, nominal=False):
        rs, rn = rngs(c, f); rsd = np.random.default_rng(SEEDS[c] * 10 + (0 if f == "canonical" else 1) + 900000)
        R = [r for r in rows if r["adm"]["A1"] and r["adm"]["A2"] and (cens or not r["cens"])]
        n = len(R)
        D = np.array([r["D"] for r in R]); gN = np.array([r["x"] for r in R]); Ms = np.array([r["Ms"] for r in R])
        MHI = np.array([r["MHI"] for r in R]); UL = np.array([r["UL"] for r in R]); sdd = np.array([r["sd_logd"] for r in R])
        sd = np.array([0.0 if r["cens"] else r["sd"] for r in R]); cz = np.array([r["cens"] for r in R])
        dU = rn.normal(spec["ups"][0], spec["ups"][1], NDRAW) if spec["ups"][1] > 0 else np.full(NDRAW, spec["ups"][0])
        q = uni(rn, spec["q"], NDRAW * n).reshape(NDRAW, n)
        mul = (UL[None] * rn.uniform(0, 1, (NDRAW, n))) if spec["ul"] else np.zeros((NDRAW, n))
        gas = 1.33 * (MHI[None] + mul)
        dd = rn.normal(0, 1, (NDRAW, n)) * sdd[None] * spec["dist"]
        da = rn.normal(0, 1, NDRAW) * W[c]["a_c"] * spec["aniso"]; ds = rn.normal(0, 1, NDRAW) * W[c]["m_c"] * spec["memb"]
        if nominal: dU[:] = 0; q[:] = 0; gas[:] = 0; dd[:] = 0; da[:] = 0; ds[:] = 0
        Bf = 10 ** dU[:, None] + 2 * q * gas / Ms[None]
        noise = rsd.normal(0, 1, (NDRAW, n)) * sd[None] if with_sd else 0.0
        Dp = D[None] + noise + 2 * ds[:, None] + da[:, None] - dd - dlaw(Bf, gN[None])
        ix = rs.integers(0, n, (NDRAW, n))
        if not (cens and cz.any()):
            x = np.median(Dp[np.arange(NDRAW)[:, None], ix], axis=1)
        else:
            x = np.empty(NDRAW)
            for d_ in range(NDRAW):
                x[d_] = km_median(Dp[d_, ix[d_]], cz[ix[d_]])[0]
        qq = np.percentile(x, [2.5, 16, 50, 84, 97.5])
        return dict(median=float(qq[2]), ci68=[float(qq[1]), float(qq[3])], ci95=[float(qq[0]), float(qq[4])], contains0=bool(qq[0] <= 0 <= qq[4]),
                    n=n, n_cens=int(cz.sum()), excluded=[r["name"] for r in rows if not (r["adm"]["A1"] and r["adm"]["A2"])])
    A3 = {}
    for c in ("MW ultra-faint", "bright M31", "MW classical"):
        rows = [rowinfo(n) for n in class_names(f, c, True)]
        A3[c] = dict(budget_measured=post(c, rows, SPEC_MAIN, cens=False), budget_se2_verbatim=post(c, rows, SPEC_MAIN, with_sd=False, cens=False),
                     full=post(c, rows, SPEC_MAIN, cens=True), widths=dict(a_c=W[c]["a_c"], m_c=W[c]["m_c"]))
    # A-full with the adown arm's values
    for c in ("MW ultra-faint", "bright M31"):
        rows = []
        for n in class_names(f, c, True):
            ri = rowinfo(n); v = A2["adown"]["_per"][n]; ri.update(D=v[0], sd=v[1], cens=v[2]); rows.append(ri)
        A3[c]["full_adown"] = post(c, rows, SPEC_MAIN, cens=True)
    out["A3"] = A3
    out["outcome"] = {c: ("FAILS HIGH SURVIVES THE DATA-SIDE REGRADE" if A3[c]["full"]["ci95"][0] > 0 else "DOES NOT SURVIVE")
                      for c in ("MW ultra-faint", "bright M31")}
    d6 = max(abs(A1[c]["measured_only"]["median"] - RB2J["footings"][f]["classes"][c]["stats"]["prim"]["median"]) for c in ("MW ultra-faint", "bright M31", "MW classical"))
    d6a = max(abs(A2["a0"][c]["median"] - A1[c]["median"]) for c in ("MW ultra-faint", "bright M31", "MW classical"))
    check(f"KA6[{f}]", d6 <= 1e-9, f"Part A on RB2's stream with no censoring (arm a0, measured only) = RB2's C2 class medians: max |d| {d6:.1e} (line 1e-9); "
          f"the paired a0 rebuild (own seed) differs from A1 by up to {d6a:.3f} dex (seed noise, reported)")
    out["KA6"] = dict(max_abs=d6, a0_rebuild_vs_A1=d6a)
    for arm in A2: A2[arm].pop("_per")
    return out

# =============================================================================== PART B
def hist_rows(f, Lkey="L0", q=0.25, Lover=None, imputed=False):
    """per system: Delta_B (RB2 prim), sd, P per edge (median over draws), R_H per edge (median, sd), L, logM*, log r12."""
    X = DS[f]; out = {}
    for r in X["rows"]:
        n = r["name"]; c = CLS[n]
        if c not in GRADED + ("LG field",) and n not in ("Crater II", "IC 1613"): continue
        src = IMP if imputed else LS
        d = src.get(n)
        if not d or not d.get("tested"): continue
        L = d[Lkey]["L"] if Lover is None else Lover[n]
        i = PER[f][n]["i"]; y = 10 ** X["ly"][i]; gr = d["Mg"] / (10 ** r["logms"]) if d["Mg"] > 0 else 0.0
        row = dict(name=n, cls=c, L=L, Lflag=d[Lkey]["flag"] if Lover is None else "scrambled", gas_ratio=gr,
                   D=PER[f][n]["med"], sd=PER[f][n]["sd"], logms=r["logms"], logr12=math.log10(R12 * r["rh"]))
        for e in ("NR", "AD"):
            Pd = P_draws(y, L, gr, q, e); RH = PER[f][n]["draws"] - Pd
            row[f"P_{e}"] = float(np.median(Pd)); row[f"RH_{e}"] = float(np.median(RH)); row[f"sdRH_{e}"] = float(np.std(RH))
        Pe = P_ext(y, L, gr, q); row["P_ext"] = float(np.median(Pe)); row["RH_ext"] = float(np.median(PER[f][n]["draws"] - Pe))
        row["y0"] = float(G * 10 ** r["logms"] * MSUN / ((r["rh"] * PC) ** 2 * A0[f]))
        out[n] = row
    return out
def L_need_v0(row, edge):
    """run-2 version (kept for the A1 check on NR): assumes P rises with L."""
    y0 = row["y0"]; gr = row["gas_ratio"]; target = row["D"]
    def Pc(lL):
        c1, c0 = cfac(10 ** lL, gr, 0.25)
        if edge == "NR": return math.log10(float(hist_NR(gNp(R12, y0), c1, c0)))
        return math.log10(hist_AD(y0, c1, c0))
    if target <= Pc(0.0): return 1.0
    if Pc(6.0) < target: return float("inf")
    return 10 ** brentq(lambda lL: Pc(lL) - target, 0.0, 6.0, xtol=1e-6)
def L_need(row, edge, with_ceiling=False):
    """A1: the smallest L in [1, 1e6] with P(L) = Delta_B (241-point scan in log10 L, brentq on the first sign change);
    infinity only if the edge's ceiling max_L P(L) is below Delta_B."""
    y0 = row["y0"]; gr = row["gas_ratio"]; target = row["D"]
    def Pc(lL):
        c1, c0 = cfac(10 ** lL, gr, 0.25)
        if edge == "NR": return math.log10(float(hist_NR(gNp(R12, y0), c1, c0)))
        return math.log10(hist_AD(y0, c1, c0))
    grid = np.linspace(0.0, 6.0, 241); vals = np.array([Pc(v) for v in grid])
    k = int(np.argmax(vals)); ceil_ = (float(vals[k]), float(10 ** grid[k]))
    if target <= vals[0]:
        res = 1.0
    else:
        above = np.where(vals >= target)[0]
        if not above.size:
            res = float("inf")
        else:
            j = int(above[0]); res = 10 ** brentq(lambda lL: Pc(lL) - target, grid[j - 1], grid[j], xtol=1e-8)
    return (res, ceil_) if with_ceiling else res
def gates(f, H, edge, power=True, nperm=10000, g5on=True):
    G_ = {}
    names = [n for n in H if H[n]["cls"] in GRADED]
    # G1
    g1 = {}
    for c in GRADED:
        nm = [n for n in names if H[n]["cls"] == c]
        st = boot_median([H[n][f"RH_{edge}"] for n in nm], [H[n][f"sdRH_{edge}"] for n in nm])
        st["before"] = boot_median([H[n]["D"] for n in nm], [H[n]["sd"] for n in nm])
        lo, hi = st["ci95"]; st["label"] = "PASS" if lo <= 0 <= hi else ("FAIL HIGH" if lo > 0 else "FAIL LOW")
        g1[c] = st
    G_["G1"] = dict(classes=g1, verdict="PASS" if all(g1[c]["label"] == "PASS" for c in GRADED) else "FAIL")
    # G2 / G3
    idx = {n: k for k, n in enumerate(names)}
    groups = [np.array([idx[n] for n in names if H[n]["cls"] == c]) for c in GRADED]
    Dv = np.array([H[n]["D"] for n in names]); Pv = np.array([H[n][f"P_{edge}"] for n in names])
    lm = np.array([H[n]["logms"] for n in names]); lr = np.array([H[n]["logr12"] for n in names])
    S, p1, p2 = perm_test(groups, Dv, Pv, nperm, 20261110)
    sl = demeaned_slope(groups, Dv, Pv, 4000, 20261111)
    per_cls = {c: float(np.sum(zrank(Dv[g]) * zrank(Pv[g]))) for c, g in zip(GRADED, groups)}
    g2pass = bool(S > 0 and p1 <= 0.05 and sl["contains1"])
    G_["G2"] = dict(S=S, p_one=p1, p_two=p2, slope=sl, rho_per_class=per_cls, verdict="PASS" if g2pass else "FAIL")
    g3 = {}
    for key, z in (("G3m", lm), ("G3r", lr)):
        Dr = resid_on(groups, Dv, z); Pr = resid_on(groups, Pv, z)
        S3, q1, q2 = perm_test(groups, Dr, Pr, nperm, 20261110)
        rhoPz = {c: float(np.sum(zrank(Pv[g]) * zrank(z[g]))) for c, g in zip(GRADED, groups)}
        g3[key] = dict(S=S3, p_one=q1, p_two=q2, rho_P_with_control=rhoPz, verdict="PASS" if (S3 > 0 and q1 <= 0.05) else "FAIL")
    G_.update(g3)
    # power (plants)
    if power:
        rms = RB2M["MUTATE"][f]["M2"]["true_rms"]["pooled"]
        sd = np.array([H[n]["sd"] for n in names])
        wv = float(np.mean([np.var(Pv[g]) for g in groups]))
        tau = math.sqrt(max(0.05 ** 2, rms ** 2 - float(np.median(sd ** 2)) - wv))
        rng = np.random.default_rng(20261112); npl = 500; npp = 1000
        gs = [g for g in groups if len(g) >= 3]; den = sum(len(g) for g in gs)
        permsx = [np.argsort(rng.random((npp, len(g))), axis=1) for g in gs]
        Pres = {"G2": Pv, "G3m": resid_on(groups, Pv, lm), "G3r": resid_on(groups, Pv, lr)}
        zx = {k: [zrank(v[g]) for g in gs] for k, v in Pres.items()}
        bsi = [rng.integers(0, len(g), (300, len(g))) for g in gs]
        passes = {"G2": 0, "G3m": 0, "G3r": 0}
        for _ in range(npl):
            Dsyn = Pv + rng.normal(0, 1, len(Pv)) * np.sqrt(sd ** 2 + tau ** 2)
            for k in passes:
                Dk = Dsyn if k == "G2" else resid_on(groups, Dsyn, lm if k == "G3m" else lr)
                zy = [zrank(Dk[g]) for g in gs]
                S0 = sum(len(g) * float(np.sum(zy[i] * zx[k][i])) for i, g in enumerate(gs)) / den
                Sp = sum(len(g) * (zx[k][i][permsx[i]] @ zy[i]) for i, g in enumerate(gs)) / den
                p = (1 + np.sum(Sp >= S0 - 1e-12)) / (npp + 1)
                ok = S0 > 0 and p <= 0.05
                if ok and k == "G2":
                    bs = np.empty(300)
                    for b in range(300):
                        xs = np.concatenate([Pv[g][bsi[i][b]] - Pv[g][bsi[i][b]].mean() for i, g in enumerate(gs)])
                        ys = np.concatenate([Dsyn[g][bsi[i][b]] - Dsyn[g][bsi[i][b]].mean() for i, g in enumerate(gs)])
                        bs[b] = np.sum(xs * ys) / np.sum(xs * xs)
                    lo_, hi_ = np.percentile(bs, [2.5, 97.5]); ok = lo_ <= 1 <= hi_
                passes[k] += ok
        pw = {k: v / npl for k, v in passes.items()}
        G_["power"] = dict(tau=tau, rms_RB2=rms, within_var_P=wv, rates=pw)
        for k in ("G2", "G3m", "G3r"):
            if pw[k] < 0.5: G_[k]["verdict"] = "NO POWER"
    # G4a
    fn = [n for n in H if H[n]["cls"] == "LG field"]
    if len(fn) >= 5:
        st = boot_median([H[n][f"RH_{edge}"] for n in fn], [H[n][f"sdRH_{edge}"] for n in fn])
        lo, hi = st["ci95"]; st["label"] = "PASS" if lo <= 0 <= hi else ("FAIL HIGH" if lo > 0 else "FAIL LOW")
        st["before_gas"] = boot_median([H[n]["D"] for n in fn], [H[n]["sd"] for n in fn]); st["names"] = fn
        G_["G4a"] = dict(stat=st, verdict="PASS" if st["label"] == "PASS" else "FAIL")
    else:
        G_["G4a"] = dict(verdict="NOT EVALUABLE", n=len(fn))
    # G4b
    order = sorted(names, key=lambda n: H[n][f"P_{edge}"]); low = order[: max(1, len(order) // 3)]
    st = boot_median([H[n][f"RH_{edge}"] for n in low], [H[n][f"sdRH_{edge}"] for n in low])
    st["names"] = low; st["P_max"] = max(H[n][f"P_{edge}"] for n in low)
    G_["G4b"] = dict(stat=st, verdict="FAIL" if st["ci95"][0] > 0 else "PASS")
    # G5 (A1: smallest root; ceilings recorded)
    if not g5on:
        G_["G5"] = dict(verdict="NOT RUN (MUTATE)")
        return G_
    g5 = {}; nrchk = 0.0
    for c in GRADED:
        nm = [n for n in names if H[n]["cls"] == c]
        lc = [L_need(H[n], edge, with_ceiling=True) for n in nm]; ln = [a for a, _ in lc]; lu = [Lval(n, "Lhi") for n in nm]
        if edge == "NR":
            for n, a in zip(nm, ln):
                b = L_need_v0(H[n], edge)
                if math.isfinite(a) or math.isfinite(b): nrchk = max(nrchk, abs(a / b - 1) if (math.isfinite(a) and math.isfinite(b)) else float("inf"))
        g5[c] = dict(median_L_need=float(np.median(ln)), median_L_upper=float(np.median(lu)), median_L_central=float(np.median([H[n]["L"] for n in nm])),
                     n_exceed=int(sum(1 for a, b in zip(ln, lu) if a > b)), n=len(nm), n_unreachable=int(sum(1 for a in ln if not math.isfinite(a))),
                     per_system={n: dict(L_need=a, ceiling_P=cc[0], ceiling_at_L=cc[1], L_upper=u, D=H[n]["D"]) for n, a, cc, u in zip(nm, ln, [x for _, x in lc], lu)},
                     ok=bool(np.median(ln) <= np.median(lu)))
    G_["G5"] = dict(classes=g5, verdict="PASS" if all(g5[c]["ok"] for c in GRADED) else "FAIL", NR_vs_run2_max_rel=nrchk if edge == "NR" else None)
    return G_
def edge_state(G_):
    keys = ("G1", "G2", "G3m", "G3r", "G4a", "G4b", "G5")
    v = {k: G_[k]["verdict"] for k in keys}
    if all(x == "PASS" for x in v.values()): return "CLOSES", v
    if any(x == "FAIL" for x in v.values()): return "FAILS", v
    return "OPEN", v

if not KA_OK:
    P("A KNOWN ANSWER FAILED: grading stops (FROZEN section 5).")
elif not MUT:
    for f in FOOTS:
        a0 = A0[f]; FR = {}
        P(f"\n================ [{f}] a0 {a0:.4e}")
        # ---------- coverage
        cov = {c: dict(n=len(class_names(f, c)), with_L=[n for n in class_names(f, c) if Lval(n) is not None],
                       imputed=[n for n in class_names(f, c) if n in IMP]) for c in GRADED + ("LG field",)}
        P("coverage (rows with an L from P1's copied code): " + "; ".join(f"{c} {len(v['with_L'])}/{v['n']} (+{len(v['imputed'])} imputed width, reported)" for c, v in cov.items()))
        FR["coverage"] = cov
        # ---------- PART A
        A = partA(f); FR["A"] = A
        P("--- Part A (data side) ---")
        for c in ("MW ultra-faint", "bright M31", "MW classical", "M31 others"):
            st = A["A1"][c]
            ml = st["ml"]
            P(f"  A1 censored KM {c:15s}: N {st['n']} ({st['n_cens']} upper limits) median {st['median']:+.3f} [{st['ci95'][0]:+.3f}, {st['ci95'][1]:+.3f}]"
              f" (measured only {st['measured_only']['median']:+.3f} [{st['measured_only']['ci95'][0]:+.3f}, {st['measured_only']['ci95'][1]:+.3f}]); "
              f"ML mu {ml.get('mu', float('nan')):+.3f} [{ml.get('ci95', [float('nan')] * 2)[0]:+.3f}, {ml.get('ci95', [float('nan')] * 2)[1]:+.3f}] tau {ml.get('tau', float('nan')):.3f}")
            if st["bounds"]: P("     bounds (dex, true residual at or below): " + ", ".join(f"{k} {v:+.2f}" for k, v in st["bounds"].items()))
        for arm, d in A["A2"].items():
            P(f"  A2 arm {arm:5s}: " + " | ".join(f"{c} {d[c]['median']:+.3f} [{d[c]['ci95'][0]:+.3f}, {d[c]['ci95'][1]:+.3f}] ({d[c]['n_cens']} cens)" for c in ("MW ultra-faint", "bright M31", "MW classical")))
        for c in ("MW ultra-faint", "bright M31", "MW classical"):
            d = A["A3"][c]
            P(f"  A3 {c:15s} (a_c {d['widths']['a_c']:.3f}, m_c {d['widths']['m_c']:.3f}): budget {d['budget_measured']['median']:+.3f} [{d['budget_measured']['ci95'][0]:+.3f}, {d['budget_measured']['ci95'][1]:+.3f}]"
              f" N {d['budget_measured']['n']} | SE2 verbatim {d['budget_se2_verbatim']['median']:+.3f} [{d['budget_se2_verbatim']['ci95'][0]:+.3f}, {d['budget_se2_verbatim']['ci95'][1]:+.3f}]"
              f" | A-full (censored + budget) {d['full']['median']:+.3f} [{d['full']['ci95'][0]:+.3f}, {d['full']['ci95'][1]:+.3f}] N {d['full']['n']} ({d['full']['n_cens']} cens); excluded {d['full']['excluded']}")
            if "full_adown" in d:
                P(f"     A-full on the adown arm: {d['full_adown']['median']:+.3f} [{d['full_adown']['ci95'][0]:+.3f}, {d['full_adown']['ci95'][1]:+.3f}]")
        P("  PART A OUTCOME: " + "; ".join(f"{c}: {v}" for c, v in A["outcome"].items()))
        # ---------- PART B
        P("--- Part B (history) ---")
        H = hist_rows(f); FR["B_rows"] = H
        P(f"  {'system':18s} {'class':14s} {'L':>7s} {'flag':6s} {'D_B':>7s} {'sd':>5s} {'P_NR':>6s} {'P_AD':>6s} {'R_NR':>7s} {'R_AD':>7s} {'P_ext':>6s} {'logM*':>6s}")
        for n, h in sorted(H.items(), key=lambda kv: (kv[1]["cls"], kv[1]["P_NR"])):
            P(f"  {n:18s} {h['cls']:14s} {h['L']:7.2f} {h['Lflag'][:6]:6s} {h['D']:+7.3f} {h['sd']:5.3f} {h['P_NR']:+6.3f} {h['P_AD']:+6.3f} {h['RH_NR']:+7.3f} {h['RH_AD']:+7.3f} {h['P_ext']:+6.3f} {h['logms']:6.2f}")
        FR["B"] = {}
        for e in ("NR", "AD"):
            Gx = gates(f, H, e); st, v = edge_state(Gx); Gx["state"] = st
            FR["B"][e] = Gx
            P(f"  [edge {e}] state {st}: " + ", ".join(f"{k} {x}" for k, x in v.items()))
            for c in GRADED:
                g = Gx["G1"]["classes"][c]
                P(f"     G1 {c:15s} N {g['n']:2d}: after history {g['median']:+.3f} [{g['ci95'][0]:+.3f}, {g['ci95'][1]:+.3f}] {g['label']} (before, same rows {g['before']['median']:+.3f} [{g['before']['ci95'][0]:+.3f}, {g['before']['ci95'][1]:+.3f}])")
            g2 = Gx["G2"]
            P(f"     G2 S {g2['S']:+.3f} p(one) {g2['p_one']:.4f} slope {g2['slope']['slope']:+.2f} [{g2['slope']['ci95'][0]:+.2f}, {g2['slope']['ci95'][1]:+.2f}] per class rho "
              + ", ".join(f"{c} {v_:+.2f}" for c, v_ in g2["rho_per_class"].items()) + f" -> {g2['verdict']}")
            for k in ("G3m", "G3r"):
                g3 = Gx[k]
                P(f"     {k} S {g3['S']:+.3f} p(one) {g3['p_one']:.4f}; rho(P, control) " + ", ".join(f"{c} {v_:+.2f}" for c, v_ in g3["rho_P_with_control"].items()) + f" -> {g3['verdict']}")
            pw = Gx["power"]; P(f"     power (plants): tau {pw['tau']:.3f}; G2 {pw['rates']['G2']:.2f}, G3m {pw['rates']['G3m']:.2f}, G3r {pw['rates']['G3r']:.2f}")
            g4 = Gx["G4a"]
            if "stat" in g4:
                s4 = g4["stat"]; P(f"     G4a LG field N {s4['n']}: after HI + history {s4['median']:+.3f} [{s4['ci95'][0]:+.3f}, {s4['ci95'][1]:+.3f}] {s4['label']} (stars only {s4['before_gas']['median']:+.3f})")
            else:
                P(f"     G4a {g4['verdict']} (N {g4['n']})")
            s4 = Gx["G4b"]["stat"]; P(f"     G4b least-loss third (P <= {s4['P_max']:.3f}, N {s4['n']}): {s4['median']:+.3f} [{s4['ci95'][0]:+.3f}, {s4['ci95'][1]:+.3f}] -> {Gx['G4b']['verdict']}")
            for c in GRADED:
                g5 = Gx["G5"]["classes"][c]
                P(f"     G5 {c:15s}: median L need {g5['median_L_need']:.2f} vs upper {g5['median_L_upper']:.2f} (central {g5['median_L_central']:.2f}); {g5['n_exceed']}/{g5['n']} exceed, {g5['n_unreachable']} beyond the edge's ceiling -> {'ok' if g5['ok'] else 'FAIL'}")
            if e == "NR":
                P(f"     A1 check: NR L_need unchanged from run 2's root finder, max rel {Gx['G5']['NR_vs_run2_max_rel']:.1e} (line 1e-4)")
            else:
                P("     AD ceilings (max_L P at central values, L at the ceiling; D_B): " + "; ".join(f"{n} {v['ceiling_P']:+.2f}@{v['ceiling_at_L']:.0f} ({v['D']:+.2f})" for c_ in GRADED for n, v in Gx["G5"]["classes"][c_]["per_system"].items()))
        # L-sensitivity, HI share, imputed and extended arms (reported)
        rep = {}
        for lab, kw in (("L lower edge", dict(Lkey="Llo")), ("L upper edge", dict(Lkey="Lhi")), ("HI q 0", dict(q=0.0)), ("HI q 0.5", dict(q=0.5))):
            Hx = hist_rows(f, **kw); rep[lab] = {}
            for e in ("NR", "AD"):
                Gx = gates(f, Hx, e, power=False, nperm=2000)
                rep[lab][e] = dict(G1={c: (Gx["G1"]["classes"][c]["median"], Gx["G1"]["classes"][c]["ci95"], Gx["G1"]["classes"][c]["label"]) for c in GRADED},
                                   G4a=(Gx["G4a"]["stat"]["median"], Gx["G4a"]["stat"]["ci95"], Gx["G4a"]["stat"]["label"]) if "stat" in Gx["G4a"] else None,
                                   G5=Gx["G5"]["verdict"], G2=(Gx["G2"]["S"], Gx["G2"]["p_one"]))
                P(f"  reported [{lab}, {e}]: G1 " + "; ".join(f"{c} {v_[0]:+.3f} [{v_[1][0]:+.3f}, {v_[1][1]:+.3f}] {v_[2]}" for c, v_ in rep[lab][e]["G1"].items())
                  + (f" | G4a {rep[lab][e]['G4a'][0]:+.3f} {rep[lab][e]['G4a'][2]}" if rep[lab][e]["G4a"] else "") + f" | G5 {rep[lab][e]['G5']} | G2 S {rep[lab][e]['G2'][0]:+.3f} p {rep[lab][e]['G2'][1]:.3f}")
        Hi = hist_rows(f, imputed=True)
        rep["imputed width rows"] = {n: dict(cls=h["cls"], L=h["L"], D=h["D"], P_NR=h["P_NR"], RH_NR=h["RH_NR"]) for n, h in Hi.items()}
        if Hi:
            P("  reported [imputed class-median width, never graded]: " + "; ".join(f"{n} L {h['L']:.1f} D {h['D']:+.2f} P {h['P_NR']:+.2f}" for n, h in Hi.items()))
            bm = [n for n in H if H[n]["cls"] == "bright M31"] + [n for n in Hi if Hi[n]["cls"] == "bright M31"]
            HH = {**H, **Hi}
            st = boot_median([HH[n]["RH_NR"] for n in bm], [HH[n]["sdRH_NR"] for n in bm])
            rep["bright M31 with imputed rows, NR G1"] = st
            P(f"  reported: bright M31 G1 (NR) with the imputed rows, N {st['n']}: {st['median']:+.3f} [{st['ci95'][0]:+.3f}, {st['ci95'][1]:+.3f}]")
        ext = [H[n]["RH_ext"] for n in H if H[n]["cls"] in GRADED]
        rep["extended lost gas (2a), NR, class medians"] = {c: float(np.median([H[n]["RH_ext"] for n in H if H[n]["cls"] == c])) for c in GRADED}
        P("  reported [lost gas as a Plummer of 2a, NR]: median after-history residual " + ", ".join(f"{c} {v_:+.3f}" for c, v_ in rep["extended lost gas (2a), NR, class medians"].items()))
        FR["B_reported"] = rep
        # ---------- label for this footing
        states = {e: FR["B"][e]["state"] for e in ("NR", "AD")}
        if any(s == "CLOSES" for s in states.values()):
            lab = "HISTORY CLOSES THE HIGH ROWS (" + ", ".join(e for e, s in states.items() if s == "CLOSES") + ")"
        elif all(s == "FAILS" for s in states.values()):
            lab = "HISTORY DOES NOT CLOSE THEM"
        else:
            lab = "NO VERDICT"
        Lsens = []
        for e in ("NR", "AD"):
            base = FR["B"][e]["G1"]["verdict"]
            for edge_lab in ("L lower edge", "L upper edge"):
                g1v = "PASS" if all(v_[2] == "PASS" for v_ in rep[edge_lab][e]["G1"].values()) else "FAIL"
                if g1v != base or rep[edge_lab][e]["G5"] != FR["B"][e]["G5"]["verdict"]: Lsens.append(f"{e}: {edge_lab}")
        FR["label"] = lab; FR["edge_states"] = states; FR["L_sensitive"] = Lsens
        P(f"  LABEL [{f}]: {lab}{' (L-sensitive: ' + '; '.join(Lsens) + ')' if Lsens else ''} | Part A: " + "; ".join(f"{c} {v}" for c, v in A["outcome"].items()))
        # ---------- PART C numbers (history on the LOW rows that have an L)
        lowP = {}
        for n in ("IC 1613", "Crater II", "NGC 147", "Cassiopeia III"):
            h = H.get(n)
            lowP[n] = dict(D=PER[f][n]["med"], sd=PER[f][n]["sd"], L=h["L"] if h else None, P_NR=h["P_NR"] if h else None, RH_NR=h["RH_NR"] if h else None)
        FR["C"] = lowP
        P("--- Part C (history on the LOW rows) --- " + "; ".join(f"{n}: D_B {v['D']:+.3f}" + (f", L {v['L']:.2f}, P {v['P_NR']:+.3f}, after history {v['RH_NR']:+.3f}" if v["L"] else ", no L on disk") for n, v in lowP.items()))
        # ---------- PART D (Weisz 2014 on disk; reported)
        RES["footings"][f] = FR
        P(f"  peak RSS {rss_gb():.3f} GB, {time.time() - T0:.0f} s")

    # =========================================================================== PART D (footing-independent tau90, footing-specific residuals)
    def weisz():
        def rd(fn):
            L_ = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "dsph", "weisz2014_dl", fn)) if l.strip() and not l.startswith("#")]
            hd = L_[0]; return [dict(zip(hd, [x.strip() for x in row])) for row in L_[3:] if len(row) == len(hd)]
        t5 = rd("table5.tsv"); t6 = rd("table6.tsv")
        def tau90(row):
            cols = sorted([(float(k[1:]), fl(v)) for k, v in row.items() if re.fullmatch(r"f\d+\.\d+", k) and fl(v) is not None], key=lambda kv: -kv[0])
            if not cols: return None, "no SFH"
            if cols[0][1] >= 0.9: return 10 ** cols[0][0] / 1e9, "cap (>= 90 % before the oldest bin)"
            for (t1, f1), (t2, f2) in zip(cols[:-1], cols[1:]):
                if f1 < 0.9 <= f2:
                    lt = t1 + (0.9 - f1) / (f2 - f1) * (t2 - t1); return 10 ** lt / 1e9, "ok"
            return None, "never reaches 0.9"
        out = {}
        for row in t6:
            out.setdefault(row["ID"], (tau90(row), "table 6"))
        for row in t5:
            out.setdefault(row["ID"], (tau90(row), f"table 5 field {row['Field']}"))
        alias = {"Canes Venetici I": "Canes Venatici I", "Canes Venetici II": "Canes Venatici II", "Sag DIG": "Sagittarius dIrr",
                 "Pegasus": "Pegasus dIrr", "Sex A": "Sextans A", "Sex B": "Sextans B"}
        return {alias.get(k, k): dict(tau90=v[0][0], flag=v[0][1], src=v[1]) for k, v in out.items()}
    TAU = weisz()
    RES["partD_tau90"] = TAU
    P("\n=== PART D (Weisz 2014 tau90 on disk; reported, not in the label) ===")
    for f in FOOTS:
        H = RES["footings"][f]["B_rows"]; D_ = {}
        for c in GRADED + ("LG field",):
            nm = [n for n in class_names(f, c) if n in TAU and TAU[n]["tau90"] is not None]
            D_[c] = dict(rows={n: dict(tau90=TAU[n]["tau90"], flag=TAU[n]["flag"], D=PER[f][n]["med"], RH_NR=H[n]["RH_NR"] if n in H else None) for n in nm})
        allc = [c for c in D_ if len(D_[c]["rows"]) >= 3]
        names = [n for c in allc for n in D_[c]["rows"]]; idx = {n: k for k, n in enumerate(names)}
        groups = [np.array([idx[n] for n in D_[c]["rows"]]) for c in allc]
        Dv = np.array([PER[f][n]["med"] for n in names]); Tv = np.array([TAU[n]["tau90"] for n in names])
        d1 = perm_test(groups, Dv, Tv, 10000, 20261114) if names else None
        hn = [n for n in names if n in H]; hidx = {n: k for k, n in enumerate(hn)}
        hgroups = [np.array([hidx[n] for n in hn if CLS[n] == c]) for c in allc]
        RHv = np.array([H[n]["RH_NR"] for n in hn]); Th = np.array([TAU[n]["tau90"] for n in hn])
        d2 = perm_test(hgroups, RHv, Th, 10000, 20261115) if hn else None
        RES["footings"][f]["D"] = dict(classes=D_, D1=dict(S=d1[0], p_one=d1[1], p_two=d1[2], n=len(names), classes=allc) if d1 else None,
                                       D2=dict(S=d2[0], p_one=d2[1], p_two=d2[2], n=len(hn)) if d2 else None)
        P(f"[{f}] overlap: " + "; ".join(f"{c} {len(D_[c]['rows'])}" for c in D_) + f". D1 (Delta_B on tau90, within class, classes with >= 3): S {d1[0]:+.3f} p(one) {d1[1]:.4f} N {len(names)}"
          + (f" | D2 (after history on tau90): S {d2[0]:+.3f} p(two) {d2[2]:.4f} N {len(hn)}" if d2 else ""))
        for c in D_:
            P(f"    {c}: " + ", ".join(f"{n} tau90 {v['tau90']:.1f} Gyr{'*' if v['flag'] != 'ok' else ''} D {v['D']:+.2f}" for n, v in sorted(D_[c]["rows"].items(), key=lambda kv: -kv[1]["tau90"])))
    # =========================================================================== LABELS
    P("\n=== LABELS ===")
    for f in FOOTS:
        FR = RES["footings"][f]
        P(f"  {f}: {FR['label']}{' (L-sensitive: ' + '; '.join(FR['L_sensitive']) + ')' if FR['L_sensitive'] else ''}; edges {FR['edge_states']}; Part A: "
          + "; ".join(f"{c} {v}" for c, v in FR["A"]["outcome"].items()))
    RES["labels"] = {f: dict(label=RES["footings"][f]["label"], L_sensitive=RES["footings"][f]["L_sensitive"], partA=RES["footings"][f]["A"]["outcome"]) for f in FOOTS}
else:
    # =========================================================================== MUTATE
    P("\n=== MUTATE ===")
    for f in FOOTS:
        MU = {}
        H = hist_rows(f)
        G0s = {e: gates(f, H, e, power=False, g5on=False) for e in ("NR", "AD")}
        rng = np.random.default_rng(4242 + (0 if f == "canonical" else 1))
        SC = {e: dict(Ss=[], npass=0, g1shift=[]) for e in ("NR", "AD")}
        for _ in range(20):
            Lover = {}
            for c in GRADED + ("LG field",):
                nm = [n for n in H if H[n]["cls"] == c]; Ls_ = [H[n]["L"] for n in nm]; p = rng.permutation(len(nm))
                for j, n in enumerate(nm): Lover[n] = Ls_[p[j]]
            for n in H:
                Lover.setdefault(n, H[n]["L"])
            Hs = hist_rows(f, Lover=Lover)
            for e in ("NR", "AD"):
                Gs = gates(f, Hs, e, power=False, nperm=2000, g5on=False)
                SC[e]["Ss"].append(Gs["G2"]["S"]); SC[e]["npass"] += Gs["G2"]["verdict"] == "PASS"
                SC[e]["g1shift"].append(max(abs(Gs["G1"]["classes"][c]["median"] - G0s[e]["G1"]["classes"][c]["median"]) for c in GRADED))
        for e in ("NR", "AD"):
            G0 = G0s[e]; S0 = G0["G2"]["S"]; Ss = SC[e]["Ss"]; npass = SC[e]["npass"]; g1shift = SC[e]["g1shift"]
            bites = npass <= 2 and float(np.median(Ss)) < S0
            MU[f"M1_{e}"] = dict(S_true=S0, S_scrambled_median=float(np.median(Ss)), S_scrambled=Ss, pass_rate=npass / 20, max_G1_shift_median=float(np.median(g1shift)),
                                 bites=bool(bites), note=None if S0 > float(np.median(Ss)) else "unscrambled S not above the scrambled median: no history ordering to destroy")
            P(f"[{f}] M1 ({e}) L scrambled within class x20: G2 S true {S0:+.3f}, scrambled median {np.median(Ss):+.3f}, pass rate {npass}/20 -> {'BITES' if bites else 'DOES NOT BITE'}"
              + ("" if S0 > float(np.median(Ss)) else " (no history ordering to destroy)"))
        # M2: stellar-mass power law in place of history
        names = [n for n in H if H[n]["cls"] in GRADED]
        lm = np.array([H[n]["logms"] for n in names]); Dv = np.array([H[n]["D"] for n in names])
        A_ = np.vstack([np.ones(len(names)), lm - 6.0]).T; coef, *_ = np.linalg.lstsq(A_, Dv, rcond=None)
        Ppl = A_ @ coef
        out = {}
        for e in ("NR", "AD"):
            Ph = np.array([H[n][f"P_{e}"] for n in names])
            rss_h = float(np.sum((Dv - Ph) ** 2)); rss_p = float(np.sum((Dv - Ppl) ** 2)); nn = len(names)
            bic_h = nn * math.log(rss_h / nn); bic_p = nn * math.log(rss_p / nn) + 2 * math.log(nn)
            rho = {c: float(np.sum(zrank(Ph[[k for k, n in enumerate(names) if H[n]['cls'] == c]]) * zrank(lm[[k for k, n in enumerate(names) if H[n]['cls'] == c]]))) for c in GRADED}
            Hp = {n: dict(H[n]) for n in H}
            for k, n in enumerate(names):
                Hp[n][f"P_{e}"] = float(Ppl[k]); Hp[n][f"RH_{e}"] = H[n]["D"] - float(Ppl[k]); Hp[n][f"sdRH_{e}"] = H[n]["sd"]
            Gp = gates(f, Hp, e, power=False, nperm=2000, g5on=False)
            G0 = gates(f, H, e, power=False, nperm=2000, g5on=False)
            g3pass = G0["G3m"]["verdict"] == "PASS" and G0["G3r"]["verdict"] == "PASS"
            if bic_h < bic_p - 2: reading = "HISTORY BEATS THE POWER LAW"
            elif max(abs(v) for v in rho.values()) >= 0.7 and not g3pass: reading = "SAME TREND RENAMED"
            else: reading = "NOT SEPARATED"
            shift = max(abs(Gp["G1"]["classes"][c]["median"] - G0["G1"]["classes"][c]["median"]) for c in GRADED)
            out[e] = dict(coef=[float(coef[0]), float(coef[1])], rms_hist=math.sqrt(rss_h / nn), rms_pl=math.sqrt(rss_p / nn), BIC_hist=bic_h, BIC_pl=bic_p,
                          rho_Phist_logM=rho, reading=reading, G1_pl={c: (Gp["G1"]["classes"][c]["median"], Gp["G1"]["classes"][c]["ci95"]) for c in GRADED},
                          G2_pl=(Gp["G2"]["S"], Gp["G2"]["p_one"]), G4a_pl=Gp["G4a"].get("stat", {}).get("median"), bites=bool(shift > 0.01), G1_shift=shift)
            P(f"[{f}] M2 ({e}) power law a {coef[0]:+.3f} b {coef[1]:+.3f}: rms hist {out[e]['rms_hist']:.3f} vs power law {out[e]['rms_pl']:.3f}; BIC {bic_h:.1f} vs {bic_p:.1f}; "
              f"rho(P_hist, log M*) " + ", ".join(f"{c} {v:+.2f}" for c, v in rho.items()) + f" -> {reading}; G1 under P_pl "
              + ", ".join(f"{c} {v[0]:+.3f}" for c, v in out[e]["G1_pl"].items()) + f"; {'BITES' if out[e]['bites'] else 'DOES NOT BITE'}")
        MU["M2"] = out
        RES["MUTATE"][f] = MU

RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = rss_gb()
P(f"\nruntime {time.time() - T0:.0f} s, peak RSS {rss_gb():.3f} GB. kappa = 1/2 FITTED; not theory closed. Relabels nothing.")
RES["out"] = OUT
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if k != "draws"}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (bool, np.bool_)): return bool(o)
    if isinstance(o, (int, np.integer)): return int(o)
    if isinstance(o, (float, np.floating)): return float(o) if math.isfinite(float(o)) else None
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
