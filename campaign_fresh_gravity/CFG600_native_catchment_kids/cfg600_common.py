"""Shared harness for CFG600 / CFG601: CFG531's cfg531_kids.py executed read-only up to `EARLY = TYP == 1` (CFG529 data + f30-matched
environment, constructions A/B, cached law tables), then node-own-profile helpers.  Nothing here is a result."""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
P531 = os.path.join(LANES, "CFG531_inner_halo_shortfall", "cfg531_kids.py")
_src = open(P531).read()
_cut = _src.index("EARLY = TYP == 1")
NS = {"__file__": P531, "__name__": "cfg531_ro"}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_src[:_cut], "cfg531_kids", "exec"), NS)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
g = NS
GP, F30, TYP, hart, BANDS, MEAS = g["GP"], g["F30"], g["TYP"], g["hart"], g["BANDS"], g["MEAS"]
CONS, FOOTS, SHMRS, T29 = g["CONS"], g["FOOTS"], g["SHMRS"], g["T29"]
evec, edge_tabs, fo_of, gstack, esd_loo, fit_eps, all_bands, comps = (g[k] for k in ("evec", "edge_tabs", "fo_of", "gstack", "esd_loo", "fit_eps", "all_bands", "comps"))
NPATCH = g["NPATCH"]
NODES = np.asarray(T29["XN"])
SEL = [j for j, x in enumerate(NODES) if x >= 0.2 - 1e-12]
EARLY = TYP == 1
_tag = [0]


def Egrid(c, mask_unused, fE, tag):
    """per-group E grid per SHMR for leaked fractions fE (dict s -> grid)."""
    _tag[0] += 1
    return {s: evec(GP, c, s, "W30", fE[s], f"cfg600|{tag}|{_tag[0]}") for s in SHMRS}


def node_own(c, foot, s, j, fO):
    fo = fo_of(fO[s])
    full, tr = edge_tabs(c, foot, "node", j, s, "W30")
    v = (1 - fo) * full + fo * tr
    return np.where(np.isfinite(v), v, 0.0)


def full_own(c, foot, s, j):
    full, tr = edge_tabs(c, foot, "node", j, s, "W30")
    return np.where(np.isfinite(full), full, 0.0)


def cp_node(c, foot, mask, j, fE, fO, Eg=None, tag="n"):
    Eg = Egrid(c, mask, fE, tag) if Eg is None else Eg
    return {s: (gstack(Eg[s], mask), gstack(node_own(c, foot, s, j, fO), mask)) for s in SHMRS}


def cp_census(c, foot, mask, fE, fO, Eg=None, tag="c"):
    Eg = Egrid(c, mask, fE, tag) if Eg is None else Eg
    return {s: (gstack(Eg[s], mask), gstack(g["census_own"](c, foot, s, fO), mask)) for s in SHMRS}


def chi2_bins(d, Cv, cp, idx, delta=True, shmr="moster"):
    idx = np.asarray(idx)
    Em, om = cp["moster"]; Eb, ob = cp["behroozi"]
    mM = Em + om
    mB = Eb + ob
    m = mM if shmr == "moster" else mB
    dl = (mB - mM) if delta else np.zeros_like(mM)
    Ct = Cv[np.ix_(idx, idx)] / hart(len(idx)) + np.outer(dl[idx], dl[idx])
    r = d[idx] - m[idx]
    c2 = float(r @ np.linalg.solve(Ct, r))
    return c2


OUTER = list(range(0, 6)); INNER = list(range(6, 15))


def calibrate(d, Cv, c, foot, mask, fE, fO, Eg, bins=OUTER, dat=None):
    """x* = node minimising chi2 (eps = 0) over `bins`; returns (jbest, chi2 list over SEL)."""
    dd = d if dat is None else dat
    curve = []
    for j in SEL:
        cp = cp_node(c, foot, mask, j, fE, fO, Eg)
        curve.append(chi2_bins(dd, Cv, cp, bins))
    return SEL[int(np.argmin(curve))], curve
