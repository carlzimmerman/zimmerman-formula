#!/usr/bin/env python3
"""r04_scale_candidates.py -- does the exact finite-ball equilibrium define a natural radius/acceleration?  (candidates declared in r00_DECLARATION.md before any of this was run)

Sections
 A  the declared radii X1..X6 (+ two clearly labelled post-hoc extras); X3 has NO solution in the domain x < pi (F_4 never reaches 1/2) -- computed, not assumed
 B  the declared accelerations Q1 (2 pi T_c), Q2 (boundary principal curvature), Q3 (static observer at the boundary), Q5 (mass = Lambda crossover), Q6 (nonlinear threshold g_*),
    in units of H (variable held fixed: L, i.e. Lambda) and of sqrt(G rho_Lambda) (H = sqrt(8 pi/3) sqrt(G rho_Lambda), the Einstein relation the equilibrium itself derives)
 C  structure: dA_V/dL > 0 for every radius (no extremum in Lambda), every acceleration function is a bijection of the radius, so every target is realised at exactly one radius
 D  ONLY NOW the comparison with a0 = H/Z (a0/H = 0.172747; a0/sqrt(G rho_Lambda) = 1/2), with six decoys and a robustness test of the one near-hit
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

mp.mp.dps = 30
SQ = mp.sqrt(8 * mp.pi / 3)          # H = SQ * sqrt(G rho_Lambda)   (c = 1)

def Vof(x): return 2 * mp.pi * (x - mp.sin(x) * mp.cos(x))
def Aof(x): return 4 * mp.pi * mp.sin(x)**2
def I4(x): return 4 * mp.pi / mp.sin(x) * (mp.sin(x)**3 / 3 - mp.cos(x) * (x / 2 - mp.sin(2 * x) / 4))
def F4(x): return I4(x) / (4 * mp.pi * x**4 / 15)
def Aflat_of_V(V): return (36 * mp.pi) ** (mp.mpf(1) / 3) * V ** (mp.mpf(2) / 3)
def g_eq_point(x):        # Q5: point mass at the centre, 8 pi G M xi_c = A_flat(V) - A_dS(V), xi_c = tan(x/2);  returns G M / R^2 in H
    return (Aflat_of_V(Vof(x)) - Aof(x)) / (8 * mp.pi * mp.tan(x / 2)) / x**2
def g_eq_uniform(x):      # robustness variant: uniform-density mass in the ball, weight int xi dV / V
    V = Vof(x)
    return (Aflat_of_V(V) - Aof(x)) * V / (8 * mp.pi * I4(x)) / x**2
def g_eq_vacuum(x):       # robustness variant: M = rho_Lambda V (no entanglement weights)
    return 3 * Vof(x) / (8 * mp.pi * x**2)
def AV(s, V, guess):
    Lc = 1 / mp.sqrt(s)
    xg = mp.findroot(lambda xg: 2 * mp.pi * Lc**3 * (xg - mp.sin(xg) * mp.cos(xg)) - V, guess)
    return 4 * mp.pi * Lc**2 * mp.sin(xg)**2
def g_star(x):            # Q6: second-order term = first-order term of A_V(s), s = L^-2, boundary acceleration G M/r_b^2 (uniform ball), see r05 N3
    V = Vof(x)
    A1 = mp.diff(lambda s: AV(s, V, x), 1, 1); A2 = mp.diff(lambda s: AV(s, V, x), 1, 2)
    return mp.sin(x) * abs(A1 / A2)

# ------------------------------------------------------------------------------------------------ A
print("A  radii")
xx = sp.symbols('x', positive=True)
serA = sp.series(sp.sin(xx)**2 / xx**2, xx, 0, 8).removeO()
serV = sp.series(sp.Rational(3, 2) * (xx - sp.sin(xx) * sp.cos(xx)) / xx**3, xx, 0, 8).removeO()
cA1, cA2 = serA.coeff(xx, 2), serA.coeff(xx, 4)
cV1, cV2 = serV.coeff(xx, 2), serV.coeff(xx, 4)
print(f"   A/A_flat = 1 + ({cA1}) x^2 + ({cA2}) x^4;   V/V_flat = 1 + ({cV1}) x^2 + ({cV2}) x^4")
F4ser = sp.series((4 * sp.pi / sp.sin(xx) * (sp.sin(xx)**3 / 3 - sp.cos(xx) * (xx / 2 - sp.sin(2 * xx) / 4))) / (4 * sp.pi * xx**4 / 15), xx, 0, 8).removeO()
cF1, cF2 = F4ser.coeff(xx, 2), F4ser.coeff(xx, 4)
print(f"   F_4 = 1 + ({cF1}) x^2 + ({cF2}) x^4")
radii = {}
radii["X1 pi/2 (equator)"] = mp.pi / 2
radii["X2 pi/4 (S_ball = S_dS/2)"] = mp.pi / 4
radii["X5 1 (R = L)"] = mp.mpf(1)
radii["X6 sqrt(8pi/3) (R* = c/sqrt(G rho_L); target-aware)"] = SQ
# X3: F_4 = 1/2 -- scan for a root
grid = [mp.mpf(k) / 200 for k in range(2, 627)]          # 0.01 .. 3.13
Fvals = [F4(x) for x in grid]
Fmin = min(Fvals); xFmin = grid[Fvals.index(Fmin)]
check(f"X3: F_4(x) never reaches 1/2 on (0, pi): min F_4 = {mp.nstr(Fmin, 6)} at x = {mp.nstr(xFmin, 4)} (the small-ball formula is never more than {mp.nstr(1 - Fmin, 3)} too big)", Fmin > 0.5)
xFmin_ref = mp.findroot(lambda x: mp.diff(F4, x), xFmin)
radii["X7 x_min of F_4 (POST HOC extra: maximal small-ball failure)"] = xFmin_ref
# F_4 = 1 second crossing (post hoc, structure only)
xF1 = mp.findroot(lambda x: F4(x) - 1, 2.9)
print(f"   (structure) F_4 returns to 1 at x = {mp.nstr(xF1, 6)} and diverges as x -> pi (weight ~ 1/sin x)")
# X4 variants
def xr(c_lead, c_next): return mp.sqrt(abs(mp.mpf(sp.Rational(c_lead)) / mp.mpf(sp.Rational(c_next))))
x4A = xr(cA1, cA2); x4V = xr(cV1, cV2)
x4F_a = mp.sqrt(1 / abs(mp.mpf(sp.Rational(cF1))))       # |c1| x^2 = 1  (next term = leading term 1)
x4F_b = xr(cF1, cF2)                                      # |c2| x^4 = |c1| x^2
print(f"   X4 variants: A-series |c1|x^2 = |c2|x^4 -> x = {mp.nstr(x4A, 6)};  V-series -> {mp.nstr(x4V, 6)};  F_4: |c1| x^2 = 1 -> {mp.nstr(x4F_a, 6)};  F_4: |c2| x^4 = |c1| x^2 -> {mp.nstr(x4F_b, 6)}   (pi = {mp.nstr(mp.pi, 6)})")
check("X4 (A-series) lies inside the domain (x < pi)", x4A < mp.pi)
check("X4 (V-series, my first hand guess was that it lies inside) lies OUTSIDE the domain: V/V_flat = 1 - x^2/5 + (2/105) x^4, radius sqrt(21/2) = 3.24 > pi", x4V > mp.pi)
check("X4 (F_4 variants) both lie OUTSIDE the domain (x > pi): no such radius exists for the equilibrium response function", x4F_a > mp.pi and x4F_b > mp.pi)
radii["X4A sqrt(15/2) (A-series)"] = x4A
for k, v in radii.items():
    print(f"   {k:64s} x = {mp.nstr(v, 10)}  ({mp.nstr(v / mp.pi, 8)} pi)")

# ------------------------------------------------------------------------------------------------ B
print("B  accelerations (units of H = 1/L; second value = a / sqrt(G rho_Lambda) = (a/H) sqrt(8 pi/3))")
Q = {
    "Q1 a_mod=cot(x/2)": lambda x: mp.cot(x / 2),
    "Q2 k1=|cot x|": lambda x: abs(mp.cot(x)),
    "Q3 a_st=|tan x|": lambda x: abs(mp.tan(x)),
    "Q5 g_eq (point mass = Lambda deficit)": g_eq_point,
    "Q6 g_* (nonlinear threshold)": g_star,
}
table = {}
hdr = "   {:64s}".format("radius") + "".join(f"{k[:16]:>18s}" for k in Q)
print(hdr)
for rk, xv in radii.items():
    row = {}
    for qk, qf in Q.items():
        try:
            v = qf(xv)
            if not mp.isfinite(v) or v > 1e6: v = mp.inf
        except Exception:
            v = mp.nan
        row[qk] = v
    table[rk] = row
    print("   {:64s}".format(rk[:64]) + "".join(f"{mp.nstr(row[qk], 6):>18s}" for qk in Q))
print("   in units of sqrt(G rho_Lambda) multiply every entry by sqrt(8 pi/3) =", mp.nstr(SQ, 8))
# exact forms at the rational-pi radii
x_ = sp.symbols('x')
ex = {}
for lbl, xv in (("pi/2", sp.pi / 2), ("pi/4", sp.pi / 4)):
    ex[lbl] = (sp.nsimplify(sp.cot(xv / 2)), sp.nsimplify(sp.cot(xv)), sp.nsimplify(sp.tan(xv)) if lbl != "pi/2" else sp.zoo)
print("   exact forms: Q1(pi/2) =", ex["pi/2"][0], "; Q2(pi/2) =", ex["pi/2"][1], "; Q3(pi/2) = infinite;  Q1(pi/4) =", sp.simplify(ex["pi/4"][0]), "; Q2(pi/4) =", ex["pi/4"][1], "; Q3(pi/4) =", ex["pi/4"][2])
check("at the equator the modular acceleration is exactly H (T_c = T_dS) and the boundary curvature vanishes", ex["pi/2"][0] == 1 and ex["pi/2"][1] == 0)
check("pi-content: at rational-pi radii the accelerations are algebraic in H (1, 1+sqrt2, ...); in sqrt(G rho_L) units they are (algebraic) x sqrt(8 pi/3) -- the pi is exactly the Einstein 8 pi the equilibrium derives",
      sp.simplify(ex["pi/4"][0] - (1 + sp.sqrt(2))) == 0)
print("   (radii that are not rational multiples of pi, e.g. x = 1, sqrt(8 pi/3), sqrt(15/2): trig of a nonzero algebraic argument is transcendental by Lindemann-Weierstrass (imported theorem, not scripted); the roots x_min, x4V, g_* thresholds have no closed form)")

# ------------------------------------------------------------------------------------------------ C
print("C  structure")
f_ = sp.sin(xx) * (2 + sp.cos(xx)**2) - 3 * xx * sp.cos(xx)
check("d/dx [sin x (2 + cos^2 x) - 3 x cos x] = 3 sin x (x - sin x cos x) identically",
      sp.simplify(sp.diff(f_, xx) - 3 * sp.sin(xx) * (xx - sp.sin(xx) * sp.cos(xx))) == 0)
check("x - sin x cos x > 0 and sin x > 0 on (0, pi), f(0) = 0  =>  f > 0: dA_V/dL = 4 pi L f(x)/sin x > 0 for EVERY radius (fixed-V area strictly increases with L: no stationary point in Lambda)",
      sp.simplify(f_.subs(xx, 0)) == 0 and all(float((mp.mpf(k) / 100) - mp.sin(mp.mpf(k) / 100) * mp.cos(mp.mpf(k) / 100)) > 0 for k in range(1, 314)))
# dA/dL|_V against direct differentiation of the closed forms
L_ = sp.symbols('L', positive=True); xs_ = sp.symbols('xs', positive=True)
Vexpr = 2 * sp.pi * L_**3 * (xs_ - sp.sin(xs_) * sp.cos(xs_))
dxdL = -sp.diff(Vexpr, L_) / sp.diff(Vexpr, xs_)
dAdL = sp.diff(4 * sp.pi * L_**2 * sp.sin(xs_)**2, L_) + sp.diff(4 * sp.pi * L_**2 * sp.sin(xs_)**2, xs_) * dxdL
check("dA/dL|_V = 4 pi L f(x)/sin(x) (closed-form derivative reproduces it)", sp.simplify(dAdL - 4 * sp.pi * L_ * (sp.sin(xs_) * (2 + sp.cos(xs_)**2) - 3 * xs_ * sp.cos(xs_)) / sp.sin(xs_)) == 0)
must_fail("C2b dA_V/dL changes sign somewhere on (0,pi) (a Lambda-selecting extremum)", any(float(mp.sin(mp.mpf(k) / 100) * (2 + mp.cos(mp.mpf(k) / 100)**2) - 3 * (mp.mpf(k) / 100) * mp.cos(mp.mpf(k) / 100)) <= 0 for k in range(1, 314)))
# bijections: Q1, Q2 strictly monotone on (0,pi) -> every target a is realised at exactly one radius
t = sp.symbols('t', positive=True)
check("Q1 = cot(x/2): strictly decreasing bijection (0,pi) -> (infinity, 0);  inverse x = 2 arctan(H/a)", sp.simplify(sp.diff(sp.cot(xx / 2), xx)) != 0 and sp.simplify(sp.cot(2 * sp.atan(1 / t) / 2) - t) == 0)
check("Q2 = cot(x): strictly decreasing bijection (0,pi) -> R;  inverse x = arctan(H/a) (for a > 0, radius below the equator)", sp.simplify(sp.cot(sp.atan(1 / t)) - t) == 0)
print("   => for ANY target acceleration there is exactly one radius (per function) realising it; the equilibrium therefore selects no acceleration by itself")

# ------------------------------------------------------------------------------------------------ D
print("D  COMPARISON WITH a0 (only now)")
Z = mp.sqrt(32 * mp.pi / 3)
target = 1 / Z
print(f"   a0/H = 1/Z = {mp.nstr(target, 10)};  a0/sqrt(G rho_Lambda) = 1/2 (same condition: c2 = c1 sqrt(8 pi/3))")
menu = {}
for rk, row in table.items():
    for qk, v in row.items():
        if mp.isfinite(v) and v > 0:
            menu[(rk.split()[0], qk.split()[0])] = v
sup_pt = mp.findroot(lambda xg: mp.diff(g_eq_point, xg), 1.3)
menu[("sup", "Q5 g_eq")] = g_eq_point(sup_pt)
print(f"   menu size = {len(menu)} numbers (finite, positive), from the declared radii/accelerations plus two POST HOC additions (radius X7 and the supremum of Q5, both added after seeing numbers)")
def hits(tgt, tol):
    return [(k, float(v / tgt - 1)) for k, v in menu.items() if abs(v / tgt - 1) < tol]
for tol in (0.02, 0.06):
    h = hits(target, tol)
    print(f"   hits of 1/Z within {tol:.0%}: {len(h)}  {h}")
h2 = hits(target, 0.02)
check("no declared candidate reproduces 1/Z within 2%", len(h2) == 0)
# detector control: a target planted at 1.005 x (a menu value) MUST be found by the same hit counter
plant = menu[("X2", "Q1")] * mp.mpf("1.005")
must_fail("hit detector fails to find a planted target (menu value x 1.005, 2% window)", len(hits(plant, 0.02)) == 0)
h6 = hits(target, 0.06)
print("   candidates within 6%:", h6)
decoys = {"Z'=5": 1 / mp.mpf(5), "Z'=5.5": 1 / mp.mpf('5.5'), "Z'=6": 1 / mp.mpf(6), "Z'=2pi": 1 / (2 * mp.pi), "Z'=6.5": 1 / mp.mpf('6.5'), "Z'=1.05Z": 1 / (mp.mpf('1.05') * Z), "forced kernel 1/sqrt(8pi/3)": 1 / SQ}
for k, dv in decoys.items():
    print(f"   decoy {k:30s} target {mp.nstr(dv, 6)}: hits within 2%: {len(hits(dv, 0.02))}, within 6%: {len(hits(dv, 0.06))}")
n_dec6 = sum(len(hits(dv, 0.06)) > 0 for dv in decoys.values())
print(f"   decoys with at least one 6%-hit: {n_dec6}/{len(decoys)};  the true target has {len(h6)} 6%-hits")
check("a 6% proximity is not discriminating: at least 3 of the 7 decoy targets also have a 6%-hit", n_dec6 >= 3)
# robustness of the one near-hit: sup of Q5 under alternative reasonable definitions
print("   robustness of the near-hit (sup over x of the mass = Lambda crossover, G M/R^2 in units of H):")
supv = {}
for nm, fn, g0 in (("point mass at centre (declared Q5)", g_eq_point, 1.3), ("uniform-density mass, weight <xi>", g_eq_uniform, 1.25), ("M = rho_Lambda V (no weights)", g_eq_vacuum, 1.55)):
    xm = mp.findroot(lambda xg: mp.diff(fn, xg), g0)
    supv[nm] = fn(xm)
    print(f"     {nm:40s} sup = {mp.nstr(supv[nm], 8)} at x = {mp.nstr(xm, 5)};  sup/(1/Z) = {mp.nstr(supv[nm] / target, 6)}")
vals = list(supv.values())
check("the near-hit is definition-dependent: alternative equally reasonable definitions of the crossover give suprema differing by a factor > 2", max(vals) / min(vals) > 2)
# what the target would require at each function (radius that realises 1/Z)
x1 = 2 * mp.atan(Z); x2 = mp.atan(Z)
print(f"   radius needed for a0: Q1 (a_mod = H/Z): x = 2 arctan(Z) = {mp.nstr(x1, 8)} ({mp.nstr(x1 / mp.pi, 6)} pi; area fraction sin^2 x = {mp.nstr(mp.sin(x1)**2, 6)}, volume fraction V/Vol(S^3) = {mp.nstr(Vof(x1) / (2 * mp.pi**2), 6)});  Q2 (k1 = H/Z): x = arctan(Z) = {mp.nstr(x2, 8)} ({mp.nstr(x2 / mp.pi, 6)} pi)")
nat = [mp.pi / 2, mp.pi / 4, mp.mpf(1), SQ, x4A]
for lbl, xv in (("Q1", x1), ("Q2", x2)):
    d = min(abs(xv / n - 1) for n in nat)
    print(f"     {lbl}: relative distance of the required radius to the nearest declared radius: {float(d):.3f}")
# NOTE: proximity in RADIUS is uninformative near x -> pi (Q1 = cot(x/2) is steep there): the required radius 2.7995 is within 2.2% of X4A = 2.7386 but the
# ACCELERATIONS differ by 18% (Q1(X4A) = 0.2043 vs 1/Z = 0.1727).  The criterion used above is on the acceleration.
qa = mp.cot(x4A / 2)
check(f"Q1 at the nearest radius (X4A) is {mp.nstr(qa, 5)} H, {float(abs(qa / target - 1)):.1%} away from 1/Z: a 2% radius proximity is an 18% acceleration miss", abs(qa / target - 1) > 0.1)
print("   c2 table (a / sqrt(G rho_Lambda)); the target is 1/2:")
for rk, row in table.items():
    print("   {:64s}".format(rk[:64]) + "".join(f"{mp.nstr(row[qk] * SQ, 6):>18s}" for qk in Q))

print(f"\nr04: {sum(ok)}/{len(ok)} checks passed")
sys.exit(0 if all(ok) else 1)
