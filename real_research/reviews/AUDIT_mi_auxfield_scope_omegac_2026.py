#!/usr/bin/env python3
r"""AUDIT_mi_auxfield_scope_omegac_2026.py -- SCOPE AUDIT of mi_auxfield_exact_circular_2026.py (15/15, exit 0).

WHAT IS BEING AUDITED. That script localizes the nonlocal MI law (A1 einbein for the square root, A2 Prony/ODE for
the memory), solves the circular orbit exactly (B: chi = [C I - S J] a), and concludes
  (C) the (v/c)^2 suppression is EXACT and "kernel-independent", 1/C = 8.9e6 at the MW, inside 3.8e5-3.8e7;
  (D) the closure additionally HID a quadrature torque S/C = Omega/w_c ~ 3e3 that "no causal memory can remove";
  (E) the one escape is a memory acting on invariants, which is inert on circular orbits.
Its arithmetic is correct. This audit tests its SCOPE, and finds the reach overstated in five places.

THE CENTRAL DEFECT. Every number in C and D is a function of ONE imposed quantity, w_c = a0/c = 3.12e-19 rad/s
(memory time 101 Gyr). The script fixes it in one unlabelled line (l.167, `wcv = A0["canonical"]/C_L`), and its
"kernel-independence" test (C4) varies the kernel SHAPE at that same fixed w_c -- so it cannot see the parameter
that actually carries the result. The corpus's own committed scripts carry w_c FIVE ORDERS LARGER:
  * real_research/reviews/mi_kernel_axis_separation_omegac_2026.py:63-68 -- the paper's committed window
    OMEGA_C_LO = 1.7824e-14 (= 3 x OMEGA_GAL, from Re G >= 0.90 at the binding galactic orbit UGC05721 inner),
    OMEGA_C_HI = 2.2113e-14 (canon) / 1.8306e-14 (alt), the LLR Gdot/G ceiling -- and that script's own verdict is
    "omega_c IS NOT REDUNDANT" (l.527): it is a FREE FIFTH CONSTANT, not fixed to a0/c.
  * real_research/reviews/route_b_memory_time_2026.py:23,199 -- Route B sets omega_c = a0/v_rel, and its S2 proves
    the circular identity FORCES c out of tau_mem (p = 0 exactly), leaving an infinite-dimensional family.
Re G in those scripts IS this script's C, and Im G IS its S. So the corpus has already committed a NON-EMPTY window
in which C >= 0.90 at a galaxy with 6.4x the Milky Way's orbital frequency, and in which the quadrature term is not
a discovery but the window's UPPER edge (the LLR drift bound). This audit re-derives both, and prices the escapes.

CHECKS. A1-A3 the w_c dependence, both footings. B1-B3 three explicit kernels that defeat D's theorem inside its
own causal linear-convolution class. C1-C2 the finite-past defect in A2/E2/E3 (memory time 101 Gyr vs a 13.8 Gyr
worldline). D1 the E1 check is a tautology; D2 the real embedding verification it should have done. E1-E2 the
system-dependence of 1/C and the corpus's own restatement of the 3.8e5-3.8e7 window.

NOT A CLAIM THAT THE FRAMEWORK IS CLOSED, and not a claim the audited script is wrong: its arithmetic reproduces
the committed 2026-08-01 action no-go independently at the ACTION's OWN forced corner w_c = a0/2c, which is
evidence. What fails is the universal quantifier. kappa = 1/2 is FITTED, NOT DERIVED.

Exit 0 = every check held. No check(True): every condition below can fail.
"""
from __future__ import annotations

import math
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 50

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


C_L = 2.99792458e8
A0 = {"canonical": 9.3614e-11, "ALT": 1.13e-10}
KPC = 3.0856775814913673e19
GYR = 3.1557e16
Z_FW = float(2 * sp.sqrt(8 * sp.pi / 3))          # 5.78881

# committed corpus values, quoted with provenance
OMEGA_C_LO = 1.7824e-14      # mi_kernel_axis_separation_omegac_2026.py:66  (3 x OMEGA_GAL, Re G >= 0.90)
OMEGA_C_HI_C = 2.2113e-14    # :67  LLR Gdot/G ceiling, canon
OMEGA_C_HI_A = 1.8306e-14    # :68  LLR Gdot/G ceiling, alt
OMEGA_GAL = 5.9414e-15       # :63  UGC05721 innermost V/r -- the BINDING galactic orbit

# Milky Way, exactly as the audited script uses it
V_MW, R_MW = 233.1e3, 8.122 * KPC
OM_MW = V_MW / R_MW
G_MW = V_MW**2 / R_MW


def C_of(wc, Om):
    return 1.0 / (1.0 + (Om / wc) ** 2)


def SoverC(wc, Om):
    return Om / wc


banner("A  THE RESULT IS A FUNCTION OF w_c ALONE -- and the corpus's own w_c gives C of order unity")

H_LAM = A0["canonical"] * Z_FW / C_L                       # c H_Lambda = Z a0  ->  H_Lambda
H0 = 2.1972e-18                                            # h = 0.6736, 67.36 km/s/Mpc
SQRT_G_RHO = H_LAM * math.sqrt(3.0 / (8.0 * math.pi))      # sqrt(G rho_Lambda) = H_Lambda sqrt(3/8pi)
CAND = [
    ("a0/c   (the audited choice)", A0["canonical"] / C_L, "imposed at l.167; = H_Lambda/Z"),
    ("a0/2c  (action's own corner)", A0["canonical"] / (2 * C_L), "axis_separation:91, tau_mem = 2c/a0"),
    ("H_Lambda", H_LAM, "raw dS correlator corner, dsunruh_tau_mem.py:92"),
    ("sqrt(G rho_Lambda)", SQRT_G_RHO, "inverse dS dynamical time"),
    ("H_0", H0, "Hubble rate today"),
    ("a0/v_rel  (Route B)", A0["canonical"] / V_MW, "route_b_memory_time_2026.py:23"),
    ("sqrt(a0/R)  (MOND dyn.)", math.sqrt(A0["canonical"] / R_MW), "local dynamical frequency"),
    ("OMEGA_C_LO (committed)", OMEGA_C_LO, "axis_separation:66, Re G >= 0.90"),
    ("OMEGA_C_HI canon (committed)", OMEGA_C_HI_C, "axis_separation:67, LLR ceiling"),
    ("OMEGA_C_HI alt (committed)", OMEGA_C_HI_A, "axis_separation:68, LLR ceiling"),
]
print(f"  Milky Way: v = {V_MW/1e3:.1f} km/s, R = {R_MW/KPC:.3f} kpc, Omega = {OM_MW:.4e} rad/s, "
      f"g_obs/a0 = {G_MW/A0['canonical']:.3f}")
print(f"\n  {'w_c choice':<30}{'w_c (rad/s)':>13}{'tau_mem':>12}{'Omega/w_c':>12}{'C(MW)':>12}{'S/C(MW)':>11}"
      f"{'1/C':>11}")
print("  " + "-" * 101)
tab = {}
for nm, wc, prov in CAND:
    Cv, sc = C_of(wc, OM_MW), SoverC(wc, OM_MW)
    tau = 1.0 / wc / GYR
    tau_s = f"{tau:.3g} Gyr" if tau >= 1e-3 else f"{tau*1e3:.3g} Myr"
    tab[nm] = (wc, Cv, sc)
    print(f"  {nm:<30}{wc:>13.4e}{tau_s:>12}{sc:>12.3e}{Cv:>12.4e}{sc:>11.3e}{1/Cv:>11.3e}")
    print(f"      provenance: {prov}")

C_lo = C_of(OMEGA_C_LO, OM_MW)
C_hi = C_of(OMEGA_C_HI_C, OM_MW)
C_audited = C_of(A0["canonical"] / C_L, OM_MW)
check(C_lo > 0.9 and C_hi > 0.9 and C_audited < 1e-6 and (C_lo / C_audited) > 1e6,
      f"A1 *** THE HEADLINE IS A STATEMENT ABOUT ONE IMPOSED CONSTANT, NOT ABOUT NONLOCAL MI. *** At the corpus's "
      f"OWN committed window edges -- OMEGA_C_LO = {OMEGA_C_LO:.4e} and OMEGA_C_HI = {OMEGA_C_HI_C:.4e} rad/s, "
      f"mi_kernel_axis_separation_omegac_2026.py:66-67, the paper's Sec 5.2 window -- the Milky Way has "
      f"C = {C_lo:.4f} and {C_hi:.4f}, i.e. NO SUPPRESSION AT ALL, against the audited script's "
      f"C = {C_audited:.3e}. The ratio is {C_lo/C_audited:.2e}. The audited script fixes w_c = a0/c in one "
      f"unlabelled line and never states that the corpus carries w_c five orders larger")
# the committed window's LOWER edge is DEFINED by Re G >= 0.90 at the binding galactic orbit
C_bind = C_of(OMEGA_C_LO, OMEGA_GAL)
check(abs(C_bind - 0.9) < 0.02 and OMEGA_GAL / OM_MW > 6.0,
      f"A2 and the window's lower edge is DEFINED by exactly the quantity the audited script computes: "
      f"OMEGA_C_LO = 3 x OMEGA_GAL gives C = {C_bind:.4f} >= 0.90 at UGC05721's innermost orbit "
      f"Omega_gal = {OMEGA_GAL:.4e}, which is {OMEGA_GAL/OM_MW:.2f}x the Milky Way's. So the corpus has a COMMITTED "
      f"NON-EMPTY window whose defining property is C = O(1) at the WORST galaxy, and the audited script's C4 "
      f"declares the opposite conclusion 'kernel-independent' without citing it. Re G in the window scripts IS "
      f"this script's C and Im G IS its S -- the same two objects, opposite verdicts, both committed")
# Route B: c is forced OUT, so no (v/c) can appear at all
u_sym, v_sym, a0_sym, Om_sym, c_sym = sp.symbols("u v a_0 Omega c", positive=True)
ratio_routeB = sp.simplify((Om_sym / (a0_sym / v_sym)))       # Omega/w_c with w_c = a0/v
check(sp.simplify(ratio_routeB - Om_sym * v_sym / a0_sym) == 0 and c_sym not in ratio_routeB.free_symbols
      and abs(tab["a0/v_rel  (Route B)"][2] - G_MW / A0["canonical"]) / (G_MW / A0["canonical"]) < 1e-12,
      f"A3 Route B (route_b_memory_time_2026.py:23, committed) removes the factor of c ALGEBRAICALLY, not "
      f"numerically: with w_c = a0/v one has Omega/w_c = Omega v/a0 = g_obs/a0 = {G_MW/A0['canonical']:.4f} "
      f"exactly (verified to 1e-12), c ABSENT from the expression. C = {tab['a0/v_rel  (Route B)'][1]:.4f} and "
      f"S/C = {tab['a0/v_rel  (Route B)'][2]:.4f} -- order unity, not 1e-7 and 3e3. That script's S2 further "
      f"proves the circular identity FORCES p = 0 (c excluded) over ALL monomials tau = c^p v^q a0^s r^t Omega^m, "
      f"leaving an infinite-dimensional family. *** The (v/c)^2 is a PROPERTY OF THE CHOICE w_c ∝ a0/c ***")
for fn, a0v in A0.items():
    print(f"  footing {fn:<10}: audited w_c = {a0v/C_L:.4e} -> C = {C_of(a0v/C_L, OM_MW):.4e};  "
          f"Route B w_c = {a0v/V_MW:.4e} -> C = {C_of(a0v/V_MW, OM_MW):.4f};  "
          f"committed LO -> C = {C_of(OMEGA_C_LO, OM_MW):.4f}")
check(C_of(A0["ALT"] / V_MW, OM_MW) > 0.1 and C_of(A0["ALT"] / C_L, OM_MW) < 1e-6,
      f"A3b and the fork is footing-INDEPENDENT: on the ALT footing the audited choice still gives "
      f"C = {C_of(A0['ALT']/C_L, OM_MW):.3e} while Route B gives C = {C_of(A0['ALT']/V_MW, OM_MW):.4f}. Both "
      f"footings, same conclusion: the six orders live in w_c, not in a0")


banner("A4  PROOF OF IDENTIFICATION -- C *IS* the corpus's Re G, to the paper's own published digits")

G_N, M_SUN, AU = 6.674e-11, 1.989e30, 1.495978707e11
print(f"  the paper's Sec 5.4, quoted in mi_kernel_axis_separation_omegac_2026.py:462: the gate leaves")
print(f"  '<= 6.2% of the MOND boost at <= 20 kAU, 0.8% at 10 kAU'. Computing THIS script's C there:")
print(f"  {'sep':>8}{'Omega (rad/s)':>15}{'C at LO':>11}{'C at HI':>11}{'S/C at LO':>11}")
wb = {}
for kau in (10, 20, 30):
    sep = kau * 1e3 * AU
    Om = math.sqrt(G_N * 2 * M_SUN / sep**3)
    wb[kau] = (C_of(OMEGA_C_LO, Om), C_of(OMEGA_C_HI_C, Om), SoverC(OMEGA_C_LO, Om))
    print(f"  {kau:>5} kAU{Om:>15.4e}{wb[kau][0]:>11.4f}{wb[kau][1]:>11.4f}{wb[kau][2]:>11.2f}")
check(wb[20][1] <= 0.062 and wb[20][0] > 0.02 and 0.004 <= wb[10][1] <= 0.008,
      f"A4 *** C IS Re G. NOT AN ANALOGY -- THE SAME NUMBERS. *** At the committed window edges this script's "
      f"C is {100*wb[20][0]:.1f}-{100*wb[20][1]:.1f}% at 20 kAU and {100*wb[10][0]:.2f}-{100*wb[10][1]:.2f}% at "
      f"10 kAU, reproducing the paper's own published gate suppression '<= 6.2% at <= 20 kAU, 0.8% at 10 kAU' "
      f"(axis_separation:462). So the audited script's C and the corpus's Re G are ONE OBJECT, and the corpus's "
      f"committed window is TUNED on it: pass galaxies (C >= 0.90), suppress wide binaries (C ~ 0.03). The audited "
      f"script computes the same quantity, at a w_c five orders away, and reports the opposite verdict for galaxies "
      f"without citing the window. Note also S/C = {wb[20][2]:.1f} at 20 kAU -- the quadrature term is O(1)-O(10) "
      f"exactly in the DR4 registered 2-30 kAU band, which is where a memory IS detectable, not 3e3 at galaxies")


banner("B  D'S THEOREM IS TRUE BUT ITS QUANTIFIER IS NOT -- three explicit escapes inside the same class")

# B1. a TIME-SYMMETRIC (half-advanced) kernel has S == 0 IDENTICALLY, at every frequency.
s_, wcs, Oms = sp.symbols("s omega_c Omega", positive=True)
# sympy cannot integrate Abs over the whole line; split the two halves and map the negative one by s -> -t
t_ = sp.Symbol("t", positive=True)
S_pos = sp.integrate(sp.Rational(1, 2) * wcs * sp.exp(-wcs * s_) * sp.sin(Oms * s_), (s_, 0, sp.oo))
S_neg = sp.integrate(sp.Rational(1, 2) * wcs * sp.exp(-wcs * t_) * sp.sin(-Oms * t_), (t_, 0, sp.oo))
S_sym = sp.simplify(S_pos + S_neg)
C_sym = sp.simplify(sp.integrate(sp.Rational(1, 2) * wcs * sp.exp(-wcs * s_) * sp.cos(Oms * s_), (s_, 0, sp.oo)) * 2)
norm_sym = sp.simplify(2 * sp.integrate(sp.Rational(1, 2) * wcs * sp.exp(-wcs * s_), (s_, 0, sp.oo)))
print(f"  time-symmetric kernel K = (w_c/2) e^(-w_c|s|):  int K = {norm_sym},  S = S+ + S- = "
      f"({sp.simplify(S_pos)}) + ({sp.simplify(S_neg)}) = {S_sym},  C = {C_sym}")
check(S_sym == 0 and sp.simplify(S_pos) != 0 and norm_sym == 1
      and sp.simplify(C_sym - wcs**2 / (wcs**2 + Oms**2)) == 0,
      f"B1 *** ESCAPE 1: a TIME-SYMMETRIC kernel has S == 0 at EVERY frequency, exactly. *** int K = 1 and "
      f"S = {S_sym} identically by oddness of sin, while C = w_c^2/(w_c^2+Omega^2) is unchanged -- and the "
      f"cancellation is between two INDIVIDUALLY NONZERO halves (S+ = {sp.simplify(S_pos)}), so it is not an "
      f"empty integral. "
      f"D's theorem derives S's isolated zeros from ANALYTICITY IN THE UPPER HALF PLANE, i.e. from CAUSALITY -- so "
      f"it excludes half-advanced/half-retarded memory BY HYPOTHESIS, and Wheeler-Feynman/Machian inertia is "
      f"exactly the tradition that uses it (Sciama 1953). The torque is removable; the suppression is not. "
      f"D's 'no causal memory can remove it' is right, 'no memory' is not")

# B2. a POSITIVE, normalised, CAUSAL kernel with S = 0 EXACTLY and |C| -> 1: a bump at half the orbital period.
wb = sp.Symbol("w", positive=True)
Kbox = 1 / (2 * wb)                       # uniform on [pi/Omega - w, pi/Omega + w]
lo, hi = sp.pi / Oms - wb, sp.pi / Oms + wb
S_bump = sp.simplify(sp.integrate(Kbox * sp.sin(Oms * s_), (s_, lo, hi)))
C_bump = sp.simplify(sp.integrate(Kbox * sp.cos(Oms * s_), (s_, lo, hi)))
n_bump = sp.simplify(sp.integrate(Kbox, (s_, lo, hi)))
lim_C = sp.limit(C_bump, wb, 0)
print(f"  positive bump on [pi/Omega - w, pi/Omega + w]:  int K = {n_bump},  S = {S_bump},  C = {C_bump},  "
      f"C(w->0) = {lim_C}")
check(S_bump == 0 and n_bump == 1 and lim_C == -1,
      f"B2 *** ESCAPE 2: a POSITIVE, normalised, strictly CAUSAL kernel with S = 0 EXACTLY and |C| = 1. *** A bump "
      f"centred at HALF the orbital period, s = pi/Omega, gives S = {S_bump} identically (sin is antisymmetric "
      f"about Omega s = pi) and C -> {lim_C} as the width shrinks: full amplitude, zero torque, no suppression. "
      f"It evades D because its SCALE IS SET BY Omega -- a state-dependent kernel is a FUNCTIONAL of the "
      f"trajectory, so S is a single NUMBER, not a function of Omega, and D's 'S = 0 on an interval' premise never "
      f"arises. Price: C = -1 flips the sign of the dressed acceleration, which G must absorb")

# B3. a SIGNED causal kernel, FIXED scale in the phase variable, with S = 0 and C = 2.
Kp = -4 * sp.exp(-s_) + 10 * sp.exp(-2 * s_)          # in units Omega = 1
n_p = sp.simplify(sp.integrate(Kp, (s_, 0, sp.oo)))
C_p = sp.simplify(sp.integrate(Kp * sp.cos(s_), (s_, 0, sp.oo)))
S_p = sp.simplify(sp.integrate(Kp * sp.sin(s_), (s_, 0, sp.oo)))
print(f"  signed 2-exponential K = -4e^-s + 10e^-2s (phase units):  int K = {n_p},  C = {C_p},  S = {S_p}")
check(n_p == 1 and S_p == 0 and C_p == 2,
      f"B3 ESCAPE 3: an explicit SIGNED causal 2-pole kernel with int K = {n_p}, S = {S_p} EXACTLY and C = {C_p} -- "
      f"an isolated zero of S is all that is needed once the kernel's scale is the orbital phase. Price, stated "
      f"against interest: a signed measure is NOT Herglotz-Nevanlinna, so this one costs the MI action's own "
      f"||K|| <= 1 positivity, and C = 2 > 1 amplifies. B2 is the cleaner escape; this one shows the zero is not "
      f"even hard to hit")

# B4. a SCALE-FREE (power-law) memory: S/C is Omega-INDEPENDENT, so one tuning works for ALL galaxies.
p = sp.Symbol("p", positive=True)
SoC_pl = sp.tan((1 - p) * sp.pi / 2)
vals = [(0.5, float(SoC_pl.subs(p, sp.Rational(1, 2)))), (0.9, float(SoC_pl.subs(p, sp.Rational(9, 10)))),
        (0.99, float(SoC_pl.subs(p, sp.Rational(99, 100))))]
print(f"  power-law memory K ~ s^-p:  int_0^inf s^-p e^(i Omega s) ds = Gamma(1-p) Omega^(p-1) e^(i(1-p)pi/2)")
for pv, r in vals:
    print(f"    p = {pv:<5} -> S/C = tan((1-p)pi/2) = {r:.4f}   (Omega-INDEPENDENT)")
check(sp.diff(SoC_pl, Oms) == 0 and vals[2][1] < 0.02 and vals[0][1] > 0.9,
      f"B4 and a SCALE-FREE memory K ~ s^-p makes S/C = tan((1-p)pi/2) EXACTLY Omega-INDEPENDENT "
      f"(d/dOmega = {sp.diff(SoC_pl, Oms)}), so ONE kernel exponent suppresses the torque at EVERY galaxy "
      f"simultaneously -- {vals[2][1]:.4f} at p = 0.99 -- which is precisely what D's 'galaxies span a continuous "
      f"range of Omega' argument assumes impossible. A scale-free kernel has NO w_c, hence no (v/c) either, and it "
      f"is exactly the STRONGLY-NONLOCAL class: it has no finite Prony sum, so A2's localization cannot represent "
      f"it. Milgrom 1994 Ann.Phys. 229:384 App.A (citation debt #8 in reviews/mi_action_programme_close_2026.py) "
      f"proves MOND MI must live THERE and 'cannot even be a limit of a sequence of local, higher-derivative "
      f"theories' -- i.e. A2's own construction is inside the class the corpus already cites as excluded")


banner("C  THE FINITE PAST -- A2/E2/E3 assume a 101 Gyr memory on a 13.8 Gyr worldline")

wc_aud = A0["canonical"] / C_L
tau_mem = 1.0 / wc_aud
T_UNI = 13.797 * GYR
T_GAL = 10.0 * GYR
# hazard: 1 - exp(-x) at x ~ 4e-3 -- use expm1
gain_uni = -math.expm1(-wc_aud * T_UNI)
gain_gal = -math.expm1(-wc_aud * T_GAL)
gain_mp = float(-mp.expm1(-mp.mpf(wc_aud) * mp.mpf(T_UNI)))
print(f"  audited w_c = {wc_aud:.4e} rad/s  ->  tau_mem = 1/w_c = {tau_mem/GYR:.1f} Gyr")
print(f"  DC gain actually available on a worldline of age T:  int_0^T K ds = -expm1(-w_c T)")
print(f"    T = 13.797 Gyr (age of the universe): {gain_uni:.6e}   [mpmath 50-digit: {gain_mp:.6e}]")
print(f"    T = 10 Gyr (galaxy formation):        {gain_gal:.6e}")
check(abs(gain_uni / gain_mp - 1) < 1e-9 and 0.10 < gain_uni < 0.15 and tau_mem / GYR > 90,
      f"C1 A2's convolution and E2/E3's 'unit gain at DC' both run the memory from tau = -infinity, but "
      f"tau_mem = {tau_mem/GYR:.0f} Gyr is {tau_mem/T_UNI:.1f}x the age of the universe. The DC gain a real "
      f"worldline can accumulate is int_0^T K = {gain_uni:.4f}, i.e. {1/gain_uni:.1f}x SMALLER than the 1 that "
      f"E2/E3 use. So E3's 'the collapse is exact, not approximate' is wrong by {1/gain_uni:.1f}x, not by orders: "
      f"stated AGAINST MY OWN FIRST ESTIMATE, which had w_c T = 4e-3 and a 230x defect -- the true product is "
      f"w_c T = {wc_aud*T_UNI:.4f}. The defect is real but modest, and E's escape survives it. (expm1 used; agrees "
      f"with mpmath at 50 digits to 1e-9, so this is not the 1-exp(-x) underflow that has bitten this corpus)")
# the homogeneous mode is FROZEN, so chi is dominated by initial data, not by the kernel's response
decay = math.exp(-wc_aud * T_UNI)
check(decay > 0.85 and C_audited < decay * 1e-6,
      f"C2 and the same number cuts BOTH ways, against the no-go as well: A2's ODE chi' + w_c chi = w_c a has "
      f"homogeneous solution chi_0 e^(-w_c tau), which retains {100*decay:.2f}% of its initial value over the "
      f"whole age of the universe. Since the particular (rotating) solution has amplitude C = {C_audited:.3e}, "
      f"chi is dominated by FROZEN INITIAL DATA by {decay/C_audited:.2e}x -- an essentially free constant vector "
      f"per system. So at w_c = a0/c the law is not 'suppressed', it is INITIAL-DATA-DOMINATED and ill-posed as a "
      f"predictive law, which is a different and stronger objection than the one the script makes. The steady-state "
      f"premise of B and C is inconsistent with the memory time C assumes")


banner("D  E1 IS A TAUTOLOGICAL CHECK -- and here is the verification it should have run")

# reproduce the audited E1 exactly and show its condition cannot fail
A_, h_, R_, w_, tau_ = sp.symbols("A h R w tau", positive=True)
a5sq_asserted = A_**2 * h_**4 + R_**2 * w_**4
cond_a = sp.diff(a5sq_asserted, tau_) == 0 and not a5sq_asserted.has(tau_)
junk = sp.Symbol("q_totally_unrelated", positive=True) ** 7 + 3       # any tau-free expression
cond_junk = sp.diff(junk, tau_) == 0 and not junk.has(tau_)
print(f"  audited E1's condition on its own asserted expression: {cond_a}")
print(f"  the SAME condition on an unrelated tau-free expression q^7 + 3: {cond_junk}")
check(cond_a and cond_junk,
      f"D1 *** E1 IS A CHECK THAT CANNOT FAIL. *** It writes a5^2 = A^2 h^4 + R^2 w^4 in symbols that contain no "
      f"tau, then verifies that this tau-free expression has no tau in it. The identical condition passes on "
      f"'q^7 + 3'. Nothing about the de Sitter worldline is tested: the embedding is never differentiated, and the "
      f"constraint A^2 h^2 - R^2 w^2 = 1 quoted in the docstring is never imposed. This is the third instance of "
      f"the defect class the file's own docstring says it avoided ('two such were caught before release')")
# the real verification: build the embedded helix WITH tau in it and differentiate
Hs = sp.Symbol("H", positive=True)
X = sp.Matrix([A_ * sp.sinh(h_ * tau_), A_ * sp.cosh(h_ * tau_), R_ * sp.cos(w_ * tau_), R_ * sp.sin(w_ * tau_),
               sp.Symbol("X4", positive=True)])
eta5 = sp.diag(-1, 1, 1, 1, 1)
U = sp.diff(X, tau_)
Acc = sp.diff(X, tau_, 2)
uu = sp.simplify((U.T * eta5 * U)[0, 0])
a5 = sp.simplify((Acc.T * eta5 * Acc)[0, 0])
print(f"  embedded helix X(tau): u.u = {uu}  (must be -1: gives the constraint A^2h^2 - R^2w^2 = 1)")
print(f"  a5.a5 = {a5};  d/dtau = {sp.simplify(sp.diff(a5, tau_))}")
check(sp.simplify(uu + A_**2 * h_**2 - R_**2 * w_**2) == 0 and sp.simplify(a5 - a5sq_asserted) == 0
      and sp.simplify(sp.diff(a5, tau_)) == 0,
      f"D2 DONE PROPERLY, the physics CLAIM IS TRUE: differentiating the actual embedded helix "
      f"X = (A sinh h tau, A cosh h tau, R cos w tau, R sin w tau, X4) gives u.u = {uu} -- so u.u = -1 IS the "
      f"constraint A^2h^2 - R^2w^2 = 1 -- and a5.a5 = {a5} = A^2 h^4 + R^2 w^4 with d/dtau = 0 exactly. So E1's "
      f"conclusion survives while its check does not. (It is also not special to de Sitter: any orbit of a Killing "
      f"vector has constant |a|, flat space included, where |a| = gamma^2 v^2/R.) A true claim behind a vacuous "
      f"check still has to be re-verified, and a false-labelled check SUPPRESSES -- the corpus's own lesson from "
      f"the alpha=1 class audit")


banner("E  1/C IS NOT A NUMBER, IT IS A FUNCTION OF THE SYSTEM -- and the window it 'confirms' was restated")

SYS = [("Milky Way (R0)", 233.1e3, 8.122 * KPC), ("big spiral outskirt", 200e3, 30.0 * KPC),
       ("dwarf (DDO-like)", 30e3, 2.0 * KPC), ("UGC05721 innermost", None, None),
       ("Earth's orbit", 29.78e3, 1.495978707e11), ("Moon about Earth", 1.022e3, 3.844e8)]
print(f"  {'system':<24}{'Omega (rad/s)':>15}{'g/a0':>12}{'1/C at w_c=a0/c':>18}{'in 3.8e5-3.8e7?':>18}")
print("  " + "-" * 88)
invs = {}
for nm, v, R in SYS:
    Om = OMEGA_GAL if v is None else v / R
    g = None if v is None else v * v / R
    iv = 1.0 + (Om / wc_aud) ** 2
    invs[nm] = iv
    gs = "n/a" if g is None else f"{g/A0['canonical']:.3e}"
    print(f"  {nm:<24}{Om:>15.4e}{gs:>12}{iv:>18.4e}{'YES' if 3.8e5 <= iv <= 3.8e7 else 'NO':>18}")
check(invs["Earth's orbit"] > 3.8e7 * 1e10 and invs["Moon about Earth"] > 3.8e7
      and 3.8e5 <= invs["Milky Way (R0)"] <= 3.8e7,
      f"E1 C2's 'lands INSIDE the corpus's committed window, which validates both routes' is a MILKY-WAY-ONLY "
      f"statement. 1/C is not a constant of the theory: at Earth's orbit -- where the SAME law must hold -- it is "
      f"{invs[chr(69)+chr(97)+chr(114)+chr(116)+chr(104)+chr(39)+chr(115)+' orbit']:.3e}, "
      f"{invs[chr(69)+chr(97)+chr(114)+chr(116)+chr(104)+chr(39)+chr(115)+' orbit']/3.8e7:.2e}x ABOVE the window's "
      f"top, and at the Moon {invs['Moon about Earth']:.3e}. Two routes 'agreeing' on a system-dependent quantity "
      f"that spans 17 orders across the systems in scope is not cross-validation -- the window is 100x wide and the "
      f"MW was the system used to build it")
# the window itself was restated by the corpus TWO DAYS BEFORE
kin_frac = V_MW**2 / (2 * C_L**2)
rescaled = invs["Milky Way (R0)"] * kin_frac
check(abs(kin_frac - 3.02e-7) / 3.02e-7 < 0.02 and rescaled < 10,
      f"E2 and the 3.8e5-3.8e7 window C2 appeals to was RESTATED by the corpus's own committed "
      f"reviews/mi_action_programme_close_2026.py:57-65 (C1a, 2026-08-02): 'the published 3.8e5-3.8e7 overstates "
      f"the wall by ~6.5 orders and must be restated', because an inertia modification must be measured against "
      f"the KINETIC term v^2/2c^2 = {kin_frac:.3e}, not the rest mass. Applying that same rescaling to this "
      f"script's own number gives 1/C x v^2/2c^2 = {rescaled:.2f} -- order unity, not six orders. So C2 confirms "
      f"agreement with a figure the corpus corrected two days earlier, and the correction, applied consistently, "
      f"moves the audited wall to O(1) as well. C2's conclusion 'validates both' is stale in both directions")


banner("F  THE AUDITED SCRIPT IS WRITTEN AGAINST A KERNEL RETIRED TWO DAYS EARLIER")

ys = sp.Symbol("y", positive=True)
nu_a1 = sp.sqrt(1 + 1 / ys)                                  # the a0-line, alpha = 1 (RETIRED)
nu_rA = 1 / (1 - sp.exp(-sp.sqrt(ys)))                       # Route A, IN FORCE since 2026-08-02 (STANDING.md:31-33)
dex = [(yv, abs(float(sp.log(nu_rA.subs(ys, yv) / nu_a1.subs(ys, yv), 10)))) for yv in (0.1, 1, 10)]
print(f"  a0-line (alpha=1, retired):  nu = {nu_a1};   Route A (in force): nu = {nu_rA}")
for yv, d in dex:
    print(f"    y = g_bar/a0 = {yv:<5} nu_alpha1 = {float(nu_a1.subs(ys, yv)):.4f}, "
          f"nu_RouteA = {float(nu_rA.subs(ys, yv)):.4f}  ->  {d:.4f} dex apart")
check(max(d for _, d in dex) > 0.03 and sp.simplify(nu_rA - nu_a1) != 0,
      f"F1 A1b's 'the localized law still reproduces the framework's EXACT a_0-line g_obs^2 = g_bar^2 + a_0 g_bar' "
      f"is the RETIRED alpha=1 kernel. The kernel IN FORCE since 2026-08-02 is Route A's exponential "
      f"nu = 1/(1-exp(-sqrt(y))) (STANDING.md:28-36, mi_route_a_kernel.py), and the two differ by up to "
      f"{max(d for _, d in dex):.4f} dex over y = 0.1-10 -- so the a_0-line is not the law, and the word 'exact' "
      f"is the unlabelled alpha=1 claim the corpus's own alpha=1-exclusive class audit exists to catch")
# and the einbein does NOT polynomialize Route A: exp(lambda) is not polynomial in lambda
lam_s, Xs = sp.symbols("lambda X", positive=True)
einbein = Xs / (2 * lam_s) + lam_s / 2
is_poly_sqrt = sp.Poly(einbein * 2 * lam_s, lam_s).degree() == 2
rA_of_lam = 1 - sp.exp(-lam_s)                                # what A1 would have to polynomialize for Route A
check(is_poly_sqrt and not rA_of_lam.is_polynomial(lam_s),
      f"F2 and A1's selling point does not carry: the einbein makes sqrt(X) POLYNOMIAL (degree "
      f"{sp.Poly(einbein*2*lam_s, lam_s).degree()} in lambda after clearing 2 lambda), but Route A's law is "
      f"transcendental in the acceleration -- 1 - exp(-lambda) is_polynomial = "
      f"{rA_of_lam.is_polynomial(lam_s)} -- so one auxiliary scalar does NOT polynomialize the kernel in force. "
      f"A1 localizes the RETIRED law. Also noted, in the audited script's favour: STANDING.md:56 already says 'the "
      f"2026-08-01 no-goes on the MI action stand: what has a healthy variational home is the KERNEL, not MI', and "
      f"Route A is a modified-GRAVITY (Bekenstein-Milgrom) realisation -- so the audited script re-closes a door "
      f"the corpus had already stepped away from. That is redundancy, not contradiction")


banner("RESULT")
n = sum(1 for c_, _ in ok if c_)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c_, m_ in ok:
        if not c_:
            print(f"    - {m_}")
    sys.exit(1)
print("""  Exit 0.  VERDICT, both ways.

  WHAT SURVIVES, and it is real: at the ACTION's own forced corner w_c = a0/2c the suppression and the quadrature
  term are exact, kernel-SHAPE-independent, and reproduce the committed 2026-08-01 (v/c)^2 no-go by an independent
  route. The A1 einbein and the A2 Prony localization are correct mathematics. E1's physics claim is true (verified
  here from the embedding, which the script did not do). That is genuine, and the reproduction is evidence.

  WHAT DOES NOT SURVIVE is the reach:
   1. Every number in C and D is a function of the single imposed constant w_c = a0/c. The corpus's OWN committed
      window (axis_separation:66-68) sits five orders higher and is DEFINED by C >= 0.90 at the binding galaxy;
      Route B (route_b:23,199) forces c out of tau_mem entirely. Both are committed; neither is cited.
   2. 'No causal memory can remove the torque' is right; 'no memory can' is not. Three explicit counterexamples
      here: time-symmetric (S == 0 at every frequency), a positive causal bump at half the orbital period
      (S = 0, |C| = 1), a signed 2-pole (S = 0, C = 2). A scale-free kernel makes S/C Omega-INDEPENDENT, defeating
      the 'galaxies span a range of Omega' step -- and that is the strongly-nonlocal class Milgrom 1994 says MOND
      MI must inhabit, which A2's Prony localization structurally cannot represent.
   3. The quadrature term is not a discovery: Im G is the corpus's LLR drift term and it already SETS the
      committed window's upper edge. It was priced, and the window came out non-empty.
   4. A2/E2/E3 assume an infinite past for a 101 Gyr memory. On a real 13.8 Gyr worldline the DC gain is 0.127
      (8x, not orders -- my own first estimate of 230x was wrong and is withdrawn here), so E3's word 'exact' is
      wrong but the escape survives. The sharper half of the same fact: the frozen homogeneous mode retains 87% of
      its initial value over cosmic time and dominates the rotating part of chi by 7.7e6x, so at w_c = a0/c the law
      is INITIAL-DATA-DOMINATED, not merely suppressed -- which contradicts the steady-state premise of B and C.
   5. E1's check cannot fail, and C2 appeals to a window the corpus restated two days earlier.

  No door is closed here, in either direction. kappa = 1/2 remains FITTED, NOT DERIVED.""")
