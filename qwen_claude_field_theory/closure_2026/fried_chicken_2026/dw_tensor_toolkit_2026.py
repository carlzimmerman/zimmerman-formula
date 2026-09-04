#!/usr/bin/env python3
"""
Minimal exact-tensor toolkit (sympy) for the localized Deffayet-Woodard nonlocal-MOND gates.

Everything is index-explicit on a coordinate chart; nothing is assumed about the metric beyond
being a symmetric invertible 4x4 sympy Matrix whose entries may depend on the coordinates.
Signature conventions: mostly plus, R^a_{bcd} = d_c Gamma^a_{db} - ..., R_{bd} = R^a_{bad}.
"""
import itertools
import sympy as sp


class Geometry:
    def __init__(self, g, coords):
        self.g = sp.Matrix(g)
        self.X = list(coords)
        self.n = len(self.X)
        self.gi = sp.simplify(self.g.inv())
        n = self.n
        self.Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    s = 0
                    for d in range(n):
                        s += self.gi[a, d] * (sp.diff(self.g[d, b], self.X[c])
                                              + sp.diff(self.g[d, c], self.X[b])
                                              - sp.diff(self.g[b, c], self.X[d]))
                    self.Gam[a][b][c] = sp.simplify(s / 2)
        self.Ric = sp.zeros(n, n)
        for b in range(n):
            for d in range(n):
                s = 0
                for a in range(n):
                    s += sp.diff(self.Gam[a][b][d], self.X[a]) - sp.diff(self.Gam[a][b][a], self.X[d])
                    for e in range(n):
                        s += self.Gam[a][a][e] * self.Gam[e][b][d] - self.Gam[a][d][e] * self.Gam[e][b][a]
                self.Ric[b, d] = sp.simplify(s)
        self.Rs = sp.simplify(sum(self.gi[a, b] * self.Ric[a, b] for a in range(n) for b in range(n)))
        self.Ein = sp.simplify(self.Ric - sp.Rational(1, 2) * self.g * self.Rs)

    # ---- covariant derivative of an all-lower-index tensor given as nested lists ----
    def cov(self, T, rank):
        """Return nabla_a T_{b1..br} as nested list with the NEW index FIRST."""
        n = self.n
        idx = list(itertools.product(range(n), repeat=rank))

        def get(t, ii):
            for i in ii:
                t = t[i]
            return t

        out = {}
        for a in range(n):
            for ii in idx:
                val = sp.diff(get(T, ii), self.X[a])
                for pos in range(rank):
                    for c in range(n):
                        jj = list(ii)
                        jj[pos] = c
                        val -= self.Gam[c][a][ii[pos]] * get(T, jj)
                out[(a,) + ii] = val
        # nested list
        def build(prefix, depth):
            if depth == rank + 1:
                return out[tuple(prefix)]
            return [build(prefix + [i], depth + 1) for i in range(n)]
        return build([], 0)

    def grad(self, S):
        return [sp.diff(S, x) for x in self.X]

    def box(self, S):
        n = self.n
        dS = self.grad(S)
        ddS = self.cov(dS, 1)
        return sum(self.gi[a, b] * ddS[a][b] for a in range(n) for b in range(n))

    def dot(self, V, W):
        n = self.n
        return sum(self.gi[a, b] * V[a] * W[b] for a in range(n) for b in range(n))

    def raise1(self, V):
        n = self.n
        return [sum(self.gi[a, b] * V[b] for b in range(n)) for a in range(n)]

    def div_vec_upper(self, Vup):
        """nabla_a V^a for an upper-index vector."""
        n = self.n
        return sum(sp.diff(Vup[a], self.X[a]) + sum(self.Gam[a][a][b] * Vup[b] for b in range(n)) for a in range(n))

    def div_sym_lower(self, E):
        """nabla^mu E_{mu nu} for symmetric all-lower E (Matrix). Returns list over nu."""
        n = self.n
        Elist = [[E[a, b] for b in range(n)] for a in range(n)]
        dE = self.cov(Elist, 2)          # dE[a][m][nu] = nabla_a E_{m nu}
        return [sum(self.gi[a, m] * dE[a][m][nu] for a in range(n) for m in range(n)) for nu in range(n)]


def euler_lagrange(L, q, coords, max_order=2):
    """delta S/delta q for a Lagrangian density L depending on q and its derivatives up to max_order."""
    res = sp.diff(L, q)
    for order in range(1, max_order + 1):
        for combo in itertools.combinations_with_replacement(coords, order):
            dq = sp.Derivative(q, *combo)
            term = sp.diff(L, dq)
            if term == 0:
                continue
            for c in combo:
                term = sp.diff(term, c)
            res += (-1) ** order * term
    return res
