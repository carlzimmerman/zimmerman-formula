#!/usr/bin/env python3
"""SY1 data: BF1's loading and split, read from ../BF1_exhaustive_law_search/bf1.py and not edited; BF1's LITTLE THINGS and Saturn rows. Adds s, D and SPARC's velocity errors. kappa = 1/2 FITTED; not theory closed."""
import hashlib, os, pickle, sys
import numpy as np
from sy1_leaves import *
HERE = os.path.dirname(os.path.abspath(__file__)); BF = os.path.join(os.path.dirname(HERE), "BF1_exhaustive_law_search", "bf1.py")
_src = open(BF).read(); BF1_SHA = hashlib.sha256(_src.encode()).hexdigest()[:16]; _a = sys.argv; sys.argv = ["bf1", "real"]; _B = {"__file__": os.path.join(HERE, "bf1.py"), "__name__": "bf1_head"}
exec(compile(_src.split("rng = np.random.default_rng(20261102)")[0], BF, "exec"), _B); sys.argv = _a
XT, XH, ST, SH, law = _B["XT"], _B["XH"], _B["ST"], _B["SH"], _B["law"]; A0 = _B["A0"]; G = _B["G"]; MS = _B["MS"]; RB = _B["RB"]; XM0, XR0, SF, SM = 0.05, 0.10, _B["SF"], _B["SM"]; ALT = 1.1312e-10
assert A0 == A0C
def _cols(A):
    """Leaves per row; s by system (column 4), so galaxies don't merge."""
    gb, ell, f, idx = A[:, 0], A[:, 2], A[:, 3], A[:, 4]; s = np.empty(len(A))
    for k in np.unique(idx):
        m = idx == k; s[m] = slope_1d(gb[m], ell[m])
    y = gb / A0C; return dict(y=y, ell=ell, f=f, s=s, D=D_leaf(y, s, ell))
def lt_rows():
    C_ = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb")); K = 3.0857e19; LT = []
    for i, g in enumerate(C_["lt"]):
        M = 10 ** g["logMb"]; R = g["R"] * K; LT.append((G * M * MS / R ** 2, (g["V"] * 1e3) ** 2 / R, R * A0 / CL ** 2, max(0, 1 - g["Mstar"] / M), i))
    return np.array(LT)
def sparc_err(par):
    """log10 g error per row, 2 eV/(V ln 10), same filter and order as BF1's sparc()."""
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"]; meta = {g["name"]: g for g in Q}; out = []; D = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod")
    for i, n in enumerate(sorted(meta)):
        if meta[n]["Q"] >= 3 or meta[n]["inc"] < 30 or i % 2 != par: continue
        for r, v, e, vg, vd, vb, *_ in np.atleast_2d(np.loadtxt(os.path.join(D, n + "_rotmod.dat"), comments="#")):
            m = abs(vg) * vg + 0.5 * abs(vd) * vd + 0.7 * abs(vb) * vb
            if r <= 0 or v <= 0 or m <= 0: continue
            out.append(2 * e / (v * np.log(10)))
    return np.array(out)
# Planted forms: wrapper, expression in the search's own grammar, arms
PLANT = dict(P1=(3, "(one + f) * log1p(one / y)", "TZ"), P2=(1, "one + 2.7 * f * inv1p(0.6 * square(s))", "T"), P3=(2, "one + inv1p(square(s)) * log1p(D)", "Z"))
SCR_SEED = 20261102
def scramble_y(c, nx):
    """y shuffled within class, D recomputed from the shuffled y so it can't hand y back. s, ell, f untouched."""
    r = np.random.default_rng(SCR_SEED); c = dict(c); y = c["y"].copy(); y[:nx] = y[:nx][r.permutation(nx)]; y[nx:] = y[nx:][r.permutation(len(y) - nx)]; c["y"] = y; c["D"] = D_leaf(y, c["s"], c["ell"]); return c
def planted_truth(tag, A):
    w, ex, _ = PLANT[tag]; return wrap(w, A[:, 0], A0C, eval_H(ex, _cols(A)))
def build(mode, tag=None):
    """Train arrays: X-COP rows first. Returns X (features), target log10(g_obs/a0), true y (the wrapper's g_b/a0), NX."""
    nx = len(XT); A = np.vstack([XT, ST]); c = {k: np.r_[_cols(XT)[k], _cols(ST)[k]] for k in LEAVES}; gobs = A[:, 1].copy(); ytrue = A[:, 0] / A0C
    if mode == "scrambled": c = scramble_y(c, nx)
    if mode == "planted":
        p, nn = tag.split("N"); gobs = np.r_[planted_truth(p, XT), planted_truth(p, ST)]
        if nn == "1":
            e = sparc_err(1); assert len(e) == len(ST); r = np.random.default_rng(20261103 + int(p[1])); gobs[nx:] = gobs[nx:] * 10 ** (e * r.standard_normal(len(e)))
    X = np.column_stack([c[k] for k in LEAVES] + [np.full(len(A), v) for v in CONSTS.values()]); assert np.all(np.isfinite(X))
    return X, np.log10(gobs / A0C), ytrue, nx
