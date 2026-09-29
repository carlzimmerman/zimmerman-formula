#!/usr/bin/env python3
"""
CFG153 POSTHOC_1 (written AFTER the frozen runs and after reading CFG123's outputs; not evidence).

Question: my m/H0 = 0.283768 (start x_i = -18) differs from CFG123's 0.283934 by 5.8e-4 (relative).
CFG123's background (cfg123_common.rr_solve) starts at a = 1e-6 (x_i = -13.82) with zero data.
Does my own background system, started at the same a = 1e-6, give CFG123's number?

It re-uses the background equations my main run derived (read from cfg153_rr_weak_field_results.json),
re-integrates them from several start times, and recomputes the two pinned canonical |R_A| values.
Outputs: POSTHOC_1_start_time.out and POSTHOC_1_start_time_results.json beside this file.  Exit 0.
"""
import os
import sys
import json
import math
import hashlib

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.normpath(os.path.join(HERE, '..', 'CFG153_FROZEN_CRITERIA.md'))
out = open(os.path.join(HERE, 'POSTHOC_1_start_time.out'), 'w')


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    out.write(s + '\n')


P('frozen criteria: ../CFG153_FROZEN_CRITERIA.md  sha256 =', hashlib.sha256(open(SPEC, 'rb').read()).hexdigest())
P('POSTHOC_1 (after the frozen runs; not evidence): start time of the background integration')
d = json.load(open(os.path.join(HERE, 'cfg153_rr_weak_field_results.json')))
be = d['background_equations']
S = {n: sp.Symbol(n) for n in ('A_sc', 'U0', 'U1', 'L0', 'L1', 'H', 'mu', 'Omega_m', 'Omega_r', 'Omega_L')}
H2 = sp.sympify(be['H2'], locals=S)
dyn = [sp.sympify(be[k], locals=S) for k in ('zeta', 'U2', 'L2')]
x = sp.Symbol('x')
args = (x, S['U0'], S['U1'], S['L0'], S['L1'], S['mu'], S['Omega_m'], S['Omega_r'], S['Omega_L'])
fh2 = sp.lambdify(args, H2.subs(S['A_sc'], sp.exp(x)), 'numpy')
fdyn = sp.lambdify((x, S['U0'], S['U1'], S['L0'], S['L1'], S['H'], S['mu'], S['Omega_m'], S['Omega_r'], S['Omega_L']),
                   [e.subs(S['A_sc'], sp.exp(x)) for e in dyn], 'numpy')
Om, Or = 0.3153, 4.15e-5 / 0.6736 ** 2


def rhs(xv, y, mu):
    h2 = fh2(xv, *y, mu, Om, Or, 0.0)
    z, u2, l2 = fdyn(xv, *y, math.sqrt(h2), mu, Om, Or, 0.0)
    return [y[1], u2, y[3], l2]


def h2_today(mu, xi):
    s = solve_ivp(rhs, (xi, 0.0), [0.0] * 4, method='DOP853', rtol=1e-11, atol=1e-14, args=(mu,))
    return fh2(0.0, *s.y[:, -1], mu, Om, Or, 0.0), s.y[:, -1]


rows = {}
for label, xi in (('a_i = 1e-6 (CFG123)', math.log(1e-6)), ('x_i = -15', -15.0), ('x_i = -18 (frozen)', -18.0),
                  ('x_i = -21', -21.0), ('x_i = -24', -24.0)):
    mu = brentq(lambda m: h2_today(m, xi)[0] - 1.0, 0.1, 0.5, xtol=1e-14, rtol=1e-13)
    y = h2_today(mu, xi)[1]
    rows[label] = {'x_i': xi, 'm_over_H0': mu, 'U_bar_0': float(y[0]), 'H0sq_S_bar_0': float(3 * y[2] / mu ** 2)}
    P('  %-22s x_i = %8.4f : m/H0 = %.6f ; U-bar(0) = %.4f ; H0^2 S-bar(0) = %.4f'
      % (label, xi, mu, y[0], 3 * y[2] / mu ** 2))
P('  CFG123 printed (A4 .out): m/H0 = 0.283934, U-bar = 16.035, S-bar = 2.064 (A2 .out embedding scan)')

# pinned canonical |R_A| with each m (my constants; exact linear form, cos(mr) factor included)
GMSUN, c, kpc = 1.32712440018e20, 299792458.0, 3.0856775814913673e19
H0 = 67.36e3 / (kpc * 1e3)
a0 = 9.3603e-11


def RA(mu, n, xg):
    GM = n * GMSUN
    rM = math.sqrt(GM / a0)
    m = mu * H0 / c
    return (m ** 2 * GM / (3 * a0)) * math.sqrt(1 + xg ** 2) * math.cos(m * xg * rM)


for mu, lab in ((rows['x_i = -18 (frozen)']['m_over_H0'], 'mine (x_i = -18)'),
                (rows['a_i = 1e-6 (CFG123)']['m_over_H0'], 'mine started at a = 1e-6'), (0.283934, 'CFG123 m')):
    P('  |R_A| canonical with %-26s: (1e9, 0.1) = %.4e ; (1e12, 30) = %.4e' % (lab, RA(mu, 1e9, 0.1), RA(mu, 1e12, 30.0)))
P('  CFG123 A2 .out prints the canonical range [2.030e-15, 6.064e-11].')
json.dump({'rows': rows, 'note': 'post hoc, not evidence'}, open(os.path.join(HERE, 'POSTHOC_1_start_time_results.json'), 'w'),
          indent=1)
out.close()
sys.exit(0)
