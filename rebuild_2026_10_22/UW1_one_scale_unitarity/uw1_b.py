# UW1 test B: the law's F on the timelike branch. s = sqrt(|Y|), Y = -s^2.
import sympy as sp
s, F0 = sp.symbols("s F0", positive=True)
ana = (-s**2 - 2*sp.I*s + 2*sp.log(1 + sp.I*s) + F0)
print("analytic branch Im F(s=1):", sp.N(sp.im(ana.subs({s: 1, F0: 0}))))
F = -s**2 - 2*s + 2*sp.log(1 + s) + F0          # real, keeps the Y term
Fp = sp.simplify(sp.diff(F, s) / (-2*s))        # dF/dY
print("real branch dF/dY:", Fp, " at s->0:", sp.limit(Fp, s, 0), " zeros s>0:", sp.solve(Fp, s))
rho_plus_P = sp.simplify(s**2 * Fp)             # units M^4
print("rho+P:", rho_plus_P, " positive for s>0:", bool(rho_plus_P.subs(s, 1) > 0))
P = -F/2
rho = rho_plus_P - P
print("rho - F0/2 at small s:", sp.series(sp.simplify(rho - F0/2), s, 0, 3))
print("P + F0/2 at small s:", sp.series(sp.simplify(P + F0/2), s, 0, 3))
print("d rho/d F0:", sp.diff(rho, F0))
