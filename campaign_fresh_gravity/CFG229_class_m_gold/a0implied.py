#!/usr/bin/env python3
"""Shared implied-a0 machinery for CFG229 and CFG228: the estimator of CFG223 (`cfg223_a0_over_time.py`, functions `nuv` and `implied`) COPIED VERBATIM, plus the kernel lever of
`cfg223_lever.py`.  The copy is checked against the original by control C10 of cfg229_preflight.py (bit-equal on 200 random sets).
Descriptive, not a verdict.  LambdaCDM has no a0.  kappa = 1/2 FITTED."""
import numpy as np

LO_LS, HI_LS, NIT = -3.0, 3.0, 64


def nuv(nu, y):
    y = np.asarray(y, float)
    return nu(y.ravel()).reshape(y.shape)


def implied(D, gb, nu, a0):
    """log10 s* for each row-set: the root of median_i log10[D_i / nu(gb_i / (a0 s))] = 0 on log10 s in [-3, 3] (vectorised bisection; the median of the
    non-increasing deltas is non-increasing in s).  D, gb: (n,) or (B, n).  Returns (log10 s*, UNBOUNDED flag) per row-set."""
    D = np.atleast_2d(np.asarray(D, float)); gb = np.atleast_2d(np.asarray(gb, float))
    logD = np.log10(D)
    Bn = D.shape[0]

    def f(ls):
        return np.median(logD - np.log10(nuv(nu, gb / (a0 * 10.0 ** ls[:, None]))), axis=1)
    a = np.full(Bn, LO_LS); b = np.full(Bn, HI_LS)
    unb = ~((f(a) > 0) & (f(b) < 0))
    for _ in range(NIT):
        m = 0.5 * (a + b)
        pos = f(m) > 0
        a = np.where(pos, m, a); b = np.where(pos, b, m)
    return 0.5 * (a + b), unb


def lever(D, gb, nu, a0, h=0.03):
    """d log10 s* / d(baryon dex) of a set: ALL baryon masses move by +-h dex (g_bar x 10^(+-h), D x 10^(-+h) at fixed g_obs), as cfg223_lever.py.  Returns (lever, flag)."""
    lp, up = implied(np.asarray(D) * 10 ** (-h), np.asarray(gb) * 10 ** h, nu, a0)
    lm, um = implied(np.asarray(D) * 10 ** h, np.asarray(gb) * 10 ** (-h), nu, a0)
    return (lp - lm) / (2 * h), (up | um)


def kernel_slope(nu, y, h=0.02):
    """-d log10 nu / d log10 y at y (the local slope of the kernel), as cfg223_lever.py"""
    y = np.asarray(y, float)
    return -(np.log10(nuv(nu, y * 10 ** h)) - np.log10(nuv(nu, y * 10 ** (-h)))) / (2 * h)
