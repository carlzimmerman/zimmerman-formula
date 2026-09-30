#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG194 library -- referee re-derivation of CFG189 (KURVS a0(z) with the MEASURED outer markers).
Written from CFG194_FROZEN_CRITERIA.md alone; CFG189's .py/.out/.json were not open.
Imports (SHARED, not independent): CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py as M (read-only, MUTATE forced to "0").
Everything else (marker reader, outer-point rules, sigma at R_out, t(z)/t0, break-evens, status, headline) is mine.
"""
import os
import sys
import math
import copy
import csv
import importlib.util

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "data_assembly")):
        return r
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "data_assembly")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO")


REPO = find_repo()
MODE = os.environ.get("MUTATE", "0")
_mut = os.environ.get("MUTATE")
os.environ["MUTATE"] = "0"
_p = os.path.join(REPO, "campaign_fresh_gravity", "CFG165_kurvs_referee", "CFG165_referee_kurvs_p4.py")
_spec = importlib.util.spec_from_file_location("CFG165_ref", _p)
M = importlib.util.module_from_spec(_spec)
sys.modules["CFG165_ref"] = M
_spec.loader.exec_module(M)
M.MODE = "0"
if _mut is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _mut

LN10 = math.log(10.0)
IDS = list(M.KURVS_IDS)
S_AXIS = (0.0, 1.0, 1.42, 1.62, 1.69, 3.00)
PLACED = (1.00, 1.42, 1.62, 1.69, 3.00)
GAS_CEIL = 3.47
DEC_MU = 0.67
OM, OL = 0.315, 0.685


def P(*a):
    print(" ".join(str(x) for x in a), flush=True)


# ------------------------------------------------------------------------------------------------ laws
def tt0_dex(z):
    """log10 t(z)/t0 for flat LCDM, Omega_m = 0.315 (closed form)."""
    z = np.asarray(z, float)
    f = lambda zz: np.arcsinh(math.sqrt(OL / OM) * (1.0 + zz) ** -1.5)
    return np.log10(f(z) / f(0.0))


def E_flat(z):
    return np.ones_like(np.asarray(z, float))


def E_T(z):
    return 10.0 ** tt0_dex(z)


_E_RIVAL = M.E_of_z


class law_ctx:
    def __init__(self, fn):
        self.fn = fn

    def __enter__(self):
        M.E_of_z = self.fn

    def __exit__(self, *a):
        M.E_of_z = _E_RIVAL


LAWS = ("flat", "rival", "T")


def cells_three(S, AS, sp, mu=DEC_MU, delta=0.0, foot="canonical", gas_scale=2.0):
    """returns {law: dict(dprime, sigma, z, raw, chi2dof)} for flat, rival(H), T at one (mu, sp)."""
    out = {}
    r = M.cell(S, AS, sp, mu, delta, foot, gas_scale=gas_scale)
    out["flat"] = r["flat"]
    out["rival"] = r["H"]
    with law_ctx(E_T):
        rt = M.cell(S, AS, sp, mu, delta, foot, gas_scale=gas_scale)
    out["T"] = rt["H"]
    return out


def spec_s(s):
    return M.spec("P0") if s == 0 else M.spec("P4", scale=float(s))


# ------------------------------------------------------------------------------------------------ data
def read_rows(path):
    with open(os.path.join(REPO, path), newline="") as f:
        return list(csv.DictReader(f))


def fnum(s):
    try:
        return float(s)
    except Exception:
        return float("nan")


def load_markers(ids=IDS):
    """per disc: dict of arrays R (signed), v, eup, elo, clip, plus e (mean bar)."""
    rows = read_rows("data_assembly/arxiv_tables/kurvs_rc_profiles/kurvs_rc_points.csv")
    D = {}
    for r in rows:
        k = int(r["kurvs_id"])
        if k not in ids:
            continue
        D.setdefault(k, []).append((fnum(r["R_kpc"]), fnum(r["v_obs_kms"]), fnum(r["err_up_kms"]), fnum(r["err_lo_kms"]),
                                    int(fnum(r["clipped_white_marker"])), int(fnum(r["has_errbar"]))))
    out = {}
    for k, l in D.items():
        a = np.array(l, float)
        out[k] = dict(R=a[:, 0], v=a[:, 1], eup=a[:, 2], elo=a[:, 3], clip=a[:, 4].astype(int), hasbar=a[:, 5].astype(int))
        out[k]["e"] = 0.5 * (a[:, 2] + a[:, 3])
    return out


def load_sigma(ids=IDS):
    rows = read_rows("data_assembly/arxiv_tables/kurvs_sigma_profiles/kurvs_sigma_profiles.csv")
    D = {}
    for r in rows:
        k = int(r["kurvs_id"])
        if k not in ids:
            continue
        s = fnum(r["sigma_obs_kms"])
        e = 0.5 * (fnum(r["err_up_kms"]) + fnum(r["err_lo_kms"])) if int(fnum(r["has_errbar"])) == 1 else 0.2 * s
        D.setdefault(k, []).append((fnum(r["R_kpc"]), s, e, int(fnum(r["clipped_white_marker"]))))
    return {k: dict(R=np.array(l)[:, 0], s=np.array(l)[:, 1], e=np.array(l)[:, 2], clip=np.array(l)[:, 3].astype(int)) for k, l in D.items()}


def load_model_curves(ids=IDS):
    rows = read_rows("data_assembly/arxiv_tables/kurvs_rc_profiles/kurvs_rc_model_curves.csv")
    D = {}
    for r in rows:
        k = int(r["kurvs_id"])
        if k in ids:
            D.setdefault(k, []).append((fnum(r["R_kpc"]), fnum(r["v_model_obs_kms"])))
    out = {}
    for k, l in D.items():
        a = np.array(sorted(l))
        out[k] = dict(R=a[:, 0], v=a[:, 1])
    return out


def sigma_side(sg, Rabs, side):
    """sigma and error at |R| = Rabs on `side` from the UNCLIPPED sigma points of that side (clamped at the ends)."""
    m = (sg["clip"] == 0) & (np.sign(sg["R"]) == side)
    if m.sum() == 0:
        m = (sg["clip"] == 0)
    R = np.abs(sg["R"][m])
    o = np.argsort(R)
    return float(np.interp(Rabs, R[o], sg["s"][m][o])), float(np.interp(Rabs, R[o], sg["e"][m][o]))


def side_pts(mk, side, allow_clipped=False, drop=None):
    m = (np.sign(mk["R"]) == side)
    if not allow_clipped:
        m &= (mk["clip"] == 0)
    if drop is not None:
        m &= ~drop
    idx = np.where(m)[0]
    o = idx[np.argsort(np.abs(mk["R"][idx]))]
    return o   # indices sorted by |R| ascending


def interp_side(mk, side, Rabs, allow_clipped=False, drop=None):
    o = side_pts(mk, side, allow_clipped, drop)
    R = np.abs(mk["R"][o])
    return float(np.interp(Rabs, R, np.abs(mk["v"][o]))), float(np.interp(Rabs, R, mk["e"][o]))


# ------------------------------------------------------------------------------------------------ outer-point rules
# each rule returns dict(Robs, Vobs, eobs (observed, NOT deprojected), side, sig, esig) for one disc
def far_side(mk, allow_clipped=False, drop=None):
    best = None
    for side in (+1, -1):
        o = side_pts(mk, side, allow_clipped, drop)
        if len(o) == 0:
            continue
        Rm = abs(mk["R"][o[-1]])
        if best is None or Rm > best[0] + 0.005 or (abs(Rm - best[0]) <= 0.005 and side == +1):
            best = (Rm, side)
    return best[1], best[0]


def rule_primary(mk, sg, allow_clipped=False, drop=None, sigmode="interp"):
    side, R = far_side(mk, allow_clipped, drop)
    o = side_pts(mk, side, allow_clipped, drop)
    j = o[-1]
    s, es = sig_at(sg, R, side, sigmode)
    return dict(R=R, v=abs(mk["v"][j]), e=mk["e"][j], side=side, sig=s, esig=es)


def sig_at(sg, R, side, mode="interp"):
    if mode == "nearest":
        m = (np.sign(sg["R"]) == side) & (sg["clip"] == 0)
        i = np.where(m)[0]
        j = i[np.argmin(np.abs(np.abs(sg["R"][i]) - R))]
        return float(sg["s"][j]), float(sg["e"][j])
    return sigma_side(sg, R, side)


def rule_outerk(mk, sg, k, drop=None):
    side, R0 = far_side(mk, False, drop)
    o = side_pts(mk, side, False, drop)[-k:]
    w = 1.0 / mk["e"][o] ** 2
    v = float(np.sum(w * np.abs(mk["v"][o])) / np.sum(w))
    e = float(1.0 / math.sqrt(np.sum(w)))
    R = float(np.sum(w * np.abs(mk["R"][o])) / np.sum(w))
    s, es = sigma_side(sg, R, side)
    return dict(R=R, v=v, e=e, side=side, sig=s, esig=es)


def rule_bothsides(mk, sg, drop=None, allow_clipped=False):
    """V-b: |v| on each side interpolated at the SHORTER side's outermost unclipped radius; average."""
    Rs = []
    for side in (+1, -1):
        o = side_pts(mk, side, allow_clipped, drop)
        Rs.append(abs(mk["R"][o[-1]]) if len(o) else np.nan)
    R = float(np.nanmin(Rs))
    v1, e1 = interp_side(mk, +1, R, allow_clipped, drop)
    v2, e2 = interp_side(mk, -1, R, allow_clipped, drop)
    s1, es1 = sigma_side(sg, R, +1)
    s2, es2 = sigma_side(sg, R, -1)
    return dict(R=R, v=0.5 * (v1 + v2), e=0.5 * math.sqrt(e1 ** 2 + e2 ** 2), side=0,
                sig=0.5 * (s1 + s2), esig=0.5 * math.sqrt(es1 ** 2 + es2 ** 2))


def rule_far_at(mk, sg, R, drop=None, side=None):
    """farther side alone, interpolated at radius R."""
    if side is None:
        side, _ = far_side(mk, False, drop)
    o = side_pts(mk, side, False, drop)
    if abs(mk["R"][o[-1]]) + 1e-9 < R:
        return None
    v, e = interp_side(mk, side, R, False, drop)
    s, es = sigma_side(sg, R, side)
    return dict(R=R, v=v, e=e, side=side, sig=s, esig=es)


def rule_both_at(mk, sg, R, drop=None):
    for side in (+1, -1):
        o = side_pts(mk, side, False, drop)
        if len(o) == 0 or abs(mk["R"][o[-1]]) + 1e-9 < R:
            return None
    v1, e1 = interp_side(mk, +1, R, False, drop)
    v2, e2 = interp_side(mk, -1, R, False, drop)
    s1, es1 = sigma_side(sg, R, +1)
    s2, es2 = sigma_side(sg, R, -1)
    return dict(R=R, v=0.5 * (v1 + v2), e=0.5 * math.sqrt(e1 ** 2 + e2 ** 2), side=0,
                sig=0.5 * (s1 + s2), esig=0.5 * math.sqrt(es1 ** 2 + es2 ** 2))


def rule_annulus(mk, sg, flo, weighted=True, drop=None):
    side, Rfar = far_side(mk, False, drop)
    sel = (mk["clip"] == 0) & (np.abs(mk["R"]) >= flo * Rfar) & (np.abs(mk["R"]) <= Rfar + 1e-9)
    if drop is not None:
        sel &= ~drop
    idx = np.where(sel)[0]
    v = np.abs(mk["v"][idx])
    e = mk["e"][idx]
    w = 1.0 / e ** 2
    Rm = float(np.sum(w * np.abs(mk["R"][idx])) / np.sum(w))
    if weighted:
        vm = float(np.sum(w * v) / np.sum(w))
    else:
        vm = float(np.median(v))
    eprop = 1.0 / math.sqrt(np.sum(w))
    sem = float(np.std(v, ddof=1) / math.sqrt(len(v))) if len(v) > 1 else eprop
    s, es = sigma_side(sg, Rm, side)
    return dict(R=Rm, v=vm, e=max(eprop, sem), side=side, sig=s, esig=es)


# ------------------------------------------------------------------------------------------------ sample builder
def subset(S, idx):
    S2 = copy.copy(S)
    n = len(S.ids)
    for k, v in list(S.__dict__.items()):
        if isinstance(v, np.ndarray) and v.ndim == 1 and len(v) == n:
            setattr(S2, k, v[idx])
        elif isinstance(v, list) and len(v) == n:
            setattr(S2, k, [v[i] for i in idx])
    return S2


_BASE = {}


def base_sample(inc_col="inc_sfr_deg", ids=None):
    key = (inc_col, tuple(ids) if ids else None)
    if key not in _BASE:
        _BASE[key] = M.load_kurvs(ids=tuple(ids) if ids else M.KURVS_IDS, inc_col=inc_col)
    return copy.copy(_BASE[key])


def build(rule, ids=None, inc_col="inc_sfr_deg", dep_col=None, vscale=1.0, err_mult=1.0, err_floor=0.0,
          mk=None, sg=None, drops=None, S_base=None, **kw):
    """Build a Sample with the outer point from `rule(mk, sg, **kw)`.
    inc_col: column for the +-5 deg error term and (default) the deprojection; dep_col: deprojection column if different.
    Returns (S, info list) ; discs where the rule returns None are dropped."""
    ids = list(ids) if ids else IDS
    mk = mk or load_markers(ids)
    sg = sg or load_sigma(ids)
    S0 = S_base if S_base is not None else base_sample(inc_col, ids)
    dep = dep_col or inc_col
    I = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_integrated.csv")}
    keep, R, V, eV, sig, esig, info = [], [], [], [], [], [], []
    for j, k in enumerate(S0.ids):
        drop = None if not drops else drops.get(k)
        o = rule(mk[k], sg[k], drop=drop, **kw)
        if o is None:
            continue
        si = 1.0 if dep == "none" else math.sin(math.radians(fnum(I[k][dep])))
        e_obs = o["e"]
        e_obs = math.sqrt((e_obs * err_mult) ** 2 + err_floor ** 2)
        keep.append(j)
        R.append(o["R"]); V.append(o["v"] / si * vscale); eV.append(e_obs / si * vscale)
        sig.append(o["sig"]); esig.append(o["esig"])
        info.append(dict(id=k, R=o["R"], side=o["side"], Vobs=o["v"], V=o["v"] / si, eV=e_obs / si, sig=o["sig"], esig=o["esig"]))
    S = subset(S0, np.array(keep, int))
    S.R = np.array(R); S.V = np.array(V); S.eV = np.array(eV); S.sig = np.array(sig); S.esig = np.array(esig)
    S.grad2 = np.zeros(len(keep))
    return S, info


def mk_err(mk, which):
    """copy of the marker dict with the error taken as the larger / smaller / mean of the two bars."""
    out = {}
    for k, d in mk.items():
        d2 = dict(d)
        d2["e"] = {"max": np.maximum(d["eup"], d["elo"]), "min": np.minimum(d["eup"], d["elo"]), "mean": 0.5 * (d["eup"] + d["elo"])}[which]
        out[k] = d2
    return out


# ------------------------------------------------------------------------------------------------ break-evens
def dprime_mu(S, AS, sp, law, mu):
    r = cells_law(S, AS, sp, law, mu)
    return r["dprime"], r["sigma"]


def cells_law(S, AS, sp, law, mu, gas_scale=2.0):
    if law == "flat":
        return M.cell(S, AS, sp, mu, 0.0, "canonical", gas_scale=gas_scale)["flat"]
    if law == "rival":
        return M.cell(S, AS, sp, mu, 0.0, "canonical", gas_scale=gas_scale)["H"]
    with law_ctx(E_T):
        return M.cell(S, AS, sp, mu, 0.0, "canonical", gas_scale=gas_scale)["H"]


MU_GRID = np.exp(np.linspace(math.log(0.01), math.log(40.0), 48))


def _root(f, grid):
    v = np.array([f(x) for x in grid])
    for i in range(len(grid) - 1):
        if np.isfinite(v[i]) and np.isfinite(v[i + 1]) and v[i] > 0 >= v[i + 1]:
            return float(brentq(f, grid[i], grid[i + 1], xtol=1e-9))
    return None


def break_even(S, AS, sp, law):
    """mu_be with 1-sigma edges (roots of Delta'(mu) = 0, +sigma(mu), -sigma(mu)); None where no root."""
    cache = {}

    def dz(mu):
        if mu not in cache:
            cache[mu] = dprime_mu(S, AS, sp, law, mu)
        return cache[mu]

    f0 = lambda mu: dz(mu)[0]
    fl = lambda mu: dz(mu)[0] - dz(mu)[1]      # Delta' = +sigma : lower mu edge
    fu = lambda mu: dz(mu)[0] + dz(mu)[1]      # Delta' = -sigma : upper mu edge
    c = _root(f0, MU_GRID)
    if c is None:
        return dict(mu=None, lo=None, hi=None, over=(dz(MU_GRID[0])[0] < 0))
    lo = _root(fl, MU_GRID)
    hi = _root(fu, MU_GRID)
    return dict(mu=c, lo=(lo if lo is not None else float(MU_GRID[0])), hi=hi, over=False)


def status(be, ceil=GAS_CEIL):
    if be["mu"] is None:
        return "over"
    return "excluded" if be["lo"] > ceil else "allowed"


def fit_point_s(S, AS, law, mu=DEC_MU):
    """s0 at which Delta'(s, mu) = 0; '<0' if Delta'(0) > 0 already; None if >6."""
    f = lambda s: cells_law(S, AS, spec_s(s), law, mu)["dprime"]
    if f(0.0) > 0:
        return "<0"
    hi = 6.0
    if f(hi) < 0:
        return None
    return float(brentq(f, 0.0, hi, xtol=1e-8))


def z_at(S, AS, s, law, mu=DEC_MU):
    r = cells_law(S, AS, spec_s(s), law, mu)
    return r["z"], r["dprime"], r["sigma"]


def crossings(S, AS, mu=DEC_MU):
    """s_mid: Delta'_flat + Delta'_H = 0 (the data midway between the laws; this reproduces CFG162/168's 0.669 -- my frozen text said "Delta'_flat = Delta'_H", which has no root: a wording slip of mine, kept; the z_flat + z_H = 0 reading gives 0.665) ; s_f2: z_flat = +2 ; s_h2: z_H = -2 (root-found in s on [0, 6])."""
    def zz(s):
        r = M.cell(S, AS, spec_s(s), mu, 0.0, "canonical")
        return r["flat"]["z"], r["H"]["z"], r["flat"]["dprime"] + r["H"]["dprime"]
    out = {}
    for name, fn in (("s_mid", lambda s: zz(s)[2]), ("s_f2", lambda s: zz(s)[0] - 2.0), ("s_h2", lambda s: zz(s)[1] + 2.0)):
        try:
            g = np.linspace(0.0, 6.0, 61)
            v = [fn(x) for x in g]
            r = None
            for i in range(len(g) - 1):
                if v[i] < 0 <= v[i + 1]:
                    r = float(brentq(fn, g[i], g[i + 1], xtol=1e-9))
                    break
            out[name] = r
        except Exception:
            out[name] = None
    return out


def headline_label(model_cells, meas_cells):
    cls_m = M.classify(model_cells["flat"]["z"], model_cells["rival"]["z"])
    cls_p = M.classify(meas_cells["flat"]["z"], meas_cells["rival"]["z"])
    dz = {l: meas_cells[l]["z"] - model_cells[l]["z"] for l in LAWS}
    unchanged = (cls_m == "lean rival") and (cls_p == cls_m) and all(abs(v) < 1.0 for v in dz.values())
    return ("UNCHANGED" if unchanged else "CHANGED"), cls_m, cls_p, dz


def classes(cells):
    return M.classify(cells["flat"]["z"], cells["rival"]["z"])


def fmt_cells(c):
    return " | ".join(f"{l}: {c[l]['dprime']:+.4f} +- {c[l]['sigma']:.4f} ({c[l]['z']:+.2f})" for l in LAWS) + f" | {classes(c)}"


def jdefault(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)
