#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage17_a0z_from_the_action_2026.py
===================================
a_0(z) DERIVED FROM THE ACTION -- the MOND scale is the dark sector's PRESSURE.

        *** a_0^2(Q) = kappa^2 c^2 G (-K(Q)) / c^2 ,   i.e.   a_0 = kappa c sqrt( G(-p_Q)/c^2 ) ***

One covariant promotion of the constant a_0 in THE_COMPLETION's action, ZERO new parameters, ONE new
relation (mu^2 Lambda_D^2 = M^4), and the a_0(z) law -- which until tonight was IMPOSED on the theory
-- becomes an OUTPUT of the theory, with w = -1 exact PRESERVED.

--------------------------------------------------------------------------------------------------
THE THEOREM THAT FORCES IT (found independently by an adversarial Gemini pass tonight, and it is
CORRECT -- credited here because it closes the naive route and thereby selects this one)
--------------------------------------------------------------------------------------------------
The naive promotion is a_0^2 propto rho_Q (the DENSITY).  Theorem: on the vacuum branch w_Q = -1
exactly ==> rho_Q = const ==> a_0 = const.  And with the charge turned on, rho_Q = M^4 + dust GROWS
into the past ==> a_0 RISES toward recombination ==> MOND ON at the CMB ==> fatal.  So the density
promotion yields either NO evolution or the WRONG SIGN of evolution.  Both branches dead.

But the action contains a SECOND scalar that equals rho_Lambda today: the PRESSURE, and p = K(Q) is
an IDENTITY in this sector (row 1.2 of THE_COMPLETION).  Under a_0^2 propto -K(Q):
    * today (u -> 0):        -K = M^4 = rho_Lambda  ==> a_0 = kappa c sqrt(G rho_Lambda) EXACTLY --
                             the committed coefficient, to the digit, with kappa = 1/2 untouched;
    * into the past:         the excitation's POSITIVE pressure climbs the DBI wall and eats the
                             offset's negative pressure ==> -p_Q falls ==> a_0 falls ==> MOND OFF at
                             recombination.  THE RIGHT SIGN, from the action's own dynamics;
    * and w = -1 stays EXACT: the vacuum never rolls.  rho_DE = M^4 = const throughout.  It is the
                             TOTAL PRESSURE that evolves, not the dark energy.
The fork "preserve w = -1  ==>  a_0 = const" is FALSE for the pressure promotion.  That is the
central structural finding of this stage.

Backreaction bonus, and it is decisive for health: the promotion feeds back into the Q equation
through d(a_0^2)/dQ.  For the density promotion that is  Q K'' = O(mu^2), UNSUPPRESSED.  For the
pressure promotion it is  -K' = -n, the CHARGE -- and the charge is trace (Part F).  The feedback is
suppressed by the very smallness the rest of the construction requires.

--------------------------------------------------------------------------------------------------
WHAT COMES OUT
--------------------------------------------------------------------------------------------------
  closed form:      a_0^2(z)/a_0^2(0) = [1 - beta(1 - 1/sqrt(1+nu^2))] / [1 - beta(1 - 1/sqrt(1+nu_0^2))]
                    with nu(z) = nu_0 (1+z)^3  (exact, from n propto a^-3)  and  beta = mu^2 Lambda_D^2 / M^4
  the relation:     beta = 1, i.e. K(saturation) = 0 -- THE LAGRANGIAN VANISHES AT THE DBI WALL.
                    Selected by the CMB off-switch; removes one free parameter (Lambda_D = M^2/mu).
  the law:          a_0 constant to <0.01% through z = 0-5, then (1+z)^(-3/2) decline, transition at
                    z_t = nu_0^(-1/3) - 1 in [18, 36], off at recombination.  NO bump at z ~ 0.5
                    (the banked DESI-CPL law had +6%; that dressing was never self-consistent with
                    the sector's own w = -1 and is REPLACED, not refined).
  the window:       nu_0 in [2.1e-5, 1.8e-4] -- cut from BELOW by the off-switch strength and from
                    ABOVE by the RAR (via the drain bound), nonempty by a factor ~8.
  load-bearing irony: stages 2-3's ADVERSE result (captured charge drains to the centre; no halo)
                    is REQUIRED here -- had the charge lingered at MOND radii, the local pressure
                    would kill a_0 exactly where the RAR needs it.  The 2d-adverse dynamics and the
                    a_0(z) derivation need each other.
"""

import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ---- constants / committed anchors --------------------------------------------------------------
C_SI = mp.mpf("2.99792458e8")
G_SI = mp.mpf("6.67430e-11")
MPC = mp.mpf("3.0856775814913673e22")
H0 = mp.mpf("67.4") * 1000 / MPC                 # s^-1
OM_L = mp.mpf("0.685")
OM_M = mp.mpf("0.315")
KAPPA = mp.mpf("0.5")
A0_COMMITTED = mp.mpf("9.3619e-11")              # m/s^2, the canonical committed value
W0, WA = mp.mpf("-0.75"), mp.mpf("-0.86")        # DESI CPL, for the BANKED law comparison
Z_REC = mp.mpf("1090")

rho_crit = 3 * H0 ** 2 / (8 * mp.pi * G_SI)      # kg/m^3
rho_L = OM_L * rho_crit

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the two candidate promotions, and the one-bit selection between them")
print("=" * 100)

u_s, Q0_s, mu_s, LD_s, M4_s = sp.symbols("u Q_0 mu Lambda_D M4", positive=True)
K_s = -M4_s + mu_s ** 2 * LD_s ** 2 * (1 - sp.sqrt(1 - u_s ** 2 / LD_s ** 2))
n_s = sp.diff(K_s, u_s)                                    # n = K'(Q), the conserved charge density
rho_s = (Q0_s + u_s) * n_s - K_s                           # committed exact thermodynamics
p_s = K_s

check(sp.simplify(n_s - mu_s ** 2 * u_s / sp.sqrt(1 - u_s ** 2 / LD_s ** 2)) == 0,
      "A1  charge density from the DBI, exact: n = K' = mu^2 u / sqrt(1 - u^2/Lambda_D^2)",
      "sympy, from the committed K(Q)")

check(sp.simplify(rho_s.subs(u_s, 0) - M4_s) == 0 and sp.simplify(p_s.subs(u_s, 0) + M4_s) == 0,
      "A2  vacuum branch u = 0: rho = M^4, p = -M^4 ==> w = -1 EXACT -- and it stays exact under the "
      "pressure promotion because the promotion never moves the offset",
      "this is the branch Gemini's theorem lives on, and the promotion does not touch it")

# the density promotion rises; the pressure promotion falls -- exact signs from the thermodynamics
drho_du = sp.simplify(sp.diff(rho_s, u_s))
dnegK_du = sp.simplify(sp.diff(-K_s, u_s))
check(sp.simplify(drho_du - (Q0_s + u_s) * sp.diff(K_s, u_s, 2)) == 0
      and sp.simplify(dnegK_du + n_s) == 0,
      "A3  *** THE ONE-BIT SELECTION: d(rho)/du > 0 (density GROWS with excitation ==> a_0 would RISE "
      "into the past ==> MOND ON at the CMB, fatal) while d(-K)/du = -n < 0 (pressure scalar FALLS "
      "with excitation ==> a_0 falls into the past ==> MOND OFF at the CMB, required). ***",
      "one bit of CMB physics selects the pressure promotion over the density promotion")

check(sp.simplify(sp.diff(-K_s, u_s) + n_s) == 0,
      "A4  and the promotion's backreaction on the Q equation is d(a_0^2)/dQ propto -K' = -n: "
      "CHARGE-SUPPRESSED.  The density promotion's is d(rho)/dQ = Q K'' = O(mu^2), unsuppressed",
      "the healthy candidate is also the selected one -- these were not guaranteed to coincide")

# deep-MOND F ~ y^(3/2): the Y-sector's contribution to the Q equation vanishes on FRW
y_s, cF = sp.symbols("y c_F", positive=True)
F_deep = cF * y_s ** sp.Rational(3, 2)
feedback = sp.simplify(F_deep - y_s * sp.diff(F_deep, y_s))
check(sp.limit(feedback, y_s, 0) == 0,
      "A5  F(y) - y F'(y) -> 0 as y -> 0 for the deep-MOND F ~ y^(3/2) (it equals -c y^(3/2)/2), and "
      "Y = 0 identically on FRW ==> the promoted Y-sector does NOT alter the background Q equation: "
      "charge conservation n propto a^-3 survives EXACTLY",
      "Gemini's F(0) = 0 condition, verified for the actual kernel's deep-MOND limit; the feedback "
      "lives only in perturbations, where it carries the extra factor n (A4)")

# today's endpoint: the committed coefficient, to the digit
a0_today = KAPPA * C_SI * mp.sqrt(G_SI * rho_L)
check(abs(a0_today / A0_COMMITTED - 1) < mp.mpf("0.01"),
      f"A6  today's endpoint: u -> 0 gives -K = M^4 = rho_Lambda and a_0 = kappa c sqrt(G rho_Lambda) "
      f"= {sig(a0_today, 5)} m/s^2 vs the committed 9.3619e-11 ({sig(100 * abs(a0_today / A0_COMMITTED - 1), 2)}% "
      "= parameter-choice rounding)",
      "the coefficient, kappa = 1/2 and all, passes through the promotion untouched")


# =================================================================================================
print()
print("=" * 100)
print("PART B -- the exact background law")
print("=" * 100)

nu_s, beta_s = sp.symbols("nu beta", positive=True)
# invert n(u) exactly: s = u/Lambda_D = nu/sqrt(1+nu^2),  nu = n/(mu^2 Lambda_D)
s_of_nu = nu_s / sp.sqrt(1 + nu_s ** 2)
n_check = sp.simplify((mu_s ** 2 * (s_of_nu * LD_s)
                       / sp.sqrt(1 - s_of_nu ** 2)) / (mu_s ** 2 * LD_s))
check(sp.simplify(n_check - nu_s) == 0,
      "B1  exact inversion of the charge relation: s = u/Lambda_D = nu/sqrt(1+nu^2) with "
      "nu = n/(mu^2 Lambda_D), so nu(z) = nu_0 (1+z)^3 EXACTLY from n propto a^-3",
      "no approximation anywhere in the background law")

negK_nu = sp.simplify((-K_s).subs(u_s, s_of_nu * LD_s))
negK_target = M4_s - mu_s ** 2 * LD_s ** 2 * (1 - 1 / sp.sqrt(1 + nu_s ** 2))
check(sp.simplify(negK_nu - negK_target) == 0,
      "B2  *** THE CLOSED FORM: -K(nu) = M^4 - mu^2 Lambda_D^2 (1 - 1/sqrt(1+nu^2)) ***, hence with "
      "beta = mu^2 Lambda_D^2/M^4:  a_0^2(z)/a_0^2(0) = [1 - beta(1 - (1+nu^2)^(-1/2))] / "
      "[1 - beta(1 - (1+nu_0^2)^(-1/2))]",
      "sympy-verified from the committed K(Q); this IS the derived a_0(z) law")


def a0_ratio_derived(z, nu0, beta=mp.mpf(1)):
    nu = nu0 * (1 + mp.mpf(z)) ** 3
    num = 1 - beta * (1 - 1 / mp.sqrt(1 + nu ** 2))
    den = 1 - beta * (1 - 1 / mp.sqrt(1 + nu0 ** 2))
    return mp.sqrt(num / den)


def a0_ratio_banked(z):
    z = mp.mpf(z)
    return (1 + z) ** (mp.mpf("1.5") * (1 + W0 + WA)) * mp.e ** (-mp.mpf("1.5") * WA * z / (1 + z))


# =================================================================================================
print()
print("=" * 100)
print("PART C -- the relation beta = 1: the Lagrangian vanishes at the DBI wall")
print("=" * 100)

# how exact must beta = 1 be for the off-switch?  floor of a_0^2 is (1-beta) as nu -> inf
off_target = mp.mpf("0.006")                      # the banked benchmark a_0(rec)/a_0(0)
beta_floor = 1 - off_target ** 2
check(beta_floor > mp.mpf("0.99996"),
      f"C1  the off-switch requires the floor (1-beta) <= (0.006)^2 = {sig(off_target ** 2, 2)}: "
      f"beta = 1 to 3.6e-5.  The natural reading is the IDENTITY K(saturation) = 0 -- the dark "
      f"sector's Lagrangian VANISHES exactly at the DBI wall",
      "the sector switches itself off, Lagrangian-wise, exactly where MOND switches off")

info("C2  beta = 1 is ONE new relation among EXISTING parameters -- mu^2 Lambda_D^2 = M^4, i.e. "
     "Lambda_D = M^2/mu -- so the dark sector LOSES a free parameter (5 -> 4) while gaining the "
     "entire a_0(z) function as output.  The alternative reading, beta tuned to 1 to 4 decimal "
     "places without a principle, is stated rather than hidden: nothing in tonight's work DERIVES "
     "K(sat) = 0; it is selected by the off-switch and then held as a structural identity.")

nu0_floor = mp.mpf(1) / ((1 + Z_REC) ** 3 * off_target ** 2)
check(abs(a0_ratio_derived(Z_REC, nu0_floor) / off_target - 1) < mp.mpf("0.02"),
      f"C3  off-switch floor on the charge: nu_0 >= {sig(nu0_floor, 3)} reproduces "
      f"a_0(1090)/a_0(0) = {sig(a0_ratio_derived(Z_REC, nu0_floor), 3)} -- the banked 0.006, which the "
      "banked DESI-CPL law also gives (Gemini independently verified 0.00603)",
      "below this charge the transition happens too late and MOND is still on at recombination")


# =================================================================================================
print()
print("=" * 100)
print("PART D -- the window on nu_0, cut from both ends by physics already committed")
print("=" * 100)

# ceiling 1: forest constancy is automatic in-window (checked in E); the REAL ceiling is the RAR.
# drain bound: captured charge free-falls (stages 2-3), residence fraction ~ t_ff/t_H at the g = a_0
# radius; local overdensity of a clustered cold species there ~ 1.5e5; the derived a_0 is local.
T_FF_OVER_TH = (mp.mpf("15") * MPC / 1000 / mp.mpf("2.0e5")) / (mp.mpf("4.35e17"))
DELTA_HALO = mp.mpf("1.5e5")                     # rho_dm-like/mean at ~15 kpc if it DID cluster
drain_gain = DELTA_HALO * T_FF_OVER_TH
nu_loc_max = mp.mpf("0.141")                     # keeps the local a_0^2 shift below 1%
nu0_ceiling = nu_loc_max / drain_gain

print(f"\n   drain arithmetic: t_ff(15 kpc)/t_H = {sig(T_FF_OVER_TH, 3)}, would-be overdensity "
      f"{sig(DELTA_HALO, 3)} ==> effective local gain {sig(drain_gain, 3)}x")
check(nu0_ceiling > nu0_floor,
      f"D1  *** THE WINDOW IS NONEMPTY: nu_0 in [{sig(nu0_floor, 3)}, {sig(nu0_ceiling, 3)}] -- a "
      f"factor {sig(nu0_ceiling / nu0_floor, 3)} -- cut from BELOW by the CMB off-switch and from "
      f"ABOVE by the RAR through the drain bound ***",
      "two unrelated observables squeeze the same dimensionless charge and leave room")

zt_lo = nu0_ceiling ** (mp.mpf(-1) / 3) - 1
zt_hi = nu0_floor ** (mp.mpf(-1) / 3) - 1
check(zt_lo > 5 and zt_hi < Z_REC,
      f"D2  the transition redshift z_t = nu_0^(-1/3) - 1 lies in [{sig(zt_lo, 3)}, {sig(zt_hi, 3)}]: "
      "ABOVE the entire forest range (z <= 5) and BELOW recombination for the whole window",
      "the law is constant where MOND is tested and off where the CMB needs it off -- for every "
      "allowed charge, not by tuning")

# the load-bearing irony, quantified: NO drain ==> nu_loc = nu_0 * DELTA_HALO
nu_loc_nodrain = nu0_floor * DELTA_HALO
a0_supp_nodrain = (1 + nu_loc_nodrain ** 2) ** (mp.mpf(-1) / 4)
check(a0_supp_nodrain < mp.mpf("0.75"),
      f"D3  *** WITHOUT the drain (i.e. had the captured charge formed a halo), even the MINIMUM "
      f"off-switch charge gives nu_loc = {sig(nu_loc_nodrain, 3)} at the g = a_0 radius ==> local a_0 "
      f"suppressed to {sig(a0_supp_nodrain, 3)} of nominal -- RAR-fatal at 0.108 dex.  Stages 2-3's "
      f"ADVERSE drain result is LOAD-BEARING for this derivation ***",
      "the 2d-adverse dynamics and the a_0(z) derivation require each other -- neither is optional")

# the trace-charge bookkeeping against the stage-3 BH ceiling
OM_KD_MAX = mp.mpf("1.7e-6") * mp.mpf("0.26")    # stage-3 escape ceiling times the old allocation
LD_over_Q0_min = OM_L * nu0_floor / OM_KD_MAX
info(f"D4  bookkeeping: Omega_khronon-dust <= {sig(OM_KD_MAX, 3)} (stage 3's BH ceiling) with "
     f"beta = 1 forces Lambda_D/Q_0 >= {sig(LD_over_Q0_min, 3)} at the window floor.  The excitation "
     f"then passes through a w ~ 0.25 phase mid-transition -- cosmologically invisible at "
     f"Omega ~ 4e-7 -- and its pressure STILL reaches M^4 at saturation, because the wall height is "
     f"a property of the potential, not of the charge.  A trace field steers a_0 without "
     f"gravitating.")

# cluster R500 check: in-window the local shift is nil
nu_R500 = nu0_ceiling * 58
info(f"D5  clusters: at R500 (the MOND-regime radius, 0.33-0.58 a_0) the residual-share overdensity "
     f"~58x mean gives nu_loc <= {sig(nu_R500, 3)} ==> local a_0 shift <= "
     f"{sig(100 * (1 - (1 + nu_R500 ** 2) ** (mp.mpf(-1) / 4)), 2)}% -- negligible in-window; cores "
     f"are Newtonian (21.6 a_0) so their larger shift is invisible to the dynamics.")


# =================================================================================================
print()
print("=" * 100)
print("PART E -- the derived law vs the banked DESI-dressed law, and what changes downstream")
print("=" * 100)

print("\n     z      banked (DESI CPL)    derived (floor nu_0)   derived (ceiling nu_0)")
zs = ("0.5", "1", "2", "3", "5", "20", "35", "1090")
tbl = {}
for z_s in zs:
    b = a0_ratio_banked(z_s)
    d1 = a0_ratio_derived(z_s, nu0_floor)
    d2 = a0_ratio_derived(z_s, nu0_ceiling)
    tbl[z_s] = (b, d1, d2)
    print(f"   {z_s:>5s}        {sig(b, 4):>8s}              {sig(d1, 4):>8s}               {sig(d2, 4):>8s}")

check(tbl["0.5"][0] > mp.mpf("1.05") and abs(tbl["0.5"][1] - 1) < mp.mpf("1e-4"),
      f"E1  *** THE BUMP IS GONE: the banked law RISES {sig(100 * (tbl['0.5'][0] - 1), 3)}% at z = 0.5 "
      f"(the DESI-CPL dressing); the derived law is constant there to <0.01%.  The banked dressing "
      f"used DESI's evolving-w numbers inside a theory whose own dark energy is w = -1 EXACT -- it "
      f"was never self-consistent, and the derived law REPLACES it ***",
      "MSA-3D's weak-tension verdict and the MUSE confrontation were graded against the banked "
      "shape and are OWED a re-examination against the derived one")

check(min(abs(tbl[z][1] - 1) for z in ("2", "3", "5")) >= 0
      and max(abs(tbl[z][2] - 1) for z in ("2", "3", "5")) < mp.mpf("0.01"),
      "E2  through the entire forest range the derived law is constant to <1% across the whole "
      "window -- so stages 14-16's a_0(z)-dependent Jeans growth simplifies: the a_0(z)^(-1/3) "
      "factor becomes unity",
      "the banked law's 13-43% forest-range decline was the LAST place the DESI dressing entered a "
      "committed result")

# forest re-map: the alphas SHRINK (margins widen) when the banked decline is removed
H_LIT = mp.mpf("0.7")
LAM0 = mp.mpf("2.2")
C_SHARP = mp.mpf("0.698")


def alpha_of_z(z_s, law):
    z = mp.mpf(z_s)
    growth = (1 + z) ** 3 * law(z_s) ** (mp.mpf(1) / 3)
    lam_com_h = LAM0 / growth * (1 + z) * H_LIT
    return C_SHARP * lam_com_h / (2 * mp.pi)


al_banked = alpha_of_z("2", a0_ratio_banked)
al_derived = alpha_of_z("2", lambda z: a0_ratio_derived(z, nu0_floor))
check(al_derived < al_banked,
      f"E3  stage 15's worst-bin alpha (z = 2) moves {sig(al_banked, 3)} -> {sig(al_derived, 3)} "
      f"h^-1 Mpc under the derived law: the margin against Murgia+18's 0.03 widens from "
      f"{sig(mp.mpf('0.03') / al_banked, 3)}x to {sig(mp.mpf('0.03') / al_derived, 3)}x",
      "removing the never-self-consistent dressing IMPROVES the boundary sector's standing")

# w_rem(z) >= -1 always: the sector cannot mimic DESI's phantom past -- stated against interest
nu_grid = [mp.mpf("0.01"), mp.mpf("0.1"), 1, 10, 100]
w_rem = []
for nu in nu_grid:
    s = nu / mp.sqrt(1 + nu ** 2)
    p_r = -1 / mp.sqrt(1 + nu ** 2)                       # p_rem/M^4 at beta = 1
    rho_r = 1 / mp.sqrt(1 + nu ** 2) + mp.sqrt(1 + nu ** 2) - 1
    w_rem.append(p_r / rho_r)
check(all(w >= -1 for w in w_rem),
      f"E4  AGAINST INTEREST: the non-dust remainder's w(z) runs {sig(w_rem[0], 3)} -> "
      f"{sig(w_rem[-1], 3)} across the transition -- ALWAYS >= -1.  This sector CANNOT produce "
      f"DESI's preferred phantom past (w_0 + w_a = -1.61 < -1).  If DESI's evolving-w detection "
      f"stands, it is evidence AGAINST w = -1 exact -- unchanged from before, but now the a_0(z) "
      f"law no longer depends on pretending otherwise",
      "the derivation removes the inconsistency; it does not remove the DESI tension")


# =================================================================================================
print()
print("=" * 100)
print("PART F -- footing fork, health, and what is owed")
print("=" * 100)

info("F1  THE FOOTING FORK IS DECIDED AT THE ACTION LEVEL: the promotion ties a_0 to the PRESSURE "
     "scalar, which DECLINES into the past -- the canonical footing.  The alt footing (cH E(z), "
     "RISING into the past) corresponds to no scalar in this action and would put MOND ON at "
     "recombination.  Per the working rule both footings still get reported against data; but the "
     "action itself is not neutral between them, and tonight is the first time that is a theorem "
     "rather than a convention.")

info("F2  HEALTH: c_T = 1 SURVIVES (the promoted F(Y/A(Q)) is still algebraic in the metric -- the "
     "GW170817 argument is untouched).  The no-ghost THEOREM does NOT automatically survive: it was "
     "proven for the factorised form, and the promotion introduces F_YQ != 0 mixing.  The mixing "
     "carries the factor n (A4), i.e. it is trace-suppressed in-window, but the full perturbation "
     "matrix redo is OWED, not waved through.")

info("F3  ALSO OWED: (i) the CLASS re-run with the derived a_0(z) -- the committed CMB pass used "
     "MOND-off-at-recombination, which the derived law delivers MORE strongly (off-switch 0.006 -> "
     "0.0014 across the window), so no surprise is expected, but expected is not verified; "
     "(ii) the MUSE/MSA-3D re-examination against the bumpless derived shape (E1); (iii) whether "
     "K(sat) = 0 can be DERIVED rather than selected (C2) -- a brane-tension/boundary argument "
     "would make beta = 1 structural; (iv) the two-field bookkeeping: chi still carries Omega_dm "
     "(stages 10-13 untouched); the khronon needs only the trace charge of D4.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE a_0(z) LAW IS NO LONGER IMPOSED.  One covariant promotion -- a_0^2(Q) propto -K(Q), the MOND
  scale tracks the dark sector's PRESSURE -- with zero new parameters and one new relation
  (mu^2 Lambda_D^2 = M^4, "the Lagrangian vanishes at the DBI wall") makes it an output:

    1. today's coefficient survives to the digit: a_0 = kappa c sqrt(G rho_Lambda) = {sig(a0_today, 5)} m/s^2;
    2. w = -1 stays EXACT -- Gemini's theorem ("keep w=-1 ==> a_0 const") is correct for the density
       promotion and FALSE for the pressure promotion, because the total pressure evolves while the
       vacuum does not;
    3. the density promotion is EXCLUDED by one bit (a_0 would rise into the past); the pressure
       promotion is selected AND is the one with charge-suppressed backreaction;
    4. the law: constant to <1% through every MOND test (z <= 5), transition at z_t in
       [{sig(zt_lo, 3)}, {sig(zt_hi, 3)}], off at recombination ({sig(a0_ratio_derived(Z_REC, nu0_ceiling), 2)}-{sig(a0_ratio_derived(Z_REC, nu0_floor), 2)});
       the DESI-CPL bump at z = 0.5 is gone, and with it the last internal inconsistency of the
       banked law;
    5. the window nu_0 in [{sig(nu0_floor, 3)}, {sig(nu0_ceiling, 3)}] is squeezed from both ends by committed
       physics (CMB off-switch from below, RAR-via-drain from above) and is NONEMPTY;
    6. stages 2-3's adverse drain result is now LOAD-BEARING: without it the promotion is RAR-fatal.

  NOT claimed: that beta = 1 is derived (it is selected, C2); that the perturbation matrix survives
  F_YQ != 0 (owed, F2); that the CLASS pass transfers (owed, F3); that DESI's evolving w is
  explained (it is not, and cannot be -- E4, against interest).
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
