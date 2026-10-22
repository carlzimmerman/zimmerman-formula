import sympy as sp
from gr_tools import ricci_scalar

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
Lam = sp.symbols('Lambda', real=True)
cs = [x, y, z]
E = sp.Symbol('E', positive=True)

def avg(expr):
    e = expr.subs(sp.cos(kk*z), (E + 1/E)/2).subs(sp.sin(kk*z), (E - 1/E)/(2*sp.I))
    return sp.simplify(sp.expand(sp.expand(sp.simplify(e))).coeff(E, 0))

def o2(expr):
    s = sp.expand(sp.series(sp.simplify(expr), eps, 0, 3).removeO())
    return sp.simplify(s.coeff(eps, 2))

f = eps*sig*sp.cos(kk*z)
m = sp.diag(1+f, 1-f, 1)
minv = m.inv()
R3m, _, _ = ricci_scalar(m, cs)
h = a**2*m
Kij = sp.Matrix(3, 3, lambda i, j: sp.diff(h[i, j], t)/2)
theta = sum(minv[i, j]*Kij[i, j] for i in range(3) for j in range(3))/a**2
Ksq = sum(minv[i, k]*minv[j, l]*Kij[i, j]*Kij[k, l]
          for i in range(3) for j in range(3) for k in range(3) for l in range(3))/a**4
sqrth = a**3*sp.sqrt(sp.det(m))
H = sp.diff(a, t)/a

pieces = {
    'R3':   o2(R3m/a**2),
    'Ksq':  o2(Ksq - 9*H**2),
    'theta2': o2(theta**2 - 9*H**2),
    'sqrth': o2(sqrth),
}
for nm, ex in pieces.items():
    print(nm, " O(eps^2) avg =", avg(ex))
print("\n<sqrth> O2 =", avg(pieces['sqrth']), " (expect -a^3 sigma^2/4)")
print("<theta^2-9H^2> =", avg(pieces['theta2']))
print("<Ksq-9H^2> =", avg(pieces['Ksq']))
print("<R3> =", avg(pieces['R3']), "(expect -k^2 sigma^2/4)")

# total, assembled by hand from pieces:  (1/4K)[ R3 + (Ksq-9H2) - (1+b)(theta2-9H2) - 2L ] * sqrth
# expand product to O(eps^2): note sqrth = a^3 + d2, and background bracket = -6H^2-2L
d2 = avg(pieces['sqrth'])
bg = -6*H**2 - 2*Lam
tot = (avg(pieces['R3']) + avg(pieces['Ksq']) - (1+sp.Symbol('beta'))*avg(pieces['theta2'])) * a**3 + bg*d2
print("\nassembled L2*a^3-free form:", sp.simplify(sp.expand(tot)))
print("  /(4K) with sd:")
sd = sp.Symbol('sd')
print("  ", sp.simplify(sp.expand(tot.subs(sp.diff(sig,t), sd))))
