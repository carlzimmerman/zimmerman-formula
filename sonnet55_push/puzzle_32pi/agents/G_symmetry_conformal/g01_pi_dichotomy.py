"""g01: what can a symmetry-only route deliver?  The pi-counting dichotomy, stated and checked.

c = G = 1.  Lambda = 3 H^2 (de Sitter), rho_Lambda = Lambda/(8 pi).
Framework coefficient:  kappa := a0 / sqrt(G rho_Lambda) = (a0/H) * sqrt(8 pi / 3).     (kappa = 1/2 fitted)

Claim (Lindemann): pi is transcendental.  Representation theory of SO(4,1) / SO(4,2) / SO(4) (Casimirs, dimensions,
degeneracies, Delta(3-Delta) = m^2/H^2, Higuchi bound...) produces RATIONAL or ALGEBRAIC numbers.  Hence
   (i)  if a0/H is algebraic (a symmetry-derived number), then kappa^2 = (8 pi/3)(a0/H)^2 is transcendental: kappa = 1/2 (any
        rational, any algebraic) is IMPOSSIBLE exactly;
   (ii) if kappa is algebraic (kappa = 1/2), then (a0/H)^2 = 3 kappa^2/(8 pi) is transcendental: a0/H cannot be a
        symmetry (algebraic) number.
   So "a0/H fixed by dS representation data" and "kappa = 1/2 exactly" are mutually exclusive.  The exact framework
   statement lives at the level  G rho_Lambda = 4 a0^2  (algebraic coefficient 4) and needs the Einstein 8 pi G to convert to H.

Checks: (A) exact symbolic reduction; (B) integer-relation searches (evidence; the theorem is Lindemann 1882) with control;
(C) mutation: with an algebraic 'Einstein coefficient' the dichotomy disappears (so the test is sensitive to the pi);
(D) numbers: what an algebraic a0/H near the data looks like and how far it is from 1/Z (data cannot resolve).
"""
import sympy as sp, mpmath as mp, sys
mp.mp.dps = 80
ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

Lam, H, a0, kap, x = sp.symbols('Lambda H a0 kappa x', positive=True)
rhoL = Lam / (8 * sp.pi)
# (A) exact reduction
kappa_expr = a0 / sp.sqrt(rhoL)                              # G = 1
kappa_H = sp.simplify(kappa_expr.subs(Lam, 3 * H**2))
chk("A1 kappa = (a0/H) sqrt(8 pi/3)", sp.simplify(kappa_H - (a0 / H) * sp.sqrt(8 * sp.pi / 3)) == 0)
sol = sp.solve(sp.Eq(kappa_H, sp.Rational(1, 2)), a0)
chk("A2 kappa = 1/2  <=>  a0 = H sqrt(3/(32 pi))   (Z = sqrt(32 pi/3))", sp.simplify(sol[0] - H * sp.sqrt(3 / (32 * sp.pi))) == 0)
chk("A3 (a0/H)^2 = 3/(32 pi) has a factor of pi in the denominator: sympy says it is not algebraic",
    (sp.Rational(3, 32) / sp.pi).is_algebraic is False)
chk("A4 control: sympy says sqrt(3/2)*7/5 IS algebraic", (sp.sqrt(sp.Rational(3, 2)) * sp.Rational(7, 5)).is_algebraic is True)

# (B) integer-relation searches on kappa^2 for a menu of algebraic a0/H values (a menu of SYMMETRY-type numbers, written
#     before running; NOT tuned to the target).  x^2 in {rational}; kappa^2 = (8 pi/3) x^2.
menu_x2 = [sp.Rational(p, q) for (p, q) in [(1, 1), (2, 1), (9, 4), (1, 2), (3, 2), (1, 4), (4, 1), (1, 36), (1, 33), (5, 4)]]
def has_poly(val, maxdeg=8, maxc=10**5):
    for d in range(1, maxdeg + 1):
        r = mp.findpoly(val, d, maxcoeff=maxc, maxsteps=200000)
        if r:
            return (d, r)
    return None
bad = 0
for x2 in menu_x2:
    k2 = (8 * mp.pi / 3) * mp.mpf(x2.p) / mp.mpf(x2.q)
    r = has_poly(k2)
    if r is not None:
        bad += 1
        print("   unexpected algebraic relation for x^2 =", x2, r)
chk("B1 for %d rational (a0/H)^2 values, kappa^2 = (8pi/3)(a0/H)^2 has no polynomial relation, degree<=8, coeff<=1e5" % len(menu_x2), bad == 0)
# also the algebraic-irrational x^2 (square-root numbers such as those of m^2/H^2 = Delta(3-Delta) with Delta = 3/2 - sqrt(9/4-n)):
menu_x2b = [mp.sqrt(2), 3 - mp.sqrt(3), (1 + mp.sqrt(5)) / 2, mp.mpf(2) ** (mp.mpf(1) / 3)]
badb = 0
for xv in menu_x2b:
    if has_poly((8 * mp.pi / 3) * xv, maxdeg=8, maxc=10**4) is not None:
        badb += 1
chk("B2 same for %d algebraic-irrational (a0/H)^2 values (degree<=8, coeff<=1e4)" % len(menu_x2b), badb == 0)
# (ii) kappa=1/2 -> (a0/H)^2 = 3/(32 pi)
chk("B3 (a0/H)^2 = 3/(32 pi) has no polynomial relation (deg<=8, coeff<=1e5)", has_poly(mp.mpf(3) / (32 * mp.pi)) is None)
chk("B4 control: the search finds sqrt(3/8)+1/7 (degree 4 polynomial) so it would see an algebraic number",
    has_poly(mp.sqrt(mp.mpf(3) / 8) + mp.mpf(1) / 7, maxdeg=8, maxc=10**5) is not None)

# (C) mutation: pretend Einstein's coefficient were algebraic (8 pi -> 8): then an algebraic a0/H DOES give an algebraic kappa
k2_mut = (mp.mpf(8) / 3) * mp.mpf(2)
chk("C1 mutation (8 pi -> 8): kappa^2 = (8/3) x^2 becomes algebraic, so the search is sensitive to the pi", has_poly(k2_mut) is not None)

# (D) numbers: the framework Z and the nearest 'natural' algebraic Z's.  (a0/H = 1/Z)
Z = mp.sqrt(32 * mp.pi / 3)
print("   Z = sqrt(32 pi/3) = %s ; Z^2 = %s ; a0/H = %s" % (mp.nstr(Z, 8), mp.nstr(Z**2, 8), mp.nstr(1 / Z, 8)))
kap_from_Z = lambda Zalg: mp.sqrt(8 * mp.pi / 3) / Zalg
rows = [("Z=6 (algebraic, integer)", mp.mpf(6)), ("Z=2 pi (thermal 2 pi; transcendental)", 2 * mp.pi),
        ("Z=1 (the natural SO(4,1) scale a0=H)", mp.mpf(1)), ("Z=sqrt(2)*4", mp.sqrt(2) * 4), ("Z=sqrt(33)", mp.sqrt(33))]
for nm, zv in rows:
    print("   %-42s Z=%8.5f  kappa=%8.5f  (kappa/0.5 - 1) = %+6.2f%%" % (nm, zv, kap_from_Z(zv), 100 * (kap_from_Z(zv) / mp.mpf(1) * 2 - 1)))
chk("D1 Z = 6 (algebraic) sits within 4% of the framework Z: an algebraic symmetry number is not excluded by any measurement that resolves a0 only to ~10%",
    abs(6 / Z - 1) < 0.04)
chk("D2 but kappa(Z=6) = sqrt(8pi/3)/6 = 0.4824 is TRANSCENDENTAL (Lindemann), hence exactly != 1/2",
    has_poly(kap_from_Z(mp.mpf(6)) ** 2) is None and abs(kap_from_Z(mp.mpf(6)) - mp.mpf(1) / 2) > mp.mpf('0.01'))
chk("D3 the natural group-theory scale a0 = H (Z = 1) is off by a factor Z = 5.79 from the framework a0", abs(Z - 5.7888) < 1e-3)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
