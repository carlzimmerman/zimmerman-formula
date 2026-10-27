#!/usr/bin/env python3
"""Diagnostic for a naive local auxiliary representation.

This is NOT a proof of a ghost in the original retarded nonlocal theory.
It only shows that the naive single-copy localization has an indefinite
velocity Hessian in flat space when the eta Box(Phi) term is integrated by parts.
"""
import sympy as sp
vphi, veta, x = sp.symbols('vphi veta x', real=True)
# L_kin = - partial_mu eta partial^mu phi, signature (-,+,+,+)
# Time derivative contribution is + eta_dot phi_dot.
Lkin = veta * vphi
H = sp.hessian(Lkin, (veta, vphi))
print('H =')
print(H)
print('det(H) =', sp.det(H))
print('eigenvals =', H.eigenvals())
if sp.det(H) >= 0:
    raise SystemExit('UNEXPECTED: Hessian is not indefinite')
print('RESULT: indefinite naive auxiliary Hessian; NOT a physical-ghost theorem')
