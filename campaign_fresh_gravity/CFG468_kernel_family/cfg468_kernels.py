#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG468 kernels -- the frozen kernel family (FROZEN_CRITERIA.md, b0d7274a0), in two forms:

  (a) PHYSICAL nu(y), y = g_N / a0, for the SPARC arm:  NU[id](y) -> nu;  IF[id](g_bar, a0) = g_bar nu(g_bar/a0).
  (b) ENGINE ADAPTERS for the CFG321/CFG358 zero-field engine (cfg468_engine.py, byte-identical, not edited): objects with
      CT(yhat), CL(yhat), Q(yhat) in the engine's normalisation, with ONE physical unit for every kernel:
          yhat = y / y*_ref,   y*_ref = log1p(1/C*)^2,   C* = (2 - alpha_c)/alpha_c   (nu_mono's y*, the engine's own)
          C_T(yhat) = (nu(y) - 1)/C*,   C_L(yhat) = d[y (nu - 1)]/dy / C*,   Q(yhat) = 2 Int_0^yhat s C_T(s) ds.
      For nu_mono this IS the engine's NuMonoKernel (control C0).

Deep-kernel form used by the adapters: with v = sqrt(y) = sqrt(y*_ref) sqrt(yhat) and f(v) = v (nu(v^2) - 1) (f -> 1 as v -> 0 for
every kernel obeying (ii)), h(v) = f + v f':
      C_T = yhat^-1/2 f(v) / (C* sqrt y*),   C_L = yhat^-1/2 h(v) / (2 C* sqrt y*),
      Q   = (4 / (C* y*^2)) Int_0^V v^2 f(v) dv,   V = sqrt(y* yhat)        (Gauss-Legendre, piecewise at kinks).
Nothing here is a result.
"""
import math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG5_common as C5                       # the record's nu_mono (XC4), imported read-only (control C-K)

ALPHA_C = 3.2e-9                               # L340 P1 alpha_c maximum (read and checked by the drivers)
CSTAR = (2.0 - ALPHA_C) / ALPHA_C
YSTAR = math.log1p(1.0 / CSTAR) ** 2           # 2.56e-18: the engine's unit of field, the same for every kernel
SY = math.sqrt(YSTAR)

Y_S1 = 0.1 * YSTAR                             # S1 splice point (engine scale), frozen
Y_S2 = 1e-8                                    # S2 splice point (below the KiDS lensing floor), frozen
V_A, V_B = math.sqrt(0.1 * YSTAR), math.sqrt(0.4 * YSTAR)   # MUTATE kinks inside the engine range (v_b = 2 v_a)
KNOTS_V = np.array([0.1, 0.3, 1.0, 3.0, 10.0])               # MUTATE kinks in the observable range

_GL_X, _GL_W = np.polynomial.legendre.leggauss(10)


# ====================================================================================================== physical nu(y)
def nu_mono(y):
    return C5.nu_mono(np.asarray(y, float))


def nu_rar(y):
    y = np.asarray(y, float)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_simple(y):                              # nu_1
    y = np.asarray(y, float)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_standard(y):                            # nu_2 = [1/2 + sqrt(1/4 + y^-2)]^(1/2) = y^-1/2 exp(asinh(y/2)/2)
    y = np.asarray(y, float)
    return np.exp(0.5 * np.arcsinh(0.5 * y)) / np.sqrt(y)


def nu_n(y, n):                                # the nu_n family, direct form (cross-check of nu_simple / nu_standard)
    y = np.asarray(y, float)
    return (0.5 + np.sqrt(0.25 + y ** (-float(n)))) ** (1.0 / n)


def nu_p2(y):                                  # sqrt(1 + 1/y): the record's earlier kernel (lane V 'alpha1')
    y = np.asarray(y, float)
    return np.sqrt(1.0 + 1.0 / y)


def _p_rar_derivs(ys):
    """p = nu_RAR - 1 = 1/expm1(sqrt y) and its first two y-derivatives at ys, to 40 digits (mpmath)."""
    import mpmath as mp
    mp.mp.dps = 60
    p = lambda t: 1 / mp.expm1(mp.sqrt(t))
    y = mp.mpf(ys)
    return float(p(y)), float(mp.diff(p, y, 1)), float(mp.diff(p, y, 2))


def splice_coeffs(ys):
    """(a, b, c): p(y) = ys^-1/2 (a + b u^2 + c u^4), u = y/ys, matching p, p', p'' of nu_mono (= nu_RAR there) at ys (C^2)."""
    p0, p1, p2 = _p_rar_derivs(ys)
    s = math.sqrt(ys)
    P0, P1, P2 = s * p0, s * ys * p1, s * ys * ys * p2
    c = (P2 - P1) / 8.0
    b = (P1 - 4.0 * c) / 2.0
    a = P0 - b - c
    return a, b, c


SPL = {"S1": (Y_S1, splice_coeffs(Y_S1)), "S2": (Y_S2, splice_coeffs(Y_S2))}


def make_nu_splice(tag):
    ys, (a, b, c) = SPL[tag]

    def nu(y):
        y = np.asarray(y, float)
        u = y / ys
        lo = 1.0 + (a + b * u * u + c * u ** 4) / math.sqrt(ys)
        with np.errstate(all="ignore"):
            hi = nu_mono(np.maximum(y, ys))
        return np.where(y < ys, lo, hi)
    return nu


nu_S1 = make_nu_splice("S1")
nu_S2 = make_nu_splice("S2")


def q_mutate(v):
    """1/nu for the MUTATE kernel: piecewise linear in v = sqrt(y) (frozen definition)."""
    v = np.asarray(v, float)
    D = np.where(v < V_A, 0.0, np.where(v < V_B, 0.5 * (v - V_A), 0.5 * (V_B - V_A)))
    qm = -np.expm1(-v)
    kv = KNOTS_V
    kq = np.concatenate([-np.expm1(-kv[:-1]) + 0.5 * (V_B - V_A), [1.0]])
    lin = np.interp(v, kv, kq)
    return np.where(v < 0.1, qm + D, np.where(v < 10.0, lin, 1.0))


def nu_mutate(y):
    return 1.0 / q_mutate(np.sqrt(np.asarray(y, float)))


NU = {"nu_mono": nu_mono, "nu_simple": nu_simple, "nu_standard": nu_standard, "S1": nu_S1, "S2": nu_S2,
      "MUTATE_kink": nu_mutate, "nu_rar": nu_rar, "nu_p2": nu_p2}
LIMITS_II = {"nu_mono": "exact", "nu_simple": "exact", "nu_standard": "exact", "S1": f"operational (y >= {Y_S1:.3g})",
             "S2": f"operational (y >= {Y_S2:.3g})", "MUTATE_kink": "exact", "nu_rar": "exact", "nu_p2": "exact"}


def make_IF(nu):
    def IF(gb, a0):
        return gb * nu(gb / a0)
    return IF


# ====================================================================================================== engine adapters
def _gl(fun, lo, hi):
    """vectorised Gauss-Legendre of fun on [lo, hi] (arrays), 10 nodes"""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    m = 0.5 * (hi + lo); r = 0.5 * (hi - lo)
    x = m[..., None] + r[..., None] * _GL_X
    return r * np.sum(_GL_W * fun(x), axis=-1)


class DeepKernel:
    """Engine adapter from f(v) = v (nu(v^2) - 1) and h(v) = f + v f' (one smooth piece on the engine range)."""

    def __init__(self, name, f, h, kinks=()):
        self.name, self.f, self.h = name, f, h
        self.kinks = tuple(sorted(kinks))
        self.alpha = ALPHA_C

    def CT(self, yh):
        yh = np.maximum(np.asarray(yh, float), 1e-300)
        v = SY * np.sqrt(yh)
        return self.f(v) / (CSTAR * SY * np.sqrt(yh))

    def CL(self, yh):
        yh = np.maximum(np.asarray(yh, float), 1e-300)
        v = SY * np.sqrt(yh)
        return self.h(v) / (2.0 * CSTAR * SY * np.sqrt(yh))

    def _I(self, V):
        """Int_0^V v^2 f(v) dv, piecewise at the kinks"""
        g = lambda x: x * x * self.f(x)
        edges = (0.0,) + self.kinks
        tot = np.zeros_like(V)
        for i, lo in enumerate(edges):
            hi = edges[i + 1] if i + 1 < len(edges) else np.inf
            top = np.minimum(V, hi)
            sel = top > lo
            if np.any(sel):
                tot[sel] += _gl(g, np.full(sel.sum(), lo), top[sel])
        return tot

    def Q(self, yh):
        yh = np.abs(np.asarray(yh, float))
        V = SY * np.sqrt(yh)
        return 4.0 / (CSTAR * YSTAR ** 2) * self._I(V)


# f and h for each smooth kernel (cancellation-safe at v ~ 1e-159)
def f_mono(v):
    return v / np.expm1(v)


def h_mono(v):                                 # f (2 - f e^v)
    f = f_mono(v)
    return f * (2.0 - f * np.exp(v))


def f_simple(v):
    return np.sqrt(1.0 + 0.25 * v * v) - 0.5 * v


def h_simple(v):
    return (1.0 + 0.5 * v * v) / np.sqrt(1.0 + 0.25 * v * v) - v


def f_standard(v):
    return np.exp(0.5 * np.arcsinh(0.5 * v * v)) - v


def h_standard(v):
    E2 = np.exp(0.5 * np.arcsinh(0.5 * v * v))
    return E2 * (1.0 + 0.5 * v * v / np.sqrt(1.0 + 0.25 * v ** 4)) - 2.0 * v


def f_mut(v):
    return v / q_mutate(v) - v


def h_mut(v):
    q = q_mutate(v)
    qp = np.exp(-v) + np.where((v >= V_A) & (v < V_B), 0.5, 0.0)
    r = v / q
    return 2.0 * r - r * r * qp - 2.0 * v


class SpliceKernel:
    """C^2 splice: below yhat_s the polynomial p = y_s^-1/2 (a + b u^2 + c u^4); above it the deep nu_mono adapter."""

    def __init__(self, tag):
        self.name = tag
        self.alpha = ALPHA_C
        self.ys, (self.a, self.b, self.c) = SPL[tag]
        self.yhs = self.ys / YSTAR
        self.base = DeepKernel("nu_mono", f_mono, h_mono)
        self.pref = 1.0 / (CSTAR * SY * math.sqrt(self.yhs))         # = y_s^-1/2 / C*
        self.Qs = float(self._Qlo(np.array([self.yhs]))[0])
        self.Qb_s = float(self.base.Q(np.array([self.yhs]))[0])

    def _Qlo(self, yh):
        u = yh / self.yhs
        return 2.0 * self.pref * self.yhs ** 2 * (self.a * u ** 2 / 2 + self.b * u ** 4 / 4 + self.c * u ** 6 / 6)

    def CT(self, yh):
        yh = np.maximum(np.asarray(yh, float), 1e-300)
        u = yh / self.yhs
        lo = self.pref * (self.a + self.b * u * u + self.c * u ** 4)
        return np.where(yh < self.yhs, lo, self.base.CT(np.maximum(yh, self.yhs)))

    def CL(self, yh):
        yh = np.maximum(np.asarray(yh, float), 1e-300)
        u = yh / self.yhs
        lo = self.pref * (self.a + 3 * self.b * u * u + 5 * self.c * u ** 4)
        return np.where(yh < self.yhs, lo, self.base.CL(np.maximum(yh, self.yhs)))

    def Q(self, yh):
        yh = np.abs(np.asarray(yh, float))
        lo = self._Qlo(np.minimum(yh, self.yhs))
        hi = self.Qs + self.base.Q(np.maximum(yh, self.yhs)) - self.Qb_s
        return np.where(yh < self.yhs, lo, hi)


def make_engine_kernel(name):
    if name == "nu_mono_generic":
        return DeepKernel(name, f_mono, h_mono)
    if name == "nu_simple":
        return DeepKernel(name, f_simple, h_simple)
    if name == "nu_standard":
        return DeepKernel(name, f_standard, h_standard)
    if name in ("S1", "S2"):
        return SpliceKernel(name)
    if name == "MUTATE_kink":
        return DeepKernel(name, f_mut, h_mut, kinks=(V_A, V_B))
    raise KeyError(name)
