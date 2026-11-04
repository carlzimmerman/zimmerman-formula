"""CT2 small check (reading, not a frozen gate): can a local divergence stiffness F(D), D = div P,
in C6's static aether equation give a screening length that scales as the source's MOND radius?
C6 balance inside the screened core (p << a0): grad Phi_N + grad F'(D) = 0  =>  F'(D) = G M / r.
Screen ends where |p| reaches a0 (the unscreened tail scale). Power law F = lam D^n / n."""
import sympy as sp
n, lam, GM, r, a0, L = sp.symbols('n lam GM r a0 L', positive=True)
D = (GM/(lam*r))**(1/(n-1))                    # from lam D^(n-1) = GM/r
p = sp.simplify(sp.integrate(D.subs(r, sp.Symbol('s'))*sp.Symbol('s')**2, (sp.Symbol('s'), 0, r))/r**2)
print("p(r) =", p)
# mass exponent of the crossover radius where p(L) = a0
expo = sp.simplify(sp.diff(sp.log(sp.solve(sp.Eq(p.subs(r, L), a0), L)[0]), GM)*GM)
print("d ln L / d ln M =", sp.simplify(expo))
print("n giving exponent 1/2:", sp.solve(sp.Eq(expo, sp.Rational(1, 2)), n))
for nv in [sp.Rational(1,2), sp.Rational(3,2), 2, 3]:
    print(f" n={nv}: exponent {sp.simplify(expo.subs(n,nv))}, F''/lam sign at D>0: {sp.sign((nv-1))}")
# log limit: F = lam ln D -> F' = lam/D = GM/r -> D = lam r/GM ; F'' = -lam/D^2 < 0
Dl = lam*r/GM
pl = sp.simplify(sp.integrate((lam*sp.Symbol('s')/GM)*sp.Symbol('s')**2, (sp.Symbol('s'), 0, r))/r**2)
Ll = sp.solve(sp.Eq(pl.subs(r, L), a0), L)[0]
print("log stiffness: p =", pl, "; L =", Ll, "; with lam = k a0^2: L =", sp.simplify(Ll.subs(lam, sp.Symbol('k')*a0**2)))
print("log stiffness F'' =", sp.diff(lam*sp.log(sp.Symbol('D')), sp.Symbol('D'), 2), "(< 0: concave, longitudinal gradient energy negative)")
# MUTATE control: n = 2 must give C6's hedgehog |p| = const = GM/(3 lam)... check r-independence
print("n=2 control, dp/dr =", sp.simplify(sp.diff(p.subs(n, 2), r)))
