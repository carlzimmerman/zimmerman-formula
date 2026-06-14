#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
Taking it further: is scaling-MOND PREDICTED by emergent gravity, or assumed?
============================================================================

The TOE path (v12_TOE_HONEST_PATH.md) rests on one load-bearing claim: that
emergent gravity NATURALLY produces a0(z) ~ cH(z) -- scaling-MOND -- rather than
a constant a0 we impose by hand. If that claim is just an assumption, evolving-a0
is a fit. If it is forced by the thermodynamics, it is a prediction. This script
pins it down.

The key distinction is WHICH horizon sources the emergent dark sector:

  APPARENT horizon  R_A = c/H(z)        (the instantaneous Hubble surface)
  ASYMPTOTIC event horizon R_inf = c/H_inf,  H_inf = H0 sqrt(Om_L)   (the final dS)

The apparent horizon is the THERMODYNAMICALLY ACTIVE one: its first law dE = T dS
reproduces the Friedmann equations (Cai-Kim 2005; Padmanabhan). Its associated
acceleration scale is c^2/R_A = cH(z) -- which EVOLVES. So an emergent a0 tied to
the (correct) apparent horizon MUST scale as H(z). Constant-a0 would require tying
a0 to the asymptotic event horizon, which is NOT thermodynamically active during
structure formation -- a teleological, final-state surface.

=> scaling-MOND is the NATURAL emergent-gravity prediction; constant-a0 is the
   less-natural choice. And the z>10 test discriminates the two horizons.

Pure stdlib. Run:  python reviews/emergent_a0_apparent_horizon.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
G = 6.674e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
A0_OBS = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def Hz(z):
    return H0 * E(z)


def part1_apparent_horizon():
    print("=" * 80)
    print("(1) The apparent horizon is the thermodynamically ACTIVE surface")
    print("=" * 80)
    R_A = C / H0
    T = HBAR * H0 / (2 * math.pi * KB)
    a_hor = C ** 2 / R_A
    print(f"   flat FRW apparent horizon:  R_A = c/H(z)      (today {R_A/MPC/1e3:.2f} Gpc)")
    print(f"   temperature:                T = hbar H/2pi kB (today {T:.2e} K)")
    print(f"   entropy:                    S = k_B A/4 l_p^2 = pi k_B R_A^2 / l_p^2")
    print(f"   horizon acceleration scale: c^2/R_A = cH(z)   (today {a_hor:.3e} m/s^2)")
    print()
    print("   FACT (Cai-Kim 2005; Padmanabhan): the first law dE = T dS on the")
    print("   APPARENT horizon reproduces the Friedmann equations. So R_A = c/H(z) is")
    print("   the surface with active cosmological thermodynamics at EVERY epoch.")
    print("   Its acceleration scale c^2/R_A = cH(z) therefore EVOLVES.\n")


def part2_which_horizon():
    print("=" * 80)
    print("(2) Apparent (evolving) vs asymptotic (constant): the fork that decides scaling")
    print("=" * 80)
    H_inf = H0 * math.sqrt(OL)                 # asymptotic de Sitter Hubble rate
    a_apparent_today = C * H0 / Z
    a_asymptotic = C * H_inf / Z
    print(f"   IF a0 ~ c/Z x (apparent horizon accel) = cH(z)/Z  -> a0(z) EVOLVES as H(z)")
    print(f"   IF a0 ~ c/Z x (asymptotic event-horizon accel) = cH_inf/Z = CONSTANT")
    print()
    print(f"   H_inf = H0 sqrt(Om_L) = {math.sqrt(OL):.3f} H0")
    print(f"   a0(apparent, z=0) = cH0/Z           = {a_apparent_today:.3e} m/s^2")
    print(f"   a0(asymptotic, all z) = cH_inf/Z    = {a_asymptotic:.3e} m/s^2 (const)")
    print(f"   observed a0                         = {A0_OBS:.3e} m/s^2")
    print(f"   (today the two differ only by sqrt(Om_L)={math.sqrt(OL):.2f}; they DIVERGE at high z)")
    print()
    print("   The apparent horizon is the thermodynamically active one; the asymptotic")
    print("   event horizon is a final-state (teleological) surface, not active during")
    print("   matter-era structure formation. So the PHYSICALLY natural choice -> scaling.\n")


def part3_discriminator():
    print("=" * 80)
    print("(3) The z>10 test now discriminates WHICH horizon sources the dark sector")
    print("=" * 80)
    a0_app0 = C * H0 / Z
    a0_asy = C * H0 * math.sqrt(OL) / Z
    print(f"   {'z':>5}{'a0 apparent=cH(z)/Z':>22}{'a0 asymptotic (const)':>24}{'ratio':>8}")
    for z in (0, 1, 6, 10, 14):
        a_app = a0_app0 * E(z)
        print(f"   {z:>5}{a_app:>22.3e}{a0_asy:>24.3e}{a_app/a0_asy:>8.1f}")
    print()
    print("   So the evolving-vs-constant a0 test is not just 'is MOND right' -- it is")
    print("   'does the dark sector track the INSTANTANEOUS (apparent) horizon or the")
    print("   FINAL (event) horizon?' A deep question about emergent gravity, settled by")
    print("   one measurement. v_flat ratio = (a_app/a_asy)^1/4 ~ 2x at z=12-14.\n")


def part4_honest_caveats():
    print("=" * 80)
    print("(4) HONEST caveats -- this is a natural argument, not a theorem")
    print("=" * 80)
    print("   * 'a0 = (O(1)) x horizon acceleration' is the emergent-gravity HYPOTHESIS")
    print("     (Verlinde-type). The apparent-horizon choice makes it scale; that choice")
    print("     is physically natural (thermodynamically active) but not proven unique.")
    print("   * the step from horizon thermodynamics to the GALAXY-scale MOND law is")
    print("     heuristic (Verlinde's elastic-medium argument is contested).")
    print("   * Verlinde emergent gravity is in tension with DATA at cluster scales and")
    print("     the CMB -- it works ~MOND-well for galaxies, less so for clusters. The")
    print("     TOE foundation is promising, NOT confirmed.")
    print("   * the O(1) coefficient is still fit (the horizon gives 2pi; Z is 8% off).")
    print("   * at recombination a0 is ~2e4x larger but a0/cH = 1/Z is constant")
    print("     (self-similar; CMB likely safe, gate2_cmb_scaling_a0.py).\n")


def main():
    part1_apparent_horizon()
    part2_which_horizon()
    part3_discriminator()
    part4_honest_caveats()
    print("=" * 80)
    print("VERDICT -- the theoretical keystone, taken one step further")
    print("=" * 80)
    print("  BEFORE: 'we assume a0(z) ~ cH(z)' (a phenomenological choice).")
    print("  NOW:    emergent gravity built on the APPARENT horizon -- the surface whose")
    print("          first law reproduces Friedmann -- has acceleration scale cH(z), which")
    print("          EVOLVES. So a0(z) prop H(z) is the NATURAL prediction; constant-a0")
    print("          requires the asymptotic event horizon, which is not thermodynamically")
    print("          active during structure formation.")
    print()
    print("  This upgrades evolving-a0 from a fit to a (natural, not yet rigorous)")
    print("  PREDICTION of emergent gravity, and it raises the stakes of the z>10 test:")
    print("  it measures which horizon sources the dark sector. That is a real step")
    print("  further on the TOE path -- honestly bounded, and pointed at one experiment.")


if __name__ == "__main__":
    main()
