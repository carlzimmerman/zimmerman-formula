"""Step 3c: linearised P equation with W -> K p^2/(2f) (leading quadratic)."""
import sympy as sp

r = sp.symbols('r', positive=True)
K, gam, a0 = sp.symbols('K gamma a0', positive=True)
N = sp.Function('N')(r)
f = sp.Function('f')(r)
p = sp.Function('p')(r)


def R3(fe):
    L = sp.log(fe)
    return -(1/fe)*(2*sp.diff(L, r, 2) + 4*sp.diff(L, r)/r + sp.Rational(1, 2)*sp.diff(L, r)**2)


def euler(L, v):
    e = sp.diff(L, v)
    for d in L.atoms(sp.Derivative):
        if d.expr == v:
            n = d.variable_count[0][1]
            e = e + (-1)**n*sp.diff(sp.diff(L, d), r, n)
    return sp.expand(e)


sqh = f**sp.Rational(3, 2)
q = sp.sqrt(f)*p
DP = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)
W2 = K*p**2/(2*f)
clock = p*sp.diff(N, r)/(f*N)
L = r**2*sqh*N*(clock - W2 - (gam/2)*DP**2)
ep = sp.simplify(euler(L, p))
print("p-eq:", sp.collect(ep, [sp.Derivative(p, r, 2), sp.Derivative(p, r), p]))
print()
# compare with  (gamma lap^2 - K) psi  with psi = D.P, expressed for a radial P
psi = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)
# divergence in the physical (orthonormal) sense:  D_i P^i = (1/sqrt h) d_i(sqrt h P^i)
print("psi =", sp.simplify(psi))
