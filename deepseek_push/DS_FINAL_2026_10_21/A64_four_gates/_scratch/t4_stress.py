import sympy as sp
r, K, a0, gam, chi, eps = sp.symbols('r K a0 gamma chi epsilon', positive=True)
n1 = sp.Function('n1')(r); h1 = sp.Function('h1')(r); p1 = sp.Function('p1')(r)
P = sp.Function('P')(r)
# background fields with eps counting
N = 1 + eps*n1
f = 1 + eps*h1
Pb = eps*p1
# chi-deformed metric in the radial frame
sqh = f**sp.Rational(3, 2)*(1 + 2*chi/3)**sp.Rational(1, 2)*(1 - chi/3)
Pr = f**-1*(1 + 2*chi/3)**-1*Pb          # P^r
u = K*sp.sqrt(f**-1*(1 + 2*chi/3)**-1)*Pb   # K|P|
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
d = (1/sqh)*sp.diff(sqh*Pr, r)
ops = {
    'W':      sqh*N*(-W),
    'clock':  sqh*Pr*sp.diff(N, r),
    'd2':     sqh*N*(-gam*d**2/2),
}
for name, Lop in ops.items():
    Pi = sp.simplify(-3*sp.diff(Lop, chi).subs(chi, 0))
    s = sp.series(sp.expand(Pi), eps, 0, 3).removeO()
    c0 = sp.simplify(s.coeff(eps, 0)); c1 = sp.simplify(s.coeff(eps, 1)); c2 = sp.simplify(s.coeff(eps, 2))
    print(f"{name:6s} Pi^(0) = {c0}\n       Pi^(1) = {c1}\n       Pi^(2) = {sp.simplify(c2)}")
    print(f"       -> O(eps) part zero: {c0 == 0 and c1 == 0}\n")
# W: exact Pi = u W'
u0 = K*Pb
Wp = a0*u0/(K*(a0 - u0))
print("W exact: Pi - u W' =", sp.simplify(ops and (-3*sp.diff(ops['W'], chi).subs(chi,0)) - u0*Wp))
print("clock exact at f=1: Pi - 2 P N' =", sp.simplify((-3*sp.diff(ops['clock'], chi).subs(chi,0)).subs(eps,0) - 2*Pb*sp.diff(N, r).subs(eps,0)))