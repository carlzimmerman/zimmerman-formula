#!/usr/bin/env python3
"""Scratch 1: LINEARIZED Einstein tensor, static, Newtonian gauge.
Robust: build g(eps) = eta + eps*h, take d/deps at eps=0 (no series)."""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
co = [t, x, y, z]
Psi0 = sp.Function('Psi')(x, y, z)
Phi0 = sp.Function('Phi')(x, y, z)
eps = sp.symbols('eps')

eta = sp.Matrix(sp.diag(-1, 1, 1, 1))
hh = sp.zeros(4, 4)
hh[0, 0] = -2*Psi0
for i in (1, 2, 3):
    hh[i, i] = -2*Phi0
g = sp.Matrix(4, 4, lambda a, b: eta[a, b] + eps*hh[a, b])
ginv = sp.simplify(g.inv())

n = 4
Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            s = 0
            for dd in range(n):
                s += ginv[a, dd]*(sp.diff(g[dd, b], co[c]) + sp.diff(g[dd, c], co[b])
                                  - sp.diff(g[b, c], co[dd]))
            Gam[a][b][c] = s/2

Ric = sp.Matrix(n, n, lambda a, b: 0)
for a in range(n):
    for b in range(n):
        s = 0
        for c in range(n):
            s += sp.diff(Gam[c][a][b], co[c]) - sp.diff(Gam[c][a][c], co[b])
            for dd in range(n):
                s += Gam[c][c][dd]*Gam[dd][a][b] - Gam[c][b][dd]*Gam[dd][a][c]
        Ric[a, b] = s
Rs = sum(ginv[a, b]*Ric[a, b] for a in range(n) for b in range(n))
Ein = sp.Matrix(n, n, lambda a, b: Ric[a, b] - sp.Rational(1, 2)*g[a, b]*Rs)


def lin(e):
    return sp.simplify(sp.diff(e, eps).subs(eps, 0))

lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)
Gup = sp.Matrix(n, n, lambda a, b: 0)
for a in range(n):
    for b in range(n):
        Gup[a, b] = lin(Ein[a, b]*ginv[b, b]) if a == b else lin(Ein[a, b])

print("G^t_t =", sp.simplify(Gup[0, 0]))
print("G^t_t - 2 laps(Phi) =", sp.simplify(Gup[0, 0] - 2*lap(Phi0)))
print("G^t_t - 2 laps(Psi) =", sp.simplify(Gup[0, 0] - 2*lap(Psi0)))
tr = sp.simplify(sum(Gup[i, i] for i in (1, 2, 3)))
print("\ntrace G^i_i =", tr)
print("trace - 2 lap(Psi - 2 Phi) =", sp.simplify(tr - 2*lap(Psi0 - 2*Phi0)))
for (i, j) in [(1, 1), (1, 2)]:
    got = sp.simplify(Gup[i, j] - (sp.Rational(1, 3) if i == j else 0)*tr)
    print(f"\nG^{i}_{j} - (1/3)delta*tr =", got)
print("\ncand -(2/3)(d_x^2 - lap)(Phi-Psi):",
      sp.simplify(-sp.Rational(2, 3)*(sp.diff(Phi0-Psi0, x, 2) - lap(Phi0-Psi0))))
print("cand -(2/3)(d_x^2 - lap)(Phi+Psi):",
      sp.simplify(-sp.Rational(2, 3)*(sp.diff(Phi0+Psi0, x, 2) - lap(Phi0+Psi0))))
print("\nG^1_2 =", sp.simplify(Gup[1, 2]))
print("-(2/3)d_xd_y(Phi-Psi) =", sp.simplify(-sp.Rational(2, 3)*sp.diff(Phi0-Psi0, x, y)))
print("-(2/3)d_xd_y(Phi+Psi) =", sp.simplify(-sp.Rational(2, 3)*sp.diff(Phi0+Psi0, x, y)))
