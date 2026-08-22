#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec9_second_variation_symbol.py -- program section 9, parts (a), (c), (d)
=========================================================================
Exact second variation of the static energy functional E (derived and
verified in sec9_energy_functional.py), the COMPLETE principal symbol of
the coupled two-field linearised operator on an arbitrary background, and
the necessary-and-sufficient local ellipticity conditions.

The energy functional (DERIVED in sec9_energy_functional.py):
  E = INT { (1/8piG)[ -(grad Psi)^2 + 2 grad Phi.grad Psi
            - (eta_K/2)(grad Phi)^2 + a0^2 F(X,Y) ] + rho Phi },
  X = |grad Phi|^2/a0^2,  Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi].

DERIVED AND CHECKED (PASS/FAIL):
  [B1] (a) EXACT second variation.  For perturbations (phi, psi) about a
       background with g0 = grad Phi0, S0 = S[Psi0], X0, Y0:
       Q = (1/2) d^2/dt^2 E[Phi0+t phi, Psi0+t psi]|_0 = INT (1/8piG) {
           -|grad psi|^2 + 2 grad phi . grad psi - (eta_K/2)|grad phi|^2
           + F_X |grad phi|^2 + (2 F_XX/a0^2)(g0 . grad phi)^2
           + (4 c^4 F_XY/a0^4)(g0 . grad phi)(S0 : S[psi])
           + (c^4 F_Y/a0^2) S[psi]:S[psi]
           + (2 c^8 F_YY/a0^6)(S0 : S[psi])^2 }
       (all F-derivatives at (X0,Y0); machine-verified against the literal
       pointwise Taylor coefficient, generic F).
  [B2] (c) the COMPLETE symbol, Hermitian 2x2, from plane waves:
       M_phiphi = (F_X - eta_K/2) k^2 + (2 F_XX/a0^2)(g0.k)^2
       M_phipsi = k^2 - i (2 c^4 F_XY/a0^4)(g0.k)(S0:kk)   [= conj(M_psiphi)]
       M_psipsi = -k^2 + (2 c^4 F_Y/3 a0^2) k^4 + (2 c^8 F_YY/a0^6)(S0:kk)^2
       For the frozen F: F_X = f_X + eps A'Y0, F_XX = f_XX + eps A''Y0,
       F_XY = eps A', F_Y = eps A, F_YY = 0, f = -2 sqrt(X)+2 log(1+sqrt X).
       The anisotropic (2 mu_X)(g0.k)^2 piece is the F_XX term.
  [B3] eps = 0: second-order system; principal symbol = full symbol; and
       det M = -k^4 [ mu - eta_K/2 + 2 X0 f_XX tau^2 ],  tau = ghat.khat.
       N&S ellipticity <=> mu - eta_K/2 + 2 X0 f_XX tau^2 != 0 for all tau;
       at eta_K = 0 both mu > 0 and mu + 2X f_XX = x(2+x)/(1+x)^2 > 0 for
       x > 0 => elliptic EVERYWHERE EXCEPT critical points of Phi0 (x = 0).
  [B4] eps != 0: Douglis-Nirenberg orders (2,3;3,4), weights (1,1;2,2)
       (any admissible weight choice gives the same principal determinant).
       PRINCIPAL symbol: pi_phiphi = M_phiphi (all of it, incl. the
       anisotropic piece); pi_phipsi = -i(2 eps A' c^4/a0^4)(g0.k)(S0:kk)
       [the GR k^2 cross term is SUBPRINCIPAL]; pi_psipsi =
       (2 eps A c^4/3a0^2) k^4 [the GR -k^2 is SUBPRINCIPAL].
       det pi / k^6 = D(khat) =
           (2 eps c^4 A/3a0^2) [ mu_dir(khat) - 1 ]
           - (4 eps^2 A'^2 c^8/a0^6) X0 tau^2 sigma^2 ,
       mu_dir(khat) := mu - eta_K/2 + eps A' Y0 + 2(f_XX + eps A'' Y0) X0 tau^2,
       sigma := (S0:khat khat)  (units s^-2), tau := ghat.khat.
  [B5] the KEY IDENTITY  det M(k) = k^4 [ -mu_dir(khat) + D(khat) k^2 ]:
       the full determinant is EXACTLY the two invariants mu_dir and D.
       Hence a real finite-k characteristic exists in direction khat
       <=> mu_dir(khat) and D(khat) have the SAME sign.
  [B6] (d) NECESSARY AND SUFFICIENT local conditions, point with X0 > 0:
       - DN-ellipticity  <=>  D(khat) != 0 for every khat in S^2.
       - ellipticity at ALL scales (DN + no frozen-coefficient real
         characteristic)  <=>  for every khat:
              (i)  mu_dir(khat) > 0   and   (ii) D(khat) < 0 .
         (mu_dir < 0 uniformly is the only other zero-free sign pattern
          and it destroys the Newtonian long-wavelength limit.)
       - eps > 0: (ii) is AUTOMATIC wherever mu_dir(khat) <= 1 (both terms
         of D are then <= 0); it only bites where mu_dir > 1.
       - eps < 0 EXCLUDED at every point with X0 > 0: D(tau=0) =
         (2 eps c^4 A/3a0^2)(mu_dir(0)-1) > 0 whenever mu_dir(0) < 1
         (Newtonian-healthy), which with (i) forces a real finite-k
         characteristic; avoiding it needs mu_dir(0) <= 0, killing the
         long-wavelength limit.  Verified numerically on a grid.
       - X0 = 0 (critical points of Phi0): A = A' = 0 => det pi == 0:
         DN-ellipticity FAILS for ANY eps != 0 (4th->2nd order collapse);
         the residual 2nd-order system is the eps = 0 one, itself
         degenerate there (mu(0) = 0).  Ellipticity holds NOWHERE at
         X0 = 0; it is a genuine boundary of the elliptic region.
  [B7] the psi-sector crossover scale (eps > 0): M_psipsi changes sign at
       k*^2 = 3 a0^2/(2 eps A c^4), l* = c^2 sqrt(2 eps A/3)/a0 -- the
       finite-k structure lives at the SAME scale l_Y ~ sqrt(eps) c^2/a0
       as the repo's tidal mechanism (mu_positivity_2026.py's l_Y).

Comparison with mu_positivity_2026.py's chi_c ~ 1.73 -> sec9_ellipticity_scan.py.
Exit code 1 on any FAIL.
"""
import sys, time, json, os, random
import numpy as np
import sympy as sp

T0 = time.time()
results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, '   [t=%.1fs]' % (time.time() - T0))

def is_zero(expr):
    ee = sp.expand(expr)
    if ee == 0: return True
    ee = sp.simplify(ee)
    return ee == 0 or (hasattr(ee, 'equals') and ee.equals(0) is True)

# ----------------------------------------------------------------- setup
t = sp.symbols('t', real=True)
c, a0, G, g = sp.symbols('c a_0 G g_0', positive=True)
etaK = sp.symbols('eta_K', real=True)
epsl = sp.symbols('epsilon', real=True)
k1, k2, k3 = sp.symbols('k_1 k_2 k_3', real=True)
u, ub, w, wb = sp.symbols('u ubar w wbar')
Z = sp.symbols('Z')                       # stands for e^{i k.x}; Z*Zbar = 1
I = sp.I
kv = [k1, k2, k3]
k2s = k1**2 + k2**2 + k3**2
delta = sp.eye(3)

# background: g0 along z (WLOG), S0 generic symmetric TRACELESS constant
g0 = [sp.S(0), sp.S(0), g]
s11, s22, s12, s13, s23 = sp.symbols('s_11 s_22 s_12 s_13 s_23', real=True)
S0 = sp.Matrix([[s11, s12, s13], [s12, s22, s23], [s13, s23, -s11 - s22]])

# plane-wave perturbations (complex amplitudes; ub, wb independent conjugates)
dphi = [I * kv[i] * (u * Z - ub / Z) for i in range(3)]
dpsi = [I * kv[i] * (w * Z - wb / Z) for i in range(3)]
Spsi = sp.Matrix(3, 3, lambda i, j: -(kv[i] * kv[j] - delta[i, j] * k2s / 3)
                 * (w * Z + wb / Z))

Xt = sum((g0[i] + t * dphi[i])**2 for i in range(3)) / a0**2
Yt = (c**4 / a0**4) * sum((S0[i, j] + t * Spsi[i, j])**2
                          for i in range(3) for j in range(3))
# F represented by its exact 2nd-order Taylor polynomial about (X0, Y0):
# higher Taylor terms are O(t^3) and cannot contribute to (1/2) d^2/dt^2 |_{t=0},
# so this IS the generic-F second variation.
X0v = (g**2 / a0**2)
Y0v = (c**4 / a0**4) * sum(S0[i, j]**2 for i in range(3) for j in range(3))
F0, FX, FY, FXX, FXY, FYY = sp.symbols('F_0 F_X F_Y F_XX F_XY F_YY', real=True)
F_taylor = (F0 + FX * (Xt - X0v) + FY * (Yt - Y0v)
            + sp.Rational(1, 2) * FXX * (Xt - X0v)**2
            + FXY * (Xt - X0v) * (Yt - Y0v)
            + sp.Rational(1, 2) * FYY * (Yt - Y0v)**2)
q_machine = (-sum(d**2 for d in dpsi)
             + 2 * sum(dphi[i] * dpsi[i] for i in range(3))
             - (etaK / 2) * sum(d**2 for d in dphi)
             + a0**2 * sp.Rational(1, 2)
             * sp.diff(F_taylor, t, 2).subs(t, 0))

print('=' * 100)
print('[B1] exact second variation (part a): machine Taylor vs the displayed formula')
print('=' * 100)
gdotdphi = sum(g0[i] * dphi[i] for i in range(3))
S0dotSpsi = sum(S0[i, j] * Spsi[i, j] for i in range(3) for j in range(3))
SpsiSpsi = sum(Spsi[i, j]**2 for i in range(3) for j in range(3))
q_hand = (-sum(d**2 for d in dpsi)
          + 2 * sum(dphi[i] * dpsi[i] for i in range(3))
          - (etaK / 2) * sum(d**2 for d in dphi)
          + FX * sum(d**2 for d in dphi)
          + (2 * FXX / a0**2) * gdotdphi**2
          + (4 * c**4 * FXY / a0**4) * gdotdphi * S0dotSpsi
          + (c**4 * FY / a0**2) * SpsiSpsi
          + (2 * c**8 * FYY / a0**6) * S0dotSpsi**2)
check('[B1] Q integrand == (1/8piG){ -|grad psi|^2 + 2 grad phi.grad psi'
      ' - (eta_K/2)|grad phi|^2 + F_X|grad phi|^2 + (2F_XX/a0^2)(g0.grad phi)^2'
      ' + (4c^4 F_XY/a0^4)(g0.grad phi)(S0:S[psi]) + (c^4F_Y/a0^2)S[psi]:S[psi]'
      ' + (2c^8F_YY/a0^6)(S0:S[psi])^2 }',
      sp.expand(q_machine - q_hand) == 0)

print('=' * 100)
print('[B2] the complete Hermitian symbol M(k) (part c)')
print('=' * 100)
# cell average: keep only Z-degree-0 terms
def zavg(expr):
    expr = sp.expand(expr)
    out = sp.S(0)
    for term in sp.Add.make_args(expr):
        if term.as_powers_dict().get(Z, 0) == 0:
            out += term
    return out

q_avg = zavg(q_machine)
M = sp.Matrix([[sp.expand(sp.diff(q_avg, u, ub)), sp.expand(sp.diff(q_avg, u, wb))],
               [sp.expand(sp.diff(q_avg, ub, w)), sp.expand(sp.diff(q_avg, w, wb))]])
S0kk = sum(S0[i, j] * kv[i] * kv[j] for i in range(3) for j in range(3))
g0k = sum(g0[i] * kv[i] for i in range(3))
M_pp_hand = (FX - etaK / 2) * k2s + (2 * FXX / a0**2) * g0k**2
M_ps_hand = k2s - I * (2 * c**4 * FXY / a0**4) * g0k * S0kk
M_ss_hand = -k2s + (2 * c**4 * FY / (3 * a0**2)) * k2s**2 \
            + (2 * c**8 * FYY / a0**6) * S0kk**2
# the machine matrix (d^2 q_avg/du dub etc.) is the EL-OPERATOR symbol = exactly
# 2 x the form-density matrix (phi = u Z + ub/Z has real amplitude 2|u|); the
# factor 2 is an overall positive constant, irrelevant to every sign/zero
# statement below.  We display and use the form-density normalisation.
check('[B2.1] M_phiphi = (F_X - eta_K/2)k^2 + (2F_XX/a0^2)(g0.k)^2   [the anisotropic'
      ' 2 mu_X (grad Phi.k)^2 piece, mu_X = F_XX]',
      sp.expand(M[0, 0] - 2 * M_pp_hand) == 0)
check('[B2.2] M_phipsi = k^2 - 2i(c^4 F_XY/a0^4)(g0.k)(S0:kk), M_psiphi = its conjugate'
      ' (Hermitian)', sp.expand(M[0, 1] - 2 * M_ps_hand) == 0 and
      sp.expand(M[1, 0] - 2 * (k2s + I * (2 * c**4 * FXY / a0**4) * g0k * S0kk)) == 0)
check('[B2.3] M_psipsi = -k^2 + (2c^4F_Y/3a0^2)k^4 + (2c^8F_YY/a0^6)(S0:kk)^2'
      '  [S[psi]:S[psi] -> (2/3)k^4]', sp.expand(M[1, 1] - 2 * M_ss_hand) == 0)
print('   NOTE: S0 enters ONLY through the scalar sigma = S0:khat khat (and Y0 in the')
print('   F-derivatives); g0 only through (g0.k).  The 4th-order sector is FROZEN-F')
print('   SIMPLE: F_YY = 0 (F linear in Y) kills the (S0:kk)^2 term in M_psipsi.')

# ---------------------------------------------------------------- frozen F
X0s = sp.symbols('X_0', positive=True)
Y0s = sp.symbols('Y_0', nonnegative=True)
xs = sp.sqrt(X0s)
fX = -1 / (1 + xs)
fXX = sp.Rational(1, 2) / (xs * (1 + xs)**2)
Aa = X0s**2 / (1 + X0s)**4
Ap = 2 * X0s * (1 - X0s) / (1 + X0s)**5
App = 2 * (3 * X0s**2 - 6 * X0s + 1) / (1 + X0s)**6
Xf = sp.symbols('X_f', positive=True)
check('[B2.4] frozen-F facts re-derived: f_X = -1/(1+x), f_XX = 1/(2x(1+x)^2),'
      ' A\' = 2X(1-X)/(1+X)^5, A\'\' = 2(3X^2-6X+1)/(1+X)^6',
      is_zero(sp.diff(-2 * sp.sqrt(Xf) + 2 * sp.log(1 + sp.sqrt(Xf)), Xf)
              + 1 / (1 + sp.sqrt(Xf))) and
      is_zero(sp.simplify(sp.diff(-2 * sp.sqrt(Xf) + 2 * sp.log(1 + sp.sqrt(Xf)), Xf, 2)
              - sp.Rational(1, 2) / (sp.sqrt(Xf) * (1 + sp.sqrt(Xf))**2))) and
      is_zero(sp.simplify(sp.diff(Xf**2 / (1 + Xf)**4, Xf)
              - 2 * Xf * (1 - Xf) / (1 + Xf)**5)) and
      is_zero(sp.simplify(sp.diff(Xf**2 / (1 + Xf)**4, Xf, 2)
              - 2 * (3 * Xf**2 - 6 * Xf + 1) / (1 + Xf)**6)))
frozen = [(FX, fX + epsl * Ap * Y0s), (FXX, fXX + epsl * App * Y0s),
          (FXY, epsl * Ap), (FY, epsl * Aa), (FYY, sp.S(0))]

# invariant variables: tau = ghat.khat, sigma = S0:khat khat
tau, sig, kk = sp.symbols('tau sigma k', real=True)
def invariant(expr):
    """rewrite an M entry in invariants (valid because entries depend on k, g0, S0
    only via k^2, (g0.k), (S0:kk)) -- substitute and verify."""
    return expr.subs([(g0k, a0 * sp.sqrt(X0s) * tau * kk), (S0kk, sig * kk**2),
                      (k2s, kk**2), (g, a0 * sp.sqrt(X0s))])

Mf = M.subs(frozen)
m_pp = sp.expand(invariant(M_pp_hand.subs(frozen)))
m_ps = sp.expand(invariant(M_ps_hand.subs(frozen)))
m_ss = sp.expand(invariant(M_ss_hand.subs(frozen)))

print('=' * 100)
print('[B3] eps = 0: the second-order system and its N&S ellipticity condition')
print('=' * 100)
mu_s = 1 + fX
det0 = sp.expand(sp.simplify((m_pp * m_ss - m_ps * sp.conjugate(m_ps))
                             .subs(epsl, 0).subs(sp.conjugate(kk), kk)
                             .subs([(sp.conjugate(s), s) for s in (tau, sig)])))
det0_target = -kk**4 * (mu_s - etaK / 2 + 2 * X0s * fXX * tau**2)
check('[B3.1] det M(eps=0) == -k^4 [ mu - eta_K/2 + 2 X0 f_XX tau^2 ]',
      is_zero(sp.simplify(det0 - det0_target)))
radial0 = sp.simplify((mu_s + 2 * X0s * fXX))
check('[B3.2] at eta_K=0: transverse coeff mu = x/(1+x) > 0 and radial coeff'
      ' mu + 2X f_XX = x(2+x)/(1+x)^2 > 0 for x > 0; both -> 0 as x -> 0'
      '  =>  N&S: elliptic <=> x > 0 (fails ONLY at critical points of Phi0)',
      is_zero(sp.simplify(mu_s - xs / (1 + xs))) and
      is_zero(sp.simplify(radial0 - xs * (2 + xs) / (1 + xs)**2)) and
      sp.limit(mu_s, X0s, 0) == 0 and sp.limit(radial0, X0s, 0) == 0)
print('   (saddle signature: the symbol is INDEFINITE -- Legendre-Hadamard fails for')
print('    the pair by [A6] -- but det != 0: ellipticity in the Petrovsky/DN sense,')
print('    which is what regularity and local solvability need.)')

print('=' * 100)
print('[B4] eps != 0: Douglis-Nirenberg principal symbol and det pi')
print('=' * 100)
print('   orders: L_phiphi = 2, L_phipsi = L_psiphi = 3, L_psipsi = 4;')
print('   admissible DN weights (s,t) = (1,1),(2,2): principal parts are the terms of')
print('   EXACT order s_i+t_j; any other admissible weight assignment must satisfy')
print('   s_phi+t_phi >= 2, s_phi+t_psi >= 3, s_psi+t_phi >= 3, s_psi+t_psi >= 4 with')
print('   equality where a nonzero term exists => the SAME principal determinant.')
pi_pp = m_pp                                    # all order 2
pi_ps = sp.expand(m_ps - kk**2)                 # order-3 part: GR k^2 is SUBPRINCIPAL
pi_ss = sp.expand(m_ss + kk**2)                 # order-4 part: GR -k^2 is SUBPRINCIPAL
check('[B4.1] pi_phipsi = -2i eps A\'(c^4/a0^4)(g0.k)(S0:kk): the GR cross term k^2'
      ' (which carries the "+1" of mu) is SUBPRINCIPAL for eps != 0',
      sp.expand(pi_ps + 2 * I * epsl * Ap * (c**4 / a0**4)
                * (a0 * sp.sqrt(X0s) * tau * kk) * sig * kk**2) == 0)
check('[B4.2] pi_psipsi = (2 eps A c^4/3a0^2) k^4',
      sp.expand(pi_ss - 2 * epsl * Aa * (c**4 / (3 * a0**2)) * kk**4) == 0)
detpi = sp.expand(pi_pp * pi_ss - pi_ps * sp.conjugate(pi_ps)
                  .subs([(sp.conjugate(s), s) for s in (tau, sig, kk)]))
mu_dir = (mu_s - etaK / 2 + epsl * Ap * Y0s
          + 2 * (fXX + epsl * App * Y0s) * X0s * tau**2)
Dfun = (2 * epsl * c**4 * Aa / (3 * a0**2)) * (mu_dir - 1) \
       - 4 * epsl**2 * Ap**2 * (c**8 / a0**6) * X0s * tau**2 * sig**2
check('[B4.3] det pi == k^6 D(khat),  D = (2 eps c^4 A/3a0^2)(mu_dir - 1)'
      ' - 4 eps^2 A\'^2 (c^8/a0^6) X0 tau^2 sigma^2,  with mu_dir = mu - eta_K/2'
      ' + eps A\'Y0 + 2(f_XX + eps A\'\'Y0) X0 tau^2',
      is_zero(sp.simplify(detpi - kk**6 * Dfun)))
check('[B4.4] X0 = 0: A(0) = A\'(0) = 0 => det pi == 0 identically: DN-ellipticity'
      ' FAILS at every critical point of Phi0, for ANY eps != 0 (order collapse 4->2)',
      sp.limit(Aa, X0s, 0) == 0 and sp.limit(Ap, X0s, 0) == 0 and
      is_zero(sp.limit(detpi.subs(Y0s, 0), X0s, 0)))

print('=' * 100)
print('[B5] the key identity: full det M(k) = k^4 [ -mu_dir + D k^2 ]')
print('=' * 100)
detM = sp.expand(m_pp * m_ss - m_ps * sp.conjugate(m_ps)
                 .subs([(sp.conjugate(s), s) for s in (tau, sig, kk)]))
check('[B5.1] det M(k) == k^4 [ -mu_dir(khat) + D(khat) k^2 ]  EXACTLY: the whole'
      ' frozen-coefficient determinant is the two invariants mu_dir and D',
      is_zero(sp.simplify(detM - kk**4 * (-mu_dir + Dfun * kk**2))))
print('   => real finite-k characteristic in direction khat  <=>  mu_dir, D same sign;')
print('      k_char^2 = mu_dir/D.  mu_dir(tau=0)|_{etaK=0} = mu + eps A\'Y0 is EXACTLY')
print('      the pointwise mu_eff of mu_positivity_2026.py: that script\'s criterion is')
print('      the tau = 0 slice of the NO-REAL-CHARACTERISTIC condition -- it is NOT the')
print('      ellipticity (det pi != 0) condition, and it misses the anisotropic')
print('      tau^2-part 2(f_XX + eps A\'\' Y0) X0 of mu_dir.')

print('=' * 100)
print('[B6] necessary-and-sufficient local conditions (part d)')
print('=' * 100)
print('   At a point with X0 > 0 (all statements verified on numeric grids below):')
print('   DN-elliptic                <=>  D(khat) != 0 for all khat in S^2')
print('   elliptic at ALL scales    <=>  for all khat:  mu_dir(khat) > 0  AND  D(khat) < 0')
print('   [the only alternative zero-free pattern, mu_dir < 0 with D > 0 for ALL khat,')
print('    flips the sign of the long-wavelength (reduced AQUAL) operator: Newtonian')
print('    limit destroyed; we exclude it on physics, and note it separately.]')
# numeric verification of the sign logic and the eps<0 exclusion
random.seed(7)
fXn = sp.lambdify(X0s, fX); fXXn = sp.lambdify(X0s, fXX)
An = sp.lambdify(X0s, Aa); Apn = sp.lambdify(X0s, Ap); Appn = sp.lambdify(X0s, App)
def mu_dir_num(X0, Y0, eps, t2, etak=0.0):
    x = np.sqrt(X0)
    return (x / (1 + x) - etak / 2 + eps * Apn(X0) * Y0
            + 2 * (fXXn(X0) + eps * Appn(X0) * Y0) * X0 * t2)
def D_num(X0, Y0, eps, t2, sg, cl=1.0, a0l=1.0, etak=0.0):
    return (2 * eps * cl**4 * An(X0) / (3 * a0l**2) * (mu_dir_num(X0, Y0, eps, t2, etak) - 1)
            - 4 * eps**2 * Apn(X0)**2 * cl**8 / a0l**6 * X0 * t2 * sg**2)
def detM_num(kappa2, X0, Y0, eps, t2, sg, etak=0.0):
    return kappa2**2 * (-mu_dir_num(X0, Y0, eps, t2, etak)
                        + D_num(X0, Y0, eps, t2, sg, etak=etak) * kappa2)
ok_logic = True
trials = 0
for _ in range(4000):
    X0 = 10**random.uniform(-3, 3); eps = random.choice([-1, 1]) * 10**random.uniform(-3, 1)
    Y0 = 10**random.uniform(-2, 3); t2 = random.uniform(0, 1); sg = random.uniform(-2, 2)
    md = mu_dir_num(X0, Y0, eps, t2); Dv = D_num(X0, Y0, eps, t2, sg)
    if md == 0 or Dv == 0: continue
    trials += 1
    kappas = np.geomspace(1e-6, 1e6, 4001)
    dets = detM_num(kappas**2, X0, Y0, eps, t2, sg)
    has_zero = bool(np.any(np.sign(dets[:-1]) * np.sign(dets[1:]) < 0)) \
               or bool(np.any(dets == 0))
    ok_logic = ok_logic and (has_zero == (md * Dv > 0))
check('[B6.1] sign logic verified on %d random (X0,Y0,eps,tau,sigma): real finite-k'
      ' zero of det M  <=>  mu_dir * D > 0' % trials, ok_logic)
# eps < 0 exclusion
ok_neg = True
for _ in range(2000):
    X0 = 10**random.uniform(-3, 3); eps = -10**random.uniform(-4, 1)
    Y0 = 10**random.uniform(-2, 3)
    md0 = mu_dir_num(X0, Y0, eps, 0.0); D0 = D_num(X0, Y0, eps, 0.0, 0.0)
    # D(tau=0) = (2 eps A c^4/3a0^2)(mu_eff - 1): for eps<0 positive iff mu_eff<1
    healthy = md0 > 0
    if healthy and md0 < 1:
        ok_neg = ok_neg and (D0 > 0)     # same sign as mu_dir -> characteristic
check('[B6.2] eps < 0 EXCLUDED: whenever the transverse sector is Newtonian-healthy'
      ' (0 < mu_eff < 1), D(tau=0) > 0 has the same sign => a real finite-k'
      ' characteristic exists; the only escape mu_eff <= 0 kills the long-wavelength'
      ' limit  (verified on a random grid)', ok_neg)
print('   For eps > 0: D < 0 is AUTOMATIC where mu_dir(khat) <= 1 (both D-terms <= 0);')
print('   the DN condition only bites where the eps A\'\'Y0-boosted mu_dir exceeds 1.')

print('=' * 100)
print('[B7] the psi-sector crossover scale (eps > 0)')
print('=' * 100)
kstar2 = sp.solve(sp.Eq(m_ss.subs(epsl, sp.Abs(epsl)), 0), kk**2)
lstar = sp.sqrt(2 * sp.Abs(epsl) * Aa / 3) * c**2 / a0
check('[B7.1] M_psipsi = 0 at k*^2 = 3a0^2/(2 eps A c^4): l* = c^2 sqrt(2 eps A/3)/a0'
      ' -- the same l_Y ~ sqrt(eps) c^2/a0 scale as the repo tidal mechanism',
      any(is_zero(sp.simplify(s - 3 * a0**2 / (2 * sp.Abs(epsl) * Aa * c**4)))
          for s in kstar2))

# ---- export the invariants for the scan script (exact sympy strings)
out = {
    'mu_dir': sp.srepr(mu_dir),
    'D': sp.srepr(Dfun),
    'detM_over_k4': sp.srepr(sp.expand(-mu_dir + Dfun * kk**2)),
    'symbols': 'X_0 Y_0 tau sigma epsilon eta_K c a_0 k',
    'notes': 'mu_dir(khat), D(khat) from sec9_second_variation_symbol.py [B4]-[B5]; '
             'det M = k^4(-mu_dir + D k^2); DN-elliptic <=> D != 0 on S^2; '
             'all-scale elliptic <=> mu_dir > 0 and D < 0 on S^2.'
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'sec9_symbol_invariants.json'), 'w') as f:
    json.dump(out, f, indent=1)
print('   exported invariants -> sec9_symbol_invariants.json')

print('=' * 100)
nfail = sum(1 for _, okc in results if not okc)
print('SUMMARY: %d checks, %d FAIL   [total %.1fs]' % (len(results), nfail, time.time() - T0))
sys.exit(1 if nfail else 0)
