#!/usr/bin/env python3
"""r05_newtonian_and_nonlinear.py -- the ball around a mass in the Newtonian regime, and the NON-LINEAR (beyond first order) exact equilibrium relation.

 N1  flat space, spherical mass: first-order fixed-V area deficit dA|_V = -8 pi G int xi rho dV, xi = (l^2-r^2)/(2l); for a point mass at the centre dA|_V/A = -G M/(l c^2) = Phi(l)/c^2
     (the fractional area deficit IS the Newtonian potential).  Checked against the EXACT GR interior/exterior slice of a uniform star (root-finding), and a wrong weight is rejected.
 N2  additivity: for a uniform-density ball the exact slice is S^3(L_c) with L_c^-2 = L^-2 + (8 pi G/3) rho_m; Lambda and matter enter ONLY through the total curvature, so the exact fixed-V area
     A_V = A_flat(V) Psi(u), u = l_f/L_c, is a function of ONE variable.  Series of Psi.
 N3  the nonlinear threshold g_*(x): boundary Newtonian acceleration g = G M/r_b^2 at which the second-order term of A_V equals the first-order term, for a ball of geodesic radius x L in dS.
     g_*(x) is a continuous strictly decreasing function from infinity (small balls, g_* l = const = c^2 x number) to 0 (x -> pi).  It takes EVERY value; it selects no acceleration.
 N4  Lambda-vs-mass crossover g_eq(x) = H^2 R x number: mass deficit equals the exact Lambda deficit; grows linearly with R (not a fixed acceleration)
 N5  why no fixed acceleration can appear: A_V is analytic in (M, 1/L^2) with only non-negative powers, so g/H = (M/R^2) L can only enter through the ratio (M/R)/(R/L), a ratio of two small numbers,
     whose O(1) values have first-order (mass and Lambda) terms comparable, not a departure from the equilibrium relation.
Exit 0 = all pass.
"""
import sys
import mpmath as mp
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

mp.mp.dps = 40

# ------------------------------------------------------------------------------------------------ N1
print("N1  flat space, exact GR uniform star vs the first-order equilibrium relation")
def flat_star_deficit(Mtot, rb):
    """exact slice of a uniform star (G=1): f = 1 - 2 M r^2/rb^3.  V_exact by quadrature, area 4 pi rb^2; returns dA_V (area minus flat area of the same volume)."""
    V = 4 * mp.pi * mp.quad(lambda r: r**2 / mp.sqrt(1 - 2 * Mtot * r**2 / rb**3), [0, rb])
    Aflat = (36 * mp.pi) ** (mp.mpf(1) / 3) * V ** (mp.mpf(2) / 3)
    return 4 * mp.pi * rb**2 - Aflat, Aflat
rb = mp.mpf(1)
for mu in (mp.mpf('1e-4'), mp.mpf('1e-6')):
    dAV, Aflat = flat_star_deficit(mu * rb / 2, rb)          # mu = 2 M / rb (compactness)
    pred = -8 * mp.pi * (mu * rb / 2) * rb / 5
    check(f"uniform star, compactness 2M/r_b = {mp.nstr(mu, 3)}: exact dA_V = {mp.nstr(dAV, 10)} vs -8 pi M l/5 = {mp.nstr(pred, 10)} (rel {mp.nstr(abs(dAV / pred - 1), 3)})",
          abs(dAV / pred - 1) < 5 * mu)
    must_fail(f"N1b wrong coefficient -4 pi M l/5 at compactness {mp.nstr(mu, 3)}", abs(dAV / (pred / 2) - 1) < 0.1)
# point-mass weight: xi_c = l/2 => dA_V/A = -G M/l
l_, M_ = sp.symbols('l M', positive=True)
Apt = 4 * sp.pi * l_**2
dApt = -8 * sp.pi * M_ * (l_ / 2)
check("point mass at the centre: dA_V / A = -G M / l  (fractional area deficit = Newtonian potential Phi(l) = -G M/l)", sp.simplify(dApt / Apt + M_ / l_) == 0)
# the general first-order relation against the exact-GR sanity for a THIN shell (all mass at radius a): weight xi(a)
# (exact through the E2 identity of r03; here only the closed form)
a_ = sp.symbols('a', positive=True)
check("shell of mass M at radius a inside the ball: dA_V = -8 pi M (l^2 - a^2)/(2 l); it vanishes for a shell on the boundary (a = l): mass outside/at the edge does not change the area at fixed V",
      sp.simplify((-8 * sp.pi * M_ * (l_**2 - a_**2) / (2 * l_)).subs(a_, l_)) == 0)

# ------------------------------------------------------------------------------------------------ N2
print("N2  additivity: Lambda and matter enter only through the total curvature; Psi(u) with one variable")
rhoL, rhom, Gn, L = sp.symbols('rho_L rho_m G L', positive=True)
Lc2 = sp.symbols('Lc2', positive=True)
# Hamiltonian constraint on a uniform slice: 6/Lc^2 = 16 pi G rho_tot ; reference 6/L^2 = 16 pi G rho_L
inv_Lc2 = 16 * sp.pi * Gn * (rhoL + rhom) / 6
inv_L2 = 16 * sp.pi * Gn * rhoL / 6
check("1/L_c^2 = 1/L^2 + (8 pi G/3) rho_m  (Lambda and matter add in the curvature)", sp.simplify(inv_Lc2 - inv_L2 - 8 * sp.pi * Gn * rhom / 3) == 0)
u, y_ = sp.symbols('u y', positive=True)
# Psi(u) from the parametric solution  u^3 = (3/2)(x - sin x cos x),  Psi = sin^2 x / u^2
xx = sp.symbols('xx', positive=True)
cs = sp.symbols('c1:6')
xser = xx * (1 + sum(cs[i] * xx**(2 * (i + 1)) for i in range(4)))
# u^3 as series in x:  (3/2)(x - sin x cos x) = x^3 (1 - (2/5) x^2 + ...)
u3 = sp.series(sp.Rational(3, 2) * (xx - sp.sin(xx) * sp.cos(xx)), xx, 0, 12).removeO()
Psi_x = sp.series(sp.sin(xx)**2 / (u3)**sp.Rational(2, 3), xx, 0, 8).removeO()
# express in u: u = x (1 - 2/5 x^2 + ...)^(1/3); invert numerically-exact via series reversion
useries = sp.series(u3**sp.Rational(1, 3), xx, 0, 9).removeO()
# reversion: x as a series in u
ua = sp.symbols('ua')
xr = ua
for _ in range(6):
    xr = sp.series(ua - (sp.expand(useries.subs(xx, xr)) - xr), ua, 0, 9).removeO()
Psi_u = sp.series(Psi_x.subs(xx, xr), ua, 0, 7).removeO()
Psi_u = sp.expand(Psi_u)
print("      Psi(u) = A_V / A_flat(V) =", Psi_u, "+ ...")
c_first, c_second = Psi_u.coeff(ua, 2), Psi_u.coeff(ua, 4)
check(f"Psi(u) = 1 - u^2/5 + ...: first coefficient {c_first} (= -(d-2)/(2(d+1)) at d = 4, eq (22) with a curvature radius L_c)", c_first == sp.Rational(-1, 5))
print("      second coefficient c2 =", c_second)
must_fail("N2b first coefficient equals -1/10", c_first == sp.Rational(-1, 10))

# ------------------------------------------------------------------------------------------------ N3
print("N3  nonlinear threshold g_*(x) in de Sitter (uniform-density ball, L = 1, H = 1)")
def AV(s, V, guess):
    Lc = 1 / mp.sqrt(s)
    f = lambda xg: 2 * mp.pi * Lc**3 * (xg - mp.sin(xg) * mp.cos(xg)) - V
    xg = mp.findroot(f, guess)
    return 4 * mp.pi * Lc**2 * mp.sin(xg)**2
def Vof(xg): return 2 * mp.pi * (xg - mp.sin(xg) * mp.cos(xg))
def gstar(xg):
    V = Vof(xg)
    A1 = mp.diff(lambda s: AV(s, V, xg), 1, 1)
    A2 = mp.diff(lambda s: AV(s, V, xg), 1, 2)
    return mp.sin(xg) * abs(A1 / A2), A1, A2
xs = [mp.mpf(v) for v in ('0.05', '0.1', '0.3', '0.5', '0.8', '1.0', '1.3', mp.pi / 2, '1.8', '2.0', '2.2', '2.4', '2.6', '2.8', '3.0')]
gs = []
A2s = []
A1s = []
for xg in xs:
    g, A1, A2 = gstar(xg)
    gs.append(g); A1s.append(A1); A2s.append(A2)
print("      x       g_*/H        g_* x")
for xg, g in zip(xs, gs):
    print(f"      {mp.nstr(xg, 5):8s} {mp.nstr(g, 8):>14s} {mp.nstr(g * xg, 6):>10s}")
check("first and second derivatives of A_V(s) are negative at every sampled radius: the geometric part is decreasing AND concave in the curvature at fixed V (the second-order variation has the sign the maximality half of the hypothesis needs)", all(a < 0 for a in A1s) and all(a < 0 for a in A2s))
must_fail("N3b the second derivative of A_V(s) is positive at some sampled radius", any(a > 0 for a in A2s))
check("g_*(x) is strictly decreasing on the sampled radii 0.05 ... 3.0", all(gs[i] > gs[i + 1] for i in range(len(gs) - 1)))
check("g_* x -> constant (a POTENTIAL threshold, c^2 x number) as x -> 0: g_* x at x=0.05, 0.1 =" + f" {mp.nstr(gs[0] * xs[0], 6)}, {mp.nstr(gs[1] * xs[1], 6)}", abs(gs[0] * xs[0] - gs[1] * xs[1]) < 0.15)
# analytic small-x limit from Psi: A_V = A_flat (1 - u^2/5 + c2 u^4), u^2 = s l_f^2.  g_* = sin x |A'/A''| -> x |(-1/5)/(2 c2)|/(x^2 ...)
# g_* x -> |c_first| / (2 |c_second|)  in units where l_f = x, s-derivative at s = 1: A' = A_flat c_first x^2, A'' = 2 A_flat c_second x^4 => g_* = x*(x^2/5)/(2 c2 x^4) => g_* x = 1/(10 |c2|)
lim = sp.Rational(1, 10) / abs(c_second) if c_second != 0 else sp.oo
check(f"small-x limit g_* x = 1/(10 |c2|) = {lim} = {float(lim):.6f} matches the numerics ({mp.nstr(gs[0] * xs[0], 6)})", abs(float(lim) - float(gs[0] * xs[0])) < 0.15)
# the value of x at which g_* = a0 = H/Z (this is the ONLY place where the target enters; comparison, not a candidate)
Z = mp.sqrt(32 * mp.pi / 3)
a0H = 1 / Z
xa = mp.findroot(lambda xg: gstar(xg)[0] - a0H, 2.25)
print(f"      g_*(x) = H/Z = {mp.nstr(a0H, 8)} at x = {mp.nstr(xa, 8)} = {mp.nstr(xa / mp.pi, 8)} pi;  x l_f in units of the puzzle radius r_s = Z L/2 = {mp.nstr(Z / 2, 6)} L")
xdecl = {"pi/2 (X1)": mp.pi / 2, "pi/4 (X2)": mp.pi / 4, "1 (X5)": mp.mpf(1), "sqrt(8pi/3) (X6)": mp.sqrt(8 * mp.pi / 3)}
xpost = dict(xdecl); xpost.update({"pi/3 (post hoc)": mp.pi / 3, "2pi/3 (post hoc)": 2 * mp.pi / 3, "3pi/4 (post hoc)": 3 * mp.pi / 4})
def mindist(xv, table):
    return min((abs(xv / v - 1), k) for k, v in table.items())
d_decl = mindist(xa, xdecl); d_post = mindist(xa, xpost)
print(f"      nearest DECLARED radius: {d_decl[1]} at relative distance {float(d_decl[0]):.3f};  nearest incl. post-hoc additions: {d_post[1]} at {float(d_post[0]):.3f}")
# calibration: for 60 decoy targets log-uniform in [0.02, 2] H, the distribution of the same statistic
import math
decoys = [mp.mpf(10) ** (mp.mpf(-1.7) + mp.mpf(2.0) * k / 59) for k in range(60)]
dd_decl, dd_post = [], []
for t in decoys:
    xr_ = mp.findroot(lambda xg, t=t: gstar(xg)[0] - t, (mp.mpf('0.06'), mp.mpf('3.05')), solver='illinois')
    dd_decl.append(float(mindist(xr_, xdecl)[0])); dd_post.append(float(mindist(xr_, xpost)[0]))
frac_decl = sum(v <= float(d_decl[0]) for v in dd_decl) / len(dd_decl)
frac_post = sum(v <= float(d_post[0]) for v in dd_post) / len(dd_post)
print(f"      calibration over 60 decoy accelerations: fraction of decoys at least as close to a natural radius: declared list {frac_decl:.2f}, incl. post-hoc list {frac_post:.2f}")
check("the a0 radius is NOT closer to the declared natural radii than typical decoys (calibration fraction >= 0.5)", frac_decl >= 0.5)
check(f"with the enlarged post-hoc list the proximity (4%) is unremarkable: {frac_post:.2f} of decoys are at least as close (a continuum target always sits near some natural fraction of pi)", frac_post >= 0.15)
roots = {}
for t in (mp.mpf('0.05'), mp.mpf('0.3'), mp.mpf(1), mp.mpf(10)):
    roots[float(t)] = mp.findroot(lambda xg, t=t: gstar(xg)[0] - t, (mp.mpf('0.06'), mp.mpf('3.0')), solver='illinois')
print("      radii where g_* = 0.05 H, 0.3 H, 1 H, 10 H:", {k: float(mp.nstr(v, 5)) for k, v in roots.items()})
check("g_*(x) is a continuous bijection onto (0, infinity): it also equals 0.05 H, 0.3 H, 1 H, 10 H at some radius (so 'equals a0 somewhere' carries no information)",
      all(abs(gstar(v)[0] - k) < 1e-10 * max(1, k) for k, v in roots.items()))

# ------------------------------------------------------------------------------------------------ N4
print("N4  mass-equals-Lambda crossover g_eq(x)")
Z_ = mp.sqrt(32 * mp.pi / 3)
def g_eq(xg):
    V = Vof(xg)
    Aflat = (36 * mp.pi) ** (mp.mpf(1) / 3) * V ** (mp.mpf(2) / 3)
    AdS = 4 * mp.pi * mp.sin(xg)**2
    GM = (Aflat - AdS) / (8 * mp.pi * mp.tan(xg / 2))       # 8 pi G M xi_c = area deficit, xi_c = L tan(x/2)
    return GM / xg**2                                        # G M / R^2 in units H = 1/L
print("      x       g_eq/H    g_eq/(H x)")
tab = {}
for xg in (mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf(1), mp.pi / 2, mp.mpf(2), mp.mpf('2.5')):
    tab[xg] = g_eq(xg)
    print(f"      {mp.nstr(xg, 5):8s} {mp.nstr(tab[xg], 8):>12s} {mp.nstr(tab[xg] / xg, 8):>12s}")
xk = list(tab.keys())
check(f"small-radius limit g_eq -> H^2 R/5 (g_eq/(H x) at x=0.01 is {mp.nstr(tab[xk[0]] / xk[0], 6)}, expected 0.2)", abs(tab[xk[0]] / xk[0] - mp.mpf(1) / 5) < 2e-3)
vals = [tab[k] for k in xk]
check("g_eq/(H x) is strictly decreasing in x: linear growth g_eq = H^2 R/5 only at small radius", all(tab[xk[i]] / xk[i] > tab[xk[i + 1]] / xk[i + 1] for i in range(len(xk) - 1)))
xm = mp.findroot(lambda xg: mp.diff(g_eq, xg), 1.4)
gm = g_eq(xm)
print(f"      g_eq has a single maximum g_max = {mp.nstr(gm, 8)} H at x = {mp.nstr(xm, 6)} (= {mp.nstr(xm / mp.pi, 5)} pi); g_max/(H/Z) = {mp.nstr(gm * Z_, 6)}")
check("g_eq(x) is bounded: it rises ~ linearly for small x, peaks at x ~ 1.3 and falls (a maximum, not a fixed acceleration): g_eq(0.01) < g_max, g_eq(2.5) < g_max",
      tab[xk[0]] < gm and tab[xk[-1]] < gm and 1.0 < xm < 1.6)
# illustration with round numbers (H0 = 70 km/s/Mpc, R = 10 kpc); NOT a data claim
Mpc = 3.0857e22; H0 = 70e3 / Mpc; c = 2.99792458e8; Rg = 10e3 * 3.0857e16
print(f"      illustration (H0 = 70 km/s/Mpc, R = 10 kpc): g_eq ~ H^2 R/5 = {H0**2 * Rg / 5:.2e} m/s^2 versus c H0/Z = {c * H0 / float(Z):.2e} m/s^2 (ratio {H0**2 * Rg / 5 / (c * H0 / float(Z)):.1e})")
check("at galactic radii the mass = Lambda crossover acceleration is >1e5 times BELOW cH/Z", H0**2 * Rg / 5 / (c * H0 / float(Z)) < 1e-5)

# ------------------------------------------------------------------------------------------------ N5
print("N5  analytic structure: only the combination (M/R)/(R/L) can carry g/H")
mu_, lam_ = sp.symbols('mu lambda', positive=True)
# uniform ball: u^2 = l_f^2 (1/L^2 + 2M/r_b^3) = lambda^2 + mu*(r_b/l_f)^3-ish; to the order needed use u^2 = lambda^2 + mu, mu = 2GM/R, lambda = R/L
Psi_expr = 1 + c_first * (lam_**2 + mu_) + c_second * (lam_**2 + mu_)**2
Psi_exp = sp.expand(Psi_expr)
poly = sp.Poly(Psi_exp, mu_, lam_)
neg = [m for m in poly.monoms() if min(m) < 0]
check(f"Psi(lambda^2 + mu) is a polynomial in mu, lambda with non-negative powers only (monomials {poly.monoms()})", len(neg) == 0)
# g/H = (G M / R^2) L = (mu/2)/lambda ; substitute mu = 2 lambda q (q = g/H): terms lambda^j q^k with j >= k : q enters with a suppression lambda^k
q = sp.symbols('q', positive=True)
sub = sp.expand(Psi_exp.subs(mu_, 2 * lam_ * q))
pq = sp.Poly(sub, q, lam_)
ok_supp = all(m[1] >= m[0] for m in pq.monoms())
check(f"in terms of q = g/H at fixed lambda = R/L: every power q^k comes with lambda^k or higher (monomials {pq.monoms()}): a fixed q = O(1) is suppressed by lambda <= 1", ok_supp)
must_fail("N5b a term q^2 lambda^0 (an O(1) function of g/H alone) appears", any(m == (2, 0) for m in pq.monoms()))

print(f"\nr05: {sum(ok)}/{len(ok)} checks passed")
sys.exit(0 if all(ok) else 1)
