#!/usr/bin/env python3
"""l05_a0point_table_scan_matter.py -- task (3): every dimensionless quantity of the SdS geometry at the a0-points; E9 closed-form scan with decoys; E7 matter-content reading (DATA-DEPENDENT).

Part 1 (table): at the black-hole a0-point (kappa_b = a0, mu = 0.98695) and the cosmological a0-point (kappa_c = a0, mu = 0.98298): mu, r_b/L, r_c/L, |r_-|/L, S_b/S_dS = x^2, S_c/S_dS = y^2,
   S_tot/S_dS = 1 - x y, T_b/T_dS, T_c/T_dS, kappa_c/kappa_b, Bousso-Hawking-normalised kappa's, A_b Lambda, static radius r*, the two static worldlines with acceleration a0 inside SdS, cone quantities.
Part 2 (E9): does any of these equal a 'simple closed form'?  Menu: (p/q) pi^a sqrt3^b sqrt2^c, p,q <= 40 (coprime), a in {-2,-1,-1/2,0,1/2,1,2}, b,c in {0,1} (27,244 entries), tested against q and q^2 at relative tolerance 1e-9.
   The menu is written WITHOUT a target (the target quantities are unknown closed forms); to calibrate the false-positive rate the identical scan is run on DECOY a0-points Z' in {2 pi, 6, 5.5, 6.5, sqrt(8 pi/3), 1.05 Z}.
   A hit counts as a result only if it appears at the a0-point and not at the decoys at a rate above the decoys' (it will not; the expected spurious rate is quoted).
Part 3 (E7, DATA-DEPENDENT, never used to fit): a horizon-sized matter mass M_m as a fraction of M_N: (i) R = L: mu = (3 sqrt3/2) Omega_m/Omega_Lambda ;  (ii) R = R_H = 1/H: mu = (3 sqrt3/2) Omega_m sqrt(Omega_Lambda).
   Exact facts (proved): max over Omega_m of (ii) is 1 (= Nariai) at Omega_m = 2/3.  Illustrative data value Omega_m = 0.315 +/- 0.007 (Planck-2018-like, quoted from memory, NOT fetched, used only as an illustration).
Exit 0 iff every check holds.
"""
import sys, math
import numpy as np
import mpmath as mp
import sympy as sp
from math import gcd

mp.mp.dps = 50
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def mut(name, wrong):
    ok.append(not bool(wrong)); print(("PASS [mutation rejected] " if not wrong else "FAIL [mutation NOT rejected] ") + name)

def kb(x): return (1 - 3 * x**2) / (2 * x)
def kc(y): return (3 * y**2 - 1) / (2 * y)
def part(x): return (-x + mp.sqrt(4 - 3 * x**2)) / 2       # partner root (x <-> y symmetric relation x^2 + x y + y^2 = 1, root of the same quadratic)
MNu = 1 / (3 * mp.sqrt(3))

def a0points(Zp):
    """returns dict of quantities at the black-hole a0-point and the cosmological a0-point for a0 = H/Zp"""
    out = {}
    Kt = 1 / Zp
    x = (mp.sqrt(1 + 3 * Zp**2) - 1) / (3 * Zp); y = part(x)                 # BH point: kappa_b = a0
    yc = (mp.sqrt(1 + 3 * Zp**2) + 1) / (3 * Zp); xc = part(yc)               # cosmological point: kappa_c = a0
    for tag, (xx, yy) in {'b': (x, y), 'c': (xc, yc)}.items():
        M = xx * yy * (xx + yy) / 2
        mu = M / MNu
        rs = M**(mp.mpf(1) / 3); fs = 1 - 3 * M**(mp.mpf(2) / 3)
        kbh, kch = kb(xx) / mp.sqrt(fs), kc(yy) / mp.sqrt(fs)
        rho = kc(yy) / kb(xx)
        d = {
            'mu': mu, 'r_b/L': xx, 'r_c/L': yy, '|r_-|/L': xx + yy, 'S_b/S_dS': xx**2, 'S_c/S_dS': yy**2, 'S_tot/S_dS': 1 - xx * yy, 'dS/S_dS': xx * yy,
            'S_b/S_c': xx**2 / yy**2, 'T_b/T_dS': kb(xx), 'T_c/T_dS': kc(yy), 'T_c/T_b': rho, 'T_b/T_c': 1 / rho,
            'kBH_b': kbh, 'kBH_c': kch, 'f(r*)': fs, 'r*/L': rs, 'M/L': M, 'A_b Lam/pi': 12 * xx**2, 'A_c Lam/pi': 12 * yy**2,
            'n_A=IntE4/32pi^2': 2 * (1 + rho), 'n_B': 2 * (1 + 1 / rho), 'rho_m/rho_L (R=L)': 2 * M, 'kb*rb': kb(xx) * xx, 'kc*rc': kc(yy) * yy,
        }
        # static worldlines with acceleration a0 in SdS: a(r) = |M/r^2 - r|/sqrt(f)
        fun = lambda r: (M / r**2 - r) / mp.sqrt(1 - 2 * M / r - r**2)
        try:
            r1 = mp.findroot(lambda r: abs(fun(r)) - Kt, (xx + (rs - xx) * mp.mpf('1e-6'), rs * (1 - mp.mpf('1e-12'))), solver='anderson', tol=1e-30, maxsteps=400)
            r2 = mp.findroot(lambda r: abs(fun(r)) - Kt, (rs * (1 + mp.mpf('1e-12')), yy - (yy - rs) * mp.mpf('1e-6')), solver='anderson', tol=1e-30, maxsteps=400)
            d['r_static1/L'] = mp.re(r1); d['r_static2/L'] = mp.re(r2)
        except Exception:
            pass
        out[tag] = d
    return out

Z = mp.sqrt(32 * mp.pi / 3)
P = a0points(Z)
print("=== Part 1: the a0-points (Z = %s) ===" % mp.nstr(Z, 10))
for tag, name in [('b', 'BLACK-HOLE horizon a0-point (kappa_b = a0)'), ('c', 'COSMOLOGICAL horizon a0-point (kappa_c = a0)')]:
    print(" " + name)
    for k, v in P[tag].items():
        print("    %-22s %s" % (k, mp.nstr(v, 14)))
b, c = P['b'], P['c']
chk("T1 identities at the b-point: x^2 + x y + y^2 = 1, 2M = x y (x+y), f(r_b)=f(r_c)=0, kappa_b = a0, T_b/T_dS = 1/Z; at the c-point kappa_c = a0",
    abs(b['r_b/L']**2 + b['r_b/L'] * b['r_c/L'] + b['r_c/L']**2 - 1) < 1e-40 and abs(b['T_b/T_dS'] - 1 / Z) < 1e-40 and abs(c['T_c/T_dS'] - 1 / Z) < 1e-40
    and abs(1 - 2 * b['M/L'] / b['r_b/L'] - b['r_b/L']**2) < 1e-40 and abs(1 - 2 * b['M/L'] / b['r_c/L'] - b['r_c/L']**2) < 1e-40)
chk("T2 A_b Lambda = 12 pi x^2 = %s (not 32 pi^2 = %s): the puzzle's AREA relation does not hold at the a0-point (audit a07 S3 reproduced); S_tot/S_dS = %s" % (mp.nstr(mp.pi * b['A_b Lam/pi'], 8), mp.nstr(32 * mp.pi**2, 8), mp.nstr(b['S_tot/S_dS'], 8)),
    abs(mp.pi * b['A_b Lam/pi'] - mp.mpf('10.297306')) < 1e-5 and mp.pi * b['A_b Lam/pi'] < 12.6)
chk("T3 BH-normalised surface gravities at the b-point: kappa_b^BH = %s H, kappa_c^BH = %s H: both > H, so in that normalisation a0 = H/Z is NOT a horizon value (a07 S5 reproduced)" % (mp.nstr(b['kBH_b'], 8), mp.nstr(b['kBH_c'], 8)), b['kBH_b'] > 1 and b['kBH_c'] > 1)
has_static = 'r_static1/L' in b and 'r_static2/L' in b
chk("T4 two static worldlines with proper acceleration a0 exist inside the b-point SdS, at r/L = %s < r* = %s < r/L = %s, both between the horizons (r_b = %s, r_c = %s); pure de Sitter: sin(theta0) = 1/sqrt(1+Z^2) = %s" % (
    mp.nstr(b.get('r_static1/L', 0), 8), mp.nstr(b['r*/L'], 8), mp.nstr(b.get('r_static2/L', 0), 8), mp.nstr(b['r_b/L'], 8), mp.nstr(b['r_c/L'], 8), mp.nstr(1 / mp.sqrt(1 + Z**2), 8)),
    has_static and b['r_b/L'] < b['r_static1/L'] < b['r*/L'] < b['r_static2/L'] < b['r_c/L'])

# ------------------------------------------------------------ Part 2: closed-form scan with decoys
menu_vals = []; menu_lab = []
alist = [-2, -1, -0.5, 0, 0.5, 1, 2]
for p in range(1, 41):
    for q in range(1, 41):
        if gcd(p, q) != 1: continue
        for a in alist:
            for bb in (0, 1):
                for cc in (0, 1):
                    menu_vals.append((p / q) * math.pi**a * math.sqrt(3)**bb * math.sqrt(2)**cc); menu_lab.append("(%d/%d) pi^%s sqrt3^%d sqrt2^%d" % (p, q, a, bb, cc))
menu_vals = np.array(menu_vals); order = np.argsort(menu_vals); menu_vals = menu_vals[order]; menu_lab = [menu_lab[i] for i in order]
TOLS = 1e-9
def scan_value(v):
    v = float(v); hits = []
    for target, tag in ((v, ''), (v * v, '^2')):
        if target <= 0: continue
        lo = np.searchsorted(menu_vals, target * (1 - TOLS)); hi = np.searchsorted(menu_vals, target * (1 + TOLS))
        for i in range(lo, hi): hits.append(("q" + tag, menu_lab[i]))
    return hits
print("\n=== Part 2 (E9): closed-form scan, menu size %d, tolerance %.0e, decoys for the hit rate ===" % (len(menu_vals), TOLS))
skip = {'b': {'T_b/T_dS'}, 'c': {'T_c/T_dS'}}
def run(Zp, label):
    Pp = a0points(Zp); n_tests = 0; hits = []
    for tag in ('b', 'c'):
        for k, v in Pp[tag].items():
            if k in skip[tag]: continue
            n_tests += 1
            h = scan_value(v)
            for hh in h: hits.append((tag, k, hh))
    return n_tests, hits
res = {}
for label, Zp in [('a0 point Z = sqrt(32pi/3)', Z), ('decoy Z = 2 pi (Milgrom)', 2 * mp.pi), ('decoy Z = 6', mp.mpf(6)), ('decoy Z = 5.5', mp.mpf('5.5')), ('decoy Z = 6.5', mp.mpf('6.5')),
                  ('decoy Z = sqrt(8pi/3) (kappa=1)', mp.sqrt(8 * mp.pi / 3)), ('decoy Z = 1.05 Z', Z * mp.mpf('1.05'))]:
    n, h = run(Zp, label); res[label] = (n, h)
    print("   %-36s quantities tested: %2d   closed-form hits: %d %s" % (label, n, len(h), [(t, k, hh) for t, k, hh in h][:4]))
n_main, h_main = res['a0 point Z = sqrt(32pi/3)']
dec_hits = sum(len(v[1]) for kx, v in res.items() if kx.startswith('decoy'))
dec_tests = sum(v[0] for kx, v in res.items() if kx.startswith('decoy'))
chk("E9a the a0-point has %d closed-form hits among %d quantities (each tested as q and q^2); the six decoy points have %d hits among %d quantities; expected spurious rate ~ %.1e per test at this menu size and tolerance"
    % (len(h_main), n_main, dec_hits, dec_tests, len(menu_vals) * 2 * TOLS * 2), len(h_main) <= max(1, dec_hits))
# what the scan CAN do: control -- inject a known closed form and recover it; and confirm the tolerance separates a 1e-6 offset
inj = math.pi * 3 / 7 * math.sqrt(3)
chk("E9b control: a planted value (3/7) pi sqrt3 is recovered by the scan (%s); the same value shifted by 1e-6 (relative) is not" % (scan_value(inj)[:1],), len(scan_value(inj)) >= 1 and len(scan_value(inj * (1 + 1e-6))) == 0)
chk("E9c verdict: no quantity of the SdS geometry at the a0-point equals a simple (rational x pi^a sqrt3^b sqrt2^c, p,q <= 40) closed form to 1e-9; every quantity is an explicit algebraic function of Z^2 = 32 pi/3 (e.g. r_b/L = (sqrt(1+32 pi) - 1)/sqrt(96 pi)) with no simplification",
    len(h_main) == 0)

# ------------------------------------------------------------ Part 3: matter-content readings (DATA-DEPENDENT)
print("\n=== Part 3 (E7): matter mass as a fraction of M_N -- DATA-DEPENDENT, never used to fit ===")
Om = sp.symbols('Omega_m', positive=True)
mu_i = 3 * sp.sqrt(3) / 2 * Om / (1 - Om)
mu_ii = 3 * sp.sqrt(3) / 2 * Om * sp.sqrt(1 - Om)
# derivations of the two readings from rho_m, rho_Lambda:  H_L^2 = 8 pi rho_L/3 = 1/L^2 ; H^2 = H_L^2/Omega_L
rL, Lq, R_H = sp.symbols('rho_L L R_H', positive=True)
Om_L = 1 - Om
Mi = sp.Rational(4, 3) * sp.pi * (Om / Om_L) * (3 / (8 * sp.pi * Lq**2)) * Lq**3        # matter mass inside R = L
Mii = sp.Rational(4, 3) * sp.pi * (Om / Om_L) * (3 / (8 * sp.pi * Lq**2)) * (Lq * sp.sqrt(Om_L))**3   # inside R_H = 1/H = L sqrt(Omega_L)
MN_s = Lq / (3 * sp.sqrt(3))
chk("M1 derivations: M_m(L)/M_N = (3 sqrt3/2) Omega_m/Omega_Lambda  and  M_m(R_H)/M_N = (3 sqrt3/2) Omega_m sqrt(Omega_Lambda) (rho_m = (Omega_m/Omega_Lambda) rho_Lambda, rho_Lambda = 3/(8 pi L^2), pi cancels)",
    sp.simplify(Mi / MN_s - mu_i) == 0 and sp.simplify(Mii / MN_s - mu_ii) == 0)
crit = sp.solve(sp.diff(mu_ii, Om), Om)
chk("M2 exact: the reading-(ii) mass fraction has its maximum at Omega_m = 2/3 with value exactly 1 (the Nariai mass): mu_ii <= 1 for every Omega_m, equality only at 2/3 (critical points %s; value %s)" % (crit, sp.simplify(mu_ii.subs(Om, sp.Rational(2, 3)))),
    crit == [sp.Rational(2, 3)] and sp.simplify(mu_ii.subs(Om, sp.Rational(2, 3))) == 1)
mus = float(P['b']['mu'])
print("   a0-point (BH) mass fraction mu* = %.8f ; cosmological a0-point mu_c = %.8f" % (mus, float(P['c']['mu'])))
kk_ = 2 * P['b']['mu'] / (3 * mp.sqrt(3))               # = x(1-x^2) = rho_m/rho_Lambda needed for reading (i)
Om_i = float(kk_ / (1 + kk_))
cub = mp.polyroots([1, -1, 0, kk_**2], maxsteps=200, extraprec=100)   # Omega^3 - Omega^2 + k^2 = 0  <=>  Omega sqrt(1-Omega) = k
roots_ii = sorted([float(mp.re(r_)) for r_ in cub if abs(mp.im(r_)) < 1e-20 and 0 < mp.re(r_) < 1])
print("   Omega_m that would give mu = mu*:  reading (i): %.4f ; reading (ii): %s" % (Om_i, [round(v, 4) for v in roots_ii]))
for om, lab in [(0.315, 'Omega_m = 0.315 (Planck-2018-like, illustrative)'), (0.27, 'Omega_m = 0.27'), (0.34, 'Omega_m = 0.34')]:
    print("   %-52s reading (i) mu = %.4f   reading (ii) mu = %.4f" % (lab, float(mu_i.subs(Om, om)), float(mu_ii.subs(Om, om))))
mu_obs_i = float(mu_i.subs(Om, 0.315)); mu_obs_ii = float(mu_ii.subs(Om, 0.315))
chk("M3 (data-dependent illustration) with Omega_m = 0.315: reading (i) mu = %.3f (%.0f%% above mu* = %.4f), reading (ii) mu = %.3f (%.0f%% below mu*): neither equals mu*; the Omega_m that would match is %.4f (reading i), %.4f/%.4f (reading ii), %.1f sigma from 0.315 +/- 0.007 for reading (i)" % (
    mu_obs_i, 100 * (mu_obs_i / mus - 1), mus, mu_obs_ii, 100 * (1 - mu_obs_ii / mus), Om_i, roots_ii[0], roots_ii[1], (0.315 - float(Om_i)) / 0.007),
    abs(mu_obs_i / mus - 1) > 0.1 and abs(mu_obs_ii / mus - 1) > 0.1)
# time dependence: rho_m/rho_Lambda ~ a^-3 ; reading (i) crosses mu* at a definite epoch
rat0 = 0.315 / 0.685; rat_star = float(2 * mu_of_b) if False else float(P['b']['rho_m/rho_L (R=L)'])
a_cross = (rat0 / rat_star)**(1 / 3)
def t_of_a(a, Om_m0=0.315, H0=67.4):
    HL = H0 * math.sqrt(1 - Om_m0) / 977.8      # 1/Gyr  (977.8/H0 Gyr per km/s/Mpc)
    return 2 / (3 * HL) * math.asinh(math.sqrt((1 - Om_m0) / Om_m0) * a**1.5)
dt = t_of_a(a_cross) - t_of_a(1.0)
chk("M4 the reading (i) mu_m(t) = (3 sqrt3/2) rho_m/rho_Lambda ~ a^-3 falls with time: it equals mu* only at a = %.4f, i.e. %+.2f Gyr from now (flat LCDM, Omega_m = 0.315, H0 = 67.4, illustrative): a time-dependent reading cannot fix a CONSTANT a0/H_Lambda (the record's flat a0(z) law), so it cannot be the principle" % (a_cross, dt), a_cross > 1 and 0 < dt < 3)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
