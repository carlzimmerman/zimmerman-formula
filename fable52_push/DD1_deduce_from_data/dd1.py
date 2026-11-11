#!/usr/bin/env python3
"""DD1: does the non-baryonic mass follow ONE rule across every class on disk? (criteria 2a3f76f295, table 441824e854)
TEST lane, quarantined; adopts nothing. kappa = 1/2 FITTED; not theory closed. One thread.
Usage: python3 dd1.py            -> dd1.json / dd1.out
       python3 dd1.py --mutate   -> dd1_MUTATE.json / dd1_MUTATE.out
Statistic: Y = log10(g_obs / g_bar) = log10(1 + X), X = M_C(<r) / M_b(<r). Residuals are dex in g_obs at fixed g_bar.
"""
import os, sys, csv, math, json, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from scipy.optimize import minimize
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "dd1_MUTATE" if MUT else "dd1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
G, MS, PC, CL = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
SEED = 20261110; LINE_DEX = 0.10; LINE_SIG = 3.0; BIN1 = 0.2; BIN2 = 0.4; MINPTS = 5
RES = dict(lane="DD1", criteria="2a3f76f295", table="441824e854", tag=TAG, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           KA={}, runs={}, labels={}, reported={}, MUTATE={})

# ======================================================================== the frozen table
def load_table():
    rows = []
    with open(os.path.join(HERE, "dd1_table.csv")) as fh:
        lines = [l for l in fh if not l.startswith("#")]
    for r in csv.DictReader(lines):
        rows.append(dict(cls=r["cls"], sys=r["sys"], bracket=r["bracket"], r_kpc=float(r["r_kpc"]), lgb=float(r["lgb"]), lgo=float(r["lgo"]),
                         e_lgb=float(r["e_lgb"]), e_lgo=float(r["e_lgo"]), eY=float(r["eY"]), z=float(r["z"]), lSig=float(r["lSig"]), last=int(r["last"])))
    return rows
ROWS = load_table()
CLASSES = []
for r in ROWS:
    if r["bracket"] == "" and r["cls"] not in CLASSES: CLASSES.append(r["cls"])

def build(rows):
    """arrays + derived variables. dep = log10(g_obs r / c^2); dsys = system max dep; Mb = log10 M_b(<r) / Msun."""
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
def table(bracket=None):
    """main table; bracket 'kids_hot' replaces KiDS by the hot-gas Nobins, 'atlas_salp' replaces ATLAS3D by Salpeter."""
    if bracket is None: rows = [r for r in ROWS if r["bracket"] == ""]
    elif bracket == "kids_hot": rows = [r for r in ROWS if (r["bracket"] == "" and r["cls"] != "KiDS") or r["bracket"] == "kids_hot"]
    elif bracket == "atlas_salp": rows = [r for r in ROWS if (r["bracket"] == "" and r["cls"] != "ATLAS3D") or r["bracket"] == "atlas_salp"]
    return build(rows)

# ======================================================================== helpers
def wmed(v, w):
    v = np.asarray(v, float); w = np.asarray(w, float)
    m = ~np.isnan(v); v, w = v[m], w[m]
    if len(v) == 0: return float("nan")
    o = np.argsort(v, kind="mergesort"); v, w = v[o], w[o]; c = np.cumsum(w)
    return float(v[np.searchsorted(c, 0.5 * c[-1])])
def XL(lgb, a0):
    t = a0 / 10 ** np.asarray(lgb, float); return 2 * t / (np.sqrt(1 + 4 * t) + 1)          # = (sqrt(1 + 4 a0/g_bar) - 1)/2, stable form
def YL(lgb, a0): return np.log10(1 + XL(lgb, a0))

# ======================================================================== rules: fit(T, idx) -> model; pred(model, T, idx) -> (Yhat, extrapolated flag)
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
    nodes = np.array(sorted(nodes)) if nodes else np.zeros((0, 3))
    return nodes
def pred2(nodes, x1, x2):
    n = len(x1); out = np.full(n, np.nan); ext = np.zeros(n, bool)
    if len(nodes) == 0: return out, ext
    pts = nodes[:, :2] / BIN2; q = np.c_[np.asarray(x1, float), np.asarray(x2, float)] / BIN2; ok = np.all(np.isfinite(q), axis=1)
    near = NearestNDInterpolator(pts, nodes[:, 2])
    lin = None
    if len(nodes) >= 3:
        try: lin = LinearNDInterpolator(pts, nodes[:, 2])
        except Exception: lin = None
    if lin is not None:
        v = lin(q[ok]); bad = ~np.isfinite(v); v[bad] = near(q[ok][bad]); out[ok] = v; e = np.zeros(ok.sum(), bool); e[bad] = True; ext[ok] = e
    else:
        out[ok] = near(q[ok]); ext[ok] = True
    return out, ext
def fit_a0(lgb, Y, w):
    """L1/L2: a0 with system-weighted median residual 0 (monotone in a0: Lean law_mono_a)."""
    def f(la): return wmed(Y - YL(lgb, 10 ** la), w)
    lo, hi = -16.0, -4.0; flo, fhi = f(lo), f(hi)
    if not (flo > 0 > fhi): return 10 ** (lo if flo <= 0 else hi)
    for _ in range(80):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if fm > 0: lo = mid
        else: hi = mid
    return 10 ** (0.5 * (lo + hi))

def make_rules(a0f):
    R = {}
    for key, v in (("a", "lgb"), ("b", "lgo"), ("c", "dep"), ("c'", "dsys"), ("d", "lSig"), ("e", "Mb"), ("f", "lr"), ("g", "zz")):
        R[key] = dict(kind="1d", v=v, fit=(lambda T, idx, v=v: fit1(v, T, idx)), pred=(lambda m, T, idx, v=v: pred1(m, T[v][idx])))
    for key, (v1, v2) in (("P1", ("lgb", "lr")), ("P2", ("lgb", "zz")), ("P3", ("lgb", "dsys"))):
        R[key] = dict(kind="2d", fit=(lambda T, idx, v1=v1, v2=v2: fit2(v1, v2, T, idx)), pred=(lambda m, T, idx, v1=v1, v2=v2: pred2(m, T[v1][idx], T[v2][idx])))
    R["L0"] = dict(kind="law", fit=lambda T, idx: a0f, pred=lambda m, T, idx: (YL(T["lgb"][idx], m), np.zeros(len(idx), bool)))
    R["L1"] = dict(kind="law", fit=lambda T, idx: fit_a0(T["lgb"][idx], T["Y"][idx], T["w"][idx]),
                   pred=lambda m, T, idx: (YL(T["lgb"][idx], m), np.zeros(len(idx), bool)))
    def fitL2(T, idx):
        return {c: fit_a0(T["lgb"][idx][T["cls"][idx] == c], T["Y"][idx][T["cls"][idx] == c], T["w"][idx][T["cls"][idx] == c]) for c in np.unique(T["cls"][idx])}
    def predL2(m, T, idx):
        out = np.full(len(idx), np.nan)
        for c, a in m.items():
            s = T["cls"][idx] == c; out[s] = YL(T["lgb"][idx][s], a)
        return out, np.zeros(len(idx), bool)
    R["L2"] = dict(kind="law2", fit=fitL2, pred=predL2)
    def fitC0(T, idx): return wmed(T["Y"][idx], np.ones(len(idx)))
    R["CONS0"] = dict(kind="cons", fit=fitC0, pred=lambda m, T, idx: (np.full(len(idx), m), np.zeros(len(idx), bool)))
    def fitC1(T, idx):
        y, d = T["Y"][idx], T["dsys"][idx]; ok = np.isfinite(y) & np.isfinite(d); y, d = y[ok], d[ok]
        def f(p): return float(np.sum(np.abs(y - np.log10(1 + 10 ** (p[0] + p[1] * d)))))
        best = None
        for p0 in (-0.5, 0.0, 0.5):
            x0 = np.array([float(np.median(np.log10(np.maximum(10 ** y - 1, 1e-3)) - p0 * d)), p0])
            r = minimize(f, x0, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=4000))
            if best is None or r.fun < best.fun: best = r
        return best.x
    R["CONS1"] = dict(kind="cons", fit=fitC1, pred=lambda m, T, idx: (np.log10(1 + 10 ** (m[0] + m[1] * T["dsys"][idx])), ~np.isfinite(T["dsys"][idx])))
    return R
ORDER = ["a", "b", "c", "c'", "d", "e", "f", "g", "P1", "P2", "P3", "L0", "L1", "L2", "CONS0", "CONS1"]
NAMES = {"a": "(a) g_bar [= x]", "b": "(b) g_obs", "c": "(c) local depth", "c'": "(c') system depth", "d": "(d) system Sigma_b [partial]",
         "e": "(e) enclosed M_b", "f": "(f) radius", "g": "(g) redshift [control]", "P1": "P1 (g_bar, r)", "P2": "P2 (g_bar, z)",
         "P3": "P3 (g_bar, system depth)", "L0": "L0 law, footing a0", "L1": "L1 law, one free a0", "L2": "L2 law, a0 per class [diag]",
         "CONS0": "CONS0 X_last = C", "CONS1": "CONS1 X_last = C dsys^p"}
FULL = [k for k in ORDER if k not in ("d", "L2", "g")]           # candidates covering every class that can set the label

# ======================================================================== split and scoring
def systems(T):
    out = {}
    for c in CLASSES:
        out[c] = sorted(set(T["sk"][T["cls"] == c]))
    return out
def split(T, seed):
    rng = np.random.default_rng(seed); A, B = set(), set()
    for c, ss in systems(T).items():
        if not ss: continue
        p = rng.permutation(len(ss)); h = int(math.ceil(len(ss) / 2))
        A |= {ss[i] for i in p[:h]}; B |= {ss[i] for i in p[h:]}
    return A, B
def cand_mask(key, T):
    if key in ("CONS0", "CONS1"): return T["last"] == 1
    if key == "d": return np.isfinite(T["lSig"])
    return np.ones(T["n"], bool)
def class_offsets(T, idx, d, eY_scale=1.0):
    """per class: off = median over systems of the system median residual; se rule of the criteria."""
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
        ok = bool(np.isfinite(off) and abs(off) <= LINE_DEX and abs(off) <= LINE_SIG * se)
        out[c] = dict(off=off, se=se, n=n, z=(off / se if se > 0 else float("inf")), pass_=ok)
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
    """class-constant reference: each class predicted by its own system-weighted training median."""
    out = np.full(len(te), np.nan)
    for c in CLASSES:
        mt = T["cls"][tr] == c; me = T["cls"][te] == c
        if mt.any() and me.any(): out[me] = wmed(T["Y"][tr][mt], T["w"][tr][mt])
    return out
def run_split(R, key, T, trS, teS, eY_scale=1.0):
    cm = cand_mask(key, T)
    tr = np.where(cm & np.isin(T["sk"], list(trS)))[0]; te = np.where(cm & np.isin(T["sk"], list(teS)))[0]
    model = R[key]["fit"](T, tr); yh, ext = R[key]["pred"](model, T, te)
    with np.errstate(invalid="ignore"): d = T["Y"][te] - yh
    rd = T["Y"][te] - ref_pred(T, tr, te)
    co = class_offsets(T, te, d, eY_scale)
    sc, rsc = bal_scatter(T, te, d), bal_scatter(T, te, rd)
    return dict(classes=co, scatter=sc, ref_scatter=rsc, point_scatter=pt_scatter(d), scatter_ok=bool(sc <= rsc),
                extrap=float(ext.mean()) if len(ext) else 0.0, all_pass=bool(all(v["pass_"] for v in co.values())),
                model=(model if isinstance(model, (float, int)) else (model.tolist() if isinstance(model, np.ndarray) else model)))
def run_loco(R, key, T, eY_scale=1.0):
    out = {}; cm = cand_mask(key, T)
    for c in CLASSES:
        te = np.where(cm & (T["cls"] == c))[0]; tr = np.where(cm & (T["cls"] != c))[0]
        if len(te) == 0: continue
        model = R[key]["fit"](T, tr); yh, ext = R[key]["pred"](model, T, te)
        with np.errstate(invalid="ignore"): d = T["Y"][te] - yh
        co = class_offsets(T, te, d, eY_scale)
        if c in co: out[c] = dict(co[c], extrap=float(ext.mean()))
    return out
def evaluate(R, key, T, seed=SEED, eY_scale=1.0, loco=True):
    A, B = split(T, seed)
    ab = run_split(R, key, T, A, B, eY_scale); ba = run_split(R, key, T, B, A, eY_scale)
    lo = run_loco(R, key, T, eY_scale) if (loco and R[key]["kind"] != "law2") else {}
    fails = {}
    for tname, co in (("A->B", ab["classes"]), ("B->A", ba["classes"]), ("LOCO", lo)):
        for c, v in co.items():
            if not v["pass_"]: fails.setdefault(c, []).append(dict(test=tname, off=v["off"], se=v["se"], z=v["z"]))
    covered = set(ab["classes"]) | set(ba["classes"])
    cover_all = all(c in covered for c in CLASSES)
    passes = bool(ab["all_pass"] and ba["all_pass"] and ab["scatter_ok"] and ba["scatter_ok"] and (not loco or R[key]["kind"] == "law2" or all(v["pass_"] for v in lo.values())))
    worst = None
    for tname, co in (("A->B", ab["classes"]), ("B->A", ba["classes"]), ("LOCO", lo)):
        for c, v in co.items():
            if np.isfinite(v["off"]) and (worst is None or abs(v["off"]) > abs(worst["off"])): worst = dict(cls=c, test=tname, off=v["off"], se=v["se"], z=v["z"])
    return dict(AB=ab, BA=ba, LOCO=lo, fails=fails, n_fail_classes=len(fails), cover_all=cover_all, passes=passes,
                scatter=0.5 * (ab["scatter"] + ba["scatter"]), ref_scatter=0.5 * (ab["ref_scatter"] + ba["ref_scatter"]),
                scatter_line=bool(ab["scatter_ok"] and ba["scatter_ok"]), worst=worst)
def label_of(E):
    ok = [k for k in FULL if E[k]["passes"] and E[k]["cover_all"]]
    if ok:
        best = min(ok, key=lambda k: E[k]["scatter"]); return "ONE RULE ORGANIZES EVERY CLASS", best, ok
    near = [k for k in FULL if E[k]["cover_all"] and E[k]["n_fail_classes"] <= 2 and E[k]["scatter_line"]]
    if near:
        best = min(near, key=lambda k: (E[k]["n_fail_classes"], abs(E[k]["worst"]["off"]) if E[k]["worst"] else 0)); return "ONE RULE EXCEPT", best, near
    best = min(FULL, key=lambda k: (E[k]["n_fail_classes"], E[k]["scatter"])); return "NO RULE AMONG THE CANDIDATES", best, []
def evaluate_all(T, a0f, keys=ORDER, **kw):
    R = make_rules(a0f); return {k: evaluate(R, k, T, **kw) for k in keys}

# ======================================================================== printing
def fmt_fail(F):
    return "; ".join(f"{c} ({', '.join(f'{x['test']} {x['off']:+.2f} [{x['z']:+.1f}se]' for x in v)})" for c, v in F.items())
def print_eval(E, title):
    P(f"\n== {title}")
    P(f"{'candidate':34s} {'scatter':>7s} {'ref':>6s} {'pass':>5s} {'nfail':>5s}  worst class (test, offset dex, in se)")
    for k in ORDER:
        if k not in E: continue
        e = E[k]; w = e["worst"]
        ws = f"{w['cls']} ({w['test']}, {w['off']:+.3f}, {w['z']:+.1f})" if w else "-"
        P(f"{NAMES[k]:34s} {e['scatter']:7.3f} {e['ref_scatter']:6.3f} {('YES' if e['passes'] else 'no'):>5s} {e['n_fail_classes']:5d}  {ws}")
def print_detail(E, k):
    e = E[k]; P(f"   {NAMES[k]}: scatter A->B {e['AB']['scatter']:.3f} (ref {e['AB']['ref_scatter']:.3f}, points {e['AB']['point_scatter']:.3f}, "
                f"extrapolated {e['AB']['extrap']:.2f}), B->A {e['BA']['scatter']:.3f} (ref {e['BA']['ref_scatter']:.3f})")
    P(f"   {'class':18s} {'A->B off (se, n)':>24s} {'B->A off (se, n)':>24s} {'LOCO off (se)':>20s}")
    for c in CLASSES:
        s = []
        for t in ("AB", "BA"):
            v = e[t]["classes"].get(c); s.append(f"{v['off']:+.3f} ({v['se']:.3f}, {v['n']}){'' if v['pass_'] else '*'}" if v else "-")
        v = e["LOCO"].get(c); s.append(f"{v['off']:+.3f} ({v['se']:.3f}){'' if v['pass_'] else '*'}" if v else "-")
        P(f"   {c:18s} {s[0]:>24s} {s[1]:>24s} {s[2]:>20s}")
    if e["fails"]: P(f"   failing classes: {fmt_fail(e['fails'])}")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else str(float(o))
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
def slim(E):
    return {k: dict(passes=v["passes"], cover_all=v["cover_all"], n_fail_classes=v["n_fail_classes"], scatter=v["scatter"], ref_scatter=v["ref_scatter"],
                    scatter_line=v["scatter_line"], worst=v["worst"], fails=v["fails"],
                    AB=dict((kk, vv) for kk, vv in v["AB"].items()), BA=dict((kk, vv) for kk, vv in v["BA"].items()), LOCO=v["LOCO"]) for k, v in E.items()}

T = table()
P(f"DD1 {'MUTATE ' if MUT else ''}run. Table: {T['n']} points, {len(set(T['sk']))} systems, {len(CLASSES)} classes. Seed {SEED}.")
if not MUT:
    # ==================================================================== KA1: SHP1 reproduced
    P("\nKA1: SHP1 reproduced")
    shp = json.load(open(os.path.join(REPO, "fable52_push", "SHP1_cold_component_shape", "shp1.json")))
    def u_in(y): y = np.asarray(y, float); return 0.5 * y + np.sqrt(0.25 * y * y + y)
    S = np.where(T["cls"] == "SPARC")[0]; gb, go = 10 ** T["lgb"][S], 10 ** T["lgo"][S]
    LBX = np.arange(-1.25, 1.5001, 0.25); ka1 = {}
    for f in FOOT:
        a0 = A0[f]; dl = np.log10(go / (a0 * u_in(gb / a0))); lx = np.log10(np.sqrt(a0 / gb)); mx = 0.0; nb = 0
        ref = {round(b["lx_lo"], 3): b for b in shp["rows"][f]["R1"]["bins"]}
        for lo, hi in zip(LBX[:-1], LBX[1:]):
            m = (lx >= lo) & (lx < hi)
            if not m.any(): continue
            b = ref[round(float(lo), 3)]; mx = max(mx, abs(float(np.median(dl[m])) - b["median_delta"])); nb += 1
            assert int(m.sum()) == b["n"], (f, lo, int(m.sum()), b["n"])
        ka1[f] = dict(R1_max_dev=mx, R1_bins=nb)
    # KiDS Nobins R2, published and hot gas, with the full covariance (SHP1's cov and R2, restated)
    B21 = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar"); G_PC = 4.52e-30; CONV = 4 * G_PC * PC
    def esd(fn):
        a = np.loadtxt(os.path.join(B21, fn), comments="#"); return dict(gbar=a[:, 0], gobs=4 * G_PC * a[:, 1] / a[:, 4] * PC)
    def cov(fn, gbar):
        c = np.loadtxt(os.path.join(B21, fn), comments="#"); n = len(gbar); C = np.zeros((n, n))
        for row in c:
            Ri, Rj, cv, bias = row[2], row[3], row[4], row[6]
            I = int(np.argmin(np.abs(np.log(gbar / Ri)))); J = int(np.argmin(np.abs(np.log(gbar / Rj)))); C[I, J] = CONV ** 2 * cv / bias
        return C
    for nm, fe, fc in (("published", "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"),
                       ("hotgas", "Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt", "Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt")):
        D = esd(fe); C = cov(fc, D["gbar"])
        for f in FOOT:
            gl = A0[f] * u_in(D["gbar"] / A0[f]); r = D["gobs"] - gl; c2 = float(r @ np.linalg.inv(C) @ r)
            q = D["gobs"] / gl - 1; Cq = C / np.outer(gl, gl); Ci = np.linalg.inv(Cq); o = np.ones(len(q)); mq = float(o @ Ci @ q / (o @ Ci @ o))
            ref = shp["rows"][f]["R2" if nm == "published" else "R2_hotgas"]
            ka1[f][f"R2_{nm}"] = dict(chi2=c2, ref_chi2=ref["chi2"], mean=mq, ref_mean=ref["mean_ratio_minus_1"],
                                      dev_mean=abs(mq - ref["mean_ratio_minus_1"]), dev_chi2_rel=abs(c2 / ref["chi2"] - 1))
    nS = len(set(T["sk"][S]))
    ka1_ok = bool(len(S) == 2700 and nS == 149 and all(ka1[f]["R1_max_dev"] <= 1e-9 for f in FOOT) and
                  all(ka1[f][f"R2_{nm}"]["dev_mean"] <= 1e-6 and ka1[f][f"R2_{nm}"]["dev_chi2_rel"] <= 1e-6 for f in FOOT for nm in ("published", "hotgas")))
    cnt = json.load(open(os.path.join(HERE, "dd1_table_counts.json")))
    RES["KA"]["KA1"] = dict(points=len(S), galaxies=nS, files=cnt["SPARC"]["files"], per_footing=ka1, pass_=ka1_ok)
    for f in FOOT:
        P(f"  [{f}] SPARC R1: {ka1[f]['R1_bins']} bins, max |median delta - SHP1| {ka1[f]['R1_max_dev']:.1e}; KiDS Nobins mean ratio - 1: published "
          f"{ka1[f]['R2_published']['mean']:+.4f} (SHP1 {ka1[f]['R2_published']['ref_mean']:+.4f}), chi2 {ka1[f]['R2_published']['chi2']:.2f} "
          f"(SHP1 {ka1[f]['R2_published']['ref_chi2']:.2f}); hot gas {ka1[f]['R2_hotgas']['mean']:+.4f} ({ka1[f]['R2_hotgas']['ref_mean']:+.4f}), "
          f"chi2 {ka1[f]['R2_hotgas']['chi2']:.2f} ({ka1[f]['R2_hotgas']['ref_chi2']:.2f})")
    P(f"  SPARC {cnt['SPARC']['files']} files, {nS} galaxies, {len(S)} points -> KA1 {'PASS' if ka1_ok else 'FAIL'}")

    # ==================================================================== KA3: loaders; KA4: identities
    P("\nKA3: loader counts and the Coma UDGs' own columns")
    def ncls(c): return len(set(T["sk"][T["cls"] == c]))
    k3 = dict(CLASH_points=int((T["cls"] == "CLASH").sum()), CLASH_clusters=ncls("CLASH"), RC100=ncls("RC100"), groups=ncls("groups"),
              XCOP=ncls("X-COP"), TDG=ncls("tidal dwarfs"), Coma=ncls("Coma UDGs"),
              coma_max_dlgb=max(abs(x["d_lgb"]) for x in cnt["KA3_coma"]), coma_max_dlgo=max(abs(x["d_lgo"]) for x in cnt["KA3_coma"]))
    fre_rows = sum(1 for l in open(os.path.join(REPO, "real_research", "data", "freundlich2022_coma_udgs.tsv")) if l.strip() and not l.startswith("#")) - 1
    k3["coma_file_rows"] = fre_rows
    k3_ok = bool(k3["CLASH_points"] == 84 and k3["CLASH_clusters"] == 20 and k3["RC100"] == 100 and k3["groups"] == 20 and k3["XCOP"] == 7
                 and k3["TDG"] == 6 and k3["Coma"] == fre_rows and k3["coma_max_dlgb"] <= 0.10 and k3["coma_max_dlgo"] <= 0.10)
    RES["KA"]["KA3"] = dict(k3, pass_=k3_ok)
    P(f"  {k3} -> KA3 {'PASS' if k3_ok else 'FAIL'}")
    P("KA4: law identities numerically")
    gg = np.logspace(-15, -8, 400); k4 = {}
    for f in FOOT:
        a0 = A0[f]; x = XL(np.log10(gg), a0); g = gg * (1 + x)
        k4[f] = dict(gobs_rel=float(np.max(np.abs(x * g / a0 - 1))), law_rel=float(np.max(np.abs(gg * (g + a0) / g ** 2 - 1))))
    k4_ok = all(v["gobs_rel"] <= 1e-12 and v["law_rel"] <= 1e-12 for v in k4.values())
    RES["KA"]["KA4"] = dict(k4, pass_=bool(k4_ok)); P(f"  {k4} -> KA4 {'PASS' if k4_ok else 'FAIL'}")

    # ==================================================================== KA2: synthetic tables
    P("\nKA2: synthetic tables (noise free; se from the real errors)")
    def synth(kind, a0=None):
        S2 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in T.items()}
        lgb = S2["lgb"]
        if kind == "law": Y = YL(lgb, a0)
        elif kind == "const": Y = np.full(S2["n"], math.log10(6.0))
        elif kind == "depth":
            A = CL / 150e3; b = 10 ** lgb * S2["r_kpc"] * KPC / CL ** 2
            X = (A * A * b + np.sqrt(A ** 4 * b * b + 4 * A * A * b)) / 2
            assert np.max(np.abs(X - A * np.sqrt(b * (1 + X))) / X) < 1e-10
            Y = np.log10(1 + X)
        S2["lgo"] = lgb + Y; S2["Y"] = Y
        rm = S2["r_kpc"] * KPC; S2["dep"] = S2["lgo"] + np.log10(rm) - 2 * math.log10(CL)
        ds = {}
        for k, d in zip(S2["sk"], S2["dep"]): ds[k] = max(ds.get(k, -np.inf), d)
        S2["dsys"] = np.array([ds[k] for k in S2["sk"]])
        return S2
    k2 = {}; k2_ok = True
    for f in FOOT:
        Es = evaluate_all(synth("law", A0[f]), A0[f], keys=["a", "L0", "g"])
        ok = Es["a"]["passes"] and Es["L0"]["passes"] and not Es["g"]["passes"]
        k2[f"law_{f}"] = dict(a=Es["a"]["passes"], L0=Es["L0"]["passes"], g=Es["g"]["passes"], worst_a=Es["a"]["worst"], worst_L0=Es["L0"]["worst"],
                              g_fails=list(Es["g"]["fails"]), g_scatter_line=Es["g"]["scatter_line"], pass_=bool(ok)); k2_ok &= ok
        P(f"  (i) law [{f}]: (a) {'PASSES' if Es['a']['passes'] else 'fails'} (worst {Es['a']['worst']['off']:+.4f}), L0 {'PASSES' if Es['L0']['passes'] else 'fails'}, "
          f"(g) {'PASSES' if Es['g']['passes'] else 'does not pass'} (fails {len(Es['g']['fails'])} classes; scatter line {Es['g']['scatter_line']}) -> {'PASS' if ok else 'FAIL'}")
    Es = evaluate_all(synth("const"), A0["canonical"], keys=["CONS0", "a"])
    C0 = 10 ** Es["CONS0"]["AB"]["model"] - 1; C0b = 10 ** Es["CONS0"]["BA"]["model"] - 1
    ok = Es["CONS0"]["passes"] and abs(C0 / 5 - 1) <= 0.01 and abs(C0b / 5 - 1) <= 0.01 and Es["a"]["passes"]
    k2["const"] = dict(CONS0=Es["CONS0"]["passes"], C_AB=C0, C_BA=C0b, a=Es["a"]["passes"], pass_=bool(ok)); k2_ok &= ok
    P(f"  (ii) constant X = 5: CONS0 {'PASSES' if Es['CONS0']['passes'] else 'fails'}, C = {C0:.4f} / {C0b:.4f}; (a) {'PASSES' if Es['a']['passes'] else 'fails'} -> {'PASS' if ok else 'FAIL'}")
    Es = evaluate_all(synth("depth"), A0["canonical"], keys=["c", "a", "g"])
    ok = Es["c"]["passes"] and not Es["a"]["passes"] and not Es["g"]["passes"]
    k2["depth"] = dict(c=Es["c"]["passes"], a=Es["a"]["passes"], g=Es["g"]["passes"], worst_c=Es["c"]["worst"], a_fails=list(Es["a"]["fails"]),
                       g_fails=list(Es["g"]["fails"]), pass_=bool(ok)); k2_ok &= ok
    P(f"  (iii) depth X = A dep^(1/2): (c) {'PASSES' if Es['c']['passes'] else 'fails'} (worst {Es['c']['worst']['off']:+.4f}); (a) {'PASSES' if Es['a']['passes'] else 'does not pass'} "
      f"(fails {list(Es['a']['fails'])}); (g) {'PASSES' if Es['g']['passes'] else 'does not pass'} -> {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA2"] = dict(k2, pass_=bool(k2_ok))
    KA_OK = all(v["pass_"] for v in RES["KA"].values())
    P(f"\nKNOWN ANSWERS: {'ALL PASS' if KA_OK else 'A KNOWN ANSWER FAILS -> NO VERDICT'}")

    # ==================================================================== main runs
    for f in FOOT:
        E = evaluate_all(T, A0[f])
        print_eval(E, f"MAIN [{f}]  (scatter = class-balanced held-out dex, mean of both splits; ref = class constants)")
        lab, best, near = label_of(E)
        if not KA_OK: lab = "NO VERDICT"
        RES["runs"][f] = slim(E); RES["labels"][f] = dict(label=lab, best=best, near=near)
        P(f"-> LABEL [{f}]: {lab}; best candidate {NAMES[best]} (failing classes {E[best]['n_fail_classes']}, scatter {E[best]['scatter']:.3f})")
        if f == "canonical":
            for k in ORDER: print_detail(E, k)
        else:
            print_detail(E, "L0")
    # reported (descriptive, grades nothing): per-class description; class x candidate matrix; failures beyond errors
    P("\nREPORTED: the classes as measured (system medians; X_last at each system's outermost point; g_c = g_obs - g_bar)")
    P(f"  {'class':18s} {'pts':>5s} {'sys':>4s} {'med lg g_bar':>12s} {'med Y':>7s} {'med X_last':>10s} {'z range':>13s} {'max g_c/a0':>10s}")
    desc = {}
    for c in CLASSES:
        m = T["cls"] == c; ss = sorted(set(T["sk"][m]))
        lgbs = [float(np.median(T["lgb"][T["sk"] == s])) for s in ss]; Ys = [float(np.median(T["Y"][T["sk"] == s])) for s in ss]
        Xl = [float(10 ** T["Y"][(T["sk"] == s) & (T["last"] == 1)][0] - 1) for s in ss]
        with np.errstate(invalid="ignore"): gc = (10 ** T["lgo"][m] - 10 ** T["lgb"][m]) / A0["canonical"]
        desc[c] = dict(points=int(m.sum()), systems=len(ss), med_lgb=float(np.median(lgbs)), med_Y=float(np.median(Ys)), med_Xlast=float(np.median(Xl)),
                       z_min=float(T["z"][m].min()), z_max=float(T["z"][m].max()), max_gc_over_a0=float(np.nanmax(gc)))
        d = desc[c]; P(f"  {c:18s} {d['points']:5d} {d['systems']:4d} {d['med_lgb']:12.2f} {d['med_Y']:7.3f} {d['med_Xlast']:10.2f} {d['z_min']:6.3f}-{d['z_max']:5.3f} {d['max_gc_over_a0']:10.2f}")
    RES["reported"]["classes"] = desc
    E0 = RES["runs"]["canonical"]
    P(f"\nREPORTED: which candidates each class fails (the {len(FULL)} full-cover candidates; beyond errors = fails beyond 3 se in some test, not only the 0.10 dex line)")
    mat = {}
    for c in CLASSES:
        fl_ = [k for k in FULL if c in E0[k]["fails"]]; hard = [k for k in fl_ if any(abs(x["z"]) > LINE_SIG for x in E0[k]["fails"][c])]
        offs = {}
        for k in FULL:
            o = [v["classes"][c]["off"] for v in (E0[k]["AB"], E0[k]["BA"]) if c in v["classes"]] + ([E0[k]["LOCO"][c]["off"]] if c in E0[k]["LOCO"] else [])
            offs[k] = max(o, key=abs) if o else float("nan")
        bestk = min(FULL, key=lambda k: abs(offs[k]) if np.isfinite(offs[k]) else 9e9)
        mat[c] = dict(n_fail=len(fl_), n_fail_beyond_errors=len(hard), fails=fl_, beyond=hard, best_candidate=bestk, best_worst_offset=offs[bestk])
        P(f"  {c:18s} fails {len(fl_):2d} / {len(FULL)} ({len(hard):2d} beyond errors); kindest candidate {NAMES[bestk]} with worst offset {offs[bestk]:+.3f}")
    RES["reported"]["class_by_candidate"] = mat
    P("  per candidate, classes failing beyond 3 se: " + "; ".join(f"{k} {sum(1 for c in CLASSES if c in E0[k]['fails'] and any(abs(x['z']) > LINE_SIG for x in E0[k]['fails'][c]))}" for k in FULL))
    # reported: L2's per-class a0 with a bootstrap over systems
    P("\nREPORTED: L2, the law's curve with a0 per class (all systems of the class; 68 % bootstrap over systems, 300 draws)")
    rng = np.random.default_rng(SEED + 2); l2 = {}
    for c in CLASSES:
        m = np.where(T["cls"] == c)[0]; ss = sorted(set(T["sk"][m])); a = fit_a0(T["lgb"][m], T["Y"][m], T["w"][m]); bs = []
        for _ in range(300):
            pick = rng.choice(len(ss), len(ss)); idx = np.concatenate([m[T["sk"][m] == ss[i]] for i in pick])
            ww = np.concatenate([np.full((T["sk"][m] == ss[i]).sum(), 1.0 / (T["sk"][m] == ss[i]).sum()) for i in pick])
            bs.append(fit_a0(T["lgb"][idx], T["Y"][idx], ww))
        lo_, hi_ = np.percentile(np.log10(bs), [16, 84])
        l2[c] = dict(a0=a, ratio_canonical=a / A0["canonical"], ratio_alt=a / A0["alt"], lg_lo=float(lo_), lg_hi=float(hi_))
        P(f"  {c:18s} a0 = {a:.3e}  ({a / A0['canonical']:6.2f} x canonical, {a / A0['alt']:6.2f} x alt)  68 %: {10 ** lo_ / A0['canonical']:.2f}-{10 ** hi_ / A0['canonical']:.2f} x canonical")
    RES["reported"]["L2_a0_per_class"] = l2
    # reported: brackets
    for br in ("kids_hot", "atlas_salp"):
        TB = table(br); E = evaluate_all(TB, A0["canonical"], keys=FULL)
        lab, best, near = label_of(E)
        RES["reported"][f"bracket_{br}"] = dict(label=lab, best=best, near=near, summary={k: dict(passes=E[k]["passes"], n_fail=E[k]["n_fail_classes"], fails=list(E[k]["fails"]),
                                                  scatter=E[k]["scatter"], worst=E[k]["worst"]) for k in FULL})
        P(f"\nREPORTED bracket {br} [canonical]: {lab}; best {NAMES[best]}")
        for k in FULL:
            w = E[k]["worst"]; P(f"  {NAMES[k]:34s} nfail {E[k]['n_fail_classes']:2d} scatter {E[k]['scatter']:.3f}  fails: {', '.join(E[k]['fails'])}")
        ck = "KiDS" if br == "kids_hot" else "ATLAS3D"
        for k in ("a", "L0", "P1"):
            v = E[k]; P(f"   {ck} under {NAMES[k]}: A->B {v['AB']['classes'].get(ck, {}).get('off', float('nan')):+.3f}  B->A {v['BA']['classes'].get(ck, {}).get('off', float('nan')):+.3f}  LOCO {v['LOCO'].get(ck, {}).get('off', float('nan')):+.3f}")
    # reported: 50 other seeds
    P("\nREPORTED: 50 other seeds (1..50), fraction in which each candidate holds both splits (every class + scatter line)")
    R = make_rules(A0["canonical"]); frac = {}
    for k in ORDER:
        if k == "L2": continue
        n_ok = 0
        for s in range(1, 51):
            A, B = split(T, s); ab = run_split(R, k, T, A, B); ba = run_split(R, k, T, B, A)
            n_ok += int(ab["all_pass"] and ba["all_pass"] and ab["scatter_ok"] and ba["scatter_ok"])
        frac[k] = n_ok / 50
    RES["reported"]["seeds_fraction_both_splits"] = frac
    P("  " + ", ".join(f"{k} {v:.2f}" for k, v in frac.items()))
else:
    # ==================================================================== MUTATE
    def outcome_a(TT, a0=A0["canonical"], eY_scale=1.0):
        R = make_rules(a0); A, B = split(TT, SEED); return run_split(R, "a", TT, A, B, eY_scale)
    base = outcome_a(T)
    worst0 = max(abs(v["off"]) for v in base["classes"].values() if np.isfinite(v["off"]))
    # M1 class labels shuffled across systems
    rng = np.random.default_rng(7); TT = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in T.items()}
    ss = sorted(set(T["sk"])); labs = [s.split("|")[0] for s in ss]; perm = rng.permutation(len(ss)); newc = {ss[i]: labs[perm[i]] for i in range(len(ss))}
    TT["cls"] = np.array([newc[s] for s in T["sk"]]); TT["sk"] = np.array([newc[s] + "|" + s for s in T["sk"]])
    m1 = outcome_a(TT); worst1 = max(abs(v["off"]) for v in m1["classes"].values() if np.isfinite(v["off"]))
    RES["MUTATE"]["M1"] = dict(worst_real=worst0, worst_shuffled=worst1, change=abs(worst1 - worst0), bites=bool(abs(worst1 - worst0) >= 0.05))
    P(f"M1 class labels shuffled: (a) worst |class offset| A->B {worst0:.3f} -> {worst1:.3f} (change {abs(worst1 - worst0):.3f}; line 0.05) -> {'bites' if RES['MUTATE']['M1']['bites'] else 'DOES NOT BITE'}")
    # M2 g_bar x 2 for CLASH
    TT = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in T.items()}; mC = TT["cls"] == "CLASH"
    TT["lgb"][mC] += math.log10(2); TT["Y"][mC] -= math.log10(2); TT["Mb"][mC] += math.log10(2)
    m2 = outcome_a(TT); o0, o2 = base["classes"]["CLASH"]["off"], m2["classes"]["CLASH"]["off"]
    RES["MUTATE"]["M2"] = dict(off_real=o0, off_mut=o2, change=abs(o2 - o0), bites=bool(abs(o2 - o0) >= 0.10))
    P(f"M2 CLASH g_bar x 2: CLASH offset under (a) A->B {o0:+.3f} -> {o2:+.3f} (change {abs(o2 - o0):.3f}; line 0.10) -> {'bites' if RES['MUTATE']['M2']['bites'] else 'DOES NOT BITE'}")
    # M3 errors halved: count failing (candidate, test, class) triples
    def count_fail(eY_scale):
        R = make_rules(A0["canonical"]); n = 0
        for k in ORDER:
            e = evaluate(R, k, T, eY_scale=eY_scale); n += sum(len(v) for v in e["fails"].values())
        return n
    n0, n3 = count_fail(1.0), count_fail(0.5)
    RES["MUTATE"]["M3"] = dict(fail_triples_real=n0, fail_triples_halved=n3, bites=bool(n3 > n0))
    P(f"M3 errors halved: failing (candidate, test, class) triples {n0} -> {n3} -> {'bites' if n3 > n0 else 'DOES NOT BITE'}")
    # M4 a0 x 2 in L0
    R = make_rules(2 * A0["canonical"]); A, B = split(T, SEED); m4 = run_split(R, "L0", T, A, B)
    R0 = make_rules(A0["canonical"]); b4 = run_split(R0, "L0", T, A, B)
    RES["MUTATE"]["M4"] = dict(SPARC_off_real=b4["classes"]["SPARC"]["off"], SPARC_pass_real=b4["classes"]["SPARC"]["pass_"],
                               SPARC_off_mut=m4["classes"]["SPARC"]["off"], SPARC_pass_mut=m4["classes"]["SPARC"]["pass_"], bites=bool(not m4["classes"]["SPARC"]["pass_"]))
    P(f"M4 a0 x 2 in L0: SPARC offset A->B {b4['classes']['SPARC']['off']:+.3f} ({'pass' if b4['classes']['SPARC']['pass_'] else 'fail'}) -> "
      f"{m4['classes']['SPARC']['off']:+.3f} ({'pass' if m4['classes']['SPARC']['pass_'] else 'fail'}) -> {'bites' if RES['MUTATE']['M4']['bites'] else 'DOES NOT BITE'}")

RES["runtime_s"] = time.time() - T0
P(f"\nruntime {RES['runtime_s']:.0f} s"); P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
