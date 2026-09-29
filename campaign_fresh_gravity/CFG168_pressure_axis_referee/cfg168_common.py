#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG168 common glue (referee of CFG162), as frozen in CFG168_FROZEN_CRITERIA.md section 7.
Imports the CFG165 referee module read-only (shared, NOT independent: loaders, sigma_out, per_object, pool, classify, alpha_K, nu_mono).
Everything else here (continuous-s curves, brentq crossings, bootstrap, placements, break-evens, mocks) is new code.
CFG162's script/out/json are NOT opened by any of this."""
import os
import sys
import math
import copy
import json

sys.dont_write_bytecode = True
_mut = os.environ.pop("MUTATE", None)          # CFG165 module reads MUTATE; keep it out of its import
import numpy as np
from scipy.optimize import brentq
from scipy.special import k0, k1
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "data_assembly")):
        return r
    d = HERE
    for _ in range(10):
        if os.path.isdir(os.path.join(d, "data_assembly")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO")


REPO = _find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG165_kurvs_referee"))
import CFG165_referee_kurvs_p4 as M      # noqa: E402  (read-only shared element)

if _mut is not None:
    os.environ["MUTATE"] = _mut
MUT = os.environ.get("CFG168_MUTATE", "0")

P = lambda *a: print(*a, flush=True)
FOOTS = M.FOOTS
MUS = M.MUS
DELS = M.DELS
LN10 = math.log(10.0)


# ------------------------------------------------------------------------------------------------ data
def load_S(inc_col="inc_star_deg"):
    return M.load_kurvs(inc_col=inc_col)


def load_A():
    A = M.load_sparc_anchor()
    A.tag = "base"
    return A


def clone(S, **kw):
    T = copy.copy(S)
    for k, v in kw.items():
        setattr(T, k, v)
    return T


def subset(S, mask, tag):
    n = len(S.R)
    T = copy.copy(S)
    for k, v in list(vars(S).items()):
        if isinstance(v, np.ndarray) and v.shape[:1] == (n,):
            setattr(T, k, v[mask])
        elif isinstance(v, list) and len(v) == n:
            setattr(T, k, [x for x, m in zip(v, mask) if m])
    T.tag = tag
    return T


# ------------------------------------------------------------------------------------------------ prescriptions
def alpha_price(y):
    y = np.asarray(y, float)
    return y * k1(y) / k0(y)


def alpha_ds(y):
    return 0.92 * np.asarray(y, float)


def spec_alpha(name, f):
    """alpha(S, anchor) = f(R/R_d)"""
    return M.spec("alpha", fn=lambda S_, a: f(S_.R / S_.Rd), name=name)


def spec_k21(s, refac=1.0):
    return M.spec("P4", scale=float(s), Refac=refac, Refac_anchor=refac)


PRESC = {
    "P0": None,
    "K21": None,
    "D&S 2010": spec_alpha("DS", alpha_ds),
    "P3 (fixed height)": M.spec("P3"),
    "Price 2022 (n=1)": spec_alpha("Price", alpha_price),
    "P2 (self-grav.)": M.spec("P2"),
}


def spkey(sp):
    if sp is None:
        return "None"
    d = {k: (v if not callable(v) else "fn") for k, v in sp.items()}
    return json.dumps(d, sort_keys=True, default=str)


# ------------------------------------------------------------------------------------------------ cells
_acache = {}


def anchor_off(A, sp_anchor, delta, foot, anchor_mode="pooled"):
    key = (getattr(A, "tag", "base"), spkey(sp_anchor), delta, foot)
    if key not in _acache:
        po = M.per_object(A, sp_anchor, None, delta, foot, anchor=True)
        pf = M.pool(po["d_flat"], po["e_flat"])
        _acache[key] = dict(pooled=pf, median=float(np.median(po["d_flat"])))
    r = _acache[key]
    m, e, c = r["pooled"]
    if anchor_mode == "none":
        return 0.0, e, c
    if anchor_mode == "median":
        return r["median"], e, c
    return m, e, c


def cellx(S, A, sp, mu, delta=0.0, foot="canonical", sp_anchor=None, anchor_mode="pooled", gas_scale=2.0):
    """decision-cell style cell: Delta'_law = pooled KURVS raw - anchor offset (flat pooled for both laws), sigma quadrature."""
    po = M.per_object(S, sp, mu, delta, foot, gas_scale=gas_scale)
    am, ae, ac = anchor_off(A, sp if sp_anchor is None else sp_anchor, delta, foot, anchor_mode)
    res = {}
    for law in ("flat", "H"):
        m, e, c = M.pool(po["d_" + law], po["e_" + law])
        dp = m - am
        sg = math.sqrt(e ** 2 + ae ** 2)
        res[law] = dict(raw=m, raw_err=e, anchor=am, dprime=dp, sigma=sg, z=dp / sg)
    res["f_press"] = float(np.mean(po["Vc2_over_V2"]) - 1.0)
    res["po"] = po
    return res


def K21cell(S, A, s, mu=0.67, delta=0.0, foot="canonical", refac=1.0, **kw):
    return cellx(S, A, spec_k21(s, refac), mu, delta, foot, **kw)


def dflat_K21(S, A, s, **kw):
    return K21cell(S, A, s, **kw)["flat"]["dprime"]


def root(f, lo, hi):
    try:
        flo, fhi = f(lo), f(hi)
    except Exception:
        return None
    if not (np.isfinite(flo) and np.isfinite(fhi)) or flo * fhi > 0:
        return None
    return float(brentq(f, lo, hi, xtol=1e-10, rtol=1e-12))


def crossings(S, A, mu=0.67, delta=0.0, foot="canonical", refac=1.0, lo=0.0, hi=4.0, swap=False, **kw):
    """s_mid: Dflat = -DH;  s_f2: Dflat = +2 sig_flat;  s_h2: DH = -2 sig_H (swap=True uses the other law: M2 control)."""
    def c(s):
        return K21cell(S, A, s, mu, delta, foot, refac, **kw)
    fl, hh = ("H", "flat") if swap else ("flat", "H")
    s_mid = root(lambda s: (lambda r: r["flat"]["dprime"] + r["H"]["dprime"])(c(s)), lo, hi)
    s_f2 = root(lambda s: (lambda r: r[fl]["dprime"] - 2 * r[fl]["sigma"])(c(s)), lo, hi)
    s_h2 = root(lambda s: (lambda r: r[hh]["dprime"] + 2 * r[hh]["sigma"])(c(s)), lo, hi)
    return dict(s_mid=s_mid, s_f2=s_f2, s_h2=s_h2)


def breakeven_mu(fn, lo=0.05, hi=60.0):
    """fn(mu) -> Delta'; root in [lo,hi] on log mu."""
    g = lambda lm: fn(math.exp(lm))
    r = root(g, math.log(lo), math.log(hi))
    return None if r is None else math.exp(r)


def s_eq(S, A, target, which="flat", mu=0.67, refac=1.0, lo=0.0, hi=6.0, **kw):
    return root(lambda s: K21cell(S, A, s, mu, refac=refac, **kw)[which]["dprime"] - target, lo, hi)


def mean_alpha_ratio(S, sp, refac=1.0):
    C, _ = M.corr(S, sp)
    C1, _ = M.corr(S, spec_k21(1.0, refac))
    return C / S.sig ** 2, C1 / S.sig ** 2


# ------------------------------------------------------------------------------------------------ s-grid curves and bootstrap
def grid_arrays(S, A, sgrid, mu=0.67, delta=0.0, foot="canonical", refac=1.0, anchor_mode="pooled"):
    """per-galaxy d,e for both laws on an s grid (shape (ns, n)); anchor offset and error per s; per-galaxy anchor arrays too."""
    ns, n = len(sgrid), len(S.R)
    Df = np.zeros((ns, n)); Ef = np.zeros((ns, n)); Dh = np.zeros((ns, n)); Eh = np.zeros((ns, n))
    Af = np.zeros(ns); Ae = np.zeros(ns)
    AD = []; AE = []
    for i, s in enumerate(sgrid):
        sp = spec_k21(s, refac)
        po = M.per_object(S, sp, mu, delta, foot)
        Df[i], Ef[i], Dh[i], Eh[i] = po["d_flat"], po["e_flat"], po["d_H"], po["e_H"]
        pa = M.per_object(A, sp, None, delta, foot, anchor=True)
        AD.append(pa["d_flat"]); AE.append(pa["e_flat"])
        m, e, c = M.pool(pa["d_flat"], pa["e_flat"])
        Af[i], Ae[i] = (0.0 if anchor_mode == "none" else m), e
    return dict(s=np.asarray(sgrid), Df=Df, Ef=Ef, Dh=Dh, Eh=Eh, Af=Af, Ae=Ae, AD=np.array(AD), AE=np.array(AE))


def pool_v(D, E):
    """vectorised M.pool over the last axis (n); D,E shape (..., n)"""
    w = 1.0 / E ** 2
    sw = w.sum(-1)
    m = (w * D).sum(-1) / sw
    chi2 = (w * (D - m[..., None]) ** 2).sum(-1)
    n = D.shape[-1]
    dof = max(n - 1, 1)
    infl = np.sqrt(np.where(chi2 / dof > 1, chi2 / dof, 1.0))
    return m, (1.0 / np.sqrt(sw)) * infl


def curves_from(G, idx, aidx=None):
    """Delta'_flat, sigma_flat, Delta'_H, sigma_H vs s for a galaxy resample idx (and optional anchor resample)"""
    mf, ef = pool_v(G["Df"][:, idx], G["Ef"][:, idx])
    mh, eh = pool_v(G["Dh"][:, idx], G["Eh"][:, idx])
    if aidx is None:
        Af, Ae = G["Af"], G["Ae"]
    else:
        Af, Ae = pool_v(G["AD"][:, aidx], G["AE"][:, aidx])
    sf = np.sqrt(ef ** 2 + Ae ** 2); sh = np.sqrt(eh ** 2 + Ae ** 2)
    return mf - Af, sf, mh - Af, sh


def cross_from_curves(s, df, sf, dh, sh):
    """crossings by cubic-spline root on the grid; None when no sign change in the grid range"""
    out = {}
    for name, y in (("s_mid", df + dh), ("s_f2", df - 2 * sf), ("s_h2", dh + 2 * sh)):
        sg = np.sign(y)
        k = np.where(sg[:-1] * sg[1:] < 0)[0]
        if len(k) == 0:
            out[name] = None
            continue
        cs = CubicSpline(s, y)
        j = k[0]
        out[name] = float(brentq(lambda t: float(cs(t)), s[j], s[j + 1], xtol=1e-10))
    return out


def bootstrap(S, A, nboot, seed, sgrid=None, mu=0.67, delta=0.0, foot="canonical", refac=1.0, boot_anchor=False):
    sgrid = np.arange(0.0, 4.0 + 1e-9, 0.01) if sgrid is None else sgrid
    G = grid_arrays(S, A, sgrid, mu, delta, foot, refac)
    rng = np.random.default_rng(seed)
    n = len(S.R); na = len(A.R)
    res = {"s_mid": [], "s_f2": [], "s_h2": []}
    none = {"s_mid": 0, "s_f2": 0, "s_h2": 0}
    for b in range(nboot):
        idx = rng.integers(0, n, n)
        aidx = rng.integers(0, na, na) if boot_anchor else None
        cur = curves_from(G, idx, aidx)
        cr = cross_from_curves(G["s"], *cur)
        for k in res:
            if cr[k] is None:
                none[k] += 1
            else:
                res[k].append(cr[k])
    return res, none, G


def pct(x, q=(16, 50, 84)):
    return [float(np.percentile(x, p)) for p in q] if len(x) else [None] * len(q)


def jackknife(S, A, refac=1.0, **kw):
    out = []
    n = len(S.R)
    for j in range(n):
        m = np.ones(n, bool); m[j] = False
        T = subset(S, m, f"jk{j}")
        out.append(crossings(T, A, refac=refac, **kw)["s_mid"])
    return out


def fmt(x, nd=3):
    return "None" if x is None else f"{x:.{nd}f}"
