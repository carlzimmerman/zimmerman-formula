#!/usr/bin/env python3
"""CFG679D common pieces: the law's own ESD (LAW_RTA 'full', cfg100_lib read-only, = CFG503's kids_Md / kids_fin path), lens groups
(CFG503's grouping), stacking, the GLS amplitude eps with E = 0 (framework-native: no environment term, no stripping), bands.
"""
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
import cfg100_lib as C                                                       # noqa: E402  (read-only)

FOOTS = ("canonical", "alt")
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2          # CFG529's conversion of the stacked sums to Msun/pc^2
BANDS = {"K-in": [12, 13, 14], "K-mid": [9, 10, 11], "K-out": [6, 7, 8], "K9": list(range(6, 15))}
GEDGE_SI = C.GEDGE                            # m/s^2, 16 edges (CFG96 gbar_edges)


def fcold(logMs):
    return 10 ** (-0.69 * logMs + 6.63)


def mgal(logMs):
    """the record's baryon convention (CFG96 stage): M_gal = M* (1 + f_cold), f_cold = 10^(-0.69 log M* + 6.63)."""
    return 10 ** logMs * (1 + fcold(logMs))


def groups(z, Mgal):
    """CFG503 grouping: 0.01 dex in log M_gal x 0.03 in z."""
    lmg = np.log10(Mgal)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
    gi = gi.ravel()
    return gi, 10 ** (np.bincount(gi, weights=lmg) / cnt), np.bincount(gi, weights=z) / cnt


def own_law_rta(Mg, zl, foot, scale_a0=1.0):
    """LAW_RTA 'full' own ESD in the 15 g_bar bins [Msun/pc^2] for baryon point mass Mg at zl (CFG503 kids_Md + kids_fin)."""
    a0 = C.A0[foot] * scale_a0
    rta = C.r_ta_law(Mg, a0, zl)
    r = np.geomspace(1e-4, rta, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


def own_newton(Mg):
    """baryon point mass only (MUTATE tooth: the Newtonian own profile)."""
    return C._finish(lambda R: Mg / (math.pi * R ** 2) + 0 * R, Mg)


def own_table(GM, GZ, foot, fn=own_law_rta):
    return np.array([fn(m, z, foot) for m, z in zip(GM, GZ)])


def stack(tab, gi, WW, wl=None):
    """stack-weighted group average per bin: sum_lens w_l WW[l,k] own[g(l),k] / sum_lens w_l WW[l,k]."""
    w8 = WW if wl is None else WW * wl[:, None]
    out = np.zeros(15)
    ng = tab.shape[0]
    for k in range(15):
        w = np.bincount(gi, weights=w8[:, k], minlength=ng)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


def esd_jk(WG, WW, patch, wl=None, npatch=NPATCH):
    """stacked ESD [Msun/pc^2] and the patch leave-one-out jackknife covariance (CFG529 esd_full_loo)."""
    if wl is not None:
        WG = WG * wl[:, None]; WW = WW * wl[:, None]
    wg = np.zeros((npatch, 15)); w = np.zeros((npatch, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch, weights=WG[:, k], minlength=npatch)
        w[:, k] = np.bincount(patch, weights=WW[:, k], minlength=npatch)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG
    loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (npatch - 1) / npatch * dev.T @ dev, loo


def hart(p, npatch=NPATCH):
    return (npatch - p - 2) / (npatch - 1)


def eps_band(d, Cv, o, idx, npatch=NPATCH):
    """GLS amplitude eps = o^T W r / o^T W o, r = d - o, W = (C_band / hart)^-1; sigma = (o^T W o)^-1/2."""
    idx = list(idx)
    W = np.linalg.inv(Cv[np.ix_(idx, idx)] / hart(len(idx), npatch))
    oo, rr = o[idx], (d - o)[idx]
    F = float(oo @ W @ oo)
    e = float(oo @ W @ rr) / F
    s = F ** -0.5
    return dict(eps=e, sig=s, Z=e / s)


def eps_loo(loo, o, idx):
    """eps per leave-one-out realisation with the full-sample-weights fixed (for a jackknife of a difference)."""
    idx = list(idx)
    return np.array([float(o[idx] @ (l[idx] - o[idx])) / float(o[idx] @ o[idx]) for l in loo])


def bin_radii(Mgal, WW):
    """stack-weighted mean R [kpc] per g_bar bin (CFG529 RmA rule)."""
    gc = np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])
    return 1e3 * (WW * np.sqrt(C.G_MPC * Mgal[:, None] / gc[None, :])).sum(0) / WW.sum(0)
