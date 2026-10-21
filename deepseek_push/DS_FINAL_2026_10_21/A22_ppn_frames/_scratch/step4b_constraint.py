"""Step 4b: quadratic Lagrangian -> exact linearised constraint equations."""
import sympy as sp

r = sp.symbols('r', positive=True)
K, gam = sp.symbols('K gamma', positive=True)
Ph = sp.Function('Phi')(r)
Ps = sp.Function('Psi')(r)
p = sp.Function('p')(r)
e = sp.symbols('e')


def R3(fe):
    Lg = sp.log(fe)
    return -(1/fe)*(2*sp.diff(Lg, r, 2) + 4*sp.diff(Lg, r)/r + sp.Rational(1, 2)*sp.diff(Lg, r)**2)


N = 1 + e*Ph
f = 1 - 2*e*Ps
pe = e*p
sqh = f**sp.Rational(3, 2)
q = sp.sqrt(f)*pe
DP = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)
W2 = K*pe**2/(2*f)
clock = pe*sp.diff(N, r)/(f*N)
L = r**2*sqh*N*(R3(f)/(4*K) + clock - W2 - (gam/2)*DP**2)

Lser = sp.series(L, e, 0, 3).removeO()
L2 = sp.expand(Lser.coeff(e, 2))
print("L quadratic part extracted, ops =", sp.count_ops(L2))


def euler(L, v):
    ee = sp.diff(L, v)
    for d in L.atoms(sp.Derivative):
        if d.expr == v:
            n = d.variable_count[0][1]
            ee = ee + (-1)**n*sp.diff(sp.diff(L, d), r, n)
    return sp.expand(ee)


for v, nm in ((Ph, 'LAPSE (Phi)'), (Ps, 'TRACE (Psi)'), (p, 'P')):
    E = sp.simplify(euler(L2, v)/(r**2))
    print('===', nm, '===')
    print(E)
    print()
