#!/usr/bin/env python3
"""FRM1: the formation reading as a theory, on DD1's frozen table (criteria 462eaa806d + fed1bc94a4).
TEST lane, quarantined; adopts nothing. kappa = 1/2 FITTED; not theory closed. One thread.
Usage: python3 frm1.py            -> frm1.json / frm1.out
       python3 frm1.py --mutate   -> frm1_MUTATE.json / frm1_MUTATE.out

The theory (criteria): X_f = X_L(g_b,f; a0) is set at formation; the non-baryonic mass M_C is a conserved charge
that moves only by transfer (f_C) and the baryons only by their own transfers (f_b), so
    X = X_f f_C/f_b ,   d = log10[(1 + X_L(g_b,f) f_C/f_b)/(1 + X_L(g_bar))] .
Statistic: Y = log10(g_obs/g_bar) = log10(1 + X); a residual is dex in g_obs at fixed g_bar.
Fitting (F4) is free: binned free functions on the training systems only, no theory assumed in the fit.
"""
import os, sys, csv, math, json, time, warnings
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore", message="All-NaN slice encountered")
warnings.filterwarnings("ignore", message="Mean of empty slice")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
DD1 = os.path.abspath(os.path.join(HERE, "..", "DD1_deduce_from_data"))
MUT = "--mutate" in sys.argv; TAG = "frm1_MUTATE" if MUT else "frm1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
G, MS, PC, CL = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
SEED = 20261110; LINE_DEX = 0.10; LINE_SIG = 3.0; BIN1 = 0.2; BIN2 = 0.4; MINPTS = 5
SIZE = 0.30          # the size line for the corrected F2 (the pre-registered band's lower edge for the stripped family)
RES = dict(lane="FRM1", criteria="462eaa806d+fed1bc94a4", table="441824e854", tag=TAG,
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, runs={}, labels={},
           reported={}, MUTATE={})

# ============================================================ DD1's frozen table, DD1's loaders (unchanged)
def load_table():
    rows = []
    with open(os.path.join(DD1, "dd1_table.csv")) as fh:
        lines = [l for l in fh if not l.startswith("#")]
    for r in csv.DictReader(lines):
        if r["bracket"] != "": continue
        rows.append(dict(cls=r["cls"], sys=r["sys"], r_kpc=float(r["r_kpc"]), lgb=float(r["lgb"]), lgo=float(r["lgo"]),
                         eY=float(r["eY"]), z=float(r["z"]), lSig=float(r["lSig"]), last=int(r["last"])))
    return rows
ROWS = load_table()
CLASSES = []
for r in ROWS:
    if r["cls"] not in CLASSES: CLASSES.append(r["cls"])

def build(rows):
    """DD1's build, verbatim in every derived variable."""
    T = {k: np.array([r[k] for r in rows]) for k in ("cls", "sys", "r_kpc", "lgb", "lgo", "eY", "z", "lSig", "last")}
    T["sk"] = np.array([c + "|" + s for c, s in zip(T["cls"], T["sys"])])
    T["Y"] = T["lgo"] - T["lgb"]
    rm = T["r_kpc"] * KPC
    with np.errstate(divide="ignore", invalid="ignore"):
        T["dep"] = T["lgo"] + np.log10(rm) - 2 * math.log10(CL)
    T["Mb"] = T["lgb"] + 2 * np.log10(rm) - math.log10(G * MS)
    T["lr"] = np.log10(T["r_kpc"]); T["zz"] = np.log10(T["z"] + 1e-3)
    ds = {}
    for k, d in zip(T["sk"], T["dep"]):
        if np.isfinite(d): ds[k] = max(ds.get(k, -np.inf), d)
    T["dsys"] = np.array([ds.get(k, np.nan) for k in T["sk"]])
    npts = {}
    for k in T["sk"]: npts[k] = npts.get(k, 0) + 1
    T["w"] = np.array([1.0 / npts[k] for k in T["sk"]])
    T["n"] = len(rows)
    return T

def wmed(v, w):
    v = np.asarray(v, float); w = np.asarray(w, float)
    m = ~np.isnan(v); v, w = v[m], w[m]
    if len(v) == 0: return float("nan")
    o = np.argsort(v, kind="mergesort"); v, w = v[o], w[o]; c = np.cumsum(w)
    return float(v[np.searchsorted(c, 0.5 * c[-1])])
def XL(lgb, a0):
    t = a0 / 10 ** np.asarray(lgb, float); return 2 * t / (np.sqrt(1 + 4 * t) + 1)
def YL(lgb, a0): return np.log10(1 + XL(lgb, a0))

# ============================================================ DD1's free-rule machinery (unchanged)
def fit1(v, T, idx):
    vv, YY, ww = T[v][idx], T["Y"][idx], T["w"][idx]
    ok = np.isfinite(vv); vv, YY, ww = vv[ok], YY[ok], ww[ok]
    b = np.floor(vv / BIN1).astype(int); nodes = []
    for k in np.unique(b):
        m = b == k
        if m.sum() < MINPTS: continue
        ym = wmed(YY[m], ww[m])
        if np.isfinite(ym): nodes.append((wmed(vv[m], ww[m]), ym))
    nodes.sort()
    return np.array(nodes) if nodes else np.zeros((0, 2))
def endline(xs, ys):
    if len(xs) == 1: return 0.0, ys[0]
    p = np.polyfit(xs, ys, 1); return p[0], p[1]
def pred1(nodes, x):
    x = np.asarray(x, float); out = np.full(len(x), np.nan); ext = np.zeros(len(x), bool)
    if len(nodes) == 0: return out, ext
    xs, ys = nodes[:, 0], nodes[:, 1]; ok = np.isfinite(x)
    if len(xs) == 1: out[ok] = ys[0]; ext[ok] = x[ok] != xs[0]; return out, ext
    out[ok] = np.interp(x[ok], xs, ys)
    lo = ok & (x < xs[0]); hi = ok & (x > xs[-1])
    s, c = endline(xs[:3], ys[:3]); out[lo] = s * x[lo] + c
    s, c = endline(xs[-3:], ys[-3:]); out[hi] = s * x[hi] + c
    ext[lo | hi] = True
    return out, ext
def fit2(v1, v2, T, idx):
    a, b, YY, ww = T[v1][idx], T[v2][idx], T["Y"][idx], T["w"][idx]
    ok = np.isfinite(a) & np.isfinite(b); a, b, YY, ww = a[ok], b[ok], YY[ok], ww[ok]
    ca = np.floor(a / BIN2).astype(int); cb = np.floor(b / BIN2).astype(int); nodes = []
    for key in set(zip(ca, cb)):
        m = (ca == key[0]) & (cb == key[1])
        if m.sum() < MINPTS: continue
        ym = wmed(YY[m], ww[m])
        if np.isfinite(ym): nodes.append((wmed(a[m], ww[m]), wmed(b[m], ww[m]), ym))
    return np.array(sorted(nodes)) if nodes else np.zeros((0, 3))
def pred2(nodes, x1, x2):
    n = len(x1); out = np.full(n, np.nan); ext = np.zeros(n, bool)
    if len(nodes) == 0: return out, ext
    pts = nodes[:, :2] / BIN2; q = np.c_[np.asarray(x1, float), np.asarray(x2, float)] / BIN2
    ok = np.all(np.isfinite(q), axis=1)
    near = NearestNDInterpolator(pts, nodes[:, 2]); lin = None
    if len(nodes) >= 3:
        try: lin = LinearNDInterpolator(pts, nodes[:, 2])
        except Exception: lin = None
    if lin is not None:
        v = lin(q[ok]); bad = ~np.isfinite(v); v[bad] = near(q[ok][bad]); out[ok] = v
        e = np.zeros(ok.sum(), bool); e[bad] = True; ext[ok] = e
    else:
        out[ok] = near(q[ok]); ext[ok] = True
    return out, ext
def fit_a0(lgb, Y, w):
    def f(la): return wmed(Y - YL(lgb, 10 ** la), w)
    lo, hi = -16.0, -4.0
    if not (f(lo) > 0 > f(hi)): return 10 ** (lo if f(lo) <= 0 else hi)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
    return 10 ** (0.5 * (lo + hi))

# ============================================================ rules: the law plus one free function of a history variable
def make_rules(a0):
    R = {}
    R["N0"] = dict(kind="law", fit=lambda T, idx: a0, pred=lambda m, T, idx: (YL(T["lgb"][idx], m), np.zeros(len(idx), bool)))
    def mk1(v):
        def fit(T, idx):
            T2 = dict(T); T2["Y"] = T["Y"] - YL(T["lgb"], a0)
            return fit1(v, T2, idx)
        def pred(m, T, idx):
            yh, ext = pred1(m, T[v][idx]); return YL(T["lgb"][idx], a0) + yh, ext
        return dict(kind="lp1", v=v, fit=fit, pred=pred)
    R["N1"] = mk1("dsys"); R["N2"] = mk1("zz")
    def mk2(v1, v2):
        def fit(T, idx):
            T2 = dict(T); T2["Y"] = T["Y"] - YL(T["lgb"], a0)
            return fit2(v1, v2, T2, idx)
        def pred(m, T, idx):
            yh, ext = pred2(m, T[v1][idx], T[v2][idx]); return YL(T["lgb"][idx], a0) + yh, ext
        return dict(kind="lp2", fit=fit, pred=pred)
    R["N3"] = mk2("dsys", "zz")
    R["L1"] = dict(kind="law", fit=lambda T, idx: fit_a0(T["lgb"][idx], T["Y"][idx], T["w"][idx]),
                   pred=lambda m, T, idx: (YL(T["lgb"][idx], m), np.zeros(len(idx), bool)))
    return R
ORDER = ["N0", "N1", "N2", "N3"]
NAMES = {"N0": "N0 law alone (force reading's rule)", "N1": "N1 law + free F(system depth)",
         "N2": "N2 law + free F(redshift)", "N3": "N3 law + free F(depth, redshift)"}

# ============================================================ DD1's split and scoring (unchanged)
def systems(T):
    return {c: sorted(set(T["sk"][T["cls"] == c])) for c in CLASSES}
def split(T, seed):
    rng = np.random.default_rng(seed); A, B = set(), set()
    for c, ss in systems(T).items():
        if not ss: continue
        p = rng.permutation(len(ss)); h = int(math.ceil(len(ss) / 2))
        A |= {ss[i] for i in p[:h]}; B |= {ss[i] for i in p[h:]}
    return A, B
def class_offsets(T, idx, d, eY_scale=1.0):
    out = {}
    cl, sk, eY = T["cls"][idx], T["sk"][idx], T["eY"][idx] * eY_scale
    for c in CLASSES:
        m = cl == c
        if not m.any(): continue
        ds, es = [], []
        for s in sorted(set(sk[m])):
            q = m & (sk == s); dv = d[q]; dv = dv[~np.isnan(dv)]
            if len(dv) == 0: continue
            ds.append(float(np.median(dv))); ef = eY[q][np.isfinite(eY[q])]; es.append(float(np.median(ef)))
        if not ds: continue
        ds, es = np.array(ds), np.array(es); n = len(ds); off = float(np.median(ds))
        if n >= 2:
            fin = ds[np.isfinite(ds)]
            mad = 1.4826 * float(np.median(np.abs(fin - np.median(fin)))) if len(fin) else float("inf")
            se = max(1.2533 * mad / math.sqrt(n), math.sqrt(float(np.sum(es ** 2))) / n)
        else: se = float(es[0])
        out[c] = dict(off=off, se=se, n=n, z=(off / se if se > 0 else float("inf")),
                      pass_=bool(np.isfinite(off) and abs(off) <= LINE_DEX and abs(off) <= LINE_SIG * se))
    return out
def bal_scatter(T, idx, d):
    cl, sk = T["cls"][idx], T["sk"][idx]; ok = ~np.isnan(d)
    if not ok.any(): return float("nan")
    w = np.zeros(len(idx))
    for c in set(cl[ok]):
        mc = ok & (cl == c); ss = set(sk[mc])
        for s in ss:
            q = mc & (sk == s); w[q] = 1.0 / (len(ss) * q.sum())
    m = wmed(d[ok], w[ok]); return 1.4826 * wmed(np.abs(d[ok] - m), w[ok])
def pt_scatter(d):
    d = d[~np.isnan(d)]; return 1.4826 * float(np.median(np.abs(d - np.median(d)))) if len(d) else float("nan")
def ref_pred(T, tr, te):
    out = np.full(len(te), np.nan)
    for c in CLASSES:
        mt = T["cls"][tr] == c; me = T["cls"][te] == c
        if mt.any() and me.any(): out[me] = wmed(T["Y"][tr][mt], T["w"][tr][mt])
    return out
def run_split(R, key, T, trS, teS):
    tr = np.where(np.isin(T["sk"], list(trS)))[0]; te = np.where(np.isin(T["sk"], list(teS)))[0]
    model = R[key]["fit"](T, tr); yh, ext = R[key]["pred"](model, T, te)
    with np.errstate(invalid="ignore"): d = T["Y"][te] - yh
    rd = T["Y"][te] - ref_pred(T, tr, te)
    co = class_offsets(T, te, d)
    sc, rsc = bal_scatter(T, te, d), bal_scatter(T, te, rd)
    return dict(classes=co, scatter=sc, ref_scatter=rsc, point_scatter=pt_scatter(d), scatter_ok=bool(sc <= rsc),
                extrap=float(ext.mean()) if len(ext) else 0.0, all_pass=bool(all(v["pass_"] for v in co.values())))
def run_loco(R, key, T):
    out = {}
    for c in CLASSES:
        te = np.where(T["cls"] == c)[0]; tr = np.where(T["cls"] != c)[0]
        if len(te) == 0: continue
        model = R[key]["fit"](T, tr); yh, ext = R[key]["pred"](model, T, te)
        with np.errstate(invalid="ignore"): d = T["Y"][te] - yh
        co = class_offsets(T, te, d)
        if c in co: out[c] = dict(co[c], extrap=float(ext.mean()))
    return out
def evaluate(R, key, T, seed=SEED):
    A, B = split(T, seed)
    ab = run_split(R, key, T, A, B); ba = run_split(R, key, T, B, A); lo = run_loco(R, key, T)
    fails = {}
    for tname, co in (("A->B", ab["classes"]), ("B->A", ba["classes"]), ("LOCO", lo)):
        for c, v in co.items():
            if not v["pass_"]: fails.setdefault(c, []).append(dict(test=tname, off=v["off"], se=v["se"], z=v["z"]))
    covered = set(ab["classes"]) | set(ba["classes"]); cover_all = all(c in covered for c in CLASSES)
    passes = bool(ab["all_pass"] and ba["all_pass"] and ab["scatter_ok"] and ba["scatter_ok"]
                  and all(v["pass_"] for v in lo.values()))
    worst = None
    for tname, co in (("A->B", ab["classes"]), ("B->A", ba["classes"]), ("LOCO", lo)):
        for c, v in co.items():
            if np.isfinite(v["off"]) and (worst is None or abs(v["off"]) > abs(worst["off"])):
                worst = dict(cls=c, test=tname, off=v["off"], se=v["se"], z=v["z"])
    return dict(AB=ab, BA=ba, LOCO=lo, fails=fails, n_fail_classes=len(fails), cover_all=cover_all, passes=passes,
                scatter=0.5 * (ab["scatter"] + ba["scatter"]), ref_scatter=0.5 * (ab["ref_scatter"] + ba["ref_scatter"]),
                scatter_line=bool(ab["scatter_ok"] and ba["scatter_ok"]), worst=worst)

# ============================================================ the FRM structure: channels, budgets, floors
def resid(T, a0):
    yl = YL(T["lgb"], a0)
    return dict(dL=T["Y"] - yl, Y=T["Y"], floor=-yl, XL=XL(T["lgb"], a0), u=a0 / 10 ** T["lgb"])
def sys_med(T, arr):
    """median over the system's points (DD1's rule: NaN dropped)."""
    out = {}
    for s in sorted(set(T["sk"])):
        q = T["sk"] == s; v = arr[q]; v = v[~np.isnan(v)]
        out[s] = float(np.median(v)) if len(v) else float("nan")
    return out
def sys_e(T):
    out = {}
    for s in sorted(set(T["sk"])):
        q = T["sk"] == s; v = T["eY"][q]; v = v[np.isfinite(v)]
        out[s] = float(np.median(v)) if len(v) else float("nan")
    return out
def cstat(vals, es):
    """DD1's class statistic over systems: median, and se = max(1.2533 MAD/sqrt n, sqrt(sum e^2)/n)."""
    v = np.array([x for x in vals if np.isfinite(x)], float); e = np.array([x for x in es if np.isfinite(x)], float)
    n = len(v)
    if n == 0: return dict(off=float("nan"), se=float("nan"), n=0, z=float("nan"))
    off = float(np.median(v))
    if n == 1: se = float(e[0]) if len(e) else float("nan")
    else:
        mad = 1.4826 * float(np.median(np.abs(v - np.median(v))))
        se = max(1.2533 * mad / math.sqrt(n), math.sqrt(float(np.sum(e ** 2))) / n)
    return dict(off=off, se=se, n=n, z=(off / se if se > 0 else float("inf")))
def solve_fb(u, Xo):
    """baryon-loss budget: solve X_L(g_bar/f_b)/f_b = X_o for f_b (t = 1/f_b, LHS increases 0 -> u)."""
    if not np.isfinite(Xo) or Xo <= 0 or not np.isfinite(u) or u <= 0: return float("nan")
    if Xo >= u: return float("nan")                      # above the channel's ceiling: no baryon loss can reach it
    def f(lt):
        t = 10 ** lt; return t * (math.sqrt(1 + 4 * u / t) - 1) / 2 - Xo
    lo, hi = -12.0, 12.0
    if f(lo) > 0 or f(hi) < 0: return float("nan")
    for _ in range(160):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0: hi = mid
        else: lo = mid
    return 10 ** (-0.5 * (lo + hi))
def budgets(T, a0):
    R = resid(T, a0); Xo = 10 ** T["Y"] - 1
    fb = np.array([solve_fb(u, x) for u, x in zip(R["u"], Xo)])
    with np.errstate(divide="ignore", invalid="ignore"):
        fc = Xo / R["XL"]
        dmax = np.log10((1 + R["u"]) / (1 + R["XL"]))
    fbS, fcS, dmS = sys_med(T, fb), sys_med(T, fc), sys_med(T, dmax)
    out = {}
    for c in CLASSES:
        m = T["cls"] == c; ss = sorted(set(T["sk"][m]))
        off = float(np.median(R["dL"][m])) if m.any() else float("nan")
        out[c] = dict(
            offset=off,
            gbf_over_gbar=(10 ** (-2 * off) if np.isfinite(off) else float("nan")),   # formation field needed, no transfer
            fb=float(np.nanmedian([fbS[s] for s in ss])) if ss else float("nan"),
            fc=float(np.nanmedian([fcS[s] for s in ss])) if ss else float("nan"),
            dmax=float(np.median(dmax[m])) if m.any() else float("nan"),
            above_ceiling=float(np.mean(Xo[m] >= R["u"][m])) if m.any() else float("nan"),
            XL_med=float(np.median(R["XL"][m])) if m.any() else float("nan"),
            u_med=float(np.median(R["u"][m])) if m.any() else float("nan"))
    return out

# ============================================================ the pre-registered predictions (criteria, committed alone)
PRED = {                       # predicted d_L interval (dex), from the class's assembly / gas / environment
 "SPARC":                 (-0.05,  0.05),
 "faint rotators":        (-0.35,  0.00),
 "tidal dwarfs":          (-0.95, -0.30),
 "massive spirals":       (-0.05,  0.20),
 "ATLAS3D":               ( 0.00,  0.20),
 "RC100":                 ( 0.00,  0.20),
 "KiDS":                  (-0.15,  0.15),
 "groups":                ( 0.00,  0.30),
 "X-COP":                 (-0.30,  0.30),
 "CLASH":                 (-0.30,  0.30),
 "MW bright dwarfs":      ( 0.00,  0.30),
 "MW ultra-faints":       ( 0.30,  0.70),
 "M31 dwarfs":            ( 0.00,  0.30),
 "LG field dwarfs":       (-0.20,  0.30),
 "Coma UDGs":             ( 0.10,  0.50),
 "NGC 1052 UDGs":         (-1.05, -0.30),
}
STRIPPED = ["tidal dwarfs", "NGC 1052 UDGs"]
HOSTED   = ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs"]
FREE     = ["SPARC", "KiDS", "LG field dwarfs"]
TDGS     = ["NGC 5291N", "NGC 5291S", "NGC 5291SW", "NGC 7252E", "NGC 7252NW", "VCC 2062"]
DF       = ["DF2", "DF4"]

# ============================================================ the battery
def battery(T, a0):
    R = resid(T, a0)
    A, B = split(T, SEED)
    idxA = np.where(np.isin(T["sk"], list(A)))[0]; idxB = np.where(np.isin(T["sk"], list(B)))[0]
    allidx = np.arange(T["n"])
    sets = {"A->B": idxB, "B->A": idxA}
    off_dL = {k: class_offsets(T, v, R["dL"][v]) for k, v in sets.items()}
    off_Y  = {k: class_offsets(T, v, R["Y"][v])  for k, v in sets.items()}
    off_fl = {k: class_offsets(T, v, R["floor"][v]) for k, v in sets.items()}
    loco_dL, loco_fl = {}, {}
    for c in CLASSES:
        m = np.where(T["cls"] == c)[0]
        a = class_offsets(T, m, R["dL"][m]); b = class_offsets(T, m, R["floor"][m])
        if c in a: loco_dL[c] = a[c]
        if c in b: loco_fl[c] = b[c]
    three = {"A->B": off_dL["A->B"], "B->A": off_dL["B->A"], "LOCO": loco_dL}
    fl3   = {"A->B": off_fl["A->B"], "B->A": off_fl["B->A"], "LOCO": loco_fl}

    # ---- F1 the floor and the stripped
    Ys, es = sys_med(T, R["Y"]), sys_e(T)
    dLs = sys_med(T, R["dL"])
    below = sorted([s for s in Ys if np.isfinite(Ys[s]) and np.isfinite(es[s]) and Ys[s] < -LINE_SIG * es[s]])
    F1a = len(below) <= 3
    F1b = True; bad_b = []
    for c in CLASSES:
        ss = sorted(set(T["sk"][T["cls"] == c]))
        st = cstat([Ys[s] for s in ss], [es[s] for s in ss])
        if np.isfinite(st["off"]) and np.isfinite(st["se"]) and st["off"] < -LINE_SIG * st["se"]:
            F1b = False; bad_b.append((c, st["off"], st["se"]))
    F1c = True; bad_c = []
    for nm in TDGS + DF:
        s = None
        for k in Ys:
            if k.split("|")[-1] == nm: s = k
        if s is None: F1c = False; bad_c.append((nm, "missing")); continue
        okY = np.isfinite(Ys[s]) and np.isfinite(es[s]) and Ys[s] >= -LINE_SIG * es[s]
        okd = np.isfinite(dLs[s]) and np.isfinite(es[s]) and dLs[s] <= LINE_SIG * es[s]
        if not (okY and okd): F1c = False; bad_c.append((nm, Ys[s], dLs[s], es[s]))
    F1 = "HOLDS" if (F1a and F1b and F1c) else "FAILS"

    # ---- F2 the two named channels.
    # Two lines. FROZEN: off <= -3 se in every scoring (as committed). CORRECTED: off <= -0.30 dex (the pre-registered
    # band's lower edge) and >= floor - 3 se in every scoring, and off <= -3 se in LOCO where the class is complete.
    def f2a(line):
        bad = []
        for c in STRIPPED:
            for t in ("A->B", "B->A", "LOCO"):
                v = three[t].get(c); f = fl3[t].get(c)
                if not v: bad.append((c, t, "no scoring")); continue
                if line == "frozen":
                    if not (v["off"] <= -LINE_SIG * v["se"]): bad.append((c, t, v["off"], v["se"], "not below 3 se"))
                else:
                    if not (v["off"] <= -SIZE): bad.append((c, t, v["off"], v["se"], f"not below {SIZE} dex"))
                    if t == "LOCO" and not (v["off"] <= -LINE_SIG * v["se"]):
                        bad.append((c, t, v["off"], v["se"], "not below 3 se"))
                if f and not (v["off"] >= f["off"] - LINE_SIG * v["se"]):
                    bad.append((c, t, v["off"], f["off"], "below the floor"))
        return (not bad), bad
    F2a_froz, bad_froz = f2a("frozen")
    F2a_corr, bad_corr = f2a("corr")
    F2b = True; F2b_bad = []; npos = 0
    for c in HOSTED:
        above = True; ok = True
        for t in ("A->B", "B->A", "LOCO"):
            v = three[t].get(c)
            if not v: ok = False; F2b_bad.append((c, t, "no scoring")); continue
            if not (v["off"] >= -LINE_SIG * v["se"]): ok = False; F2b_bad.append((c, t, v["off"], v["se"]))
            if not (v["off"] >= 0): above = False
        if not ok: F2b = False
        if above: npos += 1
    if npos < 3: F2b = False
    F2a = F2a_corr; F2a_bad = bad_corr
    F2 = "HOLDS" if (F2a and F2b) else "FAILS"
    F2_frozen = "HOLDS" if (F2a_froz and F2b) else "FAILS"

    # ---- F3 the pre-registered sizes
    inside, miss = [], {}
    for c in CLASSES:
        lo, hi = PRED[c]; good = True; where = []
        for t in ("A->B", "B->A", "LOCO"):
            v = three[t].get(c)
            if not v or not (lo <= v["off"] <= hi):
                good = False
                where.append((t, None if not v else v["off"], None if not v else v["se"]))
        if good: inside.append(c)
        else: miss[c] = dict(band=[lo, hi], where=where)
    n3 = len(inside)
    F3 = "HOLDS" if n3 >= 15 else ("HOLDS EXCEPT" if n3 >= 13 else "FAILS")

    # ---- F4 the free rule, no theory assumed (DD1's held-out and LOCO machinery)
    Rr = make_rules(a0); ev = {k: evaluate(Rr, k, T) for k in ORDER}
    F4 = "HOLDS" if any(ev[k]["passes"] for k in ("N1", "N2", "N3")) else "FAILS"

    # ---- F5 the epoch does not rescale the amount
    F5 = True; F5_bad = []
    for c in FREE:
        for t in ("A->B", "B->A", "LOCO"):
            v = three[t].get(c)
            if not v or abs(v["off"]) > LINE_SIG * v["se"]:
                F5 = False; F5_bad.append((c, t, None if not v else v["off"], None if not v else v["se"]))
    F5s = "HOLDS" if F5 else "FAILS"

    if F1 == "HOLDS" and F2 == "HOLDS" and F3 == "HOLDS" and F4 == "HOLDS" and F5s == "HOLDS":
        lab = "THE FORMATION THEORY HOLDS"
    elif F1 == "HOLDS" and F2 == "HOLDS" and F5s == "HOLDS" and F3 != "FAILS":
        lab = "HOLDS EXCEPT"
    else:
        lab = "FAILS"
    if F1 == "HOLDS" and F2_frozen == "HOLDS" and F3 == "HOLDS" and F4 == "HOLDS" and F5s == "HOLDS":
        labf = "THE FORMATION THEORY HOLDS"
    elif F1 == "HOLDS" and F2_frozen == "HOLDS" and F5s == "HOLDS" and F3 != "FAILS":
        labf = "HOLDS EXCEPT"
    else:
        labf = "FAILS"
    return dict(F1=F1, F2=F2, F2_frozen=F2_frozen, F3=F3, F4=F4, F5=F5s, label=lab, label_frozen=labf,
                F1_detail=dict(n_below=len(below), below=below[:12], classes_below=bad_b, td_df=bad_c),
                F2_detail=dict(stripped_bad=F2a_bad, stripped_bad_frozen=bad_froz, hosted_bad=F2b_bad,
                               n_hosted_positive=npos),
                F3_detail=dict(n_inside=n3, inside=inside, miss=miss),
                F5_detail=F5_bad,
                three={t: {c: dict(off=v["off"], se=v["se"], n=v["n"], z=v["z"]) for c, v in three[t].items()} for t in three},
                floor3={t: {c: dict(off=v["off"], se=v["se"]) for c, v in fl3[t].items()} for t in fl3},
                ev={k: dict(passes=ev[k]["passes"], scatter=ev[k]["scatter"], ref_scatter=ev[k]["ref_scatter"],
                            scatter_line=ev[k]["scatter_line"], n_fail_classes=ev[k]["n_fail_classes"],
                            fails=ev[k]["fails"], worst=ev[k]["worst"],
                            AB=ev[k]["AB"]["classes"], BA=ev[k]["BA"]["classes"], LOCO=ev[k]["LOCO"]) for k in ORDER},
                budgets=budgets(T, a0))

def show(b, tag):
    P(f"\n== {tag}")
    P(f"  F1 the floor and the stripped:        {b['F1']}")
    P(f"  F2 the stripped low / hosted high:    {b['F2']}   (frozen 3-se line as committed: {b['F2_frozen']})")
    P(f"  F3 the pre-registered sizes:          {b['F3']}  ({b['F3_detail']['n_inside']}/16 classes inside their band)")
    P(f"  F4 the free rule (no theory assumed): {b['F4']}")
    P(f"  F5 the epoch does not rescale:        {b['F5']}")
    P(f"  -> LABEL: {b['label']}   (under the frozen line as literally written: {b['label_frozen']})")
    d = b["F1_detail"]
    P(f"  F1: systems with Y < -3 e: {d['n_below']} {d['below'] if d['below'] else ''}; "
      f"classes with median Y < -3 se: {d['classes_below'] if d['classes_below'] else 'none'}; "
      f"TDG/DF2/DF4 violating: {d['td_df'] if d['td_df'] else 'none'}")
    d = b["F2_detail"]
    P(f"  F2: stripped exceptions {d['stripped_bad'] if d['stripped_bad'] else 'none'}; "
      f"hosted exceptions {d['hosted_bad'] if d['hosted_bad'] else 'none'}; hosted with d_L >= 0 in all three: {d['n_hosted_positive']}/4")
    if d["stripped_bad_frozen"]:
        P(f"  F2 frozen-line exceptions (the 3-se clause, void where unsatisfiable - see the KA2 note): "
          f"{d['stripped_bad_frozen']}")
    d = b["F3_detail"]
    if d["miss"]:
        P("  F3 misses:")
        for c, m in d["miss"].items():
            ws = "; ".join(f"{t} {o:+.3f} (se {s:.3f})" if o is not None else f"{t} n/a" for t, o, s in m["where"])
            P(f"    {c:18s} band [{m['band'][0]:+.2f}, {m['band'][1]:+.2f}]  {ws}")
    P(f"  F5 exceptions: {b['F5_detail'] if b['F5_detail'] else 'none'}")
    P(f"  {'class':18s} {'predicted':>15s} {'A->B':>16s} {'B->A':>16s} {'LOCO':>16s}   in band")
    for c in CLASSES:
        lo, hi = PRED[c]; row = []
        for t in ("A->B", "B->A", "LOCO"):
            v = b["three"][t].get(c)
            row.append(f"{v['off']:+.3f} ({v['se']:.3f})" if v else "-")
        ok = "yes" if c in d["inside"] else "NO"
        P(f"  {c:18s} {f'[{lo:+.2f},{hi:+.2f}]':>15s} {row[0]:>16s} {row[1]:>16s} {row[2]:>16s}   {ok}")
    P(f"  {'rule':34s} {'scatter':>7s} {'ref':>6s} {'pass':>5s} {'nfail':>5s}  worst class (test, offset dex, in se)")
    for k in ORDER:
        e = b["ev"][k]; w = e["worst"]
        ws = f"{w['cls']} ({w['test']}, {w['off']:+.3f}, {w['z']:+.1f})" if w else "-"
        P(f"  {NAMES[k]:34s} {e['scatter']:7.3f} {e['ref_scatter']:6.3f} {('YES' if e['passes'] else 'no'):>5s} "
          f"{e['n_fail_classes']:5d}  {ws}")
    P(f"  transfer budgets (medians over systems): {'class':18s} {'d_L':>7s} {'f_b':>8s} {'f_C':>8s} {'d_max':>7s} "
      f"{'g_bf/g_bar':>11s} {'X_L':>7s} {'a0/g_bar':>8s} {'frac X > a0/g_bar':>17s}")
    for c in CLASSES:
        u = b["budgets"][c]
        fmt = lambda x: (f"{x:.3f}" if np.isfinite(x) else "n/a")
        P(f"    {'':18s}"[:22] + f"{c:18s} {fmt(u['offset']):>7s} {fmt(u['fb']):>8s} {fmt(u['fc']):>8s} "
          f"{fmt(u['dmax']):>7s} {fmt(u['gbf_over_gbar']):>11s} {fmt(u['XL_med']):>7s} {fmt(u['u_med']):>8s} "
          f"{fmt(u['above_ceiling']):>17s}")

# ============================================================ known answers
def synth(T, a0, kind):
    """noise-free synthetic truths on the real points."""
    T2 = build(ROWS)
    yl = YL(T2["lgb"], a0); Xl = XL(T2["lgb"], a0)
    Yn = yl.copy()
    if kind == "force":
        pass
    elif kind == "history":
        fb = {"MW bright dwarfs": 0.3, "M31 dwarfs": 0.3, "MW ultra-faints": 0.1, "Coma UDGs": 0.2}
        for i, c in enumerate(T2["cls"]):
            if c in ("tidal dwarfs", "NGC 1052 UDGs"): Yn[i] = 0.0
            elif c in fb:
                f = fb[c]; Yn[i] = np.log10(1 + XL(T2["lgb"][i] - np.log10(f), a0) / f)
    elif kind == "cluster":
        # the history truth, with the clusters additionally given the baryon-loss channel f_b = 0.40
        fb = {"MW bright dwarfs": 0.3, "M31 dwarfs": 0.3, "MW ultra-faints": 0.1, "Coma UDGs": 0.2}
        for i, c in enumerate(T2["cls"]):
            if c in ("tidal dwarfs", "NGC 1052 UDGs"): Yn[i] = 0.0
            elif c in fb:
                f = fb[c]; Yn[i] = np.log10(1 + XL(T2["lgb"][i] - np.log10(f), a0) / f)
            elif c in ("X-COP", "CLASH"):
                f = 0.40; Yn[i] = np.log10(1 + XL(T2["lgb"][i] - np.log10(f), a0) / f)
    T2["Y"] = Yn; T2["lgo"] = T2["lgb"] + Yn
    return T2

def run_KA(T, a0):
    out = {}
    # KA1 DD1's L0 LOCO offsets
    try:
        dd = json.load(open(os.path.join(DD1, "dd1.json")))
        dev = 0.0
        b = battery(T, a0)
        for c in CLASSES:
            v = b["three"]["LOCO"].get(c); w = dd["runs"][FOOT[0] if a0 == A0["canonical"] else FOOT[1]]["L0"]["LOCO"].get(c)
            if v and w: dev = max(dev, abs(v["off"] - w["off"]), abs(v["se"] - w["se"]))
        out["KA1_max_dev_vs_dd1_L0_LOCO"] = dev; out["KA1"] = "PASS" if dev <= 1e-9 else "FAIL"
    except Exception as e:
        out["KA1"] = f"FAIL ({e})"
    # KA2 synthetic truths
    r = {}
    for kind, need in (("history", lambda b: b["F1"] == "HOLDS" and b["F2"] == "HOLDS" and b["F3_detail"]["n_inside"] == 16),
                       ("force",   lambda b: b["F2"] == "FAILS" and b["F3_detail"]["n_inside"] <= 13),
                       ("cluster", lambda b: b["F3_detail"]["n_inside"] == 16)):
        b = battery(synth(T, a0, kind), a0)
        r[kind] = dict(F1=b["F1"], F2=b["F2"], F2_frozen=b["F2_frozen"], F3=b["F3"],
                       n_inside=b["F3_detail"]["n_inside"], ok=bool(need(b)),
                       frozen_f2_exceptions=b["F2_detail"]["stripped_bad_frozen"])
    out["KA2"] = r; out["KA2_pass"] = all(v["ok"] for v in r.values())
    # KA3 HIS1's structural numbers
    R = resid(T, a0); Ys, es, dLs = sys_med(T, R["Y"]), sys_e(T), sys_med(T, R["dL"])
    nb = len([s for s in Ys if np.isfinite(Ys[s]) and np.isfinite(es[s]) and Ys[s] < -LINE_SIG * es[s]])
    td = [dLs[s] for s in dLs if s.split("|")[-1] in TDGS]
    st = cstat(td, [es[s] for s in dLs if s.split("|")[-1] in TDGS])
    out["KA3"] = dict(n_below=nb, tdg_med=st["off"], tdg_se=st["se"])
    out["KA3_pass"] = bool(nb == 0 and abs(st["off"] - (-0.687)) <= 1e-3 and abs(st["se"] - 0.115) <= 1e-3)
    # KA4 the master equation's limits
    Xl = XL(T["lgb"], a0); u = a0 / 10 ** T["lgb"]
    dev_exact = 0.0
    for fc in (0.1, 0.5, 1.0, 2.0):
        planted = np.log10(1 + Xl * fc)
        dev_exact = max(dev_exact, float(np.max(np.abs((planted - YL(T["lgb"], a0)) - np.log10((1 + Xl * fc) / (1 + Xl))))))
    neg = 0; dev_naive = 0.0; nbig = 0
    for fb in (0.5, 0.8, 0.9):
        Xt = XL(T["lgb"] - np.log10(fb), a0) / fb
        d = np.log10((1 + Xt) / (1 + Xl))
        neg += int(np.sum(d < -1e-12))
        m = (Xl >= 5) & np.isfinite(d)
        if m.any():
            dev_naive = max(dev_naive, float(np.max(np.abs(d[m] - (-0.5 * np.log10(fb)))))); nbig = int(m.sum())
    out["KA4"] = dict(dev_exact=dev_exact, n_negative=neg, dev_naive=dev_naive, n_deep=nbig)
    out["KA4_pass"] = bool(dev_exact <= 1e-12 and neg == 0 and dev_naive <= 0.10)
    # KA5 X_L bounds
    g = np.linspace(-15, -8, 4001)
    xl = XL(g, a0)
    with np.errstate(divide="ignore"):
        rat = xl / np.sqrt(a0 / 10 ** g)
    out["KA5"] = dict(min_XL=float(np.min(xl)), max_ratio=float(np.max(rat)))
    out["KA5_pass"] = bool(out["KA5"]["min_XL"] > 0 and out["KA5"]["max_ratio"] <= 1.0 + 1e-12)
    return out

# ============================================================ main
T_main = build(ROWS)
P(f"FRM1 on DD1's frozen table: {T_main['n']} points, {len(set(T_main['sk']))} systems, {len(CLASSES)} classes. "
  f"criteria {RES['criteria']}, table {RES['table']}.")
P(f"tag {TAG}")

if not MUT:
    ka = {}
    for f in FOOT: ka[f] = run_KA(T_main, A0[f])
    for f in FOOT:
        k = ka[f]
        P(f"KA1 DD1 L0 LOCO reproduced [{f}]: max dev {k['KA1_max_dev_vs_dd1_L0_LOCO']:.2e} -> {k['KA1']}")
        P(f"KA2 synthetic [{f}]: " + "; ".join(
            f"{n}: F1 {v['F1']} F2 {v['F2']} F3 {v['F3']} ({v['n_inside']}/16) {'ok' if v['ok'] else 'NOT OK'}"
            for n, v in k["KA2"].items()) + f" -> {'PASS' if k['KA2_pass'] else 'FAIL'}")
        if f == "canonical":
            P(f"KA2 note: the synthetic HISTORY TRUTH (the theory's own truth) still fails the frozen F2(a) 3-se clause "
              f"for the NGC 1052 UDGs: {k['KA2']['history']['frozen_f2_exceptions']}. With n = 1 system per half, "
              f"se = e_sys = 0.34 dex, so 3 se = 1.03 dex while the X = 0 floor is 0.84 dex: the clause is "
              f"UNSATISFIABLE there, for any data. It is void, and the corrected line (0.30 dex in every scoring, "
              f"3 se in LOCO) is used for the label. Both labels are reported.")
        if f == "canonical":
            P(f"KA3 HIS1 structure [canonical]: systems below X = 0 beyond 3 e: {k['KA3']['n_below']}; "
              f"tidal dwarfs d_L {k['KA3']['tdg_med']:+.3f} +- {k['KA3']['tdg_se']:.3f} (HIS1 -0.687 +- 0.115) "
              f"-> {'PASS' if k['KA3_pass'] else 'FAIL'}")
        P(f"KA4 master equation [{f}]: planted f_C exact to {k['KA4']['dev_exact']:.2e}; "
          f"baryon-loss offsets below 0: {k['KA4']['n_negative']}; naive -1/2 log f_b within {k['KA4']['dev_naive']:.3f} dex "
          f"on {k['KA4']['n_deep']} deep points -> {'PASS' if k['KA4_pass'] else 'FAIL'}")
        P(f"KA5 X_L bounds [{f}]: min X_L {k['KA5']['min_XL']:.4g}, max X_L/sqrt(a0/g_bar) {k['KA5']['max_ratio']:.6f} "
          f"-> {'PASS' if k['KA5_pass'] else 'FAIL'}")
    allka = all(ka[f]["KA1"] == "PASS" and ka[f]["KA2_pass"] and ka[f]["KA4_pass"] and ka[f]["KA5_pass"] for f in FOOT) \
            and ka["canonical"]["KA3_pass"]
    P(f"KNOWN ANSWERS: {'ALL PASS' if allka else 'A KNOWN ANSWER FAILED'}")
    RES["KA"] = {f: ka[f] for f in FOOT}; RES["KA_all_pass"] = bool(allka)

    runs = {}
    for f in FOOT:
        b = battery(T_main, A0[f]); runs[f] = b; show(b, f"[{f}] the formation theory")
        if not allka: b = dict(b); b["label"] = "NO VERDICT"; runs[f] = b
    RES["runs"] = runs
    RES["labels"] = {f: runs[f]["label"] for f in FOOT}
    RES["labels_frozen_line"] = {f: runs[f]["label_frozen"] for f in FOOT}
    # reported, not graded
    rep = {}
    b = runs["canonical"]
    rep["dmax_XCOP"] = b["budgets"]["X-COP"]["dmax"]; rep["dmax_CLASH"] = b["budgets"]["CLASH"]["dmax"]
    rep["dmax_ultrafaints"] = b["budgets"]["MW ultra-faints"]["dmax"]
    rep["fC_stripped"] = {c: b["budgets"][c]["fc"] for c in STRIPPED}
    rep["fb_hosted"] = {c: b["budgets"][c]["fb"] for c in HOSTED}
    rep["offset_by_z"] = {c: b["three"]["LOCO"][c]["off"] for c in ("SPARC", "KiDS", "RC100", "massive spirals")}
    rep["free_rule_failing_classes"] = {k: sorted(b["ev"][k]["fails"].keys()) for k in ORDER}
    rep["N0_fails"] = sorted(b["ev"]["N0"]["fails"].keys())
    rep["N1_per_class_LOCO"] = {c: b["ev"]["N1"]["LOCO"][c]["off"] for c in CLASSES if c in b["ev"]["N1"]["LOCO"]}
    RES["reported"] = rep
    P("\nREPORTED (grades nothing)")
    P(f"  baryon-loss ceiling d_max: X-COP {rep['dmax_XCOP']:+.3f} dex, CLASH {rep['dmax_CLASH']:+.3f} dex, "
      f"MW ultra-faints {rep['dmax_ultrafaints']:+.3f} dex")
    P(f"  f_C the stripped classes would need: " + ", ".join(f"{c} {v:.3f}" for c, v in rep["fC_stripped"].items()))
    P(f"  f_b the hosted classes would need: " + ", ".join(
        f"{c} {(f'{v:.3f}' if np.isfinite(v) else 'none (above the ceiling)')}" for c, v in rep["fb_hosted"].items()))
    P(f"  offsets of the undisturbed classes, in order of observed z: " + ", ".join(
        f"{c} {v:+.3f}" for c, v in rep["offset_by_z"].items()))
    P(f"  N0 (the law alone) failing classes: {rep['N0_fails']}")
    P(f"  free rules' failing classes: " + "; ".join(f"{k}: {len(v)}" for k, v in rep["free_rule_failing_classes"].items()))

else:
    # ---- MUTATE: each arm must change its stated outcome
    M = {}
    T1 = build(ROWS); T1["Y"] = YL(T1["lgb"], A0["canonical"]); T1["lgo"] = T1["lgb"] + T1["Y"]
    b1 = battery(T1, A0["canonical"])
    M["M1_every_system_on_the_law__F2_must_FAIL"] = dict(F2=b1["F2"], bites=bool(b1["F2"] == "FAILS"))
    P(f"M1 every system on the law: F2 {b1['F2']} -> {'bites' if b1['F2'] == 'FAILS' else 'DOES NOT BITE'}")

    T2 = build(ROWS)
    sks = sorted(set(T2["sk"])); cls_of = {s: T2["cls"][T2["sk"] == s][0] for s in sks}
    rng = np.random.default_rng(SEED); perm = rng.permutation(len(sks))
    new = {sks[i]: cls_of[sks[perm[i]]] for i in range(len(sks))}
    T2["cls"] = np.array([new[s] for s in T2["sk"]])
    T2["sk"] = np.array([c + "|" + s for c, s in zip(T2["cls"], T2["sys"])])
    b2 = battery(T2, A0["canonical"])
    n2 = b2["F3_detail"]["n_inside"]
    M["M2_class_labels_shuffled__F3_count_must_fall_below_13"] = dict(n_inside=n2, bites=bool(n2 < 13))
    P(f"M2 class labels shuffled: F3 count {n2}/16 -> {'bites' if n2 < 13 else 'DOES NOT BITE'}")

    T3 = build(ROWS)
    m3 = np.isin(T3["cls"], ["X-COP", "CLASH"])
    T3["lgb"] = np.where(m3, T3["lgb"] + math.log10(0.10), T3["lgb"]); T3["Y"] = T3["lgo"] - T3["lgb"]
    b0 = battery(T_main, A0["canonical"]); b3 = battery(T3, A0["canonical"])
    rise = {}
    for c in ("X-COP", "CLASH"):
        for t in ("A->B", "B->A", "LOCO"):
            rise[f"{c} {t}"] = b3["three"][t][c]["off"] - b0["three"][t][c]["off"]
    mn = min(rise.values())
    M["M3_clusters_lose_90pct_of_their_baryons__offset_must_rise_ge_0.15"] = dict(rise=rise, min_rise=mn, bites=bool(mn >= 0.15))
    P(f"M3 clusters' g_bar x 0.10: offsets rise by " + ", ".join(f"{k} {v:+.3f}" for k, v in rise.items()) +
      f" -> {'bites' if mn >= 0.15 else 'DOES NOT BITE'}")

    b4 = battery(T_main, 2 * A0["canonical"])
    M["M4_a0_times_2__F5_must_FAIL"] = dict(F5=b4["F5"], detail=b4["F5_detail"], bites=bool(b4["F5"] == "FAILS"))
    P(f"M4 a0 x 2: F5 {b4['F5']} {b4['F5_detail']} -> {'bites' if b4['F5'] == 'FAILS' else 'DOES NOT BITE'}")
    RES["MUTATE"] = M

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)): return str(o)
    return o

RES["runtime_s"] = round(time.time() - T0, 1)
P(f"\nruntime {RES['runtime_s']} s")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, TAG + ".json"), "w") as fh: json.dump(clean(RES), fh, indent=1, allow_nan=False)
with open(os.path.join(HERE, TAG + ".out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
