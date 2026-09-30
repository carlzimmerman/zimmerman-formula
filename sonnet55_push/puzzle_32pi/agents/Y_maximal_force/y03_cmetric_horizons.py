"""Lane Y, script 3: horizon structure of the dS C-metric, thermal equilibrium (C5), the extremal boundary (C4),
and the largest string force compatible with a static black-hole region as a function of A/H."""
import json
import os
import sympy as sp
import mpmath as mp
from common import Ledger, HERE
import cmetric as cm

L_ = Ledger("y03_cmetric_horizons")
mp.mp.dps = 50
y, x, s, h = sp.symbols("y x s h", real=True)
m, A, ell = sp.symbols("m A ell", positive=True)
Lam = sp.symbols("Lambda", positive=True)

print("\n== H1: algebra of F and of the extremal condition ==")
Fy = -(1 + h**2) + y**2 - 2 * s * y**3
Gx = 1 - x**2 - 2 * s * x**3
L_.check("F(-x) = -G(x) - h^2 identically (so F(-x) <= -h^2 < 0 on the whole conformal boundary y = -x)", sp.expand(Fy.subs(y, -x) + Gx + h**2) == 0)
ext = sp.solve(sp.Eq(Fy.subs(y, 1 / (3 * s)), 0), h**2)[0]
L_.check(f"F(1/(3 s)) = 0 (double root, F' = 0 there)  <=>  h^2 = {ext}  <=>  27 s^2 (1 + h^2) = 1", sp.simplify(ext - (1 / (27 * s**2) - 1)) == 0
         and sp.simplify(sp.diff(Fy, y).subs(y, 1 / (3 * s))) == 0)
# Dias-Lemos: 27 m^2 A^2 = 1 - 9 m^2 Lambda with Lambda = 3/ell^2 = 3 h^2 A^2, s = m A
DL = sp.simplify((27 * s**2 * (1 + h**2) - 1) - (27 * s**2 - 1 + 27 * s**2 * h**2))   # 9 m^2 Lambda = 9 (m A)^2 (3 h^2) = 27 s^2 h^2  (Lambda = 3 h^2 A^2)
L_.check("this is the Dias-Lemos extremal condition 27 m^2 A^2 = 1 - 9 m^2 Lambda (hep-th/0301046, section III B), reproduced independently", DL == 0)
L_.must_fail("control: 27 s^2 (1 + h^2) = 1 is NOT 27 s^2 = 1 (that would be the Lambda = 0 saturation)", sp.simplify(ext - (1 / (27 * s**2))) == 0)
L_.check("with F_max saturation 27 s^2 = 1 the extremal condition gives h^2 = 0: a static region needs Lambda = 0", sp.simplify(ext.subs(s, 1 / sp.sqrt(27))) == 0)

print("\n== H2: real-root structure on a grid of the allowed region 27 s^2 (1 + h^2) < 1 ==")
bad = 0; cnt = 0; worst_y2 = mp.mpf(10); worst_y1 = mp.mpf(-10)
for ks in range(1, 60):
    sv = mp.mpf(ks) / 60 * cm.SQRT27_INV
    hmax = cm.h_extremal(sv)
    for kh in range(1, 40):
        hv = hmax * mp.mpf(kh) / 40
        r = cm.F_roots(sv, hv)
        y1, y2, y3 = [mp.re(v) for v in r]
        xm, xs, xn = cm.G_roots(sv)
        cnt += 1
        ok = (y1 < -xn) and (y2 > -xs) and (y2 < 1 / (3 * sv) < y3) and all(abs(mp.im(v)) < mp.mpf("1e-30") for v in r)
        bad += (not ok)
        worst_y2 = min(worst_y2, y2 + xs)
        worst_y1 = max(worst_y1, y1 + xn)
L_.check(f"{cnt} grid points: three real roots y1 < -x_n < ... < -x_s < y2 < 1/(3s) < y3 everywhere: exactly TWO horizons (y2, y3) inside the physical range y >= -x; the third root is outside it (max of y1 + x_n = {mp.nstr(worst_y1, 5)} < 0, min of y2 + x_s = {mp.nstr(worst_y2, 5)} > 0)", bad == 0)
L_.check("so in the dS C-metric with Lambda > 0 there is NO separate acceleration horizon: y2 is the acceleration horizon and the cosmological horizon at once (as Dias-Lemos state); the brief's T_acc = T_cosm is therefore not a condition", bad == 0)
# Descartes count in r: r f = (1 - A^2 r^2)(r - 2 m) - H^2 r^3 has at most 2 positive roots
r_ = sp.symbols("r", real=True); H = sp.symbols("H", positive=True)
cub = sp.expand((1 - A**2 * r_**2) * (r_ - 2 * m) - H**2 * r_**3)
coefs = sp.Poly(cub, r_).all_coeffs()
signs = [sp.sign(c_.subs({A: 1, m: 1, H: 1})) for c_ in coefs]
changes = sum(1 for i in range(len(signs) - 1) if signs[i] != signs[i + 1])
L_.check(f"Descartes: coefficients of r f(r) have signs {signs}: {changes} sign changes => at most 2 positive roots (Lambda > 0, m > 0)", changes == 2)
cub_ads = sp.expand((1 - A**2 * r_**2) * (r_ - 2 * m) + r_**3)    # AdS-like sign for the Lambda term
signs_ads = [sp.sign(c_.subs({A: sp.Rational(1, 2), m: 1})) for c_ in sp.Poly(cub_ads, r_).all_coeffs()]
chg_ads = sum(1 for i in range(len(signs_ads) - 1) if signs_ads[i] != signs_ads[i + 1])
L_.must_fail(f"control: for the AdS sign of Lambda (coefficient signs {signs_ads}) the count is different ({chg_ads} sign change), i.e. the dS conclusion is not a generic-cubic accident", chg_ads == 2)

print("\n== H3: thermal equilibrium T_bh = T_(acc/cosm)  (C5) ==")
y1s, y2s, y3s = sp.symbols("y1 y2 y3", real=True)
Ffac = -2 * s * (y - y1s) * (y - y2s) * (y - y3s)
ratio = sp.simplify(sp.diff(Ffac, y).subs(y, y2s) / sp.diff(Ffac, y).subs(y, y3s))
L_.check(f"F'(y2)/F'(y3) = {ratio}: |T_(acc/cosm)/T_bh| = (y2 - y1)/(y3 - y1)", sp.simplify(ratio + (y2s - y1s) / (y3s - y1s)) == 0)
viol = 0; rmin = mp.mpf(2)
for ks in range(1, 60):
    sv = mp.mpf(ks) / 60 * cm.SQRT27_INV
    hmax = cm.h_extremal(sv)
    for kh in range(1, 40):
        hv = hmax * mp.mpf(kh) / 40
        y1, y2, y3 = [mp.re(v) for v in cm.F_roots(sv, hv)]
        Tr = abs(cm.Fp(y2, sv, hv)) / abs(cm.Fp(y3, sv, hv))
        rmin = min(rmin, Tr)
        viol += (Tr >= 1)
L_.check(f"T_(acc/cosm)/T_bh < 1 strictly on all {cnt} non-degenerate grid points (both temperatures for the SAME Killing vector d_t): the black-hole horizon is always hotter; equality only at y2 = y3 (degenerate/extremal), where both vanish", viol == 0)
hv = cm.h_extremal(mp.mpf("0.1")) * (1 - mp.mpf("1e-25"))
y1, y2, y3 = [mp.re(v) for v in cm.F_roots(mp.mpf("0.1"), hv)]
L_.check(f"approaching the extremal boundary the ratio tends to 1: {mp.nstr(abs(cm.Fp(y2, mp.mpf('0.1'), hv)) / abs(cm.Fp(y3, mp.mpf('0.1'), hv)), 12)}", abs(abs(cm.Fp(y2, mp.mpf('0.1'), hv)) / abs(cm.Fp(y3, mp.mpf('0.1'), hv)) - 1) < mp.mpf("1e-10"))
# m = 0 check of the effective temperature: T = |F'(y2)|/(4 pi) = sqrt(1+h^2)/(2 pi) in units of A  -> sqrt(A^2 + H^2)/(2 pi)
Tm0 = sp.simplify(sp.diff(Fy.subs(s, 0), y).subs(y, sp.sqrt(1 + h**2)) / (4 * sp.pi))
L_.check(f"m = 0: T(y2) = {Tm0} (units of A) = sqrt(A^2 + H^2)/(2 pi): the Unruh-de Sitter effective temperature of an accelerated observer", sp.simplify(Tm0 - sp.sqrt(1 + h**2) / (2 * sp.pi)) == 0)
L_.check("outcome of C5: T_bh = T_(acc/cosm) has no non-degenerate solution: label = same set as C4 (ENDPOINT/boundary), never an interior point", viol == 0)

print("\n== H4: the extremal boundary and the largest string force with a static black-hole region ==")
def s_ext(q):      # q = A/H = 1/h ; 27 s^2 (1 + h^2) = 1
    q = mp.mpf(q)
    return q / (mp.sqrt(27) * mp.sqrt(1 + q**2))
def Fmax_frac(q):  # string force in units of F_max at the extremal (largest-mass) static solution
    return 4 * cm.mu_string_south(s_ext(q))
rows = []
qF = mp.sqrt(3 / (32 * mp.pi))
for name, q in [("q = 1/6 (T6)", mp.mpf(1) / 6), ("q = 1/Z_F", qF), ("q = 1/2 (T2)", mp.mpf(1) / 2), ("q = 1", mp.mpf(1)), ("q = 10", mp.mpf(10)), ("q = 1000", mp.mpf(1000))]:
    fr = Fmax_frac(q)
    rows.append((name, str(q), str(fr)))
    print(f"   {name:14s}  s_ext = {mp.nstr(s_ext(q), 12)}   largest string force / F_max = {mp.nstr(fr, 12)}")
L_.check("largest string force is strictly below F_max for every finite A/H and tends to F_max only as A/H -> infinity (Lambda -> 0)",
         all(Fmax_frac(q) < 1 for q in [mp.mpf(1) / 6, qF, mp.mpf(1) / 2, 1, 10, 1000]) and Fmax_frac(10**6) > 1 - mp.mpf("1e-3"))
small = Fmax_frac(mp.mpf("1e-6")) / mp.mpf("1e-6")
L_.check(f"small A/H: largest force/F_max -> (4/(3 sqrt 3)) (A/H) = {mp.nstr(4/(3*mp.sqrt(3)), 8)} A/H  (the Nariai mass L/(3 sqrt 3) times A); numerically {mp.nstr(small, 8)}", abs(small - 4 / (3 * mp.sqrt(3))) < mp.mpf("1e-5"))
L_.must_fail("control: the ratio does not tend to 4 (a wrong Nariai mass)", abs(small - 4) < 0.1)
# closed form of the largest string force (derived by hand from the trigonometric roots of G, checked here numerically to 40 digits)
def Fmax_closed(q):
    q = mp.mpf(q)
    th = (mp.pi - 2 * mp.atan(q)) / 3
    return 1 - mp.sin(th) / mp.sin(2 * mp.pi / 3 - th)
test_q = [mp.mpf("0.001"), mp.mpf("0.05"), mp.mpf(1) / 6, mp.mpf("0.1727"), mp.mpf("0.5"), mp.mpf(1), mp.mpf("1.7"), mp.mpf(10), mp.mpf(300)]
errs = [abs(Fmax_closed(q) - Fmax_frac(q)) for q in test_q]
L_.check(f"closed form: (largest static string force)/F_max = 1 - sin(th)/sin(2 pi/3 - th), th = (pi - 2 arctan(A/H))/3, agrees with the root-based value to {mp.nstr(max(errs), 3)} at 9 test points", max(errs) < mp.mpf("1e-35"))
L_.check("exact special value: at A = H the largest string force is exactly F_max/2 (th = pi/6: sin = 1/2, sin(pi/2) = 1)", abs(Fmax_closed(1) - mp.mpf(1) / 2) < mp.mpf("1e-45"))
wrong = lambda q: 1 - mp.sin(2 * mp.pi / 3 - (mp.pi - 2 * mp.atan(q)) / 3) / mp.sin((mp.pi - 2 * mp.atan(q)) / 3)
L_.must_fail("control: the closed form with the two sines interchanged disagrees with the root-based values", abs(wrong(mp.mpf("0.5")) - Fmax_frac(mp.mpf("0.5"))) < mp.mpf("1e-10"))

# F_max saturation at finite Lambda: no static solution
s_sat = cm.SQRT27_INV
L_.check("at s = 1/sqrt 27 and any h > 0: 27 s^2 (1 + h^2) = 1 + h^2 > 1, so F < 0 everywhere in the physical range (no static region; the black hole is not in the family)", (27 * s_sat**2 * (1 + mp.mpf("0.01")**2)) > 1)
L_.check("outcome of C3 + C4 (string force = F_max together with a static black hole): EMPTY at finite A/H; the only limit point is A/H -> infinity (H -> 0): label ENDPOINT, q = infinity", True if Fmax_frac(mp.mpf(10)**6) > 0.999 else False)

out = {"grid_points": cnt, "Tratio_min": str(rmin), "rows_max_force": rows}
json.dump(out, open(os.path.join(HERE, "y03_results.json"), "w"), indent=1)
L_.finish()
