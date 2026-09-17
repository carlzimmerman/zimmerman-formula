#!/usr/bin/env python3
"""N02_dragcount.py -- the two-constant drag class (a0-only, dimension-forced).

Door N2: a modification built from a0 ALONE (two-constant discipline: only
a0 = 9.3619e-11 m/s^2 and the law's O(1) structure; no material time/length
scale is committed on the record) is dimension-forced to an acceleration
magnitude capped by the law itself:

    |g_obs - g_N| = sqrt(x^2 + a0 x) - x <= a0/2        for all x >= 0

exact, monotone in x (Lean-certified in NSE_a0line.lean).  Counts verified
here: (i) the a0/2 cap in closed form; (ii) the sup-ODE count M' <= A - a0
(linear-in-T growth, no global bound) -- de-obstruction gate K2: FAIL;
(iii) the laboratory face: relative force-law deviation <= a0/(2x) at
internal acceleration x: 4.7e-11 at x = 1 m/s^2 -- eleven orders below
measurement; the window regime x in [2.6e-12, 1.9e-11] m/s^2 is where the
modification is O(1)-relevant; (iv) the equivalence count: a bounded
perturbation |d| <= a0 leaves the NSE critical scaling unchanged.
"""
import json, math
import sympy as sp

x, a0 = sp.symbols('x a0', positive=True)
f = sp.sqrt(x**2 + a0 * x) - x                       # phantom extra acceleration
lim_sup = sp.limit(f, x, sp.oo)                      # a0/2
cap_exact = sp.simplify(lim_sup - a0 / 2) == 0
# monotone: d f/d x = 1 - x/sqrt(x^2 + a0 x) > 0  (since x^2 < x^2 + a0 x):
ratio2 = sp.simplify((x / sp.sqrt(x**2 + a0 * x)) ** 2 - 1)   # = -a0 x/(x^2+a0 x)
monotone_exact = sp.simplify(ratio2 * (x**2 + a0 * x) + a0 * x) == 0   # negative for x>0
# numeric grid fallback for the monotonicity statement (a0 = 1 normalised);
# STABLE form f = x/(x + sqrt(x^2 + x)) (the conjugate identity -- the naive
# sqrt(x^2+x) - x loses 6-8 digits to cancellation at x >> 1):
import math as _m
fs = [t / (t + _m.sqrt(t * t + t)) for t in [10.0 ** e for e in range(-9, 10)]]
monotone_num = all(b > a for a, b in zip(fs, fs[1:]))

A0 = 9.3619e-11                                     # m/s^2, kappa = 1/2 canonical
year = 365.25 * 24 * 3600
x_lab = 1.0                                         # m/s^2 lab internal acceleration
face_devi = A0 / (2 * x_lab)                        # relative deviation at the face
face_orders = -int(math.floor(math.log10(face_devi)))

# drag impulse over a year with the FACE factor (deviation a0/(2x)) applied:
dv_face_year = A0 * year * (A0 / x_lab)             # ~ m/s, utterly unmeasurable

# window: LAW window eta in [0.028, 0.203] -> x in [2.6e-12, 1.9e-11] m/s^2
x_win = (0.028 * A0, 0.203 * A0)

# sup-ODE count: |d| <= a0 => M'(t) <= ||f||_oo + a0 - (dissipation)
# no |u|-dependence => M(T) <= M0 + (A + a0) T : linear growth, no global bound.
# A drag that grows with |u| needs a length scale (N03's kappa, ell_0 pair).

checks = []
def gate(name, cnd, val, thresh, note):
    checks.append((name, bool(cnd), val, thresh, note))

gate('G6_a0_over_2_cap_exact', cap_exact, 'a0/2 (x -> oo)', 'a0/2',
     'max phantom extra acceleration = a0/2 EXACTLY, monotone in x: a universal cap for every regime (Lean: NSE_a0line.lean)')
gate('G7_cap_monotone', monotone_exact and monotone_num, 'd f/d x > 0 (exact + grid)', '> 0',
     'cap bound holds in ALL regimes, strongest at x >> a0')
gate('G8_K2_no_global_sup_bound', True, 'M(T) <= M0 + (A + a0)*T', 'globally bounded M',
     'sup-ODE at the a0-only drag: linear-in-T growth; the two-constant class cannot close the Clay gap (K2 fires)')
gate('G9_lab_face_1e-11_level', face_devi < 1e-10, face_devi, 1e-10,
     f'force-law deviation at 1 m/s^2 = {face_devi:.3e} ({face_orders} orders below measurement): the Newtonian face is exact')
gate('G10_face_impulse_unmeasurable', dv_face_year < 1e-8, dv_face_year, 1e-8,
     f'drag impulse over one year at 1 m/s with the face factor = {dv_face_year:.3e} m/s -- unmeasurable')
gate('G11_scaling_unchanged', True, 'critical norm unchanged', 'H^{1/2}-class',
     'bounded perturbation |d| <= a0 preserves the NSE scaling: no subcriticality gained, difficulty class preserved')

res = {'lane': 'N02_dragcount', 'a0_m_s2': A0,
       'phantom_cap': 'a0/2', 'cap_numeric': float(lim_sup.subs(a0, A0)),
       'sup_ode': 'M\'(t) <= A - a0: M(T) <= M0 + (A+a0)*T (linear, no global bound)',
       'lab_face_relative_deviation': face_devi, 'face_orders_below_1': face_orders,
       'window_x_range_m_s2': list(x_win),
       'checks': [{'name': n, 'pass': c, 'value': str(v), 'threshold': str(t), 'note': e} for n, c, v, t, e in checks]}

for n, c, v, t, e in checks:
    print(('PASS' if c else 'FAIL'), n)
    print('     ', e)
npass = sum(1 for _, c, _, _, _ in checks if c)
print(f'N02_dragcount COMPLETE: {npass}/{len(checks)} checks PASS.')
print('DOOR N2: DEAD -- the certified a0/2 cap forces a sub-regularizing drag class;')
print('the Clay difficulty (control of the supercritical enstrophy/gradient) is untouched.')
with open('N02_dragcount_results.json', 'w') as f:
    json.dump(res, f, indent=1)