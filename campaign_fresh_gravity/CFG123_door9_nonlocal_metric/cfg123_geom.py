#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg123_geom -- sympy machinery for CFG123: curvature, the covariant field equation of the localised RR (and DW) actions.

Localised RR action (frozen, CFG123_FROZEN_CRITERIA.md section b1), overall factor 1/16 pi G dropped, mostly-plus signature:
    L = sqrt(-g) [ R (1 - (m^2/6) S) - xi1 (box U + R) - xi2 (box S + U) ]
Covariant field equation (coefficient of delta g^{mu nu}), derived here by hand and CHECKED against the reduced action in A1:
    E_mu nu = F G_mu nu + (g_mu nu box - nabla_mu nabla_nu) F + d_(mu xi1 d_nu) U + d_(mu xi2 d_nu) S
              - (1/2) g_mu nu (d xi1 . d U + d xi2 . d S) + (1/2) g_mu nu xi2 U ,     F = 1 - m^2 S/6 - xi1
    = 8 pi G T_mu nu   (matter: delta S_m = -(1/2) sqrt(-g) T_mu nu delta g^{mu nu}, in the same 1/16 pi G units).
Scalar equations: E_xi1 = -(box U + R), E_xi2 = -(box S + U), E_U = -box xi1 - xi2, E_S = -(m^2/6) R - box xi2.
On shell (retarded zero-data): xi1 = (m^2/6) S, xi2 = (m^2/6) U.
DW: L = sqrt(-g) [ R (1 + f(X) - xi) - g^{mu nu} d_mu xi d_nu X ]:
    E_mu nu = F G_mu nu + (g box - nabla nabla) F - [ d_(mu xi d_nu) X - (1/2) g_mu nu d xi . d X ],  F = 1 + f(X) - xi.
"""
import sympy as sp


def geometry(g, X):
    n = len(X)
    gi = g.inv()
    Gam = [[[sum(gi[l, s] * (sp.diff(g[s, m], X[nn]) + sp.diff(g[s, nn], X[m]) - sp.diff(g[m, nn], X[s])) for s in range(n)) / 2
             for nn in range(n)] for m in range(n)] for l in range(n)]
    Gam = [[[sp.simplify(Gam[l][m][nn]) for nn in range(n)] for m in range(n)] for l in range(n)]

    def riem(r, s, m, nn):
        e = sp.diff(Gam[r][nn][s], X[m]) - sp.diff(Gam[r][m][s], X[nn])
        e += sum(Gam[r][m][l] * Gam[l][nn][s] - Gam[r][nn][l] * Gam[l][m][s] for l in range(n))
        return e

    Ric = sp.Matrix(n, n, lambda s, nn: sp.simplify(sum(riem(r, s, r, nn) for r in range(n))))
    Rs = sp.simplify(sum(gi[s, nn] * Ric[s, nn] for s in range(n) for nn in range(n)))
    Ein = sp.simplify(Ric - g * Rs / 2)
    return dict(g=g, gi=gi, Gam=Gam, Ric=Ric, R=Rs, G=Ein, X=X, n=n)


def hess(geo, f):
    X, n, Gam = geo["X"], geo["n"], geo["Gam"]
    return sp.Matrix(n, n, lambda m, nn: sp.diff(f, X[m], X[nn]) - sum(Gam[l][m][nn] * sp.diff(f, X[l]) for l in range(n)))


def box(geo, f):
    H = hess(geo, f)
    gi, n = geo["gi"], geo["n"]
    return sum(gi[m, nn] * H[m, nn] for m in range(n) for nn in range(n))


def dot(geo, a, b):
    X, gi, n = geo["X"], geo["gi"], geo["n"]
    return sum(gi[m, nn] * sp.diff(a, X[m]) * sp.diff(b, X[nn]) for m in range(n) for nn in range(n))


def symd(geo, a, b):
    """d_(mu a d_nu) b."""
    X, n = geo["X"], geo["n"]
    return sp.Matrix(n, n, lambda m, nn: (sp.diff(a, X[m]) * sp.diff(b, X[nn]) + sp.diff(a, X[nn]) * sp.diff(b, X[m])) / 2)


def E_RR(geo, m2, U, S, x1, x2):
    """covariant field equation of the localised RR action (off shell in the multipliers).  m2 = m^2."""
    g = geo["g"]
    F = 1 - m2 * S / 6 - x1
    E = F * geo["G"] + g * box(geo, F) - hess(geo, F) + symd(geo, x1, U) + symd(geo, x2, S)
    E = E - g * (dot(geo, x1, U) + dot(geo, x2, S)) / 2 + g * x2 * U / 2
    return E


def scalar_eoms_RR(geo, m2, U, S, x1, x2):
    R = geo["R"]
    return dict(U=-box(geo, x1) - x2, S=-m2 * R / 6 - box(geo, x2), x1=-(box(geo, U) + R), x2=-(box(geo, S) + U))


def E_DW(geo, fX, X_, xi):
    """covariant field equation of the localised DW action; fX = f(X) as an expression of X_."""
    g = geo["g"]
    F = 1 + fX - xi
    E = F * geo["G"] + g * box(geo, F) - hess(geo, F) - (symd(geo, xi, X_) - g * dot(geo, xi, X_) / 2)
    return E


def scalar_eoms_DW(geo, fprime, X_, xi):
    """fprime = f'(X) as an expression (passed explicitly: sympy cannot differentiate w.r.t. an expression)."""
    R = geo["R"]
    return dict(xi=-R + box(geo, X_), X=fprime * R + box(geo, xi))
