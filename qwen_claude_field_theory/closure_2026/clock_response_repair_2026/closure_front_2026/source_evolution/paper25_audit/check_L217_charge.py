#!/usr/bin/env python3
"""Bounded FLRW chi-charge audit; no parameter or full-background scan."""
import json
import sympy as S

a, q, qdot, H, gamma, w, U, d, mrel, lam, rhob = S.symbols(
    'a q qdot H gamma w U d mrel lambda rho_b', positive=True)
X = S.symbols('X', real=True)
P = S.Function('P')
checks = {}


def eq(name, lhs, rhs=0):
    checks[name] = S.simplify(lhs-rhs) == 0
    assert checks[name], (name, S.simplify(lhs-rhs))


# Homogeneous constant-gamma action, lapse fixed only after IBP.
# Original a^3 gamma X Box chi = -gamma a^3 q^2(qdot+3Hq).
L3_direct = -gamma*a**3*q**2*(qdot+3*H*q)
boundary = -gamma*a**3*q**3/3
dt_boundary = S.diff(boundary, a)*a*H+S.diff(boundary, q)*qdot
L3_ibp = -2*gamma*a**3*H*q**3
eq('cubic_integration_by_parts', L3_direct-L3_ibp, dt_boundary)
PX = S.diff(P(X), X).subs(X, q**2)
Lhom = a**3*P(q**2)+L3_ibp
charge = S.simplify(S.diff(Lhom, q))
eq('full_chi_charge', charge, a**3*(2*PX*q-6*gamma*H*q**2))
eq('cubic_current_nonzero_difference', charge-2*a**3*PX*q, -6*gamma*a**3*H*q**2)
J = S.Function('j')(a)
eq('FLRW_conserved_charge_divergence', S.diff(a**3*J, a)*a*H/a**3,
   a*H*S.diff(J, a)+3*H*J)

# L217's assigned scaling family, with mrel held independent of a.
d_family, q_family = a**(-3*(1-w)), a**(-3*w)
partial_charge_family = S.simplify(a**3*d_family*q_family/mrel)
eq('assigned_scaling_product_constant', partial_charge_family, 1/mrel)
eq('local_partial_current_dilutes', d_family*q_family/mrel, a**(-3)/mrel)
Qconst = S.symbols('Qconst', positive=True)
eq('correct_clock_identity_has_comoving_volume',
   (w*Qconst/(a**3*d*q)).subs(Qconst, a**3*d*q/mrel), w/mrel)

# Counterexample to "chi shift symmetry alone conserves inverse margin":
# the same logarithmic kinetic form, fixed U,d, gamma=0, no matter source.
x = S.symbols('x', positive=True)  # x=q/sqrt(U/(2d)), 0<x<1.
ell = x/(1-x*x)  # local shift-current density up to a constant factor.
dx_dN = S.simplify(-3/(S.diff(S.log(ell), x)))
eq('log_scalar_charge_dilution_solution', dx_dN, -3*x*(1-x*x)/(1+x*x))
eq('inverse_margin_logarithmic_drift',
   S.diff(S.log(1/(1-x*x)), x)*dx_dN, -6*x*x/(1+x*x))
eq('near_pole_inverse_margin_drift_is_minus3',
   S.limit(-6*x*x/(1+x*x), x, 1, dir='-'), -3)

# A constant source in COMOVING charge is compatible with dilution of j.
t, J0, A, B = S.symbols('t J_initial A B', positive=True)
acomoving = t**S.Rational(2, 3)
Qsource = J0+lam*B*t
jlocal = S.simplify(Qsource/acomoving**3)
Ht = S.diff(acomoving, t)/acomoving
eq('linearly_sourced_charge_still_has_Hubble_dilution',
   S.diff(jlocal, t)+3*Ht*jlocal, lam*B/acomoving**3)
eq('source_changes_global_charge', S.diff(Qsource, t), lam*B)

print(json.dumps({
    'scope': 'Constant-gamma homogeneous scalar Noether charge and source-free logarithmic-kinetic counterexample; not an on-shell PAPER25/PAPER24 background',
    'checks': checks,
    'full_chi_charge': str(charge),
    'physical_current_convention': 'j=2 P_X q-6 gamma H q^2; dot j+3Hj=lambda rho_b for +lambda chi rho_b source',
    'assigned_L217_partial_charge': str(partial_charge_family),
    'assigned_L217_local_partial_current': str(S.simplify(d_family*q_family/mrel)),
    'correct_s0_identity_in_partial_current_truncation': 's0-1=w Qchi/(a^3 d q), Qchi=a^3 d q/mrel',
    'log_kinetic_counterexample': {'dx_dN': str(dx_dN), 'dlog_inverse_margin_dN': '-6*x**2/(1+x**2)', 'domain': '0<x<1; fixed U,d>0; gamma=0; absent direct matter source'},
    'non_claims': ['No full nonlinear clock or gravity solution', 'No claim that explicit tau functions break chi shifts', 'No protection of tau clock rate from chi charge alone', 'No new bound on w or a0', 'No quantum naturalness or EFT cutoff test']
}, indent=2))
