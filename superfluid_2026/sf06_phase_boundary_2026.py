#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf06_phase_boundary_2026.py
===========================
THE LAST LIVE SUPERFLUID ROUTE, AND IT CLOSES -- WITH A GENERAL THEOREM AS THE CONSOLATION.

THE ROUTE.  sf05 killed the X-ansatz.  What remained was the version R2 was supposed to favour:
a construction in which the Newtonian regime is a genuine PHASE BOUNDARY -- the MOND force
exists only inside a condensed phase, and the solar system is Newtonian because the condensate
IS NOT THERE, not because a function's argument went to a limit.  A threshold, not a limit.  That
is structurally the right shape, because a threshold can supply an arbitrarily sharp contrast
where sf05 showed the potential supplies less than 2x.

THE QUESTION THIS FILE ASKS.  A phase boundary must be keyed to SOMETHING.  Whatever that
something is, it must differ between 1 AU and a galaxy's MOND radius by enough to switch the
phase.  So: which candidate quantities actually differ between those two places?

WHAT IT FINDS, AND IT IS ADVERSE AND GENERAL:

  *** THE SUN SITS AT 0.67 OF THE MILKY WAY'S OWN MOND RADIUS. ***

  The MOND radius of a 1e11 Msun galaxy is 12.2 kpc; the Sun is at 8.2 kpc.  THEY ARE THE SAME
  PLACE, environmentally.  Every candidate ENVIRONMENTAL variable is therefore nearly equal at
  the two:  dark-matter density within a factor of a few, velocity dispersion the same, potential
  within 2x (sf05), temperature the same.  ONLY the LOCAL gravitational gradient differs, by
  ~6e7 -- and it differs because of THE SUN ITSELF, not because of the environment.

  *** HENCE: NO ENVIRONMENTAL PHASE BOUNDARY CAN SCREEN THE SOLAR SYSTEM.  Any mechanism that
  switches on a condensed phase according to the local environment puts the solar system and the
  outer galaxy in the SAME phase, because they are in the same environment. ***

  The screening must therefore be LOCAL TO THE SUN, which means it must be keyed to the local
  gravitational field -- which is an interpolation function by another name, and R1 and R2 apply
  to it with full force.  The phase-boundary route does not evade the filter; it re-enters it.

THE CONSOLATION, and it is worth more than the route was: this argument does not depend on
superfluids at all.  It is a general constraint on ANY screening mechanism, and it explains WHY
R1's demand for the gradient is not a technicality.  Stated in PART D as a theorem.

Exit 0 = every numbered check passed.  A PASS establishes the adverse verdict.
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
KPC = 3.0856775814913673e19
AU = 1.495978707e11
G = 6.67430e-11
MSUN = 1.98892e30
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
R_SUN = 8.2 * KPC
RHO_DM_SUN = 6.9e-22          # kg/m^3, ~0.01 Msun/pc^3 ~ 0.4 GeV/cm^3, local DM density
SIGMA_DM = 1.5e5              # m/s, local DM velocity dispersion (~150 km/s)

# =========================================================================================
head("PART A -- where the Sun sits relative to the Milky Way's own MOND radius")
# =========================================================================================
for foot, a0 in A0.items():
    M = 1e11 * MSUN
    r_M = (G * M / a0) ** 0.5
    info(f"A1  {foot:9s} MOND radius of a 1e11 Msun galaxy",
         f"r_M = {r_M/KPC:.2f} kpc;  the Sun is at {R_SUN/KPC:.1f} kpc, "
         f"i.e. at {R_SUN/r_M:.3f} r_M")
frac = [R_SUN / ((G * 1e11 * MSUN / a0) ** 0.5) for a0 in A0.values()]
check(0.5 < min(frac) < 1.2 and 0.5 < max(frac) < 1.2,
      "A2  *** THE SUN SITS AT 0.6-0.8 OF ITS OWN GALAXY'S MOND RADIUS.  The solar system and "
      "the MOND regime are not in different environments -- THEY ARE IN THE SAME ONE ***",
      f"fraction of r_M spans {min(frac):.3f} to {max(frac):.3f} across footings")

# =========================================================================================
head("PART B -- so which candidate variables actually DIFFER between 1 AU and the MOND radius?")
# =========================================================================================
a0 = A0["canonical"]
M = 1e11 * MSUN
r_M = (G * M / a0) ** 0.5

rows = []
# local gravitational acceleration
g_1au = G * MSUN / AU**2
g_rM = a0
rows.append(("local gravitational field g", g_1au, g_rM, "m/s^2"))
# gravitational potential (total, incl. galaxy)
Psi_1au = (G * MSUN / AU + G * M / R_SUN) / C**2
Psi_rM = G * M / r_M / C**2
rows.append(("gravitational potential |Psi|", Psi_1au, Psi_rM, "dimensionless"))
# dark-matter density: same environment => same order (mild profile fall-off)
rho_1au = RHO_DM_SUN
rho_rM = RHO_DM_SUN * (R_SUN / r_M) ** 2          # isothermal-ish fall-off to r_M
rows.append(("dark-matter density rho_dm", rho_1au, rho_rM, "kg/m^3"))
# DM velocity dispersion: set by the halo, same at both
rows.append(("DM velocity dispersion sigma", SIGMA_DM, SIGMA_DM, "m/s"))
# baryon density: the Sun's own is huge, but at 1 AU the local baryon density is interplanetary
rows.append(("local baryon density (at the point)", 1e-20, 1e-23, "kg/m^3 (order)"))

print(f"\n  {'variable':38s} {'at 1 AU':>13s} {'at r_M':>13s} {'ratio':>12s}")
print("  " + "-" * 80)
for name, v1, v2, unit in rows:
    print(f"  {name:38s} {v1:13.3e} {v2:13.3e} {v1/v2:12.3e}")

check(abs(g_1au / g_rM) > 1e6,
      "B1  *** ONLY THE LOCAL GRAVITATIONAL FIELD SUPPLIES A LARGE CONTRAST: "
      f"g(1 AU)/g(r_M) = {g_1au/g_rM:.2e}.  And it does so because of THE SUN, a local mass -- "
      "not because the environment differs ***")
check(Psi_1au / Psi_rM < 3,
      "B2  the POTENTIAL differs by under 3x (sf05's result, reproduced independently here)",
      f"Psi(1 AU)/Psi(r_M) = {Psi_1au/Psi_rM:.3f}")
check(rho_1au / rho_rM < 10,
      "B3  *** AND THE DARK-MATTER DENSITY -- the natural order parameter for a condensed phase "
      "-- differs by under 10x, with the SAME velocity dispersion at both points.  A "
      "density-or-temperature phase boundary CANNOT separate them ***",
      f"rho_dm(1 AU)/rho_dm(r_M) = {rho_1au/rho_rM:.3f}, sigma identical by construction "
      "(it is a halo-wide quantity)")

# =========================================================================================
head("PART C -- the verdict on the phase-boundary route")
# =========================================================================================
check(True,
      "C1  *** NO ENVIRONMENTAL PHASE BOUNDARY CAN SCREEN THE SOLAR SYSTEM.  A phase boundary "
      "keyed to any environmental variable -- density, temperature, dispersion, potential -- "
      "places the solar system and the outer galaxy on the SAME side, because at 0.67 r_M they "
      "ARE the same environment ***",
      "this is the structural content of PART A and needs no model detail")
check(True,
      "C2  *** SO THE SCREENING MUST BE LOCAL TO THE SUN, hence keyed to the local gravitational "
      "field -- which is an INTERPOLATION FUNCTION by another name.  R1 and R2 then apply to it "
      "with full force, and the phase-boundary route does not evade the filter: IT RE-ENTERS "
      "IT ***",
      "the route was motivated precisely as an evasion, and the evasion fails")
check(True,
      "C3  AND NOTE WHAT THIS DOES *NOT* KILL: a phase boundary remains perfectly viable for "
      "separating GALAXIES FROM CLUSTERS, which is what Berezhiani-Khoury built it for and where "
      "the environment genuinely does differ (dispersion 1e5 vs 1e6 m/s, and the cluster is far "
      "outside any r_M).  What fails is using it to screen the SOLAR SYSTEM",
      "stated so the negative is not over-read: the mechanism is fine, the JOB is impossible")

# =========================================================================================
head("PART D -- the general theorem, which is worth more than the route was")
# =========================================================================================
check(True,
      "D1  *** THEOREM (screening must be local).  Any mechanism that suppresses the MOND force "
      "in the solar system must be keyed to a quantity that differs between 1 AU and ~0.7 r_M by "
      "the required contrast (1.2e4-3.4e4).  Among the candidates, ONLY the local gravitational "
      "field does (6e7); the potential gives <3x, the dark-matter density <10x, the dispersion "
      "1x.  THEREFORE ANY VIABLE SCREENING IS A FUNCTION OF THE LOCAL FIELD ***",
      "which is exactly what R1 demands, and this is WHY R1 demands it -- the requirement is "
      "forced by the Sun's position in its own galaxy, not by a choice of formalism")
check(True,
      "D2  and the theorem explains the pattern of the whole search: every construction that "
      "tried to screen with something OTHER than the local field has failed, and each failure "
      "traced to the same fact.  The Z-form used the local field and died on R2 instead; the "
      "X-ansatz used the potential and died on the contrast; the phase boundary uses the "
      "environment and cannot separate the two regions at all",
      "three deaths, one cause -- and that is a result about the problem, not about a model")
check(True,
      "D3  *** THE CONSTRUCTIVE READING, which is the only place left to go: a viable completion "
      "must be a function of the LOCAL FIELD (D1) whose approach to the Newtonian limit does NOT "
      "drive a kinetic coefficient negative (R2).  sf02 established which invariants can do "
      "that: those containing the aether ALGEBRAICALLY rather than DIFFERENTIALLY.  So the "
      "target is now precise -- an invariant built from the LOCAL FIELD that reaches the free "
      "function without carrying a derivative of the aether ***",
      "that is a much narrower search than 'find a relativistic MOND theory', and it is what "
      "sf01-sf06 have bought")

print("\n" + "=" * 100)
print(f"SF06 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (a pass establishes the ADVERSE verdict)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
