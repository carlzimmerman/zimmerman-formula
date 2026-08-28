import sympy as sp

y, Z = sp.symbols('y Z', positive=True)
mu = 1 - sp.exp(-y)
f = 4*(1-(1+sp.sqrt(Z)/2)*sp.exp(-sp.sqrt(Z)/2))
fp = sp.simplify(sp.diff(f,Z))
assert sp.simplify(fp - sp.Rational(1,2)*sp.exp(-sp.sqrt(Z)/2)) == 0
assert sp.simplify((1-2*fp.subs(Z,4*y**2)) - mu) == 0
F = y**2/sp.Integer(2) + (1+y)*sp.exp(-y) - 1
assert sp.simplify(sp.diff(F,y) - y*mu) == 0
lam_t = sp.simplify(mu + y*sp.diff(mu,y))
assert sp.limit(lam_t,y,sp.oo)==1
print('[PASS] f_+(Z) exact derivative')
print('[PASS] mu(y)=1-exp(-y) exactly')
print('[PASS] AQUAL primitive F\'(y)=y mu(y)')
print('[PASS] longitudinal constitutive eigenvalue =', lam_t)
print('STATUS: explicit full candidate; stability/transition/DOF remain open')
