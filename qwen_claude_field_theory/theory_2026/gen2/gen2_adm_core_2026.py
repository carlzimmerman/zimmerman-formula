#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gen2_adm_core_2026.py -- shared machinery for the CONSTRAINT-REDUCED quadratic action
of the frozen Gen-2 action.  Nothing physical is asserted here; this file only builds
the exact O(eps^2) Lagrangian and its plane-wave quadratic form.  All physics claims
live in the driver scripts, each with PASS/FAIL checks.

FROZEN ACTION (c = 1, x^0 = ct, ell := c^2/a0), unitary gauge T = t:

  S = (M_Pl^2 c^3/2) INT dt d^3x  N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
                                              - (2/ell^2) F(X, Y) ]
  a_i   = D_i ln N
  K_ij  = (dot h_ij - D_i N_j - D_j N_i) / (2N)
  X     = ell^2 h^{ij} a_i a_j
  T_ij  = D_i D_j ln N - (1/3) h_ij h^{kl} D_k D_l ln N        [= D_<i a_j>]
  Y     = ell^4 T_ij T^ij
  F     = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps_Y * A(X) * Y ,    A(X) = X^2/(1+X)^4

BACKGROUND (chosen so that T^(0)_ij = 0 EXACTLY -- no cross terms):
  h_ij = delta_ij , N = Nb(z) = exp(abar z) , N_i = 0
  => a_i = abar zhat exactly, D_iD_j ln N = 0 exactly, T^(0) = 0, Y^(0) = 0,
     X^(0) = ell^2 abar^2 =: X0  (kept EXACT: O(1) for a galaxy).

Background gradients are kept: Nb is carried as a function with dNb/dz = abar*Nb, and
Nb -> 1 is imposed only at the end (local/WKB frame at z = 0).

TRUNCATION: every quantity is carried as a 3-jet (c0, c1, c2) in the perturbation
bookkeeping parameter eps, so nothing above O(eps^2) is ever formed.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
COORDS = [x, y, z]
abar = sp.Symbol('abar', positive=True)
ell = sp.Symbol('ell', positive=True)
lam = sp.Symbol('lambda_K')
eta = sp.Symbol('eta_K')
w, k = sp.symbols('omega k', positive=True)
F0, FX, FXX, FY = sp.symbols('F_0 F_X F_XX F_Y')
X0 = sp.Symbol('X_0', nonnegative=True)
epsY = sp.Symbol('epsilon_Y')


class Nb(sp.Function):
    nargs = 1

    def fdiff(self, argindex=1):
        return abar * Nb(self.args[0])


# ------------------------------------------------------------------ 3-jets in eps
def J(c0=0, c1=0, c2=0):
    return (sp.sympify(c0), sp.sympify(c1), sp.sympify(c2))


def jadd(*js):
    return tuple(sp.Add(*[j[i] for j in js]) for i in range(3))


def jscal(s, j):
    return (s * j[0], s * j[1], s * j[2])


def jmul(a, b):
    return (sp.expand(a[0] * b[0]),
            sp.expand(a[0] * b[1] + a[1] * b[0]),
            sp.expand(a[0] * b[2] + a[1] * b[1] + a[2] * b[0]))


def jsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def jdiff(a, v):
    return tuple(sp.expand(sp.diff(c, v)) for c in a)


def jinv(a):
    """1/a for a[0] != 0"""
    i0 = 1 / a[0]
    i1 = -a[1] / a[0]**2
    i2 = (a[1]**2 / a[0]**3 - a[2] / a[0]**2)
    return (sp.expand(i0), sp.expand(i1), sp.expand(i2))


# ------------------------------------------------------------------ builder
NAMES = ['phi', 'B1', 'B2', 'B3', 'H11', 'H12', 'H13', 'H22', 'H23', 'H33']


def build_L2(kvec, gauge_zero=(), drop_fields=()):
    """
    Exact O(eps^2) Lagrangian density / (M_Pl^2 c^3/2) for plane-wave perturbations with
    wavevector kvec, in the gauge H_ij = 0 for (i,j) in gauge_zero (0-indexed pairs).
    Returns (L2const, amps, conjamps, names_used, L1).
    """
    theta = sum(kvec[i] * COORDS[i] for i in range(3)) - w * t
    E = sp.exp(sp.I * theta)
    A, Ab = {}, {}
    zeroed = set()
    for (i, j) in gauge_zero:
        zeroed.add('H%d%d' % (min(i, j) + 1, max(i, j) + 1))
    for n in NAMES:
        if n in zeroed or n in drop_fields:
            A[n] = sp.S(0); Ab[n] = sp.S(0)
        else:
            A[n] = sp.Symbol('A_' + n); Ab[n] = sp.Symbol('Ab_' + n)

    def f(n):
        return A[n] * E + Ab[n] / E

    Hm = sp.Matrix(3, 3, lambda i, j: f('H%d%d' % (min(i, j) + 1, max(i, j) + 1)))
    Bv = [f('B1'), f('B2'), f('B3')]
    phi = f('phi')

    # metric jets
    hj = [[J(1 if i == j else 0, Hm[i, j], 0) for j in range(3)] for i in range(3)]
    H2 = sp.expand(Hm * Hm)
    hinv = [[J(1 if i == j else 0, -Hm[i, j], H2[i, j]) for j in range(3)] for i in range(3)]
    trH = sp.expand(sp.trace(Hm))
    trH2 = sp.expand(sp.trace(Hm * Hm))
    sqh = J(1, trH / 2, sp.expand(trH**2 / 8 - trH2 / 4))

    Nj = J(Nb(z), Nb(z) * phi, 0)
    lnN = J(sp.log(Nb(z)), phi, sp.expand(-phi**2 / 2))

    # Christoffels  Gam^a_ij  (jet)
    dH = [[[sp.expand(sp.diff(Hm[i, j], COORDS[m])) for m in range(3)]
           for j in range(3)] for i in range(3)]
    Gam = [[[None] * 3 for _ in range(3)] for _ in range(3)]
    for a_ in range(3):
        for i in range(3):
            for j in range(3):
                acc = J()
                for l in range(3):
                    inner = J(0, sp.expand(dH[l][j][i] + dH[l][i][j] - dH[i][j][l]), 0)
                    acc = jadd(acc, jmul(hinv[a_][l], inner))
                Gam[a_][i][j] = jscal(sp.Rational(1, 2), acc)

    # Ricci (jet)
    Ric = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = J()
            for a_ in range(3):
                acc = jadd(acc, jdiff(Gam[a_][i][j], COORDS[a_]))
                acc = jsub(acc, jdiff(Gam[a_][i][a_], COORDS[j]))
                for b_ in range(3):
                    acc = jadd(acc, jmul(Gam[a_][a_][b_], Gam[b_][i][j]))
                    acc = jsub(acc, jmul(Gam[a_][j][b_], Gam[b_][i][a_]))
            Ric[i][j] = acc
    R3 = J()
    for i in range(3):
        for j in range(3):
            R3 = jadd(R3, jmul(hinv[i][j], Ric[i][j]))

    # D_i N_j  (N_j is O(eps))
    DN = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = J(0, sp.expand(sp.diff(Bv[j], COORDS[i])), 0)
            for a_ in range(3):
                acc = jsub(acc, jmul(Gam[a_][i][j], J(0, Bv[a_], 0)))
            DN[i][j] = acc
    inv2N = jscal(sp.Rational(1, 2), jinv(Nj))
    Kj = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            num = jsub(jdiff(hj[i][j], t), jadd(DN[i][j], DN[j][i]))
            Kj[i][j] = jmul(num, inv2N)
    Ktr = J()
    for i in range(3):
        for j in range(3):
            Ktr = jadd(Ktr, jmul(hinv[i][j], Kj[i][j]))
    KK = J()
    for i in range(3):
        for j in range(3):
            for m in range(3):
                for n_ in range(3):
                    KK = jadd(KK, jmul(jmul(hinv[i][m], hinv[j][n_]),
                                       jmul(Kj[i][j], Kj[m][n_])))

    # a_i, X
    aj = [jdiff(lnN, COORDS[i]) for i in range(3)]
    a2 = J()
    for i in range(3):
        for j in range(3):
            a2 = jadd(a2, jmul(hinv[i][j], jmul(aj[i], aj[j])))
    Xj = jscal(ell**2, a2)

    # T_ij, Y
    DD = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = jdiff(jdiff(lnN, COORDS[i]), COORDS[j])
            for a_ in range(3):
                acc = jsub(acc, jmul(Gam[a_][i][j], aj[a_]))
            DD[i][j] = acc
    trDD = J()
    for i in range(3):
        for j in range(3):
            trDD = jadd(trDD, jmul(hinv[i][j], DD[i][j]))
    Tj = [[jsub(DD[i][j], jscal(sp.Rational(1, 3), jmul(hj[i][j], trDD)))
           for j in range(3)] for i in range(3)]
    Yj = J()
    for i in range(3):
        for j in range(3):
            for m in range(3):
                for n_ in range(3):
                    Yj = jadd(Yj, jmul(jmul(hinv[i][m], hinv[j][n_]),
                                       jmul(Tj[i][j], Tj[m][n_])))
    Yj = jscal(ell**4, Yj)

    # F to O(eps^2)
    Fj = jadd(J(F0, 0, 0),
              jscal(FX, J(0, Xj[1], Xj[2])),
              jscal(FY, J(0, Yj[1], Yj[2])),
              jscal(sp.Rational(1, 2) * FXX, J(0, 0, sp.expand(Xj[1]**2))))

    bracket = jadd(R3, KK, jscal(-lam, jmul(Ktr, Ktr)), jscal(eta, a2),
                   jscal(-2 / ell**2, Fj))
    Lj = jmul(jmul(Nj, sqh), bracket)

    def finish(e):
        e = sp.expand(e)
        for _ in range(10):
            e2 = sp.expand(e.replace(sp.Derivative(Nb(z), z), abar * Nb(z)).doit())
            if e2 == e:
                break
            e = e2
        return sp.expand(e.subs(Nb(z), 1))

    L1 = finish(Lj[1])
    L2 = finish(Lj[2])
    CO = {t, x, y, z}
    L2c = sp.Add(*[trm for trm in sp.Add.make_args(L2) if not (trm.free_symbols & CO)])
    L2c = sp.expand(L2c.subs(abar, sp.sqrt(X0) / ell))
    used = [n for n in NAMES if A[n] != 0]
    return L2c, [A[n] for n in used], [Ab[n] for n in used], used, L1


def hermitian_matrix(L2c, amps, conj):
    n = len(amps)
    M = sp.zeros(n, n)
    for a_ in range(n):
        for b_ in range(n):
            M[a_, b_] = sp.expand(sp.diff(L2c, conj[a_], amps[b_]))
    resid = sp.expand(L2c - sum(conj[a_] * M[a_, b_] * amps[b_]
                                for a_ in range(n) for b_ in range(n)))
    return M, resid


def schur(M, keep, drop):
    Mkk = M[keep, keep]; Mkd = M[keep, drop]; Mdk = M[drop, keep]; Mdd = M[drop, drop]
    return sp.simplify(Mkk - Mkd * Mdd.inv() * Mdk)


def frozen_subs(with_Y=True):
    """F and its derivatives at the background (X0, Y=0) for the FROZEN F."""
    s = sp.sqrt(X0)
    return {F0: -2 * s + 2 * sp.log(1 + s),
            FX: -1 / (1 + s),
            FXX: 1 / (2 * s * (1 + s)**2),
            FY: (epsY * X0**2 / (1 + X0)**4) if with_Y else sp.S(0)}


KHRONO_OFF = {F0: 0, FX: 0, FXX: 0, FY: 0}
