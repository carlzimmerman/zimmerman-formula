#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hostile_attack3_dof_scalar_2026.py -- HOSTILE REFEREE, ATTACK 3
================================================================
Question under attack: does the Rbar_ij Rbar^ij (Y) sector of the frozen
non-projectable action add an extra propagating mode, given that the lapse
equation changes?  And are the [hamiltonian-dof]/[gw-sector] finite-X0
scalar results reproducible independently?

Method (own code, not shared with sec10/sec12): full scalar-sector
quadratic Lagrangian on a frozen constant-acceleration background
(a_i = a delta_i3, flat slices, N = 1 locally, coefficients frozen --
the same eikonal setting phase-1 used, so this attacks their derivation
on its own declared terms):

    N = 1 + p phi,  N_i = p d_i B,  h_ij = (1 - 2 p psi) delta_ij,
    fields (t, x1, x3);  p = perturbative bookkeeping.

Every ingredient below is expanded to O(p^2) by sympy from the frozen
action's bracket  (3)R + K_ij K^ij - lam K^2 + eta a_i a^i - 2 F(X,Y),
with F(X) kept as symbols FX, FXX at X0 = a^2 (frozen values substituted
at the end) and the Y-term entering as -2 epsA * S_ij[psi] S_ij[psi]
(A(X0) = epsA/eps; background Rbar = 0 on flat slices so Y is purely
quadratic -- DERIVED in attack 1/2 scripts).

CHECKS:
  [D1] the quadratic Lagrangian contains NO time derivative of phi and NO
       time derivative of B (lapse + shift stay non-dynamical even with
       the Y-term switched on and the lapse equation modified);
  [D2] the phi row of the Fourier system carries no omega at all
       (the modified lapse equation is elliptic, it DETERMINES phi);
  [D3] det M(omega, k) is a polynomial in omega^2 of degree EXACTLY 1
       (times k-factors) -- one scalar branch, with AND without the
       Y-term: NO extra mode, no Ostrogradsky doubling from Rbar^2;
  [D4] the Y-term enters only the psi-psi entry, as spatial k^4;
  [D5] dispersion, k || a, eta = 0, frozen F:  c_par^2 = x(x+2)(lam-1)/(3lam-1);
  [D6] dispersion, k perp a, eta = 0, frozen F: c_perp^2 = x(lam-1)/(3lam-1);
  [D7] a -> 0 limit, generic eta: c_s^2 = (lam-1)(2-alpha)/(alpha(3lam-1))
       with alpha = eta + 2 (the BPS khronometric formula with the F-term's
       F_X(0) = -1 generating the full-strength a^2 coupling);
  [D8] O(epsA) shift of omega^2 at large k equals
       + 2 epsA k^4 (lam-1)/(3(3lam-1))   [the claimed scalar k^4 term];
  [D9] eta != 0 instability structure: with eta > 0 the deep-MOND limit has
       c_par^2 < 0 below s_c = sqrt(2/(2-eta)) - 1  (gradient instability),
       reproduced from the SAME determinant.
"""
import sympy as sp
import sys

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
C = (t, x1, x2, x3)
V = (x1, x2, x3)
p = sp.symbols('p', positive=True)                     # perturbation bookkeeping
a, lam, eta, epsA = sp.symbols('a lambda_K eta_K epsilonA', real=True)
FX, FXX = sp.symbols('F_X F_XX', real=True)
w, k1, k3, K = sp.symbols('omega k_1 k_3 K', real=True)

phi = sp.Function('phi')(t, x1, x3)
B   = sp.Function('B')(t, x1, x3)
psi = sp.Function('psi')(t, x1, x3)

npass = nfail = 0
def check(name, cond):
    global npass, nfail
    if cond: npass += 1
    else: nfail += 1
    print(('PASS' if cond else 'FAIL'), '--', name); sys.stdout.flush()

def lap3(f): return sum(sp.diff(f, v, 2) for v in V)

def o2(expr):
    """order-p^2 coefficient"""
    return sp.expand(sp.series(sp.expand(expr), p, 0, 3).removeO()).coeff(p, 2)

# ---------------- ingredient 1: N sqrt(h) (3)R to O(p^2)  (own Ricci code)
h3 = sp.diag(1-2*p*psi, 1-2*p*psi, 1-2*p*psi)
h3i = h3.inv()
Gam3 = [[[0]*3 for _ in range(3)] for _ in range(3)]
for A_ in range(3):
    for b in range(3):
        for c_ in range(b, 3):
            s = sum(h3i[A_, m]*(sp.diff(h3[m, b], V[c_]) + sp.diff(h3[m, c_], V[b])
                                - sp.diff(h3[b, c_], V[m])) for m in range(3))/2
            Gam3[A_][b][c_] = Gam3[A_][c_][b] = sp.together(s)
Ric3 = sp.zeros(3, 3)
for b in range(3):
    for d in range(b, 3):
        expr = 0
        for A_ in range(3):
            expr += sp.diff(Gam3[A_][b][d], V[A_]) - sp.diff(Gam3[A_][A_][b], V[d])
            for l in range(3):
                expr += Gam3[A_][A_][l]*Gam3[l][b][d] - Gam3[A_][d][l]*Gam3[l][A_][b]
        Ric3[b, d] = Ric3[d, b] = sp.together(expr)
R3s = sp.together(sum(h3i[i, i]*Ric3[i, i] for i in range(3)))
Nlapse = 1 + p*phi
dens_R3 = o2(Nlapse*sp.sqrt(sp.together(h3.det()))*R3s)
print('  ... (3)R block expanded')

# ---------------- ingredient 2: kinetic sector (K starts at O(p))
Kij = sp.Matrix(3, 3, lambda i, j:
                -sp.diff(psi, t)*(1 if i == j else 0)
                - sp.diff(B, V[i], V[j]))
trK = sum(Kij[i, i] for i in range(3))
dens_K = sp.expand(sum(Kij[i, j]**2 for i in range(3) for j in range(3)) - lam*trK**2)

# ---------------- ingredient 3: eta a^2 and -2F(X) sectors on the frozen background
# acceleration field: a_i = d_i ln N + background a n_i, n = e_3
ai = [p*sp.diff(phi, V[i])/(1+p*phi) + (a if i == 2 else 0) for i in range(3)]
hup = [[sp.together(h3i[i, j]) for j in range(3)] for i in range(3)]
Xg = sum(hup[i][j]*ai[i]*ai[j] for i in range(3) for j in range(3))
dX = sp.expand(sp.series(sp.expand(Xg - a**2), p, 0, 3).removeO())
Fexp = FX*dX + sp.Rational(1, 2)*FXX*dX**2          # F(X0) constant dropped
meas = Nlapse*sp.sqrt(sp.together(h3.det()))
dens_Feta = o2(meas*(eta*Xg - 2*Fexp))
print('  ... F/eta block expanded')

# ---------------- ingredient 4: Y sector.  Background Rbar = 0 (flat slices),
# linear Rbar_ij = S_ij[psi] (derived in attack1/attack2)  ->  quadratic term:
Spsi = sp.Matrix(3, 3, lambda i, j: sp.diff(psi, V[i], V[j])
                 - (lap3(psi)/3 if i == j else 0))
dens_Y = -2*epsA*sum(Spsi[i, j]**2 for i in range(3) for j in range(3))

L2 = sp.expand(dens_R3 + dens_K + dens_Feta + dens_Y)

# ---------------- [D1] no phi-dot, no B-dot anywhere in L2
def has_tderiv(expr, f):
    for D in expr.atoms(sp.Derivative):
        if D.expr == f and any(v == t for v, n in D.variable_count):
            return True
    return False
check('[D1] L2 has NO d_t phi and NO d_t B (lapse+shift non-dynamical '
      'even with the Y-term on)', (not has_tderiv(L2, phi)) and (not has_tderiv(L2, B)))

# ---------------- Euler-Lagrange + plane waves
def EL(L, f):
    res = sp.diff(L, f)
    for D in L.atoms(sp.Derivative):
        if D.expr == f:
            vs = []
            for v_, n in D.variable_count:
                vs += [v_]*int(n)
            res = res + sp.Integer(-1)**len(vs)*sp.diff(sp.diff(L, D), *vs)
    return res

Aphi, AB, Apsi = sp.symbols('A_phi A_B A_psi')
E = sp.exp(sp.I*(k1*x1 + k3*x3 - w*t))
pw = {phi: Aphi*E, B: AB*E, psi: Apsi*E}

rows = []
for f in (phi, B, psi):
    r = EL(L2, f).subs(pw, simultaneous=True).doit()
    r = sp.expand(sp.simplify(r/E))
    rows.append(r)
M = sp.Matrix(3, 3, lambda i, j: rows[i].coeff([Aphi, AB, Apsi][j]))
print('  ... Fourier matrix built')

# ---------------- [D2] phi row omega-free
check('[D2] the phi row (modified lapse equation) carries NO omega: it '
      'DETERMINES phi, it does not propagate it',
      all(not sp.expand(M[0, j]).has(w) for j in range(3)))

# ---------------- [D3] det M: degree in omega^2 with and without Y
detM = sp.expand(M.det())
polw = sp.Poly(detM, w)
degw = polw.degree()
detM0 = sp.expand(detM.subs(epsA, 0))
degw0 = sp.Poly(detM0, w).degree()
odd_absent = all(sp.expand(polw.coeff_monomial(w**d)) == 0 for d in (1, 3) if d <= degw)
check('[D3] det M is degree 2 in omega (ONE scalar branch), odd powers absent, '
      'same degree with and without the Y-term: NO extra mode from Rbar^2',
      degw == 2 and degw0 == 2 and odd_absent)

# ---------------- [D4] Y enters only psi-psi, as spatial k^4
occurs = [(i, j) for i in range(3) for j in range(3)
          if sp.expand(M[i, j]).has(epsA)]
Mpp_eps = sp.expand(M[2, 2]).coeff(epsA)
check('[D4] the Y-term enters ONLY the psi-psi entry, as spatial k^4 '
      '(EL coefficient -(8/3)(k1^2+k3^2)^2), no omega attached',
      occurs == [(2, 2)] and sp.simplify(Mpp_eps + sp.Rational(8, 3)*(k1**2+k3**2)**2) == 0
      and not Mpp_eps.has(w))

# ---------------- dispersion: solve det = 0 for omega^2
w2 = sp.symbols('w2')
det_w2 = detM.subs(w**2, w2)
c1 = sp.expand(det_w2).coeff(w2, 1)
c0 = sp.expand(det_w2).coeff(w2, 0)
omega2 = sp.simplify(-c0/c1)

frozen = {FX: -1/(1+a), FXX: 1/(2*a*(1+a)**2)}

# [D5] k || a  (k1 = 0), eta = 0, epsA = 0, large-k leading
om_par = omega2.subs({k1: 0, eta: 0, epsA: 0}).subs(frozen)
om_par = sp.simplify(om_par)
cpar2 = sp.limit(om_par/k3**2, k3, sp.oo)
tgt_par = a*(a+2)*(lam-1)/(3*lam-1)
check('[D5] c_par^2 = x(x+2)(lam-1)/(3lam-1)  (x = a), frozen F, eta = 0',
      sp.simplify(cpar2 - tgt_par) == 0)

# [D6] k perp a (k3 = 0), eta = 0, epsA = 0
om_perp = omega2.subs({k3: 0, eta: 0, epsA: 0}).subs(frozen)
om_perp = sp.simplify(om_perp)
cperp2 = sp.limit(om_perp/k1**2, k1, sp.oo)
tgt_perp = a*(lam-1)/(3*lam-1)
check('[D6] c_perp^2 = x(lam-1)/(3lam-1), frozen F, eta = 0',
      sp.simplify(cperp2 - tgt_perp) == 0)

# [D7] a -> 0, generic eta: BPS formula with alpha = eta + 2
om_bps = omega2.subs({k1: 0, epsA: 0}).subs(frozen)
cbps = sp.limit(sp.simplify(om_bps/k3**2), k3, sp.oo)
cbps0 = sp.simplify(sp.limit(cbps, a, 0))
alpha = eta + 2
tgt_bps = (lam-1)*(2-alpha)/(alpha*(3*lam-1))
check('[D7] a -> 0, generic eta: c_s^2 = (lam-1)(2-alpha)/(alpha(3lam-1)), '
      'alpha = eta+2  [BPS structure, F_X(0) = -1]',
      sp.simplify(cbps0 - tgt_bps) == 0)

# [D8] O(epsA) shift of omega^2 at large k: claimed +2 epsA k^4 (lam-1)/(3(3lam-1))
om_eps = omega2.subs({k1: 0, eta: 0}).subs(frozen)
shift = sp.diff(om_eps, epsA).subs(epsA, 0)
shift_lead = sp.limit(sp.simplify(shift/k3**4), k3, sp.oo)
tgt_shift = 2*(lam-1)/(3*(3*lam-1))
check('[D8] large-k O(epsA) shift of omega^2 = +2 epsA k^4 (lam-1)/(3(3lam-1))',
      sp.simplify(shift_lead - tgt_shift) == 0)

# [D9] eta > 0 deep-MOND gradient instability threshold s_c = sqrt(2/(2-eta)) - 1
om_eta = omega2.subs({k1: 0, epsA: 0}).subs(frozen)
ceta = sp.simplify(sp.limit(om_eta/k3**2, k3, sp.oo))     # c_par^2(a, eta, lam)
s_c = sp.sqrt(2/(2-eta)) - 1
val_at_sc = sp.simplify(ceta.subs(a, s_c))
# below s_c: sign of c_par^2 flips (test numerically at eta = 1/2, lam = 2)
num = {eta: sp.Rational(1, 2), lam: 2}
scn = float(s_c.subs(num))
below = float(ceta.subs(num).subs(a, scn*0.5))
above = float(ceta.subs(num).subs(a, scn*1.5))
check('[D9] c_par^2 vanishes at s_c = sqrt(2/(2-eta)) - 1 and is NEGATIVE below '
      '(eta > 0 deep-MOND gradient instability), positive above',
      val_at_sc == 0 and below < 0 and above > 0)

print()
print('TOTAL: %d PASS, %d FAIL' % (npass, nfail))
