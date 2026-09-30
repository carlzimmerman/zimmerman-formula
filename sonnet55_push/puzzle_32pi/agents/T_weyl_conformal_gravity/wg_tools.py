"""Shared sympy tools for the Weyl-gravity lane (T).  Signature (-,+,+,+), standard Riemann convention
R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb} + Gamma^a_{ce} Gamma^e_{db} - Gamma^a_{de} Gamma^e_{cb},  R_{bd} = R^a_{bad}.
Bach tensor  B_{ab} = nabla^c nabla^d C_{acbd} + (1/2) R^{cd} C_{acbd}   (vanishes for every conformally flat metric and every Einstein space;
the Weyl-gravity vacuum equation is B_{ab} = 0).  Sign conventions of the overall Bach tensor do not matter for B_{ab} = 0.
Nothing in this file assumes any solution; it is a plain curvature calculator for a diagonal metric.
"""
import sympy as sp
import itertools


class Geo:
    def __init__(self, coords, gdiag, simp=sp.simplify):
        self.x = tuple(coords)
        self.n = len(coords)
        self.simp = simp
        self.g = sp.diag(*gdiag)
        self.gi = sp.diag(*[1 / e for e in gdiag])
        n = self.n
        x = self.x
        g, gi = self.g, self.gi
        # Christoffel Gamma^a_{bc}
        G = [[[0] * n for _ in range(n)] for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for c in range(b, n):
                    s = 0
                    for d in range(n):
                        if gi[a, d] != 0:
                            s += gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d])) / 2
                    s = simp(s)
                    G[a][b][c] = s
                    G[a][c][b] = s
        self.G = G
        # Riemann R^a_{bcd}
        Rm = {}
        for a, b, c, d in itertools.product(range(n), repeat=4):
            if c >= d:
                continue
            s = sp.diff(G[a][d][b], x[c]) - sp.diff(G[a][c][b], x[d])
            for e in range(n):
                s += G[a][c][e] * G[e][d][b] - G[a][d][e] * G[e][c][b]
            s = simp(s)
            Rm[(a, b, c, d)] = s
            Rm[(a, b, d, c)] = -s
        for a, b, c in itertools.product(range(n), repeat=3):
            Rm[(a, b, c, c)] = 0
        self.Rm = Rm
        # Ricci, scalar
        Ric = sp.zeros(n, n)
        for b in range(n):
            for d in range(n):
                Ric[b, d] = simp(sum(Rm[(a, b, a, d)] for a in range(n)))
        self.Ric = Ric
        self.R = simp(sum(gi[a, a] * Ric[a, a] for a in range(n)))
        # all-lower Riemann and Weyl
        def low(a, b, c, d):
            return sum(g[a, e] * Rm[(e, b, c, d)] for e in range(n) if g[a, e] != 0)
        Rl = {}
        for a, b, c, d in itertools.product(range(n), repeat=4):
            Rl[(a, b, c, d)] = simp(low(a, b, c, d))
        self.Rl = Rl
        C = {}
        R = self.R
        for a, b, c, d in itertools.product(range(n), repeat=4):
            val = (Rl[(a, b, c, d)]
                   - sp.Rational(1, 2) * (g[a, c] * Ric[b, d] - g[a, d] * Ric[b, c] - g[b, c] * Ric[a, d] + g[b, d] * Ric[a, c])
                   + R / 6 * (g[a, c] * g[b, d] - g[a, d] * g[b, c]))
            C[(a, b, c, d)] = simp(val)
        self.C = C

    def weyl_squared(self):
        n = self.n
        gi = self.gi
        s = 0
        for a, b, c, d in itertools.product(range(n), repeat=4):
            v = self.C[(a, b, c, d)]
            if v != 0:
                s += gi[a, a] * gi[b, b] * gi[c, c] * gi[d, d] * v * v
        return self.simp(s)

    def weyl_is_zero(self):
        return all(v == 0 for v in self.C.values())

    def bach(self):
        """B_{ab} = nabla^c nabla^d C_{acbd} + 1/2 R^{cd} C_{acbd}."""
        n, x, G, gi, C, simp = self.n, self.x, self.G, self.gi, self.C, self.simp
        # Y_{acb} = g^{de} nabla_e C_{acbd}
        Y = {}
        for a, c, b in itertools.product(range(n), repeat=3):
            s = 0
            for d in range(n):
                e = d  # diagonal metric
                term = sp.diff(C[(a, c, b, d)], x[e])
                for m in range(n):
                    term -= G[m][e][a] * C[(m, c, b, d)]
                    term -= G[m][e][c] * C[(a, m, b, d)]
                    term -= G[m][e][b] * C[(a, c, m, d)]
                    term -= G[m][e][d] * C[(a, c, b, m)]
                s += gi[d, d] * term
            Y[(a, c, b)] = simp(s)
        Bh = sp.zeros(n, n)
        for a in range(n):
            for b in range(n):
                s = 0
                for c in range(n):
                    f = c
                    term = sp.diff(Y[(a, c, b)], x[f])
                    for m in range(n):
                        term -= G[m][f][a] * Y[(m, c, b)]
                        term -= G[m][f][c] * Y[(a, m, b)]
                        term -= G[m][f][b] * Y[(a, c, m)]
                    s += gi[c, c] * term
                # + 1/2 R^{cd} C_{acbd}
                for c in range(n):
                    for d in range(n):
                        if self.Ric[c, d] != 0:
                            s += sp.Rational(1, 2) * gi[c, c] * gi[d, d] * self.Ric[c, d] * C[(a, c, b, d)]
                Bh[a, b] = simp(s)
        return Bh


def static_spherical(Bfun, r, coords=None, simp=sp.simplify):
    """ds^2 = -B dt^2 + dr^2/B + r^2 dOmega^2 (the gauge g_tt g_rr = -1, g_thth = r^2)."""
    t, th, ph = sp.symbols('t theta phi')
    X = (t, r, th, ph)
    return Geo(X, [-Bfun, 1 / Bfun, r**2, r**2 * sp.sin(th)**2], simp=simp), X
