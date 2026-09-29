#!/usr/bin/env python3
"""l01_sds_facts.py -- independent reproduction of the Schwarzschild-de Sitter two-horizon facts (lane L, puzzle_32pi wave 2).

Independent of agents/I_adversarial_audit/a07,a08: different methods where possible
 - horizon radii from a TRIGONOMETRIC parametrisation of r^3 - L^2 r + 2 M L^2 = 0 (cos 3 psi = -M/M_N), not a numerical polynomial solver;
 - surface gravity from the COVARIANT Killing definition kappa^2 = -(1/2)(nabla_mu xi_nu)(nabla^mu xi^nu) (sympy Christoffels) and from Euclidean regularity, not just f'/2;
 - the a0-points from an EXACT closed form (quadratic in the horizon radius), then compared with the audit's numbers only at the end;
 - first laws, extended (P = -rho_Lambda) first law and Smarr relation by symbolic differentiation.
Units: c = G = 1, L = 1/H_Lambda = 1 in the numerics (L kept symbolic where noted), Z = sqrt(32 pi/3).
"mutation" checks are things that must FAIL if the code/claim were wrong; a PASS there means the wrong statement was rejected.
Exit 0 iff every check held.
"""
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def mut(name, wrong_cond):
    """wrong_cond is a statement that should be FALSE; PASS = it is false (mutation rejected)"""
    ok.append(not bool(wrong_cond)); print(("PASS [mutation rejected] " if not wrong_cond else "FAIL [mutation NOT rejected] ") + name)

Z = mp.sqrt(32 * mp.pi / 3)
a0 = 1 / Z
MN = 1 / (3 * mp.sqrt(3))

# ------------------------------------------------------------------ F1 horizon structure, exact trig parametrisation
def roots_trig(mu):
    """roots of r^3 - r + 2M = 0 (L = 1), M = mu*M_N: r_k = (2/sqrt3) cos(psi_k), cos(3 psi) = -mu"""
    psi0 = mp.acos(-mu) / 3
    yc = 2 / mp.sqrt(3) * mp.cos(psi0)                       # cosmological
    xb = 2 / mp.sqrt(3) * mp.cos(psi0 - 2 * mp.pi / 3)       # black hole
    zn = 2 / mp.sqrt(3) * mp.cos(psi0 + 2 * mp.pi / 3)       # negative root
    return xb, yc, zn

r_, M_, L_ = sp.symbols('r M L', positive=True)
cubic = r_**3 - L_**2 * r_ + 2 * M_ * L_**2
disc = sp.factor(sp.discriminant(cubic, r_))
chk("F1a discriminant of r^3 - L^2 r + 2 M L^2 is 4 L^4 (L^2 - 27 M^2): vanishes at M = L/(3 sqrt3) = M_Nariai; three real roots for M < M_N", sp.simplify(disc - 4 * L_**4 * (L_**2 - 27 * M_**2)) == 0)
worst = mp.mpf(0)
for mu in ['0.001', '0.2', '0.5', '0.9', '0.987', '0.9999']:
    mu = mp.mpf(mu); M = mu * MN
    xb, yc, zn = roots_trig(mu)
    f = lambda r: 1 - 2 * M / r - r**2
    worst = max(worst, abs(f(xb)), abs(f(yc)), abs(zn**3 - zn + 2 * M), abs(xb + yc + zn), abs(xb**2 + xb * yc + yc**2 - 1), abs(xb * yc * (xb + yc) - 2 * M))
chk("F1b trig roots satisfy f(r_b) = f(r_c) = 0, r_b + r_c + r_- = 0, x^2 + x y + y^2 = 1, 2M = x y (x + y) at 6 masses (max residual %s)" % mp.nstr(worst, 3), worst < mp.mpf('1e-35'))
xb, yc, zn = roots_trig(mp.mpf(1))
chk("F1c Nariai limit: r_b = r_c = 1/sqrt3 (L = 1) from the trig roots", abs(xb - 1 / mp.sqrt(3)) < 1e-35 and abs(yc - 1 / mp.sqrt(3)) < 1e-35)
xb, yc, zn = roots_trig(mp.mpf(0))
chk("F1d M -> 0: r_b = 0, r_c = L (pure de Sitter)", abs(xb) < 1e-35 and abs(yc - 1) < 1e-35)

# ------------------------------------------------------------------ F2 surface gravity from the covariant Killing definition
t, r, th, ph = sp.symbols('t r theta phi', real=True)
Ms, Ls = sp.symbols('M L', positive=True)
f = 1 - 2 * Ms / r - r**2 / Ls**2
g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
ginv = g.inv()
X = [t, r, th, ph]
Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
xi_low = [g[n, 0] for n in range(4)]            # xi = d_t: xi_nu = g_{nu t}
nab = sp.Matrix(4, 4, lambda m, n: sp.diff(xi_low[n], X[m]) - sum(Gam[l][m][n] * xi_low[l] for l in range(4)))   # nabla_mu xi_nu
killing = sp.simplify(nab + nab.T)
chk("F2a xi = d_t is a Killing vector of SdS (nabla_(mu xi_nu) = 0, direct Christoffel computation)", killing == sp.zeros(4, 4))
nabup = ginv * nab * ginv                        # nabla^mu xi^nu
kap2 = sp.simplify(-sp.Rational(1, 2) * sum(nab[m, n] * nabup[m, n] for m in range(4) for n in range(4)))
chk("F2b covariant kappa^2 = -(1/2) nabla_mu xi_nu nabla^mu xi^nu = f'(r)^2/4 (r-independent expression, so evaluated on either horizon it gives (f'(r_h)/2)^2)", sp.simplify(kap2 - sp.diff(f, r)**2 / 4) == 0)
# Euclidean regularity: near r_h,  f ~ f'(r_h)(r-r_h), with rho = 2 sqrt((r-r_h)/f') the metric is  rho^2 (f'/2)^2 dtau^2 + drho^2  =>  beta = 4 pi/|f'| = 2 pi/kappa
rr, rh, fp = sp.symbols('rr rh fp', positive=True)
rho = 2 * sp.sqrt((rr - rh) / fp)
lhs = sp.simplify(fp * (rr - rh))                    # g_tautau
rhs = sp.simplify(rho**2 * (fp / 2)**2)
chk("F2c Euclidean regularity: g_tautau = rho^2 (f'/2)^2 near the horizon, hence the smooth period is beta = 2 pi/(f'/2) = 2 pi/kappa (kappa = |f'|/2 is the regularity normalisation of t)", sp.simplify(lhs - rhs) == 0)

# closed-form kappas in terms of horizon radius (L = 1): kappa_b = (1-3x^2)/(2x), kappa_c = (3y^2-1)/(2y)
x_, y_ = sp.symbols('x y', positive=True)
Mx = (x_ - x_**3) / 2                       # 2M = r - r^3 at r = x (horizon condition)
kb_expr = sp.simplify((sp.Rational(1, 2)) * (2 * Mx / x_**2 - 2 * x_))
kc_expr = sp.simplify(-(sp.Rational(1, 2)) * (2 * ((y_ - y_**3) / 2) / y_**2 - 2 * y_))
chk("F2d kappa_b L = (1 - 3 x^2)/(2 x) and kappa_c L = (3 y^2 - 1)/(2 y) from f'/2 with the horizon condition 2M = r - r^3", sp.simplify(kb_expr - (1 - 3 * x_**2) / (2 * x_)) == 0 and sp.simplify(kc_expr - (3 * y_**2 - 1) / (2 * y_)) == 0)
kb_of = lambda x: (1 - 3 * x**2) / (2 * x)
kc_of = lambda y: (3 * y**2 - 1) / (2 * y)
mut("F2e mutation: kappa = f'(r_h) (missing 1/2) does NOT give kappa_c(M=0) = H", abs(2 * kc_of(mp.mpf(1)) - 1) < 1e-30)
chk("F2f pure de Sitter: kappa_c(M=0) = H exactly; kappa_b -> infinity as M -> 0; both -> 0 at Nariai", abs(kc_of(mp.mpf(1)) - 1) < 1e-35 and kb_of(mp.mpf('1e-9')) > 1e8 and abs(kb_of(1 / mp.sqrt(3))) < 1e-35)

# ------------------------------------------------------------------ F3 Bousso-Hawking normalisation
def kBH(mu):
    M = mu * MN; xb, yc, _ = roots_trig(mu)
    rstar = M**(mp.mpf(1) / 3)
    fs = 1 - 2 * M / rstar - rstar**2
    return kb_of(xb) / mp.sqrt(fs), kc_of(yc) / mp.sqrt(fs), fs
fp_sym = sp.diff(1 - 2 * M_ / r_ - r_**2, r_)
rstar_sol = sp.solve(sp.Eq(fp_sym, 0), r_)
chk("F3a f'(r*) = 0 at r*^3 = M L^2 (static geodesic observer); f(r*) = 1 - 3 M^(2/3) for L = 1", sp.simplify(sp.simplify(fp_sym.subs(r_, M_**sp.Rational(1, 3))) ) == 0 and sp.simplify((1 - 2 * M_ / r_ - r_**2).subs(r_, M_**sp.Rational(1, 3)) - (1 - 3 * M_**sp.Rational(2, 3))) == 0)
vals0 = kBH(mp.mpf('1e-12'))
valsN = kBH(mp.mpf(1) - mp.mpf('1e-14'))
chk("F3b BH-normalisation: kappa_c -> H (=1) as M -> 0 and kappa_b, kappa_c -> sqrt(3) H at Nariai (%s, %s)" % (mp.nstr(valsN[0], 8), mp.nstr(valsN[1], 8)),
    abs(vals0[1] - 1) < 1e-6 and abs(valsN[0] - mp.sqrt(3)) < 1e-6 and abs(valsN[1] - mp.sqrt(3)) < 1e-6)
mus = [mp.mpf(v) for v in ('1e-6', '0.01', '0.1', '0.3', '0.6', '0.9', '0.99', '0.9999')]
allb = all(kBH(m)[0] > mp.sqrt(3) - 1e-3 for m in mus); allc = all(1 - 1e-6 < kBH(m)[1] < mp.sqrt(3) + 1e-6 for m in mus)
chk("F3c BH-normalised kappa_b >= sqrt3 H and H <= kappa_c <= sqrt3 H at 8 masses: no SdS horizon has kappa < H in that normalisation", allb and allc)
# analytic near-Nariai: kappa_f^2 L^2 = 2(1-mu) at leading order, f(r*) = (2/3)(1-mu)  ->  ratio sqrt3
eps = mp.mpf('1e-10'); mu = 1 - eps
xb, yc, _ = roots_trig(mu)
chk("F3d near-Nariai leading order: (kappa_f L)^2 = 2 (1 - mu) (rel. error %s)" % mp.nstr(abs(kb_of(xb)**2 / (2 * eps) - 1), 3), abs(kb_of(xb)**2 / (2 * eps) - 1) < 1e-4)

# ------------------------------------------------------------------ F4 thermodynamics
# first laws (fixed L): dM = T_b dS_b  and  dM = - T_c dS_c ;  S = pi r^2 (A/4), T = kappa/2pi
Mr = (x_ - x_**3) / 2
dM_dx = sp.diff(Mr, x_)
TbdSb = (kb_of(x_) / (2 * sp.pi)) * sp.diff(sp.pi * x_**2, x_)
TcdSc = (kc_of(x_) / (2 * sp.pi)) * sp.diff(sp.pi * x_**2, x_)     # same functional form with x -> y; horizon radius symbol reused
chk("F4a first law of the black-hole horizon: dM = T_b dS_b (fixed L), T_b = kappa_b/2pi, S_b = pi r_b^2", sp.simplify(dM_dx - TbdSb) == 0)
chk("F4b first law of the cosmological horizon carries the NEGATIVE-energy sign: dM = - T_c dS_c (raising M shrinks r_c); equivalently E_c = -M obeys dE_c = +T_c dS_c", sp.simplify(dM_dx + TcdSc) == 0)
mut("F4c mutation: dM = +T_c dS_c is false", sp.simplify(dM_dx - TcdSc) == 0)
# total entropy
for mm in ['0.05', '0.5', '0.95']:
    xb, yc, _ = roots_trig(mp.mpf(mm))
    assert abs((xb**2 + yc**2) - (1 - xb * yc)) < 1e-30
Sfun = lambda mu: (lambda a, b, c: mp.pi * (a**2 + b**2))(*roots_trig(mu))
dSdM = lambda mu: mp.diff(Sfun, mu) / MN
lhs = [dSdM(mp.mpf(m)) for m in ['0.05', '0.5', '0.95']]
rhs = [2 * mp.pi * (1 / kb_of(roots_trig(mp.mpf(m))[0]) - 1 / kc_of(roots_trig(mp.mpf(m))[1])) for m in ['0.05', '0.5', '0.95']]
chk("F4d S_tot = pi (r_b^2 + r_c^2) = pi L^2 (1 - x y) and dS_tot/dM = 2 pi (1/kappa_b - 1/kappa_c) < 0 (numerical derivative vs formula, 3 masses; entropy DEcreases with M)",
    all(abs(a - b) < 1e-20 for a, b in zip(lhs, rhs)) and all(a < 0 for a in lhs))
chk("F4e S_tot(Nariai)/S_dS = 2/3 (1 - x y at x = y = 1/sqrt3) and S_tot < S_dS on the whole family (entropy bound)", abs((1 - (1 / mp.sqrt(3))**2) - mp.mpf(2) / 3) < 1e-35 and all(Sfun(mp.mpf(m)) < mp.pi for m in ['0.001', '0.3', '0.9', '0.9999']))
# extended first law with P = -rho_Lambda = -Lambda/(8 pi), V_b = 4 pi r_b^3/3, and Smarr
Lam, rb = sp.symbols('Lambda r_b', positive=True)
Mext = rb / 2 * (1 - Lam * rb**2 / 3)
kap_b = sp.simplify(sp.Rational(1, 2) * (2 * Mext / rb**2 - 2 * rb * Lam / 3))
Tb = kap_b / (2 * sp.pi); Sb = sp.pi * rb**2
Pv = -Lam / (8 * sp.pi); Vb = sp.Rational(4, 3) * sp.pi * rb**3
chk("F4f extended first law dM = T dS + V dP with P = -rho_Lambda = -Lambda/8pi, V = 4 pi r_b^3/3 (partial derivatives in r_b and Lambda)",
    sp.simplify(sp.diff(Mext, rb) - Tb * sp.diff(Sb, rb)) == 0 and sp.simplify(sp.diff(Mext, Lam) - Vb * sp.diff(Pv, Lam)) == 0)
chk("F4g Smarr relation M = 2 T S - 2 P V = kappa_b r_b^2 + (8 pi/3) rho_Lambda r_b^3 (weights 1 = 2 - 2(-2 + 3)/... verified as an identity)",
    sp.simplify(Mext - (2 * Tb * Sb - 2 * Pv * Vb)) == 0 and sp.simplify(Mext - (kap_b * rb**2 + sp.Rational(8, 3) * sp.pi * (Lam / (8 * sp.pi)) * rb**3)) == 0)

# ------------------------------------------------------------------ F5 Nariai near-horizon geometry
eps_s, rho_s = sp.symbols('epsilon rho', real=True)
Ls = sp.symbols('L', positive=True)
r0 = Ls / sp.sqrt(3); MN_s = Ls / (3 * sp.sqrt(3))
fN = (1 - 2 * MN_s * (1 - eps_s) / (r0 + rho_s) - (r0 + rho_s)**2 / Ls**2)
ser = sp.series(fN, rho_s, 0, 3).removeO()
c0 = sp.simplify(ser.coeff(rho_s, 0)); c1 = sp.simplify(ser.coeff(rho_s, 1)); c2 = sp.simplify(ser.coeff(rho_s, 2))
# f(rho) = f0 - 3 rho^2/L^2 at leading order in eps: eps-independent quadratic coefficient at eps = 0
c2_0 = sp.simplify(c2.subs(eps_s, 0)); c0_1 = sp.simplify(sp.diff(c0, eps_s).subs(eps_s, 0))
chk("F5a near Nariai: f = (2/3) eps - 3 rho^2/L^2 + O(rho^3, eps rho) with r = L/sqrt3 + rho, M = M_N (1 - eps)", sp.simplify(c2_0 + 3 / Ls**2) == 0 and sp.simplify(c0_1 - sp.Rational(2, 3)) == 0 and sp.simplify(c1.subs(eps_s, 0)) == 0)
# 2D curvature of -f dt^2 + d rho^2/f is -f'': dS2 of radius ell, R2 = 2/ell^2
fq = sp.Symbol('f0') - 3 * rho_s**2 / Ls**2
R2 = -sp.diff(fq, rho_s, 2)
ell2 = sp.simplify(2 / R2)
chk("F5b the (t, rho) factor is dS_2 of radius ell = L/sqrt3 (R_2 = -f'' = 6/L^2 = 2/ell^2), the sphere factor has radius r_0 = L/sqrt3: the Nariai geometry is dS_2 x S^2 with EQUAL radii L/sqrt3", sp.simplify(ell2 - Ls**2 / 3) == 0)
chk("F5c R_4 = 2/ell^2 + 2/r_0^2 = 12/L^2 = 4 Lambda (consistency of the product with the Einstein equation R_mn = Lambda g_mn)", sp.simplify(2 / ell2 + 2 / r0**2 - 12 / Ls**2) == 0)
# ultracold: needs f = f' = f'' = 0 ; SdS has none (roots sum to zero -> triple root only at r = 0)
sol = sp.solve([sp.Eq(f, 0), sp.Eq(sp.diff(f, r), 0), sp.Eq(sp.diff(f, r, 2), 0)], [r, Ms], dict=True)
sol = [s for s in sol if s[r].is_positive and s[Ms].is_positive] if sol else []
chk("F5d no 'ultracold' (triple-root) point exists in the SdS family for r, M > 0 (needs charge); the only degenerate configuration is Nariai f = f' = 0", len(sol) == 0)

# ------------------------------------------------------------------ F6 static observers
# u^mu = (1/sqrt f) d_t ; a^mu = Gamma^mu_tt u^t u^t ; |a| = sqrt(g_rr) |a^r|
ar = sp.simplify(Gam[1][0][0] / f)
a_mag = sp.simplify(sp.sqrt(1 / f) * ar)         # a^r sqrt(g_rr)
chk("F6a static-observer proper acceleration a = f'(r)/(2 sqrt f) (Christoffel computation)", sp.simplify(a_mag - sp.diff(f, r) / (2 * sp.sqrt(f))) == 0 or sp.simplify(a_mag**2 - sp.diff(f, r)**2 / (4 * f)) == 0)
a_dS = sp.simplify((sp.diff(f, r) / (2 * sp.sqrt(f))).subs(Ms, 0))
chk("F6b pure dS: a L = tan(theta) for r = L sin(theta)", sp.simplify((a_dS * Ls).subs(r, Ls * sp.sin(th)) - sp.sin(th) / sp.cos(th)) == 0 or sp.simplify(((a_dS * Ls)**2).subs(r, Ls * sp.sin(th)) - sp.tan(th)**2) == 0)
th0 = mp.atan(1 / Z)
chk("F6c a0 static worldline in pure dS: tan(theta0) = 1/Z, sin(theta0) = 1/sqrt(1+Z^2) = %s (the earlier 'static observer' fact)" % mp.nstr(mp.sin(th0), 10), abs(mp.sin(th0) - 1 / mp.sqrt(1 + Z**2)) < 1e-35)
# Deser-Levin / Tolman: T_loc = kappa_dS/(2 pi sqrt f) = sqrt(a^2 + H^2)/(2 pi)
chk("F6d Tolman: in pure dS kappa_dS/sqrt(f) = sqrt(a^2 + H^2) exactly (the static-patch Unruh-effective temperature T^2 = (a^2 + H^2)/4 pi^2)",
    sp.simplify(((1 / Ls) / sp.sqrt(f.subs(Ms, 0)))**2 - (sp.diff(f.subs(Ms, 0), r)**2 / (4 * f.subs(Ms, 0)) + 1 / Ls**2)) == 0)

# ------------------------------------------------------------------ F7 the a0-points, exact closed forms, then comparison with the audit
# black-hole horizon: (1 - 3x^2)/(2x) = 1/Z  ->  x = (sqrt(1 + 3 Z^2) - 1)/(3 Z);  cosmological: (3 y^2 - 1)/(2 y) = 1/Z -> y = (sqrt(1+3Z^2) + 1)/(3Z)
xs = (mp.sqrt(1 + 3 * Z**2) - 1) / (3 * Z)
ys_from_xs = (-xs + mp.sqrt(4 - 3 * xs**2)) / 2                       # from x^2 + x y + y^2 = 1
mu_b = mp.mpf(3) * mp.sqrt(3) * xs * (1 - xs**2) / 2
chk("F7a exact closed form r_b/L = (sqrt(1+3Z^2) - 1)/(3Z) = (sqrt(1+32 pi) - 1)/sqrt(96 pi) = %s solves kappa_b = a0; 1 + 3 Z^2 = 1 + 32 pi" % mp.nstr(xs, 12),
    abs(kb_of(xs) - a0) < 1e-35 and abs(3 * Z**2 - 32 * mp.pi) < 1e-35 and abs(xs - (mp.sqrt(1 + 32 * mp.pi) - 1) / mp.sqrt(96 * mp.pi)) < 1e-35)
xb_t, yc_t, _ = roots_trig(mu_b)
chk("F7b consistency: the trig parametrisation at mu* = (3 sqrt3/2) x(1-x^2) = %s returns the same r_b and r_c = %s (partner from x^2+xy+y^2=1)" % (mp.nstr(mu_b, 12), mp.nstr(ys_from_xs, 10)),
    abs(xb_t - xs) < 1e-30 and abs(yc_t - ys_from_xs) < 1e-30 and abs(mu_b * MN - xs * ys_from_xs * (xs + ys_from_xs) / 2) < 1e-30)
yc_a0 = (mp.sqrt(1 + 3 * Z**2) + 1) / (3 * Z)
xb_c, yc_c = None, yc_a0
# partner black-hole radius for the cosmological a0-point:  x = (-y + sqrt(4-3y^2))/2
xb_c = (-yc_a0 + mp.sqrt(4 - 3 * yc_a0**2)) / 2
mu_c = mp.mpf(3) * mp.sqrt(3) * yc_a0 * (1 - yc_a0**2) / 2
chk("F7c cosmological-horizon a0-point: r_c/L = (sqrt(1+3Z^2)+1)/(3Z) = %s, mu_c = %s, partner r_b = %s; kappa_c = a0" % (mp.nstr(yc_a0, 10), mp.nstr(mu_c, 10), mp.nstr(xb_c, 8)), abs(kc_of(yc_a0) - a0) < 1e-35)
# compare with the audit's printed numbers (a07 .out): 0.9869523914, 0.52263231, 0.63039097, 0.98298404
chk("F7d agreement with the audit (a07): mu_b* = 0.9869523914, r_b = 0.52263231, r_c = 0.63039097; mu_c* = 0.98298404", abs(mu_b - mp.mpf('0.9869523914')) < 1e-9 and abs(xs - mp.mpf('0.52263231')) < 1e-8 and abs(ys_from_xs - mp.mpf('0.63039097')) < 1e-8 and abs(mu_c - mp.mpf('0.98298404')) < 1e-8)
mut("F7e mutation: with kappa = f' (no 1/2) the black-hole a0-point would sit at mu = 0.9869523914 (it does not)", abs(mp.findroot(lambda m: 2 * kb_of(roots_trig(m)[0]) - a0, mp.mpf('0.99')) - mp.mpf('0.9869523914')) < 1e-6)
# residual check of the horizon equations at the a0-point
M = mu_b * MN
chk("F7f f(r_b) = f(r_c) = 0 at M*: residuals %s %s" % (mp.nstr(abs(1 - 2 * M / xs - xs**2), 2), mp.nstr(abs(1 - 2 * M / ys_from_xs - ys_from_xs**2), 2)), abs(1 - 2 * M / xs - xs**2) < 1e-30 and abs(1 - 2 * M / ys_from_xs - ys_from_xs**2) < 1e-30)

print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
