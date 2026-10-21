#!/usr/bin/env python3
"""Step 3: identify what the f-variation equation is at linear order.
Compare Ef_lin with the linearized 4D Ricci scalar for g=-N^2dt^2+f delta."""
import sympy as s

r, t = s.symbols('r t', positive=True)
K, Lam = s.symbols('K Lambda', positive=True)
th, ph = s.symbols('theta phi', real=True)
n1 = s.Function('n1')(r); h1 = s.Function('h1')(r)


def christoffel_riemann(g, coords):
    n = len(coords); ginv = g.inv()
    G = [[[s.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                G[a][b][c] = s.together(s.Rational(1, 2)*sum(
                    ginv[a, d]*(s.diff(g[d, b], coords[c]) + s.diff(g[d, c], coords[b])
                                - s.diff(g[b, c], coords[d])) for d in range(n)))
    Ric = s.zeros(n, n)
    for b in range(n):
        for d in range(n):
            tot = 0
            for a in range(n):
                tot += (s.diff(G[a][b][d], coords[a]) - s.diff(G[a][b][a], coords[d])
                        + sum(G[a][a][e]*G[e][b][d] - G[a][d][e]*G[e][b][a]
                              for e in range(n)))
            Ric[b, d] = s.together(tot)
    Rs = s.together(sum(ginv[b, d]*Ric[b, d] for b in range(n) for d in range(n)))
    return G, Ric, Rs


eps = s.symbols('eps', positive=True)
N = 1 + eps*n1
f = 1 + eps*h1
g4 = s.diag(-N**2, f, f*r**2, f*r**2*s.sin(th)**2)
_, Ric4, R4 = christoffel_riemann(g4, [t, r, th, ph])
R1 = s.simplify(s.expand(s.series(s.expand(R4), eps, 0, 2).removeO()).coeff(eps, 1))
print('R^(1) =', s.factor(s.simplify(R1)))
# candidate: -2*(n1''+2n1'/r) - 2*(h1''+2h1'/r)
cand = -2*(s.diff(n1, r, 2) + 2*s.diff(n1, r)/r) - 2*(s.diff(h1, r, 2) + 2*s.diff(h1, r)/r)
print('R1 - cand =', s.simplify(R1 - cand))
