#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s2_weakfield_geometry.py -- program section 2 (task part a)
============================================================
Static weak-field geometry of the FROZEN ACTION, everything computed by
sympy from scratch (no coefficients quoted from memory).

Setup (ASSUMED, given by the task):
    T = t (khronon = coordinate time),  N = 1 + Phi/c^2,  N^i = 0,
    h_ij = (1 - 2 Psi/c^2) delta_ij,   all fields static.
    4-metric: ds^2 = -N^2 c^2 dt^2 + h_ij dx^i dx^j   (signature -+++).

DERIVED here (each printed as PASS/FAIL):
  [1] Ricci sign convention check: unit 3-sphere has R_ij = +2 h_ij, R = +6.
  [2] Exact 4D acceleration of u_mu = -grad T/|grad T|:  a_0 = 0,
      a_i = d_i ln N  (exact, static; no weak-field truncation).
  [3] Exact X = c^4 h^{ij} a_i a_j / a0^2
             = |grad Phi|^2 / ( a0^2 (1+Phi/c^2)^2 (1-2 Psi/c^2) );
      leading order X = |grad Phi|^2/a0^2 (corrections relative O(Phi/c^2, Psi/c^2)).
  [4] Linearised (3)R_ij = (1/c^2) ( d_i d_j Psi + delta_ij lap Psi )   <- exact coeffs
  [5] Linearised (3)R    = (4/c^2) lap Psi
  [6] Linearised Rbar_ij = (3)R_ij - (1/3) h_ij (3)R = (1/c^2) S_ij[Psi],
      S_ij[f] = d_i d_j f - (1/3) delta_ij lap f     (trace-free Hessian)
  [7] Y = c^8 Rbar_ij Rbar^ij / a0^4 ->  (c^4/a0^4) S_ij[Psi] S_ij[Psi]  at leading order.

KEY STRUCTURAL FACT (established by [3] vs [6]): X is built from the LAPSE
potential Phi only; Y is built from the SPATIAL potential Psi only.
"""
import sympy as sp

# ----------------------------------------------------------------------
t, x, y, z = sp.symbols('t x y z', real=True)
c, a0, eps = sp.symbols('c a_0 varepsilon', positive=True)
V = (x, y, z)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)

def grad(f):  return [sp.diff(f, v) for v in V]
def lap(f):   return sum(sp.diff(f, v, 2) for v in V)

def christoffel(g, coords):
    n = len(coords); ginv = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(b, n):
                e = sum(ginv[a, s] * (sp.diff(g[s, b], coords[d])
                                      + sp.diff(g[s, d], coords[b])
                                      - sp.diff(g[b, d], coords[s]))
                        for s in range(n)) / 2
                e = sp.simplify(e)
                Gam[a][b][d] = e
                Gam[a][d][b] = e
    return Gam

def ricci(g, coords):
    """R_bd = d_a Gam^a_bd - d_d Gam^a_ab + Gam^a_al Gam^l_bd - Gam^a_dl Gam^l_ab"""
    n = len(coords); Gam = christoffel(g, coords)
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(b, n):
            expr = sp.S(0)
            for a in range(n):
                expr += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][a][b], coords[d])
                for l in range(n):
                    expr += Gam[a][a][l] * Gam[l][b][d] - Gam[a][d][l] * Gam[l][a][b]
            Ric[b, d] = sp.simplify(expr); Ric[d, b] = Ric[b, d]
    return Ric

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name)

def is_zero(e):
    e = sp.expand(e)
    if e == 0: return True
    e = sp.simplify(e)
    return e == 0 or (hasattr(e, 'equals') and e.equals(0))

# ----------------------------------------------------------------------
# [1] convention check: unit 3-sphere
p, q, r = sp.symbols('p q r', positive=True)
gS3 = sp.diag(1, sp.sin(p)**2, sp.sin(p)**2 * sp.sin(q)**2)
RicS3 = ricci(gS3, (p, q, r))
ok1 = all(is_zero(RicS3[i, j] - 2 * gS3[i, j]) for i in range(3) for j in range(3))
RS3 = sp.simplify(sum((gS3.inv())[i, i] * RicS3[i, i] for i in range(3)))
ok1 = ok1 and is_zero(RS3 - 6)
check('[1] unit 3-sphere: R_ij = 2 h_ij and R = 6 (sign convention fixed)', ok1)

# ----------------------------------------------------------------------
# [2] exact 4D acceleration.  x^0 = t, g_00 = -N^2 c^2.
N  = 1 + Phi / c**2
W  = 1 - 2 * Psi / c**2
g4 = sp.diag(-N**2 * c**2, W, W, W)
coords4 = (t, x, y, z)
g4inv = g4.inv()

# u_mu = - d_mu T / sqrt(- g^{ab} d_a T d_b T),  T = t  ->  d_mu T = delta_mu^0
normT2 = -g4inv[0, 0]                       # = 1/(N^2 c^2) > 0
u_lo = [-1 / sp.sqrt(normT2), 0, 0, 0]      # u_0 = -N c
u_up = [sp.simplify(sum(g4inv[m, n_] * u_lo[n_] for n_ in range(4))) for m in range(4)]
ok_norm = is_zero(sum(u_up[m] * u_lo[m] for m in range(4)) + 1)

Gam4 = christoffel(g4, coords4)
a_lo = []
for m in range(4):
    expr = sp.S(0)
    for n_ in range(4):
        expr += u_up[n_] * (sp.diff(u_lo[m], coords4[n_])
                            - sum(Gam4[l][n_][m] * u_lo[l] for l in range(4)))
    a_lo.append(sp.simplify(expr))

ok2 = ok_norm and is_zero(a_lo[0]) and all(
    is_zero(a_lo[1 + i] - sp.diff(sp.log(N), V[i])) for i in range(3))
check('[2] u.u = -1,  a_0 = 0,  a_i = d_i ln N  (EXACT)', ok2)

# ----------------------------------------------------------------------
# [3] exact X
X_exact = sp.simplify(c**4 / a0**2 * sum(a_lo[1 + i]**2 for i in range(3)) / W)
gradPhi2 = sum(gi**2 for gi in grad(Phi))
X_closed = gradPhi2 / (a0**2 * (1 + Phi / c**2)**2 * (1 - 2 * Psi / c**2))
ok3 = is_zero(X_exact - X_closed)
check('[3] X_exact = |grad Phi|^2 / (a0^2 (1+Phi/c^2)^2 (1-2Psi/c^2))', ok3)

# leading order in field amplitude (Phi -> eps Phi, Psi -> eps Psi, X = O(eps^2) exactly |gradPhi|^2/a0^2)
Xe = X_exact.subs([(Phi, eps * Phi), (Psi, eps * Psi)]).doit()
X_lead = sp.expand(sp.diff(Xe, eps, 2).subs(eps, 0) / 2)
ok3b = is_zero(X_lead - gradPhi2 / a0**2)
check('[3b] leading-order X = |grad Phi|^2 / a0^2', ok3b)

# ----------------------------------------------------------------------
# exact 3D Ricci of h_ij = W delta_ij, then linearise
h3 = sp.diag(W, W, W)
Ric3 = ricci(h3, V)
R3 = sp.simplify(sum(Ric3[i, i] for i in range(3)) / W)   # h^{ij} = delta^{ij}/W

def lin(e):
    es = e.subs(Psi, eps * Psi).doit()
    return sp.expand(sp.diff(es, eps).subs(eps, 0))

# [4]
delta = sp.eye(3)
ok4 = True
for i in range(3):
    for j in range(3):
        target = (sp.diff(Psi, V[i], V[j]) + delta[i, j] * lap(Psi)) / c**2
        ok4 = ok4 and is_zero(lin(Ric3[i, j]) - target)
check('[4] linearised (3)R_ij = (1/c^2)(d_i d_j Psi + delta_ij lap Psi)', ok4)

# [5]
ok5 = is_zero(lin(R3) - 4 * lap(Psi) / c**2)
check('[5] linearised (3)R = (4/c^2) lap Psi', ok5)

# [6]
def S_ij(f, i, j):
    return sp.diff(f, V[i], V[j]) - delta[i, j] * lap(f) / 3

ok6 = True
for i in range(3):
    for j in range(3):
        Rbar_ij = Ric3[i, j] - h3[i, j] * R3 / 3
        ok6 = ok6 and is_zero(lin(Rbar_ij) - S_ij(Psi, i, j) / c**2)
check('[6] linearised Rbar_ij = (1/c^2) S_ij[Psi]  (trace-free Hessian of Psi)', ok6)

# ----------------------------------------------------------------------
# [7] Y at leading order.  Rbar^ij = h^{ik} h^{jl} Rbar_kl = Rbar_ij / W^2
Y_exact = c**8 / a0**4 * sum((Ric3[i, j] - h3[i, j] * R3 / 3)**2
                             for i in range(3) for j in range(3)) / W**2
Ye = Y_exact.subs(Psi, eps * Psi).doit()
Y_lead = sp.expand(sp.diff(Ye, eps, 2).subs(eps, 0) / 2)
Y_target = c**4 / a0**4 * sum(S_ij(Psi, i, j)**2 for i in range(3) for j in range(3))
ok7 = is_zero(Y_lead - Y_target)
check('[7] leading-order Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi]', ok7)

# ----------------------------------------------------------------------
print()
print('STRUCTURAL FACT (derived): X depends on Phi ONLY (lapse sector);')
print('Y depends on Psi ONLY (spatial-curvature sector), at leading order.')
n_fail = sum(1 for _, ok in results if not ok)
print()
print('%d checks, %d failed' % (len(results), n_fail))
raise SystemExit(1 if n_fail else 0)
