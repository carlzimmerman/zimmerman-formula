"""zkurvs: the record's KURVS/KROSS pipeline (CFG141 exec'd READ-ONLY and unmutated; CFG160's Kretschmer alpha; CFG175's delta / break-even / s0 machinery COPIED verbatim) as an importable module.
Nothing is written into the record's directories.  LAWS is a mutable registry: register any a0(z)/a0(0) function under a name and call delta(sample, mu, s, name).
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.optimize import brentq
from zcommon import *

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
sys.path.insert(0, CFG)
import CFG7_common as Cc                                    # noqa: E402  (read-only import; no Report is opened, nothing is written into CFG)

F141 = os.path.join(CFG, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
_saved = os.environ.pop("MUTATE", None)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
finally:
    if _saved is not None:
        os.environ["MUTATE"] = _saved
KU2, SP, KR = g141["KU2"], g141["SP"], g141["g140"]["KR"]
A0, E141, gbar, gpred, slope, KPC = g141["A0"], g141["E"], g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
OM = g141["g140"]["OM"]
assert abs(OM - 0.315) < 1e-12 and abs(E141(1.5) - math.sqrt(OM * 2.5 ** 3 + 1 - OM)) < 1e-12
LN10, FOOT = math.log(10), "canonical"

cos = Cosmo(H0=67.4, Om=OM, Or=9.1e-5)
L = laws(cos)
LAWS = {
    "flat": lambda z: 1.0,
    "rival": E141,                                                       # a0 ~ E(z): the H(z) footing
    "T": lambda z: tratio(z, OM),
    "D": L["particle horizon d_p (radius OR diameter)"],
    "event": L["event horizon d_e at t(z)"],
    "LCDMn": lambda z: lcdm_native(z),
}
LAWN = tuple(LAWS)


def alpha_k21(x):                                                          # CFG160's, verbatim
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def pooled(d, s):                                                          # CFG140's
    w = 1 / s ** 2
    m = float(np.sum(w * d) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    chi = float(np.sum(w * (d - m) ** 2)); dof = max(len(d) - 1, 1)
    if chi / dof > 1:
        e *= math.sqrt(chi / dof)
    return m, e


def terms(objs):
    V = np.array([o["V"] for o in objs]); eV = np.array([o["eV"] for o in objs]); sg = np.array([o["sig"] for o in objs])
    es = np.array([o["esig"] for o in objs]); Rr = np.array([o["R"] for o in objs]); sm = np.array([o["sm"] for o in objs])
    inc = [math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60) for o in objs]
    ti = np.array([2 * o["V"] ** 2 * o["einc"] / math.tan(i) for o, i in zip(objs, inc)])
    ak = np.array([alpha_k21(o["R"] / (1.68 * o["Rd"]) - 1.0) for o in objs])
    return dict(V=V, eV=eV, sg=sg, es=es, R=Rr, sm=sm, ti=ti, ak=ak)


def DS(T, s, gp, sl):
    al = s * T["ak"]
    vc2 = T["V"] ** 2 + al * T["sg"] ** 2
    go = vc2 * 1e6 / (T["R"] * KPC)
    dlog = np.sqrt((2 * T["V"] * T["eV"]) ** 2 + (2 * al * T["sg"] * T["es"]) ** 2 + T["ti"] ** 2) / vc2 / LN10
    return np.log10(go / gp), np.hypot(dlog, sl * T["sm"])


TK, TR, TS = terms(KU2), terms(KR), terms(SP)
SAMP = {"KURVS": (KU2, TK), "KROSS": (KR, TR)}
S_LIST = (0.0, 1.00, 1.42, 1.62, 1.69, 3.00)
S_NAME = {0.0: "P0 none", 1.00: "P4 Kretschmer", 1.42: "Dalcanton&Stilp", 1.62: "P3 fixed height", 1.69: "Price n=1", 3.00: "P2 self-grav"}
MU_BR = (0.25, 0.67, 1.5, 4.0)
CEIL = 3.47
_pred, _anp = {}, {}
VSCALE = 1.0                                                              # coherent velocity scale (used only in the sensitivity block)


def pred(name, mu, law):
    key = (name, round(mu, 12), law)
    if key not in _pred:
        objs = SAMP[name][0] if name != "SPARC" else SP
        gb = np.array([gbar(o, 0.67, 0.0, True) if name == "SPARC" else gbar(o, mu, 0.0) for o in objs])
        a = np.array([A0[FOOT] * LAWS[law](o["z"]) for o in objs])
        _pred[key] = (np.array([gpred(g, aa) for g, aa in zip(gb, a)]), np.array([slope(g, aa) for g, aa in zip(gb, a)]))
    return _pred[key]


def anchor(s, law):
    gp, sl = pred("SPARC", 0.67, law)
    return pooled(*DS(TS, s, gp, sl))


def delta(name, mu, s, law, vscale=1.0):
    gp, sl = pred(name, mu, law)
    T = SAMP[name][1]
    if vscale != 1.0:
        T = dict(T); T["V"] = T["V"] * vscale
    k, ek = pooled(*DS(T, s, gp, sl))
    an, ea = anchor(s, law)
    return k - an, math.hypot(ek, ea)


GRID = np.exp(np.linspace(math.log(0.01), math.log(30.0), 36))


def root_mu(name, s, law, target):
    fn = lambda mu: (lambda d: d[0] - target * d[1])(delta(name, mu, s, law))
    vals = [fn(m) for m in GRID]
    for lo, hi, flo, fhi in zip(GRID[:-1], GRID[1:], vals[:-1], vals[1:]):
        if flo == 0:
            return float(lo)
        if flo * fhi < 0:
            return float(brentq(fn, lo, hi, xtol=1e-6, rtol=1e-6))
    return float("nan")


def breakeven(name, s, law):
    return root_mu(name, s, law, 0.0), root_mu(name, s, law, +1.0), root_mu(name, s, law, -1.0)


def status(name, s, law, be):
    if np.isfinite(be[0]):
        lo = be[1] if np.isfinite(be[1]) else 0.0
        return "gas-excluded" if lo > CEIL else "gas-allowed"
    if delta(name, 0.01, s, law)[0] < 0:
        return "over-predicts"
    return "gas-excluded" if delta(name, 30.0, s, law)[0] > 0 else "no break-even"


def s0(name, law, mu=0.67):
    fn = lambda s: delta(name, mu, s, law)[0]
    f0, f6 = fn(0.0), fn(6.0)
    if f0 > 0:
        return float("-inf")
    if f6 < 0:
        return float("inf")
    return float(brentq(fn, 0.0, 6.0, xtol=1e-6))


fs = lambda v: "< 0" if v == float("-inf") else ("> 6" if v == float("inf") else f"{v:.3f}")
