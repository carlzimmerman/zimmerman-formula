"""CFG183 shared helpers (my own code) + the read-only import of the CFG165 module.
Imported read-only from CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py (SHARED, NOT INDEPENDENT):
load_kurvs, load_sparc_anchor, load_kross, per_object (via cell), pool, anchor_pool, cell, spec, alpha_K,
E_of_z, gbar, gpred, enclosed, corr, and through it CFG4_common.nu_mono and the constants.
Law plan A: the law enters the imported pipeline through the module-level E_of_z (the 'H' output of cell);
this file patches M.E_of_z inside a context manager; nothing on disk is edited.
"""
import os, sys, copy, math, contextlib
import numpy as np
from scipy.optimize import brentq

def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "campaign_fresh_gravity")):
        return os.path.abspath(r)
    p = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(p, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(p, "data_assembly")):
            return p
        p = os.path.dirname(p)
    raise SystemExit("set ZF_REPO")

REPO = find_repo()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG165_kurvs_referee"))
import CFG165_referee_kurvs_p4 as M

def scrub(txt):
    return str(txt).replace(REPO, "<repo>").replace(HERE, "<scratch>")

def pr(*a, **k):
    print(*[scrub(x) for x in a], **k)

OM0, OL0 = 0.315, 0.685
CEIL = 3.47
S_PUB = [0.0, 1.0, 1.42, 1.62, 1.69, 3.00]

# ---------------- laws: cosmic-time ratio, my own closed form + quadrature ----------------
def t_ratio(z, Om=OM0):
    z = np.asarray(z, float); OL = 1.0 - Om; k = math.sqrt(OL / Om)
    return np.arcsinh(k * (1 + z) ** -1.5) / math.asinh(k)

def _age_quad(z, Om):
    from scipy.integrate import quad
    OL = 1 - Om
    f = lambda zz: 1.0 / ((1 + zz) * math.sqrt(Om * (1 + zz) ** 3 + OL))
    return quad(f, z, np.inf, epsabs=1e-13, epsrel=1e-12)[0]

def t_ratio_quad(z, Om=OM0):
    return _age_quad(z, Om) / _age_quad(0.0, Om)

def t_ratio_onset(z, zon, Om=OM0):
    """time since flow onset at z_on, normalised to today's; zon=None -> Big Bang"""
    z = np.asarray(z, float)
    if zon is None:
        return t_ratio(z, Om)
    tz, ton = t_ratio(z, Om), float(t_ratio(zon, Om))
    return np.where(z < zon, (tz - ton) / (1 - ton), np.nan)

E_orig = M.E_of_z
def make_law(name, **kw):
    if name == "flat":
        return lambda z: np.ones_like(np.asarray(z, float))
    if name == "rival":
        return E_orig
    if name == "T":
        Om = kw.get("Om", OM0); zon = kw.get("zon", None)
        return lambda z: t_ratio_onset(z, zon, Om)
    if name == "Trecip":
        return lambda z: 1.0 / t_ratio(z)
    if name == "EdS":
        return lambda z: (1 + np.asarray(z, float)) ** -1.5
    if name == "Tconst":
        zc = kw["z"]; return lambda z: np.ones_like(np.asarray(z, float)) * float(t_ratio(zc))
    raise KeyError(name)

@contextlib.contextmanager
def law_ctx(fn):
    old = M.E_of_z
    M.E_of_z = fn
    try:
        yield
    finally:
        M.E_of_z = old

# ---------------- data ----------------
def load(inc="inc_star_deg"):
    return M.load_kurvs(inc_col=inc), M.load_sparc_anchor(), M.load_kross()

def subset(S, idx):
    idx = np.asarray(idx)
    n = len(S.z)
    T = copy.copy(S)
    for k, v in list(vars(S).items()):
        if isinstance(v, np.ndarray) and v.shape and v.shape[0] == n:
            setattr(T, k, v[idx])
        elif isinstance(v, list) and len(v) == n:
            setattr(T, k, [v[i] for i in (np.where(idx)[0] if idx.dtype == bool else idx)])
    return T

# ---------------- cells ----------------
def spec_s(s, **kw):
    return M.spec("P4", scale=float(s), **kw)

def cell(S, AS, s, mu, law=None, foot="canonical", anchor_mode="pooled", **kw):
    """returns dict: flat, law (= 'H' output, evaluated with law factor if law given else the rival) each (d, sigma)"""
    sp = spec_s(s, **kw.pop("spec_kw", {}))
    if law is None:
        r = M.cell(S, AS, sp, mu, 0.0, foot, **kw)
    else:
        with law_ctx(law):
            r = M.cell(S, AS, sp, mu, 0.0, foot, **kw)
    out = {}
    for k in ("flat", "H"):
        x = r[k]
        if anchor_mode == "pooled":
            d, sg = x["dprime"], x["sigma"]
        elif anchor_mode == "median":
            ap = M.anchor_pool(sp, 0.0, foot, AS)
            d = x["raw"] - ap["median_flat"]; sg = math.hypot(x["raw_err"], x["anchor_err"])
        elif anchor_mode == "none":
            d, sg = x["raw"], x["raw_err"]
        out[k] = (float(d), float(sg))
    out["r"] = r
    return out

def dl(S, AS, s, mu, which, law, **kw):
    """Delta', sigma for 'flat', 'rival' or 'T'-like: which in {'flat','law'}; law = fn or None (rival)"""
    c = cell(S, AS, s, mu, law, **kw)
    return c["flat"] if which == "flat" else c["H"]

# ---------------- break-even, intervals, status ----------------
MUG = np.exp(np.linspace(np.log(0.01), np.log(30.0), 200))

def _root(fn, lo, hi):
    return brentq(fn, lo, hi, xtol=1e-10, rtol=1e-12)

def breakeven(f):
    """f(mu) -> (d, sigma), d decreasing in mu.  Returns dict."""
    d = np.array([f(m)[0] for m in MUG]); sg = np.array([f(m)[1] for m in MUG])
    res = {"mu": None, "lo": None, "hi": None, "note": ""}
    if d[0] < 0:
        res["note"] = "over"; return res
    if d[-1] > 0:
        res["note"] = "under"; return res
    def root_of(g):
        gv = np.array([g(m) for m in MUG])
        sgn = np.sign(gv)
        ii = np.where((sgn[:-1] > 0) & (sgn[1:] <= 0))[0]
        if len(ii) == 0:
            return None
        i = ii[0]
        return _root(g, MUG[i], MUG[i + 1])
    res["mu"] = root_of(lambda m: f(m)[0])
    # lower edge: d = +sigma ; upper edge: d = -sigma
    gl = lambda m: f(m)[0] - f(m)[1]
    gu = lambda m: f(m)[0] + f(m)[1]
    res["lo"] = root_of(gl) if gl(MUG[0]) > 0 else 0.01
    res["hi"] = root_of(gu) if gu(MUG[-1]) < 0 else np.inf
    if res["lo"] is None: res["lo"] = 0.01
    return res

def status(be, ceil=CEIL):
    if be["mu"] is None:
        return "over" if be["note"] == "over" else "excluded"
    return "excluded" if be["lo"] > ceil else "allowed"

def fmt_be(be):
    if be["mu"] is None:
        return "none (over-predicts)" if be["note"] == "over" else "none (under-predicts)"
    hi = "inf" if not np.isfinite(be["hi"]) else "%.3f" % be["hi"]
    return "%.3f [%.3f, %s]" % (be["mu"], be["lo"], hi)

def s_root(f, target_sign=0.0, lo=0.0, hi=6.0):
    """f(s) -> (d, sigma); d increasing in s. root of d - target_sign*sigma. returns value or '<0'/'>6' strings"""
    g = lambda s: f(s)[0] - target_sign * f(s)[1]
    if g(lo) > 0: return "<0"
    if g(hi) < 0: return ">6"
    return _root(g, lo, hi)

def headline_sentence(stat_T):
    pub = [1.0, 1.42, 1.62, 1.69, 3.00]
    if all(stat_T[s] == "excluded" for s in pub):
        return "T is gas-excluded under every published prescription" + \
               (" and gas-allowed only without pressure support" if stat_T[0.0] == "allowed" else "")
    return "matrix reported as is"

# ---------------- extras used by attacks ----------------
def be_generic(f, sigma_mode="mu", mu_fixed=None):
    """breakeven with alternative sigma conventions: 'mu' (sigma at trial mu; main), 'fixed_be' (sigma at the break-even),
    'fixed' (sigma at mu_fixed)."""
    be = breakeven(f)
    if sigma_mode == "mu" or be["mu"] is None:
        return be
    mu0 = be["mu"] if sigma_mode == "fixed_be" else mu_fixed
    sg = f(mu0)[1]
    d = lambda m: f(m)[0]
    lo = brentq(lambda m: d(m) - sg, 0.01, 30.0) if d(0.01) - sg > 0 else 0.01
    hi = brentq(lambda m: d(m) + sg, 0.01, 30.0) if d(30.0) + sg < 0 else np.inf
    return {"mu": be["mu"], "lo": lo, "hi": hi, "note": ""}

def fast_be(f, edges=True):
    """fast root(s): mu_be by brentq on [0.01,30]; lower/upper edges likewise (sigma at trial mu)."""
    d = lambda m: f(m)[0]
    if d(0.01) < 0: return {"mu": None, "lo": None, "hi": None, "note": "over"}
    if d(30.0) > 0: return {"mu": None, "lo": None, "hi": None, "note": "under"}
    mu = brentq(d, 0.01, 30.0, xtol=1e-8)
    out = {"mu": mu, "lo": None, "hi": None, "note": ""}
    if edges:
        gl = lambda m: f(m)[0] - f(m)[1]; gu = lambda m: f(m)[0] + f(m)[1]
        out["lo"] = brentq(gl, 0.01, 30.0, xtol=1e-8) if gl(0.01) > 0 else 0.01
        out["hi"] = brentq(gu, 0.01, 30.0, xtol=1e-8) if gu(30.0) < 0 else np.inf
    return out

def kross_meta():
    import csv
    rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "high_z_tf_tables", "kross_v2.csv"))))
    return {r["name"]: r for r in rows}

def bar_pressure(S, AS, s):
    r = M.cell(S, AS, spec_s(s), 0.67, 0.0, "canonical")["flat"]
    return r
