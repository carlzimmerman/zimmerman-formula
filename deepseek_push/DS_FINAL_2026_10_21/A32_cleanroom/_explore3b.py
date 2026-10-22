import sympy as sp
from gr_tools import ricci_scalar, christoffel

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
cs = [x, y, z]

f = eps*sig*sp.cos(kk*z)
m = sp.diag(1+f, 1-f, 1)          # TT: trace free, d_i m_iz = 0
R3m, Ricm, Gm = ricci_scalar(m, cs)
print("R3(m) exact =", sp.simplify(R3m))
ser = sp.series(R3m, eps, 0, 3).removeO()
ser = sp.expand(ser)
c1 = sp.simplify(ser.coeff(eps, 1))
c2 = sp.simplify(ser.coeff(eps, 2))
print("\nO(eps^1):", c1, "   (must vanish: linearised Ricci of TT mode)")
print("O(eps^2):", sp.simplify(c2))
print("O(eps^2) - (1/4)(d f)^2 :", sp.simplify(c2 - sp.Rational(1,4)*(sp.diff(f,z)**2 + sp.diff(f,z)**2)))
print("O(eps^2) - (1/2)(d f)^2 :", sp.simplify(c2 - sp.Rational(1,2)*(sp.diff(f,z)**2)))
print("O(eps^2) - (d f)^2      :", sp.simplify(c2 - (sp.diff(f,z)**2)))
# also check with exp(ikz) plane wave: is residual a total derivative?
print("\n(z-derivative test) is c2 - 1/2 f'^2 a total derivative? c2-1/2f'^2 =",
      sp.simplify(c2 - sp.Rational(1,2)*sp.diff(f,z)**2))
