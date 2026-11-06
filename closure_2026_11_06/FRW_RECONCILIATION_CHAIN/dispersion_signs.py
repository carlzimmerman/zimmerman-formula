"""Frozen FRW dispersion with general mixing factor f>=0 (f=(1-z)^2 corrected; f=1 is AC2).
w^2/H^2 = E x^2 (1+l x^2) / (E(1+l x^2) + f x^2), l=ell^2>=0, E>0, x>0."""
import sympy as sp
E, l, x = sp.symbols('E l x', positive=True); f = sp.Symbol('f', nonnegative=True)
w2 = E*x**2*(1+l*x**2)/(E*(1+l*x**2)+f*x**2)
cp2 = sp.simplify(w2/x**2)
print('1-c_phase^2 =', sp.factor(sp.simplify(1-cp2)))           # >=0 termwise
w = sp.sqrt(w2); cg = sp.diff(w, x); cph = w/x
# c_group*c_phase = (1/2) d(w^2)/dx / x
prod = sp.factor(sp.simplify(sp.diff(w2, x)/(2*x)))
print('c_g*c_ph =', prod)
diff = sp.factor(sp.simplify(cp2 - prod))                         # c_ph^2 - c_g c_ph >= 0  <=> c_g <= c_ph
print('c_ph^2 - c_g*c_ph =', diff)
num_prod = sp.expand(sp.numer(prod)); print('numerator of c_g*c_ph expanded:', num_prod)
print('all coefficients of numerator nonneg:', all(c >= 0 for c in sp.Poly(num_prod, x).coeffs()))
