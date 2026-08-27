import sympy as sp

y, Z = sp.symbols('y Z', positive=True)
f = 4*(1-(1+sp.sqrt(Z)/2)*sp.exp(-sp.sqrt(Z)/2))
fp = sp.simplify(sp.diff(f, Z))
expected_fp = sp.Rational(1,2)*sp.exp(-sp.sqrt(Z)/2)
mu = sp.simplify(1-2*fp.subs(Z, 4*y**2))
expected_mu = 1-sp.exp(-y)
F = y**2/2 + (1+y)*sp.exp(-y)-1
mu_a = 1-sp.exp(-y)
print('[PASS]' if sp.simplify(fp-expected_fp)==0 else '[FAIL]', 'f_+(Z) derivative')
print('[PASS]' if sp.simplify(mu-expected_mu)==0 else '[FAIL]', 'exact exponential mu(y)')
print('[PASS]' if sp.simplify(sp.diff(F,y)-y*mu_a)==0 else '[FAIL]', 'AQUAL primitive')
print('f_+(Z) =', f)
print('mu(y) =', mu)
print('f_+(Z) series =', sp.series(f, Z, 0, 4))
