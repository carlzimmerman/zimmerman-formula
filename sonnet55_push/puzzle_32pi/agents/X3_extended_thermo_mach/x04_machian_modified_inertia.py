#!/usr/bin/env python3
"""x04: does the retarded Sciama integral give a MODIFIED inertia below a critical ACCELERATION, and is there a natural cutoff at r_s = c/sqrt(G rho_L)?
Predeclared: PREDECLARED.md, PART B-M (M1 step, M2 oscillation, M3 Rindler cap, M4 frequency->acceleration).  c = 1 inside formulas.
Premise used throughout (a premise, stated once): inertial force on the body = - (m/c^2) int G rho (dv_rel/dt)(t - r/c)/r dV, the retarded form of Sciama's
   E = -dA/dt with A = -G int rho v/r dV (as relayed by arXiv:1104.1306 and arXiv:2308.04503, both opened)."""
import sympy as sp
from sympy import pi, sqrt, Rational as Rat, symbols, simplify
import mpmath as mp
import sys

PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


def zero(e): return sp.simplify(e) == 0


r, t, T, R, a, G, rho, kap, tau, u = symbols('r t T R a G rho kappa tau u', positive=True)
w = symbols('omega', positive=True)

print("== M1: step acceleration of duration t (matter at distance r sees it only after r/c) ==")
# force/(G rho a) = int_{r < c t} dV/r  (c = 1)
F_step = sp.integrate(4 * pi * r, (r, 0, t))
chk("F(t)/(G rho a) = 2 pi c^2 t^2 for t < R/c: it depends on the DURATION t, not on the size of a", zero(F_step - 2 * pi * t ** 2))
mi_ratio = sp.Min(1, (t / R) ** 2)
chk("m_i(t)/m_i(inf) = (c t/R_c)^2 for t < R_c/c (then 1): d/da of the ratio is identically 0 (a-independent)", zero(sp.diff((t / R) ** 2, a)))
# memory kernel K(tau) = weight of matter at distance c tau, normalised on [0, T], T = R_c/c
Kern = 2 * tau / T ** 2
chk("kernel K(tau) = 2 tau/T^2 (weight ~ 4 pi r dr for the 1/r kernel) is normalised", zero(sp.integrate(Kern, (tau, 0, T)) - 1))
M1_sharp = sp.integrate(tau * Kern, (tau, 0, T))
chk("first moment M1 = (2/3) T = (2/3) R_c/c for the sharp uniform ball", zero(M1_sharp - Rat(2, 3) * T))
# the record's requirement (real_research/reviews/mi_N_count_and_kappa_iff_2026.py Part C, symbolic there): M1 = (2/3) c/a0
a0, c_, Gr = symbols('a0 c Grho', positive=True)
Tsol = sp.solve(sp.Eq(M1_sharp, Rat(2, 3) / a0), T)[0]
chk("record's action requirement M1 = (2/3) c/a0  <=>  T = c/a0, i.e. R_c = c^2/a0 (the RINDLER distance of a0) for the sharp 1/r kernel", zero(Tsol - 1 / a0))
# kernel shape matters for the identification of the cutoff (not for M1): Yukawa-screened kernel and 1/r^2 mutation
K_yuk = tau * sp.exp(-tau / T) / T ** 2
M1_yuk = sp.integrate(tau * K_yuk, (tau, 0, sp.oo))
chk("Yukawa-screened kernel (weight r e^{-r/R} dr): M1 = 2 T, so the identification would be T = c/(3 a0), R_c = c^2/(3 a0): shape-dependent cutoff",
    zero(sp.integrate(K_yuk, (tau, 0, sp.oo)) - 1) and zero(M1_yuk - 2 * T))
K_r2 = 1 / T
ctrl("mutation: a 1/r^2 kernel (weight dr) would give M1 = T/2, not (2/3) T", zero(sp.integrate(tau * K_r2, (tau, 0, T)) - Rat(2, 3) * T))
# puzzle cutoff and Sciama closure
Rstar = 1 / sqrt(Gr)
Rc_puzzle = 2 * Rstar                                      # = c^2/a0 with a0 = sqrt(G rho)/2
I_at_Rc = simplify(2 * pi * Gr * Rc_puzzle ** 2)
chk("at the puzzle's cutoff R_c = c^2/a0 = 2 R* the Sciama integral is I = |Phi|/c^2 = 8 pi (closure would need 1)", zero(I_at_Rc - 8 * pi))
RS = 1 / sqrt(2 * pi * Gr)
chk("R_c(puzzle)/R_S(Sciama closure) = sqrt(8 pi) = 5.013;  R_c(puzzle)/R_H = Z = 5.789 (R_H = c/H_L)",
    zero(Rc_puzzle / RS - sqrt(8 * pi)) and zero(Rc_puzzle / (1 / sqrt(8 * pi * Gr / 3)) - sqrt(32 * pi / 3)))
ctrl("mutation: the puzzle's cutoff equals the Sciama closure radius", zero(Rc_puzzle / RS - 1))

print("\n== M2: oscillating acceleration a cos(omega t), sharp ball of radius R_c ==")
kR = symbols('kR', positive=True)
resp = sp.integrate(r * sp.exp(-sp.I * (kR / R) * r), (r, 0, R))
chi = sp.simplify(2 * resp / R ** 2)                     # normalised to 1 at kR -> 0
chi_re = sp.simplify(sp.re(sp.expand_complex(chi)))
chi_re_expected = 2 * (sp.cos(kR) + kR * sp.sin(kR) - 1) / kR ** 2
chk("in-phase (inertial) part of the retarded response: Re chi(kR) = 2 (cos kR + kR sin kR - 1)/(kR)^2",
    all(abs(float(chi_re.subs({kR: kk, R: 1.7})) - float(chi_re_expected.subs(kR, kk))) < 1e-9 for kk in (0.3, 1.1, 2.0, 5.5, 9.0)))
chk("kR -> 0: Re chi = 1 - (kR)^2/4 + ...  (inertia is FULL at low frequency and DROPS at high frequency)",
    sp.series(chi_re_expected, kR, 0, 4).removeO() == 1 - kR ** 2 / 4)
kk0 = mp.findroot(lambda z: mp.cos(z) + z * mp.sin(z) - 1, 2.3)
print(f"   first zero of the in-phase inertia: kR_0 = {mp.nstr(kk0, 12)}  (root of cos x + x sin x = 1; transcendental equation)")
chk("the in-phase inertia changes sign (negative effective mass) at kR_0 = 2.3311...", abs(kk0 - mp.mpf('2.3311226')) < 1e-5 and float(chi_re_expected.subs(kR, 3.0)) < 0)
# Yukawa smoothed variant: chi_Y = 1/(1 + i kR)^2
chiY = 1 / (1 + sp.I * kR) ** 2
chiY_re = sp.simplify(sp.re(sp.expand_complex(chiY)))
chk("Yukawa variant: Re chi_Y = (1 - (kR)^2)/(1 + (kR)^2)^2, zero exactly at kR = 1 (omega = c/R)", zero(chiY_re - (1 - kR ** 2) / (1 + kR ** 2) ** 2) and zero(chiY_re.subs(kR, 1)))
ctrl("mutation: in-phase inertia is enhanced (>1) at some finite kR in the sharp model", any(float(chi_re_expected.subs(kR, k)) > 1.0000001 for k in [0.01, 0.1, 0.5, 1, 2, 3, 5, 8]))

print("\n== M3: matter behind the accelerated observer's horizon removed (premise) ==")
d = symbols('d', positive=True)   # distance to the horizon = c^2/a
ang = 2 * pi * (1 - d / r)        # solid angle of the region beyond the plane at distance d, at radius r >= d
Icap = sp.integrate(r * ang, (r, d, R))
chk("removed potential  int_cap dV/r = pi (R - d)^2  (exact solid-angle integral)", zero(Icap - pi * (R - d) ** 2))
mu_cap = 1 - Icap / (2 * pi * R ** 2)
chk("mu_cap(a) = 1 - (1 - c^2/(a R))^2/2 for a > c^2/R; -> 1/2 as a -> infinity; d mu/d a < 0 (inertia falls at HIGH acceleration)",
    zero(mu_cap - (1 - (1 - d / R) ** 2 / 2)) and all(float(sp.diff(mu_cap.subs({R: 1.0, d: 1 / a}), a).subs(a, av)) < 0 for av in (1.5, 3.0, 10.0, 100.0)))
chk("mu_cap never falls below 1/2: no deep-MOND slope mu ~ a/a_c, and the direction is opposite to Milgrom's mu(a/a0) -> a/a0 at low a",
    float(mu_cap.subs({R: 1.0, d: 1 / 1e9})) > 0.4999)
ctrl("mutation: mu_cap -> 0 as a -> infinity", float(mu_cap.subs({R: 1.0, d: 1 / 1e9})) < 1e-3)

print("\n== M4: from a cutoff (frequency or length) to an acceleration ==")
# a = v omega for circular motion; kernel cutoff omega_c = kR_c c/R_c
print("   a_c = (v/c) kR_c c^2/R_c :  the cutoff is a frequency, so the acceleration it corresponds to carries a factor v/c (velocity dependent).")
print("   Galactic v/c ~ 1e-3: a_c ~ 1e-3 x (c^2/R_c) x kR_c, i.e. about 1e-3 a0 for R_c = c^2/a0: the retarded-integral cutoff acts far below a0 at v << c.")
chk("a_c depends on v: two orbits with the same acceleration a = v^2/r but different (v, r) have different omega = v/r, hence different retarded response (not a function of a alone)",
    (lambda v1, r1, v2, r2: abs(v1 ** 2 / r1 - v2 ** 2 / r2) < 1e-15 and abs(v1 / r1 - v2 / r2) > 1e-3)(2.0, 4.0, 1.0, 1.0))
Grho_s = symbols('Grho_s', positive=True)
cands = {"R_H": 1 / sqrt(8 * pi * Grho_s / 3), "R_S": 1 / sqrt(2 * pi * Grho_s), "R*": 1 / sqrt(Grho_s), "2R*": 2 / sqrt(Grho_s), "Z R_H": sqrt(32 * pi / 3) / sqrt(8 * pi * Grho_s / 3)}
print("   Rindler conversion a_c = c^2/R_c (v = c: the Unruh/Rindler identification, a premise):")
tab = {}
for nm, Rcut in cands.items():
    val = simplify((1 / Rcut) ** 2 / Grho_s)
    tab[nm] = val
    print(f"     R_c = {nm:6s}: a_c^2/(G rho_L c^2) = {val} = {float(val):.5f}")
chk("Rindler conversion values: R_H -> 8 pi/3, R_S -> 2 pi, R* -> 1, 2R* -> 1/4 (the puzzle), Z R_H -> 1/4", tab["R_H"] == 8 * pi / 3 and simplify(tab["R_S"] - 2 * pi) == 0 and tab["R*"] == 1 and tab["2R*"] == Rat(1, 4) and simplify(tab["Z R_H"] - Rat(1, 4)) == 0)
chk("the puzzle's a0 is reproduced by the Sciama-type kernel ONLY if its cutoff is c^2/a0 = 2 R* = Z R_H = 5.789 Hubble radii, which is not the Hubble radius (=event horizon in dS), not the Sciama closure radius, not R*",
    tab["2R*"] == Rat(1, 4) and all(tab[k] != Rat(1, 4) for k in ("R_H", "R_S", "R*")))
# pi-class: any cutoff R_c = q R_H or q R_S or q R* with rational q
qs = symbols('q', positive=True)
q_needed_H = sp.solve(sp.Eq((1 / (qs * cands["R_H"])) ** 2 / Grho_s, Rat(1, 4)), qs)[0]
q_needed_S = sp.solve(sp.Eq((1 / (qs * cands["R_S"])) ** 2 / Grho_s, Rat(1, 4)), qs)[0]
q_needed_star = sp.solve(sp.Eq((1 / (qs * cands["R*"])) ** 2 / Grho_s, Rat(1, 4)), qs)[0]
print(f"   needed q: R_c = q R_H -> q = {sp.simplify(q_needed_H)};  R_c = q R_S -> q = {sp.simplify(q_needed_S)};  R_c = q R* -> q = {q_needed_star}")
chk("R_c = q R* needs q = 2 (rational, but R* is not a physical horizon: it is c/sqrt(G rho_L), the dimensional-analysis length); R_c = q R_H needs q = Z (transcendental), R_c = q R_S needs q = sqrt(8 pi)",
    q_needed_star == 2 and simplify(q_needed_H - sqrt(32 * pi / 3)) == 0 and simplify(q_needed_S - sqrt(8 * pi)) == 0 and (q_needed_H.is_algebraic is False) and (q_needed_S.is_algebraic is False))
print("   => the only cutoff of the form (rational) x (a length built from G rho_L alone) that works is R* itself with q = 2; R* is the length the puzzle is about, so this is the puzzle restated.")

print("\n== M5: closure + Rindler cutoff with a general gravito-electric coupling factor g (Sciama's coefficient 1 is a premise) ==")
gg = symbols('g', positive=True)
# closure: 2 pi g G rho R_c^2 = c^2 with R_c = c^2/a0  =>  a0^2/(G rho c^2) = 2 pi g
a0sq_over_Grho = sp.simplify(2 * pi * gg)
a0_sol = sp.solve(sp.Eq(2 * pi * gg * Gr * (1 / a0) ** 2, 1), a0)[0]
chk("closure I = 1 with the kernel cutoff at the Rindler distance c^2/a0 gives a0^2/(G rho c^2) = 2 pi g", zero(a0_sol ** 2 / Gr - 2 * pi * gg))
g_needed = sp.solve(sp.Eq(2 * pi * gg, Rat(1, 4)), gg)[0]
chk("the puzzle (a0^2/(G rho c^2) = 1/4) needs g = 1/(8 pi): the coupling of the vector potential would have to be G/(8 pi)", zero(g_needed - 1 / (8 * pi)))
chk("no rational g reproduces it (pi-class): 2 pi g = 1/4 needs g irrational; the fixed cutoff R_c = c^2/a0 is the only place a0 enters",
    g_needed.is_rational is False and all(abs(float(2 * pi * Rat(p, q)) - 0.25) > 1e-6 for p in range(1, 40) for q in range(1, 200)))
ctrl("mutation: g = 1 (Sciama) reproduces 1/4", abs(float(2 * pi) - 0.25) < 1e-6)
print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
