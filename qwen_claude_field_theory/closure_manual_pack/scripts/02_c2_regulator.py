#!/usr/bin/env python3
import sympy as sp

z, e = sp.symbols('z e', positive=True)
Fp = 4 * (1 - (1 + sp.sqrt(z)/2) * sp.exp(-sp.sqrt(z)/2))
Fm = sp.Rational(1,2) * z * sp.exp(-sp.sqrt(-z)/3)
# Hermite interpolation degree <= 5 matching value, first, second derivative at +/-e.
coeffs = sp.symbols('c0:6')
P = sum(coeffs[i]*z**i for i in range(6))
eqs = []
for x, branch in [(e, Fp), (-e, Fm)]:
    for n in range(3):
        eqs.append(sp.Eq(sp.diff(P,z,n).subs(z,x), sp.diff(branch,z,n).subs(z,x)))
sol = sp.solve(eqs, coeffs, dict=True, simplify=False)
if len(sol) != 1:
    raise SystemExit(f'Expected unique Hermite solution, got {len(sol)}')
Psol = sp.factor(P.subs(sol[0]))
print('P(z)=')
print(Psol)
for x, branch, side in [(e,Fp,'+'),(-e,Fm,'-')]:
    for n in range(3):
        d = sp.simplify(sp.diff(Psol,z,n).subs(z,x) - sp.diff(branch,z,n).subs(z,x))
        print(f'match {side}, n={n}:', d)
        if d != 0:
            raise SystemExit('FAIL: C2 matching')
print('PASS')
