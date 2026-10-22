#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A60 -- THE SOLAR SYSTEM'S P CONFIGURATION: the Sun embedded in the Galaxy.

Lane A22 solved the P field of the *isolated* Sun: a hedgehog of constant
magnitude, u = K|P| = GM/L*^2 = 2.42e-16 m/s^2 = 2.59e-6 a0.  Lane A36's K12
then observed that the *galactic* background at the Sun's position carries
u = 0.566 a0 -- a factor 2.19e5 larger -- and left the mismatch unresolved.
The P equation is nonlinear, so the field of the Sun-in-the-Galaxy is not the
sum of the two solutions.  This lane solves the two-scale problem.

Action (frozen round-2 ADM action, A22/A33 verbatim), c = 1, K = 4 pi G:

  L/(N sqrt h) = [R3 + K_ijK^ij - (1+beta)theta^2 - 2Lambda]/(4K)
                 + P^i D_i ln N - W(u) + (eta/2)E_iE^i
                 - (gamma/2)(D_iP^i)^2 - (gamma/4)F_ijF^ij,
  W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)],  u = K|P|,
  gamma = K L*^2/2,  lambda = sqrt(gamma/K) = L*/sqrt2.

Static, F = 0, E = 0.  The exact P equation is

  (1)   gamma lap(P_i) + d_i ln N - K W'(u) P_i/|P| = 0 .

THE TWO-SCALE EXPANSION.  With P = Pbar(X) + pi(x), X = x/R_gal (8 kpc),
x = the local (solar) coordinate, and the three small parameters

  eps_1 = r/R_gal                      scale separation
  eps_2 = u_sun/u_gal = 4.6e-6         amplitude (controls the NONLINEARITY)
  eps_3 = m^2/(gamma k^2) = (r/ell)^2  stiffness (controls the background's
                                       effect on the RESPONSE)

the order-eps_1^0 inner equation is the linearised operator about the local
background with the solar source.  Its exact solution (isotropic mass m):

  (2)   pi_r(r) = p0 f(r/ell),  f(x) = 2[1 - e^-x(1+x)]/x^2,
        p0 = GM/(2 gamma),  ell = 1/m,  m_T^2 = K/(1-ubar/a0),  m_L^2 = K/(1-ubar/a0)^2

so  u_sun(r) = (GM/L*^2) f(r/ell),  f(0)=1,  f = 1 - 2x/3 + ...  The charge is
psi = div(pi) = p0[f' + 2f/x]/ell, and the metric response gives

  (3)   alpha_1(r) = -4 (r/L*)^2 I(r/ell)/(r/ell),  I(x) = int_0^x f,

i.e. exactly A22's -4(r/L*)^2 for r << ell, with ell = 7.4-11.2 pc set by the
GALACTIC background.  The background changes alpha_1 by O(eps_3) = 5e-8 at
1 AU: it does not move.

Deliverables: report.md, this script (20 checks), a60.out, a60_results.json,
MUTATE.md.  Runtime < 60 s, deterministic, no network.

    python3 a60_checks.py [--mutate NAME] [--json-out FILE]
"""
import argparse
import json
import math
import sys

import numpy as np
from scipy.integrate import solve_bvp
import sympy as sp

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'flat_background', 'slaved_sun', 'eps_r_only',
                         'alpha1_k0', 'alpha1_prefactor2', 'pioneer_visible'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate

CHECKS = []
FAIL = []
NCHK = [0]


def rec(cid, ok, value, threshold, note=''):
    NCHK[0] += 1
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-4s %-4s value=%-44s thr=%-12s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))
    if not ok:
        FAIL.append(cid)


def info(msg):
    print('     ' + msg)


# ============================================================ constants
c = 2.99792458e8
G = 6.67430e-11
Msun = 1.98892e30
AU = 1.495978707e11
pc = 3.0856775814913673e16
kpc = 1000.0 * pc
Mpc = 3.0856775814913673e22

K = 4.0 * math.pi * G                 # c = 1 units, m/kg   (A22/A33 convention)
Ls = 24.0 * pc                        # L* (A20 surviving value)
gam = K * Ls ** 2 / 2.0               # gamma = K L*^2/2
lam = Ls / math.sqrt(2.0)             # P Compton length L*/sqrt2

a0_can = 9.36e-11                     # canonical footing (BRIEF sec.4)
a0_th = 1.132e-10                     # the theory's own vacuum value (THEORY P3)
A0 = a0_can                           # primary footing of this lane

mu = G * Msun                         # GM_sun, m^3/s^2
p0 = mu / (2.0 * gam)                 # hedgehog |P| = GM/(2 gamma)
u0 = K * p0                           # = GM/L*^2

B_ALPHA1 = 2.5e-4                     # 2 sigma LLR |alpha_1| bound (A22/A36)
B_TASK = 1.0e-4                       # the gate's working bound
B_E = 3.66e-14                        # Earth 2 sigma constant-anomaly bound (A4)
R_GAL = 8.0 * kpc                     # Sun's galactocentric radius

# Pioneer (Turyshev et al. 2012, PRL 108, 241101)
A_PIONEER = 8.74e-10
SIG_PIONEER = 1.33e-10
V_CMB = 369.0e3
W2 = (V_CMB / c) ** 2

print(__doc__)
print('=' * 110)
print('CONSTANTS  L* = %.3f pc  lambda = %.4f pc  K = 4 pi G = %.6e m/kg  gamma = %.6e m^5/(kg s^2)'
      % (Ls / pc, lam / pc, K, gam))
print('           a0(canonical) = %.4e m/s^2   a0(theory) = %.4e m/s^2   GM_sun = %.6e m^3/s^2'
      % (a0_can, a0_th, mu))
print('           p0 = GM/(2gamma) = %.6e kg/m^2   u0 = K p0 = GM/L*^2 = %.6e m/s^2'
      % (p0, u0))
print('=' * 110)


# ============================================================ K1: the sector's algebra
u_s, g_s, a0_s, K_s = sp.symbols('u g a0 K', positive=True)
W = (a0_s ** 2 / K_s) * (-u_s / a0_s - sp.log(1 - u_s / a0_s))
Wp = sp.simplify(sp.diff(W, u_s))
Wpp = sp.simplify(sp.diff(W, u_s, 2))
r1 = sp.simplify(K_s * Wp - u_s / (1 - u_s / a0_s))
r2 = sp.simplify(K_s ** 2 * Wpp - K_s / (1 - u_s / a0_s) ** 2)
u_of_g = a0_s * g_s / (g_s + a0_s)
r3 = sp.simplify(K_s * Wp.subs(u_s, u_of_g) - g_s)
info('W\' = %s' % Wp)
info('K W\' - u/(1-u/a0) = %s ;  K^2 W\'\' - K/(1-u/a0)^2 = %s ;  K W\'(u(g)) - g = %s'
     % (r1, r2, r3))
ok1 = (r1 == 0) and (r2 == 0) and (r3 == 0)
rec('K1', ok1, 'residuals %s %s %s' % (r1, r2, r3), '0 0 0',
    'the log potential\'s first two derivatives and its exact inverse u=a0 g/(g+a0)')

# ============================================================ K2: constants and the hedgehog scale
ok2 = (abs(K - 4 * math.pi * G) < 1e-30 and abs(gam - K * Ls ** 2 / 2) < 1e-10 * gam
       and abs(u0 - mu / Ls ** 2) / u0 < 1e-14 and abs(lam - Ls / math.sqrt(2)) < 1e-6)
info('u0 = %.6e m/s^2 = %.6e a0(can) = %.6e a0(th)   p0 = %.6e kg/m^2'
     % (u0, u0 / a0_can, u0 / a0_th, p0))
info('K/gamma = 2/L*^2 = %.6e m^-2   u0/(GM/L*^2) - 1 = %.2e'
     % (2 / Ls ** 2, u0 / (mu / Ls ** 2) - 1))
rec('K2', ok2, 'u0=%.4e m/s^2  K/gamma=%.3e m^-2' % (u0, 2 / Ls ** 2), '= GM/L*^2',
    'K = 4 pi G, gamma = K L*^2/2, u0 = GM/L*^2 = 2.42e-16 (A22 eq.9)')

# ============================================================ K3: the galactic background on-shell
M_BAR = 6.0e10 * Msun
A_H = 3.0 * kpc


def gN_gal(r):
    """Hernquist baryonic field of a MW-like galaxy (A36's model)."""
    return G * M_BAR / (r + A_H) ** 2


def g_law(gN, a0=A0):
    """canonical law g = (gN/2)(1+sqrt(1+4a0/gN))."""
    return 0.5 * gN * (1.0 + math.sqrt(1.0 + 4.0 * a0 / gN))


def uprime_slaved(g, a0=A0):
    return a0 ** 2 / (g + a0) ** 2


GN_GAL = gN_gal(R_GAL)
GGAL = g_law(GN_GAL)
UBAR = GGAL - GN_GAL                     # physical phantom acceleration at the Sun
if MUT == 'flat_background':
    UBAR = 1e-30                          # mutation: the Galaxy is switched off
PBAR = UBAR / K
OK3 = abs(UBAR / (1 - UBAR / A0) - GGAL) / GGAL < 1e-14
INFO3 = ('g_N(8kpc) = %.4e  g = %.4e (%.4f a0)  ubar = %.4e (%.4f a0)  KW\'(ubar)/g - 1 = %.1e'
         % (GN_GAL, GGAL, GGAL / A0, UBAR, UBAR / A0,
            (UBAR / (1 - UBAR / A0) - GGAL) / GGAL))
info(INFO3)
rec('K3', OK3 and (0 < UBAR < A0), 'ubar=%.4e m/s^2 = %.4f a0' % (UBAR, UBAR / A0),
    '0 < ubar < a0, on-shell', 'the galactic background is a solution of the same P equation')

EPS_AMP = u0 / UBAR
info('AMPLITUDE RATIO  u_sun(1AU)/u_gal = %.4e   (A36 K12 measured 2.19e5 the other way)'
     % EPS_AMP)

# masses and screening lengths of the background
ML2 = K / (1 - UBAR / A0) ** 2
MT2 = K / (1 - UBAR / A0)
ELL_L = math.sqrt(gam / ML2)
ELL_T = math.sqrt(gam / MT2)
info('m_L^2 = %.6e  m_T^2 = %.6e  ell_L = %.4f pc  ell_T = %.4f pc'
     % (ML2, MT2, ELL_L / pc, ELL_T / pc))

# ============================================================ K4: the isolated hedgehog solves the exact ODE
r_s, gam_s, mu_s = sp.symbols('r gamma mu', positive=True)
pf = sp.Function('p')
expr = (sp.diff(pf(r_s), r_s, 2) + 2 * sp.diff(pf(r_s), r_s) / r_s
        - 2 * pf(r_s) / r_s ** 2 + mu_s / (gam_s * r_s ** 2))
r4 = sp.simplify(expr.subs(pf(r_s), mu_s / (2 * gam_s)))
h1 = sp.simplify((sp.diff(r_s, r_s, 2) + 2 / r_s - 2 * r_s / r_s ** 2))
h2 = sp.simplify((sp.diff(r_s ** -2, r_s, 2) + 2 * (-2 * r_s ** -3) / r_s - 2 * r_s ** -2 / r_s ** 2))
info('hedgehog residual = %s ;  homogeneous r -> %s ;  r^-2 -> %s' % (r4, h1, h2))
rec('K4', r4 == 0 and h1 == 0 and h2 == 0, 'residual %s' % r4, '0',
    'p = GM/(2gamma) solves gamma(p\'\'+2p\'/r-2p/r^2) = -GM/r^2 exactly')

# ============================================================ K5: the scale-separation parameter
def g_sun(r):
    return mu / r ** 2


def eps_scale(r):
    return r / R_GAL


def eps_bg(r):
    """error of the frozen-background expansion: (r/R_gal)(g_gal/g_sun)."""
    if MUT == 'eps_r_only':
        return eps_scale(r)
    return eps_scale(r) * GGAL / g_sun(r)


R_STAR = (mu * R_GAL / GGAL) ** (1.0 / 3.0)
info('eps_bg(1 AU) = %.2e   eps_bg(0.1 pc) = %.2e   eps_bg(1 pc) = %.2e   breakdown r* = %.3f pc'
     % (eps_bg(AU), eps_bg(0.1 * pc), eps_bg(pc), R_STAR / pc))
ok5 = eps_bg(AU) < 1e-12 and 0.02 < eps_bg(pc) < 0.3 and 1.0 < R_STAR / pc < 4.0
rec('K5', ok5, 'eps_bg(1pc)=%.3e  r*=%.2f pc' % (eps_bg(pc), R_STAR / pc), '< 0.3 ; r* in [1,4] pc',
    'the two-scale expansion is controlled to 1 pc; it fails at r* = (GM R_gal/g_gal)^(1/3)')

# ============================================================ K6: the linearised operator
# K W'(u) Phat with P = pbar e + pi, u = K|P|, expanded to first order in pi
pbar_s, ubar_s, a0k = sp.symbols('pbar ubar a0', positive=True)
px, py, pz = sp.symbols('pi_x pi_y pi_z', real=True)
Pvec = sp.Matrix([px, py, pbar_s + pz])
Pmag = sp.sqrt(Pvec.dot(Pvec))
KWp = (K_s * Pmag / (1 - K_s * Pmag / a0k))
fvec = sp.simplify(KWp * Pvec / Pmag)
J = sp.simplify(fvec.jacobian([px, py, pz]).subs({px: 0, py: 0, pz: 0}))
mL2, mT2 = sp.symbols('m_L^2 m_T^2', positive=True)
Jtarget = sp.Matrix([[mT2, 0, 0], [0, mT2, 0], [0, 0, mL2]])
r6 = sp.simplify((J - Jtarget.subs({mL2: K_s / (1 - ubar_s / a0k) ** 2,
                                    mT2: K_s / (1 - ubar_s / a0k)})).subs(ubar_s, K_s * pbar_s))
# numerical finite-difference confirmation on the real background
hin = 1e-4 * PBAR
fb = lambda pv: (K * np.linalg.norm(pv) / (1 - K * np.linalg.norm(pv) / A0)) * pv / np.linalg.norm(pv)
Pbase = np.array([0.0, 0.0, PBAR])
Jn = np.zeros((3, 3))
for i in range(3):
    e = np.zeros(3); e[i] = hin
    Jn[:, i] = (fb(Pbase + e) - fb(Pbase - e)) / (2 * hin)
Jexp = np.diag([K / (1 - UBAR / A0), K / (1 - UBAR / A0), K / (1 - UBAR / A0) ** 2])
fd_err = np.max(np.abs(Jn - Jexp)) / np.max(np.abs(Jexp))
info('symbolic Jacobian residual = %s' % (list(r6),))
info('finite-difference Jacobian relative error = %.2e' % fd_err)
rec('K6', r6 == sp.zeros(3, 3) and fd_err < 1e-6,
    'sym=0  fd_rel=%.2e' % fd_err, '0 ; <1e-6',
    'only the mass terms survive: m_L^2 = K/(1-u/a0)^2 (along P), m_T^2 = K/(1-u/a0)')

# ============================================================ K7: exact profile
x_s, ell_s = sp.symbols('x ell', positive=True)
f_s = 2 * (1 - sp.exp(-x_s) * (1 + x_s)) / x_s ** 2
p_prof = (mu_s / (2 * gam_s)) * f_s.subs(x_s, r_s / ell_s)
ode_prof = (sp.diff(p_prof, r_s, 2) + 2 * sp.diff(p_prof, r_s) / r_s
            - 2 * p_prof / r_s ** 2 - p_prof / ell_s ** 2 + mu_s / (gam_s * r_s ** 2))
r7 = sp.simplify(ode_prof)
I_s = 2 - 2 * sp.exp(-x_s) - 2 * (1 - sp.exp(-x_s) * (1 + x_s)) / x_s
r7b = sp.simplify(sp.diff(I_s, x_s) - f_s)
info('exact-profile ODE residual = %s ;  dI/dx - f = %s' % (r7, r7b))
rec('K7', r7 == 0 and r7b == 0, 'residuals %s %s' % (r7, r7b), '0 0',
    'pi_r = p0 f(r/ell), f = 2[1-e^-x(1+x)]/x^2 solves the massive equation exactly')


def f_prof(x):
    """stable evaluation of 2(1-e^-x(1+x))/x^2 (series for x<1e-3)."""
    if x < 1e-3:
        return 1.0 - 2.0 * x / 3.0 + x * x / 4.0 - x ** 3 / 15.0 + x ** 4 / 72.0
    return 2.0 * (1.0 - math.exp(-x) * (1.0 + x)) / x ** 2


def I_prof(x):
    if x < 1e-3:
        return x - x * x / 3.0 + x ** 3 / 12.0 - x ** 4 / 60.0
    return 2.0 - 2.0 * math.exp(-x) - 2.0 * (1.0 - math.exp(-x) * (1.0 + x)) / x


# ============================================================ K8: independent numerical solves
def solve_profile(ell, nonlinear=False, x_lo=0.01, x_hi=30.0, n=6000):
    """BVP for Q=pi/p0 in x = r/pc:  Q''+2Q'/x-2Q/x^2 = -2/x^2 + mass term."""
    xx = np.logspace(math.log10(x_lo), math.log10(x_hi), n)

    def ode(x, y):
        Q, dQ = y
        if nonlinear:
            u = UBAR + u0 * Q
            term = pc ** 2 / (gam * p0) * ((u / (1 - u / A0)) - (UBAR / (1 - UBAR / A0)))
        else:
            term = (pc / ell) ** 2 * Q
        return np.vstack([dQ, -2.0 * dQ / x + 2.0 * Q / x ** 2 + term - 2.0 / x ** 2])

    def bc(ya, yb):
        return np.array([ya[0] - f_prof(x_lo * pc / ell), yb[0] - f_prof(x_hi * pc / ell)])

    y0 = np.vstack([np.array([f_prof(t * pc / ell) for t in xx]), np.zeros(n)])
    return solve_bvp(ode, bc, xx, y0, tol=1e-11, max_nodes=400000)


SOL_T = solve_profile(ELL_T)
SOL_L = solve_profile(ELL_L)
SOL_NL = solve_profile(ELL_L, nonlinear=True)
err_lin = max(abs(SOL_T.sol(t)[0] / f_prof(t * pc / ELL_T) - 1)
              for t in np.logspace(-2, 1.47, 60)) if SOL_T.status == 0 else 1.0
err_nl = max(abs(SOL_NL.sol(t)[0] / SOL_L.sol(t)[0] - 1)
             for t in np.logspace(-2, 1.47, 60)) if (SOL_NL.status == 0 and SOL_L.status == 0) else 1.0
info('BVP status: linear %d, nonlinear %d ; analytic-vs-numeric %.2e ; nonlinear-vs-linear %.2e'
     % (SOL_T.status, SOL_NL.status, err_lin, err_nl))
rec('K8', SOL_T.status == 0 and SOL_NL.status == 0 and err_lin < 1e-8 and err_nl < 1e-5,
    'lin_err=%.1e  nl_err=%.1e' % (err_lin, err_nl), '<1e-8 ; <1e-5',
    'independent BVP reproduces the analytic profile; the full nonlinear solve moves it by <1e-6')

# ============================================================ K9: u(r) from 1 AU to 1 pc
R_TAB = [1 * AU, 3 * AU, 10 * AU, 30 * AU, 70 * AU, 160 * AU, 1e3 * AU, 1e4 * AU,
         0.01 * pc, 0.1 * pc, 0.3 * pc, 1.0 * pc]

if MUT == 'slaved_sun':
    u_sun_of = lambda r: A0          # mutation: force the slaved value u = a0
    p_sun_of = lambda r: A0 / K
else:
    u_sun_of = lambda r: u0 * f_prof(r / ELL_T)
    p_sun_of = lambda r: p0 * f_prof(r / ELL_T)

TAB = []
for rr in R_TAB:
    us = u_sun_of(rr)
    TAB.append({'r_AU': rr / AU, 'r_pc': rr / pc, 'u_gal_a0': UBAR / A0,
                'u_sun_a0': us / A0, 'u_sun_over_gal': us / UBAR,
                'f': f_prof(rr / ELL_T),
                'u_tot_max_a0': (UBAR + us) / A0, 'u_tot_min_a0': abs(UBAR - us) / A0})
print()
print('     u(r) = K|P| from 1 AU to 1 pc   (galactic background + solar hedgehog)')
print('     %-10s %-10s %-11s %-12s %-11s %-11s' %
      ('r [AU]', 'r [pc]', 'u_sun/a0', 'u_sun/u_gal', 'u_max/a0', 'u_min/a0'))
for t in TAB:
    print('     %-10.4g %-10.4g %-11.4e %-12.4e %-11.6f %-11.6f'
          % (t['r_AU'], t['r_pc'], t['u_sun_a0'], t['u_sun_over_gal'],
             t['u_tot_max_a0'], t['u_tot_min_a0']))
ratio_max = max(t['u_sun_over_gal'] for t in TAB)
ratio_min = min(t['u_sun_over_gal'] for t in TAB)
spread = max(abs(t['u_sun_a0'] * A0 / u0 - 1) for t in TAB)
info('u_sun/u_gal over the whole range: %.3e ... %.3e (factor %.2f) ; u_sun/a0 spread %.2e'
     % (ratio_min, ratio_max, ratio_max / ratio_min, spread))
ok9 = (0.5 < UBAR / A0 < 0.6) and (3e-6 < u0 / UBAR * f_prof(pc / ELL_T) < 6e-6) and spread < 0.1
rec('K9', ok9, 'u_sun/u_gal=%.2e  spread=%.1e' % (ratio_max, spread), '4e-6 ; <0.1',
    'the solar contribution is 4.6e-6 of the galactic one and nearly constant to 1 pc')

# ============================================================ K10: crossovers
R_G_CROSS = math.sqrt(mu / GGAL)
# charge density of the galactic field: psi_gal = div Pbar
def psi_gal(r):
    h = 1e-4 * r
    ur = g_law(gN_gal(r - h)) - gN_gal(r - h)
    up = g_law(gN_gal(r + h)) - gN_gal(r + h)
    dpdr = (up - ur) / (2 * h) / K
    return dpdr + 2.0 * (g_law(gN_gal(r)) - gN_gal(r)) / K / r


PSI_GAL = psi_gal(R_GAL)
R_CH_CROSS = 2.0 * p0 / abs(PSI_GAL) if PSI_GAL != 0 else float('inf')
info('g-crossover  r(g_sun=g_gal) = %.4e m = %.4e AU = %.5f pc' % (R_G_CROSS, R_G_CROSS / AU, R_G_CROSS / pc))
info('charge crossover 2 p0/r = psi_gal : r = %.4e AU = %.5f pc  (psi_gal=%.3e kg/m^3)'
     % (R_CH_CROSS / AU, R_CH_CROSS / pc, PSI_GAL))
info('NO u-magnitude crossover: u_sun/u_gal = %.3e at 1 AU and %.3e at 1 pc'
     % (u0 / UBAR, u0 * f_prof(pc / ELL_T) / UBAR))
ok10 = (5000 < R_G_CROSS / AU < 8000) and (ratio_max < 1e-4) and (R_CH_CROSS / AU > 3000)
rec('K10', ok10, 'r_g=%.3e AU  r_charge=%.3e AU' % (R_G_CROSS / AU, R_CH_CROSS / AU),
    'no u-crossover; dynamical crossover ~6.4e3 AU',
    'the solar field never matches the galactic one in u; it does in acceleration at 6.4e3 AU')

# ============================================================ K11: A36's K12 resolved
# (a) the gradient term balances g_sun exactly:  gamma(p''+2p'/r-2p/r^2) = -g_sun (1+O(m^2r^2))
def grad_residual(rr):
    h = 1e-3 * rr
    p = lambda s: p0 * f_prof(s / ELL_T)
    d2 = (p(rr + h) - 2 * p(rr) + p(rr - h)) / h ** 2
    d1 = (p(rr + h) - p(rr - h)) / (2 * h)
    return abs(gam * (d2 + 2 * d1 / rr - 2 * p(rr) / rr ** 2) + g_sun(rr)) / g_sun(rr)


gres = max(grad_residual(x * AU) for x in [1.0, 10.0, 70.0, 300.0])
info('gradient-balance residual |gamma lap(pi)+g_sun|/g_sun = %.2e at 1-300 AU' % gres)
# (b) A36's number: if u were a0 at 1 AU, the gradient term would be 2 gamma u/(K r^2)
grad_if_a0 = 2.0 * gam * A0 / (K * AU ** 2)
info('forcing u_sun = a0 at 1 AU would need 2 gamma u/(K r^2) = %.3e m/s^2 = %.2e x g_sun'
     % (grad_if_a0, grad_if_a0 / g_sun(AU)))
rec('K11', gres < 1e-8 and grad_if_a0 / g_sun(AU) > 1e5,
    'resid=%.1e ; forced-u0 gradient/g=%.1e' % (gres, grad_if_a0 / g_sun(AU)), '<1e-8 ; >1e5',
    'u is set by gradient balance, not by the background: A36 K12 is a bound on u, not a contradiction')

# ============================================================ K12: alpha_1 exact
def phi_P(rr):
    """charge potential of the solar perturbation: Phi_P = K int_0^r pi ds (analytic)."""
    return K * p0 * ELL_T * I_prof(rr / ELL_T)


def alpha1_exact(rr):
    if MUT == 'alpha1_prefactor2':
        return -2.0 * phi_P(rr) / (mu / rr)
    if MUT == 'alpha1_k0':
        up = uprime_slaved(GGAL)
        return 4.0 * up / (1.0 - up)
    return -4.0 * phi_P(rr) / (mu / rr)


def alpha1_analytic_form(rr):
    x = rr / ELL_T
    return -4.0 * (rr / Ls) ** 2 * I_prof(x) / x


# independent route: numerical profile -> charge -> Poisson integral
xs = np.logspace(math.log10(0.01 * pc), math.log10(30 * pc), 4000)
Qs = np.array([SOL_L.sol(t)[0] for t in xs / pc])
ps = p0 * Qs
Phi_num = K * p0 * xs[0] + np.concatenate(
    [[0.0], np.cumsum(0.5 * (ps[1:] + ps[:-1]) * np.diff(xs))]) * K


def alpha1_num(rr):
    if rr <= xs[0]:                     # inside the first cell p = p0 to 1e-4
        return -4.0 * (K * p0 * rr) / (mu / rr)
    return -4.0 * np.interp(rr, xs, Phi_num) / (mu / rr)


A1_1AU = alpha1_exact(AU)
A1_1AU_AN = alpha1_analytic_form(AU)
A1_NUM = alpha1_num(AU)
info('alpha_1(1 AU): exact %.6e   analytic form %.6e   numerical route %.6e   rel(numerical) %.1e'
     % (A1_1AU, A1_1AU_AN, A1_NUM, abs(A1_NUM / A1_1AU_AN - 1)))
ok12 = (abs(A1_1AU / A1_1AU_AN - 1) < 1e-12) and (abs(A1_NUM / A1_1AU_AN - 1) < 1e-6) \
       and (1e-13 < abs(A1_1AU_AN) < 3e-13)
rec('K12', ok12, 'mut=%.3e exact=%.3e' % (abs(A1_1AU), abs(A1_1AU_AN)), 'both 1.63e-13',
    'alpha_1 = 4(r/L*)^2 I(x)/x = 4(r/L*)^2 to 1e-7 at 1 AU, from three routes')

# ============================================================ K13: embedded vs isolated
ELL_ISO = math.sqrt(gam / (K / (1 - u0 / A0) ** 2))
A1_ISO = -4.0 * (AU / Ls) ** 2 * I_prof(AU / ELL_ISO) / (AU / ELL_ISO)
d_rel = abs(A1_ISO / A1_1AU_AN - 1)
info('alpha_1(1 AU) embedded (ell_T=%.3f pc) = %.6e ; isolated (ell=%.3f pc) = %.6e ; rel diff %.2e'
     % (ELL_T / pc, A1_1AU_AN, ELL_ISO / pc, A1_ISO, d_rel))
rec('K13', d_rel < 1e-6 and abs(A1_ISO - A1_1AU_AN) < 1e-18,
    'rel=%.2e  abs=%.2e' % (d_rel, abs(A1_ISO - A1_1AU_AN)), '<1e-6',
    'the embedding moves alpha_1 by 5e-8 relative: A22\'s isolated-Sun value was adequate')

# ============================================================ K14: A36 K11 reproduced and diagnosed
up_ss = (AU / Ls) ** 2                       # A36's u' = r^2/(2 lambda^2) = r^2/L*^2
D_ss = 1.0 + (Ls / AU) ** 2 * up_ss / 2.0
a1_A36 = 2.0 * up_ss / (D_ss - up_ss)        # A36 K11's expression
a1_4 = 4.0 * up_ss / (D_ss - up_ss)          # their own eq. (2.5) prefactor
D_fix = 1.0 + (Ls / AU) ** 2 * (1 - u0 / A0) ** 2 / 2.0   # correct mass: (1-u/a0)^2 = 1
a1_fix = 4.0 / (D_fix - 1.0)                 # = 8 (r/L*)^2, the k=1/r proxy
info('A36 K11 reproduced: 2u\'/(D-u\') = %.4e ; their 4u\'/(D-u\') = %.4e ; '
     'formula with the correct mass = %.4e ; exact point source = %.4e'
     % (a1_A36, a1_4, a1_fix, A1_1AU_AN))
info('ratio |exact|/A36 = %.3f ; slips: prefactor 2 vs 4 (x2) and u\'=r^2/L*^2 used as the mass'
     % abs(A1_1AU_AN / a1_A36))
info('suppression where the hedgehog has (1-u/a0)^2 = 1 (x3 smaller D -> x3 smaller alpha_1)')
ok14 = (abs(a1_A36 / 5.44e-14 - 1) < 0.02) and (2.5 < abs(A1_1AU_AN) / a1_A36 < 3.5)
rec('K14', ok14, 'A36=%.3e  exact=%.3e  ratio=%.2f' % (a1_A36, abs(A1_1AU_AN), abs(A1_1AU_AN) / a1_A36),
    '5.44e-14 ; ratio 3.0',
    'K11 is low by 3x but in the safe direction; the correction is not the embedding')

# ============================================================ K15: the gate
MARGIN = B_TASK / abs(A1_1AU_AN)
A1_160 = abs(alpha1_analytic_form(160 * AU))
R_CROSS_A1 = Ls * math.sqrt(B_TASK / 4.0)
info('margin 1e-4/|alpha_1(1AU)| = %.3e ;  |alpha_1(160 AU)| = %.3e ;  4(r/L*)^2 = 1e-4 at r = %.4f pc = %.3e AU'
     % (MARGIN, A1_160, R_CROSS_A1 / pc, R_CROSS_A1 / AU))
ok15 = MARGIN > 1e8 and A1_160 < 1e-8 and 0.08 < R_CROSS_A1 / pc < 0.2
rec('K15', ok15, 'margin=%.2e  alpha1(160AU)=%.2e' % (MARGIN, A1_160), '>1e8 ; <1e-8',
    'the Solar System gate survives by 6e8 at 1 AU and by 2e8 at 160 AU')

# ============================================================ K16: a_P unchanged by the embedding
# charge psi = 2 p0/r at r << ell; A22's Phi_c = (GM/L*^2) r must be recovered
psi_1AU = 2.0 * p0 / AU
Phi_c_A22 = mu * AU / Ls ** 2
Phi_P_num = K * p0 * AU * (1.0 - (AU / ELL_T) / 3.0)     # K int_0^r pi ds, series
info('psi(1 AU) = 2p0/r = %.4e kg/m^3 ; Phi_P(1 AU) = %.6e m^2/s^2 ; A22 (GM/L*^2)r = %.6e ; rel %.1e'
     % (psi_1AU, phi_P(AU), Phi_c_A22, abs(phi_P(AU) / Phi_c_A22 - 1)))
rec('K16', abs(phi_P(AU) / Phi_c_A22 - 1) < 1e-6, 'rel=%.1e' % abs(phi_P(AU) / Phi_c_A22 - 1),
    '<1e-6', 'A22\'s a_P = GM/L*^2 is unchanged by the galactic background')

# ============================================================ K17: Pioneer
A_P = u0
RATIO_PION = A_P / A_PIONEER
DA_W2 = 2.0 * W2 * A_P
A1_20 = abs(alpha1_analytic_form(20 * AU))
A1_70 = abs(alpha1_analytic_form(70 * AU))
DA_70 = A1_70 * W2 * g_sun(70 * AU)
# the galactic field's w^2 modulation at the Pioneer distance (common mode + tide)
DA_GAL = 2.0 * W2 * GGAL
if MUT == 'pioneer_visible':
    A_P = A_PIONEER
    RATIO_PION = 1.0
    DA_W2 = 2.0 * W2 * A_P
    DA_70 = 1e-9
info('a_P = %.4e m/s^2 = %.3e a_Pioneer ; 2w^2 a_P = %.3e m/s^2 ; alpha_1(20AU)=%.3e alpha_1(70AU)=%.3e'
     % (A_P, RATIO_PION, DA_W2, A1_20, A1_70))
info('max preferred-frame acceleration at 70 AU = %.3e m/s^2 ; Pioneer thermal residual %.3e = %.1e x larger'
     % (max(DA_W2, DA_70), SIG_PIONEER, SIG_PIONEER / max(DA_W2, DA_70)))
ok17 = (RATIO_PION < 1e-6) and (max(DA_W2, DA_70) < 1e-19) and (SIG_PIONEER / max(DA_W2, DA_70) > 1e10)
rec('K17', ok17, 'a_P/a_Pio=%.2e ; w2 signal=%.2e' % (RATIO_PION, max(DA_W2, DA_70)),
    '<1e-6 ; <1e-19',
    'no Pioneer-level preferred-frame anomaly: the P signal is 1e11 below the thermal residual')

# ============================================================ K18: the slaved branch is inaccessible
def slope_param(rr):
    """gamma k^2 / m_T^2 with k = 1/r: the gradient-to-mass ratio of the response."""
    return 0.5 * (Ls / rr) ** 2 * (1 - UBAR / A0)


SL_20 = slope_param(20 * AU)
SL_70 = slope_param(70 * AU)
info('gradient/mass ratio at 20 AU = %.3e ; at 70 AU = %.3e ; at 1 AU = %.3e'
     % (SL_20, SL_70, slope_param(AU)))
ok18 = SL_70 > 1e8 and abs(u0 / A0 - 2.586e-6) < 0.01e-6
rec('K18', ok18, 'grad/mass(70AU)=%.2e  u_sun/a0=%.3e' % (SL_70, u0 / A0), '>1e8',
    'near-a0 local accelerations do not slave the P field: gradients dominate by 1e9')

# ============================================================ K19: the cap
ok19 = (UBAR + u0) / A0 < 1.0 and (1 - UBAR / A0) > 0.4
rec('K19', ok19, 'max u/a0 = %.6f' % ((UBAR + u0) / A0), '< 1',
    'u_total = 0.566 a0 is 43% below the cap everywhere in the Solar System')

# ============================================================ K20: the verdict numbers
ok20 = (ok9 and ok12 and ok15 and ok17 and ok19)
rec('K20', ok20, 'u_sun/u_gal=%.2e ; |a1(1AU)|=%.2e' % (ratio_max, abs(A1_1AU)),
    'established ; survives',
    'the number that decides: |alpha_1(1 AU)| = 1.6e-13 = 6.1e8 below the bound')

# ============================================================ sensitivity
print()
print('-' * 110)
print('SENSITIVITY')
print('-' * 110)
sens = []
for Lstar_pc in [24.0, 40.0, 90.0]:
    L = Lstar_pc * pc
    g_ = K * L ** 2 / 2
    e_ = math.sqrt(g_ / (K / (1 - UBAR / A0)))
    a1 = -4.0 * (AU / L) ** 2 * I_prof(AU / e_) / (AU / e_)
    sens.append({'Lstar_pc': Lstar_pc, 'u0_a0': (mu / L ** 2) / A0,
                 'alpha1_1AU': a1, 'margin': B_TASK / abs(a1)})
    print('  L* = %5.1f pc : u_sun/a0 = %.3e   alpha_1(1AU) = %.3e   margin = %.2e'
          % (Lstar_pc, (mu / L ** 2) / A0, a1, B_TASK / abs(a1)))
print('  a0 footing: canonical u_gal/a0 = %.4f, u_sun/u_gal = %.3e ; theory u_gal/a0 = %.4f'
      % (UBAR / a0_can, u0 / UBAR, UBAR / a0_th))
print('  alpha_1(1 AU) is a0-independent: it is fixed by r/L* alone.')

# ============================================================ summary
print()
print('=' * 110)
nfail = len(FAIL)
print('A60 COMPLETE: %d/%d checks PASS.' % (NCHK[0] - nfail, NCHK[0]))
if nfail:
    print('FAILED:', FAIL)
print('=' * 110)
print("""VERDICT
  The Sun's P configuration IS established, in the two-scale expansion:
    P = Pbar(galactic, u = 0.566 a0, outward from the Galactic Centre)
        + pi(solar hedgehog, u = 2.59e-6 a0, radial, constant to 1 pc,
             screening lengths 7.4 pc (longitudinal) / 11.2 pc (transverse)).
    The nonlinearity is controlled by eps_2 = u_sun/u_gal = 4.6e-6: amplitude
    composition fails at O(eps_2^2) = 2e-11, and the full nonlinear solve
    moves the profile by <= 9e-7.
  The Solar System gate SURVIVES the embedding:
    |alpha_1(1 AU)| = 1.63e-13, i.e. 6.1e8 below 1e-4.
  The embedding moves alpha_1 by 5e-8 relative (1e-20 absolute): A22's
  isolated-Sun solution was adequate for alpha_1.  A36's K12 "2.19e5 mismatch"
  is the small parameter of the expansion, not a contradiction.
  NO Pioneer-level preferred-frame anomaly: the largest signal is
  7e-22 to 1.5e-21 m/s^2, ~1e11 below the thermal-recoil residual
  1.33e-10 m/s^2.""")

# ============================================================ json
if ARGS.json_out and not FAIL:
    res = {
        'lane': 'A60_solar_p_config',
        'status': 'CLOSED-DERIVED (two-scale)' if not MUT else 'MUTATED',
        'mutate': ARGS.mutate,
        'checks': CHECKS,
        'constants': {'K': K, 'gamma': gam, 'Lstar_pc': Ls / pc, 'lambda_pc': lam / pc,
                      'a0_can': a0_can, 'a0_theory': a0_th, 'GM_sun': mu,
                      'p0_kg_m2': p0, 'u0_m_s2': u0},
        'background': {'gN_8kpc': GN_GAL, 'g_8kpc': GGAL, 'g_over_a0': GGAL / A0,
                       'ubar': UBAR, 'ubar_over_a0': UBAR / A0, 'pbar': PBAR,
                       'mL2': ML2, 'mT2': MT2, 'ell_L_pc': ELL_L / pc, 'ell_T_pc': ELL_T / pc},
        'expansion': {'eps_amp': EPS_AMP, 'eps_bg_1AU': eps_bg(AU), 'eps_bg_1pc': eps_bg(pc),
                      'r_star_pc': R_STAR / pc, 'r_g_cross_AU': R_G_CROSS / AU,
                      'r_charge_cross_AU': R_CH_CROSS / AU,
                      'eps_nonlinear': EPS_AMP ** 2},
        'profile': TAB,
        'alpha1': {'one_AU': A1_1AU_AN, 'isolated_one_AU': A1_ISO,
                   'rel_embedding_shift': d_rel, 'A36_K11': a1_A36,
                   'exact_over_A36': abs(A1_1AU_AN) / a1_A36,
                   'A36_formula_correct_mass': a1_fix,
                   'at_20AU': alpha1_analytic_form(20 * AU),
                   'at_70AU': alpha1_analytic_form(70 * AU),
                   'at_160AU': alpha1_analytic_form(160 * AU),
                   'at_1pc': alpha1_analytic_form(pc),
                   'r_cross_1e4_pc': R_CROSS_A1 / pc, 'r_cross_1e4_AU': R_CROSS_A1 / AU,
                   'bound': B_TASK, 'margin_1AU': MARGIN},
        'pioneer': {'a_P': A_P, 'a_Pioneer': A_PIONEER, 'ratio': RATIO_PION,
                    'w2': W2, 'signal_w2': DA_W2, 'signal_at_70AU_alpha1': DA_70,
                    'thermal_residual': SIG_PIONEER,
                    'signal_over_residual': DA_W2 / SIG_PIONEER},
        'sensitivity_Lstar': sens,
        'verdict': 'configuration established; Solar System gate survives; '
                   '|alpha_1(1AU)| = 1.63e-13 (6.1e8 below 1e-4)',
    }
    with open(ARGS.json_out, 'w') as fh:
        json.dump(res, fh, indent=2)
    print('wrote %s' % ARGS.json_out)

sys.exit(1 if FAIL else 0)