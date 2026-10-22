import sympy as sp
from gr_tools import ricci_scalar

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
beta = sp.symbols('beta', real=True)
Lam = sp.symbols('Lambda', real=True)
H = sp.diff(a, t)/a
cs = [x, y, z]

f = eps*sig*sp.cos(kk*z)
m = sp.diag(1+f, 1-f, 1)
minv = m.inv()
R3m, _, _ = ricci_scalar(m, cs)
R3m_ser = sp.expand(sp.series(R3m, eps, 0, 3).removeO())
R3 = R3m_ser/a**2                       # R3 of h_ij = a^2 m_ij

h = a**2*m
hdot = sp.diff(h, t)
Kij = sp.Matrix(3, 3, lambda i, j: sp.diff(h[i, j], t)/2)   # N=1, zero shift
theta = sum(minv[i, j]*Kij[i, j] for i in range(3) for j in range(3))/a**2
Ksq = 0
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                Ksq += minv[i, k]*minv[j, l]*Kij[i, j]*Kij[k, l]/a**4

sqrth = a**3*sp.sqrt(sp.det(m))
L = (R3 + Ksq - (1+beta)*theta**2 - 2*Lam)*sqrth/(4*sp.Symbol('K', positive=True))

Lser = sp.expand(sp.series(sp.simplify(L), eps, 0, 3).removeO())
L2 = sp.expand(Lser.coeff(eps, 2))
print("L2 (raw) =", sp.simplify(L2))

# average over one period in z: <cos^2>=<sin^2>=1/2, <cos sin>=0
def avg(expr):
    e = sp.expand(expr.rewrite(sp.cos).expand(trig=True))
    e = sp.expand_trig(sp.expand(e))
    out = sp.S.Zero
    for term in sp.Add.make_args(e):
        c = sp.simplify(term.rewrite(sp.cos).subs(sp.cos(kk*z), 0).subs(sp.sin(kk*z), 0))
        # replace cos^2->1/2 etc: substitute cos(kz)**2 -> 1/2, sin(kz)**2 -> 1/2, cos*sin->0
        t2 = term
        t2 = t2.subs(sp.cos(kk*z)**2, sp.Rational(1, 2)).subs(sp.sin(kk*z)**2, sp.Rational(1, 2))
        t2 = t2.subs(sp.cos(kk*z), 0).subs(sp.sin(kk*z), 0)
        out += t2
    return sp.simplify(out)

L2avg = avg(L2)
print("\n<L2> =", sp.simplify(sp.expand(L2avg)))
K4 = sp.Symbol('K', positive=True)
Acoef = sp.simplify(sp.diff(L2avg, sp.diff(sig, t))**0)  # placeholder
sd = sp.Symbol('sd')  # sigma-dot symbol
L2s = sp.expand(L2avg.subs(sp.diff(sig, t), sd))
A = sp.simplify(L2s.coeff(sd, 2) if L2s.coeff(sd,2)!=0 else sp.diff(L2s, sd, 2)/2)
print("coefficient of sigma_dot^2:", sp.simplify(sp.diff(L2s, sd, 2)/2))
print("rest (sigma only):", sp.simplify(L2s.subs(sd, 0)))
