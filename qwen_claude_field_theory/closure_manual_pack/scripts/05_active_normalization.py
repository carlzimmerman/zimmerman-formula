#!/usr/bin/env python3
"""Record the normalization decision from the weak-field constitutive matching.

The actual full metric variation remains a separate task. This script only
checks the coefficient logic used to distinguish the rejected and repaired
normalizations under the assumed reduced relation M=-F(Z).
"""
import sympy as sp
alpha = sp.symbols('alpha')
Fp = sp.symbols('Fp')
# If the reduced weak-field constitutive coefficient is mu = 1 - 2*alpha*Fp,
# target mu = 1 - 2*Fp requires alpha=1.
solution = sp.solve(sp.Eq(2*alpha*Fp, 2*Fp), alpha)
print('Required normalization multiplier alpha =', solution[0])
print('Rejected original alpha=2 would give mu=1-4Fp.')
print('Repaired alpha=1 gives target mu=1-2Fp.')
print('IMPORTANT: this is a reduced matching check, not the full covariant variation.')
