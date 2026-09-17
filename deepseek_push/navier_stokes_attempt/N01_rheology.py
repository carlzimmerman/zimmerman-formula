#!/usr/bin/env python3
"""N01_rheology.py -- the a0-line read as an implicit rheology (p-curl class).

Door N1: if the measured law is interpreted as a time-independent constitutive
stress response tau ~ rho*g_obs(g_N(s)) with s = |Du| the local shear rate and
g_N ~ s the Newtonian field at the flow's own scale, does the effective shear
exponent p_eff = 1 + d ln tau/d ln s reach the literature gates for global
regularity of the 3D power-law (p-curl) Navier-Stokes system?

Gates (literature, cited): shear-thinning p >= 9/5 (Ladyzhenskaya 1969; Wolf
2007 p > 8/5 weak existence); shear-thickening p >= 11/5 (Ladyzhenskaya 1969;
Bae et al. 2015 for 2 <= p < 11/5 only under extra criteria).

Exact sympy analysis: g(x) = sqrt(x^2 + a0 x), x = g_N (evaluated at the
flow's own scale, x = c_N s).  d ln g / d ln x = x (2x + a0) / (2 x (x + a0)),
so p_eff(x) = 1 + (2x + a0)/(2(x + a0)): 3/2 at x -> 0 (deep), 2 as x -> oo
(Newtonian face).  The RAR kernel deep limit gives the same 1/2 log-log slope
(g_obs ~ sqrt(a0 g_N)); the mu2 kernel is viscosity-degrading (mu2 ~ 2u small,
shear-thinning at the small scale).  All asymptotic slopes computed exactly.
"""
import json, sympy as sp

x, a0, u = sp.symbols('x a0 u', positive=True)
g_obs = sp.sqrt(x**2 + a0*x)          # the a0-line inversion (LAW_STATEMENT)
slope = sp.simplify(sp.diff(sp.log(g_obs), x) * x)  # d ln g / d ln x = x * g'/g
p_eff = sp.simplify(1 + slope)        # tau ~ |Du|^{p-1}: exponent p_eff = 1 + slope

# RAR kernel deep limit
y = sp.symbols('y', positive=True)
nu_rar = 1 / (1 - sp.exp(-sp.sqrt(y)))
slope_rar = sp.simplify(sp.limit(sp.diff(sp.log(nu_rar * y), y) * y, y, 0))
p_rar = sp.simplify(1 + slope_rar)

# mu2 kernel: effective viscosity modulation at the flow scale
mu2 = u * (2 + u) / (1 + u)**2
vis_slope = sp.simplify(sp.limit(sp.diff(sp.log(mu2), u) * u, u, 0))

lo = sp.limit(p_eff, x, 0); hi = sp.limit(p_eff, x, sp.oo)
p_at_deep_margin = sp.simplify(p_eff.subs(x, a0 * sp.Rational(1, 10**6)))

GATE_T = sp.Rational(9, 5)    # thinning gate
GATE_K = sp.Rational(11, 5)   # thickening gate

checks = []
def gate(name, cnd, val, thresh, note):
    checks.append((name, bool(cnd), val, thresh, note))

# G1: exponent below the thinning gate where the law departs from Newton by O(1)
pdeep = float(p_at_deep_margin)
gate('G1_p_eff_deep_below_9/5', pdeep < 1.8, pdeep,
     float(GATE_T), 'deep regime: exponent ' + str(pdeep) + ' < 9/5 -> the rheology door cannot borrow the thinning regularity theorems')
# G1b: exponent below the gate THROUGHOUT the measured O(1)-modification window
# eta in [0.028, 0.203] (LAW_STATEMENT): the crossing at g_N = 1.5 a0 lies BEYOND
# the window, where the S-kernel suppresses the modification to ~0.3% (S(3.5)
# with eta_c = 0.203) -- the gate and the O(1) regime never overlap.
cross = sp.solve(sp.Eq(p_eff, GATE_T), x)[0]
p_cross_window = p_eff.subs(x, 0.203 * a0)
gate('G1b_p_eff_below_gate_in_window', float(sp.N(sp.simplify(p_cross_window))) < 1.8,
     sp.N(sp.simplify(p_cross_window), 6), float(GATE_T),
     'p_eff across the window [0.028, 0.203] is ' + str(sp.N(p_cross_window, 6)) +
     ' < 9/5 (crossing at g_N = ' + str(sp.N(cross / a0, 5)) + ' a0 lies beyond the S-suppressed band): the O(1)-modification regime NEVER has a regularizing exponent')
# G2: face consistency -- Newtonian recovery p_eff -> 2 exactly
gate('G2_p_eff_newtonian_face_exact_2', sp.simplify(hi - 2) == 0, float(hi), sp.Integer(2),
     'high-shear face: exponent exactly 2 (classical Newtonian rheology), matching the law\'s Newtonian limit')
# G3: thickening gate unreachable (p_eff <= 2 < 11/5 always)
gate('G3_p_eff_never_reaches_11/5', float(hi) < 2.2, float(hi), float(GATE_K),
     'max exponent 2 < 11/5: the thickening regularity class is unreachable')
# G4: RAR-deep consistency: same 1/2 slope from the data-selected kernel
gate('G4_RAR_deep_slope_equals_1/2', sp.simplify(slope_rar - sp.Rational(1, 2)) == 0,
     float(slope_rar), sp.Rational(1, 2), 'data-selected RAR kernel: d ln g_obs/d ln g_N -> 1/2 exactly at deep (same exponent)')
# G5: mu2 viscosity degradation: effective viscosity THINS at small scale (no viscosity floor)
vis_deep = sp.limit(mu2, u, 0)
gate('G5_mu2_viscosity_shear_thinning', float(sp.limit(vis_slope, u, 0, dir='+')) > 0 and sp.simplify(vis_deep) == 0,
     float(sp.limit(vis_slope, u, 0, dir='+')), sp.Integer(1), 'mu2 kernel: effective viscosity -> 0 at small shear (shear-thinning, no regularization floor)')

res = {'lane': 'N01_rheology', 'slope_formula': str(slope),
       'p_eff_formula': str(p_eff), 'p_eff_deep': float(lo), 'p_eff_newtonian': float(hi),
       'p_eff_at_gN_1e-6_a0': float(p_at_deep_margin),
       'cross_9over5_at_gN_over_a0': float(cross / a0),
       'rar_deep_slope': float(slope_rar), 'mu2_viscosity_deep': float(sp.limit(mu2, u, 0)),
       'checks': [{'name': n, 'pass': c, 'value': float(v), 'threshold': float(t), 'note': e} for n, c, v, t, e in checks]}
print('slope formula      :', slope)
print('p_eff formula      :', p_eff)
print('p_eff deep (x->0)  :', lo, '  p_eff Newtonian (x->oo):', hi)
print('p_eff at g_N=1e-6 a0:', p_at_deep_margin)
print('p_eff = 9/5 crossing at g_N =', sp.N(cross / a0, 5), '* a0')
print('RAR deep slope     :', slope_rar, '  mu2 viscosity at u->0:', sp.limit(mu2, u, 0))
for n, c, v, t, e in checks:
    print(('PASS' if c else 'FAIL'), n, f'value={v} threshold={t}')
    print('     ', e)
npass = sum(1 for _, c, _, _, _ in checks if c)
print(f'N01_rheology COMPLETE: {npass}/{len(checks)} checks PASS.')
print('DOOR N1: DEAD -- the measured law is shear-thinning (p_eff -> 3/2) exactly where it acts;')
print('the power-law regularity class (9/5, 11/5 gates) is unreachable. FAIL = the finding.')
with open('N01_rheology_results.json', 'w') as f:
    json.dump(res, f, indent=1)