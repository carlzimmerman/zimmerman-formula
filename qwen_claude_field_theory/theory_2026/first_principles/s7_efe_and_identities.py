#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s7_efe_and_identities.py -- program section 7 (task parts e, f)
================================================================
External-field expansion of the static weak-field system derived in
s4_exact_variation.py, plus the closure identities.

Background: Phi = -g_e z + e*phi,  Psi = -g_e' z + e*psi  (slip allowed).
s4 check [9] established that these backgrounds solve the vacuum equations
for ARBITRARY (g_e, g_e'); the value g_e' = g_e + O(eps) follows from the
Psi-equation applied to the SOURCE of the external field plus decaying
boundary conditions (ASSUMED: fields -> 0 at infinity), since at eps = 0
lap(Psi - Phi) = 0 globally => Psi = Phi everywhere.

DERIVED and CHECKED (PASS/FAIL):
  [1] d_i d_j S_ij[f] = (2/3) lap^2 f   (exact identity, generic f).
  [2] F(0,0) = 0 exactly, and F = -X + (2/3) X^(3/2) + O(X^2) for small X:
      no induced cosmological constant, no tadpole, and the F-term CANCELS
      the would-be Newtonian response at low X (deep-MOND design).
  [3] A(1) = 1/16, A'(1) = 0, A ~ X^2 (X<<1), A ~ X^-2 (X>>1) (repo facts).
  [4] The O(e^2) Lagrangian of (phi, psi) about the external-field background
      equals, up to a total divergence,
        L2 = (1/16piG)[ 2(grad psi)^2 - 4 grad phi . grad psi + eta_K (grad phi)^2 ]
             - (1/8piG)[ F_X(X_e) |grad phi|^2 + 2 X_e F_XX(X_e) (d_z phi)^2 ]
             - (eps c^4/(8 pi G a0^2)) A(X_e) S_ij[psi] S_ij[psi]
             - drho * phi
      with X_e = g_e^2/a0^2 (all coefficients verified, none quoted).
  [5] The linear field equations that follow:
        (phi):  lap psi + (F_X(X_e) - eta_K/2) lap phi
                  + 2 X_e F_XX(X_e) d_z^2 phi = 4 pi G drho
        (psi):  lap(psi - phi) = -(2/3)(eps c^4/a0^2) A(X_e) lap^2 psi
  [6] Anisotropy check: 1 + F_X(X) + 2 X F_XX(X) == d/dx [x mu(x)] with
      mu = x/(1+x), x = sqrt(X): the parallel operator coefficient is the
      standard AQUAL curl-free EFE combination mu + x mu' (at eta_K = 0).
  [7] The linear-response kernels at eta_K=0: perpendicular mu_perp = x/(1+x),
      parallel mu_par = x(x+2)/(1+x)^2, both -> 1 as x -> infinity (Newtonian)
      and -> x, 2x as x -> 0 (deep MOND).
"""
import sympy as sp
from sympy.calculus.euler import euler_equations

x, y, z = sp.symbols('x y z', real=True)
c, a0, G, etaK, epsl, e = sp.symbols('c a_0 G eta_K epsilon e', positive=True)
ge, gpe = sp.symbols('g_e g_ep', positive=True)
V = (x, y, z)
phi = sp.Function('phi')(x, y, z)
psi = sp.Function('psi')(x, y, z)
drho = sp.Function('drho')(x, y, z)
f = sp.Function('f')(x, y, z)
delta = sp.eye(3)

def grad(F_): return [sp.diff(F_, v) for v in V]
def lap(F_):  return sum(sp.diff(F_, v, 2) for v in V)
def div(vec): return sum(sp.diff(vec[i], V[i]) for i in range(3))
def S_ij(F_, i, j): return sp.diff(F_, V[i], V[j]) - delta[i, j] * lap(F_) / 3

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name)

def is_zero(expr):
    ee = sp.expand(expr)
    if ee == 0: return True
    ee = sp.simplify(ee)
    return ee == 0 or (hasattr(ee, 'equals') and ee.equals(0) is True)

# ----------------------------------------------------------------------
# [1] double divergence of the trace-free Hessian
ident = sum(sp.diff(S_ij(f, i, j), V[i], V[j]) for i in range(3) for j in range(3))
check('[1] d_i d_j S_ij[f] = (2/3) lap^2 f  (VERIFIED, not corrected)',
      is_zero(ident - sp.Rational(2, 3) * lap(lap(f))))

# ----------------------------------------------------------------------
# [2] F(0,0) = 0 and small-X behaviour
Xs, Ys = sp.symbols('X_s Y_s', positive=True)
Fful = -2 * sp.sqrt(Xs) + 2 * sp.log(1 + sp.sqrt(Xs)) + epsl * Xs**2 / (1 + Xs)**4 * Ys
F00 = sp.limit(Fful.subs(Ys, 0), Xs, 0, '+')
s = sp.symbols('s', positive=True)                     # s = sqrt(X)
Fser = sp.series(Fful.subs([(Xs, s**2), (Ys, 0)]), s, 0, 5).removeO()
ok2 = (F00 == 0) and is_zero(Fser - (-s**2 + sp.Rational(2, 3) * s**3
                                     - sp.Rational(1, 2) * s**4))
check('[2] F(0,0) = 0 exactly; F = -X + (2/3)X^{3/2} - (1/2)X^2 + ... (no constant,'
      ' no cosmological term, no tadpole)', ok2)

# ----------------------------------------------------------------------
# [3] A(X) facts
A = Xs**2 / (1 + Xs)**4
ok3 = (A.subs(Xs, 1) == sp.Rational(1, 16)) and is_zero(sp.diff(A, Xs).subs(Xs, 1))
ok3 = ok3 and is_zero(sp.limit(A / Xs**2, Xs, 0) - 1) \
          and is_zero(sp.limit(A * Xs**2, Xs, sp.oo) - 1)
check('[3] A(1)=1/16, A\'(1)=0, A ~ X^2 (X<<1), A ~ X^-2 (X>>1)', ok3)

# ----------------------------------------------------------------------
# [4] quadratic action about the external-field background
# full weak-field Lagrangian from s4 (coefficients derived there):
Phi_full = -ge * z + e * phi
Psi_full = -gpe * z + e * psi
gP = grad(Phi_full); gS = grad(Psi_full)
gradPhi2 = sum(gi**2 for gi in gP)
gradPsi2 = sum(gi**2 for gi in gS)
dotPS    = sum(gP[i] * gS[i] for i in range(3))
X  = gradPhi2 / a0**2
xs = sp.sqrt(X)
Fmond = -2 * xs + 2 * sp.log(1 + xs)
Afun  = X**2 / (1 + X)**4
Y  = c**4 / a0**4 * sum(S_ij(Psi_full, i, j)**2 for i in range(3) for j in range(3))
pref = c**4 / (16 * sp.pi * G)
L = pref * (2 * gradPsi2 - 4 * dotPS + etaK * gradPhi2) / c**4 \
    - (a0**2 / (8 * sp.pi * G)) * (Fmond + epsl * Afun * Y) \
    - (e * drho) * Phi_full

L2 = sp.expand(sp.diff(L, e, 2).subs(e, 0) / 2)

Xe = ge**2 / a0**2
Fsym = -2 * sp.sqrt(Xs) + 2 * sp.log(1 + sp.sqrt(Xs))
FXe  = sp.diff(Fsym, Xs).subs(Xs, Xe)
FXXe = sp.diff(Fsym, Xs, 2).subs(Xs, Xe)
Ae   = A.subs(Xs, Xe)

gphi2 = sum(gi**2 for gi in grad(phi))
gpsi2 = sum(gi**2 for gi in grad(psi))
dps   = sum(grad(phi)[i] * grad(psi)[i] for i in range(3))
Spsi2 = sum(S_ij(psi, i, j)**2 for i in range(3) for j in range(3))

L2_target = (1 / (16 * sp.pi * G)) * (2 * gpsi2 - 4 * dps + etaK * gphi2) \
            - (1 / (8 * sp.pi * G)) * (FXe * gphi2
                                       + 2 * Xe * FXXe * sp.diff(phi, z)**2) \
            - (epsl * c**4 / (8 * sp.pi * G * a0**2)) * Ae * Spsi2 \
            - drho * phi

# equality up to total divergence <=> identical Euler-Lagrange operators
eldiff = euler_equations(sp.expand(L2 - L2_target), [phi, psi], V)
check('[4] O(e^2) Lagrangian == canonical anisotropic form (EFE quadratic action),'
      ' up to a total divergence', all(is_zero(q.lhs - q.rhs) for q in eldiff))

# ----------------------------------------------------------------------
# [5] linear field equations from L2_target
eqs = euler_equations(L2_target, [phi, psi], V)
elphi = eqs[0].lhs - eqs[0].rhs
elpsi = eqs[1].lhs - eqs[1].rhs
t_phi = (lap(psi) + (FXe - etaK / 2) * lap(phi)
         + 2 * Xe * FXXe * sp.diff(phi, z, 2)) / (4 * sp.pi * G) - drho
t_psi = -(lap(psi) - lap(phi)
          + sp.Rational(2, 3) * (epsl * c**4 / a0**2) * Ae * lap(lap(psi))) \
        / (4 * sp.pi * G)
ok5 = is_zero(elphi - t_phi) and is_zero(elpsi - t_psi)
check('[5] linear equations:  lap psi + (F_X - eta_K/2) lap phi + 2 X_e F_XX dz^2 phi'
      ' = 4piG drho ;  lap(psi-phi) = -(2/3)(eps c^4/a0^2) A(X_e) lap^2 psi', ok5)

# ----------------------------------------------------------------------
# [6] parallel-operator combination equals d(x mu)/dx, mu = x/(1+x)
xv = sp.symbols('x_v', positive=True)
comb = (1 + sp.diff(Fsym, Xs) + 2 * Xs * sp.diff(Fsym, Xs, 2)).subs(Xs, xv**2)
mu = xv / (1 + xv)
ok6 = is_zero(sp.simplify(comb - sp.diff(xv * mu, xv)))
check('[6] 1 + F_X + 2X F_XX == d(x mu)/dx  with mu = x/(1+x)  '
      '(AQUAL curl-free EFE parallel coefficient, eta_K = 0)', ok6)

# ----------------------------------------------------------------------
# [7] kernel limits
mu_perp = 1 + sp.diff(Fsym, Xs).subs(Xs, xv**2)
mu_par  = sp.simplify(comb)
ok7 = is_zero(sp.simplify(mu_perp - xv / (1 + xv))) \
      and is_zero(sp.simplify(mu_par - xv * (xv + 2) / (1 + xv)**2)) \
      and sp.limit(mu_perp, xv, sp.oo) == 1 and sp.limit(mu_par, xv, sp.oo) == 1 \
      and is_zero(sp.limit(mu_perp / xv, xv, 0) - 1) \
      and is_zero(sp.limit(mu_par / xv, xv, 0) - 2)
check('[7] mu_perp = x/(1+x), mu_par = x(x+2)/(1+x)^2; Newtonian limit 1, '
      'deep-MOND limits x and 2x', ok7)

# ----------------------------------------------------------------------
print()
print('EFE-EXPANDED LINEAR SYSTEM (z along the external field, X_e = g_e^2/a0^2):')
print('  (phi): lap psi + (F_X(X_e) - eta_K/2) lap phi + 2 X_e F_XX(X_e) dz^2 phi')
print('         = 4 pi G drho')
print('  (psi): lap (psi - phi) = -(2/3) (eps c^4/a0^2) A(X_e) lap^2 psi')
print()
print('Background slip: NOT fixed by the local vacuum equations (s4 check [9]);')
print('at eps = 0 the global Psi-equation + decaying BCs give Psi = Phi, hence')
print('g_e\' = g_e + O(eps).')
n_fail = sum(1 for _, ok in results if not ok)
print()
print('%d checks, %d failed' % (len(results), n_fail))
raise SystemExit(1 if n_fail else 0)
