#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s4_numeric_spotcheck.py -- high-precision random-point corroboration of the
two heavy identities of s4_exact_variation_fast.py:

  [4d] EL of L_eps = -(a0^2/8piG) eps A(X) Y  equals
        dPhi:  (eps/4piG) div( A'(X) Y grad Phi )
        dPsi: -(eps c^4/(4piG a0^2)) d_i d_j ( A(X) S_ij[Psi] )
  [8]  the O(eps) elimination identity (schematic recovery, on-shell)

Method: build both sides symbolically with sympy (exact Euler-Lagrange via
euler_equations, i.e. the same objects as the symbolic script), then evaluate
the DIFFERENCE at random rational points for every independent derivative
atom, with 60-digit arithmetic, N trials.  A nonzero identity would show up
at O(1); agreement to <1e-40 across all trials at random points is decisive
for a rational-radical identity.  This corroborates, and is superseded by,
the fully symbolic check in s4_exact_variation_fast.py.
"""
import random
import sympy as sp
from sympy.calculus.euler import euler_equations

random.seed(20260822)

x, y, z = sp.symbols('x y z', real=True)
c, a0, G, etaK, epsl = sp.symbols('c a_0 G eta_K epsilon', positive=True)
V = (x, y, z)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)
chi = sp.Function('chi')(x, y, z)
rho = sp.Function('rho')(x, y, z)
delta = sp.eye(3)

def grad(f):  return [sp.diff(f, v) for v in V]
def lap(f):   return sum(sp.diff(f, v, 2) for v in V)
def div(vec): return sum(sp.diff(vec[i], V[i]) for i in range(3))
def S_ij(f, i, j): return sp.diff(f, V[i], V[j]) - delta[i, j] * lap(f) / 3

def EL(L, funcs):
    out = []
    for f in funcs:
        if not L.has(f):
            out.append(sp.S(0)); continue
        qs = euler_equations(L, [f], V)
        out.append(qs[0].lhs - qs[0].rhs if qs else sp.S(0))
    return out

gP = grad(Phi)
X  = sum(gi**2 for gi in gP) / a0**2
xs = sp.sqrt(X)
FX = -1 / (1 + xs)
Afun = X**2 / (1 + X)**4
Ap   = 2 * X * (1 - X) / (1 + X)**5
Y  = c**4 / a0**4 * sum(S_ij(Psi, i, j)**2 for i in range(3) for j in range(3))
L_Fe = -(a0**2 / (8 * sp.pi * G)) * epsl * Afun * Y

print('... building EL of the eps A(X) Y term', flush=True)
q = EL(L_Fe, [Phi, Psi])
tidal = sum(sp.diff(Afun * S_ij(Psi, i, j), V[i], V[j])
            for i in range(3) for j in range(3))
d_phi = sp.expand(q[0] - (epsl / (4 * sp.pi * G)) * div([Ap * Y * gP[i] for i in range(3)]))
d_psi = sp.expand(q[1] + (epsl * c**4 / (4 * sp.pi * G * a0**2)) * tidal)

print('... building the elimination difference', flush=True)
target_phi = (lap(Psi) + div([(FX - etaK / 2 + epsl * Ap * Y) * gP[i]
                              for i in range(3)])) / (4 * sp.pi * G) - rho
target_psi = -(lap(Psi) - lap(Phi) + (epsl * c**4 / a0**2) * tidal) / (4 * sp.pi * G)
elphi_sub = target_phi.subs(Psi, Phi + epsl * chi).doit()
elpsi_sub = target_psi.subs(Psi, Phi + epsl * chi).doit()

def coeff_eps(expr, k):
    return sp.diff(expr, epsl, k).subs(epsl, 0) / sp.factorial(k)

YPhi = c**4 / a0**4 * sum(S_ij(Phi, i, j)**2 for i in range(3) for j in range(3))
tidalPhi = sum(sp.diff(Afun * S_ij(Phi, i, j), V[i], V[j])
               for i in range(3) for j in range(3))
schematic = div([(1 - etaK / 2 + FX + epsl * Ap * YPhi) * gP[i] for i in range(3)]) \
            - (epsl * c**4 / a0**2) * tidalPhi - 4 * sp.pi * G * rho
d_expr = 4 * sp.pi * G * elphi_sub - schematic
d8_0 = coeff_eps(d_expr, 0)
d8_1 = sp.expand(coeff_eps(d_expr, 1) + 4 * sp.pi * G * coeff_eps(elpsi_sub, 1))

names = {'[4d] dPhi': d_phi, '[4d] dPsi': d_psi,
         '[8] O(1)': d8_0, '[8] O(eps)': d8_1}
n_fail = 0
for name, expr in names.items():
    atoms = sorted(expr.atoms(sp.Derivative), key=sp.default_sort_key)
    funcs = sorted((a for a in expr.atoms(sp.Function)
                    if a.func in (sp.Function('Phi'), sp.Function('Psi'),
                                  sp.Function('chi'), sp.Function('rho'))),
                   key=sp.default_sort_key)
    worst = 0
    for trial in range(6):
        sub = {}
        for a_ in atoms:
            sub[a_] = sp.Rational(random.randint(-40, 40), random.randint(1, 9))
        for f_ in funcs:
            sub[f_] = sp.Rational(random.randint(-40, 40), random.randint(1, 9))
        sub.update({c: sp.Rational(7, 2), a0: sp.Rational(3, 5),
                    G: sp.Rational(2, 3), etaK: sp.Rational(1, 4),
                    epsl: sp.Rational(1, 10)})
        val = expr.xreplace(sub)
        val = abs(sp.N(val, 60))
        worst = max(worst, float(val))
    ok = worst < 1e-40
    n_fail += (not ok)
    print(('PASS' if ok else 'FAIL'), '--', name, 'worst |diff| =', worst, flush=True)

print('%d failed' % n_fail)
raise SystemExit(1 if n_fail else 0)
