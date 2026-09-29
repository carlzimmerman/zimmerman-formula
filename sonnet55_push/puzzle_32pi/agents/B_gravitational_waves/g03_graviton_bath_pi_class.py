#!/usr/bin/env python3
"""g03_graviton_bath_pi_class.py -- lane B: the record's graviton-bath chain (real_research/reviews/mi_graviton_bath_ctp_2026.py; qwen_38_experiment T003) with the
CANONICAL graviton normalisation derived in g01 (kappa_g^2 = 32 pi G).  hbar = c = 1.

The record's chain (its assumptions, taken as given here; I do not audit them):
   S_dS = pi/(G H^2)                (A1, horizon entropy)      T = H/(2 pi)         (A2)
   eps_1 = m * <h^2>                (A3; the record uses m = 1/8 from sqrt(1+X) = 1 + X/2 - X^2/8)
   eps_tot = S_dS * eps_1           (A4, incoherent sum)       a0^2 = 3 eps_tot H^2  (A6)       kappa^2 = a0^2/(G rho_L) with H^2 = 8 pi G rho_L/3 (A5)  => kappa^2 = 8 pi eps_tot
The record found kappa in {0.500, 1.447, 2.047} for three normalisations of <h^2>, and named the open question 'why eps_tot = 1/(32 pi)'.

PRE-DECLARED PREDICTION (before evaluation): with any CANONICAL <h^2> (32 pi G x <phi^2>, <phi^2> in {T^2/12 thermal, (H/2 pi)^2 per e-fold de Sitter}) and ANY rational dressing
(m, polarisation count, rational knobs c1..c7), holography cancels G,H AND the pi:  eps_tot is RATIONAL, so a0/(cH) is algebraic and kappa^2 = 8 pi eps_tot is a rational multiple of pi.
The puzzle needs eps_tot = 1/(32 pi) (not rational).  So no canonical normalisation with rational dressing can give kappa = 1/2.
Exit 0 iff all checks (including controls) behave as declared.
"""
import sys, math
import sympy as sp

ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

G, H, T, k = sp.symbols('G H T k', positive=True)
m = sp.symbols('m', positive=True)                                 # rational dressing multiplier (record: 1/8)

# --- the two canonical <phi^2> (derived here, not quoted)
import mpmath as mp
mp.mp.dps = 30
Ibose = mp.quad(lambda x: x / (mp.exp(x) - 1), [0, 1, 10, mp.inf])      # int_0^oo x/(e^x-1) dx = Gamma(2) zeta(2) = pi^2/6
assert abs(Ibose - mp.pi**2 / 6) < mp.mpf(10)**-25
Ith = T**2 * sp.pi**2 / 6                                               # int k dk n_B(k), k = T x  (value checked numerically above)
phi2_th = sp.simplify(sp.Rational(1, 2) / sp.pi**2 * Ith)          # <phi^2> = int d^3k/((2pi)^3 2k) 2 n_B = (1/(2 pi^2)) int k n_B dk
chk("B1  thermal massless scalar <phi^2> = T^2/12", sp.simplify(phi2_th - T**2 / 12) == 0)
kk, tau = sp.symbols('kk tau', real=True)
mode2 = sp.simplify(sp.Abs(H / sp.sqrt(2 * kk**3) * (1 + sp.I * kk * tau) * sp.exp(-sp.I * kk * tau))**2)
lim = sp.limit(mode2.subs(kk, 1), tau, 0)                              # |phi_k|^2 -> H^2/(2 k^3) at late times
phi2_bd = sp.simplify(kk**3 / (2 * sp.pi**2) * H**2 / (2 * kk**3))
chk("B2  de Sitter massless mode: |phi_k|^2 -> H^2/(2 k^3), <phi^2> per e-fold = (H/2 pi)^2 (Bunch-Davies)", sp.simplify(lim - H**2 / 2) == 0 and sp.simplify(phi2_bd - H**2 / (4 * sp.pi**2)) == 0)

S = sp.pi / (G * H**2)
T_dS = H / (2 * sp.pi)
h2 = lambda phi2: 32 * sp.pi * G * phi2                            # canonical: h_hat = sqrt(32 pi G) phi per unit-norm polarisation (g01 A3)

cases = {
    "thermal flat <phi^2>=T^2/12 at T=H/2pi": phi2_th.subs(T, T_dS),
    "Bunch-Davies per e-fold <phi^2>=(H/2pi)^2": phi2_bd,
}
print("\n   canonical two-point functions x horizon entropy (dressing m free):")
rat = []
for name, phi2 in cases.items():
    eps_tot = sp.simplify(S * m * h2(phi2))
    chk("B3  %-44s eps_tot = %s : G, H and pi all cancel, rational in m" % (name, eps_tot), not eps_tot.has(G) and not eps_tot.has(H) and not eps_tot.has(sp.pi))
    rat.append(eps_tot)
    a0_over_cH2 = sp.simplify(3 * eps_tot)                              # A6
    kap2 = sp.simplify(8 * sp.pi * eps_tot)                             # kappa^2 = 8 pi eps_tot
    print("        (a0/cH)^2 = %s  (algebraic);   kappa^2 = %s  (rational x pi)" % (a0_over_cH2, kap2))
eps_th = rat[0]
# the record's m = 1/8: reproduce 1/12, kappa = 1.447, and note a0 = cH/2
chk("B4  m = 1/8 (record): eps_tot = 1/12, kappa = sqrt(2 pi/3) = %.4f, (a0/cH)^2 = 1/4  i.e. a0 = cH/2 (Z = 2, not Z = 5.789)" % math.sqrt(2 * math.pi / 3),
    sp.simplify(eps_th.subs(m, sp.Rational(1, 8)) - sp.Rational(1, 12)) == 0 and sp.simplify(3 * eps_th.subs(m, sp.Rational(1, 8)) - sp.Rational(1, 4)) == 0)
chk("B5  two polarisations (m = 1/4): eps_tot = 1/6, kappa = sqrt(4 pi/3) = %.4f  (the record's 2.047)" % math.sqrt(4 * math.pi / 3),
    sp.simplify(eps_th.subs(m, sp.Rational(1, 4)) - sp.Rational(1, 6)) == 0)

# --- the general statement with ALL the record's rational knobs
c1, c2, c3, c4, c5, c6 = sp.symbols('c1 c2 c3 c4 c5 c6', positive=True)
eps_gen = (c4 * c1 * S) * (c3 * m * 32 * sp.pi * G * (H / (2 * sp.pi * c2))**2 / 12)
a0cH2 = sp.simplify(c6 * eps_gen)
chk("B6  with every rational knob c1..c6 free, (a0/cH)^2 = %s: pi-free, so a0/(cH) is an algebraic number for every rational dressing" % a0cH2, not a0cH2.has(sp.pi) and not a0cH2.has(G) and not a0cH2.has(H))
Z2 = 32 * sp.pi / 3
need = sp.simplify(1 / Z2)
chk("B7  the puzzle needs (a0/cH)^2 = 1/Z^2 = 3/(32 pi): NOT rational, so it is not in the range of B6 (Lindemann: pi transcendental => 1/Z is not algebraic)", not need.is_rational)
msol = sp.solve(sp.Eq(a0cH2.subs({c1: 1, c2: 1, c3: 1, c4: 1, c6: 3}), need), m)[0]
chk("B8  solving for the dressing: m = %s (pi^-1): a rational tensor-structure/polarisation dressing can never supply it" % msol, sp.simplify(msol - 3 / (64 * sp.pi)) == 0 and not msol.is_rational)

# --- controls
loose = sp.simplify(S * sp.Rational(1, 8) * G * T_dS**2)                # the record's loose normalisation A: <h^2> = G T^2 (no 32 pi)
chk("C1  CONTROL (test is sensitive): the record's LOOSE normalisation <h^2> = G T^2 gives eps_tot = %s = 1/(32 pi): NOT rational, kappa = 1/2 -- i.e. it is exactly the canonical 32 pi x (1/12) that is missing" % loose,
    sp.simplify(loose - 1 / (32 * sp.pi)) == 0 and not loose.is_rational and sp.simplify(sp.sqrt(8 * sp.pi * loose) - sp.Rational(1, 2)) == 0)
ratio = sp.simplify(eps_th.subs(m, sp.Rational(1, 8)) / loose)
chk("C2  canonical/loose = 32 pi/12 = 8 pi/3 (the record's factor): kappa_canon = kappa_loose sqrt(8 pi/3) = (1/2) sqrt(8 pi/3) = %.4f" % (0.5 * math.sqrt(8 * math.pi / 3)), sp.simplify(ratio - 8 * sp.pi / 3) == 0)
# variant with a pi-free mode count N = R^2/l_P^2 = 1/(G H^2) (a convention-level choice in the graviton-condensate literature, e.g. arXiv:1701.08776: 'horizon area in Planck units')
Nfree = 1 / (G * H**2)
eps_v = sp.simplify(Nfree * m * h2(phi2_th.subs(T, T_dS)))
kap_v = sp.simplify(8 * sp.pi * eps_v)
chk("C3  VARIANT (pi-free counting N = 1/(G H^2)): eps_tot = %s (pi^-1), kappa^2 = %s (rational): the pi-obstruction is lifted, but m = 1/8 gives kappa^2 = 2/3, two pols 4/3; kappa = 1/2 then needs m = %s: a free rational, no principle (not a no-go, not a derivation)" % (eps_v, kap_v, sp.solve(sp.Eq(kap_v, sp.Rational(1, 4)), m)[0]),
    kap_v.subs(m, sp.Rational(1, 8)) == sp.Rational(2, 3) and kap_v.subs(m, sp.Rational(1, 4)) == sp.Rational(4, 3) and sp.solve(sp.Eq(kap_v, sp.Rational(1, 4)), m)[0] == sp.Rational(3, 64))
# holography lemma: S_dS x <h_ij h_ij> is rational for both states (per unit-norm pol, two pols)
for name, phi2 in cases.items():
    val = sp.simplify(S * 2 * h2(phi2))
    chk("B9  S_dS x <h_ij h_ij> (2 pols), %-44s = %s (rational)" % (name, val), val.is_rational)

print("\n%d/%d checks behaved as declared" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
