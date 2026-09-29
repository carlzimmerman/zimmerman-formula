#!/usr/bin/env python3
"""a04_equivalence_and_dimension_audit.py -- adversarial audit of p04 (ten formulations) and p05 (five d-dependences).

 E1  independent derivations of the dimension-dependent ingredients used by p04-B / p05 (NOT taken from the record):
       - flat FRW in D = d+1 dimensions: Einstein tensor G_tt = d(d-1)/2 H^2  (sympy, d = 2..6)  => H^2 = 16 pi G rho/(d(d-1))
       - Schwarzschild-Tangherlini f = 1 - (r_s/r)^(D-3): surface gravity f'(r_s)/2 = (D-3)/(2 r_s) = (d-2)/(2 r_s)
 E2  each of p04's ten rows is a linear equation  C = (monomial in 1/kappa); mutate the constant of EACH row and confirm the solver moves kappa off 1/2
     (p04 has only ONE mutation control, on row 1).
 E3  which rows are conditional on a premise that is itself the factor 2:
       row 5  (p'(0) = 1)  -- equivalent to kappa = 1/2 ONLY under the convention mu = 1-(1-p)^N with N = 2 fixed (p05 A1: kappa = 1/N).  Test: N free.
       row 8  (mode count n = Z) -- with an INTEGER count n, kappa = sqrt(8 pi/3)/n is never 1/2; n = 6 gives 0.4824 (Z = 6, the 'Verlinde' coefficient).
       row 10 (Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2)) -- with the committed SPARC a0 and Omega_Lambda = 0.685 this is an EMPIRICAL statement that is off by ~32% (not an identity).
 E4  p04-B: 'Z^2 = 8 Vol(B^d) only at d = 3' -- tested for one d-generalisation only; try others (2^d Vol(B^d), Vol(S^d) forms).  And it presupposes kappa = 1/2 for every d
     (p05's option 1) while p05's other four options give Z_d different from 8 sqrt(pi/(d(d-1))).
 E5  p05 formulas: re-derive the five kappa(d) forms from E1 and check they equal 1/2 at d = 3.
Exit 0 = the audit's checks held.
"""
import math, sys
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- E1a  FRW Einstein tensor in D = d+1
def gtt_over_H2(d):
    t = sp.symbols('t', real=True); H = sp.symbols('H', positive=True)
    xs = [t] + list(sp.symbols('x1:%d' % (d + 1), real=True))
    a = sp.exp(H * t)
    g = sp.diag(*([-1] + [a**2] * d))
    n = d + 1
    ginv = g.inv()
    Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], xs[k]) + sp.diff(g[l, k], xs[j]) - sp.diff(g[j, k], xs[l])) for l in range(n)) / 2 for k in range(n)] for j in range(n)] for i in range(n)]
    def Riem(i, j, k, l):
        return sp.diff(Gam[i][j][l], xs[k]) - sp.diff(Gam[i][j][k], xs[l]) + sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(n))
    Ric = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(Riem(i, j, i, l) for i in range(n))))
    Rs = sp.simplify(sum(ginv[j, l] * Ric[j, l] for j in range(n) for l in range(n)))
    Gtt = sp.simplify(Ric[0, 0] - Rs * g[0, 0] / 2)
    return sp.simplify(Gtt / H**2)
for d in range(2, 6):
    val = gtt_over_H2(d)
    chk("E1a flat FRW, D = %d+1: G_tt = %s H^2 = d(d-1)/2 H^2  (=> H^2 = 16 pi G rho/(d(d-1)))" % (d, val), sp.simplify(val - sp.Rational(d * (d - 1), 2)) == 0)

# ---------------------------------------------------------------- E1b  Tangherlini surface gravity
r, rs = sp.symbols('r r_s', positive=True)
for D in range(4, 8):
    f = 1 - (rs / r)**(D - 3)
    kap = sp.simplify(sp.diff(f, r).subs(r, rs) / 2)
    chk("E1b Schwarzschild-Tangherlini D = %d: kappa = f'(r_s)/2 = %s = (D-3)/(2 r_s) = (d-2)/(2 r_s)" % (D, kap), sp.simplify(kap - sp.Rational(D - 3, 2) / rs) == 0)

# ---------------------------------------------------------------- E2  mutation of each of the ten rows
k, G, rho, c = sp.symbols('kappa G rho c', positive=True)
a0 = k * c * sp.sqrt(G * rho)
Lam = 8 * sp.pi * G * rho / c**2
half = sp.Rational(1, 2)
def root(eq):
    s = [x for x in sp.solve(eq, k) if x.is_positive]
    return s[0] if len(s) == 1 else None
rsw = c**2 / (2 * a0)
t_L = 1 / sp.sqrt(G * rho)
rows = {
    "1 Lambda = 32 pi a0^2/c^4": (sp.Eq(Lam, 32 * sp.pi * a0**2 / c**4), sp.Eq(Lam, 30 * sp.pi * a0**2 / c**4)),
    "2 A Lambda = 32 pi^2": (sp.Eq(4 * sp.pi * rsw**2 * Lam, 32 * sp.pi**2), sp.Eq(4 * sp.pi * rsw**2 * Lam, 30 * sp.pi**2)),
    "3 1/r_s^2 = G rho/c^2": (sp.Eq(1 / rsw**2, G * rho / c**2), sp.Eq(1 / rsw**2, 2 * G * rho / c**2)),
    "4 c^2/a0 = 2 R*": (sp.Eq(c**2 / a0, 2 * c / sp.sqrt(G * rho)), sp.Eq(c**2 / a0, 3 * c / sp.sqrt(G * rho))),
    "5 2 p'(0) = 1/kappa, p'(0) = 1": (sp.Eq(1 / (2 * k), 1), sp.Eq(1 / (2 * k), sp.Rational(3, 2))),
    "6 M1 = 2c/(3 a0) = (4/3) t_L": (sp.Eq(2 * c / (3 * a0), sp.Rational(4, 3) * t_L), sp.Eq(2 * c / (3 * a0), sp.Rational(5, 3) * t_L)),
    "9 Z = c H_L/a0 = 2 sqrt(8pi/3)": (sp.Eq(c * sp.sqrt(8 * sp.pi * G * rho / 3) / a0, 2 * sp.sqrt(8 * sp.pi / 3)), sp.Eq(c * sp.sqrt(8 * sp.pi * G * rho / 3) / a0, 3 * sp.sqrt(8 * sp.pi / 3))),
}
H0, OL = sp.symbols('H0 Omega_L', positive=True)
a0lock = k * c * sp.sqrt(G * OL * 3 * H0**2 / (8 * sp.pi * G))
rows["10 Omega_L = 32 pi a0^2/(3 H0^2 c^2)"] = (sp.Eq(OL, 32 * sp.pi * a0lock**2 / (3 * H0**2 * c**2)), sp.Eq(OL, 28 * sp.pi * a0lock**2 / (3 * H0**2 * c**2)))
allgood = True
for nm, (good, bad) in rows.items():
    rg, rb = root(good), root(bad)
    good_ok = rg is not None and sp.simplify(rg - half) == 0
    bad_ok = rb is None or sp.simplify(rb - half) != 0
    allgood = allgood and good_ok and bad_ok
    print("   row %-38s kappa = %s ; mutated -> kappa = %s" % (nm, rg, sp.simplify(rb) if rb is not None else None))
chk("E2 each of rows 1-6, 9, 10 gives kappa = 1/2 and its mutation moves kappa (p04 controlled only row 1); rows 7, 8 are solved for Z_q and n, not kappa", allgood)
beta, Zq, b = sp.symbols('beta Z_q b', positive=True)
kap2 = 2 * beta**2 / (Zq + 2 * b * beta**2)
chk("E2b row 7: kappa = 1/2 <=> Z_q/beta^2 = 8 - 2b -- ONE relation among THREE free numbers (Z_q, beta, b); kappa is not fixed by it (source FOURFORM report says the action does not select b or Z/beta^2)",
    sp.simplify(sp.solve(sp.Eq(kap2, sp.Rational(1, 4)), Zq)[0] - (8 * beta**2 - 2 * b * beta**2)) == 0 and len(kap2.free_symbols) == 3)

# ---------------------------------------------------------------- E3 conditional premises
p, N = sp.symbols('p N', positive=True)
mu = 1 - (1 - p)**N
mup0 = sp.diff(mu, p).subs(p, 0)
kap_from_p = sp.simplify(1 / mup0)
chk("E3a row 5: 'p'(0) = 1' (the response of p in mu = 1-(1-p)^N) gives kappa = 1/N; it equals 1/2 only BECAUSE N = 2 is the convention (the 2 is put in by the exponent) -- the row is equivalent to kappa = 1/2 only given N = 2",
    sp.simplify(kap_from_p - 1 / N) == 0)
Zf = math.sqrt(8 * math.pi / 3)
ks = {n: Zf / n for n in (5, 6, 7)}
print("   integer mode counts: " + ", ".join("n=%d -> kappa=%.4f (Z=%d)" % (n, kv, n) for n, kv in ks.items()))
chk("E3b row 8: with an INTEGER mode count n, kappa = sqrt(8 pi/3)/n is never 1/2 (n=6 -> 0.4824); row 8 is equivalent to kappa=1/2 only for a non-integer 'count' n = 5.789",
    all(abs(kv - 0.5) > 0.01 for kv in ks.values()) and abs(ks[6] - 0.4824) < 5e-4)
cc = 2.99792458e8; Mpc = 3.0856775814913673e22
H0v = 67.4e3 / Mpc; a0_hat = 1.0766e-10
OL_pred = 32 * math.pi * a0_hat**2 / (3 * H0v**2 * cc**2)
print("   row 10 evaluated on data: Omega_Lambda(pred from SPARC a0, H0=67.4) = %.3f vs 0.685 observed (%+.0f%%)" % (OL_pred, 100 * (OL_pred / 0.685 - 1)))
chk("E3c row 10 is an algebraic identity in kappa but, with the committed a0 and H0 = 67.4, predicts Omega_Lambda = %.2f (observed 0.685): as a cosmological statement it is NOT satisfied (the SPARC a0 exceeds the framework's c H_Lambda/Z by 15 percent = the rho_Lambda-footing tension, 2.4 sigma)" % OL_pred, OL_pred > 0.85)

# ---------------------------------------------------------------- E4 p04-B alternatives
def zd2(d): return 64 * math.pi / (d * (d - 1))
def volB(d): return math.pi**(d / 2) / math.gamma(d / 2 + 1)
def volS(d): return 2 * math.pi**((d + 1) / 2) / math.gamma((d + 1) / 2)     # unit S^d
forms = {
    "8 Vol(B^d)": lambda d: 8 * volB(d),
    "2^d Vol(B^d) (= vol of ball of radius 2)": lambda d: 2**d * volB(d),
    "(8/3) Vol(S^(d-1)) with S^(d-1) = boundary of B^d": lambda d: sp.Rational(8, 3) * (2 * math.pi**(d / 2) / math.gamma(d / 2)),
}
d_hits = {}
for nm, fn in forms.items():
    hits = [d for d in range(2, 9) if abs(float(fn(d)) - zd2(d)) < 1e-9]
    d_hits[nm] = hits
    print("   %-52s equals Z_d^2 = 64 pi/(d(d-1)) at d = %s" % (nm, hits))
chk("E4a for the generalisations tried the match is at d = 3 only (p04-B B1 confirmed for these; but it is a statement about the CHOSEN generalisations -- 32 pi/3 = 8 Vol(B^3) = (8/3) Vol(S^2) admits infinitely many d-continuations)",
    all(h == [3] for h in d_hits.values()))

# ---------------------------------------------------------------- E5 p05 forms
d = sp.symbols('d', positive=True)
Zfd = 4 * sp.sqrt(sp.pi / (d * (d - 1)))            # from E1a with kappa = 1
chk("E5a Z_f,d = H/(c sqrt(G rho)) = sqrt(16 pi/(d(d-1))) = 4 sqrt(pi/(d(d-1))) (from the FRW Einstein tensor of E1a) at d = 3 is sqrt(8pi/3)", sp.simplify(Zfd.subs(d, 3) - sp.sqrt(8 * sp.pi / 3)) == 0)
kap5 = sp.sqrt(sp.Rational(3, 2) / (d * (d - 1)))
kap3 = (d - 2) / 2
kap4 = sp.Rational(2, 3) * d / (d + 1)
kap2_ = 1 / (d - 1)
chk("E5b the five forms are 1/2, 1/(d-1), (d-2)/2, (2/3) d/(d+1), sqrt(3/(2 d (d-1))); each is exactly 1/2 at d = 3 and (3) is the Tangherlini value of E1b with r_s = R*",
    all(sp.simplify(v.subs(d, 3) - sp.Rational(1, 2)) == 0 for v in (kap2_, kap3, kap4, kap5)))
print("   NOTE E5c: option (1) 'two static channels: kappa = 1/2 for every d' is a constant, not a d-dependence: it is the statement kappa = 1/2 itself; the 'five origins' contain one restatement and four rational functions")
chk("E5d p04-B's Z_d = 8 sqrt(pi/(d(d-1))) (= 2 Z_f,d) equals only option (1) of p05: under options (2)-(5) the d-dimensional Z differs, so 'the 3 is dim SO(3)' (README 6) is conditional on d-independent kappa = 1/2",
    sp.simplify(Zfd / kap5 - 2 * sp.sqrt(8 * sp.pi / 3)) == 0 and sp.simplify(Zfd.subs(d, 4) / kap2_.subs(d, 4) - 2 * Zfd.subs(d, 4)) != 0)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
