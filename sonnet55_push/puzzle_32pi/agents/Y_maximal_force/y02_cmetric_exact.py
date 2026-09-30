"""Lane Y, script 2: the exact dS C-metric (Dias-Lemos form): field equations, acceleration a_4 = A, conical structure,
the string family R1, P_none (C2), P_sat (C3).  sympy for the field equations, mpmath (50 digits) for the conical numbers."""
import json
import os
import itertools
import sympy as sp
import mpmath as mp
from common import Ledger, HERE
import cmetric as cm

L_ = Ledger("y02_cmetric_exact")
mp.mp.dps = 50

# ------------------------------------------------------------------------ C0 field equations (symbolic)
t, y, x, z = sp.symbols("t y x z", real=True)
m, A, ell = sp.symbols("m A ell", positive=True)
X = [t, y, x, z]


def ricci_diag(gdiag):
    n = 4
    g = sp.diag(*gdiag)
    gi = sp.diag(*[1 / e for e in gdiag])
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c_ in range(n):
                Gam[a][b][c_] = sum(gi[a, d] * (sp.diff(g[d, c_], X[b]) + sp.diff(g[d, b], X[c_]) - sp.diff(g[b, c_], X[d])) for d in range(n)) / 2
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c_ in range(b, n):
            expr = 0
            for a in range(n):
                expr += sp.diff(Gam[a][b][c_], X[a]) - sp.diff(Gam[a][b][a], X[c_])
                for d in range(n):
                    expr += Gam[a][a][d] * Gam[d][b][c_] - Gam[a][c_][d] * Gam[d][b][a]
            Ric[b, c_] = expr
            Ric[c_, b] = expr
    return g, Ric


def metric(Ffun, Gfun):
    pref = 1 / (A**2 * (x + y) ** 2)
    return [-pref * Ffun, pref / Ffun, pref / Gfun, pref * Gfun]


Fdl = -1 / (ell**2 * A**2) - 1 + y**2 - 2 * m * A * y**3
Gdl = 1 - x**2 - 2 * m * A * x**3
Lam = 3 / ell**2


def einstein_residual(Ffun, Gfun):
    g, Ric = ricci_diag(metric(Ffun, Gfun))
    res = (Ric - Lam * g).applyfunc(lambda e: sp.simplify(sp.together(e)))
    return res


print("\n== C0: Einstein equation R_mu nu = Lambda g_mu nu, Lambda = 3/ell^2, for the Dias-Lemos dS C-metric ==")
res = einstein_residual(Fdl, Gdl)
L_.check("R_mu nu - Lambda g_mu nu = 0 identically in (m, A, ell, x, y)", res == sp.zeros(4, 4))
resF = einstein_residual(-1 / (ell**2 * A**2) * (-1) - 1 + y**2 - 2 * m * A * y**3, Gdl)   # + 1/(ell^2 A^2): wrong sign (AdS-like)
L_.must_fail("wrong sign of the 1/(ell^2 A^2) term in F (that is Lambda -> -Lambda) fails for Lambda = +3/ell^2", resF == sp.zeros(4, 4))
resG = einstein_residual(Fdl, 1 - x**2 - m * A * x**3)
L_.must_fail("wrong cubic coefficient in G fails", resG == sp.zeros(4, 4))
# is m = 0 exactly de Sitter?  Riemann^2 = 24/ell^4 (checked with the Einstein residual plus constant Kretschmann)
def kretschmann_m0():
    Fm0 = Fdl.subs(m, 0); Gm0 = Gdl.subs(m, 0)
    gd = metric(Fm0, Gm0)
    n = 4
    g = sp.diag(*gd); gi = sp.diag(*[1 / e for e in gd])
    Gam = [[[sum(gi[a, d] * (sp.diff(g[d, c_], X[b]) + sp.diff(g[d, b], X[c_]) - sp.diff(g[b, c_], X[d])) for d in range(n)) / 2
             for c_ in range(n)] for b in range(n)] for a in range(n)]
    def Riem(a, b, c_, d):    # R^a_{bcd}
        e = sp.diff(Gam[a][b][d], X[c_]) - sp.diff(Gam[a][b][c_], X[d])
        for k in range(n):
            e += Gam[a][c_][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][c_]
        return e
    K = 0
    for a, b, c_, d in itertools.product(range(n), repeat=4):
        R = Riem(a, b, c_, d)
        if R == 0:
            continue
        # R_{abcd} R^{abcd} with diagonal metric: g_aa R^a_bcd * g^bb g^cc g^dd R^a_bcd (a index up in R^a_{bcd})
        K += g[a, a] * R**2 * gi[b, b] * gi[c_, c_] * gi[d, d]
    return sp.simplify(K)
K0 = kretschmann_m0()
L_.check(f"m = 0: Kretschmann = {K0} = 24/ell^4 (constant curvature, i.e. it is de Sitter with radius ell)", sp.simplify(K0 - 24 / ell**4) == 0)

# ------------------------------------------------------------------------ 4D acceleration of the origin (m = 0)
print("\n== a_4 = A at m = 0 (the origin y -> infinity) ==")
Fm0 = Fdl.subs(m, 0); Gm0 = Gdl.subs(m, 0)
pref = 1 / (A**2 * (x + y) ** 2)
gtt = -pref * Fm0
lnroot = sp.log(-gtt) / 2               # a_mu = d_mu ln sqrt(-g_tt) for the static observer u ~ d_t
a2 = (1 / (pref / Fm0)) * sp.diff(lnroot, y) ** 2 + (1 / (pref / Gm0)) * sp.diff(lnroot, x) ** 2
a2lim = sp.limit(sp.simplify(a2), y, sp.oo)
L_.check(f"proper acceleration squared of the origin (y -> infinity, any x): {sp.simplify(a2lim)}  => a_4 = A, exactly, independent of ell", sp.simplify(a2lim - A**2) == 0)
L_.must_fail("control: a_4 is NOT sqrt(A^2 + 1/ell^2) (that is the 5D/embedding acceleration)", sp.simplify(a2lim - (A**2 + 1 / ell**2)) == 0)

# ------------------------------------------------------------------------ C1 conical structure
print("\n== C1: deficits at the poles, checked numerically against the proper circumference/radius ==")
s0 = mp.mpf("0.1")
xm, xs, xn = cm.G_roots(s0)
L_.check(f"three real roots x_- < x_s < 0 < x_n of G at s = 0.1: {mp.nstr(xm,8)}, {mp.nstr(xs,8)}, {mp.nstr(xn,8)}", xm < xs < 0 < xn)
Gnum = lambda xx: 1 - xx**2 - 2 * s0 * xx**3
L_.check("G > 0 on the whole open interval (x_s, x_n) (200 sample points) and G < 0 just outside it", all(Gnum(xs + (xn - xs) * k / 201) > 0 for k in range(1, 201)) and Gnum(xn + mp.mpf('0.01')) < 0 and Gnum(xs - mp.mpf('0.01')) < 0)


def circ_over_radius(s, xpole, kappa, eps=mp.mpf("1e-12")):
    """proper circumference / (2 pi proper radius) on the circle at coordinate distance eps from the pole (limit eps -> 0)"""
    Gf = lambda xx: 1 - xx**2 - 2 * s * xx**3
    sign = 1 if xpole < 0 else -1          # move inside the range [x_s, x_n]
    xe = xpole + sign * eps
    rad = mp.quad(lambda xx: 1 / mp.sqrt(Gf(xx)), [xpole, xe] if sign > 0 else [xe, xpole])
    circ = 2 * mp.pi * kappa * mp.sqrt(Gf(xe))            # z in [0, 2 pi kappa]
    return circ / (2 * mp.pi * rad)


kap = cm.kappa_reg_north(s0)
rn = circ_over_radius(s0, xn, kap)
rs = circ_over_radius(s0, xs, kap)
pred_n = (kap / 2) * abs(cm.Gp(xn, s0))
pred_s = (kap / 2) * abs(cm.Gp(xs, s0))
L_.check(f"north pole regular by the choice kappa = 2/|G'(x_n)|: circumference/(2 pi radius) = {mp.nstr(rn, 8)} -> 1", abs(rn - 1) < mp.mpf("1e-5"))
L_.check(f"south pole: circumference/(2 pi radius) = {mp.nstr(rs, 8)} matches (kappa/2)|G'(x_s)| = {mp.nstr(pred_s, 8)}", abs(rs - pred_s) < mp.mpf("1e-5"))
L_.must_fail("control: the south pole is NOT also regular for this kappa (a strut/string is unavoidable)", abs(rs - 1) < mp.mpf("1e-3"))
mu_s0 = cm.mu_string_south(s0)
L_.check(f"string tension on the south axis mu = (1 - |G'(x_s)|/|G'(x_n)|)/4 = {mp.nstr(mu_s0, 10)} > 0 (a string, not a strut); force {mp.nstr(4*mu_s0,6)} F_max", mu_s0 > 0)
# Lambda independence: G and kappa contain no ell
L_.check("G(x) contains no ell (the conical structure and the tension depend on s = m A only, not on Lambda)", not Gdl.has(ell))
# Newtonian limit  mu -> s = mA  (F = M a)
for sv in ["1e-4", "1e-6"]:
    sv = mp.mpf(sv)
    L_.check(f"small s: mu(s)/s = {mp.nstr(cm.mu_string_south(sv)/sv, 10)} -> 1  (force = m A, Newton's second law)", abs(cm.mu_string_south(sv) / sv - 1) < 10 * sv)
L_.must_fail("control: mu(s)/s does not tend to 2 (the deficit-angle mutation 4 pi G mu would double it)", abs(cm.mu_string_south(mp.mpf('1e-6')) / mp.mpf('1e-6') - 2) < 0.1)

# ------------------------------------------------------------------------ C2 P_none
print("\n== C2: P_none, no string and no strut on either axis ==")
# regularity of both poles requires kappa |G'(x_n)|/2 = kappa|G'(x_s)|/2 = 1, i.e. |G'(x_n)| = |G'(x_s)|.
ss = [mp.mpf(k) / 1000 * SQ for k in range(1, 1000) for SQ in [cm.SQRT27_INV]]
diff = [abs(cm.Gp(cm.G_roots(sv)[2], sv)) - abs(cm.Gp(cm.G_roots(sv)[1], sv)) for sv in ss]
L_.check(f"|G'(x_n)| - |G'(x_s)| > 0 on all 999 grid points of 0 < s < 1/sqrt 27 (min {mp.nstr(min(diff), 6)}): both poles can never be regular simultaneously",
         all(d > 0 for d in diff))
L_.check("the outcome of P_none is: only s = 0 (Schwarzschild-de Sitter or pure dS) is regular on both axes; the C-metric with acceleration and mass needs a string or a strut. Label: EMPTY for A m != 0",
         all(d > 0 for d in diff))
# at s = 0 (m = 0 or A = 0): G = 1 - x^2, both poles regular for kappa = 1 for every A: the label there is q FREE (A arbitrary, no mass, no string)
G0 = 1 - x**2
L_.check("s = 0: G = 1 - x^2 has |G'| = 2 at both poles, so kappa = 1 makes both regular for EVERY A (pure dS observer, no mass, no string): P_none leaves A free at s = 0",
         sp.diff(G0, x).subs(x, 1) == -2 and sp.diff(G0, x).subs(x, -1) == 2)

# ------------------------------------------------------------------------ C3 P_sat
print("\n== C3: P_sat, string force = F_max ==")
mus = [cm.mu_string_south(mp.mpf(k) / 100 * cm.SQRT27_INV) for k in range(1, 100)]
mono = all(mus[i + 1] > mus[i] for i in range(len(mus) - 1))
L_.check("mu(s) is strictly increasing on 0 < s < 1/sqrt 27 (99 grid points) and stays below 1/4", mono and all(v < mp.mpf(1) / 4 for v in mus))
near = cm.mu_string_south(cm.SQRT27_INV * (1 - mp.mpf("1e-12")))
L_.check(f"mu -> 1/4 as s -> 1/sqrt 27: mu(1 - 1e-12 of it) = {mp.nstr(near, 12)}", abs(near - mp.mpf(1) / 4) < mp.mpf("1e-5"))
sx = sp.symbols("s", positive=True)
disc = sp.discriminant(1 - x**2 - 2 * sx * x**3, x)
L_.check(f"discriminant of G in x is {sp.factor(disc)}; it vanishes iff 27 s^2 = 1 (s > 0)", sp.simplify(disc.subs(sx, 1 / sp.sqrt(27))) == 0 and sp.simplify(disc.subs(sx, sp.Rational(1, 10))) != 0)
# mutation of the regularity condition moves the saturation point
mut = mp.mpf(1) / 4 * (1 - (cm.kappa_reg_north(mp.mpf("0.1")) / 4) * abs(cm.Gp(cm.G_roots(mp.mpf("0.1"))[1], mp.mpf("0.1"))))
L_.must_fail("mutation (kappa/2)|G'| -> (kappa/4)|G'| changes the tension at s = 0.1 (so the saturation point is not insensitive to it)", abs(mut - mu_s0) < mp.mpf("1e-10"))

out = {"s0": str(s0), "mu_south_at_s0": str(mu_s0), "saturation_s": str(cm.SQRT27_INV)}
json.dump(out, open(os.path.join(HERE, "y02_results.json"), "w"), indent=1)
L_.finish()
