#!/usr/bin/env python3
"""Step 6: isolate the O(eps^2) slip equation from Ef2."""
import sympy as s, pickle

r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0, Lam = s.symbols('K beta eta gamma a0 Lambda', positive=True)
n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); p1 = s.Function('p1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r); p2 = s.Function('p2')(r)
d = pickle.load(open('scratch_step5.pkl', 'rb'))
Ef2 = s.sympify(d[('Ef', 2)]) * K
Ef2 = s.expand(Ef2 * 4)          # clear the 1/4
S2 = n2 + h2/2
lin = s.expand(Ef2.subs({p1: 0, rho: s.Symbol('rho1')*0}))
# split linear-in-second-order from quadratic
linpart = s.expand(lin.subs({n1: 0, h1: 0}))
quad = s.expand(Ef2 - linpart)
print('linear part :', s.factor(linpart))
print()
print('quadratic in (n1,h1,p1):', s.factor(quad))
