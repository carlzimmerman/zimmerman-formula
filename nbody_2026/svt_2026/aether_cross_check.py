#!/usr/bin/env python3
"""
CROSS-CHECK: allow a GENERAL aether perturbation delta A^i = eps*(ax, ay, az)(t,z) on top of
the TT metric mode, with A^0 fixed EXACTLY by the unit-norm constraint. Show, at O(eps^2):

  (1) F_{mu nu} at O(eps) contains ONLY the alpha's -- no h anywhere;
  (2) sqrt(-g) * F^{mn}F_{mn} at O(eps^2) contains NO h_p, h_x monomial (so the K_B term
      contributes zero dh (and zero h) terms to the TENSOR quadratic action, PROVED, not
      just argued from helicity);
  (3) Q and Y at O(eps^2) contain only alpha^2 -- no h -- so no dark-sector h-coupling is
      generated through the aether either;
  (4) there is NO h-alpha cross term anywhere in the full O(eps^2) Lagrangian
      (helicity-2 x helicity-0/1 decoupling, verified by explicit computation).

Same gauge/conventions as tensor_sector_v7.py.
"""
import sympy as sp
from sympy import Rational, sqrt, pi, Function

t, zz, eps = sp.symbols('t z epsilon', real=True)
x1, x2 = sp.symbols('x y', real=True)
G, Lam, KB = sp.symbols('G Lambda K_B', real=True)
a = Function('a', positive=True)(t)
hp = Function('h_p', real=True)(t, zz)
hx = Function('h_x', real=True)(t, zz)
ax = Function('alpha_x', real=True)(t, zz)
ay = Function('alpha_y', real=True)(t, zz)
az = Function('alpha_z', real=True)(t, zz)
phib = Function('phibar', real=True)(t)
coords = [t, x1, x2, zz]

def trunc(e, n=2):
    e = sp.expand(e)
    p = sp.Poly(e, eps)
    return sum(c*eps**m for (m,), c in p.terms() if m <= n)

h = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
g = sp.zeros(4, 4)
g[0, 0] = -1
for i in range(3):
    for j in range(3):
        g[i+1, j+1] = a**2 * (sp.eye(3)[i, j] + eps*h[i, j])

# unit-norm: g00 (A0)^2 + g_ij A^i A^j = -1  =>  A0 = sqrt(1 + g_ij A^i A^j)  (EXACT)
Avec = [eps*ax, eps*ay, eps*az]
gAA = sp.expand(sum(g[i+1, j+1]*Avec[i]*Avec[j] for i in range(3) for j in range(3)))
A0_exact = sqrt(1 + gAA)
A0 = trunc(sp.series(A0_exact, eps, 0, 3).removeO())
print("A^0 (unit-norm, to O(eps^2)) =", A0)
# NOTE: A0 = 1 + (eps^2/2) a^2 (ax^2+ay^2+az^2) + O(eps^3); h enters A0 only at O(eps^3).

A_up = sp.Matrix([A0, Avec[0], Avec[1], Avec[2]])
norm_check = trunc(sp.expand(sum(g[m, n]*A_up[m]*A_up[n] for m in range(4) for n in range(4))))
print("CHECK: A.A + 1 to O(eps^2) =", sp.simplify(norm_check + 1))
assert sp.simplify(norm_check + 1) == 0

A_dn = sp.Matrix([trunc(sp.expand(sum(g[m, n]*A_up[n] for n in range(4)))) for m in range(4)])

# F_mn = d_m A_n - d_n A_m
F = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        F[m, n] = trunc(sp.expand(sp.diff(A_dn[n], coords[m]) - sp.diff(A_dn[m], coords[n])))

F1 = sp.Matrix(4, 4, lambda m, n: sp.expand(F[m, n]).coeff(eps, 1))
print("\n(1) F_{mu nu} at O(eps):")
hs = [hp, hx]
has_h_in_F1 = any(F1[m, n].has(hp) or F1[m, n].has(hx) for m in range(4) for n in range(4))
print("   nonzero components:", {(m, n): F1[m, n] for m in range(4) for n in range(4) if F1[m, n] != 0})
print("   contains h_p or h_x?", has_h_in_F1)
assert not has_h_in_F1

# (2) full K_B term to O(eps^2)
ginv = g.inv().applyfunc(lambda e: trunc(sp.series(sp.together(e), eps, 0, 3).removeO()))
detg = sp.factor(g.det())
sqrtmg = trunc(sp.series(sqrt(-detg), eps, 0, 3).removeO())
F2scal = 0
for m in range(4):
    for n in range(4):
        for r in range(4):
            for s in range(4):
                if F[m, n] == 0 or ginv[m, r] == 0 or ginv[n, s] == 0:
                    continue
                F2scal += ginv[m, r]*ginv[n, s]*F[m, n]*F[r, s]
F2scal = trunc(sp.expand(F2scal))
L_KB = trunc(sp.expand(-sqrtmg*Rational(1, 2)*KB*F2scal/(16*pi*G)))
L_KB2 = sp.expand(L_KB.coeff(eps, 2))
print("\n(2) K_B-term Lagrangian at O(eps^2):")
print("   L_KB^(2) =", sp.simplify(L_KB2))
print("   contains h_p or h_x (any derivative)?", L_KB2.has(hp) or L_KB2.has(hx))
assert not (L_KB2.has(hp) or L_KB2.has(hx))
# => the K_B F^2 term contributes NOTHING to the tensor sector: no dh terms, no h terms,
#    even with the aether fully perturbed. It is pure vector/scalar-sector kinetic energy.

# (3) Q and Y with the perturbed aether
dphi = sp.Matrix([sp.diff(phib, c) for c in coords])
Q = trunc(sp.expand(sum(A_up[m]*dphi[m] for m in range(4))))
Y = trunc(sp.expand(sum((ginv[m, n] + A_up[m]*A_up[n])*dphi[m]*dphi[n]
                        for m in range(4) for n in range(4))))
print("\n(3) Q to O(eps^2) =", sp.simplify(Q))
print("    Y to O(eps^2) =", sp.simplify(Y))
assert not (sp.expand(Q).has(hp) or sp.expand(Q).has(hx))
assert not (sp.expand(Y).has(hp) or sp.expand(Y).has(hx))
Y2 = sp.expand(Y).coeff(eps, 2)
print("    Y = eps^2 * [", sp.simplify(Y2), "]  -- pure alpha^2, no h; and Y ~ O(eps^2) means")
print("    F_Y(Y/A) ~ (2/3)c (Y/A)^{3/2} ~ O(eps^3) and B(Y/A)u^2 ~ O(eps^2) alpha^2: no h coupling.")

# (4) no h-alpha cross terms in the FULL quadratic Lagrangian (EH part included)
def christoffels(gmat, ginvmat):
    Gam = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            for rho in range(nu, 4):
                s = 0
                for sig in range(4):
                    if ginvmat[mu, sig] == 0:
                        continue
                    s += ginvmat[mu, sig]*(sp.diff(gmat[sig, rho], coords[nu])
                                           + sp.diff(gmat[sig, nu], coords[rho])
                                           - sp.diff(gmat[nu, rho], coords[sig]))
                s = trunc(Rational(1, 2)*s)
                Gam[mu][nu][rho] = s
                Gam[mu][rho][nu] = s
    return Gam

Gam = christoffels(g, ginv)
Ric = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(mu, 4):
        s = 0
        for rho in range(4):
            s += sp.diff(Gam[rho][mu][nu], coords[rho]) - sp.diff(Gam[rho][mu][rho], coords[nu])
            for lamb in range(4):
                s += Gam[rho][rho][lamb]*Gam[lamb][mu][nu] - Gam[rho][nu][lamb]*Gam[lamb][mu][rho]
        Ric[mu, nu] = trunc(sp.expand(s))
        Ric[nu, mu] = Ric[mu, nu]
Rscal = trunc(sp.expand(sum(ginv[mu, nu]*Ric[mu, nu] for mu in range(4) for nu in range(4))))
Kf = Function('Kbg', real=True)(t)
L_full2 = sp.expand((trunc(sqrtmg*(Rscal - 2*Lam)/(16*pi*G)) + L_KB
                     + trunc(sqrtmg*Kf)).coeff(eps, 2))
# collect every monomial that contains BOTH an h and an alpha
cross_terms = 0
for term in sp.Add.make_args(L_full2):
    has_h = term.has(hp) or term.has(hx)
    has_a = term.has(ax) or term.has(ay) or term.has(az)
    if has_h and has_a:
        cross_terms += term
print("\n(4) h-alpha cross terms in the full O(eps^2) Lagrangian (EH + Lambda + K_B F^2 + K):",
      sp.simplify(cross_terms))
assert sp.simplify(cross_terms) == 0
print("\nALL ASSERTIONS PASSED: the tensor quadratic action receives NO contribution from the")
print("aether (K_B) term or the dark sector's derivative couplings, even with delta A^i turned on.")
