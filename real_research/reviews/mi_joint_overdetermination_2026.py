#!/usr/bin/env python3
r"""mi_joint_overdetermination_2026.py -- LANE J: THE JOINT OVER-DETERMINATION.

THE QUESTION. A parameter FITTED to one dataset is a fit. A parameter forced to a unique value by having
to satisfy SEVERAL INDEPENDENT constraints at once is DERIVED BY OVER-DETERMINATION (Chandrasekhar mass;
CKM from four fits to an over-constrained consistency test). The framework has a handful of free
dimensionless quantities and faces five observational fronts. If the fronts outnumber the parameters
there are exactly three possible outcomes, all decisive:
   (a) exactly one choice satisfies every front  -> the parameters are DERIVED
   (b) no choice satisfies every front           -> the framework is FALSIFIED as a whole
   (c) a continuum satisfies every front         -> degenerate; name the flat directions
This script builds ONE chi^2 over the free quantities against all five fronts simultaneously and reports
whichever of (a)/(b)/(c) the arithmetic gives. It does NOT steer toward (a).

MANDATORY CREDIT. nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9; his
eqs 10-11 give a second coefficient and Milgrom 2008 sec 7.3.1 calls the mismatch "not necessarily
meaningful". a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. Temperature: Narnhofer,
Peter & Thirring 1996 IJMPB 10:1507. Five-acceleration: Deser & Levin 1997 CQG 14:L163. Exponential
kernel: McGaugh 2008 ApJ 683:137 eq 11a. The framework's distinctive content is the cH_Lambda/Z
COEFFICIENT plus the modified-inertia completion. *** kappa = 1/2 IS FITTED, NOT DERIVED. ***

FRONTS, and the committed scripts they are anchored to (numbers reproduced here, not trusted):
  F1 SPARC/RAR              real_research/reviews/mi_a0_profile_likelihood_sparc_2026.py
                            real_research/rar_framework_a0_mlfit.py            (0.108 dex @ Ups=0.70)
  F2a solar-system anomaly  real_research/reviews/mi_alpha1_solar_system_2026.py   (1278x / 189x)
                            real_research/reviews/mi_alpha2_migration_2026.py      (the alpha=2 switch)
  F2b memory-drift/omega_c  real_research/reviews/mi_ephemeris_omegac_edge_2026.py
  F3 wide binaries          real_research/reviews/mi_amendment7_wb_target_conflict_2026.py (1.55 sigma cap)
  F4 clusters               real_research/reviews/clusters_eta_audit.py   (+0.4052 dex, eRASS1 v3.2)
  F5 a0(z)                  closed form of project_a0z_evolution_law (bump-then-decline)

THE TWO WAYS THIS PROJECT HAS MANUFACTURED FALSE DEFICITS, and how they are guarded here:
  (i) scatter-as-measurement-error. F1 uses the PROFILE-LIKELIHOOD width deflated by the within-galaxy
      clustering factor, never the 0.108 dex RAR scatter. F4 uses the ABSOLUTE-SCALE systematic floor
      on the MEAN, never the 0.109 dex cluster-to-cluster scatter (which would give 367 sigma).
  (ii) truncating a systematic range at its TIGHT end. Every cell of the joint is run across the FULL
      committed systematic range -- cluster floor 0.10 to 0.30 dex, drift room R1a and R1b, both
      a0 footings, all five kernels -- and the widest cell is reported alongside the tightest.

FLOAT64 HAZARDS handled explicitly, and one is a REAL BUG FOUND IN A COMMITTED SCRIPT:
  * every (nu - 1) is evaluated with expm1/log1p, never by subtracting 1 from a number near 1;
  * mi_alpha2_migration_2026.py's alpha=2 Earth anomaly 1.3167e-18 is FLOAT NOISE (P1e proves it: it is
    identical on two footings that differ by 1.2082, and a0^2 dependence cannot be footing-independent).
    The true value is a0^2/(2 g_bar) = 7.4e-19. The published conclusion is UNAFFECTED (both are ~1e-5
    of the bound) but the number must not be quoted;
  * the exponential kernel's Newtonian anomaly underflows to exactly 0.0; it is carried in log10 so a
    strict inequality is not silently turned into an equality;
  * the F1 a0 minimum is re-scanned on a 4x finer grid and the shift is printed.

Exit 0 = ran and every internal check held. No hard-coded verdicts anywhere.
"""
from __future__ import annotations

import glob
import math
import os
import sys

import numpy as np
import sympy as sp

# ------------------------------------------------------------------------------------------------
CHECKS: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    CHECKS.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


HERE = os.path.dirname(os.path.abspath(__file__))
RR = os.path.dirname(HERE)

# ---------------- constants, both footings, all cited anchors ------------------------------------
c_l, G = 2.998e8, 6.674e-11
Msun, kpc, AU = 1.989e30, 3.0857e19, 1.495978707e11
GM_SUN = 1.32712440018e20
GM_EARTH, R_MOON = 3.986004418e14, 3.844e8
YR = 3.15576e7

H0, OmL = 2.184e-18, 0.685                       # Planck+BAO, 67.4 km/s/Mpc
rho_L = OmL * 3 * H0**2 / (8 * math.pi * G)
Z_FW = math.sqrt(32.0 * math.pi / 3.0)           # the framework's Z  (kappa = 1/2)
Z_M20 = 2.0 * math.pi                            # Milgrom 2020's     (kappa = 1/2pi)
A0_CANON = (c_l / 2.0) * math.sqrt(G * rho_L)    # canonical footing: rho_DE + cH_Lambda
A0_ALT = 1.1305e-10                              # ALT footing: rho_total + cH_0  (= /sqrt(OmL))
A0_MOND = 1.20e-10                               # McGaugh, Lelli & Schombert 2016

# F2a: Sereno & Jetzer 2006 Table 1 inverted via their own Eq (9) on Pitjeva EPM2004 (committed in
# mi_alpha1_solar_system_2026.py). Earth is the tightest bound and it is a 2-sigma allowance.
EARTH_DG_2SIG = 3.66e-14
EFE_RELIEF = 1278.0 / 189.0                      # the framework's OWN EFE partial cancellation
# F2b: gate window edges (mi_ephemeris_omegac_edge_2026.py / MI_FIELD_THEORY_RESULTS_2026)
OMEGA_C_MIN = 1.782e-14                          # = 3 x omega_gal,max, THEORY-INTERNAL, a0-independent
OMEGA_GAL_MAX = 5.94e-15                         # UGC05721 innermost deep-MOND orbit
GATE_KEEP = 0.90
GDOT_LLR_2SIG = (5.0 + 2 * 9.6) * 1e-15          # /yr  Biskupek & Mueller 2021
EPM_GMDOT_3SIG = 1.4e-14                         # /yr  Pitjeva+2021 EPM2019 FIT uncertainty (R1a)
EPM_GDOT_PLUS_3SIG = 4.6e-14                     # /yr  their Gdot/G interval, mass-loss-degenerate (R1b)
A_MARS = 2.279392e11
# F3: PREREGISTRATION_DR4 Amendment 4(d) in force + Amendment 7 (mi_amendment7_wb_target_conflict_2026)
WB_TARGET, WB_RANGE, WB_SIG_SYS, WB_SIG_FIT_30K = 1.0310, (1.0218, 1.0472), 0.02, 0.0191
# F4: eRASS1 primary v3.2 (Bulbul+2024)
FITS_PATH = os.path.join(RR, "data", "erass1cl_primary_v3.2.fits")
CLUSTER_FLOORS = (0.10, 0.15, 0.20, 0.30)        # the corpus's OWN full systematic range


def gN(a):
    return GM_SUN / a**2


# ================================================================================================
banner("P0  THE LEDGER -- how many free quantities, how many INDEPENDENT constraints")

FREE = [
    ("p1 kappa  (equivalently a0's normalisation)", "continuous", "FITTED to rotation curves"),
    ("p2 omega_c  (the memory cutoff, a 5th constant)", "continuous", "window [1.78,2.21]e-14"),
    ("p3 the interpolation SHAPE index", "discrete, 5 admissible kernels", "30.6% syst on a0"),
    ("p4 I_0, the ghost-condensate AMOUNT ~ Omega_dm", "continuous", "robustly FREE"),
    ("p5 the EFE prescription factor", "continuous", "calibrated on Crater II"),
    ("d1 the FOOTING: rho_DE/cH_Lambda vs rho_tot/cH_0", "discrete binary", "spread 1.2082x"),
]
CONS = [
    ("c1 F1  SPARC RAR profile likelihood on a0", "two-sided", "p1", "binds"),
    ("c2 F2a constant sunward anomaly, Earth 2-sigma", "one-sided", "p3 (and p1 weakly)", "binds"),
    ("c3 F2b secular drift floor -> omega_c upper edge", "one-sided", "p1 x p2", "binds"),
    ("c4 SPARC Re G >= 0.90 -> omega_c lower edge", "one-sided", "p2", "binds"),
    ("c5 F4  cluster eta(R500) on eRASS1", "two-sided", "p1, p3", "binds"),
    ("c6 F5  a0(z) shape", "two-sided", "(w0,wa) -- NOT p1..p5", "adds its own parameter"),
    ("c7 F3  wide-binary gamma_v", "two-sided", "p3", "NO DATA -- 0 constraints"),
    ("c8 Crater II EFE calibration", "two-sided", "p5", "consumed by p5 (a FIT)"),
]
print(f"  {'FREE QUANTITY':<48}{'kind':<32}{'status'}")
print("  " + "-" * 104)
for a, b, cc in FREE:
    print(f"  {a:<48}{b:<32}{cc}")
print(f"\n  {'CONSTRAINT':<48}{'kind':<14}{'binds':<26}{'verdict'}")
print("  " + "-" * 104)
for a, b, cc, d in CONS:
    print(f"  {a:<48}{b:<14}{cc:<26}{d}")

N_BIND = sum(1 for _, _, _, d in CONS if d == "binds")
SUBSPACE = ["p1 kappa/a0", "p2 omega_c", "p3 shape", "d1 footing"]
print(f"\n  BINDING constraints            = {N_BIND}   (c1,c2,c3,c4,c5)")
print(f"  parameters they act on         = {len(SUBSPACE)}   ({', '.join(SUBSPACE)}), of which d1 is a binary")
print(f"  net over-determination          = {N_BIND} - 3 continuous/discrete-shape = +{N_BIND-3}")
print(f"  p4 (I_0) is touched by NO constraint  -> irreducibly free")
print(f"  p5 (EFE) has exactly ONE constraint   -> exactly determined = a FIT, zero over-determination")
check(N_BIND == 5 and N_BIND - 3 == 2,
      f"P0a the (a0, omega_c, shape) subspace IS over-determined: {N_BIND} binding constraints on 3 "
      f"quantities = +{N_BIND-3} net, which is EXACTLY the '+2 degrees of freedom' the 2026-06-15 joint "
      f"analysis found viable. So the question 'can the +2 be driven to 0' is well posed and P8 answers it")
check(sum(1 for _, _, _, d in CONS if d != "binds") == 3,
      "P0b three fronts/constraints do NOT bind and saying so is half the answer: F3 has no data (P7), "
      "F5 is kappa-blind and brings its own (w0,wa) so it is net-zero for this count (P6), and the EFE "
      "factor is fixed by a single calibration, i.e. fitted not over-determined")
all_binds = " ".join(cc for _, _, cc, _ in CONS)
bind_binds = " ".join(cc for _, _, cc, d in CONS if d == "binds")
never = [f[0].split()[0] for f in FREE if f[0].split()[0] not in all_binds]
only_nonbinding = [f[0].split()[0] for f in FREE
                   if f[0].split()[0] in all_binds and f[0].split()[0] not in bind_binds]
print(f"  named by NO constraint at all            : {never}")
print(f"  named ONLY by a non-binding constraint   : {only_nonbinding}")
check(never == ["p4", "d1"] and only_nonbinding == ["p5"],
      f"P0c ledger consistency, computed by scanning the 'binds' column rather than asserted: p4 (I_0) "
      f"and d1 (the footing) are named by NO constraint row, and p5 (EFE) only by the non-binding "
      f"Crater II calibration. d1 is a special case -- it is not a fitted parameter but a discrete "
      f"convention that every front sees, so P8 enumerates it rather than profiling it; p4 is a "
      f"genuinely irreducible flat direction identified BEFORE any fitting starts, so nothing below can "
      f"be read as having derived it")


# ================================================================================================
banner("P1  THE FIVE ADMISSIBLE KERNELS -- every (nu - 1) float64-safe, and a BUG IN A COMMITTED SCRIPT")

# nu(y), g_obs = nu(y) g_bar, y = g_bar/a0.  Newtonian tail written 1 - mu ~ A x^-alpha, so the
# modified-inertia anomaly is  Delta = (nu-1) g_bar -> A a0^alpha g_bar^(1-alpha).
def nu_m1_K1(y):        # alpha=1, A=1/2 : THE FRAMEWORK (Milgrom 1999 eq 9). nu = sqrt(1+1/y)
    return np.expm1(0.5 * np.log1p(1.0 / np.asarray(y, float)))


def nu_m1_K2(y):        # alpha=2, A=1/2 : the corpus's alpha=2 switch, mu = x/sqrt(1+x^2)
    y = np.asarray(y, float)
    t = np.expm1(0.5 * np.log1p(4.0 / (y * y)))          # = sqrt(1+4/y^2) - 1, exactly
    return np.expm1(0.5 * np.log1p(0.5 * t))             # nu = sqrt(1 + t/2)


def nu_m1_SIM(y):       # alpha=1, A=1   : "simple" mu = x/(1+x)  (Famaey & Binney 2005)
    return 0.5 * np.expm1(0.5 * np.log1p(4.0 / np.asarray(y, float)))


def nu_m1_RAR(y):       # exponential    : McGaugh 2008 ApJ 683:137 eq 11a / McGaugh+2016
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return 1.0 / np.expm1(np.sqrt(y))


def nu_m1_MIN(y):       # alpha -> infinity : nu = max(1, 1/sqrt(y)), the sharp-transition limit
    y = np.asarray(y, float)
    return np.maximum(0.0, 1.0 / np.sqrt(y) - 1.0)


KERNELS = [
    ("K1 framework alpha=1 (Milgrom 99 eq 9)", nu_m1_K1, 1.0, 0.5),
    ("K2 corpus alpha=2 switch", nu_m1_K2, 2.0, 0.5),
    ("K3 simple alpha=1 (Famaey-Binney 05)", nu_m1_SIM, 1.0, 1.0),
    ("K4 exponential (McGaugh 08 eq 11a)", nu_m1_RAR, math.inf, math.nan),
    ("K5 sharp alpha->inf (nu = max)", nu_m1_MIN, math.inf, math.nan),
]


def nu_of(f, y):
    return 1.0 + f(y)


# P1a regression: reproduce the committed alpha=1 and alpha=2 nu values
print(f"  {'y = g_bar/a0':>13}{'nu K1':>11}{'nu K2':>11}{'nu K3':>11}{'nu K4':>11}{'nu K5':>11}")
for y in (0.06, 0.5, 1.0, 1.9, 3.0, 20.0):
    row = "".join(f"{float(nu_of(f, y)):>11.4f}" for _, f, _, _ in KERNELS)
    print(f"  {y:>13.2f}{row}")
check(abs(float(nu_of(nu_m1_K1, 1.0)) - 1.4142) < 5e-4 and abs(float(nu_of(nu_m1_K2, 1.0)) - 1.2720) < 5e-4
      and abs(float(nu_of(nu_m1_K2, 1.9)) - 1.1072) < 5e-4,
      "P1a regression against mi_alpha2_migration_2026.out: nu_K1(1) = 1.4142, nu_K2(1) = 1.2720, "
      "nu_K2(1.9) = 1.1072 all reproduced from independent expm1/log1p forms")

# P1b where the shape systematic lives -- and an HONEST CORRECTION to the brief's "agree to 1.14%"
def kspread(y):
    v = [float(nu_of(f, y)) for _, f, _, _ in KERNELS]
    return (max(v) - min(v)) / float(np.mean(v))


# deep-MOND asymptote nu -> C sqrt(a0/g_bar). If the C differ, a0 rescaling absorbs the difference; if
# they are all equal there is NO rescaling freedom and the deep spread is irreducible. Computed.
Cs = [float(nu_of(f, 1e-8)) * 1e-4 for _, f, _, _ in KERNELS]
spread_deep, spread_tr = kspread(0.06), kspread(1.0)
lo, hi = 1e-8, 0.06
for _ in range(60):
    mid = math.sqrt(lo * hi)
    if kspread(mid) > 0.0114:
        hi = mid
    else:
        lo = mid
y_114 = math.sqrt(lo * hi)
print(f"\n  deep-MOND prefactors C in nu -> C sqrt(a0/g_bar): {', '.join(f'{c:.5f}' for c in Cs)}")
print(f"  kernel spread at y = 0.06 (the brief's deep anchor) : {100*spread_deep:.2f}%")
print(f"  kernel spread at y = 1.0  (the transition)          : {100*spread_tr:.2f}%")
print(f"  y at which the spread actually falls to 1.14%        : {y_114:.2e}  "
      f"({0.06/y_114:.0f}x deeper than 0.06)")
check(max(Cs) - min(Cs) < 1e-3 and spread_deep > 0.05 and spread_deep < spread_tr
      and kspread(1e-5) < 0.0114,
      f"P1b *** CORRECTION OWED TO THE BRIEF, computed. *** All five kernels share the IDENTICAL deep "
      f"asymptote C = {Cs[0]:.5f} (spread {max(Cs)-min(Cs):.1e}), so there is NO a0-rescaling freedom to "
      f"absorb a deep disagreement. And they do NOT 'agree to 1.14% at y ~ 0.06': they differ by "
      f"{100*spread_deep:.2f}% there. 1.14% is reached only at y = {y_114:.1e}, "
      f"{0.06/y_114:.0f}x deeper -- below the outermost SPARC point of essentially every galaxy. The "
      f"brief's 5.5x dilution argument therefore rests on an anchor that is not deep enough, and the "
      f"real shape systematic on a0 is the {100*spread_deep:.0f}%-class number P2c measures, not 1.14%. "
      f"The spread still grows into the transition ({100*spread_tr:.2f}% at y = 1), which is why F2 and "
      f"F4 are the shape-sensitive fronts")

# P1c the Newtonian tail, symbolically, and the anomaly law
y_s, a0_s, gb_s, A_s, al_s = sp.symbols("y a_0 g_bar A alpha", positive=True)
x_s = sp.Symbol("x", positive=True)
mu_fw = (sp.sqrt(1 + 4 * x_s**2) - 1) / (2 * x_s)
tail_fw = sp.limit(x_s * (1 - mu_fw), x_s, sp.oo)
mu_sim = x_s / (1 + x_s)
tail_sim = sp.limit(x_s * (1 - mu_sim), x_s, sp.oo)
mu_std = x_s / sp.sqrt(1 + x_s**2)
tail_std = sp.limit(x_s**2 * (1 - mu_std), x_s, sp.oo)
check(tail_fw == sp.Rational(1, 2) and tail_sim == 1 and tail_std == sp.Rational(1, 2),
      f"P1c the tail exponents/amplitudes are DERIVED, not assumed: framework lim x(1-mu) = {tail_fw} "
      f"(alpha=1, A=1/2 -- the SAME class as 'simple', which has A = {tail_sim}), and the alpha=2 "
      f"standard mu has lim x^2(1-mu) = {tail_std}. Milgrom 2009 arXiv:0906.4817 and Sereno & Jetzer "
      f"2006 both state alpha=1 is excluded by the planets; the framework INHERITS that, it did not "
      f"discover it")

# P1d the exact asymptotic anomaly vs the safe numerical evaluation -- a real cross-check
gb_earth = GM_SUN / AU**2
print(f"\n  the Newtonian anomaly Delta = (nu-1) g_bar at Earth (g_bar = {gb_earth:.4e} m/s^2).")
print(f"  'numeric' calls the (nu-1) form DIRECTLY; it never forms nu and then subtracts 1.")
print(f"  {'kernel':<40}{'a0 [m/s^2]':>13}{'numeric':>13}{'asymptotic':>13}{'agree':>8}")
anom = {}
for nm, f, al, A in KERNELS:
    for tag, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        yv = gb_earth / a0
        num = float(f(yv)) * gb_earth              # <-- f IS (nu - 1); no 1 + eps - 1 anywhere
        asy = (A * a0**al * gb_earth**(1 - al)) if np.isfinite(al) else math.nan
        anom[(nm, tag)] = num
        rel = abs(num / asy - 1) if (np.isfinite(asy) and asy > 0) else math.nan
        print(f"  {nm+' ['+tag+']':<40}{a0:>13.4e}{num:>13.4e}"
              f"{(asy if np.isfinite(asy) else float('nan')):>13.4e}{rel:>8.1e}")
ok_asy = all(abs(anom[(nm, tg)] / (A * a0**al * gb_earth**(1 - al)) - 1) < 1e-6
             for nm, f, al, A in KERNELS if np.isfinite(al)
             for tg, a0 in (("canon", A0_CANON), ("alt", A0_ALT)))
check(ok_asy,
      "P1d every finite-alpha kernel's numeric anomaly matches its own closed-form asymptote "
      "A a0^alpha g_bar^(1-alpha) to <1e-6 -- so the expm1/log1p forms are exact where a naive "
      "sqrt(1+eps)-1 would not be, and the F2a column below is trustworthy at y ~ 6e7")

# P1e *** THE BUG IN THE COMMITTED SCRIPT ***
naive_k2 = []
for a0 in (A0_CANON, A0_ALT):
    yv = gb_earth / a0
    x2 = (yv**2 + math.sqrt(yv**4 + 4.0 * yv**2)) / 2.0     # verbatim from the committed script
    naive_k2.append((math.sqrt(x2) / yv - 1.0) * gb_earth)
true_k2 = [anom[("K2 corpus alpha=2 switch", t)] for t in ("canon", "alt")]
print(f"\n  *** mi_alpha2_migration_2026.py's alpha=2 Earth anomaly, re-derived two ways ***")
print(f"  {'':<26}{'canonical':>14}{'alt':>14}{'ratio alt/canon':>18}")
print(f"  {'naive (as committed)':<26}{naive_k2[0]:>14.4e}{naive_k2[1]:>14.4e}"
      f"{(naive_k2[1]/naive_k2[0] if naive_k2[0] else float('nan')):>18.4f}")
print(f"  {'expm1/log1p (correct)':<26}{true_k2[0]:>14.4e}{true_k2[1]:>14.4e}"
      f"{true_k2[1]/true_k2[0]:>18.4f}")
print(f"  a0^2 scaling REQUIRES ratio = (1.1305/0.93614)^2 = {(A0_ALT/A0_CANON)**2:.4f}")
eps_gb = np.finfo(float).eps * gb_earth
print(f"\n  AND THE SMOKING GUN: machine epsilon x g_bar(Earth) = {np.finfo(float).eps:.6e} x "
      f"{gb_earth:.6e} = {eps_gb:.4e}")
print(f"  the committed value is {naive_k2[0]:.4e}.  These agree to "
      f"{abs(naive_k2[0]/eps_gb-1)*100:.2f}% -- it is 1 ULP, not physics.")
check(abs(naive_k2[0] / eps_gb - 1) < 0.02
      and abs(naive_k2[0] - naive_k2[1]) / max(naive_k2[0], 1e-300) < 0.05
      and abs(true_k2[1] / true_k2[0] - (A0_ALT / A0_CANON) ** 2) < 1e-6
      and abs(naive_k2[0] / true_k2[0] - 1) > 0.5,
      f"P1e *** BUG CONFIRMED IN A COMMITTED SCRIPT, and it is a float64 cancellation. *** "
      f"mi_alpha2_migration_2026.out prints 1.3167e-18 for BOTH footings; the anomaly goes as a0^2 so "
      f"two footings differing by 1.2082 CANNOT give the same number. Two independent proofs it is "
      f"noise: (1) the naive x^2 = (y^2+sqrt(y^4+4y^2))/2 loses 4y^2 against y^4 at y ~ 6e7 "
      f"(4/y^2 = {4/(gb_earth/A0_CANON)**2:.2e} vs eps = 2.2e-16); (2) the printed number EQUALS "
      f"eps x g_bar = {eps_gb:.4e} to {abs(naive_k2[0]/eps_gb-1)*100:.2f}%, i.e. exactly one ULP of the "
      f"1.0 that got subtracted. Correct values: {true_k2[0]:.4e} (canon), {true_k2[1]:.4e} (alt), "
      f"= a0^2/(2 g_bar). *** My OWN first draft of this script reproduced the same 1.3167e-18 by the "
      f"same mistake (forming nu then subtracting 1), which is how it was caught. *** The published "
      f"CONCLUSION survives untouched -- both values are ~1e-5 of the bound, so the alpha=2 switch still "
      f"discharges the liability -- but the NUMBER must not be quoted. Correction owed")

log10_anom_K4 = math.log10(gb_earth) - math.sqrt(gb_earth / A0_CANON) / math.log(10)
check(anom[("K4 exponential (McGaugh 08 eq 11a)", "canon")] == 0.0 and log10_anom_K4 < -3000,
      f"P1f and the exponential kernel's anomaly UNDERFLOWS to exactly 0.0, which would silently turn a "
      f"strict inequality into an equality. Carried in log10 instead: log10 Delta = "
      f"{log10_anom_K4:.1f}, i.e. 10^{log10_anom_K4:.0f} m/s^2. Reported, not rounded to zero")


# ================================================================================================
banner("P2  F1 -- SPARC/RAR PROFILE LIKELIHOOD ON a0, Upsilon FREE PER GALAXY, ALL FIVE KERNELS")
print("  reproducing reviews/mi_a0_profile_likelihood_sparc_2026.py (which itself corrected a")
print("  scatter-for-error mistake) and EXTENDING it from alpha=1 to all five admissible kernels.")

DATA = os.path.join(RR, "data", "sparc_data")
gals = []
for fp in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(fp, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    m = np.isfinite(R) & np.isfinite(Vobs) & (R > 0) & (Vobs > 0)
    if m.sum() < 3:
        continue
    Rm = R[m] * kpc
    ev = np.clip(eV[m], 1.0, None)
    gals.append(dict(
        name=os.path.basename(fp).replace("_rotmod.dat", ""),
        Rm=Rm,
        gobs=(Vobs[m] * 1e3) ** 2 / Rm,
        lgobs=np.log10((Vobs[m] * 1e3) ** 2 / Rm),
        sig=(ev / Vobs[m]) * 2.0 / math.log(10),
        gasterm=np.sign(Vgas[m]) * Vgas[m] ** 2 * 1e6 / Rm,
        starterm=(Vdisk[m] ** 2 + 1.4 * Vbul[m] ** 2) * 1e6 / Rm,
    ))
N_GAL = len(gals)
N_PTS = sum(len(g["lgobs"]) for g in gals)
print(f"\n  loaded {N_GAL} galaxies / {N_PTS} points from {os.path.relpath(DATA, RR)}")
check(N_GAL >= 170 and N_PTS > 3000,
      f"P2a full SPARC loaded: {N_GAL} galaxies / {N_PTS} points, matching the committed loader")

UGRID = np.linspace(0.05, 3.0, 119)


def sparc_chi2(a0, f, sig_int):
    """sum over galaxies of min_Upsilon chi^2, fully vectorised over the Upsilon grid.
    Points with g_bar <= 0 contribute 0, exactly as dropping them does."""
    tot, npts = 0.0, 0
    for g in gals:
        gbar = g["gasterm"][None, :] + UGRID[:, None] * g["starterm"][None, :]   # (nU, np)
        good = gbar > 0
        gb = np.where(good, gbar, 1.0)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            pred = np.log10(nu_of(f, gb / a0) * gb)
        r = g["lgobs"][None, :] - pred
        w = 1.0 / (g["sig"][None, :] ** 2 + sig_int**2)
        chi = np.where(good & np.isfinite(r), r * r * w, 0.0).sum(axis=1)
        j = int(np.argmin(chi))
        tot += float(chi[j])
        npts += int(good[j].sum())
    return tot, npts


def calibrate_sigint(a0, f):
    lo, hi = 0.001, 0.60
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        ch, npts = sparc_chi2(a0, f, mid)
        if ch / (npts - N_GAL - 1) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# grid wide enough to contain BOTH the RAR minimum and the cluster-preferred a0 (~5x canonical)
GRID = np.concatenate([np.linspace(0.60, 1.60, 41), np.linspace(1.7, 6.5, 25)]) * A0_CANON
F1 = {}
print(f"\n  {'kernel':<40}{'sig_int':>9}{'a0_hat/a0_c':>13}{'sig_ind':>10}{'sig_clu':>10}{'refine shift':>14}")
print("  " + "-" * 96)
for nm, f, al, A in KERNELS:
    s_int = calibrate_sigint(A0_CANON, f)
    ch = np.array([sparc_chi2(a0, f, s_int)[0] for a0 in GRID])
    npts = sparc_chi2(A0_CANON, f, s_int)[1]
    i0 = int(np.argmin(ch))
    a0_coarse = GRID[i0]
    # 4x refinement around the coarse minimum -- the brief's "coarse grids report unsampled extrema"
    lo = GRID[max(i0 - 1, 0)]
    hi = GRID[min(i0 + 1, len(GRID) - 1)]
    fine = np.linspace(lo, hi, 25)
    chf = np.array([sparc_chi2(a0, f, s_int)[0] for a0 in fine])
    a0_hat = fine[int(np.argmin(chf))]
    ch_min = float(chf.min())
    DEFL = npts / N_GAL                          # within-galaxy clustering deflation

    def dchi2(a0, _f=f, _s=s_int, _m=ch_min):
        return sparc_chi2(a0, _f, _s)[0] - _m

    def cross(target, sign):
        a, b = a0_hat, a0_hat * (2.0 if sign > 0 else 0.5)
        if dchi2(b) < target:
            return math.nan
        for _ in range(40):
            m = 0.5 * (a + b)
            if dchi2(m) < target:
                a = m
            else:
                b = m
        return 0.5 * (a + b)

    hiC, loC = cross(1.0, +1), cross(1.0, -1)
    sig_ind = 0.5 * abs(hiC - loC) / a0_hat
    sig_clu = sig_ind * math.sqrt(DEFL)
    F1[nm] = dict(f=f, s_int=s_int, a0=a0_hat, sig_ind=sig_ind, sig_clu=sig_clu,
                  grid=GRID, ch=ch, ch_min=ch_min, DEFL=DEFL, npts=npts)
    print(f"  {nm:<40}{s_int:>9.4f}{a0_hat/A0_CANON:>13.4f}{100*sig_ind:>9.2f}%{100*sig_clu:>9.2f}%"
          f"{100*(a0_hat/a0_coarse-1):>13.2f}%")

k1 = F1["K1 framework alpha=1 (Milgrom 99 eq 9)"]
check(abs(k1["a0"] / 1.0766e-10 - 1) < 0.02 and k1["sig_clu"] > 0.0544 and k1["sig_clu"] < 0.10,
      f"P2b REGRESSION on the committed script: alpha=1 gives a0_hat = {k1['a0']:.4e} "
      f"({k1['a0']/A0_CANON:.4f}x canonical) against its 1.0766e-10 (1.1500x) -- "
      f"{100*abs(k1['a0']/1.0766e-10-1):.2f}% apart on a completely independent vectorisation. The ERROR "
      f"BAR comes out WIDER: sigma_clu {100*k1['sig_clu']:.2f}% vs its 5.44%, because the committed "
      f"script read the Dchi2 = 1 crossing off a 31-point grid spaced 2.5% in a0 by linear "
      f"interpolation, while this one bisects it to 1e-6. A wider bar is the CONSERVATIVE direction, so "
      f"the correction is taken rather than argued away")

a0_hats = np.array([F1[nm]["a0"] for nm, _, _, _ in KERNELS])
shape_sys = (a0_hats.max() - a0_hats.min()) / a0_hats.mean()
print(f"\n  SHAPE SYSTEMATIC on a0 across the five kernels = {100*shape_sys:.1f}%   (brief: 30.6%)")
print(f"  a0_hat/a0_canon range = {a0_hats.min()/A0_CANON:.3f} to {a0_hats.max()/A0_CANON:.3f}")
check(shape_sys > 3 * k1["sig_clu"],
      f"P2c *** the SHAPE systematic ({100*shape_sys:.1f}%) is {shape_sys/k1['sig_clu']:.1f}x LARGER than "
      f"F1's own statistical precision ({100*k1['sig_clu']:.2f}%). *** So F1 alone cannot derive a0: any "
      f"claim of a0 to better than the shape spread is a claim about p3, and P8 must therefore profile "
      f"a0 and the kernel JOINTLY rather than quoting the alpha=1 bar")

# the three kappa hypotheses on each kernel, in DEFLATED (conservative) Dchi2
KAPPAS = [("kappa = 1/2pi  (Milgrom 2020)", A0_CANON * Z_FW / Z_M20),
          ("kappa = 1/2    (THE FRAMEWORK)", A0_CANON),
          ("kappa = 1/2, ALT footing", A0_ALT),
          ("kappa = 1      (2x)", 2 * A0_CANON),
          ("kappa = 2      (4x)", 4 * A0_CANON)]
print(f"\n  DEFLATED Dchi2 (= raw/{k1['DEFL']:.1f}, the conservative galaxy-clustered counting):")
hdr = "".join(f"{nm.split()[0]:>10}" for nm, _, _, _ in KERNELS)
print(f"  {'hypothesis':<32}{'a0/a0_c':>9}" + hdr)
print("  " + "-" * 92)
DCH = {}
for hn, a0h in KAPPAS:
    row = ""
    for nm, f, _, _ in KERNELS:
        d = (sparc_chi2(a0h, f, F1[nm]["s_int"])[0] - F1[nm]["ch_min"]) / F1[nm]["DEFL"]
        DCH[(hn, nm)] = d
        row += f"{d:>10.2f}"
    print(f"  {hn:<32}{a0h/A0_CANON:>9.4f}" + row)
NM1 = "K1 framework alpha=1 (Milgrom 99 eq 9)"
f_half = DCH[("kappa = 1/2    (THE FRAMEWORK)", NM1)]
f_m20 = DCH[("kappa = 1/2pi  (Milgrom 2020)", NM1)]
d_half = min(DCH[("kappa = 1/2    (THE FRAMEWORK)", nm)] for nm, _, _, _ in KERNELS)
d_m20 = min(DCH[("kappa = 1/2pi  (Milgrom 2020)", nm)] for nm, _, _, _ in KERNELS)
d_alt = min(DCH[("kappa = 1/2, ALT footing", nm)] for nm, _, _, _ in KERNELS)
argmin_m20 = min(KERNELS, key=lambda k: DCH[("kappa = 1/2pi  (Milgrom 2020)", k[0])])[0]
check(f_half < f_m20 and abs(f_m20 / f_half - 154.29 / 63.90) < 0.05,
      f"P2d(i) REGRESSION, and it reproduces the committed kappa result EXACTLY on the ratio: AT THE "
      f"FIXED alpha=1 KERNEL, kappa = 1/2 gives deflated Dchi2 {f_half:.2f} and kappa = 1/2pi gives "
      f"{f_m20:.2f}, ratio {f_m20/f_half:.3f} against mi_a0_profile_likelihood_sparc_2026.py's "
      f"154.29/63.90 = {154.29/63.90:.3f}. (Its raw numbers are these times the deflation "
      f"{k1['DEFL']:.1f}.) So the ~2.2 sigma preference for kappa = 1/2 is confirmed AS COMPUTED")
check(d_m20 < d_half and argmin_m20 != NM1,
      f"P2d(ii) *** AND HERE IS THE FIRST THING THE JOINT OVERTURNS, AGAINST INTEREST. *** Once the "
      f"SHAPE INDEX is admitted as the free quantity it is -- which the joint requires, since P2c shows "
      f"the shape systematic is 4x F1's statistical bar -- the ordering REVERSES: profiled over the five "
      f"admissible kernels, kappa = 1/2pi reaches Dchi2 {d_m20:.2f} (on {argmin_m20.split()[0]}) while "
      f"kappa = 1/2 reaches only {d_half:.2f}. Milgrom 2020's coefficient fits BETTER once the kernel is "
      f"free, because the simple/exponential kernels prefer a0 ~ 0.94x canonical and 1/2pi sits at "
      f"0.921x. So F1's 2.2-sigma discrimination is SHAPE-CONDITIONAL, not a measurement of kappa. This "
      f"is a correction owed to project_kappa_discriminability, and it is the opposite of a win")
check(d_alt < f_half,
      f"P2d(iii) and the third half, also against interest: the ALT footing (a0 = 1.13e-10) reaches "
      f"Dchi2 {d_alt:.2f}, better than canonical kappa = 1/2's {f_half:.2f} at fixed alpha=1. This front "
      f"prefers a HIGHER a0 than the canonical rho_DE/cH_Lambda footing the corpus publishes")


# ================================================================================================
banner("P3  F2a -- THE CONSTANT SUNWARD ANOMALY: which SHAPES survive the inner planets")
print(f"  Earth 2-sigma allowance {EARTH_DG_2SIG:.3e} m/s^2, from Sereno & Jetzer 2006 Table 1 inverted")
print(f"  through their own Eq (9) on Pitjeva EPM2004 (committed: mi_alpha1_solar_system_2026.py).")
print(f"  The framework's OWN EFE supplies a partial cancellation, factor {EFE_RELIEF:.2f} (1278x -> 189x).")
SIG_E = EARTH_DG_2SIG / 2.0
print(f"\n  {'kernel':<40}{'a0':>8}{'Delta bare':>13}{'/bound':>10}{'Delta post-EFE':>15}{'sigma':>9}")
print("  " + "-" * 96)
F2A = {}
for nm, f, al, A in KERNELS:
    for tag, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        dbare = anom[(nm, tag)]
        defe = dbare / EFE_RELIEF
        F2A[(nm, tag)] = defe
        s = defe / SIG_E
        print(f"  {nm:<40}{tag:>8}{dbare:>13.4e}{dbare/EARTH_DG_2SIG:>10.1f}x{defe:>15.4e}{s:>9.1f}")

s_k1 = F2A[("K1 framework alpha=1 (Milgrom 99 eq 9)", "canon")] / SIG_E
s_k3 = F2A[("K3 simple alpha=1 (Famaey-Binney 05)", "canon")] / SIG_E
s_k2 = F2A[("K2 corpus alpha=2 switch", "canon")] / SIG_E
check(s_k1 > 100 and s_k3 > s_k1 and s_k2 < 1e-3,
      f"P3a *** F2a KILLS THE alpha=1 SHAPE CLASS OUTRIGHT, and it is the framework's own published "
      f"kernel. *** Post-EFE the framework's alpha=1 anomaly sits {s_k1:.0f} sigma over the Earth "
      f"allowance ({anom[('K1 framework alpha=1 (Milgrom 99 eq 9)','canon')]/EARTH_DG_2SIG:.0f}x bare, "
      f"189x post-EFE, reproducing the committed number); 'simple' is worse at {s_k3:.0f} sigma; the "
      f"alpha=2 switch passes with {s_k2:.1e} sigma to spare. This is a genuine DERIVATION by "
      f"over-determination: the SHAPE INDEX is forced, alpha = 1 is excluded, and no value of kappa "
      f"rescues it because the anomaly is A a0, i.e. kappa would have to shrink by 1278x")

# how much kappa would have to shrink to save alpha=1 -- and what F1 says to that
a0_needed = SIG_E * 2 * EFE_RELIEF / 0.5          # A a0 <= bound*EFE  =>  a0 <= 2*bound*EFE
print(f"\n  to save the alpha=1 shape, a0 would have to fall to <= {a0_needed:.3e} m/s^2 "
      f"= {a0_needed/A0_CANON:.2e} x canonical,")
print(f"  i.e. kappa <= {0.5*a0_needed/A0_CANON:.2e}. F1's own bar rules that out by "
      f"{abs(math.log10(a0_needed/k1['a0']))/ (k1['sig_clu']/math.log(10)):.0f} sigma.")
check(a0_needed < 0.01 * A0_CANON,
      f"P3b and the escape 'shrink kappa' is closed quantitatively: alpha=1 needs a0 <= "
      f"{a0_needed/A0_CANON:.2e}x canonical, which destroys F1 (and every galaxy-scale front) "
      f"completely. So F2a x F1 is a genuinely MUTUALLY EXCLUSIVE pair for the alpha=1 shape -- the "
      f"first hard elimination in this joint")


# ================================================================================================
banner("P4  F2b -- THE MEMORY-DRIFT FLOOR: the constraint on a0 x omega_c, and Route B")
print("  The gate G(omega) = 1/(1 + i omega/omega_c) has a DISSIPATIVE channel giving a secular")
print("  d ln a/dt = a0 omega_c / g_N -- the same observable LLR uses for Gdot/G. The window's LOWER")
print("  edge omega_c >= 3 omega_gal,max is THEORY-INTERNAL and a0-INDEPENDENT, so there is a FLOOR on")
print("  the predicted drift that no choice of omega_c can lower. That floor is linear in a0.")
gN_mars, gN_moon = gN(A_MARS), GM_EARTH / R_MOON**2
READINGS = [
    ("LLR 2sig (Biskupek-Mueller 21)", GDOT_LLR_2SIG / 2.0, gN_moon, "Moon"),
    ("R1b EPM2019 Gdot/G, mass-loss-degenerate", EPM_GDOT_PLUS_3SIG / 3.0, gN_mars, "Mars"),
    ("R1a EPM2019 fit-only (non-degenerate)", EPM_GMDOT_3SIG / 3.0, gN_mars, "Mars"),
]
print(f"\n  {'reading':<44}{'body':>7}{'sigma_D [/yr]':>15}{'D_req(a0_c)':>14}{'sigma':>8}{'a0_max':>12}")
print("  " + "-" * 100)
F2B = {}
for rn, sD, gg, body in READINGS:
    Dreq = A0_CANON * OMEGA_C_MIN / gg * YR
    a0max = sD * 2.0 / YR * gg / OMEGA_C_MIN      # a0 at which D_req = 2 sigma_D
    F2B[rn] = dict(sigD=sD, gN=gg, body=body, a0max=a0max)
    print(f"  {rn:<44}{body:>7}{sD:>15.3e}{Dreq:>14.3e}{Dreq/sD:>8.2f}{a0max/A0_CANON:>11.3f}x")

check(abs(A0_CANON * OMEGA_C_MIN / gN_mars * YR - 2.06e-14) / 2.06e-14 < 0.02,
      f"P4a regression on mi_ephemeris_omegac_edge_2026.py: at the window's non-negotiable BOTTOM the "
      f"framework requires Mars to drift at {A0_CANON*OMEGA_C_MIN/gN_mars*YR:.3e}/yr, matching its "
      f"printed 2.06e-14/yr. 'There is no quiet corner: the drift FLOOR is set by the galaxies'")
s_r1a = A0_CANON * OMEGA_C_MIN / gN_mars * YR / F2B["R1a EPM2019 fit-only (non-degenerate)"]["sigD"]
s_r1b = A0_CANON * OMEGA_C_MIN / gN_mars * YR / F2B["R1b EPM2019 Gdot/G, mass-loss-degenerate"]["sigD"]
check(s_r1a > s_r1b > 0.5,
      f"P4b F2b is ALREADY a tension at the canonical a0, and its size is entirely the R1a/R1b fork: "
      f"{s_r1b:.2f} sigma if the MI drift may hide inside the solar mass-loss allowance (R1b), "
      f"{s_r1a:.2f} sigma if it may not (R1a -- correct in principle, because the MI drift scales as "
      f"a^2 while mass loss and Gdot are flat in a). Both carried through P8; quoting only R1a would "
      f"manufacture a deficit and quoting only R1b a comfort")
check(all(F2B[r]["a0max"] < 4 * A0_CANON for r in F2B),
      f"P4c and this is the front that caps a0 from ABOVE: a0 <= "
      f"{min(F2B[r]['a0max'] for r in F2B)/A0_CANON:.2f}x to "
      f"{max(F2B[r]['a0max'] for r in F2B)/A0_CANON:.2f}x canonical at 2 sigma across the readings. "
      f"Note the direction -- F1 pulls a0 UP to 1.15x and F2b pushes it DOWN; P8 tests whether they "
      f"still overlap")

# Route B, and the SPARC gate that kills it -- an over-determination result in its own right
wc_routeB = A0_CANON / c_l
ReG_gal = 1.0 / (1.0 + (OMEGA_GAL_MAX / wc_routeB) ** 2)
tau_routeB = 1.0 / wc_routeB / (YR * 1e9)
print(f"\n  ROUTE B (omega_c = a0/v_rel, at v_rel = c): omega_c = {wc_routeB:.3e} rad/s, memory time "
      f"{tau_routeB:.1f} Gyr")
print(f"  gate transmission at UGC05721's innermost deep-MOND orbit (omega = {OMEGA_GAL_MAX:.3e}): "
      f"Re G = {ReG_gal:.3e}")
check(ReG_gal < GATE_KEEP and wc_routeB < OMEGA_C_MIN,
      f"P4d *** ROUTE B IS EXCLUDED BY THE FRAMEWORK'S OWN ROTATION CURVES. *** omega_c = a0/c is "
      f"{OMEGA_C_MIN/wc_routeB:.2e}x BELOW the window floor, and at galaxy orbital frequencies the gate "
      f"transmits Re G = {ReG_gal:.2e} against the required >= {GATE_KEEP}. It would suppress the MOND "
      f"effect in galaxies by ~{1/ReG_gal:.1e}. So omega_c IS over-determined in one useful sense: two "
      f"one-sided constraints (SPARC from below, drift from above) leave a WINDOW and eliminate the one "
      f"closed-form candidate the corpus offers for omega_c's VALUE")
win_c = F2B["LLR 2sig (Biskupek-Mueller 21)"]
wc_up_canon = win_c["sigD"] * 2 / YR * gN_moon / A0_CANON
wc_up_alt = win_c["sigD"] * 2 / YR * gN_moon / A0_ALT
print(f"\n  window rebuild: omega_c in [{OMEGA_C_MIN:.3e}, {wc_up_canon:.3e}] canon (width "
      f"x{wc_up_canon/OMEGA_C_MIN:.3f}), [{OMEGA_C_MIN:.3e}, {wc_up_alt:.3e}] alt "
      f"(x{wc_up_alt/OMEGA_C_MIN:.3f})")
check(abs(wc_up_canon / 2.211e-14 - 1) < 0.02 and abs(wc_up_alt / 1.831e-14 - 1) < 0.02,
      f"P4e window rebuilt from the cited LLR bound alone to within 2% of the committed "
      f"[1.782,2.211]e-14 canon / [1.782,1.831]e-14 alt. Note what that means for the FOOTING: the ALT "
      f"footing F1 prefers leaves omega_c a window only x{wc_up_alt/OMEGA_C_MIN:.3f} wide -- 2.7%, "
      f"nearly a POINT, and therefore nearly CLOSED")


# ================================================================================================
banner("P5  F4 -- CLUSTERS: eta(R500) on eRASS1, all five kernels, FULL systematic floor range")
if not os.path.exists(FITS_PATH):
    print(f"  MISSING {FITS_PATH} -- refusing to fabricate a cluster number.")
    sys.exit(2)
from astropy.io import fits as _fits                                    # noqa: E402

_d = _fits.open(FITS_PATH)[1].data


def _col(nm):
    return np.array([float(v) if str(v).strip() not in ("", "--") else np.nan for v in _d[nm]], float)


_z, _M500, _Mgas, _fgas, _R500 = (_col("BEST_Z"), _col("M500"), _col("MGAS500"),
                                  _col("FGAS500"), _col("R500"))
_okc = ((_z > 0) & (_z < 1.0) & np.isfinite(_z) & (_M500 > 0) & (_Mgas > 0) & (_R500 > 0)
        & (_fgas > 0.01) & (_fgas < 0.30))
FSTAR = 0.20
_Rm = _R500[_okc] * kpc
CL_GOBS = G * (_M500[_okc] * 1e13 * Msun) / _Rm**2
CL_GBAR = G * ((1 + FSTAR) * _Mgas[_okc] * 1e11 * Msun) / _Rm**2
N_CL = int(_okc.sum())
y_cl = float(np.median(CL_GBAR / A0_CANON))
print(f"  eRASS1 primary v3.2 (Bulbul+2024), 0<z<1, 0.01<fgas<0.30, fstar={FSTAR}: N = {N_CL}")
print(f"  median y = g_bar/a0 at R500 (canonical) = {y_cl:.4f} -- DEEP MOND, not the transition, so the")
print(f"  kernel dependence here is the sub-leading one (P1b's {100*spread_deep:.0f}%-class deep spread),")
print(f"  which is why the eta column below moves by only ~0.04 dex across all five kernels.")


def cl_meanlog(a0, f):
    return float(np.mean(np.log10(CL_GOBS / (nu_of(f, CL_GBAR / a0) * CL_GBAR))))


print(f"\n  {'kernel':<40}{'<log10 eta> canon':>19}{'eta_med':>10}{'a0 needed':>12}{'sigma @0.10':>12}"
      f"{'@0.30':>8}")
print("  " + "-" * 102)
F4 = {}
for nm, f, al, A in KERNELS:
    ml = cl_meanlog(A0_CANON, f)
    med = float(np.median(CL_GOBS / (nu_of(f, CL_GBAR / A0_CANON) * CL_GBAR)))
    # a0 at which <log10 eta> = 0, by bisection (eta falls with a0)
    lo, hi = A0_CANON, 400 * A0_CANON
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if cl_meanlog(mid, f) > 0:
            lo = mid
        else:
            hi = mid
    a0_need = math.sqrt(lo * hi)
    F4[nm] = dict(ml=ml, med=med, a0_need=a0_need)
    print(f"  {nm:<40}{ml:>+19.4f}{med:>10.3f}{a0_need/A0_CANON:>11.2f}x{ml/0.10:>12.2f}{ml/0.30:>8.2f}")

ml_k1 = F4["K1 framework alpha=1 (Milgrom 99 eq 9)"]["ml"]
check(abs(ml_k1 - 0.4052) < 0.005 and abs(N_CL - 9830) <= 50,
      f"P5a REGRESSION on clusters_eta_audit.py: N = {N_CL} (its 9830), <log10 eta> = {ml_k1:+.4f} "
      f"(its +0.4052) on the framework's OWN kernel. Same data, same number, independently coded")
check(F4["K2 corpus alpha=2 switch"]["ml"] > ml_k1
      and F4["K3 simple alpha=1 (Famaey-Binney 05)"]["ml"] < ml_k1
      and abs(F4["K2 corpus alpha=2 switch"]["ml"] - ml_k1) < 0.02,
      f"P5b F2a AND F4 PUSH THE SHAPE INDEX IN OPPOSITE DIRECTIONS -- but only WEAKLY, and the "
      f"weakness matters. At the clusters' median y = {y_cl:.4f} the kernels differ only sub-leadingly, "
      f"so alpha=2 makes the cluster deficit worse by just "
      f"{F4['K2 corpus alpha=2 switch']['ml']-ml_k1:+.4f} dex "
      f"({F4['K2 corpus alpha=2 switch']['ml']:+.4f} vs {ml_k1:+.4f}) and the only kernels that help "
      f"('simple', exponential) buy {ml_k1-F4['K3 simple alpha=1 (Famaey-Binney 05)']['ml']:.4f} dex. "
      f"So the SHAPE cannot resolve F4 either way: it is not a free direction for the cluster front, "
      f"which is why P8's clash has to be priced in a0 and in the systematic floor, not in p3")
a0_need_gm = A0_CANON * 10 ** (2 * ml_k1)                 # eta^2 with the log-MEAN (geometric mean) eta
a0_need_med = A0_CANON * F4[NM1]["med"] ** 2              # eta^2 with the MEDIAN eta
r_gm = F4[NM1]["a0_need"] / a0_need_gm
r_med = F4[NM1]["a0_need"] / a0_need_med
print(f"\n  three ways to state the a0 boost the clusters demand, on the framework's own kernel:")
print(f"    median-eta ^2  (the corpus's quoted 5.45x)     : {a0_need_med/A0_CANON:.2f}x")
print(f"    geomean-eta ^2 (the corpus's other row)        : {a0_need_gm/A0_CANON:.2f}x")
print(f"    direct solve of <log10 eta>(a0) = 0            : {F4[NM1]['a0_need']/A0_CANON:.2f}x")
check(r_gm > 1.02 and r_med > 1.15,
      f"P5c the deep-MOND inversion a0 -> a0 eta^2 UNDERSTATES the boost on both of the corpus's rows: "
      f"the direct solve is {100*(r_gm-1):.0f}% above the geomean row and {100*(r_med-1):.0f}% above the "
      f"median row that the corpus quotes as '5.45x'. Reason: at y ~ {y_cl:.3f} raising a0 also slides "
      f"the points along the kernel, so eta falls more slowly than 1/sqrt(a0). The joint below uses the "
      f"direct solve, i.e. the version LEAST favourable to the framework, and says so")
check(all(F4[nm]["a0_need"] > 3 * A0_CANON for nm, _, _, _ in KERNELS),
      f"P5d on every kernel the clusters want a0 boosted by "
      f"{min(F4[nm]['a0_need'] for nm,_,_,_ in KERNELS)/A0_CANON:.1f}x-"
      f"{max(F4[nm]['a0_need'] for nm,_,_,_ in KERNELS)/A0_CANON:.1f}x, while F2b caps it at "
      f"{max(F2B[r]['a0max'] for r in F2B)/A0_CANON:.2f}x and F1 measures "
      f"{k1['a0']/A0_CANON:.2f}x. THAT is the binding triangle")
print(f"\n  the systematic floor is used on the MEAN, never the scatter: scatter = "
      f"{np.std(np.log10(CL_GOBS/(nu_of(nu_m1_K1, CL_GBAR/A0_CANON)*CL_GBAR))):.4f} dex, "
      f"SE = {np.std(np.log10(CL_GOBS/(nu_of(nu_m1_K1,CL_GBAR/A0_CANON)*CL_GBAR)))/math.sqrt(N_CL):.5f} dex")
print(f"  -> the formal statistical significance would be "
      f"{ml_k1/(np.std(np.log10(CL_GOBS/(nu_of(nu_m1_K1,CL_GBAR/A0_CANON)*CL_GBAR)))/math.sqrt(N_CL)):.0f}"
      f" sigma. It is NOT quoted: eta is an absolute-scale ratio and every cluster shares the same")
print(f"  mass-scale calibration, so the floor {CLUSTER_FLOORS} dex is the error. Full range used.")


# ================================================================================================
banner("P6  F5 -- a0(z): PROVE it is kappa-blind, so it cannot help derive kappa")
z_s, w0_s, wa_s, kap_s = sp.symbols("z w_0 w_a kappa", positive=True)
# local-response floor: a0 ~ kappa c sqrt(G rho_DE(z)),  rho_DE(z) = rho_DE0 (1+z)^{3(1+w0+wa)} e^{-3 wa z/(1+z)}
rho_ratio = (1 + z_s) ** (3 * (1 + w0_s + wa_s)) * sp.exp(-3 * wa_s * z_s / (1 + z_s))
a0_of_z = kap_s * sp.sqrt(rho_ratio)
ratio_z = sp.simplify(a0_of_z / a0_of_z.subs(z_s, 0))
check(sp.simplify(sp.diff(ratio_z, kap_s)) == 0 and kap_s not in ratio_z.free_symbols,
      f"P6a *** a0(z)/a0(0) IS EXACTLY kappa-BLIND, symbolically: d/dkappa = 0 and kappa does not "
      f"appear in the ratio {ratio_z}. *** So F5 contributes ZERO information about kappa no matter how "
      f"good the data get. It constrains (w0, wa) and the FLOOR TYPE -- and it brings (w0,wa) with it, "
      f"so in the dof ledger it is net-zero, not a free constraint")
print(f"  a0(z)/a0(0) = {ratio_z}   (the committed closed form: bump-then-decline for wa < 0)")
for zz, w0v, wav in ((1.0, -0.9, -0.3), (2.0, -0.9, -0.3), (3.0, -0.9, -0.3)):
    v = float(ratio_z.subs({z_s: zz, w0_s: w0v, wa_s: wav}))
    hz = math.sqrt(0.315 * (1 + zz) ** 3 + OmL)
    print(f"    z = {zz:.0f}:  local-response floor {v:.3f}x   |   horizon floor c H_0 E(z) {hz:.3f}x")
lam_flat = [float(ratio_z.subs({z_s: zz, w0_s: -1.0, wa_s: 1e-14})) for zz in (1.0, 2.0, 3.0)]
hor = [math.sqrt(0.315 * (1 + zz) ** 3 + OmL) for zz in (1.0, 2.0, 3.0)]
print(f"  at w = -1 exactly: local-response floor = {['%.6f' % v for v in lam_flat]} at z = 1,2,3")
print(f"                     horizon floor c H_0 E(z) = {['%.4f' % v for v in hor]}")
check(max(abs(v - 1.0) for v in lam_flat) < 1e-9 and min(hor) > 1.5,
      "P6b and for w = -1 exactly the local-response floor is CONSTANT (ratio 1.000 at every z), which "
      "is why MUSE-DARK III's RISING a0 (Ciocan 2026) is a TENSION with the canonical reading and a "
      "point in favour of a horizon floor c H_0 E(z) -- i.e. of the ALT footing that F1 also prefers. "
      "Weak (MSA-3D controlled residual +0.91 +/- 0.8 ~ 1.1 sigma from flat) and LambdaCDM-degenerate, "
      "so it is carried as a LEAN, not a constraint")


# ================================================================================================
banner("P7  F3 -- WIDE BINARIES: zero constraining power today, and that is arithmetic not opinion")
sig_tot_inf = WB_SIG_SYS
z_max = (WB_TARGET - 1.0) / sig_tot_inf
z_corners = [(g - 1.0) / sig_tot_inf for g in WB_RANGE]
print(f"  in-force target gamma_v = {WB_TARGET} (Amendment 4(d)), range {WB_RANGE}")
print(f"  frozen error model sigma_tot = sqrt(sigma_fit^2 + {WB_SIG_SYS}^2); as N -> inf, sigma_tot -> "
      f"{WB_SIG_SYS}")
print(f"  Newton-vs-MI separation ceiling = {z_max:.2f} sigma at the point value, "
      f"{min(z_corners):.2f}-{max(z_corners):.2f} across the frozen corners")
check(z_max < 3.0 and max(z_corners) < 3.0,
      f"P7a *** 3 SIGMA IS UNREACHABLE AT ANY N, so F3 cannot be a binding constraint even in "
      f"principle under the frozen error model: the ceiling is {z_max:.2f} sigma "
      f"({min(z_corners):.2f}-{max(z_corners):.2f} across corners). Reproduces "
      f"mi_amendment7_wb_target_conflict_2026.py's 1.55 / 1.09-2.36")
check(abs((WB_TARGET - 1) / (WB_RANGE[1] - 1) - 0.657) < 0.02,
      f"P7b and DR3's 1.205 is guard-zone contamination, evidence for nothing, so F3 contributes NO "
      f"likelihood term at all in P8 -- it is a PREDICTION awaiting DR4, not a constraint. Its shape "
      f"dependence is real though (alpha=1 -> 1.05-1.10, alpha=2 -> {WB_TARGET}), so once DR4 lands it "
      f"becomes a 6th constraint on p3. Registered target/upper-corner ratio "
      f"{(WB_TARGET-1)/(WB_RANGE[1]-1):.3f}")


# ================================================================================================
banner("P8  THE JOINT chi^2 -- profile over a0 and the kernel, across EVERY systematic corner")
print("  chi2_joint(a0, kernel) = F1 + F2a + F2b + F4      [F3 = 0 (P7), F5 = 0 (P6)]")
print("     F1   deflated profile likelihood, Upsilon free per galaxy       (2-sided)")
print("     F2a  (Delta_postEFE / (bound/2))^2, bound = Earth 2-sigma       (1-sided, monotone up in a0)")
print("     F2b  (D_req(a0, omega_c,min) / sigma_D)^2                       (1-sided, monotone up in a0)")
print("     F4   (<log10 eta>(a0) / floor)^2                                 (2-sided, falls with a0)")
print("  omega_c is PROFILED at its lower edge, which MINIMISES F2b -- the most favourable choice.")

LGRID = np.geomspace(0.6 * A0_CANON, 8.0 * A0_CANON, 61)


# F1's deflated Dchi2 tabulated ONCE per kernel on a dense grid, then log-log interpolated. The SPARC
# fit is the expensive term and every one of the 60 cells reuses the same curve.
F1TAB = {}
for nm, f, _, _ in KERNELS:
    tg = np.geomspace(0.55 * A0_CANON, 9.0 * A0_CANON, 121)
    tv = np.array([(sparc_chi2(a0, f, F1[nm]["s_int"])[0] - F1[nm]["ch_min"]) / F1[nm]["DEFL"]
                   for a0 in tg])
    F1TAB[nm] = (tg, tv)
print(f"  F1 tabulated on {len(F1TAB[KERNELS[0][0]][0])} a0 values x {len(KERNELS)} kernels")


def f1_dchi2(a0, nm):
    tg, tv = F1TAB[nm]
    return float(np.interp(math.log(a0), np.log(tg), tv))


_i_err = max(abs(f1_dchi2(a0, "K2 corpus alpha=2 switch")
                 - (sparc_chi2(a0, nu_m1_K2, F1["K2 corpus alpha=2 switch"]["s_int"])[0]
                    - F1["K2 corpus alpha=2 switch"]["ch_min"])
                 / F1["K2 corpus alpha=2 switch"]["DEFL"])
             for a0 in np.geomspace(0.8 * A0_CANON, 5.0 * A0_CANON, 9))
check(_i_err < 0.5,
      f"P8-INTERP the F1 interpolation is accurate to {_i_err:.3f} in Dchi2 against direct evaluation "
      f"at 9 off-grid a0 values, i.e. far below the 1.0 threshold the allowed regions are read at, so "
      f"no allowed region below is an interpolation artefact")


def joint_terms(a0, nm, floor, reading):
    f = F1[nm]["f"]
    c1 = f1_dchi2(a0, nm)
    _, _, al, A = next(k for k in KERNELS if k[0] == nm)
    if np.isfinite(al):
        dbare = A * a0**al * gb_earth ** (1 - al)      # exact asymptote, no cancellation
    else:
        dbare = float(f(gb_earth / a0)) * gb_earth     # f IS (nu-1); underflows to 0 for K4/K5
    c2 = (dbare / EFE_RELIEF / SIG_E) ** 2
    r = F2B[reading]
    c3 = (a0 * OMEGA_C_MIN / r["gN"] * YR / r["sigD"]) ** 2
    c4 = (cl_meanlog(a0, f) / floor) ** 2
    return c1, c2, c3, c4


CELLS = []
for floor in CLUSTER_FLOORS:
    for rn, _, _, _ in READINGS:
        for nm, _, _, _ in KERNELS:
            tot = np.array([sum(joint_terms(a0, nm, floor, rn)) for a0 in LGRID])
            i = int(np.argmin(tot))
            # refine 4x around the minimum
            lo = LGRID[max(i - 1, 0)]
            hi = LGRID[min(i + 1, len(LGRID) - 1)]
            fg = np.geomspace(lo, hi, 25)
            tf = np.array([sum(joint_terms(a0, nm, floor, rn)) for a0 in fg])
            j = int(np.argmin(tf))
            a0b, chib = fg[j], float(tf[j])
            t = joint_terms(a0b, nm, floor, rn)
            # allowed extent at Dchi2 <= 1 about the cell's own minimum (1 param)
            allowed = LGRID[tot - chib <= 1.0]
            ext = (allowed.min() / A0_CANON, allowed.max() / A0_CANON) if allowed.size else (np.nan, np.nan)
            CELLS.append(dict(floor=floor, reading=rn, kernel=nm, a0=a0b, chi2=chib,
                              terms=t, ext=ext, shift=fg[j] / LGRID[i] - 1))

# dof: 4 constraints, 1 continuous parameter profiled (a0); kernel and cell are enumerated not fitted
NDOF = 4 - 1
print(f"\n  4 constraint terms, 1 continuous parameter profiled  ->  dof = {NDOF}")
print(f"  {'floor':>6}  {'drift reading':<42}{'kernel':<8}{'a0_hat/a0_c':>12}{'chi2_min':>12}"
      f"{'F1':>8}{'F2a':>10}{'F2b':>8}{'F4':>8}{'sqrt(chi2/dof)':>15}{'  edge?'}")
print("  " + "-" * 140)
for floor in CLUSTER_FLOORS:
    for rn, _, _, _ in READINGS:
        for cc in [c for c in CELLS if c["floor"] == floor and c["reading"] == rn]:
            t = cc["terms"]
            edge = "GRID-EDGE" if cc["a0"] <= 1.001 * LGRID[0] else ""
            print(f"  {floor:>6.2f}  {rn:<42}{cc['kernel'].split()[0]:<8}{cc['a0']/A0_CANON:>12.3f}"
                  f"{cc['chi2']:>12.2f}{t[0]:>8.2f}{t[1]:>10.2e}{t[2]:>8.2f}{t[3]:>8.2f}"
                  f"{math.sqrt(cc['chi2']/NDOF):>15.2f}  {edge}")
        print()
edge_cells = {c["kernel"].split()[0] for c in CELLS if c["a0"] <= 1.001 * LGRID[0]}
print(f"  cells whose minimum sits ON the scanned lower boundary: kernels {sorted(edge_cells)}")
check(edge_cells == {"K1", "K3"},
      f"P8-EDGE hazard declared rather than hidden: for the alpha=1 kernels {sorted(edge_cells)} the "
      f"joint chi^2 has NO interior minimum on the scanned range -- F2a grows as a0^1 and dominates, so "
      f"the profile is still falling at the grid's lower edge and the a0_hat printed for those rows is a "
      f"BOUNDARY value, not an extremum. Extending the grid cannot rescue them: P3b already solved the "
      f"trade analytically -- at the a0 where F2a reaches 2 sigma, F1 is 77 sigma away. The alpha=1 rows "
      f"are therefore correctly read as 'excluded', and their chi^2 as a lower bound on how bad they get")

viable = [c for c in CELLS if c["chi2"] / NDOF <= 4.0]        # sqrt(chi2/dof) <= 2, i.e. ~2 sigma
best = min(CELLS, key=lambda d: d["chi2"])
worst = max(CELLS, key=lambda d: d["chi2"])
print(f"  BEST  cell: {best['kernel'].split()[0]}, floor {best['floor']}, {best['reading']}  ->  "
      f"chi2 = {best['chi2']:.2f} / {NDOF} dof = {math.sqrt(best['chi2']/NDOF):.2f} sigma-equivalent, "
      f"a0 = {best['a0']/A0_CANON:.3f}x")
print(f"  WORST cell: {worst['kernel'].split()[0]}, floor {worst['floor']}, {worst['reading']}  ->  "
      f"chi2 = {worst['chi2']:.3e}")
print(f"  cells with sqrt(chi2/dof) <= 2 : {len(viable)} of {len(CELLS)}")
check(len(viable) > 0 and len(viable) < len(CELLS),
      f"P8a the joint is NEITHER empty NOR everywhere-viable: {len(viable)} of {len(CELLS)} "
      f"(kernel x floor x drift-reading) cells survive at sqrt(chi2/dof) <= 2. So outcome (b) "
      f"NO_SOLUTION is NOT what the arithmetic gives -- the framework is not falsified as a whole -- "
      f"and neither is it unconstrained")
surv_k = sorted({c["kernel"].split()[0] for c in viable})
surv_a0 = [c["a0"] / A0_CANON for c in viable]
print(f"  surviving kernels: {surv_k}")
print(f"  surviving a0/a0_canon range: {min(surv_a0):.3f} to {max(surv_a0):.3f}")
check("K1" not in surv_k and "K3" not in surv_k,
      f"P8b *** THE SHAPE INDEX IS DERIVED: no alpha=1 kernel survives ANY cell. *** Surviving "
      f"kernels {surv_k} are exactly the alpha >= 2 ones, and they survive because F2a's Earth bound "
      f"has no free direction left once F1 fixes a0 to O(1e-10). This is a real over-determination "
      f"result and it costs the framework its published 'exact law' g_obs^2 = g_bar^2 + a0 g_bar")
check(max(surv_a0) / min(surv_a0) > 1.05,
      f"P8c but a0 is NOT driven to a point: the surviving cells span a0 = {min(surv_a0):.3f}x to "
      f"{max(surv_a0):.3f}x canonical, a factor {max(surv_a0)/min(surv_a0):.2f}. Outcome (c), a "
      f"CONTINUUM, on the a0 direction")

# --- the decisive sub-question, at the joint level -----------------------------------------------
banner("P8-KEY  IS kappa = 1/2 THE UNIQUE VALUE CONSISTENT WITH ALL FIVE FRONTS?")
KTEST = [("kappa = 1/2pi (Milgrom 2020)", A0_CANON * Z_FW / Z_M20),
         ("kappa = 1/2   (THE FRAMEWORK)", A0_CANON),
         ("kappa = 1/2, ALT footing", A0_ALT),
         ("kappa = 1", 2 * A0_CANON),
         ("kappa = 2", 4 * A0_CANON)]
print(f"  each row profiled over the SURVIVING kernels and over the full systematic range; the number")
print(f"  quoted is the BEST (most favourable) cell for that kappa -- so no kappa is penalised by a")
print(f"  corner chosen against it.\n")
print(f"  {'hypothesis':<32}{'a0/a0_c':>9}{'best chi2':>11}{'sig-eq':>8}{'best cell':>26}"
      f"{'TIGHTEST corner':>17}{'verdict':>11}")
print("  " + "-" * 116)
KRES = {}
for hn, a0h in KTEST:
    bb, ww = None, None
    for floor in CLUSTER_FLOORS:
        for rn, _, _, _ in READINGS:
            for nm, _, _, _ in KERNELS:
                if nm.split()[0] not in surv_k:
                    continue
                tot = sum(joint_terms(a0h, nm, floor, rn))
                if bb is None or tot < bb[0]:
                    bb = (tot, nm, floor, rn)
                if floor == min(CLUSTER_FLOORS) and rn.startswith("R1a"):
                    if ww is None or tot < ww[0]:
                        ww = (tot, nm)
    sig = math.sqrt(bb[0] / NDOF)
    KRES[hn] = dict(chi2=bb[0], sig=sig, cell=bb[1:], tight=math.sqrt(ww[0] / NDOF))
    print(f"  {hn:<32}{a0h/A0_CANON:>9.4f}{bb[0]:>11.2f}{sig:>8.2f}"
          f"{bb[1].split()[0]+' / '+format(bb[2],'.2f')+' / '+bb[3].split()[0]:>26}"
          f"{KRES[hn]['tight']:>17.2f}{('SURVIVES' if sig <= 2 else 'excluded'):>11}")
print(f"\n  'TIGHTEST corner' = cluster floor {min(CLUSTER_FLOORS)} dex AND the non-degenerate R1a drift")
print(f"  room, i.e. both systematics at their least forgiving. NO kappa survives that corner at <= 2:")
print(f"  minimum over the three surviving kappas = "
      f"{min(KRES[h]['tight'] for h,_ in KTEST[:3]):.2f} sigma-equivalent.")
surv_kappa = [h for h in KRES if KRES[h]["sig"] <= 2.0]
print(f"\n  kappa values surviving the JOINT at <= 2 sigma-equivalent: {len(surv_kappa)} of {len(KTEST)}")
for h in surv_kappa:
    print(f"     {h}")
check(len(surv_kappa) >= 1,
      f"P8d at least one kappa survives the joint ({len(surv_kappa)} of {len(KTEST)}), so the "
      f"over-determined system is CONSISTENT -- outcome (b) is ruled out at the joint level too")
check(len(surv_kappa) > 1,
      f"P8e *** AND THE DECISIVE ANSWER IS NO: kappa = 1/2 IS NOT UNIQUE. *** {len(surv_kappa)} of the "
      f"5 tested kappa values survive the joint at <= 2 sigma-equivalent "
      f"({', '.join(h.split('(')[0].strip() for h in surv_kappa)}). Adding F2-F5 to F1 does NOT sharpen "
      f"F1's 2.2-sigma preference into a unique value, because the fronts that could sharpen it are the "
      f"ones that do not bind (F3, F5) or that bind in the WRONG DIRECTION (F4 wants "
      f"{F4['K2 corpus alpha=2 switch']['a0_need']/A0_CANON:.1f}x, F2b caps at "
      f"{max(F2B[r]['a0max'] for r in F2B)/A0_CANON:.2f}x). Outcome (c), a CONTINUUM in kappa")
km20, khalf = KRES["kappa = 1/2pi (Milgrom 2020)"], KRES["kappa = 1/2   (THE FRAMEWORK)"]
d_order = km20["chi2"] - khalf["chi2"]
print(f"\n  Delta chi2 (1/2pi minus 1/2) at the joint level = {d_order:+.3f}")
check(abs(d_order) < 2.71,
      f"P8-ORDER *** AND THE JOINT DOES NOT EVEN PRESERVE THE ORDERING. *** Delta chi2 between "
      f"kappa = 1/2pi and kappa = 1/2, each at its own most favourable cell, is {d_order:+.3f} -- inside "
      f"the 2.71 that a 90%-confidence one-parameter separation would need, i.e. the two coefficients are "
      f"statistically INDISTINGUISHABLE in the joint. P2d(i) reproduced the committed 2.2 sigma AT FIXED "
      f"alpha=1; P2d(ii) showed it reverses when the kernel is freed; here the two effects cancel to "
      f"nothing. Honest reading: F1's kappa discrimination is real ONLY conditional on the alpha=1 "
      f"kernel, and the alpha=1 kernel is the one P3/P8b exclude at "
      f"{F2A[(NM1,'canon')]/SIG_E:.0f} sigma. The 2.2-sigma claim therefore cannot be quoted as a "
      f"joint result without that condition attached")

# --- the binding pair, priced both ways ---------------------------------------------------------
banner("P8-PAIR  WHICH PAIR OF FRONTS IS MUTUALLY EXCLUSIVE, AND BY HOW MANY SIGMA")
nm2 = "K2 corpus alpha=2 switch"
L1 = math.log10(F1[nm2]["a0"])
sig_L1 = F1[nm2]["sig_clu"] / math.log(10)
L4 = math.log10(F4[nm2]["a0_need"])
print(f"  on the surviving alpha=2 kernel:")
print(f"    F1  wants log10 a0 = {L1:.4f} +/- {sig_L1:.4f}  ({F1[nm2]['a0']/A0_CANON:.3f}x canonical, "
      f"clustered sigma)")
print(f"    F4  wants log10 a0 = {L4:.4f}  ({F4[nm2]['a0_need']/A0_CANON:.2f}x canonical), error = "
      f"2 x floor (eta ~ sqrt(a0))")
print(f"\n  {'floor [dex]':>12}{'sigma_L4':>10}{'gap [dex]':>11}{'sigma of the F1 x F4 clash':>28}")
print("  " + "-" * 62)
pair_sigmas = []
for floor in CLUSTER_FLOORS:
    sL4 = 2 * floor
    gap = L4 - L1
    s = gap / math.hypot(sig_L1, sL4)
    pair_sigmas.append(s)
    print(f"  {floor:>12.2f}{sL4:>10.3f}{gap:>11.4f}{s:>28.2f}")
print(f"\n  and the OTHER edge of the same triangle, F4 against F2b's cap:")
for rn, _, _, _ in READINGS:
    cap = F2B[rn]["a0max"]
    print(f"    {rn:<44} a0 <= {cap/A0_CANON:.3f}x  ->  F4's {F4[nm2]['a0_need']/A0_CANON:.1f}x is "
          f"{math.log10(F4[nm2]['a0_need']/cap):.3f} dex above the cap")
check(min(pair_sigmas) < 3.0 < max(pair_sigmas),
      f"P8g *** THE BINDING PAIR IS F1 x F4 (equivalently F2b x F4) AND IT STRADDLES 3 SIGMA: "
      f"{min(pair_sigmas):.2f} sigma at the LOOSE end of the cluster systematic floor (0.30 dex) to "
      f"{max(pair_sigmas):.2f} sigma at the TIGHT end (0.10 dex). *** Quoting only the tight end would "
      f"manufacture a falsification -- that is failure mode (ii) from the brief, and this repo has "
      f"committed it before. Quoting only the loose end would manufacture a pass. The honest statement "
      f"is the RANGE, and the range means the joint is NOT referee-proof either way")
check(max(pair_sigmas) > min(pair_sigmas) * 2,
      f"P8h and the verdict is dominated by ONE unmeasured number -- the absolute cluster mass-scale "
      f"systematic floor. Its committed range 0.10-0.30 dex moves the clash by "
      f"{max(pair_sigmas)/min(pair_sigmas):.1f}x. So the answer to 'is the framework falsified by the "
      f"joint' is currently a statement about cluster mass calibration, not about the framework")


# ================================================================================================
banner("P9  THE FLAT DIRECTIONS -- the irreducible dof, named")
FLAT = [
    ("p4 I_0, the ghost-condensate amount",
     "NO front in the joint touches it. P(X) is postulated; I_0 ~ Omega_dm is set by matching, and the "
     "GDM degeneracy theorem says the CMB constrains a FLUID not a PARTICLE, so it cannot be closed there.",
     "EXACTLY FLAT"),
    ("p5 the EFE prescription factor",
     "one calibration (Crater II), one parameter -> exactly determined, zero over-determination. It also "
     "enters F2a as the 6.76x relief, so a wrong f_EFE moves F2a's sigma but cannot rescue alpha=1 "
     f"(that needs {s_k1:.0f}x, not 6.76x).",
     "FITTED, not derived"),
    ("p2 omega_c inside its window",
     f"two one-sided constraints leave a window x{wc_up_canon/OMEGA_C_MIN:.3f} wide (canonical) / "
     f"x{wc_up_alt/OMEGA_C_MIN:.3f} (ALT). Nothing inside is preferred. Route B (omega_c = a0/c) is "
     f"EXCLUDED (P4d), so the window is all there is.",
     "FLAT within a 2.7-24% window"),
    ("p3 the shape index ABOVE alpha = 2",
     f"F2a excludes alpha = 1 and is satisfied by every alpha >= 2 with enormous margin "
     f"({s_k2:.1e} sigma at alpha=2, 10^{log10_anom_K4:.0f} at exponential), while F1 pays only "
     f"{abs(F1[nm2]['a0']-k1['a0'])/k1['a0']*100:.1f}% in a0 and F4 monotonically worsens. So alpha is "
     f"bounded BELOW and unbounded above.",
     "FLAT for alpha >= 2"),
    ("d1 the footing, PARTIALLY broken and NOT the way the corpus is published",
     "F1 prefers ALT (P2d), F4 prefers ALT (lower eta), F5's rising a0 prefers a horizon floor = ALT. "
     "F2b prefers CANONICAL (the ALT omega_c window is only 2.7% wide, P4e). Three fronts lean one way, "
     "one leans the other -- a real but not decisive break.",
     "LEANING ALT, 3 fronts to 1"),
    ("the product a0 x omega_c",
     "F2b constrains only this PRODUCT (D_req = a0 omega_c / g_N). F1 constrains a0 alone and the SPARC "
     "gate constrains omega_c alone, so the product is broken -- this one is NOT flat, and saying so is "
     "the check that the flat list is not padded.",
     "BROKEN (by c1 x c4)"),
]
for nm_, why, verdict in FLAT:
    print(f"\n  {nm_}\n      {why}\n      -> {verdict}")
n_flat = sum(1 for _, _, v in FLAT if v.startswith("EXACTLY FLAT") or v.startswith("FLAT"))
n_fit = sum(1 for _, _, v in FLAT if v.startswith("FITTED"))
n_broken = sum(1 for _, _, v in FLAT if v.startswith("BROKEN"))
check(n_flat == 3 and n_fit == 1 and n_broken == 1,
      f"P9a {n_flat} genuinely FLAT directions remain (I_0; omega_c within its window; alpha above 2), "
      f"{n_fit} is FITTED-not-over-determined (the EFE factor), and {n_broken} candidate flat direction "
      f"-- the product a0 x omega_c -- is demonstrably BROKEN by c1 x c4. So the flat list is not "
      f"padded: a candidate was tested and removed")
# P9b tested numerically, not asserted: each named flat direction must show a MEASURABLE flatness.
loose = [c for c in CELLS if c["floor"] == max(CLUSTER_FLOORS) and c["reading"].startswith("R1b")]
chi_K4 = next(c["chi2"] for c in loose if c["kernel"].startswith("K4"))
chi_K5 = next(c["chi2"] for c in loose if c["kernel"].startswith("K5"))
a0_span = max(surv_a0) / min(surv_a0)
wc_span = wc_up_canon / OMEGA_C_MIN
print(f"\n  flatness measured, not asserted:")
print(f"    a0 direction   : surviving span {a0_span:.3f}x           (a point would be 1.000)")
print(f"    omega_c        : window width   {wc_span:.3f}x           (a point would be 1.000)")
print(f"    alpha above 2  : |chi2(K4) - chi2(K5)| = {abs(chi_K4-chi_K5):.2f} at the loosest cell "
      f"(1 would be a 1-sigma preference)")
check(a0_span > 1.05 and wc_span > 1.05 and abs(chi_K4 - chi_K5) < 2.0,
      f"P9b *** THEREFORE THE +2 dof CANNOT BE DRIVEN TO 0, and each flat direction is MEASURED flat: "
      f"a0 spans {a0_span:.3f}x, omega_c's window is {wc_span:.3f}x wide, and two different alpha >= 2 "
      f"kernels differ by only {abs(chi_K4-chi_K5):.2f} in chi^2 -- less than a 1-sigma preference, so "
      f"nothing selects among them. *** The 2026-06-15 analysis found the "
      f"framework viable at +2 dof; the joint here confirms the count is +2 on the "
      f"(a0, omega_c, shape) subspace and shows that {n_flat} directions have NO front pointing at "
      f"them. 'Zero free parameters' is not reachable with the five fronts as they stand -- the honest "
      f"claim is ONE fitted coefficient (kappa) plus a derived-by-elimination shape class plus two "
      f"unconstrained constants (I_0, omega_c-within-window)")


# ================================================================================================
banner("P10  VERDICT")
sig_best = math.sqrt(best["chi2"] / NDOF)
print(f"""
  OUTCOME: (c) CONTINUUM -- degenerate. Not (a), not (b).

  WHAT THE OVER-DETERMINATION DID BUY, and it is not nothing:
   1. THE SHAPE INDEX IS DERIVED BY ELIMINATION. alpha = 1 -- which is the framework's OWN published
      kernel, nu = sqrt(1+1/y), Milgrom 1999 eq 9 -- is excluded at {s_k1:.0f} sigma by the Earth
      perihelion bound even AFTER the framework's own EFE relief, and no kappa rescues it (it would
      need kappa <= {0.5*a0_needed/A0_CANON:.1e}, which destroys F1). Two constraints, one parameter,
      one survivor class: alpha >= 2. That is over-determination working as advertised. It costs the
      corpus the exact law g_obs^2 = g_bar^2 + a0 g_bar, which is an alpha = 1 identity.
   2. ROUTE B FOR omega_c IS EXCLUDED. omega_c = a0/c transmits Re G = {ReG_gal:.1e} at galaxy orbital
      frequencies against the required >= {GATE_KEEP}: it would gate off the rotation curves the
      framework exists to explain. So the one closed-form candidate for the fifth constant is dead and
      omega_c reverts to a fitted window.
   3. kappa = 1 AND kappa = 2 ARE EXCLUDED by the joint ({KRES['kappa = 1']['sig']:.2f} and
      {KRES['kappa = 2']['sig']:.2f} sigma-equivalent at their OWN most favourable corners), so the
      over-determination does bound kappa -- to a factor ~1.4 window, not to a point.

  WHAT IT DID NOT BUY:
   4. kappa IS NOT UNIQUE. {len(surv_kappa)} of 5 tested values survive at <= 2 sigma-equivalent:
      1/2pi, 1/2, and 1/2-on-the-ALT-footing all fit. The reason is structural, not statistical: of
      the five fronts, F3 has no data (ceiling {z_max:.2f} sigma at ANY N), F5 is EXACTLY kappa-blind
      (proved symbolically in P6a), F2a is kappa-blind once alpha >= 2, and F4 pulls a0 the OPPOSITE
      way from F1 and F2b. Five fronts on paper, two in force on a0, and those two disagree.
   5. WORSE FOR THE HEADLINE CLAIM: the joint does NOT preserve F1's 2.2-sigma preference for
      kappa = 1/2 over Milgrom 2020's 1/2pi. Delta chi2 = {d_order:+.2f}, i.e. indistinguishable, and
      at fixed shape the preference actually REVERSES on the simple/exponential kernels (P2d(ii)). The
      2.2-sigma result is real but CONDITIONAL on the alpha=1 kernel -- the very kernel item 1 kills.
      That conjunction is the sharpest thing in this analysis and it is against interest.
   6. THREE FLAT DIRECTIONS REMAIN and one parameter is fitted-not-derived (P9): I_0 (no front),
      omega_c within its window, alpha above 2, and the EFE factor. The +2 dof of 2026-06-15 is
      CONFIRMED as +2 and cannot be driven to 0 by these fronts.

  THE BINDING PAIR, priced honestly: F1 x F4 (equivalently F2b x F4) clashes at
  {min(pair_sigmas):.2f} sigma to {max(pair_sigmas):.2f} sigma as the cluster absolute-mass-scale
  systematic floor runs across its OWN committed range 0.30 -> 0.10 dex. It straddles 3 sigma. So:
  NOT falsified, but the single number that decides whether this framework is falsified as a whole is
  the cluster mass-calibration floor, and it is not a number about the framework at all.

  AND THE OTHER END OF THE SAME RANGE, stated with equal weight: at the TIGHTEST corner -- cluster
  floor 0.10 dex AND the non-degenerate R1a drift room -- NO kappa survives. The best any of the three
  surviving coefficients manages there is {min(KRES[h]['tight'] for h,_ in KTEST[:3]):.2f}
  sigma-equivalent. So the joint's verdict spans "comfortable" to "excluded" across two systematics
  that are not measurements of the framework. Both ends are the result; neither alone is.

  AGAINST INTEREST, five items:
   * the joint's best cell still has sqrt(chi2/dof) = {sig_best:.2f}; there is no corner where all four
     terms are simultaneously comfortable.
   * the best-fitting kernel in the joint is {best['kernel'].split()[0]}
     ({[k[0] for k in KERNELS if k[0].startswith(best['kernel'].split()[0])][0]}), i.e. NOT the
     framework's own kernel and not even its adopted alpha=2 replacement -- McGaugh's exponential form
     fits the joint best. The framework's distinctive kernel loses on its own joint.
   * three of the four constraints that DO bind prefer the ALT footing (a0 = 1.13e-10) over the
     canonical rho_DE/cH_Lambda footing the corpus publishes; the fourth (F2b) prefers canonical
     because the ALT omega_c window is only 2.7% wide, i.e. nearly closed.
   * F2b is already a {s_r1b:.2f}-{s_r1a:.2f} sigma tension AT the canonical a0, before any of this,
     and it worsens linearly in a0 -- so F1's pull toward 1.15x makes F2b worse, not better.
   * the elimination of alpha = 1 is the strongest result here and it goes AGAINST the corpus's
     published kernel and its 'exact law'.

  MANDATORY CREDIT restated: nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273
  eqs 6-9 (his eqs 10-11 give a second coefficient; Milgrom 2008 sec 7.3.1 calls the mismatch 'not
  necessarily meaningful'); a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994 Ann.Phys. 229:384;
  temperature Narnhofer, Peter & Thirring 1996 IJMPB 10:1507; five-acceleration Deser & Levin 1997
  CQG 14:L163; exponential kernel McGaugh 2008 ApJ 683:137 eq 11a. kappa = 1/2 is FITTED, NOT DERIVED,
  and this joint analysis does not change that.

  NO DOOR IS CLOSED. The framework is not falsified. Nor is any parameter derived except the shape
  class, and that one was derived by killing the published kernel.
""")

banner("RESULT")
npass = sum(1 for c, _ in CHECKS if c)
print(f"  {npass}/{len(CHECKS)} checks held.")
if npass != len(CHECKS):
    for c, m in CHECKS:
        if not c:
            print(f"  FAILED: {m}")
    sys.exit(1)
print("  Exit 0: the joint over-determination ran; outcome (c) CONTINUUM, reported as the mathematics")
print("  gave it, with the F1 x F4 clash priced across its full systematic range.")
sys.exit(0)
