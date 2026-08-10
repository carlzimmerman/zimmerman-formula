#!/usr/bin/env python3
"""
ADVERSARIAL EXTENSION: the AeST action (SZ2021) also contains aether-scalar terms of the
form  cJ * J^mu grad_mu phi  (J_mu = A^nu nabla_nu A_mu; AeST coefficient 2(2-K_B)) and
cY * Y  (AeST coefficient -(2-K_B)).  Neither tensor_sector_v7.py nor aether_cross_check.py
includes them.  In the PURE tensor sector both vanish exactly (adversarial_verify.py).
Here: with the general aether perturbation delta A^i = eps*alpha^i(t,z) ON, do these terms
generate any h-alpha cross coupling at O(eps^2)?  (If yes, claim 5's 'complete Lagrangian,
zero cross terms' is refuted for full AeST.)
"""
import sympy as sp
from sympy import sqrt, pi, Function, Rational

t, zz, eps = sp.symbols('t z epsilon', real=True)
x1, x2 = sp.symbols('x1 x2', real=True)
G, cJ, cY = sp.symbols('G c_J c_Y', real=True)
a = Function('a', positive=True)(t)
hp = Function('hp', real=True)(t, zz)
hx = Function('hx', real=True)(t, zz)
ax = Function('alpha_x', real=True)(t, zz)
ay = Function('alpha_y', real=True)(t, zz)
az = Function('alpha_z', real=True)(t, zz)
phib = Function('phibar', real=True)(t)
coords = [t, x1, x2, zz]

def trunc(e, n=2):
    e = sp.expand(e)
    return sum(c*eps**m for (m,), c in sp.Poly(e, eps).terms() if m <= n)

h = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
g = sp.zeros(4, 4); g[0, 0] = -1
for i in range(3):
    for j in range(3):
        g[i+1, j+1] = a**2 * ((1 if i == j else 0) + eps*h[i, j])
ginv = g.inv().applyfunc(lambda e: trunc(sp.series(sp.together(e), eps, 0, 3).removeO()))
detg = sp.factor(g.det())
sqrtmg = trunc(sp.series(sqrt(-detg), eps, 0, 3).removeO())

Avec = [eps*ax, eps*ay, eps*az]
gAA = sp.expand(sum(g[i+1, j+1]*Avec[i]*Avec[j] for i in range(3) for j in range(3)))
A0 = trunc(sp.series(sqrt(1 + gAA), eps, 0, 3).removeO())
A_up = sp.Matrix([A0, *Avec])
A_dn = sp.Matrix([trunc(sp.expand(sum(g[m, n]*A_up[n] for n in range(4)))) for m in range(4)])

# Christoffels to O(eps^2)
Gam = [[[0]*4 for _ in range(4)] for _ in range(4)]
for mu in range(4):
    for nu in range(4):
        for rho in range(nu, 4):
            s = 0
            for sig in range(4):
                if ginv[mu, sig] == 0:
                    continue
                s += ginv[mu, sig]*(sp.diff(g[sig, rho], coords[nu])
                                    + sp.diff(g[sig, nu], coords[rho])
                                    - sp.diff(g[nu, rho], coords[sig]))
            s = trunc(Rational(1, 2)*s)
            Gam[mu][nu][rho] = s
            Gam[mu][rho][nu] = s

# J^mu = A^nu nabla_nu A^mu = A^nu (d_nu A^mu + Gamma^mu_{nu lam} A^lam)
Jup = []
for mu in range(4):
    s = 0
    for nu in range(4):
        s += A_up[nu]*sp.diff(A_up[mu], coords[nu])
        for lamb in range(4):
            s += A_up[nu]*Gam[mu][nu][lamb]*A_up[lamb]
    Jup.append(trunc(sp.expand(s)))

JdPhi = trunc(sp.expand(sum(Jup[m]*sp.diff(phib, coords[m]) for m in range(4))))
Y = trunc(sp.expand(sum((ginv[m, n] + A_up[m]*A_up[n])*sp.diff(phib, coords[m])*sp.diff(phib, coords[n])
                        for m in range(4) for n in range(4))))

L_extra = trunc(sp.expand(sqrtmg*(cJ*JdPhi + cY*Y)/(16*pi*G)))
L2 = sp.expand(L_extra.coeff(eps, 2))

cross = 0
alpha_only = 0
for term in sp.Add.make_args(L2):
    has_h = term.has(hp) or term.has(hx)
    has_a = term.has(ax) or term.has(ay) or term.has(az)
    if has_h and has_a:
        cross += term
    if has_h and not has_a:
        # pure-h contribution from the omitted terms would ALSO refute the tensor result
        alpha_only += 0
        cross += term
print("O(eps^2) of the OMITTED AeST terms [cJ*J.gradphi + cY*Y]:")
print("  full L2_extra =", sp.simplify(L2))
print("  h-alpha cross terms + pure-h terms:", sp.simplify(cross))
assert sp.simplify(cross) == 0
print("PASSED: the omitted AeST aether-scalar terms generate NO h coupling at O(eps^2),")
print("        for ANY coefficients cJ, cY -- claims 5 and 9-11 are safe against the omission.")
