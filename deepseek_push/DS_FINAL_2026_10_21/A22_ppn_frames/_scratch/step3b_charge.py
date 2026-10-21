"""Step 3b: linearised P equation, exact in N(r), f(r)."""
import sympy as sp

r = sp.symbols('r', positive=True)
K, gam, a0 = sp.symbols('K gamma a0', positive=True)
eps = sp.symbols('eps')
N = sp.Function('N')(r)
f = sp.Function('f')(r)
pf = sp.Function('pf')(r)
p = eps*pf


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
u = K*p/sp.sqrt(f)
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
clock = p*sp.diff(N, r)/(f*N)
L = r**2*sqh*N*(R3(f)/(4*K) + clock - W - (gam/2)*DP**2)

Wser = sp.series(W, eps, 0, 3).removeo()
Llin = sp.expand(r**2*sqh*N*(clock - Wser - (gam/2)*DP**2))
ep = euler(Llin, pf)
ep = sp.simplify(ep.coeff(eps, 1))
print("linear p-eq:")
print(sp.collect(sp.simplify(ep/r**2), [sp.Derivative(pf, r, 2), sp.Derivative(pf, r), pf]))
