import sympy as sp
r, K, a0, gam, eps = sp.symbols('r K a0 gamma eps', positive=True)
N = sp.Function('N')(r); f = sp.Function('f')(r); P = sp.Function('P')(r)
R3 = -2*sp.diff(f, r, 2)/f**2 + sp.Rational(3, 2)*sp.diff(f, r)**2/f**3 - 4*sp.diff(f, r)/(r*f**2)
u = K*P
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
d = f**sp.Rational(-3, 2)*(1/r**2)*sp.diff(r**2*sp.sqrt(f)*P, r)
rho = sp.Function('rho')(r)
L = 4*sp.pi*r**2*(N*f**sp.Rational(3, 2)*(R3/(4*K) - W - gam*d**2/2) + sp.sqrt(f)*P*sp.diff(N, r) - rho*N*f**sp.Rational(3, 2))
Ef = sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r) + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)
EN = sp.diff(L, N) - sp.diff(sp.diff(L, sp.diff(N, r)), r)

n1 = sp.Function('n1')(r); h1 = sp.Function('h1')(r); p1 = sp.Function('p1')(r)
def expand1(expr, fns):
    """substitute N=1+eps n1 etc and return the O(eps) coefficient"""
    e = expr
    repl = {N: 1 + eps*n1, f: 1 + eps*h1, P: eps*p1, rho: 0}
    for fn, val in repl.items():
        for k in (3, 2, 1):
            e = e.subs(sp.Derivative(fn, (r, k)), sp.diff(val, r, k))
        e = e.subs(fn, val)
    e = sp.series(sp.expand(e), eps, 0, 2).removeO()
    return sp.simplify(e.coeff(eps, 1))

Ef1 = expand1(Ef, None)
EN1 = expand1(EN, None)
print("Ef at O(eps) for h1=-2n1, p1=0 (should vanish):")
print("  ", sp.simplify(Ef1.subs({h1: -2*n1, p1: 0})))
print("\nEf at O(eps) general (p1=0):")
print("  ", sp.simplify(Ef1.subs(p1, 0)))
print("\nEN at O(eps) (p1=0) :", sp.simplify(EN1.subs(p1, 0)))