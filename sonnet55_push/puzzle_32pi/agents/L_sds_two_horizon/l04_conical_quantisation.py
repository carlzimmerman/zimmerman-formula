#!/usr/bin/env python3
"""l04_conical_quantisation.py -- E6: Euclidean regularity with a conical singularity at one horizon, Int E4 = 64 pi^2 (1 + kappa_c/kappa_b), and integer / orbifold quantisation.

Independent of a08: (i) E4 is derived from the SIX ORTHONORMAL SECTIONAL CURVATURES of a metric  -f dt^2 + dr^2/f + r^2 dOmega^2  (curvature operator is diagonal:
K_tr = -f''/2, K_ttheta = K_tphi = K_rtheta = K_rphi = -f'/(2r), K_thetaphi = (1-f)/r^2), not by a brute-force coordinate Riemann computation;
(ii) the integral is done by numerical quadrature of E4 r^2 dr, not from the closed antiderivative; (iii) the cone formula is then compared to it.
Readings:  A  beta = 2 pi/kappa_b (smooth at the black hole, cone DEFICIT at the cosmological horizon, angle 2 pi kappa_c/kappa_b < 2 pi):  Int E4 = 64 pi^2 (1 + kappa_c/kappa_b)
           B  beta = 2 pi/kappa_c (smooth at the cosmological horizon, cone EXCESS at the black hole, angle 2 pi kappa_b/kappa_c > 2 pi):  Int E4 = 64 pi^2 (1 + kappa_b/kappa_c)
Quantisation candidates (predeclared E6): Int E4 = 32 pi^2 n (n integer); orbifold cone angle 2 pi/N.
Exit 0 iff every check holds.
"""
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def mut(name, wrong):
    ok.append(not bool(wrong)); print(("PASS [mutation rejected] " if not wrong else "FAIL [mutation NOT rejected] ") + name)

Z = mp.sqrt(32 * mp.pi / 3); TARGET = 1 / Z; MN = 1 / (3 * mp.sqrt(3))
def y_of(x): return (-x + mp.sqrt(4 - 3 * x**2)) / 2
def M_of(x): return x * (1 - x**2) / 2
def mu_of(x): return 3 * mp.sqrt(3) * M_of(x)
def kb(x): return (1 - 3 * x**2) / (2 * x)
def kc(y): return (3 * y**2 - 1) / (2 * y)
xN = 1 / mp.sqrt(3)

# ---------------------------------------------------------------- Q1 E4 from sectional curvatures
r, M, L = sp.symbols('r M L', positive=True)
f = 1 - 2 * M / r - r**2 / L**2
fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
K_tr = -fpp / 2; K_t_ang = -fp / (2 * r); K_r_ang = -fp / (2 * r); K_ang = (1 - f) / r**2
# planes: (t r), (t th), (t ph), (r th), (r ph), (th ph)
Ks = {('t', 'r'): K_tr, ('t', 'th'): K_t_ang, ('t', 'ph'): K_t_ang, ('r', 'th'): K_r_ang, ('r', 'ph'): K_r_ang, ('th', 'ph'): K_ang}
idx = ['t', 'r', 'th', 'ph']
def Kpair(a, b): return Ks.get((a, b), Ks.get((b, a)))
Ric = {a: sum(Kpair(a, b) for b in idx if b != a) for a in idx}
Rs = sum(Ric.values())
Riem2 = 4 * sum(K**2 for K in Ks.values())
Ric2 = sum(v**2 for v in Ric.values())
E4 = sp.simplify(Riem2 - 4 * Ric2 + Rs**2)
chk("Q1a E4(SdS) = 24/L^4 + 48 M^2/r^6 from the six orthonormal sectional curvatures (independent of a08's coordinate computation); Ricci = 3/L^2 g (Einstein space) and R = 12/L^2",
    sp.simplify(E4 - (24 / L**4 + 48 * M**2 / r**6)) == 0 and all(sp.simplify(v - 3 / L**2) == 0 for v in Ric.values()) and sp.simplify(Rs - 12 / L**2) == 0)
mut("Q1b mutation: dropping the M^2 term would give 24/L^4 (Nariai/dS value): rejected", sp.simplify(E4 - 24 / L**4) == 0)

# ---------------------------------------------------------------- Q2 conical Gauss-Bonnet integral by quadrature
def I_smooth(x, beta):
    y = y_of(x); Mv = M_of(x)
    integrand = lambda rr: (24 + 48 * Mv**2 / rr**6) * rr**2
    return 4 * mp.pi * beta * mp.quad(integrand, [x, y])
worst_A = worst_B = 0
rows = []
for xv in ['0.05', '0.2', '0.35', '0.45', '0.52', '0.57']:
    xv = mp.mpf(xv); y = y_of(xv)
    A = I_smooth(xv, 2 * mp.pi / kb(xv)); B = I_smooth(xv, 2 * mp.pi / kc(y))
    fA = 64 * mp.pi**2 * (1 + kc(y) / kb(xv)); fB = 64 * mp.pi**2 * (1 + kb(xv) / kc(y))
    worst_A = max(worst_A, abs(A - fA)); worst_B = max(worst_B, abs(B - fB))
    rows.append((mu_of(xv), kc(y) / kb(xv), A / (32 * mp.pi**2), B / (32 * mp.pi**2)))
print("   mu       kappa_c/kappa_b    n_A = IntE4/(32 pi^2), reading A    n_B, reading B")
for mu, rho, nA, nB in rows: print("   %.4f   %.6f          %.6f                       %.6f" % (float(mu), float(rho), float(nA), float(nB)))
chk("Q2a numerical quadrature of E4 reproduces Int E4 = 64 pi^2 (1 + kappa_c/kappa_b) (reading A, max |diff| = %s) and 64 pi^2 (1 + kappa_b/kappa_c) (reading B, max |diff| = %s)" % (mp.nstr(worst_A, 3), mp.nstr(worst_B, 3)), worst_A < mp.mpf('1e-25') and worst_B < mp.mpf('1e-25'))
xb_ = mp.mpf('0.2'); yb_ = y_of(xb_)
mut("Q2b mutation: 64 pi^2 (1 + kappa_b/kappa_c) does NOT reproduce reading A at x = 0.2", abs(I_smooth(xb_, 2 * mp.pi / kb(xb_)) - 64 * mp.pi**2 * (1 + kb(xb_) / kc(yb_))) < mp.mpf('1e-10'))
# endpoints
x_small = mp.mpf('1e-9'); x_near = xN - mp.mpf('1e-9')
chk("Q2c endpoints: M -> 0 gives Int E4 -> 64 pi^2 (n = 2 = chi(S^4) with 32 pi^2 chi/..: pure dS), Nariai gives 128 pi^2 (n = 4, chi(S^2 x S^2) = 4)",
    abs(I_smooth(x_small, 2 * mp.pi / kb(x_small)) / (32 * mp.pi**2) - 2) < 1e-6 and abs(I_smooth(x_near, 2 * mp.pi / kb(x_near)) / (32 * mp.pi**2) - 4) < 1e-6)

# ---------------------------------------------------------------- Q3 allowed ratios
def rho_of(x): return kc(y_of(x)) / kb(x)          # kappa_c / kappa_b in (0,1), increasing in x
def x_from_rho(rho):
    return mp.findroot(lambda x: rho_of(x) - rho, (mp.mpf('1e-4'), xN - mp.mpf('1e-14')), solver='anderson', tol=1e-35, maxsteps=200)
print("\n   Reading A: n = 2 (1 + rho), rho = kappa_c/kappa_b in (0,1)  =>  integer n only n = 3 (rho = 1/2); n = 2 and n = 4 are the endpoints")
xA = x_from_rho(mp.mpf(1) / 2)
yA = y_of(xA)
print("   n = 3: x = %s  mu = %s   K_b = %s   K_c = %s" % (mp.nstr(xA, 10), mp.nstr(mu_of(xA), 10), mp.nstr(kb(xA), 10), mp.nstr(kc(yA), 10)))
chk("Q3a reading A has exactly ONE interior integer: n = 3, kappa_c/kappa_b = 1/2, at mu = %s with K_b = %s (n = 2 and 4 are the pure-dS and Nariai endpoints)" % (mp.nstr(mu_of(xA), 8), mp.nstr(kb(xA), 8)),
    abs(rho_of(xA) - mp.mpf(1) / 2) < 1e-30 and all(2 < 2 * (1 + rho_of(mp.mpf(v))) < 4 for v in ['0.01', '0.2', '0.4', '0.55', '0.577']))
chk("Q3b that point is not the a0 point: K_b = %s vs 1/Z = %s (ratio %s)" % (mp.nstr(kb(xA), 8), mp.nstr(TARGET, 8), mp.nstr(kb(xA) / TARGET, 6)), abs(kb(xA) / TARGET - 1) > mp.mpf('0.1'))
# reading B: kappa_b/kappa_c = n/2 - 1 >= 1 ; n = 5, 6, ...
print("   Reading B: n = 2 (1 + kappa_b/kappa_c) in (4, inf): every integer n >= 5 allowed, kappa_b/kappa_c = n/2 - 1")
rowsB = []
for n in range(5, 13):
    target = mp.mpf(n) / 2 - 1
    xn = mp.findroot(lambda x: 1 / rho_of(x) - target, (mp.mpf('1e-3'), xN - mp.mpf('1e-6')), solver='anderson', tol=1e-30, maxsteps=200)
    rowsB.append((n, xn))
    print("   n = %2d: kappa_b/kappa_c = %-5s x = %s  mu = %s  K_c = %s" % (n, mp.nstr(target, 4), mp.nstr(xn, 8), mp.nstr(mu_of(xn), 8), mp.nstr(kc(y_of(xn)), 8)))
chk("Q3c reading B admits a whole tower n = 5, 6, ..., 12 (checked), with mu decreasing and K_c increasing towards H as n grows: the integer condition does not single out a point (each K_c is algebraic, none equals 1/Z)",
    all(abs(kc(y_of(xn)) / TARGET - 1) > 1e-3 for _, xn in rowsB) and all(rowsB[i][1] > rowsB[i + 1][1] for i in range(len(rowsB) - 1)) and all(kc(y_of(rowsB[i][1])) < kc(y_of(rowsB[i + 1][1])) for i in range(len(rowsB) - 1)))
chk("Q3e the single clean interior point of reading A, n = 3 (kappa_c/kappa_b = 1/2), is EXACTLY mu = 1/sqrt2 with K_b = sqrt(3/2) and K_c = sqrt(3/8) (also = reading B, n = 6); mu = %s, K_b = %s" % (mp.nstr(mu_of(xA), 15), mp.nstr(kb(xA), 15)),
    abs(mu_of(xA) - 1 / mp.sqrt(2)) < 1e-25 and abs(kb(xA) - mp.sqrt(mp.mpf(3) / 2)) < 1e-25 and abs(kc(yA) - mp.sqrt(mp.mpf(3) / 8)) < 1e-25)
# orbifold
print("   Orbifold: cone angle 2 pi rho = 2 pi/N (reading A): rho = 1/N")
orb = []
for N in range(2, 9):
    xn = x_from_rho(mp.mpf(1) / N); orb.append((N, xn))
    print("   N = %d: mu = %s   K_b = %s" % (N, mp.nstr(mu_of(xn), 8), mp.nstr(kb(xn), 8)))
chk("Q3d orbifold cone angles 2 pi/N give a discrete set (one point per N); any rational rho = p/q also gives one: rationals are dense, so 'commensurate cone angle' does not single out a point", all(abs(rho_of(xn) - mp.mpf(1) / N) < 1e-25 for N, xn in orb))

# ---------------------------------------------------------------- Q4 the a0-points
xs = (mp.sqrt(1 + 3 * Z**2) - 1) / (3 * Z)                 # black-hole a0 point (reading A applies: kappa_b = a0)
ys = y_of(xs); rho_b = kc(ys) / kb(xs)
yc = (mp.sqrt(1 + 3 * Z**2) + 1) / (3 * Z); xc = y_of(yc) if False else (-yc + mp.sqrt(4 - 3 * yc**2)) / 2   # cosmological a0 point
rho_c = kb(xc) / kc(yc)
nA_a0 = 2 * (1 + rho_b); nB_a0 = 2 * (1 + rho_c)
print("\n   a0-point of the BLACK-HOLE horizon: mu = %s, kappa_c/kappa_b = %s, n_A = %s, cone angle = %s deg" % (mp.nstr(mu_of(xs), 10), mp.nstr(rho_b, 10), mp.nstr(nA_a0, 10), mp.nstr(360 * rho_b, 8)))
print("   a0-point of the COSMOLOGICAL horizon: mu = %s, kappa_b/kappa_c = %s, n_B = %s" % (mp.nstr(mu_of(xc), 10), mp.nstr(rho_c, 10), mp.nstr(nB_a0, 10)))
chk("Q4a at the a0-point n_A = %s (not an integer; distance to 4 is %s) and n_B = %s (not an integer; distance to 4 is %s): the a0-points are near-Nariai but are not integer-quantised points" % (mp.nstr(nA_a0, 8), mp.nstr(4 - nA_a0, 4), mp.nstr(nB_a0, 8), mp.nstr(nB_a0 - 4, 4)),
    abs(nA_a0 - mp.nint(nA_a0)) > mp.mpf('1e-3') and abs(nB_a0 - mp.nint(nB_a0)) > mp.mpf('1e-3'))
# near-Nariai expansion: 1 - rho ~ c * kappa  (leading order): rho = kappa_c/kappa_b
kk = [mp.mpf(v) for v in ['1e-3', '1e-4', '1e-5']]
lead = []
for kap_target in kk:
    xk = mp.findroot(lambda x: kb(x) - kap_target, xN - mp.mpf('1e-3') * kap_target, tol=1e-40)
    lead.append((1 - rho_of(xk)) / kap_target)
rich = lead[-1] + (lead[-1] - lead[-2]) / 9      # Richardson for an error linear in kappa (kappa ratio 10)
chk("Q4b near Nariai 1 - kappa_c/kappa_b = (4/(3 sqrt3)) kappa_b/H + O(kappa^2): Richardson-extrapolated coefficient %s vs 4/(3 sqrt3) = %s; so for ANY small a0/H the a0-points are within O(a0/H) of the Nariai ratio 1 (proximity to Nariai is generic, not specific to Z)" % (mp.nstr(rich, 8), mp.nstr(4 / (3 * mp.sqrt(3)), 8)),
    abs(rich - 4 / (3 * mp.sqrt(3))) < 1e-5)
# transcendence of rho at the a0 point (theorem; numerical PSLQ sanity with the same calibration as l03)
with mp.workdps(160):
    Zh = mp.sqrt(32 * mp.pi / 3); xh = (mp.sqrt(1 + 3 * Zh**2) - 1) / (3 * Zh); yh = (-xh + mp.sqrt(4 - 3 * xh**2)) / 2
    rho_h = ((3 * yh**2 - 1) / (2 * yh)) / ((1 - 3 * xh**2) / (2 * xh))
    fp_rho = mp.findpoly(rho_h, 8, maxcoeff=10**6, tol=mp.mpf('1e-100'), maxsteps=100000)
chk("Q4c kappa_c/kappa_b at the a0 point is an algebraic function of 1/Z (non-constant), hence transcendental by Lindemann, hence NOT rational: no integer n, no orbifold N (heuristic sanity: no integer polynomial of degree <= 8, coeff <= 1e6 at 100 digits: %s)" % (fp_rho,), fp_rho is None)

print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
