#!/usr/bin/env python3
"""Step 1: build exact static-spherical reduction; validate R3 and the ADM field
equations against an independent Einstein-tensor computation."""
import sympy as s

r, K, beta, eta, gamma, a0, Lam = s.symbols('r K beta eta gamma a0 Lambda', positive=True)


def christoffel_riemann(g, coords):
    """generic: g = Matrix of metric components (functions of coords)."""
    n = len(coords)
    ginv = g.inv()
    G = [[[s.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                tot = 0
                for d in range(n):
                    tot += s.Rational(1, 2)*ginv[a, d]*(s.diff(g[d, b], coords[c])
                                                       + s.diff(g[d, c], coords[b])
                                                       - s.diff(g[b, c], coords[d]))
                G[a][b][c] = s.simplify(tot)
    Rm = [[[[s.S.Zero]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    t = s.diff(G[a][b][d], coords[c]) - s.diff(G[a][b][c], coords[d])
                    for e in range(n):
                        t += G[a][c][e]*G[e][b][d] - G[a][d][e]*G[e][b][c]
                    Rm[a][b][c][d] = s.simplify(t)
    Ric = s.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = s.simplify(sum(Rm[a][b][a][d] for a in range(n)))
    Rs = s.simplify(sum(ginv[b, d]*Ric[b, d] for b in range(n) for d in range(n)))
    return G, Ric, Rs


# --- 3D check: h_ij = f(r) delta_ij  ->  R3 by generic 3D computation
th, ph = s.symbols('theta phi', real=True)
f = s.Function('f')(r)
h3 = s.diag(f, f*r**2, f*r**2*s.sin(th)**2)
_, Ric3, R3gen = christoffel_riemann(h3, [r, th, ph])
R3form = -2*s.diff(f, r, 2)/f**2 + s.Rational(3, 2)*s.diff(f, r)**2/f**3 - 4*s.diff(f, r)/(r*f**2)
print('R3 formula check:', s.simplify(R3gen - R3form))

# --- 4D Einstein tensor for ds^2 = -N^2 dt^2 + f(dr^2 + r^2 dOmega^2)
N = s.Function('N')(r)
t = s.symbols('t', real=True)
g4 = s.diag(-N**2, f, f*r**2, f*r**2*s.sin(th)**2)
_, Ric4, R4 = christoffel_riemann(g4, [t, r, th, ph])
ginv4 = g4.inv()
# mix-index Einstein tensor G^mu_nu = g^{mu a} (R_{a nu} - 1/2 g_{a nu} R)
Gmix = s.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Gmix[a, b] = s.simplify(sum(ginv4[a, c]*(Ric4[c, b] - s.Rational(1, 2)*g4[c, b]*R4)
                                    for c in range(4)))
for (a, b) in [(0, 0), (1, 1), (2, 2)]:
    print('G^%d_%d =' % (a, b), s.simplify(Gmix[a, b]))
print('G^2_2 - G^3_3 =', s.simplify(Gmix[2, 2] - Gmix[3, 3]))
print('G^1_1 - G^2_2 =', s.simplify(Gmix[1, 1] - Gmix[2, 2]))
saved = (Gmix, R3form)
