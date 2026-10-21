"""Step 3: the static P sector in the linear regime (r << lambda).

Derive, from the exact reduced Euler-Lagrange equations, the two scalar equations
  lap^2 Phi = K(rho - psi),   (gamma lap^2 - K) psi = -lap^2 lnN,     psi = D.P
then solve for a point mass in Fourier space and in position space, and extract
  (a) the 1/r coefficient (G renormalisation),
  (b) the constant-force (r-linear) coefficient,
  (c) the w^2 dependence of both.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
K, gam, a0, mu = sp.symbols('K gamma a0 mu', positive=True)
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
u = K*p/sp.sqrt(f)
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
clock = p*sp.diff(N, r)/(f*N)
L = r**2*sqh*N*(R3(f)/(4*K) + clock - W - (gam/2)*DP**2)

# p equation, linearised in p (u<<a0 => W ~ K p^2/(2f))
ep = euler(L, p)
ep_lin = sp.series(ep, p, 0, 2).removeo()
ep_lin = sp.expand(ep_lin.subs({sp.Derivative(p, r, 2): sp.Symbol('pp'), sp.Derivative(p, r): sp.Symbol('p1'), p: sp.Symbol('p0')}))
print("p-eq (linear, generic N,f):")
print(sp.simplify(ep_lin))
