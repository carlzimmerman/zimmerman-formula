#!/usr/bin/env python3
"""
How can we bring evolving-a0 INTO the E6 orbifold construction? (honest map)
===========================================================================

Carl's intuition: "the Z from the MOND scaling is the root of Z-squared" -- i.e.
the cosmology's Z (in a0 = cH0/Z) is sqrt of the particle-physics Z^2 = 32pi/3
(the compactification volume modulus). This script checks that, then maps -- with
no flinching either way -- exactly what it would take to make the two halves
share a MECHANISM and not just a SYMBOL.

The verdict is layered and honest:
  * Carl's algebra is RIGHT: Z_cosmo = sqrt(Z^2_particle), exactly.
  * The EVOLUTION a0(z) ~ E(z) is horizon thermodynamics (a0 ~ sqrt(rho_c)),
    and it is Z-INDEPENDENT -- it does not use the construction at all.
  * A genuine link needs two planks the construction does NOT have: a MOND
    completion (a field that produces the v^4 = G M a0 law) and moduli
    stabilization fixing Lambda. Both are open. So today it is a shared number,
    not a shared mechanism -- and the prediction is stronger left standalone.

Pure stdlib.  Run:  python reviews/a0_construction_connection.py
"""

import math

C = 2.99792458e8          # m/s
MPC = 3.0857e22           # m
G = 6.674e-11
H0_KMSMPC = 71.5          # km/s/Mpc (the framework's choice)
OM, OL = 0.315, 0.685
A0_OBS = 1.20e-10         # m/s^2

Z2_PARTICLE = 32 * math.pi / 3        # the asserted compactification modulus
Z_COSMO = 2 * math.sqrt(8 * math.pi / 3)  # the MOND-scaling divisor


def H0_si():
    return H0_KMSMPC * 1e3 / MPC      # 1/s


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def part1_algebra():
    print("=" * 78)
    print("(1) Is Z_cosmo really the square root of Z^2_particle?  -> YES (Carl right)")
    print("=" * 78)
    print(f"   Z^2_particle = 32pi/3            = {Z2_PARTICLE:.6f}")
    print(f"   Z_cosmo      = 2*sqrt(8pi/3)     = {Z_COSMO:.6f}")
    print(f"   Z_cosmo^2                        = {Z_COSMO**2:.6f}")
    print(f"   match Z_cosmo^2 == Z^2_particle ? {math.isclose(Z_COSMO**2, Z2_PARTICLE)}")
    print("   => Numerically exact: the cosmology's Z is the root of the particle Z^2.")
    print("      Both are built from the SAME geometric factor 8pi/3 (= 2 * 4pi/3,")
    print("      the 3-ball volume / the Friedmann coefficient). Carl's web is real")
    print("      at the level of the NUMBER. The question is whether it is real at the")
    print("      level of a MECHANISM. Parts 2-3.\n")


def part2_evolution_mechanism():
    print("=" * 78)
    print("(2) The evolution a0(z) ~ E(z): horizon thermodynamics, and Z CANCELS")
    print("=" * 78)
    # a0 = cH0/Z = (c/2) sqrt(G rho_c) ; rho_c(z) = rho_c0 E(z)^2 ; so a0(z)=a0(0)E(z)
    a0_0 = C * H0_si() / Z_COSMO
    rho_c0 = 3 * H0_si() ** 2 / (8 * math.pi * G)
    a0_thermo = (C / 2) * math.sqrt(G * rho_c0)
    print(f"   a0(0) = cH0/Z              = {a0_0:.3e} m/s^2")
    print(f"   a0(0) = (c/2) sqrt(G rho_c) = {a0_thermo:.3e} m/s^2   "
          f"(identical: {math.isclose(a0_0, a0_thermo, rel_tol=1e-6)})")
    print(f"   observed a0               = {A0_OBS:.3e} m/s^2")
    print()
    print(f"   {'z':>5} {'E(z)':>7} {'a0(z)=a0(0)E(z)':>18} {'a0(z)/a0(0)':>12}")
    for z in (0, 1, 3, 6, 10, 14):
        print(f"   {z:>5} {E(z):>7.2f} {a0_0*E(z):>18.3e} {E(z):>12.2f}")
    print()
    print("   The ratio a0(z)/a0(0) = E(z) carries NO Z at all -- Z divides out.")
    print("   The evolution comes from rho_c(z) ~ E(z)^2 (the Friedmann equation),")
    print("   i.e. from the HORIZON / critical density, NOT from the orbifold. This")
    print("   is why the one falsifiable prediction is independent of the entire")
    print("   particle-physics skyscraper. (Good for testing; bad for 'unification'.)\n")


def part3_the_bridge():
    print("=" * 78)
    print("(3) What a REAL construction->a0 bridge needs (and what is missing)")
    print("=" * 78)
    planks = [
        ("MOND completion: a field in the action whose deep limit gives "
         "v^4 = G M a0", "ABSENT",
         "the E6 GUT is ordinary GR + gauge + chiral matter; nothing modifies the "
         "force law at a < a0. a0 enters as a phenomenological number, not a field. "
         "Supplying this is its OWN hard problem (TeVeS / Khoury superfluid / "
         "Verlinde emergent gravity) -- not contained here."),
        ("Scale pinned to H(z): a0 must track the Hubble rate", "PARTIAL / cosmological",
         "natural IF a0 ~ sqrt(rho_c) (horizon thermodynamics) -- but that pins it to "
         "the COSMOLOGY, not to the compactification. The pin is real and is exactly "
         "what gives a0(z) ~ E(z); it just doesn't run through the orbifold."),
        ("Moduli stabilization: the volume modulus Z^2 fixes Lambda (hence H0, "
         "hence a0)", "ABSENT (open problem #3)",
         "THIS is the only place the two halves could genuinely touch: if the same "
         "stabilized modulus that sets the compactification also sets the vacuum "
         "energy Lambda, and a0 = (c/2) sqrt(G rho_c) rides on sqrt(Lambda). Until "
         "stabilization is done, 'Z^2 fixes Lambda' is a wish, not a derivation."),
    ]
    for i, (name, status, why) in enumerate(planks, 1):
        print(f"   plank {i}: {name}")
        print(f"            status: {status}")
        print(f"            {why}")
        print()


def main():
    part1_algebra()
    part2_evolution_mechanism()
    part3_the_bridge()
    print("=" * 78)
    print("VERDICT -- how to bring evolving-a0 into the construction")
    print("=" * 78)
    print("  The honest answer has two tiers:")
    print()
    print("  TIER A (what is true today): the two halves share a NUMBER, not a")
    print("    mechanism. Z_cosmo^2 = Z^2_particle exactly, via the common geometric")
    print("    factor 8pi/3 -- but that factor is asserted as a modulus on one side")
    print("    and fitted as the best O(1) divisor on the other (a0_cH0_Z_check.py).")
    print("    A shared generic constant (a 3-ball volume) is not yet a shared physics.")
    print()
    print("  TIER B (the research target, if you want the bridge): make the volume")
    print("    modulus DO double duty --")
    print("      (i)  stabilize it so its minimum fixes Lambda  (-> H0 -> a0), and")
    print("      (ii) write a MOND completion in which THAT SAME modulus (the radion)")
    print("           is the MOND field, so a < a0 dynamics emerge from its profile.")
    print("    Then a0 = (c/2) sqrt(G rho_c) would be geometric, and a0(z) ~ E(z)")
    print("    would follow automatically. Both planks are unsolved and each is a")
    print("    program in its own right.")
    print()
    print("  RECOMMENDATION: keep evolving-a0 STANDALONE. Its Z-independence is a")
    print("    FEATURE -- it makes a clean, falsifiable, near-term JWST prediction")
    print("    that does NOT depend on SUSY, the exotic-free vacuum, or moduli")
    print("    stabilization. Welding it onto the E6 GUT would import all three open")
    print("    problems into the one part of the framework that is actually testable.")
    print("    The strongest move is not to unify them by fiat, but to let the")
    print("    cosmology stand or fall on a0(z) ~ E(z) at z > 10.")


if __name__ == "__main__":
    main()
