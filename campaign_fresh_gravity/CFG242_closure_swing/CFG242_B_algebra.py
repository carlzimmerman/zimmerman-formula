#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG242_B_algebra -- shared sympy algebra for route B (L13): the flat-space quadratic action of the RELATIVE sector delta = h - h-hat of a bimetric theory,
FRESH CODE (the same conventions as CFG232_A2 so the 4D class reproduces WF2/L70, but written here):  L_rel = b EH2[delta] + mu T^(.)[delta], Fourier convention
d_mu -> i k_mu, k^mu = (omega, 0, 0, kappa), every bilinear real (a Hermitian form is D^dagger R D with D = diag(1 for T-even, i for T-odd) -- a congruence, so
residue positivity is unchanged).  EH2 = -(1/2) delta^{mn} G_mn[delta].  Two interactions, quadratic in the connection difference C^a_bc = (1/2) eta^{al}(k_b d_lc + k_c d_lb - k_l d_bc):
  '4D'   the record's tuned five-invariant class, direction T4 - T1 over all spacetime indices (CFG232's class 13a/13b).
  'FOL'  route B's class 13d: the SAME invariants built from the SPATIAL connection difference of the spatial metrics gamma_ij, gamma-hat_ij of a shared foliation
         (indices 1..3 only; no lapse, no shift, no time derivative), i.e. lapse-free.
The five invariants (record's definitions): T1 = g_ab g^mr g^ns C^a_mn C^b_rs, T2 = g_ab P^a P^b, T3 = g^mn V_m V_n, T4 = g^mn C^a_mb C^b_na, T5 = P^a V_a,
P^a = g^mn C^a_mn, V_m = C^a_am.
"""
import sympy as sp

om, ka, mu, bb = sp.symbols("omega kappa mu b")
eta = sp.diag(-1, 1, 1, 1)
kup = sp.Matrix([om, 0, 0, ka])
klo = eta * kup
k2 = (kup.T * klo)[0]
IDX = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
dsym = {ij: sp.Symbol(f"d{ij[0]}{ij[1]}") for ij in IDX}
DVEC = [dsym[ij] for ij in IDX]


def dmat():
    M = sp.zeros(4, 4)
    for (i, j), s in dsym.items():
        M[i, j] = s
        M[j, i] = s
    return M


D = dmat()


def EHquad(d):
    trd = sum(eta[i, i] * d[i, i] for i in range(4))
    Rm = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            Rm[m, n] = sp.Rational(1, 2) * (-sum(klo[m] * kup[l] * d[l, n] for l in range(4)) - sum(klo[n] * kup[l] * d[l, m] for l in range(4))
                                             + k2 * d[m, n] + klo[m] * klo[n] * trd)
    Rs = sum(eta[i, i] * Rm[i, i] for i in range(4))
    Gm = Rm - sp.Rational(1, 2) * eta * Rs
    return sp.expand(-sp.Rational(1, 2) * sum(eta[i, i] * eta[j, j] * d[i, j] * Gm[i, j] for i in range(4) for j in range(4)))


def invariants(d, spatial):
    """T1..T5 (quadratic) of the connection difference of the metric perturbation d; spatial=True restricts every index to 1..3 and uses delta_ij."""
    rng = range(1, 4) if spatial else range(4)
    g = (lambda a, b: 1 if a == b else 0) if spatial else (lambda a, b: eta[a, b])
    ko = (lambda a: kup[a])                       # k_a lowered/raised only matters through g; spatial: k_i = (0,0,kappa)
    kl = (lambda a: klo[a])
    C = {}
    for a in rng:
        for b_ in rng:
            for c_ in rng:
                C[(a, b_, c_)] = sp.Rational(1, 2) * g(a, a) * (kl(b_) * d[a, c_] + kl(c_) * d[a, b_] - kl(a) * d[b_, c_])
    Pv = {a: sum(g(m, n) * C[(a, m, n)] for m in rng for n in rng) for a in rng}
    V = {m: sum(C[(a, a, m)] for a in rng) for m in rng}
    T1 = sum(g(a, b_) * g(m, r) * g(n, s) * C[(a, m, n)] * C[(b_, r, s)] for a in rng for b_ in rng for m in rng for n in rng for r in rng for s in rng)
    T2 = sum(g(a, b_) * Pv[a] * Pv[b_] for a in rng for b_ in rng)
    T3 = sum(g(m, n) * V[m] * V[n] for m in rng for n in rng)
    T4 = sum(g(m, n) * C[(a, m, b_)] * C[(b_, n, a)] for m in rng for n in rng for a in rng for b_ in rng)
    T5 = sum(Pv[a] * V[a] for a in rng)
    return [sp.expand(T) for T in (T1, T2, T3, T4, T5)]


def interaction(kind):
    Ts = invariants(D, spatial=(kind == "FOL"))
    return sp.expand(Ts[3] - Ts[0])                  # direction T4 - T1


def lagrangian(kind, muv=mu):
    return sp.expand(bb * EHquad(D) + muv * interaction(kind))


def hessian(L):
    return sp.Matrix(10, 10, lambda i, j: sp.diff(L, DVEC[i], DVEC[j]))


def block(M, names):
    pos = {str(s): i for i, s in enumerate(DVEC)}
    ix = [pos[n] for n in names]
    return M.extract(ix, ix)
