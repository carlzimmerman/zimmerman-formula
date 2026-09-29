#!/usr/bin/env python3
"""l03_pi_count_transcendence.py -- E8: the pi-count statement for the SdS family, made exact, in BOTH variable choices (hold Lambda fixed / hold G rho_Lambda fixed).

Notation (c = G = 1, L = 1/H):  x = r_b/L, K = kappa_b/H = (1 - 3 x^2)/(2 x),  mu = M/M_N = (3 sqrt3/2) x (1 - x^2),  m = mu^2.
u = sqrt(G rho_Lambda) (an inverse length),  Lambda = 8 pi u^2,  H^2 = Lambda/3,  c_rec := kappa/u  (this is the record's 'kappa' coefficient: a0 = c_rec * sqrt(G rho_Lambda), c_rec = 1/2 fitted).

What is PROVED here (exact algebra, sympy) and what is IMPORTED (textbook theorem, not a computation):
  A. K_b is a strictly decreasing bijection of mu in (0,1) onto (0, infinity) (so the family has no preferred interior point and the relation kappa_b = c u has exactly one solution for EVERY c > 0).
  B. Elimination: K and m obey a polynomial relation P(K, m) = 0 with INTEGER coefficients.  Hence  mu algebraic  =>  K algebraic  (and conversely at fixed algebraic K, mu algebraic).
  C. K/c_rec = H/u = sqrt(8 pi/3) exactly.  So at any single point of the family K and c_rec cannot both be algebraic (unless zero): a point selected by an ALGEBRAIC condition in geometry (Lambda) units has c_rec in sqrt(pi) x algebraic; the puzzle needs c_rec = 1/2 (rational), which forces K = sqrt(3/(32 pi)) and mu transcendental.
     IMPORTED: Lindemann 1882 (pi is transcendental) => sqrt(3/(32 pi)) is transcendental.  A numerical PSLQ/findpoly check below is a HEURISTIC illustration only, not the proof.
  D. Einstein-dictionary cancellation: any mass built as rho_Lambda x (4 pi/3) R^3 with R = r L (r algebraic) gives M/M_N algebraic (the 8 pi of rho_Lambda = Lambda/8 pi cancels the 4 pi of the volume).
  E. Consequence table: c_rec at the points selected by the principles E1, E3, E5 -- all are sqrt(pi) x algebraic, none is 1/2.
Controls: (i) the elimination polynomial vanishes on the actual family (5 masses) and NOT on a perturbed K; (ii) findpoly recovers the low-degree polynomial of K at the rational mass mu = 1/2 (algebraic), and of K' built with pi replaced by 22/7
(a deliberately algebraic 'pi'), but finds none for the true 1/Z (heuristic); (iii) c_rec = 1/2 is recovered exactly at the a0-point.
Exit 0 iff all checks hold.
"""
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 60
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def mut(name, wrong):
    ok.append(not bool(wrong)); print(("PASS [mutation rejected] " if not wrong else "FAIL [mutation NOT rejected] ") + name)

x, K, m = sp.symbols('x K m', positive=True)
Kx = (1 - 3 * x**2) / (2 * x)
mux = 3 * sp.sqrt(3) * x * (1 - x**2) / 2
# A. bijection
dK = sp.simplify(sp.diff(Kx, x)); dmu = sp.simplify(sp.diff(mux, x))
chk("A1 dK/dx = -(3/2) - 1/(2 x^2) < 0 for all x > 0 (exact) and dmu/dx = (3 sqrt3/2)(1 - 3 x^2) > 0 on (0, 1/sqrt3): K_b is a strictly DEcreasing bijection of mu in (0,1) onto (0, infinity)",
    sp.simplify(dK - (-sp.Rational(3, 2) - 1 / (2 * x**2))) == 0 and sp.simplify(dmu - 3 * sp.sqrt(3) / 2 * (1 - 3 * x**2)) == 0 and sp.limit(Kx, x, 0, '+') == sp.oo and sp.simplify(Kx.subs(x, 1 / sp.sqrt(3))) == 0)
# kappa_c: K_c = (3 y - 1/y)/2 increasing in y, y decreasing in mu
y = sp.symbols('y', positive=True)
Kc = (3 * y**2 - 1) / (2 * y)
muy = 3 * sp.sqrt(3) * y * (1 - y**2) / 2
chk("A2 K_c = (3 y^2 - 1)/(2y) has dK_c/dy = 3/2 + 1/(2 y^2) > 0 and dmu/dy = (3 sqrt3/2)(1 - 3y^2) < 0 for y in (1/sqrt3, 1): K_c is a strictly decreasing bijection of mu in (0,1) onto (0, 1) (= H at M = 0): a0/H = 0.1727 is reached at ONE mass on each horizon",
    sp.simplify(sp.diff(Kc, y) - (sp.Rational(3, 2) + 1 / (2 * y**2))) == 0 and sp.simplify(sp.diff(muy, y) - 3 * sp.sqrt(3) / 2 * (1 - 3 * y**2)) == 0 and sp.simplify(Kc.subs(y, 1)) == 1)

# B. elimination
q1 = 3 * x**2 + 2 * K * x - 1                                   # K = (1-3x^2)/(2x)
q2 = 27 * x**2 * (1 - x**2)**2 - 4 * m                          # mu^2 = (27/4) x^2 (1-x^2)^2
P = sp.factor(sp.resultant(q1, q2, x))
print("   elimination polynomial P(K, m) = ", P)
chk("B1 resultant P(K, m) has integer coefficients (K = kappa_b/H, m = (M/M_N)^2)", all(c.is_integer for c in sp.Poly(sp.expand(P), K, m).coeffs()))
Pp = sp.Poly(sp.expand(P), K, m)
def MU_of_x(xv): return 3 * mp.sqrt(3) * xv * (1 - xv**2) / 2
worst = 0
for xv in ['0.03', '0.2', '0.4', '0.52', '0.57']:
    xv = mp.mpf(xv); Kv = (1 - 3 * xv**2) / (2 * xv); mv = MU_of_x(xv)**2
    val = sp.lambdify((K, m), sp.expand(P), 'mpmath')(Kv, mv)
    worst = max(worst, abs(val))
chk("B2 P(K_b(x), mu(x)^2) = 0 on the actual family at 5 masses (max |P| = %s)" % mp.nstr(worst, 3), worst < mp.mpf('1e-40'))
Kv = (1 - 3 * mp.mpf('0.4')**2) / (2 * mp.mpf('0.4')); mv = MU_of_x(mp.mpf('0.4'))**2
mut("B3 mutation: P(1.001 K, m) != 0 (P is not vacuous)", abs(sp.lambdify((K, m), sp.expand(P), 'mpmath')(Kv * mp.mpf('1.001'), mv)) < mp.mpf('1e-30'))
# control: rational mass mu = 1/2 -> K algebraic (a root of an integer polynomial)
Pm = sp.Poly(sp.expand(P.subs(m, sp.Rational(1, 4))), K)
xr = mp.findroot(lambda xv: MU_of_x(xv) - mp.mpf(1) / 2, mp.mpf('0.3'))
Kr = (1 - 3 * xr**2) / (2 * xr)
chk("B4 at the RATIONAL mass mu = 1/2 the value K_b = %s is a root of the integer polynomial %s (algebraic, as B/A imply)" % (mp.nstr(Kr, 12), Pm.as_expr()), abs(sp.lambdify(K, Pm.as_expr(), 'mpmath')(Kr)) < mp.mpf('1e-40'))
fp = mp.findpoly(Kr, 6, maxcoeff=10**6, tol=mp.mpf('1e-40'), maxsteps=100000)
chk("B5 control for the heuristic: mp.findpoly recovers a degree <= 6 integer polynomial for the algebraic K_b(mu=1/2) (found %s)" % (fp,), fp is not None)

# C. c_rec = K sqrt(8pi/3)
Lam, u, Hh, kap = sp.symbols('Lambda u H kappa', positive=True)
subs = {Lam: 8 * sp.pi * u**2}
chk("C1 H/u = sqrt(Lambda/3)/u with Lambda = 8 pi u^2 (u^2 = G rho_Lambda) equals sqrt(8 pi/3) exactly; so c_rec = kappa/u = K sqrt(8 pi/3)", sp.simplify(sp.sqrt(Lam / 3).subs(subs) / u - sp.sqrt(8 * sp.pi / 3)) == 0)
Z = mp.sqrt(32 * mp.pi / 3)
xs = (mp.sqrt(1 + 3 * Z**2) - 1) / (3 * Z)
Ka0 = (1 - 3 * xs**2) / (2 * xs)
c_a0 = Ka0 * mp.sqrt(8 * mp.pi / 3)
chk("C2 (control) at the a0-point K = 1/Z and c_rec = 1/2 exactly (c_rec = %s)" % mp.nstr(c_a0, 25), abs(c_a0 - mp.mpf(1) / 2) < mp.mpf('1e-50'))
# heuristic integer-relation search.  A first run at 60 digits / tolerance 1e-40 returned SPURIOUS degree-8 'polynomials' for 1/Z (coefficients ~3e5): 9 coefficients of size 1e6 carry ~57 digits of freedom,
# more than the 40 digits demanded.  Rule used now: digits_demanded (100) >> (deg+1) log10(maxcoeff) (<= 57).
with mp.workdps(160):
    Zh = mp.sqrt(32 * mp.pi / 3)
    Zt = mp.sqrt(32 * mp.mpf(22) / 7 / 3)     # 'pi' -> 22/7: algebraic
    fp_alg = mp.findpoly(1 / Zt, 4, maxcoeff=10**6, tol=mp.mpf('1e-100'), maxsteps=100000)
    fp_true = mp.findpoly(1 / Zh, 8, maxcoeff=10**6, tol=mp.mpf('1e-100'), maxsteps=100000)
    fp_c2 = mp.findpoly(1 / Zh**2, 8, maxcoeff=10**6, tol=mp.mpf('1e-100'), maxsteps=100000)
    fp_spur = mp.findpoly(1 / Zh, 8, maxcoeff=10**6, tol=mp.mpf('1e-40'), maxsteps=100000)
chk("C3 heuristic only (NOT the proof): at 160 digits / tolerance 1e-100, findpoly (deg <= 8, coeff <= 1e6) finds a polynomial for 1/Z' with pi -> 22/7 (algebraic; found %s) and NONE for the true 1/Z = sqrt(3/(32 pi)) (found %s); the proof is Lindemann: pi transcendental" % (fp_alg, fp_true), fp_alg is not None and fp_true is None)
chk("C4 heuristic: 1/Z^2 = 3/(32 pi) has no integer polynomial of degree <= 8, coeff <= 1e6 at tolerance 1e-100 (found %s)" % (fp_c2,), fp_c2 is None)
chk("C5 calibration of the heuristic's false-positive rate: at the too-loose tolerance 1e-40 the same search DOES return a spurious polynomial for 1/Z (%s), so tolerance 1e-100 is the meaningful one" % (fp_spur,), fp_spur is not None)

# C6. hold G rho_Lambda fixed: lengths in units of 1/a0 (u = 2 a0).  At the a0-point every SdS quantity except kappa_b/u is a non-constant algebraic function of K (L u = 2K there), hence transcendental
with mp.workdps(160):
    Zh = mp.sqrt(32 * mp.pi / 3); a0h = 1 / Zh                               # H = 1
    xh = (mp.sqrt(1 + 3 * Zh**2) - 1) / (3 * Zh); yh = (-xh + mp.sqrt(4 - 3 * xh**2)) / 2
    Mh = xh * yh * (xh + yh) / 2
    kbh = (1 - 3 * xh**2) / (2 * xh); kch = (3 * yh**2 - 1) / (2 * yh)
    ua0 = 1 / a0h                                                           # 1/a0 in units of L
    q_a0 = {'kappa_b/a0': kbh / a0h, 'kappa_c/a0': kch / a0h, 'r_b a0': xh * a0h, 'r_c a0': yh * a0h, 'M a0': Mh * a0h, '(4 pi r_b^2) a0^2': 4 * mp.pi * (xh * a0h)**2, 'L a0': a0h}
    closed_rb = (mp.sqrt(1 + 32 * mp.pi) - 1) / (32 * mp.pi)
    found = {k: mp.findpoly(v, 8, maxcoeff=10**6, tol=mp.mpf('1e-100'), maxsteps=100000) for k, v in q_a0.items()}
    rb_ok = abs(q_a0['r_b a0'] - closed_rb) < mp.mpf('1e-150')
print("   a0-units (G rho_Lambda = 4 a0^2 fixed): r_b a0 = (sqrt(1 + 32 pi) - 1)/(32 pi) = %s ;  L a0 = sqrt(3/(32 pi)) = %s" % (mp.nstr(q_a0['r_b a0'], 12), mp.nstr(q_a0['L a0'], 12)))
for k, v in found.items(): print("     %-20s algebraic (deg<=8, coeff<=1e6, 100 digits)? %s" % (k, 'YES ' + str(v) if v is not None else 'no'))
chk("C6 in units of 1/a0 (G rho_Lambda fixed) the a0-point has kappa_b/a0 = 1 (rational: the puzzle's input) and r_b a0 = (sqrt(1+32 pi) - 1)/(32 pi) exactly; every OTHER quantity (kappa_c/a0, r_c a0, M a0, area a0^2, L a0) is non-algebraic at 100-digit heuristic level (theorem: non-constant algebraic functions of 1/Z). Holding G rho fixed moves pi into L and r, it does not make the geometry produce the rational coefficient",
    rb_ok and abs(q_a0['kappa_b/a0'] - 1) < mp.mpf('1e-150') and all(found[k] is None for k in found if k != 'kappa_b/a0') and found['kappa_b/a0'] is not None)

# D. Einstein-dictionary cancellation
Rr, Ls, rr = sp.symbols('R L r', positive=True)
rho_L = 3 / (8 * sp.pi * Ls**2)                       # rho_Lambda = Lambda/(8 pi), Lambda = 3/L^2
Mv = sp.Rational(4, 3) * sp.pi * rho_L * (rr * Ls)**3
mu_v = sp.simplify(3 * sp.sqrt(3) * Mv / Ls)
chk("D1 M = (4 pi/3) rho_Lambda R^3 with R = r L equals r^3 L/2 (pi cancels): mu = (3 sqrt3/2) r^3, algebraic for algebraic r -> any 'horizon-sized vacuum mass' selects an ALGEBRAIC point", sp.simplify(mu_v - 3 * sp.sqrt(3) / 2 * rr**3) == 0)

# E. c_rec table at the points selected by E1, E3, E5 (K values from l02)
print("   c_rec = kappa/sqrt(G rho_Lambda) at the selected points (a0 needs c_rec = 1/2):")
tab = {
    'dS horizon (M=0), kappa_c = H (the record\'s kappa=1 forced kernel)': mp.mpf(1),
    'E3 Smarr half-and-half: K_b = 1/sqrt5': 1 / mp.sqrt(5),
    'E5a flat-space T(M_N) matching: a = sqrt(11)/4 H': mp.sqrt(11) / 4,
    'E5c Nariai BH-norm: kappa = sqrt3 H (a = sqrt2 H)': mp.sqrt(3),
    'E1 Nariai f-norm: kappa = 0': mp.mpf(0),
}
allbad = True
for name, Kv_ in tab.items():
    cv = Kv_ * mp.sqrt(8 * mp.pi / 3)
    print("     %-72s K = %-12s c_rec = %s" % (name, mp.nstr(Kv_, 8), mp.nstr(cv, 8)))
    if Kv_ != 0:
        allbad &= abs(cv - mp.mpf(1) / 2) > mp.mpf('1e-3')
chk("T1 none of these c_rec equals 1/2 (each is (algebraic) x sqrt(8 pi/3), i.e. sqrt(pi) x algebraic, hence never rational)", allbad)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
