#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fe_common_2026.py -- shared machinery for the SECTOR-1 metric-field-equation derivation of the
generalized completion (THE_GENERALIZED_COMPLETION.md action, c2/c4 symbolic).

Conventions: signature (-,+,+,+), c = 1, coordinates X = (t,x,y,z).
  a^mu = A^nu nabla_nu A^mu,  Q = A^mu d_mu phi,  Y = (g^{mu nu} + A^mu A^nu) d_mu phi d_nu phi,
  F_{mu nu} = nabla_mu A_nu - nabla_nu A_mu,  theta = nabla_mu A^mu.

The aether + scalar Lagrangian (everything except Einstein-Hilbert and matter) is kept GENERIC:
  L_A   = -(K_B/2) F^2 + c2 theta^2 + c4 a.a + lam (A.A + 1)
  L_phi = cJ a.dphi + cY Y + F(Y,Q)
with cJ, cY free symbols (the document's action is cJ = 2(2-K_B), cY = -(2-K_B), and
F(Y,Q) = (a0^2(Q)/8piG) G(sqrt(Y)/a0(Q)) - 2K(Q) + A B(Y/a0^2)(Q-Q0)^2).  Keeping cJ, cY, F generic
makes the metric variation strictly more general than needed; the physical values are substituted
only at display time (fe4).

CANDIDATE closed forms (derived by hand from delta g^{mu nu} at FIXED A^mu, phi, lam; every one
of them is checked against a brute-force jet-space Euler-Lagrange variation on a GENERIC metric in
fe1_metric_variation_generic_2026.py -- they are candidates until that script passes):

  T_{mu nu} = -2 (dL/dg^{mu nu})_explicit + g_{mu nu} L - X_(mu nu)
  X_{ab}    = nabla^m [ J_{m a} A_b + J_{b a} A_m - J_{a m} A_b ]      (the Christoffel-variation term)
  J^m_n     = dL/d(nabla_m A^n) = -2 K_B F^m_n + 2 c2 theta delta^m_n + 2 c4 A^m a_n + cJ A^m dphi_n

  aether EOM   E_n   = 2 lam A_n + 2 c4 a_a nabla_n A^a + cJ dphi_a nabla_n A^a
                       + [2Q (cY + F_Y) + F_Q] dphi_n - nabla_m J^m_n
  scalar EOM   E_phi = -nabla_m Jcur^m,  Jcur^m = cJ a^m + 2 (cY + F_Y) h^{mn} dphi_n + F_Q A^m,
                       h^{mn} = g^{mn} + A^m A^n                          (shift current)
  constraint   E_lam = A.A + 1
"""
import itertools
import random
import sympy as sp
from sympy import Rational as R
from sympy.core.function import AppliedUndef


# --------------------------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------------------------
class Geometry:
    """Metric g[m][n] (symmetric nested lists of expressions), inverse u, sqrt(-g) s, coords X.
    Christoffels are built with sp.diff on the metric entries (works for abstract Functions and
    for concrete expressions alike)."""

    def __init__(self, X, g, u, s):
        self.X = list(X)
        self.n = len(X)
        self.g, self.u, self.s = g, u, s
        n = self.n
        self.Gam = [[[None] * n for _ in range(n)] for _ in range(n)]
        for l in range(n):
            for m in range(n):
                for k in range(m, n):
                    e = R(1, 2) * sum(u[l][q] * (sp.diff(g[q][m], X[k]) + sp.diff(g[q][k], X[m])
                                                 - sp.diff(g[m][k], X[q])) for q in range(n))
                    self.Gam[l][m][k] = e
                    self.Gam[l][k][m] = e

    def d(self, f, m):
        return sp.diff(f, self.X[m])

    def lower(self, V):
        return [sum(self.g[m][k] * V[k] for k in range(self.n)) for m in range(self.n)]

    def raise_(self, V):
        return [sum(self.u[m][k] * V[k] for k in range(self.n)) for m in range(self.n)]

    def cov_vec_up(self, V):
        """dV[m][k] = nabla_m V^k"""
        n, G = self.n, self.Gam
        return [[sp.diff(V[k], self.X[m]) + sum(G[k][m][l] * V[l] for l in range(n))
                 for k in range(n)] for m in range(n)]

    def div_vec_up(self, V):
        n, G = self.n, self.Gam
        return sum(sp.diff(V[m], self.X[m]) + sum(G[m][m][l] * V[l] for l in range(n)) for m in range(n))

    def div_mixed(self, J):
        """out[k] = nabla_m J^m_k"""
        n, G = self.n, self.Gam
        out = []
        for k in range(n):
            e = 0
            for m in range(n):
                e += sp.diff(J[m][k], self.X[m]) + sum(G[m][m][l] * J[l][k] - G[l][m][k] * J[m][l]
                                                       for l in range(n))
            out.append(e)
        return out

    def div_rank3_up(self, W):
        """out[a][b] = nabla_m W^{m a b}"""
        n, G = self.n, self.Gam
        out = [[None] * n for _ in range(n)]
        for a in range(n):
            for b in range(n):
                e = 0
                for m in range(n):
                    e += sp.diff(W[m][a][b], self.X[m])
                    for l in range(n):
                        e += G[m][m][l] * W[l][a][b] + G[a][m][l] * W[m][l][b] + G[b][m][l] * W[m][a][l]
                out[a][b] = e
        return out

    def div_sym_lower(self, T):
        """out[k] = nabla^m T_{m k} = u^{r m} (d_r T_{m k} - Gam^l_{r m} T_{l k} - Gam^l_{r k} T_{m l})"""
        n, G, u = self.n, self.Gam, self.u
        out = []
        for k in range(n):
            e = 0
            for r in range(n):
                for m in range(n):
                    if u[r][m] == 0:
                        continue
                    e += u[r][m] * (sp.diff(T[m][k], self.X[r])
                                    - sum(G[l][r][m] * T[l][k] + G[l][r][k] * T[m][l] for l in range(n)))
            out.append(e)
        return out

    def ricci_auto(self):
        """Ricci tensor with sp.diff acting on the Christoffels directly (u differentiated
        automatically -- the 'route B' curvature used as an independent target)."""
        n, G, X = self.n, self.Gam, self.X
        Ric = [[None] * n for _ in range(n)]
        for m in range(n):
            for k in range(m, n):
                e = 0
                for r in range(n):
                    e += sp.diff(G[r][m][k], X[r]) - sp.diff(G[r][m][r], X[k])
                    for l in range(n):
                        e += G[r][r][l] * G[l][m][k] - G[r][k][l] * G[l][m][r]
                Ric[m][k] = e
                Ric[k][m] = e
        return Ric

    def einstein_lower(self, Ric=None):
        n, g, u = self.n, self.g, self.u
        if Ric is None:
            Ric = self.ricci_auto()
        Rs = sum(u[m][k] * Ric[m][k] for m in range(n) for k in range(n))
        return [[Ric[m][k] - R(1, 2) * g[m][k] * Rs for k in range(n)] for m in range(n)], Rs


# --------------------------------------------------------------------------------------------
# the aether + scalar sector: Lagrangian, candidate stress tensors, candidate EOMs
# --------------------------------------------------------------------------------------------
def build_sector(geo, A, phi, lam, Fexpr, Ys, Qs, KB, c2, c4, cJ, cY):
    """A: list of 4 expressions (A^mu, UPPER index); phi, lam: expressions; Fexpr: expression in
    the symbols Ys, Qs.  Returns a dict of everything.  All index placements as in the docstring."""
    n, g, u, X = geo.n, geo.g, geo.u, geo.X
    rng = range(n)
    dA = geo.cov_vec_up(A)                                             # nabla_m A^k
    A_dn = geo.lower(A)
    dA_dn = [[sum(g[k][r] * dA[m][r] for r in rng) for k in rng] for m in rng]   # nabla_m A_k
    dA_updn = [[sum(u[a][r] * dA_dn[r][k] for r in rng) for k in rng] for a in rng]  # nabla^a A_k
    theta = sum(dA[m][m] for m in rng)
    a_up = [sum(A[l] * dA[l][m] for l in rng) for m in rng]
    a_dn = geo.lower(a_up)
    Fmn = [[dA_dn[m][k] - dA_dn[k][m] for k in rng] for m in rng]     # F_{mk}
    Fup = [[sum(u[m][r] * Fmn[r][k] for r in rng) for k in rng] for m in rng]  # F^m_k
    F2 = sum(u[m][r] * u[k][q] * Fmn[m][k] * Fmn[r][q] for m, k, r, q in itertools.product(rng, repeat=4))
    phi_d = [sp.diff(phi, X[m]) for m in rng]
    Q = sum(A[m] * phi_d[m] for m in rng)
    Y = sum((u[m][k] + A[m] * A[k]) * phi_d[m] * phi_d[k] for m in rng for k in rng)
    AA = sum(A_dn[m] * A[m] for m in rng)
    a2 = sum(a_dn[m] * a_up[m] for m in rng)
    adphi = sum(a_up[m] * phi_d[m] for m in rng)
    rep = {Ys: Y, Qs: Q}
    Fv = Fexpr.xreplace(rep)
    FY = sp.diff(Fexpr, Ys).xreplace(rep)
    FQ = sp.diff(Fexpr, Qs).xreplace(rep)

    L_A = -KB / 2 * F2 + c2 * theta ** 2 + c4 * a2 + lam * (AA + 1)
    L_phi = cJ * adphi + cY * Y + Fv

    JA = [[-2 * KB * Fup[m][k] + 2 * c2 * theta * (1 if m == k else 0) + 2 * c4 * A[m] * a_dn[k]
           for k in rng] for m in rng]
    Jphi = [[cJ * A[m] * phi_d[k] for k in rng] for m in rng]

    def Xsym(J):
        Jup = [[sum(J[m][k] * u[k][a] for k in rng) for a in rng] for m in rng]      # J^{m a}
        W = [[[Jup[m][a] * A[b] + Jup[b][a] * A[m] - Jup[a][m] * A[b] for b in rng] for a in rng]
             for m in rng]
        Xup = geo.div_rank3_up(W)
        Xdn = [[sum(g[a][c] * g[b][d] * Xup[c][d] for c in rng for d in rng) for b in rng] for a in rng]
        return [[R(1, 2) * (Xdn[a][b] + Xdn[b][a]) for b in rng] for a in rng]

    XA, Xphi = Xsym(JA), Xsym(Jphi)
    TA = [[2 * KB * (sum(dA[m][b] * dA_dn[k][b] for b in rng) - sum(dA_updn[al][m] * dA_dn[al][k] for al in rng))
           + 2 * c4 * a_dn[m] * a_dn[k] + 2 * lam * A_dn[m] * A_dn[k] + g[m][k] * L_A - XA[m][k]
           for k in rng] for m in rng]
    Tphi = [[-2 * (cY + FY) * phi_d[m] * phi_d[k] + g[m][k] * L_phi - Xphi[m][k] for k in rng] for m in rng]

    J = [[JA[m][k] + Jphi[m][k] for k in rng] for m in rng]
    divJ = geo.div_mixed(J)
    EA = [2 * lam * A_dn[k] + 2 * c4 * sum(a_dn[al] * dA[k][al] for al in rng)
          + cJ * sum(phi_d[al] * dA[k][al] for al in rng) + (2 * Q * (cY + FY) + FQ) * phi_d[k] - divJ[k]
          for k in rng]
    cur = [cJ * a_up[m] + 2 * (cY + FY) * sum((u[m][k] + A[m] * A[k]) * phi_d[k] for k in rng) + FQ * A[m]
           for m in rng]
    Ephi = -geo.div_vec_up(cur)
    Elam = AA + 1
    # lambda from A^n E_n = 0 on the constraint surface A.A = -1
    lam_formula = R(1, 2) * (2 * c4 * a2 + cJ * adphi + 2 * Q ** 2 * (cY + FY) + Q * FQ
                             - sum(A[k] * divJ[k] for k in rng))
    return dict(dA=dA, A_dn=A_dn, dA_dn=dA_dn, theta=theta, a_up=a_up, a_dn=a_dn, Fmn=Fmn, F2=F2,
                phi_d=phi_d, Q=Q, Y=Y, AA=AA, a2=a2, adphi=adphi, F=Fv, FY=FY, FQ=FQ,
                L_A=L_A, L_phi=L_phi, JA=JA, Jphi=Jphi, J=J, XA=XA, Xphi=Xphi, TA=TA, Tphi=Tphi,
                divJ=divJ, EA=EA, cur=cur, Ephi=Ephi, Elam=Elam, lam_formula=lam_formula)


# --------------------------------------------------------------------------------------------
# abstract generic setup (10 metric functions of all four coordinates) + random-jet evaluation
# --------------------------------------------------------------------------------------------
def abstract_setup():
    X = sp.symbols('t x y z', real=True)
    gF, uF = {}, {}
    for m in range(4):
        for k in range(m, 4):
            gF[(m, k)] = sp.Function(f'g{m}{k}')(*X)
            uF[(m, k)] = sp.Function(f'u{m}{k}')(*X)
    g = [[gF[(min(m, k), max(m, k))] for k in range(4)] for m in range(4)]
    u = [[uF[(min(m, k), max(m, k))] for k in range(4)] for m in range(4)]
    s = sp.Function('s')(*X)
    A = [sp.Function(f'A{m}')(*X) for m in range(4)]
    phi = sp.Function('phi')(*X)
    lam = sp.Function('lam')(*X)
    return X, gF, uF, g, u, s, A, phi, lam


def multi_indices(n, order):
    """sorted tuples of coordinate indices with repetition, |k| = order"""
    return list(itertools.combinations_with_replacement(range(n), order))


def rand_rat(rng, lo=-1, hi=1, den=7):
    d = rng.randint(1, den)
    return R(rng.randint(lo * d, hi * d), d)


def truncate_poly(expr, X, deg):
    """keep monomials of total degree <= deg"""
    p = sp.Poly(sp.expand(expr), *X)
    out = 0
    for mon, c in p.terms():
        if sum(mon) <= deg:
            out += c * sp.prod([xi ** e for xi, e in zip(X, mon)])
    return out


class RandomJet:
    """A random generic point in jet space: metric jets to 3rd order (with the exact induced jets of
    the inverse metric and of sqrt(-g)), aether/scalar/multiplier jets to 3rd order, all rational.
    sqrt(-g) at the point is kept as the symbol S (every term of a Lagrangian density carries exactly
    one factor of it), its derivatives are S times exact rationals."""

    def __init__(self, seed, X, gF, uF, s, A, phi, lam, max_order=3):
        rng = random.Random(seed)
        self.X = list(X)
        n = len(X)
        self.S = sp.Symbol('S', positive=True)
        # metric jets: G[k] for multi-index k (sorted tuple), G[()] = value at the point
        G = {}
        G0 = sp.zeros(n, n)
        for m in range(n):
            for k in range(m, n):
                v = (-1 if m == 0 else 1) * (1 if m == k else 0) + rand_rat(rng, -1, 1, 5) / 5
                G0[m, k] = v
                G0[k, m] = v
        assert G0.det() < 0, "want a Lorentzian point"
        G[()] = G0
        for order in range(1, max_order + 1):
            for mi in multi_indices(n, order):
                M = sp.zeros(n, n)
                for m in range(n):
                    for k in range(m, n):
                        v = rand_rat(rng)
                        M[m, k] = v
                        M[k, m] = v
                G[mi] = M
        self.G = G
        # Taylor polynomial of g to 3rd order, then exact truncated inverse and sqrt(-det)
        gpoly = sp.zeros(n, n)
        for mi, M in G.items():
            mon = sp.prod([X[i] for i in mi]) if mi else 1
            fact = sp.prod([sp.factorial(mi.count(i)) for i in set(mi)]) if mi else 1
            gpoly += M * mon / fact
        U0 = G0.inv()
        Delta = gpoly - G0
        N = -U0 * Delta
        upoly = sp.zeros(n, n)
        term = sp.eye(n)
        for _ in range(max_order + 1):
            upoly += term
            term = (term * N).applyfunc(lambda e: truncate_poly(e, X, max_order))
        upoly = (upoly * U0).applyfunc(lambda e: truncate_poly(e, X, max_order))
        # check: g u = 1 to the truncation order
        chk = (gpoly * upoly - sp.eye(n)).applyfunc(lambda e: truncate_poly(e, X, max_order))
        assert all(sp.expand(chk[i, j]) == 0 for i in range(n) for j in range(n))
        w = truncate_poly(sp.expand(gpoly.det() / G0.det() - 1), X, max_order)
        sratio = truncate_poly(sp.expand(1 + w / 2 - w ** 2 / 8 + w ** 3 / 16), X, max_order)
        self.gpoly, self.upoly, self.sratio = gpoly, upoly, sratio
        # jets of u and s/S
        zero = {xi: 0 for xi in X}
        self.U, self.Sj = {}, {}
        for order in range(0, max_order + 1):
            for mi in ([()] if order == 0 else multi_indices(n, order)):
                dv = [X[i] for i in mi]
                self.U[mi] = upoly.applyfunc(lambda e: sp.diff(e, *dv).subs(zero) if dv else e.subs(zero))
                self.Sj[mi] = (sp.diff(sratio, *dv).subs(zero) if dv else sratio.subs(zero))
        # free fields
        self.Aj = {}
        self.phij = {}
        self.lamj = {}
        for order in range(0, max_order + 1):
            for mi in ([()] if order == 0 else multi_indices(n, order)):
                self.Aj[mi] = [rand_rat(rng) for _ in range(n)]
                if order == 0:
                    self.Aj[mi][0] = 1 + rand_rat(rng, -1, 1, 4) / 4      # roughly timelike, not unit
                self.phij[mi] = rand_rat(rng)
                self.lamj[mi] = rand_rat(rng)
        self.gF, self.uF, self.s, self.A, self.phi, self.lam = gF, uF, s, A, phi, lam
        self.name_map = {}
        for (m, k), f in gF.items():
            self.name_map[f.func] = ('g', m, k)
        for (m, k), f in uF.items():
            self.name_map[f.func] = ('u', m, k)
        self.name_map[s.func] = ('s',)
        for m, f in enumerate(A):
            self.name_map[f.func] = ('A', m)
        self.name_map[phi.func] = ('phi',)
        self.name_map[lam.func] = ('lam',)

    def value(self, kind, mi):
        if kind[0] == 'g':
            return self.G[mi][kind[1], kind[2]]
        if kind[0] == 'u':
            return self.U[mi][kind[1], kind[2]]
        if kind[0] == 's':
            return self.S * self.Sj[mi]
        if kind[0] == 'A':
            return self.Aj[mi][kind[1]]
        if kind[0] == 'phi':
            return self.phij[mi]
        if kind[0] == 'lam':
            return self.lamj[mi]
        raise KeyError(kind)

    def evaluate(self, expr):
        rep = {}
        for a in expr.atoms(sp.Derivative):
            f = a.expr
            if not isinstance(f, AppliedUndef) or f.func not in self.name_map:
                raise ValueError(f"unknown derivative atom {a}")
            mi = tuple(sorted(self.X.index(v) for v in a.variables))
            rep[a] = self.value(self.name_map[f.func], mi)
        for a in expr.atoms(AppliedUndef):
            if a.func in self.name_map:
                rep[a] = self.value(self.name_map[a.func], ())
        return sp.expand(expr.xreplace(rep))


def random_F(seed, Ys, Qs, deg=4, tag=None):
    """random polynomial F(Y,Q) of total degree deg with rational coefficients; every coefficient is
    multiplied by an optional symbol `tag` so residuals proportional to the F-sector are identifiable."""
    rng = random.Random(seed)
    F = 0
    for i in range(deg + 1):
        for j in range(deg + 1 - i):
            F += rand_rat(rng) * Ys ** i * Qs ** j
    return (tag * F) if tag is not None else F
