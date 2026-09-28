import sympy as sp

# --- MU2: exact closed forms ---
x = sp.symbols('x', positive=True)
mu2 = 1 - (1 + x/2)**-2
y = x*mu2
lhs = sp.simplify((x - y)/y)
rhs = sp.simplify(4/(x*(x+4)))
print("closed_form_residual (expect 0):", sp.simplify(lhs - rhs))
print("nu_minus_1_closed_form:", sp.simplify(lhs))
print("v = 1/y in terms of u = 1/x:", sp.simplify(1/y.subs(x, 1/sp.symbols('u'))))

# --- series reversion via Newton iteration on formal power series ---
u = sp.symbols('u'); v = sp.symbols('v')
f = sp.series(1/(y.subs(x, 1/u)), u, 0, 14).removeO().expand()   # v(u)
g = v
for _ in range(8):
    fg = sp.series(f.subs(u, g), v, 0, 14).removeO().expand()
    g = sp.series(g + (v - fg), v, 0, 14).removeO().expand()
u_of_v = g
print("u(v) = 1/x as series in v=1/y:", u_of_v)
nu1 = sp.series((4*u_of_v**2/(1 + 4*u_of_v)), v, 0, 13).removeO().expand()
print("nu_MU2 - 1 = series in v = 1/y:", nu1)

# --- Q binomial ---
w = sp.symbols('w')
print("Q: (1+w)^(1/2) - 1 =", sp.series((1+w)**sp.Rational(1,2) - 1, w, 0, 7))
# exact rationalized forms
print("Q: y*sqrt(1+1/y) - y =", sp.simplify(sp.symbols('y')*(sp.sqrt(1+1/sp.symbols('y')) - 1)))
