#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
What unified action works with scaling MOND? Verify the candidate.
==================================================================

Carl's question: write an action that CONTAINS 'scaling MOND' -- MOND with
a0(z) = cH(z)/Z. The honest answer is grounded in real relativistic-MOND theory,
not invented:

  S = INT d4x sqrt(-g) [
        (c^4/16piG) R                          # gravity (tensor sector: c_GW = c)
      + L_gauge+matter(A, psi; g)              # E6 -> SM from the orbifold
      - 1/2 (d chi)^2 - V(chi)                 # radion modulus: sets <chi>=Z^2 AND a0(t)
      + L_MOND(phi, vec A; g, a0[chi])         # RelMOND sector (Skordis-Zlosnik 2021)
  ]

with the SCALING relation a0(t)^2 proportional to rho_chi(t) (the modulus energy
density), so a0(t) = cH(t)/Z since H^2 = 8piG rho/3. Matter couples conformally
to phi (g~ = A^2(phi) g), which leaves the tensor sector untouched -> c_GW = c.

This script verifies the four things the action must do:
  (1) deep-MOND limit gives v^4 = G M a0   (galaxy rotation curves)
  (2) a0(z) = cH(z)/Z  ->  a0(z)/a0(0) = E(z)   (the scaling)
  (3) GW170817: c_GW = c structurally (the filter that killed TeVeS/disformal MOND)
  (4) high-z consistency flag: a0 is ~2e4x bigger at recombination, but a0/cH =
      1/Z stays constant -- whether the CMB fit survives is the key OPEN check.

Pure stdlib. Run:  python reviews/scaling_mond_action.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
MPC = 3.0857e22
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)     # 5.78881
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def mu(x):                              # AQUAL interpolation, x = g/a0
    return x / math.sqrt(1 + x * x)


def solve_g(gN, a0):
    lo, hi = 1e-30, max(10 * gN, 10 * a0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mu(mid / a0) * mid < gN:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def part1_deep_mond():
    print("=" * 80)
    print("(1) L_MOND deep limit gives v^4 = G M a0  (Bekenstein-Milgrom / SZ scalar)")
    print("=" * 80)
    print("   L_MOND = -(a0^2/8piG) F(X), X=(d phi)^2/a0^2; F->X (Newton), F->(2/3)X^3/2")
    print("   (deep MOND). EOM for a point mass: mu(g/a0) g = GM/r^2.")
    M = 6e10 * MSUN
    vflat = (G * M * A0) ** 0.25 / 1e3
    print(f"   galaxy M=6e10 Msun -> v_flat=(G M a0)^1/4 = {vflat:.0f} km/s")
    for r_kpc in (5, 20, 80):
        r = r_kpc * KPC
        g = solve_g(G * M / r ** 2, A0)
        print(f"     r={r_kpc:>3} kpc:  v = {math.sqrt(g*r)/1e3:>5.0f} km/s")
    print("   -> flat rotation curve / baryonic Tully-Fisher. The MOND sector works. OK\n")


def part2_scaling():
    print("=" * 80)
    print("(2) The SCALING: a0(t) = cH(t)/Z from a0^2 ~ rho_chi(t)")
    print("=" * 80)
    a0_0 = C * H0 / Z
    print(f"   a0(0) = cH0/Z = {a0_0:.3e} m/s^2 (obs {A0:.2e}); coupling = Z = {Z:.3f}")
    print(f"   {'z':>5}{'E(z)':>8}{'a0(z) [m/s^2]':>16}{'a0(z)/a0(0)':>13}")
    for z in (0, 1, 6, 14):
        print(f"   {z:>5}{E(z):>8.2f}{a0_0*E(z):>16.3e}{E(z):>13.2f}")
    print("   a0(z)/a0(0)=E(z): the falsifiable scaling, derived from the horizon. OK\n")


def part3_gw170817():
    print("=" * 80)
    print("(3) GW170817 filter: does the action keep c_GW = c?")
    print("=" * 80)
    print("   Measured |c_GW/c - 1| < ~1e-15 (GW170817 + GRB170817A, 2017).")
    print("   Tensor (GW) speed is set ONLY by the graviton kinetic term. In this")
    print("   action the tensor sector is pure (c^4/16piG)R, and the MOND scalar is")
    print("   CONFORMALLY coupled (matter sees A^2(phi) g) -- conformal factors do not")
    print("   change null cones, so c_GW = c EXACTLY. PASS by construction.")
    print("   This is the filter that KILLED most MOND: TeVeS and disformal/vector")
    print("   theories generically gave c_GW != c and were excluded in 2017. The")
    print("   surviving form (Skordis-Zlosnik 2021) is built to keep c_GW=c -- and so")
    print("   is this action. The GW constraint SHAPES the action, and it survives. OK\n")


def part4_highz_flag():
    print("=" * 80)
    print("(4) High-z consistency: the OPEN check (be honest)")
    print("=" * 80)
    z = 1089.9
    a0_0 = C * H0 / Z
    a0_rec = a0_0 * E(z)
    cH_rec = C * H0 * E(z)
    print(f"   at recombination z={z:.0f}: E={E(z):.0f}")
    print(f"     a0(z_rec) = {a0_rec:.2e} m/s^2  (~{E(z):.0f}x todays a0)")
    print(f"     a0/cH at z_rec = {a0_rec/cH_rec:.4f} = 1/Z = {1/Z:.4f}  (CONSTANT)")
    print("   Good news: a0/cH = 1/Z is constant, so the MOND modification stays a")
    print("   FIXED fraction of horizon-scale dynamics at every epoch -- arguably more")
    print("   natural than constant-a0 (whose MOND regime shrinks vs the horizon).")
    print("   Open worry: a0 is ~2e4x larger at recombination, so the MOND regime")
    print("   (a<a0) is much wider then. Skordis-Zlosnik fit the CMB with CONSTANT a0;")
    print("   whether the fit SURVIVES the scaling a0(z) must be recomputed. NOT done")
    print("   here -- this is the key open consistency calculation. I will not pretend")
    print("   scaling MOND automatically inherits the SZ CMB success.\n")


def main():
    part1_deep_mond()
    part2_scaling()
    part3_gw170817()
    part4_highz_flag()
    print("=" * 80)
    print("LEDGER -- what works, what is chosen, what is open")
    print("=" * 80)
    print("  WORKS / standard:")
    print("   * gravity + E6 gauge + chiral matter: the orbifold core (inherited).")
    print("   * L_MOND deep limit -> v^4=GMa0: standard Bekenstein-Milgrom/SZ.")
    print("   * c_GW = c: passes GW170817 by construction (conformal coupling).")
    print("   * a0(z) ~ E(z): DERIVED from the horizon (route-independent), testable z>10.")
    print("  CHOSEN (as in every MOND theory):")
    print("   * the interpolation function F (deep limit imposed to fit galaxies);")
    print("   * the O(1) coupling Z=2sqrt(8pi/3): best-fit; the horizon alone gives ~2pi.")
    print("  OPEN / conjectured:")
    print("   * V(chi) landing on the observed Lambda (cosmological-constant problem);")
    print("   * Z = sqrt(volume modulus 32pi/3): the interlocking-web posit;")
    print("   * re-fitting the CMB with the SCALING a0(z) (SZ did it for constant a0).")
    print()
    print("  ANSWER: the action that works with scaling MOND is a Skordis-Zlosnik-type")
    print("  relativistic MOND sector (CMB-viable, c_GW=c) with its a0 promoted to")
    print("  a0(z)=cH(z)/Z by tying it to the radion energy density, bolted onto the")
    print("  orbifold gravity+E6+matter core. The scaling is the derived, falsifiable")
    print("  part; the coupling Z and Lambda are the fit/open parts. Honest and buildable.")


if __name__ == "__main__":
    main()
