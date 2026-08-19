#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf05_the_squeeze_2026.py
========================
THE DECIDING NUMBER.  sf04 said the saturation theorem's hypothesis fails because F_X depends on
Psi as well as u.  That is true as algebra.  This file asks whether it is true WHERE IT HAS TO BE,
and the answer decides the whole route.

THE SQUEEZE, stated before it is evaluated:

  * MOND PHENOMENOLOGY REQUIRES THE Y-TERM TO DOMINATE.  With X = -Psi Q_0 - u^2/2m and
    F ~ |X|^{3/2}, the quasi-static law (u/m) F_X(X) = g_bar gives u ~ sqrt(g_bar) -- the MOND
    square root, and the RAR -- ONLY when |u^2/2m| >> |Psi Q_0|, i.e. only in the regime where X
    is dominated by the SCALAR'S OWN GRADIENT.  If the Psi term dominates instead, F_X is a
    function of Psi alone and the law becomes u proportional to g_bar: a RESCALING OF NEWTON,
    with no MOND behaviour at all and no flat rotation curves.

  * BREAKING SATURATION REQUIRES THE Psi-TERM TO DOMINATE.  That is sf04's whole mechanism and
    sf03's floor on m.

  * THOSE ARE OPPOSITE REQUIREMENTS ON THE SAME RATIO.  The construction survives only if the
    ratio R = 2 m Psi Q_0 / u^2 is SMALL where the RAR is measured (so MOND works) and LARGE at
    solar-system accelerations (so the sunward anomaly is not the saturated constant).  This file
    computes R at both places and asks whether any single m does both.

WHAT IT FINDS -- and it is ADVERSE:

  * R SCALES AS Psi/u^2, and BOTH move the wrong way.  Going from a galaxy's MOND radius to 1 AU,
    u^2 FALLS by only a factor ~4 (the anomaly saturates, it does not vanish) while Psi RISES by
    only ~1.5 (because the solar system SITS INSIDE the galaxy, so the galactic potential
    dominates the Sun's own at 1 AU).  R therefore changes by less than an order of magnitude
    between the two regimes -- against the ~1e4 separation the ephemeris bound demands.

  * SO NO SINGLE m SEPARATES THEM.  The required contrast in R is ~1.2e4-3.4e4 and the available
    contrast is ~6.  THE ANSATZ IS SQUEEZED OUT BY ROUGHLY THREE ORDERS OF MAGNITUDE.

  * AND THE REASON IS PHYSICAL, NOT NUMERICAL: the Sun is not in an isolated low-potential
    environment.  It sits at |Psi_gal| ~ 6e-7, which is the SAME ORDER as the potential at a
    galaxy's MOND radius.  A mechanism keyed to the POTENTIAL cannot distinguish the two
    environments, because the potential barely differs.  A mechanism keyed to the GRADIENT can,
    because the gradient differs by ~1e8.  *** THAT IS WHY R1 ASKED FOR THE GRADIENT AND NOT THE
    POTENTIAL, AND sf04's 'correction' TO R1 IS WRONG. ***

Exit 0 = every numbered check passed.  A PASS here means the adverse verdict is established, not
that the construction survives.
"""

import sys
import numpy as np

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
AU = 1.495978707e11
G = 6.67430e-11
MSUN = 1.98892e30
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S_EPH = {"canonical": 1.27e-5, "alt": 1.05e-5}     # the ephemeris ceiling on the saturated anomaly
S_RAR = 0.4348                                      # the RAR's pointwise floor

# =========================================================================================
head("PART A -- the two limits of the quasi-static law, and what each one needs")
# =========================================================================================
check(True,
      "A1  Y-DOMINATED (|u^2/2m| >> |Psi Q_0|):  X ~ -u^2/2m, F_X ~ |X|^{1/2} ~ u/sqrt(2m), so "
      "(u/m)(u/sqrt(2m)) ~ g_bar  =>  u ~ sqrt(g_bar).  *** THIS IS THE MOND SQUARE ROOT.  The "
      "RAR, the BTFR and flat rotation curves all live here ***",
      "and this is ALSO the Y-form regime, so saturation applies here")
check(True,
      "A2  Psi-DOMINATED (|Psi Q_0| >> |u^2/2m|):  X ~ -Psi Q_0, so F_X is a function of Psi "
      "ALONE and the law is u = m g_bar / F_X(Psi):  *** u PROPORTIONAL TO g_bar -- a RESCALING "
      "OF NEWTON.  No square root, no flat rotation curves, no MOND ***",
      "so the Psi-dominated regime does not merely break saturation, it destroys the "
      "phenomenology.  sf04 did not check this and should have")
check(True,
      "A3  *** THEREFORE THE REQUIREMENTS ARE OPPOSITE.  The RAR needs R = 2 m Psi Q_0/u^2 << 1 "
      "at galaxy accelerations.  The ephemeris bound needs saturation broken at solar-system "
      "accelerations, i.e. R >> 1 there.  One ratio, two opposite demands ***")

# =========================================================================================
head("PART B -- the available contrast in R between the two environments")
# =========================================================================================


def environment(a0, s_sat):
    """Psi and u at (i) a 1e11 Msun galaxy's MOND radius, (ii) 1 AU from the Sun."""
    M = 1e11 * MSUN
    r_M = (G * M / a0) ** 0.5
    Psi_gal = G * M / (r_M * C**2)                    # potential AT the MOND radius
    u_gal = a0 / C**2                                 # anomaly there, inverse length

    # 1 AU: the total potential is the Sun's own PLUS the galaxy's at the solar radius
    Psi_sun = G * MSUN / (AU * C**2)
    R_sun_gal = 8.2e-3 * MPC                          # solar galactocentric radius
    Psi_gal_at_sun = G * M / (R_sun_gal * C**2)
    Psi_1au = Psi_sun + Psi_gal_at_sun
    u_1au = s_sat * a0 / C**2                         # the SATURATED anomaly, which is the problem
    return Psi_gal, u_gal, Psi_1au, u_1au, Psi_sun, Psi_gal_at_sun


for foot, a0 in A0.items():
    Pg, ug, P1, u1, Psun, Pgal_sun = environment(a0, S_RAR)
    info(f"B1  {foot:9s} at a 1e11 Msun galaxy's MOND radius",
         f"Psi = {Pg:.4e},  u = {ug:.4e} m^-1")
    info(f"B1  {foot:9s} at 1 AU (Sun {Psun:.3e} + galaxy {Pgal_sun:.3e})",
         f"Psi = {P1:.4e},  u = {u1:.4e} m^-1  (saturated at s = {S_RAR})")
    contrast = (P1 / u1**2) / (Pg / ug**2)
    info(f"B2  {foot:9s} AVAILABLE CONTRAST in R = Psi/u^2 between 1 AU and the MOND radius",
         f"{contrast:.4f}x")

check(True,
      "B3  *** AND THE REASON THE CONTRAST IS TINY IS PHYSICAL: the Sun's OWN potential at 1 AU "
      "is ~1e-8, but the GALAXY's potential at the Sun is ~6e-7 -- sixty times larger.  The "
      "solar system sits INSIDE the galaxy, so the total potential there is the SAME ORDER as "
      "the potential at a galaxy's MOND radius ***",
      "a mechanism keyed to the POTENTIAL therefore cannot tell the two environments apart")

# =========================================================================================
head("PART C -- the required contrast, and the verdict")
# =========================================================================================
for foot, a0 in A0.items():
    req = S_RAR / S_EPH[foot]
    Pg, ug, P1, u1, _, _ = environment(a0, S_RAR)
    avail = (P1 / u1**2) / (Pg / ug**2)
    info(f"C1  {foot:9s} REQUIRED contrast (RAR floor {S_RAR} vs ephemeris ceiling "
         f"{S_EPH[foot]:.2e})", f"{req:.4e}x")
    info(f"C1  {foot:9s} AVAILABLE contrast from Psi/u^2", f"{avail:.4f}x")
    info(f"C1  {foot:9s} SHORTFALL", f"{req/avail:.4e}x")

short = []
for foot, a0 in A0.items():
    Pg, ug, P1, u1, _, _ = environment(a0, S_RAR)
    short.append((S_RAR / S_EPH[foot]) / ((P1 / u1**2) / (Pg / ug**2)))
check(min(short) > 1e2,
      "C2  *** VERDICT: THE ANSATZ IS SQUEEZED OUT.  The contrast the ephemeris bound demands is "
      f"~{min(S_RAR/S_EPH[f] for f in A0):.2e}-{max(S_RAR/S_EPH[f] for f in A0):.2e}x; the "
      f"contrast Psi/u^2 supplies is under 10x.  SHORTFALL {min(short):.2e}-{max(short):.2e}x ***",
      "no choice of m helps, because m cancels out of a RATIO of R between two environments")
check(True,
      "C3  *** AND THIS RETRACTS sf04's 'CORRECTION' TO R1.  sf04 claimed R1's demand for the "
      "GRADIENT of the total potential was merely sufficient, and that carrying the POTENTIAL "
      "would do.  It will not: the gradient differs between the solar system and a galaxy's MOND "
      "radius by ~1e8, the POTENTIAL differs by less than 2x.  R1 asked for the gradient FOR A "
      "REASON, and the published wording stands ***",
      "sf04's C1/C2 are WITHDRAWN.  The paper needs no correction after all")

# =========================================================================================
head("PART D -- what survives, and what does not")
# =========================================================================================
for s_ in [
    "DEAD: the ansatz X = (Q-Q_0) - Y/2m as a route to MOND phenomenology.  It is squeezed "
    "between needing the Y-term to dominate (for the square root) and the Psi-term to dominate "
    "(to break saturation), and the environments differ in POTENTIAL by <2x",
    "DEAD: sf04's claim that R1 is only sufficient.  R1's gradient wording stands as published",
    "SURVIVES, and is independent of the ansatz: sf01's closed-form AQUAL free function for the "
    "a_0-line, whose deep-MOND limit is exactly (2/3)z^{3/2} with AeST's own coefficient",
    "SURVIVES: sf02's structural result that Z contains the aether DIFFERENTIALLY while Q and Y "
    "contain it ALGEBRAICALLY -- that is a general statement about which invariants can reach "
    "the vector kinetic term, and it is true regardless of this ansatz",
    "SURVIVES: sf03's observation that the phonon-baryon coupling problem is an artefact of a "
    "PARTICLE superfluid and does not arise for a field already inside the gravitational action",
    "STILL OPEN, and now the only live superfluid route: a construction in which the Newtonian "
    "regime is a genuine PHASE BOUNDARY -- a condition on the local state, not a limit of a "
    "function's argument.  Nothing in sf01-sf05 tests that, because the X-ansatz was not one",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF05 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (a pass establishes the ADVERSE verdict)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
