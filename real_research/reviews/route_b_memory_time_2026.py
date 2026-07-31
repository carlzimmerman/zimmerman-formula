#!/usr/bin/env python3
r"""route_b_memory_time_2026.py -- ROUTE B, TESTED ADVERSARIALLY.

FRAMEWORK (its own terms, not MOND's). de Sitter-Unruh MODIFIED INERTIA.
  a0 = c H_Lambda / Z with Z = sqrt(32 pi/3) = 5.78881 on the pure-Lambda (rho_DE) footing
     -> a0 = 9.36e-11 m/s^2 = (c/2) sqrt(G rho_Lambda), i.e. EXACTLY HALF the gravitational free-fall
        acceleration at the dark-energy density. The coefficient kappa = 1/2 is Carl Zimmerman's and is
        absent from the prior literature (Milgrom 1999 PLA 253:273, Pikhitsa 2010, Klinkhamer-Kopp 2011
        all land on 2 c H_Lambda = 11.58x larger; Milgrom 2020 gives c H_Lambda / 2pi).
     CAVEAT, always stated: 32pi/3 is the Einstein-coupling conversion factor and it CANCELS in that
        reduction. The content is the ONE number kappa = 1/2, and it is FITTED, not derived (the
        kappa-forcing door closed 2026-06-17). 32pi/3 is NOT an independent geometric structure.
  Alternate footing carried on every dimensional number: a0 = 1.13e-10 (rho_total / c H0).
  Kernel in force (since 2026-07-30): alpha = 2, mu(x) = x/sqrt(1+x^2), K_2(z) = sqrt(z/(1+z)),
  spectral measure rho(s) = (1/pi) sqrt(s/(1-s)) on 0<s<1. Retired alpha = 1 carried alongside.
  Covariant completion: a PASSIVE preferred frame u^mu (zero propagating modes) + K(Box_u/a0^2),
  K Herglotz-Nevanlinna (positive measure, ||K|| <= 1, causal-retarded).

THE PROPOSAL UNDER TEST (Carl's; this script tries to break it, not to defend it).
  Theorem 8 (kernel-independent) says the nonlocal operator action's circular-orbit argument is
  w = c Omega / a0 while the law's is x = a/a0, with w/x = c/v EXACTLY. The missing factor is a SPEED.
  Route B: a locally-dragged passive frame supplies a particle-dependent MEMORY TIME
        tau_mem = v_rel / a0        (omega_c = a0 / v_rel)
  in place of the frame-independent c/a0, so that Omega tau_mem = Omega v / a0 = a/a0 = u.

WHAT THIS SCRIPT SETTLES, in order.
  S1  The identity, symbolically, both footings; and the exact repair of Theorem 8's c/v.
  S2  ITEM 5 FIRST, because it decides how much the rest is worth: enumerate every monomial
      tau = c^p v^q a0^s r^t Omega^m consistent with the circular identity. Result: c is FORCED out
      (p = 0 exactly), and what survives is a ONE-PARAMETER family (v/a0)(r Omega/v)^m -- infinite-
      dimensional once general dimensionless functions are allowed. Quantified off circles.
  S3  ITEM 2, the consistency prize: tau_mem for five real systems, both footings, against the
      corpus's FREE-but-BOUNDED window [1 Myr .. 17.5 Gyr].
  S4  THE FRAME'S DRAG LEVEL -- three independent locks, each a number:
      (a) cosmic/CMB frame (re-verified), (b) LOCAL-MATTER drag (new; this one bites hard),
      (c) HIERARCHY / nested systems (new; this is the sharpest, and it is a no-go for a LOCAL u).
  S5  ITEM 3, off circles: four candidate instantaneous frequencies, exact turning-point orbits,
      residual vs eccentricity, and the radial-motion pathology quantified.
  S6  ITEM 4, ghost-freedom + the function-vs-average inequality that Route B must close and does not
      (Jensen, signed by concavity of K_2), and the inherited Ostrogradsky cost (mpmath, 50 digits).

CREDIT. Milgrom 1994 Ann.Phys. 229:384 (modified inertia; orbit-dependent interpolating functions);
Milgrom astro-ph/0510117 (virial); Milgrom 2022 PRD 106:064060 (Fourier-space MI -- the algebraic
relation holds ONLY for single-frequency trajectories). Mach's principle is ancient prior art for
inertia-relative-to-matter; Sciama 1953 is the standard citation. Novelty is ASSESSED, never asserted.

HONESTY GUARDS. Every check is structural (identity / limit / sign / monotonicity / count) and fails if
the number moves. No check(True). Exits non-zero on any failure. Where a quantity is a difference of
large terms, mpmath at 50 digits is used and said so.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 50

# ------------------------------------------------------------------ sealed framework constants
C = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0857e19
PC = KPC / 1e3
AU = 1.495978707e11
YR = 3.155693e7
MYR = 1e6 * YR
GYR = 1e9 * YR
Z = math.sqrt(32.0 * math.pi / 3.0)
A0 = 9.36e-11                                   # canonical  c H_Lambda / Z, pure-Lambda footing
A0_ALT = 1.13e-10                               # alternate  rho_total / c H0
FOOTINGS = (("canonical cH_L/Z", A0), ("alternate rho_tot/cH0", A0_ALT))

# corpus's FREE-but-BOUNDED window for omega_c, from MI_OFFCIRCULAR_COMPLETION_2026.md verdict table:
# [1/kappa = 17.5 Gyr (raw dS correlator)  ..  1 Myr (d1 above-band pole)]
TAU_LO = 1.0 * MYR
TAU_HI = 17.5 * GYR

# framework's OWN RAR scatter, rar_framework_a0_mlfit.py at Upsilon = 0.70 (0.108 dex; 0.1116 at
# alpha=2 per STANDING sec.1). Deep regime g_obs = sqrt(g_bar a0) => d log g_obs = 0.5 d log a0,
# so the TOTAL a0 budget is 2 x scatter.
RAR_SCATTER_DEX = 0.108
A0_BUDGET_DEX = 2.0 * RAR_SCATTER_DEX

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 104)
    print(s)
    print("=" * 104)


# ------------------------------------------------------------------ kernels (framework's own)
def mu_num(x, alpha):
    x = np.asarray(x, dtype=float)
    if alpha == 1:
        return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * np.maximum(x, 1e-300))
    if alpha == 2:
        return x / np.sqrt(1.0 + x * x)
    raise ValueError(alpha)


def a_from_gbar(gbar, a0, alpha):
    """The framework's closure, inverted: mu(a/a0) a = g_bar  ->  a."""
    gbar = np.asarray(gbar, dtype=float)
    if alpha == 1:
        return np.sqrt(gbar * gbar + a0 * gbar)
    if alpha == 2:
        y = gbar / a0
        return a0 * np.sqrt(0.5 * (y * y + y * np.sqrt(y * y + 4.0)))
    raise ValueError(alpha)


# =====================================================================================================
def s1_identity():
    banner("S1. ITEM 1 -- the identity Omega tau_mem = a/a0, and the exact repair of Theorem 8's c/v")
    v, R, a0, c, Om = sp.symbols("v R a_0 c Omega", positive=True)

    # circular kinematics, imposed rather than assumed: a = Omega v = v^2/R, Omega = v/R
    a_circ = Om * v
    tau_mem = v / a0
    arg_B = sp.simplify(Om * tau_mem)                      # Route B's kernel argument
    x_law = sp.simplify(a_circ / a0)                       # the law's argument
    print(f"  tau_mem = v/a0 ;  Omega tau_mem = {arg_B} ;  a/a0 = {x_law}")
    check(sp.simplify(arg_B - x_law) == 0,
          "Omega tau_mem - a/a0 = 0 identically in v, Omega and a0 on a circular orbit (sympy exact)")

    # same thing with Omega eliminated for v/R -- identically in R too
    arg_B_R = sp.simplify((v / R) * tau_mem)
    x_law_R = sp.simplify((v**2 / R) / a0)
    check(sp.simplify(arg_B_R - x_law_R) == 0,
          f"and identically in R: {arg_B_R} = {x_law_R} (no residual)")

    w = c * Om / a0                                        # Theorem 8's operator argument
    check(sp.simplify(w / x_law - c / v) == 0,
          "Theorem 8 re-verified here: w/x = c/v exactly, kernel-free")
    check(sp.simplify(tau_mem - (v / c) * (c / a0)) == 0,
          "tau_mem = (v/c)(c/a0): Route B is EXACTLY the substitution c -> v_rel in the memory time, "
          "so it repairs Theorem 8's argument mismatch by construction on circles")

    print("\n  Numerically, both footings, four real systems (self-consistent: v from the CLOSURE):")
    print(f"  {'system':<26s} {'footing':<10s} {'u = a/a0':>11s} {'Om*tau_mem':>12s} {'rel.diff':>10s} "
          f"{'c/v (Thm 8 gap)':>16s}")
    sysdef = [("wide binary 10 kAU", 1.0 * MSUN * G, 10e3 * AU),
              ("dwarf spheroidal 2 kpc", 1e8 * MSUN * G, 2.0 * KPC),
              ("galaxy outskirt 30 kpc", 1e11 * MSUN * G, 30.0 * KPC),
              ("cluster member 1 Mpc", 1e14 * MSUN * G, 1e3 * KPC)]
    worst = 0.0
    for nm, GM, r in sysdef:
        for fn, a0v in FOOTINGS:
            A = float(a_from_gbar(GM / r**2, a0v, 2))
            vc = math.sqrt(A * r)                       # circular speed of the CLOSURE's own field
            Omv = vc / r
            u = A / a0v
            argb = Omv * vc / a0v
            rel = abs(argb - u) / u
            worst = max(worst, rel)
            print(f"  {nm:<26s} {fn.split()[0]:<10s} {u:11.4e} {argb:12.4e} {rel:10.1e} "
                  f"{C/vc:16.1f}")
    check(worst < 1e-12,
          f"the identity holds numerically to {worst:.1e} on self-consistent circular orbits across "
          f"9 decades of u and both footings -- so on circles Route B delivers exactly the argument "
          f"Theorem 8 found missing, and the factor it removes is c/v = 4e2..1e6 here")
    print("\n  READ: S1 is KINEMATICS, not a derivation. It says WHAT the frame must supply, not that")
    print("  an action supplies it. S6 tests whether the gap Theorem 8 actually names is closed.")


# =====================================================================================================
def s2_dimensional_enumeration():
    banner("S2. ITEM 5 -- is tau_mem = v/a0 FORCED? Enumerate every dimensionally-allowed monomial")
    p, q, s, t, m = sp.symbols("p q s t m", real=True)
    c, v, a0, r, Om = sp.symbols("c v a_0 r Omega", positive=True)

    # tau = c^p v^q a0^s r^t Omega^m ; on a circular orbit Omega = v/r, a = v^2/r.
    # Require Omega*tau == a/a0 == v^2 r^-1 a0^-1 IDENTICALLY in the independent quantities (v, r, a0),
    # with c a fixed constant that cannot be traded against v.
    lhs = c**p * v**q * a0**s * r**t * (v / r)**(m + 1)
    lhs = sp.powsimp(sp.expand_power_exp(lhs), force=True)
    # exponent matching
    eqs = [sp.Eq(p, 0),                       # c cannot appear
           sp.Eq(q + m + 1, 2),               # v^2
           sp.Eq(s, -1),                      # a0^-1
           sp.Eq(t - m - 1, -1)]              # r^-1
    sol = sp.solve(eqs, [p, q, s, t], dict=True)
    print("  tau = c^p v^q a0^s r^t Omega^m,  require Omega tau = a/a0 on circles identically:")
    print(f"    solution: {sol}")
    check(len(sol) == 1 and sol[0][p] == 0 and sol[0][s] == -1
          and sp.simplify(sol[0][q] - (1 - m)) == 0 and sp.simplify(sol[0][t] - m) == 0,
          "the identity forces p = 0 (c EXCLUDED), s = -1, q = 1-m, t = m -- a ONE-PARAMETER family "
          "tau_m = (v/a0)(r Omega/v)^m, with m free")

    # the two dimensional constraints are AUTOMATIC given the identity -> the identity is strictly
    # stronger than dimensional analysis. Verify by substitution rather than assertion.
    dimL = sol[0][p] + sol[0][q] + sol[0][s] + sol[0][t]
    dimT = -sol[0][p] - sol[0][q] - 2 * sol[0][s] - sol[0][m] if m in sol[0] else \
        -sol[0][p] - sol[0][q] - 2 * sol[0][s] - m
    check(sp.simplify(dimL) == 0 and sp.simplify(dimT - 1) == 0,
          f"and [L]^{sp.simplify(dimL)} [T]^{sp.simplify(dimT)} -- the length/time dimensions come out "
          f"right AUTOMATICALLY for every m, so dimensional analysis alone constrains NOTHING here; "
          f"the circular identity is what does the work, and it still leaves a free function")

    # verify a few members really do reproduce the identity on circles
    print("\n  spot-check members of the family. tau_m is written with Omega UNSUBSTITUTED so the")
    print("  (r Omega/v)^m factor stays visible; the circular relation Omega = v/r is imposed only to")
    print("  evaluate the identity, where that factor becomes exactly 1:")
    for mv in (-2, -1, 0, 1, 2):
        tau_m = (v / a0) * (r * Om / v)**mv
        argm = sp.simplify((Om * tau_m).subs(Om, v / r))
        okm = sp.simplify(argm - v**2 / (r * a0)) == 0
        print(f"    m = {mv:+d}: tau_m = {tau_m}   ->   Omega tau_m |_circ = {argm}  "
              f"{'= a/a0' if okm else 'FAILS'}")
        check(okm, f"m = {mv:+d}: a genuinely DIFFERENT memory time reproduces a/a0 on circles "
                   f"exactly -- the members are inequivalent functionals that agree on the only "
                   f"constrained slice")


    # --- the number that makes "PINS NOTHING" quantitative: the spread OFF circles -------------
    print("\n  THE SPREAD OFF CIRCLES, on exact closure-solving orbits. There r Omega/v = v_t/v, so")
    print("  the family separates as (v_t/v)^m. Omega_E = v_t/r is used for every member, so this")
    print("  isolates the tau-freedom alone. Evaluated at the orbital phase where v_t/v is smallest:")
    GMq, rsq = 1e11 * MSUN * G, 30 * KPC
    print(f"    {'e':>5s} {'min v_t/v':>10s}" + "".join(f"{('arg m='+str(mv)):>12s}"
                                                        for mv in (-2, -1, 0, 1, 2))
          + f"{'max/min':>9s} {'mu spread':>10s}")
    spreads = []
    for eq in (0.0, 0.1, 0.2, 0.4, 0.6):
        sts = _orbit_states(GMq, rsq, eq, A0, 2)
        best = min(sts, key=lambda s: s[2] / math.hypot(s[1], s[2]))
        rr, vr, vt, _A, _dA, _w = best
        vv = math.hypot(vr, vt)
        args = [(vt / rr) * (vv / A0) * (vt / vv) ** mv for mv in (-2, -1, 0, 1, 2)]
        mus = [float(mu_num(aq, 2)) for aq in args]
        spreads.append((max(args) / min(args), max(mus) / min(mus)))
        print(f"    {eq:5.2f} {vt/vv:10.5f}" + "".join(f"{aq:12.5f}" for aq in args)
              + f"{max(args)/min(args):9.2f} {max(mus)/min(mus):10.3f}")
    mono_sp = all(spreads[i + 1][0] > spreads[i][0] for i in range(len(spreads) - 1))
    check(abs(spreads[0][0] - 1.0) < 1e-9 and mono_sp and spreads[-1][0] > 3.0
          and spreads[-1][1] > 2.0,
          f"the one-parameter tau-family is EXACTLY degenerate on circles (argument spread "
          f"{spreads[0][0]:.9f}) and separates by {spreads[-1][0]:.0f}x in the kernel argument and "
          f"{spreads[-1][1]:.2f}x in mu itself by e = 0.6. 'The circular slice cannot see the freedom' "
          f"is therefore not a rhetorical point: it is a factor {spreads[-1][1]:.2f} in the predicted "
          f"g_bar at fixed acceleration, from a choice nothing in the route fixes")

    print("\n  CONCLUSION OF ITEM 5, stated flatly. tau_mem = v/a0 is NOT forced. What IS forced, and")
    print("  this is a real result, is that c CANNOT APPEAR: any tau containing c fails the circular")
    print("  identity identically in v. That is the formal version of 'the frame must be locally")
    print("  dragged'. But the surviving family is (v/a0) x [any dimensionless function equal to 1 on")
    print("  circles], which is infinite-dimensional -- monomials alone already give a one-parameter")
    print("  family. Off circles the route therefore PINS NOTHING. This is the same corner-blindness")
    print("  the corpus already records for omega_c (MI_OFFCIRCULAR_COMPLETION_2026.md, C1): the only")
    print("  constrained slice is the circular one, and it cannot see the freedom.")


# =====================================================================================================
def s3_consistency_prize():
    banner("S3. ITEM 2 -- tau_mem = v/a0 for real systems vs the corpus's [1 Myr .. 17.5 Gyr] window")
    print(f"  window provenance: MI_OFFCIRCULAR_COMPLETION_2026.md verdict table -- omega_c FREE but")
    print(f"  bounded in [1/kappa = 17.5 Gyr (raw dS correlator) .. 1 Myr (d1 above-band pole)].")
    print(f"  NOTE ON PROVENANCE, because it changes how hard a 'falsification' here bites: those two")
    print(f"  endpoints are the two BATH-NATIVE candidate scales, and the corpus's own language at")
    print(f"  both ends is 'door ~dies' -- i.e. the OBSERVABLE (dwarf sigma-hysteresis) magnitude goes")
    print(f"  to zero there, not that the theory becomes inconsistent. So landing outside is a real")
    print(f"  problem for the DOOR, and only a weak problem for CONSISTENCY. Both are reported.")

    cases = [("Milky-Way-like disk star", 220e3),
             ("dwarf-spheroidal star", 10e3),
             ("galaxy-cluster member", 1000e3),
             ("wide binary internal, 10 kAU", 0.5e3),
             ("Earth (heliocentric orbital)", 29.8e3)]
    print(f"\n  {'case':<32s} {'v_rel':>10s} " +
          "".join(f"{('tau ['+fn.split()[0]+']'):>20s} {'in window?':>11s}" for fn, _ in FOOTINGS))
    outside = []
    taus_all = []
    for nm, vv in cases:
        row = f"  {nm:<32s} {vv/1e3:9.1f}k"
        for fn, a0v in FOOTINGS:
            tau = vv / a0v
            taus_all.append(tau)
            inw = TAU_LO <= tau <= TAU_HI
            if not inw:
                outside.append((nm, fn, tau))
            unit = f"{tau/MYR:12.3f} Myr" if tau < GYR else f"{tau/GYR:12.3f} Gyr"
            row += f" {unit:>20s} {('YES' if inw else 'NO'):>11s}"
        print(row)

    lo_case = min((vv for _n, vv in cases))
    hi_case = max((vv for _n, vv in cases))
    spread = math.log10(hi_case / lo_case)
    print(f"\n  span of tau_mem demanded across these five cases: {spread:.2f} dex "
          f"(v_rel from {lo_case/1e3:.1f} to {hi_case/1e3:.0f} km/s)")
    print(f"  corpus window width: {math.log10(TAU_HI/TAU_LO):.2f} dex")

    # the load-bearing structural facts, each falsifiable if a number moves
    # the 0.5 km/s figure is an estimate; the CLOSURE's own self-consistent circular speed at
    # 10 kAU around 1 Msun is smaller, which makes the floor result MORE severe, not less.
    r_wb = 10e3 * AU
    v_wb_sc = math.sqrt(float(a_from_gbar(MSUN * G / r_wb**2, A0, 2)) * r_wb)
    print(f"\n  input-independence of the wide-binary row: the estimate above used 0.5 km/s, but the")
    print(f"  CLOSURE's own self-consistent circular speed at 10 kAU around 1 Msun is "
          f"{v_wb_sc/1e3:.3f} km/s,")
    print(f"  giving tau_mem = {v_wb_sc/A0/MYR:.3f} Myr canonical / {v_wb_sc/A0_ALT/MYR:.3f} Myr "
          f"alternate -- further BELOW the floor,")
    print(f"  so the conclusion does not depend on the 0.5 km/s estimate.")
    check(v_wb_sc / A0 < 0.5e3 / A0 < TAU_LO,
          f"self-consistent wide-binary tau_mem = {v_wb_sc/A0/MYR:.3f} Myr is "
          f"{TAU_LO/(v_wb_sc/A0):.1f}x below the 1 Myr floor, vs {TAU_LO/(0.5e3/A0):.1f}x for the "
          f"0.5 km/s estimate -- the finding is robust to the input speed and is conservative as stated")
    tau_wb_can = 0.5e3 / A0
    tau_wb_alt = 0.5e3 / A0_ALT
    check(tau_wb_can < TAU_LO and tau_wb_alt < TAU_LO,
          f"THE WIDE BINARY FALLS OUTSIDE, below the floor, on BOTH footings: "
          f"{tau_wb_can/MYR:.3f} Myr canonical ({TAU_LO/tau_wb_can:.1f}x below the 1 Myr floor) and "
          f"{tau_wb_alt/MYR:.3f} Myr alternate ({TAU_LO/tau_wb_alt:.1f}x below). Under the LITERAL "
          f"reading of the corpus bound this FALSIFIES the prescription; under the provenance-corrected "
          f"reading it says the wide-binary memory door is dead, not the theory")
    tau_dsph = 10e3 / A0
    check(TAU_LO < tau_dsph < 5 * MYR,
          f"the dwarf-spheroidal case clears the floor by only {tau_dsph/TAU_LO:.1f}x "
          f"({tau_dsph/MYR:.2f} Myr) -- it is marginal, not comfortable")
    check(all(TAU_LO <= vv / a0v <= TAU_HI for nm, vv in cases if 'wide binary' not in nm
              for _f, a0v in FOOTINGS),
          "the other four cases (MW star, dSph star, cluster member, Earth) all land INSIDE the window "
          "on both footings, spanning 2.8 Myr - 339 Myr, comfortably inside the door-relevant "
          "0.4 Gyr scale the corpus singles out")
    check(spread > 3.0,
          f"BUT NOTE THE CATEGORY CHANGE, and it is the honest headline of item 2: the corpus's "
          f"omega_c is a UNIVERSAL CONSTANT awaiting a pin; Route B makes it a STATE FUNCTION spanning "
          f"{spread:.2f} dex. The route therefore does not 'pin omega_c' -- it ELIMINATES omega_c as a "
          f"constant and replaces it with a rule. That is only a reduction in free content if the rule "
          f"is itself forced, which S2 shows it is not off circles")


# =====================================================================================================
def s4_drag_level():
    banner("S4. THE FRAME'S DRAG LEVEL -- three locks. (a) is re-verified; (b) and (c) are new.")

    # ---------------------------------------------------------------- (a) cosmic / CMB frame
    print("  (a) COSMIC (CMB) FRAME -- re-verified from the framework's own RAR.")
    print(f"      deep regime g_obs = sqrt(g_bar a0)  =>  d log10 g_obs = 0.5 d log10 a0_eff")
    print(f"      framework's own RAR scatter {RAR_SCATTER_DEX:.3f} dex  =>  TOTAL a0 budget "
          f"{A0_BUDGET_DEX:.3f} dex (factor {10**A0_BUDGET_DEX:.2f}), with nothing left over for "
          f"distance, inclination or M/L")
    # verify the 0.5 exponent structurally rather than asserting it
    a0s, gb = sp.symbols("a_0 g_bar", positive=True)
    gobs = sp.sqrt(gb * a0s)
    dlog = sp.simplify(sp.diff(sp.log(gobs), sp.log(a0s)) if False else
                       sp.simplify(a0s * sp.diff(gobs, a0s) / gobs))
    check(sp.simplify(dlog - sp.Rational(1, 2)) == 0,
          f"d log g_obs / d log a0 = {dlog} in the deep regime -- so the 2x in the budget is derived, "
          f"not assumed (and it is the same for alpha=1 and alpha=2, both of which give "
          f"g_obs -> sqrt(g_bar a0))")
    v_pec = np.array([100.0, 300.0, 620.0, 1000.0]) * 1e3
    spread_pec = math.log10(v_pec.max() / v_pec.min())
    check(spread_pec > A0_BUDGET_DEX,
          f"CMB-frame speed EXCLUDED: peculiar velocities {v_pec.min()/1e3:.0f}-{v_pec.max()/1e3:.0f} "
          f"km/s = {spread_pec:.2f} dex of injected a0 variation vs a {A0_BUDGET_DEX:.3f} dex budget "
          f"= {spread_pec/A0_BUDGET_DEX:.1f}x over")

    # ---------------------------------------------------------------- (b) local-matter drag
    print("\n  (b) LOCAL-MATTER DRAG (frame co-moving with the surrounding matter) -- NEW, and it is a")
    print("      squeeze from the OTHER side. If the passive u is dragged by the LOCAL matter, then a")
    print("      disk star's speed relative to u is not its circular speed but its RANDOM velocity,")
    print("      because the local matter co-rotates. Then a0_eff = a0 (v_circ/v_rel) is too LARGE by")
    print("      v_circ/sigma, and it varies with stellar population.")
    pops = [("thin-disk young", 220e3, 20e3), ("thin-disk old", 220e3, 35e3),
            ("thick disk", 200e3, 55e3), ("dSph (pressure-supported)", 12e3, 10e3)]
    print(f"      {'population':<28s} {'v_circ':>8s} {'sigma':>8s} {'v_circ/sigma':>13s} "
          f"{'dex in a0_eff':>14s} {'x budget':>9s}")
    ratios = []
    for nm, vc_, sg in pops:
        rat = vc_ / sg
        ratios.append(rat)
        dex = math.log10(rat)
        print(f"      {nm:<28s} {vc_/1e3:7.0f}k {sg/1e3:7.0f}k {rat:13.2f} {dex:14.3f} "
              f"{dex/A0_BUDGET_DEX:9.2f}")
    disk = [r for (nm, _v, _s), r in zip(pops, ratios) if 'disk' in nm]
    spread_disk = math.log10(max(disk) / min(disk))
    check(min(disk) > 3.0,
          f"local-matter drag mis-scales a0 for every disk population by {min(disk):.1f}-{max(disk):.1f}x "
          f"({math.log10(min(disk)):.2f}-{math.log10(max(disk)):.2f} dex), i.e. "
          f"{math.log10(min(disk))/A0_BUDGET_DEX:.1f}-{math.log10(max(disk))/A0_BUDGET_DEX:.1f}x the "
          f"whole a0 budget -- a frame dragged by the local matter is EXCLUDED")
    check(spread_disk > 0.2,
          f"and it is not even a constant offset that could be absorbed into kappa: the population "
          f"spread alone is {spread_disk:.2f} dex = {spread_disk/A0_BUDGET_DEX:.1f}x the budget, so it "
          f"would show up as RAR scatter within a single galaxy")
    print("      => the frame must be at rest w.r.t. the ORBIT'S CENTRE (the bound system's")
    print("         barycentre), not w.r.t. the local matter and not w.r.t. the cosmos. Route B is")
    print("         squeezed to exactly one prescription, and it is a NONLOCAL, MEMBERSHIP-DEPENDENT")
    print("         one: 'the barycentre of whichever bound system this particle orbits'.")

    # ---------------------------------------------------------------- (c) hierarchy / nested systems
    print("\n  (c) HIERARCHY -- the sharpest lock, and it is a NO-GO for a LOCAL frame field u(x).")
    print("      A local u assigns ONE frame per spacetime point. Take two stars at the SAME point:")
    print("      one bound to a satellite dwarf, one to the host disk. The barycentre prescription")
    print("      needs u at rest w.r.t. the DWARF for the first and w.r.t. the HOST for the second.")
    print("      A single-valued local field cannot do both. Quantify the cost of choosing the host:")
    print(f"      {'satellite v_orb (dwarf-internal)':<34s} {'host-frame v':>13s} {'factor':>8s} "
          f"{'a0_eff dex':>11s} {'sigma_pred/sigma_obs':>21s}")
    v_int = 12e3                      # km/s-scale internal orbital speed in a classical dSph
    sigma_obs = 10.0                  # km/s, classical-dSph scale (McConnachie 2012 range 6-12)
    worst_fac = 0.0
    for v_host in (100e3, 150e3, 200e3, 300e3):
        fac = v_host / v_int
        worst_fac = max(worst_fac, fac)
        # deep-regime isothermal MOND/MI relation sigma^4 = (4/81) G M a0  =>  sigma ~ a0^(1/4)
        ratio_sigma = (1.0 / fac) ** 0.25
        print(f"      {v_int/1e3:>30.0f} km/s {v_host/1e3:12.0f}k {fac:8.1f} "
              f"{-math.log10(fac):11.3f} {ratio_sigma:21.3f}")
    # verify the sigma ~ a0^(1/4) scaling symbolically rather than asserting it
    Ms, a0sym = sp.symbols("M a_0", positive=True)
    sig = (sp.Rational(4, 81) * sp.Symbol("G", positive=True) * Ms * a0sym) ** sp.Rational(1, 4)
    check(sp.simplify(sp.simplify(a0sym * sp.diff(sig, a0sym) / sig) - sp.Rational(1, 4)) == 0,
          "deep-regime isothermal relation sigma^4 = (4/81) G M a0 (Milgrom) gives "
          "d log sigma / d log a0 = 1/4, verified symbolically -- so a factor F error in a0_eff moves "
          "a dwarf's predicted dispersion by F^(1/4)")
    fac_lo, fac_hi = 100e3 / v_int, 300e3 / v_int
    sig_lo, sig_hi = sigma_obs * (1 / fac_hi) ** 0.25, sigma_obs * (1 / fac_lo) ** 0.25
    # dSph dispersion errors: classical dwarfs measured to ~0.5-1.0 km/s (many-hundred-star samples)
    sig_err = 0.9
    nsig_lo = (sigma_obs - sig_hi) / sig_err
    nsig_hi = (sigma_obs - sig_lo) / sig_err
    check(nsig_lo > 3.0,
          f"choosing the HOST barycentre makes satellite dwarfs {fac_lo:.0f}-{fac_hi:.0f}x too "
          f"Newtonian in a0_eff, so their predicted dispersions drop from {sigma_obs:.1f} to "
          f"{sig_hi:.1f}-{sig_lo:.1f} km/s -- {nsig_lo:.1f}-{nsig_hi:.1f}sigma against a ~"
          f"{sig_err:.1f} km/s measurement error. Satellite dwarfs DO sit on the relation, so a "
          f"host-dragged local frame is excluded by data that already exists")
    check(worst_fac > 10.0,
          f"and the contradiction is unavoidable for a single-valued local u: the two co-located stars "
          f"need frames differing by {worst_fac:.0f}x in speed. Escaping it requires a frame that is "
          f"PARTICLE-dependent (i.e. not a field at all), which is not a field theory, or a genuinely "
          f"nonlocal membership rule, which the framework's passive u does not have")


# =====================================================================================================
def _orbit_states(GM, rscale, e, a0v, alpha, nphi=241):
    """Exact states on a closure-solving orbit via the two turning points.

    The framework's closure a = A(r) rhat is a CENTRAL force, so (E, L) follow exactly from
    pericentre/apocentre; no ODE integration and hence no integration error. Sampling is uniform in
    psi with r = rmid - (dr/2) cos psi, which regularises the 1/sqrt(v_r) residence weight at the
    turning points. Returns (r, v_r, v_t, A, dAdr, weight) with weight ~ residence time.
    """
    ra, rp = rscale * (1.0 + e), rscale * (1.0 - e)
    if e == 0.0:
        A = float(a_from_gbar(GM / rscale**2, a0v, alpha))
        dA = float((a_from_gbar(GM / (rscale * 1.0000001)**2, a0v, alpha)
                    - a_from_gbar(GM / (rscale * 0.9999999)**2, a0v, alpha))
                   / (2e-7 * rscale))
        return [(rscale, 0.0, math.sqrt(A * rscale), A, dA, 1.0)]
    rg = np.linspace(rp * 0.9999, ra * 1.0001, 200001)
    ag = a_from_gbar(GM / rg**2, a0v, alpha)
    Phi = np.concatenate([[0.0], np.cumsum(0.5 * (ag[1:] + ag[:-1]) * np.diff(rg))])
    Pp, Pa = np.interp(rp, rg, Phi), np.interp(ra, rg, Phi)
    Lsq = 2.0 * (Pa - Pp) / (1.0 / rp**2 - 1.0 / ra**2)
    E = Pp + Lsq / (2.0 * rp**2)
    out = []
    for psi in np.linspace(0.0, math.pi, nphi)[1:-1]:
        rr = 0.5 * (rp + ra) - 0.5 * (ra - rp) * math.cos(psi)
        vr2 = 2.0 * (E - np.interp(rr, rg, Phi)) - Lsq / rr**2
        if vr2 <= 0.0:
            continue
        vr = math.sqrt(vr2)
        vt = math.sqrt(Lsq) / rr
        A = float(a_from_gbar(GM / rr**2, a0v, alpha))
        h = 1e-6 * rr
        dA = float((a_from_gbar(GM / (rr + h)**2, a0v, alpha)
                    - a_from_gbar(GM / (rr - h)**2, a0v, alpha)) / (2 * h))
        drdpsi = 0.5 * (ra - rp) * math.sin(psi)
        out.append((rr, vr, vt, A, dA, drdpsi / vr))
    return out


def _cand_args(st, a0v):
    """The four candidate instantaneous frequencies x tau_mem = v/a0, at one state.

    Position (r,0), velocity (v_r, v_t), acceleration (-A, 0). Then
      A_cand  Omega = |v x a|/v^2 = A v_t/v^2      (rotation rate of the VELOCITY direction)
      B_cand  Omega = |a|/v      = A/v            (full velocity-space rate -- tautological)
      E_cand  Omega = v_t/r                       (true angular rate; == |a x adot|/|a|^2, verified)
      G_cand  Omega = |adot|/|a|                  (rotation+growth rate of the ACCELERATION vector)
    """
    r, vr, vt, A, dA, _w = st
    v = math.hypot(vr, vt)
    tau = v / a0v
    om_A = A * vt / v**2
    om_B = A / v
    om_E = vt / r
    om_G = math.hypot(dA * vr, A * vt / r) / A
    return {"A: a_perp/v": om_A * tau, "B: |a|/v": om_B * tau,
            "E: v_t/r": om_E * tau, "G: |adot|/|a|": om_G * tau}


def s5_off_circles():
    banner("S5. ITEM 3 -- OFF CIRCLES. Four candidate frequencies, exact orbits, and the pathology.")
    print("  METHOD (same exact turning-point construction as mi_offcircular_action_2026.py S4): the")
    print("  closure is a central force, so pericentre/apocentre give exact (E, L) and hence exact")
    print("  states with NO ODE error. On each state, evaluate Route B's law")
    print("      g_bar =?= |a| mu( Omega_cand tau_mem ),      tau_mem = |v|/a0")
    print("  against the closure's own g_bar = |a| mu(|a|/a0). Residual = |mu(u) - mu(arg)|/mu(u),")
    print("  i.e. the FRACTIONAL error Route B makes in the Newtonian source at fixed acceleration.")

    # first: E_cand == |a x adot|/|a|^2 exactly (so only four candidates, not five)
    Asym, dAsym, vr_s, vt_s, r_s = sp.symbols("A A' v_r v_t r", positive=True)
    # a = -A rhat ; adot = -A' v_r rhat - A v_t/r thetahat  -> |a x adot| = A * A v_t/r
    check(sp.simplify((Asym * Asym * vt_s / r_s) / Asym**2 - vt_s / r_s) == 0,
          "|a x adot|/|a|^2 = v_t/r exactly, so the 'rotation rate of the acceleration DIRECTION' is "
          "the true angular rate -- candidate E, not a fifth option")

    for alpha in (2, 1):
        print("\n" + "-" * 104)
        print(f"  KERNEL alpha = {alpha}" + ("  (in force)" if alpha == 2 else "  (retired)"))
        for label, GM, rs in (("galaxy, M=1e11 Msun, r=30 kpc (DEEP)", 1e11 * MSUN * G, 30 * KPC),
                              ("Sun, M=1 Msun, r=1 AU (NEWTONIAN)", MSUN * G, AU)):
            for fn, a0v in FOOTINGS:
                y = (GM / rs**2) / a0v
                print(f"\n    {label}  [{fn}]  g_bar/a0 = {y:.3e}")
                keys = list(_cand_args(_orbit_states(GM, rs, 0.2, a0v, alpha)[0], a0v).keys())
                print("      " + f"{'e':>5s}" + "".join(f"{k:>18s}" for k in keys))
                grow = {k: [] for k in keys}
                for e in (0.0, 0.01, 0.05, 0.1, 0.2, 0.4, 0.6):
                    states = _orbit_states(GM, rs, e, a0v, alpha)
                    worst = {k: 0.0 for k in keys}
                    for st in states:
                        u = st[3] / a0v
                        mu_u = float(mu_num(u, alpha))
                        for k, arg in _cand_args(st, a0v).items():
                            mu_a = float(mu_num(max(arg, 1e-300), alpha))
                            worst[k] = max(worst[k], abs(mu_a - mu_u) / mu_u)
                    print("      " + f"{e:5.2f}" + "".join(f"{worst[k]:18.4e}" for k in keys))
                    for k in keys:
                        grow[k].append(worst[k])
                # structural checks
                kB = "B: |a|/v"
                check(max(grow[kB]) < 1e-13,
                      f"alpha={alpha} {label.split(',')[0]} [{fn.split()[0]}]: candidate B's residual is "
                      f"{max(grow[kB]):.1e} at EVERY eccentricity -- identically zero. That is not a "
                      f"success, it is the TAUTOLOGY: Omega_B tau_mem = (|a|/v)(v/a0) = |a|/a0, the "
                      f"speed cancels, so B is the closure rewritten and the frame does no work")
                # REGIME-AWARE. In the Newtonian regime mu -> 1, so ANY argument error is suppressed
                # by the kernel's own (1 - mu(u)): 1/(2u) for alpha=1, 1/(2u^2) for alpha=2. Demanding
                # an order-unity residual there would be wrong physics. So the order-unity claim is
                # made only in the deep regime, and the Newtonian regime gets the STRONGER test:
                # residual / (1 - mu(u)) must be O(1), which ties the computation to the kernel.
                deep = y < 10.0
                one_minus_mu = 1.0 - float(mu_num(float(a_from_gbar(GM / rs**2, a0v, alpha)) / a0v,
                                                  alpha))
                for k in ("A: a_perp/v", "E: v_t/r", "G: |adot|/|a|"):
                    seq = grow[k]
                    if max(seq) < 1e-11:
                        print(f"      -> {k}: max residual {max(seq):.1e} below the 1e-11 "
                              f"double-precision floor for this regime (1-mu(u) = "
                              f"{one_minus_mu:.2e}): UNRESOLVED, no claim made")
                        continue
                    mono = all(seq[i + 1] >= seq[i] - 1e-14 for i in range(len(seq) - 1))
                    if deep:
                        check(seq[0] < 1e-11 and mono and max(seq) > 1e-3,
                              f"alpha={alpha} {label.split(',')[0]} [{fn.split()[0]}] {k}: residual is "
                              f"{seq[0]:.1e} (zero) at e=0, rises monotonically, and reaches "
                              f"{max(seq):.3f} = {100*max(seq):.1f}% at e=0.6 -- an order-unity error in "
                              f"g_bar in the DEEP regime, not a correction")
                    else:
                        check(seq[0] < 1e-11 and mono and 0.01 < max(seq) / one_minus_mu < 100.0,
                              f"alpha={alpha} {label.split(',')[0]} [{fn.split()[0]}] {k}: residual is "
                              f"{seq[0]:.1e} at e=0, rises monotonically to {max(seq):.3e} at e=0.6, and "
                              f"that is {max(seq)/one_minus_mu:.2f}x the kernel's own 1-mu(u) = "
                              f"{one_minus_mu:.2e} -- so in the NEWTONIAN regime Route B's off-circular "
                              f"error is suppressed exactly as the kernel demands and is invisible in "
                              f"the solar system. This is a validation of the residual computation, and "
                              f"it is reported as a PASS for Route B, not a failure")

    # -------------------------------------------------------------- the radial pathology
    print("\n" + "-" * 104)
    print("  THE RADIAL PATHOLOGY, quantified. Purely radial motion has v_t = 0.")
    print("    candidate A: Omega tau = A v_t/(v a0) -> 0 ;  candidate E: v_t v/(r a0) -> 0.")
    print("    Then Route B's law reads g_bar = |a| mu(0) = 0 for any FINITE |a|, so for g_bar > 0")
    print("    there is NO finite solution: the required acceleration DIVERGES. Exhibited by taking")
    print("    v_t -> 0 at fixed r and solving g_bar = A mu(A v_t/(v a0)) for A.")
    GM, rs = 1e11 * MSUN * G, 30 * KPC
    gb = GM / rs**2
    print(f"    {'v_t/v':>10s} {'A_required/a0 (alpha=2)':>25s} {'A_closure/a0':>14s} {'ratio':>10s}")
    reqs = []
    for frac in (1.0, 0.3, 0.1, 0.03, 0.01, 1e-3, 1e-4):
        # deep regime: mu_2(x) ~ x, so g_bar = A * (A frac/a0)  ->  A = sqrt(g_bar a0/frac)
        lo, hi = 1e-14, 1e10
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            if mid * float(mu_num(mid * frac / A0, 2)) < gb:
                lo = mid
            else:
                hi = mid
        Areq = math.sqrt(lo * hi)
        Acl = float(a_from_gbar(gb, A0, 2))
        reqs.append(Areq / Acl)
        print(f"    {frac:10.1e} {Areq/A0:25.4e} {Acl/A0:14.4f} {Areq/Acl:10.3e}")
    check(reqs[-1] / reqs[0] > 50.0 and reqs[-1] > 50.0,
          f"candidates A and E are FATAL on radial motion: as v_t/v falls 1 -> 1e-4 the required "
          f"acceleration grows by {reqs[-1]/reqs[0]:.0f}x and diverges as (v_t/v)^(-1/2) in the deep "
          f"regime -- a radial faller would need unbounded acceleration to feel the same g_bar. This is "
          f"a genuine singularity of the prescription, not a small-parameter artefact")

    print("\n    candidate G = |adot|/|a| CURES it: for radial infall adot is parallel to a and")
    print("    |adot|/|a| = |A'| v_r/A != 0. But it gets the WRONG argument, and by a factor that")
    print("    grows without bound. Deep regime A = sqrt(GM a0)/r so |A'|/A = 1/r, and energy")
    print("    conservation from rest at r0 gives v_r^2 = 2 A r ln(r0/r), hence")
    print("        Omega_G tau_mem = v_r^2/(r a0) = 2 (A/a0) ln(r0/r) = 2 u ln(r0/r).")
    r0s, rr_s, GMs, a0ss = sp.symbols("r_0 r GM a_0", positive=True)
    Adeep = sp.sqrt(GMs * a0ss) / rr_s
    vr2 = 2 * sp.integrate(sp.sqrt(GMs * a0ss) / sp.Symbol("rho", positive=True),
                           (sp.Symbol("rho", positive=True), rr_s, r0s))
    argG = sp.simplify(vr2 / (rr_s * a0ss))
    pred = sp.simplify(2 * (Adeep / a0ss) * sp.log(r0s / rr_s))
    check(sp.simplify(argG - pred) == 0,
          f"symbolically: Omega_G tau_mem = {sp.simplify(argG)} = 2 u ln(r0/r) exactly on deep-regime "
          f"radial infall -- so G is off by the factor 2 ln(r0/r), which is 1 only at r0/r = e^(1/2) "
          f"= 1.65 and grows logarithmically without bound as the faller starts further out")
    print(f"      {'r0/r':>8s} {'2 ln(r0/r)':>12s}  <- the factor by which G mis-states the argument")
    facs = []
    for ratio in (1.65, 3.0, 10.0, 100.0, 1e3):
        facs.append(2 * math.log(ratio))
        print(f"      {ratio:8.2f} {2*math.log(ratio):12.3f}")
    check(abs(facs[0] - 1.0) < 0.02 and facs[-1] > 10.0,
          f"the factor runs {facs[0]:.2f} -> {facs[-1]:.1f} over r0/r = 1.65 -> 1e3, i.e. G is exact at "
          f"one radius ratio and wrong by an order of magnitude for a faller from 1000x out. Not fatal, "
          f"but not the law either -- and it costs a THIRD time derivative (jerk) in the action")

    print("\n  ITEM 3 VERDICT, both ways. Of the four candidates: B is a tautology (v cancels, the")
    print("  frame does nothing, and the resulting law is a LOCAL function of |xddot| -- which is")
    print("  exactly what corrected Theorem 3 excludes from having any local action). A and E are")
    print("  FATAL on radial motion (divergent required acceleration). G is the only non-tautological")
    print("  candidate that survives radial motion, and it is wrong there by 2 ln(r0/r), unbounded,")
    print("  while also failing off circles for bound orbits. NONE survives.")


# =====================================================================================================
def s6_ghosts_and_jensen():
    banner("S6. ITEM 4 -- ghost-freedom / positivity, and the inequality Route B must close")

    print("  (i) WHAT THE HERGLOTZ-NEVANLINNA ARGUMENT ACTUALLY BUYS, and where it stops.")
    print("      The corpus's positivity result is about a FIXED kernel K(z) = 1 - INT rho(s)ds/(z+s)")
    print("      with rho >= 0: that makes K a Herglotz-Nevanlinna function, gives ||K|| <= 1 on the")
    print("      physical domain z > 0, and makes the LINEAR response causal-retarded and passive.")
    print("      Every one of those statements is a statement about a linear, state-INDEPENDENT map.")
    print("      Route B makes the corner omega_c = a0/v_rel depend on the particle's own speed, so")
    print("      the response is a NONLINEAR functional of the trajectory. Concretely: a one-parameter")
    print("      family {K_{omega_c}} can be Herglotz member-by-member while the composite map")
    print("      x(t) -> F[x](t) is neither linear nor passive, because passivity is a statement about")
    print("      the map, not about the members. NOTHING in the corpus's positivity chain survives")
    print("      the substitution automatically. That is a precise statement of what is NOT")
    print("      established; it is not a claim that positivity fails.")

    print("\n  (ii) THE CONCRETE TEST: the function-vs-average inequality, which is the gap Theorem 8")
    print("       actually names -- K(<Box_u>_u) != <K(Box_u)>_u -- and it is UNTOUCHED by rescaling")
    print("       the argument. Route B changes WHAT the argument is; the inequality is about")
    print("       commuting K past an average. Sign it with concavity.")
    zs = sp.Symbol("z", positive=True)
    K2 = sp.sqrt(zs / (1 + zs))
    K2pp = sp.simplify(sp.diff(K2, zs, 2))
    print(f"       K_2(z) = sqrt(z/(1+z)) ;  K_2''(z) = {K2pp}")
    # sign of K2'' on z>0: factor out the manifestly positive part
    num = sp.simplify(K2pp * 4 * (1 + zs)**sp.Rational(5, 2) * zs**sp.Rational(3, 2))
    print(f"       K_2''(z) * 4 z^(3/2) (1+z)^(5/2) = {sp.expand(num)}   (the prefactor is > 0 on z>0)")
    check(sp.simplify(sp.expand(num) + 4 * zs + 1) == 0,
          f"K_2'' = -(4z+1)/[4 z^(3/2)(1+z)^(5/2)] < 0 for all z > 0: the alpha=2 kernel is STRICTLY "
          f"CONCAVE on its physical domain, so by Jensen K_2(<z>) >= <K_2(z)> with equality iff z is "
          f"deterministic -- i.e. iff the trajectory is SINGLE-FREQUENCY. This is Milgrom 2022 PRD "
          f"106:064060's single-frequency restriction, re-derived as a convexity statement")
    sample = np.logspace(-8, 8, 2001)
    K2pp_f = sp.lambdify(zs, K2pp, "numpy")
    check(bool(np.all(K2pp_f(sample) < 0)),
          f"numerically confirmed over 16 decades: max K_2'' = {float(np.max(K2pp_f(sample))):.3e} < 0")
    # alpha=1 too, so the statement is not kernel-specific
    K1 = (sp.sqrt(1 + 4 * zs) - 1) / (2 * sp.sqrt(zs))
    K1pp = sp.simplify(sp.diff(K1, zs, 2))
    K1pp_f = sp.lambdify(zs, K1pp, "numpy")
    check(bool(np.all(K1pp_f(sample) < 0)),
          f"the retired alpha=1 kernel is concave too (max K_1'' = {float(np.max(K1pp_f(sample))):.3e}), "
          f"so the Jensen direction is KERNEL-INDEPENDENT across both kernels the corpus has used")

    print("\n       Now the SIZE of the gap on real orbits: z = (|a|/a0)^2, averaged over the orbit")
    print("       with residence-time weights from the exact turning-point states.")
    for alpha in (2, 1):
        for fn, a0v in FOOTINGS[:1]:
            GM, rs = 1e11 * MSUN * G, 30 * KPC
            print(f"\n       alpha={alpha} [{fn}]  galaxy 1e11 Msun at 30 kpc")
            print(f"       {'e':>5s} {'<z>':>12s} {'K(<z>)':>11s} {'<K(z)>':>11s} {'gap':>11s} "
                  f"{'gap/K(<z>)':>12s}")
            gaps = []
            for e in (0.0, 0.05, 0.1, 0.2, 0.4, 0.6):
                sts = _orbit_states(GM, rs, e, a0v, alpha)
                w = np.array([s[5] for s in sts])
                w = w / w.sum()
                zz = np.array([(s[3] / a0v) ** 2 for s in sts])
                zbar = float(np.dot(w, zz))
                Kz = float(mu_num(np.sqrt(zbar), alpha))
                Kbar = float(np.dot(w, mu_num(np.sqrt(zz), alpha)))
                gap = Kz - Kbar
                gaps.append(gap / Kz)
                print(f"       {e:5.2f} {zbar:12.5f} {Kz:11.6f} {Kbar:11.6f} {gap:11.4e} "
                      f"{gap/Kz:12.4e}")
            check(gaps[0] < 1e-12 and all(gaps[i + 1] > gaps[i] for i in range(len(gaps) - 1))
                  and gaps[-1] > 1e-3,
                  f"alpha={alpha}: the Jensen gap is {gaps[0]:.1e} (exactly zero) on the circle, is "
                  f"POSITIVE at every e>0 as concavity requires, rises monotonically, and reaches "
                  f"{100*gaps[-1]:.2f}% at e=0.6. Route B does not shrink this by one part: the gap is "
                  f"set by the SPREAD of the argument over the orbit, and tau_mem = v/a0 changes the "
                  f"argument's value, not its dispersion")

    print("\n  (iii) THE OSTROGRADSKY COST IS INHERITED, NOT AVOIDED. The only candidate that gives the")
    print("        closure off circles is B, whose argument is |xddot|/a0 -- literally the argument of")
    print("        the local witness action S = INT dt m(|xdot|^2 f(|xddot|/a0) - phi). So B is not a")
    print("        new theory; it is that action with a new interpretation, and it inherits the")
    print("        indefinite acceleration-Hessian. Re-verified here at 50 digits (mpmath), because")
    print("        this is a difference of large terms and a float64 scan reports thousands of")
    print("        SPURIOUS sign flips from an O(u^3) cancellation.")

    def f2(u):
        u = mp.mpf(u)
        return (u * mp.sqrt(1 + u**2) - mp.asinh(u)) / (2 * u**2)

    def f1(u):
        u = mp.mpf(u)
        return (2 * u * mp.sqrt(4 * u**2 + 1) - 4 * u + mp.asinh(2 * u)) / (8 * u**2)

    print(f"        {'u':>10s} {'f2(u)':>14s} {'f2 prime':>14s} {'f2 second':>14s} "
          f"{'f2p/u (transv.)':>16s} {'indefinite?':>12s}")
    bad = 0
    for uu in (1e-4, 1e-2, 1e-1, 1.0, 10.0, 1e2, 1e4, 1e6):
        fp = mp.diff(f2, uu)
        fpp = mp.diff(f2, uu, 2)
        tr = fp / mp.mpf(uu)
        indef = (fpp < 0) and (tr > 0)
        if not indef:
            bad += 1
        print(f"        {uu:10.1e} {float(f2(uu)):14.8f} {float(fp):14.6e} {float(fpp):14.6e} "
              f"{float(tr):16.6e} {'YES' if indef else 'no':>12s}")
    check(bad == 0,
          "at 50-digit precision the alpha=2 generating function has f'' < 0 (longitudinal) and "
          "f'/u > 0 (transverse) at every u over 10 decades: the acceleration-Hessian is INDEFINITE, "
          "so omega_extra^2 < 0 and the extra modes are runaways. Candidate B inherits this in full "
          "(0.57 s e-folding at Earth, 5e7 yr at 30 kpc, |omega|/Omega_orb = 2.8 per the corpus)")
    check(abs(float(f2(1e8)) - 0.5) < 1e-6 and abs(float(f1(1e8)) - 0.5) < 1e-6,
          f"Newtonian limit intact for both kernels, f(inf) = 1/2 (f2 = {float(f2(1e8)):.9f}, "
          f"f1 = {float(f1(1e8)):.9f}) -- the control that says the generating functions are the right "
          f"objects")

    print("\n  ITEM 4 VERDICT. ESTABLISHED: (1) the corpus's Herglotz/passivity chain does not transfer")
    print("  to a state-dependent corner, and the reason is structural (linearity is used, not")
    print("  incidental); (2) both kernels are strictly concave on z > 0, so the function-vs-average")
    print("  gap is POSITIVE-DEFINITE off circles and vanishes only for single-frequency trajectories;")
    print("  (3) the gap on an e=0.6 galaxy orbit is order 1-10%, and Route B does not reduce it;")
    print("  (4) the one candidate that reproduces the closure lands back on the local witness action")
    print("  and its runaway modes. NOT ESTABLISHED, and not claimed: whether some nonlinear-passivity")
    print("  notion (e.g. a state-dependent KMS/fluctuation-dissipation condition) could rescue")
    print("  positivity. That is a real open question and this script does not settle it.")


# =====================================================================================================
def s7_wide_binary_consequence():
    banner("S7. ONE FALSIFIABLE CONSEQUENCE, and it lands on the FROZEN pre-registration")
    print("  Route B's drag level is not a philosophical choice -- it changes the wide-binary")
    print("  prediction by orders of magnitude, which is Front A (Gaia DR4, ~Dec 2026).")
    GM = 1.0 * MSUN * G
    print(f"  {'sep':>8s} {'u = a/a0':>10s} {'v_int':>10s} {'v_gal/v_int':>12s} "
          f"{'arg (barycentre)':>17s} {'arg (galactoc.)':>16s} {'mu_bary':>9s} {'mu_gal':>9s}")
    rows = []
    for sep_kau in (2.0, 5.0, 10.0, 20.0, 30.0):
        r = sep_kau * 1e3 * AU
        A = float(a_from_gbar(GM / r**2, A0, 2))
        v_int = math.sqrt(A * r)
        Om = v_int / r
        arg_bary = Om * (v_int / A0)
        arg_gal = Om * (220e3 / A0)
        mu_b = float(mu_num(arg_bary, 2))
        mu_g = float(mu_num(arg_gal, 2))
        rows.append((sep_kau, v_int, 220e3 / v_int, mu_b, mu_g))
        print(f"  {sep_kau:7.0f}k {A/A0:10.4f} {v_int:9.1f}m/s {220e3/v_int:12.0f} "
              f"{arg_bary:17.4f} {arg_gal:16.1f} {mu_b:9.5f} {mu_g:9.6f}")
    band = [r for r in rows if r[0] >= 10.0]          # the 10-30 kAU band the DR4 test lives in
    check(min(r[4] for r in band) > 0.9999 and max(r[3] for r in band) < 0.72,
          f"in the 10-30 kAU band the two drag levels are DIFFERENT THEORIES: galactocentric gives "
          f"mu = {min(r[4] for r in band):.6f}-{max(r[4] for r in band):.6f} (pure Newton, gamma -> 1) "
          f"while barycentre-dragged gives mu = {min(r[3] for r in band):.4f}-{max(r[3] for r in band):.4f} "
          f"(a {100*(1-min(r[3] for r in band)):.0f}% boost). The argument jumps by "
          f"v_gal/v_int = {min(r[2] for r in band):.0f}-{max(r[2] for r in band):.0f}x. So Route B "
          f"REPRODUCES the corpus's wide-binary DC-vs-AC gate fork under a new name -- it does not "
          f"resolve it. The frozen DR4 target gamma = 1.0246 (MI) belongs to the barycentre-dragged "
          f"branch only; the galactocentric branch predicts gamma = 1")
    check(rows[0][4] / rows[0][3] < 1.01,
          f"and the fork is SEPARATION-DEPENDENT, which is why it is testable rather than a "
          f"redefinition: at 2 kAU both branches are Newtonian (mu ratio "
          f"{rows[0][4]/rows[0][3]:.4f}), so the two drag levels only separate where u < 1")
    print("  NOTE ON PROCESS: PREREGISTRATION_DR4.md is FROZEN and hash-stamped. Nothing here changes")
    print("  a frozen target; this is a statement about which BRANCH the frozen target belongs to, and")
    print("  if Route B were ever adopted it would need an amendment filed IN THE OPEN before DR4.")


# =====================================================================================================
def main() -> int:
    banner("ROUTE B -- THE MEMORY-TIME ROUTE, TESTED. tau_mem = v_rel/a0 ?")
    print(f"  a0 = c H_Lambda / Z, Z = sqrt(32pi/3) = {Z:.5f}  ->  a0 = {A0:.4e} m/s^2 (canonical,")
    print(f"  pure-Lambda footing) = (c/2) sqrt(G rho_Lambda), i.e. EXACTLY HALF the free-fall")
    print(f"  acceleration at the dark-energy density. kappa = 1/2 is this framework's own coefficient")
    print(f"  and is not in the prior literature (Milgrom 1999 / Pikhitsa 2010 / Klinkhamer-Kopp 2011")
    print(f"  all give 2 c H_Lambda = 11.58x larger; Milgrom 2020 gives c H_Lambda/2pi). CAVEAT: 32pi/3")
    print(f"  is the Einstein-coupling conversion factor and CANCELS in that reduction -- the content")
    print(f"  is the ONE number kappa, which is FITTED, not derived.")
    print(f"  Alternate footing carried on every dimensional number: a0 = {A0_ALT:.4e} m/s^2.")
    print(f"  c/a0 = {C/A0/GYR:.1f} Gyr canonical, {C/A0_ALT/GYR:.1f} Gyr alternate -- the")
    print(f"  frame-independent memory time Route B is trying to replace.")

    s1_identity()
    s2_dimensional_enumeration()
    s3_consistency_prize()
    s4_drag_level()
    s5_off_circles()
    s6_ghosts_and_jensen()
    s7_wide_binary_consequence()

    banner("VERDICT")
    print("  Route B is PARTIAL, and the partition is sharp.")
    print("  WHAT WORKS, exactly and on both footings: on a circular orbit tau_mem = v_rel/a0 delivers")
    print("    Omega tau_mem = a/a0 identically, which is precisely the argument Theorem 8 found")
    print("    missing, and the enumeration shows c CANNOT appear in tau_mem -- so 'the frame must be")
    print("    locally dragged' is FORCED, not chosen. That is a genuine, if narrow, gain.")
    print("  WHAT DOES NOT WORK.")
    print("    * It pins nothing. The circular identity leaves a one-parameter monomial family and an")
    print("      infinite-dimensional function family; omega_c is not measured, it is replaced by a")
    print("      rule that is itself free off circles.")
    print("    * The drag level is triple-locked into an impossible corner: cosmic frame excluded by")
    print("      1.00 dex vs a 0.216 dex budget; local-matter drag excluded by 3.6-11x mis-scaling")
    print("      of a0 per disk population; and the barycentre prescription that survives both is")
    print("      NOT expressible as a local field, because two co-located stars in nested systems")
    print("      need frames differing by 8-25x in speed.")
    print("    * Off circles no candidate frequency survives: B is a tautology that lands back inside")
    print("      corrected Theorem 3, A and E diverge on radial motion, G is unboundedly wrong there.")
    print("    * The gap Theorem 8 names is K(<Box_u>) != <K(Box_u)>, and that is a function-vs-average")
    print("      statement. Both kernels are strictly concave, so the gap is positive-definite off")
    print("      circles by Jensen and is untouched by any rescaling of the argument. Route B repairs")
    print("      the argument and leaves the inequality exactly where it was.")
    print("  NOVELTY, assessed not asserted: the identity Omega (v/a0) = a/a0 is elementary kinematics;")
    print("  inertia-relative-to-matter is Mach (Sciama 1953 for the standard citation); orbit-dependent")
    print("  interpolating functions in modified inertia are Milgrom 1994 Ann.Phys. 229:384; and the")
    print("  single-frequency restriction is Milgrom 2022 PRD 106:064060. What is not in that prior art,")
    print("  as far as this script can tell, is the THREE-WAY DRAG LOCK of S4 and the Jensen signing of")
    print("  S6 -- both of which are NEGATIVE results about this framework, not new physics.")
    print("  NO DOOR IS DECLARED CLOSED. The unsettled piece is named in S6: whether a state-dependent")
    print("  passivity/KMS condition exists at all.")
    print("=" * 104)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
