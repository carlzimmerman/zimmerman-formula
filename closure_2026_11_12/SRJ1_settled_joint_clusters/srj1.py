#!/usr/bin/env python3
"""SRJ1 (FROZEN_CRITERIA.md, f21be18fd6): the settled-radius joint (FZS1's rule) on groups and clusters, graded with RB1's
frozen gates. TEST lane; relabels nothing, adopts nothing.
  Joint: C_S = s C_B inside R_set = f R_fold (FLD1, system's z, M_b,fold = M200/(1+R)), C_R (RB1's ZN4-native reference) outside,
  s = C_R(R_set)/C_B(R_set); C_B = FRZ1's cluster-regime form-B rule transposed (reference shape, observed baryons as the source).
  Gates: (a) X-COP q at r_last, (b) X-COP shape (RB1 gate 3), (c) Lovisari groups q at R500. Bullet not graded (criteria 2d).
  Checks K1-K5; twins TW-N (no phantom inside R_set) and TW-0 (f = 0).
    python3 srj1.py               -> srj1.out / srj1.json      (exit 0; 2 if a check fails)
    python3 srj1.py --twin newton -> srj1_MUTATE_newton.out / .json (exit 1 by design)
    python3 srj1.py --twin f0     -> srj1_MUTATE_f0.out / .json     (exit 1 by design)
RB1's loaders and statistics are COPIED from closure_2026_11_09/RB1_form_b_hot_systems/rb1.py; FZS1's rfold_kpc is copied;
FZS1's fzs1_hm.py is executed read-only up to its run marker for check K2 only.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import brentq
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); RB = os.path.join(REPO, "rebuild_2026_10_22")
RB1D = os.path.join(REPO, "closure_2026_11_09", "RB1_form_b_hot_systems")
FZS = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach")
CRIT = "f21be18fd6"; T0 = time.time(); SEED = 1109; NBOOT = 10000
TWIN = sys.argv[sys.argv.index("--twin") + 1] if "--twin" in sys.argv else None
OUTL = []
def P(s=""): print(s, flush=True); OUTL.append(str(s))

# ------------------------------------------------------------------ constants and helpers (RB1's, copied)
G, MS, PC = 6.6743e-11, 1.98892e30, 3.0857e16; KPC = 1e3 * PC; MPC = 1e6 * PC
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
VST = {"canonical": 265.8, "alt": 288.1}; CS_IGM = 15.0
R_COS = 5.41; FCOLD = R_COS / (1 + R_COS)
def fret(Mb, Md, R=R_COS):
    Mb = np.asarray(Mb, float); Md = np.asarray(Md, float); d = Md - Mb
    return np.where(d > 0, R * Mb / np.where(d > 0, d, 1.0), np.inf)
def li(r, m, t):
    r = np.asarray(r, float); m = np.asarray(m, float); t = float(t)
    if t < r[0] or t > r[-1]: return float("nan")
    return float(10 ** np.interp(math.log10(t), np.log10(r), np.log10(m)))
def kvm18(M500): return 1.7e12 * (np.asarray(M500, float) / 1e14) ** 0.60
def Mph_rb1(r, Mb, a0):
    if r <= 0: return 0.0
    y = G * Mb / r ** 2 / a0; return Mb * (math.sqrt(0.25 + 1.0 / y) - 0.5)
RHOC0_PER_H2 = 277.536627
def rho_crit(z, h, Om, Or=0.0): E2 = Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + (1.0 - Om - Or); return RHOC0_PER_H2 * h * h * E2

# ------------------------------------------------------------------ loaders (RB1's, copied)
def load_lovisari():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")) if not l.startswith("#")]
    hdr, rows = rows[0], rows[1:]; out = []
    for r in rows:
        d = dict(zip(hdr, r))
        out.append(dict(name=d["name"], z=float(d["z"]), R5=float(d["R500_kpc"]), M5=float(d["M500_1e13"]) * 1e13, g5=float(d["Mgas500_1e12"]) * 1e12))
    return out
LOV = load_lovisari()
R5J = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
XD = os.path.join(DATA, "xcop"); XN = sorted(d for d in os.listdir(XD) if os.path.isdir(os.path.join(XD, d)))
PROF = {}
for name in XN:
    p_ = os.path.join(XD, name)
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500h = float(h[1].header["R500"])
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy()
    st = None
    if os.path.exists(os.path.join(p_, f"{name}_mstar.fits")):
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float); okh = np.isfinite(hM) & (hM > 0)
    gr = np.array(gas["RADIUS"], float) * r500h; gM = np.array(gas["MGAS"], float); okg = np.isfinite(gM) & (gM > 0) & (gr > 0)
    d = dict(hr=hr[okh], hM=hM[okh], gr=gr[okg], gM=gM[okg], r500_fits=r500h, R500=R5J[name]["R500"] * 1e3, z=R5J[name]["z"], stars=st is not None, gas_raw=gas)
    if st is not None:
        sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float); oks = np.isfinite(sM) & (sM > 0) & (sr > 0); d["sr"], d["sM"] = sr[oks], sM[oks]
    PROF[name] = d
WITH = [n for n in XN if PROF[n]["stars"]]
xg = np.geomspace(0.02, 2.0, 60); FR = []
for n in WITH:
    d = PROF[n]; FR.append([(li(d["sr"], d["sM"], x * d["R500"]) / li(d["gr"], d["gM"], x * d["R500"])) if np.isfinite(li(d["gr"], d["gM"], x * d["R500"])) else np.nan for x in xg])
fstar_med = np.nanmedian(np.array(FR), axis=0); okf = np.isfinite(fstar_med)
def fstar(x): return float(np.interp(math.log(x), np.log(xg[okf]), fstar_med[okf]))
HYD = []
for name in XN:
    d = PROF[name]
    for r in d["gr"]:
        mh, mg = li(d["hr"], d["hM"], r), li(d["gr"], d["gM"], r)
        if d["stars"]: ms = li(d["sr"], d["sM"], r); imput = False
        else: ms = fstar(r / d["R500"]) * mg if np.isfinite(mg) else np.nan; imput = True
        if not (np.isfinite(mh) and np.isfinite(mg) and np.isfinite(ms)): continue
        HYD.append(dict(name=name, r_kpc=float(r), x=float(r / d["R500"]), M_dyn=mh, M_gas=mg, M_star=ms, M_bar=mg + ms, measured=not imput))
def xcop_last(names, at="last"):
    out = []
    for n in names:
        pts = [p for p in HYD if p["name"] == n]
        if at == "last": p = max(pts, key=lambda q: q["r_kpc"])
        else:
            d = PROF[n]; r = d["R500"]; mh, mg = li(d["hr"], d["hM"], r), li(d["gr"], d["gM"], r); ms = li(d["sr"], d["sM"], r) if d["stars"] else fstar(1.0) * mg
            p = dict(name=n, r_kpc=r, x=1.0, M_dyn=mh, M_gas=mg, M_star=ms, M_bar=mg + ms, measured=d["stars"], fallback=False)
            if not np.all(np.isfinite([mh, mg, ms])):
                p = dict(max([q for q in pts if q["x"] <= 1.0], key=lambda q: q["r_kpc"])); p["fallback"] = True
        out.append(p)
    return out
def M_nfw_at(n, r):
    d = PROF[n]; gr_all = np.array(d["gas_raw"]["RADIUS"], float) * d["r500_fits"]; mn = np.array(d["gas_raw"]["M_NFW"], float); okn = np.isfinite(mn) & (mn > 0) & (gr_all > 0)
    return li(gr_all[okn], mn[okn], r)

# ------------------------------------------------------------------ statistics (RB1's, copied)
def fin(v): v = np.asarray(v, float); return np.where(np.isfinite(v), v, 1e9)
def class_stat(vals, seed=SEED):
    v = fin(vals); n = len(v)
    if n < 5: return dict(n=n, median=float(np.median(v)) if n else float("nan"), lo=float("nan"), hi=float("nan"), label="NOT EVALUABLE")
    rng = np.random.default_rng(seed); idx = rng.integers(0, n, size=(NBOOT, n)); meds = np.median(v[idx], axis=1)
    lo, hi = float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))
    return dict(n=n, median=float(np.median(v)), lo=lo, hi=hi, n_above1=int(np.sum(v > 1)), label="FAILS" if lo > 1 else "CONSISTENT")
def ols_boot(x, y, seed=SEED):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x); b = np.polyfit(x, y, 1)[0]
    rng = np.random.default_rng(seed); bs = []
    for _ in range(NBOOT):
        i = rng.integers(0, n, n)
        if np.ptp(x[i]) > 0: bs.append(np.polyfit(x[i], y[i], 1)[0])
    return dict(slope=float(b), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), n=n)
EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]
def cl_bin_median(points, val, edges=EDGES):
    names = sorted({p["name"] for p in points}); M = np.full((len(names), len(edges) - 1), np.nan)
    for i, nm in enumerate(names):
        for b in range(len(edges) - 1):
            v = [val(p) for p in points if p["name"] == nm and edges[b] <= p["x"] < edges[b + 1]]
            if v: M[i, b] = float(np.median(v))
    return np.nanmedian(M, axis=0), np.sum(np.isfinite(M), axis=0)

# ------------------------------------------------------------------ ZN4 native shape and the anchor (RB1's, copied)
ZN = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_shapes.json")))
SH = {k: ZN[k]["0.00"] for k in ("1e14", "1e15")}
for k in SH: SH[k]["x_"] = np.array(SH[k]["x"], float); SH[k]["l_"] = np.array(SH[k]["lnm"], float)
def m_native(x, lgM, stretch=1.0):
    x = np.asarray(x, float) / stretch; a, b = SH["1e14"], SH["1e15"]; w = float(np.clip((lgM - a["lgM"]) / (b["lgM"] - a["lgM"]), 0.0, 1.0)); out = []
    for s in (a, b):
        xe = s["x_edge"]; xx = np.minimum(x, xe); lx = np.log(np.maximum(xx, 1e-12)); l0 = np.log(s["x_"][0])
        v = np.where(xx >= s["x_"][0], np.interp(lx, np.log(s["x_"]), s["l_"]), s["l_"][0] + 2.0 * (lx - l0)); out.append(v)
    return np.exp((1 - w) * out[0] + w * out[1])
def solve_R200(Mb_anchor, r_anchor, z, R=R_COS):
    fc = R / (1 + R); rc = rho_crit(z, 0.7, 0.3)
    def cold_in(R2):
        M200 = 200 * rc * 4 * math.pi / 3 * R2 ** 3; return fc * M200 * float(m_native(r_anchor / R2, math.log10(M200)))
    R2 = math.exp(brentq(lambda lr: math.log(cold_in(math.exp(lr))) - math.log(R * Mb_anchor), math.log(50.0), math.log(2e4), xtol=1e-12))
    M200 = 200 * rc * 4 * math.pi / 3 * R2 ** 3; return R2, M200, cold_in(R2) / (R * Mb_anchor) - 1

# ------------------------------------------------------------------ FLD1 R_fold and R_ta (FZS1's rfold_kpc, copied; column 3 for R_ta)
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
FT = {f: {M: np.array(json.load(open(os.path.join(FLD, "runs", f"hubble_{f}_M{M:g}_zi10_N2400.json")))["series"]) for M in MASSES} for f in FOOTS}
def at_z(S, z, col=2):
    o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, col]))
def fld_kpc(foot, z, lM, col=2):
    R = np.array([at_z(FT[foot][M], z, col) for M in MASSES])
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))

# ------------------------------------------------------------------ the law's layout: FRZ1's cluster rule, generic core
def cb_core(r, share, fc, W, m_in, outside, Mb_src, phi, rta):
    """C_B(r) = fc share m_in(r) + min(W phi(Mb_src(r), r), E) + rem min(r, r_ta)/r_ta + outside(r) (FRZ1 layout mode B, cluster)."""
    r = np.asarray(r, float); E = (1 - fc) * share
    ph = np.minimum(W * phi(Mb_src(r), r), E); ph_ta = float(np.minimum(W * phi(Mb_src(np.array([rta])), np.array([rta])), E)[0])
    rem = max(E - ph_ta, 0.0)
    return fc * share * m_in(r) + ph + rem * np.minimum(r, rta) / rta + outside(r)
def phi_si(a0):
    """the law's phantom in Msun for M in Msun, r in kpc."""
    def f(M, r):
        M = np.asarray(M, float); rr = np.asarray(r, float) * KPC
        return np.sqrt(0.25 * M * M + M * rr * rr * a0 / (G * MS)) - 0.5 * M
    return f
PHI0 = lambda M, r: np.zeros_like(np.asarray(r, float))

# ------------------------------------------------------------------ systems
def baryon_profile_xcop(n, part="bar"):
    pts = sorted([p for p in HYD if p["name"] == n], key=lambda q: q["r_kpc"])
    rr = np.array([p["r_kpc"] for p in pts]); mm = np.array([p["M_bar"] if part == "bar" else p["M_gas"] for p in pts])
    def Mb(r):
        r = np.asarray(r, float); out = np.empty_like(r)
        lo = r < rr[0]; hi = r > rr[-1]; mid = ~(lo | hi)
        out[lo] = mm[0] * (r[lo] / rr[0]) ** 3
        out[mid] = 10 ** np.interp(np.log10(np.maximum(r[mid], 1e-30)), np.log10(rr), np.log10(mm))
        out[hi] = mm[-1] * r[hi] / rr[-1]
        return out
    return Mb
def baryon_profile_group(g, R200, part="bar"):
    ms5 = float(kvm18(g["M5"])); mg5 = g["g5"]; R5 = g["R5"]
    a = 0.015 * R200 / (1 + math.sqrt(2)); rc = 0.1 * R200
    hs = lambda x: x ** 2 / (x + a) ** 2; gb = lambda x: x / rc - np.arctan(x / rc)
    def Mb(r):
        r = np.asarray(r, float); g_ = mg5 * gb(r) / gb(R5)
        return g_ if part == "gas" else g_ + ms5 * hs(r) / hs(R5)
    return Mb
def make_system(kind, key, a_r, a_Mb, z, foot, f, part="bar", twin=None, fold_mb=None):
    """returns dict with C_R, C_B, C_S callables (r in kpc, Msun) and the joint's parameters."""
    R2, M200, aerr = solve_R200(a_Mb, a_r, z); lg = math.log10(M200)
    CRf = lambda r: FCOLD * M200 * m_native(np.asarray(r, float) / R2, lg)
    share = float(CRf(np.array([R2]))[0]); m1 = float(m_native(np.array([1.0]), lg)[0])
    m_in = lambda r: m_native(np.minimum(np.asarray(r, float), R2) / R2, lg) / m1
    outside = lambda r: np.where(np.asarray(r, float) > R2, CRf(r) - share, 0.0)
    v = math.sqrt(G * M200 * MS / (R2 * KPC)) / 1e3
    fc = min(max(0.5 * (1 - (VST[foot] / v) ** 2), 0.0), 1.0); W = 1.5 * v * v / (1.5 * v * v + CS_IGM ** 2)
    Mbfun = baryon_profile_xcop(key, part) if kind == "xcop" else baryon_profile_group(key, R2, part)
    Mb_src = lambda r: Mbfun(np.minimum(np.asarray(r, float), R2))
    phi = PHI0 if twin == "newton" else phi_si(A0[foot])
    Mbf = M200 / (1 + R_COS) if fold_mb is None else fold_mb
    Rfold = fld_kpc(foot, z, math.log10(Mbf)); rta = fld_kpc(foot, z, math.log10(Mbf), col=3)
    Rset = min(f * Rfold, rta)
    CBf = lambda r: cb_core(r, share, fc, W, m_in, outside, Mb_src, phi, rta)
    if Rset > 0:
        s = float(CRf(np.array([Rset]))[0] / CBf(np.array([Rset]))[0])
        CSf = lambda r: np.where(np.asarray(r, float) <= Rset, s * CBf(r), CRf(r))
    else:
        s = float("nan"); CSf = CRf
    return dict(R200=R2, M200=M200, anchor_err=aerr, v=v, fc=fc, W=W, Rfold=Rfold, rta=rta, Rset=Rset, s=s, Mb_fold=Mbf,
                CR=CRf, CB=CBf, CS=CSf, z=z)
def junction_ok(S):
    if S["Rset"] <= 0: return 0.0, True
    e = abs(float(S["CS"](np.array([S["Rset"]]))[0] / S["CR"](np.array([S["Rset"]]))[0]) - 1)
    rr = np.geomspace(1.0, 1.5 * S["rta"], 3000); c = S["CS"](rr); mono = bool(np.all(np.diff(c) >= -1e-9 * c.max()))
    return e, mono

# ------------------------------------------------------------------ gates
JUNC = []
def gate_a(foot, f, at="last", mass="FORW", part="bar", twin=None, fold="M200"):
    pts = xcop_last(WITH, at); q = []; per = {}
    for p in pts:
        n = p["name"]; S = make_system("xcop", n, p["r_kpc"], p["M_bar"], PROF[n]["z"], foot, f, part, twin, None if fold == "M200" else p["M_bar"])
        JUNC.append(junction_ok(S))
        r = p["r_kpc"]; Md = p["M_dyn"] if mass == "FORW" else M_nfw_at(n, r)
        cs = float(S["CS"](np.array([r]))[0]); cr = float(S["CR"](np.array([r]))[0])
        qq = cs / (Md - p["M_bar"]) if Md > p["M_bar"] else float("inf"); q.append(qq)
        per[n] = dict(x=p["x"], r_kpc=r, z=S["z"], q=qq, q_ref=cr / (Md - p["M_bar"]) if Md > p["M_bar"] else float("inf"), joint_factor=cs / cr,
                      MS_over_MHSE=(p["M_bar"] + cs) / Md, R200_over_R500=S["R200"] / PROF[n]["R500"], lgMb_fold=math.log10(S["Mb_fold"]),
                      Rfold_kpc=S["Rfold"], rta_kpc=S["rta"], Rset_kpc=S["Rset"], Rset_over_R200=S["Rset"] / S["R200"], Rset_over_R500=S["Rset"] / PROF[n]["R500"],
                      s=S["s"], fc=S["fc"], v200=S["v"])
    cs_ = class_stat(q if mass == "FORW" else [v for v in q if np.isfinite(v)]); cs_["per_cluster"] = per   # RB1: M_NFW rows keep finite values only
    return cs_
def gate_b(foot, f, part="bar", twin=None, fold="M200"):
    pts = []; per = {}
    for n in WITH:
        P_ = [dict(p) for p in HYD if p["name"] == n]; pa = max(P_, key=lambda q: q["r_kpc"])
        S = make_system("xcop", n, pa["r_kpc"], pa["M_bar"], PROF[n]["z"], foot, f, part, twin, None if fold == "M200" else pa["M_bar"]); JUNC.append(junction_ok(S))
        rr = np.array([p["r_kpc"] for p in P_]); cs = S["CS"](rr)
        for p, c in zip(P_, cs): p["M_model"] = p["M_bar"] + float(c); p["D"] = math.log10(p["M_dyn"] / p["M_model"]); pts.append(p)
        per[n] = dict(Rset_over_R500=S["Rset"] / PROF[n]["R500"], s=S["s"])
    med, cnt = cl_bin_median(pts, lambda p: p["D"]); graded = cnt >= 5
    lab = ("CONSISTENT" if np.all(np.abs(med[graded]) <= 0.10) else "FAILS") if graded.any() else "NOT EVALUABLE"
    return dict(bins=med.tolist(), n_clusters=cnt.tolist(), graded=graded.tolist(), label=lab, per_cluster=per)
def gate_c(foot, f, part="bar", twin=None, fold="M200"):
    q = []; per = {}
    for g in LOV:
        Mb = g["g5"] + float(kvm18(g["M5"])); S = make_system("group", g, g["R5"], Mb, g["z"], foot, f, part, twin, None if fold == "M200" else Mb); JUNC.append(junction_ok(S))
        # check that the group baryon profile reproduces the anchor baryons at R500
        cs = float(S["CS"](np.array([g["R5"]]))[0]); cr = float(S["CR"](np.array([g["R5"]]))[0]); d = g["M5"] - Mb
        qq = cs / d if d > 0 else float("inf"); q.append(qq)
        per[g["name"]] = dict(q=qq, q_ref=cr / d if d > 0 else float("inf"), joint_factor=cs / cr, Rset_over_R500=S["Rset"] / g["R5"], Rset_over_R200=S["Rset"] / S["R200"],
                              s=S["s"], fc=S["fc"], v200=S["v"], lgMb_fold=math.log10(S["Mb_fold"]), MS_over_M500=(Mb + cs) / g["M5"])
    c = class_stat(q); c["per_group"] = per; c["n_v_below_vstiff"] = int(sum(1 for v in per.values() if v["fc"] == 0.0)); return c

def run_all(foot, f, part="bar", twin=None, fold="M200"):
    return dict(a_last=gate_a(foot, f, "last", "FORW", part, twin, fold), a_R500=gate_a(foot, f, "R500", "FORW", part, twin, fold),
                a_last_NFW=gate_a(foot, f, "last", "NFW", part, twin, fold), a_R500_NFW=gate_a(foot, f, "R500", "NFW", part, twin, fold),
                b=gate_b(foot, f, part, twin, fold), c=gate_c(foot, f, part, twin, fold))
def labels(r): return dict(a=r["a_last"]["label"], b=r["b"]["label"], c=r["c"]["label"])

# ================================================================== CHECKS
P(f"SRJ1 (criteria {CRIT}): the settled-radius joint on groups and clusters, RB1's gates. TEST lane; adopts nothing.")
P("kappa = 1/2 FITTED; not theory closed. Cold dark energy, never a particle. Footings never pooled." + (f"  [TWIN {TWIN}: deliberately wrong]" if TWIN else ""))
CHK = {}
# K5 parsers
CHK["K5"] = dict(groups=len(LOV), xcop=len(XN), xcop_stars=len(WITH), pass_=bool(len(LOV) == 20 and len(XN) == 12 and len(WITH) == 7))
P(f"K5 parsers: groups {len(LOV)} (20), X-COP {len(XN)} (12), with stars {len(WITH)} (7) -> {'PASS' if CHK['K5']['pass_'] else 'FAIL'}")
# K3 FLD1 radii (FZS1's KA-F)
KAF = {9.4: (62.2, 21.3, 7.59), 10.45: (139.3, 47.8, 17.24), 10.7: (168.8, 57.9, 20.96), 10.9: (196.9, 67.6, 24.51)}
dev = max(abs(fld_kpc("canonical", z, M) - v) for M, vs in KAF.items() for z, v in zip((0, 2, 4), vs)); CHK["K3"] = dict(max_dev_kpc=dev, pass_=bool(dev <= 0.06))
P(f"K3 FLD1 R_fold (FZS1 KA-F values): max deviation {dev:.4f} kpc (line 0.06) -> {'PASS' if CHK['K3']['pass_'] else 'FAIL'}")
# phantom cross-check against RB1's Mph
ph_dev = max(abs(float(phi_si(A0[f])(np.array([m]), np.array([r]))[0]) / (Mph_rb1(r * KPC, m * MS, A0[f]) / MS) - 1) for f in FOOTS for m in (1e12, 1e14) for r in (50.0, 1500.0))
P(f"    phantom in Msun against RB1's Mph: max relative deviation {ph_dev:.1e}")
# K1 joint off reproduces RB1
RB1J = json.load(open(os.path.join(RB1D, "rb1.json"))); K1 = {}
for foot in FOOTS:
    r0 = run_all(foot, 0.0); g1 = RB1J["gate1"][foot]; devs = []
    def cmp(mine, ref, keys=("median", "lo", "hi")): devs.extend(abs(mine[k] - ref[k]) for k in keys)
    cmp(r0["a_last"], g1["classes"]["C-X"]); devs.extend(abs(r0["a_last"]["per_cluster"][n]["q"] - v["f_ret"]) for n, v in g1["classes"]["C-X"]["per_cluster"].items())
    cmp(r0["a_R500"], g1["brackets"]["C-X at R500"]); devs.extend(abs(r0["a_R500"]["per_cluster"][n]["q"] - v["f_ret"]) for n, v in g1["brackets"]["C-X at R500"]["per_cluster"].items())
    cmp(r0["a_last_NFW"], g1["brackets"]["C-X M_NFW at last (A1, post hoc)"]); cmp(r0["a_R500_NFW"], g1["brackets"]["C-X M_NFW at R500 (A1, post hoc)"])
    cmp(r0["c"], g1["classes"]["G-H"])
    devs.extend(abs(a - b) for a, b in zip(r0["b"]["bins"], RB1J["gate3"][foot]["main"]["bins"]))
    K1[foot] = dict(max_dev=float(max(devs)), pass_=bool(max(devs) <= 1e-6), ref=r0)
    P(f"K1 [{foot}] joint off (f = 0) against rb1.json (C-X last / R500 / M_NFW x2, per cluster, G-H, gate-3 bins): max |dev| {max(devs):.2e} (line 1e-6) -> {'PASS' if K1[foot]['pass_'] else 'FAIL'}")
CHK["K1"] = {f: dict(max_dev=K1[f]["max_dev"], pass_=K1[f]["pass_"]) for f in FOOTS}
# K2 FZS1's diagnostic (fzs1_hm.py executed read-only up to its run marker)
t2 = time.time(); SRC = os.path.join(FZS, "fzs1_hm.py"); code = open(SRC).read(); cut = code.rindex("\n# ------------------------------------------------------------------ checkpointed run\n")
GZ = {"__file__": SRC, "__name__": "fzs1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), GZ)
F = GZ["F"]; Lz = GZ["L"]; GZ["set_z"](2.2); ftz = "canonical"
hb = min(Lz["HB"], key=lambda b: abs(math.log(b["M"] / 1e13)))
r_, MS_, inf = GZ["lay_S"](ftz, 2.2)(hb)
rB, MB, _ = GZ["layout"](hb, ftz, mode="B"); rR, MR, _ = GZ["layout"](hb, ftz, mode="Rb")
R2z, M2z = hb["r200c"], hb["M200c"]; FBz = F["FB"]; m_nfw_z = F["m_nfw"]
share_z = (1 - FBz) * M2z; vz = F["v_vir"](hb); fcz = min(max(0.5 * (1 - (F["VST"][ftz] / vz) ** 2), 0.0), 1.0); Wz = 1.5 * vz * vz / (1.5 * vz * vz + F["CS_IGM"] ** 2)
m_in_z = lambda r: m_nfw_z(np.minimum(np.asarray(r, float), R2z) / hb["rs"]) / m_nfw_z(R2z / hb["rs"])
out_z = lambda r: np.where(np.asarray(r, float) > R2z, F["M_L"](hb, r) - M2z, 0.0)
Mbs_z = lambda r: F["bar_cum"](hb, FBz * M2z, np.asarray(r, float), R2z, 0.1)
a0z = F["a0c"](ftz); phi_z = lambda M, r: F["phantom"](M, r, a0z)
CB_frz = MB - GZ["Bar"](hb, ftz, rB); CB_mine = cb_core(rB, share_z, fcz, Wz, m_in_z, out_z, Mbs_z, phi_z, hb["rta"])
nz = np.abs(CB_frz) > 0; rel = float(np.max(np.abs(CB_mine[nz] / CB_frz[nz] - 1)))
Rz = inf["R_set"]; CB_on = cb_core(r_, share_z, fcz, Wz, m_in_z, out_z, Mbs_z, phi_z, hb["rta"]); CR_on = share_z * m_in_z(r_) + out_z(r_)
fr = lambda C, x: np.interp(x * Rz, r_, C) / np.interp(Rz, r_, C)
s_mine = float(np.interp(Rz, r_, CR_on) / np.interp(Rz, r_, CB_on))
fl = (fr(CB_on, 0.25), fr(CB_on, 0.5)); frf = (fr(CR_on, 0.25), fr(CR_on, 0.5))
ok2 = bool(rel <= 1e-9 and abs(fl[0] - 0.128) <= 0.0006 and abs(fl[1] - 0.373) <= 0.0006 and abs(frf[0] - 0.175) <= 0.0006 and abs(frf[1] - 0.458) <= 0.0006
           and abs(Rz - 0.4106) <= 0.00006 and abs(s_mine - 1.058) <= 0.0006)
CHK["K2"] = dict(M=hb["M"], rel_dev_CB=rel, law=list(fl), ref=list(frf), R_set=Rz, s=s_mine, pass_=ok2, seconds=time.time() - t2)
P(f"K2 FZS1 diag (z 2.2 canonical, M {hb['M']:.1e}): my C_B vs FRZ1 layout(B) max rel dev {rel:.1e} (1e-9); law fractions {fl[0]:.4f}/{fl[1]:.4f} (0.128/0.373), "
  f"ref {frf[0]:.4f}/{frf[1]:.4f} (0.175/0.458); R_set {Rz:.4f} (0.4106), s {s_mine:.4f} (1.058) -> {'PASS' if ok2 else 'FAIL'}  [{time.time() - t2:.0f} s]")
del GZ, F, Lz

# ================================================================== GRADED (or twin) RUNS
RES = dict(criteria=CRIT, twin=TWIN, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed", checks=CHK)
FPTS = (1.0, 0.75, 1.25)
def show(tag, r):
    a, a5, an, a5n, b, c = r["a_last"], r["a_R500"], r["a_last_NFW"], r["a_R500_NFW"], r["b"], r["c"]
    P(f"  {tag}: (a) C-X q at r_last {a['median']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}] {a['n_above1']}/7 above 1 -> {a['label']}; at R500 {a5['median']:.3f} [{a5['lo']:.3f}, {a5['hi']:.3f}] {a5['label']}; "
      f"M_NFW last {an['median']:.3f} [{an['lo']:.3f}, {an['hi']:.3f}] {an['label']}, R500 {a5n['median']:.3f} [{a5n['lo']:.3f}, {a5n['hi']:.3f}] {a5n['label']}")
    P(f"      (b) shape bins " + " / ".join(f"{v:+.3f}{'' if g else '*'}" for v, g in zip(b["bins"], b["graded"])) + f" -> {b['label']};  (c) G-H q at R500 {c['median']:.3f} [{c['lo']:.3f}, {c['hi']:.3f}] {c['n_above1']}/20 above 1 -> {c['label']}")
OUTR = {}
for foot in FOOTS:
    P(); P(f"==== [{foot}] a0 {A0[foot]:.4e}" + (f"  TWIN {TWIN}" if TWIN else ""))
    o = {}
    if TWIN == "newton":
        o["f1.00"] = run_all(foot, 1.0); o["twin"] = run_all(foot, 1.0, twin="newton")
    elif TWIN == "f0":
        o["f1.00"] = run_all(foot, 1.0); o["twin"] = run_all(foot, 0.0)
    else:
        for fp in FPTS: o[f"f{fp:.2f}"] = run_all(foot, fp)
        o["gas_only"] = run_all(foot, 1.0, part="gas"); o["fold_Mb_obs"] = run_all(foot, 1.0, fold="obs"); o["ref_f0"] = K1[foot]["ref"]
        o["newton_internal"] = run_all(foot, 1.0, twin="newton")
    for k, r in o.items():
        if k == "newton_internal": continue
        show(k, r)
    if TWIN is None:
        g = o["f1.00"]
        P("  per cluster at r_last (f 1): name x_last z lgMb_fold R_fold R_set/R200 R_set/R500 s fc q_ref -> q (joint factor C_S/C_R) M_S/M_HSE")
        for n, v in g["a_last"]["per_cluster"].items():
            P(f"    {n:8s} {v['x']:.2f} {v['z']:.3f} {v['lgMb_fold']:.2f} {v['Rfold_kpc']:.0f} {v['Rset_over_R200']:.2f} {v['Rset_over_R500']:.2f} {v['s']:.3f} {v['fc']:.3f} {v['q_ref']:.3f} -> {v['q']:.3f} ({v['joint_factor']:.3f}) {v['MS_over_MHSE']:.3f}")
        P("  per cluster at R500 (f 1): " + "; ".join(f"{n} q_ref {v['q_ref']:.3f} -> {v['q']:.3f} ({v['joint_factor']:.3f})" for n, v in g["a_R500"]["per_cluster"].items()))
        P("  per cluster at r_last, f 0.75 / 1.25 q: " + "; ".join(f"{n} {o['f0.75']['a_last']['per_cluster'][n]['q']:.3f}/{o['f1.25']['a_last']['per_cluster'][n]['q']:.3f}" for n in g["a_last"]["per_cluster"]))
        jf = [v["joint_factor"] for v in g["c"]["per_group"].values()]; rs = [v["Rset_over_R500"] for v in g["c"]["per_group"].values()]
        P(f"  groups (f 1): joint factor C_S/C_R at R500 median {np.median(jf):.3f} (range {min(jf):.3f}-{max(jf):.3f}); R_set/R500 median {np.median(rs):.2f} (range {min(rs):.2f}-{max(rs):.2f}); "
          f"systems with v200 <= v_stiff: {g['c']['n_v_below_vstiff']}")
        # reported: gate-2 ladder with q at R500
        x = [math.log10(gg["M5"]) for gg in LOV] + [math.log10(p["M_dyn"]) for p in xcop_last(WITH, "R500")]
        for k in ("ref_f0", "f1.00"):
            y = [g_["q"] for g_ in o[k]["c"]["per_group"].values()] + [v["q"] for v in o[k]["a_R500"]["per_cluster"].values()]
            sl = ols_boot(x, np.log10(np.maximum(fin(y), 1e-6))); o[k]["ladder_slope"] = sl
            P(f"  reported gate-2 ladder slope with q at R500 [{k}]: {sl['slope']:+.3f} [{sl['lo']:+.3f}, {sl['hi']:+.3f}]")
    OUTR[foot] = o

# ================================================================== twins and words
def rms_move(b1, b2):
    g = np.array(b1["graded"]); return float(np.sqrt(np.mean((np.array(b1["bins"])[g] - np.array(b2["bins"])[g]) ** 2)))
jm = max(e for e, _ in JUNC); mono = all(m for _, m in JUNC); CHK["K4"] = dict(max_junction_dev=jm, monotone=mono, pass_=bool(jm <= 1e-12 and mono))
P(); P(f"K4 junction in every system evaluated: max |C_S/C_R - 1| at R_set {jm:.1e} (1e-12), C_S non-decreasing: {mono} -> {'PASS' if CHK['K4']['pass_'] else 'FAIL'}")
if TWIN:
    bite = {}
    for foot in FOOTS:
        o = OUTR[foot]
        if TWIN == "newton":
            mv = rms_move(o["f1.00"]["b"], o["twin"]["b"]); bite[foot] = dict(rms_move_dex=mv, bites=bool(mv >= 0.05))
        else:
            mine, ref = o["twin"], K1[foot]["ref"]
            d = max(abs(mine["a_last"]["median"] - ref["a_last"]["median"]), abs(mine["c"]["median"] - ref["c"]["median"]), max(abs(a - b) for a, b in zip(mine["b"]["bins"], ref["b"]["bins"])))
            bite[foot] = dict(max_dev_from_reference=d, bites=bool(d <= 1e-6), labels=labels(mine))
        P(f"TWIN {TWIN} [{foot}]: {bite[foot]} -> {'bites' if bite[foot]['bites'] else 'DOES NOT BITE'}")
    RES.update(results=OUTR, bite=bite)
    stem = f"srj1_MUTATE_{TWIN}"; code_exit = 1
else:
    WORD = {}
    for foot in FOOTS:
        o = OUTR[foot]; chk_ok = all(CHK[k]["pass_"] for k in ("K2", "K3", "K4", "K5")) and CHK["K1"][foot]["pass_"]
        tw_n = rms_move(o["f1.00"]["b"], o["newton_internal"]["b"]); tw_ok = tw_n >= 0.05
        lab = labels(o["f1.00"])
        if not (chk_ok and tw_ok): w = "NO VERDICT"
        elif "FAILS" in lab.values(): w = "JOINT FAILS ON CLUSTERS"
        elif all(v == "CONSISTENT" for v in lab.values()): w = "JOINT HOLDS ON CLUSTERS (ONE-SIDED)"
        else: w = "NO VERDICT"
        cross = []
        for bk in ("f0.75", "f1.25", "gas_only"):
            lb = labels(o[bk])
            for gk in ("a", "b", "c"):
                if lb[gk] != lab[gk]: cross.append(f"{bk} on ({gk}): {lb[gk]}; reference {labels(o['ref_f0'])[gk]}")
        if o["f1.00"]["a_last_NFW"]["label"] != lab["a"]: cross.append(f"M_NFW on (a): {o['f1.00']['a_last_NFW']['label']}; reference {o['ref_f0']['a_last_NFW']['label']}")
        if o["f1.00"]["a_R500"]["label"] != lab["a"]: cross.append(f"R500 aperture on (a): {o['f1.00']['a_R500']['label']}; reference {o['ref_f0']['a_R500']['label']}")
        word = w + (", FRAGILE (" + " | ".join(cross) + ")" if (cross and w != "NO VERDICT") else "")
        WORD[foot] = dict(word=word, labels=lab, checks_ok=chk_ok, newton_twin_rms_move=tw_n, crossings=cross)
        P(f"WORD [{foot}]: {word}   (gates {lab}; checks {'ok' if chk_ok else 'FAILED'}; TW-N moves shape bins {tw_n:.3f} dex rms)")
    for foot in FOOTS: OUTR[foot].pop("newton_internal", None)
    RES.update(results=OUTR, words=WORD); stem = "srj1"
    code_exit = 0 if all(CHK[k]["pass_"] for k in ("K2", "K3", "K4", "K5")) and all(CHK["K1"][f]["pass_"] for f in FOOTS) else 2
RES["seconds"] = time.time() - T0; RES["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20
P(f"[{RES['seconds']:.0f} s, peak RSS {RES['peak_rss_MB']:.0f} MB]"); P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def clean(x):
    if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.floating, float)): return float(x) if np.isfinite(x) else str(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, np.bool_): return bool(x)
    return x
json.dump(clean(RES), open(os.path.join(HERE, stem + ".json"), "w"), indent=1)
open(os.path.join(HERE, stem + ".out"), "w").write("\n".join(OUTL) + "\n")
sys.exit(code_exit)
