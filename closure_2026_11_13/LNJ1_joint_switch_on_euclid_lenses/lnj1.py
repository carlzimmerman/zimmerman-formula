#!/usr/bin/env python3
"""LNJ1 (FROZEN_CRITERIA.md, 640fbf99e4): is the ceiling break in Euclid's lenses the crossing-speed joint's switch?
Per lens: which side of v*(z_l) (JNT2's model rule from the stars; measured-speed bracket from theta_E); below, the law on
the stars (EUC1's formula, re-coded); above, stars + FRZ1's reference cold dark energy halo at X = 5.41, Newtonian,
projected in a cylinder inside R_E. Boost against s, residual against the joint, free step break s_b with bootstrap.
Twins TW-H (v*/2), TW-D (2 v*), TW-SH (stellar masses shuffled) written as lnj1_MUTATE_<twin>.json / .out.
Owners' code imported read-only (EUC1's euc1.py for cosmology and Sersic functions; JNT2's jnt2_common.py); FRZ1's halo
functions copied. Bytecode writing is off, so nothing is written outside this folder.
  nice -n 19 python3 lnj1.py
TEST lane. POST HOC twice. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, csv, json, math, hashlib, warnings, importlib.util, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
os.environ.pop("EUC1_MUTATE", None)
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
def rel(p): return os.path.relpath(p, REPO)
def load_mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E = load_mod("euc1_ro", os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling", "euc1.py"))
J = load_mod("jnt2_common_ro", os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_common.py"))
EUC10 = os.path.join(REPO, "closure_2026_11_12", "EUC10_published_source_redshifts", "euc10_partB_samples.csv")
PD1J = os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
G, MSUN, PC, KPC, ARCSEC, C = E.G, E.MSUN, E.PC, E.KPC, E.ARCSEC, E.C
MPC_M = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}       # this lane's footings
A0_EUC = dict(E.FOOT)                                     # the EUC lanes' (alt 1.132e-10), known answers only
FOOTS = ("canonical", "alt")
SEED = 20261113; NBOOT = 400; NMIN = 20; ZS_INF = E.ZS_INF; GUARD = 0.2
SHIFT_COMMON = -0.222 + 0.258                            # EUC12: - delta_E(all P) + delta_S
XC = 5.41
GLX, GLW = E.GLX, E.GLW
P("LNJ1: the crossing-speed joint's switch on Euclid's lenses (criteria 640fbf99e4). TEST lane. POST HOC twice. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# ============================================================ data (own loader)
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()
def fl(v):
    try: return float(v)
    except Exception: return float("nan")
for fn, hx in E.SHA.items():
    ok = sha256(os.path.join(DATA, fn)) == hx
    P(f"  sha256 {fn}: {'matches EUC1 frozen hash' if ok else 'MISMATCH'}")
    if not ok: sys.exit("data hash mismatch")
obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(os.path.join(DATA, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8"))}
ROWS = []
for r in csv.DictReader(open(os.path.join(DATA, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8")):
    o = obj.get(r["unique_identifier"])
    if o is None: continue
    d = dict(id=r["unique_identifier"], grade=r["lens_grade"].strip(), success=r["lens_model_success"].strip() == "True",
             final=r["final_sample"].strip() == "True", large=o["large_system_warning"].strip() == "True",
             z=fl(r["eclipse_median_phz"]), lm=fl(r["eclipse_log_survived_mass_med"]), tE=fl(r["eclipse_effective_einstein_radius"]),
             te=fl(r["eclipse_effective_radius"]), n=fl(r["eclipse_sersic_index"]))
    ROWS.append(d)
def sel(grades):
    return [r for r in ROWS if r["grade"] in grades and r["success"] and r["final"] and not r["large"]
            and r["tE"] > 0 and r["te"] > 0 and 0.6 <= r["n"] <= 10.0 and r["z"] > 0 and r["lm"] > 0]
S = sel(("A", "B"))
N = len(S)
ID = [r["id"] for r in S]; GR = np.array([r["grade"] for r in S])
Z = np.array([r["z"] for r in S]); LM0 = np.array([r["lm"] for r in S]); TE = np.array([r["tE"] for r in S])
THE = np.array([r["te"] for r in S]); NS = np.array([r["n"] for r in S])
DA = E.EUCLID.DA(Z); RE = TE * ARCSEC * DA; REFF = THE * ARCSEC * DA
isA = GR == "A"; isB = GR == "B"
P(f"  sample S (EUC1 cuts, grades A + B): N = {N} (A {isA.sum()}, B {isB.sum()}); median z_l {np.median(Z):.3f}, theta_E {np.median(TE):.3f}\"")

# ============================================================ law S and the stars
U = np.arccosh(np.maximum(1.0e6 * KPC / RE, 1.0 + 1e-9))
RN = RE[:, None] * np.cosh(GLX[None, :] * U[:, None])            # (N, 400) radii
PREF = RE ** 2 / G * U
GN1 = G * MSUN * E.M3D_frac(RN, REFF[:, None], NS[:, None]) / RN ** 2   # g_N per Msun of stars
F2D = E.M2D_frac(RE, REFF, NS)
def M2D_g(g, idx=None):
    pr = PREF if idx is None else PREF[idx]
    return pr * np.sum(GLW[None, :] * g, axis=1)
def m_law(Mstar_sun, a0, idx=None):
    g1 = GN1 if idx is None else GN1[idx]
    return M2D_g(E.g_law(Mstar_sun[:, None] * g1, a0, "S"), idx)
LOGB = np.round(np.arange(-1.5, 1.5001, 0.05), 4)
def btable(lm, a0, idx=None):
    """log10 M_law at stellar boost 10^LOGB, per lens (rows) -> b_* for any M_obs by interpolation."""
    return np.stack([np.log10(m_law(10 ** (lm + lb), a0, idx)) for lb in LOGB], axis=1)
def b_star(tab, logMobs):
    k = np.clip((tab < logMobs[:, None]).sum(axis=1), 1, len(LOGB) - 1)
    i = np.arange(len(logMobs)); y0, y1 = tab[i, k - 1], tab[i, k]
    return LOGB[k - 1] + (logMobs - y0) / (y1 - y0) * (LOGB[k] - LOGB[k - 1])

def m_obs(zs): return math.pi * RE ** 2 * E.EUCLID.sigcr(Z, zs)

# ============================================================ FRZ1's halo (copied from frz1_hm.py / cfg556_halo_model.py)
hh = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / hh ** 2; FB = om_b / (om_b + om_c); RHO_M = Om * 2.77536627e11
m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def Omz(z): return Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om)
def conc_fn(z, cfac=1.0): return lambda M: cfac * 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
def halo_basics_z(M, conc, dta, omz):
    c = conc(M); r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-12)
    xc = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - 1.0 / omz, 0.05, 1.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc, r200c=xc * r2, M200c=M * m_nfw(c * xc) / mc)
def halo_direct(X, Mb_sun, z, cfac=1.0):
    conc = conc_fn(z, cfac); dta = dta_of(z); omz = Omz(z); Mta = X * Mb_sun * hh / (1 - FB)
    lM = brentq(lambda l: halo_basics_z(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
    hb = halo_basics_z(10 ** lM, conc, dta, omz); a = MPC_M / hh / (1 + z)
    return hb["rs"] * a, hb["rta"] * a, hb
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
    """physical r_s, r_ta (m) per lens from the table (bilinear: z nodes, then log M_ta)."""
    lmta, lrs, lrta = halo_table(cfac)
    t = np.log10(X * Mb_sun * hh / (1 - FB)); zi = np.clip(np.searchsorted(ZG, z) - 1, 0, len(ZG) - 2); w = (z - ZG[zi]) / (ZG[zi + 1] - ZG[zi])
    out = []
    for arr in (lrs, lrta):
        v0 = np.array([np.interp(t[k], lmta[zi[k]], arr[zi[k]]) for k in range(len(t))])
        v1 = np.array([np.interp(t[k], lmta[zi[k] + 1], arr[zi[k] + 1]) for k in range(len(t))])
        out.append(10 ** ((1 - w) * v0 + w * v1))
    return out[0], out[1]
def c_cyl(Xarr, Mb_sun, rs, rta):
    r = np.minimum(RN, rta[:, None]); Cr = (Xarr * Mb_sun * MSUN)[:, None] * m_nfw(r / rs[:, None]) / m_nfw(rta / rs)[:, None]
    return M2D_g(G * Cr / RN ** 2)

PD1 = json.load(open(PD1J))
XTAB = {f: {zk: float(np.median([r["share_over_Mb"] for r in PD1[f]["share_tables"][zk]])) for zk in ("z0.0", "z1.0")} for f in FOOTS}

# ============================================================ speeds
EZ = np.array([J.E(z) for z in Z])
def vL(lm): return (10 * J.G * (1 + J.XS) * 10 ** lm * J.MSUN * J.H0 * EZ) ** (1 / 3) / 1e3
def vstar(ft, fac=1.0): return fac * J.vstar0_kms(ft) / EZ
def vmeas(Mobs): return np.sqrt(2 * G * Mobs / (math.pi * RE)) / 1e3

# ============================================================ statistics
CAND = np.round(np.arange(-1.0, 0.6001, 0.01), 3)
def step_fit(x, y, w):
    o = np.argsort(x); xs = x[o]; cw = np.concatenate([[0.0], np.cumsum(w[o])]); cy = np.concatenate([[0.0], np.cumsum((w * y)[o])])
    pos = np.searchsorted(xs, CAND, "left"); nlo = cw[pos]; klo = cy[pos]; nhi = cw[-1] - nlo; khi = cy[-1] - klo
    with np.errstate(all="ignore"):
        flo = klo / nlo; fhi = khi / nhi
        def ll(k, n, f): return np.where(k > 0, k * np.log(np.where(f > 0, f, 1)), 0) + np.where(n - k > 0, (n - k) * np.log(np.where(f < 1, 1 - f, 1)), 0)
        L = ll(klo, nlo, flo) + ll(khi, nhi, fhi)
    ok = (nlo >= NMIN) & (nhi >= NMIN) & (fhi > flo)
    if not ok.any(): return None
    L = np.where(ok, L, -np.inf); k = int(np.argmax(L))
    return dict(logsb=float(CAND[k]), sb=float(10 ** CAND[k]), flo=float(flo[k]), fhi=float(fhi[k]), df=float(fhi[k] - flo[k]), nlo=int(nlo[k]), nhi=int(nhi[k]))
def boot_w(rng, n): return np.bincount(rng.integers(0, n, n), minlength=n).astype(float)
def break_fit(x, y, seed=SEED):
    """x = log10 s (or log10 theta_E), y = above-band flags."""
    m = step_fit(x, y, np.ones(len(x)))
    rng = np.random.default_rng(seed); sb, df = [], []
    for _ in range(NBOOT):
        r = step_fit(x, y, boot_w(rng, len(x)))
        if r is None: df.append(0.0)
        else: sb.append(r["logsb"]); df.append(r["df"])
    if m is None: return dict(fit=None, real=False, df_lo=0.0)
    sb = np.array(sb); df = np.array(df)
    m.update(logsb_lo=float(np.percentile(sb, 2.5)) if len(sb) else float("nan"), logsb_hi=float(np.percentile(sb, 97.5)) if len(sb) else float("nan"),
             df_lo=float(np.percentile(df, 2.5)), df_hi=float(np.percentile(df, 97.5)), n_valid=int(len(sb)))
    m["sb_lo"], m["sb_hi"] = 10 ** m["logsb_lo"], 10 ** m["logsb_hi"]
    return dict(fit=m, real=bool(m["df_lo"] >= 0.20), df_lo=m["df_lo"])
def med_ci(v, seed):
    if len(v) == 0: return dict(n=0, med=float("nan"), lo=float("nan"), hi=float("nan"))
    rng = np.random.default_rng(seed); bs = [np.median(v[rng.integers(0, len(v), len(v))]) for _ in range(NBOOT)]
    return dict(n=int(len(v)), med=float(np.median(v)), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)))
def frac_ci(y, seed):
    if len(y) == 0: return dict(n=0, f=float("nan"), lo=float("nan"), hi=float("nan"))
    rng = np.random.default_rng(seed); bs = [np.mean(y[rng.integers(0, len(y), len(y))]) for _ in range(NBOOT)]
    return dict(n=int(len(y)), f=float(np.mean(y)), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)))
def dfrac_at1(s, y, seed):
    a, b = y[s >= 1], y[s < 1]
    if len(a) < 1 or len(b) < 1: return dict(d=float("nan"), hi=float("nan"))
    rng = np.random.default_rng(seed); bs = [np.mean(a[rng.integers(0, len(a), len(a))]) - np.mean(b[rng.integers(0, len(b), len(b))]) for _ in range(NBOOT)]
    return dict(d=float(np.mean(a) - np.mean(b)), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)))
SBINS = [0, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.25, np.inf]
def running_cross(s, y, lev, w=101):
    o = np.argsort(s); ys = y[o].astype(float); ss = s[o]
    if len(ys) < w: return float("nan")
    rm = np.convolve(ys, np.ones(w) / w, "valid"); sm = ss[w // 2: w // 2 + len(rm)]
    k = np.where(rm >= lev)[0]
    return float(sm[k[0]]) if len(k) else float("nan")

def joint_line(ci):
    if ci["n"] == 0 or not np.isfinite(ci["med"]): return "NONE"
    if ci["lo"] > 0.10: return "UNDER"
    if ci["hi"] < -0.10: return "OVER"
    return "FITS"

def evaluate(ft, lm, rule, zs, X="cosmic", cfac=1.0, vfac=1.0, tag=""):
    """one configuration through statistics (a)-(c) and the raw word."""
    a0 = A0[ft]; Ms = 10 ** lm
    key = (ft, hash(lm.tobytes()))
    if key not in CACHE:
        CACHE[key] = dict(law=m_law(Ms, a0), lawhi=m_law(Ms * 10 ** 0.25, a0))
    law, lawhi = CACHE[key]["law"], CACHE[key]["lawhi"]
    hk = (hash(lm.tobytes()), X, cfac, ft if X == "pd1" else "")
    if hk not in HCACHE:
        Xarr = np.full(N, XC) if X == "cosmic" else np.where(Z < 1, XTAB[ft]["z0.0"], XTAB[ft]["z1.0"])
        rs, rta = halo_interp(Xarr, Ms, Z, cfac)
        HCACHE[hk] = Ms * MSUN * F2D + c_cyl(Xarr, Ms, rs, rta)
    mj = HCACHE[hk]
    Mo = m_obs(zs) if np.ndim(zs) == 0 else math.pi * RE ** 2 * E.EUCLID.sigcr(Z, zs)
    v = vL(lm) if rule == "model" else vmeas(Mo)
    s = v / vstar(ft, vfac)
    above = Mo > lawhi; b = np.log10(Mo / law); up = s >= 1
    pred = np.where(up, mj, law); r = np.log10(Mo / pred)
    R = dict(N_above=int(up.sum()), N_below=int((~up).sum()), s_med=float(np.median(s)), s_max=float(np.max(s)),
             frac_above_band=dict(below=frac_ci(above[~up], SEED + 1), above=frac_ci(above[up], SEED + 2)),
             resid=dict(below=med_ci(r[~up], SEED + 3), above=med_ci(r[up], SEED + 4)),
             joint_vs_law_above=float(np.median(np.log10(mj[up] / law[up]))) if up.any() else float("nan"),
             dfrac_at1=dfrac_at1(s, above, SEED + 5))
    bins = []
    for lo, hi in zip(SBINS[:-1], SBINS[1:]):
        m = (s >= lo) & (s < hi)
        if m.sum() == 0: bins.append(dict(lo=lo, hi=float(hi), n=0)); continue
        bins.append(dict(lo=lo, hi=float(hi), n=int(m.sum()), b_med=float(np.median(b[m])), f_above=float(np.mean(above[m])),
                         r_joint_med=float(np.median(r[m])), r_joint_med_if_ref=float(np.median(np.log10(Mo[m] / mj[m])))))
    R["bins"] = bins
    R["break"] = break_fit(np.log10(s), above.astype(float))
    R["cross25"] = running_cross(s, above, 0.25); R["cross50"] = running_cross(s, above, 0.50)
    R["f_above_all"] = float(np.mean(above))
    # raw word
    bk = R["break"]; jl = joint_line(R["resid"]["above"]) if R["N_above"] >= NMIN else "NONE"
    fb_below = R["frac_above_band"]["below"]["f"]
    if bk["real"]:
        f = bk["fit"]; inside = f["sb_lo"] <= 1.0 <= f["sb_hi"]
        if inside:
            if R["N_above"] < NMIN: w, d = "NO POWER", "break interval contains 1 but N(s>=1) < 20"
            elif jl == "FITS" and fb_below <= 0.20: w, d = "SWITCH AT THE JOINT'S SPEED", "HIT, post hoc, awaits independent re-grade"
            elif jl in ("UNDER", "OVER"): w, d = f"JOINT {jl}-PREDICTS ABOVE THE BOUNDARY", f"median r {R['resid']['above']['med']:+.3f}"
            else: w, d = "LAW FAILS BELOW", f"fraction above band below {fb_below:.3f}"
        else:
            w = "SWITCH AT ANOTHER SPEED"; d = f"s_b {f['sb']:.3f} [{f['sb_lo']:.3f}, {f['sb_hi']:.3f}]"
            if jl in ("UNDER", "OVER"): d += f"; beside: joint {jl}-predicts above (median r {R['resid']['above']['med']:+.3f}, N {R['N_above']})"
        R["side"] = "inside" if inside else ("below" if f["sb_hi"] < 1 else "above")
    else:
        R["side"] = "none"
        if R["N_below"] >= NMIN and R["N_above"] >= NMIN and R["dfrac_at1"]["hi"] < 0.10: w, d = "NO SWITCH", ""
        elif jl in ("UNDER", "OVER"): w, d = f"JOINT {jl}-PREDICTS ABOVE THE BOUNDARY", f"median r {R['resid']['above']['med']:+.3f}"
        else: w, d = "NO POWER", "no real break and too few lenses on one side"
    R["raw_word"], R["raw_detail"] = w, d
    R["_s"], R["_above"], R["_b"], R["_r"], R["_mj"], R["_law"], R["_Mo"] = s, above, b, r, mj, law, Mo
    return R
CACHE, HCACHE = {}, {}

def bites(main, tw):
    if tw["raw_word"] != main["raw_word"]: return True
    if abs(tw["N_above"] - main["N_above"]) >= max(5, 0.25 * main["N_above"]): return True
    if main["N_above"] >= NMIN and tw["N_above"] >= NMIN and abs(tw["frac_above_band"]["above"]["f"] - main["frac_above_band"]["above"]["f"]) >= 0.10: return True
    return False
def destroys(main, tw):
    if not main["break"]["real"]: return True
    if not tw["break"]["real"]: return True
    return tw["break"]["fit"]["df"] <= 0.5 * main["break"]["fit"]["df"]
def full(ft, lm, rule, zs, X="cosmic", cfac=1.0, shuffle_perm=None, twins=True):
    m = evaluate(ft, lm, rule, zs, X, cfac)
    res = dict(main=m)
    if twins:
        res["TWH"] = evaluate(ft, lm, rule, zs, X, cfac, vfac=0.5)
        res["TWD"] = evaluate(ft, lm, rule, zs, X, cfac, vfac=2.0)
        res["TWSH"] = evaluate(ft, lm[shuffle_perm], rule, zs, X, cfac)
        bh, bd = bites(m, res["TWH"]), bites(m, res["TWD"]); ds = destroys(m, res["TWSH"])
        need = ("TWH", "TWD")
        if m["raw_word"] == "SWITCH AT ANOTHER SPEED": need = ("TWH",) if m["side"] == "below" else ("TWD",)
        gate_tw = all({"TWH": bh, "TWD": bd}[t] for t in need)
        final = m["raw_word"] if (gate_tw and ds) else "NO POWER"
        res["gates"] = dict(TWH_bites=bh, TWD_bites=bd, required=list(need), TWSH_destroys=ds, passed=bool(gate_tw and ds))
        res["final_word"] = final
    return res

def strip(R):
    return {k: v for k, v in R.items() if not k.startswith("_")}

# ============================================================ known answers
P("\n[known answers]")
KA = {}
idsE = [r["id"] for r in E.select(E.load(DATA)[0], ("A", "B"))[0]]
KA["loader"] = dict(same_ids_and_order=(idsE == ID), pass_=bool(idsE == ID))
P(f"  KA-0 own loader against EUC1's load/select (grades A+B): identical ids and order: {idsE == ID} (N {len(idsE)})")
# KA-1 EUC4 / EUC1 fractions, own route
k1 = {}
for nm in FOOTS:
    a0 = A0_EUC[nm]; Mo = m_obs(ZS_INF)
    wb = isB & (TE >= 1.7); pa = isA
    lhi = m_law(10 ** (LM0[wb] + 0.25), a0, np.where(wb)[0]); f_wb = float(np.mean(Mo[wb] > lhi))
    lhp = m_law(10 ** (LM0[pa] + 0.25), a0, np.where(pa)[0]); f_p = float(np.mean(Mo[pa] > lhp))
    k1[nm] = dict(W_B=f_wb, N_WB=int(wb.sum()), P=f_p, N_P=int(pa.sum()))
ok1 = (abs(k1["canonical"]["W_B"] - 0.758) <= 0.001 and abs(k1["alt"]["W_B"] - 0.702) <= 0.001 and k1["canonical"]["N_WB"] == 124
       and abs(k1["canonical"]["P"] - 0.156) <= 0.001 and abs(k1["alt"]["P"] - 0.139) <= 0.001 and k1["canonical"]["N_P"] == 3192)
KA["KA1"] = dict(value=k1, pass_=bool(ok1))
P(f"  KA-1 EUC4 W_B f25 {k1['canonical']['W_B']:.3f} / {k1['alt']['W_B']:.3f} (N {k1['canonical']['N_WB']}; 0.758 / 0.702); EUC1 P f25 {k1['canonical']['P']:.3f} / {k1['alt']['P']:.3f} (N {k1['canonical']['N_P']}; 0.156 / 0.139) -> {'PASS' if ok1 else 'FAIL'}")
# KA-2 EUC13 M1 (AGEL) b_med on P, 200 draws, seed 20261112, via this lane's b table
SB = list(csv.DictReader(open(EUC10, newline="")))
AG = [r for r in SB if r["sample"] == "AGEL"]; zl_s = np.array([float(r["z_l"]) for r in AG]); zs_s = np.array([float(r["z_s"]) for r in AG])
iP = np.where(isA)[0]; zP = Z[iP]
k2 = {}
for nm in FOOTS:
    tab = btable(LM0[iP], A0_EUC[nm], iP)
    rng = np.random.default_rng(20261112); nn = np.argsort(np.abs(zP[:, None] - zl_s[None, :]) / 0.1, axis=1)[:, :10]; md = []
    for it in range(200):
        zs_d = np.full(len(iP), np.nan)
        for t in range(20):
            need = ~np.isfinite(zs_d)
            if not need.any(): break
            pick = zs_s[nn[need, rng.integers(0, 10, need.sum())]]; ok = pick > zP[need] + 0.2
            ii = np.where(need)[0][ok]; zs_d[ii] = pick[ok]
        keep = np.isfinite(zs_d)
        Mo = math.pi * RE[iP][keep] ** 2 * E.EUCLID.sigcr(zP[keep], zs_d[keep])
        md.append(float(np.median(b_star(tab[keep], np.log10(Mo)))))
    k2[nm] = float(np.median(md))
    if nm == "canonical":   # table against direct bisection on 300 lenses at z_s infinity
        idx = np.arange(0, len(iP), max(1, len(iP) // 300))[:300]
        eng = E.Engine(RE[iP][idx], REFF[iP][idx], NS[iP][idx], 10 ** LM0[iP][idx] * MSUN)
        Mo = m_obs(ZS_INF)[iP][idx]; bd = eng.solve_b(Mo, A0_EUC[nm], "S"); bt = b_star(tab[idx], np.log10(Mo))
        KA["KA2_table_vs_bisection_max"] = float(np.max(np.abs(bd - bt)))
ok2 = abs(k2["canonical"] - 0.238) <= 0.003 and abs(k2["alt"] - 0.220) <= 0.003 and KA["KA2_table_vs_bisection_max"] <= 0.003
KA["KA2"] = dict(value=k2, pass_=bool(ok2))
P(f"  KA-2 EUC13 M1 AGEL b_med on P: {k2['canonical']:+.4f} / {k2['alt']:+.4f} (+0.238 / +0.220); b table vs EUC1 bisection max {KA['KA2_table_vs_bisection_max']:.1e} -> {'PASS' if ok2 else 'FAIL'}")
# KA-3 v*(0)
v0 = {nm: J.vstar0_kms(nm) for nm in FOOTS}; ok3 = abs(v0["canonical"] - 668.53) <= 0.01 and abs(v0["alt"] - 807.93) <= 0.01
KA["KA3"] = dict(value=v0, pass_=bool(ok3)); P(f"  KA-3 v*(0) {v0['canonical']:.2f} / {v0['alt']:.2f} km/s (668.53 / 807.93) -> {'PASS' if ok3 else 'FAIL'}")
# KA-4 halo copy against SRJ3 K5 (zC 400569) and table against direct
zk, lmb, Rek = 2.24, 10.95, 4.31; Xk = XTAB["canonical"]["z1.0"]
rs_, rta_, hb = halo_direct(Xk, 10 ** lmb, zk); r200c = hb["r200c"] / hh / (1 + zk) * MPC_M / KPC
Rm = Rek * KPC; gmod = G * (10 ** lmb / 2 * MSUN + Xk * 10 ** lmb * MSUN * m_nfw(Rm / rs_) / m_nfw(rta_ / rs_)) / Rm ** 2
ok4a = abs(r200c / 121.62 - 1) <= 1e-3 and abs(rs_ / KPC / 39.53 - 1) <= 1e-3 and abs(gmod / 4.4290e-10 - 1) <= 1e-3
idx = np.arange(0, N, N // 20)[:20]; errs = []
for k in idx:
    a, b_, _ = halo_direct(XC, 10 ** (LM0[k] + SHIFT_COMMON), Z[k])
    ra, rb = halo_interp(np.array([XC]), np.array([10 ** (LM0[k] + SHIFT_COMMON)]), np.array([Z[k]]))
    errs.append(max(abs(ra[0] / a - 1), abs(rb[0] / b_ - 1)))
ok4b = max(errs) <= 1e-3
KA["KA4"] = dict(r200c_kpc=r200c, rs_kpc=rs_ / KPC, g_mod=gmod, table_vs_direct_max=float(max(errs)), pass_=bool(ok4a and ok4b))
P(f"  KA-4 SRJ3 K5 zC 400569: r_200c {r200c:.2f} kpc (121.62), r_s {rs_ / KPC:.2f} kpc (39.53), g_mod {gmod:.4e} (4.4290e-10); table vs direct on 20 lenses max {max(errs):.1e} -> {'PASS' if ok4a and ok4b else 'FAIL'}")
# KA-5 projection: point mass and untruncated NFW against analytic
k = int(np.argmin(np.abs(TE - np.median(TE)))); Mp = 1e11 * MSUN
e_pt = abs(PREF[k] * np.sum(GLW * G * Mp / RN[k] ** 2) / Mp - 1)
rsk = 30 * KPC; rho_s = 1.0e7 * MSUN / KPC ** 3; Mr = 4 * math.pi * rho_s * rsk ** 3 * m_nfw(RN[k] / rsk)
num = PREF[k] * np.sum(GLW * G * Mr / RN[k] ** 2); x = RE[k] / rsk
ana = 4 * math.pi * rho_s * rsk ** 3 * (math.log(x / 2) + (math.acosh(1 / x) / math.sqrt(1 - x * x) if x < 1 else math.acos(1 / x) / math.sqrt(x * x - 1)))
e_nfw = abs(num / ana - 1); ok5 = e_pt <= 1e-3 and e_nfw <= 1e-3
KA["KA5"] = dict(point=float(e_pt), nfw=float(e_nfw), pass_=bool(ok5))
P(f"  KA-5 projection: point mass {e_pt:.1e}, NFW cylinder vs analytic {e_nfw:.1e} -> {'PASS' if ok5 else 'FAIL'}")
# KA-6 SI hand check of one lens by a second route
Hs = 67.74e3 / (1e6 * PC); Omc = 0.3089
dc = lambda zz: C / Hs * quad(lambda t: 1 / math.sqrt(Omc * (1 + t) ** 3 + 1 - Omc), 0, zz, epsabs=0, epsrel=1e-10, limit=400)[0]
zl = float(Z[k]); dl = dc(zl); ds = dc(1100.0); da = dl / (1 + zl); sc = C ** 2 / (4 * math.pi * G * da) * ds / (ds - dl)
Rk = TE[k] * math.pi / 648000 * da; Mok = math.pi * Rk ** 2 * sc; vk = math.sqrt(2 * G * Mok / (math.pi * Rk)) / 1e3
Hz = 67.4e3 / 3.0856775814913673e22 * math.sqrt(0.3153 * (1 + zl) ** 3 + 0.6847)
vLk = (10 * 6.67430e-11 * 6.41 * 10 ** (LM0[k] + SHIFT_COMMON) * 1.98892e30 * Hz) ** (1 / 3) / 1e3
Mo_l = m_obs(ZS_INF)[k]; e6 = max(abs(Mok / Mo_l - 1), abs(vk / vmeas(m_obs(ZS_INF))[k] - 1), abs(vLk / vL(LM0 + SHIFT_COMMON)[k] - 1),
                                   abs(vLk / J.vL_kms(10 ** (LM0[k] + SHIFT_COMMON), zl) - 1))
ok6 = e6 <= 2e-3
KA["KA6"] = dict(lens=ID[k], z=zl, theta_E=float(TE[k]), Sigma_cr_Msun_pc2=sc / (MSUN / PC ** 2), M_obs_Msun=Mok / MSUN, v_meas=vk, v_L=vLk, max_rel=e6, pass_=bool(ok6))
P(f"  KA-6 SI hand check {ID[k]} (z {zl:.3f}, theta_E {TE[k]:.3f}\"): Sigma_cr {sc / (MSUN / PC ** 2):.0f} Msun/pc^2, M_obs {Mok / MSUN:.3e} Msun, v_meas {vk:.1f}, v_L {vLk:.1f} km/s; max rel diff {e6:.1e} -> {'PASS' if ok6 else 'FAIL'}")
KA_ALL = all(v["pass_"] for kk, v in KA.items() if isinstance(v, dict) and "pass_" in v)
P(f"  known answers: {'all pass' if KA_ALL else 'FAILED -> NOT EVALUABLE'}")

# ============================================================ configurations
PERM = np.random.default_rng(SEED).permutation(N)
LMC = LM0 + SHIFT_COMMON
RES = dict(lane="LNJ1", criteria="640fbf99e4", note="TEST lane; POST HOC twice; adopts nothing; kappa = 1/2 FITTED; not theory closed",
           N=N, shift_common=SHIFT_COMMON, footings=A0, known_answers=KA, foot={})
TWO = {t: dict(lane="LNJ1", twin=t, foot={}) for t in ("TWH", "TWD", "TWSH")}

def summary_line(ft, name, R):
    m = R["main"]; bk = m["break"]; f = bk["fit"]
    bs = (f"s_b {f['sb']:.3f} [{f['sb_lo']:.3f}, {f['sb_hi']:.3f}] df {f['df']:.3f} (lo {f['df_lo']:.3f}) real {bk['real']}" if f else "no break fit")
    ra = m["resid"]["above"]; rb = m["resid"]["below"]
    s = (f"[{ft}] {name:26s} N above/below {m['N_above']}/{m['N_below']} (s med {m['s_med']:.3f}, max {m['s_max']:.3f}); f_above_band below "
         f"{m['frac_above_band']['below']['f']:.3f} / above {m['frac_above_band']['above']['f']:.3f}; {bs}; r_below {rb['med']:+.3f}; r_above {ra['med']:+.3f} "
         f"[{ra['lo']:+.3f}, {ra['hi']:+.3f}] -> raw {m['raw_word']}")
    if "final_word" in R:
        g = R["gates"]; s += f" | TWH bites {g['TWH_bites']} TWD bites {g['TWD_bites']} (req {g['required']}) TWSH destroys {g['TWSH_destroys']} -> {R['final_word']}"
    P(s)

for ft in FOOTS:
    P(f"\n[{ft}] a0 {A0[ft]:.4e} m/s^2; v*(0) {J.vstar0_kms(ft):.2f} km/s; v*(z_l) median {np.median(vstar(ft)):.1f} km/s")
    F = RES["foot"][ft] = {}
    cfg = {}
    cfg["primary"] = full(ft, LMC, "model", ZS_INF, shuffle_perm=PERM)
    cfg["catalogue_scale"] = full(ft, LM0, "model", ZS_INF, shuffle_perm=PERM)
    cfg["c_x0.7"] = full(ft, LMC, "model", ZS_INF, cfac=0.7, shuffle_perm=PERM)
    cfg["c_x1.4"] = full(ft, LMC, "model", ZS_INF, cfac=1.4, shuffle_perm=PERM)
    cfg["X_pd1_share"] = full(ft, LMC, "model", ZS_INF, X="pd1", shuffle_perm=PERM)
    cfg["measured_rule"] = full(ft, LMC, "meas", ZS_INF, shuffle_perm=PERM)
    cfg["measured_X_pd1"] = full(ft, LMC, "meas", ZS_INF, X="pd1", shuffle_perm=PERM)   # reported only
    for name in cfg: summary_line(ft, name, cfg[name])
    # AGEL draws (bracket): 50 draws, twins on draw 0
    nnS = np.argsort(np.abs(Z[:, None] - zl_s[None, :]) / 0.1, axis=1)[:, :10]; rng = np.random.default_rng(SEED)
    draws = {"model": [], "meas": []}; d0 = {}
    for it in range(50):
        zs_d = np.full(N, np.nan)
        for t in range(40):
            need = ~np.isfinite(zs_d)
            if not need.any(): break
            pick = zs_s[nnS[need, rng.integers(0, 10, need.sum())]]; ok = pick > Z[need] + GUARD
            ii = np.where(need)[0][ok]; zs_d[ii] = pick[ok]
        zs_d = np.where(np.isfinite(zs_d), zs_d, Z + 3.0)
        for rule in ("model", "meas"):
            if it == 0:
                d0[rule] = full(ft, LMC, rule, zs_d, shuffle_perm=PERM); m = d0[rule]["main"]
            else:
                m = evaluate(ft, LMC, rule, zs_d)
            f = m["break"]["fit"]
            draws[rule].append(dict(raw=m["raw_word"], N_above=m["N_above"], sb=(f["sb"] if f else float("nan")), sb_lo=(f["sb_lo"] if f else float("nan")),
                                    sb_hi=(f["sb_hi"] if f else float("nan")), real=m["break"]["real"], r_above=m["resid"]["above"]["med"], r_below=m["resid"]["below"]["med"],
                                    f_above_band_all=m["f_above_all"]))
    AG_RES = {}
    for rule in ("model", "meas"):
        gp = d0[rule]["gates"]["passed"]
        fw = [d["raw"] if gp else "NO POWER" for d in draws[rule]]
        vals, cnt = np.unique(fw, return_counts=True); maj = str(vals[np.argmax(cnt)])
        AG_RES[rule] = dict(draw0=d0[rule], draws=draws[rule], word_counts=dict(zip(map(str, vals), map(int, cnt))), majority_word=maj,
                            sb_median=float(np.nanmedian([d["sb"] for d in draws[rule]])), r_above_median=float(np.nanmedian([d["r_above"] for d in draws[rule]])),
                            r_below_median=float(np.nanmedian([d["r_below"] for d in draws[rule]])))
        summary_line(ft, f"AGEL draw 0 ({rule})", d0[rule])
        P(f"[{ft}]   AGEL 50 draws ({rule}): words {AG_RES[rule]['word_counts']} -> majority {maj}; s_b median {AG_RES[rule]['sb_median']:.3f}; r_above median {AG_RES[rule]['r_above_median']:+.3f}; r_below median {AG_RES[rule]['r_below_median']:+.3f}")
    cfg["agel_draws"] = d0["model"]
    # break in theta_E (reading)
    m = cfg["primary"]["main"]
    bt = break_fit(np.log10(TE), m["_above"].astype(float))
    F["theta_E_break"] = bt["fit"]
    if bt["fit"]: P(f"[{ft}] break in theta_E (reading): {bt['fit']['sb']:.3f}\" [{bt['fit']['sb_lo']:.3f}, {bt['fit']['sb_hi']:.3f}], f {bt['fit']['flo']:.3f} -> {bt['fit']['fhi']:.3f}")
    # Chabrier-like scale (reported only)
    ch = evaluate(ft, LM0 - 0.222, "model", ZS_INF)
    F["chabrier_reported"] = strip(ch); P(f"[{ft}] Chabrier-like scale (reported only): N above {ch['N_above']}, raw {ch['raw_word']}, f_above_band all {ch['f_above_all']:.3f}")
    # P and B alone (reported)
    for nmx, msk in (("P_only", isA), ("B_only", isB)):
        s = m["_s"][msk]; y = m["_above"][msk]; bb = break_fit(np.log10(s), y.astype(float))
        F[nmx] = dict(N=int(msk.sum()), N_above=int((s >= 1).sum()), f_above=float(np.mean(y)), break_=bb["fit"], real=bb["real"])
        P(f"[{ft}] {nmx} (reported): N {msk.sum()}, N above {int((s >= 1).sum())}, break {('%.3f [%.3f, %.3f] real %s' % (bb['fit']['sb'], bb['fit']['sb_lo'], bb['fit']['sb_hi'], bb['real'])) if bb['fit'] else 'none'}")
    # final word and fragility
    prim = cfg["primary"]["final_word"]
    br = {k: cfg[k]["final_word"] for k in ("catalogue_scale", "c_x0.7", "c_x1.4", "X_pd1_share", "measured_rule")}
    br["agel_draws_majority"] = AG_RES["model"]["majority_word"]
    flips = [k for k, v in br.items() if v != prim]
    word = (prim + (", FRAGILE" if flips else "")) if KA_ALL else "NOT EVALUABLE"
    F.update(word=word, primary_raw=cfg["primary"]["main"]["raw_word"], primary_detail=cfg["primary"]["main"]["raw_detail"], bracket_words=br, flips=flips,
             agel={r: dict((k, v) for k, v in AG_RES[r].items() if k != "draw0") for r in AG_RES})
    F["configs"] = {k: dict(main=strip(v["main"]), gates=v.get("gates"), final_word=v.get("final_word")) for k, v in cfg.items()}
    F["agel_draw0_meas"] = dict(main=strip(d0["meas"]["main"]), gates=d0["meas"]["gates"], final_word=d0["meas"]["final_word"])
    for t in ("TWH", "TWD", "TWSH"):
        TWO[t]["foot"][ft] = {k: dict(main=strip(v[t]), bites_or_destroys=(v["gates"]["TWSH_destroys"] if t == "TWSH" else v["gates"][t + "_bites"]))
                              for k, v in list(cfg.items()) if t in v}
    P(f"[{ft}] WORD: {word}   (primary raw: {F['primary_raw']} {F['primary_detail']}; bracket words {br}; flips {flips})")
    if ft == "canonical": PRIMC = cfg["primary"]["main"]; MEASC = cfg["measured_rule"]["main"]
    else: PRIMA = cfg["primary"]["main"]; MEASA = cfg["measured_rule"]["main"]

P("\nLNJ1: " + " / ".join(RES["foot"][f]["word"] for f in FOOTS) + " (canonical / alt)")
# per-lens table
with open(os.path.join(HERE, "lnj1_per_lens.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["unique_identifier", "grade", "z_l", "theta_E_arcsec", "log_Mstar_common", "logM_obs_inf", "s_model_can", "s_model_alt", "s_meas_can", "s_meas_alt",
                "logM_law_can", "logM_law_alt", "logM_joint_X5.41_can", "above_band_can", "above_band_alt"])
    for i in range(N):
        w.writerow([ID[i], GR[i], "%.4f" % Z[i], "%.4f" % TE[i], "%.4f" % LMC[i], "%.4f" % math.log10(PRIMC["_Mo"][i] / MSUN),
                    "%.4f" % PRIMC["_s"][i], "%.4f" % PRIMA["_s"][i], "%.4f" % MEASC["_s"][i], "%.4f" % MEASA["_s"][i],
                    "%.4f" % math.log10(PRIMC["_law"][i] / MSUN), "%.4f" % math.log10(PRIMA["_law"][i] / MSUN), "%.4f" % math.log10(PRIMC["_mj"][i] / MSUN),
                    int(PRIMC["_above"][i]), int(PRIMA["_above"][i])])
json.dump(RES, open(os.path.join(HERE, "lnj1.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "lnj1.out"), "w").write("\n".join(OUT) + f"\n(elapsed {time.time() - T0:.0f} s)\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
for t in TWO:
    json.dump(TWO[t], open(os.path.join(HERE, f"lnj1_MUTATE_{t}.json"), "w"), indent=1, default=float)
    lines = []
    for ft in FOOTS:
        for k, v in TWO[t]["foot"][ft].items():
            m = v["main"]; f = m["break"]["fit"]
            lines.append(f"[{ft}] {t} {k}: N above {m['N_above']}, f_above_band above {m['frac_above_band']['above']['f']:.3f}, break "
                         + (f"{f['sb']:.3f} [{f['sb_lo']:.3f}, {f['sb_hi']:.3f}] df {f['df']:.3f} real {m['break']['real']}" if f else "none")
                         + f", raw {m['raw_word']} -> {'bites' if t != 'TWSH' else 'destroys'} {v['bites_or_destroys']}")
    open(os.path.join(HERE, f"lnj1_MUTATE_{t}.out"), "w").write("\n".join(lines) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
P(f"(elapsed {time.time() - T0:.0f} s)")
