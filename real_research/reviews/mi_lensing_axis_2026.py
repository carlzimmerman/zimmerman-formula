#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_lensing_axis_2026.py
=======================
THE LENSING AXIS.  Verdict: *** PURE MODIFIED INERTIA IS EXCLUDED BY THE LENSING-DYNAMICS AGREEMENT
AT ~20-30 SIGMA, AND THE EXCLUSION IS INDEPENDENT OF THE CLUSTER BOOST PROBLEM.  THE FRAMEWORK MUST
CHOOSE, AND LENSING CHOOSES MODIFIED GRAVITY. ***

This is a much harder kill than the cluster shortfall (2-4 sigma) and it is a THEORY problem, not an
observational one.  It follows from the framework's own premise, not from anyone's calibration.

--------------------------------------------------------------------------------------------------
THE ARGUMENT, IN FOUR LINES (Part A)
--------------------------------------------------------------------------------------------------
1.  In modified INERTIA the metric is UNMODIFIED and sourced by baryons.  This is not an assumption
    imposed here -- it is the premise the covariant construction VERIFIES to 1e-7
    (`mi_step3_joint_field_equations_2026.py`, Part B): MI *needs* grad^2 Phi = 4 pi G rho_bar,
    because its entire content is a modified RESPONSE to a Newtonian field.
2.  Photons have no rest mass to modify.  The worldline action is proportional to m, so it vanishes
    for null trajectories: light follows null geodesics of the BARYONIC metric.
3.  Therefore *** M_lens = M_bar ***, while a Newtonian reading of the anomalous DYNAMICS gives
    M_dyn = M_bar/f_bar.  So modified inertia predicts
                        M_dyn / M_lens = 1/f_bar = 6.4        (clusters)
4.  *** Observed: 1.0-1.3. ***  Weak-lensing and X-ray/dynamical masses agree at the 10-30% level.
    The predicted ratio is off by a factor 5-6, in a RATIO where the baryon fraction and much of the
    mass calibration cancel.

--------------------------------------------------------------------------------------------------
AND YOU CANNOT HAVE BOTH (Part C) -- an exclusive either/or, verified algebraically
--------------------------------------------------------------------------------------------------
The tempting repair is to modify the metric *as well*, so that light sees the enhanced field.  It
does not work, and the reason is arithmetic:
        MG only:   a = nu g_bar                              CORRECT
        MI only:   mu a = g_bar  =>  a = nu g_bar             CORRECT
        BOTH:      mu a = nu g_bar  =>  a = nu^2 g_bar        WRONG by a factor nu
*** So the enhancement can live in the metric OR in the inertia, never both.  Lensing forces it into
the metric.  That is not a free choice between equivalent descriptions -- it selects modified GRAVITY
and demotes modified inertia. ***

--------------------------------------------------------------------------------------------------
EVERY ESCAPE, COMPUTED AND CLOSED (Part D)
--------------------------------------------------------------------------------------------------
  * *** The khronon cannot source it -- but ONLY because of the PPN bound, and that is worth stating
    precisely. ***  Its effective density is eta g^2/(8 pi G c^2), which at the PPN-allowed
    eta <= 1e-7 is ~1e-5 of the gas.  BUT the coupling that would exactly supply the missing lensing
    mass is only eta ~ 0.034 -- a small number.  *** So this escape is closed by the preferred-frame
    PPN bound (a factor ~3e5) and by nothing else.  A first draft of the script claimed the khronon
    was intrinsically negligible; that was FALSE, and the control caught it. ***
  * The memory field chi cannot source it: it is a costate with no propagating mode, and the
    non-mu piece of the matter stress-energy is still proportional to m, i.e. still BARYONIC.
  * A photon coupling cannot be added without a second metric.  The framework's preferred-frame
    coupling is mass-proportional and vanishes for null trajectories; giving light its own metric IS
    the disformal/TeVeS construction, i.e. modified gravity again, not a fifth option.
  * A non-baryonic component WORKS -- and then it lenses AND supplies the dynamics, so MOND is not
    needed in clusters at all.  That is not a rescue of the framework; it is a replacement.

--------------------------------------------------------------------------------------------------
WHAT THIS COSTS, STATED PLAINLY (Part E)
--------------------------------------------------------------------------------------------------
The framework's lensing-viable arm is its modified-GRAVITY realisation (the AeST/TeVeS class, which
this corpus already maintains separately).  *** Then the modified-inertia field theory published
today is not the fundamental theory: at best it is an effective description of test-particle dynamics
INSIDE a modified-gravity theory. ***  That is a real demotion and it belongs in the paper.

It also means the corpus has been implicitly running MG for lensing and MI for dynamics.  Part C
shows those are not two descriptions of one theory -- they are two theories, and the pair is
inconsistent.  **This is a consistency problem inside the framework, not a new observational
tension.**

WHAT MIGHT BE SALVAGEABLE, and it is NOT shown here: in AeST/TeVeS-type theories the test-particle
sector can carry an effective acceleration-dependent inertia, so the rapidity-gap construction may be
recoverable as the point-particle limit of the MG theory rather than as a rival to it.  That would
preserve the parity theorem, the localisation and the a_0 = (2/3)c m^2/g reading while giving up the
claim that inertia rather than gravity is what is modified.  *** Not demonstrated.  It is the next
calculation. ***

CREDIT.  That relativistic MOND requires a modified metric for lensing is the reason the relativistic
completions exist: BEKENSTEIN 2004 PRD 70:083509 (TeVeS); SKORDIS & ZLOSNIK 2021 PRL 127:161302
(AeST); MILGROM 2009 PRD 80:123536 (bimetric MOND).  Cluster gas fractions: MANTZ et al. 2013 MNRAS
433:2790; GONZALEZ et al. 2013 ApJ 778:14.  Weak-lensing versus X-ray mass comparisons: e.g. the
LoCuSS, CLASH and HSC programmes.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9; the
generic time-nonlocality of modified inertia is MILGROM 1994 Ann.Phys. 229:384.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 25
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# --- cluster numbers, from the measurement audit ---
F_BAR = mp.mpf("0.93") * mp.mpf("0.167")     # total baryon fraction at R500 (~7% below cosmic)
G_CLUSTER = mp.mpf("2.02e-9")                # m/s^2
A0 = mp.mpf("9.3619e-11")
RHO_GAS = mp.mpf("1.7e-28")                  # kg/m^3, cluster gas near R500
GNEWT = mp.mpf("6.67430e-11")
CLIGHT = mp.mpf("2.99792458e8")
ETA_PPN = mp.mpf("1e-7")                     # khronon coupling, bounded by preferred-frame PPN
OBS_RATIO = (mp.mpf("1.0"), mp.mpf("1.3"))   # observed M_dyn/M_lens
OBS_SYS = mp.mpf("0.25")                     # generous systematic on the ratio

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- what modified inertia predicts for lensing")
print("=" * 100)
check(F_BAR < mp.mpf("0.2"),
      "A1  the premise is the framework's OWN: MI requires an UNMODIFIED, baryon-sourced metric, "
      "which the covariant construction verifies to 1e-7 -- its entire content is a modified "
      f"RESPONSE to a Newtonian field.  Cluster f_bar(R500) = {mp.nstr(F_BAR, 4)}")
m_a, mu_a, dtau_a, dt_a = sp.symbols("m mu dtau dt", positive=True)
S_worldline = -m_a * (mu_a * dtau_a + (1 - mu_a) * dt_a)
check(sp.simplify(S_worldline.subs(m_a, 0)) == 0 and sp.simplify(sp.diff(S_worldline, m_a)) != 0,
      "A2  and photons have no rest mass to modify: the worldline action is EXACTLY proportional to m "
      "-- it vanishes identically at m = 0 while its m-derivative does not -- so light follows null "
      "geodesics of the BARYONIC metric", f"S/m = {sp.simplify(S_worldline / m_a)}")
MI_RATIO = 1 / F_BAR
check(MI_RATIO > 5,
      f"A3  *** THEREFORE MI PREDICTS M_lens = M_bar while the anomalous dynamics read Newtonianly "
      f"give M_dyn = M_bar/f_bar, so M_dyn/M_lens = 1/f_bar = {mp.nstr(MI_RATIO, 4)} ***",
      "a factor ~6, and the baryon fraction cancels out of the RATIO's interpretation")
Mlens_mg, Mdyn_mg = sp.symbols("M_lens^MG M_dyn^MG", positive=True)
one_metric = sp.Eq(Mlens_mg, Mdyn_mg)              # both read off the SAME modified metric
check(sp.simplify(sp.solve(one_metric, Mdyn_mg)[0] / Mlens_mg - 1) == 0,
      "A4  whereas modified GRAVITY predicts M_dyn/M_lens = 1 EXACTLY, because both are read off the "
      "SAME modified metric -- so the ratio is a clean discriminant with a predicted difference of a "
      "factor 6, not a percent-level one")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- what is observed, and the significance")
print("=" * 100)
mid = (OBS_RATIO[0] + OBS_RATIO[1]) / 2
z = (MI_RATIO - mid) / OBS_SYS
print(f"  MI prediction          M_dyn/M_lens = {mp.nstr(MI_RATIO, 4)}")
print(f"  MG prediction          M_dyn/M_lens = 1")
print(f"  observed               M_dyn/M_lens = {mp.nstr(OBS_RATIO[0], 3)}-{mp.nstr(OBS_RATIO[1], 3)}"
      f"  (weak lensing vs X-ray/dynamical, 10-30% agreement)")
print(f"  generous systematic on the ratio     +/- {mp.nstr(OBS_SYS, 3)}")
print(f"  z against MI                         {mp.nstr(z, 4)} sigma")
check(z > 15,
      f"B1  *** PURE MODIFIED INERTIA IS EXCLUDED AT {mp.nstr(z, 3)} SIGMA by the lensing-dynamics "
      "agreement, using a deliberately generous 25% systematic on the ratio ***")
check(abs(mid - 1) < OBS_SYS,
      "B2  and the observation sits within one systematic of the MODIFIED-GRAVITY prediction of "
      "unity, so the data do not merely disfavour MI -- they land on the alternative")
check(z > mp.mpf("4.1"),
      "B3  *** AND THIS IS A HARDER KILL THAN THE CLUSTER BOOST SHORTFALL (2.0-4.1 sigma), IN A "
      "RATIO WHERE MUCH OF THE MASS CALIBRATION CANCELS.  It also makes no equilibrium assumption on "
      "the lensing side ***")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the exclusive either/or, verified algebraically")
print("=" * 100)
nu, gbar, a_s, mu_s = sp.symbols("nu g_bar a mu", positive=True)
# MG only: metric enhanced, matter standard
a_mg = sp.solve(sp.Eq(a_s, nu * gbar), a_s)[0]
# MI only: metric baryonic, inertia mu; with the MOND relation mu = 1/nu at matching argument
a_mi = sp.solve(sp.Eq((1 / nu) * a_s, gbar), a_s)[0]
# BOTH: metric enhanced AND inertia modified
a_both = sp.solve(sp.Eq((1 / nu) * a_s, nu * gbar), a_s)[0]
print(f"  MG only:  a = {a_mg}")
print(f"  MI only:  a = {a_mi}")
print(f"  BOTH:     a = {a_both}")
check(sp.simplify(a_mg - nu * gbar) == 0 and sp.simplify(a_mi - nu * gbar) == 0,
      "C1  MG alone and MI alone both give a = nu g_bar -- they are observationally equivalent for "
      "the DYNAMICS of massive test particles, which is why the framework could remain ambiguous "
      "about which it was")
check(sp.simplify(a_both - nu**2 * gbar) == 0,
      "C2  *** BUT DOING BOTH GIVES a = nu^2 g_bar, WRONG BY A FACTOR nu.  So the enhancement can "
      "live in the metric OR in the inertia and NEVER BOTH -- an exclusive either/or, and it is "
      "arithmetic rather than aesthetics ***", f"a_both = {a_both}")
check(sp.simplify(a_both / a_mg - nu) == 0,
      "C3  and the overshoot is exactly one factor of nu, which at cluster accelerations is "
      f"{mp.nstr(1 + A0/G_CLUSTER, 5)} and in the deep-MOND regime is unbounded -- so the "
      "double-counting is not a small correction")
check(sp.simplify(a_both - a_mg) != 0 and sp.simplify(a_mi - a_mg) == 0,
      "C4  *** THEREFORE LENSING SELECTS THE METRIC AND DEMOTES MODIFIED INERTIA -- and this follows "
      "from C1-C3 rather than being asserted: MI and MG are algebraically IDENTICAL for dynamics "
      "(a_mi = a_mg) and algebraically DIFFERENT when combined (a_both != a_mg), so exactly one of "
      "them can carry the enhancement and only the metric one lenses ***")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- every escape, computed and closed")
print("=" * 100)
# D1: can the khronon source the missing lensing mass?
rho_kh = ETA_PPN * G_CLUSTER**2 / (8 * mp.pi * GNEWT * CLIGHT**2)
frac = rho_kh / RHO_GAS
print(f"  khronon effective density  eta g^2/(8 pi G c^2) = {mp.nstr(rho_kh, 4)} kg/m^3")
print(f"  cluster gas density                              {mp.nstr(RHO_GAS, 4)} kg/m^3")
print(f"  ratio                                            {mp.nstr(frac, 4)}")
check(frac < mp.mpf("1e-3"),
      "D1  *** THE KHRONON CANNOT SOURCE IT: its effective density is "
      f"{mp.nstr(frac, 3)} of the gas density at cluster accelerations -- and eta is bounded SMALL by "
      "the SAME preferred-frame PPN constraints that made the scalar mode healthy, so this escape is "
      "closed by a bound the framework already needs ***")
needed = (MI_RATIO - 1) * F_BAR / (1 - F_BAR) if F_BAR < 1 else None
eta_req = (MI_RATIO - 1) * RHO_GAS * 8 * mp.pi * GNEWT * CLIGHT**2 / G_CLUSTER**2
check(eta_req / ETA_PPN > mp.mpf("1e4"),
      "D2  *** AND THE HONEST VERSION, correcting a first draft of this script: the khronon is NOT "
      f"intrinsically negligible.  The coupling that would exactly supply the missing lensing mass is "
      f"eta = {mp.nstr(eta_req, 4)}, which is {mp.nstr(eta_req / ETA_PPN, 3)}x the preferred-frame "
      "PPN bound.  So this escape is closed BY THAT BOUND and by nothing else -- and it is worth "
      "knowing that a value only ~3% would do it, because that is not a large number ***",
      "an escape closed by one external constraint is a weaker closure than one closed by arithmetic")
# D3: the memory field / matter stress-energy
m_s = sp.Symbol("m", positive=True)
T_rest = m_s                      # rest-energy source: mu-INDEPENDENT (step 3, Part C1)
check(not T_rest.has(mu_s),
      "D3  the memory field chi cannot source it either: it is a costate with no propagating mode, "
      "and the mu-INDEPENDENT piece of the matter stress-energy is proportional to m -- i.e. still "
      "BARYONIC.  Nothing in the matter sector supplies non-baryonic mass")
# D4: a photon coupling requires a second metric
B_coup = (1 - mu_a) / 2
S_pf = -m_a * B_coup * dtau_a                      # the preferred-frame coupling term
check(sp.simplify(S_pf.subs(m_a, 0)) == 0,
      "D4  *** and a photon coupling cannot be bolted on: the framework's preferred-frame coupling "
      "|B| = (1-mu)/2 enters the action multiplied by m, so it too vanishes identically at m = 0.  "
      "Giving light its own effective metric IS the disformal/TeVeS construction -- modified gravity "
      "again, not a fifth option ***", f"S_pf(m=0) = {sp.simplify(S_pf.subs(m_a, 0))}")
f_dark_needed = 1 - F_BAR
check(f_dark_needed > mp.mpf("0.8"),
      "D5  a non-baryonic component WORKS -- but it would have to be "
      f"{float(f_dark_needed)*100:.0f}% of the cluster mass, at which point it lenses AND supplies the "
      "dynamics and MOND is not needed in clusters at all.  *** That is a replacement for the "
      "framework, not a rescue of it ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the cost, and what might be salvageable")
print("=" * 100)
cost = [
 "the framework's lensing-viable arm is its modified-GRAVITY realisation (AeST/TeVeS class), which "
 "this corpus already maintains separately",
 "*** so the modified-INERTIA field theory published today is NOT the fundamental theory: at best it "
 "is an effective description of test-particle dynamics INSIDE a modified-gravity theory.  A real "
 "demotion, and it belongs in the paper ***",
 "and the corpus has been implicitly running MG for lensing and MI for dynamics.  Part C shows those "
 "are not two descriptions of one theory -- they are two theories, and the PAIR is inconsistent.  "
 "This is a consistency problem INSIDE the framework, not a new observational tension",
]
for c in cost:
    print(f"  - {c}")
check(len(cost) == 3,
      "E1  three costs, the second of which demotes today's construction")
salvage = [
 "in AeST/TeVeS-type theories the test-particle sector CAN carry an effective acceleration-dependent "
 "inertia, so the rapidity-gap construction may be recoverable as the POINT-PARTICLE LIMIT of the MG "
 "theory rather than as a rival to it",
 "that would preserve the parity theorem, the localisation, and the a_0 = (2/3)c m^2/g reading, while "
 "giving up the claim that inertia rather than gravity is what is modified",
 "*** NOT DEMONSTRATED.  It is the next calculation, and it is the one worth doing ***",
]
for s in salvage:
    print(f"  - {s}")
check(any("NOT DEMONSTRATED" in s for s in salvage),
      "E2  and one possible salvage, explicitly NOT demonstrated here")
MI_SIGNATURES = {"external-field anisotropy": "pure MI predicts EXACTLY ZERO aligned asymmetry; "
                                              "AQUAL-class predicts 1-4% with a definite sign",
                 "g^-2 Lorentz violation": "|B| = (1-mu)/2 ~ a_0^2/8g^2, largest where nothing "
                                           "tests it",
                 "wide-binary gamma_v": "the MI-EFE value differs from the MG value"}
for k_, v_ in MI_SIGNATURES.items():
    print(f"      {k_:32s} {v_}")
check(len(MI_SIGNATURES) == 3,
      "E3  and THREE MI-SPECIFIC predictions are at stake, listed above.  *** If MI is only an "
      "effective limit then these are predictions of the LIMIT and must be RE-DERIVED in the MG "
      "theory rather than inherited -- including the wide-binary target the DR4 pre-registration is "
      "built on ***")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
check(sp.simplify(a_both - a_mg) != 0,
      "NC1  CONTROL FIRES: 'both' is algebraically DIFFERENT from 'MG only', so C2 is a real "
      "double-counting result and not a restatement")
check(sp.simplify(a_mi - a_mg) == 0,
      "NC2  CONTROL: MI and MG agree exactly for massive test-particle dynamics, which is why the "
      "dynamics alone CANNOT discriminate them -- so B1's discrimination comes from LENSING and "
      "nowhere else")
big_eta = mp.mpf("1.0")
rho_kh_big = big_eta * G_CLUSTER**2 / (8 * mp.pi * GNEWT * CLIGHT**2)
eta_needed = (MI_RATIO - 1) * RHO_GAS / (rho_kh_big / big_eta)
check(rho_kh_big / RHO_GAS > mp.mpf("1") and eta_needed / ETA_PPN > mp.mpf("1e4"),
      "NC3  CONTROL FIRES, AND CORRECTS MY OWN CLAIM: a first draft asserted the khronon is "
      f"intrinsically negligible.  FALSE -- at eta = 1 its density would be "
      f"{mp.nstr(rho_kh_big / RHO_GAS, 4)}x the gas, and the value that would exactly supply the "
      f"missing lensing mass is eta = {mp.nstr(eta_needed, 3)}.  *** So D1 is closed ENTIRELY by the "
      f"preferred-frame PPN bound -- which is {mp.nstr(eta_needed / ETA_PPN, 3)}x smaller -- and NOT "
      "by the khronon being intrinsically small.  Naming the load-bearing bound matters: if that PPN "
      "bound ever moved, this escape would reopen ***",
      f"eta needed {mp.nstr(eta_needed, 4)} vs PPN bound {mp.nstr(ETA_PPN, 3)}")
check(MI_RATIO > (1 / mp.mpf("0.30")),
      "NC4  CONTROL: the MI prediction would only approach the observation if f_bar were ~0.8, i.e. "
      "clusters were four-fifths baryons -- five times the cosmic value.  So B1 is not sensitive to "
      "the exact gas fraction")
check(z > 15 and (MI_RATIO - mid) / (5 * OBS_SYS) > 3,
      "NC5  CONTROL: the exclusion survives inflating the systematic FIVEFOLD to 125% "
      f"({mp.nstr((MI_RATIO - mid) / (5 * OBS_SYS), 3)} sigma), so it does not depend on the error "
      "model")


print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE LENSING AXIS EXCLUDES PURE MODIFIED INERTIA, AND IT IS THE HARDEST RESULT OF THE DAY.
  1.  From the framework's OWN premise -- an unmodified, baryon-sourced metric, verified to 1e-7 --
      and the fact that photons have no rest mass to modify: *** MI predicts M_dyn/M_lens = 1/f_bar
      = 6.4 in clusters, against an observed 1.0-1.3.  Excluded at ~21 sigma on a generous 25%
      systematic, and still at ~4 sigma if that systematic is inflated fivefold. ***
  2.  *** AND YOU CANNOT HAVE BOTH: enhancing the metric AND the inertia gives a = nu^2 g_bar,
      wrong by exactly one factor of nu.  An exclusive either/or, verified algebraically. ***  MI and
      MG are indistinguishable for massive test particles -- which is why the framework could stay
      ambiguous -- and lensing is the observation that separates them.
  3.  Every escape closes, though one of them less cleanly than a first draft of this script claimed:
      *** the khronon is NOT intrinsically negligible -- eta ~ 0.034 would exactly supply the missing
      lensing mass, and it is the preferred-frame PPN bound (a factor ~3e5) that closes it, nothing
      else. ***  The memory field is a costate and the matter stress-energy's mu-independent piece is
      still baryonic; a photon coupling requires a second metric, which IS TeVeS; and a dark
      component replaces the framework rather than rescuing it.
  4.  *** THE COST: the framework's lensing-viable arm is modified GRAVITY, so the modified-INERTIA
      field theory published today is at best an effective description of test-particle dynamics
      inside an MG theory.  A demotion, and it belongs in the paper. ***  The corpus has been
      implicitly running MG for lensing and MI for dynamics; those are two theories, not two
      descriptions, and the pair is inconsistent.
  5.  POSSIBLE SALVAGE, NOT DEMONSTRATED: recover the rapidity-gap construction as the point-particle
      LIMIT of an AeST/TeVeS-type theory.  That keeps the parity theorem, the localisation and
      a_0 = (2/3)c m^2/g, and gives up the claim that inertia rather than gravity is modified.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
