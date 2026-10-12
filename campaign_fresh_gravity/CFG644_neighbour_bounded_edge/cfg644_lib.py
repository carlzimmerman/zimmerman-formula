#!/usr/bin/env python3
"""CFG644 library (FROZEN_CRITERIA.md, criteria 6a03c0870): candidate-B profiles of point bodies and the neighbour-bounded
radius r_nb (pairwise closed-basin watershed; bracket S = summed collinear pulls).  Nothing here is a result.

Units: any consistent set (G, a0, M, r).  Kernel: cfg100_lib nu_mono (read-only), the KiDS harness kernel.
"""
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
for _p in ("CFG100_kids_mass_rederivation", "CFG515_census_edge_resolution"):
    sys.path.insert(0, os.path.join(LANES, _p))
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg515_lib as L                                                       # noqa: E402  (read-only)

COLD = L.COLD_PER_B                                                          # 5.364
nu = C.nu_mono

# census f_ret on a fine log grid (fret_census is a monotone-step root; the grid is checked against direct calls by the scripts)
_LMB = np.linspace(6.0, 14.5, 3401)
_FR = np.array([L.fret_census(10 ** x)[0] for x in _LMB])


def fret(Mb):
    return np.interp(np.log10(np.maximum(np.asarray(Mb, float), 1e6)), _LMB, _FR)


def supply(Mb):
    return COLD * np.asarray(Mb, float) / fret(Mb)


def mtot(Mb):
    return np.asarray(Mb, float) + supply(Mb)


def MB(Mb, r, G, a0, S=None):
    """candidate-B enclosed mass of a point body: M_b + min(M_b (nu - 1), S)."""
    Mb = np.asarray(Mb, float); r = np.maximum(np.asarray(r, float), 1e-30)
    S = supply(Mb) if S is None else S
    ph = Mb * (nu(G * Mb / (r * r * a0)) - 1.0)
    return Mb + np.minimum(ph, S)


def phantom(Mb, r, G, a0):
    r = np.maximum(np.asarray(r, float), 1e-30)
    return np.asarray(Mb, float) * (nu(G * np.asarray(Mb, float) / (r * r * a0)) - 1.0)


def r_edge(Mb, G, a0):
    """census edge (CFG515 closed form, = the numeric nu_mono root to 5e-9 per CFG515 K1)."""
    Mb = np.asarray(Mb, float)
    return np.sqrt(G * Mb / a0) / np.log1p(fret(Mb) * L.FB / (1.0 - L.FB))


def r_pair(Mo, Mj, D, G, a0, n_iter=60, gfun_o=None):
    """pairwise equal-pull radius: g_o(r) = g_j(D - r), 0 < r < D (vectorised bisection in t = r/D).
    gfun_o(r) optionally replaces the own point-body B pull (used for the MW Prof)."""
    Mo, Mj, D = np.broadcast_arrays(np.asarray(Mo, float), np.asarray(Mj, float), np.asarray(D, float))
    lo = np.zeros(D.shape); hi = np.ones(D.shape)
    So, Sj = supply(Mo), supply(Mj)
    for _ in range(n_iter):
        t = 0.5 * (lo + hi); r = t * D; d = (1 - t) * D
        go = gfun_o(r) if gfun_o is not None else G * MB(Mo, r, G, a0, So) / r ** 2
        gj = G * MB(Mj, d, G, a0, Sj) / d ** 2
        pos = go > gj
        lo = np.where(pos, t, lo); hi = np.where(pos, hi, t)
    return 0.5 * (lo + hi) * D


def r_nb_pairwise(Mo, Mj, D, G, a0, gfun_o=None, Mtot_o=None):
    """r_nb of one body from arrays of neighbours (masses Mj, separations D): min over CLOSING neighbours (M_tot,j >= M_tot,o)."""
    Mj = np.atleast_1d(np.asarray(Mj, float)); D = np.atleast_1d(np.asarray(D, float))
    To = mtot(Mo) if Mtot_o is None else Mtot_o
    k = mtot(Mj) >= To
    if not k.any():
        return np.inf
    return float(np.min(r_pair(np.full(k.sum(), Mo), Mj[k], D[k], G, a0, gfun_o=gfun_o)))


def r_nb_summed(Mo, Mj, D, G, a0, gfun_o=None, Mtot_o=None, n_iter=60):
    """bracket S: g_o(r) = sum_j g_j(D_j - r) over every neighbour, applied if sum M_tot,j >= M_tot,o; root in (0, min D)."""
    Mj = np.atleast_1d(np.asarray(Mj, float)); D = np.atleast_1d(np.asarray(D, float))
    To = mtot(Mo) if Mtot_o is None else Mtot_o
    if len(Mj) == 0 or mtot(Mj).sum() < To:
        return np.inf
    Dm = D.min(); Sj = supply(Mj); lo, hi = 0.0, 1.0
    for _ in range(n_iter):
        t = 0.5 * (lo + hi); r = t * Dm
        go = float(gfun_o(np.array([r]))[0]) if gfun_o is not None else float(G * MB(Mo, r, G, a0) / r ** 2)
        d = D - r
        gs = float(np.sum(G * MB(Mj, d, G, a0, Sj) / d ** 2))
        if go > gs:
            lo = t
        else:
            hi = t
    return 0.5 * (lo + hi) * Dm


def segmented_r_nb(Mo, To, seg, Mj, D, G, a0, n_iter=60):
    """vectorised pairwise r_nb for many owners: seg = owner index per pair. Returns r_nb per owner (inf if no closing pair)."""
    n = len(Mo); out = np.full(n, np.inf)
    k = mtot(Mj) >= To[seg]
    if k.any():
        r = r_pair(Mo[seg[k]], Mj[k], D[k], G, a0, n_iter=n_iter)
        np.minimum.at(out, seg[k], r)
    return out


def segmented_r_nb_summed(Mo, To, seg, Mj, D, G, a0, n_iter=60):
    """vectorised bracket S for many owners (collinear summed pulls, collective closure)."""
    n = len(Mo); out = np.full(n, np.inf)
    if len(seg) == 0:
        return out
    Tj = mtot(Mj)
    close = np.bincount(seg, weights=Tj, minlength=n) >= To
    Dmin = np.full(n, np.inf); np.minimum.at(Dmin, seg, D)
    own = np.nonzero(close & np.isfinite(Dmin))[0]
    if not len(own):
        return out
    sel = np.isin(seg, own)
    sg, Mjs, Ds = seg[sel], Mj[sel], D[sel]
    Sj = supply(Mjs); So = supply(Mo)
    lo = np.zeros(n); hi = np.ones(n)
    for _ in range(n_iter):
        t = 0.5 * (lo + hi); r = t * Dmin
        go = np.where(np.isfinite(r), G * MB(Mo, np.where(np.isfinite(r), r, 1.0), G, a0, So) / np.where(np.isfinite(r), r, 1.0) ** 2, 0.0)
        d = Ds - r[sg]
        gs = np.bincount(sg, weights=G * MB(Mjs, d, G, a0, Sj) / np.maximum(d, 1e-30) ** 2, minlength=n)
        pos = go > gs
        lo = np.where(pos, t, lo); hi = np.where(pos, hi, t)
    out[own] = (0.5 * (lo + hi) * Dmin)[own]
    return out
