import sympy as sp
r, K, a0, gam, eps = sp.symbols('r K a0 gamma epsilon', positive=True)
N = sp.Function('N')(r); f = sp.Function('f')(r); P = sp.Function('P')(r)
R3 = -2*sp.diff(f, r, 2)/f**2 + sp.Rational(3, 2)*sp.diff(f, r)**2/f**3 - 4*sp.diff(f, r)/(r*f**2)
u = K*P
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
d = f**sp.Rational(-3, 2)*(1/r**2)*sp.diff(r**2*sp.sqrt(f)*P, r)
rho = sp.Function('rho')(r)
L = 4*sp.pi*r**2*(N*f**sp.Rational(3, 2)*(R3/(4*K) - W - gam*d**2/2) + sp.sqrt(f)*P*sp.diff(N, r)
                  - rho*N*f**sp.Rational(3, 2))
Ef = sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r) + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)

n1 = sp.Function('n1')(r); h1 = sp.Function('h1')(r); p1 = sp.Function('p1')(r)
repl = {N: 1 + eps*n1, f: 1 + eps*h1, P: eps*p1, rho: 0}
E2 = Ef
for fn, val in repl.items():
    for kk in (3, 2, 1):
        E2 = E2.subs(sp.Derivative(fn, (r, kk)), sp.diff(val, r, kk))
    E2 = E2.subs(fn, val)
ser = sp.series(sp.expand(E2), eps, 0, 3).removeO()
E1 = sp.simplify(ser.coeff(eps, 1))
E2c = sp.simplify(sp.expand(ser.coeff(eps, 2)))
print("E1 (O(eps)) =", sp.simplify(E1/(sp.pi*r/K)))
s = sp.Function('s')(r)
lap_s = sp.diff(s, r, 2) + 2*sp.diff(s, r)/r
print("\n--- E1 in terms of s = n1 + h1/2  (h1+2n1 = 2s):")
print("   E1/(2 pi r/K) =", sp.simplify(E1/(2*sp.pi*r/K)))
# now E2c: try to write as  -(2 pi r /K)*( r^2 s2' )' ... check candidates
s1 = n1 + h1/2
print("\n--- E2c structure: substitute a test source and fit")
# Candidate A:  E2c = -(2 pi r/K)*d/dr(r^2 d(2nd-order s)/dr) + c*source(Pi)
# Let's isolate the "Pi" piece by setting n1=h1=0 (pure P, no metric backreaction)
print(" E2c at n1=h1=0:", sp.simplify(E2c.subs({n1: 0, h1: 0})))
# and the "metric-only" piece with p1=0
print("\n E2c at p1=0:", sp.simplify(E2c.subs(p1, 0)))
