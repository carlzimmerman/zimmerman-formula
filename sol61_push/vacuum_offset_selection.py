"""Exact algebra checks for the conditional vacuum-offset obstruction.

Run: python3 sol61_push/vacuum_offset_selection.py
This verifies identities, not a sourced galaxy solution or physical UV validity.
"""
import json
import sympy as s

q, A, B, ell, Z, G, Kc, V0 = s.symbols('q A B ell Z G Kc V0', positive=True)
S = 2 + 3*ell*q
U0 = A/q**2 + B*q**2
W = S*(U0 + V0)
Wpp = 12*A/q**4 + 4*B + 6*ell*A/q**3 + 18*ell*B*q
offset = s.solve(s.diff(W, q), V0)[0]
C = 2304*s.pi**3*G**3*Kc**2*q**2*(U0 + V0)/S
Cs = 1536*s.pi**3*G**3*Kc**2/ell*(A/q - B*q**3)
checks = {
    'vacuum_curvature': s.diff(W, q, 2)-Wpp,
    'stationary_energy': ((U0+V0)/S + s.diff(U0,q)/(3*ell)).subs(V0,offset),
    'coefficient': C.subs(V0,offset)-Cs,
    'implicit_root_derivative': s.diff(offset,q)+Wpp/(3*ell),
    'coefficient_offset_derivative': s.diff(Cs,q)*(-3*ell/Wpp)-4608*s.pi**3*G**3*Kc**2*(A/q**2+3*B*q**2)/Wpp,
    'static_mass': s.diff(U0,q,2)/Z + 2*s.diff(U0,q)/(Z*q) - (2*A/q**4+6*B)/Z,
    'coupling_rescaling': Cs.subs(Kc,2*Kc)-4*Cs,
}
results = {name: s.simplify(value)==0 for name,value in checks.items()}
assert all(results.values()), results
print(json.dumps({'checks': results, 'passed': len(results), 'scope': 'Exact symbolic identities; positivity and endpoint arguments are in VACUUM_OFFSET_SELECTION_RESULTS.md.'}, indent=2))
