#!/usr/bin/env python3
"""Pin the linearised Einstein identities in the conformal gauge.
ds^2 = -(1+2Phi)dt^2 + (1-2Psi)delta_ij dx^i dx^j  (static)
Read: G^0_0, G^i_j - (1/3)delta^i_j G, and the rr component in spherical symmetry.
"""
import sympy as sp

t, x, y, z, r = sp.symbols('t x y z r', real=True)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)

co = [t, x, y, z]
g = sp.Matrix(4, 4, lambda i, j: 0)
g[0, 0] = -(1 + 2*Phi)
for i in (1, 2, 3):
    g[i, i] = 1 - 2*Psi
ginv = sp.simplify(g.inv())

Gam = [[[sp.simplify(sum(ginv[k, l]*(sp.diff(g[l, i], co[j]) + sp.diff(g[l, j], co[i])
                               - sp.diff(g[i, j], co[l]))/2 for l in range(4)))
         for j in range(4)] for i in range(4)] for k in range(4)]

Rm = [[[[sp.simplify(sp.diff(Gam[l][i][j], co[k]) - sp.diff(Gam[l][i][k], co[j])
           + sum(Gam[l][k][m]*Gam[m][i][j] - Gam[l][j][m]*Gam[m][i][k] for m in range(4)))
         for l in range(4)] for j in range(4)] for i in range(4)] for k in range(4)]

Ric = sp.Matrix(4, 4, lambda i, j: sp.simplify(sum(Rm[k][i][k][j] for k in range(4))))
Rs = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(4) for j in range(4)))
Gdown = sp.simplify(Ric - Rs*g/2)

# mixed G^mu_nu at linear order in Phi,Psi
lin = lambda e: sp.series(sp.expand(e), sp.Symbol('eps'), 0, 1).removeO()
eps = sp.Symbol('eps')
sub = {Phi: eps*Phi, Psi: eps*Psi}
Gup = sp.Matrix(4, 4, lambda i, j: sp.simplify(sp.expand(
    sum(ginv[i, k]*Gdown[k, j] for k in range(4)).subs(sub)).coeff(eps, 1)))

lapf = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)
print("G^0_0 =", sp.simplify(Gup[0, 0]))
print("G^0_0 + 2 lap Phi =", sp.simplify(Gup[0, 0] + 2*lapf(Phi)))
print("G^0_0 - 2 lap Psi =", sp.simplify(Gup[0, 0] - 2*lapf(Psi)))

trG = sp.simplify(sum(Gup[i, i] for i in range(1, 4)))
print("\ntrace spatial G^i_i =", sp.simplify(trG))
f = Phi - Psi
print("\nTraceless components:")
for (i, j) in [(1, 1), (2, 2), (1, 2)]:
    lhs = sp.simplify(Gup[i, j] - (sp.Rational(1, 3) if i == j else 0)*trG)
    rhs = sp.simplify(sp.diff(f, co[i], co[j]) - (sp.Rational(1, 3) if i == j else 0)*lapf(f))
    print(f"  ({i}{j}): lhs = {sp.simplify(lhs)}")
    print(f"        diff = {sp.simplify(lhs - rhs)}   ratio lhs/rhs = {sp.simplify(lhs/rhs) if rhs != 0 else 'na'}")

print("\nG^i_i (full trace) vs 2 lap(Phi-Psi):", sp.simplify(trG - 2*lapf(f)))
print("G^0_0 vs -2 lap Psi:", sp.simplify(Gup[0,0] + 2*lapf(Psi)))
print("Ricci scalar R =", sp.simplify(Rs.subs(sub).coeff(eps, 1)))