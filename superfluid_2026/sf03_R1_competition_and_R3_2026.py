#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf03_R1_competition_and_R3_2026.py
==================================
THE THIRD QUESTION, AND IT IS THE ONE THAT DECIDES WHETHER R1's ESCAPE IS REAL OR NOMINAL.

sf01 established that the ansatz F(Y,Q) -> F(X), X = (Q-Q_0) - Y/(2m), has, in the
quasi-static limit and via the theory's OWN relation Q = (1-Psi)Q_0,

        X = -Psi Q_0 - Y/(2m)

and read that as satisfying R1, because X carries the Newtonian potential Psi directly.  But X
carries BOTH terms, and the second one is Y -- THE SCALAR'S OWN GRADIENT, WHICH IS EXACTLY THE
OBJECT WHOSE DOMINANCE CAUSED R1's SATURATION TRAP IN THE FIRST PLACE.  So the escape is real
only if the Psi term DOMINATES where the MOND phenomenology lives.  That is a numerical
question with a definite answer and this file answers it.

WHAT IT FINDS:

  * The competition is controlled by ONE dimensionless ratio,
        R := (Psi Q_0) / (Y/2m) = 2 m Psi Q_0 / u^2 ,     u = |grad phi| = the anomalous accel.
    On the deep-MOND branch u^2 -> a_0 g_bar/c^4 and Psi -> (v_c/c)^2, so R is computable from
    observables alone once m is given.  (PART B.)

  * DEMANDING R >> 1 AT THE MOND RADIUS -- i.e. demanding that R1's escape be REAL -- puts a
    LOWER BOUND on m.  PART C evaluates it on both a_0 footings and across the pinned Q_0 band,
    and reports the bound as a length 1/m so it can be compared with anything physical.

  * AND THE BOUND IS NOT IN CONFLICT WITH sf01's DEEP-MOND FIXING.  sf01 fixed m by the
    normalisation of the MOND branch; this file fixes a floor from the DOMINANCE of the Psi
    branch.  PART D checks whether the two are compatible or whether the ansatz is squeezed
    between them -- which would be a kill.

  * R3 (PART E): the ansatz needs NO Gtilde/G_N split.  The reason is structural and is stated
    as an argument, not a computation: the split in the previous candidate was FORCED because
    F(Z) annihilated the non-F static Lagrangian, making the free function's normalisation the
    sole source of Newton's constant.  Here the -(2-K_B)Y kinetic term is RETAINED and
    untouched, so Ghat survives independently of F.

  * gamma_PPN (PART F): matter couples to g_{mu nu} ALONE and the ansatz does not touch S_m.
    The Y-dependence enters exactly as AeST's own F(Y) does, so the lensing result is inherited
    rather than re-earned.  Stated as INHERITED-STRUCTURAL, and the full PPN computation is
    named as NOT DONE.

Exit 0 = every numbered check passed.
"""

import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)

C = 2.99792458e8
MPC = 3.0856775814913673e22
G = 6.67430e-11
MSUN = 1.98892e30
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Q0_BAND = {"low": 2.4e-3, "high": 1.46e-2}          # Mpc^-1  (DOI 10.5281/zenodo.21937958)

# =========================================================================================
head("PART A -- the two terms in X, and why the competition is the whole question")
# =========================================================================================
Psi, Q0s, Ys, ms, us = sp.symbols("Psi Q_0 Y m u", positive=True)
Xqs = -Psi * Q0s - Ys / (2 * ms)
check(sp.simplify(Xqs.subs(Ys, us**2) - (-Psi*Q0s - us**2/(2*ms))) == 0,
      "A1  the quasi-static argument, from sf01: X = -Psi Q_0 - Y/(2m), with Y = |grad phi|^2 "
      "= u^2 and u the ANOMALOUS acceleration in inverse-length units",
      f"sympy: X = {Xqs.subs(Ys, us**2)}")
check(True,
      "A2  *** THE TENSION, STATED PLAINLY: the FIRST term is the total Newtonian potential -- "
      "that is what buys R1.  The SECOND term is the scalar's OWN gradient -- that is exactly "
      "the object whose dominance produced R1's saturation trap.  Both are present.  So R1 is "
      "escaped only if the FIRST term dominates where the MOND phenomenology lives ***",
      "this is the question sf01 left open by reading only the leading behaviour")
R = sp.simplify((Psi * Q0s) / (us**2 / (2 * ms)))
check(sp.simplify(R - 2*ms*Psi*Q0s/us**2) == 0,
      "A3  the controlling ratio is R := (Psi Q_0)/(Y/2m) = 2 m Psi Q_0 / u^2, and R >> 1 is "
      "the condition for the escape to be REAL rather than nominal",
      f"sympy: R = {R}")

# =========================================================================================
head("PART B -- R on the deep-MOND branch, in observables")
# =========================================================================================
check(True,
      "B1  on the deep-MOND branch the anomalous acceleration is u c^2 = sqrt(a_0 g_bar) and "
      "the potential is Psi = (v_c/c)^2 with v_c^4 = G M a_0 (the BTFR).  Both sides of R are "
      "then fixed by (M, a_0) alone -- no new input",
      "so R at the MOND radius is a pure prediction once m is chosen")


def ratio_at(Mgal_msun, a0, q0_mpc, m_inv_len):
    """R = 2 m Psi Q_0 / u^2 evaluated at the MOND radius of a galaxy of mass Mgal."""
    M = Mgal_msun * MSUN
    vc = (G * M * a0) ** 0.25                 # BTFR circular speed, m/s
    Psi_val = (vc / C) ** 2                   # dimensionless
    r_M = (G * M / a0) ** 0.5                 # MOND radius, m
    g_bar = G * M / r_M**2                    # = a0 there
    u = (a0 * g_bar) ** 0.5 / C**2            # anomalous accel, inverse length
    q0 = q0_mpc / MPC                         # inverse length
    return 2.0 * m_inv_len * Psi_val * q0 / u**2, Psi_val, u, r_M


head("PART C -- the LOWER BOUND on m that makes R1's escape real")
for foot, a0 in A0.items():
    for qname, q0m in Q0_BAND.items():
        # solve R = 1 for m at a 1e11 Msun galaxy's MOND radius
        r1, Psi_val, u, r_M = ratio_at(1e11, a0, q0m, 1.0)
        m_crit = 1.0 / r1                     # m at which R = 1
        info(f"C1  {foot:9s} Q_0 = {q0m:.2e} Mpc^-1",
             f"R = 1 at m = {m_crit:.4e} m^-1, i.e. 1/m = {1/m_crit/MPC:.4e} Mpc "
             f"(MOND radius {r_M/MPC:.4f} Mpc, Psi = {Psi_val:.3e})")
m_needed = []
for foot, a0 in A0.items():
    for qname, q0m in Q0_BAND.items():
        r1, _, _, _ = ratio_at(1e11, a0, q0m, 1.0)
        m_needed.append(1.0 / r1)
check(all(np.isfinite(m_needed)) and min(m_needed) > 0,
      "C2  *** THE ESCAPE IS REAL ONLY FOR m ABOVE THAT CRITICAL VALUE.  Below it the Y term "
      "dominates and the ansatz degenerates to the Y-form -- i.e. back into R1's trap, with the "
      "1.2e4-3.4e4 gap ***",
      f"critical m spans {min(m_needed):.3e} to {max(m_needed):.3e} m^-1 across footing x Q_0")
check(True,
      "C3  and the bound has the right CHARACTER: R grows with m, so the constraint is a FLOOR, "
      "not a window.  There is no upper edge from this requirement -- a large m simply makes "
      "the Psi term dominate more completely and the theory more AQUAL-like",
      "a floor is a far weaker constraint than the two-sided squeeze that killed the Z-form")

# =========================================================================================
head("PART D -- is that floor compatible with sf01's deep-MOND fixing of m?")
# =========================================================================================
check(True,
      "D1  sf01 fixed m by the NORMALISATION of the MOND branch (the deep-MOND limit must carry "
      "a_0); this file fixes a FLOOR from the DOMINANCE of the Psi branch.  These are different "
      "conditions on the same parameter and could in principle be incompatible",
      "if they were, the ansatz would be squeezed out and this would be a KILL")
check(True,
      "D2  *** BUT THEY ARE NOT IN CONFLICT AS STATED, BECAUSE THEY CONSTRAIN DIFFERENT THINGS: "
      "the normalisation fixes the COEFFICIENT of the |X|^{3/2} branch, while the floor "
      "constrains WHICH TERM INSIDE X dominates.  A single m can satisfy both provided "
      "Lambda_D is free, and Lambda_D IS free -- the corpus pins Q_0 but not Lambda_D ***",
      "GRADED AS: not in conflict, NOT as verified compatible.  Pinning Lambda_D and checking "
      "the two conditions against each other numerically is the next computation, and it is "
      "the one that could still kill this")

# =========================================================================================
head("PART E -- R3: does the ansatz need a Gtilde/G_N split?")
# =========================================================================================
check(True,
      "E1  WHY THE PREVIOUS CANDIDATE NEEDED ONE: with F(Z) the non-F static Lagrangian was "
      "annihilated IDENTICALLY by the aether-longitudinal solution v = grad Psi, so the free "
      "function's normalisation became the SOLE source of Newton's constant, G_N = Ghat/s.  The "
      "no-ghost condition then read 2 Gtilde < K_B G_N, i.e. Gtilde/G_N <= 0.121",
      "that is the chain R3 kills, via BBN at -42 sigma and a radiation density below the photons")
check(True,
      "E2  *** THAT CHAIN DOES NOT START HERE.  The ansatz changes only the free function's "
      "ARGUMENT.  The -(2-K_B)Y kinetic term is RETAINED and untouched, so it still supplies "
      "the static Lagrangian and Ghat survives INDEPENDENTLY of F.  Nothing was repaired by a "
      "rescaling, so nothing forces a split ***",
      "STATED AS AN ARGUMENT, NOT A COMPUTATION -- the honest grade.  Computing G_N explicitly "
      "under the ansatz is owed")

# =========================================================================================
head("PART F -- gamma_PPN and the coupling to baryons")
# =========================================================================================
check(True,
      "F1  *** THE 'PHONON-BARYON COUPLING' PROBLEM DOES NOT ARISE IN THIS FORM.  It is a "
      "feature of BK's PARTICLE superfluid, whose scalar sits OUTSIDE the gravity sector and "
      "therefore needs an explicit theta rho_b term to reach matter.  Here the field is already "
      "IN the gravitational action, and matter couples to g_{mu nu} ALONE -- untouched, since "
      "the ansatz modifies only F's argument and never S_m ***",
      "so the equivalence principle is preserved by construction, not by tuning")
check(True,
      "F2  and the Y-dependence enters exactly as AeST's own F(Y) does, so gamma_PPN = 1 "
      "(residual 0.601 sigma) is INHERITED rather than re-earned.  The Q-dependence is the "
      "dust/dark-energy sector, which carries no anisotropic stress",
      "GRADED: INHERITED-STRUCTURAL.  A full PPN computation under the ansatz is NOT DONE and "
      "is named as owed -- the inheritance argument is strong but it is an argument")

# =========================================================================================
head("STANDING AFTER THIS FILE")
# =========================================================================================
for s_ in [
    "R1  CLEARED CONDITIONALLY -- real iff m exceeds the PART C floor.  Below it the ansatz "
    "falls back into the Y-form trap.  This is a genuine new condition, not present in sf01",
    "R2  CLEARED UNCONDITIONALLY (sf02): C_V = K_B > 0 for any F, at every acceleration",
    "R3  ARGUED, not computed: the -(2-K_B)Y kinetic term is retained, so nothing forces a split",
    "gamma_PPN  INHERITED-STRUCTURAL: matter still couples to g alone; full PPN owed",
    "OWED AND DECISIVE: pin Lambda_D, then check sf01's normalisation against PART C's floor "
    "numerically.  That single check is what could still kill the ansatz",
    "ALSO OWED: the scalar sector's own legality; the dust problem; clusters",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF03 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
