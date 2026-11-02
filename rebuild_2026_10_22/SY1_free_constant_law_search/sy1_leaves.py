#!/usr/bin/env python3
"""SY1 leaves and wrappers: one formula for every system, no class input. Pure functions, no data. See FROZEN_CRITERIA.md, AMENDMENT_A2.md. kappa = 1/2 FITTED; not theory closed."""
import re
import numpy as np
A0C = 9.360324825027975e-11; CL = 299792458.0
LEAVES = ("y", "ell", "f", "s", "D"); CONSTS = dict(one=1.0, two=2.0, half=0.5, pi_=np.pi); FEATURES = LEAVES + tuple(CONSTS)
def inv1p(x): return 1.0 / (1.0 + x)
def square(x): return x * x
OPS = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=inv1p, square=square, safe_sqrt=np.sqrt, safe_log1p=np.log1p)
NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*"); NUM = re.compile(r"(?<![A-Za-z_0-9.])\d+\.?\d*(?:[eE][-+]?\d+)?")
def reads(expr): return {n for n in NAME.findall(re.sub(r"\d+\.?\d*[eE][-+]?\d+", "0", expr))} & set(LEAVES)
def n_floats(expr): return len(NUM.findall(expr))
def slope_1d(gb, r):
    """s = dlog g_b/dlog r along strictly increasing runs of r; a run of one point is a point system, s = -2. r non-finite: not computable, NaN."""
    gb = np.asarray(gb, float); r = np.asarray(r, float); s = np.full(gb.shape, -2.0)
    if not np.all(np.isfinite(r)): return s * np.nan
    i = np.nonzero(gb > 0)[0]
    if len(i) < 2: return s
    cut = np.nonzero(np.diff(r[i]) <= 0)[0] + 1
    for run in np.split(i, cut):
        if len(run) >= 2: s[run] = np.gradient(np.log(gb[run]), np.log(r[run]))
    return s
def slope(gb, r):
    gb = np.asarray(gb, float); r = np.broadcast_to(np.asarray(r, float), gb.shape)
    if gb.ndim <= 1: return slope_1d(np.atleast_1d(gb), np.atleast_1d(r)).reshape(gb.shape)
    sh = gb.shape; G = gb.reshape(-1, sh[-1]); R = r.reshape(-1, sh[-1]); return np.array([slope_1d(a, b) for a, b in zip(G, R)]).reshape(sh)
def D_leaf(y, s, ell):
    """rho_b/rho_DE: rho_b = g_b (2 + s)/(4 pi G r), rho_DE = 4 a0^2/(c^2 G) from a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Floor at 0: enclosed mass can't fall."""
    return np.maximum(2.0 + s, 0.0) * y / (16.0 * np.pi * ell)
def eval_H(expr, L):
    e = dict(OPS); e.update(CONSTS); e.update(L)
    with np.errstate(all="ignore"): return eval(expr, {"__builtins__": {}}, e)
def wrap(w, gb, a, H):
    with np.errstate(all="ignore"):
        if w == 1: return 0.5 * gb + np.sqrt(0.25 * gb * gb + a * H * gb)
        if w == 2: x = gb * H; return 0.5 * x + np.sqrt(0.25 * x * x + a * x)
        if w == 3: return (0.5 * gb + np.sqrt(0.25 * gb * gb + a * gb)) * H
    raise ValueError(w)
def g_of_Q(expr, w, Q):
    """Candidate g for RQ3: leaves at a0 canonical on every footing, the wrapper at the footing's a0. Reads gg, r only if the expression does; never a label. Non-finite or non-positive H on a real point returns NaN, so RQ3 reads NOT COMPUTABLE."""
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; need = reads(expr); L = {}; pos = gb > 0; safe = np.where(pos, gb, 1.0)
    L["y"] = safe / A0C
    if "f" in need:
        with np.errstate(all="ignore"): L["f"] = np.clip(np.asarray(Q["gg"], float) / safe, 0.0, 1.0)
    if need & {"ell", "s", "D"}:
        r = np.broadcast_to(np.asarray(Q["r"], float), gb.shape); L["ell"] = r * A0C / CL ** 2
        if need & {"s", "D"}: L["s"] = slope(gb, r); L["D"] = D_leaf(L["y"], L["s"], L["ell"])
    H = np.broadcast_to(eval_H(expr, L), gb.shape); bad = pos & (~np.isfinite(H) | (H <= 0))
    v = np.where(pos, wrap(w, safe, a, np.where(pos, H, 1.0)), gb)
    return np.where(bad, np.nan, v)
