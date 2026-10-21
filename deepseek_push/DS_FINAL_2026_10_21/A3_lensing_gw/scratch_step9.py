#!/usr/bin/env python3
"""Step 9: independent check of the second-order shear source.
Compare (a) Ef2 from the action with (b) the exact G^r_r-G^theta_theta expanded
to second order, for the vacuum case."""
import sympy as s

r = s.symbols('r', positive=True)
K, gamma = s.symbols('K gamma', positive=True)
n1 = s.Function('n1')(r); h1 = s.Function('h1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r)
eps = s.symbols('eps', positive=True)


def kk(e):
    e = s.expand(e)
    ser = s.series(e, eps, 0, 3).removeO()
    return s.expand(s.expand(ser).coeff(eps, 1)), s.expand(s.expand(ser).coeff(eps, 2))


N = 1 + eps*n1 + eps**2*n2
f = 1 + eps*h1 + eps**2*h2
G11 = (-s.diff(f, r, 2)/(2*f**2) + 3*s.diff(f, r)**2/(4*f**3)
       - s.diff(N, r, 2)/(N*f) + s.diff(N, r)*s.diff(f, r)/(N*f**2)
       + s.diff(f, r)/(2*r*f**2) + s.diff(N, r)/(r*N*f))
g1, g2 = kk(G11)
print('O(eps) G11  :', s.factor(s.simplify(g1*4)))
print('\nO(eps^2) G11:', s.factor(s.expand(4*g2)))
