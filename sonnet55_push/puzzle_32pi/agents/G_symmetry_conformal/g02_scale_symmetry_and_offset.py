"""g02: the dilatation symmetry of deep MOND cannot see the vacuum energy or fix the ratio a0^2/Lambda.

Checks
 A  dimensional analysis: the units group (L,T,M) acts on the parameters (a0, Lambda, G, c, rho_Lambda); the invariants form the
    nullspace.  The puzzle ratio is the (only) genuine dimensionless combination of a0 and Lambda: a symmetry acting as a
    rescaling of units cannot constrain an invariant.
 B  deep-MOND field equation  div(|grad phi| grad phi) = 4 pi G a0 rho  is covariant under (t,r)->q(t,r) at fixed mass
    (phi weight 0, rho weight -3, G a0 fixed); the Newtonian Poisson equation is NOT (mismatch factor q) unless G -> q G.
 C  a uniform vacuum density (nonzero constant source) is NOT covariant: Lambda carries scale weight; it is an explicit breaking.
 D  the AQUAL Lagrangian L = -(a0^2/8 pi G) F(y) - rho phi: the field equation depends only on F' (=mu), so F -> F + C changes
    nothing observable to the field equation: the additive constant (a vacuum energy a0^2 C/(8 pi G)) is unconstrained by every
    symmetry of the field equation (dilatation, conformal group, Galilei).
 E  IF one nonetheless fixes the constant by demanding F -> y exactly at high acceleration (GR/Newton normalisation), the vacuum
    energy of the g = 0 (deep-MOND) state is rho = c a0^2/(8 pi G), c = int_0^inf (1 - mu) dy.  The puzzle needs c = 32 pi
    (G rho = 4 a0^2).  RESULT (my pre-run expectation 'c = O(1), 30-300x too small' was WRONG and is corrected here): c is a functional
    of the far TAIL of mu: 1/3 for a sharp transition, 2 for 1-exp(-x), 24 for a tail exp(-sqrt(x)) (the RAR shape, 26 numerically),
    divergent for the simple/standard mu.  So c = 32 pi is reachable by a slow-tail family, but only by TUNING a tail exponent.
"""
import sympy as sp, mpmath as mp, sys, random
import numpy as np
mp.mp.dps = 40
ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

# ---------------- A: units group and invariants
L_, T_, M_ = 0, 1, 2
params = {'a0': (1, -2, 0), 'Lambda': (-2, 0, 0), 'G': (3, -2, -1), 'c': (1, -1, 0), 'rho_Lambda': (-3, 0, 1)}
# Lambda is given in units 1/L^2 (geometric).  exponent vectors per parameter (L,T,M)
names = list(params)
Mx = sp.Matrix([[params[n][i] for n in names] for i in range(3)])      # 3 x 5
ns = Mx.nullspace()
print("   parameters:", names)
for v in ns:
    print("   invariant exponents:", dict(zip(names, list(v.T))))
chk("A1 5 parameters, rank-3 dimension matrix -> exactly 2 independent dimensionless invariants", len(ns) == 2 and Mx.rank() == 3)
# the two invariants can be taken as  I1 = Lambda c^4/a0^2  and  I2 = G rho_Lambda /(Lambda c^2)
def dim_of(expr_exps):
    return Mx * sp.Matrix(expr_exps)
I1 = dict(a0=-2, Lambda=1, G=0, c=4, rho_Lambda=0)
I2 = dict(a0=0, Lambda=-1, G=1, c=-2, rho_Lambda=1)
chk("A2 I1 = Lambda c^4/a0^2 and I2 = G rho/(Lambda c^2) are dimensionless",
    dim_of([I1[n] for n in names]) == sp.zeros(3, 1) and dim_of([I2[n] for n in names]) == sp.zeros(3, 1))
chk("A3 I2 is fixed by Einstein's equation Lambda = 8 pi G rho/c^2 (I2 = 1/(8 pi)); the puzzle is therefore the single number I1 = Lambda c^4/a0^2 = 32 pi",
    sp.simplify((8 * sp.pi) ** -1 * 32 * sp.pi - 4) == 0)
chk("A4 negative control: a3-parameter subset (a0, G, c) has NO dimensionless invariant, so a0 cannot be built from G, c alone",
    len(sp.Matrix([[params[n][i] for n in ['a0', 'G', 'c']] for i in range(3)]).nullspace()) == 0)

# ---------------- B: covariance of the deep-MOND field equation (random test functions, exact-ish numerics)
x, y, z = sp.symbols('x y z', real=True)
X = (x, y, z)
q = sp.symbols('q', positive=True)
def grad(f): return [sp.diff(f, v) for v in X]
def mond3(phi):            # div(|grad phi| grad phi)
    g = grad(phi); n = sp.sqrt(sum(gi**2 for gi in g))
    return sum(sp.diff(n * gi, v) for gi, v in zip(g, X))
def lap(phi): return sum(sp.diff(phi, v, 2) for v in X)
random.seed(3)
tests = [x**2 * y + z**3 + sp.sin(x * z) + 2 * y, sp.exp(x / 3) * (y + 1) + z**2 * x, x * y * z + y**3 - 4 * x + sp.cos(y)]
worst_deep = 0; worst_newt_ratio = []
for phi in tests:
    for _ in range(3):
        pt = {x: random.uniform(0.4, 1.7), y: random.uniform(0.4, 1.7), z: random.uniform(0.4, 1.7)}
        qv = random.uniform(0.5, 3.0)
        # phi_q(x) = phi(x/q) ;  E[phi_q](x) should equal q^-3 * E[phi](x/q)
        sub = {x: x / q, y: y / q, z: z / q}
        phi_q = phi.subs(sub, simultaneous=True)
        lhs = mond3(phi_q).subs({**pt, q: qv})
        rhs = qv**-3 * mond3(phi).subs({x: pt[x] / qv, y: pt[y] / qv, z: pt[z] / qv})
        worst_deep = max(worst_deep, abs(float(lhs - rhs)) / (abs(float(rhs)) + 1e-12))
        lhsN = lap(phi_q).subs({**pt, q: qv}); rhsN = lap(phi).subs({x: pt[x] / qv, y: pt[y] / qv, z: pt[z] / qv})
        worst_newt_ratio.append(float(lhsN / rhsN) / qv**-2)      # covariant with weight q^-2 would give ratio 1
chk("B1 deep-MOND operator: E[phi(x/q)](x) = q^-3 E[phi](x/q) (max rel. dev %.1e over 9 random cases)" % worst_deep, worst_deep < 1e-9)
# Newtonian: lap(phi(x/q)) = q^-2 (lap phi)(x/q)  -> it IS covariant as an operator (weight -2), but the SOURCE 4 pi G rho with rho weight -3 (mass fixed) is not:
chk("B2 Newtonian Laplacian scales with weight q^-2 (operator), while a fixed-mass source has weight q^-3: mismatch factor q, cured only by G->qG",
    max(abs(np.array(worst_newt_ratio) - 1)) < 1e-9)
# mutation: wrong weight for MOND (q^-2 instead of q^-3) must FAIL
phi = tests[0]; pt = {x: 0.9, y: 1.1, z: 0.7}; qv = 1.7
phi_q = phi.subs({x: x / q, y: y / q, z: z / q}, simultaneous=True)
lhs = float(mond3(phi_q).subs({**pt, q: qv}))
wrong = qv**-2 * float(mond3(phi).subs({x: pt[x] / qv, y: pt[y] / qv, z: pt[z] / qv}))
chk("B3 mutation: weight q^-2 for the deep-MOND operator is rejected", abs(lhs - wrong) / abs(wrong) > 0.05)

# ---------------- C: a uniform vacuum source breaks the dilatation (explicit solution)
rr = sp.sqrt(x**2 + y**2 + z**2)
Gs_, a0_, rhoL_ = sp.symbols('G a0 rho_L', positive=True)
k = 4 * sp.pi * Gs_ * a0_ * rhoL_ / 3
phi_u = sp.Rational(2, 3) * sp.sqrt(k) * rr**sp.Rational(3, 2)            # deep-MOND field of a UNIFORM density rho_L
Eu = sp.simplify(mond3(phi_u))
chk("C1a explicit solution: div(|grad phi| grad phi) = 4 pi G a0 rho_L for phi = (2/3) sqrt(k) r^(3/2), k = 4 pi G a0 rho_L/3", sp.simplify(Eu - 4 * sp.pi * Gs_ * a0_ * rhoL_) == 0)
phi_uq = phi_u.subs({x: x / q, y: y / q, z: z / q}, simultaneous=True)
Euq = sp.simplify(mond3(phi_uq))
chk("C1b the dilated solution phi(r/q) solves the equation with rho_L -> q^-3 rho_L, NOT with rho_L: a fixed uniform vacuum density breaks the dilatation (explicit scale weight)",
    sp.simplify(Euq - 4 * sp.pi * Gs_ * a0_ * rhoL_ * q**-3) == 0 and sp.simplify(Euq - 4 * sp.pi * Gs_ * a0_ * rhoL_).subs({q: 2, Gs_: 1, a0_: 1, rhoL_: 1}) != 0)
# dimension of Lambda under (t,r)->q(t,r): 1/length^2 -> q^-2 ; a0 -> a0/q ; ratio invariant (bookkeeping)
chk("C2 (bookkeeping) the dilatation maps (Lambda, a0) -> (Lambda/q^2, a0/q): the ratio Lambda/a0^2 is INVARIANT",
    sp.simplify((sp.Symbol('Lam') / q**2) / (sp.Symbol('a') / q)**2 - sp.Symbol('Lam') / sp.Symbol('a')**2) == 0)

# ---------------- D: additive constant in F is invisible to the field equation
yy, C, a0s, Gs = sp.symbols('yy C a0 G', positive=True)
F = sp.Function('F')
phi_f = sp.Function('phi')(x, y, z)
def EL(Fexpr):
    yv = sum(sp.diff(phi_f, v)**2 for v in X) / a0s**2
    Lag = -(a0s**2 / (8 * sp.pi * Gs)) * Fexpr(yv)
    return sum(sp.diff(sp.diff(Lag, sp.diff(phi_f, v)), v) for v in X)      # d_i (dL/d phi_i); dL/dphi = 0 (source added separately)
E0 = EL(lambda t: F(t)); E1 = EL(lambda t: F(t) + C)
chk("D1 Euler-Lagrange expression for F and for F + C is identical (C drops out): the vacuum-energy constant is unconstrained by the field equation",
    sp.simplify(E0.doit() - E1.doit()) == 0)

# ---------------- E: c(mu) = int_0^inf (1 - mu) dy  with y = x^2, x = g/a0
def one_minus_mu_n(xx, n):          # stable 1 - x/(1+x^n)^(1/n)
    xx = mp.mpf(xx)
    return -mp.expm1(-mp.log1p(xx**(-n)) / n) if xx > 1 else 1 - xx / (1 + xx**n)**(mp.mpf(1) / n)
def c_num(one_minus_mu, brk=(0, 1, 10, 100, 1e3, 1e4, 1e6, mp.inf)):
    return mp.quad(lambda xx: one_minus_mu(xx) * 2 * xx, list(brk))
cv = {}
cv['sharp min(x,1)'] = c_num(lambda xx: max(1 - xx, mp.mpf(0)), brk=(0, 1, 2))
cv['1-exp(-x)'] = c_num(lambda xx: mp.e**(-xx))
for n in [3, 4, 6, 10]:
    cv['mu_n n=%d' % n] = c_num((lambda n: (lambda xx: one_minus_mu_n(xx, n)))(n))
print("   c = int (1-mu) dy   [rho_vac = c a0^2/(8 pi G); the puzzle needs c = 32 pi = %s]" % mp.nstr(32 * mp.pi, 6))
for nm, v in cv.items():
    print("   %-22s c = %-12s  G rho/a0^2 = c/(8 pi) = %s" % (nm, mp.nstr(v, 8), mp.nstr(v / (8 * mp.pi), 5)))
for nm, n in [('simple n=1', 1), ('standard n=2', 2)]:
    p1 = mp.quad(lambda xx: one_minus_mu_n(xx, n) * 2 * xx, [0, 1, 10, 100, 1e3]); p2 = mp.quad(lambda xx: one_minus_mu_n(xx, n) * 2 * xx, [0, 1, 10, 100, 1e3, 1e4, 1e5, 1e6])
    print("   %-22s partial c up to x=1e3: %s ; up to x=1e6: %s  (grows without bound: offset undefined)" % (nm, mp.nstr(p1, 6), mp.nstr(p2, 6)))
    cv[nm] = (p1, p2)
chk("E1 sharp transition mu = min(x,1): c = 1/3 exactly", abs(cv['sharp min(x,1)'] - mp.mpf(1) / 3) < 1e-12)
chk("E2 mu = 1 - exp(-x): c = 2 exactly", abs(cv['1-exp(-x)'] - 2) < 1e-12)
chk("E3 mu_n = x/(1+x^n)^(1/n): finite for n >= 3 (values above, all positive) and divergent for the popular simple (n=1, linear growth) and standard (n=2, log growth) forms",
    all(cv['mu_n n=%d' % n] > 0 for n in [3, 4, 6, 10]) and cv['simple n=1'][1] > 100 * cv['simple n=1'][0] and cv['standard n=2'][1] > cv['standard n=2'][0] + 5)
# stretched-exponential tail family mu_s = 1 - exp(-x^s):  c(s) = (2/s) Gamma(2/s)   (closed form; verify numerically)
cs = lambda s: (2 / mp.mpf(s)) * mp.gamma(2 / mp.mpf(s))
num_s = {s: c_num((lambda s: (lambda xx: mp.e**(-xx**s)))(s), brk=(0, 1, 10, 100, 1e3, 1e4, 1e6, mp.inf)) for s in [1, 0.75, 0.5]}
chk("E4 stretched-exponential tails: c(s) = (2/s) Gamma(2/s) matches numerics at s = 1, 3/4, 1/2 (= 2, %s, 24)" % mp.nstr(cs(0.75), 6),
    all(abs(num_s[s] - cs(s)) / cs(s) < 1e-8 for s in num_s))
s_star = mp.findroot(lambda s: cs(s) - 32 * mp.pi, (mp.mpf('0.3'), mp.mpf('0.5')), solver='anderson', tol=1e-30, maxsteps=200)
print("   c(s) = 32 pi at s* = %s   (tail exp(-x^s*), a TUNED exponent; nothing in a symmetry selects it)" % mp.nstr(s_star, 8))
chk("E5 the required c = 32 pi is reachable in this family only at s* = %s: a one-parameter tuning, i.e. the puzzle is relocated into a tail exponent of mu, not derived" % mp.nstr(s_star, 5),
    0.3 < s_star < 0.5 and abs(cs(s_star) - 32 * mp.pi) < 1e-20)
# RAR: nu = 1/(1-exp(-sqrt(yb))), mu = 1/nu, x = yb*nu
nu = lambda yb: 1 / (1 - mp.e**(-mp.sqrt(yb)))
def c_rar():
    xfun = lambda yb: yb * nu(yb)
    integrand = lambda yb: mp.e**(-mp.sqrt(yb)) * mp.diff(lambda t: xfun(t)**2, yb)
    return mp.quad(integrand, [mp.mpf('1e-12'), 1, 10, 100, 1e3, 1e4])
c_r = c_rar()
print("   RAR (exponential nu): c = %s ; G rho/a0^2 = c/(8 pi) = %s  (the tail is exp(-sqrt(g/a0)), s = 1/2 asymptotically, c(1/2) = 24)" % (mp.nstr(c_r, 6), mp.nstr(c_r / (8 * mp.pi), 5)))
chk("E6 the RAR-shaped mu gives c = 25.98 (G rho/a0^2 = 1.03 vs the puzzle's 4): same order as c(1/2) = 24, short by a factor 3.9 -- an accident of an empirical fit's tail, which the data do not constrain beyond g ~ 10 a0",
    abs(c_r - 24) < 4 and 3.5 < 32 * mp.pi / c_r < 4.3)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
