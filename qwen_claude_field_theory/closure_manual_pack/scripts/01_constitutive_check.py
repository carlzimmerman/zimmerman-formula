#!/usr/bin/env python3
import sympy as sp

Z, eps, y = sp.symbols('Z eps y', positive=True)
Fplus = 4 * (1 - (1 + sp.sqrt(Z)/2) * sp.exp(-sp.sqrt(Z)/2))
Fp = sp.simplify(sp.diff(Fplus, Z))
Fpp = sp.simplify(sp.diff(Fp, Z))
Fppp = sp.simplify(sp.diff(Fpp, Z))
print('F\' =', Fp)
print('F\'\' =', Fpp)
print('F\'\'\' =', Fppp)
check = sp.simplify(Fp.subs(Z, 4*y**2) - sp.exp(-y)/2)
print('F\'(4 y^2) - exp(-y)/2 =', check)
mu = sp.simplify(1 - 2*Fp.subs(Z, 4*y**2))
print('mu(y) =', mu)
print('mu'(0) series =', sp.series(mu, y, 0, 4))
print('mu(infty) formal limit =', sp.limit(mu, y, sp.oo))
if check != 0 or sp.simplify(mu - (1-sp.exp(-y))) != 0:
    raise SystemExit('FAIL: constitutive identity')
print('PASS')
